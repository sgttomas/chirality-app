#!/usr/bin/env python3
"""
Build the DEV-001 implementation-readiness blocker queue.

The queue interprets each active DAG edge as:

    FromDeliverableID consumes and is blocked by TargetDeliverableID.

Implementation blockers are satisfied only by explicit committed implementation
evidence, except for PKG-00 architecture-basis edges, which are satisfied by the
accepted architecture baseline.
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from typing import Iterable


ACTIVE = "ACTIVE"
CANDIDATE = "CANDIDATE"
ARCHITECTURE_BASIS = "ARCHITECTURE_BASIS"
PKG_00 = "PKG-00"
COMMITTED = "COMMITTED"
ARCHITECTURE_BASELINE = "ARCHITECTURE_BASELINE"
MISSING_EVIDENCE = "MISSING_EVIDENCE"
BLOCKED = "BLOCKED"
UNBLOCKED = "UNBLOCKED"
LIFECYCLE_STATES = ("OPEN", "INITIALIZED", "SEMANTIC_READY", "IN_PROGRESS", "CHECKING", "ISSUED", "RETIRED")

QUEUE_COLUMNS = [
    "DeliverableID",
    "PackageID",
    "DeliverableName",
    "LifecycleState",
    "ImplementationEvidenceState",
    "EvidenceCommit",
    "ActiveUpstreamCount",
    "SatisfiedUpstreamCount",
    "BlockingUpstreamCount",
    "BlockerState",
    "BlockingUpstreamDeliverables",
    "BlockingEdgeIDs",
]

EVIDENCE_COLUMNS = [
    "DeliverableID",
    "PackageID",
    "EvidenceState",
    "EvidenceKind",
    "Commit",
    "CommitSubject",
    "CommittedDate",
    "HandoffCommit",
    "Notes",
]

Row = dict[str, str]


def read_csv_rows(path: Path) -> tuple[list[str], list[Row]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def clean(value: object) -> str:
    return str(value or "").strip()


def read_nodes(nodes_path: Path) -> list[Row]:
    _header, rows = read_csv_rows(nodes_path)
    return [row for row in rows if clean(row.get("DeliverableID"))]


def read_edges(edges_path: Path) -> tuple[list[Row], int]:
    _header, rows = read_csv_rows(edges_path)
    active_rows = [
        row for row in rows
        if clean(row.get("Status")) == ACTIVE
        and clean(row.get("FromDeliverableID"))
        and clean(row.get("TargetDeliverableID"))
    ]
    candidate_count = sum(1 for row in rows if clean(row.get("Status")) == CANDIDATE)
    return active_rows, candidate_count


def read_evidence(evidence_path: Path) -> dict[str, Row]:
    _header, rows = read_csv_rows(evidence_path)
    evidence: dict[str, Row] = {}
    for row in rows:
        deliverable_id = clean(row.get("DeliverableID"))
        if deliverable_id:
            evidence[deliverable_id] = row
    return evidence


def filesystem_lifecycle_state(node: Row) -> str:
    execution_path = clean(node.get("ExecutionPath"))
    if execution_path:
        status_path = Path(execution_path) / "_STATUS.md"
        if status_path.exists():
            text = status_path.read_text(encoding="utf-8")
            for line in text.splitlines():
                if "Current State" in line:
                    for state in LIFECYCLE_STATES:
                        if state in line:
                            return state
    return clean(node.get("LifecycleState")) or "UNKNOWN"


def is_architecture_basis_satisfied(edge: Row) -> bool:
    # PKG-00 is the accepted architecture/context baseline. After TP-DAG-004,
    # refreshed local evidence may carry more specific dependency type labels
    # while still pointing at PKG-00 providers, so package identity is the
    # blocker-satisfaction boundary.
    return clean(edge.get("TargetPackageID")) == PKG_00


def committed_evidence(evidence: Row | None) -> bool:
    return clean((evidence or {}).get("EvidenceState")) == COMMITTED


def implementation_state(deliverable_id: str, package_id: str, evidence_by_id: dict[str, Row]) -> tuple[str, str]:
    evidence = evidence_by_id.get(deliverable_id)
    if committed_evidence(evidence):
        return COMMITTED, clean(evidence.get("Commit"))
    if package_id == PKG_00:
        return ARCHITECTURE_BASELINE, ""
    if evidence:
        return clean(evidence.get("EvidenceState")) or MISSING_EVIDENCE, clean(evidence.get("Commit"))
    return MISSING_EVIDENCE, ""


def provider_satisfaction(edge: Row, evidence_by_id: dict[str, Row]) -> tuple[bool, str]:
    if is_architecture_basis_satisfied(edge):
        return True, ARCHITECTURE_BASELINE

    provider_id = clean(edge.get("TargetDeliverableID"))
    evidence = evidence_by_id.get(provider_id)
    if committed_evidence(evidence):
        return True, COMMITTED
    if evidence:
        return False, clean(evidence.get("EvidenceState")) or MISSING_EVIDENCE
    return False, MISSING_EVIDENCE


def build_queue(edges_path: Path, nodes_path: Path, evidence_path: Path) -> dict[str, object]:
    nodes = read_nodes(nodes_path)
    active_edges, candidate_count = read_edges(edges_path)
    evidence_by_id = read_evidence(evidence_path)
    node_by_id = {clean(row.get("DeliverableID")): row for row in nodes}

    blockers_by_consumer: dict[str, list[Row]] = defaultdict(list)
    satisfied_counts: Counter[str] = Counter()
    upstream_counts: Counter[str] = Counter()
    architecture_basis_satisfied_edges = 0

    for edge in active_edges:
        consumer_id = clean(edge.get("FromDeliverableID"))
        upstream_counts[consumer_id] += 1
        satisfied, _reason = provider_satisfaction(edge, evidence_by_id)
        if satisfied:
            satisfied_counts[consumer_id] += 1
            if is_architecture_basis_satisfied(edge):
                architecture_basis_satisfied_edges += 1
        else:
            blockers_by_consumer[consumer_id].append(edge)

    queue_rows: list[Row] = []
    for node in nodes:
        deliverable_id = clean(node.get("DeliverableID"))
        package_id = clean(node.get("PackageID"))
        blocker_edges = blockers_by_consumer.get(deliverable_id, [])
        implementation_evidence_state, commit = implementation_state(deliverable_id, package_id, evidence_by_id)
        queue_rows.append({
            "DeliverableID": deliverable_id,
            "PackageID": package_id,
            "DeliverableName": clean(node.get("DeliverableName")),
            "LifecycleState": filesystem_lifecycle_state(node),
            "ImplementationEvidenceState": implementation_evidence_state,
            "EvidenceCommit": commit,
            "ActiveUpstreamCount": str(upstream_counts[deliverable_id]),
            "SatisfiedUpstreamCount": str(satisfied_counts[deliverable_id]),
            "BlockingUpstreamCount": str(len(blocker_edges)),
            "BlockerState": BLOCKED if blocker_edges else UNBLOCKED,
            "BlockingUpstreamDeliverables": ";".join(clean(edge.get("TargetDeliverableID")) for edge in blocker_edges),
            "BlockingEdgeIDs": ";".join(clean(edge.get("DependencyID")) for edge in blocker_edges),
        })

    row_by_id = {row["DeliverableID"]: row for row in queue_rows}

    missing_provider_groups: dict[str, dict[str, object]] = {}
    for consumer_id, blocker_edges in blockers_by_consumer.items():
        for edge in blocker_edges:
            provider_id = clean(edge.get("TargetDeliverableID"))
            provider_node = node_by_id.get(provider_id, {})
            provider_state, provider_commit = implementation_state(
                provider_id,
                clean(provider_node.get("PackageID") or edge.get("TargetPackageID")),
                evidence_by_id,
            )
            group = missing_provider_groups.setdefault(provider_id, {
                "ProviderDeliverableID": provider_id,
                "ProviderPackageID": clean(provider_node.get("PackageID") or edge.get("TargetPackageID")),
                "ProviderName": clean(provider_node.get("DeliverableName") or edge.get("TargetName")),
                "ProviderEvidenceState": provider_state,
                "ProviderEvidenceCommit": provider_commit,
                "Consumers": set(),
                "EdgeIDs": [],
            })
            group["Consumers"].add(consumer_id)
            group["EdgeIDs"].append(clean(edge.get("DependencyID")))

    missing_provider_rows: list[dict[str, object]] = []
    for provider_id in sorted(missing_provider_groups):
        group = missing_provider_groups[provider_id]
        consumers = sorted(str(item) for item in group["Consumers"])
        group["Consumers"] = consumers
        group["EdgeIDs"] = sorted(str(item) for item in group["EdgeIDs"])
        group["BlockedConsumerCount"] = len(consumers)
        missing_provider_rows.append(group)

    package_summary: dict[str, dict[str, int]] = {}
    for row in queue_rows:
        package = row["PackageID"]
        package_summary.setdefault(package, {UNBLOCKED: 0, BLOCKED: 0})
        package_summary[package][row["BlockerState"]] += 1

    evidence_state_counts = Counter(clean(row.get("EvidenceState")) or "BLANK" for row in evidence_by_id.values())
    lifecycle_state_counts = Counter(row["LifecycleState"] for row in queue_rows)

    return {
        "edges_path": str(edges_path),
        "nodes_path": str(nodes_path),
        "evidence_path": str(evidence_path),
        "package_count": len({clean(row.get("PackageID")) for row in nodes if clean(row.get("PackageID"))}),
        "node_count": len(nodes),
        "active_edge_count": len(active_edges),
        "candidate_edge_count": candidate_count,
        "evidence_record_count": len(evidence_by_id),
        "evidence_state_counts": dict(sorted(evidence_state_counts.items())),
        "lifecycle_state_counts": dict(sorted(lifecycle_state_counts.items())),
        "committed_evidence_count": sum(1 for row in evidence_by_id.values() if committed_evidence(row)),
        "architecture_basis_satisfied_edges": architecture_basis_satisfied_edges,
        "unblocked_count": sum(1 for row in queue_rows if row["BlockerState"] == UNBLOCKED),
        "blocked_count": sum(1 for row in queue_rows if row["BlockerState"] == BLOCKED),
        "package_summary": package_summary,
        "queue_rows": queue_rows,
        "queue_rows_by_id": row_by_id,
        "missing_provider_rows": missing_provider_rows,
    }


def markdown_cell(value: object) -> str:
    text = str(value)
    return text.replace("|", "\\|").replace("\n", "<br>")


def markdown_row(values: Iterable[object]) -> str:
    return "| " + " | ".join(markdown_cell(value) for value in values) + " |"


def render_markdown(summary: dict[str, object], generated_date: str) -> str:
    queue_rows: list[Row] = summary["queue_rows"]  # type: ignore[assignment]
    package_summary: dict[str, dict[str, int]] = summary["package_summary"]  # type: ignore[assignment]
    missing_provider_rows: list[dict[str, object]] = summary["missing_provider_rows"]  # type: ignore[assignment]

    unblocked_rows = [row for row in queue_rows if row["BlockerState"] == UNBLOCKED]
    blocked_rows = [row for row in queue_rows if row["BlockerState"] == BLOCKED]
    source_graph = str(summary["edges_path"])
    evidence_source = str(summary["evidence_path"])

    lines = [
        "---",
        "doc_id: DEV-001-BLOCKER-QUEUE",
        "doc_kind: coordination.blocker_queue",
        "status: computed_active_edges_only",
        "created: 2026-04-30",
        f"updated: {generated_date}",
        f"source_graph: {source_graph}",
        f"implementation_evidence_source: {evidence_source}",
        "implementation_threshold: COMMITTED",
        "architecture_basis: satisfied_by_existing_baseline",
        "candidate_edges: excluded",
        "---",
        "",
        "# DEV-001 Implementation-Readiness Blocker Queue",
        "",
        "This blocker queue is an advisory implementation-readiness view only. It is not a schedule, staffing plan, priority list, lifecycle approval, professional approval, or readiness-for-reliance claim.",
        "",
        "## Computation Rule",
        "",
        f"- Source graph: `{source_graph}`.",
        "- Included edges: `Status=ACTIVE` only.",
        "- Excluded edges: all `Status=CANDIDATE` rows.",
        "- Direction convention: `FromDeliverableID` is the downstream consumer and is blocked by `TargetDeliverableID`, the upstream provider.",
        f"- Satisfaction threshold: upstream provider has `COMMITTED` evidence in `{evidence_source}`.",
        "- `SEMANTIC_READY` remains decomposition/context readiness evidence; it does not satisfy implementation blockers by itself.",
        "- `PKG-00` provider edges are satisfied by the accepted architecture baseline, not by implementation evidence.",
        "- `UNBLOCKED` means all active upstream implementation dependencies satisfy the threshold or are satisfied architecture-basis edges.",
        "- `BLOCKED` means one or more active upstream providers lack committed implementation evidence.",
        "",
        "## Evidence Summary",
        "",
        "| Evidence | Count |",
        "|---|---:|",
        markdown_row(["Packages represented", summary["package_count"]]),
        markdown_row(["Deliverable nodes represented", summary["node_count"]]),
        markdown_row(["Active edges included", summary["active_edge_count"]]),
        markdown_row(["Candidate edges excluded", summary["candidate_edge_count"]]),
        markdown_row(["Implementation evidence records", summary["evidence_record_count"]]),
        markdown_row(["Committed implementation evidence", summary["committed_evidence_count"]]),
        markdown_row(["Filesystem lifecycle `SEMANTIC_READY` (display only)", summary["lifecycle_state_counts"].get("SEMANTIC_READY", 0)]),  # type: ignore[index]
        markdown_row(["PKG-00 architecture-basis edges satisfied", summary["architecture_basis_satisfied_edges"]]),
        markdown_row(["Implementation `UNBLOCKED` deliverables", summary["unblocked_count"]]),
        markdown_row(["Implementation `BLOCKED` deliverables", summary["blocked_count"]]),
        "",
        "## Package Summary",
        "",
        "| PackageID | UNBLOCKED | BLOCKED |",
        "|---|---:|---:|",
    ]

    for package in sorted(package_summary):
        counts = package_summary[package]
        lines.append(markdown_row([f"`{package}`", counts.get(UNBLOCKED, 0), counts.get(BLOCKED, 0)]))

    lines += [
        "",
        "## Unblocked DAG-Ready Items",
        "",
        "These deliverables have no active upstream implementation dependency below the `COMMITTED` threshold. Items without their own committed evidence are DAG-ready candidates, not completed work.",
        "",
        "| DeliverableID | PackageID | Implementation evidence | Active upstream | Name |",
        "|---|---|---|---:|---|",
    ]

    for row in unblocked_rows:
        state = row["ImplementationEvidenceState"]
        evidence = f"`{state}`"
        if row["EvidenceCommit"]:
            evidence = f"`{state}` `{row['EvidenceCommit']}`"
        lines.append(markdown_row([
            f"`{row['DeliverableID']}`",
            f"`{row['PackageID']}`",
            evidence,
            row["ActiveUpstreamCount"],
            row["DeliverableName"],
        ]))

    lines += [
        "",
        "## Blocked Items Grouped By Missing Upstream",
        "",
    ]

    if missing_provider_rows:
        lines += [
            "| Missing upstream | PackageID | Evidence state | Blocked consumers | Consumer IDs | Edge IDs |",
            "|---|---|---|---:|---|---|",
        ]
        for group in missing_provider_rows:
            consumers = "; ".join(f"`{consumer}`" for consumer in group["Consumers"])  # type: ignore[index]
            edge_ids = "; ".join(f"`{edge_id}`" for edge_id in group["EdgeIDs"])  # type: ignore[index]
            lines.append(markdown_row([
                f"`{group['ProviderDeliverableID']}` - {group['ProviderName']}",
                f"`{group['ProviderPackageID']}`",
                f"`{group['ProviderEvidenceState']}`",
                group["BlockedConsumerCount"],
                consumers,
                edge_ids,
            ]))
    else:
        lines.append("No blocked items were found under the implementation-readiness threshold.")

    lines += [
        "",
        "## Per-Deliverable Blocked Items",
        "",
    ]

    if blocked_rows:
        lines += [
            "| DeliverableID | PackageID | Missing upstream count | Missing upstream deliverables | Name |",
            "|---|---|---:|---|---|",
        ]
        for row in blocked_rows:
            missing = "; ".join(f"`{item}`" for item in row["BlockingUpstreamDeliverables"].split(";") if item)
            lines.append(markdown_row([
                f"`{row['DeliverableID']}`",
                f"`{row['PackageID']}`",
                row["BlockingUpstreamCount"],
                missing,
                row["DeliverableName"],
            ]))
    else:
        lines.append("No per-deliverable implementation blockers were found.")

    lines += [
        "",
        "## Candidate Edges Excluded",
        "",
        "Candidate edges remain non-gating pending later `RECONCILIATION` and `CHANGE`; they were not used in the blocker state calculation.",
        "",
        "## Machine-Readable Queue",
        "",
        "Full per-deliverable queue rows are recorded in `execution/_Coordination/DEV-001_BLOCKER_QUEUE.csv`.",
        "",
    ]

    return "\n".join(lines)


def write_queue_csv(path: Path, rows: list[Row]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=QUEUE_COLUMNS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the DEV-001 implementation-readiness blocker queue.")
    parser.add_argument(
        "--dag-dir",
        type=Path,
        default=Path("execution/_DAG/DAG-001"),
        help="Directory containing DependencyEdges.csv and DeliverableNodes.csv.",
    )
    parser.add_argument("--edges", type=Path, help="Override path to DependencyEdges.csv.")
    parser.add_argument("--nodes", type=Path, help="Override path to DeliverableNodes.csv.")
    parser.add_argument(
        "--evidence",
        type=Path,
        default=Path("execution/_Coordination/DEV-001_IMPLEMENTATION_EVIDENCE.csv"),
        help="DEV-001 implementation evidence register.",
    )
    parser.add_argument(
        "--csv-out",
        type=Path,
        default=Path("execution/_Coordination/DEV-001_BLOCKER_QUEUE.csv"),
        help="Machine-readable blocker queue output.",
    )
    parser.add_argument(
        "--markdown-out",
        type=Path,
        default=Path("execution/_Coordination/DEV-001_BLOCKER_QUEUE.md"),
        help="Markdown blocker queue output.",
    )
    parser.add_argument("--generated-date", default=date.today().isoformat())
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    edges_path = args.edges or args.dag_dir / "DependencyEdges.csv"
    nodes_path = args.nodes or args.dag_dir / "DeliverableNodes.csv"
    summary = build_queue(edges_path=edges_path, nodes_path=nodes_path, evidence_path=args.evidence)

    write_queue_csv(args.csv_out, summary["queue_rows"])  # type: ignore[arg-type]
    args.markdown_out.parent.mkdir(parents=True, exist_ok=True)
    args.markdown_out.write_text(render_markdown(summary, args.generated_date), encoding="utf-8")

    print(
        "DEV-001 implementation blocker queue: "
        f"unblocked={summary['unblocked_count']} "
        f"blocked={summary['blocked_count']} "
        f"active_edges={summary['active_edge_count']} "
        f"candidate_edges_excluded={summary['candidate_edge_count']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
