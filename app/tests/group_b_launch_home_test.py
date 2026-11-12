"""The examination launch helper, one test class per invariant, with invented material only.

A shell script plays the App and a folder stands in for the real home and the
per-user cache folder. No App, window or real home Library is touched; nothing
here launches a real build.
"""
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
INVENTED_SECRETS = {'ANTHROPIC_AUTH_TOKEN': 'invented-token-1', 'CLAUDE_CODE_MESSAGING_TOKEN': 'invented-token-2',
                    'SSH_AUTH_SOCK': '/invented/agent.sock', 'OPENAI_API_KEY': 'invented-key-3'}
PLAYS_THE_APP = '''#!/bin/sh
env > "$HOME/received-env.txt"
mkdir -p "$HOME/Library/Application Support/{id}" "$HOME/Library/WebKit/{id}/WebsiteData" "$HOME/Library/Caches/{id}"
echo invented > "$HOME/Library/Application Support/{id}/state"
echo invented > "$HOME/Library/WebKit/{id}/WebsiteData/store"
'''
SHELL_OWN = {'PWD', 'SHLVL', '_', 'OLDPWD', '__CF_USER_TEXT_ENCODING'}  # set by /bin/sh or the macOS runtime itself

_PRIVATE_TMP = None


def setUpModule():
    """Fixtures live in a private folder under the account's home, made for this run and removed after it."""
    global _PRIVATE_TMP
    _PRIVATE_TMP = tempfile.mkdtemp(prefix='.launch-home-test-', dir=os.path.realpath(pwd.getpwuid(os.getuid()).pw_dir))


def tearDownModule():
    for current, dirs, _ in os.walk(_PRIVATE_TMP):  # a test may leave a folder without read permission
        for name in dirs:
            with contextlib.suppress(OSError):
                os.chmod(os.path.join(current, name), 0o700, follow_symlinks=False)
    shutil.rmtree(_PRIVATE_TMP, ignore_errors=True)


def fake_identification(app, record_path):
    """Stands in for identify_candidate (INVARIANT 6 has its own tests): returns the invented record."""
    return json.loads(Path(record_path).read_text())


class Fixture(unittest.TestCase):
    identification = staticmethod(fake_identification)

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(dir=_PRIVATE_TMP))
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
        self.parent = self.tmp / 'homes'
        self.parent.mkdir()
        self.runs = 0

    def bundle(self, script='', identifier=IDENTIFIER, where='build', exit_status=0, shebang=None,
               executable=EXECUTABLE, name=PRODUCT + '.app'):
        app = self.tmp / where / name
        (app / 'Contents/MacOS').mkdir(parents=True)
        (app / 'Contents/Resources/instructions').mkdir(parents=True)
        (app / 'Contents/Resources/instructions/AGENTS.md').write_text('invented guidance\n')
        (app / 'Contents/Info.plist').write_bytes(plistlib.dumps({
            'CFBundleIdentifier': identifier, 'CFBundleName': PRODUCT, 'CFBundleDisplayName': PRODUCT,
            'CFBundleExecutable': executable, 'CFBundleShortVersionString': '0.0.0'}))
        body = PLAYS_THE_APP.format(id=identifier) + script + f'exit {exit_status}\n'
        if shebang:
            body = shebang + '\n' + body.split('\n', 1)[1]
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

    def run_helper(self, app, record, *extra, home=None, settle='0', run_dir=None):
        self.runs += 1
        run_dir = run_dir or self.tmp / f'run-{self.runs}'
        argv = ['launch', '--app', str(app), '--record', str(record), '--run-dir', str(run_dir),
                '--settle-seconds', settle, *extra]
        argv += ['--reuse-home', str(home)] if home else ['--home-parent', str(self.parent)]
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = launch.main(argv)
        saved = Path(run_dir) / launch.RECORD
        return code, (json.loads(saved.read_text()) if saved.exists() else None), err.getvalue(), Path(run_dir)

    def received(self, record):
        lines = (Path(record['home']['path']) / 'received-env.txt').read_text().splitlines()
        return dict(line.split('=', 1) for line in lines if '=' in line)

    def assert_refused(self, code, err, reason):
        self.assertEqual(code, 2, err)
        self.assertIn(reason, json.loads(err.strip().splitlines()[-1])['error'])

    def stop_when_running(self, run_dir, act):
        def wait_then_act():
            deadline = time.monotonic() + 10
            while time.monotonic() < deadline and not (run_dir / launch.PROCESS).exists():
                time.sleep(0.05)
            time.sleep(0.3)
            if (run_dir / launch.PROCESS).exists():  # never signal unless the helper launched and installed its forwarding
                act()
        thread = threading.Thread(target=wait_then_act)
        thread.start()
        return thread


