#!/usr/bin/env python3
"""Launch one identified development App build in a throwaway home (DEL-09-02 examination tooling).

Why it exists: a build launched from an agent's shell hands that shell's
environment, which carries tokens, to the App and to the supplier it starts.
An inherited environment with names removed is not enough; here the App's
environment is built from nothing. The helper guarantees six invariants, each
held in one place in this file (search for "INVARIANT"):

1. The App's environment is a new mapping built from a written allowlist,
   never derived from this process's environment, and checked against the
   allowlist immediately before the App starts. The run record lists it.
2. A run is clean only when the App exited by itself with status 0, nobody
   asked it to stop, no process of its process group was left, and the
   watched places were listed whole twice after it exited and nothing differed
   from the listing before. A link met at or beneath a watched place makes the
   comparison incomplete; an incomplete comparison is never unchanged or clean.
3. What is watched is named exactly: entries whose name contains the bundle
   identifier (ending there or before a dot or other separator), equals the
   executable name, or is a system web view helper folder for that executable.
   An executable name that does not discriminate is refused.
4. Locations are judged by device and inode, not spelling: the run folder and
   the home are not inside the real home's Library, are not and do not contain
   the real home, and are not inside a checkout; a bundle under any folder
   named Applications, in any letter case, is refused.
5. A throwaway home is the helper's by identity (its marker records the
   home's device and inode); it is accepted or removed only while that holds,
   and never while a launch or a member of the App's process group lives. On
   reuse the helper reads only its own marker and state there. Nothing of the
   home leaves it: the App's output stays inside the home. A new throwaway
   home has no login keychain and no signed-in session; a kept one may hold the
   owner's signed-in state for the build after the owner's own sitting, which
   is why the reuse launch is meant to be the only thing that opens it.
6. Only the candidate the identification record identifies is launched: the
   record is validated and identification's own check (identify.check) must
   find the bundle equal to it. The check hashes the whole bundle twice, a few
   seconds for a real build.

Disclosed in the record, never a failure, never opened, edited or removed:
files directly under the real Library/Preferences that changed during the run,
and changes in the system's per-user cache folder (getconf
DARWIN_USER_CACHE_DIR, which does not follow HOME) among entries named by the
rule of invariant 3. These are the operating system's own records about an
application that opens a window; the helper does not redirect them.

It does not confine the App: no operating-system write restriction is applied,
and the comparison covers only the places listed in WATCHED. It sends no input
to the App and does not look at its window. A step that must use the real
login keychain or the owner's own home is outside it. Identification's
freshness check still reads the real home and is not pointed at the throwaway
home; this helper vouches for a new throwaway home's clean start.
"""
import sys

sys.dont_write_bytecode = True  # running the helper writes nothing beside the sources it imports

import argparse  # noqa: E402
from datetime import datetime, timezone  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import os  # noqa: E402
from pathlib import Path  # noqa: E402
import plistlib  # noqa: E402
import pwd  # noqa: E402
import re  # noqa: E402
import secrets  # noqa: E402
import shutil  # noqa: E402
import signal  # noqa: E402
import stat  # noqa: E402
import subprocess  # noqa: E402
import tarfile  # noqa: E402
import time  # noqa: E402
from xml.parsers.expat import ExpatError  # noqa: E402

HERE = Path(__file__).resolve().parent
REPOSITORY = HERE.parents[2]
sys.path.insert(0, str(HERE.parent / 'candidate_identity'))
import identify  # noqa: E402  (identification's record validation, check and shared identity rule)

TOOL = 'app/examination/standalone/launch.py'
NOTE = ('Evidence for a journey step record, written by ' + TOOL + '; not an examination record format, '
        'and nothing validates it.')
