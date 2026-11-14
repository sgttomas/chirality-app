"""The examination launcher for first launches on new homes under one homes root, with invented material only.

A shell script plays the App; folders stand in for the real home, the homes
root and the per-user cache folder. Every fixture, including stand-in launch
folders, lives in a temporary folder under the account's home, outside any
checkout, and is removed by the test that made it. No test creates anything
under the real homes root. No App, window, socket or real home Library is
touched; nothing here launches a real build.
"""
import builtins
import contextlib
import errno
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
import stat
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
REAL_HOMES_ROOT = launch.homes_root  # the function itself, before any test replaces it
REAL_TOP_OF_SEARCH = launch.top_of_search  # likewise

MAC = sys.platform == 'darwin'
IDENTIFIER = 'dev.chirality.app-v4.candidate.invented'
PRODUCT = 'Chirality App v4 (development invented)'
EXECUTABLE = 'chirality-app-v4'
SECRET = 'invented-secret-7f3a'
INVENTED_SECRETS = {'ANTHROPIC_AUTH_TOKEN': 'invented-token-1', 'CLAUDE_CODE_MESSAGING_TOKEN': 'invented-token-2',
                    'SSH_AUTH_SOCK': '/invented/agent.sock', 'OPENAI_API_KEY': 'invented-key-3',
                    'CHIRALITY_CODEX_HOME': '/invented/codex-home', 'CHIRALITY_WORKSPACE': '/invented/workspace'}
PLAYS_THE_APP = '''env > "$HOME/received-env.txt"
mkdir -p "$HOME/Library/Application Support/{id}" "$HOME/Library/WebKit/{id}/WebsiteData" "$HOME/Library/Caches/{id}"
echo invented > "$HOME/Library/Application Support/{id}/state"
echo invented > "$HOME/Library/WebKit/{id}/WebsiteData/store"
'''
SHELL_OWN = {'PWD', 'SHLVL', '_', 'OLDPWD', '__CF_USER_TEXT_ENCODING'}  # set by /bin/sh or the macOS runtime itself
OVERRIDES = {**{n: v for n, (v, _) in launch.PROXY_OVERRIDES.items()}, launch.MODEL_ADDRESS: 'http://127.0.0.1:9/v1'}
CLEAN_RECORD_FIELDS = {'note', 'made_by', 'made_at', 'candidate_key', 'identifier', 'candidate_folder', 'bundle',
                       'launch_folder', 'home', 'project', 'git_marker_above', 'codex', 'address_override', 'environment_constructed_for_the_app',
                       'output', 'started_at', 'pid', 'ended_at', 'process_group_after_settle', 'disclosed',
                       'app_started', 'ended', 'real_library', 'signals_received', 'failures', 'outcome'}

_PRIVATE_TMP = None


def setUpModule():
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
    """Stands in for identification's own validation and check (which have their own tests)."""


def fd_path(fd):
    if MAC:
        import fcntl
        return os.fsdecode(fcntl.fcntl(fd, fcntl.F_GETPATH, bytes(1024)).split(b'\0', 1)[0])
    return os.readlink(f'/proc/self/fd/{fd}')


def identities(root):
    found = set()
    for current, _, _ in os.walk(root):
        info = os.stat(current)
        found.add((info.st_dev, info.st_ino))
    return found


class Fixture(unittest.TestCase):
    identification = staticmethod(fake_identification)

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(dir=_PRIVATE_TMP))
        self.addCleanup(remove_fixture, self.tmp)
        self.real = self.tmp / 'real-home'
        (self.real / 'Library/Preferences').mkdir(parents=True)
        (self.real / 'Library/Preferences/com.apple.dock.plist').write_bytes(b'invented system preference')
        self.cache = self.tmp / 'user-cache'
        self.cache.mkdir()
        self.root = self.tmp / 'homes-root'  # stands in for the homes root
        self.root.mkdir()
        patches = [mock.patch.object(launch, 'real_home', return_value=self.real),
                   mock.patch.object(launch, 'homes_root', return_value=self.root),
                   mock.patch.object(launch, 'top_of_search', return_value=self.tmp),  # not what lies above the fixture
                   mock.patch.object(launch, 'user_cache_dir', return_value=self.cache),
                   mock.patch.object(launch, 'SETTLE_SECONDS', 0.0)]
        if self.identification is not None:
            patches.append(mock.patch.object(launch, 'identify_candidate', self.identification))
        for patch in patches:
            patch.start()
            self.addCleanup(patch.stop)
        self.groups = []
        self.addCleanup(self.kill_groups)

    def kill_groups(self):
        for group in self.groups:
            with contextlib.suppress(ProcessLookupError, PermissionError):
                os.killpg(group, signal.SIGKILL)

    def candidate(self, script='', where='build', exit_status=0, shebang='#!/bin/sh', executable=EXECUTABLE,
                  plays=True, name=PRODUCT + '.app', record_name=None):
        root = self.tmp / where
        app = root.joinpath(*launch.BUNDLE_FOLDER, name)
        (app / 'Contents/MacOS').mkdir(parents=True)
        (app / 'Contents/Resources/instructions').mkdir(parents=True)
        (app / 'Contents/Resources/instructions/AGENTS.md').write_text('invented guidance\n')
        (app / 'Contents/Info.plist').write_bytes(plistlib.dumps({
            'CFBundleIdentifier': IDENTIFIER, 'CFBundleName': PRODUCT, 'CFBundleDisplayName': PRODUCT,
            'CFBundleExecutable': executable, 'CFBundleShortVersionString': '0.0.0'}))
        exe = app / 'Contents/MacOS' / executable
        exe.write_text(shebang + '\n' + (PLAYS_THE_APP.format(id=IDENTIFIER) if plays else '') + script
                       + f'exit {exit_status}\n')
        exe.chmod(0o755)
        record = {'candidate_key': '0123456789-abcdefabcdef',
                  'bundle': {'identifier': IDENTIFIER, 'name': record_name if record_name is not None else name,
                             'executable': {'path': 'Contents/MacOS/' + executable,
                                            'sha256': hashlib.sha256(exe.read_bytes()).hexdigest()}}}
        (root / 'identification').mkdir()
        (root / 'identification/candidate-identification.json').write_text(json.dumps(record))
        (root / 'identification' / launch.INVENTORY).write_text('{}')
        return root

    def folders(self):
        return set(self.root.glob('launch-*'))

    def run_helper(self, candidate, *extra):
        before = self.folders()
        code, out = self.call('launch', '--candidate', str(candidate), *extra)
        new = sorted(self.folders() - before)
        folder = new[0] if new else None
        saved = folder / launch.RECORD_FOLDER / launch.RECORD if folder else None
        record = json.loads(saved.read_text()) if saved and saved.exists() else None
        if record and record.get('pid'):
            self.groups.append(record['pid'])
        return code, record, out, folder

    def call(self, *argv):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = launch.main(list(argv))
        return code, out.getvalue() + err.getvalue()

    def received(self, record):
        lines = (Path(record['home']) / 'received-env.txt').read_text().splitlines()
        return dict(line.split('=', 1) for line in lines if '=' in line)

    def assert_refused(self, code, out, reason):
        self.assertEqual(code, 2, out)
        self.assertIn(reason, json.loads(out.strip().splitlines()[-1])['error'])


