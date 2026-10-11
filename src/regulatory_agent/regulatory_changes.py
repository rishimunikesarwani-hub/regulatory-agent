"""Strict specified-version comparison context and model interpretation validation."""
import hashlib
from typing import Literal

from pydantic import Field, TypeAdapter, model_validator

from .assessment_selection import _Text
from .assessment_pipeline import AssessmentPipeline
from .contract_types import Contract, Identifier
from .contracts import Citation, ContractError, Obligation, Snapshot, SourceRead, Text, iso_date, public_url
from .local import encoded


CHANGED=frozenset(('added_requirement','changed_requirement','withdrawn_requirement'))


class ObligationChange(Contract):
    obligation_id: Identifier
    kind: Literal['added_requirement','changed_requirement','withdrawn_requirement','unchanged',
                  'wording_only','appearance_only','undetermined']
    before: Obligation | None
    after: Obligation | None
    reason: Text
    basis: list[Citation] = Field(min_length=2,max_length=20)
    affected_control_ids: list[Identifier] = Field(max_length=20)

    @model_validator(mode='after')
    def classification(self):
        if not self.reason.strip() or len(set(self.affected_control_ids))!=len(self.affected_control_ids):
            raise ValueError('invalid_change_content')
        if self.kind=='added_requirement':
            if self.before is not None or self.after is None: raise ValueError('invalid_change_sides')
        elif self.kind=='withdrawn_requirement':
            if self.before is None or self.after is not None: raise ValueError('invalid_change_sides')
        elif self.kind!='undetermined' and (self.before is None or self.after is None):
            raise ValueError('invalid_change_sides')
        if self.kind not in CHANGED and self.affected_control_ids: raise ValueError('unsupported_control_impact')
        if self.kind in {'unchanged','wording_only','appearance_only'} and any(
                getattr(self.before,k)!=getattr(self.after,k) for k in ('conditions','exceptions','applicability')):
            raise ValueError('changed_requirement_metadata')
        if self.kind=='unchanged' and ' '.join(self.before.requirement.split())!=' '.join(self.after.requirement.split()):
            raise ValueError('changed_requirement_statement')
        if any(o and o.obligation_id!=self.obligation_id for o in (self.before,self.after)):
            raise ValueError('change_obligation_mismatch')
        return self


class ChangeInterpretation(Contract):
    snapshot_id: Identifier
    older_version_id: Identifier
    newer_version_id: Identifier
    changes: list[ObligationChange] = Field(min_length=1,max_length=20)


def _source(source, raw):
    result=SourceRead.model_validate({k:source[k] for k in ('document','passages')}).model_dump()
    document=result['document']
    if document['kind']!='regulation' or document['synthetic'] or source.get('authority')!='Reserve Bank of India':
        raise ContractError('comparison_authority_invalid')
    public_url(document['source_url'])
    for field in ('source_url','publication_date','effective_date'):
        if field in source and source[field]!=document[field]: raise ContractError('comparison_metadata_conflict')
    for field in ('publication_date','effective_date'): iso_date(document[field])
    if not isinstance(raw,bytes) or hashlib.sha256(raw).hexdigest()!=document['sha256']:
        raise ContractError('comparison_original_integrity')
    parser=_Text();parser.feed(raw.decode('utf-8-sig'))
    original=' '.join(' '.join(parser.parts).split())
    passages=result['passages']; identities=[p['passage_id'] for p in passages]
    if not passages or len(identities)!=len(set(identities)) or any(
            p['document_version_id']!=document['document_version_id'] or not p['location'].strip() or
            not p['text'].strip() or ' '.join(p['text'].split()) not in original for p in passages):
        raise ContractError('comparison_passage_integrity')
    withdrawn=source.get('withdrawn');amendments=source.get('amendments')
    if withdrawn is not None and type(withdrawn) is not bool: raise ContractError('comparison_metadata_invalid')
    if amendments is not None:
        amendments=TypeAdapter(list[Identifier]).validate_python(amendments,strict=True)
        if len(set(amendments))!=len(amendments): raise ContractError('comparison_metadata_invalid')
    return result|{'authority':source['authority'],'withdrawn':withdrawn,'amendments':amendments}


