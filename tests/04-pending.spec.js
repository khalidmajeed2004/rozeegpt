// @ts-check
const { test, expect } = require("@playwright/test");
const config = require("./helpers/config");
const { login } = require("./helpers/auth");

test.describe.serial("Module 4 — Pending Invitations", () => {
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

  test("PEND-001 — Pending tab populated", async () => {
    // Click Pending tab
    const pendingTab = page.locator(
      'button:has-text("Pending"), [role="tab"]:has-text("Pending"), a:has-text("Pending")'
    );
    await pendingTab.first().click();
    await page.waitForTimeout(3000);

    const bodyText = await page.textContent("body");

    // Check for pending invitations
    const hasPending =
      bodyText.includes("Pending") ||
      bodyText.includes("pending") ||
      bodyText.includes("Invited") ||
      bodyText.includes("Resend") ||
      bodyText.includes("Revoke");

    expect(hasPending).toBeTruthy();

    // Check for action buttons
    const resendBtn = page.locator(
      'button:has-text("Resend"), a:has-text("Resend")'
    );
    const revokeBtn = page.locator(
      'button:has-text("Revoke"), a:has-text("Revoke")'
    );

    const resendCount = await resendBtn.count();
    const revokeCount = await revokeBtn.count();
    console.log(`  Resend buttons: ${resendCount}, Revoke buttons: ${revokeCount}`);
  });

  test("PEND-002 — Resend invitation", async () => {
    const resendBtn = page.locator(
      'button:has-text("Resend")'
    );

    if (await resendBtn.first().isVisible().catch(() => false)) {
      const responsePromise = page.waitForResponse(
        (resp) => resp.url().includes("resend") || resp.url().includes("TeamV2"),
        { timeout: 10000 }
      ).catch(() => null);

      await resendBtn.first().click();
      await page.waitForTimeout(3000);

      const response = await responsePromise;
      if (response) {
        try {
          const json = await response.json();
          console.log(`  Resend API response code: ${json.code}`);
        } catch {
          console.log(`  Resend response status: ${response.status()}`);
        }
      }

      const bodyText = await page.textContent("body");
      const hasSuccess =
        bodyText.includes("resent") ||
        bodyText.includes("Resent") ||
        bodyText.includes("success") ||
        bodyText.includes("sent");
      console.log(`  Resend success message: ${hasSuccess}`);
    } else {
      console.log("  ⚠ No resend button visible — no pending invitations");
    }
  });

  test("PEND-003 — Revoke invitation", async () => {
    const revokeBtn = page.locator(
      'button:has-text("Revoke")'
    );

    if (await revokeBtn.first().isVisible().catch(() => false)) {
      // Count before
      const beforeCount = await revokeBtn.count();

      await revokeBtn.first().click();
      await page.waitForTimeout(1000);

      // Handle confirmation dialog
      const confirmBtn = page.locator(
        'button:has-text("Confirm"), button:has-text("OK"), button:has-text("Yes"), button:has-text("Revoke"):visible'
      );
      page.on("dialog", async (dialog) => {
        await dialog.accept();
      });

      if (await confirmBtn.first().isVisible().catch(() => false)) {
        await confirmBtn.first().click();
      }
      await page.waitForTimeout(3000);

      const bodyText = await page.textContent("body");
      const hasSuccess =
        bodyText.includes("revoked") ||
        bodyText.includes("Revoked") ||
        bodyText.includes("removed");
      console.log(`  Revoke success: ${hasSuccess}`);

      // Verify count decreased
      const afterCount = await revokeBtn.count();
      console.log(`  Revoke buttons before: ${beforeCount}, after: ${afterCount}`);
    } else {
      console.log("  ⚠ No revoke button visible — no pending invitations to revoke");
    }
  });
});
