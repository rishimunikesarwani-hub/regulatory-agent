# The Regulator assessment report

## Export status

> Assessment export · Simulated processing · Fictional bank data

## Snapshot and selected versions

> \{
>   "assessment\_date": "2024-04-08",
>   "bank\_profile": \{
>     "name": "Fictional export bank 1791701301491"
>   \},
>   "case\_id": "ad1d0bed7ca54770a00182b92fb707d8",
>   "mode": "historical",
>   "model\_version": "in.openai.gpt-5.6-luna",
>   "prompt\_version": "controlled-vs3-v1",
>   "selected\_document\_ids": \{\},
>   "selected\_obligations": \[
>     "RBI-IT-19b"
>   \],
>   "selected\_versions": \{
>     "5a3d606c03364a6f8c9edc1f0b448c23": "1",
>     "RBI-IT-2023": "2023-11-07"
>   \},
>   "snapshot\_id": "140f6e7a0bd7590fb2aa26a1a69e0eeb",
>   "synthetic": true
> \}

## Cohort filters and time bases

> \{
>   "kind": "single\_assessment",
>   "case\_id": "ad1d0bed7ca54770a00182b92fb707d8",
>   "run\_id": "140f6e7a0bd7590fb2aa26a1a69e0eeb",
>   "snapshot\_id": "140f6e7a0bd7590fb2aa26a1a69e0eeb",
>   "model\_id": "in.openai.gpt-5.6-luna",
>   "prompt\_version": "controlled-vs3-v1",
>   "data\_mode": "controlled\_simulation",
>   "recommendation\_availability": \{
>     "through": "2026-10-11T06:48:24.485294\+00:00",
>     "end\_inclusive": true
>   \},
>   "runtime\_selection": \{
>     "job\_id": "eaaee2f2b8e4474db5e268d504b6b294",
>     "job\_admitted\_at": "2026-10-11T06:48:23.527519\+00:00",
>     "job\_state\_time\_basis": "observed\_current\_state"
>   \}
> \}

## Observed job state

> \{
>   "authority\_verified\_at": null,
>   "case\_id": "ad1d0bed7ca54770a00182b92fb707d8",
>   "created\_at": 1791701303.527519,
>   "deadline": 1791701903.7251892,
>   "finished\_at": 1791701304.0028625,
>   "freshness": "unverified",
>   "job\_id": "eaaee2f2b8e4474db5e268d504b6b294",
>   "label": "Simulated",
>   "model\_calls": 1,
>   "retrieval\_calls": 0,
>   "snapshot\_id": "140f6e7a0bd7590fb2aa26a1a69e0eeb",
>   "stage": "persistence",
>   "started\_at": 1791701303.7251892,
>   "state": "completed",
>   "stop\_reason": null,
>   "unchecked\_obligations": \[\]
> \}

## Report cutoff

> 2026-10-11T06:48:24.485294\+00:00

## Freshness and authority verification

> \{
>   "freshness": "unverified",
>   "authority\_verified\_at": null
> \}

## Obligation

> \{
>   "obligation\_id": "RBI-IT-19b",
>   "requirement": "Personnel with elevated system access entitlements shall be closely supervised with all their systems activities logged and periodically reviewed.",
>   "conditions": \[
>     "Personnel with elevated system access entitlements.",
>     "Applicability to the listed regulated entities must be established."
>   \],
>   "exceptions": \[
>     "Local Area Banks",
>     "NBFC-Core Investment Companies"
>   \],
>   "applicability": "Unverified for this fictional bank profile.",
>   "citations": \[
>     \{
>       "document\_version\_id": "RBI-IT-2023:2023-11-07",
>       "passage\_id": "RBI-IT-2023:2023-11-07:19b",
>       "location": "Clause 19(b)",
>       "quote": "Personnel with elevated system access entitlements shall be closely supervised with all their systems activities logged and periodically reviewed."
>     \},
>     \{
>       "document\_version\_id": "RBI-IT-2023:2023-11-07",
>       "passage\_id": "RBI-IT-2023:2023-11-07:2ai",
>       "location": "Clause 2(a)(i)",
>       "quote": "all Banking Companies 1 , Corresponding New Banks and State Bank of India as defined under subsections (c), (da) and (nc) of section 5 of the Banking Regulation Act, 1949 (collectively referred to as ‘commercial banks’ hereinafter)."
>     \},
>     \{
>       "document\_version\_id": "RBI-IT-2023:2023-11-07",
>       "passage\_id": "RBI-IT-2023:2023-11-07:2b",
>       "location": "Clause 2(b)",
>       "quote": "These Directions shall not be applicable to: Local Area Banks NBFC-Core Investment Companies"
>     \}
>   \]
> \}

