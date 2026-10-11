"""Native cloud persistence for the shared assessment, review, report, and export rules."""
from datetime import datetime, timezone
import hashlib
import time
import uuid

from .assessments import Assessments
from .cases import not_found
from .contracts import COMPARISON_PROMPT, ContractError, ReviewDecision, ReviewItem, ReviewRequest, Snapshot
from .local import encoded, identifier
from .reviews import Reviews, instant
from .telemetry import StageAttempt


class CloudReviews(Reviews):
    def records(self, owner, case, kind):
        return self.store.records(owner,case,kind)

    def admit(self, owner, case, run_id, snapshot_id, data_mode):
        identifier(run_id)
        snapshot=Snapshot.model_validate(self.store.get(owner,case,'snapshot',snapshot_id))
        job=self.store.admit(owner,snapshot,run_id,data_mode=data_mode)
        body=dict(run_id=run_id,job_id=job['job_id'],snapshot_id=snapshot_id,data_mode=data_mode,
            job_admitted_at=datetime.fromtimestamp(job['created_at'],timezone.utc).isoformat().replace('+00:00','Z'),
            model_id=snapshot.model_version,prompt_version=snapshot.prompt_version,selected_obligations=snapshot.selected_obligations)
        self.store.put(owner,case,'run',run_id,body)
        return body

    def present(self, owner, case, item, *, execution_token=None):
        item=ReviewItem.model_validate(item.model_dump())
        snapshot=self.store.get(owner,case,'snapshot',item.snapshot_id)
        if item.obligation_id not in snapshot['selected_obligations'] or set(item.source_version_ids)!={
                f'{name}:{version}' for name,version in snapshot['selected_versions'].items()}:
            raise ContractError('item_snapshot_scope_denied')
        run=self.store.get(owner,case,'run',item.run_id)
        if any(getattr(item,field)!=run[field] for field in ('snapshot_id','model_id','prompt_version','data_mode')):
            raise ContractError('item_run_mismatch')
        unit=uuid.uuid5(uuid.NAMESPACE_URL,encoded([item.run_id,item.obligation_id])).hex
        for _ in range(4):
            if execution_token is not None:
                self.store._claimed(self.store.read_job(owner,case,run['job_id']),execution_token,time.time())
            old=self.store._metadata(owner,case,'finding',item.finding_id,missing=True)
            if old:
                saved=self.store._body(owner,case,'finding',item.finding_id,old)
                if saved!=item.model_copy(update={'available_at':saved['available_at']}).model_dump(mode='json'):
                    raise ContractError('immutable_record')
                return ReviewItem.model_validate(saved)
            if self.store._metadata(owner,case,'review_unit',unit,missing=True): raise ContractError('duplicate_review_item')
            now=self.clock()
            if now.utcoffset() is None or now<instant(run['job_admitted_at']): raise ContractError('invalid_presentation_time')
            saved=ReviewItem.model_validate(item.model_dump()|{'available_at':now.isoformat()})
            finding=self.store.prepare(owner,case,'finding',saved.finding_id,saved.model_dump(mode='json'))
            finding['review_revision']={'N':'0'}
            unique=self.store.prepare(owner,case,'review_unit',unit,{'finding_id':saved.finding_id})
            if self.store.commit(owner,case,[finding,unique],job_id=run['job_id'],token=execution_token): return saved
        raise ContractError('record_write_conflict')

    def history(self, owner, case, finding_id):
        self.store.get(owner,case,'finding',finding_id)
        return sorted((ReviewDecision.model_validate(v) for v in self.records(owner,case,'review') if v['finding_id']==finding_id),
            key=lambda event:event.revision)

    def save(self, owner, case, finding_id, request):
        request=ReviewRequest.model_validate(request.model_dump())
        for _ in range(4):
            metadata=self.store._metadata(owner,case,'finding',finding_id)
            item=ReviewItem.model_validate(self.store._body(owner,case,'finding',finding_id,metadata))
            history=self.history(owner,case,finding_id)
            event=self.decision(owner,item,history,request)
            if event in history: return event
            if int(metadata['review_revision']['N'])!=request.expected_revision: continue
            identity=uuid.uuid5(uuid.NAMESPACE_URL,encoded([owner,case,finding_id,request.idempotency_key])).hex
            event=event.model_copy(update={'event_id':identity})
            record=self.store.prepare(owner,case,'review',identity,event.model_dump(mode='json'))
            revised=metadata | {'revision':{'N':str(int(metadata['revision']['N'])+1)},'review_revision':{'N':str(event.revision)}}
            if self.store.commit(owner,case,[revised,record]): return event
        raise ContractError('revision_conflict')

    def report(self, owner, case, cohort):
        items=[ReviewItem.model_validate(v) for v in self.records(owner,case,'finding')]
        histories={item.finding_id:self.history(owner,case,item.finding_id) for item in items}
        return self.outcomes(items,histories,cohort)

    def attempt(self, owner, case, event, *, execution_token=None, finish=False):
        event=StageAttempt.model_validate(event.model_dump())
        run=self.store.get(owner,case,'run',event.run_id)
        if (event.job_id,event.snapshot_id)!=(run['job_id'],run['snapshot_id']): raise ContractError('attempt_scope_denied')
        for _ in range(4):
            metadata=self.store._metadata(owner,case,'stage_attempt',event.event_id,missing=True)
            if finish:
                if metadata is None: raise ContractError('attempt_already_terminal')
                old=StageAttempt.model_validate_json(encoded(self.store._body(owner,case,'stage_attempt',event.event_id,metadata)))
                self.finish_attempt(old,event)
            elif metadata is not None: raise ContractError('immutable_record')
            revision=int(metadata['revision']['N']) if metadata else 0
            record=self.store.prepare(owner,case,'stage_attempt',event.event_id,event.model_dump(mode='json'),revision)
            if self.store.commit(owner,case,[record],job_id=event.job_id,token=execution_token,permit_expired=finish): return
        raise ContractError('record_write_conflict')


