#!/usr/bin/env python3
"""What the pinned Codex 0.167.0 does with sandbox and approval settings, asserted fact by fact.

Live: each test starts the pinned app server against the loopback stub in `level_fixture.py`, with a
fresh root that is removed afterwards. Skipped unless CHIRALITY_CODEX_BIN names the pinned binary
(its digest is checked against GENERATION.json before every start); with LEVEL_REQUIRE_LIVE=1, a
missing binary fails instead. LEVEL_SCRATCH names the folder the roots are made in; the system
temporary folder is used when it is unset. LEVEL_HOLD_SECONDS sets how long a call to an
App-supplied tool is left unanswered (default 120).

Every assertion names an outcome observed for the call it is about (`level_fixture.judge`): a command
that ran and succeeded, ran and was refused by the sandbox (with the refusal's text), was declined
at an approval request raised for it, or was rejected by Codex's policy. A call the stub could not
make is inconclusive and fails. Every assertion that no request arrived keeps, in the same test, a
request arriving on the same client where one is expected.

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
from level_fixture import DECLINED, REJECTED, RUNNING, SANDBOX_REFUSED, SUCCEEDED, expect  # noqa: E402

BINARY = os.environ.get('CHIRALITY_CODEX_BIN')
SCRATCH = os.environ.get('LEVEL_SCRATCH') or tempfile.gettempdir()
HOLD = float(os.environ.get('LEVEL_HOLD_SECONDS') or 120)

WW = {'type': 'workspaceWrite'}
SUPERVISED = {'approvalPolicy': 'untrusted', 'sandboxPolicy': {'type': 'readOnly'}}
EDITS_NET_OFF = {'approvalPolicy': 'on-request', 'sandboxPolicy': dict(WW, networkAccess=False)}
EDITS_NET_ON = {'approvalPolicy': 'on-request', 'sandboxPolicy': dict(WW, networkAccess=True)}
EDITS_NEVER = {'approvalPolicy': 'never', 'sandboxPolicy': dict(WW, networkAccess=False, excludeSlashTmp=True,
                                                               excludeTmpdirEnvVar=True)}
FULL = {'approvalPolicy': 'never', 'sandboxPolicy': {'type': 'dangerFullAccess'}}
READ_ONLY = {'approvalPolicy': 'on-request', 'sandboxPolicy': {'type': 'readOnly'}}
COMMAND_APPROVAL = 'item/commandExecution/requestApproval'
APP_TOOL_SPEC = [{'type': 'function', 'name': L.APP_TOOL, 'description': 'Invented records reader for a fixture.',
                  'inputSchema': {'type': 'object', 'properties': {}, 'additionalProperties': False}}]


def live_binary(binary, required):
    """The admitted binary. Without one, skip; but where the live tests are required (LEVEL_REQUIRE_LIVE=1, set
    by the CI step meant to run them), a missing binary fails instead, so the step cannot pass with every test
    skipped. An unpinned binary refuses either way."""
    if not binary:
        if required:
            raise L.Refused('LEVEL_REQUIRE_LIVE is set but CHIRALITY_CODEX_BIN is not')
        raise unittest.SkipTest('CHIRALITY_CODEX_BIN is not set; the live level fixtures need the pinned Codex')
    return L.admitted_binary(binary)


def setUpModule():
    live_binary(BINARY, os.environ.get('LEVEL_REQUIRE_LIVE') == '1')


def reported(reply):
    return {k: reply.get(k) for k in ('approvalPolicy', 'sandbox')}


def evidence(client, thread, call_id):
    """The protocol stages tied to one call id on one thread: Codex's command items and approval requests."""
    items = {n['params']['item'].get('id') for n in client.notes_for('item/started', thread)}
    asked = {(r['params'] or {}).get('itemId') for r in client.server_requests
             if r['method'] == COMMAND_APPROVAL and r['thread'] == thread}
    return items, asked


def probe(run, client, thread, key, escalate=False, forced=False, **settings):
    """Run one fixed command in one turn and return its judged outcome (`level_fixture.judge`), with the file's
    presence and the requests the turn raised on any thread."""
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
    items, asked = evidence(client, thread, call_id)
    outcome = L.judge(call_id, run.stub.issued, run.stub.not_offered, run.stub.outputs.get(call_id), items, asked,
                      done and done['turn']['status'])
    outcome.present = path.exists() if path is not None else None
    outcome.reached = run.stub.net_probes > nets
    outcome.requests = [(r['method'], r['thread']) for r in client.server_requests[seen:]]
    outcome.call_id, outcome.turn = call_id, turn
    return outcome


