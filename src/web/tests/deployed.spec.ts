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

const setting = process.env.DEPLOYED_ASSESSMENTS_ENABLED || 'false';
if (!['true', 'false'].includes(setting)) throw new Error('The deployed assessment setting must be true or false.');

test('VS1-AWS01 and VS2-AWS01 actual sign-in, case reopening and versioned documents', async ({ browser }) => {
  // Close the manually owned context before a sanitized error can reach the reporter.
  const context = await browser.newContext({ baseURL: process.env.DEPLOYED_URL });
  const page = await context.newPage();
  let passed = false;
  try {
    await page.goto('/');
    await expect(page.getByText('AWS development', { exact: true })).toBeVisible();
    await expect(page.getByRole('button', { name: 'Continue with local identity' })).toHaveCount(0);
    const config = await (await page.request.get('/config.json')).json();
    expect(config.assessments_enabled).toBe(setting === 'true');
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
    if (setting === 'false') {
      await expect(page.getByRole('heading', { name: 'Assessment', exact: true })).toHaveCount(0);
    } else {
      // RW07 uses the deployed queue, worker, model, records, and storage. No intercepted responses.
      await page.getByLabel('release-policy.txt · Version 1', { exact: true }).check();
      await page.getByLabel('Clause 19(b)', { exact: true }).check();
      await page.getByLabel('Assessment date', { exact: true }).fill('2024-04-08');
      await page.getByRole('button', { name: 'Run selected assessment with live model', exact: true }).click();
      const assessment = page.getByRole('region', { name: 'Assessment result', exact: true });
      await expect(assessment).toContainText('Job state: completed', { timeout: 650_000 });
      await expect(assessment).toContainText('Unchecked obligations: None');
      const jobId = new URL(page.url()).searchParams.get('assessment');
      expect(jobId).toBeTruthy();
      const reason = 'Fictional release check. Rejection verifies saved human review.';
      await page.getByLabel('Rejected', { exact: true }).check();
      await page.getByLabel('Review reason', { exact: true }).fill(reason);
      await page.getByRole('button', { name: 'Save review', exact: true }).click();
      await expect(assessment).toContainText('Rejected · Revision 1');
      const jsonTransfer = page.waitForEvent('download');
      await page.getByRole('button', { name: 'Download JSON', exact: true }).click();
      const jsonDownload = await jsonTransfer;
      expect(await jsonDownload.failure()).toBeNull();
      const report = JSON.parse(await readFile((await jsonDownload.path())!, 'utf8'));
      expect(report.job.job_id).toBe(jobId);
      expect(report.job.state).toBe('completed');
      expect(report.data_mode).toBe('synthetic_live');
      expect(report.live_model_calls).toBeGreaterThan(0);
      expect(report.live_model_calls).toBeLessThanOrEqual(24);
      expect(report.snapshot.case_id).toBe(caseId);
      expect(report.snapshot.assessment_date).toBe('2024-04-08');
      expect(report.sources.some((s: any) => s.document.document_version_id === originalVersion)).toBe(true);
      expect(report.summary.rejected).toBe(1);
      expect(report.reviews.some((r: any) => r.disposition === 'rejected' && r.reason === reason)).toBe(true);
      expect(report.findings.length).toBeGreaterThan(0);
      const citations = report.findings.flatMap((f: any) => f.citations);
      expect(citations.length).toBeGreaterThan(0);
      const normalize = (text: string) => text.replace(/\s+/g, ' ').trim();
      for (const citation of citations) {
        expect(report.sources.some((s: any) => s.document.document_version_id === citation.document_version_id &&
          s.passages.some((p: any) => p.passage_id === citation.passage_id && p.location === citation.location &&
            normalize(p.text).includes(normalize(citation.quote))))).toBe(true);
      }
      const markdownTransfer = page.waitForEvent('download');
      await page.getByRole('button', { name: 'Download Markdown', exact: true }).click();
      const markdownDownload = await markdownTransfer;
      expect(await markdownDownload.failure()).toBeNull();
      const markdown = await readFile((await markdownDownload.path())!, 'utf8');
      expect(markdown).toContain(jobId!);
      expect(markdown).toContain(report.snapshot.snapshot_id);
      expect(markdown).toContain(reason);
      await page.reload();
      await signIn(page);
      expect(new URL(page.url()).searchParams.get('assessment')).toBe(jobId);
      await expect(page.getByRole('region', { name: 'Assessment result', exact: true })).toContainText('Rejected · Revision 1');
    }
    passed = true;
  } catch {
    // Never report a hosted sign-in URL, entered credential, token, or raw browser error.
  } finally {
    await context.close().catch(() => {});
  }
  if (!passed) throw new Error('Deployed identity, document, or enabled assessment checks failed. Authentication details were not recorded.');
});
