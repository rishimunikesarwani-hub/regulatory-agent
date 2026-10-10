# VS3 integration candidate

Date: 2026-10-11.
Status: Preparation within authorized VS3 development. User acceptance is pending.

An integration candidate is a Git branch for checks of combined application changes before acceptance.
It is not the accepted `main` version.
Use this contract with [the VS3 contract](spec-slice-03-assessment.md).
Keep the approved feature scope and assessment limits unchanged.

## Worktree and data

Use branch `work/t4-integration-candidate` in `.worktrees/regulatory-agent-t4-integration`.
Reserve web port `5193`, feedback API port `8192`, and test API port `8193`.
Keep test records in `runs/private/slice-03-integration/browser-tests.sqlite`.
Keep the VS3 review worktree, feedback database, and running services unchanged.
Do not merge this candidate into `main` before VS3 acceptance.
Do not start VS4 or deploy AWS resources from this candidate.

## Combined behavior

Include the accepted VS2 cloud document changes and keyboard focus correction from `main`.
Keep the controlled historical assessment and saved review functions from VS3.
Show cloud document actions in AWS mode.
Keep the controlled assessment in local mode only.
Do not imply cloud assessment availability from successful cloud document checks.
Keep current assessments blocked when freshness verification is unavailable.

## Checks

| ID | Necessary behavior |
|---|---|
| VS3-INT01 | VS1-BT04 must show unchanged keyboard focus after the delayed case list loads. |
| VS3-INT02 | All backend checks from VS1, VS2, VS2 AWS, and VS3 must return code `0`. |
| VS3-INT03 | All four browser suites must return code `0` through one isolated test configuration. |
| VS3-INT04 | The combined TypeScript build must return code `0`. |
| VS3-INT05 | Keep each earlier evidence record and acceptance state unchanged. |

First, do the delayed-load check on the existing VS3 branch source.
Save its expected failure.
Then merge the accepted `main` changes into the candidate.
Correct merge conflicts.
Use the earlier failing tests for unchanged feature behavior.
Save different failing and passing records for this integration check.

## Remaining conditions

These checks do not establish live model quality or deployed AWS acceptance.
The user review remains pending.
CloudFront account verification remains necessary before deployment.
The selected Bedrock profile remains `in.openai.gpt-5.6-luna`.
Model metadata alone does not prove runtime permissions or successful inference.
