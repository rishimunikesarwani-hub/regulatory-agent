# Decision log

> Saved: 2026-10-08.
> Source of approval: the planning conversation across 7–8 October 2026.
> Exact per-answer timestamps were not recorded. The date below is the save date, not an approval timestamp.

This record gives each decision and its reason. It identifies approved choices and facts that need verification.

**Approved** means the user selected or accepted it.
**Implementation clarification** makes an approved requirement more precise without an additional product capability.
**Unverified** means evidence is still necessary.
No entry below proves that the application is built.

## Approved decisions

| ID | Recorded | Decision and rationale | Specification and acceptance links |
|---|---|---|---|
| D01 | 2026-10-08 | **Approved:** Work on Problem 1, banking/financial regulations. Build the traceable regulation-to-remediation workflow described in the source brief. | [PRD](../product/01_PRD.md). REQ-F01–REQ-F08 |
| D02 | 2026-10-08 | **Approved:** Target F3/D2: at least eight selected features with evidence of reliability on mostly structured/textual input. This is a target, not an achieved score. | [PRD metrics](../product/01_PRD.md). [quality gates](../testing/eval-model-quality.md) |
| D03 | 2026-10-08 | **Approved:** Start with India IT controls for a domestic commercial-bank scenario. One bank profile per case keeps applicability and evidence scope clear. | [PRD audience](../product/01_PRD.md). AC-F03, AC-F05 |
| D04 | 2026-10-08 | **Approved:** Support both a clearly fictional demo bank and authorized user uploads. Fictional documents must stay labeled. | [PRD inputs](../product/01_PRD.md). UT-01, BT-05 |
| D05 | 2026-10-08 | **Approved:** Private document storage and AI processing must stay in AWS India. Mumbai is the application region. The selected inference profile may use Mumbai/Hyderabad only after verification. | [Security](../security/03_SECURITY_ACCESS.md). CLOUD-01, CLOUD-02 |
| D06 | 2026-10-08 | **Approved:** Submission is 10 October 2026. The user corrected the earlier “within seven days” answer. Internal readiness targets 9 October evening IST. Exact organizer cutoff stays unverified. | [Delivery dates](../delivery/05_FEATURE_TICKETS.md) |
| D07 | 2026-10-08 | **Approved:** Design cloud-native now. Teach AWS hosting/configuration step by step when the local workflow is ready. Local tests must work without AWS setup. | [Architecture](../architecture/02_TECHNICAL_BLUEPRINT.md). CT-01, CLOUD-01–CLOUD-05 |
| D08 | 2026-10-08 | **Approved:** Use React/TypeScript/Vite, Python/FastAPI, API Gateway/Lambda, S3, DynamoDB, SQS, Cognito, and SAM. Local filesystem, SQLite, worker, and controlled-model adapters share the application contracts. | [Stack and flow](../architecture/02_TECHNICAL_BLUEPRINT.md). CT-01–CT-04 |
| D09 | 2026-10-08 | **Approved:** One bounded agent, keyword/BM25 retrieval, application-validated actions, and pinned model profile in.openai.gpt-5.6-luna. Do not change to a global profile without a notice. Do not add a managed vector service. Quality and account access are unverified. | [Agent/model contract](../architecture/02_TECHNICAL_BLUEPRINT.md). UT-07–UT-10, CLOUD-01 |
| D10 | 2026-10-08 | **Approved:** Use Cognito sign-in, own-case permissions, and India processing. Limits: 10 documents/case, 10 MB/file, and 100 extracted pages. Each run permits up to 20 obligations, 24 model calls, and a ten-minute job budget. One operator can review own findings. No independent dual approval is claimed. | [Security](../security/03_SECURITY_ACCESS.md). UT-02, UT-07–UT-12, CT-02–CT-04 |
| D11 | 2026-10-08 | **Approved:** Default light-color reviewer workspace with Cases/Documents/Assessment/Changes flows. Exact source inspection, human review in its own records, progress events, and Markdown/JSON exports. Reference screenshots: NONE — design risk, accepted by the user. | [Frontend](../frontend/04_FRONTEND_SPEC.md). BT-01–BT-05 |
| D12 | 2026-10-08 | **Approved:** Different nested Markdown specifications under ET-Hackathon/MVP, a start page, and durable decision history. The original style used Rishi Voice with 60% rawness. D18 replaces that style. Keep exact contracts unchanged. | [Handbook](../guide-start-here.md). [project instructions](../../AGENTS.md) |
| D13 | 2026-10-08 | **Approved:** Use at least 20 held-out cases. Make sure assessment agreement is at least 90%. All citations must resolve and support their claims. Make sure designated critical evidence/adversarial cases have zero false supported results. These are our gates, not organizer-issued numerical thresholds. | [Evaluation plan](../testing/eval-model-quality.md). EVAL-01–EVAL-20 |
| D14 | 2026-10-08 | **Approved:** T1–T9 build order and spec → failing test → implementation → refactor → verification loop. Save documentation first. The implementation request at that time covered that documentation plan. Application tickets stay pending. | [Tickets](../delivery/05_FEATURE_TICKETS.md). [local checks](../testing/spec-local-test-plan.md) |

