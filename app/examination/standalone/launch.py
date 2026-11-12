#!/usr/bin/env python3
"""Launch one identified development App build in a throwaway home (DEL-09-02 examination tooling).

This is a controlled development launcher, not an isolation boundary. It has
one command, launch: a first launch makes a new launch folder, and a reuse
launch opens one it made before.

What it guards, without exception:
1. The agent shell's environment does not enter the App through it. The App's
   environment is built from nothing. (What the App passes on to the supplier it
   starts is the App's own: it sets the supplier's home and removes credential
   names.)
2. Under a home it creates the home, a temporary folder per launch and an
   output file per launch, and reads and lists nothing there. What leaves a run
   is: for the real Library places named for the build and the per-user cache
   folder, the names and change labels of watched entries and their counts; for
   the preference folder, the names and change labels of the files directly in
   it that changed during the run, whatever their names; how the App ended; and
   the path of the output file. No content of any file.
3. A caller's mistake about folders or kinds is refused, not acted on: a path
   written ambiguously (not absolute, or with an empty, "." or ".." component,
   or a trailing slash), a path with a link in it, a path inside a launch folder
   (other than the launch folder named for reuse), a stale or interrupted launch
   folder, a folder that is not the helper's, a home of the other kind.
4. It never reports a clean run or an unchanged comparison that it did not
   establish: not when something is unreadable, missing or a link, not after a
   failed start or an interruption. A signal the helper received before it
   fixed the outcome makes the run not clean. If no record is written, there is
   no completed run.

The edge. A case is inside these guards if it can arise in the intended
workflow: an ordinary failure, an interruption (including the helper itself
being killed), two honest callers at once, a mistaken path, a home or launch
folder left over from another run. What is outside is a process of the same
user rearranging the helper's folders or forging its control files, at any
time, including between a check and a use; the intended workflow does not
contain one. Such a process can read any home on this account directly and
needs no helper to do it; protecting a kept home that holds the owner's
sign-in from other processes of this account is not this helper's and is not
claimed by it.

A launch folder's life. The helper makes a launch folder (launch-<kind>-<time>-
<random>, holding home/ and control/) on a first launch and opens it again on a
reuse launch; it never deletes one, because deleting is the one operation that
must walk a home. A launch folder whose home is not the owner's sitting is
removed by hand by the examination lane; one that is the owner's sitting only
on the owner's word. Removal by hand follows the project's rule that such a
folder is classified first (listed at its top level by name only), and nothing
is removed while an App started from it may still be running: a killed helper
does not end the App.

A run ends when the App quits through its own menu, or when the helper process
receives a signal (SIGINT, SIGTERM or SIGHUP), which it latches in memory before
forwarding SIGTERM to the App; such a run is not clean.

How the guards are held (each in one place below, marked INVARIANT or RULE):
- INVARIANT 1, the environment: child_environment() builds a new mapping from
  the written allowlist; check_environment() checks it immediately before the
  App starts.
- INVARIANT 2, a clean run: outcome() calls a run clean only when the App
  exited by itself with status 0, no signal was latched, no process of its
  group was left, the home's path was the same at the checks made (before the
  start and once after it), and the real Library places named for the build
  were listed whole before and twice after with no link met and nothing
  differing. Anything that could not be examined makes the comparison "not
  made". The record is written whole under its name or not at all.
- RULE D, observations: the per-user cache folder and the preference files are
  observed, never a gate; when an observation is not made whole it says why and
  gives no changes.
- INVARIANT 3, exact names: watched_name() and check_executable().
- INVARIANT 4, places: caller paths are checked as written (check_syntax) and by
  their ancestry alone (refuse_inside_a_launch_folder) before anything touches
  them, then opened component by component without following links, and judged
  by device and inode.
- INVARIANT 5 / RULE A, the home: created, and written to only through a held
  handle, never read.
- RULE B, the helper's own files: the marker and custody state in control/ are
  reached only through no-follow handles from the launch folder and must be
  regular, single-link, the user's, and in the helper's closed format; the lock
  there must be a regular single-link file of the user's, opened without
  following links and used only for the system's lock (its contents are never
  read). Anything else is a refusal. Nothing read is quoted.
- INVARIANT 6, the candidate: the bundle and its identification record are
  found at the fixed places of a candidate folder made by build_candidate.py;
  identification's own check must find the bundle equal to the record (it
  hashes the bundle twice, a few seconds). No value read from the record is
  quoted in an error.
- INVARIANT 7, the overrides: every launch that is not the owner's sitting is
  passed the address override and the proxy overrides, checked in the mapping
  immediately before launch; an owner's-sitting launch is passed neither. A
  home's kind is fixed when it is made (--owner-sitting, never the default), in
  the marker and the launch folder's name. Every inconsistency of kind the
  helper can see before it starts the App is refused.

Limits:
- The App's HOME is a pathname, which the helper cannot bind to an identity. It
  checks the path against the held home before the start and once after it; a
  swap made and undone between those checks is not seen, and a swap present at
  the check after the start has already reached the App.
- The working directory is given to the App by pathname (no pre-exec hook).
- The comparison sees names, kinds, sizes and modification times, not content.
- App startup input values are the caller's and are recorded verbatim; never
  give a credential as a value.
- A custody state naming a process group whose identifier was later reused,
  and an interrupted launch (its helper killed), leave the launch folder refused
  for reuse.
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
MARKER, STATE, LOCK = 'marker.json', 'state.json', 'lock'  # in control/
RECORD = 'launch-record.json'  # in the run folder
BUNDLE_FOLDER = ('target', 'debug', 'bundle', 'macos')  # in a candidate folder (build_candidate.py)
IDENTIFICATION = ('identification', 'candidate-identification.json')  # in a candidate folder (identify.py record)
INVENTORY = 'bundle-inventory.json'  # beside the identification record
SYSTEM_PATH = '/usr/bin:/bin:/usr/sbin:/sbin'
DEFAULT_LANG = 'en_US.UTF-8'
SETTLE_SECONDS = 5.0  # waited after the App exits before listing, and again before the second listing
DIRECTORY = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW

# INVARIANT 1: every name the App's environment can hold, with why it is there.
ALLOWED = {
    'HOME': 'the throwaway home, the home of the App and every process it starts',
    'CFFIXED_USER_HOME': "the same throwaway home for the system frameworks (web view data and caches), which HOME alone does not move",
    'TMPDIR': 'a temporary folder made fresh for this launch inside the throwaway home',
    'PATH': 'the fixed system path, so system tools are found and nothing of the caller is',
    'LANG': "the App's locale, fixed (en_US.UTF-8), never inherited",
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
# The address override: the App's development input for the supplier's model-request address. Omitted means this
# default, where nothing listens, so no stub is needed; an empty value is refused.
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
FORMATS = {id(MARKER_FORMAT): 'chirality-launch-marker/2', id(STATE_FORMAT): 'chirality-launch-state/2'}

_forwarding = threading.Event()  # set while the helper latches signals (tests wait on it before signalling)


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

def check_syntax(text, what):
    """INVARIANT 4: a caller's path as written, before any normalisation: absolute, no empty, "." or ".." component,
    no trailing slash. Returns its components; nothing is touched."""
    if not isinstance(text, str) or not text.startswith('/') or text == '/' or '\0' in text:
        raise Refusal(f'{what} must be an absolute path to a folder: {text!r}')
    parts = text.split('/')[1:]
    if any(part in ('', '.', '..') for part in parts):
        raise Refusal(f'{what} is written ambiguously (an empty, "." or ".." component, or a trailing slash): {text!r}')
    return Path(text)


def refuse_inside_a_launch_folder(path, what, allowed=None):
    """INVARIANT 4: decided by the path's ancestry as written alone, without touching the path: refuse a path inside
    a launch folder (any ancestor named in the helper's launch-folder form). `allowed` is the one launch folder a
    reuse names, which is itself not refused."""
    for ancestor in path.parents:
        if LAUNCH_FOLDER_NAME.fullmatch(ancestor.name):
            raise Refusal(f'{what} is inside a launch folder (its home or control folder): {path}')
    if LAUNCH_FOLDER_NAME.fullmatch(path.name) and path != allowed:
        raise Refusal(f'{what} is a launch folder: {path}')
    return path


def caller_path(text, what, allowed_launch_folder=False):
    """INVARIANT 4: syntax and ancestry first, before anything touches the path."""
    path = check_syntax(text, what)
    return refuse_inside_a_launch_folder(path, what, allowed=path if allowed_launch_folder else None)


def _identity(path):
    info = os.stat(path)
    return info.st_dev, info.st_ino


def ancestry(path):
    """(device, inode) and name of the deepest existing ancestor of path and of every directory above it."""
    path = Path(path)
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
    """INVARIANT 4, after the path was opened without links: not inside the real Library, not the real home or a
    folder holding it, not inside a checkout."""
    home = real_home()
    if inside(path, home / 'Library'):
        raise Refusal(f'{what} is inside the real home Library: {path}')
    if kind_of(path) != 'absent' and inside(home, path):
        raise Refusal(f'{what} is or contains the real home: {path}')
    if inside(path, REPOSITORY) or any(kind_of(p / '.git') != 'absent' for p in (path, *path.parents)):
        raise Refusal(f'{what} is inside a repository checkout: {path}')
    return path


def open_directory(path, what):
    """INVARIANT 4 / RULE B: a handle on a directory reached from / with no link in any component."""
    fd = os.open('/', DIRECTORY)
    try:
        for part in Path(path).parts[1:]:
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


def open_within(fd, names, what):
    """A handle on a folder reached from fd through names, without following any link."""
    held = os.dup(fd)
    try:
        for name in names:
            try:
                child = os.open(name, DIRECTORY, dir_fd=held)
            except OSError:
                raise Refusal(f'{what} is missing, or a link stands in its path') from None
            os.close(held)
            held = child
        return held
    except BaseException:
        os.close(held)
        raise


def regular_file(dir_fd, name, what):
    """A regular single-link file of the user's, examined without following a link (its contents are not read)."""
    try:
        info = os.stat(name, dir_fd=dir_fd, follow_symlinks=False)
    except OSError:
        raise Refusal(f'{what} is missing or could not be examined') from None
    if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1 or info.st_uid != os.getuid():
        raise Refusal(f'{what} is not a plain file of this user (a link, a folder or a shared file)')


def under_applications(path):
    """INVARIANT 4: any ancestor named Applications, in any letter case."""
    return any(name.lower() == 'applications' for name in Path(path).parts)


# ---- INVARIANT 6: only the identified candidate ---------------------------------------------------

def find_candidate(text):
    """INVARIANT 6: the bundle and its identification record at the fixed places of a candidate folder made by
    build_candidate.py, reached without following any link."""
    root = caller_path(text, 'the candidate folder')
    if under_applications(root):
        raise Refusal('a candidate under an Applications folder is not launched: ' + str(root))
    root_fd = open_directory(root, 'the candidate folder')
    try:
        check_place(root, 'the candidate folder')
        macos = open_within(root_fd, BUNDLE_FOLDER, "the candidate's bundle folder (target/debug/bundle/macos)")
        try:
            bundles = [n for n in os.listdir(macos) if n.endswith('.app')]
            if len(bundles) != 1 or len(os.listdir(macos)) != 1:
                raise Refusal("the candidate's bundle folder does not hold exactly one bundle")
            os.close(open_within(macos, [bundles[0]], 'the bundle'))
        finally:
            os.close(macos)
        identification = open_within(root_fd, IDENTIFICATION[:1], "the candidate's identification folder")
        try:
            regular_file(identification, IDENTIFICATION[1], 'the identification record')
            regular_file(identification, INVENTORY, 'the stored bundle inventory')
        finally:
            os.close(identification)
    finally:
        os.close(root_fd)
    return root.joinpath(*BUNDLE_FOLDER, bundles[0]), root.joinpath(*IDENTIFICATION)


def identify_candidate(app, record_path):
    """INVARIANT 6: the record is valid and identification's own check finds the bundle equal to it. Errors name
    the kind of failure only, never a value read from the record."""
    try:
        record = json.loads(Path(record_path).read_bytes())
        if not isinstance(record, dict) or not record.get('candidate_key'):
            raise Refusal('the identification record has no candidate key')
        identify.validate_record(record)
        result = identify.check(argparse.Namespace(record=str(record_path), app=str(app)))
    except Refusal:
        raise
    except (ValueError, KeyError, TypeError, AttributeError, json.JSONDecodeError, plistlib.InvalidFileException,
            ExpatError, tarfile.TarError, EOFError) as error:
        raise Refusal(f"the identification record or bundle did not pass identification's validation and check "
                      f'({type(error).__name__})') from None
    if not (result['equal'] and result['build_identity'] == result['recorded_build_identity']
            and not result.get('record_fields_mismatched')):
        counts = {k: len(result.get(k, [])) for k in ('changed', 'missing', 'extra')}
        fields = sorted(f for f in result.get('record_fields_mismatched', []) if re.fullmatch(r'[a-z_.]+', f))
        raise Refusal('the bundle differs from its identification record '
                      f"({counts['changed']} changed, {counts['missing']} missing, {counts['extra']} extra entries"
                      + (f"; fields: {', '.join(fields)}" if fields else '') + ')')
    return record


# ---- INVARIANT 3: what is watched -----------------------------------------------------------------

def check_executable(executable):
    """INVARIANT 3: an executable name that does not discriminate is refused before launch."""
    if not isinstance(executable, str) or not EXECUTABLE_RULE.fullmatch(executable.lower()):
        raise Refusal(f'the executable name does not discriminate (it must match {EXECUTABLE_RULE.pattern}, '
                      'as chirality-app-v4 does)')


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
        raise NotADirectoryError('not a folder')
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
        if facts['signals']:
            failures.append(f"the helper received a signal ({len(facts['signals'])}); the App did not end by itself")
        if facts.get('process_group') != 'gone':
            failures.append("a process of the App's process group was still running after the settle time")
        if facts.get('home_path') != 'the same at the checks made (before the start and once after it)':
            failures.append("the home's path was not the same at the checks made (before the start and once after it)")
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
        stream.flush()
        os.fsync(stream.fileno())


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
        check_place(parent, 'the parent')
        name = f'launch-{kind}-{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}-{secrets.token_hex(4)}'
        path = parent / name
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
    folder_fd = open_directory(path, 'the launch folder')
    handles = [folder_fd]
    try:
        check_place(path, 'launch folder')
        try:
            control_fd = os.open(CONTROL, DIRECTORY, dir_fd=folder_fd)
        except OSError:
            raise Refusal(f'not a launch folder made by this helper (its control folder is missing or a link): {path}') from None
        handles.append(control_fd)
        marker = read_own(control_fd, MARKER, MARKER_FORMAT, 'the launch folder marker')
        try:
            home_fd = os.open(HOME, DIRECTORY, dir_fd=folder_fd)
        except OSError:
            raise Refusal(f'not a launch folder made by this helper (its home is missing or a link): {path}') from None
        handles.append(home_fd)
        if marker['kind'] not in KINDS or marker['path'] != str(path) or any(
                _ident(fd) != (marker[f'{key}_device'], marker[f'{key}_inode'])
                for key, fd in (('folder', folder_fd), ('control', control_fd), ('home', home_fd))):
            raise Refusal(f'not a launch folder made by this helper (its recorded identity differs): {path}')
        if not path.name.startswith(f"launch-{marker['kind']}-"):
            raise Refusal(f"the launch folder's recorded kind does not agree with its name: {path}")
        return LaunchFolder(path, folder_fd, control_fd, home_fd, marker['kind'])
    except BaseException:
        for fd in handles:
            os.close(fd)
        raise


def lock(folder):
    """One invocation at a time per launch folder. The lock is a regular single-link file of the user's, opened
    without following links and used only for the system's lock, which the system releases if the holder dies."""
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
        reasons.append('an interrupted launch (its helper ended without releasing the folder)')
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
    """INVARIANT 7: a loopback address only, by the helper's own rule (localhost, empty and blank are refused)."""
    match = MODEL_ADDRESS_RULE.fullmatch(value) if isinstance(value, str) and len(value) <= 2048 else None
    if not match or (match.group(1) and not 1 <= int(match.group(1)) <= 65535):
        raise Refusal(f'{MODEL_ADDRESS} must be http(s)://127.0.0.1 or [::1], an optional port 1-65535 and a plain path')
    return value


def address_for(kind, given):
    """INVARIANT 7: omitted means the default (nothing listens there); an owner's sitting takes none, not even an
    empty one; anything given is checked by the rule (empty and blank are refused)."""
    if kind == 'owners-sitting':
        if given is not None:
            raise Refusal("--model-address is not given to an owner's-sitting launch")
        return None
    return DEFAULT_MODEL_ADDRESS if given is None else check_model_address(given)


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
    if env['PATH'] != SYSTEM_PATH or env['LANG'] != DEFAULT_LANG:
        raise Refusal('PATH or LANG differs from the allowlist')
    return env


def home_path_holds(folder):
    """The pathname given as HOME resolves to the home the helper holds (a stat of the home, nothing in it)."""
    try:
        return _identity(folder.home_path) == _ident(folder.home)
    except OSError:
        return False


# ---- the run --------------------------------------------------------------------------------------

def how_it_ended(returncode):
    if returncode < 0:
        try:
            return f'ended by signal {-returncode} ({signal.Signals(-returncode).name})'
        except ValueError:
            return f'ended by signal {-returncode}'
    return f'exited with status {returncode}'


def launch(args):
    # INVARIANT 4: every caller path is checked as written and by its ancestry before anything touches it.
    run = caller_path(args.run_dir, 'the run folder')
    parent = caller_path(args.parent, 'the parent') if args.parent is not None else None
    reuse = caller_path(args.reuse, 'the launch folder', allowed_launch_folder=True) if args.reuse is not None else None
    if reuse is not None and not LAUNCH_FOLDER_NAME.fullmatch(reuse.name):
        raise Refusal(f'not a launch folder made by this helper (its name is not in the launch-folder form): {reuse}')
    inputs = app_inputs(args.app_env)
    if reuse is None:  # the kind is known now: decide the address before anything is made
        model_address = address_for('owners-sitting' if args.owner_sitting else 'not-owners-sitting', args.model_address)
    app, record_path = find_candidate(args.candidate)
    record_data = identify_candidate(app, record_path)
    identifier = record_data['bundle']['identifier']
    executable_path = record_data['bundle']['executable']['path']
    executable = executable_path.rsplit('/', 1)[-1]
    check_executable(executable)
    run_parent = open_directory(run.parent, "the run folder's parent")
    try:
        check_place(run, 'the run folder')
        if kind_of(run.name, dir_fd=run_parent) != 'absent':
            raise Refusal(f'the run folder already exists: {run}')
        if reuse is not None:
            folder = own_folder(reuse)
            if args.owner_sitting and folder.kind != 'owners-sitting':
                folder.close()
                raise Refusal("--owner-sitting contradicts this launch folder's kind, fixed when it was made")
            try:
                model_address = address_for(folder.kind, args.model_address)
            except Refusal:
                folder.close()
                raise
        else:
            folder = make_folder(parent, 'owners-sitting' if args.owner_sitting else 'not-owners-sitting')
        try:
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
              'candidate_folder': args.candidate,
              'launch_folder': {'launch_folder': str(folder.path), 'state': 'reused' if args.reuse else 'created'},
              'home': str(home), 'home_kind': folder.kind,
              'watched': {'rule': 'name contains the identifier, equals the executable name, or is '
                                  'com.apple.WebKit.<Networking|WebContent|GPU>+<executable with _ for ->-<suffix>',
                          'identifier': identifier, 'executable': executable,
                          'places': ['Library', *('Library/' + w for w in WATCHED)]}}
    facts = {'started': False, 'signals': [], 'open': True, 'run': str(run)}
    proc, output = None, None
    cache = user_cache_dir()
    previous = {}

    def latch(signum, frame):  # a signal received before the outcome is fixed: kept in memory, then forwarded
        if not facts['open']:
            return
        facts['signals'].append({'signal': signal.Signals(signum).name, 'at': now()})
        if proc is not None and proc.poll() is None:
            try:
                proc.send_signal(signal.SIGTERM)
            except ProcessLookupError:
                pass
    try:
        for s in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):
            previous[s] = signal.signal(s, latch)
        _forwarding.set()
        home_operation(folder.path, lambda: os.mkdir(tmp, 0o700, dir_fd=folder.home))  # RULE A: a fresh folder
        env = child_environment(home, tmp, inputs, DEFAULT_LANG, folder.kind, model_address)
        record['environment'] = env
        record['overrides_passed'] = ({n: env[n] for n in (*PROXY_OVERRIDES, MODEL_ADDRESS) if n in env}
                                      or "none (an owner's-sitting launch)")
        record['address_override'] = ("none (an owner's-sitting launch)" if folder.kind == 'owners-sitting' else
                                      'the default (nothing listens there)' if args.model_address is None
                                      else 'given by the caller')
        try:
            before = listing(real_home() / 'Library', ('', *WATCHED), identifier, executable)
        except OSError as error:
            facts['ended'] = f'not launched: the before-listing could not be made ({type(error).__name__})'
            return _finish(run_fd, record, facts, code=2, label='not launched')
        prefs_before = preferences_observation()
        cache_before = observe(cache, ('',), identifier, executable, 'per-user cache folder')
        try:  # immediately before the start: the mapping (INVARIANTS 1 and 7) and the home path's identity
            check_environment(env, home, tmp, folder.kind)
            if not home_path_holds(folder):
                raise Refusal('the home path does not resolve to the home this helper holds')
        except Refusal as error:
            facts['ended'] = f'not launched: {error}'
            return _finish(run_fd, record, facts, code=2, label='not launched')
        if facts['signals']:
            facts['ended'] = 'not launched: the helper received a signal before the App started'
            return _finish(run_fd, record, facts, code=2, label='not launched')
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
            return _finish(run_fd, record, facts, code=1)
        facts['started'] = True
        record['pid'] = proc.pid
        if facts['signals']:
            proc.send_signal(signal.SIGTERM)
        replace_own(folder.control, STATE, STATE_FORMAT, {'phase': 'running', 'process_group': proc.pid})
        same_after_start = home_path_holds(folder)  # the one check after the start; the start has already happened
        print(json.dumps({'launched': proc.pid, 'run_folder': str(run), 'launch_folder': str(folder.path)}),
              file=sys.stderr, flush=True)
        facts['returncode'] = proc.wait()
        facts['ended'] = how_it_ended(facts['returncode'])
        record['ended_at'] = now()
        facts['home_path'] = ('the same at the checks made (before the start and once after it)' if same_after_start
                              else 'not the same at the check made once after the start')
        time.sleep(SETTLE_SECONDS)
        facts['process_group'] = record['process_group_after_settle'] = group_state(proc.pid)
        after = again = None
        try:
            after = listing(real_home() / 'Library', ('', *WATCHED), identifier, executable)
            time.sleep(SETTLE_SECONDS)
            again = listing(real_home() / 'Library', ('', *WATCHED), identifier, executable)
        except OSError as error:
            record['after_listing'] = f'could not be made ({type(error).__name__})'
        prefs_after = preferences_observation()
        cache_after = observe(cache, ('',), identifier, executable, 'per-user cache folder')
        facts['comparison'] = compare(before, after, again)
        named = {p.split('/', 1)[1] for p in before[0].keys() | (after or ({}, []))[0].keys() if p.startswith('Preferences/')}
        record['disclosed'] = {
            'note': "changed during the run by the operating system's own services or anything else running; "
                    'names and change labels only; not opened, edited or removed; never a failure',
            'preferences': disclosure(prefs_before, prefs_after, 'files directly under the real Library/Preferences', named),
            'user_cache': {'folder': str(cache) if cache else None,
                           **disclosure(cache_before, cache_after, 'entries named for the build')}}
        return _finish(run_fd, record, facts, code=None)
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
            for s, handler in previous.items():
                signal.signal(s, handler)


