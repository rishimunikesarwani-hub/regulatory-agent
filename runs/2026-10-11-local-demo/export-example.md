# The Regulator assessment report

## Export status

> Assessment export · Simulated processing · Fictional bank data

## Snapshot and selected versions

> \{
>   "assessment\_date": "2024-04-08",
>   "bank\_profile": \{
>     "name": "Fictional export bank 1791722267705"
>   \},
>   "case\_id": "2d64fc9f6665445eb48b7d605b77635d",
>   "mode": "historical",
>   "model\_version": "in.openai.gpt-5.6-luna",
>   "prompt\_version": "controlled-vs3-v1",
>   "selected\_document\_ids": \{\},
>   "selected\_obligations": \[
>     "RBI-IT-19b"
>   \],
>   "selected\_versions": \{
>     "85e7822efa754730a5e0caeef1fc430e": "1",
>     "RBI-IT-2023": "2023-11-07"
>   \},
>   "snapshot\_id": "9b0decf809855cfcb29d2e61dae94ae8",
>   "synthetic": true
> \}

## Cohort filters and time bases

> \{
>   "kind": "single\_assessment",
>   "case\_id": "2d64fc9f6665445eb48b7d605b77635d",
>   "run\_id": "9b0decf809855cfcb29d2e61dae94ae8",
>   "snapshot\_id": "9b0decf809855cfcb29d2e61dae94ae8",
>   "model\_id": "in.openai.gpt-5.6-luna",
>   "prompt\_version": "controlled-vs3-v1",
>   "data\_mode": "controlled\_simulation",
>   "recommendation\_availability": \{
>     "through": "2026-10-11T12:37:50.334406\+00:00",
>     "end\_inclusive": true
>   \},
>   "runtime\_selection": \{
>     "job\_id": "90c32e0e24a2441db8c1411beaf5fe08",
>     "job\_admitted\_at": "2026-10-11T12:37:49.336310\+00:00",
>     "job\_state\_time\_basis": "observed\_current\_state"
>   \}
> \}

## Observed job state

> \{
>   "authority\_verified\_at": null,
>   "case\_id": "2d64fc9f6665445eb48b7d605b77635d",
>   "created\_at": 1791722269.33631,
>   "deadline": 1791722869.3891416,
>   "finished\_at": 1791722269.8374074,
>   "freshness": "unverified",
>   "job\_id": "90c32e0e24a2441db8c1411beaf5fe08",
>   "label": "Simulated",
>   "model\_calls": 1,
>   "retrieval\_calls": 0,
>   "snapshot\_id": "9b0decf809855cfcb29d2e61dae94ae8",
>   "stage": "persistence",
>   "started\_at": 1791722269.3891416,
>   "state": "completed",
>   "stop\_reason": null,
>   "unchecked\_obligations": \[\]
> \}

## Report cutoff

> 2026-10-11T12:37:50.334406\+00:00

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
>       "document\_version\_id": "52479b02448a4d83ab79f75f31b91928",
>       "passage\_id": "52479b02448a4d83ab79f75f31b91928-2",
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
>         "document\_version\_id": "52479b02448a4d83ab79f75f31b91928",
>         "passage\_id": "52479b02448a4d83ab79f75f31b91928-2",
>         "location": "Line 2",
>         "quote": "Control ACCESS-01 requires supervision of privileged sessions, complete activity logging, and a weekly review."
>       \}
>     \]
>   \}
> \]

## Original findings and recommendation IDs

> \[
>   \{
>     "finding\_id": "deaf8eee13b85c6d87157f82d26f60ec",
>     "snapshot\_id": "9b0decf809855cfcb29d2e61dae94ae8",
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
>         "document\_version\_id": "52479b02448a4d83ab79f75f31b91928",
>         "passage\_id": "52479b02448a4d83ab79f75f31b91928-2",
>         "location": "Line 2",
>         "quote": "Control ACCESS-01 requires supervision of privileged sessions, complete activity logging, and a weekly review."
>       \}
>     \],
>     "rationale": "Controlled example. The policy states a control, but this example has no verified operational evidence. Applicability and activity records need human review.",
>     "remedy": "Confirm applicability. Request dated session records, supervisor sign-offs, complete activity logs, and completed periodic reviews.",
>     "gap\_kind": "evidence",
>     "applicability\_reason": null,
>     "claims": \[\],
>     "run\_id": "9b0decf809855cfcb29d2e61dae94ae8",
>     "primary\_recommendation": "Confirm applicability. Request dated session records, supervisor sign-offs, complete activity logs, and completed periodic reviews.",
>     "available\_at": "2026-10-11T12:37:49.793894Z",
>     "model\_id": "in.openai.gpt-5.6-luna",
>     "prompt\_version": "controlled-vs3-v1",
>     "data\_mode": "controlled\_simulation",
>     "source\_version\_ids": \[
>       "85e7822efa754730a5e0caeef1fc430e:1",
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
>     "idempotency\_key": "fa8ded56-d80e-489d-b2f4-0ca5522ff76d",
>     "event\_id": "f56fc72eda7044278985c841fedf600c",
>     "finding\_id": "deaf8eee13b85c6d87157f82d26f60ec",
>     "reviewer\_id": "slice-05-tests",
>     "committed\_at": "2026-10-11T12:37:50.277841Z",
>     "revision": 1
>   \}
> \]

