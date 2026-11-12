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

    def bundle(self, script='', identifier=IDENTIFIER, where='build', exit_status=0, shebang='#!/bin/sh',
               executable=EXECUTABLE, plays=True, name=PRODUCT + '.app'):
        app = self.tmp / where / name
        (app / 'Contents/MacOS').mkdir(parents=True)
        (app / 'Contents/Resources/instructions').mkdir(parents=True)
        (app / 'Contents/Resources/instructions/AGENTS.md').write_text('invented guidance\n')
        (app / 'Contents/Info.plist').write_bytes(plistlib.dumps({
            'CFBundleIdentifier': identifier, 'CFBundleName': PRODUCT, 'CFBundleDisplayName': PRODUCT,
            'CFBundleExecutable': executable, 'CFBundleShortVersionString': '0.0.0'}))
        body = shebang + '\n' + (PLAYS_THE_APP.format(id=identifier, secret=SECRET) if plays else '') + script
        body += f'exit {exit_status}\n'
        exe = app / 'Contents/MacOS' / executable
        exe.write_text(body)
        exe.chmod(0o755)
        record = {'candidate_key': '0123456789-abcdefabcdef',
                  'bundle': {'identifier': identifier, 'name': name,
                             'executable': {'path': 'Contents/MacOS/' + executable,
                                            'sha256': hashlib.sha256(exe.read_bytes()).hexdigest()}}}
        record_path = app.parent / 'candidate-identification.json'
        record_path.write_text(json.dumps(record))
        return app, record_path

    def argv(self, app, record, *extra, reuse=None, settle='0', run_dir=None, owner=False):
        argv = ['launch', '--app', str(app), '--record', str(record), '--run-dir', str(run_dir),
                '--settle-seconds', settle, *extra]
        argv += ['--reuse', str(reuse)] if reuse else ['--parent', str(self.parent)]
        return argv + (['--owner-sitting'] if owner else [])

    def run_helper(self, app, record, *extra, reuse=None, settle='0', run_dir=None, owner=False):
        self.runs += 1
        run_dir = Path(run_dir or self.tmp / f'run-{self.runs}')
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = launch.main(self.argv(app, record, *extra, reuse=reuse, settle=settle, run_dir=run_dir, owner=owner))
        saved = run_dir / launch.RECORD
        record = json.loads(saved.read_text()) if saved.exists() and not saved.is_symlink() else None
        if record and record.get('pid'):
            self.groups.append(record['pid'])
        return code, record, out.getvalue() + err.getvalue(), run_dir

    def call(self, *argv):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = launch.main(list(argv))
        return code, out.getvalue() + err.getvalue()

    def made(self, script='', owner=False, **options):
        app, record_path = self.bundle(script, where=f'made{self.runs}', **options)
        code, record, out, run_dir = self.run_helper(app, record_path, owner=owner)
        return app, record_path, Path(record['launch_folder']['launch_folder']), record

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
        """True once the helper accepts stops and has recorded the App's process."""
        if folder is None or not launch._forwarding.is_set():
            return False
        try:
            fd = os.open(folder / launch.CONTROL, launch.DIRECTORY)
            try:
                return launch.read_own(fd, launch.PROCESS, launch.PROCESS_FORMAT, 'p')['app_pid'] is not None
            finally:
                os.close(fd)
        except (OSError, ValueError):
            return False

    def in_background(self, act, folder=None):
        """Acts only once the helper confirmed its stop handling is installed and the App started; never otherwise."""
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
    def test_reviewer_child_receives_exactly_the_allowlist_while_the_helper_holds_tokens(self):
        app, record_path = self.bundle()
        with mock.patch.dict(os.environ, {**INVENTED_SECRETS, 'LANG': 'fr_FR.UTF-8', 'USER': 'invented',
                                          'HTTPS_PROXY': 'http://invented.example:8080'}):
            code, record, out, _ = self.run_helper(app, record_path, '--app-env', 'CHIRALITY_RECORDS_STORE=/invented/store')
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
        self.assertEqual((env['PATH'], env['LANG'], env['HTTPS_PROXY']),
                         (launch.SYSTEM_PATH, launch.DEFAULT_LANG, 'http://127.0.0.1:9'))
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
            'TMPDIR elsewhere': {**good, 'TMPDIR': str(self.parent / 'other')},
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
        app, record_path = self.bundle()
        built = launch.child_environment
        with mock.patch.object(launch, 'child_environment', lambda *a, **k: {**built(*a, **k), 'SSH_AUTH_SOCK': '/x'}):
            code, record, _, _ = self.run_helper(app, record_path)
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
            'watched entry is a link': (
                lambda o: ((o / 'support').mkdir(parents=True), (o / 'support/f').write_text('a'),
                           (lib / 'Application Support').mkdir(),
                           (lib / 'Application Support' / IDENTIFIER).symlink_to(o / 'support')),
                f'echo b >> "{lib}/Application Support/{IDENTIFIER}/f"\n', f'Application Support/{IDENTIFIER}'),
            'link beneath a watched entry': (
                lambda o: ((o / 'webkit').mkdir(parents=True), (o / 'webkit/f').write_text('a'),
                           (lib / 'WebKit' / IDENTIFIER).mkdir(parents=True),
                           (lib / 'WebKit' / IDENTIFIER / 'data').symlink_to(o / 'webkit')),
                f'echo b >> "{lib}/WebKit/{IDENTIFIER}/data/f"\n', f'WebKit/{IDENTIFIER}/data'),
        }
        for index, (name, (setup, script, link)) in enumerate(cases.items()):
            with self.subTest(name):
                setup(outside)
                app, record_path = self.bundle(script, where=f'link{index}')
                code, record, out, _ = self.run_helper(app, record_path)
                self.assertEqual((code, record['outcome'], record['real_library']['result']), (1, 'failed', 'incomplete'), out)
                self.assertIn(link, record['real_library']['links_met'])
                for path in (lib / 'Caches', lib / 'Application Support', lib / 'WebKit'):
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
                app, record_path = self.bundle(where=f'case{index}', **options)
                calls = []

                def listing(base, *args):
                    if Path(base) == self.real / 'Library':
                        calls.append(1)
                        if failing == 'before' or (failing == 'after' and len(calls) > 1):
                            raise PermissionError('invented: listing refused')
                    return real_listing(base, *args)
                with mock.patch.object(launch, 'listing', listing):
                    code, record, out, _ = self.run_helper(app, record_path)
                self.assertEqual(code, expected, out)
                self.assertNotEqual(record['outcome'], 'clean')
                if failing:
                    self.assertEqual(record['real_library']['result'], 'not made')

    def test_reviewer_t3_an_unexaminable_library_is_not_made_never_unchanged(self):
        lib = self.real / 'Library'
        with self.subTest('unreadable before the launch'):
            lib.chmod(0o000)
            try:
                app, record_path = self.bundle(where='before')
                code, record, out, _ = self.run_helper(app, record_path)
            finally:
                lib.chmod(0o700)
            self.assertEqual((code, record['outcome'], record['real_library']['result']), (2, 'not launched', 'not made'), out)
        with self.subTest('made unreadable by the run'):
            app, record_path = self.bundle(f'chmod 000 "{lib}"\n', where='during')
            try:
                code, record, out, _ = self.run_helper(app, record_path)
            finally:
                lib.chmod(0o700)
            self.assertEqual((code, record['outcome'], record['real_library']['result']), (1, 'failed', 'not made'), out)
        with self.subTest('an ancestor of every watched place made unexaminable by the run'):
            app, record_path = self.bundle(f'chmod 000 "{self.real}"\n', where='ancestor')
            try:
                code, record, out, _ = self.run_helper(app, record_path)
            finally:
                self.real.chmod(0o700)
            self.assertEqual((code, record['outcome'], record['real_library']['result']), (1, 'failed', 'not made'), out)
        with self.subTest('a watched folder unreadable'):
            (lib / 'Caches').mkdir()
            app, record_path = self.bundle(f'chmod 000 "{lib}/Caches"\n', where='folder')
            try:
                code, record, out, _ = self.run_helper(app, record_path)
            finally:
                (lib / 'Caches').chmod(0o700)
            self.assertEqual((code, record['real_library']['result']), (1, 'not made'), out)

    def test_the_record_states_its_fields_and_is_written_once(self):
        app, record_path = self.bundle()
        code, record, out, run_dir = self.run_helper(app, record_path)
        self.assertEqual((code, record['outcome']), (0, 'clean'), out)
        self.assertIn('not an examination record format', record['note'])
        for field in ('candidate_key', 'identifier', 'bundle', 'launch_folder', 'home', 'home_kind', 'environment',
                      'overrides_passed', 'started_at', 'ended_at', 'ended', 'pid', 'process_group_after_settle',
                      'real_library', 'stops', 'home_path_during_launch', 'disclosed', 'output', 'failures', 'outcome'):
            self.assertIn(field, record)
        self.assertEqual(set(record['output']), {'path', 'note'})  # T6: the path only
        for removed in ('address_override_input', 'model_address_input'):  # T7: nothing about what the build reads
            self.assertNotIn(removed, record)
        self.assertEqual((record['real_library']['result'], record['stops'], record['home_path_during_launch']),
                         ('unchanged', [], 'unchanged'))
        code, _ = self.call(*self.argv(app, record_path, run_dir=run_dir))
        self.assertEqual(code, 2)


