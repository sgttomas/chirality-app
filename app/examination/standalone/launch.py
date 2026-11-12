#!/usr/bin/env python3
"""Launch one identified development App build in a throwaway home (DEL-09-02 examination tooling).

What it does:
- Refuses a bundle that identification's shared rule
  (identify.judge_development_bundle) refuses, so it never launches the release
  identity (com.chirality.app, the name Chirality, the file name Chirality.app);
  refuses a bundle whose identifier, file name or executable differs from its
  candidate identification record; refuses a bundle under an Applications
  folder.
- Makes a new throwaway home (or reuses one it made earlier, recognised by the
  marker it wrote) and sets BOTH HOME and CFFIXED_USER_HOME to it. HOME alone
  does not keep a launch out of the real home's Library: the system frameworks,
  including the web view's data and caches, follow CFFIXED_USER_HOME.
- Gives the App an allowlisted environment, written out in the run record: the
  two home variables, LANG, a minimal PATH, TMPDIR inside the throwaway home,
  and only the App startup inputs the caller names. Nothing else is inherited.
- Starts the bundle's executable as a child process (an ordinary application
  with its normal window), waits for it to exit, and records how it ended. The
  App's process identifier is written to the run folder so the caller can end a
  run from the shell (`stop`, or the App's own Quit); the helper keeps waiting
  and still compares afterwards.
- Immediately before launch and after the App has exited, lists by name, size
  and modification time only (never contents) the real home's Library entries
  named for the build's identifier or executable name, and compares the two
  listings: any creation, removal or change there is a failure. Files directly
  under the real Library/Preferences that changed during the run are disclosed
  as changed by the operating system's own services (or anything else running
  at the time); they are never opened, edited or removed, and are not a failure.
- Writes one small run record, after the comparison and never before it. It is
  evidence for a journey step's record, not an examination record format, and
  nothing validates it. The outcome is "clean" only when the App started,
  exited with status 0, left no process in its process group after the settle
  time, and both after-listings were taken and equal the before-listing. A
  `stop` ends the App by SIGTERM, not by its own Quit, so a stopped run is not
  clean. Exit status: 0 clean, 1 a run was made but is not clean, 2 refused or
  not launched. No record means no completed run.
- `remove` deletes a throwaway home it made, after the caller has taken what it
  needs. The launch command removes nothing.

Limits, in plain terms:
- It redirects what the system frameworks place under the home. It does not
  redirect the operating system's own records about an application that opens
  a window (for example files under the real Library/Preferences belonging to
  system services); those are disclosed, not prevented.
- It does not confine the App: no operating-system write restriction is
  applied, and a process that ignores HOME and CFFIXED_USER_HOME, or writes
  after the after-listing, is not covered. The comparison watches only the
  listed Library places named for the build; it is not a census of the disk.
- A throwaway home has no login keychain and no signed-in session. A step that
  must use the real login keychain or the owner's signed-in session cannot run
  through this helper; its launch is made otherwise, and that step's record
  must say which home was used.
- It does not point identify.py at the throwaway home and does not change
  identify.py's freshness check, which reads the real home and stays as it is:
  identification refuses a build that an earlier unredirected launch left data
  for in the real home; this helper vouches for the throwaway home's clean start.
- It sends no input to the App and does not look at its window.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import plistlib
import pwd
import secrets
import shutil
import signal
import stat
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
REPOSITORY = HERE.parents[2]
sys.path.insert(0, str(HERE.parent / 'candidate_identity'))
import identify  # noqa: E402  (the shared development-identity rule)

TOOL = 'app/examination/standalone/launch.py'
NOTE = ('Evidence for a journey step record, written by ' + TOOL + '; not an examination record format, '
        'and nothing validates it.')
MARKER = '.chirality-launch-home.json'
ACTIVE = '.chirality-launch-active.json'
RECORD = 'launch-record.json'
PIDFILE = 'app-process.json'
OUTPUT = 'app-output.log'
SYSTEM_PATH = '/usr/bin:/bin:/usr/sbin:/sbin'
DEFAULT_LANG = 'en_US.UTF-8'
# The App's startup inputs: the keys of explicit_environment_launch in
# app/src-tauri/src/lib.rs and records_store.rs OVERRIDE_ENV. None is passed
# unless the caller names it, so by default the App takes its first-use setup route.
APP_INPUTS = ('CHIRALITY_CODEX_BIN', 'CHIRALITY_CODEX_HOME', 'CHIRALITY_WORKSPACE', 'CHIRALITY_KEY_HOME',
              'CHIRALITY_SHARED_CONFIG', 'CHIRALITY_SHARED_AGENTS', 'CHIRALITY_SHARED_SKILLS',
              'CHIRALITY_CODEX_EXPECTED_SHA256', 'CHIRALITY_ALLOW_UNVERIFIED', 'CHIRALITY_DISTRIBUTION_SUCCESSOR',
              'CHIRALITY_RECORDS_STORE')
# Library subfolders whose entries are searched for names of the build. The
# Library's own first level is searched too. Protected folders (Containers,
# Group Containers, Mail, Messages, Safari and the like) are not listed: reading
# them can be refused or raise a system privacy prompt, and a non-sandboxed
# development build does not write there through the home.
WATCHED = ('Application Support', 'Caches', 'WebKit', 'HTTPStorages', 'Preferences', 'Saved Application State',
           'Logs', 'Cookies', 'Application Scripts', 'Autosave Information', 'LaunchAgents')


def real_home():
    """The real home: the one place it is taken from (tests point it elsewhere). Not read from HOME."""
    return Path(os.path.realpath(pwd.getpwuid(os.getuid()).pw_dir))


def now():
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


def _within(path, root):
    path, root = Path(path), Path(root)
    return path == root or root in path.parents


def _in_checkout(path):
    return any(os.path.lexists(p / '.git') for p in (path, *path.parents))


def check_place(path, what):
    """A location the helper writes or removes: outside every checkout, the real Library and the real home itself."""
    given = Path(os.path.abspath(path))
    real = Path(os.path.realpath(given))
    home = real_home()
    if _within(home, real) or _within(home, given):
        raise ValueError(f'{what} is or contains the real home: {given}')
    if _within(real, home / 'Library'):
        raise ValueError(f'{what} is inside the real home Library: {given}')
    if _within(real, REPOSITORY) or _in_checkout(real):
        raise ValueError(f'{what} is inside a repository checkout: {given}')
    return real


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, 'rb') as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def read_bundle(app, record_path):
    """Judge the bundle's observed identity and bind it to its identification record; refuse anything else."""
    given = Path(os.path.abspath(app))
    real = Path(os.path.realpath(given))
    home = real_home()
    for place in (given, real):
        parts = place.parts
        if any(_within(place, a) for a in (Path('/Applications'), Path('/System/Applications'), home / 'Applications')) \
                or (len(parts) > 3 and parts[1] == 'Users' and parts[3] == 'Applications'):
            raise ValueError('a bundle under an Applications folder is not launched: ' + str(place))
    if given.suffix != '.app' or given.is_symlink() or not given.is_dir():
        raise ValueError('the bundle must be a .app directory, not a link: ' + str(given))
    plist = plistlib.loads((real / 'Contents/Info.plist').read_bytes())
    if not isinstance(plist, dict):
        raise ValueError('Info.plist is not a dictionary')
    identifier, executable = plist.get('CFBundleIdentifier'), plist.get('CFBundleExecutable')
    names = (plist.get('CFBundleName'), plist.get('CFBundleDisplayName'))
    identify.judge_development_bundle(identifier, given.name, names)
    identify.judge_development_bundle(identifier, real.name, names)
    record = json.loads(Path(record_path).read_bytes())
    bundle = record['bundle']
    identify.judge_development_bundle(bundle['identifier'], bundle['name'])
    if identifier != bundle['identifier']:
        raise ValueError(f'bundle identifier {identifier!r} differs from the record {bundle["identifier"]!r}')
    if real.name != bundle['name']:
        raise ValueError(f'bundle file name {real.name!r} differs from the record {bundle["name"]!r}')
    if not isinstance(executable, str) or not executable or '/' in executable or executable in ('.', '..'):
        raise ValueError('bundle executable name invalid')
    if 'Contents/MacOS/' + executable != bundle['executable']['path']:
        raise ValueError('bundle executable differs from the record: ' + executable)
    path = real / 'Contents/MacOS' / executable
    info = os.lstat(path)
    if not stat.S_ISREG(info.st_mode) or not info.st_mode & 0o100:
        raise ValueError('bundle executable is not an executable regular file: ' + str(path))
    if sha256_file(path) != bundle['executable']['sha256']:
        raise ValueError('bundle executable bytes differ from the identification record')
    return {'path': str(real), 'identifier': identifier, 'executable': executable, 'executable_path': str(path),
            'candidate_key': record['candidate_key']}


