"""Shared base of the 4.0.0 release tools; this module runs no command itself.

build.py, and any release tool built on it, share:

- the release identity and the candidate description;
- the closed list of failure reasons (REASONS), the only text a failure carries;
- selection: every value a returnable file holds is constructed by the tool or
  selected from tool output and validated against a stated shape;
- the two writers: `write_returnable` (validated JSON, the only content of the
  files that are sent back) and `PrivateWriter` (raw tool output and traces,
  written and never read back);
- refusal of any input path inside the private folder, by name;
- location checks by filesystem identity;
- the reading of Mach-O code signatures without Apple tools.
"""
import importlib.util
import json
import os
from pathlib import Path
import plistlib
import re
import stat
import struct
import subprocess

ROOT = Path(__file__).resolve().parents[3]


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    value = importlib.util.module_from_spec(spec); spec.loader.exec_module(value)
    return value


prepare = load_module('release_production_prepare', 'app/packaging/production_inputs/prepare.py')
inventory = prepare.inventory
require, sha, parse = prepare.require, prepare.sha, prepare.parse

# The 4.0.0 release identity (docs/RELEASE_TARGET_4.0.0.md; DEL-01-06 scope).
# The base tauri.conf.json keeps the development identity on purpose: the
# production identifier belongs only in the generated overlay, so that no
# development run points at a person's existing data.
RELEASE = {'identifier': 'com.chirality.app', 'version': '4.0.0', 'minimum_system_version': '15.0'}
PRODUCT_NAME = 'Chirality'
MAIN_EXECUTABLE = 'chirality-app-v4'  # Cargo binary name; Tauri sets no mainBinaryName
APP_NAME = PRODUCT_NAME + '.app'
VENDOR_DESTINATION = 'Contents/Resources/codex'
LIMITATIONS_SOURCE = 'docs/RELEASE_LIMITATIONS_4.0.0.md'
LIMITATIONS_IN_BUNDLE = 'Contents/Resources/release/LIMITATIONS.md'
SUPPLIER_TEAM = inventory.SUPPLIER_TEAM
APP_ID_KEY = 'com.apple.application-identifier'
TEAM_KEY = 'com.apple.developer.team-identifier'
CANDIDATE_FORMAT = 'chirality-release-candidate/1'
CANDIDATE_FILE = 'CANDIDATE.json'
CANDIDATE_PENDING = 'CANDIDATE.pending.json'
# Raw tool output, full traces and raw notarization logs go only here. The folder may hold the
# owner's account details. Restrictive modes do not keep agents out on the owner's machine (agents
# run as the owner's user); a rule does: no tool or test of ours opens this folder or anything in
# it after writing. PrivateWriter writes and has no read method; nothing elsewhere reads it.
PRIVATE_FOLDER = 'PRIVATE-raw-output-may-hold-account-details-do-not-send'


class Result:
    def __init__(self, returncode, stdout=b'', stderr=b''):
        self.returncode = returncode
        self.stdout = stdout if isinstance(stdout, bytes) else stdout.encode()
        self.stderr = stderr if isinstance(stderr, bytes) else stderr.encode()

    def text(self):
        return self.stdout.decode('utf-8', 'replace') + '\n' + self.stderr.decode('utf-8', 'replace')


def system_runner(argv, *, env, cwd=None, timeout=None):
    """Run one argv (never a shell string) with exactly the given environment."""
    done = subprocess.run(list(argv), env=dict(env), cwd=cwd, capture_output=True, timeout=timeout, stdin=subprocess.DEVNULL)
    return Result(done.returncode, done.stdout, done.stderr)


# --- The closed list of failure reasons -------------------------------------
# Every STOP and every build failure carries exactly one of these, and no other text. Each names
# its step and the observation that failed, so that a failed run can usually be repaired without
# sending anything; the detail stays in the private folder.

