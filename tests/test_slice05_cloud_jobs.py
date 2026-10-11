"""Native cloud job contracts with controlled SDK responses. No external service or inference."""
import copy
import hashlib
import json
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor
from types import SimpleNamespace
from unittest.mock import patch

from botocore.config import Config
from botocore.exceptions import ClientError
from botocore.session import Session
from botocore.validate import validate_parameters

from regulatory_agent.aws_cases import DynamoDBCases
from regulatory_agent.cases import CaseError, CaseService
from regulatory_agent.contracts import ContractError, PERIOD_PROMPT, Snapshot


class Dynamo:
    meta = SimpleNamespace(region_name='ap-south-1', endpoint_url='https://dynamodb.ap-south-1.amazonaws.com',
        config=Config(retries={'total_max_attempts':1,'mode':'standard'}))

    def __init__(self):
        self.items = {}; self.calls = []; self.lock = threading.Lock()
        self.interleave = None; self.after_read = None; self.lost_ack = False; self.failure = None
        self.model = Session().get_service_model('dynamodb')

    @staticmethod
    def key(item): return item['PK']['S'],item['SK']['S']

    def get_item(self, **args):
        validate_parameters(args,self.model.operation_model('GetItem').input_shape)
        with self.lock:
            self.calls.append(('get',copy.deepcopy(args)))
            saved = copy.deepcopy(self.items.get(self.key(args['Key'])))
        if args['Key']['SK']['S'].startswith('JOB#') and self.after_read:
            callback,self.after_read=self.after_read,None; callback()
        return {'Item':saved} if saved else {}

    def put_item(self, **args):
        validate_parameters(args,self.model.operation_model('PutItem').input_shape)
        if self.interleave:
            callback,self.interleave = self.interleave,None; callback()
        with self.lock:
            self.calls.append(('put',copy.deepcopy(args)))
            key = self.key(args['Item']); old = self.items.get(key)
            expected = args.get('ExpressionAttributeValues',{}).get(':expected',{}).get('N')
            if old is not None if expected is None else old is None or old['revision']['N'] != expected:
                raise ClientError({'Error':{'Code':'ConditionalCheckFailedException'}},'PutItem')
            if self.failure: raise self.failure
            self.items[key] = copy.deepcopy(args['Item'])
            if self.lost_ack:
                self.lost_ack = False; raise OSError('Uncertain acknowledgement')
        return {}


class Artifacts:
    def __init__(self): self.data = {}; self.calls = []; self.failure = False

    def save_extraction(self, owner, case, identity, data):
        self.calls.append(('save',owner,case,identity))
        if self.failure: raise OSError('Storage unavailable')
        ref = {'upload_id':identity+'-extracted','version_id':'v1','size_bytes':len(data),
            'key':f'owners/{owner}/cases/{case}/uploads/{identity}-extracted','sha256':hashlib.sha256(data).hexdigest()}
        self.data[(owner,case,ref['upload_id'],'v1')] = bytes(data)
        return ref

    def read_extraction(self, owner, case, reference):
        self.calls.append(('read',owner,case,reference['upload_id']))
        raw = self.data[(owner,case,reference['upload_id'],reference['version_id'])]
        if hashlib.sha256(raw).hexdigest() != reference['sha256'] or len(raw) != reference['size_bytes']:
            raise ContractError('artifact_integrity_failure')
        return raw