OWN = '.chirality-launch'  # the helper's own folder inside a throwaway home
MARKER, STATE = 'marker.json', 'state.json'
RECORD, PROCESS, STOPS = 'launch-record.json', 'app-process.json', 'stop-requests'
SYSTEM_PATH = '/usr/bin:/bin:/usr/sbin:/sbin'
DEFAULT_LANG = 'en_US.UTF-8'
LOCALE = re.compile(r'C|POSIX|[A-Za-z]{2,3}(?:_[A-Za-z]{2})?(?:\.[A-Za-z0-9-]+)?')

# INVARIANT 1: every name the App's environment can hold, with why it is there.
ALLOWED = {
    'HOME': 'the throwaway home, the home of the App and every process it starts',
    'CFFIXED_USER_HOME': "the same throwaway home for the system frameworks (web view data and caches), which HOME alone does not move",
    'TMPDIR': "temporary files, inside the helper's own folder in the throwaway home",
    'PATH': 'the fixed system path, so system tools are found and nothing of the caller is',
    'LANG': "the App's locale: the fixed default or the caller's explicit --lang, never inherited",
}
# The App's own startup inputs (keys of explicit_environment_launch in
# app/src-tauri/src/lib.rs, and records_store.rs OVERRIDE_ENV). Given only when
# the caller names one; any one selects the App's explicit environment route.
APP_INPUTS = {
    'CHIRALITY_CODEX_BIN': 'the supplier binary the App starts',
    'CHIRALITY_CODEX_HOME': 'the App-owned account home for the supplier',
    'CHIRALITY_WORKSPACE': "the App's project workspace",
    'CHIRALITY_KEY_HOME': 'the API-key home',
    'CHIRALITY_SHARED_CONFIG': 'the shared config.toml reference',
    'CHIRALITY_SHARED_AGENTS': 'the shared AGENTS.md reference',
    'CHIRALITY_SHARED_SKILLS': 'the shared skills reference',
    'CHIRALITY_CODEX_EXPECTED_SHA256': "the supplier binary's expected digest",
    'CHIRALITY_ALLOW_UNVERIFIED': 'the development allowance for an unverified supplier',
    'CHIRALITY_DISTRIBUTION_SUCCESSOR': 'the development successor-distribution switch',
    'CHIRALITY_RECORDS_STORE': "the records store override",
}

# INVARIANT 3: the Library folders searched, beside the Library's own first
# level. Protected folders (Containers, Group Containers, Mail, Safari and the
# like) are not listed: reading them can be refused or raise a privacy prompt,
# and a development build does not write there through the home.
WATCHED = ('Application Support', 'Caches', 'WebKit', 'HTTPStorages', 'Preferences', 'Saved Application State',
           'Logs', 'Cookies', 'Application Scripts', 'Autosave Information', 'LaunchAgents')
EXECUTABLE_RULE = re.compile(r'chirality-[a-z0-9][a-z0-9_-]{2,}')  # e.g. chirality-app-v4


def real_home():
    """The real home, from the account database, never from HOME; the one place tests point elsewhere."""
    return Path(os.path.realpath(pwd.getpwuid(os.getuid()).pw_dir))


def user_cache_dir():
    """The system's per-user cache folder (getconf DARWIN_USER_CACHE_DIR), or None where there is none."""
    try:
        result = subprocess.run(['/usr/bin/getconf', 'DARWIN_USER_CACHE_DIR'], capture_output=True, text=True,
                                env={'PATH': SYSTEM_PATH})
    except OSError:
        return None
    value = result.stdout.strip()
    return Path(os.path.realpath(value)) if result.returncode == 0 and value else None


def now():
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, 'rb') as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


# ---- INVARIANT 4: locations by identity -------------------------------------------------------

def _identity(path):
    info = os.stat(path)
    return info.st_dev, info.st_ino


def ancestry(path):
    """(device, inode) and name of the deepest existing ancestor of path and of every directory above it."""
    path = Path(os.path.abspath(path))
    while not os.path.lexists(path):
        path = path.parent
    real = Path(os.path.realpath(path))
    return [(_identity(p), p.name) for p in (real, *real.parents)]


