#!/usr/bin/env python3
"""Analyze a declared dependency scope with exhaustive CSV validation and graph evidence.

The historical positional root and --output-dir interface remains supported.
See tools/evaluation/README.md for report meanings and all brief-to-CLI options.
"""
from __future__ import annotations
import argparse
import csv
import json
import re
import sys
from collections import defaultdict, deque
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "evaluation"))
from audit_common import inventory, parse_register, require_root, schema

REQUIRED_COLUMNS = schema.REQUIRED_COLUMNS
HUB_THRESHOLD = 20
ID_PATTERN = re.compile(r"^((?:DEL|KTY)-\d{2,3}-\d{2,3}|(?:PKG|CAT)-\d{2,3})(?:_.+)?$")


def find_dependency_csvs(execution_root):
    return [str(unit / "Dependencies.csv") for unit in inventory(Path(execution_root)) if (unit / "Dependencies.csv").is_file()]


def normalize_id(raw_id):
    if not raw_id:
        return raw_id, False
    cleaned = raw_id.strip()
    match = ID_PATTERN.fullmatch(cleaned)
    normalized = match.group(1) if match else cleaned
    return normalized, normalized != raw_id


def validate_schema(header):
    clean = [value.strip().lstrip('\ufeff') for value in header]
    return [name for name in REQUIRED_COLUMNS if name not in clean], clean


def load_all_edges(csv_paths, normalize_ids=True):
    rows, reports, normalizations = [], {}, []
    for filename in csv_paths:
        path = Path(filename)
        report, raw_rows = parse_register(path)
        unit_id = path.parent.name.split("_")[0]
        report["valid"] = report["schema_valid"]
        report["missing_columns"] = sorted(set(REQUIRED_COLUMNS) - set(report["columns"]))
        reports[unit_id] = report
        # An unreadable/header-invalid register supplies no topology. A valid
        # header with malformed individual records still exposes other valid rows.
        bad_header = report["issues"] or not report["denominator_complete"]
        for row in raw_rows:
            for field, key in (("FromDeliverableID", "_from_id_norm"), ("TargetDeliverableID", "_target_id_norm")):
                raw = row[field]
                value, changed = normalize_id(raw) if normalize_ids else (raw.strip(), False)
                row[key] = value
                if changed:
                    normalizations.append({"original": raw, "normalized": value, "field": field, "file": str(path), "record": row["_record"]})
            row["_eligible"] = not bad_header and not row["_issues"]
            rows.append(row)
    return rows, reports, normalizations


def build_graph(rows, active_only=True, dependency_class="EXECUTION", target_type="DELIVERABLE"):
    graph, reverse, nodes = defaultdict(set), defaultdict(set), set()
    for row in rows:
        if not row.get("_eligible", True):
            continue
        if row.get("DependencyClass", "").strip() != dependency_class or row.get("TargetType", "").strip() != target_type:
            continue
        if active_only and row.get("Status", "").strip() != "ACTIVE":
            continue
        source, target = row["_from_id_norm"], row["_target_id_norm"]
        if not source or not target or row.get("Direction", "").strip() not in {"UPSTREAM", "DOWNSTREAM"}:
            continue
        if row["Direction"].strip() == "DOWNSTREAM":
            source, target = target, source
        graph[source].add(target)
        reverse[target].add(source)
        nodes.update((source, target))
    return graph, reverse, nodes


def find_sccs(graph, nodes):
    """Iterative Kosaraju traversal, including self-loops and large graphs."""
    visited, order = set(), []
    for origin in sorted(nodes):
        if origin in visited:
            continue
        visited.add(origin)
        stack = [(origin, iter(sorted(graph.get(origin, ())))) ]
        while stack:
            node, children = stack[-1]
            child = next(children, None)
            if child is None:
                order.append(node)
                stack.pop()
            elif child not in visited:
                visited.add(child)
                stack.append((child, iter(sorted(graph.get(child, ())))))
    reverse = defaultdict(set)
    for source, targets in graph.items():
        for target in targets:
            reverse[target].add(source)
    visited, components = set(), []
    for origin in reversed(order):
        if origin in visited:
            continue
        component, stack = [], [origin]
        visited.add(origin)
        while stack:
            node = stack.pop()
            component.append(node)
            for child in sorted(reverse.get(node, ())):
                if child not in visited:
                    visited.add(child)
                    stack.append(child)
        if len(component) > 1 or origin in graph.get(origin, ()):
            components.append(sorted(component))
    return sorted(components)


