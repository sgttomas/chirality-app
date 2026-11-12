"""The examination launch helper, one class per invariant and rule, with invented material only.

A shell script plays the App, and folders stand in for the real home and the
per-user cache folder. The launched program is treated as able to write
anywhere the user can. No App, window or real home Library is touched; nothing
here launches a real build.
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
SHELL_OWN = {'PWD', 'SHLVL', '_', 'OLDPWD', '__CF_USER_TEXT_ENCODING'}  # set by /bin/sh or the macOS runtime itself
HELD = set(launch.PROXY_OVERRIDES) | {launch.MODEL_ADDRESS}

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
               executable=EXECUTABLE, plays=True, name=PRODUCT + '.app', extra_bytes=''):
        app = self.tmp / where / name
        (app / 'Contents/MacOS').mkdir(parents=True)
        (app / 'Contents/Resources/instructions').mkdir(parents=True)
        (app / 'Contents/Resources/instructions/AGENTS.md').write_text('invented guidance\n')
        (app / 'Contents/Info.plist').write_bytes(plistlib.dumps({
            'CFBundleIdentifier': identifier, 'CFBundleName': PRODUCT, 'CFBundleDisplayName': PRODUCT,
            'CFBundleExecutable': executable, 'CFBundleShortVersionString': '0.0.0'}))
        body = shebang + '\n' + (PLAYS_THE_APP.format(id=identifier, secret=SECRET) if plays else '') + script
        body += f'# {extra_bytes}\nexit {exit_status}\n' if extra_bytes else f'exit {exit_status}\n'
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

    def run_helper(self, app, record, *extra, reuse=None, settle='0', run_dir=None, owner=False):
        self.runs += 1
        run_dir = Path(run_dir or self.tmp / f'run-{self.runs}')
        argv = ['launch', '--app', str(app), '--record', str(record), '--run-dir', str(run_dir),
                '--settle-seconds', settle, *extra]
        argv += ['--reuse', str(reuse)] if reuse else ['--parent', str(self.parent)]
        if owner:
            argv.append('--owner-sitting')
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = launch.main(argv)
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

    def made(self, script='', **options):
        app, record_path = self.bundle(script, where=f'made{self.runs}', **options)
        code, record, out, run_dir = self.run_helper(app, record_path)
        return app, record_path, Path(record['launch_folder']['launch_folder']), record

    def received(self, record):
        lines = (Path(record['home']) / 'received-env.txt').read_text().splitlines()
        return dict(line.split('=', 1) for line in lines if '=' in line)

    def assert_refused(self, code, out, reason):
        self.assertEqual(code, 2, out)
        self.assertIn(reason, json.loads(out.strip().splitlines()[-1])['error'])

    def in_background(self, run_dir, act):
        """Acts only once the helper confirmed its forwarding is installed and the App started; never otherwise."""
        def ready():
            return launch._forwarding.is_set() and (run_dir / launch.PROCESS).exists()

        def wait_then_act():
            deadline = time.monotonic() + 10
            while time.monotonic() < deadline and not ready():
                time.sleep(0.05)
            time.sleep(0.3)
            if ready():
                act()
        thread = threading.Thread(target=wait_then_act)
        thread.start()
        return thread

    def everything_written(self, run_dir, out):
        texts = [out]
        for current, _, files in os.walk(run_dir):
            for name in files:
                path = Path(current) / name
                if not path.is_symlink():
                    texts.append(path.read_text(errors='replace'))
        return '\n'.join(texts)


class EnvironmentFromNothing(Fixture):  # INVARIANT 1
    def test_reviewer_child_receives_exactly_the_allowlist_while_the_helper_holds_tokens(self):
        app, record_path = self.bundle()
        with mock.patch.dict(os.environ, {**INVENTED_SECRETS, 'LANG': 'fr_FR.UTF-8', 'USER': 'invented',
                                          'HTTPS_PROXY': 'http://invented.example:8080'}):
            code, record, out, _ = self.run_helper(app, record_path, '--app-env', 'CHIRALITY_RECORDS_STORE=/invented/store')
        self.assertEqual(code, 0, out)
        env = self.received(record)
        home = record['home']
        self.assertEqual(set(env) - SHELL_OWN, {'HOME', 'CFFIXED_USER_HOME', 'TMPDIR', 'PATH', 'LANG',
                                                'CHIRALITY_RECORDS_STORE'} | HELD)
        for name, value in INVENTED_SECRETS.items():
            self.assertNotIn(name, env)
            self.assertNotIn(value, (Path(home) / 'received-env.txt').read_text())
        self.assertEqual((env['HOME'], env['CFFIXED_USER_HOME'], env['TMPDIR']), (home, home, f'{home}/{launch.TMP}'))
        self.assertEqual((env['PATH'], env['LANG']), (launch.SYSTEM_PATH, launch.DEFAULT_LANG))
        self.assertEqual(env['HTTPS_PROXY'], 'http://127.0.0.1:9')
        self.assertEqual(record['environment'], {k: env[k] for k in record['environment']})

    def test_the_environment_is_checked_against_the_allowlist_immediately_before_start(self):
        home = self.parent / 'h'
        good = launch.child_environment(home, {}, 'en_US.UTF-8', 'not-owners-sitting')
        launch.check_environment(good, home, 'not-owners-sitting')
        cases = {
            'inherited name': {**good, 'SSH_AUTH_SOCK': '/x'},
            'HOME alone': {k: v for k, v in good.items() if k != 'CFFIXED_USER_HOME'},
            'CFFIXED_USER_HOME alone': {k: v for k, v in good.items() if k != 'HOME'},
            'homes differ': {**good, 'CFFIXED_USER_HOME': str(self.parent / 'other')},
            'TMPDIR elsewhere': {**good, 'TMPDIR': str(self.parent / 'other')},
            'other PATH': {**good, 'PATH': '/opt/invented/bin:' + launch.SYSTEM_PATH},
        }
        for name, env in cases.items():
            with self.subTest(name), self.assertRaises(ValueError):
                launch.check_environment(env, home, 'not-owners-sitting')
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


class CleanRun(Fixture):  # INVARIANT 2
    def test_reviewer_links_at_or_beneath_a_watched_place_make_the_comparison_incomplete(self):
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
                self.assertEqual((code, record['outcome']), (1, 'failed'), out)
                self.assertEqual(record['real_library']['result'], 'incomplete')
                self.assertIn(link, record['real_library']['links_met'])
                for path in (lib / 'Caches', lib / 'Application Support', lib / 'WebKit'):
                    if path.is_symlink():
                        path.unlink()
                    elif path.exists():
                        shutil.rmtree(path)

    def test_a_link_with_nothing_changed_is_still_incomplete_not_clean(self):
        (self.real / 'Library/Logs').mkdir()
        (self.real / f'Library/Logs/{EXECUTABLE}').symlink_to(self.tmp)
        app, record_path = self.bundle()
        code, record, _, _ = self.run_helper(app, record_path)
        self.assertEqual((code, record['real_library']['result'], record['outcome']), (1, 'incomplete', 'failed'))

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

    def test_the_record_states_its_fields_and_is_written_once(self):
        app, record_path = self.bundle()
        code, record, out, run_dir = self.run_helper(app, record_path)
        self.assertEqual((code, record['outcome']), (0, 'clean'), out)
        self.assertIn('not an examination record format', record['note'])
        for field in ('candidate_key', 'identifier', 'bundle', 'launch_folder', 'home', 'home_kind', 'environment',
                      'overrides_passed', 'address_override_input', 'started_at', 'ended_at', 'ended', 'pid', 'process_group_after_settle',
                      'real_library', 'stops', 'disclosed', 'output', 'failures', 'outcome', 'watched'):
            self.assertIn(field, record)
        self.assertEqual((record['real_library']['result'], record['stops']), ('unchanged', []))
        self.assertTrue((Path(record['home']) / f'Library/WebKit/{IDENTIFIER}/WebsiteData/store').exists())
        code, _ = self.call('launch', '--app', str(app), '--record', str(record_path), '--run-dir', str(run_dir),
                            '--parent', str(self.parent))
        self.assertEqual(code, 2)


class LatchedStop(Fixture):  # RULE C
    TRAP = "trap 'exit 0' TERM\nwhile :; do sleep 0.1; done\n"

    def test_reviewer_the_app_deleting_the_run_folder_and_exiting_zero_after_a_stop_is_not_clean(self):
        run_dir = self.tmp / f'run-{self.runs + 1}'
        app, record_path = self.bundle(f"trap 'rm -rf \"{run_dir}\"/* \"{run_dir}\"/.[!.]*; exit 0' TERM\n"
                                       'while :; do sleep 0.1; done\n', where='deleting')
        stopped = []
        thread = self.in_background(run_dir, lambda: stopped.append(launch.stop(run_dir)))
        code, record, out, _ = self.run_helper(app, record_path, settle='0.5')
        thread.join()
        self.assertTrue(stopped)
        self.assertEqual(record['ended'], 'exited with status 0')
        self.assertEqual((code, record['outcome']), (1, 'failed'), out)
        self.assertEqual([s['signal'] for s in record['stops']], ['SIGTERM'])

    def test_stop_signals_the_helper_never_the_app(self):
        run_dir = self.tmp / f'run-{self.runs + 1}'
        app, record_path = self.bundle(self.TRAP, where='trapping')
        killed = []
        real_kill = os.kill

        def watch(pid, sig):
            killed.append(pid)
            return real_kill(pid, sig)

        def act():
            with mock.patch.object(launch.os, 'kill', watch):
                launch.stop(run_dir)
        thread = self.in_background(run_dir, act)
        code, record, out, _ = self.run_helper(app, record_path, settle='0.5')
        thread.join()
        self.assertIn(os.getpid(), killed)
        self.assertNotIn(record['pid'], killed)
        self.assertEqual((code, record['outcome']), (1, 'failed'), out)

    def test_a_signal_the_helper_receives_is_latched(self):
        run_dir = self.tmp / f'run-{self.runs + 1}'
        app, record_path = self.bundle(self.TRAP, where='forwarded')
        thread = self.in_background(run_dir, lambda: os.kill(os.getpid(), signal.SIGTERM))
        code, record, _, _ = self.run_helper(app, record_path, settle='0.5')
        thread.join()
        self.assertEqual((record['ended'], code, record['outcome']), ('exited with status 0', 1, 'failed'))
        self.assertEqual(record['stops'][0]['signal'], 'SIGTERM')

    def test_stop_when_the_helper_has_ended_refuses_and_signals_nothing(self):
        ended = subprocess.Popen(['/bin/sh', '-c', 'exit 0'])
        start = launch.process_start(ended.pid)
        ended.wait()
        run_dir = self.tmp / 'ended-run'
        run_dir.mkdir()
        launch.write_own(run_dir / launch.PROCESS, launch.PROCESS_FORMAT,
                         {'helper_pid': ended.pid, 'helper_start': start or 'invented', 'app_pid': ended.pid})
        with mock.patch.object(launch.os, 'kill', side_effect=AssertionError('nothing may be signalled')):
            with self.assertRaisesRegex(ValueError, 'not running; nothing was signalled'):
                launch.stop(run_dir)

    def test_files_planted_in_the_run_folder_decide_nothing(self):
        run_dir = self.tmp / f'run-{self.runs + 1}'
        app, record_path = self.bundle(f'mkdir -p "{run_dir}/stop-requests"\necho stop > "{run_dir}/stop-requests/x.json"\n'
                                       f'ln -s "$HOME/auth.json" "{run_dir}/planted.json"\n', where='planting')
        code, record, out, _ = self.run_helper(app, record_path)
        self.assertEqual((code, record['outcome'], record['stops']), (0, 'clean', []), out)
        self.assertNotIn(SECRET, self.everything_written(run_dir, out))


class WatchedByExactName(Fixture):  # INVARIANT 3
    def test_reviewer_an_executable_name_that_does_not_discriminate_is_refused(self):
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

    def test_unwatched_neighbours_may_change_and_the_run_is_still_clean(self):
        caches = self.real / 'Library/Caches'
        caches.mkdir()
        app, record_path = self.bundle(f'echo x > "{caches}/{EXECUTABLE}.old"\nmkdir -p "{caches}/{IDENTIFIER}2"\n')
        code, record, out, _ = self.run_helper(app, record_path)
        self.assertEqual((code, record['outcome']), (0, 'clean'), out)

    def test_a_preference_named_for_the_build_fails_and_others_are_disclosed(self):
        prefs = self.real / 'Library/Preferences'
        app, record_path = self.bundle(f'echo x > "{prefs}/com.apple.spaces.plist"\necho y >> "{prefs}/com.apple.dock.plist"\n')
        code, record, out, _ = self.run_helper(app, record_path)
        self.assertEqual((code, record['outcome']), (0, 'clean'), out)
        self.assertEqual({(c['path'], c['change']) for c in record['disclosed']['preferences']['changes']},
                         {('com.apple.spaces.plist', 'created'), ('com.apple.dock.plist', 'modified')})
        app, record_path = self.bundle(f'echo x > "{prefs}/{IDENTIFIER}.plist"\n', where='named')
        code, record, out, _ = self.run_helper(app, record_path)
        self.assertEqual((code, record['real_library']['result']), (1, 'changed'), out)
        self.assertEqual(record['disclosed']['preferences']['changes'], [])


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

    def test_reviewer_an_unreadable_cache_folder_neither_refuses_nor_reports_changes(self):
        self.cache.chmod(0o000)
        try:
            app, record_path = self.bundle()
            code, record, out, _ = self.run_helper(app, record_path)
        finally:
            self.cache.chmod(0o700)
        self.assertEqual((code, record['outcome']), (0, 'clean'), out)
        cache = record['disclosed']['user_cache']
        self.assertTrue(cache['observation'].startswith('not observed'))
        self.assertNotIn('changes', cache)

    def test_reviewer_a_failed_after_observation_reports_no_changes(self):
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

    def test_reviewer_a_cache_folder_that_is_a_link_is_not_resolved(self):
        target = self.tmp / 'cache-target'
        (target / IDENTIFIER).mkdir(parents=True)
        link = self.tmp / 'cache-link'
        link.symlink_to(target)
        with mock.patch.object(launch, 'user_cache_dir', return_value=link):
            app, record_path = self.bundle(f'echo x > "{target}/{IDENTIFIER}/new"\n')
            code, record, out, _ = self.run_helper(app, record_path)
        self.assertEqual((code, record['outcome']), (0, 'clean'), out)
        self.assertEqual(record['disclosed']['user_cache']['observation'], 'not observed: the per-user cache folder is a link')
        self.assertNotIn('changes', record['disclosed']['user_cache'])

    def test_a_link_inside_the_cache_makes_the_observation_incomplete_without_changes(self):
        (self.cache / IDENTIFIER).mkdir()
        (self.cache / IDENTIFIER / 'link').symlink_to(self.tmp)
        app, record_path = self.bundle()
        code, record, out, _ = self.run_helper(app, record_path)
        self.assertEqual((code, record['outcome']), (0, 'clean'), out)
        self.assertTrue(record['disclosed']['user_cache']['observation'].startswith('incomplete'))
        self.assertNotIn('changes', record['disclosed']['user_cache'])


class PlacesByIdentity(Fixture):  # INVARIANT 4
    def test_reviewer_lower_case_spellings_reach_the_protected_places(self):
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
        link = self.tmp / 'via-link'
        link.symlink_to(self.tmp / 'elsewhere/Applications')
        self.assertTrue(launch.under_applications(link / (PRODUCT + '.app')))

    def test_a_link_spelling_into_a_protected_place_is_refused(self):
        app, record_path = self.bundle()
        into_library = self.tmp / 'into-library'
        into_library.symlink_to(self.real / 'Library')
        checkout = self.tmp / 'checkout'
        (checkout / '.git').mkdir(parents=True)
        into_checkout = self.tmp / 'into-checkout'
        into_checkout.symlink_to(checkout)
        base = ['launch', '--app', str(app), '--record', str(record_path), '--settle-seconds', '0']
        for name, argv, reason in (
                ('run folder through a link into the Library',
                 ['--run-dir', str(into_library / 'run'), '--parent', str(self.parent)], 'real home Library'),
                ('run folder in this repository',
                 ['--run-dir', str(launch.REPOSITORY / 'launch-run'), '--parent', str(self.parent)], 'checkout'),
                ('parent through a link into a checkout',
                 ['--run-dir', str(self.tmp / 'r'), '--parent', str(into_checkout)], 'checkout')):
            with self.subTest(name):
                code, out = self.call(*base, *argv)
                self.assert_refused(code, out, reason)
                self.assertFalse((self.tmp / 'r').exists())
        self.assertFalse((launch.REPOSITORY / 'launch-run').exists())
        self.assertEqual(os.listdir(checkout), ['.git'])


@contextlib.contextmanager
def reads_under(home):
    """Instrumentation: every read, listing or stat of a path under home; only an lstat of the home itself is allowed."""
    home = os.path.realpath(home)
    touched = []

    def under(path):
        if isinstance(path, int) or path is None:
            return None
        try:
            text = os.path.abspath(os.fsdecode(path))
        except TypeError:
            return None
        return text if text == home or text.startswith(home + os.sep) else None

    real = {name: getattr(os, name) for name in ('listdir', 'scandir', 'stat', 'lstat', 'open')}

    def wrap(name):
        def spied(*args, **kwargs):
            path = under(args[0] if args else kwargs.get('path', '.')) if kwargs.get('dir_fd') is None else None
            if path:
                flags = (args[1] if len(args) > 1 else kwargs.get('flags', 0)) if name == 'open' else 0
                creating = (name == 'open' and flags & os.O_ACCMODE == os.O_WRONLY and flags & os.O_CREAT
                            and flags & os.O_EXCL)
                if not creating and not (name == 'lstat' and path == home):
                    touched.append((name, path))
            return real[name](*args, **kwargs)
        return spied
    real_open = builtins.open

    def spied_open(file, *args, **kwargs):
        path = under(file)
        if path:
            touched.append(('open', path))
        return real_open(file, *args, **kwargs)
    with contextlib.ExitStack() as stack:
        for name in real:
            stack.enter_context(mock.patch.object(os, name, wrap(name)))
        stack.enter_context(mock.patch.object(builtins, 'open', spied_open))
        stack.enter_context(mock.patch.object(io, 'open', spied_open))
        yield touched


class NeverReadsTheHome(Fixture):  # RULE A
    def test_launch_reuse_stop_failed_start_and_refused_remove_read_nothing_under_the_home(self):
        app, record_path, folder, first = self.made()
        home = folder / launch.HOME
        quiet, quiet_record = self.bundle(LatchedStop.TRAP, where='quiet', plays=False)
        broken, broken_record = self.bundle(where='broken', shebang='#!/nonexistent/interpreter')
        lingering, lingering_record = self.bundle('sleep 30 &\n', where='lingering', plays=False)
        with reads_under(home) as touched:
            code, _, out, _ = self.run_helper(app, record_path, reuse=folder)
            self.assertEqual(code, 0, out)
            run_dir = self.tmp / f'run-{self.runs + 1}'
            thread = self.in_background(run_dir, lambda: launch.stop(run_dir))
            code, _, out, _ = self.run_helper(quiet, quiet_record, reuse=folder, settle='0.3')
            thread.join()
            self.assertEqual(code, 1, out)
            code, _, out, _ = self.run_helper(broken, broken_record, reuse=folder)
            self.assertEqual(code, 1, out)
            self.run_helper(lingering, lingering_record, reuse=folder)
            code, out = self.call('remove', '--launch-folder', str(folder))
            self.assert_refused(code, out, 'in use')
        self.assertEqual(touched, [])

    def test_a_new_home_is_never_read_either(self):
        app, record_path = self.bundle()
        with reads_under(self.parent) as touched:
            code, record, out, _ = self.run_helper(app, record_path)
        self.assertEqual(code, 0, out)
        self.assertEqual([t for t in touched if t[1].startswith(record['home']) and t != ('lstat', record['home'])], [])

    def test_with_every_entry_of_the_app_at_mode_000_nothing_of_the_helper_fails(self):
        app, record_path, folder, first = self.made('mkdir -p "$HOME/private/deeper"\necho x > "$HOME/private/deeper/f"\n')
        home = folder / launch.HOME
        for entry in home.iterdir():
            if entry.name != launch.TMP and not entry.name.startswith('.chirality-launch-output-'):
                entry.chmod(0o000)
        quiet, quiet_record = self.bundle(where='quiet', plays=False)
        code, record, out, _ = self.run_helper(quiet, quiet_record, reuse=folder)
        self.assertEqual((code, record['outcome']), (0, 'clean'), out)
        code, out = self.call('remove', '--launch-folder', str(folder))
        self.assertEqual(code, 0, out)
        self.assertFalse(folder.exists())


class OwnFilesDefensive(Fixture):  # RULE B
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

    def test_reviewer_marker_state_and_process_files_not_the_helpers_own_are_refused_unquoted(self):
        for target in ('marker', 'state', 'process'):
            for how in ('symlink', 'hard link', 'directory', 'extra key', 'empty', 'not a dictionary', 'missing'):
                with self.subTest(target=target, how=how):
                    run_dir = self.tmp / f'run-{self.runs + 1}'
                    app, record_path, folder, record = self.made()
                    secret = Path(record['home']) / 'auth.json'
                    path = {'marker': folder / launch.CONTROL / launch.MARKER,
                            'state': folder / launch.CONTROL / launch.STATE,
                            'process': run_dir / launch.PROCESS}[target]
                    if how == 'missing':
                        path.unlink()
                    else:
                        self.corrupt(path, how, secret)
                    real_read, read = os.read, []

                    def spied_read(fd, size):
                        data = real_read(fd, size)
                        read.append(data)
                        return data
                    if target == 'process':
                        with self.assertRaises(ValueError) as caught, mock.patch.object(launch.os, 'read', spied_read):
                            launch.stop(run_dir)
                        outputs = [str(caught.exception)]
                    else:
                        with mock.patch.object(launch.os, 'read', spied_read):
                            code_reuse, _, out_reuse, reuse_run = self.run_helper(app, record_path, reuse=folder)
                            code_remove, out_remove = self.call('remove', '--launch-folder', str(folder))
                        self.assertEqual((code_reuse, code_remove), (2, 2), out_reuse + out_remove)
                        self.assertTrue(folder.exists())
                        outputs = [out_reuse, out_remove]
                    for text in outputs:
                        self.assertNotIn(SECRET, text)
                    if how in ('symlink', 'hard link'):  # the file it points to is never even read
                        self.assertFalse(any(SECRET.encode() in data for data in read))

    @unittest.skipUnless(os.getuid() == 0, "a file of another user's making needs privilege to construct")
    def test_a_state_file_of_another_users_making_is_refused(self):
        app, record_path, folder, _ = self.made()
        os.chown(folder / launch.CONTROL / launch.STATE, 1, 1)
        self.assertEqual(self.call('remove', '--launch-folder', str(folder))[0], 2)

    def test_reviewer_a_missing_or_non_dictionary_state_never_reads_as_idle(self):
        for how in ('missing', 'not a dictionary'):
            with self.subTest(how):
                app, record_path, folder, record = self.made('sleep 30 &\n')
                state = folder / launch.CONTROL / launch.STATE
                if how == 'missing':
                    state.unlink()
                else:
                    state.write_text('[]')
                code, _, out, run_dir = self.run_helper(app, record_path, reuse=folder)
                self.assertEqual(code, 2, out)
                self.assertFalse(run_dir.exists())
                self.assertEqual(self.call('remove', '--launch-folder', str(folder))[0], 2)
                self.assertTrue(folder.exists())

    def test_reviewer_nothing_planted_by_the_app_reaches_a_record_or_output(self):
        run_dir = self.tmp / f'run-{self.runs + 1}'
        app, record_path = self.bundle(f'mkdir -p "{run_dir}/stop-requests"\n'
                                       f'ln -s "$HOME/auth.json" "{run_dir}/stop-requests/planted.json"\n'
                                       f'echo {SECRET}\necho {SECRET} >&2\n')
        code, record, out, _ = self.run_helper(app, record_path)
        self.assertEqual(code, 0, out)
        self.assertNotIn(SECRET, self.everything_written(run_dir, out))
        self.assertTrue(launch.inside(record['output']['path'], record['home']))

    def test_reviewer_remove_never_names_what_is_under_the_home(self):
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


class LaunchFolderByIdentity(Fixture):  # INVARIANT 5
    def test_reviewer_a_marker_copied_into_a_replacement_folder_is_refused(self):
        app, record_path, folder, _ = self.made()
        folder.rename(self.parent / 'moved')
        (folder / launch.CONTROL).mkdir(parents=True)
        (folder / launch.HOME).mkdir()
        (folder / 'precious').write_text("not the helper's")
        for name in (launch.MARKER, launch.STATE):
            shutil.copy(self.parent / 'moved' / launch.CONTROL / name, folder / launch.CONTROL / name)
        code, out = self.call('remove', '--launch-folder', str(folder))
        self.assert_refused(code, out, 'recorded identity differs')
        self.assertTrue((folder / 'precious').exists())
        code, _, out, run_dir = self.run_helper(app, record_path, reuse=folder)
        self.assert_refused(code, out, 'recorded identity differs')

    def test_reviewer_a_living_member_of_the_apps_group_keeps_the_folder_in_use(self):
        app, record_path, folder, record = self.made('sleep 30 &\n')
        state = launch.read_own(folder / launch.CONTROL / launch.STATE, launch.STATE_FORMAT, 'the custody state')
        self.assertEqual(state['process_group'], record['pid'])
        self.assert_refused(*self.call('remove', '--launch-folder', str(folder)), 'in use')
        code, _, out, _ = self.run_helper(app, record_path, reuse=folder)
        self.assert_refused(code, out, 'in use')
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

    def test_removal_refuses_the_real_home_checkouts_links_and_unmarked_folders(self):
        _, _, folder, _ = self.made()
        unmarked = self.parent / 'unmarked'
        (unmarked / launch.CONTROL).mkdir(parents=True)
        link = self.tmp / 'link-to-folder'
        link.symlink_to(folder)
        for name, path in (('unmarked', unmarked), ('the real home', self.real),
                           ('a folder containing the real home', self.tmp), ('this repository', launch.REPOSITORY),
                           ('a link to a launch folder', link)):
            with self.subTest(name):
                self.assertEqual(self.call('remove', '--launch-folder', str(path))[0], 2)
        self.assertTrue(folder.exists() and self.real.exists())
        self.assertEqual(self.call('remove', '--launch-folder', str(folder))[0], 0)


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

    def test_finding_8_an_unreadable_property_list_is_a_structured_refusal(self):
        app, record_path = self.bundle()
        for error in (plistlib.InvalidFileException(), ExpatError('invented')):
            with self.subTest(type(error).__name__), mock.patch.object(identify, 'validate_record'), \
                    mock.patch.object(identify, 'check', side_effect=error):
                code, _, out, _ = self.run_helper(app, record_path)
                self.assertEqual(code, 2)
                self.assertIn('error', json.loads(out.strip().splitlines()[-1]))

    @unittest.skipUnless(MAC, "identification's check reads live macOS metadata")
    def test_reviewer_a_changed_resource_is_refused_and_the_identified_bundle_launches(self):
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


class Overrides(Fixture):  # INVARIANT 7
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
        self.assertEqual(record['overrides_passed'], {name: env[name] for name in HELD})

    def test_an_owners_sitting_launch_is_passed_the_allowlist_without_the_nine(self):
        app, record_path = self.bundle()
        with mock.patch.dict(os.environ, INVENTED_SECRETS):
            code, record, out, _ = self.run_helper(app, record_path, '--app-env', 'CHIRALITY_WORKSPACE=/invented', owner=True)
        self.assertEqual(code, 0, out)
        self.assertEqual(record['home_kind'], 'owners-sitting')
        self.assertEqual(set(self.received(record)) - SHELL_OWN,
                         {'HOME', 'CFFIXED_USER_HOME', 'TMPDIR', 'PATH', 'LANG', 'CHIRALITY_WORKSPACE'})
        self.assertEqual(record['overrides_passed'], "none (an owner's-sitting launch)")
        code, _, out, _ = self.run_helper(app, record_path, '--model-address', 'http://127.0.0.1:8080/v1', owner=True)
        self.assert_refused(code, out, "owner's-sitting")

    def test_the_kind_is_fixed_when_the_home_is_made(self):
        app, record_path, folder, _ = self.made()
        code, _, out, run_dir = self.run_helper(app, record_path, reuse=folder, owner=True)
        self.assert_refused(code, out, 'contradicts')
        self.assertFalse(run_dir.exists())
        owner_app, owner_record = self.bundle(where='owner')
        code, record, out, _ = self.run_helper(owner_app, owner_record, owner=True)
        folder = Path(record['launch_folder']['launch_folder'])
        code, record, out, _ = self.run_helper(owner_app, owner_record, reuse=folder)
        self.assertEqual((code, record['home_kind']), (0, 'owners-sitting'), out)

    def test_no_redirected_signed_in_home_and_no_unredirected_other_home(self):
        owner_app, owner_record = self.bundle(where='owner')
        code, record, out, _ = self.run_helper(owner_app, owner_record, owner=True)
        owner_folder = Path(record['launch_folder']['launch_folder'])
        app, record_path, other_folder, _ = self.made()
        with self.subTest("the stub-address option on an owner's-sitting home"):
            code, _, out, run_dir = self.run_helper(owner_app, owner_record, '--model-address', 'http://127.0.0.1:8080/v1',
                                                    reuse=owner_folder)
            self.assert_refused(code, out, "owner's-sitting")
            self.assertFalse(run_dir.exists())
        built = launch.child_environment
        with self.subTest("overrides put into an owner's-sitting launch's mapping"):
            with mock.patch.object(launch, 'child_environment',
                                   lambda h, i, l, k, *a: built(h, i, l, 'not-owners-sitting')):
                code, record, out, _ = self.run_helper(owner_app, owner_record, reuse=owner_folder)
            self.assertEqual((code, record['outcome']), (2, 'not launched'), out)
        with self.subTest("overrides left out of another home's mapping"):
            with mock.patch.object(launch, 'child_environment', lambda h, i, l, k, *a: built(h, i, l, 'owners-sitting')):
                code, record, out, _ = self.run_helper(app, record_path, reuse=other_folder)
            self.assertEqual((code, record['outcome']), (2, 'not launched'), out)
        for folder, edited in ((owner_folder, 'not-owners-sitting'), (other_folder, 'owners-sitting')):
            with self.subTest('the kind edited in the control folder', to=edited):
                marker_path = folder / launch.CONTROL / launch.MARKER
                marker = json.loads(marker_path.read_text())
                marker['kind'] = edited
                marker_path.unlink()
                marker_path.write_text(json.dumps(marker))  # a valid closed-format marker: the name check catches it
                code, _, out, run_dir = self.run_helper(app, record_path, reuse=folder)
                self.assert_refused(code, out, 'does not agree with its name')
                self.assertFalse(run_dir.exists())

    def test_a_marker_without_a_valid_kind_is_refused(self):
        for kind in ('owner', None):
            with self.subTest(kind):
                app, record_path, folder, _ = self.made()
                marker_path = folder / launch.CONTROL / launch.MARKER
                marker = json.loads(marker_path.read_text())
                if kind is None:
                    del marker['kind']
                else:
                    marker['kind'] = kind
                marker_path.unlink()
                marker_path.write_text(json.dumps(marker))
                code, _, out, _ = self.run_helper(app, record_path, reuse=folder)
                self.assertEqual(code, 2, out)

    def test_each_of_the_nine_removed_or_altered_just_before_launch_is_refused(self):
        home = self.parent / 'h'
        good = launch.child_environment(home, {}, 'en_US.UTF-8', 'not-owners-sitting')
        owner = launch.child_environment(home, {}, 'en_US.UTF-8', 'owners-sitting')
        launch.check_environment(owner, home, 'owners-sitting')
        for name in sorted(HELD):
            for case, env in (('removed', {k: v for k, v in good.items() if k != name}),
                              ('altered', {**good, name: 'http://203.0.113.1:8080'})):
                with self.subTest(name=name, case=case), self.assertRaises(ValueError):
                    launch.check_environment(env, home, 'not-owners-sitting')
            with self.subTest(name=name, case="present for an owner's sitting"), self.assertRaises(ValueError):
                launch.check_environment({**owner, name: good[name]}, home, 'owners-sitting')

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
        code, _, out, run_dir = self.run_helper(app, record_path, '--model-address', 'http://localhost:8080/v1')
        self.assert_refused(code, out, launch.MODEL_ADDRESS)
        code, record, out, _ = self.run_helper(app, record_path, '--model-address', 'http://127.0.0.1:8080/v1')
        self.assertEqual(self.received(record)[launch.MODEL_ADDRESS], 'http://127.0.0.1:8080/v1')

    def test_whether_the_executable_contains_the_inputs_name_is_reported_as_exactly_that(self):
        app, record_path = self.bundle()
        code, record, out, _ = self.run_helper(app, record_path)
        note = record['address_override_input']
        self.assertEqual(note['executable'], 'the name was not found in the executable')
        self.assertEqual(note['note'], 'this build reads no address override; only the proxy overrides apply to it')
        app, record_path = self.bundle(where='with-input', extra_bytes=launch.MODEL_ADDRESS)
        code, record, out, _ = self.run_helper(app, record_path)
        self.assertEqual(code, 0, out)
        self.assertEqual(record['address_override_input']['executable'], 'the name was found in the executable')
        self.assertNotIn('note', record['address_override_input'])


class Housekeeping(unittest.TestCase):
    def test_the_real_home_is_the_account_home_not_the_home_variable(self):
        with mock.patch.dict(os.environ, {'HOME': '/invented/elsewhere'}):
            self.assertEqual(launch.real_home(), Path(os.path.realpath(pwd.getpwuid(os.getuid()).pw_dir)))

    def test_finding_9_running_the_helper_writes_no_bytecode(self):
        prefix = Path(tempfile.mkdtemp(dir=_PRIVATE_TMP))
        self.addCleanup(remove_fixture, prefix)
        env = {k: v for k, v in os.environ.items() if k != 'PYTHONDONTWRITEBYTECODE'}
        env['PYTHONPYCACHEPREFIX'] = str(prefix)
        subprocess.run([sys.executable, str(HELPER), '--help'], env=env, check=True, capture_output=True)
        written = [f for _, _, files in os.walk(prefix) for f in files]
        self.assertEqual([f for f in written if f.startswith(('identify.', 'bundled_supplier.', 'launch.'))], [])


if __name__ == '__main__':
    unittest.main()
