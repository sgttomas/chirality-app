#!/usr/bin/env python3
"""
Materialize deliverable-local Dependencies.csv mirrors from an aggregate DAG.

Only non-PKG-00 deliverables are written. PKG-00 remains architecture context
evidence and does not receive local dependency registers from this tool.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

from audit_dag import ACTIVE, CANDIDATE, PKG_00, read_csv_rows


MATERIALIZED_STATUSES = {ACTIVE, CANDIDATE}


def sort_key(row: dict[str, str]) -> tuple[str, str]:
    return (row.get("DependencyID", ""), row.get("TargetDeliverableID", ""))


def write_dependency_csv(path: Path, header: list[str], rows: list[dict[str, str]], dry_run: bool) -> None:
    if dry_run:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=header, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in header})


def dag_label_from_path(edges_path: Path) -> str:
    parent_name = edges_path.parent.name.strip()
    return parent_name if parent_name else "AGGREGATE_DAG"


def pointer_status(source_label: str) -> str:
    return f"SYNCHRONIZED_FROM_{source_label.replace('-', '_').upper()}"


def pointer_text(
    node: dict[str, str],
    row_count: int,
    active_count: int,
    candidate_count: int,
    generated: str,
    source_label: str,
    source_edges_path: Path,
) -> str:
    deliverable_id = node.get("DeliverableID", "")
    deliverable_name = node.get("DeliverableName", "")
    return "\n".join([
        f"# Dependencies: {deliverable_id} {deliverable_name}",
        "",
        "## Generated Dependency Register",
        f"- **Status:** {pointer_status(source_label)}",
        f"- **Source of Truth:** `{source_edges_path}`",
        "- **Local Register:** `Dependencies.csv`",
        f"- **Rows:** {row_count} total; {active_count} ACTIVE; {candidate_count} CANDIDATE.",
        f"- **Generated:** {generated}",
        "",
        "## Authority Boundary",
        f"- Aggregate `{source_label}` remains the sequencing and blocker-computation authority within its approval boundary.",
        "- This local register is a synchronized mirror/evidence surface, not an independent graph authority.",
        "- `CANDIDATE` rows remain non-gating until later RECONCILIATION plus CHANGE approval.",
        "- `PKG-00` architecture-basis rows are preserved here as injected context evidence; `PKG-00` does not receive local dependency registers.",
        "",
    ])


def write_pointer(path: Path, content: str, dry_run: bool) -> None:
    if dry_run:
        return
    path.write_text(content, encoding="utf-8")


def materialize_local_dependencies(
    edges_path: Path,
    nodes_path: Path,
    execution_root: Path,
    refresh_pointers: bool = False,
    dry_run: bool = False,
    generated_date: str | None = None,
    source_label: str | None = None,
    deliverable_ids: set[str] | None = None,
) -> dict[str, object]:
    header, edge_rows, edge_width_issues = read_csv_rows(edges_path)
    _node_header, node_rows, node_width_issues = read_csv_rows(nodes_path)
    generated = generated_date or date.today().isoformat()
    resolved_source_label = source_label or dag_label_from_path(edges_path)

    rows_by_from: dict[str, list[dict[str, str]]] = defaultdict(list)
    skipped_status_counts: dict[str, int] = defaultdict(int)
    for row in edge_rows:
        status = row.get("Status", "").strip()
        if status not in MATERIALIZED_STATUSES:
            skipped_status_counts[status or "BLANK"] += 1
            continue
        from_id = row.get("FromDeliverableID", "").strip()
        if from_id:
            rows_by_from[from_id].append(row)

    written: list[dict[str, object]] = []
    skipped_pkg00: list[str] = []
    missing_execution_paths: list[dict[str, str]] = []

    for node in sorted(node_rows, key=lambda item: item.get("DeliverableID", "")):
        deliverable_id = node.get("DeliverableID", "").strip()
        package_id = node.get("PackageID", "").strip()
        execution_path_raw = node.get("ExecutionPath", "").strip()
        if not deliverable_id:
            continue
        if deliverable_ids is not None and deliverable_id not in deliverable_ids:
            continue
        if package_id == PKG_00:
            skipped_pkg00.append(deliverable_id)
            continue
        if not execution_path_raw:
            missing_execution_paths.append({"DeliverableID": deliverable_id, "Reason": "blank ExecutionPath"})
            continue

        execution_path = Path(execution_path_raw)
        if not execution_path.is_absolute():
            execution_path = execution_root.parent / execution_path

        if not execution_path.exists():
            missing_execution_paths.append({"DeliverableID": deliverable_id, "Reason": str(execution_path)})
            continue

        rows = sorted(rows_by_from.get(deliverable_id, []), key=sort_key)
        active_count = sum(1 for row in rows if row.get("Status", "").strip() == ACTIVE)
        candidate_count = sum(1 for row in rows if row.get("Status", "").strip() == CANDIDATE)
        csv_path = execution_path / "Dependencies.csv"
        pointer_path = execution_path / "_DEPENDENCIES.md"

        write_dependency_csv(csv_path, header, rows, dry_run=dry_run)
        if refresh_pointers:
            write_pointer(
                pointer_path,
                pointer_text(
                    node,
                    len(rows),
                    active_count,
                    candidate_count,
                    generated,
                    resolved_source_label,
                    edges_path,
                ),
                dry_run=dry_run,
            )

        written.append({
            "DeliverableID": deliverable_id,
            "PackageID": package_id,
            "DependenciesCsv": str(csv_path),
            "DependenciesPointer": str(pointer_path) if refresh_pointers else "",
            "Rows": len(rows),
            "ActiveRows": active_count,
            "CandidateRows": candidate_count,
        })

    total_rows = sum(int(item["Rows"]) for item in written)
    total_active_rows = sum(int(item["ActiveRows"]) for item in written)
    total_candidate_rows = sum(int(item["CandidateRows"]) for item in written)

    return {
        "edges_path": str(edges_path),
        "nodes_path": str(nodes_path),
        "source_label": resolved_source_label,
        "filtered_deliverable_ids": sorted(deliverable_ids or []),
        "execution_root": str(execution_root),
        "dry_run": dry_run,
        "refresh_pointers": refresh_pointers,
        "edge_row_width_issue_count": len(edge_width_issues),
        "node_row_width_issue_count": len(node_width_issues),
        "written_count": len(written),
        "total_rows": total_rows,
        "total_active_rows": total_active_rows,
        "total_candidate_rows": total_candidate_rows,
        "written": written,
        "skipped_pkg00_count": len(skipped_pkg00),
        "skipped_pkg00": skipped_pkg00,
        "missing_execution_path_count": len(missing_execution_paths),
        "missing_execution_paths": missing_execution_paths,
        "skipped_status_counts": dict(sorted(skipped_status_counts.items())),
    }


def render_console(summary: dict[str, object]) -> str:
    lines = []
    filtered = summary.get("filtered_deliverable_ids") or []
    if filtered:
        lines.append(f"Deliverable filter: {','.join(filtered)}")
    lines.extend([
        f"Written local registers: {summary['written_count']}",
        f"Skipped PKG-00 deliverables: {summary['skipped_pkg00_count']}",
        f"Missing execution paths: {summary['missing_execution_path_count']}",
        f"Rows materialized: total={summary['total_rows']} active={summary['total_active_rows']} candidate={summary['total_candidate_rows']}",
        f"Pointer refresh: {summary['refresh_pointers']}",
        f"Dry run: {summary['dry_run']}",
    ])
    return "\n".join(lines)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Materialize local Dependencies.csv mirrors from an aggregate DAG.")
    parser.add_argument(
        "--dag-dir",
        type=Path,
        default=Path("execution/_DAG/DAG-001"),
        help="Directory containing DependencyEdges.csv and DeliverableNodes.csv.",
    )
    parser.add_argument("--edges", type=Path, help="Override path to DependencyEdges.csv.")
    parser.add_argument("--nodes", type=Path, help="Override path to DeliverableNodes.csv.")
    parser.add_argument("--execution-root", type=Path, default=Path("execution"))
    parser.add_argument("--refresh-pointers", action="store_true", help="Rewrite _DEPENDENCIES.md generated pointers.")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--json-out", type=Path, help="Write materialization summary JSON.")
    parser.add_argument("--source-label", help="Label to write into generated pointer files, e.g. DAG-002.")
    parser.add_argument(
        "--deliverable-id",
        action="append",
        default=[],
        help="Restrict materialization to a deliverable ID. May be repeated or comma-separated.",
    )
    parser.add_argument(
        "--allow-missing-execution-paths",
        action="store_true",
        help="Return success when some DAG nodes do not yet have PREPARATION-created folders.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    edges_path = args.edges or args.dag_dir / "DependencyEdges.csv"
    nodes_path = args.nodes or args.dag_dir / "DeliverableNodes.csv"
    deliverable_ids = {
        item.strip()
        for value in args.deliverable_id
        for item in value.split(",")
        if item.strip()
    } or None
    summary = materialize_local_dependencies(
        edges_path=edges_path,
        nodes_path=nodes_path,
        execution_root=args.execution_root,
        refresh_pointers=args.refresh_pointers,
        dry_run=args.dry_run,
        source_label=args.source_label,
        deliverable_ids=deliverable_ids,
    )
    print(render_console(summary))
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    if int(summary["missing_execution_path_count"]) > 0 and not args.allow_missing_execution_paths:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