class EnvironmentFromNothing(Fixture):  # INVARIANT 1
    def test_reviewer_child_receives_exactly_the_allowlist_while_the_helper_holds_tokens(self):
        app, record_path = self.bundle()
        with mock.patch.dict(os.environ, {**INVENTED_SECRETS, 'LANG': 'fr_FR.UTF-8', 'USER': 'invented'}):
            code, record, err, _ = self.run_helper(app, record_path, '--app-env', 'CHIRALITY_RECORDS_STORE=/invented/store')
        self.assertEqual(code, 0, err)
        env = self.received(record)
        home = record['home']['path']
        self.assertEqual(set(env) - SHELL_OWN, {'HOME', 'CFFIXED_USER_HOME', 'TMPDIR', 'PATH', 'LANG',
                                                'CHIRALITY_RECORDS_STORE'})
        for name, value in INVENTED_SECRETS.items():
            self.assertNotIn(name, env)
            self.assertNotIn(value, (Path(home) / 'received-env.txt').read_text())
        self.assertEqual((env['HOME'], env['CFFIXED_USER_HOME']), (home, home))
        self.assertEqual(env['TMPDIR'], f'{home}/{launch.OWN}/tmp')
        self.assertEqual((env['PATH'], env['LANG']), (launch.SYSTEM_PATH, launch.DEFAULT_LANG))
        self.assertEqual(record['environment'], {k: env[k] for k in record['environment']})
        self.assertEqual(set(record['environment']), set(env) - SHELL_OWN)

    def test_the_environment_is_checked_against_the_allowlist_immediately_before_start(self):
        home = self.parent / 'h'
        (home / launch.OWN / 'tmp').mkdir(parents=True)
        good = launch.child_environment(home, {}, 'en_US.UTF-8')
        launch.check_environment(good, home)
        other = self.parent / 'other'; other.mkdir()
        cases = {
            'inherited name': {**good, 'SSH_AUTH_SOCK': '/x'},
            'HOME alone': {k: v for k, v in good.items() if k != 'CFFIXED_USER_HOME'},
            'CFFIXED_USER_HOME alone': {k: v for k, v in good.items() if k != 'HOME'},
            'homes differ': {**good, 'CFFIXED_USER_HOME': str(other)},
            'TMPDIR outside': {**good, 'TMPDIR': str(other)},
            'other PATH': {**good, 'PATH': '/opt/invented/bin:' + launch.SYSTEM_PATH},
        }
        for name, env in cases.items():
            with self.subTest(name), self.assertRaises(ValueError):
                launch.check_environment(env, home)
        for pair in ('HOME=/x', 'CFFIXED_USER_HOME=/x', 'OPENAI_API_KEY=x', 'CHIRALITY_WORKSPACE', 'PATH=/x'):
            with self.subTest(pair), self.assertRaises(ValueError):
                launch.app_inputs([pair])

    def test_a_name_added_after_construction_is_refused_and_nothing_launches(self):
        app, record_path = self.bundle()
        built = launch.child_environment
        with mock.patch.object(launch, 'child_environment', lambda *a: {**built(*a), 'SSH_AUTH_SOCK': '/x'}):
            code, record, _, _ = self.run_helper(app, record_path)
        self.assertEqual((code, record['outcome'], record['started_at']), (2, 'not launched', None))
        self.assertFalse((Path(record['home']['path']) / 'received-env.txt').exists())


