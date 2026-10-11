# AWS release actions

Date: 2026-10-11.
Source commit: `ae2ead73d4dc4008c77fd85fad0d3485cd423a89`.
Account: `482439369658`.
Region: Mumbai, `ap-south-1`.
The [account check](../../runs/2026-10-11-slice-05-release/aws-release-preflight.json) contains read-only verification results.
These checks created no AWS resource and invoked no model.

## Verified state

AWS CLI authentication now works through `et-hackathon-admin`.
The previous expired-login observation no longer describes the current session.
The profile uses the account root identity.
The root identity belongs to the AWS account owner.
The application still requires its specified runtime role.

The monthly cost budget is `USD 25`.
It is an alert threshold, not a spending cap.
The deployment stack remains `ROLLBACK_COMPLETE`.
No CloudFront distribution is listed.
The previous deployment failed because AWS required account verification.
Completion of that verification remains unconfirmed.

The fixed India model profile is active and lists Mumbai and Hyderabad destinations.
Model availability reports `NOT_AUTHORIZED` and no active agreement.
No Mumbai model logging configuration was returned.
Hyderabad is disabled for direct account access.
The direct Hyderabad logging check failed with an invalid-token response.
That failure does not establish the model profile's routing state.

AWS permits cross-Region routing to destinations that the account has not manually enabled.
Read [AWS cross-Region guidance](https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html).
Do not enable Hyderabad only to correct this direct-access check.
Private model processing remains disabled.

## Model activation

1. Open the [Bedrock console](https://ap-south-1.console.aws.amazon.com/bedrock/home?region=ap-south-1#/quickstart).
2. Set the Region to Mumbai.
3. Open Model catalog.
4. Find `GPT-5.6 Luna` from OpenAI.
5. Review its license through the model details page.
6. Complete the displayed account activation requirements if you accept those terms.
7. Tell Codex when model activation is complete.

Activation is an account agreement, not a model quality result.
First invocation can initiate an AWS Marketplace subscription and accept the applicable model license.
Read [AWS model-access guidance](https://docs.aws.amazon.com/bedrock/latest/userguide/model-access.html).
Codex requires permission for that account agreement before activation or first invocation.
Then run one bounded fictional test with the fixed India profile.
Keep private case data disabled until the required access and retention checks pass.

## CloudFront account verification

1. Open [AWS Support Center](https://support.console.aws.amazon.com/support/home#/).
2. Confirm account `482439369658`.
3. Open the existing account-verification case if one exists.
4. Otherwise, create an account and billing support case.
5. Explain that CloudFront rejected the development distribution because the account requires verification.
6. Include the exact error from the CloudFormation `Frontend` failure event.
7. Complete the verification steps that AWS requests.
8. Give Codex the case ID and verification status.

The Support API returned `SubscriptionRequiredException` for this account.
Browser automation timed out twice while opening the existing Support tab.
No case ID or verification completion was confirmed.
Do not purchase paid Support only to use the API.
AWS Support controls the account verification outcome.

## Remaining release conditions

Approve the proposed validator tools before their installation.
Run local template and security checks before account-aware deployment validation.
The account has no listed CloudTrail trail.
Event history does not provide durable audit retention.
Record that limit before account-aware deployment validation.

Complete external source-provider selection under D20.
Verify current source coverage and preserve a genuine second regulatory version before live amendment checks.
Run the required held-out quality checks with the fixed live model.
Obtain VS5 user review under D35 before merge.
Review failed-stack recovery and combined deployment changes before deployment.
Verify Cognito, ownership, storage privacy, queue processing, permissions, and service connections after deployment.

The [VS5 release contract](spec-slice-05-release.md) preserves the complete release scope.
The model agreement and AWS account verification do not satisfy its other requirements.
