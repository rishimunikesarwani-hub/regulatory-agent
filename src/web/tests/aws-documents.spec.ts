import { test, expect, type Page } from '@playwright/test';

// Controlled protocol checks. These do not contact Cognito, DynamoDB, or S3.
const web = process.env.LOCAL_TEST_WEB_URL || 'http://127.0.0.1:5192';
const api = 'https://api.example.test/api/cases/cloud-case';
const s3 = 'https://test-regulatory-documents.s3.ap-south-1.amazonaws.com';
const identity = 'https://demo.auth.ap-south-1.amazoncognito.com';
const record = { case_id: 'cloud-case', owner_id: 'fictional-operator', bank_profile: { name: 'Fictional cloud documents bank' },
  synthetic: true, created_at: '2026-10-11T12:00:00Z' };
type Source = ReturnType<typeof source>;
function source(id: string, version: string, text: string) {
  return { document: { document_version_id: id, source_id: 'source-one', case_id: record.case_id, kind: 'policy', version,
    sha256: 'a'.repeat(64), synthetic: true }, filename: 'policy.txt', format: 'txt', units: 1, uploaded_at: record.created_at,
    passages: [{ passage_id: `${id}-1`, location: 'Line 1', text }], offset: 0, passage_count: 1, next_offset: null as number | null };
}
async function fixture(page: Page, lost = false, paged = false, failedTransfer = false) {
  const saved: Source[] = [];
  const uploads = new Map<string, { state: string; request: object; document?: Source['document']; text: string }>();
  let transfers = 0, reserves = 0, fail = lost;
  const keys = new Map<string, string>();
  await page.route('**/config.json', route => route.fulfill({ json: { mode: 'aws', api_url: 'https://api.example.test',
    cognito_domain: identity, user_pool_client_id: 'test-client', redirect_uri: `${web}/` } }));
  await page.route(`${identity}/**`, route => {
    const url = new URL(route.request().url());
    if (url.pathname === '/oauth2/authorize') {
      const callback = new URL(`${web}/?case=cloud-case`);
      callback.searchParams.set('code', 'fictional-code'); callback.searchParams.set('state', url.searchParams.get('state')!);
      return route.fulfill({ status: 302, headers: { location: callback.href } });
    }
    return route.fulfill({ json: { access_token: 'fictional-access-token', token_type: 'Bearer', expires_in: 900 } });
  });
  await page.route(`${s3}/**`, route => {
    if (route.request().method() === 'POST') {
      transfers++;
      if (failedTransfer) { failedTransfer = false; return route.abort('failed'); }
      expect(route.request().headers().authorization).toBeUndefined();
      const body = route.request().postData()!;
      expect(body).toContain('name="file"'); expect(body).toContain('AES256');
      const id = Array.from(uploads.keys()).find(id => body.includes(`\r\n${id}\r\n`))!;
      uploads.get(id)!.text = body.includes('Revised fictional') ? 'Revised fictional policy.' : 'Fictional original policy.';
      return route.fulfill({ status: 204 });
    }
    return route.fulfill({ body: 'Fictional original policy.', headers: { 'Content-Disposition': 'attachment; filename="policy.txt"' } });
  });
  await page.route('https://api.example.test/api/cases**', route => {
    expect(route.request().headers().authorization).toBe('Bearer fictional-access-token');
    const url = new URL(route.request().url());
    const path = url.pathname.replace('/api/cases/cloud-case', '');
    if (url.pathname === '/api/cases') return route.fulfill({ json: { cases: [record] } });
    if (!path) return route.fulfill({ json: record });
    if (path === '/uploads' && route.request().method() === 'POST') {
      reserves++;
      const payload = route.request().postDataJSON();
      expect(payload).not.toHaveProperty('file'); expect(typeof payload.size_bytes).toBe('number');
      expect(route.request().headers()['idempotency-key']).toBeTruthy();
      const key = route.request().headers()['idempotency-key'];
      const id = keys.get(key) || `upload-${reserves}`;
      keys.set(key, id);
      if (!uploads.has(id)) uploads.set(id, { state: 'reserved', request: payload, text: '' });
      return route.fulfill({ status: 201, json: { upload_id: id, state: 'reserved', authorization: {
        upload_id: id, destination: `${s3}/`, expires_at: '2099-01-01T00:00:00Z', eligible_for_assessment: false },
        fields: { key: id, 'x-amz-server-side-encryption': 'AES256' } } });
    }
    if (path.startsWith('/uploads/')) {
      const id = path.split('/')[2], upload = uploads.get(id)!;
      if (path.endsWith('/finalize')) {
        if (upload.state !== 'finalized') {
          const item = source(id, String(saved.length + 1), upload.text); saved.unshift(item);
          upload.state = 'finalized'; upload.document = item.document;
        }
        if (fail) { fail = false; return route.fulfill({ status: 503, json: { message: 'Uncertain save.' } }); }
        return route.fulfill({ json: { document: upload.document } });
      }
      if (path.endsWith('/cancel')) upload.state = 'cancelled';
      return route.fulfill({ json: { upload_id: id, ...upload } });
    }
    if (path === '/documents') return route.fulfill({ json: { sources: saved.map(({ passages, ...metadata }) => metadata) } });
    if (path.endsWith('/original')) return route.fulfill({ json: { url: `${s3}/original` } });
    const item = saved.find(s => path.endsWith(s.document.document_version_id))!;
    if (paged && !url.searchParams.has('offset')) return route.fulfill({ json: { ...item, passage_count: 501, next_offset: 500 } });
    if (paged && url.searchParams.get('offset') === '500') return route.fulfill({ json: { ...item, offset: 500, passage_count: 501,
      passages: [{ passage_id: `${item.document.document_version_id}-501`, location: 'Line 501', text: 'Last exact fictional line.' }] } });
    return route.fulfill({ json: item });
  });
  await page.goto('/?case=cloud-case'); await page.getByRole('button', { name: 'Sign in securely' }).click();
  await expect(page.getByRole('heading', { name: 'Documents', exact: true })).toBeVisible();
  await expect(page.getByRole('button', { name: 'Run controlled assessment', exact: true })).toHaveCount(0);
  return { saved, counts: () => ({ reserves, transfers }), keys: () => Array.from(keys.keys()) };
}
async function upload(page: Page, text = 'Fictional original policy.') {
  await page.getByLabel('Document file', { exact: true }).setInputFiles({ name: 'policy.txt', mimeType: 'text/plain', buffer: Buffer.from(text) });
  await page.getByLabel('I confirm this document contains fictional data only.', { exact: true }).check();
  await page.getByRole('button', { name: 'Upload fictional document', exact: true }).click();
}
test('VS2-AWS-BT01 direct transfer, replacement, original download and reload', async ({ page }) => {
  const state = await fixture(page);
  await upload(page);
  await expect(page.getByRole('region', { name: 'Source evidence' })).toContainText('Fictional original policy.');
  await page.getByLabel('Replace source', { exact: true }).selectOption('source-one');
  await upload(page, 'Revised fictional policy.');
  await expect(page.getByRole('region', { name: 'Source evidence' })).toContainText('Version 2');
  await page.getByRole('button', { name: 'Inspect policy.txt version 1' }).click();
  const downloaded = page.waitForEvent('download');
  await page.getByRole('button', { name: 'Download original' }).click();
  expect((await downloaded).suggestedFilename()).toBe('policy.txt');
  await page.reload(); await page.getByRole('button', { name: 'Sign in securely' }).click();
  await expect(page.getByRole('region', { name: 'Source evidence' })).toContainText('Fictional original policy.');
  expect(state.counts()).toEqual({ reserves: 2, transfers: 2 });
  expect(state.saved).toHaveLength(2);
});
test('VS2-AWS-BT02 uncertain finalization confirms the existing upload after reload', async ({ page }) => {
  const state = await fixture(page, true);
  await upload(page);
  await expect(page.getByRole('alert')).toBeVisible();
  expect(new URL(page.url()).searchParams.get('upload')).toBe('upload-1');
  expect(await page.getByLabel('Document file', { exact: true }).evaluate((el: HTMLInputElement) => el.files?.length)).toBe(1);
  await page.reload(); await page.getByRole('button', { name: 'Sign in securely' }).click();
  await page.getByRole('button', { name: 'Check upload status' }).click();
  await expect(page.getByRole('region', { name: 'Source evidence' })).toContainText('Fictional original policy.');
  expect(state.saved).toHaveLength(1); expect(state.counts()).toEqual({ reserves: 1, transfers: 1 });
});
test('VS2-AWS-BT03 exact source pages support mobile navigation', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 812 });
  await fixture(page, false, true); await upload(page);
  await page.getByRole('button', { name: 'Next source page' }).click();
  await expect(page.getByRole('region', { name: 'Source evidence' })).toContainText('Line 501');
  await page.getByRole('button', { name: 'Previous source page' }).click();
  await expect(page.getByRole('region', { name: 'Source evidence' })).toContainText('Fictional original policy.');
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
});
test('VS2-AWS-BT04 expired access clears private sources and upload state', async ({ page }) => {
  await fixture(page); await upload(page);
  await expect(page.getByRole('region', { name: 'Source evidence' })).toContainText('Fictional original policy.');
  await page.route(`${api}/documents`, route => route.fulfill({ status: 401, json: { message: 'Sign in.' } }));
  await page.getByRole('button', { name: 'Refresh documents' }).click();
  await expect(page.getByRole('button', { name: 'Sign in securely' })).toBeVisible();
  await expect(page.getByRole('heading', { name: 'Documents', exact: true })).toHaveCount(0);
});

