"""Native cloud API and complete pinned sources with controlled service state."""
import base64
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from urllib.parse import parse_qs,urlsplit
import yaml

import test_slice05_cloud_execution as execution
import test_slice05_cloud_records as records
import test_slice02_s3 as transport
from test_slice01_aws import event
from regulatory_agent.aws_cases import create_handler
from regulatory_agent.contracts import ContractError, StartAssessment


class CloudAPITests(unittest.TestCase):
    def setUp(self):
        self.f=execution.CloudAdmissionTests('runTest'); self.f.setUp(); self.addCleanup(self.f.doCleanups)
        self.service=self.f.service; self.owner,self.case=self.f.owner,self.f.case
        self.root=f'/api/cases/{self.case}'

    def handler(self,**kwargs):
        return create_handler(self.f.cases,user_pool_id='ap-south-1_pool',user_pool_client_id='client-id',
            assessments=self.service,queue=self.f.queue,**kwargs)

    def call(self,method,path,payload=None,**changes):
        return self.handler()(event(method,self.root+path,payload,self.owner)|changes,None)

    def test_ca06_earlier_full_source_records_keep_original_downloads(self):
        run=self.f.admit()
        full=self.f.documents.read_full(self.owner,self.case,self.f.version)
        metadata=self.f.store._metadata(self.owner,self.case,'document',self.f.version)
        record=self.f.store.prepare(self.owner,self.case,'document',self.f.version,full,int(metadata['revision']['N']))
        self.assertTrue(self.f.store.commit(self.owner,self.case,[record]))
        original=self.f.documents._source(self.owner,self.case,self.f.version)
        raw=self.f.objects.read(self.owner,self.case,original['original'])
        self.assertEqual(self.service.source_original(self.owner,self.case,run['job_id'],self.f.version),(raw,'fictional.txt'))
        signed=[]
        def download(owner,case,reference,filename):
            signed.append((owner,case,reference,filename))
            return 'https://controlled.s3.ap-south-1.amazonaws.com/original?versionId=original-v1'
        self.f.objects.download=download
        result=self.call('GET',f"/assessments/{run['job_id']}/sources/{self.f.version}/original")
        self.assertEqual(result['statusCode'],200)
        self.assertEqual(signed,[(self.owner,self.case,original['original'],'fictional.txt')])

    def test_ca01_disabled_and_invalid_claims_do_not_construct_clients(self):
        calls=[]
        def factory(): calls.append('private-client'); return self.service
        disabled=create_handler(self.f.cases,user_pool_id='ap-south-1_pool',user_pool_client_id='client-id')
        self.assertEqual(disabled(event('GET',self.root+'/assessment-selection',owner=self.owner),None)['statusCode'],503)
        enabled=create_handler(self.f.cases,user_pool_id='ap-south-1_pool',user_pool_client_id='client-id',assessments=factory)
        request=event('GET',self.root+'/assessment-selection',owner=self.owner)
        request['requestContext']['authorizer']['jwt']['claims']['token_use']='id'
        self.assertEqual(enabled(request,None)['statusCode'],401); self.assertEqual(calls,[])

    def test_ca02_case_ownership_precedes_factory_and_body_owner_is_rejected(self):
        calls=[]
        handler=create_handler(self.f.cases,user_pool_id='ap-south-1_pool',user_pool_client_id='client-id',
            assessments=lambda:calls.append('assessment'),queue=lambda:calls.append('queue'))
        self.assertEqual(handler(event('GET',self.root+'/assessment-selection',owner='other-owner'),None)['statusCode'],404)
        self.assertEqual(calls,[])
        result=self.call('POST','/assessments/selected',self.f.request.model_dump()|{'owner_id':self.owner})
        self.assertEqual(result['statusCode'],422); self.assertEqual(self.f.sqs.sent,[])

    def test_ca03_uncertain_send_preserves_one_admission_and_returns_safe_error(self):
        self.f.sqs.lost_ack=True
        first=self.call('POST','/assessments/selected',self.f.request.model_dump())
        self.assertEqual(first['statusCode'],503); self.assertNotIn('Uncertain',first['body'])
        second=self.call('POST','/assessments/selected',self.f.request.model_dump())
        self.assertEqual(second['statusCode'],202); run=json.loads(second['body'])
        self.assertEqual(len(self.service.list(self.owner,self.case)['runs']),1)
        self.assertEqual(json.loads(self.f.sqs.sent[0]['MessageBody'])['job_id'],run['job_id'])
        self.assertEqual(self.f.sqs.sent[0],self.f.sqs.sent[1]); self.assertNotIn('token',run)

    def test_ca04_current_and_controlled_routes_do_not_start_processing(self):
        current=self.f.request.model_dump()|{'mode':'current'}
        self.assertEqual(self.call('POST','/assessments/selected',current)['statusCode'],503)
        self.assertEqual(self.call('POST','/assessments',self.f.request.model_dump())['statusCode'],404)
        self.assertEqual(self.f.sqs.sent,[]); self.assertEqual(self.service.list(self.owner,self.case)['runs'],[])

    def large(self):
        raw=(('Fictional '+('x'*110))+'\n')*2001; raw=raw.encode()
        upload=self.f.documents.reserve(self.owner,self.case,{'x-filename':'large.txt','x-document-kind':'policy',
            'x-synthetic':'true'},len(raw),'large-policy')
        version=upload['upload_id']; self.f.objects.originals[(self.owner,self.case,version)]=raw
        self.f.documents.finalize(self.owner,self.case,version)
        request=self.f.request.model_copy(update={'selected_versions':{
            self.f.regulation['document']['source_id']:self.f.regulation['document']['version'],version:'1'},'idempotency_key':'large-run'})
        return self.f.selection.admit(self.owner,self.case,request),version,raw

    def test_ca05_large_complete_source_uses_pinned_references_without_an_expanded_record(self):
        run,version,raw=self.large(); body=self.f.store.get(self.owner,self.case,'document',version)
        self.assertNotIn('passages',body); self.assertIn('original',body); self.assertIn('extraction',body)
        self.assertLess(len(json.dumps(body)),6000)
        snapshot=self.f.store.get(self.owner,self.case,'snapshot',run['snapshot_id'])
        source=next(s for s in self.f.store.sources(self.owner,self.case,snapshot) if s['document']['document_version_id']==version)
        self.assertEqual(len(source['passages']),2001)
        self.assertEqual(self.service.source_original(self.owner,self.case,run['job_id'],version),(raw,'large.txt'))

    def test_ca06_replacement_and_corruption_cannot_change_saved_source(self):
        run=self.f.admit(); before=self.f.store.get(self.owner,self.case,'document',self.f.version)
        raw=b'Fictional replacement policy.'
        upload=self.f.documents.reserve(self.owner,self.case,{'x-filename':'replacement.txt','x-document-kind':'policy',
            'x-synthetic':'true','x-source-id':self.f.version},len(raw),'replacement')
        identity=upload['upload_id']; self.f.objects.originals[(self.owner,self.case,identity)]=raw
        self.f.documents.finalize(self.owner,self.case,identity)
        original,filename=self.service.source_original(self.owner,self.case,run['job_id'],self.f.version)
        self.assertNotEqual(original,raw); self.assertEqual(filename,'fictional.txt')
        self.assertEqual(self.f.store.get(self.owner,self.case,'document',self.f.version),before)
        self.f.objects.originals[(self.owner,self.case,self.f.version)]=b'changed'
        snapshot=self.f.store.get(self.owner,self.case,'snapshot',run['snapshot_id'])
        with self.assertRaises(ContractError): self.f.store.sources(self.owner,self.case,snapshot)

    def test_ca07_source_pages_keep_ids_counts_offsets_and_selected_scope(self):
        run=self.f.admit(); job=run['job_id']
        for offset,count,next_offset in ((0,500,500),(500,10,None)):
            reply=self.call('GET',f'/assessments/{job}/sources/{self.f.version}',queryStringParameters={'offset':str(offset)})
            self.assertEqual(reply['statusCode'],200); source=json.loads(reply['body'])
            self.assertEqual(source['offset'],offset); self.assertEqual(source['passage_count'],510)
            self.assertEqual(len(source['passages']),count); self.assertEqual(source['next_offset'],next_offset)
            self.assertEqual(source['passages'][0]['passage_id'],f'{self.f.version}-{offset+1}')
        self.assertEqual(self.call('GET',f'/assessments/{job}/sources/not-selected')['statusCode'],404)
        catalog=self.call('GET','/assessment-selection'); self.assertEqual(catalog['statusCode'],200)
        for source in json.loads(catalog['body'])['sources']:
            self.assertNotIn('original',source); self.assertNotIn('extraction',source); self.assertNotIn('passages',source)

    def test_ca08_native_review_and_reports_keep_revision_and_cutoff_rules(self):
        f=records.CloudRecordTests('runTest'); f.setUp(); self.addCleanup(f.doCleanups)
        item=f.present(); handler=create_handler(f.cases,user_pool_id='ap-south-1_pool',user_pool_client_id='client-id',assessments=f.service)
        path=f'/api/cases/{f.case}/assessments/{f.job}'
        response=handler(event('POST',path+f'/findings/{item.finding_id}/reviews',f.request().model_dump(mode='json'),f.owner),None)
        self.assertEqual(response['statusCode'],201); self.assertEqual(json.loads(response['body'])['revision'],1)
        duplicate=handler(event('POST',path+f'/findings/{item.finding_id}/reviews',f.request().model_dump(mode='json'),f.owner),None)
        self.assertEqual(duplicate['body'],response['body'])
        report=handler(event('GET',path,owner=f.owner),None); self.assertEqual(report['statusCode'],200)
        self.assertEqual(len(json.loads(report['body'])['reviews']),1)

    def test_ca16_default_cutoff_cannot_precede_returned_records(self):
        from datetime import datetime,timedelta
        from regulatory_agent.reviews import instant
        f=records.CloudRecordTests('runTest'); f.setUp(); self.addCleanup(f.doCleanups)
        item=f.present(); available=instant(item.available_at)
        clock=[available-timedelta(seconds=1)]; read=f.service._read_records
        def collected(*args):
            saved=read(*args); clock[0]=available+timedelta(seconds=1); return saved
        with patch('regulatory_agent.assessments.datetime') as date, patch.object(f.service,'_read_records',side_effect=collected):
            date.now.side_effect=lambda zone:clock[0]
            report=f.service.read(f.owner,f.case,f.job)
            self.assertEqual(len(report['findings']),1)
            self.assertGreaterEqual(instant(report['summary']['cutoff']),available)
            historical=f.service.read(f.owner,f.case,f.job,(available-timedelta(seconds=1)).isoformat())
            self.assertEqual(len(historical['findings']),0)

    def test_ca09_resume_preserves_job_and_excludes_execution_token(self):
        run=self.f.admit(); job=run['job_id']; token=self.f.store.claim(self.owner,self.case,job)
        before=self.f.store.read_job(self.owner,self.case,job)
        reply=self.call('POST',f'/assessments/{job}/resume')
        self.assertEqual(reply['statusCode'],202); self.assertNotIn('token',json.loads(reply['body']))
        self.assertEqual(self.f.store.read_job(self.owner,self.case,job),before); self.assertEqual(self.f.sqs.sent,[])
        self.assertEqual(before['token'],token)

    def test_ca10_export_response_uses_private_artifact_and_full_export_bytes(self):
        run=self.f.admit(); job=run['job_id']; saved=[]
        def save(owner,case,identity,data):
            saved.append(data); return {'upload_id':identity+'-report','version_id':'v1','size_bytes':len(data),
                'sha256':hashlib.sha256(data).hexdigest(),'key':'private-controlled-key'}
        self.f.objects.save_report=save
        self.f.objects.download_report=lambda owner,case,reference,filename:'https://controlled.s3.ap-south-1.amazonaws.com/report?versionId=v1'
        cutoff='2026-10-11T00:00:00Z'; before=self.f.store.read_job(self.owner,self.case,job)
        for _ in range(2):
            reply=self.call('POST',f'/assessments/{job}/export',{'format':'json'},queryStringParameters={'cutoff':cutoff})
            self.assertEqual(reply['statusCode'],200); self.assertEqual(set(json.loads(reply['body'])),{'url','filename'})
        self.assertEqual(saved[0],saved[1]); body=json.loads(saved[0])
        self.assertEqual(len(next(s for s in body['sources'] if s['document']['kind']=='policy')['passages']),510)
        self.assertEqual(self.f.store.read_job(self.owner,self.case,job),before); self.assertEqual(self.f.sqs.sent,[])

    def test_ca12_invalid_bodies_queries_and_large_response_fail_without_private_text(self):
        for body in ('{',json.dumps(self.f.request.model_dump())+' '*32001):
            reply=self.call('POST','/assessments/selected',body=base64.b64encode(body.encode()).decode(),isBase64Encoded=True)
            self.assertEqual(reply['statusCode'],422)
        run=self.f.admit(); path=f'/assessments/{run["job_id"]}'
        for query in ({'cutoff':'not-a-date'},{'cutoff':'2099-01-01T00:00:00Z'}):
            self.assertEqual(self.call('GET',path,queryStringParameters=query)['statusCode'],422)
        for offset in ('-1','510','bad'):
            self.assertEqual(self.call('GET',path+f'/sources/{self.f.version}',queryStringParameters={'offset':offset})['statusCode'],422)
        with patch.object(self.service,'read',return_value={'private_text':'p'*4_000_001}):
            reply=self.call('GET',path); self.assertEqual(reply['statusCode'],503); self.assertNotIn('private_text',reply['body'])


