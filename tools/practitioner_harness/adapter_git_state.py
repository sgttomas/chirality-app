#!/usr/bin/env python3
"""Read-only git-state adapter.

Emits SourcedFacts for branch, HEAD SHA, and a dirty summary scoped to a root.
Outside a git repository these become NOT_APPLICABLE facts — never a crash
(export/staging contexts are lawful).
"""

from __future__ import annotations

import subprocess
from pathlib import Path

from harness_common import SourcedFact


def _git(repo_root: Path, *args: str) -> tuple[int, str]:
    try:
        proc = subprocess.run(
            ["git", *args], cwd=repo_root, capture_output=True, text=True, check=False,
        )
    except OSError:
        return 127, ""
    return proc.returncode, proc.stdout


def is_git_repo(repo_root: Path) -> bool:
    code, out = _git(repo_root, "rev-parse", "--is-inside-work-tree")
    return code == 0 and out.strip() == "true"


def sha_reachable(repo_root: Path, sha: str) -> bool | None:
    """True/False for reachable/unreachable; None when git state is unavailable."""
    if not is_git_repo(repo_root):
        return None
    code, _ = _git(repo_root, "cat-file", "-e", f"{sha}^{{commit}}")
    return code == 0


def git_state_facts(repo_root: Path, scope: Path | None = None) -> list[SourcedFact]:
    facts: list[SourcedFact] = []
    src = ".git"
    if not is_git_repo(repo_root):
        facts.append(SourcedFact(
            fact_id="git.state", value="not a git repository",
            source_path=str(repo_root), authority_status="observed",
            parse_status="NOT_APPLICABLE",
            caveat="git-dependent facts unavailable here (export/staging context).",
        ))
        return facts
    code, out = _git(repo_root, "rev-parse", "--abbrev-ref", "HEAD")
    if code == 0:
        facts.append(SourcedFact(
            fact_id="git.branch", value=out.strip(), source_path=src,
            authority_status="observed", parse_status="PARSED"))
    code, out = _git(repo_root, "rev-parse", "HEAD")
    if code == 0:
        facts.append(SourcedFact(
            fact_id="git.head_sha", value=out.strip(), source_path=src,
            authority_status="observed", parse_status="PARSED"))
    scope_args = ["status", "--porcelain"]
    scope_label = "repo"
    if scope is not None:
        scope_args += ["--", str(scope)]
        try:
            scope_label = str(Path(scope).resolve().relative_to(repo_root.resolve()))
        except ValueError:
            scope_label = str(scope)
    code, out = _git(repo_root, *scope_args)
    if code == 0:
        lines = [ln for ln in out.splitlines() if ln.strip()]
        facts.append(SourcedFact(
            fact_id="git.dirty_paths",
            value=f"{len(lines)} dirty path(s) under {scope_label}",
            source_path=src, authority_status="observed", parse_status="PARSED"))
    return facts
