import { useEffect, useRef, useState, type FormEvent } from 'react';
import { createRoot } from 'react-dom/client';
import { authHeaders, discardCallback, endSession, finishSignIn, loadConfig, startSignIn, type Config } from './auth';
import './style.css';
import { DocumentsPanel } from './documents';

type CaseRecord = {
  case_id: string;
  owner_id: string;
  created_at: string;
  bank_profile: Record<string, string | boolean | null> & { name: string };
  synthetic: true;
};

class ApiError extends Error {
  constructor(readonly status: number) { super('api_error'); }
}

function caseRecord(value: unknown): CaseRecord {
  const record = value as CaseRecord;
  if (!record || !/^[A-Za-z0-9][A-Za-z0-9_.:-]{0,127}$/.test(record.case_id) ||
      typeof record.owner_id !== 'string' || !record.owner_id || record.synthetic !== true ||
      typeof record.bank_profile?.name !== 'string' || !record.bank_profile.name.trim() ||
      !Number.isFinite(Date.parse(record.created_at))) throw new Error('invalid_response');
  return record;
}

async function api(config: Config, path: string, body?: object): Promise<unknown> {
  const response = await fetch(`${config.api_url}/api/cases${path}`, {
    method: body ? 'POST' : 'GET', cache: 'no-store', credentials: 'omit',
    headers: { ...authHeaders(config), ...(body ? { 'Content-Type': 'application/json' } : {}) },
    body: body ? JSON.stringify(body) : undefined,
    signal: AbortSignal.timeout(20_000),
  });
  if (!response.ok) throw new ApiError(response.status);
  return response.json();
}

function setCaseURL(id?: string): void {
  const url = new URL(location.href);
  if (url.searchParams.get('case') !== id) for (const key of ['source', 'upload', 'uploadKey']) url.searchParams.delete(key);
  if (id) url.searchParams.set('case', id);
  else url.searchParams.delete('case');
  history.replaceState(null, '', url.pathname + url.search);
}

