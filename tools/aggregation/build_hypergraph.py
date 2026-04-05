#!/usr/bin/env python3
"""
build_hypergraph.py — Deterministic DOMAIN hypergraph construction from staging CSVs.

Reads discovery evidence produced by DOMAIN_HYPERGRAPH agent (Steps 0-3); writes
normalized hypergraph tables + QA report into an existing snapshot directory.

READS (from --staging-dir, which is typically {snapshot}/Evidence/):
  discovered_categories.csv         (REQUIRED)
  discovered_knowledge_types.csv    (REQUIRED)
  discovered_knowledge_subjects.csv (conditional — skip KNOWLEDGE_SUBJECT nodes + HAS_SUBJECT edges if absent)
  artifact_enumeration.csv          (conditional — skip KNOWLEDGE_ARTIFACT nodes + HAS_ARTIFACT edges if absent)
  subject_artifact_mapping.csv      (conditional — skip SUBJECT_MATERIALIZED_AS edges if absent)
  discovered_ledger_rows.csv        (optional — skip ATOMIC_UNIT nodes + LEDGER_ROW edges if absent)
  discovered_objectives.csv         (optional — skip OBJECTIVE nodes if absent)
  kty_supports_obj.csv              (optional — skip KTY_SUPPORTS_OBJ edges if absent)

WRITES (to --output-dir):
  nodes.csv
  hyperedges.csv
  incidence.csv
  hypergraph.json
  QA_Report.md

DETERMINISM:
  Same staging inputs -> byte-identical CSVs + canonical JSON (excluding generated_at).
  HyperedgeID = HGE-{Type}-{SHA1(canonical)[:12]}
  canonical = Type + "|" + "|".join(sorted("{Role}:{NodeID}" for incidences)) + "|" + SourcePath + "|" + SourceRef
  CSV rows sorted by primary key; incidence sorted by (HyperedgeID, Role, NodeID, Ordinal).
  List fields (KnowledgeTypeIDs, ObjectiveIDs) normalized: trim, dedupe, sort ascending.

NON-SCOPE:
  Does NOT invoke scaffold_tool_root.sh, create_snapshot_folder.sh, or update_latest_pointer.sh.
  Snapshot directory must already exist. Agent orchestrates scaffolding + pointer updates.
"""

import argparse
import csv
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

SCHEMA_VERSION = "HG.v1.0"

NODE_COLUMNS = [
    "SchemaVersion", "NodeID", "NodeType", "Label", "SourcePath", "SourceRef", "Notes",
    "NormalizedID", "Tags", "Variant",
]

HYPEREDGE_COLUMNS = [
    "SchemaVersion", "HyperedgeID", "HyperedgeType", "SourcePath", "SourceRef", "Notes", "Tags", "Label",
]

INCIDENCE_COLUMNS = [
    "SchemaVersion", "HyperedgeID", "NodeID", "Role", "Ordinal", "Notes",
]

VALID_EDGE_TYPES = [
    "IN_CATEGORY",
    "HAS_SUBJECT",
    "HAS_ARTIFACT",
    "SUBJECT_MATERIALIZED_AS",
    "LEDGER_ROW",
    "KTY_SUPPORTS_OBJ",
]


# ─── I/O helpers ──────────────────────────────────────────────────────────────

def read_csv_rows(path: Path) -> List[Dict[str, str]]:
    """Read a CSV file into a list of dict rows. Empty list if file absent."""
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return [{k: (v or "") for k, v in row.items()} for row in reader]


def write_csv(path: Path, columns: List[str], rows: List[Dict[str, str]]) -> None:
    """Write rows to CSV with fixed column ordering. Missing fields default to empty."""
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({col: row.get(col, "") for col in columns})


def normalize_list_field(value: str) -> List[str]:
    """Trim, dedupe, sort semicolon-separated list. Empty string -> empty list."""
    if not value:
        return []
    items = [s.strip() for s in value.split(";") if s.strip()]
    return sorted(set(items))


# ─── Node construction ────────────────────────────────────────────────────────

def build_category_nodes(rows: List[Dict[str, str]], variant: str) -> List[Dict[str, str]]:
    nodes = []
    for row in rows:
        cat_id = row.get("CategoryID", "").strip()
        if not cat_id:
            continue  # No invention; skip rows without IDs
        nodes.append({
            "SchemaVersion": SCHEMA_VERSION,
            "NodeID": cat_id,
            "NodeType": "CATEGORY",
            "Label": row.get("CategoryName", "") or "TBD",
            "SourcePath": row.get("SourcePath", ""),
            "SourceRef": row.get("SourceRef", ""),
            "Notes": row.get("Notes", ""),
            "Variant": variant,
        })
    return nodes


def build_knowledge_type_nodes(rows: List[Dict[str, str]], variant: str, normalize_ids: bool) -> List[Dict[str, str]]:
    nodes = []
    for row in rows:
        kty_id = row.get("KnowledgeTypeID", "").strip()
        if not kty_id:
            continue
        notes_parts = []
        for extra_field in ("Discipline", "Type", "Responsible", "Description", "DecompositionRef"):
            val = row.get(extra_field, "").strip()
            if val:
                notes_parts.append(f"{extra_field}={val}")
        base_notes = row.get("Notes", "").strip()
        if base_notes:
            notes_parts.insert(0, base_notes)
        node = {
            "SchemaVersion": SCHEMA_VERSION,
            "NodeID": kty_id,
            "NodeType": "KNOWLEDGE_TYPE",
            "Label": row.get("Name", "") or "TBD",
            "SourcePath": row.get("SourcePath", ""),
            "SourceRef": row.get("SourceRef", ""),
            "Notes": " | ".join(notes_parts),
            "Variant": variant,
        }
        if normalize_ids:
            node["NormalizedID"] = _normalize_id(kty_id)
        nodes.append(node)
    return nodes


