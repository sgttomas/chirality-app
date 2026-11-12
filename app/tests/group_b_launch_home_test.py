"""The examination launch helper, one class per guard, invariant and rule, with invented material only.

A shell script plays the App, and folders stand in for the real home and the
per-user cache folder. No App, window, socket or real home Library is touched;
nothing here launches a real build.
"""
import builtins
import contextlib
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import plistlib
import pwd
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from unittest import mock
from xml.parsers.expat import ExpatError

APP = Path(__file__).resolve().parents[1]
HELPER = APP / 'examination/standalone/launch.py'
SPEC = importlib.util.spec_from_file_location('examination_launch', HELPER)
launch = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(launch)
identify = launch.identify

MAC = sys.platform == 'darwin'
IDENTIFIER = 'dev.chirality.app-v4.candidate.invented'
PRODUCT = 'Chirality App v4 (development invented)'
EXECUTABLE = 'chirality-app-v4'
SECRET = 'invented-secret-from-the-home-7f3a'
INVENTED_SECRETS = {'ANTHROPIC_AUTH_TOKEN': 'invented-token-1', 'CLAUDE_CODE_MESSAGING_TOKEN': 'invented-token-2',
                    'SSH_AUTH_SOCK': '/invented/agent.sock', 'OPENAI_API_KEY': 'invented-key-3'}
PLAYS_THE_APP = '''env > "$HOME/received-env.txt"
echo {secret} > "$HOME/auth.json"
mkdir -p "$HOME/Library/Application Support/{id}" "$HOME/Library/WebKit/{id}/WebsiteData" "$HOME/Library/Caches/{id}"
echo invented > "$HOME/Library/Application Support/{id}/state"
echo invented > "$HOME/Library/WebKit/{id}/WebsiteData/store"
'''
TRAP = "trap 'exit 0' TERM\nwhile :; do sleep 0.1; done\n"
SHELL_OWN = {'PWD', 'SHLVL', '_', 'OLDPWD', '__CF_USER_TEXT_ENCODING'}  # set by /bin/sh or the macOS runtime itself
OVERRIDES = set(launch.PROXY_OVERRIDES) | {launch.MODEL_ADDRESS}
SAME = 'the same at the checks made (before the start and once after it)'

_PRIVATE_TMP = None


def setUpModule():
    """Fixtures live in a private folder under the account's home; each test also removes its own."""
    global _PRIVATE_TMP
    _PRIVATE_TMP = tempfile.mkdtemp(prefix='.launch-home-test-', dir=os.path.realpath(pwd.getpwuid(os.getuid()).pw_dir))


def tearDownModule():
    remove_fixture(_PRIVATE_TMP)


def remove_fixture(path):
    for current, dirs, files in os.walk(path):
        for name in dirs:
            with contextlib.suppress(OSError):
                if not os.path.islink(os.path.join(current, name)):
                    os.chmod(os.path.join(current, name), 0o700)
    with contextlib.suppress(OSError):
        os.chmod(path, 0o700)
    shutil.rmtree(path, ignore_errors=True)


def fake_identification(app, record_path):
    """Stands in for identify_candidate (INVARIANT 6 has its own tests): returns the invented record."""
    return json.loads(Path(record_path).read_text())


def fd_path(fd):
    """The path an open descriptor resolves to (instrumentation only)."""
    if MAC:
        import fcntl
        return os.fsdecode(fcntl.fcntl(fd, fcntl.F_GETPATH, bytes(1024)).split(b'\0', 1)[0])
    return os.readlink(f'/proc/self/fd/{fd}')


class Fixture(unittest.TestCase):
    identification = staticmethod(fake_identification)

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(dir=_PRIVATE_TMP))
        self.addCleanup(remove_fixture, self.tmp)
        self.real = self.tmp / 'real-home'  # stands in for the real home
        (self.real / 'Library/Preferences').mkdir(parents=True)
        (self.real / 'Library/Preferences/com.apple.dock.plist').write_bytes(b'invented system preference')
        self.cache = self.tmp / 'user-cache'  # stands in for DARWIN_USER_CACHE_DIR
        self.cache.mkdir()
        for name, value in (('real_home', self.real), ('user_cache_dir', self.cache)):
            patch = mock.patch.object(launch, name, return_value=value)
            patch.start()
            self.addCleanup(patch.stop)
        if self.identification is not None:
            patch = mock.patch.object(launch, 'identify_candidate', self.identification)
            patch.start()
            self.addCleanup(patch.stop)
        self.parent = self.tmp / 'parent'
        self.parent.mkdir()
        self.runs = 0
        self.groups = []
        self.addCleanup(self.kill_groups)

    def kill_groups(self):
        for group in self.groups:
            with contextlib.suppress(ProcessLookupError, PermissionError):
                os.killpg(group, signal.SIGKILL)

    def candidate(self, script='', identifier=IDENTIFIER, where='build', exit_status=0, shebang='#!/bin/sh',
                  executable=EXECUTABLE, plays=True, name=PRODUCT + '.app'):
        """A candidate folder in build_candidate.py's layout, with an invented identification record."""
        root = self.tmp / where
        app = root.joinpath(*launch.BUNDLE_FOLDER, name)
        (app / 'Contents/MacOS').mkdir(parents=True)
        (app / 'Contents/Resources/instructions').mkdir(parents=True)
        (app / 'Contents/Resources/instructions/AGENTS.md').write_text('invented guidance\n')
        (app / 'Contents/Info.plist').write_bytes(plistlib.dumps({
            'CFBundleIdentifier': identifier, 'CFBundleName': PRODUCT, 'CFBundleDisplayName': PRODUCT,
            'CFBundleExecutable': executable, 'CFBundleShortVersionString': '0.0.0'}))
        body = shebang + '\n' + (PLAYS_THE_APP.format(id=identifier, secret=SECRET) if plays else '') + script
        exe = app / 'Contents/MacOS' / executable
        exe.write_text(body + f'exit {exit_status}\n')
        exe.chmod(0o755)
        record = {'candidate_key': '0123456789-abcdefabcdef',
                  'bundle': {'identifier': identifier, 'name': name,
                             'executable': {'path': 'Contents/MacOS/' + executable,
                                            'sha256': hashlib.sha256(exe.read_bytes()).hexdigest()}}}
        (root / 'identification').mkdir()
        (root / 'identification/candidate-identification.json').write_text(json.dumps(record))
        (root / 'identification' / launch.INVENTORY).write_text('{}')
        return root

    def argv(self, candidate, *extra, reuse=None, settle='0', run_dir=None, owner=False):
        argv = ['launch', '--candidate', str(candidate), '--run-dir', str(run_dir), *extra]
        argv += ['--reuse', str(reuse)] if reuse else ['--parent', str(self.parent)]
        return argv + (['--owner-sitting'] if owner else [])

    def run_helper(self, candidate, *extra, reuse=None, settle='0', run_dir=None, owner=False):
        self.runs += 1
        run_dir = Path(run_dir or self.tmp / f'run-{self.runs}')
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err), \
                mock.patch.object(launch, 'SETTLE_SECONDS', float(settle)):
            code = launch.main(self.argv(candidate, *extra, reuse=reuse, settle=settle, run_dir=run_dir, owner=owner))
        saved = run_dir / launch.RECORD
        record = json.loads(saved.read_text()) if saved.exists() and not saved.is_symlink() else None
        if record and record.get('pid'):
            self.groups.append(record['pid'])
        return code, record, out.getvalue() + err.getvalue(), run_dir

    def call(self, *argv):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err), \
                mock.patch.object(launch, 'SETTLE_SECONDS', 0.0):
            code = launch.main(list(argv))
        return code, out.getvalue() + err.getvalue()

    def made(self, script='', owner=False, **options):
        candidate = self.candidate(script, where=f'made{self.runs}', **options)
        code, record, out, run_dir = self.run_helper(candidate, owner=owner)
        return candidate, Path(record['launch_folder']['launch_folder']), record

    def received(self, record):
        lines = (Path(record['home']) / 'received-env.txt').read_text().splitlines()
        return dict(line.split('=', 1) for line in lines if '=' in line)

    def assert_refused(self, code, out, reason):
        self.assertEqual(code, 2, out)
        self.assertIn(reason, json.loads(out.strip().splitlines()[-1])['error'])

    def newest_folder(self):
        folders = sorted(self.parent.glob('launch-*'), key=lambda p: p.stat().st_mtime_ns)
        return folders[-1] if folders else None

    def started(self, folder):
        """True once the helper latches signals and the App's process group is recorded."""
        if folder is None or not launch._forwarding.is_set():
            return False
        try:
            fd = os.open(folder / launch.CONTROL, launch.DIRECTORY)
            try:
                return launch.read_own(fd, launch.STATE, launch.STATE_FORMAT, 's')['process_group'] is not None
            finally:
                os.close(fd)
        except (OSError, ValueError):
            return False

    def in_background(self, act, folder=None):
        """Acts only once the helper latches signals and the App started; never otherwise."""
        result = {}

        def wait_then_act():
            deadline = time.monotonic() + 10
            while time.monotonic() < deadline and not self.started(folder or self.newest_folder()):
                time.sleep(0.05)
            time.sleep(0.3)
            if self.started(folder or self.newest_folder()):
                result['value'] = act(folder or self.newest_folder())
        thread = threading.Thread(target=wait_then_act)
        thread.start()
        return thread, result

    def everything_written(self, run_dir, out):
        texts = [out]
        for current, _, files in os.walk(run_dir):
            for name in files:
                path = Path(current) / name
                if not path.is_symlink():
                    texts.append(path.read_text(errors='replace'))
        return '\n'.join(texts)


