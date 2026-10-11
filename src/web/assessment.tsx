/// <reference types="vite/client" />
import { useEffect, useRef, useState, type FormEvent } from 'react';
import { authHeaders, type Config } from './auth';
import { RegulatoryComparisons } from './comparisons';
import fixture from '../../data/fixtures/slice-02-policy.txt?raw';

type Citation = { document_version_id: string; passage_id: string; location: string; quote: string };
type Content = { status: string; rationale: string; recommendation: string };
type Obligation = { obligation_id: string; requirement: string; applicability: string | null; conditions: string[]; exceptions: string[]; citations: Citation[] };
type Control = { control_id: string; statement: string; owner: string | null; frequency: string | null; citations: Citation[] };
type Finding = { finding_id: string; obligation_id: string; control_ids: string[]; status: string; rationale: string; primary_recommendation: string; citations: Citation[];
  evidence_condition: string; gap_kind: string | null; claims?: { obligation_element: string; reason: string; operational: boolean; evidence_period: {start: string; end: string} | null;
    citations: Citation[]; examined_exceptions: Citation[]; conflicting_evidence: Citation[] }[] };
type Review = { event_id: string; finding_id: string; event_kind: string; disposition: string | null; revision: number; reason: string | null; accepted_content: Content | null; committed_at: string; idempotency_key: string };
type Result = {
  job: { job_id: string; state: string; model_calls: number; stop_reason: string | null; unchecked_obligations: string[] }; snapshot: { snapshot_id: string; case_id: string; assessment_date: string; selected_versions: Record<string, string>; selected_obligations: string[]; model_version: string; prompt_version: string };
  data_mode: string; freshness: string; live_model_calls: number | null; findings: Finding[]; reviews: Review[];
  obligation: Obligation | null; control: Control | null; obligations: Obligation[]; controls: Control[];
  summary: { cutoff: string; eligible: number; reviewed: number; approved: number; edited: number; rejected: number; pending: number; approval_rate: number | null; edit_rate: number | null; rejection_rate: number | null; adoption_rate: number | null; review_coverage: number | null };
  trace: { attempts: { event_id: string; stage: string; state: string; duration_seconds: number | null; usage?: {input_tokens: number | null; output_tokens: number | null} }[] };
};
type Source = { document: { case_id: string; source_id: string; version: string; document_version_id: string; kind: string; synthetic?: boolean; publication_date?: string; effective_date?: string; source_url?: string }; label?: string; filename: string; authority?: string; stated_periods?: {period: {start: string; end: string}; citations: Citation[]}[]; passages: { passage_id: string; location: string; text: string }[] };
type Catalog = { sources: Source[]; obligations: {obligation_id: string; document_version_id: string; label: string}[]; freshness: string; current_available: boolean; data_mode: string };
type Comparison = { comparison_id: string; case_id: string; data_mode: string; baseline_job_id: string; new_job_id: string | null;
  change_kind: string; obligation_changed: boolean; affected_control_ids: string[]; older_source: Source; newer_source: Source;
  metadata_changes: Record<string, {older: string; newer: string}> };
class AssessmentError extends Error { constructor(readonly status: number, message: string) { super(message); } }
const titles: Record<string, string> = { approved: 'Approved', edited: 'Edited', rejected: 'Rejected', evidence_request: 'Evidence requested', needs_review: 'Needs review' };
const percent = (value: number | null) => value === null ? 'Not measured' : `${Math.round(value * 100)}%`;
function storageURL(value: unknown): string {
  if (typeof value !== 'string') throw new Error('invalid_storage');
  const target = new URL(value);
  if (target.protocol !== 'https:' || !/^[a-z0-9][a-z0-9.-]*\.s3\.ap-south-1\.amazonaws\.com$/.test(target.hostname) ||
      target.username || target.password || target.port) throw new Error('invalid_storage');
  return target.href;
}
type SourcePage = Source & { offset?: number; passage_count?: number; next_offset?: number | null };

