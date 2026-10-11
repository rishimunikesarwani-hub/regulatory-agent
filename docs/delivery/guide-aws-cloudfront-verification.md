# AWS CloudFront account verification

Date: 2026-10-10.
Status: The user selected CloudFront and will submit the prepared AWS Support request.

## Verified problem

AWS authentication succeeded for account `482439369658`.
The second application release passed integration checks.
CloudFront rejected distribution creation with HTTP `403`.

AWS returned this exact message:

> Your account must be verified before you can add new CloudFront resources.

The request ID is `4466b537-0143-4557-adb2-af3a2c92949d`.
The failure occurred at `2026-10-10 17:24:54 UTC`.
Release run `38071339699` failed.
Live browser acceptance was skipped.
No application URL is available.

The failed stack reached `ROLLBACK_COMPLETE`.
Rollback means that AWS reversed the incomplete resource creation.
The retention rules preserved the empty case table, frontend bucket, and user pool.
Live checks found zero case records, zero frontend objects, and zero users.
No retained resource was deleted manually.

## Submit the prepared request

The [AWS Support tab](https://support.console.aws.amazon.com/support/home#/) contains the prepared account verification request.
The page shows `Rishi Muni Demo (482439369658)` and `Basic Support`.
The request has not been sent.

1. Check the account name in the open AWS Support tab.
2. Read the prepared `Issue description`.
3. Select `Send message`.
4. Follow the AWS instructions for account verification.
5. Save the support case ID when AWS creates the case.
6. Tell Codex when AWS confirms CloudFront access.

Use the AWS console for any requested verification information.
Do not put credentials or verification documents in chat or project files.

## Current submission check

Date: 2026-10-11.

The AWS console still shows the prepared text in `Issue description`.
The Support dashboard shows `No open cases`.
The current case-history view shows `No cases to display.`
No submitted verification case was visible in these views.
This is not evidence that AWS is processing the request.

Select `Send message` in the prepared tab.
Complete the AWS case instructions until a case ID is available.
Keep any requested identity documents in the AWS verification process only.
The user selected manual submission. Codex did not send this request.

The command-line Support check returned `SubscriptionRequiredException`.
The browser console supplied the current submission evidence instead.
The application stack still has status `ROLLBACK_COMPLETE`.
No deployment or cloud resource change occurred during these checks.

Read the [handoff check](../../runs/2026-10-11-slice-03-integration/verification-handoff.md) for evidence and limits.

## Resume deployment after verification

Keep CloudFront in the approved hosting design.
Keep the monthly USD 25 cost alerts.
Review recovery of the failed stack before another release.
Obtain approval before any manual deletion.
Preserve retained resources until their disposition is approved.

Run the same serialized development workflow after recovery.
Complete actual Cognito sign-in and case persistence checks before reporting a verified release.

The local feedback interface remains available at `http://127.0.0.1:5173/`.
Its sign-in screen shows `The Regulator` and the centered `Sign in to continue` card.
All 14 local browser checks and 166 backend checks passed.
The next vertical slice remains subject to user feedback.

## Evidence

- [AWS failure](../../runs/2026-10-10-slice-01-feedback/aws-release-02-failure.json).
- [Release result](../../runs/2026-10-10-slice-01-feedback/aws-release-02/development.json).
- [Retained resources](../../runs/2026-10-10-slice-01-feedback/aws-retained-resources.json).
- [Current development access](guide-aws-development-access.md).
