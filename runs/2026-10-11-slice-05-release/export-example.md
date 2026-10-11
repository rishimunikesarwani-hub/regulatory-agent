# The Regulator assessment report

## Export status

> Assessment export · Simulated processing · Fictional bank data

## Snapshot and selected versions

> \{
>   "assessment\_date": "2024-04-08",
>   "bank\_profile": \{
>     "name": "Fictional export bank 1791708138160"
>   \},
>   "case\_id": "7cb6d94782614730923140911f4000eb",
>   "mode": "historical",
>   "model\_version": "in.openai.gpt-5.6-luna",
>   "prompt\_version": "controlled-vs3-v1",
>   "selected\_document\_ids": \{\},
>   "selected\_obligations": \[
>     "RBI-IT-19b"
>   \],
>   "selected\_versions": \{
>     "036f71b76dc6455aaca264853f90ce1d": "1",
>     "RBI-IT-2023": "2023-11-07"
>   \},
>   "snapshot\_id": "56d085a0aa9c5629867d1cce3edbbec0",
>   "synthetic": true
> \}

## Cohort filters and time bases

> \{
>   "kind": "single\_assessment",
>   "case\_id": "7cb6d94782614730923140911f4000eb",
>   "run\_id": "56d085a0aa9c5629867d1cce3edbbec0",
>   "snapshot\_id": "56d085a0aa9c5629867d1cce3edbbec0",
>   "model\_id": "in.openai.gpt-5.6-luna",
>   "prompt\_version": "controlled-vs3-v1",
>   "data\_mode": "controlled\_simulation",
>   "recommendation\_availability": \{
>     "through": "2026-10-11T08:42:20.125204\+00:00",
>     "end\_inclusive": true
>   \},
>   "runtime\_selection": \{
>     "job\_id": "1795d80c671048d388ea04def6cad152",
>     "job\_admitted\_at": "2026-10-11T08:42:19.229579\+00:00",
>     "job\_state\_time\_basis": "observed\_current\_state"
>   \}
> \}

## Observed job state

> \{
>   "authority\_verified\_at": null,
>   "case\_id": "7cb6d94782614730923140911f4000eb",
>   "created\_at": 1791708139.229579,
>   "deadline": 1791708739.3129969,
>   "finished\_at": 1791708139.5784588,
>   "freshness": "unverified",
>   "job\_id": "1795d80c671048d388ea04def6cad152",
>   "label": "Simulated",
>   "model\_calls": 1,
>   "retrieval\_calls": 0,
>   "snapshot\_id": "56d085a0aa9c5629867d1cce3edbbec0",
>   "stage": "persistence",
>   "started\_at": 1791708139.3129969,
>   "state": "completed",
>   "stop\_reason": null,
>   "unchecked\_obligations": \[\]
> \}

## Report cutoff

> 2026-10-11T08:42:20.125204\+00:00

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
>       "document\_version\_id": "68858e1be8e540618a9d96f3cf7074a7",
>       "passage\_id": "68858e1be8e540618a9d96f3cf7074a7-2",
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
>         "document\_version\_id": "68858e1be8e540618a9d96f3cf7074a7",
>         "passage\_id": "68858e1be8e540618a9d96f3cf7074a7-2",
>         "location": "Line 2",
>         "quote": "Control ACCESS-01 requires supervision of privileged sessions, complete activity logging, and a weekly review."
>       \}
>     \]
>   \}
> \]

## Original findings and recommendation IDs

> \[
>   \{
>     "finding\_id": "3dac04990c2058c2ad3bfaffdaaf5bd8",
>     "snapshot\_id": "56d085a0aa9c5629867d1cce3edbbec0",
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
>         "document\_version\_id": "68858e1be8e540618a9d96f3cf7074a7",
>         "passage\_id": "68858e1be8e540618a9d96f3cf7074a7-2",
>         "location": "Line 2",
>         "quote": "Control ACCESS-01 requires supervision of privileged sessions, complete activity logging, and a weekly review."
>       \}
>     \],
>     "rationale": "Controlled example. The policy states a control, but this example has no verified operational evidence. Applicability and activity records need human review.",
>     "remedy": "Confirm applicability. Request dated session records, supervisor sign-offs, complete activity logs, and completed periodic reviews.",
>     "gap\_kind": "evidence",
>     "applicability\_reason": null,
>     "claims": \[\],
>     "run\_id": "56d085a0aa9c5629867d1cce3edbbec0",
>     "primary\_recommendation": "Confirm applicability. Request dated session records, supervisor sign-offs, complete activity logs, and completed periodic reviews.",
>     "available\_at": "2026-10-11T08:42:19.531461Z",
>     "model\_id": "in.openai.gpt-5.6-luna",
>     "prompt\_version": "controlled-vs3-v1",
>     "data\_mode": "controlled\_simulation",
>     "source\_version\_ids": \[
>       "036f71b76dc6455aaca264853f90ce1d:1",
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
>     "idempotency\_key": "59b0e364-f489-451b-affd-ef1bc72d7edd",
>     "event\_id": "cedb6d608b0f401ab7e1c4b4c9b103f4",
>     "finding\_id": "3dac04990c2058c2ad3bfaffdaaf5bd8",
>     "reviewer\_id": "slice-05-tests",
>     "committed\_at": "2026-10-11T08:42:20.090455Z",
>     "revision": 1
>   \}
> \]

