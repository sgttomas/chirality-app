#!/usr/bin/env python3
"""The level fixtures' own parts, with no Codex: the scripted stub, the run's folders and the fixed commands.

Run from the repository root: python -m pytest -q app/supplier_checks/level/test_level_stub.py
"""
import http.client
import json
import os
import shlex
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
                    words = shlex.split(commands[key])
                    self.assertEqual(words[-1], str(path), key)
                self.assertEqual(shlex.split(commands['net'])[:2], ['/usr/bin/perl', '-e'])
                self.assertEqual(shlex.split(commands['net'])[-1], str(run.stub.port))

    def test_a_scratch_name_with_spaces_and_shell_characters_stays_one_word(self):
        odd = Path(self.scratch) / "odd dir $(touch x) 'q' ;`y`"
        odd.mkdir()
        try:
            with L.Run(odd, '/nonexistent/codex') as run:
                for key, path in run.paths().items():
                    self.assertEqual(shlex.split(run.commands()[key])[-1], str(path), key)
                self.assertEqual(shlex.split(run.commands()['read']), ['/bin/ls', str(run.project)])
            self.assertEqual(list(odd.iterdir()), [])
        finally:
            odd.rmdir()

    def test_a_toml_string_survives_any_path(self):
        import tomllib
        for value in ('/a b/c', 'q"uote\\back', "it's ; $(x) `y`", 'tab\tand\nnewline', 'é'):
            self.assertEqual(tomllib.loads('v = %s' % L.toml_string(value))['v'], value)

    def test_an_unpinned_binary_is_refused(self):
        with tempfile.NamedTemporaryFile() as fake:
            fake.write(b'not codex')
            fake.flush()
            with self.assertRaises(L.Refused):
                L.admitted_binary(fake.name)
        with self.assertRaises(L.Refused):
            L.admitted_binary('relative/codex')


class Judging(unittest.TestCase):
    """The fixture can fail: each way a call can go unobserved, or be misread, refuses or fails."""

    def judge(self, output, call='c', issued=('c',), not_offered=(), items=('c',), asked=(), turn='completed'):
        return L.judge(call, set(issued), set(not_offered), output, set(items), set(asked), turn)

    def test_the_six_outcomes_each_need_their_own_evidence(self):
        ok = 'Chunk ID: 1\nProcess exited with code 0\nOutput:\n'
        refused = 'Process exited with code 1\nOutput:\nzsh:1: operation not permitted: /x\n'
        self.assertEqual(self.judge(ok).kind, L.SUCCEEDED)
        self.assertEqual(self.judge(refused, items=()).kind, L.SANDBOX_REFUSED)
        network = 'Process exited with code 3\nOutput:\nconnect failed: Operation not permitted\n'
        self.assertEqual(self.judge(network).kind, L.SANDBOX_REFUSED)
        self.assertEqual(self.judge('exec_command failed: Rejected("rejected by user")', items=(), asked=('c',)).kind,
                         L.DECLINED)
        self.assertEqual(self.judge('approval policy is Never; reject command', items=()).kind, L.REJECTED)
        self.assertEqual(self.judge('unsupported call: apply_patch', items=()).kind, L.UNSUPPORTED)

    def test_a_call_removed_from_the_script_is_never_a_pass(self):
        with self.assertRaises(L.Refused):  # the stub never issued it
            self.judge('Process exited with code 0\nOutput:\n', issued=())
        not_offered = self.judge(None, issued=(), not_offered=('c',))
        self.assertEqual(not_offered.kind, L.NOT_OFFERED)
        for kind in (L.SANDBOX_REFUSED, L.SUCCEEDED, L.DECLINED, L.REJECTED):
            with self.assertRaisesRegex(AssertionError, 'INCONCLUSIVE'):
                L.expect(not_offered, kind)

    def test_a_turn_that_did_not_complete_is_unresolved(self):
        for turn in (None, 'interrupted', 'failed'):
            with self.assertRaises(L.Refused):
                self.judge('Process exited with code 1\nOutput:\noperation not permitted\n', turn=turn)

    def test_a_failure_without_the_sandbox_text_is_not_a_refusal(self):
        failed = self.judge('Process exited with code 7\nOutput:\ncurl: (7) Failed to connect\n', items=())
        self.assertEqual(failed.kind, L.FAILED)
        with self.assertRaises(AssertionError):
            L.expect(failed, L.SANDBOX_REFUSED)

    def test_outcomes_missing_a_stage_refuse(self):
        with self.assertRaises(L.Refused):  # exit 0 without its command item
            self.judge('Process exited with code 0\nOutput:\n', items=())
        with self.assertRaises(L.Refused):  # a decline with no request for this call
            self.judge('Rejected("rejected by user")', items=(), asked=('other',))
        with self.assertRaises(L.Refused):  # a policy rejection, yet a request was raised for it
            self.judge('approval policy is Never; reject command', items=(), asked=('c',))
        with self.assertRaises(L.Refused):  # no output at all
            self.judge(None)
        with self.assertRaises(L.Refused):  # an output nobody recognises
            self.judge('something else entirely')

    def test_a_misleading_configuration_report_fails_the_effect_check(self):
        """A reply that reports read-only while the write in fact landed: the test asserts the observed outcome,
        so the report alone cannot make it pass."""
        landed = self.judge('Process exited with code 0\nOutput:\n')
        with self.assertRaises(AssertionError):
            L.expect(landed, L.SANDBOX_REFUSED)


