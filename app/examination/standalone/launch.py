#!/usr/bin/env python3
"""Launch one identified development App build in a throwaway home (DEL-09-02 examination tooling).

This is a controlled development launcher, not an isolation boundary.

What it guards, without exception:
1. The agent shell's environment does not enter the App through it. The App's
   environment is built from nothing. (What the App passes on to the supplier it
   starts is the App's own: it sets the supplier's home and removes credential
   names.)
2. It never reads anything under a home, and never carries anything from a
   home, or the content of anything a launched program wrote, into a record,
   its output or an error message. What it does carry from outside the home is
   only the comparison's evidence: the names, kinds, sizes and modification
   times of entries named for the build in the watched places and the per-user
   cache folder (which a launched program may have made), and how the App
   ended.
3. A caller's mistake about folders or kinds is refused, not acted on: a wrong
   path, a stale folder, a home of the other kind, a folder that is not the
   helper's, a link where a folder should be.
4. It never reports a clean run or an unchanged comparison that it did not
   establish: not when something is unreadable, missing or a link, not after a
   failed start, an interruption, or a stop at any moment.

The edge. A case is inside these guards if it can arise in the intended
workflow: an ordinary failure, an interruption (including the helper itself
being killed), two honest callers at once, a mistaken path, a home or launch
folder left over from another run. What is outside is a process of the same
user rearranging the helper's folders or forging its control files, at any
time, including between a check and a use; the intended workflow does not
contain one. That is the true edge, not an omission: such a process can read
any home on this account directly and needs no helper to do it, and protecting
a kept home that holds the owner's sign-in from other processes of this
account is not this helper's and is not claimed by it. One consequence: a
forged process file in the helper's format can direct `stop` at another
process of the same user.

How the guards are held (each in one place below, marked INVARIANT or RULE):
- INVARIANT 1, the environment: child_environment() builds a new mapping from
  the written allowlist; check_environment() checks it immediately before the
  App starts.
- INVARIANT 2, a clean run: outcome() calls a run clean only when the App
  exited by itself with status 0, no stop was accepted, no process of its group
  was left, and the real Library places named for the build were listed whole
  before and twice after with no link met and nothing differing. Anything that
  could not be examined makes the comparison "not made".
- RULE C, stops: the stop command signals the helper, never the App, and is
  answered "accepted" or "not accepted". A stop is accepted only before the
  finalization boundary; every accepted stop is in the record.
- RULE D, observations: the per-user cache folder and the preference files are
  observed, never a gate; when an observation is not made whole it says why and
  gives no changes.
- INVARIANT 3, exact names: watched_name() and check_executable().
- INVARIANT 4, places: judged by device and inode; every path to a folder the
  helper writes, reuses or removes must contain no link at all.
- INVARIANT 5 / RULE A, the home: the helper creates the home and, per launch,
  a fresh temporary folder and an output file in it, all through a held handle
  of the home; in remove it deletes the tree; it reads nothing there.
- RULE B, its own files: the marker, custody state, lock, process file and stop
  requests live in control/ beside the home, are reached only through no-follow
  handles from the launch folder, and must be regular, single-link, the user's,
  and in the helper's closed format; anything else is a refusal. Nothing read is
  quoted.
- INVARIANT 6, the candidate: identification's own check must find the bundle
  equal to its record (it hashes the bundle twice, a few seconds).
- INVARIANT 7, the overrides: every launch that is not the owner's sitting is
  passed the address override and the proxy overrides, checked in the mapping
  immediately before launch; an owner's-sitting launch is passed neither. A
  home's kind is fixed when it is made (--owner-sitting, never the default), in
  the marker and the launch folder's name. Every inconsistency of kind the
  helper can see before it starts the App is refused.

Limits:
- The App's HOME is a pathname, which the helper cannot bind to an identity.
  The helper checks before the start that the path resolves to the home it
  holds; after the start, a change is detected and the run marked not clean,
  but by then the overrides, and any write, have already reached the other
  place.
- The working directory is given to the App by pathname (no pre-exec hook).
- The comparison sees names, kinds, sizes and modification times, not content.
- App startup input values are the caller's and are recorded verbatim; never
  give a credential as a value.
- A custody state that names a process group whose identifier is later reused
  refuses conservatively; an interrupted launch (its helper killed) leaves the
  launch folder refused for reuse and remove. Such a folder is removed by hand.
- The address override replaces the built-in provider's address for model
  requests only; the proxy overrides obstruct some of the supplier's other
  clients under their defaults. They do not establish where a launch's requests
  went. Outside them: the built-in provider's model catalogue address (a
  separate supplier setting the input does not replace), a home configured for
  the supplier's system proxy feature, clients built for direct routing,
  redirects, what Codex itself starts, the web view's helpers and the system.
  The App passes the address to the supplier as a command-line setting, which a
  system managed configuration or managed preferences outrank; with such a
  file or preference present, the App refuses to start the supplier in that
  home, which is the App's refusal to report as observed. The helper reads
  neither.
- It does not confine the App, sends it no input and does not look at its
  window. Identification's freshness check still reads the real home.
"""
import sys