class CleanMeansEverything(Fixture):  # INVARIANT 2
    def link_case(self, setup, script):
        outside = self.tmp / 'outside'; outside.mkdir(exist_ok=True)
        setup(outside)
        app, record_path = self.bundle(script, where=f'link-{self.runs}')
        return self.run_helper(app, record_path)

    def test_reviewer_links_at_or_beneath_a_watched_place_make_the_comparison_incomplete(self):
        lib = self.real / 'Library'
        cases = {
            'watched folder is a link': (
                lambda o: ((o / 'caches' / IDENTIFIER).mkdir(parents=True), (o / 'caches' / IDENTIFIER / 'f').write_text('a'),
                           (lib / 'Caches').symlink_to(o / 'caches')),
                f'echo b >> "{lib}/Caches/{IDENTIFIER}/f"\n', 'Caches'),
            'watched entry is a link': (
                lambda o: ((o / 'support').mkdir(), (o / 'support/f').write_text('a'),
                           (lib / 'Application Support').mkdir(),
                           (lib / 'Application Support' / IDENTIFIER).symlink_to(o / 'support')),
                f'echo b >> "{lib}/Application Support/{IDENTIFIER}/f"\n', f'Application Support/{IDENTIFIER}'),
            'link beneath a watched entry': (
                lambda o: ((o / 'webkit').mkdir(), (o / 'webkit/f').write_text('a'),
                           (lib / 'WebKit' / IDENTIFIER).mkdir(parents=True),
                           (lib / 'WebKit' / IDENTIFIER / 'data').symlink_to(o / 'webkit')),
                f'echo b >> "{lib}/WebKit/{IDENTIFIER}/data/f"\n', f'WebKit/{IDENTIFIER}/data'),
        }
        for name, (setup, script, link) in cases.items():
            with self.subTest(name):
                code, record, err, _ = self.link_case(setup, script)
                self.assertEqual((code, record['outcome']), (1, 'failed'), err)
                self.assertEqual(record['real_library']['result'], 'incomplete')
                self.assertIn(link, record['real_library']['links_met'])
                self.assertTrue(any('incomplete' in f for f in record['failures']))
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
        self.assertEqual(record['real_library']['changes'], [])

    def test_reviewer_a_stopped_app_that_exits_zero_is_not_clean(self):
        app, record_path = self.bundle("trap 'exit 0' TERM\nwhile :; do sleep 0.1; done\n", where='trapping')
        run_dir = self.tmp / f'run-{self.runs + 1}'
        stopped = []
        thread = self.stop_when_running(run_dir, lambda: stopped.append(launch.stop(run_dir)))
        code, record, _, _ = self.run_helper(app, record_path, settle='0.5')
        thread.join()
        self.assertEqual(record['ended'], 'exited with status 0')
        self.assertEqual((code, record['outcome']), (1, 'failed'))
        self.assertEqual([r['by'] for r in record['stop_requests']], ['stop command'])
        self.assertTrue(any('stop was requested' in f for f in record['failures']))
        with self.assertRaisesRegex(ValueError, 'already ended'):
            launch.stop(run_dir)

    def test_a_signal_forwarded_by_the_helper_is_a_stop_request(self):
        app, record_path = self.bundle("trap 'exit 0' TERM\nwhile :; do sleep 0.1; done\n", where='forwarded')
        run_dir = self.tmp / f'run-{self.runs + 1}'
        thread = self.stop_when_running(run_dir, lambda: os.kill(os.getpid(), signal.SIGTERM))
        code, record, _, _ = self.run_helper(app, record_path, settle='0.5')
        thread.join()
        self.assertEqual((record['ended'], code, record['outcome']), ('exited with status 0', 1, 'failed'))
        self.assertIn('SIGTERM to the helper', record['stop_requests'][0]['by'])

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

                def listing(*args):
                    calls.append(1)
                    if failing == 'before' or (failing == 'after' and len(calls) > 2):
                        raise PermissionError('invented: listing refused')
                    return real_listing(*args)
                with mock.patch.object(launch, 'listing', listing):
                    code, record, err, _ = self.run_helper(app, record_path)
                if record.get('pid'):
                    with contextlib.suppress(ProcessLookupError, PermissionError):
                        os.killpg(record['pid'], signal.SIGKILL)
                self.assertEqual(code, expected, err)
                self.assertNotEqual(record['outcome'], 'clean')
                if failing:
                    self.assertEqual(record['real_library']['result'], 'not made')

    def test_the_record_states_its_fields_and_is_written_once(self):
        app, record_path = self.bundle()
        code, record, err, run_dir = self.run_helper(app, record_path)
        self.assertEqual((code, record['outcome']), (0, 'clean'), err)
        self.assertEqual(list(record)[0], 'note')
        self.assertIn('not an examination record format', record['note'])
        for field in ('candidate_key', 'identifier', 'bundle', 'home', 'environment', 'started_at', 'ended_at',
                      'ended', 'pid', 'process_group_after_settle', 'real_library', 'stop_requests', 'disclosed',
                      'output', 'failures', 'outcome', 'watched'):
            self.assertIn(field, record)
        self.assertEqual(record['real_library']['result'], 'unchanged')
        self.assertTrue((Path(record['home']['path']) / f'Library/WebKit/{IDENTIFIER}/WebsiteData/store').exists())
        with self.assertRaises(FileExistsError):
            launch._write_new(run_dir / launch.RECORD, {})


