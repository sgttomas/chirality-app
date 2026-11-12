#!/usr/bin/env python3
"""Launch one identified development App build, once, in a new throwaway home (DEL-09-02 examination tooling).

A development launcher for first launches on new throwaway homes that never
hold a sign-in, all under one homes root. It is not a boundary around the App
or around anything the App starts. Each run creates a launch folder under the
root, launches the App once with its home there, publishes a record, and does
nothing more with them; it cannot relaunch a home. The caller does not choose
where the launch folder, the home or the record go; the candidate folder is
the only path a caller gives.

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

What the App starts, and what limits it. The App is this project's own
reviewed code; what it does with the home and environment it is given is the
App's. In every real run the App starts the supplier's Codex, which is not this
project's code. What applies to Codex in a launch by this launcher is only
this: it receives, through the App, the nine overrides, which redirect its
model address and obstruct its other network clients under their defaults, and
nothing more; it runs commands under the supplier's own sandbox and the App's
permission model, neither of which this launcher sets, checks or observes.
What the launcher can see of Codex is whether a member of the App's process
group was alive after the settle time, and nothing else: not what Codex read,
wrote or reached. This launcher starts no Codex itself.

What it also does, each with its limit:
- The homes root is dev/chirality-t3/scratch/app/homes/examination under the
  account's home (homes_root). The launcher refuses to run unless the root is
  an existing directory of this user, reached from / without following any
  link. It never creates the root and deletes nothing.
- Under the root it creates a launch folder (launch-<UTC time>-<random>) by an
  exclusive create through the root's held handle, and within it home/ and
  record/ the same way (make_folder). An exclusive create fails if anything
  already exists there under any spelling the volume treats as the same, so the
  App is never launched into a home that existed before the run. Limit: HOME is
  passed to the App as a pathname, and the launcher does not re-check it.
- The record is published in record/, whole or absent. A launch folder whose
  record/ is empty is one whose run did not complete; nothing more is known of
  it from the folder.
- Under the home it creates a temporary folder and an output file for the App's
  output, through the home's handle, and reads nothing there.
- The candidate folder is admitted (find_candidate, identify_candidate) when it
  is written as an absolute path with no empty, "." or ".." component and no
  trailing slash (refused as written, before any normalisation); it is reached
  from / with no link in its path; no directory on that path is the homes root
  (compared by device and inode while descending, before anything beneath the
  root is examined); it has build_candidate.py's layout; the identification
  record is the one at identification/candidate-identification.json inside it;
  the bundle is the one entry of target/debug/bundle/macos, whose name must be
  the record's bundle name, checked first to be a single plain name ending in
  .app and opened by the launcher only as an entry of that folder's handle; and
  identification's own validation and check of that bundle against that record
  pass (which compares the bundle's name, identifier and inventory with the
  record, and hashes the bundle twice). Identification's check reads the bundle
  by the candidate path joined with that checked name, opening each component
  without following links. The identification record does not say where its
  bundle was identified; what is compared is the record found beside the bundle
  in the build's layout. Errors name the kind of failure, counts and field
  names, not values read from the record.
- The record lists what leaves a run: the comparison's names, change labels and
  counts; the per-user cache folder and preference-folder observations (names
  and change labels; they never refuse a launch or fail a run); how the App
  ended; the output file's path. No content of any file.
- The address override replaces the built-in provider's address for model
  requests only, once the App reads that input (it arrives with the Access
  lane's change, not yet on main; of a candidate built before it, nothing is
  said). Neither override establishes where a launch's requests went. The
  launcher reads no system managed configuration.

Limits: the comparison sees names, kinds, sizes and modification times, not
content; the App's working directory is given by pathname; the launcher sends
the App no input and does not look at its window; it deletes nothing (a launch
folder is removed by hand, after the App started from it has ended: a killed
launcher does not end the App).
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
sys.path.insert(0, str(HERE.parent / 'candidate_identity'))
import identify  # noqa: E402  (identification's record validation and check)

TOOL = 'app/examination/standalone/launch.py'
NOTE = ('Evidence for a journey step record, written by ' + TOOL + '; not an examination record format, '
        'and nothing validates it.')
CODEX_NOTE = 'this launcher starts no Codex itself; whether the App started one is not known to it'
HOMES_ROOT = ('dev', 'chirality-t3', 'scratch', 'app', 'homes', 'examination')  # under the account's home
HOME, RECORD_FOLDER = 'home', 'record'  # the two children of a launch folder
RECORD = 'launch-record.json'  # in record/
BUNDLE_FOLDER = ('target', 'debug', 'bundle', 'macos')  # in a candidate folder (build_candidate.py)
IDENTIFICATION = ('identification', 'candidate-identification.json')  # in a candidate folder (identify.py record)
INVENTORY = 'bundle-inventory.json'  # beside the identification record
SYSTEM_PATH = '/usr/bin:/bin:/usr/sbin:/sbin'
LANG = 'en_US.UTF-8'
SETTLE_SECONDS = 5.0  # waited after the App exits before listing, and again before the second listing
DIRECTORY = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW

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

_forwarding = threading.Event()  # set while the launcher latches signals (tests wait on it before signalling)


class Refusal(ValueError):
    """A refusal whose message is the launcher's own words, never content read from a file."""


