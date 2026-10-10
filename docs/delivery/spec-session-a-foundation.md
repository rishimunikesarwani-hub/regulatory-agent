# Session A foundation

Date: 2026-10-10
Scope: T1 source and fixture preparation.
User selection: Foundation only.

## Feature connection

This work prepares inputs for REQ-F01, regulatory knowledge ingestion.
It also prepares known assessment cases for REQ-F03 through REQ-F08.
It does not implement those product features.

The approved design uses retrieval-augmented generation, or RAG.
RAG supplies retrieved passages to a model that generates an output.
Keyword/BM25 search is the approved passage-selection method under D09.
BM25 ranks text by matching query terms and their frequency.
A vector database is not required by the approved design.

The external API retrieves regulatory sources and their current-version information.
Internal retrieval selects passages from the authorized case and fixed source versions.
The model then uses those passages to prepare an assessment.
This foundation supplies test inputs before those components are implemented.

## Inherited requirements

- Keep the external provider undecided under D20.
- Use real public sources or clearly labelled regulatory simulations.
- Label all fictional bank records.
- Keep source versions, locations, dates, and file hashes.
- Separate development examples from at least 20 held-out cases.
- Keep expected answers outside model-visible inputs.
- Distinguish missing evidence from demonstrated control failure.
- Record failing tests before the validator implementation.
- Do not contact external services during default tests.

## Implementation choices

These choices implement T1. They do not replace the T2 application contracts.

Use the 2023 RBI IT-governance document as a fixed historical source.
Save the original HTML response and selected exact passages.
An HTML citation uses its clause locator. Do not invent PDF page numbers.
The application upload formats remain unchanged.
HTML is the source-acquisition record, not a new bank-upload format.

Use JSON files for the fixture inputs and expected answers.
A fixture is fixed test data with a recorded purpose and expected result.
Use three development cases and 20 held-out cases.
Define one primary assessment decision per case.
Mark constructed regulatory changes as simulations in both input and answer files.

Keep the validator and inspection command under `ops/`.
Keep their tests under `tests/`.
Use the Python standard library. Do not add application dependencies.
Keep the fixture format separate from Session B's executable API schemas.

## Acceptance tests

| ID | Required result | Requirement |
| --- | --- | --- |
| A-01 | The complete fixture package passes validation. | T1, REQ-X03 |
| A-02 | Changed source or fixture bytes fail the frozen hash check. | REQ-X03 |
| A-03 | Every allowed citation resolves to its selected version and exact passage. | REQ-F01, REQ-X03 |
| A-04 | Development and held-out IDs are separate. Operational records cannot be reused across these sets. | T1, REQ-X06 |
| A-05 | Answer fields are absent from model-visible inputs. Manual review checks answer separation. | T1, REQ-X06 |
| A-06 | All fictional bank records and simulated rules have explicit labels. | REQ-F01, REQ-X05 |
| A-07 | Exactly 20 held-out cases cover the approved scenario IDs. | T1, EVAL-01 through EVAL-20 |
| A-08 | Each expected status has a reason and source references. | REQ-F03 through REQ-F08 |
| A-09 | Critical missing, conflicting, and adversarial cases cannot expect supported. | REQ-F06, REQ-F07 |
| A-10 | The inspector permits development cases only. | T1, REQ-X06 |
| A-11 | Source acquisition cannot establish current regulatory coverage. | REQ-F01, D20 |
| A-12 | Case/version access excludes another case's records. | REQ-X02, REQ-X03 |

Run tests with network access blocked inside the test process.
Also verify the package from a clean source copy.
These checks validate fixtures. They do not measure model assessment quality.

## Source limits

The source was retrieved from RBI's official website.
Its published version is dated 2023-11-07 and states commencement on 2024-04-01.
The assessment cases use fixed historical periods.
Current amendment coverage, withdrawal status, and provider synchronization remain unverified.
Do not mark this source current for a new live assessment.

The constructed change cases do not represent actual RBI amendments.
The expected answers are benchmark-author judgments.
No qualified regulatory expert has reviewed them.
T1 remains incomplete until the provider and current-source requirements are verified.

## Handoff

Session B can use the minimum labelled fixture to develop T2 contracts.
Keep the input and answer files separate during model calls.
Do not use held-out cases to tune prompts.
T3, T4, cloud integration, and live model evaluation remain later work.

## References

- [Feature tickets](05_FEATURE_TICKETS.md).
- [Technical blueprint](../architecture/02_TECHNICAL_BLUEPRINT.md#3-agent-and-retrieval-rules).
- [AI quality plan](../testing/eval-model-quality.md).
- [RBI source](https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=12562).
- [RAG research paper](https://arxiv.org/abs/2005.11401).