REASONS = {
    'BUILD_HOST': 'build: this host is not Apple Silicon macOS',
    'BUILD_OUT': 'build: --out exists, or the folder that would hold it does not, or it is inside /Applications or ~/Library',
    'BUILD_ENVIRONMENT': 'build: the caller environment is not exactly PATH and LANG with single-line values and absolute PATH entries',
    'BUILD_TOOLS': 'build: the resolved rustc, cargo, clang and ld are not all given, or rustc or cargo on PATH is not the given one or is a rustup proxy',
    'BUILD_PUBLISHER_PAIR': 'build: the publisher input file and its digest were not given together',
    'BUILD_NODE_MODULES': 'build: the source export holds node_modules; dependencies come from the npm cache',
    'BUILD_CARGO_CACHE': 'build: the Cargo cache input holds configuration or credentials',
    'BUILD_LINK': 'build: the source export, the Cargo home or the npm cache holds a link (a symbolic link, or a file with more than one hard link)',
    'BUILD_PRIVATE_INPUT': 'build: an input path lies inside a folder named as the private output folder',
    'BUILD_LIMITATIONS': 'build: the source export lacks docs/RELEASE_LIMITATIONS_4.0.0.md',
    'BUILD_PUBLISHER_SOURCE': 'build: the compiled keychain selection in the source is not exactly one release identifier and team',
    'BUILD_PLAN': 'build: prepare.py refused the plan or check_plan did not pass',
    'BUILD_OVERLAY': 'build: the plan overlay is not the 4.0.0 release identity',
    'BUILD_RECIPE': 'build: the recipe is not an unsigned build from an empty environment of exactly the allowlist',
    'BUILD_CONTAINED': 'build: a writable location of the build environment is not inside the run folder',
    'BUILD_SCOPE': 'build: the host, macOS or SDK could not be observed, or differs from the Cargo build input\'s scope',
    'BUILD_CARGO_INPUT': 'build: the Cargo configuration or the toolchain digests differ from the Cargo build input',
    'BUILD_INSTALL': 'build: the offline dependency install did not return zero',
    'BUILD_RUN': 'build: the recipe build did not return zero',
    'BUILD_BUNDLE': 'build: not exactly one Chirality.app bundle was built',
    'BUILD_CHECKS': 'build: a check of the built bundle failed; BUILD_REFUSED.json names each check',
    'BUILD_FINAL': 'build: the final reading of the described candidate did not verify',
    'BUILD_INTERRUPTED': 'build: the build was interrupted before it finished',
}
BUILD_STAGES = {'INPUTS': 'reading the inputs', 'COPY': 'copying the inputs', 'PLAN': 'preparing the plan', 'ENVIRONMENT': 'preparing the build environment',
                'INSTALL': 'the offline dependency install', 'RUN': 'the recipe build', 'CHECKS': 'checking the built bundle',
                'PUBLISH': 'publishing the candidate'}
for _stage, _name in BUILD_STAGES.items():
    REASONS[f'BUILD_UNEXPECTED_{_stage}'] = f'build: an error no check covers during {_name}; the private folder holds the trace'


class FixedParser(__import__('argparse').ArgumentParser):
    """An argument parser whose errors never echo what was typed."""

    def error(self, message):
        self.exit(2, 'usage error: an argument is missing, repeated or unknown; see --help\n')


class Failure(Exception):
    """A failure with a code from REASONS; its text is the fixed reason and nothing else."""

    def __init__(self, code):
        require(code in REASONS, 'unlisted failure reason')
        super().__init__(REASONS[code])
        self.code, self.reason = code, REASONS[code]


def check(condition, code):
    if not condition:
        raise Failure(code)


# --- Shapes: every value a returnable file holds is one of these -------------

