"""Native admission, SQS transport, and worker cleanup with no external traffic."""
import copy
from datetime import datetime, timezone
import hashlib
import json
import time
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from botocore.config import Config
from botocore.session import Session
from botocore.validate import validate_parameters

import test_slice05_cloud_jobs as jobs
import test_slice05_cloud_records as records
import test_slice05_worker as workers
from regulatory_agent.cases import CaseError, CaseService
from regulatory_agent.contracts import ContractError, StartAssessment
from regulatory_agent.aws_cases import DynamoDBCases
from regulatory_agent.aws_documents import CloudDocuments
from regulatory_agent.aws_records import DynamoRecords
from regulatory_agent.aws_assessments import CloudAssessments


ACCOUNT='482439369658'
QUEUE=f'https://sqs.ap-south-1.amazonaws.com/{ACCOUNT}/regulatory-agent-dev-assessments'
ARN=f'arn:aws:sqs:ap-south-1:{ACCOUNT}:regulatory-agent-dev-assessments'


class Objects(jobs.Artifacts):
    def __init__(self): super().__init__(); self.originals={}
    def grant(self,*args): return {}
    def pin(self,owner,case,identity,size):
        raw=self.originals[(owner,case,identity)]
        if len(raw)!=size: raise ContractError('original_size_invalid')
        return {'upload_id':identity,'size_bytes':size,'sha256':hashlib.sha256(raw).hexdigest(),'version_id':'original-v1'},raw
    def read(self,owner,case,reference):
        raw=self.originals[(owner,case,reference['upload_id'])]
        if len(raw)!=reference['size_bytes'] or hashlib.sha256(raw).hexdigest()!=reference['sha256']:
            raise ContractError('original_integrity_failure')
        return raw


class SQS:
    meta=SimpleNamespace(region_name='ap-south-1',endpoint_url='https://sqs.ap-south-1.amazonaws.com',
        config=Config(retries={'mode':'standard','total_max_attempts':1}))
    def __init__(self): self.sent=[]; self.lost_ack=False; self.model=Session().get_service_model('sqs')
    def send_message(self,**args):
        validate_parameters(args,self.model.operation_model('SendMessage').input_shape)
        self.sent.append(copy.deepcopy(args))
        if self.lost_ack: self.lost_ack=False; raise OSError('Uncertain send acknowledgement')
        return {'MessageId':str(len(self.sent))}