## Review summary

metric_definition_version: d24-v1

cutoff: 2026-10-11T12:37:50.334406+00:00

data_mode: controlled_simulation

run_id: 9b0decf809855cfcb29d2e61dae94ae8

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
>   "run\_id": "9b0decf809855cfcb29d2e61dae94ae8",
>   "attempts": \[
>     \{
>       "actual\_response\_model\_id": null,
>       "artifact\_ids": \[\],
>       "attempt\_id": "17fbd0e5a3aa4a41ad0d1ad2a1435e46",
>       "candidate\_passage\_ids": \[\],
>       "dispatched": true,
>       "duration\_seconds": 0.015000000013969839,
>       "errors": \[\],
>       "event\_id": "5e345650711846eebc5242d492d21f95",
>       "finished\_at": "2026-10-11T12:37:49.425225Z",
>       "first\_token\_seconds": null,
>       "job\_id": "90c32e0e24a2441db8c1411beaf5fe08",
>       "model\_id": null,
>       "operation": "internal",
>       "original\_processing\_event\_id": null,
>       "provider\_request\_id": null,
>       "retry\_index": 0,
>       "returned\_bytes": null,
>       "run\_id": "9b0decf809855cfcb29d2e61dae94ae8",
>       "selected\_passage\_ids": \[\],
>       "selected\_text\_bytes": null,
>       "snapshot\_id": "9b0decf809855cfcb29d2e61dae94ae8",
>       "stage": "source\_verification",
>       "stage\_id": "source\_verification",
>       "started\_at": "2026-10-11T12:37:49.421158Z",
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
>       "attempt\_id": "391cc017c5634387a4d85008e42f77b5",
>       "candidate\_passage\_ids": \[\],
>       "dispatched": true,
>       "duration\_seconds": 0.015000000013969839,
>       "errors": \[\],
>       "event\_id": "72ed74d2ccc34f36991fb5f2cb0dd0c7",
>       "finished\_at": "2026-10-11T12:37:49.803949Z",
>       "first\_token\_seconds": null,
>       "job\_id": "90c32e0e24a2441db8c1411beaf5fe08",
>       "model\_id": null,
>       "operation": "storage",
>       "original\_processing\_event\_id": null,
>       "provider\_request\_id": null,
>       "retry\_index": 0,
>       "returned\_bytes": null,
>       "run\_id": "9b0decf809855cfcb29d2e61dae94ae8",
>       "selected\_passage\_ids": \[\],
>       "selected\_text\_bytes": null,
>       "snapshot\_id": "9b0decf809855cfcb29d2e61dae94ae8",
>       "stage": "persistence",
>       "stage\_id": "persistence",
>       "started\_at": "2026-10-11T12:37:49.789808Z",
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
>       "attempt\_id": "742496dcfb6a457cbd13a341a12ae5cb",
>       "candidate\_passage\_ids": \[
>         "52479b02448a4d83ab79f75f31b91928-1",
>         "52479b02448a4d83ab79f75f31b91928-2",
>         "52479b02448a4d83ab79f75f31b91928-3",
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
>       "event\_id": "918458d15e7141598549a0ee0ce9bcf4",
>       "finished\_at": "2026-10-11T12:37:49.594949Z",
>       "first\_token\_seconds": null,
>       "job\_id": "90c32e0e24a2441db8c1411beaf5fe08",
>       "model\_id": null,
>       "operation": "retrieval",
>       "original\_processing\_event\_id": null,
>       "provider\_request\_id": null,
>       "retry\_index": 0,
>       "returned\_bytes": null,
>       "run\_id": "9b0decf809855cfcb29d2e61dae94ae8",
>       "selected\_passage\_ids": \[
>         "RBI-IT-2023:2023-11-07:19b",
>         "RBI-IT-2023:2023-11-07:2ai",
>         "RBI-IT-2023:2023-11-07:2b",
>         "52479b02448a4d83ab79f75f31b91928-2"
>       \],
>       "selected\_text\_bytes": null,
>       "snapshot\_id": "9b0decf809855cfcb29d2e61dae94ae8",
>       "stage": "retrieval",
>       "stage\_id": "retrieval",
>       "started\_at": "2026-10-11T12:37:49.594949Z",
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
>       "attempt\_id": "f74c92407657497c8505a040d032e5d7",
>       "candidate\_passage\_ids": \[\],
>       "dispatched": true,
>       "duration\_seconds": 0.0,
>       "errors": \[\],
>       "event\_id": "a1e9370fbc0940f1afc989850a108d88",
>       "finished\_at": "2026-10-11T12:37:49.670329Z",
>       "first\_token\_seconds": null,
>       "job\_id": "90c32e0e24a2441db8c1411beaf5fe08",
>       "model\_id": null,
>       "operation": "internal",
>       "original\_processing\_event\_id": null,
>       "provider\_request\_id": null,
>       "retry\_index": 0,
>       "returned\_bytes": null,
>       "run\_id": "9b0decf809855cfcb29d2e61dae94ae8",
>       "selected\_passage\_ids": \[
>         "RBI-IT-2023:2023-11-07:19b",
>         "RBI-IT-2023:2023-11-07:2ai",
>         "RBI-IT-2023:2023-11-07:2b",
>         "52479b02448a4d83ab79f75f31b91928-2"
>       \],
>       "selected\_text\_bytes": null,
>       "snapshot\_id": "9b0decf809855cfcb29d2e61dae94ae8",
>       "stage": "context\_selection",
>       "stage\_id": "context\_selection",
>       "started\_at": "2026-10-11T12:37:49.670329Z",
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
>         "f56fc72eda7044278985c841fedf600c"
>       \],
>       "attempt\_id": "455bd5ce239c46ea87dd8b2d4bb16a44",
>       "candidate\_passage\_ids": \[\],
>       "dispatched": true,
>       "duration\_seconds": 0.0159999999741558,
>       "errors": \[\],
>       "event\_id": "ab48eb9063f9479fb4e3002d6adcfdeb",
>       "finished\_at": "2026-10-11T12:37:50.289812Z",
>       "first\_token\_seconds": null,
>       "job\_id": "90c32e0e24a2441db8c1411beaf5fe08",
>       "model\_id": null,
>       "operation": "storage",
>       "original\_processing\_event\_id": null,
>       "provider\_request\_id": null,
>       "retry\_index": 0,
>       "returned\_bytes": null,
>       "run\_id": "9b0decf809855cfcb29d2e61dae94ae8",
>       "selected\_passage\_ids": \[\],
>       "selected\_text\_bytes": null,
>       "snapshot\_id": "9b0decf809855cfcb29d2e61dae94ae8",
>       "stage": "review\_event",
>       "stage\_id": "review\_event",
>       "started\_at": "2026-10-11T12:37:50.275824Z",
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
>         "52479b02448a4d83ab79f75f31b91928"
>       \],
>       "attempt\_id": "295bf8e7a5bc47e9ac4433a7bfd2ff3c",
>       "candidate\_passage\_ids": \[\],
>       "dispatched": false,
>       "duration\_seconds": 0.0,
>       "errors": \[\],
>       "event\_id": "bbd0cfb9df67431ea6ddd9403349519a",
>       "finished\_at": "2026-10-11T12:37:49.500488Z",
>       "first\_token\_seconds": null,
>       "job\_id": "90c32e0e24a2441db8c1411beaf5fe08",
>       "model\_id": null,
>       "operation": "internal",
>       "original\_processing\_event\_id": "52479b02448a4d83ab79f75f31b91928",
>       "provider\_request\_id": null,
>       "retry\_index": 0,
>       "returned\_bytes": null,
>       "run\_id": "9b0decf809855cfcb29d2e61dae94ae8",
>       "selected\_passage\_ids": \[\],
>       "selected\_text\_bytes": null,
>       "snapshot\_id": "9b0decf809855cfcb29d2e61dae94ae8",
>       "stage": "extraction",
>       "stage\_id": "extraction",
>       "started\_at": "2026-10-11T12:37:49.500488Z",
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
>       "attempt\_id": "fcfc19b3897d49d7921fae440a9fed97",
>       "candidate\_passage\_ids": \[\],
>       "dispatched": true,
>       "duration\_seconds": 0.014999999984866008,
>       "errors": \[\],
>       "event\_id": "bc8db6aa90dc484aa57dbc56ade0c52e",
>       "finished\_at": "2026-10-11T12:37:49.734432Z",
>       "first\_token\_seconds": null,
>       "job\_id": "90c32e0e24a2441db8c1411beaf5fe08",
>       "model\_id": "in.openai.gpt-5.6-luna",
>       "operation": "model",
>       "original\_processing\_event\_id": null,
>       "provider\_request\_id": null,
>       "retry\_index": 0,
>       "returned\_bytes": null,
>       "run\_id": "9b0decf809855cfcb29d2e61dae94ae8",
>       "selected\_passage\_ids": \[\],
>       "selected\_text\_bytes": null,
>       "snapshot\_id": "9b0decf809855cfcb29d2e61dae94ae8",
>       "stage": "model\_call",
>       "stage\_id": "model\_call",
>       "started\_at": "2026-10-11T12:37:49.710743Z",
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
>       "attempt\_id": "06b020fc2ef64b60aa5d7bae737f10d8",
>       "candidate\_passage\_ids": \[\],
>       "dispatched": true,
>       "duration\_seconds": 0.0,
>       "errors": \[\],
>       "event\_id": "d71b49cda73345939aabf110089cb345",
>       "finished\_at": "2026-10-11T12:37:49.761734Z",
>       "first\_token\_seconds": null,
>       "job\_id": "90c32e0e24a2441db8c1411beaf5fe08",
>       "model\_id": null,
>       "operation": "internal",
>       "original\_processing\_event\_id": null,
>       "provider\_request\_id": null,
>       "retry\_index": 0,
>       "returned\_bytes": null,
>       "run\_id": "9b0decf809855cfcb29d2e61dae94ae8",
>       "selected\_passage\_ids": \[\],
>       "selected\_text\_bytes": null,
>       "snapshot\_id": "9b0decf809855cfcb29d2e61dae94ae8",
>       "stage": "validation",
>       "stage\_id": "validation",
>       "started\_at": "2026-10-11T12:37:49.761734Z",
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
>     "case\_id": "2d64fc9f6665445eb48b7d605b77635d",
>     "document\_version\_id": "52479b02448a4d83ab79f75f31b91928",
>     "effective\_date": null,
>     "kind": "policy",
>     "publication\_date": null,
>     "sha256": "e5b255e307bc926270d6a12c7499dce86350ab981325fd74264c344af32f9e6f",
>     "source\_id": "85e7822efa754730a5e0caeef1fc430e",
>     "source\_url": null,
>     "storage\_reference": "52479b02448a4d83ab79f75f31b91928",
>     "synthetic": true,
>     "version": "1"
>   \},
>   "filename": "policy.txt",
>   "format": "txt",
>   "passages": \[
>     \{
>       "document\_version\_id": "52479b02448a4d83ab79f75f31b91928",
>       "location": "Line 1",
>       "passage\_id": "52479b02448a4d83ab79f75f31b91928-1",
>       "text": "Synthetic demo. Fictional bank policy."
>     \},
>     \{
>       "document\_version\_id": "52479b02448a4d83ab79f75f31b91928",
>       "location": "Line 2",
>       "passage\_id": "52479b02448a4d83ab79f75f31b91928-2",
>       "text": "Control ACCESS-01 requires supervision of privileged sessions, complete activity logging, and a weekly review."
>     \},
>     \{
>       "document\_version\_id": "52479b02448a4d83ab79f75f31b91928",
>       "location": "Line 3",
>       "passage\_id": "52479b02448a4d83ab79f75f31b91928-3",
>       "text": "Weekly timing is bank policy, not an RBI-specified interval."
>     \}
>   \],
>   "units": 1,
>   "uploaded\_at": "2026-10-11T12:37:48.597669\+00:00"
> \}

## Source Version

> \{
>   "document": \{
>     "case\_id": "2d64fc9f6665445eb48b7d605b77635d",
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
