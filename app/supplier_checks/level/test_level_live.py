#!/usr/bin/env python3
"""What the pinned Codex 0.169.0 does with sandbox and approval settings, asserted fact by fact.

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
import pprint
import subprocess
import signal
import re
import stat
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
# Debug only: a folder to write the raw record of the temporary folder rows into (see `raw_record`). It changes
# no judgment and no assertion; unset, nothing is written.
RAW = os.environ.get('LEVEL_RAW_DIR')

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


def evidence(client, thread, call_id, turn=None):
    """The protocol stages tied to one call id: the commandExecution items started in that turn on that thread
    (in any of the thread's turns when `turn` is None), the status that call's item completed with, and the
    approval requests raised on that thread."""
    def ours(note):
        p = note['params']
        return p['item'].get('type') == 'commandExecution' and (turn is None or p.get('turnId') == turn)
    items = {n['params']['item'].get('id') for n in client.notes_for('item/started', thread) if ours(n)}
    completed = next((n['params']['item'] for n in client.notes_for('item/completed', thread)
                      if ours(n) and n['params']['item'].get('id') == call_id), None)
    asked = {(r['params'] or {}).get('itemId') for r in client.server_requests
             if r['method'] == COMMAND_APPROVAL and r['thread'] == thread}
    return items, asked, completed


def target_of(run, key):
    """What a refusal of this command must name: its file, the network, or nothing (a read)."""
    if key == 'net':
        return L.NETWORK
    if key in run.touch_refusals():  # `touch` prints its own refusal line, not a shell's
        return run.touch_refusals()[key]
    return run.paths().get(key)


def probe(run, client, thread, key, escalate=False, forced=False, **settings):
    """Run one fixed command in one turn and return its judged outcome (`level_fixture.judge`), with the file's
    presence and the requests the turn raised on any thread."""
    path = run.paths().get(key)
    if path is not None and path.exists():
        path.unlink()
    nets, seen = run.stub.net_probes, len(client.server_requests)
    call_id = 'call_%s_%d' % (key, len(run.stub.requests))
    command = run.commands()[key]
    if forced:  # call exec_command whether or not the request offers it, keeping any escalation
        run.stub.scripts[call_id] = L.forced_exec_script(call_id, command, escalate=escalate)
    else:
        run.stub.scripts[call_id] = L.command_script(call_id, command, escalate=escalate)
    turn, done = client.turn(thread, 'LEVEL[%s] go' % call_id, **settings)
    items, asked, completed = evidence(client, thread, call_id, turn)
    outcome = L.judge(call_id, run.stub.issued, run.stub.not_offered, run.stub.outputs.get(call_id), items, asked,
                      done and done['turn']['status'], target=target_of(run, key),
                      item_status=completed and completed.get('status'), item_exit=completed and completed.get('exitCode'))
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
        """An approval request raised for exactly this call, on its own thread; the decline's own output; a completed
        item ended declined with no exit code; and no effect on its file or the network. (This is what is
        observed; it does not show that the command never ran.)"""
        expect(outcome, DECLINED)
        self.assertEqual(outcome.requests, [(COMMAND_APPROVAL, thread)])
        self.assertEqual(outcome.evidence['item_status'], 'declined')  # the completed declined item is required
        self.assertIsNone(outcome.evidence['item_exit'])  # and it carries no exit code
        self.assertIsNone(outcome.exit)
        self.assertFalse(outcome.present)
        self.assertFalse(outcome.reached)
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

    def test_supervised_asks_before_every_command_tried_and_a_declined_one_shows_no_effect(self):
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

    def test_no_edits_level_writes_in_private_var_tmp(self):
        """The App's three edits levels, each with both temporary folders excluded as the App sends them: a write
        in the run's own folder under /private/var/tmp runs and is refused by the sandbox. A write that succeeded
        there would be a writable folder the App did not name."""
        with L.Run(SCRATCH, BINARY, var_tmp=True) as run:
            client = run.start()
            both = dict(WW, excludeSlashTmp=True, excludeTmpdirEnvVar=True)
            for name, settings in (('edits', dict(EDITS_NET_OFF, sandboxPolicy=dict(both, networkAccess=False))),
                                   ('edits-network', dict(EDITS_NET_ON, sandboxPolicy=dict(both, networkAccess=True))),
                                   ('edits-no-asking', EDITS_NEVER)):
                thread = client.start_thread()['thread']['id']
                outcome = probe(run, client, thread, 'vartmp', **settings)
                if outcome.kind == SUCCEEDED:
                    self.fail('%s wrote in /private/var/tmp: a writable folder the App did not name' % name)
                self.refused(outcome)
                self.succeeded(probe(run, client, thread, 'in', **settings))  # the same thread writes its project
            control = client.start_thread()['thread']['id']
            self.succeeded(probe(run, client, control, 'vartmp', **FULL))

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
        quoted commands write only their own targets, and the sandbox still refuses outside the project. A double
        quote is left out here (the next test)."""
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

    def test_a_double_quote_in_the_project_path_prevents_the_workspace_write_command_from_starting(self):
        """With a double quote in the project's path, the sandbox profile Codex writes for macOS does not parse:
        a command under workspace write fails with sandbox-exec's own parse error and does not run. It fails
        closed: nothing is written. Under full access, which uses no sandbox, the same write succeeds."""
        with L.Run(SCRATCH, BINARY, project_name='project dq "x"') as run:
            client = run.start()
            thread = client.start_thread()['thread']['id']
            failed = probe(run, client, thread, 'in', **EDITS_NET_OFF)
            expect(failed, L.FAILED)
            self.assertTrue(failed.text.startswith('sandbox-exec: unbound variable: '), failed.text)
            self.assertFalse(failed.present)
            self.succeeded(probe(run, client, thread, 'in', **FULL))
        with L.Run(SCRATCH, BINARY) as run:  # the control: the same command and level in a plain folder
            client = run.start()
            thread = client.start_thread()['thread']['id']
            self.succeeded(probe(run, client, thread, 'in', **EDITS_NET_OFF))


def raw_record(name, record):
    """With LEVEL_RAW_DIR set, write one record as a plain JSON file there; otherwise do nothing. A record holds
    what was observed, as observed; nothing is summarised."""
    if not RAW:
        return
    folder = Path(RAW)
    folder.mkdir(parents=True, exist_ok=True)
    (folder / (name + '.json')).write_text(json.dumps(record, indent=2, sort_keys=True) + '\n')


def raw_entries(run):
    """For the raw record only (the assertions use `Run.entries`): each folder on the temporary folder's path, as
    lstat sees it, or absent; whether it is a link; and the names each of the run's root, the Working Files
    folder and codex-tmp holds, or why they could not be listed."""
    out = {}
    for folder in (run.root, run.data, run.working, run.codex_tmp, run.tmpdir):
        try:
            st = os.lstat(folder)
            out[str(folder)] = {'device': st.st_dev, 'inode': st.st_ino, 'type': oct(stat.S_IFMT(st.st_mode)),
                                'link': stat.S_ISLNK(st.st_mode)}
        except OSError as error:
            out[str(folder)] = {'absent': str(error)}
    names = {}
    for folder in (run.root, run.working, run.codex_tmp):
        try:
            names[str(folder)] = sorted(os.listdir(folder))
        except OSError as error:
            names[str(folder)] = 'not listed: %s' % error
    return {'identity': out, 'names': names}


def raw_ident(reading):
    ident, names = reading
    return {'identity (device, inode, type)': ident, 'names': names}


class TemporaryFolderEntries(Probing):
    """The App's layout (`Run(working_files=True)`): a fresh home with new, empty settings inside an invented data
    folder, and TMPDIR a folder made in "codex-tmp" inside the "<data folder> Working Files" folder beside it.
    Nothing is sent by the client. Each scripted command tries to change the directory entry that names the
    temporary folder, or an ancestor's entry: rename it, remove it and make it again, replace it with a link,
    and make a new link beside it."""

    def entry_probe(self, run, client, thread, key, **settings):
        command, lines = run.entry_operations()[key]
        call_id = 'call_%s_%d' % (key, len(run.stub.requests))
        run.stub.scripts[call_id] = L.command_script(call_id, command)
        turn, done = client.turn(thread, 'LEVEL[%s] go' % call_id, **settings)
        items, asked, completed = evidence(client, thread, call_id, turn)
        outcome = L.judge(call_id, run.stub.issued, run.stub.not_offered, run.stub.outputs.get(call_id), items,
                          asked, done and done['turn']['status'], target=lines,
                          item_status=completed and completed.get('status'),
                          item_exit=completed and completed.get('exitCode'))
        outcome.requests = [(r['method'], r['thread']) for r in client.server_requests if r['thread'] == thread]
        outcome.command, outcome.output = command, run.stub.outputs.get(call_id)
        return outcome

    def raw(self, run, level, key, outcome, before, after):
        raw_record('%s--%s' % (level, key), {
            'level': level, 'operation': key, 'command': outcome.command,
            'output returned by Codex': outcome.output,
            'outcome judged': {'kind': outcome.kind, 'exit': outcome.exit, 'text': outcome.text,
                               'evidence': outcome.evidence},
            'requests seen on the thread': [{'method': m, 'thread': t} for m, t in outcome.requests],
            'entries before': before, 'entries after': after})

    def raw_start(self, run, level, reply):
        raw_record('%s--start' % level, {
            'level': level, 'binary': run.binary, 'binary sha256 as checked': L.sha256_file(L.admitted_binary(run.binary)),
            'pinned sha256 (supplier manifest)': L.pinned_sha256(),
            'reply approvalPolicy': reply.get('approvalPolicy'), 'reply sandbox': reply.get('sandbox'),
            'reply activePermissionProfile': reply.get('activePermissionProfile'),
            'environment given to Codex': run.environment()})

    def test_with_nothing_sent_no_entry_on_the_temporary_folders_path_changes(self):
        with L.Run(SCRATCH, BINARY, working_files=True) as run:
            client = run.start()
            reply = client.start_thread()
            thread = reply['thread']['id']
            self.assertEqual((reply['approvalPolicy'], reply['sandbox']),
                             ('on-request', {'type': 'readOnly', 'networkAccess': False}))
            self.raw_start(run, 'nothing-sent', reply)
            before = run.entries()
            for key in run.entry_operations():
                one_before = raw_entries(run)
                outcome = self.entry_probe(run, client, thread, key)
                self.raw(run, 'nothing-sent', key, outcome, one_before, raw_entries(run))
                expect(outcome, SANDBOX_REFUSED)
                self.assertEqual(outcome.requests, [], key)
            self.assertEqual(run.entries(), before)  # every entry the same folder, by device and inode
            one_before = raw_entries(run)
            inside = probe(run, client, thread, 'tmpdir')  # a write inside the temporary folder itself
            inside.command, inside.output = run.commands()['tmpdir'], run.stub.outputs.get(inside.call_id)
            self.raw(run, 'nothing-sent', 'write-inside-tmpdir', inside, one_before, raw_entries(run))
            self.refused(inside)
            raw_record('nothing-sent--entries-compared', {
                'Run.entries() before the operations': raw_ident(before),
                'Run.entries() after the operations and the write inside': raw_ident(run.entries())})
            self.assertEqual(run.entries(), before)
            self.declined(probe(run, client, thread, 'out', escalate=True), thread)  # the same thread asks

    def test_at_full_access_the_same_operations_change_the_entries(self):
        """The control: each operation succeeds at full access, so each refusal above is the sandbox's. Removing
        the non-empty codex-tmp folder fails here for its contents, with its own words, where the sandbox refused
        it first. After each, the layout is put back by the fixture, outside Codex."""
        with L.Run(SCRATCH, BINARY, working_files=True) as run:
            client = run.start()
            reply = client.start_thread()
            thread = reply['thread']['id']
            self.raw_start(run, 'full-access-on-each-turn', reply)  # full access is sent on each turn; no reply echoes it
            t, p, w = run.tmpdir, run.codex_tmp, run.working
            aside = lambda path, suffix: path.with_name(path.name + suffix)  # noqa: E731

            def put_back(link, folder):
                os.unlink(link)
                os.rename(folder, link)

            checks = {
                'entry-t-rename': (lambda: aside(t, '.moved').is_dir() and not os.path.lexists(t),
                                   lambda: os.rename(aside(t, '.moved'), t)),
                'entry-t-remake': (lambda: t.is_dir() and os.lstat(t).st_ino != remade_from[0], lambda: None),
                'entry-t-link': (lambda: t.is_symlink() and aside(t, '.aside').is_dir(),
                                 lambda: put_back(t, aside(t, '.aside'))),
                'entry-p-new-link': (lambda: (p / 'x-link').is_symlink(), lambda: os.unlink(p / 'x-link')),
                'entry-p-rename': (lambda: aside(p, '.moved').is_dir() and not os.path.lexists(p),
                                   lambda: os.rename(aside(p, '.moved'), p)),
                'entry-p-link': (lambda: p.is_symlink() and aside(p, '.aside').is_dir(),
                                 lambda: put_back(p, aside(p, '.aside'))),
                'entry-w-rename': (lambda: aside(w, '.moved').is_dir() and not os.path.lexists(w),
                                   lambda: os.rename(aside(w, '.moved'), w)),
                'entry-w-new-link': (lambda: (w / 'x-link').is_symlink(), lambda: os.unlink(w / 'x-link')),
            }
            for key in run.entry_operations():
                remade_from = [os.lstat(t).st_ino]
                one_before = raw_entries(run)
                outcome = self.entry_probe(run, client, thread, key, **FULL)
                self.raw(run, 'full-access-on-each-turn', key, outcome, one_before, raw_entries(run))
                if key == 'entry-p-remove':
                    expect(outcome, L.FAILED)
                    self.assertEqual(outcome.text, 'rmdir: %s: Directory not empty' % p)
                    continue
                expect(outcome, SUCCEEDED)
                changed, restore = checks[key]
                self.assertTrue(changed(), key)
                restore()
            one_before = raw_entries(run)
            inside = probe(run, client, thread, 'tmpdir', **FULL)
            inside.command, inside.output = run.commands()['tmpdir'], run.stub.outputs.get(inside.call_id)
            self.raw(run, 'full-access-on-each-turn', 'write-inside-tmpdir', inside, one_before, raw_entries(run))
            self.succeeded(inside)


LEVELS_TABLE = L.APP / 'src-tauri' / 'src' / 'codex_levels.json'


def level_settings(row):
    """What the App sends for one row of its table: on thread/start, the mode name and the workspace options
    through `config`; on each turn, the structured policy. Built from the table alone."""
    common = {'approvalPolicy': row['approvalPolicy'], 'approvalsReviewer': 'user'}
    start = dict(common, sandbox=row['sandbox'])
    if row['workspaceWrite'] is not None:
        start['config'] = {'sandbox_workspace_write': row['workspaceWrite']}
    return start, dict(common, sandboxPolicy=row['sandboxPolicy'])


class Table(Probing):
    """The App's own table (`codex_levels.json`), row by row: each row's values are sent as the App sends them,
    Codex's reply reports them, and the effects each row's dimensions state are observed."""

    def test_each_row_of_the_apps_table_does_what_its_dimensions_say(self):
        table = json.loads(LEVELS_TABLE.read_text())
        self.assertEqual(table['pin'], L.PIN)
        self.assertEqual([r['id'] for r in table['levels']],
                         ['supervised', 'edits', 'edits-network', 'edits-no-asking', 'full'])
        for row in table['levels']:
            with self.subTest(level=row['id']), L.Run(SCRATCH, BINARY, slash_tmp=True, git_marker=True) as run:
                start, turn = level_settings(row)
                client = run.start()
                reply = client.start_thread(**start)
                thread = reply['thread']['id']
                self.assertEqual(reply['approvalPolicy'], row['approvalPolicy'])
                self.assertEqual(reply['approvalsReviewer'], 'user')
                for key, value in row['sandboxPolicy'].items():
                    self.assertEqual(reply['sandbox'].get(key), value, key)
                dims = row['dimensions']
                if dims['asks'] == 'before-a-command-not-known-safe':
                    # Every command tried is put to the person first; the client declines, so the writes'
                    # own effects are not observed here (the read-only sandbox's are, in the "nothing sent" row).
                    for key in ('in', 'read'):
                        self.declined(probe(run, client, thread, key, **turn), thread)
                    self.assertEqual((dims['writes'], dims['network'], reply['sandbox']['type']),
                                     ('nowhere', 'off', 'readOnly'))
                    continue
                if dims['writes'] == 'project':
                    self.succeeded(probe(run, client, thread, 'in', **turn))
                    for key in ('out', 'git', 'tmpdir', 'slashtmp'):
                        self.refused(probe(run, client, thread, key, **turn))
                elif dims['writes'] == 'everywhere':
                    for key in ('in', 'out', 'git', 'tmpdir', 'slashtmp'):
                        self.succeeded(probe(run, client, thread, key, **turn))
                else:
                    self.fail('a writes value this test does not know: %r' % dims['writes'])
                net = probe(run, client, thread, 'net', **turn)
                if dims['network'] == 'on':
                    self.succeeded(net, network=True)
                else:
                    self.refused(net)
                escalation = probe(run, client, thread, 'out', escalate=True, **turn)
                if dims['asks'] == 'when-beyond-the-sandbox':
                    self.declined(escalation, thread)
                elif dims['asks'] == 'never':
                    self.rejected(escalation)
                    self.channel_live(run, client)
                else:
                    self.fail('an asks value this test does not know: %r' % dims['asks'])


class Carriers(Probing):
    """Case 2: where a setting can be sent, whether it is held to, and what the replies report."""

    def test_thread_start_turn_start_and_resume(self):
        with L.Run(SCRATCH, BINARY) as run:
            client = run.start()
            started = client.start_thread(approvalPolicy='never', sandbox='danger-full-access')
            a = started['thread']['id']
            self.assertEqual(reported(started), {'approvalPolicy': 'never', 'sandbox': {'type': 'dangerFullAccess'}})
            self.succeeded(probe(run, client, a, 'out'))
            self.rejected(probe(run, client, a, 'out2', escalate=True))  # approval never, in effect

            b = client.start_thread()['thread']['id']
            self.refused(probe(run, client, b, 'out'))  # before: read-only
            self.succeeded(probe(run, client, b, 'out', **FULL))
            self.succeeded(probe(run, client, b, 'out'))  # the turn's setting holds for the next turn
            self.rejected(probe(run, client, b, 'out2', escalate=True))  # its approval too
            # thread/read reports no setting: these two fields are absent or null.
            self.assertEqual(reported(client.result('thread/read', {'threadId': b})),
                             {'approvalPolicy': None, 'sandbox': None})
            client.stop()

            again = run.start()
            for thread in (a, b):  # resume with none keeps the last setting, set at thread start or on a turn
                resumed = again.result('thread/resume', {'threadId': thread})
                self.assertEqual(reported(resumed), {'approvalPolicy': 'never', 'sandbox': {'type': 'dangerFullAccess'}})
                self.succeeded(probe(run, again, thread, 'out'))
                self.rejected(probe(run, again, thread, 'out2', escalate=True))
            again.stop()

            third = run.start()
            narrowed = third.result('thread/resume', {'threadId': a, 'sandbox': 'read-only',
                                                      'approvalPolicy': 'on-request'})
            self.assertEqual(reported(narrowed), {'approvalPolicy': 'on-request',
                                                  'sandbox': {'type': 'readOnly', 'networkAccess': False}})
            self.refused(probe(run, third, a, 'out'))
            self.declined(probe(run, third, a, 'out2', escalate=True), a)  # approval on-request, in effect

    def test_config_carries_the_workspace_write_options_on_start_fork_and_resume(self):
        """thread start, resume and fork take only a sandbox mode name; `config` carries the rest. Each reply
        reports the whole policy, and each policy is exercised, allowed and refused effects both."""
        with L.Run(SCRATCH, BINARY, slash_tmp=True) as run:
            outside = [str(run.root / 'outside')]

            def options(net, slash, tmpdir, roots=()):
                return {'sandbox_workspace_write': {'network_access': net, 'exclude_slash_tmp': slash,
                                                    'exclude_tmpdir_env_var': tmpdir, 'writable_roots': list(roots)}}

            def policy(net, slash, tmpdir, roots=()):
                return {'type': 'workspaceWrite', 'writableRoots': list(roots), 'networkAccess': net,
                        'excludeTmpdirEnvVar': tmpdir, 'excludeSlashTmp': slash}
            client = run.start()
            started = client.start_thread(approvalPolicy='on-request', sandbox='workspace-write',
                                          config=options(True, True, True, outside))
            thread = started['thread']['id']
            self.assertEqual(started['sandbox'], policy(True, True, True, outside))
            self.succeeded(probe(run, client, thread, 'in'))
            self.succeeded(probe(run, client, thread, 'out'))  # the root given at start
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
            self.refused(probe(run, client, forked, 'out', forced=True))  # the start's root removed on fork
            client.stop()

            again = run.start()
            resumed = again.result('thread/resume', {'threadId': thread, 'sandbox': 'workspace-write',
                                                     'config': options(False, True, False, outside)})
            self.assertEqual(resumed['sandbox'], policy(False, True, False, outside))
            self.succeeded(probe(run, again, thread, 'out'))  # the root given again on resume
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
                escalated = probe(run, client, forked, 'out2', escalate=True, forced=True)
                if approval == 'never':  # the fork's approval, in effect
                    self.rejected(escalated)
                else:
                    self.declined(escalated, forked)
                if sandbox['type'] == 'dangerFullAccess':
                    self.succeeded(probe(run, client, forked, 'out', forced=True))
                    self.succeeded(probe(run, client, forked, 'net', forced=True), network=True)
                else:
                    self.refused(probe(run, client, forked, 'out', forced=True))
                    self.refused(probe(run, client, forked, 'in', forced=True))
                    self.succeeded(probe(run, client, forked, 'read', forced=True))  # what read-only allows
                fork_requests = run.stub.requests[seen:]
                self.assertTrue(fork_requests)
                for request in fork_requests:
                    self.assertNotIn('tools', request['body_keys'])


    def test_a_forks_first_turn_is_governed_by_the_level_sent_on_that_turn(self):
        """The App sends the whole level on a fork's first turn, as on every turn. That turn's setting is what the
        fork's execution rests on, whatever the fork call carried or inherited: a fork of a full-access thread
        whose first turn sends read-only refuses the project write and declines an escalation; a fork of a
        read-only thread whose first turn sends edits writes in the project and is refused outside it."""
        with L.Run(SCRATCH, BINARY) as run:
            client = run.start()
            full = client.start_thread(approvalPolicy='never', sandbox='danger-full-access')['thread']['id']
            self.succeeded(probe(run, client, full, 'out'))
            narrowed = client.result('thread/fork', {'threadId': full})['thread']['id']  # inherits full access
            self.refused(probe(run, client, narrowed, 'in', forced=True, **READ_ONLY))
            self.declined(probe(run, client, narrowed, 'out2', escalate=True, forced=True, **READ_ONLY), narrowed)
            plain = client.start_thread()['thread']['id']
            self.refused(probe(run, client, plain, 'in'))
            widened = client.result('thread/fork', {'threadId': plain})['thread']['id']  # inherits read-only
            self.succeeded(probe(run, client, widened, 'in', forced=True, **EDITS_NET_OFF))
            self.refused(probe(run, client, widened, 'out', forced=True, **EDITS_NET_OFF))


class Narrowing(Probing):
    """Case 3: a narrower setting on a later turn does not restrain a command already running."""

    def test_a_running_command_outlives_its_turn_and_a_narrower_next_turn(self):
        with L.Run(SCRATCH, BINARY) as run:
            client = run.start()
            thread = client.start_thread()['thread']['id']
            late = run.paths()['late']
            run.stub.scripts['late'] = L.command_script('call_late', run.commands()['late'], background=True)
            turn, done = client.turn(thread, 'LEVEL[late] go', **FULL)
            items, asked, completed = evidence(client, thread, 'call_late', turn)
            started = L.judge('call_late', run.stub.issued, run.stub.not_offered, run.stub.outputs.get('call_late'),
                              items, asked, done and done['turn']['status'],
                              item_status=completed and completed.get('status'))
            expect(started, RUNNING)  # the turn completed while the command sleeps
            self.assertFalse(late.exists())
            self.refused(probe(run, client, thread, 'in', **READ_ONLY))  # read-only is in force: workspace write would allow this
            deadline = time.monotonic() + 15
            while not late.exists() and time.monotonic() < deadline:
                time.sleep(0.25)
            self.assertTrue(late.exists())


def started_at(pid):
    """The start time of the running process `pid`, observed alone; a failed observation fails the row."""
    state, started = L.observe_process(pid)
    if state != 'present':
        raise AssertionError('process %d is not running' % pid)
    return started


still_running = L.still_running
end_known = L.end_known


class RunningProcess(unittest.TestCase):
    """A process started at full access with a terminal (`tty`) and still running, used on a later, narrower turn, and what ends it. The held
    command prints its own process number and then becomes `cat > <outside>/w-held`, which writes only what it is
    given; the test checks that one process by its number and start time, and searches no other process."""

    def hold(self, run, client, thread):
        target = run.root / 'outside' / 'w-held'
        command = 'echo PID $$; exec cat > %s' % target
        run.stub.allowed_commands = set(run.stub.allowed_commands) | {command, 'sleep 20'}
        session = {}

        def hold_script(body, outputs, stub):
            if 'call_hold' in outputs:
                return [L.message('Done.', 'msg_hold')]
            return [{'type': 'function_call', 'call_id': 'call_hold', 'id': 'fc_call_hold', 'name': 'exec_command',
                     'arguments': json.dumps({'cmd': command, 'tty': True, 'yield_time_ms': 250})}]
        run.stub.scripts['hold'] = hold_script
        turn, done = client.turn(thread, 'LEVEL[hold] go', **FULL)
        self.assertEqual(done['turn']['status'], 'completed')
        output = run.stub.outputs.get('call_hold') or ''
        found = re.search(r'session ID (\d+)', output)
        self.assertTrue(found, output)
        session['id'] = int(found.group(1))
        pid = re.search(r'PID (\d+)', output)
        self.assertTrue(pid, output)
        held = {'cat': (int(pid.group(1)), started_at(int(pid.group(1))))}
        self.assertIsNotNone(held['cat'][1], 'the held command is running')
        self.addCleanup(end_known, held)
        return target, session, held

    def send(self, run, client, thread, session, key, text, **settings):
        call_id = 'call_' + key

        def script(body, outputs, stub):
            if call_id in outputs:
                return [L.message('Done.', 'msg_' + key)]
            return [{'type': 'function_call', 'call_id': call_id, 'id': 'fc_' + call_id, 'name': 'write_stdin',
                     'arguments': json.dumps({'session_id': session['id'], 'chars': text + '\n', 'yield_time_ms': 500})}]
        run.stub.scripts[key] = script
        client.turn(thread, 'LEVEL[%s] go' % key, **settings)
        time.sleep(1)
        return run.stub.outputs.get(call_id) or ''

    def written(self, target):
        return target.read_text() if target.exists() else None

    def use_at(self, row, decision):
        """Hold a process at full access, then try to use it on a turn at `row`, answering any request with
        `decision`. Returns (requests raised, the call's output, what reached the process)."""
        saved = dict(L.DECLINE)
        L.DECLINE['item/commandExecution/requestApproval'] = {'decision': decision}
        try:
            with L.Run(SCRATCH, BINARY) as run:
                client = run.start()
                thread = client.start_thread()['thread']['id']
                target, session, _ = self.hold(run, client, thread)
                output = self.send(run, client, thread, session, 'use', 'used on a narrower turn',
                                   **level_settings(row)[1])
                asked = [r for r in client.server_requests if r['method'] == 'item/commandExecution/requestApproval']
                return asked, output, self.written(target)
        finally:
            L.DECLINE.clear()
            L.DECLINE.update(saved)

    def test_each_narrower_level_of_the_apps_table_asks_or_refuses_before_it_uses_a_process_started_at_full_access(self):
        table = json.loads(LEVELS_TABLE.read_text())
        for row in table['levels']:
            if row['id'] == 'full':
                continue
            with self.subTest(level=row['id']):
                asked, output, written = self.use_at(row, 'decline')
                self.assertEqual(written, '', row['id'])  # nothing reached the process
                if row['approvalPolicy'] == 'never':
                    self.assertEqual(asked, [])  # refused without a request to the person
                    self.assertIn('AskForApproval is set to Never', output)
                else:
                    self.assertEqual(len(asked), 1)  # put to the person first; declined here
                    self.assertIn('runs without a filesystem sandbox', asked[0]['params'].get('reason') or '')
        supervised = next(r for r in table['levels'] if r['id'] == 'supervised')
        asked, output, written = self.use_at(supervised, 'accept')  # the control: accepted, the line is written
        self.assertEqual(len(asked), 1)
        self.assertIn('runs without a filesystem sandbox', asked[0]['params'].get('reason') or '')
        self.assertEqual(written, 'used on a narrower turn\n')

    def test_an_interrupt_leaves_running_processes_and_cleaning_ends_them(self):
        with L.Run(SCRATCH, BINARY) as run:
            client = run.start()
            thread = client.start_thread()['thread']['id']
            target, session, held = self.hold(run, client, thread)
            run.stub.scripts['slow'] = L.command_script('call_slow', 'sleep 20')
            turn = client.result('turn/start', dict({'threadId': thread, 'input': [{'type': 'text', 'text': 'LEVEL[slow] go'}]},
                                                    **FULL))['turn']['id']
            time.sleep(3)
            client.result('turn/interrupt', {'threadId': thread, 'turnId': turn})
            completed = client.wait(lambda: client.notes_for('turn/completed', thread, turn), 20)
            self.assertTrue(completed)
            self.assertEqual(completed[0]['params']['turn']['status'], 'interrupted')  # the interrupt took effect
            listed = {t['command'] for t in client.result('thread/backgroundTerminals/list', {'threadId': thread})['data']}
            self.assertIn('sleep 20', listed)  # the interrupted turn's own command is still running
            self.send(run, client, thread, session, 'after_interrupt', 'after the interrupt', **FULL)
            self.assertEqual(self.written(target), 'after the interrupt\n')
            pid, at = held['cat']
            self.assertTrue(still_running(pid, at))  # the held command is running before cleaning
            client.result('thread/backgroundTerminals/clean', {'threadId': thread})
            time.sleep(2)
            self.assertFalse(still_running(pid, at))  # cleaning ended that very process
            output = self.send(run, client, thread, session, 'after_clean', 'after cleaning', **FULL)
            self.assertIn('Unknown process id', output)
            self.assertEqual(self.written(target), 'after the interrupt\n')


class QuitEnds(unittest.TestCase):
    """What ends background commands when Codex ends. Two commands are left running at full access: one with a
    terminal and one without. Each starts a `sleep` in the background, prints that child's process number and its
    own, and then becomes its last program, so the numbers printed are the processes that run:
    `sleep 7771 & echo PIDS $! $$; exec cat > <outside>/w-held` (terminal) and
    `sleep 7772 & echo PIDS $! $$; exec sleep 7773` (none). The test checks those four processes by number and start
    time, searches no other process, and ends any survivor itself."""

    def start_two(self, run):
        target = run.root / 'outside' / 'w-held'
        commands = {'t': ('sleep 7771 & echo PIDS $! $$; exec cat > %s' % target, True, ('7771', 'cat')),
                    'p': ('sleep 7772 & echo PIDS $! $$; exec sleep 7773', False, ('7772', '7773'))}
        run.stub.allowed_commands = set(run.stub.allowed_commands) | {c for c, _, _ in commands.values()}
        for key, (command, tty, _) in commands.items():
            def script(body, outputs, stub, key=key, command=command, tty=tty):
                if 'call_' + key in outputs:
                    return [L.message('Done.', 'msg_' + key)]
                args = dict({'cmd': command, 'yield_time_ms': 250}, **({'tty': True} if tty else {}))
                return [{'type': 'function_call', 'call_id': 'call_' + key, 'id': 'fc_call_' + key,
                         'name': 'exec_command', 'arguments': json.dumps(args)}]
            run.stub.scripts[key] = script
        client = run.start()
        thread = client.start_thread()['thread']['id']
        self.thread = thread
        known = {}
        # Whatever happens next, every process these commands printed is ended when the test ends.
        self.addCleanup(end_known, known)
        for key, (_, _, names) in commands.items():
            client.turn(thread, 'LEVEL[%s] go' % key, **FULL)
            printed = re.search(r'PIDS (\d+) (\d+)', run.stub.outputs.get('call_' + key) or '')
            self.assertTrue(printed, run.stub.outputs.get('call_' + key))
            for name, pid in zip(names, (int(printed.group(1)), int(printed.group(2)))):
                known[name] = (pid, started_at(pid))
        before = self.alive(known)
        self.assertTrue(all(before.values()), before)
        for pid, _ in known.values():
            self.assertNotEqual(os.getpgid(pid), client.pgid, 'each runs in a process group of its own')
        return client, known, before

    def alive(self, known):
        return {name: still_running(pid, at) for name, (pid, at) in known.items()}

    def test_closing_codexs_input_ends_background_commands_and_what_they_started(self):
        with L.Run(SCRATCH, BINARY) as run:
            client, known, before = self.start_two(run)
            client.proc.stdin.close()  # as the App's stop does first
            deadline = time.monotonic() + 3  # the App waits up to 3 s for the server's group to empty
            client.proc.wait(3)  # reaped, as the App reaps its child, so the server itself is no longer counted
            while L.group_members(client.pgid) and time.monotonic() < deadline:
                time.sleep(0.05)
            self.assertEqual(L.group_members(client.pgid), 0, "the server's group emptied within 3 s")
            time.sleep(1)
            self.assertEqual(self.alive(known), {'7771': False, '7772': False, '7773': False, 'cat': False})

    def test_with_codex_answering_cleaning_ends_a_command_without_a_terminal_and_what_it_started(self):
        with L.Run(SCRATCH, BINARY) as run:
            client, known, before = self.start_two(run)
            client.result('thread/backgroundTerminals/clean', {'threadId': self.thread})
            time.sleep(2)
            self.assertIsNone(client.proc.poll())  # Codex is still running
            self.assertEqual(self.alive(known), {'7771': False, '7772': False, '7773': False, 'cat': False})

    def test_when_codex_is_ended_at_once_a_background_command_without_a_terminal_outlives_it(self):
        with L.Run(SCRATCH, BINARY) as run:
            client, known, before = self.start_two(run)
            client.kill()  # the server's whole process group, at once, as a crash or a forced end
            time.sleep(2)
            after = self.alive(known)
            self.assertEqual((after['7771'], after['cat']), (False, False))  # the terminal's commands ended
            self.assertEqual((after['7772'], after['7773']), (True, True))  # these outlived it (ended at cleanup)


class TrustWrite(unittest.TestCase):
    """At full access, with the home's own new, empty settings (the App's layout): what `thread/start` writes into
    the settings with and without one explicit project trust entry, as the App sends it, for the project's root."""

    FULL_START = {'approvalPolicy': 'never', 'approvalsReviewer': 'user', 'sandbox': 'danger-full-access'}

    def settings_after(self, run, entry_root):
        cfg = run.home / 'config.toml'
        self.assertEqual(cfg.read_bytes(), b'')
        client = run.start()
        params = dict(self.FULL_START)
        if entry_root is not None:
            params['config'] = {'projects': {os.path.realpath(str(entry_root)): {'trust_level': 'untrusted'}}}
        self.assertEqual(client.start_thread(**params)['sandbox']['type'], 'dangerFullAccess')
        time.sleep(2)
        return cfg.read_text()

    def test_a_git_project_is_marked_trusted_in_the_settings_unless_an_entry_is_sent(self):
        for entry in (False, True):
            with self.subTest(entry=entry), L.Run(SCRATCH, BINARY, working_files=True, git_marker=True) as run:
                (run.project / '.git' / 'HEAD').write_text('ref: refs/heads/main\n')
                written = self.settings_after(run, run.project if entry else None)
                if entry:
                    self.assertEqual(written, '')
                else:
                    self.assertEqual(written, '[projects."%s"]\ntrust_level = "trusted"\n' % os.path.realpath(str(run.project)))

    def test_a_worktree_marks_its_main_repository_unless_an_entry_for_the_worktree_is_sent(self):
        for entry in (False, True):
            with self.subTest(entry=entry), L.Run(SCRATCH, BINARY, working_files=True, project_name='wt') as run:
                main = run.root / 'outside' / 'main'
                linked = main / '.git' / 'worktrees' / 'wt'
                linked.mkdir(parents=True)
                (main / '.git' / 'HEAD').write_text('ref: refs/heads/main\n')
                (linked / 'HEAD').write_text('ref: refs/heads/wt\n')
                (linked / 'commondir').write_text('../..\n')
                (linked / 'gitdir').write_text(str(run.project / '.git') + '\n')
                (run.project / '.git').write_text('gitdir: %s\n' % linked)
                written = self.settings_after(run, run.project if entry else None)
                if entry:
                    self.assertEqual(written, '')  # the entry for the worktree's own root is enough
                else:
                    self.assertEqual(written, '[projects."%s"]\ntrust_level = "trusted"\n' % os.path.realpath(str(main)))


class AskEachCommandInsideTheProject(unittest.TestCase):
    """Whether a level can ask about each command and keep what the person allows inside the project: approval
    `untrusted` with a workspace-write sandbox (not a level of the App's table). The command writes outside the
    project, which the workspace-write sandbox refuses when it applies."""

    def outside_write(self, decision):
        saved = dict(L.DECLINE)
        L.DECLINE['item/commandExecution/requestApproval'] = {'decision': decision}
        try:
            with L.Run(SCRATCH, BINARY) as run:
                run.stub.scripts['w'] = L.command_script('call_w', run.commands()['out'])
                client = run.start()
                workspace = {'network_access': False, 'exclude_slash_tmp': True, 'exclude_tmpdir_env_var': True,
                             'writable_roots': []}
                reply = client.start_thread(approvalPolicy='untrusted', approvalsReviewer='user', sandbox='workspace-write',
                                            config={'sandbox_workspace_write': workspace})
                self.assertEqual((reply['approvalPolicy'], reply['sandbox']['type']), ('untrusted', 'workspaceWrite'))
                client.turn(reply['thread']['id'], 'LEVEL[w] go', approvalPolicy='untrusted', approvalsReviewer='user',
                            sandboxPolicy={'type': 'workspaceWrite', 'writableRoots': [], 'networkAccess': False,
                                           'excludeTmpdirEnvVar': True, 'excludeSlashTmp': True})
                asked = [r for r in client.server_requests if r['method'] == 'item/commandExecution/requestApproval']
                return len(asked), run.paths()['out'].exists()
        finally:
            L.DECLINE.clear()
            L.DECLINE.update(saved)

    def test_an_allowed_command_is_not_kept_inside_the_project(self):
        self.assertEqual(self.outside_write('decline'), (1, False))  # asked; declined, nothing is written
        self.assertEqual(self.outside_write('accept'), (1, True))  # asked once; allowed, it writes outside the project


class Background(Probing):
    def test_a_background_commands_item_stays_in_progress_after_its_turn_and_completes_when_it_ends(self):
        """A command left running when its turn completes: its item was started with a process id, and is still
        in progress (no completed item) once the turn has completed; when the process ends, the item completes."""
        with L.Run(SCRATCH, BINARY) as run:
            client = run.start()
            thread = client.start_thread()['thread']['id']
            late = run.paths()['late']
            run.stub.scripts['late'] = L.command_script('call_late', run.commands()['late'], background=True)
            turn, done = client.turn(thread, 'LEVEL[late] go', **FULL)
            self.assertEqual(done['turn']['status'], 'completed')
            self.assertFalse(late.exists())  # still sleeping
            started = [n['params']['item'] for n in client.notes_for('item/started', thread)
                       if n['params']['item'].get('id') == 'call_late']
            self.assertEqual(len(started), 1)
            self.assertEqual(started[0].get('status'), 'inProgress')
            self.assertTrue(started[0].get('processId'))

            def completed():
                return [n['params']['item'] for n in client.notes_for('item/completed', thread)
                        if n['params']['item'].get('id') == 'call_late']
            self.assertEqual(completed(), [])  # the turn completed; the command's item did not
            final = client.wait(completed, 20)
            self.assertTrue(late.exists())
            self.assertTrue(final, 'the item did not complete within 20 s of its turn')
            self.assertEqual((final[0].get('status'), final[0].get('exitCode')), ('completed', 0))


def invented_jwt(claims):
    """An invented, unsigned token of the shape Codex parses. Nothing in it belongs to anyone."""
    import base64
    part = lambda value: base64.urlsafe_b64encode(json.dumps(value).encode()).rstrip(b'=').decode()  # noqa: E731
    return '%s.%s.%s' % (part({'alg': 'none', 'typ': 'JWT'}), part(claims), 'invented-signature')


def invented_sign_in(home, refreshed_days_ago):
    """AN INVENTED SIGN-IN, in the run's own invented home: a made-up ChatGPT credential file with invented
    tokens, an invented address and an invented account id, kept in the home's own file (never a keychain).
    It signs in to nothing: no server issued it."""
    exp = int(time.time()) + 30 * 86400
    claims = {'email': 'invented-person@example.invalid', 'exp': exp,
              'https://api.openai.com/auth': {'chatgpt_plan_type': 'plus',
                                              'chatgpt_account_id': 'invented-account-0001'}}
    last = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(time.time() - refreshed_days_ago * 86400))
    (home / 'auth.json').write_text(json.dumps({
        'auth_mode': 'chatgpt', 'OPENAI_API_KEY': None,
        'tokens': {'id_token': invented_jwt(claims), 'access_token': invented_jwt(claims),
                   'refresh_token': 'invented-refresh-token', 'account_id': 'invented-account-0001'},
        'last_refresh': last}))
    os.chmod(home / 'auth.json', 0o600)
    (home / 'config.toml').write_text('cli_auth_credentials_store = "file"\n')