class CloudAssessments(Assessments):
    def __init__(self, cases, documents, store):
        self.cases,self.documents,self.store=cases,documents,store
        self.reviews=CloudReviews(store)

    def _bank_source(self, owner, case, version_id):
        return self.documents.read_full(owner,case,version_id)

    def list(self, owner, case):
        return {'runs':[r for r in self.store.records(owner,case,'run') if r['prompt_version']!=COMPARISON_PROMPT]}

    def _run(self, owner, case, job_id):
        job=self.store.read_job(owner,case,job_id)
        for run in self.store.records(owner,case,'run'):
            if run['job_id']==job_id:
                if run['snapshot_id']!=job['snapshot_id']: raise ContractError('run_snapshot_scope_invalid')
                snapshot=self.store.get(owner,case,'snapshot',run['snapshot_id'])
                if snapshot!=self.store.snapshot(owner,case,job_id): raise ContractError('run_snapshot_scope_invalid')
                return run,snapshot
        raise not_found()

    def _public_original(self, owner, case, source):
        self.cases.read(owner,case)
        reference=source.get('original_ref')
        if not reference: raise ContractError('source_original_missing')
        raw=self.store.objects.read_extraction(owner,case,reference)
        if hashlib.sha256(raw).hexdigest()!=source['document']['sha256']: raise ContractError('source_integrity_failure')
        return raw

    def _read_records(self, owner, case, run):
        job=self.store.read_job(owner,case,run['job_id'])
        items=[ReviewItem.model_validate(v) for v in self.store.records(owner,case,'finding') if v['run_id']==run['run_id']]
        events=[event.model_dump() for item in items for event in self.reviews.history(owner,case,item.finding_id)]
        trace=[v for v in self.store.records(owner,case,'stage_attempt') if v['run_id']==run['run_id']]
        return job,items,events,trace

    def _bank_record(self, owner, case, version_id):
        stored=self.store.get(owner,case,'document',version_id)
        if 'original' in stored: return stored
        original=self.documents._source(owner,case,version_id)
        if original['document']!=stored['document']: raise ContractError('source_integrity_failure')
        return original

    def source_original(self, owner, case, job_id, version_id):
        source=self.source(owner,case,job_id,version_id)
        if source['document']['kind']=='regulation': return self._public_original(owner,case,source),'historical-regulation.html'
        stored=self._bank_record(owner,case,version_id)
        raw=self.store.objects.read(owner,case,stored['original'])
        if hashlib.sha256(raw).hexdigest()!=source['document']['sha256']: raise ContractError('source_integrity_failure')
        return raw,stored['filename']

    def source_page(self, owner, case, job_id, version_id, *, offset=0):
        from .aws_documents import source_read
        from .documents import rejected
        _,snapshot=self._run(owner,case,job_id)
        if version_id not in snapshot['selected_document_ids'].values(): raise not_found()
        source=self.store.get(owner,case,'document',version_id)
        if source['document']['kind']!='regulation' and 'passages' not in source:
            return source_read(self.store.objects,owner,case,source,offset=offset)
        if source['document']['kind']=='regulation': self._public_original(owner,case,source)
        passages=source['passages']
        if type(offset) is not int or not 0<=offset<len(passages): raise rejected()
        return {k:v for k,v in source.items() if k not in {'original_ref','original_blob'}}|{
            'passages':passages[offset:offset+500],'offset':offset,'passage_count':len(passages),
            'next_offset':offset+500 if offset+500<len(passages) else None}
