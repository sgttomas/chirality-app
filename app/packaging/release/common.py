"""Shared pieces of the 4.0.0 release procedure; this module runs no command itself.

The build (build.py), the owner's signing run (owner_sign.py) and the package
identity record (record.py) share the release identity, the command runner
interface, the reading of Mach-O code signatures without Apple tools, the
parsing of `codesign` display output and the candidate description.
"""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import plistlib
import re
import struct
import subprocess
from xml.parsers.expat import ExpatError

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
VOLUME_NAME = 'Chirality'
MAIN_EXECUTABLE = 'chirality-app-v4'  # Cargo binary name; Tauri sets no mainBinaryName
APP_NAME = PRODUCT_NAME + '.app'
VENDOR_DESTINATION = 'Contents/Resources/codex'
LIMITATIONS_SOURCE = 'docs/RELEASE_LIMITATIONS_4.0.0.md'
LIMITATIONS_IN_BUNDLE = 'Contents/Resources/release/LIMITATIONS.md'
LIMITATIONS_IN_IMAGE = 'Release Limitations.md'
SUPPLIER_TEAM = inventory.SUPPLIER_TEAM
APP_ID_KEY = 'com.apple.application-identifier'
TEAM_KEY = 'com.apple.developer.team-identifier'
CANDIDATE_FORMAT = 'chirality-release-candidate/1'
CANDIDATE_FILE = 'CANDIDATE.json'


class Result:
    def __init__(self, returncode, stdout=b'', stderr=b''):
        self.returncode = returncode
        self.stdout = stdout if isinstance(stdout, bytes) else stdout.encode()
        self.stderr = stderr if isinstance(stderr, bytes) else stderr.encode()

    def text(self):
        return self.stdout.decode('utf-8', 'replace') + self.stderr.decode('utf-8', 'replace')


def system_runner(argv, *, env, cwd=None, timeout=None):
    """Run one argv (never a shell string) with exactly the given environment."""
    done = subprocess.run(list(argv), env=dict(env), cwd=cwd, capture_output=True, timeout=timeout, stdin=subprocess.DEVNULL)
    return Result(done.returncode, done.stdout, done.stderr)


def read_info_plist(app):
    raw = (Path(app) / 'Contents/Info.plist').read_bytes()
    value = plistlib.loads(raw)
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
            errors.append(f'Info.plist {key} is {identity[key]!r}, not {wanted!r}')
    if identity['executable'] != MAIN_EXECUTABLE:
        errors.append(f"Info.plist main executable is {identity['executable']!r}, not {MAIN_EXECUTABLE!r}")
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


def require_inside(path, root, what):
    """Every path a tool writes must be physically inside its own new output directory."""
    refuse_installed_location(path, what)
    require(prepare.identity(Path(os.path.realpath(root))) in physical_ancestry(Path(path).parent),
            f'{what} is not inside the output directory')


# --- One redaction path for everything written ------------------------------

CREDENTIAL_PATTERNS = [re.compile(p) for p in (
    r'\b[a-z]{4}-[a-z]{4}-[a-z]{4}-[a-z]{4}\b',                       # app-specific password shape
    r'-----BEGIN [A-Z0-9 ]+-----[\s\S]*?(?:-----END [A-Z0-9 ]+-----|$)',  # PEM material
    r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}',                 # an Apple account e-mail
    r'\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]+\.?[A-Za-z0-9_-]*',        # JSON web token
    r'(?i)["\']?\b(?:password|passwd|secret|api[_-]?key|private[_-]?key|token|apple[_-]?id|username)\b["\']?\s*[=:]\s*("[^"]*"|\'[^\']*\'|\S+)',
)]
TEAM_LIKE = re.compile(r'\b(?=[A-Z0-9]{10}\b)(?=[A-Z0-9]*[0-9])(?=[A-Z0-9]*[A-Z])[A-Z0-9]{10}\b')
SENSITIVE_KEY = re.compile(r'(?i)pass(?:word|wd)|secret|token|api[_-]?key|private[_-]?key|apple[_-]?id|user(?:name)?$|e-?mail|account|credential|issuer|key[_-]?id|provider')


class Redactor:
    """Removes credential-shaped text, account names and team identifiers other than the public ones.

    `allowed` strings (the identity name and the notary profile name, which the
    owner passes as arguments) are kept verbatim. `public_teams` are the team
    identifiers published in source: the compiled publisher team and the
    supplier's.
    """

    def __init__(self, allowed=(), public_teams=()):
        self.allowed = sorted({a for a in allowed if a}, key=len, reverse=True)
        self.public_teams = set(public_teams)

    def text(self, value):
        value = str(value)
        held = {}
        for index, allowed in enumerate(self.allowed):
            token = f'\x00{index}\x00'
            if allowed in value:
                value, held[token] = value.replace(allowed, token), allowed
        for pattern in CREDENTIAL_PATTERNS:
            value = pattern.sub('[redacted]', value)
        value = TEAM_LIKE.sub(lambda m: m.group(0) if m.group(0) in self.public_teams else '[redacted]', value)
        for token, allowed in held.items():
            value = value.replace(token, allowed)
        return value

    def json(self, value, structural=False):
        """Redacted copy of a JSON value. `structural` also blanks values under sensitive keys (external JSON)."""
        if isinstance(value, dict):
            return {self.text(k) if structural else k:
                    ('[redacted]' if structural and SENSITIVE_KEY.search(str(k)) else self.json(v, structural))
                    for k, v in value.items()}
        if isinstance(value, list):
            return [self.json(v, structural) for v in value]
        if isinstance(value, str):
            return self.text(value)
        return value


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