test('VS2-AWS-BT02 failed S3 transfer resumes the same reserved upload', async ({ page }) => {
  const state = await fixture(page, false, false, true);
  await upload(page);
  await expect(page.getByRole('alert')).toBeVisible();
  await page.getByRole('button', { name: 'Check upload status' }).click();
  await expect(page.getByRole('status')).toContainText('unfinished');
  await page.getByRole('button', { name: 'Resume upload' }).click();
  await expect(page.getByRole('region', { name: 'Source evidence' })).toContainText('Fictional original policy.');
  expect(state.saved).toHaveLength(1);
  expect(state.saved[0].document.document_version_id).toBe('upload-1');
  expect(state.counts()).toEqual({ reserves: 2, transfers: 2 });
});

test('VS2-AWS-BT02 unfinished reservation can be cancelled without showing a saved source', async ({ page }) => {
  const state = await fixture(page, false, false, true);
  await upload(page);
  await expect(page.getByRole('alert')).toBeVisible();
  await page.getByRole('button', { name: 'Cancel unfinished upload' }).click();
  await expect(page.getByRole('status')).toContainText('not saved');
  await expect(page.getByRole('button', { name: 'Upload fictional document', exact: true })).toBeEnabled();
  expect(state.saved).toHaveLength(0);
});

