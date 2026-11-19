#!/usr/bin/env python3
"""The level fixtures' own parts, with no Codex: the scripted stub, the run's folders and the fixed commands.

Run from the repository root: python -m pytest -q app/supplier_checks/level/test_level_stub.py
"""
import http.client
import io
import json
import threading
import os
import re
import shlex
import subprocess
import sys
import tempfile
import time
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
        self.stub.allowed_commands = {'printf ok > /x'}  # a bare stub allows no command until given its list
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

    def test_the_var_tmp_folder_is_made_only_when_absent_and_removed_after(self):
        with mock.patch.object(L, 'VAR_TMP', Path(self.scratch)):
            run = L.Run(self.scratch, '/nonexistent/codex', var_tmp=True)
            with run:
                self.assertTrue(run.var_tmp.is_dir())
                self.assertEqual(run.paths()['vartmp'].parent, run.var_tmp)
                self.assertEqual(shlex.split(run.commands()['vartmp'])[-1], str(run.paths()['vartmp']))
            self.assertFalse(run.var_tmp.exists())
            again = L.Run(self.scratch, '/nonexistent/codex', var_tmp=True)
            os.mkdir(again.var_tmp)
            try:
                with self.assertRaises(L.Refused):
                    again.__enter__()
                self.assertTrue(again.var_tmp.is_dir())  # one it found is never removed
            finally:
                os.rmdir(again.var_tmp)

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

    def test_the_apps_layout_puts_the_home_and_tmpdir_where_the_app_does_and_its_operations_stay_inside(self):
        with L.Run(self.scratch, '/nonexistent/codex', working_files=True) as run:
            env = run.environment()
            self.assertEqual(Path(env['CODEX_HOME']), run.root / 'Invented App Data' / 'homes' / 'account')
            self.assertEqual((run.home / 'config.toml').read_bytes(), b'')
            self.assertEqual(run.tmpdir.parent, run.root / 'Invented App Data Working Files' / 'codex-tmp')
            self.assertEqual(env['TMPDIR'], str(run.tmpdir) + '/')
            ops = run.entry_operations()
            self.assertEqual(set(ops) - set(run.commands()), set())  # every operation is on the enforced list
            for key, (command, lines) in ops.items():
                words = [w for w in shlex.split(command) if w.startswith('/')]
                self.assertTrue(words and all(w.startswith(str(run.root) + '/') for w in words), key)
                self.assertNotIn('rm ', command + ' ')
                self.assertEqual(len(lines), 1, key)
            ident, names = run.entries()
            self.assertEqual(len(ident), 5)
            self.assertEqual(names[str(run.codex_tmp)], [run.tmpdir.name])
        self.assertFalse(run.root.exists())
        with L.Run(self.scratch, '/nonexistent/codex') as run:
            self.assertEqual(run.entry_operations(), {})

    def test_a_scratch_name_with_spaces_and_shell_characters_stays_one_word(self):
        odd = Path(self.scratch) / "odd dir 'q' (p) ; & #"
        odd.mkdir()
        try:
            with L.Run(odd, '/nonexistent/codex', project_name='project dq "x"') as run:
                for key, path in run.paths().items():
                    self.assertEqual(shlex.split(run.commands()[key])[-1], str(path), key)
                self.assertEqual(shlex.split(run.commands()['read']), ['/bin/ls', str(run.project)])
            self.assertEqual(list(odd.iterdir()), [])
        finally:
            odd.rmdir()

    def test_a_scratch_base_holding_a_character_a_shell_expands_is_refused(self):
        for name in ('has $(x)', 'has `y`', 'has "q"', 'has \\ b', 'has $HOME'):
            bad = Path(self.scratch) / name / 'inner'
            bad.mkdir(parents=True)
            try:
                with self.assertRaises(L.Refused):
                    L.Run(bad, '/nonexistent/codex')  # the ancestor carries it
            finally:
                bad.rmdir()
                bad.parent.rmdir()

    def test_a_command_off_the_fixed_list_never_reaches_codex(self):
        with L.Run(self.scratch, '/nonexistent/codex') as run:
            run.stub.scripts['k'] = L.command_script('call_k', 'printf ok > /somewhere/else')
            items = run.stub.answer(body('LEVEL[k] go'))
            self.assertEqual([i['type'] for i in items], ['message'])
            self.assertEqual(run.stub.violations, ['printf ok > /somewhere/else'])
            self.assertNotIn('call_k', run.stub.issued)
            run.stub.scripts['j'] = L.command_script('call_j', run.commands()['in'])
            self.assertEqual(run.stub.answer(body('LEVEL[j] go'))[0]['type'], 'function_call')

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



