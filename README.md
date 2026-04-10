<div align="center">

# 名家蒸餾器.skill

> *"與其模仿風格，不如蒸餾風骨。歡迎加入數位文脈！"*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-green)](https://agentskills.io)

<br>

同事跑了，你蒸餾同事。前任分了，你蒸餾前任。<br>
但有沒有想過——**還可以蒸餾一位千年前的文豪？**<br>
把唐宋八大家拆成可運行的數位文人，讓他們在今天繼續寫作、議論與回應。<br>

**與其模仿風格，不如蒸餾風骨。歡迎加入數位文脈！**

<br>

提供傳世文本、史料、評點，再加上你對該名家的理解<br>
我們將其解構為一套可運行結構：<br>
**Part A — Master Memory（文學生平記憶）+ Part B — Persona（辭章人格模型）**<br>
生成一個能按該名家語氣思考、按其文律回應的數位鏡像

[安裝](#安裝) · [使用](#使用) · [效果示例](#效果示例) · [English](README_EN.md)

</div>

---

## 安裝

### Claude Code

> **重要**：Claude Code 從 **git 倉庫根目錄** 的 `.claude/skills/` 查找 skill。請在正確位置執行。

```bash
# 安裝到目前專案（在 git 倉庫根目錄執行）
mkdir -p .claude/skills
git clone <YOUR_REPO_URL> .claude/skills/master-distiller

# 或安裝到全域（所有專案都能用）
git clone <YOUR_REPO_URL> ~/.claude/skills/master-distiller
```

### 依賴（可選）

```bash
pip install -r requirements.txt
```

---

## 使用

在 Claude Code 中輸入：

```
/distill-master
```

按提示輸入名家代號、朝代背景、精神核心，然後提供文本與史料。所有欄位可漸進補充。

完成後用 `/{slug}` 調用該名家 Skill，進入文風對話/創作模式。

### 管理命令

| 命令 | 說明 |
|------|------|
| `/list-masters` | 列出所有名家 Skill |
| `/{slug}` | 調用完整名家 Skill（按該名家思考與表達） |
| `/{slug}-self` | 名家檔案模式（生平與思想脈絡） |
| `/{slug}-persona` | 人格模式（僅文風與表達規則） |
| `/update-master {slug}` | 對話糾正後更新該名家畫像 |
| `/delete-master {slug}` | 刪除對應鏡像 |

---

## 效果示例

> 輸入：`韓愈，中唐，古文運動領袖，文以載道，剛直進諫`

**場景一：議論文生成**

```
使用者        ❯ 寫一段勸學短文

han-yu.skill ❯ 學者，所以明道而致用也。苟徒飾辭章，不求其本，
               則文雖工而道愈晦。故為學之要，在立志、在勤行、
               在審問而篤思，不可一日自欺。
```

**場景二：風格糾正**

```
使用者        ❯ 這句太輕佻了，韓愈不會這樣說

han-yu.skill ❯ 已記錄糾正：語氣應更峻直、論斷應先立是非。
               我將按 L1/L4 規則重寫該段。
```

**場景三：現代議題轉譯**

```
使用者        ❯ 如果韓愈看短影片會怎麼說

han-yu.skill ❯ 器可新，而道不可失。若以末技奪其本心，
               則日見其巧，歲失其正。
```

---

## 功能特性

### 資料來源

| 來源 | 格式 | 備註 |
|------|------|------|
| 名家全集 | TXT / Markdown /（可選）PDF | 核心語料，提取句法、虛詞、意象 |
| 史料與年譜 | TXT / CSV / Markdown | 提取時間線、地理軌跡、關鍵轉折 |
| 後世評點 | TXT / Markdown | 捕捉文風特質與後世共識 |
| 書信與往來 | TXT / Markdown | 提取私人語氣與人際風格 |
| 人工口述補充 | 純文字 | 用於補齊解釋框架 |

### 生成的 Skill 結構

每個名家 Skill 由兩部分組成：

| 部分 | 內容 |
|------|------|
| **Part A — Master Memory** | 生平節點、價值觀、政治與思想立場、地理與關係網絡 |
| **Part B — Persona** | 5 層人格結構：硬規則 -> 身分 -> 表達風格 -> 判斷邏輯 -> 社交行為 |

運行邏輯：`收到訊息 -> Persona 決定該名家如何回應 -> Master Memory 注入歷史與價值背景 -> 輸出`

### 進化機制

- **追加記憶** -> 導入新史料/新評點 -> 增量分析 -> merge 到對應層
- **對話糾正** -> 說「他不會這樣說」-> 寫入 correction 邏輯並更新畫像
- **版本管理** -> 每次更新可備份，支援回滾

---

## 專案結構

本專案遵循 [AgentSkills](https://agentskills.io) 開放標準：

```text
master-distiller/
├── SKILL.md
├── README.md
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

## 注意事項

- **原材料品質決定還原度**：全集 + 史料 + 評點 > 僅口述標籤
- 建議優先提供：
  1. 核心代表作（高頻引句）
  2. 人生轉折期文本（貶謫、起復、爭論）
  3. 政論/書信（價值判斷與語氣）
  4. 後世評點（幫助界定風格邊界）
- 這是文風建模工具，不是歷史真實性的最終裁判
- 名家鏡像會隨著新材料持續演化

---

## 致敬 & 引用

本專案結構參考並受以下開源專案啟發：
- **[yourself-skill](https://github.com/notdog1998/yourself-skill)** — 雙層蒸餾結構（Memory + Persona）
- **[同事.skill](https://github.com/titanwings/colleague-skill)** — 人物蒸餾技能化思路
- **[前任.skill](https://github.com/therealXiaomanChu/ex-partner-skill)** — 場景遷移與互動演化機制

名家蒸餾器.skill 在此基礎上把對象擴展到古典文人，強調史料可追溯與辭章一致性。

本專案遵循 [AgentSkills](https://agentskills.io) 開放標準，相容 Claude Code。

---

### 寫在最後

> "文脈不死，只待重寫。"

這個 Skill 不會替代歷史上的名家，但能把其風骨、邏輯與語言結構轉成可對話的數位形態。

你可以校正它、迭代它、推翻它，再讓它在下一版變得更像那位你心中的名家。

**與其模仿風格，不如蒸餾風骨。**

**歡迎加入數位文脈。**

MIT License © Contributors