## D15 — Unverified facts and later configuration

Recorded 2026-10-08. These are not approvals or established facts.

| Open item | Current state | Resolve in |
|---|---|---|
| AWS account, permissions, model entitlement | User requested a later teaching walkthrough. Account readiness was not established | T8 |
| Numerical cloud spending ceiling | User chose credits available / flexible. No amount confirmed | T8 resource/cost review |
| Actual model quality | No live evaluation was done | T9 |
| Regulatory corpus and genuine change pair | Source leads exist. The necessary authoritative versions are not yet available or validated in this workspace | T1 |
| Runtime/dependency versions and SDK support | Not installed or pinned for this project | T2. Live confirmation T8 |
| Nonpaginated page-equivalent handling | Must be specified before a claim that the system applies aggregate extraction limits | T2 |
| Retention, cleanup, and applicable provider terms | No automatic deletion schedule approved. Review before real private uploads | T8 |
| Exact submission cutoff | User supplied the date only | Before submission. Internal target stays earlier |
| Market demand and productivity improvement | No user research or measured baseline | Future discovery. Do not invent claims |

## D16 — Implementation clarifications preserved in the written specs

Recorded 2026-10-08. **Status: implementation clarifications, not individual answers from the user.**

These make the approved evidence, retry, and review requirements testable:
- A supported finding needs the required evidence elements. A policy assertion cannot prove an operational act.
- Missing/conflicting evidence, partial fulfillment, and a demonstrated gap are different outcomes.
- A reviewer decision does not overwrite the AI assessment.
- Each job keeps the bank profile, selected documents, extracted passages, and model/prompt versions fixed.
- Citations use the original PDF page, DOCX paragraph/table cell, TXT line, or CSV row. Each quote must pass a check against the source.
- Model-call allowances are reserved before dispatch and persist through failures, retries, and uncertain outcomes.
- The ten-minute processing clock begins at worker start and does not restart on redelivery. Code records queue wait independently.
- Completed, partial, and failed job states must show whether the job accounted for all selected obligations.
- Failed outputs and abstentions stay in the evaluation denominator.
- UI support text, status colors, and technical field names are implementation defaults. They are not additional user-research findings.

Affected documents: [architecture](../architecture/02_TECHNICAL_BLUEPRINT.md), [security](../security/03_SECURITY_ACCESS.md), [local tests](../testing/spec-local-test-plan.md), and [evaluation](../testing/eval-model-quality.md).

## D17 — Technical blueprint language

Recorded 2026-10-09. **Status: approved language change.**

The user requested ASD-STE100 language, then identified the technical architecture as the target document.
Rewrite the [technical blueprint](../architecture/02_TECHNICAL_BLUEPRINT.md) with ASD-STE100 Issue 9 writing rules.

D17 replaced D12's Rishi Voice style for the technical blueprint only.
Other documents kept that style until D18.
The change kept application scope, privacy rules, interfaces, identifiers, limits, quality gates, and approval history unchanged.
It did not authorize application implementation or deployment.

Keep the [original wording](../../runs/2026-10-09-technical-blueprint-before-ste100.txt). Record the language and preservation checks in the [verification record](../../runs/2026-10-09-ste100-verification.md). The rewrite does not establish independently verified compliance with the complete STE dictionary.

