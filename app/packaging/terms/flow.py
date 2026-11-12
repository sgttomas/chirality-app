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

The sign-in types come only from the exact expression forms in FORMS and GENERIC_GUARD below.
Every occurrence of the literal "account/login/start" in host source must be accounted for under
RULES, and each is reported by file and line; an occurrence the tool cannot account for, a stated
form spelt differently, or syntax it cannot read makes the result `unresolved`. Unknown never
reads as unchanged.

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
METHOD = 'account/login/start'
SOURCE_DIR = 'app/src-tauri/src'

# The exact expression forms this tool was written against. Each is compared after stripping the
# line's leading and trailing whitespace and nothing else; any other spelling is not recognised.
FORMS = {
    'native sign-in sender': (
        re.compile(r'let kind=match mode\{((?:NativeLoginMode::[A-Za-z]+=>"[A-Za-z]+",)*NativeLoginMode::[A-Za-z]+=>"[A-Za-z]+")\};'),
        'let source=self.request_begin_scoped("account/login/start",json!({"type":kind}),json!({"kind":"person-directed"}),false,Some(generation))?;'),
    'API-key sender': (
        re.compile(re.escape('let params=input.into_params();Self::validate_native_result("LoginAccountParams",&params).map_err(|_|"native API-key input shape invalid; sensitive diagnostic withheld".to_string())?;')),
        'let source=self.request_begin_scoped_private("account/login/start",params,json!({"kind":"person-directed"}),false,Some(generation),true,None,None)?;'),
}
GENERIC_GUARD = ('if method == "account/login/start"', '&& !matches!(', 'params["type"].as_str(),',
                 re.compile(r'Some\(("[A-Za-z]+"(?: \| "[A-Za-z]+")*)\)'), ')', '{')
API_KEY_PARAMS = ('pub(crate) fn into_params(self) -> Value {', 'json!({"type":"apiKey","apiKey":self.value})', '}')
API_KEY_CALLER = re.compile(r'\.account_login_api_key_from_native_entry\(')
RULES = (
    'Every .rs file under app/src-tauri/src, at any depth, is host source, except a file named *_tests.rs that '
    'host source names only from items gated by #[cfg(test)] or #[cfg(all(test, ...))]; items so gated are not read.',
    'Every string literal equal to "account/login/start" in host source is accounted for, by file and line, as one of: '
    'the native sign-in sender, the API-key sender, the generic route guard (each in its exact stated form), a comparison '
    '(== or !=), a match pattern (followed by =>, or by an if guard and =>), or a pattern inside matches!(...). '
    'Any other occurrence, or a stated form spelt differently, is unresolved.',
    'A literal that contains "login/start" without equalling the method, a concat! naming account, a #[path] or include! '
    'reaching outside app/src-tauri/src, an unterminated literal or comment, or unbalanced braces is unresolved.',
    'Method names assembled at run time are outside what reading literals can show; the generic route guard, read in its '
    'exact form, is the boundary for a method name chosen at run time.',
)
class Unreadable(Exception):
    pass


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


CHAR = re.compile(r"'(?:\\(?:u\{[0-9a-fA-F_]{1,8}\}|x[0-9a-fA-F]{2}|[nrt\\0'\"])|[^\\'\n])'")
RAW = re.compile(r'b?r(#*)"')
ESCAPE = re.compile(r'\\(u\{([0-9a-fA-F_]{1,8})\}|x([0-9a-fA-F]{2})|.)', re.S)
SIMPLE = {'n': '\n', 'r': '\r', 't': '\t', '\\': '\\', '0': '\0', "'": "'", '"': '"'}