class EnvironmentFromNothing(Fixture):  # STATEMENT 1
    def test_the_child_receives_exactly_the_allowlist_with_the_nine_overrides(self):
        with mock.patch.dict(os.environ, {**INVENTED_SECRETS, 'LANG': 'fr_FR.UTF-8', 'USER': 'invented',
                                          'HTTPS_PROXY': 'http://invented.example:8080',
                                          launch.MODEL_ADDRESS: 'http://invented.example/v1'}):
            code, record, out, _ = self.run_helper(self.candidate())
        self.assertEqual(code, 0, out)
        env = self.received(record)
        home = record['home']
        self.assertEqual(set(env) - SHELL_OWN, set(launch.ALLOWED))
        for name, value in INVENTED_SECRETS.items():
            self.assertNotIn(name, env)
            self.assertNotIn(value, (Path(home) / 'received-env.txt').read_text())
        self.assertEqual((env['HOME'], env['CFFIXED_USER_HOME'], env['PATH'], env['LANG']),
                         (home, home, launch.SYSTEM_PATH, 'en_US.UTF-8'))
        self.assertTrue(env['TMPDIR'].startswith(home + '/.chirality-launch-tmp-'))
        self.assertEqual({n: env[n] for n in OVERRIDES}, OVERRIDES)
        self.assertEqual(record['environment_constructed_for_the_app'], {k: env[k] for k in launch.ALLOWED})

    def test_no_option_passes_another_name_and_the_nine_are_on_every_launch(self):
        candidate = self.candidate()
        for option in ('--app-env', '--owner-sitting', '--reuse', '--lang', '--settle-seconds', '--parent', '--run-dir',
                       '--label'):
            with self.subTest(option), contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                launch.main(['launch', '--candidate', str(candidate), option, 'x'])
        for extra in ((), ('--model-address', 'http://127.0.0.1:8080/v1')):
            with self.subTest(extra=extra):
                code, record, out, _ = self.run_helper(candidate, *extra)
                env = self.received(record)
                self.assertEqual(set(env) - SHELL_OWN, set(launch.ALLOWED))
                for name, (value, _) in launch.PROXY_OVERRIDES.items():
                    self.assertEqual(env[name], value)
                self.assertIn(launch.MODEL_ADDRESS, env)

    def test_the_exact_mapping_is_checked_immediately_before_the_start(self):
        home, tmp = self.tmp / 'h', '.chirality-launch-tmp-x'
        good = launch.child_environment(home, tmp, launch.DEFAULT_MODEL_ADDRESS)
        launch.check_environment(good, home, tmp)
        cases = {'an added name': {**good, 'SSH_AUTH_SOCK': '/x'},
                 'HOME alone': {k: v for k, v in good.items() if k != 'CFFIXED_USER_HOME'},
                 'homes differ': {**good, 'CFFIXED_USER_HOME': str(self.tmp / 'other')},
                 'TMPDIR elsewhere': {**good, 'TMPDIR': str(home / 'other')},
                 'other PATH': {**good, 'PATH': '/opt/x:' + launch.SYSTEM_PATH},
                 'other LANG': {**good, 'LANG': 'fr_FR.UTF-8'}}
        for name in OVERRIDES:
            cases[f'{name} removed'] = {k: v for k, v in good.items() if k != name}
            cases[f'{name} altered'] = {**good, name: 'http://203.0.113.1:8080'}
        for name, env in cases.items():
            with self.subTest(name), self.assertRaises(ValueError):
                launch.check_environment(env, home, tmp)
        built = launch.child_environment
        with mock.patch.object(launch, 'child_environment', lambda *a: {**built(*a), 'SSH_AUTH_SOCK': '/x'}):
            code, record, _, _ = self.run_helper(self.candidate(where='added'))
        self.assertEqual((code, record['outcome'], record['app_started']), (2, 'not launched', 'not started'))
        self.assertFalse((Path(record['home']) / 'received-env.txt').exists())


