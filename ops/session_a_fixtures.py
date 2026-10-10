"""Inspect and validate T1 fixtures. This is not an assessment service."""

import argparse
from collections import Counter
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = (
    "data/sources/rbi-it-governance-2023.html",
    "data/sources/rbi-it-governance-2023-excerpts.txt",
    "data/sources/source-manifest.json",
    "data/fixtures/development-inputs.json",
    "data/fixtures/development-labels.json",
    "evals/fixtures/held-out-inputs.json",
    "evals/fixtures/held-out-labels.json",
)
CRITICAL = {"EVAL-09", "EVAL-10", "EVAL-17", "EVAL-18", "EVAL-19", "EVAL-20"}
STATUSES = {"supported", "partial", "gap", "needs_review", "not_applicable"}


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_pack(root=ROOT):
    pack = {"sources": read_json(root / FILES[2]), "inputs": {}, "labels": {}}
    for split, prefix in (("development", "data/fixtures/development"),
                          ("held_out", "evals/fixtures/held-out")):
        for kind in ("inputs", "labels"):
            pack[kind][split] = read_json(root / f"{prefix}-{kind}.json")["cases"]
    return pack


def resolve_reference(case, sources, reference):
    """Resolve only the stated owner, case, selected version, and exact quote."""
    if any(reference.get(key) != case[key] for key in ("owner_id", "case_id")):
        raise ValueError("citation owner/case denied")
    doc_id, version = reference.get("document_id"), reference.get("version_id")
    if case["selected_versions"].get(doc_id) != version:
        raise ValueError("citation version denied")
    candidates = [*case["documents"], *sources["versions"]]
    matches = [d for d in candidates if d["document_id"] == doc_id and d["version_id"] == version]
    if len(matches) != 1:
        raise ValueError("citation document absent or ambiguous")
    document = matches[0]
    if "case_id" in document and any(document[key] != case[key] for key in ("case_id", "owner_id")):
        raise ValueError("citation document scope denied")
    passages = [p for p in document["passages"] if p["passage_id"] == reference.get("passage_id")]
    if len(passages) != 1:
        raise ValueError("citation passage absent or ambiguous")
    passage = passages[0]
    if passage["text"] != reference.get("quote") or passage["locator"] != reference.get("locator"):
        raise ValueError("citation quote or locator mismatch")
    return passage


def answer_keys(value):
    if isinstance(value, dict):
        for key, item in value.items():
            if key.startswith("expected_") or key in {
                "rationale", "allowed_references", "required_elements", "minimum_change",
                "critical_tags", "gold_answer", "answer", "label_status",
            }:
                yield key
            yield from answer_keys(item)
    elif isinstance(value, list):
        for item in value:
            yield from answer_keys(item)