def representative_cycles(graph, components, maximum):
    """One deterministic representative per SCC, bounded by maximum."""
    cycles = []
    for component in components[:maximum]:
        start, allowed = component[0], set(component)
        if start in graph.get(start, ()):
            cycles.append([start, start])
            continue
        queue = deque((child, [start, child]) for child in sorted(graph.get(start, ())) if child in allowed)
        visited = {start}
        while queue:
            node, path = queue.popleft()
            if start in graph.get(node, ()):
                cycles.append(path + [start])
                break
            if node in visited:
                continue
            visited.add(node)
            for child in sorted(graph.get(node, ())):
                if child in allowed and child not in visited:
                    queue.append((child, path + [child]))
    return cycles


def find_orphans(graph, reverse, all_deliverable_ids):
    """Historical function name: returns isolated units, not unresolved targets."""
    connected = {node for node in graph if graph[node]} | {node for node in reverse if reverse[node]}
    connected.update(target for targets in graph.values() for target in targets)
    return sorted(set(all_deliverable_ids) - connected)


def find_hubs(graph, reverse, threshold):
    nodes = set(graph) | set(reverse)
    hubs = [{"node": node, "in_degree": len(reverse.get(node, ())), "out_degree": len(graph.get(node, ())),
             "total": len(reverse.get(node, ())) + len(graph.get(node, ()))} for node in nodes]
    return sorted((item for item in hubs if item["total"] >= threshold), key=lambda item: (-item["total"], item["node"]))


def find_bidirectional_pairs(graph):
    return sorted({tuple(sorted((source, target))) for source, targets in graph.items() for target in targets if source != target and source in graph.get(target, ())})


def select_units(root, scope):
    units = inventory(root)
    if scope == ["ALL"]:
        return units, units
    if "ALL" in scope:
        raise ValueError("ALL cannot be combined with other scope selectors")
    selected = set()
    for selector in scope:
        candidate = (root / selector).resolve()
        matches = [unit for unit in units if selector in {unit.name.split("_")[0], unit.parent.parent.name.split("_")[0]} or candidate in {unit.resolve(), unit.parent.parent.resolve(), (unit / "Dependencies.csv").resolve()}]
        if not matches:
            raise ValueError(f"scope selector matches no production units: {selector}")
        selected.update(matches)
    return sorted(selected), units


