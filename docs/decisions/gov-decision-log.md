# Decision log

> Persisted: 2026-10-08.
> Source of approval: the planning conversation across 7–8 October 2026.
> Exact per-answer timestamps were not captured. The date below is the persistence date, not an invented approval timestamp.

This record gives each decision and its reason. It separates approved choices from facts that need verification.

**Approved** means the user selected or accepted it. **Implementation clarification** makes an approved requirement precise without adding a product capability. **Unverified** means evidence is still needed. No entry below establishes that the application is built.

## Approved decisions

| ID | Recorded | Decision and rationale | Specification and acceptance links |
|---|---|---|---|
| D01 | 2026-10-08 | **Approved:** Work on Problem 1, banking/financial regulations. Build the traceable regulation-to-remediation workflow described in the source brief. | [PRD](../product/01_PRD.md). REQ-F01–REQ-F08 |
| D02 | 2026-10-08 | **Approved:** Target F3/D2: at least eight selected features with demonstrable reliability on mostly structured/textual input. This is a target, not an achieved score. | [PRD metrics](../product/01_PRD.md). [quality gates](../testing/eval-model-quality.md) |
| D03 | 2026-10-08 | **Approved:** Start with India IT controls for a domestic commercial-bank scenario. One bank profile per case keeps applicability and evidence scope concrete. | [PRD audience](../product/01_PRD.md). AC-F03, AC-F05 |
| D04 | 2026-10-08 | **Approved:** Support both a clearly fictional demo bank and authorized user uploads. Fictional documents must remain labelled. | [PRD inputs](../product/01_PRD.md). UT-01, BT-05 |
| D05 | 2026-10-08 | **Approved:** Private document storage and AI processing must stay within AWS India. Mumbai is the application region. The selected inference profile may use Mumbai/Hyderabad only after verification. | [Security](../security/03_SECURITY_ACCESS.md). CLOUD-01, CLOUD-02 |
| D06 | 2026-10-08 | **Approved:** Submission is 10 October 2026. The user corrected the earlier “within seven days” answer. Internal readiness targets 9 October evening IST. Exact organiser cutoff remains unverified. | [Delivery dates](../delivery/05_FEATURE_TICKETS.md) |
| D07 | 2026-10-08 | **Approved:** Design cloud-native now. Teach AWS hosting/configuration step by step when the local workflow is ready. Local tests must not require AWS setup. | [Architecture](../architecture/02_TECHNICAL_BLUEPRINT.md). CT-01, CLOUD-01–CLOUD-05 |
| D08 | 2026-10-08 | **Approved:** React/TypeScript/Vite. Python/FastAPI. API Gateway/Lambda. S3. DynamoDB. SQS. Cognito. SAM. Local filesystem, SQLite, worker, and controlled-model adapters share the application contracts. | [Stack and flow](../architecture/02_TECHNICAL_BLUEPRINT.md). CT-01–CT-04 |
| D09 | 2026-10-08 | **Approved:** One bounded agent, keyword/BM25 retrieval, application-validated actions, and pinned model profile in.openai.gpt-5.6-luna. No silent global fallback or managed-vector-service addition. Quality and account access are unverified. | [Agent/model contract](../architecture/02_TECHNICAL_BLUEPRINT.md). UT-07–UT-10, CLOUD-01 |
| D10 | 2026-10-08 | **Approved:** Use Cognito sign-in, own-case permissions, and India processing. Limits: 10 documents/case, 10 MB/file, and 100 extracted pages. Each run permits up to 20 obligations, 24 model calls, and a ten-minute job budget. One operator can review own findings. No independent dual approval is claimed. | [Security](../security/03_SECURITY_ACCESS.md). UT-02, UT-07–UT-12, CT-02–CT-04 |
| D11 | 2026-10-08 | **Approved:** Default light reviewer workspace, Cases/Documents/Assessment/Changes flows, exact source inspection, separate human review, progress events, and Markdown/JSON exports. Reference screenshots: NONE — design risk, accepted by the user. | [Frontend](../frontend/04_FRONTEND_SPEC.md). BT-01–BT-05 |
| D12 | 2026-10-08 | **Approved:** Separate nested Markdown specifications under ET-Hackathon/MVP, a start page, and durable decision history. The original style used Rishi Voice with 60% rawness. D18 replaces that style. Preserve literal contracts. | [Handbook](../guide-start-here.md). [project instructions](../../AGENTS.md) |
| D13 | 2026-10-08 | **Approved:** Use at least 20 held-out cases. Require at least 90% assessment agreement. All citations must resolve and support their claims. Require zero false supported results on designated critical evidence/adversarial cases. These are our gates, not organiser-issued numerical thresholds. | [Evaluation plan](../testing/eval-model-quality.md). EVAL-01–EVAL-20 |
| D14 | 2026-10-08 | **Approved:** T1–T9 build order and spec → failing test → implementation → refactor → verification loop. Persist documentation first. The present implementation request executes that documentation plan. Application tickets remain pending. | [Tickets](../delivery/05_FEATURE_TICKETS.md). [local checks](../testing/spec-local-test-plan.md) |