class Probing(unittest.TestCase):
    def refused(self, outcome):
        """Ran, the sandbox refused it with its own text, nothing landed or connected, and nothing was asked."""
        expect(outcome, SANDBOX_REFUSED)
        self.assertFalse(outcome.present)
        self.assertFalse(outcome.reached)
        self.assertEqual(outcome.requests, [])
        return outcome

    def succeeded(self, outcome, network=False):
        expect(outcome, SUCCEEDED)
        if network:
            self.assertTrue(outcome.reached)
        elif outcome.present is not None:
            self.assertTrue(outcome.present)
        self.assertEqual(outcome.requests, [])
        return outcome

    def declined(self, outcome, thread):
        """An approval request raised for exactly this call, on its own thread, and nothing done."""
        expect(outcome, DECLINED)
        self.assertEqual(outcome.requests, [(COMMAND_APPROVAL, thread)])
        self.assertFalse(outcome.present)
        return outcome

    def rejected(self, outcome):
        """Refused by Codex's policy before it ran: no request, nothing done."""
        expect(outcome, REJECTED)
        self.assertEqual(outcome.requests, [])
        self.assertFalse(outcome.present)
        return outcome

    def channel_live(self, run, client):
        """The same-client control for an assertion that no request arrived: under a level that asks, an
        escalation request reaches this client, tied to its call."""
        thread = client.start_thread()['thread']['id']
        self.declined(probe(run, client, thread, 'out', escalate=True, **EDITS_NET_OFF), thread)


