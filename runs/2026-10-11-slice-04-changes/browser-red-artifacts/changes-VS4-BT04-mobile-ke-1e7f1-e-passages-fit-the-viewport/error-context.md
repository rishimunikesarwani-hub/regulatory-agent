# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: changes.spec.ts >> VS4-BT04 mobile keyboard controls and source passages fit the viewport
- Location: tests\changes.spec.ts:79:1

# Error details

```
Test timeout of 7000ms exceeded.
```

```
Error: locator.selectOption: Test timeout of 7000ms exceeded.
Call log:
  - waiting for getByLabel('Regulatory source', { exact: true })

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
    - generic [ref=e8]:
      - generic [ref=e9]: Local development
      - button "Sign out" [ref=e10] [cursor=pointer]
  - main [ref=e11]:
    - button "← Back to cases" [ref=e12] [cursor=pointer]
    - status [ref=e13]: Case saved
    - generic [ref=e14]:
      - generic [ref=e15]:
        - generic [ref=e16]: Synthetic demo
        - heading "Fictional version bank 1791686896503" [level=1] [ref=e17]
        - paragraph [ref=e18]: Your fictional bank profile is saved.
      - generic [ref=e19]: Not started
    - generic [ref=e20]:
      - heading "Case details" [level=2] [ref=e21]
      - generic [ref=e22]:
        - generic [ref=e23]:
          - term [ref=e24]: Bank profile
          - definition [ref=e25]: Fictional version bank 1791686896503
        - generic [ref=e26]:
          - term [ref=e27]: Data type
          - definition [ref=e28]: Fictional data
        - generic [ref=e29]:
          - term [ref=e30]: Created
          - definition [ref=e31]: 10/11/2026, 8:18:16 AM
        - generic [ref=e32]:
          - term [ref=e33]: Case ID
          - definition [ref=e34]: 3bea480931dc4a3d91cfaf38bc230124
    - generic [ref=e35]:
      - region [ref=e36]:
        - generic [ref=e37]:
          - generic [ref=e38]:
            - paragraph [ref=e39]: SOURCE DOCUMENTS
            - heading "Documents" [level=2] [ref=e40]
            - paragraph [ref=e41]: Keep the original file and inspect its extracted text.
          - button "Refresh documents" [ref=e42] [cursor=pointer]
        - status [ref=e43]: Document saved. Earlier versions remain available.
        - generic [ref=e44]:
          - generic [ref=e45]:
            - region [ref=e46]:
              - heading "Upload a fictional document" [level=3] [ref=e47]
              - paragraph [ref=e48]: Text PDF, DOCX, TXT, or CSV. Maximum 10 MB per file and 10 saved versions per case.
              - group [ref=e50]:
                - generic [ref=e51]: Document file
                - button "Document file" [ref=e52]
                - generic [ref=e53]: Document role
                - combobox "Document role" [ref=e54]:
                  - option "Bank profile"
                  - option "Policy" [selected]
                  - option "Control"
                  - option "Evidence"
                - generic [ref=e55]: Replace source
                - combobox "Replace source" [ref=e56]:
                  - option "New source" [selected]
                  - option "policy.txt"
                - paragraph [ref=e57]: A replacement adds a version. It keeps the earlier version.
                - generic [ref=e58]:
                  - checkbox "I confirm this document contains fictional data only." [ref=e59]
                  - generic [ref=e60]: I confirm this document contains fictional data only.
                - button "Upload fictional document" [disabled] [ref=e61]
            - region [ref=e62]:
              - heading "Saved versions 1" [level=3] [ref=e63]
              - button "Inspect policy.txt version 1" [pressed] [ref=e64] [cursor=pointer]:
                - strong [ref=e65]: policy.txt
                - generic [ref=e66]: policy · Version 1 · TXT
          - region [ref=e67]:
            - heading "Source evidence" [level=3] [ref=e68]
            - generic [ref=e69]:
              - generic [ref=e70]:
                - heading "policy.txt" [level=3] [ref=e71]
                - paragraph [ref=e72]: Version 1 · policy · TXT
              - button "Download original" [ref=e73] [cursor=pointer]
            - paragraph [ref=e74]: Extracted text can omit images and visual table structure. Use the original file to check them.
            - paragraph [ref=e75]: "Version ID: 810c04ead63b42cbb9896abbda4e524b"
            - group [ref=e76]:
              - generic "Content hash (SHA-256)" [ref=e77]
            - generic [ref=e78]:
              - article [ref=e79]:
                - heading "Line 1" [level=4] [ref=e80]
                - generic [ref=e81]: Synthetic demo. Fictional bank policy.
              - article [ref=e82]:
                - heading "Line 2" [level=4] [ref=e83]
                - generic [ref=e84]: Control ACCESS-01 requires supervision of privileged sessions, complete activity logging, and a weekly review.
              - article [ref=e85]:
                - heading "Line 3" [level=4] [ref=e86]
                - generic [ref=e87]: Weekly timing is bank policy, not an RBI-specified interval.
      - region [ref=e88]:
        - generic [ref=e89]:
          - generic [ref=e90]:
            - paragraph [ref=e91]: HISTORICAL EXAMPLE
            - heading "Assessment" [level=2] [ref=e92]
            - paragraph [ref=e93]: Review one fictional policy against RBI clause 19(b).
          - button "Refresh assessment" [ref=e94] [cursor=pointer]
        - generic [ref=e95]:
          - paragraph [ref=e96]: Use the supplied fictional policy. Other documents cannot run this controlled example.
          - paragraph [ref=e97]:
            - link "Download the fictional policy" [ref=e98] [cursor=pointer]:
              - /url: data:text/plain;charset=utf-8,…
            - text: ", then upload it as a policy document."
          - generic [ref=e99]: Policy version
          - combobox "Policy version" [ref=e100]:
            - option "Upload a fictional policy first"
            - option "policy.txt · Version 1" [selected]
          - paragraph [ref=e101]: "Historical date: 8 April 2024. Current regulatory status is unverified. No live model call is made."
          - button "Run controlled assessment" [ref=e102] [cursor=pointer]
          - paragraph [ref=e103]: No assessment has run.
  - contentinfo [ref=e104]: Fictional case workspace · Development release
```

