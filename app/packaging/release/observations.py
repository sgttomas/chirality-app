"""The one rule for observations of Apple's tools, with every output form declared as data.

The rule. A command's output is an observation only when:
  1. the command returned zero;
  2. every line of its output, on each stream, is of a form declared below for that command
     (blank lines carry nothing and are allowed); nothing is selected from undeclared text, and
     nothing is concluded from the absence of a failure message;
  3. no property list or JSON it parses has a key twice, and no form that may appear once appears
     twice;
  4. every form that carries a required fact is present, with a value of its declared shape;
  5. where a form carries a path, the path is the object asked about (the single assessment source
     and the object binding of the earlier rounds are part of the declared forms).
Anything else is no observation, and the caller stops with a fixed reason naming its step.

Sources. Every form names where it was taken from. Only the tools' published documentation and real
outputs retained in this repository are used; no tool was run to produce or display a form.
  TN3126  Apple, "TN3126: Inside Code Signing: Hashes" (codesign --display -vvv listings)
  TN3127  Apple, "TN3127: Inside Code Signing: Requirements" (codesign --verify -v -R listings)
  TN3161  Apple, "TN3161: Inside Code Signing: Certificates" (Authority chain, Timestamp, Signed Time)
  TN3125  Apple, "TN3125: Inside Code Signing: Provisioning Profiles" (--entitlements - --xml output)
  NOTARY  Apple, "Customizing the notarization workflow" (notarytool submit --wait and log output, log JSON)
  WITNESS app/examination/native_support/signed_witness_collect.sh, which reads real codesign and
          spctl output with grep for ^Identifier=, ^TeamIdentifier=, ^CDHash= and source=Notarized Developer ID
  ADVANCE app/src-tauri/resources/distribution-reference/VERSION_ADVANCE_0.160.0.md (codesign --verify messages)
  RUN1103 the 2026-11-03 signing and notarization records, retained in Git history
          (git show 8560ac2e^:execution/PKG-01/DEL-01-06/Work/selected-production-build/f664ee1d-caec11a00be3/*.json):
          "The staple and validate action worked!", "The validate action worked!", "valid on disk; satisfies its
          Designated Requirement", "accepted, source=Notarized Developer ID", Sealed Resources version/rules/files,
          and the notarization log fields statusCode and sha256.
A line the real tools print that no source shows (for example a line naming the executable, or a
progress line) is not declared, so a first real run may stop on it. The owner's page says what
happens then.
"""
import importlib.util
import json
import os
from pathlib import Path
import plistlib
import re
import sys
from xml.parsers.expat import ExpatError


def sibling(name):
    key = 'chirality_release_' + name
    if key not in sys.modules:
        spec = importlib.util.spec_from_file_location(key, Path(__file__).resolve().parent / (name + '.py'))
        module = importlib.util.module_from_spec(spec); sys.modules[key] = module; spec.loader.exec_module(module)
    return sys.modules[key]


common = sibling('common')

UUID = r'[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}'
STATUS = r'Accepted|Invalid|Rejected|In Progress'
SUBJECT = object()  # a form whose path group must be the object asked about
BASENAME = object()  # a form whose value must be the object's file name

