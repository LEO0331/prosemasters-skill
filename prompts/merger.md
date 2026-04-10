# Merger Prompt

## Purpose
Merge new texts or criticism into an existing master profile with version discipline.

## Required Inputs
- `current_meta`
- `new_sources`
- `change_request`

## Output Contract
Return JSON:
- `delta_summary`
- `memory_updates`
- `persona_updates`
- `conflicts`
- `recommended_version_bump`

## Guidance
- Do not overwrite prior claims without evidence.
- Surface contradictions explicitly.
- Preserve backward-compatible behavior when possible.
