#!/usr/bin/env python3
"""Compare a candidate's sign-in flow with the one the retained terms record covers.

DEL-01-06 AC-004, second sentence: "The candidate's offering and sign-in flow are the ones the
applicability statement covers; a changed offering or sign-in flow reads as unresolved." VER-004
reads the applicability statement "against the offering and the sign-in flow the candidate
actually uses".

The retained record (app/packaging/terms/retained, read and never written) covers the stock
Codex-managed `account/login/start` with type `chatgpt` or `chatgptDeviceCode`, recorded at
repository revision fdcf608f, whose declared pin was 0.160.0. That is the baseline.

Two parts:

1. Schema, exact. The compared definitions are the request, response and notification definitions
   of the methods the sign-in flow uses (account/login/start, account/login/cancel,
   account/login/completed, account/read, account/updated, account/logout), the login-method
   policy the host consults (ForcedLoginMethod, the item type of configRequirements'
   allowedLoginMethods), and every definition those reach through `$ref`. They are compared with
   the baseline's by exact content.

2. Source, evidence plus a bound reading. The tool concludes nothing about the host source by
   itself. It computes one digest over the whole host source tree (every file under
   app/src-tauri/src) and lists, by plain text search with no parsing and no exclusions, every
   line containing "account/login", "login/start" or "LoginAccount". That search is evidence for a
   reader; an unusual spelling can evade it. The result rests on a reading: a JSON file under
   app/packaging/terms/readings/ that a named reader, who did not write the sign-in code change,
   made against that exact source tree digest and pin, stating the account sign-in types the host
   sends. Any change to the host source makes a reading stale, so a reading is made once, for the
   final candidate. The tool never writes a reading.

The result is `unchanged` only when the compared definitions equal the baseline's, exactly one
well-formed reading exists for the current source tree digest and the candidate's pin, and that
reading's account sign-in types equal the baseline's. Otherwise it is `unresolved`, with each
condition that failed. It states no applicability: that is the owner's statement. Equal schemas
and an equal reading do not show that the supplier's own sign-in behaviour inside Codex is
unchanged between pins.
"""
import argparse
from datetime import date
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
RETAINED_RECORD = 'app/packaging/terms/retained/execution/PKG-01/DEL-01-06/Work/terms-position-v1/OpenAI.json'
SCHEMA = 'app/src-tauri/resources/supplier/{pin}/codex_app_server_protocol.v2.schemas.json'
SOURCE_DIR = 'app/src-tauri/src'
READINGS_DIR = 'app/packaging/terms/readings'
PIN_SOURCE = 'app/src-tauri/src/hosting.rs'
PIN = re.compile(rb'pub const DECLARED_PIN: &str = "([0-9]+\.[0-9]+\.[0-9]+)";')
TREE_METHOD = 'chirality.app.source-tree.sha256/v1'
SEARCH = (b'account/login', b'login/start', b'LoginAccount')
READING_FORMAT = 'chirality-terms-sign-in-reading/v1'

# What the retained record covers, from repository revision fdcf608f (a test re-derives the pin
# and schema bytes from that revision when Git history is available).
BASELINE = {
    'revision': 'fdcf608fb57c4f8299c7440ffc56519314046cff',
    'pin': '0.160.0',
    'schema_file_sha256': 'e77b7d1436a78f431a74b2cb263a862e92ae40d70411bc63835b47ab2168827c',
    'account_sign_in_types': ['chatgpt', 'chatgptDeviceCode'],
}

# Roots of the compared set; the set is these plus their `$ref` closure in the pin's schema.
ROOTS = (
    'LoginAccountParams', 'LoginAccountResponse',                     # account/login/start
    'CancelLoginAccountParams', 'CancelLoginAccountResponse',         # account/login/cancel
    'AccountLoginCompletedNotification',                              # account/login/completed
    'GetAccountParams', 'GetAccountResponse',                         # account/read
    'AccountUpdatedNotification',                                     # account/updated
    'LogoutAccountResponse',                                          # account/logout
    'ForcedLoginMethod',                                              # allowedLoginMethods policy
)
# The survey's named list; reported for comparison with the closure, not used to decide.
NAMED = ROOTS + ('CancelLoginAccountStatus', 'LoginAppBrand', 'AuthMode')

ESTABLISHES = (
    'The schema comparison is exact: the compared definitions at the candidate\'s pin against the baseline\'s, by content.',
    'The source evidence is a plain text search that an unusual spelling can evade; it is evidence for a reader, not a '
    'conclusion, which is why the result rests on a reading bound to the exact source tree digest.',
    'Any change to the host source makes a reading stale; a reading is made once, for the final candidate.',
    'Nothing here states applicability; that is the owner\'s statement (DEL-01-06 CLM-003).',
)