def inside(path, place):
    """INVARIANT 4: path is place or lies inside it, judged by device and inode, never by spelling."""
    try:
        target = _identity(place)
    except FileNotFoundError:
        return False
    return target in {ident for ident, _ in ancestry(path)}


def check_place(path, what):
    """INVARIANT 4: a place the helper writes, reuses or removes."""
    path = Path(os.path.abspath(path))
    home = real_home()
    if inside(path, home / 'Library'):
        raise ValueError(f'{what} is inside the real home Library: {path}')
    if os.path.lexists(path) and inside(home, path):
        raise ValueError(f'{what} is or contains the real home: {path}')
    real = Path(os.path.realpath(path))
    if inside(path, REPOSITORY) or any(os.path.lexists(p / '.git') for p in (real, *real.parents)):
        raise ValueError(f'{what} is inside a repository checkout: {path}')
    return path


def under_applications(path):
    """INVARIANT 4: any ancestor named Applications, in any letter case, wherever it is."""
    names = [name for _, name in ancestry(path)] + list(Path(os.path.abspath(path)).parts)
    return any(name.lower() == 'applications' for name in names)


# ---- INVARIANT 6: only the identified candidate -----------------------------------------------

def identify_candidate(app, record_path):
    """INVARIANT 6: the record is valid and identification's own check finds the bundle equal to it."""
    record = json.loads(Path(record_path).read_bytes())
    if not isinstance(record, dict) or not record.get('candidate_key'):
        raise ValueError('the identification record has no candidate key')
    identify.validate_record(record)
    result = identify.check(argparse.Namespace(record=str(record_path), app=str(app)))
    if not (result['equal'] and result['build_identity'] == result['recorded_build_identity']
            and not result.get('record_fields_mismatched')):
        differing = (result.get('changed', []) + result.get('missing', []) + result.get('extra', [])
                     + result.get('record_fields_mismatched', []))
        raise ValueError('the bundle differs from its identification record: ' + (', '.join(differing[:10]) or
                                                                                  'build identity differs'))
    return record


# ---- INVARIANT 3: what is watched -------------------------------------------------------------

def check_executable(executable):
    """INVARIANT 3: an executable name that does not discriminate is refused before launch."""
    if not isinstance(executable, str) or not EXECUTABLE_RULE.fullmatch(executable.lower()):
        raise ValueError(f'executable name {executable!r} does not discriminate (it must match '
                         f'{EXECUTABLE_RULE.pattern}, as chirality-app-v4 does)')


def watched_name(name, identifier, executable):
    """INVARIANT 3, the one rule: contains the identifier, equals the executable name, or is its web view helper folder."""
    name, identifier, executable = name.lower(), identifier.lower(), executable.lower()
    at = name.find(identifier)
    while at >= 0:
        end = at + len(identifier)
        if end == len(name) or not (name[end].isalnum() or name[end] == '-'):
            return True
        at = name.find(identifier, at + 1)
    if name == executable:
        return True
    helper = r'com\.apple\.webkit\.(?:networking|webcontent|gpu)\+' + re.escape(executable.replace('-', '_')) + r'-.+'
    return re.fullmatch(helper, name) is not None


def _describe(info):
    kind = 'dir' if stat.S_ISDIR(info.st_mode) else 'file' if stat.S_ISREG(info.st_mode) \
        else 'link' if stat.S_ISLNK(info.st_mode) else 'other'
    entry = {'kind': kind, 'mtime_ns': info.st_mtime_ns}
    if kind != 'dir':
        entry['size'] = info.st_size
    return entry


def _raise(error):
    raise error


