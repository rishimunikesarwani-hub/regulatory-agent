# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: changes.spec.ts >> VS4-BT02 wording and cosmetic changes preserve the original review
- Location: tests/changes.spec.ts:49:1

# Error details

```
Test timeout of 30000ms exceeded.
```

```
Error: locator.click: Test timeout of 30000ms exceeded.
Call log:
  - waiting for getByRole('button', { name: 'Save review', exact: true })

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
        - heading "Fictional version bank 1791687686323" [level=1] [ref=e17]
        - paragraph [ref=e18]: Your fictional bank profile is saved.
      - generic [ref=e19]: Controlled assessment completed
    - generic [ref=e20]:
      - heading "Case details" [level=2] [ref=e21]
      - generic [ref=e22]:
        - generic [ref=e23]:
          - term [ref=e24]: Bank profile
          - definition [ref=e25]: Fictional version bank 1791687686323
        - generic [ref=e26]:
          - term [ref=e27]: Data type
          - definition [ref=e28]: Fictional data
        - generic [ref=e29]:
          - term [ref=e30]: Created
          - definition [ref=e31]: 10/11/2026, 3:01:26 AM
        - generic [ref=e32]:
          - term [ref=e33]: Case ID
          - definition [ref=e34]: c7dca39b68a241ac91c5ac9293039106
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
            - paragraph [ref=e75]: "Version ID: b168002925ac4b6fac7e77af9dd36cf8"
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
            - paragraph [ref=e91]: CONTROLLED EXAMPLE
            - heading "Assessment" [level=2] [ref=e92]
            - paragraph [ref=e93]: Review one fictional policy against a selected historical or simulated rule.
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
          - generic [ref=e101]: Regulatory source
          - combobox "Regulatory source" [ref=e102]:
            - option "RBI clause 19(b) · historical 2023 version"
            - option "Simulated access rule · v1" [selected]
          - paragraph [ref=e103]: "Simulated date: 8 May 2024. These changes are fictional, not RBI amendments. No live model call is made."
          - button "Run controlled assessment" [ref=e104] [cursor=pointer]
          - generic [ref=e105]: Saved assessments
          - combobox "Saved assessments" [ref=e106]:
            - option "Select a saved assessment"
            - option "10/11/2026, 3:01:26 AM · 404e7673" [selected]
        - region "Regulatory changes" [ref=e107]:
          - heading "Regulatory changes" [level=2] [ref=e108]
          - generic [ref=e109]: Synthetic regulatory simulation
          - paragraph [ref=e110]: Compare specified fictional versions. Earlier assessments and human reviews stay unchanged.
          - paragraph [ref=e111]: These examples do not establish current regulatory coverage or live model quality.
          - paragraph [ref=e112]: "Older version: SIM-ACCESS:v1 · Selected assessment: 404e7673"
          - generic [ref=e113]: Newer version
          - combobox "Newer version" [ref=e114]:
            - option "v2-added · Separate reviewer approval" [selected]
            - option "v2-replaced · Same rule, different wording"
            - option "v2-cosmetic · Punctuation change"
          - button "Compare versions" [ref=e115] [cursor=pointer]
        - region "Assessment result" [ref=e116]:
          - generic [ref=e117]:
            - generic [ref=e118]: Controlled simulation
            - heading "Assessment completed" [level=3] [ref=e119]
            - paragraph [ref=e120]: This is a fixed example. It does not establish compliance or current regulatory coverage.
          - article [ref=e122]:
            - heading "Requirement and applicability" [level=3] [ref=e123]
            - paragraph [ref=e124]: Privileged sessions must be logged and reviewed each week.
            - paragraph [ref=e125]: Unverified for this fictional bank profile. Synthetic regulatory simulation.
            - heading "Conditions" [level=4] [ref=e126]
            - list [ref=e127]:
              - listitem [ref=e128]: Fictional commercial-bank rule for this simulation.
            - heading "Exceptions" [level=4] [ref=e129]
            - list
            - heading "Policy control" [level=4] [ref=e130]
            - paragraph [ref=e131]: Control ACCESS-01 requires supervision of privileged sessions, complete activity logging, and a weekly review.
            - paragraph [ref=e132]: Weekly timing belongs to the fictional policy and simulated rule.
            - button "Inspect Simulated clause 1" [ref=e134] [cursor=pointer]
          - generic [ref=e135]:
            - heading "Saved review outcomes" [level=3] [ref=e136]
            - paragraph [ref=e137]: "Approved: 0 · Edited: 0 · Rejected: 0 · Pending: 0"
            - paragraph [ref=e138]: "Eligible: 0 · Reviewed: 0"
            - paragraph [ref=e139]: "Approval without edits: Not measured"
            - paragraph [ref=e140]: "Edit rate: Not measured · Rejection rate: Not measured"
            - paragraph [ref=e141]: "Adoption with or without edits: Not measured"
            - paragraph [ref=e142]: "Review coverage: Not measured"
            - paragraph [ref=e143]: These figures measure human review decisions. They do not measure correctness. Latest final decisions count at the shown cutoff.
            - paragraph [ref=e144]: "Cutoff: 2026-10-11T03:01:26.801294+00:00 · Definition: d24-v1"
          - group [ref=e145]:
            - generic "Saved run record" [ref=e146] [cursor=pointer]
  - contentinfo [ref=e147]: Fictional case workspace · Development release
```