def real_home():
    """The real home, from the account database, never from HOME."""
    return Path(os.path.realpath(pwd.getpwuid(os.getuid()).pw_dir))


def homes_root():
    """The one homes root; the one thing tests replace with a stand-in."""
    return real_home().joinpath(*HOMES_ROOT)


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


def _ident(fd):
    info = os.fstat(fd)
    return info.st_dev, info.st_ino


def plain_name(value, what):
    """A single plain entry name: text, not empty, no separator or NUL, not "." or ".."."""
    if not isinstance(value, str) or value in ('', '.', '..') or '/' in value or '\0' in value:
        raise Refusal(f'{what} is not a single plain name')
    return value


# ---- the homes root and the new launch folder ---------------------------------------------------------

def open_directory(path, what, refuse_identity=None):
    """A handle on a directory reached from / with no link in any component. With refuse_identity, a directory on
    the way (or the end) whose device and inode equal it is refused before anything beneath it is examined."""
    fd = os.open('/', DIRECTORY)
    try:
        for part in Path(path).parts[1:]:
            if refuse_identity is not None and _ident(fd) == refuse_identity:
                raise Refusal(f'{what} lies under the homes root: {path}')
            try:
                child = os.open(part, DIRECTORY, dir_fd=fd)
            except OSError:
                raise Refusal(f'{what} must be an existing folder given by a path with no link in it '
                              f'(a link or something else stands where a folder should be, or it could not be opened): '
                              f'{path}') from None
            os.close(fd)
            fd = child
        if refuse_identity is not None and _ident(fd) == refuse_identity:
            raise Refusal(f'{what} is the homes root: {path}')
        return fd
    except BaseException:
        os.close(fd)
        raise


def open_root():
    """The homes root: an existing directory of this user, reached from / without following any link. Never created."""
    root = homes_root()
    fd = open_directory(root, 'the homes root')
    if os.fstat(fd).st_uid != os.getuid():
        os.close(fd)
        raise Refusal(f'the homes root is not owned by this user: {root}')
    return root, fd


def new_folder_name():
    return f'launch-{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}-{secrets.token_hex(4)}'


def make_folder(root, root_fd):
    """A new launch folder under the root and home/ and record/ within it, each by an exclusive create through a held
    handle: a create fails if anything already exists there under any spelling the volume treats as the same.
    Returns the folder's path and held handles on home/ and record/. Nothing in the home is read."""
    name = new_folder_name()
    try:
        os.mkdir(name, 0o700, dir_fd=root_fd)
    except FileExistsError:
        raise Refusal(f'a launch folder could not be created: something already exists there ({root / name})') from None
    folder_fd = os.open(name, DIRECTORY, dir_fd=root_fd)
    try:
        handles = []
        for child in (HOME, RECORD_FOLDER):
            try:
                os.mkdir(child, 0o700, dir_fd=folder_fd)
            except FileExistsError:
                raise Refusal(f'{child}/ could not be created: something already exists there ({root / name})') from None
            handles.append(os.open(child, DIRECTORY, dir_fd=folder_fd))
    finally:
        os.close(folder_fd)
    return root / name, handles[0], handles[1]


# ---- the candidate ------------------------------------------------------------------------------------

def check_syntax(text, what):
    """A caller's path as written, before any normalisation: absolute, no empty, "." or ".." component, no trailing
    slash. Nothing is touched."""
    if not isinstance(text, str) or not text.startswith('/') or text == '/' or '\0' in text:
        raise Refusal(f'{what} must be an absolute path to a folder: {text!r}')
    if any(part in ('', '.', '..') for part in text.split('/')[1:]):
        raise Refusal(f'{what} is written ambiguously (an empty, "." or ".." component, or a trailing slash): {text!r}')
    return Path(text)


def open_within(fd, names, what):
    """A handle on a folder reached from fd through names (each a plain entry name), without following any link."""
    held = os.dup(fd)
    try:
        for name in names:
            try:
                child = os.open(plain_name(name, what), DIRECTORY, dir_fd=held)
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


