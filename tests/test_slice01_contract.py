"""VS1 shared contract is established before frontend/backend implementation."""
import json
from pathlib import Path
import unittest
from pydantic import ValidationError
from regulatory_agent.contracts import CaseCreate, CaseRecord, CaseList, SafeError


class CaseContractTests(unittest.TestCase):
    def test_case_name_is_nonblank_and_bounded(self):
        for profile in ({}, {"name": " "}, {"name": "x" * 201}, {"name": True}):
            with self.assertRaises(ValidationError):
                CaseCreate(bank_profile=profile)
        self.assertEqual(CaseCreate(bank_profile={"name": " Synthetic bank "}).bank_profile["name"], "Synthetic bank")

    def test_saved_schemas_match_executable_types(self):
        saved = json.loads((Path(__file__).resolve().parents[1] / "data/contracts/slice-01-api.json").read_text())
        self.assertEqual(saved["version"], "slice-01-v1")
        self.assertEqual(saved["schemas"], {kind.__name__: kind.model_json_schema()
                                          for kind in (CaseCreate, CaseRecord, CaseList, SafeError)})