def build_subject_nodes(rows: List[Dict[str, str]], variant: str) -> List[Dict[str, str]]:
    nodes = []
    for row in rows:
        subject_id = row.get("SubjectID", "").strip()
        if not subject_id:
            continue
        nodes.append({
            "SchemaVersion": SCHEMA_VERSION,
            "NodeID": subject_id,
            "NodeType": "KNOWLEDGE_SUBJECT",
            "Label": row.get("SubjectName", "") or "TBD",
            "SourcePath": row.get("SourcePath", ""),
            "SourceRef": row.get("SourceRef", ""),
            "Notes": row.get("Notes", ""),
            "Variant": variant,
        })
    return nodes


def build_artifact_nodes(rows: List[Dict[str, str]], variant: str) -> List[Dict[str, str]]:
    nodes = []
    for row in rows:
        artifact_id = row.get("ArtifactID", "").strip()
        if not artifact_id:
            continue
        notes_parts = []
        src = row.get("ArtifactSource", "").strip()
        if src:
            notes_parts.append(f"ArtifactSource={src}")
        filename = row.get("Filename", "").strip()
        if filename:
            notes_parts.append(f"Filename={filename}")
        base_notes = row.get("Notes", "").strip()
        if base_notes:
            notes_parts.insert(0, base_notes)
        nodes.append({
            "SchemaVersion": SCHEMA_VERSION,
            "NodeID": artifact_id,
            "NodeType": "KNOWLEDGE_ARTIFACT",
            "Label": row.get("ArtifactLabel", "") or filename or "TBD",
            "SourcePath": row.get("SourcePath", ""),
            "SourceRef": row.get("SourceRef", ""),
            "Notes": " | ".join(notes_parts),
            "Variant": variant,
        })
    return nodes


def build_atomic_unit_nodes(ledger_rows: List[Dict[str, str]], variant: str) -> List[Dict[str, str]]:
    nodes = []
    seen: Set[str] = set()
    for row in ledger_rows:
        unit_id = row.get("AtomicUnitID", "").strip()
        if not unit_id or unit_id in seen:
            continue
        seen.add(unit_id)
        nodes.append({
            "SchemaVersion": SCHEMA_VERSION,
            "NodeID": unit_id,
            "NodeType": "ATOMIC_UNIT",
            "Label": row.get("UnitStatement", "") or "TBD",
            "SourcePath": row.get("SourcePath", ""),
            "SourceRef": row.get("SourceRef", ""),
            "Notes": row.get("Notes", ""),
            "Variant": variant,
        })
    return nodes


def build_objective_nodes(rows: List[Dict[str, str]], variant: str) -> List[Dict[str, str]]:
    nodes = []
    for row in rows:
        obj_id = row.get("ObjectiveID", "").strip()
        if not obj_id:
            continue
        nodes.append({
            "SchemaVersion": SCHEMA_VERSION,
            "NodeID": obj_id,
            "NodeType": "OBJECTIVE",
            "Label": row.get("Label", "") or "TBD",
            "SourcePath": row.get("SourcePath", ""),
            "SourceRef": row.get("SourceRef", ""),
            "Notes": row.get("Notes", ""),
            "Variant": variant,
        })
    return nodes


def _normalize_id(node_id: str) -> str:
    """Strip trailing descriptive suffix after last underscore (analysis-only)."""
    if "_" in node_id:
        prefix, _, _suffix = node_id.rpartition("_")
        if prefix:
            return prefix
    return node_id


# ─── Hyperedge construction ───────────────────────────────────────────────────

def compute_hyperedge_id(edge_type: str, incidences: List[Tuple[str, str]], source_path: str, source_ref: str) -> str:
    """
    Deterministic ID: sort incidences by (Role, NodeID) ascending, serialize canonical string, SHA1[:12].

    canonical = edge_type + "|" + "|".join(sorted(f"{role}:{node_id}" ...)) + "|" + source_path + "|" + source_ref
    """
    sorted_incidences = sorted(incidences, key=lambda x: (x[1], x[0]))  # (Role, NodeID)
    incidence_tokens = "|".join(f"{role}:{node_id}" for node_id, role in sorted_incidences)
    canonical = f"{edge_type}|{incidence_tokens}|{source_path}|{source_ref}"
    digest = hashlib.sha1(canonical.encode("utf-8")).hexdigest()[:12]
    return f"HGE-{edge_type}-{digest}"


class HyperedgeBuilder:
    """Accumulates hyperedges + incidence rows. Handles dedupe + ordinal assignment."""

    def __init__(self):
        self.edges: List[Dict[str, str]] = []
        self.incidences: List[Dict[str, str]] = []
        self._seen_edge_ids: Set[str] = set()

    def add_edge(
        self,
        edge_type: str,
        incidences: List[Tuple[str, str]],  # list of (node_id, role)
        source_path: str,
        source_ref: str,
        notes: str = "",
    ) -> Optional[str]:
        """Add one hyperedge with its incidences. Returns HyperedgeID, or None if dedupe collision."""
        edge_id = compute_hyperedge_id(edge_type, incidences, source_path, source_ref)
        if edge_id in self._seen_edge_ids:
            return edge_id  # Idempotent: same canonical string -> same ID -> skip
        self._seen_edge_ids.add(edge_id)

        self.edges.append({
            "SchemaVersion": SCHEMA_VERSION,
            "HyperedgeID": edge_id,
            "HyperedgeType": edge_type,
            "SourcePath": source_path,
            "SourceRef": source_ref,
            "Notes": notes,
        })

        # Ordinals assigned by sorted (Role, NodeID) order — deterministic
        sorted_incidences = sorted(incidences, key=lambda x: (x[1], x[0]))
        for ordinal, (node_id, role) in enumerate(sorted_incidences):
            self.incidences.append({
                "SchemaVersion": SCHEMA_VERSION,
                "HyperedgeID": edge_id,
                "NodeID": node_id,
                "Role": role,
                "Ordinal": str(ordinal),
                "Notes": "",
            })
        return edge_id