def find_candidate(text, root_identity):
    """The candidate folder in build_candidate.py's layout, reached without following any link and not under the
    homes root; its identification record and stored inventory are plain files of this user; its bundle folder holds
    exactly one entry. Returns the candidate path and the record's path; the bundle is found from the record."""
    candidate = check_syntax(text, 'the candidate folder')
    candidate_fd = open_directory(candidate, 'the candidate folder', refuse_identity=root_identity)
    try:
        identification = open_within(candidate_fd, IDENTIFICATION[:1], "the candidate's identification folder")
        try:
            regular_file(identification, IDENTIFICATION[1], 'the identification record')
            regular_file(identification, INVENTORY, 'the stored bundle inventory')
        finally:
            os.close(identification)
    finally:
        os.close(candidate_fd)
    return candidate, candidate.joinpath(*IDENTIFICATION)


def find_bundle(candidate, record_data):
    """The bundle is the one entry of the candidate's bundle folder whose name is the record's bundle name. The name
    read from the record is checked to be a single plain name ending in .app before anything is opened by it, and it
    is opened only as an entry of the bundle folder's held handle. The executable path from the record is checked to
    be Contents/MacOS/<plain name> the same way."""
    bundle = record_data.get('bundle') if isinstance(record_data.get('bundle'), dict) else {}
    name = plain_name(bundle.get('name'), "the record's bundle name")
    if not name.endswith('.app'):
        raise Refusal("the record's bundle name does not end in .app")
    executable = bundle.get('executable', {}).get('path') if isinstance(bundle.get('executable'), dict) else None
    parts = executable.split('/') if isinstance(executable, str) else []
    if len(parts) != 3 or parts[:2] != ['Contents', 'MacOS']:
        raise Refusal("the record's executable path is not Contents/MacOS/<name>")
    plain_name(parts[2], "the record's executable name")
    candidate_fd = open_directory(candidate, 'the candidate folder')
    try:
        macos = open_within(candidate_fd, BUNDLE_FOLDER, "the candidate's bundle folder (target/debug/bundle/macos)")
        try:
            if os.listdir(macos) != [name]:
                raise Refusal("the candidate's bundle folder does not hold exactly the record's bundle")
            os.close(open_within(macos, [name], 'the bundle'))
        finally:
            os.close(macos)
    finally:
        os.close(candidate_fd)
    return candidate.joinpath(*BUNDLE_FOLDER, name), executable, parts[2]


def identify_candidate(app, record_path):
    """Identification's own validation and check of the bundle against the record. Errors name the kind of failure,
    counts and field names, never a value read from the record."""
    try:
        identify.validate_record(json.loads(Path(record_path).read_bytes()))
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


def read_record(record_path):
    """The identification record's content, read once; only its own fields are used, never quoted in an error."""
    try:
        value = json.loads(Path(record_path).read_bytes())
    except (OSError, ValueError):
        raise Refusal('the identification record could not be read as JSON') from None
    if not isinstance(value, dict) or not isinstance(value.get('candidate_key'), str) or not value['candidate_key']:
        raise Refusal('the identification record has no candidate key')
    if not isinstance(value.get('bundle'), dict) or not isinstance(value['bundle'].get('identifier'), str):
        raise Refusal('the identification record has no bundle identifier')
    return value


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
            failures.append(f"the launcher received a signal ({len(facts['signals'])}) before the outcome was fixed")
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


# ---- STATEMENT 1: the environment ---------------------------------------------------------------------

def check_model_address(value):
    """A loopback address only, by the launcher's own rule (localhost, empty and blank are refused)."""
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


def group_state(pgid):
    try:
        os.killpg(pgid, 0)
    except ProcessLookupError:
        return 'gone'
    except PermissionError:
        return 'still running'
    return 'still running'


def launch(args):
    model_address = DEFAULT_MODEL_ADDRESS if args.model_address is None else check_model_address(args.model_address)
    root, root_fd = open_root()
    try:
        candidate, record_path = find_candidate(args.candidate, _ident(root_fd))
        record_data = read_record(record_path)
        app, executable_path, executable = find_bundle(candidate, record_data)
        check_executable(executable)
        identify_candidate(app, record_path)
        folder, home_fd, record_fd = make_folder(root, root_fd)
    finally:
        os.close(root_fd)
    print(json.dumps({'launch_folder': str(folder)}), file=sys.stderr, flush=True)
    try:
        return _run(args, app, record_data, executable_path, executable, model_address, folder, home_fd, record_fd)
    finally:
        os.close(record_fd)
        os.close(home_fd)


