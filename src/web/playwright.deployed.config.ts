import { defineConfig } from '@playwright/test';

const deployed = process.env.DEPLOYED_URL;
if (!deployed || !process.env.COGNITO_TEST_USERNAME || !process.env.COGNITO_TEST_PASSWORD) {
  throw new Error('DEPLOYED_URL, COGNITO_TEST_USERNAME, and COGNITO_TEST_PASSWORD are required. Supply credentials through the secure deployment environment.');
}
const url = new URL(deployed);
if (url.protocol !== 'https:' || url.username || url.password || url.search || url.hash) throw new Error('DEPLOYED_URL must be a public HTTPS application URL.');

export default defineConfig({
  testDir: './tests',
  testMatch: 'deployed.spec.ts',
  workers: 1,
  retries: 0,
  timeout: 780_000,
  reporter: 'list',
  outputDir: '../../runs/2026-10-10-autonomous-build/frontend-deployed-artifacts',
  use: { baseURL: deployed, browserName: 'chromium', trace: 'off', screenshot: 'off', video: 'off' },
});
