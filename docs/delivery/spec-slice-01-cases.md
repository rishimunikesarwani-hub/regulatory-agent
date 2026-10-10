# Slice 01: sign in and save a case

Date: 2026-10-10.
Decision: D27.
Contract version: `slice-01-v1`.

The user selected delivery through complete user flows.
This slice starts with sign-in and ends with a saved case that the operator can reopen.
It establishes the authenticated case scope for all eight MVP features.
It does not complete a regulatory assessment feature.

## Shared API contract

An API contract defines the permitted request and response data.
Frontend and backend work must use this contract before implementation starts.
The executable types are in [contracts.py](../../src/regulatory_agent/contracts.py).
The saved schemas are in [slice-01-api.json](../../data/contracts/slice-01-api.json).

| Operation | Request | Successful response |
|---|---|---|
| `POST /api/cases` | `CaseCreate` | `201`, `CaseRecord` |
| `GET /api/cases` | No request body | `200`, `CaseList` |
| `GET /api/cases/{case_id}` | Case ID in the path | `200`, `CaseRecord` |
| `GET /api/health` | No request body | `200`, public service status and commit ID only |

`CaseCreate` contains `bank_profile` and `synthetic`.
`bank_profile.name` must contain 1 to 200 characters after removal of outer whitespace.
Other profile values use the existing string, Boolean, or null contract.
The server supplies `case_id`, `owner_id`, and the UTC `created_at` value.
The first slice accepts fictional cases only.
It rejects `synthetic: false` until the private-data checks pass.

`CaseList` contains a `cases` array.
The server restricts this array to the authenticated owner.
The server saves each case before it sends a successful response.
A fresh process must be able to read that case.

Errors use `SafeError`: `code`, `message`, `next_action`, and `correlation_id`.

Use `401` for absent or invalid authentication.
Use `404` for an absent case or a case owned by another operator.
Use `422` for an invalid request.
Use `503` when persistence fails.
Do not return private exception text.
Send `Cache-Control: no-store` for private API responses.

The current create request has no retry key.
The interface must prevent duplicate clicks while a save is pending.
After an uncertain save, show the case list before another create request.
Do not claim exactly-once creation after a network failure.

## Authentication and deployment

Use Cognito authorization-code sign-in with PKCE and the `S256` method.
Keep access tokens in browser memory.
Keep only the temporary state and verifier in session storage during sign-in.
Remove them after the code exchange.

Keep the selected case ID in the temporary state value during sign-in.
Keep the random part of that value at 32 bytes.
Validate the returned state before restoring the case ID.
Permit only valid case IDs, not external URLs or arbitrary paths.
Keep the existing owner check when the application reopens the case.

Disable public sign-up.

The AWS API uses a JWT authorizer with the configured user pool and client ID.
The Lambda handler gets the owner from the authorizer claims.
It rejects missing claims and ID tokens.
It does not accept a caller-supplied owner.

Local development uses the configured development identity on loopback only.
Label that mode `Local development`.
It is not evidence of Cognito sign-in.
Do not enable this identity in AWS.

Save case records in DynamoDB in `ap-south-1`.
Serve public React assets through S3 and CloudFront.
Use the private API directly for case data.
Do not put case data in public assets or the CloudFront cache.

Use one GitHub Actions workflow for AWS development deployment.
Use one concurrency group with `cancel-in-progress: false`.
Do integration checks before deployment.
Do browser checks after deployment.
Use short-lived AWS credentials through GitHub OIDC.
Do not store AWS access keys in GitHub.

The account setup defines the case function role before application deployment.
The deployment configuration must select `regulatory-agent-dev-case-runtime` in the expected account.
CloudFormation can pass this role to Lambda but cannot change its permissions.
The role permits case records and application logs only.
See [D28](../decisions/gov-decision-log.md#d28---development-access-and-feedback-checkpoint).

## Acceptance tests

Write each failing test before its implementation.

| Test ID | Required result |
|---|---|
| VS1-CT01 | An authenticated operator can create, list, and read a case through the shared schemas. |
| VS1-CT02 | A restarted service can reopen the saved case. |
| VS1-CT03 | Missing authentication, forged owners, and another operator's case are denied. |
| VS1-CT04 | Invalid profiles, real-data requests, and failed saves cannot produce a success response. |
| VS1-BT01 | The operator can sign in, create a fictional case, leave its detail view, and reopen it. |
| VS1-BT02 | Loading, empty, failed-save, expired-session, and access-denied states give a usable next action. |
| VS1-BT03 | Keyboard navigation and a narrow viewport permit the same case flow. |
| VS1-AWS01 | The deployed flow uses Cognito and DynamoDB in Mumbai. Local identity is unavailable. |
| VS1-REL01 | The release record contains its URL, exact commit, test results, and limits. |

Local browser checks can use controlled authentication.
They cannot replace the deployed Cognito check.
A release stays unverified when a mandatory deployed check has no result.

## Ownership

The integration owner controls this contract, shared Python schemas, dependency locks, and the deployment workflow.
The slice owner is responsible for the complete flow and its release record.
Frontend and backend helpers can work concurrently after the contract is saved.
Each helper must edit only its assigned files in the selected worktree.

## Setup still needed

The AWS account and `rishicodex` CLI profile were confirmed on 2026-10-10.
The profile lacks CloudFormation and Lambda inspection permissions.
The repository contains the development workflow but has no configured deployment variables or operator secrets.
The [access guide](guide-aws-development-access.md) records the proposed account setup.

Before deployment, confirm the development account, GitHub deployment role, and CloudFormation execution role.
Configure the approved USD 25 monthly alert and the Cognito test operator.
Use AWS or GitHub secure input for credentials.
Do not put them in chat.

The first slice does not need the regulatory retrieval provider or a model call.
Private documents stay disabled.
Production deployment needs different, explicit authorization.

## Technical references

- [Cognito authorization and PKCE](https://docs.aws.amazon.com/cognito/latest/developerguide/authorization-endpoint.html).
- [AWS SAM JWT authorizer](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-controlling-access-to-apis-oauth2-authorizer.html).
- [GitHub OIDC for AWS](https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-aws).

These references describe service behavior.
They do not prove that this project has a working AWS deployment.