## Review summary

metric_definition_version: d24-v1

cutoff: 2026-10-11T08:42:20.125204+00:00

data_mode: controlled_simulation

run_id: 56d085a0aa9c5629867d1cce3edbbec0

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
>   "run\_id": "56d085a0aa9c5629867d1cce3edbbec0",
>   "attempts": \[
>     \{
>       "actual\_response\_model\_id": null,
>       "artifact\_ids": \[
>         "cedb6d608b0f401ab7e1c4b4c9b103f4"
>       \],
>       "attempt\_id": "f026872b4ae14f86bac4eb8b4f90cfbb",
>       "candidate\_passage\_ids": \[\],
>       "dispatched": true,
>       "duration\_seconds": 0.014999999984866008,
>       "errors": \[\],
>       "event\_id": "01d39717889c42d09ca1d0a4e28a48d8",
>       "finished\_at": "2026-10-11T08:42:20.102577Z",
>       "first\_token\_seconds": null,
>       "job\_id": "1795d80c671048d388ea04def6cad152",
>       "model\_id": null,
>       "operation": "storage",
>       "original\_processing\_event\_id": null,
>       "provider\_request\_id": null,
>       "retry\_index": 0,
>       "returned\_bytes": null,
>       "run\_id": "56d085a0aa9c5629867d1cce3edbbec0",
>       "selected\_passage\_ids": \[\],
>       "selected\_text\_bytes": null,
>       "snapshot\_id": "56d085a0aa9c5629867d1cce3edbbec0",
>       "stage": "review\_event",
>       "stage\_id": "review\_event",
>       "started\_at": "2026-10-11T08:42:20.089446Z",
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
>       "attempt\_id": "2179aafe3d79432bb9ff3fdc26b292ba",
>       "candidate\_passage\_ids": \[
>         "68858e1be8e540618a9d96f3cf7074a7-1",
>         "68858e1be8e540618a9d96f3cf7074a7-2",
>         "68858e1be8e540618a9d96f3cf7074a7-3",
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
>       "event\_id": "0dc9c82d229949f2bb6553e32c575762",
>       "finished\_at": "2026-10-11T08:42:19.377581Z",
>       "first\_token\_seconds": null,
>       "job\_id": "1795d80c671048d388ea04def6cad152",
>       "model\_id": null,
>       "operation": "retrieval",
>       "original\_processing\_event\_id": null,
>       "provider\_request\_id": null,
>       "retry\_index": 0,
>       "returned\_bytes": null,
>       "run\_id": "56d085a0aa9c5629867d1cce3edbbec0",
>       "selected\_passage\_ids": \[
>         "RBI-IT-2023:2023-11-07:19b",
>         "RBI-IT-2023:2023-11-07:2ai",
>         "RBI-IT-2023:2023-11-07:2b",
>         "68858e1be8e540618a9d96f3cf7074a7-2"
>       \],
>       "selected\_text\_bytes": null,
>       "snapshot\_id": "56d085a0aa9c5629867d1cce3edbbec0",
>       "stage": "retrieval",
>       "stage\_id": "retrieval",
>       "started\_at": "2026-10-11T08:42:19.377581Z",
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
>       "attempt\_id": "663a59d9917440a58c3608f4aed2a45b",
>       "candidate\_passage\_ids": \[\],
>       "dispatched": true,
>       "duration\_seconds": 0.030999999988125637,
>       "errors": \[\],
>       "event\_id": "1cf2dafc749244d29d1e1c76f06a40bf",
>       "finished\_at": "2026-10-11T08:42:19.480154Z",
>       "first\_token\_seconds": null,
>       "job\_id": "1795d80c671048d388ea04def6cad152",
>       "model\_id": "in.openai.gpt-5.6-luna",
>       "operation": "model",
>       "original\_processing\_event\_id": null,
>       "provider\_request\_id": null,
>       "retry\_index": 0,
>       "returned\_bytes": null,
>       "run\_id": "56d085a0aa9c5629867d1cce3edbbec0",
>       "selected\_passage\_ids": \[\],
>       "selected\_text\_bytes": null,
>       "snapshot\_id": "56d085a0aa9c5629867d1cce3edbbec0",
>       "stage": "model\_call",
>       "stage\_id": "model\_call",
>       "started\_at": "2026-10-11T08:42:19.448616Z",
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
>       "attempt\_id": "9f59302397264efbaee773cddc82b4a8",
>       "candidate\_passage\_ids": \[\],
>       "dispatched": true,
>       "duration\_seconds": 0.0,
>       "errors": \[\],
>       "event\_id": "700b105a721f4778ab1a107554ff8fbf",
>       "finished\_at": "2026-10-11T08:42:19.327225Z",
>       "first\_token\_seconds": null,
>       "job\_id": "1795d80c671048d388ea04def6cad152",
>       "model\_id": null,
>       "operation": "internal",
>       "original\_processing\_event\_id": null,
>       "provider\_request\_id": null,
>       "retry\_index": 0,
>       "returned\_bytes": null,
>       "run\_id": "56d085a0aa9c5629867d1cce3edbbec0",
>       "selected\_passage\_ids": \[\],
>       "selected\_text\_bytes": null,
>       "snapshot\_id": "56d085a0aa9c5629867d1cce3edbbec0",
>       "stage": "source\_verification",
>       "stage\_id": "source\_verification",
>       "started\_at": "2026-10-11T08:42:19.324998Z",
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
>       "attempt\_id": "b96efd3a62fe4ac582e0386805c94dff",
>       "candidate\_passage\_ids": \[\],
>       "dispatched": true,
>       "duration\_seconds": 0.0159999999741558,
>       "errors": \[\],
>       "event\_id": "98bdaaba1d07407ebc3d7b05930ef915",
>       "finished\_at": "2026-10-11T08:42:19.540459Z",
>       "first\_token\_seconds": null,
>       "job\_id": "1795d80c671048d388ea04def6cad152",
>       "model\_id": null,
>       "operation": "storage",
>       "original\_processing\_event\_id": null,
>       "provider\_request\_id": null,
>       "retry\_index": 0,
>       "returned\_bytes": null,
>       "run\_id": "56d085a0aa9c5629867d1cce3edbbec0",
>       "selected\_passage\_ids": \[\],
>       "selected\_text\_bytes": null,
>       "snapshot\_id": "56d085a0aa9c5629867d1cce3edbbec0",
>       "stage": "persistence",
>       "stage\_id": "persistence",
>       "started\_at": "2026-10-11T08:42:19.529462Z",
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
>       "attempt\_id": "db8d1f082e4c4140929869fc1ac6b7f3",
>       "candidate\_passage\_ids": \[\],
>       "dispatched": true,
>       "duration\_seconds": 0.0,
>       "errors": \[\],
>       "event\_id": "a9d1242fa57b4a5ba79dca2e9580416d",
>       "finished\_at": "2026-10-11T08:42:19.396621Z",
>       "first\_token\_seconds": null,
>       "job\_id": "1795d80c671048d388ea04def6cad152",
>       "model\_id": null,
>       "operation": "internal",
>       "original\_processing\_event\_id": null,
>       "provider\_request\_id": null,
>       "retry\_index": 0,
>       "returned\_bytes": null,
>       "run\_id": "56d085a0aa9c5629867d1cce3edbbec0",
>       "selected\_passage\_ids": \[
>         "RBI-IT-2023:2023-11-07:19b",
>         "RBI-IT-2023:2023-11-07:2ai",
>         "RBI-IT-2023:2023-11-07:2b",
>         "68858e1be8e540618a9d96f3cf7074a7-2"
>       \],
>       "selected\_text\_bytes": null,
>       "snapshot\_id": "56d085a0aa9c5629867d1cce3edbbec0",
>       "stage": "context\_selection",
>       "stage\_id": "context\_selection",
>       "started\_at": "2026-10-11T08:42:19.396621Z",
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
>       "attempt\_id": "1468b9399d1644698a54d6ac1eb355b3",
>       "candidate\_passage\_ids": \[\],
>       "dispatched": true,
>       "duration\_seconds": 0.0,
>       "errors": \[\],
>       "event\_id": "e03a1e556fed4d6081037899b8a1814d",
>       "finished\_at": "2026-10-11T08:42:19.509459Z",
>       "first\_token\_seconds": null,
>       "job\_id": "1795d80c671048d388ea04def6cad152",
>       "model\_id": null,
>       "operation": "internal",
>       "original\_processing\_event\_id": null,
>       "provider\_request\_id": null,
>       "retry\_index": 0,
>       "returned\_bytes": null,
>       "run\_id": "56d085a0aa9c5629867d1cce3edbbec0",
>       "selected\_passage\_ids": \[\],
>       "selected\_text\_bytes": null,
>       "snapshot\_id": "56d085a0aa9c5629867d1cce3edbbec0",
>       "stage": "validation",
>       "stage\_id": "validation",
>       "started\_at": "2026-10-11T08:42:19.509459Z",
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
>         "68858e1be8e540618a9d96f3cf7074a7"
>       \],
>       "attempt\_id": "92fe3a5ced9443b2aa86a04c664a9819",
>       "candidate\_passage\_ids": \[\],
>       "dispatched": false,
>       "duration\_seconds": 0.0,
>       "errors": \[\],
>       "event\_id": "ed3b357ca736449a914a68a18edde14c",
>       "finished\_at": "2026-10-11T08:42:19.353297Z",
>       "first\_token\_seconds": null,
>       "job\_id": "1795d80c671048d388ea04def6cad152",
>       "model\_id": null,
>       "operation": "internal",
>       "original\_processing\_event\_id": "68858e1be8e540618a9d96f3cf7074a7",
>       "provider\_request\_id": null,
>       "retry\_index": 0,
>       "returned\_bytes": null,
>       "run\_id": "56d085a0aa9c5629867d1cce3edbbec0",
>       "selected\_passage\_ids": \[\],
>       "selected\_text\_bytes": null,
>       "snapshot\_id": "56d085a0aa9c5629867d1cce3edbbec0",
>       "stage": "extraction",
>       "stage\_id": "extraction",
>       "started\_at": "2026-10-11T08:42:19.353297Z",
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
>     \}
>   \]
> \}