sys.dont_write_bytecode = True  # running the helper writes nothing beside the sources it imports

import argparse  # noqa: E402
from datetime import datetime, timezone  # noqa: E402
import fcntl  # noqa: E402
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
MARKER, STATE, LOCK, PROCESS = 'marker.json', 'state.json', 'lock', 'process.json'  # in control/
REQUEST, ANSWER = 'stop-request-', 'stop-answer-'  # stop requests and answers, in control/
RECORD = 'launch-record.json'  # in the run folder
SYSTEM_PATH = '/usr/bin:/bin:/usr/sbin:/sbin'
DEFAULT_LANG = 'en_US.UTF-8'
LOCALE = re.compile(r'C|POSIX|[A-Za-z]{2,3}(?:_[A-Za-z]{2})?(?:\.[A-Za-z0-9-]+)?')
NONCE = re.compile(r'[0-9a-f]{16}')
DIRECTORY = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW

# INVARIANT 1: every name the App's environment can hold, with why it is there.
ALLOWED = {
    'HOME': 'the throwaway home, the home of the App and every process it starts',
    'CFFIXED_USER_HOME': "the same throwaway home for the system frameworks (web view data and caches), which HOME alone does not move",
    'TMPDIR': 'a temporary folder made fresh for this launch inside the throwaway home',
    'PATH': 'the fixed system path, so system tools are found and nothing of the caller is',
    'LANG': "the App's locale: the fixed default or the caller's explicit --lang, never inherited",
}
# The App's own startup inputs (keys of explicit_environment_launch in app/src-tauri/src/lib.rs, and
# records_store.rs OVERRIDE_ENV). Given only when the caller names one; values are the caller's and recorded verbatim.
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
# INVARIANT 7: the proxy overrides every launch that is not the owner's sitting is passed: name -> (value, why).
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
# The address override: the App's development input fixing the supplier's model address on its command line.
MODEL_ADDRESS = 'CHIRALITY_DEV_OPENAI_BASE_URL'
DEFAULT_MODEL_ADDRESS = 'http://127.0.0.1:9/v1'
MODEL_ADDRESS_RULE = re.compile(r'https?://(?:127\.0\.0\.1|\[::1\])(?::([1-9][0-9]{0,4}))?(?:/[A-Za-z0-9._~/-]*)?')
KINDS = ('owners-sitting', 'not-owners-sitting')
LAUNCH_FOLDER_NAME = re.compile(r'launch-(?:owners-sitting|not-owners-sitting)-[0-9]{8}T[0-9]{6}Z-[0-9a-f]{8}')

# INVARIANT 3: the Library folders searched, beside the Library's own first level. Protected folders (Containers,
# Group Containers, Mail, Safari and the like) are not listed: reading them can be refused or raise a privacy prompt.
WATCHED = ('Application Support', 'Caches', 'WebKit', 'HTTPStorages', 'Preferences', 'Saved Application State',
           'Logs', 'Cookies', 'Application Scripts', 'Autosave Information', 'LaunchAgents')
EXECUTABLE_RULE = re.compile(r'chirality-[a-z0-9][a-z0-9_-]{2,}')  # e.g. chirality-app-v4

# RULE B: the helper's own files and their closed formats (name: allowed types).
NUMBER, MAYBE_NUMBER, TEXT = (int,), (int, type(None)), (str,)
MARKER_FORMAT = {'format': TEXT, 'path': TEXT, 'kind': TEXT, 'folder_device': NUMBER, 'folder_inode': NUMBER,
                 'home_device': NUMBER, 'home_inode': NUMBER, 'control_device': NUMBER, 'control_inode': NUMBER}
STATE_FORMAT = {'format': TEXT, 'phase': TEXT, 'process_group': MAYBE_NUMBER}
PROCESS_FORMAT = {'format': TEXT, 'helper_pid': NUMBER, 'helper_start': TEXT, 'app_pid': MAYBE_NUMBER}
REQUEST_FORMAT = {'format': TEXT, 'nonce': TEXT}
ANSWER_FORMAT = {'format': TEXT, 'nonce': TEXT, 'answer': TEXT}
FORMATS = {id(MARKER_FORMAT): 'chirality-launch-marker/2', id(STATE_FORMAT): 'chirality-launch-state/2',
           id(PROCESS_FORMAT): 'chirality-launch-process/2', id(REQUEST_FORMAT): 'chirality-launch-stop-request/1',
           id(ANSWER_FORMAT): 'chirality-launch-stop-answer/1'}
ACCEPTED, TOO_LATE = 'accepted', 'not accepted: the run had already ended'

_forwarding = threading.Event()  # set while the helper accepts stops (tests wait on it before signalling)


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


def kind_of(path, dir_fd=None):
    """'absent', 'dir', 'link' or 'other'. Anything else that stops the path being examined is raised, never taken
    for absence (GUARD 4)."""
    try:
        info = os.stat(path, dir_fd=dir_fd, follow_symlinks=False)
    except FileNotFoundError:
        return 'absent'
    return 'link' if stat.S_ISLNK(info.st_mode) else 'dir' if stat.S_ISDIR(info.st_mode) else 'other'