def build_hyperedges(
    kty_rows: List[Dict[str, str]],
    subject_rows: List[Dict[str, str]],
    artifact_rows: List[Dict[str, str]],
    mapping_rows: List[Dict[str, str]],
    ledger_rows: List[Dict[str, str]],
    kty_supports_obj_rows: List[Dict[str, str]],
    node_ids_by_type: Dict[str, Set[str]],
    edgeset: List[str],
    qa_findings: List[Dict[str, str]],
) -> HyperedgeBuilder:
    builder = HyperedgeBuilder()
    all_node_ids = set().union(*node_ids_by_type.values())

    # 5A: IN_CATEGORY
    if "IN_CATEGORY" in edgeset:
        for row in kty_rows:
            kty_id = row.get("KnowledgeTypeID", "").strip()
            cat_id = row.get("CategoryID", "").strip()
            if not kty_id:
                continue
            if not cat_id:
                qa_findings.append({
                    "level": "WARNING",
                    "code": "KTY_WITHOUT_CATEGORY",
                    "detail": f"KnowledgeType {kty_id} has no CategoryID",
                    "source_path": row.get("SourcePath", ""),
                    "source_ref": row.get("SourceRef", ""),
                })
                continue
            if cat_id not in node_ids_by_type.get("CATEGORY", set()):
                qa_findings.append({
                    "level": "WARNING",
                    "code": "CATEGORY_REF_MISSING_NODE",
                    "detail": f"KnowledgeType {kty_id} references CategoryID={cat_id} which has no CATEGORY node",
                    "source_path": row.get("SourcePath", ""),
                    "source_ref": row.get("SourceRef", ""),
                })
                continue
            builder.add_edge(
                "IN_CATEGORY",
                incidences=[(cat_id, "PARENT_CATEGORY"), (kty_id, "CHILD_KNOWLEDGE_TYPE")],
                source_path=row.get("SourcePath", ""),
                source_ref=row.get("SourceRef", ""),
            )

    # 5B: HAS_SUBJECT
    if "HAS_SUBJECT" in edgeset:
        for row in subject_rows:
            subject_id = row.get("SubjectID", "").strip()
            kty_id = row.get("KnowledgeTypeID", "").strip()
            if not subject_id or not kty_id:
                continue
            if kty_id not in node_ids_by_type.get("KNOWLEDGE_TYPE", set()):
                qa_findings.append({
                    "level": "WARNING",
                    "code": "SUBJECT_REF_MISSING_KTY",
                    "detail": f"Subject {subject_id} references KnowledgeTypeID={kty_id} which has no KNOWLEDGE_TYPE node",
                    "source_path": row.get("SourcePath", ""),
                    "source_ref": row.get("SourceRef", ""),
                })
                continue
            builder.add_edge(
                "HAS_SUBJECT",
                incidences=[(kty_id, "OWNER_KNOWLEDGE_TYPE"), (subject_id, "SUBJECT")],
                source_path=row.get("SourcePath", ""),
                source_ref=row.get("SourceRef", ""),
            )

    # 5C: HAS_ARTIFACT
    if "HAS_ARTIFACT" in edgeset:
        for row in artifact_rows:
            artifact_id = row.get("ArtifactID", "").strip()
            kty_id = row.get("KnowledgeTypeID", "").strip()
            if not artifact_id or not kty_id:
                continue
            if kty_id not in node_ids_by_type.get("KNOWLEDGE_TYPE", set()):
                qa_findings.append({
                    "level": "WARNING",
                    "code": "ARTIFACT_REF_MISSING_KTY",
                    "detail": f"Artifact {artifact_id} references KnowledgeTypeID={kty_id} which has no KNOWLEDGE_TYPE node",
                    "source_path": row.get("SourcePath", ""),
                    "source_ref": row.get("SourceRef", ""),
                })
                continue
            builder.add_edge(
                "HAS_ARTIFACT",
                incidences=[(kty_id, "OWNER_KNOWLEDGE_TYPE"), (artifact_id, "ARTIFACT")],
                source_path=row.get("SourcePath", ""),
                source_ref=row.get("SourceRef", ""),
            )

    # 5D: SUBJECT_MATERIALIZED_AS
    if "SUBJECT_MATERIALIZED_AS" in edgeset:
        for row in mapping_rows:
            subject_id = row.get("SubjectID", "").strip()
            artifact_id = row.get("ArtifactID", "").strip()
            if not subject_id or not artifact_id:
                qa_findings.append({
                    "level": "WARNING",
                    "code": "SUBJECT_ARTIFACT_MAPPING_INCOMPLETE",
                    "detail": f"Mapping row has incomplete SubjectID/ArtifactID (SubjectID={subject_id}, ArtifactID={artifact_id})",
                    "source_path": row.get("SourcePath", ""),
                    "source_ref": row.get("SourceRef", ""),
                })
                continue
            if subject_id not in node_ids_by_type.get("KNOWLEDGE_SUBJECT", set()):
                qa_findings.append({
                    "level": "WARNING",
                    "code": "MAPPING_REF_MISSING_SUBJECT",
                    "detail": f"Mapping references SubjectID={subject_id} which has no KNOWLEDGE_SUBJECT node",
                    "source_path": row.get("SourcePath", ""),
                    "source_ref": row.get("SourceRef", ""),
                })
                continue
            if artifact_id not in node_ids_by_type.get("KNOWLEDGE_ARTIFACT", set()):
                qa_findings.append({
                    "level": "WARNING",
                    "code": "MAPPING_REF_MISSING_ARTIFACT",
                    "detail": f"Mapping references ArtifactID={artifact_id} which has no KNOWLEDGE_ARTIFACT node",
                    "source_path": row.get("SourcePath", ""),
                    "source_ref": row.get("SourceRef", ""),
                })
                continue
            builder.add_edge(
                "SUBJECT_MATERIALIZED_AS",
                incidences=[(subject_id, "SUBJECT"), (artifact_id, "ARTIFACT")],
                source_path=row.get("SourcePath", ""),
                source_ref=row.get("SourceRef", ""),
            )

    # 5E: LEDGER_ROW
    if "LEDGER_ROW" in edgeset:
        for row in ledger_rows:
            unit_id = row.get("AtomicUnitID", "").strip()
            if not unit_id:
                continue
            incidences: List[Tuple[str, str]] = [(unit_id, "UNIT")]
            cat_id = row.get("CategoryID", "").strip()
            if cat_id:
                if cat_id in node_ids_by_type.get("CATEGORY", set()):
                    incidences.append((cat_id, "CATEGORY"))
                else:
                    qa_findings.append({
                        "level": "WARNING",
                        "code": "LEDGER_REF_MISSING_NODE",
                        "detail": f"Ledger row {unit_id} references CategoryID={cat_id} which has no CATEGORY node",
                        "source_path": row.get("SourcePath", ""),
                        "source_ref": row.get("SourceRef", ""),
                    })
            for kty_id in normalize_list_field(row.get("KnowledgeTypeIDs", "")):
                if kty_id in node_ids_by_type.get("KNOWLEDGE_TYPE", set()):
                    incidences.append((kty_id, "KNOWLEDGE_TYPE"))
                else:
                    qa_findings.append({
                        "level": "WARNING",
                        "code": "LEDGER_REF_MISSING_NODE",
                        "detail": f"Ledger row {unit_id} references KnowledgeTypeID={kty_id} which has no KNOWLEDGE_TYPE node",
                        "source_path": row.get("SourcePath", ""),
                        "source_ref": row.get("SourceRef", ""),
                    })
            for obj_id in normalize_list_field(row.get("ObjectiveIDs", "")):
                if obj_id in node_ids_by_type.get("OBJECTIVE", set()):
                    incidences.append((obj_id, "OBJECTIVE"))
                else:
                    qa_findings.append({
                        "level": "WARNING",
                        "code": "LEDGER_REF_MISSING_NODE",
                        "detail": f"Ledger row {unit_id} references ObjectiveID={obj_id} which has no OBJECTIVE node",
                        "source_path": row.get("SourcePath", ""),
                        "source_ref": row.get("SourceRef", ""),
                    })
            builder.add_edge(
                "LEDGER_ROW",
                incidences=incidences,
                source_path=row.get("SourcePath", ""),
                source_ref=row.get("SourceRef", ""),
            )

    # 5F: KTY_SUPPORTS_OBJ
    if "KTY_SUPPORTS_OBJ" in edgeset:
        for row in kty_supports_obj_rows:
            kty_id = row.get("KnowledgeTypeID", "").strip()
            obj_id = row.get("ObjectiveID", "").strip()
            if not kty_id or not obj_id:
                continue
            if kty_id not in node_ids_by_type.get("KNOWLEDGE_TYPE", set()):
                qa_findings.append({
                    "level": "WARNING",
                    "code": "KTY_SUPPORTS_OBJ_REF_MISSING_KTY",
                    "detail": f"KTY_SUPPORTS_OBJ row references KnowledgeTypeID={kty_id} which has no KNOWLEDGE_TYPE node",
                    "source_path": row.get("SourcePath", ""),
                    "source_ref": row.get("SourceRef", ""),
                })
                continue
            if obj_id not in node_ids_by_type.get("OBJECTIVE", set()):
                qa_findings.append({
                    "level": "WARNING",
                    "code": "OBJ_REF_MISSING_NODE",
                    "detail": f"KTY_SUPPORTS_OBJ row references ObjectiveID={obj_id} which has no OBJECTIVE node",
                    "source_path": row.get("SourcePath", ""),
                    "source_ref": row.get("SourceRef", ""),
                })
                continue
            builder.add_edge(
                "KTY_SUPPORTS_OBJ",
                incidences=[(kty_id, "KNOWLEDGE_TYPE"), (obj_id, "OBJECTIVE")],
                source_path=row.get("SourcePath", ""),
                source_ref=row.get("SourceRef", ""),
            )

    return builder