## Unchecked obligations

> \[\]

## Source Version

> \{
>   "document": \{
>     "case\_id": "7cb6d94782614730923140911f4000eb",
>     "document\_version\_id": "68858e1be8e540618a9d96f3cf7074a7",
>     "effective\_date": null,
>     "kind": "policy",
>     "publication\_date": null,
>     "sha256": "e5b255e307bc926270d6a12c7499dce86350ab981325fd74264c344af32f9e6f",
>     "source\_id": "036f71b76dc6455aaca264853f90ce1d",
>     "source\_url": null,
>     "storage\_reference": "68858e1be8e540618a9d96f3cf7074a7",
>     "synthetic": true,
>     "version": "1"
>   \},
>   "filename": "policy.txt",
>   "format": "txt",
>   "passages": \[
>     \{
>       "document\_version\_id": "68858e1be8e540618a9d96f3cf7074a7",
>       "location": "Line 1",
>       "passage\_id": "68858e1be8e540618a9d96f3cf7074a7-1",
>       "text": "Synthetic demo. Fictional bank policy."
>     \},
>     \{
>       "document\_version\_id": "68858e1be8e540618a9d96f3cf7074a7",
>       "location": "Line 2",
>       "passage\_id": "68858e1be8e540618a9d96f3cf7074a7-2",
>       "text": "Control ACCESS-01 requires supervision of privileged sessions, complete activity logging, and a weekly review."
>     \},
>     \{
>       "document\_version\_id": "68858e1be8e540618a9d96f3cf7074a7",
>       "location": "Line 3",
>       "passage\_id": "68858e1be8e540618a9d96f3cf7074a7-3",
>       "text": "Weekly timing is bank policy, not an RBI-specified interval."
>     \}
>   \],
>   "units": 1,
>   "uploaded\_at": "2026-10-11T08:42:18.945712\+00:00"
> \}

## Source Version

> \{
>   "document": \{
>     "case\_id": "7cb6d94782614730923140911f4000eb",
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
