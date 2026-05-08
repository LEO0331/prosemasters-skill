# System Design Review: Master Persona Builder

## 1. Scope and context
This review covers `apps/master-persona-builder` only.

Primary runtime model:
- Static frontend (`index.html`, `styles.css`, `app.js`)
- Serverless Python APIs (`api/validate.py`, `api/generate.py`, `api/health.py`)
- Shared normalization/validation/render helpers (`api/_lib.py`)
- Optional repository toolchain execution (`tools/*.py`) with template fallback

## 2. High-level architecture
```mermaid
flowchart TD
  U[User Browser] --> F[Static UI\nindex.html + app.js]
  F --> V[/api/validate]
  F --> G[/api/generate]

  V --> L[_lib.py\nnormalize + validate + auth + CORS]
  G --> L

  G --> D{repo_root found\n+ tools available?}
  D -- yes --> T[Run toolchain\nliterature_parser/meter/biography/citation\nthen skill_writer build+combine]
  D -- no/fail --> R[Template render\nrender_skill_md + render_wiki_md]

  T --> O[files + tool_plan + warnings]
  R --> O
  O --> F
```

## 3. Request/response contract
Request (normalized shape):
- `meta`: identity and generation metadata (`slug`, `name`, `description`, `version`, `language`, `target_platforms`)
- `master`: persona identity baseline (`display_name`, `dynasty`, etc.)
- `memory`: list-based memory facets
- `persona`: list-based behavioral/style constraints
- `commands`: trigger command templates
- `source_materials[]`: array of `{category, title, content}`

Response:
- `ok`, `warnings`
- `files`: generated `SKILL.md`, `wiki.md`, and optionally `self.md/persona.md/meta.json/sources.json`
- `tool_plan`: `mode`, `routes`, `executions[]`

## 4. Key architectural tradeoffs

### 4.1 Frontend -> Python API (direct)
Chosen because:
- Lowest moving parts for deployment and maintenance
- No extra gateway auth/routing layer
- Fastest path for deterministic form-to-file generation

Tradeoff:
- Python API must own all boundary concerns (CORS, auth, validation, limits)
- Harder to split concerns when traffic/complexity grows

Alternative:
- Node gateway + Python workers
- Better protocol translation and rate limiting flexibility
- More operational overhead and higher latency

### 4.2 Serverless, stateless execution
Chosen because:
- Scales for bursty, interactive generation traffic
- No persistent infrastructure needed
- Cost-efficient for low/medium volume

Tradeoff:
- Cold starts and subprocess runtime constraints
- `/tmp` and execution time limits constrain heavy data extraction

Alternative:
- Containerized long-running API service
- Better control for large jobs and warm caches
- Higher fixed cost and operational burden

### 4.3 Repo-tools mode with template fallback
Chosen because:
- Preserves high-fidelity generation when full toolchain exists
- Still returns useful output in constrained runtimes
- Improves reliability from user perspective

Tradeoff:
- Dual-path behavior can hide toolchain regressions if fallback is overused

Alternative:
- Hard-fail when toolchain unavailable
- Stronger correctness signal, worse availability/UX

### 4.4 Subprocess boundary for toolchain
Chosen because:
- Reuses existing CLI tools with minimal rewrite risk
- Strong fault isolation by process

Tradeoff:
- Serialization to temp files adds overhead
- Error handling and observability are more complex than in-process calls

Alternative:
- Import tools as Python modules (in-process)
- Faster and cleaner typed interfaces
- Requires larger refactor and tighter coupling

## 5. Data structure choices and alternatives

### 5.1 Why nested object + list model (`meta/master/memory/persona/commands/source_materials`)
Chosen because:
- Maps naturally to domain semantics (identity vs memory vs style)
- Stable keys enable deterministic rendering templates
- Backward-compatible extension: add optional keys without breaking old payloads

