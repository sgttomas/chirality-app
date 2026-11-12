#!/usr/bin/env python3
"""Launch one identified development App build, once, in a new throwaway home (DEL-09-02 examination tooling).

A controlled development launcher for first launches on new throwaway homes
that never hold a sign-in. It is not an isolation boundary. Each run creates a
launch folder and its home, launches the App once, and does nothing more with
them; it cannot relaunch a home.

What the launcher states, and nothing more:
1. The App's environment is built from nothing: HOME and CFFIXED_USER_HOME
   (equal, the new home), TMPDIR inside it, the fixed PATH, the fixed LANG,
   and the nine overrides (the eight proxy names and
   CHIRALITY_DEV_OPENAI_BASE_URL). The exact mapping is checked against this
   list immediately before the start (child_environment, check_environment).
2. A run's record is whole or absent (write_record), and the record never says
   clean on what was not established: clean means the App started and exited
   by itself with status 0, nothing of its process group was left, both
   after-listings were made and equal to the before-listing, and no signal was
   received before the outcome was fixed (outcome, compare).
3. The real Library's places named for the build are compared before and after
   the run, by names, kinds, sizes and modification times (listing, compare).

What it also does, each with its limit:
- It checks the bundle against its identification record with identification's
  own check before the launch (identify_candidate). The check hashes the bundle
  twice, a few seconds for a real build. Its errors name the kind of failure,
  counts and field names, not values read from the record.
- It refuses a listed, not exhaustive, set of mistakes in the paths it is given
  (check_syntax, refuse_launch_folder_ancestry, open_directory, check_place): a
  path that is not absolute or has an empty, "." or ".." component or a
  trailing slash, refused as written before any normalisation; a path whose
  written ancestry names a launch folder; a link anywhere in the access path; a
  place in the real Library, the real home itself or a folder holding it, or a
  checkout; a run folder that already exists. Limit: a path that reaches a
  launch folder by another spelling of its name (a different letter case on a
  volume that ignores case, another Unicode form) is not detected.
- The home the App is launched into is one it has just created: the launch
  folder and home/ within it are each made by an exclusive create, which fails
  if anything already exists there under any spelling the volume treats as the
  same, and nothing is ever reused (make_folder). A caller's mistake may put a
  new launch folder inside another throwaway home; the App is still launched
  only into the new home. Limit: HOME is passed to the App as a pathname, and
  the helper does not re-check it after the create.
- Under the new home it creates a temporary folder and an output file for the
  App's output, through a held handle, and reads nothing there.
- It records what the record-field table in the pull request lists: the
  comparison's names and change labels and counts, the per-user cache folder
  and preference-folder observations (names and change labels; they never
  refuse a launch or fail a run), how the App ended, and the output file's
  path. No content of any file.
- The address override (CHIRALITY_DEV_OPENAI_BASE_URL) replaces the built-in
  provider's address for model requests only, once the App reads that input
  (it arrives with the Access lane's change, not yet on main; of a candidate
  built before it, nothing is said). The proxy overrides obstruct some of the
  supplier's other clients under their defaults. Neither establishes where a
  launch's requests went. The helper reads no system managed configuration.

Limits: the comparison sees names, kinds, sizes and modification times, not
content; the App's working directory is given by pathname; the helper does not
confine the App, sends it no input and does not look at its window; it deletes
nothing (a launch folder is removed by hand, after the App started from it has
ended: a killed helper does not end the App).
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
import identify  # noqa: E402  (identification's record validation and check)

TOOL = 'app/examination/standalone/launch.py'
NOTE = ('Evidence for a journey step record, written by ' + TOOL + '; not an examination record format, '
        'and nothing validates it.')
HOME = 'home'  # the one entry of a launch folder
RECORD = 'launch-record.json'  # in the run folder
BUNDLE_FOLDER = ('target', 'debug', 'bundle', 'macos')  # in a candidate folder (build_candidate.py)
IDENTIFICATION = ('identification', 'candidate-identification.json')  # in a candidate folder (identify.py record)
INVENTORY = 'bundle-inventory.json'  # beside the identification record
SYSTEM_PATH = '/usr/bin:/bin:/usr/sbin:/sbin'
LANG = 'en_US.UTF-8'
SETTLE_SECONDS = 5.0  # waited after the App exits before listing, and again before the second listing
DIRECTORY = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
LAUNCH_FOLDER_NAME = re.compile(r'launch-[0-9]{8}T[0-9]{6}Z-[0-9a-f]{8}')

# STATEMENT 1: the proxy overrides every launch is passed: name -> (value, why). All eight: the supplier has a
# websocket client (reads HTTPS, then HTTP, then ALL, upper case first) and an HTTP client (HTTPS for secure, HTTP for
# plain destinations, ALL as fallback); a name left unset could be the one read.
_PROXY = ('http://127.0.0.1:9', 'scheme http because the websocket client rejects an https proxy; port 9 is this '
          "repository's address where no server runs, so a connection is refused at once")
_EXEMPT = ('127.0.0.1,localhost,::1', 'loopback exempted without ports, brackets or spaces (the HTTP client does not '
           'understand ports and takes a bracketed entry as a name), with localhost because neither client resolves '
           'a name before comparing')
PROXY_OVERRIDES = {**{name: _PROXY for name in ('HTTPS_PROXY', 'https_proxy', 'HTTP_PROXY', 'http_proxy',
                                                'ALL_PROXY', 'all_proxy')},
                   'NO_PROXY': _EXEMPT, 'no_proxy': _EXEMPT}
# The address override: the App's development input for the supplier's model-request address. Omitted means this
# default, where nothing listens, so no stub is needed; an empty or blank value is refused.
MODEL_ADDRESS = 'CHIRALITY_DEV_OPENAI_BASE_URL'
DEFAULT_MODEL_ADDRESS = 'http://127.0.0.1:9/v1'
MODEL_ADDRESS_RULE = re.compile(r'https?://(?:127\.0\.0\.1|\[::1\])(?::([1-9][0-9]{0,4}))?(?:/[A-Za-z0-9._~/-]*)?')
# STATEMENT 1: every name the App's environment holds, with why it is there.
ALLOWED = {
    'HOME': 'the new throwaway home, the home of the App and every process it starts',
    'CFFIXED_USER_HOME': "the same home for the system frameworks (web view data and caches), which HOME alone does not move",
    'TMPDIR': 'a temporary folder made for this launch inside the new home',
    'PATH': 'the fixed system path, so system tools are found and nothing of the caller is',
    'LANG': "the App's locale, fixed (en_US.UTF-8), never inherited",
    **{name: why for name, (_, why) in PROXY_OVERRIDES.items()},
    MODEL_ADDRESS: 'the address override; the default where nothing listens, or a loopback stub the caller names',
}

# STATEMENT 3: the Library folders searched, beside the Library's own first level. Protected folders (Containers,
# Group Containers, Mail, Safari and the like) are not listed: reading them can be refused or raise a privacy prompt.
WATCHED = ('Application Support', 'Caches', 'WebKit', 'HTTPStorages', 'Preferences', 'Saved Application State',
           'Logs', 'Cookies', 'Application Scripts', 'Autosave Information', 'LaunchAgents')
EXECUTABLE_RULE = re.compile(r'chirality-[a-z0-9][a-z0-9_-]{2,}')  # e.g. chirality-app-v4

_forwarding = threading.Event()  # set while the helper latches signals (tests wait on it before signalling)


class Refusal(ValueError):
    """A refusal whose message is the helper's own words, never content read from a file."""


