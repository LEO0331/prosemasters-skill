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
  CORPUS_MAIN="tests/fixtures/$slug/source.txt"
  CORPUS_CRITIC="tests/fixtures/$slug/criticism.txt"
  CORPUS_LETTERS="tests/fixtures/$slug/letters.txt"
  BIO_CSV="tests/fixtures/$slug/biography.csv"

  echo "[3/8] parse source: $slug"
  python3 tools/literature_parser.py "$CORPUS_MAIN" "$CORPUS_CRITIC" "$CORPUS_LETTERS" -o "/tmp/$slug.parsed.json"

  echo "[4/8] meter analysis: $slug"
  python3 tools/meter_analyzer.py "/tmp/$slug.parsed.json" -o "/tmp/$slug.meter.json"

  echo "[5/8] biography + citation map: $slug"
  python3 tools/biography_mapper.py "$BIO_CSV" -o "/tmp/$slug.bio.json"
  python3 tools/citation_manager.py "$CORPUS_MAIN" "$CORPUS_CRITIC" "$CORPUS_LETTERS" "$BIO_CSV" -o "/tmp/$slug.citations.json"

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

echo "[9/9] security hardening checks"
if python3 tools/skill_writer.py --action delete --slug ../../tmp >/dev/null 2>&1; then
  echo "FAIL: path traversal slug was accepted by skill_writer"
  exit 1
fi

if python3 tools/version_manager.py --action status --slug ../../tmp >/dev/null 2>&1; then
  echo "FAIL: path traversal slug was accepted by version_manager"
  exit 1
fi

touch /tmp/fake.tar.gz
if python3 tools/version_manager.py --action rollback --slug su-shi --archive /tmp/fake.tar.gz >/dev/null 2>&1; then
  echo "FAIL: untrusted external archive was accepted without override"
  exit 1
fi

echo "Regression completed"
