import { defineConfig } from '@playwright/test';

// All local slice checks use the VS2 test database, never the feedback database.
process.env.LOCAL_TEST_API_URL = 'http://127.0.0.1:8121';
process.env.LOCAL_TEST_WEB_URL = 'http://127.0.0.1:5182';
process.env.BROWSER_EVIDENCE_DIR = '../../runs/2026-10-10-slice-02-documents';
const python = process.platform === 'win32' ? '"../../.venv/Scripts/python.exe"' : 'python';

export default defineConfig({
  testDir: './tests', testMatch: ['cases.spec.ts', 'documents.spec.ts'], workers: 1, retries: 0, reporter: 'list',
  outputDir: '../../runs/2026-10-10-slice-02-documents/frontend-browser-artifacts',
  use: { baseURL: 'http://127.0.0.1:5182', browserName: 'chromium', screenshot: 'only-on-failure' },
  webServer: [
    { command: 'node node_modules/vite/bin/vite.js --host 127.0.0.1 --port 5182 --strictPort',
      url: 'http://127.0.0.1:5182', reuseExistingServer: false, env: { LOCAL_API_PORT: '8121' } },
    { command: `${python} -m uvicorn regulatory_agent.api:app --app-dir ../ --host 127.0.0.1 --port 8121 --no-proxy-headers`,
      url: 'http://127.0.0.1:8121/api/health', reuseExistingServer: false,
      env: { APP_ENV: 'local', DEVELOPMENT_USER: 'slice-02-tests', LOCAL_WEB_PORT: '5182',
        CASES_DB_PATH: '../../runs/private/slice-02/browser-tests.sqlite' } },
  ],
});