class CloudJobTests(unittest.TestCase):
    def setUp(self):
        from regulatory_agent.aws_jobs import DynamoJobs
        self.client = Dynamo(); self.objects = Artifacts()
        self.cases = CaseService(DynamoDBCases(self.client,'cases'))
        self.owner = 'cloud-job-operator'
        self.case = self.cases.create(self.owner,{'bank_profile':{'name':'Fictional cloud job bank'},'synthetic':True}).case_id
        self.snapshot = Snapshot(snapshot_id='snapshot-1',case_id=self.case,bank_profile={'name':'Fictional cloud job bank'},
            selected_versions={'rbi':'v1','bank':'v1'},selected_document_ids={'rbi':'rbi-artifact','bank':'bank-artifact'},
            selected_obligations=['O1','O2'],assessment_date='2024-04-08',mode='historical',
            prompt_version=PERIOD_PROMPT,model_version='in.openai.gpt-5.6-luna',synthetic=True)
        self.jobs = DynamoJobs(self.cases,self.client,'cases',self.objects)

    def start(self):
        job = self.jobs.admit(self.owner,self.snapshot,'request-1',now=1)
        token = self.jobs.claim(self.owner,self.case,job['job_id'],now=10)
        return job['job_id'],token

    def test_cj01_identical_admission_preserves_job_snapshot_and_artifact(self):
        first = self.jobs.admit(self.owner,self.snapshot,'request-1',now=1)
        repeated = self.jobs.admit(self.owner,self.snapshot,'request-1',now=5)
        self.assertEqual(first,repeated)
        self.assertEqual(sum(c[0]=='save' for c in self.objects.calls),1)
        self.assertEqual(self.jobs.snapshot(self.owner,self.case,first['job_id']),self.snapshot.model_dump(mode='json'))
        with self.assertRaises(ContractError):
            self.jobs.admit(self.owner,self.snapshot.model_copy(update={'assessment_date':'2024-04-09'}),'request-1')
        for changed in ({'synthetic':False},{'mode':'current'},{'prompt_version':'unapproved'},{'model_version':'global.model'}):
            with self.assertRaises(ContractError): self.jobs.admit(self.owner,self.snapshot.model_copy(update=changed),'request-2')

    def test_cj02_wrong_owner_case_and_forged_saved_identity_are_denied(self):
        identity,_ = self.start(); before = len(self.objects.calls)
        with self.assertRaises(CaseError): self.jobs.read_job('outside',self.case,identity)
        with self.assertRaises(CaseError): self.jobs.read_job(self.owner,'outside',identity)
        self.assertEqual(len(self.objects.calls),before)
        key = next(k for k in self.client.items if k[1].startswith('JOB#'))
        saved = json.loads(self.client.items[key]['body']['S']); saved['case_id']='outside'
        self.client.items[key]['body']['S'] = json.dumps(saved)
        with self.assertRaises(ContractError): self.jobs.read_job(self.owner,self.case,identity)

    def test_cj03_mumbai_clients_and_native_conditional_shapes(self):
        from regulatory_agent.aws_jobs import DynamoJobs
        identity,_ = self.start(); self.jobs.read_job(self.owner,self.case,identity)
        self.assertTrue(all(args['ConsistentRead'] for operation,args in self.client.calls if operation=='get'))
        writes = [a for op,a in self.client.calls if op=='put' and a['Item']['SK']['S'].startswith('JOB#')]
        self.assertTrue(all(a.get('ConditionExpression') for a in writes))
        for region,endpoint in (('us-east-1','https://dynamodb.us-east-1.amazonaws.com'),
                                ('ap-south-1','https://proxy.example.com')):
            client = Dynamo(); client.meta=SimpleNamespace(region_name=region,endpoint_url=endpoint)
            with self.assertRaises(ValueError): DynamoJobs(self.cases,client,'cases',self.objects)
        client=Dynamo(); client.meta=SimpleNamespace(region_name='ap-south-1',endpoint_url='https://dynamodb.ap-south-1.amazonaws.com',
            config=Config(retries={'total_max_attempts':2,'mode':'standard'}))
        with self.assertRaises(ValueError): DynamoJobs(self.cases,client,'cases',self.objects)

    def test_cj04_claim_race_and_lease_recovery_keep_the_original_budget(self):
        job = self.jobs.admit(self.owner,self.snapshot,'request-1',now=1); identity=job['job_id']
        winner=[]
        self.client.interleave=lambda: winner.append(self.jobs.claim(self.owner,self.case,identity,now=10))
        self.assertIsNone(self.jobs.claim(self.owner,self.case,identity,now=10))
        token=winner[0]; self.assertTrue(token)
        self.jobs.reserve(self.owner,self.case,identity,token,'model',now=11)
        recovered=self.jobs.claim(self.owner,self.case,identity,now=42)
        self.assertNotEqual(token,recovered)
        saved=self.jobs.read_job(self.owner,self.case,identity)
        self.assertEqual((saved['started_at'],saved['deadline'],saved['model_calls']),(10,610,1))
        with self.assertRaises(ContractError): self.jobs.reserve(self.owner,self.case,identity,token,'model',now=43)

    def test_cj05_concurrent_and_uncertain_reservations_never_reset_allowances(self):
        identity,token=self.start()
        def reserve(_):
            try: return self.jobs.reserve(self.owner,self.case,identity,token,'model',now=11)
            except ContractError: return None
        with ThreadPoolExecutor(max_workers=8) as pool: results=list(pool.map(reserve,range(36)))
        saved=self.jobs.read_job(self.owner,self.case,identity)
        self.assertLessEqual(saved['model_calls'],24); self.assertEqual(len(set(r for r in results if r)),len([r for r in results if r]))
        for _ in range(24-saved['model_calls']): self.jobs.reserve(self.owner,self.case,identity,token,'model',now=11)
        with self.assertRaises(ContractError): self.jobs.reserve(self.owner,self.case,identity,token,'model',now=11)
        self.client.lost_ack=True
        with self.assertRaises(OSError): self.jobs.reserve(self.owner,self.case,identity,token,'retrieval',now=12)
        self.assertEqual(self.jobs.read_job(self.owner,self.case,identity)['retrieval_calls'],1)
        for _ in range(19): self.jobs.reserve(self.owner,self.case,identity,token,'retrieval',now=12)
        with self.assertRaises(ContractError): self.jobs.reserve(self.owner,self.case,identity,token,'retrieval',now=12)

    def test_cj06_renewal_preserves_deadline_and_rejects_expired_claims(self):
        identity,token=self.start(); self.jobs.renew(self.owner,self.case,identity,token,now=20)
        saved=self.jobs.read_job(self.owner,self.case,identity)
        self.assertEqual((saved['deadline'],saved['lease_until']),(610,50))
        with self.assertRaises(ContractError): self.jobs.renew(self.owner,self.case,identity,token,now=51)
        late=self.jobs.claim(self.owner,self.case,identity,now=611)
        self.assertIsNone(late)
        self.assertEqual(self.jobs.read_job(self.owner,self.case,identity)['deadline'],610)

    def test_cj07_large_stage_uses_versioned_artifact_and_cannot_be_changed(self):
        identity,token=self.start(); output={'text':'fictional '*30_000,'accounted_obligations':['O1']}
        self.jobs.save_stage(self.owner,self.case,identity,token,'obligation-O1',output,now=11)
        self.assertEqual(self.jobs.read_job(self.owner,self.case,identity)['stages']['obligation-O1'],output)
        metadata=next(json.loads(v['body']['S']) for k,v in self.client.items.items() if k[1].startswith('JOB#'))
        self.assertNotIn(output['text'],json.dumps(metadata)); self.assertLess(len(json.dumps(metadata)),400_000)
        before=len(self.objects.calls)
        self.jobs.save_stage(self.owner,self.case,identity,token,'obligation-O1',output,now=12)
        self.assertEqual(sum(c[0]=='save' for c in self.objects.calls[before:]),0)
        with self.assertRaises(ContractError): self.jobs.save_stage(self.owner,self.case,identity,token,'obligation-O1',{'different':True},now=13)
        with self.assertRaises(ContractError): self.jobs.save_stage(self.owner,self.case,identity,token,'outside',{'accounted_obligations':['outside']},now=13)

    def test_cj08_lost_claim_and_storage_failure_cannot_attach_outputs(self):
        identity,token=self.start()
        self.client.interleave=lambda: self.jobs.claim(self.owner,self.case,identity,now=41)
        with self.assertRaises(ContractError): self.jobs.save_stage(self.owner,self.case,identity,token,'lost',{'accounted_obligations':['O1']},now=11)
        self.assertEqual(self.jobs.read_job(self.owner,self.case,identity)['stages'],{})
        self.objects.failure=True
        current=self.jobs.read_job(self.owner,self.case,identity)['token']
        with self.assertRaises(OSError): self.jobs.save_stage(self.owner,self.case,identity,current,'failed',{'accounted_obligations':['O1']},now=42)
        self.assertEqual(self.jobs.read_job(self.owner,self.case,identity)['stages'],{})

    def test_cj09_finalization_requires_exact_scope_and_preserves_partial_results(self):
        identity,token=self.start()
        with self.assertRaises(ContractError): self.jobs.finalize(self.owner,self.case,identity,token,'completed',[],now=11)
        self.jobs.save_stage(self.owner,self.case,identity,token,'O1',{'accounted_obligations':['O1']},now=11)
        with self.assertRaises(ContractError): self.jobs.finalize(self.owner,self.case,identity,token,'partial',[],now=12)
        self.jobs.finalize(self.owner,self.case,identity,token,'partial',['O2'],reason='deadline_exhausted',now=611)
        saved=self.jobs.read_job(self.owner,self.case,identity)
        self.assertEqual((saved['state'],saved['unchecked_obligations']),( 'partial',['O2']))
        self.assertEqual(saved['stages']['O1']['accounted_obligations'],['O1'])

    def test_cj10_terminal_retry_and_corrupt_artifact_never_become_new_execution(self):
        identity,token=self.start()
        self.jobs.save_stage(self.owner,self.case,identity,token,'all',{'accounted_obligations':['O1','O2']},now=11)
        with self.assertRaises(ContractError): self.jobs.finalize(self.owner,self.case,identity,token,'completed',[],now=611)
        self.jobs.finalize(self.owner,self.case,identity,token,'completed',[],now=12)
        self.assertIsNone(self.jobs.claim(self.owner,self.case,identity,now=99))
        for key in self.objects.data:
            if b'accounted_obligations' in self.objects.data[key]: self.objects.data[key]=b'altered artifact'
        with self.assertRaises(ContractError): self.jobs.read_job(self.owner,self.case,identity)

    def test_cj11_elapsed_storage_reads_recheck_time_before_mutation(self):
        identity,token=self.start()
        self.jobs.save_stage(self.owner,self.case,identity,token,'all',{'accounted_obligations':['O1','O2']},now=11)
        for operation in ('reserve','renew','finalize'):
            stamp=[20]
            self.client.after_read=lambda: stamp.__setitem__(0,611)
            with patch('regulatory_agent.aws_jobs.time.time',side_effect=lambda:stamp[0]):
                with self.assertRaisesRegex(ContractError,'deadline_or_lease_exhausted'):
                    if operation=='reserve': self.jobs.reserve(self.owner,self.case,identity,token,'model')
                    elif operation=='renew': self.jobs.renew(self.owner,self.case,identity,token)
                    else: self.jobs.finalize(self.owner,self.case,identity,token,'completed',[])
        self.assertEqual(self.jobs.read_job(self.owner,self.case,identity)['model_calls'],0)
        failure=self.jobs.admit(self.owner,self.snapshot,'request-failure',now=1)['job_id']
        failed_token=self.jobs.claim(self.owner,self.case,failure,now=10)
        self.jobs.finalize(self.owner,self.case,failure,failed_token,'failed',['O1','O2'],reason='deadline_exhausted',now=611)
        self.assertEqual(self.jobs.read_job(self.owner,self.case,failure)['state'],'failed')


if __name__ == '__main__': unittest.main()