# Each form: (name, regular expression for the whole line, kind, may repeat, source).
# Kinds: 'fact' carries a required fact; 'known' is an optional known field; 'noise' is known and carries nothing.
FORMS = {
    # codesign -d --verbose=3 PATH: key=value lines on standard error, nothing on standard output.
    'signature': {'stdout': [], 'stderr': [
        ('identifier', r'Identifier=(?P<value>[A-Za-z0-9](?:[A-Za-z0-9._-]{0,253}[A-Za-z0-9])?)', 'fact', False, 'WITNESS'),
        ('format', r'Format=.{1,200}', 'noise', False, 'TN3126'),
        ('code_directory', r'CodeDirectory v=\d+ size=\d+ flags=(?P<value>0x[0-9a-f]+\([a-z,-]*\)) hashes=\d+\+\d+ location=embedded',
         'fact', False, 'TN3126'),
        ('hash_type', r'Hash type=sha256 size=32', 'noise', False, 'TN3126'),
        ('candidate_cdhash', r'CandidateCDHash sha(?:1|256)=[0-9a-f]{40}', 'noise', True, 'TN3126'),
        ('candidate_cdhash_full', r'CandidateCDHashFull (?:sha1=[0-9a-f]{40}|sha256=[0-9a-f]{64})', 'noise', True, 'TN3126'),
        ('hash_choices', r'Hash choices=sha(?:1|256)(?:,sha256)?', 'noise', False, 'TN3126'),
        ('cdhash', r'CDHash=(?P<value>[0-9a-f]{40})', 'fact', False, 'TN3126, WITNESS'),
        ('authority', r'Authority=(?P<value>Developer ID Application: .{1,200} \([A-Z0-9]{10}\)|Developer ID Certification Authority|Apple Root CA)',
         'fact', True, 'TN3161'),
        ('timestamp', r'Timestamp=(?P<value>' + common.SHAPES['timestamp'] + ')', 'fact', False, 'TN3161'),
        ('signed_time', r'Signed Time=.{1,60}', 'known', False, 'TN3161 (present instead of Timestamp when there is no secure timestamp)'),
        ('team', r'TeamIdentifier=(?P<value>[A-Z0-9]{10})', 'fact', False, 'WITNESS'),
        ('sealed_resources', r'Sealed Resources version=\d+ rules=\d+ files=\d+', 'noise', False, 'RUN1103'),
    ]},
    # codesign -d --entitlements - --xml PATH: one XML property list on standard output, nothing on standard error.
    'entitlements': {'stdout': 'xml-plist', 'stderr': [], 'source': 'TN3125'},
    # codesign --verify --strict --verbose=1 PATH (and --deep): one line per message about the object.
    'verify': {'either': [
        ('valid', r'(?P<path>.+): valid on disk', 'fact', False, 'TN3127 (path: message form), ADVANCE, RUN1103'),
        ('designated', r'(?P<path>.+): satisfies its Designated Requirement', 'known', False, 'ADVANCE, RUN1103'),
    ]},
    'requirement': {'either': [
        ('valid', r'(?P<path>.+): valid on disk', 'fact', False, 'TN3127 (path: message form), ADVANCE, RUN1103'),
        ('designated', r'(?P<path>.+): satisfies its Designated Requirement', 'known', False, 'ADVANCE, RUN1103'),
        ('explicit', r'(?P<path>.+): explicit requirement satisfied', 'fact', False, 'TN3127'),
    ]},
    # spctl -a -t open|exec -v PATH
    'assessment': {'either': [
        ('accepted', r'(?P<path>.+): accepted', 'fact', False, 'RUN1103'),
        ('source', r'source=Notarized Developer ID', 'fact', False, 'WITNESS, RUN1103'),
    ]},
    # xcrun stapler staple|validate PATH
    'staple': {'either': [('worked', r'The staple and validate action worked!', 'fact', False, 'RUN1103')]},
    'validate': {'either': [('worked', r'The validate action worked!', 'fact', False, 'RUN1103')]},
    # xcrun notarytool submit PATH --keychain-profile NAME --wait (text output)
    'submit': {'either': [
        ('uploaded', r'Successfully uploaded file\.', 'fact', False, 'NOTARY'),
        ('upload_id', r' id: (?P<value>' + UUID + ')', 'fact', False, 'NOTARY'),
        ('upload_path', r' path: (?P<path>.+)', 'fact', False, 'NOTARY'),
        ('created', r'createdDate: \d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z', 'known', False, 'NOTARY'),
        ('id', r'id: (?P<value>' + UUID + ')', 'fact', False, 'NOTARY'),
        ('name', r'name: (?P<name>.+)', 'fact', False, 'NOTARY'),
        ('status', r'status: (?P<value>' + STATUS + ')', 'fact', False, 'NOTARY'),
    ]},
    # xcrun notarytool log ID --keychain-profile NAME FILE (text output; the log is written to FILE)
    'log': {'either': [
        ('downloaded', r'Successfully downloaded submission log', 'fact', False, 'NOTARY'),
        ('id', r' id: (?P<value>' + UUID + ')', 'fact', False, 'NOTARY'),
        ('location', r' location: (?P<path>.+)', 'fact', False, 'NOTARY'),
    ]},
}
# The notarization log file: every key declared; value kinds as data.
LOG_KEYS = {
    'archiveFilename': ('str', 'NOTARY'), 'issues': ('issues', 'NOTARY'), 'jobId': ('uuid', 'NOTARY'),
    'logFormatVersion': ('int', 'NOTARY'), 'status': ('status', 'NOTARY'), 'statusSummary': ('str', 'NOTARY'),
    'ticketContents': ('list_or_null', 'NOTARY'), 'uploadDate': ('str', 'NOTARY'),
    'statusCode': ('int', 'RUN1103'), 'sha256': ('sha256', 'RUN1103'),
}
LOG_REQUIRED = ('jobId', 'status', 'issues', 'sha256')
ISSUE_KEYS = {'message', 'path', 'severity'}  # NOTARY


