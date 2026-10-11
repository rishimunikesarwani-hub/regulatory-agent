"""Stated date grounding checks. Controlled responses only, with no quality or live-access claim."""
import copy
import json
import unittest
import uuid
from unittest.mock import patch

import test_slice05_admission as admission
from pydantic import ValidationError
from regulatory_agent.assessment_pipeline import AssessmentPipeline, ranked_context
from regulatory_agent.contracts import ContractError, ModelReply, Snapshot, StartAssessment
from regulatory_agent.local import ControlledModel

PERIOD_PROMPT = 'assessment-vs5-selected-period-v1'
PERIOD = {'start':'2024-04-01', 'end':'2024-04-07'}


def source(texts, *, kind='evidence', format='txt'):
    return {'document':{'document_version_id':'d', 'source_id':'source', 'version':'1', 'kind':kind},
        'format':format, 'filename':'records-2024-04-01.txt', 'uploaded_at':'2024-04-08T00:00:00Z',
        'passages':[{'document_version_id':'d','passage_id':f'd-{i}', 'location':f'Row {i}', 'text':text}
                    for i,text in enumerate(texts,1)]}


class PeriodParsingTests(unittest.TestCase):
    def setUp(self):
        from regulatory_agent.evidence_periods import with_periods
        self.extract = with_periods

    def test_ep01_explicit_intervals_keep_exact_quotes_and_original_passages(self):
        for text in ('Records: 2024-04-01 to 2024-04-07.', 'Records: 1 April 2024 through 7 April 2024.',
                     'Records: Apr 1, 2024 until Apr 7, 2024.', 'Records: 2024-04-01–2024-04-07.'):
            with self.subTest(text=text):
                original = source([text]); before = copy.deepcopy(original)
                parsed = self.extract(original)['stated_periods']
                self.assertEqual(len(parsed),1); self.assertEqual(parsed[0]['period'],PERIOD)
                self.assertIn(parsed[0]['citations'][0]['quote'],text)
                self.assertEqual(parsed[0]['citations'][0]['passage_id'],'d-1')
                self.assertEqual(original,before)

    def test_ep02_invalid_conflicting_isolated_and_filename_dates_stay_unknown(self):
        for text in ('2024-02-30 to 2024-04-07', '2024-04-07 to 2024-04-01', 'Recorded on 2024-04-01.',
                     'No period supplied.', '2024-04-01 to 2024-04-07. Revised: 2024-04-02 to 2024-04-06.'):
            with self.subTest(text=text):
                self.assertEqual(self.extract(source([text]))['stated_periods'],[])
        repeated = self.extract(source(['2024-04-01 to 2024-04-07. Same: 2024-04-01 through 2024-04-07.']))
        self.assertEqual(len(repeated['stated_periods']),1)
        self.assertEqual(self.extract(source(['2024-04-01 to 2024-04-07'],kind='policy'))['stated_periods'],[])

    def test_ep03_csv_uses_explicit_columns_and_preserves_header_and_record(self):
        parsed = self.extract(source(['period_start,period_end,activity', '2024-04-01,2024-04-07,access reviewed',
                                     '2024-04-10,2024-04-12,access reviewed'],format='csv'))
        self.assertEqual([v['period'] for v in parsed['stated_periods']], [PERIOD,{'start':'2024-04-10','end':'2024-04-12'}])
        self.assertEqual([c['passage_id'] for c in parsed['stated_periods'][0]['citations']],['d-1','d-2'])
        for texts in (['start,end,activity','2024-04-01,2024-04-07,access'],
                      ['period_start,evidence_period_start,period_end','2024-04-01,2024-04-02,2024-04-07'],
                      ['period_start,period_end,activity','2024-04-01,2024-04-07'],
                      ['period_start,period_end,activity','2024-04-07,2024-04-01,access']):
            self.assertEqual(self.extract(source(texts,format='csv'))['stated_periods'],[])

    def test_ep04_passage_period_filters_and_csv_grounding_fit_context_allowance(self):
        dated = self.extract(source(['2024-04-01 to 2024-04-07: access records.',
            '2024-05-01 to 2024-05-07: access records.', 'Access records with unknown period.']))
        result = ranked_context([dated],{'source':'1'},query='access',kinds={'evidence'},assessment_date='2024-04-08',period=PERIOD)
        self.assertEqual(set(result['selected_passage_ids']),{'d-1','d-3'})
        self.assertEqual(result['unknown_period_version_ids'],['d'])
        csv = self.extract(source(['period_start,period_end,activity','2024-04-01,2024-04-07,access reviewed'],format='csv'))
        result = ranked_context([csv],{'source':'1'},query='access',kinds={'evidence'},assessment_date='2024-04-08',max_passages=2)
        self.assertEqual(set(result['selected_passage_ids']),{'d-1','d-2'})
        smaller = ranked_context([csv],{'source':'1'},query='access',kinds={'evidence'},assessment_date='2024-04-08',max_passages=1)
        self.assertNotIn('d-2',smaller['selected_passage_ids'])


class PeriodIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.base = admission.AdmissionTests('runTest'); self.base.setUp()
        self.addCleanup(self.base.doCleanups)
        for key in ('owner','case','store','service','selection','flow','custom','regulation'):
            setattr(self,key,getattr(self.base,key))
        self.evidence = self.upload(b'FICTIONAL DATA ONLY\n2024-04-01 to 2024-04-07: Access records were reviewed.\n')

    def upload(self, data, *, filename='dated-records.txt', source_id=None):
        headers = {'X-Filename':filename,'X-Document-Kind':'evidence','X-Synthetic':'true'}
        if source_id: headers['X-Source-Id'] = source_id
        response = self.flow.call('POST',self.flow.sources,content=data,headers=headers)
        self.assertEqual(response.status_code,201,response.text)
        return response.json()

    def admit(self, evidence=None):
        evidence = evidence or self.evidence
        request = StartAssessment.model_validate(self.base.request.model_dump() | {
            'selected_versions':self.base.request.selected_versions | {evidence['document']['source_id']:evidence['document']['version']},
            'selected_obligations':self.base.obligations[:1],'idempotency_key':uuid.uuid4().hex})
        run = self.selection.admit(self.owner,self.case,request)
        snapshot = self.store.get(self.owner,self.case,'snapshot',run['snapshot_id'])
        return run,snapshot

    def model(self,run,snapshot, *, evidence=None, passage=None, period=PERIOD, status='supported'):
        evidence = evidence or self.evidence
        sources = self.service._sources(self.owner,self.case,snapshot)
        regulatory = next(s for s in sources if s['document']['kind']=='regulation')
        lookup = {p['passage_id']:p for p in regulatory['passages']}
        obligation_id = snapshot['selected_obligations'][0]
        cite = lambda p: {k:p[k] for k in ('document_version_id','passage_id','location')} | {'quote':p['text']}
        obligation = {'obligation_id':obligation_id, 'requirement':lookup[regulatory['obligation_scopes'][obligation_id][-1]]['text'],
            'conditions':[], 'exceptions':[], 'applicability':None,
            'citations':[cite(lookup[p]) for p in regulatory['obligation_scopes'][obligation_id]]}
        control = {'control_id':'C','statement':self.custom['passages'][0]['text'],'purpose':None,'owner':None,'frequency':None,
            'citations':[cite(self.custom['passages'][0])]}
        citations = obligation['citations'] + control['citations']
        if period is not None: citations += [cite(passage or evidence['passages'][1])]
        finding = {'finding_id':'controlled-finding','snapshot_id':snapshot['snapshot_id'],'obligation_id':obligation_id,
            'control_ids':['C'],'status':status,'evidence_condition':'sufficient' if status=='supported' else 'missing',
            'gap_kind':None if status=='supported' else 'evidence', 'rationale':'Controlled grounding check only.',
            'remedy':'Examine the original records.', 'citations':citations,
            'claims':[{'obligation_element':obligation['requirement'],'reason':'Controlled date-grounding check.',
                'operational':period is not None,'evidence_period':period,'citations':citations,
                'examined_exceptions':[],'conflicting_evidence':[]}]}
        common = {'snapshot_id':snapshot['snapshot_id'],'document_version_ids':list(snapshot['selected_document_ids'].values())}
        responses = [json.dumps(common | {'action':'retrieve_obligations','obligations':[obligation]}),
            json.dumps(common | {'action':'find_controls','controls':[control]}),
            json.dumps(common | {'action':'propose_findings','findings':[finding]})]
        class DeclaredLiveStub(ControlledModel):
            def __init__(self): super().__init__(responses); self.prompts = []
            def dispatch(self,*args,**kwargs):
                self.prompts.append(json.loads(args[5]['prompt']))
                self.system = args[5]['system']
                reply = super().dispatch(*args,**kwargs)
                return ModelReply.model_validate(reply.model_dump() | {'label':'Live'})
        return DeclaredLiveStub()

    def execute(self,run,model):
        return AssessmentPipeline(self.service,model).run(self.owner,self.case,run['job_id'])

    def test_ep05_actual_selected_upload_processes_grounded_period_without_extra_inference(self):
        run,snapshot = self.admit()
        self.assertEqual(snapshot['prompt_version'],PERIOD_PROMPT)
        model = self.model(run,snapshot); result = self.execute(run,model)
        self.assertEqual(result['state'],'completed'); self.assertEqual(model.dispatches,3)
        viewed = self.service.read(self.owner,self.case,run['job_id'])
        self.assertEqual(viewed['findings'][0]['claims'][0]['evidence_period'],PERIOD)
        self.assertTrue(all(a['versions']['schema_version']=='vs5-selection-period-v1' for a in viewed['trace']['attempts']))
        self.assertTrue(all(a['versions']['extraction']=='vs2-period-v1' for a in viewed['trace']['attempts']))
        source = self.service.source(self.owner,self.case,run['job_id'],self.evidence['document']['document_version_id'])
        self.assertEqual(source['stated_periods'][0]['period'],PERIOD)
        csv = self.upload(b'period_start,period_end,activity\n2024-04-01,2024-04-07,FICTIONAL DATA ONLY access records reviewed\n',filename='dated-records.csv')
        csv_run,csv_snapshot = self.admit(csv)
        csv_model = self.model(csv_run,csv_snapshot,evidence=csv)
        self.assertEqual(self.execute(csv_run,csv_model)['state'],'completed')
        self.assertEqual(csv_model.dispatches,3)

    def test_ep06_uncited_or_unknown_period_does_not_support_claim(self):
        for text, index in ((b'FICTIONAL DATA ONLY\nAccess records with no dates.\n',1),
                            (b'FICTIONAL DATA ONLY\n2024-04-01 to 2024-04-07: Access records were reviewed.\nUndated unrelated record.\n',2)):
            evidence = self.upload(text); run,snapshot = self.admit(evidence)
            model = self.model(run,snapshot,evidence=evidence,passage=evidence['passages'][index])
            result = self.execute(run,model)
            self.assertEqual(result['state'],'failed')
            self.assertEqual(self.service.read(self.owner,self.case,run['job_id'])['findings'],[])

    def test_ep07_prior_protocol_and_source_records_remain_unchanged(self):
        run,snapshot = self.admit()
        before = self.store.get(self.owner,self.case,'document',self.evidence['document']['document_version_id'])
        old = Snapshot.model_validate(snapshot | {'snapshot_id':uuid.uuid4().hex,'prompt_version':'assessment-vs5-selected-v1'})
        self.store.save_snapshot(self.owner,old)
        legacy = self.service.reviews.admit(self.owner,self.case,uuid.uuid4().hex,old.snapshot_id,'synthetic_live')
        self.assertNotIn('stated_periods',self.service.source(self.owner,self.case,legacy['job_id'],self.evidence['document']['document_version_id']))
        legacy_model = self.model(legacy,old.model_dump(mode='json'),period=None,status='needs_review')
        self.assertEqual(self.execute(legacy,legacy_model)['state'],'completed')
        self.assertNotIn('Stated evidence periods',legacy_model.system)
        self.service.source(self.owner,self.case,run['job_id'],self.evidence['document']['document_version_id'])
        self.assertEqual(self.store.get(self.owner,self.case,'document',self.evidence['document']['document_version_id']),before)
        with patch('regulatory_agent.assessment_worker.supervise') as worker:
            self.service.run_selected(self.owner,self.case,run['job_id']); self.service.run_selected(self.owner,self.case,legacy['job_id'])
            self.assertEqual(worker.call_count,2)
        with self.assertRaises(ValidationError): Snapshot.model_validate(snapshot | {'prompt_version':PERIOD_PROMPT,'selected_document_ids':{}})

    def test_ep08_corrupted_source_copy_cannot_supply_inspection_dates(self):
        run,_ = self.admit(); identity = self.evidence['document']['document_version_id']
        corrupted = copy.deepcopy(self.evidence)
        corrupted['passages'][1]['text'] = '2020-01-01 to 2020-12-31: invented source text.'
        with self.store.transaction() as db:
            db.execute("UPDATE records SET body=? WHERE case_id=? AND kind='document' AND id=?",(json.dumps(corrupted),self.case,identity))
        with self.assertRaises(ContractError): self.service.source(self.owner,self.case,run['job_id'],identity)

    def test_ep09_selected_period_export_survives_upload_replacement(self):
        run,snapshot = self.admit(); identity = self.evidence['document']['document_version_id']
        self.upload(b'FICTIONAL DATA ONLY\n2024-04-10 to 2024-04-20: Changed records.\n',source_id=self.evidence['document']['source_id'])
        source = self.service.source(self.owner,self.case,run['job_id'],identity)
        self.assertEqual(source['stated_periods'][0]['period'],PERIOD)
        report = json.loads(self.service.export(self.owner,self.case,run['job_id'],'json'))
        evidence = next(s for s in report['sources'] if s['document']['document_version_id']==identity)
        self.assertEqual(evidence['stated_periods'][0]['period'],PERIOD)
        self.assertEqual(report['snapshot']['selected_versions'],snapshot['selected_versions'])

    def test_ep10_only_context_period_metadata_reaches_model(self):
        evidence = self.upload(('FICTIONAL DATA ONLY\n' + '2024-04-01 to 2024-04-07: Access records were reviewed.\n'*120).encode())
        run,snapshot = self.admit(evidence); model = self.model(run,snapshot,evidence=evidence,period=None,status='needs_review')
        result = self.execute(run,model)
        self.assertEqual(result['state'],'completed'); self.assertEqual(model.dispatches,3)
        assessment = model.prompts[-1]; selected = {p['passage_id'] for p in assessment['passages']}
        periods = [v for s in assessment['source_metadata'] for v in s.get('stated_periods',[])]
        self.assertTrue(periods); self.assertLessEqual(len(periods),20)
        self.assertTrue(all(c['passage_id'] in selected for v in periods for c in v['citations']))


if __name__ == '__main__': unittest.main()
