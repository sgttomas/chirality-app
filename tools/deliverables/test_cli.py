"""Behavioral tests of dependency queries and their observation boundaries."""
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).parent))
import cli


def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args], text=True).strip()


@pytest.fixture
def repo(tmp_path, monkeypatch):
    git(tmp_path, 'init', '-q')
    git(tmp_path, 'config', 'user.email', 'fixture@example.com')
    git(tmp_path, 'config', 'user.name', 'Fixture')
    (tmp_path / 'project').mkdir()
    (tmp_path / '.keep').write_text('fixture')
    git(tmp_path, 'add', '.')
    git(tmp_path, 'commit', '-qm', 'initial')
    monkeypatch.chdir(tmp_path)
    return tmp_path


def put(repo, identifier, needs=(), **fields):
    path = repo / 'project' / 'execution' / identifier / 'deliverable.yaml'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(dict(id=identifier, needs=list(needs), **fields)))
    return path


def query(capsys, *args):
    code = cli.main(['--project', 'project', *args])
    return code, json.loads(capsys.readouterr().out)


def test_unknown_conditions_cycles_and_non_gating_are_not_completion(repo, capsys):
    put(repo, 'DEL-01-01', [{'from': 'DEL-01-02', 'condition': 'interface'},
                           {'from': 'DEL-01-02', 'condition': 'qualification', 'gating': False},
                           {'from': 'DEL-99-99', 'condition': 'future input'}])
    put(repo, 'DEL-01-02', [{'from': 'DEL-01-01', 'condition': 'mutual design'}])
    code, result = query(capsys, 'check')
    assert code == 0
    assert result['cycles'] == [['DEL-01-01', 'DEL-01-02']]
    assert len(result['needs']) == 4
    assert all(row['suitability'] == 'unknown' for row in result['needs'])
    assert len(result['unknown']) == 1
    assert result['basis']['revision'] == git(repo, 'rev-parse', 'HEAD')
    assert result['basis']['working_tree_changes']
    code, result = query(capsys, 'impact', 'DEL-01-01')
    assert result['affected'] == ['DEL-01-02']


def test_distinct_cases_unknowns_and_queries_preserve_declarations(repo, capsys):
    path = put(repo, 'DEL-01-01', [
        {'from': 'DEL-01-02', 'condition': 'rating for winter case', 'when': 'winter review'},
        {'from': 'DEL-01-02', 'condition': 'rating for summer case', 'when': 'summer review', 'gating': False},
        {'from': 'unknown', 'condition': 'identify owner review source'},
        {'from': 'external:recipient', 'direction': 'downstream', 'condition': 'provide agreed drawing'},
    ])
    put(repo, 'DEL-01-02')
    before = path.read_bytes(), path.stat().st_mtime_ns
    for command in (('check',), ('neighborhood', 'DEL-01-01'), ('impact', 'DEL-01-02')):
        code, result = query(capsys, *command)
        assert code == 0, result
        assert (path.read_bytes(), path.stat().st_mtime_ns) == before
        if command[0] == 'neighborhood':
            assert len(result['upstream']) == 3 and len(result['outputs']) == 1
            assert [row['when'] for row in result['upstream'][:2]] == ['winter review', 'summer review']
        if command[0] == 'impact':
            assert result['affected'] == ['DEL-01-01']
            assert len(result['relationships']) == 4


def test_identity_binding_and_native_outward_duplicates_are_rejected(repo, capsys):
    path = put(repo, 'DEL-01-01')
    path.write_text('id: DEL-01-02\nneeds: []\n')
    code, result = query(capsys, 'check')
    assert code == 2 and 'disagrees with deliverable identity DEL-01-01' in result['errors'][0]
    path.write_text('id: DEL-01-01\nneeds:\n- from: DEL-01-02\n  direction: downstream\n  condition: drawing\n')
    code, result = query(capsys, 'check')
    assert code == 2 and 'native consumers declare their own needs' in result['errors'][0]


