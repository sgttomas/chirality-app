#!/usr/bin/env python3
"""Validate deliverable-local semantic pipeline write scope against git status."""

from __future__ import annotations

import argparse
import importlib.util
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

SOW_COMMON_PATH = Path(__file__).resolve().parents[1] / "scope_of_work" / "common.py"
_spec = importlib.util.spec_from_file_location("chirality_scope_of_work_common", SOW_COMMON_PATH)
if _spec is None or _spec.loader is None:
    raise ImportError(f"cannot load Scope-of-Work common module: {SOW_COMMON_PATH}")
_common = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = _common
_spec.loader.exec_module(_common)
PRODUCTION_FORMATS = _common.PRODUCTION_FORMATS
SowError = _common.SowError
require_requested_format = _common.require_requested_format
resolve_production_format = _common.resolve_production_format


STEP_ALLOWED = {
    "init": {"ScopeOfWork.md", "_STATUS.md"},
    "semantic": {"_SEMANTIC.md", "_STATUS.md"},
    "lens": {"_SEMANTIC_LENSING.md"},
}
LEGACY_P3_ALLOWED = {"Datasheet.md", "Specification.md", "Guidance.md", "Procedure.md", "_STATUS.md"}
SOW_P3_ALLOWED = {"ScopeOfWork.md"}
STEP_CHOICES = (*STEP_ALLOWED, "p3", "sow-p3")
ALWAYS_ALLOWED_PREFIXES = ("_run_records/",)


@dataclass(frozen=True)
class Finding:
    category: str
    message: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate semantic pipeline write scope for one deliverable.")
    parser.add_argument("deliverable_path", help="Path to a deliverable folder")
    parser.add_argument("--step", choices=sorted(STEP_CHOICES), required=True, help="Pipeline step to validate")
    parser.add_argument("--production-format", choices=["AUTO", *PRODUCTION_FORMATS], default="AUTO")
    parser.add_argument("--isolated-migration", action="store_true")
    parser.add_argument("--migration-authority", default="")
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


def init_blocked_by_existing_contract(production_state: str) -> bool:
    """`INIT` requires no production contract.

    Only an already-present production contract disqualifies an `INIT` run. A
    genuine pre-INIT deliverable resolves to `INVALID` ("missing production
    contract"), which is the expected starting state and must not be blocked.
    """
    return production_state in {"SOW_V1", "MIGRATION_DUAL"}


def validate_changed_paths(
    changed_paths: list[str],
    deliverable_rel: str,
    step: str,
    *,
    allow_memory: bool = False,
    strict_repo: bool = False,
    production_format: str = "LEGACY_FOUR_DOC",
) -> list[Finding]:
    if step in STEP_ALLOWED:
        allowed = set(STEP_ALLOWED[step])
    elif step == "sow-p3" or production_format in {"SOW_V1", "MIGRATION_DUAL"}:
        allowed = set(SOW_P3_ALLOWED)
    else:
        allowed = set(LEGACY_P3_ALLOWED)
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

    production_format = args.production_format
    if args.step in {"p3", "sow-p3"}:
        resolution = resolve_production_format(
            deliverable_path,
            isolated_migration=args.isolated_migration,
            migration_authority=args.migration_authority,
        )
        try:
            require_requested_format(resolution, args.production_format)
        except SowError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 2
        if not resolution.valid:
            print(f"ERROR: format state is {resolution.state}: {'; '.join(resolution.issues)}", file=sys.stderr)
            return 2
        production_format = resolution.state
        if args.step == "sow-p3" and production_format not in {"SOW_V1", "MIGRATION_DUAL"}:
            print("ERROR: sow-p3 requires SOW_V1 or MIGRATION_DUAL", file=sys.stderr)
            return 2
    elif args.step == "init":
        # `INIT` requires no production contract (skills/scope-of-work/SKILL.md).
        # Resolution is advisory for this step and its validity is deliberately
        # NOT gated on: a genuine pre-INIT deliverable resolves INVALID with
        # "missing production contract", which is the expected starting state.
        # Only an already-present production contract disqualifies an INIT run.
        resolution = resolve_production_format(
            deliverable_path,
            isolated_migration=args.isolated_migration,
            migration_authority=args.migration_authority,
        )
        if init_blocked_by_existing_contract(resolution.state):
            print("ERROR: init requires no existing production contract", file=sys.stderr)
            return 2

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
        production_format=production_format,
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
