#!/usr/bin/env python3
"""Adapter-manifest loader — two registered locations, two registered schemas.

| Working root | Manifest location | Schema |
|---|---|---|
| project (`projects/<name>`) | `<project-root>/_harness/adapter.yaml` | `practitioner-harness-adapter/v1` |
| root product (`WORKING_ROOT == REPO_ROOT`, SPEC §0.2.2) | `<repo-root>/execution/_harness/adapter.yaml` | `root-harness-adapter/v1` |

The manifest is harness configuration authority only (governed, committed,
human-reviewed); it is never lifecycle or project truth (plan v3 §Authority
Classes). Unknown schema or missing required keys are operational errors
(exit 2), never guesses.

Both shapes are validated strictly and independently — there is no fallback
between them. Location and schema must agree: a `root-harness-adapter/v1`
document at the project relpath (or the reverse) is an operational error, not
a shape the loader will try the other validator on. Where both locations carry
a manifest the loader refuses as ambiguous rather than picking one.

The root shape is then NORMALIZED into this module's single internal
`AdapterManifest` so every consuming command keeps one shape to read:

| `root-harness-adapter/v1` | internal `AdapterManifest` | note |
|---|---|---|
| `product` | `project` | the working root's identity string |
| `prd` | `plan` | the PRD fills the role `plan` serves for a project |
| `coordination` | `coordination` | same meaning |
| `decision_register` | `decision_register` | same meaning |
| `status_glob`, `states`, `parser_dialect`, `exclude_globs` | same names | same meaning |
| `baselines.status_files` | `drift_baseline_files` | pinned drift denominator |
| `baselines.status_mismatch` | `drift_baseline_mismatch` | pinned drift numerator |
| `baselines.pinned_at` | `baseline_pinned_at` | pin provenance (root only) |
| `working_root`, `execution_root` | same names | declared explicitly by root only |
| *(not declared)* | `dag_pointer = ""` | root registers no DAG pointer surface |
| *(not declared)* | `validation_commands = []` | root declares no validation surfaces |

`kind` records which shape was loaded, and `declares_dag_pointer()` /
`declares_validation_commands()` let a command detect an absent field and
refuse rather than guess (see `harness.py` for the per-command policy).

Authority note: `tools/validation/validate_root_harness_adapter.py` (G1) is
the root adapter's authority. This loader neither weakens nor replaces it; it
validates what the harness needs in order to read the manifest at all.
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

ROOT_ADAPTER_SCHEMA = "root-harness-adapter/v1"
ROOT_ADAPTER_RELPATH = Path("execution") / "_harness" / "adapter.yaml"

KIND_PROJECT = "project"
KIND_ROOT = "root"

# (kind, relpath, schema) in probe order.
REGISTERED_LOCATIONS = (
    (KIND_PROJECT, ADAPTER_RELPATH, ADAPTER_SCHEMA),
    (KIND_ROOT, ROOT_ADAPTER_RELPATH, ROOT_ADAPTER_SCHEMA),
)

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

# Mirrors the G1 validator's required-key set (that guard remains the root
# adapter's authority); the loader additionally requires the two baseline
# integers it must have to report drift at all.
ROOT_REQUIRED_KEYS = (
    "schema",
    "product",
    "working_root",
    "execution_root",
    "prd",
    "coordination",
    "decision_register",
    "status_glob",
    "states",
    "parser_dialect",
    "baselines",
)

ROOT_REQUIRED_BASELINE_KEYS = ("status_files", "status_mismatch", "pinned_at")


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
    kind: str = KIND_PROJECT
    working_root: str = ""
    execution_root: str = ""
    baseline_pinned_at: str = ""
    mode: str = "legacy"
    governance_state: dict = field(default_factory=dict)

    def historical_root(self) -> bool:
        return self.kind == KIND_ROOT and self.mode == "governance-only"

    def declares_dag_pointer(self) -> bool:
        """False when the loaded schema registers no DAG pointer surface. A
        command that genuinely needs one refuses; it never guesses a path."""
        return bool(self.dag_pointer)

    def declares_validation_commands(self) -> bool:
        return bool(self.validation_commands)

    def manifest_relpath(self, repo_root: Path) -> str:
        """Repo-relative POSIX path of the manifest, for citation in reports."""
        if self.manifest_path is None:
            return ""
        try:
            return self.manifest_path.relative_to(repo_root).as_posix()
        except ValueError:
            return self.manifest_path.as_posix()


def _require_yaml() -> None:
    if yaml is None:
        raise HarnessOperationalError(
            "PyYAML is required to read adapter manifests but is not importable "
            "in this interpreter (operational error, exit 2)."
        )


def _load_yaml_mapping(manifest_path: Path) -> dict:
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
    return data


def _nonempty_str(data: dict, key: str, manifest_path: Path) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        raise HarnessOperationalError(
            f"Adapter manifest {manifest_path} key {key!r} must be a non-empty "
            f"string; got {value!r}."
        )
    return value.strip()


def _plain_int(value: object, label: str, manifest_path: Path) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise HarnessOperationalError(
            f"Adapter manifest {manifest_path} {label} must be an integer; "
            f"got {value!r}."
        )
    return int(value)


def _project_manifest(data: dict, project_root: Path, manifest_path: Path) -> AdapterManifest:
    if "mode" in data or "governance_state" in data or data.get("parser_dialect") == "root-historical-v1" or "RETIRED" in data.get("states", []):
        raise HarnessOperationalError("Root historical mode/RETIRED is not an ordinary project lifecycle.")
    missing = [k for k in REQUIRED_KEYS if k not in data]
    if missing:
        raise HarnessOperationalError(
            f"Adapter manifest {manifest_path} missing required keys: {missing}"
        )
    return AdapterManifest(
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
        kind=KIND_PROJECT,
    )


def _root_manifest(data: dict, project_root: Path, manifest_path: Path) -> AdapterManifest:
    """Validate `root-harness-adapter/v1` strictly, then normalize it into the
    internal shape (see the module docstring's mapping table)."""
    missing = [k for k in ROOT_REQUIRED_KEYS if k not in data]
    if missing:
        raise HarnessOperationalError(
            f"Adapter manifest {manifest_path} missing required keys: {missing}"
        )

    if "governance_state" in data and "mode" not in data:
        raise HarnessOperationalError("Root governance_state requires explicit governance-only mode.")
    mode = data.get("mode", "legacy")
    if mode not in ("legacy", "governance-only") or ("mode" in data and mode == "legacy"):
        raise HarnessOperationalError(f"Unknown explicit Root mode: {mode!r}")
    governance_state = {}
    if mode == "governance-only":
        if data.get("parser_dialect") != "root-historical-v1" or data.get("states") != ["RETIRED"]:
            raise HarnessOperationalError("Governance Root requires root-historical-v1 and states [RETIRED].")
        from root_historical_status import resolve_state
        governance_state = resolve_state(project_root, data)
    elif data.get("parser_dialect") != "prose-bullet-v1" or "RETIRED" in data.get("states", []):
        raise HarnessOperationalError("Legacy Root requires the frozen ordinary lifecycle parser.")

    working_root = _nonempty_str(data, "working_root", manifest_path)
    if working_root != ".":
        raise HarnessOperationalError(
            f"Adapter manifest {manifest_path} declares working_root "
            f"{working_root!r}; the root product's working root is the "
            "repository root, declared as '.' (D-GOV-21 / SPEC §0.2.2)."
        )
    product = _nonempty_str(data, "product", manifest_path)
    execution_root = _nonempty_str(data, "execution_root", manifest_path)
    prd = _nonempty_str(data, "prd", manifest_path)
    coordination = _nonempty_str(data, "coordination", manifest_path)
    decision_register = _nonempty_str(data, "decision_register", manifest_path)
    status_glob = _nonempty_str(data, "status_glob", manifest_path)
    parser_dialect = _nonempty_str(data, "parser_dialect", manifest_path)

    states = data.get("states")
    if (not isinstance(states, list) or not states
            or not all(isinstance(s, str) and s.strip() for s in states)):
        raise HarnessOperationalError(
            f"Adapter manifest {manifest_path} key 'states' must be a non-empty "
            f"list of non-empty strings; got {states!r}."
        )

    exclude_globs = data.get("exclude_globs") or []
    if not isinstance(exclude_globs, list) or not all(
            isinstance(g, str) for g in exclude_globs):
        raise HarnessOperationalError(
            f"Adapter manifest {manifest_path} key 'exclude_globs' must be a "
            f"list of strings; got {exclude_globs!r}."
        )

    baselines = data.get("baselines")
    if not isinstance(baselines, dict):
        raise HarnessOperationalError(
            f"Adapter manifest {manifest_path} key 'baselines' must be a "
            f"mapping; got {baselines!r}."
        )
    missing_baselines = [k for k in ROOT_REQUIRED_BASELINE_KEYS if k not in baselines]
    if missing_baselines:
        raise HarnessOperationalError(
            f"Adapter manifest {manifest_path} baselines missing required keys: "
            f"{missing_baselines}"
        )
    baseline_files = _plain_int(
        baselines.get("status_files"), "baselines.status_files", manifest_path)
    baseline_mismatch = _plain_int(
        baselines.get("status_mismatch"), "baselines.status_mismatch", manifest_path)
    if baseline_files < 0 or baseline_mismatch < 0:
        raise HarnessOperationalError(
            f"Adapter manifest {manifest_path} baselines must be >= 0; got "
            f"status_files={baseline_files}, status_mismatch={baseline_mismatch}."
        )
    if baseline_mismatch > baseline_files:
        raise HarnessOperationalError(
            f"Adapter manifest {manifest_path} baselines.status_mismatch "
            f"({baseline_mismatch}) exceeds baselines.status_files "
            f"({baseline_files}); the pin is unusable as a drift denominator."
        )
    pinned_at = baselines.get("pinned_at")
    if not isinstance(pinned_at, str) or not pinned_at.strip():
        raise HarnessOperationalError(
            f"Adapter manifest {manifest_path} baselines.pinned_at must be a "
            f"non-empty string recording the pin's provenance; got {pinned_at!r}."
        )

    return AdapterManifest(
        schema=str(data["schema"]),
        project=product,
        plan=prd,
        coordination=coordination,
        decision_register=decision_register,
        # root-harness-adapter/v1 registers no DAG pointer surface. Empty is
        # the normalized "not declared" marker; consumers must branch on
        # declares_dag_pointer() rather than joining an empty relpath.
        dag_pointer="",
        status_glob=status_glob,
        states=[s.strip() for s in states],
        parser_dialect=parser_dialect,
        drift_baseline_mismatch=baseline_mismatch,
        drift_baseline_files=baseline_files,
        exclude_globs=[str(g) for g in exclude_globs],
        validation_commands=[],
        project_root=project_root,
        manifest_path=manifest_path,
        kind=KIND_ROOT,
        working_root=working_root,
        execution_root=execution_root,
        baseline_pinned_at=pinned_at.strip(),
        mode=mode,
        governance_state=governance_state,
    )


def _locate(project_root: Path) -> tuple[str, Path, str]:
    """The single registered manifest under `project_root`.

    Zero found and more-than-one found are both operational errors: the loader
    never picks a location, and never invents one (K-INVENT-1)."""
    found = [(kind, project_root / relpath, schema)
             for kind, relpath, schema in REGISTERED_LOCATIONS
             if (project_root / relpath).is_file()]
    if not found:
        searched = ", ".join(
            str(project_root / relpath) for _, relpath, _ in REGISTERED_LOCATIONS)
        raise HarnessOperationalError(
            f"Adapter manifest missing: {project_root / ADAPTER_RELPATH} "
            f"(operational error, exit 2). Registered locations searched: {searched}."
        )
    if len(found) > 1:
        raise HarnessOperationalError(
            "Ambiguous adapter registration under "
            f"{project_root}: manifests exist at "
            + " and ".join(str(path) for _, path, _ in found)
            + ". Exactly one registered location may carry a manifest; the "
              "loader refuses rather than choosing one (K-INVENT-1)."
        )
    return found[0]


def load_adapter(project_root: Path) -> AdapterManifest:
    """Load and normalize the adapter manifest registered under `project_root`.

    `project_root` is the working root: a project directory, or the repository
    root for the root product (whose manifest lives at
    `execution/_harness/adapter.yaml`)."""
    _require_yaml()
    kind, manifest_path, expected_schema = _locate(project_root)
    data = _load_yaml_mapping(manifest_path)
    if "schema" not in data:
        raise HarnessOperationalError(
            f"Adapter manifest {manifest_path} missing required keys: ['schema']"
        )
    declared = data["schema"]
    if declared != expected_schema:
        known = {schema for _, _, schema in REGISTERED_LOCATIONS}
        if declared in known:
            raise HarnessOperationalError(
                f"Adapter manifest {manifest_path} declares schema {declared!r}, "
                f"but this location is registered for {expected_schema!r}; "
                "location and schema must agree — the loader refuses rather "
                "than falling back to the other shape."
            )
        raise HarnessOperationalError(
            f"Adapter manifest {manifest_path} declares unknown schema "
            f"{declared!r}; this harness understands {expected_schema!r} at "
            f"this location (registered schemas: {sorted(known)})."
        )
    if kind == KIND_ROOT:
        return _root_manifest(data, project_root, manifest_path)
    return _project_manifest(data, project_root, manifest_path)
