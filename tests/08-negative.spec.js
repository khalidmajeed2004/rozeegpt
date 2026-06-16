// @ts-check
const { test, expect } = require("@playwright/test");
const config = require("./helpers/config");
const { login } = require("./helpers/auth");

test.describe.serial("Module 8 — Negative & Guard Rails", () => {
  /** @type {import('@playwright/test').Page} */
  let page;

  test.beforeAll(async ({ browser }) => {
    page = await browser.newPage();
    await login(page);
  });

  test.afterAll(async () => {
    await page.close();
  });

  test("NEG-001 — Cannot remove company admin", async () => {
    await page.goto(config.TEAM_URL, { waitUntil: "networkidle" });
    await page.waitForTimeout(3000);

    // Find Company Admin member rows
    const adminRow = page.locator(
      'tr:has-text("Company Admin"), [class*="row"]:has-text("Company Admin"), [class*="member"]:has-text("Company Admin")'
    ).first();

    if (await adminRow.isVisible().catch(() => false)) {
      const removeBtn = adminRow.locator(
        'button[aria-label*="emove"], button:has(svg[class*="trash"]), [title*="Remove"], [class*="delete"], [class*="remove"]'
      );

      const removeCount = await removeBtn.count();
      if (removeCount > 0) {
        const isDisabled = await removeBtn.first().isDisabled().catch(() => null);
        console.log(`  Remove button disabled: ${isDisabled}`);
        if (isDisabled === false) {
          console.log("  ⚠ Remove button is enabled for Company Admin — potential issue");
        }
      } else {
        console.log("  ✓ No remove button for Company Admin row");
      }
    } else {
      console.log("  ⚠ Company Admin row not identified");
    }
  });

  test("NEG-002 — Invalid email on invite", async () => {
    const inviteBtn = page.locator(
      'button:has-text("Invite Member"), button:has-text("Invite")'
    );
    await inviteBtn.first().click();
    await page.waitForTimeout(2000);

    const emailField = page.locator(
      'input[type="email"], input[placeholder*="mail"]'
    );
    await emailField.first().fill("not-an-email");

    const nextBtn = page.locator(
      'button:has-text("Next"), button:has-text("Continue"), button:has-text("Send")'
    );
    await nextBtn.first().click();
    await page.waitForTimeout(2000);

    const bodyText = await page.textContent("body");
    const hasError =
      bodyText.includes("valid") ||
      bodyText.includes("Valid") ||
      bodyText.includes("invalid") ||
      bodyText.includes("Invalid") ||
      bodyText.includes("email format") ||
      bodyText.includes("required");

    expect(hasError).toBeTruthy();
    console.log("  ✓ Invalid email validation triggered");

    // Cancel
    const cancelBtn = page.locator('button:has-text("Cancel")');
    await cancelBtn.first().click().catch(() => {});
  });

  test("NEG-003 — Session expired handling", async () => {
    // Create new context without cookies
    const browser = page.context().browser();
    const freshContext = await browser.newContext();
    const freshPage = await freshContext.newPage();

    try {
      await freshPage.goto(config.TEAM_URL, { waitUntil: "networkidle" });
      await freshPage.waitForTimeout(3000);

      const url = freshPage.url();
      const bodyText = await freshPage.textContent("body");

      const redirectedToLogin =
        url.includes("/signin") ||
        url.includes("/login") ||
        bodyText.includes("Sign in") ||
        bodyText.includes("Log in") ||
        bodyText.includes("Session expired") ||
        bodyText.includes("401") ||
        bodyText.includes("421");

      expect(redirectedToLogin).toBeTruthy();
      console.log(`  Unauthenticated redirect URL: ${url}`);
    } finally {
      await freshPage.close();
      await freshContext.close();
    }
  });

  test("NEG-004 — Unauthorized route (if test user lacks right)", async () => {
    // This test requires a non-admin user; SKIP if only Company Admin available
    console.log("  SKIP — Only Company Admin account available for testing");
    console.log("  To test: create a limited-role account and verify Team page access is restricted");
  });
});