class Presets(Probing):
    """Case 1: each preset against the fixed writes, the network probe and an escalation request. The level is
    sent on every turn, except for "nothing sent", which is what the App sends today."""

    def matrix(self, settings, run, client, thread):
        return {key: probe(run, client, thread, key, **settings)
                for key in ('in', 'out', 'tmpdir', 'slashtmp', 'git', 'net')}

    def test_edits_that_never_ask_fail_whatever_needs_more_and_raise_nothing(self):
        """The examinations' level: workspace write, network off, both temporary folders excluded, approval
        never. Whatever needs more than the sandbox gives runs and is refused by the sandbox; a command asking
        for escalation is rejected by Codex's policy; no request of any kind arises on that thread."""
        with L.Run(SCRATCH, BINARY, slash_tmp=True, git_marker=True) as run:
            client = run.start()
            thread = client.start_thread()['thread']['id']
            rows = self.matrix(EDITS_NEVER, run, client, thread)
            self.succeeded(rows['in'])
            for key in ('out', 'tmpdir', 'slashtmp', 'git', 'net'):
                self.refused(rows[key])
            self.rejected(probe(run, client, thread, 'out', escalate=True, **EDITS_NEVER))
            self.assertEqual([r for r in client.server_requests if r['thread'] == thread], [])
            self.channel_live(run, client)

    def test_nothing_sent_is_on_request_read_only_and_a_refused_write_asks_no_one(self):
        with L.Run(SCRATCH, BINARY, slash_tmp=True, git_marker=True) as run:
            client = run.start()
            reply = client.start_thread()
            thread = reply['thread']['id']
            self.assertEqual(reply['approvalPolicy'], 'on-request')
            self.assertEqual(reply['sandbox'], {'type': 'readOnly', 'networkAccess': False})
            self.assertEqual((reply.get('activePermissionProfile') or {}).get('id'), ':read-only')
            for key, outcome in self.matrix({}, run, client, thread).items():
                self.refused(outcome)  # the project's own write included
            self.declined(probe(run, client, thread, 'out', escalate=True), thread)  # the same thread asks

    def test_a_write_the_sandbox_refused_completes_no_command_item(self):
        with L.Run(SCRATCH, BINARY) as run:
            client = run.start()
            thread = client.start_thread()['thread']['id']
            refused = self.refused(probe(run, client, thread, 'out', **EDITS_NET_OFF))
            landed = self.succeeded(probe(run, client, thread, 'in', **EDITS_NET_OFF))
            self.assertFalse(refused.evidence['item'])
            self.assertTrue(landed.evidence['item'])
            self.assertEqual(client.items(thread, refused.turn, 'commandExecution'), [])

    def test_supervised_asks_before_every_command_tried_and_a_declined_one_does_not_run(self):
        with L.Run(SCRATCH, BINARY, slash_tmp=True, git_marker=True) as run:
            client = run.start()
            thread = client.start_thread()['thread']['id']
            for key, outcome in self.matrix(SUPERVISED, run, client, thread).items():
                self.declined(outcome, thread)
            self.declined(probe(run, client, thread, 'read', **SUPERVISED), thread)  # a plain read too

    def test_edits_with_network_off(self):
        with L.Run(SCRATCH, BINARY, slash_tmp=True, git_marker=True) as run:
            client = run.start()
            thread = client.start_thread()['thread']['id']
            rows = self.matrix(EDITS_NET_OFF, run, client, thread)
            for key in ('in', 'tmpdir', 'slashtmp'):
                self.succeeded(rows[key])
            for key in ('out', 'git', 'net'):
                self.refused(rows[key])
            self.declined(probe(run, client, thread, 'out', escalate=True, **EDITS_NET_OFF), thread)

    def test_edits_with_network_on(self):
        with L.Run(SCRATCH, BINARY, slash_tmp=True, git_marker=True) as run:
            client = run.start()
            thread = client.start_thread()['thread']['id']
            rows = self.matrix(EDITS_NET_ON, run, client, thread)
            for key in ('in', 'tmpdir', 'slashtmp'):
                self.succeeded(rows[key])
            self.succeeded(rows['net'], network=True)
            for key in ('out', 'git'):
                self.refused(rows[key])
            self.declined(probe(run, client, thread, 'out', escalate=True, **EDITS_NET_ON), thread)

    def test_full_access_writes_everywhere_tried_and_an_escalation_request_is_refused_by_codex(self):
        with L.Run(SCRATCH, BINARY, slash_tmp=True, git_marker=True) as run:
            client = run.start()
            thread = client.start_thread()['thread']['id']
            rows = self.matrix(FULL, run, client, thread)
            for key in ('in', 'out', 'tmpdir', 'slashtmp', 'git'):
                self.succeeded(rows[key])
            self.succeeded(rows['net'], network=True)
            self.rejected(probe(run, client, thread, 'out', escalate=True, **FULL))
            self.channel_live(run, client)

    def test_the_two_temporary_folder_exclusions(self):
        with L.Run(SCRATCH, BINARY, slash_tmp=True) as run:
            client = run.start()
            for excluded, kept, policy in (('slashtmp', 'tmpdir', dict(WW, excludeSlashTmp=True)),
                                           ('tmpdir', 'slashtmp', dict(WW, excludeTmpdirEnvVar=True))):
                thread = client.start_thread()['thread']['id']
                settings = dict(EDITS_NET_OFF, sandboxPolicy=policy)
                self.succeeded(probe(run, client, thread, 'in', **settings))
                self.succeeded(probe(run, client, thread, kept, **settings))
                self.refused(probe(run, client, thread, excluded, **settings))

    def test_an_extra_writable_root(self):
        with L.Run(SCRATCH, BINARY) as run:
            client = run.start()
            without = client.start_thread()['thread']['id']
            self.refused(probe(run, client, without, 'extra', **EDITS_NET_OFF))
            thread = client.start_thread()['thread']['id']
            settings = dict(EDITS_NET_OFF, sandboxPolicy=dict(WW, writableRoots=[str(run.root / 'outside')]))
            self.succeeded(probe(run, client, thread, 'extra', **settings))
            self.succeeded(probe(run, client, thread, 'in', **settings))

    def test_paths_with_spaces_and_shell_characters_stay_contained(self):
        """A scratch folder whose name holds spaces, single quotes, parentheses, a semicolon and an ampersand: the
        quoted commands write only their own targets, and the sandbox still refuses outside the project. A dollar
        sign, a backquote and a double quote are left out, because Codex itself mishandles them (the next two
        tests)."""
        odd = Path(tempfile.mkdtemp(prefix="level odd 'q' (p) ; & ", dir=SCRATCH))
        try:
            before = sorted(p.name for p in odd.parent.iterdir())
            with L.Run(odd, BINARY) as run:
                client = run.start()
                thread = client.start_thread()['thread']['id']
                self.succeeded(probe(run, client, thread, 'in', **EDITS_NET_OFF))
                self.refused(probe(run, client, thread, 'out', **EDITS_NET_OFF))
                self.assertEqual(sorted(p.name for p in run.root.iterdir()),
                                 sorted(['home', 'userhome', 'project', 'outside', 'tmpdir'] +
                                        [p.name for p in run.root.glob('codex-stderr-*.log')]))
                self.assertEqual(sorted(p.name for p in run.project.iterdir()), ['w-in'])
                self.assertEqual(list((run.root / 'outside').iterdir()), [])
            self.assertEqual(sorted(p.name for p in odd.parent.iterdir()), before)
            self.assertEqual(list(odd.iterdir()), [])
        finally:
            odd.rmdir()

    def test_a_double_quote_in_the_project_path_makes_every_sandboxed_command_fail_to_start(self):
        """With a double quote in the project's path, the sandbox profile Codex writes for macOS does not parse:
        a command under workspace write fails with sandbox-exec's own parse error and does not run. It fails
        closed: nothing is written. Under full access, which uses no sandbox, the same write succeeds."""
        odd = Path(tempfile.mkdtemp(prefix='level dq "x" ', dir=SCRATCH))
        try:
            with L.Run(odd, BINARY) as run:
                client = run.start()
                thread = client.start_thread()['thread']['id']
                failed = probe(run, client, thread, 'in', **EDITS_NET_OFF)
                expect(failed, L.FAILED)
                self.assertTrue(failed.text.startswith('sandbox-exec: '), failed.text)  # the profile's own parse error
                self.assertFalse(failed.present)
                self.succeeded(probe(run, client, thread, 'in', **FULL))
        finally:
            odd.rmdir()

    def test_codex_expands_its_home_path_at_thread_start_beyond_the_threads_level(self):
        """Codex validates its shell snapshot with `. "<snapshot path>"`, the path under CODEX_HOME inside double
        quotes (core/src/shell_snapshot.rs at the tag), so a command substitution in the home's folder name runs.
        Observed: at thread/start, before any turn, it ran with the project as its folder and wrote there, though
        the thread's level is read-only and a turn's write to the project is refused."""
        with L.Run(SCRATCH, BINARY, home_name='home $(touch level-mark)') as run:
            mark = run.project / 'level-mark'
            client = run.start()
            self.assertFalse(mark.exists())
            reply = client.start_thread()
            self.assertEqual(reply['sandbox'], {'type': 'readOnly', 'networkAccess': False})
            self.assertTrue(client.wait(lambda: mark.exists(), 20))  # before any turn
            self.assertEqual([n for n in client.notes if n['method'] == 'turn/started'], [])
            self.refused(probe(run, client, reply['thread']['id'], 'in'))  # the level forbids this write


