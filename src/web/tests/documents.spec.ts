import { expect, test, type Page } from '@playwright/test';
import { readFile } from 'node:fs/promises';
const evidenceDir = process.env.BROWSER_EVIDENCE_DIR || '../../runs/2026-10-10-slice-02-documents';

test.beforeEach(async ({ page }) => {
  await page.goto('/');
  // Stop before any write if a worktree accidentally points at another slice's database.
  const configuration = await page.request.get('/config.json');
  expect((await configuration.json()).api_url).toBe(process.env.LOCAL_TEST_API_URL || 'http://127.0.0.1:8121');
});

async function caseAndUpload(page: Page, content = 'Fictional policy.\nOwner is unknown.\n') {
  await page.getByRole('button', { name: 'Continue with local identity' }).click();
  await page.getByLabel('Fictional bank name').fill(`Fictional document bank ${Date.now()}`);
  await page.getByLabel('I confirm this case contains fictional data only.', { exact: true }).check();
  await page.getByRole('button', { name: 'Save fictional case' }).click();
  await expect(page.getByRole('heading', { name: 'Documents', exact: true })).toBeVisible();
  await page.getByLabel('Document file', { exact: true }).setInputFiles({ name: 'policy.txt', mimeType: 'text/plain', buffer: Buffer.from(content) });
  await page.getByLabel('Document role', { exact: true }).selectOption('policy');
  await page.getByLabel('I confirm this document contains fictional data only.', { exact: true }).check();
  await page.getByRole('button', { name: 'Upload fictional document', exact: true }).click();
  await expect(page.getByRole('region', { name: 'Source evidence', exact: true })).toContainText('Owner is unknown.');
}

test('VS2-BT01 upload, inspect source lines, refresh and reopen the same version', async ({ page }) => {
  await caseAndUpload(page);
  const source = page.getByRole('region', { name: 'Source evidence', exact: true });
  await expect(source).toContainText('Line 2');
  await expect(source).toContainText('Version 1');
  await expect(page.getByText('No assessment has run.', { exact: true })).toBeVisible();
  const selected = new URL(page.url()).searchParams.get('source');
  expect(selected).toBeTruthy();
  await page.reload();
  await page.getByRole('button', { name: 'Continue with local identity' }).click();
  await expect(source).toContainText('Owner is unknown.');
  expect(new URL(page.url()).searchParams.get('source')).toBe(selected);
  await page.screenshot({ path: `${evidenceDir}/documents-desktop.png`, fullPage: true });
});

test('VS2-BT02 replacement leaves the earlier version available', async ({ page }) => {
  await caseAndUpload(page);
  await page.getByLabel('Replace source', { exact: true }).selectOption({ label: 'policy.txt' });
  await page.getByLabel('Document file', { exact: true }).setInputFiles({ name: 'policy.txt', mimeType: 'text/plain', buffer: Buffer.from('Revised fictional policy.\n') });
  await page.getByLabel('I confirm this document contains fictional data only.', { exact: true }).check();
  await page.getByRole('button', { name: 'Upload fictional document', exact: true }).click();
  await expect(page.getByRole('region', { name: 'Source evidence', exact: true })).toContainText('Revised fictional policy.');
  await expect(page.getByRole('region', { name: 'Source evidence', exact: true })).toContainText('Version 2');
  await page.getByRole('button', { name: 'Inspect policy.txt version 1', exact: true }).click();
  await expect(page.getByRole('region', { name: 'Source evidence', exact: true })).toContainText('Owner is unknown.');
});

test('VS2-BT03 malformed input is rejected and source text cannot execute HTML', async ({ page }) => {
  await caseAndUpload(page, 'Fictional policy.\nOwner is unknown.\n<img src=x onerror="document.title=\'bad\'">');
  await expect(page).toHaveTitle('The Regulator');
  await expect(page.getByRole('region', { name: 'Source evidence', exact: true })).toContainText('<img src=x');
  await page.getByLabel('Document file', { exact: true }).setInputFiles({ name: 'invalid.pdf', mimeType: 'application/pdf', buffer: Buffer.from('Not a PDF') });
  await page.getByLabel('I confirm this document contains fictional data only.', { exact: true }).check();
  await page.getByRole('button', { name: 'Upload fictional document', exact: true }).click();
  await expect(page.getByRole('alert')).toContainText(/unreadable|invalid|supported/i);
  await expect(page.getByRole('button', { name: 'Inspect policy.txt version 1', exact: true })).toBeVisible();
});

test('VS2-BT04 source inspection supports keyboard focus and mobile layout', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 812 });
  await caseAndUpload(page);
  const inspect = page.getByRole('button', { name: 'Inspect policy.txt version 1', exact: true });
  await inspect.focus();
  await page.keyboard.press('Enter');
  await expect(page.getByRole('region', { name: 'Source evidence', exact: true })).toContainText('Owner is unknown.');
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true);
  await page.screenshot({ path: `${evidenceDir}/documents-mobile.png`, fullPage: true });
});

test('VS2-BT05 an uncertain upload requires checking saved versions before retry', async ({ page }) => {
  await caseAndUpload(page);
  await page.route('**/documents', async route => {
    if (route.request().method() !== 'POST') return route.continue();
    // The server saved the version, but its acknowledgment was lost.
    await route.fetch();
    await route.fulfill({ status: 503, json: { code: 'unavailable' } });
  });
  await page.getByLabel('Document file', { exact: true }).setInputFiles({ name: 'saved-but-uncertain.txt', mimeType: 'text/plain', buffer: Buffer.from('Another fictional policy.') });
  await page.getByLabel('I confirm this document contains fictional data only.', { exact: true }).check();
  const upload = page.getByRole('button', { name: 'Upload fictional document', exact: true });
  await upload.click();
  await expect(upload).toBeDisabled();
  await expect(page.getByRole('alert')).toContainText('Refresh documents');
  await page.getByRole('button', { name: 'Refresh documents', exact: true }).click();
  await expect(page.getByRole('button', { name: 'Inspect saved-but-uncertain.txt version 1', exact: true })).toBeVisible();
});

test('VS2-BT06 original download preserves the uploaded bytes', async ({ page }) => {
  const content = 'Fictional policy.\nOwner is unknown.\n';
  await caseAndUpload(page, content);
  const received = page.waitForEvent('download');
  await page.getByRole('button', { name: 'Download original', exact: true }).click();
  const download = await received;
  expect(download.suggestedFilename()).toBe('policy.txt');
  expect(await readFile((await download.path())!, 'utf8')).toBe(content);
});