class SecondProject(unittest.TestCase):
    """The second project folder B beside the project A, its fixed commands, and the invented instruction and
    settings files, with no Codex."""

    BEFORE = {'in', 'out', 'out2', 'tmpdir', 'late', 'git', 'extra'}

    def setUp(self):
        self.scratch = tempfile.mkdtemp(prefix='level-second-test-')
        self.addCleanup(lambda: os.path.isdir(self.scratch) and os.rmdir(self.scratch))

    def test_without_it_the_run_is_as_before(self):
        with L.Run(self.scratch, '/nonexistent/codex') as run:
            self.assertIsNone(run.project_b)
            self.assertEqual(set(run.paths()), self.BEFORE)
            self.assertEqual(set(run.commands()) - self.BEFORE, {'read', 'net'})
            self.assertEqual((run.relative_landings(), run.settings_roots(), run.markers), ({}, {}, {}))
            self.assertEqual(sorted(p.name for p in run.root.iterdir()), ['home', 'outside', 'project', 'tmpdir', 'userhome'])
            self.assertEqual(list(run.project.iterdir()), [])
            self.assertEqual(run.stub.watched, ())

    def test_b_is_made_beside_a_with_the_same_care_and_removed_after(self):
        with L.Run(self.scratch, '/nonexistent/codex', git_marker=True, second_project='project-b',
                   second_git_marker=True) as run:
            self.assertEqual(run.project_b, run.root / 'project-b')
            self.assertEqual(run.project_b.parent, run.project.parent)
            self.assertEqual(os.stat(run.project_b).st_mode & 0o777, 0o700)
            self.assertTrue((run.project_b / '.git').is_dir())
            self.assertEqual(sorted(p.name for p in run.project_b.iterdir()), ['.git'])  # no files unless asked
            self.assertEqual(sorted(p.name for p in run.project.iterdir()), ['.git'])
            self.assertEqual(run.paths()['in-b'], run.project_b / 'w-in-b')
            commands = run.commands()
            self.assertEqual(set(commands) - self.BEFORE, {'read', 'net', 'in-b', 'pwd', 'relative'})
            self.assertEqual(run.stub.allowed_commands, set(commands.values()))  # every one on the enforced list
            for key, path in run.paths().items():
                self.assertTrue(str(path).startswith(str(run.root) + '/'), key)
                self.assertEqual(shlex.split(commands[key])[-1], str(path), key)
            self.assertEqual(shlex.split(commands['pwd']), ['/bin/pwd', '-P'])
            self.assertEqual(commands['relative'], 'case "$(/bin/pwd -P)" in %s|%s) printf ok > %s;; *) exit 97;; esac'
                             % (shlex.quote(os.path.realpath(run.project)),
                                shlex.quote(os.path.realpath(run.project_b)), L.RELATIVE_NAME))
            # Run by a shell in each project it lands there; in any other folder it exits 97 and writes nothing.
            elsewhere = run.root / 'outside'
            for folder, code in ((run.project, 0), (run.project_b, 0), (elsewhere, L.RELATIVE_ELSEWHERE)):
                for shell in filter(os.path.exists, ('/bin/sh', '/bin/zsh', '/bin/bash')):
                    landing = folder / L.RELATIVE_NAME
                    done = subprocess.run([shell, '-c', commands['relative']], cwd=str(folder), capture_output=True)
                    self.assertEqual(done.returncode, code, (shell, folder, done.stderr))
                    self.assertEqual(landing.exists(), code == 0, (shell, folder))
                    if code == 0:
                        self.assertEqual(landing.read_text(), 'ok')
                        landing.unlink()
            self.assertEqual(os.listdir(elsewhere), [])
            self.assertNotIn('/', L.RELATIVE_NAME)
            self.assertEqual(run.relative_landings(), {'a': run.project / L.RELATIVE_NAME,
                                                       'b': run.project_b / L.RELATIVE_NAME})
        self.assertFalse(run.root.exists())

    def test_bs_name_is_checked(self):
        for name in ('', '.', '..', 'a/b', 'project', 'outside', 'home', 'userhome', 'tmpdir', 'has $x', 'q"x',
                     'b`x`', 'back\\slash', '.git', 'Invented App Data', 'Invented App Data Working Files',
                     'codex-stderr-0.log'):
            with self.subTest(name=name), self.assertRaises(L.Refused):
                L.Run(self.scratch, '/nonexistent/codex', second_project=name)
        for option in ('second_git_marker', 'instructions', 'project_settings'):
            with self.subTest(option=option), self.assertRaises(L.Refused):
                L.Run(self.scratch, '/nonexistent/codex', **{option: True})
        self.assertEqual(os.listdir(self.scratch), [])

    def test_the_instruction_files_carry_a_marker_of_their_own(self):
        with L.Run(self.scratch, '/nonexistent/codex', second_project='project-b', instructions=True) as run:
            a, b = run.markers['a'], run.markers['b']
            self.assertNotEqual(a, b)
            self.assertFalse(a in b or b in a)
            self.assertNotIn('LEVEL[', a + b)  # never mistaken for a turn's script key
            text_a = (run.project / 'AGENTS.md').read_text()
            text_b = (run.project_b / 'AGENTS.md').read_text()
            self.assertEqual((a in text_a, b in text_a, b in text_b, a in text_b), (True, False, True, False))
            self.assertFalse((run.project / '.codex').exists())
            again = L.Run(self.scratch, '/nonexistent/codex', second_project='project-b', instructions=True)
            self.assertNotEqual(again.markers, run.markers)  # a marker seen cannot be another run's

    def test_each_projects_settings_name_a_writable_root_of_its_own(self):
        import tomllib
        with L.Run(self.scratch, '/nonexistent/codex', second_project='project-b', project_settings=True) as run:
            roots = run.settings_roots()
            self.assertEqual(roots, {'a': run.root / 'outside' / 'root-a', 'b': run.root / 'outside' / 'root-b'})
            for side, folder in (('a', run.project), ('b', run.project_b)):
                self.assertEqual(os.stat(roots[side]).st_mode & 0o777, 0o700)
                settings = tomllib.loads((folder / '.codex' / 'config.toml').read_text())
                self.assertEqual(settings, {'sandbox_workspace_write': {'writable_roots': [str(roots[side])]}})
                self.assertEqual(run.paths()['root-' + side], roots[side] / ('w-root-' + side))
                self.assertEqual(shlex.split(run.commands()['root-' + side])[-1], str(roots[side] / ('w-root-' + side)))
            self.assertFalse((run.project / 'AGENTS.md').exists())
        self.assertFalse(run.root.exists())

    def test_the_stub_notes_only_the_watched_markers_a_request_carries(self):
        stub = L.ScriptedStub()
        self.addCleanup(stub.close)
        carrying = body('LEVEL[k] go')
        carrying['input'][0]['content'][0]['text'] = 'invented INVENTED-B here'
        stub.answer(carrying)
        self.assertEqual(stub.requests[-1]['markers'], [])  # nothing watched, nothing noted
        stub.watched = ('INVENTED-A', 'INVENTED-B')
        stub.answer(carrying)
        stub.answer(body('LEVEL[k] go'))
        self.assertEqual([r['markers'] for r in stub.requests[1:]], [['INVENTED-B'], []])
        # Only the markers are kept: nothing else of the request's text is in what the stub retains for it.
        self.assertEqual(set(stub.requests[1]), {'key', 'tools', 'body_tools', 'body_keys', 'markers'})
        self.assertNotIn('invented INVENTED-B here', json.dumps(stub.requests[1]))
        self.assertEqual(stub.requests[-1]['key'], 'k')