class Stops(Fixture):  # GUARD 4, RULE C
    def test_reviewer_the_app_deleting_the_run_folder_and_exiting_zero_after_a_stop_is_not_clean(self):
        run_dir = self.tmp / f'run-{self.runs + 1}'
        app, record_path = self.bundle(f"trap 'rm -rf \"{run_dir}\"/*; exit 0' TERM\nwhile :; do sleep 0.1; done\n",
                                       where='deleting')
        thread, result = self.in_background(lambda folder: launch.stop(folder))
        code, record, out, _ = self.run_helper(app, record_path, settle='0.5')
        thread.join()
        self.assertEqual(result['value']['answer'], launch.ACCEPTED)
        self.assertEqual((record['ended'], code, record['outcome']), ('exited with status 0', 1, 'failed'), out)
        self.assertEqual(len(record['stops']), 1)

    def test_stop_signals_the_helper_never_the_app(self):
        app, record_path = self.bundle(TRAP, where='trapping')
        killed = []
        real_kill = os.kill

        def act(folder):
            me = threading.get_ident()

            def watch(pid, sig):
                if threading.get_ident() == me:  # what the stop command signals, not the helper's own forwarding
                    killed.append(pid)
                return real_kill(pid, sig)
            with mock.patch.object(launch.os, 'kill', watch):
                return launch.stop(folder)
        thread, result = self.in_background(act)
        code, record, out, _ = self.run_helper(app, record_path, settle='0.5')
        thread.join()
        self.assertEqual(killed, [os.getpid()])
        self.assertEqual((code, record['outcome']), (1, 'failed'), out)

    def test_a_signal_the_helper_receives_is_accepted_the_same_way(self):
        app, record_path = self.bundle(TRAP, where='forwarded')
        thread, _ = self.in_background(lambda folder: os.kill(os.getpid(), signal.SIGTERM))
        code, record, _, _ = self.run_helper(app, record_path, settle='0.5')
        thread.join()
        self.assertEqual((record['ended'], code, record['outcome']), ('exited with status 0', 1, 'failed'))
        self.assertEqual(record['stops'][0]['signal'], 'SIGTERM')

    def test_reviewer_t4_a_stop_at_each_step_of_finalization_is_in_the_record_or_told_not_accepted(self):
        for step in ('settle', 'compare', 'outcome', 'write_record'):
            with self.subTest(step):
                app, record_path = self.bundle(where=f'final-{step}')
                answers = []
                real = {name: getattr(launch, name) for name in ('compare', 'outcome', 'write_record')}

                def inject(name):
                    def injected(*args, **kwargs):
                        if not answers:
                            answers.append(launch.stop(self.newest_folder(), wait_seconds=5))
                        return real[name](*args, **kwargs)
                    return injected
                real_sleep = launch.time.sleep

                def sleep(seconds):
                    if step == 'settle' and not answers and launch._forwarding.is_set():
                        answers.append(launch.stop(self.newest_folder(), wait_seconds=5))
                    return real_sleep(seconds)
                patches = [mock.patch.object(launch.time, 'sleep', sleep)] + (
                    [mock.patch.object(launch, step, inject(step))] if step in real else [])
                with contextlib.ExitStack() as stack:
                    for patch in patches:
                        stack.enter_context(patch)
                    code, record, out, _ = self.run_helper(app, record_path)
                self.assertEqual(len(answers), 1, out)
                answer = answers[0]['answer']
                self.assertIn(answer, (launch.ACCEPTED, launch.TOO_LATE))
                accepted_in_record = any(s['stop_requests_answered'] for s in record['stops'])
                self.assertEqual(answer == launch.ACCEPTED, accepted_in_record, (step, answer, record['stops']))
                if answer == launch.ACCEPTED:
                    self.assertEqual(record['outcome'], 'failed')

    def test_two_stops_at_once_are_both_answered_and_both_in_the_record(self):
        app, record_path = self.bundle(TRAP, where='two-stops')
        results = []

        def both(folder):
            threads = [threading.Thread(target=lambda: results.append(launch.stop(folder))) for _ in range(2)]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()
        thread, _ = self.in_background(both)
        code, record, out, _ = self.run_helper(app, record_path, settle='0.5')
        thread.join()
        self.assertEqual(len(results), 2, out)
        accepted = [r for r in results if r['answer'] == launch.ACCEPTED]
        answered = [n for s in record['stops'] for n in s['stop_requests_answered']]
        self.assertEqual(len(answered), len(accepted))
        self.assertEqual(record['outcome'], 'failed')

    def test_stop_when_the_helper_has_ended_refuses_and_signals_nothing(self):
        app, record_path, folder, _ = self.made()
        ended = subprocess.Popen(['/bin/sh', '-c', 'exit 0'])
        start = launch.process_start(ended.pid)
        ended.wait()
        handle = launch.own_folder(folder)
        try:
            launch.replace_own(handle.control, launch.PROCESS, launch.PROCESS_FORMAT,
                               {'helper_pid': ended.pid, 'helper_start': start or 'invented', 'app_pid': None})
        finally:
            handle.close()
        with mock.patch.object(launch.os, 'kill', side_effect=AssertionError('nothing may be signalled')):
            code, out = self.call('stop', '--launch-folder', str(folder))
        self.assert_refused(code, out, 'no running helper is recorded')

    def test_files_planted_in_the_run_folder_decide_nothing(self):
        run_dir = self.tmp / f'run-{self.runs + 1}'
        app, record_path = self.bundle(f'mkdir -p "{run_dir}/stop-requests"\necho stop > "{run_dir}/stop-requests/x.json"\n'
                                       f'ln -s "$HOME/auth.json" "{run_dir}/planted.json"\n', where='planting')
        code, record, out, _ = self.run_helper(app, record_path)
        self.assertEqual((code, record['outcome'], record['stops']), (0, 'clean', []), out)
        self.assertNotIn(SECRET, self.everything_written(run_dir, out))


