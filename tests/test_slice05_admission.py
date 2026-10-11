"""Historical selection and immutable admission checks. No live model or external source calls."""
import copy
import hashlib
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from pydantic import ValidationError
import test_slice03_assessment as fixtures
from regulatory_agent.assessment_pipeline import AssessmentPipeline
from regulatory_agent.assessments import Assessments
from regulatory_agent.cases import CaseService, SQLiteCases
from regulatory_agent.contracts import ContractError, ModelReply, Snapshot, StartAssessment
from regulatory_agent.documents import Documents
from regulatory_agent.local import ControlledModel, Store, validated_action


class AdmissionTests(unittest.TestCase):
    def setUp(self):
        from regulatory_agent.assessment_selection import AssessmentSelection
        self.flow = fixtures.AssessmentSliceTests('runTest'); self.flow.setUp()
        self.addCleanup(self.flow.tearDown)
        self.owner, self.case = 'operator-a', self.flow.case
        self.store = Store(self.flow.path)
        cases = CaseService(SQLiteCases(self.store))
        self.service = Assessments(cases, Documents(cases))
        self.selection = AssessmentSelection(self.service)
        response = self.flow.call('POST', self.flow.sources, content=b'Fictional policy. Review access monthly.\n',
            headers={'X-Filename':'custom-policy.txt', 'X-Document-Kind':'policy', 'X-Synthetic':'true'})
        self.assertEqual(response.status_code, 201)
        self.custom = response.json()
        self.catalog = self.selection.catalog(self.owner, self.case)
        self.regulation = next(s for s in self.catalog['sources'] if s['document']['kind'] == 'regulation')
        self.obligations = [o['obligation_id'] for o in self.catalog['obligations']][:2]
        self.request = StartAssessment(selected_versions={self.regulation['document']['source_id']:self.regulation['document']['version'],
            self.custom['document']['source_id']:self.custom['document']['version']}, selected_obligations=self.obligations,
            assessment_date='2024-04-08', mode='historical', idempotency_key='selected-request')

    def admit(self, request=None):
        return self.selection.admit(self.owner, self.case, request or self.request)

    def test_a01_catalog_lists_owned_sources_and_explicit_limits(self):
        catalog = self.flow.call('GET', f'/api/cases/{self.case}/assessment-selection')
        self.assertEqual(catalog.status_code, 200, catalog.text)
        value = catalog.json()
        self.assertEqual(value['freshness'], 'unverified')
        self.assertFalse(value['current_available'])
        self.assertEqual(value['coverage'], 'saved historical excerpts')
        self.assertEqual(value['data_mode'], 'synthetic_live')
        self.assertTrue(value['obligations'])
        self.assertNotIn('SIM-ACCESS', {s['document']['source_id'] for s in value['sources']})
        self.assertIn(self.custom['document']['document_version_id'], {s['document']['document_version_id'] for s in value['sources']})

    def test_a02_multiple_clauses_and_arbitrary_fictional_policy_are_admitted(self):
        run = self.admit()
        snapshot = self.store.get(self.owner, self.case, 'snapshot', run['snapshot_id'])
        self.assertEqual(snapshot['selected_obligations'], self.obligations)
        self.assertEqual(snapshot['selected_versions'], self.request.selected_versions)
        self.assertEqual(run['data_mode'], 'synthetic_live')
        self.assertEqual(snapshot['prompt_version'], 'assessment-vs5-selected-period-v1')
        self.assertEqual(self.store.read_job(self.owner, self.case, run['job_id'])['label'], 'Live')
        sources = self.service._sources(self.owner, self.case, snapshot)
        self.assertEqual(len(sources), 2)
        scopes = next(s for s in sources if s['document']['kind']=='regulation')['obligation_scopes']
        self.assertTrue(all(len(scopes[o]) >= 4 for o in self.obligations))
        self.assertTrue(all('evidence_period' not in s for s in sources if s['document']['kind']!='regulation'))

    def test_a03_explicit_artifacts_do_not_rewrite_legacy_records(self):
        legacy = self.flow.start()
        old = self.store.get(self.owner, self.case, 'document', 'RBI-IT-2023:2023-11-07')
        run = self.admit()
        snapshot = self.store.get(self.owner, self.case, 'snapshot', run['snapshot_id'])
        self.assertEqual(set(snapshot['selected_document_ids']), set(snapshot['selected_versions']))
        self.assertEqual(self.store.get(self.owner, self.case, 'document', 'RBI-IT-2023:2023-11-07'), old)
        self.assertEqual(self.flow.result(legacy)['job']['state'], 'completed')
        self.assertNotEqual(snapshot['selected_document_ids']['RBI-IT-2023'], 'RBI-IT-2023:2023-11-07')

    def test_a04_invalid_ownership_scope_versions_and_current_mode_start_no_run(self):
        with self.assertRaises(Exception):
            self.selection.catalog('other-owner', self.case)
        before = self.service.list(self.owner, self.case)
        for changes in ({'mode':'current'}, {'selected_obligations':['outside']},
            {'selected_versions':self.request.selected_versions | {'outside':'1'}}, {'assessment_date':'2023-01-01'}):
            bad = StartAssessment.model_validate(self.request.model_dump() | changes)
            with self.assertRaises(Exception): self.admit(bad)
        self.assertEqual(self.service.list(self.owner, self.case), before)
        other = self.flow.application('other-owner')
        response = self.flow.call('POST', f'{self.flow.url}/selected', app=other, json=self.request.model_dump())
        self.assertEqual(response.status_code, 404)

    def test_a05_retry_after_replacement_keeps_snapshot_and_conflicts_on_changed_request(self):
        first = self.admit()
        replacement = self.flow.upload(b'Fictional replacement policy.\n', self.custom['document']['source_id'])
        self.assertEqual(replacement.status_code, 201)
        self.assertEqual(self.admit(), first)
        snapshot = self.store.get(self.owner, self.case, 'snapshot', first['snapshot_id'])
        self.assertEqual(snapshot['selected_document_ids'][self.custom['document']['source_id']], self.custom['document']['document_version_id'])
        changed = StartAssessment.model_validate(self.request.model_dump() | {'assessment_date':'2024-04-09'})
        with self.assertRaises(Exception): self.admit(changed)

    def test_a06_citation_reads_and_export_use_selected_artifacts(self):
        run = self.admit(); snapshot = self.store.get(self.owner, self.case, 'snapshot', run['snapshot_id'])
        sources = self.service._sources(self.owner, self.case, snapshot)
        source = next(s for s in sources if s['document']['kind']=='regulation'); passage = source['passages'][3]
        citation = {key:passage[key] for key in ('document_version_id','passage_id','location')} | {'quote':passage['text']}
        action = {'action':'retrieve_obligations', 'snapshot_id':snapshot['snapshot_id'],
            'document_version_ids':list(snapshot['selected_document_ids'].values()),
            'obligations':[{'obligation_id':self.obligations[0],'requirement':passage['text'], 'conditions':[], 'exceptions':[],
                'applicability':None,'citations':[citation]}]}
        validated_action(json.dumps(action), self.store, self.owner, self.case, run['job_id'])
        lookup_action = action | {'document_version_ids':[f'{s}:{v}' for s,v in snapshot['selected_versions'].items()]}
        with self.assertRaisesRegex(ContractError, 'model_scope_denied'):
            validated_action(json.dumps(lookup_action), self.store, self.owner, self.case, run['job_id'])
        viewed = self.service.source(self.owner, self.case, run['job_id'], source['document']['document_version_id'])
        self.assertEqual(viewed, source)
        exported = json.loads(self.service.export(self.owner, self.case, run['job_id'], 'json'))
        self.assertEqual(exported['snapshot']['selected_document_ids'], snapshot['selected_document_ids'])

    def test_a07_archived_public_and_original_bank_corruption_prevent_inference(self):
        for public in (True, False):
            run = self.admit(StartAssessment.model_validate(self.request.model_dump() | {'idempotency_key':f'integrity-{public}'}))
            snapshot = self.store.get(self.owner, self.case, 'snapshot', run['snapshot_id'])
            if public:
                source = next(s for s in self.service._sources(self.owner, self.case, snapshot) if s['document']['kind']=='regulation')
                archive = self.selection.blobs.path(self.owner, self.case, source['original_blob'])
                original = archive.read_bytes(); archive.write_bytes(b'altered public source')
                self.addCleanup(archive.write_bytes, original)
            else:
                with self.store.transaction() as db:
                    db.execute('UPDATE documents SET original=? WHERE id=?', (b'altered bank source', self.custom['document']['document_version_id']))
            model = ControlledModel([])
            result = AssessmentPipeline(self.service, model).run(self.owner, self.case, run['job_id'])
            self.assertEqual(result['state'], 'failed'); self.assertEqual(model.dispatches, 0)
            if public: archive.write_bytes(original)

    def test_a08_http_admission_dispatch_and_resume_keep_server_configuration(self):
        with patch.object(Assessments, 'run_selected') as worker:
            response = self.flow.call('POST', f'{self.flow.url}/selected', json=self.request.model_dump())
        self.assertEqual(response.status_code, 202, response.text)
        run = response.json(); worker.assert_called_once_with(self.owner, self.case, run['job_id'])
        with patch('regulatory_agent.assessment_worker.supervise') as supervisor:
            self.service.run_selected(self.owner, self.case, run['job_id'])
        self.assertEqual(supervisor.call_args.args[:4], (self.store, self.owner, self.case, run['job_id']))
        self.assertEqual(supervisor.call_args.kwargs['args'][0], str(self.store.path))
        with patch.object(Assessments, 'run_selected') as worker, patch.object(Assessments, 'run') as legacy:
            response = self.flow.call('POST', f"{self.flow.url}/{run['job_id']}/resume")
        self.assertEqual(response.status_code, 202, response.text)
        worker.assert_called_once(); legacy.assert_not_called()
        forged = self.request.model_dump() | {'model_version':'other', 'profile':'other', 'data_mode':'controlled_simulation'}
        self.assertEqual(self.flow.call('POST', f'{self.flow.url}/selected', json=forged).status_code, 422)

    def test_a09_original_download_preserves_bytes_and_denies_outside_versions(self):
        run = self.admit(); snapshot = self.store.get(self.owner, self.case, 'snapshot', run['snapshot_id'])
        identity = snapshot['selected_document_ids']['RBI-IT-2023']
        url = f"{self.flow.url}/{run['job_id']}/sources/{identity}/original"
        response = self.flow.call('GET', url)
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(hashlib.sha256(response.content).hexdigest(), self.regulation['document']['sha256'])
        self.assertEqual(response.headers['cache-control'], 'no-store')
        self.assertIn('attachment', response.headers['content-disposition'])
        self.assertEqual(self.flow.call('GET', url, app=self.flow.application('other-owner')).status_code, 404)
        self.assertEqual(self.flow.call('GET', url.replace(identity, 'outside')).status_code, 404)

    def test_a10_invalid_artifact_binding_and_oversized_context_fail_closed(self):
        run = self.admit(); snapshot = self.store.get(self.owner, self.case, 'snapshot', run['snapshot_id'])
        with self.assertRaises(ValidationError):
            Snapshot.model_validate(snapshot | {'selected_document_ids':{'outside':'artifact'}})
        missing = snapshot | {'selected_document_ids':{}}
        with self.assertRaises(ValidationError): Snapshot.model_validate(missing)
        with self.assertRaises(ContractError): self.service._sources(self.owner,self.case,missing)
        forged = copy.deepcopy(snapshot)
        forged['selected_document_ids']['RBI-IT-2023'] = self.custom['document']['document_version_id']
        with self.assertRaises(ContractError): self.service._sources(self.owner, self.case, forged)
        sources = copy.deepcopy(self.catalog['sources'])
        reg = next(s for s in sources if s['document']['kind']=='regulation')
        reg['passages'][0]['text'] = 'large source ' * 6000
        with patch.object(self.selection, '_catalog_sources', return_value=sources):
            bad = StartAssessment.model_validate(self.request.model_dump() | {'idempotency_key':'oversized'})
            with self.assertRaisesRegex(ContractError, 'mandatory_regulatory_context_limit'): self.admit(bad)

    def test_a11_admitted_snapshot_runs_through_full_selected_pipeline(self):
        run = self.admit(); snapshot = self.store.get(self.owner, self.case, 'snapshot', run['snapshot_id'])
        sources = self.service._sources(self.owner, self.case, snapshot)
        reg = next(s for s in sources if s['document']['kind']=='regulation')
        bank = next(s for s in sources if s['document']['kind']=='policy')
        passages = {p['passage_id']:p for p in reg['passages']}
        def cite(p):
            return {key:p[key] for key in ('document_version_id','passage_id','location')} | {'quote':p['text']}
        base = {'snapshot_id':snapshot['snapshot_id'], 'document_version_ids':list(snapshot['selected_document_ids'].values())}
        obligations = [{'obligation_id':o, 'requirement':passages[reg['obligation_scopes'][o][-1]]['text'],
            'conditions':[], 'exceptions':[], 'applicability':None,
            'citations':[cite(passages[p]) for p in reg['obligation_scopes'][o]]} for o in self.obligations]
        controls = [{'control_id':'C-1','statement':bank['passages'][0]['text'], 'purpose':None,'owner':None,'frequency':None,
            'citations':[cite(bank['passages'][0])]}]
        responses = [json.dumps(base | {'action':'retrieve_obligations','obligations':obligations}),
                     json.dumps(base | {'action':'find_controls','controls':controls})]
        for o in obligations:
            citations = o['citations'] + controls[0]['citations']
            finding = {'finding_id':'controlled-id','snapshot_id':snapshot['snapshot_id'],'obligation_id':o['obligation_id'],
                'control_ids':['C-1'],'status':'needs_review','evidence_condition':'missing','gap_kind':'evidence',
                'citations':citations,'rationale':'Controlled integration check. No model quality claim.',
                'remedy':'Request operational evidence.', 'claims':[{'obligation_element':o['requirement'],
                    'citations':citations, 'reason':'Controlled source-reference check.', 'operational':False,
                    'evidence_period':None, 'examined_exceptions':[], 'conflicting_evidence':[]}]}
            responses.append(json.dumps(base | {'action':'propose_findings','findings':[finding]}))
        class DeclaredLiveStub(ControlledModel):
            def dispatch(self, *args, **kwargs):
                reply = super().dispatch(*args, **kwargs)
                return ModelReply.model_validate(reply.model_dump() | {'label':'Live'})
        result = AssessmentPipeline(self.service, DeclaredLiveStub(responses)).run(self.owner, self.case, run['job_id'])
        self.assertEqual(result['state'],'completed')
        self.assertEqual(result['model_calls'],4)
        viewed = self.service.read(self.owner,self.case,run['job_id'])
        self.assertEqual({f['obligation_id'] for f in viewed['findings']},set(self.obligations))
        self.assertEqual(viewed['data_mode'],'synthetic_live')
        self.assertEqual(len(viewed['obligations']),2)
        self.assertEqual(len(viewed['controls']),1)
        self.assertTrue(all(t['versions']['schema_version']=='vs5-selection-period-v1' for t in viewed['trace']['attempts']))
        exported = json.loads(self.service.export(self.owner,self.case,run['job_id'],'json'))
        self.assertEqual(len(exported['findings']),2)

    def test_a12_corrupt_archive_cannot_be_inspected_or_exported(self):
        run = self.admit(); snapshot = self.store.get(self.owner,self.case,'snapshot',run['snapshot_id'])
        source = next(s for s in self.service._sources(self.owner,self.case,snapshot) if s['document']['kind']=='regulation')
        path = self.selection.blobs.path(self.owner,self.case,source['original_blob'])
        original = path.read_bytes(); path.write_bytes(b'corrupt public archive')
        self.addCleanup(path.write_bytes,original)
        with self.assertRaises(ContractError):
            self.service.source(self.owner,self.case,run['job_id'],source['document']['document_version_id'])
        with self.assertRaises(ContractError):
            self.service.export(self.owner,self.case,run['job_id'],'json')


if __name__ == '__main__': unittest.main()
