export type Config = {
  mode: 'local' | 'aws';
  api_url: string;
  cognito_domain?: string;
  user_pool_client_id?: string;
  redirect_uri?: string;
  commit_sha?: string;
};

const pkceKey = 'regulatory-agent.pkce';
let accessToken: string | null = null;
let expiresAt = 0;
const loopback = (hostname: string) => ['localhost', '127.0.0.1', '[::1]'].includes(hostname);

function safeURL(value: unknown): URL {
  if (typeof value !== 'string') throw new Error('configuration');
  const url = new URL(value);
  if (url.username || url.password || url.search || url.hash) throw new Error('configuration');
  return url;
}

export async function loadConfig(): Promise<Config> {
  const response = await fetch('/config.json', { cache: 'no-store', credentials: 'omit' });
  const raw: unknown = response.status === 404 && loopback(location.hostname)
    ? { mode: 'local', api_url: 'http://127.0.0.1:8110' }
    : response.ok ? await response.json() : null;
  if (!raw || typeof raw !== 'object') throw new Error('configuration');
  const config = raw as Config;
  const api = safeURL(config.api_url);
  if (config.mode === 'local') {
    if (!loopback(location.hostname) || !loopback(api.hostname) || !['http:', 'https:'].includes(api.protocol)) throw new Error('configuration');
  } else if (config.mode === 'aws') {
    const cognito = safeURL(config.cognito_domain);
    const redirect = safeURL(config.redirect_uri);
    if (api.protocol !== 'https:' || cognito.protocol !== 'https:' || cognito.pathname !== '/' ||
        !config.user_pool_client_id || !/^[\w-]+$/.test(config.user_pool_client_id) ||
        redirect.origin !== location.origin || (redirect.protocol !== 'https:' && !loopback(redirect.hostname))) throw new Error('configuration');
  } else throw new Error('configuration');
  return { ...config, api_url: api.href.replace(/\/$/, '') };
}

function base64url(bytes: Uint8Array): string {
  return btoa(String.fromCharCode(...bytes)).replaceAll('+', '-').replaceAll('/', '_').replace(/=+$/, '');
}

export async function startSignIn(config: Config): Promise<void> {
  if (config.mode !== 'aws') throw new Error('configuration');
  const state = base64url(crypto.getRandomValues(new Uint8Array(32)));
  const verifier = base64url(crypto.getRandomValues(new Uint8Array(64)));
  const challenge = base64url(new Uint8Array(await crypto.subtle.digest('SHA-256', new TextEncoder().encode(verifier))));
  sessionStorage.setItem(pkceKey, JSON.stringify({ state, verifier }));
  const url = new URL('/oauth2/authorize', config.cognito_domain);
  url.search = new URLSearchParams({ response_type: 'code', client_id: config.user_pool_client_id!,
    redirect_uri: config.redirect_uri!, scope: 'openid', state, code_challenge_method: 'S256', code_challenge: challenge }).toString();
  location.assign(url.href);
}

export async function finishSignIn(config: Config): Promise<boolean> {
  const url = new URL(location.href);
  const callback = ['code', 'state', 'error', 'error_description'].some(key => url.searchParams.has(key));
  if (!callback) {
    sessionStorage.removeItem(pkceKey);
    return false;
  }
  const code = url.searchParams.get('code');
  const state = url.searchParams.get('state');
  const error = url.searchParams.has('error');
  const pending = sessionStorage.getItem(pkceKey);
  sessionStorage.removeItem(pkceKey);
  for (const key of ['code', 'state', 'error', 'error_description']) url.searchParams.delete(key);
  history.replaceState(null, '', url.pathname + url.search);
  if (config.mode !== 'aws' || error || !code || !state || !pending) throw new Error('signin');
  const saved = JSON.parse(pending) as { state?: string; verifier?: string };
  if (state !== saved.state || !saved.verifier) throw new Error('signin');
  const response = await fetch(new URL('/oauth2/token', config.cognito_domain), {
    method: 'POST', credentials: 'omit', cache: 'no-store',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({ grant_type: 'authorization_code', client_id: config.user_pool_client_id!,
      redirect_uri: config.redirect_uri!, code, code_verifier: saved.verifier }),
  });
  if (!response.ok) throw new Error('signin');
  const tokens: unknown = await response.json();
  if (!tokens || typeof tokens !== 'object') throw new Error('signin');
  const result = tokens as Record<string, unknown>;
  if (typeof result.access_token !== 'string' || !result.access_token || result.token_type !== 'Bearer' ||
      typeof result.expires_in !== 'number' || result.expires_in <= 0 || !Number.isFinite(result.expires_in)) throw new Error('signin');
  accessToken = result.access_token;
  expiresAt = Date.now() + result.expires_in * 1000;
  return true;
}

export function authHeaders(config: Config): Record<string, string> {
  if (config.mode === 'local') return {};
  if (!accessToken || Date.now() >= expiresAt) {
    endSession();
    throw new Error('expired');
  }
  return { Authorization: `Bearer ${accessToken}` };
}

export function endSession(): void {
  accessToken = null;
  expiresAt = 0;
  sessionStorage.removeItem(pkceKey);
}

export function discardCallback(): void {
  endSession();
  const url = new URL(location.href);
  for (const key of ['code', 'state', 'error', 'error_description']) url.searchParams.delete(key);
  history.replaceState(null, '', url.pathname + url.search);
}
