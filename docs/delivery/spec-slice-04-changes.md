# VS4 simulated version comparison

Date: 2026-10-11.
Status: Implementation contract within the user's approved VS4 local development under D40.
Requirements: REQ-F02, REQ-X02, REQ-X03, REQ-X07, and REQ-X08.
Tickets: T1, T3, T5, and the applicable T6 through T9 work.

## Purpose and limits

The reviewer selects two specified regulatory versions and an earlier assessment snapshot.
A snapshot is the unchanged set of inputs saved for one assessment.
A changed requirement starts a new controlled assessment with different findings and review records.
Earlier source copies, findings, and human reviews stay unchanged.

Use the existing `SIM-ACCESS` source fixtures in `data/sources/source-manifest.json`.
These fixtures describe simulated amendments. They do not describe RBI events.
Keep the historical RBI example available.
Keep current assessments blocked when source verification is unavailable.
No live regulatory provider or model invocation belongs to this controlled acceptance record.

Use one fixed comparison of `v1` with `v2-added`, `v2-replaced`, or `v2-cosmetic`.
The simulated assessment date is `2024-05-08`.
The selected obligation is `SIM-ACCESS-1`.
Keep the approved fictional policy fixture and control `ACCESS-01`.
Do not read evaluation labels during application execution.

## Saved sources and behavior

Keep both complete source passages, authority labels, version IDs, dates, and source locations in the comparison record.
Show source metadata changes independently of changed requirements.
The added requirement asks for a different reviewer to approve each weekly review.
Identify `ACCESS-01` as the affected control.

Request dated records and evidence of approval by a different reviewer in the new finding.
Missing evidence gives `needs_review`, with an evidence gap. It does not prove an operational failure.

The replacement wording keeps the same requirement in this fixed example.
The cosmetic version changes punctuation only.
Neither comparison starts another assessment automatically.
This fixed classification is not a general method for interpretation of regulatory changes.

## Local API contract

All routes need the authenticated case owner and local mode.
AWS mode must reject these controlled actions.
Use the existing `ComparisonRequest` schema for comparison requests.

| Operation | Request or result |
|---|---|
| `POST /api/cases/{case_id}/assessments` | Existing schema. The simulated selection uses one policy version, `SIM-ACCESS`, and `SIM-ACCESS-1`. |
| `GET /api/cases/{case_id}/comparisons` | Return saved comparison records for this case only. |
| `POST /api/cases/{case_id}/comparisons` | The request must contain `older_version_id`, `newer_version_id`, `snapshot_id`, and `idempotency_key`. Return code `202`. |
| `GET /api/cases/{case_id}/comparisons/{comparison_id}` | Return the saved version pair, source passages, classification, affected controls, and optional new job ID. |

The version identifiers include the document ID, such as `SIM-ACCESS:v1`.
The older version must match the selected earlier snapshot.
The earlier assessment must be completed.
Reject unknown, identical, reversed, mixed-document, or unsupported version pairs.
Keep selected policy versions and obligation scope unchanged in the new snapshot.
Use the existing assessment source, job, trace, and human-review routes for the new assessment.

Repeated requests with the same key and content return the same comparison and new job.
Return `409` if that key has different content.
Keep recoverable assessment admission if comparison persistence fails.
Do not show a saved comparison before its record is committed.
Return `404` for another case owner's records.

## Acceptance checks

| ID | Necessary behavior |
|---|---|
| VS4-CT01 | A simulated baseline saves its exact source, obligation, control, and independent review. |
| VS4-CT02 | An added requirement saves both versions and starts one new snapshot with the affected control. |
| VS4-CT03 | Earlier findings, source copies, and reviews stay unchanged after comparison and new review. |
| VS4-CT04 | Wording and cosmetic changes do not start another assessment or show affected controls. |
| VS4-CT05 | Request retries and restart keep the same comparison and new job. Conflicting content returns `409`. |
| VS4-CT06 | Cross-owner comparison, source, assessment, and review access is denied. |
| VS4-CT07 | Invalid pairs, mismatched snapshots, and unfinished baselines cannot start a comparison. |
| VS4-CT08 | Current and AWS modes stay blocked for these controlled operations. |
| VS4-CT09 | A replacement policy cannot change either saved assessment or source copy. |
| VS4-CT10 | The new job keeps the existing call allowance, deadline, validated citations, and saved trace. |
| VS4-CT11 | An interrupted comparison save permits a retry without a second assessment. |
| VS4-CT12 | Simultaneous identical requests keep one comparison, one new assessment, and one controlled model call. |
| VS4-BT01 | Compare an added requirement, inspect both passages, open the new assessment, and save its independent review. |
| VS4-BT02 | Cosmetic and wording changes keep the earlier assessment and review visible. |
| VS4-BT03 | Reload restores saved comparisons and both assessment histories. |
| VS4-BT04 | Mobile and keyboard use keeps comparison and review controls accessible without horizontal overflow. |
| VS4-BT05 | Review saves stay disabled until the selected assessment completes loading. |

Save failing results before new application code.
Then save passing backend, browser, and build results.
Inspect desktop and mobile screenshots.
Request local VS4 feedback before merge and VS5 development.

## Isolation and release

Use `work/t5-agent` in `.worktrees/regulatory-agent-t5-agent`.
Use web port `5184`, feedback API port `8140`, and browser API port `8141`.
Keep browser records in `runs/private/slice-04/browser-tests.sqlite`.
Keep feedback records in `runs/private/slice-04/feedback.sqlite`.
Keep evidence in `runs/2026-10-11-slice-04-changes/`.
Do not change the earlier review databases or services.

AWS deployment needs account verification and failed-stack recovery.
Controlled local checks do not establish deployed acceptance, current coverage, or live model quality.
The complete project and remaining VS5 work stay incomplete.
