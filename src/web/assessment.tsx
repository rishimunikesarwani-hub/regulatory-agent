/// <reference types="vite/client" />
import { useEffect, useRef, useState, type FormEvent } from 'react';
import { authHeaders, type Config } from './auth';
import fixture from '../../data/fixtures/slice-02-policy.txt?raw';

type Citation = { document_version_id: string; passage_id: string; location: string; quote: string };
type Content = { status: string; rationale: string; recommendation: string };
type Finding = { finding_id: string; status: string; rationale: string; primary_recommendation: string; citations: Citation[] };
type Review = { event_id: string; event_kind: string; disposition: string | null; revision: number; reason: string | null; accepted_content: Content | null; committed_at: string; idempotency_key: string };
type Result = {
  job: { job_id: string; state: string; model_calls: number; stop_reason: string | null; unchecked_obligations: string[] }; snapshot: { snapshot_id: string; case_id: string; assessment_date: string; selected_versions: Record<string, string> };
  data_mode: string; freshness: string; findings: Finding[]; reviews: Review[];
  obligation: { requirement: string; applicability: string; conditions: string[]; exceptions: string[]; citations: Citation[] };
  control: { statement: string; frequency: string }; summary: { cutoff: string; eligible: number; reviewed: number; approved: number; edited: number; rejected: number; pending: number; approval_rate: number | null; edit_rate: number | null; rejection_rate: number | null; adoption_rate: number | null; review_coverage: number | null };
  trace: { attempts: { event_id: string; stage: string; state: string; duration_seconds: number | null }[] };
};
type Source = { document: { case_id: string; source_id: string; version: string; document_version_id: string; kind: string; synthetic?: boolean }; label?: string; filename: string; passages: { passage_id: string; location: string; text: string }[] };
type Comparison = { comparison_id: string; case_id: string; data_mode: string; baseline_job_id: string; new_job_id: string | null;
  change_kind: string; obligation_changed: boolean; affected_control_ids: string[]; older_source: Source; newer_source: Source;
  metadata_changes: Record<string, {older: string; newer: string}> };
class AssessmentError extends Error { constructor(readonly status: number, message: string) { super(message); } }
const titles: Record<string, string> = { approved: 'Approved', edited: 'Edited', rejected: 'Rejected', evidence_request: 'Evidence requested', needs_review: 'Needs review' };
const percent = (value: number | null) => value === null ? 'Not measured' : `${Math.round(value * 100)}%`;

