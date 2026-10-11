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

The user subsequently approved VS2 local acceptance and authorized VS3 local development.
Complete the VS2 GitHub integration checks before merge.

## D37 - VS3 controlled assessment integration

Date: 2026-10-10.
Status: Implementation details within the user's approved VS3 local development.

Use the [VS3 contract](../delivery/spec-slice-03-assessment.md) for one controlled historical example and saved human review.
Use the existing historical RBI source and approved fictional policy fixture.
Keep the fixed finding visibly controlled and its applicability unverified.
Do not present this example as an assessment of arbitrary bank documents.

Reuse the existing job store, controlled adapter, source contracts, trace schema, and review service.
Keep current assessments blocked until the source provider and freshness checks pass.
Keep the approved baseline model unchanged without claiming a live invocation.
Record model quality, AWS service connections, and deployed acceptance as unverified.

## D38 - Accepted VS2 cloud document integration

Date: 2026-10-11.
Status: Implementation clarification within accepted VS2 and authorized AWS development.

VS2 local integration merged through PR8 after its GitHub checks passed.
Its cloud preparation uses [the cloud source contract](../delivery/spec-slice-02-aws-documents.md).
Send file bytes directly to private, versioned S3 storage in Mumbai.
Lambda's synchronous payload limit cannot carry the approved 10 MB uploads.
Keep the approved limits unchanged.
Save upload records and case counters through conditional DynamoDB transactions.
Pin original and extracted object versions before exposing saved source evidence.

Use temporary signed transfer permission for one declared key and file length.
Configure the S3 SDK with an explicit Mumbai endpoint and virtual addressing.
Keep every extracted passage accessible through 500-passage source pages in AWS mode.
Give unfinished uploads explicit status, resume, and cancellation actions.
Cancellation changes metadata only.
Retain existing originals and earlier document versions.

The controlled checks cover VS2-S3-01 through VS2-S3-09 and VS2-AWS-01 through VS2-AWS-10.
They also cover VS2-AWS-BT01 through VS2-AWS-BT04.
These checks contribute to T3, T6, T7, T8, and T9.
They do not establish live AWS acceptance or model quality.
Read the [preparation guide](../delivery/guide-slice-02-aws-documents.md) for the evidence and remaining deployment conditions.

D34 and D35 remain in force.
The user chose to keep CloudFront while AWS account verification is pending.
The new cloud permission template has not been applied.
VS3 remains in its separate review branch until the pending user review.
No earlier product decision or approval record is replaced.

## D39 - VS3 integration preparation

Date: 2026-10-11.
Status: Implementation clarification within authorized VS3 local development.

Use a different candidate worktree for checks of VS3 and current accepted `main` changes.
The [integration contract](../delivery/spec-slice-03-integration.md) gives its ports, database, and check IDs.
Keep the existing VS3 review build and its feedback records unchanged.
Keep the user-review condition before merge into `main` and VS4 development.

The candidate keeps cloud document actions and local controlled assessment actions in their permitted modes.
It includes the accepted delayed-load focus correction.
Use one browser configuration for all four suites.
Keep earlier evidence and acceptance history unchanged.

Model profile metadata does not establish runtime permissions, invocation logging, or live model quality.
No product scope, AWS release condition, or earlier approval record changes.

## D40 - VS3 acceptance and VS4 authorization

Date: 2026-10-11.
Status: Approved by the user in this conversation.

The user wrote "approved vs3 and development of vs4".
This approval meets D35's local review condition for VS3.
Update PR9 with the combined candidate and this acceptance record.
Merge its exact checked commit after the updated GitHub checks pass.
Start VS4 in its own branch, worktree, ports, and databases.
Use the VS4 version-comparison contract before new behavior tests and code.

Earlier evidence and approval history stay unchanged.
AWS account verification and deployed acceptance stay pending.
No feature scope, model, budget, or external-message permission changes.

## D41 - VS4 simulated version comparison

Date: 2026-10-11.
Status: Implementation clarification within the user's approved VS4 local development under D40.

The [VS4 contract](../delivery/spec-slice-04-changes.md) controls specified source pairs and new assessment snapshots.
Use the existing simulated access-rule fixtures and fictional policy.
Show complete passages and metadata for both source versions.
Keep wording changes and cosmetic changes different from the added approval requirement.
Use fixed classifications only for these labeled simulations.
Do not treat them as live regulatory interpretation or RBI amendments.

