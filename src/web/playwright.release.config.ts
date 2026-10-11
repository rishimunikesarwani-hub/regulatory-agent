import { defineConfig } from '@playwright/test';

const webPort = process.env.LOCAL_TEST_WEB_PORT || '5185';
const apiPort = process.env.LOCAL_TEST_API_PORT || '8151';
process.env.LOCAL_TEST_WEB_URL = `http://127.0.0.1:${webPort}`;
process.env.LOCAL_TEST_API_URL = `http://127.0.0.1:${apiPort}`;
const evidence = process.env.BROWSER_EVIDENCE_DIR || '../../runs/2026-10-11-slice-05-release';
process.env.BROWSER_EVIDENCE_DIR = evidence;
const python = process.platform === 'win32' ? '"../../.venv/Scripts/python.exe"' : 'python';

export default defineConfig({
  testDir: './tests', testMatch: ['cases.spec.ts', 'documents.spec.ts', 'aws-documents.spec.ts', 'aws-assessment.spec.ts', 'assessment.spec.ts', 'changes.spec.ts', 'release.spec.ts', 'selection.spec.ts', 'comparison.spec.ts'],
  workers: 1, retries: 0, reporter: 'list',
  outputDir: `${evidence}/browser-artifacts`,
  use: { baseURL: `http://127.0.0.1:${webPort}`, browserName: 'chromium', screenshot: 'only-on-failure' },
  webServer: [
    { command: `node node_modules/vite/bin/vite.js --host 127.0.0.1 --port ${webPort} --strictPort`,
      url: `http://127.0.0.1:${webPort}`, reuseExistingServer: false, env: { LOCAL_API_PORT: apiPort } },
    { command: `${python} -m uvicorn regulatory_agent.api:app --app-dir ../ --host 127.0.0.1 --port ${apiPort} --no-proxy-headers`,
      url: `http://127.0.0.1:${apiPort}/api/health`, reuseExistingServer: false,
      env: { APP_ENV: 'local', DEVELOPMENT_USER: 'slice-05-tests', LOCAL_WEB_PORT: webPort,
        CASES_DB_PATH: process.env.LOCAL_TEST_DB_PATH || '../../runs/private/slice-05/browser-tests.sqlite' } },
  ],
});
