from __future__ import annotations

import json
from pathlib import Path

import citation_manager


def test_digest_and_manifest(tmp_path: Path) -> None:
    a = tmp_path / "a.txt"
    b = tmp_path / "b.txt"
    a.write_text("alpha", encoding="utf-8")
    b.write_text("beta", encoding="utf-8")

    assert len(citation_manager.digest("x")) == 12
    manifest = citation_manager.build_manifest([a, b], excerpt_chars=3)
    assert manifest["source_count"] == 2
    assert manifest["sources"][0]["excerpt"] == "alp"
    assert manifest["sources"][0]["citation_id"].startswith("SRC-")
    assert manifest["sources"][0]["path"] == "a.txt"


def test_display_path_relative_and_sanitized(tmp_path: Path) -> None:
    nested = tmp_path / "nested" / "c.txt"
    nested.parent.mkdir()
    nested.write_text("gamma", encoding="utf-8")

    assert citation_manager.display_path(nested, tmp_path) == "nested/c.txt"
    assert citation_manager.display_path(nested, tmp_path / "elsewhere") == "c.txt"


def test_main_success_and_missing(tmp_path: Path, monkeypatch, capsys) -> None:
    a = tmp_path / "a.txt"
    out = tmp_path / "c.json"
    a.write_text("alpha", encoding="utf-8")

    monkeypatch.setattr("sys.argv", ["citation_manager.py", str(a), "-o", str(out)])
    assert citation_manager.main() == 0
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["source_count"] == 1

    monkeypatch.setattr("sys.argv", ["citation_manager.py", str(tmp_path / "missing.txt")])
    assert citation_manager.main() == 1
    assert "missing files" in capsys.readouterr().err


def test_main_stdout_path(tmp_path: Path, monkeypatch, capsys) -> None:
    a = tmp_path / "a.txt"
    a.write_text("alpha", encoding="utf-8")
    monkeypatch.setattr("sys.argv", ["citation_manager.py", str(a)])
    assert citation_manager.main() == 0
    assert '"source_count": 1' in capsys.readouterr().out