class TrustedProjectFiles(unittest.TestCase):
    """A project's own files for the trusted-project rows, their marker commands and the second listener, with no
    Codex."""

    def setUp(self):
        self.scratch = tempfile.mkdtemp(prefix='level-trust-test-')
        self.addCleanup(lambda: os.path.isdir(self.scratch) and os.rmdir(self.scratch))

    def test_without_it_the_run_is_as_before(self):
        with L.Run(self.scratch, '/nonexistent/codex') as run:
            self.assertIsNone(run.other)
            self.assertEqual((run.trust_markers, run.touch_refusals()), ({}, {}))
            self.assertEqual(set(run.paths()), SecondProject.BEFORE)
            self.assertEqual(set(run.commands()) - SecondProject.BEFORE, {'read', 'net'})
            self.assertEqual(list((run.root / 'outside').iterdir()), [])
            for refused in (lambda: run.marker('notify'), lambda: run.write_trust_file('.codex/config.toml', ''),
                            lambda: run.write_home_file('config.toml', ''), run.hooks_json, run.policy_toml):
                with self.assertRaises(L.Refused):
                    refused()
            self.assertFalse((run.project / '.codex').exists())

    def test_each_marker_command_appends_to_its_own_file_alone_and_exits(self):
        with L.Run(self.scratch, '/nonexistent/codex', trusted_project=True) as run:
            outside = run.root / 'outside'
            shell_files = {'zdotdir', 'bash-env.sh'}
            self.assertEqual({p.name for p in outside.iterdir()}, shell_files)
            with self.assertRaises(L.Refused):
                run.marker('elsewhere')
            for name in L.PROJECT_MARKERS:
                path = run.marker(name)
                self.assertEqual(path.parent, outside)
                words = shlex.split(run.marker_command(name))
                self.assertEqual((words[0], words[-2], words[-1]), ('/usr/bin/printf', '>>', str(path)))
                self.assertEqual(run.marker_argv(name), ['/bin/sh', '-c', run.marker_command(name)])
                self.assertEqual(run.marker_runs(name), 0)
                for times in (1, 2):
                    done = subprocess.run(run.marker_argv(name) + ['an argument notify would add'], capture_output=True,
                                          env={'PATH': '/nonexistent'})  # absolute binaries only: no PATH needed
                    self.assertEqual((done.returncode, done.stdout, done.stderr), (0, b'', b''))
                    self.assertEqual(run.marker_runs(name), times)
            self.assertEqual({p.name for p in outside.iterdir()},
                             shell_files | {'m-' + name for name in L.PROJECT_MARKERS})
            run.clear_markers()
            self.assertEqual({p.name for p in outside.iterdir()}, shell_files)
        self.assertFalse(run.root.exists())

    def test_the_shell_start_up_files_are_the_marker_commands(self):
        with L.Run(self.scratch, '/nonexistent/codex', trusted_project=True) as run:
            files = run.shell_files()
            # The one line beside the marker command: a builtin export, starting no program and writing nothing.
            self.assertEqual(L.STARTUP_LINE, 'export LEVEL_INVENTED_STARTUP=ran')
            self.assertEqual((files['zdotdir'] / '.zshenv').read_text(),
                             L.STARTUP_LINE + '\n' + run.marker_command('zdotdir') + '\n')
            self.assertEqual(files['bash-env'].read_text(),
                             L.STARTUP_LINE + '\n' + run.marker_command('bash-env') + '\n')
            # The measured command sees what either start-up file exports, through the shell that reads it; only
            # that file's marker runs.
            for shell, variable, value, name in (('/bin/zsh', 'ZDOTDIR', files['zdotdir'], 'zdotdir'),
                                                 ('/bin/bash', 'BASH_ENV', files['bash-env'], 'bash-env')):
                if os.path.exists(shell):
                    done = subprocess.run([shell, '-c', run.commands()['env']], capture_output=True, text=True,
                                          env={'PATH': L.SYSTEM_PATH, variable: str(value)}, check=True,
                                          stdin=subprocess.DEVNULL)
                    self.assertEqual(done.stdout, 'startup=ran\nvariable=unset', shell)
                    self.assertEqual({other: run.marker_runs(other) for other in ('zdotdir', 'bash-env')},
                                     {'zdotdir': int(name == 'zdotdir'), 'bash-env': int(name == 'bash-env')}, shell)
                    run.clear_markers()
            # Each is read where its shell reads it: shown here, so that the live control's marker means what it says.
            # Standard input is /dev/null: bash reads no BASH_ENV when its standard input is a socket (its check for
            # being started by a remote shell daemon), and a test runner's inherited input can be one.
            for shell, variable, value, name in (('/bin/zsh', 'ZDOTDIR', files['zdotdir'], 'zdotdir'),
                                                 ('/bin/bash', 'BASH_ENV', files['bash-env'], 'bash-env')):
                if os.path.exists(shell):
                    subprocess.run([shell, '-c', 'true'], env={'PATH': L.SYSTEM_PATH, variable: str(value)}, check=True,
                                   stdin=subprocess.DEVNULL)
                    self.assertEqual(run.marker_runs(name), 1, shell)

    def test_the_project_files_parse_and_name_only_the_marker_commands(self):
        import tomllib
        with L.Run(self.scratch, '/nonexistent/codex', trusted_project=True) as run:
            text = (run.mcp_toml() + run.notify_toml() + run.policy_toml() + run.provider_toml() +
                    run.developer_toml() + run.shell_env_toml() + run.permissions_toml() + run.thread_store_toml() +
                    run.hook_state_toml([('/invented/.codex/hooks.json:stop:0:0', 'sha256:invented')]))
            settings = tomllib.loads(text)  # every builder joins with every other
            self.assertEqual(settings['mcp_servers'][L.MCP_STDIO]['command'], '/bin/sh')
            self.assertEqual(['/bin/sh'] + settings['mcp_servers'][L.MCP_STDIO]['args'], run.marker_argv('mcp-stdio'))
            self.assertEqual(settings['mcp_servers'][L.MCP_HTTP]['url'], 'http://127.0.0.1:%d/mcp' % run.other.port)
            self.assertEqual(settings['notify'], run.marker_argv('notify'))
            self.assertEqual((settings['approval_policy'], settings['sandbox_mode'], settings['approvals_reviewer'],
                              settings['sandbox_workspace_write']),
                             ('never', 'danger-full-access', 'auto_review', {'network_access': True}))
            self.assertEqual((settings['model_provider'], settings['model'], settings['openai_base_url']),
                             (L.OTHER_PROVIDER, L.OTHER_MODEL, run.other.base_url))
            self.assertEqual(settings['model_providers'][L.OTHER_PROVIDER]['base_url'], run.other.base_url)
            self.assertNotEqual(run.other.port, run.stub.port)
            self.assertEqual(settings['developer_instructions'], run.trust_markers['project'])
            self.assertEqual(settings['shell_environment_policy']['set'],
                             {L.TRUST_ENV: run.trust_markers['project'], 'ZDOTDIR': str(run.shell_files()['zdotdir']),
                              'BASH_ENV': str(run.shell_files()['bash-env'])})
            self.assertEqual(settings['default_permissions'], ':danger-full-access')
            self.assertEqual(settings['experimental_thread_store_endpoint'], run.other_origin())
            self.assertEqual(settings['hooks'], {'state': {'/invented/.codex/hooks.json:stop:0:0':
                                                           {'trusted_hash': 'sha256:invented'}}})
            hooks = json.loads(run.hooks_json())
            self.assertEqual(set(hooks), {'hooks'})
            self.assertEqual(set(hooks['hooks']), set(L.HOOK_MARKERS))
            for event, name in L.HOOK_MARKERS.items():
                self.assertEqual(hooks['hooks'][event], [{'hooks': [{'type': 'command', 'timeout': 5,
                                                                     'command': run.marker_command(name)}]}])
            # Every program any file names is a marker command, and every address is the second listener's.
            commands = {run.marker_command(n) for n in L.PROJECT_MARKERS}
            for blob in (text, run.hooks_json()):
                self.assertEqual(blob.count('printf'), sum(blob.count(json.dumps(c)[1:-1]) for c in commands))
                self.assertEqual(blob.count('http://'), blob.count(run.other_origin()))
            self.assertEqual(run.rules_text().count('prefix_rule('), 2)
            self.assertEqual(set(re.findall(r'pattern = \[([^\]]*)\]', run.rules_text())),
                             {'"/usr/bin/touch"', '"touch"'})

    def test_project_and_home_files_go_only_where_named(self):
        with L.Run(self.scratch, '/nonexistent/codex', trusted_project=True) as run:
            for relative in L.TRUST_FILES:
                target = run.write_trust_file(relative, 'invented\n')
                self.assertEqual(target, run.project / relative)
                self.assertEqual(target.read_text(), 'invented\n')
            run.write_trust_file('.codex/config.toml', 'replaced\n')
            self.assertEqual((run.project / '.codex' / 'config.toml').read_text(), 'replaced\n')
            for relative in L.HOME_FILES:
                self.assertEqual(run.write_home_file(relative, 'invented\n'), run.home / relative)
            for bad in ('../outside/x', '.codex/other.toml', 'sub/other.md', 'other/AGENTS.md', '/etc/x', 'config.toml'):
                with self.subTest(bad=bad), self.assertRaises(L.Refused):
                    run.write_trust_file(bad, 'x')
            for bad in ('../x', 'auth.json', 'rules/other.rules'):
                with self.subTest(bad=bad), self.assertRaises(L.Refused):
                    run.write_home_file(bad, 'x')
        self.assertFalse(run.root.exists())

    def test_the_second_rounds_files_parse_and_name_only_the_marker_commands(self):
        import tomllib
        with L.Run(self.scratch, '/nonexistent/codex', trusted_project=True) as run:
            person = tomllib.loads(run.person_mcp_toml())['mcp_servers']
            self.assertEqual(set(person), {L.MCP_STDIO, L.MCP_PERSON})  # one shares the project's server's name
            self.assertEqual(['/bin/sh'] + person[L.MCP_STDIO]['args'], run.marker_argv('mcp-person-same'))
            self.assertEqual(['/bin/sh'] + person[L.MCP_PERSON]['args'], run.marker_argv('mcp-person-other'))
            helper = tomllib.loads(run.headers_helper_toml())['mcp_servers'][L.MCP_HELPER]
            self.assertEqual(helper['url'], 'http://127.0.0.1:%d/mcp-helper' % run.other.port)
            self.assertEqual(helper['http_headers_helper'], run.marker_command('mcp-headers-helper'))
            # Codex runs a headers helper as `sh -c <command>`: so run, it appends its marker and prints nothing.
            done = subprocess.run(['sh', '-c', helper['http_headers_helper']], capture_output=True,
                                  env={'PATH': L.SYSTEM_PATH})
            self.assertEqual((done.returncode, done.stdout, run.marker_runs('mcp-headers-helper')), (0, b'', 1))
            with self.assertRaises(tomllib.TOMLDecodeError):
                tomllib.loads(run.malformed_toml())
            for which, folder in (('root', run.project), ('sub', run.subfolder())):
                text = run.agents_md(which)
                self.assertIn(run.trust_markers['agents-' + which], text)
                target = run.write_trust_file('AGENTS.md' if which == 'root' else 'sub/AGENTS.md', text)
                self.assertEqual(target, folder / 'AGENTS.md')
            self.assertEqual(run.subfolder(), run.project / L.SUBFOLDER)
            markers = list(run.trust_markers.values())
            self.assertEqual(len(set(markers)), len(markers))
            self.assertFalse(any(a != b and a in b for a in markers for b in markers))  # none hides another
            denied = run.denied_read_folder()
            self.assertEqual((denied.parent, list(denied.iterdir()), run.denied_read_folder()),
                             (run.root / 'outside', [], denied))

    def test_the_stub_notes_where_each_watched_marker_sits(self):
        stub = L.ScriptedStub()
        self.addCleanup(stub.close)
        stub.answer(body('LEVEL[k] go'))
        self.assertEqual(stub.placements, [{}])  # nothing watched, nothing noted, still aligned
        stub.watched = ('INVENTED-A', 'INVENTED-B', 'INVENTED-C')
        carrying = body('LEVEL[k] go INVENTED-B', outputs=[('c1', 'an output naming INVENTED-A')])
        carrying['input'][0]['content'][0]['text'] = 'invented INVENTED-A and INVENTED-A again'
        carrying['input'][0]['id'] = 'INVENTED-C'  # in an entry's other field, not in the text the model reads
        carrying['instructions'] = 'base INVENTED-B'
        carrying['model'] = L.MODEL
        stub.record_model = True
        stub.answer(carrying)
        self.assertEqual(len(stub.placements), len(stub.requests))
        self.assertEqual(stub.placements[-1], {
            'INVENTED-A': {'count': 2, 'where': ['input[0]:developer'], 'elsewhere': 1},  # and once in an output
            'INVENTED-B': {'count': 2, 'where': ['instructions', 'input[1]:user'], 'elsewhere': 0},
            'INVENTED-C': {'count': 0, 'where': [], 'elsewhere': 1}})
        self.assertNotIn('invented', json.dumps(stub.placements))  # positions only, never the text
        self.assertEqual(stub.requests[-1]['model'], L.MODEL)  # the model each request names is kept

    def test_a_client_that_fails_after_its_server_started_leaves_nothing_running(self):
        """Between the server's start and the Client's return nobody else holds it: a failure there ends it."""
        started = []
        real = subprocess.Popen

        def popen(argv, **kwargs):  # a stand-in that stays up until its input closes, in place of Codex
            started.append(real(['/bin/sh', '-c', 'read unused'], **kwargs))
            return started[-1]
        with L.Run(self.scratch, '/nonexistent/codex', trusted_project=True) as run:
            with mock.patch.object(L.subprocess, 'Popen', popen), \
                    mock.patch.object(L, 'observe_process', side_effect=RuntimeError('invented failure')):
                with self.assertRaisesRegex(RuntimeError, 'invented failure'):
                    L.Client(run)
            self.assertEqual((len(started), run.clients), (1, []))
            proc = started[0]
            self.assertIsNotNone(proc.poll())  # ended and reaped
            self.assertFalse(L.group_has_members(proc.pid))
            self.assertTrue(proc.stdin.closed and proc.stdout.closed)

    def test_the_second_listener_is_closed_when_it_cannot_start_serving(self):
        import socket
        real, made = L.ScriptedStub.serve, []

        def serve(stub):
            made.append(stub)
            if len(made) == 2:  # the second listener's
                raise OSError('invented serving failure')
            return real(stub)
        run = L.Run(self.scratch, '/nonexistent/codex', trusted_project=True)
        with mock.patch.object(L.ScriptedStub, 'serve', serve):
            with self.assertRaisesRegex(OSError, 'invented serving failure'):
                run.__enter__()
        self.assertIs(run.other, made[1])  # registered before it was to serve, so the run's cleanup closed it
        self.assertFalse(run.root.exists())
        for stub in made:
            self.assertEqual(stub.server.socket.fileno(), -1)
            with self.assertRaises(OSError):
                socket.create_connection(('127.0.0.1', stub.port), timeout=1).close()

    def test_closing_a_listener_ends_a_connection_its_handler_holds(self):
        import socket
        stub = L.ScriptedStub()
        self.addCleanup(stub.close)
        raw = socket.create_connection(('127.0.0.1', stub.port), timeout=5)
        self.addCleanup(raw.close)  # sends nothing: its handler waits for a request line that never comes
        deadline = time.monotonic() + 3
        while not stub.active and time.monotonic() < deadline:
            time.sleep(0.05)
        self.assertEqual((stub.connections, len(stub.active)), (1, 1))
        began = time.monotonic()
        stub.close()
        self.assertLess(time.monotonic() - began, 5)
        try:
            ended = raw.recv(1) == b''
        except ConnectionResetError:
            ended = True
        self.assertTrue(ended)  # the held connection was ended, not left open
        self.assertEqual(stub.active, set())

    def test_the_touch_and_variable_commands(self):
        with L.Run(self.scratch, '/nonexistent/codex', trusted_project=True) as run:
            commands = run.commands()
            self.assertEqual(run.stub.allowed_commands, set(commands.values()))
            self.assertIs(run.other.allowed_commands, run.stub.allowed_commands)
            for key, folder in (('touch-out', run.root / 'outside'), ('touch-in', run.project)):
                path = run.paths()[key]
                self.assertEqual(path.parent, folder)
                self.assertEqual(shlex.split(commands[key]), ['/usr/bin/touch', str(path)])
                self.assertEqual(run.touch_refusals()[key], {'touch: %s: Operation not permitted' % path})
                subprocess.run(['/bin/sh', '-c', commands[key]], check=True)
                self.assertTrue(path.exists())
            for env, printed in (({}, 'startup=unset\nvariable=unset'),
                                 ({L.TRUST_ENV: 'invented'}, 'startup=unset\nvariable=invented'),
                                 ({L.TRUST_ENV: ''}, 'startup=unset\nvariable='),
                                 ({L.STARTUP_ENV: 'ran'}, 'startup=ran\nvariable=unset')):
                done = subprocess.run(['/bin/sh', '-c', commands['env']], capture_output=True, text=True, env=env)
                self.assertEqual((done.returncode, done.stdout), (0, printed))

    def test_the_second_listener_is_loopback_counts_every_connection_and_closes_with_the_run(self):
        import socket
        with L.Run(self.scratch, '/nonexistent/codex', trusted_project=True) as run:
            other = run.other
            self.assertTrue(other.base_url.startswith('http://127.0.0.1:'))
            self.assertEqual(other.server.server_address[0], '127.0.0.1')
            self.assertEqual((other.connections, other.contacts), (0, []))
            with socket.create_connection(('127.0.0.1', other.port), timeout=3) as raw:
                raw.sendall(b'PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n')  # not HTTP/1.1, yet counted
                raw.recv(64)
            conn = http.client.HTTPConnection('127.0.0.1', other.port, timeout=3)
            conn.request('POST', '/mcp', body=b'{}', headers={'Content-Type': 'application/json'})
            self.assertEqual(conn.getresponse().status, 404)
            conn.close()
            deadline = time.monotonic() + 3
            while other.connections < 2 and time.monotonic() < deadline:
                time.sleep(0.05)
            self.assertEqual(other.connections, 2)
            self.assertEqual(other.contacts, [('POST', '/mcp')])
            self.assertEqual(run.stub.connections, 0)  # the stub's own count is apart
            port = other.port
        with self.assertRaises(OSError):
            socket.create_connection(('127.0.0.1', port), timeout=1).close()


