#!/usr/bin/env python3
"""Scan added or modified committed files for credential leaks and escaping links.

The historical command name remains compatible with CI callers. The scope is
all changed files, including maintained source, fixtures and documentation now
that routine run records are retired. Unchanged history is not re-scanned.
Binary formats are skipped; large files receive a non-blocking artifact warning.
Reads bytes from Git for sparse-checkout compatibility. Exit 2 means the input
revision could not be read; exit 1 means a credential or escaping link was found.
"""
from __future__ import annotations

import argparse
import posixpath
import re
import subprocess
import sys

BINARY_EXTENSIONS = ('.zip', '.png', '.jpg', '.jpeg', '.gif', '.webp', '.webm', '.gz', '.sqlite3', '.bin', '.pdf')
LARGE_BYTES = 5_000_000
SYMLINK_MODE = '120000'
FAKE_RE = re.compile(r'(?i)example|dummy|fake|placeholder|test')
PATTERNS = {
    'aws-access-key': r'\b(?:AKIA|ASIA)[0-9A-Z]{16}\b',
    'github-token': r'\b(?:gh[pousr]_[A-Za-z0-9]{36,}|github_pat_[A-Za-z0-9_]{60,})\b',
    'anthropic-key': r'\bsk-ant-[A-Za-z0-9_-]{32,}',
    'openai-key': r'\bsk-(?!ant-)(?:proj-|svcacct-)?[A-Za-z0-9_-]{40,}',
    'slack-token': r'\bxox[abposr]-[A-Za-z0-9-]{10,}',
    'google-api-key': r'\bAIza[0-9A-Za-z_-]{35}\b',
    'stripe-live-key': r'\b[rs]k_live_[0-9A-Za-z]{20,}',
    'private-key': r'-----BEGIN (?:RSA |EC |DSA |OPENSSH |PGP |ENCRYPTED )?PRIVATE KEY(?: BLOCK)?-----',
    'bearer-token': r'(?i)\bauthorization["\']?\s*[:=]\s*["\']?bearer\s+[A-Za-z0-9._~+/-]{32,}',
    'jwt': r'\beyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{20,}',
    'aws-secret-key': r'(?i)aws_?secret_?access_?key["\']?\s*[:=]\s*["\']?[A-Za-z0-9/+]{40}\b',
    'gitlab-token': r'\bglpat-[A-Za-z0-9_-]{20,}',
    'huggingface-token': r'\bhf_[A-Za-z]{34,}\b',
    'npm-token': r'\bnpm_[A-Za-z0-9]{36}\b',
    'slack-webhook': r'https://hooks\.slack\.com/services/T[A-Z0-9]+/B[A-Z0-9]+/[A-Za-z0-9]{20,}',
}
COMPILED = {name: re.compile(pattern) for name, pattern in PATTERNS.items()}


def git(*args: str) -> bytes:
    return subprocess.check_output(['git', *args])


def changed_files(base: str, head: str) -> list[tuple[str, str]]:
    """(path, head mode) for each file added, modified or retyped."""
    fields = git('diff', '--raw', '--no-renames', '--diff-filter=AMT', '-z', base, head, '--').decode().split('\0')
    # --raw -z alternates ':<old mode> <new mode> <old oid> <new oid> <status>' and the path.
    return [(path, meta.split()[1]) for meta, path in zip(fields[0::2], fields[1::2])]


def escapes_repository(path: str, target: str) -> bool:
    if target.startswith(('/', '\\', '~')) or re.match(r'^[A-Za-z]:[\\/]', target):
        return True
    resolved = posixpath.normpath(posixpath.join(posixpath.dirname(path), target))
    return resolved == '..' or resolved.startswith('../')


def findings(path: str, data: bytes, mode: str = '100644') -> list[tuple[str, str]]:
    results = []
    if mode == SYMLINK_MODE:
        target = data.decode('utf-8', errors='replace')
        if escapes_repository(path, target):
            results.append(('BLOCK', f'{path}: symlink to a machine-local path ({target}); '
                                     'commit the evidence bytes, not a link'))
        return results
    if len(data) > LARGE_BYTES:
        results.append(('WARN', f'{path}: {len(data) / 1e6:.1f} MB committed file; keep large evidence as CI artifacts'))
    if path.lower().endswith(BINARY_EXTENSIONS):
        return results
    text = data.decode('utf-8', errors='ignore')
    for name, pattern in COMPILED.items():
        for match in pattern.finditer(text):
            if not FAKE_RE.search(match.group(0)):
                line = text.count('\n', 0, match.start()) + 1
                results.append(('BLOCK', f'{path}:{line}: possible {name} ({match.group(0)[:8]}…)'))
                break
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--base', required=True)
    parser.add_argument('--head', default='HEAD')
    args = parser.parse_args()
    try:
        paths = changed_files(args.base, args.head)
        results = [f for p, mode in paths for f in findings(p, git('show', f'{args.head}:{p}'), mode)]
    except subprocess.CalledProcessError as exc:
        print(f'ERROR: cannot read {args.base}..{args.head}: {exc}', file=sys.stderr)
        return 2
    for severity, message in results:
        print(f'{severity}: {message}')
    blocks = sum(severity == 'BLOCK' for severity, _ in results)
    links = sum(severity == 'BLOCK' and 'symlink to' in message for severity, message in results)
    print(f'{"BLOCK" if blocks else "PASS"}: {len(paths)} changed file(s) scanned; '
          f'{blocks - links} possible credential(s); {links} machine-local symlink(s).')
    return 1 if blocks else 0


if __name__ == '__main__':
    raise SystemExit(main())
