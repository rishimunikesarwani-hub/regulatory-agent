# VS3 integration review record

Date: 2026-10-11.
Status: Local integration checks completed. User acceptance and AWS acceptance are pending.

## Sources and isolation

The candidate branch is `work/t4-integration-candidate`.
The source VS3 commit is `3a2ad9b5ee724df88121ca2ce0b5bcad62d6173e`.
The accepted `main` source is `a38654b7e2d8c1c98a64a0b6b1d22398cc460950`.
The specification and behavior test commit is `baeee72`.

The candidate uses web port `5193`, test API port `8193`, and its own ignored database.
The VS3 review worktree and its feedback services stayed unchanged.
No merge into `main`, VS4 start, or deployment occurred.

## Failure evidence

The existing VS1-BT04 test failed against the earlier VS3 source.
The delayed case list moved keyboard focus from the fictional-data checkbox.
The [failure record](focus-red.txt) and `focus-red-artifacts/` keep that result.
The candidate now includes the accepted focus correction from `main`.

The first combined browser attempt stopped after a cloud authentication fixture failure.
The fixture used the earlier port in its redirect URL.
The application correctly rejected that different origin.
The [partial record](browser-red-v1.txt) is not a completed suite result.
The `browser-red-v1-artifacts/` directory keeps the failure details.

The fixtures now use the selected test configuration for expected API and redirect addresses.
Their checks still reject a configuration that points at a different worktree.
The assessment screenshots now use the selected evidence directory.

## Combined results

| Check | Result | Evidence |
|---|---|---|
| VS3-INT01 | VS1-BT04 completed without failure. | [Browser result](browser-green.txt). |
| VS3-INT02 | 215 backend tests completed without failure. | [Backend result](python-green.txt). |
| VS3-INT03 | 33 browser tests completed without failure. | [Browser result](browser-green.txt). |
| VS3-INT04 | The interface build and final TypeScript checks returned code `0`. | [Build](frontend-build.txt). [TypeScript](typescript-final.txt). |
| VS3-INT05 | Earlier evidence and acceptance records stayed unchanged. | Git comparison with the two source commits. |

The browser suites cover cases, local documents, controlled AWS documents, and controlled assessments.
The cloud document fixtures also show no controlled assessment action in AWS mode.
The combined interface keeps source inspection, original downloads, and saved human reviews.
Desktop and mobile screenshots show the fictional assessment and review controls.
The source snapshots, controlled labels, and current-assessment block stay unchanged.

## AWS metadata

Read the [metadata record](aws-metadata.json) for the read-only AWS results.
The approved profile is active and lists only Mumbai and Hyderabad model destinations.
The failed application stack still has status `ROLLBACK_COMPLETE`.
These checks made no model invocation and changed no cloud resources.
Runtime permissions, invocation logging, and model quality are unverified.

The Python login credential provider could not load without its optional CRT dependency.
The AWS CLI completed the metadata checks without a dependency change.
This limitation does not establish an application runtime failure.

## Remaining work

VS3 user review is still pending at `http://127.0.0.1:5183/`.
Draft PR9 and its original review branch are unchanged.
Do not merge VS3 into `main` or start VS4 before the user decision.
CloudFront account verification and failed-stack recovery remain necessary before deployment.
Real model connections, current regulatory retrieval, and full project acceptance are not established by these checks.

## Language review

The review used the project's ASD-STE100 Issue 9 reference and selected dictionary entries.
The changes keep requirement IDs, source commits, ports, test results, and approval conditions unchanged.
The manual meaning review kept local checks different from live AWS and model evidence.
Git branch, worktree, integration, fixture, and model terms use the meanings in the project glossary.
Dictionary and grammatical-role review is incomplete for all remaining prose.
Mechanical results do not establish full ASD-STE100 compliance.