# Test source

```ts
  1  | import { expect, test, type Page } from '@playwright/test';
  2  | import { readFileSync } from 'node:fs';
  3  | const evidence = process.env.BROWSER_EVIDENCE_DIR || '../../runs/2026-10-11-slice-04-changes';
  4  |
  5  | async function baseline(page: Page) {
  6  |   await page.goto('/');
  7  |   expect((await (await page.request.get('/config.json')).json()).api_url).toBe(process.env.LOCAL_TEST_API_URL);
  8  |   await page.getByRole('button', {name: 'Continue with local identity'}).click();
  9  |   await page.getByLabel('Fictional bank name').fill(`Fictional version bank ${Date.now()}`);
  10 |   await page.getByLabel('I confirm this case contains fictional data only.', {exact: true}).check();
  11 |   await page.getByRole('button', {name: 'Save fictional case'}).click();
  12 |   await page.getByLabel('Document file', {exact: true}).setInputFiles({name: 'policy.txt', mimeType: 'text/plain', buffer: readFileSync('../../data/fixtures/slice-02-policy.txt')});
  13 |   await page.getByLabel('I confirm this document contains fictional data only.', {exact: true}).check();
  14 |   await page.getByRole('button', {name: 'Upload fictional document', exact: true}).click();
> 15 |   await page.getByLabel('Regulatory source', {exact: true}).selectOption('SIM-ACCESS');
     |                                                             ^ Error: locator.selectOption: Test timeout of 7000ms exceeded.
  16 |   await page.getByRole('button', {name: 'Run controlled assessment', exact: true}).click();
  17 |   const result = page.getByRole('region', {name: 'Assessment result', exact: true});
  18 |   await expect(result).toContainText('Privileged sessions must be logged and reviewed each week.');
  19 |   await page.getByRole('button', {name: 'Save review', exact: true}).click();
  20 |   await expect(result).toContainText('Approved · Revision 1');
  21 |   return {result, changes: page.getByRole('region', {name: 'Regulatory changes', exact: true}), original: page.url()};
  22 | }
  23 |
  24 | test('VS4-BT01 added requirement creates an independent review and preserves the original', async ({page}) => {
  25 |   const {result, changes, original} = await baseline(page);
  26 |   await changes.getByRole('button', {name: 'Compare versions', exact: true}).click();
  27 |   await expect(changes).toContainText('Added requirement');
  28 |   await expect(changes).toContainText('Affected control: ACCESS-01');
  29 |   await expect(changes).toContainText('A separate reviewer must approve each weekly review.');
  30 |   await expect(result).toContainText('Approved · Revision 1');
  31 |   await changes.getByRole('button', {name: 'Open new assessment', exact: true}).click();
  32 |   await expect(result).toContainText('Approved: 0');
  33 |   await expect(result).toContainText('Pending: 1');
  34 |   await expect(result).not.toContainText('Approved · Revision 1');
  35 |   expect(page.url()).not.toBe(original);
  36 |   await result.getByRole('button', {name: 'Inspect Simulated clause 1', exact: true}).click();
  37 |   await expect(page.getByRole('dialog')).toContainText('Synthetic regulatory simulation');
  38 |   await page.getByRole('button', {name: 'Close source', exact: true}).click();
  39 |   await page.getByLabel('Rejected', {exact: true}).check();
  40 |   await page.getByLabel('Review reason', {exact: true}).fill('Separate approval evidence is missing.');
  41 |   await page.getByRole('button', {name: 'Save review', exact: true}).click();
  42 |   await expect(result).toContainText('Rejected · Revision 1');
  43 |   await changes.getByRole('button', {name: 'Open previous assessment', exact: true}).click();
  44 |   await expect(result).toContainText('Approved · Revision 1');
  45 |   await expect(result).not.toContainText('Rejected · Revision 1');
  46 |   await page.screenshot({path: `${evidence}/changes-desktop.png`, fullPage: true});
  47 | });
  48 |
  49 | test('VS4-BT02 wording and cosmetic changes preserve the original review', async ({page}) => {
  50 |   const {result, changes, original} = await baseline(page);
  51 |   for (const [version, title] of [['v2-cosmetic', 'Appearance only'], ['v2-replaced', 'Wording only']]) {
  52 |     await changes.getByLabel('Newer version', {exact: true}).selectOption(version);
  53 |     await changes.getByRole('button', {name: 'Compare versions', exact: true}).click();
  54 |     await expect(changes).toContainText(title);
  55 |     await expect(changes).toContainText('No changed requirement in this fixed simulation.');
  56 |     await expect(changes.getByRole('button', {name: 'Open new assessment', exact: true})).toHaveCount(0);
  57 |     await expect(result).toContainText('Approved · Revision 1');
  58 |     expect(page.url()).toBe(original);
  59 |   }
  60 | });
  61 |
  62 | test('VS4-BT03 reload restores comparisons and separate review histories', async ({page}) => {
  63 |   const {result, changes} = await baseline(page);
  64 |   await changes.getByRole('button', {name: 'Compare versions', exact: true}).click();
  65 |   await changes.getByRole('button', {name: 'Open new assessment', exact: true}).click();
  66 |   await page.getByRole('button', {name: 'Save review', exact: true}).click();
  67 |   await expect(result).toContainText('Approved · Revision 1');
  68 |   const job = new URL(page.url()).searchParams.get('assessment');
  69 |   await page.reload();
  70 |   await page.getByRole('button', {name: 'Continue with local identity'}).click();
  71 |   await expect(result).toContainText('Approved · Revision 1');
  72 |   expect(new URL(page.url()).searchParams.get('assessment')).toBe(job);
  73 |   await expect(changes).toContainText('Added requirement');
  74 |   await changes.getByRole('button', {name: 'Open previous assessment', exact: true}).click();
  75 |   await expect(result).toContainText('Approved · Revision 1');
  76 |   expect(new URL(page.url()).searchParams.get('assessment')).not.toBe(job);
  77 | });
  78 |
  79 | test('VS4-BT04 mobile keyboard controls and source passages fit the viewport', async ({page}) => {
  80 |   await page.setViewportSize({width: 390, height: 844});
  81 |   const {changes} = await baseline(page);
  82 |   const candidate = changes.getByLabel('Newer version', {exact: true});
  83 |   await candidate.focus();
  84 |   await expect(candidate).toBeFocused();
  85 |   await page.keyboard.press('Tab');
  86 |   await expect(changes.getByRole('button', {name: 'Compare versions', exact: true})).toBeFocused();
  87 |   await page.keyboard.press('Enter');
  88 |   await expect(changes).toContainText('Added requirement');
  89 |   expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBeTruthy();
  90 |   await page.screenshot({path: `${evidence}/changes-mobile.png`, fullPage: true});
  91 | });
  92 |
```
