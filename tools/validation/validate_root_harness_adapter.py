#!/usr/bin/env python3
"""G1 — root harness adapter registration (D-GOV-21 §5.3).

Deterministic guard shipped by the D-GOV-21 guard-capability tranche (packet
§6 step 6) and wired into governance-harness CI. It gives root `execution/`
the same deterministic status/drift surface the project working roots have:
a committed, schema-valid adapter manifest carrying pinned baselines.

Design of record (why this state surface, in this place, with this schema)
------------------------------------------------------------------------
Project working roots register a harness adapter at
`{PROJECT_ROOT}/_harness/adapter.yaml` with `schema:
practitioner-harness-adapter/v1`, loaded by
`tools/practitioner_harness/adapter_loader.py` and observed by
`adapter_project.py`; its `drift_baseline_files` / `drift_baseline_mismatch`
integers are the pinned baselines against which `harness.py drift` reports.

For the root product `WORKING_ROOT` == `REPO_ROOT` (D-GOV-21, `docs/SPEC.md`
§0.2.2), so the literal project convention would place the manifest at
`{REPO_ROOT}/_harness/adapter.yaml`. This guard instead registers the root
adapter at `{REPO_ROOT}/execution/_harness/adapter.yaml`, for three reasons:

1. It co-locates with G0's registration surface
   (`execution/_harness/root_guards.yaml`), so the root working root has one
   harness control directory rather than two.
2. Root `execution/` is outside the public-export boundary (packet §4) while a
   new top-level `_harness/` would sit beside the exported instruction
   surface.
3. The practitioner harness resolves projects through a hardcoded alias table
   in `tools/practitioner_harness/harness.py`. At authoring time the root was
   not in it and adoption was a recorded open item; that item closed at the
   ROOT-CLOSEOUT-20260725 tranche — the harness now loads this adapter from
   `execution/_harness/adapter.yaml` under aliases `root`/`chirality-root`
   (status/drift observation only). This guard remains the adapter's
   authority; the harness loader is a consumer, never a substitute.

Consequently the schema id is `root-harness-adapter/v1`, not
`practitioner-harness-adapter/v1`: it is key-compatible where the keys carry
the same meaning (`status_glob`, `states`, `parser_dialect`, `coordination`,
`decision_register`, `exclude_globs`) and differs where root reality differs
(`prd` replaces `plan`; `working_root`/`execution_root` are declared
explicitly; baselines are nested under `baselines` with a `pinned_at` SHA so
the pin's provenance is recorded, not assumed). All declared paths are
repo-root-relative POSIX paths.

Behavior (severity semantics per D-GOV-02)
------------------------------------------
- Manifest absent and no `PKG-*`/`DEL-*` materialized under root `execution/`:
  PASS idle (exit 0). This is the lawful pre-instantiation condition — the
  adapter is instantiated by root Project Setup (packet §6 step 8).
- Manifest absent while `PKG-*`/`DEL-*` structure exists under root
  `execution/`: BLOCK (exit 1). Materialized root structure with no adapter
  has no status/drift surface at all, which is the condition §5.3 requires
  this guard to prevent. (This conditional is stricter than "absent → idle";
  it can only fire after materialization, which G0 independently gates.)
- Manifest present: schema-valid, required keys present and well-typed,
  declared pointers repo-relative and existing, pinned baselines verifiable
  against the observed tree. Any failure is BLOCK (exit 1).
- PyYAML unimportable while a manifest exists: operational error (exit 2) —
  the guard cannot observe, so it asserts nothing.

Observation boundary
--------------------
The manifest file's recorded fields; the existence of the repo-relative paths
it declares; the count of files matching its `status_glob` under `{REPO_ROOT}`
after `exclude_globs`; and the names of direct `PKG-*`/`DEL-*` children of
root `execution/`. It does NOT parse `_STATUS.md` documents (mismatch counting
is the practitioner harness's job), does not verify SHA reachability (offline,
shallow-clone-safe), and inspects no other working root. This guard holds no
authority and confers none (K-AUTH-1).

Registration entry it will assert in `execution/_harness/root_guards.yaml`
(written by root Project Setup, never by this tranche)::

    guards:
      G1:
        registered: true
        status: passing
        validator: tools/validation/validate_root_harness_adapter.py
        tests: tools/validation/test_validate_root_harness_adapter.py
        state_surface: execution/_harness/adapter.yaml
        schema: root-harness-adapter/v1
"""

