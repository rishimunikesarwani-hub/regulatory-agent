# PRD - The Regulatory Agent

> Status: Approved in the planning conversation. First saved on 2026-10-08.
> Purpose: Help an Indian bank reviewer connect requirements to controls, evidence, gaps, and proposed corrections.
> Scope: [D01–D06](../decisions/gov-decision-log.md).
> Language revision: 2026-10-09. Use ASD-STE100 writing rules under D18.

## 1. Problem

The brief requires an agentic system for banking regulations.
The system must track changes, assess internal controls, identify gaps, and suggest corrections.

The brief defines this relationship:

**Regulations → obligations → applicability → policies/controls → evidence → testing → gaps → remediation → monitoring.**

A reviewer must be able to inspect the full relationship.
Each supported finding needs an accessible source passage and document version.
If evidence is missing, the system must state what it cannot establish.

This problem definition comes from the brief.
Market size, customer demand, and time savings remain unverified.

## 2. Users and scope

- **Primary user:** An IT compliance analyst at an Indian commercial bank.
- **Task:** Compare documented controls and supplied evidence with selected applicable requirements.
- **Reviewer:** A person who accepts a finding, disagrees with it, or requests more evidence.
- **First-release institution:** A domestic commercial-bank scenario.
- **Case scope:** One bank profile per case.

The project has not observed the user's existing process.
It has no measured time-saving baseline.
Document comparison and evidence collection are intended application functions, not verified research findings.

One authenticated operator can do the review in the demo.
This does not establish independent two-person approval.

## 3. Required first-release functions

The eight functions below come from the organizer's feature list.

| Requirement | Brief feature | Required behavior | Acceptance case |
|---|---|---|---|
| REQ-F01 | 1. Regulatory intelligence and knowledge ingestion | Retrieve current regulations through an external API. Keep authoritative sources, versions, verification times, and source locations. | AC-F01: The reviewer can inspect a clause, its authority, and its verification time. Block current assessments if verification fails. |
| REQ-F02 | 2. Regulatory change intelligence | Compare two specified versions. Show changed obligations and affected control mappings. | AC-F02: A changed requirement creates a new assessment snapshot. The old assessment remains accessible. |
| REQ-F03 | 3. Regulatory obligation extraction | Extract specific requirements, stated applicability, and clause references. | AC-F03: Keep source conditions, exceptions, and scope. |
| REQ-F04 | 4. Bank control-framework understanding | Extract stated controls and purposes. Extract owners and frequencies only when the source supplies them. | AC-F04: Keep missing fields unknown. Do not invent values. |
| REQ-F05 | 5. Regulatory-to-control mapping | Connect applicable requirements to relevant controls. Include reasons and source references. | AC-F05: An unrelated control does not establish sufficient coverage. |
| REQ-F06 | 7. Evidence-based compliance assessment | Compare supplied evidence with the requirement. Keep uncertainty visible. | AC-F06: A policy alone cannot prove that an operational control occurred. |
| REQ-F07 | 8. Gap identification | Identify evidenced control gaps and evidence gaps. Keep their meanings separate. | AC-F07: Missing records cause an evidence gap or needs-review result. They do not prove an operational failure. |
| REQ-F08 | 10. Remediation recommendation engine | Propose a correction or evidence request. Connect it to the obligation and finding. | AC-F08: The reviewer can inspect the proposal's source and record a decision. Keep the original finding. |

The following requirements support the eight functions.

| Requirement | Behavior | Acceptance case |
|---|---|---|
| REQ-X01 | Bounded agent tools and job allowances | AC-X01: Stop safely for prohibited actions or exhausted allowances. |
| REQ-X02 | Case ownership and India-only private processing | AC-X02: Deny cross-case access. Verify cloud destinations before private uploads. |
| REQ-X03 | Fixed snapshots and valid citations | AC-X03: A replacement document cannot change an active assessment. |
| REQ-X04 | Saved asynchronous jobs | AC-X04: Retries cannot create a second active assessment or a second final report. |
| REQ-X05 | Reviewer interface and export | AC-X05: Source inspection, review decisions, and exports keep the evidence relationship. |
| REQ-X06 | Separate local and cloud operation | AC-X06: Default checks need no AWS credentials. Simulated results have visible labels. |

### Finding terms

