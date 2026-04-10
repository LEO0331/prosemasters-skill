const $ = (id) => document.getElementById(id);

const I18N = {
  en: {
    page_title: "Master Persona Builder",
    lang_button: "繁中",
    eyebrow: "Digital Lineage Studio",
    hero_title: "Master Persona Builder",
    hero_subtitle: "Generate <code>SKILL.md</code> and <code>wiki.md</code> from form input or custom JSON.",
    section_core: "Core Fields",
    section_advanced: "Advanced Arrays (one item per line)",
    section_json: "Custom JSON",
    section_sources: "Source Materials Routing",
    section_output: "Generated Output",
    section_tool_preview: "Tool Routing Preview",
    desc_core: "Define the master identity and base metadata used by all generated outputs.",
    desc_advanced: "Each line becomes one structured item in memory/persona to improve fidelity.",
    desc_json: "Use JSON mode to import/export full payloads for reproducible generation.",
    desc_output: "Choose one target format to generate. Both use the same backend pipeline and output panel.",
    desc_tool_preview: "Shows planned extraction routes and real execution logs for each tool step.",
    sources_subtitle: "Categorize each source so backend can decide extraction tools automatically.",
    label_slug: "Slug",
    label_name: "Name",
    label_description: "Description",
    label_version: "Version",
    label_display_name: "Display Name",
    label_dynasty: "Dynasty",
    label_school: "Literary School",
    label_context: "Historical Context",
    label_philosophy: "Core Philosophy",
    label_core_values: "Core Values",
    label_timeline: "Timeline Milestones",
    label_l1_rules: "L1 Hard Rules",
    label_l3_style: "L3 Expression Style",
    label_decision: "Decision Ladder",
    label_voice: "Voice Anchors",
    label_api_key: "API Key (optional for protected API)",
    th_step: "Step",
    th_tool: "Tool",
    th_status: "Status",
    th_exit: "Exit",
    th_duration: "Duration (ms)",
    th_logs: "Logs",
    btn_from_form: "Load JSON from Form",
    btn_to_form: "Apply JSON to Form",
    btn_download_json: "Download JSON",
    btn_add_source: "Add Source",
    btn_generate_skill: "Generate SKILL.md",
    btn_generate_wiki: "Generate wiki.md",
    btn_copy_output: "Copy",
    btn_download_output: "Download",
    src_category: "Category",
    src_title: "Title",
    src_content: "Content",
    src_remove: "Remove",
    src_option_works: "Works",
    src_option_criticism: "Criticism",
    src_option_letters: "Letters",
    src_option_biography: "Biography",
    src_option_citation: "Citation",
    output_skill: "SKILL.md",
    output_wiki: "wiki.md",
    placeholder_slug: "han-yu",
    placeholder_name: "Han Yu",
    placeholder_description: "High-fidelity literary persona",
    placeholder_display_name: "Han Yu",
    placeholder_dynasty: "Middle Tang",
    placeholder_school: "Leader of Classical Prose Movement",
    placeholder_json: "Paste custom JSON here...",
    placeholder_api_key: "Set if MPB_API_KEY is enabled on server",
    placeholder_source_title: "source title",
    placeholder_source_content: "paste source text or csv lines",
    status_no_exec: "No execution records.",
    status_logs: "view logs",
    status_success: "success",
    status_failed: "failed",
    status_skipped: "skipped",
    status_unknown: "unknown",
    msg_generation_completed: "Generation completed",
    msg_generate_error: "Generate error",
    msg_loaded_json: "Loaded JSON from form",
    msg_applied_json: "Applied JSON to form",
    msg_json_parse_error: "JSON parse error",
  },
  "zh-Hant": {
    page_title: "名家人格生成器",
    lang_button: "EN",
    eyebrow: "數位文脈工坊",
    hero_title: "名家人格生成器",
    hero_subtitle: "以表單或自訂 JSON 生成 <code>SKILL.md</code> 與 <code>wiki.md</code>。",
    section_core: "核心欄位",
    section_advanced: "進階陣列（每行一筆）",
    section_json: "自訂 JSON",
    section_sources: "來源素材路由",
    section_output: "生成輸出",
    section_tool_preview: "工具路由預覽",
    desc_core: "定義名家身份與基礎元資料，所有輸出都會使用這些資訊。",
    desc_advanced: "每行視為一筆結構化資料，用於提升記憶與人格擬真度。",
    desc_json: "可匯入或匯出完整 JSON 載荷，方便重現與版本管理。",
    desc_output: "選擇要生成的格式。兩種格式共用同一條後端流程與輸出區。",
    desc_tool_preview: "顯示規劃路由與每個工具步驟的實際執行紀錄。",
    sources_subtitle: "為每份來源分類，讓後端自動判定抽取工具。",
    label_slug: "代號 Slug",
    label_name: "名稱",
    label_description: "描述",
    label_version: "版本",
    label_display_name: "顯示名稱",
    label_dynasty: "朝代",
    label_school: "文學流派",
    label_context: "歷史脈絡",
    label_philosophy: "精神核心",
    label_core_values: "核心價值",
    label_timeline: "生平節點",
    label_l1_rules: "L1 硬性規則",
    label_l3_style: "L3 表達風格",
    label_decision: "判斷階梯",
    label_voice: "語氣錨點",
    label_api_key: "API 金鑰（若伺服器啟用保護）",
    th_step: "步驟",
    th_tool: "工具",
    th_status: "狀態",
    th_exit: "代碼",
    th_duration: "耗時（毫秒）",
    th_logs: "日誌",
    btn_from_form: "由表單載入 JSON",
    btn_to_form: "將 JSON 套用到表單",
    btn_download_json: "下載 JSON",
    btn_add_source: "新增來源",
    btn_generate_skill: "生成 SKILL.md",
    btn_generate_wiki: "生成 wiki.md",
    btn_copy_output: "複製",
    btn_download_output: "下載",
    src_category: "分類",
    src_title: "標題",
    src_content: "內容",
    src_remove: "移除",
    src_option_works: "作品",
    src_option_criticism: "評點",
    src_option_letters: "書信",
    src_option_biography: "傳記",
    src_option_citation: "引文",
    output_skill: "SKILL.md",
    output_wiki: "wiki.md",
    placeholder_slug: "han-yu",
    placeholder_name: "韓愈",
    placeholder_description: "高擬真文學人格",
    placeholder_display_name: "韓愈",
    placeholder_dynasty: "中唐",
    placeholder_school: "古文運動領袖",
    placeholder_json: "貼上自訂 JSON...",
    placeholder_api_key: "若伺服器啟用 MPB_API_KEY，請在此輸入",
    placeholder_source_title: "來源標題",
    placeholder_source_content: "貼上來源文本或 CSV 內容",
    status_no_exec: "目前沒有執行紀錄。",
    status_logs: "展開日誌",
    status_success: "成功",
    status_failed: "失敗",
    status_skipped: "略過",
    status_unknown: "未知",
    msg_generation_completed: "生成完成",
    msg_generate_error: "生成錯誤",
    msg_loaded_json: "已由表單載入 JSON",
    msg_applied_json: "已將 JSON 套用到表單",
    msg_json_parse_error: "JSON 解析錯誤",
  },
};

