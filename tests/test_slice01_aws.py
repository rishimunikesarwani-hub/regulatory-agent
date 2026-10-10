"""VS1-AWS01 controlled checks. These tests make no AWS requests."""
import base64
import copy
import json
import time
import unittest
from botocore.paginate import Paginator
from botocore.session import Session

from regulatory_agent.aws_cases import DynamoDBCases, create_handler
from regulatory_agent.cases import CaseService
from regulatory_agent.contracts import CaseRecord, SafeError


class FakeDynamoDB:
    def __init__(self):
        self.items = {}
        self.calls = []

    def get_paginator(self, operation):
        assert operation == 'query'
        return Paginator(self.query, {'input_token': 'ExclusiveStartKey', 'output_token': 'LastEvaluatedKey',
                         'result_key': 'Items', 'limit_key': 'Limit'}, Session().get_service_model('dynamodb').operation_model('Query'))

    def put_item(self, **kwargs):
        self.calls.append(("put", kwargs))
        item = kwargs["Item"]
        self.items[(item["PK"]["S"], item["SK"]["S"])] = copy.deepcopy(item)
        return {}

    def get_item(self, **kwargs):
        self.calls.append(("get", kwargs))
        key = kwargs["Key"]
        item = self.items.get((key["PK"]["S"], key["SK"]["S"]))
        return {"Item": copy.deepcopy(item)} if item else {}

    def query(self, **kwargs):
        self.calls.append(("query", kwargs))
        owner = kwargs["ExpressionAttributeValues"][":owner"]["S"]
        prefix = kwargs['ExpressionAttributeValues'].get(':case', {}).get('S', '')
        items = [item for (pk, sk), item in sorted(self.items.items()) if pk == owner and sk.startswith(prefix)]
        start = kwargs.get("ExclusiveStartKey")
        if start:
            items = [item for item in items if item["SK"]["S"] > start["SK"]["S"]]
        response = {"Items": copy.deepcopy(items[:1])}
        if len(items) > 1:
            response["LastEvaluatedKey"] = {key: items[0][key] for key in ("PK", "SK")}
        return response


def event(method="GET", path="/api/cases", body=None, owner="operator-a"):
    return {"version": "2.0", "rawPath": path, "body": json.dumps(body) if body is not None else None,
            "isBase64Encoded": False, "headers": {},
            "requestContext": {"http": {"method": method, "sourceIp": "192.0.2.1"},
                               "authorizer": {"jwt": {"claims": {
                                   "sub": owner, "token_use": "access", "client_id": "client-id",
                                   "iss": "https://cognito-idp.ap-south-1.amazonaws.com/ap-south-1_pool",
                                   "exp": str(int(time.time()) + 3600)}}}}}


