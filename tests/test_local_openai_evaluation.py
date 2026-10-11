"""OE01 through OE12: frozen benchmark execution boundaries without external calls."""
from pathlib import Path
import json
import os
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


ROOT=Path(__file__).resolve().parents[1]


class LocalOpenAIEvaluationTests(unittest.TestCase):
    def test_oe11_diagnostic_child_keeps_fixed_codes_after_mandatory_audit_without_content(self):
        from ops.run_openai_evaluation import diagnostic_child
        from regulatory_agent.assessment_pipeline import AssessmentPipeline
        from regulatory_agent.contracts import ContractError
        from regulatory_agent import assessment_worker
        from types import SimpleNamespace
        saved=[]
        def finish(*args,**kwargs):saved.append('audit')
        def target(*args):
            event=SimpleNamespace(stage_id='validated-rule-1',stage='validation')
            for error in (ContractError('claim_citation_not_in_finding'),ValueError('PRIVATE_RESPONSE_KEY')):
                AssessmentPipeline._finish_attempt(None,None,None,None,None,(event,None),error=error)
                self.assertTrue(saved)
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'evaluation.sqlite'
            with patch.object(AssessmentPipeline,'_finish_attempt',finish),patch.object(assessment_worker,'bedrock_child',target):
                diagnostic_child(str(path),None,'owner','case','job-1','token')
            text=(path.parent/'job-1-diagnostic.json').read_text(encoding='utf-8')
            self.assertNotIn('PRIVATE_RESPONSE_KEY',text)
            self.assertNotIn('token',text)
            self.assertEqual(json.loads(text)[0]['code'],'claim_citation_not_in_finding')
            self.assertEqual(json.loads(text)[1]['code'],'unclassified_failure')
            with patch.object(AssessmentPipeline,'_finish_attempt',finish),patch.object(assessment_worker,'bedrock_child',target),\
                 patch.object(Path,'write_bytes',side_effect=OSError('PRIVATE_PATH')):
                diagnostic_child(str(path),None,'owner','case','job-2','token')
            with patch.object(AssessmentPipeline,'_finish_attempt',side_effect=RuntimeError('mandatory_audit_failed')),\
                 patch.object(assessment_worker,'bedrock_child',target):
                with self.assertRaisesRegex(RuntimeError,'mandatory_audit_failed'):
                    diagnostic_child(str(path),None,'owner','case','job-3','token')

    def test_oe12_subsequent_scoring_cannot_establish_held_out_sample(self):
        from ops.run_openai_evaluation import score
        labels=[{'case_id':f'EVAL-{i:02}','expected_status':'supported','critical_tags':[]} for i in range(1,21)]
        report=score(labels,[{'case_id':c['case_id'],'status':'supported','citations_resolve':[True]} for c in labels])
        self.assertEqual(report['primary_agreement']['value'],1)
        self.assertFalse(report['gates']['held_out_sample'])
        self.assertFalse(report['quality_gates_pass'])

    def test_oe10_default_cli_runs_without_credentials_or_model_calls(self):
        env={k:v for k,v in os.environ.items() if not k.upper().startswith(('PYTHONPATH','AWS_','OPENAI_','LANGFUSE_'))}
        run=subprocess.run([sys.executable,'ops/run_openai_evaluation.py'],cwd=ROOT,env=env,capture_output=True,text=True)
        self.assertEqual(run.returncode,0,run.stderr)
        self.assertEqual(json.loads(run.stdout)['model_calls'],0)

    def test_oe01_oe02_frozen_inputs_exclude_answers_and_reject_changed_hash(self):
        from ops.run_openai_evaluation import inputs
        cases,sources,selections,hashes=inputs(ROOT)
        self.assertEqual(len(cases),20)
        self.assertEqual(set(selections),{c['case_id'] for c in cases})
        self.assertNotIn('expected_status',json.dumps(cases))
        original=Path.read_bytes
        def changed(path):
            body=original(path)
            return body+b' ' if path.name=='held-out-inputs.json' else body
        with patch.object(Path,'read_bytes',changed):
            with self.assertRaisesRegex(ValueError,'frozen_hash_mismatch'):inputs(ROOT)

    def test_oe04_oe05_source_scope_preserves_frozen_passages(self):
        from ops.run_openai_evaluation import inputs,prepare
        from regulatory_agent.local import Store
        from regulatory_agent.assessment_pipeline import AssessmentPipeline
        cases,sources,selections,_=inputs(ROOT)
        with tempfile.TemporaryDirectory() as directory:
            store=Store(Path(directory)/'evaluation.sqlite')
            service,run=prepare(ROOT,store,cases[0],sources,selections[cases[0]['case_id']])
            saved=store.get(cases[0]['owner_id'],cases[0]['case_id'],'snapshot',run['snapshot_id'])
            actual,_=AssessmentPipeline(service,None)._sources(cases[0]['owner_id'],cases[0]['case_id'],saved)
            by_id={s['document']['source_id']:s for s in actual}
            for doc in cases[0]['documents']:
                self.assertEqual([p['text'] for p in by_id[doc['document_id']]['passages']],
                                 [p['text'] for p in doc['passages']])
                self.assertEqual([p['location'] for p in by_id[doc['document_id']]['passages']],
                                 [p['locator'] for p in doc['passages']])
            self.assertNotIn('expected_status',json.dumps(saved))
            self.assertEqual(saved['selected_obligations'],['RBI-IT-2023:29e'])

    def test_oe06_output_directory_cannot_use_feedback_or_existing_run(self):
        from ops.run_openai_evaluation import output_directory
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            with self.assertRaisesRegex(ValueError,'evaluation_path_denied'):
                output_directory(root,root/'runs/private/slice-05')
            target=root/'runs/private/openai-evaluations/run-1'
            self.assertEqual(output_directory(root,target),target)
            with self.assertRaisesRegex(FileExistsError,''):
                output_directory(root,target)

    def test_oe04_adversarial_fixture_text_uses_evidence_role_without_becoming_instructions(self):
        from ops.run_openai_evaluation import inputs,prepare
        from regulatory_agent.local import Store
        from regulatory_agent.assessment_pipeline import AssessmentPipeline
        cases,sources,selections,_=inputs(ROOT)
        with tempfile.TemporaryDirectory() as directory:
            store=Store(Path(directory)/'evaluation.sqlite')
            for case in (cases[16],cases[19]):
                service,run=prepare(ROOT,store,case,sources,selections[case['case_id']])
                snapshot=store.get(case['owner_id'],case['case_id'],'snapshot',run['snapshot_id'])
                saved,_=AssessmentPipeline(service,None)._sources(case['owner_id'],case['case_id'],snapshot)
                instruction=next(d for d in case['documents'] if d['kind']=='untrusted')
                source=next(s for s in saved if s['document']['source_id']==instruction['document_id'])
                self.assertEqual(source['document']['kind'],'evidence')
                self.assertEqual(source['fixture_kind'],'untrusted')
                self.assertEqual([p['text'] for p in source['passages']],[p['text'] for p in instruction['passages']])

    def test_oe07_oe09_errors_stay_in_denominator_and_support_stays_unknown(self):
        from ops.run_openai_evaluation import score
        labels=[{'case_id':f'EVAL-{i:02}','expected_status':'supported','critical_tags':[]} for i in range(1,21)]
        rows=[{'case_id':'EVAL-01','status':'supported','citations_resolve':[True]}]
        report=score(labels,rows)
        self.assertEqual(report['primary_agreement']['denominator'],20)
        self.assertEqual(report['primary_agreement']['numerator'],1)
        self.assertFalse(report['quality_gates_pass'])
        self.assertEqual(report['citation_support']['value'],None)