class Carriers(Probing):
    """Case 2: where a setting can be sent, whether it is held to, and what the replies report."""

    def test_thread_start_turn_start_and_resume(self):
        with L.Run(SCRATCH, BINARY) as run:
            client = run.start()
            started = client.start_thread(approvalPolicy='never', sandbox='danger-full-access')
            a = started['thread']['id']
            self.assertEqual(reported(started), {'approvalPolicy': 'never', 'sandbox': {'type': 'dangerFullAccess'}})
            self.succeeded(probe(run, client, a, 'out'))

            b = client.start_thread()['thread']['id']
            self.refused(probe(run, client, b, 'out'))  # before: read-only
            self.succeeded(probe(run, client, b, 'out', **FULL))
            self.succeeded(probe(run, client, b, 'out'))  # the turn's setting holds for the next turn
            # thread/read reports no setting: these two fields are absent or null.
            self.assertEqual(reported(client.result('thread/read', {'threadId': b})),
                             {'approvalPolicy': None, 'sandbox': None})
            client.stop()

            again = run.start()
            for thread in (a, b):  # resume with none keeps the last setting, set at thread start or on a turn
                resumed = again.result('thread/resume', {'threadId': thread})
                self.assertEqual(reported(resumed), {'approvalPolicy': 'never', 'sandbox': {'type': 'dangerFullAccess'}})
                self.succeeded(probe(run, again, thread, 'out'))
            again.stop()

            third = run.start()
            narrowed = third.result('thread/resume', {'threadId': a, 'sandbox': 'read-only',
                                                      'approvalPolicy': 'on-request'})
            self.assertEqual(reported(narrowed), {'approvalPolicy': 'on-request',
                                                  'sandbox': {'type': 'readOnly', 'networkAccess': False}})
            self.refused(probe(run, third, a, 'out'))

    def test_config_carries_the_workspace_write_options_on_start_fork_and_resume(self):
        """thread start, resume and fork take only a sandbox mode name; `config` carries the rest. Each reply
        reports the whole policy, and each policy is exercised, allowed and refused effects both."""
        def options(net, slash, tmpdir):
            return {'sandbox_workspace_write': {'network_access': net, 'exclude_slash_tmp': slash,
                                                'exclude_tmpdir_env_var': tmpdir, 'writable_roots': []}}

        def policy(net, slash, tmpdir):
            return {'type': 'workspaceWrite', 'writableRoots': [], 'networkAccess': net,
                    'excludeTmpdirEnvVar': tmpdir, 'excludeSlashTmp': slash}
        with L.Run(SCRATCH, BINARY, slash_tmp=True) as run:
            client = run.start()
            started = client.start_thread(approvalPolicy='on-request', sandbox='workspace-write',
                                          config=options(True, True, True))
            thread = started['thread']['id']
            self.assertEqual(started['sandbox'], policy(True, True, True))
            self.succeeded(probe(run, client, thread, 'in'))
            self.succeeded(probe(run, client, thread, 'net'), network=True)
            self.refused(probe(run, client, thread, 'tmpdir'))
            self.refused(probe(run, client, thread, 'slashtmp'))

            fork = client.result('thread/fork', {'threadId': thread, 'sandbox': 'workspace-write',
                                                 'config': options(False, False, False)})
            forked = fork['thread']['id']
            self.assertEqual(fork['sandbox'], policy(False, False, False))
            self.succeeded(probe(run, client, forked, 'in', forced=True))
            self.succeeded(probe(run, client, forked, 'tmpdir', forced=True))
            self.succeeded(probe(run, client, forked, 'slashtmp', forced=True))
            self.refused(probe(run, client, forked, 'net', forced=True))
            self.refused(probe(run, client, forked, 'out', forced=True))
            client.stop()

            again = run.start()
            resumed = again.result('thread/resume', {'threadId': thread, 'sandbox': 'workspace-write',
                                                     'config': options(False, True, False)})
            self.assertEqual(resumed['sandbox'], policy(False, True, False))
            self.succeeded(probe(run, again, thread, 'tmpdir'))
            self.refused(probe(run, again, thread, 'slashtmp'))
            self.refused(probe(run, again, thread, 'net'))

    def test_writable_roots_from_the_home_config_are_removed_only_by_a_start_override(self):
        """A writable root in the Codex home's config.toml (the person's own settings) widens workspace write.
        `config.sandbox_workspace_write.writable_roots = []` on thread start removes it; a turn's sandboxPolicy
        with `writableRoots: []` does not."""
        with L.Run(SCRATCH, BINARY) as run:
            outside = run.root / 'outside'
            (run.root / 'home' / 'config.toml').write_text(
                '[sandbox_workspace_write]\nwritable_roots = [%s]\n' % L.toml_string(outside))
            client = run.start()
            kept = client.start_thread(approvalPolicy='on-request', sandbox='workspace-write')
            self.assertEqual(kept['sandbox']['writableRoots'], [str(outside)])
            self.succeeded(probe(run, client, kept['thread']['id'], 'out'))
            self.succeeded(probe(run, client, kept['thread']['id'], 'out', approvalPolicy='on-request',
                                 sandboxPolicy=dict(WW, writableRoots=[])))  # the configured root still applies
            removed = client.start_thread(approvalPolicy='on-request', sandbox='workspace-write',
                                          config={'sandbox_workspace_write': {'writable_roots': []}})
            self.assertEqual(removed['sandbox']['writableRoots'], [])
            self.succeeded(probe(run, client, removed['thread']['id'], 'in'))
            self.refused(probe(run, client, removed['thread']['id'], 'out'))

    def test_the_level_sent_wins_over_the_home_config_on_every_other_dimension(self):
        """The home's config.toml names the widest values (approval never, the automatic reviewer, full access,
        network on, neither temporary folder excluded), or, separately, a named full-access permissions profile.
        With nothing sent the person's own apply; the level sent at start, or on each turn alone, decides
        approval, reviewer, sandbox, network and both exclusions, observed in effect."""
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
        unsent_settings = {wide: ('never', 'auto_review', None),
                           'default_permissions = ":danger-full-access"\n': ('on-request', 'user', ':danger-full-access')}

        def held(run, client, thread, **settings):
            self.succeeded(probe(run, client, thread, 'in', **settings))
            for key in ('out', 'tmpdir', 'slashtmp', 'net'):
                self.refused(probe(run, client, thread, key, **settings))
            self.declined(probe(run, client, thread, 'out', escalate=True, **settings), thread)  # the person answers
        for home_config, (approval, reviewer, profile) in unsent_settings.items():
            with L.Run(SCRATCH, BINARY, slash_tmp=True) as run:
                (run.root / 'home' / 'config.toml').write_text(home_config)
                client = run.start()
                unsent = client.start_thread()
                self.assertEqual((unsent['approvalPolicy'], unsent['approvalsReviewer'], unsent['sandbox']),
                                 (approval, reviewer, {'type': 'dangerFullAccess'}))
                self.assertEqual((unsent.get('activePermissionProfile') or {}).get('id'), profile)
                self.succeeded(probe(run, client, unsent['thread']['id'], 'out'))  # the person's own applies
                sent = client.start_thread(**start)
                self.assertEqual((sent['approvalPolicy'], sent['approvalsReviewer'], sent['sandbox']),
                                 ('on-request', 'user', narrow))
                self.assertIsNone(sent.get('activePermissionProfile'))
                held(run, client, sent['thread']['id'])
                held(run, client, unsent['thread']['id'], **turn)

    def test_fork(self):
        """Fork with none inherits; fork with a setting applies it. Each is held to it: a write the level forbids
        and one it allows. A fork's requests to the provider carry no tools, yet a call made anyway runs."""
        with L.Run(SCRATCH, BINARY) as run:
            client = run.start()
            full = client.start_thread(approvalPolicy='never', sandbox='danger-full-access')['thread']['id']
            self.succeeded(probe(run, client, full, 'in'))
            plain = client.start_thread()['thread']['id']
            self.refused(probe(run, client, plain, 'in'))
            read_only = {'type': 'readOnly', 'networkAccess': False}
            cases = ((full, {}, 'never', {'type': 'dangerFullAccess'}),
                     (full, {'sandbox': 'read-only', 'approvalPolicy': 'on-request'}, 'on-request', read_only),
                     (plain, {'sandbox': 'danger-full-access', 'approvalPolicy': 'never'}, 'never',
                      {'type': 'dangerFullAccess'}),
                     (plain, {}, 'on-request', read_only))
            for source, settings, approval, sandbox in cases:
                fork = client.result('thread/fork', dict({'threadId': source}, **settings))
                self.assertEqual(reported(fork), {'approvalPolicy': approval, 'sandbox': sandbox})
                forked = fork['thread']['id']
                seen = len(run.stub.requests)
                if sandbox['type'] == 'dangerFullAccess':
                    self.succeeded(probe(run, client, forked, 'out', forced=True))
                else:
                    self.refused(probe(run, client, forked, 'out', forced=True))
                    self.refused(probe(run, client, forked, 'in', forced=True))
                fork_requests = run.stub.requests[seen:]
                self.assertTrue(fork_requests)
                for request in fork_requests:
                    self.assertNotIn('tools', request['body_keys'])


