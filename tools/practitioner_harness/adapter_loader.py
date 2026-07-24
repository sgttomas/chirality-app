#!/usr/bin/env python3
"""Adapter-manifest loader — `<project-root>/_harness/adapter.yaml`.

The manifest is harness configuration authority only (governed, committed,
human-reviewed); it is never lifecycle or project truth (plan v3 §Authority
Classes). Unknown schema or missing required keys are operational errors
(exit 2), never guesses.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover - exercised only in missing dependency environments.
    yaml = None  # type: ignore[assignment]

from harness_common import HarnessOperationalError

ADAPTER_SCHEMA = "practitioner-harness-adapter/v1"
ADAPTER_RELPATH = Path("_harness") / "adapter.yaml"

REQUIRED_KEYS = (
    "schema",
    "project",
    "plan",
    "coordination",
    "decision_register",
    "dag_pointer",
    "status_glob",
    "states",
    "parser_dialect",
    "drift_baseline_mismatch",
    "drift_baseline_files",
)


@dataclass
class AdapterManifest:
    schema: str
    project: str
    plan: str
    coordination: str
    decision_register: str
    dag_pointer: str
    status_glob: str
    states: list[str]
    parser_dialect: str
    drift_baseline_mismatch: int
    drift_baseline_files: int
    coordination_pointer: str = ""
    exclude_globs: list[str] = field(default_factory=list)
    dependency_register_structured: str = ""
    dependency_register_summary: str = ""
    validation_commands: list[dict] = field(default_factory=list)
    guard_requires_committed_ruling_path: bool = True
    guard_requires_approval_sha: bool = False
    guard_approval_sha_field: str = ""
    project_root: Path | None = None
    manifest_path: Path | None = None


def load_adapter(project_root: Path) -> AdapterManifest:
    if yaml is None:
        raise HarnessOperationalError(
            "PyYAML is required to read adapter manifests but is not importable "
            "in this interpreter (operational error, exit 2)."
        )
    manifest_path = project_root / ADAPTER_RELPATH
    if not manifest_path.is_file():
        raise HarnessOperationalError(
            f"Adapter manifest missing: {manifest_path} (operational error, exit 2)."
        )
    try:
        data = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - any parse failure is operational.
        raise HarnessOperationalError(
            f"Unparseable adapter manifest {manifest_path}: {exc}"
        ) from exc
    if not isinstance(data, dict):
        raise HarnessOperationalError(
            f"Unparseable adapter manifest {manifest_path}: top level is not a mapping."
        )
    missing = [k for k in REQUIRED_KEYS if k not in data]
    if missing:
        raise HarnessOperationalError(
            f"Adapter manifest {manifest_path} missing required keys: {missing}"
        )
    if data["schema"] != ADAPTER_SCHEMA:
        raise HarnessOperationalError(
            f"Adapter manifest {manifest_path} declares unknown schema "
            f"{data['schema']!r}; this harness understands {ADAPTER_SCHEMA!r}."
        )
    manifest = AdapterManifest(
        schema=str(data["schema"]),
        project=str(data["project"]),
        plan=str(data["plan"]),
        coordination=str(data["coordination"]),
        decision_register=str(data["decision_register"]),
        dag_pointer=str(data["dag_pointer"]),
        status_glob=str(data["status_glob"]),
        states=[str(s) for s in data["states"]],
        parser_dialect=str(data["parser_dialect"]),
        drift_baseline_mismatch=int(data["drift_baseline_mismatch"]),
        drift_baseline_files=int(data["drift_baseline_files"]),
        coordination_pointer=str(data.get("coordination_pointer", "") or ""),
        exclude_globs=[str(g) for g in (data.get("exclude_globs") or [])],
        dependency_register_structured=str(data.get("dependency_register_structured", "") or ""),
        dependency_register_summary=str(data.get("dependency_register_summary", "") or ""),
        validation_commands=list(data.get("validation_commands") or []),
        guard_requires_committed_ruling_path=bool(
            data.get("guard_requires_committed_ruling_path", True)),
        guard_requires_approval_sha=bool(data.get("guard_requires_approval_sha", False)),
        guard_approval_sha_field=str(data.get("guard_approval_sha_field", "") or ""),
        project_root=project_root,
        manifest_path=manifest_path,
    )
    return manifest