from __future__ import annotations

import re
import subprocess
import root_governance_state as governance
import sys
from pathlib import Path, PurePosixPath

ADAPTER_RELPATH = Path("execution/_harness/adapter.yaml")
ADAPTER_SCHEMA = "root-harness-adapter/v1"

REQUIRED_KEYS = (
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

# Declared pointers that must exist in the checkout.
POINTER_KEYS = ("prd", "coordination", "decision_register", "execution_root")

REQUIRED_BASELINE_KEYS = ("status_files", "status_mismatch", "pinned_at")

SHA_RE = re.compile(r"^[0-9a-f]{7,40}$")


def repo_root() -> Path:
    out = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=True,
    )
    return Path(out.stdout.strip())


def materialized_children(root: Path) -> list[str]:
    """Direct `PKG-*`/`DEL-*` child directories of root `execution/` (G0's boundary)."""
    execution = root / "execution"
    if not execution.is_dir():
        return []
    return sorted(
        child.name
        for child in execution.iterdir()
        if child.is_dir()
        and (child.name.startswith("PKG-") or child.name.startswith("DEL-"))
    )


def is_repo_relative(value: str) -> bool:
    if not value or value.startswith("/") or value.startswith("~"):
        return False
    if re.match(r"^[A-Za-z]:[\\/]", value):
        return False
    return ".." not in PurePosixPath(value).parts


def excluded(rel: PurePosixPath, exclude_globs: list[str]) -> bool:
    parts = set(rel.parts)
    for pattern in exclude_globs:
        if pattern.endswith("/**"):
            if pattern[:-3] in parts:
                return True
        elif rel.match(pattern):
            return True
    return False


def count_status_files(root: Path, status_glob: str, exclude_globs: list[str]) -> int:
    total = 0
    for path in root.glob(status_glob):
        if not path.is_file():
            continue
        rel = PurePosixPath(path.relative_to(root).as_posix())
        if excluded(rel, exclude_globs):
            continue
        total += 1
    return total


