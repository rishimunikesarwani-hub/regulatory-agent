"""Cloud document metadata transactions and version-bound private S3 evidence."""
from datetime import datetime, timezone
import hashlib
import json
from urllib.parse import quote
import uuid

from botocore.exceptions import ClientError

from .cases import CaseError, not_found, unavailable
from .contracts import ContractError, DocumentVersion, Passage
from .documents import extract_document, rejected, upload_request
from .local import identifier


def conflict():
    return CaseError(409, 'upload_conflict', 'The upload state changed.', 'Check the upload status before another save.')


def source_read(objects, owner, case, source, *, offset=None):
    """Read the exact stored extraction, either completely or as an inspection page."""
    identity=source['document']['document_version_id']
    original=objects.read(owner,case,source['original'])
    if source['document']['case_id']!=case or hashlib.sha256(original).hexdigest()!=source['document']['sha256']:
        raise ContractError('source_integrity_failure')
    passages=json.loads(objects.read_extraction(owner,case,source['extraction']))['passages']
    if offset is not None and (type(offset) is not int or not 0<=offset<len(passages)): raise rejected()
    start=0 if offset is None else offset
    chosen=passages if offset is None else passages[start:start+500]
    result={k:v for k,v in source.items() if k not in {'original','extraction'}}
    result['passages']=[Passage(passage_id=f'{identity}-{i+1}',document_version_id=identity,**p).model_dump()
                        for i,p in enumerate(chosen,start)]
    if offset is not None: result.update(offset=start,passage_count=len(passages),next_offset=start+500 if start+500<len(passages) else None)
    return result