class Narrowing(Probing):
    """Case 3: a narrower setting on a later turn does not restrain a command already running."""

    def test_a_running_command_outlives_its_turn_and_a_narrower_next_turn(self):
        with L.Run(SCRATCH, BINARY) as run:
            client = run.start()
            thread = client.start_thread()['thread']['id']
            late = run.paths()['late']
            run.stub.scripts['late'] = L.command_script('call_late', run.commands()['late'], background=True)
            turn, done = client.turn(thread, 'LEVEL[late] go', **FULL)
            items, asked = evidence(client, thread, 'call_late')
            started = L.judge('call_late', run.stub.issued, run.stub.not_offered, run.stub.outputs.get('call_late'),
                              items, asked, done and done['turn']['status'])
            expect(started, RUNNING)  # the turn completed while the command sleeps
            self.assertFalse(late.exists())
            self.refused(probe(run, client, thread, 'out', **READ_ONLY))  # the narrower level is in force
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
    test.assertIn('call_spawn', run.stub.issued)
    receivers = [t for item in client.items(thread, turn, 'collabAgentToolCall')
                 for t in item.get('receiverThreadIds') or []]
    test.assertEqual(len(receivers), 1)
    child = receivers[0]
    child_done = client.wait(lambda: client.notes_for('turn/completed', child), 60)
    test.assertTrue(child_done)
    test.assertEqual(child_done[0]['params']['turn']['status'], 'completed')
    return child


