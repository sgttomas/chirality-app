#!/usr/bin/env python3
"""Launch one identified development App build in a throwaway home (DEL-09-02 examination tooling).

Why it exists: a build launched from an agent's shell would inherit that
shell's environment, which carries tokens. Through this helper the agent
shell's inherited environment does not enter the App: the App's environment is
built from nothing. (What the App passes on to the supplier it starts is the
App's own: it sets the supplier's home and removes credential names.) An
inherited environment with names removed is not enough.

The launched program is treated as able to write anywhere the user can,
including the helper's own files. Each guarantee is held in one place in this
file (search for "INVARIANT" and "RULE"):

1. INVARIANT 1, the environment. The App's environment is a new mapping built
   from a written allowlist, never derived from this process's environment,
   and checked against the allowlist immediately before the App starts.
2. INVARIANT 2, a clean run. A run is clean only when the App exited by itself
   with status 0, no stop was latched (RULE C), no process of its process group
   was left, and the real Library places named for the build were listed whole
   before and twice after, with no link met and nothing differing. RULE C: the
   stop command signals the helper (found through its own process file, start
   time checked), never the App; the helper latches every stop it receives in
   memory before forwarding SIGTERM to the App, and nothing in the run folder is
   read to judge the run. RULE D: the per-user cache and preference folders are
   observations that never refuse a launch or fail a run; when one was not made
   whole, the record says why and gives no changes for it.
3. INVARIANT 3, what is watched. Entries whose name contains the bundle
   identifier (ending there or before a separator), equals the executable name,
   or is the system web view helper folder for that executable. An executable
   name that does not discriminate is refused.
4. INVARIANT 4, places. Judged by device and inode, not spelling: the launch
   folder and run folder are not inside the real home's Library, are not and do
   not contain the real home, and are not inside a checkout; a bundle under any
   folder named Applications, in any letter case, is refused.
5. INVARIANT 5, the throwaway home. RULE A: the helper never reads anything
   under a throwaway home. It creates the home, the App's temporary folder and
   one output file per launch there (created exclusively, write-only, never read
   back; its size is taken from the helper's own descriptor), and in remove
   deletes the tree; nothing else. The home itself is only lstat'ed, for its
   identity. Its own records about a home (marker and custody state) live in a
   control folder beside the home, inside one launch folder the helper makes.
   RULE B: what the helper reads back (marker, custody state, process file) is
   opened without following links, must be a regular file with one link owned
   by the user, and must parse to the helper's closed format; anything else,
   including a missing custody state, is a refusal. Nothing read from a file is
   quoted in a record, the helper's output or an error message; errors about a
   home name the launch folder only.
6. INVARIANT 6, the candidate. The identification record is validated and
   identification's own check (identify.check) must find the bundle equal to
   it. The check hashes the whole bundle twice, a few seconds for a real build.
7. INVARIANT 7, the overrides. Every launch that is not the owner's sitting is
   passed the address override and the proxy overrides, checked in the mapping
   immediately before launch; an owner's-sitting launch is passed neither. This
   is an environment construction, a check and a refusal; the helper reads
   nothing in any home for it. Each home has a kind, fixed when the helper
   creates it (--owner-sitting on the first launch, never the default), kept in
   the control folder's marker and in the launch folder's name, and never
   changed: a launch of a home under the other kind is refused, so an
   owner's-sitting home is never launched with the overrides and another home
   never without them. An owner's-sitting home is the one home in which the
   supplier may address its real service, because the owner signs in there as
   their own act. The proxy overrides are the eight names of PROXY_OVERRIDES
   (a loopback port where nothing listens, loopback exempted); the address
   override is the App's development input CHIRALITY_DEV_OPENAI_BASE_URL, a
   loopback address under MODEL_ADDRESS_RULE. The overrides redirect the
   built-in provider's address and obstruct some of the supplier's other
   clients under their defaults; they do not establish where a launch's
   requests went. Outside them: a home whose configuration turns on the
   supplier's system proxy feature (the operating system's answer is then taken
   first), the supplier's clients built for direct routing, redirects, what
   Codex itself starts, the web view's helpers (started by the system without
   the launch environment), and the system. The exemption is by exact host, so a
   loopback stub must be addressed as 127.0.0.1, localhost or [::1]. The record
   names the overrides passed and says whether the input's name was found in
   the executable (a byte search, nothing more).

Limits:
- The comparison sees names, kinds, sizes and modification times, not
  content: a file changed with its size and time restored reads unchanged.
  Names of entries named for the build in the real Library, the per-user cache
  folder and Preferences are reported, never their contents.
- The App startup inputs are a closed set of names; their values are the
  caller's responsibility. A caller can point them at real locations, and every
  value given is written into the record verbatim: never give a credential as
  a value.
- The marker is a consistency check against mistakes and stale paths, not
  proof against a deliberate forgery by a process of the same user: a
  same-user process that rewrites the control folder and the launch folder's
  name consistently (including the home's kind) is not guarded against. In remove,
  between the identity check (lstat of the launch folder, home and control
  folder) and the deletion, a process of the same user could put something
  else at the launch folder's path; the deletion would remove that.
- A custody state naming a process identifier later reused by an unrelated
  process refuses reuse and removal; that launch folder is then abandoned and
  removed by hand.
- It does not confine the App (no operating-system write restriction), and the
  comparison covers only the places in WATCHED. It does not redirect the
  operating system's own records about an application that opens a window; it
  discloses them. A new throwaway home has no login keychain and no signed-in
  session; a kept one may hold the owner's signed-in state for the build after
  the owner's own sitting, which is why the reuse launch is meant to be the only
  thing that opens it and why the helper never reads it. A step that must use
  the real login keychain or the owner's own home is outside this helper.
- Identification's freshness check still reads the real home and is not
  pointed at the throwaway home. The helper sends no input to the App and does
  not look at its window.
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
import threading  # noqa: E402
import time  # noqa: E402
from xml.parsers.expat import ExpatError  # noqa: E402

HERE = Path(__file__).resolve().parent
REPOSITORY = HERE.parents[2]
sys.path.insert(0, str(HERE.parent / 'candidate_identity'))
import identify  # noqa: E402  (identification's record validation, check and shared identity rule)

TOOL = 'app/examination/standalone/launch.py'
NOTE = ('Evidence for a journey step record, written by ' + TOOL + '; not an examination record format, '
        'and nothing validates it.')
HOME, CONTROL = 'home', 'control'  # the two entries of a launch folder
MARKER, STATE = 'marker.json', 'state.json'  # in the control folder
TMP = '.chirality-launch-tmp'  # the App's temporary folder, in the home
RECORD, PROCESS = 'launch-record.json', 'app-process.json'  # in the run folder
SYSTEM_PATH = '/usr/bin:/bin:/usr/sbin:/sbin'
DEFAULT_LANG = 'en_US.UTF-8'
LOCALE = re.compile(r'C|POSIX|[A-Za-z]{2,3}(?:_[A-Za-z]{2})?(?:\.[A-Za-z0-9-]+)?')

# INVARIANT 1: every name the App's environment can hold, with why it is there.
ALLOWED = {
    'HOME': 'the throwaway home, the home of the App and every process it starts',
    'CFFIXED_USER_HOME': "the same throwaway home for the system frameworks (web view data and caches), which HOME alone does not move",
    'TMPDIR': "temporary files, in the App's temporary folder inside the throwaway home",
    'PATH': 'the fixed system path, so system tools are found and nothing of the caller is',
    'LANG': "the App's locale: the fixed default or the caller's explicit --lang, never inherited",
}
# The App's own startup inputs (keys of explicit_environment_launch in
# app/src-tauri/src/lib.rs, and records_store.rs OVERRIDE_ENV). Given only when
# the caller names one; any one selects the App's explicit environment route.
# Values are the caller's responsibility and are recorded verbatim.
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
    'CHIRALITY_RECORDS_STORE': 'the records store override',
}

# INVARIANT 3: the Library folders searched, beside the Library's own first
# level. Protected folders (Containers, Group Containers, Mail, Safari and the
# like) are not listed: reading them can be refused or raise a privacy prompt,
# and a development build does not write there through the home.
WATCHED = ('Application Support', 'Caches', 'WebKit', 'HTTPStorages', 'Preferences', 'Saved Application State',
           'Logs', 'Cookies', 'Application Scripts', 'Autosave Information', 'LaunchAgents')
# INVARIANT 7: fixed names and values every launch whose home is NOT the owner's sitting carries, and an
# owner's-sitting launch never carries: name -> (value, why). Used by child_environment and check_environment.
# All eight: the supplier has a websocket client (reads HTTPS, then HTTP, then ALL, upper case first) and an HTTP
# client (HTTPS for secure, HTTP for plain destinations, ALL as fallback); a name left unset could be the one read.
_PROXY = ('http://127.0.0.1:9', 'scheme http because the websocket client rejects an https proxy; port 9 is this '
          "repository's address where no server runs, so a connection is refused at once")
_EXEMPT = ('127.0.0.1,localhost,::1', 'loopback exempted without ports, brackets or spaces (the HTTP client does not '
           'understand ports and takes a bracketed entry as a name), with localhost because neither client resolves '
           'a name before comparing')
PROXY_OVERRIDES = {**{name: _PROXY for name in ('HTTPS_PROXY', 'https_proxy', 'HTTP_PROXY', 'http_proxy',
                                                     'ALL_PROXY', 'all_proxy')},
                        'NO_PROXY': _EXEMPT, 'no_proxy': _EXEMPT}
# The App's development input fixing the supplier's model address on its command line (arrives with the Access
# lane's change from branch claude/access-local-settings; builds without it ignore the name). Non-owner launches
# carry it, by default at a loopback port where nothing listens; a caller may name a loopback stub instead.
MODEL_ADDRESS = 'CHIRALITY_DEV_OPENAI_BASE_URL'
DEFAULT_MODEL_ADDRESS = 'http://127.0.0.1:9/v1'
MODEL_ADDRESS_RULE = re.compile(r'https?://(?:127\.0\.0\.1|\[::1\])(?::([1-9][0-9]{0,4}))?(?:/[A-Za-z0-9._~/-]*)?')
KINDS = ('owners-sitting', 'not-owners-sitting')
EXECUTABLE_RULE = re.compile(r'chirality-[a-z0-9][a-z0-9_-]{2,}')  # e.g. chirality-app-v4

# RULE B: the helper's own files and their closed formats (name: allowed types).
NUMBER, MAYBE_NUMBER, TEXT = (int,), (int, type(None)), (str,)
MARKER_FORMAT = {'format': TEXT, 'path': TEXT, 'kind': TEXT, 'folder_device': NUMBER, 'folder_inode': NUMBER,
                 'home_device': NUMBER, 'home_inode': NUMBER, 'control_device': NUMBER, 'control_inode': NUMBER}
STATE_FORMAT = {'format': TEXT, 'helper_pid': MAYBE_NUMBER, 'process_group': MAYBE_NUMBER}
PROCESS_FORMAT = {'format': TEXT, 'helper_pid': NUMBER, 'helper_start': TEXT, 'app_pid': NUMBER}
FORMATS = {id(MARKER_FORMAT): 'chirality-launch-marker/1', id(STATE_FORMAT): 'chirality-launch-state/1',
           id(PROCESS_FORMAT): 'chirality-launch-process/1'}

_forwarding = threading.Event()  # set while the helper's signal forwarding is installed (tests wait on it)


class Refusal(ValueError):
    """A refusal whose message is the helper's own words, never content read from a file."""


