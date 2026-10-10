# ArchView verification

Date: 2026-10-09.
Decision: [D21](../docs/decisions/gov-decision-log.md#d21---technical-architecture-views).

## Scope

The user requested the full Regulatory Agent architecture.
The user excluded a crawler view and retained the external retrieval API.
The provider remains undecided.
The application remains unimplemented.

The [blueprint](../docs/architecture/02_TECHNICAL_BLUEPRINT.md#architecture-views) contains links and image previews.
The two views show the AWS components and assessment controls.
Both role nodes in the assessment view represent the same case operator.
They do not establish independent approval.

## Tools and sources

Used the local ArchView skill in lean mode.
Read its skill instructions and lean data specification.
Ran its create-archview.js generator for both JSON sources.
The [render script](../ops/render_architecture.py) runs this generator and sets readable positions.
It preserves the ArchView icons, relationships, zoom control, and export controls.
The shared skill files remain unchanged.

The system source contains 12 nodes and 13 edges.
The assessment source contains 12 nodes and 11 edges.
All edge endpoints resolve.
Each HTML file contains its scripts and images.
The view links require the companion files in the same folder.

## Browser checks

Opened both HTML files in an isolated Chrome session.
Inspected the rendered diagrams and both exported PNG files.
Adjusted node positions and edge labels for readability.

| Check | Result |
|---|---|
| System view has all 12 nodes | PASS |
| Assessment view has all 12 nodes | PASS |
| System-to-assessment navigation | PASS |
| Assessment-to-system navigation | PASS |
| Zoom and Move mode control | PASS |
| PNG export for both views | PASS |
| JavaScript errors during these checks | None |

Saved browser images:

- [System view](2026-10-09-arch-system-browser.png).
- [Assessment view](2026-10-09-arch-assessment-browser.png).

The Report control opens the browser print dialog.
The first check incorrectly expected a direct PDF download and timed out.
No saved PDF is part of this delivery.
The blueprint now gives the browser print steps.

## Language review

Used the ASD-STE100 skill on the complete blueprint.
See the [language review](2026-10-09-architecture-ste-review.md) for the original comparison and technical terms.
The [source copy](2026-10-09-before-archview-blueprint.txt) preserves the text before this task.

The original D17 rewrite used a custom language scan.
The later regulatory API task used the skill checker on the blueprint.
Its [saved result](2026-10-09-regulatory-api-ste-check-v2.json) reports no mechanical findings.
These records do not prove full ASD-STE100 compliance.

This task reviewed instruction order, explicit actors, consistent terms, permissions, limits, and technical meaning.
The final check includes the new navigation text and view descriptions.
The complete official dictionary could not be retrieved.
Vocabulary, permitted meanings, and grammatical-role compliance remain unverified.

The final skill check reported zero mechanical findings across all six inputs.
Its output is runs/2026-10-09-archview-final-ste-check.json.
The structural check found 19 Markdown files and 155 valid local links.
All original blueprint tables and external source links remain unchanged.
The root retains four files and seven folders.
Its output is runs/2026-10-09-archview-structure-check.json.

## Reproduction

From the project root, run:

```powershell
py -X utf8 -B ops\render_architecture.py
```

The script requires Node.js, Python, and the installed ArchView skill.
It regenerates the HTML files from their JSON sources.
After a source change, export each PNG again through its Image control.

## Evidence boundary

The diagrams preserve the model identifier, India constraints, immutable evidence, private-query restrictions, and job limits.
No crawler, OCR capability, regulatory provider, or independent reviewer role was added.
No application tests, live model evaluations, provider checks, or AWS deployment ran.
