# AWS development access

Date: 2026-10-10.
Status: Development access installed. Application deployment is pending.

## Verified account state

The `rishicodex` profile authenticates as `rishicodex-aws` in account `482439369658`.
CloudFormation stack inspection and Lambda account inspection return access-denied responses.
The browser console can inspect the account and its IAM policies.
The initial Mumbai console inspection showed no active application stacks.
The user completed temporary AWS authentication with profile `et-hackathon-admin`.
Stack `regulatory-agent-dev-access` reached `CREATE_COMPLETE`.

The user approved AWS development deployment and a USD 25 monthly budget.
The monthly budget alert is configured.
Actual cost alerts use 80% and 100% thresholds.
The forecast alert uses a 100% threshold.
The account owner's verified email receives these alerts.
The amount is an alert threshold, not a spending cap.

## Prepared access setup

The [account template](../../ops/aws-development-bootstrap.yaml) creates these resources.
The installed stack name is `regulatory-agent-dev-access`.
The target region is `ap-south-1`.

| Resource | Permission boundary |
|---|---|
| GitHub identity provider | Supplies temporary credentials. An existing provider can be selected by ARN. |
| `regulatory-agent-dev-github` role | Trusts only `rishimunikesarwani-hub/regulatory-agent` and its `development` environment. |
| `regulatory-agent-dev-cloudformation` role | Creates and updates application resources. Cannot create or change IAM roles or policies. |
| `regulatory-agent-dev-case-runtime` role | Reads and writes development case records. Writes application logs in Mumbai. |
| Artifact bucket | Stores encrypted deployment packages. Blocks public access and unencrypted transport. Keeps versions. |

The GitHub role can deploy only `regulatory-agent-dev-s01`.
Its trust condition includes verified owner ID `292392448` and repository ID `1412648942`.
The required subject is `repo:rishimunikesarwani-hub@292392448/regulatory-agent@1412648942:environment:development`.
The development environment permits deployments from `main` only.

It can pass only the specified CloudFormation role.
CloudFormation can pass only the case function role to Lambda.
CloudFormation can use the AWS SAM transform to convert the application template.
That permission covers only `arn:aws:cloudformation:ap-south-1:aws:transform/Serverless-2016-10-31`.
The application role has no model, document, or IAM permissions.

Some service permissions have a wider scope because resource identifiers are generated during creation.
API Gateway and Cognito management permissions cover the account in Mumbai.
CloudFront management permissions cover the account globally.
The reviewed application template uses those permissions for this development stack.
The user requested this development deployment and completed its AWS authentication.
The reviewed setup was installed through the authenticated local AWS session.

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

The first application release stopped because the execution role lacked the SAM transform permission.
Decision D32 records the narrow correction.
Application resource creation and deployed browser acceptance remain pending.

Ten selected AWS Guard rules ran with `cfn-guard 3.2.1`.
All applicable rules passed after the secure-transport value used Boolean `false`.
The S3 transport restriction stays unchanged.
These selected rules do not establish general security compliance.
The rule source commit is `7f7340c26ae5d5e8874651dbffeb12e0e9f505b6`.

CloudFormation reported no pre-deployment validation errors for the installed setup.
CloudTrail event history contains the CloudFormation plan operation.
No durable CloudTrail trail is configured.
Audit retention is therefore limited to the default event history.

## References

- [AWS role passing](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_passrole.html).
- [AWS GitHub identity setup](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc.html).
- [AWS Budgets](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html).
- [Slice contract](spec-slice-01-cases.md).
- [Decision D28](../decisions/gov-decision-log.md#d28---development-access-and-feedback-checkpoint).
