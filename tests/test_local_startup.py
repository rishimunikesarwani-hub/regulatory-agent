"""Local startup boundaries. No provider traffic or real child processes."""
import contextlib
import importlib.util
import io
import os
from pathlib import Path
import socket
import sys
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('local_launcher', Path(__file__).resolve().parents[1]/'ops/run_local_demo.py')
launcher = importlib.util.module_from_spec(spec)
spec.loader.exec_module(launcher)


class LocalStartupTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        vite = self.root/'src/web/node_modules/vite/bin/vite.js'
        vite.parent.mkdir(parents=True)
        vite.write_text('// fixture', encoding='utf-8')
        self.env = {'MODEL_PROVIDER': 'openai', 'OPENAI_API_KEY': 'fixture-private-key'}

    def run_launcher(self, *arguments):
        output = io.StringIO()
        with patch.object(launcher, 'ROOT', self.root), patch.dict(os.environ, self.env, clear=True), \
                patch.object(sys, 'argv', ['run_local_demo.py', *arguments]), \
                patch.object(launcher.subprocess, 'check_output', return_value='fixture-commit'), \
                patch.object(launcher.subprocess, 'Popen') as process, contextlib.redirect_stdout(output):
            process.return_value.wait.return_value = 0
            process.return_value.poll.return_value = 0
            try:
                result = launcher.main()
            finally:
                self.output = output.getvalue()
                self.calls = process.call_args_list
        return result

    def test_ls01_missing_key_check_and_start_fail_without_children_or_secret_values(self):
        self.env.pop('OPENAI_API_KEY')
        for arguments in (('--check',), ()):
            with self.assertRaisesRegex(SystemExit, 'Set OPENAI_API_KEY'):
                self.run_launcher(*arguments)
            self.assertEqual(self.calls, [])
        self.env['OPENAI_API_KEY'] = '  '
        with self.assertRaisesRegex(SystemExit, 'Set OPENAI_API_KEY'):
            self.run_launcher('--check')
        self.assertNotIn('fixture-private-key', self.output)

    def test_ls02_selected_ports_and_private_database_reach_both_servers(self):
        with socket.socket() as web, socket.socket() as api:
            web.bind(('127.0.0.1', 0))
            api.bind(('127.0.0.1', 0))
            web_port, api_port = str(web.getsockname()[1]), str(api.getsockname()[1])
        with patch('shutil.which', return_value='node'):
            self.assertEqual(self.run_launcher('--web-port', web_port, '--api-port', api_port,
                '--db-path', 'runs/private/local-startup/feedback.sqlite'), 0)
        self.assertEqual(len(self.calls), 2)
        for call in self.calls:
            env = call.kwargs['env']
            self.assertEqual(env['LOCAL_WEB_PORT'], web_port)
            self.assertEqual(env['LOCAL_API_PORT'], api_port)
            self.assertEqual(Path(env['CASES_DB_PATH']), self.root/'runs/private/local-startup/feedback.sqlite')
            self.assertEqual(env['APP_ENV'], 'local')
        self.assertIn(api_port, self.calls[0].args[0])
        self.assertIn(web_port, self.calls[1].args[0])
        self.assertIn('http://127.0.0.1:'+web_port+'/', self.output)
        self.assertNotIn('fixture-private-key', self.output)

    def test_ls03_busy_port_preserves_existing_server_and_starts_no_children(self):
        with socket.socket() as occupied:
            occupied.bind(('127.0.0.1', 0))
            port = str(occupied.getsockname()[1])
            with self.assertRaisesRegex(SystemExit, 'already in use'):
                self.run_launcher('--api-only', '--api-port', port)
            self.assertEqual(self.calls, [])
            self.assertEqual(occupied.getsockname()[1], int(port))

    def test_ls04_invalid_settings_start_no_children(self):
        for arguments in (('--web-port', '0'), ('--api-port', '65536'),
                ('--web-port', '8160', '--api-port', '8160'), ('--db-path', 'published.sqlite'),
                ('--db-path', 'runs/private/../../published.sqlite')):
            with self.assertRaises(SystemExit):
                self.run_launcher(*arguments, '--check')
            self.assertEqual(self.calls, [])

    def test_ls05_missing_frontend_has_actionable_error_but_api_only_can_start(self):
        (self.root/'src/web/node_modules/vite/bin/vite.js').unlink()
        with self.assertRaisesRegex(SystemExit, 'npm ci'):
            self.run_launcher()
        self.assertEqual(self.calls, [])
        with socket.socket() as available:
            available.bind(('127.0.0.1', 0))
            port = str(available.getsockname()[1])
        self.assertEqual(self.run_launcher('--api-only', '--api-port', port), 0)
        self.assertEqual(len(self.calls), 1)

    def test_ls06_template_has_empty_keys_and_optional_tracing(self):
        root = Path(__file__).resolve().parents[1]
        with patch.dict(os.environ, {}, clear=True):
            env = launcher.load_environment(root/'.env.example')
        self.assertEqual(env.get('MODEL_PROVIDER'), 'openai')
        self.assertEqual(env.get('OPENAI_API_KEY'), '')
        self.assertEqual(env.get('LANGFUSE_SECRET_KEY'), '')
        self.assertNotEqual(env.get('LANGFUSE_CAPTURE_CONTENT'), 'fictional-local')
        self.assertEqual(self.run_launcher('--check'), 0)
        self.assertEqual(self.calls, [])
        self.assertIn('Langfuse keys configured: False', self.output)


if __name__ == '__main__':
    unittest.main()