class Judging(unittest.TestCase):
    """The fixture can fail: each way a call can go unobserved, or be misread, refuses or fails."""

    def judge(self, output, call='c', issued=('c',), not_offered=(), items=('c',), asked=(), turn='completed',
              target='/run/project/w-in', item_status=None, item_exit=None):
        return L.judge(call, set(issued), set(not_offered), output, set(items), set(asked), turn, target=target,
                       item_status=item_status, item_exit=item_exit)

    def test_the_six_outcomes_each_need_their_own_evidence(self):
        ok = 'Chunk ID: 1\nProcess exited with code 0\nOutput:\n'
        refused = 'Process exited with code 1\nOutput:\nzsh:1: operation not permitted: /run/project/w-in\n'
        self.assertEqual(self.judge(ok).kind, L.SUCCEEDED)
        self.assertEqual(self.judge(refused, items=()).kind, L.SANDBOX_REFUSED)
        network = 'Process exited with code 3\nOutput:\nconnect failed: Operation not permitted\n'
        self.assertEqual(self.judge(network, target=L.NETWORK).kind, L.SANDBOX_REFUSED)
        bash = 'Process exited with code 1\nOutput:\n/bin/bash: /run/project/w-in: Operation not permitted\n'
        self.assertEqual(self.judge(bash, items=()).kind, L.SANDBOX_REFUSED)
        self.assertEqual(self.judge('exec_command failed: Rejected("rejected by user")', items=(), asked=('c',),
                                    item_status='declined').kind, L.DECLINED)
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

    def test_the_readers_three_misclassifications_are_not_refusals(self):
        # A path holding the words, failing for another reason.
        words = '/run/operation not permitted/w-in'
        other = 'Process exited with code 1\nOutput:\nzsh:1: no such file or directory: %s\n' % words
        self.assertEqual(self.judge(other, items=(), target=words).kind, L.FAILED)
        with self.assertRaisesRegex(AssertionError, 'INCONCLUSIVE'):
            L.expect(self.judge(other, items=(), target=words), L.SANDBOX_REFUSED)
        # A command that prints the words and exits 1.
        printed = 'Process exited with code 1\nOutput:\nsomething: operation not permitted\n'
        self.assertEqual(self.judge(printed, items=()).kind, L.FAILED)
        # The refusal line for another target is not a refusal of this one.
        elsewhere = 'Process exited with code 1\nOutput:\nzsh:1: operation not permitted: /run/outside/w-out\n'
        self.assertEqual(self.judge(elsewhere, items=()).kind, L.FAILED)
        # An item of another turn or type with the same id cannot carry a success: only this turn's
        # commandExecution ids are passed in, so an exit 0 without one refuses.
        with self.assertRaises(L.Refused):
            self.judge('Process exited with code 0\nOutput:\n', items=())

    def test_a_declined_item_carrying_an_exit_code_refuses(self):
        # The third reading's break: a declined item with exit code 0.
        with self.assertRaises(L.Refused):
            self.judge('Rejected("rejected by user")', items=('c',), asked=('c',), item_status='declined', item_exit=0)
        declined = self.judge('Rejected("rejected by user")', items=('c',), asked=('c',), item_status='declined')
        self.assertIsNone(declined.evidence['item_exit'])

    def test_a_forks_approval_inverted_fails(self):
        # The third reading's break: a fork's effective approval inverted. The forced call keeps its escalation,
        # so the escalation's outcome shows the approval in effect, and the other outcome fails the check.
        script = L.forced_exec_script('call_f', 'printf ok > /x', escalate=True)
        args = json.loads(script({}, {}, None)[0]['arguments'])
        self.assertEqual(args['sandbox_permissions'], 'require_escalated')
        rejected = self.judge('approval policy is Never; reject command', items=())
        declined = self.judge('Rejected("rejected by user")', items=('c',), asked=('c',), item_status='declined')
        with self.assertRaises(AssertionError):
            L.expect(rejected, L.DECLINED)  # a fork reporting on-request whose approval is in fact never
        with self.assertRaises(AssertionError):
            L.expect(declined, L.REJECTED)  # and the reverse

    def test_a_declined_call_whose_item_ran_refuses(self):
        with self.assertRaises(L.Refused):
            self.judge('Rejected("rejected by user")', items=('c',), asked=('c',), item_status='completed')

    def test_a_turn_that_did_not_complete_is_unresolved(self):
        for turn in (None, 'interrupted', 'failed'):
            with self.assertRaises(L.Refused):
                self.judge('Process exited with code 1\nOutput:\noperation not permitted\n', turn=turn)

    def test_given_lines_alone_make_a_refusal(self):
        lines = L.Lines({'mv: rename /a to /b: Operation not permitted'})
        refused = self.judge('Process exited with code 1\nOutput:\nmv: rename /a to /b: Operation not permitted\n',
                             target=lines, items=())
        self.assertEqual(refused.kind, L.SANDBOX_REFUSED)
        other = self.judge('Process exited with code 1\nOutput:\nmv: rename /a to /c: Operation not permitted\n',
                           target=lines, items=())
        self.assertEqual(other.kind, L.FAILED)

    def test_an_item_that_contradicts_a_refusal_refuses(self):
        refused = 'Process exited with code 1\nOutput:\nzsh:1: operation not permitted: /run/project/w-in\n'
        self.assertEqual(self.judge(refused, items=()).kind, L.SANDBOX_REFUSED)  # no item: a refusal
        self.assertEqual(self.judge(refused, item_status='failed', item_exit=1).kind, L.SANDBOX_REFUSED)
        for status, exit_code in (('completed', 0), ('completed', 1), ('failed', 0), (None, 0)):
            with self.assertRaises(L.Refused, msg=(status, exit_code)):
                self.judge(refused, item_status=status, item_exit=exit_code)

    def test_a_failure_without_the_sandbox_text_is_not_a_refusal(self):
        failed = self.judge('Process exited with code 7\nOutput:\ncurl: (7) Failed to connect\n', items=())
        self.assertEqual(failed.kind, L.FAILED)
        with self.assertRaises(AssertionError):
            L.expect(failed, L.SANDBOX_REFUSED)

    def test_outcomes_missing_a_stage_refuse(self):
        with self.assertRaises(L.Refused):  # exit 0 without its command item
            self.judge('Process exited with code 0\nOutput:\n', items=())
        with self.assertRaises(L.Refused):  # a decline with no request for this call
            self.judge('Rejected("rejected by user")', items=(), asked=('other',), item_status='declined')
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
        broken.proc.poll.return_value = 0
        broken.started_at = None
        run.clients.append(broken)
        with mock.patch.object(L, 'group_has_members', return_value=False):
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

    def server(self, poll=0, started_at=None, pid=999999, pgid=4242):
        client = mock.Mock()
        client.proc.pid, client.pgid, client.started_at = pid, pgid, started_at
        client.proc.poll.return_value = poll
        return client

    def test_a_server_of_the_run_left_running_fails_naming_it_by_number(self):
        """Known by its number and recorded start time, and its group by a signal 0: no command line is read."""
        run = L.Run(self.scratch, '/nonexistent/codex')
        run.__enter__()
        try:
            with mock.patch.object(L, 'group_has_members', return_value=False):
                run.clients = [self.server(poll=None)]
                with self.assertRaisesRegex(L.Refused, 'server 999999: still running'):
                    run.nothing_remains(wait=0.3)
                run.clients = [self.server(started_at='at')]
                with mock.patch.object(L, 'still_running', return_value=True):
                    with self.assertRaisesRegex(L.Refused, 'server 999999: still running'):
                        run.nothing_remains(wait=0.3)
                with mock.patch.object(L, 'still_running', side_effect=L.Unobserved('invented ps failure')):
                    with self.assertRaisesRegex(L.Refused, 'server 999999: invented ps failure'):
                        run.nothing_remains(wait=0.3)
                with mock.patch.object(L, 'still_running', return_value=False):  # gone, or the number used again
                    run.nothing_remains(wait=0.3)
            run.clients = [self.server()]
            with mock.patch.object(L, 'group_has_members', return_value=True):
                with self.assertRaisesRegex(L.Refused, 'process group 4242 has a member'):
                    run.nothing_remains(wait=0.3)
            with mock.patch.object(L, 'group_has_members', return_value=False):
                run.nothing_remains(wait=0.3)
            with mock.patch.object(L, 'subprocess') as subprocess_module:
                with mock.patch.object(L, 'group_has_members', return_value=False):
                    run.nothing_remains(wait=0.3)
                subprocess_module.run.assert_not_called()  # no process list is read
        finally:
            run.clients = []
            run.__exit__(None, None, None)

    def test_a_group_is_checked_by_a_signal_to_it(self):
        def gone(pgid, sig):
            raise ProcessLookupError()
        def denied(pgid, sig):
            raise PermissionError()
        self.assertFalse(L.group_has_members(4242, killpg=gone, members=lambda pgid: self.fail('not counted')))
        self.assertTrue(L.group_has_members(4242, killpg=lambda pgid, sig: None, members=lambda pgid: self.fail('not counted')))
        self.assertTrue(L.group_has_members(4242, killpg=denied, members=lambda pgid: 1))
        self.assertFalse(L.group_has_members(4242, killpg=denied, members=lambda pgid: 0))

    def test_a_permission_error_from_the_signal_fails_while_the_group_has_members(self):
        client = L.Client.__new__(L.Client)
        client.pgid = 4242
        client.proc = mock.Mock()
        client.proc.poll.return_value = 0
        with mock.patch.object(L.os, 'killpg', side_effect=PermissionError('invented')):
            with mock.patch.object(L, 'group_members', return_value=1):
                with self.assertRaises(PermissionError):
                    client.kill_group()
            with mock.patch.object(L, 'group_members', return_value=0):
                client.kill_group()  # the group has no members: nothing is left to signal

    def test_the_whole_group_is_signalled_even_after_its_leader_exited(self):
        client = L.Client.__new__(L.Client)
        client.pgid = 4242
        client.proc = mock.Mock()
        client.proc.poll.return_value = 0  # the leader has exited
        with mock.patch.object(L.os, 'killpg') as killpg:
            client.kill_group()
        killpg.assert_called_once_with(4242, L.signal.SIGKILL)


