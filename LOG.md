# Project log

## 2026-10-08 — Approved specification package persisted

**Completed request:** Save the approved decisions in different, nested Markdown files under ET-Hackathon, using Rishi Voice for the explanations.

The user approved the five specification drafts in the planning conversation.
The user then approved the save plan and requested its implementation.
That authorization still applies.
These files do not change the approved choices.

### Delivered

- A [document index](docs/guide-start-here.md) and five topic-specific blueprint documents.
- A [decision log](docs/decisions/gov-decision-log.md) separating approved choices, implementation clarifications, and unresolved verification.
- A [local test plan](docs/testing/spec-local-test-plan.md) and a different [AI quality plan](docs/testing/eval-model-quality.md).
- Project instructions, metadata, and the seven-folder workspace structure.

### Current evidence boundary

The application is not built.
No application test command, AI evaluation result, or verified AWS deployment exists yet.
Account access is unverified.
The metadata manifest does not claim that the application can operate.

The planning review examined the complete source PDF.
It included a visual review of Problem 1 pages 5–6.
The PRD contains the saved source fingerprint.
Earlier research identified possible AWS and RBI sources.
The source-ingestion ticket must get and validate the actual regulatory corpus before its use as an assessment baseline.

### Verification

See [the documentation verification record](runs/2026-10-08-spec-verification.md) for the checks on this saved package. Documentation checks do not establish application correctness.

### Next task

Start the open T1 work: collect the regulatory source versions and fictional bank fixtures.
Keep these inputs unchanged for each assessment.
Then build T2's local test environment.
Next, build the first complete assessment workflow.
Follow [the approved build order](docs/delivery/05_FEATURE_TICKETS.md).

The deadline is 10 October 2026. The internal readiness target is 9 October evening IST, not a claim that the application is already ready.

## 2026-10-09 — Technical blueprint rewritten with STE writing rules

**Completed request:** Rewrite the technical architecture in ASD-STE100 language.

Revised [the technical blueprint](docs/architecture/02_TECHNICAL_BLUEPRINT.md) with short sentences, direct instructions, and consistent technical terms. Kept all eight sections, configuration values, record fields, source links, limits, and the distinction between approved design and verified implementation.

