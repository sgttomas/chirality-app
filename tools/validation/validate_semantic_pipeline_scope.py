#!/usr/bin/env python3
"""Validate deliverable-local semantic pipeline write scope against git status."""

from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


STEP_ALLOWED = {
    "semantic": {"_SEMANTIC.md", "_STATUS.md"},
    "lens": {"_SEMANTIC_LENSING.md"},
    "p3": {"Datasheet.md", "Specification.md", "Guidance.md", "Procedure.md", "_STATUS.md"},
}
ALWAYS_ALLOWED_PREFIXES = ("_run_records/",)


@dataclass(frozen=True)
class Finding:
    category: str
    message: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate semantic pipeline write scope for one deliverable.")
    parser.add_argument("deliverable_path", help="Path to a deliverable folder")
    parser.add_argument("--step", choices=sorted(STEP_ALLOWED), required=True, help="Pipeline step to validate")
    parser.add_argument("--allow-memory", action="store_true", help="Allow MEMORY.md as closeout evidence")
    parser.add_argument(
        "--strict-repo",
        action="store_true",
        help="Also fail when there are dirty files outside the deliverable folder",
    )
    return parser.parse_args()


def normalize_status_path(raw_path: str) -> str:
    path = raw_path.strip()
    if " -> " in path:
        path = path.split(" -> ", 1)[1]
    return path.strip('"')


def git_status_paths(repo_root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=all"],
        cwd=repo_root,
        check=False,
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "git status failed")
    paths: list[str] = []
    for line in result.stdout.splitlines():
        if not line:
            continue
        paths.append(normalize_status_path(line[3:]))
    return paths


def validate_changed_paths(
    changed_paths: list[str],
    deliverable_rel: str,
    step: str,
    *,
    allow_memory: bool = False,
    strict_repo: bool = False,
) -> list[Finding]:
    allowed = set(STEP_ALLOWED[step])
    if allow_memory:
        allowed.add("MEMORY.md")
    findings: list[Finding] = []
    prefix = deliverable_rel.rstrip("/") + "/"

    for path in changed_paths:
        if not path.startswith(prefix):
            if strict_repo:
                findings.append(Finding("DIRTY_OUTSIDE_DELIVERABLE", f"{path} is outside {deliverable_rel}"))
            continue
        local = path[len(prefix) :]
        if local in allowed or local.startswith(ALWAYS_ALLOWED_PREFIXES):
            continue
        findings.append(Finding("OUT_OF_SCOPE_PATH", f"{local} is not allowed for step {step}"))

    return findings


def main() -> int:
    args = parse_args()
    repo_root = Path.cwd()
    deliverable_path = Path(args.deliverable_path)
    if not deliverable_path.is_absolute():
        deliverable_path = (repo_root / deliverable_path).resolve()
    try:
        deliverable_rel = deliverable_path.relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        print(f"ERROR: deliverable path is outside repo root: {deliverable_path}", file=sys.stderr)
        return 1

    try:
        changed_paths = git_status_paths(repo_root)
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    findings = validate_changed_paths(
        changed_paths,
        deliverable_rel,
        args.step,
        allow_memory=args.allow_memory,
        strict_repo=args.strict_repo,
    )
    if findings:
        print(f"INVALID: {deliverable_rel} ({args.step})")
        for finding in findings:
            print(f"  [{finding.category}] {finding.message}")
        return 1

    print(f"VALID: {deliverable_rel} ({args.step})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
