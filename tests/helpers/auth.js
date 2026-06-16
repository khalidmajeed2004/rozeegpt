const config = require("./config");

async function login(page) {
  await page.goto(config.SIGN_IN_URL, { waitUntil: "networkidle" });

  const emailInput = page.locator(
    'input[type="email"], input[name="email"], input[placeholder*="mail"]'
  );
  const passwordInput = page.locator(
    'input[type="password"], input[name="password"]'
  );

  await emailInput.first().waitFor({ state: "visible", timeout: 15000 });
  await emailInput.first().fill(config.TEST_EMAIL);
  await passwordInput.first().fill(config.TEST_PASSWORD);

  const submitBtn = page.locator(
    'button[type="submit"], button:has-text("Sign in"), button:has-text("Log in"), button:has-text("Login")'
  );
  await submitBtn.first().click();

  await page.waitForURL(/\/(employer|dashboard)/, { timeout: 30000 }).catch(() => {});

  // Handle company selection if it appears
  const companySelect = page.locator(
    'text="Select Company", text="Choose Company", [class*="company-select"]'
  );
  if (await companySelect.first().isVisible().catch(() => false)) {
    const firstCompany = page.locator(
      '[class*="company"] >> nth=0, [role="option"] >> nth=0'
    );
    if (await firstCompany.isVisible().catch(() => false)) {
      await firstCompany.click();
    }
  }

  await page.waitForTimeout(2000);
}

async function ensureLoggedIn(page) {
  const currentUrl = page.url();
  if (currentUrl.includes("/signin") || currentUrl.includes("/login")) {
    await login(page);
  }
}

module.exports = { login, ensureLoggedIn };
