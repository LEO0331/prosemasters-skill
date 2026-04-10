# SkillsMP Publishing Kit

This folder contains the materials and process to publish this skill on https://skillsmp.com/.

## What to prepare

- Canonical skill file: `SKILL.md`
- Listing metadata: `docs/skillsmp/skillsmp-meta.template.json`
- Listing copy (ZH): `docs/skillsmp/listing.zh.md`
- Optional listing copy (EN): `docs/skillsmp/listing.en.md`

## Field mapping (SkillsMP)

- `name` -> skill short name (e.g. `master-distiller`)
- `description` -> one-line role statement
- `Role` -> narrative role/persona paragraph
- `Mission` -> outcome-oriented execution mission
- `Work Principles` -> operational constraints and quality gates
- `Execution` -> implementation and verification expectations

## Recommended publishing flow

1. Update `SKILL.md` and verify it reflects the latest behavior.
2. Fill `skillsmp-meta.template.json`.
3. Update `listing.zh.md` and (optional) `listing.en.md`.
4. Run `bash docs/skillsmp/build_bundle.sh` to create a submission bundle.
5. Upload/paste bundle content to SkillsMP listing form.

## Verification before publish

- `bash scripts/regression.sh`
- Confirm generated examples still pass:
  - `masters/examples/su-shi/`
  - `masters/examples/han-yu/`
- Confirm listing text and SKILL behavior are aligned (commands, constraints, outputs).
