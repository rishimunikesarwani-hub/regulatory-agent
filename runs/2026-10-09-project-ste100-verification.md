# Project Markdown language verification

Date: 2026-10-09.
Decision: [D18](../docs/decisions/gov-decision-log.md#d18--project-markdown-language).
Status: PASS for the documented language and preservation checks.
Full ASD-STE100 dictionary compliance remains unverified.

## Scope

Apply ASD-STE100 writing rules to all current project Markdown.
Set the same default for new projects in the global AGENTS.md.
Do not change other existing projects.

The project originally contained 14 Markdown files.
This change adds a [writing guide](../docs/guide-ste100-writing.md) and this report.
The final package contains 16 Markdown files.

The global file is `C:\Users\Be Flith Rich\AGENTS.md`.
Only the new Markdown language section changes that file.
The other global instructions remain unchanged.

## Preserved sources

The [backup archive](2026-10-09-before-project-ste100.zip) contains all 14 original Markdown files.
The [manifest](2026-10-09-ste100-source-manifest.json) maps their paths, archive names, and SHA-256 hashes.
Each archive entry matches its recorded source hash.

The global backup is `C:\Users\Be Flith Rich\AGENTS.md.2026-10-09-before-ste100.bak`.
The earlier [blueprint source](2026-10-09-technical-blueprint-before-ste100.txt) remains unchanged.

## Language review

The reference is [ASD-STE100 Issue 9](https://www.asd-ste100.org/assets/files/ASD-STE100_ISSUE9.pdf).
The issue date is 2025-01-15.
The [writing guide](../docs/guide-ste100-writing.md) records the writing rules and project terms.

The edit uses short sentences and direct instructions.
It removes metaphors and separates instructions.
It retains technical names, exact identifiers, and source quotations.
It keeps historical results as historical records.

The scan measures sentences and table cells after removal of Markdown formatting and link destinations.
The scan does not split sentences at colons.
The scan excludes fenced code.
This structural check does not establish dictionary or approved-meaning compliance.

## Preservation review

The review compares original and revised files.
It covers scope, requirements, prohibitions, permissions, uncertainty, dates, budgets, and approval history.
The automated comparison covers IDs, numeric tokens, inline literals, and source URLs.

The handbook no longer prescribes 60% Rishi Voice rawness.
D12 retains that historical value.
D18 authorizes its replacement with the STE rule.

The eight blueprint sections remain.
The configuration rows and record identity/content cells remain exact.
Historical reports retain their original counts and hashes.
Their scope notes identify the earlier checks.

## Final file checks

- All 16 project Markdown files match the reviewed text.
- All 122 local file and anchor links resolve.
- All documents have a title and valid UTF-8 text.
- No scanned sentence or table cell exceeds 20 words.
- No project Markdown prose contains a semicolon.
- All 14 requirement IDs remain.
- All 20 evaluation case IDs remain.
- All 18 decision IDs are present.
- All original test IDs, ticket IDs, inline literals, and source URLs remain.
- Original numeric tokens remain, except the replaced handbook style value described above.
- The previously revised technical blueprint remains text-identical.
- All 14 original Markdown archive entries match the source manifest hashes.
- The earlier blueprint source copy retains its original SHA-256.
- The source PDF retains its original SHA-256.
- The root still contains four files and seven folders.
- The global AGENTS.md differs only by the new language section.

The source PDF SHA-256 is:

`51c4e3c7cfece1e7f52eed3a1f81918ffc95625a59e77aa31ca37fc4b23a3483`

## Verification limits

The full official PDF request returned HTTP 403.
Official public descriptions and indexed excerpts were available.
The complete dictionary, part-of-speech rules, and approved meanings remain unverified.
Do not treat this report as certification of full ASD-STE100 compliance.

This edit does not verify external link availability, AWS account access, model quality, or deployment.
No application code or software tests ran.
No live model evaluation ran.
T1 source and fixture work remains pending.

## Next work

Use the [approved feature tickets](../docs/delivery/05_FEATURE_TICKETS.md).
Keep the local software tests separate from live model evaluations.
