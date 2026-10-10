# PRD - The Regulatory Agent

> Status: The user gave approval during planning. First saved on 2026-10-08.
> Purpose: Help an Indian bank reviewer connect requirements to controls, evidence, gaps, and proposed corrections.
> Scope: [D01–D06](../decisions/gov-decision-log.md).
> Language revision: 2026-10-09. Use ASD-STE100 writing rules under D18.

> Measurement update: 2026-10-10. [D24](../decisions/gov-decision-log.md#d24---reviewer-outcomes-and-measured-agent-baseline) adds reviewer outcomes, different evaluations, and stage traces.

## 1. Problem

The brief has a requirement for an agentic system for banking regulations.
The system must record changes and do assessments of internal controls.
It must identify gaps and give proposed corrections.

The brief gives this relationship:

**Regulations → obligations → applicability → policies/controls → evidence → testing → gaps → remediation → monitoring.**

A reviewer must be able to examine the full relationship.
Each supported finding must have an accessible source passage and document version.
If evidence is missing, the system must state which conclusions do not have sufficient evidence.

This problem definition comes from the brief.
The project has no verification results for market size, customer demand, or time savings.

## 2. Users and scope

- **Primary user:** An IT compliance analyst at an Indian commercial bank.
- **Task:** Compare documented controls and supplied evidence with selected applicable requirements.
- **Reviewer:** A person who gives approval, edits or rejects a recommendation, or requests more evidence before a final decision.
- **First-release institution:** A domestic commercial-bank scenario.
- **Case scope:** One bank profile per case.

The project has no record of the user's existing process from direct observation.
It has no measured time-saving baseline.
Document comparison and evidence collection are intended application functions.
They are not research findings with verification results.

One authenticated operator can do the review in the demo.
This is not evidence of two-person approval by reviewers who work independently.

## 3. Required first-release functions

The eight functions below come from the organizer's feature list.

| Requirement | Brief feature | Mandatory behavior | Acceptance case |
|---|---|---|---|
| REQ-F01 | 1. Regulatory intelligence and knowledge ingestion | Retrieve current regulations through an external API. Keep authoritative sources, versions, verification times, and source locations. | AC-F01: The reviewer can examine a clause, its authority, and its verification time. Block current assessments if verification fails. |
| REQ-F02 | 2. Regulatory change intelligence | Compare two specified versions. Show changed obligations and affected control mappings. | AC-F02: A changed requirement causes a new assessment snapshot. The previous assessment stays accessible. |
| REQ-F03 | 3. Regulatory obligation extraction | Extract specific requirements, stated applicability, and clause references. | AC-F03: Keep source conditions, exceptions, and scope. |
| REQ-F04 | 4. Bank control-framework understanding | Extract stated controls and purposes. Extract owners and frequencies only when the source supplies them. | AC-F04: Keep missing fields unknown. Do not invent values. |
| REQ-F05 | 5. Regulatory-to-control mapping | Connect applicable requirements to relevant controls. Include reasons and source references. | AC-F05: An unrelated control does not give sufficient coverage. |
| REQ-F06 | 7. Evidence-based compliance assessment | Compare supplied evidence with the requirement. Keep uncertainty visible. | AC-F06: A policy alone is not sufficient evidence that an operational control occurred. |
| REQ-F07 | 8. Gap identification | Identify control gaps with evidence, and evidence gaps. Keep their meanings different. | AC-F07: Missing records cause an evidence gap or needs-review result. They are not sufficient evidence of an operational failure. |
| REQ-F08 | 10. Remediation recommendation engine | Propose a correction or evidence request. Connect it to the obligation and finding. | AC-F08: The reviewer can examine the proposal's source and record a decision. Keep the initial finding. |

The following requirements are necessary for the eight functions.

| Requirement | Behavior | Acceptance case |
|---|---|---|
| REQ-X01 | Bounded agent tools and job allowances | AC-X01: Stop safely for prohibited actions or exhausted allowances. |
| REQ-X02 | Case ownership and India-only private processing | AC-X02: Deny cross-case access. Make sure that cloud destinations meet the India-only rule before private uploads. |
| REQ-X03 | Fixed snapshots and correct citations | AC-X03: A replacement document cannot change an active assessment. |
| REQ-X04 | Saved asynchronous jobs | AC-X04: Retries cannot cause a second active assessment or a second final report. |
| REQ-X05 | Reviewer interface and export | AC-X05: Source inspection, review decisions, and exports keep the evidence relationship. |
| REQ-X06 | Local and cloud operation with different checks | AC-X06: AWS credentials are not necessary for default checks. Simulated results have visible labels. |
| REQ-X07 | Reviewer outcomes and primary product measure | AC-X07: Save Approved, Edited, and Rejected outcomes in different records from AI findings. Calculate rates, review coverage, and pending counts without duplicate items. |
| REQ-X08 | Per-stage trace and runtime measurements | AC-X08: Connect sources, selected passages, model calls, checks, and outcomes. Record duration, attempts, usage, costs, and failures without private operational log content. |
| REQ-X09 | Retrieval and assessment evaluations with different scores | AC-X09: Calculate scores for source coverage and necessary passages independently of finding accuracy. Keep fixed labels, held-out cases, and the approved model baseline. |

### Finding terms

A supported finding means that supplied evidence is sufficient for the selected requirement.
It does not give compliance certification to the bank.
It is not evidence of an inspection of live bank systems.

Use these finding status values:

- supported
- partial
- gap
- needs_review
- not_applicable

Also record the evidence condition: sufficient, partial, missing, or conflicting.

A not_applicable finding must have an applicability reason with source references.
Missing evidence alone is not sufficient evidence that a rule is not applicable.

A control gap is a failure to meet a requirement, with evidence of that failure.
An evidence gap means that assessment information is missing or not sufficient.
Keep the reviewer decision in a different record.

**ELI10:** A policy states what the bank intends to do.
An operational record can give evidence of what the bank did.

### Input limits

Retrieve public regulations and amendments through the external API.
Refresh before selection and before each current assessment.
Keep the exact retrieved version as assessment evidence.
Do not use S3 as the authority for current regulatory content.
Provider selection and current-source verification are pending under [D20](../decisions/gov-decision-log.md#d20---current-regulatory-retrieval).

Use clearly fictional bank documents for the demo.
Use the same process for authorized user uploads.
Do not describe fictional records as evidence from a bank.

Approved limits:

- 10 documents per case.
- 10 MB per file.
- 100 extracted document pages per case.
- Up to 20 selected obligations per assessment.

The [security specification](../security/03_SECURITY_ACCESS.md) gives rejection and scope rules.

### Work after the first release

Measure reviewer effort against a baseline from direct observation.
Expand the evidence collection after review.

These are future opportunities.
They are not submission requirements.
D24 makes retrieval measurements, assessment measurements, and runtime traces mandatory for this release.
Keep the two types of quality measurements different.

### Deferred functions

- OCR and multimodal interpretation.
- Other jurisdictions and bank categories.
- Reviewer roles that operate independently.
- Managed vector retrieval.
- Broad regulatory crawling and a scheduled monitor that operates independently.
- Changes to bank systems.

Do not claim the remaining brief features as additional functions for this release.
These include control effectiveness assessment, risk prioritization, autonomous impact analysis, what-if simulation, cross-regulation intelligence, and contradiction detection.

## 4. Success criteria

### Reviewer acceptance is the north star

The primary product measure is approval without edits.
The user's label for this measure is “north star.”
Measure how often the reviewer accepts an initial recommendation without edits.
Show the edited and rejected shares beside that rate.
Use one immutable finding and primary recommendation per selected obligation in a run as the review item.
Keep the initial AI content when the reviewer saves an edited version.

Let A, E, and R be the counts of Approved, Edited, and Rejected items.
Let N = A + E + R.
Use the latest saved final outcome for each item at the report cutoff.

| Product measure | Formula | Meaning |
|---|---|---|
| Approval rate, primary product measure | A / N | Accepted without edits. |
| Edit rate | E / N | Changed and accepted by the reviewer. |
| Rejection rate | R / N | Not accepted by the reviewer. |
| Adoption including edits | (A + E) / N | Accepted with or without changes. This is a secondary measure. |
| Review coverage | N / all eligible items | The share that received a final review. |

Show counts, pending items, cohort filters, and the report cutoff with every rate.
Show Not measured when the denominator is zero.
Requests for more evidence and unsaved drafts stay pending until a final outcome exists.
For an Edited outcome, changed content and a reason must be saved.
For a Rejected outcome, a reason must be saved.
Review revisions keep history and do not increase the item count.

Show result coverage, failed jobs, partial jobs, and unchecked obligations beside acceptance.
Do not hide missing results with reports of only completed or approved cases.
Use different result groups for synthetic demonstrations, controlled model simulations, held-out evaluations, and live authorized work.
There is no selected numerical acceptance target. Record the baseline before you set an improvement target.

Acceptance measures usefulness to the reviewer.
It is not sufficient evidence of correct regulatory interpretation or operation of a bank control.
Keep assessment agreement, contextual citation support, and critical evidence gates mandatory.
The [measurement contract](../testing/spec-measurement-contract.md) gives cohorts, formulas, traces, costs, and evaluation rules.

### Quality and delivery gates

| Metric | Target | Measurement |
|---|---|---|
| Feature coverage | Show all eight selected functions in operation. | Evidence for AC-F01–AC-F08 |
| Assessment agreement | At least 90% on at least 20 held-out labeled cases. | Expected outcomes and measured outcomes. Include a per-status confusion matrix. |
| Citation validity | 100% resolve to the intended snapshot passage. | Make sure that references resolve correctly and their context supports the finding. |
| Critical evidence failures | Zero false supported findings in designated missing, conflicting, or adversarial cases. | Explicit critical-case results |
| Correct software behavior | All applicable P0 local checks pass. No unexplained skips. | [Local test plan](../testing/spec-local-test-plan.md) |
| Correct measurements | Necessary formulas, trace records, privacy checks, and failure accounting pass their tests. | REQ-X07–REQ-X09 and the [measurement contract](../testing/spec-measurement-contract.md). |
| Cloud readiness | Do verification checks of private destinations, permissions, storage, jobs, and identity. | Evidence from the deployed system |
| Submission | A working demo and detailed structural architecture. | A rehearsed submission package |

These numerical quality limits have the user's approval.
The organizer did not give these limits.
A small benchmark is not sufficient evidence of general regulatory accuracy.
The final F/D claim must use recorded results.

### Baseline and improvement

Use one bounded agent and the approved model first.
Measure regulatory retrieval, bank-evidence retrieval, and assessment quality independently.
Record a trace for each stage, including failed and interrupted attempts.
Use recorded failures and costs to select the next experiment.
Then do a test of model routing or a second reviewer against that named problem.
Do not introduce either option automatically or replace the baseline without a recorded decision.

## 5. Product direction

A later release can repeat assessments when a rule or bank document changes.
Its history can record the requirement, selected evidence, assessment result, and human decision.

This is a product direction.
Continuous live monitoring, broad regulatory coverage, and enterprise readiness are future work.

## 6. Application procedure

1. Sign in.
2. Make a bank case or load the labeled fictional example.
3. Refresh regulations through the external API.
4. Upload policy documents, controls, and evidence.
5. Examine extraction results.
6. Select the applicable obligations.
7. Start the assessment.
8. Examine stage and tool events.
9. Open a finding and its source passages.
10. Select Approve, edit, or reject for the recommendation, or request more evidence before a final decision.
11. Keep the reviewer content and note in a different record from the AI finding.
12. Refresh regulations again.
13. Compare obligations and affected controls.
14. Export findings, citations, and review decisions as Markdown or JSON.

## Source record

Source: [ET AI Hackathon detailed problem statements](../../../hackthon_data/6ab20c4818adf_et_hackathon_detailed_problem_statements_branded.pdf).
The PDF has 14 pages.
Pages 2–4 describe the solution grid and submission rules.
Pages 5–6 describe Problem 1.

Source PDF SHA-256:

**51C4E3C7CFECE1E7F52EED3A1F81918FFC95625A59E77AA31CA37FC4B23A3483**

F1, F2, and F3 have minimum requirements of 3, 6, and 8 listed features respectively.
D1 uses mostly structured or textual input with satisfactory outputs in most situations.
For D2, evidence of high reliability with similar inputs is mandatory.
D3 adds heterogeneous multimodal input.

The submission must include a working demo and detailed structural architecture.
The brief warns against incorrect self-estimation.

## Pending verification

The exact submission cutoff is unknown.
There are no verification results for runtime versions, AWS access, the regulatory source collection, or evaluation results.
Read [D15](../decisions/gov-decision-log.md).
Do not record these items as completed.

[Next: Technical blueprint](../architecture/02_TECHNICAL_BLUEPRINT.md)
