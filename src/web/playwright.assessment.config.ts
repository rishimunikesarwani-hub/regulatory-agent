import { defineConfig } from '@playwright/test';

process.env.LOCAL_TEST_API_URL = 'http://127.0.0.1:8131';
process.env.LOCAL_TEST_WEB_URL = 'http://127.0.0.1:5183';
process.env.BROWSER_EVIDENCE_DIR = '../../runs/2026-10-10-slice-03-assessment';
const python = process.platform === 'win32' ? '"../../.venv/Scripts/python.exe"' : 'python';

export default defineConfig({
  testDir: './tests', testMatch: ['cases.spec.ts', 'documents.spec.ts', 'assessment.spec.ts'], workers: 1, retries: 0, reporter: 'list',
  outputDir: '../../runs/2026-10-10-slice-03-assessment/frontend-browser-artifacts',
  use: { baseURL: 'http://127.0.0.1:5183', browserName: 'chromium', screenshot: 'only-on-failure' },
  webServer: [
    { command: 'node node_modules/vite/bin/vite.js --host 127.0.0.1 --port 5183 --strictPort',
      url: 'http://127.0.0.1:5183', reuseExistingServer: false, env: { LOCAL_API_PORT: '8131' } },
    { command: `${python} -m uvicorn regulatory_agent.api:app --app-dir ../ --host 127.0.0.1 --port 8131 --no-proxy-headers`,
      url: 'http://127.0.0.1:8131/api/health', reuseExistingServer: false,
      env: { APP_ENV: 'local', DEVELOPMENT_USER: 'slice-03-tests', LOCAL_WEB_PORT: '5183',
        CASES_DB_PATH: '../../runs/private/slice-03/browser-tests.sqlite' } },
  ],
});