def real_home():
    """The real home, from the account database, never from HOME; the one place tests point elsewhere."""
    return Path(os.path.realpath(pwd.getpwuid(os.getuid()).pw_dir))


def user_cache_dir():
    """The per-user cache folder as getconf DARWIN_USER_CACHE_DIR reports it, not resolved; None if none."""
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
    for absence."""
    try:
        info = os.stat(path, dir_fd=dir_fd, follow_symlinks=False)
    except FileNotFoundError:
        return 'absent'
    return 'link' if stat.S_ISLNK(info.st_mode) else 'dir' if stat.S_ISDIR(info.st_mode) else 'other'


# ---- the listed path checks (not exhaustive) ----------------------------------------------------------

def check_syntax(text, what):
    """A caller's path as written, before any normalisation: absolute, no empty, "." or ".." component, no trailing
    slash. Nothing is touched."""
    if not isinstance(text, str) or not text.startswith('/') or text == '/' or '\0' in text:
        raise Refusal(f'{what} must be an absolute path to a folder: {text!r}')
    if any(part in ('', '.', '..') for part in text.split('/')[1:]):
        raise Refusal(f'{what} is written ambiguously (an empty, "." or ".." component, or a trailing slash): {text!r}')
    return Path(text)


def refuse_launch_folder_ancestry(path, what):
    """Refuse a path whose written ancestry, or own name, names a launch folder, as written (another spelling of the
    name is not detected). Nothing is touched."""
    if any(LAUNCH_FOLDER_NAME.fullmatch(p.name) for p in (path, *path.parents)):
        raise Refusal(f'{what} names a launch folder in its path: {path}')
    return path


def caller_path(text, what):
    return refuse_launch_folder_ancestry(check_syntax(text, what), what)


def _identity(path):
    info = os.stat(path)
    return info.st_dev, info.st_ino


def inside(path, place):
    """path is place or lies inside it, judged by device and inode."""
    try:
        target = _identity(place)
    except FileNotFoundError:
        return False
    path = Path(path)
    while kind_of(path) == 'absent':
        path = path.parent
    real = Path(os.path.realpath(path))
    return target in {_identity(p) for p in (real, *real.parents)}


def check_place(path, what):
    """Not inside the real Library, not the real home or a folder holding it, not inside a checkout."""
    home = real_home()
    if inside(path, home / 'Library'):
        raise Refusal(f'{what} is inside the real home Library: {path}')
    if kind_of(path) != 'absent' and inside(home, path):
        raise Refusal(f'{what} is or contains the real home: {path}')
    if inside(path, REPOSITORY) or any(kind_of(p / '.git') != 'absent' for p in (path, *path.parents)):
        raise Refusal(f'{what} is inside a repository checkout: {path}')
    return path


def open_directory(path, what):
    """A handle on a directory reached from / with no link in any component."""
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
    return any(name.lower() == 'applications' for name in Path(path).parts)


# ---- the candidate ------------------------------------------------------------------------------------

def find_candidate(text):
    """The bundle and its identification record at the fixed places of a candidate folder made by
    build_candidate.py, reached without following any link."""
    root = caller_path(text, 'the candidate folder')
    if under_applications(root):
        raise Refusal('a candidate under an Applications folder is not launched: ' + str(root))
    root_fd = open_directory(root, 'the candidate folder')
    try:
        check_place(root, 'the candidate folder')
        macos = open_within(root_fd, BUNDLE_FOLDER, "the candidate's bundle folder (target/debug/bundle/macos)")
        try:
            entries = os.listdir(macos)
            if len(entries) != 1 or not entries[0].endswith('.app'):
                raise Refusal("the candidate's bundle folder does not hold exactly one bundle")
            os.close(open_within(macos, entries, 'the bundle'))
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
    return root.joinpath(*BUNDLE_FOLDER, entries[0]), root.joinpath(*IDENTIFICATION)


def identify_candidate(app, record_path):
    """The record is valid and identification's own check finds the bundle equal to it. Errors name the kind of
    failure, counts and field names, never a value read from the record."""
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


# ---- STATEMENT 3: the comparison ----------------------------------------------------------------------

def check_executable(executable):
    """An executable name that does not discriminate is refused before launch."""
    if not isinstance(executable, str) or not EXECUTABLE_RULE.fullmatch(executable.lower()):
        raise Refusal(f'the executable name does not discriminate (it must match {EXECUTABLE_RULE.pattern}, '
                      'as chirality-app-v4 does)')


def watched_name(name, identifier, executable):
    """The rule for a name the comparison watches."""
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

    Returns (entries, links). Anything that cannot be examined raises: absence is the only quiet case.
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


def compare(before, after, again):
    """STATEMENTS 2 and 3: unchanged only when all three listings were taken whole, met no link and agree."""
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
    """STATEMENT 2, the one place a run is judged."""
    failures = []
    if not facts.get('started'):
        failures.append('the App was not started')
    else:
        if facts.get('returncode') != 0:
            failures.append('the App ' + facts['ended'])
        if facts['signals']:
            failures.append(f"the helper received a signal ({len(facts['signals'])}) before the outcome was fixed")
        if facts.get('process_group') != 'gone':
            failures.append("a process of the App's process group was still running after the settle time")
    result = facts.get('comparison', {}).get('result', 'not made')
    if result != 'unchanged':
        failures.append({'not made': 'no complete comparison was made',
                         'incomplete': 'the comparison is incomplete: a link was met at or beneath a watched place',
                         'changed': 'the real Library changed in places named for the build'}[result])
    return ('clean' if not failures else 'failed'), failures


# ---- observations that never gate ---------------------------------------------------------------------

def observe(base, folders, identifier, executable, what):
    """An observation, never a refusal or a failure. Returns (entries, None) or (None, reason by category)."""
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
    """Files directly under the real Library/Preferences, by name, kind, size and time. A link there is listed as an
    entry of kind link (not followed); only the folder itself being a link, or anything that cannot be examined,
    makes the observation not made."""
    folder = real_home() / 'Library/Preferences'
    try:
        found = kind_of(folder)
        if found == 'absent':
            return {}, None
        if found != 'dir':
            return None, 'not observed: the preference folder is a link or not a folder'
        with os.scandir(folder) as entries:
            infos = {e.name: e.stat(follow_symlinks=False) for e in entries}
        return {name: _describe(info) for name, info in infos.items() if not stat.S_ISDIR(info.st_mode)}, None
    except OSError as error:
        return None, f'not observed: the preference folder could not be examined ({type(error).__name__})'


def disclosure(before, after, exclude=()):
    """Changes only when both observations were made; otherwise why not, and no changes at all."""
    if before[1] or after[1]:
        return {'observation': before[1] or after[1]}
    return {'observation': 'made', 'changes': [c for c in differences(before[0], after[0]) if c['path'] not in exclude]}


# ---- the new launch folder and its home ---------------------------------------------------------------

def new_folder_name():
    return f'launch-{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}-{secrets.token_hex(4)}'


def make_folder(parent):
    """A new launch folder and home/ within it, each by an exclusive create through a held handle: the create fails
    if anything already exists there under any spelling the volume treats as the same. Returns the folder's path and
    a held handle on the new home. Nothing in the home is read."""
    parent_fd = open_directory(parent, 'the parent')
    try:
        check_place(parent, 'the parent')
        name = new_folder_name()
        try:
            os.mkdir(name, 0o700, dir_fd=parent_fd)
        except FileExistsError:
            raise Refusal(f'a launch folder could not be created: something already exists there ({parent / name})') from None
        folder_fd = os.open(name, DIRECTORY, dir_fd=parent_fd)
    finally:
        os.close(parent_fd)
    try:
        try:
            os.mkdir(HOME, 0o700, dir_fd=folder_fd)
        except FileExistsError:
            raise Refusal(f'the home could not be created: something already exists there ({parent / name / HOME})') from None
        home_fd = os.open(HOME, DIRECTORY, dir_fd=folder_fd)
    finally:
        os.close(folder_fd)
    return parent / name, home_fd


# ---- STATEMENT 1: the environment ---------------------------------------------------------------------

def check_model_address(value):
    """A loopback address only, by the helper's own rule (localhost, empty and blank are refused)."""
    match = MODEL_ADDRESS_RULE.fullmatch(value) if isinstance(value, str) and len(value) <= 2048 else None
    if not match or (match.group(1) and not 1 <= int(match.group(1)) <= 65535):
        raise Refusal(f'{MODEL_ADDRESS} must be http(s)://127.0.0.1 or [::1], an optional port 1-65535 and a plain path')
    return value


