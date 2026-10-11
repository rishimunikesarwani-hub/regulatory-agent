"""Mumbai job metadata with conditional execution fences and versioned private S3 artifacts."""
import hashlib
import json
import time
import uuid

from botocore.exceptions import ClientError

from .contracts import COMPARISON_PROMPT, ContractError, SELECTED_PROMPTS, Snapshot
from .local import Store, encoded, identifier


class DynamoJobs:
    def __init__(self, cases, client, table, objects):
        if client.meta.region_name != 'ap-south-1' or client.meta.endpoint_url != 'https://dynamodb.ap-south-1.amazonaws.com':
            raise ValueError('mumbai_dynamodb_client_required')
        if client.meta.config.retries.get('total_max_attempts')!=1:
            raise ValueError('job_sdk_retries_denied')
        if not isinstance(table,str) or not table.strip(): raise ValueError('missing_jobs_table')
        self.cases, self.client, self.table, self.objects = cases, client, table, objects

    @staticmethod
    def _key(owner, case, identity):
        for value in (owner,case,identity): identifier(value)
        return {'PK':{'S':f'OWNER#{owner}'},'SK':{'S':f'JOB#{case}#{identity}'}}

    def _load(self, owner, case, identity, *, missing=False):
        self.cases.read(owner,case)
        key=self._key(owner,case,identity)
        item=self.client.get_item(TableName=self.table,Key=key,ConsistentRead=True).get('Item')
        if item is None:
            if missing: return 0,None
            raise ContractError('job_not_found')
        job=json.loads(item['body']['S']); revision=int(item['revision']['N'])
        if revision < 1 or any(item[k]!=key[k] for k in key) or \
                (job['owner_id'],job['case_id'],job['job_id']) != (owner,case,identity):
            raise ContractError('stored_job_scope_invalid')
        return revision,job

    def _save(self, owner, case, revision, job):
        body=encoded(job)
        # Leave room for keys and attribute names below DynamoDB's 400 KiB item limit.
        if len(body.encode()) > 390_000: raise ContractError('job_metadata_too_large')
        args={'TableName':self.table,'Item':self._key(owner,case,job['job_id']) |
            {'body':{'S':body},'revision':{'N':str(revision+1)}},
            'ConditionExpression':'#revision = :expected' if revision else 'attribute_not_exists(PK)'}
        if revision:
            args.update(ExpressionAttributeNames={'#revision':'revision'},ExpressionAttributeValues={':expected':{'N':str(revision)}})
        try:
            self.client.put_item(**args)
            return True
        except ClientError as error:
            if error.response['Error']['Code']=='ConditionalCheckFailedException': return False
            raise

    def _change(self, owner, case, identity, change):
        for _ in range(4):
            revision,job=self._load(owner,case,identity); before=encoded(job)
            result=change(job)
            if encoded(job)==before or self._save(owner,case,revision,job): return result
        raise ContractError('job_write_conflict')

    def _artifact(self, owner, case, identity, reference):
        if not isinstance(reference,dict) or not str(reference.get('upload_id','')).startswith(f'job-{identity}-'):
            raise ContractError('job_artifact_scope_invalid')
        raw=self.objects.read_extraction(owner,case,reference)
        if not isinstance(raw,bytes) or len(raw)!=reference['size_bytes'] or hashlib.sha256(raw).hexdigest()!=reference['sha256']:
            raise ContractError('job_artifact_integrity_failure')
        return json.loads(raw)

    def snapshot(self, owner, case, identity):
        _,job=self._load(owner,case,identity)
        snapshot=Snapshot.model_validate(self._artifact(owner,case,identity,job['snapshot_ref']))
        if (snapshot.case_id,snapshot.snapshot_id)!=(case,job['snapshot_id']):
            raise ContractError('job_snapshot_scope_invalid')
        return snapshot.model_dump(mode='json')

    def admit(self, owner, snapshot, key, *, data_mode='synthetic_live', now=None):
        snapshot=Snapshot.model_validate(snapshot.model_dump()); identifier(key)
        profile=self.cases.read(owner,snapshot.case_id)
        if not snapshot.synthetic or snapshot.mode!='historical' or snapshot.prompt_version not in SELECTED_PROMPTS|{COMPARISON_PROMPT} or \
                snapshot.model_version!='in.openai.gpt-5.6-luna' or snapshot.bank_profile!=profile.bank_profile:
            raise ContractError('cloud_job_scope_denied')
        case=snapshot.case_id
        identity=uuid.uuid5(uuid.NAMESPACE_URL,encoded(['cloud-job-v1',owner,case,key])).hex
        _,old=self._load(owner,case,identity,missing=True)
        body=snapshot.model_dump(mode='json')
        if old:
            if old['data_mode']!=data_mode or self.snapshot(owner,case,identity)!=body:
                raise ContractError('idempotency_conflict')
            return self.read_job(owner,case,identity)
        if data_mode!='synthetic_live': raise ContractError('cloud_job_mode_denied')
        reference=self.objects.save_extraction(owner,case,f'job-{identity}-{uuid.uuid4().hex}',encoded(body).encode())
        job=dict(job_id=identity,owner_id=owner,case_id=case,snapshot_id=snapshot.snapshot_id,snapshot_ref=reference,
            data_mode=data_mode,state='queued',stage=None,created_at=time.time() if now is None else now,
            started_at=None,deadline=None,token=None,lease_until=None,model_calls=0,retrieval_calls=0,stage_refs={},
            unchecked_obligations=[],stop_reason=None,freshness='unverified',authority_verified_at=None,label='Live')
        if not self._save(owner,case,0,job):
            return self.admit(owner,snapshot,key,data_mode=data_mode,now=now)
        return self.read_job(owner,case,identity)

    def read_job(self, owner, case, identity):
        _,job=self._load(owner,case,identity); stages={}
        for stage,saved in job['stage_refs'].items():
            value=self._artifact(owner,case,identity,saved['reference'])
            if sorted(value.get('accounted_obligations',[]))!=saved['accounted_obligations']:
                raise ContractError('stage_accounting_invalid')
            stages[stage]=value
        return job | {'stages':stages}

    _claimed=staticmethod(Store._claimed)

    def claim(self, owner, case, identity, now=None):
        def change(job):
            stamp=time.time() if now is None else now
            if job['state'] in {'completed','partial','failed'} or job['deadline'] is not None and stamp>=job['deadline']:
                return None
            if job['state']=='running' and job['lease_until']>stamp: return None
            if job['started_at'] is None: job.update(started_at=stamp,deadline=stamp+600)
            job.update(state='running',token=uuid.uuid4().hex,lease_until=min(stamp+30,job['deadline']))
            return job['token']
        return self._change(owner,case,identity,change)

    def reserve(self, owner, case, identity, token, kind, now=None):
        if kind not in {'model','retrieval'}: raise ContractError('invalid_allowance')
        field,maximum=('model_calls',24) if kind=='model' else ('retrieval_calls',20)
        def change(job):
            stamp=time.time() if now is None else now
            self._claimed(job,token,stamp)
            if job[field]>=maximum: raise ContractError('allowance_exhausted')
            job[field]+=1; job['lease_until']=min(stamp+30,job['deadline'])
            return job[field]
        return self._change(owner,case,identity,change)

    def renew(self, owner, case, identity, token, now=None):
        def change(job):
            stamp=time.time() if now is None else now
            self._claimed(job,token,stamp); job['lease_until']=min(stamp+30,job['deadline'])
        self._change(owner,case,identity,change)

    def save_stage(self, owner, case, identity, token, stage, output, now=None):
        identifier(stage)
        raw=encoded(output).encode()
        if len(raw)>400_000: raise ContractError('stage_too_large')
        accounted=output.get('accounted_obligations',[])
        if not isinstance(accounted,list) or not all(isinstance(o,str) for o in accounted) or \
                len(set(accounted))!=len(accounted) or not set(accounted)<=set(self.snapshot(owner,case,identity)['selected_obligations']):
            raise ContractError('stage_accounting_invalid')
        _,job=self._load(owner,case,identity); self._claimed(job,token,time.time() if now is None else now)
        digest=hashlib.sha256(raw).hexdigest(); saved=job['stage_refs'].get(stage)
        if saved and saved['reference']['sha256']!=digest: raise ContractError('immutable_stage')
        reference=saved['reference'] if saved else self.objects.save_extraction(owner,case,f'job-{identity}-{uuid.uuid4().hex}',raw)
        def change(job):
            stamp=time.time() if now is None else now
            self._claimed(job,token,stamp)
            previous=job['stage_refs'].get(stage)
            if previous:
                if previous['reference']['sha256']!=digest: raise ContractError('immutable_stage')
                return
            job['stage_refs'][stage]={'reference':reference,'accounted_obligations':sorted(accounted)}
            job.update(stage=stage,lease_until=min(stamp+30,job['deadline']))
        self._change(owner,case,identity,change)

    def finalize(self, owner, case, identity, token, state, unchecked, reason=None, now=None):
        required=set(self.snapshot(owner,case,identity)['selected_obligations'])
        if state not in {'completed','partial','failed'} or len(set(unchecked))!=len(unchecked) or not set(unchecked)<=required:
            raise ContractError('invalid_finalization')
        # Confirm artifact integrity before claiming that its accounted results were saved.
        self.read_job(owner,case,identity)
        def change(job):
            stamp=time.time() if now is None else now
            self._claimed(job,token,stamp,permit_expired=state!='completed')
            accounted={o for s in job['stage_refs'].values() for o in s['accounted_obligations']}
            if state=='completed' and (unchecked or not required<=accounted): raise ContractError('unchecked_obligations')
            if state=='partial' and (not accounted or set(unchecked)!=required-accounted): raise ContractError('invalid_partial_result')
            job.update(state=state,unchecked_obligations=unchecked,stop_reason=reason,finished_at=stamp)
        self._change(owner,case,identity,change)