class Child(Probing):
    """Case 4: a delegated child is held to the parent's level, and asks on its own thread."""

    def child_run(self, settings):
        with L.Run(SCRATCH, BINARY) as run:
            client = run.start()
            thread = client.start_thread()['thread']['id']
            commands = run.commands()
            calls = (('call_cin', 'in', False), ('call_cout', 'out', False), ('call_cesc', 'out2', True))
            run.stub.scripts['spawn'] = spawn_script('child')

            def child(body, outputs, stub):
                for call_id, key, escalate in calls:
                    if call_id not in outputs:
                        call = L.shell_call(body, call_id, commands[key], escalate=escalate)
                        if call is None:
                            stub.not_offered.add(call_id)
                            return [L.message('No shell tool offered.', 'msg_noshell')]
                        return [call]
                return [L.message('Child done.', 'msg_child')]
            run.stub.scripts['child'] = child
            child_thread = spawn_child(self, run, client, thread, **settings)
            outcomes = {}
            for call_id, key, _ in calls:
                items, asked = evidence(client, child_thread, call_id)
                outcomes[key] = L.judge(call_id, run.stub.issued, run.stub.not_offered,
                                        run.stub.outputs.get(call_id), items, asked, 'completed')
            paths = run.paths()
            tools = next(r['tools'] for r in run.stub.requests if r['key'] == 'child')
            requests = [(r['method'], r['thread'], (r['params'] or {}).get('itemId')) for r in client.server_requests]
            resumed = client.result('thread/resume', {'threadId': child_thread})
            return {'outcomes': outcomes, 'files': {k: paths[k].exists() for k in ('in', 'out', 'out2')},
                    'requests': requests, 'child': child_thread, 'tools': tools, 'reported': reported(resumed)}

    def test_a_child_under_edits(self):
        seen = self.child_run(EDITS_NET_OFF)
        expect(seen['outcomes']['in'], SUCCEEDED)
        expect(seen['outcomes']['out'], SANDBOX_REFUSED)
        expect(seen['outcomes']['out2'], DECLINED)
        self.assertEqual(seen['files'], {'in': True, 'out': False, 'out2': False})
        self.assertEqual(seen['requests'], [(COMMAND_APPROVAL, seen['child'], 'call_cesc')])
        self.assertEqual(seen['reported']['sandbox']['type'], 'workspaceWrite')
        self.assertFalse(any(t.endswith('spawn_agent') for t in seen['tools']))

    def test_a_child_under_full_access(self):
        seen = self.child_run(FULL)
        expect(seen['outcomes']['in'], SUCCEEDED)
        expect(seen['outcomes']['out'], SUCCEEDED)
        expect(seen['outcomes']['out2'], REJECTED)
        self.assertEqual(seen['files'], {'in': True, 'out': True, 'out2': False})
        self.assertEqual(seen['requests'], [])
        self.assertEqual(seen['reported'], {'approvalPolicy': 'never', 'sandbox': {'type': 'dangerFullAccess'}})
        self.assertFalse(any(t.endswith('spawn_agent') for t in seen['tools']))


