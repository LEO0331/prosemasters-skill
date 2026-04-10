#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
OUT_DIR="$ROOT_DIR/docs/skillsmp/dist"

mkdir -p "$OUT_DIR"

cp "$ROOT_DIR/SKILL.md" "$OUT_DIR/SKILL.md"
cp "$ROOT_DIR/SKILL.codex.md" "$OUT_DIR/SKILL.codex.md"
cp "$ROOT_DIR/SKILL.codex.zh.md" "$OUT_DIR/SKILL.codex.zh.md"
cp "$ROOT_DIR/docs/skillsmp/skillsmp-meta.template.json" "$OUT_DIR/skillsmp-meta.json"
cp "$ROOT_DIR/docs/skillsmp/listing.zh.md" "$OUT_DIR/listing.zh.md"
cp "$ROOT_DIR/docs/skillsmp/listing.en.md" "$OUT_DIR/listing.en.md"

cat > "$OUT_DIR/README.txt" <<'TXT'
SkillsMP submission bundle generated.

Files:
- SKILL.md
- SKILL.codex.md
- SKILL.codex.zh.md
- skillsmp-meta.json
- listing.zh.md
- listing.en.md

Next:
1. Review text for final wording.
2. Paste/upload to https://skillsmp.com/ listing workflow.
TXT

echo "Bundle ready: $OUT_DIR"