# ─── QA checks ────────────────────────────────────────────────────────────────

def run_qa_checks(
    nodes: List[Dict[str, str]],
    edges: List[Dict[str, str]],
    incidences: List[Dict[str, str]],
    normalize_ids: bool,
    has_ledger: bool,
    qa_findings: List[Dict[str, str]],
) -> None:
    """Append findings to qa_findings list. 9 checks per agent Step 6."""

    node_ids: Set[str] = {n["NodeID"] for n in nodes}
    edge_ids: Set[str] = {e["HyperedgeID"] for e in edges}
    node_types_by_id: Dict[str, str] = {n["NodeID"]: n["NodeType"] for n in nodes}

    # Check 1: Schema presence — implicit (we're reading/writing CSVs; format correct by construction)
    qa_findings.append({
        "level": "PASS",
        "code": "SCHEMA_PRESENCE",
        "detail": "nodes.csv, hyperedges.csv, incidence.csv produced with SchemaVersion headers",
    })

    # Check 2: Referential integrity
    dangling_inc_node_ids: List[str] = []
    dangling_inc_edge_ids: List[str] = []
    for inc in incidences:
        if inc["NodeID"] not in node_ids:
            dangling_inc_node_ids.append(inc["NodeID"])
        if inc["HyperedgeID"] not in edge_ids:
            dangling_inc_edge_ids.append(inc["HyperedgeID"])
    if dangling_inc_node_ids or dangling_inc_edge_ids:
        qa_findings.append({
            "level": "BLOCKER",
            "code": "REFERENTIAL_INTEGRITY_FAILURE",
            "detail": f"dangling NodeIDs={sorted(set(dangling_inc_node_ids))}, dangling HyperedgeIDs={sorted(set(dangling_inc_edge_ids))}",
        })
    else:
        qa_findings.append({
            "level": "PASS",
            "code": "REFERENTIAL_INTEGRITY",
            "detail": "All incidences resolve to existing nodes and hyperedges",
        })

    # Check 3: Category membership integrity (<=1 IN_CATEGORY per KTY)
    kty_to_in_category_count: Dict[str, int] = {}
    for edge in edges:
        if edge["HyperedgeType"] != "IN_CATEGORY":
            continue
        for inc in incidences:
            if inc["HyperedgeID"] == edge["HyperedgeID"] and inc["Role"] == "CHILD_KNOWLEDGE_TYPE":
                kty_to_in_category_count[inc["NodeID"]] = kty_to_in_category_count.get(inc["NodeID"], 0) + 1
    for kty_id, count in kty_to_in_category_count.items():
        if count > 1:
            qa_findings.append({
                "level": "BLOCKER",
                "code": "CATEGORY_MEMBERSHIP_PARTITION_AMBIGUITY",
                "detail": f"KnowledgeType {kty_id} has {count} IN_CATEGORY edges (>1 = partition ambiguity)",
            })
    for kty_id in node_ids_by_type_from_nodes(nodes, "KNOWLEDGE_TYPE"):
        if kty_id not in kty_to_in_category_count:
            qa_findings.append({
                "level": "WARNING",
                "code": "KTY_WITHOUT_CATEGORY",
                "detail": f"KnowledgeType {kty_id} has 0 IN_CATEGORY edges (missing category mapping)",
            })

    # Check 4: Subject attachment (each SUBJECT participates in >=1 HAS_SUBJECT)
    subjects_with_edges: Set[str] = set()
    for edge in edges:
        if edge["HyperedgeType"] != "HAS_SUBJECT":
            continue
        for inc in incidences:
            if inc["HyperedgeID"] == edge["HyperedgeID"] and inc["Role"] == "SUBJECT":
                subjects_with_edges.add(inc["NodeID"])
    for subject_id in node_ids_by_type_from_nodes(nodes, "KNOWLEDGE_SUBJECT"):
        if subject_id not in subjects_with_edges:
            qa_findings.append({
                "level": "WARNING",
                "code": "ORPHAN_SUBJECT",
                "detail": f"KnowledgeSubject {subject_id} has no HAS_SUBJECT edge (orphan subject)",
            })

    # Check 5: Artifact attachment
    artifacts_with_edges: Set[str] = set()
    for edge in edges:
        if edge["HyperedgeType"] != "HAS_ARTIFACT":
            continue
        for inc in incidences:
            if inc["HyperedgeID"] == edge["HyperedgeID"] and inc["Role"] == "ARTIFACT":
                artifacts_with_edges.add(inc["NodeID"])
    for artifact_id in node_ids_by_type_from_nodes(nodes, "KNOWLEDGE_ARTIFACT"):
        if artifact_id not in artifacts_with_edges:
            qa_findings.append({
                "level": "WARNING",
                "code": "ORPHAN_ARTIFACT",
                "detail": f"KnowledgeArtifact {artifact_id} has no HAS_ARTIFACT edge (orphan artifact)",
            })

    # Check 6: Subject/artifact bridge integrity
    subject_bridge_count: Dict[str, int] = {}
    artifact_bridge_count: Dict[str, int] = {}
    for edge in edges:
        if edge["HyperedgeType"] != "SUBJECT_MATERIALIZED_AS":
            continue
        for inc in incidences:
            if inc["HyperedgeID"] == edge["HyperedgeID"]:
                if inc["Role"] == "SUBJECT":
                    subject_bridge_count[inc["NodeID"]] = subject_bridge_count.get(inc["NodeID"], 0) + 1
                elif inc["Role"] == "ARTIFACT":
                    artifact_bridge_count[inc["NodeID"]] = artifact_bridge_count.get(inc["NodeID"], 0) + 1
    for subject_id, count in subject_bridge_count.items():
        if count > 1:
            qa_findings.append({
                "level": "BLOCKER",
                "code": "SUBJECT_SPLIT_AMBIGUITY",
                "detail": f"KnowledgeSubject {subject_id} has {count} SUBJECT_MATERIALIZED_AS edges (>1 = split-subject ambiguity)",
            })
    for artifact_id, count in artifact_bridge_count.items():
        if count > 1:
            qa_findings.append({
                "level": "BLOCKER",
                "code": "ARTIFACT_MERGE_AMBIGUITY",
                "detail": f"KnowledgeArtifact {artifact_id} has {count} SUBJECT_MATERIALIZED_AS edges (>1 = merged-artifact ambiguity)",
            })

    # Check 7: Ledger integrity (only if ledger ingested)
    if has_ledger:
        units_in_ledger_rows: Set[str] = set()
        unit_categories: Dict[str, Set[str]] = {}
        for edge in edges:
            if edge["HyperedgeType"] != "LEDGER_ROW":
                continue
            edge_incs = [inc for inc in incidences if inc["HyperedgeID"] == edge["HyperedgeID"]]
            unit_nodes = [inc["NodeID"] for inc in edge_incs if inc["Role"] == "UNIT"]
            cat_nodes = [inc["NodeID"] for inc in edge_incs if inc["Role"] == "CATEGORY"]
            for u in unit_nodes:
                units_in_ledger_rows.add(u)
                if cat_nodes:
                    unit_categories.setdefault(u, set()).update(cat_nodes)
        for unit_id in node_ids_by_type_from_nodes(nodes, "ATOMIC_UNIT"):
            if unit_id not in units_in_ledger_rows:
                qa_findings.append({
                    "level": "WARNING",
                    "code": "UNIT_WITHOUT_LEDGER_ROW",
                    "detail": f"AtomicUnit {unit_id} does not appear in any LEDGER_ROW edge",
                })
        for unit_id, cats in unit_categories.items():
            if len(cats) > 1:
                qa_findings.append({
                    "level": "BLOCKER",
                    "code": "UNIT_MULTIPLE_CATEGORIES",
                    "detail": f"AtomicUnit {unit_id} maps to {len(cats)} categories via ledger rows: {sorted(cats)}",
                })

    # Check 8: ID collisions
    node_id_counts: Dict[str, int] = {}
    for n in nodes:
        node_id_counts[n["NodeID"]] = node_id_counts.get(n["NodeID"], 0) + 1
    for nid, count in node_id_counts.items():
        if count > 1:
            qa_findings.append({
                "level": "BLOCKER",
                "code": "DUPLICATE_NODE_ID",
                "detail": f"NodeID {nid} appears {count} times",
            })
    if normalize_ids:
        norm_id_counts: Dict[str, List[str]] = {}
        for n in nodes:
            norm_id = n.get("NormalizedID", "")
            if norm_id:
                norm_id_counts.setdefault(norm_id, []).append(n["NodeID"])
        for norm_id, originals in norm_id_counts.items():
            if len(originals) > 1:
                qa_findings.append({
                    "level": "WARNING",
                    "code": "DUPLICATE_NORMALIZED_ID",
                    "detail": f"NormalizedID {norm_id} collides across NodeIDs: {sorted(originals)}",
                })

    # Check 9: Evidence completeness
    missing_evidence_nodes = [n["NodeID"] for n in nodes if not n.get("SourcePath") or not n.get("SourceRef")]
    missing_evidence_edges = [e["HyperedgeID"] for e in edges if not e.get("SourcePath") or not e.get("SourceRef")]
    if missing_evidence_nodes:
        qa_findings.append({
            "level": "WARNING",
            "code": "EVIDENCE_MISSING_ON_NODES",
            "detail": f"{len(missing_evidence_nodes)} nodes missing SourcePath or SourceRef (first 5: {missing_evidence_nodes[:5]})",
        })
    if missing_evidence_edges:
        qa_findings.append({
            "level": "WARNING",
            "code": "EVIDENCE_MISSING_ON_EDGES",
            "detail": f"{len(missing_evidence_edges)} hyperedges missing SourcePath or SourceRef (first 5: {missing_evidence_edges[:5]})",
        })


