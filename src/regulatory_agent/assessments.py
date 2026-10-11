"""One controlled historical example using the existing durable job and review services."""
from datetime import datetime, timezone
import hashlib
import html
import json
import os
from pathlib import Path
import re
import uuid

from .cases import CaseError, not_found
from .contracts import Citation, ContractError, Control, Finding, Obligation, PERIOD_PROMPT, ReviewDecision, ReviewItem, SELECTED_PROMPT, SELECTED_PROMPTS, Snapshot, StartAssessment
from .local import ControlledModel, LocalRunner, encoded
from .reviews import Reviews, counts, instant
from .telemetry import AttemptTimer, StageAttempt, VersionMetadata

ROOT = Path(__file__).resolve().parents[2]
MODEL = 'in.openai.gpt-5.6-luna'
REGULATION = 'RBI-IT-2023'
VERSION = '2023-11-07'
REG_ID = f'{REGULATION}:{VERSION}'
OBLIGATION = 'RBI-IT-19b'
PROMPT = 'controlled-vs3-v1'
SIMULATION = 'SIM-ACCESS'
SIM_OBLIGATION = 'SIM-ACCESS-1'
SIM_VERSIONS = {'v1', 'v2-added', 'v2-replaced', 'v2-cosmetic'}


def invalid(code='assessment_scope_invalid', status=422):
    return CaseError(status, code, 'This controlled assessment request is unavailable.',
                     'Use the fictional policy fixture and the historical clause 19(b) example.')