def listing(base, folders, identifier, executable):
    """Names, kinds, sizes and times of the watched entries under base, walked; contents never read; links never followed.

    Returns (entries, links): every link met at a watched folder, at a watched entry or beneath one.
    """
    entries, links = {}, []
    if os.path.islink(base):
        return entries, ['.']
    if not os.path.isdir(base):
        return entries, links
    for folder in folders:
        where = Path(base) / folder if folder else Path(base)
        if os.path.islink(where):
            links.append(folder)
            continue
        if not os.path.isdir(where):
            continue
        for name in sorted(os.listdir(where)):
            if not watched_name(name, identifier, executable):
                continue
            relative = f'{folder}/{name}' if folder else name
            info = os.lstat(where / name)
            entries[relative] = _describe(info)
            if stat.S_ISLNK(info.st_mode):
                links.append(relative)
            elif stat.S_ISDIR(info.st_mode):
                for current, dirs, files in os.walk(where / name, onerror=_raise):
                    for child_name in dirs + files:
                        child = Path(current) / child_name
                        child_info = os.lstat(child)
                        child_relative = str(child.relative_to(base))
                        entries[child_relative] = _describe(child_info)
                        if stat.S_ISLNK(child_info.st_mode):
                            links.append(child_relative)
    return dict(sorted(entries.items())), sorted(links)


def preferences_listing():
    """Files directly under the real Library/Preferences: names, sizes and times (disclosure only)."""
    folder = real_home() / 'Library/Preferences'
    if folder.is_symlink() or not folder.is_dir():
        return {}
    with os.scandir(folder) as found:
        return {e.name: _describe(e.stat(follow_symlinks=False)) for e in found if not e.is_dir(follow_symlinks=False)}


def differences(before, after):
    return [{'path': p, 'change': 'created' if p not in before else 'removed' if p not in after else 'modified'}
            for p in sorted(before.keys() | after.keys()) if before.get(p) != after.get(p)]


def compare(before, after, again):
    """INVARIANT 2: unchanged only when all three listings were taken whole, met no link and agree."""
    if before is None or after is None or again is None:
        return {'result': 'not made'}
    links = sorted(set(before[1]) | set(after[1]) | set(again[1]))
    changes, still = differences(before[0], after[0]), differences(after[0], again[0])
    result = 'incomplete' if links else 'changed' if changes or still else 'unchanged'
    out = {'result': result, 'entries_before': len(before[0]), 'changes': changes}
    if still:
        out['still_changing'] = still
    if links:
        out['links_met'] = links
    return out


def outcome(facts):
    """INVARIANT 2, the one place a run is judged."""
    failures = []
    if not facts.get('started'):
        failures.append('the App was not started: ' + facts.get('ended', 'refused before launch'))
    else:
        if facts.get('returncode') != 0:
            failures.append('the App ' + facts['ended'])
        if facts.get('stop_requests'):
            failures.append('a stop was requested (' + str(len(facts['stop_requests'])) + '); the App did not end by itself')
        if facts.get('process_group') != 'gone':
            failures.append("a process of the App's process group was still running after the settle time")
    result = facts.get('comparison', {}).get('result', 'not made')
    if result != 'unchanged':
        failures.append({'not made': 'no complete comparison was made',
                         'incomplete': 'the comparison is incomplete: a link was met at or beneath a watched place',
                         'changed': 'the real Library changed in places named for the build'}[result])
    return ('clean' if not failures else 'failed'), failures


# ---- INVARIANT 5: the throwaway home ---------------------------------------------------------

def _write_new(path, value):
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, 'w') as stream:
        stream.write(json.dumps(value, indent=2) + '\n')


def _own_dir(home, *parts):
    path = Path(home, OWN, *parts)
    info = os.lstat(path)
    if not stat.S_ISDIR(info.st_mode):
        raise ValueError("the helper's own folder in the home is not a plain directory: " + str(path))
    return path


def plan_home(parent):
    """A new home path under the caller's parent, its place checked before anything is made."""
    parent = Path(os.path.abspath(parent))
    if parent.is_symlink() or not parent.is_dir():
        raise ValueError('the home parent must be an existing directory, not a link: ' + str(parent))
    home = Path(os.path.realpath(parent)) / f'launch-home-{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}-{secrets.token_hex(4)}'
    return check_place(home, 'throwaway home')