export function AssessmentPanel({ config, caseId, documentRevision, onExpired, onState }: {
  config: Config; caseId: string; documentRevision: number; onExpired: (reason: unknown) => boolean; onState: (state: string) => void;
}) {
  const [policies, setPolicies] = useState<Source[]>([]), [policyId, setPolicyId] = useState('');
  const [regulation, setRegulation] = useState('RBI-IT-2023'), [newerVersion, setNewerVersion] = useState('v2-added');
  const [comparisons, setComparisons] = useState<Comparison[]>([]), [comparison, setComparison] = useState<Comparison | null>(null);
  const [runs, setRuns] = useState<{ job_id: string; job_admitted_at: string }[]>([]);
  const [result, setResult] = useState<Result | null>(null), [source, setSource] = useState<Source | null>(null);
  const [busy, setBusy] = useState(false), [uncertain, setUncertain] = useState(false), [error, setError] = useState('');
  const [outcome, setOutcome] = useState('approved'), [reason, setReason] = useState('');
  const [edited, setEdited] = useState<Content>({ status: 'needs_review', rationale: '', recommendation: '' });
  const active = useRef(true), generation = useRef(0), dialog = useRef<HTMLDialogElement>(null);
  const reviewDraft = useRef<{ signature: string; body: object } | null>(null);
  const startDraft = useRef<object | null>(null);
  const comparisonDraft = useRef<{signature: string; body: object} | null>(null);
  const editedFinding = useRef('');
  const root = `${config.api_url}/api/cases/${encodeURIComponent(caseId)}`;

  async function request(path: string, body?: object): Promise<any> {
    const response = await fetch(root + path, { method: body ? 'POST' : 'GET', credentials: 'omit', cache: 'no-store',
      headers: { ...authHeaders(config), ...(body ? { 'Content-Type': 'application/json' } : {}) },
      body: body ? JSON.stringify(body) : undefined, signal: AbortSignal.timeout(20_000) });
    if (response.status === 401) throw new Error('expired');
    const data = await response.json();
    if (!response.ok) throw new AssessmentError(response.status, `${data.message || 'The assessment request could not be confirmed.'} ${data.next_action || 'Refresh assessment before another attempt.'}`);
    return data;
  }
  function failed(cause: unknown): void {
    if (active.current && !onExpired(cause)) setError(cause instanceof AssessmentError ? cause.message : 'The request could not be confirmed. Keep your draft and refresh assessment.');
  }
  async function options(): Promise<void> {
    const [documents, assessments, savedComparisons] = await Promise.all([request('/documents'), request('/assessments'), request('/comparisons')]);
    if (!active.current) return;
    const available = documents.sources.filter((s: Source) => s.document.case_id === caseId && s.document.kind === 'policy');
    setPolicies(available); setPolicyId(current => available.some((s: Source) => s.document.document_version_id === current) ? current : available[0]?.document.document_version_id || '');
    setRuns(assessments.runs);
    if (!Array.isArray(savedComparisons.comparisons) || savedComparisons.comparisons.some((c: Comparison) => c.case_id !== caseId || c.data_mode !== 'controlled_simulation')) throw new Error('invalid_response');
    setComparisons(savedComparisons.comparisons);
    setComparison(current => current || savedComparisons.comparisons.at(-1) || null);
  }
  async function open(job: string): Promise<boolean> {
    const current = ++generation.current;
    setError(''); setBusy(true);
    try {
      const data = await request(`/assessments/${encodeURIComponent(job)}`) as Result;
      if (!active.current || current !== generation.current) return false;
      if (data.snapshot.case_id !== caseId || data.job.job_id !== job || data.data_mode !== 'controlled_simulation' || !Array.isArray(data.findings)) throw new Error('invalid_response');
      setResult(data); onState(data.job.state === 'completed' ? 'Controlled assessment completed' : `Assessment ${data.job.state}`);
      const item = data.findings[0];
      if (item && editedFinding.current !== item.finding_id) {
        editedFinding.current = item.finding_id; reviewDraft.current = null; setReason(''); setOutcome('approved');
        setEdited({ status: item.status, rationale: item.rationale, recommendation: item.primary_recommendation });
      }
      const url = new URL(location.href); url.searchParams.set('assessment', job); history.replaceState(null, '', url.pathname + url.search);
      if (data.job.state === 'queued' || data.job.state === 'running') setTimeout(() => { if (active.current && current === generation.current) void open(job); }, 500);
      return true;
    } catch (cause) { if (current === generation.current) failed(cause); return false; }
    finally { if (active.current && current === generation.current) setBusy(false); }
  }
  async function refresh(): Promise<void> {
    setBusy(true); setError('');
    try {
      await options();
      const job = result?.job.job_id || new URL(location.href).searchParams.get('assessment');
      const confirmed = !job || await open(job);
      if (active.current && confirmed) setUncertain(false);
    } catch (cause) { failed(cause); }
    finally { if (active.current) setBusy(false); }
  }
  useEffect(() => {
    active.current = true; void refresh();
    return () => { active.current = false; generation.current++; };
  }, []);
  useEffect(() => { void options().catch(failed); }, [documentRevision]);
  useEffect(() => { if (source) dialog.current?.showModal(); }, [source]);

  async function start(): Promise<void> {
    const policy = policies.find(s => s.document.document_version_id === policyId);
    if (!policy || busy || uncertain) return;
    setBusy(true); setError('');
    const simulated = regulation === 'SIM-ACCESS';
    const body = startDraft.current || { selected_versions: { [regulation]: simulated ? 'v1' : '2023-11-07', [policy.document.source_id]: policy.document.version },
      selected_obligations: [simulated ? 'SIM-ACCESS-1' : 'RBI-IT-19b'], assessment_date: simulated ? '2024-05-08' : '2024-04-08', mode: 'historical', idempotency_key: crypto.randomUUID() };
    startDraft.current = body;
    try {
      const saved = await request('/assessments', body);
      if (!active.current) return;
      reviewDraft.current = null; setReason(''); setEdited({ status: 'needs_review', rationale: '', recommendation: '' });
      await open(saved.job_id); await options(); startDraft.current = null;
    } catch (cause) {
      if (!(cause instanceof AssessmentError) || cause.status >= 500) setUncertain(true);
      failed(cause);
    } finally { if (active.current) setBusy(false); }
  }
  async function compare(): Promise<void> {
    if (!result || busy || uncertain || result.snapshot.selected_versions['SIM-ACCESS'] !== 'v1') return;
    const body = {older_version_id: 'SIM-ACCESS:v1', newer_version_id: `SIM-ACCESS:${newerVersion}`, snapshot_id: result.snapshot.snapshot_id};
    const signature = JSON.stringify(body);
    if (comparisonDraft.current?.signature !== signature) comparisonDraft.current = {signature, body: {...body, idempotency_key: crypto.randomUUID()}};
    setBusy(true); setError('');
    try {
      const saved = await request('/comparisons', comparisonDraft.current.body) as Comparison;
      if (!active.current) return;
      if (saved.case_id !== caseId || saved.data_mode !== 'controlled_simulation' || saved.baseline_job_id !== result.job.job_id) throw new Error('invalid_response');
      setComparison(saved); await options(); comparisonDraft.current = null;
    } catch (cause) {
      if (!(cause instanceof AssessmentError) || cause.status >= 500) setUncertain(true);
      failed(cause);
    } finally { if (active.current) setBusy(false); }
  }
  async function inspect(citation: Citation): Promise<void> {
    if (!result) return;
    const current = generation.current;
    try {
      const data = await request(`/assessments/${encodeURIComponent(result.job.job_id)}/sources/${encodeURIComponent(citation.document_version_id)}`) as Source;
      if (data.document.case_id !== caseId || data.document.document_version_id !== citation.document_version_id) throw new Error('invalid_response');
      if (active.current && current === generation.current) setSource(data);
    } catch (cause) { failed(cause); }
  }
  async function save(event: FormEvent): Promise<void> {
    event.preventDefault();
    const finding = result?.findings[0];
    if (!result || !finding || busy || uncertain) return;
    const content = outcome === 'approved' ? { status: finding.status, rationale: finding.rationale, recommendation: finding.primary_recommendation } :
      edited;
    const body = { event_kind: outcome === 'evidence_request' ? 'evidence_request' : 'final_review', disposition: outcome === 'evidence_request' ? null : outcome,
      accepted_content: outcome === 'approved' || outcome === 'edited' ? content : null, reason: reason.trim() || null,
      expected_revision: result.reviews.at(-1)?.revision || 0 };
    const signature = JSON.stringify(body);
    if (reviewDraft.current?.signature !== signature) reviewDraft.current = { signature, body: { ...body, idempotency_key: crypto.randomUUID() } };
    setBusy(true); setError('');
    try {
      await request(`/assessments/${encodeURIComponent(result.job.job_id)}/findings/${encodeURIComponent(finding.finding_id)}/reviews`, reviewDraft.current.body);
      await open(result.job.job_id); reviewDraft.current = null;
    } catch (cause) {
      if (!(cause instanceof AssessmentError) || cause.status >= 500) setUncertain(true);
      failed(cause);
    } finally { if (active.current) setBusy(false); }
  }
  const finding = result?.findings[0];
  return <section className="assessment-workspace" aria-labelledby="assessment-heading">
    <div className="page-heading"><div><p className="eyebrow">CONTROLLED EXAMPLE</p><h2 id="assessment-heading">Assessment</h2><p>Review one fictional policy against a selected historical or simulated rule.</p></div>
      <button className="secondary" disabled={busy} onClick={() => void refresh()}>Refresh assessment</button></div>
    {error && <p className="alert" role="alert">{error}</p>}
    <div className="panel assessment-setup"><p>Use the supplied fictional policy. Other documents cannot run this controlled example.</p>
      <p className="field-hint"><a download="slice-02-policy.txt" href={`data:text/plain;charset=utf-8,${encodeURIComponent(fixture)}`}>Download the fictional policy</a>, then upload it as a policy document.</p>
      <label htmlFor="assessment-policy">Policy version</label><select id="assessment-policy" value={policyId} disabled={busy} onChange={e => setPolicyId(e.target.value)}><option value="">Upload a fictional policy first</option>{policies.map(s => <option key={s.document.document_version_id} value={s.document.document_version_id}>{s.filename} · Version {s.document.version}</option>)}</select>
      <label htmlFor="assessment-regulation">Regulatory source</label><select id="assessment-regulation" value={regulation} disabled={busy || uncertain} onChange={e => {setRegulation(e.target.value); startDraft.current = null;}}><option value="RBI-IT-2023">RBI clause 19(b) · historical 2023 version</option><option value="SIM-ACCESS">Simulated access rule · v1</option></select>
      <p className="field-hint">{regulation === 'SIM-ACCESS' ? 'Simulated date: 8 May 2024. These changes are fictional, not RBI amendments.' : 'Historical date: 8 April 2024. Current regulatory status is unverified.'} No live model call is made.</p>
      <button disabled={busy || uncertain || !policyId} onClick={() => void start()}>Run controlled assessment</button>
      {runs.length > 0 && <><label htmlFor="saved-assessment">Saved assessments</label><select id="saved-assessment" disabled={busy} value={result?.job.job_id || ''} onChange={e => { setSource(null); setReason(''); setEdited({status: 'needs_review', rationale: '', recommendation: ''}); reviewDraft.current = null; void open(e.target.value); }}><option value="">Select a saved assessment</option>{runs.map(r => <option key={r.job_id} value={r.job_id}>{new Date(r.job_admitted_at).toLocaleString()} · {r.job_id.slice(0, 8)}</option>)}</select></>}
      {!result && <p className="assessment-notice">{runs.length ? 'Select a saved assessment to inspect its result.' : 'No assessment has run.'}</p>}</div>
    <section className="panel changes-workspace" aria-label="Regulatory changes"><h2>Regulatory changes</h2><span className="badge">Synthetic regulatory simulation</span>
      <p>Compare specified fictional versions. Earlier assessments and human reviews stay unchanged.</p>
      <p className="field-hint">These examples do not establish current regulatory coverage or live model quality.</p>
      {result?.snapshot.selected_versions['SIM-ACCESS'] === 'v1' && result.job.state === 'completed' ? <>
        <p>Older version: SIM-ACCESS:v1 · Selected assessment: {result.job.job_id.slice(0, 8)}</p>
        <label htmlFor="newer-version">Newer version</label><select id="newer-version" value={newerVersion} disabled={busy || uncertain} onChange={e => setNewerVersion(e.target.value)}><option value="v2-added">v2-added · Separate reviewer approval</option><option value="v2-replaced">v2-replaced · Same rule, different wording</option><option value="v2-cosmetic">v2-cosmetic · Punctuation change</option></select>
        <button disabled={busy || uncertain} onClick={() => void compare()}>Compare versions</button>
      </> : <p className="assessment-notice">Run or open a completed simulated v1 assessment to select the earlier version.</p>}
      {comparisons.length > 0 && <><label htmlFor="saved-comparison">Saved comparison</label><select id="saved-comparison" value={comparison?.comparison_id || ''} disabled={busy} onChange={e => setComparison(comparisons.find(c => c.comparison_id === e.target.value) || null)}>{comparisons.map(c => <option key={c.comparison_id} value={c.comparison_id}>{c.older_source.document.version} → {c.newer_source.document.version} · {c.comparison_id.slice(0, 8)}</option>)}</select></>}
      {comparison && <div className="comparison-result"><h3>{({added_requirement: 'Added requirement', wording_only: 'Wording only', appearance_only: 'Appearance only'} as Record<string, string>)[comparison.change_kind]}</h3>
        {comparison.obligation_changed ? <p>Affected control: {comparison.affected_control_ids.join(', ')}. The new assessment needs its own human review.</p> : <p>No changed requirement in this fixed simulation. No new assessment was started.</p>}
        <div className="assessment-grid">{[['Older', comparison.older_source], ['Newer', comparison.newer_source]].map(([label, s]) => {const source = s as Source; return <article className="passage" key={label as string}><h4>{label as string} source · {source.document.document_version_id}</h4><p className="field-hint">{source.label}</p>{source.passages.map(p => <div key={p.passage_id}><h4>{p.location}</h4><pre>{p.text}</pre></div>)}</article>;})}</div>
        <details><summary>Source metadata changes</summary>{Object.entries(comparison.metadata_changes).map(([name, values]) => <p key={name}>{name.replaceAll('_', ' ')}: {values.older} → {values.newer}</p>)}<p>Dates and text changes do not automatically establish a changed obligation.</p></details>
        <div className="citation-actions"><button className="secondary" disabled={busy} onClick={() => void open(comparison.baseline_job_id)}>Open previous assessment</button>{comparison.new_job_id && <button disabled={busy} onClick={() => void open(comparison.new_job_id!)}>Open new assessment</button>}</div>
      </div>}
    </section>
    {result && <section className="assessment-result" aria-label="Assessment result">
      <div className="assessment-result-heading"><span className="badge">Controlled simulation</span><h3>{finding ? titles[finding.status] || finding.status : `Assessment ${result.job.state}`}</h3><p>This is a fixed example. It does not establish compliance or current regulatory coverage.</p>
        {result.job.stop_reason && <p className="alert">Stopped: {result.job.stop_reason.replaceAll('_', ' ')}. Unchecked obligations: {result.job.unchecked_obligations.length}.</p>}
        {['queued', 'running'].includes(result.job.state) && <button className="secondary" disabled={busy} onClick={() => { void request(`/assessments/${encodeURIComponent(result.job.job_id)}/resume`, {}).then(() => open(result.job.job_id)).catch(failed); }}>Resume saved assessment</button>}</div>
      <div className="assessment-grid"><article className="panel"><h3>Requirement and applicability</h3><p>{result.obligation.requirement}</p><p className="assessment-notice">{result.obligation.applicability}</p>
        <h4>Conditions</h4><ul>{result.obligation.conditions.map(c => <li key={c}>{c}</li>)}</ul><h4>Exceptions</h4><ul>{result.obligation.exceptions.map(c => <li key={c}>{c}</li>)}</ul>
        <h4>Policy control</h4><p>{result.control.statement}</p><p className="field-hint">{result.snapshot.selected_versions['SIM-ACCESS'] ? 'Weekly timing belongs to the fictional policy and simulated rule.' : 'Weekly timing is bank policy. RBI does not specify that interval in this clause.'}</p>
        <div className="citation-actions">{result.obligation.citations.map(c => <button className="secondary" key={c.passage_id} onClick={() => void inspect(c)}>Inspect {c.location}</button>)}</div></article>
      {finding && <article className="panel"><h3>Original finding</h3><p className="original-rationale">{finding.rationale}</p><h4>Proposed recommendation</h4><p>{finding.primary_recommendation}</p>
        <div className="citation-actions">{finding.citations.filter(c => !c.document_version_id.startsWith('RBI-') && !c.document_version_id.startsWith('SIM-ACCESS:')).map(c => <button className="secondary" key={c.passage_id} onClick={() => void inspect(c)}>Inspect policy {c.location}</button>)}</div>
        <form onSubmit={e => void save(e)}><fieldset disabled={busy}><legend>Human review</legend><div className="review-options">{['approved', 'edited', 'rejected', 'evidence_request'].map(value => <label key={value}><input type="radio" name="review-outcome" checked={outcome === value} onChange={() => setOutcome(value)} />{value === 'evidence_request' ? 'Request more evidence' : titles[value]}</label>)}</div>
          {outcome === 'edited' && <><label htmlFor="edited-status">Edited finding status</label><select id="edited-status" value={edited.status} onChange={e => setEdited({...edited, status: e.target.value})}>{['needs_review', 'supported', 'partial', 'gap', 'not_applicable'].map(s => <option key={s} value={s}>{s.replaceAll('_', ' ')}</option>)}</select>
            <label htmlFor="edited-rationale">Edited rationale</label><textarea id="edited-rationale" required maxLength={4000} value={edited.rationale} onChange={e => setEdited({...edited, rationale: e.target.value})} />
            <label htmlFor="edited-recommendation">Edited recommendation</label><textarea id="edited-recommendation" required maxLength={4000} value={edited.recommendation} onChange={e => setEdited({...edited, recommendation: e.target.value})} /></>}
          <label htmlFor="review-reason">Review reason</label><textarea id="review-reason" maxLength={4000} required={outcome !== 'approved'} value={reason} onChange={e => setReason(e.target.value)} />
          <button type="submit" disabled={uncertain}>Save review</button></fieldset></form></article>}</div>
      <section className="panel review-summary"><h3>Saved review outcomes</h3><p>Approved: {result.summary.approved} · Edited: {result.summary.edited} · Rejected: {result.summary.rejected} · Pending: {result.summary.pending}</p><p>Eligible: {result.summary.eligible} · Reviewed: {result.summary.reviewed}</p><p>Approval without edits: {percent(result.summary.approval_rate)}</p><p>Edit rate: {percent(result.summary.edit_rate)} · Rejection rate: {percent(result.summary.rejection_rate)}</p><p>Adoption with or without edits: {percent(result.summary.adoption_rate)}</p><p>Review coverage: {percent(result.summary.review_coverage)}</p>
        <p className="field-hint">These figures measure human review decisions. They do not measure correctness. Latest final decisions count at the shown cutoff.</p><p className="field-hint">Cutoff: {result.summary.cutoff} · Definition: d24-v1</p>
        {result.reviews.map(r => <article className="review-event" key={r.event_id}><h4>{titles[r.disposition || r.event_kind]} · Revision {r.revision}</h4>{r.accepted_content && <><p>{r.accepted_content.rationale}</p><p>{r.accepted_content.recommendation}</p></>}{r.reason && <p>Reason: {r.reason}</p>}</article>)}</section>
      <details className="panel run-record"><summary>Saved run record</summary><p className="field-hint">Assessment date: {result.snapshot.assessment_date} · Controlled dispatches: {result.job.model_calls} · Live model calls: 0 · Usage and cost: not measured</p><p className="identifier">Job: {result.job.job_id}</p>
        <ul>{result.trace.attempts.map(t => <li key={t.event_id}>{t.stage.replaceAll('_', ' ')}: {t.state} · {t.duration_seconds === null ? 'Duration unknown' : `${t.duration_seconds.toFixed(4)} s`}</li>)}</ul>
        <p className="identifier">Saved versions: {Object.entries(result.snapshot.selected_versions).map(([id, version]) => `${id}:${version}`).join(', ')}</p></details>
    </section>}
    {source && <dialog ref={dialog} aria-labelledby="assessment-source-title" onClose={() => setSource(null)}><div className="source-heading"><h3 id="assessment-source-title">Assessment source</h3><button className="secondary" onClick={() => dialog.current?.close()}>Close source</button></div><p>{source.filename}</p><p className="field-hint">{source.label || (source.document.kind === 'regulation' ? 'Current status unverified. Saved historical source only.' : 'Saved fictional policy version.')}</p><p className="identifier source-version">Version: {source.document.document_version_id}</p>{source.passages.map(p => <article className="passage" key={p.passage_id}><h4>{p.location}</h4><pre>{p.text}</pre></article>)}</dialog>}
  </section>;
}