class AccountRead(unittest.TestCase):
    """What the App's account read (`account/read`, empty params) and model list read (`model/list`) contact, on an
    account home with no sign-in and with an invented ChatGPT sign-in. The network is denied as everywhere in this
    suite; the proxy's closed port is replaced by a listener that refuses the same way and records each target.
    Before each read the run waits until Codex's own start-up attempts have stopped for 3 s, so an attempt seen
    during a read is the read's."""

    QUIET = 3.0

    def settle(self, recorder, limit=30.0):
        """Wait until QUIET seconds have passed with no new attempt (counting from now); return all attempts so far."""
        begun = time.monotonic()
        while True:
            with recorder.lock:
                last = max([begun] + [at for at, _, _ in recorder.attempts])
            now = time.monotonic()
            if now - last >= self.QUIET:
                return recorder.since(0)
            self.assertLess(now - begun, limit, 'attempts did not stop within %.0f s' % limit)
            time.sleep(0.25)

    def observe(self, signed_in):
        recorder = L.RecordingRefusal()
        try:
            with L.Run(SCRATCH, BINARY, proxy=recorder) as run:
                if signed_in:
                    invented_sign_in(run.home, refreshed_days_ago=0)
                else:
                    (run.home / 'config.toml').write_text('cli_auth_credentials_store = "file"\n')
                client = run.start()
                startup = self.settle(recorder)
                mark = time.monotonic()
                account = client.call('account/read', {}, timeout=60)
                during_account = recorder.since(mark)
                self.settle(recorder)
                mark = time.monotonic()
                models = client.call('model/list', {'includeHidden': False}, timeout=60)
                during_models = recorder.since(mark)
                self.settle(recorder)
                mark = time.monotonic()
                history = client.call('thread/list', {'sortDirection': 'desc'}, timeout=60)
                during_history = recorder.since(mark)
                self.settle(recorder)
                return {'startup': startup, 'account': account, 'during_account': during_account,
                        'models': models, 'during_models': during_models,
                        'history': history, 'during_history': during_history}
        finally:
            recorder.close()

    def test_with_no_sign_in_the_account_read_contacts_nothing_and_reports_no_account(self):
        seen = self.observe(signed_in=False)
        self.assertEqual(seen['account'].get('result', {}).get('account', 'missing'), None, seen['account'])
        self.assertEqual(seen['during_account'], [])
        self.assertTrue(seen['models'].get('result', {}).get('data'), 'the model list is answered')
        self.assertEqual(seen['during_models'], [])
        self.assertIn('data', seen['history'].get('result', {}), seen['history'])
        self.assertEqual(seen['during_history'], [], 'the history list read contacts nothing')
        self.assertIn(('CONNECT', 'chatgpt.com:443'), seen['startup'], 'Codex itself tries the network at start')

    def test_with_an_invented_sign_in_the_account_read_contacts_the_account_server_and_fails_when_refused(self):
        seen = self.observe(signed_in=True)
        targets = {target for _, target in seen['during_account']}
        self.assertIn('chatgpt.com:443', targets, 'the read asks the account server (workspace routing)')
        self.assertLessEqual(targets, {'chatgpt.com:443', 'auth.openai.com:443'}, seen['during_account'])
        self.assertIn('error', seen['account'], 'refused, the read answers an error, never an account')
        self.assertNotIn('result', seen['account'])
        self.assertTrue(seen['models'].get('result', {}).get('data'), 'the model list is answered')
        self.assertEqual(seen['during_models'], [], 'the model list read itself contacts nothing')
        self.assertIn('data', seen['history'].get('result', {}), seen['history'])
        self.assertEqual(seen['during_history'], [], 'the history list read contacts nothing')
        self.assertIn(('CONNECT', 'chatgpt.com:443'), seen['startup'], 'Codex itself tries the network at start')


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
                items, asked, completed = evidence(client, child_thread, call_id)
                outcomes[key] = L.judge(call_id, run.stub.issued, run.stub.not_offered,
                                        run.stub.outputs.get(call_id), items, asked, 'completed',
                                        target=run.paths()[key], item_status=completed and completed.get('status'),
                                        item_exit=completed and completed.get('exitCode'))
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
        self.assertEqual(seen['outcomes']['out2'].evidence['item_status'], 'declined')
        self.assertIsNone(seen['outcomes']['out2'].evidence['item_exit'])
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
            client.kill()
            client.drain()  # every frame of this server's life has been read
            # An observation, with no control: no serverRequest/resolved arrived in this server's whole life.
            observed = time.monotonic() - interrupted_at
            self.assertEqual(client.notes_for('serverRequest/resolved'), [], 'within %.1f s' % observed)

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

            # Over the second server's whole life, read to its end: the outstanding call was never raised again,
            # while new calls on the same client were (call_resumed, call_forked: the control).
            again.stop()
            again.drain()
            observed = time.monotonic() - resumed_at
            self.assertEqual(tool_calls(again, outstanding['params']['callId']), [], 'within %.1f s' % observed)
            self.assertEqual(tool_calls(again, interrupted['params']['callId']), [])
            self.assertEqual(len(tool_calls(again)), 2)

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
    """Case 6: the supplier's question tool in an ordinary conversation. Default mode and plan mode run on one
    client, each the other's control."""

    def test_refused_in_default_mode_and_reaches_the_client_in_plan_mode(self):
        with L.Run(SCRATCH, BINARY) as run:
            client = run.start()
            seen = {}
            for mode, settings in (('default', {}),
                                   ('plan', {'collaborationMode': {'mode': 'plan', 'settings': {'model': L.MODEL}}})):
                thread = client.start_thread()['thread']['id']
                call_id = 'call_ask_' + mode

                def script(body, outputs, stub, call_id=call_id):
                    if call_id in outputs:
                        return [L.message('Asked.', 'msg_' + call_id)]
                    return [{'type': 'function_call', 'name': 'request_user_input', 'call_id': call_id,
                             'id': 'fc_' + call_id, 'arguments': json.dumps({'questions': [{
                                 'id': 'q1', 'header': 'Invented', 'question': 'Invented question?',
                                 'options': [{'label': 'Yes', 'description': 'Invented yes'},
                                             {'label': 'No', 'description': 'Invented no'}]}]})}]
                run.stub.scripts[call_id] = script
                _, done = client.turn(thread, 'LEVEL[%s] go' % call_id, **settings)
                self.assertEqual(done['turn']['status'], 'completed')
                self.assertIn(call_id, run.stub.issued)
                request = next(r for r in run.stub.requests if r['key'] == call_id)
                seen[mode] = ('request_user_input' in request['tools'],
                              [r['method'] for r in client.server_requests if r['thread'] == thread],
                              run.stub.outputs.get(call_id, ''))
            listed, requests, output = seen['default']
            self.assertTrue(listed)
            self.assertEqual(requests, [])
            self.assertIn('unavailable in Default mode', output)
            listed, requests, _ = seen['plan']
            self.assertTrue(listed)
            self.assertEqual(requests, ['item/tool/requestUserInput'])