class WatchedByExactName(Fixture):  # INVARIANT 3
    def test_reviewer_an_executable_name_that_does_not_discriminate_is_refused(self):
        for index, name in enumerate(('a', 'app', 'chirality', 'Chirality-x')):
            with self.subTest(name):
                app, record_path = self.bundle(executable=name, where=f'short{index}')
                code, record, err, run_dir = self.run_helper(app, record_path)
                self.assert_refused(code, err, 'does not discriminate')
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
        script = (f'echo x > "{caches}/{EXECUTABLE}.old"\n'
                  f'mkdir -p "{caches}/{IDENTIFIER}2"\n')
        app, record_path = self.bundle(script)
        code, record, err, _ = self.run_helper(app, record_path)
        self.assertEqual((code, record['outcome']), (0, 'clean'), err)

    def test_the_per_user_cache_folder_is_disclosed_and_never_a_failure(self):
        helper = f'com.apple.WebKit.WebContent+{EXECUTABLE.replace("-", "_")}-0a1b'
        script = (f'mkdir -p "{self.cache}/{helper}" "{self.cache}/{IDENTIFIER}"\n'
                  f'echo x > "{self.cache}/{helper}/data"\necho x > "{self.cache}/unrelated"\n')
        app, record_path = self.bundle(script)
        code, record, err, _ = self.run_helper(app, record_path)
        self.assertEqual((code, record['outcome']), (0, 'clean'), err)
        disclosed = {(c['path'], c['change']) for c in record['disclosed']['user_cache']['changes']}
        self.assertEqual(disclosed, {(helper, 'created'), (helper + '/data', 'created'), (IDENTIFIER, 'created')})
        self.assertTrue((self.cache / helper / 'data').exists())

    def test_a_changed_system_preference_is_disclosed_and_one_named_for_the_build_fails(self):
        prefs = self.real / 'Library/Preferences'
        app, record_path = self.bundle(f'echo x > "{prefs}/com.apple.spaces.plist"\necho y >> "{prefs}/com.apple.dock.plist"\n')
        code, record, err, _ = self.run_helper(app, record_path)
        self.assertEqual((code, record['outcome']), (0, 'clean'), err)
        self.assertEqual({(c['path'], c['change']) for c in record['disclosed']['preferences']},
                         {('com.apple.spaces.plist', 'created'), ('com.apple.dock.plist', 'modified')})
        app, record_path = self.bundle(f'echo x > "{prefs}/{IDENTIFIER}.plist"\n', where='named')
        code, record, err, _ = self.run_helper(app, record_path)
        self.assertEqual((code, record['real_library']['result']), (1, 'changed'), err)
        self.assertEqual(record['real_library']['changes'], [{'path': f'Preferences/{IDENTIFIER}.plist', 'change': 'created'}])
        self.assertEqual(record['disclosed']['preferences'], [])


