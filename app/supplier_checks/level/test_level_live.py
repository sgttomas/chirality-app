#!/usr/bin/env python3
"""What the pinned Codex 0.167.0 does with sandbox and approval settings, asserted fact by fact.

Live: each test starts the pinned app server against the loopback stub in `level_fixture.py`, with a
fresh root that is removed afterwards. Skipped unless CHIRALITY_CODEX_BIN names the pinned binary
(its digest is checked against GENERATION.json before every start). LEVEL_SCRATCH names the folder
the roots are made in; the system temporary folder is used when it is unset. LEVEL_HOLD_SECONDS
sets how long a call to an App-supplied tool is left unanswered (default 120).

Run from `app/`: python3 supplier_checks/level/test_level_live.py
The facts each test guards are listed in README.md beside this file.
"""
import json
import os
import sys
import tempfile
import time
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import level_fixture as L  # noqa: E402

BINARY = os.environ.get('CHIRALITY_CODEX_BIN')
SCRATCH = os.environ.get('LEVEL_SCRATCH') or tempfile.gettempdir()
HOLD = float(os.environ.get('LEVEL_HOLD_SECONDS') or 120)

WW = {'type': 'workspaceWrite'}
SUPERVISED = {'approvalPolicy': 'untrusted', 'sandboxPolicy': {'type': 'readOnly'}}
EDITS_NET_OFF = {'approvalPolicy': 'on-request', 'sandboxPolicy': dict(WW, networkAccess=False)}
EDITS_NET_ON = {'approvalPolicy': 'on-request', 'sandboxPolicy': dict(WW, networkAccess=True)}
FULL = {'approvalPolicy': 'never', 'sandboxPolicy': {'type': 'dangerFullAccess'}}
READ_ONLY = {'approvalPolicy': 'on-request', 'sandboxPolicy': {'type': 'readOnly'}}
COMMAND_APPROVAL = 'item/commandExecution/requestApproval'
APP_TOOL_SPEC = [{'type': 'function', 'name': L.APP_TOOL, 'description': 'Invented records reader for a fixture.',
                  'inputSchema': {'type': 'object', 'properties': {}, 'additionalProperties': False}}]


def live_binary(binary, required):
    """The admitted binary. Without one, skip; but where the live tests are required (LEVEL_REQUIRE_LIVE=1, set
    by the CI step meant to run them), a missing or unpinned binary fails instead, so the step cannot pass with
    every test skipped."""
    if not binary:
        if required:
            raise L.Refused('LEVEL_REQUIRE_LIVE is set but CHIRALITY_CODEX_BIN is not')
        raise unittest.SkipTest('CHIRALITY_CODEX_BIN is not set; the live level fixtures need the pinned Codex')
    return L.admitted_binary(binary)  # an unpinned binary refuses whether or not the tests are required


def setUpModule():
    live_binary(BINARY, os.environ.get('LEVEL_REQUIRE_LIVE') == '1')


def reported(reply):
    return {k: reply.get(k) for k in ('approvalPolicy', 'sandbox')}


def probe(run, client, thread, key, escalate=False, forced=False, **settings):
    """Run one fixed command in one turn. Returns what happened, by effect, never by message text."""
    path = run.paths().get(key)
    if path is not None and path.exists():
        path.unlink()
    nets, seen = run.stub.net_probes, len(client.server_requests)
    call_id = 'call_%s_%d' % (key, len(run.stub.requests))
    command = run.commands()[key]
    if forced:  # call exec_command whether or not the request offers it
        def script(body, outputs, stub):
            if call_id in outputs:
                return [L.message('Done.', 'msg_' + call_id)]
            return [{'type': 'function_call', 'name': 'exec_command', 'call_id': call_id, 'id': 'fc_' + call_id,
                     'arguments': json.dumps({'cmd': command})}]
        run.stub.scripts[call_id] = script
    else:
        run.stub.scripts[call_id] = L.command_script(call_id, command, escalate=escalate)
    turn, done = client.turn(thread, 'LEVEL[%s] go' % call_id, **settings)
    output = run.stub.outputs.get(call_id)
    return {
        'effect': path.exists() if path is not None else run.stub.net_probes > nets,
        'requests': [(r['method'], r['thread']) for r in client.server_requests[seen:]],
        'turn': done and done['turn']['status'],
        'ran': output is not None and 'exited with code' in output,
        'exit_zero': output is not None and 'exited with code 0' in output,
        'command_items': len(client.items(thread, turn, 'commandExecution')),
        'output': output,
    }