def app_inputs(pairs):
    """Explicit App startup inputs from NAME=VALUE pairs; only the App's own startup variable names."""
    given = {}
    for pair in pairs or ():
        name, sep, value = pair.partition('=')
        if not sep or name not in APP_INPUTS:
            raise ValueError(f'not an App startup input (allowed: {", ".join(APP_INPUTS)}): {name!r}')
        if name in given:
            raise ValueError('App startup input given twice: ' + name)
        given[name] = value
    return given


def plan_environment(home, inputs, lang=DEFAULT_LANG):
    env = {'HOME': str(home), 'CFFIXED_USER_HOME': str(home), 'LANG': lang, 'PATH': SYSTEM_PATH,
           'TMPDIR': str(Path(home) / 'tmp'), **inputs}
    check_home_variables(env)
    return env


def check_home_variables(env):
    """Both home variables, equal, naming one throwaway home; and nothing outside the allowlist."""
    homes = env.get('HOME'), env.get('CFFIXED_USER_HOME')
    if None in homes or '' in homes:
        raise ValueError('HOME and CFFIXED_USER_HOME must both be set; refusing to launch with only one')
    if homes[0] != homes[1]:
        raise ValueError('HOME and CFFIXED_USER_HOME differ; refusing to launch')
    extra = set(env) - {'HOME', 'CFFIXED_USER_HOME', 'LANG', 'PATH', 'TMPDIR', *APP_INPUTS}
    if extra:
        raise ValueError('environment outside the allowlist: ' + ', '.join(sorted(extra)))
    if not _within(Path(env.get('TMPDIR', '/')), Path(homes[0])):
        raise ValueError('TMPDIR is not inside the throwaway home')
    return homes[0]