def child_environment(home, tmp, model_address):
    """STATEMENT 1: a new mapping from the allowlist alone; nothing is read from this process's environment."""
    env = {'HOME': str(home), 'CFFIXED_USER_HOME': str(home), 'TMPDIR': str(Path(home, tmp)),
           'PATH': SYSTEM_PATH, 'LANG': LANG}
    env.update({name: value for name, (value, _) in PROXY_OVERRIDES.items()})
    env[MODEL_ADDRESS] = model_address
    return env


def check_environment(env, home, tmp):
    """STATEMENT 1, immediately before the App starts: exactly the allowlist, with these values."""
    if not isinstance(env, dict) or not all(isinstance(k, str) and isinstance(v, str) for k, v in env.items()):
        raise Refusal('the App environment is not a mapping of names to text')
    if set(env) != set(ALLOWED):
        raise Refusal(f'App environment outside the allowlist: extra {sorted(set(env) - set(ALLOWED))}, '
                      f'missing {sorted(set(ALLOWED) - set(env))}')
    if env['HOME'] != str(home) or env['CFFIXED_USER_HOME'] != str(home):
        raise Refusal('HOME and CFFIXED_USER_HOME must both be the new home; refusing to launch')
    if env['TMPDIR'] != str(Path(home, tmp)):
        raise Refusal("TMPDIR is not this launch's folder in the new home; refusing to launch")
    if env['PATH'] != SYSTEM_PATH or env['LANG'] != LANG:
        raise Refusal('PATH or LANG differs from the allowlist')
    if any(env[name] != value for name, (value, _) in PROXY_OVERRIDES.items()):
        raise Refusal('a proxy override differs from its fixed value; refusing to launch')
    check_model_address(env[MODEL_ADDRESS])
    return env