class CloudAdmissionTests(unittest.TestCase):
    def setUp(self):
        self.client=records.RecordsDynamo(); self.objects=Objects(); self.owner='native-admission-owner'
        self.cases=CaseService(DynamoDBCases(self.client,'cases'))
        self.case=self.cases.create(self.owner,{'bank_profile':{'name':'Fictional selected bank'},'synthetic':True}).case_id
        self.documents=CloudDocuments(self.cases,self.client,'cases',self.objects)
        self.store=DynamoRecords(self.cases,self.client,'cases',self.objects)
        self.service=CloudAssessments(self.cases,self.documents,self.store)
        raw=('Fictional access control. Review privileged access monthly.\n'*510).encode()
        upload=self.documents.reserve(self.owner,self.case,{'x-filename':'fictional.txt','x-document-kind':'policy',
            'x-synthetic':'true'},len(raw),'bank-upload')
        self.version=upload['upload_id']; self.objects.originals[(self.owner,self.case,self.version)]=raw
        self.documents.finalize(self.owner,self.case,self.version)
        from regulatory_agent.aws_execution import CloudSelection, AssessmentQueue
        self.selection=CloudSelection(self.service); self.sqs=SQS()
        self.queue=AssessmentQueue(self.service,self.sqs,QUEUE,ACCOUNT)
        catalog=self.selection.catalog(self.owner,self.case)
        self.regulation=next(s for s in catalog['sources'] if s['document']['kind']=='regulation')
        bank=next(s for s in catalog['sources'] if s['document']['kind']=='policy')
        self.request=StartAssessment(selected_versions={self.regulation['document']['source_id']:self.regulation['document']['version'],
            bank['document']['source_id']:bank['document']['version']},selected_obligations=[catalog['obligations'][0]['obligation_id']],
            assessment_date='2024-04-08',mode='historical',idempotency_key='native-admit')

    def admit(self,request=None): return self.selection.admit(self.owner,self.case,request or self.request)

    def test_ce01_native_admission_saves_exact_originals_without_local_storage(self):
        run=self.admit(); snapshot=self.store.get(self.owner,self.case,'snapshot',run['snapshot_id'])
        self.assertFalse(hasattr(self.store,'path')); self.assertFalse(hasattr(self.store,'transaction'))
        self.assertEqual(snapshot['selected_document_ids'][self.version],self.version)
        sources=self.service._sources(self.owner,self.case,snapshot)
        self.assertEqual(len(next(s for s in sources if s['document']['kind']=='policy')['passages']),510)
        source=next(s for s in sources if s['document']['kind']=='regulation')
        raw=self.service._public_original(self.owner,self.case,source)
        self.assertEqual(hashlib.sha256(raw).hexdigest(),source['document']['sha256'])
        self.assertEqual(self.store.read_job(self.owner,self.case,run['job_id'])['state'],'queued')
        self.assertEqual(len(self.service.list(self.owner,self.case)['runs']),1)

    def test_ce02_admission_retry_keeps_original_references_and_rejects_changed_selection(self):
        first=self.admit(); count=len(self.objects.data); before=self.store.records(self.owner,self.case,'document')
        self.assertEqual(self.admit(),first); self.assertEqual(len(self.objects.data),count)
        self.assertEqual(self.store.records(self.owner,self.case,'document'),before)
        with self.assertRaises(CaseError): self.admit(self.request.model_copy(update={'assessment_date':'2024-04-09'}))
        self.assertEqual(len(self.service.list(self.owner,self.case)['runs']),1)

    def test_ce03_full_bank_reads_verify_original_and_keep_public_pagination(self):
        page=self.documents.read(self.owner,self.case,self.version)
        self.assertEqual(len(page['passages']),500); self.assertEqual(page['next_offset'],500)
        full=self.documents.read_full(self.owner,self.case,self.version)
        self.assertEqual(len(full['passages']),510)
        self.objects.originals[(self.owner,self.case,self.version)]=b'changed fictional original'
        with self.assertRaisesRegex(ContractError,'original_integrity_failure'): self.admit()
        self.assertEqual(self.service.list(self.owner,self.case)['runs'],[])

    def test_ce04_current_mode_and_other_owner_do_not_admit_or_send(self):
        with self.assertRaises(CaseError): self.admit(self.request.model_copy(update={'mode':'current'}))
        with self.assertRaises(CaseError): self.selection.admit('other-owner',self.case,self.request)
        self.assertEqual(self.sqs.sent,[]); self.assertEqual(self.service.list(self.owner,self.case)['runs'],[])

    def test_ce05_queue_rejects_invalid_native_client_configuration(self):
        from regulatory_agent.aws_execution import AssessmentQueue
        for values in ({'region_name':'us-east-1'},{'endpoint_url':'https://sqs.ap-south-1.amazonaws.com.evil.invalid'},
                       {'config':Config(retries={'total_max_attempts':2})}):
            client=SQS(); client.meta=SimpleNamespace(**(vars(SQS.meta)|values))
            with self.assertRaises(ValueError): AssessmentQueue(self.service,client,QUEUE,ACCOUNT)
        for queue,account in ((QUEUE,'000000000000'),(QUEUE+'?redirect=other',ACCOUNT),(QUEUE+'.fifo',ACCOUNT)):
            with self.assertRaises(ValueError): AssessmentQueue(self.service,SQS(),queue,account)

    def test_ce06_uncertain_send_retry_preserves_admission_and_identifier_only_message(self):
        first=self.admit(); self.sqs.lost_ack=True
        with self.assertRaises(OSError): self.queue.send(self.owner,self.case,first['job_id'])
        retry=self.admit(); self.queue.send(self.owner,self.case,retry['job_id'])
        self.assertEqual(retry,first); self.assertEqual(len(self.service.list(self.owner,self.case)['runs']),1)
        self.assertEqual(self.sqs.sent[0],self.sqs.sent[1])
        body=json.loads(self.sqs.sent[0]['MessageBody'])
        self.assertEqual(body,{'version':1,'owner_id':self.owner,'case_id':self.case,'job_id':first['job_id']})
        self.assertEqual(set(self.sqs.sent[0]),{'QueueUrl','MessageBody'})

    def test_ce07_terminal_and_active_jobs_do_not_enqueue_another_execution(self):
        run=self.admit(); job=run['job_id']; token=self.store.claim(self.owner,self.case,job)
        self.assertEqual(self.queue.send(self.owner,self.case,job)['state'],'running'); self.assertEqual(self.sqs.sent,[])
        self.store.finalize(self.owner,self.case,job,token,'failed',self.request.selected_obligations)
        self.assertEqual(self.queue.send(self.owner,self.case,job)['state'],'failed'); self.assertEqual(self.sqs.sent,[])
        with self.assertRaises(CaseError): self.queue.send('other-owner',self.case,job)

    def test_ce15_changed_run_snapshot_cannot_replace_pinned_job_snapshot(self):
        run=self.admit(); metadata=self.store._metadata(self.owner,self.case,'snapshot',run['snapshot_id'])
        original=self.store.get(self.owner,self.case,'snapshot',run['snapshot_id'])
        replacement=self.store.prepare(self.owner,self.case,'snapshot',run['snapshot_id'],
            original|{'assessment_date':'2024-04-09'},int(metadata['revision']['N']))
        self.client.items[self.client.key(replacement)]=replacement
        with self.assertRaisesRegex(ContractError,'run_snapshot_scope_invalid'):
            self.queue.send(self.owner,self.case,run['job_id'])
        self.assertEqual(self.sqs.sent,[])


