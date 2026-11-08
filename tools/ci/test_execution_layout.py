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


def test_removing_manifest_row_cannot_exempt_a_drifting_schema(tmp_path):
    from unittest.mock import patch
    manifest_path = execution_inputs.MANIFEST
    manifest = json.loads(manifest_path.read_bytes())
    manifest['data'] = [row for row in manifest['data'] if not row['source'].endswith('/RS_RECORD.schema.json')]
    original = Path.read_bytes
    def removed(path):
        return json.dumps(manifest).encode() if path == manifest_path else original(path)
    with patch.object(Path, 'read_bytes', removed), pytest.raises(ValueError, match='Unregistered or missing App input'):
        execution_inputs.check()


def test_schema_consumer_cannot_select_an_unregistered_source():
    from unittest.mock import patch
    schema = execution_inputs.ROOT / 'app/src-tauri/schemas/manifest.json'
    value = json.loads(schema.read_bytes())
    value['resources'][0]['source'] = 'execution/PKG-04/DEL-04-03/Work/new-unregistered.schema.json'
    original = Path.read_bytes
    def changed(path):
        return json.dumps(value).encode() if path == schema else original(path)
    with patch.object(Path, 'read_bytes', changed), pytest.raises(ValueError, match='Consumer requires data registration'):
        execution_inputs.check()


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


def test_reclassifying_schema_as_code_cannot_exempt_freshness():
    from unittest.mock import patch
    manifest_path = execution_inputs.MANIFEST
    value = json.loads(manifest_path.read_bytes())
    row = next(row for row in value['data'] if row['source'].endswith('/RS_RECORD.schema.json'))
    value['data'].remove(row)
    value['code'].append({'source': row['source'], 'path': row['copy'], 'sha256': row['sha256'], 'bound': False})
    original = Path.read_bytes
    def changed(path):
        if path == manifest_path:
            return json.dumps(value).encode()
        if path == execution_inputs.ROOT / row['copy']:
            return b'{"changed":true}\n'
        return original(path)
    with patch.object(Path, 'read_bytes', changed), pytest.raises(ValueError, match='cannot exempt a retained authoring input'):
        execution_inputs.check()


@pytest.mark.parametrize('quote', ["'", '"'])
def test_shell_quoting_does_not_hide_interpreter_path(repo, quote):
    command = quote + '/usr/bin/python3' + quote + ' execution/probe/notes.md'
    source = 'import subprocess; subprocess.run(' + repr(command) + ', shell=True)'
    write(repo, 'tools/probe.py', source.encode())
    with pytest.raises(ValueError, match='Interpreter invocation'):
        guard.check(repo)