def _exclusive_json(path, value):
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, 'w') as stream:
        stream.write(json.dumps(value, indent=2) + '\n')


def make_home(parent):
    parent = Path(os.path.abspath(parent))
    if parent.is_symlink() or not parent.is_dir():
        raise ValueError('the home parent must be an existing directory, not a link: ' + str(parent))
    home = Path(os.path.realpath(parent)) / f'launch-home-{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}-{secrets.token_hex(4)}'
    check_place(home, 'throwaway home')
    os.mkdir(home, 0o700)
    if os.listdir(home):
        raise ValueError('new throwaway home is not empty: ' + str(home))
    _exclusive_json(home / MARKER, {'made_by': TOOL, 'path': str(home), 'made_at': now()})
    os.mkdir(home / 'tmp', 0o700)
    return home, {'path': str(home), 'state': 'created', 'empty_when_created': True}


def read_marker(home):
    marker = Path(home) / MARKER
    try:
        info = os.lstat(marker)
        value = json.loads(marker.read_bytes()) if stat.S_ISREG(info.st_mode) else None
    except (OSError, ValueError):
        value = None
    if not isinstance(value, dict) or value.get('made_by') != TOOL or value.get('path') != str(home):
        raise ValueError('not a throwaway home made by this helper (no matching marker): ' + str(home))
    return value


def reuse_home(path):
    if Path(os.path.abspath(path)).is_symlink():
        raise ValueError('the reused home must not be a link: ' + str(path))
    home = check_place(path, 'reused home')
    read_marker(home)
    tmp = home / 'tmp'
    if not tmp.is_dir() or tmp.is_symlink():
        raise ValueError('the reused home has no temporary folder of its own: ' + str(tmp))
    entries = sorted(n for n in os.listdir(home) if n not in (MARKER, 'tmp'))
    return home, {'path': str(home), 'state': 'reused', 'empty_at_start': not entries, 'entries_at_start': len(entries)}