def real_home():
    """The real home, from the account database, never from HOME; the one place tests point elsewhere."""
    return Path(os.path.realpath(pwd.getpwuid(os.getuid()).pw_dir))


def user_cache_dir():
    """RULE D: the per-user cache folder as getconf DARWIN_USER_CACHE_DIR reports it, not resolved; None if none."""
    try:
        result = subprocess.run(['/usr/bin/getconf', 'DARWIN_USER_CACHE_DIR'], capture_output=True, text=True,
                                env={'PATH': SYSTEM_PATH})
    except OSError:
        return None
    value = result.stdout.strip().rstrip('/')
    return Path(value) if result.returncode == 0 and value.startswith('/') else None


def now():
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, 'rb') as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


# ---- INVARIANT 4: places by identity -----------------------------------------------------------

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
    """INVARIANT 4: a place the helper writes, reuses or removes (never a path inside a throwaway home)."""
    path = Path(os.path.abspath(path))
    home = real_home()
    if inside(path, home / 'Library'):
        raise Refusal(f'{what} is inside the real home Library: {path}')
    if os.path.lexists(path) and inside(home, path):
        raise Refusal(f'{what} is or contains the real home: {path}')
    real = Path(os.path.realpath(path))
    if inside(path, REPOSITORY) or any(os.path.lexists(p / '.git') for p in (real, *real.parents)):
        raise Refusal(f'{what} is inside a repository checkout: {path}')
    return path


