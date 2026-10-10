# Feature tickets

> Status: Approved in the planning conversation. Persisted 2026-10-08.
> Depends on: [PRD](../product/01_PRD.md), [Technical Blueprint](../architecture/02_TECHNICAL_BLUEPRINT.md), [Security](../security/03_SECURITY_ACCESS.md), and [Frontend](../frontend/04_FRONTEND_SPEC.md).
> Decisions: [D12–D14](../decisions/gov-decision-log.md).
> Implementation state: Documentation saved. Application work and fixture acquisition remain pending.

First, assess one obligation through the complete process. Record its source, mapped control, evidence, finding, and review decision. Then extend the process.

## Priority and status

- **P0:** Required for the scoped submission.
- **P1:** Useful after the scoped release. Not on its critical path.
- **P2:** Deferred exploration.

All T1–T9 below are P0. Each ticket contains work that can be verified. Record incomplete work. Do not mark an incomplete ticket as complete.

## T1 — Specifications and fixtures

**Status:** In progress: specification persistence complete. Source and fixture work not started.  
**Dependencies:** None.  
**Requirements:** All requirement IDs. Especially REQ-F01–REQ-F08 and REQ-X03.

Save the approved five documents, their decisions, and test/evaluation contracts. Acquire and freeze appropriate public RBI source versions and a clearly fictional bank evidence pack.

Acceptance:
- [x] Five individually approved specifications saved in their agreed nested locations.
- [x] Decision history, source-brief fingerprint, local test plan, and AI evaluation plan saved.
- [ ] Select the external regulatory retrieval provider. Verify authority coverage, update delay, versions, amendments, terms, and pricing.
- [ ] Acquire the regulatory source files. Record authority, publication/effective dates, scope, version, URL, retrieval time, and content hash.
- [ ] Verify a genuine change pair or explicitly label a constructed change as a simulation. Never present a synthetic amendment as an RBI event.
- [ ] Create a fictional bank profile, policies, controls, and planted evidence/control gaps with source-linked expected outcomes.
- [ ] Separate development examples from at least 20 held-out evaluation cases before tuning prompts.
- [x] Validate the documentation package. Link its report in LOG.md.