CONDITIONS = ('input unreadable', 'schema differs', 'malformed reading', 'no reading for this source tree',
              'reading made for another tree or pin', 'more than one reading for this source tree', 'types differ')


class Unreadable(Exception):
    pass


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def _os(what, call, *args, **kwargs):
    try:
        return call(*args, **kwargs)
    except OSError as error:
        raise Unreadable(f'{what}: {type(error).__name__}') from error


DIR_FLAGS = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
FILE_FLAGS = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK


class Tree:
    """Reads beneath a root, opening every component without following a link."""
    def __init__(self, root):
        self.root = Path(os.path.abspath(root))

    def _open_dir(self, relative):
        fd = _os(str(self.root), os.open, '/', DIR_FLAGS)
        try:
            for part in self.root.parts[1:] + tuple(p for p in PurePosixPath(relative).parts if relative):
                child = _os(f'{relative or "."}: link, missing or untraversable', os.open, part, DIR_FLAGS, dir_fd=fd)
                os.close(fd); fd = child
        except BaseException:
            os.close(fd); raise
        return fd

    @staticmethod
    def _read_at(fd, name, where):
        leaf = _os(where, os.open, name, FILE_FLAGS, dir_fd=fd)
        try:
            before = os.fstat(leaf)
            if not stat.S_ISREG(before.st_mode):
                raise Unreadable(f'{where}: not a regular file')
            chunks = []
            while chunk := _os(where, os.read, leaf, 1 << 20):
                chunks.append(chunk)
            after = os.fstat(leaf)
            if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
                raise Unreadable(f'{where}: changed while read')
            return b''.join(chunks)
        finally:
            os.close(leaf)

    def read(self, relative):
        parent, _, name = relative.rpartition('/')
        fd = self._open_dir(parent)
        try:
            return self._read_at(fd, name, relative)
        finally:
            os.close(fd)

    def listing(self, relative):
        """Names and own metadata in one directory; returns None when it does not exist."""
        try:
            fd = self._open_dir(relative)
        except Unreadable as error:
            if isinstance(error.__cause__, FileNotFoundError):
                return None
            raise
        try:
            return {n: _os(f'{relative}/{n}', os.stat, n, dir_fd=fd, follow_symlinks=False)
                    for n in _os(relative, os.listdir, fd)}
        finally:
            os.close(fd)

    def files(self, relative):
        """Every file under a directory: relative path -> bytes. Links, special files, line breaks
        in names, anything unreadable and a directory that changes while read refuse."""
        found = {}
        def visit(fd, prefix):
            def identities():
                names = _os(prefix or relative, os.listdir, fd)
                out = {}
                for name in names:
                    if '\n' in name or '\r' in name:
                        raise Unreadable(f'{prefix}{name!r}: line break in a name')
                    info = _os(prefix + name, os.stat, name, dir_fd=fd, follow_symlinks=False)
                    out[name] = (info.st_mode, info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns)
                return out
            before = identities()
            for name, (mode, *_rest) in sorted(before.items(), key=lambda item: item[0].encode()):
                if stat.S_ISLNK(mode):
                    raise Unreadable(f'{prefix}{name}: symbolic link refused')
                if stat.S_ISDIR(mode):
                    child = _os(prefix + name, os.open, name, DIR_FLAGS, dir_fd=fd)
                    try:
                        visit(child, prefix + name + '/')
                    finally:
                        os.close(child)
                elif stat.S_ISREG(mode):
                    found[prefix + name] = self._read_at(fd, name, prefix + name)
                else:
                    raise Unreadable(f'{prefix}{name}: special file refused')
            if identities() != before:
                raise Unreadable(f'{prefix or relative}: changed while read')
        fd = self._open_dir(relative)
        try:
            visit(fd, '')
        finally:
            os.close(fd)
        return found


class GitRevision:
    """Committed bytes at a revision; used only to re-derive the baseline's pin and schema."""
    def __init__(self, repository, revision):
        self.repository, self.revision = repository, revision

    def read(self, relative):
        result = subprocess.run(['git', '-C', str(self.repository), 'show', f'{self.revision}:{relative}'],
                                capture_output=True, timeout=60)
        if result.returncode != 0:
            raise Unreadable(f'git show {relative}')
        return result.stdout