def under_applications(path):
    """INVARIANT 4: any ancestor named Applications, in any letter case, wherever it is."""
    names = [name for _, name in ancestry(path)] + list(Path(os.path.abspath(path)).parts)
    return any(name.lower() == 'applications' for name in names)


# ---- INVARIANT 6: only the identified candidate ------------------------------------------------

def identify_candidate(app, record_path):
    """INVARIANT 6: the record is valid and identification's own check finds the bundle equal to it."""
    record = json.loads(Path(record_path).read_bytes())
    if not isinstance(record, dict) or not record.get('candidate_key'):
        raise Refusal('the identification record has no candidate key')
    identify.validate_record(record)
    result = identify.check(argparse.Namespace(record=str(record_path), app=str(app)))
    if not (result['equal'] and result['build_identity'] == result['recorded_build_identity']
            and not result.get('record_fields_mismatched')):
        differing = (result.get('changed', []) + result.get('missing', []) + result.get('extra', [])
                     + result.get('record_fields_mismatched', []))
        raise Refusal('the bundle differs from its identification record: ' + (', '.join(differing[:10]) or
                                                                              'build identity differs'))
    return record


# ---- INVARIANT 3: what is watched --------------------------------------------------------------

def check_executable(executable):
    """INVARIANT 3: an executable name that does not discriminate is refused before launch."""
    if not isinstance(executable, str) or not EXECUTABLE_RULE.fullmatch(executable.lower()):
        raise Refusal(f'executable name {executable!r} does not discriminate (it must match '
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
    """Names, kinds, sizes and times of watched entries under base, walked; contents never read; links never followed.

    Returns (entries, links): every link met at the base, a watched folder, a watched entry or beneath one.
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


def differences(before, after):
    return [{'path': p, 'change': 'created' if p not in before else 'removed' if p not in after else 'modified'}
            for p in sorted(before.keys() | after.keys()) if before.get(p) != after.get(p)]


# ---- INVARIANT 2: a clean run ------------------------------------------------------------------

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
    """INVARIANT 2, the one place a run is judged. Nothing in the run folder is read for it."""
    failures = []
    if not facts.get('started'):
        failures.append('the App was not started')
    else:
        if facts.get('returncode') != 0:
            failures.append('the App ' + facts['ended'])
        if facts.get('stops'):
            failures.append(f"a stop was latched ({len(facts['stops'])}); the App did not end by itself")
        if facts.get('process_group') != 'gone':
            failures.append("a process of the App's process group was still running after the settle time")
    result = facts.get('comparison', {}).get('result', 'not made')
    if result != 'unchanged':
        failures.append({'not made': 'no complete comparison was made',
                         'incomplete': 'the comparison is incomplete: a link was met at or beneath a watched place',
                         'changed': 'the real Library changed in places named for the build'}[result])
    return ('clean' if not failures else 'failed'), failures


# ---- RULE D: observations that never gate ------------------------------------------------------

def observe(base, folders, identifier, executable, what):
    """RULE D: an observation, never a refusal or a failure. Returns (entries, None) or (None, reason by category)."""
    if base is None:
        return None, f'not observed: there is no {what} on this system'
    if os.path.islink(base):
        return None, f'not observed: the {what} is a link'
    try:
        entries, links = listing(base, folders, identifier, executable)
    except OSError as error:
        return None, f'not observed: the {what} or an entry in it could not be listed ({type(error).__name__})'
    if links:
        return None, f'incomplete: a link was met in the {what}'
    return entries, None


def preferences_observation():
    """RULE D: files directly under the real Library/Preferences, by name, size and time."""
    folder = real_home() / 'Library/Preferences'
    if os.path.islink(folder):
        return None, 'not observed: the preference folder is a link'
    try:
        with os.scandir(folder) as found:
            return {e.name: _describe(e.stat(follow_symlinks=False)) for e in found
                    if not e.is_dir(follow_symlinks=False)}, None
    except FileNotFoundError:
        return {}, None
    except OSError as error:
        return None, f'not observed: the preference folder could not be listed ({type(error).__name__})'


def disclosure(before, after, what, exclude=()):
    """RULE D: changes only when both observations were made; otherwise why not, and no changes at all."""
    if before[1] or after[1]:
        return {'observation': before[1] or after[1]}
    return {'observation': 'made', 'what': what,
            'changes': [c for c in differences(before[0], after[0]) if c['path'] not in exclude]}


# ---- RULE B: the helper's own files, read defensively ------------------------------------------

def write_own(path, fmt, values):
    value = {'format': FORMATS[id(fmt)], **values}
    if set(value) != set(fmt):
        raise Refusal('internal: fields differ from the closed format')
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, 'w') as stream:
        stream.write(json.dumps(value) + '\n')


def replace_own(path, fmt, values):
    temporary = Path(path).with_name(f'.{Path(path).name}.{os.getpid()}.{secrets.token_hex(3)}')
    write_own(temporary, fmt, values)
    os.replace(temporary, path)


def read_own(path, fmt, what):
    """RULE B: no link followed; a regular file with one link, owned by the user; the closed format exactly."""
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    except OSError:
        raise Refusal(f'{what} is missing, a link or unreadable') from None
    try:
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1 or info.st_uid != os.getuid() or info.st_size > 4096:
            raise Refusal(f"{what} is not the helper's own plain file")
        data = os.read(fd, 4097)
    finally:
        os.close(fd)
    try:
        value = json.loads(data)
    except ValueError:
        raise Refusal(f'{what} is not in the helper\'s format') from None
    if not isinstance(value, dict) or set(value) != set(fmt) or value.get('format') != FORMATS[id(fmt)] or any(
            type(value[k]) not in types for k, types in fmt.items()):
        raise Refusal(f"{what} is not in the helper's format")
    return value


class HomeError(Refusal):
    pass


def home_operation(folder, action):
    """RULE B: an error from an operation under a throwaway home names the launch folder only."""
    try:
        return action()
    except OSError as error:
        raise HomeError(f'an operation on the throwaway home in {folder} failed ({type(error).__name__})') from None


# ---- INVARIANT 5: the launch folder, its home and control folder (RULES A and B) ---------------

def plan_folder(parent, kind):
    """A new launch folder path under the caller's parent, its place checked before anything is made."""
    parent = Path(os.path.abspath(parent))
    if parent.is_symlink() or not parent.is_dir():
        raise Refusal('the parent must be an existing directory, not a link: ' + str(parent))
    name = f'launch-{kind}-{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}-{secrets.token_hex(4)}'
    return check_place(Path(os.path.realpath(parent)) / name, 'launch folder')


def make_folder(folder, kind):
    """RULE A: makes the home and the App's temporary folder in it; reads nothing there. The marker and an idle
    custody state go in the control folder beside the home."""
    check_place(folder, 'launch folder')
    os.mkdir(folder, 0o700)
    os.mkdir(folder / CONTROL, 0o700)
    home_operation(folder, lambda: (os.mkdir(folder / HOME, 0o700), os.mkdir(folder / HOME / TMP, 0o700)))
    ids = {key: os.lstat(folder / part) for key, part in (('folder', '.'), ('home', HOME), ('control', CONTROL))}
    if kind not in KINDS:
        raise Refusal('internal: unknown home kind')
    write_own(folder / CONTROL / MARKER, MARKER_FORMAT, {
        'path': str(folder), 'kind': kind, **{f'{k}_device': v.st_dev for k, v in ids.items()},
        **{f'{k}_inode': v.st_ino for k, v in ids.items()}})
    write_own(folder / CONTROL / STATE, STATE_FORMAT, {'helper_pid': None, 'process_group': None})
    return folder


def own_folder(path):
    """INVARIANT 5: a launch folder this helper made, by the identity its marker records (lstat of the folder, the
    home and the control folder themselves; nothing inside the home is read)."""
    given = Path(os.path.abspath(path))
    if given.is_symlink():
        raise Refusal('refusing a link: ' + str(given))
    folder = check_place(Path(os.path.realpath(given)), 'launch folder')
    marker = read_own(folder / CONTROL / MARKER, MARKER_FORMAT, 'the launch folder marker')
    if marker['kind'] not in KINDS:
        raise Refusal("the launch folder marker is not in the helper's format")
    if not folder.name.startswith(f"launch-{marker['kind']}-"):  # the kind is fixed in the name as well as the marker
        raise Refusal(f"the launch folder's recorded kind does not agree with its name: {folder}")
    for key, part in (('folder', '.'), ('home', HOME), ('control', CONTROL)):
        try:
            info = os.lstat(folder / part)
        except OSError:
            info = None
        if marker['path'] != str(folder) or info is None or not stat.S_ISDIR(info.st_mode) \
                or (info.st_dev, info.st_ino) != (marker[f'{key}_device'], marker[f'{key}_inode']):
            raise Refusal(f'not a launch folder made by this helper (its recorded identity differs): {folder}')
    return folder, marker['kind']


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


def in_use(folder):
    """INVARIANT 5 custody: a missing or invalid state refuses; a live launch or group member keeps the folder in use."""
    state = read_own(folder / CONTROL / STATE, STATE_FORMAT, 'the custody state')
    reasons = []
    if state['helper_pid'] is not None and _alive(state['helper_pid']):
        reasons.append(f"a launch (helper process {state['helper_pid']})")
    if state['process_group'] is not None and group_state(state['process_group']) != 'gone':
        reasons.append(f"a member of the App's process group {state['process_group']}")
    return reasons


def claim(folder):
    reasons = in_use(folder)
    if reasons:
        raise Refusal('the launch folder is in use by ' + ' and '.join(reasons))
    replace_own(folder / CONTROL / STATE, STATE_FORMAT, {'helper_pid': os.getpid(), 'process_group': None})


def release(folder, group):
    """Custody outlives the launcher: a living group stays recorded and keeps the launch folder in use."""
    alive = group is not None and group_state(group) != 'gone'
    replace_own(folder / CONTROL / STATE, STATE_FORMAT, {'helper_pid': None, 'process_group': group if alive else None})


def delete_tree(folder):
    """RULE A, remove only: delete the launch folder; entries without permission are opened up first. Errors name the
    launch folder only."""
    def run():
        os.chmod(folder, 0o700)
        for current, dirs, _ in os.walk(folder):
            for name in dirs:
                path = os.path.join(current, name)
                if not os.path.islink(path):
                    os.chmod(path, 0o700)
        shutil.rmtree(folder)
    try:
        run()
    except OSError as error:
        raise HomeError(f'could not remove all of the launch folder {folder} ({type(error).__name__}); '
                        'part of it may remain') from None


# ---- INVARIANT 1: the environment --------------------------------------------------------------

def app_inputs(pairs):
    given = {}
    for pair in pairs or ():
        name, sep, value = pair.partition('=')
        if not sep or name not in APP_INPUTS or '\0' in value:
            raise Refusal(f'not an App startup input (allowed: {", ".join(APP_INPUTS)}): {name!r}')
        if name in given:
            raise Refusal('App startup input given twice: ' + name)
        given[name] = value
    return given


def check_model_address(value):
    """INVARIANT 7: a loopback address only, by the helper's own rule (localhost is not accepted)."""
    match = MODEL_ADDRESS_RULE.fullmatch(value) if isinstance(value, str) and len(value) <= 2048 else None
    if not match or (match.group(1) and not 1 <= int(match.group(1)) <= 65535):
        raise Refusal(f'{MODEL_ADDRESS} must be http(s)://127.0.0.1 or [::1], an optional port 1-65535 and a plain path')
    return value


def child_environment(home, inputs, lang, kind, model_address=DEFAULT_MODEL_ADDRESS):
    """INVARIANTS 1 and 7: a new mapping from the allowlist alone; nothing is read from this process's environment."""
    env = {'HOME': str(home), 'CFFIXED_USER_HOME': str(home), 'TMPDIR': str(Path(home, TMP)),
           'PATH': SYSTEM_PATH, 'LANG': lang}
    env.update(inputs)
    if kind != 'owners-sitting':
        env.update({name: value for name, (value, _) in PROXY_OVERRIDES.items()})
        env[MODEL_ADDRESS] = model_address
    return env


def check_environment(env, home, kind):
    """INVARIANTS 1 and 7, immediately before the App starts: the allowlist exactly, the homes and TMPDIR as
    constructed, and the address and proxy overrides present with their fixed or rule-conforming values unless the home is the owner's
    sitting, where they are absent."""
    if not isinstance(env, dict) or not all(isinstance(k, str) and isinstance(v, str) for k, v in env.items()):
        raise Refusal('the App environment is not a mapping of names to text')
    if kind not in KINDS:
        raise Refusal('unknown home kind')
    for name, (value, _) in PROXY_OVERRIDES.items():
        if (env.get(name) != value) if kind != 'owners-sitting' else (name in env):
            raise Refusal(f'{name} is not as invariant 7 requires for this home; refusing to launch')
    if kind == 'owners-sitting':
        if MODEL_ADDRESS in env:
            raise Refusal(f"{MODEL_ADDRESS} is not given to an owner's-sitting launch; refusing to launch")
    else:
        check_model_address(env.get(MODEL_ADDRESS))
    extra = set(env) - set(ALLOWED) - set(APP_INPUTS) - set(PROXY_OVERRIDES) - {MODEL_ADDRESS}
    missing = set(ALLOWED) - set(env)
    if extra or missing:
        raise Refusal(f'App environment outside the allowlist: extra {sorted(extra)}, missing {sorted(missing)}')
    if env['HOME'] != str(home) or env['CFFIXED_USER_HOME'] != str(home):
        raise Refusal('HOME and CFFIXED_USER_HOME must both be the throwaway home; refusing to launch')
    if env['TMPDIR'] != str(Path(home, TMP)):
        raise Refusal("TMPDIR is not the App's temporary folder in the throwaway home; refusing to launch")
    if env['PATH'] != SYSTEM_PATH or not LOCALE.fullmatch(env['LANG']):
        raise Refusal('PATH or LANG differs from the allowlist')
    return env


# ---- the run -----------------------------------------------------------------------------------

def address_input_note(executable, kind):
    """INVARIANT 7: whether the input's name occurs in the executable, by a byte search and labelled as exactly that."""
    if kind == 'owners-sitting':
        return {'passed': False, 'note': "an owner's-sitting launch is passed neither the address nor the proxy overrides"}
    found = MODEL_ADDRESS.encode() in Path(executable).read_bytes()
    note = {'passed': True, 'name': MODEL_ADDRESS,
            'executable': 'the name was found in the executable' if found else 'the name was not found in the executable'}
    if not found:
        note['note'] = 'this build reads no address override; only the proxy overrides apply to it'
    return note


def process_start(pid):
    """The process's start time as ps reports it, or None; tells a process from a reused identifier."""
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


def launch(args):
    app = Path(os.path.abspath(args.app))
    if under_applications(app):
        raise Refusal('a bundle under an Applications folder is not launched: ' + str(app))
    inputs = app_inputs(args.app_env)
    if not LOCALE.fullmatch(args.lang) or args.settle_seconds < 0:
        raise Refusal('invalid --lang or --settle-seconds')
    record_data = identify_candidate(app, args.record)
    identifier = record_data['bundle']['identifier']
    executable_path = record_data['bundle']['executable']['path']
    executable = executable_path.rsplit('/', 1)[-1]
    check_executable(executable)
    run = check_place(args.run_dir, 'run folder')
    if args.reuse:
        folder, kind = own_folder(args.reuse)
        if args.owner_sitting and kind != 'owners-sitting':
            raise Refusal("--owner-sitting contradicts this launch folder's kind, fixed when it was made")
        reasons = in_use(folder)
        if reasons:
            raise Refusal('the launch folder is in use by ' + ' and '.join(reasons))
    else:
        kind = 'owners-sitting' if args.owner_sitting else 'not-owners-sitting'
        folder = plan_folder(args.parent, kind)
    if kind == 'owners-sitting' and args.model_address is not None:
        raise Refusal("--model-address is not given to an owner's-sitting launch")
    os.mkdir(run, 0o700)
    if args.reuse:
        folder_note = {'launch_folder': str(folder), 'state': 'reused'}
    else:
        make_folder(folder, kind)
        folder_note = {'launch_folder': str(folder), 'state': 'created', 'home_empty_when_created': True}
    home = folder / HOME
    claim(folder)
    if args.reuse:  # RULE A: recreate the App's temporary folder if the App removed it; nothing in the home is read
        try:
            os.mkdir(home / TMP, 0o700)
        except FileExistsError:
            pass
        except OSError:
            home_operation(folder, lambda: _raise(OSError()))
    env = child_environment(home, inputs, args.lang, kind,
                            check_model_address(args.model_address or DEFAULT_MODEL_ADDRESS))
    record = {'note': NOTE, 'helper': {'path': TOOL, 'sha256': sha256_file(__file__)},
              'candidate_key': record_data['candidate_key'], 'identifier': identifier, 'bundle': str(app),
              'identification_record': str(Path(os.path.abspath(args.record))),
              'launch_folder': folder_note, 'home': str(home), 'home_kind': kind, 'environment': env,
              'overrides_passed': ({name: env[name] for name in (*PROXY_OVERRIDES, MODEL_ADDRESS) if name in env}
                                   or "none (an owner's-sitting launch)"),
              'address_override_input': address_input_note(app / executable_path, kind),
              'watched': {'rule': 'name contains the identifier, equals the executable name, or is '
                                  'com.apple.WebKit.<Networking|WebContent|GPU>+<executable with _ for ->-<suffix>',
                          'identifier': identifier, 'executable': executable,
                          'places': ['Library', *('Library/' + w for w in WATCHED)]}}
    facts = {'started': False, 'stops': []}
    proc, output = None, None
    cache = user_cache_dir()
    previous = {}

    def latch(signum, frame):  # RULE C: the stop is recorded in memory before anything is forwarded
        facts['stops'].append({'signal': signal.Signals(signum).name, 'at': now()})
        if proc is not None and proc.poll() is None:
            try:
                proc.send_signal(signal.SIGTERM)
            except ProcessLookupError:
                pass
    try:
        for s in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):
            previous[s] = signal.signal(s, latch)
        _forwarding.set()
        try:
            before = listing(real_home() / 'Library', ('', *WATCHED), identifier, executable)
        except OSError as error:
            facts['ended'] = record['ended'] = f'not launched: the before-listing failed ({type(error).__name__})'
            record['started_at'] = None
            return _finish(run, record, facts, code=2, label='not launched')
        prefs_before = preferences_observation()
        cache_before = observe(cache, ('',), identifier, executable, 'per-user cache folder')
        try:  # immediately before the start: the mapping (INVARIANTS 1 and 7) and the home's identity
            check_environment(env, home, kind)
            if (os.lstat(home).st_dev, os.lstat(home).st_ino) != tuple(
                    read_own(folder / CONTROL / MARKER, MARKER_FORMAT, 'the launch folder marker')[k]
                    for k in ('home_device', 'home_inode')):
                raise Refusal(f'the home in {folder} is not the one this helper made')
        except (Refusal, OSError) as error:
            reason = str(error) if isinstance(error, Refusal) else type(error).__name__
            facts['ended'] = record['ended'] = f'not launched: {reason}'
            record['started_at'] = None
            return _finish(run, record, facts, code=2, label='not launched')
        if facts['stops']:  # RULE C: a stop latched before the start means the App is not started
            facts['ended'] = record['ended'] = 'not launched: a stop was latched before the App started'
            record['started_at'] = None
            return _finish(run, record, facts, code=2, label='not launched')
        output_path = home / f'.chirality-launch-output-{run.name}-{secrets.token_hex(3)}.log'
        output = home_operation(folder, lambda: os.open(
            output_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600))
        record['started_at'] = now()
        try:
            proc = subprocess.Popen([str(app / executable_path)], env=env, cwd=home, stdin=subprocess.DEVNULL,
                                    stdout=output, stderr=output, start_new_session=True, close_fds=True)
        except OSError as error:
            facts['ended'] = record['ended'] = f'did not start ({type(error).__name__})'
            record['ended_at'] = now()
            return _finish(run, record, facts, code=1)
        facts['started'] = True
        record['pid'] = proc.pid
        if facts['stops']:  # RULE C: a stop latched while the App was being started is forwarded now
            proc.send_signal(signal.SIGTERM)
        replace_own(folder / CONTROL / STATE, STATE_FORMAT, {'helper_pid': os.getpid(), 'process_group': proc.pid})
        write_own(run / PROCESS, PROCESS_FORMAT, {'helper_pid': os.getpid(), 'helper_start': process_start(os.getpid()) or '',
                                                  'app_pid': proc.pid})
        print(json.dumps({'launched': proc.pid, 'run_folder': str(run), 'launch_folder': str(folder)}),
              file=sys.stderr, flush=True)
        facts['returncode'] = proc.wait()
        facts['ended'] = record['ended'] = how_it_ended(facts['returncode'])
        record['ended_at'] = now()
        time.sleep(args.settle_seconds)
        facts['process_group'] = record['process_group_after_settle'] = group_state(proc.pid)
        after = again = None
        try:
            after = listing(real_home() / 'Library', ('', *WATCHED), identifier, executable)
            time.sleep(args.settle_seconds)
            again = listing(real_home() / 'Library', ('', *WATCHED), identifier, executable)
        except OSError as error:
            record['after_listing'] = f'failed ({type(error).__name__})'
        prefs_after = preferences_observation()
        cache_after = observe(cache, ('',), identifier, executable, 'per-user cache folder')
        facts['comparison'] = compare(before, after, again)
        named = {p.split('/', 1)[1] for p in before[0].keys() | (after or ({}, []))[0].keys() if p.startswith('Preferences/')}
        record['disclosed'] = {
            'note': "changed during the run by the operating system's own services or anything else running; "
                    'names and times only; not opened, edited or removed; never a failure',
            'preferences': disclosure(prefs_before, prefs_after, 'files directly under the real Library/Preferences', named),
            'user_cache': {'folder': str(cache) if cache else None,
                           **disclosure(cache_before, cache_after, 'entries named for the build')}}
        record['output'] = {'path': str(output_path), 'size': os.fstat(output).st_size,
                            'note': "kept inside the throwaway home; size from the helper's own descriptor; never read"}
        return _finish(run, record, facts, code=None)
    finally:
        if output is not None:
            os.close(output)
        if proc is not None and proc.poll() is None:
            print(json.dumps({'warning': f'the App (process {proc.pid}) is still running; no record says it ended'}),
                  file=sys.stderr)
        try:
            release(folder, proc.pid if proc is not None else None)
        finally:
            _forwarding.clear()
            for s, handler in previous.items():
                signal.signal(s, handler)


