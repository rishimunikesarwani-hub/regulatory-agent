# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: release.spec.ts >> VS5-BT01 JSON and Markdown downloads preserve saved review and exact sources
- Location: tests\release.spec.ts:25:1

# Error details

```
Test timeout of 30000ms exceeded.
```

```
Error: page.waitForEvent: Test timeout of 30000ms exceeded.
=========================== logs ===========================
waiting for event "download"
============================================================
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
        - heading "Fictional export bank 1791689572852" [level=1] [ref=e17]
        - paragraph [ref=e18]: Your fictional bank profile is saved.
      - generic [ref=e19]: Controlled assessment completed
    - generic [ref=e20]:
      - heading "Case details" [level=2] [ref=e21]
      - generic [ref=e22]:
        - generic [ref=e23]:
          - term [ref=e24]: Bank profile
          - definition [ref=e25]: Fictional export bank 1791689572852
        - generic [ref=e26]:
          - term [ref=e27]: Data type
          - definition [ref=e28]: Fictional data
        - generic [ref=e29]:
          - term [ref=e30]: Created
          - definition [ref=e31]: 10/11/2026, 9:02:52 AM
        - generic [ref=e32]:
          - term [ref=e33]: Case ID
          - definition [ref=e34]: b6b839b6021f4d3685b3c31f94797231
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
            - paragraph [ref=e75]: "Version ID: b0984a0f0db44a1f87cad0c10fdc9e95"
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
            - option "RBI clause 19(b) · historical 2023 version" [selected]
            - option "Simulated access rule · v1"
          - paragraph [ref=e103]: "Historical date: 8 April 2024. Current regulatory status is unverified. No live model call is made."
          - button "Run controlled assessment" [ref=e104] [cursor=pointer]
          - generic [ref=e105]: Saved assessments
          - combobox "Saved assessments" [ref=e106]:
            - option "Select a saved assessment"
            - option "10/11/2026, 9:02:53 AM · 78e27792" [selected]
        - region "Regulatory changes" [ref=e107]:
          - heading "Regulatory changes" [level=2] [ref=e108]
          - generic [ref=e109]: Synthetic regulatory simulation
          - paragraph [ref=e110]: Compare specified fictional versions. Earlier assessments and human reviews stay unchanged.
          - paragraph [ref=e111]: These examples do not establish current regulatory coverage or live model quality.
          - paragraph [ref=e112]: Run or open a completed simulated v1 assessment to select the earlier version.
        - region "Assessment result" [ref=e113]:
          - generic [ref=e114]:
            - generic [ref=e115]: Controlled simulation
            - heading "Needs review" [level=3] [ref=e116]
            - paragraph [ref=e117]: This is a fixed example. It does not establish compliance or current regulatory coverage.
          - generic [ref=e118]:
            - article [ref=e119]:
              - heading "Requirement and applicability" [level=3] [ref=e120]
              - paragraph [ref=e121]: Personnel with elevated system access entitlements shall be closely supervised with all their systems activities logged and periodically reviewed.
              - paragraph [ref=e122]: Unverified for this fictional bank profile.
              - heading "Conditions" [level=4] [ref=e123]
              - list [ref=e124]:
                - listitem [ref=e125]: Personnel with elevated system access entitlements.
                - listitem [ref=e126]: Applicability to the listed regulated entities must be established.
              - heading "Exceptions" [level=4] [ref=e127]
              - list [ref=e128]:
                - listitem [ref=e129]: Local Area Banks
                - listitem [ref=e130]: NBFC-Core Investment Companies
              - heading "Policy control" [level=4] [ref=e131]
              - paragraph [ref=e132]: Control ACCESS-01 requires supervision of privileged sessions, complete activity logging, and a weekly review.
              - paragraph [ref=e133]: Weekly timing is bank policy. RBI does not specify that interval in this clause.
              - generic [ref=e134]:
                - button "Inspect Clause 19(b)" [ref=e135] [cursor=pointer]
                - button "Inspect Clause 2(a)(i)" [ref=e136] [cursor=pointer]
                - button "Inspect Clause 2(b)" [ref=e137] [cursor=pointer]
            - article [ref=e138]:
              - heading "Original finding" [level=3] [ref=e139]
              - paragraph [ref=e140]: Controlled example. The policy states a control, but this example has no verified operational evidence. Applicability and activity records need human review.
              - heading "Proposed recommendation" [level=4] [ref=e141]
              - paragraph [ref=e142]: Confirm applicability. Request dated session records, supervisor sign-offs, complete activity logs, and completed periodic reviews.
              - button "Inspect policy Line 2" [ref=e144] [cursor=pointer]
              - group "Human review" [ref=e146]:
                - generic [ref=e148]:
                  - generic [ref=e149]:
                    - radio "Approved" [checked] [ref=e150]
                    - text: Approved
                  - generic [ref=e151]:
                    - radio "Edited" [ref=e152]
                    - text: Edited
                  - generic [ref=e153]:
                    - radio "Rejected" [ref=e154]
                    - text: Rejected
                  - generic [ref=e155]:
                    - radio "Request more evidence" [ref=e156]
                    - text: Request more evidence
                - generic [ref=e157]: Review reason
                - textbox "Review reason" [ref=e158]
                - button "Save review" [ref=e159] [cursor=pointer]
          - generic [ref=e160]:
            - heading "Saved review outcomes" [level=3] [ref=e161]
            - paragraph [ref=e162]: "Approved: 1 · Edited: 0 · Rejected: 0 · Pending: 0"
            - paragraph [ref=e163]: "Eligible: 1 · Reviewed: 1"
            - paragraph [ref=e164]: "Approval without edits: 100%"
            - paragraph [ref=e165]: "Edit rate: 0% · Rejection rate: 0%"
            - paragraph [ref=e166]: "Adoption with or without edits: 100%"
            - paragraph [ref=e167]: "Review coverage: 100%"
            - paragraph [ref=e168]: These figures measure human review decisions. They do not measure correctness. Latest final decisions count at the shown cutoff.
            - paragraph [ref=e169]: "Cutoff: 2026-10-11T03:32:54.310989+00:00 · Definition: d24-v1"
            - article [ref=e170]:
              - heading "Approved · Revision 1" [level=4] [ref=e171]
              - paragraph [ref=e172]: Controlled example. The policy states a control, but this example has no verified operational evidence. Applicability and activity records need human review.
              - paragraph [ref=e173]: Confirm applicability. Request dated session records, supervisor sign-offs, complete activity logs, and completed periodic reviews.
          - group [ref=e174]:
            - generic "Saved run record" [ref=e175] [cursor=pointer]
  - contentinfo [ref=e176]: Fictional case workspace · Development release
```