class CleanRun(Fixture):  # STATEMENTS 2 and 3
    def test_a_clean_run_records_exactly_the_tabled_fields_in_its_record_folder(self):
        code, record, out, folder = self.run_helper(self.candidate())
        self.assertEqual((code, record['outcome']), (0, 'clean'), out)
        self.assertEqual(set(record), CLEAN_RECORD_FIELDS)
        self.assertEqual(set(record['disclosed']), {'preferences', 'user_cache'})
        self.assertEqual((record['real_library']['result'], record['signals_received'], record['app_started']),
                         ('unchanged', [], 'started'))
        self.assertEqual(record['codex'], launch.CODEX_NOTE)
        self.assertEqual(sorted(os.listdir(folder)), [launch.HOME, launch.PROJECT, launch.RECORD_FOLDER])
        self.assertEqual(os.listdir(folder / launch.RECORD_FOLDER), [launch.RECORD])

    def test_links_at_or_beneath_a_watched_place_make_the_comparison_incomplete(self):
        lib = self.real / 'Library'
        outside = self.tmp / 'outside'
        (outside / IDENTIFIER).mkdir(parents=True)
        (lib / 'Caches').symlink_to(outside)
        code, record, out, _ = self.run_helper(self.candidate(f'echo b >> "{lib}/Caches/{IDENTIFIER}/f"\n'))
        self.assertEqual((code, record['outcome'], record['real_library']['result']), (1, 'failed', 'incomplete'), out)

    def test_failed_starts_exits_listings_and_lingering_processes_are_never_clean(self):
        cases = {'exit status 3': (dict(exit_status=3), None, 1),
                 'does not start': (dict(shebang='#!/nonexistent/interpreter'), None, 1),
                 'process left in the group': (dict(script='sleep 5 &\n'), None, 1),
                 'after-listing fails': ({}, 'after', 1),
                 'before-listing fails': ({}, 'before', 2)}
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
        for name, script, undo in (('made unreadable by the run', f'chmod 000 "{lib}"\n', lambda: lib.chmod(0o700)),
                                   ('an ancestor made unexaminable', f'chmod 000 "{self.real}"\n',
                                    lambda: self.real.chmod(0o700))):
            with self.subTest(name):
                try:
                    code, record, out, _ = self.run_helper(self.candidate(script, where=name.replace(' ', '-')))
                finally:
                    undo()
                self.assertEqual((code, record['real_library']['result']), (1, 'not made'), out)

    def test_a_before_listing_that_cannot_be_made_refuses_and_names_the_place(self):
        (self.real / 'Library/Logs').mkdir()
        (self.real / 'Library/Logs').chmod(0o000)
        self.addCleanup((self.real / 'Library/Logs').chmod, 0o700)
        code, record, out, folder = self.run_helper(self.candidate())
        self.assertEqual((code, record['outcome'], record['app_started']), (2, 'not launched', 'not started'), out)
        self.assertEqual(record['ended'], 'not launched: the before-listing could not be made (PermissionError at Logs)')

    def test_the_two_protected_folders_are_not_watched_so_a_refused_listing_of_them_does_not_stop_a_launch(self):
        for name in ('Cookies', 'Autosave Information'):
            self.assertNotIn(name, launch.WATCHED)
            (self.real / 'Library' / name).mkdir()
            (self.real / 'Library' / name).chmod(0o000)
            self.addCleanup((self.real / 'Library' / name).chmod, 0o700)
        code, record, out, folder = self.run_helper(self.candidate())
        self.assertEqual((code, record['outcome'], record['real_library']['result']), (0, 'clean', 'unchanged'), out)

    def test_an_interrupted_record_write_leaves_no_record_and_an_empty_record_folder(self):
        with mock.patch.object(launch.os, 'link', side_effect=OSError(28, 'No space left on device')):
            code, record, out, folder = self.run_helper(self.candidate())
        self.assertIsNone(record)
        self.assertEqual(code, 2)
        self.assertTrue(all(n.startswith('.' + launch.RECORD + '.partial-')
                            for n in os.listdir(folder / launch.RECORD_FOLDER)))

    def test_a_signal_received_before_the_outcome_is_fixed_makes_the_run_not_clean(self):
        for step in ('while the App runs', 'settle', 'compare'):
            with self.subTest(step):
                script = "trap 'exit 0' TERM\nwhile :; do sleep 0.1; done\n" if step == 'while the App runs' else ''
                candidate = self.candidate(script, where=step.replace(' ', '-'))
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
                thread = None
                if step == 'while the App runs':
                    def later():
                        deadline = time.monotonic() + 10
                        while time.monotonic() < deadline and not list(self.root.glob('launch-*/home/received-env.txt')):
                            real_sleep(0.05)
                        real_sleep(0.3)
                        if launch._forwarding.is_set():
                            sent.append(1)
                            os.kill(os.getpid(), signal.SIGTERM)
                    thread = threading.Thread(target=later)
                    thread.start()
                with mock.patch.object(launch, 'compare', compare), mock.patch.object(launch.time, 'sleep', sleep):
                    code, record, out, _ = self.run_helper(candidate)
                if thread:
                    thread.join()
                self.assertEqual(sent, [1])
                self.assertEqual((code, record['outcome'], len(record['signals_received'])), (1, 'failed', 1), out)
                if step == 'while the App runs':  # the record says so in the launcher's words
                    self.assertRegex(record['ended'], r'^(exited with status 0|ended by signal 15 \(SIGTERM\)); '
                                     r'the launcher attempted to pass a termination to the App$')
                    self.assertEqual(record['process_group_after_settle'], 'gone')
                else:  # the App had already ended by itself: nothing was passed to it
                    self.assertEqual(record['ended'], 'exited with status 0')

    def test_the_record_does_not_say_when_a_signal_arrived(self):
        real_popen, real_sleep = subprocess.Popen, launch.time.sleep
        # A signal that arrives after the last check before the start, and before the process exists.
        def popen(*args, **kwargs):
            os.kill(os.getpid(), signal.SIGTERM)
            real_sleep(0.05)
            return real_popen(*args, **kwargs)
        script = "trap 'exit 0' TERM\nwhile :; do sleep 0.1; done\n"
        with mock.patch.object(launch.subprocess, 'Popen', popen):
            code, record, out, _ = self.run_helper(self.candidate(script, where='before-the-process'))
        self.assertEqual((code, record['outcome'], [s['signal'] for s in record['signals_received']]), (1, 'failed', ['SIGTERM']), out)
        self.assertEqual(record['app_started'], 'started')  # the process was created, and then signalled
        self.assertIsInstance(record['pid'], int)
        self.assertRegex(record['ended'], r'^(exited with status 0|ended by signal 15 \(SIGTERM\)); '
                         r'the launcher attempted to pass a termination to the App$')
        self.assertNotIn('while the App ran', record['ended'])
        # One signal while the App runs, and another during the settle time, after the App has exited.
        sent = []

        def sleep(seconds):
            if sent == ['running']:
                sent.append('settle')
                os.kill(os.getpid(), signal.SIGINT)
                real_sleep(0.05)
            return real_sleep(seconds)

        def later():
            deadline = time.monotonic() + 10
            while time.monotonic() < deadline and not list(self.root.glob('launch-*/home/started-twice')):
                real_sleep(0.05)
            if launch._forwarding.is_set():
                sent.append('running')
                os.kill(os.getpid(), signal.SIGTERM)
        # The trap is set before the file that says the App runs, so the signal sent on seeing the file can only meet
        # the trap: the App then exits 0, the one ending asserted below.
        script = "trap 'exit 0' TERM\ntouch \"$HOME/started-twice\"\nwhile :; do sleep 0.1; done\n"
        thread = threading.Thread(target=later)
        thread.start()
        with mock.patch.object(launch.time, 'sleep', sleep):
            code, record, out, _ = self.run_helper(self.candidate(script, where='two-signals'))
        thread.join()
        self.assertEqual(sent, ['running', 'settle'], out)
        self.assertEqual((code, record['outcome'], [s['signal'] for s in record['signals_received']]),
                         (1, 'failed', ['SIGTERM', 'SIGINT']), out)
        self.assertEqual(record['ended'], 'exited with status 0; the launcher attempted to pass a termination to the App')
        self.assertEqual(record['process_group_after_settle'], 'gone')

    def test_ended_repeats_no_signal_so_one_received_during_the_after_listings_cannot_be_missing_from_it(self):
        real_listing, real_sleep = launch.listing, launch.time.sleep
        sent = []

        def listing(*args, **kwargs):  # the before-listing is the first call; the after-listings follow the App's exit
            if sent == ['running']:
                sent.append('after-listing')
                os.kill(os.getpid(), signal.SIGHUP)
                real_sleep(0.05)
            return real_listing(*args, **kwargs)

        def later():
            deadline = time.monotonic() + 10
            while time.monotonic() < deadline and not list(self.root.glob('launch-*/home/started-here')):
                real_sleep(0.05)
            if launch._forwarding.is_set():
                sent.append('running')
                os.kill(os.getpid(), signal.SIGTERM)
        # The trap first, as above: the signal sent on seeing the file can only meet it.
        script = 'trap \'exit 0\' TERM\ntouch "$HOME/started-here"\nwhile :; do sleep 0.1; done\n'
        thread = threading.Thread(target=later)
        thread.start()
        with mock.patch.object(launch, 'listing', listing):
            code, record, out, _ = self.run_helper(self.candidate(script, where='signal-during-after-listing'))
        thread.join()
        self.assertEqual(sent, ['running', 'after-listing'], out)
        self.assertEqual((code, record['outcome']), (1, 'failed'), out)
        self.assertEqual([s['signal'] for s in record['signals_received']], ['SIGTERM', 'SIGHUP'])  # every signal is here
        self.assertEqual(record['ended'], 'exited with status 0; the launcher attempted to pass a termination to the App')
        for name in ('SIGTERM', 'SIGHUP', 'SIGINT', 'process group', 'settle'):
            self.assertNotIn(name, record['ended'].split('; ', 1)[1])


