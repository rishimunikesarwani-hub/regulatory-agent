import { useEffect, useRef, useState, type FormEvent } from 'react';
import { authHeaders, type Config } from './auth';

type Source = {
  document: { document_version_id: string; source_id: string; case_id: string; kind: string; version: string; sha256: string; synthetic: true };
  filename: string;
  format: string;
  units: number;
  uploaded_at: string;
};
type Evidence = Source & { passages: { passage_id: string; location: string; text: string }[];
  offset?: number; passage_count?: number; next_offset?: number | null };
type UploadMetadata = { filename: string; kind: string; size_bytes: number; synthetic: true; source_id?: string };
type UploadStatus = { upload_id: string; state: 'reserved' | 'uploaded' | 'finalized' | 'failed' | 'cancelled';
  request?: UploadMetadata; document?: Source['document']; error?: string };
type Grant = UploadStatus & { authorization?: { upload_id: string; destination: string; expires_at: string; eligible_for_assessment: false }; fields?: Record<string, string> };
class DocumentError extends Error {
  constructor(readonly status: number, message: string) { super(message); }
}

export function DocumentsPanel({ config, caseId, onExpired, onUploaded }: { config: Config; caseId: string; onExpired: (reason: unknown) => boolean; onUploaded?: () => void }) {
  const [sources, setSources] = useState<Source[]>([]);
  const [evidence, setEvidence] = useState<Evidence | null>(null);
  const [files, setFiles] = useState<File[]>([]);
  const file = files[0] ?? null;
  const [kind, setKind] = useState('policy');
  const [replacement, setReplacement] = useState('');
  const [fictional, setFictional] = useState(false);
  const [busy, setBusy] = useState(false);
  const [loading, setLoading] = useState(true);
  const [uncertain, setUncertain] = useState(false);
  const [error, setError] = useState('');
  const [notice, setNotice] = useState('');
  const [pending, setPending] = useState<{ key: string; id?: string; request?: UploadMetadata } | null>(null);
  const pendingNow = useRef(pending);
  const fileInput = useRef<HTMLInputElement>(null);
  const requestId = useRef(0);
  const active = useRef(true);
  const root = `${config.api_url}/api/cases/${encodeURIComponent(caseId)}/documents`;

  async function request(path = '', options: RequestInit = {}, uploads = false): Promise<Response> {
    const response = await fetch((uploads ? root.replace(/\/documents$/, '/uploads') : root) + path, { ...options, cache: 'no-store', credentials: 'omit',
      signal: AbortSignal.timeout(uploads && path.endsWith('/finalize') ? 30_000 : 20_000), headers: { ...authHeaders(config), ...options.headers } });
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

  async function inspect(id: string, offset = 0): Promise<void> {
    const current = ++requestId.current;
    setError('');
    try {
      const source = await (await request(`/${encodeURIComponent(id)}${offset ? `?offset=${offset}` : ''}`)).json() as Evidence;
      if (source.document?.case_id !== caseId || source.document.document_version_id !== id || source.document.synthetic !== true ||
          !Array.isArray(source.passages) || source.passages.some(p => typeof p.text !== 'string' || typeof p.location !== 'string') ||
          (config.mode === 'aws' && (source.offset !== offset || !Number.isInteger(source.passage_count) || source.passage_count! < source.passages.length ||
            (source.next_offset !== null && source.next_offset !== offset + 500)))) throw new Error('The source response is invalid. Refresh documents.');
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
      if (resume && config.mode === 'aws') {
        const url = new URL(location.href);
        const uploadId = url.searchParams.get('upload'), key = url.searchParams.get('uploadKey');
        if (uploadId || key) { pendingNow.current = { key: key || '', id: uploadId || undefined }; setPending(pendingNow.current); setUncertain(true); }
      }
      if (id) await inspect(id);
    } catch (reason) { failed(reason, 'Could not load documents. Try again.'); }
    finally { if (active.current) setLoading(false); }
  }

  useEffect(() => {
    active.current = true;
    void refresh(true);
    return () => { active.current = false; requestId.current++; };
  }, []);

  function savePending(value: { key: string; id?: string; request?: UploadMetadata } | null): void {
    pendingNow.current = value; setPending(value);
    const url = new URL(location.href);
    for (const name of ['upload', 'uploadKey']) url.searchParams.delete(name);
    if (value?.id) url.searchParams.set('upload', value.id);
    if (value?.key) url.searchParams.set('uploadKey', value.key);
    history.replaceState(null, '', url.pathname + url.search);
  }

  async function confirmed(document: Source['document'], reset = true): Promise<void> {
    if (document.case_id !== caseId || document.synthetic !== true || !document.document_version_id) throw new Error('invalid_upload');
    if (!active.current) return;
    savePending(null); setUncertain(false);
    if (reset) {
      setFiles(files.slice(1));
      if (files.length <= 1) { setFictional(false); if (fileInput.current) fileInput.current.value = ''; }
    }
    await refresh(); await inspect(document.document_version_id);
    onUploaded?.();
    setNotice('Document saved. Earlier versions remain available.');
  }

  async function cloudUpload(metadata: UploadMetadata, key: string, selectedFile = file, batch = false): Promise<void> {
    savePending({ key, id: pendingNow.current?.key === key ? pendingNow.current.id : undefined, request: metadata });
    const grant = await (await request('', { method: 'POST', body: JSON.stringify(metadata),
      headers: { 'Content-Type': 'application/json', 'Idempotency-Key': key } }, true)).json() as Grant;
    if (!/^[A-Za-z0-9][A-Za-z0-9_.:-]{0,127}$/.test(grant.upload_id)) throw new Error('invalid_upload');
    savePending({ key, id: grant.upload_id, request: metadata });
    if (grant.state === 'finalized' && grant.document) { await confirmed(grant.document, !batch); return; }
    if (grant.state === 'uploaded') {
      const result = await (await request(`/${encodeURIComponent(grant.upload_id)}/finalize`, { method: 'POST' }, true)).json() as UploadStatus;
      if (!result.document) throw new Error('invalid_upload');
      await confirmed(result.document, !batch); return;
    }
    const authorization = grant.authorization;
    if (grant.state !== 'reserved' || !authorization || authorization.upload_id !== grant.upload_id ||
      authorization.eligible_for_assessment !== false || !grant.fields || !selectedFile) throw new Error('invalid_upload');
    const destination = new URL(authorization.destination);
    if (destination.protocol !== 'https:' || !/^[a-z0-9][a-z0-9.-]*\.s3\.ap-south-1\.amazonaws\.com$/.test(destination.hostname) ||
      destination.username || destination.password || destination.search || destination.hash ||
      !Number.isFinite(Date.parse(authorization.expires_at)) || Date.parse(authorization.expires_at) <= Date.now()) throw new Error('invalid_storage');
    const form = new FormData();
    for (const [name, value] of Object.entries(grant.fields)) {
      if (typeof value !== 'string' || name === 'file') throw new Error('invalid_storage');
      form.append(name, value);
    }
    form.append('file', selectedFile);
    const transfer = await fetch(destination.href, { method: 'POST', body: form, credentials: 'omit', signal: AbortSignal.timeout(60_000) });
    if (!transfer.ok) throw new Error('upload_transfer');
    const result = await (await request(`/${encodeURIComponent(grant.upload_id)}/finalize`, { method: 'POST' }, true)).json() as UploadStatus;
    if (!result.document) throw new Error('invalid_upload');
    await confirmed(result.document, !batch);
  }

  async function checkUpload(cancel = false): Promise<void> {
    if (!pending?.id || busy) return;
    setBusy(true); setError('');
    try {
      const status = await (await request(`/${encodeURIComponent(pending.id)}${cancel ? '/cancel' : ''}`,
        cancel ? { method: 'POST' } : {}, true)).json() as UploadStatus;
      if (status.upload_id !== pending.id) throw new Error('invalid_upload');
      if (status.state === 'finalized' && status.document) await confirmed(status.document);
      else if (status.state === 'uploaded') {
        const result = await (await request(`/${encodeURIComponent(pending.id)}/finalize`, { method: 'POST' }, true)).json() as UploadStatus;
        if (!result.document) throw new Error('invalid_upload');
        await confirmed(result.document);
      } else if (status.state === 'reserved' && status.request) {
        savePending({ ...pending, request: status.request });
        setNotice(`The upload is unfinished. Select ${status.request.filename} and resume, or cancel the upload.`);
      } else if (status.state === 'failed' || status.state === 'cancelled') {
        savePending(null); setUncertain(false); setNotice('The upload was not saved. You can try again.');
      } else throw new Error('invalid_upload');
    } catch (reason) { failed(reason, 'Could not confirm the upload. Check its status before another upload.'); }
    finally { if (active.current) setBusy(false); }
  }

  async function resumeUpload(): Promise<void> {
    if (!pending || !file || !fictional || busy) return;
    const metadata = pending.request || { filename: file.name, kind, size_bytes: file.size, synthetic: true,
      ...(replacement ? { source_id: replacement } : {}) };
    if (file.name !== metadata.filename || file.size !== metadata.size_bytes) { setError('Select the same file name and size to resume.'); return; }
    setBusy(true); setError('');
    try { await cloudUpload(metadata, pending.key); }
    catch (reason) { setUncertain(true); failed(reason, 'The upload could not be confirmed. Check its status before another upload.'); }
    finally { if (active.current) setBusy(false); }
  }

  async function upload(event: FormEvent): Promise<void> {
    event.preventDefault();
    if (!file || !fictional || busy || uncertain) return;
    if (replacement && files.length > 1) { setError('Select one file to replace a source.'); return; }
    if (files.length > 10 - sources.length) { setError(`Select at most ${10 - sources.length} remaining files for this case.`); return; }
    if (files.some(f => f.size > 10_000_000)) { setError('A file exceeds the 10 MB limit. Use smaller documents.'); return; }
    setBusy(true); setError(''); setNotice('');
    const selected = [...files]; let savedCount = 0;
    try {
      for (const selectedFile of selected) {
        setNotice(`Saving ${savedCount + 1} of ${selected.length}: ${selectedFile.name}`);
        if (config.mode === 'aws') {
          await cloudUpload({ filename: selectedFile.name, kind, size_bytes: selectedFile.size, synthetic: true,
            ...(replacement ? { source_id: replacement } : {}) }, crypto.randomUUID(), selectedFile, true);
        } else {
          const saved = await (await request('', { method: 'POST', body: selectedFile, headers: {
            'Content-Type': 'application/octet-stream', 'X-Filename': encodeURIComponent(selectedFile.name),
            'X-Document-Kind': kind, 'X-Synthetic': 'true', ...(replacement ? { 'X-Source-Id': replacement } : {}),
          } })).json() as Evidence;
          await confirmed(saved.document, false);
        }
        if (!active.current) return;
        savedCount++; setFiles(selected.slice(savedCount));
      }
      setFictional(false);
      if (fileInput.current) fileInput.current.value = '';
      setNotice(selected.length === 1 ? 'Document saved. Earlier versions remain available.' : `${savedCount} documents saved. Earlier versions remain available.`);
    } catch (reason) {
      // An interrupted POST might have saved. Require a list refresh before retrying.
      if (config.mode === 'aws' && reason instanceof DocumentError && reason.status < 500 && !pendingNow.current?.id) savePending(null);
      if (!(reason instanceof DocumentError) || reason.status >= 500) setUncertain(true);
      setFiles(selected.slice(savedCount));
      setNotice(`${savedCount} of ${selected.length} files confirmed. Remaining files: ${selected.slice(savedCount).map(f => f.name).join(', ')}.`);
      const message = reason instanceof DocumentError ? reason.message : 'The upload could not be confirmed. Refresh documents before you try again.';
      if (active.current && !onExpired(reason)) setError(`${savedCount} of ${selected.length} files confirmed. ${message}`);
    } finally { if (active.current) setBusy(false); }
  }

  async function download(): Promise<void> {
    if (!evidence || busy) return;
    setBusy(true); setError('');
    try {
      const response = await request(`/${encodeURIComponent(evidence.document.document_version_id)}/original`);
      const blob = config.mode === 'local' ? await response.blob() : null;
      if (!active.current) return;
      let url: string;
      if (blob) url = URL.createObjectURL(blob);
      else {
        const result = await response.json() as { url: string };
        const target = new URL(result.url);
        if (target.protocol !== 'https:' || !/^[a-z0-9][a-z0-9.-]*\.s3\.ap-south-1\.amazonaws\.com$/.test(target.hostname) || target.username || target.password) throw new Error('invalid_storage');
        url = target.href;
      }
      const link = document.createElement('a');
      link.href = url; link.download = evidence.filename;
      link.click();
      if (blob) setTimeout(() => URL.revokeObjectURL(url), 1000);
    } catch (reason) { failed(reason, 'Could not download the original. Try again.'); }
    finally { if (active.current) setBusy(false); }
  }

  const latest = sources.filter((s, index) => sources.findIndex(other => other.document.source_id === s.document.source_id) === index);
  return <section className="document-workspace" aria-labelledby="documents-heading">
    <div className="page-heading"><div><p className="eyebrow">SOURCE DOCUMENTS</p><h2 id="documents-heading">Documents</h2><p>Keep the original file and inspect its extracted text.</p></div>
      <button className="secondary" disabled={busy || loading} onClick={() => void refresh()}>Refresh documents</button></div>
    {error && <p className="alert" role="alert">{error}{uncertain && ' Refresh documents before you upload again.'}</p>}
    {notice && <p className="success" role="status">{notice}</p>}
    {pending && <div className="panel"><p>An upload needs confirmation before another upload.</p>
      {pending.id && <><button className="secondary" disabled={busy} onClick={() => void checkUpload()}>Check upload status</button>{' '}
        <button className="secondary" disabled={busy} onClick={() => void checkUpload(true)}>Cancel unfinished upload</button>{' '}</>}
      <button className="secondary" disabled={busy || !file || !fictional} onClick={() => void resumeUpload()}>Resume upload</button></div>}
    <div className="document-layout"><div className="document-controls"><section className="panel" aria-labelledby="upload-heading">
      <h3 id="upload-heading">Upload fictional documents</h3><p className="field-hint">Text PDF, DOCX, TXT, or CSV. Select multiple new sources with the same role. Maximum 10 MB per file and 10 saved versions per case.</p>
      <form onSubmit={event => void upload(event)}><fieldset disabled={busy || loading}>
        <label htmlFor="document-file">Document file</label><input id="document-file" type="file" multiple accept=".pdf,.docx,.txt,.csv" ref={fileInput} onChange={event => setFiles(Array.from(event.target.files ?? []))} />
        {files.length > 0 && <p className="field-hint">Selected: {files.map(f => f.name).join(', ')}</p>}
        <label htmlFor="document-kind">Document role</label><select id="document-kind" value={kind} onChange={event => setKind(event.target.value)}>
          <option value="profile">Bank profile</option><option value="policy">Policy</option><option value="control">Control</option><option value="evidence">Evidence</option></select>
        <label htmlFor="replace-source">Replace source</label><select id="replace-source" value={replacement} onChange={event => setReplacement(event.target.value)}>
          <option value="">New source</option>{latest.map(s => <option key={s.document.source_id} value={s.document.source_id}>{s.filename}</option>)}</select>
        <p className="field-hint">A replacement adds a version. It keeps the earlier version.</p>
        <label className="checkbox-label"><input type="checkbox" checked={fictional} onChange={event => setFictional(event.target.checked)} /><span>I confirm this document contains fictional data only.</span></label>
        <button className="full-width" type="submit" disabled={!file || !fictional || uncertain || !!pending || sources.length >= 10}>{busy ? 'Saving document…' : 'Upload fictional document'}</button>
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
          {config.mode === 'aws' && evidence.passage_count! > 500 && <nav aria-label="Source pages">
            <p>Passages {evidence.offset! + 1}–{evidence.offset! + evidence.passages.length} of {evidence.passage_count}</p>
            <button className="secondary" disabled={busy || !evidence.offset} onClick={() => void inspect(evidence.document.document_version_id, Math.max(0, evidence.offset! - 500))}>Previous source page</button>{' '}
            <button className="secondary" disabled={busy || evidence.next_offset === null} onClick={() => void inspect(evidence.document.document_version_id, evidence.next_offset!)}>Next source page</button>
          </nav>}
        </>}
      </section></div>
  </section>;
}