class EnvironmentFromNothing(Fixture):  # GUARD 1, INVARIANT 1
    def test_child_receives_exactly_the_allowlist_while_the_helper_holds_tokens(self):
        candidate = self.candidate()
        with mock.patch.dict(os.environ, {**INVENTED_SECRETS, 'LANG': 'fr_FR.UTF-8', 'USER': 'invented',
                                          'HTTPS_PROXY': 'http://invented.example:8080',
                                          launch.MODEL_ADDRESS: 'http://invented.example/v1'}):
            code, record, out, _ = self.run_helper(candidate, '--app-env', 'CHIRALITY_RECORDS_STORE=/invented/store')
        self.assertEqual(code, 0, out)
        env = self.received(record)
        home = record['home']
        self.assertEqual(set(env) - SHELL_OWN, {'HOME', 'CFFIXED_USER_HOME', 'TMPDIR', 'PATH', 'LANG',
                                                'CHIRALITY_RECORDS_STORE'} | OVERRIDES)
        for name, value in INVENTED_SECRETS.items():
            self.assertNotIn(name, env)
            self.assertNotIn(value, (Path(home) / 'received-env.txt').read_text())
        self.assertEqual((env['HOME'], env['CFFIXED_USER_HOME']), (home, home))
        self.assertTrue(env['TMPDIR'].startswith(home + '/.chirality-launch-tmp-'))
        self.assertEqual((env['PATH'], env['LANG'], env['HTTPS_PROXY'], env[launch.MODEL_ADDRESS]),
                         (launch.SYSTEM_PATH, launch.DEFAULT_LANG, 'http://127.0.0.1:9', 'http://127.0.0.1:9/v1'))
        self.assertEqual(record['environment'], {k: env[k] for k in record['environment']})

    def test_the_environment_is_checked_against_the_allowlist_immediately_before_start(self):
        home, tmp = self.parent / 'h', '.chirality-launch-tmp-x'
        good = launch.child_environment(home, tmp, {}, 'en_US.UTF-8', 'not-owners-sitting')
        launch.check_environment(good, home, tmp, 'not-owners-sitting')
        cases = {
            'inherited name': {**good, 'SSH_AUTH_SOCK': '/x'},
            'HOME alone': {k: v for k, v in good.items() if k != 'CFFIXED_USER_HOME'},
            'CFFIXED_USER_HOME alone': {k: v for k, v in good.items() if k != 'HOME'},
            'homes differ': {**good, 'CFFIXED_USER_HOME': str(self.parent / 'other')},
            'TMPDIR an earlier folder': {**good, 'TMPDIR': str(home / '.chirality-launch-tmp-old')},
            'other PATH': {**good, 'PATH': '/opt/invented/bin:' + launch.SYSTEM_PATH},
        }
        for name, env in cases.items():
            with self.subTest(name), self.assertRaises(ValueError):
                launch.check_environment(env, home, tmp, 'not-owners-sitting')
        for pair in ('HOME=/x', 'CFFIXED_USER_HOME=/x', 'OPENAI_API_KEY=x', 'CHIRALITY_WORKSPACE', 'PATH=/x',
                     'HTTPS_PROXY=x', launch.MODEL_ADDRESS + '=http://127.0.0.1:9'):
            with self.subTest(pair), self.assertRaises(ValueError):
                launch.app_inputs([pair])

    def test_a_name_added_after_construction_is_refused_and_nothing_launches(self):
        candidate = self.candidate()
        built = launch.child_environment
        with mock.patch.object(launch, 'child_environment', lambda *a, **k: {**built(*a, **k), 'SSH_AUTH_SOCK': '/x'}):
            code, record, _, _ = self.run_helper(candidate)
        self.assertEqual((code, record['outcome'], record['started_at']), (2, 'not launched', None))
        self.assertFalse((Path(record['home']) / 'received-env.txt').exists())


