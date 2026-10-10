# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: cases.spec.ts >> VS1-BT04 delayed case list preserves keyboard focus during form entry
- Location: tests\cases.spec.ts:166:1

# Error details

```
Error: expect(locator).toBeFocused() failed

Locator:  getByLabel('I confirm this case contains fictional data only.', { exact: true })
Expected: focused
Received: inactive
Timeout:  5000ms

Call log:
  - Expect "toBeFocused" getByLabel('I confirm this case contains fictional data only.', { exact: true }) with timeout 5000ms
  - waiting for getByLabel('I confirm this case contains fictional data only.', { exact: true })
    14 × locator resolved to <input type="checkbox"/>
       - unexpected value "inactive"

```

```yaml
- checkbox "I confirm this case contains fictional data only."
```

# Test source

```ts
  84  |     } else await route.continue();
  85  |   });
  86  |   await fillCase(page, 'Fictional failed save');
  87  |   await page.getByRole('button', { name: 'Save fictional case' }).click();
  88  |   await expect(page.getByRole('alert')).toContainText('could not be confirmed');
  89  |   await expect(page.getByLabel('Fictional bank name')).toHaveValue('Fictional failed save');
  90  |   await expect(page.getByText('Case saved', { exact: true })).toHaveCount(0);
  91  |   await expect(page.getByRole('button', { name: 'Save fictional case' })).toBeDisabled();
  92  |   await page.getByRole('button', { name: 'Check saved cases' }).click();
  93  |   await expect(page.getByRole('button', { name: 'Save fictional case' })).toBeEnabled();
  94  | });
  95  |
  96  | test('VS1-BT02 save is disabled in flight and uncertain transport needs a list check', async ({ page }) => {
  97  |   await signIn(page);
  98  |   let posts = 0;
  99  |   let release: () => void = () => {};
  100 |   const gate = new Promise<void>(resolve => { release = resolve; });
  101 |   await page.route(api, async route => {
  102 |     if (route.request().method() !== 'POST') return route.continue();
  103 |     posts++;
  104 |     await gate;
  105 |     await route.abort();
  106 |   });
  107 |   await fillCase(page, 'Fictional uncertain save');
  108 |   await page.getByRole('button', { name: 'Save fictional case' }).click();
  109 |   await expect(page.getByRole('button', { name: 'Saving case…' })).toBeDisabled();
  110 |   release();
  111 |   await expect(page.getByRole('alert')).toContainText('Check saved cases');
  112 |   await expect(page.getByRole('button', { name: 'Save fictional case' })).toBeDisabled();
  113 |   expect(posts).toBe(1);
  114 | });
  115 |
  116 | test('VS1-BT02 expired session clears case data and returns to sign in', async ({ page }) => {
  117 |   await signIn(page);
  118 |   await page.route(api, route => route.fulfill({ status: 401, json: { code: 'unauthorized', message: 'Sign in.', next_action: 'Sign in.', correlation_id: 'test-401' } }));
  119 |   await page.getByRole('button', { name: 'Refresh cases' }).click();
  120 |   await expect(page.getByRole('alert')).toContainText('session ended');
  121 |   await expect(page.getByRole('button', { name: 'Continue with local identity' })).toBeVisible();
  122 |   await expect(page.getByRole('heading', { name: 'Your cases' })).toHaveCount(0);
  123 | });
  124 |
  125 | test('VS1-BT02 unavailable or denied case provides return navigation', async ({ page }) => {
  126 |   await signIn(page);
  127 |   await fillCase(page, `Fictional denied case ${Date.now()}`);
  128 |   await page.getByRole('button', { name: 'Save fictional case' }).click();
  129 |   await expect(page.getByRole('button', { name: 'Back to cases' })).toBeVisible();
  130 |   const caseUrl = page.url();
  131 |   await page.route(`${api}/*`, route => route.fulfill({ status: 404, json: { code: 'not_found', message: 'Unavailable.', next_action: 'Return to cases.', correlation_id: 'test-404' } }));
  132 |   await page.goto(caseUrl);
  133 |   await page.getByRole('button', { name: 'Continue with local identity' }).click();
  134 |   await expect(page.getByRole('alert')).toContainText('not available');
  135 |   await page.getByRole('button', { name: 'Back to cases' }).click();
  136 |   await expect(page.getByRole('heading', { name: 'Your cases' })).toBeVisible();
  137 | });
  138 |
  139 | test('VS1-BT03 narrow viewport and keyboard complete the saved case flow', async ({ page }) => {
  140 |   await page.setViewportSize({ width: 375, height: 812 });
  141 |   await page.goto('/');
  142 |   await page.getByRole('button', { name: 'Continue with local identity' }).focus();
  143 |   await page.keyboard.press('Enter');
  144 |   await expect(page.getByRole('heading', { name: 'Your cases' })).toBeVisible();
  145 |   const name = `Fictional keyboard bank ${Date.now()}`;
  146 |   await page.getByLabel('Fictional bank name').focus();
  147 |   await page.keyboard.type(name);
  148 |   await page.keyboard.press('Tab');
  149 |   await expect(page.getByLabel('I confirm this case contains fictional data only.')).toBeFocused();
  150 |   await page.keyboard.press('Space');
  151 |   await page.keyboard.press('Tab');
  152 |   await expect(page.getByRole('button', { name: 'Save fictional case' })).toBeFocused();
  153 |   await page.keyboard.press('Enter');
  154 |   await expect(page.getByRole('heading', { name })).toBeVisible();
  155 |   expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true);
  156 |   await page.screenshot({ path: `${process.env.BROWSER_EVIDENCE_DIR || '../../runs/2026-10-10-autonomous-build'}/frontend-mobile.png`, fullPage: true });
  157 | });
  158 |
  159 | test('VS1 authentication configuration fails closed without Cognito settings', async ({ page }) => {
  160 |   await page.route('**/config.json', route => route.fulfill({ json: { mode: 'aws', api_url: 'https://api.example.test' } }));
  161 |   await page.goto('/');
  162 |   await expect(page.getByRole('alert')).toContainText('configuration');
  163 |   await expect(page.getByRole('button', { name: 'Continue with local identity' })).toHaveCount(0);
  164 | });
  165 |
  166 | test('VS1-BT04 delayed case list preserves keyboard focus during form entry', async ({ page }) => {
  167 |   let release!: () => void;
  168 |   const delayed = new Promise<void>(resolve => { release = resolve; });
  169 |   await page.route(api, async route => {
  170 |     if (route.request().method() !== 'GET') return route.fallback();
  171 |     await delayed;
  172 |     return route.fulfill({ json: { cases: [] } });
  173 |   });
  174 |   await signIn(page);
  175 |   await expect(page.getByText('Loading your cases…', { exact: true })).toBeVisible();
  176 |   const name = `Fictional delayed keyboard bank ${Date.now()}`;
  177 |   await page.getByLabel('Fictional bank name').focus();
  178 |   await page.keyboard.type(name);
  179 |   await page.keyboard.press('Tab');
  180 |   const checkbox = page.getByLabel('I confirm this case contains fictional data only.', { exact: true });
  181 |   await expect(checkbox).toBeFocused();
  182 |   release();
  183 |   await expect(page.getByText('Loading your cases…', { exact: true })).toHaveCount(0);
> 184 |   await expect(checkbox).toBeFocused();
      |                          ^ Error: expect(locator).toBeFocused() failed
  185 |   await page.keyboard.press('Space');
  186 |   await page.keyboard.press('Tab');
  187 |   await expect(page.getByRole('button', { name: 'Save fictional case', exact: true })).toBeFocused();
  188 |   await page.keyboard.press('Enter');
  189 |   await expect(page.getByRole('heading', { name, exact: true })).toBeVisible();
  190 | });
  191 |
  192 | test('VS1 AWS mode never fabricates a local signed-in session', async ({ page }) => {
  193 |   await page.route('**/config.json', route => route.fulfill({ json: { mode: 'aws', api_url: 'https://api.example.test',
  194 |     cognito_domain: 'https://demo.auth.ap-south-1.amazoncognito.com', user_pool_client_id: 'test-client', redirect_uri: `${testWeb}/` } }));
  195 |   await page.goto('/');
  196 |   await expect(page.getByRole('button', { name: 'Sign in securely' })).toBeVisible();
  197 |   await expect(page.getByRole('button', { name: 'Continue with local identity' })).toHaveCount(0);
  198 |   expect(await page.evaluate(() => localStorage.length)).toBe(0);
  199 |   await page.reload();
  200 |   await expect(page.getByRole('button', { name: 'Sign in securely' })).toBeVisible();
  201 | });
  202 |
  203 | test('VS1 callback state mismatch is rejected and temporary values are removed', async ({ page }) => {
  204 |   await page.route('**/config.json', route => route.fulfill({ json: { mode: 'aws', api_url: 'https://api.example.test',
  205 |     cognito_domain: 'https://demo.auth.ap-south-1.amazoncognito.com', user_pool_client_id: 'test-client', redirect_uri: `${testWeb}/` } }));
  206 |   await page.addInitScript(() => sessionStorage.setItem('regulatory-agent.pkce', JSON.stringify({ state: 'expected-state', verifier: 'fictional-verifier' })));
  207 |   await page.goto('/?code=fictional-code&state=wrong-state');
  208 |   await expect(page.getByRole('alert')).toContainText('Sign-in could not be completed');
  209 |   expect(new URL(page.url()).search).toBe('');
  210 |   expect(await page.evaluate(() => sessionStorage.length)).toBe(0);
  211 |   expect(await page.evaluate(() => localStorage.length)).toBe(0);
  212 | });
  213 |
  214 | test('VS1 malformed configuration also clears an OAuth callback', async ({ page }) => {
  215 |   await page.route('**/config.json', route => route.fulfill({ json: { mode: 'aws', api_url: 'https://api.example.test' } }));
  216 |   await page.addInitScript(() => sessionStorage.setItem('regulatory-agent.pkce', JSON.stringify({ state: 'expected-state', verifier: 'fictional-verifier' })));
  217 |   await page.goto('/?code=fictional-code&state=expected-state');
  218 |   await expect(page.getByRole('alert')).toContainText('configuration');
  219 |   expect(new URL(page.url()).search).toBe('');
  220 |   expect(await page.evaluate(() => sessionStorage.length)).toBe(0);
  221 | });
  222 |
  223 | test('VS1-BT01 cloud sign-in returns to the selected case after a reload', async ({ page }) => {
  224 |   const record = { case_id: 'feedback-case.1', owner_id: 'fictional-operator',
  225 |     bank_profile: { name: 'Fictional returning reviewer bank' }, synthetic: true,
  226 |     created_at: '2026-10-10T12:00:00Z' };
  227 |   const identity = 'https://demo.auth.ap-south-1.amazoncognito.com';
  228 |   await page.route('**/config.json', route => route.fulfill({ json: { mode: 'aws', api_url: 'https://api.example.test',
  229 |     cognito_domain: identity, user_pool_client_id: 'test-client', redirect_uri: `${testWeb}/` } }));
  230 |   await page.route(`${identity}/**`, route => {
  231 |     const url = new URL(route.request().url());
  232 |     if (url.pathname === '/oauth2/authorize') {
  233 |       const callback = new URL(`${testWeb}/`);
  234 |       callback.searchParams.set('code', 'fictional-code');
  235 |       callback.searchParams.set('state', url.searchParams.get('state')!);
  236 |       return route.fulfill({ status: 302, headers: { location: callback.href } });
  237 |     }
  238 |     if (url.pathname === '/oauth2/token') return route.fulfill({ json: {
  239 |       access_token: 'fictional-access-token', token_type: 'Bearer', expires_in: 900,
  240 |     } });
  241 |     return route.abort();
  242 |   });
  243 |   await page.route('https://api.example.test/api/cases', route => route.fulfill({ json: { cases: [record] } }));
  244 |   await page.route(`https://api.example.test/api/cases/${record.case_id}`, route => route.fulfill({ json: record }));
  245 |   await page.goto(`/?case=${record.case_id}`);
  246 |   for (let attempt = 0; attempt < 2; attempt++) {
  247 |     await page.getByRole('button', { name: 'Sign in securely' }).click();
  248 |     await expect(page.getByRole('heading', { name: record.bank_profile.name, level: 1 })).toBeVisible();
  249 |     expect(new URL(page.url()).searchParams.get('case')).toBe(record.case_id);
  250 |     expect(new URL(page.url()).searchParams.has('code')).toBe(false);
  251 |     expect(await page.evaluate(() => localStorage.length === 0 && sessionStorage.length === 0)).toBe(true);
  252 |     if (attempt === 0) await page.reload();
  253 |   }
  254 | });
  255 |
  256 | test('VS1 case resume rejects a return URL before exchanging a sign-in code', async ({ page }) => {
  257 |   const state = 'fictional-state.https://untrusted.example/';
  258 |   let tokenRequests = 0;
  259 |   await page.route('**/config.json', route => route.fulfill({ json: { mode: 'aws', api_url: 'https://api.example.test',
  260 |     cognito_domain: 'https://demo.auth.ap-south-1.amazoncognito.com', user_pool_client_id: 'test-client', redirect_uri: `${testWeb}/` } }));
  261 |   await page.route('https://demo.auth.ap-south-1.amazoncognito.com/**', route => { tokenRequests++; return route.abort(); });
  262 |   await page.addInitScript(value => sessionStorage.setItem('regulatory-agent.pkce', JSON.stringify({
  263 |     state: value, verifier: 'fictional-verifier',
  264 |   })), state);
  265 |   await page.goto(`/?code=fictional-code&state=${encodeURIComponent(state)}`);
  266 |   await expect(page.getByRole('alert')).toContainText('Sign-in could not be completed');
  267 |   expect(new URL(page.url()).origin).toBe(testWeb);
  268 |   expect(new URL(page.url()).search).toBe('');
  269 |   expect(await page.evaluate(() => sessionStorage.length)).toBe(0);
  270 |   expect(tokenRequests).toBe(0);
  271 | });
  272 |
```