# ---- INVARIANT 4: places --------------------------------------------------------------------------

def _identity(path):
    info = os.stat(path)
    return info.st_dev, info.st_ino


def ancestry(path):
    """(device, inode) and name of the deepest existing ancestor of path and of every directory above it."""
    path = Path(os.path.abspath(path))
    while kind_of(path) == 'absent':
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
    """INVARIANT 4: not inside the real Library, not the real home or a folder holding it, not inside a checkout."""
    path = Path(os.path.abspath(path))
    home = real_home()
    if inside(path, home / 'Library'):
        raise Refusal(f'{what} is inside the real home Library: {path}')
    if kind_of(path) != 'absent' and inside(home, path):
        raise Refusal(f'{what} is or contains the real home: {path}')
    real = Path(os.path.realpath(path))
    if inside(path, REPOSITORY) or any(kind_of(p / '.git') != 'absent' for p in (real, *real.parents)):
        raise Refusal(f'{what} is inside a repository checkout: {path}')
    if any(LAUNCH_FOLDER_NAME.fullmatch(p.name) for p in (*path.parents, *real.parents)):
        raise Refusal(f'{what} is inside a launch folder (its home or control folder): {path}')
    return path


def open_directory(path, what):
    """INVARIANT 4 / RULE B: a handle on a directory reached from / with no link in any component."""
    path = Path(os.path.abspath(path))
    fd = os.open('/', DIRECTORY)
    try:
        for part in path.parts[1:]:
            try:
                child = os.open(part, DIRECTORY, dir_fd=fd)
            except OSError:
                raise Refusal(f'{what} must be an existing folder given by a path with no link in it '
                              f'(a link or something else stands where a folder should be, or it could not be opened): '
                              f'{path}') from None
            os.close(fd)
            fd = child
        return fd
    except BaseException:
        os.close(fd)
        raise


def under_applications(path):
    """INVARIANT 4: any ancestor named Applications, in any letter case, wherever it is."""
    names = [name for _, name in ancestry(path)] + list(Path(os.path.abspath(path)).parts)
    return any(name.lower() == 'applications' for name in names)


# ---- INVARIANT 6: only the identified candidate ---------------------------------------------------

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