# ---- the run ------------------------------------------------------------------------------------------

def how_it_ended(returncode):
    if returncode < 0:
        try:
            return f'ended by signal {-returncode} ({signal.Signals(-returncode).name})'
        except ValueError:
            return f'ended by signal {-returncode}'
    return f'exited with status {returncode}'


def launch(args):
    run = caller_path(args.run_dir, 'the run folder')
    parent = caller_path(args.parent, 'the parent')
    model_address = DEFAULT_MODEL_ADDRESS if args.model_address is None else check_model_address(args.model_address)
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
        folder, home_fd = make_folder(parent)
        try:
            os.mkdir(run.name, 0o700, dir_fd=run_parent)
            run_fd = os.open(run.name, DIRECTORY, dir_fd=run_parent)
        except BaseException:
            os.close(home_fd)
            raise
    finally:
        os.close(run_parent)
    try:
        return _run(args, app, record_data, identifier, executable_path, executable, model_address,
                    folder, home_fd, run, run_fd)
    finally:
        os.close(run_fd)
        os.close(home_fd)


def _run(args, app, record_data, identifier, executable_path, executable, model_address, folder, home_fd, run, run_fd):
    home = folder / HOME
    tmp = f'.chirality-launch-tmp-{secrets.token_hex(4)}'
    record = {'note': NOTE, 'helper': {'path': TOOL, 'sha256': sha256_file(__file__)},
              'candidate_key': record_data['candidate_key'], 'identifier': identifier, 'bundle': str(app),
              'candidate_folder': args.candidate, 'launch_folder': str(folder), 'home': str(home),
              'address_override': 'the default (nothing listens there)' if args.model_address is None
              else 'given by the caller'}
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
        os.mkdir(tmp, 0o700, dir_fd=home_fd)
        env = child_environment(home, tmp, model_address)
        record['environment_constructed_for_the_app'] = env
        try:
            before = listing(real_home() / 'Library', ('', *WATCHED), identifier, executable)
        except OSError as error:
            facts['ended'] = f'not launched: the before-listing could not be made ({type(error).__name__})'
            return _finish(run_fd, record, facts, code=2, label='not launched')
        prefs_before = preferences_observation()
        cache_before = observe(cache, ('',), identifier, executable, 'per-user cache folder')
        try:  # immediately before the start: the exact mapping (STATEMENT 1)
            check_environment(env, home, tmp)
        except Refusal as error:
            facts['ended'] = f'not launched: {error}'
            return _finish(run_fd, record, facts, code=2, label='not launched')
        if facts['signals']:
            facts['ended'] = 'not launched: the helper received a signal before the App started'
            return _finish(run_fd, record, facts, code=2, label='not launched')
        output_name = f'.chirality-launch-output-{secrets.token_hex(3)}.log'
        output = os.open(output_name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=home_fd)
        record['output'] = str(home / output_name)
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
        print(json.dumps({'launched': proc.pid, 'run_folder': str(run), 'launch_folder': str(folder)}),
              file=sys.stderr, flush=True)
        facts['returncode'] = proc.wait()
        facts['ended'] = how_it_ended(facts['returncode'])
        record['ended_at'] = now()
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
        record['disclosed'] = {'preferences': disclosure(prefs_before, prefs_after, named),
                               'user_cache': {'folder': str(cache) if cache else None,
                                              **disclosure(cache_before, cache_after)}}
        return _finish(run_fd, record, facts, code=None)
    finally:
        _forwarding.clear()
        if output is not None:
            os.close(output)
        if proc is not None and proc.poll() is None:
            print(json.dumps({'warning': f'the App (process {proc.pid}) is still running; no record says it ended'}),
                  file=sys.stderr)
        for s, handler in previous.items():
            signal.signal(s, handler)


