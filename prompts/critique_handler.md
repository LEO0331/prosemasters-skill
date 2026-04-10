# Critique Handler Prompt

## Purpose
Handle feedback like "he would not say this" and convert it into precise revisions.

## Required Inputs
- `feedback_text`
- `current_output`
- `persona_rules`
- `citations`

## Output Contract
Return Markdown with:
- `Feedback Classification`
- `Root Cause`
- `Revision Plan`
- `Patch Text`
- `Verification Checklist`

## Guidance
- Map critique to exact violated rules.
- Prefer minimum-change corrections.
- Require at least one citation-backed justification.
