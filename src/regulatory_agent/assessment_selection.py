"""Immutable historical admission. The external current-source adapter remains separate."""
import hashlib
from html.parser import HTMLParser
import json
import os
import re
import uuid

from .assessment_pipeline import AssessmentPipeline
from .assessments import PERIOD_PROMPT, ROOT, invalid
from .cases import CaseError, not_found
from .contracts import ContractError, Snapshot, SourceRead, public_url
from .local import BlobStore
from .openai_model import selected_model


class _Text(HTMLParser):
    def __init__(self):
        super().__init__(); self.parts = []; self.hidden = 0

    def handle_starttag(self, tag, attrs):
        if tag in {'script', 'style'}: self.hidden += 1

    def handle_endtag(self, tag):
        if tag in {'script', 'style'}: self.hidden = max(0, self.hidden - 1)

    def handle_data(self, data):
        if not self.hidden: self.parts.append(data)


class AssessmentSelection:
    root = ROOT
    def __init__(self, service):
        self.service = service
        self.store = service.store
        self.blobs = BlobStore(self.store.path.with_suffix('.sources'), self.store)

    def _raw(self, manifest):
        path = (self.root / manifest['raw_path']).resolve()
        if not path.is_relative_to((self.root / 'data/sources').resolve()):
            raise ContractError('source_path_denied')
        raw = path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != manifest['sha256']:
            raise ContractError('historical_source_integrity')
        return raw

    def _catalog_sources(self, owner, case):
        self.service.cases.read(owner, case)
        sources = []
        for entry in json.loads((self.root / 'data/sources/source-manifest.json').read_text(encoding='utf-8'))['versions']:
            if entry['synthetic']: continue
            public_url(entry['source_url'])
            raw = self._raw(entry)
            parser = _Text(); parser.feed(raw.decode('utf-8-sig'))
            original = ' '.join(' '.join(parser.parts).split())
            if any(' '.join(p['text'].split()) not in original for p in entry['passages']):
                raise ContractError('historical_extraction_integrity')
            name, version = entry['document_id'], entry['version_id']
            identity = uuid.uuid5(uuid.NAMESPACE_URL, f'{case}:{name}:{version}:source-vs5-v1').hex
            passages = [{'document_version_id':identity, 'passage_id':f"{identity}:{p['passage_id']}",
                         'location':p['locator'], 'text':p['text']} for p in entry['passages']]
            common = [p['passage_id'] for p in passages if re.match(r'^Clause 2\(', p['location'])]
            scopes = {f"{name}:{p['passage_id']}":common + [passages[i]['passage_id']]
                for i,p in enumerate(entry['passages']) if not re.match(r'^Clause 2\(', p['locator'])}
            doc = {'document_version_id':identity, 'case_id':case, 'source_id':name, 'version':version,
                   'kind':'regulation', 'sha256':entry['sha256'], 'synthetic':False,
                   'storage_reference':identity+'-original', 'source_url':entry['source_url'],
                   'publication_date':entry['publication_date'], 'effective_date':entry['effective_date']}
            SourceRead.model_validate({'document':doc, 'passages':passages})
            sources.append({'document':doc, 'passages':passages, 'obligation_scopes':scopes,
                'original_blob':doc['storage_reference'], 'filename':entry['title'], 'format':'html',
                'source_url':entry['source_url'], 'publication_date':entry['publication_date'],
                'effective_date':entry['effective_date'], 'authority':entry['authority'],
                'freshness':'unverified', 'coverage':'saved historical excerpts'})
        return sources + [self.service._bank_source(owner, case, s['document']['document_version_id'])
                          for s in self.service.documents.list(owner, case)['sources']]

    def catalog(self, owner, case):
        sources = self._catalog_sources(owner, case)
        obligations = []
        for source in sources:
            passages = {p['passage_id']:p for p in source['passages']}
            doc = source['document']
            for identity, scope in source.get('obligation_scopes', {}).items():
                obligations.append({'obligation_id':identity, 'document_version_id':doc['document_version_id'],
                    'source_id':doc['source_id'], 'version':doc['version'], 'label':passages[scope[-1]]['location'],
                    'scope_passage_ids':scope})
        model=selected_model()
        from .langfuse_trace import configured
        return {'sources':sources, 'obligations':obligations, 'freshness':'unverified', 'current_available':False,
                'coverage':'saved historical excerpts', 'data_mode':'synthetic_live', 'model_id':model,
                'demo_services':{'openai_key_configured':bool(os.environ.get('OPENAI_API_KEY')) if model.startswith('openai:') else False,
                                 'langfuse_configured':configured()}}

    def admit(self, owner, case, request):
        profile = self.service.cases.read(owner, case)
        identity = uuid.uuid5(uuid.NAMESPACE_URL, f'vs5-selected:{owner}:{case}:{request.idempotency_key}').hex
        for old in self.service.list(owner, case)['runs']:
            if old['run_id'] == identity:
                saved = self.store.get(owner, case, 'snapshot', old['snapshot_id'])
                if any(saved[field] != getattr(request, field) for field in
                       ('selected_versions', 'selected_obligations', 'assessment_date', 'mode')):
                    raise invalid('idempotency_conflict', 409)
                return old
        if request.mode != 'historical':
            raise CaseError(503, 'freshness_unverified', 'Current source verification is unavailable.',
                            'Select a historical date or wait for current source verification.')
        sources = self._catalog_sources(owner, case)
        selected = []
        for name, version in request.selected_versions.items():
            source = next((s for s in sources if s['document']['source_id']==name and s['document']['version']==version), None)
            if source is None: raise not_found()
            selected.append(source)
        if not any(s['document']['kind'] != 'regulation' for s in selected):
            raise invalid('bank_source_required')
        scopes = {key:ids for s in selected for key,ids in s.get('obligation_scopes', {}).items()}
        if not set(request.selected_obligations) <= scopes.keys():
            raise invalid('selected_scope_unavailable')
        mandatory = {p['passage_id']:p for s in selected for p in s['passages']
            if any(p['passage_id'] in scopes[o] for o in request.selected_obligations)}
        pipeline = AssessmentPipeline(self.service, None)
        pipeline._context(list(mandatory.values()))
        if sum(len(p['text'].encode()) for s in selected for p in s['passages']) > 400_000:
            raise ContractError('source_extraction_limit')
        self._persist_sources(owner, case, selected)
        snapshot = Snapshot(snapshot_id=identity, case_id=case, bank_profile=profile.bank_profile,
            selected_versions=request.selected_versions, selected_obligations=request.selected_obligations,
            selected_document_ids={s['document']['source_id']:s['document']['document_version_id'] for s in selected},
            assessment_date=request.assessment_date, mode=request.mode, prompt_version=PERIOD_PROMPT,
            model_version=selected_model(), synthetic=True)
        pipeline._sources(owner, case, snapshot.model_dump())
        self.store.save_snapshot(owner, snapshot)
        return self.service.reviews.admit(owner, case, identity, identity, 'synthetic_live')

    def _persist_sources(self, owner, case, selected):
        entries = json.loads((self.root / 'data/sources/source-manifest.json').read_text(encoding='utf-8'))['versions']
        for source in selected:
            doc = source['document']
            if doc['kind']=='regulation':
                entry = next(e for e in entries if e['document_id']==doc['source_id'] and e['version_id']==doc['version'])
                self.blobs.put(owner, case, source['original_blob'], self._raw(entry))
            self.store.put(owner, case, 'document', doc['document_version_id'], source)
