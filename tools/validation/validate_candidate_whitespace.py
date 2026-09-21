#!/usr/bin/env python3
"""Validate whitespace in the current Git candidate set.

Tracked changes are delegated to ``git diff --check`` so Git's established
whitespace semantics remain authoritative. Git does not include untracked
files in a diff, so this tool closes that seam by scanning non-ignored,
text-like untracked files before they are staged.

Only the recurring defects evidenced by governed closeout are checked beyond
Git's own behavior: trailing spaces/tabs and surplus terminal blank lines.
The tool is read-only.

Advisory under D-GOV-43 item 11: findings inform the author and never gate a
merge; no CI workflow invokes this tool as a required check.

Exit codes:
    0: no findings
    1: whitespace findings
    2: operational error
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


EXIT_CLEAN = 0
EXIT_FINDINGS = 1
EXIT_OPERATIONAL = 2

# These extensions are binary even when a short sample happens not to contain
# NUL. Git attributes remain the first authority; this list is a conservative
# safety fallback for untracked files without attributes.
BINARY_SUFFIXES = {
    ".7z", ".a", ".avi", ".bmp", ".class", ".db", ".dll", ".dylib",
    ".eot", ".exe", ".gif", ".gz", ".ico", ".jar", ".jpeg", ".jpg",
    ".lockb", ".m4a", ".mov", ".mp3", ".mp4", ".o", ".otf", ".parquet",
    ".pdf", ".png", ".pyc", ".so", ".sqlite", ".sqlite3", ".tar", ".tif",
    ".tiff", ".ttf", ".wasm", ".webm", ".webp", ".woff", ".woff2", ".xls",
    ".xlsb", ".xlsm", ".xlsx", ".zip",
}


@dataclass(frozen=True)
class Finding:
    path: str
    line: int
    message: str

    def render(self) -> str:
        rendered_path = (
            self.path
            .replace("\\", "\\\\")
            .replace("\n", "\\n")
            .replace("\r", "\\r")
            .replace("\t", "\\t")
        )
        return f"{rendered_path}:{self.line}: {self.message}"


class OperationalError(RuntimeError):
    """The validator could not establish or inspect its Git scope."""


def _run_git(
    repo_root: Path,
    args: Sequence[str],
    *,
    check: bool = True,
) -> subprocess.CompletedProcess[bytes]:
    result = subprocess.run(
        ["git", *args],
        cwd=repo_root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if check and result.returncode != 0:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        raise OperationalError(
            f"git {' '.join(args)} failed with exit {result.returncode}"
            + (f": {detail}" if detail else "")
        )
    return result


def resolve_repo_root(start: Path) -> Path:
    result = subprocess.run(
        ["git", "-C", str(start), "rev-parse", "--show-toplevel"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        raise OperationalError(
            "not inside a Git worktree" + (f": {detail}" if detail else "")
        )
    return Path(os.fsdecode(result.stdout).strip()).resolve()


def normalize_paths(repo_root: Path, raw_paths: Sequence[str]) -> list[str]:
    """Return repo-relative literal pathspecs, rejecting escape attempts."""
    normalized: list[str] = []
    for raw in raw_paths:
        candidate = Path(raw)
        if candidate.is_absolute():
            try:
                candidate = candidate.resolve().relative_to(repo_root)
            except ValueError as exc:
                raise OperationalError(
                    f"path is outside the repository: {raw}"
                ) from exc
        if ".." in candidate.parts:
            raise OperationalError(f"path traversal is not allowed: {raw}")
        value = candidate.as_posix()
        normalized.append(value if value not in ("", ".") else ".")
    return normalized or ["."]


def literal_pathspecs(paths: Sequence[str]) -> list[str]:
    """Protect caller-supplied paths from Git pathspec magic expansion."""
    return [f":(literal){path}" for path in paths]


def _diff_check(
    repo_root: Path,
    args: Sequence[str],
    paths: Sequence[str],
) -> tuple[bool, str]:
    """Run Git's check verbatim; any nonzero with output is a finding."""
    result = _run_git(
        repo_root,
        [*args, "--", *literal_pathspecs(paths)],
        check=False,
    )
    stdout = result.stdout.decode("utf-8", errors="replace")
    stderr = result.stderr.decode("utf-8", errors="replace")
    if result.returncode == 0:
        return False, stdout
    if not stdout and stderr:
        raise OperationalError(
            f"git {' '.join(args)} failed with exit {result.returncode}: "
            f"{stderr.strip()}"
        )
    return True, stdout + stderr


def check_tracked_changes(
    repo_root: Path,
    paths: Sequence[str],
    base_ref: str | None,
) -> tuple[bool, list[tuple[str, str]]]:
    """Preserve git-diff whitespace behavior for every tracked candidate."""
    outputs: list[tuple[str, str]] = []
    failed = False
    checks: list[tuple[str, list[str]]] = []
    if base_ref:
        verify = _run_git(
            repo_root,
            ["rev-parse", "--verify", "--quiet", f"{base_ref}^{{commit}}"],
            check=False,
        )
        if verify.returncode != 0:
            raise OperationalError(f"base ref is not a commit: {base_ref}")
        checks.append(
            (
                f"committed range {base_ref}...HEAD",
                ["diff", "--check", f"{base_ref}...HEAD"],
            )
        )
    checks.extend(
        [
            ("staged changes", ["diff", "--cached", "--check"]),
            ("unstaged changes", ["diff", "--check"]),
        ]
    )
    for label, args in checks:
        has_findings, output = _diff_check(repo_root, args, paths)
        failed = failed or has_findings
        if output:
            outputs.append((label, output))
    return failed, outputs


