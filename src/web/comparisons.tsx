import { useEffect, useRef, useState, type FormEvent } from 'react';
import { authHeaders, type Config } from './auth';

type Citation={document_version_id:string;passage_id:string;location:string;quote:string};
type Requirement={requirement:string;conditions:string[];exceptions:string[];applicability:string|null;citations:Citation[]};
type Version={document:{case_id:string;source_id:string;version:string;document_version_id:string;publication_date:string;effective_date:string;source_url:string};
  authority:string;filename?:string;passages?:{passage_id:string;location:string;text:string}[]};
type Selection={case_id:string;snapshot_id:string;baseline_job_id:string;assessment_date:string;selected_versions:Record<string,string>;
  selected_obligations:string[];freshness:string;older_versions:Version[];newer_versions:Version[]};
type Summary={comparison_id:string;case_id:string;baseline_job_id:string;older_version_id:string;newer_version_id:string;state:string};
type Comparison={comparison_id:string;case_id:string;snapshot_id:string;baseline_job_id:string;new_job_id:string|null;state:string;freshness:string;
  model_calls:number;unchecked_obligations:string[];older_source:Version;newer_source:Version;assessment_context:Pick<Selection,'assessment_date'|'selected_versions'|'selected_obligations'>;
  result:null|{changes:{obligation_id:string;kind:string;before:Requirement|null;after:Requirement|null;reason:string;basis:Citation[];affected_control_ids:string[]}[];
    assessment_required:boolean;unresolved_obligation_ids:string[];metadata_changes:Record<string,{older:unknown;newer:unknown}>};
  trace:{event_id:string;stage:string;state:string;duration_seconds:number|null;usage:{input_tokens:number|null;output_tokens:number|null}}[]};
type Baseline={job:{job_id:string;state:string};snapshot:{snapshot_id:string;case_id:string}};
class ComparisonError extends Error {constructor(readonly status:number,message:string){super(message);}}
const labels:Record<string,string>={added_requirement:'Added requirement',changed_requirement:'Changed requirement',withdrawn_requirement:'Withdrawn requirement',
  unchanged:'Unchanged requirement',wording_only:'Wording only',appearance_only:'Appearance only',undetermined:'Undetermined'};
const display=(value:unknown)=>value===null?'Unknown':typeof value==='object'?JSON.stringify(value):String(value);
function publicLink(value:string):string|undefined {
  try {const url=new URL(value);if(url.protocol==='https:'&&['rbi.org.in','www.rbi.org.in'].includes(url.hostname)&&
    !url.username&&!url.password&&!url.port&&!url.hash)return url.href;}catch{}
}

