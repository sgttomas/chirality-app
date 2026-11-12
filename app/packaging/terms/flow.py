#!/usr/bin/env python3
"""Compare a candidate's sign-in flow with the one the retained terms record covers.

DEL-01-06 AC-004, second sentence: "The candidate's offering and sign-in flow are the ones the
applicability statement covers; a changed offering or sign-in flow reads as unresolved."

The retained record (app/packaging/terms/retained) covers the stock Codex-managed
`account/login/start` with type `chatgpt` or `chatgptDeviceCode`, recorded at repository
revision fdcf608f, whose declared pin was 0.160.0. This tool derives for a candidate source
tree: its declared pin; a canonical SHA-256 over the sign-in definitions of that pin's
generated v2 schema; and the sign-in types the host source sends for account sign-in. It
reports `unchanged` when those equal the baseline and `unresolved` otherwise, with every
difference. An input it cannot read is `unresolved`, never `unchanged`.

It reads the retained record and never writes anything. It states no applicability: whether
the position applies to a candidate is the owner's statement. Equal schema definitions and
equal sign-in types do not show that the supplier's own sign-in behaviour inside Codex is
unchanged between pins; that is outside what a schema and the App's source can show.

The compared definitions are the request, response and notification definitions of the
methods the sign-in flow uses (account/login/start, account/login/cancel,
account/login/completed, account/read, account/updated, account/logout), the login-method
policy the host consults before starting sign-in (ForcedLoginMethod, the item type of
configRequirements' allowedLoginMethods), and every definition those reach through `$ref`.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
RETAINED_RECORD = 'app/packaging/terms/retained/execution/PKG-01/DEL-01-06/Work/terms-position-v1/OpenAI.json'
SCHEMA = 'app/src-tauri/resources/supplier/{pin}/codex_app_server_protocol.v2.schemas.json'

# What the retained record covers, derived from repository revision fdcf608f (see the test that
# re-derives it from that revision when Git history is available).
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

PIN = re.compile(r'pub const DECLARED_PIN: &str = "([0-9]+\.[0-9]+\.[0-9]+)";')
OAUTH = re.compile(r'let kind=match mode\{([^}]*)\};\s*let source=self\.request_begin_scoped\("account/login/start",json!\(\{"type":kind\}\)')
GENERIC = re.compile(r'if method == "account/login/start"\s*&& !matches!\(\s*params\["type"\]\.as_str\(\),\s*Some\(([^)]*)\)\s*\)')
API_KEY_PARAMS = re.compile(r'fn into_params\(self\) -> Value \{\s*json!\(\{"type":"apiKey","apiKey":self\.value\}\)')
API_KEY_SEND = re.compile(r'let params=input\.into_params\(\);[^\n]*\n\s*let source=self\.request_begin_scoped_private\("account/login/start",params,')
SEND_SITE = re.compile(r'request_begin_scoped(?:_private)?\("account/login/start"')
API_KEY_CALLER = re.compile(r'\.account_login_api_key_from_native_entry\(')
LITERAL = re.compile(r'"([A-Za-z]+)"')


class Unreadable(Exception):
    pass


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


class Tree:
    """Bounded no-follow reads from a source root."""
    def __init__(self, root):
        self.root = Path(os.path.abspath(root))

    def read(self, relative):
        path = self.root / relative
        try:
            for parent in (path, *path.parents):
                if parent == self.root.parent:
                    break
                if parent.is_symlink():
                    raise Unreadable(f'{relative}: symbolic link refused')
            fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
            try:
                if not stat.S_ISREG(os.fstat(fd).st_mode):
                    raise Unreadable(f'{relative}: not a regular file')
                chunks = []
                while chunk := os.read(fd, 1 << 20):
                    chunks.append(chunk)
                return b''.join(chunks)
            finally:
                os.close(fd)
        except OSError as error:
            raise Unreadable(f'{relative}: {type(error).__name__}') from error

    def rust_sources(self):
        folder = self.root / 'app/src-tauri/src'
        try:
            names = sorted(n for n in os.listdir(folder) if n.endswith('.rs') and not n.endswith('_tests.rs'))
        except OSError as error:
            raise Unreadable(f'app/src-tauri/src: {type(error).__name__}') from error
        return {n: self.read(f'app/src-tauri/src/{n}').decode('utf-8') for n in names}


class GitRevision(Tree):
    """The same reads from a committed revision (used to re-derive the baseline)."""
    def __init__(self, repository, revision):
        self.repository, self.revision = repository, revision

    def _git(self, *args):
        result = subprocess.run(['git', '-C', str(self.repository), *args], capture_output=True, timeout=60)
        if result.returncode != 0:
            raise Unreadable('git: ' + ' '.join(args[:1]))
        return result.stdout

    def read(self, relative):
        return self._git('show', f'{self.revision}:{relative}')

    def rust_sources(self):
        names = self._git('ls-tree', '--name-only', f'{self.revision}:app/src-tauri/src').decode().split('\n')
        names = sorted(n for n in names if n.endswith('.rs') and not n.endswith('_tests.rs'))
        return {n: self.read(f'app/src-tauri/src/{n}').decode('utf-8') for n in names}


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


def compared_definitions(schema):
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
    return {name: definitions[name] for name in sorted(selected)}


def sign_in_types(sources):
    """The types the host sends for account sign-in, and the separate API-key login."""
    hosting, auth = sources.get('hosting.rs'), sources.get('auth_rpc.rs')
    if hosting is None or auth is None:
        raise Unreadable('hosting.rs or auth_rpc.rs absent')
    oauth = OAUTH.findall(hosting)
    generic = GENERIC.findall(auth)
    if len(oauth) != 1 or len(generic) != 1:
        raise Unreadable('account sign-in send site not recognised')
    sites = {n: len(SEND_SITE.findall(text)) for n, text in sources.items() if SEND_SITE.search(text)}
    api_key = bool(API_KEY_PARAMS.search(auth)) and len(API_KEY_SEND.findall(hosting)) == 1
    expected_sites = {'hosting.rs': 2 if api_key else 1}
    if sites != expected_sites:
        raise Unreadable('unrecognised account/login/start send site: ' + json.dumps(sites, sort_keys=True))
    native = sorted(set(re.findall(r'=>"([A-Za-z]+)"', oauth[0])))
    allowed = sorted(set(LITERAL.findall(generic[0])))
    result = {'account_sign_in_types': sorted(set(native) | set(allowed)),
              'native_sign_in_types': native, 'generic_route_allowed_types': allowed,
              'separate_api_key_login': None}
    if api_key:
        callers = sorted(n for n, text in sources.items() if API_KEY_CALLER.search(text) and n != 'hosting.rs')
        result['separate_api_key_login'] = {
            'type': 'apiKey', 'sent_from': callers,
            'standing': 'API-key login to a dedicated home, not account sign-in; outside the compared set'}
    return result


def derive(reader):
    pin_match = PIN.findall(reader.read('app/src-tauri/src/hosting.rs').decode('utf-8'))
    if len(pin_match) != 1:
        raise Unreadable('declared pin not found')
    pin = pin_match[0]
    raw = reader.read(SCHEMA.format(pin=pin))
    try:
        schema = json.loads(raw)
    except ValueError as error:
        raise Unreadable('schema is not JSON') from error
    definitions = compared_definitions(schema)
    named = {n: schema['definitions'].get(n) for n in NAMED}
    flow = sign_in_types(reader.rust_sources())
    return {'pin': pin, 'schema_path': SCHEMA.format(pin=pin), 'schema_file_sha256': sha(raw),
            'compared_definitions': sorted(definitions),
            'compared_set_sha256': sha(canonical(definitions)),
            'definition_sha256': {n: sha(canonical(v)) for n, v in definitions.items()},
            'named_set_sha256': sha(canonical(named)), **flow}


def baseline(tree):
    """The flow the retained record covers: fdcf608f's pin, its schema and its sign-in types."""
    record = json.loads(tree.read(RETAINED_RECORD))
    scope = record.get('scope') if isinstance(record, dict) else None
    text = json.dumps(record)
    if BASELINE['revision'] not in text or not all(t in text for t in BASELINE['account_sign_in_types']):
        raise Unreadable('retained record does not name the baseline revision and sign-in types')
    raw = tree.read(SCHEMA.format(pin=BASELINE['pin']))
    if sha(raw) != BASELINE['schema_file_sha256']:
        raise Unreadable('baseline schema bytes differ from those at the recorded revision')
    definitions = compared_definitions(json.loads(raw))
    named = {n: json.loads(raw)['definitions'].get(n) for n in NAMED}
    return {'revision': BASELINE['revision'], 'pin': BASELINE['pin'], 'retained_scope': scope,
            'schema_file_sha256': BASELINE['schema_file_sha256'],
            'compared_definitions': sorted(definitions), 'compared_set_sha256': sha(canonical(definitions)),
            'definition_sha256': {n: sha(canonical(v)) for n, v in definitions.items()},
            'named_set_sha256': sha(canonical(named)),
            'account_sign_in_types': list(BASELINE['account_sign_in_types'])}