def group_state(pgid):
    try:
        os.killpg(pgid, 0)
    except ProcessLookupError:
        return 'gone'
    except PermissionError:
        return 'still running'
    return 'still running'


def write_record(run_fd, record):
    """STATEMENT 2: the record exists whole under its name or not at all: written to a temporary name in the run
    folder, flushed, then linked to its name (never over an existing one). A temporary file left by an interruption
    has another name and is not the record."""
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
    record['app_started'] = facts['started']
    record['ended'] = facts.get('ended')
    record.setdefault('started_at', None)
    record['real_library'] = facts.get('comparison', {'result': 'not made'})
    record['signals_received'] = list(facts['signals'])
    record['failures'] = failures
    record['outcome'] = label or result
    write_record(run_fd, record)
    print(json.dumps({'outcome': record['outcome'], 'record': facts['run'] + '/' + RECORD, 'failures': failures},
                     indent=2))
    return code if code is not None else (0 if result == 'clean' else 1)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description=__doc__.splitlines()[0] + ' A controlled development launcher, not an isolation boundary.',
        epilog='Each run creates a new launch folder (launch-<time>-<random>) holding a new home (home/), launches the '
               'App once, and does nothing more with them. The helper deletes nothing. What it states, what it also '
               'does and its limits are in the module docstring.')
    parser.add_argument('command', choices=['launch'])
    parser.add_argument('--candidate', required=True,
                        help='the candidate folder made by build_candidate.py: the bundle is read from '
                             'target/debug/bundle/macos and its identification record from '
                             "identification/candidate-identification.json; identification's check must pass")
    parser.add_argument('--run-dir', required=True, help='new folder for the run record')
    parser.add_argument('--parent', required=True, help='existing folder in which the new launch folder is made')
    parser.add_argument('--model-address', help=f'a loopback stub address for {MODEL_ADDRESS}; omitted means the default '
                        f'{DEFAULT_MODEL_ADDRESS} (nothing listens there); empty or blank is refused; '
                        'http(s)://127.0.0.1 or [::1] only')
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
