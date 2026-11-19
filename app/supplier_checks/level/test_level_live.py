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
                self.assertEqual([r['method'] for r in client.server_requests if r['thread'] == thread],
                                 ['item/tool/requestUserInput'])  # the question and nothing else was asked
                listed = question_tool_description(next(r for r in run.stub.requests if r['key'] == key))
                self.assertIn('Default', listed)
                self.assertIn('Plan', listed)
                self.assertFalse(client.notes_for('turn/completed', thread, turn))
                client.answer_question(asked, {'q1': ['Yes']})
                self.assertEqual(self.completed(client, thread, turn), 'completed')
                self.assertEqual(json.loads(run.stub.outputs['call_' + key]), {'answers': {'q1': {'answers': ['Yes']}}})

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
            kept = [i for t in read['thread']['turns'] for i in t.get('items') or []
                    if i.get('type') == 'agentMessage' and i.get('questions')]
            self.assertEqual([i['questions'] for i in kept], [[ASYNC_QUESTION]])

    def test_a_plain_resume_gives_the_question_and_the_persons_reply_is_an_ordinary_message_after_it(self):
        with L.Run(SCRATCH, BINARY) as run:
            client = run.start()
            thread = client.start_thread(model=CATALOGUE_MODEL)['thread']['id']

            def script(body, outputs, stub):
                if 'call_resumeask' in outputs:
                    return [L.message('Carried on.', 'msg_resumeask')]
                return [{'type': 'function_call', 'name': 'request_user_input_async', 'call_id': 'call_resumeask',
                         'id': 'fc_resumeask', 'arguments': json.dumps({'questions': [ASYNC_QUESTION]})}]
            run.stub.scripts['resumeask'] = script
            asked_turn, done = client.turn(thread, 'LEVEL[resumeask] go')
            self.assertEqual(done['turn']['status'], 'completed')
            self.assertEqual(json.loads(run.stub.outputs['call_resumeask']), {'accepted': True})
            # In the turn's own items the question comes before the agent's closing message.
            live = [(i['type'], i['id']) for i in client.items(thread, asked_turn, 'agentMessage')]
            self.assertEqual(live, [('agentMessage', 'call_resumeask'), ('agentMessage', 'msg_resumeask')])
            client.kill()
            client.drain()

            def questions_in(turns):
                return [(t['id'], i['id'], i['questions']) for t in turns for i in t.get('items') or []
                        if i.get('type') == 'agentMessage' and i.get('questions')]
            again = run.start()
            resumed = again.result('thread/resume', {'threadId': thread})
            # The resume reply itself, with nothing further read, holds the question.
            self.assertEqual(questions_in(resumed['thread']['turns']), [(asked_turn, 'call_resumeask', [ASYNC_QUESTION])])
            # A list of the conversation's turns holds it too.
            listed = again.result('thread/turns/list', {'threadId': thread})['data']
            self.assertEqual(questions_in(listed), [(asked_turn, 'call_resumeask', [ASYNC_QUESTION])])

            # The person's reply is an ordinary next message: a new turn whose first item is theirs.
            run.stub.scripts['reply'] = lambda body, outputs, stub: [L.message('Thank you.', 'msg_reply')]
            reply_turn, done = again.turn(thread, 'LEVEL[reply] Invented yes')
            self.assertEqual(done['turn']['status'], 'completed')
            self.assertEqual([r['method'] for r in again.server_requests if r['thread'] == thread], [])
            read = again.result('thread/read', {'threadId': thread, 'includeTurns': True})['thread']['turns']
            self.assertEqual([t['id'] for t in read], [asked_turn, reply_turn])
            first = read[1]['items'][0]
            self.assertEqual(first['type'], 'userMessage')
            self.assertIn('Invented yes', json.dumps(first))
            self.assertEqual(questions_in(read), [(asked_turn, 'call_resumeask', [ASYNC_QUESTION])])

    def test_a_turn_summary_holds_the_persons_messages_and_the_question_as_the_full_read_does(self):
        """PROPOSED (written by the App lane's builder; not yet run): what the App's own history reads see. The App
        reads turns with `itemsView` `summary` after a restart; whether such a turn can establish that a question is
        waiting, or that a message from the person follows it, rests on the summary keeping those items in order."""
        with L.Run(SCRATCH, BINARY) as run:
            client = run.start()
            thread = client.start_thread(model=CATALOGUE_MODEL)['thread']['id']

            def ask(body, outputs, stub):
                if 'call_sumask' in outputs:
                    return [L.message('Carried on.', 'msg_sumask')]
                return [{'type': 'function_call', 'name': 'request_user_input_async', 'call_id': 'call_sumask',
                         'id': 'fc_sumask', 'arguments': json.dumps({'questions': [ASYNC_QUESTION]})}]
            run.stub.scripts['sumask'] = ask
            run.stub.scripts['sumreply'] = lambda body, outputs, stub: [L.message('Thank you.', 'msg_sumreply')]
            asked_turn, done = client.turn(thread, 'LEVEL[sumask] go')
            self.assertEqual(done['turn']['status'], 'completed')
            reply_turn, done = client.turn(thread, 'LEVEL[sumreply] Invented yes')
            self.assertEqual(done['turn']['status'], 'completed')
            client.kill()
            client.drain()

            def decisive(items):
                # The items a reading decides on: the person's messages, and questions by their id.
                return [('userMessage', None) if i.get('type') == 'userMessage' else ('question', i['id'])
                        for i in items or [] if i.get('type') == 'userMessage'
                        or (i.get('type') == 'agentMessage' and i.get('delivery') == 'async' and i.get('questions'))]
            again = run.start()
            again.result('thread/resume', {'threadId': thread, 'excludeTurns': True})
            # As the App's recovery and history reads ask: newest first, item summaries.
            summary = again.result('thread/turns/list', {'threadId': thread, 'sortDirection': 'desc', 'itemsView': 'summary'})['data']
            full = again.result('thread/read', {'threadId': thread, 'includeTurns': True})['thread']['turns']
            views = [(t['id'], t.get('itemsView')) for t in summary]
            self.assertEqual([t['id'] for t in summary], [reply_turn, asked_turn], views)
            self.assertEqual([decisive(t.get('items')) for t in full],
                             [[('userMessage', None), ('question', 'call_sumask')], [('userMessage', None)]])
            by_turn = {t['id']: decisive(t.get('items')) for t in full}
            for turn in summary:
                self.assertEqual(decisive(turn.get('items')), by_turn[turn['id']],
                                 'turn %s (itemsView %r) holds other decisive items than the full read' % (turn['id'], turn.get('itemsView')))

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


if __name__ == '__main__':
    unittest.main(verbosity=2)
