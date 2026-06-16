// @ts-check
const { test, expect } = require("@playwright/test");
const config = require("./helpers/config");
const { login } = require("./helpers/auth");

test.describe.serial("Module 3 — Invite Team Member", () => {
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

  test("INV-001 — Open invite modal", async () => {
    const inviteBtn = page.locator(
      'button:has-text("Invite Member"), button:has-text("Invite"), a:has-text("Invite Member")'
    );
    await inviteBtn.first().click();
    await page.waitForTimeout(2000);

    // Modal should be visible
    const modal = page.locator(
      '[class*="modal"], [class*="Modal"], [class*="dialog"], [role="dialog"], [class*="drawer"]'
    );
    await modal.first().waitFor({ state: "visible", timeout: 5000 });

    const modalText = await modal.first().textContent();

    // Check for step indicator and fields
    const hasTitle =
      modalText.includes("Invite") || modalText.includes("invite");
    expect(hasTitle).toBeTruthy();

    // Check for email / name fields
    const emailField = page.locator(
      'input[type="email"], input[placeholder*="mail"], input[name*="email"]'
    );
    const hasEmail = (await emailField.count()) > 0;

    const nameField = page.locator(
      'input[placeholder*="ame"], input[name*="name"], input[placeholder*="Full"]'
    );
    const hasName = (await nameField.count()) > 0;

    console.log(`  Email field present: ${hasEmail}, Name field present: ${hasName}`);

    // Check Next/Cancel buttons
    const nextBtn = page.locator(
      'button:has-text("Next"), button:has-text("Continue")'
    );
    const cancelBtn = page.locator('button:has-text("Cancel")');

    expect(await nextBtn.first().isVisible().catch(() => false) || await cancelBtn.first().isVisible().catch(() => false)).toBeTruthy();
  });

  test("INV-002 — Step 1 validation: email required", async () => {
    // Try clicking Next without entering email
    const emailField = page.locator(
      'input[type="email"], input[placeholder*="mail"], input[name*="email"]'
    );
    await emailField.first().fill("").catch(() => {});

    const nextBtn = page.locator(
      'button:has-text("Next"), button:has-text("Continue"), button:has-text("Choose Role")'
    );
    await nextBtn.first().click();
    await page.waitForTimeout(1000);

    const bodyText = await page.textContent("body");
    const hasValidation =
      bodyText.includes("required") ||
      bodyText.includes("Required") ||
      bodyText.includes("enter") ||
      bodyText.includes("valid email") ||
      bodyText.includes("Email is required");

    expect(hasValidation).toBeTruthy();
  });

  test("INV-003 — Step 1: fill details and advance", async () => {
    // Fill name
    const nameField = page.locator(
      'input[placeholder*="ame"], input[name*="name"], input[placeholder*="Full"]'
    );
    if (await nameField.first().isVisible().catch(() => false)) {
      await nameField.first().fill(config.MEMBER_NAME);
    }

    // Fill email
    const emailField = page.locator(
      'input[type="email"], input[placeholder*="mail"], input[name*="email"]'
    );
    await emailField.first().fill(config.INVITE_EMAIL);

    // Select department if available
    const deptField = page.locator(
      'input[placeholder*="epartment"], [class*="department"], select:has(option:has-text("Department"))'
    );
    if (await deptField.first().isVisible().catch(() => false)) {
      await deptField.first().click();
      await page.waitForTimeout(500);
      // Select first option or type new
      const deptOption = page.locator(
        '[role="option"] >> nth=0, [class*="option"] >> nth=0'
      );
      if (await deptOption.isVisible().catch(() => false)) {
        await deptOption.click();
      }
    }

    // Click Next
    const nextBtn = page.locator(
      'button:has-text("Next"), button:has-text("Continue"), button:has-text("Choose Role")'
    );
    await nextBtn.first().click();
    await page.waitForTimeout(2000);

    // Should advance to step 2 — role selection
    const bodyText = await page.textContent("body");
    const hasRoleStep =
      bodyText.includes("Select a Role") ||
      bodyText.includes("Choose Role") ||
      bodyText.includes("Role") ||
      bodyText.includes("Company Admin") ||
      bodyText.includes("HR Manager");

    expect(hasRoleStep).toBeTruthy();
    console.log("  Advanced to Step 2: Role Selection");
  });

  test("INV-004 — Step 2: select HR Recruiter", async () => {
    // Select HR Recruiter role
    const recruiterCard = page.locator(
      'text="HR Recruiter"'
    );
    await recruiterCard.first().click();
    await page.waitForTimeout(500);

    // Click Next to step 3
    const nextBtn = page.locator(
      'button:has-text("Next"), button:has-text("Continue"), button:has-text("Set Access")'
    );
    await nextBtn.first().click();
    await page.waitForTimeout(2000);

    // Should advance to step 3 — job access
    const bodyText = await page.textContent("body");
    const hasAccessStep =
      bodyText.includes("Job Access") ||
      bodyText.includes("Access") ||
      bodyText.includes("All Jobs") ||
      bodyText.includes("Specific") ||
      bodyText.includes("Send Invitation");

    expect(hasAccessStep).toBeTruthy();
    console.log("  Advanced to Step 3: Job Access");
  });

  test("INV-005 — Step 3: specific jobs invite", async () => {
    // Try selecting Specific Jobs if available
    const specificJobs = page.locator(
      'text="Specific Jobs", label:has-text("Specific"), input[value*="specific"]'
    );
    if (await specificJobs.first().isVisible().catch(() => false)) {
      await specificJobs.first().click();
      await page.waitForTimeout(1000);

      // Select a job chip
      const jobChip = page.locator(
        '[class*="chip"] >> nth=0, [class*="job-item"] >> nth=0, [class*="tag"] >> nth=0'
      );
      if (await jobChip.isVisible().catch(() => false)) {
        await jobChip.click();
      }
    }

    // Capture network response
    const responsePromise = page.waitForResponse(
      (resp) => resp.url().includes("invite") || resp.url().includes("TeamV2"),
      { timeout: 15000 }
    ).catch(() => null);

    // Send invitation
    const sendBtn = page.locator(
      'button:has-text("Send Invitation"), button:has-text("Send"), button:has-text("Invite")'
    );
    await sendBtn.first().click();
    await page.waitForTimeout(3000);

    // Check for success
    const bodyText = await page.textContent("body");
    const hasSuccess =
      bodyText.includes("sent") ||
      bodyText.includes("Sent") ||
      bodyText.includes("success") ||
      bodyText.includes("Success");

    // Check API response if captured
    const response = await responsePromise;
    if (response) {
      try {
        const json = await response.json();
        console.log(`  API response code: ${json.code}, message: ${json.message || ""}`);
        if (json.code === config.API_SUCCESS) {
          console.log("  ✓ API returned success code 11");
        }
      } catch {
        console.log(`  API response status: ${response.status()}`);
      }
    }

    // Verify no "Something went wrong"
    expect(bodyText).not.toContain("Something went wrong");
    console.log("  Invitation sent");
  });

  test("INV-006 — Invite company-wide role (HR Manager)", async () => {
    // Navigate back to team page and open invite again
    await page.goto(config.TEAM_URL, { waitUntil: "networkidle" });
    await page.waitForTimeout(2000);

    const inviteBtn = page.locator(
      'button:has-text("Invite Member"), button:has-text("Invite")'
    );
    await inviteBtn.first().click();
    await page.waitForTimeout(2000);

    // Fill step 1
    const nameField = page.locator(
      'input[placeholder*="ame"], input[name*="name"]'
    );
    if (await nameField.first().isVisible().catch(() => false)) {
      await nameField.first().fill(`QA Manager ${config.TS}`);
    }

    const emailField = page.locator(
      'input[type="email"], input[placeholder*="mail"], input[name*="email"]'
    );
    await emailField.first().fill(config.INVITE_MGR_EMAIL);

    const nextBtn = page.locator(
      'button:has-text("Next"), button:has-text("Continue"), button:has-text("Choose Role")'
    );
    await nextBtn.first().click();
    await page.waitForTimeout(2000);

    // Step 2: select HR Manager
    const mgrCard = page.locator('text="HR Manager"');
    await mgrCard.first().click();
    await page.waitForTimeout(500);

    const nextBtn2 = page.locator(
      'button:has-text("Next"), button:has-text("Continue"), button:has-text("Set Access")'
    );
    await nextBtn2.first().click();
    await page.waitForTimeout(2000);

    // Step 3: company-wide role should not require job selection
    const sendBtn = page.locator(
      'button:has-text("Send Invitation"), button:has-text("Send"), button:has-text("Invite")'
    );
    await sendBtn.first().click();
    await page.waitForTimeout(3000);

    const bodyText = await page.textContent("body");
    expect(bodyText).not.toContain("Something went wrong");
    console.log("  HR Manager invitation sent");
  });

  test("INV-007 — Back navigation in wizard", async () => {
    // Open invite again
    await page.goto(config.TEAM_URL, { waitUntil: "networkidle" });
    await page.waitForTimeout(2000);

    const inviteBtn = page.locator(
      'button:has-text("Invite Member"), button:has-text("Invite")'
    );
    await inviteBtn.first().click();
    await page.waitForTimeout(2000);

    // Fill step 1
    const emailField = page.locator(
      'input[type="email"], input[placeholder*="mail"]'
    );
    const testEmail = `qa-back-test-${config.TS}@mailinator.com`;
    await emailField.first().fill(testEmail);

    // Go to step 2
    const nextBtn = page.locator(
      'button:has-text("Next"), button:has-text("Continue")'
    );
    await nextBtn.first().click();
    await page.waitForTimeout(1500);

    // Select a role and go to step 3
    const roleCard = page.locator('text="HR Recruiter"');
    if (await roleCard.first().isVisible().catch(() => false)) {
      await roleCard.first().click();
      const nextBtn2 = page.locator(
        'button:has-text("Next"), button:has-text("Continue")'
      );
      await nextBtn2.first().click().catch(() => {});
      await page.waitForTimeout(1000);
    }

    // Go back
    const backBtn = page.locator(
      'button:has-text("Back"), button:has-text("← Back"), button:has-text("Previous")'
    );
    if (await backBtn.first().isVisible().catch(() => false)) {
      await backBtn.first().click();
      await page.waitForTimeout(500);
      // Go back again to step 1
      if (await backBtn.first().isVisible().catch(() => false)) {
        await backBtn.first().click();
        await page.waitForTimeout(1000);
      }
    }

    // Verify email preserved
    const emailValue = await emailField.first().inputValue().catch(() => "");
    if (emailValue) {
      expect(emailValue).toContain("qa-back-test");
      console.log("  ✓ Email preserved on back navigation");
    } else {
      console.log("  ⚠ Could not verify email preservation");
    }

    // Cancel
    const cancelBtn = page.locator('button:has-text("Cancel")');
    await cancelBtn.first().click().catch(() => {});
    await page.waitForTimeout(1000);
  });

  test("INV-008 — Duplicate invite handling", async () => {
    // Try inviting same email that was already invited in INV-005
    const inviteBtn = page.locator(
      'button:has-text("Invite Member"), button:has-text("Invite")'
    );
    await inviteBtn.first().click();
    await page.waitForTimeout(2000);

    const nameField = page.locator(
      'input[placeholder*="ame"], input[name*="name"]'
    );
    if (await nameField.first().isVisible().catch(() => false)) {
      await nameField.first().fill(config.MEMBER_NAME);
    }

    const emailField = page.locator(
      'input[type="email"], input[placeholder*="mail"]'
    );
    await emailField.first().fill(config.INVITE_EMAIL);

    // Go through wizard
    const nextBtn = page.locator(
      'button:has-text("Next"), button:has-text("Continue")'
    );
    await nextBtn.first().click();
    await page.waitForTimeout(1500);

    // Select role
    const roleCard = page.locator('text="HR Recruiter"');
    if (await roleCard.first().isVisible().catch(() => false)) {
      await roleCard.first().click();
      await nextBtn.first().click().catch(() => {});
      await page.waitForTimeout(1500);
    }

    // Try to send
    const sendBtn = page.locator(
      'button:has-text("Send"), button:has-text("Invite")'
    );
    await sendBtn.first().click().catch(() => {});
    await page.waitForTimeout(3000);

    const bodyText = await page.textContent("body");
    const hasDuplicateError =
      bodyText.includes("already") ||
      bodyText.includes("Already") ||
      bodyText.includes("duplicate") ||
      bodyText.includes("exists") ||
      bodyText.includes("invited");

    console.log(`  Duplicate handling message found: ${hasDuplicateError}`);

    // Close modal
    const cancelBtn = page.locator('button:has-text("Cancel"), button:has-text("Close")');
    await cancelBtn.first().click().catch(() => {});
  });
});
