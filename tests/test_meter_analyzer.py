from __future__ import annotations

import json
from pathlib import Path

import meter_analyzer


def test_analyze_counts_and_parallelism() -> None:
    text = "春風又綠江南岸。明月何時照我還。山高水長。天寒地凍。"
    report = meter_analyzer.analyze(text)
    assert report["sentence_count"] == 4
    assert report["parallelism_pair_count"] >= 1
    assert isinstance(report["top_line_endings"], list)


def test_load_text_from_parser_json(tmp_path: Path) -> None:
    p = tmp_path / "parsed.json"
    p.write_text(
        json.dumps({"files": [{"paragraphs": ["a", "b"]}, {"paragraphs": ["c"]}]}, ensure_ascii=False),
        encoding="utf-8",
    )
    assert meter_analyzer.load_text(p) == "a\nb\nc"


def test_main_success_and_error(tmp_path: Path, monkeypatch, capsys) -> None:
    inp = tmp_path / "in.txt"
    out = tmp_path / "out.json"
    inp.write_text("甲。乙。", encoding="utf-8")

    monkeypatch.setattr("sys.argv", ["meter_analyzer.py", str(inp), "-o", str(out)])
    assert meter_analyzer.main() == 0
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["sentence_count"] == 2

    monkeypatch.setattr("sys.argv", ["meter_analyzer.py", str(tmp_path / "missing.txt")])
    assert meter_analyzer.main() == 1
    assert "input does not exist" in capsys.readouterr().err


def test_main_stdout_path(tmp_path: Path, monkeypatch, capsys) -> None:
    inp = tmp_path / "in.txt"
    inp.write_text("甲。乙。", encoding="utf-8")
    monkeypatch.setattr("sys.argv", ["meter_analyzer.py", str(inp)])
    assert meter_analyzer.main() == 0
    assert '"sentence_count": 2' in capsys.readouterr().out