export function AssessmentPanel({ config, caseId, documentRevision, onExpired, onState }: {
  config: Config; caseId: string; documentRevision: number; onExpired: (reason: unknown) => boolean; onState: (state: string) => void;
}) {
  const [policies, setPolicies] = useState<Source[]>([]), [policyId, setPolicyId] = useState('');
  const [regulation, setRegulation] = useState('RBI-IT-2023'), [newerVersion, setNewerVersion] = useState('v2-added');
  const [comparisons, setComparisons] = useState<Comparison[]>([]), [comparison, setComparison] = useState<Comparison | null>(null);
  const [runs, setRuns] = useState<{ job_id: string; job_admitted_at: string }[]>([]);
  const [result, setResult] = useState<Result | null>(null), [source, setSource] = useState<SourcePage | null>(null);
  const [catalog, setCatalog] = useState<Catalog | null>(null), [selectedRegulation, setSelectedRegulation] = useState('');
  const [selectedBanks, setSelectedBanks] = useState<string[]>([]), [selectedClauses, setSelectedClauses] = useState<string[]>([]);
  const [assessmentDate, setAssessmentDate] = useState(''), [findingId, setFindingId] = useState('');
  const [busy, setBusy] = useState(false), [uncertain, setUncertain] = useState(false), [error, setError] = useState('');
  const [outcome, setOutcome] = useState('approved'), [reason, setReason] = useState('');
  const [edited, setEdited] = useState<Content>({ status: 'needs_review', rationale: '', recommendation: '' });
  const active = useRef(true), generation = useRef(0), dialog = useRef<HTMLDialogElement>(null);
  const reviewDraft = useRef<{ signature: string; body: object } | null>(null);
  const startDraft = useRef<object | null>(null);
  const selectedDraft = useRef<{signature: string; body: object} | null>(null);
  const comparisonDraft = useRef<{signature: string; body: object} | null>(null);
  const editedFinding = useRef('');
  const root = `${config.api_url}/api/cases/${encodeURIComponent(caseId)}`;

  const [exporting, setExporting] = useState(false);
  const requestedJob = useRef('');
  async function download(format: 'json' | 'markdown'): Promise<void> {
    if (!result) return;
    const selected = result;
    requestedJob.current = selected.job.job_id;
    setExporting(true); setError('');
    try {
      const response = await fetch(`${root}/assessments/${encodeURIComponent(selected.job.job_id)}/export?cutoff=${encodeURIComponent(selected.summary.cutoff)}`, {
        method: 'POST', credentials: 'omit', cache: 'no-store', headers: {...authHeaders(config), 'Content-Type': 'application/json'},
        body: JSON.stringify({format}), signal: AbortSignal.timeout(20_000),
      });
      if (response.status === 401) throw new Error('expired');
      if (!response.ok) {
        const failure = await response.json();
        throw new AssessmentError(response.status, `${failure.message || 'Export unavailable.'} ${failure.next_action || 'Retry the export.'}`);
      }
      const grant = config.mode === 'aws' ? await response.json() : null;
      const file = config.mode === 'local' ? await response.blob() : null;
      if (!active.current || requestedJob.current !== selected.job.job_id) return;
      const url = file ? URL.createObjectURL(file) : storageURL(grant.url);
      const link = document.createElement('a');
      link.href = url; link.download = `assessment-${selected.job.job_id}.${format === 'json' ? 'json' : 'md'}`;
      document.body.appendChild(link); link.click(); link.remove();
      if (file) window.setTimeout(() => URL.revokeObjectURL(url), 1000);
    } catch (cause) { if (requestedJob.current === selected.job.job_id) failed(cause); }
    finally { if (active.current) setExporting(false); }
  }

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
    const [documents, assessments, savedComparisons, selection] = await Promise.all([request('/documents'), request('/assessments'),
      config.mode === 'local' ? request('/comparisons') : null, request('/assessment-selection')]);
    if (!active.current) return;
    const available = documents.sources.filter((s: Source) => s.document.case_id === caseId && s.document.kind === 'policy');
    setPolicies(available); setPolicyId(current => available.some((s: Source) => s.document.document_version_id === current) ? current : available[0]?.document.document_version_id || '');
    setRuns(assessments.runs);
    if (savedComparisons) {
      if (!Array.isArray(savedComparisons.comparisons) || savedComparisons.comparisons.some((c: Comparison) => c.case_id !== caseId || c.data_mode !== 'controlled_simulation')) throw new Error('invalid_response');
      setComparisons(savedComparisons.comparisons);
      setComparison(current => current || savedComparisons.comparisons.at(-1) || null);
    }
    if (selection) {
      if (selection.data_mode !== 'synthetic_live' || selection.freshness !== 'unverified' || selection.current_available !== false ||
        !Array.isArray(selection.sources) || selection.sources.some((s: Source) => s.document.case_id !== caseId)) throw new Error('invalid_response');
      setCatalog(selection);
      setSelectedRegulation(current => selection.sources.some((s: Source) => s.document.kind === 'regulation' && s.document.document_version_id === current)
        ? current : selection.sources.find((s: Source) => s.document.kind === 'regulation')?.document.document_version_id || '');
    }
  }
  async function open(job: string): Promise<boolean> {
    requestedJob.current = job;
    const current = ++generation.current;
    setError(''); setBusy(true);
    try {
      const data = await request(`/assessments/${encodeURIComponent(job)}`) as Result;
      if (!active.current || current !== generation.current) return false;
      if (data.snapshot.case_id !== caseId || data.job.job_id !== job || !['controlled_simulation', 'synthetic_live'].includes(data.data_mode) || !Array.isArray(data.findings)) throw new Error('invalid_response');
      setResult(data); onState(data.job.state === 'completed' ? (data.data_mode === 'controlled_simulation' ? 'Controlled assessment completed' : 'Selected assessment completed') : `Assessment ${data.job.state}`);
      const item = data.findings.find(f => f.finding_id === editedFinding.current) || data.findings[0];
      setFindingId(item?.finding_id || '');
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
  async function startSelected(event: FormEvent): Promise<void> {
    event.preventDefault();
    const selected = catalog?.sources.filter(s => s.document.document_version_id === selectedRegulation || selectedBanks.includes(s.document.document_version_id)) || [];
    if (busy || uncertain || !assessmentDate || !selectedClauses.length || !selectedBanks.length || selected.length > 10) return;
    const body = {selected_versions: Object.fromEntries(selected.map(s => [s.document.source_id, s.document.version])),
      selected_obligations:selectedClauses, assessment_date:assessmentDate, mode:'historical'};
    const signature = JSON.stringify(body);
    if (selectedDraft.current?.signature !== signature) selectedDraft.current = {signature,body:{...body,idempotency_key:crypto.randomUUID()}};
    setBusy(true); setError('');
    try {
      const saved = await request('/assessments/selected', selectedDraft.current.body);
      if (!active.current) return;
      await open(saved.job_id); await options(); selectedDraft.current = null;
    } catch (cause) {
      if (!(cause instanceof AssessmentError) || cause.status >= 500) setUncertain(true);
      failed(cause);
    } finally { if (active.current) setBusy(false); }
  }
  function chooseFinding(id: string): void {
    const item = result?.findings.find(f => f.finding_id === id);
    if (!item) return;
    editedFinding.current = id; setFindingId(id); reviewDraft.current = null; setReason(''); setOutcome('approved');
    setEdited({status:item.status, rationale:item.rationale, recommendation:item.primary_recommendation});
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
  async function inspect(citation: Pick<Citation, 'document_version_id'>, offset = 0): Promise<void> {
    if (!result) return;
    const current = generation.current;
    try {
      const data = await request(`/assessments/${encodeURIComponent(result.job.job_id)}/sources/${encodeURIComponent(citation.document_version_id)}${config.mode === 'aws' ? `?offset=${offset}` : ''}`) as SourcePage;
      if (data.document.case_id !== caseId || data.document.document_version_id !== citation.document_version_id) throw new Error('invalid_response');
      if (!Array.isArray(data.passages) || (config.mode === 'aws' && (data.offset !== offset || !Number.isInteger(data.passage_count) ||
          data.passage_count! < offset + data.passages.length || (data.next_offset !== null && data.next_offset !== offset + 500)))) throw new Error('invalid_response');
      if (active.current && current === generation.current) setSource(data);
    } catch (cause) { failed(cause); }
  }
  async function save(event: FormEvent): Promise<void> {
    event.preventDefault();
    const finding = result?.findings.find(f => f.finding_id === findingId);
    if (!result || !finding || busy || uncertain) return;
    const content = outcome === 'approved' ? { status: finding.status, rationale: finding.rationale, recommendation: finding.primary_recommendation } :
      edited;
    const body = { event_kind: outcome === 'evidence_request' ? 'evidence_request' : 'final_review', disposition: outcome === 'evidence_request' ? null : outcome,
      accepted_content: outcome === 'approved' || outcome === 'edited' ? content : null, reason: reason.trim() || null,
      expected_revision: Math.max(0, ...result.reviews.filter(r => r.finding_id === finding.finding_id).map(r => r.revision)) };
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
  const finding = result?.findings.find(f => f.finding_id === findingId);
  const obligation = result?.obligations.find(o => o.obligation_id === finding?.obligation_id);
  const controls = result?.controls.filter(c => finding?.control_ids.includes(c.control_id)) || [];
  const controlled = result?.data_mode === 'controlled_simulation';
  const regulatory = catalog?.sources.find(s => s.document.document_version_id === selectedRegulation);
  const bankSources = catalog?.sources.filter(s => s.document.kind !== 'regulation') || [];
  const clauses = catalog?.obligations.filter(o => o.document_version_id === selectedRegulation) || [];
  return <section className="assessment-workspace" aria-labelledby="assessment-heading">
    <div className="page-heading"><div><p className="eyebrow">ASSESSMENT WORKSPACE</p><h2 id="assessment-heading">Assessment</h2><p>{config.mode === 'local' ? 'Select historical scope or open the controlled example.' : 'Select historical scope or open a saved assessment.'}</p></div>
      <button className="secondary" disabled={busy} onClick={() => void refresh()}>Refresh assessment</button></div>
    {error && <p className="alert" role="alert">{error}</p>}
    {catalog && <section className="panel assessment-setup selected-setup" aria-label="Selected historical assessment"><h3>Selected historical assessment</h3>
      <p>Use fictional bank documents with live model processing. AWS model access is required.</p>
      <p className="field-hint">Saved historical excerpts · Current status unverified. Current assessments are unavailable until source verification passes.</p>
      <form onSubmit={e => void startSelected(e)}><fieldset disabled={busy || uncertain}>
        <label htmlFor="selected-regulation">Historical regulation version</label><select id="selected-regulation" value={selectedRegulation} onChange={e => {setSelectedRegulation(e.target.value); setSelectedClauses([]);}}>{catalog.sources.filter(s => s.document.kind === 'regulation').map(s => <option key={s.document.document_version_id} value={s.document.document_version_id}>{s.filename} · {s.document.version}</option>)}</select>
        {regulatory && <p className="field-hint">Authority: {regulatory.authority || 'Unknown'} · Published: {regulatory.document.publication_date || 'Unknown'} · Effective: {regulatory.document.effective_date || 'Unknown'}<br/>
          <a href={regulatory.document.source_url} target="_blank" rel="noopener noreferrer">Original public source</a></p>}
        <fieldset><legend>Bank document versions</legend><p className="field-hint">Select one version per source. Maximum 10 documents, including the regulation.</p>
          {bankSources.length ? bankSources.map(s => <label className="checkbox-label" key={s.document.document_version_id}><input type="checkbox" checked={selectedBanks.includes(s.document.document_version_id)}
            onChange={e => setSelectedBanks(current => e.target.checked ? [...current.filter(id => !bankSources.some(other => other.document.document_version_id === id && other.document.source_id === s.document.source_id)), s.document.document_version_id] : current.filter(id => id !== s.document.document_version_id))}/>{s.filename} · Version {s.document.version}</label>) : <p>Upload a fictional bank document first.</p>}
        </fieldset>
        <fieldset><legend>Regulatory clauses</legend><p className="field-hint">Select up to 20 clauses. Saved applicability and exception passages are included.</p>
          {clauses.map(o => <label className="checkbox-label" key={o.obligation_id}><input type="checkbox" checked={selectedClauses.includes(o.obligation_id)} disabled={selectedClauses.length >= 20 && !selectedClauses.includes(o.obligation_id)}
            onChange={e => setSelectedClauses(current => e.target.checked ? [...current, o.obligation_id] : current.filter(id => id !== o.obligation_id))}/>{o.label}</label>)}
        </fieldset>
        <label htmlFor="selected-date">Assessment date</label><input id="selected-date" type="date" required min={regulatory?.document.effective_date} max={new Date().toISOString().slice(0,10)} value={assessmentDate} onChange={e => setAssessmentDate(e.target.value)}/>
        <p className="field-hint">Selected: {selectedBanks.length + (selectedRegulation ? 1 : 0)} documents · {selectedClauses.length} clauses. Unknown evidence periods stay unknown.</p>
        {selectedBanks.length > 9 && <p className="field-hint">Select fewer bank versions before starting the assessment.</p>}
        <button type="submit" disabled={!selectedRegulation || !selectedBanks.length || selectedBanks.length > 9 || !selectedClauses.length || !assessmentDate}>Run selected assessment with live model</button>
      </fieldset></form></section>}
    {config.mode === 'local' && <div className="panel assessment-setup"><p>Use the supplied fictional policy. Other documents cannot run this controlled example.</p>
      <p className="field-hint"><a download="slice-02-policy.txt" href={`data:text/plain;charset=utf-8,${encodeURIComponent(fixture)}`}>Download the fictional policy</a>, then upload it as a policy document.</p>
      <label htmlFor="assessment-policy">Policy version</label><select id="assessment-policy" value={policyId} disabled={busy} onChange={e => setPolicyId(e.target.value)}><option value="">Upload a fictional policy first</option>{policies.map(s => <option key={s.document.document_version_id} value={s.document.document_version_id}>{s.filename} · Version {s.document.version}</option>)}</select>
      <label htmlFor="assessment-regulation">Regulatory source</label><select id="assessment-regulation" value={regulation} disabled={busy || uncertain} onChange={e => {setRegulation(e.target.value); startDraft.current = null;}}><option value="RBI-IT-2023">RBI clause 19(b) · historical 2023 version</option><option value="SIM-ACCESS">Simulated access rule · v1</option></select>
      <p className="field-hint">{regulation === 'SIM-ACCESS' ? 'Simulated date: 8 May 2024. These changes are fictional, not RBI amendments.' : 'Historical date: 8 April 2024. Current regulatory status is unverified.'} No live model call is made.</p>
      <button disabled={busy || uncertain || !policyId} onClick={() => void start()}>Run controlled assessment</button>
      {runs.length > 0 && <><label htmlFor="saved-assessment">Saved assessments</label><select id="saved-assessment" disabled={busy} value={result?.job.job_id || ''} onChange={e => { setSource(null); setReason(''); setEdited({status: 'needs_review', rationale: '', recommendation: ''}); reviewDraft.current = null; void open(e.target.value); }}><option value="">Select a saved assessment</option>{runs.map(r => <option key={r.job_id} value={r.job_id}>{new Date(r.job_admitted_at).toLocaleString()} · {r.job_id.slice(0, 8)}</option>)}</select></>}
      {!result && <p className="assessment-notice">{runs.length ? 'Select a saved assessment to inspect its result.' : 'No assessment has run.'}</p>}</div>}
    {config.mode === 'aws' && runs.length > 0 && <div className="panel"><label htmlFor="cloud-saved-assessment">Saved assessments</label><select id="cloud-saved-assessment" disabled={busy} value={result?.job.job_id || ''} onChange={e => {setSource(null); void open(e.target.value);}}><option value="">Select a saved assessment</option>{runs.map(r => <option key={r.job_id} value={r.job_id}>{new Date(r.job_admitted_at).toLocaleString()} · {r.job_id.slice(0,8)}</option>)}</select></div>}
    {config.mode === 'local' && <section className="panel changes-workspace" aria-label="Regulatory changes"><h2>Regulatory changes</h2><span className="badge">Synthetic regulatory simulation</span>
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
    </section>}
    {result?.data_mode==='synthetic_live'&&<RegulatoryComparisons config={config} caseId={caseId} baseline={result} onOpen={open} onExpired={onExpired}/>}
    {result && <section className="assessment-result" aria-label="Assessment result">
      <div className="assessment-result-heading"><span className="badge">{controlled ? 'Controlled simulation' : 'Fictional inputs · Live model processing'}</span><h3>{finding ? titles[finding.status] || finding.status : `Assessment ${result.job.state}`}</h3>
        <p>{controlled ? 'This is a fixed example.' : 'This assessment uses selected historical excerpts and fictional bank documents.'} It does not establish compliance or current regulatory coverage.</p>
        {result.job.stop_reason && <p className="alert">Stopped: {result.job.stop_reason.replaceAll('_', ' ')}.</p>}
        <p>Job state: {result.job.state} · Findings: {result.findings.length} · Selected obligations: {result.snapshot.selected_obligations.length}</p>
        <p className="identifier">Unchecked obligations: {result.job.unchecked_obligations.length ? result.job.unchecked_obligations.join(', ') : 'None'}</p>
        {result.findings.length > 1 && <><label htmlFor="selected-finding">Finding</label><select id="selected-finding" value={findingId} disabled={busy || uncertain} onChange={e => chooseFinding(e.target.value)}>{result.findings.map(f => <option key={f.finding_id} value={f.finding_id}>{f.obligation_id} · {titles[f.status] || f.status}</option>)}</select></>}
        {['queued', 'running'].includes(result.job.state) && <button className="secondary" disabled={busy} onClick={() => { void request(`/assessments/${encodeURIComponent(result.job.job_id)}/resume`, {}).then(() => open(result.job.job_id)).catch(failed); }}>Resume saved assessment</button>}</div>
      <div className="assessment-grid">{obligation && <article className="panel"><h3>Requirement and applicability</h3><p>{obligation.requirement}</p><p className="assessment-notice">{obligation.applicability || 'Applicability unknown'}</p>
        <h4>Conditions</h4><ul>{obligation.conditions.map(c => <li key={c}>{c}</li>)}</ul><h4>Exceptions</h4><ul>{obligation.exceptions.map(c => <li key={c}>{c}</li>)}</ul>
        <h4>Mapped controls</h4>{controls.length ? controls.map(c => <div key={c.control_id}><p>{c.statement}</p><p className="field-hint">Owner: {c.owner || 'Unknown'} · Frequency: {c.frequency || 'Unknown'}</p>
          <div className="citation-actions">{c.citations.map(reference => <button className="secondary" key={reference.passage_id} onClick={() => void inspect(reference)}>Inspect control {reference.location}</button>)}</div></div>) : <p>No mapped control.</p>}
        {controlled && <p className="field-hint">{result.snapshot.selected_versions['SIM-ACCESS'] ? 'Weekly timing belongs to the fictional policy and simulated rule.' : 'Weekly timing is bank policy. RBI does not specify that interval in this clause.'}</p>}
        <div className="citation-actions">{obligation.citations.map(c => <button className="secondary" key={c.passage_id} onClick={() => void inspect(c)}>Inspect {c.location}</button>)}</div></article>}
      {finding && <article className="panel"><h3>Original finding</h3><p className="original-rationale">{finding.rationale}</p><h4>Proposed recommendation</h4><p>{finding.primary_recommendation}</p>
        <p className="field-hint">Evidence condition: {finding.evidence_condition} · Gap type: {finding.gap_kind || 'None'}</p>
        {finding.claims?.map((c, index) => <div className="passage" key={index}><h4>{c.obligation_element}</h4><p>{c.reason}</p><p className="field-hint">{c.operational ? 'Operational claim' : 'Documented claim'} · Evidence period: {c.evidence_period ? `${c.evidence_period.start} to ${c.evidence_period.end}` : 'Unknown'}</p>
          <div className="citation-actions">{[['claim', c.citations], ['exception', c.examined_exceptions], ['conflict', c.conflicting_evidence]].map(([label, references]) => (references as Citation[]).map(reference => <button className="secondary" key={`${label}:${reference.passage_id}`} onClick={() => void inspect(reference)}>Inspect {label as string} {reference.location}</button>))}</div></div>)}
        <div className="citation-actions">{finding.citations.filter(c => !obligation?.citations.some(o => o.document_version_id === c.document_version_id && o.passage_id === c.passage_id)).map(c => <button className="secondary" key={c.passage_id} onClick={() => void inspect(c)}>Inspect {c.location}</button>)}</div>
        <form onSubmit={e => void save(e)}><fieldset disabled={busy}><legend>Human review</legend><div className="review-options">{['approved', 'edited', 'rejected', 'evidence_request'].map(value => <label key={value}><input type="radio" name="review-outcome" checked={outcome === value} onChange={() => setOutcome(value)} />{value === 'evidence_request' ? 'Request more evidence' : titles[value]}</label>)}</div>
          {outcome === 'edited' && <><label htmlFor="edited-status">Edited finding status</label><select id="edited-status" value={edited.status} onChange={e => setEdited({...edited, status: e.target.value})}>{['needs_review', 'supported', 'partial', 'gap', 'not_applicable'].map(s => <option key={s} value={s}>{s.replaceAll('_', ' ')}</option>)}</select>
            <label htmlFor="edited-rationale">Edited rationale</label><textarea id="edited-rationale" required maxLength={4000} value={edited.rationale} onChange={e => setEdited({...edited, rationale: e.target.value})} />
            <label htmlFor="edited-recommendation">Edited recommendation</label><textarea id="edited-recommendation" required maxLength={4000} value={edited.recommendation} onChange={e => setEdited({...edited, recommendation: e.target.value})} /></>}
          <label htmlFor="review-reason">Review reason</label><textarea id="review-reason" maxLength={4000} required={outcome !== 'approved'} value={reason} onChange={e => setReason(e.target.value)} />
          <button type="submit" disabled={uncertain}>Save review</button></fieldset></form></article>}</div>
      <section className="panel review-summary"><h3>Saved review outcomes</h3><p>Approved: {result.summary.approved} · Edited: {result.summary.edited} · Rejected: {result.summary.rejected} · Pending: {result.summary.pending}</p><p>Eligible: {result.summary.eligible} · Reviewed: {result.summary.reviewed}</p><p>Approval without edits: {percent(result.summary.approval_rate)}</p><p>Edit rate: {percent(result.summary.edit_rate)} · Rejection rate: {percent(result.summary.rejection_rate)}</p><p>Adoption with or without edits: {percent(result.summary.adoption_rate)}</p><p>Review coverage: {percent(result.summary.review_coverage)}</p>
        <p className="field-hint">These figures measure human review decisions for this assessment only. They do not measure correctness. Latest final decisions count at the shown cutoff.</p><p className="field-hint">Cutoff: {result.summary.cutoff} · Definition: d24-v1</p>
        {finding && <section aria-label="Selected finding review history"><h4>Selected finding review history</h4>{result.reviews.filter(r => r.finding_id === finding.finding_id).map(r => <article className="review-event" key={r.event_id}><h4>{titles[r.disposition || r.event_kind]} · Revision {r.revision}</h4>{r.accepted_content && <><p>{r.accepted_content.rationale}</p><p>{r.accepted_content.recommendation}</p></>}{r.reason && <p>Reason: {r.reason}</p>}</article>)}</section>}</section>
      <section className="panel" aria-label="Export assessment"><h3>Export assessment</h3>
        <p>Download the saved versions, source passages, findings, and human reviews at the displayed cutoff.</p>
        <p className="field-hint">{controlled ? 'Controlled simulation.' : 'Fictional inputs with live model processing.'} Current regulatory status is unverified. The report keeps its job state and unchecked scope. Cost remains unknown.</p>
        <div className="source-heading"><button className="secondary" disabled={busy || exporting} onClick={() => void download('json')}>Download JSON</button>
          <button className="secondary" disabled={busy || exporting} onClick={() => void download('markdown')}>Download Markdown</button></div>
        {exporting && <p role="status">Preparing export…</p>}
      </section>
      <details className="panel run-record"><summary>Saved run record</summary><p className="field-hint">Assessment date: {result.snapshot.assessment_date} · {controlled ? `Controlled dispatches: ${result.job.model_calls} · ` : ''}Live model calls: {result.live_model_calls ?? 'Unknown'} · Cost: Unknown</p><p className="identifier">Job: {result.job.job_id}</p>
        <p className="identifier">Model: {result.snapshot.model_version} · Prompt: {result.snapshot.prompt_version}</p>
        <ul>{result.trace.attempts.map(t => <li key={t.event_id}>{t.stage.replaceAll('_', ' ')}: {t.state} · {t.duration_seconds === null ? 'Duration unknown' : `${t.duration_seconds.toFixed(4)} s`} · Input tokens: {t.usage?.input_tokens ?? 'Unknown'} · Output tokens: {t.usage?.output_tokens ?? 'Unknown'}</li>)}</ul>
        <p className="identifier">Saved versions: {Object.entries(result.snapshot.selected_versions).map(([id, version]) => `${id}:${version}`).join(', ')}</p></details>
    </section>}
    {source && <dialog ref={dialog} aria-labelledby="assessment-source-title" onClose={() => setSource(null)}><div className="source-heading"><h3 id="assessment-source-title">Assessment source</h3><button className="secondary" onClick={() => dialog.current?.close()}>Close source</button></div><p>{source.filename}</p><p className="field-hint">{source.label || (source.document.kind === 'regulation' ? 'Current status unverified. Saved historical source only.' : 'Saved fictional bank document version.')}</p><p className="identifier">Source: {source.document.source_id} · Version: {source.document.version} · Kind: {source.document.kind}</p><p className="identifier source-version">Document: {source.document.document_version_id}</p>{source.document.kind === 'evidence' && source.stated_periods !== undefined && <section aria-label="Stated evidence periods"><h4>Stated evidence periods</h4><p className="field-hint">These dates do not establish complete records or actual control operation.</p>{source.stated_periods.length ? source.stated_periods.map((v,i) => <article className="passage" key={i}><h4>{v.period.start} to {v.period.end}</h4>{v.citations.map(c => <blockquote key={c.passage_id}><p>{c.location}</p><pre>{c.quote}</pre></blockquote>)}</article>) : <p>Stated evidence period: Unknown</p>}</section>}{source.passages.map(p => <article className="passage" key={p.passage_id}><h4>{p.location}</h4><pre>{p.text}</pre></article>)}{config.mode === 'aws' && <div className="source-heading"><p>Passages {(source.offset || 0) + 1} to {(source.offset || 0) + source.passages.length} of {source.passage_count}</p><button className="secondary" disabled={!source.offset} onClick={() => void inspect(source.document, Math.max(0, source.offset! - 500))}>Previous source passages</button><button className="secondary" disabled={source.next_offset === null} onClick={() => void inspect(source.document, source.next_offset!)}>Next source passages</button></div>}</dialog>}
  </section>;
}
