import { defineConfig } from '@playwright/test';

process.env.LOCAL_TEST_WEB_URL = 'http://127.0.0.1:5184';
process.env.LOCAL_TEST_API_URL = 'http://127.0.0.1:8141';
process.env.BROWSER_EVIDENCE_DIR = '../../runs/2026-10-11-slice-04-changes';
const python = process.platform === 'win32' ? '"../../.venv/Scripts/python.exe"' : 'python';

export default defineConfig({
  testDir: './tests', testMatch: ['cases.spec.ts', 'documents.spec.ts', 'aws-documents.spec.ts', 'assessment.spec.ts', 'changes.spec.ts'],
  workers: 1, retries: 0, reporter: 'list',
  outputDir: '../../runs/2026-10-11-slice-04-changes/browser-artifacts',
  use: { baseURL: 'http://127.0.0.1:5184', browserName: 'chromium', screenshot: 'only-on-failure' },
  webServer: [
    { command: 'node node_modules/vite/bin/vite.js --host 127.0.0.1 --port 5184 --strictPort',
      url: 'http://127.0.0.1:5184', reuseExistingServer: false, env: { LOCAL_API_PORT: '8141' } },
    { command: `${python} -m uvicorn regulatory_agent.api:app --app-dir ../ --host 127.0.0.1 --port 8141 --no-proxy-headers`,
      url: 'http://127.0.0.1:8141/api/health', reuseExistingServer: false,
      env: { APP_ENV: 'local', DEVELOPMENT_USER: 'slice-04-tests', LOCAL_WEB_PORT: '5184',
        CASES_DB_PATH: '../../runs/private/slice-04/browser-tests.sqlite' } },
  ],
});