def node_ids_by_type_from_nodes(nodes: List[Dict[str, str]], node_type: str) -> List[str]:
    return [n["NodeID"] for n in nodes if n["NodeType"] == node_type]


# ─── Output serialization ─────────────────────────────────────────────────────

def sort_and_write_nodes(nodes: List[Dict[str, str]], path: Path) -> None:
    nodes_sorted = sorted(nodes, key=lambda n: (n["NodeType"], n["NodeID"]))
    write_csv(path, NODE_COLUMNS, nodes_sorted)


def sort_and_write_edges(edges: List[Dict[str, str]], path: Path) -> None:
    edges_sorted = sorted(edges, key=lambda e: (e["HyperedgeType"], e["HyperedgeID"]))
    write_csv(path, HYPEREDGE_COLUMNS, edges_sorted)


def sort_and_write_incidences(incidences: List[Dict[str, str]], path: Path) -> None:
    incidences_sorted = sorted(incidences, key=lambda i: (i["HyperedgeID"], i["Role"], i["NodeID"], int(i["Ordinal"])))
    write_csv(path, INCIDENCE_COLUMNS, incidences_sorted)


def write_hypergraph_json(
    path: Path,
    brief: Dict,
    nodes: List[Dict[str, str]],
    edges: List[Dict[str, str]],
    incidences: List[Dict[str, str]],
    qa_findings: List[Dict[str, str]],
    delta: Optional[Dict],
    generated_at: str,
) -> None:
    # Group incidences by HyperedgeID for embedded view
    inc_by_edge: Dict[str, List[Dict[str, str]]] = {}
    for inc in sorted(incidences, key=lambda i: (i["HyperedgeID"], i["Role"], i["NodeID"], int(i["Ordinal"]))):
        inc_by_edge.setdefault(inc["HyperedgeID"], []).append({
            "NodeID": inc["NodeID"],
            "Role": inc["Role"],
            "Ordinal": int(inc["Ordinal"]),
        })

    nodes_out = sorted(nodes, key=lambda n: (n["NodeType"], n["NodeID"]))
    edges_out = sorted(edges, key=lambda e: (e["HyperedgeType"], e["HyperedgeID"]))
    edges_with_incidences = []
    for edge in edges_out:
        edges_with_incidences.append({
            **edge,
            "incidences": inc_by_edge.get(edge["HyperedgeID"], []),
        })

    node_counts_by_type: Dict[str, int] = {}
    for n in nodes_out:
        node_counts_by_type[n["NodeType"]] = node_counts_by_type.get(n["NodeType"], 0) + 1
    edge_counts_by_type: Dict[str, int] = {}
    for e in edges_out:
        edge_counts_by_type[e["HyperedgeType"]] = edge_counts_by_type.get(e["HyperedgeType"], 0) + 1

    qa_blockers = sum(1 for f in qa_findings if f.get("level") == "BLOCKER")
    qa_warnings = sum(1 for f in qa_findings if f.get("level") == "WARNING")
    unresolved_refs = sum(
        1 for f in qa_findings
        if f.get("code", "") in (
            "CATEGORY_REF_MISSING_NODE",
            "LEDGER_REF_MISSING_NODE",
            "SUBJECT_REF_MISSING_KTY",
            "ARTIFACT_REF_MISSING_KTY",
            "MAPPING_REF_MISSING_SUBJECT",
            "MAPPING_REF_MISSING_ARTIFACT",
            "KTY_SUPPORTS_OBJ_REF_MISSING_KTY",
            "OBJ_REF_MISSING_NODE",
        )
    )

    out = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": generated_at,
        "run_label": brief.get("run_label", ""),
        "execution_root": brief.get("execution_root", ""),
        "scope": brief.get("scope", ""),
        "brief": brief,
        "nodes": nodes_out,
        "hyperedges": edges_with_incidences,
        "metrics": {
            "node_count": len(nodes_out),
            "node_counts_by_type": node_counts_by_type,
            "hyperedge_count": len(edges_out),
            "hyperedge_counts_by_type": edge_counts_by_type,
            "incidence_count": len(incidences),
            "categories_discovered": node_counts_by_type.get("CATEGORY", 0),
            "knowledge_types_discovered": node_counts_by_type.get("KNOWLEDGE_TYPE", 0),
            "knowledge_subjects_discovered": node_counts_by_type.get("KNOWLEDGE_SUBJECT", 0),
            "knowledge_artifacts_discovered": node_counts_by_type.get("KNOWLEDGE_ARTIFACT", 0),
            "objectives_loaded": node_counts_by_type.get("OBJECTIVE", 0),
            "atomic_units_loaded": node_counts_by_type.get("ATOMIC_UNIT", 0),
            "unresolved_references": unresolved_refs,
            "qa_blockers": qa_blockers,
            "qa_warnings": qa_warnings,
        },
    }
    if delta is not None:
        out["delta"] = delta

    with path.open("w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, sort_keys=True)
        f.write("\n")


def write_qa_report(path: Path, qa_findings: List[Dict[str, str]], delta: Optional[Dict]) -> None:
    by_level: Dict[str, List[Dict[str, str]]] = {"BLOCKER": [], "WARNING": [], "PASS": []}
    for f in qa_findings:
        by_level.setdefault(f.get("level", "PASS"), []).append(f)

    lines = ["# QA Report — DOMAIN Hypergraph", ""]
    lines.append(f"**Schema Version:** {SCHEMA_VERSION}")
    lines.append(f"**Blockers:** {len(by_level['BLOCKER'])}  |  **Warnings:** {len(by_level['WARNING'])}  |  **Passes:** {len(by_level['PASS'])}")
    lines.append("")

    for level in ("BLOCKER", "WARNING", "PASS"):
        items = by_level.get(level, [])
        if not items:
            continue
        lines.append(f"## {level} ({len(items)})")
        lines.append("")
        for item in items:
            code = item.get("code", "")
            detail = item.get("detail", "")
            sp = item.get("source_path", "")
            sr = item.get("source_ref", "")
            line = f"- **{code}**: {detail}"
            if sp or sr:
                line += f"  _(SourcePath={sp}, SourceRef={sr})_"
            lines.append(line)
        lines.append("")

    if delta is not None:
        lines.append("## Delta vs prior run")
        lines.append("")
        lines.append(f"- Prior run label: `{delta.get('prior_run_label', '')}`")
        lines.append(f"- Nodes added: {delta.get('nodes_added', 0)}")
        lines.append(f"- Nodes removed: {delta.get('nodes_removed', 0)}")
        lines.append(f"- Hyperedges added: {delta.get('hyperedges_added', 0)}")
        lines.append(f"- Hyperedges removed: {delta.get('hyperedges_removed', 0)}")
        lines.append("")

    with path.open("w", encoding="utf-8") as f:
        f.write("\n".join(lines))


# ─── Delta computation ────────────────────────────────────────────────────────

def compute_delta(prior_snapshot: Path, current_nodes: List[Dict[str, str]], current_edges: List[Dict[str, str]]) -> Optional[Dict]:
    prior_json = prior_snapshot / "hypergraph.json"
    if not prior_json.exists():
        return None
    with prior_json.open("r", encoding="utf-8") as f:
        prior = json.load(f)

    prior_node_ids: Set[str] = {n["NodeID"] for n in prior.get("nodes", [])}
    prior_edge_ids: Set[str] = {e["HyperedgeID"] for e in prior.get("hyperedges", [])}
    curr_node_ids: Set[str] = {n["NodeID"] for n in current_nodes}
    curr_edge_ids: Set[str] = {e["HyperedgeID"] for e in current_edges}

    added_node_ids = curr_node_ids - prior_node_ids
    removed_node_ids = prior_node_ids - curr_node_ids
    added_edge_ids = curr_edge_ids - prior_edge_ids
    removed_edge_ids = prior_edge_ids - curr_edge_ids

    curr_node_types: Dict[str, str] = {n["NodeID"]: n["NodeType"] for n in current_nodes}
    prior_node_types: Dict[str, str] = {n["NodeID"]: n["NodeType"] for n in prior.get("nodes", [])}
    curr_edge_types: Dict[str, str] = {e["HyperedgeID"]: e["HyperedgeType"] for e in current_edges}
    prior_edge_types: Dict[str, str] = {e["HyperedgeID"]: e["HyperedgeType"] for e in prior.get("hyperedges", [])}

    changes_by_type: Dict[str, Dict[str, int]] = {}
    for nid in added_node_ids:
        t = curr_node_types.get(nid, "")
        changes_by_type.setdefault(f"nodes:{t}", {"added": 0, "removed": 0})["added"] += 1
    for nid in removed_node_ids:
        t = prior_node_types.get(nid, "")
        changes_by_type.setdefault(f"nodes:{t}", {"added": 0, "removed": 0})["removed"] += 1
    for eid in added_edge_ids:
        t = curr_edge_types.get(eid, "")
        changes_by_type.setdefault(f"edges:{t}", {"added": 0, "removed": 0})["added"] += 1
    for eid in removed_edge_ids:
        t = prior_edge_types.get(eid, "")
        changes_by_type.setdefault(f"edges:{t}", {"added": 0, "removed": 0})["removed"] += 1

    return {
        "prior_run_label": prior.get("run_label", ""),
        "nodes_added": len(added_node_ids),
        "nodes_removed": len(removed_node_ids),
        "hyperedges_added": len(added_edge_ids),
        "hyperedges_removed": len(removed_edge_ids),
        "changes_by_type": changes_by_type,
    }


# ─── Main ─────────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(description="Build DOMAIN hypergraph from staging CSVs.")
    parser.add_argument("--staging-dir", required=True, type=Path, help="Directory containing staging CSVs (typically {snapshot}/Evidence/)")
    parser.add_argument("--output-dir", required=True, type=Path, help="Directory for tool outputs (typically {snapshot}/)")
    parser.add_argument("--run-label", default="DOMAIN_HYPERGRAPH", help="Run label recorded in hypergraph.json")
    parser.add_argument("--execution-root", default="", help="Execution root path recorded in hypergraph.json")
    parser.add_argument("--scope", default="ALL", help="Scope recorded in hypergraph.json (passthrough)")
    parser.add_argument("--normalize-ids", default="true", choices=["true", "false"], help="Compute NormalizedID (analysis-only)")
    parser.add_argument("--edgeset", default="DEFAULT", help=f"Comma-separated edge types to emit, or DEFAULT ({','.join(VALID_EDGE_TYPES)})")
    parser.add_argument("--variant", default="DOMAIN", help="Variant recorded on nodes (default DOMAIN)")
    parser.add_argument("--prior-snapshot", type=Path, default=None, help="Path to prior snapshot directory for delta computation")
    args = parser.parse_args()

    if not args.staging_dir.is_dir():
        print(f"ERROR: staging-dir does not exist: {args.staging_dir}", file=sys.stderr)
        return 2
    args.output_dir.mkdir(parents=True, exist_ok=True)

    # Required files
    cat_path = args.staging_dir / "discovered_categories.csv"
    kty_path = args.staging_dir / "discovered_knowledge_types.csv"
    if not cat_path.exists() or not kty_path.exists():
        print(f"ERROR: required staging files missing: {cat_path.name} and/or {kty_path.name}", file=sys.stderr)
        return 2

    # Edgeset resolution
    normalize_ids = args.normalize_ids == "true"
    if args.edgeset == "DEFAULT":
        edgeset = VALID_EDGE_TYPES[:]
    else:
        edgeset = [e.strip() for e in args.edgeset.split(",") if e.strip()]
        invalid = [e for e in edgeset if e not in VALID_EDGE_TYPES]
        if invalid:
            print(f"ERROR: invalid edge types in --edgeset: {invalid}", file=sys.stderr)
            return 2

    # Read staging
    cat_rows = read_csv_rows(cat_path)
    kty_rows = read_csv_rows(kty_path)
    subject_rows = read_csv_rows(args.staging_dir / "discovered_knowledge_subjects.csv")
    artifact_rows = read_csv_rows(args.staging_dir / "artifact_enumeration.csv")
    mapping_rows = read_csv_rows(args.staging_dir / "subject_artifact_mapping.csv")
    ledger_rows = read_csv_rows(args.staging_dir / "discovered_ledger_rows.csv")
    objective_rows = read_csv_rows(args.staging_dir / "discovered_objectives.csv")
    kty_supports_obj_rows = read_csv_rows(args.staging_dir / "kty_supports_obj.csv")
    has_ledger = len(ledger_rows) > 0

    qa_findings: List[Dict[str, str]] = []

    # Build nodes
    nodes: List[Dict[str, str]] = []
    nodes.extend(build_category_nodes(cat_rows, args.variant))
    nodes.extend(build_knowledge_type_nodes(kty_rows, args.variant, normalize_ids))
    nodes.extend(build_subject_nodes(subject_rows, args.variant))
    nodes.extend(build_artifact_nodes(artifact_rows, args.variant))
    nodes.extend(build_atomic_unit_nodes(ledger_rows, args.variant))
    # Objectives: from explicit file OR from ledger ObjectiveIDs field
    explicit_objectives = build_objective_nodes(objective_rows, args.variant)
    nodes.extend(explicit_objectives)
    explicit_obj_ids = {n["NodeID"] for n in explicit_objectives}
    for row in ledger_rows:
        for obj_id in normalize_list_field(row.get("ObjectiveIDs", "")):
            if obj_id and obj_id not in explicit_obj_ids:
                nodes.append({
                    "SchemaVersion": SCHEMA_VERSION,
                    "NodeID": obj_id,
                    "NodeType": "OBJECTIVE",
                    "Label": "TBD",
                    "SourcePath": row.get("SourcePath", ""),
                    "SourceRef": row.get("SourceRef", "") + "#LEDGER_DERIVED",
                    "Notes": "Derived from ledger row ObjectiveIDs field",
                    "Variant": args.variant,
                })
                explicit_obj_ids.add(obj_id)

    # Index node IDs by type for edge construction
    node_ids_by_type: Dict[str, Set[str]] = {}
    for n in nodes:
        node_ids_by_type.setdefault(n["NodeType"], set()).add(n["NodeID"])

    # Build edges + incidences
    builder = build_hyperedges(
        kty_rows=kty_rows,
        subject_rows=subject_rows,
        artifact_rows=artifact_rows,
        mapping_rows=mapping_rows,
        ledger_rows=ledger_rows,
        kty_supports_obj_rows=kty_supports_obj_rows,
        node_ids_by_type=node_ids_by_type,
        edgeset=edgeset,
        qa_findings=qa_findings,
    )

    # QA
    run_qa_checks(nodes, builder.edges, builder.incidences, normalize_ids, has_ledger, qa_findings)

    # Delta
    delta = None
    if args.prior_snapshot is not None:
        delta = compute_delta(args.prior_snapshot, nodes, builder.edges)

    # Write outputs
    sort_and_write_nodes(nodes, args.output_dir / "nodes.csv")
    sort_and_write_edges(builder.edges, args.output_dir / "hyperedges.csv")
    sort_and_write_incidences(builder.incidences, args.output_dir / "incidence.csv")

    generated_at = datetime.now(timezone.utc).isoformat()
    brief = {
        "run_label": args.run_label,
        "execution_root": args.execution_root,
        "scope": args.scope,
        "normalize_ids": normalize_ids,
        "edgeset": edgeset,
        "variant": args.variant,
    }
    write_hypergraph_json(
        args.output_dir / "hypergraph.json",
        brief, nodes, builder.edges, builder.incidences, qa_findings, delta, generated_at,
    )
    write_qa_report(args.output_dir / "QA_Report.md", qa_findings, delta)

    # Summary to stdout
    qa_blockers = sum(1 for f in qa_findings if f.get("level") == "BLOCKER")
    qa_warnings = sum(1 for f in qa_findings if f.get("level") == "WARNING")
    print(f"build_hypergraph: nodes={len(nodes)} edges={len(builder.edges)} incidences={len(builder.incidences)} blockers={qa_blockers} warnings={qa_warnings}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