# --- codesign display output ----------------------------------------------

def parse_display(result):
    """Facts from `codesign -d --verbose=4 PATH` (written to standard error)."""
    lines = result.stderr.decode('utf-8', 'replace').splitlines()
    values, authorities = {}, []
    for line in lines:
        key, sep, value = line.partition('=')
        if not sep:
            continue
        if key == 'Authority':
            authorities.append(value)
        elif key == 'CodeDirectory v':
            values['code_directory'] = line
            values['flags'] = re.search(r'flags=(0x[0-9a-f]+)\(([^)]*)\)', line)
        elif key not in values:
            values[key] = value
    flags = values.pop('flags', None)
    flag_value = int(flags.group(1), 16) if flags else None
    flag_names = flags.group(2).split(',') if flags else []
    return {'returncode': result.returncode, 'identifier': values.get('Identifier'), 'team': values.get('TeamIdentifier'),
            'authorities': authorities, 'timestamp': values.get('Timestamp'), 'cdhash': values.get('CDHash'),
            'flags': flag_value, 'flag_names': flag_names,
            'runtime': flag_value is not None and bool(flag_value & CS_RUNTIME) and 'runtime' in flag_names,
            'adhoc': flag_value is None or bool(flag_value & CS_ADHOC) or 'adhoc' in flag_names,
            'unsigned': 'code object is not signed at all' in result.stderr.decode('utf-8', 'replace').lower()}


def parse_entitlements(result):
    """Entitlements from `codesign -d --entitlements - --xml PATH`; None when unreadable."""
    if result.returncode != 0 or not result.stdout.strip():
        return None  # empty output is not an empty entitlement set
    try:
        value = plistlib.loads(result.stdout)
    except (plistlib.InvalidFileException, ExpatError, ValueError):
        return None
    return value if isinstance(value, dict) else None


def display_argv(path):
    return ['/usr/bin/codesign', '-d', '--verbose=4', str(path)]


def entitlements_argv(path):
    return ['/usr/bin/codesign', '-d', '--entitlements', '-', '--xml', str(path)]


def plain(value):
    """JSON-safe copy of a property-list value (dates and data become text)."""
    if isinstance(value, dict):
        return {str(k): plain(v) for k, v in value.items()}
    if isinstance(value, list):
        return [plain(v) for v in value]
    if isinstance(value, bytes):
        return {'sha256': sha(value)}
    if hasattr(value, 'isoformat'):
        return value.isoformat()
    return value


# --- candidate description -------------------------------------------------

def tree_entries(tree):
    """Inventory entries without the absolute root, for records."""
    return {'root_mode': tree['root_mode'], 'manifest_sha256': tree['manifest_sha256'], 'files': tree['files'],
            'macho_files': tree['macho_files'], 'entries': tree['entries']}


def tree_equal(actual, recorded):
    return inventory.compare(actual, recorded)


def macho_paths(tree):
    return [e['path'] for e in tree['entries'] if e.get('macho')]


def write_json_new(path, value, mode=0o644, redactor=None):
    if redactor is not None:
        value = redactor.json(value)
    raw = (json.dumps(value, indent=2, sort_keys=True) + '\n').encode()
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, mode)
    with os.fdopen(fd, 'wb') as output:
        output.write(raw); output.flush(); os.fsync(output.fileno())
    os.chmod(path, mode)
    return sha(raw)


def load_candidate(candidate):
    """Read and verify a candidate description against the bytes it describes.

    Returns (description, app path). Any difference refuses: the owner's step
    may only act on exactly what the build described.
    """
    candidate = inventory.anchored(candidate)
    refuse_installed_location(candidate, 'candidate')
    for marker in ('INCOMPLETE.txt', 'BUILD_FAILED.json', 'BUILD_REFUSED.json'):
        require(not os.path.lexists(candidate / marker), 'the build did not finish: ' + marker + ' is present')
    raw = (candidate / CANDIDATE_FILE).read_bytes()
    value = parse(raw)
    require(value.get('format') == CANDIDATE_FORMAT, 'unknown candidate description format')
    app = candidate / prepare.files.relative(value['bundle']['path'])
    require(app.name == APP_NAME and app.is_dir() and not app.is_symlink(), 'candidate App bundle missing')
    tree = inventory.scan(app)
    compared = inventory.compare(tree, value['bundle']['inventory'])
    require(compared['equal'], 'candidate App differs from its description: ' + json.dumps(
        {k: compared[k][:5] for k in ('differing', 'missing', 'extra')} | {'root_mode_equal': compared['root_mode_equal']}))
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
    for name in ('binding', 'requirement', 'projection'):
        file = publisher[name]
        require(sha((candidate / prepare.files.relative(file['path'])).read_bytes()) == file['sha256'],
                'candidate publisher output changed: ' + name)
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