# The commands whose output is read, and the selection of what may be recorded from it.
def display_argv(path):
    return ['/usr/bin/codesign', '-d', '--verbose=3', str(path)]


def entitlements_argv(path):
    return ['/usr/bin/codesign', '-d', '--entitlements', '-', '--xml', str(path)]


def select_team(value, public_teams):
    """A team identifier is recorded only when it is one published in source; otherwise the word 'other'."""
    return value if value in public_teams else 'other'


def select_entitlements(value, public_teams):
    """(selected entitlements, count of unexpected keys or values). Free text never passes."""
    if not isinstance(value, dict):
        return None, 0
    chosen, unexpected = {}, 0
    def app_id(text):
        match = isinstance(text, str) and len(text) <= 255 and common.APP_ID.fullmatch(text)
        return text if match and match.group(1) in public_teams else None
    for key, item in value.items():
        kind = common.KNOWN_ENTITLEMENTS.get(key)
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


class ObservationFailed(ValueError):
    def __init__(self, name, why):
        super().__init__(f'no observation: {name}')
        self.name, self.why = name, why


def unique_pairs(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise ValueError('a key appears twice')
        value[key] = item
    return value


class _UniqueDict(dict):
    def __setitem__(self, key, value):
        if key in self:
            raise ValueError('a key appears twice')
        super().__setitem__(key, value)


def load_xml_plist(raw):
    """One XML property list whose dictionaries have no key twice (plistlib alone keeps the last)."""
    if not raw.lstrip().startswith(b'<?xml'):
        raise ValueError('not an XML property list')
    try:
        return plistlib.loads(raw, fmt=plistlib.FMT_XML, dict_type=_UniqueDict)
    except (plistlib.InvalidFileException, ExpatError) as error:
        raise ValueError('not one XML property list') from error


def _same(reported, subject):
    return reported == str(subject) or os.path.realpath(reported) == os.path.realpath(str(subject))


def _match_lines(name, lines, forms, subject, found, why):
    for line in lines:
        line = line.rstrip()
        if not line.strip():
            continue  # a blank line carries nothing
        for form, pattern, kind, repeats, _ in forms:
            match = re.fullmatch(pattern, line)
            if match:
                break
        else:
            why.append('a line of an undeclared form')
            continue
        values = match.groupdict()
        if 'path' in values and (subject is None or not _same(values['path'], subject)):
            why.append('another object named')
        if 'name' in values and (subject is None or values['name'] != Path(str(subject)).name):
            why.append('another object named')
        if form in found and not repeats:
            why.append('a form appears twice: ' + form)
        found.setdefault(form, []).append(values.get('value'))


def observe(name, result, subject=None):
    """Apply the rule to one command result about `subject`; returns the facts; raises ObservationFailed."""
    spec = FORMS[name]
    why = []
    if result.returncode != 0:
        raise ObservationFailed(name, ['return code'])
    stdout, stderr = result.stdout.decode('utf-8', 'replace'), result.stderr.decode('utf-8', 'replace')
    found = {}
    if 'either' in spec:
        _match_lines(name, stdout.splitlines() + stderr.splitlines(), spec['either'], subject, found, why)
        forms = spec['either']
    else:
        if spec['stdout'] == 'xml-plist':
            try:
                value = load_xml_plist(result.stdout)
                if not isinstance(value, dict):
                    why.append('not a dictionary')
            except ValueError:
                why.append('not one XML property list without duplicate keys')
                value = None
        else:
            _match_lines(name, stdout.splitlines(), spec['stdout'], subject, found, why)
        _match_lines(name, stderr.splitlines(), spec['stderr'], subject, found, why)
        forms = spec['stderr'] if spec['stdout'] == 'xml-plist' else spec['stdout'] + spec['stderr']
        if spec['stdout'] == 'xml-plist':
            if why:
                raise ObservationFailed(name, why)
            return dict(value)
    for form, _, kind, _, _ in forms:
        if kind == 'fact' and form not in found:
            why.append('missing: ' + form)
    if why:
        raise ObservationFailed(name, why)
    return getattr(sys.modules[__name__], '_facts_' + name, lambda f: f)(found)


def _facts_signature(found):
    authorities = found['authority']
    leaves = [a for a in authorities if a.startswith('Developer ID Application: ')]
    chain = [a for a in authorities if not a.startswith('Developer ID Application: ')]
    # Exactly one leaf, first; each authority of the chain at most once.
    if len(leaves) != 1 or authorities[0] != leaves[0] or len(set(chain)) != len(chain):
        raise ObservationFailed('signature', ['the signer chain is not one leaf followed by distinct authorities'])
    if 'signed_time' in found:
        raise ObservationFailed('signature', ['Signed Time: no secure timestamp'])
    flags = re.fullmatch(r'(0x[0-9a-f]+)\(([a-z,-]*)\)', found['code_directory'][0])
    value = int(flags.group(1), 16)
    names = [n for n in flags.group(2).split(',') if n]
    leaf = re.fullmatch(r'Developer ID Application: (.+) \(([A-Z0-9]{10})\)', leaves[0])
    return {'identifier': found['identifier'][0], 'team': found['team'][0], 'cdhash': found['cdhash'][0],
            'timestamp': found['timestamp'][0], 'flags': value, 'flag_names': names,
            'runtime': bool(value & common.CS_RUNTIME) and 'runtime' in names,
            'adhoc': bool(value & common.CS_ADHOC) or 'adhoc' in names,
            'signer_kind': 'Developer ID Application', 'signer_team': leaf.group(2), 'leaf_authority': leaves[0]}


def _facts_submit(found):
    if found['upload_id'][0].lower() != found['id'][0].lower():
        raise ObservationFailed('submit', ['two submission identifiers'])
    return {'id': found['id'][0].lower(), 'status': found['status'][0]}


def _facts_log(found):
    return {'id': found['id'][0].lower()}


def observe_log_file(raw, submission_id, submitted_sha256):
    """The fetched notarization log: every key declared, none twice, required facts present."""
    try:
        value = json.loads(raw, object_pairs_hook=unique_pairs)
    except ValueError:
        raise ObservationFailed('log file', ['not one JSON object without duplicate keys'])
    why = []
    if not isinstance(value, dict):
        raise ObservationFailed('log file', ['not a JSON object'])
    for key, item in value.items():
        if key not in LOG_KEYS:
            why.append('an undeclared key')
            continue
        kind = LOG_KEYS[key][0]
        ok = {'str': isinstance(item, str), 'int': isinstance(item, int) and not isinstance(item, bool),
              'uuid': isinstance(item, str) and re.fullmatch(UUID, item) is not None,
              'status': isinstance(item, str) and re.fullmatch(STATUS, item) is not None,
              'sha256': isinstance(item, str) and re.fullmatch(r'[0-9a-f]{64}', item) is not None,
              'list_or_null': item is None or isinstance(item, list),
              'issues': item is None or (isinstance(item, list) and all(isinstance(i, dict) and set(i) <= ISSUE_KEYS for i in item))}[kind]
        if not ok:
            why.append('a value of an undeclared form: ' + key)
    for key in LOG_REQUIRED:
        if key not in value:
            why.append('missing: ' + key)
    if why:
        raise ObservationFailed('log file', why)
    return {'job': value['jobId'].lower(), 'status': value['status'], 'sha256': value['sha256'],
            'issue_count': 0 if value['issues'] is None else len(value['issues'])}


def signature_facts(fields, public_teams):
    """The recordable selection of an observed signature."""
    return {'identifier': fields['identifier'], 'team': select_team(fields['team'], public_teams), 'cdhash': fields['cdhash'],
            'flags': fields['flags'], 'runtime': fields['runtime'], 'adhoc': fields['adhoc'], 'timestamp': fields['timestamp'],
            'signer': fields['signer_kind'], 'signer_team': select_team(fields['signer_team'], public_teams)}


# The owner's steps and their fixed reasons, added to the one closed list in common.REASONS.
STEP_NAMES = {0: 'reading the supplier signatures', 1: 'copying the App', 2: 'placing the profile', 3: 'writing the entitlements',
              4: 'signing the App', 5: 'verifying the signed App', 6: 'notarizing the App', 7: 'stapling the App',
              8: 'verifying the stapled App', 9: 'making the disk image', 10: 'notarizing the disk image',
              11: 'stapling the disk image', 12: 'the Gatekeeper assessments', 13: 'reading the package for the record'}
NOT_AN_OBSERVATION = 'a line of an undeclared form, a duplicate, another object or a missing required field'
OWNER_REASONS = {
    'REFUSED_HOST': 'refused: this host is not Apple Silicon macOS',
    'REFUSED_ENVIRONMENT': 'refused: Apple, Tauri signing or notary variables are set in the environment; the keychain supplies everything',
    'REFUSED_IDENTITY_PATH': 'refused: --identity is a path, not the name of a signing identity',
    'REFUSED_IDENTITY_FORM': 'refused: --identity is not of the form "Developer ID Application: <name> (<TEAMID>)"',
    'REFUSED_IDENTITY_CREDENTIAL': 'refused: --identity looks like a credential',
    'REFUSED_NOTARY_PROFILE': 'refused: --notary-profile is not a keychain profile name (letters, digits, . _ -)',
    'REFUSED_PROFILE_DIGEST_FORM': 'refused: --profile-sha256 is not 64 lowercase hexadecimal digits',
    'REFUSED_ARGUMENT_CREDENTIAL': 'refused: a path argument looks like a credential or a key file',
    'REFUSED_PRIVATE_INPUT': 'refused: an argument path lies inside a folder named as the private output folder',
    'REFUSED_LOCATION': 'refused: --candidate or --out is inside /Applications, /System/Applications or ~/Library',
    'REFUSED_OUT_EXISTS': 'refused: --out already exists; give a new folder',
    'REFUSED_OUT_PARENT': 'refused: the folder that would hold --out does not exist',
    'REFUSED_CANDIDATE': 'refused: the candidate does not verify against CANDIDATE.json, or its build did not finish',
    'REFUSED_TEAM': 'refused: the identity names a team other than the candidate\'s compiled publisher team',
    'REFUSED_LIMITATIONS': 'refused: --limitations is not the candidate source\'s release limitations file',
    'REFUSED_PROFILE_BYTES': 'refused: the provisioning profile\'s bytes differ from --profile-sha256',
    'REFUSED_UNREADABLE': 'refused: an argument file or the candidate could not be read; nothing ran',
    'S0_NO_MACHO': 'step 0: the supplier\'s tree holds no Mach-O file',
    'S0_SIGNATURE': ('step 0: a supplier executable\'s signature display is not an observation (' + NOT_AN_OBSERVATION + '), or shows '
                     'another signer or team, no hardened runtime or no secure timestamp; re-signing is not part of the arrangement '
                     '(DEL-01-06 CLM-002), so if the display was read, the pin returns to the owner'),
    'S0_ENTITLEMENTS': ('step 0: a supplier executable\'s entitlements are not an observation (' + NOT_AN_OBSERVATION + ') or include '
                        'get-task-allow; re-signing is not part of the arrangement (DEL-01-06 CLM-002)'),
    'S1_COPY': 'step 1: the working copy of the App differs from the candidate in bytes, modes or types',
    'S2_PROFILE': 'step 2: the provisioning profile is not a current Developer ID profile granting the publisher App ID and team',
    'S2_PLACED': 'step 2: the placed profile is not mode 0644 with the selected digest',
    'S3_APP_ID': 'step 3: the profile grants another application identifier than the publisher binding derives',
    'S4_SIGN': 'step 4: codesign did not return zero when signing the App',
    'S6_ARCHIVE': 'step 6: ditto did not archive the App for submission',
    'S6_ARCHIVE_CHANGED': 'step 6: archiving the App for submission changed the App',
    'S7_ONLY_TICKET': 'step 7: stapling changed the App beyond adding its ticket at Contents/CodeResources',
    'S7_VENDOR': 'step 7: stapling changed the supplier\'s tree inside the App',
    'S9_CREATE': 'step 9: hdiutil did not create the disk image',
    'S9_SIGN': 'step 9: codesign did not return zero when signing the disk image',
    'S9_VERIFY': 'step 9: the disk image\'s verification is not an observation of a valid signature (' + NOT_AN_OBSERVATION + ')',
    'S9_DISPLAY': 'step 9: the disk image\'s signature display is not an observation (' + NOT_AN_OBSERVATION + '), or lacks the given identity, the team or a secure timestamp',
    'S9_APP_CHANGED': 'step 9: the stapled App changed while the disk image was made',
    'S12_OPEN': 'step 12: the disk image\'s Gatekeeper assessment is not an observation of acceptance from Notarized Developer ID (' + NOT_AN_OBSERVATION + ')',
    'S12_ATTACH': 'step 12: the disk image did not mount read-only',
    'S12_MOUNTED': 'step 12: the App in the mounted disk image differs from the stapled App',
    'S12_LIMITATIONS': 'step 12: the limitations file in the disk image differs from the candidate source',
    'S12_EXEC': 'step 12: the mounted App\'s Gatekeeper assessment is not an observation of acceptance from Notarized Developer ID (' + NOT_AN_OBSERVATION + ')',
    'S12_DETACH': 'step 12: the disk image did not detach; detach it with hdiutil detach',
    'S13_ATTACH': 'step 13: the disk image did not mount read-only for the record',
    'S13_OBSERVATION': 'step 13: an observation the record states failed; no record was written',
    'S13_DETACH': 'step 13: the disk image did not detach; no record was written; detach it with hdiutil detach',
    'GUARD_SIGNING': 'guard: a signing call other than the one on the App and the one on the disk image was refused',
    'INTERRUPTED': 'interrupted: the run was interrupted; nothing ran after the interruption',
}
for _number, _name in STEP_NAMES.items():
    OWNER_REASONS[f'S{_number}_UNEXPECTED'] = f'step {_number}: an error no check covers while {_name}; the private folder holds the trace'
for _number, _subject in ((5, 'signed App'), (8, 'stapled App')):
    OWNER_REASONS.update({
        f'S{_number}_DEEP': f'step {_number}: the {_subject}\'s deep strict verification is not an observation of a valid signature ({NOT_AN_OBSERVATION})',
        f'S{_number}_REQUIREMENT': f'step {_number}: the {_subject}\'s verification against the compiled publisher requirement is not an observation of it satisfied ({NOT_AN_OBSERVATION})',
        f'S{_number}_DISPLAY': f'step {_number}: the {_subject}\'s signature display is not an observation ({NOT_AN_OBSERVATION})',
        f'S{_number}_SIGNER': f'step {_number}: the {_subject}\'s signature lacks hardened runtime, the given identity, the team or the identifier',
        f'S{_number}_ENTITLEMENTS': f'step {_number}: the {_subject}\'s entitlements are not an observation ({NOT_AN_OBSERVATION}) or not exactly the two expected keys',
        f'S{_number}_INVENTORY': (f'step {_number}: the {_subject} changed beyond the main executable, _CodeSignature, the profile'
                                  + (' and its ticket' if _number == 8 else '')),
        f'S{_number}_VENDOR': f'step {_number}: the supplier\'s tree inside the {_subject} changed',
        f'S{_number}_CDHASH': f'step {_number}: a supplier executable\'s signature display in the {_subject} is not an observation, or its code-directory hash changed',
    })
for _number, _subject in ((6, 'App archive'), (10, 'disk image')):
    OWNER_REASONS.update({
        f'S{_number}_SUBMIT': f'step {_number}: the submission of the {_subject} is not an observation ({NOT_AN_OBSERVATION}); it may have reached Apple, but nothing was stapled',
        f'S{_number}_STATUS': f'step {_number}: the notarization status of the {_subject} is not Accepted; nothing was stapled',
        f'S{_number}_LOG': f'step {_number}: the fetched notarization log of the {_subject} is not an observation ({NOT_AN_OBSERVATION}, or an undeclared log key); nothing was stapled',
        f'S{_number}_LOG_STATUS': f'step {_number}: the notarization log of the {_subject} is not Accepted; nothing was stapled',
        f'S{_number}_ISSUES': f'step {_number}: the notarization log of the {_subject} does not state an empty issues list; nothing was stapled',
        f'S{_number}_DIGEST': f'step {_number}: the notarization log names a digest other than the submitted {_subject}\'s; nothing was stapled',
        f'S{_number}_JOB': f'step {_number}: the notarization log names another submission than the {_subject}\'s; nothing was stapled',
    })
for _number, _subject in ((7, 'the App'), (11, 'the disk image')):
    OWNER_REASONS.update({
        f'S{_number}_STAPLE': f'step {_number}: stapling {_subject} is not an observation of success ({NOT_AN_OBSERVATION})',
        f'S{_number}_VALIDATE': f'step {_number}: validating {_subject}\'s ticket is not an observation of success ({NOT_AN_OBSERVATION})',
    })
common.REASONS.update(OWNER_REASONS)
common.VOCABULARY.update(OWNER_REASONS.values())
