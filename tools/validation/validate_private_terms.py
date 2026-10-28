#!/usr/bin/env python3
"""Private-term check for what a change adds: file contents, file paths and commit metadata.

The repository is public. The owner's machine names (the Mac's network name,
its host and computer names, earlier names it answered to) must never be
committed, in any form. This check keeps them out without publishing them:
the terms come from outside the repository and are never printed, and each is
matched in plain, split, escaped and character-class forms (`Ex""ample`,
`box[.]lan[.]example`, `\\u2019`, `%20`, `&#8217;` between its characters),
case-insensitively.

Terms (one per line; blank lines and `#` comments ignored) come from any of:
- the `PRIVATE_TERMS` environment variable (CI: the `PRIVATE_TERMS`
  repository secret; keep it to the terms only, since GitHub masks each line);
- `--terms-file PATH` (a local file kept outside the repository);
- `--from-host` (this machine's own names, read at run time: `hostname`, and
  on macOS `scutil --get LocalHostName` and `ComputerName`).
Terms shorter than six alphanumeric characters are not screened, and generic
names (`office-laptop`) would trip on ordinary text: list distinctive names.

What is screened, for `--base..--head` (or the index, with `--staged`):
- each added file whole, and each modified file's added lines;
- every file's raw bytes, binary or not (a NUL or any other non-word byte may
  sit between a term's characters, so UTF-16 text is caught too); `.gz` files
  and `.zip` members are also screened decompressed;
- each changed file's path;
- each new commit's author, committer and message (`--staged`: the identity
  the next commit will carry, which catches git's `user@<host>.local`
  default when `user.email` is unset).

Rules:
- BLOCK (exit 1): a private term, in any form. A finding names the place and
  the term's position in the list, never the term; paths are shown with any
  term masked as `<host>`.
- BLOCK (exit 1): a junit `<testsuite>`/`<testsuites>` `hostname` attribute
  with a real value, anywhere. Remove it before committing; empty, `<host>`
  and `&lt;host&gt;` pass. It needs no terms, so it runs without the secret.
- NOTE (exit 0): no terms configured (a pull request from a fork receives no
  secrets); only the junit rule ran. With `--require-terms` (CI on pushes and
  same-repository pull requests) a missing secret is an error instead.

Exit 2 on operational errors: refs unresolvable, an unreadable terms file,
or required terms missing. Errors never print terms, paths or file content.
"""
from __future__ import annotations

import argparse
import gzip
import io
import os
import re
import subprocess
import sys
import zipfile
import zlib

# Up to six separators may sit between any two characters of a term: non-word
# bytes (quotes, brackets, backslashes, dots, hyphens, spaces, NUL, CR) or
# escapes of one character (JSON \\uXXXX, \\xXX, percent-encoding, HTML entities).
JOINER = (rb'(?:[\W_]|\\u[0-9a-fA-F]{4}|\\x[0-9a-fA-F]{2}|%[0-9a-fA-F]{2}'
          rb'|&#[xX]?[0-9a-fA-F]{1,6};|&[a-zA-Z]{2,8};){0,6}')
MIN_TERM_CHARS = 6
JUNIT_HOST_RE = re.compile(rb'<testsuites?\b[^<>]*?\bhostname\s*=\s*\\?(["\'])(.*?)\\?\1')
PLACEHOLDER_HOSTS = {b'', b'<host>', b'&lt;host&gt;'}
MAX_ZIP_MEMBER = 512 * 1024 * 1024


class OperationalError(Exception):
    """Raised with a message that carries no term, path or content."""


def git(*args: str) -> bytes:
    try:
        return subprocess.run(['git', '-C', TOP, *args], capture_output=True, check=True).stdout
    except subprocess.CalledProcessError as exc:
        raise OperationalError(f'git {args[0]} failed (exit {exc.returncode})') from None


def term_pattern(term: str) -> re.Pattern[bytes] | None:
    """Every alphanumeric character of the term, in order, with joiners between them."""
    chars = [c for c in term if c.isalnum()]
    if len(chars) < MIN_TERM_CHARS:
        return None
    return re.compile(JOINER.join(re.escape(c.encode()) for c in chars), re.IGNORECASE)