class CleanRun(Fixture):  # GUARD 4, INVARIANT 2
    def test_links_at_or_beneath_a_watched_place_make_the_comparison_incomplete(self):
        lib = self.real / 'Library'
        outside = self.tmp / 'outside'
        cases = {
            'watched folder is a link': (
                lambda o: ((o / 'caches' / IDENTIFIER).mkdir(parents=True), (o / 'caches' / IDENTIFIER / 'f').write_text('a'),
                           (lib / 'Caches').symlink_to(o / 'caches')),
                f'echo b >> "{lib}/Caches/{IDENTIFIER}/f"\n', 'Caches'),
            'link beneath a watched entry': (
                lambda o: ((o / 'webkit').mkdir(parents=True), (o / 'webkit/f').write_text('a'),
                           (lib / 'WebKit' / IDENTIFIER).mkdir(parents=True),
                           (lib / 'WebKit' / IDENTIFIER / 'data').symlink_to(o / 'webkit')),
                f'echo b >> "{lib}/WebKit/{IDENTIFIER}/data/f"\n', f'WebKit/{IDENTIFIER}/data'),
        }
        for index, (name, (setup, script, link)) in enumerate(cases.items()):
            with self.subTest(name):
                setup(outside)
                code, record, out, _ = self.run_helper(self.candidate(script, where=f'link{index}'))
                self.assertEqual((code, record['outcome'], record['real_library']['result']), (1, 'failed', 'incomplete'), out)
                self.assertIn(link, record['real_library']['links_met'])
                for path in (lib / 'Caches', lib / 'WebKit'):
                    if path.is_symlink():
                        path.unlink()
                    elif path.exists():
                        shutil.rmtree(path)

    def test_failed_starts_exits_listings_and_lingering_processes_are_never_clean(self):
        cases = {
            'exit status 3': (dict(exit_status=3), None, 1),
            'does not start': (dict(shebang='#!/nonexistent/interpreter'), None, 1),
            'process left in the group': (dict(script='sleep 5 &\n'), None, 1),
            'after-listing fails': ({}, 'after', 1),
            'before-listing fails': ({}, 'before', 2),
        }
        real_listing = launch.listing
        for index, (name, (options, failing, expected)) in enumerate(cases.items()):
            with self.subTest(name):
                candidate = self.candidate(where=f'case{index}', **options)
                calls = []

                def listing(base, *args):
                    if Path(base) == self.real / 'Library':
                        calls.append(1)
                        if failing == 'before' or (failing == 'after' and len(calls) > 1):
                            raise PermissionError('invented: listing refused')
                    return real_listing(base, *args)
                with mock.patch.object(launch, 'listing', listing):
                    code, record, out, _ = self.run_helper(candidate)
                self.assertEqual(code, expected, out)
                self.assertNotEqual(record['outcome'], 'clean')
                if failing:
                    self.assertEqual(record['real_library']['result'], 'not made')

    def test_an_unexaminable_library_is_not_made_never_unchanged(self):
        lib = self.real / 'Library'
        for name, script, undo, expected in (
                ('made unreadable by the run', f'chmod 000 "{lib}"\n', lambda: lib.chmod(0o700), (1, 'failed')),
                ('an ancestor made unexaminable by the run', f'chmod 000 "{self.real}"\n', lambda: self.real.chmod(0o700),
                 (1, 'failed'))):
            with self.subTest(name):
                try:
                    code, record, out, _ = self.run_helper(self.candidate(script, where=name.replace(' ', '-')))
                finally:
                    undo()
                self.assertEqual((code, record['outcome'], record['real_library']['result']), (*expected, 'not made'), out)

    def test_the_record_states_its_fields_and_is_written_once(self):
        candidate = self.candidate()
        code, record, out, run_dir = self.run_helper(candidate)
        self.assertEqual((code, record['outcome']), (0, 'clean'), out)
        for field in ('note', 'helper', 'candidate_key', 'identifier', 'bundle', 'candidate_folder', 'launch_folder',
                      'home', 'home_kind', 'watched', 'environment', 'overrides_passed', 'address_override', 'output',
                      'started_at', 'pid', 'ended_at', 'process_group_after_settle', 'disclosed', 'ended',
                      'real_library', 'signals_received', 'home_path_during_launch', 'failures', 'outcome'):
            self.assertIn(field, record)
        self.assertEqual(set(record['output']), {'path', 'note'})
        self.assertEqual((record['real_library']['result'], record['signals_received'], record['home_path_during_launch']),
                         ('unchanged', [], SAME))
        self.assertEqual([n for n in os.listdir(run_dir)], [launch.RECORD])
        self.assertEqual(self.call(*self.argv(candidate, run_dir=run_dir))[0], 2)


class AtomicRecord(Fixture):  # GUARD 4: a record exists whole under its name or not at all (round 4, item 7)
    def test_an_interrupted_write_leaves_no_record_under_its_name(self):
        candidate = self.candidate()
        with mock.patch.object(launch.os, 'link', side_effect=OSError(28, 'No space left on device')):
            code, record, out, run_dir = self.run_helper(candidate)
        self.assertIsNone(record)
        self.assertNotEqual(code, 0)
        self.assertFalse((run_dir / launch.RECORD).exists())
        for name in os.listdir(run_dir):
            self.assertTrue(name.startswith('.' + launch.RECORD + '.partial-'))


class Signals(Fixture):  # GUARD 4: a signal to the helper before the outcome is fixed makes the run not clean
    def test_the_app_deleting_the_run_folder_and_exiting_zero_after_a_signal_is_not_clean(self):
        run_dir = self.tmp / f'run-{self.runs + 1}'
        candidate = self.candidate(f"trap 'rm -rf \"{run_dir}\"/*; exit 0' TERM\nwhile :; do sleep 0.1; done\n",
                                   where='deleting')
        thread, _ = self.in_background(lambda folder: os.kill(os.getpid(), signal.SIGTERM))
        code, record, out, _ = self.run_helper(candidate, settle='0.5')
        thread.join()
        self.assertEqual((record['ended'], code, record['outcome']), ('exited with status 0', 1, 'failed'), out)
        self.assertEqual(record['signals_received'][0]['signal'], 'SIGTERM')

    def test_a_signal_during_finalization_before_the_outcome_is_fixed_is_in_the_record(self):
        for step in ('settle', 'compare'):
            with self.subTest(step):
                candidate = self.candidate(where=f'final-{step}')
                sent = []
                real_compare, real_sleep = launch.compare, launch.time.sleep

                def send():
                    if not sent and launch._forwarding.is_set():
                        sent.append(1)
                        os.kill(os.getpid(), signal.SIGTERM)
                        real_sleep(0.05)

                def compare(*args):
                    if step == 'compare':
                        send()
                    return real_compare(*args)

                def sleep(seconds):
                    if step == 'settle':
                        send()
                    return real_sleep(seconds)
                with mock.patch.object(launch, 'compare', compare), mock.patch.object(launch.time, 'sleep', sleep):
                    code, record, out, _ = self.run_helper(candidate)
                self.assertEqual(sent, [1])
                self.assertEqual((code, record['outcome'], len(record['signals_received'])), (1, 'failed', 1), out)