Reuse the existing saved jobs, source inspection, traces, and human-review service.
Give each changed assessment different finding and review records.
Keep the earlier policy selection, obligation scope, assessment, and reviews unchanged.
Save the comparison before you show success.
Repeated and simultaneous requests must not make additional assessments or model calls.
AWS mode must not expose controlled assessment or comparison actions.

No approved feature scope, model, budget, or AWS release condition changes.
VS4 local review and deployed acceptance stay pending.

## D42 — VS4 local acceptance and VS5 authorization

Date: 2026-10-11.
Status: Approved by the user's review response.

The user approved VS4 local acceptance, its merge, and VS5 local development while AWS verification remains pending.
The response satisfies the D35 local review condition for VS4.
The [VS4 contract](../delivery/spec-slice-04-changes.md) and its saved checks control the completed local behavior.
Merge the final VS4 commit after its GitHub checks pass.
Start VS5 in its separate branch, worktree, ports, and test database.
Keep the approved complete scope and live evaluation conditions.
This approval does not establish live model quality, current regulatory coverage, or deployed AWS acceptance.
No Support case ID or account verification completion has been confirmed.

## D43 — VS5 export and release work

Date: 2026-10-11.
Status: Implementation clarification within D42's approved local development.

VS4 merged through PR12 at `4ffdd0713961a64da7d20ad91232c761f1dc07cd` after run `38107994304` passed.
The [VS5 contract](../delivery/spec-slice-05-release.md) keeps all remaining first-release conditions.
Local export work reuses immutable snapshots, case ownership, source inspection, saved review events, and safe traces.
Reports use one saved review cutoff and explicit single-assessment filters.
Current job state and historical review outcomes have different time bases.
Exports do not create jobs, dispatch model calls, or change reviews.
Keep older trace application and prompt versions unchanged.

The user authorized research of RBI-source API options.
The [research record](../references/ref-regulatory-api-options.md) gives the options and one public transport probe.
Provider selection and current-source verification remain pending under D20.
No complete-source, live model, evaluation, or AWS acceptance claim changes.
VS5 user acceptance remains pending under D35.

## D44 - Bounded model dispatch

Date: 2026-10-11.
Status: Implementation clarification within D42's approved local development.

The [model adapter contract](../delivery/spec-slice-05-model.md) connects the saved dispatch allowance to native Bedrock Converse.
The adapter keeps the selected India profile, case ownership, source selection, and synthetic-input restriction.
The SDK does not repeat an inference request automatically.
Available numeric usage and request IDs remain available after an unusable response.
Source/version lookup keys and saved document IDs have different purposes.
Citation checks resolve the selected records before comparing saved document IDs.

Native SDK checks use fake credentials and controlled responses.
These checks do not establish live access, source completeness, model quality, or private-processing approval.
The complete assessment worker and its independent deadline remain unfinished.
Provider selection under D20 and user acceptance under D35 remain pending.

## D45 - Selected-scope historical processing

Date: 2026-10-11.
Status: Implementation clarification within D42's approved local development.

The [pipeline contract](../delivery/spec-slice-05-pipeline.md) extends processing beyond the fixed example.
It processes each admitted selected obligation with the same bounded model interface.
Saved scope maps connect selected obligation IDs to their original regulatory passages.
Keyword ranking keeps selected versions, kinds, known periods, candidate IDs, selected IDs, and context limits.
Structured claims keep source references, examined exceptions, conflicts, reasons, and known or unknown evidence periods.

Presentation checks the execution claim inside its database transaction.
Exports validate nested claim references and retain the declared processing mode.
Available numeric usage survives failed responses.
Interrupted validated output can resume without duplicate inference or findings.
The SDK's `crt` extra supports the existing login profile.
All 26 earlier locked package versions remain unchanged.

The current interface still uses the earlier controlled example.
General API admission, source selection, and the independent worker supervisor remain unfinished.
The software checks do not establish live access, contextual model quality, or current regulatory completeness.
Provider selection under D20, AWS verification, and VS5 acceptance under D35 remain pending.

## D46 - Independent local worker supervision

Date: 2026-10-11.
Status: Implementation clarification within D42's approved local development.
Requirements: REQ-X02, REQ-X08, and the existing job deadline contract.

The [worker contract](../delivery/spec-slice-05-worker.md) adds a separate local supervisor without another dependency.
The supervisor reserves the existing claim and renews its execution lease.
The pipeline uses that inherited claim without acquiring another claim.
The original deadline and counters remain unchanged.
The supervisor stops a hung child before finalization.

Saved findings, validated outputs, dispatched calls, unknown usage, and unchecked scope remain available.
The supervisor saves interrupted audit records and finalization in one transaction.
Windows startup argument validation prevents a failed serialization from launching an untracked child.
Empty inherited claims receive the same rejection as stale claims.

