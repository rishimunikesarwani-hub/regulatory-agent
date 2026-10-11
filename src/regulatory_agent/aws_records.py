"""Native assessment metadata and execution-fenced records with private versioned S3 bodies."""
import hashlib
import json
import time
import uuid

from botocore.exceptions import ClientError

from .aws_jobs import DynamoJobs
from .contracts import ContractError
from .local import Store, encoded, identifier


class DynamoRecords(DynamoJobs):
    save_snapshot = Store.save_snapshot

    def sources(self, owner, case, snapshot):
        from .aws_documents import source_read
        return [source_read(self.objects,owner,case,s) if s['document']['kind']!='regulation' and 'passages' not in s else s
                for s in Store.sources(self,owner,case,snapshot)]

    @staticmethod
    def record_key(owner, case, kind, identity):
        for value in (owner,case,kind,identity): identifier(value)
        if kind not in {'document','snapshot','run','finding','review','stage_attempt','review_unit','comparison'}:
            raise ContractError('invalid_record_kind')
        return {'PK':{'S':f'OWNER#{owner}'},'SK':{'S':f'RECORD#{case}#{kind}#{identity}'}}

    @staticmethod
    def _prefix(owner, case, kind, identity):
        return 'record-'+uuid.uuid5(uuid.NAMESPACE_URL,encoded([owner,case,kind,identity])).hex+'-'

    def _metadata(self, owner, case, kind, identity, *, missing=False):
        self.cases.read(owner,case); key=self.record_key(owner,case,kind,identity)
        item=self.client.get_item(TableName=self.table,Key=key,ConsistentRead=True).get('Item')
        if item is None:
            if missing: return None
            raise ContractError('record_not_found')
        self._scope(owner,case,kind,identity,item)
        return item

    def _scope(self, owner, case, kind, identity, item):
        key=self.record_key(owner,case,kind,identity)
        if any(item[k]!=key[k] for k in key) or int(item['revision']['N'])<1 or any(
                item[field]['S']!=value for field,value in (('owner_id',owner),('case_id',case),('kind',kind),('record_id',identity))):
            raise ContractError('stored_record_scope_invalid')

    def _body(self, owner, case, kind, identity, item):
        self._scope(owner,case,kind,identity,item)
        reference=json.loads(item['reference']['S'])
        if not reference.get('upload_id','').startswith(self._prefix(owner,case,kind,identity)):
            raise ContractError('record_artifact_scope_invalid')
        raw=self.objects.read_extraction(owner,case,reference)
        if not isinstance(raw,bytes) or len(raw)!=reference['size_bytes'] or hashlib.sha256(raw).hexdigest()!=reference['sha256']:
            raise ContractError('record_artifact_integrity_failure')
        body=json.loads(raw)
        self.body_scope(owner,case,kind,identity,body)
        return body

    @staticmethod
    def body_scope(owner, case, kind, identity, body):
        if not isinstance(body,dict) or body.get('owner_id',owner)!=owner or body.get('case_id',case)!=case:
            raise ContractError('forged_scope')
        if kind=='document':
            document=body.get('document',{})
            if (document.get('case_id'),document.get('document_version_id'))!=(case,identity):
                raise ContractError('record_body_scope_invalid')
        else:
            field={'snapshot':'snapshot_id','run':'run_id','finding':'finding_id','review':'event_id','stage_attempt':'event_id','comparison':'comparison_id'}.get(kind)
            if field and body.get(field)!=identity: raise ContractError('record_body_scope_invalid')

    def get(self, owner, case, kind, identity):
        return self._body(owner,case,kind,identity,self._metadata(owner,case,kind,identity))

    def records(self, owner, case, kind):
        self.cases.read(owner,case); self.record_key(owner,case,kind,'validate')
        args=dict(TableName=self.table,ConsistentRead=True,KeyConditionExpression='PK = :owner AND begins_with(SK, :prefix)',
            ExpressionAttributeValues={':owner':{'S':f'OWNER#{owner}'},':prefix':{'S':f'RECORD#{case}#{kind}#'}})
        records=[]
        while True:
            response=self.client.query(**args)
            records.extend(self._body(owner,case,kind,item['record_id']['S'],item) for item in response.get('Items',[]))
            if not response.get('LastEvaluatedKey'): return records
            args['ExclusiveStartKey']=response['LastEvaluatedKey']

    def prepare(self, owner, case, kind, identity, body, revision=0):
        self.cases.read(owner,case); key=self.record_key(owner,case,kind,identity)
        self.body_scope(owner,case,kind,identity,body)
        raw=encoded(body).encode()
        if len(raw)>400_000: raise ContractError('record_too_large')
        reference=self.objects.save_extraction(owner,case,self._prefix(owner,case,kind,identity)+uuid.uuid4().hex,raw)
        return key | {'owner_id':{'S':owner},'case_id':{'S':case},'kind':{'S':kind},'record_id':{'S':identity},
            'reference':{'S':encoded(reference)},'revision':{'N':str(revision+1)}}

    def commit(self, owner, case, changes, *, job_id=None, token=None, permit_expired=False):
        self.cases.read(owner,case); actions=[]
        # Read after S3 writes. A job revision condition fences a concurrent claim change.
        if token is not None:
            revision,job=self._load(owner,case,job_id)
            self._claimed(job,token,time.time(),permit_expired=permit_expired)
            actions.append({'ConditionCheck':{'TableName':self.table,'Key':self._key(owner,case,job_id),
                'ConditionExpression':'#revision = :expected','ExpressionAttributeNames':{'#revision':'revision'},
                'ExpressionAttributeValues':{':expected':{'N':str(revision)}}}})
        for item in changes:
            self._scope(owner,case,item['kind']['S'],item['record_id']['S'],item)
            old=int(item['revision']['N'])-1
            put={'TableName':self.table,'Item':item,'ConditionExpression':'#revision = :expected' if old else 'attribute_not_exists(PK)'}
            if old: put.update(ExpressionAttributeNames={'#revision':'revision'},ExpressionAttributeValues={':expected':{'N':str(old)}})
            actions.append({'Put':put})
        try:
            self.client.transact_write_items(TransactItems=actions)
            return True
        except ClientError as error:
            reasons=error.response.get('CancellationReasons',[])
            if error.response['Error']['Code']=='TransactionCanceledException' and reasons and \
                    any(r.get('Code')=='ConditionalCheckFailed' for r in reasons) and \
                    all(r.get('Code') in {'None','ConditionalCheckFailed'} for r in reasons): return False
            raise

    def put(self, owner, case, kind, identity, body):
        for _ in range(4):
            old=self._metadata(owner,case,kind,identity,missing=True)
            if old:
                if self._body(owner,case,kind,identity,old)!=body: raise ContractError('immutable_record')
                return
            item=self.prepare(owner,case,kind,identity,body)
            if self.commit(owner,case,[item]): return
        raise ContractError('record_write_conflict')
