import { expect, test, type Page, type Download } from '@playwright/test';
import { readFileSync } from 'node:fs';
const evidenceDir = process.env.BROWSER_EVIDENCE_DIR || '../../runs/2026-10-11-slice-05-release';

async function assessment(page: Page) {
  await page.goto('/');
  await page.getByRole('button', {name: 'Continue with local identity'}).click();
  await page.getByLabel('Fictional bank name').fill(`Fictional export bank ${Date.now()}`);
  await page.getByLabel('I confirm this case contains fictional data only.', {exact:true}).check();
  await page.getByRole('button', {name: 'Save fictional case'}).click();
  await page.getByLabel('Document file', {exact:true}).setInputFiles({name:'policy.txt',mimeType:'text/plain',buffer:readFileSync('../../data/fixtures/slice-02-policy.txt')});
  await page.getByLabel('I confirm this document contains fictional data only.', {exact:true}).check();
  await page.getByRole('button', {name:'Upload fictional document',exact:true}).click();
  await page.getByRole('button', {name:'Run controlled assessment',exact:true}).click();
  const result = page.getByRole('region',{name:'Assessment result',exact:true});
  await expect(result).toContainText('Needs review');
  return result;
}

async function text(download: Download) {
  expect(await download.failure()).toBeNull();
  return readFileSync((await download.path())!, 'utf8');
}

test('VS5-BT01 JSON and Markdown downloads preserve saved review and exact sources',async ({page}) => {
  const result = await assessment(page);
  await page.getByLabel('Approved',{exact:true}).check();
  await page.getByRole('button',{name:'Save review',exact:true}).click();
  await expect(result).toContainText('Approved · Revision 1');
  const expected = await result.locator('.identifier').first().innerText();
  const [json] = await Promise.all([page.waitForEvent('download'),page.getByRole('button',{name:'Download JSON',exact:true}).click()]);
  const report = JSON.parse(await text(json));
  expect(report.summary.approved).toBe(1);
  expect(report.summary.approval_rate).toBe(1);
  expect(report.snapshot.snapshot_id).toBeTruthy();
  expect(report.sources).toHaveLength(2);
  expect(report.data_mode).toBe('controlled_simulation');
  expect(report.label).toContain('Simulated');
  expect(report.cost_usd).toBeNull();
  expect(report.findings[0].status).toBe('needs_review');
  const [markdown] = await Promise.all([page.waitForEvent('download'),page.getByRole('button',{name:'Download Markdown',exact:true}).click()]);
  const contents = await text(markdown);
  expect(contents).toContain(report.snapshot.snapshot_id);
  expect(contents).toContain('approved: 1');
  expect(contents).toContain('Clause 19(b)');
  expect(contents).toContain('cost: Unknown');
  await expect(result).toContainText(expected);
  await json.saveAs(`${evidenceDir}/export-example.json`);
  await markdown.saveAs(`${evidenceDir}/export-example.md`);
  await page.screenshot({path:`${evidenceDir}/release-desktop.png`,fullPage:true});
});

test('VS5-BT02 export failure preserves saved review and retry succeeds',async ({page}) => {
  const result = await assessment(page);
  await page.getByLabel('Approved',{exact:true}).check();
  await page.getByRole('button',{name:'Save review',exact:true}).click();
  await expect(result).toContainText('Approved · Revision 1');
  const job = new URL(page.url()).searchParams.get('assessment');
  await page.route('**/assessments/*/export*',route=>route.fulfill({status:503,contentType:'application/json',body:JSON.stringify({message:'Export unavailable.',next_action:'Retry the export.'})}),{times:1});
  await page.getByRole('button',{name:'Download JSON',exact:true}).click();
  await expect(page.getByRole('alert')).toContainText('Export unavailable');
  await expect(result).toContainText('Approved · Revision 1');
  expect(new URL(page.url()).searchParams.get('assessment')).toBe(job);
  const [download] = await Promise.all([page.waitForEvent('download'),page.getByRole('button',{name:'Download JSON',exact:true}).click()]);
  expect(JSON.parse(await text(download)).summary.approved).toBe(1);
});

test('VS5-BT03 mobile keyboard download keeps labels and does not overflow',async ({page}) => {
  await page.setViewportSize({width:390,height:844});
  const result = await assessment(page);
  const download = page.getByRole('button',{name:'Download JSON',exact:true});
  await download.focus();
  const [file] = await Promise.all([page.waitForEvent('download'),page.keyboard.press('Enter')]);
  expect(JSON.parse(await text(file)).label).toContain('Simulated');
  expect(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth)).toBe(true);
  await expect(result).toContainText('Not measured');
  await page.screenshot({path:`${evidenceDir}/release-mobile.png`,fullPage:true});
});

test('VS5-BT04 refreshing the same assessment cannot discard an in-flight export',async ({page}) => {
  await assessment(page);
  let release!: () => void;
  const gate = new Promise<void>(resolve => {release = resolve;});
  await page.route('**/assessments/*/export*',async route => {
    const response = await route.fetch();
    await gate;
    await route.fulfill({response});
  },{times:1});
  await page.getByRole('button',{name:'Download JSON',exact:true}).click();
  await expect(page.getByRole('region',{name:'Export assessment',exact:true}).getByRole('status')).toContainText('Preparing export');
  const loaded = page.waitForResponse(response=>response.request().method()==='GET' && /\/assessments\/[^/?]+$/.test(new URL(response.url()).pathname));
  await page.getByRole('button',{name:'Refresh assessment',exact:true}).click();
  await loaded;
  await expect(page.getByRole('button',{name:'Refresh assessment',exact:true})).toBeEnabled();
  const downloaded = page.waitForEvent('download',{timeout:5000});
  release();
  expect(JSON.parse(await text(await downloaded)).state).toBe('completed');
  await expect(page.getByRole('button',{name:'Download JSON',exact:true})).toBeEnabled();
});