def _finish(run, record, facts, code, label=None):
    result, failures = outcome(facts)
    record['real_library'] = facts.get('comparison', {'result': 'not made'})
    record['stops'] = list(facts['stops'])  # from the helper's memory (RULE C), never from the run folder
    record['failures'] = failures
    record['outcome'] = label or result
    path = Path(run, RECORD)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)  # written once, after the comparison
    with os.fdopen(fd, 'w') as stream:
        stream.write(json.dumps(record, indent=2) + '\n')
    print(json.dumps({'outcome': record['outcome'], 'record': str(path), 'failures': failures}, indent=2))
    return code if code is not None else (0 if result == 'clean' else 1)


def stop(run_dir):
    """RULE C: signal the helper of a run (never the App directly); the helper latches the stop and forwards it."""
    process = read_own(Path(os.path.abspath(run_dir), PROCESS), PROCESS_FORMAT, "the run's process file")
    helper = process['helper_pid']
    if not process['helper_start'] or process_start(helper) != process['helper_start']:
        raise Refusal('the helper of this run is not running; nothing was signalled '
                      "(end the App with its own Quit, or by hand)")
    os.kill(helper, signal.SIGTERM)
    return {'signalled_helper': helper, 'signal': 'SIGTERM'}


def remove(path):
    """INVARIANT 5: remove a launch folder this helper made, by identity, when nothing of a launch lives."""
    folder, _ = own_folder(path)
    reasons = in_use(folder)
    if reasons:
        raise Refusal('the launch folder is in use by ' + ' and '.join(reasons))
    delete_tree(folder)
    return {'removed': str(folder)}


