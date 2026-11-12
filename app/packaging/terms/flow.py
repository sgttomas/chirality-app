#!/usr/bin/env python3
"""Compare a candidate's sign-in flow with the one the retained terms record covers.

DEL-01-06 AC-004, second sentence: "The candidate's offering and sign-in flow are the ones the
applicability statement covers; a changed offering or sign-in flow reads as unresolved." VER-004
reads the applicability statement "against the offering and the sign-in flow the candidate
actually uses".

Everything is read from the Git object store at one named commit, which does not change under the
tool: the retained record (app/packaging/terms/retained, never written), the schemas, the evidence
and the readings. The working tree under app/ must equal that commit; otherwise, or without a Git
checkout of the revision, the result is unresolved.

Baseline (the retained record's scope): repository revision fdcf608f, its 0.160.0 schema, and the
account sign-in types `chatgpt` and `chatgptDeviceCode`.

1. Schema, exact. The compared definitions are the request, response and notification definitions
   of account/login/start, account/login/cancel, account/login/completed, account/read,
   account/updated and account/logout, the login-method policy the host consults
   (ForcedLoginMethod), and every definition those reach through `$ref`, compared by content at
   the candidate's pin against the baseline.

2. Bound set, evidence and a reading. The bound set is every file Git tracks under app/ at the
   commit except the readings folder app/packaging/terms/readings/. Its identity is BOUND_FORM
   below. The evidence is every line containing "account/login", "login/start" or "LoginAccount"
   in any tracked file under app/src-tauri and app/src at the commit, by plain text search with no
   parsing; an unusual spelling can evade it, so it is a starting point for a reader and decides
   nothing. The result rests on a reading: a JSON file tracked under the readings folder at the
   commit, made by a named reader in a closed set of roles, naming the commit it was made against
   and that commit's bound-set digest, which must equal this commit's.

The result is `unchanged` only when the compared definitions equal the baseline's, exactly one
well-formed reading exists for this bound set and pin, and its account sign-in types equal the
baseline's. Otherwise `unresolved`, naming each failed condition. See LIMITS for what this
withstands. It states no applicability; that is the owner's statement.
"""
import argparse
from datetime import date
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
RETAINED_RECORD = 'app/packaging/terms/retained/execution/PKG-01/DEL-01-06/Work/terms-position-v1/OpenAI.json'
SCHEMA = 'app/src-tauri/resources/supplier/{pin}/codex_app_server_protocol.v2.schemas.json'
READINGS_DIR = 'app/packaging/terms/readings/'
PIN_SOURCE = 'app/src-tauri/src/hosting.rs'
PIN = re.compile(rb'pub const DECLARED_PIN: &str = "([0-9]+\.[0-9]+\.[0-9]+)";')
SEARCH = ('account/login', 'login/start', 'LoginAccount')
EVIDENCE_PATHS = ('app/src-tauri', 'app/src')
READING_FORMAT = 'chirality-terms-sign-in-reading/v2'
ROLES = ('owner', 'independent reviewer')
NOT_READERS = {'flow.py', 'app/packaging/terms/flow.py', 'the tool', 'tool', 'claude', 'codex'}
BOUND_FORM = ('SHA-256 over the concatenation, in the order `git ls-tree -r -z <commit> -- app/` gives, of '
              '"<mode> <type> <object>\\t<path>\\n" (UTF-8, path as Git stores it) for every entry whose path does '
              'not start with "app/packaging/terms/readings/"')

BASELINE = {
    'revision': 'fdcf608fb57c4f8299c7440ffc56519314046cff',
    'pin': '0.160.0',
    'schema_file_sha256': 'e77b7d1436a78f431a74b2cb263a862e92ae40d70411bc63835b47ab2168827c',
    'account_sign_in_types': ['chatgpt', 'chatgptDeviceCode'],
}

