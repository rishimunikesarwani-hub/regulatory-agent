# Frontend Spec - reviewer interface

> Status: Approved in the planning conversation. First saved on 2026-10-08.
> Required documents: [PRD](../product/01_PRD.md) and [Security & Access](../security/03_SECURITY_ACCESS.md).

> Reference screenshots: **NONE — design risk**. The user gave approval to the default design.
> Decision: [D11](../decisions/gov-decision-log.md).
> Language revision: 2026-10-09.

> Measurement update: 2026-10-10. Obey [D24](../decisions/gov-decision-log.md#d24---reviewer-outcomes-and-measured-agent-baseline) and the [measurement contract](../testing/spec-measurement-contract.md).

The interface must show the requirement, control, evidence, finding, and proposed correction.
The reviewer must be able to examine each finding.
The interface must let the reviewer reject or correct it.

## 1. Screens and functions

### Cases

Show the bank profile, assessment status, and last activity.
Give fictional cases a visible Synthetic demo label.
Give a create-case action and a load-demo action.

Explain the contents of a case in the empty state.
Do not show invented completed assessments.

### Case workspace

Use Documents, Assessment, and Regulatory Changes tabs.

| Tab | Required functions |
|---|---|
| Documents | Upload bank files. Select their role. Refresh public regulations through the API. Show extraction, source versions, and verification times. Explain formats and limits before upload. |
| Assessment | Select up to 20 obligations. Start a job. Show progress. Open findings. |
| Regulatory Changes | Select the older and newer versions. Show changes and affected controls. Keep access to the previous assessment. |

If the selection exceeds a limit, request a smaller scope.
Do not select a subset without a message to the user.

Show the regulatory source authority, publication date, effective date, and last authority check that passed.
Label failed checks Freshness unverified.
After a failed check, do not let a new current assessment start.
If a selected version changed, request selection review.
Keep access to previous reports with their initial versions and dates.

### Finding detail

Show **requirement → mapped control → evidence → finding → proposed fix**.

Open the exact source passage beside the finding.
Include the document, version, and page, paragraph, line, or row location.

Reference resolution alone is not proof of claim support.
The preview must let the reviewer examine the passage's meaning.
Keep review controls near the finding.

## 2. Human review and agent events

Give Approve, Edit and accept, Reject, and Request more evidence actions.
Show final outcomes as Approved, Edited, and Rejected.
Keep the original AI finding and recommendation visible beside any saved reviewer revision.
For Edit and accept, make changed review content and a reason mandatory.
For Reject, make a reason mandatory.

A comment alone does not change an Approved item into an Edited item.
Request more evidence is a pending action until the reviewer saves a final outcome.
Do not include unsaved drafts in saved review events.
Do not discard a saved final outcome while the reviewer edits an unsaved revision.

Show review history and the current saved outcome.
Acceptance of a saved reviewer revision keeps the Edited outcome.
To save Approved, the reviewer must select the original AI item, also after a previous edit.
Retry a failed save. Do not add duplicate events or metric counts.

If a different save changed the current revision, show a revision conflict. Keep the draft.
Before the reviewer sends the changed draft again, make review of the saved content mandatory.
Do not carry a review outcome into a new assessment automatically.

An Approved outcome accepts the recommendation. It does not change the original AI finding status.
For example, the reviewer can give approval to a needs_review finding that requests missing evidence.
Do not show that approval as Supported or as proof of bank compliance.

Show completed stages, tool actions, examined sources, and stop reasons.
Use factual events. Example: “Retrieved three evidence passages.”
Do not show hidden chain-of-thought.
Do not invent progress percentages.

Label controlled model outputs Simulated.
Live outputs must identify their input snapshot and job status.
A demo dataset that looks like bank data must not hide simulated model processing.

### Review outcome summary

Show the summary in the Assessment tab for the selected authorized cohort.
Use approval without edits as the primary rate.
Show the edited and rejected shares with their counts and common reviewed-item denominator.
Show adoption with edits as a different secondary measure.
Also show review coverage, pending items, result coverage, failed jobs, partial jobs, and unchecked obligations.

Show the recommendation-availability window, filters, and report cutoff for reviewer rates.
Show the job-admission window for runtime and result-coverage measures.
These time bases can produce different populations. Label them independently.
Use Not measured for zero denominators. Never invent an empty-cohort percentage.

Use the last saved final review for each item. Revisions must not increase the item count.
Show the baseline model/prompt version and synthetic or live status for comparisons.
Do not combine simulated and live results.
Do not label approval as accuracy.

Keep the same formulas in the interface, API response, and export.

### Runtime details

Show recorded stage outcomes, duration, retry counts, and safe stop reasons in job details.
Give authorized links from a trace to its selected source passages.
Show numeric model token usage when available.
Label cost as estimated or billed. Show its included components.

If usage or price data is missing, show Unknown.
Do not show a partial cost estimate as total system cost.
Keep raw prompts, responses, query text, credentials, and hidden reasoning out of the event timeline.
Show source text and reviewer content only in their authorized evidence and review views.

Do not show an audit-save failure as a completed assessment.
An external metric-export failure must not start one more assessment.

**Technical:** The timeline shows application audit events.
**ELI10:** It shows the agent's actions and the documents used for those actions.

## 3. Visual specification

| Role | Value | Use |
|---|---|---|
| Page background | #F8FAFC | Workspace background |
| Surface | #FFFFFF | Panels, tables, and source previews |
| Text | #0F172A | Primary text and headings |
| Primary/action | #1D4ED8 | Buttons, links, and active controls |
| Muted text | #475569 | Secondary data. Do a check of contrast. |
| Supported indicator | #166534 | Status text and icon. Do not use color alone. |
| Review/partial indicator | #92400E | Needs-review and partial states |
| Gap/error indicator | #B91C1C | Gaps with evidence and failures |

The last four text and status colors are implementation defaults.
They extend the approved palette.
Do a check of contrast in the implemented interface.

Use local system fonts.
Use 16 px body text and approximately 14 px labels.
Use heading sizes from 20–28 px.
Use 8 px spacing increments and 8 px corners.
Use light borders and limited shadows.

For example, use Run assessment, Compare versions, Inspect source, and Save review as action labels.
Connect each input to its label.
Put validation information beside the related field.

## 4. Layout and access

Design the desktop workspace first.
Show the finding and source panel beside each other.

Below 768 px, replace wide tables with stacked cards.
Use a full-width evidence view.

Keyboard navigation must give access to tabs, findings, source previews, and review controls.
Keep keyboard focus visible.
When the source panel opens, move focus in the same way each time.
When the panel closes, move focus back to its previous position.

Include text in status labels.
Distinguish Needs review from a passed assessment.

## 5. Connections and interface states

| Connection | Progress state | Failure or partial state |
|---|---|---|
| Identity | Sign-in indicator | Go back to sign-in. Keep safe navigation context. |
| Cases | Load indicator | Retry action. No false case data. |
| Upload/extraction | Per-file stages | Specific rejection. Show that the file is not ready. |
| Regulatory retrieval | Source-check progress and selected scope | Freshness unverified. Retry action. No silent use of an old source. |
| Assessment job | Recorded stage and tool events | Stop reason, completed findings, and unchecked obligations |
| Citations | Source-load indicator | Unavailable or invalid reference. No invented excerpt. |
| Version comparison | Identified version pair and progress | Keep the previous assessment and validated comparison outputs. |
| Review save | Pending-save indicator | Keep the note. Retry without duplicate decisions. |
| Export | Generation indicator | Explain failure. Do not give a partial export a success label. |

Export only an authorized snapshot.
Include source references, versions, findings, job status, limitations, and reviewer decisions in Markdown and JSON exports.
Give partial exports a clear label.
Include regulatory source URLs, authority verification time, and freshness status.

Include original recommendation IDs, saved reviewer revisions, outcome counts, denominators, cohort definition, and report cutoff.
Include metric version and available safe runtime measurements with their missing-data labels.
An export with a previous cutoff must keep the review outcomes applicable at that cutoff.

## 6. Browser acceptance

Use this sequence:

1. Refresh regulations. Upload bank documents.
2. Start an assessment.
3. Examine a citation.
4. Record a review.
5. Compare regulatory versions.
6. Export the result.

Also do tests of invalid uploads, access denial, interrupted jobs, invalid citations, keyboard navigation, and a narrow viewport.
BT-06 must also test all three final review outcomes, pending actions, edit validation, outcome revisions, zero denominators, and summary/export parity.
These are planned acceptance checks.
The project has no tested browser implementation.

[Next: Feature tickets](../delivery/05_FEATURE_TICKETS.md)