# ---- INVARIANT 3: what is watched -----------------------------------------------------------------

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

    Returns (entries, links). Anything that cannot be examined raises (GUARD 4): absence is the only quiet case.
    """
    entries, links = {}, []
    base_kind = kind_of(base)
    if base_kind == 'link':
        return entries, ['.']
    if base_kind == 'absent':
        return entries, links
    if base_kind != 'dir':
        raise NotADirectoryError(f'not a folder: {base}')
    for folder in folders:
        where = Path(base) / folder if folder else Path(base)
        found = kind_of(where)
        if found == 'link':
            links.append(folder)
            continue
        if found != 'dir':
            continue  # absent, or a file where a watched folder could be: it holds no watched entry
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


# ---- INVARIANT 2: a clean run ---------------------------------------------------------------------

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
    """INVARIANT 2, the one place a run is judged. Nothing in the run folder or the home is read for it."""
    failures = []
    if not facts.get('started'):
        failures.append('the App was not started')
    else:
        if facts.get('returncode') != 0:
            failures.append('the App ' + facts['ended'])
        if facts['stops']:
            failures.append(f"a stop was accepted ({len(facts['stops'])}); the App did not end by itself")
        if facts.get('process_group') != 'gone':
            failures.append("a process of the App's process group was still running after the settle time")
        if facts.get('home_path') != 'unchanged':
            failures.append("the home's path changed during launch: detected after start and marked not clean")
    result = facts.get('comparison', {}).get('result', 'not made')
    if result != 'unchanged':
        failures.append({'not made': 'no complete comparison was made',
                         'incomplete': 'the comparison is incomplete: a link was met at or beneath a watched place',
                         'changed': 'the real Library changed in places named for the build'}[result])
    return ('clean' if not failures else 'failed'), failures


# ---- RULE D: observations that never gate ---------------------------------------------------------

def observe(base, folders, identifier, executable, what):
    """RULE D: an observation, never a refusal or a failure. Returns (entries, None) or (None, reason by category)."""
    if base is None:
        return None, f'not observed: there is no {what} on this system'
    try:
        if kind_of(base) == 'link':
            return None, f'not observed: the {what} is a link'
        entries, links = listing(base, folders, identifier, executable)
    except OSError as error:
        return None, f'not observed: the {what} or an entry in it could not be examined ({type(error).__name__})'
    if links:
        return None, f'incomplete: a link was met at or beneath an entry named for the build in the {what}'
    return entries, None


def preferences_observation():
    """RULE D: files directly under the real Library/Preferences, by name, kind, size and time. A link there is
    listed as an entry of kind link (its own size and time, not followed); only the folder itself being a link, or
    anything that cannot be examined, makes the observation not made."""
    folder = real_home() / 'Library/Preferences'
    try:
        found = kind_of(folder)
        if found == 'absent':
            return {}, None
        if found != 'dir':
            return None, 'not observed: the preference folder is a link or not a folder'
        with os.scandir(folder) as entries:
            infos = {e.name: e.stat(follow_symlinks=False) for e in entries}  # explicit: any error is raised
        return {name: _describe(info) for name, info in infos.items() if not stat.S_ISDIR(info.st_mode)}, None
    except OSError as error:
        return None, f'not observed: the preference folder could not be examined ({type(error).__name__})'


def disclosure(before, after, what, exclude=()):
    """RULE D: changes only when both observations were made; otherwise why not, and no changes at all."""
    if before[1] or after[1]:
        return {'observation': before[1] or after[1]}
    return {'observation': 'made', 'what': what,
            'changes': [c for c in differences(before[0], after[0]) if c['path'] not in exclude]}


# ---- RULE B: the helper's own files, reached by handle and read defensively -----------------------

def write_own(dir_fd, name, fmt, values):
    value = {'format': FORMATS[id(fmt)], **values}
    if set(value) != set(fmt):
        raise Refusal('internal: fields differ from the closed format')
    fd = os.open(name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=dir_fd)
    with os.fdopen(fd, 'w') as stream:
        stream.write(json.dumps(value) + '\n')


def replace_own(dir_fd, name, fmt, values):
    temporary = f'.{name}.{os.getpid()}.{secrets.token_hex(3)}'
    write_own(dir_fd, temporary, fmt, values)
    os.replace(temporary, name, src_dir_fd=dir_fd, dst_dir_fd=dir_fd)


def read_own(dir_fd, name, fmt, what):
    """RULE B: no link followed; a regular file with one link, owned by the user; the closed format exactly."""
    try:
        fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=dir_fd)
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
        raise Refusal(f"{what} is not in the helper's format") from None
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


# ---- INVARIANT 5: the launch folder, its home and control folder (RULES A and B) ------------------

class LaunchFolder:
    """Held, verified handles on a launch folder, its control folder and its home."""

    def __init__(self, path, folder_fd, control_fd, home_fd, kind):
        self.path, self.fd, self.control, self.home, self.kind = path, folder_fd, control_fd, home_fd, kind
        self.lock = None

    @property
    def home_path(self):
        return self.path / HOME

    def close(self):
        for fd in (self.lock, self.home, self.control, self.fd):
            if fd is not None:
                os.close(fd)


def _ident(fd):
    info = os.fstat(fd)
    return info.st_dev, info.st_ino


def make_folder(parent, kind):
    """A new launch folder with its control folder (marker, idle state, lock) and an empty home, made through held
    handles. RULE A: nothing in the home is read."""
    if kind not in KINDS:
        raise Refusal('internal: unknown home kind')
    parent_fd = open_directory(parent, 'the parent')
    try:
        name = f'launch-{kind}-{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}-{secrets.token_hex(4)}'
        path = check_place(Path(os.path.abspath(parent)) / name, 'launch folder')
        os.mkdir(name, 0o700, dir_fd=parent_fd)
        folder_fd = os.open(name, DIRECTORY, dir_fd=parent_fd)
    finally:
        os.close(parent_fd)
    os.mkdir(CONTROL, 0o700, dir_fd=folder_fd)
    control_fd = os.open(CONTROL, DIRECTORY, dir_fd=folder_fd)
    home_operation(path, lambda: os.mkdir(HOME, 0o700, dir_fd=folder_fd))
    home_fd = home_operation(path, lambda: os.open(HOME, DIRECTORY, dir_fd=folder_fd))
    ids = {'folder': _ident(folder_fd), 'home': _ident(home_fd), 'control': _ident(control_fd)}
    write_own(control_fd, MARKER, MARKER_FORMAT, {
        'path': str(path), 'kind': kind, **{f'{k}_device': v[0] for k, v in ids.items()},
        **{f'{k}_inode': v[1] for k, v in ids.items()}})
    write_own(control_fd, STATE, STATE_FORMAT, {'phase': 'idle', 'process_group': None})
    os.close(os.open(LOCK, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=control_fd))
    return LaunchFolder(path, folder_fd, control_fd, home_fd, kind)


def own_folder(path):
    """INVARIANT 5 / RULE B: a launch folder this helper made. The folder is reached with no link in its path; its
    control folder and home are opened from its handle without following links; the marker, read through the
    control handle, must record the identity of all three handles, a valid kind and this path, and the kind must
    agree with the folder's name. Nothing inside the home is opened."""
    given = Path(os.path.abspath(path))
    folder_fd = open_directory(given, 'the launch folder')
    handles = [folder_fd]
    try:
        check_place(given, 'launch folder')
        try:
            control_fd = os.open(CONTROL, DIRECTORY, dir_fd=folder_fd)
        except OSError:
            raise Refusal(f'not a launch folder made by this helper (its control folder is missing or a link): {given}') from None
        handles.append(control_fd)
        marker = read_own(control_fd, MARKER, MARKER_FORMAT, 'the launch folder marker')
        try:
            home_fd = os.open(HOME, DIRECTORY, dir_fd=folder_fd)
        except OSError:
            raise Refusal(f'not a launch folder made by this helper (its home is missing or a link): {given}') from None
        handles.append(home_fd)
        if marker['kind'] not in KINDS or marker['path'] != str(given) or any(
                _ident(fd) != (marker[f'{key}_device'], marker[f'{key}_inode'])
                for key, fd in (('folder', folder_fd), ('control', control_fd), ('home', home_fd))):
            raise Refusal(f'not a launch folder made by this helper (its recorded identity differs): {given}')
        if not given.name.startswith(f"launch-{marker['kind']}-"):
            raise Refusal(f"the launch folder's recorded kind does not agree with its name: {given}")
        return LaunchFolder(given, folder_fd, control_fd, home_fd, marker['kind'])
    except BaseException:
        for fd in handles:
            os.close(fd)
        raise