KILLED_RUNNER = '''
import importlib.util, json, sys, time
from pathlib import Path
from unittest import mock
spec = importlib.util.spec_from_file_location('launch_under_test', sys.argv[1])
launch = importlib.util.module_from_spec(spec)
spec.loader.exec_module(launch)
stage, real, cache, root, sentinel = sys.argv[2], Path(sys.argv[3]), Path(sys.argv[4]), Path(sys.argv[5]), Path(sys.argv[6])
def reached(*args, **kwargs):
    sentinel.write_text('reached')
    time.sleep(60)
patches = [mock.patch.object(launch, 'SETTLE_SECONDS', 0.0),
           mock.patch.object(launch, 'real_home', return_value=real),
           mock.patch.object(launch, 'homes_root', return_value=root),
           mock.patch.object(launch, 'user_cache_dir', return_value=cache),
           mock.patch.object(launch, 'identify_candidate', lambda app, record: None)]
if stage == 'before start':
    patches.append(mock.patch.object(launch, 'check_environment', reached))
if stage == 'finalizing':
    patches.append(mock.patch.object(launch, 'compare', reached))
for patch in patches:
    patch.start()
sys.exit(launch.main(sys.argv[7:]))
'''


class KilledLauncher(Fixture):  # STATEMENT 2: a killed launcher leaves no record
    def test_a_launcher_killed_at_each_stage_leaves_no_record(self):
        runner = self.tmp / 'runner.py'
        runner.write_text(KILLED_RUNNER)
        for stage in ('before start', 'running', 'finalizing'):
            with self.subTest(stage):
                slug = stage.replace(' ', '-')
                sentinel = self.tmp / f'sentinel-{slug}'
                script = f'echo $$ > "{sentinel}"\nsleep 60\n' if stage == 'running' else ''
                candidate = self.candidate(script, where=f'killed-{slug}', plays=False)
                before = self.folders()
                helper = subprocess.Popen([sys.executable, '-B', str(runner), str(HELPER), stage, str(self.real),
                                           str(self.cache), str(self.root), str(sentinel),
                                           'launch', '--candidate', str(candidate)],
                                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                try:  # an interrupted test skips unittest's cleanups, so the helper is ended here whatever happens
                    deadline = time.monotonic() + 20
                    while not (sentinel.exists() and sentinel.read_text().strip()) and time.monotonic() < deadline:
                        time.sleep(0.05)
                    self.assertTrue(sentinel.exists())
                finally:
                    helper.kill()
                    helper.wait()
                    if stage == 'running':
                        with contextlib.suppress(OSError, ValueError, ProcessLookupError, PermissionError):
                            os.killpg(int(sentinel.read_text().strip()), signal.SIGKILL)
                [folder] = sorted(self.folders() - before)
                for name in os.listdir(folder / launch.RECORD_FOLDER):
                    self.assertTrue(name.startswith('.' + launch.RECORD + '.partial-'), name)


@contextlib.contextmanager
def touches(names=(), dirs=()):
    """Instrumentation, lexical and resolved: every open, listing or stat whose path or last component is one of
    `names`, or that is one of `dirs` or lies under one (exclusive write-only creation is not counted)."""
    dirs = [os.path.realpath(d) for d in dirs]
    touched = []

    def hit(text, raw):
        if text is None:
            return False
        return (os.path.basename(raw) in names or raw in names
                or any(text == d or text.startswith(d + os.sep) for d in dirs))

    def resolve(path, dir_fd):
        if isinstance(path, int):
            try:
                return fd_path(path), ''
            except OSError:  # a descriptor with no path (a pipe): not a touch of any watched place
                return None, ''
        raw = os.fsdecode(path)
        if dir_fd is not None and not os.path.isabs(raw):
            return os.path.normpath(os.path.join(fd_path(dir_fd), raw)), raw
        return os.path.abspath(raw), raw

    real = {name: getattr(os, name) for name in ('listdir', 'scandir', 'stat', 'lstat', 'fstat', 'readlink', 'open')}

    def wrap(name):
        def spied(*args, **kwargs):
            lexical, raw = resolve(args[0] if args else kwargs.get('path', '.'), kwargs.get('dir_fd'))
            flags = (args[1] if len(args) > 1 else kwargs.get('flags', 0)) if name == 'open' else 0
            creating = name == 'open' and flags & os.O_ACCMODE == os.O_WRONLY and flags & os.O_CREAT and flags & os.O_EXCL
            if not creating and hit(lexical, raw):
                touched.append((name, lexical))
            return real[name](*args, **kwargs)
        return spied
    real_open = builtins.open

    def spied_open(file, *args, **kwargs):
        if not isinstance(file, int) and hit(os.path.abspath(os.fsdecode(file)), os.fsdecode(file)):
            touched.append(('open', file))
        return real_open(file, *args, **kwargs)
    with contextlib.ExitStack() as stack:
        for name in real:
            stack.enter_context(mock.patch.object(os, name, wrap(name)))
        stack.enter_context(mock.patch.object(builtins, 'open', spied_open))
        stack.enter_context(mock.patch.object(io, 'open', spied_open))
        yield touched


class TheHomesRoot(Fixture):  # the root: existing, the user's, reached without links; never created
    def test_without_the_root_the_launcher_refuses_before_creating_anything(self):
        candidate = self.candidate()
        stand_in_real_home = self.tmp / 'another-real-home'
        stand_in_real_home.mkdir()
        target = self.tmp / 'elsewhere'
        target.mkdir()
        for name, setup in (('absent', lambda: None),
                            ('a link', lambda: (stand_in_real_home.joinpath(*launch.HOMES_ROOT[:-1]).mkdir(parents=True),
                                                stand_in_real_home.joinpath(*launch.HOMES_ROOT).symlink_to(target)))):
            with self.subTest(name), mock.patch.object(launch, 'homes_root', REAL_HOMES_ROOT), \
                    mock.patch.object(launch, 'real_home', return_value=stand_in_real_home):
                setup()
                before = identities(self.tmp)
                code, out = self.call('launch', '--candidate', str(candidate))
                self.assert_refused(code, out, 'the homes root')
                self.assertEqual(identities(self.tmp), before)
                self.assertEqual(os.listdir(target), [])

    def test_the_real_root_function_is_under_the_account_home(self):
        with mock.patch.object(launch, 'real_home', return_value=Path('/invented/account-home')):
            self.assertEqual(REAL_HOMES_ROOT(), Path('/invented/account-home/dev/chirality-t3/scratch/app/homes/examination'))


class NewHomeOnly(Fixture):  # the home is new: exclusive creates under the root's handle
    def test_a_normal_run_launches_into_a_home_that_did_not_exist_before(self):
        (self.root / launch.new_folder_name()).mkdir()  # an earlier launch folder
        before = identities(self.tmp)
        with touches(dirs=[str(self.root)]) as touched:
            code, record, out, folder = self.run_helper(self.candidate())
        self.assertEqual(code, 0, out)
        home = os.stat(record['home'])
        self.assertNotIn((home.st_dev, home.st_ino), before)
        self.assertEqual([t for t in touched if str(t[1]).startswith(record['home'] + os.sep)], [])

    def test_a_launch_folder_name_that_already_exists_in_any_spelling_is_refused_by_the_create(self):
        name = launch.new_folder_name()
        (self.tmp / 'CaseProbe').write_text('')
        spellings = [name] + ([name.upper()] if (self.tmp / 'caseprobe').exists() else [])
        for spelling in spellings:
            with self.subTest(spelling):
                (self.root / spelling / launch.HOME).mkdir(parents=True)
                (self.root / spelling / launch.HOME / 'kept').write_text(SECRET)
                before = identities(self.root)
                with mock.patch.object(launch, 'new_folder_name', return_value=name):
                    code, out = self.call('launch', '--candidate', str(self.candidate(where=f'c-{len(spelling)}-'
                                                                                        f'{spelling == name}')))
                self.assert_refused(code, out, 'could not be created: something already exists there')
                self.assertEqual(identities(self.root), before)
                self.assertFalse((self.root / spelling / launch.HOME / 'received-env.txt').exists())
                shutil.rmtree(self.root / spelling)


    def test_each_create_inside_the_launch_folder_is_exclusive_and_its_failure_launches_nothing(self):
        real_mkdir = os.mkdir
        for child in (launch.HOME, launch.RECORD_FOLDER, launch.PROJECT):
            for name, failure in (('something already there', None), ('no space', OSError(errno.ENOSPC, 'invented'))):
                with self.subTest(child=child, case=name):
                    def mkdir(path, mode=0o777, *, dir_fd=None):
                        if path == child and dir_fd is not None:
                            if failure is not None:
                                raise failure
                            real_mkdir(path, 0o700, dir_fd=dir_fd)  # something else made it first
                        return real_mkdir(path, mode, dir_fd=dir_fd)
                    before = self.folders()
                    candidate = self.candidate(where=f'create-{child}-{failure is None}')
                    with mock.patch.object(os, 'mkdir', mkdir):
                        code, out = self.call('launch', '--candidate', str(candidate))
                    self.assertEqual(code, 2, out)
                    if failure is None:
                        self.assert_refused(code, out, f'{child}/ could not be created: something already exists there')
                    [folder] = sorted(self.folders() - before)
                    self.assertFalse((folder / launch.HOME / 'received-env.txt').exists())  # the App never ran
                    self.assertFalse((folder / launch.RECORD_FOLDER / launch.RECORD).exists())  # and no record says it did


class NothingAbove(Fixture):  # the project folder, no .git entry above, and what the home holds at the start
    def test_the_project_folder_is_new_empty_beside_the_home_and_named_in_the_record(self):
        code, record, out, folder = self.run_helper(self.candidate())
        self.assertEqual((code, record['outcome']), (0, 'clean'), out)
        self.assertEqual(record['project'], str(folder / launch.PROJECT))
        self.assertEqual(Path(record['project']).parent, Path(record['home']).parent)
        self.assertEqual(os.listdir(record['project']), [])
        self.assertEqual(stat.S_IMODE(os.stat(record['project']).st_mode), 0o700)
        self.assertIn('none: ', record['git_marker_above'])

    def test_a_git_entry_in_any_folder_above_refuses_and_the_refusal_names_the_folder(self):
        real_mkdir = os.mkdir
        for place in ('the launch folder', 'the homes root', 'above the homes root'):
            for kind in ('a folder', 'a file', 'a link to nothing'):
                with self.subTest(place=place, kind=kind):
                    def put(folder):
                        marker = Path(folder) / '.git'
                        if kind == 'a folder':
                            marker.mkdir()
                        elif kind == 'a file':
                            marker.write_text('gitdir: /invented/elsewhere')
                        else:
                            marker.symlink_to('/invented/nowhere')
                        return marker

                    def take_away(marker):
                        if marker is not None and os.path.lexists(marker):
                            marker.rmdir() if marker.is_dir() and not marker.is_symlink() else marker.unlink()

                    def mkdir(path, mode=0o777, *, dir_fd=None):  # the entry appears in the new launch folder
                        result = real_mkdir(path, mode, dir_fd=dir_fd)
                        if path == launch.PROJECT and dir_fd is not None:
                            put(fd_path(dir_fd))
                        return result
                    marker = None if place == 'the launch folder' else put(self.root if place == 'the homes root' else self.tmp)
                    candidate = self.candidate(where=f'above-{place}-{kind}'.replace(' ', '-'))
                    try:
                        with mock.patch.object(os, 'mkdir', mkdir if place == 'the launch folder' else real_mkdir):
                            code, record, out, folder = self.run_helper(candidate)
                    finally:
                        take_away(marker)
                    holder = str(folder if place == 'the launch folder' else marker.parent)
                    self.assertEqual((code, record['outcome'], record['app_started']), (2, 'not launched', 'not started'), out)
                    self.assertIn(f'{holder} holds a .git entry', record['ended'])
                    self.assertNotIn('git_marker_above', record)
                    self.assertFalse((Path(record['home']) / 'received-env.txt').exists())
                    self.assertEqual(os.listdir(record['project']), [])

    def test_the_search_asks_by_lstat_alone_goes_to_the_top_and_stops_there(self):
        self.assertEqual(REAL_TOP_OF_SEARCH(), Path('/'))
        (self.tmp.parent / '.git').mkdir()  # above the fixture's top: never asked
        self.addCleanup((self.tmp.parent / '.git').rmdir)
        with touches(names=('.git',)) as touched:
            code, record, out, folder = self.run_helper(self.candidate())
        self.assertEqual((code, record['outcome']), (0, 'clean'), out)
        asked = [Path(path).parent for name, path in touched]
        self.assertEqual({name for name, path in touched}, {'lstat'})
        self.assertEqual(asked, [folder, self.root, self.tmp])  # the launch folder, the root, the top; each once
        self.assertEqual(record['git_marker_above'], 'none: 3 folders above the home and the project folder asked by presence')

    def test_a_folder_that_cannot_be_asked_refuses_and_is_named(self):
        real_lstat = os.lstat

        def lstat(path, *args, **kwargs):
            if os.fspath(path) == str(self.root / '.git'):
                raise PermissionError(errno.EACCES, 'invented')
            return real_lstat(path, *args, **kwargs)
        with mock.patch.object(os, 'lstat', lstat):
            code, record, out, folder = self.run_helper(self.candidate())
        self.assertEqual((code, record['outcome'], record['app_started']), (2, 'not launched', 'not started'), out)
        self.assertIn(f'{self.root} could not be checked for a .git entry (PermissionError)', record['ended'])
        self.assertFalse((Path(record['home']) / 'received-env.txt').exists())

    def test_home_names_the_home_allocated_for_this_launch_and_nothing_else(self):
        home, other = self.tmp / 'invented-home', self.tmp / 'another-home'
        other.mkdir()
        (other / 'kept').write_text('something already here')
        good = launch.child_environment(home, 'tmp', launch.DEFAULT_MODEL_ADDRESS)
        launch.check_environment(dict(good), home, 'tmp')
        for name in ('HOME', 'CFFIXED_USER_HOME'):
            for case, change, said in (
                    ('unset', lambda env: env.pop(name), f'^{name} is unset or empty'),
                    ('empty', lambda env: env.update({name: ''}), f'^{name} is unset or empty'),
                    ('another folder', lambda env: env.update({name: str(other)}), f'^{name} does not name the home'),
                    ('the account home', lambda env: env.update({name: str(self.real)}), f'^{name} does not name the home')):
                with self.subTest(name=name, case=case):
                    env = dict(good)
                    change(env)
                    with self.assertRaisesRegex(launch.Refusal, said):
                        launch.check_environment(env, home, 'tmp')
        both = {**good, 'HOME': str(other), 'CFFIXED_USER_HOME': str(other), 'TMPDIR': str(other / 'tmp')}
        with self.assertRaisesRegex(launch.Refusal, '^HOME does not name the home'):
            launch.check_environment(both, home, 'tmp')  # the two agree with each other and are still refused
        real = launch.child_environment
        for case, change in (('empty', {'HOME': ''}),
                             ('another folder', {'HOME': str(other), 'CFFIXED_USER_HOME': str(other)}),
                             ('the frameworks home alone another folder', {'CFFIXED_USER_HOME': str(other)})):
            with self.subTest(run=case), mock.patch.object(launch, 'child_environment', lambda *a: {**real(*a), **change}):
                code, record, out, folder = self.run_helper(self.candidate(where='home-' + case.replace(' ', '-')))
                self.assertEqual((code, record['outcome'], record['app_started']), (2, 'not launched', 'not started'), out)
                self.assertIn('HOME ', record['ended'])
                self.assertFalse((Path(record['home']) / 'received-env.txt').exists())
                self.assertEqual(os.listdir(other), ['kept'])

    def test_the_folder_home_names_is_the_directory_the_launcher_holds(self):
        real_listing = launch.listing
        moved = {}

        def swap(case):
            def listing(*args, **kwargs):  # after the allocation, before the start
                [folder] = self.folders()
                home = folder / launch.HOME
                if not moved.get(case):
                    moved[case] = True
                    home.rename(folder / 'home-moved-aside')
                    if case == 'another folder at the same name':
                        home.mkdir()
                    elif case == 'a link to the allocated one':
                        home.symlink_to(folder / 'home-moved-aside')
                return real_listing(*args, **kwargs)
            return listing
        for case, said in (('another folder at the same name', 'is not the directory allocated for this launch'),
                           ('a link to the allocated one', 'is not the directory allocated for this launch'),
                           ('nothing at the name', 'could not be checked (FileNotFoundError)')):
            with self.subTest(case), mock.patch.object(launch, 'listing', swap(case)):
                code, record, out, folder = self.run_helper(self.candidate(where='swap-' + case.replace(' ', '-')))
                self.assertEqual((code, record['outcome'], record['app_started']), (2, 'not launched', 'not started'), out)
                self.assertIn('the folder HOME names ' + said, record['ended'])
                self.assertFalse(any(folder.rglob('received-env.txt')))
                shutil.rmtree(folder)

    def test_home_is_an_absolute_path(self):
        with self.assertRaisesRegex(launch.Refusal, 'not an absolute path'), mock.patch.object(
                launch.os, 'stat', lambda *a, **k: os.fstat(os.open(self.tmp, os.O_RDONLY))), \
                mock.patch.object(launch, '_ident', lambda fd: (os.stat(self.tmp).st_dev, os.stat(self.tmp).st_ino)):
            launch.check_home({'HOME': 'relative/home'}, None)
        self.assertTrue(os.path.isabs(str(REAL_HOMES_ROOT())))

    def test_the_mapping_carries_no_codex_home_variable(self):
        home = self.tmp / 'invented-home'
        good = launch.child_environment(home, 'tmp', launch.DEFAULT_MODEL_ADDRESS)
        for name in ('CODEX_HOME', 'CHIRALITY_CODEX_HOME', 'CODEX_SQLITE_HOME', 'CHIRALITY_WORKSPACE'):
            with self.subTest(name):
                self.assertNotIn(name, launch.ALLOWED)
                self.assertNotIn(name, good)
                for value in (str(home / 'codex-home'), '/invented/elsewhere'):
                    with self.assertRaisesRegex(launch.Refusal, 'outside the allowlist'):
                        launch.check_environment({**good, name: value}, home, 'tmp')

    def test_at_the_start_the_home_holds_only_the_launchers_two_entries_and_is_the_working_folder(self):
        seen = self.tmp / 'seen-at-start.txt'
        script = f'pwd > "{seen}"\nls -A "$HOME" >> "{seen}"\n'
        code, record, out, folder = self.run_helper(self.candidate(script, plays=False))
        self.assertEqual((code, record['outcome']), (0, 'clean'), out)
        working, *names = seen.read_text().splitlines()
        self.assertEqual(os.path.realpath(working), os.path.realpath(record['home']))
        self.assertEqual(len(names), 2, names)
        self.assertEqual(sorted(name.rsplit('-', 1)[0] for name in names),
                         ['.chirality-launch-output', '.chirality-launch-tmp'])
        self.assertEqual(set(names) & {'.codex', '.agents', 'AGENTS.md', 'AGENTS.override.md', '.git'}, set())


class CandidateAdmission(Fixture):  # the only caller path
    def test_ambiguous_syntax_is_refused_before_normalisation(self):
        candidate = self.candidate()
        (self.tmp / 'linked').symlink_to(self.tmp / 'build')
        for name, text in (('".." through a link', f'{self.tmp}/linked/../build'), ('"."', f'{self.tmp}/./build'),
                           ('empty component', f'{self.tmp}//build'), ('trailing slash', f'{candidate}/'),
                           ('relative', 'build')):
            with self.subTest(name):
                code, out = self.call('launch', '--candidate', text)
                self.assert_refused(code, out, 'written ambiguously' if text.startswith('/') else 'absolute')
        self.assertEqual(self.folders(), set())

    def test_a_link_in_the_access_path_or_the_layout_is_refused(self):
        candidate = self.candidate()
        (self.tmp / 'aliased').symlink_to(candidate)
        self.assert_refused(*self.call('launch', '--candidate', str(self.tmp / 'aliased')), 'no link')
        outside = self.tmp / 'outside-identification'
        shutil.move(str(candidate / 'identification'), outside)
        (candidate / 'identification').symlink_to(outside)
        self.assert_refused(*self.call('launch', '--candidate', str(candidate)), 'identification folder')
        self.assertEqual(self.folders(), set())

    def test_a_candidate_under_the_homes_root_is_refused_by_identity_in_any_spelling(self):
        inner = self.candidate(where='homes-root/kept-candidate')
        spellings = [str(inner)]
        (self.tmp / 'CaseProbe').write_text('')
        if (self.tmp / 'caseprobe').exists():
            spellings.append(str(self.tmp / 'HOMES-ROOT' / 'kept-candidate'))
        for text in spellings:
            with self.subTest(text):
                with touches(dirs=[str(self.root / 'kept-candidate')]) as touched:
                    code, out = self.call('launch', '--candidate', text)
                self.assert_refused(code, out, 'under the homes root')
                self.assertEqual(touched, [])  # nothing beneath the root was examined
        self.assertEqual(self.folders(), set())

    def test_a_bundle_name_from_the_record_that_is_not_a_plain_name_is_refused_before_it_is_opened(self):
        for bad in ('../x.app', 'a/b.app', '.', '/absolute/x.app', '', 'x.notapp'):
            with self.subTest(bad):
                candidate = self.candidate(where=f'bad-{abs(hash(bad))}', record_name=bad)
                with touches(names=[n for n in (bad, 'x.app', 'b.app', 'a') if n not in ('', '.', '/')]) as touched:
                    code, out = self.call('launch', '--candidate', str(candidate))
                self.assert_refused(code, out, "the record's bundle name")
                self.assertEqual(touched, [])
        self.assertEqual(self.folders(), set())

    def test_a_bundle_folder_that_does_not_hold_exactly_the_records_bundle_is_refused(self):
        candidate = self.candidate(record_name='Other.app')
        self.assert_refused(*self.call('launch', '--candidate', str(candidate)), "exactly the record's bundle")
        candidate = self.candidate(where='two')
        candidate.joinpath(*launch.BUNDLE_FOLDER, 'Extra.app').mkdir()
        self.assert_refused(*self.call('launch', '--candidate', str(candidate)), "exactly the record's bundle")


class WatchedByExactName(Fixture):
    def test_an_executable_name_that_does_not_discriminate_is_refused(self):
        for index, name in enumerate(('a', 'app', 'chirality', 'Chirality-x')):
            with self.subTest(name):
                code, record, out, folder = self.run_helper(self.candidate(executable=name, where=f'short{index}'))
                self.assert_refused(code, out, 'does not discriminate')
                self.assertIsNone(folder)

    def test_the_rule_names_entries_exactly(self):
        helper = 'com.apple.WebKit.{}+chirality_app_v4-0a1b2c'
        for name in [IDENTIFIER, IDENTIFIER + '.plist', 'prefix.' + IDENTIFIER, EXECUTABLE, 'Chirality-App-V4',
                     helper.format('Networking'), helper.format('WebContent'), helper.format('GPU')]:
            self.assertTrue(launch.watched_name(name, IDENTIFIER, EXECUTABLE), name)
        for name in [IDENTIFIER + '2', IDENTIFIER + '-other', EXECUTABLE + '.old', 'chirality-app',
                     'com.apple.WebKit.Networking+other_app-1', 'com.apple.spaces.plist']:
            self.assertFalse(launch.watched_name(name, IDENTIFIER, EXECUTABLE), name)

    def test_changed_preference_files_are_disclosed_whatever_their_names(self):
        prefs = self.real / 'Library/Preferences'
        code, record, out, _ = self.run_helper(self.candidate(
            f'echo x > "{prefs}/com.apple.spaces.plist"\necho y >> "{prefs}/com.apple.dock.plist"\n'))
        self.assertEqual((code, record['outcome']), (0, 'clean'), out)
        self.assertEqual({(c['path'], c['change']) for c in record['disclosed']['preferences']['changes']},
                         {('com.apple.spaces.plist', 'created'), ('com.apple.dock.plist', 'modified')})
        code, record, out, _ = self.run_helper(self.candidate(f'echo x > "{prefs}/{IDENTIFIER}.plist"\n', where='named'))
        self.assertEqual((code, record['real_library']['result']), (1, 'changed'), out)


class ObservationNotGate(Fixture):
    def test_the_per_user_cache_folder_is_disclosed_and_never_a_failure(self):
        helper = f'com.apple.WebKit.WebContent+{EXECUTABLE.replace("-", "_")}-0a1b'
        code, record, out, _ = self.run_helper(self.candidate(
            f'mkdir -p "{self.cache}/{helper}"\necho x > "{self.cache}/{helper}/data"\necho x > "{self.cache}/unrelated"\n'))
        self.assertEqual((code, record['outcome']), (0, 'clean'), out)
        self.assertEqual({(c['path'], c['change']) for c in record['disclosed']['user_cache']['changes']},
                         {(helper, 'created'), (helper + '/data', 'created')})

    def test_an_unexaminable_or_linked_cache_folder_neither_refuses_nor_reports_changes(self):
        link = self.tmp / 'cache-link'
        link.symlink_to(self.cache)
        for name, base, setup, undo in (('unreadable', self.cache, lambda: self.cache.chmod(0o000),
                                         lambda: self.cache.chmod(0o700)),
                                        ('a link', link, lambda: None, lambda: None)):
            with self.subTest(name), mock.patch.object(launch, 'user_cache_dir', return_value=base):
                setup()
                try:
                    code, record, out, _ = self.run_helper(self.candidate(where=name.replace(' ', '-')))
                finally:
                    undo()
                self.assertEqual((code, record['outcome']), (0, 'clean'), out)
                self.assertTrue(record['disclosed']['user_cache']['observation'].startswith('not observed'))
                self.assertNotIn('changes', record['disclosed']['user_cache'])


class AddressOverride(Fixture):
    def test_omitted_is_the_recorded_default_and_empty_or_blank_is_refused(self):
        candidate = self.candidate()
        code, record, out, _ = self.run_helper(candidate)
        self.assertEqual((record['address_override'], self.received(record)[launch.MODEL_ADDRESS]),
                         ('the default (nothing listens there)', launch.DEFAULT_MODEL_ADDRESS))
        for value in ('', '   '):
            with self.subTest(repr(value)):
                code, _, out, folder = self.run_helper(candidate, '--model-address', value)
                self.assert_refused(code, out, launch.MODEL_ADDRESS)
                self.assertIsNone(folder)
        code, record, out, _ = self.run_helper(candidate, '--model-address', 'http://127.0.0.1:8080/v1')
        self.assertEqual((record['address_override'], self.received(record)[launch.MODEL_ADDRESS]),
                         ('given by the caller', 'http://127.0.0.1:8080/v1'))

    def test_the_model_address_rule(self):
        for value in ['http://127.0.0.1:9/v1', 'https://[::1]:8080', 'http://127.0.0.1', 'http://127.0.0.1:65535/a-b_c.~/d']:
            self.assertEqual(launch.check_model_address(value), value)
        for value in ['', ' ', 'http://localhost:9', 'http://10.0.0.1:9', 'http://127.0.0.1:0', 'http://127.0.0.1:70000',
                      'http://127.0.0.1:09', 'http://127.0.0.1:9/v1?x=1', 'http://user@127.0.0.1:9', 'http://127.0.0.1:9#f',
                      ' http://127.0.0.1:9', 'http://127.0.0.1:9/' + 'a' * 2030, 'ftp://127.0.0.1']:
            with self.subTest(value[:40]), self.assertRaises(ValueError):
                launch.check_model_address(value)


class OnlyTheIdentifiedCandidate(Fixture):
    identification = None

    def record_path(self, candidate):
        return candidate / 'identification/candidate-identification.json'

    def test_an_invalid_record_is_refused_and_no_record_value_is_quoted(self):
        candidate = self.candidate()
        record = json.loads(self.record_path(candidate).read_text())
        for name, value in (('unknown format', {**record, 'format': 'invented/v9', 'candidate_key': SECRET}),
                            ('schema failure', {**record, 'format': identify.FORMAT, 'candidate_key': SECRET}),
                            ('empty candidate key', {**record, 'candidate_key': ''})):
            with self.subTest(name):
                self.record_path(candidate).write_text(json.dumps(value))
                code, out = self.call('launch', '--candidate', str(candidate))
                self.assertEqual(code, 2, out)
                self.assertNotIn(SECRET, out)
        self.assertEqual(self.folders(), set())

    def test_a_check_that_finds_a_difference_is_refused_by_counts_and_field_names(self):
        candidate = self.candidate()
        same = {'equal': True, 'build_identity': 'x', 'recorded_build_identity': 'x', 'record_fields_mismatched': []}
        for name, result in (('inventory differs', {**same, 'equal': False, 'missing': [SECRET]}),
                             ('identity differs', {**same, 'build_identity': 'y'}),
                             ('record fields differ', {**same, 'record_fields_mismatched': ['identifier']})):
            with self.subTest(name), mock.patch.object(identify, 'validate_record'), \
                    mock.patch.object(identify, 'check', return_value=result):
                code, out = self.call('launch', '--candidate', str(candidate))
                self.assert_refused(code, out, 'differs from its identification record')
                self.assertNotIn(SECRET, out)
        for error in (plistlib.InvalidFileException(), ExpatError('invented')):
            with self.subTest(type(error).__name__), mock.patch.object(identify, 'validate_record'), \
                    mock.patch.object(identify, 'check', side_effect=error):
                self.assertEqual(self.call('launch', '--candidate', str(candidate))[0], 2)

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
        code, out = self.call('launch', '--candidate', str(candidate))
        self.assert_refused(code, out, '1 changed')


class KeptHome(Fixture):  # keep-make, keep-launch and keep-remove: one home across launches, every network block on
    def setUp(self):
        super().setUp()
        patch = mock.patch.object(launch, 'running_candidates', return_value=[])
        patch.start()
        self.addCleanup(patch.stop)

    def make(self, candidate):
        code, out = self.call('keep-make', '--candidate', str(candidate))
        self.assertEqual(code, 0, out)
        return Path(json.loads(out)['kept_folder'])

    def test_one_home_is_launched_twice_with_the_environment_of_launch_and_a_numbered_record_each_time(self):
        candidate = self.candidate('echo "$((1 + $(cat "$HOME/launches" 2>/dev/null || echo 0)))" > "$HOME/launches"\n')
        folder = self.make(candidate)
        self.assertEqual(sorted(p.name for p in folder.iterdir()), ['home', 'project', 'record'])
        kept = json.loads((folder / 'record/kept.json').read_text())
        self.assertEqual((kept['folder'], kept['device'], kept['inode']), (str(folder), folder.stat().st_dev, folder.stat().st_ino))
        for number in (1, 2):
            code, out = self.call('keep-launch', '--folder', str(folder), '--candidate', str(candidate))
            record = json.loads((folder / f'record/launch-record-{number}.json').read_text())
            self.groups.append(record['pid'])
            self.assertEqual(record['home'], str(folder / 'home'))
            self.assertEqual((folder / 'home/launches').read_text().strip(), str(number))  # the same home, kept
        env = record['environment_constructed_for_the_app']
        self.assertEqual(set(env), set(launch.ALLOWED))  # the allowlist of launch, every proxy and the address on it
        self.assertTrue(all(env[name] == value for name, (value, _) in launch.PROXY_OVERRIDES.items()))
        self.assertEqual(env[launch.MODEL_ADDRESS], launch.DEFAULT_MODEL_ADDRESS)

    def test_a_kept_launch_is_refused_unless_every_condition_holds(self):
        candidate = self.candidate()
        folder = self.make(candidate)
        launch_folder = self.root / 'launch-20260101T000000Z-00000000'
        launch_folder.mkdir()
        kept = json.loads((folder / 'record/kept.json').read_text())
        cases = {
            'a folder not named kept-': (str(launch_folder), None, 'not a kept folder'),
            'a folder outside the homes root': (str(self.tmp / folder.name), None, 'not a kept folder'),
            'a record naming another folder': (str(folder), {**kept, 'inode': kept['inode'] + 1}, 'does not name this folder'),
            'an expired folder': (str(folder), {**kept, 'expires_at': '2000-01-01T00:00:00Z'}, 'expired'),
            'another candidate': (str(folder), {**kept, 'candidate_key': 'another'}, 'another candidate'),
        }
        for name, (given, record, reason) in cases.items():
            with self.subTest(name):
                saved = (folder / 'record/kept.json').read_text()
                if record is not None:
                    (folder / 'record/kept.json').write_text(json.dumps(record))
                try:
                    code, out = self.call('keep-launch', '--folder', given, '--candidate', str(candidate))
                finally:
                    (folder / 'record/kept.json').write_text(saved)
                self.assert_refused(code, out, reason)
                self.assertFalse(list((folder / 'record').glob('launch-record-*.json')))
        with mock.patch.object(launch, 'running_candidates', return_value=[{'pid': 1}]):
            code, out = self.call('keep-launch', '--folder', str(folder), '--candidate', str(candidate))
        self.assert_refused(code, out, 'already running')
        with self.assertRaises(SystemExit), contextlib.redirect_stderr(io.StringIO()):  # no address override: every block stays
            launch.main(['keep-launch', '--folder', str(folder), '--candidate', str(candidate), '--model-address', 'http://127.0.0.1:1/v1'])

    def test_a_test_build_carrying_the_scripted_driver_is_never_kept_or_launched(self):
        for marker in launch.DRIVER_MARKERS:
            with self.subTest(marker.decode()):
                candidate = self.candidate(f'# {marker.decode()}\n', where=f'marked-{marker.decode()[-6:]}')
                code, out = self.call('keep-make', '--candidate', str(candidate))
                self.assert_refused(code, out, 'test build carrying the scripted driver')
                self.assertFalse([p for p in self.root.iterdir() if p.name.startswith('kept-')])

    def test_remove_deletes_the_folder_whole_without_following_a_link_and_refuses_what_is_not_the_kept_folder(self):
        candidate = self.candidate()
        folder = self.make(candidate)
        outside = self.tmp / 'outside-file'
        outside.write_text('must stay')
        (folder / 'home/a-link').symlink_to(outside)
        (folder / 'project/deep/er').mkdir(parents=True)
        code, out = self.call('keep-remove', '--folder', str(self.tmp / folder.name))
        self.assert_refused(code, out, 'not a kept folder')
        code, out = self.call('keep-remove', '--folder', str(folder))
        self.assert_refused(code, out, 'needs the candidate')
        self.assertTrue(folder.exists())
        with mock.patch.object(launch, 'running_candidates', return_value=[{'pid': 1}]):
            code, out = self.call('keep-remove', '--folder', str(folder), '--candidate', str(candidate))
        self.assert_refused(code, out, 'still running')
        self.assertTrue(folder.exists())
        code, out = self.call('keep-remove', '--folder', str(folder), '--candidate', str(candidate))
        self.assertEqual(code, 0, out)
        self.assertFalse(folder.exists())
        self.assertEqual(outside.read_text(), 'must stay')


class Housekeeping(unittest.TestCase):
    def test_the_real_home_is_the_account_home_not_the_home_variable(self):
        with mock.patch.dict(os.environ, {'HOME': '/invented/elsewhere'}):
            self.assertEqual(launch.real_home(), Path(os.path.realpath(pwd.getpwuid(os.getuid()).pw_dir)))

    def test_the_removed_commands_and_machinery_are_gone(self):
        for command in ('stop', 'remove'):
            with self.subTest(command), contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                launch.main([command])
        for name in ('stop', 'remove', 'own_folder', 'claim', 'lock', 'in_use', 'read_own', 'APP_INPUTS', 'KINDS',
                     'refuse_launch_folder_ancestry', 'check_place', 'LAUNCH_FOLDER_NAME'):
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
