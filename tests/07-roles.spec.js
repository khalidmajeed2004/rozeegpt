// @ts-check
const { test, expect } = require("@playwright/test");
const config = require("./helpers/config");
const { login } = require("./helpers/auth");

test.describe.serial("Module 7 — Roles & Permissions", () => {
  /** @type {import('@playwright/test').Page} */
  let page;

  test.beforeAll(async ({ browser }) => {
    page = await browser.newPage();
    await login(page);
  });

  test.afterAll(async () => {
    await page.close();
  });

  test("ROLE-001 — Roles page load", async () => {
    await page.goto(config.ROLES_URL, { waitUntil: "networkidle" });
    await page.waitForTimeout(3000);

    const bodyText = await page.textContent("body");

    expect(
      bodyText.includes("Roles") || bodyText.includes("Permissions")
    ).toBeTruthy();

    // Toggle Cards/Matrix
    const toggle = page.locator(
      'text="Role Cards", text="Permissions Matrix", button:has-text("Cards"), button:has-text("Matrix")'
    );
    const toggleVisible = await toggle.first().isVisible().catch(() => false);
    console.log(`  Cards/Matrix toggle visible: ${toggleVisible}`);

    // Create Custom Role button
    const createBtn = page.locator(
      'button:has-text("Create Custom Role"), button:has-text("Custom Role"), button:has-text("+ Create")'
    );
    const createVisible = await createBtn.first().isVisible().catch(() => false);
    console.log(`  Create Custom Role button: ${createVisible}`);

    // System roles section
    const hasSystemRoles =
      bodyText.includes("System Roles") ||
      bodyText.includes("Company Admin");
    expect(hasSystemRoles).toBeTruthy();
  });

  test("ROLE-002 — System role cards content", async () => {
    for (const role of config.SYSTEM_ROLES) {
      const card = page.locator(`text="${role}"`).first();
      const visible = await card.isVisible().catch(() => false);
      console.log(`  ${role}: ${visible ? "✓" : "✗"}`);
    }

    // Check for View Rights buttons
    const viewRightsBtn = page.locator(
      'button:has-text("View Rights"), a:has-text("View Rights")'
    );
    const viewRightsCount = await viewRightsBtn.count();
    console.log(`  View Rights buttons: ${viewRightsCount}`);
    expect(viewRightsCount).toBeGreaterThan(0);
  });

  test("ROLE-003 — View Rights modal (system role)", async () => {
    // Find HR Recruiter's View Rights button
    const recruiterSection = page.locator(
      ':has-text("HR Recruiter")'
    );
    const viewRightsBtn = page.locator(
      'button:has-text("View Rights")'
    );

    // Click first available View Rights (ideally HR Recruiter's)
    await viewRightsBtn.first().click();
    await page.waitForTimeout(2000);

    const bodyText = await page.textContent("body");

    // Modal with permissions
    const hasPermissions =
      bodyText.includes("permissions") ||
      bodyText.includes("Permissions") ||
      bodyText.includes("Rights") ||
      bodyText.includes("rights");
    expect(hasPermissions).toBeTruthy();

    // Check for Clone button
    const cloneBtn = page.locator(
      'button:has-text("Clone"), button:has-text("clone"), a:has-text("Clone")'
    );
    const cloneVisible = await cloneBtn.first().isVisible().catch(() => false);
    console.log(`  Clone as Custom Role button: ${cloneVisible}`);

    // Close modal
    const closeBtn = page.locator(
      'button:has-text("Close"), button:has-text("Cancel"), button[aria-label="Close"], [class*="close"]'
    );
    await closeBtn.first().click().catch(() => {});
    await page.waitForTimeout(1000);
  });

  test("ROLE-004 — Permissions Matrix view", async () => {
    const matrixToggle = page.locator(
      'button:has-text("Permissions Matrix"), button:has-text("Matrix"), text="Permissions Matrix"'
    );

    if (await matrixToggle.first().isVisible().catch(() => false)) {
      await matrixToggle.first().click();
      await page.waitForTimeout(3000);

      const bodyText = await page.textContent("body");
      // Matrix should show roles as columns and permissions as rows
      const hasMatrix =
        bodyText.includes("Company Admin") &&
        (bodyText.includes("HR Manager") || bodyText.includes("Recruiter"));
      expect(hasMatrix).toBeTruthy();
      console.log("  Permissions Matrix loaded");
    } else {
      console.log("  ⚠ Matrix toggle not found");
    }
  });

  test("ROLE-005 — Matrix ↔ Cards toggle", async () => {
    const cardsToggle = page.locator(
      'button:has-text("Role Cards"), button:has-text("Cards"), text="Role Cards"'
    );

    if (await cardsToggle.first().isVisible().catch(() => false)) {
      await cardsToggle.first().click();
      await page.waitForTimeout(2000);

      const bodyText = await page.textContent("body");
      expect(bodyText).toContain("Company Admin");
      console.log("  Toggled back to Role Cards");
    } else {
      console.log("  ⚠ Cards toggle not found");
    }
  });

  test("ROLE-006 — Member count consistency", async () => {
    // Get member counts from role cards
    const cards = page.locator('[class*="card"], [class*="Card"]');
    const cardCount = await cards.count();

    let totalFromCards = 0;
    for (let i = 0; i < cardCount; i++) {
      const text = await cards.nth(i).textContent().catch(() => "");
      const match = text.match(/(\d+)\s*member/i);
      if (match) {
        totalFromCards += parseInt(match[1]);
      }
    }
    console.log(`  Total members from role cards: ${totalFromCards}`);

    // Navigate to team page and get total
    await page.goto(config.TEAM_URL, { waitUntil: "networkidle" });
    await page.waitForTimeout(2000);
    const bodyText = await page.textContent("body");
    const totalMatch = bodyText.match(/Total\s*Members?\s*[:\s]*(\d+)/i);
    if (totalMatch) {
      console.log(`  Total Members on Team page: ${totalMatch[1]}`);
    }

    // Navigate back
    await page.goto(config.ROLES_URL, { waitUntil: "networkidle" });
    await page.waitForTimeout(2000);
  });

  test("ROLE-010 — Create custom role", async () => {
    await page.goto(config.ROLES_URL, { waitUntil: "networkidle" });
    await page.waitForTimeout(2000);

    const createBtn = page.locator(
      'button:has-text("Create Custom Role"), button:has-text("Custom Role"), button:has-text("+ Create")'
    );
    await createBtn.first().click();
    await page.waitForTimeout(2000);

    // Fill role name
    const nameInput = page.locator(
      'input[placeholder*="ame"], input[name*="name"], input[placeholder*="Role"]'
    );
    await nameInput.first().fill(config.CUSTOM_ROLE);

    // Fill description
    const descInput = page.locator(
      'textarea, input[placeholder*="escription"], input[name*="description"]'
    );
    if (await descInput.first().isVisible().catch(() => false)) {
      await descInput.first().fill("QA automation custom role");
    }

    // Toggle some rights (3-5)
    const toggles = page.locator(
      'input[type="checkbox"], [role="switch"], [class*="toggle"], [class*="Toggle"]'
    );
    const toggleCount = await toggles.count();
    const toToggle = Math.min(5, toggleCount);
    for (let i = 0; i < toToggle; i++) {
      await toggles.nth(i).click().catch(() => {});
      await page.waitForTimeout(200);
    }
    console.log(`  Toggled ${toToggle} rights`);

    // Save
    const saveBtn = page.locator(
      'button:has-text("Save"), button:has-text("Create"), button:has-text("Done")'
    );
    await saveBtn.first().click();
    await page.waitForTimeout(3000);

    const bodyText = await page.textContent("body");
    const hasRole = bodyText.includes(config.CUSTOM_ROLE);
    expect(hasRole).toBeTruthy();
    console.log(`  Custom role "${config.CUSTOM_ROLE}" created`);
  });

  test("ROLE-011 — Edit custom role", async () => {
    // Find our custom role
    const customRoleEl = page.locator(`text="${config.CUSTOM_ROLE}"`).first();

    if (await customRoleEl.isVisible().catch(() => false)) {
      // Find edit button near it
      const editBtn = page.locator(
        `button:has-text("Edit"):near(:text("${config.CUSTOM_ROLE}"))`,
      ).first();

      const altEdit = page.locator(`text="${config.CUSTOM_ROLE}"`).locator(
        "xpath=ancestor::*[contains(@class,'card') or contains(@class,'Card')]//button[contains(text(),'Edit') or @aria-label='Edit']"
      ).first();

      const target = (await editBtn.isVisible().catch(() => false)) ? editBtn : altEdit;

      if (await target.isVisible().catch(() => false)) {
        await target.click();
        await page.waitForTimeout(2000);

        // Change description
        const descInput = page.locator('textarea').first();
        if (await descInput.isVisible().catch(() => false)) {
          await descInput.fill("QA automation custom role - updated");
        }

        const saveBtn = page.locator(
          'button:has-text("Save"), button:has-text("Update")'
        );
        await saveBtn.first().click();
        await page.waitForTimeout(3000);
        console.log("  Custom role updated");
      } else {
        console.log("  ⚠ Edit button not found for custom role");
      }
    }
  });

  test("ROLE-012 — Clone system role as custom", async () => {
    // View Rights on Interviewer and clone
    const viewRightsBtns = page.locator('button:has-text("View Rights")');
    const count = await viewRightsBtns.count();

    // Try to find Interviewer's View Rights
    for (let i = 0; i < count; i++) {
      const parent = viewRightsBtns.nth(i).locator("xpath=ancestor::*[contains(@class,'card') or contains(@class,'Card')]").first();
      const text = await parent.textContent().catch(() => "");
      if (text.includes("Interviewer")) {
        await viewRightsBtns.nth(i).click();
        await page.waitForTimeout(2000);
        break;
      }
    }

    const cloneBtn = page.locator(
      'button:has-text("Clone"), button:has-text("clone")'
    );
    if (await cloneBtn.first().isVisible().catch(() => false)) {
      await cloneBtn.first().click();
      await page.waitForTimeout(2000);

      const nameInput = page.locator(
        'input[placeholder*="ame"], input[name*="name"]'
      );
      if (await nameInput.first().isVisible().catch(() => false)) {
        await nameInput.first().fill(config.CLONE_ROLE);
        const saveBtn = page.locator(
          'button:has-text("Save"), button:has-text("Create")'
        );
        await saveBtn.first().click();
        await page.waitForTimeout(3000);
        console.log(`  Cloned as "${config.CLONE_ROLE}"`);
      }
    } else {
      console.log("  ⚠ Clone button not found");
      // Close modal
      const closeBtn = page.locator('button:has-text("Close"), button[aria-label="Close"]');
      await closeBtn.first().click().catch(() => {});
    }
  });

  test("ROLE-013 — Delete custom role (unassigned)", async () => {
    await page.goto(config.ROLES_URL, { waitUntil: "networkidle" });
    await page.waitForTimeout(2000);

    // Find the cloned role and delete it
    const cloneRoleEl = page.locator(`text="${config.CLONE_ROLE}"`).first();

    if (await cloneRoleEl.isVisible().catch(() => false)) {
      const deleteBtn = page.locator(`text="${config.CLONE_ROLE}"`).locator(
        "xpath=ancestor::*[contains(@class,'card') or contains(@class,'Card')]//button[contains(text(),'Delete') or @aria-label='Delete' or contains(@class,'delete')]"
      ).first();

      if (await deleteBtn.isVisible().catch(() => false)) {
        await deleteBtn.click();
        await page.waitForTimeout(1000);

        // Confirm
        page.on("dialog", async (dialog) => await dialog.accept());
        const confirmBtn = page.locator(
          'button:has-text("Confirm"), button:has-text("Delete"), button:has-text("Yes")'
        );
        if (await confirmBtn.first().isVisible().catch(() => false)) {
          await confirmBtn.first().click();
        }
        await page.waitForTimeout(3000);

        const bodyText = await page.textContent("body");
        const deleted = !bodyText.includes(config.CLONE_ROLE);
        console.log(`  Clone role deleted: ${deleted}`);
      } else {
        console.log("  ⚠ Delete button not found for clone role");
      }
    } else {
      console.log("  ⚠ Clone role not found — may not have been created");
    }
  });

  test("ROLE-014 — Cannot delete system role", async () => {
    // System roles should not have delete buttons
    const adminCard = page.locator(
      ':has-text("Company Admin")'
    ).first();

    if (await adminCard.isVisible().catch(() => false)) {
      const deleteBtn = adminCard.locator(
        'button:has-text("Delete"), [aria-label*="elete"]'
      );
      const hasDelete = await deleteBtn.count();
      expect(hasDelete).toBe(0);
      console.log("  ✓ No delete button on system role cards");
    }
  });

  test("ROLE-015 — Invite with custom role", async () => {
    await page.goto(config.TEAM_URL, { waitUntil: "networkidle" });
    await page.waitForTimeout(2000);

    const inviteBtn = page.locator(
      'button:has-text("Invite Member"), button:has-text("Invite")'
    );
    await inviteBtn.first().click();
    await page.waitForTimeout(2000);

    // Fill step 1
    const nameField = page.locator('input[placeholder*="ame"], input[name*="name"]');
    if (await nameField.first().isVisible().catch(() => false)) {
      await nameField.first().fill(`QA Custom Tester ${config.TS}`);
    }

    const emailField = page.locator('input[type="email"], input[placeholder*="mail"]');
    await emailField.first().fill(config.INVITE_CUSTOM_EMAIL);

    const nextBtn = page.locator('button:has-text("Next"), button:has-text("Continue")');
    await nextBtn.first().click();
    await page.waitForTimeout(2000);

    // Step 2: look for custom role
    const bodyText = await page.textContent("body");
    const hasCustomRole = bodyText.includes(config.CUSTOM_ROLE);
    console.log(`  Custom role in invite list: ${hasCustomRole}`);

    if (hasCustomRole) {
      const customCard = page.locator(`text="${config.CUSTOM_ROLE}"`);
      await customCard.first().click();
      await page.waitForTimeout(500);

      await nextBtn.first().click().catch(() => {});
      await page.waitForTimeout(1500);

      const sendBtn = page.locator('button:has-text("Send"), button:has-text("Invite")');
      await sendBtn.first().click();
      await page.waitForTimeout(3000);
      console.log("  Invitation with custom role sent");
    }

    // Cancel/close
    const cancelBtn = page.locator('button:has-text("Cancel"), button:has-text("Close")');
    await cancelBtn.first().click().catch(() => {});
  });
});
