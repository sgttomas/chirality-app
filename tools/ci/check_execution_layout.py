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
import shlex
import subprocess

import yaml

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
            or path.name.endswith('.py.txt') or launcher or path.name in {'Makefile', 'Justfile', 'Dockerfile'})


def execution_literal(node):
    return any(isinstance(n, ast.Constant) and isinstance(n.value, str)
               and re.search(r'(?:^|[/\s\"\'])execution(?:/|$)', n.value)
               for n in ast.walk(node))


def shell_execution_calls(command):
    """Inspect literal interpreter commands after removing shell quoting."""
    try:
        words = shlex.split(command, comments=True)
    except ValueError:
        if re.search(r'\bexecution/', command):
            yield 'Unparseable invocation into execution/'
        return
    for index, word in enumerate(words):
        interpreter = re.fullmatch(r'(?:.*/)?(?:python[\d.]*|node|bash|sh|zsh|source|\.)', word)
        if interpreter and any(re.search(r'(?:^|[/\s\"\'])execution(?:/|$)', arg) for arg in words[index + 1:]):
            yield 'Interpreter invocation into execution/'
            break
    if words and re.search(r'(^|/)execution/', words[0]):
        yield 'Interpreter invocation into execution/'


def workflow_commands(value):
    if isinstance(value, dict):
        for key, item in value.items():
            if key == 'run' and isinstance(item, str):
                yield item
            else:
                yield from workflow_commands(item)
    elif isinstance(value, list):
        for item in value:
            yield from workflow_commands(item)


def execution_calls(tree):
    """Ordinary Python imports/loaders and subprocess forms, including aliases."""
    aliases = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for item in node.names:
                aliases[item.asname or item.name.split('.')[0]] = item.name if item.asname else item.name.split('.')[0]
        elif isinstance(node, ast.ImportFrom):
            for item in node.names:
                aliases[item.asname or item.name] = (node.module or '') + '.' + item.name
    def qualified(node):
        if isinstance(node, ast.Name):
            return aliases.get(node.id, node.id)
        if isinstance(node, ast.Attribute):
            return qualified(node.value) + '.' + node.attr
        return ''
    loaders = {'runpy.run_path', 'importlib.util.spec_from_file_location',
               'importlib.machinery.SourceFileLoader', 'importlib.machinery.SourcelessFileLoader',
               'exec', 'eval', 'compile', 'builtins.exec', 'builtins.eval', 'builtins.compile'}
    processes = {'subprocess.run', 'subprocess.Popen', 'subprocess.call', 'subprocess.check_call',
                 'subprocess.check_output', 'os.system', 'os.popen', 'os.execl', 'os.execv',
                 'os.execve', 'os.execvp', 'os.execvpe', 'os.execlp', 'os.execle', 'os.execlpe',
                 'os.spawnv', 'os.spawnve', 'os.spawnvp', 'os.spawnvpe', 'os.spawnl', 'os.spawnle', 'os.spawnlp', 'os.spawnlpe', 'asyncio.create_subprocess_exec',
                 'asyncio.create_subprocess_shell'}
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        name = qualified(node.func)
        if name in loaders and execution_literal(node):
            yield 'Dynamic module from execution/'
        if name in {'importlib.import_module', '__import__', 'builtins.__import__'}:
            if any(isinstance(arg, ast.Constant) and isinstance(arg.value, str)
                   and (arg.value == 'execution' or arg.value.startswith('execution.')) for arg in node.args):
                yield 'Import from execution/'
        if name not in processes:
            continue
        if name.startswith(('os.exec', 'os.spawn')) or name == 'asyncio.create_subprocess_exec':
            index = 1 if name.startswith('os.spawn') else 0
            if len(node.args) > index:
                program = node.args[index]
                interpreter = (isinstance(program, ast.Constant) and isinstance(program.value, str)
                               and re.fullmatch(r'(?:.*/)?(?:python[\d.]*|node|bash|sh|zsh)', program.value)) or qualified(program) == 'sys.executable'
                if execution_literal(program) or (interpreter and any(execution_literal(arg) for arg in node.args[index + 1:])):
                    yield 'Interpreter invocation into execution/'
        command = node.args[0] if node.args else next((k.value for k in node.keywords if k.arg == 'args'), None)
        if command is None:
            continue
        if isinstance(command, (ast.List, ast.Tuple)) and command.elts:
            program, *arguments = command.elts
            if execution_literal(program):
                yield 'Interpreter invocation into execution/'
            interpreter = (isinstance(program, ast.Constant) and isinstance(program.value, str)
                           and re.fullmatch(r'(?:.*/)?(?:python[\d.]*|node|bash|sh|zsh)', program.value)) or qualified(program) == 'sys.executable'
            if interpreter and any(execution_literal(argument) for argument in arguments):
                # Conservative for interpreter argv: option operands and embedded
                # -c programs cannot hide a reference into the documentary tree.
                yield 'Interpreter invocation into execution/'
        elif isinstance(command, ast.Constant) and isinstance(command.value, str):
            yield from shell_execution_calls(command.value)

def check(root=ROOT):
    root = Path(root)
    catalog = json.loads((root / 'tools/ci/execution-fidelity.json').read_bytes())
    exceptions = {row['path']: row for row in catalog['exceptions']}
    if len(exceptions) != len(catalog['exceptions']) or len(exceptions) != 1:
        raise ValueError('The one reviewed fidelity exception must be explicit and unique')
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
        if path.suffix not in CODE_SUFFIXES | {'.yml', '.yaml'} and not path.name.endswith('.py.txt'):
            continue
        text = path.read_text(errors='replace')
        # The guard's regression fixtures contain intentionally forbidden examples.
        if name == 'tools/ci/test_execution_layout.py':
            continue
        if (path.suffix in {'.sh', '.bash', '.zsh'} or name.startswith('.github/')) and invocation.search(text):
            errors.append('Interpreter invocation into execution/: ' + name)
        commands = [text] if path.suffix in {'.sh', '.bash', '.zsh'} else []
        if name.startswith('.github/') and path.suffix in {'.yml', '.yaml'}:
            try:
                commands = list(workflow_commands(yaml.safe_load(text)))
            except yaml.YAMLError:
                errors.append('Unparseable workflow: ' + name)
        for command in commands:
            for line in command.replace('\\\n', '').splitlines():
                errors.extend(reason + ': ' + name for reason in shell_execution_calls(line))
        if path.suffix == '.py' or path.name.endswith('.py.txt'):
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
            errors.extend(reason + ': ' + name for reason in execution_calls(tree))
    if errors:
        raise ValueError('\n'.join(errors))
    return {'fidelity_records': len(seen), 'tracked_paths_checked': len(paths)}


if __name__ == '__main__':
    print(json.dumps(check(), sort_keys=True))
