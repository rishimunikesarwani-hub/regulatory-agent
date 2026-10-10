import { expect, test, type Page } from '@playwright/test';

const testApi = process.env.LOCAL_TEST_API_URL || 'http://127.0.0.1:8110';
const api = `${testApi}/api/cases`;

test.beforeEach(async ({ page }) => {
  if (process.env.LOCAL_TEST_API_URL) {
    await page.route('**/config.json', route => route.fulfill({ json: { mode: 'local', api_url: testApi } }));
  }
});

async function signIn(page: Page) {
  await page.goto('/');
  await expect(page.getByText('Local development', { exact: true })).toBeVisible();
  await page.getByRole('button', { name: 'Continue with local identity' }).click();
  await expect(page.getByRole('heading', { name: 'Your cases' })).toBeVisible();
}

test('VS1-BT03 requested sign-in stays centered on desktop and mobile', async ({ page }) => {
  for (const viewport of [{ width: 1440, height: 900 }, { width: 375, height: 812 }]) {
    await page.setViewportSize(viewport);
    await page.goto('/');
    await expect(page).toHaveTitle('The Regulator');
    await expect(page.locator('.brand')).toHaveText('RThe Regulator');
    const panel = page.locator('.sign-in-panel');
    await expect(panel.getByRole('heading', { name: 'Sign in to continue', level: 1 })).toBeVisible();
    await expect(panel.getByRole('button', { name: 'Continue with local identity' })).toBeVisible();
    await expect(panel.locator('p, .small-label')).toHaveCount(0);
    await expect(page.getByText('A clear starting point', { exact: false })).toHaveCount(0);
    const bounds = await panel.boundingBox();
    expect(bounds).not.toBeNull();
    expect(Math.abs(bounds!.x + bounds!.width / 2 - viewport.width / 2)).toBeLessThan(2);
    expect(Math.abs(bounds!.y + bounds!.height / 2 - viewport.height / 2)).toBeLessThan(40);
    await page.screenshot({ path: `../../runs/2026-10-10-slice-01-feedback/sign-in-${viewport.width > 767 ? 'desktop' : 'mobile'}.png` });
  }
});

async function fillCase(page: Page, name: string) {
  await page.getByLabel('Fictional bank name').fill(name);
  await page.getByLabel('I confirm this case contains fictional data only.').check();
}

test('VS1-BT01 sign in, create, leave, reopen and reload a real saved case', async ({ page }) => {
  const name = `Browser fictional bank ${Date.now()}`;
  const errors: string[] = [];
  page.on('pageerror', error => errors.push(error.message));
  await signIn(page);
  await fillCase(page, name);
  await page.getByRole('button', { name: 'Save fictional case' }).click();
  await expect(page.getByRole('heading', { name })).toBeVisible();
  await expect(page.getByText('Case saved', { exact: true })).toBeVisible();
  await expect(page.getByText('Not started', { exact: true })).toBeVisible();
  await page.screenshot({ path: '../../runs/2026-10-10-autonomous-build/frontend-desktop.png', fullPage: true });
  await page.getByRole('button', { name: 'Back to cases' }).click();
  await page.getByRole('button', { name: `Open ${name}`, exact: true }).click();
  await expect(page.getByRole('heading', { name })).toBeVisible();
  await page.reload();
  await page.getByRole('button', { name: 'Continue with local identity' }).click();
  await expect(page.getByRole('heading', { name })).toBeVisible();
  await expect.poll(() => errors).toEqual([]);
});

test('VS1-BT02 empty and loading states have a clear action', async ({ page }) => {
  let release: () => void = () => {};
  const gate = new Promise<void>(resolve => { release = resolve; });
  await page.route(api, async route => {
    await gate;
    await route.fulfill({ json: { cases: [] } });
  });
  await page.goto('/');
  await page.getByRole('button', { name: 'Continue with local identity' }).click();
  await expect(page.getByRole('status')).toContainText('Loading your cases');
  release();
  await expect(page.getByText('No cases yet', { exact: true })).toBeVisible();
  await expect(page.getByLabel('Fictional bank name')).toBeVisible();
});

test('VS1-BT02 failed save keeps the draft and never shows success', async ({ page }) => {
  await signIn(page);
  await page.route(api, async route => {
    if (route.request().method() === 'POST') {
      await route.fulfill({ status: 503, json: { code: 'save_failed', message: 'Could not save.', next_action: 'Try again.', correlation_id: 'test-save' } });
    } else await route.continue();
  });
  await fillCase(page, 'Fictional failed save');
  await page.getByRole('button', { name: 'Save fictional case' }).click();
  await expect(page.getByRole('alert')).toContainText('could not be confirmed');
  await expect(page.getByLabel('Fictional bank name')).toHaveValue('Fictional failed save');
  await expect(page.getByText('Case saved', { exact: true })).toHaveCount(0);
  await expect(page.getByRole('button', { name: 'Save fictional case' })).toBeDisabled();
  await page.getByRole('button', { name: 'Check saved cases' }).click();
  await expect(page.getByRole('button', { name: 'Save fictional case' })).toBeEnabled();
});