ROOTS = (
    'LoginAccountParams', 'LoginAccountResponse',                     # account/login/start
    'CancelLoginAccountParams', 'CancelLoginAccountResponse',         # account/login/cancel
    'AccountLoginCompletedNotification',                              # account/login/completed
    'GetAccountParams', 'GetAccountResponse',                         # account/read
    'AccountUpdatedNotification',                                     # account/updated
    'LogoutAccountResponse',                                          # account/logout
    'ForcedLoginMethod',                                              # allowedLoginMethods policy
)
NAMED = ROOTS + ('CancelLoginAccountStatus', 'LoginAppBrand', 'AuthMode')

LIMITS = (
    'This is an operator-run check on stable inputs. It is built so that an observation that was not made, that failed, '
    'or that is incomplete cannot come out as success, and so that drift and mistakes are caught.',
    'It is not built to withstand a writer changing the inputs during the run, nor someone with write access forging a '
    'reading.',
    'The schema comparison is exact. The evidence is a plain text search that an unusual spelling can evade; it decides '
    'nothing.',
    'The tool checks that a reading exists for exactly this commit\'s bound set and pin, and what it states. It cannot '
    'establish that an independent reading occurred: a reading\'s truth rests on the review of the pull request that '
    'commits it and on the named reader, not on the tool.',
    'Any change to a tracked file under app/ other than the readings folder changes the bound set, so a reading is made '
    'once, for the final candidate. Files Git ignores under app/ (build output, generated files) and files outside app/ '
    'are not in the bound set and are not looked at.',
    'Nothing here states applicability; that is the owner\'s statement (DEL-01-06 CLM-003).',
)


class Unresolved(Exception):
    def __init__(self, condition, detail):
        super().__init__(detail)
        self.condition = condition


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


class Repository:
    """Read-only access to one commit's object store."""
    def __init__(self, path):
        self.path = Path(path)

    def git(self, *args, ok=(0,)):
        try:
            result = subprocess.run(['git', '-C', str(self.path), *args], capture_output=True, timeout=120)
        except (OSError, subprocess.TimeoutExpired) as error:
            raise Unresolved('input unreadable', f'git {args[0]}: {type(error).__name__}') from error
        if result.returncode not in ok:
            raise Unresolved('input unreadable', f'git {args[0]} failed')
        return result

    def commit(self, revision):
        result = subprocess.run(['git', '-C', str(self.path), 'rev-parse', '--verify', '--quiet', revision + '^{commit}'],
                                capture_output=True, timeout=60) if self.path.is_dir() else None
        if result is None or result.returncode != 0 or not re.fullmatch(rb'[0-9a-f]{40}\n', result.stdout):
            raise Unresolved('no git checkout of the revision', f'{revision} does not resolve to a commit here')
        top = subprocess.run(['git', '-C', str(self.path), 'rev-parse', '--show-toplevel'], capture_output=True, timeout=60)
        if top.returncode != 0:
            raise Unresolved('no git checkout of the revision', 'not inside a Git working tree')
        self.path = Path(top.stdout.decode().strip())   # paths below are relative to the repository root
        return result.stdout.decode().strip()

    def require_clean(self, commit):
        """The working tree under app/ must equal the commit: nothing modified, staged or untracked."""
        status = self.git('status', '--porcelain=v1', '-z', '--untracked-files=all', '--', 'app/').stdout
        head = self.git('rev-parse', '--verify', 'HEAD^{commit}').stdout.decode().strip()
        differs = self.git('diff', '--name-only', '-z', commit, '--', 'app/').stdout
        if status or differs or (head != commit and self.git('diff', '--cached', '--name-only', '-z', commit, '--', 'app/').stdout):
            raise Unresolved('working tree differs from the commit under app/',
                             'modified, staged or untracked files under app/ differ from the named commit')

    def show(self, commit, path):
        return self.git('show', f'{commit}:{path}').stdout

    def entries(self, commit):
        """(mode, type, object, path) for every entry under app/ at the commit, in ls-tree order."""
        raw = self.git('ls-tree', '-r', '-z', commit, '--', 'app/').stdout
        out = []
        for item in raw.split(b'\0'):
            if not item:
                continue
            meta, _, path = item.partition(b'\t')
            mode, kind, obj = meta.split(b' ')
            path = path.decode('utf-8')
            if '\n' in path:
                raise Unresolved('input unreadable', 'a tracked path holds a line break')
            out.append((mode.decode(), kind.decode(), obj.decode(), path))
        if not out:
            raise Unresolved('input unreadable', 'nothing tracked under app/ at the commit')
        return out