def analyze(root, scope=None, active_only=True, normalize_ids=True, dependency_class="EXECUTION", target_type="DELIVERABLE", hub_threshold=20, max_cycles=10000):
    root = require_root(Path(root))
    selected, all_units = select_units(root, scope or ["ALL"])
    paths = [str(unit / "Dependencies.csv") for unit in selected if (unit / "Dependencies.csv").is_file()]
    rows, reports, normalizations = load_all_edges(paths, normalize_ids)
    ids = {unit.name.split("_")[0] for unit in selected}
    if len(ids) != len(selected):
        raise ValueError("duplicate production-unit IDs in selected inventory")
    workspace_ids = {unit.name.split("_")[0] for unit in all_units}
    issues = []
    for unit in selected:
        key = unit.name.split("_")[0]
        if key not in reports:
            reports[key] = {"path": str(unit / "Dependencies.csv"), "valid": False, "rows": 0, "issues": ["missing register"], "row_findings": [], "implements_node_rows": 0}
        info = reports[key]
        if not info["valid"]:
            issues.append({"check": "schema", "unit": key, "path": info["path"], "issues": info["issues"], "row_findings": info["row_findings"]})
    for row in rows:
        source = row["_from_id_norm"]
        if source not in ids:
            row["_eligible"] = False
            issues.append({"check": "missing_source", "source": source, "path": row["_source_file"], "record": row["_record"]})
    graph, reverse, graph_nodes = build_graph(rows, active_only, dependency_class, target_type)
    orphan_rows, outside_rows = [], []
    for row in rows:
        if not row["_eligible"] or row["DependencyClass"].strip() != dependency_class or row["TargetType"].strip() != target_type or (active_only and row["Status"].strip() != "ACTIVE"):
            continue
        target = row["_target_id_norm"]
        evidence = {"FromDeliverableID": row["_from_id_norm"], "TargetDeliverableID": target,
            "DependencyID": row["DependencyID"], "Evidence": row["_source_file"], "Record": row["_record"], "Status": row["Status"]}
        if target not in workspace_ids:
            orphan_rows.append(evidence)
        elif target not in ids:
            outside_rows.append(evidence)
    components = find_sccs(graph, graph_nodes | ids)
    cycles = representative_cycles(graph, components, max_cycles)
    isolated = find_orphans(graph, reverse, ids)
    hubs = find_hubs(graph, reverse, hub_threshold)
    bidirectional = find_bidirectional_pairs(graph)
    coverage = [{"DeliverableID": key, "HasDependencyCsv": "Y" if Path(info["path"]).is_file() else "N", "RowCount": info["rows"], "SchemaValid": "Y" if info["valid"] else "N", "HasImplementsNode": "Y" if info["implements_node_rows"] else "N"} for key, info in sorted(reports.items())]
    summary = {"schema_version": 2, "run_status": "COMPLETE", "subject_status": "FAIL" if issues or orphan_rows or components else "PASS" if selected else "NOT_ASSESSED",
        "scope": scope or ["ALL"], "filters": {"active_only": active_only, "normalize_ids": normalize_ids, "dependency_class": dependency_class, "target_type": target_type, "hub_threshold": hub_threshold, "max_cycles": max_cycles},
        "total_files": len(paths), "total_rows": sum(info["rows"] for info in reports.values()), "production_units": len(ids),
        "schema_valid": sum(info["valid"] for info in reports.values()), "schema_invalid": sum(not info["valid"] for info in reports.values()),
        "anchor_rows": sum(row["DependencyClass"].strip() == "ANCHOR" for row in rows), "execution_rows": sum(row["DependencyClass"].strip() == "EXECUTION" for row in rows),
        "implements_node_present": sum(info["implements_node_rows"] > 0 for info in reports.values()), "implements_node_missing": sum(info["implements_node_rows"] == 0 for info in reports.values()),
        "evidence_populated": sum(bool(row["EvidenceFile"].strip()) for row in rows), "evidence_total": sum(info["rows"] for info in reports.values()),
        "denominator_complete": all(info.get("denominator_complete", True) for info in reports.values()),
        "graph_nodes": len(graph_nodes | ids), "graph_edges": sum(len(targets) for targets in graph.values()),
        "orphan_count": len(orphan_rows), "isolated_count": len(isolated), "outside_scope_count": len(outside_rows),
        "scc_count": len(components), "scc_sizes": [len(component) for component in components], "representative_cycles": len(cycles), "cycles_truncated": len(cycles) < len(components),
        "hub_count": len(hubs), "bidirectional_pair_count": len(bidirectional), "normalization_count": len(normalizations), "issues": issues}
    misplaced = sum(row["TargetType"].strip() != "DELIVERABLE" and bool(row["TargetDeliverableID"].strip()) for row in rows)
    invalid_ids = [{"field": field, "value": row[field], "path": row["_source_file"], "record": row["_record"]}
        for row in rows for field in ("FromDeliverableID", "TargetDeliverableID")
        if row[field].strip() and not ID_PATTERN.fullmatch(row[field].strip())]
    summary["misplaced_field_count"] = misplaced
    summary["invalid_ids"] = invalid_ids
    summary["checks"] = {
        "schema_compliance": "BLOCKER" if summary["schema_invalid"] else "PASS",
        "orphan_dependencies": "BLOCKER" if orphan_rows else "PASS",
        "circular_dependencies": "BLOCKER" if components else "PASS",
        "anchor_coverage": "WARNING" if summary["implements_node_missing"] else "PASS",
        "misplaced_fields": "BLOCKER" if misplaced else "PASS",
        "id_format_consistency": "WARNING" if normalizations or invalid_ids else "PASS",
        "isolated_units": "WARNING" if isolated else "PASS",
        "hubs": "WARNING" if hubs else "PASS",
        "bidirectional_pairs": "INFO" if bidirectional else "PASS",
    }
    return summary, {"orphans": orphan_rows, "outside_scope": outside_rows, "isolated": isolated, "sccs": components, "cycles": cycles, "hubs": hubs, "bidirectional": bidirectional, "coverage": coverage, "normalizations": normalizations}


