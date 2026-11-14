#!/usr/bin/env python3
"""The level fixtures' own parts, with no Codex: the scripted stub, the run's folders and the fixed commands.

Run from the repository root: python -m pytest -q app/supplier_checks/level/test_level_stub.py
"""
import http.client
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))
import level_fixture as L  # noqa: E402


def body(text, tools=('exec_command',), outputs=()):
    entries = [{'type': 'message', 'role': 'developer', 'content': [{'type': 'input_text', 'text': 'invented'}]},
               {'type': 'message', 'role': 'user', 'content': [{'type': 'input_text', 'text': text}]}]
    entries += [{'type': 'function_call_output', 'call_id': c, 'output': o} for c, o in outputs]
    return {'input': entries, 'tools': [{'type': 'function', 'name': n, 'parameters': {'properties': {'cmd': {}}}}
                                        for n in tools]}


def events(raw):
    return [json.loads(line[len('data: '):]) for line in raw.decode().splitlines() if line.startswith('data: ')]


class Scripts(unittest.TestCase):
    def test_the_last_user_message_and_the_outputs_after_it(self):
        b = body('LEVEL[a] go', outputs=[('call_1', 'out')])
        b['input'].insert(1, {'type': 'message', 'role': 'user', 'content': [{'type': 'input_text', 'text': 'LEVEL[old]'}]})
        b['input'].insert(2, {'type': 'function_call_output', 'call_id': 'call_old', 'output': 'stale'})
        self.assertEqual(L.turn_view(b), ('LEVEL[a] go', {'call_1': 'out'}))

    def test_the_shell_tool_offered_is_the_one_called(self):
        self.assertEqual(L.shell_call(body('x'), 'c', 'printf ok > /x')['name'], 'exec_command')
        self.assertEqual(json.loads(L.shell_call(body('x', ('shell_command',)), 'c', 'p')['arguments']), {'command': 'p'})
        self.assertEqual(json.loads(L.shell_call(body('x', ('shell',)), 'c', 'p')['arguments'])['command'],
                         ['/bin/sh', '-c', 'p'])
        self.assertIsNone(L.shell_call(body('x', ('view_image',)), 'c', 'p'))
        escalated = json.loads(L.shell_call(body('x'), 'c', 'p', escalate=True)['arguments'])
        self.assertEqual(escalated['sandbox_permissions'], 'require_escalated')

    def test_namespaced_tool_names(self):
        b = {'tools': [{'type': 'namespace', 'name': 'multi_agent_v1', 'tools': [{'name': 'spawn_agent'}]},
                       {'type': 'web_search'}]}
        self.assertEqual(L.tool_names(b), ['multi_agent_v1.spawn_agent', 'web_search'])

    def test_a_command_script_calls_once_then_closes(self):
        script = L.command_script('call_x', 'printf ok > /x')
        self.assertEqual(script(body('LEVEL[x]'), {}, None)[0]['type'], 'function_call')
        self.assertEqual(script(body('LEVEL[x]'), {'call_x': 'done'}, None)[0]['type'], 'message')