const fields = {
  slug: $("slug"),
  name: $("name"),
  description: $("description"),
  version: $("version"),
  display_name: $("display_name"),
  dynasty: $("dynasty"),
  literary_school: $("literary_school"),
  historical_context: $("historical_context"),
  core_philosophy: $("core_philosophy"),
  core_values: $("core_values"),
  timeline_milestones: $("timeline_milestones"),
  l1_hard_rules: $("l1_hard_rules"),
  l3_expression_style: $("l3_expression_style"),
  decision_ladder: $("decision_ladder"),
  voice_anchors: $("voice_anchors"),
};

const status = $("status");
const jsonInput = $("json_input");
const outputOut = $("output_out");
const outputTitle = $("output_title");
const toolPlanOut = $("tool_plan_summary");
const sourcesList = $("sources_list");
const execTableBody = $("exec_table").querySelector("tbody");
const apiKeyInput = $("api_key");
const langSwitchBtn = $("lang_switch");

const API_KEY_STORAGE_KEY = "mpb_api_key";
const LANG_STORAGE_KEY = "mpb_lang";
let currentLang = "en";
let lastGenerated = null;
let currentOutputType = "skill";

function detectInitialLang() {
  const stored = window.localStorage.getItem(LANG_STORAGE_KEY);
  if (stored && I18N[stored]) return stored;
  const browser = (navigator.language || "").toLowerCase();
  return browser.startsWith("zh") ? "zh-Hant" : "en";
}

