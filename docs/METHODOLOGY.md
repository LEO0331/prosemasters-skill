# Literary Distillation Methodology

This project models Tang-Song literary masters as runnable skill profiles using a two-part architecture:
- Master Memory (historical grounding)
- Literary Persona (stylistic execution filter)

V1 methodology:
1. Ingest primary works and historical records.
2. Extract timeline, values, and social context.
3. Distill rhetorical and structural writing signals.
4. Build `self.md` and `persona.md` with citation traceability.
5. Export runtime skill packages into `.claude/skills/{slug}`.

Current limitations:
- Meter and parallelism analysis is heuristic in v1.
- OCR/PDF-heavy workflows are not guaranteed yet.
- Citation mapping is deterministic but not a scholarly critical edition.