def bound_set(entries):
    listing = b''.join(f'{m} {k} {o}\t{p}\n'.encode('utf-8') for m, k, o, p in entries if not p.startswith(READINGS_DIR))
    return sha(listing)


def evidence(repo, commit):
    args = ['grep', '-z', '-n', '-a', '-F']
    for term in SEARCH:
        args += ['-e', term]
    raw = repo.git(*args, commit, '--', *EVIDENCE_PATHS, ok=(0, 1)).stdout
    found = []
    for line in raw.split(b'\n'):
        if not line:
            continue
        name, number, text = line.split(b'\0', 2)
        found.append({'file': name.decode('utf-8').split(':', 1)[1], 'line': int(number),
                      'text': text.strip().decode('utf-8', 'replace')[:240]})
    return found


def references(value, found):
    if isinstance(value, dict):
        for key, item in value.items():
            if key == '$ref' and isinstance(item, str):
                if not item.startswith('#/definitions/'):
                    raise Unresolved('input unreadable', 'schema reference outside its definitions')
                found.add(item.rsplit('/', 1)[1])
            else:
                references(item, found)
    elif isinstance(value, list):
        for item in value:
            references(item, found)


def compared_definitions(raw):
    try:
        schema = json.loads(raw)
    except ValueError as error:
        raise Unresolved('input unreadable', 'schema is not JSON') from error
    definitions = schema.get('definitions') if isinstance(schema, dict) else None
    if not isinstance(definitions, dict):
        raise Unresolved('input unreadable', 'schema has no definitions')
    selected, pending = set(), list(ROOTS)
    while pending:
        name = pending.pop()
        if name in selected:
            continue
        if name not in definitions:
            raise Unresolved('input unreadable', f'schema lacks definition {name}')
        selected.add(name)
        found = set(); references(definitions[name], found); pending.extend(found - selected)
    compared = {name: definitions[name] for name in sorted(selected)}
    return {'compared_definitions': sorted(compared), 'compared_set_sha256': sha(canonical(compared)),
            'definition_sha256': {n: sha(canonical(v)) for n, v in compared.items()},
            'named_set_sha256': sha(canonical({n: definitions.get(n) for n in NAMED}))}


def baseline(repo, commit):
    try:
        record = json.loads(repo.show(commit, RETAINED_RECORD))
    except ValueError as error:
        raise Unresolved('input unreadable', 'retained record is not JSON') from error
    text = json.dumps(record)
    if BASELINE['revision'] not in text or not all(t in text for t in BASELINE['account_sign_in_types']):
        raise Unresolved('input unreadable', 'retained record does not name the baseline revision and sign-in types')
    raw = repo.show(commit, SCHEMA.format(pin=BASELINE['pin']))
    if sha(raw) != BASELINE['schema_file_sha256']:
        raise Unresolved('input unreadable', 'baseline schema bytes differ from those at the recorded revision')
    return {'revision': BASELINE['revision'], 'pin': BASELINE['pin'], 'schema_file_sha256': BASELINE['schema_file_sha256'],
            'account_sign_in_types': list(BASELINE['account_sign_in_types']), **compared_definitions(raw)}


def declared_pin(repo, commit):
    found = PIN.findall(repo.show(commit, PIN_SOURCE))
    if len(found) != 1:
        raise Unresolved('input unreadable', 'declared pin not found exactly once')
    return found[0].decode()


def strict_json(raw):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f'duplicated field: {key}')
            result[key] = value
        return result
    return json.loads(raw.decode('utf-8'), object_pairs_hook=unique,
                      parse_constant=lambda x: (_ for _ in ()).throw(ValueError('non-finite number')))