SHAPES = {
    'sha256': r'[0-9a-f]{64}', 'cdhash': r'[0-9a-f]{40}', 'revision': r'[0-9a-f]{40}',
    'uuid': r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}',
    'profile_uuid': r'[0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12}',
    'identifier': r'[A-Za-z0-9](?:[A-Za-z0-9._-]{0,253}[A-Za-z0-9])?',
    'version': r'\d+(?:\.\d+){0,3}',
    'mode': r'0o[0-7]{3,4}',
    'timestamp': r'\d{1,2} [A-Z][a-z]{2} \d{4} at \d{1,2}:\d{2}:\d{2}',  # the form TN3161 shows for codesign's Timestamp=
    'iso_datetime': r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})?',
    'relative_path': r'(?!/)(?!.*(?:^|/)\.\.(?:/|$))[A-Za-z0-9._+@ ,()/-]+',
    'placeholder_path': r'<(?:out|candidate)>(?:/[A-Za-z0-9._+@ ,()-]+)*',
    'tool_path': r'/usr/(?:s?bin)/[a-z_]+',
    'option': r'-{1,2}[a-z][a-z0-9-]*(?:=[0-9]+)?',
}
COMPILED_SHAPES = {name: re.compile(pattern) for name, pattern in SHAPES.items()}
STATUS_WORDS = {'Accepted', 'Invalid', 'Rejected', 'In Progress'}
AUTHORITY_KINDS = {'Developer ID Application', 'Developer ID Certification Authority', 'Apple Root CA'}
VOCABULARY = set(REASONS.values()) | STATUS_WORDS | AUTHORITY_KINDS | {
    'file', 'dir', 'symlink', 'other', 'not observed', 'complete', 'stopped', 'failed', 'Notarized Developer ID',
    'unexpected entitlement present', 'notarytool', 'submit', 'log', 'stapler', 'staple', 'validate', 'create', 'attach',
    'detach', 'UDZO', 'context:primary-signature', 'open', 'exec', 'runtime', 'json', 'Chirality', 'build', 'ci', 'npm', 'node',
    'node_modules/@tauri-apps/cli/tauri.js', 'custom-protocol,distribution-successor', 'app', '-', 'macos-arm64-rust-1.97.1-no-strip',
    'aarch64-apple-darwin', '--', '<elsewhere>', '<app-submission-id>', '<disk-image-submission-id>',
    'limitations copy in the bundle: absent', 'limitations copy in the disk_image: absent', 'publisher-build-selection.s1 generated from the source keychain selection', 'supplied publisher input file',
    CANDIDATE_FORMAT,
}


MAX_LENGTH = 1024  # every string field, paths and identifiers included, is bounded


def is_shape(value, name):
    return isinstance(value, str) and len(value) <= MAX_LENGTH and COMPILED_SHAPES[name].fullmatch(value) is not None


def selected(value, name):
    """`value` if it has the shape, else None (the caller records a failure)."""
    return value if is_shape(value, name) else None


# Known entitlements and the type their value must have. A key outside this list is counted as
# "unexpected entitlement present"; its value is never recorded.
KNOWN_ENTITLEMENTS = {
    APP_ID_KEY: 'app_id', TEAM_KEY: 'team', 'keychain-access-groups': 'app_id_list',
    'com.apple.security.get-task-allow': bool, 'get-task-allow': bool,
    'com.apple.security.app-sandbox': bool, 'com.apple.security.cs.allow-jit': bool,
    'com.apple.security.cs.allow-unsigned-executable-memory': bool, 'com.apple.security.cs.disable-library-validation': bool,
    'com.apple.security.cs.allow-dyld-environment-variables': bool, 'com.apple.security.cs.disable-executable-page-protection': bool,
    'com.apple.security.cs.debugger': bool, 'com.apple.security.network.client': bool, 'com.apple.security.network.server': bool,
    'com.apple.security.device.audio-input': bool, 'com.apple.security.device.camera': bool,
    'com.apple.security.automation.apple-events': bool, 'com.apple.security.files.user-selected.read-write': bool,
    'com.apple.security.files.user-selected.read-only': bool, 'com.apple.security.inherit': bool,
}
APP_ID = re.compile(r'([A-Z0-9]{10})\.(?:[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*(?:\.\*)?|\*)')


# --- The two writers ------------------------------------------------------------

def validate_returnable(value, public_teams, where='', argv_allowed=None, in_argv=False):
    """Every key and string in a returnable file has a stated shape or is fixed tool text.

    `argv_allowed` holds (previous argument, value) pairs allowed verbatim inside an `argv` list only:
    the identity name after --sign, the notary profile name after --keychain-profile, and the compiled
    requirement after -R.
    """
    if isinstance(value, dict):
        for key, item in value.items():
            require(isinstance(key, str) and (key in VOCABULARY or key in KNOWN_ENTITLEMENTS
                    or any(is_shape(key, s) for s in ('identifier', 'relative_path'))), 'unshaped key in returnable file')
            validate_returnable(item, public_teams, where + '.' + key, argv_allowed, in_argv=(key == 'argv'))
        return
    if isinstance(value, list):
        for index, item in enumerate(value):
            if in_argv and argv_allowed and isinstance(item, str) and index and (value[index - 1], item) in argv_allowed:
                require(len(item) <= MAX_LENGTH, 'over-long value in returnable file')  # the bound holds here too
                continue
            validate_returnable(item, public_teams, where, argv_allowed)
        return
    if value is None or isinstance(value, bool) or isinstance(value, int):
        return
    require(isinstance(value, str), 'unshaped value in returnable file')
    require(len(value) <= MAX_LENGTH, 'over-long value in returnable file')
    app_id = APP_ID.fullmatch(value)
    require(value in VOCABULARY or value in public_teams or value in KNOWN_ENTITLEMENTS or any(is_shape(value, s) for s in SHAPES)
            or (app_id is not None and app_id.group(1) in public_teams), 'unshaped value in returnable file at ' + where)


