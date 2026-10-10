"""Accepted VS2 cloud protocol checks with isolated, controlled provider state."""
import copy
import hashlib
import json
import unittest

from botocore.exceptions import ClientError
from botocore.session import Session
from botocore.validate import validate_parameters

from regulatory_agent.aws_cases import DynamoDBCases, create_handler
from regulatory_agent.aws_documents import CloudDocuments
from regulatory_agent.cases import CaseError, CaseService
from test_slice01_aws import FakeDynamoDB, event


class Transactions(FakeDynamoDB):
    def __init__(self):
        super().__init__()
        self.conflict = False
        self.lost_ack = False
        self.interleave = None

    def transact_write_items(self, **args):
        if self.interleave:
            action, self.interleave = self.interleave, None
            action()
        model = Session().get_service_model('dynamodb').operation_model('TransactWriteItems')
        validate_parameters(args, model.input_shape)
        self.calls.append(('transaction', copy.deepcopy(args)))
        for action in args['TransactItems']:
            put = action['Put']
            item = put['Item']
            old = self.items.get((item['PK']['S'], item['SK']['S']))
            expected = put.get('ExpressionAttributeValues', {}).get(':expected', {}).get('N')
            if self.conflict or (old is not None if expected is None else not old or old['revision']['N'] != expected):
                self.conflict = False
                raise ClientError({'Error': {'Code': 'TransactionCanceledException'},
                    'CancellationReasons': [{'Code': 'ConditionalCheckFailed'}]}, 'TransactWriteItems')
        for action in args['TransactItems']:
            self.put_item(Item=action['Put']['Item'])
        if self.lost_ack:
            self.lost_ack = False
            raise OSError('Uncertain acknowledgement')
        return {}


class Objects:
    def __init__(self):
        self.data = {}
        self.artifacts = {}
        self.calls = []

    def grant(self, owner, case, upload, headers, size):
        self.calls.append(('grant', owner, case, upload))
        return {'authorization': {'upload_id': upload, 'destination': 'https://test.s3.ap-south-1.amazonaws.com',
                'expires_at': '2099-01-01T00:00:00Z', 'eligible_for_assessment': False}, 'fields': {'key': upload}}

    def pin(self, owner, case, upload, size):
        self.calls.append(('pin', owner, case, upload))
        data = self.data[upload]
        if len(data) != size:
            raise ValueError('length')
        return {'upload_id': upload, 'key': upload, 'version_id': 'original-v1', 'size_bytes': size,
                'sha256': hashlib.sha256(data).hexdigest()}, data

    def save_extraction(self, owner, case, upload, data):
        self.artifacts[upload] = data
        return {'upload_id': upload, 'version_id': 'extraction-v1', 'size_bytes': len(data),
                'sha256': hashlib.sha256(data).hexdigest()}

    def read(self, owner, case, reference):
        data = self.data[reference['upload_id']]
        if hashlib.sha256(data).hexdigest() != reference['sha256']:
            raise ValueError('hash')
        return data

    def read_extraction(self, owner, case, reference):
        data = self.artifacts[reference['upload_id']]
        if hashlib.sha256(data).hexdigest() != reference['sha256']:
            raise ValueError('hash')
        return data

    def download(self, owner, case, reference, filename):
        self.calls.append(('download', owner, case, reference['version_id']))
        return 'https://test.s3.ap-south-1.amazonaws.com/saved-original'


