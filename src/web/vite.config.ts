import { defineConfig } from 'vite';

export default defineConfig({
  plugins: [{
    name: 'explicit-loopback-development-config',
    configureServer(server) {
      server.middlewares.use('/config.json', (_request, response) => {
        response.setHeader('Content-Type', 'application/json');
        response.setHeader('Cache-Control', 'no-store');
        response.end(JSON.stringify({ mode: 'local', api_url: 'http://127.0.0.1:8110' }));
      });
    },
  }],
});