class PlacesByIdentity(Fixture):  # INVARIANT 4
    def case_insensitive(self):
        probe = self.tmp / 'CaseProbe'
        probe.write_text('')
        return (self.tmp / 'caseprobe').exists()

    def test_reviewer_lower_case_spellings_reach_the_protected_places(self):
        if not self.case_insensitive():
            self.skipTest('needs a case-insensitive volume')
        app, record_path = self.bundle()
        (self.real / 'Library/Caches').mkdir()
        for name, run_dir in (('library', self.real / 'library/Caches/run'), ('LIBRARY', self.real / 'LIBRARY/run')):
            with self.subTest(name):
                code, _, err, _ = self.run_helper(app, record_path, run_dir=run_dir)
                self.assert_refused(code, err, 'inside the real home Library')
                self.assertFalse((self.real / 'Library/Caches/run').exists())
        lower = self.tmp / 'lower'
        app, record_path = self.bundle(where='lower/applications')
        code, _, err, _ = self.run_helper(app, record_path)
        self.assert_refused(code, err, 'Applications folder')
        self.assertTrue(lower.exists())

    def test_an_applications_folder_anywhere_and_in_any_case_is_refused(self):
        for index, where in enumerate(('elsewhere/Applications', 'deep/APPLICATIONS/x', 'real-home/Applications')):
            with self.subTest(where):
                app, record_path = self.bundle(where=where)
                code, _, err, run_dir = self.run_helper(app, record_path)
                self.assert_refused(code, err, 'Applications folder')
                self.assertFalse(run_dir.exists())
        link = self.tmp / 'via-link'
        (self.tmp / 'elsewhere').mkdir(exist_ok=True)
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
        cases = (('run folder through a link into the Library', ['--run-dir', str(into_library / 'run')], 'real home Library'),
                 ('run folder in this repository', ['--run-dir', str(launch.REPOSITORY / 'launch-run')], 'checkout'),
                 ('home parent through a link into a checkout', ['--home-parent', str(into_checkout)], 'checkout'))
        for name, argv, reason in cases:
            with self.subTest(name):
                full = ['launch', '--app', str(app), '--record', str(record_path), '--settle-seconds', '0']
                full += argv if '--run-dir' in argv else ['--run-dir', str(self.tmp / 'r'), *argv]
                full += [] if '--home-parent' in argv else ['--home-parent', str(self.parent)]
                err = io.StringIO()
                with contextlib.redirect_stderr(err), contextlib.redirect_stdout(io.StringIO()):
                    code = launch.main(full)
                self.assert_refused(code, err.getvalue(), reason)
                self.assertFalse((self.tmp / 'r').exists())
        self.assertFalse((self.real / 'Library/run').exists())
        self.assertFalse((launch.REPOSITORY / 'launch-run').exists())
        self.assertEqual(os.listdir(checkout), ['.git'])


