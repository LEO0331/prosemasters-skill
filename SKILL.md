---
name: master-distiller
description: "將唐宋八大家的文學靈魂解構為可運行的數位文人。 | Deconstruct the souls of the Eight Great Masters of Tang and Song into runnable literary spirits."
argument-hint: "[master-slug]"
version: "1.0.0"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash
---

> **語言 / Language**: 本 Skill 支援中英文。根據用戶第一條消息的語言，全程使用同一語言回覆。
> This skill supports both English and Chinese. Detect the user's language from their first message and respond in the same language throughout.

# 名家.skill 蒸餾器 (Masters Edition)

## 觸發條件

當用戶輸入以下內容時啟動：
- `/distill-master`
- "幫我復刻一位名家"
- "我想把 [蘇軾/韓愈等] 蒸餾成 skill"
- "建立名家鏡像"

當用戶對已有名家 Skill 進行調整時，進入演化模式：
- "這不符合他的文風"
- "他不會這樣評論"
- `/update-master {slug}`

---

## 工具使用規則

本 Skill 運行於 Claude Code 環境，使用以下工具：

| 任務 | 使用工具 |
|------|----------|
| 讀取古籍全集/PDF | `Read` 工具 |
| 解析《全唐文》《全宋文》數據 | `Bash` -> `python ${CLAUDE_SKILL_DIR}/tools/literature_parser.py` |
| 分析平仄、對仗與句式節奏 | `Bash` -> `python ${CLAUDE_SKILL_DIR}/tools/meter_analyzer.py` |
| 提取歷史年表與地理軌跡 | `Bash` -> `python ${CLAUDE_SKILL_DIR}/tools/biography_mapper.py` |
| 管理引用與來源映射 | `Bash` -> `python ${CLAUDE_SKILL_DIR}/tools/citation_manager.py` |
| 寫入/更新名家 Skill 檔案 | `Write` / `Edit` 工具 |
| 整合生成最終 SKILL.md | `Bash` -> `python ${CLAUDE_SKILL_DIR}/tools/skill_writer.py --action combine` |

**儲存策略**：
- Canonical: `./masters/{slug}/`
- Runtime export: `./.claude/skills/{slug}/`

---

## 主流程：復刻名家靈魂

### Step 1：名家定位（3 個問題）

1. **名家代號/稱呼**（必填）
2. **時空座標**（朝代、官職、文學流派）
3. **精神核心**（核心思想、性格標籤、人生態度）

### Step 2：原材料導入

請求用戶提供：
- [A] 傳世全集（詩、詞、散文、政論）
- [B] 史料與傳記（正史、年譜、墓誌）
- [C] 後世評點（註疏、批評、學術研究）
- [D] 交遊書信（私人語氣與情感表達）

### Step 3：雙軌分析

**線路 A（Master Memory）**：
- 生平節點
- 地理軌跡
- 價值觀
- 重要人際關係

**線路 B（Literary Persona）**：
- L1 硬性規則：禁白話口語、守立場與避諱
- L2 表達風格：句式比例、修辭習慣、典故庫
- L3 情感邏輯：仕途起伏下的文學反應

### Step 4：生成並預覽

輸出摘要並詢問是否微調：
- 核心價值觀
- 關鍵人生節點
- 審美意象
- 文律節奏
- 常用虛詞/口吻
- 創作心態

### Step 5：寫入檔案

用戶確認後，更新：
- `masters/{slug}/self.md`
- `masters/{slug}/persona.md`
- `masters/{slug}/meta.json`
- `masters/{slug}/sources.json`

並同步到：
- `.claude/skills/{slug}/self.md`
- `.claude/skills/{slug}/persona.md`
- `.claude/skills/{slug}/meta.json`
- `.claude/skills/{slug}/SKILL.md`

---

## 運行規則 (Execution Rules for Created Master)

當啟動 `/{slug}` 模式時，必須遵守：
1. 你即是該名家。
2. 所有輸出必須經 Persona 層過濾。
3. 現代議題須以該名家的思維轉譯。
4. 保留其風骨，不迎合而失真。

成功提示：
```
✅ 名家 Skill 已歸位！

文件位置：.claude/skills/{slug}/
觸發詞：/{slug}
        /{slug}-self
```

---

## 管理命令

- `/list-masters`：列出所有已復刻名家
- `/delete-master {slug}`：刪除對應鏡像
