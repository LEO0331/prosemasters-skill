#!/usr/bin/env python3
"""Map biography events into a timeline and geography list."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path


LINE_PATTERN = re.compile(r"^\s*(\d{3,4}(?:[-/]\d{1,2})?(?:[-/]\d{1,2})?)\s*[\t,，]\s*([^\t,，]+)\s*[\t,，]\s*(.+)$")


def parse_txt(path: Path) -> list[dict]:
    events = []
    for line in path.read_text(encoding="utf-8").splitlines():
        m = LINE_PATTERN.match(line)
        if not m:
            continue
        events.append({"date": m.group(1), "place": m.group(2).strip(), "event": m.group(3).strip()})
    return events


def parse_csv(path: Path) -> list[dict]:
    events = []
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            date = (row.get("date") or "").strip()
            place = (row.get("place") or "").strip()
            event = (row.get("event") or "").strip()
            if date and place and event:
                events.append({"date": date, "place": place, "event": event})
    return events


def main() -> int:
    ap = argparse.ArgumentParser(description="Build timeline and exile/geography map from biography records")
    ap.add_argument("input", help="Input .txt or .csv with date/place/event records")
    ap.add_argument("-o", "--output", help="Output JSON path (default: stdout)")
    args = ap.parse_args()

    try:
        path = Path(args.input)
        if not path.exists():
            raise RuntimeError(f"input does not exist: {path}")
        if path.suffix.lower() == ".csv":
            events = parse_csv(path)
        else:
            events = parse_txt(path)
        events.sort(key=lambda x: x["date"])

        places = []
        seen = set()
        for e in events:
            p = e["place"]
            if p not in seen:
                seen.add(p)
                places.append(p)

        payload_obj = {
            "event_count": len(events),
            "timeline": events,
            "geography_path": places,
        }
        payload = json.dumps(payload_obj, ensure_ascii=False, indent=2)
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
