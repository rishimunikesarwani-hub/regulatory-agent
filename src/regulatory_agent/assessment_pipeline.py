"""Selected historical scope with controlled or pinned live model adapters. No source transport or API admission."""
from datetime import datetime, timezone
from contextlib import contextmanager
import math
import re
import time
import uuid

from pydantic import ValidationError

from .assessments import PERIOD_PROMPT, SELECTED_PROMPT

from .contracts import COMPARISON_PROMPT, Citation, ContractError, EvidencePeriod, Finding, ReviewItem, SourceRead, citation_matches, iso_date, public_url
from .local import encoded, validated_action
from .telemetry import AttemptTimer, StageAttempt, TokenUsage, VersionMetadata


def ranked_context(sources, selected_versions, *, query, kinds, assessment_date, period=None, max_passages=20, max_bytes=64_000):
    """Filter before ranking. Unknown periods never become verified dates."""
    requested = EvidencePeriod.model_validate(period) if period else None
    if not 0 <= max_passages <= 20 or not 0 <= max_bytes <= 64_000:
        raise ContractError('context_limit_invalid')
    candidates, unknown, companions = [], [], {}
    for source in sources:
        document = source['document']
        if selected_versions.get(document['source_id']) != document['version'] or document['kind'] not in kinds:
            continue
        legacy = EvidencePeriod.model_validate(source['evidence_period']) if 'stated_periods' not in source and source.get('evidence_period') else None
        periods = {v['citations'][-1]['passage_id']:v for v in source.get('stated_periods',[])}
        lookup = {p['passage_id']:p for p in source['passages']}
        for passage in source['passages']:
            declared = periods.get(passage['passage_id'])
            known = EvidencePeriod.model_validate(declared['period']) if declared else legacy
            if known and (known.end > assessment_date or requested and (known.end < requested.start or known.start > requested.end)):
                continue
            if document['kind'] == 'evidence' and known is None:
                unknown.append(document['document_version_id'])
            candidates.append(passage)
            companions[passage['passage_id']] = [lookup[c['passage_id']] for c in declared['citations'][:-1]] if declared else []
    words = set(re.findall(r'[a-z0-9]+', query.lower()))
    def score(passage):
        tokens = re.findall(r'[a-z0-9]+', passage['text'].lower())
        return len(words.intersection(tokens)) / math.sqrt(max(1, len(tokens)))
    ordered = sorted(candidates, key=lambda p: (-score(p), p['passage_id']))
    selected, size, selected_ids = [], 0, set()
    for passage in ordered:
        bundle = [p for p in companions[passage['passage_id']] + [passage] if p['passage_id'] not in selected_ids]
        length = sum(len(p['text'].encode()) for p in bundle)
        if len(selected) + len(bundle) <= max_passages and size + length <= max_bytes:
            selected.extend(bundle); size += length; selected_ids.update(p['passage_id'] for p in bundle)
    return {'candidate_passage_ids': [p['passage_id'] for p in ordered],
            'selected_passage_ids': [p['passage_id'] for p in selected], 'passages': selected,
            'selected_bytes': size, 'unknown_period_version_ids': sorted(set(unknown))}


