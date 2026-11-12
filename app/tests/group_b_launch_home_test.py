"""The examination launch helper with invented material: a shell script plays the App and a folder stands in for the real home.

No App, window or real home Library is touched; nothing here launches a real build.
"""
import contextlib
import hashlib
import io
import json
import os
from pathlib import Path
import plistlib
import pwd
import shutil
import signal
import tempfile
import threading
import time
import unittest
from unittest import mock

import importlib.util

APP = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('examination_launch', APP / 'examination/standalone/launch.py')
launch = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(launch)

IDENTIFIER = 'dev.chirality.app-v4.candidate.invented'
PRODUCT = 'Chirality App v4 (development invented)'
EXECUTABLE = 'chirality-app-v4'
PLAYS_THE_APP = '''#!/bin/sh
env > "$HOME/received-env.txt"
mkdir -p "$HOME/Library/Application Support/{id}" "$HOME/Library/WebKit/{id}/WebsiteData" "$HOME/Library/Caches/{id}"
echo invented > "$HOME/Library/Application Support/{id}/state"
echo invented > "$HOME/Library/WebKit/{id}/WebsiteData/store"
'''


class LaunchHome(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(os.path.realpath(tempfile.mkdtemp()))
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.real = self.tmp / 'real-home'  # stands in for the real home
        (self.real / 'Library/Preferences').mkdir(parents=True)
        (self.real / 'Library/Preferences/com.apple.dock.plist').write_bytes(b'invented system preference')
        patch = mock.patch.object(launch, 'real_home', return_value=self.real)
        patch.start()
        self.addCleanup(patch.stop)
        self.parent = self.tmp / 'homes'
        self.parent.mkdir()
        self.runs = 0

    def bundle(self, script='', identifier=IDENTIFIER, name=PRODUCT + '.app', product=PRODUCT,
               where='build', record_identifier=None, exit_status=0, shebang=None):
        app = self.tmp / where / name
        (app / 'Contents/MacOS').mkdir(parents=True)
        (app / 'Contents/Info.plist').write_bytes(plistlib.dumps({
            'CFBundleIdentifier': identifier, 'CFBundleName': product, 'CFBundleDisplayName': product,
            'CFBundleExecutable': EXECUTABLE}))
        body = PLAYS_THE_APP.format(id=identifier) + script + f'exit {exit_status}\n'
        if shebang:
            body = shebang + '\n' + body.split('\n', 1)[1]
        exe = app / 'Contents/MacOS' / EXECUTABLE
        exe.write_text(body)
        exe.chmod(0o755)
        record = {'candidate_key': '0123456789-abcdefabcdef',
                  'bundle': {'identifier': record_identifier or identifier, 'name': name,
                             'executable': {'path': 'Contents/MacOS/' + EXECUTABLE,
                                            'sha256': hashlib.sha256(exe.read_bytes()).hexdigest()}}}
        record_path = app.parent / 'candidate-identification.json'
        record_path.write_text(json.dumps(record))
        return app, record_path

    def run_helper(self, app, record, *extra, home=None):
        self.runs += 1
        run_dir = self.tmp / f'run-{self.runs}'
        argv = ['launch', '--app', str(app), '--record', str(record), '--run-dir', str(run_dir),
                '--settle-seconds', '0', *extra]
        argv += ['--reuse-home', str(home)] if home else ['--home-parent', str(self.parent)]
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = launch.main(argv)
        saved = run_dir / launch.RECORD
        return code, (json.loads(saved.read_text()) if saved.exists() else None), err.getvalue(), run_dir

    def received(self, record):
        lines = (Path(record['home']['path']) / 'received-env.txt').read_text().splitlines()
        return dict(line.split('=', 1) for line in lines if '=' in line)

    def test_child_receives_both_home_variables_equal_and_only_the_allowlist(self):
        app, record_path = self.bundle()
        code, record, err, _ = self.run_helper(app, record_path, '--app-env', 'CHIRALITY_RECORDS_STORE=/invented/store')
        self.assertEqual(code, 0, err)
        home = record['home']['path']
        env = self.received(record)
        self.assertEqual(env['HOME'], home)
        self.assertEqual(env['CFFIXED_USER_HOME'], home)
        shell_own = {'PWD', 'SHLVL', '_', 'OLDPWD'}  # set by /bin/sh itself
        self.assertEqual(set(env) - shell_own, {'HOME', 'CFFIXED_USER_HOME', 'LANG', 'PATH', 'TMPDIR',
                                                'CHIRALITY_RECORDS_STORE'})
        self.assertEqual(env['TMPDIR'], home + '/tmp')
        self.assertEqual(env['PATH'], launch.SYSTEM_PATH)
        self.assertEqual(record['environment'], {k: env[k] for k in record['environment']})
        self.assertEqual(record['home'], {'path': home, 'state': 'created', 'empty_when_created': True})
        self.assertTrue((Path(home) / f'Library/WebKit/{IDENTIFIER}/WebsiteData/store').exists())
        self.assertEqual(record['real_library']['result'], 'unchanged')
        self.assertEqual(record['outcome'], 'clean')

    def test_the_record_states_its_fields_and_is_not_a_record_format(self):
        app, record_path = self.bundle()
        code, record, err, run_dir = self.run_helper(app, record_path)
        self.assertEqual(code, 0, err)
        self.assertEqual(list(record)[0], 'note')
        self.assertIn('not an examination record format', record['note'])
        for field in ('candidate_key', 'identifier', 'bundle', 'home', 'environment', 'started_at', 'ended_at',
                      'ended', 'pid', 'process_group_after_settle', 'real_library', 'system_preferences_changed',
                      'failures', 'outcome'):
            self.assertIn(field, record)
        self.assertEqual((record['candidate_key'], record['identifier']), ('0123456789-abcdefabcdef', IDENTIFIER))
        self.assertEqual(record['bundle'], str(app))
        self.assertEqual(record['ended'], 'exited with status 0')
        self.assertEqual(record['process_group_after_settle'], 'gone')
        self.assertTrue(record['real_library']['compared'])
        self.assertEqual(json.loads((run_dir / launch.PIDFILE).read_text())['pid'], record['pid'])

    def test_one_home_variable_alone_differing_homes_or_extra_variables_refuse(self):
        home = str(self.parent / 'h')
        good = launch.plan_environment(home, {})
        self.assertEqual(launch.check_home_variables(good), home)
        cases = {
            'HOME alone': {k: v for k, v in good.items() if k != 'CFFIXED_USER_HOME'},
            'CFFIXED_USER_HOME alone': {k: v for k, v in good.items() if k != 'HOME'},
            'empty': {**good, 'CFFIXED_USER_HOME': ''},
            'differing': {**good, 'CFFIXED_USER_HOME': home + '-other'},
            'inherited variable': {**good, 'USER': 'someone'},
            'TMPDIR outside': {**good, 'TMPDIR': '/tmp'},
        }
        for name, env in cases.items():
            with self.subTest(name):
                with self.assertRaises(ValueError):
                    launch.check_home_variables(env)
        for pair in ('HOME=/x', 'CFFIXED_USER_HOME=/x', 'OPENAI_API_KEY=invented', 'CHIRALITY_WORKSPACE',
                     'PATH=/x'):
            with self.subTest(pair):
                with self.assertRaises(ValueError):
                    launch.app_inputs([pair])

    def test_release_identity_mismatches_and_applications_folders_refuse_before_anything_is_made(self):
        cases = {
            'release identifier': (dict(identifier='com.chirality.app'), 'development builds only'),
            'release file name': (dict(name='Chirality.app'), 'not named Chirality.app'),
            'release product name': (dict(product='Chirality'), 'release name Chirality'),
            'record names another identifier': (dict(record_identifier=IDENTIFIER + '-other'), 'differs from the record'),
            'under the real home Applications': (dict(where='real-home/Applications'), 'under an Applications folder'),
        }
        for index, (name, (options, reason)) in enumerate(cases.items()):
            with self.subTest(name):
                app, record_path = self.bundle(where=options.pop('where', f'case{index}'), **options)
                code, record, err, run_dir = self.run_helper(app, record_path)
                self.assertEqual(code, 2)
                self.assertIn(reason, json.loads(err.strip().splitlines()[-1])['error'])
                self.assertFalse(run_dir.exists())
                self.assertEqual(os.listdir(self.parent), [])
        with self.subTest('/Applications'):
            for path in ('/Applications/Invented Development.app', '/Users/invented/Applications/Invented.app'):
                with self.assertRaisesRegex(ValueError, 'under an Applications folder'):
                    launch.read_bundle(path, '/nonexistent')
        with self.subTest('executable bytes differ from the record'):
            app, record_path = self.bundle(where='changed')
            (app / 'Contents/MacOS' / EXECUTABLE).write_text('#!/bin/sh\nexit 0\n')
            code, _, err, run_dir = self.run_helper(app, record_path)
            self.assertEqual(code, 2)
            self.assertIn('differ from the identification record', err)
            self.assertFalse(run_dir.exists())

    def test_a_change_in_a_real_library_folder_named_for_the_build_fails_and_says_what_changed(self):
        caches = self.real / f'Library/Caches/{IDENTIFIER}'
        caches.mkdir(parents=True)
        (caches / 'existing').write_text('invented')
        leak = (f'mkdir -p "{self.real}/Library/Application Support/{IDENTIFIER}"\n'
                f'echo leak > "{self.real}/Library/Application Support/{IDENTIFIER}/state"\n'
                f'echo more >> "{caches}/existing"\n')
        app, record_path = self.bundle(leak)
        code, record, err, _ = self.run_helper(app, record_path)
        self.assertEqual(code, 1, err)
        self.assertEqual(record['outcome'], 'failed')
        self.assertEqual(record['real_library']['result'], 'changed')
        self.assertEqual(record['real_library']['entries_before'], 2)
        changes = {(c['path'], c['change']) for c in record['real_library']['changes']}
        self.assertIn((f'Application Support/{IDENTIFIER}', 'created'), changes)
        self.assertIn((f'Application Support/{IDENTIFIER}/state', 'created'), changes)
        self.assertIn((f'Caches/{IDENTIFIER}/existing', 'modified'), changes)
        self.assertTrue(any(f'created Library/Application Support/{IDENTIFIER}' in f for f in record['failures']))

    def test_a_changed_system_preference_is_disclosed_and_is_not_a_failure(self):
        prefs = self.real / 'Library/Preferences'
        script = (f'echo invented > "{prefs}/com.apple.spaces.plist"\n'
                  f'echo invented-change >> "{prefs}/com.apple.dock.plist"\n')
        app, record_path = self.bundle(script)
        code, record, err, _ = self.run_helper(app, record_path)
        self.assertEqual(code, 0, err)
        self.assertEqual(record['outcome'], 'clean')
        self.assertEqual({(c['name'], c['change']) for c in record['system_preferences_changed']},
                         {('com.apple.spaces.plist', 'created'), ('com.apple.dock.plist', 'modified')})
        self.assertEqual((prefs / 'com.apple.dock.plist').read_bytes(), b'invented system preference' + b'invented-change\n')

    def test_a_preference_file_named_for_the_build_is_a_failure_not_a_disclosure(self):
        prefs = self.real / 'Library/Preferences'
        app, record_path = self.bundle(f'echo invented > "{prefs}/{IDENTIFIER}.plist"\n')
        code, record, err, _ = self.run_helper(app, record_path)
        self.assertEqual(code, 1, err)
        self.assertEqual(record['real_library']['changes'], [{'path': f'Preferences/{IDENTIFIER}.plist', 'change': 'created'}])
        self.assertEqual(record['system_preferences_changed'], [])

    def test_reuse_accepts_only_a_home_this_helper_marked(self):
        app, record_path = self.bundle()
        code, first, err, _ = self.run_helper(app, record_path)
        self.assertEqual(code, 0, err)
        home = Path(first['home']['path'])
        code, second, err, _ = self.run_helper(app, record_path, home=home)
        self.assertEqual(code, 0, err)
        self.assertEqual(second['home']['path'], str(home))
        self.assertEqual(second['home']['state'], 'reused')
        self.assertFalse(second['home']['empty_at_start'])
        unmarked = self.parent / 'unmarked'; (unmarked / 'tmp').mkdir(parents=True)
        copied = self.parent / 'copied-marker'; (copied / 'tmp').mkdir(parents=True)
        shutil.copy(home / launch.MARKER, copied / launch.MARKER)
        for name, path in (('unmarked', unmarked), ('marker copied from another home', copied),
                           ('the real home', self.real)):
            with self.subTest(name):
                code, record, err, run_dir = self.run_helper(app, record_path, home=path)
                self.assertEqual(code, 2)
                self.assertIsNone(record)
                self.assertFalse(run_dir.exists())

    def test_removal_refuses_unmarked_paths_the_real_home_and_checkouts_and_removes_a_marked_home(self):
        app, record_path = self.bundle()
        code, record, err, _ = self.run_helper(app, record_path)
        self.assertEqual(code, 0, err)
        home = Path(record['home']['path'])
        unmarked = self.parent / 'unmarked'; unmarked.mkdir()
        (self.real / launch.MARKER).write_text(json.dumps({'made_by': launch.TOOL, 'path': str(self.real)}))
        checkout = self.tmp / 'checkout'; (checkout / '.git').mkdir(parents=True)
        inside = checkout / 'home'; inside.mkdir()
        (inside / launch.MARKER).write_text(json.dumps({'made_by': launch.TOOL, 'path': str(inside)}))
        for name, path in (('unmarked', unmarked), ('real home, even marked', self.real),
                           ('folder containing the real home', self.tmp), ('inside a checkout', inside),
                           ('this repository', launch.REPOSITORY)):
            with self.subTest(name):
                with self.assertRaises(ValueError):
                    launch.remove(path)
                self.assertTrue(path.exists())
        (home / launch.ACTIVE).write_text(json.dumps({'helper_pid': os.getpid()}))
        with self.assertRaisesRegex(ValueError, 'still using'):
            launch.remove(home)
        (home / launch.ACTIVE).unlink()
        self.assertEqual(launch.remove(home), {'removed': str(home)})
        self.assertFalse(home.exists())

    def test_runs_that_fail_never_read_as_clean(self):
        with self.subTest('the App exits with a failure status'):
            app, record_path = self.bundle(where='failing', exit_status=3)
            code, record, _, _ = self.run_helper(app, record_path)
            self.assertEqual((code, record['outcome'], record['ended']), (1, 'failed', 'exited with status 3'))
        with self.subTest('the App does not start'):
            app, record_path = self.bundle(where='unstartable', shebang='#!/nonexistent/interpreter')
            code, record, _, _ = self.run_helper(app, record_path)
            self.assertEqual((code, record['outcome']), (1, 'failed'))
            self.assertTrue(record['ended'].startswith('did not start'))
            self.assertFalse(record['real_library']['compared'])
        with self.subTest('the after-listing cannot be taken'):
            app, record_path = self.bundle(where='unreadable')
            real_listing = launch.library_listing
            calls = []

            def listing(*args):
                calls.append(1)
                if len(calls) > 1:
                    raise PermissionError('invented: after-listing refused')
                return real_listing(*args)
            with mock.patch.object(launch, 'library_listing', listing):
                code, record, _, _ = self.run_helper(app, record_path)
            self.assertEqual((code, record['outcome']), (1, 'failed'))
            self.assertFalse(record['real_library']['compared'])
            self.assertTrue(record['real_library']['result'].startswith('not compared'))
        with self.subTest('the before-listing cannot be taken: nothing is launched'):
            app, record_path = self.bundle(where='unlisted')
            with mock.patch.object(launch, 'library_listing', side_effect=PermissionError('invented')):
                code, record, _, _ = self.run_helper(app, record_path)
            self.assertEqual((code, record['outcome'], record['started_at']), (2, 'not launched', None))
            self.assertFalse((Path(record['home']['path']) / 'received-env.txt').exists())

    def test_a_process_left_running_in_the_apps_group_is_not_a_clean_run(self):
        app, record_path = self.bundle('sleep 5 &\n', where='lingering')
        code, record, _, _ = self.run_helper(app, record_path)
        with contextlib.suppress(ProcessLookupError):
            os.killpg(record['pid'], signal.SIGKILL)
        self.assertEqual((code, record['outcome'], record['process_group_after_settle']), (1, 'failed', 'still running'))

    def test_stop_from_the_shell_ends_the_app_and_the_helper_still_compares(self):
        app, record_path = self.bundle('exec sleep 30\n', where='stopped')
        run_dir = self.tmp / f'run-{self.runs + 1}'
        stopped = []

        def stop_when_running():
            deadline = time.monotonic() + 10
            while time.monotonic() < deadline and not (run_dir / launch.PIDFILE).exists():
                time.sleep(0.05)
            time.sleep(0.2)
            stopped.append(launch.stop(run_dir))
        thread = threading.Thread(target=stop_when_running)
        thread.start()
        code, record, _, _ = self.run_helper(app, record_path)
        thread.join()
        self.assertEqual(stopped[0]['signalled'], record['pid'])
        self.assertEqual(record['ended'], 'ended by signal 15 (SIGTERM)')
        self.assertTrue(record['real_library']['compared'])
        self.assertEqual((code, record['outcome']), (1, 'failed'))  # a stop is not the App's own Quit
        with self.assertRaisesRegex(ValueError, 'already ended'):
            launch.stop(run_dir)

    def test_run_folder_and_home_parent_inside_a_checkout_refuse(self):
        app, record_path = self.bundle()
        for argv in (['--run-dir', str(launch.REPOSITORY / 'launch-run'), '--home-parent', str(self.parent)],
                     ['--run-dir', str(self.tmp / 'r'), '--home-parent', str(launch.REPOSITORY)]):
            with self.subTest(argv):
                with contextlib.redirect_stderr(io.StringIO()):
                    code = launch.main(['launch', '--app', str(app), '--record', str(record_path),
                                        '--settle-seconds', '0', *argv])
                self.assertEqual(code, 2)
                self.assertFalse((launch.REPOSITORY / 'launch-run').exists())


class RealHomeDefault(unittest.TestCase):
    def test_the_real_home_is_the_account_home_not_the_home_variable(self):
        with mock.patch.dict(os.environ, {'HOME': '/invented/elsewhere'}):
            self.assertEqual(launch.real_home(), Path(os.path.realpath(pwd.getpwuid(os.getuid()).pw_dir)))


if __name__ == '__main__':
    unittest.main()