## Mapped control

> \{
>   "control\_id": "ACCESS-01",
>   "statement": "Control ACCESS-01 requires supervision of privileged sessions, complete activity logging, and a weekly review.",
>   "purpose": "Privileged session oversight",
>   "owner": null,
>   "frequency": "Weekly under the fictional bank policy.",
>   "citations": \[
>     \{
>       "document\_version\_id": "47b99e978120442a99c94a0a0f00a13c",
>       "passage\_id": "47b99e978120442a99c94a0a0f00a13c-2",
>       "location": "Line 2",
>       "quote": "Control ACCESS-01 requires supervision of privileged sessions, complete activity logging, and a weekly review."
>     \}
>   \]
> \}

## Selected obligations

> \[
>   \{
>     "obligation\_id": "RBI-IT-19b",
>     "requirement": "Personnel with elevated system access entitlements shall be closely supervised with all their systems activities logged and periodically reviewed.",
>     "conditions": \[
>       "Personnel with elevated system access entitlements.",
>       "Applicability to the listed regulated entities must be established."
>     \],
>     "exceptions": \[
>       "Local Area Banks",
>       "NBFC-Core Investment Companies"
>     \],
>     "applicability": "Unverified for this fictional bank profile.",
>     "citations": \[
>       \{
>         "document\_version\_id": "RBI-IT-2023:2023-11-07",
>         "passage\_id": "RBI-IT-2023:2023-11-07:19b",
>         "location": "Clause 19(b)",
>         "quote": "Personnel with elevated system access entitlements shall be closely supervised with all their systems activities logged and periodically reviewed."
>       \},
>       \{
>         "document\_version\_id": "RBI-IT-2023:2023-11-07",
>         "passage\_id": "RBI-IT-2023:2023-11-07:2ai",
>         "location": "Clause 2(a)(i)",
>         "quote": "all Banking Companies 1 , Corresponding New Banks and State Bank of India as defined under subsections (c), (da) and (nc) of section 5 of the Banking Regulation Act, 1949 (collectively referred to as ‘commercial banks’ hereinafter)."
>       \},
>       \{
>         "document\_version\_id": "RBI-IT-2023:2023-11-07",
>         "passage\_id": "RBI-IT-2023:2023-11-07:2b",
>         "location": "Clause 2(b)",
>         "quote": "These Directions shall not be applicable to: Local Area Banks NBFC-Core Investment Companies"
>       \}
>     \]
>   \}
> \]

## Extracted controls

> \[
>   \{
>     "control\_id": "ACCESS-01",
>     "statement": "Control ACCESS-01 requires supervision of privileged sessions, complete activity logging, and a weekly review.",
>     "purpose": "Privileged session oversight",
>     "owner": null,
>     "frequency": "Weekly under the fictional bank policy.",
>     "citations": \[
>       \{
>         "document\_version\_id": "47b99e978120442a99c94a0a0f00a13c",
>         "passage\_id": "47b99e978120442a99c94a0a0f00a13c-2",
>         "location": "Line 2",
>         "quote": "Control ACCESS-01 requires supervision of privileged sessions, complete activity logging, and a weekly review."
>       \}
>     \]
>   \}
> \]

## Original findings and recommendation IDs

