// @ts-check
const { test, expect } = require("@playwright/test");
const config = require("./helpers/config");
const { login } = require("./helpers/auth");

test.describe.serial("Module 9 — Cleanup", () => {
  /** @type {import('@playwright/test').Page} */
  let page;

  test.beforeAll(async ({ browser }) => {
    page = await browser.newPage();
    await login(page);
  });

  test.afterAll(async () => {
    await page.close();
  });

  test("CLEANUP-001 — Revert test artifacts", async () => {
    console.log("=== CLEANUP START ===");

    // 1. Revoke pending invites
    await page.goto(config.TEAM_URL, { waitUntil: "networkidle" });
    await page.waitForTimeout(2000);

    const pendingTab = page.locator(
      'button:has-text("Pending"), [role="tab"]:has-text("Pending")'
    );
    await pendingTab.first().click();
    await page.waitForTimeout(3000);

    // Revoke all qa-* invites
    let revoked = 0;
    for (let attempt = 0; attempt < 10; attempt++) {
      const qaInvite = page.locator('text=/qa-/').first();
      if (!(await qaInvite.isVisible().catch(() => false))) break;

      const revokeBtn = page.locator('button:has-text("Revoke")').first();
      if (!(await revokeBtn.isVisible().catch(() => false))) break;

      await revokeBtn.click();
      await page.waitForTimeout(1000);

      // Handle confirmation
      page.on("dialog", async (dialog) => await dialog.accept());
      const confirmBtn = page.locator(
        'button:has-text("Confirm"), button:has-text("Revoke"), button:has-text("Yes")'
      );
      if (await confirmBtn.first().isVisible().catch(() => false)) {
        await confirmBtn.first().click();
      }
      await page.waitForTimeout(2000);
      revoked++;
    }
    console.log(`  Revoked ${revoked} pending invites`);

    // 2. Delete custom roles
    await page.goto(config.ROLES_URL, { waitUntil: "networkidle" });
    await page.waitForTimeout(2000);

    const rolesToDelete = [config.CUSTOM_ROLE, config.CLONE_ROLE];
    let rolesDeleted = 0;

    for (const roleName of rolesToDelete) {
      const roleEl = page.locator(`text="${roleName}"`).first();
      if (await roleEl.isVisible().catch(() => false)) {
        const card = roleEl.locator(
          "xpath=ancestor::*[contains(@class,'card') or contains(@class,'Card')]"
        ).first();
        const deleteBtn = card.locator(
          'button:has-text("Delete"), [aria-label*="elete"]'
        ).first();

        if (await deleteBtn.isVisible().catch(() => false)) {
          await deleteBtn.click();
          await page.waitForTimeout(1000);

          const confirmBtn = page.locator(
            'button:has-text("Confirm"), button:has-text("Delete"), button:has-text("Yes")'
          );
          if (await confirmBtn.first().isVisible().catch(() => false)) {
            await confirmBtn.first().click();
          }
          await page.waitForTimeout(2000);
          rolesDeleted++;
          console.log(`  Deleted role: ${roleName}`);
        }
      }
    }
    console.log(`  Deleted ${rolesDeleted} custom roles`);

    // 3. Delete test department
    await page.goto(config.TEAM_URL, { waitUntil: "networkidle" });
    await page.waitForTimeout(2000);

    const deptTab = page.locator(
      'button:has-text("Departments"), [role="tab"]:has-text("Departments")'
    );
    await deptTab.first().click();
    await page.waitForTimeout(2000);

    const deptEl = page.locator(`text=/QA Dept/`).first();
    if (await deptEl.isVisible().catch(() => false)) {
      const deleteBtn = deptEl.locator(
        "xpath=ancestor::tr//button[contains(@aria-label,'Delete') or contains(@class,'delete')], xpath=ancestor::*[contains(@class,'row')]//button:last-of-type"
      ).first();
      if (await deleteBtn.isVisible().catch(() => false)) {
        await deleteBtn.click();
        await page.waitForTimeout(1000);
        const confirmBtn = page.locator('button:has-text("Confirm"), button:has-text("Delete")');
        if (await confirmBtn.first().isVisible().catch(() => false)) {
          await confirmBtn.first().click();
        }
        await page.waitForTimeout(2000);
        console.log("  Deleted test department");
      }
    }

    console.log("=== CLEANUP DONE ===");
  });
});
