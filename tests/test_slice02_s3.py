"""Accepted document transport checks against botocore models, with no AWS requests."""
import base64
import hashlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

import boto3
from botocore.config import Config
from botocore.stub import Stubber

from regulatory_agent.cases import CaseError, CaseService, SQLiteCases
from regulatory_agent.contracts import UploadAuthorization
from regulatory_agent.aws_document_objects import S3DocumentObjects

ACCOUNT = '482439369658'
BUCKET = 'test-regulatory-documents'
DATA = b'Synthetic document. Fictional policy controls.\n'
UPLOAD = 'upload-one'


class BrokenBody(io.BytesIO):
    def read(self, size=-1):
        raise OSError('controlled stream failure')


class S3DocumentTransportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.cases = CaseService(SQLiteCases(Path(self.temp.name) / 'cloud-case-tests.sqlite'))
        self.case = self.cases.create('operator-a', {'bank_profile': {'name': 'Fictional cloud bank'}}).case_id
        self.other = self.cases.create('operator-b', {'bank_profile': {'name': 'Other fictional cloud bank'}}).case_id
        self.s3 = boto3.client('s3', region_name='ap-south-1', aws_access_key_id='testing', aws_secret_access_key='testing',
                               endpoint_url='https://s3.ap-south-1.amazonaws.com', config=Config(signature_version='s3v4', s3={'addressing_style': 'virtual'}))
        self.stub = Stubber(self.s3); self.stub.activate()
        self.objects = S3DocumentObjects(self.cases, self.s3, BUCKET, ACCOUNT)
        self.key = f'owners/operator-a/cases/{self.case}/uploads/{UPLOAD}'
        self.headers = {'x-filename': 'fictional-policy.txt', 'x-document-kind': 'policy', 'x-synthetic': 'true'}

    def tearDown(self):
        self.stub.assert_no_pending_responses(); self.stub.deactivate(); self.s3.close(); self.temp.cleanup()

    def ready(self, *, region='ap-south-1', versioning='Enabled'):
        self.stub.add_response('get_bucket_location', {'LocationConstraint': region},
                               {'Bucket': BUCKET, 'ExpectedBucketOwner': ACCOUNT})
        if region == 'ap-south-1':
            self.stub.add_response('get_bucket_versioning', {'Status': versioning},
                                   {'Bucket': BUCKET, 'ExpectedBucketOwner': ACCOUNT})

    def body(self, data=DATA, version='original-v1', stream=None):
        stream = stream or io.BytesIO(data)
        self.stub.add_response('get_object', {'Body': stream, 'ContentLength': len(DATA), 'VersionId': version},
                               {'Bucket': BUCKET, 'Key': self.key, 'VersionId': version, 'ExpectedBucketOwner': ACCOUNT})
        return stream

    def reference(self):
        return {'upload_id': UPLOAD, 'key': self.key, 'version_id': 'original-v1',
                'size_bytes': len(DATA), 'sha256': hashlib.sha256(DATA).hexdigest()}

    def test_s3_10_extraction_artifact_has_private_pinned_version_and_verified_bytes(self):
        data = b'{"passages":[{"location":"Line 1","text":"Fictional"}]}'
        key = self.key + '-extracted'
        self.ready()
        self.stub.add_response('put_object', {'VersionId': 'extraction-v1', 'ServerSideEncryption': 'AES256'},
            {'Bucket': BUCKET, 'Key': key, 'Body': data, 'ContentType': 'application/json',
             'ServerSideEncryption': 'AES256', 'ExpectedBucketOwner': ACCOUNT})
        reference = self.objects.save_extraction('operator-a', self.case, UPLOAD, data)
        self.assertEqual(reference['key'], key)
        self.assertEqual(reference['version_id'], 'extraction-v1')
        self.ready()
        body = io.BytesIO(data)
        self.stub.add_response('get_object', {'Body': body, 'ContentLength': len(data), 'VersionId': 'extraction-v1'},
            {'Bucket': BUCKET, 'Key': key, 'VersionId': 'extraction-v1', 'ExpectedBucketOwner': ACCOUNT})
        self.assertEqual(self.objects.read_extraction('operator-a', self.case, reference), data)
        self.assertTrue(body.closed)

    def test_s3_01_owner_checks_precede_every_storage_operation(self):
        for operation in (
            lambda: self.objects.grant('operator-b', self.case, UPLOAD, self.headers, len(DATA)),
            lambda: self.objects.pin('operator-a', self.other, UPLOAD, len(DATA)),
            lambda: self.objects.read('operator-b', self.case, self.reference()),
            lambda: self.objects.download('operator-b', self.case, self.reference(), 'policy.txt'),
        ):
            with self.subTest(operation=operation), self.assertRaises(CaseError) as caught: operation()
            self.assertEqual(caught.exception.status_code, 404)

    def test_s3_02_signed_policy_fixes_key_length_type_and_encryption(self):
        self.ready()
        grant = self.objects.grant('operator-a', self.case, UPLOAD, self.headers, len(DATA))
        authorization = UploadAuthorization.model_validate(grant['authorization'])
        self.assertFalse(authorization.eligible_for_assessment)
        self.assertEqual(urlsplit(authorization.destination).hostname, f'{BUCKET}.s3.ap-south-1.amazonaws.com')
        fields = grant['fields']; policy = json.loads(base64.b64decode(fields['policy']))
        self.assertEqual(authorization.expires_at, policy['expiration'])
        self.assertIn({'key': self.key}, policy['conditions'])
        self.assertIn(['content-length-range', len(DATA), len(DATA)], policy['conditions'])
        self.assertIn({'Content-Type': 'application/octet-stream'}, policy['conditions'])
        self.assertIn({'x-amz-server-side-encryption': 'AES256'}, policy['conditions'])
        self.assertNotIn('fictional-policy.txt', fields['key'])
        self.assertIn('/ap-south-1/s3/aws4_request', fields['x-amz-credential'])

    def test_s3_03_invalid_metadata_never_reaches_storage(self):
        for headers, size in ((self.headers, 10_000_001), (self.headers, 0),
                              (self.headers | {'x-synthetic': 'false'}, len(DATA)),
                              (self.headers | {'x-filename': '../policy.txt'}, len(DATA)),
                              (self.headers | {'x-filename': 'policy.exe'}, len(DATA))):
            with self.subTest(headers=headers, size=size), self.assertRaises(CaseError):
                self.objects.grant('operator-a', self.case, UPLOAD, headers, size)

    def test_s3_04_wrong_bucket_region_or_versioning_is_rejected(self):
        for region, versioning in (('us-east-1', 'Enabled'), ('ap-south-1', 'Suspended')):
            self.ready(region=region, versioning=versioning)
            with self.subTest(region=region), self.assertRaises(CaseError) as caught:
                self.objects.grant('operator-a', self.case, UPLOAD, self.headers, len(DATA))
            self.assertEqual(caught.exception.status_code, 503)

    def test_s3_04_client_region_and_account_configuration_fail_closed(self):
        foreign = boto3.client('s3', region_name='us-east-1', aws_access_key_id='testing', aws_secret_access_key='testing')
        try:
            with self.assertRaises(ValueError): S3DocumentObjects(self.cases, foreign, BUCKET, ACCOUNT)
        finally: foreign.close()
        with self.assertRaises(ValueError): S3DocumentObjects(self.cases, self.s3, BUCKET, 'not-an-account')
        self.stub.add_client_error('get_bucket_location', service_error_code='AccessDenied', http_status_code=403,
                                   expected_params={'Bucket': BUCKET, 'ExpectedBucketOwner': ACCOUNT})
        with self.assertRaises(self.s3.exceptions.ClientError):
            self.objects.grant('operator-a', self.case, UPLOAD, self.headers, len(DATA))

    def test_s3_05_pin_and_reopen_use_the_exact_version_after_overwrite(self):
        self.ready()
        self.stub.add_response('head_object', {'ContentLength': len(DATA), 'VersionId': 'original-v1', 'ServerSideEncryption': 'AES256'},
                               {'Bucket': BUCKET, 'Key': self.key, 'ExpectedBucketOwner': ACCOUNT})
        initial = self.body()
        reference, content = self.objects.pin('operator-a', self.case, UPLOAD, len(DATA))
        self.assertEqual(reference, self.reference()); self.assertEqual(content, DATA); self.assertTrue(initial.closed)
        self.ready(); reopened = self.body()
        self.assertEqual(self.objects.read('operator-a', self.case, reference), DATA)
        self.assertTrue(reopened.closed)
        # No latest-version lookup is queued. A regression fails Stubber before any real network request.

    def test_s3_06_missing_version_and_changed_size_cannot_finalize(self):
        for patch in ({'VersionId': 'null'}, {'VersionId': ''}, {'ContentLength': len(DATA) + 1}):
            self.ready()
            response = {'ContentLength': len(DATA), 'VersionId': 'original-v1', 'ServerSideEncryption': 'AES256'} | patch
            self.stub.add_response('head_object', response, {'Bucket': BUCKET, 'Key': self.key, 'ExpectedBucketOwner': ACCOUNT})
            with self.subTest(patch=patch), self.assertRaises(CaseError):
                self.objects.pin('operator-a', self.case, UPLOAD, len(DATA))

    def test_s3_06_short_long_or_changed_content_is_rejected_and_closed(self):
        for data in (DATA[:-1], DATA + b'X', b'X' * len(DATA)):
            self.ready(); stream = self.body(data)
            with self.subTest(data_size=len(data)), self.assertRaises(CaseError):
                self.objects.read('operator-a', self.case, self.reference())
            self.assertTrue(stream.closed)

    def test_s3_07_stream_read_failure_still_closes_the_body(self):
        self.ready(); stream = self.body(stream=BrokenBody(DATA))
        with self.assertRaises(OSError): self.objects.read('operator-a', self.case, self.reference())
        self.assertTrue(stream.closed)

    def test_s3_08_download_uses_saved_version_and_safe_filename(self):
        self.ready(); stream = self.body()
        url = self.objects.download('operator-a', self.case, self.reference(), 'fictional policy.txt')
        parsed = urlsplit(url); query = parse_qs(parsed.query)
        self.assertEqual(parsed.scheme, 'https'); self.assertEqual(parsed.hostname, f'{BUCKET}.s3.ap-south-1.amazonaws.com')
        self.assertEqual(query['versionId'], ['original-v1']); self.assertEqual(query['X-Amz-Expires'], ['300'])
        self.assertIn('fictional%20policy.txt', query['response-content-disposition'][0])
        self.assertTrue(stream.closed)

    def test_s3_09_forged_or_cross_case_reference_does_not_read_content(self):
        second = self.cases.create('operator-a', {'bank_profile': {'name': 'Second fictional bank'}}).case_id
        for case, reference in ((self.case, self.reference() | {'key': 'owners/operator-b/secret'}),
                                (second, self.reference()), (self.case, self.reference() | {'version_id': 'null'})):
            with self.subTest(case=case), self.assertRaises(CaseError):
                self.objects.read('operator-a', case, reference)