def is_private_path(path):
    """True when any component of the path, as given or resolved, is the private folder's name."""
    try:
        text = os.fsdecode(os.fspath(path))
    except TypeError:
        return True
    parts = set(Path(text).parts) | set(Path(os.path.realpath(text)).parts)
    return PRIVATE_FOLDER in parts


def refuse_private(path, what):
    """Refuse an input inside the private folder, by name, before anything is opened."""
    require(not is_private_path(path), f'{what} lies inside the private folder')


def require_inside(path, root, what):
    """A path a tool writes must be physically inside its own output folder, and not an existing link."""
    path = Path(path)
    refuse_installed_location(path, what)
    require(prepare.identity(Path(os.path.realpath(root))) in physical_ancestry(path.parent), f'{what} is not inside the output folder')
    if os.path.lexists(path):
        info = os.lstat(path)
        require(not stat.S_ISLNK(info.st_mode), f'{what} is an existing link')
        require(not stat.S_ISREG(info.st_mode) or info.st_nlink == 1, f'{what} is hard-linked')


def write_returnable(path, value, root, public_teams, argv_allowed=None, append=False):
    """The only writer of returnable files: validated, inside the output folder, never through a link."""
    require_inside(path, root, 'a returnable file')
    if append:
        validate_returnable(value, public_teams, argv_allowed=argv_allowed)
        raw = (json.dumps(value, sort_keys=True) + '\n').encode()
        flags = os.O_WRONLY | os.O_APPEND | os.O_CREAT | os.O_NOFOLLOW
    else:
        validate_returnable(value, public_teams)
        raw = (json.dumps(value, indent=2, sort_keys=True) + '\n').encode()
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW
    fd = os.open(path, flags, 0o644)
    try:
        require(os.fstat(fd).st_nlink == 1, 'a returnable file is hard-linked')
        os.write(fd, raw); os.fsync(fd)
    finally:
        os.close(fd)
    return sha(raw)


class PrivateWriter:
    """The only code that touches the private folder. It writes; it has no read method.

    The folder holds raw command output, raw notarization logs and full traces for the owner's own
    diagnosis. It may contain account details, stays on the owner's machine, is not sent back, and
    no tool or test of ours opens it or anything in it after writing.
    """

    def __init__(self, root):
        self.root = Path(root)
        self.folder = self.root / PRIVATE_FOLDER
        self.count = 0

    def write(self, label, raw):
        if not os.path.lexists(self.folder):
            require_inside(self.folder, self.root, 'the private folder')
            os.mkdir(self.folder, 0o700)
        os.chmod(self.folder, 0o700)
        self.count += 1
        name = f'{self.count:04d}-' + re.sub(r'[^a-z0-9]+', '-', label.lower()).strip('-')[:60]
        path = self.folder / name
        require_inside(path, self.root, 'a private file')
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
        try:
            os.fchmod(fd, 0o600)
            os.write(fd, raw if isinstance(raw, bytes) else str(raw).encode('utf-8', 'replace')); os.fsync(fd)
            file_mode = stat.S_IMODE(os.fstat(fd).st_mode)
        finally:
            os.close(fd)
        # The path and the modes this writer set, from its own descriptor: callers never look inside.
        return path, file_mode, stat.S_IMODE(os.lstat(self.folder).st_mode)


# --- Info.plist and locations ---------------------------------------------------

def read_info_plist(app):
    raw = (Path(app) / 'Contents/Info.plist').read_bytes()
    value = plistlib.loads(raw, dict_type=prepare.UniquePlistDict)  # a key twice is refused, never resolved to the last
    require(isinstance(value, dict), 'Info.plist is not a dictionary')
    return raw, value


def bundle_identity(info):
    return {'identifier': info.get('CFBundleIdentifier'), 'version': info.get('CFBundleShortVersionString'),
            'bundle_version': info.get('CFBundleVersion'), 'minimum_system_version': info.get('LSMinimumSystemVersion'),
            'executable': info.get('CFBundleExecutable')}