def make_home(home):
    check_place(home, 'throwaway home')
    os.mkdir(home, 0o700)
    if os.listdir(home):
        raise ValueError('new throwaway home is not empty: ' + str(home))
    for part in (OWN, OWN + '/tmp', OWN + '/output'):
        os.mkdir(home / part, 0o700)
    info = os.lstat(home)
    _write_new(home / OWN / MARKER, {'made_by': TOOL, 'path': str(home), 'device': info.st_dev,
                                     'inode': info.st_ino, 'made_at': now()})
    return home


def own_home(path):
    """INVARIANT 5a: a home this helper made, by identity; only its own marker is read."""
    given = Path(os.path.abspath(path))
    if given.is_symlink():
        raise ValueError('refusing a link: ' + str(given))
    home = check_place(Path(os.path.realpath(given)), 'throwaway home')
    info = os.lstat(home)
    try:
        marker = json.loads((_own_dir(home) / MARKER).read_bytes()) \
            if stat.S_ISREG(os.lstat(home / OWN / MARKER).st_mode) else None
    except (OSError, ValueError):
        marker = None
    if not stat.S_ISDIR(info.st_mode) or not isinstance(marker, dict) or marker.get('made_by') != TOOL \
            or marker.get('path') != str(home) or (marker.get('device'), marker.get('inode')) != (info.st_dev, info.st_ino):
        raise ValueError('not a throwaway home made by this helper (marker absent, or its recorded identity differs): '
                         + str(home))
    return home


def _alive(pid):
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def group_state(pgid):
    try:
        os.killpg(pgid, 0)
    except ProcessLookupError:
        return 'gone'
    except PermissionError:
        return 'still running'
    return 'still running'


def read_state(home):
    try:
        state = json.loads((_own_dir(home) / STATE).read_bytes())
    except FileNotFoundError:
        return {}
    return state if isinstance(state, dict) else {}


def write_state(home, state):
    own = _own_dir(home)
    temporary = own / f'{STATE}.{os.getpid()}'
    _write_new(temporary, state)
    os.replace(temporary, own / STATE)


def in_use(home):
    """INVARIANT 5b: the home is in use while its launch lives or any member of the App's process group does."""
    state = read_state(home)
    reasons = []
    helper, group = state.get('helper_pid'), state.get('process_group')
    if isinstance(helper, int) and _alive(helper):
        reasons.append(f'a launch (helper process {helper})')
    if isinstance(group, int) and group_state(group) != 'gone':
        reasons.append(f"a member of the App's process group {group}")
    return reasons


def claim(home):
    reasons = in_use(home)
    if reasons:
        raise ValueError('the throwaway home is in use by ' + ' and '.join(reasons))
    write_state(home, {'helper_pid': os.getpid(), 'process_group': None, 'since': now()})


def release(home, group):
    """Custody outlives the launcher: a living group stays recorded and keeps the home in use."""
    alive = group is not None and group_state(group) != 'gone'
    write_state(home, {'helper_pid': None, 'process_group': group if alive else None, 'since': now()})


# ---- INVARIANT 1: the environment ------------------------------------------------------------

def app_inputs(pairs):
    given = {}
    for pair in pairs or ():
        name, sep, value = pair.partition('=')
        if not sep or name not in APP_INPUTS or '\0' in value:
            raise ValueError(f'not an App startup input (allowed: {", ".join(APP_INPUTS)}): {name!r}')
        if name in given:
            raise ValueError('App startup input given twice: ' + name)
        given[name] = value
    return given


def child_environment(home, inputs, lang):
    """INVARIANT 1: a new mapping from the allowlist alone; nothing is read from this process's environment."""
    env = {'HOME': str(home), 'CFFIXED_USER_HOME': str(home), 'TMPDIR': str(Path(home, OWN, 'tmp')),
           'PATH': SYSTEM_PATH, 'LANG': lang}
    env.update(inputs)
    return env