class CloudArtifactTests(unittest.TestCase):
    def test_ca11_storage_destination_rejects_userinfo_ports_and_other_regions(self):
        from regulatory_agent.aws_document_objects import S3DocumentObjects
        from regulatory_agent.cases import CaseError
        transport=object.__new__(S3DocumentObjects); transport.bucket='test-documents'
        valid='https://test-documents.s3.ap-south-1.amazonaws.com/report'
        self.assertEqual(transport._target(valid),valid)
        for url in (valid.replace('https://','https://user:password@'),valid.replace('.com/','.com:8443/'),
                    valid.replace('ap-south-1','ap-south-2')):
            with self.subTest(url=url), self.assertRaises(CaseError): transport._target(url)

    def setUp(self):
        self.f=transport.S3DocumentTransportTests('runTest'); self.f.setUp(); self.addCleanup(self.f.tearDown)
        self.objects=self.f.objects; self.data=b'{"label":"Fictional assessment"}\n'
        self.digest=hashlib.sha256(self.data).hexdigest(); self.checksum=base64.b64encode(bytes.fromhex(self.digest)).decode()
        self.key=self.f.key.replace(transport.UPLOAD,'report-one-report')
        self.reference={'upload_id':'report-one-report','key':self.key,'version_id':'report-v1',
                        'size_bytes':len(self.data),'sha256':self.digest}

    def head(self,**changes):
        self.f.ready()
        self.f.stub.add_response('head_object',{'ContentLength':len(self.data),'VersionId':'report-v1',
            'ServerSideEncryption':'AES256','ChecksumSHA256':self.checksum,'ChecksumType':'FULL_OBJECT'}|changes,
            {'Bucket':transport.BUCKET,'Key':self.key,'VersionId':'report-v1','ExpectedBucketOwner':transport.ACCOUNT,'ChecksumMode':'ENABLED'})

    def test_ca11_report_write_and_download_validate_native_shapes_and_exact_version(self):
        self.f.ready()
        self.f.stub.add_response('put_object',{'VersionId':'report-v1','ServerSideEncryption':'AES256','ChecksumSHA256':self.checksum},
            {'Bucket':transport.BUCKET,'Key':self.key,'Body':self.data,'ContentType':'application/octet-stream',
             'ServerSideEncryption':'AES256','ExpectedBucketOwner':transport.ACCOUNT,'ChecksumSHA256':self.checksum})
        reference=self.objects.save_report('operator-a',self.f.case,'report-one',self.data)
        self.assertEqual(reference,self.reference)
        self.head(); url=self.objects.download_report('operator-a',self.f.case,reference,'assessment-one.json')
        target=urlsplit(url); params=parse_qs(target.query)
        self.assertEqual(target.hostname,f'{transport.BUCKET}.s3.ap-south-1.amazonaws.com')
        self.assertEqual(params['versionId'],['report-v1']); self.assertEqual(params['X-Amz-Expires'],['300'])

    def test_ca11_report_scope_metadata_and_checksum_fail_before_signing(self):
        from regulatory_agent.cases import CaseError
        for changes in ({'key':'other-owner/report'},{'version_id':'null'},{'upload_id':'ordinary-upload'},
                        {'sha256':'not-a-hash'},{'size_bytes':128_000_001}):
            with self.assertRaises((CaseError,ContractError)):
                self.objects.download_report('operator-a',self.f.case,self.reference|changes,'assessment-one.json')
        with self.assertRaises(CaseError): self.objects.download_report('operator-b',self.f.case,self.reference,'assessment-one.json')
        for changes in ({'ChecksumSHA256':base64.b64encode(b'wrong-checksum').decode()},
                        {'ContentLength':len(self.data)+1},{'VersionId':'other-version'},{'ServerSideEncryption':'aws:kms'},
                        {'ChecksumType':'COMPOSITE'}):
            self.head(**changes)
            with patch.object(self.f.s3,'generate_presigned_url') as sign:
                with self.assertRaises(CaseError): self.objects.download_report('operator-a',self.f.case,self.reference,'assessment-one.json')
                sign.assert_not_called()