Affected specification: [Technical Blueprint](../architecture/02_TECHNICAL_BLUEPRINT.md). Existing requirement, test, and ticket references stay unchanged.

## D18 — Project Markdown language

Recorded 2026-10-09. **Status: approved language change.**

The user requested ASD-STE100 for all current ET-Hackathon Markdown files and all new projects.
The user requested this rule in the global AGENTS.md.
Do not rewrite other existing projects without another request.

D18 replaces the Rishi Voice style in D12 for all project Markdown.
It extends the language scope of D17 to the complete project.
Other approved product decisions stay in effect.

Apply the [writing guide](../guide-ste100-writing.md).
Keep requirements, identifiers, numbers, links, commands, uncertainty, and approval history.
Keep source quotations unchanged when exact wording is necessary.
Review sentence length, technical terms, and meaning.
A sentence-length check does not prove full dictionary compliance.

Global instruction file: `C:\Users\Be Flith Rich\AGENTS.md`.
The global rule applies to new projects and this project.
Use a different style only if the user requests it for the document.

The [backup archive](../../runs/2026-10-09-before-project-ste100.zip) keeps the 14 original Markdown files.
The [source manifest](../../runs/2026-10-09-ste100-source-manifest.json) records their paths and hashes.
The [verification record](../../runs/2026-10-09-project-ste100-verification.md) records the current checks.

## D19 - Project name

Recorded 2026-10-09. **Status: approved name change.**

The user selected The Regulatory Agent as the project name.
This name replaces Banking Control Assurance.
Use `the-regulatory-agent` as the manifest identifier.
The README and PRD use the selected name.
The application scope and requirements stay unchanged.

## D20 - Current regulatory retrieval

Recorded 2026-10-09. **Status: approved design change.**

The user requested current regulatory retrieval through an external API instead of a static S3 regulatory source.
The user requested only the necessary document corrections.
The user chose to keep the provider undecided.

The API supplies current public regulations, amendments, replacements, and withdrawals.
Get current source data before source selection.
Do source verification again for selected versions before each current assessment.
Record authority verification time and freshness status.
Block a current assessment if verification fails or selected versions changed.

Keep private bank content and model processing in India.
The external regulatory API receives public source queries only.
S3 keeps bank files and fixed assessment evidence copies.
It does not determine the current regulatory version.

Keep assessment snapshots and historical citations unchanged.
Compare new versions without overwriting previous findings.
An independent scheduled monitor is still future work.
Current-source verification does not guarantee zero update delay.

D20 changes the source-retrieval parts of D07–D09 and the PRD's manual regulatory loading process.
The broader crawling scope stays deferred.
All model limits, document limits, quality gates, and review rules stay in effect.

Provider endpoint, coverage, update delay, versions, terms, credentials, and pricing stay TBD.
No regulatory API has been selected, implemented, or live-tested.

