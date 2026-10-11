"""Native assessment persistence with controlled SDK responses, not deployed acceptance."""
import copy
from datetime import datetime, timezone
import hashlib
import json
import time
import unittest
from concurrent.futures import ThreadPoolExecutor

from botocore.exceptions import ClientError
from botocore.validate import validate_parameters

from regulatory_agent.contracts import ContractError, ModelReply, PERIOD_PROMPT, ReviewCohort, ReviewItem, ReviewRequest
from regulatory_agent.local import validated_action
from regulatory_agent.telemetry import StageAttempt, VersionMetadata
import test_slice05_cloud_jobs as cloud_jobs
import test_slice05_pipeline as pipeline_tests


class RecordsDynamo(cloud_jobs.Dynamo):
    def __init__(self):
        super().__init__(); self.page_size=2; self.before_transaction=None

    def query(self, **args):
        validate_parameters(args,self.model.operation_model('Query').input_shape)
        with self.lock:
            self.calls.append(('query',copy.deepcopy(args)))
            values=args['ExpressionAttributeValues']; owner=values[':owner']['S']; prefix=values[':prefix']['S']
            rows=sorted((k,v) for k,v in self.items.items() if k[0]==owner and k[1].startswith(prefix))
            start=self.key(args['ExclusiveStartKey']) if args.get('ExclusiveStartKey') else None
            rows=[(k,v) for k,v in rows if start is None or k>start]
            page=rows[:self.page_size]; response={'Items':[copy.deepcopy(v) for _,v in page]}
            if len(rows)>self.page_size: response['LastEvaluatedKey']={k:page[-1][1][k] for k in ('PK','SK')}
            return response

    def transact_write_items(self, **args):
        validate_parameters(args,self.model.operation_model('TransactWriteItems').input_shape)
        if self.before_transaction:
            callback,self.before_transaction=self.before_transaction,None; callback()
        with self.lock:
            self.calls.append(('transaction',copy.deepcopy(args))); reasons=[]; changes=[]
            for action in args['TransactItems']:
                name,operation=next(iter(action.items())); key=self.key(operation.get('Item',operation.get('Key')))
                old=self.items.get(key); condition=operation['ConditionExpression']
                expected=operation.get('ExpressionAttributeValues',{}).get(':expected',{}).get('N')
                matches=old is None if condition=='attribute_not_exists(PK)' else old is not None and old['revision']['N']==expected
                reasons.append({'Code':'None' if matches else 'ConditionalCheckFailed'})
                if name=='Put': changes.append((key,operation['Item']))
            if any(r['Code']!='None' for r in reasons):
                raise ClientError({'Error':{'Code':'TransactionCanceledException'},'CancellationReasons':reasons},'TransactWriteItems')
            if self.failure: raise self.failure
            for key,item in changes: self.items[key]=copy.deepcopy(item)
            if self.lost_ack:
                self.lost_ack=False; raise OSError('Uncertain transaction acknowledgement')
        return {}


