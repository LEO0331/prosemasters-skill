#!/usr/bin/env python3
"""Parse classical literature sources into a normalized JSON artifact."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Iterable


def read_text(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".txt", ".md"}:
        return path.read_text(encoding="utf-8")
    if suffix == ".pdf":
        try:
            from pypdf import PdfReader  # type: ignore
        except Exception as exc:  # pragma: no cover
            raise RuntimeError("PDF parsing requires optional dependency: pypdf") from exc
        reader = PdfReader(str(path))
        return "\n".join((page.extract_text() or "") for page in reader.pages)
    raise RuntimeError(f"Unsupported file type: {path}")


def normalize(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def to_paragraphs(text: str) -> list[str]:
    chunks = [c.strip() for c in re.split(r"\n\s*\n", text)]
    return [c for c in chunks if c]


def parse_files(files: Iterable[Path]) -> dict:
    parsed = []
    total_chars = 0
    total_paragraphs = 0
    for path in files:
        raw = read_text(path)
        cleaned = normalize(raw)
        paragraphs = to_paragraphs(cleaned)
        total_chars += len(cleaned)
        total_paragraphs += len(paragraphs)
        parsed.append(
            {
                "path": str(path),
                "chars": len(cleaned),
                "paragraph_count": len(paragraphs),
                "preview": cleaned[:200],
                "paragraphs": paragraphs,
            }
        )
    return {
        "version": 1,
        "file_count": len(parsed),
        "total_chars": total_chars,
        "total_paragraphs": total_paragraphs,
        "files": parsed,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Parse literature files into normalized JSON")
    parser.add_argument("inputs", nargs="+", help="Input files (.txt/.md/.pdf)")
    parser.add_argument("-o", "--output", help="Output JSON path (default: stdout)")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        files = [Path(p) for p in args.inputs]
        missing = [str(p) for p in files if not p.exists()]
        if missing:
            raise RuntimeError(f"Missing input files: {', '.join(missing)}")

        data = parse_files(files)
        payload = json.dumps(data, ensure_ascii=False, indent=2)
        if args.output:
            out = Path(args.output)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(payload + "\n", encoding="utf-8")
        else:
            print(payload)
        return 0
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
