from __future__ import annotations

import csv
import sys
from pathlib import Path


COORDINATION_DIR = Path(__file__).resolve().parent
if str(COORDINATION_DIR) not in sys.path:
    sys.path.insert(0, str(COORDINATION_DIR))

from audit_dag import ACTIVE, CANDIDATE, ARCHITECTURE_BASIS, REQUIRED_COLUMNS, audit_dag, strict_passed  # noqa: E402
from materialize_local_dependencies import materialize_local_dependencies  # noqa: E402


NODE_COLUMNS = ["NodeID", "PackageID", "DeliverableID", "DeliverableName", "ExecutionPath"]


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def node(deliverable_id: str, package_id: str, name: str, execution_path: Path | None = None) -> dict[str, str]:
    return {
        "NodeID": deliverable_id,
        "PackageID": package_id,
        "DeliverableID": deliverable_id,
        "DeliverableName": name,
        "ExecutionPath": str(execution_path or ""),
    }


def edge(
    dependency_id: str,
    from_package: str,
    from_deliverable: str,
    target_package: str,
    target_deliverable: str,
    status: str = ACTIVE,
    dependency_type: str = "DOMAIN_MODEL",
) -> dict[str, str]:
    row = {column: "" for column in REQUIRED_COLUMNS}
    row.update({
        "RegisterSchemaVersion": "v3.1",
        "DependencyID": dependency_id,
        "FromPackageID": from_package,
        "FromDeliverableID": from_deliverable,
        "FromDeliverableName": f"{from_deliverable} name",
        "DependencyClass": "EXECUTION",
        "AnchorType": "DELIVERABLE",
        "Direction": "UPSTREAM",
        "DependencyType": dependency_type,
        "TargetType": "DELIVERABLE",
        "TargetPackageID": target_package,
        "TargetDeliverableID": target_deliverable,
        "TargetRefID": target_deliverable,
        "TargetName": f"{target_deliverable} name",
        "Statement": f"{from_deliverable} depends on {target_deliverable}",
        "EvidenceFile": "_CONTEXT.md",
        "SourceRef": "fixture",
        "EvidenceQuote": "fixture evidence",
        "Explicitness": "EXPLICIT",
        "RequiredMaturity": "SEMANTIC_READY",
        "ProposedMaturity": "SEMANTIC_READY",
        "SatisfactionStatus": "UNKNOWN",
        "Confidence": "HIGH",
        "Origin": "TEST",
        "FirstSeen": "2026-04-30",
        "LastSeen": "2026-04-30",
        "Status": status,
        "Notes": "fixture",
    })
    return row


def read_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def test_aggregate_dag_audit_reports_fixture_hygiene_findings(tmp_path: Path) -> None:
    nodes_path = tmp_path / "DeliverableNodes.csv"
    edges_path = tmp_path / "DependencyEdges.csv"
    write_csv(nodes_path, [
        node("DEL-00-01", "PKG-00", "Architecture basis"),
        node("DEL-01-01", "PKG-01", "A"),
        node("DEL-01-02", "PKG-01", "B"),
        node("DEL-02-01", "PKG-02", "C"),
    ], NODE_COLUMNS)
    write_csv(edges_path, [
        edge("DAG-TEST-E0001", "PKG-01", "DEL-01-01", "PKG-01", "DEL-01-02"),
        edge("DAG-TEST-E0002", "PKG-01", "DEL-01-01", "PKG-01", "DEL-01-02"),
        edge("DAG-TEST-E0003", "PKG-01", "DEL-01-02", "PKG-01", "DEL-01-01"),
        edge("DAG-TEST-E0004", "PKG-01", "DEL-01-01", "PKG-02", "DEL-99-99"),
        edge("DAG-TEST-E0005", "PKG-02", "DEL-02-01", "PKG-01", "DEL-01-01", status=CANDIDATE),
        edge(
            "DAG-TEST-E0006",
            "PKG-01",
            "DEL-01-01",
            "PKG-00",
            "DEL-00-01",
            dependency_type=ARCHITECTURE_BASIS,
        ),
    ], REQUIRED_COLUMNS)

    summary = audit_dag(edges_path=edges_path, nodes_path=nodes_path, hub_threshold=1)

    assert summary["edge_schema"]["valid"] is True
    assert summary["active_edge_count"] == 5
    assert summary["candidate_edge_count"] == 1
    assert summary["endpoint_issue_count"] == 1
    assert summary["active_graph"]["scc_count"] == 1
    assert summary["active_graph"]["duplicate_edge_count"] == 1
    assert summary["active_graph"]["bidirectional_pair_count"] == 1
    assert summary["dev001_projection"]["active_edge_count"] == 4
    assert strict_passed(summary) is False


