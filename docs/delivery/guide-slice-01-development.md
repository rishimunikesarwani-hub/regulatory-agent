# Prepare and operate slice 01

Date: 2026-10-10.
Flow: Sign in, make a fictional case, save it, and reopen it.

This slice establishes the case and identity boundary for all eight MVP features.
It does not assess a regulation or accept private documents.
The [API contract](spec-slice-01-cases.md) gives the required behavior.

## Local setup

Use the selected worktree.

```powershell
cd 'C:\Users\Be Flith Rich\My Project Folder\ET-Hackathon\.worktrees\regulatory-agent-autonomous-build'
powershell -NoProfile -ExecutionPolicy Bypass -File ops/setup.ps1
npm --prefix src/web ci --ignore-scripts
npm --prefix src/web run build
```

The setup command can download dependencies.
The default Python checks block external network traffic.
The package locks identify the installed dependency versions.

Start the local API in one terminal.

```powershell
$env:APP_ENV = 'local'
$env:DEVELOPMENT_USER = 'local-operator'
$env:CASES_DB_PATH = 'runs/private/slice01-cases.sqlite'
.venv/Scripts/python.exe -m uvicorn regulatory_agent.api:app --app-dir src --host 127.0.0.1 --port 8110 --no-proxy-headers
```

Start the interface in another terminal.

```powershell
npm --prefix src/web run dev
```

Open `http://127.0.0.1:5173`.
Select the local development sign-in action.
Make a fictional case.
Return to the case list.
Reopen the case.

The local identity is a development substitute for Cognito.
It does not prove that AWS sign-in works.
The SQLite file contains the saved local cases.
Do not share that writable file between worktrees.

## Local checks

Keep the API available on port `8110` for browser checks.
Let Playwright start the test interface on port `5173`.
Stop a manually started interface before these checks.

```powershell
.venv/Scripts/python.exe -X utf8 ops/check.py
npm --prefix src/web test
```

Playwright is the browser test tool.
Install its Chromium browser if the browser is unavailable.

```powershell
cd src/web
npx playwright install chromium
```

The tests use fictional cases.
Cloud adapter tests use controlled responses.
They do not establish a working AWS deployment.

## AWS setup that is still needed

The user must set up an AWS account.
No deployment has occurred.
The account number, access method, roles, and spending limit are not confirmed.

1. Make the AWS development account.
2. Enable multi-factor authentication for its root identity.
3. Set up an administrative role through IAM Identity Center or another approved temporary-access method.
4. Select Mumbai, `ap-south-1`, for private application resources.
5. Set a development spending limit and a budget alert.
6. Review [sam-dev.yaml](../../ops/sam-dev.yaml) before the first deployment.
7. Make the deployment artifact bucket in Mumbai with encryption and public access blocked.
8. Configure GitHub OIDC trust for this repository and its `development` environment.
9. Make the deployment role and the CloudFormation execution role with reviewed permissions.
10. Configure the GitHub environment values below.

OIDC supplies temporary AWS credentials to GitHub Actions.
The trust policy must match this repository's actual subject claim.
Use the exact repository and environment identity.
Do not use an unrestricted repository wildcard.

| GitHub value | Purpose |
|---|---|
| Variable `AWS_DEV_ENABLED` | Set `true` only after the development setup has approval. |
| Variable `AWS_DEV_ACCOUNT_ID` | Expected development account number. |
| Variable `AWS_DEV_DEPLOY_ROLE_ARN` | Role that the workflow can assume through OIDC. |
| Variable `AWS_DEV_EXECUTION_ROLE_ARN` | Role that CloudFormation uses for the reviewed resources. |
| Variable `AWS_DEV_RUNTIME_ROLE_ARN` | Fixed case function role from the account setup. |
| Variable `AWS_DEV_ARTIFACT_BUCKET` | Private Mumbai bucket for application deployment files. |
| Variable `AWS_DEV_MONTHLY_BUDGET_USD` | Approved positive monthly budget amount. |
| Secret `COGNITO_TEST_USERNAME` | Username of the fictional-case test operator. |
| Secret `COGNITO_TEST_PASSWORD` | Password supplied through GitHub's secure secret interface. |

The budget variable records an approved amount.
It does not enforce a spending cap or configure an AWS Budget.
The actual budget alert needs its own AWS setup.

Do not send passwords, access keys, or recovery codes in chat.
Do not save them in source files.
Do not make a production role available to this workflow.
Restrict the GitHub `development` environment to `main`.

The deployment role needs access to the development stack, its artifact bucket, and its permitted execution role.
It also needs the specified public-asset upload and CloudFront invalidation actions.
The execution role needs permissions for the resources in the reviewed SAM template.
The [account-specific setup](guide-aws-development-access.md) is prepared for permission review.
Do not substitute administrator permissions to avoid that review.

## Deployment and acceptance

The only deployment workflow is [dev-release.yml](../../.github/workflows/dev-release.yml).
It does checks for pull requests and updates to `main`.
Development deployment starts only through its manual action on `main` with the deployment input selected.
The repository must also have `AWS_DEV_ENABLED=true`.
The workflow has one concurrency group and does not cancel an active deployment.

The workflow does integration checks before deployment.
It does infrastructure checks before the CloudFormation change.
It deploys the API, DynamoDB table, Cognito pool, and public frontend assets.
Then it does browser checks against the deployed URL.

The first stack makes a Cognito user pool with public sign-up disabled.
Make the test operator through an authorized AWS console session after that pool exists.
Keep its credentials in the secure GitHub environment.
Until that operator exists, the deployed browser check cannot pass.
An installation without passing browser checks is not a verified release.

The workflow saves a JSON release record as an Actions artifact.
The record contains the development URL, exact commit, integration result, browser result, and limits.
Failed attempts keep an unverified status.
The browser check must use real Cognito sign-in for a verified development release.
Local identity tests cannot replace it.

## Resources, costs, and recovery

The first slice uses an HTTP API, Lambda, DynamoDB, Cognito, S3, CloudFront, and CloudWatch Logs.
The template limits the case function to two simultaneous executions and a ten-second timeout.
These limits do not guarantee a monetary maximum.
The project has no account-specific cost estimate yet.

The application role can put, get, and query case records in its table.
It has no model-invocation or bank-document permissions.
CloudFront serves public application assets only.
Private case responses use `Cache-Control: no-store`.

CloudFormation can roll back a failed stack update.
For an application regression, prepare a revert commit through the same tests and deployment workflow.
Keep the earlier release record.
Do not rewrite Git history.

The data table, user pool, asset bucket, and log group use retention rules.
They are not automatically deleted with the stack.
Review costs and retained resources before any later cleanup.
Deletion and production deployment need different, explicit authorization.

## Source references

- [AWS account root-user practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/root-user-best-practices.html).
- [GitHub OIDC trust for AWS](https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-aws).
- [GitHub deployment concurrency](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/control-deployments).

Use the [delivery tickets](05_FEATURE_TICKETS.md#delivery-slices) for the next complete flow.
