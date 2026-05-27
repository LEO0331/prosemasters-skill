const { test, expect } = require("@playwright/test");

async function fillFields(page, values) {
  for (const [selector, value] of Object.entries(values)) {
    await page.locator(selector).fill(value);
  }
}

test.describe("master-persona-builder", () => {
  test("generates SKILL.md and wiki.md through the real browser flow", async ({ page }) => {
    await page.goto("/");

    await fillFields(page, {
      "#slug": "e2e-master",
      "#name": "E2E Master Persona",
      "#description": "End-to-end generated literary persona",
      "#display_name": "E2E Master",
      "#dynasty": "Test Dynasty",
      "#literary_school": "Test School",
      "#historical_context": "A deterministic test context for browser automation.",
      "#core_philosophy": "Clarity before ornament.",
      "#core_values": "Precision\nDiscipline",
      "#timeline_milestones": "1200, born\n1230, major work",
      "#l1_hard_rules": "No slang",
      "#l3_expression_style": "Balanced cadence",
      "#decision_ladder": "Observe\nJudge\nRespond",
      "#voice_anchors": "Measured, direct, grounded",
      ".src-title": "Representative work",
      ".src-content": "The clear sentence should hold before the ornate one.",
    });

    await page.locator("#generate_skill_btn").click();
    await expect(page.locator("#status")).toContainText("Generation completed");
    await expect(page.locator("#output_out")).toHaveValue(/name: e2e-master/);
    await expect(page.locator("#output_out")).toHaveValue(/# E2E Master/);
    await expect(page.locator("#tool_plan_summary")).toContainText("\"mode\"");
    await expect(page.locator("#exec_table tbody tr").first()).toBeVisible();

    await page.locator("#generate_wiki_btn").click();
    await expect(page.locator("#status")).toContainText("Generation completed");
    await expect(page.locator("#output_out")).toHaveValue(/# E2E Master \(e2e-master\)/);
    await expect(page.locator("#output_title")).toHaveText("wiki.md");
  });

  test("surfaces backend validation errors to the user", async ({ page }) => {
    await page.goto("/");

    await page.locator("#json_input").fill(
      JSON.stringify(
        {
          meta: {
            slug: "Bad Slug",
            name: "Broken Persona",
            description: "invalid slug should fail",
          },
          master: {
            display_name: "Broken Persona",
          },
        },
        null,
        2
      )
    );

    await page.locator("#generate_skill_btn").click();
    await expect(page.locator("#status")).toContainText("Generate error");
    await expect(page.locator("#status")).toContainText("meta.slug must match");
  });
});