**Source candidates:** Planning research identified [RBI's Master Directions index](https://www.rbi.org.in/scripts/BS_ViewMasterDirections.aspx), [a current-direction candidate](https://www.rbi.org.in/scripts/BS_ViewMasDirections.aspx?id=13643), and [a historical-version candidate](https://www.rbi.org.in/scripts/NotificationPreVersion.aspx?Histid=250&id=13643). A later request for the two content pages failed. Get the source files. Verify their text, applicability, and dates before fixture use. Do not describe a 2023 document as current without verification.

## T2 — Local test environment and executable contracts

**Status:** Not started.  
**Dependencies:** T1's specifications and minimum labelled fixture.  
**Requirements:** REQ-X06 and the contract surfaces for all features.

Create the minimal local developer environment. Pin compatible runtime/dependency versions. Freeze executable data/API schemas and adapter contracts before application handlers.

Acceptance:
- [ ] One documented command runs default local checks without AWS credentials or external network calls.
- [ ] Loopback browser/API tests remain permitted. External-network blocking is verified in actual worker processes.
- [ ] Filesystem, SQLite, local job runner, and controlled model adapters satisfy shared contracts.
- [ ] Define the regulatory API schema and controlled local responses. Set bounded retrieval requests, retries, timeouts, pagination, and sizes.
- [ ] Nonpaginated extracted-size/page-equivalent handling is explicitly specified and tested before upload enforcement is claimed.
- [ ] Requirement IDs and corresponding red/green test evidence are recorded.
- [ ] Dependency/runtime locks and setup instructions work from a clean environment.

## T3 — Documents and traceability

**Status:** Not started.  
**Dependencies:** T2.  
**Requirements:** REQ-F01, REQ-X02, REQ-X03.

Implement bank-file validation, extraction, source locations, immutable versions, and selected-snapshot retrieval.
Implement regulatory API refresh and current-source verification.

Acceptance:
- [ ] PDF, DOCX, TXT, and CSV preserve their appropriate source locations.
- [ ] Invalid, encrypted, scanned, unreadable, unsupported, or oversized input is rejected clearly.
- [ ] File and aggregate limits are enforced without silent truncation.
- [ ] Citation quotes resolve to the exact selected document version.
- [ ] Refresh before selection and revalidate before assessment. Block failures and changed selections.
- [ ] Detect amendments, replacements, withdrawals, and effective-date changes. Preserve historical assessment evidence.
- [ ] The external API receives public source queries only. Enforce destination and response limits.
- [ ] Replacing a file creates a new version and does not change an existing or running assessment.

## T4 — First complete assessment slice

**Status:** Not started.  
**Dependencies:** T3.  
**Requirements:** REQ-F03–REQ-F08.

Use the local adapter contracts. Implement one complete sequence: obligation → control → evidence → finding → remediation.

Acceptance:
- [ ] Conditions and applicability remain attached to the extracted obligation.
- [ ] A relevant control is mapped with source references.
- [ ] Missing operational evidence cannot be replaced by a policy promise.
- [ ] Findings distinguish supported, partial, gap, needs_review, and not_applicable according to the rubric.
- [ ] Evidence gaps and evidenced control failures remain distinguishable.
- [ ] Proposed fixes and reviewer decisions are linked to the original finding.

## T5 — Bounded agent and regulatory changes

**Status:** Not started.  
**Dependencies:** T4.  
**Requirements:** REQ-F02–REQ-F08, REQ-X01, REQ-X03.

Add validated model-selected tool actions, controlled retrieval refinement, and explicit version comparisons. Expand only to the approved obligation scope.

Acceptance:
- [ ] The agent selects permitted tools through validated structured actions.
- [ ] Scope filters apply before retrieval, and injected instructions cannot grant additional capabilities.
- [ ] Invalid JSON, rejected actions, and retried calls consume the same persisted call budget.
- [ ] A material regulatory change identifies affected obligations/controls and produces a new snapshot.
- [ ] Cosmetic changes do not automatically become changed obligations.
- [ ] Stale evidence, unavailable tools, budget exhaustion, and partial results follow the specification.

## T6 — API, jobs, ownership, and review records

**Status:** Not started.  
**Dependencies:** T4. Shared contracts from T2.  
**Requirements:** REQ-X02–REQ-X05.

Implement short owner-scoped API requests and durable asynchronous execution. Keep review records separate from AI findings.

Acceptance:
- [ ] Start operations return job IDs and stable input snapshots.
- [ ] Access checks cover cases, uploads, source previews, jobs, findings, and exports.
- [ ] Duplicate requests/messages yield one active execution and one finalized result.
- [ ] Counters, deadlines, execution claims, and stage outputs survive retries/restarts.
- [ ] Partial and failed outcomes preserve attributable work and expose unchecked obligations.
- [ ] Review saves cannot overwrite the AI finding or create duplicate decisions on retry.

## T7 — Review interface

**Status:** Not started.  
**Dependencies:** T5 and T6.  
**Requirements:** REQ-X05, REQ-X06. AC-F01–AC-F08.

Implement the approved case workspace, source inspection, change comparison, and exports.

Acceptance:
- [ ] Browser tests cover upload → assessment → citation inspection → review → comparison → export.
- [ ] Source previews resolve to the original snapshot after a document replacement.
- [ ] Synthetic data and simulated model outputs are labelled independently.
- [ ] Loading, empty, denied, partial, and failed states are useful and truthful.
- [ ] Keyboard navigation and a viewport below 768 px work.
- [ ] Export retains versions, evidence, run status, reviewer records, and limitations.
- [ ] Show authority verification time and freshness failures. Export that metadata.

## T8 — AWS integration and Rishi's guided deployment

**Status:** Not started.  
**Dependencies:** T6 and T7. Begin connectivity checks when the local slice is stable.  
**Requirements:** REQ-X02, REQ-X04, REQ-X06.

Implement the SAM configuration and AWS adapters. Validate both. Explain each service and configuration step during T8.

Acceptance:
- [ ] Validate infrastructure configuration and review the concrete resources, permissions, expected costs, and rollback/cleanup approach before deployment.
- [ ] Guide Rishi through account/role access without asking for secrets in chat.
- [ ] Verify the pinned model's account access, SDK/API shape, inference-profile destinations, and applicable retention configuration.
- [ ] Run a small live call using synthetic input before private documents.
- [ ] Verify real Cognito login, ownership, S3 privacy, records, queue processing, and worker permissions.
- [ ] Check that development identity cannot run in the cloud configuration.
- [ ] Verify live regulatory API access, authority synchronization, change detection, failure handling, and absence of private request content.
- [ ] Document the commands and observed outputs in a step-by-step deployment guide and dated run record.
- [ ] Leave private uploads disabled until the required region/access checks pass.

Available credits do not prove model access. They do not permit unlimited spending. Record the cost estimate and spending controls during the deployment instructions.

## T9 — Quality and submission evidence

**Status:** Not started.  
**Dependencies:** T8 and completed T1 held-out set.  
**Requirements:** All feature acceptance cases and release gates.

Run the live evaluation. Rehearse the demonstration. Document the architecture of the implemented system. Include decisions, tool actions, model use, and failure handling.

Acceptance:
- [ ] At least 20 held-out cases run with the pinned live model and recorded prompt/model versions.
- [ ] At least 90% expected-assessment agreement. All cases accounted for, including abstentions and errors.
- [ ] All reported citations resolve to the intended passage, and contextual support is checked.
- [ ] Zero false supported findings in designated critical evidence/adversarial cases.
- [ ] All eight feature claims link to demonstrated behaviour and evidence.
- [ ] Remaining failures and scope limits appear in the report. The F/D claim follows actual evidence.
- [ ] Working demo, architecture, and rehearsal record are ready before submission.
- [ ] The user performs or explicitly authorizes the external submission. Preparing this package does not authorize sending it.

## Build order and dates

**8 October target:** Prepare the sources, fixtures, and local environment. Implement the first complete assessment. T5 and T6 extend that assessment. T7 adds the review interface.

**9 October target:** Complete guided AWS integration and live evaluation. Correct failures. Rehearse the demonstration. Complete the architecture documents. Target completion that evening IST.

**10 October:** Submission date. The exact organiser cutoff remains unverified. These dates are targets. They do not show completed work.

Exclude P1/P2 work from this delivery sequence unless the user explicitly changes the scope. See the [PRD](../product/01_PRD.md) for deferred capabilities.

[Next: Local test plan](../testing/spec-local-test-plan.md)