class CloudDeploymentTests(unittest.TestCase):
    def test_ca13_relocated_public_package_loads_the_real_historical_catalog(self):
        from ops.deploy_dev import package_application
        from regulatory_agent.aws_execution import CloudSelection
        fixture=execution.CloudAdmissionTests('runTest'); fixture.setUp(); self.addCleanup(fixture.doCleanups)
        project=Path(__file__).resolve().parents[1]
        manifest=json.loads((project/'data/sources/source-manifest.json').read_text())
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary)
            (root/'src/regulatory_agent').mkdir(parents=True); (root/'src/regulatory_agent/__init__.py').write_text('')
            (root/'ops').mkdir(); (root/'ops/requirements.lock').write_text('pydantic==2.14.1\n')
            (root/'data/sources').mkdir(parents=True)
            (root/'data/sources/source-manifest.json').write_text(json.dumps(manifest))
            for entry in manifest['versions']:
                if entry['synthetic']: continue
                target=root/entry['raw_path']; target.parent.mkdir(parents=True,exist_ok=True)
                target.write_bytes((project/entry['raw_path']).read_bytes())
            package=root/'runs/private/sam-package'; package_application(root,package)
            catalog=CloudSelection(fixture.service,root=package).catalog(fixture.owner,fixture.case)
            self.assertGreater(len(catalog['obligations']),0)
            self.assertTrue(any(source['document']['kind']=='regulation' for source in catalog['sources']))
            self.assertTrue(all('passages' not in source for source in catalog['sources']))
            self.assertFalse((package/'data/fixtures').exists())

    def test_ca13_package_keeps_only_verified_public_sources_and_recovers_previous_package(self):
        from ops.deploy_dev import package_application
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary); source=root/'src/regulatory_agent'; source.mkdir(parents=True)
            (source/'__init__.py').write_text('')
            (root/'ops').mkdir(); (root/'ops/requirements.lock').write_text('pydantic==2.14.1\n')
            assets=root/'data/sources'; assets.mkdir(parents=True); raw=b'<p>Historical public RBI excerpt.</p>'
            (assets/'archive.html').write_bytes(raw)
            manifest={'versions':[{'synthetic':False,'raw_path':'data/sources/archive.html','sha256':hashlib.sha256(raw).hexdigest(),
                'source_url':'https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=12562'},
                {'synthetic':True,'private_label':'Do not package this'}]}
            (assets/'source-manifest.json').write_text(json.dumps(manifest))
            (assets/'unselected-secret.txt').write_text('Do not package this')
            (root/'data/fixtures').mkdir(); (root/'data/fixtures/held-out.json').write_text('Do not package this')
            destination=root/'runs/private/sam-package'; destination.mkdir(parents=True)
            (destination/'unwanted-private-file.txt').write_text('Preserve in archive only')
            package_application(root,destination)
            self.assertEqual((destination/'data/sources/archive.html').read_bytes(),raw)
            packaged=json.loads((destination/'data/sources/source-manifest.json').read_text())
            self.assertEqual(len(packaged['versions']),1)
            self.assertEqual(sorted(str(p.relative_to(destination)).replace('\\','/') for p in destination.rglob('*') if p.is_file()),
                ['data/sources/archive.html','data/sources/source-manifest.json','regulatory_agent/__init__.py','requirements.txt'])
            self.assertEqual(len(list((root/'runs/private/package-archive').rglob('unwanted-private-file.txt'))),1)
            manifest['versions'][0]['sha256']='0'*64; (assets/'source-manifest.json').write_text(json.dumps(manifest))
            with self.assertRaises(ValueError): package_application(root,destination)
            self.assertEqual((destination/'data/sources/archive.html').read_bytes(),raw)
            manifest['versions'][0].update(raw_path='data/fixtures/held-out.json',sha256=hashlib.sha256(b'Do not package this').hexdigest())
            (assets/'source-manifest.json').write_text(json.dumps(manifest))
            with self.assertRaises(ValueError): package_application(root,destination)

    def test_ca14_queue_worker_and_roles_match_execution_and_access_contracts(self):
        root=Path(__file__).resolve().parents[1]
        application=yaml.safe_load((root/'ops/sam-dev.yaml').read_text())
        bootstrap=yaml.safe_load((root/'ops/aws-development-bootstrap.yaml').read_text())
        resources=application['Resources']; queue=resources['AssessmentQueue']; dead=resources['AssessmentDeadLetterQueue']
        self.assertEqual(application['Parameters']['AssessmentsEnabled']['Default'],'false')
        self.assertEqual(queue['Properties']['VisibilityTimeout'],3960); self.assertTrue(queue['Properties']['SqsManagedSseEnabled'])
        self.assertEqual(queue['Properties']['RedrivePolicy']['maxReceiveCount'],5)
        self.assertGreater(dead['Properties']['MessageRetentionPeriod'],queue['Properties']['MessageRetentionPeriod'])
        worker=resources['AssessmentWorker']['Properties']; self.assertEqual(worker['Timeout'],660)
        self.assertNotIn('ReservedConcurrentExecutions',worker)
        event=worker['Events']['QueuedAssessment']['Properties']
        self.assertEqual(event['BatchSize'],1); self.assertEqual(event['FunctionResponseTypes'],['ReportBatchItemFailures'])
        self.assertEqual(event['ScalingConfig']['MaximumConcurrency'],2)
        for name in ('AssessmentQueue','AssessmentDeadLetterQueue','AssessmentWorker'):
            self.assertEqual(resources[name]['Condition'],'AssessmentsEnabled')
        case=resources['CaseFunction']['Properties']; self.assertEqual(case['Environment']['Variables']['ASSESSMENTS_ENABLED'],{'Ref':'AssessmentsEnabled'})
        paths={item['Properties']['Path'] for item in case['Events'].values()}
        for suffix in ('assessment-selection','assessments/selected','assessments/{job_id}/export',
                       'assessments/{job_id}/sources/{version_id}','assessments/{job_id}/findings/{finding_id}/reviews'):
            self.assertIn('/api/cases/{case_id}/'+suffix,paths)
        role=bootstrap['Resources']['AssessmentWorkerRole']; self.assertEqual(role['Properties']['RoleName'],'regulatory-agent-dev-assessment-worker')
        statements=[statement for policy in role['Properties']['Policies'] for statement in policy['PolicyDocument']['Statement']]
        actions={action for statement in statements for action in statement['Action']}
        self.assertTrue({'dynamodb:ConditionCheckItem','sqs:ReceiveMessage','sqs:DeleteMessage','bedrock:InvokeModel','bedrock:GetInferenceProfile'}<=actions)
        inference=[statement for statement in statements if 'bedrock:InvokeModel' in statement['Action']]
        serialized=json.dumps(inference)
        self.assertNotIn('foundation-model/*',serialized); self.assertNotIn('global.',serialized)
        self.assertIn('ap-south-2',serialized); self.assertIn('bedrock:InferenceProfileArn',serialized)
        runtime=bootstrap['Resources']['CaseRuntimeRole']['Properties']['Policies'][0]['PolicyDocument']['Statement']
        self.assertTrue(any('sqs:SendMessage' in statement['Action'] for statement in runtime))
        self.assertTrue(any('dynamodb:ConditionCheckItem' in statement['Action'] for statement in runtime))


if __name__=='__main__': unittest.main()
