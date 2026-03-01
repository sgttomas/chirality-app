#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import dataclasses
import datetime as dt
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, DefaultDict, Iterable, Literal


REQUIRED_COLUMNS_V31 = [
    "RegisterSchemaVersion",
    "DependencyID",
    "FromPackageID",
    "FromDeliverableID",
    "FromDeliverableName",
    "DependencyClass",
    "AnchorType",
    "Direction",
    "DependencyType",
    "TargetType",
    "TargetPackageID",
    "TargetDeliverableID",
    "TargetRefID",
    "TargetName",
    "TargetLocation",
    "Statement",
    "EvidenceFile",
    "SourceRef",
    "EvidenceQuote",
    "Explicitness",
    "RequiredMaturity",
    "ProposedMaturity",
    "SatisfactionStatus",
    "Confidence",
    "Origin",
    "FirstSeen",
    "LastSeen",
    "Status",
    "Notes",
]


def _clean(s: Any) -> str:
    return str(s or "").strip()


_DEL_ID_RE = re.compile(r"^(DEL-\d{3}-\d{2})(?:_.*)?$")
_PKG_ID_RE = re.compile(r"^(PKG-\d{3})(?:_.*)?$")


def normalize_entity_id(raw_id: str) -> str:
    raw = _clean(raw_id)
    if not raw:
        return ""
    if "_" in raw:
        return raw.split("_", 1)[0].strip()
    return raw


def normalize_deliverable_id(raw_id: str) -> str:
    raw = _clean(raw_id)
    if not raw:
        return ""
    match = _DEL_ID_RE.match(raw)
    if match:
        return match.group(1)
    # Fallback: strip suffix after first underscore.
    return normalize_entity_id(raw)


def normalize_package_id(raw_id: str) -> str:
    raw = _clean(raw_id)
    if not raw:
        return ""
    match = _PKG_ID_RE.match(raw)
    if match:
        return match.group(1)
    return normalize_entity_id(raw)


@dataclasses.dataclass(frozen=True)
class Deliverable:
    deliverable_id: str
    package_id: str
    path: Path


@dataclasses.dataclass(frozen=True)
class Edge:
    src: str
    dst: str
    from_id: str
    target_id: str
    direction: str
    dependency_id: str
    dependency_type: str
    estimate_impact_class: str
    evidence: str
    evidence_file: str
    row_number: int
    csv_path: str
    ambiguous_direction: bool


@dataclasses.dataclass(frozen=True)
class Issue:
    issue_id: str
    severity: Literal["BLOCKER", "WARNING", "INFO"]
    check: str
    from_id: str
    target_id: str
    dependency_id: str
    evidence: str
    fix_suggestion: str


def discover_deliverables(execution_root: Path) -> list[Deliverable]:
    deliverables: list[Deliverable] = []
    for pkg_dir in sorted(execution_root.glob("PKG-*")):
        if not pkg_dir.is_dir():
            continue
        pkg_id = normalize_package_id(pkg_dir.name)
        working_dir = pkg_dir / "1_Working"
        if not working_dir.is_dir():
            continue
        for del_dir in sorted(working_dir.iterdir()):
            if not del_dir.is_dir():
                continue
            if not del_dir.name.startswith("DEL-"):
                continue
            del_id = normalize_deliverable_id(del_dir.name)
            if not del_id:
                continue
            deliverables.append(Deliverable(deliverable_id=del_id, package_id=pkg_id, path=del_dir))
    return deliverables


