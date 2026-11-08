#!/usr/bin/env python3
"""Enforce the declarative execution tree and the fidelity-only exception boundary.

This is a source/layout guard, not a proof about arbitrary program behavior.
New code surfaces or dynamic execution routes require explicit review here.
"""
from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]
CODE_SUFFIXES = frozenset({'.py', '.pyw', '.sh', '.bash', '.zsh', '.fish', '.mjs', '.cjs',
                          '.js', '.ts', '.tsx', '.jsx', '.rs', '.c', '.h', '.cpp', '.hpp',
                          '.swift', '.go', '.rb', '.pl', '.ps1', '.bat', '.cmd', '.wasm',
                          '.ipynb', '.jar', '.class', '.exe', '.dll', '.dylib', '.so', '.o'})


def tracked(root):
    raw = subprocess.check_output(['git', '-C', str(root), 'ls-files', '-z', '--cached', '--others', '--exclude-standard'])
    return sorted({p.decode() for p in raw.split(b'\0') if p and ((root / p.decode()).is_file() or (root / p.decode()).is_symlink())})


def code_surface(path, raw, mode):
    launcher = False
    if raw.lstrip().startswith(b'{'):
        try:
            value = json.loads(raw)
            launcher = isinstance(value, dict) and '_run' in value
        except (ValueError, UnicodeError):
            pass
    return (path.suffix.lower() in CODE_SUFFIXES or bool(mode & 0o111)
            or raw.startswith(b'#!') or b'<script' in raw.lower() or b'\0' in raw
            or launcher or path.name in {'Makefile', 'Justfile', 'Dockerfile'})


def check(root=ROOT):
    root = Path(root)
    catalog = json.loads((root / 'tools/ci/execution-fidelity.json').read_bytes())
    exceptions = {row['path']: row for row in catalog['exceptions']}
    if len(exceptions) != len(catalog['exceptions']) or len(exceptions) != 9:
        raise ValueError('The reviewed nine fidelity exceptions must be explicit and unique')
    errors, seen = [], set()
    paths = tracked(root)
    for name in paths:
        path = root / name
        if not name.startswith('execution/'):
            continue
        if path.is_symlink():
            errors.append('Linked execution input refused: ' + name)
            continue
        raw = path.read_bytes()
        if name in exceptions:
            seen.add(name)
            if hashlib.sha256(raw).hexdigest() != exceptions[name]['sha256']:
                errors.append('Fidelity bytes changed: ' + name)
        elif code_surface(path, raw, path.stat().st_mode):
            errors.append('Runnable code belongs outside execution/: ' + name)
    errors += ['Missing fidelity record: ' + p for p in sorted(exceptions.keys() - seen)]
    # Reject direct imports and literal interpreter invocations, including scripts
    # disguised as data. Code inventory above catches new indirect code paths.
    invocation = re.compile(r'(?:python[\d.]*|node|bash|zsh|sh|source|\.)\s+[^\n]*?\bexecution/[^\s\"\'`]+')
    for name in paths:
        if not name.startswith(('app/', 'tools/', '.github/')) or '/frozen/' in name:
            continue
        path = root / name
        if path.suffix not in CODE_SUFFIXES | {'.yml', '.yaml'}:
            continue
        text = path.read_text(errors='replace')
        # The guard's regression fixtures contain intentionally forbidden examples.
        if name == 'tools/ci/test_execution_layout.py':
            continue
        if (path.suffix in {'.sh', '.bash', '.zsh'} or name.startswith('.github/')) and invocation.search(text):
            errors.append('Interpreter invocation into execution/: ' + name)
        if path.suffix == '.py':
            try:
                tree = ast.parse(text)
            except SyntaxError:
                errors.append('Unparseable Python reader: ' + name)
                continue
            for node in ast.walk(tree):
                modules = ([a.name for a in node.names] if isinstance(node, ast.Import)
                           else [node.module or ''] if isinstance(node, ast.ImportFrom) else [])
                if any(m == 'execution' or m.startswith('execution.') for m in modules):
                    errors.append('Import from execution/: ' + name)
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr in {'spec_from_file_location', 'run_path'}:
                    literals = [n.value for n in ast.walk(node) if isinstance(n, ast.Constant) and isinstance(n.value, str)]
                    if any(re.search(r'(^|/)execution/', x) for x in literals):
                        errors.append('Dynamic module from execution/: ' + name)
    if errors:
        raise ValueError('\n'.join(errors))
    return {'fidelity_records': len(seen), 'tracked_paths_checked': len(paths)}


if __name__ == '__main__':
    print(json.dumps(check(), sort_keys=True))
