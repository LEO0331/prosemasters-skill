from __future__ import annotations

import json
import os
import re
import secrets
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

SLUG_RE = re.compile(r"^[a-z0-9-]+$")


def _allowed_origins() -> set[str]:
    raw = os.getenv("MPB_ALLOWED_ORIGINS", "")
    return {x.strip() for x in raw.split(",") if x.strip()}


def _request_origin(handler: Any) -> str:
    return str(handler.headers.get("Origin", "")).strip()


def _same_origin(handler: Any, origin: str) -> bool:
    if not origin:
        return True
    host = str(handler.headers.get("Host", "")).strip()
    if not host:
        return False
    parsed = urlparse(origin)
    if not parsed.scheme or not parsed.netloc:
        return False
    if parsed.netloc != host:
        return False

    forwarded_proto = str(handler.headers.get("X-Forwarded-Proto", "")).strip().lower()
    if not forwarded_proto:
        # Fallback for local/self-hosted runtimes where this header is absent.
        return True
    return parsed.scheme.lower() == forwarded_proto


def is_origin_allowed(handler: Any) -> bool:
    origin = _request_origin(handler)
    if not origin:
        return True
    if _same_origin(handler, origin):
        return True
    return origin in _allowed_origins()


def is_authorized(handler: Any) -> bool:
    expected = os.getenv("MPB_API_KEY", "").strip()
    if not expected:
        return True

    provided = str(handler.headers.get("X-API-Key", "")).strip()
    if not provided:
        auth = str(handler.headers.get("Authorization", "")).strip()
        if auth.lower().startswith("bearer "):
            provided = auth[7:].strip()
    return bool(provided) and secrets.compare_digest(provided, expected)


def reject_forbidden_origin(handler: Any) -> bool:
    if is_origin_allowed(handler):
        return False
    send_json(handler, 403, {"ok": False, "errors": ["Forbidden origin"]})
    return True


def reject_unauthorized(handler: Any) -> bool:
    if is_authorized(handler):
        return False
    send_json(handler, 401, {"ok": False, "errors": ["Unauthorized"]})
    return True


def send_json(handler: Any, status: int, payload: dict[str, Any]) -> None:
    raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    origin = _request_origin(handler)
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    if origin and is_origin_allowed(handler):
        handler.send_header("Access-Control-Allow-Origin", origin)
        handler.send_header("Vary", "Origin")
    handler.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
    handler.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-API-Key")
    handler.send_header("X-Content-Type-Options", "nosniff")
    handler.send_header("Cache-Control", "no-store")
    handler.send_header("Content-Length", str(len(raw)))
    handler.end_headers()
    handler.wfile.write(raw)


def read_json_body(handler: Any, max_bytes: int = 2_000_000) -> dict[str, Any]:
    try:
        length = int(handler.headers.get("Content-Length", "0"))
    except ValueError as exc:
        raise ValueError("Invalid Content-Length") from exc
    if length <= 0:
        raise ValueError("Empty body")
    if length > max_bytes:
        raise ValueError(f"Payload too large ({length} bytes)")
    data = handler.rfile.read(length)
    obj = json.loads(data.decode("utf-8"))
    if not isinstance(obj, dict):
        raise ValueError("JSON payload must be an object")
    return obj


def split_lines(value: str) -> list[str]:
    return [x.strip() for x in value.splitlines() if x.strip()]