## D15 — Unverified facts and later configuration

Recorded 2026-10-08. These are not approvals or established facts.

| Open item | Current state | Resolve in |
|---|---|---|
| AWS account, permissions, model entitlement | User requested a later teaching walkthrough. Account readiness was not established | T8 |
| Numerical cloud spending ceiling | User chose credits available / flexible. No amount confirmed | T8 resource/cost review |
| Actual model quality | No live evaluation has run | T9 |
| Regulatory corpus and genuine change pair | Source leads exist. The actual authoritative versioned files have not been acquired or validated in this workspace | T1 |
| Runtime/dependency versions and SDK support | Not installed or pinned for this project | T2. Live confirmation T8 |
| Nonpaginated page-equivalent handling | Must be made explicit before claiming aggregate extraction limits are enforced | T2 |
| Retention, cleanup, and applicable provider terms | No automatic deletion schedule approved. Review before real private uploads | T8 |
| Exact submission cutoff | User supplied the date only | Before submission. Internal target remains earlier |
| Market demand and productivity improvement | No user research or measured baseline | Future discovery. Do not invent claims |

## D16 — Implementation clarifications preserved in the written specs

Recorded 2026-10-08. **Status: implementation clarifications, not separately attributed user answers.**

These make the approved evidence, retry, and review requirements testable:
- A supported finding needs the required evidence elements. A policy assertion cannot prove an operational act.
- Missing/conflicting evidence, partial fulfilment, and a demonstrated gap are distinct outcomes.
- A reviewer decision does not overwrite the AI assessment.
- Each job freezes the bank profile, selected documents, extracted passages, and model/prompt versions.
- Citations use the original PDF page, DOCX paragraph/table cell, TXT line, or CSV row. Every quote is checked.
- Model-call allowances are reserved before dispatch and persist through failures, retries, and uncertain outcomes.
- The ten-minute processing clock begins at worker start and does not restart on redelivery. Queue wait is recorded separately.
- Completed, partial, and failed jobs must reflect whether all selected obligations were accounted for.
- Failed outputs and abstentions remain in the evaluation denominator.
- Supporting UI text/status colours and technical field names are implementation defaults, not additional user-research findings.

Affected documents: [architecture](../architecture/02_TECHNICAL_BLUEPRINT.md), [security](../security/03_SECURITY_ACCESS.md), [local tests](../testing/spec-local-test-plan.md), and [evaluation](../testing/eval-model-quality.md).

## D17 — Technical blueprint language

Recorded 2026-10-09. **Status: approved language change.**

The user requested ASD-STE100 language, then identified the technical architecture as the target document. Rewrite the [technical blueprint](../architecture/02_TECHNICAL_BLUEPRINT.md) with ASD-STE100 Issue 9 writing rules.

D17 replaced D12's Rishi Voice style for the technical blueprint only. Other documents retained that style until D18. The change preserved application scope, privacy rules, interfaces, identifiers, limits, quality gates, and approval history. It did not authorize application implementation or deployment.

Preserve the [original wording](../../runs/2026-10-09-technical-blueprint-before-ste100.txt). Record the language and preservation checks in the [verification record](../../runs/2026-10-09-ste100-verification.md). The rewrite does not establish independently verified compliance with the complete STE dictionary.

Affected specification: [Technical Blueprint](../architecture/02_TECHNICAL_BLUEPRINT.md). Existing requirement, test, and ticket references remain unchanged.

## D18 — Project Markdown language

Recorded 2026-10-09. **Status: approved language change.**