Controlled software checks do not establish live model quality or AWS timeout behavior.
Catastrophic supervisor termination and operating-system failure remain outside the local evidence.
General admission, source-selection integration, provider selection under D20, and live quality gates remain unfinished.
AWS authentication needs renewal. VS5 remains a draft under D35.


## D47 - Selected historical admission and artifact references

Date: 2026-10-11.
Status: Implementation clarification within D42's approved local development.
Requirements: REQ-F03–REQ-F08 and REQ-X02–REQ-X06.

The [admission contract](../delivery/spec-slice-05-admission.md) connects selected historical scope to the existing pipeline and separate worker.
It accepts owned fictional uploads without the earlier fixed policy hash requirement.
The catalog exposes saved real-source excerpts and keeps current verification unavailable.
It does not approve or integrate an external provider under D20.

Snapshots now contain exact document artifact references in addition to canonical source versions.
The shared resolver serves processing, citation validation, inspection, and exports.
Legacy reports keep their original records and lookup paths.
Public original bytes remain in authorized storage with checksum validation.

The selected protocol uses `assessment-vs5-selected-v1` and `vs5-selection-v1`.
The server controls processing configuration and labels.
Controlled checks do not establish live access, complete source coverage, or model quality.
The selection interface, evidence-period integration, current verification, and AWS acceptance remain unfinished.
VS5 remains a draft under D35.


## D48 - Selected historical interface

Date: 2026-10-11.
Status: Implementation clarification within D42's approved local development.
Requirements: REQ-F03–REQ-F08 and REQ-X03–REQ-X06.

The [interface contract](../delivery/spec-slice-05-selection-ui.md) connects the D47 catalog and admission API to local selection controls.
The reviewer selects bank versions, historical clauses, and a date.
The existing controlled example remains accessible through a different action.
The interface identifies fictional inputs with live model processing and keeps current assessments unavailable.

Each selected finding uses its own review revision and source references.
Queued and partial runs keep their recorded state, call count, and unchecked scope visible.
Available token counts remain numeric. Unknown costs and evidence periods remain unknown.

Default browser checks use controlled native-processing responses and make no external model call.
They do not establish live access, complete regulatory coverage, or assessment quality.
Provider selection under D20, grounded evidence periods, live quality gates, and AWS acceptance remain pending.
VS5 remains a draft under D35.

## D49 - Stated evidence periods

Date: 2026-10-11.
Status: Implementation clarification within D42's approved local development.
Requirements: REQ-F06, REQ-X03, REQ-X05, and REQ-X08.

The [period contract](../delivery/spec-slice-05-evidence-periods.md) derives stated dates from original selected evidence passages.
Explicit CSV period columns require both header and record citations.
The source reader checks original document integrity before extraction, processing, inspection, or export.
Retrieval filters known periods per passage within the existing context allowance.
Known claim periods require a cited record interval and its grounding context.

These dates do not establish complete records or actual control operation.
Unknown and conflicting intervals remain unknown.
New selected runs use a separate protocol and retain the original source records.
Earlier protocols retain their original prompts and processing path.
No model call or dependency was added for extraction.

Controlled local checks do not establish live model access, quality, or current regulatory completeness.
Provider selection, live evaluations, and AWS acceptance remain pending.
VS5 remains a draft under D35.

## D50 - Native cloud job state and pre-dispatch checks

Date: 2026-10-11.
Status: Implementation clarification within D42 and the approved AWS blueprint.
Requirements: REQ-X02, REQ-X03, REQ-X05, REQ-X07, and REQ-X08.

The [cloud job contract](../delivery/spec-slice-05-cloud-jobs.md) adds conditional DynamoDB metadata, claims, and allowance counters.
The existing Mumbai S3 adapter keeps exact immutable snapshots and stage artifacts.
Large outputs remain outside DynamoDB items.
Competing claims and lost acknowledgements cannot reset the saved deadline or counters.
The job client permits one SDK write attempt.

Storage completion triggers a fresh execution check before inference.
An unused reservation remains consumed when that check prevents dispatch.
The trace records the known absence of dispatch separately.
The live-call report uses saved dispatch records instead of the reserved-call counter.
The [model contract](../delivery/spec-slice-05-model.md) assigns the corresponding deadline and storage checks.

Controlled checks do not establish live cloud behavior, model quality, or deployed permissions.
The cloud job component does not replace the remaining queue, API, review, and worker integration.
Cloud assessment routes remain disabled until the complete integration passes.
Provider selection, live quality gates, and AWS account verification remain pending.
VS5 remains a draft under D35.

