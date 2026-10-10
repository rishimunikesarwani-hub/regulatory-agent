"""VS1 deployment contract: one development path, protected identity and storage."""
from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]


class DeploymentContractTests(unittest.TestCase):
    def setUp(self):
        self.template = yaml.safe_load((ROOT / "ops/sam-dev.yaml").read_text())
        self.workflow = yaml.safe_load((ROOT / ".github/workflows/dev-release.yml").read_text())

    def test_private_storage_and_region_are_enforced(self):
        resources = self.template["Resources"]
        table = resources["CasesTable"]
        self.assertEqual(table["DeletionPolicy"], "Retain")
        self.assertTrue(table["Properties"]["SSESpecification"]["SSEEnabled"])
        block = resources["FrontendBucket"]["Properties"]["PublicAccessBlockConfiguration"]
        self.assertTrue(all(block.values()))
        self.assertIn("MumbaiOnly", self.template["Rules"])
        self.assertEqual(resources["CaseFunction"]["Properties"]["Environment"]["Variables"]["APP_ENV"], "aws")
        self.assertNotIn("DEVELOPMENT_USER", resources["CaseFunction"]["Properties"]["Environment"]["Variables"])

    def test_cognito_code_flow_and_case_routes_are_authorized(self):
        resources = self.template["Resources"]
        client = resources["UserPoolClient"]["Properties"]
        self.assertEqual(client["AllowedOAuthFlows"], ["code"])
        self.assertFalse(client["GenerateSecret"])
        self.assertTrue(resources["UserPool"]["Properties"]["AdminCreateUserConfig"]["AllowAdminCreateUserOnly"])
        self.assertEqual(resources["HttpApi"]["Properties"]["Auth"]["DefaultAuthorizer"], "Cognito")
        for name, event in resources["CaseFunction"]["Properties"]["Events"].items():
            if name != "Health":
                self.assertNotEqual(event["Properties"].get("Auth", {}).get("Authorizer"), "NONE")

    def test_only_one_serialized_dev_pipeline_and_checks_before_deploy(self):
        self.assertEqual(len(list((ROOT / ".github/workflows").glob("*.yml"))), 1)
        self.assertEqual(self.workflow["concurrency"], {"group": "regulatory-agent-development", "cancel-in-progress": False})
        deploy = self.workflow["jobs"]["deploy-development"]
        self.assertIn("checks", deploy["needs"])
        self.assertEqual(deploy["environment"], "development")
        condition = deploy["if"]
        self.assertIn("refs/heads/main", condition)
        self.assertIn("deploy_development", condition)
        commands = [s.get("run", "") for s in deploy["steps"]]
        deployment = next(n for n, command in enumerate(commands) if "ops/deploy_dev.py" in command)
        browser = next(n for n, command in enumerate(commands) if "test:deployed" in command)
        self.assertLess(deployment, browser)
        self.assertEqual(deploy["permissions"]["id-token"], "write")

    def test_deployment_trust_requires_the_verified_repository_and_environment(self):
        bootstrap = yaml.safe_load((ROOT / "ops/aws-development-bootstrap.yaml").read_text())
        trust = bootstrap["Resources"]["GitHubDeploymentRole"]["Properties"]["AssumeRolePolicyDocument"]
        condition = trust["Statement"][0]["Condition"]["StringEquals"]
        self.assertEqual(condition["token.actions.githubusercontent.com:aud"], "sts.amazonaws.com")
        self.assertEqual(condition["token.actions.githubusercontent.com:sub"],
                         "repo:rishimunikesarwani-hub@292392448/regulatory-agent@1412648942:environment:development")

    def test_lambda_role_has_no_model_or_document_access(self):
        function = self.template["Resources"]["CaseFunction"]["Properties"]
        self.assertEqual(function["Role"], {"Ref": "CaseRuntimeRoleArn"})
        self.assertNotIn("Policies", function)
        bootstrap = yaml.safe_load((ROOT / "ops/aws-development-bootstrap.yaml").read_text())
        policies = bootstrap["Resources"]["CaseRuntimeRole"]["Properties"]["Policies"]
        actions = {action for policy in policies for statement in policy["PolicyDocument"]["Statement"] for action in statement["Action"]}
        self.assertEqual(actions, {"dynamodb:PutItem", "dynamodb:GetItem", "dynamodb:Query",
                                  "logs:CreateLogStream", "logs:PutLogEvents"})
        execution = bootstrap["Resources"]["CloudFormationRole"]["Properties"]["Policies"]
        iam_actions = {action for policy in execution for statement in policy["PolicyDocument"]["Statement"]
                       for action in statement["Action"] if action.startswith("iam:")}
        self.assertEqual(iam_actions, {"iam:PassRole", "iam:GetRole"})
        outputs = self.template["Outputs"]
        self.assertTrue({"FrontendUrl", "ApiUrl", "CommitSha", "UserPoolId", "UserPoolClientId"} <= outputs.keys())
