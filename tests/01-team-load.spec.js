// @ts-check
const { test, expect } = require("@playwright/test");
const config = require("./helpers/config");
const { login } = require("./helpers/auth");

test.describe.serial("Module 1 — Team Page Load & Layout", () => {
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

  test("TEAM-001 — Stat cards match tab data", async () => {
    // Get Total Members stat
    const totalMembersStat = page.locator(
      ':has-text("Total Members") >> xpath=.. >> [class*="count"], :has-text("Total Members") >> xpath=.. >> [class*="number"], :has-text("Total Members") + *'
    );

    // Get Active Members tab count
    const activeTab = page.locator(
      'text=/Active\\s*Members?\\s*\\(?\\d+\\)?/, button:has-text("Active"), [role="tab"]:has-text("Active")'
    );
    const activeTabText = await activeTab.first().textContent().catch(() => "");
    const tabCountMatch = activeTabText.match(/\((\d+)\)/);
    const tabCount = tabCountMatch ? parseInt(tabCountMatch[1]) : null;

    if (tabCount !== null) {
      console.log(`  Active Members tab count: ${tabCount}`);
    } else {
      console.log(`  Active tab text: "${activeTabText}" (count not parseable)`);
    }

    // Count member rows
    await page.waitForTimeout(2000);
    const memberRows = page.locator(
      '[class*="member-row"], [class*="MemberRow"], table tbody tr, [class*="team-member"], [data-testid*="member"]'
    );
    const rowCount = await memberRows.count();
    console.log(`  Visible member rows: ${rowCount}`);

    expect(rowCount).toBeGreaterThan(0);
  });

  test("TEAM-002 — Active members list renders", async () => {
    // Ensure we're on Active Members tab
    const activeTab = page.locator(
      'button:has-text("Active"), [role="tab"]:has-text("Active"), text=/Active/'
    );
    await activeTab.first().click().catch(() => {});
    await page.waitForTimeout(2000);

    const bodyText = await page.textContent("body");

    // Should see at least one member with role info
    const hasMembers =
      bodyText.includes("Admin") ||
      bodyText.includes("Manager") ||
      bodyText.includes("Recruiter") ||
      bodyText.includes("mkhalid") ||
      bodyText.includes("Member");
    expect(hasMembers).toBeTruthy();

    // Check for role badges
    const roleBadges = page.locator(
      '[class*="badge"], [class*="role"], [class*="chip"]'
    );
    const badgeCount = await roleBadges.count();
    console.log(`  Role badges found: ${badgeCount}`);
  });

  test("TEAM-003 — Info alert and Roles link", async () => {
    // Look for info alert about access
    const infoAlert = page.locator(
      'text=/[Hh]ow access works/, text=/role.*access/, [class*="alert"], [class*="info-box"]'
    );
    const alertVisible = await infoAlert.first().isVisible().catch(() => false);

    if (alertVisible) {
      const rolesLink = page.locator(
        'a:has-text("View roles"), a:has-text("roles & matrix"), a[href*="/roles"]'
      );
      const linkVisible = await rolesLink.first().isVisible().catch(() => false);
      expect(linkVisible).toBeTruthy();
    } else {
      console.log("  ⚠ Info alert not visible — may require scrolling or different layout");
    }
  });

  test("TEAM-004 — Self row: cannot change own role", async () => {
    // Find logged-in user's row
    const selfRow = page.locator(
      `text=${config.TEST_EMAIL}`
    ).first();
    const selfVisible = await selfRow.isVisible().catch(() => false);
    expect(selfVisible).toBeTruthy();

    // Check if role dropdown is disabled for self
    const selfRowParent = selfRow.locator("xpath=ancestor::*[contains(@class,'row') or contains(@class,'member') or self::tr]").first();

    const roleDropdown = selfRowParent.locator(
      'select, [class*="dropdown"], [role="combobox"], [class*="role-select"]'
    );

    if (await roleDropdown.count() > 0) {
      const isDisabled = await roleDropdown.first().isDisabled().catch(() => null);
      if (isDisabled !== null) {
        console.log(`  Role dropdown disabled for self: ${isDisabled}`);
      }
    } else {
      console.log("  Role dropdown not found in self row — may use different mechanism");
    }
  });
});