> \[
>   \{
>     "finding\_id": "a929677e34df5aecafb124f3a7e0c3fd",
>     "snapshot\_id": "140f6e7a0bd7590fb2aa26a1a69e0eeb",
>     "obligation\_id": "RBI-IT-19b",
>     "control\_ids": \[
>       "ACCESS-01"
>     \],
>     "status": "needs\_review",
>     "evidence\_condition": "missing",
>     "citations": \[
>       \{
>         "document\_version\_id": "RBI-IT-2023:2023-11-07",
>         "passage\_id": "RBI-IT-2023:2023-11-07:19b",
>         "location": "Clause 19(b)",
>         "quote": "Personnel with elevated system access entitlements shall be closely supervised with all their systems activities logged and periodically reviewed."
>       \},
>       \{
>         "document\_version\_id": "47b99e978120442a99c94a0a0f00a13c",
>         "passage\_id": "47b99e978120442a99c94a0a0f00a13c-2",
>         "location": "Line 2",
>         "quote": "Control ACCESS-01 requires supervision of privileged sessions, complete activity logging, and a weekly review."
>       \}
>     \],
>     "rationale": "Controlled example. The policy states a control, but this example has no verified operational evidence. Applicability and activity records need human review.",
>     "remedy": "Confirm applicability. Request dated session records, supervisor sign-offs, complete activity logs, and completed periodic reviews.",
>     "gap\_kind": "evidence",
>     "applicability\_reason": null,
>     "claims": \[\],
>     "run\_id": "140f6e7a0bd7590fb2aa26a1a69e0eeb",
>     "primary\_recommendation": "Confirm applicability. Request dated session records, supervisor sign-offs, complete activity logs, and completed periodic reviews.",
>     "available\_at": "2026-10-11T06:48:23.960894Z",
>     "model\_id": "in.openai.gpt-5.6-luna",
>     "prompt\_version": "controlled-vs3-v1",
>     "data\_mode": "controlled\_simulation",
>     "source\_version\_ids": \[
>       "5a3d606c03364a6f8c9edc1f0b448c23:1",
>       "RBI-IT-2023:2023-11-07"
>     \]
>   \}
> \]

## Saved review events

> \[
>   \{
>     "event\_kind": "final\_review",
>     "disposition": "approved",
>     "accepted\_content": \{
>       "status": "needs\_review",
>       "rationale": "Controlled example. The policy states a control, but this example has no verified operational evidence. Applicability and activity records need human review.",
>       "recommendation": "Confirm applicability. Request dated session records, supervisor sign-offs, complete activity logs, and completed periodic reviews."
>     \},
>     "reason": null,
>     "expected\_revision": 0,
>     "idempotency\_key": "39b5dc12-a414-480e-8e79-94ba900eab4b",
>     "event\_id": "45c8c57bf33445c8b7a18df77584afbf",
>     "finding\_id": "a929677e34df5aecafb124f3a7e0c3fd",
>     "reviewer\_id": "slice-05-tests",
>     "committed\_at": "2026-10-11T06:48:24.437938Z",
>     "revision": 1
>   \}
> \]

## Review summary

metric_definition_version: d24-v1

cutoff: 2026-10-11T06:48:24.485294+00:00

data_mode: controlled_simulation

run_id: 140f6e7a0bd7590fb2aa26a1a69e0eeb

eligible: 1

reviewed: 1

pending: 0

approved: 1

edited: 0

rejected: 0

approval_rate: 1.0

edit_rate: 0.0

rejection_rate: 0.0

adoption_rate: 1.0

review_coverage: 1.0

## Recorded runtime

cost: Unknown

