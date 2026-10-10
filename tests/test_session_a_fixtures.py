"""A-01 through A-12: offline fixture integrity and boundary checks."""

import copy
import json
from pathlib import Path
import socket
import tempfile
import unittest
from unittest.mock import patch

from ops.session_a_fixtures import (
    inspect_development, load_pack, resolve_reference, validate_files, validate_pack,
)

ROOT = Path(__file__).resolve().parents[1]


class FoundationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Block external calls in the actual test process, including accidental DNS.
        cls.network = [patch.object(socket, name, side_effect=AssertionError("Network forbidden"))
                       for name in ("socket", "create_connection", "getaddrinfo")]
        for guard in cls.network:
            guard.start()
            cls.addClassCleanup(guard.stop)

    def setUp(self):
        self.pack = load_pack(ROOT)

    def rejects(self, text):
        errors = validate_pack(self.pack)
        self.assertTrue(any(text in error for error in errors), errors)

    def test_a01_complete_pack_is_valid(self):
        self.assertEqual(validate_files(ROOT), [])

    def test_a01_test_process_blocks_network(self):
        with self.assertRaisesRegex(AssertionError, "Network forbidden"):
            socket.create_connection(("www.rbi.org.in", 443))
        with self.assertRaisesRegex(AssertionError, "Network forbidden"):
            socket.getaddrinfo("www.rbi.org.in", 443)

    def test_a02_changed_bytes_fail(self):
        manifest = json.loads((ROOT / "data/fixtures/freeze-manifest.json").read_text())
        for changed in ("data/sources/rbi-it-governance-2023.html",
                        "data/fixtures/development-inputs.json"):
            with self.subTest(changed=changed), tempfile.TemporaryDirectory() as directory:
                target = Path(directory)
                for relative in [*manifest["sha256"], "data/fixtures/freeze-manifest.json"]:
                    path = target / relative
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_bytes((ROOT / relative).read_bytes())
                with (target / changed).open("ab") as stream:
                    stream.write(b"\nchanged")
                self.assertTrue(any("hash mismatch" in e for e in validate_files(target)))

    def test_a03_quote_must_match(self):
        self.pack["labels"]["development"][0]["allowed_references"][0]["quote"] = "Invented quote"
        self.rejects("citation")

    def test_a03_locator_must_match(self):
        self.pack["labels"]["development"][0]["allowed_references"][0]["locator"] = "page 999"
        self.rejects("citation")

    def test_a03_passage_must_exist(self):
        self.pack["labels"]["development"][0]["allowed_references"][0]["passage_id"] = "absent"
        self.rejects("citation")

    def test_a04_ids_must_be_unique(self):
        self.pack["inputs"]["development"].append(copy.deepcopy(self.pack["inputs"]["development"][0]))
        self.rejects("duplicate")

    def test_a04_splits_must_be_separate(self):
        self.pack["inputs"]["held_out"][0]["case_id"] = "DEV-01"
        self.rejects("split")

    def test_a04_operational_records_are_not_reused_across_splits(self):
        text = self.pack["inputs"]["development"][0]["documents"][2]["passages"][0]["text"]
        self.pack["inputs"]["held_out"][0]["documents"][2]["passages"][0]["text"] = text
        self.rejects("operational record overlap")

    def test_a05_nested_answers_are_rejected(self):
        self.pack["inputs"]["development"][0]["profile"]["expected_status"] = "supported"
        self.rejects("answer leakage")

    def test_a06_bank_labels_required(self):
        self.pack["inputs"]["development"][0]["documents"][0]["synthetic"] = False
        self.rejects("fictional bank")

    def test_a06_rule_simulation_labels_required(self):
        simulation = next(v for v in self.pack["sources"]["versions"] if v["synthetic"])
        simulation["label"] = "RBI amendment"
        self.rejects("simulation label")

    def test_a07_catalogue_must_be_complete(self):
        self.pack["inputs"]["held_out"].pop()
        self.rejects("EVAL-01 through EVAL-20")

    def test_a08_rationale_required(self):
        self.pack["labels"]["development"][0]["rationale"] = ""
        self.rejects("rationale")

    def test_a08_missing_label_rejected(self):
        self.pack["labels"]["development"].pop()
        self.rejects("label IDs")

    def test_a08_sources_required(self):
        self.pack["labels"]["development"][0]["allowed_references"] = []
        self.rejects("source references")

    def test_a08_supported_requires_present_elements(self):
        self.pack["labels"]["development"][0]["required_elements"][0]["outcome"] = "unknown"
        self.rejects("element rubric")

    def test_a08_partial_requires_known_mixed_fulfilment(self):
        self.pack["labels"]["held_out"][4]["required_elements"][-1]["outcome"] = "unknown"
        self.rejects("element rubric")

    def test_a08_mapping_requires_exact_rule_passage(self):
        self.pack["labels"]["development"][0]["expected_mapping"]["requirement_passage"] = "missing"
        self.rejects("mapping rule passage")

    def test_a11_effective_date_boundary_is_enforced(self):
        self.pack["inputs"]["held_out"][15]["selected_versions"]["SIM-ACCESS"] = "v2-added"
        self.rejects("not yet effective")

    def test_a09_critical_cases_cannot_expect_supported(self):
        for identity in ("EVAL-09", "EVAL-10", "EVAL-17", "EVAL-18", "EVAL-19", "EVAL-20"):
            with self.subTest(identity=identity):
                self.pack = load_pack(ROOT)
                label = next(x for x in self.pack["labels"]["held_out"] if x["case_id"] == identity)
                label["expected_status"] = "supported"
                self.rejects("critical")

    def test_a09_critical_tag_cannot_be_removed(self):
        self.pack["labels"]["held_out"][8]["critical_tags"] = []
        self.rejects("critical")

    def test_a10_inspector_shows_development_with_author_label(self):
        result = inspect_development(ROOT, "DEV-02")
        self.assertEqual(result["expected_answer"]["expected_status"], "needs_review")
        self.assertEqual(result["mode"], "fixture inspection; no model execution")
        self.assertFalse(result["current_coverage_verified"])

    def test_a10_inspector_denies_held_out(self):
        with self.assertRaisesRegex(ValueError, "development"):
            inspect_development(ROOT, "EVAL-01")

    def test_a11_download_does_not_establish_current_coverage(self):
        self.pack["sources"]["current_coverage_verified"] = True
        self.rejects("current coverage")

    def test_a12_other_case_is_denied(self):
        case = self.pack["inputs"]["development"][0]
        reference = copy.deepcopy(self.pack["labels"]["development"][1]["allowed_references"][-1])
        with self.assertRaises(ValueError):
            resolve_reference(case, self.pack["sources"], reference)

    def test_a12_other_owner_is_denied(self):
        reference = copy.deepcopy(self.pack["labels"]["development"][0]["allowed_references"][0])
        reference["owner_id"] = "another-owner"
        with self.assertRaises(ValueError):
            resolve_reference(self.pack["inputs"]["development"][0], self.pack["sources"], reference)

    def test_a12_unselected_version_is_denied(self):
        case = self.pack["inputs"]["held_out"][18]
        reference = case["untrusted_proposed_references"][0]
        with self.assertRaises(ValueError):
            resolve_reference(case, self.pack["sources"], reference)

    def test_a12_document_owner_is_checked(self):
        self.pack["inputs"]["development"][0]["documents"][0]["owner_id"] = "another-owner"
        self.rejects("document scope")

    def test_simulated_change_cases_identify_both_versions(self):
        for case in self.pack["inputs"]["held_out"][12:16]:
            self.assertEqual(case["change_event"]["label"], "Synthetic regulatory simulation")
            self.assertNotEqual(case["change_event"]["previous_version"], case["change_event"]["candidate_version"])


if __name__ == "__main__":
    unittest.main()