def release_identity_errors(info):
    identity = bundle_identity(info)
    errors = []
    for key, wanted in (('identifier', RELEASE['identifier']), ('version', RELEASE['version']),
                        ('bundle_version', RELEASE['version']), ('minimum_system_version', RELEASE['minimum_system_version'])):
        if identity[key] != wanted:
            errors.append('info_plist_' + key)
    if identity['executable'] != MAIN_EXECUTABLE:
        errors.append('info_plist_executable')
    return errors


def protected_places():
    """Where an installed App or a person's data lives; these tools never write there or take a candidate from there."""
    return [Path('/Applications'), Path('/System/Applications'), Path.home() / 'Library']


def physical_ancestry(path):
    """(device, inode) of the nearest existing ancestor of `path` and of each of its parents.

    Symlinks are resolved first; case aliases and macOS firmlinks are caught
    because the comparison is by filesystem identity, as prepare.py does.
    """
    path = Path(os.path.realpath(path))
    while not os.path.lexists(path):
        require(path != path.parent, 'no existing ancestor')
        path = path.parent
    return prepare.ancestors(path)


def refuse_installed_location(path, what):
    """Refuse a path physically inside /Applications, /System/Applications or ~/Library."""
    ancestry = physical_ancestry(path)
    for place in protected_places():
        if os.path.exists(place):
            require(prepare.identity(Path(os.path.realpath(place))) not in ancestry,
                    f'{what} may not be inside {place}; installing is the owner\'s act')


# --- Mach-O code signature, read from the bytes (no Apple tool) -------------

CS_ADHOC, CS_RUNTIME, CS_LINKER_SIGNED = 0x2, 0x10000, 0x20000
_THIN = {b'\xcf\xfa\xed\xfe': ('<', 32), b'\xce\xfa\xed\xfe': ('<', 28), b'\xfe\xed\xfa\xcf': ('>', 32), b'\xfe\xed\xfa\xce': ('>', 28)}
_FAT = {b'\xca\xfe\xba\xbe': 20, b'\xca\xfe\xba\xbf': 32}


def _slice_signature(raw):
    order, header = _THIN.get(raw[:4], (None, None))
    require(order is not None, 'not a Mach-O slice')
    ncmds, sizeofcmds = struct.unpack_from(order + 'II', raw, 16)
    offset, end = header, header + sizeofcmds
    require(end <= len(raw), 'Mach-O load commands exceed file')
    signature = None
    for _ in range(ncmds):
        cmd, size = struct.unpack_from(order + 'II', raw, offset)
        require(size >= 8 and offset + size <= end, 'malformed Mach-O load command')
        if cmd == 0x1d:
            require(signature is None, 'two code signature load commands')
            signature = struct.unpack_from(order + 'II', raw, offset + 8)
        offset += size
    if signature is None:
        return {'signed': False}
    dataoff, datasize = signature
    require(dataoff + datasize <= len(raw) and datasize >= 12, 'code signature outside file')
    blob = raw[dataoff:dataoff + datasize]
    magic, length, count = struct.unpack_from('>III', blob, 0)
    require(magic == 0xfade0cc0 and length <= len(blob), 'code signature is not an embedded SuperBlob')
    flags, code_directories, cms = None, [], False
    for index in range(count):
        kind, at = struct.unpack_from('>II', blob, 12 + 8 * index)
        require(at + 8 <= length, 'code signature blob index outside SuperBlob')
        bmagic, blength = struct.unpack_from('>II', blob, at)
        require(at + blength <= length, 'code signature blob outside SuperBlob')
        if bmagic == 0xfade0c02:
            cd_flags = struct.unpack_from('>I', blob, at + 12)[0]
            code_directories.append(sha(blob[at:at + blength]))
            flags = cd_flags if flags is None else flags | cd_flags
        elif bmagic == 0xfade0b01 and blength > 8:
            cms = True
    require(code_directories, 'code signature has no CodeDirectory')
    return {'signed': True, 'flags': flags, 'adhoc': bool(flags & CS_ADHOC), 'linker_signed': bool(flags & CS_LINKER_SIGNED),
            'runtime': bool(flags & CS_RUNTIME), 'cms': cms, 'code_directory_sha256': code_directories}