class HomeByIdentity(Fixture):  # INVARIANT 5
    def made_home(self, script=''):
        app, record_path = self.bundle(script, where=f'home{self.runs}')
        code, record, err, _ = self.run_helper(app, record_path)
        return app, record_path, Path(record['home']['path']), record

    def test_reviewer_a_marker_copied_into_a_replacement_directory_is_refused(self):
        app, record_path, home, _ = self.made_home()
        home.rename(self.parent / 'moved')
        (home / launch.OWN).mkdir(parents=True)
        (home / 'precious').write_text('not the helper\'s')
        shutil.copy(self.parent / 'moved' / launch.OWN / launch.MARKER, home / launch.OWN / launch.MARKER)
        with self.assertRaisesRegex(ValueError, 'recorded identity differs'):
            launch.remove(home)
        self.assertTrue((home / 'precious').exists())
        code, _, err, run_dir = self.run_helper(app, record_path, home=home)
        self.assert_refused(code, err, 'recorded identity differs')
        self.assertFalse(run_dir.exists())

    def test_reviewer_a_living_member_of_the_apps_group_keeps_the_home_in_use(self):
        app, record_path, home, record = self.made_home('sleep 30 &\n')
        try:
            self.assertEqual(launch.read_state(home)['process_group'], record['pid'])
            with self.assertRaisesRegex(ValueError, 'in use'):
                launch.remove(home)
            code, _, err, _ = self.run_helper(app, record_path, home=home)
            self.assert_refused(code, err, 'in use')
        finally:
            os.killpg(record['pid'], signal.SIGKILL)
        deadline = time.monotonic() + 5
        while launch.group_state(record['pid']) != 'gone' and time.monotonic() < deadline:
            time.sleep(0.05)
        self.assertEqual(launch.remove(home), {'removed': str(home)})

    def test_reviewer_reuse_does_not_look_into_the_home(self):
        app, record_path, home, _ = self.made_home()
        home.chmod(0o300)  # the helper may enter its own folder but cannot list the home
        try:
            code, record, err, _ = self.run_helper(app, record_path, home=home)
        finally:
            home.chmod(0o700)
        self.assertEqual((code, record['outcome']), (0, 'clean'), err)
        self.assertEqual(record['home'], {'path': str(home), 'state': 'reused'})

    def test_reviewer_the_apps_output_stays_inside_the_home(self):
        secret = 'invented-secret-from-the-home-7f3a'
        app, record_path, home, record = self.made_home(f'echo {secret}\necho {secret} >&2\n')
        output = Path(record['output']['path'])
        self.assertTrue(launch.inside(output, home))
        self.assertEqual(record['output']['size'], output.stat().st_size)
        self.assertIn(secret, output.read_text())
        run_dir = self.tmp / f'run-{self.runs}'
        for current, _, files in os.walk(run_dir):
            for name in files:
                self.assertNotIn(secret, (Path(current) / name).read_text(), name)

    def test_removal_refuses_the_real_home_checkouts_links_and_unmarked_folders(self):
        _, _, home, _ = self.made_home()
        unmarked = self.parent / 'unmarked'; unmarked.mkdir()
        (self.real / launch.OWN).mkdir()
        info = self.real.stat()
        (self.real / launch.OWN / launch.MARKER).write_text(json.dumps({
            'made_by': launch.TOOL, 'path': str(self.real), 'device': info.st_dev, 'inode': info.st_ino}))
        link = self.tmp / 'link-to-home'; link.symlink_to(home)
        for name, path in (('unmarked', unmarked), ('the real home, even marked', self.real),
                           ('a folder containing the real home', self.tmp), ('this repository', launch.REPOSITORY),
                           ('a link to a marked home', link)):
            with self.subTest(name), self.assertRaises(ValueError):
                launch.remove(path)
        self.assertTrue(home.exists() and self.real.exists())
        self.assertEqual(launch.remove(home), {'removed': str(home)})