class WatchedByExactName(Fixture):  # INVARIANT 3
    def test_an_executable_name_that_does_not_discriminate_is_refused(self):
        for index, name in enumerate(('a', 'app', 'chirality', 'Chirality-x')):
            with self.subTest(name):
                app, record_path = self.bundle(executable=name, where=f'short{index}')
                code, record, out, run_dir = self.run_helper(app, record_path)
                self.assert_refused(code, out, 'does not discriminate')
                self.assertFalse(run_dir.exists())
        launch.check_executable(EXECUTABLE)

    def test_the_rule_names_entries_exactly(self):
        helper = 'com.apple.WebKit.{}+chirality_app_v4-0a1b2c'
        watched = [IDENTIFIER, IDENTIFIER + '.plist', IDENTIFIER + '.savedState', IDENTIFIER + '.binarycookies',
                   'prefix.' + IDENTIFIER, EXECUTABLE, 'Chirality-App-V4', helper.format('Networking'),
                   helper.format('WebContent'), helper.format('GPU')]
        unwatched = [IDENTIFIER + '2', IDENTIFIER + '-other', EXECUTABLE + '.old', 'chirality-app', 'a',
                     'com.apple.WebKit.Networking+other_app-1', 'com.apple.WebKit.Networking+chirality_app_v4',
                     'com.apple.spaces.plist']
        for name in watched:
            self.assertTrue(launch.watched_name(name, IDENTIFIER, EXECUTABLE), name)
        for name in unwatched:
            self.assertFalse(launch.watched_name(name, IDENTIFIER, EXECUTABLE), name)

    def test_a_preference_named_for_the_build_fails_and_others_are_disclosed(self):
        prefs = self.real / 'Library/Preferences'
        app, record_path = self.bundle(f'echo x > "{prefs}/com.apple.spaces.plist"\necho y >> "{prefs}/com.apple.dock.plist"\n'
                                       f'ln -s /invented/target "{prefs}/com.apple.linked.plist"\n')
        code, record, out, _ = self.run_helper(app, record_path)
        self.assertEqual((code, record['outcome']), (0, 'clean'), out)
        preferences = record['disclosed']['preferences']
        self.assertEqual(preferences['observation'], 'made')  # a link there is an entry, not a failed observation
        self.assertEqual({(c['path'], c['change']) for c in preferences['changes']},
                         {('com.apple.spaces.plist', 'created'), ('com.apple.dock.plist', 'modified'),
                          ('com.apple.linked.plist', 'created')})
        app, record_path = self.bundle(f'echo x > "{prefs}/{IDENTIFIER}.plist"\n', where='named')
        code, record, out, _ = self.run_helper(app, record_path)
        self.assertEqual((code, record['real_library']['result']), (1, 'changed'), out)