def list_untracked(repo_root: Path, paths: Sequence[str]) -> list[str]:
    result = _run_git(
        repo_root,
        [
            "ls-files",
            "--others",
            "--exclude-standard",
            "-z",
            "--",
            *literal_pathspecs(paths),
        ],
    )
    return sorted(os.fsdecode(item) for item in result.stdout.split(b"\0") if item)


def _git_attributes(repo_root: Path, relpath: str) -> dict[str, str]:
    result = _run_git(
        repo_root,
        ["check-attr", "-z", "diff", "text", "binary", "--", relpath],
    )
    fields = result.stdout.split(b"\0")
    if fields and fields[-1] == b"":
        fields.pop()
    if len(fields) % 3:
        raise OperationalError(f"unexpected git check-attr output for {relpath}")
    attributes: dict[str, str] = {}
    for idx in range(0, len(fields), 3):
        attributes[os.fsdecode(fields[idx + 1])] = os.fsdecode(fields[idx + 2])
    return attributes


def _is_binary_candidate(repo_root: Path, relpath: str, path: Path) -> bool:
    attributes = _git_attributes(repo_root, relpath)
    if (
        attributes.get("diff") == "unset"
        or attributes.get("text") == "unset"
        or attributes.get("binary") == "set"
    ):
        return True
    if attributes.get("diff") == "set" or attributes.get("text") == "set":
        return False
    if path.suffix.lower() in BINARY_SUFFIXES:
        return True
    with path.open("rb") as handle:
        return b"\0" in handle.read(8192)


def scan_untracked_text(path: Path, relpath: str) -> list[Finding]:
    """Check one untracked text file without modifying it."""
    findings: list[Finding] = []
    terminal_blank_lines: list[int] = []

    with path.open("rb") as handle:
        for line_number, raw_line in enumerate(handle, start=1):
            content = raw_line[:-1] if raw_line.endswith(b"\n") else raw_line
            if content.endswith(b"\r"):
                content = content[:-1]

            if content.endswith((b" ", b"\t")):
                findings.append(Finding(relpath, line_number, "trailing whitespace"))

            if content == b"":
                terminal_blank_lines.append(line_number)
            else:
                terminal_blank_lines.clear()

    for line_number in terminal_blank_lines:
        findings.append(Finding(relpath, line_number, "blank line at end of file"))

    return findings


def check_untracked(
    repo_root: Path,
    paths: Sequence[str],
) -> tuple[list[Finding], list[str]]:
    findings: list[Finding] = []
    skipped: list[str] = []
    for relpath in list_untracked(repo_root, paths):
        path = repo_root / relpath
        try:
            path.lstat()
        except FileNotFoundError:
            raise OperationalError(f"untracked path disappeared during scan: {relpath}")
        if not path.is_file() or path.is_symlink():
            skipped.append(relpath)
            continue
        if _is_binary_candidate(repo_root, relpath, path):
            skipped.append(relpath)
            continue
        try:
            findings.extend(scan_untracked_text(path, relpath))
        except OSError as exc:
            raise OperationalError(f"cannot read {relpath}: {exc}") from exc
    return findings, skipped


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Run Git whitespace checks for tracked changes and scan non-ignored "
            "untracked text candidates."
        )
    )
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Path inside the target Git worktree (default: current directory).",
    )
    parser.add_argument(
        "--base-ref",
        help="Also check committed changes from the merge base with this ref to HEAD.",
    )
    parser.add_argument(
        "--paths",
        nargs="+",
        default=["."],
        metavar="PATH",
        help="Repo-contained paths to check (default: the whole worktree).",
    )
    parser.add_argument(
        "--no-untracked",
        action="store_true",
        help="Do not scan untracked candidates.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        repo_root = resolve_repo_root(Path(args.repo_root))
        paths = normalize_paths(repo_root, args.paths)
        tracked_failed, tracked_outputs = check_tracked_changes(
            repo_root, paths, args.base_ref
        )
        untracked_findings: list[Finding] = []
        skipped: list[str] = []
        if not args.no_untracked:
            untracked_findings, skipped = check_untracked(repo_root, paths)
    except OperationalError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return EXIT_OPERATIONAL

    for label, output in tracked_outputs:
        print(f"Tracked whitespace findings ({label}):")
        print(output, end="" if output.endswith("\n") else "\n")
    if untracked_findings:
        print("Untracked text whitespace findings:")
        for finding in untracked_findings:
            print(finding.render())

    if tracked_failed or untracked_findings:
        print(
            "FAIL: candidate whitespace findings "
            f"(untracked binary/symlink paths safely skipped: {len(skipped)})."
        )
        return EXIT_FINDINGS

    print(
        "PASS: candidate whitespace is clean "
        f"(untracked binary/symlink paths safely skipped: {len(skipped)})."
    )
    return EXIT_CLEAN


if __name__ == "__main__":
    raise SystemExit(main())
