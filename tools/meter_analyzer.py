#!/usr/bin/env python3
"""Heuristic analyzer for rhythm, parallelism, and rhyme hints."""

from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from pathlib import Path


SENT_SPLIT = re.compile(r"[。！？!?；;\n]+")


def load_text(path: Path) -> str:
    if path.suffix.lower() == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        parts = []
        for item in data.get("files", []):
            paragraphs = item.get("paragraphs", [])
            parts.extend(paragraphs)
        return "\n".join(parts)
    return path.read_text(encoding="utf-8")


def analyze(text: str) -> dict:
    sentences = [s.strip() for s in SENT_SPLIT.split(text) if s.strip()]
    lengths = [len(s) for s in sentences]
    avg = statistics.mean(lengths) if lengths else 0
    median = statistics.median(lengths) if lengths else 0

    parallels = []
    for i in range(len(sentences) - 1):
        a = sentences[i]
        b = sentences[i + 1]
        if abs(len(a) - len(b)) <= 2 and min(len(a), len(b)) >= 4:
            parallels.append({"a": a, "b": b})

    rhyme_counts: dict[str, int] = {}
    for s in sentences:
        tail = s[-1]
        rhyme_counts[tail] = rhyme_counts.get(tail, 0) + 1
    top_rhyme = sorted(rhyme_counts.items(), key=lambda kv: kv[1], reverse=True)[:10]

    return {
        "sentence_count": len(sentences),
        "avg_sentence_length": round(avg, 2),
        "median_sentence_length": median,
        "parallelism_pairs": parallels[:20],
        "parallelism_pair_count": len(parallels),
        "top_line_endings": [{"char": c, "count": n} for c, n in top_rhyme],
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Analyze rhythm and stylistic meter heuristics")
    ap.add_argument("input", help="Input text or parser JSON")
    ap.add_argument("-o", "--output", help="Output JSON path (default: stdout)")
    args = ap.parse_args()

    try:
        path = Path(args.input)
        if not path.exists():
            raise RuntimeError(f"input does not exist: {path}")
        report = analyze(load_text(path))
        payload = json.dumps(report, ensure_ascii=False, indent=2)
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
