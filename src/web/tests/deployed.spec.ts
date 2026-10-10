import { expect, test, type Page } from '@playwright/test';
import { readFile } from 'node:fs/promises';

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

test('VS1-AWS01 and VS2-AWS01 actual sign-in, case reopening and versioned documents', async ({ browser }) => {
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
    const original = Buffer.from('Fictional cloud release policy.\nOriginal exact line.\n');
    await page.getByLabel('Document file', { exact: true }).setInputFiles({ name: 'release-policy.txt', mimeType: 'text/plain', buffer: original });
    await page.getByLabel('I confirm this document contains fictional data only.', { exact: true }).check();
    await page.getByRole('button', { name: 'Upload fictional document', exact: true }).click();
    const evidence = page.getByRole('region', { name: 'Source evidence', exact: true });
    await expect(evidence).toContainText('Original exact line.', { timeout: 45_000 });
    await expect(evidence).toContainText('Line 2');
    const originalVersion = new URL(page.url()).searchParams.get('source');
    await page.getByLabel('Replace source', { exact: true }).selectOption({ label: 'release-policy.txt' });
    await page.getByLabel('Document file', { exact: true }).setInputFiles({ name: 'release-policy.txt', mimeType: 'text/plain',
      buffer: Buffer.from('Fictional cloud release policy.\nRevised exact line.\n') });
    await page.getByLabel('I confirm this document contains fictional data only.', { exact: true }).check();
    await page.getByRole('button', { name: 'Upload fictional document', exact: true }).click();
    await expect(evidence).toContainText('Revised exact line.', { timeout: 45_000 });
    await expect(evidence).toContainText('Version 2');
    await page.getByRole('button', { name: 'Inspect release-policy.txt version 1', exact: true }).click();
    await expect(evidence).toContainText('Original exact line.');
    const transfer = page.waitForEvent('download');
    await page.getByRole('button', { name: 'Download original' }).click();
    const download = await transfer;
    expect(download.suggestedFilename()).toBe('release-policy.txt');
    expect(await readFile((await download.path())!)).toEqual(original);
    await page.reload();
    await expect(page.getByRole('button', { name: 'Sign in securely' })).toBeVisible();
    await signIn(page);
    await expect(page.getByRole('heading', { name, level: 1 })).toBeVisible();
    expect(new URL(page.url()).searchParams.get('case')).toBe(caseId);
    expect(new URL(page.url()).searchParams.get('source')).toBe(originalVersion);
    await expect(evidence).toContainText('Original exact line.');
    expect(await page.evaluate(() => localStorage.length === 0 && sessionStorage.length === 0)).toBe(true);
    passed = true;
  } catch {
    // Never report a hosted sign-in URL, entered credential, token, or raw browser error.
  } finally {
    await context.close().catch(() => {});
  }
  if (!passed) throw new Error('VS1-AWS01 or VS2-AWS01 failed. Check deployment, permissions, and the test operator. Authentication details were not recorded.');
});
