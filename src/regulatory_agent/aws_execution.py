"""Native historical admission and identifier-only SQS delivery with supervised execution."""
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import time
import uuid

from .assessment_selection import AssessmentSelection
from .contracts import ContractError
from .local import encoded, identifier
from .telemetry import StageAttempt


class CloudSelection(AssessmentSelection):
    def __init__(self, service, *, root=None):
        self.service,self.store=service,service.store
        if root is not None: self.root=Path(root)

    def _persist_sources(self, owner, case, selected):
        entries=json.loads((self.root/'data/sources/source-manifest.json').read_text(encoding='utf-8'))['versions']
        for source in selected:
            document=source['document']; identity=document['document_version_id']; body=source
            if document['kind']=='regulation':
                metadata=self.store._metadata(owner,case,'document',identity,missing=True)
                if metadata:
                    body=self.store._body(owner,case,'document',identity,metadata)
                else:
                    entry=next(e for e in entries if e['document_id']==document['source_id'] and e['version_id']==document['version'])
                    reference=self.store.objects.save_extraction(owner,case,'regulation-'+uuid.uuid4().hex,self._raw(entry))
                    body=source|{'original_ref':reference}
                if {k:v for k,v in body.items() if k!='original_ref'}!=source:
                    raise ContractError('source_integrity_failure')
                self.service._public_original(owner,case,body)
            try:
                self.store.put(owner,case,'document',identity,body)
            except ContractError as error:
                # A competing admission can save another exact version of the same original.
                if str(error)!='immutable_record' or document['kind']!='regulation': raise
                saved=self.store.get(owner,case,'document',identity)
                if {k:v for k,v in saved.items() if k!='original_ref'}!=source: raise
                self.service._public_original(owner,case,saved)


class AssessmentQueue:
    def __init__(self, service, client, url, account):
        if not isinstance(account,str) or not re.fullmatch(r'\d{12}',account) or \
                url!=f'https://sqs.ap-south-1.amazonaws.com/{account}/regulatory-agent-dev-assessments':
            raise ValueError('development_queue_required')
        if client.meta.region_name!='ap-south-1' or client.meta.endpoint_url!='https://sqs.ap-south-1.amazonaws.com' or \
                client.meta.config.retries.get('total_max_attempts')!=1:
            raise ValueError('mumbai_single_attempt_queue_required')
        self.service,self.client,self.url=service,client,url

    def send(self, owner, case, job_id):
        self.service._run(owner,case,job_id)
        job=self.service.store.read_job(owner,case,job_id)
        if job['state'] in {'completed','partial','failed'} or job['state']=='running' and job['lease_until']>time.time(): return job
        self.client.send_message(QueueUrl=self.url,MessageBody=encoded(
            {'version':1,'owner_id':owner,'case_id':case,'job_id':job_id}))
        return job


def stop_worker(service, owner, case, job_id, token, reason):
    store=service.store; job=store.read_job(owner,case,job_id)
    if job['state']!='running' or job['token']!=token: return job
    for body in service.reviews.records(owner,case,'stage_attempt'):
        if body['job_id']!=job_id or body['state']!='unknown': continue
        event=StageAttempt.model_validate_json(encoded(body))
        errors=('timeout' if reason=='worker_timeout' else 'interrupted',)
        if event.operation=='model': errors+=('unknown_outcome',)
        terminal=StageAttempt.model_validate(event.model_dump()|{'state':'interrupted',
            'finished_at':datetime.now(timezone.utc),'errors':errors})
        service.reviews.attempt(owner,case,terminal,execution_token=token,finish=True)
    # Re-read after attempt writes. Conditional finalization fences a newer execution claim.
    job=store.read_job(owner,case,job_id)
    accounted={o for stage in job['stages'].values() for o in stage.get('accounted_obligations',[])}
    snapshot=store.snapshot(owner,case,job_id)
    unchecked=[o for o in snapshot['selected_obligations'] if o not in accounted]
    store.finalize(owner,case,job_id,token,'partial' if accounted else 'failed',unchecked,reason)
    return store.read_job(owner,case,job_id)


