"""Shared pieces of the 4.0.0 release procedure; this module runs no command itself.

The build (build.py), the owner's signing run (owner_sign.py) and the package
identity record (record.py) share:

- the release identity and the candidate description;
- the closed list of failure reasons (REASONS), the only text a STOP carries;
- the one rule for observations (`observe`), with each observation's required
  fields declared as data in OBSERVATIONS;
- selection: every value a returnable file holds is constructed by the tool or
  selected from tool output and validated against a stated shape;
- the two writers: `write_returnable` (validated JSON, the only content of the
  files that are sent back) and `PrivateWriter` (raw tool output and traces,
  written and never read back);
- location checks by filesystem identity;
- the reading of Mach-O code signatures without Apple tools.
"""
import datetime
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import plistlib
import re
import stat
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

def _steps(numbers, code, text):
    return {f'S{n}_{code}': f'step {n}: ' + text.format(**kw) for n, kw in numbers}


REASONS = {
    'REFUSED_HOST': 'refused: this host is not Apple Silicon macOS',
    'REFUSED_ENVIRONMENT': 'refused: Apple, Tauri signing or notary variables are set in the environment; the keychain supplies everything',
    'REFUSED_IDENTITY_PATH': 'refused: --identity is a path, not the name of a signing identity',
    'REFUSED_IDENTITY_FORM': 'refused: --identity is not of the form "Developer ID Application: <name> (<TEAMID>)"',
    'REFUSED_IDENTITY_CREDENTIAL': 'refused: --identity looks like a credential',
    'REFUSED_NOTARY_PROFILE': 'refused: --notary-profile is not a keychain profile name (letters, digits, . _ -)',
    'REFUSED_PROFILE_DIGEST_FORM': 'refused: --profile-sha256 is not 64 lowercase hexadecimal digits',
    'REFUSED_ARGUMENT_CREDENTIAL': 'refused: a path argument looks like a credential or a key file',
    'REFUSED_LOCATION': 'refused: --candidate or --out is inside /Applications, /System/Applications or ~/Library',
    'REFUSED_OUT_EXISTS': 'refused: --out already exists; give a new folder',
    'REFUSED_OUT_PARENT': 'refused: the folder that would hold --out does not exist',
    'REFUSED_CANDIDATE': 'refused: the candidate does not verify against CANDIDATE.json, or its build did not finish',
    'REFUSED_TEAM': 'refused: the identity names a team other than the candidate\'s compiled publisher team',
    'REFUSED_LIMITATIONS': 'refused: --limitations is not the candidate source\'s release limitations file',
    'REFUSED_PROFILE_BYTES': 'refused: the provisioning profile\'s bytes differ from --profile-sha256',
    'S0_NO_MACHO': 'step 0: the supplier\'s tree holds no Mach-O file',
    'S0_SIGNATURE': ('step 0: a supplier executable\'s signature display lacks a required field, or shows another signer or team, '
                     'no hardened runtime or no timestamp; re-signing is not part of the arrangement (DEL-01-06 CLM-002), so the pin returns to the owner'),
    'S0_ENTITLEMENTS': ('step 0: a supplier executable\'s entitlements could not be read or include get-task-allow; '
                        're-signing is not part of the arrangement (DEL-01-06 CLM-002), so the pin returns to the owner'),
    'S1_COPY': 'step 1: the working copy of the App differs from the candidate in bytes, modes or types',
    'S2_PROFILE': 'step 2: the provisioning profile is not a current Developer ID profile granting the publisher App ID and team',
    'S2_PLACED': 'step 2: the placed profile is not mode 0644 with the selected digest',
    'S3_APP_ID': 'step 3: the profile grants another application identifier than the publisher binding derives',
    'S4_SIGN': 'step 4: codesign did not sign the App',
    'S6_ARCHIVE': 'step 6: ditto did not archive the App for submission',
    'S6_ARCHIVE_CHANGED': 'step 6: archiving the App for submission changed the App',
    'S7_ONLY_TICKET': 'step 7: stapling changed the App beyond adding its ticket at Contents/CodeResources',
    'S7_VENDOR': 'step 7: stapling changed the supplier\'s tree inside the App',
    'S9_CREATE': 'step 9: hdiutil did not create the disk image',
    'S9_SIGN': 'step 9: codesign did not sign the disk image',
    'S9_VERIFY': 'step 9: codesign did not report the disk image\'s signature valid',
    'S9_DISPLAY': 'step 9: the disk image\'s signature display lacks a required field, the given identity, the team or a timestamp',
    'S9_APP_CHANGED': 'step 9: the stapled App changed while the disk image was made',
    'S12_OPEN': 'step 12: Gatekeeper did not report the disk image as accepted from Notarized Developer ID',
    'S12_ATTACH': 'step 12: the disk image did not mount read-only',
    'S12_MOUNTED': 'step 12: the App in the mounted disk image differs from the stapled App',
    'S12_LIMITATIONS': 'step 12: the limitations file in the disk image differs from the candidate source',
    'S12_EXEC': 'step 12: Gatekeeper did not report the mounted App as accepted from Notarized Developer ID',
    'S12_DETACH': 'step 12: the disk image did not detach; detach it with hdiutil detach',
    'S13_ATTACH': 'step 13: the disk image did not mount read-only for the record',
    'S13_OBSERVATION': 'step 13: an observation the record states failed; no record was written',
    'S13_DETACH': 'step 13: the disk image did not detach; no record was written; detach it with hdiutil detach',
    'GUARD_SIGNING': 'guard: a signing call other than the one on the App and the one on the disk image was refused',
    'REFUSED_UNREADABLE': 'refused: an argument file or the candidate could not be read; nothing ran',
    'INTERRUPTED': 'interrupted: the run was interrupted; nothing ran after the interruption',
    'BUILD_HOST': 'build: this host is not Apple Silicon macOS',
    'BUILD_OUT': 'build: --out exists, or the folder that would hold it does not, or it is inside /Applications or ~/Library',
    'BUILD_ENVIRONMENT': 'build: the caller environment is not exactly PATH and LANG with single-line values and absolute PATH entries',
    'BUILD_TOOLS': 'build: the resolved rustc, cargo, clang and ld are not all given, or rustc or cargo on PATH is not the given one or is a rustup proxy',
    'BUILD_PUBLISHER_PAIR': 'build: the publisher input file and its digest were not given together',
    'BUILD_NODE_MODULES': 'build: the source export holds node_modules; dependencies come from the npm cache',
    'BUILD_CARGO_CACHE': 'build: the Cargo cache input holds configuration or credentials',
    'BUILD_LINK': 'build: the Cargo or npm cache holds a symbolic link, or a link in the source export leaves it',
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
STEP_NAMES = {0: 'reading the supplier signatures', 1: 'copying the App', 2: 'placing the profile', 3: 'writing the entitlements',
              4: 'signing the App', 5: 'verifying the signed App', 6: 'notarizing the App', 7: 'stapling the App',
              8: 'verifying the stapled App', 9: 'making the disk image', 10: 'notarizing the disk image',
              11: 'stapling the disk image', 12: 'the Gatekeeper assessments', 13: 'reading the package for the record'}
BUILD_STAGES = {'INPUTS': 'reading the inputs', 'COPY': 'copying the inputs', 'PLAN': 'preparing the plan', 'ENVIRONMENT': 'preparing the build environment',
                'INSTALL': 'the offline dependency install', 'RUN': 'the recipe build', 'CHECKS': 'checking the built bundle',
                'PUBLISH': 'publishing the candidate'}
for _number, _name in STEP_NAMES.items():
    REASONS[f'S{_number}_UNEXPECTED'] = f'step {_number}: an error no check covers while {_name}; the private folder holds the trace'
for _stage, _name in BUILD_STAGES.items():
    REASONS[f'BUILD_UNEXPECTED_{_stage}'] = f'build: an error no check covers during {_name}; the private folder holds the trace'
for _number, _subject in ((5, 'signed App'), (8, 'stapled App')):
    REASONS.update({
        f'S{_number}_DEEP': f'step {_number}: codesign did not report the {_subject} valid on deep strict verification',
        f'S{_number}_REQUIREMENT': f'step {_number}: codesign did not report the {_subject} as satisfying the compiled publisher requirement',
        f'S{_number}_DISPLAY': f'step {_number}: the {_subject}\'s signature display lacks a required field',
        f'S{_number}_SIGNER': f'step {_number}: the {_subject}\'s signature lacks hardened runtime, a timestamp, the given identity, the team or the identifier',
        f'S{_number}_ENTITLEMENTS': f'step {_number}: the {_subject}\'s entitlements are not exactly the two expected keys',
        f'S{_number}_INVENTORY': (f'step {_number}: the {_subject} changed beyond the main executable, _CodeSignature, the profile'
                                  + (' and its ticket' if _number == 8 else '')),
        f'S{_number}_VENDOR': f'step {_number}: the supplier\'s tree inside the {_subject} changed',
        f'S{_number}_CDHASH': f'step {_number}: a supplier executable\'s code-directory hash in the {_subject} changed or could not be read',
    })
for _number, _subject in ((6, 'App archive'), (10, 'disk image')):
    REASONS.update({
        f'S{_number}_SUBMIT': f'step {_number}: notarytool submit of the {_subject} returned no submission identifier and status in the expected form',
        f'S{_number}_STATUS': f'step {_number}: the notarization status of the {_subject} is not Accepted; nothing was stapled',
        f'S{_number}_LOG': f'step {_number}: the notarization log of the {_subject} could not be fetched or lacks a required field; nothing was stapled',
        f'S{_number}_LOG_STATUS': f'step {_number}: the notarization log of the {_subject} is not Accepted; nothing was stapled',
        f'S{_number}_ISSUES': f'step {_number}: the notarization log of the {_subject} does not state an empty issues list; nothing was stapled',
        f'S{_number}_DIGEST': f'step {_number}: the notarization log names a digest other than the submitted {_subject}\'s; nothing was stapled',
        f'S{_number}_JOB': f'step {_number}: the notarization log names another submission than the {_subject}\'s; nothing was stapled',
    })
for _number, _subject in ((7, 'the App'), (11, 'the disk image')):
    REASONS.update({
        f'S{_number}_STAPLE': f'step {_number}: stapler did not report stapling {_subject}',
        f'S{_number}_VALIDATE': f'step {_number}: stapler did not report {_subject}\'s ticket valid',
    })


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
    'timestamp': r'[A-Z][a-z]{2} \d{1,2}, \d{4} at \d{1,2}:\d{2}:\d{2}(?: [AP]M)?',
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


def select_team(value, public_teams):
    """A team identifier is recorded only when it is one published in source; otherwise the word 'other'."""
    return value if value in public_teams else 'other'


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


def select_entitlements(value, public_teams):
    """(selected entitlements, count of unexpected keys or values). Free text never passes."""
    if not isinstance(value, dict):
        return None, 0
    chosen, unexpected = {}, 0
    def app_id(text):
        match = isinstance(text, str) and len(text) <= 255 and APP_ID.fullmatch(text)
        return text if match and match.group(1) in public_teams else None
    for key, item in value.items():
        kind = KNOWN_ENTITLEMENTS.get(key)
        if kind is bool and isinstance(item, bool):
            chosen[key] = item
        elif kind == 'team' and isinstance(item, str) and item in public_teams:
            chosen[key] = item
        elif kind == 'app_id' and app_id(item):
            chosen[key] = item
        elif kind == 'app_id_list' and isinstance(item, list) and item and all(app_id(i) for i in item):
            chosen[key] = list(item)
        else:
            unexpected += 1
    return chosen, unexpected


# --- The one rule for observations --------------------------------------------
# An observation counts only when:
#   1. its command returned zero;
#   2. its output names the object asked about wherever the output carries a path, and names no
#      other object (a bundle's own nested code inside it is the same object);
#   3. it is unambiguous: no field appears twice with different values, JSON output has no
#      duplicate key, and an assessment has exactly one source;
#   4. every required field is present with a value of its expected form;
#   5. it holds the positive form its declaration requires and no negative marker.
# OBSERVATIONS declares each observation as data; `observe` is the only function that applies the rule.

NEGATIVE = re.compile(r'(?i)\b(?:rejected|not accepted|denied|invalid|error|failed|failure|not signed|does not|unnotarized|'
                      r'no ticket|unable|cannot|could not|not satisfy|not valid|modified|revoked|malformed|truncated|corrupt)\b')
OBSERVATIONS = {
    # codesign -d --verbose=4: key=value lines on standard error; Executable names the object.
    'signature': {'format': 'lines', 'fields': {
        'identifier': ('Identifier', SHAPES['identifier']),
        'team': ('TeamIdentifier', r'[A-Z0-9]{10}'),
        'cdhash': ('CDHash', SHAPES['cdhash']),
        'code_directory': ('CodeDirectory v', r'\d+ size=\d+ flags=0x[0-9a-f]+\([a-z,-]*\).*'),
        'timestamp': ('Timestamp', SHAPES['timestamp']),
        'authority': ('Authority', r'(?:Developer ID Application: .+ \([A-Z0-9]{10}\)|Developer ID Certification Authority|Apple Root CA)'),
    }},
    # codesign -d --entitlements - --xml: one property list dictionary on standard output; Executable on standard error.
    'entitlements': {'format': 'plist'},
    'verify': {'format': 'text', 'subject_messages': ['valid on disk']},
    'requirement': {'format': 'text', 'subject_messages': ['valid on disk', 'explicit requirement satisfied']},
    'assessment': {'format': 'text', 'subject_messages': ['accepted'], 'single': ('source', 'Notarized Developer ID'), 'ignore': ('origin=',)},
    'staple': {'format': 'text', 'processing': True, 'phrases': ['The staple and validate action worked!']},
    'validate': {'format': 'text', 'processing': True, 'phrases': ['The validate action worked!']},
    'dyld_validate': {'format': 'text'},
    'submit': {'format': 'json', 'fields': {'id': ('id', SHAPES['uuid']), 'status': ('status', None)}},
    'notary_log': {'format': 'json', 'fields': {'job': ('jobId', SHAPES['uuid']), 'status': ('status', None), 'sha256': ('sha256', SHAPES['sha256'])},
                   'keys': ('issues',)},
}


class ObservationFailed(ValueError):
    def __init__(self, name, missing):
        super().__init__(f'observation {name} failed')
        self.name, self.missing = name, missing


def _same(reported, subject):
    return reported == str(subject) or os.path.realpath(reported) == os.path.realpath(str(subject))


def _inside(reported, subject):
    """The object asked about, or (for a bundle) its own nested code."""
    if _same(reported, subject):
        return True
    root = os.path.realpath(str(subject))
    return str(subject).endswith('.app') and os.path.realpath(reported).startswith(root + os.sep)


def _executable_matches(reported, subject):
    return _same(reported, subject) or (str(subject).endswith('.app') and _same(reported, Path(subject) / 'Contents/MacOS' / MAIN_EXECUTABLE))


def _reported_path(line):
    """(path, message) when the line reports about a path, else (None, line)."""
    for prefix in ('Processing: ', '--prepared:', '--validated:'):
        if line.startswith(prefix):
            return line[len(prefix):], ''
    if line.startswith('/'):
        path, sep, message = line.rpartition(': ')
        return (path, message) if sep else (line, '')
    return None, line


def _unique_json(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise ValueError('duplicate key')
        value[key] = item
    return value


def _lines(stream, failures, subject):
    """key=value lines: a key that repeats with a different value is ambiguous (Authority is the chain)."""
    found, authorities = {}, []
    for line in stream.decode('utf-8', 'replace').splitlines():
        key, sep, item = line.partition('=')
        if not sep:
            continue
        if key == 'Authority':
            authorities.append(item)
        elif key in found and found[key] != item:
            failures.append('ambiguous ' + key)
        else:
            found[key] = item
    if subject is not None and not ('Executable' in found and _executable_matches(found['Executable'], subject)):
        failures.append('another or no object named')
    return found, authorities


def observe(name, result, subject=None):
    """Apply the one rule to one command result about `subject`. Returns the parsed fields; raises ObservationFailed."""
    spec = OBSERVATIONS[name]
    failures = []
    if spec['format'] != 'json' and subject is None:
        raise ObservationFailed(name, ['no object asked about'])
    if result.returncode != 0:
        raise ObservationFailed(name, ['return code'])
    if spec['format'] == 'text':
        lines = [l for l in result.text().splitlines() if l.strip() and not l.startswith(spec.get('ignore', ()) or ('\0',))]
        about_subject, messages = [], []
        for line in lines:
            path, message = _reported_path(line)
            if path is not None:
                if subject is None or not _inside(path, subject):
                    failures.append('another object named')
                elif _same(path, subject):
                    about_subject.append(message)
                if line.startswith('Processing: ') and subject is not None and _same(path, subject):
                    about_subject.append('processing')
            messages.append(message)
        for message in spec.get('subject_messages', []):
            if message not in about_subject:
                failures.append('missing: ' + message)
        if spec.get('processing') and 'processing' not in about_subject:
            failures.append('missing: processing line for the object')
        for phrase in spec.get('phrases', []):
            if phrase not in messages:
                failures.append('missing: ' + phrase)
        if 'single' in spec:
            key, wanted = spec['single']
            sources = [m for m in messages if m.startswith(key + '=')]
            if sources != [key + '=' + wanted]:
                failures.append('not exactly one ' + key)
        if any(NEGATIVE.search(m) for m in messages):
            failures.append('negative marker present')
        if failures:
            raise ObservationFailed(name, failures)
        return {}
    if spec['format'] == 'plist':
        if subject is not None:
            _lines(result.stderr, failures, subject)
        try:
            value = plistlib.loads(result.stdout) if result.stdout.strip() else None
        except (plistlib.InvalidFileException, ExpatError, ValueError):
            value = None
        if not isinstance(value, dict):
            failures.append('property list dictionary')
        if failures:
            raise ObservationFailed(name, failures)
        return value
    if spec['format'] == 'json':
        try:
            value = json.loads(result.stdout, object_pairs_hook=_unique_json)
        except ValueError:
            value = None
        if not isinstance(value, dict):
            raise ObservationFailed(name, ['one JSON object without duplicate keys'])
        fields = {}
        for field, (key, pattern) in spec['fields'].items():
            item = value.get(key)
            ok = item in STATUS_WORDS if pattern is None else isinstance(item, str) and re.fullmatch(pattern, item) is not None
            if ok:
                fields[field] = item
            else:
                failures.append(field)
        for key in spec.get('keys', ()):
            if key not in value:
                failures.append(key)
        if 'issues' in spec.get('keys', ()) and 'issues' in value:
            issues = value['issues']
            if issues is None or isinstance(issues, list):
                fields['issue_count'] = 0 if issues is None else len(issues)
            else:
                failures.append('issues')
        if failures:
            raise ObservationFailed(name, failures)
        return fields
    # 'lines': codesign display on standard error.
    found, authorities = _lines(result.stderr, failures, subject)
    found['Authority'] = authorities[0] if authorities else None
    fields = {}
    for field, (key, pattern) in spec['fields'].items():
        item = found.get(key)
        if isinstance(item, str) and re.fullmatch(pattern, item):
            fields[field] = item
        else:
            failures.append(field)
    if failures:
        raise ObservationFailed(name, failures)
    flags = re.search(r'flags=(0x[0-9a-f]+)\(([a-z,-]*)\)', fields['code_directory'])
    fields['flags'] = int(flags.group(1), 16)
    fields['flag_names'] = [n for n in flags.group(2).split(',') if n]
    fields['runtime'] = bool(fields['flags'] & CS_RUNTIME) and 'runtime' in fields['flag_names']
    fields['adhoc'] = bool(fields['flags'] & CS_ADHOC) or 'adhoc' in fields['flag_names']
    leaf = re.fullmatch(r'Developer ID Application: (.+) \(([A-Z0-9]{10})\)', fields['authority'])
    fields['signer_kind'] = 'Developer ID Application' if leaf else fields['authority']
    fields['signer_team'] = leaf.group(2) if leaf else None
    fields['leaf_authority'] = fields['authority']  # compared in memory only; never recorded
    return fields


def signature_facts(fields, public_teams, identity=None):
    """The recordable selection of an observed signature."""
    return {'identifier': fields['identifier'], 'team': select_team(fields['team'], public_teams), 'cdhash': fields['cdhash'],
            'flags': fields['flags'], 'runtime': fields['runtime'], 'adhoc': fields['adhoc'], 'timestamp': fields['timestamp'],
            'signer': fields['signer_kind'], 'signer_team': select_team(fields['signer_team'], public_teams),
            **({'signer_is_given_identity': fields['leaf_authority'] == identity} if identity is not None else {})}


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
        finally:
            os.close(fd)
        return path


# --- Info.plist and locations ---------------------------------------------------

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


def display_argv(path):
    return ['/usr/bin/codesign', '-d', '--verbose=4', str(path)]


def entitlements_argv(path):
    return ['/usr/bin/codesign', '-d', '--entitlements', '-', '--xml', str(path)]


def plain_datetime(value):
    if isinstance(value, datetime.datetime):
        return value.replace(microsecond=0).isoformat() + ('' if value.tzinfo else 'Z')
    return None


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