class ObservationNotGate(Fixture):  # RULE D
    def test_the_per_user_cache_folder_is_disclosed_and_never_a_failure(self):
        helper = f'com.apple.WebKit.WebContent+{EXECUTABLE.replace("-", "_")}-0a1b'
        app, record_path = self.bundle(f'mkdir -p "{self.cache}/{helper}" "{self.cache}/{IDENTIFIER}"\n'
                                       f'echo x > "{self.cache}/{helper}/data"\necho x > "{self.cache}/unrelated"\n')
        code, record, out, _ = self.run_helper(app, record_path)
        self.assertEqual((code, record['outcome']), (0, 'clean'), out)
        cache = record['disclosed']['user_cache']
        self.assertEqual(cache['observation'], 'made')
        self.assertEqual({(c['path'], c['change']) for c in cache['changes']},
                         {(helper, 'created'), (helper + '/data', 'created'), (IDENTIFIER, 'created')})

    def test_an_unexaminable_cache_folder_neither_refuses_nor_reports_changes(self):
        hidden_parent = self.tmp / 'hidden'
        (hidden_parent / 'cache').mkdir(parents=True)
        for name, setup, undo, base in (
                ('unreadable folder', lambda: self.cache.chmod(0o000), lambda: self.cache.chmod(0o700), self.cache),
                ('unexaminable ancestor (T3)', lambda: hidden_parent.chmod(0o000), lambda: hidden_parent.chmod(0o700),
                 hidden_parent / 'cache')):
            with self.subTest(name), mock.patch.object(launch, 'user_cache_dir', return_value=base):
                setup()
                try:
                    app, record_path = self.bundle(where=name.replace(' ', '-'))
                    code, record, out, _ = self.run_helper(app, record_path)
                finally:
                    undo()
                self.assertEqual((code, record['outcome']), (0, 'clean'), out)
                cache = record['disclosed']['user_cache']
                self.assertTrue(cache['observation'].startswith('not observed'), cache)
                self.assertNotIn('changes', cache)

    def test_a_failed_after_observation_reports_no_changes(self):
        real = launch.observe
        calls = []

        def observe(*args):
            calls.append(1)
            return real(*args) if len(calls) == 1 else (None, 'not observed: invented failure (PermissionError)')
        app, record_path = self.bundle()
        with mock.patch.object(launch, 'observe', observe):
            code, record, out, _ = self.run_helper(app, record_path)
        self.assertEqual((code, record['outcome']), (0, 'clean'), out)
        self.assertNotIn('changes', record['disclosed']['user_cache'])

    def test_a_cache_folder_that_is_a_link_is_not_resolved_and_a_link_inside_is_incomplete(self):
        target = self.tmp / 'cache-target'
        (target / IDENTIFIER).mkdir(parents=True)
        link = self.tmp / 'cache-link'
        link.symlink_to(target)
        with mock.patch.object(launch, 'user_cache_dir', return_value=link):
            app, record_path = self.bundle(f'echo x > "{target}/{IDENTIFIER}/new"\n')
            code, record, out, _ = self.run_helper(app, record_path)
        self.assertEqual(record['disclosed']['user_cache']['observation'], 'not observed: the per-user cache folder is a link')
        (self.cache / IDENTIFIER).mkdir()
        (self.cache / IDENTIFIER / 'link').symlink_to(self.tmp)
        app, record_path = self.bundle(where='inner')
        code, record, out, _ = self.run_helper(app, record_path)
        self.assertEqual((code, record['outcome']), (0, 'clean'), out)
        self.assertTrue(record['disclosed']['user_cache']['observation'].startswith('incomplete'))
        self.assertNotIn('changes', record['disclosed']['user_cache'])


class PlacesByIdentity(Fixture):  # GUARD 3, INVARIANT 4
    def test_lower_case_spellings_reach_the_protected_places(self):
        (self.tmp / 'CaseProbe').write_text('')
        if not (self.tmp / 'caseprobe').exists():
            self.skipTest('needs a case-insensitive volume')
        app, record_path = self.bundle()
        (self.real / 'Library/Caches').mkdir()
        for run_dir in (self.real / 'library/Caches/run', self.real / 'LIBRARY/run'):
            with self.subTest(str(run_dir)):
                code, _, out, _ = self.run_helper(app, record_path, run_dir=run_dir)
                self.assert_refused(code, out, 'inside the real home Library')
        app, record_path = self.bundle(where='lower/applications')
        code, _, out, _ = self.run_helper(app, record_path)
        self.assert_refused(code, out, 'Applications folder')

    def test_an_applications_folder_anywhere_and_in_any_case_is_refused(self):
        for where in ('elsewhere/Applications', 'deep/APPLICATIONS/x', 'real-home/Applications'):
            with self.subTest(where):
                app, record_path = self.bundle(where=where)
                code, _, out, run_dir = self.run_helper(app, record_path)
                self.assert_refused(code, out, 'Applications folder')
                self.assertFalse(run_dir.exists())

    def test_a_link_anywhere_in_a_path_to_the_helpers_folders_is_refused(self):
        app, record_path, folder, _ = self.made()
        into_library = self.tmp / 'into-library'
        into_library.symlink_to(self.real / 'Library')
        checkout = self.tmp / 'checkout'
        (checkout / '.git').mkdir(parents=True)
        aliased_parent = self.tmp / 'aliased-parent'
        aliased_parent.symlink_to(self.parent)
        base = ['launch', '--app', str(app), '--record', str(record_path), '--settle-seconds', '0']
        for name, argv, reason in (
                ('run folder through a link into the Library',
                 ['--run-dir', str(into_library / 'run'), '--parent', str(self.parent)], 'real home Library'),
                ('run folder in this repository',
                 ['--run-dir', str(launch.REPOSITORY / 'launch-run'), '--parent', str(self.parent)], 'checkout'),
                ('parent inside a checkout', ['--run-dir', str(self.tmp / 'r'), '--parent', str(checkout)], 'checkout'),
                ('run folder through a link', ['--run-dir', str(aliased_parent / 'run'), '--parent', str(self.parent)],
                 'no link'),
                ('reused folder through a link', ['--run-dir', str(self.tmp / 'r'), '--reuse', str(aliased_parent / folder.name)],
                 'no link')):
            with self.subTest(name):
                code, out = self.call(*base, *argv)
                self.assert_refused(code, out, reason)
                self.assertFalse((self.tmp / 'r').exists())
        for command in (['remove'], ['stop']):
            with self.subTest(command):
                self.assert_refused(*self.call(*command, '--launch-folder', str(aliased_parent / folder.name)), 'no link')
        self.assertFalse((launch.REPOSITORY / 'launch-run').exists())


@contextlib.contextmanager
def reads_under(home):
    """Instrumentation, lexical and resolved: every open for reading, listing or stat whose path, or whose
    descriptor-relative path or resolved target, lies under home. Only the home itself may be opened as a handle or
    stat'ed, and only exclusive write-only creation may happen under it."""
    home = os.path.realpath(home)
    touched = []

    def strictly_under(text):
        return text is not None and text.startswith(home + os.sep)

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
            result = real[name](*args, **kwargs)
            resolved = fd_path(result) if name == 'open' else None
            listing = name in ('listdir', 'scandir')
            if not creating and (strictly_under(lexical) or strictly_under(resolved)
                                 or (listing and lexical == home)):
                touched.append((name, lexical, resolved))
            return result
        return spied
    real_open = builtins.open

    def spied_open(file, *args, **kwargs):
        if not isinstance(file, int) and strictly_under(os.path.realpath(os.fsdecode(file))):
            touched.append(('open', file, None))
        return real_open(file, *args, **kwargs)
    with contextlib.ExitStack() as stack:
        for name in real:
            stack.enter_context(mock.patch.object(os, name, wrap(name)))
        stack.enter_context(mock.patch.object(builtins, 'open', spied_open))
        stack.enter_context(mock.patch.object(io, 'open', spied_open))
        yield touched


