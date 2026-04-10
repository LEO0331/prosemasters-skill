from __future__ import annotations

import json
import os
import subprocess
import tempfile
import time
import uuid
from http.server import BaseHTTPRequestHandler
from pathlib import Path
from typing import Any

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import (
    is_authorized,
    is_origin_allowed,
    normalize_payload,
    read_json_body,
    render_skill_md,
    render_wiki_md,
    repo_root_from_api_file,
    send_json,
    validate_payload,
)


def _exec_cmd(cmd: list[str], cwd: Path, step: str, must_succeed: bool = False) -> dict[str, Any]:
    t0 = time.time()
    timeout_sec = int(os.getenv("MPB_SUBPROCESS_TIMEOUT_SEC", "25"))
    expose_tool_logs = os.getenv("MPB_EXPOSE_TOOL_LOGS", "").strip().lower() in {"1", "true", "yes", "on"}
    try:
        cp = subprocess.run(
            cmd,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout_sec,
        )
    except subprocess.TimeoutExpired:
        rec = {
            "step": step,
            "tool": cmd[1] if len(cmd) > 1 else cmd[0],
            "status": "failed",
            "exit_code": 124,
            "duration_ms": int((time.time() - t0) * 1000),
            "stdout": "",
            "stderr": f"timed out after {timeout_sec}s",
        }
        if must_succeed:
            raise RuntimeError(f"{step} failed (timeout)") from None
        return rec

    rec = {
        "step": step,
        "tool": cmd[1] if len(cmd) > 1 else cmd[0],
        "status": "success" if cp.returncode == 0 else "failed",
        "exit_code": cp.returncode,
        "duration_ms": int((time.time() - t0) * 1000),
        "stdout": (cp.stdout or "")[:1200] if expose_tool_logs else "",
        "stderr": (cp.stderr or "")[:1200] if expose_tool_logs else "",
    }
    if must_succeed and cp.returncode != 0:
        raise RuntimeError(f"{step} failed (exit={cp.returncode})")
    return rec


def build_tool_plan(data: dict) -> dict:
    category_tool = {
        "works": ["tools/literature_parser.py", "tools/meter_analyzer.py"],
        "criticism": ["tools/literature_parser.py"],
        "letters": ["tools/literature_parser.py"],
        "biography": ["tools/biography_mapper.py"],
        "citation": ["tools/citation_manager.py"],
    }
    routes = []
    for item in data.get("source_materials", []):
        c = item.get("category", "works")
        routes.append(
            {
                "category": c,
                "title": item.get("title", ""),
                "tools": category_tool.get(c, ["tools/literature_parser.py"]),
            }
        )
    return {"mode": "planned", "routes": routes, "executions": []}


def _write_source_files(work: Path, source_materials: list[dict[str, Any]]) -> dict[str, list[Path]]:
    categorized: dict[str, list[Path]] = {
        "works": [],
        "criticism": [],
        "letters": [],
        "biography": [],
        "citation": [],
    }
    for i, item in enumerate(source_materials):
        category = str(item.get("category", "works")).strip().lower()
        if category not in categorized:
            category = "works"
        content = str(item.get("content", "")).strip()
        if not content:
            continue

        ext = ".txt"
        if category == "biography" and ("," in content or "\t" in content):
            ext = ".csv"

        p = work / f"{category}-{i}{ext}"
        p.write_text(content + "\n", encoding="utf-8")
        categorized[category].append(p)

    return categorized


