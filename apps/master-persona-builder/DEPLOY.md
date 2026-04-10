# Deploy Guide (Vercel)

## Target
Deploy this folder as an isolated app:
- Root Directory: `apps/master-persona-builder`

## Steps
1. Import repository into Vercel.
2. Set project Root Directory to `apps/master-persona-builder`.
3. Deploy with default settings.

## Recommended Security Environment Variables
- `MPB_ALLOWED_ORIGINS`: comma-separated allowlist, e.g. `https://your-domain.com,https://www.your-domain.com`
- `MPB_API_KEY`: optional API key for `/api/validate` and `/api/generate`
- `MPB_SUBPROCESS_TIMEOUT_SEC`: subprocess timeout per tool step (default: `25`)
- `MPB_MAX_SOURCE_ITEMS`: max `source_materials` entries (default: `24`)
- `MPB_MAX_SOURCE_CHARS`: max characters per source item (default: `30000`)
- `MPB_MAX_TOTAL_SOURCE_CHARS`: max total characters across all source items (default: `200000`)
- `MPB_MAX_BIOGRAPHY_STEPS`: max biography mapping steps (default: `8`)
- `MPB_EXPOSE_TOOL_LOGS`: set `true` only for debugging; keep unset/false in production

## GitHub Actions (Security/Test Only)
Workflow file: `.github/workflows/deploy-master-persona-builder.yml`

This workflow does **not** deploy. It only runs syntax/regression/security-oriented checks.
No Vercel secrets are required for this workflow.

## Endpoints
- `GET /api/health`
- `POST /api/validate`
- `POST /api/generate`

## Runtime Notes
- Python functions use `/tmp` for temporary files.
- If root repo tools are available in runtime, `/api/generate` uses them.
- If not available, `/api/generate` falls back to template-only output.