QUESTION_FLAG = 'features.default_mode_request_user_input=true'
INVENTED_QUESTION = {'id': 'q1', 'header': 'Invented', 'question': 'Invented question?',
                     'options': [{'label': 'Yes', 'description': 'Invented yes'},
                                 {'label': 'No', 'description': 'Invented no'}]}


def question_script(call_id):
    def script(body, outputs, stub):
        if call_id in outputs:
            return [L.message('Asked.', 'msg_' + call_id)]
        return [{'type': 'function_call', 'name': 'request_user_input', 'call_id': call_id, 'id': 'fc_' + call_id,
                 'arguments': json.dumps({'questions': [INVENTED_QUESTION]})}]
    return script


def questions_raised(client, call_id=None):
    return [r for r in client.server_requests if r['method'] == 'item/tool/requestUserInput'
            and (call_id is None or r['params'].get('itemId') == call_id)]


def question_tool_description(request):
    for tool in request['body_tools'] or []:
        if isinstance(tool, dict) and tool.get('name') == 'request_user_input':
            return tool.get('description') or ''
    return None


class QuestionInAnOrdinaryConversation(unittest.TestCase):
    """Case 7: the supplier's question tool in Default mode, once Codex is started with the under-development
    feature `default_mode_request_user_input`. No collaboration mode is sent on any turn here."""

    def ask(self, run, client, thread, key, **settings):
        """Start a turn whose scripted model asks the invented question; return (turn id, the request raised)."""
        call_id = 'call_' + key
        run.stub.scripts[key] = question_script(call_id)
        params = dict({'threadId': thread, 'input': [{'type': 'text', 'text': 'LEVEL[%s] go' % key}]}, **settings)
        turn = client.result('turn/start', params)['turn']['id']
        self.assertTrue(client.wait(lambda: questions_raised(client, call_id), 30))
        self.assertIn(call_id, run.stub.issued)
        asked = questions_raised(client, call_id)[0]
        self.assertEqual((asked['thread'], asked['params'].get('turnId')), (thread, turn))
        return turn, asked

    def completed(self, client, thread, turn, timeout=30):
        done = client.wait(lambda: client.notes_for('turn/completed', thread, turn), timeout)
        self.assertTrue(done)
        return done[0]['params']['turn']['status']

    def test_at_every_level_of_the_apps_table_the_question_reaches_the_client_and_its_answer_reaches_the_agent(self):
        table = json.loads(LEVELS_TABLE.read_text())
        for row in table['levels']:
            with self.subTest(level=row['id']), L.Run(SCRATCH, BINARY) as run:
                start, each_turn = level_settings(row)
                client = run.start(flags=[QUESTION_FLAG])
                client.question_policy = 'hold'
                thread = client.start_thread(**start)['thread']['id']
                key = 'ask_' + row['id'].replace('-', '_')
                turn, asked = self.ask(run, client, thread, key, **each_turn)
                params = asked['params']
                self.assertIs(params.get('isBlocking'), False)  # Codex marks it as one that need not block
                self.assertIsNone(params.get('autoResolutionMs'))
                self.assertEqual(len(params['questions']), 1)
                question = params['questions'][0]
                self.assertEqual({k: question.get(k) for k in INVENTED_QUESTION}, INVENTED_QUESTION)
                self.assertIs(question.get('isOther'), True)  # Codex adds the free answer itself
                listed = question_tool_description(next(r for r in run.stub.requests if r['key'] == key))
                self.assertIn('Default', listed)
                self.assertIn('Plan', listed)
                self.assertFalse(client.notes_for('turn/completed', thread, turn))
                client.answer_question(asked, {'q1': ['Yes']})
                self.assertEqual(self.completed(client, thread, turn), 'completed')
                self.assertEqual(json.loads(run.stub.outputs['call_' + key]), {'answers': {'q1': {'answers': ['Yes']}}})
                # Over the server's whole life, read to the end of its output after the turn completed: the
                # question, and nothing else, was asked of the client.
                client.stop()
                client.drain()
                self.assertEqual([r['method'] for r in client.server_requests], ['item/tool/requestUserInput'])

    def test_with_the_feature_off_in_the_homes_own_settings_the_session_flag_still_raises_the_question(self):
        """The person's own settings name the feature off; the App's session flag is given all the same. The
        control is the same home without the flag, which refuses the call."""
        full = next(r for r in json.loads(LEVELS_TABLE.read_text())['levels'] if r['id'] == 'full')
        start, each_turn = level_settings(full)
        off = '[features]\ndefault_mode_request_user_input = false\n'
        with L.Run(SCRATCH, BINARY) as run:
            (run.home / 'config.toml').write_text(off)
            client = run.start(flags=[QUESTION_FLAG])
            client.question_policy = 'hold'
            thread = client.start_thread(**start)['thread']['id']
            turn, asked = self.ask(run, client, thread, 'setoff', **each_turn)
            client.answer_question(asked, {'q1': ['Yes']})
            self.assertEqual(self.completed(client, thread, turn), 'completed')
            self.assertEqual(json.loads(run.stub.outputs['call_setoff']), {'answers': {'q1': {'answers': ['Yes']}}})
            self.assertEqual((run.home / 'config.toml').read_text(), off)  # the person's settings are as they were
        with L.Run(SCRATCH, BINARY) as run:
            (run.home / 'config.toml').write_text(off)
            client = run.start()
            client.question_policy = 'hold'
            thread = client.start_thread(**start)['thread']['id']
            run.stub.scripts['setoffplain'] = question_script('call_setoffplain')
            _, done = client.turn(thread, 'LEVEL[setoffplain] go', **each_turn)
            self.assertEqual(done['turn']['status'], 'completed')
            self.assertEqual(questions_raised(client), [])
            self.assertIn('unavailable in Default mode', run.stub.outputs.get('call_setoffplain', ''))

    def test_without_the_feature_the_same_start_refuses_the_question(self):
        """The control for the row above, on the level the App uses by default."""
        full = next(r for r in json.loads(LEVELS_TABLE.read_text())['levels'] if r['id'] == 'full')
        start, each_turn = level_settings(full)
        with L.Run(SCRATCH, BINARY) as run:
            client = run.start()
            client.question_policy = 'hold'
            thread = client.start_thread(**start)['thread']['id']
            run.stub.scripts['plain'] = question_script('call_plain')
            _, done = client.turn(thread, 'LEVEL[plain] go', **each_turn)
            self.assertEqual(done['turn']['status'], 'completed')
            self.assertIn('call_plain', run.stub.issued)
            self.assertEqual(questions_raised(client), [])
            self.assertIn('unavailable in Default mode', run.stub.outputs.get('call_plain', ''))
            listed = question_tool_description(next(r for r in run.stub.requests if r['key'] == 'plain'))
            self.assertNotIn('Default', listed)

    def test_held_declined_interrupted_relaunched_resumed_and_forked(self):
        full = next(r for r in json.loads(LEVELS_TABLE.read_text())['levels'] if r['id'] == 'full')
        start, each_turn = level_settings(full)
        with L.Run(SCRATCH, BINARY) as run:
            client = run.start(flags=[QUESTION_FLAG])
            client.question_policy = 'hold'
            thread = client.start_thread(**start)['thread']['id']

            # Unanswered, the question waits: Codex answers nothing for the person and the turn does not end.
            turn, held = self.ask(run, client, thread, 'held', **each_turn)
            held_since = time.monotonic()
            self.assertFalse(client.wait(lambda: client.notes_for('turn/completed', thread, turn), HOLD))
            self.assertGreaterEqual(time.monotonic() - held_since, HOLD - 1)
            self.assertIsNone(client.proc.poll())  # the server is still up
            self.assertNotIn('call_held', run.stub.outputs)  # and the agent has been told nothing
            client.answer_question(held, {'q1': ['A free answer, invented.']})
            self.assertEqual(self.completed(client, thread, turn), 'completed')
            self.assertEqual(json.loads(run.stub.outputs['call_held']),
                             {'answers': {'q1': {'answers': ['A free answer, invented.']}}})

            # An explicit decline is an answer with no answers, and the agent is told exactly that.
            turn, declined = self.ask(run, client, thread, 'declined', **each_turn)
            client.answer_question(declined, {})
            self.assertEqual(self.completed(client, thread, turn), 'completed')
            self.assertEqual(json.loads(run.stub.outputs['call_declined']), {'answers': {}})

            # Interrupting the turn ends it; the question's call is not answered.
            turn, interrupted = self.ask(run, client, thread, 'interrupted', **each_turn)
            client.result('turn/interrupt', {'threadId': thread, 'turnId': turn})
            self.assertEqual(self.completed(client, thread, turn, 20), 'interrupted')
            self.assertNotIn('call_interrupted', run.stub.outputs)

            # Ended with a question outstanding, as a quit or a crash ends it.
            turn, outstanding = self.ask(run, client, thread, 'relaunch', **each_turn)
            client.kill()
            client.drain()

            again = run.start(flags=[QUESTION_FLAG])
            again.question_policy = 'hold'
            resumed_at = time.monotonic()
            again.result('thread/resume', {'threadId': thread})
            time.sleep(10)
            turns = again.result('thread/turns/list', {'threadId': thread})['data']
            self.assertEqual(next(t['status'] for t in turns if t['id'] == turn), 'interrupted')

            # A new question on the resumed conversation is raised and answered.
            turn, resumed = self.ask(run, again, thread, 'resumed', **each_turn)
            again.answer_question(resumed, {'q1': ['No']})
            self.assertEqual(self.completed(again, thread, turn), 'completed')
            self.assertEqual(json.loads(run.stub.outputs['call_resumed']), {'answers': {'q1': {'answers': ['No']}}})

            # And on a fork of it.
            fork = again.result('thread/fork', {'threadId': thread})['thread']['id']
            turn, forked = self.ask(run, again, fork, 'forked', **each_turn)
            again.answer_question(forked, {'q1': ['Yes']})
            self.assertEqual(self.completed(again, fork, turn), 'completed')
            self.assertEqual(json.loads(run.stub.outputs['call_forked']), {'answers': {'q1': {'answers': ['Yes']}}})

            # Over the second server's whole life, read to its end: the question outstanding when the first
            # server ended, and the interrupted one, were never raised again, while new ones were (the control).
            again.stop()
            again.drain()
            observed = time.monotonic() - resumed_at
            self.assertEqual(questions_raised(again, outstanding['params']['itemId']), [], 'within %.1f s' % observed)
            self.assertEqual(questions_raised(again, interrupted['params']['itemId']), [])
            self.assertEqual(len(questions_raised(again)), 2)

    def test_a_childs_question_is_refused_and_reaches_no_one(self):
        with L.Run(SCRATCH, BINARY) as run:
            client = run.start(flags=[QUESTION_FLAG])
            client.question_policy = 'hold'
            thread = client.start_thread()['thread']['id']
            # The control: the parent's own question reaches the client.
            turn, asked = self.ask(run, client, thread, 'parentask')
            client.answer_question(asked, {'q1': ['Yes']})
            self.assertEqual(self.completed(client, thread, turn), 'completed')
            run.stub.scripts['spawn'] = spawn_script('childask')
            run.stub.scripts['childask'] = question_script('call_childask')
            child = spawn_child(self, run, client, thread)
            self.assertIn('call_childask', run.stub.issued)
            self.assertEqual(questions_raised(client, 'call_childask'), [])
            self.assertEqual([r for r in client.server_requests if r['thread'] == child], [])
            self.assertIn('can only be used by the root thread', run.stub.outputs.get('call_childask', ''))

    def test_what_a_catalogue_model_is_told_about_the_tool_with_and_without_the_feature(self):
        """For a model with a catalogue entry the request to the provider carries no `tools`, so what the model is
        told is read from the whole request. Each start is the other's control."""
        seen = {}
        for name, flags in (('with', [QUESTION_FLAG]), ('without', [])):
            with L.Run(SCRATCH, BINARY) as run:
                client = run.start(flags=flags)
                client.question_policy = 'hold'
                thread = client.start_thread(model=CATALOGUE_MODEL)['thread']['id']
                bodies = []

                def script(body, outputs, stub, bodies=bodies):
                    bodies.append(json.dumps(body))
                    if 'call_told' in outputs:
                        return [L.message('Asked.', 'msg_told')]
                    return [{'type': 'function_call', 'name': 'request_user_input', 'call_id': 'call_told',
                             'id': 'fc_told', 'arguments': json.dumps({'questions': [INVENTED_QUESTION]})}]
                run.stub.scripts['told'] = script
                turn = client.result('turn/start', {'threadId': thread, 'input': [
                    {'type': 'text', 'text': 'LEVEL[told] go'}]})['turn']['id']
                if name == 'with':
                    self.assertTrue(client.wait(lambda: questions_raised(client, 'call_told'), 30))
                    client.answer_question(questions_raised(client, 'call_told')[0], {'q1': ['Yes']})
                self.assertEqual(self.completed(client, thread, turn), 'completed')
                seen[name] = (bodies[0], len(questions_raised(client)), run.stub.outputs.get('call_told', ''))
                # For this model the request to the provider carries no `tools`, with the feature or without.
                self.assertTrue(all('tools' not in r['body_keys'] for r in run.stub.requests if r['key'] == 'told'))
                self.assertNotIn('tools', json.loads(bodies[0]))
        told, raised, output = seen['with']
        self.assertEqual(raised, 1)
        self.assertEqual(json.loads(output), {'answers': {'q1': {'answers': ['Yes']}}})
        self.assertIn('This tool is only available in Default or Plan mode', told)
        # The supplier's own words to this model about asking in an ordinary conversation.
        self.assertIn('only for optional questions where the answer would materially improve', told)
        self.assertIn('continue with best judgment instead of asking again', told)
        told, raised, output = seen['without']
        self.assertEqual(raised, 0)
        self.assertIn('unavailable in Default mode', output)
        self.assertNotIn('This tool is only available in Default or Plan mode', told)