class Presets(unittest.TestCase):
    """Case 1: each preset against the fixed writes, the network probe and an escalation request.

    The level is sent on every turn (turn/start approvalPolicy and sandboxPolicy), except for
    "nothing sent", which is what the App sends today."""

    def matrix(self, settings, escalated=True):
        with L.Run(SCRATCH, BINARY, slash_tmp=True, git_marker=True) as run:
            client = run.start()
            reply = client.start_thread()
            thread = reply['thread']['id']
            rows = {key: probe(run, client, thread, key, **settings)
                    for key in ('in', 'out', 'tmpdir', 'slashtmp', 'git', 'net')}
            if escalated:
                rows['escalated'] = probe(run, client, thread, 'out', escalate=True, **settings)
            return reply, thread, rows

    def assertWrites(self, rows, expected):
        self.assertEqual({k: rows[k]['effect'] for k in expected}, expected)

    def assertNoRequests(self, rows, keys):
        for key in keys:
            self.assertEqual(rows[key]['requests'], [], key)

    def test_nothing_sent_is_on_request_read_only_and_a_refused_write_asks_no_one(self):
        reply, thread, rows = self.matrix({})
        self.assertEqual(reply['approvalPolicy'], 'on-request')
        self.assertEqual(reply['sandbox'], {'type': 'readOnly', 'networkAccess': False})
        self.assertEqual((reply.get('activePermissionProfile') or {}).get('id'), ':read-only')
        self.assertWrites(rows, {'in': False, 'out': False, 'tmpdir': False, 'slashtmp': False, 'git': False,
                                 'net': False})
        # Each refused write ran, failed, and raised no request to the client.
        self.assertNoRequests(rows, ('in', 'out', 'tmpdir', 'slashtmp', 'git', 'net'))
        for key in ('in', 'out', 'tmpdir', 'slashtmp', 'git'):
            self.assertTrue(rows[key]['ran'] and not rows[key]['exit_zero'], key)
        # Only a command that itself asks for escalation reaches the client, on its own thread.
        self.assertEqual(rows['escalated']['requests'], [(COMMAND_APPROVAL, thread)])
        self.assertFalse(rows['escalated']['effect'])

    def test_a_write_the_sandbox_refused_completes_no_command_item(self):
        with L.Run(SCRATCH, BINARY) as run:
            client = run.start()
            thread = client.start_thread()['thread']['id']
            refused = probe(run, client, thread, 'out')
            ran = probe(run, client, thread, 'net')  # fails by exit code, not by a refused write
        self.assertTrue(refused['ran'] and not refused['exit_zero'])
        self.assertEqual(refused['command_items'], 0)
        self.assertEqual(ran['command_items'], 1)

    def test_supervised_asks_before_every_command_and_a_declined_one_does_not_run(self):
        _, thread, rows = self.matrix(SUPERVISED)
        for key, row in rows.items():
            self.assertEqual(row['requests'], [(COMMAND_APPROVAL, thread)], key)
            self.assertFalse(row['effect'], key)

    def test_supervised_asks_before_a_plain_read_too(self):
        with L.Run(SCRATCH, BINARY) as run:
            client = run.start()
            thread = client.start_thread()['thread']['id']
            run.stub.scripts['ls'] = L.command_script('call_ls', run.commands()['read'])
            client.turn(thread, 'LEVEL[ls] go', **SUPERVISED)
            self.assertEqual([(r['method'], r['thread']) for r in client.server_requests], [(COMMAND_APPROVAL, thread)])
            self.assertNotIn('exited with code', run.stub.outputs.get('call_ls') or '')

    def test_edits_with_network_off(self):
        _, thread, rows = self.matrix(EDITS_NET_OFF)
        self.assertWrites(rows, {'in': True, 'out': False, 'tmpdir': True, 'slashtmp': True, 'git': False,
                                 'net': False})
        self.assertNoRequests(rows, ('in', 'out', 'tmpdir', 'slashtmp', 'git', 'net'))
        self.assertEqual(rows['escalated']['requests'], [(COMMAND_APPROVAL, thread)])

    def test_edits_with_network_on(self):
        _, thread, rows = self.matrix(EDITS_NET_ON)
        self.assertWrites(rows, {'in': True, 'out': False, 'tmpdir': True, 'slashtmp': True, 'git': False,
                                 'net': True})
        self.assertNoRequests(rows, ('in', 'out', 'tmpdir', 'slashtmp', 'git', 'net'))
        self.assertEqual(rows['escalated']['requests'], [(COMMAND_APPROVAL, thread)])

    def test_full_access_writes_everywhere_and_an_escalation_request_is_refused_by_codex(self):
        _, _, rows = self.matrix(FULL)
        self.assertWrites(rows, {'in': True, 'out': True, 'tmpdir': True, 'slashtmp': True, 'git': True,
                                 'net': True})
        self.assertNoRequests(rows, rows)
        self.assertFalse(rows['escalated']['effect'])
        self.assertFalse(rows['escalated']['ran'])

    def test_edits_that_never_ask_fail_whatever_needs_more_and_raise_nothing(self):
        """The examinations' level: workspace write, network off, both temporary folders excluded,
        approval "never"."""
        settings = {'approvalPolicy': 'never', 'sandboxPolicy': dict(WW, networkAccess=False, excludeSlashTmp=True,
                                                                     excludeTmpdirEnvVar=True)}
        _, _, rows = self.matrix(settings)
        self.assertWrites(rows, {'in': True, 'out': False, 'tmpdir': False, 'slashtmp': False, 'git': False,
                                 'net': False})
        self.assertNoRequests(rows, rows)
        for key in ('out', 'tmpdir', 'slashtmp', 'git', 'net'):
            self.assertTrue(rows[key]['ran'] and not rows[key]['exit_zero'], key)
        self.assertFalse(rows['escalated']['effect'])
        self.assertFalse(rows['escalated']['ran'])  # refused by Codex before it runs

    def test_the_two_temporary_folder_exclusions(self):
        _, _, slash = self.matrix(dict(EDITS_NET_OFF, sandboxPolicy=dict(WW, excludeSlashTmp=True)), escalated=False)
        _, _, tmpdir = self.matrix(dict(EDITS_NET_OFF, sandboxPolicy=dict(WW, excludeTmpdirEnvVar=True)),
                                   escalated=False)
        self.assertWrites(slash, {'in': True, 'tmpdir': True, 'slashtmp': False})
        self.assertWrites(tmpdir, {'in': True, 'tmpdir': False, 'slashtmp': True})

    def test_an_extra_writable_root(self):
        with L.Run(SCRATCH, BINARY) as run:
            client = run.start()
            thread = client.start_thread()['thread']['id']
            settings = dict(EDITS_NET_OFF, sandboxPolicy=dict(WW, writableRoots=[str(run.root / 'outside')]))
            extra = probe(run, client, thread, 'extra', **settings)
            out = probe(run, client, thread, 'in', **settings)
        self.assertTrue(extra['effect'])
        self.assertTrue(out['effect'])


