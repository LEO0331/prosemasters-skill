from __future__ import annotations

import json
from pathlib import Path

import literature_parser


def test_normalize_and_paragraphs() -> None:
    text = "a  b\r\n\r\n\r\nc\t\t d\r\n"
    normalized = literature_parser.normalize(text)
    assert normalized == "a b\n\nc d"
    assert literature_parser.to_paragraphs(normalized) == ["a b", "c d"]


def test_parse_files_text_and_md(tmp_path: Path) -> None:
    a = tmp_path / "a.txt"
    b = tmp_path / "b.md"
    a.write_text("第一段\n\n第二段", encoding="utf-8")
    b.write_text("x\n\n\ny", encoding="utf-8")

    data = literature_parser.parse_files([a, b])
    assert data["file_count"] == 2
    assert data["total_paragraphs"] == 4
    assert data["files"][0]["path"].endswith("a.txt")


def test_read_text_unsupported_suffix(tmp_path: Path) -> None:
    bad = tmp_path / "x.bin"
    bad.write_bytes(b"abc")
    try:
        literature_parser.read_text(bad)
        assert False, "expected RuntimeError"
    except RuntimeError as exc:
        assert "Unsupported file type" in str(exc)


def test_read_text_pdf_requires_dependency(tmp_path: Path) -> None:
    pdf = tmp_path / "x.pdf"
    pdf.write_bytes(b"%PDF-1.4")
    try:
        literature_parser.read_text(pdf)
        assert False, "expected RuntimeError"
    except RuntimeError as exc:
        assert "PDF parsing requires optional dependency" in str(exc)


def test_main_writes_output_json(tmp_path: Path, monkeypatch) -> None:
    inp = tmp_path / "in.txt"
    out = tmp_path / "out.json"
    inp.write_text("alpha\n\nbeta", encoding="utf-8")
    monkeypatch.setattr(
        "sys.argv",
        ["literature_parser.py", str(inp), "-o", str(out)],
    )
    rc = literature_parser.main()
    assert rc == 0
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["file_count"] == 1


def test_main_missing_input_returns_1(monkeypatch, capsys) -> None:
    monkeypatch.setattr("sys.argv", ["literature_parser.py", "missing.txt"])
    rc = literature_parser.main()
    captured = capsys.readouterr()
    assert rc == 1
    assert "Missing input files" in captured.err
