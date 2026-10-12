import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).with_name('validate_run_record_leaks.py')
# Assembled at runtime so this test file never itself carries a matchable token.
GITHUB_TOKEN = 'ghp_' + 'a1B2c3D4e5F6g7H8i9J0k1L2m3N4o5P6q7R8'
RUN = 'projects/x/execution/_Coordination/AgentRuns/RUN-1/'


@pytest.fixture
def repo(tmp_path):
    def git(*args):
        return subprocess.run(['git', *args], cwd=tmp_path, check=True, capture_output=True, text=True)
    git('init', '-q')
    git('config', 'user.name', 'Fixture')
    git('config', 'user.email', 'fixture@example.invalid')
    old = tmp_path / RUN / 'old.md'
    old.parent.mkdir(parents=True)
    old.write_text(f'pre-existing history {GITHUB_TOKEN}\n')  # history is not re-scanned
    git('add', '.')
    git('commit', '-qm', 'base')
    return tmp_path, git, git('rev-parse', 'HEAD').stdout.strip()


def run(repo, files):
    root, git, base = repo
    for name, content in files.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content if isinstance(content, bytes) else content.encode())
    git('add', '.')
    git('commit', '-qm', 'change')
    return subprocess.run([sys.executable, str(SCRIPT), '--base', base, '--head', 'HEAD'],
                          cwd=root, capture_output=True, text=True)


def test_credential_in_new_run_record_blocks(repo):
    result = run(repo, {RUN + 'transcript.md': f'token={GITHUB_TOKEN}\n'})
    assert result.returncode == 1
    assert 'possible github-token' in result.stdout and GITHUB_TOKEN not in result.stdout


@pytest.mark.parametrize('secret', [
    '"Authorization": "Bearer ' + 'Zx9' * 12 + '"',
    'eyJ' + 'hbGciOiJIUzI1NiJ9' + '.eyJ' + 'zdWIiOiIxMjM0NTY3ODkwIn0' + '.' + 'Qk9' * 8,
    'aws_secret_access_key = ' + 'wJalrXUtnFEMIK7MDENGbPxRfiCY' + 'Zx9Qk9Zx9Qk9',
    'glpat-' + 'Zx9Qk9' * 4,
    'https://hooks.slack.com/services/' + 'T0AB12CD3/B0AB12CD3/' + 'Zx9Qk9' * 4,
])
def test_more_credential_formats_block(repo, secret):
    result = run(repo, {RUN + 'response.json': secret + '\n'})
    assert result.returncode == 1, result.stdout


def test_history_and_fake_values_pass(repo):
    result = run(repo, {'docs/notes.md': 'ordinary notes\n',
                        RUN + 'fixture.txt': 'AKIAIOSFODNN7EXAMPLE sk-ant-dummy-value-for-tests-0123456789abcdef\n',
                        'projects/x/execution/PKG-1/_run_records/r.json': '{"ok": true}\n'})
    assert result.returncode == 0, result.stdout
    assert '3 changed file(s) scanned' in result.stdout


def test_large_or_binary_evidence_warns_without_blocking(repo):
    result = run(repo, {RUN + 'trace.zip': b'\0' * 5_000_001})
    assert result.returncode == 0
    assert 'WARN:' in result.stdout and 'CI artifacts' in result.stdout


def test_unresolvable_base_is_operational_error(repo):
    root, _, _ = repo
    result = subprocess.run([sys.executable, str(SCRIPT), '--base', 'nope', '--head', 'HEAD'],
                            cwd=root, capture_output=True, text=True)
    assert result.returncode == 2


def link(repo, links):
    """Commit `links` ({path: target}) as symlinks and run the check."""
    root, git, base = repo
    for name, target in links.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists() or path.is_symlink():
            path.unlink()
        path.symlink_to(target)
    git('add', '.')
    git('commit', '-qm', 'links')
    return subprocess.run([sys.executable, str(SCRIPT), '--base', base, '--head', 'HEAD'],
                          cwd=root, capture_output=True, text=True)


@pytest.mark.parametrize('target', [
    '/Users/example/worktree/frame_kernel/src/lib.rs',
    '../../../../../../../../outside.txt',
    '~/notes.md',
])
def test_machine_local_or_escaping_symlink_blocks(repo, target):
    result = link(repo, {RUN + 'fixture/lib.rs': target})
    assert result.returncode == 1, result.stdout
    assert 'symlink to a machine-local path' in result.stdout
    assert '0 possible credential(s); 1 machine-local symlink(s)' in result.stdout


def test_file_retyped_to_symlink_blocks(repo):
    result = link(repo, {RUN + 'old.md': '/tmp/old.md'})
    assert result.returncode == 1, result.stdout
    assert 'old.md: symlink to a machine-local path' in result.stdout


def test_symlink_inside_repository_passes(repo):
    result = link(repo, {RUN + 'fixture/lib.rs': '../../../../../../../docs/lib.rs'})
    assert result.returncode == 0, result.stdout
    assert '1 changed file(s) scanned' in result.stdout


@pytest.mark.parametrize("path", ["docs/notes.md", "fixtures/response.json", "tools/helper.py"])
def test_credential_outside_retired_record_paths_blocks(repo, path):
    result = run(repo, {path: f"token={GITHUB_TOKEN}\n"})
    assert result.returncode == 1
    assert "possible github-token" in result.stdout
