import { useEffect, useRef, useState, type FormEvent } from 'react';
import { authHeaders, type Config } from './auth';

type Source = {
  document: { document_version_id: string; source_id: string; case_id: string; kind: string; version: string; sha256: string; synthetic: true };
  filename: string;
  format: string;
  units: number;
  uploaded_at: string;
};
type Evidence = Source & { passages: { passage_id: string; location: string; text: string }[] };
class DocumentError extends Error {
  constructor(readonly status: number, message: string) { super(message); }
}

export function DocumentsPanel({ config, caseId, onExpired }: { config: Config; caseId: string; onExpired: (reason: unknown) => boolean }) {
  const [sources, setSources] = useState<Source[]>([]);
  const [evidence, setEvidence] = useState<Evidence | null>(null);
  const [file, setFile] = useState<File | null>(null);
  const [kind, setKind] = useState('policy');
  const [replacement, setReplacement] = useState('');
  const [fictional, setFictional] = useState(false);
  const [busy, setBusy] = useState(false);
  const [loading, setLoading] = useState(true);
  const [uncertain, setUncertain] = useState(false);
  const [error, setError] = useState('');
  const [notice, setNotice] = useState('');
  const fileInput = useRef<HTMLInputElement>(null);
  const requestId = useRef(0);
  const active = useRef(true);
  const root = `${config.api_url}/api/cases/${encodeURIComponent(caseId)}/documents`;

  async function request(path = '', options: RequestInit = {}): Promise<Response> {
    const response = await fetch(root + path, { ...options, cache: 'no-store', credentials: 'omit',
      signal: AbortSignal.timeout(20_000), headers: { ...authHeaders(config), ...options.headers } });
    if (response.status === 401) throw new Error('expired');
    if (!response.ok) {
      const detail = await response.json().catch(() => ({}));
      const message = typeof detail.message === 'string' ? detail.message : 'The document is invalid.';
      const next = typeof detail.next_action === 'string' ? ` ${detail.next_action}` : '';
      throw new DocumentError(response.status, response.status === 422 || response.status === 413 ? message + next : 'The source is unavailable. Refresh documents and try again.');
    }
    return response;
  }

  function failed(reason: unknown, fallback: string): void {
    if (active.current && !onExpired(reason)) setError(reason instanceof DocumentError ? reason.message : fallback);
  }

  async function inspect(id: string): Promise<void> {
    const current = ++requestId.current;
    setError('');
    try {
      const source = await (await request(`/${encodeURIComponent(id)}`)).json() as Evidence;
      if (source.document?.case_id !== caseId || source.document.document_version_id !== id || source.document.synthetic !== true ||
          !Array.isArray(source.passages) || source.passages.some(p => typeof p.text !== 'string' || typeof p.location !== 'string')) throw new Error('The source response is invalid. Refresh documents.');
      if (!active.current || current !== requestId.current) return;
      setEvidence(source);
      const url = new URL(location.href);
      url.searchParams.set('source', id);
      history.replaceState(null, '', url.pathname + url.search);
    } catch (reason) { if (current === requestId.current) failed(reason, 'Could not open the source. Try again.'); }
  }

  async function refresh(resume = false): Promise<void> {
    setLoading(true);
    setError('');
    try {
      const result = await (await request()).json() as { sources: Source[] };
      if (!Array.isArray(result.sources) || result.sources.some(s => s.document?.case_id !== caseId || s.document.synthetic !== true)) throw new Error('The document list is unavailable. Try again.');
      if (!active.current) return;
      setSources(result.sources);
      setUncertain(false);
      const id = resume ? new URL(location.href).searchParams.get('source') : null;
      if (id) await inspect(id);
    } catch (reason) { failed(reason, 'Could not load documents. Try again.'); }
    finally { if (active.current) setLoading(false); }
  }

  useEffect(() => {
    active.current = true;
    void refresh(true);
    return () => { active.current = false; requestId.current++; };
  }, []);

  async function upload(event: FormEvent): Promise<void> {
    event.preventDefault();
    if (!file || !fictional || busy || uncertain) return;
    if (file.size > 10_000_000) { setError('The file exceeds the 10 MB limit. Use a smaller document.'); return; }
    setBusy(true); setError(''); setNotice('');
    try {
      const saved = await (await request('', { method: 'POST', body: file, headers: {
        'Content-Type': 'application/octet-stream', 'X-Filename': encodeURIComponent(file.name),
        'X-Document-Kind': kind, 'X-Synthetic': 'true', ...(replacement ? { 'X-Source-Id': replacement } : {}),
      } })).json() as Evidence;
      if (!active.current) return;
      setFile(null); setFictional(false);
      if (fileInput.current) fileInput.current.value = '';
      await refresh();
      await inspect(saved.document.document_version_id);
      setNotice('Document saved. Earlier versions remain available.');
    } catch (reason) {
      // An interrupted POST might have saved. Require a list refresh before retrying.
      if (!(reason instanceof DocumentError) || reason.status >= 500) setUncertain(true);
      failed(reason, 'The upload could not be confirmed. Refresh documents before you try again.');
    } finally { if (active.current) setBusy(false); }
  }

  async function download(): Promise<void> {
    if (!evidence || busy) return;
    setBusy(true); setError('');
    try {
      const response = await request(`/${encodeURIComponent(evidence.document.document_version_id)}/original`);
      const blob = await response.blob();
      if (!active.current) return;
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url; link.download = evidence.filename;
      link.click();
      setTimeout(() => URL.revokeObjectURL(url), 1000);
    } catch (reason) { failed(reason, 'Could not download the original. Try again.'); }
    finally { if (active.current) setBusy(false); }
  }

  const latest = sources.filter((s, index) => sources.findIndex(other => other.document.source_id === s.document.source_id) === index);
  return <section className="document-workspace" aria-labelledby="documents-heading">
    <div className="page-heading"><div><p className="eyebrow">SOURCE DOCUMENTS</p><h2 id="documents-heading">Documents</h2><p>Keep the original file and inspect its extracted text.</p></div>
      <button className="secondary" disabled={busy || loading} onClick={() => void refresh()}>Refresh documents</button></div>
    {error && <p className="alert" role="alert">{error}{uncertain && ' Refresh documents before you upload again.'}</p>}
    {notice && <p className="success" role="status">{notice}</p>}
    <div className="document-layout"><div className="document-controls"><section className="panel" aria-labelledby="upload-heading">
      <h3 id="upload-heading">Upload a fictional document</h3><p className="field-hint">Text PDF, DOCX, TXT, or CSV. Maximum 10 MB per file and 10 saved versions per case.</p>
      <form onSubmit={event => void upload(event)}><fieldset disabled={busy || loading}>
        <label htmlFor="document-file">Document file</label><input id="document-file" type="file" accept=".pdf,.docx,.txt,.csv" ref={fileInput} required onChange={event => setFile(event.target.files?.[0] ?? null)} />
        <label htmlFor="document-kind">Document role</label><select id="document-kind" value={kind} onChange={event => setKind(event.target.value)}>
          <option value="profile">Bank profile</option><option value="policy">Policy</option><option value="control">Control</option><option value="evidence">Evidence</option></select>
        <label htmlFor="replace-source">Replace source</label><select id="replace-source" value={replacement} onChange={event => setReplacement(event.target.value)}>
          <option value="">New source</option>{latest.map(s => <option key={s.document.source_id} value={s.document.source_id}>{s.filename}</option>)}</select>
        <p className="field-hint">A replacement adds a version. It keeps the earlier version.</p>
        <label className="checkbox-label"><input type="checkbox" checked={fictional} onChange={event => setFictional(event.target.checked)} /><span>I confirm this document contains fictional data only.</span></label>
        <button className="full-width" type="submit" disabled={!file || !fictional || uncertain || sources.length >= 10}>{busy ? 'Saving document…' : 'Upload fictional document'}</button>
        {sources.length >= 10 && <p className="field-hint">This case has reached its 10-version limit.</p>}
      </fieldset></form></section>
      <section className="panel source-list" aria-labelledby="saved-documents-heading"><h3 id="saved-documents-heading">Saved versions <span className="count">{sources.length}</span></h3>
        {loading ? <p role="status">Loading documents…</p> : sources.length === 0 ? <p>No documents yet. Upload a fictional source to inspect it.</p> : sources.map(s =>
          <button className="source-button" key={s.document.document_version_id} aria-pressed={evidence?.document.document_version_id === s.document.document_version_id}
            aria-label={`Inspect ${s.filename} version ${s.document.version}`} disabled={busy} onClick={() => void inspect(s.document.document_version_id)}>
            <strong>{s.filename}</strong><span>{s.document.kind} · Version {s.document.version} · {s.format.toUpperCase()}</span></button>)}
      </section></div>
      <section className="panel source-evidence" aria-labelledby="source-evidence-heading"><h3 id="source-evidence-heading">Source evidence</h3>
        {!evidence ? <div className="source-empty"><p>Select a saved version to inspect its text and source locations.</p></div> : <>
          <div className="source-heading"><div><h3>{evidence.filename}</h3><p>Version {evidence.document.version} · {evidence.document.kind} · {evidence.format.toUpperCase()}</p></div>
            <button className="secondary" disabled={busy} onClick={() => void download()}>Download original</button></div>
          <p className="field-hint">Extracted text can omit images and visual table structure. Use the original file to check them.</p>
          <p className="identifier source-version">Version ID: {evidence.document.document_version_id}</p>
          <details className="source-version"><summary>Content hash (SHA-256)</summary><p className="identifier">{evidence.document.sha256}</p></details>
          <div className="passages">{evidence.passages.map(p => <article className="passage" key={p.passage_id}><h4>{p.location}</h4><pre>{p.text}</pre></article>)}</div>
        </>}
      </section></div>
    <p className="assessment-notice">No assessment has run.</p>
  </section>;
}
