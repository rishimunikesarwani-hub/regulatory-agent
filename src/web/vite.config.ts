import { defineConfig } from 'vite';

const apiPort = process.env.LOCAL_API_PORT ?? '8110';
if (!/^[1-9]\d{0,4}$/.test(apiPort) || Number(apiPort) > 65535) throw new Error('Use a valid loopback API port.');

export default defineConfig({
  plugins: [{
    name: 'explicit-loopback-development-config',
    configureServer(server) {
      server.middlewares.use('/config.json', (_request, response) => {
        response.setHeader('Content-Type', 'application/json');
        response.setHeader('Cache-Control', 'no-store');
        response.end(JSON.stringify({ mode: 'local', api_url: `http://127.0.0.1:${apiPort}` }));
      });
    },
  }],
});
