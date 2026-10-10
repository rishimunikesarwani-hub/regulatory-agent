# Feature tickets

> Status: The user gave approval during planning. Saved 2026-10-08.
> Depends on: [PRD](../product/01_PRD.md), [Technical Blueprint](../architecture/02_TECHNICAL_BLUEPRINT.md), [Security](../security/03_SECURITY_ACCESS.md), and [Frontend](../frontend/04_FRONTEND_SPEC.md).

> Decisions: [D12–D14](../decisions/gov-decision-log.md) and [D24](../decisions/gov-decision-log.md#d24---reviewer-outcomes-and-measured-agent-baseline).
> Measurement requirements: [Measurement contract](../testing/spec-measurement-contract.md). Approval is under D24. Application measurements are not available.

> Development state: Session A and Session B foundations are integrated. The combined offline checks passed 60 tests.
> D24 foundation: The recorded offline checks passed 123 tests. T1 and T2 still have incomplete acceptance conditions.

> VS1 local checks: 166 Python tests and 14 browser tests passed.
> VS1 deployment: AWS behavior is unverified. CloudFront requires AWS account verification under D34.
> VS1 state: The user approved local acceptance. Deployed sign-in and browser acceptance remain pending.
> Delivery order: [D27](../decisions/gov-decision-log.md#d27---delivery-by-complete-user-flow) replaces the horizontal ticket sequence with VS0 through VS5.

The user approved continued local development through VS2 while AWS verification is pending.
D35 controls the isolated workspaces and combined release sequence.
Keep local acceptance and AWS acceptance records separate.
Extend the accepted local case flow through evidence inspection, one assessment, citation inspection, and a saved review.

The measurement contract controls reviewer outcomes, retrieval scores, assessment quality, traces, and cost calculations.
Keep one agent and the approved model `in.openai.gpt-5.6-luna` for the baseline.
Use code for fixed rules, access, workflow routing, retries, budgets, validation, and progress.
Keep the 24-call allowance and 600-second worker deadline.
The linked test records give evidence for their stated checks.
This ticket inventory does not establish live model quality or measured improvement.

See the [VS1 development guide](guide-slice-01-development.md) for setup and remaining AWS steps.
The [Python result](../../runs/2026-10-10-autonomous-build/final-python-green.txt) and [browser result](../../runs/2026-10-10-autonomous-build/frontend-green.txt) record local checks.

## Delivery slices

A vertical slice is one complete user flow across the browser, API, storage, and AWS development environment.
T1 through T9 stay as the capability acceptance inventory.
Their acceptance conditions, requirement IDs, test IDs, and quality limits stay unchanged.
A slice uses the necessary parts of several tickets.
Completion of a slice does not establish completion of those entire tickets.

VS0 prepares the shared contract before VS1.
After VS0, each session must complete the selected user flow.
Frontend and backend work can proceed concurrently after the shared API contract is recorded.
AWS development deployment and browser acceptance belong to that same flow.

| Slice | User result | Ticket allocation | Start condition |
|---|---|---|---|
| VS0 | One agreed API contract and reconciled source state. | T1 and T2 contracts, with existing D24 work. | Compare Session A, Session B, integration history, and current approved specifications. |
| VS1 | Sign in, make a case, save it, and reopen it after reload. | T2 case contract, T6 identity and records, T7 case screens, T8 development infrastructure, T9 evidence. | Complete VS0. Configure authorized AWS development access. |
| VS2 | Open a case, upload evidence, and inspect its unchanged source version. | T1 selected fixtures, T2 source contract, T3 documents, T6 access, T7 source screens, T8 storage, T9 evidence. | Obtain VS1 local acceptance under D35. Record the source API contract. Keep AWS acceptance pending until verification. |
| VS3 | Assess one obligation, inspect its citations, and save a review. | T1 selected labels, T2 measurement contracts, T3 sources, T4 assessment, T5 bounded execution, T6-T9 applicable work. | Complete VS2. Record the assessment and review API contracts. |
| VS4 | Compare specified regulatory versions and inspect a new assessment with its own review history. | T1 change fixtures, T3 versions, T5 changes, T6-T9 applicable work. | Complete VS3. Record the version-comparison API contract. |
| VS5 | Use the full approved scope and inspect release evidence for all eight features. | All remaining T1-T9 acceptance conditions. | Complete VS4. Complete provider, model, source, and held-out-data prerequisites for live evaluation. |

### Slice acceptance

| Slice | Frontend and backend | AWS development and tests | Release evidence |
|---|---|---|---|
| VS0 | Agree on requests, responses, identity, errors, limits, and controlled responses. | Keep default checks offline. Compare the shared schemas with current specifications. | Record the contract version, source commits, test results, and remaining differences. No deployed application claim. |
| VS1 | Connect sign-in and case screens to authorized persistent case operations. | Do API and ownership tests before deployment. Do browser sign-in, save, reload, and reopen checks after deployment. | Give the development URL, commit SHA, test results, and known limits. |
| VS2 | Connect upload and source inspection to extraction, immutable versions, and case access. | Do extraction and ownership tests before deployment. Inspect exact source locations in the deployed browser. | Include upload failures, version preservation, and the source-inspection result. |
| VS3 | Connect one-obligation assessment, citations, and review actions to durable jobs and D24 records. | Do integration tests before deployment. Do the complete deployed assessment and review flow afterward. | Identify controlled or live processing. Include findings, citations, review history, traces, failures, and provider limits. |
| VS4 | Connect comparison screens to source changes, affected controls, and new snapshots. | Do change and snapshot tests before deployment. Inspect both versions and both review histories afterward. | Identify simulated amendments. Keep earlier findings and reviews unchanged. |
| VS5 | Complete scope controls, failures, exports, and all eight feature flows. | Do integration tests before deployment. Do deployed browser acceptance and authorized live evaluations afterward. | Give all feature evidence, held-out results, retrieval scores, runtime measures, costs, and remaining limitations. |

Use one serialized AWS development pipeline for every application slice.
Only one deployment can operate at a time.
A failed integration test blocks deployment.
A failed browser acceptance check blocks the slice release.
Production deployment and external submission need additional explicit authorization.

VS1 needs no regulatory retrieval provider or model invocation.
VS3 can use labeled controlled responses for development acceptance.
Controlled acceptance does not establish current regulatory coverage or live model quality.
Live assessments need the approved provider and model checks before use.
VS5 keeps the 20-case minimum, 90% agreement, citation checks, and zero critical false-supported gate.

The [parallel guide](guide-parallel-development.md) controls ownership and integration.
The [active worktree guide](guide-next-worktrees.md) controls workspace state and the next flow.
The [VS1 API contract](spec-slice-01-cases.md) controls the first application slice.

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

**Dependencies:** None. Prepare the necessary source and fixture subset before each dependent slice.

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

**Status:** In progress. Local adapters and D24 contract work exist. Remaining acceptance conditions are incomplete.

**Dependencies:** T1's specifications and minimum labeled fixture. Record each slice contract before its frontend and backend work.

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

**Dependencies:** VS2 and later slices use the corresponding T2 contracts. Complete the necessary document behavior before assessment.

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

**Dependencies:** VS3 uses the selected T3 document and source behavior, with its T2 contracts.

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

**Dependencies:** VS3 uses the first T4 assessment. VS4 adds changes. VS5 extends the approved scope.

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

**Dependencies:** VS1 starts with T2 case contracts. Each later slice adds its API, job, or review behavior.

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

**Dependencies:** Each slice starts frontend and backend work after agreement on its shared T2 API contract.

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

**Dependencies:** VS1 starts development infrastructure. Each later slice adds the AWS services needed for its complete flow.

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

**Dependencies:** Each slice supplies development release evidence. VS5 needs applicable T8 cloud checks and the completed T1 held-out set.

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

## Historical planning dates

D27 replaces the earlier horizontal sequence below.
These dated targets remain as planning history, not current delivery instructions.

**8 October target:** Prepare the sources, fixtures, and local environment. Write code for the first full assessment. T5 and T6 extend that assessment. T7 adds the review interface.

**9 October target:** Complete guided AWS integration and live evaluation. Correct failures. Do the demonstration rehearsal. Complete the architecture documents. Target completion that evening IST.

**10 October:** Submission date. There is no verification result for the exact organizer cutoff. These dates are targets. They do not show completed work.

Do not include P1/P2 work in this delivery sequence unless the user explicitly changes the scope. See the [PRD](../product/01_PRD.md) for deferred capabilities.

[Next: Local test plan](../testing/spec-local-test-plan.md)
