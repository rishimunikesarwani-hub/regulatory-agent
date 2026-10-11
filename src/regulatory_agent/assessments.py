"""One controlled historical example using the existing durable job and review services."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import uuid

from .cases import CaseError, not_found
from .contracts import Citation, ContractError, Control, Finding, Obligation, ReviewItem, Snapshot
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
        bank = {name: version for name, version in request.selected_versions.items() if name != REGULATION}
        if request.selected_obligations != [OBLIGATION] or request.assessment_date != '2024-04-08' or \
                request.selected_versions.get(REGULATION) != VERSION or len(bank) != 1:
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
        manifest = json.loads((ROOT / 'data/sources/source-manifest.json').read_text(encoding='utf-8'))['versions'][0]
        raw = (ROOT / manifest['raw_path']).read_bytes()
        if hashlib.sha256(raw).hexdigest() != manifest['sha256']:
            raise invalid('historical_source_integrity', 503)
        regulation = {'document': {'document_version_id': REG_ID, 'case_id': case, 'source_id': REGULATION,
            'kind': 'regulation', 'version': VERSION, 'sha256': manifest['sha256'], 'synthetic': False},
            'filename': manifest['title'], 'format': 'html', 'freshness': 'unverified', 'source_url': manifest['source_url'],
            'publication_date': manifest['publication_date'], 'effective_date': manifest['effective_date'],
            'passages': [{'passage_id': f"{REG_ID}:{p['passage_id']}", 'document_version_id': REG_ID,
                          'location': p['locator'], 'text': p['text']} for p in manifest['passages']]}
        self.store.put(owner, case, 'document', REG_ID, regulation)
        self.store.put(owner, case, 'document', f'{name}:{version}', document)
        snapshot = Snapshot(snapshot_id=identity, case_id=case, bank_profile=profile.bank_profile,
            selected_versions=request.selected_versions, selected_obligations=request.selected_obligations,
            assessment_date=request.assessment_date, mode=request.mode, prompt_version=PROMPT, model_version=MODEL, synthetic=True)
        try:
            self.store.save_snapshot(owner, snapshot)
        except ContractError:
            raise invalid('idempotency_conflict', 409) from None
        return self.reviews.admit(owner, case, identity, identity, 'controlled_simulation')

    def list(self, owner, case):
        self.cases.read(owner, case)
        with self.store.transaction() as db:
            self.store.authorize(owner, case, db)
            return {'runs': self.reviews._records(db, case, 'run')}

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

    def _sources(self, owner, case, snapshot):
        return [self.store.get(owner, case, 'document', f'{name}:{version}') for name, version in snapshot['selected_versions'].items()]

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
            versions=VersionMetadata(application='vs3-v1', schema='t2-v1', extraction='vs2-v1', chunking='source-locations-v1',
                retrieval='fixed-example-v1', prompt=PROMPT, model_configuration='controlled-response-v1'),
            model_id=MODEL if operation == 'model' else None, artifact_ids=tuple(artifacts), original_processing_event_id=original,
            candidate_passage_ids=tuple(candidates), selected_passage_ids=tuple(selected), errors=(error,) if error else ())
        with self.store.transaction() as db:
            self.store.authorize(owner, case, db)
            self.reviews._insert(db, case, 'stage_attempt', event.event_id, event.model_dump(mode='json'))

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
            if finding.snapshot_id != snapshot['snapshot_id'] or finding.obligation_id != OBLIGATION:
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
                available_at=datetime.now(timezone.utc).isoformat(), model_id=MODEL, prompt_version=PROMPT,
                data_mode='controlled_simulation', source_version_ids=[f'{name}:{version}' for name, version in snapshot['selected_versions'].items()])
            self.reviews.present(owner, case, item)
            return {'accounted_obligations': [OBLIGATION], 'finding_id': item.finding_id}

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

    def read(self, owner, case, job_id, cutoff=None):
        run, snapshot = self._run(owner, case, job_id)
        try:
            limit = instant(cutoff) if cutoff else datetime.now(timezone.utc)
            if limit.utcoffset() is None:
                raise ValueError()
        except ValueError:
            raise invalid('invalid_cutoff') from None
        with self.store.transaction() as db:
            self.store.authorize(owner, case, db)
            items = [ReviewItem.model_validate(item) for item in self.reviews._records(db, case, 'finding') if item['run_id'] == run['run_id']]
            events = [event.model_dump() for item in items for event in self.reviews._history(db, case, item.finding_id)]
            trace = [event for event in self.reviews._records(db, case, 'stage_attempt') if event['run_id'] == run['run_id']]
        eligible = [item for item in items if instant(item.available_at) <= limit]
        finals = []
        for item in eligible:
            history = [event for event in self.reviews.history(owner, case, item.finding_id)
                       if event.event_kind == 'final_review' and instant(event.committed_at) <= limit]
            finals.append(history[-1] if history else None)
        job = self.store.read_job(owner, case, job_id)
        obligation, control, _ = self._example(owner, case, job_id, snapshot)
        return {'data_mode': 'controlled_simulation', 'freshness': 'unverified', 'live_model_calls': 0, 'cost_usd': None,
            'job': {key: value for key, value in job.items() if key not in {'token', 'stages'}}, 'snapshot': snapshot,
            'obligation': obligation.model_dump(), 'control': control.model_dump(), 'findings': [item.model_dump() for item in items],
            'reviews': sorted(events, key=lambda e: e['revision']),
            'summary': {'metric_definition_version': 'd24-v1', 'cutoff': limit.isoformat(), 'data_mode': 'controlled_simulation',
                        'run_id': run['run_id'], **counts(eligible, finals)},
            'trace': {'run_id': run['run_id'], 'attempts': trace}}

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