def write_record(run_fd, record):
    """The record exists whole under its name or not at all: written to a temporary name in the run folder,
    flushed, then linked to its name (never over an existing one). A temporary file left by an interruption has
    another name and is not the record."""
    temporary = f'.{RECORD}.partial-{secrets.token_hex(4)}'
    fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=run_fd)
    with os.fdopen(fd, 'w') as stream:
        stream.write(json.dumps(record, indent=2) + '\n')
        stream.flush()
        os.fsync(stream.fileno())
    os.link(temporary, RECORD, src_dir_fd=run_fd, dst_dir_fd=run_fd, follow_symlinks=False)
    os.unlink(temporary, dir_fd=run_fd)


def _finish(run_fd, record, facts, code, label=None):
    facts['open'] = False  # the outcome is fixed from here: a later signal changes nothing in the record
    result, failures = outcome(facts)
    record['ended'] = facts.get('ended')
    record.setdefault('started_at', None)
    record['real_library'] = facts.get('comparison', {'result': 'not made'})
    record['signals_received'] = list(facts['signals'])
    record['home_path_during_launch'] = facts.get('home_path', 'not checked: the App did not start')
    record['failures'] = failures
    record['outcome'] = label or result
    write_record(run_fd, record)
    print(json.dumps({'outcome': record['outcome'], 'record': facts['run'] + '/' + RECORD, 'failures': failures},
                     indent=2))
    return code if code is not None else (0 if result == 'clean' else 1)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description=__doc__.splitlines()[0] + ' A controlled development launcher, not an isolation boundary.',
        epilog="A launch folder (launch-<kind>-<time>-<random>) holds the throwaway home (home/) and the helper's "
               'control folder (control/). The helper never deletes one; see the module docstring. Every path must be '
               'absolute, written plainly (no empty, "." or ".." component, no trailing slash) and contain no link. '
               'A run ends when the App quits through its own menu, or when the helper receives SIGINT, SIGTERM or '
               'SIGHUP (the run is then not clean). Exit status: 0 clean run, 1 run made but not clean, 2 refused or '
               'not launched. What the helper guards, its edge and its limits are in the module docstring.')
    parser.add_argument('command', choices=['launch'])
    parser.add_argument('--candidate', required=True,
                        help='the candidate folder made by build_candidate.py: the bundle is read from '
                             'target/debug/bundle/macos and its identification record from '
                             "identification/candidate-identification.json; identification's check must pass")
    parser.add_argument('--run-dir', required=True, help='new folder for the run record; outside any checkout, '
                        'launch folder and the real Library')
    where = parser.add_mutually_exclusive_group(required=True)
    where.add_argument('--parent', help='existing folder in which a new launch folder (home/ and control/) is made')
    where.add_argument('--reuse', metavar='LAUNCH_FOLDER', help='a launch folder this helper made, for a later launch '
                       'of the same walk')
    parser.add_argument('--owner-sitting', action='store_true',
                        help="make the new home the owner's sitting (passed no overrides); never the default; fixed "
                             'when the home is made; on --reuse only to confirm that kind')
    parser.add_argument('--model-address', help=f'a loopback stub address for {MODEL_ADDRESS}; omitted means the default '
                        f'{DEFAULT_MODEL_ADDRESS} (nothing listens there); empty is refused; http(s)://127.0.0.1 or '
                        "[::1] only; never for an owner's sitting")
    parser.add_argument('--app-env', action='append', metavar='NAME=VALUE',
                        help='an App startup input (repeatable; none by default; the value is recorded verbatim, never '
                             'give a credential): ' + ', '.join(APP_INPUTS))
    args = parser.parse_args(argv)
    try:
        return launch(args)
    except (ValueError, KeyError, TypeError, AttributeError, OSError, ImportError, json.JSONDecodeError,
            plistlib.InvalidFileException, ExpatError, subprocess.CalledProcessError, tarfile.TarError,
            EOFError) as error:
        print(json.dumps({'error': f'{type(error).__name__}: {error}'}), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
