"""VS5 native SDK dispatch checks with fake credentials and zero external traffic."""
from datetime import datetime, timezone
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import boto3
from botocore.config import Config
from botocore.exceptions import ReadTimeoutError
from botocore.stub import ANY, Stubber

from regulatory_agent.contracts import ContractError, ModelReply, Snapshot
from regulatory_agent.local import Store, ControlledModel


PROFILE = 'in.openai.gpt-5.6-luna'
REGIONS = ('ap-south-1', 'ap-south-2')


class BedrockDispatchTests(unittest.TestCase):
    def setUp(self):
        from regulatory_agent.bedrock_model import BedrockModel
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = Store(Path(self.temp.name)/'jobs.sqlite')
        self.store.create_case('owner-1','case-1',{'name':'Fictional adapter bank'})
        self.snapshot = Snapshot(snapshot_id='snapshot-1',case_id='case-1',bank_profile={'name':'Fictional adapter bank'},
            selected_versions={'regulation':'1','policy':'1'},selected_obligations=['obligation-1'],
            assessment_date='2024-04-08',mode='historical',prompt_version='live-vs5-v1',model_version=PROFILE,synthetic=True)
        self.store.save_snapshot('owner-1',self.snapshot)
        for name in self.snapshot.selected_versions:
            self.store.put('owner-1','case-1','document',f'{name}:1',
                {'document':{'document_version_id':f'{name}:1','source_id':name,'version':'1'}})
        self.job = self.store.enqueue('owner-1','case-1','snapshot-1','request-1',now=1000)
        self.token = self.store.claim('owner-1','case-1',self.job['job_id'],now=1000)
        self.now = 1001
        cfg = Config(retries={'total_max_attempts':1,'mode':'standard'},connect_timeout=3,read_timeout=20)
        session = boto3.Session(region_name='ap-south-1',aws_access_key_id='test',aws_secret_access_key='test')
        self.runtime = session.client('bedrock-runtime',config=cfg)
        self.management = session.client('bedrock',config=cfg)
        self.runtime_stub = Stubber(self.runtime);self.runtime_stub.activate();self.addCleanup(self.runtime_stub.deactivate)
        self.management_stub = Stubber(self.management);self.management_stub.activate();self.addCleanup(self.management_stub.deactivate)
        self.adapter = BedrockModel(self.runtime,self.management,clock=lambda:self.now)
        self.request = {'system':'Assess only the supplied evidence.','prompt':'Fictional policy and regulatory passages.','max_tokens':512}
        self.action = {'action':'propose_findings','snapshot_id':'snapshot-1','document_version_ids':['regulation:1','policy:1'],
            'passage_ids':[],'findings':[],'obligations':[],'controls':[]}

    def profile(self, *, status='ACTIVE', regions=REGIONS):
        self.management_stub.add_response('get_inference_profile',{'inferenceProfileName':'India test profile',
            'inferenceProfileId':PROFILE,'inferenceProfileArn':f'arn:aws:bedrock:ap-south-1:123456789012:inference-profile/{PROFILE}',
            'type':'SYSTEM_DEFINED','status':status,'createdAt':datetime(2026,10,11,tzinfo=timezone.utc),
            'updatedAt':datetime(2026,10,11,tzinfo=timezone.utc),
            'models':[{'modelArn':f'arn:aws:bedrock:{region}::foundation-model/openai.gpt-5.6-luna'} for region in regions]},
            {'inferenceProfileIdentifier':PROFILE})

    def response(self, action=None, stop='end_turn', **changes):
        return {'output':{'message':{'role':'assistant','content':[{'text':json.dumps(action or self.action)}]}},
            'stopReason':stop,'usage':{'inputTokens':100,'outputTokens':50,'totalTokens':150},'metrics':{'latencyMs':20},
            'ResponseMetadata':{'RequestId':'provider-request-1','HTTPStatusCode':200,'RetryAttempts':0}} | changes

    def dispatch(self, request=None, owner='owner-1'):
        return self.adapter.dispatch(self.store,owner,'case-1',self.job['job_id'],self.token,request or self.request,now=self.now)

    def calls(self):
        return self.store.read_job('owner-1','case-1',self.job['job_id'])['model_calls']

    def test_mt11_slow_reservation_prevents_provider_dispatch_after_deadline(self):
        self.profile(); reserve=self.store.reserve
        def delayed(*args,**kwargs):
            result=reserve(*args,**kwargs); self.now=1601; return result
        with patch.object(self.store,'reserve',side_effect=delayed), patch.object(self.runtime,'converse',return_value=self.response()) as provider:
            with self.assertRaises(ContractError): self.dispatch()
            self.assertEqual(provider.call_count,0)
        self.assertEqual(self.calls(),1)

    def test_mt12_pre_dispatch_storage_failure_is_safe_and_known_undispatched(self):
        self.profile(); initial=self.store.read_job('owner-1','case-1',self.job['job_id'])
        with patch.object(self.store,'read_job',side_effect=[initial,OSError('PRIVATE STORAGE DETAIL')]), \
                patch.object(self.runtime,'converse',return_value=self.response()) as provider:
            with self.assertRaises(ContractError) as failure: self.dispatch()
            self.assertFalse(failure.exception.dispatched)
            self.assertNotIn('PRIVATE STORAGE DETAIL',str(failure.exception))
            self.assertEqual(provider.call_count,0)
        self.assertEqual(self.calls(),1)

    def test_mt01_native_request_pins_profile_schema_and_reserves_one_call(self):
        self.profile()
        expected={'modelId':PROFILE,'messages':[{'role':'user','content':[{'text':self.request['prompt']}]}],
            'system':ANY,'inferenceConfig':{'maxTokens':512},'outputConfig':ANY}
        self.runtime_stub.add_response('converse',self.response(),expected)
        captured=[]
        self.runtime.meta.events.register('before-parameter-build.bedrock-runtime.Converse',lambda params,**kw:captured.append(params.copy()))
        result=self.dispatch()
        self.assertEqual(self.calls(),1)
        self.assertEqual(result.label,'Live')
        self.assertEqual(result.model_id,PROFILE)
        self.assertEqual(captured[0]['outputConfig']['textFormat']['type'],'json_schema')
        schema=json.loads(captured[0]['outputConfig']['textFormat']['structure']['jsonSchema']['schema'])
        self.assertFalse(schema['additionalProperties'])
        self.assertEqual(set(schema['required']),set(schema['properties']))
        self.assertEqual(self.runtime.meta.config.retries['total_max_attempts'],1)
        self.runtime_stub.assert_no_pending_responses();self.management_stub.assert_no_pending_responses()

    def test_mt02_objects_unknown_fields_usage_and_request_identity_survive(self):
        self.profile()
        action=self.action|{'action':'find_controls','controls':[{'control_id':'control-1','statement':'Record privileged sessions.',
            'purpose':None,'owner':None,'frequency':None,'citations':[{'document_version_id':'policy:1','passage_id':'policy:1:line-1','location':'Line 1','quote':'Record privileged sessions.'}]}]}
        self.runtime_stub.add_response('converse',self.response(action))
        result=self.dispatch()
        self.assertIsNone(result.action.controls[0].owner)
        self.assertIsNone(result.action.controls[0].frequency)
        self.assertEqual(result.usage.input_tokens,100)
        self.assertEqual(result.usage.output_tokens,50)
        self.assertIsNone(result.usage.cache_read_tokens)
        self.assertEqual(result.provider_request_id,'provider-request-1')
        self.assertIsNone(result.actual_response_model_id)

    def test_mt03_missing_usage_remains_unknown_and_reasoning_is_discarded(self):
        self.profile()
        response=self.response();response.pop('usage')
        response['output']['message']['content'].append({'reasoningContent':{'reasoningText':{'text':'private reasoning','signature':'test'}}})
        with patch.object(self.runtime,'converse',return_value=response):result=self.dispatch()
        self.assertIsNone(result.usage.input_tokens)
        self.assertNotIn('private reasoning',result.model_dump_json())

    def test_mt04_malformed_and_outside_scope_outputs_count_and_fail(self):
        variants=[self.action|{'snapshot_id':'outside'},self.action|{'document_version_ids':['outside:1']},
            self.action|{'obligations':[{'obligation_id':'outside','requirement':'Unrelated rule.','conditions':[],'exceptions':[],
                'applicability':None,'citations':[{'document_version_id':'regulation:1','passage_id':'clause-1','location':'Clause 1','quote':'Rule.'}]}]},
            self.action|{'controls':[{'control_id':'c1','statement':'Unknown rule.','purpose':None,'owner':None,'frequency':None,
                'citations':[{'document_version_id':'outside:1','passage_id':'clause-1','location':'Clause 1','quote':'Rule.'}]}]}]
        for action in variants:
            self.profile();self.runtime_stub.add_response('converse',self.response(action))
            with self.assertRaises(ContractError):self.dispatch()
        self.profile();response=self.response();response['output']['message']['content']=[{'text':'not JSON'}]
        self.runtime_stub.add_response('converse',response)
        with self.assertRaises(ContractError):self.dispatch()
        self.assertEqual(self.calls(),5)

    def test_mt05_rejections_timeouts_and_truncation_never_retry(self):
        self.profile();self.runtime_stub.add_client_error('converse',service_error_code='AccessDeniedException',service_message='private provider detail')
        with self.assertRaises(ContractError) as failure:self.dispatch()
        self.assertNotIn('private provider detail',str(failure.exception))
        self.profile()
        with patch.object(self.runtime,'converse',side_effect=ReadTimeoutError(endpoint_url=self.runtime.meta.endpoint_url)) as call:
            with self.assertRaises(ContractError):self.dispatch()
            self.assertEqual(call.call_count,1)
        for stop in ('max_tokens','guardrail_intervened','tool_use'):
            self.profile();self.runtime_stub.add_response('converse',self.response(stop=stop))
            with self.assertRaises(ContractError) as failure:self.dispatch()
            self.assertEqual(failure.exception.usage.output_tokens,50)
            self.assertEqual(failure.exception.provider_request_id,'provider-request-1')
        self.assertEqual(self.calls(),5)

    def test_mt06_owner_profile_destination_and_private_guards_prevent_inference(self):
        with self.assertRaises(ContractError):self.dispatch(owner='other-owner')
        for regions in (('us-east-1',),):
            self.profile(regions=regions)
            with self.assertRaises(ContractError):self.dispatch()
        with patch.object(self.management,'get_inference_profile',return_value={'inferenceProfileId':PROFILE,'status':'ACTIVE','models':[]}):
            with self.assertRaises(ContractError):self.dispatch()
        self.profile(status='INACTIVE')
        with self.assertRaises(ContractError):self.dispatch()
        with self.store.transaction() as db:
            value=self.snapshot.model_dump()|{'synthetic':False}
            db.execute("UPDATE records SET body=? WHERE case_id='case-1' AND kind='snapshot' AND id='snapshot-1'",(json.dumps(value),))
        with self.assertRaises(ContractError):self.dispatch()
        self.assertEqual(self.calls(),0)

    def test_mt07_limits_prevent_dispatch_and_late_responses_are_unusable(self):
        self.now=1601
        with self.assertRaises(ContractError):self.dispatch()
        self.now=1001
        with self.store.transaction() as db:
            job=self.store._job(db,'owner-1','case-1',self.job['job_id']);job['model_calls']=24;self.store._save_job(db,job)
        with self.assertRaises(ContractError):self.dispatch()
        with self.store.transaction() as db:
            job=self.store._job(db,'owner-1','case-1',self.job['job_id']);job['model_calls']=0;self.store._save_job(db,job)
        self.profile();self.runtime_stub.add_response('converse',self.response())
        self.runtime.meta.events.register('after-call.bedrock-runtime.Converse',lambda **kw:setattr(self,'now',1601))
        with self.assertRaises(ContractError):self.dispatch()
        self.assertEqual(self.calls(),1)

    def test_mt09_citations_use_selected_saved_document_identity(self):
        # Uploaded version IDs differ from their source/version lookup keys.
        with self.store.transaction() as db:
            db.execute("UPDATE records SET body=? WHERE case_id='case-1' AND kind='document' AND id='policy:1'",
                (json.dumps({'document':{'document_version_id':'uploaded-version-1','source_id':'policy','version':'1'}}),))
        self.store.put('owner-1','case-1','document','unselected:1',
            {'document':{'document_version_id':'unselected-version','source_id':'unselected','version':'1'}})
        control={'control_id':'control-1','statement':'Record sessions.','purpose':None,'owner':None,'frequency':None,
            'citations':[{'document_version_id':'uploaded-version-1','passage_id':'saved-passage','location':'Line 1','quote':'Record sessions.'}]}
        action=self.action|{'action':'find_controls','controls':[control]}
        self.profile();self.runtime_stub.add_response('converse',self.response(action))
        self.assertEqual(self.dispatch().action.controls[0].citations[0].document_version_id,'uploaded-version-1')
        for forbidden in ('unselected-version','policy:1'):
            control['citations'][0]['document_version_id']=forbidden
            self.profile();self.runtime_stub.add_response('converse',self.response(action))
            with self.assertRaisesRegex(ContractError,'model_citation_scope_denied'):self.dispatch()
        self.assertEqual(self.calls(),3)

    def test_mt10_client_configuration_cannot_hide_routing_or_retries(self):
        from regulatory_agent.bedrock_model import BedrockModel
        session=boto3.Session(aws_access_key_id='test',aws_secret_access_key='test')
        for overrides, region, endpoint, error in (
            ({'total_max_attempts':2},'ap-south-1',None,'model_hidden_retries_denied'),
            ({'total_max_attempts':1},'us-east-1',None,'model_endpoint_denied'),
            ({'total_max_attempts':1},'ap-south-1','https://example.invalid','model_endpoint_denied')):
            with self.subTest(error=error,region=region):
                runtime=session.client('bedrock-runtime',region_name=region,endpoint_url=endpoint,
                    config=Config(retries=overrides,connect_timeout=3,read_timeout=20))
                with self.assertRaisesRegex(ContractError,error):BedrockModel(runtime,self.management)
        runtime=session.client('bedrock-runtime',region_name='ap-south-1',
            config=Config(retries={'total_max_attempts':1},connect_timeout=3,read_timeout=30))
        with self.assertRaisesRegex(ContractError,'model_timeout_configuration_denied'):BedrockModel(runtime,self.management)
        self.assertEqual(self.calls(),0)

    def test_mt08_request_limits_and_controlled_adapter_remain_compatible(self):
        for request in (self.request|{'modelId':'global.openai.gpt-5.6-luna'},self.request|{'prompt':'x'*400_001},
                        self.request|{'max_tokens':0},self.request|{'max_tokens':True}):
            with self.assertRaises(ContractError):self.dispatch(request)
        self.assertEqual(self.calls(),0)
        result=ControlledModel([json.dumps(self.action)]).dispatch(self.store,'owner-1','case-1',self.job['job_id'],self.token,{},now=1001)
        self.assertIsInstance(result,ModelReply)
        self.assertEqual(result.label,'Simulated')


if __name__=='__main__':
    unittest.main()