def tree_digest(files):
    """SHA-256 over method, count, then each file in UTF-8 path byte order: path length, path,
    content length, content (lengths as 8-byte big-endian)."""
    preimage = bytearray(TREE_METHOD.encode()); preimage.append(0)
    preimage += len(files).to_bytes(8, 'big')
    for path in sorted(files, key=str.encode):
        raw = files[path]
        preimage += len(path.encode()).to_bytes(8, 'big') + path.encode() + len(raw).to_bytes(8, 'big') + raw
    return sha(bytes(preimage))


def evidence(files):
    """Every line containing a search term, by plain text search: no parsing, no exclusions."""
    found = []
    for path in sorted(files, key=str.encode):
        for number, line in enumerate(files[path].split(b'\n'), 1):
            if any(term in line for term in SEARCH):
                found.append({'file': path, 'line': number, 'text': line.strip().decode('utf-8', 'replace')[:240]})
    return found


def declared_pin(reader):
    found = PIN.findall(reader.read(PIN_SOURCE))
    if len(found) != 1:
        raise Unreadable('declared pin not found exactly once')
    return found[0].decode()


def references(value, found):
    if isinstance(value, dict):
        for key, item in value.items():
            if key == '$ref' and isinstance(item, str):
                if not item.startswith('#/definitions/'):
                    raise Unreadable('schema reference outside its definitions')
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
        raise Unreadable('schema is not JSON') from error
    definitions = schema.get('definitions') if isinstance(schema, dict) else None
    if not isinstance(definitions, dict):
        raise Unreadable('schema has no definitions')
    selected, pending = set(), list(ROOTS)
    while pending:
        name = pending.pop()
        if name in selected:
            continue
        if name not in definitions:
            raise Unreadable(f'schema lacks definition {name}')
        selected.add(name)
        found = set(); references(definitions[name], found); pending.extend(found - selected)
    compared = {name: definitions[name] for name in sorted(selected)}
    named = {n: definitions.get(n) for n in NAMED}
    return {'compared_definitions': sorted(compared), 'compared_set_sha256': sha(canonical(compared)),
            'definition_sha256': {n: sha(canonical(v)) for n, v in compared.items()},
            'named_set_sha256': sha(canonical(named))}


def baseline(tree):
    record = json.loads(tree.read(RETAINED_RECORD))
    text = json.dumps(record)
    if BASELINE['revision'] not in text or not all(t in text for t in BASELINE['account_sign_in_types']):
        raise Unreadable('retained record does not name the baseline revision and sign-in types')
    raw = tree.read(SCHEMA.format(pin=BASELINE['pin']))
    if sha(raw) != BASELINE['schema_file_sha256']:
        raise Unreadable('baseline schema bytes differ from those at the recorded revision')
    return {'revision': BASELINE['revision'], 'pin': BASELINE['pin'],
            'retained_scope': record.get('scope') if isinstance(record, dict) else None,
            'schema_file_sha256': BASELINE['schema_file_sha256'],
            'account_sign_in_types': list(BASELINE['account_sign_in_types']), **compared_definitions(raw)}


HEX64 = re.compile(r'[0-9a-f]{64}')
PIN_TEXT = re.compile(r'[0-9]+\.[0-9]+\.[0-9]+')
TYPE_TEXT = re.compile(r'[A-Za-z][A-Za-z0-9]*')


def _location(value, files, where):
    if not (isinstance(value, dict) and set(value) == {'file', 'line'}):
        raise ValueError(f'{where}: exactly file and line required')
    path, line = value['file'], value['line']
    if not (isinstance(path, str) and path in files and type(line) is int and line >= 1):
        raise ValueError(f'{where}: names no file of this source tree or no line')
    if line > files[path].count(b'\n') + 1:
        raise ValueError(f'{where}: line beyond the end of {path}')


def validate_reading(value, files, matches_tree):
    """Strict structure. Locations are checked against the tree only when the digest matches."""
    keys = {'format', 'source_tree_sha256', 'pin', 'reader', 'date', 'account_sign_in_types',
            'separate_credential_logins', 'relied_on'}
    if not (isinstance(value, dict) and set(value) == keys):
        raise ValueError('reading must hold exactly: ' + ', '.join(sorted(keys)))
    if value['format'] != READING_FORMAT:
        raise ValueError('unknown reading format')
    if not (isinstance(value['source_tree_sha256'], str) and HEX64.fullmatch(value['source_tree_sha256'])):
        raise ValueError('source_tree_sha256 must be 64 lowercase hex')
    if not (isinstance(value['pin'], str) and PIN_TEXT.fullmatch(value['pin'])):
        raise ValueError('pin must be x.y.z')
    reader = value['reader']
    if not (isinstance(reader, dict) and set(reader) == {'name', 'role', 'did_not_write_the_sign_in_change'}
            and all(isinstance(reader[k], str) and reader[k].strip() for k in ('name', 'role'))
            and reader['did_not_write_the_sign_in_change'] is True):
        raise ValueError('reader must name, role and did_not_write_the_sign_in_change: true')
    try:
        date.fromisoformat(value['date'])
        if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', value['date']):
            raise ValueError
    except (TypeError, ValueError) as error:
        raise ValueError('date must be YYYY-MM-DD') from error
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
        if matches_tree:
            for j, place in enumerate(login['sent_from']):
                _location(place, files, f'separate_credential_logins[{k}].sent_from[{j}]')
    relied = value['relied_on']
    if not (isinstance(relied, list) and relied):
        raise ValueError('relied_on must be a non-empty list')
    if matches_tree:
        for k, place in enumerate(relied):
            _location(place, files, f'relied_on[{k}]')


