from __future__ import annotations

import csv
import sys
from pathlib import Path


COORDINATION_DIR = Path(__file__).resolve().parent
if str(COORDINATION_DIR) not in sys.path:
    sys.path.insert(0, str(COORDINATION_DIR))

from audit_dag import ARCHITECTURE_BASIS, REQUIRED_COLUMNS  # noqa: E402
from build_dev001_blocker_queue import (  # noqa: E402
    ACTIVE,
    BLOCKED,
    CANDIDATE,
    COMMITTED,
    UNBLOCKED,
    build_queue,
)


NODE_COLUMNS = ["NodeID", "PackageID", "DeliverableID", "DeliverableName", "LifecycleState"]
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


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def node(deliverable_id: str, package_id: str = "PKG-01", name: str | None = None) -> dict[str, str]:
    return {
        "NodeID": deliverable_id,
        "PackageID": package_id,
        "DeliverableID": deliverable_id,
        "DeliverableName": name or f"{deliverable_id} name",
        "LifecycleState": "SEMANTIC_READY",
    }


def edge(
    dependency_id: str,
    from_deliverable: str,
    target_deliverable: str,
    from_package: str = "PKG-01",
    target_package: str = "PKG-01",
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
        "FirstSeen": "2026-05-01",
        "LastSeen": "2026-05-01",
        "Status": status,
        "Notes": "fixture",
    })
    return row


def evidence(deliverable_id: str, state: str = COMMITTED, package_id: str = "PKG-01") -> dict[str, str]:
    return {
        "DeliverableID": deliverable_id,
        "PackageID": package_id,
        "EvidenceState": state,
        "EvidenceKind": "FIXTURE",
        "Commit": "abc1234",
        "CommitSubject": "fixture commit",
        "CommittedDate": "2026-05-01",
        "HandoffCommit": "",
        "Notes": "fixture",
    }


def build_fixture(
    tmp_path: Path,
    nodes: list[dict[str, str]],
    edges: list[dict[str, str]],
    evidence_rows: list[dict[str, str]] | None = None,
) -> dict[str, object]:
    nodes_path = tmp_path / "DeliverableNodes.csv"
    edges_path = tmp_path / "DependencyEdges.csv"
    evidence_path = tmp_path / "DEV-001_IMPLEMENTATION_EVIDENCE.csv"
    write_csv(nodes_path, nodes, NODE_COLUMNS)
    write_csv(edges_path, edges, REQUIRED_COLUMNS)
    write_csv(evidence_path, evidence_rows or [], EVIDENCE_COLUMNS)
    return build_queue(edges_path=edges_path, nodes_path=nodes_path, evidence_path=evidence_path)


def test_from_deliverable_is_blocked_by_missing_target_evidence(tmp_path: Path) -> None:
    summary = build_fixture(
        tmp_path,
        [node("DEL-A"), node("DEL-B")],
        [edge("DAG-TEST-E0001", "DEL-A", "DEL-B")],
    )

    row = summary["queue_rows_by_id"]["DEL-A"]  # type: ignore[index]
    assert row["BlockerState"] == BLOCKED
    assert row["BlockingUpstreamDeliverables"] == "DEL-B"
    assert row["BlockingEdgeIDs"] == "DAG-TEST-E0001"


def test_committed_upstream_evidence_unblocks_downstream_item(tmp_path: Path) -> None:
    summary = build_fixture(
        tmp_path,
        [node("DEL-A"), node("DEL-B")],
        [edge("DAG-TEST-E0001", "DEL-A", "DEL-B")],
        [evidence("DEL-B")],
    )

    row = summary["queue_rows_by_id"]["DEL-A"]  # type: ignore[index]
    assert row["BlockerState"] == UNBLOCKED
    assert row["SatisfiedUpstreamCount"] == "1"
    assert row["BlockingUpstreamCount"] == "0"


def test_candidate_edges_are_ignored_for_blocker_computation(tmp_path: Path) -> None:
    summary = build_fixture(
        tmp_path,
        [node("DEL-A"), node("DEL-B")],
        [edge("DAG-TEST-E0001", "DEL-A", "DEL-B", status=CANDIDATE)],
    )

    row = summary["queue_rows_by_id"]["DEL-A"]  # type: ignore[index]
    assert row["BlockerState"] == UNBLOCKED
    assert row["ActiveUpstreamCount"] == "0"
    assert summary["candidate_edge_count"] == 1


def test_pkg00_architecture_basis_edges_are_satisfied_without_implementation_evidence(tmp_path: Path) -> None:
    summary = build_fixture(
        tmp_path,
        [node("DEL-A"), node("DEL-00-01", package_id="PKG-00")],
        [
            edge(
                "DAG-TEST-E0001",
                "DEL-A",
                "DEL-00-01",
                target_package="PKG-00",
                dependency_type=ARCHITECTURE_BASIS,
            )
        ],
    )

    row = summary["queue_rows_by_id"]["DEL-A"]  # type: ignore[index]
    assert row["BlockerState"] == UNBLOCKED
    assert row["SatisfiedUpstreamCount"] == "1"
    assert summary["architecture_basis_satisfied_edges"] == 1


def test_semantic_only_upstreams_do_not_satisfy_implementation_dependencies(tmp_path: Path) -> None:
    summary = build_fixture(
        tmp_path,
        [node("DEL-A"), node("DEL-B")],
        [edge("DAG-TEST-E0001", "DEL-A", "DEL-B")],
        [evidence("DEL-B", state="SEMANTIC_READY")],
    )

    row = summary["queue_rows_by_id"]["DEL-A"]  # type: ignore[index]
    assert row["BlockerState"] == BLOCKED
    assert row["BlockingUpstreamDeliverables"] == "DEL-B"
