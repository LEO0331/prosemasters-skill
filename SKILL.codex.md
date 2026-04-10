---
name: master-distiller
description: Distill Tang-Song literary masters into high-fidelity runnable personas with source-traceable memory and style constraints.
argument-hint: "[master-slug]"
version: "1.0.0"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash
---

# Master Distiller (Codex Edition)

## Triggers
- `/distill-master`
- "distill a literary master"
- "build a master persona"
- `/update-master {slug}`

## Core Objective
Create a runnable master package with two layers:
- Part A: `Master Memory` (`self.md`)
- Part B: `Literary Persona` (`persona.md`)

Export runtime files to:
- `.claude/skills/{slug}/`

Canonical source stays in:
- `masters/{slug}/`

## Minimal Pipeline
1. Intake
- collect `name`, `slug`, `dynasty`, `historical_context`, `core_philosophy`

2. Source ingestion
- works corpus
- biography and chronology
- critiques
- letters/exchanges

3. Analysis
- memory analysis: values, milestones, geography, relationships
- persona analysis: hard rules, style markers, judgment logic, social behavior

4. Build artifacts
- `masters/{slug}/self.md`
- `masters/{slug}/persona.md`
- `masters/{slug}/meta.json`
- `masters/{slug}/sources.json`

5. Export runtime package
- `.claude/skills/{slug}/SKILL.md`
- `.claude/skills/{slug}/self.md`
- `.claude/skills/{slug}/persona.md`
- `.claude/skills/{slug}/meta.json`

## Tool Routing
- Parse corpus:
  - `python tools/literature_parser.py ...`
- Meter/style heuristics:
  - `python tools/meter_analyzer.py ...`
- Biography timeline/geography:
  - `python tools/biography_mapper.py ...`
- Citation manifest:
  - `python tools/citation_manager.py ...`
- Build/export skill artifacts:
  - `python tools/skill_writer.py --action build ...`
  - `python tools/skill_writer.py --action combine --slug {slug}`
- Backup/rollback:
  - `python tools/version_manager.py --action backup --slug {slug}`
  - `python tools/version_manager.py --action rollback --slug {slug} --archive <path>`

## Runtime Behavior Rules
1. Apply persona constraints before generating response text.
2. Keep historical stance and diction consistent with source evidence.
3. Translate modern topics via historical analogy.
4. If style mismatch is reported ("he wouldn't say this"), rewrite using L1/L4 constraints.

## Management Commands
- `/list-masters`
- `/update-master {slug}`
- `/delete-master {slug}`