def test_materializer_writes_non_pkg00_mirrors_and_preserves_rows(tmp_path: Path) -> None:
    execution_root = tmp_path / "execution"
    pkg00_path = execution_root / "PKG-00" / "1_Working" / "DEL-00-01_Architecture basis"
    del0101_path = execution_root / "PKG-01" / "1_Working" / "DEL-01-01_Project governance baseline"
    del0102_path = execution_root / "PKG-01" / "1_Working" / "DEL-01-02_Copyright policy"
    pkg00_path.mkdir(parents=True)
    del0101_path.mkdir(parents=True)
    del0102_path.mkdir(parents=True)

    nodes_path = tmp_path / "DeliverableNodes.csv"
    edges_path = tmp_path / "DependencyEdges.csv"
    write_csv(nodes_path, [
        node("DEL-00-01", "PKG-00", "Architecture basis", pkg00_path),
        node("DEL-01-01", "PKG-01", "Project governance baseline", del0101_path),
        node("DEL-01-02", "PKG-01", "Copyright policy", del0102_path),
    ], NODE_COLUMNS)
    write_csv(edges_path, [
        edge(
            "DAG-001-E0002",
            "PKG-01",
            "DEL-01-01",
            "PKG-01",
            "DEL-01-02",
            status=CANDIDATE,
        ),
        edge(
            "DAG-001-E0001",
            "PKG-01",
            "DEL-01-01",
            "PKG-00",
            "DEL-00-01",
            dependency_type=ARCHITECTURE_BASIS,
        ),
        edge("DAG-001-E0003", "PKG-00", "DEL-00-01", "PKG-01", "DEL-01-01"),
        edge("DAG-001-E0004", "PKG-01", "DEL-01-02", "PKG-01", "DEL-01-01"),
    ], REQUIRED_COLUMNS)

    summary = materialize_local_dependencies(
        edges_path=edges_path,
        nodes_path=nodes_path,
        execution_root=execution_root,
        refresh_pointers=True,
        generated_date="2026-04-30",
        source_label="DAG-001",
    )

    assert summary["written_count"] == 2
    assert summary["skipped_pkg00"] == ["DEL-00-01"]
    assert not (pkg00_path / "Dependencies.csv").exists()

    header, rows = read_rows(del0101_path / "Dependencies.csv")
    assert header == REQUIRED_COLUMNS
    assert [row["DependencyID"] for row in rows] == ["DAG-001-E0001", "DAG-001-E0002"]
    assert rows[0]["RegisterSchemaVersion"] == "v3.1"
    assert rows[0]["DependencyType"] == ARCHITECTURE_BASIS
    assert rows[1]["Status"] == CANDIDATE
    assert rows[1]["TargetDeliverableID"] == "DEL-01-02"

    _header, del0102_rows = read_rows(del0102_path / "Dependencies.csv")
    assert [row["DependencyID"] for row in del0102_rows] == ["DAG-001-E0004"]

    pointer = (del0101_path / "_DEPENDENCIES.md").read_text(encoding="utf-8")
    assert "SYNCHRONIZED_FROM_DAG_001" in pointer
    assert "CANDIDATE` rows remain non-gating" in pointer


def test_materializer_can_scope_to_selected_deliverables(tmp_path: Path) -> None:
    execution_root = tmp_path / "execution"
    del0101_path = execution_root / "PKG-01" / "1_Working" / "DEL-01-01_Project governance baseline"
    del0102_path = execution_root / "PKG-01" / "1_Working" / "DEL-01-02_Copyright policy"
    del0101_path.mkdir(parents=True)
    del0102_path.mkdir(parents=True)

    nodes_path = tmp_path / "DeliverableNodes.csv"
    edges_path = tmp_path / "DependencyEdges.csv"
    write_csv(nodes_path, [
        node("DEL-01-01", "PKG-01", "Project governance baseline", del0101_path),
        node("DEL-01-02", "PKG-01", "Copyright policy", del0102_path),
    ], NODE_COLUMNS)
    write_csv(edges_path, [
        edge("DAG-001-E0001", "PKG-01", "DEL-01-01", "PKG-01", "DEL-01-02"),
        edge("DAG-001-E0002", "PKG-01", "DEL-01-02", "PKG-01", "DEL-01-01"),
    ], REQUIRED_COLUMNS)

    summary = materialize_local_dependencies(
        edges_path=edges_path,
        nodes_path=nodes_path,
        execution_root=execution_root,
        refresh_pointers=True,
        generated_date="2026-04-30",
        source_label="DAG-001",
        deliverable_ids={"DEL-01-02"},
    )

    assert summary["written_count"] == 1
    assert summary["filtered_deliverable_ids"] == ["DEL-01-02"]
    assert not (del0101_path / "Dependencies.csv").exists()

    _header, rows = read_rows(del0102_path / "Dependencies.csv")
    assert [row["DependencyID"] for row in rows] == ["DAG-001-E0002"]
