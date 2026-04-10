const $ = (id) => document.getElementById(id);

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
const skillOut = $("skill_out");
const wikiOut = $("wiki_out");
const toolPlanOut = $("tool_plan_summary");
const sourcesList = $("sources_list");
const execTableBody = $("exec_table").querySelector("tbody");

function lines(v) {
  return v.split("\n").map((x) => x.trim()).filter(Boolean);
}

function setStatus(msg, obj) {
  status.textContent = obj ? `${msg}\n${JSON.stringify(obj, null, 2)}` : msg;
}

function escapeHtml(v) {
  return String(v ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}

function renderExecutionsTable(toolPlan) {
  execTableBody.innerHTML = "";
  const executions = (toolPlan && toolPlan.executions) || [];
  if (!executions.length) {
    const tr = document.createElement("tr");
    tr.innerHTML = `<td colspan="6">No execution records.</td>`;
    execTableBody.appendChild(tr);
    return;
  }

  for (const rec of executions) {
    const tr = document.createElement("tr");
    const status = rec.status || "unknown";
    const statusClass =
      status === "success"
        ? "status-success"
        : status === "failed"
          ? "status-failed"
          : "status-skipped";

    const stderr = (rec.stderr || "").trim();
    const stdout = (rec.stdout || "").trim();
    const reason = rec.reason || "";
    const logs = [stderr ? `stderr:\n${stderr}` : "", stdout ? `stdout:\n${stdout}` : "", reason ? `reason:\n${reason}` : ""]
      .filter(Boolean)
      .join("\n\n");

    const logsCell = logs
      ? `<details><summary>view logs</summary><pre class="log-block">${escapeHtml(logs)}</pre></details>`
      : "-";

    tr.innerHTML = `
      <td>${escapeHtml(rec.step || "-")}</td>
      <td>${escapeHtml(rec.tool || "-")}</td>
      <td><span class="status-pill ${statusClass}">${escapeHtml(status)}</span></td>
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
      <label>Category
        <select class="src-category">
          <option value="works">works</option>
          <option value="criticism">criticism</option>
          <option value="letters">letters</option>
          <option value="biography">biography</option>
          <option value="citation">citation</option>
        </select>
      </label>
      <label>Title<input class="src-title" placeholder="source title" /></label>
    </div>
    <label>Content<textarea class="src-content" rows="4" placeholder="paste source text or csv lines"></textarea></label>
    <div class="row"><button class="remove-source">Remove</button></div>
  `;
  wrap.querySelector(".src-category").value = item.category || "works";
  wrap.querySelector(".src-title").value = item.title || "";
  wrap.querySelector(".src-content").value = item.content || "";
  wrap.querySelector(".remove-source").onclick = () => wrap.remove();
  return wrap;
}

function getSourceMaterials() {
  return [...sourcesList.querySelectorAll(".source-item")].map((node) => ({
    category: node.querySelector(".src-category").value,
    title: node.querySelector(".src-title").value.trim(),
    content: node.querySelector(".src-content").value.trim(),
  })).filter((x) => x.content);
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
      language: "zh-TW",
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
  const r = await fetch(path, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const data = await r.json();
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

async function onValidate() {
  try {
    const payload = JSON.parse(jsonInput.value || "{}");
    const res = await postJson("/api/validate", payload);
    setStatus(res.ok ? "Validation passed" : "Validation failed", res);
  } catch (e) {
    setStatus(`Validation error: ${e.message}`);
  }
}

async function onGenerate() {
  try {
    const payload = JSON.parse(jsonInput.value || "{}");
    const res = await postJson("/api/generate", payload);
    skillOut.value = res.files.skill_md || "";
    wikiOut.value = res.files.wiki_md || "";
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
    setStatus("Generation completed", { warnings: res.warnings || [] });
  } catch (e) {
    setStatus(`Generate error: ${e.message}`);
  }
}

$("from_form").onclick = () => {
  const payload = toPayloadFromForm();
  jsonInput.value = JSON.stringify(payload, null, 2);
  setStatus("Loaded JSON from form");
};

$("to_form").onclick = () => {
  try {
    const payload = JSON.parse(jsonInput.value || "{}");
    applyPayloadToForm(payload);
    setStatus("Applied JSON to form");
  } catch (e) {
    setStatus(`JSON parse error: ${e.message}`);
  }
};

$("download_json").onclick = () => download("master-persona.json", jsonInput.value || "{}");
$("validate_btn").onclick = onValidate;
$("generate_btn").onclick = onGenerate;
$("copy_skill").onclick = async () => navigator.clipboard.writeText(skillOut.value || "");
$("copy_wiki").onclick = async () => navigator.clipboard.writeText(wikiOut.value || "");
$("download_skill").onclick = () => download("SKILL.md", skillOut.value || "");
$("download_wiki").onclick = () => download("wiki.md", wikiOut.value || "");
$("add_source").onclick = () => sourcesList.appendChild(sourceRow());

fetch("/shared/examples/master.example.json")
  .then((r) => r.ok ? r.json() : null)
  .then((example) => {
    if (!example) return;
    jsonInput.value = JSON.stringify(example, null, 2);
    applyPayloadToForm(example);
    toolPlanOut.textContent = "";
    renderExecutionsTable({});
  })
  .catch(() => null);