def check(root: Path) -> tuple[int, list[str]]:
    """Returns (exit_code, report_lines). 0 PASS, 1 BLOCK, 2 operational."""
    try:
        import yaml
        mode_path = root / ADAPTER_RELPATH
        mode_data = yaml.safe_load(mode_path.read_text()) if mode_path.is_file() else {}
        if isinstance(mode_data, dict):
            if governance.check_mode(mode_data):
                return _check_governance_g1(root, mode_data)
        elif mode_path.is_file():
            raise governance.GovernanceError('Root state is not a mapping')
    except yaml.YAMLError as exc:
        return 1, ['unparseable Root state: ' + str(exc)]
    except (governance.GovernanceError, ValueError, OSError) as exc:
        return 1, ['G1 BLOCK: ' + str(exc)]
    lines: list[str] = []
    path = root / ADAPTER_RELPATH
    children = materialized_children(root)

    if not path.is_file():
        if children:
            lines.append(
                f"G1 BLOCK: root harness adapter {ADAPTER_RELPATH.as_posix()} is "
                "absent while PKG-*/DEL-* structure exists under root execution/ "
                "(" + ", ".join(children) + "); materialized root structure must "
                "carry a status/drift surface (D-GOV-21 §5.3)."
            )
            return 1, lines
        lines.append(
            f"G1 PASS: root harness adapter {ADAPTER_RELPATH.as_posix()} absent and "
            "no PKG-*/DEL-* materialized under root execution/; guard idle "
            "(pre-instantiation condition — Project Setup instantiates the adapter)."
        )
        return 0, lines

    try:
        import yaml  # type: ignore
    except ImportError:
        lines.append(
            "G1 OPERATIONAL (exit 2): PyYAML is not importable, so the present "
            f"adapter {ADAPTER_RELPATH.as_posix()} cannot be observed; this guard "
            "asserts nothing."
        )
        return 2, lines

    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - any parse failure is a malformed surface.
        lines.append(
            f"G1 BLOCK: adapter {ADAPTER_RELPATH.as_posix()} is unparseable: {exc}"
        )
        return 1, lines

    failures: list[str] = []
    if not isinstance(data, dict):
        lines.append(
            f"G1 BLOCK: adapter {ADAPTER_RELPATH.as_posix()} top level is not a mapping."
        )
        return 1, lines

    missing = [k for k in REQUIRED_KEYS if k not in data]
    if missing:
        failures.append(f"missing required keys: {sorted(missing)}")

    schema = data.get("schema")
    if schema is not None and schema != ADAPTER_SCHEMA:
        failures.append(
            f"schema is {schema!r}; this guard understands {ADAPTER_SCHEMA!r}"
        )

    working_root = data.get("working_root")
    if "working_root" in data and working_root != ".":
        failures.append(
            f"working_root is {working_root!r}; the root product's working root is "
            "the repository root, declared as '.' (D-GOV-21)"
        )
    execution_root = data.get("execution_root")
    if "execution_root" in data and execution_root != "execution":
        failures.append(
            f"execution_root is {execution_root!r}; the root execution root is "
            "'execution' (D-GOV-21)"
        )

    for key in POINTER_KEYS:
        value = data.get(key)
        if value is None:
            continue
        if not isinstance(value, str) or not is_repo_relative(value):
            failures.append(
                f"{key} is not a repo-relative POSIX path: {value!r}"
            )
            continue
        if not (root / value).exists():
            failures.append(f"{key} points at {value!r}, which does not exist")

    states = data.get("states")
    if "states" in data and (
        not isinstance(states, list)
        or not states
        or not all(isinstance(s, str) and s for s in states)
    ):
        failures.append("states must be a non-empty list of strings")

    for key in ("product", "status_glob", "parser_dialect"):
        value = data.get(key)
        if key in data and (not isinstance(value, str) or not value):
            failures.append(f"{key} must be a non-empty string")

    exclude_globs = data.get("exclude_globs") or []
    if not isinstance(exclude_globs, list) or not all(
        isinstance(g, str) for g in exclude_globs
    ):
        failures.append("exclude_globs must be a list of strings")
        exclude_globs = []

    baselines = data.get("baselines")
    if "baselines" in data:
        if not isinstance(baselines, dict):
            failures.append("baselines must be a mapping")
        else:
            missing_baselines = [
                k for k in REQUIRED_BASELINE_KEYS if k not in baselines
            ]
            if missing_baselines:
                failures.append(
                    f"baselines missing required keys: {sorted(missing_baselines)}"
                )
            pinned_at = baselines.get("pinned_at")
            if pinned_at is not None and (
                not isinstance(pinned_at, str) or not SHA_RE.match(pinned_at)
            ):
                failures.append(
                    f"baselines.pinned_at is not a 7-40 character hex SHA: {pinned_at!r}"
                )
            declared_files = baselines.get("status_files")
            declared_mismatch = baselines.get("status_mismatch")
            if declared_files is not None and not isinstance(declared_files, bool) and isinstance(declared_files, int):
                status_glob = data.get("status_glob")
                if isinstance(status_glob, str) and status_glob:
                    try:
                        observed = count_status_files(root, status_glob, exclude_globs)
                    except (ValueError, OSError) as exc:
                        failures.append(f"status_glob {status_glob!r} is unusable: {exc}")
                    else:
                        if observed != declared_files:
                            failures.append(
                                "pinned baseline drift: baselines.status_files "
                                f"declares {declared_files} but {observed} file(s) "
                                f"match status_glob {status_glob!r} under the checkout"
                            )
            elif declared_files is not None:
                failures.append("baselines.status_files must be an integer")

            if isinstance(declared_mismatch, bool) or not isinstance(
                declared_mismatch, int
            ):
                if declared_mismatch is not None:
                    failures.append("baselines.status_mismatch must be an integer")
            else:
                if declared_mismatch < 0:
                    failures.append("baselines.status_mismatch must be >= 0")
                elif (
                    isinstance(declared_files, int)
                    and not isinstance(declared_files, bool)
                    and declared_mismatch > declared_files
                ):
                    failures.append(
                        f"baselines.status_mismatch ({declared_mismatch}) exceeds "
                        f"baselines.status_files ({declared_files})"
                    )
                elif declared_mismatch > 0 and not str(
                    baselines.get("mismatch_disposition", "")
                ).strip():
                    failures.append(
                        "baselines.status_mismatch is nonzero but no "
                        "baselines.mismatch_disposition records why the pin "
                        "accepts drift"
                    )

    if failures:
        lines.append(
            f"G1 BLOCK: root harness adapter {ADAPTER_RELPATH.as_posix()} is invalid:"
        )
        lines.extend(f"  - {failure}" for failure in failures)
        return 1, lines

    lines.append(
        f"G1 PASS: root harness adapter {ADAPTER_RELPATH.as_posix()} is schema-valid "
        f"({ADAPTER_SCHEMA}); declared pointers exist and pinned baselines match the "
        f"observed tree (status_files={baselines.get('status_files')}, "
        f"pinned_at={baselines.get('pinned_at')})."
    )
    if children:
        lines.append(
            "G1: materialized root packages/deliverables observed: "
            + ", ".join(children)
        )
    return 0, lines


