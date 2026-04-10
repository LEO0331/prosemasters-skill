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


def normalize_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    if isinstance(value, str):
        value = value.strip()
        return [value] if value else []
    text = str(value).strip()
    return [text] if text else []


def to_bullets(items: list[str], fallback: str) -> str:
    if not items:
        return f"- {fallback}\n"
    return "".join(f"- {x}\n" for x in items)


def render_self_md(profile: dict[str, Any], memory: dict[str, Any]) -> str:
    name = str(profile.get("name", "Unknown Master"))
    dynasty = str(profile.get("dynasty", "Unknown"))
    context = str(profile.get("historical_context", "Not provided"))
    school = str(profile.get("literary_school", "Not provided"))
    philosophy = str(profile.get("core_philosophy", "Not provided"))

    values = normalize_list(memory.get("core_values", profile.get("core_values")))
    milestones = normalize_list(memory.get("timeline_milestones", profile.get("timeline_milestones")))
    geography = normalize_list(memory.get("geography_path", profile.get("geography_path")))
    relationships = normalize_list(memory.get("relationships", profile.get("relationships")))
    citations = normalize_list(memory.get("citation_ids"))

    intellectual_axes = normalize_list(memory.get("intellectual_axes", profile.get("intellectual_axes")))
    worldview_tensions = normalize_list(memory.get("worldview_tensions", profile.get("worldview_tensions")))
    preferred_themes = normalize_list(memory.get("preferred_themes", profile.get("preferred_themes")))
    emotional_signature = normalize_list(memory.get("emotional_signature", profile.get("emotional_signature")))
    voice_anchors = normalize_list(memory.get("voice_anchors", profile.get("voice_anchors")))
    anachronism_policy = normalize_list(memory.get("anachronism_policy", profile.get("anachronism_policy")))

    return (
        f"# {name} Master Memory\n\n"
        f"## Identity\n"
        f"- Name: {name}\n"
        f"- Dynasty: {dynasty}\n"
        f"- Literary school: {school}\n"
        f"- Historical context: {context}\n"
        f"- Core philosophy: {philosophy}\n\n"
        f"## Core Values\n{to_bullets(values, 'Pending extraction')}\n"
        f"## Intellectual Axes\n{to_bullets(intellectual_axes, 'Pending extraction')}\n"
        f"## Worldview Tensions\n{to_bullets(worldview_tensions, 'Pending extraction')}\n"
        f"## Preferred Themes\n{to_bullets(preferred_themes, 'Pending extraction')}\n"
        f"## Emotional Signature\n{to_bullets(emotional_signature, 'Pending extraction')}\n"
        f"## Timeline Milestones\n{to_bullets(milestones, 'Pending extraction')}\n"
        f"## Geography Path\n{to_bullets(geography, 'Pending extraction')}\n"
        f"## Key Relationships\n{to_bullets(relationships, 'Pending extraction')}\n"
        f"## Voice Anchors\n{to_bullets(voice_anchors, 'Pending extraction')}\n"
        f"## Anachronism Policy\n{to_bullets(anachronism_policy, 'Translate modern topics by analogy to historical categories.')}\n"
        f"## Citation IDs\n{to_bullets(citations, 'No citations yet')}"
    )


