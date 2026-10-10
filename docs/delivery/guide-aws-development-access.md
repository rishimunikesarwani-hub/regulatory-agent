# AWS development access

Date: 2026-10-10.
Status: Prepared for review. Not installed.

## Verified account state

The `rishicodex` profile authenticates as `rishicodex-aws` in account `482439369658`.
CloudFormation stack inspection and Lambda account inspection return access-denied responses.
The browser console can inspect the account and its IAM policies.
The Mumbai console shows no active application stacks.

The user approved AWS development deployment and a USD 25 monthly budget.
The budget alert is not configured.
Its recipient still needs selection.
The amount is an alert threshold, not a spending cap.

## Prepared access setup

The [account template](../../ops/aws-development-bootstrap.yaml) creates these resources.
The proposed stack name is `regulatory-agent-dev-access`.
The target region is `ap-south-1`.

| Resource | Permission boundary |
|---|---|
| GitHub identity provider | Supplies temporary credentials. An existing provider can be selected by ARN. |
| `regulatory-agent-dev-github` role | Trusts only `rishimunikesarwani-hub/regulatory-agent` and its `development` environment. |
| `regulatory-agent-dev-cloudformation` role | Creates and updates application resources. Cannot create or change IAM roles or policies. |
| `regulatory-agent-dev-case-runtime` role | Reads and writes development case records. Writes application logs in Mumbai. |
| Artifact bucket | Stores encrypted deployment packages. Blocks public access and unencrypted transport. Keeps versions. |

The GitHub role can deploy only `regulatory-agent-dev-s01`.
It can pass only the specified CloudFormation role.
CloudFormation can pass only the case function role to Lambda.
The application role has no model, document, or IAM permissions.

Some service permissions have a wider scope because resource identifiers are generated during creation.
API Gateway and Cognito management permissions cover the account in Mumbai.
CloudFront management permissions cover the account globally.
The reviewed application template uses those permissions for this development stack.
These permissions need confirmation before installation.

No administrator policy is included.
The setup does not change the existing user's policies or create access keys.
The setup does not deploy the application.
Application releases still use the single serialized GitHub workflow.

## Installation and release

1. Confirm the new role permissions before installation.
2. Inspect existing GitHub identity providers.
3. Select the existing provider ARN if one exists.
4. Review the account template in CloudFormation.
5. Create `regulatory-agent-dev-access` in Mumbai.
6. Verify its resources and outputs.
7. Restrict the GitHub `development` environment to `main`.
8. Set the workflow variables from the stack outputs.
9. Configure the USD 25 monthly alert with the selected recipient.
10. Run integration checks through the release workflow.
11. Deploy the reviewed application commit.
12. Configure the test operator through an authorized secure method.
13. Run the deployed browser checks.
14. Record the release URL, commit, results, and remaining limits.

| GitHub variable | Stack output or value |
|---|---|
| `AWS_DEV_ACCOUNT_ID` | `482439369658` |
| `AWS_DEV_DEPLOY_ROLE_ARN` | `DeploymentRoleArn` |
| `AWS_DEV_EXECUTION_ROLE_ARN` | `ExecutionRoleArn` |
| `AWS_DEV_RUNTIME_ROLE_ARN` | `RuntimeRoleArn` |
| `AWS_DEV_ARTIFACT_BUCKET` | `ArtifactBucketName` |
| `AWS_DEV_MONTHLY_BUDGET_USD` | `25` |
| `AWS_DEV_ENABLED` | Set `true` after setup verification. |

Keep operator credentials in the GitHub environment secrets.
Do not put credentials in chat or tracked files.
Keep public sign-up disabled.

## Validation limits

The templates pass `cfn-lint 1.57.2` without findings.
The Python checks reject missing, incorrect, and cross-account runtime roles.
The case role test excludes model, document, and IAM actions.
These checks do not prove live permission coverage.
CloudFormation account validation and deployed browser acceptance are pending.
The separate `cfn-guard` compliance check has not run.

## References

- [AWS role passing](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_passrole.html).
- [AWS GitHub identity setup](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc.html).
- [AWS Budgets](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html).
- [Slice contract](spec-slice-01-cases.md).
- [Decision D28](../decisions/gov-decision-log.md#d28---development-access-and-feedback-checkpoint).