# Test source

```ts
  1   | import { expect, test, type Page } from '@playwright/test';
  2   | import { readFileSync } from 'node:fs';
  3   | const evidence = process.env.BROWSER_EVIDENCE_DIR || '../../runs/2026-10-11-slice-04-changes';
  4   |
  5   | async function baseline(page: Page) {
  6   |   await page.goto('/');
  7   |   expect((await (await page.request.get('/config.json')).json()).api_url).toBe(process.env.LOCAL_TEST_API_URL);
  8   |   await page.getByRole('button', {name: 'Continue with local identity'}).click();
  9   |   await page.getByLabel('Fictional bank name').fill(`Fictional version bank ${Date.now()}`);
  10  |   await page.getByLabel('I confirm this case contains fictional data only.', {exact: true}).check();
  11  |   await page.getByRole('button', {name: 'Save fictional case'}).click();
  12  |   await page.getByLabel('Document file', {exact: true}).setInputFiles({name: 'policy.txt', mimeType: 'text/plain', buffer: readFileSync('../../data/fixtures/slice-02-policy.txt')});
  13  |   await page.getByLabel('I confirm this document contains fictional data only.', {exact: true}).check();
  14  |   await page.getByRole('button', {name: 'Upload fictional document', exact: true}).click();
  15  |   await page.getByLabel('Regulatory source', {exact: true}).selectOption('SIM-ACCESS');
  16  |   await page.getByRole('button', {name: 'Run controlled assessment', exact: true}).click();
  17  |   const result = page.getByRole('region', {name: 'Assessment result', exact: true});
  18  |   await expect(result).toContainText('Privileged sessions must be logged and reviewed each week.');
> 19  |   await page.getByRole('button', {name: 'Save review', exact: true}).click();
      |                                                                      ^ Error: locator.click: Test timeout of 30000ms exceeded.
  20  |   await expect(result).toContainText('Approved · Revision 1');
  21  |   return {result, changes: page.getByRole('region', {name: 'Regulatory changes', exact: true}), original: page.url()};
  22  | }
  23  |
  24  | test('VS4-BT01 added requirement creates an independent review and preserves the original', async ({page}) => {
  25  |   const {result, changes, original} = await baseline(page);
  26  |   await changes.getByRole('button', {name: 'Compare versions', exact: true}).click();
  27  |   await expect(changes).toContainText('Added requirement');
  28  |   await expect(changes).toContainText('Affected control: ACCESS-01');
  29  |   await expect(changes).toContainText('A separate reviewer must approve each weekly review.');
  30  |   await expect(result).toContainText('Approved · Revision 1');
  31  |   await changes.getByRole('button', {name: 'Open new assessment', exact: true}).click();
  32  |   await expect(result).toContainText('Approved: 0');
  33  |   await expect(result).toContainText('Pending: 1');
  34  |   await expect(result).not.toContainText('Approved · Revision 1');
  35  |   expect(page.url()).not.toBe(original);
  36  |   await result.getByRole('button', {name: 'Inspect Simulated clause 1', exact: true}).click();
  37  |   await expect(page.getByRole('dialog')).toContainText('Synthetic regulatory simulation');
  38  |   await page.getByRole('button', {name: 'Close source', exact: true}).click();
  39  |   await page.getByLabel('Rejected', {exact: true}).check();
  40  |   await page.getByLabel('Review reason', {exact: true}).fill('Separate approval evidence is missing.');
  41  |   await page.getByRole('button', {name: 'Save review', exact: true}).click();
  42  |   await expect(result).toContainText('Rejected · Revision 1');
  43  |   await changes.getByRole('button', {name: 'Open previous assessment', exact: true}).click();
  44  |   await expect(result).toContainText('Approved · Revision 1');
  45  |   await expect(result).not.toContainText('Rejected · Revision 1');
  46  |   await page.screenshot({path: `${evidence}/changes-desktop.png`, fullPage: true});
  47  | });
  48  |
  49  | test('VS4-BT02 wording and cosmetic changes preserve the original review', async ({page}) => {
  50  |   const {result, changes, original} = await baseline(page);
  51  |   for (const [version, title] of [['v2-cosmetic', 'Appearance only'], ['v2-replaced', 'Wording only']]) {
  52  |     await changes.getByLabel('Newer version', {exact: true}).selectOption(version);
  53  |     await changes.getByRole('button', {name: 'Compare versions', exact: true}).click();
  54  |     await expect(changes).toContainText(title);
  55  |     await expect(changes).toContainText('No changed requirement in this fixed simulation.');
  56  |     await expect(changes.getByRole('button', {name: 'Open new assessment', exact: true})).toHaveCount(0);
  57  |     await expect(result).toContainText('Approved · Revision 1');
  58  |     expect(page.url()).toBe(original);
  59  |   }
  60  | });
  61  |
  62  | test('VS4-BT03 reload restores comparisons and separate review histories', async ({page}) => {
  63  |   const {result, changes} = await baseline(page);
  64  |   await changes.getByRole('button', {name: 'Compare versions', exact: true}).click();
  65  |   await changes.getByRole('button', {name: 'Open new assessment', exact: true}).click();
  66  |   await page.getByRole('button', {name: 'Save review', exact: true}).click();
  67  |   await expect(result).toContainText('Approved · Revision 1');
  68  |   const job = new URL(page.url()).searchParams.get('assessment');
  69  |   await page.reload();
  70  |   await page.getByRole('button', {name: 'Continue with local identity'}).click();
  71  |   await expect(result).toContainText('Approved · Revision 1');
  72  |   expect(new URL(page.url()).searchParams.get('assessment')).toBe(job);
  73  |   await expect(changes).toContainText('Added requirement');
  74  |   await changes.getByRole('button', {name: 'Open previous assessment', exact: true}).click();
  75  |   await expect(result).toContainText('Approved · Revision 1');
  76  |   await expect.poll(() => new URL(page.url()).searchParams.get('assessment')).not.toBe(job);
  77  | });
  78  |
  79  | test('VS4-BT05 review saves wait for the selected assessment to finish loading', async ({page}) => {
  80  |   const {result, changes} = await baseline(page);
  81  |   const [response] = await Promise.all([
  82  |     page.waitForResponse(r => r.request().method() === 'POST' && r.url().endsWith('/comparisons')),
  83  |     changes.getByRole('button', {name: 'Compare versions', exact: true}).click(),
  84  |   ]);
  85  |   const comparison = await response.json();
  86  |   let release!: () => void;
  87  |   const waiting = new Promise<void>(resolve => {release = resolve;});
  88  |   await page.route(`**/assessments/${comparison.new_job_id}`, async route => {await waiting; await route.continue();});
  89  |   await changes.getByRole('button', {name: 'Open new assessment', exact: true}).click();
  90  |   await expect(result.getByRole('button', {name: 'Save review', exact: true})).toBeDisabled();
  91  |   release();
  92  |   await expect(result).toContainText('Pending: 1');
  93  |   await expect(result.getByRole('button', {name: 'Save review', exact: true})).toBeEnabled();
  94  |   await expect(result).not.toContainText('Approved · Revision 1');
  95  | });
  96  |
  97  | test('VS4-BT04 mobile keyboard controls and source passages fit the viewport', async ({page}) => {
  98  |   await page.setViewportSize({width: 390, height: 844});
  99  |   const {changes} = await baseline(page);
  100 |   const candidate = changes.getByLabel('Newer version', {exact: true});
  101 |   await candidate.focus();
  102 |   await expect(candidate).toBeFocused();
  103 |   await page.keyboard.press('Tab');
  104 |   await expect(changes.getByRole('button', {name: 'Compare versions', exact: true})).toBeFocused();
  105 |   await page.keyboard.press('Enter');
  106 |   await expect(changes).toContainText('Added requirement');
  107 |   expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBeTruthy();
  108 |   await page.screenshot({path: `${evidence}/changes-mobile.png`, fullPage: true});
  109 | });
  110 |
```