Affected requirements: REQ-F01, REQ-F02, REQ-X01, REQ-X02, REQ-X03, REQ-X04, REQ-X05, and REQ-X06.
Affected delivery tasks: T1, T2, T3, T5, T7, and T8.
See the [blueprint](../architecture/02_TECHNICAL_BLUEPRINT.md#current-regulatory-sources) for the controlling contract.

## D21 - Technical architecture views

Recorded 2026-10-09. **Status: approved document change.**

The user requested ArchView diagrams for the full Regulatory Agent.
The user excluded a crawler view and kept the external retrieval API.
Provider selection stays undecided under D20.

The [blueprint](../architecture/02_TECHNICAL_BLUEPRINT.md#architecture-views) links the system and assessment views.
Each view has an editable JSON source and an HTML output.
The ASD-STE100 skill reviewed the blueprint again.
The complete dictionary was unavailable for that review.

This decision changes architecture presentation and wording.
It does not add application features or authorize deployment.
All approved models, regions, limits, evidence rules, and access rules stay unchanged.
See the [verification record](../../runs/2026-10-09-archview-verification.md).

## D22 - Agent operation comparison

Recorded 2026-10-10. **Status: proposed architecture.**

The user requested an argument comparing one-agent and multi-agent operation.
The requested direction includes different jobs, bounded ReAct loops, a master orchestrator, streaming tools, a registry, and governance.

Saved the [comparison](../architecture/arch-agent-operation-comparison.md) and [operating proposal](../architecture/arch-multi-agent-proposal.md).
The proposal assigns model coordination, authentication, and runtime enforcement to different components.
It allocates 22 model calls to roles and two calls to a shared repair reserve.
The total stays at 24 calls in the inherited 600-second deadline.

The detailed roles, local time limits, and reserve policy are proposed allocations.
Their adequacy stays unverified.
No comparison evaluation was done.
D09 and the approved specifications stay unchanged.
The existing diagrams still describe the one-agent design.

Affected requirements if adopted: REQ-F01 through REQ-F08 and REQ-X01 through REQ-X06.
Proposed tests: MA-01 through MA-12.
The proposal identifies the specification and diagram updates required before implementation.

## D23 - AWS review and code orchestration

Recorded 2026-10-10. **Status: review recommendation.**

The user specified one operator and requested code for tasks with fixed rules.
The review compares one agent with two specialists from the AWS hosting perspective.

The [AWS review](../architecture/arch-agent-aws-review.md) recommends one bounded agent with orchestration in code.
It keeps two specialists as an evaluation candidate.
It removes the AI master from the recommendation because the present workflow has fixed dependencies.
The [comparison](../architecture/arch-agent-operation-comparison.md) now contains five material decision points.

D22's seven-role allocation stays in the review history. It is not an approved design.
D09, the approved specifications, and the existing diagrams stay unchanged.
The review added no user roles, tenant management, or individual agent services.

IAM controls AWS operations. Application code controls case scope and tool access.
Different agent names in one function do not give different IAM permissions.
No measurements show a slowdown, privacy incident, or candidate quality advantage.
The formal performance audit is UNVERIFIED because no runtime samples exist.

Affected areas: REQ-X01 through REQ-X04, T2, T5, T8, and T9.
Keep the 24-call allowance, 600-second worker deadline, and existing evaluation gates.
See [the verification record](../../runs/2026-10-10-aws-agent-review-verification.md).

## D24 - Reviewer outcomes and measured agent baseline

Recorded 2026-10-10. **Status: approved direction with implementation definitions.**

The user selected one agent as the baseline.
The user selected different evaluations for retrieval and assessment, with a trace for each stage.
The user selected the approved model for the first measured baseline.
Later routing or a second reviewer must address observed failures through comparison tests.
The user requested Approved, Edited, and Rejected reviewer ratios as the north star measurements.
The user requested specification changes and tests during development.

The [measurement contract](../testing/spec-measurement-contract.md) specifies the software behavior.
The primary rate is approval without edits among finally reviewed items.
Edited and rejected shares have different fields. Adoption including edits is secondary.
Reports show review coverage, pending items, result coverage, failures, and unchecked obligations.

The formulas, cohort boundaries, zero-denominator rules, and review-event semantics are implementation definitions for the requested direction.
They are not independently measured results or new numerical quality targets.
No acceptance-rate target or baseline value exists yet.

Keep original findings and recommendations unchanged.
Save review events in different records from the AI findings.
Review revisions cannot increase the counted item total.
Approval measures reviewer acceptance. It does not establish regulatory correctness or live control operation.
The existing 90% agreement gate, 20-case minimum, citation requirements, and zero critical false-supported gate stay mandatory.

Measure source coverage, passage retrieval, and assessment quality independently.
Make a trace for each stage and attempt.
Include safe identifiers, durations, usage, cost coverage, failures, and version references.
Keep private text and authentication tokens out of operational telemetry.
Keep the 24-call allowance, 600-second worker deadline, India-only processing, and external regulatory API boundary.

D24 adopts the one-agent baseline from D09 and the code orchestration recommendation from D23.
D22 stays unadopted proposal history.
The three review outcomes replace the earlier Agree and Disagree interface wording.
Request more evidence stays a pending action. It is not a final outcome.
No routing service, autonomous second reviewer, extra user role, or cloud deployment is authorized by this specification update.

Affected specifications: [PRD](../product/01_PRD.md), [blueprint](../architecture/02_TECHNICAL_BLUEPRINT.md), [security](../security/03_SECURITY_ACCESS.md), [frontend](../frontend/04_FRONTEND_SPEC.md), and [tickets](../delivery/05_FEATURE_TICKETS.md).
New requirements: REQ-X07 through REQ-X09, with AC-X07 through AC-X09.
Development checks: UT-13 through UT-18, CT-06 through CT-08, BT-06, and CLOUD-06.
Retrieval evaluations: RET-01 through RET-06. Keep EVAL-01 through EVAL-20.

See the [local test plan](../testing/spec-local-test-plan.md) and [AI quality plan](../testing/eval-model-quality.md).
Application tests and live evaluations stay pending until development.

## D25 - Permanent documentation language rule

Recorded 2026-10-10. **Status: approved language instruction.**

The user repeated the requirement for ASD-STE100 documentation.
The user requested a permanent rule in the local AGENTS.md.
Apply the rule to all new documentation and each document change.
Do not wait for another request to use STE.

The [local instructions](../../AGENTS.md#documentation-language-always-use-asd-ste100) specify the mandatory writing and review steps.
The [language guide](../guide-ste100-writing.md) records dictionary decisions and project technical terms.
The complete official Issue 9 standard became available for this correction.
Earlier records keep the review limits that applied on their dates.

A sentence-length check alone is insufficient.
Do a manual review of word meanings, parts of speech, technical terms, and applicable rules.
Keep technical meaning, formulas, permissions, limits, identifiers, and approval history unchanged.

This decision strengthens D18's language process.
It does not change the approved application design or authorize deployment.
See the [language review record](../../runs/2026-10-10-ste-language-correction-verification.md).

## D26 - Foundation integration and remaining worktrees

The horizontal sequence and eight-folder assignments below are superseded by [D27](#d27---delivery-by-complete-user-flow).
The integration evidence, accepted foundations, requirements, and safety limits stay applicable.

Date: 2026-10-10.
Status: Approved worktree preparation and implementation clarification.

The user requested integration of Session A and Session B through pull requests.
The user then requested all remaining worktrees before further implementation.
The private repository uses GitHub, with `main` as its integration branch.

[PR #1](https://github.com/rishimunikesarwani-hub/regulatory-agent/pull/1) contains the final Session A foundation.
[PR #2](https://github.com/rishimunikesarwani-hub/regulatory-agent/pull/2) contains Session B contracts, adapters, and combined test evidence.
The combined offline checks passed 60 tests with the final Session A fixture revision.
Historical Session B records keep their original results and fixture hashes.

The [blueprint](../architecture/02_TECHNICAL_BLUEPRINT.md#integrated-t2-limits) now records the implemented T2 extraction and retrieval defaults.
These defaults do not establish live network behavior or file-parser enforcement.
The approved model, India boundary, 24-call allowance, and 600-second deadline stay unchanged.

T1 and T2 are incomplete against D24.
The foundation worktree owns their remaining fixture and executable-contract additions for this phase.
The integration session must review and merge these shared changes before T3.
Other shared specification and contract changes still need integration-owner review.

The [worktree guide](../delivery/guide-next-worktrees.md) gives eight task folders, branches, and dependency conditions.
Its T5 and T6 folders replace the original Session A and Session B folder assignments for later development.
This change keeps the ticket scope and dependency sequence unchanged.
Provider selection stays with the user.
Production deployment and external submission still need explicit authorization.

Affected requirements: REQ-X06 through REQ-X09 and the shared contracts for REQ-F01 through REQ-F08.
Affected tickets: T1 through T9.
The [integration record](../../runs/2026-10-10-integration/verification.md) gives evidence and remaining limits.

## D27 - Delivery by complete user flow

Date: 2026-10-10.
Status: Approved delivery change from the user's current instructions.

The user requested vertical slices after reconciliation of Session A, Session B, and the latest approved specifications.
A vertical slice is one complete user flow across the browser, API, storage, and AWS development environment.

Record the shared API contract before frontend and backend implementation.
Then permit concurrent frontend and backend work against that contract.
Give each file one owner.
Each application session must complete its selected flow, including development deployment and browser acceptance.
VS0 supplies the contract preparation before the application slices.

The first application slice is sign-in, case creation, storage, and reopening.
Subsequent slices add evidence inspection, one-obligation assessment, citation inspection, saved reviews, regulatory changes, and the full approved scope.
The [ticket inventory](../delivery/05_FEATURE_TICKETS.md#delivery-slices) assigns VS0 through VS5.
T1 through T9 stay as capability acceptance records.
All existing acceptance conditions, requirement IDs, and test IDs stay mandatory.

Use one serialized AWS development pipeline.
Do integration tests before deployment.
Do browser acceptance after deployment.
Give each development release its URL, commit SHA, tests, and known limits.
A local test result does not establish deployment or browser acceptance.

This decision supersedes D26's horizontal sequence and eight-folder assignment plan.
It also supersedes earlier frontend and AWS scheduling that deferred those components until backend tickets were complete.
It does not replace D26's foundation integration evidence or D24's measurement definitions.
The active [worktree guide](../delivery/guide-next-worktrees.md) records the observed worktrees and the selected development folder.
The [parallel guide](../delivery/guide-parallel-development.md) controls ownership and deployment coordination.

The eight product features, India processing boundary, fixed model, 24-call allowance, and 600-second worker deadline stay unchanged.
The 20-case minimum, 90% agreement, citation checks, and zero critical false-supported gate stay unchanged.
The first case slice needs no regulatory provider or model invocation.
Live regulatory and model operations still need their specified prerequisites.
Provider selection stays with the user.
Production deployment and external submission still need additional explicit authorization.

Affected requirements: REQ-F01 through REQ-F08 and REQ-X01 through REQ-X09.
Affected delivery records: T1 through T9, the two development guides, and the project log.
The [VS1 API contract](../delivery/spec-slice-01-cases.md) controls the first application flow.

## D28 - Development access and feedback checkpoint

Date: 2026-10-10.
Status: Development execution and a USD 25 monthly budget have user approval.
Status: The new AWS permission installation needs confirmation in the browser.

The user requested one complete slice at a time for testing and feedback.
Keep VS1 active until its acceptance checks and user review are complete.
Do not start VS2 during this checkpoint.

The `rishicodex` profile authenticated in account `482439369658`.
CloudFormation and Lambda access checks failed with access-denied responses.
The existing policies do not supply the required application deployment access.

The proposed account setup creates different deployment, CloudFormation, and case function roles.
The case function role permits case records and application logs only.
CloudFormation can pass this role but cannot change its permissions.
The GitHub role trusts only this repository's `development` environment.
The proposed setup does not grant account administrator access.
The USD 25 budget requires an alert destination before configuration.
It is an alert threshold, not a spending cap.

Affected acceptance cases: VS1-AWS01 and VS1-REL01.
The application scope and existing quality gates stay unchanged.

## D29 - Verified GitHub deployment identity

Date: 2026-10-10.
Status: Implementation clarification within D28.

The repository uses GitHub's immutable subject format for OpenID Connect.
OpenID Connect supplies a temporary deployment identity without stored AWS access keys.
The verified owner ID is `292392448`.
The verified repository ID is `1412648942`.
The AWS trust condition must include both IDs and the `development` environment.
The permitted repository, environment, and AWS actions stay unchanged.

The GitHub development environment was created successfully.
Its deployment branch policy permits only `main`.
General branch protection is unavailable under the current account plan.
The successful environment policy is a different control.

Affected acceptance cases: VS1-AWS01 and VS1-REL01.
Update the [access setup](../delivery/guide-aws-development-access.md) before installation.
Use the [GitHub reference](https://docs.github.com/en/actions/reference/security/oidc#immutable-subject-claims) for the subject format.

## D30 - Development concurrency quota

Date: 2026-10-10.
Status: Implementation clarification within the authorized development deployment.

The authenticated AWS account has a Mumbai Lambda concurrency quota of 10.
Concurrency is the number of requests that run at the same time.
AWS requires 100 unreserved executions before a function can reserve additional capacity.
The first application deployment must omit reserved concurrency.
The existing account quota stays unchanged.

Use an API request rate target of 2 requests per second.
Use an API burst target of 4 requests.
These targets reduce development traffic.
They are not a spending cap or a guaranteed concurrency limit.
Keep the monthly budget alert threshold at USD 25.

Affected acceptance cases: VS1-AWS01 and VS1-REL01.
The application scope and authentication conditions stay unchanged.
See the [AWS concurrency rule](https://docs.aws.amazon.com/lambda/latest/dg/configuration-concurrency.html).

## D31 - User-approved sign-in design

Date: 2026-10-10.
Status: Approved by the user's screenshot instructions.

Use `The Regulator` as the visible application name.
Remove the sign-in introduction panel.
Center the sign-in card.
Keep only `Sign in to continue` and the sign-in action inside that card.
Keep authentication errors and fictional-data controls available.

The nine reference screenshots are in `MVP/docs/frontend/Design Ideas`.
The [frontend specification](../frontend/04_FRONTEND_SPEC.md#sign-in-screen) controls this change.
Affected acceptance cases: VS1-BT01 and VS1-BT03.
The application scope and AWS deployment request stay unchanged.

## D32 - CloudFormation transform permission

Date: 2026-10-10.
Status: Implementation correction from the first live development release.

The release stopped before application resource creation.
The CloudFormation execution role could not use the AWS SAM transform.
The SAM transform converts the application template into CloudFormation resources.

Permit `cloudformation:CreateChangeSet` on `arn:aws:cloudformation:ap-south-1:aws:transform/Serverless-2016-10-31` for that execution role.
Do not add wildcard CloudFormation resource permissions.
The existing IAM restrictions stay unchanged.
Keep the failed release as evidence.
Retry the reviewed application release after the role update.

Affected acceptance cases: VS1-AWS01 and VS1-REL01.
The application scope, data boundary, and budget stay unchanged.

## D34 - Keep CloudFront after the account verification failure

Date: 2026-10-10.
Status: Approved by the user after the second development release failed.

AWS rejected CloudFront distribution creation because the account needs verification.
The user chose to keep CloudFront and submit an AWS Support verification request.
Do not replace the approved hosting design with an API Gateway frontend.
The request is prepared but has not been sent.
The [verification guide](../delivery/guide-aws-cloudfront-verification.md) controls the handoff and recovery steps.

Keep the failed release and retained resource records as evidence.
Obtain approval before any manual deletion during recovery.
Keep the USD 25 alerts and the current fictional-data boundary.
Live AWS acceptance and the next vertical slice remain pending.

## D35 - Isolated slices and combined release checks

Date: 2026-10-10.
Status: Approved by the user's new five-step development goal.

Give each selected vertical slice its own branch, worktree, port, and test database.
Follow specification, failing tests, implementation, and passing tests in that order.
Use Ponytail for the minimum implementation.
Merge accepted slices regularly into the `main` integration branch.
Test the combined application locally before its AWS release.
Verify AWS authentication, permissions, and service connections after deployment.

The [workspace guide](../delivery/guide-slice-workspaces.md) controls current isolation assignments and the development sequence.
Keep the earlier user feedback checkpoint before the next slice.
Record local acceptance and AWS acceptance separately.
The user can approve local progress while CloudFront verification is pending under D34.
This sequence replaces any requirement to wait for AWS before approved local development can continue.
The approved feature scope and security boundaries stay unchanged.

The user subsequently approved VS1 local acceptance and authorized VS2 local development.
Keep VS1 AWS acceptance pending until account verification and deployed checks pass.

## D36 - VS2 local source contract

Date: 2026-10-10.
Status: Implementation details within the user's approved VS2 local development.

Use the [VS2 contract](../delivery/spec-slice-02-documents.md) for upload and exact source-version inspection.
Combine local authorization, extraction, and finalization in one request.
Use SQLite transactions to keep original bytes and source versions unchanged.
Count saved replacement versions against the existing case allowance.
Keep the original page, paragraph, line, or row locations.
Use one bounded extraction process and the pinned `pypdf 6.20.0` parser.
Use the Python standard library for DOCX, TXT, and CSV.
Do not add assessment or regulatory retrieval behavior to this slice.
Keep private AWS upload and storage acceptance pending until the required cloud checks pass.

## How to add a decision

Add a new entry with:

1. Stable ID and recorded date.
2. Status: proposed, approved, implementation clarification, unverified, or superseded.
3. The decision and its reason.
4. Approval/source evidence, without invented timestamps.
5. Affected specification, requirement IDs, tests, and tickets.
6. Any decision it replaces.

Update the controlling specification in the same change.
Keep replaced history.
Add a link to its replacement.
Minor wording changes do not need new product approval.
Changes to scope, privacy, budgets, quality gates, or external actions need approval.

[Next: Local test plan](../testing/spec-local-test-plan.md)
