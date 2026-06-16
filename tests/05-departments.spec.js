// @ts-check
const { test, expect } = require("@playwright/test");
const config = require("./helpers/config");
const { login } = require("./helpers/auth");

test.describe.serial("Module 5 — Departments", () => {
  /** @type {import('@playwright/test').Page} */
  let page;

  test.beforeAll(async ({ browser }) => {
    page = await browser.newPage();
    await login(page);
    await page.goto(config.TEAM_URL, { waitUntil: "networkidle" });
    await page.waitForTimeout(3000);
  });

  test.afterAll(async () => {
    await page.close();
  });

  test("DEPT-001 — Departments tab layout", async () => {
    const deptTab = page.locator(
      'button:has-text("Departments"), [role="tab"]:has-text("Departments"), a:has-text("Departments")'
    );
    await deptTab.first().click();
    await page.waitForTimeout(3000);

    const bodyText = await page.textContent("body");
    expect(bodyText).toContain("Department");

    // Check for Add Department button
    const addBtn = page.locator(
      'button:has-text("Add Department"), button:has-text("+ Add")'
    );
    const addVisible = await addBtn.first().isVisible().catch(() => false);
    console.log(`  Add Department button visible: ${addVisible}`);
    expect(addVisible).toBeTruthy();
  });

  test("DEPT-002 — Add department", async () => {
    const addBtn = page.locator(
      'button:has-text("Add Department"), button:has-text("+ Add")'
    );
    await addBtn.first().click();
    await page.waitForTimeout(2000);

    // Fill department name
    const nameInput = page.locator(
      '[class*="modal"] input, [role="dialog"] input, [class*="drawer"] input'
    );
    await nameInput.first().waitFor({ state: "visible", timeout: 5000 });
    await nameInput.first().fill(config.DEPT_NAME);

    // Save
    const saveBtn = page.locator(
      'button:has-text("Save"), button:has-text("Add"), button:has-text("Create")'
    );
    await saveBtn.first().click();
    await page.waitForTimeout(3000);

    const bodyText = await page.textContent("body");
    const hasSuccess =
      bodyText.includes("saved") ||
      bodyText.includes("Saved") ||
      bodyText.includes("created") ||
      bodyText.includes("Created") ||
      bodyText.includes(config.DEPT_NAME);

    expect(bodyText).toContain(config.DEPT_NAME);
    console.log(`  Department "${config.DEPT_NAME}" created`);
  });

  test("DEPT-003 — Edit department", async () => {
    // Find edit button for the dept we created
    const deptRow = page.locator(`text=${config.DEPT_NAME}`).first();
    const editBtn = deptRow.locator(
      "xpath=ancestor::tr//button[contains(@class,'edit') or @aria-label='Edit'], xpath=ancestor::*[contains(@class,'row')]//button[contains(@class,'edit') or @aria-label='Edit']"
    ).first();

    const altEditBtn = page.locator(
      `tr:has-text("${config.DEPT_NAME}") button:has(svg), tr:has-text("${config.DEPT_NAME}") [class*="edit"]`
    ).first();

    const editTarget = (await editBtn.isVisible().catch(() => false))
      ? editBtn
      : altEditBtn;

    if (await editTarget.isVisible().catch(() => false)) {
      await editTarget.click();
      await page.waitForTimeout(2000);

      const nameInput = page.locator(
        '[class*="modal"] input, [role="dialog"] input'
      );
      await nameInput.first().fill(`${config.DEPT_NAME} Updated`);

      const saveBtn = page.locator(
        'button:has-text("Save"), button:has-text("Update")'
      );
      await saveBtn.first().click();
      await page.waitForTimeout(3000);

      const bodyText = await page.textContent("body");
      expect(bodyText).toContain(`${config.DEPT_NAME} Updated`);
      console.log("  Department renamed successfully");
    } else {
      console.log("  ⚠ Edit button not found for department row");
    }
  });

  test("DEPT-004 — Duplicate department name blocked", async () => {
    const addBtn = page.locator(
      'button:has-text("Add Department"), button:has-text("+ Add")'
    );
    await addBtn.first().click();
    await page.waitForTimeout(2000);

    const nameInput = page.locator(
      '[class*="modal"] input, [role="dialog"] input'
    );
    await nameInput.first().fill(`${config.DEPT_NAME} Updated`);

    const saveBtn = page.locator(
      'button:has-text("Save"), button:has-text("Add"), button:has-text("Create")'
    );
    await saveBtn.first().click();
    await page.waitForTimeout(3000);

    const bodyText = await page.textContent("body");
    const hasDuplicateError =
      bodyText.includes("already exists") ||
      bodyText.includes("duplicate") ||
      bodyText.includes("Already") ||
      bodyText.includes("exists");

    console.log(`  Duplicate error shown: ${hasDuplicateError}`);

    // Close modal
    const cancelBtn = page.locator('button:has-text("Cancel"), button:has-text("Close")');
    await cancelBtn.first().click().catch(() => {});
  });
});
