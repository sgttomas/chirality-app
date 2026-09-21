#!/usr/bin/env python3
"""G3 — pre-dispatch root work-graph check (D-GOV-21 §5.3, mechanisms M1/M2).

Deterministic guard shipped by the D-GOV-21 guard-capability tranche (packet
§6 step 6) and wired into governance-harness CI. It verifies, before dispatch,
that each active node's write targets are declared, that concurrently active
nodes' targets are disjoint or serialized per M1, and that instruction-surface
intersection carries the M2 marker. The first accepted work graph is
instantiated later, by root Project Setup (packet §6 step 8); this tranche
ships capability only.

Governance mode
---------------
mode: governance-only binds the same governance_state as G2. Active nodes
require Root control ownership and published
capability_basis and owner_acts, eligible runtime_capabilities and completed
local predecessors. execution_class governance-migration uses the approved exact
Gate4 migration scopes; governance-operation requires Gate5 effectiveness.
Pending/partial retirement transactions prohibit either class. stage dispatch binds a hashed child-execution JSON record
(node, session_id, parent_session_id, stage); stage fan-in additionally binds a
hashed return. This is recorded execution provenance, not a process-liveness
claim. It cannot turn a brief into execution or a branch owner act into a
published acceptance. Static empty graphs can validate before effectiveness.
Legacy observation boundaries below apply only outside governance mode.

Design of record (state surface, schema, marker convention, modes)
------------------------------------------------------------------
State surface: `{REPO_ROOT}/execution/_harness/work_graph.yaml`, co-located
with G0's `root_guards.yaml`, G1's `adapter.yaml`, and G2's
`surface_ownership.yaml`. Schema id: `root-work-graph/v1`. All paths are
repo-root-relative POSIX paths or globs. Shape::

    schema: root-work-graph/v1
    accepted_basis: <commit sha>     # M3 frozen instruction basis for the graph
    nodes:
      - id: N1
        status: active              # active | pending | complete | blocked
        owner: PKG-01_Example       # optional: owning G2 register entry
        write_targets:
          - execution/PKG-01_Example/**
        depends_on: [N0]            # optional
        serialized_after: [N0]      # optional explicit M1 serialization edges
        integration_owner: ""       # optional: the single declared integration
                                    # owner for an overlapping target
        m2_marker: "M2:docs/governance_harness/tranche_manifests/<ID>.yaml"

**M2 marker convention (defined here).** The marker is the string field
`m2_marker`, whose value is `M2:<repo-relative path>` naming the tranche
manifest (G4's surface) that records the M2 gate for the instruction-surface
touch. It is REQUIRED on any node — and on any run brief — whose declared
write targets intersect the instruction surface, and the named path must
exist. The marker records that a gate was taken; it does not grant
authorization, and no deterministic marker ever could (K-AUTH-1).

**Modes.**

- *CI mode* (no arguments): if the work-graph surface is absent, PASS idle. If
  it exists, validate its internal consistency (schema, unique ids, known
  statuses, resolvable dependency references, no dependency cycle, declared
  and repo-relative write targets on every non-complete node, active-node
  disjointness-or-serialization, M2 markers). When the G2 register exists, a
  node declaring `owner` must have its targets covered by that register entry
  (M1 tie-in); when the register is absent that cross-check is skipped and
  reported as not applicable, never assumed.
- *Dispatch mode* (`--work-graph PATH --brief PATH [--brief PATH ...]`):
  everything CI mode checks, plus, for each named run brief: the brief's node
  exists and is `active`; every write target the brief declares is covered by
  that node's declared targets (undeclared write target → BLOCK); the brief
  carries the M2 marker if its targets intersect the instruction surface; and
  the dispatched set is pairwise disjoint-or-serialized against every other
  active node. A brief is a `.yaml`/`.yml` mapping or a Markdown file whose
  first block is YAML front matter delimited by `---` lines; a brief with no
  machine-readable dispatch block is a BLOCK, never a guess.

Behavior (severity semantics per D-GOV-02): exit 0 PASS, exit 1 BLOCK, exit 2
operational error (PyYAML unimportable, unusable arguments, unreadable file).
A dependency cycle is BLOCK and is reported as an unresolved ordering that
must be resolved by a recorded move per the `AGENTS.md` cycle-resolution rule;
this guard never linearizes a cycle itself.

Observation boundary
--------------------
The work graph's and briefs' recorded fields, the existence of paths those
fields name, and (when present) the G2 register's declared targets. It does
not observe running processes, git state, or any other working root; the
"concurrently active" relation is read from declared `status`, not detected.
This guard holds no authority and confers none (K-AUTH-1).

Registration entry it will assert in `execution/_harness/root_guards.yaml`
(written by root Project Setup, never by this tranche)::

    guards:
      G3:
        registered: true
        status: passing
        validator: tools/validation/validate_root_work_graph_dispatch.py
        tests: tools/validation/test_validate_root_work_graph_dispatch.py
        state_surface: execution/_harness/work_graph.yaml
        schema: root-work-graph/v1
        dispatch_mode: "--work-graph PATH --brief PATH [--brief PATH ...]"
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath

WORK_GRAPH_RELPATH = Path("execution/_harness/work_graph.yaml")
WORK_GRAPH_SCHEMA = "root-work-graph/v1"
REGISTER_RELPATH = Path("execution/_harness/surface_ownership.yaml")

VALID_STATUSES = ("active", "pending", "complete", "blocked")
M2_MARKER_PREFIX = "M2:"

# Instruction surface per the `docs/SPEC.md` §0.2.1 enumeration as amended by
# D-GOV-26, which ratified `CLAUDE.md` (the session-init instruction pointer)
# and `.github/workflows/` (the CI workflow definitions that gate merges) into
# the set. Kept identical to G2's and G4's sets by construction; any change is
# a governance action, not a local edit.
INSTRUCTION_SURFACE_FILES = ("AGENTS.md", "CLAUDE.md")
INSTRUCTION_SURFACE_DIRS = (
    "agents/",
    "skills/",  # Historical packages remain instruction surfaces.
    "workflows/",
    "tools/",
    "docs/",
    "init/",
    ".github/workflows/",
)


def repo_root() -> Path:
    out = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=True,
    )
    return Path(out.stdout.strip())


def is_repo_relative(value: str) -> bool:
    if not value or value.startswith("/") or value.startswith("~"):
        return False
    if re.match(r"^[A-Za-z]:[\\/]", value):
        return False
    return ".." not in PurePosixPath(value).parts


def normalize_target(target: str) -> str:
    """Strip leading `./` segments only — never a leading dot of `.github/`."""
    normalized = target.strip()
    while normalized.startswith("./"):
        normalized = normalized[2:]
    return normalized


def intersects_instruction_surface(target: str) -> bool:
    normalized = normalize_target(target)
    if normalized in ("*", "**", "**/*"):
        return True
    if normalized in INSTRUCTION_SURFACE_FILES:
        return True
    return any(normalized.startswith(prefix) for prefix in INSTRUCTION_SURFACE_DIRS)


def literal_prefix(target: str) -> str:
    """The fixed leading path portion of a target, ignoring any glob tail."""
    normalized = normalize_target(target)
    head = normalized.split("*", 1)[0]
    return head.rstrip("/")


def targets_overlap(a: str, b: str) -> bool:
    """Conservative path-boundary overlap test between two targets/globs."""
    pa, pb = literal_prefix(a), literal_prefix(b)
    if pa == pb:
        return True
    if not pa or not pb:
        return True
    return pa.startswith(pb + "/") or pb.startswith(pa + "/")


def covered_by(target: str, declared: list[str]) -> bool:
    """True if `target` falls inside at least one `declared` target."""
    prefix = literal_prefix(target)
    for candidate in declared:
        base = literal_prefix(candidate)
        if not base:
            return True
        if prefix == base or prefix.startswith(base + "/"):
            return True
    return False


def load_yaml_mapping(path: Path) -> tuple[dict | None, str | None, bool]:
    """Returns (mapping, error, operational). `operational` distinguishes exit 2."""
    try:
        import yaml  # type: ignore
    except ImportError:
        return None, "PyYAML is not importable; cannot observe YAML surfaces", True
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return None, f"{path.name} is unreadable: {exc}", True

    if path.suffix.lower() in (".yaml", ".yml"):
        payload = text
    elif text.startswith("---\n") or text.startswith("---\r\n"):
        rest = text.split("\n", 1)[1]
        end = re.search(r"^---\s*$", rest, re.MULTILINE)
        if end is None:
            return None, f"{path.name}: unterminated YAML front matter", False
        payload = rest[: end.start()]
    else:
        return (
            None,
            f"{path.name}: no machine-readable dispatch block (expected a .yaml/.yml "
            "mapping or leading YAML front matter delimited by '---')",
            False,
        )

    try:
        data = yaml.safe_load(payload)
    except Exception as exc:  # noqa: BLE001 - any parse failure is a malformed surface.
        return None, f"{path.name} is unparseable: {exc}", False
    if not isinstance(data, dict):
        return None, f"{path.name}: top level is not a mapping", False
    return data, None, False


def load_register_targets(root: Path) -> dict[str, list[str]] | None:
    """Declared write targets per G2 register entry, or None when absent/unreadable."""
    path = root / REGISTER_RELPATH
    if not path.is_file():
        return None
    data, error, _ = load_yaml_mapping(path)
    if data is None or error is not None:
        return None
    entries = data.get("entries")
    if not isinstance(entries, list):
        return None
    out: dict[str, list[str]] = {}
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        entry_id = entry.get("id")
        targets = entry.get("write_targets")
        if isinstance(entry_id, str) and isinstance(targets, list):
            out[entry_id] = [str(t) for t in targets]
    return out


def find_cycle(edges: dict[str, set[str]]) -> list[str] | None:
    """Returns one dependency cycle as a node list, or None."""
    state: dict[str, int] = {}
    stack: list[str] = []

    def visit(node: str) -> list[str] | None:
        state[node] = 1
        stack.append(node)
        for nxt in sorted(edges.get(node, ())):
            if nxt not in edges:
                continue
            if state.get(nxt, 0) == 0:
                found = visit(nxt)
                if found:
                    return found
            elif state.get(nxt) == 1:
                return stack[stack.index(nxt):] + [nxt]
        stack.pop()
        state[node] = 2
        return None

    for node in sorted(edges):
        if state.get(node, 0) == 0:
            found = visit(node)
            if found:
                return found
    return None


def check_governance_graph(root: Path, data: dict, nodes: dict[str, dict]) -> list[str]:
    """Observe pinned launch/return records, never infer a child from a brief.

    Evidence is instruction-asserted execution provenance, not process liveness.
    Published owner acts and branch-local predecessor completion are distinct.
    """
    from root_governance_state import GovernanceError, load_governance_state, safe_path, verify_owner_act, status_verification
    from validate_root_surface_ownership import canonical_target, canonical_covered, check_governance
    errors: list[str] = []
    try:
        state = load_governance_state(
            root, data,
            require_effective=any(n.get("status") == "active" and n.get("execution_class") != "governance-migration" for n in nodes.values()),
            verify_statuses=status_verification(root, data),
        )
        transaction = state.get("transaction")
        if transaction is not None and any(n.get("status") == "active" for n in nodes.values()):
            if not isinstance(transaction, dict):
                raise GovernanceError("invalid transaction reference")
            journal = safe_path(root, transaction.get("path"), allow_missing=False)
            raw = journal.read_bytes()
            if transaction.get("sha256") is not None and hashlib.sha256(raw).hexdigest() != transaction["sha256"]:
                raise GovernanceError("transaction journal hash mismatch")
            if json.loads(raw).get("state") != "APPLIED":
                raise GovernanceError("pending/partial transaction prohibits dispatch")
        register, error, _ = load_yaml_mapping(root / REGISTER_RELPATH)
        if error or not register or register.get("mode") != "governance-only":
            raise GovernanceError("governance dispatch requires valid governance G2 register")
        code, messages = check_governance(root, register)
        if code or register.get("governance_state") != data.get("governance_state"):
            raise GovernanceError(f"G2 ownership/state mismatch: {messages}")
        owners = {entry["id"]: entry for entry in register["entries"]}
        for node_id, node in nodes.items():
            owner = node.get("owner")
            if owner not in owners or owners[owner]["project"] != "root":
                raise GovernanceError(f"{node_id}: unknown, historical or non-Root owner")
            for target in node.get("write_targets", []):
                if not canonical_covered(root, target, owners[owner]["write_targets"]):
                    raise GovernanceError(f"{node_id}: foreign or undeclared write target")
            marker = node.get("m2_marker")
            if isinstance(marker, str) and marker.startswith(M2_MARKER_PREFIX):
                safe_path(root, marker[len(M2_MARKER_PREFIX):].strip(), allow_missing=False)
            if node.get("status") != "active":
                continue
            if node.get("execution_class") not in ("governance-migration", "governance-operation"):
                raise GovernanceError(f"{node_id}: explicit execution_class required")
            for key in ("depends_on", "serialized_after"):
                predecessors = node.get(key, [])
                if isinstance(predecessors, str):
                    predecessors = [predecessors]
                for predecessor in predecessors:
                    if predecessor not in nodes or nodes[predecessor].get("status") != "complete":
                        raise GovernanceError(f"{node_id}: predecessor not complete: {predecessor}")
            held = state.get("held_capabilities")
            if not isinstance(held, list) or not all(isinstance(c, str) and c for c in held):
                raise GovernanceError("accepted held capability inventory is required")
            capabilities = node.get("runtime_capabilities", [])
            if not isinstance(capabilities, list) or capabilities:
                raise GovernanceError(f"{node_id}: runtime feature capabilities are not granted by the migration")
            basis = node.get("capability_basis")
            verify_owner_act(root, basis, state["gate4"]["subject_sha256"])
            acts = node.get("owner_acts", [])
            if not isinstance(acts, list):
                raise GovernanceError("owner_acts must be a list")
            for act in acts:
                if not isinstance(act, dict):
                    raise GovernanceError("owner act must be a mapping")
                verify_owner_act(root, act.get("ref"), act.get("subject_sha256"))
            stage = node.get("stage")
            if stage not in ("dispatch", "fan-in"):
                raise GovernanceError(f"{node_id}: stage must be dispatch or fan-in")
            evidence_ref = node.get("child_evidence")
            if not isinstance(evidence_ref, dict):
                raise GovernanceError(f"{node_id}: actual child evidence is required")
            evidence_path = safe_path(root, evidence_ref.get("path"), allow_missing=False)
            raw = evidence_path.read_bytes()
            if hashlib.sha256(raw).hexdigest() != evidence_ref.get("sha256"):
                raise GovernanceError(f"{node_id}: child evidence hash mismatch")
            evidence = json.loads(raw)
            for key in ("session_id", "parent_session_id"):
                if not isinstance(node.get(key), str) or not node[key] or evidence.get(key) != node[key]:
                    raise GovernanceError(f"{node_id}: reconstructible child {key} required")
            if node["session_id"] == node["parent_session_id"]:
                raise GovernanceError("child session cannot be its own parent")
            if evidence.get("node") != node_id or evidence.get("stage") != stage or evidence.get("kind") != "child-execution":
                raise GovernanceError(f"{node_id}: evidence is not matching execution record")
            if stage == "fan-in":
                returned = evidence.get("return")
                if not isinstance(returned, dict):
                    raise GovernanceError(f"{node_id}: fan-in requires actual child return")
                payload = safe_path(root, returned.get("path"), allow_missing=False).read_bytes()
                if hashlib.sha256(payload).hexdigest() != returned.get("sha256"):
                    raise GovernanceError(f"{node_id}: child return hash mismatch")
        # Canonical aliases can overlap even where textual prefixes do not.
        active = [n for n in nodes if nodes[n].get("status") == "active"]
        for index, left in enumerate(active):
            for right in active[index + 1:]:
                for lt in nodes[left].get("write_targets", []):
                    for rt in nodes[right].get("write_targets", []):
                        a, b = canonical_target(root, lt), canonical_target(root, rt)
                        if (a.is_relative_to(b) or b.is_relative_to(a)) and not serialized(nodes, left, right):
                            raise GovernanceError(f"{left}/{right}: canonical write overlap without serialization")
    except (GovernanceError, KeyError, TypeError, ValueError, OSError) as exc:
        errors.append(str(exc))
    return errors


def check_graph(
    root: Path, graph_path: Path, data: dict
) -> tuple[list[str], list[str], dict[str, dict]]:
    """Validate a loaded work graph. Returns (failures, notes, nodes_by_id)."""
    failures: list[str] = []
    notes: list[str] = []
    rel = graph_path.name

    if data.get("schema") != WORK_GRAPH_SCHEMA:
        failures.append(
            f"{rel}: schema is {data.get('schema')!r}; this guard understands "
            f"{WORK_GRAPH_SCHEMA!r}"
        )
    basis = data.get("accepted_basis")
    if not isinstance(basis, str) or not re.match(r"^[0-9a-f]{7,40}$", basis):
        failures.append(
            f"{rel}: accepted_basis must be a 7-40 character hex commit SHA "
            f"(M3 frozen instruction basis); got {basis!r}"
        )

    raw_nodes = data.get("nodes")
    if not isinstance(raw_nodes, list):
        failures.append(f"{rel}: nodes must be a list (may be empty)")
        raw_nodes = []

    nodes: dict[str, dict] = {}
    for index, node in enumerate(raw_nodes):
        label = f"nodes[{index}]"
        if not isinstance(node, dict):
            failures.append(f"{rel}: {label} is not a mapping")
            continue
        node_id = node.get("id")
        if not isinstance(node_id, str) or not node_id.strip():
            failures.append(f"{rel}: {label} has no usable id")
            continue
        if node_id in nodes:
            failures.append(f"{rel}: duplicate node id {node_id!r}")
            continue
        nodes[node_id] = node

    register = load_register_targets(root)
    if register is None:
        notes.append(
            "G2 register absent or unreadable; node-to-register coverage "
            "cross-check NOT_APPLICABLE (skipped, not assumed)"
        )

    edges: dict[str, set[str]] = {nid: set() for nid in nodes}
    for node_id, node in nodes.items():
        status = node.get("status")
        if status not in VALID_STATUSES:
            failures.append(
                f"{rel}: node {node_id}: status {status!r} not in {list(VALID_STATUSES)}"
            )

        targets = node.get("write_targets")
        if status != "complete":
            if (
                not isinstance(targets, list)
                or not targets
                or not all(isinstance(t, str) and t for t in targets)
            ):
                failures.append(
                    f"{rel}: node {node_id}: write_targets must be a non-empty list "
                    "of strings for any non-complete node (M1)"
                )
                targets = []
        if not isinstance(targets, list):
            targets = []
        clean = [t for t in targets if isinstance(t, str) and t]
        for target in clean:
            if not is_repo_relative(target):
                failures.append(
                    f"{rel}: node {node_id}: write target {target!r} is not a "
                    "repo-relative POSIX path"
                )

        for key in ("depends_on", "serialized_after"):
            refs = node.get(key) or []
            if isinstance(refs, str):
                refs = [refs]
            if not isinstance(refs, list):
                failures.append(f"{rel}: node {node_id}: {key} must be a list of node ids")
                continue
            for ref in refs:
                if not isinstance(ref, str) or ref not in nodes:
                    failures.append(
                        f"{rel}: node {node_id}: {key} references unknown node {ref!r}"
                    )
                else:
                    edges[node_id].add(ref)

        marker = node.get("m2_marker")
        touching = [t for t in clean if intersects_instruction_surface(t)]
        if touching:
            if not isinstance(marker, str) or not marker.startswith(M2_MARKER_PREFIX):
                failures.append(
                    f"{rel}: node {node_id}: write target(s) {touching} intersect the "
                    f"instruction surface but no {M2_MARKER_PREFIX}<path> marker is "
                    "declared (D-GOV-21 M2)"
                )
            else:
                marker_path = marker[len(M2_MARKER_PREFIX):].strip()
                if not is_repo_relative(marker_path):
                    failures.append(
                        f"{rel}: node {node_id}: m2_marker path {marker_path!r} is not "
                        "repo-relative"
                    )
                elif not (root / marker_path).exists():
                    failures.append(
                        f"{rel}: node {node_id}: m2_marker names {marker_path!r}, which "
                        "does not exist (the tranche manifest must exist; the marker "
                        "records a gate and grants nothing — K-AUTH-1)"
                    )

        owner = node.get("owner")
        if isinstance(owner, str) and owner and register is not None:
            if owner not in register:
                failures.append(
                    f"{rel}: node {node_id}: owner {owner!r} has no entry in the G2 "
                    "surface-ownership register"
                )
            else:
                uncovered = [t for t in clean if not covered_by(t, register[owner])]
                if uncovered:
                    failures.append(
                        f"{rel}: node {node_id}: write target(s) {uncovered} are not "
                        f"covered by the register entry for owner {owner!r} "
                        "(undeclared write target, M1)"
                    )

    cycle = find_cycle(edges)
    if cycle:
        failures.append(
            f"{rel}: dependency cycle among nodes {' -> '.join(cycle)}; ordering is "
            "undecided and must be resolved by a recorded move (decompose / invert / "
            "merge / cut) per the AGENTS.md cycle-resolution rule — this guard never "
            "linearizes a cycle"
        )

    active = sorted(nid for nid, node in nodes.items() if node.get("status") == "active")
    for i, a_id in enumerate(active):
        for b_id in active[i + 1:]:
            a_targets = [t for t in (nodes[a_id].get("write_targets") or []) if isinstance(t, str)]
            b_targets = [t for t in (nodes[b_id].get("write_targets") or []) if isinstance(t, str)]
            conflicts = sorted(
                {
                    f"{ta} ~ {tb}"
                    for ta in a_targets
                    for tb in b_targets
                    if targets_overlap(ta, tb)
                }
            )
            if not conflicts:
                continue
            if serialized(nodes, a_id, b_id):
                notes.append(
                    f"{rel}: active nodes {a_id} and {b_id} overlap on {conflicts} and "
                    "are serialized as declared (M1)"
                )
                continue
            failures.append(
                f"{rel}: concurrently active nodes {a_id} and {b_id} have overlapping "
                f"write targets {conflicts} with no declared serialization — M1 "
                "requires disjoint targets, serialization against an accepted "
                "predecessor, or one declared integration owner"
            )

    if data.get("mode") == "governance-only":
        failures.extend(check_governance_graph(root, data, nodes))
        for node in nodes.values():
            node["_governance_mode"] = True
    elif "mode" in data or "governance_state" in data:
        failures.append("unknown or incomplete governance mode")
    else:
        register_data, _, _ = load_yaml_mapping(root / REGISTER_RELPATH)
        if register_data and register_data.get("mode") == "governance-only":
            failures.append("governance ownership requires an explicit governance work graph")

    return failures, notes, nodes


def serialized(nodes: dict[str, dict], a_id: str, b_id: str) -> bool:
    def refs(node_id: str, key: str) -> set[str]:
        value = nodes[node_id].get(key) or []
        if isinstance(value, str):
            value = [value]
        return {v for v in value if isinstance(v, str)}

    for first, second in ((a_id, b_id), (b_id, a_id)):
        if second in refs(first, "serialized_after") or second in refs(first, "depends_on"):
            return True
    owner_a = str(nodes[a_id].get("integration_owner") or "").strip()
    owner_b = str(nodes[b_id].get("integration_owner") or "").strip()
    return bool(owner_a) and owner_a == owner_b


def check_briefs(
    root: Path, nodes: dict[str, dict], brief_paths: list[Path]
) -> tuple[list[str], list[str], int]:
    """Validate run briefs against the accepted graph. Returns (failures, notes, op_code)."""
    failures: list[str] = []
    notes: list[str] = []
    for brief_path in brief_paths:
        if not brief_path.is_file():
            return [], [], 2
        data, error, operational = load_yaml_mapping(brief_path)
        if operational:
            return [], [], 2
        if error is not None or data is None:
            failures.append(f"brief {brief_path.name}: {error}")
            continue

        node_id = data.get("node")
        if not isinstance(node_id, str) or node_id not in nodes:
            failures.append(
                f"brief {brief_path.name}: node {node_id!r} is not a node of the "
                "accepted work graph"
            )
            continue
        node = nodes[node_id]
        if node.get("status") != "active":
            failures.append(
                f"brief {brief_path.name}: node {node_id} has status "
                f"{node.get('status')!r}; only 'active' nodes may be dispatched"
            )

        declared = [
            t for t in (node.get("write_targets") or []) if isinstance(t, str) and t
        ]
        brief_targets = data.get("write_targets")
        if (
            not isinstance(brief_targets, list)
            or not brief_targets
            or not all(isinstance(t, str) and t for t in brief_targets)
        ):
            failures.append(
                f"brief {brief_path.name}: write_targets must be a non-empty list of "
                "strings (M1: every dispatched node declares its write targets)"
            )
            continue

        if node.get("_governance_mode"):
            from root_governance_state import GovernanceError
            from validate_root_surface_ownership import canonical_covered
            try:
                for target in brief_targets:
                    if not canonical_covered(root, target, declared):
                        raise GovernanceError("brief target outside canonical node scope")
                for key in ("session_id", "parent_session_id", "stage", "child_evidence"):
                    if data.get(key) != node.get(key):
                        raise GovernanceError(f"brief {key} differs from execution-bound node")
            except (GovernanceError, TypeError, ValueError, OSError) as exc:
                failures.append(f"brief {brief_path.name}: {exc}")

        for target in brief_targets:
            if not is_repo_relative(target):
                failures.append(
                    f"brief {brief_path.name}: write target {target!r} is not a "
                    "repo-relative POSIX path"
                )
            elif not covered_by(target, declared):
                failures.append(
                    f"brief {brief_path.name}: undeclared write target {target!r} — "
                    f"not covered by node {node_id}'s declared targets {declared}"
                )

        touching = [t for t in brief_targets if intersects_instruction_surface(t)]
        marker = data.get("m2_marker")
        if touching:
            if not isinstance(marker, str) or not marker.startswith(M2_MARKER_PREFIX):
                failures.append(
                    f"brief {brief_path.name}: write target(s) {touching} intersect the "
                    f"instruction surface but no {M2_MARKER_PREFIX}<path> marker is "
                    "declared (D-GOV-21 M2)"
                )
            else:
                marker_path = marker[len(M2_MARKER_PREFIX):].strip()
                if not is_repo_relative(marker_path) or not (root / marker_path).exists():
                    failures.append(
                        f"brief {brief_path.name}: m2_marker names {marker_path!r}, "
                        "which is not a repo-relative existing path"
                    )
                elif marker != node.get("m2_marker"):
                    failures.append(
                        f"brief {brief_path.name}: m2_marker {marker!r} does not match "
                        f"node {node_id}'s declared marker {node.get('m2_marker')!r}"
                    )
        notes.append(f"brief {brief_path.name}: dispatch of node {node_id} checked")
    return failures, notes, 0


def check(
    root: Path,
    graph_path: Path | None = None,
    brief_paths: list[Path] | None = None,
) -> tuple[int, list[str]]:
    """Returns (exit_code, report_lines). 0 PASS, 1 BLOCK, 2 operational."""
    lines: list[str] = []
    dispatch = brief_paths is not None
    path = graph_path if graph_path is not None else root / WORK_GRAPH_RELPATH

    if not path.is_file():
        if dispatch:
            lines.append(
                f"G3 OPERATIONAL (exit 2): named work graph {path.name} does not exist; "
                "dispatch mode cannot check an absent graph."
            )
            return 2, lines
        register_data, _, _ = load_yaml_mapping(root / REGISTER_RELPATH)
        if register_data and register_data.get("mode") == "governance-only":
            return 1, ["G3 BLOCK: governance ownership requires a work graph"]
        lines.append(
            f"G3 PASS: work-graph surface {WORK_GRAPH_RELPATH.as_posix()} absent; "
            "guard idle (pre-instantiation condition — Project Setup instantiates "
            "the first accepted work graph)."
        )
        return 0, lines

    data, error, operational = load_yaml_mapping(path)
    if operational:
        lines.append(f"G3 OPERATIONAL (exit 2): {error}; this guard asserts nothing.")
        return 2, lines
    if data is None:
        lines.append(f"G3 BLOCK: {error}")
        return 1, lines

    failures, notes, nodes = check_graph(root, path, data)

    if dispatch:
        brief_failures, brief_notes, op_code = check_briefs(root, nodes, brief_paths or [])
        if op_code == 2:
            lines.append(
                "G3 OPERATIONAL (exit 2): a named run brief is missing or unreadable, "
                "or PyYAML is unavailable; this guard asserts nothing."
            )
            return 2, lines
        failures.extend(brief_failures)
        notes.extend(brief_notes)

    mode = "dispatch" if dispatch else "CI"
    if failures:
        lines.append(f"G3 BLOCK ({mode} mode): work graph {path.name} failed:")
        lines.extend(f"  - {failure}" for failure in failures)
        lines.extend(f"  INFO: {note}" for note in notes)
        return 1, lines

    active = sorted(nid for nid, node in nodes.items() if node.get("status") == "active")
    lines.append(
        f"G3 PASS ({mode} mode): work graph {path.name} is schema-valid "
        f"({WORK_GRAPH_SCHEMA}); {len(nodes)} node(s), active: {active or 'none'}; "
        "declared write targets, disjointness/serialization, and M2 markers check out."
    )
    lines.extend(f"  INFO: {note}" for note in notes)
    return 0, lines


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "G3 pre-dispatch root work-graph check (D-GOV-21 §5.3). No arguments: "
            "CI mode against the default work-graph surface. With --work-graph and "
            "--brief: dispatch mode."
        )
    )
    parser.add_argument(
        "--work-graph",
        help="Repo-relative or absolute path to the accepted work graph (dispatch mode).",
    )
    parser.add_argument(
        "--brief",
        action="append",
        default=[],
        help="Path to a run brief being dispatched; repeatable (dispatch mode).",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if bool(args.work_graph) != bool(args.brief):
        print(
            "G3 OPERATIONAL (exit 2): dispatch mode requires both --work-graph and at "
            "least one --brief; supply neither for CI mode."
        )
        return 2
    root = repo_root()

    graph_path = None
    briefs = None
    if args.work_graph:
        graph_path = Path(args.work_graph)
        if not graph_path.is_absolute():
            graph_path = root / graph_path
        briefs = []
        for raw in args.brief:
            brief_path = Path(raw)
            if not brief_path.is_absolute():
                brief_path = root / brief_path
            briefs.append(brief_path)

    code, lines = check(root, graph_path, briefs)
    for line in lines:
        print(line)
    return code


if __name__ == "__main__":
    sys.exit(main())