class WatchedByExactName(Fixture):  # INVARIANT 3
    def test_an_executable_name_that_does_not_discriminate_is_refused(self):
        for index, name in enumerate(('a', 'app', 'chirality', 'Chirality-x')):
            with self.subTest(name):
                code, record, out, run_dir = self.run_helper(self.candidate(executable=name, where=f'short{index}'))
                self.assert_refused(code, out, 'does not discriminate')
                self.assertFalse(run_dir.exists())

    def test_the_rule_names_entries_exactly(self):
        helper = 'com.apple.WebKit.{}+chirality_app_v4-0a1b2c'
        watched = [IDENTIFIER, IDENTIFIER + '.plist', IDENTIFIER + '.savedState', 'prefix.' + IDENTIFIER, EXECUTABLE,
                   'Chirality-App-V4', helper.format('Networking'), helper.format('WebContent'), helper.format('GPU')]
        unwatched = [IDENTIFIER + '2', IDENTIFIER + '-other', EXECUTABLE + '.old', 'chirality-app', 'a',
                     'com.apple.WebKit.Networking+other_app-1', 'com.apple.WebKit.Networking+chirality_app_v4',
                     'com.apple.spaces.plist']
        for name in watched:
            self.assertTrue(launch.watched_name(name, IDENTIFIER, EXECUTABLE), name)
        for name in unwatched:
            self.assertFalse(launch.watched_name(name, IDENTIFIER, EXECUTABLE), name)

    def test_changed_preference_files_are_disclosed_whatever_their_names(self):
        prefs = self.real / 'Library/Preferences'
        code, record, out, _ = self.run_helper(self.candidate(
            f'echo x > "{prefs}/com.apple.spaces.plist"\necho y >> "{prefs}/com.apple.dock.plist"\n'
            f'ln -s /invented/target "{prefs}/com.apple.linked.plist"\n'))
        self.assertEqual((code, record['outcome']), (0, 'clean'), out)
        preferences = record['disclosed']['preferences']
        self.assertEqual(preferences['observation'], 'made')
        self.assertEqual({(c['path'], c['change']) for c in preferences['changes']},
                         {('com.apple.spaces.plist', 'created'), ('com.apple.dock.plist', 'modified'),
                          ('com.apple.linked.plist', 'created')})
        code, record, out, _ = self.run_helper(self.candidate(f'echo x > "{prefs}/{IDENTIFIER}.plist"\n', where='named'))
        self.assertEqual((code, record['real_library']['result']), (1, 'changed'), out)


class ObservationNotGate(Fixture):  # RULE D
    def test_the_per_user_cache_folder_is_disclosed_and_never_a_failure(self):
        helper = f'com.apple.WebKit.WebContent+{EXECUTABLE.replace("-", "_")}-0a1b'
        code, record, out, _ = self.run_helper(self.candidate(
            f'mkdir -p "{self.cache}/{helper}" "{self.cache}/{IDENTIFIER}"\n'
            f'echo x > "{self.cache}/{helper}/data"\necho x > "{self.cache}/unrelated"\n'))
        self.assertEqual((code, record['outcome']), (0, 'clean'), out)
        cache = record['disclosed']['user_cache']
        self.assertEqual({(c['path'], c['change']) for c in cache['changes']},
                         {(helper, 'created'), (helper + '/data', 'created'), (IDENTIFIER, 'created')})

    def test_an_unexaminable_or_linked_cache_folder_neither_refuses_nor_reports_changes(self):
        hidden_parent = self.tmp / 'hidden'
        (hidden_parent / 'cache').mkdir(parents=True)
        target = self.tmp / 'cache-target'
        target.mkdir()
        link = self.tmp / 'cache-link'
        link.symlink_to(target)
        for name, setup, undo, base, expected in (
                ('unreadable folder', lambda: self.cache.chmod(0o000), lambda: self.cache.chmod(0o700), self.cache,
                 'not observed'),
                ('unexaminable ancestor', lambda: hidden_parent.chmod(0o000), lambda: hidden_parent.chmod(0o700),
                 hidden_parent / 'cache', 'not observed'),
                ('the folder is a link', lambda: None, lambda: None, link,
                 'not observed: the per-user cache folder is a link')):
            with self.subTest(name), mock.patch.object(launch, 'user_cache_dir', return_value=base):
                setup()
                try:
                    code, record, out, _ = self.run_helper(self.candidate(where=name.replace(' ', '-')))
                finally:
                    undo()
                self.assertEqual((code, record['outcome']), (0, 'clean'), out)
                cache = record['disclosed']['user_cache']
                self.assertTrue(cache['observation'].startswith(expected), cache)
                self.assertNotIn('changes', cache)


@contextlib.contextmanager
def reads_under(*roots):
    """Instrumentation, lexical and resolved: every open, listing or stat whose path, or whose descriptor-relative
    path or resolved target, is or lies under one of roots. Only exclusive write-only creation is not counted; an
    open or stat of a root itself is counted only when `strict` roots are given as (path, True)."""
    watched = [(os.path.realpath(r[0]), r[1]) if isinstance(r, tuple) else (os.path.realpath(r), False) for r in roots]
    touched = []

    def hit(text):
        if text is None:
            return False
        return any(text.startswith(root + os.sep) or (strict and text == root) for root, strict in watched)

    def resolve(path, dir_fd):
        if isinstance(path, int):
            return fd_path(path)
        if path is None:
            return None
        text = os.fsdecode(path)
        if dir_fd is not None and not os.path.isabs(text):
            return os.path.normpath(os.path.join(fd_path(dir_fd), text))
        return os.path.abspath(text)

    real = {name: getattr(os, name) for name in ('listdir', 'scandir', 'stat', 'lstat', 'open')}

    def wrap(name):
        def spied(*args, **kwargs):
            path = args[0] if args else kwargs.get('path', '.')
            lexical = resolve(path, kwargs.get('dir_fd'))
            flags = (args[1] if len(args) > 1 else kwargs.get('flags', 0)) if name == 'open' else 0
            creating = name == 'open' and flags & os.O_ACCMODE == os.O_WRONLY and flags & os.O_CREAT and flags & os.O_EXCL
            try:
                result = real[name](*args, **kwargs)
            except OSError:
                if not creating and hit(lexical):
                    touched.append((name, lexical, None))
                raise
            resolved = fd_path(result) if name == 'open' else None
            listing = name in ('listdir', 'scandir') and any(lexical == root for root, _ in watched)
            if not creating and (hit(lexical) or hit(resolved) or listing):
                touched.append((name, lexical, resolved))
            return result
        return spied
    real_open = builtins.open

    def spied_open(file, *args, **kwargs):
        if not isinstance(file, int) and hit(os.path.realpath(os.fsdecode(file))):
            touched.append(('open', file, None))
        return real_open(file, *args, **kwargs)
    with contextlib.ExitStack() as stack:
        for name in real:
            stack.enter_context(mock.patch.object(os, name, wrap(name)))
        stack.enter_context(mock.patch.object(builtins, 'open', spied_open))
        stack.enter_context(mock.patch.object(io, 'open', spied_open))
        yield touched


