# Selected-scope pipeline review

Date: 2026-10-11.
Contract: [Selected-scope pipeline](../../docs/delivery/spec-slice-05-pipeline.md).
Scope: Admitted historical processing, claims, retrieval, audit records, presentation, and exports.

The pipeline uses the existing case, document, snapshot, job, model, and review services.
It verifies original bank documents before inference.
It requires saved regulatory scope maps.
It preserves unknown owners, frequencies, periods, usage, and costs.
It records selected passages without operational log text.
Known processing failures end their audit records.
Interrupted processing keeps an explicit unknown or interrupted record.

## Behavior evidence

| Record | Result |
|---|---|
| `pipeline-red.txt` | Nine checks failed because the implementation was absent. |
| `pipeline-first.txt` | Shared reads assumed the earlier fixed example. Resumed audit parsing used the wrong input mode. |
| `pipeline-second.txt` | All nine initial checks passed. |
| `pipeline-boundaries-red.txt` | Four additional checks exposed context allocation, late writes, processing labels, and nested citations. |
| `pipeline-terminal-red.txt` | A known extraction failure left an unknown audit record. |
| `pipeline-green.txt` | All fourteen pipeline checks passed. |
| `backend-pipeline-final.txt` | All 260 backend checks passed before the SDK dependency addition. |
| `backend-pipeline-crt-final.txt` | All 260 checks passed with the final locked SDK dependency. |
| `sdk-login-red.txt` | Client construction needed the official SDK extra. |
| `sdk-login-dependency-green.txt` | Client construction passed after adding the required dependency. |
| `pipeline-public-boundary-red.txt` | The original guard also rejected real public regulations. |
| `backend-pipeline-public-final.txt` | All 261 checks passed after separating public regulations from private bank input. |

Public regulatory records can use an allowed RBI URL without a fictional-data flag.
Private bank input remains blocked.
This URL check does not establish content authenticity, coverage, or freshness.

Native SDK login support needs `awscrt==0.36.0`.
The dependency change preserves all 26 earlier locked versions.
The CLI and live SDK profile check still require renewed authentication.
No inference was dispatched during these read-only checks.

## Remaining conditions

The current interface still uses the earlier controlled example.
General API admission and source-selection integration remain necessary.
Source provider selection and current verification remain pending under D20.
The synchronous pipeline checks deadlines before and after processing.
The independent process supervisor remains necessary for a hard wall-clock limit.
Private processing remains disabled pending its separate checks.
Native provider stubs do not establish live authentication or model quality.
Human held-out evaluation must check contextual support, conflicts, applicability, and every approved quality gate.
CloudFront verification still blocks deployment.
VS5 remains a draft under D35.

## Language and meaning review

Reference: ASD-STE100 Issue 9 and the project glossary.
Protected content includes identifiers, paths, quantities, permissions, prohibitions, and evidence states.
The manual review checked ownership, selected scope, unknown values, deadlines, and controlled-versus-live labels.
No quality gate or release condition changed.
The complete dictionary meaning review remains incomplete.
Mechanical results appear in separate checker reports.
This receipt does not claim full ASD-STE100 compliance.
