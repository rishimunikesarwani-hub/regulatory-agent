# Integration keyboard-focus correction

Date: 2026-10-11.
Branch: `work/t3-aws-documents-focus`.
Status: Local and GitHub checks passed. Integrated through PR11.

GitHub run `38084594559` passed for `120c4748862f064856586f00bdb921d31ad69fac`.
It verified 204 backend checks, 27 browser checks, and the frontend build.
PR11 merged at `af59cc6cc8507b5b59d8866ae0899718172e3d47`.
Deployment was skipped.
Read [PR11](https://github.com/rishimunikesarwani-hub/regulatory-agent/pull/11) and [its check run](https://github.com/rishimunikesarwani-hub/regulatory-agent/actions/runs/38084594559).

CI run `38084172144` failed the existing narrow-view keyboard check.
The case-list response moved focus to the heading after the user had started form entry.
The application source was identical to the earlier passing integration commit.
The failure exposed a timing-dependent application behavior.
It was not treated as a reason to weaken the keyboard assertion.

The focus contract preceded the correction in commit `6605f77`.
`focus-red.txt` records a deterministic delayed-response reproduction.
The checkbox received focus before the delayed case-list request completed.
Its focus then changed to the heading.
The correction permits automatic heading focus only when the document body has focus.
An active application control keeps its focus.

`focus-green.txt` records 27 passing browser checks.
These include the earlier keyboard flow and the new delayed-response check.
`focus-build.txt` records the passing TypeScript and Vite build.
The backend source is unchanged from the integrated 204-check result.
The earlier screenshots were restored from their recorded commit.
The correction's screenshots remain in `focus-regression/`.

This correction uses the existing isolated API port `8191`, web port `5192`, and browser-test database.
The VS3 review branch and feedback services remain unchanged.
Live AWS deployment and model integration remain pending.
The documentation received mechanical and meaning-preservation review.
The dictionary and approved-meaning review remains incomplete.