class NeverReadsAHome(Fixture):  # GUARD 2, RULE A
    def test_launch_reuse_signal_failed_start_and_refused_reuse_read_nothing_under_the_home(self):
        candidate, folder, first = self.made()
        quiet = self.candidate(TRAP, where='quiet', plays=False)
        broken = self.candidate(where='broken', shebang='#!/nonexistent/interpreter')
        lingering = self.candidate('sleep 30 &\n', where='lingering', plays=False)
        with reads_under(folder / launch.HOME) as touched:
            code, _, out, _ = self.run_helper(candidate, reuse=folder)
            self.assertEqual(code, 0, out)
            thread, _ = self.in_background(lambda f: os.kill(os.getpid(), signal.SIGTERM), folder)
            code, _, out, _ = self.run_helper(quiet, reuse=folder, settle='0.3')
            thread.join()
            self.assertEqual(code, 1, out)
            code, _, out, _ = self.run_helper(broken, reuse=folder)
            self.assertEqual(code, 1, out)
            self.run_helper(lingering, reuse=folder)
            code, _, out, _ = self.run_helper(candidate, reuse=folder)
            self.assert_refused(code, out, 'process group')
        self.assertEqual(touched, [])

    def test_a_new_home_is_never_read_either(self):
        candidate = self.candidate()
        with reads_under(self.parent) as touched:
            code, record, out, _ = self.run_helper(candidate)
        self.assertEqual(code, 0, out)
        self.assertEqual([t for t in touched if (t[1] or '').startswith(record['home'] + os.sep)
                          or (t[2] or '').startswith(record['home'] + os.sep)], [])

    def test_a_control_folder_linked_into_the_home_is_refused_unread(self):
        candidate, folder, record = self.made()
        home = folder / launch.HOME
        fake = home / 'fake-control'
        shutil.copytree(folder / launch.CONTROL, fake)
        (folder / launch.CONTROL).rename(folder / 'control-moved')
        (folder / launch.CONTROL).symlink_to(fake)
        with reads_under(home) as touched:
            code, _, out, _ = self.run_helper(candidate, reuse=folder)
            self.assert_refused(code, out, 'control folder is missing or a link')
        self.assertEqual(touched, [])

    def test_with_every_entry_of_the_app_at_mode_000_a_reuse_launch_does_not_fail(self):
        candidate, folder, first = self.made('mkdir -p "$HOME/private/deeper"\necho x > "$HOME/private/deeper/f"\n')
        for entry in (folder / launch.HOME).iterdir():
            if not entry.name.startswith('.chirality-launch-output-'):
                entry.chmod(0o000)
        code, record, out, _ = self.run_helper(self.candidate(where='quiet', plays=False), reuse=folder)
        self.assertEqual((code, record['outcome']), (0, 'clean'), out)

    def test_a_temporary_folder_replaced_by_a_link_is_never_used_again(self):
        outside = self.tmp / 'outside-tmp'
        outside.mkdir()
        candidate, folder, first = self.made(f'rm -rf "$TMPDIR"\nln -s "{outside}" "$TMPDIR"\n')
        old_tmp = self.received(first)['TMPDIR']
        writer = self.candidate('echo x > "$TMPDIR/written"\nenv > "$HOME/received-env.txt"\n', where='writer', plays=False)
        code, record, out, _ = self.run_helper(writer, reuse=folder)
        self.assertEqual(code, 0, out)
        new_tmp = self.received(record)['TMPDIR']
        self.assertNotEqual(new_tmp, old_tmp)
        self.assertTrue((Path(new_tmp) / 'written').exists())
        self.assertEqual(os.listdir(outside), [])


class MistakenPaths(Fixture):  # GUARD 3: round 4's items 3, 4 and 6, refused before anything is touched
    def test_round4_paths_inside_a_launch_folder_are_refused_untouched(self):
        candidate, folder, record = self.made()
        home = folder / launch.HOME
        (home / 'written-identification.json').write_text(json.dumps({'candidate_key': SECRET}))
        (home / 'sessions').mkdir()
        inner = self.candidate(where=f'{folder.relative_to(self.tmp)}/home/cand')  # a candidate written under the home
        cases = {
            'candidate folder under the home': self.argv(inner, run_dir=self.tmp / 'r1'),
            'candidate folder is the home': self.argv(home, run_dir=self.tmp / 'r2'),
            'run folder under the home (H/sessions/run)': self.argv(candidate, run_dir=home / 'sessions/run'),
            'run folder in the control folder': self.argv(candidate, run_dir=folder / launch.CONTROL / 'run'),
            'parent under the home': self.argv(candidate, run_dir=self.tmp / 'r3') [:-2] + ['--parent', str(home)],
            'the home given for reuse': self.argv(candidate, run_dir=self.tmp / 'r4', reuse=home),
            'the control folder given for reuse': self.argv(candidate, run_dir=self.tmp / 'r5', reuse=folder / launch.CONTROL),
        }
        for name, argv in cases.items():
            with self.subTest(name):
                with reads_under((str(home), True), (str(folder / launch.CONTROL), True)) as touched:
                    code, out = self.call(*argv)
                self.assert_refused(code, out, 'launch folder')
                self.assertEqual(touched, [])
                self.assertNotIn(SECRET, out)
        self.assertFalse((home / 'sessions/run').exists())

    def test_round4_ambiguous_syntax_is_refused_before_normalisation(self):
        candidate, folder, record = self.made()
        (self.tmp / 'other/deep').mkdir(parents=True)
        (self.tmp / 'linked').symlink_to(self.tmp / 'other/deep')
        for name, text in (('".." through a link (B/linked/../parent)', f'{self.tmp}/linked/../parent'),
                           ('"." component', f'{self.tmp}/./parent'), ('empty component', f'{self.tmp}//parent'),
                           ('trailing slash', f'{self.parent}/'), ('relative', 'parent')):
            with self.subTest(name):
                argv = self.argv(candidate, run_dir=self.tmp / 'r')[:-2] + ['--parent', text]
                self.assert_refused(*self.call(*argv), 'written ambiguously' if text.startswith('/') else 'absolute')
                self.assertFalse((self.tmp / 'r').exists())
        for option in ('--candidate', '--run-dir'):
            with self.subTest(option):
                argv = self.argv(candidate, run_dir=self.tmp / 'r')
                argv[argv.index(option) + 1] += '/'
                self.assert_refused(*self.call(*argv), 'written ambiguously')
        self.assertEqual(sorted(p.name for p in (self.tmp / 'other/deep').iterdir()), [])

    def test_links_in_a_candidate_folder_are_refused(self):
        candidate = self.candidate()
        outside = self.tmp / 'outside-identification'
        shutil.copytree(candidate / 'identification', outside)
        shutil.rmtree(candidate / 'identification')
        (candidate / 'identification').symlink_to(outside)
        self.assert_refused(*self.call(*self.argv(candidate, run_dir=self.tmp / 'r')), 'identification folder')
        aliased = self.tmp / 'aliased'
        aliased.symlink_to(self.candidate(where='plain'))
        self.assert_refused(*self.call(*self.argv(aliased, run_dir=self.tmp / 'r')), 'no link')

    def test_places_by_identity(self):
        candidate = self.candidate()
        (self.tmp / 'CaseProbe').write_text('')
        if (self.tmp / 'caseprobe').exists():
            (self.real / 'Library/Caches').mkdir()
            self.assert_refused(*self.call(*self.argv(candidate, run_dir=self.real / 'library/Caches/run')),
                                'inside the real home Library')
        checkout = self.tmp / 'checkout'
        (checkout / '.git').mkdir(parents=True)
        self.assert_refused(*self.call(*self.argv(candidate, run_dir=checkout / 'run')), 'checkout')
        self.assert_refused(*self.call(*self.argv(candidate, run_dir=launch.REPOSITORY / 'launch-run')), 'checkout')
        for where in ('elsewhere/Applications/c', 'deep/APPLICATIONS/x/c'):
            self.assert_refused(*self.call(*self.argv(self.candidate(where=where), run_dir=self.tmp / 'r')),
                                'Applications folder')
        self.assertFalse((launch.REPOSITORY / 'launch-run').exists())