class OnlyTheIdentifiedCandidate(Fixture):  # INVARIANT 6
    identification = None  # identification's own validation and check, not the stand-in

    def test_unknown_format_or_missing_key_is_refused(self):
        app, record_path = self.bundle()
        record = json.loads(record_path.read_text())
        for name, value in (('unknown format', {**record, 'format': 'invented/v9'}),
                            ('empty candidate key', {**record, 'candidate_key': ''})):
            with self.subTest(name):
                record_path.write_text(json.dumps(value))
                code, _, err, run_dir = self.run_helper(app, record_path)
                self.assertEqual(code, 2, err)
                self.assertFalse(run_dir.exists())

    def test_a_check_that_finds_a_difference_is_refused(self):
        app, record_path = self.bundle()
        same = {'equal': True, 'build_identity': 'x', 'recorded_build_identity': 'x', 'record_fields_mismatched': []}
        for name, result in (('inventory differs', {**same, 'equal': False, 'changed': ['Contents/Resources/x']}),
                             ('identity differs', {**same, 'build_identity': 'y'}),
                             ('record fields differ', {**same, 'record_fields_mismatched': ['identifier']})):
            with self.subTest(name), mock.patch.object(identify, 'validate_record'), \
                    mock.patch.object(identify, 'check', return_value=result):
                code, _, err, run_dir = self.run_helper(app, record_path)
                self.assert_refused(code, err, 'differs from its identification record')
                self.assertFalse(run_dir.exists())

    def test_finding_8_an_unreadable_property_list_is_a_structured_refusal(self):
        app, record_path = self.bundle()
        for error in (plistlib.InvalidFileException(), ExpatError('invented')):
            with self.subTest(type(error).__name__), mock.patch.object(identify, 'validate_record'), \
                    mock.patch.object(identify, 'check', side_effect=error):
                code, _, err, _ = self.run_helper(app, record_path)
                self.assertEqual(code, 2)
                self.assertIn('error', json.loads(err.strip().splitlines()[-1]))

    @unittest.skipUnless(MAC, "identification's check reads live macOS metadata")
    def test_reviewer_a_changed_resource_is_refused_and_the_identified_bundle_launches(self):
        app, record_path = self.bundle()
        repo = self.tmp / 'repo'; (repo / 'src').mkdir(parents=True)
        (repo / 'src/main.rs').write_text('fn main() {}\n')
        env = {'PATH': launch.SYSTEM_PATH, 'HOME': str(self.tmp), 'GIT_CONFIG_NOSYSTEM': '1',
               'GIT_AUTHOR_NAME': 'Fixture', 'GIT_AUTHOR_EMAIL': 'fixture@example.invalid',
               'GIT_COMMITTER_NAME': 'Fixture', 'GIT_COMMITTER_EMAIL': 'fixture@example.invalid'}
        for command in (['init', '-q'], ['add', '.'], ['commit', '-q', '-m', 'fixture']):
            subprocess.run(['git', '-C', str(repo), *command], check=True, env=env, capture_output=True)
        export = self.tmp / 'export'; export.mkdir()
        subprocess.run(['tar', '-x', '-C', str(export)], input=identify.git(repo, 'archive', 'HEAD'), check=True)
        facts = self.tmp / 'facts.json'
        facts.write_text(json.dumps({'procedure': 'invented', 'profile': 'debug', 'signing': 'none', 'features': [],
                                     'command': ['build'], 'config_overlays': [], 'toolchain': {}, 'lockfiles': {},
                                     'offline': True, 'environment': {}, 'started_at': '2000-01-01T00:00:00Z',
                                     'finished_at': '2000-01-01T00:00:00Z'}))
        out = self.tmp / 'identification'
        with mock.patch.object(Path, 'home', return_value=self.real), contextlib.redirect_stdout(io.StringIO()):
            code = identify.main(['record', '--app', str(app), '--repo', str(repo), '--revision', 'HEAD',
                                  '--export-root', str(export), '--build-facts', str(facts),
                                  '--identified-at', '2000-01-01T00:00:00Z', '--out-dir', str(out)])
        self.assertEqual(code, 0)
        record_path = out / 'candidate-identification.json'
        code, record, err, _ = self.run_helper(app, record_path)
        self.assertEqual((code, record['outcome']), (0, 'clean'), err)
        self.assertEqual(record['candidate_key'], json.loads(record_path.read_text())['candidate_key'])
        (app / 'Contents/Resources/instructions/AGENTS.md').write_text('changed after identification\n')
        code, _, err, run_dir = self.run_helper(app, record_path)
        self.assert_refused(code, err, 'Contents/Resources/instructions/AGENTS.md')
        self.assertFalse(run_dir.exists())


class Housekeeping(unittest.TestCase):
    def test_the_real_home_is_the_account_home_not_the_home_variable(self):
        with mock.patch.dict(os.environ, {'HOME': '/invented/elsewhere'}):
            self.assertEqual(launch.real_home(), Path(os.path.realpath(pwd.getpwuid(os.getuid()).pw_dir)))

    def test_finding_9_running_the_helper_writes_no_bytecode(self):
        prefix = Path(tempfile.mkdtemp(dir=_PRIVATE_TMP))
        env = {k: v for k, v in os.environ.items() if k != 'PYTHONDONTWRITEBYTECODE'}
        env['PYTHONPYCACHEPREFIX'] = str(prefix)
        subprocess.run([sys.executable, str(HELPER), '--help'], env=env, check=True, capture_output=True)
        written = [f for _, _, files in os.walk(prefix) for f in files]
        self.assertEqual([f for f in written if f.startswith(('identify.', 'bundled_supplier.', 'launch.'))], [])


if __name__ == '__main__':
    unittest.main()
