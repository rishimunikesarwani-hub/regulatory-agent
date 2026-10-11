# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: changes.spec.ts >> VS4-BT03 reload restores comparisons and separate review histories
- Location: tests\changes.spec.ts:62:1

# Error details

```
Error: expect(received).not.toBe(expected) // Object.is equality

Expected: not "2f482c2663e341a3b97572b4bf33cfbf"
```

# Page snapshot

```yaml
- generic [ref=f1e2]:
  - link "Skip to content" [ref=f1e3] [cursor=pointer]:
    - /url: "#main"
  - banner [ref=f1e4]:
    - generic [ref=f1e5]:
      - generic [aria-hidden] [ref=f1e6]: R
      - generic [ref=f1e7]: The Regulator
    - generic [ref=f1e8]:
      - generic [ref=f1e9]: Local development
      - button "Sign out" [ref=f1e10] [cursor=pointer]
  - main [ref=f1e11]:
    - button "← Back to cases" [ref=f1e12] [cursor=pointer]
    - generic [ref=f1e13]:
      - generic [ref=f1e14]:
        - generic [ref=f1e15]: Synthetic demo
        - heading "Fictional version bank 1791687233599" [level=1] [ref=f1e16]
        - paragraph [ref=f1e17]: Your fictional bank profile is saved.
      - generic [ref=f1e18]: Controlled assessment completed
    - generic [ref=f1e19]:
      - heading "Case details" [level=2] [ref=f1e20]
      - generic [ref=f1e21]:
        - generic [ref=f1e22]:
          - term [ref=f1e23]: Bank profile
          - definition [ref=f1e24]: Fictional version bank 1791687233599
        - generic [ref=f1e25]:
          - term [ref=f1e26]: Data type
          - definition [ref=f1e27]: Fictional data
        - generic [ref=f1e28]:
          - term [ref=f1e29]: Created
          - definition [ref=f1e30]: 10/11/2026, 8:23:53 AM
        - generic [ref=f1e31]:
          - term [ref=f1e32]: Case ID
          - definition [ref=f1e33]: a9a05a32be4e471298ac96531d33388b
    - generic [ref=f1e34]:
      - region [ref=f1e35]:
        - generic [ref=f1e36]:
          - generic [ref=f1e37]:
            - paragraph [ref=f1e38]: SOURCE DOCUMENTS
            - heading "Documents" [level=2] [ref=f1e39]
            - paragraph [ref=f1e40]: Keep the original file and inspect its extracted text.
          - button "Refresh documents" [ref=f1e41] [cursor=pointer]
        - generic [ref=f1e42]:
          - generic [ref=f1e43]:
            - region [ref=f1e44]:
              - heading "Upload a fictional document" [level=3] [ref=f1e45]
              - paragraph [ref=f1e46]: Text PDF, DOCX, TXT, or CSV. Maximum 10 MB per file and 10 saved versions per case.
              - group [ref=f1e48]:
                - generic [ref=f1e49]: Document file
                - button "Document file" [ref=f1e50]
                - generic [ref=f1e51]: Document role
                - combobox "Document role" [ref=f1e52]:
                  - option "Bank profile"
                  - option "Policy" [selected]
                  - option "Control"
                  - option "Evidence"
                - generic [ref=f1e53]: Replace source
                - combobox "Replace source" [ref=f1e54]:
                  - option "New source" [selected]
                  - option "policy.txt"
                - paragraph [ref=f1e55]: A replacement adds a version. It keeps the earlier version.
                - generic [ref=f1e56]:
                  - checkbox "I confirm this document contains fictional data only." [ref=f1e57]
                  - generic [ref=f1e58]: I confirm this document contains fictional data only.
                - button "Upload fictional document" [disabled] [ref=f1e59]
            - region [ref=f1e60]:
              - heading "Saved versions 1" [level=3] [ref=f1e61]
              - button "Inspect policy.txt version 1" [pressed] [ref=f1e62] [cursor=pointer]:
                - strong [ref=f1e63]: policy.txt
                - generic [ref=f1e64]: policy · Version 1 · TXT
          - region [ref=f1e65]:
            - heading "Source evidence" [level=3] [ref=f1e66]
            - generic [ref=f1e67]:
              - generic [ref=f1e68]:
                - heading "policy.txt" [level=3] [ref=f1e69]
                - paragraph [ref=f1e70]: Version 1 · policy · TXT
              - button "Download original" [ref=f1e71] [cursor=pointer]
            - paragraph [ref=f1e72]: Extracted text can omit images and visual table structure. Use the original file to check them.
            - paragraph [ref=f1e73]: "Version ID: 465ddb06aa0d4258823f1b314a9e75d4"
            - group [ref=f1e74]:
              - generic "Content hash (SHA-256)" [ref=f1e75]
            - generic [ref=f1e76]:
              - article [ref=f1e77]:
                - heading "Line 1" [level=4] [ref=f1e78]
                - generic [ref=f1e79]: Synthetic demo. Fictional bank policy.
              - article [ref=f1e80]:
                - heading "Line 2" [level=4] [ref=f1e81]
                - generic [ref=f1e82]: Control ACCESS-01 requires supervision of privileged sessions, complete activity logging, and a weekly review.
              - article [ref=f1e83]:
                - heading "Line 3" [level=4] [ref=f1e84]
                - generic [ref=f1e85]: Weekly timing is bank policy, not an RBI-specified interval.
      - region [ref=f1e86]:
        - generic [ref=f1e87]:
          - generic [ref=f1e88]:
            - paragraph [ref=f1e89]: CONTROLLED EXAMPLE
            - heading "Assessment" [level=2] [ref=f1e90]
            - paragraph [ref=f1e91]: Review one fictional policy against a selected historical or simulated rule.
          - button "Refresh assessment" [ref=f1e92] [cursor=pointer]
        - generic [ref=f1e93]:
          - paragraph [ref=f1e94]: Use the supplied fictional policy. Other documents cannot run this controlled example.
          - paragraph [ref=f1e95]:
            - link "Download the fictional policy" [ref=f1e96] [cursor=pointer]:
              - /url: data:text/plain;charset=utf-8,…
            - text: ", then upload it as a policy document."
          - generic [ref=f1e97]: Policy version
          - combobox "Policy version" [ref=f1e98]:
            - option "Upload a fictional policy first"
            - option "policy.txt · Version 1" [selected]
          - generic [ref=f1e99]: Regulatory source
          - combobox "Regulatory source" [ref=f1e100]:
            - option "RBI clause 19(b) · historical 2023 version" [selected]
            - option "Simulated access rule · v1"
          - paragraph [ref=f1e101]: "Historical date: 8 April 2024. Current regulatory status is unverified. No live model call is made."
          - button "Run controlled assessment" [ref=f1e102] [cursor=pointer]
          - generic [ref=f1e103]: Saved assessments
          - combobox "Saved assessments" [ref=f1e104]:
            - option "Select a saved assessment"
            - option "10/11/2026, 8:23:55 AM · 2f482c26"
            - option "10/11/2026, 8:23:54 AM · f52af038" [selected]
        - region "Regulatory changes" [ref=f1e105]:
          - heading "Regulatory changes" [level=2] [ref=f1e106]
          - generic [ref=f1e107]: Synthetic regulatory simulation
          - paragraph [ref=f1e108]: Compare specified fictional versions. Earlier assessments and human reviews stay unchanged.
          - paragraph [ref=f1e109]: These examples do not establish current regulatory coverage or live model quality.
          - paragraph [ref=f1e110]: "Older version: SIM-ACCESS:v1 · Selected assessment: f52af038"
          - generic [ref=f1e111]: Newer version
          - combobox "Newer version" [ref=f1e112]:
            - option "v2-added · Separate reviewer approval" [selected]
            - option "v2-replaced · Same rule, different wording"
            - option "v2-cosmetic · Punctuation change"
          - button "Compare versions" [ref=f1e113] [cursor=pointer]
          - generic [ref=f1e114]: Saved comparison
          - combobox "Saved comparison" [ref=f1e115]:
            - option "v1 → v2-added · 00ba1f51" [selected]
          - generic [ref=f1e116]:
            - heading "Added requirement" [level=3] [ref=f1e117]
            - paragraph [ref=f1e118]: "Affected control: ACCESS-01. The new assessment needs its own human review."
            - generic [ref=f1e119]:
              - article [ref=f1e120]:
                - heading "Older source · SIM-ACCESS:v1" [level=4] [ref=f1e121]
                - paragraph [ref=f1e122]: Synthetic regulatory simulation
                - generic [ref=f1e123]:
                  - heading "Simulated clause 1" [level=4] [ref=f1e124]
                  - generic [ref=f1e125]: Privileged sessions must be logged and reviewed each week.
              - article [ref=f1e126]:
                - heading "Newer source · SIM-ACCESS:v2-added" [level=4] [ref=f1e127]
                - paragraph [ref=f1e128]: Synthetic regulatory simulation
                - generic [ref=f1e129]:
                  - heading "Simulated clause 1" [level=4] [ref=f1e130]
                  - generic [ref=f1e131]: Privileged sessions must be logged and reviewed each week. A separate reviewer must approve each weekly review.
            - group [ref=f1e132]:
              - generic "Source metadata changes" [ref=f1e133]
            - generic [ref=f1e134]:
              - button "Open previous assessment" [ref=f1e135] [cursor=pointer]
              - button "Open new assessment" [ref=f1e136] [cursor=pointer]
        - region "Assessment result" [ref=f1e137]:
          - generic [ref=f1e138]:
            - generic [ref=f1e139]: Controlled simulation
            - heading "Needs review" [level=3] [ref=f1e140]
            - paragraph [ref=f1e141]: This is a fixed example. It does not establish compliance or current regulatory coverage.
          - generic [ref=f1e142]:
            - article [ref=f1e143]:
              - heading "Requirement and applicability" [level=3] [ref=f1e144]
              - paragraph [ref=f1e145]: Privileged sessions must be logged and reviewed each week.
              - paragraph [ref=f1e146]: Unverified for this fictional bank profile. Synthetic regulatory simulation.
              - heading "Conditions" [level=4] [ref=f1e147]
              - list [ref=f1e148]:
                - listitem [ref=f1e149]: Fictional commercial-bank rule for this simulation.
              - heading "Exceptions" [level=4] [ref=f1e150]
              - list
              - heading "Policy control" [level=4] [ref=f1e151]
              - paragraph [ref=f1e152]: Control ACCESS-01 requires supervision of privileged sessions, complete activity logging, and a weekly review.
              - paragraph [ref=f1e153]: Weekly timing belongs to the fictional policy and simulated rule.
              - button "Inspect Simulated clause 1" [ref=f1e155] [cursor=pointer]
            - article [ref=f1e156]:
              - heading "Original finding" [level=3] [ref=f1e157]
              - paragraph [ref=f1e158]: Controlled simulation. The policy states a control. Operational records and applicability have not been verified.
              - heading "Proposed recommendation" [level=4] [ref=f1e159]
              - paragraph [ref=f1e160]: Request dated privileged-session logs and completed weekly reviews.
              - button "Inspect policy Line 2" [ref=f1e162] [cursor=pointer]
              - group "Human review" [ref=f1e164]:
                - generic [ref=f1e166]:
                  - generic [ref=f1e167]:
                    - radio "Approved" [checked] [ref=f1e168]
                    - text: Approved
                  - generic [ref=f1e169]:
                    - radio "Edited" [ref=f1e170]
                    - text: Edited
                  - generic [ref=f1e171]:
                    - radio "Rejected" [ref=f1e172]
                    - text: Rejected
                  - generic [ref=f1e173]:
                    - radio "Request more evidence" [ref=f1e174]
                    - text: Request more evidence
                - generic [ref=f1e175]: Review reason
                - textbox "Review reason" [ref=f1e176]
                - button "Save review" [ref=f1e177] [cursor=pointer]
          - generic [ref=f1e178]:
            - heading "Saved review outcomes" [level=3] [ref=f1e179]
            - paragraph [ref=f1e180]: "Approved: 1 · Edited: 0 · Rejected: 0 · Pending: 0"
            - paragraph [ref=f1e181]: "Eligible: 1 · Reviewed: 1"
            - paragraph [ref=f1e182]: "Approval without edits: 100%"
            - paragraph [ref=f1e183]: "Edit rate: 0% · Rejection rate: 0%"
            - paragraph [ref=f1e184]: "Adoption with or without edits: 100%"
            - paragraph [ref=f1e185]: "Review coverage: 100%"
            - paragraph [ref=f1e186]: These figures measure human review decisions. They do not measure correctness. Latest final decisions count at the shown cutoff.
            - paragraph [ref=f1e187]: "Cutoff: 2026-10-11T02:53:56.496516+00:00 · Definition: d24-v1"
            - article [ref=f1e188]:
              - heading "Approved · Revision 1" [level=4] [ref=f1e189]
              - paragraph [ref=f1e190]: Controlled simulation. The policy states a control. Operational records and applicability have not been verified.
              - paragraph [ref=f1e191]: Request dated privileged-session logs and completed weekly reviews.
          - group [ref=f1e192]:
            - generic "Saved run record" [ref=f1e193] [cursor=pointer]
  - contentinfo [ref=f1e194]: Fictional case workspace · Development release
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
  15 |   await page.getByLabel('Regulatory source', {exact: true}).selectOption('SIM-ACCESS');
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
> 76 |   expect(new URL(page.url()).searchParams.get('assessment')).not.toBe(job);
     |                                                                  ^ Error: expect(received).not.toBe(expected) // Object.is equality
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