def render_persona_md(profile: dict[str, Any], persona: dict[str, Any]) -> str:
    base = profile.get("persona", {})
    base = base if isinstance(base, dict) else {}

    layer1 = normalize_list(persona.get("l1_hard_rules", base.get("l1_hard_rules")))
    layer2 = normalize_list(persona.get("l2_identity_role", base.get("l2_identity_role")))
    layer3 = normalize_list(persona.get("l3_expression_style", base.get("l3_expression_style")))
    layer4 = normalize_list(persona.get("l4_judgment_logic", base.get("l4_judgment_logic")))
    layer5 = normalize_list(persona.get("l5_social_conduct", base.get("l5_social_conduct")))

    lexicon = normalize_list(persona.get("lexicon_preferences", base.get("lexicon_preferences")))
    rhythm = normalize_list(persona.get("rhythm_structure", base.get("rhythm_structure")))
    decision_ladder = normalize_list(persona.get("decision_ladder", base.get("decision_ladder")))
    audience_tone = normalize_list(persona.get("audience_tone", base.get("audience_tone")))
    anti_patterns = normalize_list(persona.get("anti_patterns", base.get("anti_patterns")))
    rewrite_strategies = normalize_list(persona.get("rewrite_strategies", base.get("rewrite_strategies")))

    return (
        "# Literary Persona\n\n"
        "## L1 Hard Rules\n"
        f"{to_bullets(layer1, 'No modern colloquial style.')}\n"
        "## L2 Identity and Role\n"
        f"{to_bullets(layer2, 'Keep historical consistency.')}\n"
        "## L3 Expression Style\n"
        f"{to_bullets(layer3, 'Prefer classical diction and measured cadence.')}\n"
        "## L3.1 Lexicon Preferences\n"
        f"{to_bullets(lexicon, 'Prefer source-attested terms and imagery.')}\n"
        "## L3.2 Rhythm and Structure\n"
        f"{to_bullets(rhythm, 'Control sentence-length contrast and rhetorical pacing.')}\n"
        "## L4 Judgment Logic\n"
        f"{to_bullets(layer4, 'Align with known ethical and political stance.')}\n"
        "## L4.1 Decision Ladder\n"
        f"{to_bullets(decision_ladder, 'Principle -> context -> action -> rhetorical closure.')}\n"
        "## L5 Social Conduct\n"
        f"{to_bullets(layer5, 'Preserve tone toward peers, juniors, and rivals.')}\n"
        "## L5.1 Audience Tone Matrix\n"
        f"{to_bullets(audience_tone, 'Vary tone by audience while preserving identity.')}\n"
        "## Failure Modes to Avoid\n"
        f"{to_bullets(anti_patterns, 'Avoid empty ornament and ahistorical postures.')}\n"
        "## Rewrite Strategies\n"
        f"{to_bullets(rewrite_strategies, 'If style drifts, restate claim with stronger period diction and logic.') }"
    )


def build_meta(profile: dict[str, Any], slug: str) -> dict[str, Any]:
    name = profile.get("name", slug)
    dynasty = profile.get("dynasty", "Unknown")
    return {
        "slug": slug,
        "name": name,
        "dynasty": dynasty,
        "titles": profile.get("titles", []),
        "historical_context": profile.get("historical_context", ""),
        "literary_school": profile.get("literary_school", ""),
        "core_philosophy": profile.get("core_philosophy", ""),
        "version": profile.get("version", "1.0.0"),
        "fidelity_profile": {
            "min_citations_per_nontrivial_claim": 1,
            "allow_modern_topic_translation": True,
            "modern_topic_strategy": "analogy_to_historical_categories",
            "reject_ahistorical_slang": True,
        },
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
description: High-fidelity distilled literary persona for {name}
user-invocable: true
---

# {name}

## Identity Contract
You are not a generic assistant in this mode. You are a constrained digital reconstruction of **{name}**.

## Required Local Artifacts
- self.md
- persona.md
- meta.json

## Runtime Rules
1. Apply `persona.md` as the first-pass filter before writing any response.
2. Ground nontrivial judgments in `self.md` memory and source-backed stance.
3. If user asks modern topics, translate by historical analogy instead of modern slang.
4. Keep period-appropriate diction and rhetorical posture.
5. If challenged with "he wouldn't say this", self-correct using L1/L4 constraints and rewrite.

## Response Quality Gate
- Voice consistency: pass/fail
- Historical consistency: pass/fail
- Argument coherence: pass/fail
- Style drift check: pass/fail

If any gate fails, rewrite before final output.
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
    (dst / "SKILL.md").write_text(runtime_skill_markdown(slug, str(meta.get("name", slug))), encoding="utf-8")
    return {"action": "export", "slug": slug, "runtime_path": str(dst)}


def combine_master(slug: str) -> dict[str, Any]:
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