class OwnFilesDefensive(Fixture):  # GUARDS 2 and 3, RULE B
    def corrupt(self, path, how, secret_path):
        path.unlink()
        if how == 'symlink':
            path.symlink_to(secret_path)
        elif how == 'hard link':
            os.link(secret_path, path)
        elif how == 'directory':
            path.mkdir()
        elif how == 'extra key':
            path.write_text(json.dumps({'format': 'x', 'extra': SECRET}))
        elif how == 'empty':
            path.write_text('')
        elif how == 'not a dictionary':
            path.write_text(json.dumps([SECRET]))

    def test_marker_state_and_lock_that_are_not_the_helpers_own_are_refused_unread_and_unquoted(self):
        for target in (launch.MARKER, launch.STATE, launch.LOCK):
            for how in ('symlink', 'hard link', 'directory', 'extra key', 'empty', 'not a dictionary', 'missing'):
                if target == launch.LOCK and how in ('extra key', 'empty', 'not a dictionary'):
                    continue  # the lock's contents are never read
                with self.subTest(target=target, how=how):
                    candidate, folder, record = self.made()
                    path = folder / launch.CONTROL / target
                    if how == 'missing':
                        path.unlink()
                    else:
                        self.corrupt(path, how, Path(record['home']) / 'auth.json')
                    real_read, read = os.read, []

                    def spied_read(fd, size):
                        data = real_read(fd, size)
                        read.append(data)
                        return data
                    with mock.patch.object(launch.os, 'read', spied_read):
                        code, _, out, run_dir = self.run_helper(candidate, reuse=folder)
                    self.assertEqual(code, 2, out)
                    self.assertNotIn(SECRET, out)
                    self.assertFalse(run_dir.exists())
                    if how in ('symlink', 'hard link'):
                        self.assertFalse(any(SECRET.encode() in data for data in read))

    def test_nothing_planted_by_the_app_reaches_a_record_or_output(self):
        run_dir = self.tmp / f'run-{self.runs + 1}'
        code, record, out, _ = self.run_helper(self.candidate(
            f'mkdir -p "{run_dir}/x"\nln -s "$HOME/auth.json" "{run_dir}/x/planted.json"\necho {SECRET}\necho {SECRET} >&2\n'))
        self.assertEqual(code, 0, out)
        self.assertNotIn(SECRET, self.everything_written(run_dir, out))


class LaunchFolderCustody(Fixture):  # GUARDS 3 and 4, INVARIANT 5
    def test_a_marker_copied_into_a_replacement_folder_is_refused(self):
        candidate, folder, _ = self.made()
        folder.rename(self.parent / 'moved')
        (folder / launch.HOME).mkdir(parents=True)
        shutil.copytree(self.parent / 'moved' / launch.CONTROL, folder / launch.CONTROL)
        code, _, out, _ = self.run_helper(candidate, reuse=folder)
        self.assert_refused(code, out, 'recorded identity differs')

    def test_a_living_member_of_the_apps_group_keeps_the_folder_refused(self):
        candidate, folder, record = self.made('sleep 30 &\n')
        code, _, out, _ = self.run_helper(candidate, reuse=folder)
        self.assert_refused(code, out, 'process group')

    def test_reuse_records_reused_and_says_nothing_about_the_home(self):
        candidate, folder, _ = self.made()
        code, record, out, _ = self.run_helper(candidate, reuse=folder)
        self.assertEqual(code, 0, out)
        self.assertEqual(record['launch_folder'], {'launch_folder': str(folder), 'state': 'reused'})

    def test_two_honest_callers_at_once_one_is_refused(self):
        candidate, folder, _ = self.made()
        slow = self.candidate('sleep 1\n', where='slow', plays=False)
        second = {}

        def other(folder):
            second['reuse'] = self.call(*self.argv(candidate, reuse=folder, run_dir=self.tmp / 'second-run'))
        thread, _ = self.in_background(other, folder)
        code, record, out, _ = self.run_helper(slow, reuse=folder)
        thread.join()
        self.assertEqual((code, record['outcome']), (0, 'clean'), out)
        self.assert_refused(*second['reuse'], 'in use by another invocation')
        self.assertFalse((self.tmp / 'second-run').exists())


KILLED_RUNNER = '''
import importlib.util, json, sys, time
from pathlib import Path
from unittest import mock
spec = importlib.util.spec_from_file_location('launch_under_test', sys.argv[1])
launch = importlib.util.module_from_spec(spec)
spec.loader.exec_module(launch)
stage, real, cache, sentinel = sys.argv[2], Path(sys.argv[3]), Path(sys.argv[4]), Path(sys.argv[5])
def reached(*args, **kwargs):
    sentinel.write_text('reached')
    time.sleep(60)
patches = [mock.patch.object(launch, 'SETTLE_SECONDS', 0.0),
           mock.patch.object(launch, 'real_home', return_value=real),
           mock.patch.object(launch, 'user_cache_dir', return_value=cache),
           mock.patch.object(launch, 'identify_candidate', lambda app, record: json.loads(Path(record).read_text()))]
if stage == 'before start':
    patches.append(mock.patch.object(launch, 'check_environment', reached))
if stage == 'finalizing':
    patches.append(mock.patch.object(launch, 'compare', reached))
if stage == 'record write':
    patches.append(mock.patch.object(launch.os, 'link', reached))
for patch in patches:
    patch.start()
sys.exit(launch.main(sys.argv[6:]))
'''


