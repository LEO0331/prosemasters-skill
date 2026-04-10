<div align="center">

# Master Distiller.skill

> *"Why imitate style when you can distill literary spirit? Welcome to digital lineage."*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-green)](https://agentskills.io)

<br>

You distilled your colleague. You distilled your ex.<br>
But have you considered this—**you can distill a literary master from a thousand years ago?**<br>
Turn Tang-Song prose masters into runnable digital scholars that can still write, argue, and respond today.<br>

**Why imitate style when you can distill literary spirit? Welcome to digital lineage.**

<br>

Provide classical texts, biographies, and critiques, plus your interpretation of the master.<br>
We deconstruct the target into a runnable structure:<br>
**Part A — Master Memory + Part B — Persona**.<br>
Generate a digital replica that reasons and writes in the master's voice.

[Data Sources](#data-sources) · [Installation](#installation) · [Usage](#usage) · [Examples](#examples)

</div>

---

## Installation

### Claude Code

> **Important**: Claude Code looks for skills in `.claude/skills/` from the **git repo root**. Run these commands in the correct location.

```bash
# Install in current project
mkdir -p .claude/skills
git clone https://github.com/YOUR_USERNAME/master-distiller-skill .claude/skills/master-distiller

# Or install globally (available in all projects)
git clone https://github.com/YOUR_USERNAME/master-distiller-skill ~/.claude/skills/master-distiller
```

### Dependencies (Optional)

```bash
pip install -r requirements.txt
```

---

## Usage

In Claude Code, type:

```
/distill-master
```

Follow the prompts to enter the master's alias, historical context, and core philosophy, then provide source materials. Fields can be filled progressively.

After creation, invoke with `/{slug}` to start writing or discussing in that master's style.

### Management Commands

| Command | Description |
|---------|-------------|
| `/list-masters` | List all master Skills |
| `/{slug}` | Full Skill (reason and write like the master) |
| `/{slug}-self` | Archive mode (biography and historical reasoning) |
| `/{slug}-persona` | Persona mode (style and expression rules only) |
| `/update-master {slug}` | Apply correction updates to one master |
| `/delete-master {slug}` | Delete |

---

## Examples

> Input: `Han Yu, Middle Tang, leader of the Classical Prose Movement, literature as moral vehicle, upright remonstration`

**Scenario 1: Short prose generation**

```
User            ❯ Write a short passage to encourage study

han-yu.skill    ❯ Learning exists to clarify the Way and make it useful.
                 If one polishes words but neglects the root,
                 the text may glitter while truth grows dim.
```

**Scenario 2: Style correction**

```
User            ❯ This line is too playful. Han Yu wouldn't say this.

han-yu.skill    ❯ Correction recorded: tone must be stricter,
                 and judgments must establish right/wrong first.
                 I will rewrite using L1/L4 constraints.
```

**Scenario 3: Modern topic translation**

```
User            ❯ What would Han Yu say about short-video culture?

han-yu.skill    ❯ Tools may be new, but principles must not be lost.
                 When technique overwhelms purpose,
                 craft increases while integrity declines.
```

---

## Data Sources

| Source | Format | Notes |
|--------|--------|-------|
| Collected works | TXT / Markdown / (optional) PDF | Core corpus for diction, cadence, and imagery |
| Biography & chronology | TXT / CSV / Markdown | Timeline, geography, and turning points |
| Later critiques | TXT / Markdown | Style boundaries and consensus signals |
| Letters and exchanges | TXT / Markdown | Private tone and social behavior |
| Human notes | Plain text | Supplemental interpretation |

### Generated Skill Structure

Each master Skill has two parts:

| Part | Contents |
|------|----------|
| **Part A — Master Memory** | Biography milestones, values, political/intellectual stance, geography, relationships |
| **Part B — Persona** | 5-layer model: hard rules -> identity -> expression style -> judgment logic -> social conduct |

Runtime logic: `Receive message -> Persona decides response strategy -> Master Memory injects historical/value context -> Output`

### Evolution Mechanics

* **Append memory** -> Add new texts/critiques -> incremental analysis -> merge into corresponding layers
* **Conversation correction** -> Say "he wouldn't say this" -> writes correction logic and updates profile
* **Version management** -> Backup on update, supports rollback

---

## Project Structure

This project follows the [AgentSkills](https://agentskills.io) open standard:

```text
master-distiller/
├── SKILL.md
├── README.md
├── README_EN.md
├── prompts/
│   ├── intake.md
│   ├── memory_analyzer.md
│   ├── literary_persona_analyzer.md
│   ├── self_builder.md
│   ├── persona_builder.md
│   ├── merger.md
│   └── critique_handler.md
├── tools/
│   ├── literature_parser.py
│   ├── meter_analyzer.py
│   ├── biography_mapper.py
│   ├── citation_manager.py
│   ├── skill_writer.py
│   └── version_manager.py
├── masters/
├── tests/fixtures/
├── scripts/regression.sh
├── docs/
│   ├── METHODOLOGY.md
│   └── USAGE.md
├── requirements.txt
└── LICENSE
```

---

## Notes

* **Source quality determines fidelity**: primary texts + biography + critiques > labels alone
* Recommended priorities:
  1. Canonical representative works
  2. Texts from turning-point periods (demotion, recall, debate)
  3. Political essays and letters (value judgments and voice)
  4. Later critiques (style boundaries)
* This is a literary modeling tool, not a final authority on historical authenticity
* Master profiles evolve as more material is added

---

## Credits

Architectural inspiration and related open-source work:
- **[yourself-skill](https://github.com/notdog1998/yourself-skill)** — dual-layer distillation structure (Memory + Persona)
- **[colleague-skill](https://github.com/titanwings/colleague-skill)** — person-to-skill distillation concept
- **[ex-partner-skill](https://github.com/therealXiaomanChu/ex-partner-skill)** — evolution mechanics in scenario adaptation

Master Distiller.skill extends these ideas to classical literary figures with emphasis on source traceability and stylistic consistency.

This project follows the [AgentSkills](https://agentskills.io) open standard and is compatible with Claude Code.

---

### Final Words

> "Lineage does not die. It waits to be rewritten."

This Skill does not replace historical masters. It converts their stylistic logic and rhetorical structure into a dialog-capable digital form.

You can correct it, iterate it, reject it, and rebuild it in the next version.

**After all, the core of digital lineage is not imitation—it is controlled reconstruction.**

MIT License © Contributors
