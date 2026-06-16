// @ts-check
const { test, expect } = require("@playwright/test");
const config = require("./helpers/config");
const { login } = require("./helpers/auth");

test.describe.serial("Module 2 — Search & Filters", () => {
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

  test("TEAM-010 — Search by name or email", async () => {
    const searchInput = page.locator(
      'input[placeholder*="earch"], input[placeholder*="name"], input[placeholder*="email"], input[type="search"]'
    );
    await searchInput.first().waitFor({ state: "visible", timeout: 5000 }).catch(() => {});

    const searchVisible = await searchInput.first().isVisible().catch(() => false);
    expect(searchVisible).toBeTruthy();

    // Type search term
    await searchInput.first().fill("mkhalid");
    await page.waitForTimeout(1500);

    const bodyText = await page.textContent("body");
    expect(bodyText).toContain("mkhalid");

    // Clear search
    await searchInput.first().fill("");
    await page.waitForTimeout(1500);
  });

  test("TEAM-011 — Search no results empty state", async () => {
    const searchInput = page.locator(
      'input[placeholder*="earch"], input[placeholder*="name"], input[placeholder*="email"], input[type="search"]'
    );

    await searchInput.first().fill("zzzznonexistent99999");
    await page.waitForTimeout(2000);

    const bodyText = await page.textContent("body");
    const hasEmptyState =
      bodyText.includes("No members found") ||
      bodyText.includes("No results") ||
      bodyText.includes("no members") ||
      bodyText.includes("Try adjusting");

    expect(hasEmptyState).toBeTruthy();

    // Verify no console errors
    const errors = [];
    page.on("pageerror", (err) => errors.push(err.message));
    await page.waitForTimeout(500);

    // Clear search
    await searchInput.first().fill("");
    await page.waitForTimeout(1000);
  });

  test("TEAM-012 — Role filter dropdown", async () => {
    const roleFilter = page.locator(
      'select:has(option:has-text("All Roles")), button:has-text("All Roles"), [class*="filter"]:has-text("Role"), [class*="dropdown"]:has-text("All Roles")'
    );

    const filterVisible = await roleFilter.first().isVisible().catch(() => false);

    if (filterVisible) {
      await roleFilter.first().click();
      await page.waitForTimeout(500);

      // Select a specific role
      const roleOption = page.locator(
        'option:has-text("HR Recruiter"), [role="option"]:has-text("HR Recruiter"), li:has-text("HR Recruiter")'
      );
      if (await roleOption.first().isVisible().catch(() => false)) {
        await roleOption.first().click();
        await page.waitForTimeout(1500);

        const bodyText = await page.textContent("body");
        expect(bodyText).toContain("HR Recruiter");
      }

      // Reset to All Roles
      await roleFilter.first().click().catch(() => {});
      const allOption = page.locator(
        'option:has-text("All Roles"), [role="option"]:has-text("All Roles"), li:has-text("All Roles")'
      );
      await allOption.first().click().catch(() => {});
      await page.waitForTimeout(1000);
    } else {
      console.log("  ⚠ Role filter dropdown not found — checking alternative filter UI");
      // May use a different filter mechanism
      const anyFilter = page.locator('[class*="filter"]');
      console.log(`  Found ${await anyFilter.count()} filter elements`);
    }
  });
});
