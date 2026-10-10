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
