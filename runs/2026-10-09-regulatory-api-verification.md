# Regulatory API design verification

Date: 2026-10-09.
Decision: [D20](../docs/decisions/gov-decision-log.md#d20---current-regulatory-retrieval).
Status: PASS for design consistency and document checks.
The external provider and implementation remain unverified.

## Change scope

The user requested current regulatory retrieval through an external API.
The user chose to leave the provider undecided.
The [blueprint](../docs/architecture/02_TECHNICAL_BLUEPRINT.md#current-regulatory-sources) contains the controlling design.

The change modifies only the necessary contracts.
Five specifications, two verification plans, project instructions, the decision log, and the project log receive corrections.
The [backup archive](2026-10-09-before-regulatory-api.zip) preserves the ten previous files.

The external API supplies current public regulations and amendments.
Each current assessment verifies selected versions before processing.
S3 retains bank files and historical assessment evidence.
Stored copies do not establish current-source status.

## Design review

| Condition | Required behavior |
|---|---|
| Normal operation | Refresh the scoped source catalogue. Verify selected versions before assessment. |
| Authority evidence | Keep source URLs, exact text, versions, verification times, and amendment references. |
| Provider cache | Require authority synchronization evidence. A recent API response alone is insufficient. |
| Amendment or withdrawal | Create new version metadata. Request review when selected versions changed. |
| Future-effective rule | Use the assessment date to determine applicability. |
| Verification failure | Stop before a current assessment. Show the last successful check. |
| Historical review | Keep prior snapshots, source passages, and findings unchanged. |
| Request privacy | Send public source queries only. Keep private bank content in India. |
| Request limits | Set bounded requests, timeouts, retries, pagination, and response sizes before implementation. |
| Local tests | Use controlled API responses. Block external calls in default tests. |
| Live verification | Verify provider coverage, authority synchronization, request privacy, and failure handling separately. |

No new scheduler, crawler, vector service, or deployment is part of this correction.
Independent scheduled monitoring remains future work.
All original model limits, document limits, requirement IDs, and numerical quality gates remain.

## References

[RBI Master Directions](https://www.rbi.org.in/Scripts/BS_ViewMasterDirections.aspx?did=338) describe updates when rules or policy change.
This source does not establish an RBI API contract.

[HTTP caching and validation](https://www.rfc-editor.org/rfc/rfc9111.html#section-4.3) describes response validation.
Provider authority synchronization remains a separate verification requirement.

## Language review

Use ASD-STE100 Issue 9 writing rules.
Keep technical identifiers, original requirements, and existing source links.
The user authorized the source-retrieval design change and related acceptance corrections.
The complete dictionary review remains unverified.

## File verification

- The package contains 17 Markdown files.
- All 130 local file and anchor links resolve.
- All 14 requirement IDs and 20 evaluation case IDs remain.
- The decision log contains D01–D20.
- The ten changed files match the reviewed corrections.
- All six unrelated Markdown files remain unchanged.
- All original test IDs, ticket IDs, numeric tokens, inline literals, and source URLs remain.
- The model, region, and job-limit configuration table remains exact.
- The ten archived source files match their original text.
- The source PDF SHA-256 remains unchanged.
- The root retains four files and seven folders.
- The STE checker reported zero mechanical findings in the changed files and this report.

The STE checker used procedural mode with the 20-word limit.
The checker also reviewed punctuation and contractions.
The review preserved permissions, prohibitions, privacy boundaries, and historical evidence.
The authorized design changes are recorded in D20.
Full dictionary and approved-meaning compliance remains unverified.

## Limits

No provider has been selected.
No application code, software tests, live API checks, model evaluations, or cloud deployment ran.
Mechanical document checks do not establish provider freshness.
The provider endpoint, update delay, coverage, historical versions, pricing, and terms remain TBD.