The user requested ASD-STE100 for all current ET-Hackathon Markdown files and all new projects.
The user requested this rule in the global AGENTS.md.
Do not rewrite other existing projects without a separate request.

D18 replaces the Rishi Voice style in D12 for all project Markdown.
It extends the language scope of D17 to the complete project.
Other approved product decisions remain in effect.

Apply the [writing guide](../guide-ste100-writing.md).
Keep requirements, identifiers, numbers, links, commands, uncertainty, and approval history.
Keep source quotations unchanged when exact wording is necessary.
Review sentence length, technical terms, and meaning.
A sentence-length check does not prove full dictionary compliance.

Global instruction file: `C:\Users\Be Flith Rich\AGENTS.md`.
The global rule applies to new projects and this project.
A different style requires an explicit document request from the user.

The [backup archive](../../runs/2026-10-09-before-project-ste100.zip) preserves the 14 original Markdown files.
The [source manifest](../../runs/2026-10-09-ste100-source-manifest.json) records their paths and hashes.
The [verification record](../../runs/2026-10-09-project-ste100-verification.md) records the current checks.

## D19 - Project name

Recorded 2026-10-09. **Status: approved name change.**

The user selected The Regulatory Agent as the project name.
This name replaces Banking Control Assurance.
Use `the-regulatory-agent` as the manifest identifier.
The README and PRD use the selected name.
The application scope and requirements remain unchanged.

## D20 - Current regulatory retrieval

Recorded 2026-10-09. **Status: approved design change.**

The user requested current regulatory retrieval through an external API instead of a static S3 regulatory source.
The user requested only the necessary document corrections.
The user chose to keep the provider undecided.

The API supplies current public regulations, amendments, replacements, and withdrawals.
Refresh before source selection.
Revalidate selected versions before each current assessment.
Record authority verification time and freshness status.
Block a current assessment if verification fails or selected versions changed.

Keep private bank content and model processing within India.
The external regulatory API receives public source queries only.
S3 retains bank files and immutable assessment evidence copies.
It does not determine the current regulatory version.

Keep assessment snapshots and historical citations unchanged.
Compare new versions without overwriting previous findings.
An independent scheduled monitor remains future work.
Current-source verification does not guarantee zero update delay.

D20 changes the source-retrieval parts of D07–D09 and the PRD's manual regulatory loading process.
The broader deferred crawling scope remains deferred.
All model limits, document limits, quality gates, and review rules remain in effect.

Provider endpoint, coverage, update delay, versions, terms, credentials, and pricing remain TBD.
No regulatory API has been selected, implemented, or live-tested.

Affected requirements: REQ-F01, REQ-F02, REQ-X01, REQ-X02, REQ-X03, REQ-X04, REQ-X05, and REQ-X06.
Affected delivery tasks: T1, T2, T3, T5, T7, and T8.
See the [blueprint](../architecture/02_TECHNICAL_BLUEPRINT.md#current-regulatory-sources) for the controlling contract.

## D21 - Technical architecture views

Recorded 2026-10-09. **Status: approved document change.**

The user requested ArchView diagrams for the full Regulatory Agent.
The user explicitly excluded a crawler view and retained the external retrieval API.
Provider selection remains undecided under D20.

The [blueprint](../architecture/02_TECHNICAL_BLUEPRINT.md#architecture-views) links the system and assessment views.
Each view has an editable JSON source and an HTML output.
The ASD-STE100 skill reviewed the blueprint again.
Its complete dictionary review remains unavailable.

This decision changes architecture presentation and wording.
It does not add application features or authorize deployment.
All approved models, regions, limits, evidence rules, and access rules remain.
See the [verification record](../../runs/2026-10-09-archview-verification.md).

## How to add a decision

Append a new entry with:
1. Stable ID and recorded date.
2. Status: proposed, approved, implementation clarification, unverified, or superseded.
3. The decision and its reason.
4. Approval/source evidence, without invented timestamps.
5. Affected specification, requirement IDs, tests, and tickets.
6. Any decision it replaces.

Update the authoritative spec in the same change. Keep superseded history and link to its replacement. Minor wording changes do not need new product approval. Changes to scope, privacy, budgets, quality gates, or external actions need approval.

[Next: Local test plan](../testing/spec-local-test-plan.md)