def lock(folder):
    """One invocation at a time per launch folder (released by the system if the holder dies, even killed)."""
    try:
        fd = os.open(LOCK, os.O_RDWR | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=folder.control)
    except OSError:
        raise Refusal("the launch folder's lock is missing or not the helper's own") from None
    info = os.fstat(fd)
    if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1 or info.st_uid != os.getuid():
        os.close(fd)
        raise Refusal("the launch folder's lock is not the helper's own plain file")
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        os.close(fd)
        raise Refusal('the launch folder is in use by another invocation of this helper') from None
    folder.lock = fd


def group_state(pgid):
    try:
        os.killpg(pgid, 0)
    except ProcessLookupError:
        return 'gone'
    except PermissionError:
        return 'still running'
    return 'still running'


def in_use(folder):
    """INVARIANT 5 custody, under the lock: a missing or invalid state refuses; an interrupted launch or a live member
    of the App's process group keeps the folder refused."""
    state = read_own(folder.control, STATE, STATE_FORMAT, 'the custody state')
    reasons = []
    if state['phase'] != 'idle':
        reasons.append('an interrupted launch (its helper ended without releasing the folder; remove it by hand)')
    if state['process_group'] is not None and group_state(state['process_group']) != 'gone':
        reasons.append(f"a member of the App's process group {state['process_group']}")
    return reasons


def claim(folder):
    lock(folder)
    reasons = in_use(folder)
    if reasons:
        raise Refusal('the launch folder is refused: ' + ' and '.join(reasons))
    replace_own(folder.control, STATE, STATE_FORMAT, {'phase': 'running', 'process_group': None})


def release(folder, group):
    """Custody outlives the launcher: a living group stays recorded and keeps the launch folder refused."""
    alive = group is not None and group_state(group) != 'gone'
    replace_own(folder.control, STATE, STATE_FORMAT, {'phase': 'idle', 'process_group': group if alive else None})


def delete_tree(folder):
    """RULE A, remove only: delete the launch folder through handles; entries without permission are opened up
    first. Errors name the launch folder only."""
    parent_fd = None
    try:
        os.fchmod(folder.fd, 0o700)
        for _, dirs, _, dir_fd in os.fwalk(dir_fd=folder.fd):
            for name in dirs:
                if stat.S_ISDIR(os.stat(name, dir_fd=dir_fd, follow_symlinks=False).st_mode):
                    os.chmod(name, 0o700, dir_fd=dir_fd)
        parent_fd = open_directory(folder.path.parent, 'the parent')
        if os.stat(folder.path.name, dir_fd=parent_fd, follow_symlinks=False).st_ino != _ident(folder.fd)[1]:
            raise Refusal(f'the launch folder {folder.path} changed before removal')
        shutil.rmtree(folder.path.name, dir_fd=parent_fd)
    except OSError as error:
        raise HomeError(f'could not remove all of the launch folder {folder.path} ({type(error).__name__}); '
                        'part of it may remain') from None
    finally:
        if parent_fd is not None:
            os.close(parent_fd)


# ---- INVARIANTS 1 and 7: the environment ----------------------------------------------------------

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


def child_environment(home, tmp, inputs, lang, kind, model_address=DEFAULT_MODEL_ADDRESS):
    """INVARIANTS 1 and 7: a new mapping from the allowlist alone; nothing is read from this process's environment."""
    env = {'HOME': str(home), 'CFFIXED_USER_HOME': str(home), 'TMPDIR': str(Path(home, tmp)),
           'PATH': SYSTEM_PATH, 'LANG': lang}
    env.update(inputs)
    if kind != 'owners-sitting':
        env.update({name: value for name, (value, _) in PROXY_OVERRIDES.items()})
        env[MODEL_ADDRESS] = model_address
    return env