def main(argv=None):
    parser = argparse.ArgumentParser(
        description=__doc__.splitlines()[0],
        epilog='A launch folder (launch-<time>-<random>) holds the throwaway home (home/) and the helper\'s control '
               'folder (control/); --reuse and remove take the launch folder. Exit status: 0 clean run, 1 run made '
               'but not clean (see the record), 2 refused or not launched. Invariants, rules and limits are in the '
               'module docstring.')
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('launch', help='launch the identified bundle in a throwaway home and compare the real Library')
    p.add_argument('--app', required=True, help='the built development bundle (.app)')
    p.add_argument('--record', required=True, help="its candidate identification record; identification's check must pass")
    p.add_argument('--run-dir', required=True, help='new folder for the run record; outside any checkout and the real Library')
    where = p.add_mutually_exclusive_group(required=True)
    where.add_argument('--parent', help='existing folder in which a new launch folder (home/ and control/) is made')
    where.add_argument('--reuse', metavar='LAUNCH_FOLDER', help='a launch folder this helper made, for a later launch '
                       'of the same walk')
    p.add_argument('--app-env', action='append', metavar='NAME=VALUE',
                   help='an App startup input (repeatable; none by default; the value is recorded verbatim, never give a '
                        'credential): ' + ', '.join(APP_INPUTS))
    p.add_argument('--owner-sitting', action='store_true',
                   help="make the new home the owner's sitting (the one kind of home whose supplier may address its real "
                        'service; it is passed no overrides); never the default; fixed when the home is made; on --reuse '
                        'only to confirm that kind')
    p.add_argument('--model-address', help=f'a loopback stub address for {MODEL_ADDRESS} (default {DEFAULT_MODEL_ADDRESS}, '
                   "where nothing listens); http(s)://127.0.0.1 or [::1] only; never for an owner's sitting")
    p.add_argument('--lang', default=DEFAULT_LANG, help='LANG for the App (default %(default)s; never inherited)')
    p.add_argument('--settle-seconds', type=float, default=5.0,
                   help='wait after the App exits before listing, and again before the second listing (default 5)')
    p = sub.add_parser('stop', help="ask a run's helper to stop the App (SIGTERM; the run is then not clean)")
    p.add_argument('--run-dir', required=True)
    p = sub.add_parser('remove', help='remove a launch folder this helper made, when no launch or App process lives')
    p.add_argument('--launch-folder', required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == 'launch':
            return launch(args)
        print(json.dumps(stop(args.run_dir) if args.command == 'stop' else remove(args.launch_folder)))
        return 0
    except (ValueError, KeyError, TypeError, AttributeError, OSError, ImportError, json.JSONDecodeError,
            plistlib.InvalidFileException, ExpatError, subprocess.CalledProcessError, tarfile.TarError,
            EOFError) as error:
        print(json.dumps({'error': f'{type(error).__name__}: {error}'}), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