> \{
>   "run\_id": "140f6e7a0bd7590fb2aa26a1a69e0eeb",
>   "attempts": \[
>     \{
>       "actual\_response\_model\_id": null,
>       "artifact\_ids": \[\],
>       "attempt\_id": "acacb59f701e4b9bb55c21499abb8da2",
>       "candidate\_passage\_ids": \[
>         "47b99e978120442a99c94a0a0f00a13c-1",
>         "47b99e978120442a99c94a0a0f00a13c-2",
>         "47b99e978120442a99c94a0a0f00a13c-3",
>         "RBI-IT-2023:2023-11-07:2a",
>         "RBI-IT-2023:2023-11-07:2ai",
>         "RBI-IT-2023:2023-11-07:2b",
>         "RBI-IT-2023:2023-11-07:19a",
>         "RBI-IT-2023:2023-11-07:19b",
>         "RBI-IT-2023:2023-11-07:19c",
>         "RBI-IT-2023:2023-11-07:29a",
>         "RBI-IT-2023:2023-11-07:29b",
>         "RBI-IT-2023:2023-11-07:29e"
>       \],
>       "dispatched": true,
>       "duration\_seconds": 0.0,
>       "errors": \[\],
>       "event\_id": "0e83f19b71414736a8cb96f8c82f38f3",
>       "finished\_at": "2026-10-11T06:48:23.795856Z",
>       "first\_token\_seconds": null,
>       "job\_id": "eaaee2f2b8e4474db5e268d504b6b294",
>       "model\_id": null,
>       "operation": "retrieval",
>       "original\_processing\_event\_id": null,
>       "provider\_request\_id": null,
>       "retry\_index": 0,
>       "returned\_bytes": null,
>       "run\_id": "140f6e7a0bd7590fb2aa26a1a69e0eeb",
>       "selected\_passage\_ids": \[
>         "RBI-IT-2023:2023-11-07:19b",
>         "RBI-IT-2023:2023-11-07:2ai",
>         "RBI-IT-2023:2023-11-07:2b",
>         "47b99e978120442a99c94a0a0f00a13c-2"
>       \],
>       "selected\_text\_bytes": null,
>       "snapshot\_id": "140f6e7a0bd7590fb2aa26a1a69e0eeb",
>       "stage": "retrieval",
>       "stage\_id": "retrieval",
>       "started\_at": "2026-10-11T06:48:23.795345Z",
>       "state": "succeeded",
>       "streaming": false,
>       "unused\_allowance": null,
>       "usage": \{
>         "cache\_read\_tokens": null,
>         "cache\_write\_tokens": null,
>         "input\_tokens": null,
>         "output\_tokens": null
>       \},
>       "versions": \{
>         "application": "vs5-v1",
>         "chunking": "source-locations-v1",
>         "extraction": "vs2-v1",
>         "model\_configuration": "controlled-response-v1",
>         "prompt": "controlled-vs3-v1",
>         "retrieval": "fixed-example-v1",
>         "schema\_version": "t2-v1"
>       \}
>     \},
>     \{
>       "actual\_response\_model\_id": null,
>       "artifact\_ids": \[\],
>       "attempt\_id": "c3382036205f4aa7b2708f360d493cf1",
>       "candidate\_passage\_ids": \[\],
>       "dispatched": true,
>       "duration\_seconds": 0.046999999991385266,
>       "errors": \[\],
>       "event\_id": "532d198585704260a7ffc519389c10e5",
>       "finished\_at": "2026-10-11T06:48:23.903636Z",
>       "first\_token\_seconds": null,
>       "job\_id": "eaaee2f2b8e4474db5e268d504b6b294",
>       "model\_id": "in.openai.gpt-5.6-luna",
>       "operation": "model",
>       "original\_processing\_event\_id": null,
>       "provider\_request\_id": null,
>       "retry\_index": 0,
>       "returned\_bytes": null,
>       "run\_id": "140f6e7a0bd7590fb2aa26a1a69e0eeb",
>       "selected\_passage\_ids": \[\],
>       "selected\_text\_bytes": null,
>       "snapshot\_id": "140f6e7a0bd7590fb2aa26a1a69e0eeb",
>       "stage": "model\_call",
>       "stage\_id": "model\_call",
>       "started\_at": "2026-10-11T06:48:23.857710Z",
>       "state": "succeeded",
>       "streaming": false,
>       "unused\_allowance": null,
>       "usage": \{
>         "cache\_read\_tokens": null,
>         "cache\_write\_tokens": null,
>         "input\_tokens": null,
>         "output\_tokens": null
>       \},
>       "versions": \{
>         "application": "vs5-v1",
>         "chunking": "source-locations-v1",
>         "extraction": "vs2-v1",
>         "model\_configuration": "controlled-response-v1",
>         "prompt": "controlled-vs3-v1",
>         "retrieval": "fixed-example-v1",
>         "schema\_version": "t2-v1"
>       \}
>     \},
>     \{
>       "actual\_response\_model\_id": null,
>       "artifact\_ids": \[\],
>       "attempt\_id": "e258d33723a342a9824d846178877a9a",
>       "candidate\_passage\_ids": \[\],
>       "dispatched": true,
>       "duration\_seconds": 0.0,
>       "errors": \[\],
>       "event\_id": "54e4931d5504442aa8c66607b0243cb0",
>       "finished\_at": "2026-10-11T06:48:23.929947Z",
>       "first\_token\_seconds": null,
>       "job\_id": "eaaee2f2b8e4474db5e268d504b6b294",
>       "model\_id": null,
>       "operation": "internal",
>       "original\_processing\_event\_id": null,
>       "provider\_request\_id": null,
>       "retry\_index": 0,
>       "returned\_bytes": null,
>       "run\_id": "140f6e7a0bd7590fb2aa26a1a69e0eeb",
>       "selected\_passage\_ids": \[\],
>       "selected\_text\_bytes": null,
>       "snapshot\_id": "140f6e7a0bd7590fb2aa26a1a69e0eeb",
>       "stage": "validation",
>       "stage\_id": "validation",
>       "started\_at": "2026-10-11T06:48:23.928744Z",
>       "state": "succeeded",
>       "streaming": false,
>       "unused\_allowance": null,
>       "usage": \{
>         "cache\_read\_tokens": null,
>         "cache\_write\_tokens": null,
>         "input\_tokens": null,
>         "output\_tokens": null
>       \},
>       "versions": \{
>         "application": "vs5-v1",
>         "chunking": "source-locations-v1",
>         "extraction": "vs2-v1",
>         "model\_configuration": "controlled-response-v1",
>         "prompt": "controlled-vs3-v1",
>         "retrieval": "fixed-example-v1",
>         "schema\_version": "t2-v1"
>       \}
>     \},
>     \{
>       "actual\_response\_model\_id": null,
>       "artifact\_ids": \[
>         "45c8c57bf33445c8b7a18df77584afbf"
>       \],
>       "attempt\_id": "90b9b091fe2f4e79a426b86f28c79c7e",
>       "candidate\_passage\_ids": \[\],
>       "dispatched": true,
>       "duration\_seconds": 0.015000000013969839,
>       "errors": \[\],
>       "event\_id": "73008df7455142ed8d98c2c5ee519695",
>       "finished\_at": "2026-10-11T06:48:24.446879Z",
>       "first\_token\_seconds": null,
>       "job\_id": "eaaee2f2b8e4474db5e268d504b6b294",
>       "model\_id": null,
>       "operation": "storage",
>       "original\_processing\_event\_id": null,
>       "provider\_request\_id": null,
>       "retry\_index": 0,
>       "returned\_bytes": null,
>       "run\_id": "140f6e7a0bd7590fb2aa26a1a69e0eeb",
>       "selected\_passage\_ids": \[\],
>       "selected\_text\_bytes": null,
>       "snapshot\_id": "140f6e7a0bd7590fb2aa26a1a69e0eeb",
>       "stage": "review\_event",
>       "stage\_id": "review\_event",
>       "started\_at": "2026-10-11T06:48:24.435065Z",
>       "state": "succeeded",
>       "streaming": false,
>       "unused\_allowance": null,
>       "usage": \{
>         "cache\_read\_tokens": null,
>         "cache\_write\_tokens": null,
>         "input\_tokens": null,
>         "output\_tokens": null
>       \},
>       "versions": \{
>         "application": "vs5-v1",
>         "chunking": "source-locations-v1",
>         "extraction": "vs2-v1",
>         "model\_configuration": "controlled-response-v1",
>         "prompt": "controlled-vs3-v1",
>         "retrieval": "fixed-example-v1",
>         "schema\_version": "t2-v1"
>       \}
>     \},
>     \{
>       "actual\_response\_model\_id": null,
>       "artifact\_ids": \[\],
>       "attempt\_id": "9b854c9a3ab5463f85e8ad7a9787c70c",
>       "candidate\_passage\_ids": \[\],
>       "dispatched": true,
>       "duration\_seconds": 0.0,
>       "errors": \[\],
>       "event\_id": "73f25e44b5b849ea96415b8bdd3a8419",
>       "finished\_at": "2026-10-11T06:48:23.742797Z",
>       "first\_token\_seconds": null,
>       "job\_id": "eaaee2f2b8e4474db5e268d504b6b294",
>       "model\_id": null,
>       "operation": "internal",
>       "original\_processing\_event\_id": null,
>       "provider\_request\_id": null,
>       "retry\_index": 0,
>       "returned\_bytes": null,
>       "run\_id": "140f6e7a0bd7590fb2aa26a1a69e0eeb",
>       "selected\_passage\_ids": \[\],
>       "selected\_text\_bytes": null,
>       "snapshot\_id": "140f6e7a0bd7590fb2aa26a1a69e0eeb",
>       "stage": "source\_verification",
>       "stage\_id": "source\_verification",
>       "started\_at": "2026-10-11T06:48:23.739793Z",
>       "state": "succeeded",
>       "streaming": false,
>       "unused\_allowance": null,
>       "usage": \{
>         "cache\_read\_tokens": null,
>         "cache\_write\_tokens": null,
>         "input\_tokens": null,
>         "output\_tokens": null
>       \},
>       "versions": \{
>         "application": "vs5-v1",
>         "chunking": "source-locations-v1",
>         "extraction": "vs2-v1",
>         "model\_configuration": "controlled-response-v1",
>         "prompt": "controlled-vs3-v1",
>         "retrieval": "fixed-example-v1",
>         "schema\_version": "t2-v1"
>       \}
>     \},
>     \{
>       "actual\_response\_model\_id": null,
>       "artifact\_ids": \[
>         "47b99e978120442a99c94a0a0f00a13c"
>       \],
>       "attempt\_id": "e30a5746e9ca4ba6b398597799ee7bde",
>       "candidate\_passage\_ids": \[\],
>       "dispatched": false,
>       "duration\_seconds": 0.0,
>       "errors": \[\],
>       "event\_id": "9e3582d845394dfbbc6f691545917792",
>       "finished\_at": "2026-10-11T06:48:23.768277Z",
>       "first\_token\_seconds": null,
>       "job\_id": "eaaee2f2b8e4474db5e268d504b6b294",
>       "model\_id": null,
>       "operation": "internal",
>       "original\_processing\_event\_id": "47b99e978120442a99c94a0a0f00a13c",
>       "provider\_request\_id": null,
>       "retry\_index": 0,
>       "returned\_bytes": null,
>       "run\_id": "140f6e7a0bd7590fb2aa26a1a69e0eeb",
>       "selected\_passage\_ids": \[\],
>       "selected\_text\_bytes": null,
>       "snapshot\_id": "140f6e7a0bd7590fb2aa26a1a69e0eeb",
>       "stage": "extraction",
>       "stage\_id": "extraction",
>       "started\_at": "2026-10-11T06:48:23.768277Z",
>       "state": "skipped",
>       "streaming": false,
>       "unused\_allowance": null,
>       "usage": \{
>         "cache\_read\_tokens": null,
>         "cache\_write\_tokens": null,
>         "input\_tokens": null,
>         "output\_tokens": null
>       \},
>       "versions": \{
>         "application": "vs5-v1",
>         "chunking": "source-locations-v1",
>         "extraction": "vs2-v1",
>         "model\_configuration": "controlled-response-v1",
>         "prompt": "controlled-vs3-v1",
>         "retrieval": "fixed-example-v1",
>         "schema\_version": "t2-v1"
>       \}
>     \},
>     \{
>       "actual\_response\_model\_id": null,
>       "artifact\_ids": \[\],
>       "attempt\_id": "2b970a30bd674821b10c7bb48aa72a5b",
>       "candidate\_passage\_ids": \[\],
>       "dispatched": true,
>       "duration\_seconds": 0.0,
>       "errors": \[\],
>       "event\_id": "ab6fd568774142b4a393606dcad5c25c",
>       "finished\_at": "2026-10-11T06:48:23.832899Z",
>       "first\_token\_seconds": null,
>       "job\_id": "eaaee2f2b8e4474db5e268d504b6b294",
>       "model\_id": null,
>       "operation": "internal",
>       "original\_processing\_event\_id": null,
>       "provider\_request\_id": null,
>       "retry\_index": 0,
>       "returned\_bytes": null,
>       "run\_id": "140f6e7a0bd7590fb2aa26a1a69e0eeb",
>       "selected\_passage\_ids": \[
>         "RBI-IT-2023:2023-11-07:19b",
>         "RBI-IT-2023:2023-11-07:2ai",
>         "RBI-IT-2023:2023-11-07:2b",
>         "47b99e978120442a99c94a0a0f00a13c-2"
>       \],
>       "selected\_text\_bytes": null,
>       "snapshot\_id": "140f6e7a0bd7590fb2aa26a1a69e0eeb",
>       "stage": "context\_selection",
>       "stage\_id": "context\_selection",
>       "started\_at": "2026-10-11T06:48:23.832899Z",
>       "state": "succeeded",
>       "streaming": false,
>       "unused\_allowance": null,
>       "usage": \{
>         "cache\_read\_tokens": null,
>         "cache\_write\_tokens": null,
>         "input\_tokens": null,
>         "output\_tokens": null
>       \},
>       "versions": \{
>         "application": "vs5-v1",
>         "chunking": "source-locations-v1",
>         "extraction": "vs2-v1",
>         "model\_configuration": "controlled-response-v1",
>         "prompt": "controlled-vs3-v1",
>         "retrieval": "fixed-example-v1",
>         "schema\_version": "t2-v1"
>       \}
>     \},
>     \{
>       "actual\_response\_model\_id": null,
>       "artifact\_ids": \[\],
>       "attempt\_id": "cc3eaabb804c4a94ae6d5abdffd709c3",
>       "candidate\_passage\_ids": \[\],
>       "dispatched": true,
>       "duration\_seconds": 0.01600000000325963,
>       "errors": \[\],
>       "event\_id": "c7d03f09b9774d728f021280ad90c637",
>       "finished\_at": "2026-10-11T06:48:23.971710Z",
>       "first\_token\_seconds": null,
>       "job\_id": "eaaee2f2b8e4474db5e268d504b6b294",
>       "model\_id": null,
>       "operation": "storage",
>       "original\_processing\_event\_id": null,
>       "provider\_request\_id": null,
>       "retry\_index": 0,
>       "returned\_bytes": null,
>       "run\_id": "140f6e7a0bd7590fb2aa26a1a69e0eeb",
>       "selected\_passage\_ids": \[\],
>       "selected\_text\_bytes": null,
>       "snapshot\_id": "140f6e7a0bd7590fb2aa26a1a69e0eeb",
>       "stage": "persistence",
>       "stage\_id": "persistence",
>       "started\_at": "2026-10-11T06:48:23.956897Z",
>       "state": "succeeded",
>       "streaming": false,
>       "unused\_allowance": null,
>       "usage": \{
>         "cache\_read\_tokens": null,
>         "cache\_write\_tokens": null,
>         "input\_tokens": null,
>         "output\_tokens": null
>       \},
>       "versions": \{
>         "application": "vs5-v1",
>         "chunking": "source-locations-v1",
>         "extraction": "vs2-v1",
>         "model\_configuration": "controlled-response-v1",
>         "prompt": "controlled-vs3-v1",
>         "retrieval": "fixed-example-v1",
>         "schema\_version": "t2-v1"
>       \}
>     \}
>   \]
> \}