def check_environment(env, home):
    """INVARIANT 1, immediately before the App starts: the allowlist, and the homes and TMPDIR in the throwaway home."""
    if not isinstance(env, dict) or not all(isinstance(k, str) and isinstance(v, str) for k, v in env.items()):
        raise ValueError('the App environment is not a mapping of names to text')
    extra = set(env) - set(ALLOWED) - set(APP_INPUTS)
    missing = set(ALLOWED) - set(env)
    if extra or missing:
        raise ValueError(f'App environment outside the allowlist: extra {sorted(extra)}, missing {sorted(missing)}')
    for name in ('HOME', 'CFFIXED_USER_HOME'):
        if not os.path.isdir(env[name]) or _identity(env[name]) != _identity(home):
            raise ValueError(f'{name} is not the throwaway home; refusing to launch')
    if not os.path.isdir(env['TMPDIR']) or not inside(env['TMPDIR'], home):
        raise ValueError('TMPDIR is not inside the throwaway home; refusing to launch')
    if env['PATH'] != SYSTEM_PATH or not LOCALE.fullmatch(env['LANG']):
        raise ValueError('PATH or LANG differs from the allowlist')
    return env


# ---- the run ---------------------------------------------------------------------------------

def process_start(pid):
    """The process's start time as ps reports it, or None; tells the launched App from a reused identifier."""
    result = subprocess.run(['ps', '-o', 'lstart=', '-p', str(pid)], capture_output=True, text=True)
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def how_it_ended(returncode):
    if returncode < 0:
        try:
            return f'ended by signal {-returncode} ({signal.Signals(-returncode).name})'
        except ValueError:
            return f'ended by signal {-returncode}'
    return f'exited with status {returncode}'


def request_stop(run, by):
    """INVARIANT 2b: a stop request is written to the run folder before any signal, independent of the exit status."""
    _write_new(Path(run, STOPS, f'{datetime.now(timezone.utc):%Y%m%dT%H%M%S%fZ}-{secrets.token_hex(3)}.json'),
               {'by': by, 'at': now()})


def stop_requests(run):
    folder = Path(run, STOPS)
    return [json.loads((folder / n).read_bytes()) for n in sorted(os.listdir(folder))]