def tool_call_script(call_id):
    def script(body, outputs, stub):
        if call_id in outputs:
            return [L.message('Tool answered.', 'msg_' + call_id)]
        return [{'type': 'function_call', 'name': L.APP_TOOL, 'call_id': call_id, 'id': 'fc_' + call_id,
                 'arguments': '{}'}]
    return script


def offered(request):
    return any(t.split('.')[-1] == L.APP_TOOL for t in request['tools'])


def tool_calls(client, call_id=None):
    return [r for r in client.server_requests
            if r['method'] == 'item/tool/call' and (call_id is None or r['params'].get('callId') == call_id)]


class AppTool(unittest.TestCase):
    """Case 5: a call to an App-supplied tool (dynamicTools at thread start)."""

    def start_call(self, run, client, thread, key):
        call_id = 'call_' + key
        run.stub.scripts[key] = tool_call_script(call_id)
        turn = client.result('turn/start', {'threadId': thread,
                                            'input': [{'type': 'text', 'text': 'LEVEL[%s] go' % key}]})['turn']['id']
        self.assertTrue(client.wait(lambda: tool_calls(client, call_id), 30))
        self.assertIn(call_id, run.stub.issued)
        call = tool_calls(client, call_id)[0]
        self.assertEqual((call['thread'], call['params'].get('turnId')), (thread, turn))
        return turn, call

    def test_held_interrupted_relaunched_resumed_and_forked(self):
        with L.Run(SCRATCH, BINARY) as run:
            client = run.start()
            client.tool_call_policy = 'hold'
            thread = client.start_thread(dynamicTools=APP_TOOL_SPEC)['thread']['id']

            turn, call = self.start_call(run, client, thread, 'held')
            self.assertTrue(offered(run.stub.requests[-1]))
            held_since = time.monotonic()
            self.assertFalse(client.wait(lambda: client.notes_for('turn/completed', thread, turn), HOLD))
            self.assertGreaterEqual(time.monotonic() - held_since, HOLD - 1)
            self.assertIsNone(client.proc.poll())  # the server is still up
            client.answer_tool_call(call)
            done = client.wait(lambda: client.notes_for('turn/completed', thread, turn), 30)
            self.assertEqual(done[0]['params']['turn']['status'], 'completed')
            self.assertEqual(run.stub.outputs.get('call_held'), 'Invented records answer.')

            turn, interrupted = self.start_call(run, client, thread, 'interrupted')
            interrupted_at = time.monotonic()
            client.result('turn/interrupt', {'threadId': thread, 'turnId': turn})
            done = client.wait(lambda: client.notes_for('turn/completed', thread, turn), 20)
            self.assertEqual(done[0]['params']['turn']['status'], 'interrupted')

            turn, outstanding = self.start_call(run, client, thread, 'relaunch')
            # At the end of this generation: the client was never told that the interrupted call ended.
            observed = time.monotonic() - interrupted_at
            self.assertEqual(client.notes_for('serverRequest/resolved'), [], 'within %.1f s' % observed)
            client.kill()

            again = run.start()
            again.tool_call_policy = 'hold'
            resumed_at = time.monotonic()
            again.result('thread/resume', {'threadId': thread})
            time.sleep(10)
            turns = again.result('thread/turns/list', {'threadId': thread})['data']
            self.assertEqual(next(t['status'] for t in turns if t['id'] == turn), 'interrupted')

            again.tool_call_policy = 'answer'
            seen = len(run.stub.requests)
            run.stub.scripts['resumed'] = tool_call_script('call_resumed')
            _, done = again.turn(thread, 'LEVEL[resumed] go')
            self.assertEqual(done['turn']['status'], 'completed')
            self.assertTrue(offered(run.stub.requests[seen]))
            self.assertEqual([c['thread'] for c in tool_calls(again, 'call_resumed')], [thread])  # a new call, raised
            self.assertEqual(run.stub.outputs.get('call_resumed'), 'Invented records answer.')  # and answered

            fork = again.result('thread/fork', {'threadId': thread})['thread']['id']
            seen = len(run.stub.requests)
            run.stub.scripts['forked'] = tool_call_script('call_forked')
            _, done = again.turn(fork, 'LEVEL[forked] go')
            self.assertEqual(done['turn']['status'], 'completed')
            self.assertTrue(run.stub.requests[seen:])
            self.assertFalse(any(offered(r) for r in run.stub.requests[seen:]))  # not listed to the model
            self.assertEqual([c['thread'] for c in tool_calls(again, 'call_forked')], [fork])  # yet routed
            self.assertEqual(run.stub.outputs.get('call_forked'), 'Invented records answer.')

            # At the end of the second generation: the outstanding call was never raised again.
            observed = time.monotonic() - resumed_at
            self.assertEqual(tool_calls(again, outstanding['params']['callId']), [], 'within %.1f s' % observed)
            self.assertEqual(tool_calls(again, interrupted['params']['callId']), [])

    def test_a_child_is_not_given_the_app_tool(self):
        with L.Run(SCRATCH, BINARY) as run:
            client = run.start()
            thread = client.start_thread(dynamicTools=APP_TOOL_SPEC)['thread']['id']
            self.assertTrue(offered_to_parent(self, run, client, thread))
            run.stub.scripts['spawn'] = spawn_script('childtool')
            run.stub.scripts['childtool'] = tool_call_script('call_child')
            spawn_child(self, run, client, thread)
            self.assertIn('call_child', run.stub.issued)
            child_request = next(r for r in run.stub.requests if r['key'] == 'childtool')
            self.assertFalse(offered(child_request))
            self.assertEqual(tool_calls(client, 'call_child'), [])
            self.assertTrue(run.stub.outputs.get('call_child', '').startswith('unsupported call'))


def offered_to_parent(test, run, client, thread):
    """The control: the parent's own request lists the tool and a call from it reaches the client."""
    run.stub.scripts['parentcall'] = tool_call_script('call_parent')
    _, done = client.turn(thread, 'LEVEL[parentcall] go')
    test.assertEqual(done['turn']['status'], 'completed')
    test.assertEqual([c['thread'] for c in tool_calls(client, 'call_parent')], [thread])
    return offered(next(r for r in run.stub.requests if r['key'] == 'parentcall'))


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
            _, done = client.turn(thread, 'LEVEL[ask] go', **settings)
            self.assertEqual(done['turn']['status'], 'completed')
            self.assertIn('call_ask', run.stub.issued)
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