class Assessments:
    def __init__(self, cases, documents):
        self.cases, self.documents = cases, documents
        self.store = documents.store
        self.reviews = Reviews(self.store)

    def _record(self, owner, case, kind, identity):
        self.cases.read(owner, case)
        try:
            return self.store.get(owner, case, kind, identity)
        except ContractError:
            raise not_found() from None

    def start(self, owner, case, request):
        profile = self.cases.read(owner, case)
        identity = uuid.uuid5(uuid.NAMESPACE_URL, f'vs3:{owner}:{case}:{request.idempotency_key}').hex
        with self.store.transaction() as db:
            self.store.authorize(owner, case, db)
            old = db.execute("SELECT body FROM records WHERE case_id=? AND kind='run' AND id=?", (case, identity)).fetchone()
        if old:
            saved = json.loads(old[0])
            snapshot = self.store.get(owner, case, 'snapshot', saved['snapshot_id'])
            if any(snapshot[field] != getattr(request, field) for field in ('selected_versions', 'selected_obligations', 'assessment_date', 'mode')):
                raise invalid('idempotency_conflict', 409)
            return saved
        if request.mode == 'current':
            raise CaseError(503, 'freshness_unverified', 'Current regulatory verification is unavailable.',
                            'Use the labeled historical controlled example. Current assessments are disabled.')
        simulated = SIMULATION in request.selected_versions
        regulation = SIMULATION if simulated else REGULATION
        version = request.selected_versions.get(regulation)
        bank = {name: value for name, value in request.selected_versions.items() if name not in {REGULATION, SIMULATION}}
        if len(request.selected_versions) != 2 or len(bank) != 1 or \
                request.selected_obligations != [SIM_OBLIGATION if simulated else OBLIGATION] or \
                request.assessment_date != ('2024-05-08' if simulated else '2024-04-08') or \
                version not in (SIM_VERSIONS if simulated else {VERSION}):
            raise invalid()
        sources = self.documents.list(owner, case)['sources']
        name, version = next(iter(bank.items()))
        selected = next((s for s in sources if s['document']['source_id'] == name and s['document']['version'] == version), None)
        if selected is None:
            raise not_found()
        document = self.documents.read(owner, case, selected['document']['document_version_id'])
        expected = hashlib.sha256((ROOT / 'data/fixtures/slice-02-policy.txt').read_bytes()).hexdigest()
        if document['document']['kind'] != 'policy' or document['document']['sha256'] != expected:
            raise invalid('controlled_fixture_required')
        regulatory = self._regulation(case, regulation, request.selected_versions[regulation])
        self.store.put(owner, case, 'document', regulatory['document']['document_version_id'], regulatory)
        self.store.put(owner, case, 'document', f'{name}:{version}', document)
        snapshot = Snapshot(snapshot_id=identity, case_id=case, bank_profile=profile.bank_profile,
            selected_versions=request.selected_versions, selected_obligations=request.selected_obligations,
            assessment_date=request.assessment_date, mode=request.mode, prompt_version='controlled-vs4-v1' if simulated else PROMPT,
            model_version=MODEL, synthetic=True)
        try:
            self.store.save_snapshot(owner, snapshot)
        except ContractError:
            raise invalid('idempotency_conflict', 409) from None
        return self.reviews.admit(owner, case, identity, identity, 'controlled_simulation')

    @staticmethod
    def _regulation(case, name, version):
        manifest = next((v for v in json.loads((ROOT / 'data/sources/source-manifest.json').read_text(encoding='utf-8'))['versions']
                         if v['document_id'] == name and v['version_id'] == version), None)
        if manifest is None:
            raise invalid('comparison_pair_invalid')
        identity = f'{name}:{version}'
        if manifest['synthetic']:
            digest = hashlib.sha256(encoded(manifest).encode()).hexdigest()
        else:
            raw = (ROOT / manifest['raw_path']).read_bytes()
            digest = hashlib.sha256(raw).hexdigest()
            if digest != manifest['sha256']:
                raise invalid('historical_source_integrity', 503)
        return {'document': {'document_version_id': identity, 'case_id': case, 'source_id': name,
            'kind': 'regulation', 'version': version, 'sha256': digest, 'synthetic': manifest['synthetic']},
            'filename': manifest['title'], 'format': 'html', 'freshness': 'unverified', 'source_url': manifest['source_url'],
            **({'label': manifest['label'], 'authority': manifest['authority']} if manifest['synthetic'] else {}),
            'publication_date': manifest['publication_date'], 'effective_date': manifest['effective_date'],
            'passages': [{'passage_id': f"{identity}:{p['passage_id']}", 'document_version_id': identity,
                          'location': p['locator'], 'text': p['text']} for p in manifest['passages']]}

    def list(self, owner, case):
        self.cases.read(owner, case)
        with self.store.transaction() as db:
            self.store.authorize(owner, case, db)
            return {'runs': self.reviews._records(db, case, 'run')}

    def comparisons(self, owner, case):
        self.cases.read(owner, case)
        with self.store.transaction() as db:
            self.store.authorize(owner, case, db)
            return {'comparisons': self.reviews._records(db, case, 'comparison')}

    def comparison(self, owner, case, identity):
        return self._record(owner, case, 'comparison', identity)

    def compare(self, owner, case, request):
        self.cases.read(owner, case)
        identity = uuid.uuid5(uuid.NAMESPACE_URL, f'vs4:{owner}:{case}:{request.idempotency_key}').hex
        for old in self.comparisons(owner, case)['comparisons']:
            if old['comparison_id'] == identity:
                if old['request'] != request.model_dump():
                    raise invalid('idempotency_conflict', 409)
                return old
        snapshot = self._record(owner, case, 'snapshot', request.snapshot_id)
        if snapshot['mode'] != 'historical' or snapshot['selected_versions'].get(SIMULATION) != 'v1' or \
                request.older_version_id != 'SIM-ACCESS:v1' or \
                request.newer_version_id not in {f'{SIMULATION}:{v}' for v in SIM_VERSIONS - {'v1'}}:
            raise invalid('comparison_pair_invalid')
        baseline = self._record(owner, case, 'run', request.snapshot_id)
        if self.store.read_job(owner, case, baseline['job_id'])['state'] != 'completed':
            raise invalid('comparison_baseline_unfinished', 409)
        older = self.store.get(owner, case, 'document', request.older_version_id)
        version = request.newer_version_id.split(':', 1)[1]
        newer = self._regulation(case, SIMULATION, version)
        # ponytail: classifications for three labeled fixtures only; live comparisons need validated interpretation.
        changed = version == 'v2-added'
        new_job = None
        if changed:
            new_job = self.start(owner, case, StartAssessment(selected_versions=snapshot['selected_versions'] | {SIMULATION: version},
                selected_obligations=snapshot['selected_obligations'], assessment_date=snapshot['assessment_date'],
                mode='historical', idempotency_key=f'comparison:{identity}'))['job_id']
        result = {'comparison_id': identity, 'case_id': case, 'request': request.model_dump(),
            'data_mode': 'controlled_simulation', 'label': 'Synthetic regulatory simulation',
            'older_source': older, 'newer_source': newer,
            'change_kind': {'v2-added': 'added_requirement', 'v2-replaced': 'wording_only', 'v2-cosmetic': 'appearance_only'}[version],
            'obligation_changed': changed, 'affected_obligation_ids': [SIM_OBLIGATION] if changed else [],
            'affected_control_ids': ['ACCESS-01'] if changed else [],
            'metadata_changes': {field: {'older': older[field], 'newer': newer[field]} for field in ('publication_date', 'effective_date')
                                 if older[field] != newer[field]},
            'baseline_job_id': baseline['job_id'], 'new_job_id': new_job}
        try:
            with self.store.transaction() as db:
                self.store.authorize(owner, case, db)
                saved = db.execute("SELECT body FROM records WHERE case_id=? AND kind='comparison' AND id=?", (case, identity)).fetchone()
                if saved:
                    value = json.loads(saved[0])
                    if value['request'] != request.model_dump():
                        raise invalid('idempotency_conflict', 409)
                    return value
                self.reviews._insert(db, case, 'comparison', identity, result)
        except ContractError:
            raise CaseError(503, 'comparison_save_unconfirmed', 'The comparison save could not be confirmed.',
                            'Retry the same version pair and request key. Earlier records are unchanged.') from None
        return result

    def _run(self, owner, case, job_id):
        self.cases.read(owner, case)
        with self.store.transaction() as db:
            self.store.authorize(owner, case, db)
            row = db.execute("SELECT body FROM records WHERE case_id=? AND kind='run' AND json_extract(body,'$.job_id')=?",
                             (case, job_id)).fetchone()
        if row is None:
            raise not_found()
        run = json.loads(row[0])
        return run, self.store.get(owner, case, 'snapshot', run['snapshot_id'])

    def _bank_source(self, owner, case, version_id):
        return self.documents.read(owner,case,version_id)

    def _sources(self, owner, case, snapshot):
        sources = self.store.sources(owner, case, snapshot)
        for source in sources:
            if source['document']['kind']=='regulation':
                if snapshot.get('selected_document_ids'): self._public_original(owner, case, source)
            else:
                original = self._bank_source(owner, case, source['document']['document_version_id'])
                if any(original[key] != source[key] for key in ('document', 'passages')):
                    raise ContractError('source_integrity_failure')
        if snapshot['prompt_version'] == PERIOD_PROMPT:
            from .evidence_periods import with_periods
            return [with_periods(s) for s in sources]
        return sources

    def _public_original(self, owner, case, source):
        if not source.get('original_blob'):
            raise ContractError('source_original_missing')
        from .local import BlobStore
        raw = BlobStore(self.store.path.with_suffix('.sources'), self.store).read(owner, case, source['original_blob'])
        if hashlib.sha256(raw).hexdigest() != source['document']['sha256']:
            raise ContractError('source_integrity_failure')
        return raw

    def run_selected(self, owner, case, job_id):
        from .assessment_worker import bedrock_child, supervise
        run, snapshot = self._run(owner, case, job_id)
        if run['data_mode'] != 'synthetic_live' or snapshot['prompt_version'] not in SELECTED_PROMPTS:
            raise invalid('selected_processing_scope_invalid')
        return supervise(self.store, owner, case, job_id, bedrock_child,
            args=(str(self.store.path), os.environ.get('BEDROCK_PROFILE')))

    def source_original(self, owner, case, job_id, version_id):
        source = self.source(owner, case, job_id, version_id)
        if source['document']['kind'] != 'regulation':
            return self.documents.read(owner, case, version_id, original=True)
        if not source.get('original_blob'):
            raise not_found()
        return self._public_original(owner, case, source), 'historical-regulation.html'

    def source(self, owner, case, job_id, version_id):
        _, snapshot = self._run(owner, case, job_id)
        for source in self._sources(owner, case, snapshot):
            if source['document']['document_version_id'] == version_id:
                if source['document']['kind'] != 'regulation':
                    self.documents.read(owner, case, version_id)
                return source
        raise not_found()

    @staticmethod
    def _citation(passage):
        return Citation(document_version_id=passage['document_version_id'], passage_id=passage['passage_id'],
                        location=passage['location'], quote=passage['text'])

    def _example(self, owner, case, job_id, snapshot):
        sources = self._sources(owner, case, snapshot)
        regulatory = next(s for s in sources if s['document']['kind'] == 'regulation')
        policy = next(s for s in sources if s['document']['kind'] == 'policy')
        references = {p['location']: p for p in regulatory['passages']}
        passage = next(p for p in policy['passages'] if p['text'].startswith('Control ACCESS-01 '))
        if regulatory['document']['source_id'] == SIMULATION:
            rule = regulatory['passages'][0]
            obligation = Obligation(obligation_id=SIM_OBLIGATION, requirement=rule['text'],
                conditions=['Fictional commercial-bank rule for this simulation.'], exceptions=[],
                applicability='Unverified for this fictional bank profile. Synthetic regulatory simulation.', citations=[self._citation(rule)])
            control = Control(control_id='ACCESS-01', statement=passage['text'], purpose='Privileged session oversight',
                owner=None, frequency='Weekly under the fictional policy and simulated rule.', citations=[self._citation(passage)])
            recommendation = 'Request dated privileged-session logs and completed weekly reviews.'
            if regulatory['document']['version'] == 'v2-added':
                recommendation += ' Request evidence that a separate reviewer approved each weekly review.'
            finding = Finding(finding_id=uuid.uuid5(uuid.NAMESPACE_URL, f'{job_id}:{SIM_OBLIGATION}').hex,
                snapshot_id=snapshot['snapshot_id'], obligation_id=SIM_OBLIGATION, control_ids=['ACCESS-01'], status='needs_review',
                evidence_condition='missing', citations=[self._citation(rule), self._citation(passage)],
                rationale='Controlled simulation. The policy states a control. Operational records and applicability have not been verified.',
                remedy=recommendation, gap_kind='evidence')
            return obligation, control, finding
        obligation = Obligation(obligation_id=OBLIGATION, requirement=references['Clause 19(b)']['text'],
            conditions=['Personnel with elevated system access entitlements.', 'Applicability to the listed regulated entities must be established.'],
            exceptions=['Local Area Banks', 'NBFC-Core Investment Companies'], applicability='Unverified for this fictional bank profile.',
            citations=[self._citation(references[key]) for key in ('Clause 19(b)', 'Clause 2(a)(i)', 'Clause 2(b)')])
        control = Control(control_id='ACCESS-01', statement=passage['text'], purpose='Privileged session oversight',
            owner=None, frequency='Weekly under the fictional bank policy.', citations=[self._citation(passage)])
        finding = Finding(finding_id=uuid.uuid5(uuid.NAMESPACE_URL, f'{job_id}:{OBLIGATION}').hex,
            snapshot_id=snapshot['snapshot_id'], obligation_id=OBLIGATION, control_ids=['ACCESS-01'], status='needs_review',
            evidence_condition='missing', citations=[self._citation(references['Clause 19(b)']), self._citation(passage)],
            rationale='Controlled example. The policy states a control, but this example has no verified operational evidence. Applicability and activity records need human review.',
            remedy='Confirm applicability. Request dated session records, supervisor sign-offs, complete activity logs, and completed periodic reviews.', gap_kind='evidence')
        return obligation, control, finding

    def _trace(self, owner, case, run, stage, timer, *, state='succeeded', operation='internal', artifacts=(), original=None, candidates=(), selected=(), error=None):
        event = StageAttempt(event_id=uuid.uuid4().hex, run_id=run['run_id'], job_id=run['job_id'], snapshot_id=run['snapshot_id'],
            stage_id=stage, attempt_id=uuid.uuid4().hex, stage=stage, operation=operation, state=state,
            dispatched=state not in {'skipped', 'not_applicable'}, **timer.finish(),
            versions=VersionMetadata(application='vs5-v1', schema='t2-v1', extraction='vs2-v1', chunking='source-locations-v1',
                retrieval='fixed-example-v1', prompt=run['prompt_version'],
                model_configuration='controlled-response-v1' if run['data_mode']=='controlled_simulation' else 'india-converse-v1'),
            model_id=MODEL if operation == 'model' else None, artifact_ids=tuple(artifacts), original_processing_event_id=original,
            candidate_passage_ids=tuple(candidates), selected_passage_ids=tuple(selected), errors=(error,) if error else ())
        self.reviews.attempt(owner,case,event)

    def run(self, owner, case, job_id):
        run, snapshot = self._run(owner, case, job_id)
        sources = self._sources(owner, case, snapshot)
        passages = [p for s in sources for p in s['passages']]
        obligation, control, example = self._example(owner, case, job_id, snapshot)
        selected = [c.passage_id for c in [*obligation.citations, *control.citations]]

        def stage(name, operation, handler, *, reuse=False):
            def execute(job):
                timer = AttemptTimer()
                try:
                    output = handler(job)
                except Exception:
                    self._trace(owner, case, run, name, timer, state='failed', operation=operation, error='validation_failure' if name == 'validation' else 'tool_failure')
                    raise
                policy = next(s for s in sources if s['document']['kind'] == 'policy')['document']['document_version_id']
                self._trace(owner, case, run, name, timer, operation=operation, state='skipped' if reuse else 'succeeded',
                    artifacts=(policy,) if reuse else (), original=policy if reuse else None,
                    candidates=[p['passage_id'] for p in passages] if name == 'retrieval' else (),
                    selected=selected if name in {'retrieval', 'context_selection'} else ())
                return output
            return execute

        def verify(_job):
            for source in sources:
                if source['document']['kind'] == 'policy':
                    self.documents.read(owner, case, source['document']['document_version_id'])
            return {'freshness': 'unverified', 'mode': 'historical', 'live_verification': False}

        def dispatch(job):
            action = {'action': 'propose_findings', 'snapshot_id': snapshot['snapshot_id'],
                      'document_version_ids': [f'{name}:{version}' for name, version in snapshot['selected_versions'].items()],
                      'passage_ids': selected, 'findings': [example.model_dump()]}
            reply = ControlledModel([encoded(action)]).dispatch(self.store, owner, case, job_id, job['token'], {'controlled': True})
            if reply.action.action != 'propose_findings' or len(reply.action.findings) != 1:
                raise ContractError('invalid_controlled_action')
            return {'finding': reply.action.findings[0].model_dump(), 'label': reply.label}

        def validate(job):
            finding = Finding.model_validate(job['stages']['model_call']['finding'])
            if finding.snapshot_id != snapshot['snapshot_id'] or finding.obligation_id != obligation.obligation_id:
                raise ContractError('finding_scope_denied')
            if finding.status != 'needs_review' or finding.evidence_condition != 'missing' or finding.gap_kind != 'evidence':
                raise ContractError('controlled_evidence_state_invalid')
            if {c.document_version_id for c in finding.citations} != {s['document']['document_version_id'] for s in sources}:
                raise ContractError('required_citation_missing')
            for citation in finding.citations:
                if not any(p['document_version_id'] == citation.document_version_id and p['passage_id'] == citation.passage_id
                           and p['location'] == citation.location and citation.quote in p['text'] for p in passages):
                    raise ContractError('invalid_citation')
            return {'finding': finding.model_dump()}

        def present(job):
            finding = Finding.model_validate(job['stages']['validation']['finding'])
            item = ReviewItem(**finding.model_dump(), run_id=run['run_id'], primary_recommendation=finding.remedy,
                available_at=datetime.now(timezone.utc).isoformat(), model_id=MODEL, prompt_version=snapshot['prompt_version'],
                data_mode='controlled_simulation', source_version_ids=[f'{name}:{version}' for name, version in snapshot['selected_versions'].items()])
            self.reviews.present(owner, case, item, execution_token=job['token'])
            return {'accounted_obligations': [obligation.obligation_id], 'finding_id': item.finding_id}

        # ponytail: one short trusted example; use a separate worker before live model execution.
        return LocalRunner(self.store).run(owner, case, job_id, {
            'source_verification': stage('source_verification', 'internal', verify),
            'extraction': stage('extraction', 'internal', lambda _j: {'saved_source_versions': list(snapshot['selected_versions'])}, reuse=True),
            'retrieval': stage('retrieval', 'retrieval', lambda _j: {'candidate_passage_ids': [p['passage_id'] for p in passages], 'selected_passage_ids': selected}),
            'context_selection': stage('context_selection', 'internal', lambda _j: {'selected_passage_ids': selected}),
            'model_call': stage('model_call', 'model', dispatch),
            'validation': stage('validation', 'internal', validate),
            'persistence': stage('persistence', 'storage', present),
        })

    def _read_records(self, owner, case, run):
        with self.store.transaction() as db:
            self.store.authorize(owner,case,db)
            job=self.store._job(db,owner,case,run['job_id'])
            items=[ReviewItem.model_validate(item) for item in self.reviews._records(db,case,'finding') if item['run_id']==run['run_id']]
            events=[event.model_dump() for item in items for event in self.reviews._history(db,case,item.finding_id)]
            trace=[event for event in self.reviews._records(db,case,'stage_attempt') if event['run_id']==run['run_id']]
        return job,items,events,trace

    def read(self, owner, case, job_id, cutoff=None):
        run, snapshot = self._run(owner, case, job_id)
        try:
            limit = instant(cutoff) if cutoff else None
            if limit is not None and limit.utcoffset() is None:
                raise ValueError()
        except ValueError:
            raise invalid('invalid_cutoff') from None
        job,items,events,trace=self._read_records(owner,case,run)
        limit=limit or datetime.now(timezone.utc)
        eligible = [item for item in items if instant(item.available_at) <= limit]
        events = [event for event in events if instant(event['committed_at']) <= limit]
        trace = [event for event in trace if instant(event['finished_at'] or event['started_at']) <= limit]
        finals = []
        for item in eligible:
            history = [event for event in events if event['finding_id'] == item.finding_id and event['event_kind'] == 'final_review']
            latest = max(history, key=lambda event: event['revision'], default=None)
            finals.append(ReviewDecision.model_validate(latest) if latest else None)
        if snapshot['prompt_version'] in {PROMPT, 'controlled-vs4-v1'}:
            obligation, control, _ = self._example(owner, case, job_id, snapshot)
            obligations, controls = [obligation.model_dump()], [control.model_dump()]
        else:
            obligations = job['stages'].get('obligations', {}).get('obligations', [])
            controls = job['stages'].get('controls', {}).get('controls', [])
        return {'data_mode': run['data_mode'], 'freshness': 'unverified',
            'live_model_calls': 0 if run['data_mode']=='controlled_simulation' else None if any(t['operation']=='model' and
                (t['state']=='unknown' or 'unknown_outcome' in t['errors']) for t in trace)
                else sum(t['operation']=='model' and t['dispatched'] for t in trace), 'cost_usd': None,
            'job': {key: value for key, value in job.items() if key not in {'token', 'stages'}}, 'snapshot': snapshot,
            'obligation': obligations[0] if obligations else None, 'control': controls[0] if controls else None,
            'obligations': obligations, 'controls': controls, 'findings': [item.model_dump() for item in eligible],
            'reviews': sorted(events, key=lambda e: e['revision']),
            'summary': {'metric_definition_version': 'd24-v1', 'cutoff': limit.isoformat(), 'data_mode': run['data_mode'],
                        'run_id': run['run_id'], **counts(eligible, finals)},
            'trace': {'run_id': run['run_id'], 'attempts': trace}}

    def export(self, owner, case, job_id, format, cutoff=None):
        if cutoff:
            try:
                stamp = instant(cutoff)
                if stamp.utcoffset() is None or stamp > datetime.now(timezone.utc):
                    raise ValueError()
            except ValueError:
                raise invalid('invalid_cutoff') from None
        result = self.read(owner, case, job_id, cutoff)
        snapshot = result['snapshot']
        sources = self._sources(owner, case, snapshot)
        for finding in result['findings']:
            citations = finding['citations'] + [citation for claim in finding.get('claims', [])
                for key in ('citations', 'examined_exceptions', 'conflicting_evidence') for citation in claim[key]]
            for citation in citations:
                if not any(source['document']['document_version_id'] == citation['document_version_id']
                        and passage['passage_id'] == citation['passage_id'] and passage['location'] == citation['location']
                        and citation['quote'] in passage['text'] for source in sources for passage in source['passages']):
                    raise CaseError(422, 'export_citation_invalid', 'A saved citation could not be verified.',
                                    'Review the saved sources before exporting this assessment.')
        presented = {finding['obligation_id'] for finding in result['findings']}
        unchecked = [obligation for obligation in snapshot['selected_obligations'] if obligation not in presented]
        state = result['job']['state']
        export_state = 'failed' if state == 'failed' else 'completed' if state == 'completed' and not unchecked else 'partial'
        label = {'completed':'Assessment export', 'partial':'Partial export', 'failed':'Failed assessment export'}[export_state]
        processing = 'Simulated processing' if result['data_mode']=='controlled_simulation' else 'Live model processing'
        data_label = 'Fictional bank data' if snapshot['synthetic'] else 'Authorized bank data'
        report = result | {'job': {key:value for key,value in result['job'].items() if key != 'lease_until'},
            'state': export_state, 'label': f'{label} · {processing} · {data_label}',
            'sources': sources, 'source_urls': sorted({s.get('source_url') for s in sources if s.get('source_url')}),
            'authority_verified_at': result['job']['authority_verified_at'], 'unchecked_obligations': unchecked,
            'cost_status': 'unknown', 'report_cutoff': result['summary']['cutoff'],
            'cohort': {'kind':'single_assessment', 'case_id':case, 'run_id':result['summary']['run_id'],
                'snapshot_id':snapshot['snapshot_id'], 'model_id':snapshot['model_version'],
                'prompt_version':snapshot['prompt_version'], 'data_mode':result['data_mode'],
                'recommendation_availability': {'through':result['summary']['cutoff'], 'end_inclusive':True},
                'runtime_selection': {'job_id':job_id, 'job_admitted_at':datetime.fromtimestamp(result['job']['created_at'], timezone.utc).isoformat(),
                    'job_state_time_basis':'observed_current_state'}},
            'limitations': [
                'Current regulatory status is unverified. This report does not certify bank compliance.',
                'A policy alone does not prove operational execution.', 'Human approval measures review decisions, not assessment accuracy.',
                'Available token usage appears in recorded attempts. Inference and total system costs remain unknown.',
                'The observed job state is current. The report cutoff controls saved findings, reviews, and trace events.']}
        if result['data_mode']=='controlled_simulation':
            report['limitations'].insert(0, 'Controlled example only. No live model call occurred.')
        else:
            report['limitations'].insert(0, 'Live model processing does not establish held-out quality or current-source completeness.')
        if unchecked or export_state != 'completed':
            report['limitations'].append('The assessment is incomplete or failed. Examine unchecked scope and the saved stop reason.')
        if format == 'json':
            return (json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False)+'\n').encode('utf-8')
        return markdown_export(report).encode('utf-8')

    def review(self, owner, case, job_id, finding_id, request):
        run, _ = self._run(owner, case, job_id)
        item = self._record(owner, case, 'finding', finding_id)
        if item['run_id'] != run['run_id']:
            raise not_found()
        timer = AttemptTimer()
        try:
            event = self.reviews.save(owner, case, finding_id, request)
        except ContractError as error:
            raise CaseError(409 if str(error) in {'revision_conflict', 'idempotency_conflict'} else 422, str(error),
                'The review was not saved. Its content or revision needs review.', 'Keep your draft. Refresh the saved review before another attempt.') from None
        self._trace(owner, case, run, 'review_event', timer, operation='storage', artifacts=(event.event_id,))
        return event