class NetworkProbe(unittest.TestCase):
    def test_one_deadline_bounds_the_whole_probe(self):
        # A single alarm, set once before the connection: it covers connect and read together and is never reset.
        self.assertEqual(L.NET_PROBE.count('alarm'), 1)
        self.assertLess(L.NET_PROBE.index('alarm 3'), L.NET_PROBE.index('IO::Socket::INET->new'))


class Draining(unittest.TestCase):
    """A frame written before the server's output ends is taken before the output is closed, and a reader that
    stops for any other reason than the end of the output fails."""

    def client_on(self, stream):
        client = L.Client.__new__(L.Client)
        client.lock = threading.Lock()
        client.changed = threading.Condition(client.lock)
        client.notes, client.replies, client.server_requests, client.held = [], {}, [], []
        client.tool_call_policy = 'hold'
        client.writer = threading.Lock()
        client.proc = mock.Mock()
        client.proc.stdout = stream
        client.reader_end = None
        client.reader = threading.Thread(target=client.read, daemon=True)
        return client

    def test_a_call_raised_during_teardown_is_not_lost(self):
        # The third reading's break: a call re-raised as the server ends. Its frame must be read before any
        # assertion that no such call arrived.
        read_end, write_end = os.pipe()
        late = json.dumps({'jsonrpc': '2.0', 'id': 7, 'method': 'item/tool/call',
                           'params': {'threadId': 't', 'callId': 'call_outstanding', 'turnId': 'u',
                                      'tool': L.APP_TOOL, 'arguments': {}}}) + '\n'
        os.write(write_end, late.encode())
        os.close(write_end)
        client = self.client_on(os.fdopen(read_end, 'rb'))
        client.reader.start()
        client.drain()
        self.assertEqual([r['params']['callId'] for r in client.server_requests], ['call_outstanding'])

    def test_a_reader_that_failed_is_not_taken_for_the_end(self):
        class Broken:
            def __iter__(self):
                raise OSError('invented read failure')
        client = self.client_on(Broken())
        client.reader.start()
        with self.assertRaisesRegex(L.Refused, 'invented read failure'):
            client.drain()

    def test_stop_drains_before_closing_the_output(self):
        read_end, write_end = os.pipe()
        os.write(write_end, (json.dumps({'jsonrpc': '2.0', 'method': 'turn/completed', 'params': {}}) + '\n').encode())
        os.close(write_end)
        client = self.client_on(os.fdopen(read_end, 'rb'))
        client.pgid = 424242
        client.proc.poll.return_value = 0
        client.proc.stdin = io.BytesIO()
        client.stderr = io.BytesIO()
        client.reader.start()
        with mock.patch.object(L.os, 'killpg', side_effect=ProcessLookupError):
            client.stop()
        self.assertEqual([n['method'] for n in client.notes], ['turn/completed'])


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