class Carriers(unittest.TestCase):
    """Case 2: where a setting can be sent, whether it takes effect, and what the replies report."""

    def test_thread_start_turn_start_and_resume(self):
        with L.Run(SCRATCH, BINARY) as run:
            client = run.start()
            started = client.start_thread(approvalPolicy='never', sandbox='danger-full-access')
            a = started['thread']['id']
            self.assertEqual(reported(started), {'approvalPolicy': 'never', 'sandbox': {'type': 'dangerFullAccess'}})
            self.assertTrue(probe(run, client, a, 'out')['effect'])

            b = client.start_thread()['thread']['id']
            self.assertTrue(probe(run, client, b, 'out', **FULL)['effect'])
            # A turn's setting holds for the next turn sent with none.
            self.assertTrue(probe(run, client, b, 'out')['effect'])
            # thread/read reports no setting at all.
            self.assertEqual(reported(client.result('thread/read', {'threadId': b})),
                             {'approvalPolicy': None, 'sandbox': None})
            client.stop()

            again = run.start()
            for thread in (a, b):  # resume with none keeps the last setting, set by thread start or by turn
                resumed = again.result('thread/resume', {'threadId': thread})
                self.assertEqual(reported(resumed), {'approvalPolicy': 'never', 'sandbox': {'type': 'dangerFullAccess'}})
                self.assertTrue(probe(run, again, thread, 'out')['effect'])
            again.stop()

            third = run.start()
            narrowed = third.result('thread/resume', {'threadId': a, 'sandbox': 'read-only',
                                                      'approvalPolicy': 'on-request'})
            self.assertEqual(reported(narrowed), {'approvalPolicy': 'on-request',
                                                  'sandbox': {'type': 'readOnly', 'networkAccess': False}})
            self.assertFalse(probe(run, third, a, 'out')['effect'])

    def test_config_carries_the_workspace_write_options_on_start_fork_and_resume(self):
        """thread start, resume and fork take only a sandbox mode name; `config` carries the rest."""
        def options(net, slash, tmpdir):
            return {'sandbox_workspace_write': {'network_access': net, 'exclude_slash_tmp': slash,
                                                'exclude_tmpdir_env_var': tmpdir}}

        def policy(net, slash, tmpdir):
            return {'type': 'workspaceWrite', 'writableRoots': [], 'networkAccess': net,
                    'excludeTmpdirEnvVar': tmpdir, 'excludeSlashTmp': slash}
        with L.Run(SCRATCH, BINARY, slash_tmp=True) as run:
            client = run.start()
            started = client.start_thread(approvalPolicy='on-request', sandbox='workspace-write',
                                          config=options(True, True, True))
            thread = started['thread']['id']
            self.assertEqual(started['sandbox'], policy(True, True, True))
            effects = {k: probe(run, client, thread, k)['effect'] for k in ('in', 'tmpdir', 'slashtmp', 'net')}
            self.assertEqual(effects, {'in': True, 'tmpdir': False, 'slashtmp': False, 'net': True})
            fork = client.result('thread/fork', {'threadId': thread, 'sandbox': 'workspace-write',
                                                 'config': options(False, False, False)})
            self.assertEqual(fork['sandbox'], policy(False, False, False))
            client.stop()
            again = run.start()
            resumed = again.result('thread/resume', {'threadId': thread, 'sandbox': 'workspace-write',
                                                     'config': options(False, True, False)})
            self.assertEqual(resumed['sandbox'], policy(False, True, False))
            self.assertEqual({k: probe(run, again, thread, k)['effect'] for k in ('tmpdir', 'slashtmp', 'net')},
                             {'tmpdir': True, 'slashtmp': False, 'net': False})

    def test_writable_roots_from_the_home_config_are_removed_only_by_a_start_override(self):
        """A writable root in the Codex home's config.toml (the person's own settings) widens workspace write.
        `config.sandbox_workspace_write.writable_roots = []` on thread start removes it; a turn's sandboxPolicy
        with `writableRoots: []` does not."""
        with L.Run(SCRATCH, BINARY) as run:
            outside = run.root / 'outside'
            (run.root / 'home' / 'config.toml').write_text(
                '[sandbox_workspace_write]\nwritable_roots = ["%s"]\n' % outside)
            client = run.start()
            kept = client.start_thread(approvalPolicy='on-request', sandbox='workspace-write')
            self.assertEqual(kept['sandbox']['writableRoots'], [str(outside)])
            self.assertTrue(probe(run, client, kept['thread']['id'], 'out')['effect'])
            turn_only = probe(run, client, kept['thread']['id'], 'out', approvalPolicy='on-request',
                              sandboxPolicy=dict(WW, writableRoots=[]))
            self.assertTrue(turn_only['effect'])  # the configured root still applies
            removed = client.start_thread(approvalPolicy='on-request', sandbox='workspace-write',
                                          config={'sandbox_workspace_write': {'writable_roots': []}})
            self.assertEqual(removed['sandbox']['writableRoots'], [])
            self.assertFalse(probe(run, client, removed['thread']['id'], 'out')['effect'])

    def test_the_level_sent_wins_over_the_home_config_on_every_other_dimension(self):
        """The home's config.toml names the widest values: approval never, the automatic reviewer, full access,
        network on, neither temporary folder excluded; and, separately, a named permissions profile. The level
        sent at start, or on each turn alone, decides every one of them."""
        wide = ('approval_policy = "never"\napprovals_reviewer = "auto_review"\nsandbox_mode = "danger-full-access"\n'
                '[sandbox_workspace_write]\nnetwork_access = true\nexclude_slash_tmp = false\n'
                'exclude_tmpdir_env_var = false\n')
        start = {'approvalPolicy': 'on-request', 'approvalsReviewer': 'user', 'sandbox': 'workspace-write',
                 'config': {'sandbox_workspace_write': {'network_access': False, 'exclude_slash_tmp': True,
                                                        'exclude_tmpdir_env_var': True, 'writable_roots': []}}}
        turn = {'approvalPolicy': 'on-request', 'approvalsReviewer': 'user',
                'sandboxPolicy': dict(WW, networkAccess=False, excludeSlashTmp=True, excludeTmpdirEnvVar=True,
                                      writableRoots=[])}
        narrow = {'type': 'workspaceWrite', 'writableRoots': [], 'networkAccess': False,
                  'excludeTmpdirEnvVar': True, 'excludeSlashTmp': True}

        def effects(run, client, thread, **settings):
            seen = {k: probe(run, client, thread, k, **settings)['effect'] for k in ('out', 'tmpdir', 'slashtmp', 'net')}
            escalated = probe(run, client, thread, 'out', escalate=True, **settings)
            seen['asked'] = [(m, t == thread) for m, t in escalated['requests']]
            return seen
        expected = {'out': False, 'tmpdir': False, 'slashtmp': False, 'net': False,
                    'asked': [(COMMAND_APPROVAL, True)]}  # the person answers: the reviewer sent is user
        for home_config in (wide, 'default_permissions = ":danger-full-access"\n'):
            with L.Run(SCRATCH, BINARY, slash_tmp=True) as run:
                (run.root / 'home' / 'config.toml').write_text(home_config)
                client = run.start()
                unsent = client.start_thread()
                self.assertEqual(unsent['sandbox'], {'type': 'dangerFullAccess'})  # the person's own, when nothing is sent
                sent = client.start_thread(**start)
                self.assertEqual((sent['approvalPolicy'], sent['approvalsReviewer'], sent['sandbox']),
                                 ('on-request', 'user', narrow))
                self.assertIsNone(sent.get('activePermissionProfile'))
                self.assertEqual(effects(run, client, sent['thread']['id']), expected)
                self.assertEqual(effects(run, client, unsent['thread']['id'], **turn), expected)

    def test_fork(self):
        with L.Run(SCRATCH, BINARY) as run:
            client = run.start()
            full = client.start_thread(approvalPolicy='never', sandbox='danger-full-access')['thread']['id']
            probe(run, client, full, 'in')
            plain = client.start_thread()['thread']['id']
            probe(run, client, plain, 'in')
            cases = ((full, {}, True), (full, {'sandbox': 'read-only', 'approvalPolicy': 'on-request'}, False),
                     (plain, {'sandbox': 'danger-full-access', 'approvalPolicy': 'never'}, True), (plain, {}, False))
            for source, settings, writes in cases:
                fork = client.result('thread/fork', dict({'threadId': source}, **settings))
                expected = 'never' if writes else 'on-request'
                self.assertEqual(fork['approvalPolicy'], expected)
                seen = len(run.stub.requests)
                row = probe(run, client, fork['thread']['id'], 'out', forced=True)
                self.assertEqual(row['effect'], writes, settings)
                # A fork's request to the provider carries no tools at all; the call is made anyway.
                self.assertNotIn('tools', run.stub.requests[seen]['body_keys'])