class Stub(unittest.TestCase):
    def setUp(self):
        self.stub = L.ScriptedStub()
        self.addCleanup(self.stub.close)

    def request(self, method, path, payload=None, headers=None):
        conn = http.client.HTTPConnection('127.0.0.1', self.stub.port, timeout=5)
        data = json.dumps(payload).encode() if payload is not None else None
        conn.request(method, path, body=data, headers=dict(headers or {}, **({'Content-Type': 'application/json'}
                                                                             if data else {})))
        response = conn.getresponse()
        return response.status, response.read()

    def test_listens_on_loopback_only(self):
        self.assertEqual(self.stub.server.server_address[0], '127.0.0.1')
        self.assertEqual(self.stub.base_url, 'http://127.0.0.1:%d/v1' % self.stub.port)

    def test_a_websocket_upgrade_gets_426_and_anything_else_404(self):
        self.assertEqual(self.request('GET', '/v1/responses', headers={'Upgrade': 'websocket'})[0], 426)
        self.assertEqual(self.request('GET', '/v1/models')[0], 404)
        self.assertEqual(self.request('POST', '/v1/other', {})[0], 404)
        self.assertEqual(self.stub.unexpected, [('GET', '/v1/models'), ('POST', '/v1/other')])

    def test_a_scripted_turn_streams_its_call_and_records_the_tools_offered(self):
        self.stub.scripts['k'] = L.command_script('call_k', 'printf ok > /x')
        status, raw = self.request('POST', '/v1/responses', body('LEVEL[k] go'))
        self.assertEqual(status, 200)
        kinds = [e['type'] for e in events(raw)]
        self.assertEqual(kinds[0], 'response.created')
        self.assertEqual(kinds[-1], 'response.completed')
        done = [e['item'] for e in events(raw) if e['type'] == 'response.output_item.done']
        self.assertEqual([i['type'] for i in done], ['function_call'])
        self.assertEqual(self.stub.requests[-1]['key'], 'k')
        self.assertEqual(self.stub.requests[-1]['tools'], ['exec_command'])

    def test_an_unscripted_turn_gets_a_message(self):
        _, raw = self.request('POST', '/v1/responses', body('no marker'))
        done = [e['item'] for e in events(raw) if e['type'] == 'response.output_item.done']
        self.assertEqual([i['type'] for i in done], ['message'])

    def test_the_network_probe_is_counted(self):
        self.assertEqual(self.request('GET', '/level-net-probe')[0], 200)
        self.assertEqual(self.stub.net_probes, 1)


class Runs(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.mkdtemp(prefix='level-stub-test-')
        self.addCleanup(lambda: os.path.isdir(self.scratch) and os.rmdir(self.scratch))

    def test_a_run_makes_its_folders_and_removes_them(self):
        with mock.patch.object(L, 'SLASH_TMP', Path(self.scratch)):
            run = L.Run(self.scratch, '/nonexistent/codex', slash_tmp=True, git_marker=True)
            with run:
                for child in ('home', 'userhome', 'project', 'outside', 'tmpdir', 'project/.git'):
                    self.assertTrue((run.root / child).is_dir(), child)
                self.assertTrue(run.slash_tmp.is_dir())
                env = run.environment()
                self.assertEqual(env['CODEX_HOME'], str(run.root / 'home'))
                self.assertEqual(env['HOME'], str(run.root / 'userhome'))
                self.assertTrue(env['TMPDIR'].startswith(str(run.root / 'tmpdir')))
                self.assertEqual({env[n] for n in L.PROXY_NAMES}, {L.PROXY})
                self.assertNotIn('CODEX_EXEC_SERVER_URL', env)
            self.assertFalse(run.root.exists())
            self.assertFalse(run.slash_tmp.exists())

    def test_the_slash_tmp_folder_must_not_exist_before(self):
        with mock.patch.object(L, 'SLASH_TMP', Path(self.scratch)):
            run = L.Run(self.scratch, '/nonexistent/codex', slash_tmp=True)
            os.mkdir(run.slash_tmp)
            try:
                with self.assertRaises(L.Refused):
                    run.__enter__()
                self.assertFalse(run.root.exists())
            finally:
                os.rmdir(run.slash_tmp)

    def test_every_fixed_command_writes_only_under_the_run(self):
        with mock.patch.object(L, 'SLASH_TMP', Path(self.scratch)):
            with L.Run(self.scratch, '/nonexistent/codex', slash_tmp=True) as run:
                commands = run.commands()
                for key, path in run.paths().items():
                    self.assertTrue(str(path).startswith((str(run.root) + '/', str(run.slash_tmp) + '/')), key)
                    self.assertIn('> %s' % path, commands[key])
                self.assertEqual(commands['net'],
                                 '/usr/bin/curl -s -m 3 -o /dev/null http://127.0.0.1:%d/level-net-probe' % run.stub.port)

    def test_an_unpinned_binary_is_refused(self):
        with tempfile.NamedTemporaryFile() as fake:
            fake.write(b'not codex')
            fake.flush()
            with self.assertRaises(L.Refused):
                L.admitted_binary(fake.name)
        with self.assertRaises(L.Refused):
            L.admitted_binary('relative/codex')


if __name__ == '__main__':
    unittest.main(verbosity=2)
