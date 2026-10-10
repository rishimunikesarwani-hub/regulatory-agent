import { expect, test, type Page } from '@playwright/test';

async function signIn(page: Page) {
  await page.getByRole('button', { name: 'Sign in securely' }).click();
  const username = page.locator('input[name="username"]:visible');
  const workspace = page.getByRole('button', { name: 'Sign out', exact: true });
  await expect(username.or(workspace)).toBeVisible({ timeout: 30_000 });
  if (await username.isVisible()) {
    await username.fill(process.env.COGNITO_TEST_USERNAME!);
    await page.locator('input[name="password"]:visible').fill(process.env.COGNITO_TEST_PASSWORD!);
    await page.locator('input[type="submit"]:visible, button[type="submit"]:visible').filter({ hasText: /sign in/i }).or(page.locator('input[type="submit"][value="Sign in"]:visible')).first().click();
  }
  await expect(workspace).toBeVisible({ timeout: 30_000 });
}

test('VS1-AWS01 actual Cognito sign-in and saved fictional case reopening', async ({ browser }) => {
  // Close the manually owned context before a sanitized error can reach the reporter.
  const context = await browser.newContext({ baseURL: process.env.DEPLOYED_URL });
  const page = await context.newPage();
  let passed = false;
  try {
    await page.goto('/');
    await expect(page.getByText('AWS development', { exact: true })).toBeVisible();
    await expect(page.getByRole('button', { name: 'Continue with local identity' })).toHaveCount(0);
    await signIn(page);
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
    const caseId = new URL(page.url()).searchParams.get('case');
    await page.reload();
    await expect(page.getByRole('button', { name: 'Sign in securely' })).toBeVisible();
    await signIn(page);
    await expect(page.getByRole('heading', { name, level: 1 })).toBeVisible();
    expect(new URL(page.url()).searchParams.get('case')).toBe(caseId);
    expect(await page.evaluate(() => localStorage.length === 0 && sessionStorage.length === 0)).toBe(true);
    passed = true;
  } catch {
    // Never report a hosted sign-in URL, entered credential, token, or raw browser error.
  } finally {
    await context.close().catch(() => {});
  }
  if (!passed) throw new Error('VS1-AWS01 failed. Check the configured deployment and test operator. Authentication details were not recorded.');
});
