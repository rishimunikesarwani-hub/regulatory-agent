"""Metadata-only tracing checks with the real SDK and no external traffic."""
import json
import os
import unittest
import httpx
from unittest.mock import MagicMock, patch

from langfuse import Langfuse
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter

from regulatory_agent import langfuse_trace as tracing


class LangfuseTracingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.exporter = InMemorySpanExporter()
        cls.client = Langfuse(public_key='pk-lf-tracing-test', secret_key='sk-lf-tracing-test',
            tracer_provider=TracerProvider(), span_exporter=cls.exporter)

    @classmethod
    def tearDownClass(cls):
        cls.client.shutdown()

    def setUp(self):
        self.exporter.clear()
        self.record = {'job_id':'b'*32, 'event_id':'a'*32, 'stage_id':'assess-O-1-0',
            'stage':'model_call', 'operation':'model', 'model_id':'openai:gpt-4.1-mini-2025-04-14',
            'state':'succeeded', 'duration_seconds':1.2, 'dispatched':True,
            'usage':{'input_tokens':100, 'output_tokens':50},
            'owner':'PRIVATE_OWNER', 'prompt':'PRIVATE_PROMPT', 'output':'PRIVATE_OUTPUT'}

    def test_lf01_lf03_lf04_parent_types_and_stable_names(self):
        root=tracing.start_job({'job_id':'b'*32}, client=self.client)
        self.assertIsNotNone(root)
        observation=tracing.start_attempt(self.record, client=self.client, parent=root)
        self.assertTrue(tracing.export_attempt(self.record, observation=observation))
        tracing.finish_job(root, {'state':'completed', 'model_calls':1, 'stop_reason':None})
        self.client.flush()
        spans=self.exporter.get_finished_spans()
        child=next(s for s in spans if s.name=='generate-assessment')
        parent=next(s for s in spans if s.name=='assess-regulatory-evidence')
        self.assertEqual(child.parent.span_id, parent.context.span_id)
        self.assertEqual(child.context.trace_id, parent.context.trace_id)
        self.assertEqual(child.attributes['langfuse.observation.type'], 'generation')
        self.assertEqual(parent.attributes['langfuse.observation.type'], 'agent')
        self.assertIn('gpt-4.1-mini-2025-04-14', str(child.attributes))
        for value in ('PRIVATE_OWNER','PRIVATE_PROMPT','PRIVATE_OUTPUT'):
            self.assertNotIn(value,str([s.attributes for s in spans]))
        self.assertFalse(any('input'==k or k.endswith('.input') or k.endswith('.output') for s in spans for k in s.attributes))

    def test_lf05_failed_update_still_ends_observation(self):
        observation=MagicMock(); observation.update.side_effect=RuntimeError('PRIVATE')
        self.assertFalse(tracing.export_attempt(self.record, observation=observation))
        observation.end.assert_called_once()

    def test_lf06_disabled_configuration_never_constructs_client(self):
        with patch.dict(os.environ,{},clear=True), patch.object(tracing,'_client') as client:
            self.assertIsNone(tracing.start_job({'job_id':'b'*32}))
            self.assertIsNone(tracing.start_attempt(self.record))
            client.assert_not_called()

    def test_lf02_pipeline_nests_extraction_and_generation(self):
        from test_slice05_pipeline import PipelineTests
        from regulatory_agent.openai_model import OpenAIModel, MODEL
        fixture=PipelineTests(); fixture.setUp(); self.addCleanup(fixture.doCleanups)
        fixture.snapshot=fixture.snapshot.model_copy(update={'snapshot_id':'trace-pipeline','model_version':MODEL})
        fixture.store.save_snapshot(fixture.owner,fixture.snapshot)
        fixture.run=fixture.reviews.admit(fixture.owner,fixture.case,'tracing-run',fixture.snapshot.snapshot_id,'synthetic_live')
        fixture.job_id=fixture.run['job_id']
        actions=iter([fixture.extraction(),fixture.controls(),fixture.proposed(),fixture.proposed('O-2')])
        self.provider_requests=[]
        self.provider_outputs=[]
        def respond(request):
            self.provider_requests.append(json.loads(request.content))
            content=next(actions); self.provider_outputs.append(content)
            return httpx.Response(200,json={'model':'gpt-4.1-mini-2025-04-14',
                'usage':{'prompt_tokens':100,'completion_tokens':50},
                'choices':[{'finish_reason':'stop','message':{'content':content}}]})
        with httpx.Client(transport=httpx.MockTransport(respond)) as provider, \
                patch.object(tracing,'configured',return_value=True), patch.object(tracing,'_client',return_value=self.client):
            outcome,_,_=fixture.execute(model=OpenAIModel('offline-test',client=provider))
        self.assertEqual(outcome['state'],'completed')
        self.client.flush(); spans=self.exporter.get_finished_spans()
        self.assertEqual(sum(s.name=='assess-regulatory-evidence' for s in spans),1)
        extract=next(s for s in spans if s.name=='extract-obligations')
        parent=next(s for s in spans if s.context.span_id==extract.parent.span_id)
        self.assertEqual(parent.name,'extract-evidence')
        self.assertTrue(any(s.attributes.get('langfuse.observation.type')=='retriever' for s in spans))
        self.assertNotIn(fixture.owner,str([s.attributes for s in spans]))

    def test_dd01_dd05_actual_model_messages_and_responses_without_credentials(self):
        with patch.dict(os.environ, {'APP_ENV':'local','LANGFUSE_CAPTURE_CONTENT':'fictional-local'}):
            self.test_lf02_pipeline_nests_extraction_and_generation()
        generations=[s for s in self.exporter.get_finished_spans() if s.attributes.get('langfuse.observation.type')=='generation']
        self.assertEqual(len(generations),4)
        for span,request,response in zip(generations,self.provider_requests,self.provider_outputs):
            self.assertEqual(json.loads(span.attributes['langfuse.observation.input']),request['messages'])
            self.assertEqual(json.loads(span.attributes['langfuse.observation.output']),{'role':'assistant','content':response})
            self.assertIn('prompt_version',str(span.attributes))
            self.assertIn('response_format',str(span.attributes))
        self.assertNotIn('offline-test',str([s.attributes for s in generations]))

    def test_dd01_dd02_dd05_disabled_capture_and_failure_isolation(self):
        snapshot={'synthetic':True,'mode':'historical','model_version':'openai:gpt-4.1-mini-2025-04-14','prompt_version':'example'}
        observation=MagicMock()
        with tracing.model_observation(observation):
            for setting,change in [({},{}),({'LANGFUSE_CAPTURE_CONTENT':'fictional-local'},{}),({'APP_ENV':'production','LANGFUSE_CAPTURE_CONTENT':'fictional-local'},{}),
                    ({'APP_ENV':'local','LANGFUSE_CAPTURE_CONTENT':'fictional-local'},{'synthetic':False}),
                    ({'APP_ENV':'local','LANGFUSE_CAPTURE_CONTENT':'fictional-local'},{'mode':'current'}),
                    ({'APP_ENV':'local','LANGFUSE_CAPTURE_CONTENT':'fictional-local'},{'model_version':'bedrock:example'})]:
                with patch.dict(os.environ,setting,clear=True):
                    self.assertFalse(tracing.capture_model_content(snapshot|change,input=[{'role':'user','content':'PRIVATE'}]))
            observation.update.assert_not_called()
            observation.update.side_effect=RuntimeError('PRIVATE')
            with patch.dict(os.environ,{'APP_ENV':'local','LANGFUSE_CAPTURE_CONTENT':'fictional-local'},clear=True):
                self.assertFalse(tracing.capture_model_content(snapshot,output={'role':'assistant','content':'fictional'}))
        self.assertFalse(tracing.capture_model_content(snapshot,output='outside observation'))

    def test_lf05_lf06_root_update_failure_is_isolated(self):
        root=MagicMock(); root.update.side_effect=RuntimeError('PRIVATE')
        self.assertFalse(tracing.finish_job(root, {'state':'failed'}))
        root.end.assert_called_once()

    def test_lf05_unfinished_stage_ends_as_interrupted(self):
        from regulatory_agent.assessment_pipeline import AssessmentPipeline
        service=MagicMock(); service.store.read_job.return_value={'state':'failed','model_calls':0}
        pipeline=AssessmentPipeline(service,MagicMock())
        pipeline._trace_root=tracing.start_job({'job_id':'b'*32},client=self.client)
        record=self.record|{'operation':'retrieval','stage':'retrieval'}
        pending=tracing.start_attempt(record,client=self.client,parent=pipeline._trace_root)
        pipeline._trace_observations={'pending':pending}; pipeline._trace_stack=['pending']
        pipeline._end_trace('PRIVATE_OWNER','PRIVATE_CASE','b'*32)
        self.client.flush(); spans=self.exporter.get_finished_spans()
        self.assertEqual(len(spans),2)
        child=next(s for s in spans if s.name=='retrieve-evidence')
        self.assertIn('interrupted',str(child.attributes))
        self.assertNotIn('PRIVATE_OWNER',str([s.attributes for s in spans]))
        self.assertEqual(pipeline._trace_observations,{})
        self.assertEqual(pipeline._trace_stack,[])
        self.assertIsNone(pipeline._trace_root)