class KilledHelper(Fixture):  # GUARD 4 (round 4, item 7): a killed helper leaves nothing that reads as completed
    def test_a_helper_killed_at_each_stage_leaves_no_record_and_an_interrupted_launch_folder(self):
        runner = self.tmp / 'runner.py'
        runner.write_text(KILLED_RUNNER)
        for stage in ('before start', 'running', 'finalizing', 'record write'):
            with self.subTest(stage):
                candidate, folder, _ = self.made()
                slug = stage.replace(' ', '-')
                sentinel = self.tmp / f'sentinel-{slug}'
                script = f'echo reached > "{sentinel}"\nsleep 60\n' if stage == 'running' else ''
                runnable = self.candidate(script, where=f'killed-{slug}', plays=False)
                run_dir = self.tmp / f'killed-run-{slug}'
                helper = subprocess.Popen([sys.executable, '-B', str(runner), str(HELPER), stage, str(self.real),
                                           str(self.cache), str(sentinel),
                                           *self.argv(runnable, reuse=folder, run_dir=run_dir)],
                                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                deadline = time.monotonic() + 20
                while not sentinel.exists() and time.monotonic() < deadline:
                    time.sleep(0.05)
                self.assertTrue(sentinel.exists())
                helper.kill()
                helper.wait()
                fd = os.open(folder / launch.CONTROL, launch.DIRECTORY)
                try:
                    group = launch.read_own(fd, launch.STATE, launch.STATE_FORMAT, 's')['process_group']
                finally:
                    os.close(fd)
                if group:
                    self.groups.append(group)
                self.assertFalse((run_dir / launch.RECORD).exists())
                for name in (os.listdir(run_dir) if run_dir.exists() else []):
                    self.assertTrue(name.startswith('.' + launch.RECORD + '.partial-'), name)
                code, _, out, _ = self.run_helper(candidate, reuse=folder)
                self.assert_refused(code, out, 'interrupted launch')
                self.assertTrue(folder.exists())


class OnlyTheIdentifiedCandidate(Fixture):  # INVARIANT 6
    identification = None

    def record_path(self, candidate):
        return candidate / 'identification/candidate-identification.json'

    def test_unknown_format_or_missing_key_is_refused_and_no_record_value_is_quoted(self):
        candidate = self.candidate()
        record = json.loads(self.record_path(candidate).read_text())
        for name, value in (('unknown format', {**record, 'format': 'invented/v9', 'candidate_key': SECRET}),
                            ('schema failure', {**record, 'format': identify.FORMAT, 'candidate_key': SECRET}),
                            ('empty candidate key', {**record, 'candidate_key': ''})):
            with self.subTest(name):
                self.record_path(candidate).write_text(json.dumps(value))
                code, _, out, run_dir = self.run_helper(candidate)
                self.assertEqual(code, 2, out)
                self.assertNotIn(SECRET, out)
                self.assertFalse(run_dir.exists())

    def test_a_check_that_finds_a_difference_is_refused_by_counts_and_field_names(self):
        candidate = self.candidate()
        same = {'equal': True, 'build_identity': 'x', 'recorded_build_identity': 'x', 'record_fields_mismatched': []}
        for name, result in (('inventory differs', {**same, 'equal': False, 'missing': [SECRET]}),
                             ('identity differs', {**same, 'build_identity': 'y'}),
                             ('record fields differ', {**same, 'record_fields_mismatched': ['identifier']})):
            with self.subTest(name), mock.patch.object(identify, 'validate_record'), \
                    mock.patch.object(identify, 'check', return_value=result):
                code, _, out, run_dir = self.run_helper(candidate)
                self.assert_refused(code, out, 'differs from its identification record')
                self.assertNotIn(SECRET, out)

    def test_an_unreadable_property_list_is_a_structured_refusal(self):
        candidate = self.candidate()
        for error in (plistlib.InvalidFileException(), ExpatError('invented')):
            with self.subTest(type(error).__name__), mock.patch.object(identify, 'validate_record'), \
                    mock.patch.object(identify, 'check', side_effect=error):
                code, _, out, _ = self.run_helper(candidate)
                self.assertEqual(code, 2)

    @unittest.skipUnless(MAC, "identification's check reads live macOS metadata")
    def test_a_changed_resource_is_refused_and_the_identified_bundle_launches(self):
        candidate = self.candidate()
        app = candidate.joinpath(*launch.BUNDLE_FOLDER, PRODUCT + '.app')
        shutil.rmtree(candidate / 'identification')
        repo = self.tmp / 'repo'
        (repo / 'src').mkdir(parents=True)
        (repo / 'src/main.rs').write_text('fn main() {}\n')
        env = {'PATH': launch.SYSTEM_PATH, 'HOME': str(self.tmp), 'GIT_CONFIG_NOSYSTEM': '1',
               'GIT_AUTHOR_NAME': 'Fixture', 'GIT_AUTHOR_EMAIL': 'fixture@example.invalid',
               'GIT_COMMITTER_NAME': 'Fixture', 'GIT_COMMITTER_EMAIL': 'fixture@example.invalid'}
        for command in (['init', '-q'], ['add', '.'], ['commit', '-q', '-m', 'fixture']):
            subprocess.run(['git', '-C', str(repo), *command], check=True, env=env, capture_output=True)
        export = self.tmp / 'export'
        export.mkdir()
        subprocess.run(['tar', '-x', '-C', str(export)], input=identify.git(repo, 'archive', 'HEAD'), check=True)
        facts = self.tmp / 'facts.json'
        facts.write_text(json.dumps({'procedure': 'invented', 'profile': 'debug', 'signing': 'none', 'features': [],
                                     'command': ['build'], 'config_overlays': [], 'toolchain': {}, 'lockfiles': {},
                                     'offline': True, 'environment': {}, 'started_at': '2000-01-01T00:00:00Z',
                                     'finished_at': '2000-01-01T00:00:00Z'}))
        with mock.patch.object(Path, 'home', return_value=self.real), contextlib.redirect_stdout(io.StringIO()):
            code = identify.main(['record', '--app', str(app), '--repo', str(repo), '--revision', 'HEAD',
                                  '--export-root', str(export), '--build-facts', str(facts),
                                  '--identified-at', '2000-01-01T00:00:00Z', '--out-dir', str(candidate / 'identification')])
        self.assertEqual(code, 0)
        code, record, out, _ = self.run_helper(candidate)
        self.assertEqual((code, record['outcome']), (0, 'clean'), out)
        (app / 'Contents/Resources/instructions/AGENTS.md').write_text('changed after identification\n')
        code, _, out, run_dir = self.run_helper(candidate)
        self.assert_refused(code, out, '1 changed')
        self.assertFalse(run_dir.exists())


class Overrides(Fixture):  # GUARD 3, INVARIANT 7
    def test_the_default_home_is_not_the_owners_sitting_and_is_passed_the_nine_overrides(self):
        code, record, out, _ = self.run_helper(self.candidate())
        self.assertEqual(code, 0, out)
        self.assertEqual(record['home_kind'], 'not-owners-sitting')
        env = self.received(record)
        for name in ('HTTPS_PROXY', 'https_proxy', 'HTTP_PROXY', 'http_proxy', 'ALL_PROXY', 'all_proxy'):
            self.assertEqual(env[name], 'http://127.0.0.1:9')
        self.assertEqual((env['NO_PROXY'], env['no_proxy']), ('127.0.0.1,localhost,::1',) * 2)
        self.assertEqual(record['overrides_passed'], {name: env[name] for name in OVERRIDES})

    def test_round4_address_omitted_is_the_recorded_default_and_empty_or_blank_is_refused(self):
        candidate = self.candidate()
        code, record, out, _ = self.run_helper(candidate)
        self.assertEqual((record['address_override'], self.received(record)[launch.MODEL_ADDRESS]),
                         ('the default (nothing listens there)', launch.DEFAULT_MODEL_ADDRESS))
        for value in ('', '   '):
            with self.subTest(repr(value)):
                code, _, out, run_dir = self.run_helper(candidate, '--model-address', value)
                self.assert_refused(code, out, launch.MODEL_ADDRESS)
                self.assertFalse(run_dir.exists())
        code, record, out, _ = self.run_helper(candidate, '--model-address', 'http://127.0.0.1:8080/v1')
        self.assertEqual((record['address_override'], self.received(record)[launch.MODEL_ADDRESS]),
                         ('given by the caller', 'http://127.0.0.1:8080/v1'))

    def test_an_owners_sitting_launch_is_passed_the_allowlist_without_the_nine(self):
        with mock.patch.dict(os.environ, INVENTED_SECRETS):
            code, record, out, _ = self.run_helper(self.candidate(), '--app-env', 'CHIRALITY_WORKSPACE=/invented',
                                                   owner=True)
        self.assertEqual(code, 0, out)
        self.assertEqual(set(self.received(record)) - SHELL_OWN,
                         {'HOME', 'CFFIXED_USER_HOME', 'TMPDIR', 'PATH', 'LANG', 'CHIRALITY_WORKSPACE'})
        self.assertEqual(record['overrides_passed'], "none (an owner's-sitting launch)")

    def test_every_inconsistency_of_kind_the_helper_can_see_before_the_start_is_refused(self):
        owner = self.candidate(where='owner')
        code, record, out, _ = self.run_helper(owner, owner=True)
        owner_folder = Path(record['launch_folder']['launch_folder'])
        candidate, other_folder, _ = self.made()
        for name, argv, reason in (
                ("an address on an owner's-sitting home", self.argv(owner, '--model-address', 'http://127.0.0.1:8080/v1',
                                                                    reuse=owner_folder, run_dir=self.tmp / 'k1'), "owner's-sitting"),
                ("an empty address on an owner's-sitting home", self.argv(owner, '--model-address', '',
                                                                          reuse=owner_folder, run_dir=self.tmp / 'k2'), "owner's-sitting"),
                ('--owner-sitting on a home of the other kind', self.argv(candidate, reuse=other_folder,
                                                                          run_dir=self.tmp / 'k3', owner=True), 'contradicts')):
            with self.subTest(name):
                self.assert_refused(*self.call(*argv), reason)
        built = launch.child_environment
        with mock.patch.object(launch, 'child_environment', lambda h, t, i, l, k, *a: built(h, t, i, l, 'not-owners-sitting')):
            code, record, out, _ = self.run_helper(owner, reuse=owner_folder)
        self.assertEqual((code, record['outcome']), (2, 'not launched'), out)
        for folder, edited in ((owner_folder, 'not-owners-sitting'), (other_folder, 'owners-sitting')):
            with self.subTest('the kind edited in the marker', to=edited):
                marker_path = folder / launch.CONTROL / launch.MARKER
                marker = json.loads(marker_path.read_text())
                marker['kind'] = edited
                marker_path.unlink()
                marker_path.write_text(json.dumps(marker))
                code, _, out, _ = self.run_helper(candidate, reuse=folder)
                self.assert_refused(code, out, 'does not agree with its name')

    def test_a_home_path_swapped_at_the_start_is_not_the_same_at_the_check_after_it(self):
        owner = self.candidate(where='owner', plays=False)
        code, record, out, _ = self.run_helper(owner, owner=True)
        owner_home = Path(record['home'])
        candidate, folder, _ = self.made()
        home = folder / launch.HOME
        real_popen = subprocess.Popen

        def swapped(*args, **kwargs):
            if str(args[0][0]).endswith('/' + EXECUTABLE):
                home.rename(folder / 'home-moved')
                home.symlink_to(owner_home)
            return real_popen(*args, **kwargs)
        writer = self.candidate('echo written > "$HOME/written-by-the-launch"\n', where='writer', plays=False)
        try:
            with mock.patch.object(launch.subprocess, 'Popen', swapped):
                code, record, out, _ = self.run_helper(writer, reuse=folder)
        finally:
            home.unlink()
            (folder / 'home-moved').rename(home)
        self.assertEqual((code, record['outcome']), (1, 'failed'), out)
        self.assertEqual(record['home_path_during_launch'], 'not the same at the check made once after the start')
        self.assertTrue((owner_home / 'written-by-the-launch').exists())  # it had already reached the App

    def test_a_home_path_that_does_not_resolve_before_the_start_is_not_launched(self):
        candidate, folder, _ = self.made()
        with mock.patch.object(launch, 'home_path_holds', return_value=False):
            code, record, out, _ = self.run_helper(candidate, reuse=folder)
        self.assertEqual((code, record['outcome']), (2, 'not launched'), out)

    def test_each_of_the_nine_removed_or_altered_just_before_launch_is_refused(self):
        home, tmp = self.parent / 'h', '.chirality-launch-tmp-x'
        good = launch.child_environment(home, tmp, {}, 'en_US.UTF-8', 'not-owners-sitting')
        owner = launch.child_environment(home, tmp, {}, 'en_US.UTF-8', 'owners-sitting')
        launch.check_environment(owner, home, tmp, 'owners-sitting')
        for name in sorted(OVERRIDES):
            for case, env in (('removed', {k: v for k, v in good.items() if k != name}),
                              ('altered', {**good, name: 'http://203.0.113.1:8080'})):
                with self.subTest(name=name, case=case), self.assertRaises(ValueError):
                    launch.check_environment(env, home, tmp, 'not-owners-sitting')
            with self.subTest(name=name, case="present for an owner's sitting"), self.assertRaises(ValueError):
                launch.check_environment({**owner, name: good[name]}, home, tmp, 'owners-sitting')

    def test_the_model_address_rule(self):
        accepted = ['http://127.0.0.1:9/v1', 'https://[::1]:8080', 'http://127.0.0.1', 'http://127.0.0.1:65535/a-b_c.~/d']
        refused = ['', ' ', 'http://localhost:9', 'http://10.0.0.1:9', 'http://127.0.0.1:0', 'http://127.0.0.1:70000',
                   'http://127.0.0.1:09', 'http://127.0.0.1:9/v1?x=1', 'http://user@127.0.0.1:9', 'http://127.0.0.1:9#f',
                   ' http://127.0.0.1:9', 'http://127.0.0.1:9/' + 'a' * 2030, 'ftp://127.0.0.1']
        for value in accepted:
            self.assertEqual(launch.check_model_address(value), value)
        for value in refused:
            with self.subTest(value[:40]), self.assertRaises(ValueError):
                launch.check_model_address(value)


class Housekeeping(unittest.TestCase):
    def test_the_real_home_is_the_account_home_not_the_home_variable(self):
        with mock.patch.dict(os.environ, {'HOME': '/invented/elsewhere'}):
            self.assertEqual(launch.real_home(), Path(os.path.realpath(pwd.getpwuid(os.getuid()).pw_dir)))

    def test_the_cut_commands_are_gone(self):
        for command in ('stop', 'remove'):
            with self.subTest(command), contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                launch.main([command])
        for name in ('stop', 'remove', 'delete_tree', 'answer_requests'):
            self.assertFalse(hasattr(launch, name), name)

    def test_running_the_helper_writes_no_bytecode(self):
        prefix = Path(tempfile.mkdtemp(dir=_PRIVATE_TMP))
        self.addCleanup(remove_fixture, prefix)
        env = {k: v for k, v in os.environ.items() if k != 'PYTHONDONTWRITEBYTECODE'}
        env['PYTHONPYCACHEPREFIX'] = str(prefix)
        subprocess.run([sys.executable, str(HELPER), '--help'], env=env, check=True, capture_output=True)
        written = [f for _, _, files in os.walk(prefix) for f in files]
        self.assertEqual([f for f in written if f.startswith(('identify.', 'bundled_supplier.', 'launch.'))], [])


if __name__ == '__main__':
    unittest.main()