test('VS1-BT02 save is disabled in flight and uncertain transport needs a list check', async ({ page }) => {
  await signIn(page);
  let posts = 0;
  let release: () => void = () => {};
  const gate = new Promise<void>(resolve => { release = resolve; });
  await page.route(api, async route => {
    if (route.request().method() !== 'POST') return route.continue();
    posts++;
    await gate;
    await route.abort();
  });
  await fillCase(page, 'Fictional uncertain save');
  await page.getByRole('button', { name: 'Save fictional case' }).click();
  await expect(page.getByRole('button', { name: 'Saving case…' })).toBeDisabled();
  release();
  await expect(page.getByRole('alert')).toContainText('Check saved cases');
  await expect(page.getByRole('button', { name: 'Save fictional case' })).toBeDisabled();
  expect(posts).toBe(1);
});

test('VS1-BT02 expired session clears case data and returns to sign in', async ({ page }) => {
  await signIn(page);
  await page.route(api, route => route.fulfill({ status: 401, json: { code: 'unauthorized', message: 'Sign in.', next_action: 'Sign in.', correlation_id: 'test-401' } }));
  await page.getByRole('button', { name: 'Refresh cases' }).click();
  await expect(page.getByRole('alert')).toContainText('session ended');
  await expect(page.getByRole('button', { name: 'Continue with local identity' })).toBeVisible();
  await expect(page.getByRole('heading', { name: 'Your cases' })).toHaveCount(0);
});

test('VS1-BT02 unavailable or denied case provides return navigation', async ({ page }) => {
  await signIn(page);
  await fillCase(page, `Fictional denied case ${Date.now()}`);
  await page.getByRole('button', { name: 'Save fictional case' }).click();
  await expect(page.getByRole('button', { name: 'Back to cases' })).toBeVisible();
  const caseUrl = page.url();
  await page.route(`${api}/*`, route => route.fulfill({ status: 404, json: { code: 'not_found', message: 'Unavailable.', next_action: 'Return to cases.', correlation_id: 'test-404' } }));
  await page.goto(caseUrl);
  await page.getByRole('button', { name: 'Continue with local identity' }).click();
  await expect(page.getByRole('alert')).toContainText('not available');
  await page.getByRole('button', { name: 'Back to cases' }).click();
  await expect(page.getByRole('heading', { name: 'Your cases' })).toBeVisible();
});

test('VS1-BT03 narrow viewport and keyboard complete the saved case flow', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 812 });
  await page.goto('/');
  await page.getByRole('button', { name: 'Continue with local identity' }).focus();
  await page.keyboard.press('Enter');
  await expect(page.getByRole('heading', { name: 'Your cases' })).toBeVisible();
  const name = `Fictional keyboard bank ${Date.now()}`;
  await page.getByLabel('Fictional bank name').focus();
  await page.keyboard.type(name);
  await page.keyboard.press('Tab');
  await expect(page.getByLabel('I confirm this case contains fictional data only.')).toBeFocused();
  await page.keyboard.press('Space');
  await page.keyboard.press('Tab');
  await expect(page.getByRole('button', { name: 'Save fictional case' })).toBeFocused();
  await page.keyboard.press('Enter');
  await expect(page.getByRole('heading', { name })).toBeVisible();
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true);
  await page.screenshot({ path: '../../runs/2026-10-10-autonomous-build/frontend-mobile.png', fullPage: true });
});

test('VS1 authentication configuration fails closed without Cognito settings', async ({ page }) => {
  await page.route('**/config.json', route => route.fulfill({ json: { mode: 'aws', api_url: 'https://api.example.test' } }));
  await page.goto('/');
  await expect(page.getByRole('alert')).toContainText('configuration');
  await expect(page.getByRole('button', { name: 'Continue with local identity' })).toHaveCount(0);
});

test('VS1 AWS mode never fabricates a local signed-in session', async ({ page }) => {
  await page.route('**/config.json', route => route.fulfill({ json: { mode: 'aws', api_url: 'https://api.example.test',
    cognito_domain: 'https://demo.auth.ap-south-1.amazoncognito.com', user_pool_client_id: 'test-client', redirect_uri: 'http://127.0.0.1:5173/' } }));
  await page.goto('/');
  await expect(page.getByRole('button', { name: 'Sign in securely' })).toBeVisible();
  await expect(page.getByRole('button', { name: 'Continue with local identity' })).toHaveCount(0);
  expect(await page.evaluate(() => localStorage.length)).toBe(0);
  await page.reload();
  await expect(page.getByRole('button', { name: 'Sign in securely' })).toBeVisible();
});