class Narrowing(unittest.TestCase):
    """Case 3: a narrower setting on a later turn does not restrain a command already running."""

    def test_a_running_command_outlives_its_turn_and_a_narrower_next_turn(self):
        with L.Run(SCRATCH, BINARY) as run:
            client = run.start()
            thread = client.start_thread()['thread']['id']
            late = run.paths()['late']
            run.stub.scripts['late'] = L.command_script('call_late', run.commands()['late'], background=True)
            _, done = client.turn(thread, 'LEVEL[late] go', **FULL)
            self.assertEqual(done['turn']['status'], 'completed')
            self.assertFalse(late.exists())  # the command is still sleeping
            narrowed = probe(run, client, thread, 'in', **READ_ONLY)
            self.assertFalse(narrowed['effect'])
            deadline = time.monotonic() + 15
            while not late.exists() and time.monotonic() < deadline:
                time.sleep(0.25)
            self.assertTrue(late.exists())


def spawn_script(child_marker):
    def script(body, outputs, stub):
        if 'call_spawn' in outputs:
            return [L.message('Parent done.', 'msg_parent')]
        return [{'type': 'function_call', 'namespace': 'multi_agent_v1', 'name': 'spawn_agent', 'call_id': 'call_spawn',
                 'id': 'fc_spawn', 'arguments': json.dumps({'message': 'LEVEL[%s] work' % child_marker})}]
    return script