class NeverReadsAHome(Fixture):  # GUARD 2, RULE A
    def test_launch_reuse_stop_failed_start_and_refused_remove_read_nothing_under_the_home(self):
        app, record_path, folder, first = self.made()
        quiet, quiet_record = self.bundle(TRAP, where='quiet', plays=False)
        broken, broken_record = self.bundle(where='broken', shebang='#!/nonexistent/interpreter')
        lingering, lingering_record = self.bundle('sleep 30 &\n', where='lingering', plays=False)
        with reads_under(folder / launch.HOME) as touched:
            code, _, out, _ = self.run_helper(app, record_path, reuse=folder)
            self.assertEqual(code, 0, out)
            thread, _ = self.in_background(lambda f: launch.stop(f), folder)
            code, _, out, _ = self.run_helper(quiet, quiet_record, reuse=folder, settle='0.3')
            thread.join()
            self.assertEqual(code, 1, out)
            code, _, out, _ = self.run_helper(broken, broken_record, reuse=folder)
            self.assertEqual(code, 1, out)
            self.run_helper(lingering, lingering_record, reuse=folder)
            self.assert_refused(*self.call('remove', '--launch-folder', str(folder)), 'refused')
        self.assertEqual(touched, [])

    def test_a_new_home_is_never_read_either(self):
        app, record_path = self.bundle()
        with reads_under(self.parent) as touched:
            code, record, out, _ = self.run_helper(app, record_path)
        self.assertEqual(code, 0, out)
        self.assertEqual([t for t in touched if (t[1] or '').startswith(record['home'] + os.sep)
                          or (t[2] or '').startswith(record['home'] + os.sep)], [])

    def test_reviewer_t2_a_control_folder_or_run_folder_linked_into_the_home_is_refused_unread(self):
        app, record_path, folder, record = self.made()
        home = folder / launch.HOME
        fake = home / 'fake-control'
        shutil.copytree(folder / launch.CONTROL, fake)
        (folder / launch.CONTROL).rename(folder / 'control-moved')
        (folder / launch.CONTROL).symlink_to(fake)
        with reads_under(home) as touched:
            code, _, out, _ = self.run_helper(app, record_path, reuse=folder)
            self.assert_refused(code, out, 'control folder is missing or a link')
            self.assert_refused(*self.call('remove', '--launch-folder', str(folder)), 'control folder is missing or a link')
            self.assert_refused(*self.call('stop', '--launch-folder', str(folder)), 'control folder is missing or a link')
            code, out = self.call(*self.argv(app, record_path, run_dir=home / 'run-inside', reuse=None))
            self.assert_refused(code, out, 'inside a launch folder')
        self.assertEqual(touched, [])
        self.assertNotIn(SECRET, out)
        self.assertFalse((home / 'run-inside').exists())

    def test_with_every_entry_of_the_app_at_mode_000_nothing_of_the_helper_fails(self):
        app, record_path, folder, first = self.made('mkdir -p "$HOME/private/deeper"\necho x > "$HOME/private/deeper/f"\n')
        home = folder / launch.HOME
        for entry in home.iterdir():
            if not entry.name.startswith('.chirality-launch-output-'):
                entry.chmod(0o000)
        quiet, quiet_record = self.bundle(where='quiet', plays=False)
        code, record, out, _ = self.run_helper(quiet, quiet_record, reuse=folder)
        self.assertEqual((code, record['outcome']), (0, 'clean'), out)
        code, out = self.call('remove', '--launch-folder', str(folder))
        self.assertEqual(code, 0, out)
        self.assertFalse(folder.exists())

    def test_reviewer_t5_a_temporary_folder_replaced_by_a_link_is_never_used_again(self):
        outside = self.tmp / 'outside-tmp'
        outside.mkdir()
        app, record_path, folder, first = self.made(f'rm -rf "$TMPDIR"\nln -s "{outside}" "$TMPDIR"\n')
        old_tmp = self.received(first)['TMPDIR']
        writer, writer_record = self.bundle('echo x > "$TMPDIR/written"\nenv > "$HOME/received-env.txt"\n',
                                            where='writer', plays=False)
        code, record, out, _ = self.run_helper(writer, writer_record, reuse=folder)
        self.assertEqual(code, 0, out)
        new_tmp = self.received(record)['TMPDIR']
        self.assertNotEqual(new_tmp, old_tmp)
        self.assertTrue(new_tmp.startswith(record['home'] + '/.chirality-launch-tmp-'))
        self.assertTrue((Path(new_tmp) / 'written').exists())
        self.assertEqual(os.listdir(outside), [])


class OwnFilesDefensive(Fixture):  # GUARDS 2 and 3, RULE B
    def corrupt(self, control, name, how, secret_path):
        path = control / name
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

    def test_marker_state_process_and_lock_files_not_the_helpers_own_are_refused_unread_and_unquoted(self):
        for target in (launch.MARKER, launch.STATE, launch.PROCESS, launch.LOCK):
            for how in ('symlink', 'hard link', 'directory', 'extra key', 'empty', 'not a dictionary', 'missing'):
                if target == launch.LOCK and how in ('extra key', 'empty', 'not a dictionary'):
                    continue  # the lock's content is never read
                with self.subTest(target=target, how=how):
                    app, record_path, folder, record = self.made()
                    secret = Path(record['home']) / 'auth.json'
                    control = folder / launch.CONTROL
                    if how == 'missing':
                        (control / target).unlink()
                    else:
                        self.corrupt(control, target, how, secret)
                    real_read, read = os.read, []

                    def spied_read(fd, size):
                        data = real_read(fd, size)
                        read.append(data)
                        return data
                    with mock.patch.object(launch.os, 'read', spied_read):
                        if target == launch.PROCESS:
                            outputs = [self.call('stop', '--launch-folder', str(folder))]
                        else:
                            code, _, out, _ = self.run_helper(app, record_path, reuse=folder)
                            outputs = [(code, out), self.call('remove', '--launch-folder', str(folder))]
                    for code, text in outputs:
                        self.assertEqual(code, 2, text)
                        self.assertNotIn(SECRET, text)
                    self.assertTrue(folder.exists())
                    if how in ('symlink', 'hard link'):
                        self.assertFalse(any(SECRET.encode() in data for data in read))

    @unittest.skipUnless(os.getuid() == 0, "a file of another user's making needs privilege to construct")
    def test_a_state_file_of_another_users_making_is_refused(self):
        app, record_path, folder, _ = self.made()
        os.chown(folder / launch.CONTROL / launch.STATE, 1, 1)
        self.assertEqual(self.call('remove', '--launch-folder', str(folder))[0], 2)

    def test_nothing_planted_by_the_app_reaches_a_record_or_output(self):
        run_dir = self.tmp / f'run-{self.runs + 1}'
        app, record_path = self.bundle(f'mkdir -p "{run_dir}/stop-requests"\n'
                                       f'ln -s "$HOME/auth.json" "{run_dir}/stop-requests/planted.json"\n'
                                       f'echo {SECRET}\necho {SECRET} >&2\n')
        code, record, out, _ = self.run_helper(app, record_path)
        self.assertEqual(code, 0, out)
        self.assertNotIn(SECRET, self.everything_written(run_dir, out))

    def test_remove_never_names_what_is_under_the_home(self):
        app, record_path, folder, _ = self.made('mkdir -p "$HOME/secret-descendant-name/inner"\n')
        (folder / launch.HOME / 'secret-descendant-name').chmod(0o000)
        failing = PermissionError(13, 'Permission denied', str(folder / launch.HOME / 'secret-descendant-name' / 'inner'))
        with mock.patch.object(launch.shutil, 'rmtree', side_effect=failing):
            code, out = self.call('remove', '--launch-folder', str(folder))
        self.assert_refused(code, out, str(folder))
        self.assertNotIn('secret-descendant-name', out)
        code, out = self.call('remove', '--launch-folder', str(folder))
        self.assertEqual(code, 0, out)
        self.assertNotIn('secret-descendant-name', out)


