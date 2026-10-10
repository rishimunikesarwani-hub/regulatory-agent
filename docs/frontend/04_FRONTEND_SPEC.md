# Frontend Spec - reviewer interface

> Status: Approved in the planning conversation. First saved on 2026-10-08.
> Required documents: [PRD](../product/01_PRD.md) and [Security & Access](../security/03_SECURITY_ACCESS.md).
> Reference screenshots: **NONE — design risk**. The user approved the default design.
> Decision: [D11](../decisions/gov-decision-log.md).
> Language revision: 2026-10-09.

The interface must show the requirement, control, evidence, finding, and proposed correction.
The reviewer must be able to inspect and challenge each finding.

## 1. Screens and functions

### Cases

Show the bank profile, assessment status, and latest activity.
Give fictional cases a visible Synthetic demo label.
Provide a create-case action and a load-demo action.

Explain the contents of a case in the empty state.
Do not show invented completed assessments.

### Case workspace

Use Documents, Assessment, and Regulatory Changes tabs.

| Tab | Required functions |
|---|---|
| Documents | Upload bank files. Select their role. Refresh public regulations through the API. Show extraction, source versions, and verification times. Explain formats and limits before upload. |
| Assessment | Select up to 20 obligations. Start a job. Show progress. Open findings. |
| Regulatory Changes | Select explicit older and newer versions. Show changes and affected controls. Keep access to the previous assessment. |

If the selection exceeds a limit, request a smaller scope.
Do not select an arbitrary subset without telling the user.

Show the regulatory source authority, publication date, effective date, and last successful authority check.
Label failed checks Freshness unverified.
Do not permit a new current assessment after a failed check.
If a selected version changed, request selection review.
Keep earlier reports accessible with their original versions and dates.

### Finding detail

Show **requirement → mapped control → evidence → finding → proposed fix**.

Open the exact source passage beside the finding.
Include the document, version, and page, paragraph, line, or row location.

Reference resolution alone does not establish support.
The preview must permit review of the passage's meaning.
Keep review controls near the finding.

## 2. Human review and agent events

Provide Agree, Disagree, and Request more evidence actions.
Record the review note.
Show the reviewer disposition separately from the AI finding.

Show completed stages, tool actions, inspected sources, and stop reasons.
Use factual events such as “Retrieved three evidence passages.”
Do not show hidden chain-of-thought.
Do not invent progress percentages.

Label controlled model outputs Simulated.
Live outputs must identify their input snapshot and job status.
A realistic demo dataset must not hide simulated model processing.

**Technical:** The timeline shows application audit events.
**ELI10:** It shows the agent's actions and the documents used for those actions.

## 3. Visual specification

| Role | Value | Use |
|---|---|---|
| Page background | #F8FAFC | Workspace background |
| Surface | #FFFFFF | Panels, tables, and source previews |
| Text | #0F172A | Main text and headings |
| Primary/action | #1D4ED8 | Buttons, links, and active controls |
| Muted text | #475569 | Secondary data. Verify contrast. |
| Supported indicator | #166534 | Status text and icon. Do not use color alone. |
| Review/partial indicator | #92400E | Needs-review and partial states |
| Gap/error indicator | #B91C1C | Evidenced gaps and failures |

The last four text and status colors are implementation defaults.
They extend the approved palette.
Verify contrast in the actual interface.

Use local system fonts.
Use 16 px body text and approximately 14 px labels.
Use heading sizes from 20–28 px.
Use 8 px spacing increments and 8 px corners.
Use light borders and limited shadows.

Use action labels such as Run assessment, Compare versions, Inspect source, and Save review.
Associate each input with its label.
Put validation information beside the related field.

## 4. Layout and access

Design the desktop workspace first.
Show the finding and source panel beside each other.

Below 768 px, replace wide tables with stacked cards.
Use a full-width evidence view.

Keyboard navigation must reach tabs, findings, source previews, and review controls.
Keep keyboard focus visible.
Move focus predictably when the source panel opens.
Restore focus when the panel closes.

Include text in status labels.
Distinguish Needs review from a passed assessment.

## 5. Connections and interface states

| Connection | Progress state | Failure or partial state |
|---|---|---|
| Identity | Sign-in indicator | Return to sign-in. Keep safe navigation context. |
| Cases | Load indicator | Retry action. No false case data. |
| Upload/extraction | Per-file stages | Specific rejection. Show that the file is not ready. |
| Regulatory retrieval | Source-check progress and selected scope | Freshness unverified. Retry action. No silent use of an old source. |
| Assessment job | Actual stage and tool events | Stop reason, completed findings, and unchecked obligations |
| Citations | Source-load indicator | Unavailable or invalid reference. No invented excerpt. |
| Version comparison | Identified version pair and progress | Keep the previous assessment and valid comparison outputs. |
| Review save | Pending-save indicator | Keep the note. Retry without duplicate decisions. |
| Export | Generation indicator | Explain failure. Do not label a partial export successful. |

Export only an authorized snapshot.
Include source references, versions, findings, job status, limitations, and reviewer decisions in Markdown and JSON exports.
Label partial exports explicitly.
Include regulatory source URLs, authority verification time, and freshness status.

## 6. Browser acceptance

Use this sequence:

1. Refresh regulations and upload bank documents.
2. Start an assessment.
3. Inspect a citation.
4. Record a review.
5. Compare regulatory versions.
6. Export the result.

Also do tests of invalid uploads, access denial, interrupted jobs, invalid citations, keyboard navigation, and a narrow viewport.
These are planned acceptance checks.
The project has no tested browser implementation.

[Next: Feature tickets](../delivery/05_FEATURE_TICKETS.md)