def _alive(pid):
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def claim_home(home):
    active = home / ACTIVE
    if os.path.lexists(active):
        try:
            holder = json.loads(active.read_bytes()).get('helper_pid')
        except (OSError, ValueError, AttributeError):
            holder = None
        if isinstance(holder, int) and _alive(holder):
            raise ValueError(f'a launch is already using this home (helper process {holder})')
        os.unlink(active)
    _exclusive_json(active, {'helper_pid': os.getpid(), 'since': now()})
    return active


def _describe(info):
    kind = 'dir' if stat.S_ISDIR(info.st_mode) else 'file' if stat.S_ISREG(info.st_mode) \
        else 'symlink' if stat.S_ISLNK(info.st_mode) else 'other'
    entry = {'kind': kind, 'mtime_ns': info.st_mtime_ns}
    if kind != 'dir':
        entry['size'] = info.st_size
    return entry


def _raise(error):
    raise error


def library_listing(identifier, executable):
    """Names, kinds, sizes and modification times of real-Library entries named for the build; contents are never read."""
    library = real_home() / 'Library'
    watched = sorted({identifier.lower(), executable.lower()})
    entries = {}
    if not os.path.lexists(library):
        return entries
    if not library.is_dir() or library.is_symlink():
        raise ValueError('the real home Library is not a directory')

    def add(relative):
        path = library / relative
        info = os.lstat(path)
        entries[relative] = _describe(info)
        if stat.S_ISDIR(info.st_mode):
            for current, dirs, files in os.walk(path, onerror=_raise):
                for name in dirs + files:
                    child = Path(current) / name
                    entries[str(child.relative_to(library))] = _describe(os.lstat(child))

    for folder in ('', *WATCHED):
        where = library / folder if folder else library
        if folder and (where.is_symlink() or not where.is_dir()):
            continue
        for name in sorted(os.listdir(where)):
            if any(w in name.lower() for w in watched):
                add(f'{folder}/{name}' if folder else name)
    return dict(sorted(entries.items()))


def preferences_listing():
    """Names, sizes and times of files directly under the real Library/Preferences."""
    folder = real_home() / 'Library/Preferences'
    if folder.is_symlink() or not folder.is_dir():
        return {}
    out = {}
    with os.scandir(folder) as listing:
        for entry in listing:
            info = entry.stat(follow_symlinks=False)
            if not stat.S_ISDIR(info.st_mode):
                out[entry.name] = _describe(info)
    return out


def differences(before, after):
    return [{'path': p, 'change': 'created' if p not in before else 'removed' if p not in after else 'modified'}
            for p in sorted(before.keys() | after.keys()) if before.get(p) != after.get(p)]


def process_start(pid):
    """The process's start time as ps reports it, or None; used to tell the launched App from a reused identifier."""
    result = subprocess.run(['ps', '-o', 'lstart=', '-p', str(pid)], capture_output=True, text=True)
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def process_group_state(pgid):
    try:
        os.killpg(pgid, 0)
    except ProcessLookupError:
        return 'gone'
    except PermissionError:
        return 'still running'
    return 'still running'


def how_it_ended(returncode):
    if returncode < 0:
        try:
            return f'ended by signal {-returncode} ({signal.Signals(-returncode).name})'
        except ValueError:
            return f'ended by signal {-returncode}'
    return f'exited with status {returncode}'


def make_run_dir(path):
    run = check_place(path, 'run folder')
    os.mkdir(run, 0o700)
    return run


