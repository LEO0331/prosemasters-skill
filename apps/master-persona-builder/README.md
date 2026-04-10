# Master Persona Builder (Frontend -> Python API)

[![Vercel Runtime](https://img.shields.io/badge/Vercel-Python%20Functions-black)](https://vercel.com)
[![Security Guardrails](https://img.shields.io/badge/Security-CORS%20%2B%20API%20Key%20%2B%20Limits-0a7f5a)](#notes)
[![CI](https://img.shields.io/badge/GitHub%20Actions-Security%20%2F%20Test-1f6feb)](../../.github/workflows/deploy-master-persona-builder.yml)

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
- Production should set `MPB_ALLOWED_ORIGINS`.
- If server sets `MPB_API_KEY`, enter the same key in the UI `API Key` field (stored in browser `localStorage` and sent as `X-API-Key`).
- Request hardening envs: `MPB_SUBPROCESS_TIMEOUT_SEC`, `MPB_MAX_SOURCE_ITEMS`, `MPB_MAX_SOURCE_CHARS`, `MPB_MAX_TOTAL_SOURCE_CHARS`, `MPB_MAX_BIOGRAPHY_STEPS`.
- GitHub Actions workflow is security/test only (no deploy): `.github/workflows/deploy-master-persona-builder.yml`.
