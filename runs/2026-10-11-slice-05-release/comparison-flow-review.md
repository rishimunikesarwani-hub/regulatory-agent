# Comparison flow review

Date: 2026-10-11.
Scope: D56 and [VS5-CF01 through VS5-CF12](../../docs/delivery/spec-slice-05-comparison-flow.md).
This record describes controlled software checks.
It does not establish live regulatory interpretation or deployed acceptance.

## Behavior checks

The corrected initial API suite ran nine checks with eight failures and one error.
All four initial browser checks failed because the comparison control did not exist.
Later failing checks exposed an internal storage reference, mixed legacy comparison records, and an incorrect returned comparison ID.
The corrections use shared metadata selection, separate record modes, and a specified record ID check.

Two intermediate browser failures came from test assertions and reload authentication setup.
The corrected test checks independent review records and signs in again after reload.
The first API check incorrectly matched numeric token field names as execution tokens.
The corrected assertion checks the exact private JSON field.
The initial API syntax error remains in its separate evidence file.

| Check | Result |
|---|---|
| Focused API checks | 11 passed in 5.791 seconds. |
| Complete local backend | 403 passed in 186.977 seconds. |
| Complete local browser | 59 passed in 2.2 minutes. |
| TypeScript and production build | Passed. |
| Desktop and mobile screenshots | Readable controls, sources, and result sections. |
| Mobile keyboard flow | Passed with no horizontal overflow. |
| External provider and model traffic | None in these checks. |

The API checks use SDK parameter validation and controlled storage and queue clients.
Browser checks use controlled HTTP responses and fictional case records.
Test regulatory changes are explicitly labeled controlled text.
They do not become real source versions in the application source set.

## Code review

Authentication and case ownership precede native comparison service construction.
The disabled assessment flag remains false.
The six routes use existing resources and permissions.
The local and native adapters use one comparison response function.
No dependency was added.

Selection keeps baseline versions, dates, and obligation scope.
Public source metadata excludes storage references.
Uncertain admission keeps its request key and saved job.
Reassessment requires explicit selection review and separate human reviews.
Legacy simulation records remain separate from native comparison records.

## Language and meaning review

Reference: Official ASD-STE100 Issue 9, dated 2025-01-15.
Reviewed files: The comparison flow contract, D56, changed specification sections, glossary additions, LOG entry, and this receipt.
Protected items include API paths, identifiers, check counts, dates, authorization, and prohibitions.
Previous decision records and approval history remain unchanged.

The manual review checked actors, conditions, negative requirements, processing order, and technical limits.
The glossary defines model protocol, execution claim, and selection review.
Selection review does not approve AI findings or establish actual control operation.
The text checker provides sentence-length and punctuation evidence.
Complete vocabulary and approved-meaning review remains incomplete.
No full compliance or ASD approval is claimed.

## Remaining conditions

The source set contains one verified historical regulatory version.
Current coverage remains unverified.
Provider approval, live semantic evaluation, template validation, AWS authentication, CloudFront verification, and deployed acceptance remain pending.
VS5 remains a draft under D35.