def launch(args):
    bundle = read_bundle(args.app, args.record)
    inputs = app_inputs(args.app_env)
    if args.settle_seconds < 0:
        raise ValueError('settle time cannot be negative')
    check_place(args.run_dir, 'run folder')
    if args.reuse_home:
        check_place(args.reuse_home, 'reused home')
        read_marker(Path(os.path.realpath(args.reuse_home)))
    run = make_run_dir(args.run_dir)
    record = {'note': NOTE, 'helper': {'path': TOOL, 'sha256': sha256_file(__file__)},
              'candidate_key': bundle['candidate_key'], 'identifier': bundle['identifier'],
              'bundle': bundle['path'], 'record': str(Path(os.path.abspath(args.record)))}
    failures = []
    home, record['home'] = reuse_home(args.reuse_home) if args.reuse_home else make_home(args.home_parent)
    env = plan_environment(home, inputs, args.lang)
    record['environment'] = env
    active = claim_home(home)
    proc = None
    try:
        try:
            before = library_listing(bundle['identifier'], bundle['executable'])
            prefs_before = preferences_listing()
        except (OSError, ValueError) as error:
            record.update(started_at=None, ended_at=None, ended=f'not launched: the before-listing failed: {error}',
                          real_library={'compared': False, 'result': 'not compared: no before-listing'},
                          system_preferences_changed=[], outcome='not launched')
            failures.append('the before-listing could not be taken; nothing was launched')
            return _finish(run, record, failures, 2)
        record['real_library'] = {'watched_names': sorted({bundle['identifier'], bundle['executable']}),
                                  'watched_places': ['Library', *('Library/' + w for w in WATCHED)],
                                  'entries_before': len(before)}
        record['started_at'] = now()
        output = os.open(run / OUTPUT, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
        try:
            proc = subprocess.Popen([bundle['executable_path']], env=env, cwd=home, stdin=subprocess.DEVNULL,
                                    stdout=output, stderr=output, start_new_session=True, close_fds=True)
        except OSError as error:
            record.update(ended_at=now(), ended=f'did not start: {error}', outcome='failed',
                          system_preferences_changed=[])
            record['real_library'].update(compared=False, result='not compared: the App did not start')
            failures.append('the App did not start')
            return _finish(run, record, failures, 1)
        finally:
            os.close(output)
        record['pid'] = proc.pid
        _exclusive_json(run / PIDFILE, {'pid': proc.pid, 'process_start': process_start(proc.pid),
                                        'executable': bundle['executable_path'], 'helper_pid': os.getpid()})
        print(json.dumps({'launched': proc.pid, 'run_folder': str(run), 'home': str(home)}), file=sys.stderr, flush=True)
        stop_requests = []

        def forward(signum, frame):
            stop_requests.append(f'{signal.Signals(signum).name} to the helper at {now()}; SIGTERM forwarded to the App')
            try:
                proc.send_signal(signal.SIGTERM)
            except ProcessLookupError:
                pass
        previous = {s: signal.signal(s, forward) for s in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP)}
        try:
            returncode = proc.wait()
        finally:
            for s, handler in previous.items():
                signal.signal(s, handler)
        record.update(ended_at=now(), ended=how_it_ended(returncode))
        if stop_requests:
            record['stop_requests'] = stop_requests
        if returncode != 0:
            failures.append('the App ' + record['ended'])
        time.sleep(args.settle_seconds)
        record['process_group_after_settle'] = process_group_state(proc.pid)
        if record['process_group_after_settle'] != 'gone':
            failures.append("processes in the App's process group were still running after the settle time")
        try:
            after = library_listing(bundle['identifier'], bundle['executable'])
            prefs_after = preferences_listing()
            time.sleep(args.settle_seconds)
            again = library_listing(bundle['identifier'], bundle['executable'])
        except (OSError, ValueError) as error:
            record['real_library'].update(compared=False, result=f'not compared: the after-listing failed: {error}')
            record['system_preferences_changed'] = []
            failures.append('the after-listing could not be taken, so no comparison was made')
            return _finish(run, record, failures, 1)
        changes = differences(before, after)
        record['real_library'].update(compared=True, result='changed' if changes else 'unchanged', changes=changes)
        if changes:
            failures.append('the real Library changed in places named for the build: ' +
                            '; '.join(f"{c['change']} Library/{c['path']}" for c in changes))
        if again != after:
            record['real_library']['still_changing'] = differences(after, again)
            failures.append('the real Library places named for the build were still changing after the App exited')
        named = {p.split('/', 1)[1] for p in before.keys() | after.keys() if p.startswith('Preferences/')}
        record['system_preferences_changed'] = [
            {'name': c['path'], 'change': c['change'],
             'disclosed_as': "changed during the run by the operating system's own services or anything else running; "
                             'not opened, edited or removed'}
            for c in differences(prefs_before, prefs_after) if c['path'] not in named]
        return _finish(run, record, failures, 1 if failures else 0)
    finally:
        if proc is not None and proc.poll() is None:  # the helper is leaving early: say so, never leave silently
            print(json.dumps({'warning': f'the App (process {proc.pid}) is still running; no record says it ended'}),
                  file=sys.stderr)
        try:
            os.unlink(active)
        except FileNotFoundError:
            pass