def check_environment(env, home, tmp, kind):
    """INVARIANTS 1 and 7, immediately before the App starts: the allowlist exactly; both homes the throwaway home;
    TMPDIR this launch's fresh folder in it; the overrides present with their values unless the home is the owner's
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
    if env['TMPDIR'] != str(Path(home, tmp)):
        raise Refusal("TMPDIR is not this launch's fresh folder in the throwaway home; refusing to launch")
    if env['PATH'] != SYSTEM_PATH or not LOCALE.fullmatch(env['LANG']):
        raise Refusal('PATH or LANG differs from the allowlist')
    return env


def home_path_holds(folder):
    """The pathname given as HOME still resolves to the home the helper holds (a stat of the home, nothing in it)."""
    try:
        return _identity(folder.home_path) == _ident(folder.home)
    except OSError:
        return False


# ---- RULE C: stops --------------------------------------------------------------------------------

def process_start(pid):
    """The process's start time as ps reports it, or None; tells a process from a reused identifier."""
    result = subprocess.run(['ps', '-o', 'lstart=', '-p', str(pid)], capture_output=True, text=True)
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def answer_requests(folder, answer):
    """RULE C: answer every stop request in the control folder that has no answer yet; returns the requests answered."""
    answered = []
    names = set(os.listdir(folder.control))
    for name in sorted(names):
        nonce = name[len(REQUEST):-len('.json')] if name.startswith(REQUEST) and name.endswith('.json') else None
        if not nonce or not NONCE.fullmatch(nonce) or f'{ANSWER}{nonce}.json' in names:
            continue
        try:
            if read_own(folder.control, name, REQUEST_FORMAT, 'a stop request')['nonce'] != nonce:
                continue
            write_own(folder.control, f'{ANSWER}{nonce}.json', ANSWER_FORMAT, {'nonce': nonce, 'answer': answer})
            answered.append(nonce)
        except (Refusal, OSError):
            continue
    return answered


def stop(path, wait_seconds=10.0):
    """RULE C: ask a run's helper to stop the App. The helper is found through its own process file in the control
    folder, its start time checked, and signalled; never the App. The answer is the helper's."""
    folder = own_folder(path)
    try:
        process = read_own(folder.control, PROCESS, PROCESS_FORMAT, "the run's process file")
        helper = process['helper_pid']
        if process_start(helper) != process['helper_start']:
            raise Refusal('no running helper is recorded for this launch folder; nothing was signalled '
                          "(end the App with its own Quit, or by hand)")
        nonce = secrets.token_hex(8)
        write_own(folder.control, f'{REQUEST}{nonce}.json', REQUEST_FORMAT, {'nonce': nonce})
        os.kill(helper, signal.SIGTERM)
        deadline = time.monotonic() + wait_seconds
        while time.monotonic() < deadline:
            try:
                answer = read_own(folder.control, f'{ANSWER}{nonce}.json', ANSWER_FORMAT, 'the stop answer')
            except Refusal:
                time.sleep(0.05)
                continue
            if answer['nonce'] == nonce and answer['answer'] in (ACCEPTED, TOO_LATE):
                return {'signalled_helper': helper, 'answer': answer['answer']}
            break
        return {'signalled_helper': helper, 'answer': 'not accepted: the helper gave no answer (it may have ended)'}
    finally:
        folder.close()


# ---- the run --------------------------------------------------------------------------------------

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
    run_parent = open_directory(run.parent, 'the run folder\'s parent')
    try:
        if kind_of(run.name, dir_fd=run_parent) != 'absent':
            raise Refusal(f'the run folder already exists: {run}')
        if args.reuse:
            folder = own_folder(args.reuse)
            if args.owner_sitting and folder.kind != 'owners-sitting':
                folder.close()
                raise Refusal("--owner-sitting contradicts this launch folder's kind, fixed when it was made")
        else:
            folder = make_folder(args.parent, 'owners-sitting' if args.owner_sitting else 'not-owners-sitting')
        try:
            if folder.kind == 'owners-sitting' and args.model_address is not None:
                raise Refusal("--model-address is not given to an owner's-sitting launch")
            model_address = check_model_address(args.model_address or DEFAULT_MODEL_ADDRESS)
            os.mkdir(run.name, 0o700, dir_fd=run_parent)
            try:
                claim(folder)
            except BaseException:
                os.rmdir(run.name, dir_fd=run_parent)  # the empty run folder this call made
                raise
            run_fd = os.open(run.name, DIRECTORY, dir_fd=run_parent)
        except BaseException:
            folder.close()
            raise
    finally:
        os.close(run_parent)
    try:
        return _run(args, app, record_data, identifier, executable_path, executable, inputs, model_address,
                    folder, run, run_fd)
    finally:
        os.close(run_fd)
        folder.close()


