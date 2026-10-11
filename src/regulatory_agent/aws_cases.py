"""Mumbai DynamoDB storage and the API Gateway HTTP v2 Lambda entry point."""
import base64
import binascii
import json
import os
import time
from urllib.parse import quote

from .cases import (CaseError, CaseService, authenticated_owner, authentication_error,
                    error_body, invalid_request, not_found, unavailable)
from .contracts import CaseRecord
from .documents import rejected


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
        arguments = dict(TableName=self.table_name, KeyConditionExpression="#pk = :owner AND begins_with(#sk, :case)",
                         ExpressionAttributeNames={"#pk": "PK", "#sk": "SK"},
                         ExpressionAttributeValues={":owner": {"S": f"OWNER#{owner}"}, ":case": {"S": "CASE#"}}, ConsistentRead=True)
        records, seen_cursors = [], set()
        for response in self.client.get_paginator('query').paginate(**arguments):
            records.extend(self.record(item, owner) for item in response.get("Items", []))
            cursor = response.get("LastEvaluatedKey")
            if not cursor:
                return records
            serialized = json.dumps(cursor, sort_keys=True)
            if serialized in seen_cursors or cursor.get("PK") != {"S": f"OWNER#{owner}"}:
                raise ValueError("invalid_pagination")
            seen_cursors.add(serialized)
        return records


def _response(status, body):
    return {"statusCode": status, "headers": {"Content-Type": "application/json", "Cache-Control": "no-store",
                                             "X-Content-Type-Options": "nosniff"},
            "isBase64Encoded": False, "body": json.dumps(body, ensure_ascii=False, allow_nan=False)}


def create_handler(service, *, environment="aws", region="ap-south-1", user_pool_id,
                   user_pool_client_id, commit_sha="unknown", clock=time.time, documents=None,
                   assessments=None, queue=None, source_root=None):
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
            parts = path.split('/') if isinstance(path, str) else []
            if len(parts)>=5 and parts[:3]==['','api','cases'] and parts[4] in {'assessment-selection','assessments'}:
                active.read(owner,parts[3])
                if assessments is None: raise unavailable()
                from .aws_assessment_api import response
                assessment=assessments() if callable(assessments) else assessments
                status,body=response(assessment,queue,owner,parts[3],method,parts[4:],event,source_root=source_root)
                result=_response(status,body)
                if len(result['body'].encode())>4_000_000: raise unavailable()
                return result
            if len(parts) >= 5 and parts[:3] == ['', 'api', 'cases'] and parts[4] in ('documents', 'uploads'):
                if documents is None:
                    raise unavailable()
                docs = documents() if callable(documents) else documents
                case, route = parts[3], parts[4:]
                if method == 'POST' and route == ['uploads']:
                    body = event.get('body') or ''
                    if len(body) > 8192:
                        raise rejected()
                    try:
                        if event.get('isBase64Encoded') is True:
                            body = base64.b64decode(body, validate=True).decode('utf-8')
                        payload = json.loads(body)
                        if not isinstance(payload, dict) or set(payload) - {'filename', 'kind', 'size_bytes', 'synthetic', 'source_id'}:
                            raise ValueError('invalid_upload_metadata')
                        headers = {'x-filename': quote(payload['filename'], safe=''), 'x-document-kind': payload['kind'],
                                   'x-synthetic': 'true' if payload['synthetic'] is True else 'false'}
                        if 'source_id' in payload:
                            headers['x-source-id'] = payload['source_id']
                        incoming = {k.lower(): v for k, v in (event.get('headers') or {}).items()}
                        size = payload['size_bytes']
                    except (ValueError, TypeError, KeyError, UnicodeError, binascii.Error):
                        raise rejected() from None
                    return _response(201, docs.reserve(owner, case, headers, size, incoming.get('idempotency-key')))
                if method == 'GET' and route == ['documents']:
                    return _response(200, docs.list(owner, case))
                if len(route) == 2 and route[0] == 'uploads' and method == 'GET':
                    return _response(200, docs.status(owner, case, route[1]))
                if len(route) == 3 and route[0] == 'uploads' and method == 'POST':
                    if route[2] == 'finalize':
                        return _response(200, docs.finalize(owner, case, route[1]))
                    if route[2] == 'cancel':
                        return _response(200, docs.cancel(owner, case, route[1]))
                if len(route) == 2 and route[0] == 'documents' and method == 'GET':
                    try:
                        offset = int((event.get('queryStringParameters') or {}).get('offset', '0'))
                    except (ValueError, TypeError):
                        raise rejected() from None
                    return _response(200, docs.read(owner, case, route[1], offset=offset))
                if len(route) == 3 and route[0] == 'documents' and route[2] == 'original' and method == 'GET':
                    return _response(200, docs.download(owner, case, route[1]))
                raise not_found()
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
_documents = None
_assessments = None
_queue = None


def _configured_service():
    global _service
    if _service is None:
        import boto3
        from botocore.config import Config
        client = boto3.client("dynamodb", region_name="ap-south-1",
            config=Config(connect_timeout=2, read_timeout=4, retries={'mode': 'standard', 'total_max_attempts': 2}))
        _service = CaseService(DynamoDBCases(client, os.environ.get("CASES_TABLE", "")))
    return _service


def _configured_documents():
    global _documents
    if _documents is None:
        import boto3
        from botocore.config import Config
        from .aws_document_objects import S3DocumentObjects
        from .aws_documents import CloudDocuments
        cases = _configured_service()
        client = boto3.client('s3', region_name='ap-south-1', endpoint_url='https://s3.ap-south-1.amazonaws.com',
            config=Config(signature_version='s3v4', s3={'addressing_style': 'virtual'},
                          connect_timeout=2, read_timeout=4, retries={'mode': 'standard', 'total_max_attempts': 2}))
        objects = S3DocumentObjects(cases, client, os.environ.get('DOCUMENTS_BUCKET', ''), os.environ.get('AWS_ACCOUNT_ID', ''))
        _documents = CloudDocuments(cases, cases.repository.client, cases.repository.table_name, objects)
    return _documents


def handler(event, context):
    from pathlib import Path
    enabled=os.environ.get('ASSESSMENTS_ENABLED')=='true'
    return create_handler(_configured_service, environment=os.environ.get("APP_ENV", ""),
                          region=os.environ.get("AWS_REGION", ""), user_pool_id=os.environ.get("USER_POOL_ID", ""),
                          user_pool_client_id=os.environ.get("USER_POOL_CLIENT_ID", ""),
                          commit_sha=os.environ.get("COMMIT_SHA", "unknown"), documents=_configured_documents,
                          assessments=_configured_assessments if enabled else None, queue=_configured_queue if enabled else None,
                          source_root=Path(__file__).resolve().parents[1])(event, context)


def _configured_assessments():
    global _assessments
    if _assessments is None:
        from .aws_execution import configured_service
        _assessments=configured_service()
    return _assessments


def _configured_queue():
    global _queue
    if _queue is None:
        import boto3
        from botocore.config import Config
        from .aws_execution import AssessmentQueue
        client=boto3.client('sqs',region_name='ap-south-1',endpoint_url='https://sqs.ap-south-1.amazonaws.com',
            config=Config(connect_timeout=2,read_timeout=4,retries={'mode':'standard','total_max_attempts':1}))
        _queue=AssessmentQueue(_configured_assessments(),client,os.environ.get('ASSESSMENT_QUEUE_URL',''),os.environ.get('AWS_ACCOUNT_ID',''))
    return _queue