CATALOGUE_MODEL = 'gpt-6.1-sol'  # a model whose entry in the pinned Codex's bundled catalogue lists the tool below
ASYNC_QUESTION = {'title': 'Invented question, asked without waiting?', 'options': ['Invented yes', 'Invented no']}


class QuestionThatDoesNotWait(unittest.TestCase):
    """Case 8: `request_user_input_async`, which Codex offers by the model's catalogue entry, with no feature set
    and no collaboration mode sent. It raises no request: the question arrives as an agent message item."""

    def test_the_question_arrives_as_an_agent_message_item_and_the_turn_does_not_wait(self):
        with L.Run(SCRATCH, BINARY) as run:
            client = run.start()
            thread = client.start_thread(model=CATALOGUE_MODEL)['thread']['id']

            # The call is made whether or not the request lists the tool: for a catalogue model the request to
            # the provider carries no `tools` (seen below), so the listing cannot be read from it.
            def script(body, outputs, stub):
                if 'call_nowait' in outputs:
                    return [L.message('Carried on.', 'msg_nowait')]
                return [{'type': 'function_call', 'name': 'request_user_input_async', 'call_id': 'call_nowait',
                         'id': 'fc_nowait', 'arguments': json.dumps({'questions': [ASYNC_QUESTION]})}]
            run.stub.scripts['nowait'] = script
            turn, done = client.turn(thread, 'LEVEL[nowait] go')
            request = next(r for r in run.stub.requests if r['key'] == 'nowait')
            output = run.stub.outputs.get('call_nowait')
            self.assertNotIn('tools', request['body_keys'])
            if output != '{"accepted":true}':
                self.fail('inconclusive: the call was answered %r; the request held %r and listed %r'
                          % (output, request['body_keys'], request['tools']))
            self.assertIn('call_nowait', run.stub.issued)
            self.assertEqual(done['turn']['status'], 'completed')  # with no answer from anyone
            self.assertEqual(json.loads(run.stub.outputs['call_nowait']), {'accepted': True})
            self.assertEqual([r['method'] for r in client.server_requests if r['thread'] == thread], [])
            asked = [i for i in client.items(thread, turn, 'agentMessage') if i.get('questions')]
            self.assertEqual(len(asked), 1)
            self.assertEqual(asked[0]['questions'], [ASYNC_QUESTION])
            self.assertEqual(asked[0].get('delivery'), 'async')
            self.assertEqual(asked[0]['id'], 'call_nowait')

            # After the server is ended and the conversation resumed, its history still holds the question.
            client.kill()
            client.drain()
            again = run.start()
            again.result('thread/resume', {'threadId': thread})
            read = again.result('thread/read', {'threadId': thread, 'includeTurns': True})
            self.assertEqual(read['thread']['id'], thread)
            # The same item, in the same turn of the same conversation: its id, its delivery and its questions.
            kept = [(t['id'], i['id'], i.get('delivery'), i['questions'])
                    for t in read['thread']['turns'] for i in t.get('items') or []
                    if i.get('type') == 'agentMessage' and (i.get('questions') or i.get('delivery'))]
            self.assertEqual(kept, [(turn, 'call_nowait', 'async', [ASYNC_QUESTION])])

    def test_on_a_model_the_catalogue_does_not_list_it_for_the_same_call_is_unsupported(self):
        """The control: the fixture's invented model has no catalogue entry."""
        with L.Run(SCRATCH, BINARY) as run:
            client = run.start()
            thread = client.start_thread()['thread']['id']

            def script(body, outputs, stub):
                if 'call_plainmodel' in outputs:
                    return [L.message('Done.', 'msg_plainmodel')]
                return [{'type': 'function_call', 'name': 'request_user_input_async', 'call_id': 'call_plainmodel',
                         'id': 'fc_plainmodel', 'arguments': json.dumps({'questions': [ASYNC_QUESTION]})}]
            run.stub.scripts['plainmodel'] = script
            turn, done = client.turn(thread, 'LEVEL[plainmodel] go')
            self.assertEqual(done['turn']['status'], 'completed')
            self.assertIn('call_plainmodel', run.stub.issued)
            self.assertTrue(run.stub.outputs.get('call_plainmodel', '').startswith('unsupported call'))
            self.assertEqual([i for i in client.items(thread, turn, 'agentMessage') if i.get('questions')], [])
            tools = next(r['tools'] for r in run.stub.requests if r['key'] == 'plainmodel')
            self.assertIn('request_user_input', tools)
            self.assertNotIn('request_user_input_async', tools)


SECOND = 'project-b'


def same_folder(a, b):
    """Whether two folders are the same one. A reported folder that is not an absolute path is no folder: it is
    never resolved against the folder these tests happen to run in."""
    if a is None or b is None or not os.path.isabs(str(a)) or not os.path.isabs(str(b)):
        return False
    return os.path.realpath(str(a)) == os.path.realpath(str(b))


def app_level(level_id):
    """One row of the App's own table, by its id."""
    return next(r for r in json.loads(LEVELS_TABLE.read_text())['levels'] if r['id'] == level_id)


class FolderPerConversation(Probing):
    """One app server for every project, each conversation given its own folder. The app server is started in the
    project A (`Run.project`, as `Client` starts it); each conversation under test is started in a second project
    B beside it (`Run(second_project=...)`), with the folder on `thread/start` and `thread/resume` as the App sends
    it. Each test asserts that B governs what it names. Where that could fail, the message states what was
    observed instead, naming A and B, so a failing run reports the fact either way."""

    EDITS = app_level('edits')

    def named(self, run, path):
        """A folder as the messages name it: B, A (the process's own folder), or its path."""
        if path is None:
            return 'nothing'
        if same_folder(path, run.project_b):
            return 'B (%s)' % path
        if same_folder(path, run.project):
            return "A, the server's own folder (%s)" % path
        return str(path)

    def entry(self, folder, trust='untrusted'):
        """The App's one trust entry: the folder's root under its canonical spelling, as `TrustReading::projects`
        sends it. Neither project here has a `.git` with `HEAD` above itself, so the root is the folder."""
        return {os.path.realpath(str(folder)): {'trust_level': trust}}

    def app_frame(self, folder, trust='untrusted'):
        """What the App adds to `thread/start` and `thread/resume` at the edits level, for a conversation in
        `folder`: the folder; the level's approval, reviewer, mode name and workspace options; and the one trust
        entry. "untrusted" is what the App sends for a folder the person's settings do not mark."""
        start, turn = level_settings(self.EDITS)
        frame = dict(start, cwd=str(folder))
        frame['config'] = dict(start['config'], projects=self.entry(folder, trust))
        return frame, turn

    def start_in(self, run, client, folder, trust='untrusted'):
        frame, turn = self.app_frame(folder, trust)
        return client.start_thread(**frame), turn

    def saved(self, client, thread, **turn):
        """One turn with no command, so that the conversation is saved: the stub answers it with a message."""
        _, done = client.turn(thread, 'LEVEL[none] save', **turn)
        self.assertEqual(done and done['turn']['status'], 'completed')

    def ran_in(self, run, client, thread, **turn):
        """The folder a command runs in: `/bin/pwd -P`'s own output, after it ran and succeeded."""
        return self.succeeded(probe(run, client, thread, 'pwd', **turn)).text

    def relative_write(self, run, client, thread, **turn):
        """The relative write, and where its file landed: ({'a': bool, 'b': bool}, the outcome)."""
        for path in run.relative_landings().values():
            if path.exists():
                path.unlink()
        outcome = probe(run, client, thread, 'relative', **turn)
        if outcome.kind == L.NOT_OFFERED:
            expect(outcome, SUCCEEDED)  # inconclusive: fails, saying so
        for side, path in run.relative_landings().items():
            if path.exists():  # the file is this call's: both landings were cleared before it
                self.assertEqual(path.read_text(), 'ok', 'the relative write left other bytes in %s' % side.upper())
        return {side: path.exists() for side, path in run.relative_landings().items()}, outcome

    def governed_by_b(self, run, client, thread, **turn):
        """The command facts of a conversation in B at the edits level: it runs in B; the relative write lands in
        B; the write in B succeeds; the write in A, the server's own folder, runs and is refused by the sandbox."""
        folder = self.ran_in(run, client, thread, **turn)
        self.assertTrue(same_folder(folder, run.project_b),
                        'the command ran in %s, not in B' % self.named(run, folder))
        landed, outcome = self.relative_write(run, client, thread, **turn)
        self.assertEqual((outcome.kind, landed), (SUCCEEDED, {'a': False, 'b': True}),
                         'the relative write was observed %r and landed in A: %s, in B: %s'
                         % (outcome, landed['a'], landed['b']))
        in_b = probe(run, client, thread, 'in-b', **turn)
        if in_b.kind != SUCCEEDED:
            self.fail('the write in B was observed %r: the sandbox did not take B as the project' % in_b)
        self.succeeded(in_b)
        in_a = probe(run, client, thread, 'in', **turn)
        if in_a.kind == SUCCEEDED:
            self.fail("the write in A, the server's own folder, succeeded at edits: A was writable as well")
        self.refused(in_a)

    def test_a_thread_started_in_b_reports_b_and_is_listed_under_b_alone(self):
        with L.Run(SCRATCH, BINARY, second_project=SECOND) as run:
            client = run.start()
            in_b, turn = self.start_in(run, client, run.project_b)
            in_a, _ = self.start_in(run, client, run.project)
            b, a = in_b['thread']['id'], in_a['thread']['id']
            for reply, folder, name in ((in_b, run.project_b, 'B'), (in_a, run.project, 'A')):
                self.assertTrue(same_folder(reply['cwd'], folder), "the start in %s reported the folder %s"
                                % (name, self.named(run, reply['cwd'])))
                self.assertTrue(same_folder(reply['thread']['cwd'], folder), "the start in %s reported the thread's "
                                "folder %s" % (name, self.named(run, reply['thread']['cwd'])))
            self.saved(client, b, **turn)
            self.saved(client, a, **turn)
            listed = {row['id']: row for row in client.result('thread/list', {'sortDirection': 'desc'})['data']}
            self.assertEqual(sorted({a, b} - set(listed)), [], 'a conversation started here was not listed at all')
            self.assertTrue(same_folder(listed[b]['cwd'], run.project_b),
                            "B's conversation is listed with the folder %s" % self.named(run, listed[b]['cwd']))
            self.assertTrue(same_folder(listed[a]['cwd'], run.project))  # the control: A's under A
            for folder, name, wanted, other in ((run.project_b, 'B', b, a), (run.project, 'A', a, b)):
                ids = {row['id'] for row in client.result('thread/list', {
                    'sortDirection': 'desc', 'cwd': os.path.realpath(str(folder))})['data']}
                self.assertEqual((wanted in ids, other in ids), (True, False),
                                 'listed under %s: its own conversation %s, the other %s'
                                 % (name, wanted in ids, other in ids))

    def test_a_command_in_a_thread_started_in_b_runs_in_b(self):
        """`/bin/pwd -P` prints B, and the relative write lands in B and not in A. Both at the edits level, so a
        relative write can land only where the sandbox allows it. A conversation in A is open on the same server
        throughout, and the two take turns: B, A, B, A, B. Each runs and writes in its own folder every time, so
        a folder kept for the whole server, set by whichever conversation started or ran last, would fail."""
        with L.Run(SCRATCH, BINARY, second_project=SECOND) as run:
            client = run.start()
            in_b, turn = self.start_in(run, client, run.project_b)
            in_a, _ = self.start_in(run, client, run.project)  # started second: the last start is in A
            threads = {'b': (in_b['thread']['id'], run.project_b, {'a': False, 'b': True}),
                       'a': (in_a['thread']['id'], run.project, {'a': True, 'b': False})}
            for side in ('b', 'a', 'b', 'a', 'b'):
                thread, own, lands = threads[side]
                folder = self.ran_in(run, client, thread, **turn)
                self.assertTrue(same_folder(folder, own), "%s's command ran in %s"
                                % (side.upper(), self.named(run, folder)))
                landed, outcome = self.relative_write(run, client, thread, **turn)
                self.assertEqual((outcome.kind, landed), (SUCCEEDED, lands),
                                 "%s's relative write was observed %r and landed in A: %s, in B: %s"
                                 % (side.upper(), outcome, landed['a'], landed['b']))

    def test_at_the_edits_level_the_sandbox_takes_b_as_the_project_and_refuses_a(self):
        """Started in B as the App starts it at edits (its one trust entry, untrusted, for B), with the edits level on
        each turn: the write in B succeeds; the write in A, the server's own folder, runs and is refused by the
        sandbox. The control: the same write in A at full access on the same thread succeeds."""
        with L.Run(SCRATCH, BINARY, second_project=SECOND) as run:
            client = run.start()
            reply, turn = self.start_in(run, client, run.project_b)
            thread = reply['thread']['id']
            in_b = probe(run, client, thread, 'in-b', **turn)
            if in_b.kind != SUCCEEDED:
                self.fail('the write in B was observed %r: the sandbox did not take B as the project' % in_b)
            self.succeeded(in_b)
            in_a = probe(run, client, thread, 'in', **turn)
            if in_a.kind == SUCCEEDED:
                self.fail("the write in A, the server's own folder, succeeded at edits: A was writable as well")
            self.refused(in_a)
            self.refused(probe(run, client, thread, 'out', **turn))
            self.succeeded(probe(run, client, thread, 'in', **FULL))  # the control: A's refusal was the sandbox's

    def test_a_thread_started_in_b_loads_bs_instructions_and_not_as(self):
        """An invented `AGENTS.md` in each of A and B, each with its own marker line. For a conversation started in
        B and, as the control, one started in A, each with its one trust entry untrusted and then trusted: which of
        the two files the start reply's `instructionSources` names, and which marker lines the requests the stub
        receives for that conversation's turn carry. With a trusted entry the conversation's own folder's file is
        named and its marker carried, and never the other folder's; with an untrusted entry, as the App sends for
        a folder the person's settings do not mark, no file is named and no marker carried. The markers are looked
        for anywhere in the body of each request the stub received carrying that turn's key, and nowhere else.
        Every case is observed before anything is asserted, so a failure states all of them."""
        with L.Run(SCRATCH, BINARY, second_project=SECOND, instructions=True) as run:
            run.stub.watched = (run.markers['a'], run.markers['b'])
            files = {side: os.path.realpath(str(f / 'AGENTS.md')) for side, f in
                     (('a', run.project), ('b', run.project_b))}
            client = run.start()
            observed = {}
            # B's untrusted start comes before its trusted one and A's after, so being the first or the second
            # start in a folder cannot stand in for the entry.
            for own, folder, order in (('b', run.project_b, ('untrusted', 'trusted')),
                                       ('a', run.project, ('trusted', 'untrusted'))):
                for trust in order:
                    key = 'instr_%s_%s' % (own, trust)
                    reply, turn = self.start_in(run, client, folder, trust)
                    sources = [os.path.realpath(path) for path in reply.get('instructionSources') or []]
                    _, done = client.turn(reply['thread']['id'], 'LEVEL[%s] go' % key, **turn)
                    self.assertEqual(done and done['turn']['status'], 'completed')
                    requests = [r for r in run.stub.requests if r['key'] == key]
                    self.assertTrue(requests, 'no request reached the stub for the turn of %s' % key)
                    carried = {m for r in requests for m in r['markers']}
                    observed[(own, trust)] = {
                        'named': sorted(side for side, path in files.items() if path in sources),
                        'other sources': sorted(path for path in sources if path not in files.values()),
                        'carried': sorted(side for side, marker in run.markers.items() if marker in carried)}
            expected = {(own, trust): {'named': loaded, 'other sources': [], 'carried': loaded}
                        for own in ('b', 'a') for trust, loaded in (('untrusted', []), ('trusted', [own]))}
            self.assertEqual(observed, expected, 'by (the folder the conversation was started in, its trust entry): '
                             'which AGENTS.md the reply named and which marker the turn carried: %r' % (observed,))

    def test_a_thread_started_in_b_loads_bs_own_settings_and_only_when_b_is_trusted(self):
        """The setting: `sandbox_workspace_write.writable_roots` in a project's own `.codex/config.toml`. The
        Carriers rows show it observable twice over: the start reply's `sandbox.writableRoots` lists it, and a
        write there succeeds that is otherwise refused; and a turn's `writableRoots: []` does not remove it. A's
        settings name `outside/root-a`, B's `outside/root-b`, and the home's own settings mark A trusted, so A's
        could load if the server's own folder were read.

        The start departs from the App's frame in one field only: it sends no `config.sandbox_workspace_write`,
        whose `writable_roots = []` would remove the setting from sight. It sends the approval, reviewer, mode
        name and the one trust entry for B, trusted and then untrusted; each turn sends the edits level.
        Trusted: the reply lists root-b alone, the write in root-b succeeds and the write in root-a is refused.
        Untrusted: neither root is listed, and both writes are refused. The control: a conversation started in A,
        with its trusted entry, lists root-a."""
        with L.Run(SCRATCH, BINARY, second_project=SECOND, project_settings=True) as run:
            (run.home / 'config.toml').write_text('[projects.%s]\ntrust_level = "trusted"\n'
                                                  % L.toml_string(os.path.realpath(str(run.project))))
            roots = run.settings_roots()
            turn = level_settings(self.EDITS)[1]
            client = run.start()

            def started(folder, trust):
                reply = client.start_thread(cwd=str(folder), approvalPolicy='on-request', approvalsReviewer='user',
                                            sandbox='workspace-write', config={'projects': self.entry(folder, trust)})
                listed = {os.path.realpath(p) for p in (reply['sandbox'].get('writableRoots') or [])}
                named = {side for side, root in roots.items() if os.path.realpath(str(root)) in listed}
                return reply['thread']['id'], named, sorted(listed)

            control, named, listed = started(run.project, 'trusted')
            self.assertEqual(named, {'a'}, 'started in A, trusted, the reply listed %r' % listed)
            for trust, expected in (('trusted', {'b'}), ('untrusted', set())):
                with self.subTest(trust=trust):
                    thread, named, listed = started(run.project_b, trust)
                    self.assertEqual(named, expected, 'started in B with B %s, the reply listed %r (root-a: %s, '
                                     'root-b: %s)' % (trust, listed, roots['a'], roots['b']))
                    self.succeeded(probe(run, client, thread, 'in-b', **turn))
                    b_root = probe(run, client, thread, 'root-b', **turn)
                    if 'b' in expected:
                        self.assertEqual(b_root.kind, SUCCEEDED, "with B trusted, the write in B's root was "
                                         "observed %r" % b_root)
                        self.succeeded(b_root)
                    else:
                        self.assertNotEqual(b_root.kind, SUCCEEDED, "with B untrusted, the write in B's root "
                                            "succeeded: B's settings were loaded")
                        self.refused(b_root)
                    a_root = probe(run, client, thread, 'root-a', **turn)
                    self.assertNotEqual(a_root.kind, SUCCEEDED, "started in B, the write in A's root succeeded: "
                                        "A's settings were loaded")
                    self.refused(a_root)

    def test_with_the_apps_own_start_a_trusted_projects_writable_root_is_not_added(self):
        """The App's own start at edits, whole: its `config.sandbox_workspace_write` with `writable_roots = []`
        beside the one trust entry, here trusted, for a conversation in B whose own `.codex/config.toml` names
        root-b. The reply lists neither fixture root and the write in root-b is refused by the sandbox, while the
        write in B succeeds: the App's start removes a writable root that a trusted project's own settings name.
        The control is the row above, where the same trusted start without that one field lists root-b and the
        write there succeeds."""
        with L.Run(SCRATCH, BINARY, second_project=SECOND, project_settings=True) as run:
            roots = run.settings_roots()
            client = run.start()
            reply, turn = self.start_in(run, client, run.project_b, 'trusted')
            thread = reply['thread']['id']
            listed = sorted(os.path.realpath(p) for p in (reply['sandbox'].get('writableRoots') or []))
            named = {side for side, root in roots.items() if os.path.realpath(str(root)) in listed}
            b_root = probe(run, client, thread, 'root-b', **turn)
            self.assertEqual((named, b_root.kind), (set(), SANDBOX_REFUSED),
                             "with the App's own start and B trusted, the reply listed %r (root-b: %s) and the "
                             "write in root-b was observed %r" % (listed, roots['b'], b_root))
            self.refused(b_root)
            self.succeeded(probe(run, client, thread, 'in-b', **turn))

    def test_a_start_in_b_marks_b_in_the_settings_unless_an_entry_for_b_is_sent(self):
        """As the trust-mark rows: at full access, in the App's layout with the home's new, empty settings, with
        both A and B git projects. A start in B with no trust entry writes the trust mark for B alone; with the
        App's one entry for B, nothing is written. Each start is the other's control."""
        for entry in (False, True):
            with self.subTest(entry=entry), L.Run(SCRATCH, BINARY, working_files=True, git_marker=True,
                                                  second_project=SECOND, second_git_marker=True) as run:
                for folder in (run.project, run.project_b):
                    (folder / '.git' / 'HEAD').write_text('ref: refs/heads/main\n')
                cfg = run.home / 'config.toml'
                self.assertEqual(cfg.read_bytes(), b'')
                client = run.start()
                params = dict(TrustWrite.FULL_START, cwd=str(run.project_b))
                if entry:
                    params['config'] = {'projects': self.entry(run.project_b)}
                self.assertEqual(client.start_thread(**params)['sandbox']['type'], 'dangerFullAccess')
                time.sleep(2)
                written = cfg.read_text()
                if entry:
                    self.assertEqual(written, '', 'with the entry for B sent, the settings now read %r' % written)
                else:
                    self.assertEqual(written, '[projects."%s"]\ntrust_level = "trusted"\n'
                                     % os.path.realpath(str(run.project_b)),
                                     'with no entry sent, the settings now read %r (A: %s, B: %s)'
                                     % (written, run.project, run.project_b))

    def test_resumed_with_b_in_a_new_server_started_in_a_the_thread_is_governed_by_b(self):
        """A conversation started in B and saved; the first server stopped; a second started, again in A; the
        conversation resumed as the App's Continue resumes it at edits: the thread, `excludeTurns`, B as its
        folder, the level and the one trust entry for B. The resume reply is for that thread and reports B, in its
        own `cwd` and its thread's; a command runs in B; the relative write lands in B; the write in B succeeds;
        the write in A runs and is refused by the sandbox. The folder sent is the folder saved, as it always is
        from the App, so this shows the conversation continuing in B and not which of the two Codex took it from."""
        with L.Run(SCRATCH, BINARY, second_project=SECOND) as run:
            client = run.start()
            reply, turn = self.start_in(run, client, run.project_b)
            thread = reply['thread']['id']
            self.saved(client, thread, **turn)
            client.stop()
            again = run.start()
            frame, _ = self.app_frame(run.project_b)
            resumed = again.result('thread/resume', dict(frame, threadId=thread, excludeTurns=True))
            self.assertEqual(resumed['thread']['id'], thread)
            for what, folder in (('the folder', resumed['cwd']), ("the thread's folder", resumed['thread']['cwd'])):
                self.assertTrue(same_folder(folder, run.project_b),
                                'the resume reported %s %s' % (what, self.named(run, folder)))
            self.governed_by_b(run, again, thread, **turn)


