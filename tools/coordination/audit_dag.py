#!/usr/bin/env python3
"""
Audit an aggregate DAG dependency register.

The audit treats execution/_DAG/DAG-001/DependencyEdges.csv as the aggregate
authority and reports graph hygiene without reading deliverable-local
Dependencies.csv mirrors.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Callable, Iterable


REQUIRED_COLUMNS = [
    "RegisterSchemaVersion", "DependencyID", "FromPackageID", "FromDeliverableID",
    "FromDeliverableName", "DependencyClass", "AnchorType", "Direction",
    "DependencyType", "TargetType", "TargetPackageID", "TargetDeliverableID",
    "TargetRefID", "TargetName", "TargetLocation", "Statement",
    "EvidenceFile", "SourceRef", "EvidenceQuote", "Explicitness",
    "RequiredMaturity", "ProposedMaturity", "SatisfactionStatus", "Confidence",
    "Origin", "FirstSeen", "LastSeen", "Status", "Notes",
]

ACTIVE = "ACTIVE"
CANDIDATE = "CANDIDATE"
DELIVERABLE = "DELIVERABLE"
EXECUTION = "EXECUTION"
ARCHITECTURE_BASIS = "ARCHITECTURE_BASIS"
PKG_00 = "PKG-00"
DEFAULT_HUB_THRESHOLD = 20

Row = dict[str, str]
EdgePredicate = Callable[[Row], bool]


def read_csv_rows(path: Path) -> tuple[list[str], list[Row], list[dict[str, object]]]:
    """Read CSV while keeping headers normalized and detecting ragged rows."""
    row_width_issues: list[dict[str, object]] = []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle)
        try:
            header = [col.strip() for col in next(reader)]
        except StopIteration:
            return [], [], []

        rows: list[Row] = []
        for line_number, raw in enumerate(reader, start=2):
            if len(raw) != len(header):
                row_width_issues.append({
                    "line": line_number,
                    "column_count": len(raw),
                    "expected_column_count": len(header),
                })
            padded = raw + [""] * max(0, len(header) - len(raw))
            rows.append({name: padded[index] for index, name in enumerate(header)})
    return header, rows, row_width_issues


def validate_schema(header: Iterable[str]) -> dict[str, object]:
    clean_header = [col.strip().lstrip("\ufeff") for col in header]
    missing = [col for col in REQUIRED_COLUMNS if col not in clean_header]
    extensions = [col for col in clean_header if col not in REQUIRED_COLUMNS]
    return {
        "valid": not missing,
        "required_column_count": len(REQUIRED_COLUMNS),
        "column_count": len(clean_header),
        "missing_columns": missing,
        "extension_columns": extensions,
    }


def normalized_edge(row: Row) -> tuple[str, str] | None:
    from_id = row.get("FromDeliverableID", "").strip()
    target_id = row.get("TargetDeliverableID", "").strip()
    if not from_id or not target_id:
        return None

    direction = row.get("Direction", "").strip()
    if direction == "UPSTREAM":
        return from_id, target_id
    if direction == "DOWNSTREAM":
        return target_id, from_id
    return from_id, target_id


def graph_rows(
    rows: Iterable[Row],
    statuses: set[str],
    predicate: EdgePredicate | None = None,
) -> list[Row]:
    selected: list[Row] = []
    for row in rows:
        if predicate and not predicate(row):
            continue
        if row.get("DependencyClass", "").strip() != EXECUTION:
            continue
        if row.get("TargetType", "").strip() != DELIVERABLE:
            continue
        if row.get("Status", "").strip() not in statuses:
            continue
        if normalized_edge(row) is None:
            continue
        selected.append(row)
    return selected


def build_graph(rows: Iterable[Row]) -> tuple[dict[str, set[str]], set[str], list[dict[str, str]]]:
    graph: dict[str, set[str]] = defaultdict(set)
    nodes: set[str] = set()
    edge_records: list[dict[str, str]] = []
    for row in rows:
        edge = normalized_edge(row)
        if edge is None:
            continue
        source, target = edge
        graph[source].add(target)
        nodes.add(source)
        nodes.add(target)
        edge_records.append({
            "DependencyID": row.get("DependencyID", ""),
            "Source": source,
            "Target": target,
        })
    return graph, nodes, edge_records


def find_sccs(graph: dict[str, set[str]], nodes: Iterable[str]) -> list[list[str]]:
    index_counter = [0]
    stack: list[str] = []
    index: dict[str, int] = {}
    lowlink: dict[str, int] = {}
    on_stack: set[str] = set()
    sccs: list[list[str]] = []

    def strongconnect(node: str) -> None:
        index[node] = index_counter[0]
        lowlink[node] = index_counter[0]
        index_counter[0] += 1
        stack.append(node)
        on_stack.add(node)

        for target in sorted(graph.get(node, set())):
            if target not in index:
                strongconnect(target)
                lowlink[node] = min(lowlink[node], lowlink[target])
            elif target in on_stack:
                lowlink[node] = min(lowlink[node], index[target])

        if lowlink[node] == index[node]:
            scc: list[str] = []
            while True:
                current = stack.pop()
                on_stack.remove(current)
                scc.append(current)
                if current == node:
                    break
            if len(scc) > 1:
                sccs.append(sorted(scc))

    for node in sorted(nodes):
        if node not in index:
            strongconnect(node)
    return sorted(sccs, key=lambda item: (len(item), item))


def endpoint_issues(rows: Iterable[Row], node_ids: set[str]) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    for row in rows:
        dep_id = row.get("DependencyID", "")
        from_id = row.get("FromDeliverableID", "").strip()
        target_id = row.get("TargetDeliverableID", "").strip()
        if from_id and from_id not in node_ids:
            issues.append({
                "DependencyID": dep_id,
                "Field": "FromDeliverableID",
                "Value": from_id,
            })
        if row.get("TargetType", "").strip() == DELIVERABLE and target_id and target_id not in node_ids:
            issues.append({
                "DependencyID": dep_id,
                "Field": "TargetDeliverableID",
                "Value": target_id,
            })
    return issues


def duplicate_edges(edge_records: Iterable[dict[str, str]]) -> dict[str, list[str]]:
    grouped: dict[tuple[str, str], list[str]] = defaultdict(list)
    for edge in edge_records:
        grouped[(edge["Source"], edge["Target"])].append(edge["DependencyID"])
    return {
        f"{source}->{target}": dep_ids
        for (source, target), dep_ids in sorted(grouped.items())
        if len(dep_ids) > 1
    }


def bidirectional_pairs(edge_records: Iterable[dict[str, str]]) -> list[list[str]]:
    pairs = {(edge["Source"], edge["Target"]) for edge in edge_records}
    bidirectional = set()
    for source, target in pairs:
        if (target, source) in pairs:
            bidirectional.add(tuple(sorted((source, target))))
    return [list(pair) for pair in sorted(bidirectional)]


def hub_summary(edge_records: Iterable[dict[str, str]], threshold: int) -> list[dict[str, object]]:
    degrees: dict[str, dict[str, int]] = defaultdict(lambda: {"in": 0, "out": 0})
    for edge in edge_records:
        source = edge["Source"]
        target = edge["Target"]
        degrees[source]["out"] += 1
        degrees[target]["in"] += 1

    hubs: list[dict[str, object]] = []
    for node, counts in degrees.items():
        total = counts["in"] + counts["out"]
        if total >= threshold:
            hubs.append({
                "DeliverableID": node,
                "InDegree": counts["in"],
                "OutDegree": counts["out"],
                "TotalDegree": total,
            })
    return sorted(hubs, key=lambda item: (-int(item["TotalDegree"]), str(item["DeliverableID"])))


def status_counts(rows: Iterable[Row]) -> dict[str, int]:
    return dict(sorted(Counter(row.get("Status", "").strip() or "BLANK" for row in rows).items()))


def dependency_type_counts(rows: Iterable[Row]) -> dict[str, int]:
    return dict(sorted(Counter(row.get("DependencyType", "").strip() or "BLANK" for row in rows).items()))


def dev001_projection(row: Row) -> bool:
    return (
        row.get("FromPackageID", "").strip() != PKG_00
        and row.get("TargetPackageID", "").strip() != PKG_00
        and row.get("DependencyType", "").strip() != ARCHITECTURE_BASIS
    )


def graph_analysis(
    rows: list[Row],
    statuses: set[str],
    hub_threshold: int,
    predicate: EdgePredicate | None = None,
) -> dict[str, object]:
    selected_rows = graph_rows(rows, statuses=statuses, predicate=predicate)
    graph, nodes, edge_records = build_graph(selected_rows)
    sccs = find_sccs(graph, nodes)
    duplicates = duplicate_edges(edge_records)
    bidirectional = bidirectional_pairs(edge_records)
    return {
        "node_count": len(nodes),
        "edge_count": len(edge_records),
        "scc_count": len(sccs),
        "sccs": sccs,
        "duplicate_edge_count": len(duplicates),
        "duplicate_edges": duplicates,
        "bidirectional_pair_count": len(bidirectional),
        "bidirectional_pairs": bidirectional,
        "hub_threshold": hub_threshold,
        "hub_count": len(hub_summary(edge_records, hub_threshold)),
        "hubs": hub_summary(edge_records, hub_threshold),
    }


def audit_dag(edges_path: Path, nodes_path: Path, hub_threshold: int = DEFAULT_HUB_THRESHOLD) -> dict[str, object]:
    edge_header, edge_rows, edge_width_issues = read_csv_rows(edges_path)
    node_header, node_rows, node_width_issues = read_csv_rows(nodes_path)
    node_ids = {row.get("DeliverableID", "").strip() for row in node_rows if row.get("DeliverableID", "").strip()}

    active_rows = [row for row in edge_rows if row.get("Status", "").strip() == ACTIVE]
    candidate_rows = [row for row in edge_rows if row.get("Status", "").strip() == CANDIDATE]
    projection_rows = [row for row in edge_rows if dev001_projection(row)]
    projection_active_rows = [row for row in projection_rows if row.get("Status", "").strip() == ACTIVE]
    projection_candidate_rows = [row for row in projection_rows if row.get("Status", "").strip() == CANDIDATE]

    return {
        "edges_path": str(edges_path),
        "nodes_path": str(nodes_path),
        "edge_schema": validate_schema(edge_header),
        "node_header_column_count": len(node_header),
        "edge_row_count": len(edge_rows),
        "node_row_count": len(node_rows),
        "package_count": len({row.get("PackageID", "").strip() for row in node_rows if row.get("PackageID", "").strip()}),
        "status_counts": status_counts(edge_rows),
        "active_edge_count": len(active_rows),
        "candidate_edge_count": len(candidate_rows),
        "active_dependency_type_counts": dependency_type_counts(active_rows),
        "candidate_dependency_type_counts": dependency_type_counts(candidate_rows),
        "endpoint_issue_count": len(endpoint_issues(edge_rows, node_ids)),
        "endpoint_issues": endpoint_issues(edge_rows, node_ids),
        "edge_row_width_issue_count": len(edge_width_issues),
        "edge_row_width_issues": edge_width_issues,
        "node_row_width_issue_count": len(node_width_issues),
        "node_row_width_issues": node_width_issues,
        "active_graph": graph_analysis(edge_rows, {ACTIVE}, hub_threshold),
        "active_plus_candidate_graph": graph_analysis(edge_rows, {ACTIVE, CANDIDATE}, hub_threshold),
        "dev001_projection": {
            "definition": "Excludes PKG-00 endpoints and ARCHITECTURE_BASIS rows; candidate rows remain non-gating.",
            "node_count": len({
                row.get("DeliverableID", "").strip()
                for row in node_rows
                if row.get("PackageID", "").strip() != PKG_00 and row.get("DeliverableID", "").strip()
            }),
            "edge_row_count": len(projection_rows),
            "active_edge_count": len(projection_active_rows),
            "candidate_edge_count": len(projection_candidate_rows),
            "active_dependency_type_counts": dependency_type_counts(projection_active_rows),
            "candidate_dependency_type_counts": dependency_type_counts(projection_candidate_rows),
            "active_graph": graph_analysis(edge_rows, {ACTIVE}, hub_threshold, predicate=dev001_projection),
            "active_plus_candidate_graph": graph_analysis(edge_rows, {ACTIVE, CANDIDATE}, hub_threshold, predicate=dev001_projection),
        },
    }


def strict_passed(summary: dict[str, object]) -> bool:
    edge_schema = summary["edge_schema"]
    active_graph = summary["active_graph"]
    return (
        bool(edge_schema["valid"])
        and int(summary["endpoint_issue_count"]) == 0
        and int(summary["edge_row_width_issue_count"]) == 0
        and int(active_graph["scc_count"]) == 0
        and int(active_graph["duplicate_edge_count"]) == 0
        and int(active_graph["bidirectional_pair_count"]) == 0
    )


def render_markdown(summary: dict[str, object]) -> str:
    edge_schema = summary["edge_schema"]
    active = summary["active_graph"]
    combined = summary["active_plus_candidate_graph"]
    projection = summary["dev001_projection"]
    projection_active = projection["active_graph"]
    projection_combined = projection["active_plus_candidate_graph"]

    lines = [
        "---",
        "doc_id: DEV-001-AGGREGATE-DAG-AUDIT",
        "doc_kind: coordination.audit",
        "status: generated",
        "created: 2026-04-30",
        "---",
        "",
        "# DEV-001 Aggregate DAG Audit",
        "",
        "## Authority",
        "",
        "- Source of truth: `execution/_DAG/DAG-001/DependencyEdges.csv`.",
        "- Local `Dependencies.csv` files are synchronized mirrors, not independent sequencing authority.",
        "- `CANDIDATE` rows remain non-gating.",
        "",
        "## Schema And Counts",
        "",
        f"- Edge schema valid: {edge_schema['valid']}",
        f"- Edge rows: {summary['edge_row_count']}",
        f"- Node rows: {summary['node_row_count']}",
        f"- Packages represented: {summary['package_count']}",
        f"- Active edges: {summary['active_edge_count']}",
        f"- Candidate edges: {summary['candidate_edge_count']}",
        f"- Endpoint issues: {summary['endpoint_issue_count']}",
        f"- Ragged edge rows: {summary['edge_row_width_issue_count']}",
        "",
        "## Active Graph",
        "",
        f"- Nodes touched: {active['node_count']}",
        f"- Directed edges: {active['edge_count']}",
        f"- SCCs with more than one node: {active['scc_count']}",
        f"- Duplicate directed edges: {active['duplicate_edge_count']}",
        f"- Bidirectional pairs: {active['bidirectional_pair_count']}",
        f"- Hubs at degree >= {active['hub_threshold']}: {active['hub_count']}",
        "",
        "## Active Plus Candidate Graph",
        "",
        f"- Nodes touched: {combined['node_count']}",
        f"- Directed edges: {combined['edge_count']}",
        f"- SCCs with more than one node: {combined['scc_count']}",
        f"- Duplicate directed edges: {combined['duplicate_edge_count']}",
        f"- Bidirectional pairs: {combined['bidirectional_pair_count']}",
        "",
        "## DEV-001 Projection",
        "",
        f"- Definition: {projection['definition']}",
        f"- Projection nodes: {projection['node_count']}",
        f"- Projection rows: {projection['edge_row_count']}",
        f"- Projection active edges: {projection['active_edge_count']}",
        f"- Projection candidate edges: {projection['candidate_edge_count']}",
        f"- Projection active SCCs: {projection_active['scc_count']}",
        f"- Projection active duplicate directed edges: {projection_active['duplicate_edge_count']}",
        f"- Projection active bidirectional pairs: {projection_active['bidirectional_pair_count']}",
        f"- Projection active+candidate SCCs: {projection_combined['scc_count']}",
        "",
    ]

    if active["sccs"]:
        lines += ["## Active SCCs", ""]
        for index, scc in enumerate(active["sccs"], start=1):
            lines.append(f"- SCC-{index:03d}: {', '.join(scc)}")
        lines.append("")

    if combined["sccs"]:
        lines += ["## Active Plus Candidate SCCs", ""]
        for index, scc in enumerate(combined["sccs"], start=1):
            lines.append(f"- SCC-C-{index:03d}: {', '.join(scc)}")
        lines.append("")

    if active["hubs"]:
        lines += ["## Active Hubs", ""]
        for hub in active["hubs"]:
            lines.append(
                f"- {hub['DeliverableID']}: in={hub['InDegree']} "
                f"out={hub['OutDegree']} total={hub['TotalDegree']}"
            )
        lines.append("")

    if summary["endpoint_issues"]:
        lines += ["## Endpoint Issues", ""]
        for issue in summary["endpoint_issues"]:
            lines.append(f"- {issue['DependencyID']}: {issue['Field']} `{issue['Value']}` is not in DeliverableNodes.csv")
        lines.append("")

    return "\n".join(lines)


def render_console(summary: dict[str, object]) -> str:
    active = summary["active_graph"]
    projection = summary["dev001_projection"]
    projection_active = projection["active_graph"]
    return "\n".join([
        f"Edge schema valid: {summary['edge_schema']['valid']}",
        f"Rows: edges={summary['edge_row_count']} nodes={summary['node_row_count']}",
        f"Status: ACTIVE={summary['active_edge_count']} CANDIDATE={summary['candidate_edge_count']}",
        f"Endpoint issues: {summary['endpoint_issue_count']}",
        f"Active graph: edges={active['edge_count']} sccs={active['scc_count']} "
        f"duplicates={active['duplicate_edge_count']} bidirectional={active['bidirectional_pair_count']}",
        f"DEV-001 projection: active_edges={projection['active_edge_count']} "
        f"candidate_edges={projection['candidate_edge_count']} active_sccs={projection_active['scc_count']}",
    ])


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit an aggregate DAG dependency register.")
    parser.add_argument(
        "--dag-dir",
        type=Path,
        default=Path("execution/_DAG/DAG-001"),
        help="Directory containing DependencyEdges.csv and DeliverableNodes.csv.",
    )
    parser.add_argument("--edges", type=Path, help="Override path to DependencyEdges.csv.")
    parser.add_argument("--nodes", type=Path, help="Override path to DeliverableNodes.csv.")
    parser.add_argument("--json-out", type=Path, help="Write JSON summary to this path.")
    parser.add_argument("--markdown-out", type=Path, help="Write markdown report to this path.")
    parser.add_argument("--hub-threshold", type=int, default=DEFAULT_HUB_THRESHOLD)
    parser.add_argument("--strict", action="store_true", help="Exit non-zero for active graph hygiene failures.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    edges_path = args.edges or args.dag_dir / "DependencyEdges.csv"
    nodes_path = args.nodes or args.dag_dir / "DeliverableNodes.csv"
    summary = audit_dag(edges_path=edges_path, nodes_path=nodes_path, hub_threshold=args.hub_threshold)

    print(render_console(summary))

    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    if args.markdown_out:
        args.markdown_out.parent.mkdir(parents=True, exist_ok=True)
        args.markdown_out.write_text(render_markdown(summary) + "\n", encoding="utf-8")

    if args.strict and not strict_passed(summary):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