def boolean(value):
    if value.lower() not in {"true", "false"}:
        raise argparse.ArgumentTypeError("expected true or false")
    return value.lower() == "true"


def write_csv(output, name, headers, rows):
    with (output / name).open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(headers)
        writer.writerows(rows)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("execution_root", type=Path)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--scope", nargs="+", default=["ALL"])
    parser.add_argument("--filter-active-only", type=boolean, default=True)
    parser.add_argument("--normalize-ids", type=boolean, default=True)
    parser.add_argument("--dependency-class", choices=sorted(schema.CANONICAL_ENUMS["DependencyClass"]), default="EXECUTION")
    parser.add_argument("--target-type", choices=["DELIVERABLE"], default="DELIVERABLE", help="Topology requires production-unit target IDs")
    parser.add_argument("--hub-threshold", type=int, default=20)
    parser.add_argument("--max-cycles", type=int, default=10000)
    parser.add_argument("--prior-summary", type=Path, help="Explicit prior closure_summary.json for comparison")
    args = parser.parse_args(argv)
    try:
        if args.hub_threshold < 1 or args.max_cycles < 0:
            raise ValueError("hub threshold must be positive; max cycles must be nonnegative")
        summary, data = analyze(args.execution_root, args.scope, args.filter_active_only, args.normalize_ids, args.dependency_class, args.target_type, args.hub_threshold, args.max_cycles)
        if args.prior_summary:
            prior = json.loads(args.prior_summary.read_text(encoding="utf-8"))
            if not isinstance(prior, dict):
                raise ValueError("prior summary must be an object")
            comparable = ("total_files", "total_rows", "graph_nodes", "graph_edges", "scc_count", "hub_count")
            summary["comparison"] = {"basis": str(args.prior_summary), "deltas": {key: summary[key] - prior[key] for key in comparable if isinstance(prior.get(key), int)}}
        if args.output_dir:
            output = args.output_dir.resolve()
            if "1_Working" in output.parts:
                raise ValueError("output directory must be outside production-unit source paths")
            output.mkdir(parents=True, exist_ok=True)
            (output / "closure_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            fields = ["FromDeliverableID", "TargetDeliverableID", "DependencyID", "Evidence", "Record", "Status"]
            for name in ("orphans", "outside_scope"):
                write_csv(output, name + ".csv", fields, [[row[field] for field in fields] for row in data[name]])
            write_csv(output, "isolated.csv", ["DeliverableID"], [[value] for value in data["isolated"]])
            write_csv(output, "scc_summary.csv", ["SCC_ID", "Size", "Nodes"], [[f"SCC-{index:03d}", len(component), ";".join(component)] for index, component in enumerate(data["sccs"], 1)])
            write_csv(output, "cycles_sample.csv", ["Cycle_ID", "Nodes"], [[f"CYCLE-{index:05d}", ";".join(cycle)] for index, cycle in enumerate(data["cycles"], 1)])
            write_csv(output, "hubs.csv", ["DeliverableID", "InDegree", "OutDegree", "TotalDegree"], [[row[key] for key in ("node", "in_degree", "out_degree", "total")] for row in data["hubs"]])
            write_csv(output, "bidirectional_pairs.csv", ["NodeA", "NodeB"], data["bidirectional"])
            fields = ["DeliverableID", "HasDependencyCsv", "RowCount", "SchemaValid", "HasImplementsNode"]
            write_csv(output, "coverage.csv", fields, [[row[field] for field in fields] for row in data["coverage"]])
            write_csv(output, "id_normalization.csv", ["Original", "Normalized", "Field", "File", "Record"], [[row[key] for key in ("original", "normalized", "field", "file", "record")] for row in data["normalizations"]])
        print(json.dumps(summary, indent=2, sort_keys=True))
        return 0
    except (OSError, ValueError) as exc:
        print(json.dumps({"schema_version": 2, "run_status": "FAILED_INPUTS", "subject_status": "NOT_ASSESSED", "issues": [str(exc)]}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
