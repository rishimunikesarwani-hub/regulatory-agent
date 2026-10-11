"""Full selected-scope software checks. No live calls or held-out evaluation labels."""
import copy
import hashlib
import json
import time
import unittest
import uuid
from unittest.mock import patch

import test_slice03_assessment as assessment_flow
from regulatory_agent.assessments import Assessments
from regulatory_agent.bedrock_model import ModelFailure
from regulatory_agent.cases import CaseService, SQLiteCases
from regulatory_agent.contracts import ContractError, Snapshot
from regulatory_agent.documents import Documents
from regulatory_agent.local import ControlledModel, Store
from regulatory_agent.reviews import Reviews
from regulatory_agent.telemetry import TokenUsage


class PipelineTests(unittest.TestCase):
    def setUp(self):
        from regulatory_agent.assessment_pipeline import AssessmentPipeline
        self.Pipeline = AssessmentPipeline
        self.flow = assessment_flow.AssessmentSliceTests('runTest'); self.flow.setUp()
        self.addCleanup(self.flow.tearDown)
        self.owner, self.case = 'operator-a', self.flow.case
        self.store = Store(self.flow.path)
        self.service = Assessments(CaseService(SQLiteCases(self.store)), Documents(CaseService(SQLiteCases(self.store))))
        self.reviews = Reviews(self.store)
        self.policy = self.flow.policy
        response = self.flow.call('POST',self.flow.sources,
            content=b'Fictional records only.\n2024-04-01 to 2024-04-07: Privileged sessions were recorded and reviewed.\n',
            headers={'X-Filename':'session-records.txt','X-Document-Kind':'evidence','X-Synthetic':'true'})
        self.assertEqual(response.status_code,201,response.text)
        self.evidence=response.json()
        self.evidence['evidence_period']={'start':'2024-04-01','end':'2024-04-07'}
        self.regulation={'document':{'document_version_id':'rules:v1','case_id':self.case,'source_id':'rules','version':'v1',
            'kind':'regulation','sha256':hashlib.sha256(b'fictional rules').hexdigest(),'storage_reference':'fictional-rules',
            'synthetic':True},'passages':[
                {'document_version_id':'rules:v1','passage_id':'rule-1','location':'Clause 1','text':'Record privileged sessions for privileged access.'},
                {'document_version_id':'rules:v1','passage_id':'rule-2','location':'Clause 2','text':'Review activity logs for privileged access.'}],
            'obligation_scopes':{'O-1':['rule-1'],'O-2':['rule-2']}}
        self.sources=[self.regulation,self.policy,self.evidence]
        self.versions={s['document']['source_id']:s['document']['version'] for s in self.sources}
        for source in self.sources:
            doc=source['document']; self.store.put(self.owner,self.case,'document',f"{doc['source_id']}:{doc['version']}",source)
        self.snapshot=Snapshot(snapshot_id='pipeline-snapshot',case_id=self.case,bank_profile={'name':'Fictional pipeline bank'},
            selected_versions=self.versions,selected_obligations=['O-1','O-2'],assessment_date='2024-04-08',mode='historical',
            prompt_version='assessment-vs5-v1',model_version='in.openai.gpt-5.6-luna',synthetic=True)
        self.store.save_snapshot(self.owner,self.snapshot)
        self.new_run()

    def new_run(self):
        self.run=self.reviews.admit(self.owner,self.case,uuid.uuid4().hex,self.snapshot.snapshot_id,'controlled_simulation')
        self.job_id=self.run['job_id']

    @staticmethod
    def cite(passage):
        return {key:passage[key] for key in ('document_version_id','passage_id','location')}|{'quote':passage['text']}

    def action(self,kind,**values):
        return json.dumps({'action':kind,'snapshot_id':self.snapshot.snapshot_id,
            'document_version_ids':[f'{name}:{version}' for name,version in self.versions.items()]}|values)

    def extraction(self):
        return self.action('retrieve_obligations',obligations=[{
            'obligation_id':identity,'requirement':passage['text'],'conditions':['Privileged access'],
            'exceptions':['Fictional excluded entity'],'applicability':'Applies to this fictional entity.',
            'citations':[self.cite(passage)]} for identity,passage in zip(('O-1','O-2'),self.regulation['passages'])])

    def controls(self):
        return self.action('find_controls',controls=[{'control_id':'C-1','statement':'Record and review sessions.',
            'purpose':None,'owner':None,'frequency':None,'citations':[self.cite(self.policy['passages'][0])]}])

    def finding(self,identity='O-1'):
        regulation=self.regulation['passages'][0 if identity=='O-1' else 1]
        cites=[self.cite(regulation),self.cite(self.policy['passages'][0])]
        if identity=='O-1':cites.append(self.cite(self.evidence['passages'][1]))
        return {'finding_id':'model-finding','snapshot_id':self.snapshot.snapshot_id,'obligation_id':identity,
            'control_ids':['C-1'],'status':'supported' if identity=='O-1' else 'needs_review',
            'evidence_condition':'sufficient' if identity=='O-1' else 'missing','citations':cites,
            'rationale':'Fictional software check. Examine the cited records.',
            'remedy':'Maintain session records.' if identity=='O-1' else 'Request dated activity reviews.',
            'gap_kind':None if identity=='O-1' else 'evidence',
            'claims':[{'obligation_element':regulation['text'],'citations':cites,'reason':'Fictional assessment reason.',
                'operational':True,'evidence_period':self.evidence['evidence_period'] if identity=='O-1' else None,
                'examined_exceptions':[],'conflicting_evidence':[]}]}

    def proposed(self,identity='O-1',finding=None):
        return self.action('propose_findings',findings=[finding or self.finding(identity)])

    def execute(self,responses=None,model=None):
        model=model or ControlledModel(responses or [self.extraction(),self.controls(),self.proposed(),self.proposed('O-2')])
        pipeline=self.Pipeline(self.service,model)
        result=pipeline.run(self.owner,self.case,self.job_id)
        return result,pipeline,model

    def findings(self):
        return self.service.read(self.owner,self.case,self.job_id)['findings']

    def test_pt01_all_selected_obligations_preserve_claims_sources_and_unknown_fields(self):
        result,_,model=self.execute()
        self.assertEqual(result['state'],'completed');self.assertEqual(result['unchecked_obligations'],[])
        findings=self.findings()
        self.assertEqual({f['obligation_id'] for f in findings},{'O-1','O-2'})
        self.assertEqual(len({f['finding_id'] for f in findings}),2)
        self.assertEqual({f['status'] for f in findings},{'supported','needs_review'})
        self.assertTrue(all(f['claims'] and f['primary_recommendation'] for f in findings))
        self.assertTrue(all(f['data_mode']=='controlled_simulation' for f in findings))
        self.assertEqual(model.dispatches,4)
        extraction=result['stages']['obligations']['obligations'][0]
        self.assertEqual(extraction['conditions'],['Privileged access'])
        self.assertEqual(extraction['exceptions'],['Fictional excluded entity'])
        self.assertIsNone(result['stages']['controls']['controls'][0]['owner'])
        traces=self.service.read(self.owner,self.case,self.job_id)['trace']['attempts']
        self.assertEqual(len([t for t in traces if t['operation']=='model']),4)
        self.assertTrue(all(t['state']=='succeeded' for t in traces))

    def test_pt02_ranking_filters_versions_kinds_and_known_periods_before_selection(self):
        from regulatory_agent.assessment_pipeline import ranked_context
        sources=copy.deepcopy(self.sources)
        future=copy.deepcopy(self.evidence);future['document']['source_id']='future';future['document']['version']='2'
        future['document']['document_version_id']='future-version'
        future['evidence_period']={'start':'2025-01-01','end':'2025-01-02'}
        for p in future['passages']:p['document_version_id']='future-version';p['passage_id']='future-'+p['passage_id']
        wrong=copy.deepcopy(future);wrong['document']['version']='3';wrong['evidence_period']=None
        context=ranked_context(sources+[future,wrong],self.versions|{'future':'2'},query='privileged sessions',
            kinds={'evidence'},period={'start':'2024-04-01','end':'2024-04-07'},assessment_date='2024-04-08')
        self.assertEqual(set(context['candidate_passage_ids']),{p['passage_id'] for p in self.evidence['passages']})
        self.assertNotIn('future-version',json.dumps(context))
        self.assertLessEqual(context['selected_bytes'],64_000)
        sources[2].pop('evidence_period')
        unknown=ranked_context(sources,self.versions,query='sessions',kinds={'evidence'},
            period={'start':'2024-04-01','end':'2024-04-07'},assessment_date='2024-04-08')
        self.assertEqual(unknown['unknown_period_version_ids'],[self.evidence['document']['document_version_id']])

    def test_pt03_owner_scope_and_original_integrity_prevent_inference(self):
        model=ControlledModel([]);pipeline=self.Pipeline(self.service,model)
        with self.assertRaises(Exception):pipeline.run('other-owner',self.case,self.job_id)
        self.assertEqual(model.dispatches,0)
        with self.store.transaction() as db:
            db.execute("UPDATE documents SET original=? WHERE id=?",(b'altered original',self.policy['document']['document_version_id']))
        result,_,model=self.execute(model=model)
        self.assertEqual(result['state'],'failed');self.assertEqual(model.dispatches,0)
        self.new_run()
        with self.store.transaction() as db:
            db.execute("UPDATE documents SET original=? WHERE id=?",(assessment_flow.POLICY,self.policy['document']['document_version_id']))
            record=copy.deepcopy(self.regulation);record['obligation_scopes']['O-1']=['not-a-passage']
            db.execute("UPDATE records SET body=? WHERE case_id=? AND kind='document' AND id='rules:v1'",(json.dumps(record),self.case))
        result,_,model=self.execute(model=ControlledModel([]))
        self.assertEqual(result['state'],'failed');self.assertEqual(model.dispatches,0)

    def test_pt04_invalid_support_quotes_and_unexamined_passages_never_present(self):
        for problem in ('policy_only','unknown_period','wrong_quote','unexamined'):
            with self.subTest(problem=problem):
                self.new_run();finding=self.finding();claim=finding['claims'][0]
                if problem=='policy_only':
                    finding['citations']=finding['citations'][:2];claim['citations']=claim['citations'][:2]
                elif problem=='unknown_period':claim['evidence_period']=None
                elif problem=='wrong_quote':finding['citations'][0]['quote']='Invented quotation'
                else:
                    citation=self.cite(self.regulation['passages'][1]);finding['citations'].append(citation);claim['citations'].append(citation)
                result,_,_=self.execute([self.extraction(),self.controls(),self.proposed(finding=finding)])
                self.assertEqual(result['state'],'failed');self.assertEqual(self.findings(),[])
                self.assertEqual(set(result['unchecked_obligations']),{'O-1','O-2'})

    def test_pt05_refinement_and_inspection_are_bounded_actions(self):
        refine=self.action('refine_retrieval',retrieval_query='privileged sessions')
        inspect=self.action('inspect_evidence',passage_ids=[self.evidence['passages'][1]['passage_id']])
        result,_,model=self.execute([self.extraction(),self.controls(),refine,inspect,self.proposed(),self.proposed('O-2')])
        self.assertEqual(result['state'],'completed');self.assertEqual(model.dispatches,6)
        for invalid in (refine,self.extraction(),self.action('inspect_evidence',passage_ids=['outside-candidate'])):
            self.new_run()
            result,_,_=self.execute([self.extraction(),self.controls(),refine,invalid])
            self.assertEqual(result['state'],'failed');self.assertEqual(self.findings(),[])

    def test_pt06_later_failure_keeps_usable_findings_and_unchecked_scope(self):
        result,_,model=self.execute([self.extraction(),self.controls(),self.proposed(),'not JSON'])
        self.assertEqual(result['state'],'partial');self.assertEqual(result['unchecked_obligations'],['O-2'])
        self.assertEqual(len(self.findings()),1);self.assertEqual(model.dispatches,4)
        self.new_run()
        with self.store.transaction() as db:
            job=self.store._job(db,self.owner,self.case,self.job_id);job['model_calls']=24;self.store._save_job(db,job)
        result,_,model=self.execute()
        self.assertEqual(result['state'],'failed');self.assertEqual(model.dispatches,0)

    def test_pt07_resume_reuses_validated_output_without_duplicate_inference(self):
        model=ControlledModel([self.extraction(),self.controls(),self.proposed(),self.proposed('O-2')])
        pipeline=self.Pipeline(self.service,model)
        with patch.object(pipeline.reviews,'present',side_effect=KeyboardInterrupt):
            with self.assertRaises(KeyboardInterrupt):pipeline.run(self.owner,self.case,self.job_id)
        self.assertEqual(model.dispatches,3)
        with self.store.transaction() as db:
            job=self.store._job(db,self.owner,self.case,self.job_id);job['lease_until']=0;self.store._save_job(db,job)
        result=pipeline.run(self.owner,self.case,self.job_id)
        self.assertEqual(result['state'],'completed');self.assertEqual(model.dispatches,4)
        self.assertEqual(len(self.findings()),2)
        pipeline.run(self.owner,self.case,self.job_id)
        self.assertEqual(model.dispatches,4)

    def test_pt08_failed_dispatch_retains_usage_without_private_error_text(self):
        class FailingModel(ControlledModel):
            def dispatch(model,*args,**kwargs):
                super(FailingModel,model).dispatch(*args,**kwargs)
                raise ModelFailure('model_response_incomplete',usage=TokenUsage(input_tokens=100,output_tokens=50),provider_request_id='safe-provider-id')
        result,_,_=self.execute(model=FailingModel([self.extraction()]))
        self.assertEqual(result['state'],'failed');self.assertEqual(result['model_calls'],1)
        traces=self.service.read(self.owner,self.case,self.job_id)['trace']['attempts']
        failed=next(t for t in traces if t['operation']=='model')
        self.assertEqual(failed['state'],'failed');self.assertTrue(failed['dispatched'])
        self.assertEqual(failed['usage']['output_tokens'],50);self.assertEqual(failed['provider_request_id'],'safe-provider-id')
        self.assertNotIn('raw_response',json.dumps(traces));self.assertNotIn('requirement',json.dumps(traces))
        self.assertTrue(all(t['state'] in {'succeeded','failed'} for t in traces))

    def test_pt10_twenty_candidates_share_the_context_budget_with_regulatory_scope(self):
        content=b'Fictional records only.\n2024-04-01 to 2024-04-07: Privileged sessions were recorded and reviewed.\n'
        content += b'\n'.join(f'Unrelated fictional record {i}.'.encode() for i in range(25))
        response=self.flow.call('POST',self.flow.sources,content=content,
            headers={'X-Filename':'larger-records.txt','X-Document-Kind':'evidence','X-Synthetic':'true'})
        self.assertEqual(response.status_code,201,response.text)
        self.evidence=response.json();self.evidence['evidence_period']={'start':'2024-04-01','end':'2024-04-07'}
        self.sources[2]=self.evidence
        self.versions={s['document']['source_id']:s['document']['version'] for s in self.sources}
        doc=self.evidence['document'];self.store.put(self.owner,self.case,'document',f"{doc['source_id']}:{doc['version']}",self.evidence)
        self.snapshot=Snapshot.model_validate(self.snapshot.model_dump()|{'snapshot_id':'larger-snapshot','selected_versions':self.versions})
        self.store.save_snapshot(self.owner,self.snapshot);self.new_run()
        result,_,_=self.execute()
        self.assertEqual(result['state'],'completed')
        attempts=self.service.read(self.owner,self.case,self.job_id)['trace']['attempts']
        self.assertTrue(all(len(t['selected_passage_ids'])<=20 for t in attempts))

    def test_pt11_all_statuses_and_repeated_assessments_keep_independent_items(self):
        ids=[]
        for status, condition, gap in (('supported','sufficient',None),('partial','partial','evidence'),
                ('gap','sufficient','control'),('needs_review','missing','evidence'),('not_applicable','missing',None)):
            self.new_run();finding=self.finding()
            finding.update(status=status,evidence_condition=condition,gap_kind=gap)
            if status=='not_applicable':finding['applicability_reason']='The cited fictional scope exception applies.'
            result,_,_=self.execute([self.extraction(),self.controls(),self.proposed(finding=finding),self.proposed('O-2')])
            self.assertEqual(result['state'],'completed')
            item=next(f for f in self.findings() if f['obligation_id']=='O-1')
            self.assertEqual(item['status'],status);ids.append(item['finding_id'])
        self.assertEqual(len(set(ids)),5)

    def test_pt12_presentation_checks_execution_claim_inside_its_transaction(self):
        pipeline=self.Pipeline(self.service,ControlledModel([self.extraction(),self.controls(),self.proposed()]))
        original=pipeline.reviews.present
        def late(*args,**kwargs):
            with self.store.transaction() as db:
                job=self.store._job(db,self.owner,self.case,self.job_id);job['deadline']=time.time()-1;self.store._save_job(db,job)
            return original(*args,**kwargs)
        with patch.object(pipeline.reviews,'present',side_effect=late):result=pipeline.run(self.owner,self.case,self.job_id)
        self.assertEqual(result['state'],'failed');self.assertEqual(self.findings(),[])

    def test_pt13_live_metadata_exports_do_not_claim_simulated_processing(self):
        class LiveResponseStub(ControlledModel):
            def dispatch(model,*args,**kwargs):
                reply=super(LiveResponseStub,model).dispatch(*args,**kwargs)
                return reply.model_copy(update={'label':'Live','usage':TokenUsage(input_tokens=100,output_tokens=50)})
        self.run=self.reviews.admit(self.owner,self.case,uuid.uuid4().hex,self.snapshot.snapshot_id,'synthetic_live');self.job_id=self.run['job_id']
        result,_,_=self.execute(model=LiveResponseStub([self.extraction(),self.controls(),self.proposed(),self.proposed('O-2')]))
        self.assertEqual(result['state'],'completed')
        report=json.loads(self.service.export(self.owner,self.case,self.job_id,'json'))
        self.assertEqual(report['data_mode'],'synthetic_live');self.assertEqual(report['live_model_calls'],4)
        self.assertNotIn('Simulated processing',report['label'])
        self.assertNotIn('No live model call occurred.',json.dumps(report['limitations']))
        attempts=report['trace']['attempts']
        self.assertTrue({'extraction','context_selection'} <= {t['stage'] for t in attempts})

    def test_pt14_export_validates_claim_exception_and_conflict_citations(self):
        self.execute();item=self.findings()[0]
        item['claims'][0]['examined_exceptions']=[self.cite(self.regulation['passages'][0])|{'quote':'Forged exception quote'}]
        with self.store.transaction() as db:
            db.execute("UPDATE records SET body=? WHERE case_id=? AND kind='finding' AND id=?",(json.dumps(item),self.case,item['finding_id']))
        with self.assertRaises(Exception):self.service.export(self.owner,self.case,self.job_id,'json')

    def test_pt15_public_regulatory_input_is_distinct_from_private_bank_input(self):
        public=copy.deepcopy(self.regulation)
        public['document'].update(synthetic=False,source_url='https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=12562&Mode=0')
        with self.store.transaction() as db:
            db.execute("UPDATE records SET body=? WHERE case_id=? AND kind='document' AND id='rules:v1'",(json.dumps(public),self.case))
        result,_,_=self.execute()
        self.assertEqual(result['state'],'completed')
        for invalid in ('private_bank','unverified_public_url'):
            self.new_run()
            with self.store.transaction() as db:
                if invalid=='private_bank':
                    document=copy.deepcopy(self.policy);document['document']['synthetic']=False
                    doc=document['document'];key=f"{doc['source_id']}:{doc['version']}"
                else:
                    policy=self.policy['document']
                    db.execute("UPDATE records SET body=? WHERE case_id=? AND kind='document' AND id=?",
                        (json.dumps(self.policy),self.case,f"{policy['source_id']}:{policy['version']}"))
                    document=copy.deepcopy(public);document['document']['source_url']='https://example.invalid/rules';key='rules:v1'
                db.execute("UPDATE records SET body=? WHERE case_id=? AND kind='document' AND id=?",(json.dumps(document),self.case,key))
            result,_,model=self.execute()
            self.assertEqual(result['state'],'failed');self.assertEqual(model.dispatches,0)

    def test_pt09_audit_failure_late_response_and_stale_claim_cannot_complete(self):
        model=ControlledModel([self.extraction()]);pipeline=self.Pipeline(self.service,model)
        with patch.object(pipeline,'_finish_attempt',side_effect=OSError('private failure text')):
            result=pipeline.run(self.owner,self.case,self.job_id)
        self.assertEqual(result['state'],'failed')
        self.new_run()
        original=model.dispatch
        def late(*args,**kwargs):
            reply=original(*args,**kwargs)
            with self.store.transaction() as db:
                job=self.store._job(db,self.owner,self.case,self.job_id);job['deadline']=time.time()-1;self.store._save_job(db,job)
            return reply
        with patch.object(model,'dispatch',side_effect=late):result=pipeline.run(self.owner,self.case,self.job_id)
        self.assertEqual(result['state'],'failed');self.assertEqual(self.findings(),[])
        self.new_run();model=ControlledModel([self.extraction()]);pipeline=self.Pipeline(self.service,model)
        original=model.dispatch
        def stale(*args,**kwargs):
            reply=original(*args,**kwargs)
            with self.store.transaction() as db:
                job=self.store._job(db,self.owner,self.case,self.job_id);job['token']='new-worker-token';self.store._save_job(db,job)
            return reply
        with patch.object(model,'dispatch',side_effect=stale):
            with self.assertRaisesRegex(ContractError,'stale_execution_claim'):pipeline.run(self.owner,self.case,self.job_id)
        self.assertEqual(self.store.read_job(self.owner,self.case,self.job_id)['state'],'running')
        self.assertEqual(self.findings(),[])


if __name__=='__main__':unittest.main()
