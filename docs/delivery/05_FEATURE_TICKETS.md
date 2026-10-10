# Feature tickets

> Status: The user gave approval during planning. Saved 2026-10-08.
> Depends on: [PRD](../product/01_PRD.md), [Technical Blueprint](../architecture/02_TECHNICAL_BLUEPRINT.md), [Security](../security/03_SECURITY_ACCESS.md), and [Frontend](../frontend/04_FRONTEND_SPEC.md).

> Decisions: [D12–D14](../decisions/gov-decision-log.md) and [D24](../decisions/gov-decision-log.md#d24---reviewer-outcomes-and-measured-agent-baseline).
> Measurement requirements: [Measurement contract](../testing/spec-measurement-contract.md). Approval is under D24. Application measurements are not available.
> Development state: Session A and Session B foundations are integrated. The combined offline checks passed 60 tests.
> Remaining work: T1 and T2 D24 additions, followed by T3 through T9. See the [worktree handoffs](guide-next-worktrees.md).

First, do an assessment of one obligation through the full process. Record its source, mapped control, evidence, finding, and review decision. Then extend the process.

The measurement contract controls reviewer outcomes, retrieval scores, assessment quality, traces, and cost calculations.
Keep one agent and the approved model `in.openai.gpt-5.6-luna` for the baseline.
Use code for fixed rules, access, workflow routing, retries, budgets, validation, and progress.
Keep the 24-call allowance and 600-second worker deadline.
These tickets are not evidence of completed tests or measured improvement.

## Priority and status

- **P0:** Necessary for the scoped submission.
- **P1:** Useful after the scoped release. Not on its critical path.
- **P2:** Deferred exploration.

All T1–T9 below are P0. Each ticket contains work with verification criteria. Record work that is not completed. Do not give it a completed status.

For each behavior, record its failing test result before you write the application code.
Then record the passing result and regression checks for affected behavior.
A test plan or a later passing result alone does not meet this sequence requirement.

## T1 — Specifications and fixtures

**Status:** In progress. Historical sources and synthetic fixtures are integrated. Provider verification and D24 fixture additions are pending.

**Dependencies:** None.

**Requirements:** All requirement IDs. Especially REQ-F01–REQ-F08, REQ-X03, and REQ-X07–REQ-X09.

Save the approved five documents, their decisions, and test/evaluation contracts.
Get applicable public RBI source versions and a clearly fictional bank evidence pack.
Keep these versions unchanged.

Acceptance:
- [x] Five specifications with individual approval saved in their agreed nested locations.
- [x] Decision history, source-brief fingerprint, local test plan, and AI evaluation plan saved.
- [ ] Select the external regulatory retrieval provider. Do verification checks of authority coverage, update delay, versions, amendments, terms, and pricing.
- [x] Get the historical regulatory source files with the specified metadata. Current coverage stays unverified.
- [x] Identify the constructed changes as simulations. No simulated amendment represents an RBI event.
- [x] Make a fictional bank profile, policies, controls, and intentional evidence/control gaps with expected-outcome source references.
- [x] Keep three development examples and 20 held-out assessment cases in different data sets before prompt tuning.
- [ ] Before retrieval evaluation, give labels to the necessary source versions and source spans. Include decisive exceptions, conflicts, irrelevant passages, and missing evidence.
- [ ] Record annotation rules and domain-review status. Do not use the model under evaluation as the only label authority.
- [ ] Prepare review histories covering Approved, Edited, Rejected, pending actions, revisions, duplicate requests, empty cohorts, and partial jobs.
- [ ] Prepare controlled clocks, model responses, usage records, and failures for the measurement tests.
- [x] Validate the documentation package. Put a link to its report in LOG.md.

**Measurement checks:** UT-13–UT-18 and RET-01–RET-06 use these fixtures. The existing EVAL-01–EVAL-20 assessment cases are mandatory.

**Source candidates:** Planning research identified [RBI's Master Directions index](https://www.rbi.org.in/scripts/BS_ViewMasterDirections.aspx), [a current-direction candidate](https://www.rbi.org.in/scripts/BS_ViewMasDirections.aspx?id=13643), and [a historical-version candidate](https://www.rbi.org.in/scripts/NotificationPreVersion.aspx?Histid=250&id=13643). A later request for the two content pages failed. Get the source files. Do verification checks of their text, applicability, and dates before fixture use. Do not describe a 2023 document as current without verification.

## T2 — Local test environment and executable contracts

**Status:** In progress. Local contracts and adapters are integrated. The D24 measurement contracts and their checks are pending.

**Dependencies:** T1's specifications and minimum labeled fixture.

**Requirements:** REQ-X06–REQ-X09 and the contract surfaces for all features.

Prepare the minimum local developer environment. Use compatible runtime/dependency versions that do not change.
Save executable data/API schemas and adapter contracts before you write application handlers. Keep those contracts unchanged.

Acceptance:
- [x] One documented command starts default local checks without AWS credentials or external network calls.
- [x] Worker-process checks permit loopback traffic and block external Python network calls. This control is not an operating-system firewall.
- [x] Filesystem, SQLite, local job runner, and controlled model adapters satisfy the original shared contracts. D24 additions are pending.
- [x] Regulatory schemas and controlled responses include request, retry, timeout, pagination, and size limits. A live transport is pending.
- [x] Extracted-size and page-equivalent rules passed contract tests. Actual file parsers and upload-limit enforcement are pending under T3.
- [ ] Write schemas for immutable review items, saved review events, cohort filters, cutoffs, and aggregate reports under the measurement contract.
- [ ] Write schemas for stage and attempt records with stable IDs, versions, status, timing, usage, and safe error fields.
- [ ] Write different contracts for retrieval evaluation and assessment evaluation. Keep controlled tests in a different result group from live quality measurements.
- [ ] Records include requirement IDs and the related failing and passing test evidence.
- [x] Dependency/runtime locks and setup instructions passed the recorded clean-copy check.

**Measurement checks:** UT-13–UT-18 and CT-06–CT-08 cover formulas, history, retrieval scoring, traces, cost, privacy, persistence, exports, and baseline configuration.
Write each behavior test before its application code. Use the recorded failing and passing results for ticket acceptance.

## T3 — Documents and traceability

**Status:** Not started.

**Dependencies:** T2.

**Requirements:** REQ-F01, REQ-X02, REQ-X03, REQ-X08, REQ-X09.

Write code for bank-file validation, extraction, source locations, immutable versions, and selected-snapshot retrieval.
Write code for regulatory API refresh and current-source verification.

Acceptance:
- [ ] PDF, DOCX, TXT, and CSV keep the applicable source locations.
- [ ] Input rejection gives a clear reason for invalid, encrypted, scanned, unreadable, unsupported, or oversized input.
- [ ] File and aggregate limits apply without silent truncation.
- [ ] Citation quotes resolve to the exact selected document version.
- [ ] Refresh before selection and revalidate before assessment. Block failures and changed selections.
- [ ] Find amendments, replacements, withdrawals, and effective-date changes. Keep historical assessment evidence.
- [ ] The external API receives public source queries only. Enforce destination and response limits.
- [ ] File replacement makes a new version and does not change an existing or active assessment.
- [ ] Keep source spans and extraction/version records for retrieval labels, selected passages, and claim inspection.
- [ ] Connect reused artifacts to their initial extraction or verification records. Record skipped or not_applicable stages explicitly.
- [ ] Keep private source text and queries in authorized India case storage. Do not include them in operational logs.

**Measurement checks:** UT-18 and CT-07 cover record integrity and safe persistence. RET-04 and RET-06 cover source boundaries and overlapping passages.

## T4 — First complete assessment slice

**Status:** Not started.

**Dependencies:** T3.

**Requirements:** REQ-F03–REQ-F08, REQ-X08, REQ-X09.

Use the local adapter contracts. Write code for one full sequence: obligation → control → evidence → finding → remediation.

Acceptance:
- [ ] Conditions and applicability stay attached to the extracted obligation.
- [ ] A relevant control is mapped with source references.
- [ ] Missing operational evidence cannot be replaced by a policy promise.
- [ ] Findings distinguish supported, partial, gap, needs_review, and not_applicable according to the rubric.
- [ ] Evidence gaps have a different meaning from control failures with evidence.
- [ ] Proposed fixes and reviewer decisions have links to the initial finding.
- [ ] Apply case, snapshot, source-version, and evidence-period filters before bounded passage retrieval.
- [ ] Keep candidate and selected passage IDs. Record query duration, attempts, passage counts, and selected text size.
- [ ] Calculate different scores for provider coverage, regulatory retrieval, and bank-evidence retrieval against labeled source spans.
- [ ] Use the measurement contract rules for duplicate spans, empty results, missing spans, unknown labels, and decisive omissions.
- [ ] Keep each claim's obligation element, citations, evidence period, short reason, and exceptions or conflicts used in the assessment.

**Measurement checks:** UT-15 and RET-01–RET-06 cover retrieval. Existing assessment tests examine meaning and evidence support independently.
An exact quote match is not sufficient evidence of contextual support.

## T5 — Bounded agent and regulatory changes

**Status:** Not started.

**Dependencies:** T4.

**Requirements:** REQ-F02–REQ-F08, REQ-X01, REQ-X03, REQ-X08, REQ-X09.

Add model-selected tool actions with validation, controlled retrieval refinement, and explicit version comparisons. Expand only to the approved obligation scope.

Acceptance:
- [ ] The agent selects permitted tools through structured actions with validation.
- [ ] Use one bounded agent with code orchestration and the approved model. Keep the model unchanged. Add no automatic router or autonomous second reviewer.
- [ ] Scope filters apply before retrieval, and injected instructions cannot grant additional capabilities.
- [ ] Invalid JSON, rejected actions, and retried calls use the same saved call budget.
- [ ] Record every dispatched model attempt, including uncertain outcomes, against the same 24-call allowance.
- [ ] Record model configuration, prompt, schema, extraction, chunking, retrieval, and application versions. Record provider identifiers only when available.
- [ ] Trace source verification, extraction, retrieval, context selection, model calls, validation, persistence, and review events.
- [ ] End every started attempt or record an explicit unknown or interrupted status. Keep the saved 600-second worker deadline across restarts.
- [ ] An important regulatory change identifies affected obligations/controls and gives a new snapshot.
- [ ] Make new review items for each new assessment. Never copy earlier human outcomes automatically.
- [ ] Changes to appearance do not automatically become changed obligations.
- [ ] Use the specification rules for stale evidence, unavailable tools, budget exhaustion, and partial results.

**Measurement checks:** UT-16, UT-18, and CT-08 examine traces, limits, and the fixed baseline.

## T6 — API, jobs, ownership, and review records

**Status:** Not started.

**Dependencies:** T4. Shared contracts from T2.

**Requirements:** REQ-X02–REQ-X05, REQ-X07, REQ-X08.

Write code for short API requests with owner scope and durable asynchronous execution.
Use different records for reviewer decisions and AI findings.

Acceptance:
- [ ] Start operations return job IDs and stable input snapshots.
- [ ] Access checks cover cases, uploads, source previews, jobs, findings, and exports.
- [ ] Duplicate requests/messages give one active execution and one final result.
- [ ] Retries/restarts keep counters, deadlines, execution claims, and stage outputs.
- [ ] Partial and failed outcomes keep work with its source records and show unchecked obligations.
- [ ] Review saves cannot overwrite the AI finding or add duplicate decisions on retry.
- [ ] Store Approved, Edited, and Rejected as final outcomes for one immutable finding and its primary recommendation.
- [ ] For Edited, changed accepted content and a reason are mandatory. For Rejected, a reason is mandatory.
- [ ] Keep unsaved drafts pending. Keep evidence requests pending until the reviewer saves a final outcome.
- [ ] Keep review history and earlier report cutoffs. Keep a saved final outcome active while a later revision is unsaved.
- [ ] Calculate approval without edits, edit share, rejection share, adoption including edits, review coverage, and result coverage in code.
- [ ] Count each review item once. Use its latest saved final outcome at the cutoff. Return null for zero-denominator rates.
- [ ] Include valid partial-job items, failed runs, and unchecked obligations with the denominators from the measurement contract. Never invent findings for unchecked work.
- [ ] Calculate duration summaries and costs from controlled records. Keep unknown values and incomplete cost coverage.
- [ ] Save audit-critical references before success. Record metric-export failures independently. Retry export without repeating the model assessment.
- [ ] Deduplicate trace and metric events during retries and queue redelivery. Keep private review content outside operational logs.

**Measurement checks:** UT-13, UT-14, UT-17, UT-18, CT-06, and CT-07 cover reviews, aggregates, history, privacy, and recovery.

## T7 — Review interface

**Status:** Not started.

**Dependencies:** T5 and T6.

**Requirements:** REQ-X05–REQ-X08. AC-F01–AC-F08.

Write code for the approved case workspace, source inspection, change comparison, and exports.

Acceptance:
- [ ] Browser tests cover upload → assessment → citation inspection → review → comparison → export.
- [ ] Source previews resolve to the assessment's selected snapshot after a document replacement.
- [ ] Synthetic data and simulated model outputs have different labels.
- [ ] Loading, empty, denied, partial, and failed states give useful and correct information.
- [ ] Keyboard navigation and a viewport below 768 px work.
- [ ] Export keeps versions, evidence, run status, reviewer records, and limitations.
- [ ] Show authority verification time and freshness failures. Export that metadata.
- [ ] Show Approved, Edited, and Rejected independently of AI finding status. Keep drafts and show review history.
- [ ] Show approval without edits as the primary product measure. Show edit, rejection, adoption, review coverage, and result coverage independently.
- [ ] Show counts, denominators, cohort filters, cutoff, and Not measured states. Display failed/partial jobs and unchecked obligations beside coverage.
- [ ] Use different result groups for model/prompt versions, finding statuses, reviewers, and data classes. Keep live results, controlled simulations, and offline benchmarks in different groups.
- [ ] Export the same authorized metric definitions, counts, filters, and limitations that the interface displays.
- [ ] Use the existing operator identity. Do not claim review by a different operator. Do not use human approval as sufficient evidence of regulatory accuracy.

**Measurement checks:** BT-06 examines outcomes, coverage, history, and empty states. CT-06 examines authorized reports and exports for consistency.

## T8 — AWS integration and Rishi's guided deployment

**Status:** Not started.

**Dependencies:** T6 and T7. Begin connectivity checks when the first local assessment sequence is stable.

**Requirements:** REQ-X02, REQ-X04, REQ-X06, REQ-X08.

Write the SAM configuration and AWS adapters. Validate both. Explain each service and configuration step during T8.

Acceptance:
- [ ] Validate infrastructure configuration before deployment. Examine the specified resources, permissions, expected costs, and rollback/cleanup procedure before deployment.
- [ ] Guide Rishi through account/role access without asking for secrets in chat.
- [ ] Do verification checks of the fixed model's account access, SDK/API structure, inference-profile destinations, and applicable retention configuration.
- [ ] Make a small live call with synthetic input before private documents.
- [ ] Do verification checks of live Cognito login, ownership, S3 privacy, records, queue processing, and worker permissions.
- [ ] Make sure that the development identity cannot operate in the cloud configuration.
- [ ] Do verification checks of live regulatory API access, authority synchronization, change detection, failure handling, and absence of private request content.
- [ ] Record the commands and their outputs in a deployment guide with numbered steps and a dated run record.
- [ ] Keep private uploads disabled until the necessary region/access checks pass.
- [ ] Reconcile application attempts with available AWS metrics. Keep the saved dispatch counter authoritative for the 24-call allowance.
- [ ] Do verification checks of stage timing, usage availability, safe logs, metric deduplication, and audit-save recovery in AWS.
- [ ] Record missing provider usage as unknown. Do not interpret missing metrics as zero calls or zero cost.
- [ ] Record inference cost and measured system cost as different values. Record currency, rate source/date, Region, coverage, and estimated or billed status.

**Measurement check:** CLOUD-06 examines the live measurement limits. Controlled local responses are not evidence of cloud behavior.

Available credits are not evidence of model access. They do not permit unlimited spending. Record the cost estimate and spending controls during the deployment instructions.

## T9 — Quality and submission evidence

**Status:** Not started.

**Dependencies:** T8 and completed T1 held-out set.

**Requirements:** All feature acceptance cases and release gates.

Do the live evaluation. Do the demonstration rehearsal. Record the architecture of the developed system. Include decisions, tool actions, model use, and failure handling.

Acceptance:
- [ ] Use at least 20 held-out cases with the fixed live model. Record prompt/model versions.
- [ ] Save the one-agent baseline with `in.openai.gpt-5.6-luna` and all necessary configuration versions.
- [ ] Do RET-01–RET-06 independently of EVAL-01–EVAL-20. Give provider coverage, regulatory retrieval, and bank-evidence retrieval in different report fields.
- [ ] Keep per-query counts, source labels, selected context, decisive omissions, and aggregate numerator/denominator totals.
- [ ] Do not give measured recall for live cases without labels. Keep historical benchmark scores in a different result group from current-source verification.
- [ ] At least 90% expected-assessment agreement. The report includes all cases, including abstentions and errors.
- [ ] Give per-status results and a confusion matrix in the report. Use different groups for retrieval failures, incorrect mappings, unsupported claims, citation failures, status errors, and poor remedies.
- [ ] All citations in the report resolve to the intended passage. Contextual support has completed checks.
- [ ] Zero false supported findings in designated critical evidence/adversarial cases.
- [ ] Give reviewer outcomes and assessment accuracy in different report fields. Record same-operator review and small sample counts without significance claims.
- [ ] Give queue wait, stage/attempt timing, terminal duration, retries, failures, usage, and cost coverage from the saved traces in the report.
- [ ] Calculate nearest-rank p50/p95 for specified comparable groups. Do not present the 600-second deadline as an end-to-end percentile target.
- [ ] Include failed and incorrect runs in cost per correct assessment. If no correct cases exist, give the ratio as undefined.
- [ ] All eight feature claims have links to behavior with demonstration evidence.
- [ ] Remaining failures and scope limits appear in the report. The F/D claim agrees with recorded evidence.
- [ ] Working demo, architecture, and rehearsal record are ready before submission.
- [ ] The user must do the external submission or give explicit authorization. Preparation of this package is not authorization to send it.

Keep routing and an autonomous second reviewer as later experiments after the baseline.
Before you compare options, name a problem from recorded results.

Keep cases, source versions, permissions, and aggregate limits comparable.
Do verification checks of candidate model versions, India processing, and tool compatibility before private use.
Do not tune from held-out answers and still describe those cases as untouched.
Before you adopt a candidate, make sure that it meets existing quality gates and has a measured benefit.
An experiment does not automatically replace the approved baseline or enter this P0 delivery sequence.

## Build order and dates

**8 October target:** Prepare the sources, fixtures, and local environment. Write code for the first full assessment. T5 and T6 extend that assessment. T7 adds the review interface.

**9 October target:** Complete guided AWS integration and live evaluation. Correct failures. Do the demonstration rehearsal. Complete the architecture documents. Target completion that evening IST.

**10 October:** Submission date. There is no verification result for the exact organizer cutoff. These dates are targets. They do not show completed work.

Do not include P1/P2 work in this delivery sequence unless the user explicitly changes the scope. See the [PRD](../product/01_PRD.md) for deferred capabilities.

[Next: Local test plan](../testing/spec-local-test-plan.md)
