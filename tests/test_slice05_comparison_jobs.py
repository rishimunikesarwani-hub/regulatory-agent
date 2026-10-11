"""Saved comparison execution with native records and controlled responses only."""
import copy
from datetime import datetime, timezone
import hashlib
import json
import time
import unittest
from unittest.mock import patch

import test_slice05_cloud_execution as execution
from regulatory_agent.contracts import ComparisonRequest, ContractError, ReviewItem
from regulatory_agent.local import validated_action
from regulatory_agent.comparison_jobs import Comparisons


class Replies:
    def __init__(self, replies): self.replies=iter(replies); self.requests=[]
    def dispatch(self, store, owner, case, job, token, request):
        from regulatory_agent.regulatory_changes import ComparisonReply
        from regulatory_agent.telemetry import TokenUsage
        store.reserve(owner,case,job,token,'model'); self.requests.append(json.loads(request['prompt']))
        action=validated_action(json.dumps(next(self.replies)),store,owner,case,job)
        return ComparisonReply(label='Live',action=action,usage=TokenUsage(input_tokens=100,output_tokens=40),provider_request_id='comparison-provider')


class ComparisonJobTests(unittest.TestCase):
    def setUp(self):
        self.f=execution.CloudAdmissionTests('runTest'); self.f.setUp(); self.addCleanup(self.f.doCleanups)
        self.service,self.store,self.owner,self.case=self.f.service,self.f.store,self.f.owner,self.f.case
        self.baseline=self.f.admit(); self.snapshot=self.store.get(self.owner,self.case,'snapshot',self.baseline['snapshot_id'])
        self.old=self.store.get(self.owner,self.case,'document',self.f.regulation['document']['document_version_id'])
        self.obligation=self.snapshot['selected_obligations'][0]
        bank=next(s for s in self.service._sources(self.owner,self.case,self.snapshot) if s['document']['kind']=='policy')
        p=bank['passages'][0]
        citation={k:p[k] for k in ('document_version_id','passage_id','location')}|{'quote':p['text']}
        self.control={'control_id':'ACCESS-01','statement':p['text'],'purpose':None,'owner':None,'frequency':'monthly','citations':[citation]}
        token=self.store.claim(self.owner,self.case,self.baseline['job_id'])
        self.store.save_stage(self.owner,self.case,self.baseline['job_id'],token,'controls',{'controls':[self.control]})
        self.item=ReviewItem(finding_id='baseline-finding',run_id=self.baseline['run_id'],snapshot_id=self.snapshot['snapshot_id'],
            obligation_id=self.obligation,control_ids=['ACCESS-01'],status='needs_review',evidence_condition='missing',
            citations=[citation],rationale='Test baseline needs records.',remedy='Supply records.',primary_recommendation='Supply records.',
            gap_kind='evidence',available_at=datetime.now(timezone.utc).isoformat(),model_id=self.snapshot['model_version'],
            prompt_version=self.snapshot['prompt_version'],data_mode='synthetic_live',
            source_version_ids=[f'{name}:{v}' for name,v in self.snapshot['selected_versions'].items()])
        self.service.reviews.present(self.owner,self.case,self.item,execution_token=token)
        self.store.save_stage(self.owner,self.case,self.baseline['job_id'],token,'baseline-result',{'accounted_obligations':[self.obligation]})
        self.store.finalize(self.owner,self.case,self.baseline['job_id'],token,'completed',[])
        # This is controlled test text, not an RBI amendment or a provider source.
        raw=b'Test source only: Require independent approval for access reviews.'
        ref=self.f.objects.save_extraction(self.owner,self.case,'comparison-test-original',raw)
        self.new=copy.deepcopy(self.old)
        self.new['document'].update(document_version_id='new-test-regulation',version='test-new-version',
            sha256=hashlib.sha256(raw).hexdigest(),publication_date='2024-01-01',effective_date='2024-04-01')
        self.new.update(original_ref=ref,passages=[{'document_version_id':'new-test-regulation','passage_id':'new-test-clause',
            'location':'Test clause','text':raw.decode()}],obligation_scopes={self.obligation:['new-test-clause']})
        for k in ('publication_date','effective_date'): self.new[k]=self.new['document'][k]
        self.store.put(self.owner,self.case,'document','new-test-regulation',self.new)
        self.request=ComparisonRequest(snapshot_id=self.snapshot['snapshot_id'],
            older_version_id=self.old['document']['document_version_id'],newer_version_id='new-test-regulation',idempotency_key='compare-test')
        self.comparisons=Comparisons(self.service)

    def admit(self): return self.comparisons.admit(self.owner,self.case,self.request)

    def reply(self, record, kind='changed_requirement'):
        def obligation(source):
            p=source['passages'][0]
            return {'obligation_id':self.obligation,'requirement':p['text'],'conditions':[],'exceptions':[],
                'applicability':None,'citations':[{k:p[k] for k in ('document_version_id','passage_id','location')}|{'quote':p['text']}]}
        old,new=obligation(record['pair']['older_source']),obligation(record['pair']['newer_source'])
        return {'action':'compare_obligations','snapshot_id':record['comparison_id'],
            'document_version_ids':record['document_version_ids'],'comparison':{'snapshot_id':self.snapshot['snapshot_id'],
                'older_version_id':self.request.older_version_id,'newer_version_id':self.request.newer_version_id,
                'changes':[{'obligation_id':self.obligation,'kind':kind,'before':old,'after':new,
                    'reason':'Controlled test interpretation.', 'basis':old['citations']+new['citations'],
                    'affected_control_ids':['ACCESS-01'] if kind=='changed_requirement' else []}]}}

    def process(self, record, reply=None):
        model=Replies([reply or self.reply(record)])
        result=Comparisons(self.service,model).run(self.owner,self.case,record['job_id'])
        return result,model

    def test_cj01_native_admission_pins_pair_without_changing_baseline(self):
        before=copy.deepcopy(self.service.read(self.owner,self.case,self.baseline['job_id']))
        saved=self.admit()
        self.assertNotEqual(saved['job_id'],self.baseline['job_id']); self.assertEqual(saved['baseline_job_id'],self.baseline['job_id'])
        self.assertEqual(saved['pair']['selected_obligations'],[self.obligation]); self.assertEqual(saved['controls'],[self.control])
        self.assertEqual(self.service.read(self.owner,self.case,self.baseline['job_id'])['findings'],before['findings'])
        self.assertEqual(len(self.service.list(self.owner,self.case)['runs']),1)
        self.assertEqual(self.store.read_job(self.owner,self.case,saved['job_id'])['state'],'queued')

    def test_cj02_idempotency_and_conflicting_selection(self):
        first=self.admit(); self.assertEqual(self.admit(),first)
        with self.assertRaisesRegex(ContractError,'idempotency_conflict'):
            self.comparisons.admit(self.owner,self.case,self.request.model_copy(update={'newer_version_id':'other'}))
        self.assertEqual(len(self.store.records(self.owner,self.case,'comparison')),1)

    def test_cj03_scope_and_baseline_guards(self):
        with self.assertRaises(Exception): self.comparisons.admit('another-owner',self.case,self.request)
        original=self.store.read_job
        with patch.object(self.store,'read_job',side_effect=lambda *a:original(*a)|{'state':'running'}):
            with self.assertRaisesRegex(ContractError,'comparison_baseline_unfinished'):self.admit()
        self.assertEqual(self.store.records(self.owner,self.case,'comparison'),[])

    def test_cj04_processing_saves_changes_and_measured_attempts(self):
        record=self.admit(); result,model=self.process(record)
        self.assertEqual(result['state'],'completed'); self.assertEqual(result['model_calls'],1)
        read=self.comparisons.read(self.owner,self.case,record['comparison_id'])
        self.assertTrue(read['result']['assessment_required']); self.assertEqual(read['result']['affected_control_ids'],['ACCESS-01'])
        attempts=[a for a in read['trace'] if a['operation']=='model']
        self.assertEqual(len(attempts),1); self.assertEqual(attempts[0]['usage']['input_tokens'],100)
        self.assertEqual(model.requests[0]['controls'],[self.control]); self.assertEqual(read['unchecked_obligations'],[])
        self.assertNotIn('token',read); self.assertNotIn('token',read.get('job',{}))

    def test_cj05_rejected_reply_consumes_allowance_and_does_not_complete(self):
        record=self.admit(); bad=self.reply(record); bad['comparison']['changes'][0]['affected_control_ids']=['invented']
        result,_=self.process(record,bad)
        self.assertEqual(result['state'],'failed'); self.assertEqual(result['model_calls'],1)
        self.assertEqual(result['unchecked_obligations'],[self.obligation])
        read=self.comparisons.read(self.owner,self.case,record['comparison_id']); self.assertIsNone(read['result'])
        self.assertEqual(next(a for a in read['trace'] if a['operation']=='model')['state'],'failed')

    def test_cj06_recovery_does_not_dispatch_saved_results_again(self):
        record=self.admit(); token=self.store.claim(self.owner,self.case,record['job_id'])
        model=Replies([self.reply(record)])
        # Emulate an interruption after the result commit and before finalization.
        with patch.object(self.store,'finalize',side_effect=OSError('interrupted')):
            with self.assertRaises(OSError): Comparisons(self.service,model).run(self.owner,self.case,record['job_id'],execution_token=token)
        job=self.store.read_job(self.owner,self.case,record['job_id']); original_deadline=job['deadline']
        self.store.renew(self.owner,self.case,record['job_id'],token)
        resumed=Comparisons(self.service,Replies([])).run(self.owner,self.case,record['job_id'],execution_token=token)
        self.assertEqual(resumed['state'],'completed'); self.assertEqual(resumed['model_calls'],1)
        self.assertEqual(resumed['deadline'],original_deadline)

    def test_cj07_new_assessment_keeps_bank_scope_and_independent_history(self):
        record=self.admit(); self.process(record)
        run=self.comparisons.reassess(self.owner,self.case,record['comparison_id'])
        self.assertEqual(self.comparisons.reassess(self.owner,self.case,record['comparison_id']),run)
        snapshot=self.store.get(self.owner,self.case,'snapshot',run['snapshot_id'])
        self.assertEqual(snapshot['selected_obligations'],self.snapshot['selected_obligations'])
        self.assertEqual(snapshot['assessment_date'],self.snapshot['assessment_date'])
        self.assertEqual(snapshot['selected_document_ids'][self.old['document']['source_id']],'new-test-regulation')
        self.assertEqual(snapshot['selected_document_ids'][self.f.version],self.f.version)
        self.assertNotEqual(run['snapshot_id'],self.snapshot['snapshot_id'])
        self.assertEqual(self.service.read(self.owner,self.case,run['job_id'])['findings'],[])

    def test_cj08_unfinished_or_unresolved_changes_do_not_admit_assessment(self):
        record=self.admit()
        with self.assertRaisesRegex(ContractError,'comparison_reassessment_unavailable'):self.comparisons.reassess(self.owner,self.case,record['comparison_id'])
        reply=self.reply(record,'undetermined'); self.process(record,reply)
        with self.assertRaisesRegex(ContractError,'comparison_reassessment_unavailable'):self.comparisons.reassess(self.owner,self.case,record['comparison_id'])

    def test_cj09_saved_snapshot_selects_protocol_and_rejects_other_action(self):
        record=self.admit(); action=self.reply(record)
        self.assertEqual(validated_action(json.dumps(action),self.store,self.owner,self.case,record['job_id']).action,'compare_obligations')
        with self.assertRaises(ContractError):validated_action(json.dumps(action),self.store,self.owner,self.case,self.baseline['job_id'])
        action['snapshot_id']=self.snapshot['snapshot_id']
        with self.assertRaises(ContractError):validated_action(json.dumps(action),self.store,self.owner,self.case,record['job_id'])

    def test_cj10_uncertain_comparison_commit_recovers_same_admission(self):
        original=self.store.commit; failed=[False]
        def uncertain(owner,case,changes,**kwargs):
            result=original(owner,case,changes,**kwargs)
            if changes[0]['kind']['S']=='comparison' and not failed[0]: failed[0]=True; raise OSError('lost acknowledgement')
            return result
        with patch.object(self.store,'commit',side_effect=uncertain):
            with self.assertRaises(OSError):self.admit()
        saved=self.admit(); self.assertEqual(self.admit(),saved)
        self.assertEqual(len(self.store.records(self.owner,self.case,'comparison')),1)
        self.assertEqual(len(self.store.records(self.owner,self.case,'run')),2)

    def test_cj11_missing_control_support_and_original_integrity_fail(self):
        original=self.store.read_job
        def no_controls(*a):return original(*a)|{'stages':{}}
        with patch.object(self.store,'read_job',side_effect=no_controls):
            with self.assertRaisesRegex(ContractError,'comparison_control_support_missing'):self.admit()
        record=self.admit(); self.f.objects.data[(self.owner,self.case,self.new['original_ref']['upload_id'],'v1')]=b'changed original'
        result,_=self.process(record)
        self.assertEqual(result['state'],'failed'); self.assertEqual(result['model_calls'],0)

    def test_cj12_native_bedrock_dispatch_uses_saved_comparison_schema(self):
        import test_slice05_bedrock as bedrock
        from botocore.stub import ANY
        from regulatory_agent.bedrock_model import structured_schema
        from regulatory_agent.regulatory_changes import ComparisonAction, ComparisonReply
        record=self.admit(); token=self.store.claim(self.owner,self.case,record['job_id'])
        adapter=bedrock.BedrockDispatchTests('runTest'); adapter.setUp(); self.addCleanup(adapter.doCleanups)
        adapter.adapter.clock=time.time; adapter.profile()
        adapter.runtime_stub.add_response('converse',adapter.response(self.reply(record)),{
            'modelId':adapter.snapshot.model_version,'system':ANY,'messages':ANY,'inferenceConfig':{'maxTokens':512},
            'outputConfig':{'textFormat':{'type':'json_schema','structure':{'jsonSchema':{
                'name':'assessment_action','schema':structured_schema(ComparisonAction)}}}}})
        reply=adapter.adapter.dispatch(self.store,self.owner,self.case,record['job_id'],token,adapter.request)
        self.assertIsInstance(reply,ComparisonReply); self.assertEqual(reply.action.action,'compare_obligations')
        self.assertEqual(self.store.read_job(self.owner,self.case,record['job_id'])['model_calls'],1)
        adapter.runtime_stub.assert_no_pending_responses(); adapter.management_stub.assert_no_pending_responses()

    def test_cj13_native_worker_routes_comparison_from_saved_snapshot(self):
        from regulatory_agent.aws_execution import bedrock_child
        record=self.admit(); token=self.store.claim(self.owner,self.case,record['job_id'])
        model=Replies([self.reply(record)])
        with patch('regulatory_agent.aws_execution.configured_service',return_value=self.service), \
                patch('regulatory_agent.bedrock_model.BedrockModel.configured',return_value=model):
            bedrock_child(self.owner,self.case,record['job_id'],token)
        self.assertEqual(self.store.read_job(self.owner,self.case,record['job_id'])['state'],'completed')
        self.assertEqual(len(model.requests),1)
