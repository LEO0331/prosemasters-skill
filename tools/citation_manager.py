#!/usr/bin/env python3
"""Assign stable citation IDs for source files and optional excerpts."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


def build_manifest(files: list[Path], excerpt_chars: int) -> dict:
    entries = []
    for path in files:
        text = path.read_text(encoding="utf-8")
        cid = f"SRC-{digest(str(path) + text[:1000])}"
        entries.append(
            {
                "citation_id": cid,
                "path": str(path),
                "chars": len(text),
                "content_hash": digest(text),
                "excerpt": text[:excerpt_chars],
            }
        )
    return {
        "version": 1,
        "source_count": len(entries),
        "sources": entries,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate citation manifest for source materials")
    ap.add_argument("inputs", nargs="+", help="Source files")
    ap.add_argument("-o", "--output", help="Output JSON path (default: stdout)")
    ap.add_argument("--excerpt-chars", type=int, default=120, help="Excerpt length per source")
    args = ap.parse_args()

    try:
        files = [Path(p) for p in args.inputs]
        missing = [str(p) for p in files if not p.exists()]
        if missing:
            raise RuntimeError(f"missing files: {', '.join(missing)}")

        payload = json.dumps(build_manifest(files, args.excerpt_chars), ensure_ascii=False, indent=2)
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