function App() {
  const [config, setConfig] = useState<Config | null>(null);
  const [initializing, setInitializing] = useState(true);
  const [configurationFailed, setConfigurationFailed] = useState(false);
  const [signedIn, setSignedIn] = useState(false);
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [uncertainSave, setUncertainSave] = useState(false);
  const [error, setError] = useState('');
  const [notice, setNotice] = useState('');
  const [cases, setCases] = useState<CaseRecord[]>([]);
  const [selected, setSelected] = useState<CaseRecord | null>(null);
  const [view, setView] = useState<'cases' | 'detail'>('cases');
  const [name, setName] = useState('');
  const [fictional, setFictional] = useState(false);
  const heading = useRef<HTMLHeadingElement>(null);

  function handleExpired(reason: unknown): boolean {
    if ((reason instanceof ApiError && reason.status === 401) || (reason instanceof Error && reason.message === 'expired')) {
      endSession();
      setSignedIn(false);
      setCases([]);
      setSelected(null);
      setName('');
      setFictional(false);
      setNotice('');
      setError('Your session ended. Sign in again to open your cases.');
      return true;
    }
    return false;
  }

  async function openCase(id: string, current = config): Promise<void> {
    if (!current) return;
    setView('detail');
    setSelected(null);
    setLoading(true);
    setError('');
    setNotice('');
    setCaseURL(id);
    try {
      setSelected(caseRecord(await api(current, `/${encodeURIComponent(id)}`)));
    } catch (reason) {
      if (!handleExpired(reason)) setError('This case is not available. Return to your cases and select another case.');
    } finally { setLoading(false); }
  }

  async function loadCases(current = config, resume = false): Promise<void> {
    if (!current) return;
    setSignedIn(true);
    setView('cases');
    setSelected(null);
    setLoading(true);
    setError('');
    setNotice('');
    try {
      const result = await api(current, '') as { cases?: unknown[] };
      if (!Array.isArray(result.cases)) throw new Error('invalid_response');
      setCases(result.cases.map(caseRecord));
      setUncertainSave(false);
      const id = resume ? new URL(location.href).searchParams.get('case') : null;
      if (id) await openCase(id, current);
      else setCaseURL();
    } catch (reason) {
      if (!handleExpired(reason)) setError('Could not load your cases. Select Refresh cases to try again.');
    } finally { setLoading(false); }
  }

  useEffect(() => {
    void (async () => {
      let current: Config;
      try { current = await loadConfig(); setConfig(current); }
      catch { discardCallback(); setConfigurationFailed(true); setError('Application configuration is unavailable. Contact the deployment administrator.'); setInitializing(false); return; }
      try { if (await finishSignIn(current)) await loadCases(current, true); }
      catch { setError('Sign-in could not be completed. Select Sign in securely to try again.'); }
      finally { setInitializing(false); }
    })();
  }, []);

  useEffect(() => {
    if (signedIn && !initializing && !loading && document.activeElement === document.body) heading.current?.focus();
  }, [signedIn, initializing, loading, selected]);

  async function signIn(): Promise<void> {
    if (!config) return;
    setError('');
    if (config.mode === 'local') await loadCases(config, true);
    else {
      setLoading(true);
      try { await startSignIn(config); }
      catch { setError('Sign-in could not be started. Try again.'); setLoading(false); }
    }
  }

  async function saveCase(event: FormEvent): Promise<void> {
    event.preventDefault();
    if (!config || saving || uncertainSave || !fictional || !name.trim()) return;
    setSaving(true);
    setError('');
    setNotice('');
    try {
      const saved = caseRecord(await api(config, '', { bank_profile: { name: name.trim() }, synthetic: true }));
      setSelected(saved);
      setView('detail');
      setCaseURL(saved.case_id);
      setNotice('Case saved');
      setName('');
      setFictional(false);
    } catch (reason) {
      if (!handleExpired(reason)) {
        if (reason instanceof ApiError && reason.status === 422) setError('The case was not saved. Use a fictional bank name with 1 to 200 characters.');
        else {
          setUncertainSave(true);
          setError('The save could not be confirmed. Check saved cases before you try again to avoid creating a duplicate.');
        }
      }
    } finally { setSaving(false); }
  }

  function signOut(): void {
    endSession(); setSignedIn(false); setCases([]); setSelected(null); setName(''); setFictional(false);
    setError(''); setNotice(''); setCaseURL();
  }

  return <>
    <a className="skip-link" href="#main">Skip to content</a>
    <header className="topbar"><div className="brand"><span className="brand-mark" aria-hidden="true">R</span><span>The Regulator</span></div>
      <div className="topbar-actions">{config && <span className="mode">{config.mode === 'local' ? 'Local development' : 'AWS development'}</span>}
        {signedIn && <button className="text-button" onClick={signOut}>Sign out</button>}</div>
    </header>
    <main id="main" className={signedIn ? 'workspace' : 'welcome'}>
      {error && <div className="alert" role="alert">{error}</div>}
      {initializing ? <p role="status">Loading application…</p> : configurationFailed ? <section className="panel"><h1>Application unavailable</h1><p>The sign-in configuration must be corrected before you continue.</p><button onClick={() => location.reload()}>Reload application</button></section> : !signedIn ?
        <section className="sign-in-layout"><div className="panel sign-in-panel"><h1>Sign in to continue</h1>
            <button className="full-width" disabled={loading} onClick={() => void signIn()}>{loading ? 'Starting sign-in…' : config?.mode === 'local' ? 'Continue with local identity' : 'Sign in securely'}</button>
          </div></section>
      : <>
        {view === 'cases' ? <>
          <div className="page-heading"><div><p className="eyebrow">CASE WORKSPACE</p><h1 tabIndex={-1} ref={heading}>Your cases</h1><p>Start a fictional case or reopen a saved profile.</p></div><button className="secondary" disabled={loading || saving} onClick={() => void loadCases()}>Refresh cases</button></div>
          <div className="case-layout"><section className="saved-cases" aria-labelledby="saved-heading"><h2 id="saved-heading">Saved cases <span className="count">{cases.length}</span></h2>
            {loading ? <p className="panel" role="status">Loading your cases…</p> : cases.length === 0 ? <div className="panel empty"><span className="empty-mark" aria-hidden="true">+</span><h3>No cases yet</h3><p>Create your first fictional case. Your saved bank profile will appear here.</p></div> : <div className="case-list">{cases.map(record => <article className="panel case-card" key={record.case_id}><div><span className="badge">Synthetic demo</span><h3>{record.bank_profile.name}</h3><p>Saved {new Date(record.created_at).toLocaleString()}</p><span className="status-label">Assessment not started</span></div><button className="secondary" disabled={saving || loading} aria-label={`Open ${record.bank_profile.name}`} onClick={() => void openCase(record.case_id)}>Open case <span aria-hidden="true">→</span></button></article>)}</div>}
          </section><section className="panel create-panel" aria-labelledby="create-heading"><p className="small-label">NEW CASE</p><h2 id="create-heading">Create a fictional case</h2><p>Use a made-up bank name. Private bank data is not enabled.</p>
            <form onSubmit={event => void saveCase(event)}><label htmlFor="bank-name">Fictional bank name</label><input id="bank-name" name="bank-name" value={name} maxLength={200} required autoComplete="off" placeholder="For example, Sample River Bank" disabled={saving} onChange={event => setName(event.target.value)} aria-describedby="name-hint" /><p id="name-hint" className="field-hint">Use 1 to 200 characters.</p>
              <label className="checkbox-label"><input type="checkbox" checked={fictional} disabled={saving} onChange={event => setFictional(event.target.checked)} /><span>I confirm this case contains fictional data only.</span></label>
              <button className="full-width" type="submit" disabled={saving || loading || uncertainSave || !name.trim() || !fictional}>{saving ? 'Saving case…' : 'Save fictional case'}</button>
              {uncertainSave && <button className="secondary full-width check-button" type="button" disabled={loading} onClick={() => void loadCases()}>Check saved cases</button>}
            </form></section></div>
        </> : <>
          <button className="text-button back-button" onClick={() => void loadCases()}>← <span>Back to cases</span></button>
          {loading ? <p role="status">Loading case…</p> : selected && <>
            {notice && <p className="success" role="status">{notice}</p>}
            <div className="page-heading"><div><span className="badge">Synthetic demo</span><h1 tabIndex={-1} ref={heading}>{selected.bank_profile.name}</h1><p>Your fictional bank profile is saved.</p></div><span className="status-label">Not started</span></div>
            <section className="panel detail-panel"><h2>Case details</h2><dl><div><dt>Bank profile</dt><dd>{selected.bank_profile.name}</dd></div><div><dt>Data type</dt><dd>Fictional data</dd></div><div><dt>Created</dt><dd>{new Date(selected.created_at).toLocaleString()}</dd></div><div><dt>Case ID</dt><dd className="identifier">{selected.case_id}</dd></div></dl></section>
            {config && <DocumentsPanel key={selected.case_id} config={config} caseId={selected.case_id} onExpired={handleExpired} />}
          </>}
        </>}
      </>}
    </main>
    <footer>Fictional case workspace · Development release{config?.commit_sha && <span> · Build {config.commit_sha.slice(0, 12)}</span>}</footer>
  </>;
}

createRoot(document.getElementById('root')!).render(<App />);
