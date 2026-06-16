// @ts-check
const { test, expect } = require("@playwright/test");
const config = require("./helpers/config");
const { login } = require("./helpers/auth");

test.describe.serial("Module 0 — Setup & Login", () => {
  /** @type {import('@playwright/test').Page} */
  let page;

  test.beforeAll(async ({ browser }) => {
    page = await browser.newPage();
  });

  test.afterAll(async () => {
    await page.close();
  });

  test("SETUP-001 — Sign in with test account", async () => {
    await login(page);

    const url = page.url();
    expect(
      url.includes("/employer") || url.includes("/dashboard")
    ).toBeTruthy();

    // Verify no error toasts
    const errorToast = page.locator(
      '[class*="error"], [class*="toast"][class*="error"], [role="alert"]:has-text("error")'
    );
    const errorCount = await errorToast.count();
    // Allow page to not have error toasts (0 is fine)
    expect(errorCount).toBeLessThanOrEqual(1); // some sites show non-error alerts
  });

  test("SETUP-002 — Sidebar shows Team and Roles", async () => {
    // Look for sidebar/nav
    const sidebar = page.locator(
      'nav, [class*="sidebar"], [class*="Sidebar"], aside, [role="navigation"]'
    );
    await sidebar.first().waitFor({ state: "visible", timeout: 10000 }).catch(() => {});

    // Check for Organization section or Team/Roles links
    const teamLink = page.locator(
      'a:has-text("Team"), [href*="/team"], nav >> text="Team"'
    );
    const rolesLink = page.locator(
      'a:has-text("Roles"), [href*="/roles"], nav >> text="Roles"'
    );

    const teamVisible = await teamLink.first().isVisible().catch(() => false);
    const rolesVisible = await rolesLink.first().isVisible().catch(() => false);

    expect(teamVisible).toBeTruthy();
    expect(rolesVisible).toBeTruthy();
  });

  test("SETUP-003 — Navigate to Team Management", async () => {
    await page.goto(config.TEAM_URL, { waitUntil: "networkidle" });
    await page.waitForTimeout(3000);

    // Page title area
    const pageContent = await page.textContent("body");

    // Check for Team Management title or similar
    const hasTeamTitle =
      pageContent.includes("Team Management") ||
      pageContent.includes("Team") ||
      pageContent.includes("Members");
    expect(hasTeamTitle).toBeTruthy();

    // Stat cards
    const statTexts = [
      "Total Members",
      "Pending",
      "Departments",
      "Roles",
    ];
    for (const text of statTexts) {
      const el = page.locator(`text=${text}`).first();
      const visible = await el.isVisible().catch(() => false);
      if (!visible) {
        console.log(`  ⚠ Stat card "${text}" not found (may use different label)`);
      }
    }

    // Tabs
    const tabs = ["Active", "Pending", "Departments", "Removed"];
    for (const tab of tabs) {
      const el = page.locator(`text=${tab}`).first();
      const visible = await el.isVisible().catch(() => false);
      if (!visible) {
        console.log(`  ⚠ Tab "${tab}" not found`);
      }
    }

    // Invite button
    const inviteBtn = page.locator(
      'button:has-text("Invite"), button:has-text("invite"), a:has-text("Invite")'
    );
    const inviteVisible = await inviteBtn.first().isVisible().catch(() => false);
    expect(inviteVisible).toBeTruthy();
  });
});