# Test source

```ts
  1  | import { expect, test, type Page, type Download } from '@playwright/test';
  2  | import { readFileSync } from 'node:fs';
  3  | const evidenceDir = process.env.BROWSER_EVIDENCE_DIR || '../../runs/2026-10-11-slice-05-release';
  4  |
  5  | async function assessment(page: Page) {
  6  |   await page.goto('/');
  7  |   await page.getByRole('button', {name: 'Continue with local identity'}).click();
  8  |   await page.getByLabel('Fictional bank name').fill(`Fictional export bank ${Date.now()}`);
  9  |   await page.getByLabel('I confirm this case contains fictional data only.', {exact:true}).check();
  10 |   await page.getByRole('button', {name: 'Save fictional case'}).click();
  11 |   await page.getByLabel('Document file', {exact:true}).setInputFiles({name:'policy.txt',mimeType:'text/plain',buffer:readFileSync('../../data/fixtures/slice-02-policy.txt')});
  12 |   await page.getByLabel('I confirm this document contains fictional data only.', {exact:true}).check();
  13 |   await page.getByRole('button', {name:'Upload fictional document',exact:true}).click();
  14 |   await page.getByRole('button', {name:'Run controlled assessment',exact:true}).click();
  15 |   const result = page.getByRole('region',{name:'Assessment result',exact:true});
  16 |   await expect(result).toContainText('Needs review');
  17 |   return result;
  18 | }
  19 |
  20 | async function text(download: Download) {
  21 |   expect(await download.failure()).toBeNull();
  22 |   return readFileSync((await download.path())!, 'utf8');
  23 | }
  24 |
  25 | test('VS5-BT01 JSON and Markdown downloads preserve saved review and exact sources',async ({page}) => {
  26 |   const result = await assessment(page);
  27 |   await page.getByLabel('Approved',{exact:true}).check();
  28 |   await page.getByRole('button',{name:'Save review',exact:true}).click();
  29 |   await expect(result).toContainText('Approved · Revision 1');
  30 |   const expected = await result.locator('.identifier').first().innerText();
> 31 |   const [json] = await Promise.all([page.waitForEvent('download'),page.getByRole('button',{name:'Download JSON',exact:true}).click()]);
     |                                          ^ Error: page.waitForEvent: Test timeout of 30000ms exceeded.
  32 |   const report = JSON.parse(await text(json));
  33 |   expect(report.summary.approved).toBe(1);
  34 |   expect(report.summary.approval_rate).toBe(1);
  35 |   expect(report.snapshot.snapshot_id).toBeTruthy();
  36 |   expect(report.sources).toHaveLength(2);
  37 |   expect(report.data_mode).toBe('controlled_simulation');
  38 |   expect(report.label).toContain('Simulated');
  39 |   expect(report.cost_usd).toBeNull();
  40 |   expect(report.findings[0].status).toBe('needs_review');
  41 |   const [markdown] = await Promise.all([page.waitForEvent('download'),page.getByRole('button',{name:'Download Markdown',exact:true}).click()]);
  42 |   const contents = await text(markdown);
  43 |   expect(contents).toContain(report.snapshot.snapshot_id);
  44 |   expect(contents).toContain('approved: 1');
  45 |   expect(contents).toContain('Clause 19(b)');
  46 |   expect(contents).toContain('cost: Unknown');
  47 |   await expect(result).toContainText(expected);
  48 |   await json.saveAs(`${evidenceDir}/export-example.json`);
  49 |   await markdown.saveAs(`${evidenceDir}/export-example.md`);
  50 |   await page.screenshot({path:`${evidenceDir}/release-desktop.png`,fullPage:true});
  51 | });
  52 |
  53 | test('VS5-BT02 export failure preserves saved review and retry succeeds',async ({page}) => {
  54 |   const result = await assessment(page);
  55 |   await page.getByLabel('Approved',{exact:true}).check();
  56 |   await page.getByRole('button',{name:'Save review',exact:true}).click();
  57 |   await expect(result).toContainText('Approved · Revision 1');
  58 |   const job = new URL(page.url()).searchParams.get('assessment');
  59 |   await page.route('**/assessments/*/export*',route=>route.fulfill({status:503,contentType:'application/json',body:JSON.stringify({message:'Export unavailable.',next_action:'Retry the export.'})}),{times:1});
  60 |   await page.getByRole('button',{name:'Download JSON',exact:true}).click();
  61 |   await expect(page.getByRole('alert')).toContainText('Export unavailable');
  62 |   await expect(result).toContainText('Approved · Revision 1');
  63 |   expect(new URL(page.url()).searchParams.get('assessment')).toBe(job);
  64 |   const [download] = await Promise.all([page.waitForEvent('download'),page.getByRole('button',{name:'Download JSON',exact:true}).click()]);
  65 |   expect(JSON.parse(await text(download)).summary.approved).toBe(1);
  66 | });
  67 |
  68 | test('VS5-BT03 mobile keyboard download keeps labels and does not overflow',async ({page}) => {
  69 |   await page.setViewportSize({width:390,height:844});
  70 |   const result = await assessment(page);
  71 |   const download = page.getByRole('button',{name:'Download JSON',exact:true});
  72 |   await download.focus();
  73 |   const [file] = await Promise.all([page.waitForEvent('download'),page.keyboard.press('Enter')]);
  74 |   expect(JSON.parse(await text(file)).label).toContain('Simulated');
  75 |   expect(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth)).toBe(true);
  76 |   await expect(result).toContainText('Not measured');
  77 |   await page.screenshot({path:`${evidenceDir}/release-mobile.png`,fullPage:true});
  78 | });
  79 |
```