def lex(text):
    """Mask comments and literal contents (keeping offsets and line breaks) and list string literals
    as (start, end, value). Raises Unreadable on an unterminated literal or comment."""
    masked, literals, i, n = list(text), [], 0, len(text)
    def blank(a, b):
        for k in range(a, b):
            if masked[k] != '\n':
                masked[k] = ' '
    while i < n:
        c = text[i]
        ident_before = i > 0 and (text[i - 1].isalnum() or text[i - 1] == '_')
        if text.startswith('//', i):
            j = text.find('\n', i); j = n if j < 0 else j
            blank(i, j); i = j
        elif text.startswith('/*', i):
            depth, j = 1, i + 2
            while depth:
                if j >= n:
                    raise Unreadable('unterminated block comment')
                if text.startswith('/*', j):
                    depth += 1; j += 2
                elif text.startswith('*/', j):
                    depth -= 1; j += 2
                else:
                    j += 1
            blank(i, j); i = j
        elif not ident_before and (m := RAW.match(text, i)):
            close = '"' + m.group(1)
            j = text.find(close, m.end())
            if j < 0:
                raise Unreadable('unterminated raw string')
            literals.append((i, j + len(close), text[m.end():j]))
            blank(m.end(), j); i = j + len(close)
        elif c == '"' or (c == 'b' and not ident_before and text.startswith('b"', i)):
            start = i + (2 if c == 'b' else 1)
            j = start
            while True:
                if j >= n:
                    raise Unreadable('unterminated string')
                if text[j] == '\\':
                    j += 2
                elif text[j] == '"':
                    break
                else:
                    j += 1
            body = text[start:j]
            def unescape(m):
                if m.group(2):
                    return chr(int(m.group(2).replace('_', ''), 16))
                if m.group(3):
                    return chr(int(m.group(3), 16))
                return SIMPLE.get(m.group(1), '' if m.group(1) == '\n' else '\\' + m.group(1))
            literals.append((i, j + 1, ESCAPE.sub(unescape, body)))
            blank(start, j); i = j + 1
        elif c == "'" and (m := CHAR.match(text, i)):
            blank(i + 1, m.end() - 1); i = m.end()
        else:
            i += 1
    return ''.join(masked), literals


TEST_CFG = re.compile(r'test|all\(\s*test\s*(?:,[^()]*)?\)|all\([^()]*,\s*test\s*(?:,[^()]*)?\)')
ATTRIBUTE = re.compile(r'#\[\s*cfg\s*\(')


def matching(masked, at, opening, closing):
    depth = 0
    for k in range(at, len(masked)):
        if masked[k] == opening:
            depth += 1
        elif masked[k] == closing:
            depth -= 1
            if depth == 0:
                return k
    raise Unreadable(f'unbalanced {opening}{closing}')


def test_regions(masked):
    """Spans of items gated by a test-only cfg attribute, and whether the whole file is."""
    spans = []
    if re.search(r'#!\[\s*cfg\s*\(\s*test\s*\)\s*\]', masked):
        return [(0, len(masked))], True
    for m in ATTRIBUTE.finditer(masked):
        if any(a <= m.start() < b for a, b in spans):
            continue
        close = matching(masked, m.end() - 1, '(', ')')
        if not TEST_CFG.fullmatch(masked[m.end():close].strip()):
            continue
        end_attr = matching(masked, m.start() + 1, '[', ']')
        k, depth = end_attr + 1, 0
        while k < len(masked):
            ch = masked[k]
            if ch in '([':
                depth += 1
            elif ch in ')]':
                depth -= 1
            elif depth == 0 and ch == ';':
                break
            elif depth == 0 and ch == '{':
                k = matching(masked, k, '{', '}')
                break
            k += 1
        else:
            raise Unreadable('test item has no end')
        spans.append((m.start(), k + 1))
    return spans, False


def enclosing(masked, at):
    """Open groups around an offset, innermost first: (opening offset, char, word before it)."""
    groups, stack = [], []
    for k in range(at):
        ch = masked[k]
        if ch in '([{':
            stack.append(k)
        elif ch in ')]}' and stack:
            stack.pop()
    for k in reversed(stack):
        word = re.search(r'([A-Za-z_][A-Za-z0-9_]*!?)\s*$', masked[:k])
        groups.append((k, masked[k], word.group(1) if word else ''))
    return groups


