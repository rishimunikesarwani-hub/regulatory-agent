"""Execute frozen fictional inputs in an isolated local OpenAI evaluation database."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import uuid
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
sys.path.insert(0,str(ROOT))

from regulatory_agent.assessments import Assessments
from regulatory_agent.cases import CaseService, SQLiteCases
from regulatory_agent.contracts import CaseRecord, OPENAI_DATED_PROMPT, Snapshot, SourceRead, citation_matches
from regulatory_agent.documents import Documents
from regulatory_agent.evaluation import AssessmentCase, AssessmentResult, CitationCheck, evaluate_assessments
from regulatory_agent.local import BlobStore, Store, encoded
from regulatory_agent.openai_model import MODEL


def inputs(root):
    hashes=json.loads((root/'data/fixtures/freeze-manifest.json').read_text(encoding='utf-8'))['sha256']
    for name,digest in hashes.items():
        if hashlib.sha256((root/name).read_bytes()).hexdigest()!=digest:raise ValueError('frozen_hash_mismatch')
    cases=json.loads((root/'evals/fixtures/held-out-inputs.json').read_bytes())['cases']
    sources=json.loads((root/'data/sources/source-manifest.json').read_bytes())['versions']
    selections=json.loads((root/'evals/fixtures/local-openai-selections.json').read_bytes())['cases']
    from ops.session_a_fixtures import answer_keys
    if list(answer_keys(cases)) or set(selections)!={c['case_id'] for c in cases}:raise ValueError('evaluation_inputs_invalid')
    return cases,sources,selections,hashes


def output_directory(root,path):
    path=path.resolve(); base=(root/'runs/private/openai-evaluations').resolve()
    if not path.is_relative_to(base) or path==base:raise ValueError('evaluation_path_denied')
    path.mkdir(parents=True,exist_ok=False)
    return path


def prepare(root,store,case,entries,clause):
    owner,identity=case['owner_id'],case['case_id']
    profile=case['profile']|{'name':case['profile']['bank_name'],'obligation_scope':case['obligation_scope'],
        'assessment_period_start':case['assessment_period']['start'],'assessment_period_end':case['assessment_period']['end']}
    cases=CaseService(SQLiteCases(store)); documents=Documents(cases); service=Assessments(cases,documents)
    cases.repository.save(CaseRecord(case_id=identity,owner_id=owner,bank_profile=profile,synthetic=True,
        created_at=datetime.now(timezone.utc).isoformat()))
    selected=[]; obligation=None
    regulations=[e|{'kind':'regulation'} for e in entries if case['selected_versions'].get(e['document_id'])==e['version_id']]
    for entry in [*regulations,*case['documents']]:
        if entry.get('owner_id',owner)!=owner or entry.get('case_id',identity)!=identity:raise ValueError('fixture_scope_denied')
        name,version=entry['document_id'],entry['version_id']; key=f'{name}:{version}'
        if case['selected_versions'].get(name)!=version:raise ValueError('fixture_version_denied')
        raw=(root/entry['raw_path']).read_bytes() if entry.get('raw_path') else encoded(entry).encode()
        kind='evidence' if entry['kind']=='untrusted' else entry['kind']
        doc={'document_version_id':key,'case_id':identity,'source_id':name,'version':version,'kind':kind,
            'sha256':hashlib.sha256(raw).hexdigest(),'storage_reference':key,'synthetic':entry['synthetic']}
        if entry['kind']=='regulation':
            doc.update(source_url=entry['source_url'],publication_date=entry['publication_date'],effective_date=entry['effective_date'])
        source={'document':doc,'passages':[{'document_version_id':key,'passage_id':key+':'+p['passage_id'],
            'location':p['locator'],'text':p['text']} for p in entry['passages']], 'filename':name+'.json','format':'fixture-json'}
        if entry['kind']=='untrusted':source['fixture_kind']='untrusted'
        SourceRead.model_validate({k:source[k] for k in ('document','passages')})
        if entry['kind']=='regulation':
            primary=next(p for p in entry['passages'] if p['passage_id']==clause)
            obligation=name+':'+primary['passage_id']
            scope=[key+':'+p['passage_id'] for p in entry['passages'] if p['passage_id'] in ('2a','2ai','2b',clause)]
            source.update(obligation_scopes={obligation:scope},original_blob=key)
            BlobStore(store.path.with_suffix('.sources'),store).put(owner,identity,key,raw)
        else:
            with store.transaction() as db:
                db.execute('INSERT INTO documents VALUES (?,?,?,?,?,?,?)',(key,identity,name,raw,encoded(source),
                    len(source['passages']),sum(len(p['text'].encode()) for p in source['passages'])))
        store.put(owner,identity,'document',key,source); selected.append(source)
    if obligation is None or {s['document']['source_id'] for s in selected}!=case['selected_versions'].keys():
        raise ValueError('fixture_selection_incomplete')
    snapshot_id=uuid.uuid4().hex
    snapshot=Snapshot(snapshot_id=snapshot_id,case_id=identity,bank_profile=profile,
        selected_versions=case['selected_versions'],selected_document_ids={s['document']['source_id']:s['document']['document_version_id'] for s in selected},
        selected_obligations=[obligation],assessment_date=case['assessment_as_of'],mode='historical',
        prompt_version=OPENAI_DATED_PROMPT,model_version=MODEL,synthetic=True)
    store.save_snapshot(owner,snapshot)
    return service,service.reviews.admit(owner,identity,snapshot_id,snapshot_id,'synthetic_live')


def diagnostic_child(database_path,profile,owner,case,job_id,token):
    """Record fixed failure codes after mandatory audit; never capture model or source content."""
    from regulatory_agent.assessment_pipeline import AssessmentPipeline
    from regulatory_agent.assessment_worker import bedrock_child
    from regulatory_agent.contracts import ContractError
    original=AssessmentPipeline._finish_attempt; failures=[]
    allowed={'finding_action_invalid','finding_mapping_invalid','finding_claim_or_remedy_missing',
        'unexamined_or_invalid_citation','claim_citation_not_in_finding','claim_period_invalid',
        'claim_period_unverified','operational_support_unverified','unsupported_control_gap',
        'invalid_model_response','model_dispatch_outcome_unknown','openai_provider_rejected',
        'obligation_extraction_invalid','control_extraction_invalid','model_scope_denied',
        'model_response_incomplete','model_context_limit','inspection_scope_denied'}
    def finish(self,*args,**kwargs):
        result=original(self,*args,**kwargs)
        error=kwargs.get('error')
        if error is not None:
            event=args[-1][0]
            code=str(error) if isinstance(error,ContractError) and str(error) in allowed else 'unclassified_failure'
            failures.append({'stage_id':event.stage_id,'stage':event.stage,'code':code})
            try:
                (Path(database_path).parent/(job_id+'-diagnostic.json')).write_bytes((json.dumps(failures,indent=2)+'\n').encode())
            except OSError:
                pass
        return result
    with patch.object(AssessmentPipeline,'_finish_attempt',finish):
        return bedrock_child(database_path,profile,owner,case,job_id,token)


def score(labels,rows):
    cases=[AssessmentCase(c['case_id'],c['expected_status'],bool(c.get('critical_tags'))) for c in labels]
    results=[AssessmentResult(r['case_id'],r['status'],tuple(CitationCheck(v,None) for v in r.get('citations_resolve',[]))) for r in rows]
    report=evaluate_assessments(cases,results,split='development',execution_mode='live',same_operator_review=True)
    report['citation_support'].update(numerator=None,value=None,status='not_measured')
    return report


def execute(root,path,cases,entries,selections,hashes):
    store=Store(path/'evaluation.sqlite'); rows=[]
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
    receipt={'execution_mode':'live','provider':MODEL,'prompt_version':OPENAI_DATED_PROMPT,'source_commit':head,
        'split':'development','independent_holdout':False,
        'application_working_tree_sha256':{str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted((root/'src/regulatory_agent').glob('*.py'))},
        'harness_working_tree_sha256':{name:hashlib.sha256((root/name).read_bytes()).hexdigest() for name in
            ('ops/run_openai_evaluation.py','evals/fixtures/local-openai-selections.json')},
        'frozen_hashes':hashes,'selection_sha256':hashlib.sha256((root/'evals/fixtures/local-openai-selections.json').read_bytes()).hexdigest(),
        'scope':'Fixed fictional benchmark inputs; historical and simulated regulatory sources',
        'qualified_domain_review':False,'original_bedrock_gate_satisfied':False,'rows':rows}
    for case in cases:
        started=time.monotonic(); row={'case_id':case['case_id'],'status':'error','citations_resolve':[],'job_id':None}
        try:
            service,run=prepare(root,store,case,entries,selections[case['case_id']]); row['job_id']=run['job_id']
            with patch('regulatory_agent.assessment_worker.bedrock_child',diagnostic_child):
                service.run_selected(case['owner_id'],case['case_id'],run['job_id'])
            diagnostic=path/(run['job_id']+'-diagnostic.json')
            if diagnostic.exists():row['failure_details']=json.loads(diagnostic.read_bytes())
            result=service.read(case['owner_id'],case['case_id'],run['job_id'])
            (path/(case['case_id']+'-report.json')).write_bytes((json.dumps(result,indent=2)+'\n').encode())
            row.update(job_state=result['job']['state'],stop_reason=result['job']['stop_reason'],model_calls=result['job']['model_calls'])
            attempts=[a for a in result['trace']['attempts'] if a['operation']=='model']
            row['attempts']=[{k:a.get(k) for k in ('state','dispatched','actual_response_model_id','provider_request_id','usage','errors')} for a in attempts]
            if result['job']['state']=='completed' and len(result['findings'])==1:
                finding=result['findings'][0]; row['status']=finding['status']
                saved=service._sources(case['owner_id'],case['case_id'],result['snapshot'])
                passages={p['passage_id']:p for s in saved for p in s['passages']}
                citations=finding['citations']+[c for claim in finding['claims'] for c in claim['citations']]
                row['citations_resolve']=[citation_matches(c,passages.get(c['passage_id'])) for c in citations]
        except Exception as error:
            row['error_type']=type(error).__name__
        row['elapsed_seconds']=round(time.monotonic()-started,3); rows.append(row)
        (path/'execution.json').write_bytes((json.dumps(receipt,indent=2)+'\n').encode())
        print(json.dumps({k:row.get(k) for k in ('case_id','status','job_state','model_calls','elapsed_seconds')}),flush=True)
    # Read expected answers only after every model execution finishes.
    labels=json.loads((root/'evals/fixtures/held-out-labels.json').read_bytes())['cases']
    receipt['assessment_metrics']=score(labels,rows)
    receipt['limits']=['Claim support needs human context review.','No qualified domain review.','Current source coverage and AWS acceptance remain unverified.','Original Bedrock quality gate remains pending.']
    (path/'execution.json').write_bytes((json.dumps(receipt,indent=2)+'\n').encode())
    return receipt


def main():
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('--run',action='store_true')
    parser.add_argument('--case',action='append',choices=[f'EVAL-{i:02}' for i in range(1,21)])
    parser.add_argument('--env-file',type=Path,default=ROOT/'runs/private/local-demo.env')
    args=parser.parse_args(); cases,entries,selections,hashes=inputs(ROOT)
    if args.case:cases=[c for c in cases if c['case_id'] in args.case]
    if not args.run:
        print(json.dumps({'cases':len(cases),'frozen_hashes_verified':True,'model_calls':0})); return 0
    from ops.run_local_demo import load_environment
    env=load_environment(args.env_file)
    if env.get('MODEL_PROVIDER')!='openai' or not env.get('OPENAI_API_KEY'):raise ValueError('openai_configuration_missing')
    os.environ.update(env)
    os.environ['COMMIT_SHA']=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    path=output_directory(ROOT,ROOT/'runs/private/openai-evaluations'/uuid.uuid4().hex)
    print('Evaluation directory: '+str(path),flush=True)
    execute(ROOT,path,cases,entries,selections,hashes)
    return 0


if __name__=='__main__':raise SystemExit(main())