class CloudDocumentTests(unittest.TestCase):
    def setUp(self):
        self.client = Transactions()
        self.cases = CaseService(DynamoDBCases(self.client, 'test-cases'))
        self.case = self.cases.create('operator-a', {'bank_profile': {'name': 'Fictional Cloud Bank'}}).case_id
        self.objects = Objects()
        self.documents = CloudDocuments(self.cases, self.client, 'test-cases', self.objects)
        self.headers = {'x-filename': 'policy.txt', 'x-document-kind': 'policy', 'x-synthetic': 'true'}

    def upload(self, data=b'Fictional policy\nEvery location stays exact.', key='attempt-1', source=None):
        headers = self.headers | ({'x-source-id': source} if source else {})
        reservation = self.documents.reserve('operator-a', self.case, headers, len(data), key)
        identity = reservation['upload_id']
        self.objects.data[identity] = data
        return identity, self.documents.finalize('operator-a', self.case, identity)

    def test_aws01_case_authorization_precedes_document_storage(self):
        before = len(self.client.calls)
        for method, args in ((self.documents.reserve, (self.headers, 3, 'key')),
                             (self.documents.list, ()), (self.documents.status, ('missing',)),
                             (self.documents.finalize, ('missing',)), (self.documents.read, ('missing',))):
            with self.assertRaises(CaseError) as caught:
                method('operator-b', self.case, *args)
            self.assertEqual(caught.exception.status_code, 404)
        self.assertTrue(all(name == 'get' for name, _ in self.client.calls[before:]))
        self.assertEqual(self.objects.calls, [])

    def test_aws02_idempotent_reservation_and_changed_metadata_conflict(self):
        first = self.documents.reserve('operator-a', self.case, self.headers, 3, 'same-key')
        second = self.documents.reserve('operator-a', self.case, self.headers, 3, 'same-key')
        self.assertEqual(first['upload_id'], second['upload_id'])
        self.assertEqual(sum(name == 'transaction' for name, _ in self.client.calls), 1)
        with self.assertRaises(CaseError) as caught:
            self.documents.reserve('operator-a', self.case, self.headers, 4, 'same-key')
        self.assertEqual(caught.exception.status_code, 409)

    def test_aws03_finalization_retry_and_service_restart_preserve_one_version(self):
        identity, result = self.upload()
        reopened = CloudDocuments(self.cases, self.client, 'test-cases', self.objects)
        again = reopened.finalize('operator-a', self.case, identity)
        self.assertEqual(again, result)
        self.assertEqual(reopened.status('operator-a', self.case, identity)['state'], 'finalized')
        sources = reopened.list('operator-a', self.case)['sources']
        self.assertEqual(len(sources), 1)
        source = reopened.read('operator-a', self.case, result['document']['document_version_id'])
        self.assertEqual([p['location'] for p in source['passages']], ['Line 1', 'Line 2'])
        self.assertNotIn('original', sources[0])
        self.assertNotIn('extraction', sources[0])
        self.assertEqual(sum(call[0] == 'pin' for call in self.objects.calls), 1)

    def test_aws04_replacement_keeps_earlier_source_and_rejects_foreign_id(self):
        first_id, first = self.upload()
        _, second = self.upload(b'Fictional revised policy.', key='attempt-2', source=first['document']['source_id'])
        self.assertEqual(second['document']['version'], '2')
        self.assertEqual(first['document']['source_id'], second['document']['source_id'])
        self.assertEqual(self.documents.read('operator-a', self.case, first_id)['passages'][0]['text'], 'Fictional policy')
        with self.assertRaises(CaseError) as caught:
            self.documents.reserve('operator-a', self.case, self.headers | {'x-source-id': 'foreign'}, 3, 'foreign')
        self.assertEqual(caught.exception.status_code, 404)

    def test_aws05_reservations_conflicts_and_case_extraction_limit(self):
        self.client.conflict = True
        first, _ = self.upload(b'x' * 399_999)
        pending = self.documents.reserve('operator-a', self.case, self.headers, 2, 'over-text')['upload_id']
        self.objects.data[pending] = b'xx'
        with self.assertRaises(CaseError) as caught:
            self.documents.finalize('operator-a', self.case, pending)
        self.assertEqual(caught.exception.code, 'extraction_limit')
        self.assertEqual(self.documents.status('operator-a', self.case, pending)['state'], 'failed')
        for index in range(9):
            self.documents.reserve('operator-a', self.case, self.headers, 2, f'reserve-{index}')
        with self.assertRaises(CaseError) as caught:
            self.documents.reserve('operator-a', self.case, self.headers, 2, 'eleventh')
        self.assertEqual(caught.exception.code, 'extraction_limit')
        self.assertEqual(self.documents.list('operator-a', self.case)['sources'][0]['document']['document_version_id'], first)

    def test_aws05_interleaved_reservations_cannot_take_the_same_last_slot(self):
        for index in range(9):
            self.documents.reserve('operator-a', self.case, self.headers, 3, f'initial-{index}')
        self.client.interleave = lambda: self.documents.reserve('operator-a', self.case, self.headers, 3, 'winner')
        with self.assertRaises(CaseError) as caught:
            self.documents.reserve('operator-a', self.case, self.headers, 3, 'loser')
        self.assertEqual(caught.exception.code, 'extraction_limit')
        _, state = self.documents._load('operator-a', self.case)
        self.assertEqual(len(state['pending']), 10)

    def test_aws06_unfinished_invalid_and_cancelled_never_eligible(self):
        pending = self.documents.reserve('operator-a', self.case, self.headers, 3, 'invalid')['upload_id']
        self.assertEqual(self.documents.list('operator-a', self.case), {'sources': []})
        self.objects.data[pending] = b'\x00xx'
        with self.assertRaises(CaseError):
            self.documents.finalize('operator-a', self.case, pending)
        self.assertEqual(self.documents.status('operator-a', self.case, pending)['state'], 'failed')
        other = self.documents.reserve('operator-a', self.case, self.headers, 3, 'cancel')['upload_id']
        self.assertEqual(self.documents.cancel('operator-a', self.case, other)['state'], 'cancelled')
        with self.assertRaises(CaseError):
            self.documents.finalize('operator-a', self.case, other)
        self.assertIn(pending, self.objects.data)

    def test_aws07_lost_transaction_acknowledgement_retries_without_duplication(self):
        self.client.lost_ack = True
        with self.assertRaises(OSError):
            self.documents.reserve('operator-a', self.case, self.headers, 3, 'lost-ack')
        reservation = self.documents.reserve('operator-a', self.case, self.headers, 3, 'lost-ack')
        identity = reservation['upload_id']
        self.objects.data[identity] = b'abc'
        self.client.lost_ack = True
        with self.assertRaises(OSError):
            self.documents.finalize('operator-a', self.case, identity)
        confirmed = self.documents.finalize('operator-a', self.case, identity)
        self.assertEqual(confirmed['document']['version'], '1')
        self.assertEqual(len(self.documents.list('operator-a', self.case)['sources']), 1)

    def test_aws08_paged_source_preserves_every_line_below_payload_limit(self):
        identity, _ = self.upload(b'x\n' * 10_001)
        offset, passages = 0, []
        while offset is not None:
            page = self.documents.read('operator-a', self.case, identity, offset=offset)
            self.assertLessEqual(len(page['passages']), 500)
            self.assertLess(len(json.dumps(page).encode()), 1_000_000)
            passages.extend(page['passages'])
            offset = page['next_offset']
        self.assertEqual(len(passages), 10_001)
        self.assertEqual(passages[-1]['location'], 'Line 10001')
        self.assertEqual(len({p['passage_id'] for p in passages}), 10_001)

    def test_aws08_maximum_short_line_source_stays_in_s3_and_pages_without_truncation(self):
        identity, _ = self.upload(b'x\n' * 200_000)
        artifact = self.objects.artifacts[identity]
        self.assertGreater(len(artifact), 6 * 1024 * 1024)
        self.assertLess(len(artifact), 32_000_000)
        first = self.documents.read('operator-a', self.case, identity)
        last = self.documents.read('operator-a', self.case, identity, offset=199_500)
        self.assertEqual(first['passage_count'], 200_000)
        self.assertEqual(last['passages'][-1]['location'], 'Line 200000')
        self.assertIsNone(last['next_offset'])
        self.assertLess(len(json.dumps(first).encode()), 1_000_000)
        self.assertLess(len(json.dumps(last).encode()), 1_000_000)

    def test_aws09_artifact_corruption_and_version_specific_download(self):
        identity, _ = self.upload()
        self.assertIn('/saved-original', self.documents.download('operator-a', self.case, identity)['url'])
        self.assertEqual(self.objects.calls[-1][-1], 'original-v1')
        self.objects.artifacts[identity] = b'changed'
        with self.assertRaises(ValueError):
            self.documents.read('operator-a', self.case, identity)

    def test_aws10_case_list_excludes_document_and_upload_metadata(self):
        self.upload()
        self.assertEqual([r.case_id for r in self.cases.repository.list('operator-a')], [self.case])

    def test_aws01_http_routes_share_jwt_checks_and_safe_failures(self):
        handler = create_handler(self.cases, documents=self.documents,
                                 user_pool_id='ap-south-1_pool', user_pool_client_id='client-id')
        root = f'/api/cases/{self.case}'
        reserve = event('POST', root + '/uploads', {'filename': 'policy.txt', 'kind': 'policy', 'size_bytes': 3, 'synthetic': True})
        reserve['headers']['idempotency-key'] = 'http-one'
        response = handler(reserve, None)
        self.assertEqual(response['statusCode'], 201)
        upload = json.loads(response['body'])['upload_id']
        self.objects.data[upload] = b'abc'
        self.assertEqual(handler(event('POST', root + f'/uploads/{upload}/finalize'), None)['statusCode'], 200)
        bad = event('GET', root + '/documents')
        bad['requestContext'].pop('authorizer')
        self.assertEqual(handler(bad, None)['statusCode'], 401)
        self.objects.artifacts[upload] = b'private error'
        response = handler(event('GET', root + f'/documents/{upload}'), None)
        self.assertEqual(response['statusCode'], 503)
        self.assertNotIn('private error', response['body'])


if __name__ == '__main__':
    unittest.main()