def markdown_export(report):
    """Untrusted source and reviewer text is quoted and escaped, never executable markup."""
    def quoted(value):
        text = json.dumps(value, ensure_ascii=False, indent=2) if not isinstance(value, str) else value
        safe = re.sub(r'([\\`*_{}\[\]#+!|>~])', r'\\\1', html.escape(text, quote=False))
        return '\n'.join('> '+line for line in safe.splitlines())+'\n'

    sections = [('Export status', report['label']), ('Snapshot and selected versions', report['snapshot']),
        ('Cohort filters and time bases', report['cohort']),
        ('Observed job state', report['job']), ('Report cutoff', report['report_cutoff']),
        ('Freshness and authority verification', {'freshness':report['freshness'], 'authority_verified_at':report['authority_verified_at']}),
        ('Obligation', report['obligation']), ('Mapped control', report['control']),
        ('Selected obligations', report['obligations']), ('Extracted controls', report['controls']),
        ('Original findings and recommendation IDs', report['findings']), ('Saved review events', report['reviews'])]
    text = '# The Regulator assessment report\n\n'+''.join(f'## {title}\n\n{quoted(value)}\n' for title,value in sections)
    text += '## Review summary\n\n'+''.join(f'{key}: {"Not measured" if value is None else value}\n\n' for key,value in report['summary'].items())
    text += '## Recorded runtime\n\ncost: Unknown\n\n'+quoted(report['trace'])+'\n'
    text += '## Unchecked obligations\n\n'+quoted(report['unchecked_obligations'])+'\n'
    for source in report['sources']:
        text += '## Source Version\n\n'+quoted(source)+'\n'
    return text+'## Limitations\n\n'+quoted('\n'.join(report['limitations']))
