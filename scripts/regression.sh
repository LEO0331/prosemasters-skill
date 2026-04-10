#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "[1/8] py_compile"
python3 -m py_compile tools/*.py

echo "[2/8] help checks"
python3 tools/literature_parser.py --help >/dev/null
python3 tools/meter_analyzer.py --help >/dev/null
python3 tools/biography_mapper.py --help >/dev/null
python3 tools/citation_manager.py --help >/dev/null
python3 tools/skill_writer.py --help >/dev/null
python3 tools/version_manager.py --help >/dev/null

for slug in su-shi han-yu; do
  echo "[3/8] parse source: $slug"
  python3 tools/literature_parser.py "tests/fixtures/$slug/source.txt" -o "/tmp/$slug.parsed.json"

  echo "[4/8] meter analysis: $slug"
  python3 tools/meter_analyzer.py "/tmp/$slug.parsed.json" -o "/tmp/$slug.meter.json"

  echo "[5/8] citation map: $slug"
  python3 tools/citation_manager.py "tests/fixtures/$slug/source.txt" -o "/tmp/$slug.citations.json"

  echo "[6/8] build+combine: $slug"
  python3 tools/skill_writer.py --action build --slug "$slug" \
    --profile "tests/fixtures/$slug/profile.json" \
    --memory "tests/fixtures/$slug/memory.json" \
    --persona "tests/fixtures/$slug/persona.json" \
    --citations "/tmp/$slug.citations.json" >/dev/null
  python3 tools/skill_writer.py --action combine --slug "$slug" >/dev/null

  echo "[7/8] backup+status: $slug"
  python3 tools/version_manager.py --action backup --slug "$slug" >/tmp/$slug.backup.json
  python3 tools/version_manager.py --action status --slug "$slug" >/dev/null

done

echo "[8/8] list masters"
python3 tools/skill_writer.py --action list

echo "Regression completed"