def classify(masked, start, end):
    before, after = masked[:start].rstrip(), masked[end:].lstrip()
    if before.endswith(('==', '!=')) or after.startswith(('==', '!=')):
        return 'comparison'
    if after.startswith('=>') or re.match(r'if\b[^;{}]*=>', after):
        return 'match pattern'
    for k, ch, word in enclosing(masked, start):
        if ch != '(':
            break
        if word == 'matches!':
            depth, first_comma = 0, None
            for j in range(k + 1, start):
                if masked[j] in '([{':
                    depth += 1
                elif masked[j] in ')]}':
                    depth -= 1
                elif masked[j] == ',' and depth == 0:
                    first_comma = j
                    break
            return 'matches! pattern' if first_comma is not None else None
        close = matching(masked, k, '(', ')')
        if masked[close + 1:].lstrip().startswith('=>'):
            return 'match pattern'
    return None


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
        """Every .rs file under the source folder at any depth: relative path -> text."""
        folder = self.root / SOURCE_DIR
        found = []
        def walk(directory, prefix):
            try:
                entries = sorted(os.scandir(directory), key=lambda e: e.name)
            except OSError as error:
                raise Unreadable(f'{SOURCE_DIR}/{prefix}: {type(error).__name__}') from error
            for entry in entries:
                if entry.is_symlink():
                    raise Unreadable(f'{SOURCE_DIR}/{prefix}{entry.name}: symbolic link refused')
                if entry.is_dir(follow_symlinks=False):
                    walk(entry.path, prefix + entry.name + '/')
                elif entry.name.endswith('.rs'):
                    found.append(prefix + entry.name)
        walk(folder, '')
        return {n: self.read(f'{SOURCE_DIR}/{n}').decode('utf-8') for n in found}


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
        names = self._git('ls-tree', '-r', '--name-only', self.revision, '--', SOURCE_DIR).decode().split('\n')
        names = sorted(n[len(SOURCE_DIR) + 1:] for n in names if n.endswith('.rs'))
        return {n: self.read(f'{SOURCE_DIR}/{n}').decode('utf-8') for n in names}


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


def _lines_at(text, offset):
    return text.count('\n', 0, offset) + 1


def _stripped_lines(text):
    return [line.strip() for line in text.split('\n')]