def host_terms() -> list[str]:
    terms = []
    for command in (['hostname'], ['scutil', '--get', 'LocalHostName'], ['scutil', '--get', 'ComputerName']):
        try:
            value = subprocess.run(command, capture_output=True, text=True, check=False).stdout.strip()
        except OSError:
            continue
        if value:
            terms.append(value)
    return terms


def load_terms(args: argparse.Namespace) -> list[str]:
    raw = os.environ.get('PRIVATE_TERMS', '').splitlines()
    if args.terms_file:
        try:
            with open(args.terms_file, encoding='utf-8') as handle:
                raw += handle.read().splitlines()
        except (OSError, UnicodeDecodeError):
            raise OperationalError('the terms file cannot be read as UTF-8 text') from None
    if args.from_host:
        raw += host_terms()
    terms = []
    for line in raw:
        line = line.strip()
        if line and not line.startswith('#') and line not in terms:
            terms.append(line)
    return terms


def changes(args: argparse.Namespace) -> list[tuple[str, str]]:
    """(status, path) for each file added, modified or retyped; paths keep undecodable bytes."""
    span = ['--cached'] if args.staged else [args.base, args.head]
    out = git('diff', '--no-ext-diff', '--name-status', '--no-renames', '--diff-filter=AMT', '-z', *span, '--')
    fields = out.decode('utf-8', 'surrogateescape').split('\0')
    return [(status, path) for status, path in zip(fields[0::2], fields[1::2]) if path]


def blob(path: str, args: argparse.Namespace) -> bytes:
    return git('show', f':{path}' if args.staged else f'{args.head}:{path}')


def added_lines(path: str, args: argparse.Namespace) -> list[tuple[int, bytes]]:
    span = ['--cached'] if args.staged else [args.base, args.head]
    diff = git('diff', '--no-ext-diff', '--no-textconv', '--text', '--no-color', '-U0', *span, '--',
               f':(top,literal){path}')
    lines, number, in_hunk = [], 0, False
    for line in diff.split(b'\n'):
        hunk = re.match(rb'@@ -\S+ \+(\d+)', line)
        if hunk:
            number, in_hunk = int(hunk.group(1)), True
        elif in_hunk and line.startswith(b'+'):
            lines.append((number, line[1:]))
            number += 1
    return lines


def numbered(data: bytes) -> list[tuple[int, bytes]]:
    return list(enumerate(data.split(b'\n'), 1))


def units(status: str, path: str, args: argparse.Namespace) -> list[tuple[str, list[tuple[int, bytes]]]]:
    """(label, numbered lines) to screen for one changed file."""
    lower = path.lower()
    data = blob(path, args)
    result = []
    if lower.endswith('.gz'):
        try:
            result.append(('decompressed', numbered(gzip.decompress(data))))
        except (OSError, EOFError, zlib.error):
            result.append(('not decompressible', []))
            try:  # screen whatever a truncated or damaged stream still yields
                partial = zlib.decompressobj(31).decompress(data)
                if partial:
                    result.append(('partly decompressed', numbered(partial)))
            except zlib.error:
                pass
    if lower.endswith('.zip'):
        try:
            with zipfile.ZipFile(io.BytesIO(data)) as archive:
                for info in archive.infolist():
                    if info.is_dir():
                        continue
                    if info.file_size > MAX_ZIP_MEMBER:
                        result.append(('a zip member too large to expand', []))
                        continue
                    result.append((f'zip member {len(result) + 1}', numbered(archive.read(info))))
        except (zipfile.BadZipFile, OSError, EOFError, zlib.error, RuntimeError, NotImplementedError, UnicodeDecodeError):
            result.append(('not a readable zip', []))
    if status == 'M' and not lower.endswith(('.gz', '.zip')) and b'\0' not in data[:8192]:
        result.append(('', added_lines(path, args)))
    else:
        result.append(('', numbered(data)))
    return result


def masked(text: str, patterns: list[tuple[int, re.Pattern[bytes]]]) -> str:
    raw = text.encode('utf-8', 'surrogateescape')
    for _, pattern in patterns:
        raw = pattern.sub(b'<host>', raw)
    return raw.decode('utf-8', 'replace')