## Unchecked obligations

> \[\]

## Source Version

> \{
>   "document": \{
>     "case\_id": "ad1d0bed7ca54770a00182b92fb707d8",
>     "document\_version\_id": "47b99e978120442a99c94a0a0f00a13c",
>     "effective\_date": null,
>     "kind": "policy",
>     "publication\_date": null,
>     "sha256": "e5b255e307bc926270d6a12c7499dce86350ab981325fd74264c344af32f9e6f",
>     "source\_id": "5a3d606c03364a6f8c9edc1f0b448c23",
>     "source\_url": null,
>     "storage\_reference": "47b99e978120442a99c94a0a0f00a13c",
>     "synthetic": true,
>     "version": "1"
>   \},
>   "filename": "policy.txt",
>   "format": "txt",
>   "passages": \[
>     \{
>       "document\_version\_id": "47b99e978120442a99c94a0a0f00a13c",
>       "location": "Line 1",
>       "passage\_id": "47b99e978120442a99c94a0a0f00a13c-1",
>       "text": "Synthetic demo. Fictional bank policy."
>     \},
>     \{
>       "document\_version\_id": "47b99e978120442a99c94a0a0f00a13c",
>       "location": "Line 2",
>       "passage\_id": "47b99e978120442a99c94a0a0f00a13c-2",
>       "text": "Control ACCESS-01 requires supervision of privileged sessions, complete activity logging, and a weekly review."
>     \},
>     \{
>       "document\_version\_id": "47b99e978120442a99c94a0a0f00a13c",
>       "location": "Line 3",
>       "passage\_id": "47b99e978120442a99c94a0a0f00a13c-3",
>       "text": "Weekly timing is bank policy, not an RBI-specified interval."
>     \}
>   \],
>   "units": 1,
>   "uploaded\_at": "2026-10-11T06:48:22.772289\+00:00"
> \}