HEX64 = re.compile(r'[0-9a-f]{64}')
HEX40 = re.compile(r'[0-9a-f]{40}')
PIN_TEXT = re.compile(r'[0-9]+\.[0-9]+\.[0-9]+')
TYPE_TEXT = re.compile(r'[A-Za-z][A-Za-z0-9]*')
KEYS = {'format', 'commit', 'bound_set_sha256', 'pin', 'reader', 'date', 'how_read', 'account_sign_in_types',
        'separate_credential_logins', 'relied_on'}


def validate_reading(value, location):
    """Strict structure; `location(file, line)` raises ValueError for a place not in the bound set."""
    if not (isinstance(value, dict) and set(value) == KEYS):
        raise ValueError('reading must hold exactly: ' + ', '.join(sorted(KEYS)))
    if value['format'] != READING_FORMAT:
        raise ValueError('unknown reading format')
    if not (isinstance(value['commit'], str) and HEX40.fullmatch(value['commit'])):
        raise ValueError('commit must be a full 40-hex commit identifier')
    if not (isinstance(value['bound_set_sha256'], str) and HEX64.fullmatch(value['bound_set_sha256'])):
        raise ValueError('bound_set_sha256 must be 64 lowercase hex')
    if not (isinstance(value['pin'], str) and PIN_TEXT.fullmatch(value['pin'])):
        raise ValueError('pin must be x.y.z')
    reader = value['reader']
    if not (isinstance(reader, dict) and set(reader) == {'name', 'role'} and isinstance(reader['name'], str)
            and reader['name'].strip() and reader['name'].strip().casefold() not in NOT_READERS and reader['role'] in ROLES):
        raise ValueError('reader must hold a name and a role in ' + ', '.join(ROLES) + '; the tool is not a reader')
    if not (isinstance(value['date'], str) and re.fullmatch(r'\d{4}-\d{2}-\d{2}', value['date'])):
        raise ValueError('date must be YYYY-MM-DD')
    date.fromisoformat(value['date'])
    if not (isinstance(value['how_read'], str) and len(value['how_read'].strip()) >= 20):
        raise ValueError('how_read must say, in the reader\'s words, which commit and what was searched and read')
    types = value['account_sign_in_types']
    if not (isinstance(types, list) and types and all(isinstance(t, str) and TYPE_TEXT.fullmatch(t) for t in types)
            and len(set(types)) == len(types)):
        raise ValueError('account_sign_in_types must be a non-empty list of distinct type names')
    logins = value['separate_credential_logins']
    if not isinstance(logins, list):
        raise ValueError('separate_credential_logins must be a list')
    for k, login in enumerate(logins):
        if not (isinstance(login, dict) and set(login) == {'type', 'home', 'sent_from'}
                and isinstance(login['type'], str) and TYPE_TEXT.fullmatch(login['type'])
                and isinstance(login['home'], str) and login['home'].strip()
                and isinstance(login['sent_from'], list) and login['sent_from']):
            raise ValueError(f'separate_credential_logins[{k}] must hold type, home and a non-empty sent_from')
        for place in login['sent_from']:
            location(place)
    if not (isinstance(value['relied_on'], list) and value['relied_on']):
        raise ValueError('relied_on must be a non-empty list')
    for place in value['relied_on']:
        location(place)