def scan(lines: list[tuple[int, bytes]], patterns: list[tuple[int, re.Pattern[bytes]]], where: str) -> list[str]:
    results = []
    for number, text in lines:
        for index, pattern in patterns:
            if pattern.search(text):
                results.append(f'{where}:{number}: private term {index} (any form)')
        for match in JUNIT_HOST_RE.finditer(text):
            if match.group(2) not in PLACEHOLDER_HOSTS:
                results.append(f'{where}:{number}: junit hostname attribute; remove it before committing')
                break
    return results


def metadata(args: argparse.Namespace, patterns: list[tuple[int, re.Pattern[bytes]]]) -> list[str]:
    results = []
    if args.staged:
        for var in ('GIT_AUTHOR_IDENT', 'GIT_COMMITTER_IDENT'):
            ident = git('var', var)
            for index, pattern in patterns:
                if pattern.search(ident):
                    results.append(f'the next commit\'s {var[4:-6].lower()} identity: private term {index} (any form)')
        return results
    for sha in git('rev-list', f'{args.base}..{args.head}').split():
        record = git('log', '-1', '--no-show-signature', '--format=%an%x00%ae%x00%cn%x00%ce%x00%B', sha.decode())
        fields = record.split(b'\0', 4)
        short = sha[:10].decode('ascii', 'replace')
        labelled = list(zip(('author name', 'author email', 'committer name', 'committer email', 'message'), fields))
        for index, pattern in patterns:
            hits = [label for label, value in labelled if pattern.search(value)]
            if not hits and pattern.search(record):
                hits = ['metadata']
            for label in hits:
                results.append(f'commit {short} {label}: private term {index} (any form)')
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--base', help='base revision (required unless --staged)')
    parser.add_argument('--head', default='HEAD')
    parser.add_argument('--staged', action='store_true', help='screen the index and the next commit identity')
    parser.add_argument('--terms-file', help='a file of private terms kept outside the repository')
    parser.add_argument('--from-host', action='store_true', help="also screen this machine's own names")
    parser.add_argument('--require-terms', action='store_true', help='treat a missing or empty term list as an error')
    args = parser.parse_args()
    if not args.staged and not args.base:
        parser.error('--base is required unless --staged')

    global TOP
    try:
        TOP = subprocess.run(['git', 'rev-parse', '--show-toplevel'], capture_output=True, text=True,
                             check=True).stdout.strip()
        terms = load_terms(args)
        if args.require_terms and not terms:
            raise OperationalError('private terms are required here, but PRIVATE_TERMS is unset or empty')
        patterns = [(index, pattern) for index, pattern in
                    ((i, term_pattern(t)) for i, t in enumerate(terms, 1)) if pattern is not None]
        short = len(terms) - len(patterns)
        changed = changes(args)
        results = []
        for status, path in changed:
            shown = masked(path, patterns)
            for index, pattern in patterns:
                if pattern.search(path.encode('utf-8', 'surrogateescape')):
                    results.append(f'path {shown}: private term {index} (any form)')
            for label, lines in units(status, path, args):
                if label in ('not decompressible', 'not a readable zip', 'a zip member too large to expand'):
                    print(f'NOTE: {shown}: {label}; its raw bytes are screened')
                    continue
                results += scan(lines, patterns, f'{shown} ({label})' if label else shown)
        results += metadata(args, patterns)
    except subprocess.CalledProcessError as exc:
        print(f'ERROR: git failed (exit {exc.returncode})', file=sys.stderr)
        return 2
    except OperationalError as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 2

    if not terms:
        print('NOTE: no private terms configured (PRIVATE_TERMS unset or empty); only the junit hostname rule ran.')
    if short:
        print(f'NOTE: {short} term(s) shorter than {MIN_TERM_CHARS} alphanumeric characters were not screened.')
    for message in results:
        print(f'BLOCK: {message}')
    print(f'{"BLOCK" if results else "PASS"}: {len(changed)} changed file(s) scanned against '
          f'{len(patterns)} private term(s); {len(results)} finding(s).')
    return 1 if results else 0


TOP = '.'

if __name__ == '__main__':
    raise SystemExit(main())
