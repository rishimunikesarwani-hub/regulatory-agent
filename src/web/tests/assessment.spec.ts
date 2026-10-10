import { expect, test, type Page } from '@playwright/test';
import { readFileSync } from 'node:fs';

async function assessment(page: Page) {
  await page.goto('/');
  expect((await (await page.request.get('/config.json')).json()).api_url).toBe('http://127.0.0.1:8131');
  await page.getByRole('button', { name: 'Continue with local identity' }).click();
  await page.getByLabel('Fictional bank name').fill(`Fictional assessment bank ${Date.now()}`);
  await page.getByLabel('I confirm this case contains fictional data only.', {exact: true}).check();
  await page.getByRole('button', {name: 'Save fictional case'}).click();
  await page.getByLabel('Document file', {exact: true}).setInputFiles({name: 'policy.txt', mimeType: 'text/plain', buffer: readFileSync('../../data/fixtures/slice-02-policy.txt')});
  await page.getByLabel('I confirm this document contains fictional data only.', {exact: true}).check();
  await page.getByRole('button', {name: 'Upload fictional document', exact: true}).click();
  await expect(page.getByRole('heading', {name: 'Assessment', exact: true})).toBeVisible();
  await page.getByRole('button', {name: 'Run controlled assessment', exact: true}).click();
  const result = page.getByRole('region', {name: 'Assessment result', exact: true});
  await expect(result).toContainText('Needs review');
  await expect(result).toContainText('Controlled simulation');
  return result;
}

test('VS3-BT01 assessment, exact citation, saved approval and refresh', async ({page}) => {
  const result = await assessment(page);
  await result.getByRole('button', {name: 'Inspect Clause 19(b)', exact: true}).click();
  const source = page.getByRole('dialog', {name: 'Assessment source', exact: true});
  await expect(source).toContainText('Personnel with elevated system access entitlements');
  await expect(source).toContainText('Current status unverified');
  await page.getByRole('button', {name: 'Close source', exact: true}).click();
  await page.getByLabel('Approved', {exact: true}).check();
  await page.getByRole('button', {name: 'Save review', exact: true}).click();
  await expect(result).toContainText('Approved · Revision 1');
  await expect(result).toContainText('Approval without edits: 100%');
  const job = new URL(page.url()).searchParams.get('assessment');
  expect(job).toBeTruthy();
  await page.reload();
  await page.getByRole('button', {name: 'Continue with local identity'}).click();
  await expect(result).toContainText('Approved · Revision 1');
  expect(new URL(page.url()).searchParams.get('assessment')).toBe(job);
  await page.screenshot({path: '../../runs/2026-10-10-slice-03-assessment/assessment-desktop.png', fullPage: true});
  await result.screenshot({path: '../../runs/2026-10-10-slice-03-assessment/assessment-review.png'});
});

test('VS3-BT02 edited and rejected reviews keep the original finding and evidence requests', async ({page}) => {
  const result = await assessment(page);
  const original = await result.locator('.original-rationale').innerText();
  await page.getByLabel('Edited', {exact: true}).check();
  await page.getByLabel('Edited rationale', {exact: true}).fill('Human review needs dated evidence.');
  await page.getByLabel('Review reason', {exact: true}).fill('The period was missing.');
  await page.getByRole('button', {name: 'Save review', exact: true}).click();
  await expect(result).toContainText('Edited · Revision 1');
  await expect(result.locator('.original-rationale')).toHaveText(original);
  await page.getByLabel('Rejected', {exact: true}).check();
  await page.getByLabel('Review reason', {exact: true}).fill('Evidence has not been examined.');
  await page.getByRole('button', {name: 'Save review', exact: true}).click();
  await expect(result).toContainText('Rejected · Revision 2');
  await page.getByLabel('Request more evidence', {exact: true}).check();
  await page.getByLabel('Review reason', {exact: true}).fill('Supply the dated activity log.');
  await page.getByRole('button', {name: 'Save review', exact: true}).click();
  await expect(result).toContainText('Evidence requested · Revision 3');
  await expect(result).toContainText('Rejected: 1');
  await expect(result).toContainText('Pending: 0');
});