class CloudDocuments:
    # ponytail: One bounded case record plus one record per upload. Split only if the ten-version limit changes.
    def __init__(self, cases, client, table, objects):
        self.cases, self.client, self.table, self.objects = cases, client, table, objects

    @staticmethod
    def _key(owner, case, upload=None):
        return {'PK': {'S': f'OWNER#{owner}'},
                'SK': {'S': f'UPLOAD#{case}#{upload}' if upload else f'DOCUMENTS#{case}'}}

    def _load(self, owner, case, upload=None):
        key = self._key(owner, case, upload)
        item = self.client.get_item(TableName=self.table, Key=key, ConsistentRead=True).get('Item')
        if not item:
            return 0, None if upload else {'owner': owner, 'case': case, 'pending': [], 'sources': [], 'units': 0, 'text_bytes': 0}
        body = json.loads(item['body']['S'])
        if any(item[k] != key[k] for k in key) or body['owner'] != owner or body['case'] != case or (upload and body['upload_id'] != upload):
            raise unavailable()
        return int(item['revision']['N']), body

    def _commit(self, owner, case, revision, state, upload_revision, upload):
        actions = []
        for key, old, body in ((self._key(owner, case), revision, state),
                               (self._key(owner, case, upload['upload_id']), upload_revision, upload)):
            put = {'TableName': self.table, 'Item': key | {'body': {'S': json.dumps(body)}, 'revision': {'N': str(old + 1)}},
                   'ConditionExpression': '#revision = :expected' if old else 'attribute_not_exists(PK)'}
            if old:
                put.update(ExpressionAttributeNames={'#revision': 'revision'}, ExpressionAttributeValues={':expected': {'N': str(old)}})
            actions.append({'Put': put})
        try:
            self.client.transact_write_items(TransactItems=actions)
            return True
        except ClientError as error:
            reasons = error.response.get('CancellationReasons', [])
            if error.response['Error']['Code'] == 'TransactionCanceledException' and reasons and \
                    any(r.get('Code') == 'ConditionalCheckFailed' for r in reasons) and \
                    all(r.get('Code') in ('None', 'ConditionalCheckFailed') for r in reasons):
                return False
            raise

    @staticmethod
    def _public(source):
        return {key: value for key, value in source.items() if key not in ('original', 'extraction')}

    @staticmethod
    def _status(upload):
        return {key: upload[key] for key in ('upload_id', 'state', 'request', 'document', 'error') if key in upload}

    def _authorized(self, owner, case, upload=None):
        self.cases.read(owner, case)
        if upload is not None:
            try:
                identifier(upload)
            except (ValueError, TypeError):
                raise not_found() from None

    def reserve(self, owner, case, headers, size, key):
        self._authorized(owner, case)
        request, kind = upload_request(headers, size)
        try:
            identifier(key)
        except (ValueError, TypeError):
            raise rejected() from None
        identity = uuid.uuid5(uuid.NAMESPACE_URL, json.dumps([owner, case, key])).hex
        payload = request.model_dump() | {'source_id': headers.get('x-source-id') or identity}
        for _ in range(3):
            revision, state = self._load(owner, case)
            upload_revision, upload = self._load(owner, case, identity)
            if upload:
                if upload['request'] != payload:
                    raise conflict()
                if upload['state'] != 'reserved':
                    return self._status(upload)
                break
            if headers.get('x-source-id') and not any(s['document']['source_id'] == payload['source_id'] for s in state['sources']):
                raise not_found()
            if len(state['sources']) + len(state['pending']) >= 10:
                raise rejected('extraction_limit')
            upload = {'owner': owner, 'case': case, 'upload_id': identity, 'request': payload, 'format': kind, 'state': 'reserved'}
            state['pending'].append(identity)
            if self._commit(owner, case, revision, state, upload_revision, upload):
                break
        else:
            raise conflict()
        return self._status(upload) | self.objects.grant(owner, case, identity, headers, size)

    def status(self, owner, case, identity):
        self._authorized(owner, case, identity)
        _, upload = self._load(owner, case, identity)
        if not upload:
            raise not_found()
        return self._status(upload)

    def _finish(self, owner, case, identity, state_name, error=None):
        for _ in range(3):
            revision, state = self._load(owner, case)
            upload_revision, upload = self._load(owner, case, identity)
            if not upload:
                raise not_found()
            if upload['state'] in ('finalized', 'cancelled', 'failed'):
                return self._status(upload)
            state['pending'].remove(identity)
            upload['state'] = state_name
            if error:
                upload['error'] = error
            if self._commit(owner, case, revision, state, upload_revision, upload):
                return self._status(upload)
        raise conflict()

    def cancel(self, owner, case, identity):
        self._authorized(owner, case, identity)
        return self._finish(owner, case, identity, 'cancelled')

    def finalize(self, owner, case, identity):
        self._authorized(owner, case, identity)
        for _ in range(3):
            revision, state = self._load(owner, case)
            upload_revision, upload = self._load(owner, case, identity)
            if not upload:
                raise not_found()
            if upload['state'] == 'finalized':
                return {'document': upload['document']}
            if upload['state'] not in ('reserved', 'uploaded') or identity not in state['pending']:
                raise conflict()
            if upload['state'] == 'uploaded':
                original = upload['original']
                data = self.objects.read(owner, case, original)
                break
            original, data = self.objects.pin(owner, case, identity, upload['request']['size_bytes'])
            upload.update(state='uploaded', original=original)
            if self._commit(owner, case, revision, state, upload_revision, upload):
                break
        else:
            raise conflict()
        try:
            extracted = extract_document(upload['format'], data)
        except CaseError as error:
            self._finish(owner, case, identity, 'failed', error.code)
            raise
        artifact = self.objects.save_extraction(owner, case, identity, json.dumps(extracted, ensure_ascii=False).encode('utf-8'))
        for _ in range(3):
            revision, state = self._load(owner, case)
            upload_revision, upload = self._load(owner, case, identity)
            if upload['state'] == 'finalized':
                return {'document': upload['document']}
            if upload['state'] != 'uploaded' or identity not in state['pending']:
                raise conflict()
            if state['units'] + extracted['units'] > 100 or state['text_bytes'] + extracted['text_bytes'] > 400_000:
                self._finish(owner, case, identity, 'failed', 'extraction_limit')
                raise rejected('extraction_limit')
            request = upload['request']
            version = 1 + sum(s['document']['source_id'] == request['source_id'] for s in state['sources'])
            document = DocumentVersion(document_version_id=identity, case_id=case, source_id=request['source_id'],
                kind=request['kind'], version=str(version), sha256=original['sha256'], storage_reference=identity, synthetic=True).model_dump()
            source = {'document': document, 'filename': request['filename'], 'format': upload['format'], 'units': extracted['units'],
                      'uploaded_at': datetime.now(timezone.utc).isoformat(), 'original': original, 'extraction': artifact}
            state['sources'].insert(0, source)
            state['pending'].remove(identity)
            state['units'] += extracted['units']
            state['text_bytes'] += extracted['text_bytes']
            upload.update(state='finalized', document=document)
            if self._commit(owner, case, revision, state, upload_revision, upload):
                return {'document': document}
        raise conflict()

    def list(self, owner, case):
        self._authorized(owner, case)
        _, state = self._load(owner, case)
        return {'sources': [self._public(source) for source in state['sources']]}

    def _source(self, owner, case, identity):
        self._authorized(owner, case, identity)
        _, state = self._load(owner, case)
        for source in state['sources']:
            if source['document']['document_version_id'] == identity:
                return source
        raise not_found()

    def read(self, owner, case, identity, *, offset=0):
        source = self._source(owner, case, identity)
        extracted = json.loads(self.objects.read_extraction(owner, case, source['extraction']))
        passages = extracted['passages']
        if type(offset) is not int or offset < 0 or offset >= len(passages):
            raise rejected()
        page = [Passage(passage_id=f'{identity}-{i + 1}', document_version_id=identity, **p).model_dump()
                for i, p in enumerate(passages[offset:offset + 500], offset)]
        return self._public(source) | {'passages': page, 'offset': offset, 'passage_count': len(passages),
                                      'next_offset': offset + 500 if offset + 500 < len(passages) else None}

    def download(self, owner, case, identity):
        source = self._source(owner, case, identity)
        return {'url': self.objects.download(owner, case, source['original'], source['filename'])}

    def read_full(self, owner, case, identity):
        """Internal assessment read. Verify the pinned original before using extracted text."""
        return source_read(self.objects,owner,case,self._source(owner,case,identity))