def macho_signatures(raw):
    """Signature facts for each slice of a thin or universal Mach-O."""
    if raw[:4] in _FAT:
        width = _FAT[raw[:4]]
        count = struct.unpack_from('>I', raw, 4)[0]
        require(0 < count <= 8, 'implausible universal Mach-O')
        slices = []
        for index in range(count):
            at = 8 + width * index
            if width == 20:
                offset, size = struct.unpack_from('>II', raw, at + 8)
            else:
                offset, size = struct.unpack_from('>QQ', raw, at + 8)
            require(offset + size <= len(raw), 'universal slice outside file')
            slices.append(_slice_signature(raw[offset:offset + size]))
        return slices
    return [_slice_signature(raw)]


def only_linker_adhoc(raw):
    """True when every slice carries only the linker's ad hoc signature."""
    slices = macho_signatures(raw)
    return all(s['signed'] and s['adhoc'] and s['linker_signed'] and not s['cms'] for s in slices), slices


# --- candidate description -------------------------------------------------

def tree_entries(tree):
    """Inventory entries without the absolute root, for records."""
    return {'root_mode': tree['root_mode'], 'manifest_sha256': tree['manifest_sha256'], 'files': tree['files'],
            'macho_files': tree['macho_files'], 'entries': tree['entries']}


def macho_paths(tree):
    return [e['path'] for e in tree['entries'] if e.get('macho')]


def load_candidate(candidate, name=CANDIDATE_FILE, finishing=False):
    """Read and verify a candidate description against the bytes it describes.

    Returns (description, app path, binding, requirement). Any difference refuses: the owner's step
    may only act on exactly what the build described. `finishing` is the build's own final check of
    the pending description, before it is published.
    """
    refuse_private(candidate, 'candidate')
    candidate = inventory.anchored(candidate)
    refuse_installed_location(candidate, 'candidate')
    markers = ('BUILD_FAILED.json', 'BUILD_REFUSED.json') + (() if finishing else ('INCOMPLETE.txt',))
    for marker in markers:
        require(not os.path.lexists(candidate / marker), 'the build did not finish: ' + marker + ' is present')
    raw = (candidate / name).read_bytes()
    value = parse(raw)
    require(value.get('format') == CANDIDATE_FORMAT, 'unknown candidate description format')
    app = candidate / prepare.files.relative(value['bundle']['path'])
    require(app.name == APP_NAME and app.is_dir() and not app.is_symlink(), 'candidate App bundle missing')
    tree = inventory.scan(app)
    require(inventory.compare(tree, value['bundle']['inventory'])['equal'], 'candidate App differs from its description')
    info_raw, info = read_info_plist(app)
    require(sha(info_raw) == value['bundle']['info_plist_sha256'], 'candidate Info.plist digest differs')
    require(not release_identity_errors(info), 'candidate Info.plist is not the 4.0.0 release identity')
    executable = (app / 'Contents/MacOS' / MAIN_EXECUTABLE).read_bytes()
    require(sha(executable) == value['bundle']['executable_sha256'], 'candidate executable digest differs')
    adhoc, _ = only_linker_adhoc(executable)
    require(adhoc, 'candidate executable carries a signature other than the linker ad hoc one')
    require(not (app / 'Contents/_CodeSignature').exists() and not (app / 'Contents/embedded.provisionprofile').exists(),
            'candidate App is already signed or holds a profile')
    vendor = inventory.scan(app / VENDOR_DESTINATION)
    require(inventory.compare(vendor, value['vendor']['inventory'])['equal'], 'candidate vendor tree differs from its description')
    publisher = value['publisher']
    for key in ('binding', 'requirement', 'projection'):
        file = publisher[key]
        require(sha((candidate / prepare.files.relative(file['path'])).read_bytes()) == file['sha256'],
                'candidate publisher output changed: ' + key)
    binding = parse((candidate / publisher['binding']['path']).read_bytes())
    requirement = (candidate / publisher['requirement']['path']).read_bytes()
    require(binding.get('state') == 'selected-production' and binding.get('production_bundle_identifier') == RELEASE['identifier'],
            'candidate publisher binding is not the selected production identity')
    require(binding.get('requirement_sha256') == sha(requirement), 'candidate requirement differs from its binding')
    require((candidate / publisher['binding']['path']).read_bytes() in executable and requirement in executable,
            'candidate executable does not hold the described publisher binding and requirement')
    limitations = value['limitations']
    require(sha((candidate / prepare.files.relative(limitations['copy'])).read_bytes()) == limitations['sha256'],
            'candidate limitations copy differs from the source digest')
    return value, app, binding, requirement.decode()