class LaunchFolderCustody(Fixture):  # GUARDS 3 and 4, INVARIANT 5
    def test_a_marker_copied_into_a_replacement_folder_is_refused(self):
        app, record_path, folder, _ = self.made()
        folder.rename(self.parent / 'moved')
        (folder / launch.HOME).mkdir(parents=True)
        shutil.copytree(self.parent / 'moved' / launch.CONTROL, folder / launch.CONTROL)
        (folder / 'precious').write_text("not the helper's")
        self.assert_refused(*self.call('remove', '--launch-folder', str(folder)), 'recorded identity differs')
        self.assertTrue((folder / 'precious').exists())
        code, _, out, _ = self.run_helper(app, record_path, reuse=folder)
        self.assert_refused(code, out, 'recorded identity differs')

    def test_a_living_member_of_the_apps_group_keeps_the_folder_refused(self):
        app, record_path, folder, record = self.made('sleep 30 &\n')
        self.assert_refused(*self.call('remove', '--launch-folder', str(folder)), 'process group')
        code, _, out, _ = self.run_helper(app, record_path, reuse=folder)
        self.assert_refused(code, out, 'process group')
        os.killpg(record['pid'], signal.SIGKILL)
        deadline = time.monotonic() + 5
        while launch.group_state(record['pid']) != 'gone' and time.monotonic() < deadline:
            time.sleep(0.05)
        self.assertEqual(self.call('remove', '--launch-folder', str(folder))[0], 0)

    def test_reuse_records_reused_and_says_nothing_about_the_home(self):
        app, record_path, folder, _ = self.made()
        code, record, out, _ = self.run_helper(app, record_path, reuse=folder)
        self.assertEqual(code, 0, out)
        self.assertEqual(record['launch_folder'], {'launch_folder': str(folder), 'state': 'reused'})

    def test_removal_refuses_the_real_home_checkouts_and_unmarked_folders(self):
        _, _, folder, _ = self.made()
        unmarked = self.parent / 'unmarked'
        (unmarked / launch.CONTROL).mkdir(parents=True)
        for name, path in (('unmarked', unmarked), ('the real home', self.real),
                           ('a folder containing the real home', self.tmp), ('this repository', launch.REPOSITORY)):
            with self.subTest(name):
                self.assertEqual(self.call('remove', '--launch-folder', str(path))[0], 2)
        self.assertTrue(folder.exists() and self.real.exists())
        self.assertEqual(self.call('remove', '--launch-folder', str(folder))[0], 0)

    def test_two_honest_callers_at_once_one_is_refused(self):
        app, record_path, folder, _ = self.made()
        slow, slow_record = self.bundle('sleep 1\n', where='slow', plays=False)
        second = {}

        def other(folder):
            second['reuse'] = self.call(*self.argv(app, record_path, reuse=folder, run_dir=self.tmp / 'second-run'))
            second['remove'] = self.call('remove', '--launch-folder', str(folder))
        thread, _ = self.in_background(other, folder)
        code, record, out, _ = self.run_helper(slow, slow_record, reuse=folder)
        thread.join()
        self.assertEqual((code, record['outcome']), (0, 'clean'), out)
        self.assert_refused(*second['reuse'], 'in use by another invocation')
        self.assert_refused(*second['remove'], 'in use by another invocation')
        self.assertFalse((self.tmp / 'second-run').exists())
        self.assertTrue(folder.exists())


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
patches = [mock.patch.object(launch, 'real_home', return_value=real),
           mock.patch.object(launch, 'user_cache_dir', return_value=cache),
           mock.patch.object(launch, 'identify_candidate', lambda app, record: json.loads(Path(record).read_text()))]
if stage == 'before start':
    patches.append(mock.patch.object(launch, 'check_environment', reached))
if stage == 'finalizing':
    patches.append(mock.patch.object(launch, 'compare', reached))
for patch in patches:
    patch.start()