## Source Version

> \{
>   "document": \{
>     "case\_id": "ad1d0bed7ca54770a00182b92fb707d8",
>     "document\_version\_id": "RBI-IT-2023:2023-11-07",
>     "kind": "regulation",
>     "sha256": "d742aece8d2b5d74240e83e4d2ec6150a57f2076c02a9c878528ad6c42151786",
>     "source\_id": "RBI-IT-2023",
>     "synthetic": false,
>     "version": "2023-11-07"
>   \},
>   "effective\_date": "2024-04-01",
>   "filename": "Master Direction on Information Technology Governance, Risk, Controls and Assurance Practices",
>   "format": "html",
>   "freshness": "unverified",
>   "passages": \[
>     \{
>       "document\_version\_id": "RBI-IT-2023:2023-11-07",
>       "location": "Clause 2(a)",
>       "passage\_id": "RBI-IT-2023:2023-11-07:2a",
>       "text": "These Directions shall be applicable to the following entities (collectively referred to as ‘regulated entities’ or ’REs’ in these directions):"
>     \},
>     \{
>       "document\_version\_id": "RBI-IT-2023:2023-11-07",
>       "location": "Clause 2(a)(i)",
>       "passage\_id": "RBI-IT-2023:2023-11-07:2ai",
>       "text": "all Banking Companies 1 , Corresponding New Banks and State Bank of India as defined under subsections (c), (da) and (nc) of section 5 of the Banking Regulation Act, 1949 (collectively referred to as ‘commercial banks’ hereinafter)."
>     \},
>     \{
>       "document\_version\_id": "RBI-IT-2023:2023-11-07",
>       "location": "Clause 2(b)",
>       "passage\_id": "RBI-IT-2023:2023-11-07:2b",
>       "text": "These Directions shall not be applicable to: Local Area Banks NBFC-Core Investment Companies"
>     \},
>     \{
>       "document\_version\_id": "RBI-IT-2023:2023-11-07",
>       "location": "Clause 19(a)",
>       "passage\_id": "RBI-IT-2023:2023-11-07:19a",
>       "text": "Access to information assets shall be allowed only where a valid business need exists. REs shall have documented standards and procedures, which are approved by the ITSC and kept up to date for administering need-based access to an information system."
>     \},
>     \{
>       "document\_version\_id": "RBI-IT-2023:2023-11-07",
>       "location": "Clause 19(b)",
>       "passage\_id": "RBI-IT-2023:2023-11-07:19b",
>       "text": "Personnel with elevated system access entitlements shall be closely supervised with all their systems activities logged and periodically reviewed."
>     \},
>     \{
>       "document\_version\_id": "RBI-IT-2023:2023-11-07",
>       "location": "Clause 19(c)",
>       "passage\_id": "RBI-IT-2023:2023-11-07:19c",
>       "text": "REs shall adopt multi-factor authentication for privileged users of i) critical information systems and ii) for critical activities, basis the RE’s risk assessment."
>     \},
>     \{
>       "document\_version\_id": "RBI-IT-2023:2023-11-07",
>       "location": "Clause 29(a)",
>       "passage\_id": "RBI-IT-2023:2023-11-07:29a",
>       "text": "Periodicity of DR drills for critical information systems shall be at least on a half-yearly basis and for other information systems, as per RE’s risk assessment."
>     \},
>     \{
>       "document\_version\_id": "RBI-IT-2023:2023-11-07",
>       "location": "Clause 29(b)",
>       "passage\_id": "RBI-IT-2023:2023-11-07:29b",
>       "text": "Any major issues observed during the DR drill shall be resolved and tested again to ensure successful conduct of drill before the next cycle."
>     \},
>     \{
>       "document\_version\_id": "RBI-IT-2023:2023-11-07",
>       "location": "Clause 29(e)",
>       "passage\_id": "RBI-IT-2023:2023-11-07:29e",
>       "text": "REs shall backup data and periodically restore such backed-up data to check its usability. The integrity of such backup data shall be preserved along with securing it from unauthorised access."
>     \}
>   \],
>   "publication\_date": "2023-11-07",
>   "source\_url": "https://www.rbi.org.in/Scripts/BS\_ViewMasDirections.aspx?id=12562"
> \}

## Limitations

> Controlled example only. No live model call occurred.
> Current regulatory status is unverified. This report does not certify bank compliance.
> A policy alone does not prove operational execution.
> Human approval measures review decisions, not assessment accuracy.
> Available token usage appears in recorded attempts. Inference and total system costs remain unknown.
> The observed job state is current. The report cutoff controls saved findings, reviews, and trace events.