## D51 - Native assessment and review persistence

Date: 2026-10-11.
Status: Implementation clarification within D42 and the approved AWS blueprint.
Requirements: REQ-X02, REQ-X03, REQ-X04, REQ-X05, REQ-X07, and REQ-X08.

The [cloud record contract](../delivery/spec-slice-05-cloud-records.md) connects the shared pipeline to native DynamoDB and versioned S3 records.
Conditional transactions protect worker claims, one finding per obligation, review revisions, and immutable attempt identities.
The shared review functions keep original-content validation and historical cutoff calculations.
Incomplete dispatch audit data produces Unknown instead of zero live calls.
Native review traces identify their actual processing configuration.

The controlled checks include complete and partial assessments, review retries, concurrent saves, source inspection, and exports.
These checks do not establish deployed permissions, live inference, or quality.
Cloud admission, the API, SQS delivery, and worker integration remain unfinished.
Cloud assessment routes remain disabled.
Provider selection, live quality, AWS authentication, and CloudFront acceptance remain pending.
VS5 remains a draft under D35.

## D52 - Native admission and SQS execution

Date: 2026-10-11.
Status: Implementation clarification within D42 and the approved AWS blueprint.
Requirements: REQ-X02, REQ-X03, REQ-X05, REQ-X07, and REQ-X08.

The [native execution contract](../delivery/spec-slice-05-cloud-execution.md) connects shared selection to native admission and identifier-only SQS messages.
Internal bank reads include all passages and verify pinned originals.
Repeated admission preserves original object versions and the saved run.
The worker keeps native job claims, counters, deadlines, partial results, and interrupted attempts.
An acknowledgement requires saved terminal state.
The run snapshot must equal the job's immutable original snapshot.
The shared process supervisor uses native cleanup without a multiprocessing queue or pool.

Controlled native checks do not establish hosted Lambda acceptance, current-source coverage, or live quality.
Cloud assessment routes remain disabled.
API integration, source packaging, queue resources, event-source mapping, and worker IAM remain unfinished.
D30 still prohibits reserved concurrency for the first deployment.
Provider selection, AWS authentication, and CloudFront acceptance remain pending.
VS5 remains a draft under D35.

## D53 - Native assessment API and deployment preparation

Date: 2026-10-11.
Status: Implementation clarification within D42 and the approved AWS blueprint.
Requirements: REQ-X02, REQ-X03, REQ-X05, REQ-X07, and REQ-X08.

The [cloud API contract](../delivery/spec-slice-05-cloud-api.md) connects authenticated native admission, reports, review records, source pages, and private downloads.
Case ownership is checked before assessment client construction.

Native bank source records keep pinned original and extraction references.
Internal processing reads all verified passages.
Public source inspection uses stable passage identifiers and pages.
Reports use private, versioned S3 objects with checksum verification before download signing.

The deployment package contains application code and verified public source files.
The package excludes private fixtures and unrelated source files.
Previous packages remain in a private archive.

The SAM template prepares encrypted queues, a dead-letter queue, and a bounded Lambda worker.
The bootstrap template defines fixed runtime roles and scoped resource permissions.
Assessment deployment remains disabled by default.
The frontend supports selected cloud assessments behind that release flag.
D30 still prohibits reserved concurrency for the first deployment.

W14 records deadline or lease exhaustion during renewal as timeout.
The correction preserves saved deadlines, counters, and replacement-claim protection.

Default report cutoffs follow their record read.
Concurrent completion cannot hide returned findings.
Explicit historical cutoffs remain unchanged.

Controlled SDK and browser checks do not establish deployed AWS permissions or live model quality.
CloudFormation schema and security validation remain pending tool approval.
Native version comparisons, provider selection, source verification, live evaluations, and deployed acceptance remain required.
AWS authentication and CloudFront acceptance remain pending.
VS5 remains a draft under D35.

## D54 - Regulatory change validation

Date: 2026-10-11.
Status: Implementation clarification within D42 and REQ-F02.
Requirements: REQ-F02, REQ-X02, REQ-X03, and REQ-X08.

The [change validation contract](../delivery/spec-slice-05-change-validation.md) defines specified source pairs and citation-supported model interpretation records.
It keeps the baseline obligation scope and permits affected controls only from the earlier mapping.
Publication dates and effective dates have different meanings.
Future requirements cannot cause an assessment for an earlier date.
Missing metadata stays unknown.