def _run(args, app, record_data, executable_path, executable, model_address, folder, home_fd, record_fd):
    identifier = record_data['bundle']['identifier']
    home = folder / HOME
    tmp = f'.chirality-launch-tmp-{secrets.token_hex(4)}'
    record = {'note': NOTE, 'made_by': {'path': TOOL, 'sha256': sha256_file(__file__)}, 'made_at': now(),
              'candidate_key': record_data['candidate_key'], 'identifier': identifier, 'candidate_folder': args.candidate,
              'bundle': str(app), 'launch_folder': str(folder), 'home': str(home), 'codex': CODEX_NOTE,
              'address_override': 'the default (nothing listens there)' if args.model_address is None
              else 'given by the caller'}
    facts = {'started': False, 'signals': [], 'open': True, 'record': str(folder / RECORD_FOLDER / RECORD)}
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
            return _finish(record_fd, record, facts, code=2, label='not launched')
        prefs_before = preferences_observation()
        cache_before = observe(cache, ('',), identifier, executable, 'per-user cache folder')
        try:  # immediately before the start: the exact mapping (STATEMENT 1)
            check_environment(env, home, tmp)
        except Refusal as error:
            facts['ended'] = f'not launched: {error}'
            return _finish(record_fd, record, facts, code=2, label='not launched')
        if facts['signals']:
            facts['ended'] = 'not launched: the launcher received a signal before the App started'
            return _finish(record_fd, record, facts, code=2, label='not launched')
        output_name = f'.chirality-launch-output-{secrets.token_hex(3)}.log'
        output = os.open(output_name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=home_fd)
        record['output'] = str(home / output_name)
        record['started_at'] = now()
        try:  # the working directory is given by pathname (no pre-exec hook)
            proc = subprocess.Popen([str(app / executable_path)], env=env, cwd=home, stdin=subprocess.DEVNULL,
                                    stdout=output, stderr=output, start_new_session=True, close_fds=True)
        except OSError as error:
            facts['ended'] = f'did not start ({type(error).__name__})'
            return _finish(record_fd, record, facts, code=1)
        facts['started'] = True
        record['pid'] = proc.pid
        if facts['signals']:
            proc.send_signal(signal.SIGTERM)
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
        return _finish(record_fd, record, facts, code=None)
    finally:
        _forwarding.clear()
        if output is not None:
            os.close(output)
        if proc is not None and proc.poll() is None:
            print(json.dumps({'warning': f'the App (process {proc.pid}) is still running; no record says it ended'}),
                  file=sys.stderr)
        for s, handler in previous.items():
            signal.signal(s, handler)


def write_record(record_fd, record):
    """STATEMENT 2: the record exists whole under its name or not at all: written to a temporary name in record/,
    flushed, then linked to its name (never over an existing one). A temporary file left by an interruption has
    another name and is not the record."""
    temporary = f'.{RECORD}.partial-{secrets.token_hex(4)}'
    fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=record_fd)
    with os.fdopen(fd, 'w') as stream:
        stream.write(json.dumps(record, indent=2) + '\n')
        stream.flush()
        os.fsync(stream.fileno())
    os.link(temporary, RECORD, src_dir_fd=record_fd, dst_dir_fd=record_fd, follow_symlinks=False)
    os.unlink(temporary, dir_fd=record_fd)


def _finish(record_fd, record, facts, code, label=None):
    facts['open'] = False  # the outcome is fixed from here: a later signal changes nothing in the record
    result, failures = outcome(facts)
    record['app_started'] = 'started' if facts['started'] else 'not started'
    record['ended'] = facts.get('ended')
    record.setdefault('started_at', None)
    record['real_library'] = facts.get('comparison', {'result': 'not made'})
    record['signals_received'] = list(facts['signals'])
    record['failures'] = failures
    record['outcome'] = label or result
    write_record(record_fd, record)
    print(json.dumps({'outcome': record['outcome'], 'record': facts['record'], 'failures': failures}, indent=2))
    return code if code is not None else (0 if result == 'clean' else 1)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description=__doc__.splitlines()[0] + ' Not a boundary around the App or what it starts.',
        epilog='Each run creates a new launch folder (launch-<time>-<random>) under the homes root '
               '(dev/chirality-t3/scratch/app/homes/examination under the account\'s home, which must exist), with '
               'home/ and record/ in it, launches the App once and publishes the record in record/. The caller does '
               'not choose where they go. What the launcher states, what it also does and its limits are in the '
               'module docstring.')
    parser.add_argument('command', choices=['launch'])
    parser.add_argument('--candidate', required=True,
                        help='the candidate folder made by build_candidate.py; the identification record is '
                             'identification/candidate-identification.json in it and the bundle the one entry of '
                             "target/debug/bundle/macos, named as the record names it; identification's check must pass")
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