def spawn_child(test, run, client, thread, **settings):
    turn, done = client.turn(thread, 'LEVEL[spawn] go', **settings)
    test.assertEqual(done['turn']['status'], 'completed')
    receivers = [t for item in client.items(thread, turn, 'collabAgentToolCall')
                 for t in item.get('receiverThreadIds') or []]
    test.assertEqual(len(receivers), 1)
    child = receivers[0]
    test.assertTrue(client.wait(lambda: client.notes_for('turn/completed', child), 60))
    return child


class Child(unittest.TestCase):
    """Case 4: a delegated child takes the parent's level, and asks on its own thread."""

    def child_run(self, settings):
        with L.Run(SCRATCH, BINARY) as run:
            client = run.start()
            thread = client.start_thread()['thread']['id']
            commands = run.commands()
            run.stub.scripts['spawn'] = spawn_script('child')

            def child(body, outputs, stub):
                for call_id, key, escalate in (('call_cin', 'in', False), ('call_cout', 'out', False),
                                               ('call_cesc', 'out', True)):
                    if call_id not in outputs:
                        return [L.shell_call(body, call_id, commands[key], escalate=escalate)]
                return [L.message('Child done.', 'msg_child')]
            run.stub.scripts['child'] = child
            child_thread = spawn_child(self, run, client, thread, **settings)
            paths = run.paths()
            tools = next(r['tools'] for r in run.stub.requests if r['key'] == 'child')
            requests = [(r['method'], r['thread']) for r in client.server_requests]
            resumed = client.result('thread/resume', {'threadId': child_thread})
            return {'in': paths['in'].exists(), 'out': paths['out'].exists(), 'requests': requests,
                    'child': child_thread, 'tools': tools, 'reported': reported(resumed)}

    def test_a_child_under_edits(self):
        seen = self.child_run(EDITS_NET_OFF)
        self.assertEqual((seen['in'], seen['out']), (True, False))
        self.assertEqual(seen['requests'], [(COMMAND_APPROVAL, seen['child'])])
        self.assertEqual(seen['reported']['sandbox']['type'], 'workspaceWrite')
        self.assertFalse(any(t.endswith('spawn_agent') for t in seen['tools']))

    def test_a_child_under_full_access(self):
        seen = self.child_run(FULL)
        self.assertEqual((seen['in'], seen['out']), (True, True))
        self.assertEqual(seen['requests'], [])
        self.assertEqual(seen['reported'], {'approvalPolicy': 'never', 'sandbox': {'type': 'dangerFullAccess'}})