def run_worker(service, owner, case, job_id, context):
    from .assessment_worker import supervise
    job=service.store.read_job(owner,case,job_id)
    if context.get_remaining_time_in_millis()<15_000: raise ContractError('worker_time_unavailable')
    if job['state'] in {'completed','partial','failed'}: return job
    if job['deadline'] is not None and time.time()>=job['deadline']:
        return stop_worker(service,owner,case,job_id,job['token'],'worker_timeout')
    def stop(store,owner,case,job_id,token,reason):
        return stop_worker(service,owner,case,job_id,token,reason)
    result=supervise(service.store,owner,case,job_id,bedrock_child,stop=stop,
        available_seconds=lambda:context.get_remaining_time_in_millis()/1000)
    if result['state'] not in {'completed','partial','failed'}:
        raise ContractError('worker_execution_unfinished')
    return result


def create_worker(service, queue_arn, *, process=run_worker):
    if not isinstance(queue_arn,str) or not re.fullmatch(r'arn:aws:sqs:ap-south-1:\d{12}:regulatory-agent-dev-assessments',queue_arn):
        raise ValueError('development_queue_required')
    def handle(event,context):
        rows=event.get('Records') if isinstance(event,dict) else None
        if not isinstance(rows,list) or len(rows)!=1: raise ContractError('single_queue_message_required')
        record=rows[0]
        if not isinstance(record,dict): raise ContractError('invalid_queue_message')
        message=record.get('messageId')
        try: identifier(message)
        except (TypeError,ValueError): raise ContractError('invalid_queue_message') from None
        try:
            if record.get('eventSource')!='aws:sqs' or record.get('eventSourceARN')!=queue_arn:
                raise ContractError('queue_scope_denied')
            raw=record.get('body')
            if not isinstance(raw,str) or len(raw.encode())>4096: raise ContractError('queue_message_invalid')
            body=json.loads(raw)
            if not isinstance(body,dict) or set(body)!={'version','owner_id','case_id','job_id'} or \
                    type(body['version']) is not int or body['version']!=1: raise ContractError('queue_message_invalid')
            for field in ('owner_id','case_id','job_id'): identifier(body[field])
            active=service() if callable(service) else service
            scope=(body['owner_id'],body['case_id'],body['job_id'])
            active._run(*scope)
            job=active.store.read_job(*scope)
            if job['state'] not in {'completed','partial','failed'}:
                process(active,*scope,context)
                if active.store.read_job(*scope)['state'] not in {'completed','partial','failed'}:
                    raise ContractError('worker_execution_unfinished')
            return {'batchItemFailures':[]}
        except Exception:
            return {'batchItemFailures':[{'itemIdentifier':message}]}
    return handle


def configured_service():
    """Trusted environment only. Do not reuse the case client's automatic write retries."""
    if os.environ.get('APP_ENV')!='aws' or os.environ.get('AWS_REGION')!='ap-south-1':
        raise ContractError('cloud_configuration_denied')
    import boto3
    from botocore.config import Config
    from .aws_cases import _configured_service, _configured_documents
    from .aws_records import DynamoRecords
    from .aws_assessments import CloudAssessments
    cases=_configured_service(); documents=_configured_documents()
    client=boto3.client('dynamodb',region_name='ap-south-1',endpoint_url='https://dynamodb.ap-south-1.amazonaws.com',
        config=Config(connect_timeout=2,read_timeout=4,retries={'mode':'standard','total_max_attempts':1}))
    return CloudAssessments(cases,documents,DynamoRecords(cases,client,cases.repository.table_name,documents.objects))


def bedrock_child(owner, case, job_id, token):
    from .assessment_pipeline import AssessmentPipeline
    from .bedrock_model import BedrockModel
    service=configured_service(); run,snapshot=service._run(owner,case,job_id)
    service.store._claimed(service.store.read_job(owner,case,job_id),token,time.time())
    if run['data_mode']!='synthetic_live' or not snapshot['synthetic'] or snapshot['mode']!='historical':
        raise ContractError('private_model_processing_unverified')
    AssessmentPipeline(service,BedrockModel.configured()).run(owner,case,job_id,execution_token=token)


def handler(event,context):
    return create_worker(configured_service,os.environ.get('ASSESSMENT_QUEUE_ARN',''))(event,context)
