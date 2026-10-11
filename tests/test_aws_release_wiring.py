"""RW01-RW06 release behavior without AWS traffic or credentials."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import yaml

from ops import deploy_dev
from test_slice01_release import COMMIT, configuration


class ReleaseWiringTests(unittest.TestCase):
    def test_rw05_workflow_preserves_explicit_approval_and_scope(self):
        root=Path(deploy_dev.ROOT)
        workflow=yaml.safe_load((root/'.github/workflows/dev-release.yml').read_text())
        selection=workflow['on']['workflow_dispatch']['inputs']['enable_assessments']
        self.assertEqual(selection['type'],'boolean');self.assertIs(selection['default'],False)
        release=workflow['jobs']['deploy-development']
        self.assertEqual(release['env']['AWS_DEV_ASSESSMENTS_ENABLED'],"${{ inputs.enable_assessments && 'true' || 'false' }}")
        self.assertEqual(release['env']['AWS_DEV_ASSESSMENT_RELEASE_APPROVED_SHA'],
                         '${{ vars.AWS_DEV_ASSESSMENT_RELEASE_APPROVED_SHA }}')
        browser=next(step for step in release['steps'] if step.get('id')=='browser')
        self.assertEqual(browser['env']['DEPLOYED_ASSESSMENTS_ENABLED'],'${{ env.AWS_DEV_ASSESSMENTS_ENABLED }}')
        template=yaml.safe_load((root/'ops/sam-dev.yaml').read_text())
        self.assertEqual(template['Outputs']['AssessmentsEnabled']['Value'],{'Ref':'AssessmentsEnabled'})
        self.assertEqual(template['Parameters']['AssessmentsEnabled']['Default'],'false')

    def deploy(self, requested=None, observed='false'):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory); (root/'src/web/dist').mkdir(parents=True)
            env=configuration() | {'GITHUB_OUTPUT':str(root/'output')}
            if requested is not None:
                env.update(AWS_DEV_ASSESSMENTS_ENABLED=requested,
                           AWS_DEV_ASSESSMENT_RELEASE_APPROVED_SHA=COMMIT)
            outputs={'CommitSha':COMMIT,'ApiUrl':'https://api.example.test','CognitoDomain':'https://identity.example.test',
                     'UserPoolClientId':'client','FrontendUrl':'https://frontend.example.test',
                     'FrontendBucket':'fictional-frontend','DistributionId':'fictional-distribution'}
            if observed is not None: outputs['AssessmentsEnabled']=observed
            calls=[]
            def command(*args,**kwargs):
                calls.append(args)
                if args[:3]==('git','rev-parse','HEAD'): return COMMIT
                if args[:3]==('aws','sts','get-caller-identity'): return json.dumps({'Account':env['AWS_DEV_ACCOUNT_ID']})
                if args[:3]==('aws','cloudformation','describe-stacks'):
                    return json.dumps({'Stacks':[{'Outputs':[{'OutputKey':k,'OutputValue':v} for k,v in outputs.items()]}]})
                if args[:3]==('aws','cloudfront','create-invalidation'): return json.dumps({'Invalidation':{'Id':'fictional'}})
                return ''
            with patch.dict(os.environ,env,clear=True), patch.object(deploy_dev,'ROOT',root), \
                 patch.object(deploy_dev.os,'chdir'), patch.object(deploy_dev,'command',side_effect=command), \
                 patch.object(deploy_dev,'package_application'):
                try: deploy_dev.main()
                except ValueError:
                    self.assertFalse(any(c[:3]==('aws','s3','sync') for c in calls))
                    self.assertFalse(any(c[:3]==('aws','cloudfront','create-invalidation') for c in calls))
                    raise
            return calls,json.loads((root/'src/web/dist/config.json').read_text()),json.loads((root/'runs/releases/development.json').read_text())

    def test_rw01_and_rw04_backend_frontend_and_evidence_agree(self):
        for requested,observed,expected in ((None,'false',False),('true','true',True)):
            with self.subTest(requested=requested):
                calls,config,record=self.deploy(requested,observed)
                deploy=next(c for c in calls if c[:2]==('sam','deploy'))
                self.assertIn(f'AssessmentsEnabled={str(expected).lower()}',deploy)
                self.assertIs(config['assessments_enabled'],expected)
                self.assertIs(record['assessments_enabled'],expected)

    def test_rw02_rejects_invalid_flag_or_missing_exact_commit_approval_before_commands(self):
        for setting,approval in (('yes',COMMIT),('TRUE',COMMIT),('',COMMIT),('true',None),('true','b'*40)):
            env=configuration() | {'AWS_DEV_ASSESSMENTS_ENABLED':setting}
            if approval is not None: env['AWS_DEV_ASSESSMENT_RELEASE_APPROVED_SHA']=approval
            with self.subTest(setting=setting,approval=approval),patch.dict(os.environ,env,clear=True), \
                 patch.object(deploy_dev.os,'chdir'),patch.object(deploy_dev,'command') as command:
                with self.assertRaises(ValueError): deploy_dev.main()
                command.assert_not_called()

    def test_rw03_stack_flag_mismatch_stops_before_asset_upload(self):
        for requested,observed in ((None,None),(None,'invalid'),(None,'true'),('true','false')):
            with self.subTest(requested=requested,observed=observed),self.assertRaises(ValueError):
                self.deploy(requested,observed)

    def test_rw06_successful_document_checks_cannot_verify_enabled_assessments(self):
        for enabled in (False,True):
            with self.subTest(enabled=enabled),tempfile.TemporaryDirectory() as directory:
                root=Path(directory); path=root/'runs/releases/development.json';path.parent.mkdir(parents=True)
                path.write_text(json.dumps({'commit':COMMIT,'environment':'development','url':'https://fictional.cloudfront.net',
                    'assessments_enabled':enabled,'limitations':['Fictional data only.']}))
                env=os.environ.copy() | {'GITHUB_SHA':COMMIT,'DEPLOYMENT_RESULT':'success','BROWSER_RESULT':'success'}
                env.pop('ASSESSMENT_BROWSER_RESULT',None)
                result=subprocess.run([sys.executable,'-X','utf8',str(Path(deploy_dev.ROOT)/'ops/record_release.py')],
                    cwd=root,env=env,capture_output=True,text=True)
                self.assertEqual(result.returncode,0,result.stderr)
                record=json.loads(path.read_text())
                self.assertEqual(record['acceptance_scope'],'identity_cases_documents')
                self.assertEqual(record['status'],'unverified' if enabled else 'verified_development_slice')

    def test_rw06_only_successful_assessment_checks_extend_the_verified_scope(self):
        for outcome in ('unknown','failure','skipped','success'):
            with self.subTest(outcome=outcome),tempfile.TemporaryDirectory() as directory:
                root=Path(directory);path=root/'runs/releases/development.json';path.parent.mkdir(parents=True)
                path.write_text(json.dumps({'commit':COMMIT,'environment':'development','url':'https://fictional.cloudfront.net',
                    'assessments_enabled':True,'limitations':['Assessment AWS acceptance is pending.','Private uploads are disabled.']}))
                env=os.environ.copy() | {'GITHUB_SHA':COMMIT,'DEPLOYMENT_RESULT':'success','BROWSER_RESULT':'success',
                    'ASSESSMENT_BROWSER_RESULT':outcome}
                r=subprocess.run([sys.executable,'-X','utf8',str(Path(deploy_dev.ROOT)/'ops/record_release.py')],
                    cwd=root,env=env,capture_output=True,text=True)
                self.assertEqual(r.returncode,0,r.stderr)
                record=json.loads(path.read_text())
                self.assertEqual(record['status'],'verified_development_slice' if outcome=='success' else 'unverified')
                self.assertEqual(record['acceptance_scope'],'identity_cases_documents_assessments_reviews_exports'
                                 if outcome=='success' else 'identity_cases_documents')
                self.assertIn('Private uploads are disabled.',record['limitations'])
                self.assertEqual('Assessment AWS acceptance is pending.' in record['limitations'],outcome!='success')


if __name__=='__main__': unittest.main()
