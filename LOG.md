# Project log

## 2026-10-08 — Approved specification package persisted

**Request implemented:** Save the approved decisions in separate, nested Markdown files under ET-Hackathon, using Rishi Voice for the explanations.

The five specification drafts were approved in the planning conversation. The user subsequently approved the persistence plan and requested implementation. That authorization is carried forward. These files do not reopen the approved choices.

### Delivered

- A [reading index](docs/guide-start-here.md) and five topic-specific blueprint documents.
- A [decision log](docs/decisions/gov-decision-log.md) separating approved choices, implementation clarifications, and unresolved verification.
- A [local test plan](docs/testing/spec-local-test-plan.md) and a separate [AI quality plan](docs/testing/eval-model-quality.md).
- Project instructions, metadata, and the seven-folder workspace structure.

### Current evidence boundary

The application is not implemented. There is no application test command yet, no executed AI evaluation, and no verified AWS deployment or account access. The metadata manifest does not claim that an application package is runnable.

The source PDF was read in full during planning. Problem 1 pages 5–6 were also visually inspected. Its saved source fingerprint is in the PRD. Earlier research identified possible AWS and RBI sources. The source-ingestion ticket must acquire and validate the actual regulatory corpus before using it as an assessment baseline.

### Verification

See [the documentation verification record](runs/2026-10-08-spec-verification.md) for the checks on this saved package. Documentation checks do not establish application correctness.

### Next task

Begin the remaining work in T1: collect and freeze the regulatory source versions and fictional bank fixtures. Then implement T2's local test environment, followed by the first complete assessment slice. Follow [the approved build order](docs/delivery/05_FEATURE_TICKETS.md).

The deadline is 10 October 2026. The internal readiness target is 9 October evening IST, not a claim that the application is already ready.

## 2026-10-09 — Technical blueprint rewritten with STE writing rules

**Request implemented:** Rewrite the technical architecture in ASD-STE100 language.

Revised [the technical blueprint](docs/architecture/02_TECHNICAL_BLUEPRINT.md) with short sentences, direct instructions, and consistent technical terms. Kept all eight sections, configuration values, record fields, source links, limits, and the distinction between approved design and verified implementation.

Saved [the original wording](runs/2026-10-09-technical-blueprint-before-ste100.txt). Added [D17](docs/decisions/gov-decision-log.md#d17--technical-blueprint-language) for the user-requested language change. Updated the handbook's writing note to identify the blueprint exception to D12.

**Verification:** The configuration table and record identity/content cells match exactly. All original links remain. Sentence/cell length, local links, identifiers, numeric tokens, file hashes, and project layout passed the checks in [the verification record](runs/2026-10-09-ste100-verification.md).

**Remaining uncertainty:** The full STE dictionary and approved-meaning review is unverified. No application code, tests, model evaluations, or cloud deployment were part of this edit.

**Next task:** T1 source and fixture acquisition remains pending. The approved application design and build order remain unchanged.

## 2026-10-09 — Project Markdown and global language rule

**Request implemented:** Apply ASD-STE100 writing rules to this project and all new projects.

The global AGENTS.md now contains the default language rule.
Other existing projects remain outside this request.

The project Markdown now uses short sentences and consistent technical terms.
[D18](docs/decisions/gov-decision-log.md#d18--project-markdown-language) records the approved style change.
The [writing guide](docs/guide-ste100-writing.md) gives the rules and technical glossary.
The [backup archive](runs/2026-10-09-before-project-ste100.zip) preserves the original project Markdown.

See the [verification record](runs/2026-10-09-project-ste100-verification.md) for the language and preservation checks.
Full dictionary compliance remains unverified.
Application implementation, software tests, live evaluations, and AWS deployment remain pending.

## 2026-10-09 - Project name

The user selected The Regulatory Agent as the project name.
The README already used this name.
Updated the PRD title and manifest identifier.
[D19](docs/decisions/gov-decision-log.md#d19---project-name) records the change.
Verified the name in the README, PRD, and manifest.

## 2026-10-09 - Current regulatory retrieval

[D20](docs/decisions/gov-decision-log.md#d20---current-regulatory-retrieval) records the user-requested design change.
The external regulatory API now supplies current regulatory content.
Provider selection remains undecided.
Saved regulatory copies serve as assessment evidence.

The blueprint defines refresh, authority verification, version history, and failure behavior.
Small related edits align product, security, interface, delivery, test, evaluation, and agent instructions.
No application code or cloud resources changed.
See the [verification record](runs/2026-10-09-regulatory-api-verification.md).

## 2026-10-09 - ArchView and architecture language review

The user requested architecture views for the full Regulatory Agent.
The user confirmed the external retrieval API and excluded a crawler view.
Added system and assessment views with editable JSON sources.
The [blueprint](docs/architecture/02_TECHNICAL_BLUEPRINT.md#architecture-views) links both views.

Applied the ASD-STE100 skill to the complete blueprint.
Preserved technical requirements, configuration values, record fields, and existing links.
The complete dictionary review remains unavailable.
See [D21](docs/decisions/gov-decision-log.md#d21---technical-architecture-views) and the [verification record](runs/2026-10-09-archview-verification.md).

No application implementation, live model evaluation, or deployment occurred.

## 2026-10-10 - Separate Draw.io architecture copy

The user requested the architecture-diagrams skill and selected Public classification.
Saved an [editable diagram](docs/architecture/arch-regulatory-agent-component-v1.drawio) and a [rendered SVG](docs/architecture/arch-regulatory-agent-component-v1.svg).
The SVG also contains editable diagram data.
The original blueprint and all six ArchView files retain their exact file hashes.

Verified 12 components, 13 flows, SVG import, and a temporary browser label edit.
The diagram retains the external retrieval API and excludes a crawler.
See the [verification record](runs/2026-10-10-architecture-diagrams-verification.md).
This change does not alter the approved application design.

## 2026-10-10 - Private repository and separate worktrees

The user selected a new private GitHub repository named `regulatory-agent`.
Created [the repository](https://github.com/rishimunikesarwani-hub/regulatory-agent) and pushed the reviewed specification checkpoint.
Prepared `work/session-a` and `work/session-b` in separate folders.
Both worktrees start from the same initial commit.

The [development guide](docs/delivery/guide-parallel-development.md) defines ownership, dependency gates, test evidence, and merge steps.
The [verification record](runs/2026-10-10-git-worktree-verification.md) records the repository and worktree checks.
Six existing ArchView link targets remain missing.
No approved specification or application code changed.
Feature development and executable tests remain pending.