def normalize_array(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    if isinstance(value, str):
        return split_lines(value)
    return [str(value).strip()] if str(value).strip() else []


def normalize_payload(payload: dict[str, Any]) -> dict[str, Any]:
    meta = payload.get("meta") or {}
    master = payload.get("master") or {}
    memory = payload.get("memory") or {}
    persona = payload.get("persona") or {}
    commands = payload.get("commands") or {}
    source_materials = payload.get("source_materials") or []

    normalized = {
        "meta": {
            "slug": str(meta.get("slug", "")).strip().lower(),
            "name": str(meta.get("name", "")).strip(),
            "description": str(meta.get("description", "")).strip(),
            "version": str(meta.get("version", "1.0.0")).strip() or "1.0.0",
            "language": str(meta.get("language", "zh-TW")).strip() or "zh-TW",
            "target_platforms": normalize_array(meta.get("target_platforms", ["claude", "codex"])),
        },
        "master": {
            "display_name": str(master.get("display_name", "")).strip(),
            "dynasty": str(master.get("dynasty", "")).strip(),
            "titles": normalize_array(master.get("titles")),
            "historical_context": str(master.get("historical_context", "")).strip(),
            "literary_school": str(master.get("literary_school", "")).strip(),
            "core_philosophy": str(master.get("core_philosophy", "")).strip(),
        },
        "memory": {k: normalize_array(memory.get(k)) for k in [
            "core_values", "intellectual_axes", "worldview_tensions", "preferred_themes",
            "emotional_signature", "timeline_milestones", "geography_path", "relationships",
            "voice_anchors", "anachronism_policy", "citation_ids",
        ]},
        "persona": {k: normalize_array(persona.get(k)) for k in [
            "l1_hard_rules", "l2_identity_role", "l3_expression_style", "lexicon_preferences",
            "rhythm_structure", "l4_judgment_logic", "decision_ladder", "l5_social_conduct",
            "audience_tone", "anti_patterns", "rewrite_strategies",
        ]},
        "commands": {
            "trigger": str(commands.get("trigger", "/distill-master")).strip() or "/distill-master",
            "update": str(commands.get("update", "/update-master {slug}")).strip() or "/update-master {slug}",
            "list": str(commands.get("list", "/list-masters")).strip() or "/list-masters",
            "delete": str(commands.get("delete", "/delete-master {slug}")).strip() or "/delete-master {slug}",
        },
        "source_materials": [],
    }
    if isinstance(source_materials, list):
        for item in source_materials:
            if not isinstance(item, dict):
                continue
            category = str(item.get("category", "")).strip().lower()
            title = str(item.get("title", "")).strip()
            content = str(item.get("content", "")).strip()
            if not content:
                continue
            normalized["source_materials"].append(
                {"category": category, "title": title, "content": content}
            )
    return normalized


def validate_payload(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    meta = payload.get("meta") or {}
    master = payload.get("master") or {}
    source_materials = payload.get("source_materials", [])

    slug = str(meta.get("slug", "")).strip().lower()
    if not slug:
        errors.append("meta.slug is required")
    elif not SLUG_RE.fullmatch(slug):
        errors.append("meta.slug must match ^[a-z0-9-]+$")

    if not str(meta.get("name", "")).strip():
        errors.append("meta.name is required")
    if not str(meta.get("description", "")).strip():
        errors.append("meta.description is required")
    if not str(master.get("display_name", "")).strip():
        errors.append("master.display_name is required")

    allowed_categories = {"works", "criticism", "letters", "biography", "citation"}
    max_source_items = int(os.getenv("MPB_MAX_SOURCE_ITEMS", "24"))
    max_source_chars = int(os.getenv("MPB_MAX_SOURCE_CHARS", "30000"))
    max_total_source_chars = int(os.getenv("MPB_MAX_TOTAL_SOURCE_CHARS", "200000"))

    if len(source_materials) > max_source_items:
        errors.append(f"source_materials max items exceeded ({len(source_materials)} > {max_source_items})")

    total_source_chars = 0
    for i, item in enumerate(source_materials):
        c = item.get("category", "")
        if c not in allowed_categories:
            errors.append(f"source_materials[{i}].category must be one of {sorted(allowed_categories)}")
        content_len = len(str(item.get("content", "")))
        total_source_chars += content_len
        if content_len > max_source_chars:
            errors.append(f"source_materials[{i}].content too large ({content_len} > {max_source_chars})")
    if total_source_chars > max_total_source_chars:
        errors.append(
            f"source_materials total content too large ({total_source_chars} > {max_total_source_chars})"
        )

    return errors


def _bullets(items: list[str], fallback: str) -> str:
    if not items:
        return f"- {fallback}\n"
    return "".join(f"- {x}\n" for x in items)


def render_skill_md(data: dict[str, Any]) -> str:
    meta = data["meta"]
    master = data["master"]
    cmd = data["commands"]
    return f"""---
name: {meta['slug']}
description: {meta['description']}
version: {meta['version']}
user-invocable: true
allowed-tools: Read, Write, Edit, Bash
---

# {master['display_name']} Persona Skill

## Trigger
- {cmd['trigger']}

## Core
- Dynasty: {master['dynasty']}
- Literary school: {master['literary_school']}
- Core philosophy: {master['core_philosophy']}

## Runtime
1. Apply persona constraints before response.
2. Use memory anchors for nontrivial judgments.
3. Translate modern topics by historical analogy.

## Management
- {cmd['list']}
- {cmd['update']}
- {cmd['delete']}
"""


def render_wiki_md(data: dict[str, Any]) -> str:
    meta = data["meta"]
    master = data["master"]
    memory = data["memory"]
    persona = data["persona"]

    return (
        f"# {master['display_name']} ({meta['slug']})\n\n"
        f"## Overview\n"
        f"- Name: {meta['name']}\n"
        f"- Dynasty: {master['dynasty']}\n"
        f"- Description: {meta['description']}\n"
        f"- Historical context: {master['historical_context']}\n\n"
        f"## Memory\n"
        f"### Core Values\n{_bullets(memory['core_values'], 'N/A')}\n"
        f"### Timeline Milestones\n{_bullets(memory['timeline_milestones'], 'N/A')}\n"
        f"### Voice Anchors\n{_bullets(memory['voice_anchors'], 'N/A')}\n"
        f"## Persona\n"
        f"### L1 Hard Rules\n{_bullets(persona['l1_hard_rules'], 'N/A')}\n"
        f"### Style\n{_bullets(persona['l3_expression_style'], 'N/A')}\n"
        f"### Decision Ladder\n{_bullets(persona['decision_ladder'], 'N/A')}\n"
    )


def repo_root_from_api_file(api_file: Path) -> Path | None:
    cur = api_file.resolve().parent
    for _ in range(8):
        if (cur / "tools" / "skill_writer.py").exists():
            return cur
        if cur.parent == cur:
            break
        cur = cur.parent
    return None