test('VS1 callback state mismatch is rejected and temporary values are removed', async ({ page }) => {
  await page.route('**/config.json', route => route.fulfill({ json: { mode: 'aws', api_url: 'https://api.example.test',
    cognito_domain: 'https://demo.auth.ap-south-1.amazoncognito.com', user_pool_client_id: 'test-client', redirect_uri: 'http://127.0.0.1:5173/' } }));
  await page.addInitScript(() => sessionStorage.setItem('regulatory-agent.pkce', JSON.stringify({ state: 'expected-state', verifier: 'fictional-verifier' })));
  await page.goto('/?code=fictional-code&state=wrong-state');
  await expect(page.getByRole('alert')).toContainText('Sign-in could not be completed');
  expect(new URL(page.url()).search).toBe('');
  expect(await page.evaluate(() => sessionStorage.length)).toBe(0);
  expect(await page.evaluate(() => localStorage.length)).toBe(0);
});

test('VS1 malformed configuration also clears an OAuth callback', async ({ page }) => {
  await page.route('**/config.json', route => route.fulfill({ json: { mode: 'aws', api_url: 'https://api.example.test' } }));
  await page.addInitScript(() => sessionStorage.setItem('regulatory-agent.pkce', JSON.stringify({ state: 'expected-state', verifier: 'fictional-verifier' })));
  await page.goto('/?code=fictional-code&state=expected-state');
  await expect(page.getByRole('alert')).toContainText('configuration');
  expect(new URL(page.url()).search).toBe('');
  expect(await page.evaluate(() => sessionStorage.length)).toBe(0);
});

test('VS1-BT01 cloud sign-in returns to the selected case after a reload', async ({ page }) => {
  const record = { case_id: 'feedback-case.1', owner_id: 'fictional-operator',
    bank_profile: { name: 'Fictional returning reviewer bank' }, synthetic: true,
    created_at: '2026-10-10T12:00:00Z' };
  const identity = 'https://demo.auth.ap-south-1.amazoncognito.com';
  await page.route('**/config.json', route => route.fulfill({ json: { mode: 'aws', api_url: 'https://api.example.test',
    cognito_domain: identity, user_pool_client_id: 'test-client', redirect_uri: 'http://127.0.0.1:5173/' } }));
  await page.route(`${identity}/**`, route => {
    const url = new URL(route.request().url());
    if (url.pathname === '/oauth2/authorize') {
      const callback = new URL('http://127.0.0.1:5173/');
      callback.searchParams.set('code', 'fictional-code');
      callback.searchParams.set('state', url.searchParams.get('state')!);
      return route.fulfill({ status: 302, headers: { location: callback.href } });
    }
    if (url.pathname === '/oauth2/token') return route.fulfill({ json: {
      access_token: 'fictional-access-token', token_type: 'Bearer', expires_in: 900,
    } });
    return route.abort();
  });
  await page.route('https://api.example.test/api/cases', route => route.fulfill({ json: { cases: [record] } }));
  await page.route(`https://api.example.test/api/cases/${record.case_id}`, route => route.fulfill({ json: record }));
  await page.goto(`/?case=${record.case_id}`);
  for (let attempt = 0; attempt < 2; attempt++) {
    await page.getByRole('button', { name: 'Sign in securely' }).click();
    await expect(page.getByRole('heading', { name: record.bank_profile.name, level: 1 })).toBeVisible();
    expect(new URL(page.url()).searchParams.get('case')).toBe(record.case_id);
    expect(new URL(page.url()).searchParams.has('code')).toBe(false);
    expect(await page.evaluate(() => localStorage.length === 0 && sessionStorage.length === 0)).toBe(true);
    if (attempt === 0) await page.reload();
  }
});

test('VS1 case resume rejects a return URL before exchanging a sign-in code', async ({ page }) => {
  const state = 'fictional-state.https://untrusted.example/';
  let tokenRequests = 0;
  await page.route('**/config.json', route => route.fulfill({ json: { mode: 'aws', api_url: 'https://api.example.test',
    cognito_domain: 'https://demo.auth.ap-south-1.amazoncognito.com', user_pool_client_id: 'test-client', redirect_uri: 'http://127.0.0.1:5173/' } }));
  await page.route('https://demo.auth.ap-south-1.amazoncognito.com/**', route => { tokenRequests++; return route.abort(); });
  await page.addInitScript(value => sessionStorage.setItem('regulatory-agent.pkce', JSON.stringify({
    state: value, verifier: 'fictional-verifier',
  })), state);
  await page.goto(`/?code=fictional-code&state=${encodeURIComponent(state)}`);
  await expect(page.getByRole('alert')).toContainText('Sign-in could not be completed');
  expect(new URL(page.url()).origin).toBe('http://127.0.0.1:5173');
  expect(new URL(page.url()).search).toBe('');
  expect(await page.evaluate(() => sessionStorage.length)).toBe(0);
  expect(tokenRequests).toBe(0);
});
