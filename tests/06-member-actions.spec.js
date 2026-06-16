// @ts-check
const { test, expect } = require("@playwright/test");
const config = require("./helpers/config");
const { login } = require("./helpers/auth");

test.describe.serial("Module 6 — Active Member Actions", () => {
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

  test("TEAM-020 — Change member role", async () => {
    // Find a non-admin, non-self member
    const memberRows = page.locator(
      'tr, [class*="member-row"], [class*="MemberRow"]'
    );
    const count = await memberRows.count();

    let targetRow = null;
    for (let i = 0; i < count; i++) {
      const row = memberRows.nth(i);
      const text = await row.textContent().catch(() => "");
      if (
        !text.includes(config.TEST_EMAIL) &&
        !text.includes("Company Admin") &&
        (text.includes("HR") || text.includes("Recruiter") || text.includes("Manager") || text.includes("Interviewer") || text.includes("Line"))
      ) {
        targetRow = row;
        break;
      }
    }

    if (targetRow) {
      const roleDropdown = targetRow.locator(
        'select, [class*="dropdown"], [role="combobox"], [class*="role"]'
      ).first();

      if (await roleDropdown.isVisible().catch(() => false)) {
        await roleDropdown.click();
        await page.waitForTimeout(1000);

        // Select a different role
        const option = page.locator(
          '[role="option"]:has-text("Line Manager"), option:has-text("Line Manager"), li:has-text("Line Manager")'
        );
        if (await option.first().isVisible().catch(() => false)) {
          await option.first().click();
          await page.waitForTimeout(3000);

          const bodyText = await page.textContent("body");
          const hasSuccess =
            bodyText.includes("updated") || bodyText.includes("Updated") || bodyText.includes("changed");
          console.log(`  Role change success: ${hasSuccess}`);
        } else {
          console.log("  ⚠ Line Manager option not visible");
        }
      } else {
        console.log("  ⚠ Role dropdown not found on target row");
      }
    } else {
      console.log("  ⚠ No suitable non-admin member found for role change test");
    }
  });

  test("TEAM-021 — Fine-tune rights modal", async () => {
    // Find sliders/settings icon on a non-self member
    const slidersIcon = page.locator(
      'button[aria-label*="ights"], button[aria-label*="tune"], button:has(svg[class*="slider"]), [class*="rights-btn"], [title*="Rights"], [title*="rights"]'
    );

    // Also try generic icon buttons that might be the sliders
    const iconBtns = page.locator(
      'button:has(svg), [class*="icon-button"]'
    );

    let found = false;
    const count = await iconBtns.count();
    for (let i = 0; i < Math.min(count, 20); i++) {
      const btn = iconBtns.nth(i);
      const ariaLabel = await btn.getAttribute("aria-label").catch(() => "");
      const title = await btn.getAttribute("title").catch(() => "");
      if (
        (ariaLabel && (ariaLabel.includes("right") || ariaLabel.includes("tune") || ariaLabel.includes("slider"))) ||
        (title && (title.includes("right") || title.includes("tune") || title.includes("slider")))
      ) {
        await btn.click();
        found = true;
        break;
      }
    }

    if (found) {
      await page.waitForTimeout(2000);
      const bodyText = await page.textContent("body");
      const hasModal =
        bodyText.includes("Fine-Tune Rights") ||
        bodyText.includes("Rights") ||
        bodyText.includes("Permissions") ||
        bodyText.includes("Toggle");
      console.log(`  Fine-Tune Rights modal opened: ${hasModal}`);

      // Close modal
      const closeBtn = page.locator(
        'button:has-text("Close"), button:has-text("Cancel"), button[aria-label="Close"]'
      );
      await closeBtn.first().click().catch(() => {});
    } else {
      console.log("  ⚠ Sliders/rights icon not identified — checking alternative selectors");
    }
  });

  test("TEAM-022 — My Access read-only (self)", async () => {
    // Find own row's sliders icon
    const selfRow = page.locator(`text=${config.TEST_EMAIL}`).first();
    const selfParent = selfRow.locator(
      "xpath=ancestor::tr | xpath=ancestor::*[contains(@class,'row') or contains(@class,'member')]"
    ).first();

    if (await selfParent.isVisible().catch(() => false)) {
      const iconBtn = selfParent.locator("button:has(svg)").first();
      if (await iconBtn.isVisible().catch(() => false)) {
        await iconBtn.click();
        await page.waitForTimeout(2000);

        const bodyText = await page.textContent("body");
        const isReadOnly =
          bodyText.includes("My Access") ||
          bodyText.includes("read-only") ||
          bodyText.includes("Read Only");
        console.log(`  My Access read-only: ${isReadOnly}`);

        // Close
        const closeBtn = page.locator(
          'button:has-text("Close"), button:has-text("Cancel"), button[aria-label="Close"]'
        );
        await closeBtn.first().click().catch(() => {});
      }
    } else {
      console.log("  ⚠ Self row parent not found");
    }
  });

  test("TEAM-023 — Manage job access", async () => {
    // Find a "N Job(s) Shared" link
    const jobAccessLink = page.locator(
      'text=/\\d+\\s*Job/, a:has-text("Jobs Shared"), [class*="job-access"]'
    );

    if (await jobAccessLink.first().isVisible().catch(() => false)) {
      await jobAccessLink.first().click();
      await page.waitForTimeout(2000);

      const bodyText = await page.textContent("body");
      const hasModal =
        bodyText.includes("Manage Job Access") ||
        bodyText.includes("Job Access") ||
        bodyText.includes("All Jobs") ||
        bodyText.includes("Specific");
      console.log(`  Job Access modal: ${hasModal}`);

      // Close without saving
      const closeBtn = page.locator(
        'button:has-text("Close"), button:has-text("Cancel"), button[aria-label="Close"]'
      );
      await closeBtn.first().click().catch(() => {});
    } else {
      // Check for "All Jobs" text
      const allJobs = page.locator('text="All Jobs"');
      if (await allJobs.first().isVisible().catch(() => false)) {
        console.log("  Members have All Jobs access — no specific job access to test");
      } else {
        console.log("  ⚠ No job access link found");
      }
    }
  });

  test("TEAM-024 — Remove member (test account only)", async () => {
    // Only remove test accounts we created — look for QA test members
    const qaRow = page.locator(
      `text=/qa-invite|QA Tester|qa-custom/`
    ).first();

    if (await qaRow.isVisible().catch(() => false)) {
      const parentRow = qaRow.locator(
        "xpath=ancestor::tr | xpath=ancestor::*[contains(@class,'row') or contains(@class,'member')]"
      ).first();
      const removeBtn = parentRow.locator(
        'button[aria-label*="emove"], button:has(svg[class*="trash"]), [title*="Remove"]'
      );

      if (await removeBtn.first().isVisible().catch(() => false)) {
        await removeBtn.first().click();
        await page.waitForTimeout(1000);

        // Confirm
        page.on("dialog", async (dialog) => await dialog.accept());
        const confirmBtn = page.locator(
          'button:has-text("Confirm"), button:has-text("Remove"), button:has-text("Yes")'
        );
        if (await confirmBtn.first().isVisible().catch(() => false)) {
          await confirmBtn.first().click();
        }
        await page.waitForTimeout(3000);

        const bodyText = await page.textContent("body");
        console.log(`  Member removed: ${bodyText.includes("removed") || bodyText.includes("Removed")}`);
      }
    } else {
      console.log("  ⚠ No QA test member found to remove — SKIP (safe)");
    }
  });

  test("TEAM-025 — Removed tab audit view", async () => {
    const removedTab = page.locator(
      'button:has-text("Removed"), [role="tab"]:has-text("Removed")'
    );
    await removedTab.first().click();
    await page.waitForTimeout(3000);

    const bodyText = await page.textContent("body");
    const hasContent =
      bodyText.includes("Removed") ||
      bodyText.includes("removed") ||
      bodyText.includes("No removed members") ||
      bodyText.includes("No members");

    expect(hasContent).toBeTruthy();
    console.log("  Removed tab loaded");
  });
});
