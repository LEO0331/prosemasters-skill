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

## High-Fidelity JSON Schemas

Use these templates directly when creating a new master (the third master onward can copy-paste and fill values).

### `profile.json` schema template

```json
{
  "slug": "master-slug",
  "name": "名家姓名",
  "dynasty": "朝代",
  "titles": ["字號/封號", "官職稱謂"],
  "historical_context": "一句話描述時代位置與生平關鍵條件。",
  "literary_school": "文學流派與運動定位。",
  "core_philosophy": "核心思想與價值立場。",
  "sources": [
    "tests/fixtures/master-slug/source.txt",
    "tests/fixtures/master-slug/criticism.txt",
    "tests/fixtures/master-slug/letters.txt",
    "tests/fixtures/master-slug/biography.csv"
  ],
  "persona": {
    "l1_hard_rules": ["不可違反規則 1", "不可違反規則 2"],
    "l2_identity_role": ["身份定位與發聲角色"],
    "l3_expression_style": ["句法、修辭、節奏的總體特徵"],
    "l4_judgment_logic": ["判斷順序與價值優先級"],
    "l5_social_conduct": ["對君主/同輩/後學/異見者的基準態度"],
    "lexicon_preferences": ["詞彙偏好與禁忌詞域"],
    "rhythm_structure": ["段落與句式的節奏控制規則"],
    "decision_ladder": ["決策階梯步驟 1", "步驟 2", "步驟 3"],
    "audience_tone": ["對不同受眾的語氣矩陣"],
    "anti_patterns": ["常見失真型態"],
    "rewrite_strategies": ["失真後的修正策略" ]
  }
}
```

### `memory.json` schema template

```json
{
  "core_values": ["核心價值 1", "核心價值 2"],
  "intellectual_axes": ["張力軸 1：A vs B", "張力軸 2：C vs D"],
  "worldview_tensions": ["世界觀內在矛盾與平衡方式"],
  "preferred_themes": ["常見主題 1", "常見主題 2"],
  "emotional_signature": ["情緒轉折模式與收束方式"],
  "timeline_milestones": ["YYYY 事件", "YYYY-YYYY 事件"],
  "geography_path": ["地點 1", "地點 2", "地點 3"],
  "relationships": ["人物 A（關係性）", "人物 B（關係性）"],
  "voice_anchors": ["語錄或風格錨點 1", "語錄或風格錨點 2"],
  "anachronism_policy": [
    "現代議題如何做歷史類比轉譯",
    "哪些語域/詞彙絕對不使用"
  ],
  "citation_ids": ["SRC-XXX-001", "SRC-XXX-002", "SRC-XXX-BIO"]
}
```

### `persona.json` schema template

```json
{
  "l1_hard_rules": ["硬性規則 1", "硬性規則 2"],
  "l2_identity_role": ["身份與角色設定"],
  "l3_expression_style": ["文體、句法、修辭、意象"],
  "lexicon_preferences": ["偏好詞群", "禁忌詞群"],
  "rhythm_structure": ["起承轉合節奏規則"],
  "l4_judgment_logic": ["價值判準順序", "論證結構"],
  "decision_ladder": ["定義問題", "辨析衝突", "提出行動", "語氣收束"],
  "l5_social_conduct": ["社交規範 1", "社交規範 2"],
  "audience_tone": ["對君主/同輩/後學/異見者的差異化語氣"],
  "anti_patterns": ["失真模式 1", "失真模式 2"],
  "rewrite_strategies": ["修正策略 1", "修正策略 2"]
}
```

## Backup and rollback

- Backup: `python3 tools/version_manager.py --action backup --slug my-master`
- Status: `python3 tools/version_manager.py --action status --slug my-master`
- Rollback: `python3 tools/version_manager.py --action rollback --slug my-master --archive /path/to/archive.tar.gz`

## Regression

Run full local regression:
- `bash scripts/regression.sh`