def test_flat_or_phase_locality_label_does_not_change_stable_identity(repo, capsys):
    path = repo / 'project/execution/PKG-01/1_Working/DEL-01-01_Drawing-Set/deliverable.yaml'
    path.parent.mkdir(parents=True)
    path.write_text('id: DEL-01-01\nneeds: []\n')
    code, result = query(capsys, 'check')
    assert code == 0 and result['deliverables'] == 1
    assert cli.parse(path.read_text(), str(path), expected_id='DEL-01-01')['id'] == 'DEL-01-01'
    with pytest.raises(cli.Invalid, match='disagrees'):
        cli.parse(path.read_text(), str(path), expected_id='DEL-02-01')


def test_typed_targets_and_present_evidence_do_not_claim_satisfaction(repo, capsys):
    (repo / 'project' / 'interface.md').write_text('a stub')
    put(repo, 'DEL-01-01', [{'from': 'doc:interface.md', 'condition': 'correct interface',
                           'evidence': 'interface.md::contract'},
                          {'from': 'external:consumer', 'condition': 'provide schema',
                           'direction': 'downstream', 'gating': False},
                          {'from': 'package:PKG-02', 'condition': 'package input'}])
    code, result = query(capsys, 'neighborhood', 'DEL-01-01')
    assert code == 0
    assert len(result['outputs']) == 1
    assert len(result['upstream']) == 2
    assert result['upstream'][0]['supplier']['state'] == 'observed'
    assert result['upstream'][0]['suitability'] == 'unknown'
    assert 'no check executed' in result['upstream'][0]['evidence_fact']['meaning']


def test_touches_shared_relevance_and_unmapped_paths(repo, capsys):
    for identifier in ['DEL-01-01', 'DEL-01-02']:
        put(repo, identifier, code_paths=['src/**'])
    put(repo, 'DEL-01-03')
    (repo / 'project' / 'src').mkdir()
    (repo / 'project' / 'src' / 'a.py').write_text('old')
    git(repo, 'add', '.')
    git(repo, 'commit', '-qm', 'code')
    (repo / 'project' / 'src' / 'a.py').write_text('new')
    (repo / '.keep').write_text('unmapped')
    git(repo, 'add', '.')
    git(repo, 'commit', '-qm', 'selected change')
    (repo / 'later.txt').write_text('not part of the commit')
    code, result = query(capsys, 'touches', 'HEAD')
    assert code == 0
    assert sorted(result['relevant']) == ['DEL-01-01', 'DEL-01-02']
    assert result['unknown_deliverables'] == ['DEL-01-03']
    assert result['unmapped_paths'] == ['.keep']


def stub_gh(bin_dir, monkeypatch, response):
    """Put a fake `gh` first on PATH that records its arguments and prints `response`."""
    (bin_dir / 'response.json').write_text(json.dumps(response))
    gh = bin_dir / 'gh'
    gh.write_text(f'#!/bin/sh\nprintf "%s\\n" "$@" > "{bin_dir}/args"\ncat "{bin_dir}/response.json"\n')
    gh.chmod(0o755)
    monkeypatch.setenv('PATH', f'{bin_dir}{os.pathsep}{os.environ["PATH"]}')
    return bin_dir


