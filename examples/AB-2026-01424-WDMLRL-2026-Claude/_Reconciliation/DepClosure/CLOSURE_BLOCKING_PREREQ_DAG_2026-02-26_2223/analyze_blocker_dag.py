#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import dataclasses
import datetime as dt
import json
import re
import sys
from collections import defaultdict, deque
from pathlib import Path
from typing import Any, DefaultDict, Iterable, Literal


def _clean(value: Any) -> str:
    return str(value or "").strip()


_DEL_ID_RE = re.compile(r"^(DEL-\d{3}-\d{2})(?:_.*)?$")
_PKG_ID_RE = re.compile(r"^(PKG-\d{3})(?:_.*)?$")


def normalize_deliverable_id(raw_id: str) -> str:
    raw = _clean(raw_id)
    if not raw:
        return ""
    match = _DEL_ID_RE.match(raw)
    if match:
        return match.group(1)
    return raw.split("_", 1)[0] if "_" in raw else raw


def normalize_package_id(raw_id: str) -> str:
    raw = _clean(raw_id)
    if not raw:
        return ""
    match = _PKG_ID_RE.match(raw)
    if match:
        return match.group(1)
    return raw.split("_", 1)[0] if "_" in raw else raw


@dataclasses.dataclass(frozen=True)
class Deliverable:
    deliverable_id: str
    package_id: str
    path: Path


@dataclasses.dataclass(frozen=True)
class Edge:
    src: str
    dst: str
    dependency_id: str
    csv_path: str
    row_number: int
    direction: str
    from_id: str
    target_id: str
    statement: str


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
    except Exception as e:  # noqa: BLE001 - report as unreadable
        return [], [], f"UNREADABLE: {type(e).__name__}: {e}"


def tarjan_scc(nodes: Iterable[str], adjacency: dict[str, list[str]]) -> list[list[str]]:
    index = 0
    index_map: dict[str, int] = {}
    lowlink: dict[str, int] = {}
    stack: list[str] = []
    on_stack: set[str] = set()
    sccs: list[list[str]] = []

    sys.setrecursionlimit(20000)

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

    return sorted(sccs, key=lambda s: (-len(s), s[0] if s else ""))


def topo_tiers(nodes: list[str], adjacency: dict[str, list[str]]) -> dict[str, int]:
    indegree: DefaultDict[str, int] = defaultdict(int)
    for u in nodes:
        indegree.setdefault(u, 0)
    for u, vs in adjacency.items():
        for v in vs:
            indegree[v] += 1

    tier: dict[str, int] = {n: 0 for n in nodes}
    q = deque(sorted([n for n in nodes if indegree[n] == 0]))

    while q:
        u = q.popleft()
        for v in adjacency.get(u, []):
            tier[v] = max(tier[v], tier[u] + 1)
            indegree[v] -= 1
            if indegree[v] == 0:
                q.append(v)

    return tier


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in fieldnames})