def tool_call_script(call_id):
    def script(body, outputs, stub):
        if call_id in outputs:
            return [L.message('Tool answered.', 'msg_' + call_id)]
        return [{'type': 'function_call', 'name': L.APP_TOOL, 'call_id': call_id, 'id': 'fc_' + call_id,
                 'arguments': '{}'}]
    return script


def offered(request):
    return any(t.split('.')[-1] == L.APP_TOOL for t in request['tools'])


class AppTool(unittest.TestCase):
    """Case 5: a call to an App-supplied tool (dynamicTools at thread start)."""

    def start_call(self, run, client, thread, key):
        held = len(client.held)
        run.stub.scripts[key] = tool_call_script('call_' + key)
        turn = client.result('turn/start', {'threadId': thread,
                                            'input': [{'type': 'text', 'text': 'LEVEL[%s] go' % key}]})['turn']['id']
        self.assertTrue(client.wait(lambda: len(client.held) > held, 30))
        return turn, client.held[-1]

    def test_held_interrupted_relaunched_resumed_and_forked(self):
        with L.Run(SCRATCH, BINARY) as run:
            client = run.start()
            client.tool_call_policy = 'hold'
            thread = client.start_thread(dynamicTools=APP_TOOL_SPEC)['thread']['id']

            turn, call = self.start_call(run, client, thread, 'held')
            self.assertTrue(offered(run.stub.requests[-1]))
            self.assertEqual(call['thread'], thread)
            # Unanswered for HOLD seconds: the turn does not end and nothing is resolved.
            self.assertFalse(client.wait(lambda: client.notes_for('turn/completed', thread, turn), HOLD))
            client.answer_tool_call(call)
            done = client.wait(lambda: client.notes_for('turn/completed', thread, turn), 30)
            self.assertEqual(done[0]['params']['turn']['status'], 'completed')
            self.assertEqual(run.stub.outputs.get('call_held'), 'Invented records answer.')

            turn, call = self.start_call(run, client, thread, 'interrupted')
            client.result('turn/interrupt', {'threadId': thread, 'turnId': turn})
            done = client.wait(lambda: client.notes_for('turn/completed', thread, turn), 20)
            self.assertEqual(done[0]['params']['turn']['status'], 'interrupted')
            # The client is never told that the call it holds has ended.
            self.assertEqual(client.notes_for('serverRequest/resolved'), [])

            turn, call = self.start_call(run, client, thread, 'relaunch')
            client.kill()
            again = run.start()
            again.tool_call_policy = 'hold'
            again.result('thread/resume', {'threadId': thread})
            time.sleep(10)
            self.assertEqual(again.held, [])  # not raised again
            turns = again.result('thread/turns/list', {'threadId': thread})['data']
            self.assertEqual(next(t['status'] for t in turns if t['id'] == turn), 'interrupted')

            again.tool_call_policy = 'answer'
            seen = len(run.stub.requests)
            run.stub.scripts['resumed'] = tool_call_script('call_resumed')
            again.turn(thread, 'LEVEL[resumed] go')
            self.assertTrue(offered(run.stub.requests[seen]))
            self.assertIn('call_resumed', run.stub.outputs)

            fork = again.result('thread/fork', {'threadId': thread})['thread']['id']
            seen = len(run.stub.requests)
            run.stub.scripts['forked'] = tool_call_script('call_forked')
            again.turn(fork, 'LEVEL[forked] go')
            self.assertFalse(offered(run.stub.requests[seen]))  # not listed to the model
            calls = [r['thread'] for r in again.server_requests if r['method'] == 'item/tool/call']
            self.assertEqual(calls[-1], fork)  # yet a call is routed to the client on the fork's thread

    def test_a_child_is_not_given_the_app_tool(self):
        with L.Run(SCRATCH, BINARY) as run:
            client = run.start()
            thread = client.start_thread(dynamicTools=APP_TOOL_SPEC)['thread']['id']
            run.stub.scripts['spawn'] = spawn_script('childtool')
            run.stub.scripts['childtool'] = tool_call_script('call_child')
            spawn_child(self, run, client, thread)
            child_request = next(r for r in run.stub.requests if r['key'] == 'childtool')
            self.assertFalse(offered(child_request))
            self.assertEqual([r for r in client.server_requests if r['method'] == 'item/tool/call'], [])
            self.assertIn('unsupported call', run.stub.outputs.get('call_child', ''))