Validation cannot establish correct semantic interpretation or current source coverage.
Durable comparison admission, bounded model processing, native routes, and browser acceptance remain required.
Applicable changed requirements must cause a new snapshot without changing previous findings or human reviews.
Provider selection, live quality, AWS authentication, and CloudFront acceptance remain pending.
VS5 remains a draft under D35.

## D55 - Saved comparison processing

Date: 2026-10-11.
Status: Implementation clarification within D42, D54, and REQ-F02.
Requirements: REQ-F02, REQ-X02, REQ-X03, and REQ-X08.

The [comparison job contract](../delivery/spec-slice-05-comparison-jobs.md) defines saved admission, bounded processing, and independent reassessment records.
Comparison jobs use a different model protocol selected by their saved snapshot.
They keep the specified versions and original baseline control mappings.
Each obligation has a separate model call and saved result.
Interrupted executions keep their original deadline, consumed calls, and completed results.

Applicable changes can admit a new assessment with pinned bank sources and a different review history.
Unresolved, future, unchanged, and unfinished results cannot authorize reassessment.
Comparison jobs stay outside ordinary assessment lists.
Native routes, browser acceptance, provider approval, live quality, and deployed acceptance remain pending.
This implementation does not establish full REQ-F02 acceptance.
VS5 remains a draft under D35.

## D56 - Comparison API and reviewer interface

Date: 2026-10-11.
Status: Implementation clarification within D42, D54, and D55.
Requirements: REQ-F02, REQ-X02, REQ-X03, and REQ-X08.

The [comparison flow contract](../delivery/spec-slice-05-comparison-flow.md) connects owned saved versions, bounded jobs, cited changes, and independent reassessment admission.
The native API uses Cognito authorization, the existing queue and worker, and the disabled assessment flag.
The local API uses the same comparison rules with supervised background execution.
The accepted VS4 simulation keeps separate records and controls.

The reviewer explicitly selects the newer saved version.
Applicable changes require selection review before a new assessment.
The new snapshot keeps bank versions, the assessment date, and the complete obligation scope.
Earlier AI findings and human decisions stay unchanged.

Current source coverage, provider selection, live semantic quality, template validation, and deployed acceptance remain unverified.
Controlled HTTP and browser checks cannot establish real amendment interpretation.
The current source set has no second verified regulatory version.
The interface shows this limit instead of creating an amendment from test text.
VS5 remains a draft under D35.

## D57 - Submission-day local model and trace services

Date: 2026-10-11.
Status: Approved by the user's explicit local demo request.
Requirements: REQ-X03, REQ-X08, and LD01 through LD09.

The user requested an OpenAI API fallback and Langfuse because AWS services are unavailable today.
The [local demo contract](../delivery/spec-local-demo-openai.md) controls this exception.
New local jobs can use a saved OpenAI model identifier with fictional bank inputs and public historical regulatory text.
Langfuse receives safe measurements only.

The exception does not replace the AWS private-data boundary or establish the original model quality gates.
Earlier snapshots, findings, reviews, and approval history stay unchanged.
AWS acceptance and current regulatory coverage remain pending.

## D58 - Langfuse execution hierarchy

Date: 2026-10-11.
Status: Approved by the user's explicit skill installation and application tracing request.
Requirements: LD06 through LD08 and LF01 through LF09.

The user requested the official Langfuse skill and application tracing with current best practices.
The [execution tracing contract](../delivery/spec-langfuse-tracing.md) controls this work.
One execution parent contains stage observations with stable operation names.
Each model request retains its separate generation observation.
The integration excludes automatic content capture and uses an isolated provider.

D57's metadata-only restriction takes precedence over general recommendations to capture prompts, responses, and reasoning.
Tracing remains optional and cannot replace local audit storage.
Remote verification does not establish held-out quality or AWS acceptance.

## D59 - Local fictional-policy action instructions

Date: 2026-10-11.
Status: Implementation clarification under the user's local fictional-policy demonstration request.
Requirements: LD01 through LD09 and OP01 through OP10.

The user stated that AWS restrictions must not prevent local model calls or Langfuse Cloud observations.
The [OpenAI action contract](../delivery/spec-openai-phase-contract.md) specifies the local correction.
New OpenAI assessments use a different prompt version with explicit phase and citation instructions.
The response schema limits actions, unused fields, selected identifiers, and exact source citations before dispatch.
The instruction distinguishes documented policy controls from evidence of actual operation.

The correction keeps earlier snapshots and their instructions unchanged.
It preserves evidence validation, ownership checks, call allowances, and the metadata-only tracing boundary.
AWS acceptance and held-out model quality remain separate requirements.

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