def readings(tree, files, digest):
    """(well-formed readings with their file names, malformed reading problems)."""
    entries = tree.listing(READINGS_DIR)
    good, malformed = [], []
    for name in sorted(entries or {}):
        info = entries[name]
        if name == 'README.md' and stat.S_ISREG(info.st_mode):
            continue
        if not (name.endswith('.json') and stat.S_ISREG(info.st_mode)):
            malformed.append({'reading': name, 'problem': 'not a regular .json file'})
            continue
        try:
            value = json.loads(tree.read(f'{READINGS_DIR}/{name}'))
            validate_reading(value, files, isinstance(value, dict) and value.get('source_tree_sha256') == digest)
        except (ValueError, UnicodeDecodeError) as error:
            malformed.append({'reading': name, 'problem': str(error)})
            continue
        good.append((name, value))
    return good, malformed


def compare(source_root, record_root=None):
    tree, retained = Tree(source_root), Tree(record_root or source_root)
    report = {'format': 'chirality-terms-sign-in-flow/v2', 'establishes': list(ESTABLISHES),
              'baseline_revision': BASELINE['revision']}
    failed, differences = [], []
    try:
        base = baseline(retained)
        pin = declared_pin(tree)
        candidate = {'pin': pin, 'schema_path': SCHEMA.format(pin=pin), **compared_definitions(tree.read(SCHEMA.format(pin=pin)))}
        files = tree.files(SOURCE_DIR)
        digest = tree_digest(files)
        good, malformed = readings(tree, files, digest)
    except (Unreadable, ValueError, UnicodeDecodeError, RecursionError) as error:
        return report | {'status': 'unresolved', 'conditions_failed': ['input unreadable'], 'unreadable': str(error)}
    for name in sorted(set(base['definition_sha256']) | set(candidate['definition_sha256'])):
        before, after = base['definition_sha256'].get(name), candidate['definition_sha256'].get(name)
        if before != after:
            differences.append({'definition': name, 'baseline': before, 'candidate': after})
    if differences:
        failed.append('schema differs')
    if malformed:
        failed.append('malformed reading')
    bound = [(n, r) for n, r in good if r['source_tree_sha256'] == digest and r['pin'] == pin]
    if len(bound) > 1:
        failed.append('more than one reading for this source tree')
    elif not bound:
        failed.append('reading made for another tree or pin' if good else 'no reading for this source tree')
    elif sorted(bound[0][1]['account_sign_in_types']) != sorted(base['account_sign_in_types']):
        failed.append('types differ')
    source = {'tree_method': TREE_METHOD, 'tree_sha256': digest, 'files': len(files),
              'search_terms': [t.decode() for t in SEARCH], 'evidence': evidence(files)}
    report |= {'status': 'unresolved' if failed else 'unchanged', 'conditions_failed': failed,
               'schema': {'baseline': base, 'candidate': candidate, 'differences': differences,
                          'named_set_equal': base['named_set_sha256'] == candidate['named_set_sha256']},
               'source': source,
               'readings': {'bound': [n for n, _ in bound], 'other': [{'reading': n, 'source_tree_sha256': r['source_tree_sha256'],
                            'pin': r['pin']} for n, r in good if (n, r) not in bound], 'malformed': malformed}}
    if len(bound) == 1:
        report['readings']['account_sign_in_types'] = bound[0][1]['account_sign_in_types']
        report['readings']['reader'] = bound[0][1]['reader']['name']
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--source-root', default=str(ROOT), help='candidate source tree (default: this checkout)')
    parser.add_argument('--record-root', help='tree holding the retained record and baseline schema (default: the source root)')
    args = parser.parse_args(argv)
    report = compare(args.source_root, args.record_root)
    print(json.dumps(report, indent=2))
    return 0 if report['status'] == 'unchanged' else 1


if __name__ == '__main__':
    sys.exit(main())
