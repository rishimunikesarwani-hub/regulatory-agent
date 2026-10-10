"""Development preflight and release evidence checks without AWS access."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from ops import deploy_dev


ROOT = Path(__file__).resolve().parents[1]
COMMIT = "a" * 40


def configuration():
    return {
        "AWS_REGION": "ap-south-1", "AWS_DEV_ACCOUNT_ID": "123456789012",
        "AWS_DEV_STACK": "regulatory-agent-dev-s01",
        "AWS_DEV_EXECUTION_ROLE_ARN": "arn:aws:iam::123456789012:role/development/cloudformation",
        "AWS_DEV_RUNTIME_ROLE_ARN": "arn:aws:iam::123456789012:role/regulatory-agent-dev-case-runtime",
        "AWS_DEV_ARTIFACT_BUCKET": "fictional-dev-artifacts",
        "AWS_DEV_MONTHLY_BUDGET_USD": "25.50", "GITHUB_SHA": COMMIT,
        "GITHUB_OUTPUT": "workflow-output.txt",
    }


class DeploymentConfigurationTests(unittest.TestCase):
    def test_accepts_only_the_declared_development_target(self):
        self.assertEqual(deploy_dev.configuration(configuration()),
                         ("123456789012", "regulatory-agent-dev-s01"))

    def test_rejects_wrong_region_account_role_stack_and_commit(self):
        invalid = {
            "AWS_REGION": ("us-east-1", "ap-south-2", ""),
            "AWS_DEV_ACCOUNT_ID": ("123", "12345678901a", "1234567890123"),
            "AWS_DEV_EXECUTION_ROLE_ARN": ("arn:aws:iam::999999999999:role/deploy",
                                           "arn:aws:iam::123456789012:user/operator", "not-an-arn"),
            "AWS_DEV_RUNTIME_ROLE_ARN": ("arn:aws:iam::999999999999:role/regulatory-agent-dev-case-runtime",
                                         "arn:aws:iam::123456789012:role/Administrator", ""),
            "AWS_DEV_STACK": ("regulatory-agent-production", "other-dev-stack", ""),
            "GITHUB_SHA": ("main", "a" * 39, "g" * 40, "a" * 41),
            "AWS_DEV_ARTIFACT_BUCKET": ("UPPERCASE", "ab", "bucket/with-path"),
        }
        for key, values in invalid.items():
            for value in values:
                with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                    deploy_dev.configuration(configuration() | {key: value})

    def test_rejects_invalid_or_unbounded_budget_values(self):
        for budget in ("", "0", "-1", "NaN", "Infinity", "-Infinity", "not-money"):
            with self.subTest(budget=budget), self.assertRaises(ValueError):
                deploy_dev.configuration(configuration() | {"AWS_DEV_MONTHLY_BUDGET_USD": budget})

    def test_missing_inputs_are_rejected_before_any_command(self):
        for key in ("AWS_DEV_ACCOUNT_ID", "AWS_DEV_EXECUTION_ROLE_ARN", "AWS_DEV_ARTIFACT_BUCKET",
                    "AWS_DEV_MONTHLY_BUDGET_USD", "AWS_DEV_RUNTIME_ROLE_ARN", "GITHUB_SHA", "GITHUB_OUTPUT"):
            env = configuration()
            env.pop(key)
            with self.subTest(key=key), patch.dict(os.environ, env, clear=True), \
                    patch.object(deploy_dev, "command") as command, patch.object(deploy_dev.os, "chdir"):
                with self.assertRaises(ValueError):
                    deploy_dev.main()
                command.assert_not_called()

    def test_wrong_checkout_commit_stops_before_aws(self):
        with patch.dict(os.environ, configuration(), clear=True), \
                patch.object(deploy_dev, "command", return_value="b" * 40) as command, \
                patch.object(deploy_dev.os, "chdir"):
            with self.assertRaisesRegex(ValueError, "Checkout"):
                deploy_dev.main()
            self.assertEqual(command.call_count, 1)
            self.assertEqual(command.call_args.args[:2], ("git", "rev-parse"))

    def test_dirty_checkout_stops_before_aws(self):
        with patch.dict(os.environ, configuration(), clear=True), \
                patch.object(deploy_dev, "command", side_effect=[COMMIT, " M src/changed.py"]) as command, \
                patch.object(deploy_dev.os, "chdir"):
            with self.assertRaisesRegex(ValueError, "Release source"):
                deploy_dev.main()
            self.assertEqual(command.call_count, 2)
            self.assertTrue(all(call.args[0] == "git" for call in command.call_args_list))

    def test_wrong_observed_account_stops_before_deployment(self):
        responses = [COMMIT, "", json.dumps({"Account": "999999999999"})]
        with patch.dict(os.environ, configuration(), clear=True), \
                patch.object(deploy_dev, "command", side_effect=responses) as command, \
                patch.object(deploy_dev.os, "chdir"):
            with self.assertRaisesRegex(ValueError, "AWS account mismatch"):
                deploy_dev.main()
            self.assertEqual(command.call_count, 3)
            self.assertEqual(command.call_args.args[:3], ("aws", "sts", "get-caller-identity"))


class ReleaseResultTests(unittest.TestCase):
    def record(self, previous=None, *, deployment="success", browser="success", commit=COMMIT):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "runs/releases/development.json"
            if previous is not None:
                path.parent.mkdir(parents=True)
                path.write_text(json.dumps(previous), encoding="utf-8")
            env = os.environ.copy() | {"GITHUB_SHA": commit, "DEPLOYMENT_RESULT": deployment, "BROWSER_RESULT": browser}
            result = subprocess.run([sys.executable, "-X", "utf8", str(ROOT / "ops/record_release.py")],
                                    cwd=directory, env=env, capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(result.returncode, 0, result.stderr)
            return json.loads(path.read_text(encoding="utf-8"))

    @staticmethod
    def deployed():
        return {"commit": COMMIT, "url": "https://fictional.cloudfront.net", "environment": "development",
                "region": "ap-south-1", "status": "deployed_pending_browser",
                "limitations": ["Fictional cases only.", "Private uploads are disabled."]}

    def test_verified_result_needs_successful_deployment_and_browser(self):
        record = self.record(self.deployed())
        self.assertEqual(record["status"], "verified_development_slice")
        self.assertEqual(record["commit"], COMMIT)
        self.assertEqual(record["url"], self.deployed()["url"])
        self.assertEqual(record["limitations"], self.deployed()["limitations"])
        self.assertTrue(record["recorded_at"].endswith("+00:00"))

    def test_failed_cancelled_skipped_and_unknown_results_stay_unverified(self):
        for deployment, browser in (("failure", "success"), ("success", "failure"), ("cancelled", "skipped"),
                                    ("success", "skipped"), ("unknown", "unknown")):
            with self.subTest(deployment=deployment, browser=browser):
                record = self.record(self.deployed(), deployment=deployment, browser=browser)
                self.assertEqual(record["status"], "unverified")
                self.assertEqual(record["deployment_result"], deployment)
                self.assertEqual(record["browser_checks"], browser)

    def test_failed_deployment_without_record_has_no_invented_url(self):
        record = self.record(deployment="failure", browser="skipped")
        self.assertEqual(record["status"], "unverified")
        self.assertIsNone(record["url"])
        self.assertEqual(record["commit"], COMMIT)

    def test_success_flags_without_a_saved_deployment_cannot_verify_a_release(self):
        self.assertEqual(self.record()["status"], "unverified")

    def test_stale_commit_wrong_environment_or_missing_url_cannot_verify_a_release(self):
        for changes in ({"commit": "b" * 40}, {"environment": "production"}, {"url": None}, {"url": ""}):
            with self.subTest(changes=changes):
                record = self.record(self.deployed() | changes)
                self.assertEqual(record["status"], "unverified")


if __name__ == "__main__":
    unittest.main()
