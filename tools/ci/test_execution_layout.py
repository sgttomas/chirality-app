"""Outcome tests: executable content and invocations cannot re-enter execution/."""
import json
from pathlib import Path
import shutil
import subprocess

import pytest

from tools.ci import check_execution_layout as guard


@pytest.fixture
def repo(tmp_path):
    subprocess.run(['git', 'init', '-q', str(tmp_path)], check=True)
    manifest = 'tools/ci/execution-fidelity.json'
    paths = [manifest, *[r['path'] for r in json.loads((guard.ROOT / manifest).read_bytes())['exceptions']]]
    for name in paths:
        target = tmp_path / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(guard.ROOT / name, target)
    return tmp_path


def write(root, name, raw):
    target = root / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(raw)
    return target


def test_approved_fidelity_records_are_data_and_hash_bound(repo):
    assert guard.check(repo)['fidelity_records'] == 1
    row = json.loads((repo / 'tools/ci/execution-fidelity.json').read_bytes())['exceptions'][0]
    with (repo / row['path']).open('ab') as stream:
        stream.write(b'\nchanged')
    with pytest.raises(ValueError, match='Fidelity bytes changed'):
        guard.check(repo)


@pytest.mark.parametrize('name,raw', [
    ('new.py', b'print("new code")\n'),
    ('hidden.txt', b'#!/usr/bin/env python3\nprint(1)\n'),
    ('new.mjs', b'console.log(1)\n'),
    ('launcher', b'{\n  \"_run\": [\"python\", \"x.md\"]\n}'),
    ('hidden.bin', b'\x7fELF\x00code'),
    ('new.html', b'<html><script>run()</script></html>'),
])
def test_new_code_is_rejected_even_without_executable_mode(repo, name, raw):
    write(repo, 'execution/new/' + name, raw)
    with pytest.raises(ValueError, match='Runnable code belongs outside'):
        guard.check(repo)


def test_executable_mode_on_document_is_rejected(repo):
    write(repo, 'execution/new/notes.md', b'document\n').chmod(0o755)
    with pytest.raises(ValueError, match='Runnable code belongs outside'):
        guard.check(repo)


@pytest.mark.parametrize('name,raw', [
    ('.github/workflows/bad.yml', b'run: python3 execution/notes.md\n'),
    ('tools/bad.py', b'from execution.example import run\n'),
    ('tools/bad.py', b'from runpy import run_path; run_path("execution/new/notes.md")\n'),
    ('tools/bad.py', b'from runpy import run_path as execute; execute("execution/new/notes.md")\n'),
    ('tools/bad.py', b'import subprocess; subprocess.run(["python3", "execution/new/notes.md"])\n'),
    ('tools/bad.py', b'from subprocess import run as launch; launch(["python3", "execution/new/notes.md"])\n'),
    ('tools/bad.py', b'import sys, subprocess; subprocess.run([sys.executable, "execution/new/notes.md"])\n'),
    ('tools/bad.py', b'from pathlib import Path; exec(Path("execution/new/notes.md").read_text())\n'),
    ('tools/bad.py', b'import importlib.util\nimportlib.util.spec_from_file_location("bad", "execution/notes.md")\n'),
])
def test_import_or_invocation_cannot_use_documentary_extension(repo, name, raw):
    write(repo, name, raw)
    with pytest.raises(ValueError, match='(?:invocation|Import|Dynamic module)'):
        guard.check(repo)


def test_declarative_spec_data_does_not_become_an_execution_exception(repo):
    write(repo, 'execution/new/spec.json', b'{"schema": "data"}\n')
    write(repo, 'tools/read.py', b'from pathlib import Path\nPath("execution/new/spec.json").read_bytes()\n')
    assert guard.check(repo)['fidelity_records'] == 1


def test_native_successor_dependencies_resolve_to_operational_sources():
    import importlib.util
    path = guard.ROOT / 'app/examination/native_support/native_successor_setup.py'
    spec = importlib.util.spec_from_file_location('_layout_successor_sources', path)
    setup = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(setup)
    assert setup.REPO == guard.ROOT
    dependencies = setup.dependency_digests()
    retained = guard.ROOT / 'app/examination/native_support/retained-controller-v2.py.txt'
    assert str(retained) in dependencies
    assert dependencies[str(retained)] == '91c9ca98d7bf8d784e2cea5cbd42d237230b9018d58f5e04e369a755d5b7720c'
    # Import class definitions only; do not instantiate AX or invoke a campaign.
    assert setup.load_base().load_ax().__name__ == 'ScopedAX'


@pytest.mark.parametrize('source', [
    'import subprocess; subprocess.run("/usr/bin/python3 execution/probe/notes.md", shell=True)',
    'import subprocess; subprocess.run(["python3", "-W", "ignore", "execution/probe/notes.md"])',
    'import os; os.execl("/usr/bin/python3", "python3", "execution/probe/notes.md")',
    'import os; os.execv("/usr/bin/python3", ["python3", "execution/probe/notes.md"])',
    'import os; os.spawnv(0, "/usr/bin/python3", ["python3", "execution/probe/notes.md"])',
])
def test_literal_interpreter_options_absolute_shell_and_exec_argv_are_guarded(repo, source):
    write(repo, 'tools/probe.py', source.encode())
    with pytest.raises(ValueError, match='Interpreter invocation'):
        guard.check(repo)


@pytest.mark.parametrize('quote', ["'", '"'])
def test_shell_quoting_does_not_hide_interpreter_path(repo, quote):
    command = quote + '/usr/bin/python3' + quote + ' execution/probe/notes.md'
    source = 'import subprocess; subprocess.run(' + repr(command) + ', shell=True)'
    write(repo, 'tools/probe.py', source.encode())
    with pytest.raises(ValueError, match='Interpreter invocation'):
        guard.check(repo)


@pytest.mark.parametrize('quote', ["'", '"'])
@pytest.mark.parametrize('surface', ['shell', 'workflow-block', 'workflow-scalar'])
def test_quoted_interpreters_in_shell_files_and_workflows_are_guarded(repo, quote, surface):
    import yaml
    command = quote + '/usr/bin/python3' + quote + ' execution/probe/notes.md'
    write(repo, 'execution/probe/notes.md', b'print("must not run from execution")\n')
    if surface == 'shell':
        write(repo, 'tools/probe.sh', ('#!/bin/sh\nset -eu\n' + command + '\n').encode())
    elif surface == 'workflow-block':
        text = 'jobs:\n  probe:\n    steps:\n      - run: |\n          set -eu\n          ' + command + '\n'
        write(repo, '.github/workflows/probe.yml', text.encode())
    else:
        workflow = {'jobs': {'probe': {'steps': [{'run': command}]}}}
        write(repo, '.github/workflows/probe.yml', yaml.safe_dump(workflow).encode())
    with pytest.raises(ValueError, match='Interpreter invocation'):
        guard.check(repo)
