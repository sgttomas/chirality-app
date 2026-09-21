from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


SCRIPT = Path(__file__).with_name("validate_candidate_whitespace.py")


def git(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=repo,
        text=True,
        capture_output=True,
        check=True,
    )


def write(path: Path, data: str | bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(data, bytes):
        path.write_bytes(data)
    else:
        path.write_text(data, encoding="utf-8")


def init_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init", "-q")
    git(repo, "config", "user.name", "Whitespace Test")
    git(repo, "config", "user.email", "whitespace@example.invalid")
    write(repo / ".gitignore", "ignored/\n")
    write(repo / "tracked.md", "clean\n")
    git(repo, "add", ".")
    git(repo, "commit", "-qm", "basis")
    return repo


def run_validator(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--repo-root", str(repo), *args],
        text=True,
        capture_output=True,
        check=False,
    )


def test_clean_untracked_markdown_passes(tmp_path: Path) -> None:
    repo = init_repo(tmp_path)
    write(repo / "candidate.md", "clean\n")

    result = run_validator(repo)

    assert result.returncode == 0
    assert "PASS: candidate whitespace is clean" in result.stdout


def test_untracked_markdown_reports_spaces_tabs_and_eof_blank_line(
    tmp_path: Path,
) -> None:
    repo = init_repo(tmp_path)
    write(repo / "candidate.md", b"space  \ntab\t\n\n")

    result = run_validator(repo)

    assert result.returncode == 1
    assert "candidate.md:1: trailing whitespace" in result.stdout
    assert "candidate.md:2: trailing whitespace" in result.stdout
    assert "candidate.md:3: blank line at end of file" in result.stdout


def test_single_posix_final_newline_is_allowed(tmp_path: Path) -> None:
    repo = init_repo(tmp_path)
    write(repo / "candidate.md", "one final newline\n")

    result = run_validator(repo)

    assert result.returncode == 0


def test_tracked_diff_behavior_is_delegated_to_git(tmp_path: Path) -> None:
    repo = init_repo(tmp_path)
    write(repo / "tracked.md", "dirty  \n")

    expected_result = subprocess.run(
        ["git", "diff", "--check"],
        cwd=repo,
        text=True,
        capture_output=True,
        check=False,
    )
    expected = expected_result.stdout
    result = run_validator(repo)

    assert expected_result.returncode != 0
    assert result.returncode == 1
    assert expected
    assert expected in result.stdout
    assert "tracked.md:1: trailing whitespace." in result.stdout


def test_staged_tracked_diff_is_checked(tmp_path: Path) -> None:
    repo = init_repo(tmp_path)
    write(repo / "tracked.md", "dirty\t\n")
    git(repo, "add", "tracked.md")

    result = run_validator(repo)

    assert result.returncode == 1
    assert "Tracked whitespace findings (staged changes)" in result.stdout
    assert "tracked.md:1: trailing whitespace." in result.stdout


def test_ignored_and_binary_untracked_files_are_not_scanned(tmp_path: Path) -> None:
    repo = init_repo(tmp_path)
    write(repo / "ignored" / "bad.md", "ignored  \n")
    write(repo / "image.bin", b"\x89PNG\x00binary  \n")

    result = run_validator(repo)

    assert result.returncode == 0
    assert "safely skipped: 1" in result.stdout
    assert "ignored/bad.md" not in result.stdout
    assert "image.bin" not in result.stdout


def test_git_attributes_can_mark_untracked_file_binary(tmp_path: Path) -> None:
    repo = init_repo(tmp_path)
    write(repo / ".gitattributes", "*.snapshot -diff -text\n")
    git(repo, "add", ".gitattributes")
    git(repo, "commit", "-qm", "attributes")
    write(repo / "opaque.snapshot", b"text-shaped bytes  \n")

    result = run_validator(repo)

    assert result.returncode == 0
    assert "safely skipped: 1" in result.stdout


def test_explicit_text_attribute_overrides_binary_suffix_fallback(
    tmp_path: Path,
) -> None:
    repo = init_repo(tmp_path)
    write(repo / ".gitattributes", "*.pdf text\n")
    git(repo, "add", ".gitattributes")
    git(repo, "commit", "-qm", "attributes")
    write(repo / "text-shaped.pdf", b"must scan  \n")

    result = run_validator(repo)

    assert result.returncode == 1
    assert "text-shaped.pdf:1: trailing whitespace" in result.stdout


def test_path_scope_limits_tracked_and_untracked_checks(tmp_path: Path) -> None:
    repo = init_repo(tmp_path)
    write(repo / "inside" / "bad.md", "bad  \n")
    write(repo / "outside" / "bad.md", "bad  \n")

    result = run_validator(repo, "--paths", "inside")

    assert result.returncode == 1
    assert "inside/bad.md:1: trailing whitespace" in result.stdout
    assert "outside/bad.md" not in result.stdout


def test_path_scope_is_literal_not_git_pathspec_magic(tmp_path: Path) -> None:
    repo = init_repo(tmp_path)
    write(repo / ":(top)" / "bad.md", "inside  \n")
    write(repo / "outside" / "bad.md", "outside  \n")

    result = run_validator(repo, "--paths", ":(top)")

    assert result.returncode == 1
    assert ":(top)/bad.md:1: trailing whitespace" in result.stdout
    assert "outside/bad.md" not in result.stdout


def test_path_outside_repo_is_rejected(tmp_path: Path) -> None:
    repo = init_repo(tmp_path)
    outside = tmp_path / "outside.md"
    write(outside, "clean\n")

    result = run_validator(repo, "--paths", os.fspath(outside))

    assert result.returncode == 2
    assert "path is outside the repository" in result.stderr


def test_base_ref_checks_committed_range(tmp_path: Path) -> None:
    repo = init_repo(tmp_path)
    basis = git(repo, "rev-parse", "HEAD").stdout.strip()
    write(repo / "tracked.md", "committed bad  \n")
    git(repo, "add", "tracked.md")
    git(repo, "commit", "-qm", "bad commit")

    clean_worktree = run_validator(repo)
    range_check = run_validator(repo, "--base-ref", basis)

    assert clean_worktree.returncode == 0
    assert range_check.returncode == 1
    assert f"committed range {basis}...HEAD" in range_check.stdout
    assert "tracked.md:1: trailing whitespace." in range_check.stdout


def test_control_characters_in_path_are_rendered_unambiguously(
    tmp_path: Path,
) -> None:
    repo = init_repo(tmp_path)
    write(repo / "line\nbreak.md", "bad  \n")

    result = run_validator(repo)

    assert result.returncode == 1
    assert "line\\nbreak.md:1: trailing whitespace" in result.stdout
    assert "line\nbreak.md:1" not in result.stdout