def account_senders(sources):
    """Account for every occurrence of the method literal in host source; derive the sign-in types."""
    lexed, skipped_text, problems = {}, [], []
    for name, text in sources.items():
        masked, literals = lex(text)
        spans, whole = test_regions(masked)
        lexed[name] = (text, masked, literals, spans)
        skipped_text.extend(text[a:b] for a, b in spans)
    def in_test(name, offset):
        return any(a <= offset < b for a, b in lexed[name][3])
    host, excluded = [], []
    for name in sorted(sources):
        base = name.rsplit('/', 1)[-1]
        text, masked, literals, spans = lexed[name]
        named_in_tests = any(base in s for s in skipped_text)
        named_elsewhere = any(base in v[0] and any(lit[2].endswith(base) and not in_test(other, lit[0]) for lit in v[2])
                              for other, v in lexed.items() if other != name)
        if spans == [(0, len(masked))] or (base.endswith('_tests.rs') and named_in_tests and not named_elsewhere):
            excluded.append(name)
        else:
            host.append(name)
    examined, oauth, generic, api_key = [], [], [], []
    for name in host:
        text, masked, literals, spans = lexed[name]
        lines = _stripped_lines(text)
        for start, end, value in literals:
            if in_test(name, start):
                continue
            line = _lines_at(text, start)
            here = lines[line - 1]
            previous = lines[line - 2] if line >= 2 else ''
            if value != METHOD:
                if 'login/start' in value:
                    problems.append({'file': name, 'line': line, 'unrecognised': 'literal names the method in another form'})
                continue
            form = None
            for label, (prior, exact) in FORMS.items():
                if here == exact:
                    if (m := prior.fullmatch(previous)):
                        form = label
                        if label == 'native sign-in sender':
                            oauth.append(sorted(set(re.findall(r'=>"([A-Za-z]+)"', m.group(1)))))
                        else:
                            api_key.append(name)
                    break
            if form is None and here == GENERIC_GUARD[0] and name.rsplit('/', 1)[-1] == 'auth_rpc.rs':
                following = lines[line:line + 5]
                if (len(following) == 5 and following[0] == GENERIC_GUARD[1] and following[1] == GENERIC_GUARD[2]
                        and (m := GENERIC_GUARD[3].fullmatch(following[2])) and following[3:] == list(GENERIC_GUARD[4:])):
                    form = 'generic route guard'
                    generic.append(sorted(set(re.findall(r'"([A-Za-z]+)"', m.group(1)))))
            if form is None and not any(here.startswith(e) or e in here for e in (f[1] for f in FORMS.values())):
                form = classify(masked, start, end)
            if form is None:
                problems.append({'file': name, 'line': line, 'unrecognised': here[:200]})
            else:
                examined.append({'file': name, 'line': line, 'form': form})
        for m in re.finditer(r'#\[\s*path\s*=\s*"([^"]*)"\s*\]|include!\(\s*"([^"]*)"\s*\)', text):
            if in_test(name, m.start()):
                continue
            target = os.path.normpath(os.path.join(os.path.dirname(name), m.group(1) or m.group(2)))
            if target.startswith('..') or os.path.isabs(target):
                problems.append({'file': name, 'line': _lines_at(text, m.start()), 'unrecognised': 'source outside app/src-tauri/src'})
        for m in re.finditer(r'concat!\s*\(', masked):
            close = matching(masked, m.end() - 1, '(', ')')
            if not in_test(name, m.start()) and any(m.start() <= s < close and 'account' in v for s, e, v in literals):
                problems.append({'file': name, 'line': _lines_at(text, m.start()), 'unrecognised': 'concat! naming account'})
    if len(oauth) != 1:
        problems.append({'unrecognised': f'native sign-in sender found {len(oauth)} times; exactly one expected'})
    if len(generic) != 1:
        problems.append({'unrecognised': f'generic route guard found {len(generic)} times; exactly one expected'})
    if api_key:
        auth = next((lexed[n][0] for n in host if n.rsplit('/', 1)[-1] == 'auth_rpc.rs'), '')
        lines = _stripped_lines(auth)
        if not any(lines[k:k + 3] == list(API_KEY_PARAMS) for k in range(len(lines))):
            problems.append({'unrecognised': 'API-key sender without the stated into_params form'})
    native = oauth[0] if len(oauth) == 1 else []
    allowed = generic[0] if len(generic) == 1 else []
    result = {'account_sign_in_types': sorted(set(native) | set(allowed)),
              'native_sign_in_types': native, 'generic_route_allowed_types': allowed,
              'senders_examined': examined, 'unaccounted': problems,
              'host_source_files': len(host), 'test_files_not_read': excluded,
              'separate_api_key_login': None}
    if api_key:
        callers = sorted(n for n in host if API_KEY_CALLER.search(lexed[n][1]) and n.rsplit('/', 1)[-1] != 'hosting.rs')
        result['separate_api_key_login'] = {
            'type': 'apiKey', 'sent_from': callers,
            'standing': 'API-key login to a dedicated home, not account sign-in; outside the compared types'}
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
    flow = account_senders(reader.rust_sources())
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
    report = {'format': 'chirality-terms-sign-in-flow/v1', 'rules': list(RULES),
              'standing': 'states no applicability; whether the position applies is the owner\'s statement (DEL-01-06 CLM-003)'}
    try:
        base = baseline(retained)
        candidate = derive(tree)
    except (Unreadable, ValueError, UnicodeDecodeError, RecursionError) as error:
        return report | {'status': 'unresolved', 'differences': [{'unreadable': str(error)}]}
    differences = []
    for name in sorted(set(base['definition_sha256']) | set(candidate['definition_sha256'])):
        before, after = base['definition_sha256'].get(name), candidate['definition_sha256'].get(name)
        if before != after:
            differences.append({'definition': name, 'baseline': before, 'candidate': after})
    if candidate['unaccounted']:
        differences.append({'unaccounted': candidate['unaccounted']})
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