def compare(repository, revision='HEAD'):
    repo = Repository(repository)
    report = {'format': 'chirality-terms-sign-in-flow/v3', 'limits': list(LIMITS), 'bound_set_form': BOUND_FORM,
              'baseline_revision': BASELINE['revision'], 'reader_roles': list(ROLES)}
    try:
        commit = repo.commit(revision)
        report['commit'] = commit
        repo.require_clean(commit)
        entries = repo.entries(commit)
        digest = bound_set(entries)
        base = baseline(repo, commit)
        pin = declared_pin(repo, commit)
        candidate = {'pin': pin, 'schema_path': SCHEMA.format(pin=pin),
                     **compared_definitions(repo.show(commit, SCHEMA.format(pin=pin)))}
        found = evidence(repo, commit)
    except Unresolved as error:
        return report | {'status': 'unresolved', 'conditions_failed': [error.condition], 'detail': str(error)}
    blobs = {p: o for m, k, o, p in entries if k == 'blob' and not p.startswith(READINGS_DIR)}
    line_counts = {}
    def location(place):
        if not (isinstance(place, dict) and set(place) == {'file', 'line'} and isinstance(place['file'], str)
                and type(place['line']) is int and place['line'] >= 1):
            raise ValueError('a place must hold exactly file and line')
        if place['file'] not in blobs:
            raise ValueError(f'{place["file"]} is not a file of the bound set')
        if place['file'] not in line_counts:
            line_counts[place['file']] = repo.show(commit, place['file']).count(b'\n') + 1
        if place['line'] > line_counts[place['file']]:
            raise ValueError(f'line {place["line"]} is beyond the end of {place["file"]}')
    good, malformed = [], []
    for mode, kind, obj, path in entries:
        if not path.startswith(READINGS_DIR):
            continue
        name = path[len(READINGS_DIR):]
        if name == 'README.md' and kind == 'blob' and mode == '100644':
            continue
        if not (kind == 'blob' and mode == '100644' and name.endswith('.json') and '/' not in name):
            malformed.append({'reading': name, 'problem': 'not a regular .json file directly in the readings folder'})
            continue
        try:
            value = strict_json(repo.show(commit, path))
            validate_reading(value, location)
            stated = repo.commit(value['commit'])
            if bound_set(repo.entries(stated)) != value['bound_set_sha256']:
                raise ValueError('the named commit\'s bound set is not the digest the reading states')
        except (ValueError, UnicodeDecodeError, Unresolved) as error:
            malformed.append({'reading': name, 'problem': str(error)})
            continue
        good.append((name, value))
    failed, differences = [], []
    for name in sorted(set(base['definition_sha256']) | set(candidate['definition_sha256'])):
        if base['definition_sha256'].get(name) != candidate['definition_sha256'].get(name):
            differences.append({'definition': name, 'baseline': base['definition_sha256'].get(name),
                                'candidate': candidate['definition_sha256'].get(name)})
    if differences:
        failed.append('schema differs')
    if malformed:
        failed.append('malformed reading')
    bound = [(n, r) for n, r in good if r['bound_set_sha256'] == digest and r['pin'] == pin]
    if len(bound) > 1:
        failed.append('more than one reading for this bound set')
    elif not bound:
        failed.append('reading made for another bound set or pin' if good else 'no reading for this bound set')
    elif sorted(bound[0][1]['account_sign_in_types']) != sorted(base['account_sign_in_types']):
        failed.append('types differ')
    report |= {'status': 'unresolved' if failed else 'unchanged', 'conditions_failed': failed,
               'schema': {'baseline': base, 'candidate': candidate, 'differences': differences,
                          'named_set_equal': base['named_set_sha256'] == candidate['named_set_sha256']},
               'bound_set': {'sha256': digest, 'entries': sum(not e[3].startswith(READINGS_DIR) for e in entries)},
               'evidence': {'search_terms': list(SEARCH), 'paths': list(EVIDENCE_PATHS), 'lines': found},
               'readings': {'bound': [n for n, _ in bound],
                            'other': [{'reading': n, 'bound_set_sha256': r['bound_set_sha256'], 'pin': r['pin']}
                                      for n, r in good if (n, r) not in bound],
                            'malformed': malformed}}
    if len(bound) == 1:
        report['readings'] |= {'account_sign_in_types': bound[0][1]['account_sign_in_types'],
                               'reader': bound[0][1]['reader'], 'reading_commit': bound[0][1]['commit']}
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__ + '\nLimits:\n  ' + '\n  '.join(LIMITS),
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--repository', default=str(ROOT), help='Git checkout of the candidate (default: this one)')
    parser.add_argument('--revision', default='HEAD', help='commit to read (default: HEAD)')
    args = parser.parse_args(argv)
    report = compare(args.repository, args.revision)
    print(json.dumps(report, indent=2))
    return 0 if report['status'] == 'unchanged' else 1


if __name__ == '__main__':
    sys.exit(main())
