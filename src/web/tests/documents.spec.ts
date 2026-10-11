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

test('DD07 DD12 multiple files are saved as independent selectable sources', async ({ page }) => {
  await caseAndUpload(page);
  await page.getByLabel('Document file', { exact: true }).setInputFiles([
    { name: 'policy-two.txt', mimeType: 'text/plain', buffer: Buffer.from('Fictional weekly policy.') },
    { name: 'policy-three.txt', mimeType: 'text/plain', buffer: Buffer.from('Fictional monthly policy.') },
  ]);
  await page.getByLabel('I confirm this document contains fictional data only.', { exact: true }).check();
  await page.getByRole('button', { name: 'Upload fictional document', exact: true }).click();
  await expect(page.getByRole('region',{name:'Documents',exact:true}).getByText('2 documents saved. Earlier versions remain available.',{exact:true})).toBeVisible();
  for (const name of ['policy-two.txt','policy-three.txt']) {
    await expect(page.getByRole('button', {name:`Inspect ${name} version 1`,exact:true})).toBeVisible();
    await expect(page.getByLabel(`${name} · Version 1`,{exact:true})).toBeVisible();
  }
});

test('DD08 a replacement accepts one file and batch capacity applies before any write', async ({ page }) => {
  await caseAndUpload(page);
  const files=Array.from({length:10},(_,i)=>({name:`batch-${i}.txt`,mimeType:'text/plain',buffer:Buffer.from('Fictional policy.')}));
  await page.getByLabel('Document file', { exact: true }).setInputFiles(files.slice(0,2));
  await page.getByLabel('Replace source', { exact: true }).selectOption({ label: 'policy.txt' });
  await page.getByLabel('I confirm this document contains fictional data only.', { exact: true }).check();
  await page.getByRole('button', { name: 'Upload fictional document', exact: true }).click();
  await expect(page.getByRole('alert')).toContainText('one file');
  await page.getByLabel('Replace source', { exact: true }).selectOption('');
  await page.getByLabel('Document file', { exact: true }).setInputFiles(files);
  await page.getByRole('button', { name: 'Upload fictional document', exact: true }).click();
  await expect(page.getByRole('alert')).toContainText('9 remaining');
  await expect(page.getByRole('button', { name: 'Inspect batch-0.txt version 1', exact: true })).toHaveCount(0);
});

test('DD10 DD11 a partial batch stops on an uncertain write and keeps confirmed sources', async ({ page }) => {
  await caseAndUpload(page);
  const posts:string[]=[];
  await page.route('**/documents',async route=>{
    if(route.request().method()!=='POST')return route.continue();
    const filename=decodeURIComponent(route.request().headers()['x-filename']); posts.push(filename);
    if(filename==='uncertain.txt'){
      await route.fetch(); return route.fulfill({status:503,json:{code:'unavailable'}});
    }
    return route.continue();
  });
  await page.getByLabel('Document file', { exact: true }).setInputFiles(['confirmed.txt','uncertain.txt','later.txt'].map(name=>({name,mimeType:'text/plain',buffer:Buffer.from('Fictional policy.')})));
  await page.getByLabel('I confirm this document contains fictional data only.', { exact: true }).check();
  const upload=page.getByRole('button', { name: 'Upload fictional document', exact: true });
  await upload.click();
  await expect(upload).toBeDisabled();
  await expect(page.getByRole('alert')).toContainText('1 of 3');
  expect(posts).toEqual(['confirmed.txt','uncertain.txt']);
  await page.getByRole('button', { name: 'Refresh documents', exact: true }).click();
  await expect(page.getByRole('button', { name: 'Inspect confirmed.txt version 1', exact: true })).toBeVisible();
  await expect(page.getByRole('button', { name: 'Inspect uncertain.txt version 1', exact: true })).toBeVisible();
  await expect(page.getByRole('button', { name: 'Inspect later.txt version 1', exact: true })).toHaveCount(0);
});
