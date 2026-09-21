import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).with_name('validate_conflict_markers.py')


@pytest.fixture
def repo(tmp_path):
    def git(*args):
        return subprocess.run(['git', *args], cwd=tmp_path, check=True,
                              capture_output=True, text=True)
    git('init', '-q')
    git('config', 'user.name', 'Fixture')
    git('config', 'user.email', 'fixture@example.invalid')
    (tmp_path / 'sample.md').write_text('base\n')
    git('add', '.')
    git('commit', '-qm', 'base')
    base = git('rev-parse', 'HEAD').stdout.strip()
    return tmp_path, git, base


def check(repo, content, base_override=None, filename="sample.md"):
    root, git, base = repo
    (root / filename).write_text(content)
    # Path attributes can re-enable whitespace regardless of core.whitespace;
    # they must not make cosmetic findings block this check.
    (root / '.gitattributes').write_text('*.md whitespace=blank-at-eol,blank-at-eof\n')
    git('add', '.')
    git('commit', '-qm', 'candidate')
    return subprocess.run([sys.executable, str(SCRIPT), '--base', base_override or base],
                          cwd=root, capture_output=True, text=True)


def test_cosmetic_whitespace_and_markdown_hard_breaks_pass(repo):
    result = check(repo, 'hard break  \n\t indented\n\n')
    assert result.returncode == 0, result.stdout + result.stderr


def test_conflict_markers_still_block_with_cosmetic_findings(repo):
    result = check(repo, 'trailing  \n<<<<<<< HEAD\nleft\n=======\nright\n>>>>>>> other\n')
    assert result.returncode == 1
    assert 'leftover conflict marker' in result.stdout
    assert 'trailing whitespace' not in result.stdout


def test_git_failure_is_not_reported_as_clean(repo):
    result = check(repo, 'valid\n', 'missing-ref')
    assert result.returncode == 1
    assert 'PASS' not in result.stdout


def test_conflict_markers_in_plus_prefixed_filename_block(repo):
    result = check(repo, '<<<<<<< HEAD\nleft\n=======\nright\n>>>>>>> other\n', filename='+sample.md')
    assert result.returncode == 1
    assert '+sample.md:1: leftover conflict marker' in result.stdout


def test_cosmetic_source_line_resembling_diagnostic_does_not_block(repo):
    result = check(repo, ' \tpretend.md:1: leftover conflict marker\n')
    assert result.returncode == 0, result.stdout + result.stderr