class CloudWorkerTests(unittest.TestCase):
    def setUp(self):
        self.f=records.CloudRecordTests('runTest'); self.f.setUp(); self.addCleanup(self.f.doCleanups)
        self.service=self.f.service; self.store=self.f.store; self.scope=(self.f.owner,self.f.case,self.f.job)
        self.context=SimpleNamespace(get_remaining_time_in_millis=lambda:660_000)

    def message(self,**changes):
        return {'messageId':'message-1','eventSource':'aws:sqs','eventSourceARN':ARN,
            'body':json.dumps({'version':1,'owner_id':self.f.owner,'case_id':self.f.case,'job_id':self.f.job})}|changes

    def test_ce08_queue_event_rejection_happens_before_service_construction(self):
        from regulatory_agent.aws_execution import create_worker
        calls=[]
        worker=create_worker(lambda:calls.append('service'),ARN)
        for message in (self.message(eventSourceARN=ARN.replace('ap-south-1','us-east-1')),
                        self.message(eventSource='http'),self.message(body='not-json'),
                        self.message(body=json.dumps({'version':True,'owner_id':self.f.owner,'case_id':self.f.case,'job_id':self.f.job})),
                        self.message(body=json.dumps({'version':1,'owner_id':self.f.owner,'case_id':self.f.case,'job_id':self.f.job,'prompt':'private text'}))):
            self.assertEqual(worker({'Records':[message]},self.context),{'batchItemFailures':[{'itemIdentifier':'message-1'}]})
        self.assertEqual(calls,[])
        with self.assertRaises(ContractError): worker({'Records':[self.message(),self.message()]},self.context)
        self.assertEqual(calls,[])

    def test_ce09_worker_uses_saved_run_and_reports_uncertain_delivery(self):
        from regulatory_agent.aws_execution import create_worker
        received=[]
        def process(service,owner,case,job,context):
            received.append((service,owner,case,job,context)); raise OSError('PRIVATE exception')
        worker=create_worker(self.service,ARN,process=process)
        result=worker({'Records':[self.message()]},self.context)
        self.assertEqual(received[0],(self.service,*self.scope,self.context))
        self.assertEqual(result,{'batchItemFailures':[{'itemIdentifier':'message-1'}]}); self.assertNotIn('PRIVATE',str(result))
        unfinished=create_worker(self.service,ARN,process=lambda *args:{'state':'completed'})
        self.assertEqual(unfinished({'Records':[self.message()]},self.context),result)
        self.store.finalize(*self.scope,self.f.token,'failed',self.f.snapshot.selected_obligations)
        received.clear(); self.assertEqual(worker({'Records':[self.message()]},self.context),{'batchItemFailures':[]})
        self.assertEqual(received,[])

    def test_ce10_insufficient_invocation_time_leaves_job_without_child_or_new_claim(self):
        from regulatory_agent.aws_execution import run_worker
        before=self.store.read_job(*self.scope)
        context=SimpleNamespace(get_remaining_time_in_millis=lambda:1000)
        with patch('regulatory_agent.assessment_worker.multiprocessing.get_context') as factory:
            with self.assertRaisesRegex(ContractError,'worker_time_unavailable'): run_worker(self.service,*self.scope,context)
        factory.assert_not_called(); self.assertEqual(self.store.read_job(*self.scope),before)
        run=self.service.reviews.admit(self.f.owner,self.f.case,'queued-run',self.f.snapshot.snapshot_id,'synthetic_live')
        scope=(self.f.owner,self.f.case,run['job_id']); before=self.store.read_job(*scope)
        context=SimpleNamespace(get_remaining_time_in_millis=lambda:601_000)
        with self.assertRaisesRegex(ContractError,'worker_time_unavailable'): run_worker(self.service,*scope,context)
        self.assertEqual(self.store.read_job(*scope),before); self.assertIsNone(before['started_at'])

    def expire(self):
        def change(job): job.update(deadline=time.time()-1,lease_until=time.time()-2)
        self.store._change(*self.scope,change)

    def test_ce11_expired_delivery_preserves_partial_results_and_never_starts_child(self):
        from regulatory_agent.aws_execution import run_worker
        self.store.reserve(*self.scope,self.f.token,'model')
        self.f.present(); self.store.save_stage(*self.scope,self.f.token,'saved',{'accounted_obligations':['O1']})
        self.expire(); before=self.store.read_job(*self.scope)
        with patch('regulatory_agent.assessment_worker.multiprocessing.get_context') as factory:
            result=run_worker(self.service,*self.scope,self.context)
        factory.assert_not_called(); self.assertEqual(result['state'],'partial'); self.assertEqual(result['unchecked_obligations'],['O2'])
        self.assertEqual(result['model_calls'],1); self.assertEqual(result['deadline'],before['deadline'])
        self.assertEqual(len(self.store.records(self.f.owner,self.f.case,'finding')),1)

    def test_ce12_interrupted_unknown_dispatch_stays_unknown_in_report(self):
        from regulatory_agent.aws_execution import stop_worker
        event=self.f.event(); self.f.reviews.attempt(self.f.owner,self.f.case,event,execution_token=self.f.token)
        self.store.reserve(*self.scope,self.f.token,'model'); self.expire()
        result=stop_worker(self.service,*self.scope,self.f.token,'worker_timeout')
        self.assertEqual(result['state'],'failed')
        report=self.service.read(*self.scope); self.assertIsNone(report['live_model_calls'])
        attempt=report['trace']['attempts'][0]; self.assertEqual(attempt['state'],'interrupted')
        self.assertIn('unknown_outcome',attempt['errors']); self.assertIsNone(attempt['usage']['input_tokens'])

    def test_ce13_replaced_claim_and_unknown_storage_ack_are_not_terminal_success(self):
        from regulatory_agent.aws_execution import stop_worker
        before=self.store.read_job(*self.scope)
        self.store._change(*self.scope,lambda job:job.update(token='newer-token'))
        result=stop_worker(self.service,*self.scope,before['token'],'worker_timeout')
        self.assertEqual(result['token'],'newer-token'); self.assertEqual(result['state'],'running')
        with patch.object(self.store,'finalize',side_effect=OSError('PRIVATE uncertain write')):
            with self.assertRaises(OSError): stop_worker(self.service,*self.scope,'newer-token','worker_crashed')
        self.assertEqual(self.store.read_job(*self.scope)['state'],'running')

    def test_ce14_shared_supervisor_stops_real_child_before_returning(self):
        from regulatory_agent.assessment_worker import supervise
        fixture=workers.WorkerTests('runTest'); fixture.setUp(); self.addCleanup(fixture.doCleanups)
        fixture.remaining(1); marker=fixture.store.path.parent/'cloud-supervision-late.txt'; finalized=[]
        def stop(store,owner,case,job,token,reason):
            from regulatory_agent.assessment_worker import _stop
            finalized.append(reason); return _stop(store,owner,case,job,token,reason)
        result=supervise(fixture.store,*fixture.scope,workers.hanging_child,
            args=(str(fixture.store.path),str(marker)),stop=stop,available_seconds=lambda:660)
        self.assertEqual(result['state'],'failed'); self.assertEqual(finalized,['worker_timeout']); self.assertFalse(marker.exists())


if __name__=='__main__': unittest.main()