test('DD09 cloud batches reserve each file separately and keep exact transfer bytes', async ({page})=>{
  const state=await fixture(page);
  const transferred:string[]=[];
  await page.route(`${s3}/**`,async route=>{
    transferred.push(route.request().postData()!);
    return route.fallback();
  });
  await page.getByLabel('Document file',{exact:true}).setInputFiles([
    {name:'first.txt',mimeType:'text/plain',buffer:Buffer.from('Fictional first policy.')},
    {name:'second.txt',mimeType:'text/plain',buffer:Buffer.from('Fictional second policy.')},
  ]);
  await page.getByLabel('I confirm this document contains fictional data only.',{exact:true}).check();
  await page.getByRole('button',{name:'Upload fictional document',exact:true}).click();
  await expect(page.getByRole('region',{name:'Documents',exact:true}).getByText('2 documents saved. Earlier versions remain available.',{exact:true})).toBeVisible();
  expect(state.saved).toHaveLength(2);
  expect(state.counts()).toEqual({reserves:2,transfers:2});
  expect(new Set(state.keys()).size).toBe(2);
  expect(transferred[0]).toContain('filename="first.txt"');
  expect(transferred[0]).toContain('Fictional first policy.');
  expect(transferred[1]).toContain('filename="second.txt"');
  expect(transferred[1]).toContain('Fictional second policy.');
});
