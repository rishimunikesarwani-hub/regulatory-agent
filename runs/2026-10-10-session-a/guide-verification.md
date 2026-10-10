# Session A verification

Date: 2026-10-10
Branch: `work/session-a`
Base commit: `20743635e68c57257432de655f6f02a669b956a8`

## Result

The requested source and fixture foundation is complete.
All 30 software tests pass.
The same tests pass from a clean temporary copy with credential variables removed.
The tests block network calls inside their process.

The package contains three development cases and 20 evaluation cases.
All 20 approved scenario IDs are present.
The evaluation answers contain seven supported, two partial, three gap, seven review, and one not-applicable result.
These counts describe expected answers, not model results.

The minimum labelled fixture is ready for the T2 dependency.
The full T1 ticket remains incomplete because provider and current-source verification are pending.

## Test evidence

| Record | Observed result |
| --- | --- |
| [Initial red run](red.txt) | Import failed before the validator existed. |
| [Behavior red run](red-behavior.txt) | Three new tests failed on unsupported element and mapping rules. |
| [Overlap red run](red-overlap.txt) | A new test failed before the record-overlap check existed. |
| [Green run](green.txt) | All 30 tests passed after implementation. |
| [Clean copy](clean-copy.txt) | All 30 tests passed without installed project dependencies. |
| [Inspection output](inspection.txt) | Three development cases display explicit benchmark-author answers. |
| [Machine receipt](verification.json) | Counts, runtime, isolation, and unchanged-file checks. |
| [Before hashes](before.json) | Baseline hashes for ten protected files. |
| [Freeze manifest](../../data/fixtures/freeze-manifest.json) | Hashes for all seven source and fixture files. |

Tests cover byte changes, exact quotations, locations, case ownership, selected versions, split separation, and required synthetic labels.
They also cover critical-case labels, effective dates, required answers, and rule mappings.
Input checks reject answer fields, including nested fields.
Those checks do not prove the absence of every possible semantic clue.

The fixture citation resolver is a test-data utility.
It does not establish application authorization or runtime isolation.
No application service uses it yet.

## Source review

The original HTML came from RBI's official website through HTTPS.
Nine selected passages match the saved source after documented whitespace normalization.
The source manifest records authority, URL, publication date, effective date, acquisition time, and content hash.

The source was selected as fixed historical evidence.
Current amendment coverage, withdrawal status, and provider freshness remain unverified.
Four additional versions are explicitly simulated.
Their dates and text do not describe RBI events.

Each case has one primary decision.
EVAL-06 fixes the expected answer as partial before model execution.
EVAL-13 assesses the newly added approval element and expects a gap.
EVAL-16 selects the earlier version before the simulated effective-date boundary.
Critical cases cannot expect supported.

Pre-release review corrected an approval date and separated operational records across the two sets.
It also moved assessment dates after the required completed reviews.
The package was frozen after these corrections.
No model or prompt was used to score or tune the cases.
Expected answers remain benchmark-author judgments without qualified regulatory expert review.

## Preserved boundaries

The five approved specifications and dependency manifest retain their original hashes.
The other protected files also retain their hashes.
No change was made in the integration or Session B worktrees.
No application feature, external retrieval adapter, model call, or AWS resource was created.
The private GitHub repository remains separate from a deployment.

The integration session must update shared status records after a reviewed merge.
This record supplies the completed work, test evidence, remaining limits, and next step.
Session B can begin T2 with the development fixture after integration.

A read-only comparison found different fixture-manifest, validator, and test copies in Session B.
Preserve that session's work during integration.
Reconcile its copies against this branch's final frozen hashes before running dependent checks.

## Language review

Applied the ASD-STE100 skill to the new Markdown files.
Checked sentence lengths, instructions, protected identifiers, links, and technical meaning.
Source quotations, commands, paths, JSON identifiers, and expected statuses are protected text.
The official dictionary download returned HTTP 403 during this session.
Full dictionary and approved-meaning compliance is not established.
See the mechanical checker records in this folder.