def launch(args):
    app = Path(os.path.abspath(args.app))
    if under_applications(app):
        raise ValueError('a bundle under an Applications folder is not launched: ' + str(app))
    inputs = app_inputs(args.app_env)
    if not LOCALE.fullmatch(args.lang) or args.settle_seconds < 0:
        raise ValueError('invalid --lang or --settle-seconds')
    record_data = identify_candidate(app, args.record)
    identifier = record_data['bundle']['identifier']
    executable_path = record_data['bundle']['executable']['path']
    executable = executable_path.rsplit('/', 1)[-1]
    check_executable(executable)
    run = check_place(args.run_dir, 'run folder')
    if args.reuse_home:
        home = own_home(args.reuse_home)
        if in_use(home):
            raise ValueError('the throwaway home is in use by ' + ' and '.join(in_use(home)))
        home_note = {'path': str(home), 'state': 'reused'}
    else:
        home = plan_home(args.home_parent)
    os.mkdir(run, 0o700)
    os.mkdir(run / STOPS, 0o700)
    if not args.reuse_home:
        make_home(home)
        home_note = {'path': str(home), 'state': 'created', 'empty_when_created': True}
    claim(home)
    for part in ('tmp', 'output'):  # the helper's own folders only; the rest of the home is not looked into
        if not os.path.lexists(home / OWN / part):
            os.mkdir(home / OWN / part, 0o700)
    env = child_environment(home, inputs, args.lang)
    record = {'note': NOTE, 'helper': {'path': TOOL, 'sha256': sha256_file(__file__)},
              'candidate_key': record_data['candidate_key'], 'identifier': identifier, 'bundle': str(app),
              'identification_record': str(Path(os.path.abspath(args.record))), 'home': home_note,
              'environment': env, 'watched': {
                  'rule': 'name contains the identifier, equals the executable name, or is '
                          'com.apple.WebKit.<Networking|WebContent|GPU>+<executable with _ for ->-<suffix>',
                  'identifier': identifier, 'executable': executable,
                  'places': ['Library', *('Library/' + w for w in WATCHED)]}}
    facts = {'started': False}
    proc = None
    cache = user_cache_dir()
    try:
        try:
            before = listing(real_home() / 'Library', ('', *WATCHED), identifier, executable)
            prefs_before = preferences_listing()
            cache_before = listing(cache, ('',), identifier, executable) if cache else None
            check_environment(env, home)
        except (OSError, ValueError) as error:
            facts['ended'] = f'not launched: {error}'
            record.update(started_at=None, ended=facts['ended'])
            return _finish(run, record, facts, code=2, label='not launched')
        output_path = _own_dir(home, 'output') / f'{run.name}-{secrets.token_hex(3)}.log'
        output = os.open(output_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
        record['started_at'] = now()
        try:
            proc = subprocess.Popen([str(app / executable_path)], env=env, cwd=home, stdin=subprocess.DEVNULL,
                                    stdout=output, stderr=output, start_new_session=True, close_fds=True)
        except OSError as error:
            facts['ended'] = f'did not start: {error}'
            record.update(ended_at=now(), ended=facts['ended'])
            return _finish(run, record, facts, code=1)
        finally:
            os.close(output)
        facts['started'] = True
        record['pid'] = proc.pid

        def forward(signum, frame):
            request_stop(run, f'{signal.Signals(signum).name} to the helper, forwarded to the App as SIGTERM')
            try:
                proc.send_signal(signal.SIGTERM)
            except ProcessLookupError:
                pass
        previous = {s: signal.signal(s, forward) for s in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP)}
        try:
            write_state(home, {'helper_pid': os.getpid(), 'process_group': proc.pid, 'since': now()})
            _write_new(run / PROCESS, {'pid': proc.pid, 'process_start': process_start(proc.pid),
                                       'helper_pid': os.getpid()})
            print(json.dumps({'launched': proc.pid, 'run_folder': str(run), 'home': str(home)}), file=sys.stderr,
                  flush=True)
            facts['returncode'] = proc.wait()
        finally:
            for s, handler in previous.items():
                signal.signal(s, handler)
        facts['ended'] = how_it_ended(facts['returncode'])
        record.update(ended_at=now(), ended=facts['ended'])
        time.sleep(args.settle_seconds)
        facts['process_group'] = record['process_group_after_settle'] = group_state(proc.pid)
        after = again = None
        try:
            after = listing(real_home() / 'Library', ('', *WATCHED), identifier, executable)
            prefs_after = preferences_listing()
            cache_after = listing(cache, ('',), identifier, executable) if cache else None
            time.sleep(args.settle_seconds)
            again = listing(real_home() / 'Library', ('', *WATCHED), identifier, executable)
        except (OSError, ValueError) as error:
            record['after_listing_error'] = str(error)
            prefs_after, cache_after = prefs_before, cache_before
        facts['comparison'] = record['real_library'] = compare(before, after, again)
        facts['stop_requests'] = record['stop_requests'] = stop_requests(run)
        named = {p.split('/', 1)[1] for p in before[0].keys() | (after or ({}, []))[0].keys() if p.startswith('Preferences/')}
        disclosed = "changed during the run by the operating system's own services or anything else running; not opened, edited or removed"
        record['disclosed'] = {
            'note': disclosed,
            'preferences': [c for c in differences(prefs_before, prefs_after) if c['path'] not in named],
            'user_cache': ({'folder': str(cache), 'changes': differences(cache_before[0], cache_after[0]),
                            'links_met': sorted(set(cache_before[1]) | set(cache_after[1]))}
                           if cache else 'no per-user cache folder on this system')}
        size = os.lstat(output_path).st_size
        record['output'] = {'path': str(output_path), 'size': size, 'note': 'kept inside the throwaway home'}
        return _finish(run, record, facts, code=None)
    finally:
        if proc is not None and proc.poll() is None:
            print(json.dumps({'warning': f'the App (process {proc.pid}) is still running; no record says it ended'}),
                  file=sys.stderr)
        release(home, proc.pid if proc is not None else None)