A supported finding means that supplied evidence supports the selected requirement.
It does not certify the bank.
It does not establish inspection of live bank systems.

Use these finding status values:

- supported
- partial
- gap
- needs_review
- not_applicable

Also record the evidence condition: sufficient, partial, missing, or conflicting.

A not_applicable finding needs a source-backed applicability reason.
Missing evidence alone does not establish that a rule is not applicable.

A control gap is an evidenced shortfall against a requirement.
An evidence gap means that assessment information is missing or insufficient.
Keep the reviewer disposition in a separate record.

**ELI10:** A policy states what the bank intends to do.
An operational record can show what the bank actually did.

### Input limits

Retrieve public regulations and amendments through the external API.
Refresh before selection and before each current assessment.
Keep the exact retrieved version as assessment evidence.
Do not use S3 as the authority for current regulatory content.
Provider selection and current-source verification remain pending under [D20](../decisions/gov-decision-log.md#d20---current-regulatory-retrieval).
Use clearly fictional bank documents for the demo.
Support authorized user uploads through the same process.
Do not describe fictional records as real bank evidence.

Approved limits:

- 10 documents per case.
- 10 MB per file.
- 100 extracted document pages per case.
- Up to 20 selected obligations per assessment.

The [security specification](../security/03_SECURITY_ACCESS.md) defines rejection and scope rules.

### Work after the first release

Measure reviewer effort against an observed baseline.
Use evaluation failures to improve retrieval.
Expand the evidence collection after review.

These are future opportunities.
They are not submission requirements.

### Deferred functions

- OCR and multimodal interpretation.
- Other jurisdictions and bank categories.
- Independent reviewer roles.
- Managed vector retrieval.
- Broad regulatory crawling and an independent scheduled monitor.
- Changes to bank systems.

Do not separately claim the remaining brief features for this release.
These include control effectiveness assessment, risk prioritization, autonomous impact analysis, what-if simulation, cross-regulation intelligence, and contradiction detection.

## 4. Success criteria

| Metric | Target | Measurement |
|---|---|---|
| Feature coverage | Demonstrate all eight selected functions. | Evidence for AC-F01–AC-F08 |
| Assessment agreement | At least 90% on at least 20 held-out labelled cases. | Expected and actual outcomes. Include a per-status confusion matrix. |
| Citation validity | 100% resolve to the intended snapshot passage. | Verify reference resolution and contextual support. |
| Critical evidence failures | Zero false supported findings in designated missing, conflicting, or adversarial cases. | Explicit critical-case results |
| Software correctness | All applicable P0 local checks pass. No unexplained skips. | [Local test plan](../testing/spec-local-test-plan.md) |
| Cloud readiness | Verify private destinations, permissions, storage, jobs, and identity. | Actual deployment evidence |
| Submission | A working demo and detailed structural architecture. | A rehearsed submission package |

The user approved these numerical quality limits.
The organizer did not specify these limits.
A small benchmark does not prove general regulatory accuracy.
The final F/D claim must use observed results.

## 5. Product direction

A later release can repeat assessments when a rule or bank document changes.
Its history can record the requirement, selected evidence, assessment result, and human decision.

This is a product direction.
Continuous live monitoring, broad regulatory coverage, and enterprise readiness remain future work.

## 6. Application procedure

1. Sign in.
2. Create a bank case or load the labelled fictional example.
3. Refresh regulations through the external API.
4. Upload policy documents, controls, and evidence.
5. Inspect extraction results.
6. Select the applicable obligations.
7. Start the assessment.
8. Inspect stage and tool events.
9. Open a finding and its source passages.
10. Record agreement, disagreement, or a request for evidence.
11. Keep the reviewer note separate from the AI finding.
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

F1, F2, and F3 require at least 3, 6, and 8 listed features respectively.
D1 uses mostly structured or textual input with acceptable outputs in most situations.
D2 requires demonstrably high reliability with similar inputs.
D3 adds heterogeneous multimodal input.

The submission needs a working demo and detailed structural architecture.
The brief warns against incorrect self-estimation.

## Pending verification

The exact submission cutoff remains unknown.
Runtime versions, AWS access, the regulatory source collection, and evaluation results remain unverified.
Read [D15](../decisions/gov-decision-log.md).
Do not report these items as complete.

[Next: Technical blueprint](../architecture/02_TECHNICAL_BLUEPRINT.md)