def _run(args, app, record_data, identifier, executable_path, executable, inputs, model_address, folder, run, run_fd):
    home = folder.home_path
    tmp = f'.chirality-launch-tmp-{run.name}-{secrets.token_hex(4)}'
    record = {'note': NOTE, 'helper': {'path': TOOL, 'sha256': sha256_file(__file__)},
              'candidate_key': record_data['candidate_key'], 'identifier': identifier, 'bundle': str(app),
              'identification_record': str(Path(os.path.abspath(args.record))),
              'launch_folder': {'launch_folder': str(folder.path), 'state': 'reused' if args.reuse else 'created'},
              'home': str(home), 'home_kind': folder.kind,
              'watched': {'rule': 'name contains the identifier, equals the executable name, or is '
                                  'com.apple.WebKit.<Networking|WebContent|GPU>+<executable with _ for ->-<suffix>',
                          'identifier': identifier, 'executable': executable,
                          'places': ['Library', *('Library/' + w for w in WATCHED)]}}
    facts = {'started': False, 'stops': [], 'open': True, 'run': str(run)}
    proc, output = None, None
    cache = user_cache_dir()
    previous = {}

    def latch(signum, frame):  # RULE C: accepted (in memory, before forwarding) only before the boundary
        if not facts['open']:
            try:
                answer_requests(folder, TOO_LATE)
            except OSError:
                pass
            return
        entry = {'signal': signal.Signals(signum).name, 'at': now(), 'stop_requests_answered': []}
        facts['stops'].append(entry)  # in the record before anyone is told "accepted"
        if proc is not None and proc.poll() is None:
            try:
                proc.send_signal(signal.SIGTERM)
            except ProcessLookupError:
                pass
        try:
            entry['stop_requests_answered'] = answer_requests(folder, ACCEPTED)
        except OSError:
            pass
    try:
        for s in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):
            previous[s] = signal.signal(s, latch)
        for name in os.listdir(folder.control):  # the helper's own stale requests and answers
            if name.startswith((REQUEST, ANSWER)):
                os.unlink(name, dir_fd=folder.control)
        replace_own(folder.control, PROCESS, PROCESS_FORMAT, {
            'helper_pid': os.getpid(), 'helper_start': process_start(os.getpid()) or '', 'app_pid': None})
        _forwarding.set()
        home_operation(folder.path, lambda: os.mkdir(tmp, 0o700, dir_fd=folder.home))  # RULE A: a fresh folder
        env = child_environment(home, tmp, inputs, args.lang, folder.kind, model_address)
        record['environment'] = env
        record['overrides_passed'] = ({n: env[n] for n in (*PROXY_OVERRIDES, MODEL_ADDRESS) if n in env}
                                      or "none (an owner's-sitting launch)")
        try:
            before = listing(real_home() / 'Library', ('', *WATCHED), identifier, executable)
        except OSError as error:
            facts['ended'] = f'not launched: the before-listing could not be made ({type(error).__name__})'
            return _finish(folder, run_fd, record, facts, code=2, label='not launched')
        prefs_before = preferences_observation()
        cache_before = observe(cache, ('',), identifier, executable, 'per-user cache folder')
        try:  # immediately before the start: the mapping (INVARIANTS 1 and 7) and the home path's identity
            check_environment(env, home, tmp, folder.kind)
            if not home_path_holds(folder):
                raise Refusal('the home path no longer resolves to the home this helper holds')
        except Refusal as error:
            facts['ended'] = f'not launched: {error}'
            return _finish(folder, run_fd, record, facts, code=2, label='not launched')
        if facts['stops']:
            facts['ended'] = 'not launched: a stop was accepted before the App started'
            return _finish(folder, run_fd, record, facts, code=2, label='not launched')
        output_name = f'.chirality-launch-output-{run.name}-{secrets.token_hex(3)}.log'
        output = home_operation(folder.path, lambda: os.open(
            output_name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=folder.home))
        record['output'] = {'path': str(home / output_name), 'note': 'kept inside the throwaway home; never read'}
        record['started_at'] = now()
        try:  # the working directory is given by pathname (no pre-exec hook)
            proc = subprocess.Popen([str(app / executable_path)], env=env, cwd=home, stdin=subprocess.DEVNULL,
                                    stdout=output, stderr=output, start_new_session=True, close_fds=True)
        except OSError as error:
            facts['ended'] = f'did not start ({type(error).__name__})'
            return _finish(folder, run_fd, record, facts, code=1)
        facts['started'] = True
        record['pid'] = proc.pid
        if facts['stops']:
            proc.send_signal(signal.SIGTERM)
        replace_own(folder.control, STATE, STATE_FORMAT, {'phase': 'running', 'process_group': proc.pid})
        replace_own(folder.control, PROCESS, PROCESS_FORMAT, {
            'helper_pid': os.getpid(), 'helper_start': process_start(os.getpid()) or '', 'app_pid': proc.pid})
        held_at_start = home_path_holds(folder)  # detection only: by now the start has already happened
        print(json.dumps({'launched': proc.pid, 'run_folder': str(run), 'launch_folder': str(folder.path)}),
              file=sys.stderr, flush=True)
        facts['returncode'] = proc.wait()
        facts['ended'] = how_it_ended(facts['returncode'])
        record['ended_at'] = now()
        facts['home_path'] = 'unchanged' if held_at_start and home_path_holds(folder) else 'changed'
        time.sleep(args.settle_seconds)
        facts['process_group'] = record['process_group_after_settle'] = group_state(proc.pid)
        after = again = None
        try:
            after = listing(real_home() / 'Library', ('', *WATCHED), identifier, executable)
            time.sleep(args.settle_seconds)
            again = listing(real_home() / 'Library', ('', *WATCHED), identifier, executable)
        except OSError as error:
            record['after_listing'] = f'could not be made ({type(error).__name__})'
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
        return _finish(folder, run_fd, record, facts, code=None)
    finally:
        _forwarding.clear()
        if output is not None:
            os.close(output)
        if proc is not None and proc.poll() is None:
            print(json.dumps({'warning': f'the App (process {proc.pid}) is still running; no record says it ended'}),
                  file=sys.stderr)
        try:
            release(folder, proc.pid if proc is not None else None)
        finally:
            for s in previous:
                signal.signal(s, signal.SIG_IGN)  # no stop is accepted any more; a late stop gets no "accepted"
            try:
                answer_requests(folder, TOO_LATE)
            except OSError:
                pass
            for s, handler in previous.items():
                signal.signal(s, handler)


