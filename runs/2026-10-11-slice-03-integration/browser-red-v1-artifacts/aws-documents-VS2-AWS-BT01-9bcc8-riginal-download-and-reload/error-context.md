# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: aws-documents.spec.ts >> VS2-AWS-BT01 direct transfer, replacement, original download and reload
- Location: tests\aws-documents.spec.ts:94:1

# Error details

```
Test timeout of 30000ms exceeded.
```

```
Error: locator.click: Test timeout of 30000ms exceeded.
Call log:
  - waiting for getByRole('button', { name: 'Sign in securely' })

```

# Page snapshot

```yaml
- generic [ref=e2]:
  - link "Skip to content" [ref=e3] [cursor=pointer]:
    - /url: "#main"
  - banner [ref=e4]:
    - generic [ref=e5]:
      - generic [aria-hidden] [ref=e6]: R
      - generic [ref=e7]: The Regulator
  - main [ref=e8]:
    - alert [ref=e9]: Application configuration is unavailable. Contact the deployment administrator.
    - generic [ref=e10]:
      - heading "Application unavailable" [level=1] [ref=e11]
      - paragraph [ref=e12]: The sign-in configuration must be corrected before you continue.
      - button "Reload application" [ref=e13] [cursor=pointer]
  - contentinfo [ref=e14]: Fictional case workspace · Development release
```

# Test source