class Question(unittest.TestCase):
    """Case 6: the supplier's question tool in an ordinary conversation."""

    def ask(self, **settings):
        with L.Run(SCRATCH, BINARY) as run:
            client = run.start()
            thread = client.start_thread()['thread']['id']

            def script(body, outputs, stub):
                if 'call_ask' in outputs:
                    return [L.message('Asked.', 'msg_asked')]
                return [{'type': 'function_call', 'name': 'request_user_input', 'call_id': 'call_ask', 'id': 'fc_ask',
                         'arguments': json.dumps({'questions': [{
                             'id': 'q1', 'header': 'Invented', 'question': 'Invented question?',
                             'options': [{'label': 'Yes', 'description': 'Invented yes'},
                                         {'label': 'No', 'description': 'Invented no'}]}]})}]
            run.stub.scripts['ask'] = script
            client.turn(thread, 'LEVEL[ask] go', **settings)
            return ('request_user_input' in run.stub.requests[0]['tools'],
                    [r['method'] for r in client.server_requests], run.stub.outputs.get('call_ask', ''))

    def test_offered_but_refused_in_default_mode(self):
        listed, requests, output = self.ask()
        self.assertTrue(listed)
        self.assertEqual(requests, [])
        self.assertIn('unavailable in Default mode', output)

    def test_reaches_the_client_in_plan_mode(self):
        listed, requests, _ = self.ask(collaborationMode={'mode': 'plan', 'settings': {'model': L.MODEL}})
        self.assertTrue(listed)
        self.assertEqual(requests, ['item/tool/requestUserInput'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