def _read_csv_rows(csv_path: Path) -> tuple[list[str], list[dict[str, str]], str | None]:
    try:
        with csv_path.open("r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if reader.fieldnames is None:
                return [], [], "NO_HEADER"
            fieldnames = [name.strip() for name in reader.fieldnames]
            rows = []
            for row in reader:
                rows.append({k.strip(): _clean(v) for k, v in row.items()})
            return fieldnames, rows, None
    except UnicodeDecodeError:
        # Try a permissive fallback encoding.
        try:
            with csv_path.open("r", newline="", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                if reader.fieldnames is None:
                    return [], [], "NO_HEADER"
                fieldnames = [name.strip() for name in reader.fieldnames]
                rows = []
                for row in reader:
                    rows.append({k.strip(): _clean(v) for k, v in row.items()})
                return fieldnames, rows, None
        except Exception as e:  # noqa: BLE001 - report as UNREADABLE
            return [], [], f"UNREADABLE: {type(e).__name__}: {e}"
    except Exception as e:  # noqa: BLE001 - report as UNREADABLE
        return [], [], f"UNREADABLE: {type(e).__name__}: {e}"


def validate_schema_v31(fieldnames: list[str]) -> tuple[bool, list[str]]:
    field_set = set(fieldnames)
    missing = [c for c in REQUIRED_COLUMNS_V31 if c not in field_set]
    return len(missing) == 0, missing


def classify_direction(direction_raw: str) -> tuple[Literal["UPSTREAM", "DOWNSTREAM", "UNKNOWN"], bool]:
    d = _clean(direction_raw).upper()
    if d in {"UPSTREAM", "INBOUND"}:
        return "UPSTREAM", False
    if d in {"DOWNSTREAM", "OUTBOUND"}:
        return "DOWNSTREAM", False
    if d:
        return "UNKNOWN", True
    return "UNKNOWN", True


def build_edges(
    *,
    deliverable: Deliverable,
    csv_path: Path,
    fieldnames: list[str],
    rows: list[dict[str, str]],
    filter_active_only: bool,
    normalize_ids: bool,
    issues: list[Issue],
    misplaced_rows: list[dict[str, str]],
    id_normalization_events: list[dict[str, str]],
) -> tuple[list[Edge], dict[str, Any]]:
    """
    Returns:
      - edges extracted from this Dependencies.csv under the default edge filter
      - per-deliverable stats used by reporting (anchors, totals, etc.)
    """
    stats: dict[str, Any] = {
        "row_count": len(rows),
        "active_anchor_implements_node": 0,
        "active_execution_to_deliverable": 0,
        "unknown_direction_rows": 0,
        "from_id_mismatch_rows": 0,
    }

    edges: list[Edge] = []
    for idx, row in enumerate(rows, start=2):  # data rows start after header
        status = _clean(row.get("Status", "")).upper()
        dep_class = _clean(row.get("DependencyClass", "")).upper()
        anchor_type = _clean(row.get("AnchorType", "")).upper()
        target_type = _clean(row.get("TargetType", "")).upper()
        direction_raw = row.get("Direction", "")
        dependency_id = _clean(row.get("DependencyID", ""))

        from_id_raw = row.get("FromDeliverableID", "")
        target_id_raw = row.get("TargetDeliverableID", "")

        from_id_norm = normalize_deliverable_id(from_id_raw) if normalize_ids else _clean(from_id_raw)
        target_id_norm = normalize_deliverable_id(target_id_raw) if normalize_ids else _clean(target_id_raw)

        if normalize_ids:
            if from_id_raw and from_id_norm and from_id_raw != from_id_norm:
                id_normalization_events.append(
                    {
                        "DeliverableID": deliverable.deliverable_id,
                        "CSV": str(csv_path),
                        "Row": str(idx),
                        "Field": "FromDeliverableID",
                        "Raw": from_id_raw,
                        "Normalized": from_id_norm,
                    }
                )
            if target_id_raw and target_id_norm and target_id_raw != target_id_norm:
                id_normalization_events.append(
                    {
                        "DeliverableID": deliverable.deliverable_id,
                        "CSV": str(csv_path),
                        "Row": str(idx),
                        "Field": "TargetDeliverableID",
                        "Raw": target_id_raw,
                        "Normalized": target_id_norm,
                    }
                )

        if status == "ACTIVE" and dep_class == "ANCHOR" and anchor_type == "IMPLEMENTS_NODE":
            stats["active_anchor_implements_node"] += 1

        if _clean(row.get("TargetDeliverableID", "")) and target_type and target_type != "DELIVERABLE":
            misplaced_rows.append(
                {
                    "DeliverableID": deliverable.deliverable_id,
                    "DependencyID": dependency_id,
                    "Row": str(idx),
                    "TargetType": target_type,
                    "TargetDeliverableID": _clean(row.get("TargetDeliverableID", "")),
                    "CSV": str(csv_path),
                }
            )

        if filter_active_only and status != "ACTIVE":
            continue
        if dep_class != "EXECUTION":
            continue
        if target_type != "DELIVERABLE":
            continue
        if not from_id_norm or not target_id_norm:
            continue

        if from_id_norm != deliverable.deliverable_id:
            stats["from_id_mismatch_rows"] += 1
            issues.append(
                Issue(
                    issue_id=f"FROM_ID_MISMATCH::{deliverable.deliverable_id}::{dependency_id}",
                    severity="WARNING",
                    check="ID format consistency",
                    from_id=from_id_norm,
                    target_id=target_id_norm,
                    dependency_id=dependency_id,
                    evidence=f"{csv_path}:{idx} (DependencyID={dependency_id})",
                    fix_suggestion="Set FromDeliverableID to the owning deliverable’s ID.",
                )
            )

        direction_class, ambiguous = classify_direction(direction_raw)
        if ambiguous:
            stats["unknown_direction_rows"] += 1

        dependency_type = _clean(row.get("DependencyType", "")).upper()
        estimate_impact_class = _clean(row.get("EstimateImpactClass", "")).upper()
        evidence_file = _clean(row.get("EvidenceFile", ""))
        evidence = f"{csv_path}:{idx} (DependencyID={dependency_id})"

        if direction_class == "UPSTREAM":
            src, dst = target_id_norm, from_id_norm
        elif direction_class == "DOWNSTREAM":
            src, dst = from_id_norm, target_id_norm
        else:
            # Unknown direction: keep nominal orientation but flag as ambiguous; SCC detection
            # will treat as undirected (A<->B).
            src, dst = from_id_norm, target_id_norm

        stats["active_execution_to_deliverable"] += 1
        edges.append(
            Edge(
                src=src,
                dst=dst,
                from_id=from_id_norm,
                target_id=target_id_norm,
                direction=direction_class,
                dependency_id=dependency_id,
                dependency_type=dependency_type,
                estimate_impact_class=estimate_impact_class,
                evidence=evidence,
                evidence_file=evidence_file,
                row_number=idx,
                csv_path=str(csv_path),
                ambiguous_direction=ambiguous,
            )
        )

    return edges, stats


def tarjan_scc(nodes: Iterable[str], adjacency: dict[str, list[str]]) -> list[list[str]]:
    index = 0
    index_map: dict[str, int] = {}
    lowlink: dict[str, int] = {}
    stack: list[str] = []
    on_stack: set[str] = set()
    sccs: list[list[str]] = []

    sys.setrecursionlimit(10000)

    def strongconnect(v: str) -> None:
        nonlocal index
        index_map[v] = index
        lowlink[v] = index
        index += 1
        stack.append(v)
        on_stack.add(v)

        for w in adjacency.get(v, []):
            if w not in index_map:
                strongconnect(w)
                lowlink[v] = min(lowlink[v], lowlink[w])
            elif w in on_stack:
                lowlink[v] = min(lowlink[v], index_map[w])

        if lowlink[v] == index_map[v]:
            scc: list[str] = []
            while True:
                w = stack.pop()
                on_stack.remove(w)
                scc.append(w)
                if w == v:
                    break
            sccs.append(sorted(scc))

    for v in sorted(set(nodes)):
        if v not in index_map:
            strongconnect(v)

    # Sort SCCs deterministically: by size desc then by first node id.
    return sorted(sccs, key=lambda s: (-len(s), s[0] if s else ""))


def find_representative_cycle(nodes: set[str], adjacency: dict[str, list[str]]) -> list[str] | None:
    color: dict[str, int] = {n: 0 for n in nodes}  # 0 unvisited, 1 visiting, 2 done
    stack: list[str] = []

    def dfs(u: str) -> list[str] | None:
        color[u] = 1
        stack.append(u)
        for v in sorted(adjacency.get(u, [])):
            if v not in nodes:
                continue
            if color[v] == 0:
                cyc = dfs(v)
                if cyc:
                    return cyc
            elif color[v] == 1:
                # back edge found; extract cycle from the stack
                try:
                    idx = stack.index(v)
                except ValueError:
                    idx = 0
                return stack[idx:] + [v]
        stack.pop()
        color[u] = 2
        return None

    for start in sorted(nodes):
        if color[start] == 0:
            cyc = dfs(start)
            if cyc:
                return cyc
    return None


def _write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in fieldnames})


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="AUDIT_DEP_CLOSURE — cross-deliverable dependency closure analysis")
    parser.add_argument("--execution-root", default=".", help="Execution root (repo-relative or absolute)")
    parser.add_argument("--scope", default="ALL", help="Scope selector (ALL only supported by this script)")
    parser.add_argument("--run-label", default="AUDIT_DEP_CLOSURE", help="Run label")
    parser.add_argument("--requested-by", default="USER", help="Invoking agent/name")
    parser.add_argument("--filter-active-only", default="true", choices=["true", "false"])
    parser.add_argument("--normalize-ids", default="true", choices=["true", "false"])
    parser.add_argument("--hub-threshold", type=int, default=20)
    parser.add_argument("--max-cycles", type=int, default=10000)
    parser.add_argument("--output-dir", required=True, help="Snapshot output directory")
    parser.add_argument(
        "--brief-verbatim",
        default="Run AUDIT_DEP_CLOSURE",
        help="Verbatim brief text to embed in Brief.md",
    )
    args = parser.parse_args()

    execution_root = Path(args.execution_root).resolve()
    output_dir = Path(args.output_dir).resolve()
    evidence_dir = output_dir / "Evidence"
    evidence_dir.mkdir(parents=True, exist_ok=True)

    filter_active_only = args.filter_active_only.lower() == "true"
    normalize_ids = args.normalize_ids.lower() == "true"

    if args.scope != "ALL":
        _write_text(
            output_dir / "RUN_SUMMARY.md",
            "RUN_STATUS = FAILED_INPUTS\n\nReason: This script currently supports `--scope ALL` only.\n",
        )
        return 2

    deliverables = discover_deliverables(execution_root)
    if not deliverables:
        _write_text(
            output_dir / "RUN_SUMMARY.md",
            "RUN_STATUS = FAILED_INPUTS\n\nReason: No deliverables discovered under execution root.\n",
        )
        return 2

    deliverable_ids = [d.deliverable_id for d in deliverables]
    deliverable_id_set = set(deliverable_ids)

    duplicate_ids = sorted({d for d in deliverable_ids if deliverable_ids.count(d) > 1})

    issues: list[Issue] = []
    misplaced_rows: list[dict[str, str]] = []
    id_normalization_events: list[dict[str, str]] = []

    coverage_rows: list[dict[str, str]] = []
    edges_all: list[Edge] = []
    anchors_missing: list[str] = []
    schema_invalid_details: list[dict[str, str]] = []
    unreadable_details: list[dict[str, str]] = []

    for deliverable in deliverables:
        dep_csv = deliverable.path / "Dependencies.csv"
        if not dep_csv.exists():
            coverage_rows.append(
                {
                    "DeliverableID": deliverable.deliverable_id,
                    "PackageID": deliverable.package_id,
                    "Path": str(deliverable.path),
                    "DependenciesCsv": str(dep_csv),
                    "CoverageStatus": "MISSING_DEPENDENCIES_CSV",
                    "RowCount": "0",
                    "ActiveAnchorImplementsNode": "",
                    "ActiveExecutionToDeliverableRows": "",
                    "UnknownDirectionRows": "",
                }
            )
            anchors_missing.append(deliverable.deliverable_id)
            continue

        fieldnames, rows, error = _read_csv_rows(dep_csv)
        if error:
            coverage_rows.append(
                {
                    "DeliverableID": deliverable.deliverable_id,
                    "PackageID": deliverable.package_id,
                    "Path": str(deliverable.path),
                    "DependenciesCsv": str(dep_csv),
                    "CoverageStatus": "UNREADABLE",
                    "RowCount": "0",
                    "ActiveAnchorImplementsNode": "",
                    "ActiveExecutionToDeliverableRows": "",
                    "UnknownDirectionRows": "",
                }
            )
            unreadable_details.append(
                {
                    "DeliverableID": deliverable.deliverable_id,
                    "DependenciesCsv": str(dep_csv),
                    "Error": error,
                }
            )
            anchors_missing.append(deliverable.deliverable_id)
            continue

        ok_schema, missing_cols = validate_schema_v31(fieldnames)
        if not ok_schema:
            coverage_rows.append(
                {
                    "DeliverableID": deliverable.deliverable_id,
                    "PackageID": deliverable.package_id,
                    "Path": str(deliverable.path),
                    "DependenciesCsv": str(dep_csv),
                    "CoverageStatus": "SCHEMA_INVALID",
                    "RowCount": str(len(rows)),
                    "ActiveAnchorImplementsNode": "",
                    "ActiveExecutionToDeliverableRows": "",
                    "UnknownDirectionRows": "",
                }
            )
            schema_invalid_details.append(
                {
                    "DeliverableID": deliverable.deliverable_id,
                    "DependenciesCsv": str(dep_csv),
                    "MissingColumns": ";".join(missing_cols),
                }
            )
            anchors_missing.append(deliverable.deliverable_id)
            continue

        edges, stats = build_edges(
            deliverable=deliverable,
            csv_path=dep_csv,
            fieldnames=fieldnames,
            rows=rows,
            filter_active_only=filter_active_only,
            normalize_ids=normalize_ids,
            issues=issues,
            misplaced_rows=misplaced_rows,
            id_normalization_events=id_normalization_events,
        )
        edges_all.extend(edges)

        if stats["active_anchor_implements_node"] == 0:
            anchors_missing.append(deliverable.deliverable_id)

        coverage_rows.append(
            {
                "DeliverableID": deliverable.deliverable_id,
                "PackageID": deliverable.package_id,
                "Path": str(deliverable.path),
                "DependenciesCsv": str(dep_csv),
                "CoverageStatus": "OK",
                "RowCount": str(stats["row_count"]),
                "ActiveAnchorImplementsNode": str(stats["active_anchor_implements_node"]),
                "ActiveExecutionToDeliverableRows": str(stats["active_execution_to_deliverable"]),
                "UnknownDirectionRows": str(stats["unknown_direction_rows"]),
            }
        )

    # Evidence: coverage + schema/unreadable details + misplaced + id normalization events
    _write_csv(
        evidence_dir / "coverage.csv",
        coverage_rows,
        [
            "DeliverableID",
            "PackageID",
            "Path",
            "DependenciesCsv",
            "CoverageStatus",
            "RowCount",
            "ActiveAnchorImplementsNode",
            "ActiveExecutionToDeliverableRows",
            "UnknownDirectionRows",
        ],
    )
    if schema_invalid_details:
        _write_csv(
            evidence_dir / "schema_invalid.csv",
            schema_invalid_details,
            ["DeliverableID", "DependenciesCsv", "MissingColumns"],
        )
    if unreadable_details:
        _write_csv(evidence_dir / "unreadable.csv", unreadable_details, ["DeliverableID", "DependenciesCsv", "Error"])
    if misplaced_rows:
        _write_csv(
            evidence_dir / "misplaced_fields.csv",
            misplaced_rows,
            ["DeliverableID", "DependencyID", "Row", "TargetType", "TargetDeliverableID", "CSV"],
        )
    if id_normalization_events:
        _write_csv(
            evidence_dir / "id_normalization.csv",
            id_normalization_events,
            ["DeliverableID", "CSV", "Row", "Field", "Raw", "Normalized"],
        )

    # Orphans (based on TargetDeliverableID referenced in the row)
    orphans_rows: list[dict[str, str]] = []
    internal_edges: list[Edge] = []
    ambiguous_edges_internal: list[Edge] = []

    for edge in sorted(edges_all, key=lambda e: (e.from_id, e.target_id, e.dependency_id, e.csv_path, e.row_number)):
        if edge.target_id not in deliverable_id_set:
            orphans_rows.append(
                {
                    "FromDeliverableID": edge.from_id,
                    "TargetDeliverableID": edge.target_id,
                    "DependencyID": edge.dependency_id,
                    "Direction": edge.direction,
                    "Evidence": edge.evidence,
                }
            )
            issues.append(
                Issue(
                    issue_id=f"ORPHAN::{edge.from_id}::{edge.target_id}::{edge.dependency_id}",
                    severity="BLOCKER",
                    check="Orphan dependencies",
                    from_id=edge.from_id,
                    target_id=edge.target_id,
                    dependency_id=edge.dependency_id,
                    evidence=edge.evidence,
                    fix_suggestion="Update TargetDeliverableID to an existing DEL-XXX-YY in scope, or set TargetType=PACKAGE if referencing a package.",
                )
            )
            continue

        if edge.src in deliverable_id_set and edge.dst in deliverable_id_set:
            internal_edges.append(edge)
            if edge.ambiguous_direction or edge.direction == "UNKNOWN":
                ambiguous_edges_internal.append(edge)

    if orphans_rows:
        _write_csv(
            evidence_dir / "orphans.csv",
            orphans_rows,
            ["FromDeliverableID", "TargetDeliverableID", "DependencyID", "Direction", "Evidence"],
        )

    # Graph build: adjacency (definite directed) + adjacency_scc (direction-unknown treated as undirected)
    adjacency: DefaultDict[str, set[str]] = defaultdict(set)
    adjacency_scc: DefaultDict[str, set[str]] = defaultdict(set)
    indegree: DefaultDict[str, int] = defaultdict(int)
    outdegree: DefaultDict[str, int] = defaultdict(int)

    definite_internal_edges = [e for e in internal_edges if not (e.ambiguous_direction or e.direction == "UNKNOWN")]

    for e in definite_internal_edges:
        adjacency[e.src].add(e.dst)
        adjacency_scc[e.src].add(e.dst)

    for e in ambiguous_edges_internal:
        # Undirected for SCC membership only: add both ways.
        adjacency_scc[e.src].add(e.dst)
        adjacency_scc[e.dst].add(e.src)

    for node in deliverable_ids:
        # ensure keys exist for deterministic ordering
        _ = adjacency.get(node, set())
        _ = adjacency_scc.get(node, set())

    adjacency_list = {k: sorted(v) for k, v in adjacency.items()}
    adjacency_scc_list = {k: sorted(v) for k, v in adjacency_scc.items()}

    for src, dsts in adjacency_list.items():
        for dst in dsts:
            outdegree[src] += 1
            indegree[dst] += 1

    for node in deliverable_ids:
        indegree.setdefault(node, 0)
        outdegree.setdefault(node, 0)

    # SCC / cycles
    sccs = tarjan_scc(deliverable_ids, adjacency_scc_list)
    cyclic_sccs = [s for s in sccs if len(s) > 1]

    scc_summary_rows: list[dict[str, str]] = []
    cycles_sample_rows: list[dict[str, str]] = []

    def _edge_evidence_between(a: str, b: str) -> str | None:
        candidates = [e for e in internal_edges if e.src == a and e.dst == b]
        if not candidates:
            return None
        chosen = sorted(candidates, key=lambda e: (e.ambiguous_direction, e.dependency_id, e.csv_path, e.row_number))[0]
        return chosen.evidence

    for scc_idx, scc in enumerate(cyclic_sccs, start=1):
        nodes_set = set(scc)
        cyc = find_representative_cycle(nodes_set, adjacency_scc_list)
        cycle_str = ""
        cycle_evidence = ""
        if cyc:
            cycle_str = " -> ".join(cyc)
            ev_parts: list[str] = []
            for a, b in zip(cyc, cyc[1:], strict=False):
                ev = _edge_evidence_between(a, b)
                if ev:
                    ev_parts.append(ev)
            cycle_evidence = "; ".join(ev_parts)
            cycles_sample_rows.append(
                {
                    "SCC_ID": f"SCC-{scc_idx:03d}",
                    "CycleIndex": "1",
                    "CycleNodes": cycle_str,
                    "EdgeEvidence": cycle_evidence,
                    "ContainsAmbiguousDirectionEdges": "true" if ambiguous_edges_internal else "false",
                }
            )
        issues.append(
            Issue(
                issue_id=f"CYCLE::SCC-{scc_idx:03d}",
                severity="WARNING",
                check="Circular dependencies",
                from_id=scc[0] if scc else "",
                target_id=scc[1] if len(scc) > 1 else "",
                dependency_id="",
                evidence=cycle_evidence
                or (f"SCC-{scc_idx:03d} contains a cycle; see Evidence/scc_summary.csv and Evidence/cycles_sample.csv"),
                fix_suggestion="Review EXECUTION edges within the SCC; adjust Direction/DependencyType (or reclassify as non-precedence) to break the cycle, or accept as an iterative bundle for tiering/scheduling.",
            )
        )

        scc_summary_rows.append(
            {
                "SCC_ID": f"SCC-{scc_idx:03d}",
                "Size": str(len(scc)),
                "Nodes": ";".join(scc),
                "RepresentativeCycle": cycle_str,
            }
        )

    if scc_summary_rows:
        _write_csv(evidence_dir / "scc_summary.csv", scc_summary_rows, ["SCC_ID", "Size", "Nodes", "RepresentativeCycle"])
    if cycles_sample_rows:
        _write_csv(
            evidence_dir / "cycles_sample.csv",
            cycles_sample_rows,
            ["SCC_ID", "CycleIndex", "CycleNodes", "EdgeEvidence", "ContainsAmbiguousDirectionEdges"],
        )

    # Isolated nodes (no internal definite EXECUTION edges)
    isolated = sorted([n for n in deliverable_ids if indegree[n] + outdegree[n] == 0])
    isolated_rows = [{"DeliverableID": d} for d in isolated]
    if isolated_rows:
        _write_csv(evidence_dir / "isolated_deliverables.csv", isolated_rows, ["DeliverableID"])
        for d in isolated:
            issues.append(
                Issue(
                    issue_id=f"ISOLATED::{d}",
                    severity="WARNING",
                    check="Isolated deliverables",
                    from_id=d,
                    target_id="",
                    dependency_id="",
                    evidence="No in-scope EXECUTION edges after filters.",
                    fix_suggestion="Rerun DEPENDENCIES for this deliverable and/or add declared upstream/downstream dependencies as appropriate.",
                )
            )

    # Hub analysis (degree >= threshold)
    hubs_rows: list[dict[str, str]] = []
    for node in deliverable_ids:
        degree = indegree[node] + outdegree[node]
        if degree >= args.hub_threshold:
            hubs_rows.append(
                {
                    "DeliverableID": node,
                    "InDegree": str(indegree[node]),
                    "OutDegree": str(outdegree[node]),
                    "TotalDegree": str(degree),
                }
            )
    if hubs_rows:
        hubs_rows = sorted(hubs_rows, key=lambda r: (-int(r["TotalDegree"]), r["DeliverableID"]))
        _write_csv(evidence_dir / "hubs.csv", hubs_rows, ["DeliverableID", "InDegree", "OutDegree", "TotalDegree"])

    # Bidirectional pairs (definite directed only)
    edge_set = {(e.src, e.dst) for e in definite_internal_edges}
    bidirectional_pairs: set[tuple[str, str]] = set()
    for a, b in edge_set:
        if (b, a) in edge_set:
            pair = tuple(sorted((a, b)))
            bidirectional_pairs.add(pair)
    bidirectional_rows = [{"A": a, "B": b} for a, b in sorted(bidirectional_pairs)]
    if bidirectional_rows:
        _write_csv(evidence_dir / "bidirectional_pairs.csv", bidirectional_rows, ["A", "B"])

    # Anchor coverage issues
    anchors_missing_sorted = sorted(set(anchors_missing))
    if anchors_missing_sorted:
        _write_csv(
            evidence_dir / "anchors_missing.csv",
            [{"DeliverableID": d} for d in anchors_missing_sorted],
            ["DeliverableID"],
        )
        for d in anchors_missing_sorted:
            issues.append(
                Issue(
                    issue_id=f"ANCHOR_MISSING::{d}",
                    severity="WARNING",
                    check="Anchor coverage",
                    from_id=d,
                    target_id="",
                    dependency_id="",
                    evidence="No ACTIVE ANCHOR row with AnchorType=IMPLEMENTS_NODE (or dependencies file missing/invalid).",
                    fix_suggestion="Ensure Dependencies.csv includes an ACTIVE ANCHOR row with AnchorType=IMPLEMENTS_NODE (DEPENDENCIES agent Function 5).",
                )
            )

    # Misplaced fields issues
    for m in misplaced_rows:
        issues.append(
            Issue(
                issue_id=f"MISPLACED::{m.get('DeliverableID','')}::{m.get('DependencyID','')}",
                severity="WARNING",
                check="Misplaced fields",
                from_id=m.get("DeliverableID", ""),
                target_id=m.get("TargetDeliverableID", ""),
                dependency_id=m.get("DependencyID", ""),
                evidence=f"{m.get('CSV','')}:{m.get('Row','')}",
                fix_suggestion="Clear TargetDeliverableID when TargetType is not DELIVERABLE, or correct TargetType to DELIVERABLE.",
            )
        )

    # Duplicate deliverable IDs (structural)
    if duplicate_ids:
        for d in duplicate_ids:
            issues.append(
                Issue(
                    issue_id=f"DUPLICATE_DELIVERABLE_ID::{d}",
                    severity="BLOCKER",
                    check="Schema compliance",
                    from_id=d,
                    target_id="",
                    dependency_id="",
                    evidence="Multiple deliverable folders discovered with the same ID.",
                    fix_suggestion="Ensure deliverable folder names have unique DEL-XXX-YY IDs; rename duplicates.",
                )
            )

    # Verdicts per core check
    total_deliverables = len(deliverables)
    ok_count = sum(1 for r in coverage_rows if r["CoverageStatus"] == "OK")
    missing_count = sum(1 for r in coverage_rows if r["CoverageStatus"] == "MISSING_DEPENDENCIES_CSV")
    unreadable_count = sum(1 for r in coverage_rows if r["CoverageStatus"] == "UNREADABLE")
    schema_invalid_count = sum(1 for r in coverage_rows if r["CoverageStatus"] == "SCHEMA_INVALID")

    def verdict_for_schema() -> str:
        if missing_count == 0 and unreadable_count == 0 and schema_invalid_count == 0:
            return "PASS"
        if ok_count == 0:
            return "BLOCKER"
        return "WARNING"

    def verdict_for_count(count: int, blocker_if_any: bool = False) -> str:
        if count == 0:
            return "PASS"
        return "BLOCKER" if blocker_if_any else "WARNING"

    schema_verdict = verdict_for_schema()
    orphan_verdict = verdict_for_count(len(orphans_rows), blocker_if_any=True)
    cycle_verdict = verdict_for_count(len(cyclic_sccs), blocker_if_any=False)
    anchor_verdict = verdict_for_count(len(anchors_missing_sorted), blocker_if_any=False)
    misplaced_verdict = verdict_for_count(len(misplaced_rows), blocker_if_any=False)
    id_norm_verdict = "INFO" if id_normalization_events else "PASS"
    isolated_verdict = verdict_for_count(len(isolated), blocker_if_any=False)
    hub_verdict = "INFO" if hubs_rows else "PASS"
    bidi_verdict = "INFO" if bidirectional_rows else "PASS"

    overall = "PASS"
    if "BLOCKER" in {schema_verdict, orphan_verdict}:
        overall = "BLOCKER"
    elif any(v in {"WARNING"} for v in [schema_verdict, cycle_verdict, anchor_verdict, misplaced_verdict, isolated_verdict]):
        overall = "WARNING"

    run_status = "OK" if overall == "PASS" else "WARNINGS"

    # Issue log CSV
    issues_sorted = sorted(issues, key=lambda i: ({"BLOCKER": 0, "WARNING": 1, "INFO": 2}[i.severity], i.issue_id))
    issue_rows = [
        {
            "ID": i.issue_id,
            "Severity": i.severity,
            "Check": i.check,
            "FromDeliverableID": i.from_id,
            "TargetDeliverableID": i.target_id,
            "DependencyID": i.dependency_id,
            "Evidence": i.evidence,
            "FixSuggestion": i.fix_suggestion,
        }
        for i in issues_sorted
    ]
    _write_csv(
        output_dir / "Dependency_Closure_IssueLog.csv",
        issue_rows,
        ["ID", "Severity", "Check", "FromDeliverableID", "TargetDeliverableID", "DependencyID", "Evidence", "FixSuggestion"],
    )

    # Evidence tables not explicitly required but recommended by agent spec
    if bidirectional_rows:
        pass

    # Summary JSON
    summary = {
        "run_label": args.run_label,
        "timestamp_local": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "execution_root": str(execution_root),
        "scope": args.scope,
        "filters": {
            "filter_active_only": filter_active_only,
            "normalize_ids": normalize_ids,
            "edge_filter": {"DependencyClass": "EXECUTION", "TargetType": "DELIVERABLE"},
        },
        "deliverables": {
            "total": total_deliverables,
            "coverage": {
                "ok": ok_count,
                "missing_dependencies_csv": missing_count,
                "unreadable": unreadable_count,
                "schema_invalid": schema_invalid_count,
            },
        },
        "edges": {
            "execution_to_deliverable_rows_total": len(edges_all),
            "internal_definite_edges": len(definite_internal_edges),
            "internal_ambiguous_direction_edges": len(ambiguous_edges_internal),
        },
        "checks": {
            "schema_compliance": schema_verdict,
            "orphan_dependencies": orphan_verdict,
            "circular_dependencies": cycle_verdict,
            "anchor_coverage": anchor_verdict,
            "misplaced_fields": misplaced_verdict,
            "id_format_consistency": id_norm_verdict,
            "isolated_deliverables": isolated_verdict,
            "hub_analysis": hub_verdict,
            "bidirectional_pairs": bidi_verdict,
        },
        "metrics": {
            "orphans": len(orphans_rows),
            "cyclic_sccs": len(cyclic_sccs),
            "isolated_deliverables": len(isolated),
            "anchors_missing": len(anchors_missing_sorted),
            "misplaced_rows": len(misplaced_rows),
            "id_normalizations": len(id_normalization_events),
            "hubs": len(hubs_rows),
            "bidirectional_pairs": len(bidirectional_rows),
        },
        "overall": overall,
    }
    (output_dir / "closure_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    # Brief / logs
    brief_md = f"""# Brief — AUDIT_DEP_CLOSURE

## Verbatim

{args.brief_verbatim}

## Normalized

- EXECUTION_ROOT: `{execution_root}`
- SCOPE: `ALL`
- RUN_LABEL: `{args.run_label}`
- REQUESTED_BY: `{args.requested_by}`
- FILTER_ACTIVE_ONLY: `{str(filter_active_only).lower()}`
- NORMALIZE_IDS: `{str(normalize_ids).lower()}`
- EDGE_FILTER: `DependencyClass=EXECUTION`, `TargetType=DELIVERABLE`
- HUB_THRESHOLD: `{args.hub_threshold}`
- MAX_CYCLES: `{args.max_cycles}`
"""
    _write_text(output_dir / "Brief.md", brief_md)

    decision_log = f"""# Decision Log

- Used `EXECUTION_ROOT={execution_root}` (from INIT.md execution root; script arg default is `.`).
- Used default edge filter: `DependencyClass=EXECUTION` and `TargetType=DELIVERABLE`.
- Orphan detection is based on `TargetDeliverableID` after normalization (analysis-only).
- Graph metrics (isolates/hubs/SCCs) are computed on in-scope deliverables only; edges to orphans are excluded from SCC/degree calculations but recorded in `Evidence/orphans.csv`.
- SCC detection treats rows with unknown/missing `Direction` as undirected for SCC membership only (adds A↔B in SCC graph) and records the ambiguity via metrics.
"""
    _write_text(output_dir / "Decision_Log.md", decision_log)

    qa_lines = [
        "# QA Report",
        "",
        "## Coverage",
        "",
        f"- Total deliverables discovered: {total_deliverables}",
        f"- Dependencies.csv OK: {ok_count}",
        f"- Missing Dependencies.csv: {missing_count}",
        f"- Unreadable Dependencies.csv: {unreadable_count}",
        f"- Schema-invalid Dependencies.csv: {schema_invalid_count}",
        "",
        "## Limits / Notes",
        "",
        "- Schema validation supports v3.1 required columns (see AGENT_DEPENDENCIES.md).",
        "- SCC analysis uses definite directed edges plus bidirectional treatment for unknown-direction edges (membership only).",
    ]
    if unreadable_details:
        qa_lines.append("")
        qa_lines.append("## Unreadable files")
        for d in unreadable_details[:20]:
            qa_lines.append(f"- {d['DeliverableID']}: {d['DependenciesCsv']} — {d['Error']}")
        if len(unreadable_details) > 20:
            qa_lines.append(f"- (truncated) {len(unreadable_details) - 20} more")
    if schema_invalid_details:
        qa_lines.append("")
        qa_lines.append("## Schema-invalid files")
        for d in schema_invalid_details[:20]:
            qa_lines.append(f"- {d['DeliverableID']}: missing {d['MissingColumns']}")
        if len(schema_invalid_details) > 20:
            qa_lines.append(f"- (truncated) {len(schema_invalid_details) - 20} more")
    _write_text(output_dir / "QA_Report.md", "\n".join(qa_lines) + "\n")

    # Dependency Closure Report
    top_issues = [i for i in issues_sorted if i.severity in {"BLOCKER", "WARNING"}][:10]
    report_lines = [
        "# Dependency Closure Report — AUDIT_DEP_CLOSURE",
        "",
        f"- Snapshot: `{output_dir}`",
        f"- Execution root: `{execution_root}`",
        f"- Scope: `ALL`",
        f"- Overall verdict: **{overall}**",
        "",
        "## Check Verdicts",
        "",
        f"- Schema compliance: {schema_verdict}",
        f"- Orphan dependencies: {orphan_verdict}",
        f"- Circular dependencies (SCCs): {cycle_verdict}",
        f"- Anchor coverage (IMPLEMENTS_NODE): {anchor_verdict}",
        f"- Misplaced fields: {misplaced_verdict}",
        f"- ID format consistency / normalization: {id_norm_verdict}",
        f"- Isolated deliverables: {isolated_verdict}",
        f"- Hub analysis (degree ≥ {args.hub_threshold}): {hub_verdict}",
        f"- Bidirectional pairs: {bidi_verdict}",
        "",
        "## Key Metrics",
        "",
        f"- Orphan deps (TargetDeliverableID not found): {len(orphans_rows)}",
        f"- Cyclic SCCs: {len(cyclic_sccs)}",
        f"- Isolated deliverables: {len(isolated)}",
        f"- Missing anchors: {len(anchors_missing_sorted)}",
        f"- Misplaced-field rows: {len(misplaced_rows)}",
        "",
        "## Evidence Files",
        "",
        "- `Evidence/coverage.csv`",
        "- `Evidence/orphans.csv` (if any)",
        "- `Evidence/scc_summary.csv` and `Evidence/cycles_sample.csv` (if any)",
        "- `Evidence/isolated_deliverables.csv` (if any)",
        "- `Evidence/hubs.csv` (if any)",
        "- `Evidence/bidirectional_pairs.csv` (if any)",
        "- `Dependency_Closure_IssueLog.csv` (worklist)",
        "",
    ]
    if top_issues:
        report_lines.append("## Top Issues (≤10)")
        report_lines.append("")
        for i in top_issues:
            report_lines.append(f"- {i.severity} {i.check}: {i.issue_id} — {i.evidence}")
        report_lines.append("")

    report_lines.append("## Recommended Next Actions")
    report_lines.append("")
    if orphan_verdict == "BLOCKER":
        report_lines.append("- Fix orphan TargetDeliverableID references (see `Evidence/orphans.csv`), then rerun closure.")
    if schema_invalid_count or unreadable_count or missing_count:
        report_lines.append("- Rerun DEPENDENCIES on any missing/unreadable/schema-invalid deliverables, then rerun closure.")
    if cyclic_sccs:
        report_lines.append("- Review cyclic SCCs (see `Evidence/scc_summary.csv`) and decide: bundle as iterative sets or adjust dependency directions/types.")
    if isolated:
        report_lines.append("- Review isolated deliverables; add declared deps or rerun DEPENDENCIES extraction.")
    if not (orphan_verdict == "BLOCKER" or cyclic_sccs or isolated or schema_invalid_count or unreadable_count or missing_count):
        report_lines.append("- No action required; dependency graph closure is clean for the default edge filter.")

    _write_text(output_dir / "Dependency_Closure_Report.md", "\n".join(report_lines) + "\n")

    _write_text(output_dir / "RUN_SUMMARY.md", f"RUN_STATUS = {run_status}\n\nOVERALL = {overall}\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