class AssessmentPipeline:
    def __init__(self, assessments, model):
        self.service, self.model = assessments, model
        self.store, self.reviews = assessments.store, assessments.reviews
        self._trace_observations = {}

    def _sources(self, owner, case, snapshot):
        sources, scopes, seen = self.service._sources(owner, case, snapshot), {}, set()
        for source in sources:
            validated = SourceRead.model_validate({key: source[key] for key in ('document', 'passages')})
            doc = validated.document
            if doc.case_id != case or snapshot['selected_versions'].get(doc.source_id) != doc.version:
                raise ContractError('source_scope_denied')
            if not doc.synthetic:
                if doc.kind != 'regulation' or not doc.source_url:
                    raise ContractError('private_source_processing_unverified')
                public_url(doc.source_url)
            for value in (doc.publication_date, doc.effective_date):
                if value is not None:iso_date(value)
            if doc.kind=='regulation' and doc.effective_date and doc.effective_date > snapshot['assessment_date']:
                raise ContractError('source_not_effective')
            if source.get('evidence_period'):
                EvidencePeriod.model_validate(source['evidence_period'])
            by_id = {p.passage_id: p for p in validated.passages}
            if len(by_id) != len(validated.passages) or seen.intersection(by_id) or any(p.document_version_id != doc.document_version_id for p in validated.passages):
                raise ContractError('ambiguous_source_passage')
            seen.update(by_id)
            if doc.kind == 'regulation':
                for obligation, ids in source.get('obligation_scopes', {}).items():
                    if obligation in snapshot['selected_obligations']:
                        if not isinstance(ids, list) or not ids or len(set(ids)) != len(ids) or not set(ids) <= by_id.keys():
                            raise ContractError('regulatory_scope_invalid')
                        scopes.setdefault(obligation, []).extend(by_id[key].model_dump() for key in ids)
        if set(scopes) != set(snapshot['selected_obligations']):
            raise ContractError('regulatory_scope_missing')
        if sum(len(p['text'].encode()) for s in sources for p in s['passages']) > 400_000:
            raise ContractError('source_extraction_limit')
        return sources, scopes

    def _begin_attempt(self, owner, case, run, token, key, stage, operation, *, candidates=(), selected=(), selected_bytes=None):
        job = self.store.read_job(owner, case, run['job_id'])
        self.store._claimed(job, token, time.time())
        timer = AttemptTimer()
        event = StageAttempt(event_id=uuid.uuid4().hex, attempt_id=uuid.uuid4().hex,
            run_id=run['run_id'], job_id=run['job_id'], snapshot_id=run['snapshot_id'], stage_id=key,
            stage=stage, operation=operation, state='unknown', dispatched=False,
            started_at=timer.started_at, finished_at=None, duration_seconds=None,
            versions=VersionMetadata(application='vs5-v1',
                schema='vs5-comparison-v1' if run['prompt_version']==COMPARISON_PROMPT else 'vs5-selection-period-v1' if run['prompt_version']==PERIOD_PROMPT else 'vs5-selection-v1' if run['prompt_version']==SELECTED_PROMPT else 'vs5-pipeline-v1',
                extraction='vs2-period-v1' if run['prompt_version']==PERIOD_PROMPT else 'vs2-v1',
                chunking='source-locations-v1', retrieval='specified-comparison-vs5-v1' if run['prompt_version']==COMPARISON_PROMPT else 'keyword-period-vs5-v1' if run['prompt_version']==PERIOD_PROMPT else 'keyword-vs5-v1', prompt=run['prompt_version'],
                model_configuration='controlled-response-v1' if run['data_mode']=='controlled_simulation' else
                    'openai-demo-v1' if run['model_id'].startswith('openai:') else 'india-converse-v1'),
            model_id=run['model_id'] if operation=='model' else None,
            unused_allowance=24-job['model_calls'] if operation=='model' else None,
            candidate_passage_ids=tuple(candidates), selected_passage_ids=tuple(selected), selected_text_bytes=selected_bytes)
        self.reviews.attempt(owner,case,event,execution_token=token)
        if run['data_mode']=='synthetic_live':
            from .langfuse_trace import start_attempt
            self._trace_observations[event.event_id]=start_attempt(event.model_dump(mode='json'))
        return event, timer

    def _finish_attempt(self, owner, case, run, token, attempt, *, state='succeeded', result=None, error=None):
        event, timer = attempt
        job = self.store.read_job(owner, case, run['job_id'])
        metadata = result or error
        calls = job['model_calls']
        update = dict(state=state, **timer.finish(),
            dispatched=getattr(metadata,'dispatched',calls > 24-event.unused_allowance) if event.operation=='model' else True,
            usage=getattr(metadata, 'usage', TokenUsage()), provider_request_id=getattr(metadata, 'provider_request_id', None),
            actual_response_model_id=getattr(metadata, 'actual_response_model_id', None),
            unused_allowance=24-calls if event.operation=='model' else None,
            errors=('validation_failure' if isinstance(error, (ContractError, ValidationError)) else 'tool_failure',) if error else ())
        if isinstance(result, dict) and 'selected_passage_ids' in result:
            update.update(candidate_passage_ids=tuple(result['candidate_passage_ids']),
                selected_passage_ids=tuple(result['selected_passage_ids']), selected_text_bytes=result['selected_bytes'])
        terminal = StageAttempt.model_validate(event.model_dump() | update)
        self.reviews.attempt(owner,case,terminal,execution_token=token,finish=True)
        if run['data_mode']=='synthetic_live':
            from .langfuse_trace import export_attempt
            export_attempt(terminal.model_dump(mode='json'),observation=self._trace_observations.pop(event.event_id,None))

    def _interrupt_attempts(self, owner, case, run, token):
        job=self.store.read_job(owner,case,run['job_id']); self.store._claimed(job,token,time.time())
        for body in self.reviews.records(owner,case,'stage_attempt'):
            if body['job_id']==run['job_id'] and body['state']=='unknown':
                event=StageAttempt.model_validate_json(encoded(body))
                event=StageAttempt.model_validate(event.model_dump() | {'state':'interrupted','errors':('interrupted',),
                    'finished_at':datetime.now(timezone.utc),
                    'dispatched':job['model_calls']>24-event.unused_allowance if event.operation=='model' else False})
                self.reviews.attempt(owner,case,event,execution_token=token,finish=True)

    @contextmanager
    def _processing(self, owner, case, run, token, key, stage, operation, **context):
        attempt = self._begin_attempt(owner, case, run, token, key, stage, operation, **context)
        completed = {}
        try:
            yield completed
        except Exception as error:
            self._finish_attempt(owner, case, run, token, attempt, state='failed', result=completed.get('result'), error=error)
            raise
        else:
            self._finish_attempt(owner, case, run, token, attempt, result=completed.get('result'))

    @staticmethod
    def _check_citations(citations, passages):
        lookup = {p['passage_id']: p for p in passages}
        for citation in citations:
            passage = lookup.get(citation.passage_id)
            if not citation_matches(citation,passage):
                raise ContractError('unexamined_or_invalid_citation')

    def _call(self, owner, case, run, snapshot, token, key, phase, data, context, sources):
        with self._processing(owner, case, run, token, f'select-{key}', 'context_selection', 'internal') as completed:
            prompt = encoded({'phase':phase, 'snapshot_id':snapshot['snapshot_id'],
                'document_version_ids':list(snapshot.get('selected_document_ids', {}).values()) or
                    [f'{name}:{version}' for name,version in snapshot['selected_versions'].items()],
                'bank_profile':snapshot['bank_profile'], 'assessment_date':snapshot['assessment_date'], 'data':data,
                'passages':context['passages'], 'candidate_passage_ids':context['candidate_passage_ids'],
                'source_metadata':[{'document_version_id':s['document']['document_version_id'], 'kind':s['document']['kind'],
                    'evidence_period':s.get('evidence_period')} | ({'stated_periods':[v for v in s['stated_periods']
                        if all(c['passage_id'] in context['selected_passage_ids'] for c in v['citations'])]} if 'stated_periods' in s else {}) for s in sources],
                'unknown_period_version_ids':context['unknown_period_version_ids']})
            if len(prompt.encode()) > 400_000:
                raise ContractError('model_context_limit')
            completed['result'] = context
        with self._processing(owner, case, run, token, key, 'model_call', 'model',
                candidates=context['candidate_passage_ids'], selected=context['selected_passage_ids'], selected_bytes=context['selected_bytes']) as completed:
            reply = self.model.dispatch(self.store, owner, case, run['job_id'], token,
                {'system': 'Assess only the selected evidence. Keep conditions, exceptions, and applicability. Missing owners and frequencies remain null. '
                    'A policy promise is not operational evidence. Missing or conflicting evidence requires review or an evidence gap, not proof of failure. '
                    'Use supported, partial, gap, needs_review, or not_applicable as appropriate. Not applicable needs a cited applicability reason. '
                    'Every finding needs cited claims, examined exceptions and conflicts, a known or null evidence period, and one nonblank primary remedy. '
                    'Use only the requested phase and supplied passage IDs. Never claim that unexamined documents were checked. '
                    'For assessment, inspect supplied candidates, request at most one refinement, or propose exactly one finding for the requested obligation.'
                    + (' Stated evidence periods declare dates only, not record completeness or actual control operation. Use a known claim period only within a cited record interval; otherwise keep it null.'
                       if snapshot['prompt_version']==PERIOD_PROMPT else ''),
                 'prompt':prompt, 'max_tokens':8192})
            completed['result'] = reply
            self.store._claimed(self.store.read_job(owner, case, run['job_id']), token, time.time())
            if (run['data_mode']=='controlled_simulation') != (reply.label=='Simulated'):
                raise ContractError('model_execution_mode_mismatch')
            action = validated_action(reply.action.model_dump_json(), self.store, owner, case, run['job_id'])
            return action

    def _context(self, passages):
        size = sum(len(p['text'].encode()) for p in passages)
        if len(passages) > 20 or size > 64_000:
            raise ContractError('mandatory_regulatory_context_limit')
        return {'candidate_passage_ids':[p['passage_id'] for p in passages],
                'selected_passage_ids':[p['passage_id'] for p in passages], 'passages':passages,
                'selected_bytes':size, 'unknown_period_version_ids':[]}

    def _validated_finding(self, action, obligation, controls, context, sources, snapshot, run):
        if action.action != 'propose_findings' or action.obligations or action.controls or action.retrieval_query or len(action.findings) != 1:
            raise ContractError('finding_action_invalid')
        finding = action.findings[0]
        if finding.obligation_id != obligation['obligation_id'] or not set(finding.control_ids) <= {c['control_id'] for c in controls}:
            raise ContractError('finding_mapping_invalid')
        if not finding.claims or not finding.remedy or not finding.remedy.strip():
            raise ContractError('finding_claim_or_remedy_missing')
        self._check_citations(finding.citations, context['passages'])
        declared = {encoded(c.model_dump()) for c in finding.citations}
        by_version = {s['document']['document_version_id']:s for s in sources}
        for claim in finding.claims:
            self._check_citations([*claim.citations, *claim.examined_exceptions, *claim.conflicting_evidence], context['passages'])
            if not all(encoded(c.model_dump()) in declared for c in claim.citations):
                raise ContractError('claim_citation_not_in_finding')
            if claim.evidence_period and claim.evidence_period.end > snapshot['assessment_date']:
                raise ContractError('claim_period_invalid')
            period = claim.evidence_period
            evidence = [by_version[c.document_version_id] for c in claim.citations if by_version[c.document_version_id]['document']['kind']=='evidence']
            grounded = False
            if period and snapshot['prompt_version']==PERIOD_PROMPT:
                cited = {c.passage_id for c in claim.citations}
                for source in evidence:
                    for stated in source['stated_periods']:
                        if stated['citations'][-1]['passage_id'] in cited and stated['period']['start'] <= period.start <= period.end <= stated['period']['end'] and all(c['passage_id'] in context['selected_passage_ids'] for c in stated['citations']):
                            self._check_citations(map(Citation.model_validate,stated['citations']),context['passages'])
                            grounded = True
                if not grounded: raise ContractError('claim_period_unverified')
            elif period:
                grounded = any(s.get('evidence_period') and s['evidence_period']['start'] <= period.start <= period.end <= s['evidence_period']['end'] for s in evidence)
            if finding.status == 'supported' and claim.operational and (period is None or not grounded):
                raise ContractError('operational_support_unverified')
        if finding.status == 'gap' and (finding.gap_kind != 'control' or finding.evidence_condition == 'missing'):
            raise ContractError('unsupported_control_gap')
        return Finding.model_validate(finding.model_dump() | {
            'finding_id':uuid.uuid5(uuid.NAMESPACE_URL, f"{run['run_id']}:{obligation['obligation_id']}").hex})

    def run(self, owner, case, job_id, *, execution_token=None):
        run, snapshot = self.service._run(owner, case, job_id)
        token = self.store.claim(owner, case, job_id) if execution_token is None else execution_token
        if token is None:
            return self.store.read_job(owner, case, job_id)
        self.store._claimed(self.store.read_job(owner, case, job_id), token, time.time())
        try:
            self._interrupt_attempts(owner, case, run, token)
            with self._processing(owner, case, run, token, 'source-check', 'source_verification', 'internal'):
                if snapshot['mode'] != 'historical' or not snapshot['synthetic']:
                    raise ContractError('source_or_private_processing_unverified')
                sources, scopes = self._sources(owner, case, snapshot)
            all_regulation = list({p['passage_id']:p for values in scopes.values() for p in values}.values())
            reg_context = self._context(all_regulation)
            job = self.store.read_job(owner, case, job_id)
            if 'obligations' not in job['stages']:
                with self._processing(owner, case, run, token, 'obligation-extraction', 'extraction', 'internal'):
                    action = self._call(owner, case, run, snapshot, token, 'extract-obligations', 'retrieve_obligations',
                        {'selected_obligations':snapshot['selected_obligations'], 'scope_passage_ids':{k:[p['passage_id'] for p in v] for k,v in scopes.items()}}, reg_context, sources)
                    if action.action != 'retrieve_obligations' or action.controls or action.findings or action.retrieval_query or {o.obligation_id for o in action.obligations} != set(scopes) or len(action.obligations) != len(scopes):
                        raise ContractError('obligation_extraction_invalid')
                    for obligation in action.obligations:self._check_citations(obligation.citations, scopes[obligation.obligation_id])
                    by_id = {o.obligation_id:o.model_dump() for o in action.obligations}
                    self.store.save_stage(owner, case, job_id, token, 'obligations', {'obligations':[by_id[o] for o in snapshot['selected_obligations']]})
            obligations = self.store.read_job(owner, case, job_id)['stages']['obligations']['obligations']
            if 'controls' not in job['stages']:
                with self._processing(owner, case, run, token, 'control-extraction', 'extraction', 'internal'):
                    context = ranked_context(sources, snapshot['selected_versions'], query=' '.join(o['requirement'] for o in obligations),
                        kinds={'policy','control'}, assessment_date=snapshot['assessment_date'])
                    action = self._call(owner, case, run, snapshot, token, 'extract-controls', 'find_controls', {'obligations':obligations}, context, sources)
                    if action.action != 'find_controls' or action.obligations or action.findings or action.retrieval_query or len({c.control_id for c in action.controls}) != len(action.controls):
                        raise ContractError('control_extraction_invalid')
                    for control in action.controls:self._check_citations(control.citations, context['passages'])
                    self.store.save_stage(owner, case, job_id, token, 'controls', {'controls':[c.model_dump() for c in action.controls]})
            controls = self.store.read_job(owner, case, job_id)['stages']['controls']['controls']
            for obligation in obligations:
                identity = obligation['obligation_id']; key = f'validated-{identity}'; presented = f'presented-{identity}'
                job = self.store.read_job(owner, case, job_id)
                if presented in job['stages']:continue
                if key not in job['stages']:
                    query = obligation['requirement']; refined = False; inspected = False; inspection = []
                    for iteration in range(4):
                        retrieval = self._begin_attempt(owner, case, run, token, f'context-{identity}-{iteration}', 'retrieval', 'retrieval')
                        source_passages = {p['passage_id']:p for s in sources for p in s['passages']}
                        mandatory = {p['passage_id']:p for p in scopes[identity]}
                        mandatory.update({c['passage_id']:source_passages[c['passage_id']] for control in controls for c in control['citations']})
                        mandatory_context = self._context(list(mandatory.values()))
                        bank = ranked_context(sources, snapshot['selected_versions'], query=query, kinds={'profile','policy','control','evidence'},
                            assessment_date=snapshot['assessment_date'], max_passages=20-len(mandatory), max_bytes=64_000-mandatory_context['selected_bytes'])
                        remaining = [p for p in bank['passages'] if p['passage_id'] not in mandatory]
                        if inspection:
                            chosen = [source_passages[key] for key in inspection if key not in mandatory]
                            self._context(list(mandatory.values())+chosen)
                            remaining = chosen + [p for p in remaining if p['passage_id'] not in inspection]
                        selected = list(mandatory.values())
                        for passage in remaining:
                            if len(selected)<20 and sum(len(p['text'].encode()) for p in selected)+len(passage['text'].encode())<=64_000:
                                selected.append(passage)
                        context = self._context(selected)
                        context['candidate_passage_ids'] = [p['passage_id'] for p in scopes[identity]] + bank['candidate_passage_ids']
                        context['unknown_period_version_ids'] = bank['unknown_period_version_ids']
                        self._finish_attempt(owner, case, run, token, retrieval, result=context)
                        action = self._call(owner, case, run, snapshot, token, f'assess-{identity}-{iteration}', 'assessment',
                            {'obligation':obligation, 'controls':controls, 'refinement_used':refined}, context, sources)
                        if action.action == 'refine_retrieval' and not refined and not (action.findings or action.controls or action.obligations):
                            query = action.retrieval_query or query; refined = True; continue
                        if action.action == 'inspect_evidence' and not inspected and not (action.findings or action.controls or action.obligations or action.retrieval_query):
                            if not action.passage_ids or len(action.passage_ids)>20 or not set(action.passage_ids) <= set(context['candidate_passage_ids']):
                                raise ContractError('inspection_scope_denied')
                            inspection = action.passage_ids; inspected = True; continue
                        with self._processing(owner, case, run, token, key, 'validation', 'internal'):
                            finding = self._validated_finding(action, obligation, controls, context, sources, snapshot, run)
                            self.store.save_stage(owner, case, job_id, token, key, {'finding':finding.model_dump()})
                        break
                    else:raise ContractError('agent_action_limit')
                finding = self.store.read_job(owner, case, job_id)['stages'][key]['finding']
                item = ReviewItem.model_validate(finding | {'run_id':run['run_id'], 'primary_recommendation':finding['remedy'],
                    'available_at':datetime.now(timezone.utc).isoformat(), 'model_id':run['model_id'], 'prompt_version':run['prompt_version'],
                    'data_mode':run['data_mode'], 'source_version_ids':[f'{name}:{version}' for name,version in snapshot['selected_versions'].items()]})
                with self._processing(owner, case, run, token, presented, 'persistence', 'storage'):
                    self.reviews.present(owner, case, item, execution_token=token)
                self.store.save_stage(owner, case, job_id, token, presented, {'accounted_obligations':[identity]})
            job = self.store.read_job(owner, case, job_id)
            accounted = {o for stage in job['stages'].values() for o in stage.get('accounted_obligations', [])}
            unchecked = [o for o in snapshot['selected_obligations'] if o not in accounted]
            self.store.finalize(owner, case, job_id, token, 'partial' if unchecked else 'completed', unchecked)
        except Exception:
            job = self.store.read_job(owner, case, job_id)
            if job['token'] != token or job['state'] != 'running':
                raise ContractError('stale_execution_claim') from None
            accounted = {o for stage in job['stages'].values() for o in stage.get('accounted_obligations', [])}
            unchecked = [o for o in snapshot['selected_obligations'] if o not in accounted]
            self.store.finalize(owner, case, job_id, token, 'partial' if accounted else 'failed', unchecked, reason='pipeline_failed')
        return self.store.read_job(owner, case, job_id)