def prepare_pair(snapshot, older, newer, older_original, newer_original):
    """Pure preparation. A source difference is not a semantic requirement classification."""
    try:
        snapshot=Snapshot.model_validate(snapshot.model_dump() if isinstance(snapshot,Snapshot) else snapshot)
        old,new=_source(older,older_original),_source(newer,newer_original)
        a,b=old['document'],new['document'];name=a['source_id']
        if a['case_id']!=snapshot.case_id or b['case_id']!=snapshot.case_id or b['source_id']!=name or \
                a['version']==b['version'] or a['document_version_id']==b['document_version_id'] or \
                snapshot.selected_versions.get(name)!=a['version'] or \
                snapshot.selected_document_ids.get(name)!=a['document_version_id'] or \
                b['publication_date']<a['publication_date']:
            raise ContractError('comparison_pair_invalid')
        if set(p['passage_id'] for p in old['passages']).intersection(p['passage_id'] for p in new['passages']):
            raise ContractError('comparison_passage_integrity')
        metadata={field:{'older':a[field],'newer':b[field]} for field in ('publication_date','effective_date','source_url')
                  if a[field]!=b[field]}
        metadata.update({field:{'older':old[field],'newer':new[field]} for field in ('withdrawn','amendments')
                         if old[field]!=new[field]})
        pair={'snapshot_id':snapshot.snapshot_id,'assessment_date':snapshot.assessment_date,
            'selected_obligations':list(snapshot.selected_obligations),'older_source':old,'newer_source':new,
            'metadata_changes':metadata,'older_applicable':a['effective_date']<=snapshot.assessment_date,
            'newer_applicable':b['effective_date']<=snapshot.assessment_date,'freshness':'unverified'}
        if len(old['passages'])+len(new['passages'])>20 or len(encoded(pair).encode())>64_000:
            raise ContractError('comparison_context_limit')
        return pair
    except (ValueError,TypeError,KeyError,AttributeError) as error:
        if isinstance(error,ContractError): raise
        raise ContractError('comparison_source_invalid') from None


def _citations(citations, sources, *, versions):
    if any(c.document_version_id not in versions for c in citations): raise ContractError('comparison_citation_invalid')
    AssessmentPipeline._check_citations(citations,[p for s in sources for p in s['passages']])


def validate_changes(pair, response, baseline_findings):
    """Validate a model proposal. This does not prove semantic support or authorize processing."""
    try:
        result=ChangeInterpretation.model_validate(response)
        old,new=pair['older_source'],pair['newer_source']
        a,b=old['document']['document_version_id'],new['document']['document_version_id']
        if (result.snapshot_id,result.older_version_id,result.newer_version_id)!=(pair['snapshot_id'],a,b):
            raise ContractError('comparison_interpretation_scope')
        selected=pair['selected_obligations']; ids=[c.obligation_id for c in result.changes]
        if len(ids)!=len(set(ids)) or set(ids)!=set(selected): raise ContractError('comparison_obligation_scope')
        mappings={identity:set() for identity in selected}
        for finding in baseline_findings:
            if finding['snapshot_id']!=pair['snapshot_id'] or finding['obligation_id'] not in mappings:
                raise ContractError('comparison_baseline_scope')
            controls=TypeAdapter(list[Identifier]).validate_python(finding['control_ids'],strict=True)
            mappings[finding['obligation_id']].update(controls)
        for change in result.changes:
            _citations(change.basis,[old,new],versions={a,b})
            if {c.document_version_id for c in change.basis}!={a,b}: raise ContractError('comparison_basis_missing')
            for obligation,version in ((change.before,a),(change.after,b)):
                if obligation:
                    if not obligation.requirement.strip(): raise ContractError('comparison_requirement_invalid')
                    _citations(obligation.citations,[old,new],versions={version})
            if not set(change.affected_control_ids)<=mappings[change.obligation_id]:
                raise ContractError('comparison_control_scope')
        changed=any(c.kind in CHANGED for c in result.changes)
        unresolved=[c.obligation_id for c in result.changes if c.kind=='undetermined']
        return result.model_dump()|{'metadata_changes':pair['metadata_changes'],
            'affected_control_ids':sorted({control for c in result.changes for control in c.affected_control_ids}),
            'unresolved_obligation_ids':unresolved,'assessment_required':changed and pair['newer_applicable'],
            'selection_review_required':bool(changed or unresolved or pair['metadata_changes'])}
    except (ValueError,TypeError,KeyError,AttributeError) as error:
        if isinstance(error,ContractError): raise
        raise ContractError('comparison_interpretation_invalid') from None
