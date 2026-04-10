#!/usr/bin/env python3
"""Create/build/combine/export/list/delete distilled master skill artifacts."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MASTERS_DIR = ROOT / "masters"
RUNTIME_DIR = ROOT / ".claude" / "skills"
PROMPTS_DIR = ROOT / "prompts"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def slug_required(slug: str | None) -> str:
    if not slug:
        raise RuntimeError("--slug is required for this action")
    return slug


def ensure_master(slug: str) -> Path:
    d = MASTERS_DIR / slug
    d.mkdir(parents=True, exist_ok=True)
    return d


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def maybe_read_json(path: str | None) -> dict[str, Any]:
    if not path:
        return {}
    p = Path(path)
    if not p.exists():
        raise RuntimeError(f"JSON input does not exist: {p}")
    return read_json(p)


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def to_bullets(items: list[str], fallback: str) -> str:
    if not items:
        return f"- {fallback}\n"
    return "".join(f"- {x}\n" for x in items)


def render_self_md(profile: dict[str, Any], memory: dict[str, Any]) -> str:
    name = profile.get("name", "Unknown Master")
    dynasty = profile.get("dynasty", "Unknown")
    context = profile.get("historical_context", "Not provided")
    philosophy = profile.get("core_philosophy", "Not provided")

    values = memory.get("core_values", profile.get("core_values", []))
    values = values if isinstance(values, list) else [str(values)]

    milestones = memory.get("timeline_milestones", profile.get("timeline_milestones", []))
    milestones = milestones if isinstance(milestones, list) else [str(milestones)]

    geography = memory.get("geography_path", profile.get("geography_path", []))
    geography = geography if isinstance(geography, list) else [str(geography)]

    relationships = memory.get("relationships", profile.get("relationships", []))
    relationships = relationships if isinstance(relationships, list) else [str(relationships)]

    citations = memory.get("citation_ids", [])
    citations = citations if isinstance(citations, list) else [str(citations)]

    return (
        f"# {name} Master Memory\n\n"
        f"## Identity\n"
        f"- Name: {name}\n"
        f"- Dynasty: {dynasty}\n"
        f"- Historical context: {context}\n"
        f"- Core philosophy: {philosophy}\n\n"
        f"## Core Values\n{to_bullets(values, 'Pending extraction')}\n"
        f"## Timeline Milestones\n{to_bullets(milestones, 'Pending extraction')}\n"
        f"## Geography Path\n{to_bullets(geography, 'Pending extraction')}\n"
        f"## Key Relationships\n{to_bullets(relationships, 'Pending extraction')}\n"
        f"## Citation IDs\n{to_bullets(citations, 'No citations yet')}"
    )


def render_persona_md(profile: dict[str, Any], persona: dict[str, Any]) -> str:
    p = profile.get("persona", {})
    p = p if isinstance(p, dict) else {}

    layer1 = persona.get("l1_hard_rules", p.get("l1_hard_rules", []))
    layer2 = persona.get("l2_identity_role", p.get("l2_identity_role", []))
    layer3 = persona.get("l3_expression_style", p.get("l3_expression_style", []))
    layer4 = persona.get("l4_judgment_logic", p.get("l4_judgment_logic", []))
    layer5 = persona.get("l5_social_conduct", p.get("l5_social_conduct", []))

    layer1 = layer1 if isinstance(layer1, list) else [str(layer1)]
    layer2 = layer2 if isinstance(layer2, list) else [str(layer2)]
    layer3 = layer3 if isinstance(layer3, list) else [str(layer3)]
    layer4 = layer4 if isinstance(layer4, list) else [str(layer4)]
    layer5 = layer5 if isinstance(layer5, list) else [str(layer5)]

    return (
        "# Literary Persona\n\n"
        "## L1 Hard Rules\n"
        f"{to_bullets(layer1, 'No modern colloquial style.')}\n"
        "## L2 Identity and Role\n"
        f"{to_bullets(layer2, 'Keep historical consistency.')}\n"
        "## L3 Expression Style\n"
        f"{to_bullets(layer3, 'Prefer classical diction and measured cadence.')}\n"
        "## L4 Judgment Logic\n"
        f"{to_bullets(layer4, 'Align with known ethical and political stance.')}\n"
        "## L5 Social Conduct\n"
        f"{to_bullets(layer5, 'Preserve tone toward peers, juniors, and rivals.')}"
    )


def build_meta(profile: dict[str, Any], slug: str) -> dict[str, Any]:
    name = profile.get("name", slug)
    dynasty = profile.get("dynasty", "Unknown")
    meta = {
        "slug": slug,
        "name": name,
        "dynasty": dynasty,
        "titles": profile.get("titles", []),
        "historical_context": profile.get("historical_context", ""),
        "literary_school": profile.get("literary_school", ""),
        "core_philosophy": profile.get("core_philosophy", ""),
        "version": profile.get("version", "1.0.0"),
        "prompt_contract": [
            str(PROMPTS_DIR / "intake.md"),
            str(PROMPTS_DIR / "memory_analyzer.md"),
            str(PROMPTS_DIR / "literary_persona_analyzer.md"),
            str(PROMPTS_DIR / "self_builder.md"),
            str(PROMPTS_DIR / "persona_builder.md"),
            str(PROMPTS_DIR / "merger.md"),
            str(PROMPTS_DIR / "critique_handler.md"),
        ],
        "created_at": now_iso(),
        "updated_at": now_iso(),
    }
    return meta


def build_sources(profile: dict[str, Any], citation_data: dict[str, Any]) -> dict[str, Any]:
    if citation_data:
        return citation_data
    srcs = profile.get("sources", [])
    if not isinstance(srcs, list):
        srcs = [str(srcs)]
    return {"version": 1, "source_count": len(srcs), "sources": [{"path": s} for s in srcs]}


def create_master(slug: str, name: str, dynasty: str, philosophy: str) -> dict[str, Any]:
    d = ensure_master(slug)
    self_md = d / "self.md"
    persona_md = d / "persona.md"
    meta = d / "meta.json"
    sources = d / "sources.json"

    if not self_md.exists():
        self_md.write_text(f"# {name} Master Memory\n\n- Dynasty: {dynasty}\n- Core philosophy: {philosophy}\n", encoding="utf-8")
    if not persona_md.exists():
        persona_md.write_text(
            "# Literary Persona\n\n## L1 Hard Rules\n- No modern colloquial style.\n\n## L2 Identity and Role\n- Keep historical consistency.\n\n## L3 Expression Style\n- Prefer classical diction and measured cadence.\n\n## L4 Judgment Logic\n- Reflect the master's known political and ethical stance.\n\n## L5 Social Conduct\n- Preserve tone toward peers, juniors, and rivals.\n",
            encoding="utf-8",
        )
    if not meta.exists():
        write_json(
            meta,
            {
                "slug": slug,
                "name": name,
                "dynasty": dynasty,
                "core_philosophy": philosophy,
                "version": "1.0.0",
                "created_at": now_iso(),
                "updated_at": now_iso(),
            },
        )
    if not sources.exists():
        write_json(sources, {"version": 1, "sources": []})

    return {"action": "create", "slug": slug, "path": str(d)}


def build_master(slug: str, profile_path: str, memory_path: str | None, persona_path: str | None, citations_path: str | None) -> dict[str, Any]:
    profile_file = Path(profile_path)
    if not profile_file.exists():
        raise RuntimeError(f"profile file not found: {profile_file}")

    profile = read_json(profile_file)
    memory = maybe_read_json(memory_path)
    persona = maybe_read_json(persona_path)
    citations = maybe_read_json(citations_path)

    if "slug" in profile and str(profile["slug"]) != slug:
        raise RuntimeError("--slug does not match profile slug")

    d = ensure_master(slug)
    self_md = render_self_md(profile, memory)
    persona_md = render_persona_md(profile, persona)

    (d / "self.md").write_text(self_md, encoding="utf-8")
    (d / "persona.md").write_text(persona_md, encoding="utf-8")
    write_json(d / "meta.json", build_meta(profile, slug))
    write_json(d / "sources.json", build_sources(profile, citations))

    return {
        "action": "build",
        "slug": slug,
        "path": str(d),
        "used_inputs": {
            "profile": str(profile_file),
            "memory": memory_path,
            "persona": persona_path,
            "citations": citations_path,
        },
    }


def runtime_skill_markdown(slug: str, name: str) -> str:
    return f"""---