test('VS3-BT03 mobile review keeps the draft after stale revision and checks uncertain saves', async ({page}) => {
  await page.setViewportSize({width: 375, height: 812});
  const result = await assessment(page);
  await page.getByLabel('Edited', {exact: true}).check();
  await page.getByLabel('Edited rationale', {exact: true}).fill('Human review needs dated evidence.');
  await page.getByLabel('Review reason', {exact: true}).fill('Keep this draft.');
  let uncertain = false;
  await page.route('**/reviews', async route => {
    if (!uncertain) return route.fulfill({status: 409, json: {code: 'revision_conflict', message: 'The review revision changed.', next_action: 'Keep your draft. Refresh the saved review.'}});
    await route.fetch();
    return route.fulfill({status: 503, json: {code: 'unavailable'}});
  });
  const save = page.getByRole('button', {name: 'Save review', exact: true});
  await save.focus(); await page.keyboard.press('Enter');
  await expect(page.getByRole('alert')).toContainText('Keep your draft');
  await expect(page.getByLabel('Review reason', {exact: true})).toHaveValue('Keep this draft.');
  await page.getByRole('button', {name: 'Refresh assessment', exact: true}).click();
  uncertain = true;
  await save.click();
  await expect(save).toBeDisabled();
  await page.getByRole('button', {name: 'Refresh assessment', exact: true}).click();
  await expect(result).toContainText('Edited · Revision 1');
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true);
  await page.screenshot({path: '../../runs/2026-10-10-slice-03-assessment/assessment-mobile.png', fullPage: true});
});

test('VS3-BT04 failed refresh cannot authorize another uncertain review save', async ({page}) => {
  const result = await assessment(page);
  await page.route('**/reviews', async route => { await route.fetch(); await route.fulfill({status: 503, json: {code: 'unavailable'}}); });
  const save = page.getByRole('button', {name: 'Save review', exact: true});
  await save.click(); await expect(save).toBeDisabled();
  await page.route(/\/assessments\/[^/]+$/, route => route.fulfill({status: 503, json: {message: 'Saved review is unavailable.'}}));
  await page.getByRole('button', {name: 'Refresh assessment', exact: true}).click();
  await expect(page.getByRole('alert')).toContainText('Saved review is unavailable');
  await expect(save).toBeDisabled();
  await page.unroute(/\/assessments\/[^/]+$/);
  await page.getByRole('button', {name: 'Refresh assessment', exact: true}).click();
  await expect(result).toContainText('Approved · Revision 1');
  await expect(result).not.toContainText('Revision 2');
});

test('VS3-BT05 expired assessment access clears private findings and review drafts', async ({page}) => {
  await assessment(page);
  await page.getByLabel('Review reason', {exact: true}).fill('Private fictional review draft.');
  await page.route(/\/assessments\/[^/]+$/, route => route.fulfill({status: 401, json: {code: 'authentication_required'}}));
  await page.getByRole('button', {name: 'Refresh assessment', exact: true}).click();
  await expect(page.getByRole('heading', {name: 'Sign in to continue'})).toBeVisible();
  await expect(page.getByText('Private fictional review draft.', {exact: true})).not.toBeVisible();
  await expect(page.getByRole('region', {name: 'Assessment result'})).not.toBeVisible();
});

test('VS3-BT06 a new case cannot inherit the previous assessment state', async ({page}) => {
  await assessment(page);
  await expect(page.getByText('Controlled assessment completed', {exact: true})).toBeVisible();
  await page.getByRole('button', {name: 'Back to cases'}).click();
  await page.getByLabel('Fictional bank name').fill(`Fictional new case ${Date.now()}`);
  await page.getByLabel('I confirm this case contains fictional data only.', {exact: true}).check();
  await page.getByRole('button', {name: 'Save fictional case'}).click();
  await expect(page.getByText('Not started', {exact: true})).toBeVisible();
  await expect(page.getByRole('region', {name: 'Assessment result'})).not.toBeVisible();
});