def compare(source_root, record_root=None):
    """`unchanged` only when every input was read and nothing in the compared flow differs."""
    tree, retained = Tree(source_root), Tree(record_root or source_root)
    report = {'format': 'chirality-terms-sign-in-flow/v1',
              'standing': 'states no applicability; whether the position applies is the owner\'s statement (DEL-01-06 CLM-003)'}
    try:
        base = baseline(retained)
        candidate = derive(tree)
    except (Unreadable, ValueError, UnicodeDecodeError) as error:
        return report | {'status': 'unresolved', 'differences': [{'unreadable': str(error)}]}
    differences = []
    for name in sorted(set(base['definition_sha256']) | set(candidate['definition_sha256'])):
        before, after = base['definition_sha256'].get(name), candidate['definition_sha256'].get(name)
        if before != after:
            differences.append({'definition': name, 'baseline': before, 'candidate': after})
    if base['account_sign_in_types'] != candidate['account_sign_in_types']:
        differences.append({'account_sign_in_types': {'baseline': base['account_sign_in_types'],
                                                      'candidate': candidate['account_sign_in_types']}})
    status = 'unchanged' if not differences else 'unresolved'
    return report | {'status': status, 'baseline': base, 'candidate': candidate, 'differences': differences,
                     'named_set_equal': base['named_set_sha256'] == candidate['named_set_sha256']}


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