def validate_pack(pack):
    """Check the fixture contract. Human source/meaning review remains required."""
    errors = []
    sources = pack["sources"]
    if sources["current_coverage_verified"] is not False or sources["provider"] is not None:
        errors.append("current coverage/provider must remain unverified in this historical pack")
    versions = sources["versions"]
    version_keys = [(v["document_id"], v["version_id"]) for v in versions]
    if len(version_keys) != len(set(version_keys)):
        errors.append("duplicate source versions")
    for version in versions:
        if version["synthetic"] and (version["label"] != "Synthetic regulatory simulation"
                                      or version["source_url"] is not None):
            errors.append("simulation label or source URL is invalid")
        passage_ids = [p["passage_id"] for p in version["passages"]]
        if len(passage_ids) != len(set(passage_ids)):
            errors.append("duplicate source passage")
    all_ids = []
    for split in ("development", "held_out"):
        cases, answers = pack["inputs"][split], pack["labels"][split]
        ids = [c["case_id"] for c in cases]
        all_ids.extend(ids)
        if len(ids) != len(set(ids)):
            errors.append(f"{split}: duplicate case IDs")
        expected_ids = ({f"DEV-{n:02}" for n in range(1, 4)} if split == "development"
                        else {f"EVAL-{n:02}" for n in range(1, 21)})
        if set(ids) != expected_ids:
            errors.append(f"{split}: split IDs must match " +
                          ("DEV-01 through DEV-03" if split == "development" else "EVAL-01 through EVAL-20"))
        if sorted(a["case_id"] for a in answers) != sorted(ids):
            errors.append(f"{split}: label IDs do not match inputs")
        by_id = {a["case_id"]: a for a in answers}
        for case in cases:
            identity = case["case_id"]
            if case["split"] != split:
                errors.append(f"{identity}: split mismatch")
            if list(answer_keys(case)):
                errors.append(f"{identity}: answer leakage in input keys")
            for record in (case, case["profile"], *case["documents"]):
                if record.get("synthetic") is not True or record.get("label") != "Synthetic demo":
                    errors.append(f"{identity}: fictional bank label missing")
            docs = case["documents"]
            if len({d["document_id"] for d in docs}) != len(docs):
                errors.append(f"{identity}: duplicate document IDs")
            for doc in docs:
                if any(doc[key] != case[key] for key in ("owner_id", "case_id")):
                    errors.append(f"{identity}: document scope mismatch")
                if case["selected_versions"].get(doc["document_id"]) != doc["version_id"]:
                    errors.append(f"{identity}: document version not selected")
                for passage in doc["passages"]:
                    if not passage["text"].startswith("Synthetic demo."):
                        errors.append(f"{identity}: fictional bank passage label missing")
            known = {(d["document_id"], d["version_id"]) for d in [*docs, *versions]}
            if any(pair not in known for pair in case["selected_versions"].items()):
                errors.append(f"{identity}: selected version absent")
            selected_rules = [v for v in versions if case["selected_versions"].get(v["document_id"]) == v["version_id"]]
            if not selected_rules:
                errors.append(f"{identity}: selected rule absent")
            if any(v["effective_date"] > case["assessment_as_of"] for v in selected_rules):
                errors.append(f"{identity}: selected rule is not yet effective")
            if not case["assessment_period"]["start"] <= case["assessment_period"]["end"] <= case["assessment_as_of"]:
                errors.append(f"{identity}: assessment date precedes completed period")
            event = case.get("change_event")
            if event and (event["label"] != "Synthetic regulatory simulation" or
                          any((event["document_id"], event[k]) not in known
                              for k in ("previous_version", "candidate_version"))):
                errors.append(f"{identity}: simulation change versions invalid")
            for proposed in case["untrusted_proposed_references"]:
                try:
                    resolve_reference(case, sources, proposed)
                except ValueError:
                    pass
                else:
                    errors.append(f"{identity}: invalid-reference fixture unexpectedly resolves")
            answer = by_id.get(identity)
            if answer is None:
                continue
            if answer["split"] != split or answer["expected_status"] not in STATUSES:
                errors.append(f"{identity}: invalid label status/split")
            for key in ("rationale", "minimum_change", "required_elements", "expected_mapping"):
                if not answer.get(key):
                    errors.append(f"{identity}: {key} missing")
            outcomes = {e["outcome"] for e in answer["required_elements"]}
            rubric = {
                "supported": outcomes == {"present"},
                "partial": outcomes == {"present", "absent"},
                "gap": "absent" in outcomes,
                "needs_review": bool(outcomes & {"unknown", "contradicted"}),
                "not_applicable": outcomes == {"not_applicable"},
            }
            if not rubric.get(answer["expected_status"], False):
                errors.append(f"{identity}: element rubric conflicts with status")
            if answer["synthetic_regulatory_simulation"] != any(v["synthetic"] for v in selected_rules):
                errors.append(f"{identity}: simulation label mismatch")
            if identity in CRITICAL and (not answer["critical_tags"] or answer["expected_status"] != "needs_review"):
                errors.append(f"{identity}: critical-case gate violated")
            if answer["critical_tags"] and answer["expected_status"] == "supported":
                errors.append(f"{identity}: critical case cannot expect supported")
            refs = answer["allowed_references"]
            if not refs or not any((r["document_id"], r["version_id"]) in version_keys for r in refs):
                errors.append(f"{identity}: source references missing")
            for reference in refs:
                try:
                    resolve_reference(case, sources, reference)
                except ValueError as exc:
                    errors.append(f"{identity}: {exc}")
            mapping = answer["expected_mapping"]
            if not any(r["document_id"] == mapping["requirement_document"] and
                       r["passage_id"] == mapping["requirement_passage"] for r in refs):
                errors.append(f"{identity}: mapping rule passage absent")
            if not set(mapping["relevant_document_ids"]).issubset({r["document_id"] for r in refs}):
                errors.append(f"{identity}: mapping references absent")
    if len(all_ids) != len(set(all_ids)):
        errors.append("split IDs overlap")
    records = {}
    for split, cases in pack["inputs"].items():
        records[split] = {p["text"] for c in cases for d in c["documents"]
                          if d["kind"] == "evidence" for p in d["passages"]}
    if records["development"] & records["held_out"]:
        errors.append("operational record overlap between development and held-out inputs")
    return errors