TRUST_CASES = ('untrusted', 'trusted')  # each the other's control; untrusted first, so a marker it shows is its own
HOOK_EVENT_NAMES = {'SessionStart': 'sessionStart', 'UserPromptSubmit': 'userPromptSubmit', 'PreToolUse': 'preToolUse',
                    'PostToolUse': 'postToolUse', 'Stop': 'stop'}  # the protocol's spelling of each hook event


def shown(observed):
    """Every observation of a test, for its failure message."""
    return pprint.pformat(observed, width=110)


class TrustedProject(Probing):
    """What a `trusted` entry for a project turns on at the pinned Codex, beyond its `AGENTS.md` and its writable
    root (the folder-per-conversation rows), and what the project's own files can do that the App's level does not
    override. The project is A, the folder the app server is started in; each start sends what the App sends for a
    conversation there (`frame`): the folder, the level's approval, reviewer, mode name and workspace options, and
    the one trust entry, `untrusted` or `trusted`; each turn sends the level. The project's files are invented by
    the fixture (`Run(trusted_project=True)`), and every program they name is the fixture's marker command.

    Each test's docstring names its own controls. Most observe both entries, each the other's control, and where
    an outcome is an absence, some add a positive control: the same declaration in the person's own settings (the
    Codex home). The three tests that try what the App's start can keep off while trusted, and the resume test,
    compare cases within one trust state instead. Every observation of a test is recorded and printed to standard
    error under `OBSERVED` (`report`) before anything is asserted, and a failure states all of them. A test's
    assertion is the one place its expectation lives. Where how often something ran, or the order of
    notifications, is not the fact, the count is recorded and printed, and only whether it is zero, or whether it
    rose, is asserted."""

    EDITS = app_level('edits')
    SUPERVISED_ROW = app_level('supervised')
    FULL_ROW = app_level('full')

    def frame(self, run, trust, level=None):
        """What the App sends on `thread/start` for a conversation in A at `level` (edits unless named), with the
        one trust entry `trust` for A's root (no entry when None), and what it sends on each turn."""
        start, turn = level_settings(level or self.EDITS)
        frame = dict(start, cwd=str(run.project), model=L.MODEL, modelProvider='openai')
        config = dict(start.get('config') or {})
        if trust is not None:
            config['projects'] = {os.path.realpath(str(run.project)): {'trust_level': trust}}
        if config:
            frame['config'] = config
        return frame, turn

    def start(self, run, client, trust, level=None, config=None, drop=(), **extra):
        """(the start reply or None, its error or None, the turn's level). An error is recorded, not raised.
        `config` adds keys to the frame's `config` beside what the App sends; `drop` removes frame fields."""
        frame, turn = self.frame(run, trust, level)
        frame.update(extra)
        if config:
            frame['config'] = dict(frame.get('config') or {}, **config)
        for field in drop:
            frame.pop(field, None)
        reply = client.call('thread/start', frame)
        return reply.get('result'), reply.get('error'), turn

    def report(self, observed):
        """Print every observation of the test to standard error, whatever its outcome."""
        sys.stderr.write('\nOBSERVED %s:\n%s\n' % (self.id().rsplit('.', 1)[-1], shown(observed)))
        sys.stderr.flush()

    def placed(self, stub, key, names=None):
        """For the requests carrying the turn `key`: each watched marker's places, per request, keyed by the
        marker or, with `names` ({marker: name}), by its name."""
        names = names or {}
        return [{names.get(m, m): v for m, v in p.items()}
                for r, p in zip(stub.requests, stub.placements) if r['key'] == key]

    def seen(self, run, client, thread, key, **settings):
        """One fixed command's judged outcome, as (outcome, requests raised, effect: its file present or the
        network reached); an outcome the judge refuses is recorded with its reason."""
        try:
            outcome = probe(run, client, thread, key, **settings)
        except L.Refused as error:
            return ('unresolved', str(error)[:200])
        effect = outcome.reached if key == 'net' else outcome.present
        return (outcome.kind, len(outcome.requests), effect)

    def reported(self, reply):
        sandbox = reply.get('sandbox') or {}
        return (reply.get('approvalPolicy'), reply.get('approvalsReviewer'), sandbox.get('type'),
                sandbox.get('networkAccess'))

    def keyed_turn(self, run, client, thread, key, **turn):
        """A turn with no command, keyed so that the stubs' requests for it can be found."""
        _, done = client.turn(thread, 'LEVEL[%s] go' % key, **turn)
        return done and done['turn']['status']

    def carried(self, stub, key, marker):
        return any(marker in r['markers'] for r in stub.requests if r['key'] == key)

    def sources(self, run, reply):
        """The instruction files a start or resume reply names: the project's own `AGENTS.md` by that name when
        the path is that file, any other path as it is."""
        own = {os.path.realpath(str(run.project / 'AGENTS.md')): "the project's AGENTS.md"}
        return sorted(own.get(os.path.realpath(p), p) for p in (reply or {}).get('instructionSources') or [])

    def shapes(self, placements):
        """The distinct shapes of the turn's requests (`placed`), each as {marker: (times in message text, the
        roles of the messages holding it, times anywhere else in the body)}, with 'order' for two markers each in
        one input message: 'same entry', or which comes first. The entries' indices are left out, so that what is
        asserted is the role and the order."""
        def index(where):
            return int(where[len('input['):where.index(']')]) if where.startswith('input[') else None
        found = []
        for placement in placements:
            shape = {m: (v['count'], [w.split(':', 1)[1] if ':' in w else w for w in v['where']], v['elsewhere'])
                     for m, v in sorted(placement.items())}
            names = sorted(placement)
            if len(names) == 2 and all(len(placement[m]['where']) == 1 for m in names):
                first, second = (index(placement[m]['where'][0]) for m in names)
                if None not in (first, second):
                    shape['order'] = ('same entry' if first == second else
                                      '%s first' % names[0] if first < second else '%s first' % names[1])
            if shape not in found:
                found.append(shape)
        return found

    # ----- a: the project layer -----

    def mark_text(self, run):
        """The trust mark Codex writes for A into the home's settings."""
        return '[projects."%s"]\ntrust_level = "trusted"\n' % os.path.realpath(str(run.project))

    def settings_state(self, run):
        """The home's `config.toml`: 'absent', 'the mark for A' (exactly `mark_text`), or its text."""
        path = run.home / 'config.toml'
        if not path.exists():
            return 'absent'
        text = path.read_text()
        return 'the mark for A' if text == self.mark_text(run) else 'other: %r' % text[:300]

    # The keys the project's settings in this row supply that the public source's denylist names.
    SUPPLIED_STRIPPED = ('model_provider', 'model_providers', 'notify', 'openai_base_url')

    def test_a_project_layer_loads_with_a_trusted_mark_or_entry_and_with_no_entry_but_not_with_an_untrusted_entry(self):
        """The project's `.codex/config.toml` names developer instructions (a marker line), approval, sandbox,
        network, reviewer, another provider and model, the built-in provider's address and a notify program. Each
        case is a fresh run, with the home's settings either holding Codex's own trust mark for A ('marked') or
        absent ('not marked'), and the settings' state asserted before the start. `config/read` with layers for the
        project (as the App reads it), before any start: when marked, one project layer, enabled, with the keys
        approval, reviewer, developer instructions, model, sandbox mode and workspace options; the marker as the
        effective developer instructions; the project's approval (`never`), sandbox (full access), reviewer
        (automatic) and model as effective values and the built-in provider as the provider; and none of the four
        keys this file supplies that the public source's denylist names (provider, providers, notify, the built-in
        provider's address). When not marked: the same keys in one layer, disabled with a reason, and the marker not
        effective. Then a start at the App's edits level with no entry, a `trusted` entry or an `untrusted` entry:
        whether the turn's requests carry the marker, and the settings after it. Marked: the marker is carried with
        no entry and with `trusted`, not with `untrusted`, and the settings stay the mark. Not marked: with no
        entry, the marker is carried and Codex writes the trust mark for A into the settings; with `trusted`, the
        marker is carried and the settings stay absent; with `untrusted`, neither. Recorded, not asserted: the
        wording of the reason given for the disabled layer. The controls: marked against not marked, and each entry
        against the others."""
        observed = {}
        for marked in (True, False):
            name = 'marked' if marked else 'not marked'
            for entry in (None, 'trusted', 'untrusted'):
                with L.Run(SCRATCH, BINARY, trusted_project=True) as run:
                    marker = run.trust_markers['project']
                    run.stub.watched = (marker,)
                    run.write_trust_file('.codex/config.toml', run.developer_toml() + run.policy_toml() +
                                         run.provider_toml() + run.notify_toml())
                    if marked:
                        run.write_home_file('config.toml', self.mark_text(run))
                    client = run.start()
                    if entry is None:
                        read = client.call('config/read', {'cwd': str(run.project), 'includeLayers': True})
                        if 'error' in read:
                            observed[name + ': config/read'] = 'error: %s' % json.dumps(read['error'])[:300]
                        else:
                            result = read['result']
                            layers = [layer for layer in result.get('layers') or []
                                      if (layer.get('name') or {}).get('type') == 'project']
                            keys = sorted({k for layer in layers for k in (layer.get('config') or {})})
                            effective = result.get('config') or {}
                            observed[name + ': config/read'] = {
                                'project layers': len(layers),
                                'disabled': [bool(layer.get('disabledReason')) for layer in layers],
                                'reasons': [(layer.get('disabledReason') or '')[:240] for layer in layers],
                                'keys': keys,
                                'supplied stripped keys present': sorted(set(keys) & set(self.SUPPLIED_STRIPPED)),
                                'marker effective': effective.get('developer_instructions') == marker,
                                'effective': {k: effective.get(k) for k in (
                                    'approval_policy', 'sandbox_mode', 'approvals_reviewer', 'model_provider', 'model')}}
                    case = '%s: entry %s' % (name, entry or 'none')
                    before = self.settings_state(run)
                    reply, error, turn = self.start(run, client, entry)
                    if error:
                        observed[case] = {'settings before': before, 'start error': json.dumps(error)[:300]}
                        continue
                    key = 'layers_%s_%s' % ('m' if marked else 'u', entry or 'none')
                    status = self.keyed_turn(run, client, reply['thread']['id'], key, **turn)
                    client.stop()
                    observed[case] = {'settings before': before, 'turn': status,
                                      'marker carried': self.carried(run.stub, key, marker),
                                      'settings after': self.settings_state(run)}
        self.report(observed)
        self.assertEqual(set(self.SUPPLIED_STRIPPED) - set(L.PROJECT_DENYLIST_READ), set())
        keys = ['approval_policy', 'approvals_reviewer', 'developer_instructions', 'model', 'sandbox_mode',
                'sandbox_workspace_write']
        reads = {k: observed.get(k) for k in ('marked: config/read', 'not marked: config/read')}
        reads = {k: (v if not isinstance(v, dict) else
                     {'project layers': v['project layers'], 'disabled': v['disabled'],
                      'reason given': [bool(r) for r in v['reasons']], 'keys': v['keys'],
                      'marker effective': v['marker effective'],
                      'supplied stripped keys present': v['supplied stripped keys present'],
                      'effective': v['effective'] if k.startswith('marked') else '-'})
                 for k, v in reads.items()}
        cases = {k: v for k, v in observed.items() if 'entry' in k}
        mark, absent = 'the mark for A', 'absent'
        self.assertEqual((reads, cases), (
            {'marked: config/read': {'project layers': 1, 'disabled': [False], 'reason given': [False], 'keys': keys,
                                     'marker effective': True, 'supplied stripped keys present': [],
                                     'effective': {'approval_policy': 'never', 'sandbox_mode': 'danger-full-access',
                                                   'approvals_reviewer': 'auto_review', 'model_provider': 'openai',
                                                   'model': L.OTHER_MODEL}},
             'not marked: config/read': {'project layers': 1, 'disabled': [True], 'reason given': [True],
                                         'keys': keys, 'marker effective': False,
                                         'supplied stripped keys present': [], 'effective': '-'}},
            {'marked: entry none': {'settings before': mark, 'turn': 'completed', 'marker carried': True,
                                    'settings after': mark},
             'marked: entry trusted': {'settings before': mark, 'turn': 'completed', 'marker carried': True,
                                       'settings after': mark},
             'marked: entry untrusted': {'settings before': mark, 'turn': 'completed', 'marker carried': False,
                                         'settings after': mark},
             'not marked: entry none': {'settings before': absent, 'turn': 'completed', 'marker carried': True,
                                        'settings after': mark},
             'not marked: entry trusted': {'settings before': absent, 'turn': 'completed', 'marker carried': True,
                                           'settings after': absent},
             'not marked: entry untrusted': {'settings before': absent, 'turn': 'completed', 'marker carried': False,
                                             'settings after': absent}}),
            'observed:\n%s' % shown(observed))

    # ----- b: hooks -----

    def hooks_case(self, run, trust):
        """A fresh server; a start at edits with the entry `trust`; `hooks/list` for the thread; one turn with a
        command (so that the tool events fire); two seconds; then the server stopped and its output drained, and
        only then what ran: per event, how often its marker ran and whether a `hook/started` named it. Returns
        (observations, the (event, key, hash) of each hook listed, as Codex reported them)."""
        run.clear_markers()
        client = run.start()
        reply, error, turn = self.start(run, client, trust)
        if error:
            client.stop()
            return {'start error': json.dumps(error)[:300]}, []
        thread = reply['thread']['id']
        listed = client.call('hooks/list', {'threadId': thread})
        hooks = [] if 'error' in listed else [h for entry in listed['result'].get('data') or []
                                             for h in entry.get('hooks') or []]
        warnings = [] if 'error' in listed else [w for entry in listed['result'].get('data') or []
                                                 for w in (entry.get('warnings') or []) + (entry.get('errors') or [])]
        command = self.seen(run, client, thread, 'in', **turn)
        time.sleep(2)  # a hook ending after the turn
        client.stop()  # drained: every notification the server wrote has been read
        started = sorted({(n['params']['run'].get('eventName'), n['params']['run'].get('source'),
                           n['params']['run'].get('scope')) for n in client.notes_for('hook/started')})
        named = {event for event, _, _ in started}
        observations = {
            'listed': sorted((h.get('eventName'), h.get('source'), h.get('trustStatus'), h.get('enabled'))
                             for h in hooks),
            'list error': listed.get('error') and json.dumps(listed['error'])[:200],
            'list warnings': [str(w)[:200] for w in warnings],
            'command': command, 'hook/started': started,
            'per event (marker runs, hook/started)': {
                event: (run.marker_runs(name), HOOK_EVENT_NAMES[event] in named)
                for event, name in L.HOOK_MARKERS.items()}}
        return observations, [(h.get('eventName'), h['key'], h['currentHash']) for h in hooks
                              if h.get('key') and h.get('currentHash')]

    def per_event(self, case):
        """Per event: (its marker ran, a `hook/started` named it)."""
        if not isinstance(case, dict) or 'start error' in case:
            return case
        return {e: (runs > 0, named) for e, (runs, named) in case['per event (marker runs, hook/started)'].items()}

    def test_a_projects_own_hooks_do_not_run_and_are_listed_untrusted(self):
        """A command hook for each of five events (session start, user prompt submitted, before and after a tool
        call, stop), declared in the project's `.codex/hooks.json`. The App never sends `bypass_hook_trust` or
        `hooks.state`, and neither is sent here. Each case: one turn whose command (the project write) succeeds;
        the server then stopped and drained. With either entry, for each of the five events, its marker does not
        run and no `hook/started` names it. With the `trusted` entry, `hooks/list` for the thread lists the five,
        each from the source `project`, enabled, with the trust status `untrusted`. The positive control: the
        person's own approval of each hook as Codex listed it (its key and current hash in `hooks.state` in the
        Codex home), with the `trusted` entry: for each of the five events, its marker runs and a `hook/started`
        names it, and the command succeeds."""
        with L.Run(SCRATCH, BINARY, trusted_project=True) as run:
            run.write_trust_file('.codex/hooks.json', run.hooks_json())
            observed, states = {}, {}
            for trust in TRUST_CASES:
                observed[trust], states[trust] = self.hooks_case(run, trust)
            if states['trusted']:
                run.write_home_file('config.toml', run.hook_state_toml([(k, h) for _, k, h in states['trusted']]))
                observed['control: approved by the person'], _ = self.hooks_case(run, 'trusted')
            else:
                observed['control: approved by the person'] = 'not made: no hook was listed to approve'
        self.report(observed)
        none = {e: (False, False) for e in L.HOOK_MARKERS}
        asserted = {k: v if not isinstance(v, dict) or 'start error' in v else
                    {'command': v['command'], 'per event': self.per_event(v)} for k, v in observed.items()}
        asserted['trusted listing'] = observed['trusted'].get('listed')
        self.assertEqual(asserted, {
            'untrusted': {'command': (SUCCEEDED, 0, True), 'per event': none},
            'trusted': {'command': (SUCCEEDED, 0, True), 'per event': none},
            'trusted listing': sorted((HOOK_EVENT_NAMES[e], 'project', 'untrusted', True) for e in L.HOOK_MARKERS),
            'control: approved by the person': {'command': (SUCCEEDED, 0, True),
                                                'per event': {e: (True, True) for e in L.HOOK_MARKERS}}},
            'observed:\n%s' % shown(observed))

    def test_a_projects_own_hook_state_does_not_approve_its_hooks(self):
        """The same five hooks; with the `trusted` entry, `hooks/list` gives each hook's key and current hash, and
        the test requires one for each of the five events. The project's own `.codex/config.toml` is then written to
        approve each (`hooks.state.<key>.trusted_hash`, the form the person's approval takes), and a fresh server
        started: with the `trusted` entry each is still listed `untrusted`, and for each event its marker does not
        run and no `hook/started` names it, while the turn's command succeeds. The control, in the same test: the
        project's file emptied and the same approvals written into the person's own settings, a fresh server, the
        `trusted` entry: for each of the five events, its marker runs and a `hook/started` names it."""
        with L.Run(SCRATCH, BINARY, trusted_project=True) as run:
            run.write_trust_file('.codex/hooks.json', run.hooks_json())
            observed = {}
            observed['before'], states = self.hooks_case(run, 'trusted')
            observed['events with a key and hash'] = sorted(e for e, _, _ in states)
            if len(states) == len(L.HOOK_MARKERS):
                approval = run.hook_state_toml([(k, h) for _, k, h in states])
                run.write_trust_file('.codex/config.toml', approval)
                observed['approved in the project'], _ = self.hooks_case(run, 'trusted')
                run.write_trust_file('.codex/config.toml', '')
                run.write_home_file('config.toml', approval)
                observed['the same approval in the home'], _ = self.hooks_case(run, 'trusted')
        self.report(observed)
        self.assertEqual(observed['events with a key and hash'], sorted(HOOK_EVENT_NAMES.values()),
                         'INCONCLUSIVE: not every hook was listed with a key and hash to approve:\n%s'
                         % shown(observed))
        project, home = observed['approved in the project'], observed['the same approval in the home']
        self.assertEqual(
            {'approved in the project': {'listed': project.get('listed'), 'command': project.get('command'),
                                         'per event': self.per_event(project)},
             'the same approval in the home': {'command': home.get('command'), 'per event': self.per_event(home)}},
            {'approved in the project': {
                'listed': sorted((HOOK_EVENT_NAMES[e], 'project', 'untrusted', True) for e in L.HOOK_MARKERS),
                'command': (SUCCEEDED, 0, True), 'per event': {e: (False, False) for e in L.HOOK_MARKERS}},
             'the same approval in the home': {'command': (SUCCEEDED, 0, True),
                                               'per event': {e: (True, True) for e in L.HOOK_MARKERS}}},
            'observed:\n%s' % shown(observed))

    # ----- c: MCP servers -----

    MCP_NAMES = (L.MCP_STDIO, L.MCP_HTTP, L.MCP_PERSON, L.MCP_HELPER)

    def mcp_case(self, run, trust, config=None, markers=('mcp-stdio',), outside=False):
        """A fresh server, initialised, and two seconds; a start at edits with the entry `trust` (and `config`
        added to the App's); three seconds; one turn; two seconds; with `outside`, a plain write outside the project
        on the same thread; `mcpServerStatus/list` for the thread; one second; then the server stopped and drained.
        "(marker runs, connections)" is sampled before the thread starts, at start (after the three seconds), by the
        turn, after the listing and after the stop: the first of `markers`' runs and the connections the second
        listener accepted (each an accepted socket, whatever it carried). `markers` gives each named marker's runs
        by the turn, just before the listing is asked for, as it returns, a second after it, and after the stop.
        Startup notifications are the set of (server, state) pairs, unordered."""
        run.clear_markers()
        connections = run.other.connections

        def sample():
            return (run.marker_runs(markers[0]), run.other.connections - connections)
        client = run.start()
        time.sleep(2)
        before = sample()
        reply, error, turn = self.start(run, client, trust, config=config)
        if error:
            client.stop()
            return {'before the thread starts': before, 'start error': json.dumps(error)[:300]}
        thread = reply['thread']['id']
        time.sleep(3)
        at_start = sample()
        key = 'mcp_%s_%d' % (trust, len(run.stub.requests))
        status = self.keyed_turn(run, client, thread, key, **turn)
        time.sleep(2)
        by_turn = sample()
        by_marker = {name: run.marker_runs(name) for name in markers}
        offered = sorted({t for r in run.stub.requests if r['key'] == key for t in r['tools']
                          if any(name in str(t) for name in self.MCP_NAMES)})
        startup = sorted({(n['params'].get('name'), n['params'].get('status'))
                          for n in client.notes_for('mcpServer/startupStatus/updated')
                          if n['params'].get('name') in self.MCP_NAMES})
        case = {'turn': status}
        if outside:
            case['plain write outside'] = self.seen(run, client, thread, 'out', **turn)
        before_listing = {name: run.marker_runs(name) for name in markers}
        listing = client.call('mcpServerStatus/list', {'threadId': thread})
        right_after_listing = {name: run.marker_runs(name) for name in markers}
        listed = (json.dumps(listing['error'])[:200] if 'error' in listing else
                  sorted(s.get('name') for s in listing['result'].get('data') or []
                         if s.get('name') in self.MCP_NAMES))
        time.sleep(1)
        after_listing = sample()
        markers_after_listing = {name: run.marker_runs(name) for name in markers}
        client.stop()
        case.update({'before the thread starts': before, 'at start': at_start, 'by the turn': by_turn,
                     'after the listing': after_listing, 'after the stop': sample(), 'markers by the turn': by_marker,
                     'markers before the listing': before_listing,
                     'markers as the listing returns': right_after_listing,
                     'markers a second after the listing': markers_after_listing,
                     'markers after the stop': {name: run.marker_runs(name) for name in markers},
                     'tools offered': offered, 'startup notifications': startup, 'listed': listed})
        return case

    def test_a_trusted_projects_own_mcp_servers_are_started_and_an_untrusted_ones_are_not(self):
        """Two MCP servers in the project's `.codex/config.toml`: one whose command is the fixture's marker command
        (writing its marker under `outside`, outside the project), one at the second listener's loopback address.
        Each case on a fresh server at the App's edits level (`mcp_case`, with a plain write outside the project
        on the same thread). With the `trusted` entry: nothing has started before the thread starts; at thread
        start the marker has run and the second listener has accepted a connection, and by the end of the first
        turn both counts have risen; the startup notifications are, as a set, `starting` and `failed` for each of
        the two (the fixture's programs are not MCP servers); none of their tools is offered;
        `mcpServerStatus/list` for the thread lists neither; and on that thread a plain write outside the project
        by a command is refused by the sandbox. With the `untrusted` entry: no marker run and no connection at any
        sample through the stop, no notification, nothing listed, and the same refusal. Recorded, not asserted:
        the counts themselves. The positive control: the same two servers in the person's own settings, with the
        `untrusted` entry, are started and rise in the same way, and the listing names both."""
        observed = {}
        with L.Run(SCRATCH, BINARY, trusted_project=True) as run:
            run.write_trust_file('.codex/config.toml', run.mcp_toml())
            for trust in TRUST_CASES:
                observed[trust] = self.mcp_case(run, trust, outside=True)
        with L.Run(SCRATCH, BINARY, trusted_project=True) as run:
            run.write_home_file('config.toml', run.mcp_toml())
            observed["control: in the person's settings"] = self.mcp_case(run, 'untrusted', outside=True)
        self.report(observed)

        def started(case):
            if not isinstance(case, dict) or 'start error' in case:
                return case
            out = {'turn': case['turn'], 'before the thread starts': case['before the thread starts'],
                   'at start': tuple(n > 0 for n in case['at start']),
                   'risen by the turn': tuple(b > a for a, b in zip(case['at start'], case['by the turn'])),
                   'tools offered': case['tools offered'], 'startup notifications': case['startup notifications'],
                   'listed': case['listed'], 'plain write outside': case['plain write outside']}
            if not any(case['at start']):  # an absence is asserted through the listing and the stop
                out['after the listing'], out['after the stop'] = case['after the listing'], case['after the stop']
            return out
        both = [(L.MCP_HTTP, 'failed'), (L.MCP_HTTP, 'starting'), (L.MCP_STDIO, 'failed'), (L.MCP_STDIO, 'starting')]
        running = {'turn': 'completed', 'before the thread starts': (0, 0), 'at start': (True, True),
                   'risen by the turn': (True, True), 'tools offered': [], 'startup notifications': both,
                   'plain write outside': (SANDBOX_REFUSED, 0, False)}
        self.assertEqual({k: started(v) for k, v in observed.items()}, {
            'untrusted': {'turn': 'completed', 'before the thread starts': (0, 0), 'at start': (False, False),
                          'risen by the turn': (False, False), 'tools offered': [], 'startup notifications': [],
                          'listed': [], 'plain write outside': (SANDBOX_REFUSED, 0, False),
                          'after the listing': (0, 0), 'after the stop': (0, 0)},
            'trusted': dict(running, listed=[]),
            "control: in the person's settings": dict(running, listed=[L.MCP_HTTP, L.MCP_STDIO])},
            'observed:\n%s' % shown(observed))

    # ----- d: notify -----

    def test_a_projects_own_notify_program_does_not_run(self):
        """`notify` in the project's `.codex/config.toml` names the fixture's marker command. With either entry, a
        turn completes and the marker has not run when read three seconds after it, with the server stopped and
        drained. The positive control: the same `notify` in the person's own settings, with the `untrusted` entry:
        the marker runs."""
        observed = {}

        def case(run, trust):
            run.clear_markers()
            client = run.start()
            reply, error, turn = self.start(run, client, trust)
            if error:
                client.stop()
                return {'start error': json.dumps(error)[:300]}
            status = self.keyed_turn(run, client, reply['thread']['id'], 'notify_%s' % trust, **turn)
            time.sleep(3)
            client.stop()
            return {'turn': status, 'ran': run.marker_runs('notify')}
        with L.Run(SCRATCH, BINARY, trusted_project=True) as run:
            run.write_trust_file('.codex/config.toml', run.notify_toml())
            for trust in TRUST_CASES:
                observed[trust] = case(run, trust)
        with L.Run(SCRATCH, BINARY, trusted_project=True) as run:
            run.write_home_file('config.toml', run.notify_toml())
            control = observed['control: in the person\'s settings'] = case(run, 'untrusted')
        self.report(observed)
        self.assertEqual(({t: observed[t] for t in TRUST_CASES}, isinstance(control, dict) and control['ran'] > 0),
                         ({t: {'turn': 'completed', 'ran': 0} for t in TRUST_CASES}, True),
                         'observed:\n%s' % shown(observed))

    # ----- e: approval, sandbox, network and review routing -----

    def test_a_projects_approval_sandbox_network_and_reviewer_do_not_move_the_apps_level(self):
        """The project's `.codex/config.toml` names approval `never`, full access, network on and the automatic
        reviewer. At the App's edits level, with either entry: the start reply reports `on-request`, reviewer
        `user`, workspace write and network off; a write outside the project runs and is refused by the sandbox;
        the network probe runs and is refused; an escalation raises a request for that call, which the client
        declines. At the App's supervised level, with either entry: the reply reports `untrusted`, reviewer `user`
        and read-only, and the project write is put to the client first and declined. The controls: each entry
        against the other, and on each thread the refused and the asked operations."""
        observed = {}
        with L.Run(SCRATCH, BINARY, trusted_project=True) as run:
            run.write_trust_file('.codex/config.toml', run.policy_toml())
            client = run.start()
            for trust in TRUST_CASES:
                reply, error, turn = self.start(run, client, trust)
                if error:
                    observed['edits, ' + trust] = 'start error: %s' % json.dumps(error)[:300]
                else:
                    thread = reply['thread']['id']
                    observed['edits, ' + trust] = {
                        'reported': self.reported(reply), 'outside': self.seen(run, client, thread, 'out', **turn),
                        'network': self.seen(run, client, thread, 'net', **turn),
                        'escalation': self.seen(run, client, thread, 'out2', escalate=True, **turn)}
                reply, error, turn = self.start(run, client, trust, level=self.SUPERVISED_ROW)
                if error:
                    observed['supervised, ' + trust] = 'start error: %s' % json.dumps(error)[:300]
                else:
                    observed['supervised, ' + trust] = {
                        'reported': self.reported(reply),
                        'project write': self.seen(run, client, reply['thread']['id'], 'in', **turn)}
        self.report(observed)
        edits = {'reported': ('on-request', 'user', 'workspaceWrite', False),
                 'outside': (SANDBOX_REFUSED, 0, False), 'network': (SANDBOX_REFUSED, 0, False),
                 'escalation': (DECLINED, 1, False)}
        supervised = {'reported': ('untrusted', 'user', 'readOnly', False), 'project write': (DECLINED, 1, False)}
        expected = {}
        for trust in TRUST_CASES:
            expected['edits, ' + trust], expected['supervised, ' + trust] = edits, supervised
        self.assertEqual(observed, expected, 'observed:\n%s' % shown(observed))

    def test_a_projects_default_permissions_do_not_move_the_apps_level(self):
        """The project's `.codex/config.toml` selects the built-in full-access permissions profile
        (`default_permissions`). At the App's edits level, with either entry: the reply reports workspace write with
        network off and no active permissions profile; a write outside the project and the network probe each run
        and are refused by the sandbox. The control: each entry against the other. No case here selects a profile,
        so this shows the App's frame kept, not what the setting does when it applies."""
        observed = {}
        with L.Run(SCRATCH, BINARY, trusted_project=True) as run:
            run.write_trust_file('.codex/config.toml', run.permissions_toml())
            client = run.start()
            for trust in TRUST_CASES:
                reply, error, turn = self.start(run, client, trust)
                if error:
                    observed[trust] = 'start error: %s' % json.dumps(error)[:300]
                    continue
                thread = reply['thread']['id']
                observed[trust] = {'reported': self.reported(reply),
                                   'profile': (reply.get('activePermissionProfile') or {}).get('id'),
                                   'outside': self.seen(run, client, thread, 'out', **turn),
                                   'network': self.seen(run, client, thread, 'net', **turn)}
        self.report(observed)
        self.assertEqual(observed, {t: {'reported': ('on-request', 'user', 'workspaceWrite', False), 'profile': None,
                                        'outside': (SANDBOX_REFUSED, 0, False), 'network': (SANDBOX_REFUSED, 0, False)}
                                    for t in TRUST_CASES}, 'observed:\n%s' % shown(observed))

    # ----- f: the model's destination -----

    def test_a_projects_provider_and_model_do_not_move_the_turn(self):
        """The project's `.codex/config.toml` names another provider (defined there, at the second listener's
        loopback address), another model, and the built-in provider's address moved to that listener. With the App's
        start (model and provider on the frame, and the process started with `model_provider="openai"` and its own
        `openai_base_url`), with either entry, each on a fresh server: the reply reports the App's model and the
        built-in provider; the turn's requests reach the stub, and each names the App's model; and, read after the
        server is stopped and drained, the second listener has accepted no connection. The control: each entry
        against the other."""
        observed = {}
        with L.Run(SCRATCH, BINARY, trusted_project=True) as run:
            run.write_trust_file('.codex/config.toml', run.provider_toml())
            run.stub.record_model = True
            for trust in TRUST_CASES:
                connections = run.other.connections
                client = run.start()
                reply, error, turn = self.start(run, client, trust)
                if error:
                    client.stop()
                    observed[trust] = 'start error: %s' % json.dumps(error)[:300]
                    continue
                key = 'provider_%s' % trust
                status = self.keyed_turn(run, client, reply['thread']['id'], key, **turn)
                client.stop()
                ours = [r for r in run.stub.requests if r['key'] == key]
                observed[trust] = {'reported': (reply.get('model'), reply.get('modelProvider')), 'turn': status,
                                   'stub requests': len(ours) > 0,
                                   'models requested': sorted({str(r.get('model')) for r in ours}),
                                   'second listener after the stop': (
                                       sum(r['key'] == key for r in run.other.requests),
                                       run.other.connections - connections)}
        self.report(observed)
        self.assertEqual(observed, {t: {'reported': (L.MODEL, 'openai'), 'turn': 'completed', 'stub requests': True,
                                        'models requested': [L.MODEL], 'second listener after the stop': (0, 0)}
                                    for t in TRUST_CASES},
                         'observed:\n%s' % shown(observed))

    def test_a_trusted_projects_settings_file_codex_cannot_load_refuses_the_start(self):
        """Two causes, each the project's whole `.codex/config.toml`, each started on a fresh server with each
        entry. A key Codex no longer supports, `experimental_thread_store_endpoint` (named here at the second
        listener's loopback address): with the `trusted` entry the start is refused, "failed to load
        configuration: `experimental_thread_store_endpoint` is no longer supported; remove it from config.toml", and
        the second listener accepts no connection. A file that is not TOML: with the `trusted` entry the start is
        refused with a message holding "failed to load configuration: Error parsing project config file ", the
        project's `.codex/config.toml`, "TOML parse error at line 1, column 6" and "key with no value, expected
        `=`". With the `untrusted` entry, each start succeeds and a turn completes. The control: each entry against
        the other."""
        observed = {}
        with L.Run(SCRATCH, BINARY, trusted_project=True) as run:
            for cause, text in (('unsupported key', run.thread_store_toml()), ('not TOML', run.malformed_toml())):
                run.write_trust_file('.codex/config.toml', text)
                for trust in TRUST_CASES:
                    connections = run.other.connections
                    client = run.start()
                    reply, error, turn = self.start(run, client, trust)
                    status = None
                    if not error:
                        status = self.keyed_turn(run, client, reply['thread']['id'], 'load_%s_%s'
                                                 % (cause.replace(' ', '-'), trust), **turn)
                    time.sleep(2)
                    client.stop()
                    message = error and str(error.get('message'))
                    observed['%s, %s' % (cause, trust)] = {
                        'start error': message, 'turn': status, 'connections': run.other.connections - connections,
                        'names the file': bool(message) and any(
                            path in message for path in (str(run.project / '.codex' / 'config.toml'),
                                                         os.path.realpath(str(run.project / '.codex' / 'config.toml'))))}
        self.report(observed)
        # The stable parts of each message: the not-TOML one also holds the run's path, checked as 'names the file'.
        stated = {'unsupported key': ('failed to load configuration: `experimental_thread_store_endpoint` is no '
                                      'longer supported; remove it from config.toml',),
                  'not TOML': ('failed to load configuration: Error parsing project config file ',
                               'TOML parse error at line 1, column 6', 'key with no value, expected `=`')}
        asserted = {}
        for case, seen in observed.items():
            message = seen['start error'] or ''
            asserted[case] = {'refused': bool(message), 'turn': seen['turn'], 'connections': seen['connections'],
                              'message': [part for part in stated[case.split(',')[0]] if part in message]}
        asserted['not TOML, trusted']['names the file'] = observed['not TOML, trusted']['names the file']
        self.assertEqual(asserted, {
            'unsupported key, untrusted': {'refused': False, 'turn': 'completed', 'connections': 0, 'message': []},
            'unsupported key, trusted': {'refused': True, 'turn': None, 'connections': 0,
                                         'message': list(stated['unsupported key'])},
            'not TOML, untrusted': {'refused': False, 'turn': 'completed', 'connections': 0, 'message': []},
            'not TOML, trusted': {'refused': True, 'turn': None, 'connections': 0,
                                  'message': list(stated['not TOML']), 'names the file': True}},
            'observed:\n%s' % shown(observed))

    # ----- g: instructions from settings -----

    def test_a_trusted_projects_developer_instructions_are_carried_and_the_apps_own_are_kept(self):
        """The project's `.codex/config.toml` sets `developer_instructions` to a marker line. Each start is the App's
        at edits, without and then with the App's own `developerInstructions` (another marker line). With the
        `trusted` entry and none from the App, the turn's requests carry the project's marker; with the App's own,
        they carry the App's and not the project's. With the `untrusted` entry, never the project's. The App's
        marker is carried whenever the App sends it. The control: each entry against the other, and each start
        with and without the App's own."""
        observed = {}
        with L.Run(SCRATCH, BINARY, trusted_project=True) as run:
            markers = run.trust_markers
            run.stub.watched = (markers['project'], markers['app'])
            run.write_trust_file('.codex/config.toml', run.developer_toml())
            client = run.start()
            for trust in TRUST_CASES:
                for app in (False, True):
                    extra = {'developerInstructions': 'Invented App instructions. %s' % markers['app']} if app else {}
                    reply, error, turn = self.start(run, client, trust, **extra)
                    case = '%s, %s' % (trust, 'with the App\'s own' if app else 'none from the App')
                    if error:
                        observed[case] = 'start error: %s' % json.dumps(error)[:300]
                        continue
                    key = 'dev_%s_%s' % (trust, app)
                    status = self.keyed_turn(run, client, reply['thread']['id'], key, **turn)
                    observed[case] = {'turn': status, 'project': self.carried(run.stub, key, markers['project']),
                                      'app': self.carried(run.stub, key, markers['app'])}
        self.report(observed)
        self.assertEqual(observed, {
            'untrusted, none from the App': {'turn': 'completed', 'project': False, 'app': False},
            "untrusted, with the App's own": {'turn': 'completed', 'project': False, 'app': True},
            'trusted, none from the App': {'turn': 'completed', 'project': True, 'app': False},
            "trusted, with the App's own": {'turn': 'completed', 'project': False, 'app': True}},
            'observed:\n%s' % shown(observed))

    # ----- h: the trust mark -----

    def test_a_trusted_entry_writes_nothing_into_the_settings(self):
        """As the trust-mark rows: at full access, in the App's layout with the home's new, empty settings, in a git
        project, each case on a fresh run. With one `trusted` entry for the project's root, the home's `config.toml`
        is still empty when read two seconds after the start. The control: with no entry, the trust mark is
        written."""
        observed = {}
        for entry in (None, 'trusted'):
            with L.Run(SCRATCH, BINARY, working_files=True, git_marker=True) as run:
                (run.project / '.git' / 'HEAD').write_text('ref: refs/heads/main\n')
                cfg = run.home / 'config.toml'
                self.assertEqual(cfg.read_bytes(), b'')
                client = run.start()
                params = dict(TrustWrite.FULL_START)
                if entry:
                    params['config'] = {'projects': {os.path.realpath(str(run.project)): {'trust_level': entry}}}
                reply = client.start_thread(**params)
                time.sleep(2)
                observed[entry or 'no entry'] = {'sandbox': reply['sandbox']['type'], 'settings': cfg.read_text(),
                                                 'mark': '[projects."%s"]\ntrust_level = "trusted"\n'
                                                         % os.path.realpath(str(run.project))}
        self.report(observed)
        none, trusted = observed['no entry'], observed['trusted']
        self.assertEqual({'no entry': (none['sandbox'], none['settings'] == none['mark']),
                          'trusted': (trusted['sandbox'], trusted['settings'])},
                         {'no entry': ('dangerFullAccess', True), 'trusted': ('dangerFullAccess', '')},
                         'observed:\n%s' % shown(observed))

    # ----- i: the project's other files and settings -----

    def test_a_trusted_projects_allow_rule_takes_a_command_out_of_the_sandbox_and_past_the_person(self):
        """An exec-policy rule in the project's `.codex/rules/invented.rules` allows `/usr/bin/touch` (by its path
        and by its name). On a fresh server for each entry, at the App's edits and supervised levels, on each
        thread a `touch` of a file outside the project and a plain write outside the project that the rule does not
        match. With the `trusted` entry: at edits, the `touch` succeeds and its file appears, with no request, while
        the plain write is refused by the sandbox; at supervised, the `touch` succeeds with no request, while the
        plain write is put to the client first and declined. With the `untrusted` entry: at edits both are refused
        by the sandbox; at supervised both are put to the client first and declined. The positive control: the
        same rule in the person's own rules (the Codex home's `rules/default.rules`), with the `untrusted` entry, at
        edits: the same `touch` succeeds, while a plain write outside the project is refused by the sandbox."""
        observed = {}
        with L.Run(SCRATCH, BINARY, trusted_project=True) as run:
            run.write_trust_file('.codex/rules/invented.rules', run.rules_text())
            for trust in TRUST_CASES:
                client = run.start()
                case = {}
                for name, level in (('edits', None), ('supervised', self.SUPERVISED_ROW)):
                    reply, error, turn = self.start(run, client, trust, level=level)
                    if error:
                        case[name] = 'start error: %s' % json.dumps(error)[:300]
                        continue
                    thread = reply['thread']['id']
                    case[name] = {'touch outside': self.seen(run, client, thread, 'touch-out', **turn),
                                  'plain write outside': self.seen(run, client, thread, 'out', **turn)}
                client.stop()
                observed[trust] = case
        with L.Run(SCRATCH, BINARY, trusted_project=True) as run:
            run.write_home_file('rules/default.rules', run.rules_text())
            client = run.start()
            reply, error, turn = self.start(run, client, 'untrusted')
            observed["control: in the person's rules"] = (
                'start error: %s' % json.dumps(error)[:300] if error else
                {'touch outside': self.seen(run, client, reply['thread']['id'], 'touch-out', **turn),
                 'plain write outside': self.seen(run, client, reply['thread']['id'], 'out', **turn)})
        self.report(observed)
        refused, declined, passed = (SANDBOX_REFUSED, 0, False), (DECLINED, 1, False), (SUCCEEDED, 0, True)
        self.assertEqual(observed, {
            'untrusted': {'edits': {'touch outside': refused, 'plain write outside': refused},
                          'supervised': {'touch outside': declined, 'plain write outside': declined}},
            'trusted': {'edits': {'touch outside': passed, 'plain write outside': refused},
                        'supervised': {'touch outside': passed, 'plain write outside': declined}},
            "control: in the person's rules": {'touch outside': passed, 'plain write outside': refused}},
            'observed:\n%s' % shown(observed))

    def shell_case(self, run, trust, config=None, level=None, commands=1):
        """A fresh server; a start at `level` (full access unless named) with the entry `trust` (and `config` added
        to the App's); then `commands` commands on the thread, each printing, on a labelled line each, the
        variable the `ZDOTDIR` start-up file exports and the fixture's variable, with the `ZDOTDIR` marker's runs
        read before and after each; then the server stopped. A command's value is its `variable=` line, shown as
        'the variable set' when it is the value the settings give the variable; its `startup=` line is kept as
        'startup', and any other output lines apart."""
        run.clear_markers()
        client = run.start()
        reply, error, turn = self.start(run, client, trust, level=level or self.FULL_ROW, config=config)
        if error:
            client.stop()
            return {'start error': json.dumps(error)[:300]}
        thread = reply['thread']['id']
        each = []
        for _ in range(commands):
            before = run.marker_runs('zdotdir')
            try:
                outcome = probe(run, client, thread, 'env', **turn)
                lines = outcome.text.splitlines()
                labelled = {line.split('=', 1)[0]: line.split('=', 1)[1] for line in lines
                            if line.startswith(('startup=', 'variable='))}
                value = labelled.get('variable', 'not printed')
                command = (outcome.kind, 'the variable set' if value == run.trust_markers['project'] else value)
                startup = labelled.get('startup', 'not printed')
                other = [line.replace(str(run.root), '<run root>') for line in lines
                         if not line.startswith(('startup=', 'variable='))]
            except L.Refused as refused:
                command, startup, other = ('unresolved', str(refused)[:200]), None, []
            each.append({'command': command, 'startup': startup, 'other output lines': other,
                         'zdotdir before and after': (before, run.marker_runs('zdotdir'))})
        time.sleep(1)
        client.stop()
        return {'command': each[0]['command'], 'commands': each, 'zdotdir': run.marker_runs('zdotdir'),
                'bash-env': run.marker_runs('bash-env')}

    def shell_seen(self, case):
        if not isinstance(case, dict) or 'start error' in case:
            return case
        return {'command': case['command'], 'zdotdir ran': case['zdotdir'] > 0, 'bash-env': case['bash-env']}

    def test_a_trusted_projects_shell_environment_reaches_commands_and_runs_its_zdotdir(self):
        """The project's `.codex/config.toml` sets, through `shell_environment_policy.set`, a variable of the
        fixture's own, `ZDOTDIR` (a folder whose `.zshenv` exports `LEVEL_INVENTED_STARTUP=ran` and then runs the
        marker command, writing under `outside`) and `BASH_ENV` (a file that is the marker command). At the App's
        edits and full-access levels, on a fresh server for each entry, two commands on the thread, each printing
        the start-up file's variable and the project's. With the `trusted` entry, at both levels, each command sees
        the project's variable and the start-up file's: the start-up file runs inside each command. At edits it
        runs under that command's sandbox: the marker's runs do not rise across either command, its write outside
        the project being refused there. At full access its write succeeds, and the marker's runs rise across each
        command. With the `untrusted` entry, at both levels, each command sees both variables unset and the marker
        never runs. The `BASH_ENV` marker never runs (the commands' shell is zsh). Recorded, not asserted: the
        marker's counts and each command's other output lines (at edits, the start-up file's refused write). The
        positive control: the same policy in the person's own settings, with the `untrusted` entry, at full access:
        each command sees both variables and the marker's runs rise across each."""
        observed = {}
        for level_name, level in (('edits', self.EDITS), ('full access', self.FULL_ROW)):
            with L.Run(SCRATCH, BINARY, trusted_project=True) as run:
                run.write_trust_file('.codex/config.toml', run.shell_env_toml())
                for trust in TRUST_CASES:
                    observed['%s, %s' % (trust, level_name)] = self.shell_case(run, trust, level=level, commands=2)
        with L.Run(SCRATCH, BINARY, trusted_project=True) as run:
            run.write_home_file('config.toml', run.shell_env_toml())
            observed["control: in the person's settings, full access"] = self.shell_case(
                run, 'untrusted', level=self.FULL_ROW, commands=2)
        self.report(observed)

        def seen(name, case):
            if not isinstance(case, dict) or 'start error' in case:
                return case
            out = {'commands': [c['command'] for c in case['commands']],
                   'startup': [c['startup'] for c in case['commands']], 'bash-env': case['bash-env']}
            if name.startswith('untrusted'):
                out['zdotdir'] = case['zdotdir']
            else:
                out['zdotdir risen across each command'] = [a > b for b, a in
                                                            (c['zdotdir before and after'] for c in case['commands'])]
            return out
        variable, unset = (SUCCEEDED, 'the variable set'), (SUCCEEDED, 'unset')
        seen_both = {'commands': [variable, variable], 'startup': ['ran', 'ran'], 'bash-env': 0}
        unseen = {'commands': [unset, unset], 'startup': ['unset', 'unset'], 'bash-env': 0, 'zdotdir': 0}
        rising = dict(seen_both, **{'zdotdir risen across each command': [True, True]})
        self.assertEqual({k: seen(k, v) for k, v in observed.items()}, {
            'untrusted, edits': unseen,
            'trusted, edits': dict(seen_both, **{'zdotdir risen across each command': [False, False]}),
            'untrusted, full access': unseen,
            'trusted, full access': rising,
            "control: in the person's settings, full access": rising},
            'observed:\n%s' % shown(observed))

    # ----- withholding while trusted: what the App's start can keep off -----

    def test_with_a_trusted_entry_enabled_false_on_the_start_keeps_each_named_project_mcp_server_off(self):
        """The person's own settings name a server with the same name as the project's stdio server (its own marker
        command) and one of their own. Three cases, all with the `trusted` entry and the App's own start at edits,
        each on a fresh server (`mcp_case`); the controls are these cases against each other, within the one trust
        state. Every turn completes. The project naming no server: by the end of the turn the person's two servers
        have run, and the second listener accepts no connection through the stop. The project naming its two
        servers (as in the MCP row), no override: by the end of the turn the project's definition of the shared
        name has run and the person's has not, the person's other server has run, and the second listener has
        accepted a connection; `mcpServerStatus/list` lists the person's other server and the shared name. The
        same, with `mcp_servers.<name>.enabled = false` in the start's `config` for each server the project names:
        through the stop, neither the project's nor the person's definition of the shared name runs and the second
        listener accepts no connection; no notification names either of the project's names; the person's other
        server has run by the end of the turn; and, in this configuration, `mcpServerStatus/list` for the thread
        fails with "failed to reload config: invalid transport" naming `mcp_servers.<the project's HTTP server>`.
        Recorded, not asserted: every marker's runs just before the listing, as it returns, a second after it and
        after the stop. In one run, with the project naming both and no override, the person's own definition of
        the shared name ran once after the listing was asked for, and the person's other server once more."""
        markers = ('mcp-stdio', 'mcp-person-same', 'mcp-person-other')
        off = {'mcp_servers': {L.MCP_STDIO: {'enabled': False}, L.MCP_HTTP: {'enabled': False}}}
        observed = {}
        with L.Run(SCRATCH, BINARY, trusted_project=True) as run:
            run.write_home_file('config.toml', run.person_mcp_toml())
            run.write_trust_file('.codex/config.toml', '')
            observed['the project naming none'] = self.mcp_case(run, 'trusted', markers=markers)
            run.write_trust_file('.codex/config.toml', run.mcp_toml())
            observed['the project naming both, no override'] = self.mcp_case(run, 'trusted', markers=markers)
            observed['the project naming both, enabled = false for each'] = self.mcp_case(
                run, 'trusted', config=off, markers=markers)
        self.report(observed)

        def seen(case):
            if 'start error' in case:
                return case
            listed = case['listed']
            if isinstance(listed, str):  # the error, as its stable parts
                listed = ('error', [part for part in ('failed to reload config: invalid transport',
                                                      '`mcp_servers.%s`' % L.MCP_HTTP) if part in listed])
            out = {'turn': case['turn'],
                   'ran by the turn': {k: v > 0 for k, v in case['markers by the turn'].items()},
                   'second listener': case['by the turn'][1] > 0,
                   'names notified': sorted({name for name, _ in case['startup notifications']}),
                   'listed': listed}
            if not case['by the turn'][1]:  # an absence is asserted through the stop
                out['second listener'] = case['after the stop'][1] > 0
            return out
        observed_seen = {k: seen(v) for k, v in observed.items()}
        override = observed['the project naming both, enabled = false for each']
        if 'start error' not in override:  # the override's absences, through the stop
            observed_seen['the override through the stop'] = {
                k: override['markers after the stop'][k] > 0 for k in ('mcp-stdio', 'mcp-person-same')}
        self.assertEqual(observed_seen, {
            'the project naming none': {
                'turn': 'completed',
                'ran by the turn': {'mcp-stdio': False, 'mcp-person-same': True, 'mcp-person-other': True},
                'second listener': False, 'names notified': [L.MCP_PERSON, L.MCP_STDIO],
                'listed': [L.MCP_PERSON, L.MCP_STDIO]},
            'the project naming both, no override': {
                'turn': 'completed',
                'ran by the turn': {'mcp-stdio': True, 'mcp-person-same': False, 'mcp-person-other': True},
                'second listener': True, 'names notified': [L.MCP_HTTP, L.MCP_PERSON, L.MCP_STDIO],
                'listed': [L.MCP_PERSON, L.MCP_STDIO]},
            'the project naming both, enabled = false for each': {
                'turn': 'completed',
                'ran by the turn': {'mcp-stdio': False, 'mcp-person-same': False, 'mcp-person-other': True},
                'second listener': False, 'names notified': [L.MCP_PERSON],
                'listed': ('error', ['failed to reload config: invalid transport', '`mcp_servers.%s`' % L.MCP_HTTP])},
            'the override through the stop': {'mcp-stdio': False, 'mcp-person-same': False}},
            'observed:\n%s' % shown(observed))

    def test_with_a_trusted_entry_only_an_empty_value_or_include_only_on_the_start_keeps_a_projects_shell_environment_out(self):
        """The project's policy is the one in the shell-environment row; each case with the `trusted` entry, the
        App's own start at full access, one command, on a fresh server; the override in the start's
        `config.shell_environment_policy`. The controls are these cases against each other, within the one trust
        state. No override: the command sees the project's variable and the `ZDOTDIR` marker runs. Of the forms
        exercised, two keep it out. Each key the project sets, given an empty value: the command sees the variable
        empty, not unset, and the marker does not run. `include_only` listing the names of the environment Codex is
        given: the variable is unset and the marker does not run. Three do not: `inherit = "none"`, `exclude` of
        each key, and the whole table sent again with an empty `set`, after each of which the command still sees the
        project's variable and the marker still runs."""
        observed = {}
        with L.Run(SCRATCH, BINARY, trusted_project=True) as run:
            run.write_trust_file('.codex/config.toml', run.shell_env_toml())
            names = (L.TRUST_ENV, 'ZDOTDIR', 'BASH_ENV')
            cases = {'no override': None,
                     'each key set empty': {'set': {name: '' for name in names}},
                     'include_only the environment Codex is given': {'include_only': sorted(run.environment())},
                     'inherit none': {'inherit': 'none'},
                     'exclude each key': {'exclude': list(names)},
                     'the whole table, with an empty set': {'inherit': 'all', 'set': {}}}
            for name, policy in cases.items():
                observed[name] = self.shell_case(
                    run, 'trusted', config=policy and {'shell_environment_policy': policy})
        self.report(observed)
        still = {'command': (SUCCEEDED, 'the variable set'), 'zdotdir ran': True, 'bash-env': 0}
        self.assertEqual({k: self.shell_seen(v) for k, v in observed.items()}, {
            'no override': still,
            'each key set empty': {'command': (SUCCEEDED, ''), 'zdotdir ran': False, 'bash-env': 0},
            'include_only the environment Codex is given': {'command': (SUCCEEDED, 'unset'), 'zdotdir ran': False,
                                                            'bash-env': 0},
            'inherit none': still, 'exclude each key': still, 'the whole table, with an empty set': still},
            'observed:\n%s' % shown(observed))

    def profile_case(self, run, client, profile, filesystem=None):
        """The `trusted` entry with, instead of the mode name and workspace options, a permissions profile sent in
        the start's `config` (`extends = ":workspace"`, and `filesystem` when given) and named by `permissions` on
        the start and on each turn; then the reply's level and profile, and five operations on the thread."""
        frame, _ = self.frame(run, 'trusted')
        frame.pop('sandbox')
        definition = {'extends': ':workspace'}
        if filesystem:
            definition['filesystem'] = filesystem
        frame['config'] = {'projects': frame['config']['projects'], 'permissions': {profile: definition}}
        frame['permissions'] = profile
        started = client.call('thread/start', frame)
        turn = {'approvalPolicy': 'on-request', 'approvalsReviewer': 'user', 'permissions': profile}
        if 'error' in started:
            return 'start error: %s' % json.dumps(started['error'])[:400]
        reply, thread = started['result'], started['result']['thread']['id']
        return {'reported': self.reported(reply), 'profile': reply.get('activePermissionProfile'),
                'touch outside': self.seen(run, client, thread, 'touch-out', **turn),
                'project write': self.seen(run, client, thread, 'in', **turn),
                'plain write outside': self.seen(run, client, thread, 'out', **turn),
                'escalation': self.seen(run, client, thread, 'out2', escalate=True, **turn)}

    def test_with_a_trusted_entry_a_profile_denying_a_read_keeps_an_allow_rules_command_in_the_sandbox(self):
        """The project's rule allows `touch` (as in the rules row); every case has the `trusted` entry, on one
        server, so the controls are these cases against each other. The App's own start at edits: `touch` outside
        the project succeeds with no request. A permissions profile in place of the mode name and workspace options
        (`profile_case`), `extends = ":workspace"` with one invented folder under `outside` denied for reading: the
        reply reports `on-request`, reviewer `user`, workspace write and network off, and the profile as active; the
        allowed `touch` outside the project runs and is refused by the sandbox; a plain write outside is refused by
        the sandbox; the project write succeeds; an escalation raises a request for that call, which the client
        declines. The matched control: the same profile without the denied read: the same reply and the same
        outcomes, except that the allowed `touch` outside the project succeeds with no request."""
        observed = {}
        with L.Run(SCRATCH, BINARY, trusted_project=True) as run:
            run.write_trust_file('.codex/rules/invented.rules', run.rules_text())
            client = run.start()
            reply, error, turn = self.start(run, client, 'trusted')
            observed["control: the App's own start"] = (
                'start error: %s' % json.dumps(error)[:300] if error else
                {'touch outside': self.seen(run, client, reply['thread']['id'], 'touch-out', **turn)})
            observed['the profile with the denied read'] = self.profile_case(
                run, client, 'level_invented_edits', filesystem={str(run.denied_read_folder()): 'deny'})
            observed['the same profile without it'] = self.profile_case(run, client, 'level_invented_edits_open')
        self.report(observed)

        def expected(profile, touch):
            return {'reported': ('on-request', 'user', 'workspaceWrite', False),
                    'profile': {'id': profile, 'extends': ':workspace'}, 'touch outside': touch,
                    'project write': (SUCCEEDED, 0, True), 'plain write outside': (SANDBOX_REFUSED, 0, False),
                    'escalation': (DECLINED, 1, False)}
        self.assertEqual(observed, {
            "control: the App's own start": {'touch outside': (SUCCEEDED, 0, True)},
            'the profile with the denied read': expected('level_invented_edits', (SANDBOX_REFUSED, 0, False)),
            'the same profile without it': expected('level_invented_edits_open', (SUCCEEDED, 0, True))},
            'observed:\n%s' % shown(observed))

    # ----- the other route: an untrusted entry, and the App hands over the instructions -----

    def test_with_an_untrusted_entry_agents_md_text_handed_over_in_developer_instructions_reaches_the_model(self):
        """The project's own `AGENTS.md` carries a marker line; the App's own developer instructions carry another.
        Where each marker sits is read from the text of the request's messages (`ScriptedStub.placements`): the
        roles of the messages holding it, how many times, and how many more times it appears anywhere else in the
        request. With the `trusted` entry and the App's own instructions (Codex loads the file), the start names
        the project's `AGENTS.md` by its full path and no other file, and the turn carries both markers, each once
        and nowhere else: the App's in a developer message, the file's in a user message after it. With the
        `untrusted` entry and the App's instructions followed by the file's text in `developerInstructions`, the
        start names no file and the turn carries both markers, each once and nowhere else, in the same developer
        message. The control: each route against the other."""
        observed = {}
        with L.Run(SCRATCH, BINARY, trusted_project=True) as run:
            markers = run.trust_markers
            agents = run.agents_md('root')
            run.write_trust_file('AGENTS.md', agents)
            run.stub.watched = (markers['agents-root'], markers['app'])
            names = {markers['agents-root']: 'agents', markers['app']: 'app'}
            guidance = 'Invented App instructions. %s' % markers['app']
            client = run.start()
            cases = {'Codex loads it (trusted entry)': ('trusted', guidance),
                     'the App hands it over (untrusted entry, after its own)': ('untrusted', guidance + '\n\n' + agents)}
            for index, (name, (trust, instructions)) in enumerate(cases.items()):
                reply, error, turn = self.start(run, client, trust, developerInstructions=instructions)
                if error:
                    observed[name] = 'start error: %s' % json.dumps(error)[:300]
                    continue
                key = 'handover_%d' % index
                status = self.keyed_turn(run, client, reply['thread']['id'], key, **turn)
                observed[name] = {'turn': status, 'files named': self.sources(run, reply),
                                  'placements': self.placed(run.stub, key, names)}
        self.report(observed)
        self.assertEqual({k: v if not isinstance(v, dict) else
                          {'turn': v['turn'], 'files named': v['files named'], 'placed': self.shapes(v['placements'])}
                          for k, v in observed.items()}, {
            'Codex loads it (trusted entry)': {
                'turn': 'completed', 'files named': ["the project's AGENTS.md"],
                'placed': [{'agents': (1, ['user'], 0), 'app': (1, ['developer'], 0), 'order': 'app first'}]},
            'the App hands it over (untrusted entry, after its own)': {
                'turn': 'completed', 'files named': [],
                'placed': [{'agents': (1, ['developer'], 0), 'app': (1, ['developer'], 0), 'order': 'same entry'}]}},
            'observed:\n%s' % shown(observed))

    def test_a_nested_agents_md_is_named_and_carried_with_a_trusted_entry_and_neither_file_with_an_untrusted_one(self):
        """A git project with its own `AGENTS.md` and a nested `sub/AGENTS.md`, each with a marker line of its own;
        the conversation's folder is `sub`, the one trust entry is for the project's root (as the App sends it), on
        a fresh server for each entry, with the App's own start at edits. With the `trusted` entry, the start names
        both files by their full paths and no other, and the turn carries both markers; with the `untrusted` entry,
        neither file is named and neither marker is carried. The control: each entry against the other."""
        observed = {}
        with L.Run(SCRATCH, BINARY, trusted_project=True, git_marker=True) as run:
            (run.project / '.git' / 'HEAD').write_text('ref: refs/heads/main\n')
            run.write_trust_file('AGENTS.md', run.agents_md('root'))
            run.write_trust_file('sub/AGENTS.md', run.agents_md('sub'))
            markers = {k: run.trust_markers['agents-' + k] for k in ('root', 'sub')}
            files = {'root': os.path.realpath(str(run.project / 'AGENTS.md')),
                     'sub': os.path.realpath(str(run.subfolder() / 'AGENTS.md'))}
            run.stub.watched = tuple(markers.values())
            for trust in TRUST_CASES:
                client = run.start()
                reply, error, turn = self.start(run, client, trust, cwd=str(run.subfolder()))
                if error:
                    observed[trust] = 'start error: %s' % json.dumps(error)[:300]
                else:
                    key = 'nested_%s' % trust
                    status = self.keyed_turn(run, client, reply['thread']['id'], key, **turn)
                    sources = [os.path.realpath(p) for p in reply.get('instructionSources') or []]
                    observed[trust] = {'turn': status, 'cwd is sub': same_folder(reply.get('cwd'), run.subfolder()),
                                       'named': sorted(k for k, path in files.items() if path in sources),
                                       'other sources': sorted(p for p in sources if p not in files.values()),
                                       'carried': sorted(k for k, m in markers.items()
                                                         if self.carried(run.stub, key, m))}
                client.stop()
        self.report(observed)
        self.assertEqual(observed, {
            'trusted': {'turn': 'completed', 'cwd is sub': True, 'named': ['root', 'sub'], 'other sources': [],
                        'carried': ['root', 'sub']},
            'untrusted': {'turn': 'completed', 'cwd is sub': True, 'named': [], 'other sources': [], 'carried': []}},
            'observed:\n%s' % shown(observed))

    def test_handed_over_instructions_after_a_resume(self):
        """Two conversations started with the `untrusted` entry and the App's instructions (a marker line) followed
        by the project's `AGENTS.md` text (another), each with one turn; the server stopped; a second server
        started; each resumed as the App's Continue resumes it (the folder, the level, the one entry,
        `excludeTurns`), the first without `developerInstructions`, the second sending the same text again; one turn
        each. Both are untrusted throughout, so the controls are the first turns and the two resumes against each
        other. Every turn completes, and every turn, before and after the resume, carries both markers, each once
        and nowhere else, in the same developer message: the text is carried after a resume without being sent
        again, and sending it again does not carry it twice. Recorded, not asserted: the instruction files each
        resume reply names."""
        observed = {}
        with L.Run(SCRATCH, BINARY, trusted_project=True) as run:
            markers = run.trust_markers
            names = {markers['agents-root']: 'agents', markers['app']: 'app'}
            text = 'Invented App instructions. %s\n\n%s' % (markers['app'], run.agents_md('root'))
            run.write_trust_file('AGENTS.md', run.agents_md('root'))
            run.stub.watched = (markers['agents-root'], markers['app'])
            client = run.start()
            threads = {}
            for name in ('resumed without it', 'resumed with it again'):
                reply, error, turn = self.start(run, client, 'untrusted', developerInstructions=text)
                if error:
                    observed[name + ': first turn'] = 'start error: %s' % json.dumps(error)[:300]
                    continue
                threads[name] = reply['thread']['id']
                key = 'before_%d' % len(threads)
                status = self.keyed_turn(run, client, threads[name], key, **turn)
                observed[name + ': first turn'] = {'turn': status, 'placements': self.placed(run.stub, key, names)}
            client.stop()
            again = run.start()
            for index, (name, thread) in enumerate(threads.items()):
                frame, turn = self.frame(run, 'untrusted')
                for field in ('model', 'modelProvider'):
                    frame.pop(field)
                frame.update(threadId=thread, excludeTurns=True)
                if name == 'resumed with it again':
                    frame['developerInstructions'] = text
                resumed = again.call('thread/resume', frame)
                if 'error' in resumed:
                    observed[name + ': after the resume'] = 'resume error: %s' % json.dumps(resumed['error'])[:300]
                    continue
                key = 'after_%d' % index
                status = self.keyed_turn(run, again, thread, key, **turn)
                observed[name + ': after the resume'] = {
                    'resumed thread': resumed['result']['thread']['id'] == thread,
                    'files the resume names': self.sources(run, resumed['result']), 'turn': status,
                    'placements': self.placed(run.stub, key, names)}
        self.report(observed)
        once = {'turn': 'completed',
                'placed': [{'agents': (1, ['developer'], 0), 'app': (1, ['developer'], 0), 'order': 'same entry'}]}
        self.assertEqual({k: v if not isinstance(v, dict) else
                          dict({x: v[x] for x in ('turn', 'resumed thread') if x in v},
                               placed=self.shapes(v['placements'])) for k, v in observed.items()},
                         {'resumed without it: first turn': once,
                          'resumed with it again: first turn': once,
                          'resumed without it: after the resume': dict(once, **{'resumed thread': True}),
                          'resumed with it again: after the resume': dict(once, **{'resumed thread': True})},
                         'observed:\n%s' % shown(observed))

    # ----- what else a trusted project's settings reach -----

    def test_what_else_a_trusted_projects_settings_start(self):
        """One case per key a project's settings may still set (not stripped) that starts a process or opens a
        connection and that the rows above do not cover, each with the fixture's marker command or the second
        listener, on a fresh server for each entry, with the App's own start at edits (`mcp_case`). The keys
        considered and left out are listed in README.
        - `mcp_servers.<name>.http_headers_helper` on an HTTP server at the second listener. With the `trusted`
          entry: the helper has not run before the thread starts, has run at thread start and by the end of the
          first turn; the startup notifications are, as a set, `starting` and `failed` for the server;
          `mcpServerStatus/list` lists nothing of it; and the second listener has accepted no connection at any
          sample through the stop. With the `untrusted` entry: the helper never runs, no notification names the
          server, nothing is listed, and no connection. Recorded, not asserted: how many times the helper ran. The
          control: each entry against the other."""
        cases = {'mcp_servers.<name>.http_headers_helper': (lambda run: run.headers_helper_toml(), 'mcp-headers-helper')}
        observed = {}
        for name, (settings, marker) in cases.items():
            with L.Run(SCRATCH, BINARY, trusted_project=True) as run:
                run.write_trust_file('.codex/config.toml', settings(run))
                for trust in TRUST_CASES:
                    observed['%s, %s' % (name, trust)] = self.mcp_case(run, trust, markers=(marker,))
        self.report(observed)

        def seen(case):
            if 'start error' in case:
                return case
            samples = ('before the thread starts', 'at start', 'by the turn', 'after the listing', 'after the stop')
            return {'turn': case['turn'], 'ran': [case[when][0] > 0 for when in samples[:3]],
                    'connections': [case[when][1] for when in samples],
                    'startup notifications': case['startup notifications'], 'listed': case['listed']}
        notified = [(L.MCP_HELPER, 'failed'), (L.MCP_HELPER, 'starting')]
        self.assertEqual({k: seen(v) for k, v in observed.items()}, {
            'mcp_servers.<name>.http_headers_helper, trusted': {
                'turn': 'completed', 'ran': [False, True, True], 'connections': [0, 0, 0, 0, 0],
                'startup notifications': notified, 'listed': []},
            'mcp_servers.<name>.http_headers_helper, untrusted': {
                'turn': 'completed', 'ran': [False, False, False], 'connections': [0, 0, 0, 0, 0],
                'startup notifications': [], 'listed': []}},
            'observed:\n%s' % shown(observed))


if __name__ == '__main__':
    unittest.main(verbosity=2)