def test_touches_pr_diffs_base_and_head_locally_beyond_github_file_limit(repo, capsys, monkeypatch, tmp_path_factory):
    put(repo, 'DEL-01-01', code_paths=['src/mapped/**'])
    git(repo, 'add', '.')
    git(repo, 'commit', '-qm', 'deliverable')
    fork = git(repo, 'rev-parse', 'HEAD')
    git(repo, 'switch', '-qc', 'feature')
    changed = [f'project/src/mapped/m{index:03}.rs' for index in range(30)]
    changed += [f'project/src/other/o{index:03}.rs' for index in range(120)]
    for path in changed:
        (repo / path).parent.mkdir(parents=True, exist_ok=True)
        (repo / path).write_text(path)
    git(repo, 'add', '.')
    git(repo, 'commit', '-qm', 'pull request with 150 files')
    head = git(repo, 'rev-parse', 'HEAD')
    git(repo, 'switch', '-q', '-')
    (repo / 'project' / 'base-only.txt').write_text('later base change, not part of the PR')
    git(repo, 'add', '.')
    git(repo, 'commit', '-qm', 'base moves on')
    base = git(repo, 'rev-parse', 'HEAD')
    truncated = [{'path': path} for path in sorted(changed)[:100]]
    bin_dir = stub_gh(tmp_path_factory.mktemp('gh'), monkeypatch,
                      {'baseRefOid': base, 'headRefOid': head, 'files': truncated,
                       'url': 'https://github.com/example/repo/pull/7'})
    code, result = query(capsys, 'touches', 'PR:7')
    assert code == 0, result
    args = (bin_dir / 'args').read_text().split()
    assert args[:3] == ['pr', 'view', '7'] and 'files' not in args[args.index('--json') + 1]
    assert result['selection'] == {'pr': 'https://github.com/example/repo/pull/7', 'base': base,
                                   'head': head, 'diff': f'{base}...{head}'}
    assert sorted(result['relevant']['DEL-01-01']) == sorted(changed[:30])
    assert sorted(result['unmapped_paths']) == sorted(changed[30:])
    assert fork != base and 'project/base-only.txt' not in result['unmapped_paths']


def test_touches_preserves_distinct_control_characters_in_git_paths(repo, capsys, monkeypatch, tmp_path_factory):
    put(repo, 'DEL-01-01')
    git(repo, 'add', '.')
    git(repo, 'commit', '-qm', 'deliverable')
    base = git(repo, 'rev-parse', 'HEAD')
    changed = ['project/line\rbreak.txt', 'project/line\nbreak.txt',
               'project/tab\tname.txt', 'project/tick`name.txt']
    for path in changed:
        (repo / path).write_text('distinct path')
    git(repo, 'add', '.')
    git(repo, 'commit', '-qm', 'unusual filenames')
    head = git(repo, 'rev-parse', 'HEAD')
    stub_gh(tmp_path_factory.mktemp('gh'), monkeypatch,
            {'baseRefOid': base, 'headRefOid': head, 'url': 'https://github.com/example/repo/pull/7'})
    for selection in ('PR:7', f'{base}...{head}'):
        code, result = query(capsys, 'touches', selection)
        assert code == 0, result
        assert sorted(result['unmapped_paths']) == sorted(changed)


def test_touches_pr_with_missing_local_commit_fails_without_partial_list(repo, capsys, monkeypatch, tmp_path_factory):
    base = git(repo, 'rev-parse', 'HEAD')
    absent = 'f' * 40
    bin_dir = tmp_path_factory.mktemp('gh')
    stub_gh(bin_dir, monkeypatch, {'baseRefOid': base, 'headRefOid': absent,
                                   'files': [{'path': '.keep'}], 'url': 'https://github.com/example/repo/pull/8'})
    code, result = query(capsys, 'touches', 'PR:8')
    assert code == 2
    assert 'unmapped_paths' not in result and 'relevant' not in result
    assert result['errors'] == [f'https://github.com/example/repo/pull/8: head commit {absent} is not in this '
                                f'repository; fetch it (for example `git fetch origin {absent}`) and retry']
    stub_gh(bin_dir, monkeypatch, {'url': 'https://github.com/example/repo/pull/9'})
    code, result = query(capsys, 'touches', 'PR:9')
    assert code == 2 and result['errors'] == ['https://github.com/example/repo/pull/9: gh returned no base commit']


