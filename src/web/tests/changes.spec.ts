import { expect, test, type Page } from '@playwright/test';
import { readFileSync } from 'node:fs';
const evidence = process.env.BROWSER_EVIDENCE_DIR || '../../runs/2026-10-11-slice-04-changes';

async function baseline(page: Page) {
  await page.goto('/');
  expect((await (await page.request.get('/config.json')).json()).api_url).toBe(process.env.LOCAL_TEST_API_URL);
  await page.getByRole('button', {name: 'Continue with local identity'}).click();
  await page.getByLabel('Fictional bank name').fill(`Fictional version bank ${Date.now()}`);
  await page.getByLabel('I confirm this case contains fictional data only.', {exact: true}).check();
  await page.getByRole('button', {name: 'Save fictional case'}).click();
  await page.getByLabel('Document file', {exact: true}).setInputFiles({name: 'policy.txt', mimeType: 'text/plain', buffer: readFileSync('../../data/fixtures/slice-02-policy.txt')});
  await page.getByLabel('I confirm this document contains fictional data only.', {exact: true}).check();
  await page.getByRole('button', {name: 'Upload fictional document', exact: true}).click();
  await page.getByLabel('Regulatory source', {exact: true}).selectOption('SIM-ACCESS');
  await page.getByRole('button', {name: 'Run controlled assessment', exact: true}).click();
  const result = page.getByRole('region', {name: 'Assessment result', exact: true});
  await expect(result).toContainText('Privileged sessions must be logged and reviewed each week.');
  await page.getByRole('button', {name: 'Save review', exact: true}).click();
  await expect(result).toContainText('Approved · Revision 1');
  return {result, changes: page.getByRole('region', {name: 'Regulatory changes', exact: true}), original: page.url()};
}

test('VS4-BT01 added requirement creates an independent review and preserves the original', async ({page}) => {
  const {result, changes, original} = await baseline(page);
  await changes.getByRole('button', {name: 'Compare versions', exact: true}).click();
  await expect(changes).toContainText('Added requirement');
  await expect(changes).toContainText('Affected control: ACCESS-01');
  await expect(changes).toContainText('A separate reviewer must approve each weekly review.');
  await expect(result).toContainText('Approved · Revision 1');
  await changes.getByRole('button', {name: 'Open new assessment', exact: true}).click();
  await expect(result).toContainText('Approved: 0');
  await expect(result).toContainText('Pending: 1');
  await expect(result).not.toContainText('Approved · Revision 1');
  expect(page.url()).not.toBe(original);
  await result.getByRole('button', {name: 'Inspect Simulated clause 1', exact: true}).click();
  await expect(page.getByRole('dialog')).toContainText('Synthetic regulatory simulation');
  await page.getByRole('button', {name: 'Close source', exact: true}).click();
  await page.getByLabel('Rejected', {exact: true}).check();
  await page.getByLabel('Review reason', {exact: true}).fill('Separate approval evidence is missing.');
  await page.getByRole('button', {name: 'Save review', exact: true}).click();
  await expect(result).toContainText('Rejected · Revision 1');
  await changes.getByRole('button', {name: 'Open previous assessment', exact: true}).click();
  await expect(result).toContainText('Approved · Revision 1');
  await expect(result).not.toContainText('Rejected · Revision 1');
  await page.screenshot({path: `${evidence}/changes-desktop.png`, fullPage: true});
});

test('VS4-BT02 wording and cosmetic changes preserve the original review', async ({page}) => {
  const {result, changes, original} = await baseline(page);
  for (const [version, title] of [['v2-cosmetic', 'Appearance only'], ['v2-replaced', 'Wording only']]) {
    await changes.getByLabel('Newer version', {exact: true}).selectOption(version);
    await changes.getByRole('button', {name: 'Compare versions', exact: true}).click();
    await expect(changes).toContainText(title);
    await expect(changes).toContainText('No changed requirement in this fixed simulation.');
    await expect(changes.getByRole('button', {name: 'Open new assessment', exact: true})).toHaveCount(0);
    await expect(result).toContainText('Approved · Revision 1');
    expect(page.url()).toBe(original);
  }
});

test('VS4-BT03 reload restores comparisons and separate review histories', async ({page}) => {
  const {result, changes} = await baseline(page);
  await changes.getByRole('button', {name: 'Compare versions', exact: true}).click();
  await changes.getByRole('button', {name: 'Open new assessment', exact: true}).click();
  await page.getByRole('button', {name: 'Save review', exact: true}).click();
  await expect(result).toContainText('Approved · Revision 1');
  const job = new URL(page.url()).searchParams.get('assessment');
  await page.reload();
  await page.getByRole('button', {name: 'Continue with local identity'}).click();
  await expect(result).toContainText('Approved · Revision 1');
  expect(new URL(page.url()).searchParams.get('assessment')).toBe(job);
  await expect(changes).toContainText('Added requirement');
  await changes.getByRole('button', {name: 'Open previous assessment', exact: true}).click();
  await expect(result).toContainText('Approved · Revision 1');
  await expect.poll(() => new URL(page.url()).searchParams.get('assessment')).not.toBe(job);
});

test('VS4-BT05 review saves wait for the selected assessment to finish loading', async ({page}) => {
  const {result, changes} = await baseline(page);
  const [response] = await Promise.all([
    page.waitForResponse(r => r.request().method() === 'POST' && r.url().endsWith('/comparisons')),
    changes.getByRole('button', {name: 'Compare versions', exact: true}).click(),
  ]);
  const comparison = await response.json();
  let release!: () => void;
  const waiting = new Promise<void>(resolve => {release = resolve;});
  await page.route(`**/assessments/${comparison.new_job_id}`, async route => {await waiting; await route.continue();});
  await changes.getByRole('button', {name: 'Open new assessment', exact: true}).click();
  await expect(result.getByRole('button', {name: 'Save review', exact: true})).toBeDisabled();
  release();
  await expect(result).toContainText('Pending: 1');
  await expect(result.getByRole('button', {name: 'Save review', exact: true})).toBeEnabled();
  await expect(result).not.toContainText('Approved · Revision 1');
});

test('VS4-BT04 mobile keyboard controls and source passages fit the viewport', async ({page}) => {
  await page.setViewportSize({width: 390, height: 844});
  const {changes} = await baseline(page);
  const candidate = changes.getByLabel('Newer version', {exact: true});
  await candidate.focus();
  await expect(candidate).toBeFocused();
  await page.keyboard.press('Tab');
  await expect(changes.getByRole('button', {name: 'Compare versions', exact: true})).toBeFocused();
  await page.keyboard.press('Enter');
  await expect(changes).toContainText('Added requirement');
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBeTruthy();
  await page.screenshot({path: `${evidence}/changes-mobile.png`, fullPage: true});
});