def _check_governance_g1(root: Path, data: dict) -> tuple[int, list[str]]:
    try:
        required={'schema':'root-harness-adapter/v1','product':'chirality-root','working_root':'.','execution_root':'execution',
            'prd':'docs/PRD_ROOT.md','coordination':'execution/_Coordination/CURRENT_WORKPLAN.md',
            'decision_register':'docs/governance_harness/_DECISIONS/_REGISTER.md',
            'loop_init':'execution/_Coordination/LOOP_INIT.md','receipts':'execution/_Coordination/LOOP_RECEIPTS.md',
            'status_glob':'execution/PKG-*/1_Working/DEL-*/_STATUS.md','parser_dialect':'root-historical-v1'}
        for key,value in required.items():
            if data.get(key)!=value: raise governance.GovernanceError('invalid governance adapter '+key)
        for key in ['prd','coordination','decision_register','loop_init','receipts']:
            governance.safe_path(root,data[key])
        if data.get('states')!=['RETIRED']: raise governance.GovernanceError('Root historical states must be RETIRED only')
        if data.get('exclude_globs') not in ([],['.archive/**']): raise governance.GovernanceError('historical census exclusions cannot hide carriers')
        bases=data.get('baselines',{})
        if bases.get('status_files')!=53 or bases.get('status_mismatch')!=0:
            raise governance.GovernanceError('historical adapter baseline mismatch')
        if not isinstance(bases.get('pinned_at'),str) or len(bases['pinned_at'])!=40:
            raise governance.GovernanceError('historical baseline requires full basis commit')
        state=governance.load_governance_state(root,data,verify_statuses=governance.status_verification(root,data))
        declared={r['path'] for r in state['source_statuses']}
        actual={str(p.relative_to(root)) for p in root.glob(data['status_glob']) if p.is_file()}
        if actual!=declared: raise governance.GovernanceError('adapter status identity census mismatch')
        return 0,['G1 PASS: governance adapter exact pointers, controls and historical census; stage='+state['stage']]
    except (governance.GovernanceError,OSError,ValueError,KeyError,TypeError) as exc:
        return 1,['G1 BLOCK: '+str(exc)]


def main() -> int:
    root = repo_root()
    code, lines = check(root)
    for line in lines:
        print(line)
    return code


if __name__ == "__main__":
    sys.exit(main())
