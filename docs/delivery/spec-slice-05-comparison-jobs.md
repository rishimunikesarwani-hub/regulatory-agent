# VS5 saved comparison processing

Date: 2026-10-11.
Authorization: D42 permits development under REQ-F02.
Tickets: T3, T5, and T6.
Related contract: [Specified version validation](spec-slice-05-change-validation.md).

A comparison job saves its input snapshot before model processing.
The job compares selected obligations from two specified versions of one regulatory document.
Its source references, control mappings, and baseline findings stay unchanged.
An earlier human decision cannot become a new AI result.

Require a completed historical assessment with fictional bank data and the selected VS5 model configuration.
Require saved original sources and a baseline finding for each compared obligation.
Use only obligations assigned to the older regulatory source in the baseline selection.
Reject missing control statements or invalid control citations.
Use the existing case ownership checks, execution claims, deadline, and call allowance.

Save a different model protocol for comparison jobs.
Select that protocol from the saved snapshot.
Do not select the protocol from model text or a request flag.
Keep the existing assessment model protocol unchanged.

Process one selected obligation in each model call.
Include both regulatory versions and the original mapped control statements in the context.
Keep the existing limits of 20 passages and 64,000 text bytes.
Reject excessive context without truncation.
Reject citations outside the examined context.

Save each validated result with its selected obligation ID.
Skip saved results after an interrupted execution.
Keep the original deadline and consumed call allowance after a new execution claim.
Keep uncertain calls visible in the stage trace.
Return partial results without presenting unchecked obligations as completed.

Keep comparison jobs separate from assessment lists and reviewer measurements.
Require a completed, applicable change before admitting a new assessment.
Reject a new assessment when an interpretation remains unresolved.
Keep the baseline bank versions, assessment date, and complete obligation selection in the new snapshot.
Use the specified newer regulatory version.
Give the new assessment its own finding and review records.

## Acceptance checks

| Check | Required behavior |
|---|---|
| VS5-CJ01 | Admission saves the specified pair and a different job with an unchanged baseline. |
| VS5-CJ02 | A repeated request returns the same job. Changed requests with the same key fail. |
| VS5-CJ03 | Case ownership, completed baseline, historical mode, and fictional processing checks apply before admission. |
| VS5-CJ04 | Processing saves cited changes, original control mappings, numeric usage, and separate trace records. |
| VS5-CJ05 | Invalid replies consume their call allowance and leave their obligations unchecked. |
| VS5-CJ06 | An interrupted execution keeps saved results and consumed calls. |
| VS5-CJ07 | Applicable changes admit one new assessment with independent records and pinned versions. |
| VS5-CJ08 | Future, unchanged, unresolved, and unfinished comparisons cannot admit a new assessment. |
| VS5-CJ09 | The saved snapshot selects the strict comparison protocol. Ordinary assessments retain their protocol. |
| VS5-CJ10 | Uncertain storage acknowledgments cannot produce a second admission. |
| VS5-CJ11 | Original source changes and missing baseline control support fail before model processing. |
| VS5-CJ12 | Native SDK processing uses the comparison schema from the saved snapshot. |
| VS5-CJ13 | The native worker selects comparison processing from the saved snapshot. |

Native routes, browser acceptance, provider approval, source verification, and live evaluation remain pending.
Controlled checks cannot establish complete REQ-F02 acceptance or correct model interpretation.
The language review uses Issue 9. Dictionary review remains incomplete.
