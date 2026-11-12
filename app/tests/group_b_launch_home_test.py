"""The examination launcher for first launches on new homes, with invented material only.

A shell script plays the App, and folders stand in for the real home and the
per-user cache folder. Every fixture, including stand-in launch folders, lives
in a temporary folder under the account's home, outside any checkout, and is
removed by the test that made it. No App, window, socket or real home Library
is touched; nothing here launches a real build.
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
CLEAN_RECORD_FIELDS = {'note', 'helper', 'candidate_key', 'identifier', 'bundle', 'candidate_folder', 'launch_folder',
                       'home', 'address_override', 'environment_constructed_for_the_app', 'output', 'started_at', 'pid',
                       'ended_at', 'process_group_after_settle', 'disclosed', 'app_started', 'ended', 'real_library',
                       'signals_received', 'failures', 'outcome'}

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
    """Stands in for identify_candidate (identification has its own tests): returns the invented record."""
    return json.loads(Path(record_path).read_text())


def fd_path(fd):
    if MAC:
        import fcntl
        return os.fsdecode(fcntl.fcntl(fd, fcntl.F_GETPATH, bytes(1024)).split(b'\0', 1)[0])
    return os.readlink(f'/proc/self/fd/{fd}')


def identities(root):
    """(device, inode) of every folder under root, root included."""
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
        for name, value in (('real_home', self.real), ('user_cache_dir', self.cache), ('SETTLE_SECONDS', 0.0)):
            patch = mock.patch.object(launch, name, return_value=value) if callable(getattr(launch, name)) \
                else mock.patch.object(launch, name, value)
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

    def candidate(self, script='', where='build', exit_status=0, shebang='#!/bin/sh', executable=EXECUTABLE,
                  plays=True, name=PRODUCT + '.app'):
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
                  'bundle': {'identifier': IDENTIFIER, 'name': name,
                             'executable': {'path': 'Contents/MacOS/' + executable,
                                            'sha256': hashlib.sha256(exe.read_bytes()).hexdigest()}}}
        (root / 'identification').mkdir()
        (root / 'identification/candidate-identification.json').write_text(json.dumps(record))
        (root / 'identification' / launch.INVENTORY).write_text('{}')
        return root

    def argv(self, candidate, *extra, run_dir=None, parent=None):
        return ['launch', '--candidate', str(candidate), '--run-dir', str(run_dir), '--parent', str(parent or self.parent),
                *extra]

    def run_helper(self, candidate, *extra, run_dir=None, parent=None):
        self.runs += 1
        run_dir = Path(run_dir or self.tmp / f'run-{self.runs}')
        code, out = self.call(*self.argv(candidate, *extra, run_dir=run_dir, parent=parent))
        saved = run_dir / launch.RECORD
        record = json.loads(saved.read_text()) if saved.exists() and not saved.is_symlink() else None
        if record and record.get('pid'):
            self.groups.append(record['pid'])
        return code, record, out, run_dir

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
        for option in ('--app-env', '--owner-sitting', '--reuse', '--lang', '--settle-seconds'):
            with self.subTest(option), contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                launch.main(self.argv(candidate, option, 'CHIRALITY_WORKSPACE=/x', run_dir=self.tmp / 'r'))
        for extra in ((), ('--model-address', 'http://127.0.0.1:8080/v1')):
            with self.subTest(extra=extra):
                code, record, out, _ = self.run_helper(candidate, *extra)
                env = self.received(record)
                self.assertEqual(set(env) - SHELL_OWN, set(launch.ALLOWED))
                for name, (value, _) in launch.PROXY_OVERRIDES.items():
                    self.assertEqual(env[name], value)
                self.assertIn(launch.MODEL_ADDRESS, env)

    def test_the_exact_mapping_is_checked_immediately_before_the_start(self):
        home, tmp = self.parent / 'h', '.chirality-launch-tmp-x'
        good = launch.child_environment(home, tmp, launch.DEFAULT_MODEL_ADDRESS)
        launch.check_environment(good, home, tmp)
        cases = {'an added name': {**good, 'SSH_AUTH_SOCK': '/x'},
                 'HOME alone': {k: v for k, v in good.items() if k != 'CFFIXED_USER_HOME'},
                 'homes differ': {**good, 'CFFIXED_USER_HOME': str(self.parent / 'other')},
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
        self.assertEqual((code, record['outcome'], record['app_started']), (2, 'not launched', False))
        self.assertFalse((Path(record['home']) / 'received-env.txt').exists())


class CleanRun(Fixture):  # STATEMENTS 2 and 3
    def test_a_clean_run_records_exactly_the_tabled_fields(self):
        code, record, out, run_dir = self.run_helper(self.candidate())
        self.assertEqual((code, record['outcome']), (0, 'clean'), out)
        self.assertEqual(set(record), CLEAN_RECORD_FIELDS)
        self.assertEqual(set(record['disclosed']), {'preferences', 'user_cache'})
        self.assertEqual((record['real_library']['result'], record['signals_received'], record['app_started']),
                         ('unchanged', [], True))
        self.assertEqual(os.listdir(run_dir), [launch.RECORD])

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

    def test_an_interrupted_record_write_leaves_no_record_under_its_name(self):
        with mock.patch.object(launch.os, 'link', side_effect=OSError(28, 'No space left on device')):
            code, record, out, run_dir = self.run_helper(self.candidate())
        self.assertIsNone(record)
        self.assertEqual(code, 2)
        self.assertFalse((run_dir / launch.RECORD).exists())
        self.assertTrue(all(n.startswith('.' + launch.RECORD + '.partial-') for n in os.listdir(run_dir)))

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
                        while time.monotonic() < deadline and not list(self.parent.glob('launch-*/home/received-env.txt')):
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
for patch in patches:
    patch.start()
sys.exit(launch.main(sys.argv[6:]))
'''


class KilledHelper(Fixture):  # STATEMENT 2: a killed helper leaves no record
    def test_a_helper_killed_at_each_stage_leaves_no_record(self):
        runner = self.tmp / 'runner.py'
        runner.write_text(KILLED_RUNNER)
        for stage in ('before start', 'running', 'finalizing'):
            with self.subTest(stage):
                slug = stage.replace(' ', '-')
                sentinel = self.tmp / f'sentinel-{slug}'
                script = f'echo $$ > "{sentinel}"\nsleep 60\n' if stage == 'running' else ''
                candidate = self.candidate(script, where=f'killed-{slug}', plays=False)
                run_dir = self.tmp / f'killed-run-{slug}'
                helper = subprocess.Popen([sys.executable, '-B', str(runner), str(HELPER), stage, str(self.real),
                                           str(self.cache), str(sentinel), *self.argv(candidate, run_dir=run_dir)],
                                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                deadline = time.monotonic() + 20
                while not (sentinel.exists() and sentinel.read_text().strip()) and time.monotonic() < deadline:
                    time.sleep(0.05)
                self.assertTrue(sentinel.exists())
                helper.kill()
                helper.wait()
                if stage == 'running':
                    self.groups.append(int(sentinel.read_text().strip()))
                self.assertFalse((run_dir / launch.RECORD).exists())
                for name in (os.listdir(run_dir) if run_dir.exists() else []):
                    self.assertTrue(name.startswith('.' + launch.RECORD + '.partial-'), name)


@contextlib.contextmanager
def reads_under(paths, dirs=()):
    """Instrumentation, lexical and resolved: every listing, read or stat of one of `paths` or of anything under one
    of `dirs` (exclusive write-only creation is not counted)."""
    paths = {os.path.realpath(p) for p in paths}
    dirs = [os.path.realpath(d) for d in dirs]
    touched = []

    def hit(text):
        return text is not None and (text in paths or any(text.startswith(d + os.sep) for d in dirs))

    def resolve(path, dir_fd):
        if isinstance(path, int):
            return fd_path(path)
        text = os.fsdecode(path)
        if dir_fd is not None and not os.path.isabs(text):
            return os.path.normpath(os.path.join(fd_path(dir_fd), text))
        return os.path.abspath(text)

    real = {name: getattr(os, name) for name in ('listdir', 'scandir', 'stat', 'lstat', 'open')}

    def wrap(name):
        def spied(*args, **kwargs):
            lexical = resolve(args[0] if args else kwargs.get('path', '.'), kwargs.get('dir_fd'))
            flags = (args[1] if len(args) > 1 else kwargs.get('flags', 0)) if name == 'open' else 0
            creating = name == 'open' and flags & os.O_ACCMODE == os.O_WRONLY and flags & os.O_CREAT and flags & os.O_EXCL
            result = real[name](*args, **kwargs)
            resolved = fd_path(result) if name == 'open' else None
            if not creating and (hit(lexical) or hit(resolved)):
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


class NewHomeOnly(Fixture):  # the home is new: an exclusive create, never a reuse
    def test_the_new_home_is_never_read(self):
        candidate = self.candidate()
        with reads_under((), dirs=[self.parent]) as touched:
            code, record, out, _ = self.run_helper(candidate)
        self.assertEqual(code, 0, out)
        self.assertEqual([t for t in touched if (t[1] or '').startswith(record['home'] + os.sep)
                          or (t[2] or '').startswith(record['home'] + os.sep)], [])

    def test_reviewer_round5_a_launch_folder_named_in_another_case_in_parent_gets_a_new_home_inside_it(self):
        existing = self.tmp / 'existing'
        old_home = existing / launch.new_folder_name().upper() / launch.HOME
        (old_home / 'kept').mkdir(parents=True)
        (old_home / 'kept/auth.json').write_text(SECRET)
        before = identities(self.tmp)
        old_entries = [str(p) for p in old_home.rglob('*')]
        with reads_under(old_entries) as touched:
            code, record, out, _ = self.run_helper(self.candidate(), parent=old_home)
        self.assertEqual(code, 0, out)
        launched_into = os.stat(record['home'])
        self.assertNotIn((launched_into.st_dev, launched_into.st_ino), before)  # the App's home did not exist before
        self.assertTrue(record['home'].startswith(str(old_home) + '/launch-'))
        self.assertEqual(touched, [])  # the existing home's own entries were neither listed nor read
        self.assertEqual((old_home / 'kept/auth.json').read_text(), SECRET)
        self.assertNotIn(SECRET, out)

    def test_a_home_path_that_already_exists_is_refused_by_the_create_itself(self):
        name = launch.new_folder_name()
        case_insensitive = (self.tmp / 'CaseProbe').write_text('') or (self.tmp / 'caseprobe').exists()
        spellings = [name] + ([name.upper()] if case_insensitive else [])
        for index, spelling in enumerate(spellings):
            with self.subTest(spelling):
                parent = self.tmp / f'p-{index}'
                (parent / spelling / launch.HOME).mkdir(parents=True)
                before = identities(parent)
                with mock.patch.object(launch, 'new_folder_name', return_value=name):
                    code, record, out, run_dir = self.run_helper(self.candidate(where=f'c-{index}'), parent=parent)
                self.assert_refused(code, out, 'could not be created: something already exists there')
                self.assertIsNone(record)
                self.assertEqual(identities(parent), before)


class ListedPathChecks(Fixture):  # a listed, not exhaustive, set of refusals
    def test_a_path_whose_written_ancestry_names_a_launch_folder_is_refused_untouched(self):
        code, record, out, _ = self.run_helper(self.candidate())
        folder = Path(record['launch_folder'])
        home = folder / launch.HOME
        (home / 'sessions').mkdir()
        inner = self.candidate(where=f'{folder.relative_to(self.tmp)}/home/cand')
        cases = {'candidate folder under a launch folder': self.argv(inner, run_dir=self.tmp / 'r1'),
                 'run folder under a launch folder': self.argv(self.candidate(where='c2'), run_dir=home / 'sessions/run'),
                 'parent under a launch folder': self.argv(self.candidate(where='c3'), run_dir=self.tmp / 'r3', parent=home)}
        for name, argv in cases.items():
            with self.subTest(name):
                with reads_under([str(home)], dirs=[str(home)]) as touched:
                    code, out = self.call(*argv)
                self.assert_refused(code, out, 'names a launch folder')
                self.assertEqual(touched, [])
        self.assertFalse((home / 'sessions/run').exists())

    def test_ambiguous_syntax_is_refused_before_normalisation(self):
        candidate = self.candidate()
        (self.tmp / 'other/deep').mkdir(parents=True)
        (self.tmp / 'linked').symlink_to(self.tmp / 'other/deep')
        for name, text in (('".." through a link', f'{self.tmp}/linked/../parent'), ('"."', f'{self.tmp}/./parent'),
                           ('empty component', f'{self.tmp}//parent'), ('trailing slash', f'{self.parent}/'),
                           ('relative', 'parent')):
            with self.subTest(name):
                code, out = self.call(*self.argv(candidate, run_dir=self.tmp / 'r', parent=text))
                self.assert_refused(code, out, 'written ambiguously' if text.startswith('/') else 'absolute')
                self.assertFalse((self.tmp / 'r').exists())
        self.assertEqual(os.listdir(self.tmp / 'other/deep'), [])

    def test_links_in_an_access_path_and_protected_places_are_refused(self):
        candidate = self.candidate()
        outside = self.tmp / 'outside-identification'
        shutil.copytree(candidate / 'identification', outside)
        shutil.rmtree(candidate / 'identification')
        (candidate / 'identification').symlink_to(outside)
        self.assert_refused(*self.call(*self.argv(candidate, run_dir=self.tmp / 'r')), 'identification folder')
        plain = self.candidate(where='plain')
        (self.tmp / 'aliased').symlink_to(plain)
        self.assert_refused(*self.call(*self.argv(self.tmp / 'aliased', run_dir=self.tmp / 'r')), 'no link')
        checkout = self.tmp / 'checkout'
        (checkout / '.git').mkdir(parents=True)
        self.assert_refused(*self.call(*self.argv(plain, run_dir=checkout / 'run')), 'checkout')
        self.assert_refused(*self.call(*self.argv(plain, run_dir=launch.REPOSITORY / 'launch-run')), 'checkout')
        self.assert_refused(*self.call(*self.argv(plain, run_dir=self.real / 'Library/run')), 'real home Library')
        self.assert_refused(*self.call(*self.argv(self.candidate(where='x/Applications/c'), run_dir=self.tmp / 'r')),
                            'Applications folder')
        code, record, out, run_dir = self.run_helper(plain)
        self.assert_refused(*self.call(*self.argv(plain, run_dir=run_dir)), 'already exists')
        self.assertFalse((launch.REPOSITORY / 'launch-run').exists())


class WatchedByExactName(Fixture):
    def test_an_executable_name_that_does_not_discriminate_is_refused(self):
        for index, name in enumerate(('a', 'app', 'chirality', 'Chirality-x')):
            with self.subTest(name):
                code, record, out, run_dir = self.run_helper(self.candidate(executable=name, where=f'short{index}'))
                self.assert_refused(code, out, 'does not discriminate')
                self.assertFalse(run_dir.exists())

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
                code, _, out, run_dir = self.run_helper(candidate, '--model-address', value)
                self.assert_refused(code, out, launch.MODEL_ADDRESS)
                self.assertFalse(run_dir.exists())
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
                code, _, out, _ = self.run_helper(candidate)
                self.assert_refused(code, out, 'differs from its identification record')
                self.assertNotIn(SECRET, out)
        for error in (plistlib.InvalidFileException(), ExpatError('invented')):
            with self.subTest(type(error).__name__), mock.patch.object(identify, 'validate_record'), \
                    mock.patch.object(identify, 'check', side_effect=error):
                self.assertEqual(self.run_helper(candidate)[0], 2)

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


class Housekeeping(unittest.TestCase):
    def test_the_real_home_is_the_account_home_not_the_home_variable(self):
        with mock.patch.dict(os.environ, {'HOME': '/invented/elsewhere'}):
            self.assertEqual(launch.real_home(), Path(os.path.realpath(pwd.getpwuid(os.getuid()).pw_dir)))

    def test_the_removed_commands_and_machinery_are_gone(self):
        for command in ('stop', 'remove'):
            with self.subTest(command), contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                launch.main([command])
        for name in ('stop', 'remove', 'own_folder', 'claim', 'lock', 'in_use', 'read_own', 'APP_INPUTS', 'KINDS'):
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