def write_record(run_fd, record):
    fd = os.open(RECORD, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=run_fd)
    with os.fdopen(fd, 'w') as stream:
        stream.write(json.dumps(record, indent=2) + '\n')


def _finish(folder, run_fd, record, facts, code, label=None):
    facts['open'] = False  # RULE C, the finalization boundary: no stop is accepted after this line
    result, failures = outcome(facts)
    record['ended'] = facts.get('ended')
    record.setdefault('started_at', None)
    record['real_library'] = facts.get('comparison', {'result': 'not made'})
    record['stops'] = list(facts['stops'])  # every stop accepted before the boundary
    record['home_path_during_launch'] = facts.get('home_path', 'not checked: the App did not start')
    record['failures'] = failures
    record['outcome'] = label or result
    write_record(run_fd, record)  # written once, after the comparison and the boundary
    print(json.dumps({'outcome': record['outcome'], 'record': facts['run'] + '/' + RECORD, 'failures': failures},
                     indent=2))
    return code if code is not None else (0 if result == 'clean' else 1)


def remove(path):
    """INVARIANT 5: remove a launch folder this helper made, by identity, under its lock, when nothing of a launch
    lives and its last launch was not interrupted."""
    folder = own_folder(path)
    try:
        lock(folder)
        reasons = in_use(folder)
        if reasons:
            raise Refusal('the launch folder is refused: ' + ' and '.join(reasons))
        delete_tree(folder)
        return {'removed': str(folder.path)}
    finally:
        folder.close()


def main(argv=None):
    parser = argparse.ArgumentParser(
        description=__doc__.splitlines()[0] + ' A controlled development launcher, not an isolation boundary.',
        epilog="A launch folder (launch-<kind>-<time>-<random>) holds the throwaway home (home/) and the helper's "
               'control folder (control/); --reuse, stop and remove take the launch folder. Paths to folders the helper '
               'writes, reuses or removes must contain no link. Exit status: 0 clean run (or stop accepted, or '
               'removed), 1 run made but not clean (or stop not accepted), 2 refused or not launched. What the helper '
               'guards, its edge and its limits are in the module docstring.')
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('launch', help='launch the identified bundle in a throwaway home and compare the real Library')
    p.add_argument('--app', required=True, help='the built development bundle (.app)')
    p.add_argument('--record', required=True, help="its candidate identification record; identification's check must pass")
    p.add_argument('--run-dir', required=True, help='new folder for the run record; outside any checkout and the real Library')
    where = p.add_mutually_exclusive_group(required=True)
    where.add_argument('--parent', help='existing folder in which a new launch folder (home/ and control/) is made')
    where.add_argument('--reuse', metavar='LAUNCH_FOLDER', help='a launch folder this helper made, for a later launch '
                       'of the same walk')
    p.add_argument('--owner-sitting', action='store_true',
                   help="make the new home the owner's sitting (passed no overrides); never the default; fixed when the "
                        'home is made; on --reuse only to confirm that kind')
    p.add_argument('--model-address', help=f'a loopback stub address for {MODEL_ADDRESS} (default {DEFAULT_MODEL_ADDRESS}); '
                   "http(s)://127.0.0.1 or [::1] only; never for an owner's sitting")
    p.add_argument('--app-env', action='append', metavar='NAME=VALUE',
                   help='an App startup input (repeatable; none by default; the value is recorded verbatim, never give a '
                        'credential): ' + ', '.join(APP_INPUTS))
    p.add_argument('--lang', default=DEFAULT_LANG, help='LANG for the App (default %(default)s; never inherited)')
    p.add_argument('--settle-seconds', type=float, default=5.0,
                   help='wait after the App exits before listing, and again before the second listing (default 5)')
    p = sub.add_parser('stop', help="ask a launch folder's running helper to stop the App (SIGTERM; the run is then "
                       'not clean); answered accepted or not accepted')
    p.add_argument('--launch-folder', required=True)
    p = sub.add_parser('remove', help='remove a launch folder this helper made, when no launch or App process lives')
    p.add_argument('--launch-folder', required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == 'launch':
            return launch(args)
        if args.command == 'stop':
            result = stop(args.launch_folder)
            print(json.dumps(result))
            return 0 if result['answer'] == ACCEPTED else 1
        print(json.dumps(remove(args.launch_folder)))
        return 0
    except (ValueError, KeyError, TypeError, AttributeError, OSError, ImportError, json.JSONDecodeError,
            plistlib.InvalidFileException, ExpatError, subprocess.CalledProcessError, tarfile.TarError,
            EOFError) as error:
        print(json.dumps({'error': f'{type(error).__name__}: {error}'}), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
