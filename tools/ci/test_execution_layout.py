"""Outcome tests: executable content and invocations cannot re-enter execution/."""
import json
from pathlib import Path
import shutil
import subprocess

import pytest

from tools.ci import check_execution_layout as guard
from tools.ci import execution_inputs
from tools.ci import check_documentary_sources


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
    assert guard.check(repo)['fidelity_records'] == 9
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
    ('tools/bad.py', b'import importlib.util\nimportlib.util.spec_from_file_location("bad", "execution/notes.md")\n'),
])
def test_import_or_invocation_cannot_use_documentary_extension(repo, name, raw):
    write(repo, name, raw)
    with pytest.raises(ValueError, match='(?:invocation|Import|Dynamic module)'):
        guard.check(repo)


def test_declarative_spec_data_does_not_become_an_execution_exception(repo):
    write(repo, 'execution/new/spec.json', b'{"schema": "data"}\n')
    write(repo, 'tools/read.py', b'from pathlib import Path\nPath("execution/new/spec.json").read_bytes()\n')
    assert guard.check(repo)['fidelity_records'] == 9


def test_current_projection_extents_remain_governing():
    report = check_documentary_sources.check()
    assert report['current_projection_groups'] == 68
    assert report['selector_applications'] == 772


def test_copied_inputs_keep_full_or_existing_selected_correspondence():
    assert execution_inputs.check() > 0


def test_static_staging_preserves_bound_bytes_and_only_translates_basis_paths(tmp_path):
    import importlib.util
    import hashlib
    path = guard.ROOT / 'app/packaging/static_distribution/check.py'
    spec = importlib.util.spec_from_file_location('_layout_static_source', path)
    static = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(static)
    scratch = tmp_path / 'static'
    scratch.mkdir()
    model, _ = static.source_model(static.Frozen(scratch / 'artifacts'), scratch)
    original = json.loads((scratch / 'original-basis.json').read_bytes())
    assert not (scratch / 'source/execution').exists()
    assert '/app/contract_inputs/' in model.__file__
    model_bytes = Path(model.__file__).read_bytes()
    row = next(x for x in json.loads((guard.ROOT / 'tools/ci/execution-inputs.json').read_bytes())['code']
               if x['source'].endswith('/distribution-s1/model.py'))
    assert hashlib.sha256(model_bytes).hexdigest() == row['sha256']
    staged = model.BASIS
    assert {k: v for k, v in original.items() if k != 'reads'} == {k: v for k, v in staged.items() if k != 'reads'}
    for before, after in zip(original['reads'], staged['reads'], strict=True):
        assert {k: v for k, v in before.items() if k != 'path'} == {k: v for k, v in after.items() if k != 'path'}
        assert not after['path'].startswith(('execution/', 'projects/'))
