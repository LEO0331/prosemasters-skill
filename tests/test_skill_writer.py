from __future__ import annotations

import json
from pathlib import Path

import skill_writer


def _set_paths(base: Path) -> tuple[Path, Path, Path]:
    masters = base / "masters"
    runtime = base / ".claude" / "skills"
    prompts = base / "prompts"
    masters.mkdir(parents=True, exist_ok=True)
    runtime.mkdir(parents=True, exist_ok=True)
    prompts.mkdir(parents=True, exist_ok=True)
    for name in [
        "intake.md",
        "memory_analyzer.md",
        "literary_persona_analyzer.md",
        "self_builder.md",
        "persona_builder.md",
        "merger.md",
        "critique_handler.md",
    ]:
        (prompts / name).write_text("# x\n", encoding="utf-8")
    skill_writer.MASTERS_DIR = masters
    skill_writer.RUNTIME_DIR = runtime
    skill_writer.PROMPTS_DIR = prompts
    return masters, runtime, prompts


def test_slug_required_and_safe_child(tmp_path: Path) -> None:
    _set_paths(tmp_path)
    assert skill_writer.slug_required("han-yu") == "han-yu"
    try:
        skill_writer.slug_required("Han Yu")
        assert False, "expected RuntimeError"
    except RuntimeError as exc:
        assert "invalid slug" in str(exc)

    child = skill_writer.safe_child(tmp_path, "a/b")
    assert child == (tmp_path / "a/b").resolve()
    try:
        skill_writer.safe_child(tmp_path, "../escape")
        assert False, "expected RuntimeError"
    except RuntimeError as exc:
        assert "unsafe path escape attempt" in str(exc)


def test_helpers_render_and_meta_sources(tmp_path: Path) -> None:
    _set_paths(tmp_path)
    assert skill_writer.normalize_list("x") == ["x"]
    assert skill_writer.normalize_list(["a", " ", "b"]) == ["a", "b"]
    assert skill_writer.to_bullets([], "fallback") == "- fallback\n"

    profile = {
        "name": "韓愈",
        "dynasty": "中唐",
        "literary_school": "古文運動",
        "historical_context": "context",
        "core_philosophy": "philosophy",
        "sources": ["a.txt"],
    }
    self_md = skill_writer.render_self_md(profile, {"core_values": ["義理"]})
    persona_md = skill_writer.render_persona_md(profile, {"l1_hard_rules": ["rule"]})
    meta = skill_writer.build_meta(profile, "slug-a")
    sources = skill_writer.build_sources(profile, {})
    assert "# 韓愈 Master Memory" in self_md
    assert "## L1 Hard Rules" in persona_md
    assert meta["slug"] == "slug-a"
    assert len(meta["prompt_contract"]) == 7
    assert all(not Path(p).is_absolute() for p in meta["prompt_contract"])
    assert meta["prompt_contract"][0] == "prompts/intake.md"
    assert sources["source_count"] == 1


def test_create_build_export_combine_delete_flow(tmp_path: Path) -> None:
    masters, runtime, _ = _set_paths(tmp_path)
    created = skill_writer.create_master("han-yu", "韓愈", "中唐", "文以載道")
    assert created["action"] == "create"
    assert (masters / "han-yu" / "self.md").exists()

    profile = tmp_path / "profile.json"
    memory = tmp_path / "memory.json"
    persona = tmp_path / "persona.json"
    citations = tmp_path / "citations.json"
    profile.write_text(
        json.dumps(
            {
                "slug": "han-yu",
                "name": "韓愈",
                "dynasty": "中唐",
                "literary_school": "古文運動",
                "historical_context": "context",
                "core_philosophy": "philosophy",
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    memory.write_text(json.dumps({"core_values": ["義理"]}, ensure_ascii=False), encoding="utf-8")
    persona.write_text(json.dumps({"l1_hard_rules": ["rule"]}, ensure_ascii=False), encoding="utf-8")
    citations.write_text(json.dumps({"version": 1, "sources": []}, ensure_ascii=False), encoding="utf-8")

    built = skill_writer.build_master("han-yu", str(profile), str(memory), str(persona), str(citations))
    assert built["action"] == "build"
    assert (masters / "han-yu" / "meta.json").exists()
    assert skill_writer.load_meta("han-yu")["slug"] == "han-yu"

    exported = skill_writer.export_master("han-yu")
    assert exported["action"] == "export"
    assert (runtime / "han-yu" / "SKILL.md").exists()

    combined = skill_writer.combine_master("han-yu")
    assert combined["action"] == "export"

    listed = skill_writer.list_masters()
    assert listed["count"] == 1

    deleted = skill_writer.delete_master("han-yu")
    assert deleted["action"] == "delete"
    assert not (masters / "han-yu").exists()


def test_build_master_errors(tmp_path: Path) -> None:
    _set_paths(tmp_path)
    missing = tmp_path / "missing.json"
    try:
        skill_writer.build_master("x", str(missing), None, None, None)
        assert False, "expected RuntimeError"
    except RuntimeError as exc:
        assert "profile file not found" in str(exc)

    p = tmp_path / "profile.json"
    p.write_text(json.dumps({"slug": "other"}), encoding="utf-8")
    try:
        skill_writer.build_master("x", str(p), None, None, None)
        assert False, "expected RuntimeError"
    except RuntimeError as exc:
        assert "does not match profile slug" in str(exc)


def test_main_actions_and_errors(monkeypatch, capsys, tmp_path: Path) -> None:
    _set_paths(tmp_path)
    monkeypatch.setattr("sys.argv", ["skill_writer.py", "--action", "list"])
    assert skill_writer.main() == 0

    monkeypatch.setattr("sys.argv", ["skill_writer.py", "--action", "create"])
    assert skill_writer.main() == 1
    assert "--slug is required" in capsys.readouterr().err

    monkeypatch.setattr("sys.argv", ["skill_writer.py", "--action", "build", "--slug", "x"])
    assert skill_writer.main() == 1
    assert "--profile is required" in capsys.readouterr().err


def test_runtime_skill_markdown() -> None:
    md = skill_writer.runtime_skill_markdown("slug-a", "Name A")
    assert "name: slug-a" in md
    assert "# Name A" in md