sys.exit(launch.main(sys.argv[6:]))
'''


class KilledHelper(Fixture):  # GUARD 4: the helper killed (SIGKILL, which it cannot accept) at each stage
    def test_after_a_killed_helper_reuse_stop_and_remove_find_it_interrupted_never_idle_or_clean(self):
        runner = self.tmp / 'runner.py'
        runner.write_text(KILLED_RUNNER)
        for stage in ('before start', 'running', 'finalizing'):
            with self.subTest(stage):
                app, record_path, folder, _ = self.made()
                sentinel = self.tmp / f'sentinel-{stage.replace(" ", "-")}'
                script = f'echo reached > "{sentinel}"\nsleep 60\n' if stage == 'running' else ''
                runnable, runnable_record = self.bundle(script, where=f'killed-{stage.replace(" ", "-")}', plays=False)
                run_dir = self.tmp / f'killed-run-{stage.replace(" ", "-")}'
                argv = self.argv(runnable, runnable_record, reuse=folder, run_dir=run_dir)
                helper = subprocess.Popen([sys.executable, '-B', str(runner), str(HELPER), stage, str(self.real),
                                           str(self.cache), str(sentinel), *argv],
                                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                deadline = time.monotonic() + 20
                while not sentinel.exists() and time.monotonic() < deadline:
                    time.sleep(0.05)
                self.assertTrue(sentinel.exists())
                helper.kill()
                helper.wait()
                handle = launch.own_folder(folder)
                try:
                    group = launch.read_own(handle.control, launch.STATE, launch.STATE_FORMAT, 's')['process_group']
                finally:
                    handle.close()
                if group:
                    self.groups.append(group)
                self.assertFalse((run_dir / launch.RECORD).exists())  # no record: never clean
                code, _, out, _ = self.run_helper(app, record_path, reuse=folder)
                self.assert_refused(code, out, 'interrupted launch')
                self.assert_refused(*self.call('remove', '--launch-folder', str(folder)), 'interrupted launch')
                self.assert_refused(*self.call('stop', '--launch-folder', str(folder)), 'no running helper is recorded')
                self.assertTrue(folder.exists())


class OnlyTheIdentifiedCandidate(Fixture):  # INVARIANT 6
    identification = None

    def test_unknown_format_or_missing_key_is_refused(self):
        app, record_path = self.bundle()
        record = json.loads(record_path.read_text())
        for name, value in (('unknown format', {**record, 'format': 'invented/v9'}),
                            ('empty candidate key', {**record, 'candidate_key': ''})):
            with self.subTest(name):
                record_path.write_text(json.dumps(value))
                code, _, out, run_dir = self.run_helper(app, record_path)
                self.assertEqual(code, 2, out)
                self.assertFalse(run_dir.exists())

    def test_a_check_that_finds_a_difference_is_refused(self):
        app, record_path = self.bundle()
        same = {'equal': True, 'build_identity': 'x', 'recorded_build_identity': 'x', 'record_fields_mismatched': []}
        for name, result in (('inventory differs', {**same, 'equal': False, 'changed': ['Contents/Resources/x']}),
                             ('identity differs', {**same, 'build_identity': 'y'}),
                             ('record fields differ', {**same, 'record_fields_mismatched': ['identifier']})):
            with self.subTest(name), mock.patch.object(identify, 'validate_record'), \
                    mock.patch.object(identify, 'check', return_value=result):
                code, _, out, run_dir = self.run_helper(app, record_path)
                self.assert_refused(code, out, 'differs from its identification record')
                self.assertFalse(run_dir.exists())

    def test_an_unreadable_property_list_is_a_structured_refusal(self):
        app, record_path = self.bundle()
        for error in (plistlib.InvalidFileException(), ExpatError('invented')):
            with self.subTest(type(error).__name__), mock.patch.object(identify, 'validate_record'), \
                    mock.patch.object(identify, 'check', side_effect=error):
                code, _, out, _ = self.run_helper(app, record_path)
                self.assertEqual(code, 2)
                self.assertIn('error', json.loads(out.strip().splitlines()[-1]))

    @unittest.skipUnless(MAC, "identification's check reads live macOS metadata")
    def test_a_changed_resource_is_refused_and_the_identified_bundle_launches(self):
        app, record_path = self.bundle()
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
        out_dir = self.tmp / 'identification'
        with mock.patch.object(Path, 'home', return_value=self.real), contextlib.redirect_stdout(io.StringIO()):
            code = identify.main(['record', '--app', str(app), '--repo', str(repo), '--revision', 'HEAD',
                                  '--export-root', str(export), '--build-facts', str(facts),
                                  '--identified-at', '2000-01-01T00:00:00Z', '--out-dir', str(out_dir)])
        self.assertEqual(code, 0)
        record_path = out_dir / 'candidate-identification.json'
        code, record, out, _ = self.run_helper(app, record_path)
        self.assertEqual((code, record['outcome']), (0, 'clean'), out)
        (app / 'Contents/Resources/instructions/AGENTS.md').write_text('changed after identification\n')
        code, _, out, run_dir = self.run_helper(app, record_path)
        self.assert_refused(code, out, 'Contents/Resources/instructions/AGENTS.md')
        self.assertFalse(run_dir.exists())


class Overrides(Fixture):  # GUARD 3, INVARIANT 7
    def test_the_default_home_is_not_the_owners_sitting_and_is_passed_the_nine_overrides(self):
        app, record_path = self.bundle()
        code, record, out, _ = self.run_helper(app, record_path)
        self.assertEqual(code, 0, out)
        self.assertEqual(record['home_kind'], 'not-owners-sitting')
        env = self.received(record)
        for name in ('HTTPS_PROXY', 'https_proxy', 'HTTP_PROXY', 'http_proxy', 'ALL_PROXY', 'all_proxy'):
            self.assertEqual(env[name], 'http://127.0.0.1:9')
        self.assertEqual((env['NO_PROXY'], env['no_proxy']), ('127.0.0.1,localhost,::1',) * 2)
        self.assertEqual(env[launch.MODEL_ADDRESS], 'http://127.0.0.1:9/v1')
        self.assertEqual(record['overrides_passed'], {name: env[name] for name in OVERRIDES})

    def test_an_owners_sitting_launch_is_passed_the_allowlist_without_the_nine(self):
        app, record_path = self.bundle()
        with mock.patch.dict(os.environ, INVENTED_SECRETS):
            code, record, out, _ = self.run_helper(app, record_path, '--app-env', 'CHIRALITY_WORKSPACE=/invented', owner=True)
        self.assertEqual(code, 0, out)
        self.assertEqual(record['home_kind'], 'owners-sitting')
        self.assertEqual(set(self.received(record)) - SHELL_OWN,
                         {'HOME', 'CFFIXED_USER_HOME', 'TMPDIR', 'PATH', 'LANG', 'CHIRALITY_WORKSPACE'})
        self.assertEqual(record['overrides_passed'], "none (an owner's-sitting launch)")

    def test_every_inconsistency_of_kind_the_helper_can_see_before_the_start_is_refused(self):
        owner_app, owner_record = self.bundle(where='owner')
        code, record, out, _ = self.run_helper(owner_app, owner_record, owner=True)
        owner_folder = Path(record['launch_folder']['launch_folder'])
        app, record_path, other_folder, _ = self.made()
        with self.subTest("the stub-address option on an owner's-sitting home"):
            code, _, out, run_dir = self.run_helper(owner_app, owner_record, '--model-address', 'http://127.0.0.1:8080/v1',
                                                    reuse=owner_folder)
            self.assert_refused(code, out, "owner's-sitting")
            self.assertFalse(run_dir.exists())
        with self.subTest('--owner-sitting on a home of the other kind'):
            code, _, out, run_dir = self.run_helper(app, record_path, reuse=other_folder, owner=True)
            self.assert_refused(code, out, 'contradicts')
        built = launch.child_environment
        with self.subTest("overrides put into an owner's-sitting launch's mapping"):
            with mock.patch.object(launch, 'child_environment',
                                   lambda h, t, i, l, k, *a: built(h, t, i, l, 'not-owners-sitting')):
                code, record, out, _ = self.run_helper(owner_app, owner_record, reuse=owner_folder)
            self.assertEqual((code, record['outcome']), (2, 'not launched'), out)
        with self.subTest("overrides left out of another home's mapping"):
            with mock.patch.object(launch, 'child_environment', lambda h, t, i, l, k, *a: built(h, t, i, l, 'owners-sitting')):
                code, record, out, _ = self.run_helper(app, record_path, reuse=other_folder)
            self.assertEqual((code, record['outcome']), (2, 'not launched'), out)
        for folder, edited in ((owner_folder, 'not-owners-sitting'), (other_folder, 'owners-sitting')):
            with self.subTest('the kind edited in the marker', to=edited):
                marker_path = folder / launch.CONTROL / launch.MARKER
                marker = json.loads(marker_path.read_text())
                marker['kind'] = edited
                marker_path.unlink()
                marker_path.write_text(json.dumps(marker))  # a valid closed-format marker: the name check catches it
                code, _, out, run_dir = self.run_helper(app, record_path, reuse=folder)
                self.assert_refused(code, out, 'does not agree with its name')
                self.assertFalse(run_dir.exists())
        for kind in ('owner', None):
            with self.subTest('a marker without a valid kind', kind=kind):
                app2, record2, folder, _ = self.made()
                marker_path = folder / launch.CONTROL / launch.MARKER
                marker = json.loads(marker_path.read_text())
                if kind is None:
                    del marker['kind']
                else:
                    marker['kind'] = kind
                marker_path.unlink()
                marker_path.write_text(json.dumps(marker))
                code, _, out, _ = self.run_helper(app2, record2, reuse=folder)
                self.assertEqual(code, 2, out)

    def test_reviewer_t1_a_home_path_swapped_at_the_start_is_detected_after_start_and_marked_not_clean(self):
        owner_app, owner_record = self.bundle(where='owner', plays=False)
        code, record, out, _ = self.run_helper(owner_app, owner_record, owner=True)
        owner_home = Path(record['home'])
        app, record_path, folder, _ = self.made()
        home = folder / launch.HOME
        real_popen = subprocess.Popen

        def swapped(*args, **kwargs):  # the swap a same-user process could make between the check and the use
            if str(args[0][0]).endswith('/' + EXECUTABLE):
                home.rename(folder / 'home-moved')
                home.symlink_to(owner_home)
            return real_popen(*args, **kwargs)
        writer, writer_record = self.bundle('echo written > "$HOME/written-by-the-launch"\n', where='writer', plays=False)
        try:
            with mock.patch.object(launch.subprocess, 'Popen', swapped):
                code, record, out, _ = self.run_helper(writer, writer_record, reuse=folder)
        finally:
            home.unlink()
            (folder / 'home-moved').rename(home)
        self.assertEqual((code, record['outcome'], record['home_path_during_launch']), (1, 'failed', 'changed'), out)
        self.assertIn("the home's path changed during launch: detected after start and marked not clean", record['failures'])
        self.assertTrue((owner_home / 'written-by-the-launch').exists())  # detection, not prevention

    def test_a_home_path_swapped_only_around_the_start_is_detected_by_the_check_right_after_it(self):
        owner_app, owner_record = self.bundle(where='owner', plays=False)
        code, record, out, _ = self.run_helper(owner_app, owner_record, owner=True)
        owner_home = Path(record['home'])
        app, record_path, folder, _ = self.made()
        home = folder / launch.HOME
        real_popen = subprocess.Popen

        def swap_back():
            home.unlink()
            (folder / 'home-moved').rename(home)

        def swapped_and_back(*args, **kwargs):  # swapped for the start, put back while the App still runs
            if not str(args[0][0]).endswith('/' + EXECUTABLE):
                return real_popen(*args, **kwargs)
            home.rename(folder / 'home-moved')
            home.symlink_to(owner_home)
            threading.Timer(0.4, swap_back).start()
            return real_popen(*args, **kwargs)
        writer, writer_record = self.bundle('sleep 1.5\n', where='writer', plays=False)
        with mock.patch.object(launch.subprocess, 'Popen', swapped_and_back):
            code, record, out, _ = self.run_helper(writer, writer_record, reuse=folder)
        self.assertEqual((code, record['outcome'], record['home_path_during_launch']), (1, 'failed', 'changed'), out)

    def test_a_home_path_that_no_longer_resolves_before_the_start_is_not_launched(self):
        app, record_path, folder, _ = self.made()
        with mock.patch.object(launch, 'home_path_holds', return_value=False):
            code, record, out, _ = self.run_helper(app, record_path, reuse=folder)
        self.assertEqual((code, record['outcome']), (2, 'not launched'), out)
        self.assertIn('no longer resolves', record['ended'])

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
        refused = ['http://localhost:9', 'http://10.0.0.1:9', 'http://127.0.0.1:0', 'http://127.0.0.1:70000',
                   'http://127.0.0.1:09', 'http://127.0.0.1:9/v1?x=1', 'http://user@127.0.0.1:9', 'http://127.0.0.1:9#f',
                   ' http://127.0.0.1:9', 'http://127.0.0.1:9/' + 'a' * 2030, 'ftp://127.0.0.1']
        for value in accepted:
            self.assertEqual(launch.check_model_address(value), value)
        for value in refused:
            with self.subTest(value[:40]), self.assertRaises(ValueError):
                launch.check_model_address(value)
        self.assertEqual(len('http://127.0.0.1:9/' + 'a' * 2030), 2049)
        app, record_path = self.bundle()
        code, _, out, _ = self.run_helper(app, record_path, '--model-address', 'http://localhost:8080/v1')
        self.assert_refused(code, out, launch.MODEL_ADDRESS)
        code, record, out, _ = self.run_helper(app, record_path, '--model-address', 'http://127.0.0.1:8080/v1')
        self.assertEqual(self.received(record)[launch.MODEL_ADDRESS], 'http://127.0.0.1:8080/v1')


class Housekeeping(unittest.TestCase):
    def test_the_real_home_is_the_account_home_not_the_home_variable(self):
        with mock.patch.dict(os.environ, {'HOME': '/invented/elsewhere'}):
            self.assertEqual(launch.real_home(), Path(os.path.realpath(pwd.getpwuid(os.getuid()).pw_dir)))

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
