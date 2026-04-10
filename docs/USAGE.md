# Master Distiller Usage

## Phase 2.5: Prompt-to-Build pipeline

`tools/skill_writer.py --action build` is the bridge between prompt outputs and runnable skill artifacts.

Expected inputs:
- `--profile`: stable identity and master-level configuration JSON
- `--memory`: optional memory analyzer JSON
- `--persona`: optional persona analyzer JSON
- `--citations`: optional citation manifest JSON

Output targets:
- Canonical files in `masters/{slug}/`
- Runtime files in `.claude/skills/{slug}/` via `--action combine`

## Minimal build flow

1. Parse sources
- `python3 tools/literature_parser.py works.txt criticism.txt letters.txt -o /tmp/master.parsed.json`

2. Analyze meter/style
- `python3 tools/meter_analyzer.py /tmp/master.parsed.json -o /tmp/master.meter.json`

3. Map biography timeline
- `python3 tools/biography_mapper.py biography.csv -o /tmp/master.bio.json`

4. Build citations
- `python3 tools/citation_manager.py works.txt criticism.txt letters.txt biography.csv -o /tmp/master.citations.json`

5. Build canonical package
- `python3 tools/skill_writer.py --action build --slug my-master --profile tests/fixtures/my-master/profile.json --memory tests/fixtures/my-master/memory.json --persona tests/fixtures/my-master/persona.json --citations /tmp/master.citations.json`

6. Export runnable skill
- `python3 tools/skill_writer.py --action combine --slug my-master`

## Backup and rollback

- Backup: `python3 tools/version_manager.py --action backup --slug my-master`
- Status: `python3 tools/version_manager.py --action status --slug my-master`
- Rollback: `python3 tools/version_manager.py --action rollback --slug my-master --archive /path/to/archive.tar.gz`

## Regression

Run full local regression:
- `bash scripts/regression.sh`
