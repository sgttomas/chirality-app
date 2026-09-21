#!/usr/bin/env python3
"""G0 — root materialization fence (D-GOV-21 §5.3).

Deterministic guard shipped by the D-GOV-21 implementation tranche and wired
into governance-harness CI. It enforces the ruled gate ordering: no `PKG-*` or
`DEL-*` structure may exist as a direct child of root `execution/` until the
D-GOV-21 guards G1-G4 are registered and passing.

Behavior (severity semantics per D-GOV-02):

- No `execution/PKG-*` / `execution/DEL-*` direct children exist:
  PASS (exit 0). This is the state at ruling time; nothing materializes at
  ruling (packet §10).
- Such children exist and the guard registration surface
  (`execution/_harness/root_guards.yaml`) is absent, unreadable, or does not
  record every guard G1-G4 as `registered: true` with `status: passing`:
  BLOCK (exit 1).
- Children exist and all four guards are registered and passing:
  PASS (exit 0), reporting the registration state it verified.

The registration surface is written by the guard-capability tranche (packet
§6 step 6) and instantiated with state at root Project Setup (packet §5.3).
This fence checks recorded registration; it holds no authority and confers
none (K-AUTH-1) — it exists so the §6 ordering is mechanically real from the
moment D-GOV-21 takes effect.

Observation boundary: direct children of `{REPO_ROOT}/execution/` matching
`PKG-*`/`DEL-*` by name, plus the registration file's recorded fields. It does
not inspect package contents, nested structure, or any other working root.
"""

from __future__ import annotations

import subprocess
import root_governance_state as governance
import sys
from pathlib import Path

REQUIRED_GUARDS = ("G1", "G2", "G3", "G4")
REGISTRATION_RELPATH = Path("execution/_harness/root_guards.yaml")


def repo_root() -> Path:
    out = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=True,
    )
    return Path(out.stdout.strip())


def materialized_children(root: Path) -> list[str]:
    execution = root / "execution"
    if not execution.is_dir():
        return []
    return sorted(
        child.name
        for child in execution.iterdir()
        if child.is_dir() and (child.name.startswith("PKG-") or child.name.startswith("DEL-"))
    )


def load_registration(root: Path) -> dict[str, dict[str, object]] | None:
    """Parse the guard registration file. Returns None if absent/unreadable.

    Uses PyYAML when available; the expected shape is:

        guards:
          G1: {registered: true, status: passing, ...}
          ...
    """
    path = root / REGISTRATION_RELPATH
    if not path.is_file():
        return None
    try:
        import yaml  # type: ignore

        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception:
        return None
    if not isinstance(data, dict):
        return None
    guards = data.get("guards")
    if not isinstance(guards, dict):
        return None
    return {str(k): v for k, v in guards.items() if isinstance(v, dict)}


def check(root: Path) -> tuple[int, list[str]]:
    """Returns (exit_code, report_lines)."""
    try:
        import yaml
        mode_path = root / REGISTRATION_RELPATH
        mode_data = yaml.safe_load(mode_path.read_text()) if mode_path.is_file() else {}
        if isinstance(mode_data, dict):
            if governance.check_mode(mode_data):
                return _check_governance_g0(root, mode_data)
        elif mode_path.is_file():
            raise governance.GovernanceError('Root state is not a mapping')
    except yaml.YAMLError as exc:
        return 1, ['unparseable Root state: ' + str(exc)]
    except (governance.GovernanceError, ValueError, OSError) as exc:
        return 1, ['G0 BLOCK: ' + str(exc)]
    lines: list[str] = []
    children = materialized_children(root)
    if not children:
        lines.append(
            "G0 PASS: no PKG-*/DEL-* direct children under root execution/; "
            "fence idle (D-GOV-21 gate not yet in play)."
        )
        return 0, lines

    lines.append(
        "G0: materialized root packages/deliverables found: " + ", ".join(children)
    )
    guards = load_registration(root)
    if guards is None:
        lines.append(
            f"G0 BLOCK: guard registration surface {REGISTRATION_RELPATH} is "
            "absent or unreadable while PKG-*/DEL-* structure exists under root "
            "execution/ (D-GOV-21 §5.3: materialization requires G1-G4 "
            "registered and passing)."
        )
        return 1, lines

    failures: list[str] = []
    for guard in REQUIRED_GUARDS:
        entry = guards.get(guard)
        if entry is None:
            failures.append(f"{guard}: not registered")
            continue
        if entry.get("registered") is not True:
            failures.append(f"{guard}: registered != true")
        if entry.get("status") != "passing":
            failures.append(f"{guard}: status != passing (got {entry.get('status')!r})")

    if failures:
        lines.append("G0 BLOCK: guard registration incomplete or not passing:")
        lines.extend(f"  - {failure}" for failure in failures)
        return 1, lines

    lines.append(
        "G0 PASS: G1-G4 registered and passing per "
        f"{REGISTRATION_RELPATH}; materialization gate satisfied."
    )
    return 0, lines


def _check_governance_g0(root: Path, data: dict) -> tuple[int, list[str]]:
    try:
        state=governance.load_governance_state(root,data,verify_statuses=governance.status_verification(root,data))
        expected={str(Path(r['path']).parent) for r in state['source_statuses']}
        packages={r['source_package'] for r in state['source_statuses']}
        actual_packages={p.name for p in (root/'execution').glob('PKG-*') if p.is_dir()}
        if actual_packages!=packages: raise governance.GovernanceError('unexpected/missing Root package')
        def deliverable_evidence(path):
            relative=str(path.relative_to(root))
            return any(relative.startswith(base+'/_run_records/') for base in expected)
        actual={str(p.relative_to(root)) for pkg in actual_packages for p in (root/'execution'/pkg).rglob('DEL-*') if p.is_dir() and not deliverable_evidence(p)}
        # Registered tool roots hold immutable/candidate evidence, not active materialization.
        evidence_roots={'_Aggregation','_Change','_Coordination','_Decomposition','_Estimates','_Evaluation','_Reconciliation','_Archive','_Scripts','_Sources','_LocalIndexes','_DomainEngines','_Schedule','_ScopeChange','_harness'}
        for container in (root/'execution').iterdir():
            if not container.is_dir() or container.name in evidence_roots: continue
            for item in [container,*container.rglob('*')]:
                if not item.is_dir() or deliverable_evidence(item): continue
                rel=str(item.relative_to(root))
                if item.name.startswith('DEL-'): actual.add(rel)
                if item.name.startswith('PKG-') and rel not in {'execution/'+p for p in packages}:
                    raise governance.GovernanceError('nested or unregistered Root package')
        if actual!=expected: raise governance.GovernanceError('unexpected/missing nested or direct Root carrier')
        guards=data.get('guards',{})
        for name in REQUIRED_GUARDS:
            if guards.get(name,{}).get('registered') is not True or guards.get(name,{}).get('status')!='passing':
                raise governance.GovernanceError(name+' registration not passing')
        return 0,['G0 PASS: exact governance/historical census validated; stage='+state['stage']+'; no production authorization']
    except (governance.GovernanceError, OSError, ValueError, KeyError, TypeError) as exc:
        return 1,['G0 BLOCK: '+str(exc)]


def main() -> int:
    root = repo_root()
    code, lines = check(root)
    for line in lines:
        print(line)
    return code


if __name__ == "__main__":
    sys.exit(main())