class CloudRecordTests(unittest.TestCase):
    def setUp(self):
        from regulatory_agent.aws_records import DynamoRecords
        from regulatory_agent.aws_assessments import CloudAssessments
        from regulatory_agent.aws_cases import DynamoDBCases
        from regulatory_agent.cases import CaseService
        self.client=RecordsDynamo(); self.objects=cloud_jobs.Artifacts(); self.owner='cloud-record-operator'
        self.cases=CaseService(DynamoDBCases(self.client,'cases'))
        self.case=self.cases.create(self.owner,{'bank_profile':{'name':'Fictional cloud bank'},'synthetic':True}).case_id
        self.store=DynamoRecords(self.cases,self.client,'cases',self.objects)
        source=cloud_jobs.CloudJobTests('runTest'); source.setUp()
        self.snapshot=source.snapshot.model_copy(update={'case_id':self.case,'bank_profile':{'name':'Fictional cloud bank'}})
        self.store.save_snapshot(self.owner,self.snapshot)
        self.service=CloudAssessments(self.cases,None,self.store)
        self.reviews=self.service.reviews
        self.run=self.reviews.admit(self.owner,self.case,'run-1',self.snapshot.snapshot_id,'synthetic_live')
        self.job=self.run['job_id']; self.token=self.store.claim(self.owner,self.case,self.job)

    def item(self, identity='finding-1', obligation='O1'):
        return ReviewItem(finding_id=identity,run_id='run-1',snapshot_id=self.snapshot.snapshot_id,obligation_id=obligation,
            control_ids=[],status='needs_review',evidence_condition='missing',citations=[],rationale='Evidence is missing.',
            remedy='Supply records.',primary_recommendation='Supply records.',gap_kind='evidence',
            available_at=datetime.now(timezone.utc).isoformat(),model_id=self.snapshot.model_version,
            prompt_version=PERIOD_PROMPT,data_mode='synthetic_live',source_version_ids=['rbi:v1','bank:v1'])

    def present(self, item=None):
        return self.reviews.present(self.owner,self.case,item or self.item(),execution_token=self.token)

    def request(self, key='review-1', revision=0, disposition='approved', item=None):
        return ReviewRequest(event_kind='final_review',disposition=disposition,expected_revision=revision,
            idempotency_key=key,accepted_content=(item or self.item()).original_content() if disposition=='approved' else None,
            reason='Additional evidence is necessary.' if disposition=='rejected' else None)

    def event(self):
        return StageAttempt(event_id='attempt-event',attempt_id='attempt-1',run_id='run-1',job_id=self.job,
            snapshot_id=self.snapshot.snapshot_id,stage_id='extract',stage='model_call',operation='model',
            state='unknown',dispatched=False,started_at=datetime.now(timezone.utc),finished_at=None,duration_seconds=None,
            model_id=self.snapshot.model_version,
            versions=VersionMetadata(application='vs5-v1',schema='v1',extraction='v1',chunking='v1',retrieval='v1',prompt=PERIOD_PROMPT,
                model_configuration='controlled-native-v1'))

    def test_cr01_immutable_large_records_keep_exact_artifact_references(self):
        body={'document':{'case_id':self.case,'document_version_id':'large'},'private_text':'x'*395_000}
        self.store.put(self.owner,self.case,'document','large',body)
        self.assertEqual(self.store.get(self.owner,self.case,'document','large'),body)
        before=len(self.objects.data); self.store.put(self.owner,self.case,'document','large',body)
        self.assertEqual(len(self.objects.data),before)
        with self.assertRaisesRegex(ContractError,'immutable_record'):
            self.store.put(self.owner,self.case,'document','large',body|{'private_text':'changed'})
        record=next(v for k,v in self.client.items.items() if k[1].endswith('#document#large'))
        self.assertLess(len(json.dumps(record)),2000)
        self.assertNotIn('private_text',json.dumps(record))

    def test_cr02_scope_and_corrupt_artifacts_fail_before_content_disclosure(self):
        self.store.put(self.owner,self.case,'document','original',{'document':{'case_id':self.case,'document_version_id':'original'},'text':'Fictional text'})
        before=len(self.objects.calls)
        from regulatory_agent.cases import CaseError
        with self.assertRaises(CaseError): self.store.get('other',self.case,'document','original')
        self.assertEqual(len(self.objects.calls),before)
        key=next(k for k in self.client.items if k[1].endswith('#document#original'))
        original=copy.deepcopy(self.client.items[key]); self.client.items[key]['case_id']['S']='other'
        with self.assertRaises(ContractError): self.store.get(self.owner,self.case,'document','original')
        self.client.items[key]=original
        reference=json.loads(original['reference']['S'])
        self.objects.data[(self.owner,self.case,reference['upload_id'],reference['version_id'])]=b'corrupt'
        with self.assertRaises(ContractError): self.store.get(self.owner,self.case,'document','original')

    def test_cr03_query_pagination_is_complete_strong_and_scoped(self):
        for n in range(5): self.store.put(self.owner,self.case,'document',f'd{n}',{'n':n,'document':{'case_id':self.case,'document_version_id':f'd{n}'}})
        self.assertEqual({v['n'] for v in self.store.records(self.owner,self.case,'document')},set(range(5)))
        calls=[v for op,v in self.client.calls if op=='query']
        self.assertEqual(len(calls),3); self.assertTrue(all(v['ConsistentRead'] for v in calls))
        self.assertTrue(all(v['ExpressionAttributeValues'][':prefix']['S']==f'RECORD#{self.case}#document#' for v in calls))

    def test_cr04_claim_changed_during_artifact_save_cannot_commit(self):
        def replace_claim():
            self.store.claim(self.owner,self.case,self.job,now=time.time()+31)
        self.client.before_transaction=replace_claim
        with self.assertRaisesRegex(ContractError,'stale_execution_claim'): self.present()
        self.assertEqual(self.store.records(self.owner,self.case,'finding'),[])
        event=self.event()
        with self.assertRaises(ContractError): self.reviews.attempt(self.owner,self.case,event,execution_token=self.token)

    def test_cr05_concurrent_duplicate_obligation_cannot_present_twice(self):
        def save(n):
            try: return self.present(self.item(f'finding-{n}'))
            except ContractError: return None
        with ThreadPoolExecutor(max_workers=2) as pool: values=list(pool.map(save,range(2)))
        self.assertEqual(sum(v is not None for v in values),1)
        self.assertEqual(len(self.store.records(self.owner,self.case,'finding')),1)
        saved=next(v for v in values if v is not None)
        self.assertEqual(self.present(saved),saved)

    def test_cr06_attempt_terminal_transition_is_fenced_and_immutable(self):
        event=self.event(); self.reviews.attempt(self.owner,self.case,event,execution_token=self.token)
        terminal=event.model_copy(update={'state':'succeeded','dispatched':True,'finished_at':datetime.now(timezone.utc),'duration_seconds':0.01})
        self.reviews.attempt(self.owner,self.case,terminal,execution_token=self.token,finish=True)
        with self.assertRaisesRegex(ContractError,'attempt_already_terminal'):
            self.reviews.attempt(self.owner,self.case,terminal,execution_token=self.token,finish=True)
        self.assertEqual(len(self.store.records(self.owner,self.case,'stage_attempt')),1)
        forged=event.model_copy(update={'snapshot_id':'outside'})
        with self.assertRaises(ContractError): self.reviews.attempt(self.owner,self.case,forged,execution_token=self.token)

    def test_cr07_reviews_keep_originals_and_return_delayed_duplicate(self):
        item=self.present(); first=self.reviews.save(self.owner,self.case,item.finding_id,self.request(item=item))
        second=self.reviews.save(self.owner,self.case,item.finding_id,self.request('review-2',1,'rejected'))
        self.assertEqual(second.revision,2)
        self.assertEqual(self.reviews.save(self.owner,self.case,item.finding_id,self.request(item=item)),first)
        with self.assertRaisesRegex(ContractError,'idempotency_conflict'):
            self.reviews.save(self.owner,self.case,item.finding_id,self.request('review-1',0,'rejected'))
        with self.assertRaisesRegex(ContractError,'revision_conflict'):
            self.reviews.save(self.owner,self.case,item.finding_id,self.request('review-3',0,'rejected'))
        self.assertEqual(self.store.get(self.owner,self.case,'finding',item.finding_id),item.model_dump(mode='json'))

    def test_cr08_competing_reviews_and_lost_ack_keep_one_event(self):
        item=self.present()
        def save(n):
            try: return self.reviews.save(self.owner,self.case,item.finding_id,self.request(f'key-{n}',item=item))
            except ContractError: return None
        with ThreadPoolExecutor(max_workers=2) as pool: values=list(pool.map(save,range(2)))
        self.assertEqual(sum(v is not None for v in values),1)
        self.assertEqual(len(self.reviews.history(self.owner,self.case,item.finding_id)),1)
        request=self.request('lost-ack',1,'rejected'); self.client.lost_ack=True
        with self.assertRaises(OSError): self.reviews.save(self.owner,self.case,item.finding_id,request)
        saved=self.reviews.save(self.owner,self.case,item.finding_id,request)
        self.assertEqual(saved.revision,2)
        self.assertEqual(len(self.reviews.history(self.owner,self.case,item.finding_id)),2)

    def test_cr09_report_cutoff_keeps_earlier_final_and_pending_item(self):
        first=self.present(); self.present(self.item('finding-2','O2'))
        event=self.reviews.save(self.owner,self.case,first.finding_id,self.request(item=first))
        cutoff=event.committed_at
        self.reviews.save(self.owner,self.case,first.finding_id,self.request('second',1,'rejected'))
        cohort=ReviewCohort(start='2026-01-01T00:00:00Z',end='2027-01-01T00:00:00Z',cutoff=cutoff,
            display_timezone='Asia/Kolkata',model_id=self.snapshot.model_version,prompt_version=PERIOD_PROMPT,data_mode='synthetic_live')
        result=self.reviews.report(self.owner,self.case,cohort)
        self.assertEqual((result.approved,result.rejected,result.pending),(1,0,1))
        self.assertEqual(result.review_coverage,0.5)

    def pipeline(self, responses=None, *, fail_audit=False):
        fixture=pipeline_tests.PipelineTests('runTest'); fixture.setUp(); self.addCleanup(fixture.doCleanups)
        snapshot=fixture.snapshot.model_copy(update={'case_id':self.case,'bank_profile':{'name':'Fictional cloud bank'},
            'prompt_version':'assessment-vs5-selected-v1',
            'selected_document_ids':{s['document']['source_id']:s['document']['document_version_id'] for s in fixture.sources}})
        # Native runtime has no database path or SQL transaction API. SQLite only prepares existing fixtures.
        fixture.snapshot=snapshot
        for source in fixture.sources:
            source['document']['case_id']=self.case
            if source['document']['kind']=='regulation':
                source['original_ref']=self.objects.save_extraction(self.owner,self.case,'historical-original',b'fictional rules')
            self.store.put(self.owner,self.case,'document',source['document']['document_version_id'],source)
        self.store.save_snapshot(self.owner,snapshot)
        run=self.reviews.admit(self.owner,self.case,'pipeline-run',snapshot.snapshot_id,'synthetic_live')
        sources={s['document']['document_version_id']:s for s in fixture.sources}
        class Documents:
            def read(inner,owner,case,identity,**kwargs):
                self.cases.read(owner,case); return copy.deepcopy(sources[identity])
        self.service.documents=Documents()
        if fail_audit:
            original=self.reviews.attempt
            def save_attempt(owner,case,event,**kwargs):
                if event.operation=='model' and kwargs.get('finish'):
                    raise OSError('Controlled audit storage failure')
                return original(owner,case,event,**kwargs)
            self.reviews.attempt=save_attempt
        prepared=responses(fixture) if responses else [fixture.extraction(),fixture.controls(),fixture.proposed(),fixture.proposed('O-2')]
        for index,raw in enumerate(prepared):
            if raw=='malformed': continue
            action=json.loads(raw); action['document_version_ids']=list(snapshot.selected_document_ids.values()); prepared[index]=json.dumps(action)
        class NativeControlledModel:
            def __init__(inner): inner.calls=0
            def dispatch(inner,store,owner,case,job,token,request):
                store.reserve(owner,case,job,token,'model'); raw=prepared[inner.calls]; inner.calls+=1
                return ModelReply(label='Live',model_id=snapshot.model_version,action=validated_action(raw,store,owner,case,job))
        from regulatory_agent.assessment_pipeline import AssessmentPipeline
        model=NativeControlledModel(); result=AssessmentPipeline(self.service,model).run(self.owner,self.case,run['job_id'])
        return result,model,run

    def test_cr10_shared_pipeline_completes_with_native_records_without_sqlite(self):
        result,model,run=self.pipeline()
        self.assertEqual(result['state'],'completed'); self.assertEqual(model.calls,4)
        report=self.service.read(self.owner,self.case,run['job_id'])
        self.assertEqual(len(report['findings']),2); self.assertEqual(report['live_model_calls'],4)
        self.assertEqual(report['summary']['pending'],2); self.assertEqual(report['reviews'],[])
        self.assertFalse(hasattr(self.store,'path')); self.assertFalse(hasattr(self.store,'transaction'))
        self.assertTrue(any(op=='transaction' for op,_ in self.client.calls))

    def test_cr11_partial_pipeline_exports_verified_sources_and_unchecked_scope(self):
        result,model,run=self.pipeline(lambda f:[f.extraction(),f.controls(),f.proposed(),'malformed'])
        self.assertEqual(result['state'],'partial'); self.assertEqual(result['unchecked_obligations'],['O-2'])
        raw=self.service.export(self.owner,self.case,run['job_id'],'json')
        report=json.loads(raw); self.assertEqual(report['state'],'partial')
        self.assertEqual(len(report['findings']),1); self.assertEqual(report['unchecked_obligations'],['O-2'])
        self.assertEqual(len(report['sources']),3); self.assertNotIn('token',report['job'])
        self.assertEqual(report['reviews'],[])

    def test_cr12_body_identity_and_changed_attempt_identity_are_denied(self):
        with self.assertRaises(ContractError):
            self.store.put(self.owner,self.case,'snapshot','different',self.snapshot.model_dump(mode='json'))
        with self.assertRaises(ContractError):
            self.store.put(self.owner,self.case,'document','different',{'document':{'case_id':'other','document_version_id':'different'}})
        event=self.event(); self.reviews.attempt(self.owner,self.case,event,execution_token=self.token)
        changed=event.model_copy(update={'state':'succeeded','finished_at':datetime.now(timezone.utc),'duration_seconds':0.01,'attempt_id':'other'})
        with self.assertRaisesRegex(ContractError,'attempt_scope_denied'):
            self.reviews.attempt(self.owner,self.case,changed,execution_token=self.token,finish=True)

    def test_cr13_missing_dispatch_audit_cannot_report_zero_live_calls(self):
        result,model,run=self.pipeline(fail_audit=True)
        self.assertEqual(result['state'],'failed'); self.assertEqual(model.calls,1)
        report=self.service.read(self.owner,self.case,run['job_id'])
        self.assertEqual(report['job']['model_calls'],1)
        self.assertIsNone(report['live_model_calls'])
        self.assertEqual(next(t for t in report['trace']['attempts'] if t['operation']=='model')['state'],'unknown')

    def test_cr14_local_attempt_finish_cannot_change_audit_identity(self):
        fixture=pipeline_tests.PipelineTests('runTest'); fixture.setUp(); self.addCleanup(fixture.doCleanups)
        token=fixture.store.claim(fixture.owner,fixture.case,fixture.job_id)
        event=self.event().model_copy(update={'run_id':fixture.run['run_id'],'job_id':fixture.job_id,'snapshot_id':fixture.snapshot.snapshot_id})
        fixture.reviews.attempt(fixture.owner,fixture.case,event,execution_token=token)
        changed=event.model_copy(update={'state':'succeeded','finished_at':datetime.now(timezone.utc),'duration_seconds':0.01,'attempt_id':'other'})
        with self.assertRaisesRegex(ContractError,'attempt_scope_denied'):
            fixture.reviews.attempt(fixture.owner,fixture.case,changed,execution_token=token,finish=True)

    def test_cr15_edited_revision_and_evidence_request_keep_original_review_rules(self):
        item=self.present(); edited=item.original_content().model_copy(update={'recommendation':'Supply dated records.'})
        request=ReviewRequest(event_kind='final_review',disposition='edited',expected_revision=0,idempotency_key='edit-1',
            accepted_content=edited,reason='The original request needs dates.')
        first=self.reviews.save(self.owner,self.case,item.finding_id,request)
        self.assertEqual(first.disposition,'edited')
        evidence=ReviewRequest(event_kind='evidence_request',expected_revision=1,idempotency_key='evidence-1',reason='More records are necessary.')
        self.reviews.save(self.owner,self.case,item.finding_id,evidence)
        with self.assertRaisesRegex(ContractError,'approval_requires_original'):
            self.reviews.save(self.owner,self.case,item.finding_id,self.request('bad-approval',2,item=item).model_copy(update={'accepted_content':edited}))
        final=self.reviews.save(self.owner,self.case,item.finding_id,self.request('original-approval',2,item=item))
        self.assertEqual(final.disposition,'approved'); self.assertEqual(final.revision,3)
        self.assertEqual(self.reviews.history(self.owner,self.case,item.finding_id)[0],first)

    def test_cr16_native_service_review_and_export_keep_processing_configuration(self):
        result,model,run=self.pipeline()
        self.assertEqual(result['state'],'completed')
        report=self.service.read(self.owner,self.case,run['job_id'])
        item=ReviewItem.model_validate(report['findings'][0])
        event=self.service.review(self.owner,self.case,run['job_id'],item.finding_id,self.request(item=item))
        exported=json.loads(self.service.export(self.owner,self.case,run['job_id'],'json'))
        self.assertEqual(exported['summary']['reviewed'],1)
        self.assertEqual(exported['reviews'][0]['event_id'],event.event_id)
        trace=next(t for t in exported['trace']['attempts'] if t['stage']=='review_event')
        self.assertEqual(trace['versions']['model_configuration'],'india-converse-v1')
        self.assertEqual(trace['artifact_ids'],[event.event_id])


if __name__=='__main__': unittest.main()
