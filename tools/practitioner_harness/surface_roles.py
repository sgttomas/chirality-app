#!/usr/bin/env python3
"""Shared active-surface portability classification and exception policy.

The policy deliberately distinguishes active managed controls from immutable
runtime evidence.  It does not infer evidence from arbitrary filenames and it
does not turn historical project-tree telemetry into an ever-growing baseline.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from enum import Enum
from pathlib import Path, PurePosixPath
from typing import Iterable


MACHINE_ABS_PATH_RE = re.compile(
    r"(?<![A-Za-z0-9_.{-])"
    r"(?:/(?:Users|private|home|tmp|var/folders)/[^\s)\"'`<>]+"
    r"|[A-Za-z]:\\Users\\[A-Za-z0-9._-]+[^\s`'\"<>)\]]*)"
)

POLICY_RELPATH = PurePosixPath("validation/portability_policy.json")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


class SurfaceRole(str, Enum):
    CONTROL = "CONTROL"
    EVIDENCE = "EVIDENCE"
    UNCLASSIFIED = "UNCLASSIFIED"


@dataclass(frozen=True)
class SurfaceClassification:
    role: SurfaceRole
    reason: str
    active: bool


@dataclass(frozen=True)
class PolicyEntry:
    path: str
    sha256: str
    entry_type: str
    role: SurfaceRole
    reason: str
    authority: str


@dataclass(frozen=True)
class PolicyIssue:
    code: str
    message: str
    source_path: str


@dataclass(frozen=True)
class LoadedPolicy:
    project_root: str
    overrides: dict[str, PolicyEntry]
    exceptions: dict[str, PolicyEntry]
    issues: tuple[PolicyIssue, ...]
    policy_path: str
    enabled: bool

    @property
    def entries(self) -> tuple[PolicyEntry, ...]:
        return tuple(self.overrides.values()) + tuple(self.exceptions.values())


CONTROL_NAMES = {
    "ORCHESTRATION_PLAN.md",
    "LAUNCH_BRIEF.md",
    "CHILD_BRIEF.md",
    "INIT-TASK.md",
    "WORK_GRAPH.json",
    "NEXT_INSTANCE_PROMPT.md",
    "_COORDINATION.md",
}
EVIDENCE_NAMES = {
    "RETURN.md",
    "HANDOFF_STATE.md",
    "STATUS.json",
    "RUN_RECORD.md",
    "INTERRUPTION_RECORD.md",
    "TOOL_ERROR_RECORD.md",
}
CONTROL_TOKEN_RE = re.compile(
    r"(?:^|_)(?:PLAN|BRIEF|AMENDMENT|NOTICE|DIRECTION|UPDATE)(?:_|\.|$)")
VERSIONED_EVIDENCE_NAME_RE = re.compile(
    r"^(?:RETURN_V[1-9][0-9]*\.md|STATUS_V[1-9][0-9]*\.json)$")
EVIDENCE_DIRS = {"_run_records"}


def normalize_repo_relative_path(value: str) -> str:
    """Return a canonical POSIX repo-relative path or raise ValueError."""
    if not isinstance(value, str) or not value or "\\" in value:
        raise ValueError("path must be a non-empty POSIX string")
    path = PurePosixPath(value)
    if path.is_absolute() or value != path.as_posix():
        raise ValueError("path must be normalized and repo-relative")
    if any(part in {"", ".", ".."} for part in path.parts):
        raise ValueError("path contains a forbidden segment")
    return path.as_posix()


def _agentruns_tail(relpath: str) -> tuple[str, ...] | None:
    parts = PurePosixPath(relpath).parts
    for idx in range(len(parts) - 3):
        if parts[idx:idx + 3] == ("execution", "_Coordination", "AgentRuns"):
            return parts[idx + 3:]
    return None


def classify_surface(relpath: str, *, live_entry: bool = False) -> SurfaceClassification:
    """Classify a repository surface without consulting migration policy.

    Control precedence is intentional.  Within AgentRuns, only enumerated
    structural records are evidence; an unknown artifact remains fail-closed.
    Outside AgentRuns, callers opt in validator-defined live entry surfaces.
    """
    relpath = normalize_repo_relative_path(relpath)
    path = PurePosixPath(relpath)
    tail = _agentruns_tail(relpath)
    if tail is not None:
        name = path.name
        if path.suffix not in {".md", ".json", ".yaml", ".yml", ".txt"}:
            return SurfaceClassification(
                SurfaceRole.UNCLASSIFIED,
                f"unsupported managed artifact suffix `{path.suffix}`", True)
        if name in CONTROL_NAMES or CONTROL_TOKEN_RE.search(name):
            return SurfaceClassification(
                SurfaceRole.CONTROL, f"managed control record `{name}`", True)
        if name in EVIDENCE_NAMES or VERSIONED_EVIDENCE_NAME_RE.fullmatch(name):
            return SurfaceClassification(
                SurfaceRole.EVIDENCE, f"managed evidence record `{name}`", True)
        if any(part in EVIDENCE_DIRS for part in tail[:-1]):
            return SurfaceClassification(
                SurfaceRole.EVIDENCE, "managed evidence directory", True)
        return SurfaceClassification(
            SurfaceRole.UNCLASSIFIED, "unknown managed AgentRuns artifact", True)

    if "_run_records" in path.parts:
        return SurfaceClassification(
            SurfaceRole.EVIDENCE, "structural run-record directory", True)

    parts = path.parts
    project_live_entry = (
        len(parts) >= 5
        and parts[0] in {"projects", "domains"}
        and parts[2:4] == ("execution", "_Coordination")
        and path.name in {"NEXT_INSTANCE_PROMPT.md", "_COORDINATION.md"}
    ) or (
        len(parts) >= 4
        and parts[0] in {"projects", "domains"}
        and parts[2] == "init"
        and path.suffix == ".md"
    )
    if project_live_entry:
        return SurfaceClassification(
            SurfaceRole.CONTROL, "structural live project entry surface", True)
    if live_entry:
        return SurfaceClassification(
            SurfaceRole.CONTROL, "validator-defined live entry surface", True)
    return SurfaceClassification(
        SurfaceRole.UNCLASSIFIED, "historical/non-active project surface", False)


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _issue(code: str, message: str, policy_path: str) -> PolicyIssue:
    return PolicyIssue(code, message, policy_path)


def _parse_entries(
    raw_entries: object,
    expected_type: str,
    expected_role: SurfaceRole,
    repo_root: Path,
    project_root: str,
    policy_path: str,
    seen: set[str],
) -> tuple[dict[str, PolicyEntry], list[PolicyIssue]]:
    entries: dict[str, PolicyEntry] = {}
    issues: list[PolicyIssue] = []
    if not isinstance(raw_entries, list):
        return entries, [_issue(
            "PORTABILITY_POLICY_SCHEMA",
            f"`{expected_type}` section must be a list.", policy_path)]
    for index, raw in enumerate(raw_entries):
        label = f"{expected_type}[{index}]"
        if not isinstance(raw, dict):
            issues.append(_issue(
                "PORTABILITY_POLICY_SCHEMA", f"{label} must be an object.", policy_path))
            continue
        required = {"path", "sha256", "entry_type", "role", "reason", "authority"}
        missing = sorted(required - raw.keys())
        extra = sorted(raw.keys() - required)
        if missing or extra:
            issues.append(_issue(
                "PORTABILITY_POLICY_SCHEMA",
                f"{label} has missing={missing} extra={extra}.", policy_path))
            continue
        try:
            relpath = normalize_repo_relative_path(raw["path"])
        except (TypeError, ValueError) as exc:
            issues.append(_issue(
                "PORTABILITY_POLICY_PATH", f"{label} path is invalid: {exc}.", policy_path))
            continue
        if relpath in seen:
            issues.append(_issue(
                "PORTABILITY_POLICY_DUPLICATE", f"duplicate path `{relpath}`.", policy_path))
            continue
        seen.add(relpath)
        if not (relpath == project_root or relpath.startswith(project_root + "/")):
            issues.append(_issue(
                "PORTABILITY_POLICY_PATH",
                f"`{relpath}` is outside declared project root `{project_root}`.", policy_path))
            continue
        if raw["entry_type"] != expected_type or raw["role"] != expected_role.value:
            issues.append(_issue(
                "PORTABILITY_POLICY_SCHEMA",
                f"{label} must declare entry_type={expected_type!r} and "
                f"role={expected_role.value!r}.", policy_path))
            continue
        if not isinstance(raw["sha256"], str) or not SHA256_RE.fullmatch(raw["sha256"]):
            issues.append(_issue(
                "PORTABILITY_POLICY_HASH", f"{label} has an invalid SHA-256.", policy_path))
            continue
        if not isinstance(raw["reason"], str) or not raw["reason"].strip():
            issues.append(_issue(
                "PORTABILITY_POLICY_SCHEMA", f"{label} reason is empty.", policy_path))
            continue
        if not isinstance(raw["authority"], str) or not raw["authority"].strip():
            issues.append(_issue(
                "PORTABILITY_POLICY_SCHEMA", f"{label} authority is empty.", policy_path))
            continue
        entry = PolicyEntry(
            relpath, raw["sha256"], raw["entry_type"], expected_role,
            raw["reason"].strip(), raw["authority"].strip())
        target = repo_root / relpath
        if not target.is_file() or target.is_symlink():
            issues.append(_issue(
                "PORTABILITY_POLICY_TARGET_MISSING",
                f"policy target `{relpath}` is absent or not a regular file.", policy_path))
            continue
        actual_hash = file_sha256(target)
        if actual_hash != entry.sha256:
            issues.append(_issue(
                "PORTABILITY_POLICY_HASH_DRIFT",
                f"policy target `{relpath}` hash drifted: expected "
                f"{entry.sha256}, observed {actual_hash}.", policy_path))
            continue
        try:
            text = target.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            text = ""
        if not MACHINE_ABS_PATH_RE.search(text):
            issues.append(_issue(
                "PORTABILITY_POLICY_STALE",
                f"policy target `{relpath}` no longer contains a machine-absolute path.",
                policy_path))
            continue
        base = classify_surface(relpath)
        if expected_type == "historical_role_override":
            if base.role is not SurfaceRole.UNCLASSIFIED or not base.active:
                issues.append(_issue(
                    "PORTABILITY_POLICY_ROLE_MISMATCH",
                    f"role override `{relpath}` must target an active, structurally "
                    f"UNCLASSIFIED artifact; observed {base.role.value}/{base.active}.",
                    policy_path))
                continue
        elif base.role is SurfaceRole.EVIDENCE:
            issues.append(_issue(
                "PORTABILITY_POLICY_ROLE_MISMATCH",
                f"control exception `{relpath}` cannot reclassify structural "
                "EVIDENCE as CONTROL.", policy_path))
            continue
        entries[relpath] = entry
    return entries, issues


def load_project_policy(repo_root: Path, project_root: Path) -> LoadedPolicy:
    repo_root = repo_root.resolve()
    project_root = project_root.resolve()
    project_rel = project_root.relative_to(repo_root).as_posix()
    policy_file = project_root / POLICY_RELPATH
    policy_rel = policy_file.relative_to(repo_root).as_posix()
    if not policy_file.is_file():
        return LoadedPolicy(project_rel, {}, {}, (), policy_rel, False)
    try:
        raw = json.loads(policy_file.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        return LoadedPolicy(project_rel, {}, {}, (
            _issue("PORTABILITY_POLICY_SCHEMA", f"cannot parse policy: {exc}.", policy_rel),),
            policy_rel, True)
    if not isinstance(raw, dict):
        return LoadedPolicy(project_rel, {}, {}, (
            _issue("PORTABILITY_POLICY_SCHEMA", "policy root must be an object.", policy_rel),),
            policy_rel, True)
    expected_keys = {
        "schema_version", "project_root", "historical_role_overrides",
        "control_path_exceptions",
    }
    issues: list[PolicyIssue] = []
    if set(raw) != expected_keys or raw.get("schema_version") != 1:
        issues.append(_issue(
            "PORTABILITY_POLICY_SCHEMA",
            f"policy requires exactly keys {sorted(expected_keys)} and schema_version=1.",
            policy_rel))
    if raw.get("project_root") != project_rel:
        issues.append(_issue(
            "PORTABILITY_POLICY_PATH",
            f"project_root must be `{project_rel}`.", policy_rel))
    seen: set[str] = set()
    overrides, override_issues = _parse_entries(
        raw.get("historical_role_overrides"), "historical_role_override",
        SurfaceRole.EVIDENCE, repo_root, project_rel, policy_rel, seen)
    exceptions, exception_issues = _parse_entries(
        raw.get("control_path_exceptions"), "control_path_exception",
        SurfaceRole.CONTROL, repo_root, project_rel, policy_rel, seen)
    issues.extend(override_issues)
    issues.extend(exception_issues)
    return LoadedPolicy(
        project_rel, overrides, exceptions, tuple(issues), policy_rel, True)


def effective_role(relpath: str, policy: LoadedPolicy) -> SurfaceClassification:
    base = classify_surface(relpath)
    if relpath in policy.overrides:
        return SurfaceClassification(
            SurfaceRole.EVIDENCE, "hash-bound historical role override", True)
    if relpath in policy.exceptions:
        return SurfaceClassification(
            SurfaceRole.CONTROL, "hash-bound historical control exception", True)
    return base


def has_control_exception(relpath: str, policy: LoadedPolicy) -> bool:
    return relpath in policy.exceptions


def iter_machine_path_lines(text: str) -> Iterable[int]:
    for line_no, line in enumerate(text.splitlines(), start=1):
        if MACHINE_ABS_PATH_RE.search(line):
            yield line_no