Alternative A: flat object with 100+ keys
- Pros: simple at first glance
- Cons: naming collisions, weak domain boundaries, painful evolution

Alternative B: strongly versioned typed schema per edition (`v1`, `v2`, ...)
- Pros: strict compatibility control
- Cons: migration complexity for UI and generated examples

### 5.2 Why arrays for memory/persona fields
Chosen because:
- Order matters in writing constraints (priority and rhythm)
- Easy UI input model (one line = one item)
- Easier template bullet rendering

Alternative A: map/object sets (`{"key": true}`)
- Pros: dedup semantics
- Cons: loses meaningful order and reduces expressive nuance

Alternative B: rich objects per line (`{text, weight, source}`)
- Pros: future scoring and provenance
- Cons: significantly higher UX and validation complexity now

### 5.3 Why `source_materials` is array of records
Chosen because:
- Supports repeated categories with different sources
- Preserves user ordering
- Simple routing by `category`

Alternative A: category-indexed map (`{works: [...], biography: [...]}`)
- Pros: direct access per category
- Cons: harder to preserve original cross-category sequence; more UI mapping logic

Alternative B: normalized relational storage (SQL tables)
- Pros: querying and analytics
- Cons: overkill for synchronous serverless generation path

### 5.4 Why `tool_plan.executions[]` append-only records
Chosen because:
- Human-auditable execution log
- Direct fit for frontend table rendering
- Easy to enrich (`status`, `exit_code`, `stderr`, `duration_ms`)

Alternative A: DAG execution graph
- Pros: models dependency topology precisely
- Cons: too heavy for current linear/sublinear pipeline and UI

Alternative B: opaque string logs only
- Pros: implementation simplicity
- Cons: weak machine readability and poor UX

### 5.5 Why `files` as a keyed JSON object of text outputs
Chosen because:
- Immediate frontend display/copy/download without extra fetch
- Works for both template and repo-tool modes

Alternative A: zip binary response
- Pros: packaging efficiency for many files
- Cons: worse inline preview and browser-side processing complexity

Alternative B: object storage URLs
- Pros: offloads payload size and caching
- Cons: requires signed URL flow and lifecycle management

## 6. Current risk profile and mitigations
1. Mode divergence risk (repo-tools vs template)
- Mitigation: expose `tool_plan.mode` + warnings; keep regression tests for both paths.

2. Subprocess reliability risk
- Mitigation: timeout/env limits, bounded output capture, per-step status records.

3. Input abuse risk
- Mitigation: content length/item caps, origin restrictions, optional API key.

4. Schema drift risk between frontend and backend
- Mitigation: maintain `shared/schema.json` + integration tests on normalized payload.

## 7. Deep-dive Q&A prep (English)
1. Why not force one single generation path?
- Because availability is prioritized: template fallback guarantees useful output even when repo tools are not runnable in serverless.

2. Why keep data mostly untyped lists instead of weighted structures?
- Current goal is deterministic authoring output, not ranking/ML scoring. Lists minimize friction and keep author intent order.

3. Why not use a database?
- Current flow is request-scoped generation with no persistent transactional requirement. File/text outputs are sufficient and cheaper.

4. What breaks first at scale?
- Subprocess-heavy tool execution under serverless time/memory limits; next bottleneck is payload size and total source parsing latency.

5. How to evolve toward enterprise usage?
- Introduce async job queue + persistent artifact storage + strict versioned schema contracts + observability traces.

6. Why return execution logs to frontend?
- Improves trust and debuggability for users, especially when mixed source categories route to different tools.

7. How do we prevent sensitive local path leakage?
- Tool names are normalized to repo-relative or basename before returning (`_display_tool_name`).

## 8. Suggested next design checkpoints
- Add explicit API contract version field (`meta.contract_version`)
- Add dual-mode golden tests (repo-tools + template fallback)
- Add optional async execution mode for large corpora
- Add structured audit IDs for tool_plan steps
