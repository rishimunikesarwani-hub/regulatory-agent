# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: changes.spec.ts >> VS4-BT03 reload restores comparisons and separate review histories
- Location: tests\changes.spec.ts:62:1

# Error details

```
Error: expect(locator).toContainText(expected) failed

Locator: getByRole('region', { name: 'Assessment result', exact: true })
Expected substring: "Approved · Revision 1"
Received string:    "Controlled simulationNeeds reviewThis is a fixed example. It does not establish compliance or current regulatory coverage.Requirement and applicabilityPrivileged sessions must be logged and reviewed each week. A separate reviewer must approve each weekly review.Unverified for this fictional bank profile. Synthetic regulatory simulation.ConditionsFictional commercial-bank rule for this simulation.ExceptionsPolicy controlControl ACCESS-01 requires supervision of privileged sessions, complete activity logging, and a weekly review.Weekly timing belongs to the fictional policy and simulated rule.Inspect Simulated clause 1Original findingControlled simulation. The policy states a control. Operational records and applicability have not been verified.Proposed recommendationRequest dated privileged-session logs and completed weekly reviews. Request evidence that a separate reviewer approved each weekly review.Inspect policy Line 2Human reviewApprovedEditedRejectedRequest more evidenceReview reasonSave reviewSaved review outcomesApproved: 0 · Edited: 0 · Rejected: 0 · Pending: 1Eligible: 1 · Reviewed: 0Approval without edits: Not measuredEdit rate: Not measured · Rejection rate: Not measuredAdoption with or without edits: Not measuredReview coverage: 0%These figures measure human review decisions. They do not measure correctness. Latest final decisions count at the shown cutoff.Cutoff: 2026-10-11T02:50:31.328944+00:00 · Definition: d24-v1Saved run recordAssessment date: 2024-05-08 · Controlled dispatches: 1 · Live model calls: 0 · Usage and cost: not measuredJob: f19456fd83a8461fb88e715f703f8cd4model call: succeeded · 0.0160 scontext selection: succeeded · 0.0000 sextraction: skipped · 0.0000 ssource verification: succeeded · 0.0000 sretrieval: succeeded · 0.0000 svalidation: succeeded · 0.0000 spersistence: succeeded · 0.0310 sSaved versions: 433a66789d434faf8080cecbb028c24c:1, SIM-ACCESS:v2-added"
Timeout: 5000ms

Call log:
  - Expect "toContainText" getByRole('region', { name: 'Assessment result', exact: true }) with timeout 5000ms
  - waiting for getByRole('region', { name: 'Assessment result', exact: true })
    12 × locator resolved to <section class="assessment-result" aria-label="Assessment result">…</section>
       - unexpected value "Controlled simulationNeeds reviewThis is a fixed example. It does not establish compliance or current regulatory coverage.Requirement and applicabilityPrivileged sessions must be logged and reviewed each week. A separate reviewer must approve each weekly review.Unverified for this fictional bank profile. Synthetic regulatory simulation.ConditionsFictional commercial-bank rule for this simulation.ExceptionsPolicy controlControl ACCESS-01 requires supervision of privileged sessions, complete activity logging, and a weekly review.Weekly timing belongs to the fictional policy and simulated rule.Inspect Simulated clause 1Original findingControlled simulation. The policy states a control. Operational records and applicability have not been verified.Proposed recommendationRequest dated privileged-session logs and completed weekly reviews. Request evidence that a separate reviewer approved each weekly review.Inspect policy Line 2Human reviewApprovedEditedRejectedRequest more evidenceReview reasonSave reviewSaved review outcomesApproved: 0 · Edited: 0 · Rejected: 0 · Pending: 1Eligible: 1 · Reviewed: 0Approval without edits: Not measuredEdit rate: Not measured · Rejection rate: Not measuredAdoption with or without edits: Not measuredReview coverage: 0%These figures measure human review decisions. They do not measure correctness. Latest final decisions count at the shown cutoff.Cutoff: 2026-10-11T02:50:31.328944+00:00 · Definition: d24-v1Saved run recordAssessment date: 2024-05-08 · Controlled dispatches: 1 · Live model calls: 0 · Usage and cost: not measuredJob: f19456fd83a8461fb88e715f703f8cd4model call: succeeded · 0.0160 scontext selection: succeeded · 0.0000 sextraction: skipped · 0.0000 ssource verification: succeeded · 0.0000 sretrieval: succeeded · 0.0000 svalidation: succeeded · 0.0000 spersistence: succeeded · 0.0310 sSaved versions: 433a66789d434faf8080cecbb028c24c:1, SIM-ACCESS:v2-added"

```

```yaml
- region "Assessment result":
  - text: Controlled simulation
  - heading "Needs review" [level=3]
  - paragraph: This is a fixed example. It does not establish compliance or current regulatory coverage.
  - article:
    - heading "Requirement and applicability" [level=3]
    - paragraph: Privileged sessions must be logged and reviewed each week. A separate reviewer must approve each weekly review.
    - paragraph: Unverified for this fictional bank profile. Synthetic regulatory simulation.
    - heading "Conditions" [level=4]
    - list:
      - listitem: Fictional commercial-bank rule for this simulation.
    - heading "Exceptions" [level=4]
    - list
    - heading "Policy control" [level=4]
    - paragraph: Control ACCESS-01 requires supervision of privileged sessions, complete activity logging, and a weekly review.
    - paragraph: Weekly timing belongs to the fictional policy and simulated rule.
    - button "Inspect Simulated clause 1"
  - article:
    - heading "Original finding" [level=3]
    - paragraph: Controlled simulation. The policy states a control. Operational records and applicability have not been verified.
    - heading "Proposed recommendation" [level=4]
    - paragraph: Request dated privileged-session logs and completed weekly reviews. Request evidence that a separate reviewer approved each weekly review.
    - button "Inspect policy Line 2"
    - group "Human review":
      - text: Human review
      - radio "Approved" [checked]
      - text: Approved
      - radio "Edited"
      - text: Edited
      - radio "Rejected"
      - text: Rejected
      - radio "Request more evidence"
      - text: Request more evidence Review reason
      - textbox "Review reason"
      - button "Save review"
  - heading "Saved review outcomes" [level=3]
  - paragraph: "Approved: 0 · Edited: 0 · Rejected: 0 · Pending: 1"
  - paragraph: "Eligible: 1 · Reviewed: 0"
  - paragraph: "Approval without edits: Not measured"
  - paragraph: "Edit rate: Not measured · Rejection rate: Not measured"
  - paragraph: "Adoption with or without edits: Not measured"
  - paragraph: "Review coverage: 0%"
  - paragraph: These figures measure human review decisions. They do not measure correctness. Latest final decisions count at the shown cutoff.
  - paragraph: "Cutoff: 2026-10-11T02:50:31.328944+00:00 · Definition: d24-v1"
  - group: Saved run record
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
> 71 |   await expect(result).toContainText('Approved · Revision 1');
     |                        ^ Error: expect(locator).toContainText(expected) failed
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