def _execute_category_tools(
    repo_root: Path,
    work: Path,
    data: dict[str, Any],
) -> tuple[list[dict[str, Any]], Path]:
    py = "python3"
    tools = repo_root / "tools"
    records: list[dict[str, Any]] = []

    sources = _write_source_files(work, data.get("source_materials", []))
    works = sources["works"]
    criticism = sources["criticism"]
    letters = sources["letters"]
    biography = sources["biography"]
    citation = sources["citation"]

    max_biography_steps = int(os.getenv("MPB_MAX_BIOGRAPHY_STEPS", "8"))

    # works/criticism/letters parser route
    combined_textual = works + criticism + letters
    textual_parsed = work / "textual.parsed.json"
    if combined_textual:
        records.append(
            _exec_cmd(
                [py, str(tools / "literature_parser.py"), *[str(x) for x in combined_textual], "-o", str(textual_parsed)],
                repo_root,
                "parse_textual_corpus",
                must_succeed=False,
            )
        )
    else:
        records.append(
            {
                "step": "parse_textual_corpus",
                "tool": "tools/literature_parser.py",
                "status": "skipped",
                "reason": "no works/criticism/letters provided",
            }
        )

    # meter route for works only
    if works and textual_parsed.exists():
        meter_out = work / "works.meter.json"
        records.append(
            _exec_cmd(
                [py, str(tools / "meter_analyzer.py"), str(textual_parsed), "-o", str(meter_out)],
                repo_root,
                "analyze_meter",
                must_succeed=False,
            )
        )
    else:
        records.append(
            {
                "step": "analyze_meter",
                "tool": "tools/meter_analyzer.py",
                "status": "skipped",
                "reason": "no works provided or parser output missing",
            }
        )

    # biography mapping (per file)
    if biography:
        if len(biography) > max_biography_steps:
            records.append(
                {
                    "step": "map_biography_limit",
                    "tool": "tools/biography_mapper.py",
                    "status": "skipped",
                    "reason": f"truncated to first {max_biography_steps} biography sources",
                }
            )
        for i, b in enumerate(biography[:max_biography_steps]):
            bio_out = work / f"biography-{i}.json"
            records.append(
                _exec_cmd(
                    [py, str(tools / "biography_mapper.py"), str(b), "-o", str(bio_out)],
                    repo_root,
                    f"map_biography_{i}",
                    must_succeed=False,
                )
            )
    else:
        records.append(
            {
                "step": "map_biography",
                "tool": "tools/biography_mapper.py",
                "status": "skipped",
                "reason": "no biography sources provided",
            }
        )

    # citation route (prefer citation category, fallback to all source files)
    all_sources = citation or (combined_textual + biography)
    citations_path = work / "citations.json"
    if all_sources:
        records.append(
            _exec_cmd(
                [py, str(tools / "citation_manager.py"), *[str(x) for x in all_sources], "-o", str(citations_path)],
                repo_root,
                "build_citations",
                must_succeed=False,
            )
        )
        if not citations_path.exists():
            citations_path.write_text(
                json.dumps({"version": 1, "source_count": 1, "sources": [{"citation_id": "SRC-FALLBACK", "path": "user-input"}]}, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
    else:
        records.append(
            {
                "step": "build_citations",
                "tool": "tools/citation_manager.py",
                "status": "skipped",
                "reason": "no source materials provided",
            }
        )
        citations_path.write_text(
            json.dumps({"version": 1, "source_count": 1, "sources": [{"citation_id": "SRC-FALLBACK", "path": "user-input"}]}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    return records, citations_path


def _try_generate_with_repo_tools(data: dict, repo_root: Path) -> tuple[dict[str, str], dict]:
    tools = repo_root / "tools"
    if not (tools / "skill_writer.py").exists():
        raise RuntimeError("tools/skill_writer.py not found")

    slug = data["meta"]["slug"]
    tool_plan = build_tool_plan(data)
    tool_plan["mode"] = "repo-tools"

    with tempfile.TemporaryDirectory(prefix="mpb-", dir="/tmp") as td:
        work = Path(td)
        profile_path = work / "profile.json"
        memory_path = work / "memory.json"
        persona_path = work / "persona.json"

        profile = {
            "slug": slug,
            "name": data["meta"]["name"],
            "dynasty": data["master"]["dynasty"],
            "titles": data["master"]["titles"],
            "historical_context": data["master"]["historical_context"],
            "literary_school": data["master"]["literary_school"],
            "core_philosophy": data["master"]["core_philosophy"],
            "sources": ["user-input"],
            "persona": data["persona"],
        }

        profile_path.write_text(json.dumps(profile, ensure_ascii=False, indent=2), encoding="utf-8")
        memory_path.write_text(json.dumps(data["memory"], ensure_ascii=False, indent=2), encoding="utf-8")
        persona_path.write_text(json.dumps(data["persona"], ensure_ascii=False, indent=2), encoding="utf-8")

        execution_records, citations_path = _execute_category_tools(repo_root, work, data)
        tool_plan["executions"] = execution_records

        py = "python3"
        build_rec = _exec_cmd(
            [
                py,
                str(tools / "skill_writer.py"),
                "--action",
                "build",
                "--slug",
                slug,
                "--profile",
                str(profile_path),
                "--memory",
                str(memory_path),
                "--persona",
                str(persona_path),
                "--citations",
                str(citations_path),
            ],
            repo_root,
            "build_master_package",
            must_succeed=True,
        )
        tool_plan["executions"].append(build_rec)

        combine_rec = _exec_cmd(
            [py, str(tools / "skill_writer.py"), "--action", "combine", "--slug", slug],
            repo_root,
            "export_runtime_package",
            must_succeed=True,
        )
        tool_plan["executions"].append(combine_rec)

        canonical = repo_root / "masters" / slug
        runtime = repo_root / ".claude" / "skills" / slug

        files = {
            "skill_md": (runtime / "SKILL.md").read_text(encoding="utf-8"),
            "wiki_md": render_wiki_md(data),
            "self_md": (canonical / "self.md").read_text(encoding="utf-8"),
            "persona_md": (canonical / "persona.md").read_text(encoding="utf-8"),
            "meta_json": (canonical / "meta.json").read_text(encoding="utf-8"),
            "sources_json": (canonical / "sources.json").read_text(encoding="utf-8"),
        }
        return files, tool_plan


class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        if not is_origin_allowed(self):
            send_json(self, 403, {"ok": False, "errors": ["Forbidden origin"]})
            return
        send_json(self, 200, {"ok": True})

    def do_POST(self):
        try:
            if not is_origin_allowed(self):
                send_json(self, 403, {"ok": False, "errors": ["Forbidden origin"]})
                return
            if not is_authorized(self):
                send_json(self, 401, {"ok": False, "errors": ["Unauthorized"]})
                return
            payload = read_json_body(self)
            data = normalize_payload(payload)
            errors = validate_payload(data)
            if errors:
                send_json(self, 400, {"ok": False, "errors": errors})
                return

            repo_root = repo_root_from_api_file(Path(__file__))
            warnings: list[str] = []
            files: dict[str, str] | None = None
            tool_plan = build_tool_plan(data)

            if repo_root:
                try:
                    files, tool_plan = _try_generate_with_repo_tools(data, repo_root)
                except Exception as exc:
                    req_id = str(uuid.uuid4())
                    print(f"[generate][{req_id}] repo tool generation failed: {exc}", file=sys.stderr)
                    warnings.append("repo tool generation failed, fallback to template mode")

            if files is None:
                tool_plan["mode"] = "template-fallback"
                tool_plan["executions"].append(
                    {
                        "step": "template_render",
                        "tool": "inline_renderer",
                        "status": "success",
                        "reason": "repo tools unavailable or failed",
                    }
                )
                files = {
                    "skill_md": render_skill_md(data),
                    "wiki_md": render_wiki_md(data),
                    "self_md": "",
                    "persona_md": "",
                    "meta_json": json.dumps(data["meta"], ensure_ascii=False, indent=2),
                    "sources_json": json.dumps({"version": 1, "source_count": 1, "sources": [{"path": "user-input"}]}, ensure_ascii=False, indent=2),
                }
                if not repo_root:
                    warnings.append("repo tools not found in runtime; generated from template only")

            send_json(self, 200, {"ok": True, "warnings": warnings, "files": files, "tool_plan": tool_plan})
        except Exception as exc:
            req_id = str(uuid.uuid4())
            print(f"[generate][{req_id}] unhandled error: {exc}", file=sys.stderr)
            send_json(self, 500, {"ok": False, "errors": ["Internal server error"], "request_id": req_id})