def test_dag_diff_tracks_conditions_and_gating_but_not_folder_moves(repo, capsys):
    original = put(repo, 'DEL-01-01', [{'from': 'external:vendor', 'condition': 'v1', 'gating': False}])
    git(repo, 'add', '.')
    git(repo, 'commit', '-qm', 'baseline')
    git(repo, 'tag', 'baseline')
    moved = repo / 'project' / 'execution' / 'PKG-01' / '1_Working' / 'DEL-01-01' / 'deliverable.yaml'
    moved.parent.mkdir(parents=True)
    original.rename(moved)
    code, result = query(capsys, 'dag-diff', 'baseline')
    assert code == 0 and result['added'] == result['removed'] == []
    data = yaml.safe_load(moved.read_text())
    data['needs'][0].update(condition='v2', gating=True)
    moved.write_text(yaml.safe_dump(data))
    code, result = query(capsys, 'dag-diff', 'baseline')
    assert result['added'][0]['condition'] == 'v2'
    assert result['added'][0]['gating'] is True
    assert result['removed'][0]['condition'] == 'v1'


def test_escaped_paths_and_symlinks_are_not_read(repo, capsys):
    put(repo, 'DEL-01-01', code_paths=['../private/**'])
    code, result = query(capsys, 'check')
    assert code == 2 and 'escapes' in result['errors'][0]
    target = repo / 'outside.yaml'
    target.write_text('id: DEL-02-02\nneeds: []\n')
    path = repo / 'project' / 'evil' / 'deliverable.yaml'
    path.parent.mkdir()
    path.symlink_to(target)
    code, result = query(capsys, 'check')
    assert code == 2 and any('contained regular file' in error for error in result['errors'])


def test_reference_symlink_is_unknown_without_reading_target(repo, capsys):
    outside = repo / 'private.txt'
    outside.write_text('private')
    (repo / 'project' / 'link.txt').symlink_to(outside)
    put(repo, 'DEL-01-01', [{'from': 'doc:link.txt', 'condition': 'input'}])
    code, result = query(capsys, 'check')
    assert code == 0
    assert result['needs'][0]['supplier']['state'] == 'unknown'


def test_duplicate_yaml_and_identities_fail_with_partial_results(repo, capsys):
    put(repo, 'DEL-01-01')
    duplicate = repo / 'project' / 'duplicate' / 'deliverable.yaml'
    duplicate.parent.mkdir()
    duplicate.write_text('id: DEL-01-01\nneeds: []\n')
    code, result = query(capsys, 'check')
    assert code == 2 and 'duplicate identity' in result['errors'][0]
    duplicate.write_text('id: DEL-01-02\nneeds: []\nneeds: []\n')
    code, result = query(capsys, 'check')
    assert code == 2 and 'duplicate or non-string YAML key' in result['errors'][0]
    assert result['deliverables'] == 1


def test_missing_project_or_identity_is_explicit(repo, capsys):
    code, result = query(capsys, 'neighborhood', 'DEL-01-01')
    assert code == 0 and result['state'] == 'unknown'
    code = cli.main(['--project', '../outside', 'check'])
    result = json.loads(capsys.readouterr().out)
    assert code == 2 and result['errors']


def test_touches_single_revision_ranges_and_root_commit_ignore_worktree(repo):
    initial = git(repo, 'rev-parse', 'HEAD')
    assert cli.changed_paths(repo, initial)[0] == ['.keep']
    (repo / 'first.txt').write_text('first')
    git(repo, 'add', '.')
    git(repo, 'commit', '-qm', 'first')
    first = git(repo, 'rev-parse', 'HEAD')
    (repo / 'second.txt').write_text('second')
    git(repo, 'add', '.')
    git(repo, 'commit', '-qm', 'second')
    assert cli.changed_paths(repo, 'HEAD')[0] == ['second.txt']
    (repo / '.keep').write_text('dirty unrelated content')
    assert cli.changed_paths(repo, first)[0] == ['first.txt']
    assert cli.changed_paths(repo, 'HEAD')[0] == ['second.txt']
    assert cli.changed_paths(repo, initial + '..HEAD')[0] == ['first.txt', 'second.txt']