export function RegulatoryComparisons({config,caseId,baseline,onOpen,onExpired}:{config:Config;caseId:string;baseline:Baseline;
  onOpen:(job:string)=>Promise<boolean>;onExpired:(reason:unknown)=>boolean}) {
  const [opened,setOpened]=useState(false),[selection,setSelection]=useState<Selection|null>(null),[history,setHistory]=useState<Summary[]>([]);
  const [older,setOlder]=useState(''),[newer,setNewer]=useState(''),[comparison,setComparison]=useState<Comparison|null>(null);
  const [busy,setBusy]=useState(false),[uncertain,setUncertain]=useState(false),[reviewed,setReviewed]=useState(false),[error,setError]=useState('');
  const active=useRef(true),context=useRef(baseline.snapshot.snapshot_id),readSequence=useRef(0);
  const draft=useRef<{signature:string;body:object}|null>(null);
  context.current=baseline.snapshot.snapshot_id;
  const root=`${config.api_url}/api/cases/${encodeURIComponent(caseId)}/regulatory-comparisons`;
  useEffect(()=>{active.current=true;return()=>{active.current=false;readSequence.current++;};},[]);
  useEffect(()=>{setSelection(null);setOlder('');setNewer('');setReviewed(false);},[baseline.snapshot.snapshot_id]);

  async function request(path:string,body?:object):Promise<any> {
    const response=await fetch(root+path,{method:body?'POST':'GET',credentials:'omit',cache:'no-store',
      headers:{...authHeaders(config),...(body?{'Content-Type':'application/json'}:{})},body:body?JSON.stringify(body):undefined,
      signal:AbortSignal.timeout(20_000)});
    if(response.status===401)throw new Error('expired');
    const data=await response.json();
    if(!response.ok)throw new ComparisonError(response.status,`${data.message||'Comparison unavailable.'} ${data.next_action||'Refresh the saved comparison.'}`);
    return data;
  }
  function failed(cause:unknown):void {
    if(active.current&&!onExpired(cause))setError(cause instanceof ComparisonError?cause.message:
      'The comparison request could not be confirmed. Keep your selection and refresh the saved comparison.');
  }
  function validate(data:Comparison):void {
    if(data.case_id!==caseId||data.older_source.document.case_id!==caseId||data.newer_source.document.case_id!==caseId||
      data.freshness!=='unverified'||!Array.isArray(data.unchecked_obligations)||
      !['queued','running','completed','partial','failed'].includes(data.state)||
      data.result?.changes.some(c=>!labels[c.kind]))throw new Error('invalid_comparison');
  }
  function show(data:Comparison,expectedId?:string):void {
    if(expectedId&&data.comparison_id!==expectedId)throw new Error('invalid_comparison');
    validate(data);setComparison(data);setReviewed(false);
    const url=new URL(location.href);url.searchParams.set('comparison',data.comparison_id);window.history.replaceState(null,'',url);
  }
  async function loadOptions():Promise<boolean> {
    const snapshot=baseline.snapshot.snapshot_id;
    const [data,saved]=await Promise.all([request(`/selection?snapshot_id=${encodeURIComponent(snapshot)}`),request('')]);
    if(!active.current||context.current!==snapshot)return false;
    if(data.case_id!==caseId||data.snapshot_id!==snapshot||data.baseline_job_id!==baseline.job.job_id||data.freshness!=='unverified'||
      !Array.isArray(data.older_versions)||!Array.isArray(data.newer_versions)||
      [...data.older_versions,...data.newer_versions].some((v:Version)=>v.document.case_id!==caseId)||
      !Array.isArray(saved.comparisons)||saved.comparisons.some((c:Summary)=>c.case_id!==caseId))throw new Error('invalid_selection');
    const selected=data.older_versions.find((v:Version)=>v.document.document_version_id===older)||data.older_versions[0];
    setSelection(data);setHistory(saved.comparisons);setOlder(selected?.document.document_version_id||'');
    setNewer(current=>data.newer_versions.some((v:Version)=>v.document.document_version_id===current&&
      v.document.source_id===selected?.document.source_id)?current:'');
    return true;
  }
  async function read(id:string):Promise<void> {
    const sequence=++readSequence.current;const data=await request('/'+encodeURIComponent(id)) as Comparison;
    if(active.current&&sequence===readSequence.current)show(data,id);
  }
  async function refresh():Promise<void> {
    setOpened(true);setBusy(true);setError('');
    try {
      // A new assessment can be queued while its previous comparison stays accessible.
      if(baseline.job.state==='completed'&&!await loadOptions())return;
      const id=comparison?.comparison_id||new URL(location.href).searchParams.get('comparison');
      if(id)await read(id);
      if(active.current)setUncertain(false);
    }catch(cause){failed(cause);}finally{if(active.current)setBusy(false);}
  }
  async function compare(event:FormEvent):Promise<void> {
    event.preventDefault();
    if(busy||uncertain||!older||!newer||selection?.snapshot_id!==context.current||baseline.job.state!=='completed')return;
    const body={snapshot_id:selection.snapshot_id,older_version_id:older,newer_version_id:newer},signature=JSON.stringify(body);
    if(draft.current?.signature!==signature)draft.current={signature,body:{...body,idempotency_key:crypto.randomUUID()}};
    setBusy(true);setError('');
    try {
      const saved=await request('',draft.current.body) as Comparison;
      if(!active.current||context.current!==body.snapshot_id)return;
      if(saved.snapshot_id!==body.snapshot_id||saved.baseline_job_id!==baseline.job.job_id||
        saved.older_source.document.document_version_id!==older||saved.newer_source.document.document_version_id!==newer)throw new Error('invalid_comparison');
      show(saved);await loadOptions();draft.current=null;
    }catch(cause){if(!(cause instanceof ComparisonError)||cause.status>=500)setUncertain(true);failed(cause);}
    finally{if(active.current)setBusy(false);}
  }
  async function choose(id:string):Promise<void> {
    if(!id)return;setBusy(true);setError('');
    try{await read(id);}catch(cause){failed(cause);}finally{if(active.current)setBusy(false);}
  }
  async function resume():Promise<void> {
    if(!comparison||busy||uncertain)return;setBusy(true);setError('');
    try{const data=await request('/'+encodeURIComponent(comparison.comparison_id)+'/resume',{}) as Comparison;if(active.current)show(data,comparison.comparison_id);}
    catch(cause){setUncertain(true);failed(cause);}finally{if(active.current)setBusy(false);}
  }
  const canAssess=!!comparison&&!!comparison.assessment_context&&comparison.state==='completed'&&!!comparison.result?.assessment_required&&
    !comparison.result.unresolved_obligation_ids.length&&!comparison.unchecked_obligations.length;
  async function reassess():Promise<void> {
    if(!comparison||!canAssess||!reviewed||busy||uncertain)return;
    const selected=comparison;setBusy(true);setError('');
    try {
      const run=await request('/'+encodeURIComponent(selected.comparison_id)+'/reassess',{selection_reviewed:true});
      if(!active.current)return;
      if(typeof run.job_id!=='string'||!run.job_id)throw new Error('invalid_assessment');
      setComparison(current=>current?.comparison_id===selected.comparison_id?{...current,new_job_id:run.job_id}:current);
      await onOpen(run.job_id);
    }catch(cause){setUncertain(true);failed(cause);}finally{if(active.current)setBusy(false);}
  }
  const old=selection?.older_versions.find(v=>v.document.document_version_id===older);
  const candidates=selection?.newer_versions.filter(v=>v.document.source_id===old?.document.source_id)||[];
  function requirement(label:string,value:Requirement|null) {
    return <div><h4>{label}</h4>{value?<><p>{value.requirement}</p><p>Conditions: {value.conditions.join('; ')||'None stated'}</p>
      <p>Exceptions: {value.exceptions.join('; ')||'None stated'}</p><p>Applicability: {value.applicability||'Unknown'}</p>
      {value.citations.map((c,i)=><blockquote key={i}><p className="identifier">{c.document_version_id} · {c.location}</p><pre>{c.quote}</pre></blockquote>)}</>:
      <p>No requirement interpretation for this side.</p>}</div>;
  }
  return <section className="panel changes-workspace" aria-label="Saved regulatory comparison">
    <div className="source-heading"><h2>Saved regulatory comparison</h2>{opened?
      <button className="secondary" disabled={busy} onClick={()=>void refresh()}>Refresh comparison</button>:
      <button className="secondary" disabled={busy||baseline.job.state!=='completed'} onClick={()=>void refresh()}>Compare regulatory versions</button>}</div>
    {opened&&<><p className="field-hint">Current status unverified. Compare saved historical versions with fictional bank inputs.</p>
      {error&&<p className="alert" role="alert">{error}</p>}
      {selection&&<form onSubmit={event=>void compare(event)}><fieldset disabled={busy||uncertain||selection.snapshot_id!==baseline.snapshot.snapshot_id}>
        <p className="identifier">Baseline assessment: {selection.baseline_job_id} · Date: {selection.assessment_date}</p>
        <label htmlFor="comparison-older">Older saved version</label><select id="comparison-older" value={older} onChange={event=>{setOlder(event.target.value);setNewer('');}}>
          {selection.older_versions.map(v=><option key={v.document.document_version_id} value={v.document.document_version_id}>{v.filename||v.document.source_id} · {v.document.version}</option>)}</select>
        {old&&<p>Published: {old.document.publication_date} · Effective: {old.document.effective_date}</p>}
        <label htmlFor="comparison-newer">Newer saved version</label><select id="comparison-newer" required value={newer} onChange={event=>setNewer(event.target.value)}>
          <option value="">Select a saved version</option>{candidates.map(v=><option key={v.document.document_version_id} value={v.document.document_version_id}>{v.filename||v.document.source_id} · {v.document.version} · Effective {v.document.effective_date}</option>)}</select>
        <button disabled={!newer||baseline.job.state!=='completed'}>Compare saved versions</button>
        {!candidates.length&&<p className="assessment-notice">No other saved regulatory version is available. Source-provider approval and version retrieval are pending.</p>}
      </fieldset></form>}
      {history.length>0&&<><label htmlFor="native-saved-comparison">Saved regulatory comparisons</label><select id="native-saved-comparison" disabled={busy} value={comparison?.comparison_id||''} onChange={event=>void choose(event.target.value)}>
        <option value="">Select a saved comparison</option>{history.map(c=><option key={c.comparison_id} value={c.comparison_id}>{c.comparison_id.slice(0,8)} · {c.state}</option>)}</select></>}
      {comparison&&<div className="comparison-result"><h3>Comparison {comparison.state}</h3>
        <p className="identifier">Previous assessment: {comparison.baseline_job_id}</p>
        {comparison.unchecked_obligations.length>0&&<p>Unchecked obligations: {comparison.unchecked_obligations.join(', ')}</p>}
        {['queued','running'].includes(comparison.state)&&<button className="secondary" disabled={busy||uncertain} onClick={()=>void resume()}>Resume comparison</button>}
        <div className="assessment-grid">{[['Older',comparison.older_source],['Newer',comparison.newer_source]].map(([title,value])=>{
          const version=value as Version,link=publicLink(version.document.source_url);
          return <article className="passage" key={title as string}><h4>{title as string} source</h4><p className="identifier">{version.document.document_version_id} · {version.document.version}</p>
            <p>Published: {version.document.publication_date}<br/>Effective: {version.document.effective_date}</p>
            {link&&<a href={link} target="_blank" rel="noopener noreferrer">Original public source</a>}
            {version.passages?.map(p=><div key={p.passage_id}><h4>{p.location}</h4><pre>{p.text}</pre></div>)}</article>;})}</div>
        {comparison.result&&<>{comparison.result.changes.map(change=><article className="passage" key={change.obligation_id}>
          <h3>{labels[change.kind]}</h3><p className="identifier">Obligation: {change.obligation_id}</p><p>{change.reason}</p>
          <div className="assessment-grid">{requirement('Before requirement',change.before)}{requirement('After requirement',change.after)}</div>
          <p>Affected controls: {change.affected_control_ids.join(', ')||'None established'}</p>
          <details><summary>Comparison basis</summary>{change.basis.map((c,i)=><blockquote key={i}><p className="identifier">{c.document_version_id} · {c.location}</p><pre>{c.quote}</pre></blockquote>)}</details>
        </article>)}
          {comparison.result.unresolved_obligation_ids.length>0&&<p>Unresolved obligations: {comparison.result.unresolved_obligation_ids.join(', ')}</p>}
          <details><summary>Source metadata changes</summary>{Object.entries(comparison.result.metadata_changes).map(([field,values])=><p key={field}>{field.replaceAll('_',' ')}: {display(values.older)} → {display(values.newer)}</p>)}
            <p>Metadata changes do not establish a changed requirement.</p></details>
          <div className="panel"><h3>Review changed selection</h3>
            {comparison.assessment_context&&<><p>Assessment date: {comparison.assessment_context.assessment_date}. Bank document versions and obligation scope stay unchanged.</p>
              <p className="identifier">Selected versions: {Object.entries(comparison.assessment_context.selected_versions).map(([name,version])=>`${name}: ${name===comparison.newer_source.document.source_id?comparison.newer_source.document.version:version}`).join(', ')}</p>
              <p>Selected obligations: {comparison.assessment_context.selected_obligations.join(', ')}</p></>}
            <label className="checkbox-label"><input type="checkbox" disabled={busy||uncertain||!canAssess} checked={reviewed} onChange={event=>setReviewed(event.target.checked)}/>I reviewed the newer version and unchanged assessment inputs.</label>
            <button disabled={busy||uncertain||!canAssess||!reviewed||!!comparison.new_job_id} onClick={()=>void reassess()}>Start new assessment</button>
            {!canAssess&&<p className="field-hint">A completed, applicable requirement change with no unresolved obligations is required.</p>}
          </div></>}
        <div className="citation-actions"><button className="secondary" disabled={busy} onClick={()=>void onOpen(comparison.baseline_job_id)}>Open previous assessment</button>
          {comparison.new_job_id&&<button disabled={busy} onClick={()=>void onOpen(comparison.new_job_id!)}>Open new assessment</button>}</div>
        <details><summary>Comparison execution</summary><p>Model calls: {comparison.model_calls} · Cost: Unknown</p>{comparison.trace.map(a=><p key={a.event_id}>{a.stage.replaceAll('_',' ')} · {a.state} · {a.duration_seconds??'Unknown'} seconds · Input tokens: {a.usage.input_tokens??'Unknown'} · Output tokens: {a.usage.output_tokens??'Unknown'}</p>)}</details>
      </div>}
    </>}
  </section>;
}
