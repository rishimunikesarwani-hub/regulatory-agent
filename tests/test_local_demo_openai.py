"""Submission-day provider, accounting, and trace privacy checks. No external traffic."""
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import MagicMock, patch

import httpx

from regulatory_agent.contracts import ContractError, Snapshot
from regulatory_agent.local import Store


class LocalDemoTests(unittest.TestCase):
    def setUp(self):
        from regulatory_agent.openai_model import OpenAIModel, MODEL
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = Store(Path(self.temp.name)/'demo.sqlite')
        self.store.create_case('owner-1','case-1',{'name':'Fictional bank'})
        self.snapshot = Snapshot(snapshot_id='snapshot-1',case_id='case-1',bank_profile={'name':'Fictional bank'},
            selected_versions={'regulation':'1'}, selected_obligations=['obligation-1'], assessment_date='2024-04-08',
            mode='historical',prompt_version='live-vs5-v1',model_version=MODEL,synthetic=True)
        self.store.save_snapshot('owner-1', self.snapshot)
        self.job = self.store.enqueue('owner-1','case-1','snapshot-1','request-1',now=1000)
        self.token = self.store.claim('owner-1','case-1',self.job['job_id'],now=1000)
        self.now = 1001; self.requests = []
        self.action = {'action':'propose_findings','snapshot_id':'snapshot-1','document_version_ids':['regulation:1'],
            'passage_ids':[],'findings':[],'obligations':[],'controls':[],'retrieval_query':None}
        self.payload = {'model':'gpt-4.1-mini-2025-04-14','usage':{'prompt_tokens':100,'completion_tokens':50},
            'choices':[{'finish_reason':'stop','message':{'content':json.dumps(self.action),'refusal':None}}]}
        self.status=200
        def respond(request):
            self.requests.append(request)
            return httpx.Response(self.status,json=self.payload,headers={'x-request-id':'req-demo-1'})
        self.client = httpx.Client(transport=httpx.MockTransport(respond)); self.addCleanup(self.client.close)
        self.adapter = OpenAIModel('test-secret',client=self.client,clock=lambda:self.now)
        self.request={'system':'Use supplied evidence only.','prompt':'Fictional bank text.','max_tokens':512}

    def dispatch(self,owner='owner-1'):
        return self.adapter.dispatch(self.store,owner,'case-1',self.job['job_id'],self.token,self.request)

    def calls(self):
        return self.store.read_job('owner-1','case-1',self.job['job_id'])['model_calls']

    def test_ld01_live_reply_identifies_openai_and_uses_strict_schema(self):
        reply=self.dispatch(); body=json.loads(self.requests[0].content)
        self.assertEqual(reply.label,'Live'); self.assertEqual(reply.model_id,self.snapshot.model_version)
        self.assertEqual(reply.actual_response_model_id,'gpt-4.1-mini-2025-04-14')
        self.assertEqual(reply.usage.input_tokens,100); self.assertEqual(reply.provider_request_id,'req-demo-1')
        self.assertTrue(body['response_format']['json_schema']['strict']); self.assertFalse(body['store'])
        self.assertEqual(str(self.requests[0].url),'https://api.openai.com/v1/chat/completions')
        self.assertEqual(self.calls(),1)

    def test_ld02_provider_selection_is_local_and_explicit(self):
        from regulatory_agent.openai_model import selected_model, MODEL
        with patch.dict(os.environ,{'APP_ENV':'local','MODEL_PROVIDER':'openai'},clear=True):
            self.assertEqual(selected_model(),MODEL)
        with patch.dict(os.environ,{'APP_ENV':'aws','MODEL_PROVIDER':'openai'},clear=True):
            with self.assertRaisesRegex(ContractError,'local_demo_only'): selected_model()

    def test_ld03_private_or_current_snapshot_never_dispatches(self):
        for changes in ({'synthetic':False},{'mode':'current'},{'model_version':'in.openai.gpt-5.6-luna'}):
            with patch.object(self.store,'get',return_value=self.snapshot.model_dump()|changes):
                with self.assertRaises(ContractError): self.dispatch()
        self.assertEqual(self.requests,[]); self.assertEqual(self.calls(),0)

    def test_ld04_other_owner_never_dispatches(self):
        with self.assertRaises(ContractError): self.dispatch('other-owner')
        self.assertEqual(self.requests,[])

    def test_ld05_rejection_is_safe_and_one_call_no_hidden_retry(self):
        self.status=401; self.payload={'error':{'message':'PRIVATE provider detail test-secret'}}
        with self.assertRaisesRegex(ContractError,'openai_provider_rejected') as error:self.dispatch()
        self.assertNotIn('PRIVATE',str(error.exception)); self.assertEqual(self.calls(),1)
        self.assertEqual(len(self.requests),1)

    def test_ld06_deadline_after_reservation_blocks_dispatch(self):
        reserve=self.store.reserve
        def delayed(*args,**kwargs):
            value=reserve(*args,**kwargs); self.now=1601; return value
        with patch.object(self.store,'reserve',side_effect=delayed):
            with self.assertRaises(ContractError) as error:self.dispatch()
        self.assertFalse(error.exception.dispatched); self.assertEqual(self.requests,[]); self.assertEqual(self.calls(),1)

    def test_ld07_invalid_scope_or_refusal_never_becomes_a_finding(self):
        self.payload['choices'][0]['message']['content']=json.dumps(self.action|{'snapshot_id':'other-snapshot'})
        with self.assertRaisesRegex(ContractError,'model_scope_denied'):self.dispatch()
        self.payload['choices'][0]['message']['refusal']='PRIVATE refusal'
        with self.assertRaisesRegex(ContractError,'model_response_incomplete'):self.dispatch()

    def test_ld08_optional_langfuse_receives_allowlisted_metadata_only(self):
        from regulatory_agent.langfuse_trace import export_attempt
        client=MagicMock(); observation=client.start_observation.return_value
        record={'event_id':'a'*32,'job_id':'b'*32,'snapshot_id':'snapshot-1','stage_id':'extract-controls',
            'operation':'model','model_id':self.snapshot.model_version,'actual_response_model_id':'gpt-4.1-mini-2025-04-14',
            'state':'succeeded','duration_seconds':1.2,'dispatched':True,'usage':{'input_tokens':100,'output_tokens':50},
            'started_at':'2026-10-11T09:00:00+00:00','finished_at':'2026-10-11T09:00:01.200000+00:00',
            'owner':'PRIVATE_OWNER','prompt':'PRIVATE_PROMPT','output':'PRIVATE_RESPONSE','errors':[]}
        self.assertTrue(export_attempt(record,client=client))
        sent=str(client.mock_calls)
        for secret in ('PRIVATE_OWNER','PRIVATE_PROMPT','PRIVATE_RESPONSE'):self.assertNotIn(secret,sent)
        self.assertTrue(observation.end.called)
        self.assertIn('usage_details',sent)

    def test_ld09_langfuse_failure_does_not_fail_local_assessment(self):
        from regulatory_agent.langfuse_trace import export_attempt
        client=MagicMock(); client.start_observation.side_effect=RuntimeError('PRIVATE secret')
        self.assertFalse(export_attempt({'job_id':'b'*32,'event_id':'a'*32,'stage_id':'stage','operation':'model'},client=client))

    def test_ld10_invalid_request_and_exhausted_budget_never_dispatch(self):
        self.request['max_tokens']=True
        with self.assertRaisesRegex(ContractError,'invalid_model_request'):self.dispatch()
        self.request['max_tokens']=512
        for _ in range(24):self.store.reserve('owner-1','case-1',self.job['job_id'],self.token,'model',now=1001)
        with self.assertRaisesRegex(ContractError,'allowance_exhausted'):self.dispatch()
        self.assertEqual(self.requests,[])

    def test_ld11_timeout_is_unknown_without_retry(self):
        def timeout(request):raise httpx.ReadTimeout('PRIVATE',request=request)
        with httpx.Client(transport=httpx.MockTransport(timeout)) as client:
            self.adapter.client=client
            with self.assertRaisesRegex(ContractError,'model_dispatch_outcome_unknown'):self.dispatch()
        self.assertEqual(self.calls(),1)

    def test_ld12_missing_keys_report_safe_configuration_failure(self):
        from regulatory_agent.openai_model import OpenAIModel
        with patch.dict(os.environ,{},clear=True):
            with self.assertRaisesRegex(ContractError,'openai_key_missing'):OpenAIModel.configured()

    def test_ld13_complete_pipeline_exports_openai_identity_despite_langfuse_failure(self):
        from test_slice05_pipeline import PipelineTests
        from regulatory_agent.openai_model import OpenAIModel, MODEL
        fixture=PipelineTests(); fixture.setUp(); self.addCleanup(fixture.doCleanups)
        fixture.snapshot=fixture.snapshot.model_copy(update={'snapshot_id':'openai-pipeline','model_version':MODEL})
        fixture.store.save_snapshot(fixture.owner,fixture.snapshot)
        run=fixture.reviews.admit(fixture.owner,fixture.case,'openai-run',fixture.snapshot.snapshot_id,'synthetic_live')
        actions=iter([fixture.extraction(),fixture.controls(),fixture.proposed(),fixture.proposed('O-2')])
        def respond(request):
            self.requests.append(request)
            return httpx.Response(200,json={'model':'gpt-4.1-mini-2025-04-14','usage':{'prompt_tokens':100,'completion_tokens':50},
                'choices':[{'finish_reason':'stop','message':{'content':next(actions)}}]})
        with httpx.Client(transport=httpx.MockTransport(respond)) as client, \
                patch('regulatory_agent.langfuse_trace.start_attempt',return_value=None), \
                patch('regulatory_agent.langfuse_trace.export_attempt',return_value=False) as export:
            pipeline=fixture.Pipeline(fixture.service,OpenAIModel('test-secret',client=client))
            outcome=pipeline.run(fixture.owner,fixture.case,run['job_id'])
            self.assertEqual(outcome['state'],'completed')
            self.assertGreaterEqual(export.call_count,4)
        report=fixture.service.read(fixture.owner,fixture.case,run['job_id'])
        self.assertEqual(len(report['findings']),2); self.assertEqual(report['live_model_calls'],4)
        self.assertTrue(all(f['model_id']==MODEL for f in report['findings']))
        attempts=[a for a in report['trace']['attempts'] if a['operation']=='model']
        self.assertTrue(all(a['actual_response_model_id']=='gpt-4.1-mini-2025-04-14' for a in attempts))
        self.assertTrue(all(a['versions']['model_configuration']=='openai-demo-v1' for a in attempts))

    def test_ld14_installed_langfuse_sdk_exports_metadata_without_content(self):
        from langfuse import Langfuse
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter
        from regulatory_agent.langfuse_trace import start_attempt, export_attempt
        exporter=InMemorySpanExporter(); provider=TracerProvider()
        client=Langfuse(public_key='pk-lf-offline-demo',secret_key='sk-lf-offline-demo',
            tracer_provider=provider,span_exporter=exporter,
            should_export_span=lambda span:span.instrumentation_scope.name=='langfuse-sdk')
        self.addCleanup(client.shutdown)
        record={'job_id':'b'*32,'event_id':'a'*32,'stage_id':'extract-obligations','operation':'model',
            'model_id':self.snapshot.model_version,'state':'succeeded','duration_seconds':1.0,'dispatched':True,
            'usage':{'input_tokens':100,'output_tokens':50},'prompt':'PRIVATE_PROMPT','output':'PRIVATE_RESPONSE'}
        observation=start_attempt(record,client=client)
        self.assertIsNotNone(observation)
        self.assertTrue(export_attempt(record,client=client,observation=observation)); client.flush()
        spans=exporter.get_finished_spans(); self.assertEqual(len(spans),1)
        attributes=str(spans[0].attributes)
        self.assertNotIn('PRIVATE_PROMPT',attributes); self.assertNotIn('PRIVATE_RESPONSE',attributes)
        self.assertIn('100',attributes); self.assertIn('gpt-4.1-mini-2025-04-14',attributes)
