import { expect, test } from '@playwright/test';

test('VS1-AWS01 actual Cognito sign-in and saved fictional case reopening', async ({ browser }) => {
  // Close the manually owned context before a sanitized error can reach the reporter.
  const context = await browser.newContext({ baseURL: process.env.DEPLOYED_URL });
  const page = await context.newPage();
  let passed = false;
  try {
    await page.goto('/');
    await expect(page.getByText('AWS development', { exact: true })).toBeVisible();
    await expect(page.getByRole('button', { name: 'Continue with local identity' })).toHaveCount(0);
    await page.getByRole('button', { name: 'Sign in securely' }).click();
    await page.locator('input[name="username"]:visible').fill(process.env.COGNITO_TEST_USERNAME!);
    await page.locator('input[name="password"]:visible').fill(process.env.COGNITO_TEST_PASSWORD!);
    await page.locator('input[type="submit"]:visible, button[type="submit"]:visible').filter({ hasText: /sign in/i }).or(page.locator('input[type="submit"][value="Sign in"]:visible')).first().click();
    await expect(page.getByRole('heading', { name: 'Your cases' })).toBeVisible({ timeout: 30_000 });
    const name = `Fictional release bank ${Date.now()}`;
    await page.getByLabel('Fictional bank name').fill(name);
    await page.getByLabel('I confirm this case contains fictional data only.').check();
    await page.getByRole('button', { name: 'Save fictional case' }).click();
    await expect(page.getByRole('heading', { name })).toBeVisible();
    await page.getByRole('button', { name: 'Back to cases' }).click();
    await page.getByRole('button', { name: `Open ${name}`, exact: true }).click();
    await expect(page.getByRole('heading', { name })).toBeVisible();
    const storageEmpty = await page.evaluate(() => localStorage.length === 0 && sessionStorage.length === 0);
    expect(storageEmpty).toBe(true);
    expect(new URL(page.url()).searchParams.has('code')).toBe(false);
    await page.reload();
    await expect(page.getByRole('button', { name: 'Sign in securely' })).toBeVisible();
    passed = true;
  } catch {
    // Never report a hosted sign-in URL, entered credential, token, or raw browser error.
  } finally {
    await context.close().catch(() => {});
  }
  if (!passed) throw new Error('VS1-AWS01 failed. Check the configured deployment and test operator. Authentication details were not recorded.');
});