name: {slug}
description: Distilled literary persona for {name}
user-invocable: true
---

# {name}

This generated skill uses local artifacts:
- self.md
- persona.md
- meta.json

When invoked, speak and write with this master's distilled literary voice.
"""


def load_meta(slug: str) -> dict[str, Any]:
    p = MASTERS_DIR / slug / "meta.json"
    if not p.exists():
        raise RuntimeError(f"missing meta.json for slug: {slug}")
    return json.loads(p.read_text(encoding="utf-8"))


def export_master(slug: str) -> dict[str, Any]:
    src = MASTERS_DIR / slug
    if not src.exists():
        raise RuntimeError(f"master not found: {slug}")
    dst = RUNTIME_DIR / slug
    dst.mkdir(parents=True, exist_ok=True)

    for fname in ["self.md", "persona.md", "meta.json"]:
        s = src / fname
        if not s.exists():
            raise RuntimeError(f"missing canonical file: {s}")
        shutil.copy2(s, dst / fname)

    meta = load_meta(slug)
    (dst / "SKILL.md").write_text(runtime_skill_markdown(slug, meta.get("name", slug)), encoding="utf-8")
    return {"action": "export", "slug": slug, "runtime_path": str(dst)}


def combine_master(slug: str) -> dict[str, Any]:
    # In v1, combine validates canonical schema then exports runtime files.
    _ = load_meta(slug)
    return export_master(slug)


def list_masters() -> dict[str, Any]:
    MASTERS_DIR.mkdir(parents=True, exist_ok=True)
    slugs = []
    for p in MASTERS_DIR.iterdir():
        if not p.is_dir() or p.name.startswith("."):
            continue
        if (p / "meta.json").exists():
            slugs.append(p.name)
    slugs.sort()
    return {"action": "list", "count": len(slugs), "masters": slugs}


def delete_master(slug: str) -> dict[str, Any]:
    removed = []
    for path in [MASTERS_DIR / slug, RUNTIME_DIR / slug]:
        if path.exists():
            shutil.rmtree(path)
            removed.append(str(path))
    return {"action": "delete", "slug": slug, "removed": removed}


def main() -> int:
    ap = argparse.ArgumentParser(description="Manage distilled master artifacts")
    ap.add_argument("--action", required=True, choices=["create", "build", "combine", "export", "list", "delete"])
    ap.add_argument("--slug")
    ap.add_argument("--name", default="Unknown Master")
    ap.add_argument("--dynasty", default="Unknown")
    ap.add_argument("--philosophy", default="Unknown")

    ap.add_argument("--profile", help="Profile JSON path for --action build")
    ap.add_argument("--memory", help="Memory analysis JSON path for --action build")
    ap.add_argument("--persona", help="Persona analysis JSON path for --action build")
    ap.add_argument("--citations", help="Citation manifest JSON path for --action build")
    args = ap.parse_args()

    try:
        if args.action == "create":
            result = create_master(slug_required(args.slug), args.name, args.dynasty, args.philosophy)
        elif args.action == "build":
            slug = slug_required(args.slug)
            if not args.profile:
                raise RuntimeError("--profile is required for --action build")
            result = build_master(slug, args.profile, args.memory, args.persona, args.citations)
        elif args.action == "combine":
            result = combine_master(slug_required(args.slug))
        elif args.action == "export":
            result = export_master(slug_required(args.slug))
        elif args.action == "list":
            result = list_masters()
        elif args.action == "delete":
            result = delete_master(slug_required(args.slug))
        else:
            raise RuntimeError(f"unsupported action: {args.action}")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