class SourceText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []

    def handle_data(self, text):
        self.parts.append(text)


def validate_files(root=ROOT):
    errors = []
    try:
        freeze = read_json(root / "data/fixtures/freeze-manifest.json")
        if set(freeze["sha256"]) != set(FILES):
            errors.append("frozen file list mismatch")
        for relative in FILES:
            digest = hashlib.sha256((root / relative).read_bytes()).hexdigest()
            if digest != freeze["sha256"].get(relative):
                errors.append(f"hash mismatch: {relative}")
        if errors:
            return errors
        pack = load_pack(root)
        errors.extend(validate_pack(pack))
        for version in pack["sources"]["versions"]:
            if version["synthetic"]:
                continue
            if version["raw_path"] not in FILES:
                errors.append("source path outside frozen files")
                continue
            raw = (root / version["raw_path"]).read_bytes()
            if hashlib.sha256(raw).hexdigest() != version["sha256"]:
                errors.append("source manifest hash mismatch")
            parser = SourceText()
            parser.feed(raw.decode("utf-8"))
            normalized = " ".join(" ".join(parser.parts).split())
            excerpts = (root / FILES[1]).read_text(encoding="utf-8")
            for passage in version["passages"]:
                if passage["text"] not in normalized or passage["text"] not in excerpts:
                    errors.append(f"source quote absent: {passage['passage_id']}")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors.append(f"invalid fixture package: {exc}")
    return errors


def inspect_development(root, identity):
    if identity not in {"DEV-01", "DEV-02", "DEV-03"}:
        raise ValueError("Only development cases are available in this inspector")
    errors = validate_files(root)
    if errors:
        raise ValueError("; ".join(errors))
    pack = load_pack(root)
    return {
        "mode": "fixture inspection; no model execution",
        "current_coverage_verified": False,
        "case": next(c for c in pack["inputs"]["development"] if c["case_id"] == identity),
        "expected_answer": next(a for a in pack["labels"]["development"] if a["case_id"] == identity),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("validate", "inspect"))
    parser.add_argument("case_id", nargs="?", default="DEV-02")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if args.command == "validate":
        errors = validate_files()
        if errors:
            print(json.dumps({"valid": False, "errors": errors}, indent=2))
            return 1
        pack = load_pack(ROOT)
        print(json.dumps({"valid": True, "development_cases": 3, "held_out_cases": 20,
                          "held_out_status_counts": dict(Counter(a["expected_status"] for a in pack["labels"]["held_out"])),
                          "current_coverage_verified": False, "model_evaluation": "not run"}, indent=2))
    else:
        try:
            result = inspect_development(ROOT, args.case_id)
        except ValueError as exc:
            print(str(exc))
            return 1
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            case, answer = result["case"], result["expected_answer"]
            print(f"{case['case_id']} | {case['label']} | {result['mode']}")
            print("Scope: " + case["obligation_scope"])
            print("Records: " + ", ".join(d["kind"] for d in case["documents"]))
            print("Expected answer (benchmark author): " + answer["expected_status"])
            print("Reason: " + answer["rationale"])
            print("Needed next: " + answer["minimum_change"])
            print(f"Exact allowed citations: {len(answer['allowed_references'])}")
            print("Current regulatory coverage: unverified. Model calls: 0.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