```ts
  1   | import { test, expect, type Page } from '@playwright/test';
  2   |
  3   | // Controlled protocol checks. These do not contact Cognito, DynamoDB, or S3.
  4   | const web = 'http://127.0.0.1:5192';
  5   | const api = 'https://api.example.test/api/cases/cloud-case';
  6   | const s3 = 'https://test-regulatory-documents.s3.ap-south-1.amazonaws.com';
  7   | const identity = 'https://demo.auth.ap-south-1.amazoncognito.com';
  8   | const record = { case_id: 'cloud-case', owner_id: 'fictional-operator', bank_profile: { name: 'Fictional cloud documents bank' },
  9   |   synthetic: true, created_at: '2026-10-11T12:00:00Z' };
  10  | type Source = ReturnType<typeof source>;
  11  | function source(id: string, version: string, text: string) {
  12  |   return { document: { document_version_id: id, source_id: 'source-one', case_id: record.case_id, kind: 'policy', version,
  13  |     sha256: 'a'.repeat(64), synthetic: true }, filename: 'policy.txt', format: 'txt', units: 1, uploaded_at: record.created_at,
  14  |     passages: [{ passage_id: `${id}-1`, location: 'Line 1', text }], offset: 0, passage_count: 1, next_offset: null as number | null };
  15  | }
  16  | async function fixture(page: Page, lost = false, paged = false, failedTransfer = false) {
  17  |   const saved: Source[] = [];
  18  |   const uploads = new Map<string, { state: string; request: object; document?: Source['document']; text: string }>();
  19  |   let transfers = 0, reserves = 0, fail = lost;
  20  |   const keys = new Map<string, string>();
  21  |   await page.route('**/config.json', route => route.fulfill({ json: { mode: 'aws', api_url: 'https://api.example.test',
  22  |     cognito_domain: identity, user_pool_client_id: 'test-client', redirect_uri: `${web}/` } }));
  23  |   await page.route(`${identity}/**`, route => {
  24  |     const url = new URL(route.request().url());
  25  |     if (url.pathname === '/oauth2/authorize') {
  26  |       const callback = new URL(`${web}/?case=cloud-case`);
  27  |       callback.searchParams.set('code', 'fictional-code'); callback.searchParams.set('state', url.searchParams.get('state')!);
  28  |       return route.fulfill({ status: 302, headers: { location: callback.href } });
  29  |     }
  30  |     return route.fulfill({ json: { access_token: 'fictional-access-token', token_type: 'Bearer', expires_in: 900 } });
  31  |   });
  32  |   await page.route(`${s3}/**`, route => {
  33  |     if (route.request().method() === 'POST') {
  34  |       transfers++;
  35  |       if (failedTransfer) { failedTransfer = false; return route.abort('failed'); }
  36  |       expect(route.request().headers().authorization).toBeUndefined();
  37  |       const body = route.request().postData()!;
  38  |       expect(body).toContain('name="file"'); expect(body).toContain('AES256');
  39  |       const id = Array.from(uploads.keys()).find(id => body.includes(`\r\n${id}\r\n`))!;
  40  |       uploads.get(id)!.text = body.includes('Revised fictional') ? 'Revised fictional policy.' : 'Fictional original policy.';
  41  |       return route.fulfill({ status: 204 });
  42  |     }
  43  |     return route.fulfill({ body: 'Fictional original policy.', headers: { 'Content-Disposition': 'attachment; filename="policy.txt"' } });
  44  |   });
  45  |   await page.route('https://api.example.test/api/cases**', route => {
  46  |     expect(route.request().headers().authorization).toBe('Bearer fictional-access-token');
  47  |     const url = new URL(route.request().url());
  48  |     const path = url.pathname.replace('/api/cases/cloud-case', '');
  49  |     if (url.pathname === '/api/cases') return route.fulfill({ json: { cases: [record] } });
  50  |     if (!path) return route.fulfill({ json: record });
  51  |     if (path === '/uploads' && route.request().method() === 'POST') {
  52  |       reserves++;
  53  |       const payload = route.request().postDataJSON();
  54  |       expect(payload).not.toHaveProperty('file'); expect(typeof payload.size_bytes).toBe('number');
  55  |       expect(route.request().headers()['idempotency-key']).toBeTruthy();
  56  |       const key = route.request().headers()['idempotency-key'];
  57  |       const id = keys.get(key) || `upload-${reserves}`;
  58  |       keys.set(key, id);
  59  |       if (!uploads.has(id)) uploads.set(id, { state: 'reserved', request: payload, text: '' });
  60  |       return route.fulfill({ status: 201, json: { upload_id: id, state: 'reserved', authorization: {
  61  |         upload_id: id, destination: `${s3}/`, expires_at: '2099-01-01T00:00:00Z', eligible_for_assessment: false },
  62  |         fields: { key: id, 'x-amz-server-side-encryption': 'AES256' } } });
  63  |     }
  64  |     if (path.startsWith('/uploads/')) {
  65  |       const id = path.split('/')[2], upload = uploads.get(id)!;
  66  |       if (path.endsWith('/finalize')) {
  67  |         if (upload.state !== 'finalized') {
  68  |           const item = source(id, String(saved.length + 1), upload.text); saved.unshift(item);
  69  |           upload.state = 'finalized'; upload.document = item.document;
  70  |         }
  71  |         if (fail) { fail = false; return route.fulfill({ status: 503, json: { message: 'Uncertain save.' } }); }
  72  |         return route.fulfill({ json: { document: upload.document } });
  73  |       }
  74  |       if (path.endsWith('/cancel')) upload.state = 'cancelled';
  75  |       return route.fulfill({ json: { upload_id: id, ...upload } });
  76  |     }
  77  |     if (path === '/documents') return route.fulfill({ json: { sources: saved.map(({ passages, ...metadata }) => metadata) } });
  78  |     if (path.endsWith('/original')) return route.fulfill({ json: { url: `${s3}/original` } });
  79  |     const item = saved.find(s => path.endsWith(s.document.document_version_id))!;
  80  |     if (paged && !url.searchParams.has('offset')) return route.fulfill({ json: { ...item, passage_count: 501, next_offset: 500 } });
  81  |     if (paged && url.searchParams.get('offset') === '500') return route.fulfill({ json: { ...item, offset: 500, passage_count: 501,
  82  |       passages: [{ passage_id: `${item.document.document_version_id}-501`, location: 'Line 501', text: 'Last exact fictional line.' }] } });
  83  |     return route.fulfill({ json: item });
  84  |   });
> 85  |   await page.goto('/?case=cloud-case'); await page.getByRole('button', { name: 'Sign in securely' }).click();
      |                                                                                                      ^ Error: locator.click: Test timeout of 30000ms exceeded.
  86  |   await expect(page.getByRole('heading', { name: 'Documents', exact: true })).toBeVisible();
  87  |   return { saved, counts: () => ({ reserves, transfers }) };
  88  | }
  89  | async function upload(page: Page, text = 'Fictional original policy.') {
  90  |   await page.getByLabel('Document file', { exact: true }).setInputFiles({ name: 'policy.txt', mimeType: 'text/plain', buffer: Buffer.from(text) });
  91  |   await page.getByLabel('I confirm this document contains fictional data only.', { exact: true }).check();
  92  |   await page.getByRole('button', { name: 'Upload fictional document', exact: true }).click();
  93  | }
  94  | test('VS2-AWS-BT01 direct transfer, replacement, original download and reload', async ({ page }) => {
  95  |   const state = await fixture(page);
  96  |   await upload(page);
  97  |   await expect(page.getByRole('region', { name: 'Source evidence' })).toContainText('Fictional original policy.');
  98  |   await page.getByLabel('Replace source', { exact: true }).selectOption('source-one');
  99  |   await upload(page, 'Revised fictional policy.');
  100 |   await expect(page.getByRole('region', { name: 'Source evidence' })).toContainText('Version 2');
  101 |   await page.getByRole('button', { name: 'Inspect policy.txt version 1' }).click();
  102 |   const downloaded = page.waitForEvent('download');
  103 |   await page.getByRole('button', { name: 'Download original' }).click();
  104 |   expect((await downloaded).suggestedFilename()).toBe('policy.txt');
  105 |   await page.reload(); await page.getByRole('button', { name: 'Sign in securely' }).click();
  106 |   await expect(page.getByRole('region', { name: 'Source evidence' })).toContainText('Fictional original policy.');
  107 |   expect(state.counts()).toEqual({ reserves: 2, transfers: 2 });
  108 |   expect(state.saved).toHaveLength(2);
  109 | });
  110 | test('VS2-AWS-BT02 uncertain finalization confirms the existing upload after reload', async ({ page }) => {
  111 |   const state = await fixture(page, true);
  112 |   await upload(page);
  113 |   await expect(page.getByRole('alert')).toBeVisible();
  114 |   expect(new URL(page.url()).searchParams.get('upload')).toBe('upload-1');
  115 |   expect(await page.getByLabel('Document file', { exact: true }).evaluate((el: HTMLInputElement) => el.files?.length)).toBe(1);
  116 |   await page.reload(); await page.getByRole('button', { name: 'Sign in securely' }).click();
  117 |   await page.getByRole('button', { name: 'Check upload status' }).click();
  118 |   await expect(page.getByRole('region', { name: 'Source evidence' })).toContainText('Fictional original policy.');
  119 |   expect(state.saved).toHaveLength(1); expect(state.counts()).toEqual({ reserves: 1, transfers: 1 });
  120 | });
  121 | test('VS2-AWS-BT03 exact source pages support mobile navigation', async ({ page }) => {
  122 |   await page.setViewportSize({ width: 375, height: 812 });
  123 |   await fixture(page, false, true); await upload(page);
  124 |   await page.getByRole('button', { name: 'Next source page' }).click();
  125 |   await expect(page.getByRole('region', { name: 'Source evidence' })).toContainText('Line 501');
  126 |   await page.getByRole('button', { name: 'Previous source page' }).click();
  127 |   await expect(page.getByRole('region', { name: 'Source evidence' })).toContainText('Fictional original policy.');
  128 |   expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
  129 | });
  130 | test('VS2-AWS-BT04 expired access clears private sources and upload state', async ({ page }) => {
  131 |   await fixture(page); await upload(page);
  132 |   await expect(page.getByRole('region', { name: 'Source evidence' })).toContainText('Fictional original policy.');
  133 |   await page.route(`${api}/documents`, route => route.fulfill({ status: 401, json: { message: 'Sign in.' } }));
  134 |   await page.getByRole('button', { name: 'Refresh documents' }).click();
  135 |   await expect(page.getByRole('button', { name: 'Sign in securely' })).toBeVisible();
  136 |   await expect(page.getByRole('heading', { name: 'Documents', exact: true })).toHaveCount(0);
  137 | });
  138 |
  139 | test('VS2-AWS-BT02 failed S3 transfer resumes the same reserved upload', async ({ page }) => {
  140 |   const state = await fixture(page, false, false, true);
  141 |   await upload(page);
  142 |   await expect(page.getByRole('alert')).toBeVisible();
  143 |   await page.getByRole('button', { name: 'Check upload status' }).click();
  144 |   await expect(page.getByRole('status')).toContainText('unfinished');
  145 |   await page.getByRole('button', { name: 'Resume upload' }).click();
  146 |   await expect(page.getByRole('region', { name: 'Source evidence' })).toContainText('Fictional original policy.');
  147 |   expect(state.saved).toHaveLength(1);
  148 |   expect(state.saved[0].document.document_version_id).toBe('upload-1');
  149 |   expect(state.counts()).toEqual({ reserves: 2, transfers: 2 });
  150 | });
  151 |
  152 | test('VS2-AWS-BT02 unfinished reservation can be cancelled without showing a saved source', async ({ page }) => {
  153 |   const state = await fixture(page, false, false, true);
  154 |   await upload(page);
  155 |   await expect(page.getByRole('alert')).toBeVisible();
  156 |   await page.getByRole('button', { name: 'Cancel unfinished upload' }).click();
  157 |   await expect(page.getByRole('status')).toContainText('not saved');
  158 |   await expect(page.getByRole('button', { name: 'Upload fictional document', exact: true })).toBeEnabled();
  159 |   expect(state.saved).toHaveLength(0);
  160 | });
  161 |
```