class Cleanup(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.mkdtemp(prefix='level-cleanup-test-')
        self.addCleanup(lambda: os.path.isdir(self.scratch) and __import__('shutil').rmtree(self.scratch))

    def test_a_failing_step_does_not_stop_the_later_ones_and_is_raised(self):
        run = L.Run(self.scratch, '/nonexistent/codex')
        run.__enter__()
        broken = mock.Mock()
        broken.stop.side_effect = OSError('invented stop failure')
        run.clients.append(broken)
        with self.assertRaisesRegex(L.Refused, 'invented stop failure'):
            run.__exit__(None, None, None)
        self.assertFalse(run.root.exists())  # removal still ran

    def test_a_removal_error_is_not_ignored(self):
        run = L.Run(self.scratch, '/nonexistent/codex')
        run.__enter__()
        with mock.patch.object(L.shutil, 'rmtree', side_effect=PermissionError('invented removal failure')):
            with self.assertRaisesRegex(L.Refused, 'invented removal failure'):
                run.__exit__(None, None, None)
        __import__('shutil').rmtree(run.root)

    def test_the_whole_group_is_signalled_even_after_its_leader_exited(self):
        client = L.Client.__new__(L.Client)
        client.pgid = 4242
        client.proc = mock.Mock()
        client.proc.poll.return_value = 0  # the leader has exited
        with mock.patch.object(L.os, 'killpg') as killpg:
            client.kill_group()
        killpg.assert_called_once_with(4242, L.signal.SIGKILL)


class LiveRequirement(unittest.TestCase):
    """The live suite's skip condition, without starting Codex."""

    def setUp(self):
        import test_level_live
        self.live = test_level_live

    def test_without_a_binary_it_skips_unless_required(self):
        with self.assertRaises(unittest.SkipTest):
            self.live.live_binary(None, required=False)
        with self.assertRaises(L.Refused):
            self.live.live_binary(None, required=True)
        with self.assertRaises(L.Refused):
            self.live.live_binary('', required=True)

    def test_an_unpinned_binary_fails_whether_or_not_required(self):
        with tempfile.NamedTemporaryFile() as fake:
            fake.write(b'not codex')
            fake.flush()
            for required in (False, True):
                with self.assertRaises(L.Refused):
                    self.live.live_binary(fake.name, required=required)


if __name__ == '__main__':
    unittest.main(verbosity=2)
