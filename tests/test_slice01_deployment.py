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

    def test_development_traffic_limits_fit_the_verified_account_quota(self):
        resources = self.template["Resources"]
        self.assertNotIn("ReservedConcurrentExecutions", resources["CaseFunction"]["Properties"])
        settings = resources["HttpApi"]["Properties"]["DefaultRouteSettings"]
        self.assertEqual(settings["ThrottlingRateLimit"], 2)
        self.assertEqual(settings["ThrottlingBurstLimit"], 4)

    def test_execution_role_can_use_only_the_required_aws_transform(self):
        bootstrap = yaml.safe_load((ROOT / "ops/aws-development-bootstrap.yaml").read_text())
        policies = bootstrap["Resources"]["CloudFormationRole"]["Properties"]["Policies"]
        transform = [statement for policy in policies for statement in policy["PolicyDocument"]["Statement"]
                     if "cloudformation:CreateChangeSet" in statement["Action"]]
        self.assertEqual(len(transform), 1)
        self.assertEqual(transform[0]["Resource"],
                         "arn:aws:cloudformation:ap-south-1:aws:transform/Serverless-2016-10-31")

    def test_deployment_trust_requires_the_verified_repository_and_environment(self):
        bootstrap = yaml.safe_load((ROOT / "ops/aws-development-bootstrap.yaml").read_text())
        trust = bootstrap["Resources"]["GitHubDeploymentRole"]["Properties"]["AssumeRolePolicyDocument"]
        condition = trust["Statement"][0]["Condition"]["StringEquals"]
        self.assertEqual(condition["token.actions.githubusercontent.com:aud"], "sts.amazonaws.com")
        self.assertEqual(condition["token.actions.githubusercontent.com:sub"],
                         "repo:rishimunikesarwani-hub@292392448/regulatory-agent@1412648942:environment:development")

    def test_lambda_role_has_only_owned_records_documents_queue_and_log_access(self):
        function = self.template["Resources"]["CaseFunction"]["Properties"]
        self.assertEqual(function["Role"], {"Ref": "CaseRuntimeRoleArn"})
        self.assertNotIn("Policies", function)
        bootstrap = yaml.safe_load((ROOT / "ops/aws-development-bootstrap.yaml").read_text())
        policies = bootstrap["Resources"]["CaseRuntimeRole"]["Properties"]["Policies"]
        actions = {action for policy in policies for statement in policy["PolicyDocument"]["Statement"] for action in statement["Action"]}
        self.assertEqual(actions, {"dynamodb:PutItem", "dynamodb:GetItem", "dynamodb:Query", 'dynamodb:ConditionCheckItem', 'sqs:SendMessage',
                                  "logs:CreateLogStream", "logs:PutLogEvents", 's3:GetBucketLocation', 's3:GetBucketVersioning',
                                  's3:GetObject', 's3:GetObjectVersion', 's3:PutObject'})
        queue = [statement for policy in policies for statement in policy['PolicyDocument']['Statement'] if 'sqs:SendMessage' in statement['Action']]
        self.assertEqual(queue[0]['Resource'], {'Fn::Sub':'arn:aws:sqs:ap-south-1:${AWS::AccountId}:regulatory-agent-dev-assessments'})
        execution = bootstrap["Resources"]["CloudFormationRole"]["Properties"]["Policies"]
        iam_actions = {action for policy in execution for statement in policy["PolicyDocument"]["Statement"]
                       for action in statement["Action"] if action.startswith("iam:")}
        self.assertEqual(iam_actions, {"iam:PassRole", "iam:GetRole"})
        outputs = self.template["Outputs"]
        self.assertTrue({"FrontendUrl", "ApiUrl", "CommitSha", "UserPoolId", "UserPoolClientId"} <= outputs.keys())

    def test_vs2_private_document_bucket_and_routes_preserve_cloud_contract(self):
        resources = self.template['Resources']
        bucket = resources['DocumentsBucket']
        self.assertEqual(bucket['DeletionPolicy'], 'Retain')
        properties = bucket['Properties']
        self.assertEqual(properties['VersioningConfiguration']['Status'], 'Enabled')
        self.assertTrue(all(properties['PublicAccessBlockConfiguration'].values()))
        self.assertEqual(properties['OwnershipControls']['Rules'][0]['ObjectOwnership'], 'BucketOwnerEnforced')
        self.assertEqual(properties['BucketEncryption']['ServerSideEncryptionConfiguration'][0]['ServerSideEncryptionByDefault']['SSEAlgorithm'], 'AES256')
        self.assertNotIn('LifecycleConfiguration', properties)
        cors = properties['CorsConfiguration']['CorsRules'][0]
        self.assertEqual(cors['AllowedOrigins'], [{'Fn::Sub': 'https://${Frontend.DomainName}'}])
        self.assertEqual(cors['AllowedMethods'], ['GET', 'POST'])
        policy = resources['DocumentsBucketPolicy']['Properties']['PolicyDocument']['Statement']
        self.assertTrue(any(s['Effect'] == 'Deny' and s.get('Condition', {}).get('Bool', {}).get('aws:SecureTransport') is False for s in policy))
        function = resources['CaseFunction']['Properties']
        self.assertEqual(function['Environment']['Variables']['DOCUMENTS_BUCKET'], {'Ref': 'DocumentsBucket'})
        self.assertGreaterEqual(function['Timeout'], 29)
        routes = {e['Properties']['Path'] for e in function['Events'].values()}
        self.assertTrue({'/api/cases/{case_id}/uploads', '/api/cases/{case_id}/uploads/{upload_id}',
          '/api/cases/{case_id}/uploads/{upload_id}/finalize', '/api/cases/{case_id}/uploads/{upload_id}/cancel',
          '/api/cases/{case_id}/documents', '/api/cases/{case_id}/documents/{version_id}',
          '/api/cases/{case_id}/documents/{version_id}/original'} <= routes)
        bootstrap = yaml.safe_load((ROOT / 'ops/aws-development-bootstrap.yaml').read_text())
        statements = bootstrap['Resources']['CaseRuntimeRole']['Properties']['Policies'][0]['PolicyDocument']['Statement']
        for statement in statements:
            if any(a.startswith('s3:') for a in statement['Action']):
                self.assertIn('documents-', str(statement['Resource']))
                self.assertNotIn('s3:DeleteObject', statement['Action'])
                self.assertEqual(statement['Condition']['StringEquals']['aws:RequestedRegion'], 'ap-south-1')