def _finish(run, record, facts, code, label=None):
    result, failures = outcome(facts)
    record['real_library'] = facts.get('comparison', record.get('real_library', {'result': 'not made'}))
    record['failures'] = failures
    record['outcome'] = label or result
    _write_new(Path(run, RECORD), record)  # written once, after the comparison
    print(json.dumps({'outcome': record['outcome'], 'record': str(Path(run, RECORD)), 'failures': failures}, indent=2))
    return code if code is not None else (0 if result == 'clean' else 1)


def stop(run_dir):
    """End a running App from the shell: record the request, then SIGTERM to the recorded process."""
    run = Path(os.path.abspath(run_dir))
    if os.path.lexists(run / RECORD):
        raise ValueError('this run has already ended (its record exists)')
    process = json.loads((run / PROCESS).read_bytes())
    pid, started = process['pid'], process.get('process_start')
    if not started or process_start(pid) != started:
        raise ValueError(f'process {pid} is no longer the launched App (or its start time was not recorded)')
    request_stop(run, 'stop command')
    os.kill(pid, signal.SIGTERM)
    return {'signalled': pid, 'signal': 'SIGTERM'}


def remove(path):
    """INVARIANT 5: remove a throwaway home this helper made, by identity, when nothing of a launch lives."""
    home = own_home(path)
    reasons = in_use(home)
    if reasons:
        raise ValueError('the throwaway home is in use by ' + ' and '.join(reasons))
    shutil.rmtree(home)
    return {'removed': str(home)}


def main(argv=None):
    parser = argparse.ArgumentParser(
        description=__doc__.splitlines()[0],
        epilog='Exit status: 0 clean run, 1 run made but not clean (see the record), 2 refused or not launched. '
               'The invariants and limits are in the module docstring.')
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('launch', help='launch the identified bundle in a throwaway home and compare the real Library')
    p.add_argument('--app', required=True, help='the built development bundle (.app)')
    p.add_argument('--record', required=True, help="its candidate identification record; identification's check must pass")
    p.add_argument('--run-dir', required=True, help='new folder for the run record; outside any checkout and the real Library')
    where = p.add_mutually_exclusive_group(required=True)
    where.add_argument('--home-parent', help='existing folder in which a new, empty throwaway home is made')
    where.add_argument('--reuse-home', help='a throwaway home this helper made, for a later launch of the same walk')
    p.add_argument('--app-env', action='append', metavar='NAME=VALUE',
                   help='an App startup input, given explicitly (repeatable; none by default): ' + ', '.join(APP_INPUTS))
    p.add_argument('--lang', default=DEFAULT_LANG, help='LANG for the App (default %(default)s; never inherited)')
    p.add_argument('--settle-seconds', type=float, default=5.0,
                   help='wait after the App exits before listing, and again before the second listing (default 5)')
    p = sub.add_parser('stop', help="end a running App (SIGTERM, not the App's own Quit; the run is then not clean)")
    p.add_argument('--run-dir', required=True)
    p = sub.add_parser('remove', help='remove a throwaway home this helper made, when no launch or App process lives')
    p.add_argument('--home', required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == 'launch':
            return launch(args)
        print(json.dumps(stop(args.run_dir) if args.command == 'stop' else remove(args.home)))
        return 0
    except (ValueError, KeyError, TypeError, AttributeError, OSError, ImportError, json.JSONDecodeError,
            plistlib.InvalidFileException, ExpatError, subprocess.CalledProcessError, tarfile.TarError,
            EOFError) as error:
        print(json.dumps({'error': f'{type(error).__name__}: {error}'}), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
