"""Mumbai DynamoDB storage and the API Gateway HTTP v2 Lambda entry point."""
import base64
import binascii
import json
import os
import time

from .cases import (CaseError, CaseService, authenticated_owner, authentication_error,
                    error_body, invalid_request, not_found, unavailable)
from .contracts import CaseRecord


class DynamoDBCases:
    def __init__(self, client, table_name):
        if not isinstance(table_name, str) or not table_name.strip():
            raise ValueError("missing_cases_table")
        self.client = client
        self.table_name = table_name

    @staticmethod
    def key(owner, case_id):
        return {"PK": {"S": f"OWNER#{owner}"}, "SK": {"S": f"CASE#{case_id}"}}

    @staticmethod
    def record(item, owner):
        record = CaseRecord.model_validate_json(item["record"]["S"])
        if record.owner_id != owner or DynamoDBCases.key(owner, record.case_id) != {key: item[key] for key in ("PK", "SK")}:
            raise ValueError("invalid_stored_scope")
        return record

    def save(self, record):
        self.client.put_item(TableName=self.table_name,
                             Item=self.key(record.owner_id, record.case_id) | {"record": {"S": record.model_dump_json()}},
                             ConditionExpression="attribute_not_exists(PK) AND attribute_not_exists(SK)")

    def read(self, owner, case_id):
        response = self.client.get_item(TableName=self.table_name, Key=self.key(owner, case_id), ConsistentRead=True)
        item = response.get("Item")
        return self.record(item, owner) if item else None

    def list(self, owner):
        arguments = dict(TableName=self.table_name, KeyConditionExpression="#pk = :owner",
                         ExpressionAttributeNames={"#pk": "PK"},
                         ExpressionAttributeValues={":owner": {"S": f"OWNER#{owner}"}}, ConsistentRead=True)
        records, seen_cursors = [], set()
        while True:
            response = self.client.query(**arguments)
            records.extend(self.record(item, owner) for item in response.get("Items", []))
            cursor = response.get("LastEvaluatedKey")
            if not cursor:
                return records
            serialized = json.dumps(cursor, sort_keys=True)
            if serialized in seen_cursors or cursor.get("PK") != {"S": f"OWNER#{owner}"}:
                raise ValueError("invalid_pagination")
            seen_cursors.add(serialized)
            arguments["ExclusiveStartKey"] = cursor


def _response(status, body):
    return {"statusCode": status, "headers": {"Content-Type": "application/json", "Cache-Control": "no-store",
                                             "X-Content-Type-Options": "nosniff"},
            "isBase64Encoded": False, "body": json.dumps(body, ensure_ascii=False, allow_nan=False)}


def create_handler(service, *, environment="aws", region="ap-south-1", user_pool_id,
                   user_pool_client_id, commit_sha="unknown", clock=time.time):
    def handle(event, context):
        try:
            if not isinstance(event, dict) or event.get("version") != "2.0":
                raise authentication_error()
            request_context = event.get("requestContext", {})
            if not isinstance(request_context, dict) or not isinstance(request_context.get("http", {}), dict):
                raise authentication_error()
            method = request_context.get("http", {}).get("method")
            path = event.get("rawPath", "")
            if method == "GET" and path == "/api/health":
                return _response(200, {"status": "ok", "commit_sha": commit_sha})
            if (environment != "aws" or region != "ap-south-1" or not user_pool_id
                    or not user_pool_id.startswith("ap-south-1_") or not user_pool_client_id):
                raise unavailable()
            try:
                claims = request_context.get("authorizer", {}).get("jwt", {}).get("claims", {})
                owner = authenticated_owner(claims.get("sub"))
                valid = (claims.get("token_use") == "access" and claims.get("client_id") == user_pool_client_id
                         and claims.get("iss") == f"https://cognito-idp.{region}.amazonaws.com/{user_pool_id}"
                         and int(claims.get("exp", "0")) > clock())
            except (ValueError, TypeError, AttributeError):
                raise authentication_error() from None
            if not valid:
                raise authentication_error()
            active = service() if callable(service) else service
            if path == "/api/cases" and method == "POST":
                try:
                    body = event.get("body") or ""
                    if event.get("isBase64Encoded") is True:
                        body = base64.b64decode(body, validate=True).decode("utf-8")
                    payload = json.loads(body)
                except (ValueError, TypeError, UnicodeError, binascii.Error):
                    raise invalid_request() from None
                return _response(201, active.create(owner, payload).model_dump())
            if path == "/api/cases" and method == "GET":
                return _response(200, active.list(owner).model_dump())
            if method == "GET" and path.startswith("/api/cases/"):
                return _response(200, active.read(owner, path[len("/api/cases/"):]).model_dump())
            raise not_found()
        except CaseError as error:
            return _response(error.status_code, error_body(error))
        except Exception:
            return _response(503, error_body(unavailable()))
    return handle


_service = None


def _configured_service():
    global _service
    if _service is None:
        import boto3
        client = boto3.client("dynamodb", region_name="ap-south-1")
        _service = CaseService(DynamoDBCases(client, os.environ.get("CASES_TABLE", "")))
    return _service


def handler(event, context):
    return create_handler(_configured_service, environment=os.environ.get("APP_ENV", ""),
                          region=os.environ.get("AWS_REGION", ""), user_pool_id=os.environ.get("USER_POOL_ID", ""),
                          user_pool_client_id=os.environ.get("USER_POOL_CLIENT_ID", ""),
                          commit_sha=os.environ.get("COMMIT_SHA", "unknown"))(event, context)