Saved [the original wording](runs/2026-10-09-technical-blueprint-before-ste100.txt). Added [D17](docs/decisions/gov-decision-log.md#d17--technical-blueprint-language) for the user-requested language change. Updated the handbook's writing note to identify the blueprint exception to D12.

**Verification:** The configuration table and record identity/content cells match exactly. All original links stay unchanged. Sentence/cell length, local links, identifiers, numeric tokens, file hashes, and project layout passed the checks in [the verification record](runs/2026-10-09-ste100-verification.md).

**Remaining uncertainty:** The full STE dictionary and approved-meaning review was incomplete at that time. No application code, tests, model evaluations, or cloud deployment were part of this edit.

**Next task:** T1 source and fixture acquisition stays pending. The approved application design and build order stay unchanged.

## 2026-10-09 — Project Markdown and global language rule

**Completed request:** Apply ASD-STE100 writing rules to this project and all new projects.

The global AGENTS.md now contains the default language rule.
Other existing projects stay outside this request.

The project Markdown now uses short sentences and consistent technical terms.
[D18](docs/decisions/gov-decision-log.md#d18--project-markdown-language) records the approved style change.
The [writing guide](docs/guide-ste100-writing.md) gives the rules and technical glossary.
The [backup archive](runs/2026-10-09-before-project-ste100.zip) keeps the original project Markdown.

See the [verification record](runs/2026-10-09-project-ste100-verification.md) for the language and preservation checks.
Full dictionary compliance was unverified for that review.
Application implementation, software tests, live evaluations, and AWS deployment stay pending.

## 2026-10-09 - Project name

The user selected The Regulatory Agent as the project name.
The README already used this name.
Updated the PRD title and manifest identifier.
[D19](docs/decisions/gov-decision-log.md#d19---project-name) records the change.
Did a check of the name in the README, PRD, and manifest.

## 2026-10-09 - Current regulatory retrieval

[D20](docs/decisions/gov-decision-log.md#d20---current-regulatory-retrieval) records the user-requested design change.
The external regulatory API now supplies current regulatory content.
Provider selection stays undecided.
Saved regulatory copies serve as assessment evidence.

The blueprint specifies refresh, authority verification, version history, and failure behavior.
Related edits keep the product, security, interface, delivery, test, evaluation, and agent instructions consistent.
No application code or cloud resources changed.
See the [verification record](runs/2026-10-09-regulatory-api-verification.md).

## 2026-10-09 - ArchView and architecture language review

The user requested architecture views for the full Regulatory Agent.
The user confirmed the external retrieval API and excluded a crawler view.
Added system and assessment views with editable JSON sources.
The [blueprint](docs/architecture/02_TECHNICAL_BLUEPRINT.md#architecture-views) links both views.

Applied the ASD-STE100 skill to the complete blueprint.
Kept technical requirements, configuration values, record fields, and existing links unchanged.
The complete dictionary was unavailable for that review.
See [D21](docs/decisions/gov-decision-log.md#d21---technical-architecture-views) and the [verification record](runs/2026-10-09-archview-verification.md).

No application implementation, live model evaluation, or deployment occurred.

## 2026-10-10 - Separate Draw.io architecture copy

The user requested the architecture-diagrams skill and selected Public classification.
Saved an [editable diagram](docs/architecture/arch-regulatory-agent-component-v1.drawio) and a [rendered SVG](docs/architecture/arch-regulatory-agent-component-v1.svg).
The SVG also contains editable diagram data.
The original blueprint and all six ArchView files kept their exact file hashes.

Did checks of 12 components, 13 flows, SVG import, and a temporary browser label edit.
The diagram keeps the external retrieval API and excludes a crawler.
See the [verification record](runs/2026-10-10-architecture-diagrams-verification.md).
This change does not change the approved application design.

## 2026-10-10 - Private repository and separate worktrees

The user selected a new private GitHub repository named `regulatory-agent`.
Made [the repository](https://github.com/rishimunikesarwani-hub/regulatory-agent) and pushed the reviewed specification checkpoint.
Prepared `work/session-a` and `work/session-b` in different folders.
Both worktrees start from the same initial commit.

The [development guide](docs/delivery/guide-parallel-development.md) specifies ownership, dependency gates, test evidence, and merge steps.
The [verification record](runs/2026-10-10-git-worktree-verification.md) records the repository and worktree checks.
Six existing ArchView link targets are missing.
No approved specification or application code changed.
Feature development and executable tests stay pending.

## 2026-10-10 - One-agent and multi-agent comparison

Saved a [comparison table](docs/architecture/arch-agent-operation-comparison.md) and a [multi-agent proposal](docs/architecture/arch-multi-agent-proposal.md).
The proposal specifies one coordinator and six specialist roles.
It keeps the shared 24-call allowance and 600-second deadline.
Authentication and governance enforcement stay application responsibilities.

[D22](docs/decisions/gov-decision-log.md#d22---agent-operation-comparison) records the requested direction and proposed allocations.
The approved specifications and existing diagrams stay unchanged.
The comparison has no measured performance result.
See the [verification record](runs/2026-10-10-agent-comparison-verification.md).

## 2026-10-10 - AWS agent review

Saved the [AWS review](docs/architecture/arch-agent-aws-review.md).
Reduced the [comparison](docs/architecture/arch-agent-operation-comparison.md) to five decision points.
Marked the earlier seven-role proposal as review history.
The recommendation is one bounded agent with orchestration in code.
Two specialists are still an evaluation candidate.

[D23](docs/decisions/gov-decision-log.md#d23---aws-review-and-code-orchestration) records the user's clarification and the review outcome.
The formal audit includes 17 areas and shows UNVERIFIED performance.
No runtime measurements or cloud actions occurred.
The approved specifications and existing diagrams stay unchanged.
See the [verification record](runs/2026-10-10-aws-agent-review-verification.md).

## 2026-10-10 - Retrieval quality and model routing argument

Saved [review notes](docs/architecture/arch-retrieval-quality-and-model-routing.md) on retrieval, assessment checks, observability, and routing.
The notes challenge the proposed approach and identify the missing labeled retrieval fixtures.
They use different measures for runtime checks, source coverage, and assessment quality.
Model routing stays a proposed experiment, not an approved model change.
No application, cloud resource, or approved specification changed.

## 2026-10-10 - Approved measurement specification

[D24](docs/decisions/gov-decision-log.md#d24---reviewer-outcomes-and-measured-agent-baseline) adopts the user's one-agent measurement baseline.
Updated all five specifications and both test plans.
Added the [measurement contract](docs/testing/spec-measurement-contract.md).

Approval without edits is the primary product measure.
Edited and rejected shares have different fields, with review coverage and pending counts.
The specifications make different evaluations for retrieval and assessment mandatory.
They also make a trace for each stage mandatory.
The approved model, 24-call allowance, 600-second worker deadline, India boundaries, and existing correctness gates stay unchanged.

Added 11 planned software and cloud test groups and six retrieval evaluation groups.
Kept all 20 existing assessment case rows unchanged.
Did checks of formula examples, new links, requirement references, and selected STE rules.
Six earlier ArchView targets are missing.
The change added no missing target.
See the [verification record](runs/2026-10-10-measurement-spec-verification.md).

Application tests and live evaluations stay pending.
Next: prepare labeled fixtures and write failing contract tests before implementation.

## 2026-10-10 - Permanent STE documentation rule

The user repeated the ASD-STE100 requirement for all documentation.
Updated [AGENTS.md](AGENTS.md#documentation-language-always-use-asd-ste100) with mandatory steps for every new document and document change.
[D25](docs/decisions/gov-decision-log.md#d25---permanent-documentation-language-rule) records this instruction.

Retrieved the complete official ASD-STE100 Issue 9 standard and dictionary.
Corrected the current specifications, plans, instructions, and architecture review text.
The [language guide](docs/guide-ste100-writing.md) records word choices and project technical terms.
The language correction keeps the approved design, formulas, test meanings, limits, and approval history unchanged.

Saved the [source backup](runs/2026-10-10-before-ste-language-correction.zip) before the corrections.
See the [language review record](runs/2026-10-10-ste-language-correction-verification.md) for the checks and their limits.
Earlier verification records keep their dated results.
Application tests and live evaluations stay pending.
Next: prepare labeled fixtures and write failing contract tests before application code.

## 2026-10-10 - Foundation integration and remaining worktrees

Merged [Session A PR #1](https://github.com/rishimunikesarwani-hub/regulatory-agent/pull/1) and [Session B PR #2](https://github.com/rishimunikesarwani-hub/regulatory-agent/pull/2) into `main`.
The combined offline checks passed 60 tests.
The DEV-02 demonstration gave its expected contract results, with no compliance findings or live model calls.

Kept the final Session A fixtures during integration.
Kept the older Session B import in a named Git stash with unchanged bytes.
The existing specification edits kept their file hashes during the update from remote `main`.
Historical evidence records keep their original results.

[D26](docs/decisions/gov-decision-log.md#d26---foundation-integration-and-remaining-worktrees) records the integration and new worktree allocation.
The [worktree guide](docs/delivery/guide-next-worktrees.md) gives eight assignments and their dependency conditions.
The [integration record](runs/2026-10-10-integration/verification.md) gives the evidence and preparation results.

Prepared eight worktrees with independent Python 3.12.13 environments.
Each worktree passed 60 offline tests from cached dependencies.
The [preparation record](runs/2026-10-10-integration/worktree-readiness.json) identifies the branches, paths, dependency conditions, and results.
No new application feature or server started during preparation.

T1 and T2 D24 additions are pending.
T3 through T9 implementation is pending.
Next: start the foundation measurement task only when the user requests implementation.

## 2026-10-10 - Complete delivery slices and first case flow

The user authorized development, tests, and GitHub updates, one worktree at a time.
[D27](docs/decisions/gov-decision-log.md#d27---delivery-by-complete-user-flow) replaces the earlier allocation by technical component.
Each slice now includes its frontend, backend, AWS configuration, and tests.
All eight MVP features and all 115 existing acceptance rows remain in the tickets.

Used `work/autonomous-build` in an isolated worktree.
Reconciled Session A fixtures, Session B contracts, and the latest specification changes.
Kept the source worktrees and their uncommitted files.
The [reconciliation record](runs/2026-10-10-autonomous-build/reconciliation.json) identifies the inspected branches and source hashes.

Saved the [case API contract](docs/delivery/spec-slice-01-cases.md) before frontend and backend implementation.
Both components use the same request, response, and error contracts.
The local user can sign in, make a fictional case, save it, and reopen it.
SQLite saves local cases across process restarts.
The AWS adapter uses Cognito identity and owner-scoped DynamoDB records.
AWS operation remains unverified.

Saved failing tests before the related implementation changes.
The [Python report](runs/2026-10-10-autonomous-build/final-python-green.txt) records 163 passing tests, including the release guards.
The [browser report](runs/2026-10-10-autonomous-build/frontend-green.txt) records 11 passing tests.
The browser checks include the actual local API, keyboard operation, a narrow viewport, and failed saves.
Desktop and mobile screenshots received visual checks.
The [clean setup report](runs/2026-10-10-autonomous-build/clean-source-green.txt) records successful setup with a new environment and an empty package cache.

D24 functions now calculate reviewer outcomes, retrieval measures, assessment measures, stage timing, and recorded costs.
Their tests cover saved review revisions, report cutoffs, denominators, missing data, and repeated event records.
Complete runtime connections, live model evaluations, and measured model quality remain pending.
Unit test results do not prove assessment quality.

Prepared one serialized [development pipeline](.github/workflows/dev-release.yml).
It requires integration checks before deployment and browser checks after deployment.
Each release record includes its URL, commit, results, and limits.
The [SAM review](runs/2026-10-10-autonomous-build/sam-validation.json) passed local infrastructure checks.
No AWS deployment occurred.
Production deployment still needs explicit authorization.

The user said an AWS account is not set up.
The [development guide](docs/delivery/guide-slice-01-development.md) lists the missing account, roles, budget, and secure workflow configuration.
No secrets are requested in chat.
The first slice is ready for account setup and deployment verification.
Its AWS acceptance remains open.
Next: finish that verification, then extend the flow to evidence inspection and one-obligation review under VS2 and VS3.

### Final worktree reconciliation

A later inspection found eight additional worktrees at the local specification commit `e68ab5d`.
The project has 12 registered worktrees, including the original integration folder and the active slice folder.
The [current inventory](runs/2026-10-10-autonomous-build/final-worktree-inventory.json) records their branches and file states.
Kept their existing branch names and local files.
The vertical slice plan controls their next assignments.

The latest blueprint clarifies retrieval-operation limits and the missing shared response-byte total.
Kept that clarification during reconciliation.
The clarification does not establish live provider enforcement.

### Prepared worktrees after PR #3

Updated the eight prepared worktrees with the current integrated code and D27 instructions.
Each worktree and `MVP` passed 163 Python tests and the frontend build with cached dependencies.
The [current preparation record](runs/2026-10-10-integration/worktree-refresh.md) gives source and environment evidence.
The additional folders stay reserved until the user selects a complete flow.
No application code, running server, or cloud resource was added during this preparation.

## 2026-10-10 - Slice 01 feedback checkpoint

The user requested one complete slice at a time for testing and feedback.
Updated the active slice worktree from `main` at `7489fc8` through a fast-forward merge.
The local case flow passed 163 Python checks and 11 browser checks.
The frontend build passed.
The browser checks include saved-case reload, failed saves, keyboard use, and a narrow viewport.
The [current evidence](runs/2026-10-10-slice-01-feedback/) keeps these results and screenshots.

Opened the local interface at `http://127.0.0.1:5173/` for user review.
Its API uses a separate feedback database in ignored `runs/private/` storage.
The browser-test database remains separate.
Local identity does not prove Cognito authentication.

The `rishicodex` AWS profile authenticated in account `482439369658`.
CloudFormation and Lambda inspection returned access-denied responses.
The browser console confirmed four existing policies and no active Mumbai application stacks.
The user selected a USD 25 monthly budget.
The alert is not configured.

Prepared the [account access template](ops/aws-development-bootstrap.yaml) under D28.
Wrote failing deployment checks before changing the runtime role configuration.
The revised Python checks pass.
Both infrastructure templates pass `cfn-lint 1.57.2` without findings.
The setup does not give CloudFormation permission to change IAM policies.
Live permission coverage and the separate compliance check remain unverified.

Requested confirmation for the new permissions under the browser security policy.
The console file chooser did not open through the browser tool.
No template upload or AWS stack creation completed.
Next: collect local feedback, install the approved access setup, and complete AWS deployment and browser acceptance.
Keep VS2 pending until the first slice review is complete.

### Sign-in return correction

The review found that cloud sign-in lost the selected case after a page reload.
A controlled browser test reproduced this failure before the correction.
The temporary state now keeps the selected case ID with its existing random value.
The callback validates that state and ID before restoring the case location.
It does not accept an external return URL.
Access tokens stay in memory, and temporary sign-in values are removed.

The new return-flow test passes for initial sign-in and sign-in after reload.
The state-mismatch and external-return-URL checks pass.
The frontend build passes.
The deployed browser check now requires reopening the same case after sign-in again.
That live check remains pending.
No AWS resources or permissions changed during this correction.

All 13 browser checks passed after the correction.
They used a separate API on port `8111` and the test database.
The temporary test API was stopped after verification.
The feedback API and interface remain available on ports `8110` and `5173`.
The [updated verification record](runs/2026-10-10-slice-01-feedback/verification-v2.json) identifies the checked files and results.

### AWS authentication and release preparation

The user requested AWS deployment and offered to complete authentication.
The temporary profile `et-hackathon-admin` has an open AWS sign-in request.
Authentication has not finished.
The existing `rishicodex` permissions stay unchanged.

The release changes were saved in commit `9b08e74` and pull request `5`.
The GitHub integration checks passed for that commit.
The development environment now permits deployments from `main` only.

Live inspection found that this repository uses immutable GitHub identity subjects.
Decision D29 records the verified owner and repository IDs.
A new check failed with the old subject before the template correction.
All 164 backend checks pass after the correction.
Both templates pass cfn-lint 1.57.2.
The application interface and its 13 passing browser checks stay unchanged.

Next: complete AWS authentication, verify account access, and install the reviewed development setup.
Then configure the spending alert and run the serialized release pipeline.
AWS deployment and live browser acceptance remain pending.

### Development access installation and sign-in design

Temporary AWS authentication completed for account `482439369658`.
The reviewed access stack reached `CREATE_COMPLETE` in Mumbai.
It created three development roles, a GitHub identity provider, and the private artifact bucket with its policy.
The existing IAM user's policies stay unchanged.

The verified Lambda concurrency quota is 10.
Decision D30 removes the incompatible capacity reservation.
The API now uses a request rate target of 2 requests per second and a burst target of 4 requests.
These traffic targets are not a spending cap.
The USD 25 alert still needs the user's recipient selection.

The official AWS Guard 3.2.1 archive matched its published SHA-256 digest.
The selected security rules passed after the transport condition used Boolean `false`.
Both templates passed cfn-lint 1.57.2.
CloudFormation returned no pre-deployment validation errors for the access setup.
CloudTrail event history records its plan operation, but no durable trail is configured.

The user supplied nine design references and three specific sign-in changes.
Decision D31 records those approved changes.
The interface now shows `The Regulator` and a centered sign-in card.
The introduction and explanatory card paragraphs were removed.
The sign-in action and authentication error handling stay available.

The new design check failed before implementation.
All 14 browser checks pass after the changes.
All 165 backend checks and the frontend build pass.
Desktop and mobile screenshots are in the slice feedback evidence directory.
The separate browser-test API was stopped after verification.
The user feedback API and interface remain available.

Next: configure the budget alert, finish the reviewed integration, and run the AWS release pipeline.
Live AWS application acceptance is pending.

### First development release and transform correction

The USD 25 monthly budget is configured and healthy.
Actual cost alerts use 80% and 100% thresholds.
The forecast alert uses a 100% threshold.
The account owner's verified email receives the alerts.
The budget is not a spending cap.

Pull request 5 merged after all integration checks passed.
Release run `38070282103` stopped before application resource creation.
The CloudFormation execution role lacked `cloudformation:CreateChangeSet` for the AWS SAM transform.
Decision D32 records the correction for that exact transform ARN.
The new permission check failed before the correction.
All 166 backend checks pass after the correction.
Both templates pass cfn-lint 1.57.2.
The selected AWS Guard rules pass for the corrected access template.

Next: verify the access update, merge the correction, and retry the serialized application release.
Live application acceptance remains pending.

### CloudFront verification handoff

The transform correction passed GitHub checks and merged through pull request 6.
Application release `38071339699` used commit `acfb4bc1d87bf646281db2f6633799f1d3e3e6f3`.
Its integration checks passed.
CloudFront rejected distribution creation because account `482439369658` needs AWS verification.
The application stack reached `ROLLBACK_COMPLETE`.
No application URL was produced, and live browser acceptance was skipped.

The configured retention rules preserved the case table, frontend bucket, and user pool.
Live checks found zero records, zero objects, and zero users.
The test operator process stopped without creating a user.
No retained resource was deleted manually.

Decision D34 records the user's choice to keep CloudFront.
The AWS Support request is prepared in the open Chrome tab and has not been sent.
The verification guide records the manual submission steps and recovery boundary.
The local feedback interface remains available with the requested sign-in design.
All 166 backend checks and 14 local browser checks passed before the release.

Next: obtain AWS account verification and review the failed stack recovery.
Live AWS acceptance remains pending.

### VS2 local document slice

The user approved VS1 locally and authorized VS2 while AWS verification is pending.
D35 controls the isolated branch, worktree, ports, and databases.
D36 and the VS2 source contract were recorded before implementation.
The new HTTP tests failed for missing document routes.
The browser tests failed for the missing document interface.
The port guard found the old API address before any writes.

Local upload now supports text PDF, DOCX, TXT, and CSV.
Each source version keeps its original bytes and exact text locations.
Replacements keep earlier versions accessible.
Case access checks apply to upload, inspection, replacement, and original download.
File and case limits reject excess input without a partial save.
One different extraction process stops after 10 seconds.
The timeout test failed before its safe rejection correction.
The uncertain-save test failed before its retry guard.

All 178 backend checks and 20 combined browser checks passed.
The frontend build passed.
The source screen was inspected in Chrome with the fictional policy fixture.
The feedback interface uses port `5182` and API port `8120`.
Its database is `runs/private/slice-02/feedback.sqlite`.
Browser tests use API port `8121` and their own database.
The VS1 feedback services and unrelated worktree changes stay unchanged.

Read the [local evidence](runs/2026-10-10-slice-02-documents/review-local.md) and [development guide](docs/delivery/guide-slice-02-development.md).
The user approved VS2 local acceptance and authorized VS3 local development.
The VS2 integration merge stays pending until GitHub checks pass.
AWS source adapters, service permissions, and deployed browser acceptance stay pending.
The Support verification request has not been sent by this session.
No cloud resources were deleted manually.

Next: complete the checked VS2 integration merge.
Start the authorized VS3 local slice after that merge.
Keep the CloudFront verification handoff open.

### VS3 controlled assessment and saved review

Date: 2026-10-11.

VS2 merged through pull request 8 after GitHub checks passed.
The integration commit is `c0413c8b030383a98926acccf06c2bff3d2bdd51`.
The integration worktree was updated without changes to the user's Design Ideas.
The user authorized VS3 local development while AWS verification is pending.
D37 and the VS3 contract were recorded before implementation.

The assessment HTTP tests failed for missing routes.
The browser test failed for the missing assessment screen.
A different negative test found an unsupported operational claim with valid policy quotations.
The validation correction now rejects that claim before finding presentation.
The first browser integration run found a different telemetry time-field name.
The corrected interface uses the existing seconds field.

VS3 now saves one controlled historical assessment and its fixed source snapshot.
It keeps RBI conditions, exceptions, applicability uncertainty, and exact citations accessible.
Saved Approved, Edited, Rejected, and evidence-request events keep the initial finding unchanged.
Review summaries use D24 cutoff and final-outcome rules.

Stale or uncertain saves keep the user's draft.
A failed refresh cannot enable another uncertain save.
Expired access clears private findings and review drafts.

The case-switch test failed before the new-case assessment status correction.
All 189 backend checks and 26 combined browser checks passed.
The frontend build passed.
Desktop and mobile assessment screens were inspected.
The [development guide](docs/delivery/guide-slice-03-development.md) records the isolated feedback services and review steps.
The [local evidence](runs/2026-10-10-slice-03-assessment/review-local.md) records the test scope and limits.

No live model call was made.
Current regulatory verification and AWS assessment adapters stay unconfigured.
CloudFront account verification remains necessary before deployment.
No Support message was sent by this session.
No cloud resource was deleted manually.

Next: obtain VS3 local feedback before merge and VS4 development.