class Recorder(unittest.TestCase):
    """The recording refusal that stands in for the closed proxy port: it refuses everything, and keeps only where
    each request was going."""

    def test_it_records_the_target_only_and_refuses(self):
        import socket
        recorder = L.RecordingRefusal()
        try:
            port = int(recorder.url.rsplit(':', 1)[1])
            for request in (b'CONNECT chatgpt.com:443 HTTP/1.1\r\nHost: chatgpt.com:443\r\n\r\n',
                            b'GET http://example.invalid:8080/secret/path?q=1 HTTP/1.1\r\nAuthorization: x\r\n\r\n'):
                with socket.create_connection(('127.0.0.1', port), timeout=5) as conn:
                    conn.sendall(request)
                    self.assertTrue(conn.recv(100).startswith(b'HTTP/1.1 502'))
            for _ in range(50):
                if len(recorder.since(0)) == 2:
                    break
                import time
                time.sleep(0.05)
            self.assertEqual(recorder.since(0), [('CONNECT', 'chatgpt.com:443'), ('GET', 'http://example.invalid:8080')])
        finally:
            recorder.close()

    def test_a_run_given_a_recorder_points_every_proxy_name_at_it(self):
        recorder = L.RecordingRefusal()
        try:
            run = L.Run(tempfile.gettempdir(), '/bin/true', proxy=recorder)
            env = run.environment()
            self.assertEqual({env[name] for name in L.PROXY_NAMES}, {recorder.url})
            self.assertEqual(env['NO_PROXY'], L.EXEMPT)
            plain = L.Run(tempfile.gettempdir(), '/bin/true').environment()
            self.assertEqual({plain[name] for name in L.PROXY_NAMES}, {L.PROXY})
        finally:
            recorder.close()

