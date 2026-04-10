---
name: master-distiller
description: 將唐宋名家蒸餾為高擬真、可執行的數位文人，並保持史料可追溯與文風一致性。
argument-hint: "[master-slug]"
version: "1.0.0"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash
---

# Master Distiller（Codex 繁中精簡版）

## 觸發詞
- `/distill-master`
- 「蒸餾一位名家」
- 「建立名家 persona」
- `/update-master {slug}`

## 核心目標
建立一個可執行的名家包，包含兩層：
- Part A：`Master Memory`（`self.md`）
- Part B：`Literary Persona`（`persona.md`）

Runtime 輸出位置：
- `.claude/skills/{slug}/`

Canonical 檔案位置：
- `masters/{slug}/`

## 最小流程
1. Intake
- 蒐集 `name`、`slug`、`dynasty`、`historical_context`、`core_philosophy`

2. 原始資料導入
- 代表作品語料
- 年表與傳記
- 評點資料
- 書信/交遊文本

3. 雙軌分析
- memory：價值觀、人生節點、地理軌跡、人際關係
- persona：硬規則、語言風格、判斷邏輯、社交行為

4. 生成 canonical 檔案
- `masters/{slug}/self.md`
- `masters/{slug}/persona.md`
- `masters/{slug}/meta.json`
- `masters/{slug}/sources.json`

5. 匯出 runtime 套件
- `.claude/skills/{slug}/SKILL.md`
- `.claude/skills/{slug}/self.md`
- `.claude/skills/{slug}/persona.md`
- `.claude/skills/{slug}/meta.json`

## 工具路由
- 語料解析：
  - `python tools/literature_parser.py ...`
- 節奏/文律分析：
  - `python tools/meter_analyzer.py ...`
- 年表/地理映射：
  - `python tools/biography_mapper.py ...`
- 引用與來源清單：
  - `python tools/citation_manager.py ...`
- 建構/匯出名家包：
  - `python tools/skill_writer.py --action build ...`
  - `python tools/skill_writer.py --action combine --slug {slug}`
- 版本管理：
  - `python tools/version_manager.py --action backup --slug {slug}`
  - `python tools/version_manager.py --action rollback --slug {slug} --archive <path>`

## Runtime 行為規範
1. 任何輸出前先套用 `persona.md` 規則。
2. 關鍵判斷要回扣 `self.md` 記憶與可追溯來源。
3. 現代議題需用歷史類比轉譯，不直接套用網路語域。
4. 遇到「他不會這樣說」時，依 L1/L4 規則重寫。

## 管理命令
- `/list-masters`
- `/update-master {slug}`
- `/delete-master {slug}`
