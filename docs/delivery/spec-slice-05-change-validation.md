# VS5 regulatory change validation

Date: 2026-10-11.
Authorization: D42 permits VS5 development within REQ-F02 and the approved architecture.
Tickets: T3, T5, and T6.

## Component and limits

This component prepares a specified regulatory version pair for model interpretation.
It validates the interpretation before the application can use its changed obligations and affected controls.
Use the existing strict contracts and source citations.
Add no dependency.

Do not extend the VS4 fixed classifications to real regulatory versions.
Text differences cannot establish changed requirements.
Structural validation cannot establish correct interpretation.
Live evaluation and source verification remain mandatory.

The complete comparison flow still needs durable admission, model processing, native routes, and browser acceptance.
It must start a new assessment snapshot when an applicable requirement changes.
Earlier sources, findings, and human reviews must stay unchanged.
This component cannot establish complete REQ-F02 acceptance.

## Version pair and context

Use the baseline snapshot's case and selected older regulatory version.
Require two different versions of the same regulatory document.
Use the specified newer version independently of the current catalog.
Do not select the latest version automatically.
Reject reversed publication dates, contradictory metadata, and sources from another case.

Make sure that both original byte sequences match their saved hashes.
Require RBI authority labels and permitted public authority URLs.
Keep publication dates and effective dates independent.
Keep future requirements visible without applying them to an earlier assessment date.

Use at most 20 source passages and 64,000 context bytes.
Reject excessive context instead of truncating source text.
Keep passage identifiers, locations, and unchanged text.
Reject duplicate identifiers and passages assigned to the wrong version.
Keep the selected obligation scope unchanged.

Record metadata changes independently of requirement classifications.
Missing withdrawal or amendment metadata stays unknown.
Do not treat stored historical sources as proof of current coverage.

## Interpretation contract

Require the baseline snapshot ID and both specified document version IDs.
Require one result for each selected obligation.
Reject omitted, repeated, or additional obligations.
Use classifications for added, changed, withdrawn, unchanged, wording-only, appearance-only, or undetermined requirements.

Keep the before and after requirements, conditions, exceptions, applicability, and citations in the result.
Added requirements have no before requirement.
Withdrawn requirements have no after requirement.
Other classifications need both requirements.
Undetermined results can keep missing interpretations without claiming affected controls.

Resolve every citation against its specified version, passage, location, and quoted text.
Require source references from both versions for every result.
A withdrawal needs references to the newer source.
Absence from an excerpt alone cannot establish withdrawal.
Semantic support for each interpretation remains an evaluation condition.

Permit affected controls only from the baseline mapping for that obligation.
Do not invent a new mapping during comparison.
Do not copy human review outcomes into a new result.
Unchanged, wording-only, appearance-only, and undetermined results cannot claim affected controls.
Wording-only and appearance-only results must keep conditions, exceptions, and applicability unchanged.

Unchanged results must keep the requirement statement unchanged after whitespace normalization.
Use the shared assessment citation validation for comparison references.
Reject quotes that contain only whitespace in assessment, comparison, and export validation.

Identify unresolved interpretations and metadata changes as reasons for selection review.
Do not apply a future effective version automatically.
Do not start assessment processing from this validation component.

## Acceptance checks

| Check | Required behavior |
|---|---|
| VS5-VC01 | Specified originals, versions, selected scope, and independent dates appear in the prepared context. |
| VS5-VC02 | Changed obligations keep both cited interpretations and only their baseline control mappings. |
| VS5-VC03 | Wrong case, source, older selection, same version, and reversed publication dates fail. |
| VS5-VC04 | Changed original bytes, contradictory metadata, and invalid authority URLs fail. |
| VS5-VC05 | Duplicate passage identifiers, wrong versions, excessive passages, and excessive bytes fail without truncation. |
| VS5-VC06 | Forged snapshot or pair identifiers and omitted, repeated, or additional obligations fail. |
| VS5-VC07 | Wrong-side, missing, invented, blank, or altered citations fail. |
| VS5-VC08 | Invented controls and controls mapped only to another obligation fail. Unchanged results cannot claim affected controls. |
| VS5-VC09 | Before and after requirements follow classification rules. Changed exceptions cannot become wording-only changes. |
| VS5-VC10 | Future effective dates do not cause an assessment for the earlier date. Metadata changes still need selection review. |
| VS5-VC11 | Explicit withdrawal results keep newer citations. Missing metadata and undetermined interpretations stay unknown. |
| VS5-VC12 | Preparation and validation cannot change input sources, snapshots, findings, or human reviews. |
| VS5-VC13 | Unchanged, wording-only, appearance-only, and added classifications keep their specified before and after structures. |
| VS5-VC14 | Shared assessment citation validation rejects quotes that contain only whitespace. |
| VS5-VC15 | An unchanged classification cannot hide a different requirement statement. |
| VS5-VC16 | Export validation rejects whitespace-only quotes in previously saved findings. |

Write failing checks before application code.
Use controlled source text and model responses without credentials or external traffic.
Keep comparison integration and live semantic acceptance pending.

## Language review

Use the project glossary and a different language review receipt.
Vocabulary review remains incomplete.
Sentence checks alone cannot establish full ASD-STE100 compliance.