if __name__ == '__main__':
    unittest.main(verbosity=2)


class ProcessObservation(unittest.TestCase):
    """The running-command rows observe a process by number alone. Gone needs positive evidence; a failed
    observation is unknown, never gone."""

    class Done:
        def __init__(self, code, out):
            self.returncode, self.stdout = code, out

    def kill_alive(self, pid, sig):
        return None

    def kill_gone(self, pid, sig):
        raise ProcessLookupError

    def test_present_and_gone_on_positive_evidence(self):
        self.assertEqual(L.observe_process(7, kill=self.kill_alive, run=lambda *a, **k: self.Done(0, 'Sat Nov 14 10:00:00 2026\n')),
                         ('present', 'Sat Nov 14 10:00:00 2026'))
        self.assertEqual(L.observe_process(7, kill=self.kill_gone, run=lambda *a, **k: self.fail('no ps when gone')), ('gone', None))

    def test_ps_failing_or_printing_nothing_is_unknown_not_gone(self):
        for done in (self.Done(1, ''), self.Done(0, ''), self.Done(0, '  \n')):
            with self.subTest(code=done.returncode, out=done.stdout):
                with self.assertRaises(L.Unobserved):
                    L.observe_process(7, kill=self.kill_alive, run=lambda *a, **k: done)

    def test_a_process_that_ends_between_the_two_observations_is_established_gone(self):
        calls = []
        def kill(pid, sig):
            calls.append(sig)
            if len(calls) > 1:
                raise ProcessLookupError
        self.assertEqual(L.observe_process(7, kill=kill, run=lambda *a, **k: self.Done(1, '')), ('gone', None))

    def test_a_row_relying_on_a_failed_observation_fails(self):
        def failed(pid):
            raise L.Unobserved('invented')
        with self.assertRaises(L.Unobserved):
            L.still_running(7, 'at', observe=failed)

    def test_a_reused_number_is_not_the_same_process(self):
        self.assertFalse(L.still_running(7, 'earlier', observe=lambda pid: ('present', 'later')))
        self.assertTrue(L.still_running(7, 'same', observe=lambda pid: ('present', 'same')))

    def test_cleanup_tries_to_end_an_unobserved_process(self):
        ended = []
        def failed(pid):
            raise L.Unobserved('invented')
        L.end_known({'a': (7, 'at')}, observe=failed, kill=lambda pid, sig: ended.append(pid))
        self.assertEqual(ended, [7])
        ended.clear()
        L.end_known({'a': (7, 'at')}, observe=lambda pid: ('gone', None), kill=lambda pid, sig: ended.append(pid))
        self.assertEqual(ended, [])
