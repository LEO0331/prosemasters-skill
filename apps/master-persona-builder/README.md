# Master Persona Builder (Frontend -> Python API)

This app is isolated from existing repository functionality.

## What it does
- Accepts form input or custom JSON
- Validates payload with `/api/validate`
- Generates `SKILL.md` and `wiki.md` with `/api/generate`
- Returns optional `self.md/persona.md/meta.json/sources.json` when repo tools are available

## Template Mode
- If runtime cannot access root repo tools (`tools/skill_writer.py` etc.), API falls back to **template mode**.
- Template mode still generates `SKILL.md` and `wiki.md`, but skips deeper canonical/runtime package generation.

## Source category routing
Send `source_materials[]` with:
- `category`: `works` | `criticism` | `letters` | `biography` | `citation`
- `title`
- `content`

`/api/generate` returns `tool_plan.routes[]`, mapping each category to extraction tools:
- `works` -> `literature_parser.py` + `meter_analyzer.py`
- `criticism` -> `literature_parser.py`
- `letters` -> `literature_parser.py`
- `biography` -> `biography_mapper.py`
- `citation` -> `citation_manager.py`

## Local structure
- `index.html`, `styles.css`, `app.js`: static frontend
- `api/*.py`: Vercel Python Functions
- `shared/schema.json`: JSON schema reference
- `shared/examples/master.example.json`: starter payload

## Deploy on Vercel
1. Import repository into Vercel
2. Set Root Directory to `apps/master-persona-builder`
3. Deploy

## Notes
- Python functions use `/tmp` for temporary files.
- If root repo tools are unavailable in runtime, generate falls back to template-only output.
- Production should set `MPB_ALLOWED_ORIGINS` and (optionally) `MPB_API_KEY` to reduce cross-origin abuse risk.