def main() -> int:
    parser = argparse.ArgumentParser(description="Blocking prerequisite deliverable DAG analysis")
    parser.add_argument("--execution-root", default=".", help="Execution root (repo-relative or absolute)")
    parser.add_argument("--output-dir", required=True, help="Snapshot output directory")
    parser.add_argument("--run-label", default="BLOCKING_PREREQ_DAG")
    parser.add_argument(
        "--brief-verbatim",
        default="Compute deliverable DAG for blocking prerequisites only",
        help="Verbatim brief text to embed in Brief.md",
    )
    args = parser.parse_args()

    execution_root = Path(args.execution_root).resolve()
    output_dir = Path(args.output_dir).resolve()
    evidence_dir = output_dir / "Evidence"
    evidence_dir.mkdir(parents=True, exist_ok=True)

    deliverables = discover_deliverables(execution_root)
    if not deliverables:
        _write_text(output_dir / "RUN_SUMMARY.md", "RUN_STATUS = FAILED_INPUTS\n\nReason: No deliverables discovered.\n")
        return 2

    deliverable_ids = sorted({d.deliverable_id for d in deliverables})
    pkg_by_del = {d.deliverable_id: d.package_id for d in deliverables}
    del_set = set(deliverable_ids)

    coverage_rows: list[dict[str, str]] = []
    edges: list[Edge] = []
    orphans: list[dict[str, str]] = []
    unreadable: list[dict[str, str]] = []

    # Filter definition (hard-coded; this snapshot exists specifically to define a DAG)
    FILTER = {
        "Status": "ACTIVE",
        "DependencyClass": "EXECUTION",
        "TargetType": "DELIVERABLE",
        "DependencyType": "PREREQUISITE",
        "EstimateImpactClass": "BLOCKING",
        "Direction": {"UPSTREAM", "DOWNSTREAM"},
    }

    for d in deliverables:
        csv_path = d.path / "Dependencies.csv"
        if not csv_path.exists():
            coverage_rows.append(
                {
                    "DeliverableID": d.deliverable_id,
                    "PackageID": d.package_id,
                    "DependenciesCsv": str(csv_path),
                    "CoverageStatus": "MISSING_DEPENDENCIES_CSV",
                    "EdgeRowsIncluded": "0",
                }
            )
            continue

        fieldnames, rows, err = _read_csv_rows(csv_path)
        if err:
            coverage_rows.append(
                {
                    "DeliverableID": d.deliverable_id,
                    "PackageID": d.package_id,
                    "DependenciesCsv": str(csv_path),
                    "CoverageStatus": "UNREADABLE",
                    "EdgeRowsIncluded": "0",
                }
            )
            unreadable.append({"DeliverableID": d.deliverable_id, "DependenciesCsv": str(csv_path), "Error": err})
            continue

        included = 0
        for row_number, row in enumerate(rows, start=2):
            if _clean(row.get("Status", "")).upper() != FILTER["Status"]:
                continue
            if _clean(row.get("DependencyClass", "")).upper() != FILTER["DependencyClass"]:
                continue
            if _clean(row.get("TargetType", "")).upper() != FILTER["TargetType"]:
                continue
            if _clean(row.get("DependencyType", "")).upper() != FILTER["DependencyType"]:
                continue
            if _clean(row.get("EstimateImpactClass", "")).upper() != FILTER["EstimateImpactClass"]:
                continue
            direction = _clean(row.get("Direction", "")).upper()
            if direction not in FILTER["Direction"]:
                continue

            from_id = normalize_deliverable_id(row.get("FromDeliverableID", ""))
            target_id = normalize_deliverable_id(row.get("TargetDeliverableID", ""))
            if not from_id or not target_id:
                continue

            if target_id not in del_set:
                orphans.append(
                    {
                        "FromDeliverableID": from_id,
                        "TargetDeliverableID": target_id,
                        "DependencyID": _clean(row.get("DependencyID", "")),
                        "Evidence": f"{csv_path}:{row_number}",
                    }
                )
                continue

            if direction == "UPSTREAM":
                src, dst = target_id, from_id
            else:
                src, dst = from_id, target_id

            edges.append(
                Edge(
                    src=src,
                    dst=dst,
                    dependency_id=_clean(row.get("DependencyID", "")),
                    csv_path=str(csv_path),
                    row_number=row_number,
                    direction=direction,
                    from_id=from_id,
                    target_id=target_id,
                    statement=_clean(row.get("Statement", "")),
                )
            )
            included += 1

        coverage_rows.append(
            {
                "DeliverableID": d.deliverable_id,
                "PackageID": d.package_id,
                "DependenciesCsv": str(csv_path),
                "CoverageStatus": "OK",
                "EdgeRowsIncluded": str(included),
            }
        )

    _write_csv(
        evidence_dir / "coverage.csv",
        coverage_rows,
        ["DeliverableID", "PackageID", "DependenciesCsv", "CoverageStatus", "EdgeRowsIncluded"],
    )
    if unreadable:
        _write_csv(evidence_dir / "unreadable.csv", unreadable, ["DeliverableID", "DependenciesCsv", "Error"])

    if orphans:
        _write_csv(
            evidence_dir / "orphans.csv",
            orphans,
            ["FromDeliverableID", "TargetDeliverableID", "DependencyID", "Evidence"],
        )

    # Build adjacency and degrees
    adjacency_set: DefaultDict[str, set[str]] = defaultdict(set)
    indegree: DefaultDict[str, int] = defaultdict(int)
    outdegree: DefaultDict[str, int] = defaultdict(int)

    for node in deliverable_ids:
        indegree.setdefault(node, 0)
        outdegree.setdefault(node, 0)

    for e in edges:
        if e.src not in del_set or e.dst not in del_set:
            continue
        if e.dst not in adjacency_set[e.src]:
            adjacency_set[e.src].add(e.dst)
            outdegree[e.src] += 1
            indegree[e.dst] += 1

    adjacency = {k: sorted(v) for k, v in adjacency_set.items()}

    # SCCs / cycles
    sccs = tarjan_scc(deliverable_ids, adjacency)
    cyclic_sccs = [s for s in sccs if len(s) > 1]

    # Tiers (longest-path level) only meaningful if acyclic
    tiers: dict[str, int] = {}
    if not cyclic_sccs:
        tiers = topo_tiers(deliverable_ids, adjacency)

    # Evidence: edge list
    edge_rows = []
    for e in sorted(edges, key=lambda x: (x.src, x.dst, x.dependency_id, x.csv_path, x.row_number)):
        edge_rows.append(
            {
                "Src": e.src,
                "Dst": e.dst,
                "DependencyID": e.dependency_id,
                "Direction": e.direction,
                "FromDeliverableID": e.from_id,
                "TargetDeliverableID": e.target_id,
                "Evidence": f"{e.csv_path}:{e.row_number}",
                "Statement": e.statement,
            }
        )
    _write_csv(
        evidence_dir / "edges.csv",
        edge_rows,
        ["Src", "Dst", "DependencyID", "Direction", "FromDeliverableID", "TargetDeliverableID", "Evidence", "Statement"],
    )

    # Evidence: tiers
    if tiers:
        tier_rows = []
        for d_id in deliverable_ids:
            tier_rows.append(
                {
                    "DeliverableID": d_id,
                    "PackageID": pkg_by_del.get(d_id, ""),
                    "Tier": str(tiers.get(d_id, 0)),
                    "InDegree": str(indegree.get(d_id, 0)),
                    "OutDegree": str(outdegree.get(d_id, 0)),
                }
            )
        _write_csv(
            evidence_dir / "tiers.csv",
            tier_rows,
            ["DeliverableID", "PackageID", "Tier", "InDegree", "OutDegree"],
        )

    overall: Literal["PASS", "WARNING", "BLOCKER"] = "PASS"
    if orphans or unreadable:
        overall = "BLOCKER"
    elif cyclic_sccs:
        overall = "WARNING"

    run_status = "OK" if overall == "PASS" else "WARNINGS"

    # Brief / summary / report
    brief = f"""# Brief — {args.run_label}

## Verbatim

{args.brief_verbatim}

## DAG Definition (hard-coded for this run)

- Status = ACTIVE
- DependencyClass = EXECUTION
- TargetType = DELIVERABLE
- DependencyType = PREREQUISITE
- EstimateImpactClass = BLOCKING
- Direction in {{UPSTREAM, DOWNSTREAM}}

Direction interpretation:
- UPSTREAM rows are treated as `TargetDeliverableID → FromDeliverableID`
- DOWNSTREAM rows are treated as `FromDeliverableID → TargetDeliverableID`
"""
    _write_text(output_dir / "Brief.md", brief)

    summary = {
        "run_label": args.run_label,
        "timestamp_local": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "execution_root": str(execution_root),
        "filters": {k: sorted(v) if isinstance(v, set) else v for k, v in FILTER.items()},
        "deliverables_total": len(deliverable_ids),
        "edges_included": len(edges),
        "orphans": len(orphans),
        "cyclic_sccs": len(cyclic_sccs),
        "overall": overall,
    }
    _write_text(output_dir / "blocker_dag_summary.json", json.dumps(summary, indent=2, sort_keys=True) + "\n")

    report_lines = [
        f"# Blocking Prerequisite Deliverable DAG — {args.run_label}",
        "",
        f"- Snapshot: `{output_dir}`",
        f"- Execution root: `{execution_root}`",
        f"- Deliverables: {len(deliverable_ids)}",
        f"- Included edges: {len(edges)}",
        f"- Orphans (deliverable targets missing): {len(orphans)}",
        f"- Cyclic SCCs: {len(cyclic_sccs)}",
        f"- Overall: **{overall}**",
        "",
        "## Evidence",
        "",
        "- `Evidence/coverage.csv`",
        "- `Evidence/edges.csv`",
        "- `Evidence/tiers.csv` (only when acyclic)",
        "- `Evidence/orphans.csv` (if any)",
        "",
    ]
    if cyclic_sccs:
        report_lines.append("## Cycles")
        report_lines.append("")
        report_lines.append("This DAG definition still contains cycles. Review SCCs and decide whether to:")
        report_lines.append("- treat SCCs as iterative bundles (condensation DAG), or")
        report_lines.append("- reclassify non-precedence edges (e.g., INTERFACE vs PREREQUISITE), or")
        report_lines.append("- split deliverables into procurement vs installation phases (if decomposition changes are allowed).")
        report_lines.append("")
        for i, scc in enumerate(cyclic_sccs[:10], start=1):
            report_lines.append(f"- SCC-{i:03d} size={len(scc)} nodes={';'.join(scc)}")
        if len(cyclic_sccs) > 10:
            report_lines.append(f"- (truncated) {len(cyclic_sccs) - 10} more SCCs")
        report_lines.append("")
    else:
        report_lines.append("## Tiers (execution order aid)")
        report_lines.append("")
        report_lines.append("This DAG is acyclic under the definition above. Use `Evidence/tiers.csv` as a wave/tier execution order for:")
        report_lines.append("- blocker-based progress reporting,")
        report_lines.append("- tiered estimating fan-out (parallel within a tier),")
        report_lines.append("- or schedule scaffolding (precedence constraints).")
        report_lines.append("")

    _write_text(output_dir / "Blocker_Prereq_DAG_Report.md", "\n".join(report_lines) + "\n")

    _write_text(output_dir / "RUN_SUMMARY.md", f"RUN_STATUS = {run_status}\n\nOVERALL = {overall}\n")

    return 0 if overall != "BLOCKER" else 1


if __name__ == "__main__":
    raise SystemExit(main())