def _finish(run, record, failures, code):
    record['failures'] = failures
    record.setdefault('outcome', 'clean' if not failures else 'failed')
    _exclusive_json(run / RECORD, record)
    print(json.dumps({'outcome': record['outcome'], 'record': str(run / RECORD), 'failures': failures}, indent=2))
    return code


def stop(run_dir):
    """End a running App from the shell: SIGTERM to the recorded process, after checking it is still that process."""
    run = Path(os.path.abspath(run_dir))
    if os.path.lexists(run / RECORD):
        raise ValueError('this run has already ended (its record exists)')
    process = json.loads((run / PIDFILE).read_bytes())
    pid, started = process['pid'], process.get('process_start')
    if not started or process_start(pid) != started:
        raise ValueError(f'process {pid} is no longer the launched App (or its start time was not recorded)')
    os.kill(pid, signal.SIGTERM)
    return {'signalled': pid, 'signal': 'SIGTERM'}


def remove(path):
    """Remove a throwaway home this helper made; refuse anything else."""
    given = Path(os.path.abspath(path))
    if given.is_symlink():
        raise ValueError('refusing a link: ' + str(given))
    home = check_place(given, 'path to remove')
    read_marker(home)
    active = home / ACTIVE
    if os.path.lexists(active):
        try:
            holder = json.loads(active.read_bytes()).get('helper_pid')
        except (OSError, ValueError, AttributeError):
            holder = None
        if isinstance(holder, int) and _alive(holder):
            raise ValueError(f'a launch is still using this home (helper process {holder})')
    shutil.rmtree(home)
    return {'removed': str(home)}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0],
                                     epilog='Exit status: 0 clean run, 1 run made but not clean (see the record), 2 refused.')
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('launch', help='launch the bundle in a throwaway home and compare the real Library before and after')
    p.add_argument('--app', required=True, help='the built development bundle (.app)')
    p.add_argument('--record', required=True, help='its candidate identification record (identify.py record)')
    p.add_argument('--run-dir', required=True, help='new folder for the run record, created here; outside any checkout')
    where = p.add_mutually_exclusive_group(required=True)
    where.add_argument('--home-parent', help='existing folder in which a new, empty throwaway home is made')
    where.add_argument('--reuse-home', help='a throwaway home an earlier launch of this helper made (same walk)')
    p.add_argument('--app-env', action='append', metavar='NAME=VALUE',
                   help='an App startup input, passed explicitly (repeatable); none by default: ' + ', '.join(APP_INPUTS))
    p.add_argument('--lang', default=DEFAULT_LANG, help='LANG for the App (default %(default)s)')
    p.add_argument('--settle-seconds', type=float, default=5.0,
                   help='wait after the App exits before listing, and again before the second after-listing (default 5)')
    p = sub.add_parser('stop', help="end a running App (SIGTERM, not the App's own Quit); the launch command keeps waiting")
    p.add_argument('--run-dir', required=True)
    p = sub.add_parser('remove', help='remove a throwaway home this helper made, after its contents are taken')
    p.add_argument('--home', required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == 'launch':
            return launch(args)
        print(json.dumps(stop(args.run_dir) if args.command == 'stop' else remove(args.home)))
        return 0
    except (ValueError, KeyError, TypeError, OSError, plistlib.InvalidFileException) as error:
        print(json.dumps({'error': f'{type(error).__name__}: {error}'}), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