class AWSCaseSliceTests(unittest.TestCase):
    def setUp(self):
        self.client = FakeDynamoDB()
        self.service = CaseService(DynamoDBCases(self.client, "test-cases"))
        self.handler = create_handler(self.service, environment="aws", region="ap-south-1",
                                      user_pool_id="ap-south-1_pool", user_pool_client_id="client-id", commit_sha="test-sha")

    def call(self, request):
        response = self.handler(request, None)
        self.assertEqual(response["headers"]["Cache-Control"], "no-store")
        return response["statusCode"], json.loads(response["body"])

    def test_vs1_aws01_authorized_create_persists_and_new_adapter_reads_same_record(self):
        status, created = self.call(event("POST", body={"bank_profile": {"name": "Fictional AWS Bank"}}))
        self.assertEqual(status, 201)
        record = CaseRecord.model_validate(created)
        reopened = CaseService(DynamoDBCases(self.client, "test-cases")).read("operator-a", record.case_id)
        self.assertEqual(reopened, record)
        self.assertEqual(self.client.calls[0][1]["Item"]["PK"]["S"], "OWNER#operator-a")
        self.assertIn("attribute_not_exists", self.client.calls[0][1]["ConditionExpression"])
        self.assertTrue(self.client.calls[-1][1]["ConsistentRead"])

    def test_vs1_aws01_list_queries_owner_and_handles_all_pages(self):
        for name in ("One", "Two", "Three"):
            self.service.create("operator-a", {"bank_profile": {"name": name}})
        self.service.create("operator-b", {"bank_profile": {"name": "Other owner"}})
        status, listed = self.call(event())
        self.assertEqual(status, 200)
        self.assertEqual(len(listed["cases"]), 3)
        queries = [args for name, args in self.client.calls if name == "query"]
        self.assertEqual(len(queries), 3)
        for arguments in queries:
            self.assertEqual(arguments["KeyConditionExpression"], "#pk = :owner AND begins_with(#sk, :case)")
            self.assertEqual(arguments["ExpressionAttributeValues"][":owner"], {"S": "OWNER#operator-a"})

    def test_vs1_aws01_cross_owner_read_returns_404(self):
        case = self.service.create("operator-b", {"bank_profile": {"name": "Other owner"}})
        self.assertEqual(self.call(event(path=f"/api/cases/{case.case_id}"))[0], 404)
        self.assertEqual(self.client.calls[-1][1]["Key"]["PK"]["S"], "OWNER#operator-a")

    def test_vs1_aws01_rejects_missing_wrong_expired_or_id_token_claims_before_storage(self):
        invalid = []
        missing = event()
        missing["requestContext"].pop("authorizer")
        missing["headers"] = {"x-owner-id": "operator-a", "authorization": "Bearer fabricated"}
        invalid.append(missing)
        for key, value in (("sub", ""), ("token_use", "id"), ("client_id", "other-client"),
                           ("iss", "https://example.com"), ("exp", "0"), ("exp", "invalid")):
            request = event()
            request["requestContext"]["authorizer"]["jwt"]["claims"][key] = value
            invalid.append(request)
        for request in invalid:
            with self.subTest(request=request):
                status, body = self.call(request)
                self.assertEqual(status, 401)
                SafeError.model_validate(body)
        self.assertEqual(self.client.calls, [])

    def test_vs1_aws01_rejects_local_mode_and_wrong_region(self):
        for changes in ({"environment": "local"}, {"region": "us-east-1"}):
            config = dict(environment="aws", region="ap-south-1", user_pool_id="ap-south-1_pool",
                          user_pool_client_id="client-id") | changes
            handler = create_handler(self.service, **config)
            self.assertEqual(handler(event(), None)["statusCode"], 503)
        self.assertEqual(self.client.calls, [])

    def test_vs1_aws01_malformed_auth_envelopes_are_401_without_storage(self):
        for patch in ({"requestContext": None}, {"requestContext": []},
                      {"requestContext": {"http": {"method": "GET"}, "authorizer": None}},
                      {"requestContext": {"http": {"method": "GET"}, "authorizer": {"jwt": None}}}):
            with self.subTest(patch=patch):
                self.assertEqual(self.call(event() | patch)[0], 401)
        self.assertEqual(self.client.calls, [])

    def test_vs1_aws01_expiry_boundary_uses_injected_clock(self):
        handler = create_handler(self.service, environment="aws", region="ap-south-1",
                                 user_pool_id="ap-south-1_pool", user_pool_client_id="client-id", clock=lambda: 100)
        request = event()
        claims = request["requestContext"]["authorizer"]["jwt"]["claims"]
        claims["exp"] = "100"
        self.assertEqual(handler(request, None)["statusCode"], 401)
        claims["exp"] = "101"
        self.assertEqual(handler(request, None)["statusCode"], 200)

    def test_vs1_aws01_base64_invalid_json_and_real_data_use_shared_validation(self):
        request = event("POST", body={"bank_profile": {"name": "Encoded fixture"}})
        request["body"] = base64.b64encode(request["body"].encode()).decode()
        request["isBase64Encoded"] = True
        self.assertEqual(self.call(request)[0], 201)
        for body in ("{", "[]", json.dumps({"bank_profile": {"name": "Private"}, "synthetic": False}),
                     json.dumps({"bank_profile": {"name": "Forged"}, "owner_id": "operator-b"})):
            request = event("POST")
            request["body"] = body
            status, error = self.call(request)
            self.assertEqual(status, 422)
            SafeError.model_validate(error)

    def test_vs1_aws01_provider_failures_are_safe_503(self):
        def fail(**kwargs):
            raise RuntimeError("private credential and bank profile")

        self.client.put_item = fail
        status, body = self.call(event("POST", body={"bank_profile": {"name": "Fictional"}}))
        self.assertEqual(status, 503)
        self.assertNotIn("credential", json.dumps(body))

    def test_vs1_aws01_public_health_has_no_claim_or_storage_dependency(self):
        request = event(path="/api/health")
        request["requestContext"].pop("authorizer")
        self.assertEqual(self.call(request), (200, {"status": "ok", "commit_sha": "test-sha"}))
        self.assertEqual(self.client.calls, [])


if __name__ == "__main__":
    unittest.main()
