"""Owned comparison HTTP flows with controlled native service state, never AWS traffic."""
import json
import copy
from pathlib import Path
import unittest
from unittest.mock import patch

import yaml
import test_slice05_comparison_jobs as jobs
from test_slice01_aws import event
from regulatory_agent.aws_cases import create_handler


class ComparisonAPITests(unittest.TestCase):
    def setUp(self):
        self.f=jobs.ComparisonJobTests('runTest');self.f.setUp();self.addCleanup(self.f.doCleanups)
        self.service,self.owner,self.case=self.f.service,self.f.owner,self.f.case
        self.root=f'/api/cases/{self.case}/regulatory-comparisons'
        self.queue=self.f.f.queue

    def handler(self, **changes):
        return create_handler(self.f.f.cases,user_pool_id='ap-south-1_pool',user_pool_client_id='client-id',
            assessments=self.service,queue=self.queue,**changes)

    def call(self, method='GET', suffix='', body=None, **changes):
        return self.handler()(event(method,self.root+suffix,body,self.owner)|changes,None)

    def admit(self):
        reply=self.call('POST',body=self.f.request.model_dump())
        self.assertEqual(reply['statusCode'],202,reply['body']);return json.loads(reply['body'])

    def test_cf01_authentication_ownership_and_disabled_flag_precede_factories(self):
        called=[]
        handler=create_handler(self.f.f.cases,user_pool_id='ap-south-1_pool',user_pool_client_id='client-id',
            assessments=lambda:called.append('service'),queue=lambda:called.append('queue'))
        request=event('GET',self.root,owner=self.owner)
        request['requestContext']['authorizer']['jwt']['claims']['token_use']='id'
        self.assertEqual(handler(request,None)['statusCode'],401);self.assertEqual(called,[])
        self.assertEqual(handler(event('GET',self.root,owner='other-owner'),None)['statusCode'],404);self.assertEqual(called,[])
        disabled=create_handler(self.f.f.cases,user_pool_id='ap-south-1_pool',user_pool_client_id='client-id')
        self.assertEqual(disabled(event('GET',self.root,owner=self.owner),None)['statusCode'],503)

    def test_cf02_selection_keeps_baseline_versions_and_safe_owned_metadata(self):
        response=self.call(suffix='/selection',queryStringParameters={'snapshot_id':self.f.snapshot['snapshot_id']})
        self.assertEqual(response['statusCode'],200,response['body']);data=json.loads(response['body'])
        self.assertEqual(data['case_id'],self.case);self.assertEqual(data['snapshot_id'],self.f.snapshot['snapshot_id'])
        self.assertEqual(data['baseline_job_id'],self.f.baseline['job_id']);self.assertEqual(data['freshness'],'unverified')
        self.assertEqual(data['older_versions'][0]['document']['document_version_id'],self.f.request.older_version_id)
        self.assertIn(self.f.request.newer_version_id,[v['document']['document_version_id'] for v in data['newer_versions']])
        for prohibited in ('original_ref','control_passages','owner_id','execution_token'):
            self.assertNotIn(prohibited,response['body'])
        self.assertEqual(self.call(suffix='/selection')['statusCode'],422)

    def test_cf03_uncertain_delivery_preserves_admission_and_safe_public_body(self):
        self.f.f.sqs.lost_ack=True
        first=self.call('POST',body=self.f.request.model_dump());self.assertEqual(first['statusCode'],503)
        self.assertNotIn('Uncertain',first['body'])
        saved=self.admit();again=self.admit();self.assertEqual(saved['job_id'],again['job_id'])
        self.assertEqual(len(self.f.store.records(self.owner,self.case,'comparison')),1)
        for key in ('token','baseline_snapshot','control_passages','original_ref','controls'):
            self.assertNotIn(key,saved)
        messages=[json.loads(sent['MessageBody']) for sent in self.f.f.sqs.sent]
        self.assertEqual({m['job_id'] for m in messages},{saved['job_id']})
        self.assertEqual(set(messages[0]),{'version','owner_id','case_id','job_id'})

    def test_cf04_lists_and_reads_keep_cited_results_and_separate_assessment_lists(self):
        saved=self.admit();record=self.f.store.get(self.owner,self.case,'comparison',saved['comparison_id'])
        self.f.process(record)
        response=self.call(suffix='/'+saved['comparison_id']);self.assertEqual(response['statusCode'],200)
        read=json.loads(response['body']);self.assertEqual(read['state'],'completed')
        self.assertEqual(read['result']['affected_control_ids'],['ACCESS-01']);self.assertEqual(read['unchecked_obligations'],[])
        self.assertEqual(read['result']['changes'][0]['basis'][1]['passage_id'],'new-test-clause')
        listing=json.loads(self.call()['body'])['comparisons'];self.assertEqual(listing[0]['comparison_id'],saved['comparison_id'])
        self.assertNotIn('control_passages',json.dumps(listing));self.assertNotIn('"token":',json.dumps(read))
        self.assertNotIn('"storage_reference":',json.dumps(read))
        self.assertEqual(len(self.service.list(self.owner,self.case)['runs']),1)

    def test_cf05_reviewed_selection_queues_one_independent_assessment(self):
        saved=self.admit();record=self.f.store.get(self.owner,self.case,'comparison',saved['comparison_id']);self.f.process(record)
        path='/'+saved['comparison_id']+'/reassess'
        for body in ({},{'selection_reviewed':False},{'selection_reviewed':1},{'selection_reviewed':True,'snapshot_id':'forged'}):
            with self.subTest(body=body):self.assertEqual(self.call('POST',path,body)['statusCode'],422)
        response=self.call('POST',path,{'selection_reviewed':True});self.assertEqual(response['statusCode'],202,response['body'])
        run=json.loads(response['body']);repeat=json.loads(self.call('POST',path,{'selection_reviewed':True})['body'])
        self.assertEqual(run,repeat);self.assertNotEqual(run['job_id'],self.f.baseline['job_id'])
        self.assertEqual(json.loads(self.f.f.sqs.sent[-1]['MessageBody'])['job_id'],run['job_id'])
        self.assertEqual(self.service.read(self.owner,self.case,run['job_id'])['reviews'],[])
        snapshot=self.f.store.get(self.owner,self.case,'snapshot',run['snapshot_id'])
        self.assertEqual(snapshot['selected_document_ids'][self.f.f.version],self.f.f.version)
        self.assertEqual(snapshot['selected_obligations'],self.f.snapshot['selected_obligations'])

    def test_cf06_resume_uses_saved_identifiers_and_rejects_unknown_records_and_extra_fields(self):
        saved=self.admit();response=self.call('POST','/'+saved['comparison_id']+'/resume',{})
        self.assertEqual(response['statusCode'],202)
        self.assertEqual(json.loads(self.f.f.sqs.sent[-1]['MessageBody'])['job_id'],saved['job_id'])
        self.assertEqual(self.call(suffix='/unknown')['statusCode'],404)
        self.assertEqual(self.call('POST','/'+saved['comparison_id']+'/resume',{'owner_id':self.owner})['statusCode'],422)
        self.assertEqual(self.call('POST',body=self.f.request.model_dump()|{'owner_id':self.owner})['statusCode'],422)
        malformed=event('POST',self.root,owner=self.owner)|{'body':'!bad-base64','isBase64Encoded':True}
        self.assertEqual(self.handler()(malformed,None)['statusCode'],422)

    def test_cf07_unfinished_and_unresolved_comparisons_cannot_reassess(self):
        saved=self.admit();path='/'+saved['comparison_id']+'/reassess'
        self.assertEqual(self.call('POST',path,{'selection_reviewed':True})['statusCode'],409)
        record=self.f.store.get(self.owner,self.case,'comparison',saved['comparison_id'])
        self.f.process(record,self.f.reply(record,'undetermined'))
        self.assertEqual(self.call('POST',path,{'selection_reviewed':True})['statusCode'],409)
        self.assertEqual(len(self.service.list(self.owner,self.case)['runs']),1)

    def test_cf07_future_effective_changes_do_not_queue_an_earlier_assessment(self):
        source=copy.deepcopy(self.f.new)
        source['document'].update(document_version_id='future-test-version',version='future-test',effective_date='2025-01-01')
        source['effective_date']='2025-01-01'
        for passage in source['passages']:passage['document_version_id']='future-test-version'
        self.f.store.put(self.owner,self.case,'document','future-test-version',source)
        self.f.request=self.f.request.model_copy(update={'newer_version_id':'future-test-version','idempotency_key':'future-test'})
        saved=self.admit();record=self.f.store.get(self.owner,self.case,'comparison',saved['comparison_id']);self.f.process(record)
        response=self.call('POST','/'+saved['comparison_id']+'/reassess',{'selection_reviewed':True})
        self.assertEqual(response['statusCode'],409)
        self.assertEqual(len(self.service.list(self.owner,self.case)['runs']),1)
        self.assertEqual(len(self.f.f.sqs.sent),1)

    def test_cf08_local_histories_keep_native_and_simulated_comparisons_separate(self):
        import tempfile
        from types import SimpleNamespace
        from regulatory_agent.local import Store
        from regulatory_agent.assessments import Assessments
        with tempfile.TemporaryDirectory() as folder:
            store=Store(Path(folder)/'case.sqlite');store.create_case(self.owner,self.case,{'name':'Fictional test bank'})
            for identity,mode in [('native','synthetic_live'),('simulated','controlled_simulation')]:
                store.put(self.owner,self.case,'comparison',identity,{'comparison_id':identity,'case_id':self.case,'data_mode':mode})
            service=Assessments(self.f.f.cases,SimpleNamespace(store=store))
            self.assertEqual([c['comparison_id'] for c in service.comparisons(self.owner,self.case)['comparisons']],['simulated'])

    def test_cf08_local_routes_share_rules_and_register_background_execution(self):
        from fastapi.testclient import TestClient
        from regulatory_agent.api import create_app
        from regulatory_agent.comparison_jobs import Comparisons
        with patch('regulatory_agent.api.Documents',return_value=self.f.f.documents), \
                patch('regulatory_agent.api.Assessments',return_value=self.service),patch.object(Comparisons,'run_local') as run:
            app=create_app(service=self.f.f.cases,environment='local',development_user=self.owner)
            client=TestClient(app,client=('127.0.0.1',123))
            response=client.post(self.root,json=self.f.request.model_dump())
            self.assertEqual(response.status_code,202,response.text);saved=response.json()
            run.assert_called_once_with(self.owner,self.case,saved['job_id'])
            self.assertEqual(client.get(self.root+'/'+saved['comparison_id']).status_code,200)
            self.assertEqual(client.get(self.root+'/selection',params={'snapshot_id':self.f.snapshot['snapshot_id']}).status_code,200)
            self.assertEqual(client.post(self.root+'/'+saved['comparison_id']+'/reassess',json={}).status_code,422)

    def test_cf09_sam_routes_share_the_existing_authenticated_case_function(self):
        template=yaml.safe_load((Path(__file__).resolve().parents[1]/'ops/sam-dev.yaml').read_text(encoding='utf-8'))
        properties=template['Resources']['CaseFunction']['Properties'];events=properties['Events']
        routes={(v['Properties']['Method'],v['Properties']['Path']) for v in events.values()}
        for method,suffix in [('GET',''),('POST',''),('GET','/selection'),('GET','/{comparison_id}'),
                ('POST','/{comparison_id}/resume'),('POST','/{comparison_id}/reassess')]:
            self.assertIn((method,'/api/cases/{case_id}/regulatory-comparisons'+suffix),routes)
        self.assertEqual(template['Parameters']['AssessmentsEnabled']['Default'],'false')
        self.assertEqual(properties['Environment']['Variables']['ASSESSMENTS_ENABLED'],{'Ref':'AssessmentsEnabled'})
        self.assertEqual(template['Resources']['HttpApi']['Properties']['Auth']['DefaultAuthorizer'],'Cognito')
