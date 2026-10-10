# Session B verification

Date: 2026-10-10.
Branch: `work/session-b`.
Base commit: `20743635e68c57257432de655f6f02a669b956a8`.
Scope: T2 local contracts, adapters, and test environment.

## Results

The local suite passed 59 tests with no failures or skipped tests.
This total contains 29 imported T1 fixture checks and 30 T2 checks.
A fresh source copy passed the same suite.
Its installation used a new Python environment and an empty package cache.
The controlled development demonstration completed successfully.

| Evidence | Result |
| --- | --- |
| [Initial missing-package test](red.txt) | Failed before implementation. |
| [Missing adapter behavior](red-behavior.txt) | 23 checks ran. Fourteen failed because the adapters were absent. |
| [Freshness regression](red-freshness.txt) | A future verification timestamp caused the intended failing assertion. |
| [Local suite](green.txt) | 59 passed. |
| [Clean installation](clean-copy.txt) | New environment, exact dependencies, tests, and demonstration passed. |
| [T1 import receipt](t1-import.json) | Frozen source and fixture hashes matched before import. |
| [Testing-guide language check](ste-guide.json) | No mechanical findings. |
| [Contract language check](ste-contracts-v3.json) | No mechanical findings after paragraph separation. |

The runtime is CPython `3.12.13` on Windows.
The package manager used for setup is `uv 0.11.26`.
The [lock file](../../ops/requirements.lock) records all 11 exact package versions.
The default worker removes cloud credential environment variables.
Child-process tests verify blocked external connections and permitted loopback connections.

## Requirement coverage

| Checks | Requirement and verified behavior |
| --- | --- |
| B01-B04 | CT-05. Request schemas, response schemas, forbidden owner fields, scope limits, and finding status constraints. |
| B05 | UT-02 contract portion. Byte limits, page equivalents, and aggregate document limits. |
| B06 | CT-01 and CT-02. Development identity requires local mode and a loopback peer. |
| B07-B08 | CT-02 and CT-04. Case authorization, immutable records, immutable blobs, and snapshot preservation. |
| B09-B12 | CT-03, CT-04, UT-09, and UT-11 contract portions. Atomic claims, duplicate requests, counters, deadlines, and finalization. |
| B13-B14 | CT-01 and UT-12 storage portion. Local runner and separate review records. |
| B15-B20 | CT-01 and CT-05 retrieval portion. Controlled sources, bounds, failure handling, selected versions, and conditional responses. |
| B21-B23 | REQ-X06. Worker network guard, absent cloud credentials, and labelled development fixtures. |
| B24-B28 | CT-04 and CT-05 retrieval portion. Verification dates, saved pages, bounded retries, and immutable prior snapshots. |
| B29-B30 | CT-01, UT-07, and CT-04 contract portions. Adapter interfaces, model action scope, and persistence across processes. |

No row establishes completion of an entire later-ticket acceptance case.
The shared schemas define those later behavior contracts.
T3 through T9 remain unimplemented in this worktree.

## User test

Read [the testing guide](../../docs/delivery/guide-session-b-testing.md).
Run `.venv\Scripts\python.exe -X utf8 ops/check.py` from worktree B.
Expect `Ran 59 tests` and `OK`.

The demonstration uses `DEV-02` by default.
It saves an immutable snapshot and validates one simulated model action.
It verifies duplicate-request identity, denied cross-owner access, and the saved call count.
It creates no assessment finding.
Its assessment job therefore reports `failed`, with the selected obligation unchecked.
This expected state prevents a false completed-assessment claim.

## Integration state and limits

All changes remain local in Session B.
No commit, merge, push, deployment, or submission occurred.
Session A files were copied without edits.
The five approved specifications, project instructions, root manifest, and project log remain unchanged.
The integration session owns updates to those shared records.

The extraction equivalent and retrieval limits are explicit T2 implementation defaults.
The integration owner must incorporate them before dependent implementation.
HTTP handlers, file parsers, exact citation validation, assessment logic, and the reviewer interface remain later work.
No live regulatory provider, model call, or AWS service was exercised.
No model-quality evaluation ran.
The 20 held-out cases remain separate from development inputs.

The network guard controls Python socket operations.
It is not a firewall for arbitrary native programs.
The controlled retrieval adapter does not implement a live HTTP timeout or redirect check.
The future live adapter must enforce the defined transport requirements.

Reviewed new prose for sentence length, terminology, scope, permissions, and requirement preservation.
The complete official ASD-STE100 Issue 9 dictionary was unavailable.
Full dictionary and approved-meaning review remain incomplete.