function t(key) {
  const langPack = I18N[currentLang] || I18N.en;
  return langPack[key] ?? I18N.en[key] ?? key;
}

function lines(v) {
  return v.split("\n").map((x) => x.trim()).filter(Boolean);
}

function setStatus(msg, obj) {
  status.textContent = obj ? `${msg}\n${JSON.stringify(obj, null, 2)}` : msg;
}

function getApiKey() {
  const fromInput = (apiKeyInput?.value || "").trim();
  if (fromInput) return fromInput;
  return (window.localStorage.getItem(API_KEY_STORAGE_KEY) || "").trim();
}

function persistApiKey() {
  if (!apiKeyInput) return;
  const value = (apiKeyInput.value || "").trim();
  if (value) {
    window.localStorage.setItem(API_KEY_STORAGE_KEY, value);
  } else {
    window.localStorage.removeItem(API_KEY_STORAGE_KEY);
  }
}

function escapeHtml(v) {
  return String(v ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}

function formatRowStatus(statusText) {
  const normalized = String(statusText || "unknown").toLowerCase();
  if (normalized === "success") return t("status_success");
  if (normalized === "failed") return t("status_failed");
  if (normalized === "skipped") return t("status_skipped");
  return t("status_unknown");
}

function renderExecutionsTable(toolPlan) {
  execTableBody.innerHTML = "";
  const executions = (toolPlan && toolPlan.executions) || [];
  if (!executions.length) {
    const tr = document.createElement("tr");
    tr.innerHTML = `<td colspan="6">${escapeHtml(t("status_no_exec"))}</td>`;
    execTableBody.appendChild(tr);
    return;
  }

  for (const rec of executions) {
    const tr = document.createElement("tr");
    const rowStatus = rec.status || "unknown";
    const statusClass =
      rowStatus === "success"
        ? "status-success"
        : rowStatus === "failed"
          ? "status-failed"
          : "status-skipped";

    const stderr = (rec.stderr || "").trim();
    const stdout = (rec.stdout || "").trim();
    const reason = rec.reason || "";
    const logs = [stderr ? `stderr:\n${stderr}` : "", stdout ? `stdout:\n${stdout}` : "", reason ? `reason:\n${reason}` : ""]
      .filter(Boolean)
      .join("\n\n");

    const logsCell = logs
      ? `<details><summary>${escapeHtml(t("status_logs"))}</summary><pre class="log-block">${escapeHtml(logs)}</pre></details>`
      : "-";

    tr.innerHTML = `
      <td>${escapeHtml(rec.step || "-")}</td>
      <td>${escapeHtml(rec.tool || "-")}</td>
      <td><span class="status-pill ${statusClass}">${escapeHtml(formatRowStatus(rowStatus))}</span></td>
      <td>${escapeHtml(rec.exit_code ?? "-")}</td>
      <td>${escapeHtml(rec.duration_ms ?? "-")}</td>
      <td>${logsCell}</td>
    `;
    execTableBody.appendChild(tr);
  }
}

function sourceRow(item = { category: "works", title: "", content: "" }) {
  const wrap = document.createElement("div");
  wrap.className = "source-item";
  wrap.innerHTML = `
    <div class="grid">
      <label>${escapeHtml(t("src_category"))}
        <select class="src-category">
          <option value="works">${escapeHtml(t("src_option_works"))}</option>
          <option value="criticism">${escapeHtml(t("src_option_criticism"))}</option>
          <option value="letters">${escapeHtml(t("src_option_letters"))}</option>
          <option value="biography">${escapeHtml(t("src_option_biography"))}</option>
          <option value="citation">${escapeHtml(t("src_option_citation"))}</option>
        </select>
      </label>
      <label>${escapeHtml(t("src_title"))}<input class="src-title" placeholder="${escapeHtml(t("placeholder_source_title"))}" /></label>
    </div>
    <label>${escapeHtml(t("src_content"))}<textarea class="src-content" rows="4" placeholder="${escapeHtml(t("placeholder_source_content"))}"></textarea></label>
    <div class="row"><button class="remove-source" type="button">${escapeHtml(t("src_remove"))}</button></div>
  `;
  wrap.querySelector(".src-category").value = item.category || "works";
  wrap.querySelector(".src-title").value = item.title || "";
  wrap.querySelector(".src-content").value = item.content || "";
  wrap.querySelector(".remove-source").onclick = () => wrap.remove();
  return wrap;
}

function getSourceMaterials() {
  return [...sourcesList.querySelectorAll(".source-item")]
    .map((node) => ({
      category: node.querySelector(".src-category").value,
      title: node.querySelector(".src-title").value.trim(),
      content: node.querySelector(".src-content").value.trim(),
    }))
    .filter((x) => x.content);
}

function setSourceMaterials(items) {
  sourcesList.innerHTML = "";
  (items || []).forEach((item) => sourcesList.appendChild(sourceRow(item)));
  if (!sourcesList.children.length) sourcesList.appendChild(sourceRow());
}

function toPayloadFromForm() {
  return {
    meta: {
      slug: fields.slug.value.trim().toLowerCase(),
      name: fields.name.value.trim(),
      description: fields.description.value.trim(),
      version: fields.version.value.trim() || "1.0.0",
      language: currentLang === "zh-Hant" ? "zh-TW" : "en",
      target_platforms: ["claude", "codex"],
    },
    master: {
      display_name: fields.display_name.value.trim(),
      dynasty: fields.dynasty.value.trim(),
      titles: [],
      historical_context: fields.historical_context.value.trim(),
      literary_school: fields.literary_school.value.trim(),
      core_philosophy: fields.core_philosophy.value.trim(),
    },
    memory: {
      core_values: lines(fields.core_values.value),
      intellectual_axes: [],
      worldview_tensions: [],
      preferred_themes: [],
      emotional_signature: [],
      timeline_milestones: lines(fields.timeline_milestones.value),
      geography_path: [],
      relationships: [],
      voice_anchors: lines(fields.voice_anchors.value),
      anachronism_policy: [],
      citation_ids: [],
    },
    persona: {
      l1_hard_rules: lines(fields.l1_hard_rules.value),
      l2_identity_role: [],
      l3_expression_style: lines(fields.l3_expression_style.value),
      lexicon_preferences: [],
      rhythm_structure: [],
      l4_judgment_logic: [],
      decision_ladder: lines(fields.decision_ladder.value),
      l5_social_conduct: [],
      audience_tone: [],
      anti_patterns: [],
      rewrite_strategies: [],
    },
    commands: {
      trigger: "/distill-master",
      update: "/update-master {slug}",
      list: "/list-masters",
      delete: "/delete-master {slug}",
    },
    source_materials: getSourceMaterials(),
  };
}

function applyPayloadToForm(payload) {
  const m = payload.meta || {};
  const master = payload.master || {};
  const memory = payload.memory || {};
  const persona = payload.persona || {};

  fields.slug.value = m.slug || "";
  fields.name.value = m.name || "";
  fields.description.value = m.description || "";
  fields.version.value = m.version || "1.0.0";
  fields.display_name.value = master.display_name || "";
  fields.dynasty.value = master.dynasty || "";
  fields.literary_school.value = master.literary_school || "";
  fields.historical_context.value = master.historical_context || "";
  fields.core_philosophy.value = master.core_philosophy || "";

  fields.core_values.value = (memory.core_values || []).join("\n");
  fields.timeline_milestones.value = (memory.timeline_milestones || []).join("\n");
  fields.voice_anchors.value = (memory.voice_anchors || []).join("\n");

  fields.l1_hard_rules.value = (persona.l1_hard_rules || []).join("\n");
  fields.l3_expression_style.value = (persona.l3_expression_style || []).join("\n");
  fields.decision_ladder.value = (persona.decision_ladder || []).join("\n");
  setSourceMaterials(payload.source_materials || []);
}

async function postJson(path, payload) {
  const headers = { "Content-Type": "application/json" };
  const apiKey = getApiKey();
  if (apiKey) headers["X-API-Key"] = apiKey;
  const r = await fetch(path, {
    method: "POST",
    headers,
    body: JSON.stringify(payload),
  });
  const contentType = (r.headers.get("content-type") || "").toLowerCase();
  const isJson = contentType.includes("application/json");
  const data = isJson ? await r.json() : { errors: [await r.text()] };
  if (!r.ok) throw new Error(data.errors ? data.errors.join("; ") : `HTTP ${r.status}`);
  return data;
}

function download(name, content) {
  const blob = new Blob([content], { type: "text/markdown;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = name;
  a.click();
  URL.revokeObjectURL(url);
}

function showOutput(kind) {
  currentOutputType = kind;
  if (!lastGenerated) {
    outputTitle.textContent = kind === "wiki" ? t("output_wiki") : t("output_skill");
    outputOut.value = "";
    return;
  }
  if (kind === "wiki") {
    outputTitle.textContent = t("output_wiki");
    outputOut.value = lastGenerated.files.wiki_md || "";
  } else {
    outputTitle.textContent = t("output_skill");
    outputOut.value = lastGenerated.files.skill_md || "";
  }
}

async function onGenerate(kind) {
  try {
    const payload = JSON.parse(jsonInput.value || "{}");
    const res = await postJson("/api/generate", payload);
    lastGenerated = res;
    toolPlanOut.textContent = JSON.stringify(
      {
        mode: res.tool_plan?.mode || "unknown",
        routes: (res.tool_plan?.routes || []).map((r) => ({
          category: r.category,
          title: r.title,
          tools: r.tools || [],
        })),
      },
      null,
      2
    );
    renderExecutionsTable(res.tool_plan || {});
    showOutput(kind);
    setStatus(t("msg_generation_completed"), { warnings: res.warnings || [] });
  } catch (e) {
    setStatus(`${t("msg_generate_error")}: ${e.message}`);
  }
}

function applyLanguage(lang) {
  currentLang = I18N[lang] ? lang : "en";
  window.localStorage.setItem(LANG_STORAGE_KEY, currentLang);
  document.documentElement.lang = currentLang === "zh-Hant" ? "zh-Hant" : "en";
  document.title = t("page_title");

  const textMap = {
    eyebrow: "eyebrow",
    hero_title: "hero_title",
    section_core: "section_core",
    section_advanced: "section_advanced",
    section_json: "section_json",
    section_sources: "section_sources",
    section_output: "section_output",
    section_tool_preview: "section_tool_preview",
    desc_core: "desc_core",
    desc_advanced: "desc_advanced",
    desc_json: "desc_json",
    desc_output: "desc_output",
    desc_tool_preview: "desc_tool_preview",
    sources_subtitle: "sources_subtitle",
    label_slug: "label_slug",
    label_name: "label_name",
    label_description: "label_description",
    label_version: "label_version",
    label_display_name: "label_display_name",
    label_dynasty: "label_dynasty",
    label_school: "label_school",
    label_context: "label_context",
    label_philosophy: "label_philosophy",
    label_core_values: "label_core_values",
    label_timeline: "label_timeline",
    label_l1_rules: "label_l1_rules",
    label_l3_style: "label_l3_style",
    label_decision: "label_decision",
    label_voice: "label_voice",
    label_api_key: "label_api_key",
    th_step: "th_step",
    th_tool: "th_tool",
    th_status: "th_status",
    th_exit: "th_exit",
    th_duration: "th_duration",
    th_logs: "th_logs",
    from_form: "btn_from_form",
    to_form: "btn_to_form",
    download_json: "btn_download_json",
    add_source: "btn_add_source",
    generate_skill_btn: "btn_generate_skill",
    generate_wiki_btn: "btn_generate_wiki",
    copy_output: "btn_copy_output",
    download_output: "btn_download_output",
  };

  Object.entries(textMap).forEach(([id, key]) => {
    const el = $(id);
    if (el) el.textContent = t(key);
  });

  const subtitle = $("hero_subtitle");
  if (subtitle) subtitle.innerHTML = t("hero_subtitle");
  if (langSwitchBtn) langSwitchBtn.textContent = t("lang_button");

  fields.slug.placeholder = t("placeholder_slug");
  fields.name.placeholder = t("placeholder_name");
  fields.description.placeholder = t("placeholder_description");
  fields.display_name.placeholder = t("placeholder_display_name");
  fields.dynasty.placeholder = t("placeholder_dynasty");
  fields.literary_school.placeholder = t("placeholder_school");
  jsonInput.placeholder = t("placeholder_json");
  apiKeyInput.placeholder = t("placeholder_api_key");

  const currentSources = getSourceMaterials();
  setSourceMaterials(currentSources);
  showOutput(currentOutputType);
}

$("from_form").onclick = () => {
  const payload = toPayloadFromForm();
  jsonInput.value = JSON.stringify(payload, null, 2);
  setStatus(t("msg_loaded_json"));
};

$("to_form").onclick = () => {
  try {
    const payload = JSON.parse(jsonInput.value || "{}");
    applyPayloadToForm(payload);
    setStatus(t("msg_applied_json"));
  } catch (e) {
    setStatus(`${t("msg_json_parse_error")}: ${e.message}`);
  }
};

$("download_json").onclick = () => download("master-persona.json", jsonInput.value || "{}");
$("generate_skill_btn").onclick = () => onGenerate("skill");
$("generate_wiki_btn").onclick = () => onGenerate("wiki");
$("copy_output").onclick = async () => navigator.clipboard.writeText(outputOut.value || "");
$("download_output").onclick = () => {
  const filename = currentOutputType === "wiki" ? "wiki.md" : "SKILL.md";
  download(filename, outputOut.value || "");
};
$("add_source").onclick = () => sourcesList.appendChild(sourceRow());

if (apiKeyInput) {
  apiKeyInput.value = window.localStorage.getItem(API_KEY_STORAGE_KEY) || "";
  apiKeyInput.addEventListener("change", persistApiKey);
  apiKeyInput.addEventListener("blur", persistApiKey);
}

if (langSwitchBtn) {
  langSwitchBtn.addEventListener("click", () => {
    applyLanguage(currentLang === "en" ? "zh-Hant" : "en");
  });
}

applyLanguage(detectInitialLang());
setSourceMaterials([{ category: "works", title: "", content: "" }]);
showOutput("skill");
