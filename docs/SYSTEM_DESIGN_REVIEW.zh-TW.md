# 系統設計審視：Master Persona Builder

## 1. 範圍與背景
本文件僅審視 `apps/master-persona-builder`。

主要執行模型：
- 靜態前端（`index.html`, `styles.css`, `app.js`）
- Serverless Python API（`api/validate.py`, `api/generate.py`, `api/health.py`）
- 共用正規化/驗證/渲染工具（`api/_lib.py`）
- 可選的 repo 工具鏈執行（`tools/*.py`），失敗時退回 template 模式

## 2. 高階架構
```mermaid
flowchart TD
  U[使用者瀏覽器] --> F[靜態前端\nindex.html + app.js]
  F --> V[/api/validate]
  F --> G[/api/generate]

  V --> L[_lib.py\nnormalize + validate + auth + CORS]
  G --> L

  G --> D{是否找到 repo_root\n且 tools 可執行?}
  D -- 是 --> T[執行工具鏈\nliterature_parser/meter/biography/citation\n再做 skill_writer build+combine]
  D -- 否或失敗 --> R[Template 渲染\nrender_skill_md + render_wiki_md]

  T --> O[files + tool_plan + warnings]
  R --> O
  O --> F
```

## 3. 請求/回應契約
請求（正規化後）：
- `meta`：識別與生成中繼資料（`slug`, `name`, `description`, `version`, `language`, `target_platforms`）
- `master`：人格主體基礎資訊（`display_name`, `dynasty` 等）
- `memory`：記憶維度（list）
- `persona`：風格與行為約束（list）
- `commands`：觸發命令模板
- `source_materials[]`：`{category, title, content}` 陣列

回應：
- `ok`, `warnings`
- `files`：`SKILL.md`, `wiki.md`，以及可選的 `self.md/persona.md/meta.json/sources.json`
- `tool_plan`：`mode`, `routes`, `executions[]`

## 4. 核心架構取捨

### 4.1 直接前端 -> Python API
選這種設計的原因：
- 部件最少，部署維運成本低
- 不需要額外 gateway 層
- 最快達成 deterministic 的表單到文件生成

代價：
- Python API 要自己處理全部邊界（CORS、Auth、Validation、限流/限量）
- 流量與功能變複雜時，拆層成本增加

替代方案：
- Node gateway + Python workers
- 優點：協定轉換、統一限流更彈性
- 缺點：維運成本和延遲上升

### 4.2 Serverless 無狀態執行
選這種設計的原因：
- 適合互動式突發流量
- 無需常駐基礎設施
- 低中量級成本效率高

代價：
- 冷啟動與子程序限制
- `/tmp` 容量與執行時間限制不利於重資料抽取

替代方案：
- 常駐容器 API
- 優點：長任務與快取控制更好
- 缺點：固定成本與維運負擔更高

### 4.3 repo-tools 模式 + template fallback
選這種設計的原因：
- 工具鏈可用時保留高擬真輸出
- 受限環境仍能回傳可用結果
- 端到端可用性更高

代價：
- 雙路徑行為可能掩蓋工具鏈退化（若 fallback 太常啟動）

替代方案：
- 工具鏈不可用就硬失敗
- 優點：正確性訊號更強
- 缺點：可用性與使用體驗下降

### 4.4 以 subprocess 作工具邊界
選這種設計的原因：
- 可重用既有 CLI 工具，不需大改
- 行程隔離提升容錯

代價：
- 檔案序列化到 `/tmp` 有額外開銷
- 錯誤傳遞與觀測較 in-process 複雜

替代方案：
- 把工具改為 Python module 直接呼叫
- 優點：速度與型別介面更乾淨
- 缺點：重構成本高、耦合加深

## 5. 資料結構選型：為什麼這樣設計

### 5.1 為什麼用巢狀物件 + list（`meta/master/memory/persona/commands/source_materials`）
原因：
- 對應領域語義清楚（身份、記憶、風格分層）
- key 穩定，便於 deterministic 模板生成
- 可向後相容擴充（新增 optional keys）

替代 A：扁平大物件（100+ 欄）
- 優點：初看直接
- 缺點：命名衝突高、演進困難、邊界不清

替代 B：每版強型別 schema（`v1/v2/...`）
- 優點：版本相容控制嚴格
- 缺點：UI/範例遷移成本高

### 5.2 為什麼 memory/persona 採 list
原因：
- 順序即語義（優先序、語氣節奏）
- UI 輸入簡單（每行一筆）
- 模板輸出為條列時最自然

替代 A：set/map 形式（例如 `{"rule": true}`）
- 優點：天然去重
- 缺點：失去順序與細膩表達

替代 B：rich object（`{text, weight, source}`）
- 優點：可做加權與溯源
- 缺點：使用門檻與驗證複雜度大增

### 5.3 為什麼 `source_materials` 是 record 陣列
原因：
- 支援同分類多來源
- 保留使用者輸入順序
- 依 `category` 路由工具很直接

替代 A：分類 map（`{works: [...], biography: [...]}`）
- 優點：分類查找快
- 缺點：不易保留跨分類原始序列，UI 映射變複雜

替代 B：關聯式資料庫正規化
- 優點：查詢與分析能力強
- 缺點：對同步 serverless 生成流程偏重

### 5.4 為什麼 `tool_plan.executions[]` 用 append-only 紀錄
原因：
- 可稽核、可讀
- 前端表格直接渲染
- 容易擴欄位（`status`, `exit_code`, `stderr`, `duration_ms`）

替代 A：DAG 執行圖
- 優點：依賴關係表達更完整
- 缺點：對目前流程過重，前端呈現成本高

替代 B：純文字 log
- 優點：實作最簡
- 缺點：機器可讀性差、UX 弱

### 5.5 為什麼 `files` 用 keyed JSON text
原因：
- 前端可即時顯示/複製/下載，無需二次請求
- template 與 repo-tools 模式可共用

替代 A：zip 二進位回應
- 優點：多檔封包效率高
- 缺點：前端預覽與處理變複雜

替代 B：物件儲存 URL
- 優點：適合大檔與快取
- 缺點：要簽名 URL 與生命週期管理

## 6. 目前風險與緩解
1. 雙模式漂移（repo-tools vs template）
- 緩解：回傳 `tool_plan.mode` 與 warnings，並維持雙路徑回歸測試。

2. 子程序穩定性
- 緩解：timeout/長度上限、輸出截斷、逐步狀態紀錄。

3. 輸入濫用風險
- 緩解：內容大小/筆數上限、Origin 限制、可選 API key。

4. 前後端 schema 漂移
- 緩解：維護 `shared/schema.json` 與 normalized payload 整合測試。

## 7. Deep-dive 問答準備（繁中）
1. 為什麼不強制只走單一路徑？
- 因為目前優先可用性。serverless 若無法跑完整工具鏈，fallback 仍可交付主要輸出。

2. 為什麼不用加權結構而用 list？
- 現階段目標是 deterministic 生成，不是 ranking/訓練。list 最低摩擦且保留作者排序意圖。

3. 為什麼不用資料庫？
- 現行是 request-scoped 生成，沒有強交易/持久化依賴，用文字檔回傳更輕量。

4. 放大流量時第一個瓶頸是什麼？
- serverless 下的 subprocess 執行時間/記憶體限制，其次是來源文本總量導致解析延遲。

5. 要升級到企業級怎麼走？
- 加入 async job queue、持久化 artifact storage、嚴格版本化契約、完整 observability。

6. 為什麼要把執行紀錄回傳前端？
- 增加可解釋性與除錯效率，尤其多分類來源對應不同工具時能快速定位問題。

7. 如何避免本機路徑洩漏？
- 回傳前會做工具名稱正規化（轉 repo 相對路徑或檔名，避免絕對路徑外洩）。

## 8. 下一步設計檢查點
- 新增 API 契約版本欄位（`meta.contract_version`）
- 補強雙路徑 golden tests（repo-tools + template fallback）
- 對大語料加入可選 async 模式
- 為 `tool_plan` 每步驟增加穩定 audit id
