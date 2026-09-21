#!/usr/bin/env python3
"""Refine Chirality Gate 3 category boundaries and rerun ratification.

This is a deterministic refinement helper for the Chirality self-domain
decomposition. It does not change atom text. It rewrites category scopes,
applies explicit primary-function boundary rules to the draft category ledger,
marks existing ambiguous assignment findings as resolved by forced decision, and
recomputes BM25/dense category-scope evidence against an existing source_v2
snapshot.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sqlite3
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "tools" / "source_catalog"))
from source_database import resolve_domain_root, resolve_snapshot_path  # noqa: E402


CATEGORY_REFINEMENTS: dict[str, dict[str, str]] = {
    "CAT-001": {
        "Name": "Epistemic and Professional-Practice Foundations",
        "ScopeDescription": (
            "Foundational claims about knowledge, warrant, professional reliance, "
            "regulated engineering accountability, human responsibility, and the "
            "ontology/epistemology/praxiology/axiology basis of Chirality. This "
            "category owns professional and philosophical warrant concepts, not "
            "the operational audit workflows that inspect them."
        ),
        "InclusionCriteria": (
            "Include atoms about professional obligations, APEGA-aligned "
            "responsibilities, responsible charge, public welfare, evidence over "
            "plausibility, human accountability, warrant states, epistemic labels, "
            "reliability/safety framing as professional-practice foundations, and "
            "philosophical framework claims."
        ),
        "Exclusions": (
            "Exclude concrete audit/review procedures, validation tools, agent "
            "execution contracts, repository topology, and license terms unless "
            "the atom's primary function is professional or epistemic warrant."
        ),
        "Query": (
            "professional practice epistemic warrant accountability responsible "
            "charge APEGA public welfare evidence plausibility human authority "
            "warrant state epistemic label ontology epistemology praxiology "
            "axiology safety reliability professional responsibility"
        ),
    },
    "CAT-002": {
        "Name": "Governance and Agent Instruction Architecture",
        "ScopeDescription": (
            "The normative architecture of the agent suite: agent types, "
            "epistemic posture, instruction-file authority, precedence layers, "
            "invariants, approval gates, governance integration rules, and "
            "human/agent authority boundaries."
        ),
        "InclusionCriteria": (
            "Include atoms about AGENTS.md, agent matrices, Type 0/1/2 authority, "
            "PROTOCOL/SPEC/STRUCTURE/RATIONALE precedence, non-negotiable "
            "invariants, derivative-package and snapshot rules, governance "
            "grammar, and human-gated authority."
        ),
        "Exclusions": (
            "Exclude the detailed procedure of a specific decomposer, auditor, "
            "publisher, extraction worker, project coordinator, or skill pack "
            "when that procedure belongs to a more specific operational category."
        ),
        "Query": (
            "agent governance instruction architecture authority type matrix "
            "precedence invariant protocol spec structure rationale derivative "
            "package snapshot rule closure rule human approval normative "
            "operative evaluative"
        ),
    },
    "CAT-003": {
        "Name": "Decomposition Lifecycle and Domain Structuring",
        "ScopeDescription": (
            "The decomposition machinery that turns sources into governed "
            "domain, project, or software structures: intake, skeletons, dispatch "
            "plans, atomization, ledgers, categories, knowledge types, subjects, "
            "scope change, and decomposition package review. This category owns "
            "decomposition-specific manifests and remediation planning."
        ),
        "InclusionCriteria": (
            "Include atoms about DECOMPOSITION_STANDARD, DOMAIN_DECOMP, PROJECT_DECOMP, "
            "SOFTWARE_DECOMP, source atomization, source skeletons, dispatch "
            "units, Domain Ledger rows, Category/KTY/Subject assignment, "
            "decomposition package review, and source-driven scope change."
        ),
        "Exclusions": (
            "Exclude generic TASK/skill runtime contracts, independent audit "
            "execution, publication/synthesis packages, and extraction mechanics "
            "unless the atom is specifically about decomposition or atomization."
        ),
        "Query": (
            "decomposition lifecycle intake source skeleton dispatch unit "
            "atomization domain ledger category knowledge type subject scope "
            "change package review remediation manifest gate"
        ),
    },
    "CAT-004": {
        "Name": "Task, Skill, and Tool Execution Contracts",
        "ScopeDescription": (
            "Generic bounded worker execution contracts and local method/tool "
            "mechanics: TASK shell behavior, TaskSkill selection, brief schemas, "
            "runtime overrides, allowed tools, skill metadata, tool policy, and "
            "deterministic tool ownership."
        ),
        "InclusionCriteria": (
            "Include atoms about TASK dispatch, skill pack contracts, BRIEF_SCHEMA, "
            "QA_CHECKS, TOOL_POLICY, RuntimeOverrides, AllowedTools, Skillmaker, "
            "Toolmaker, validation of generic skill metadata, and method-pack "
            "boundaries."
        ),
        "Exclusions": (
            "Exclude extraction, publication, decomposition, audit/review, or "
            "coordination content when a skill or tool atom primarily specifies "
            "that domain operation rather than the generic execution contract."
        ),
        "Query": (
            "TASK TaskSkill skill pack tool contract brief schema QA checks tool "
            "policy runtime overrides allowed tools deterministic tools "
            "Skillmaker Toolmaker method pack validation metadata"
        ),
    },
    "CAT-005": {
        "Name": "Source Fidelity, Retrieval, and Validation Infrastructure",
        "ScopeDescription": (
            "Narrow infrastructure that preserves and queries source truth: "
            "SourceRefs, content hashes, source manifests, source catalogs, local "
            "indexes, source_v2 BM25/dense retrieval, chunks, section nodes, "
            "review HTML anchors, telemetry, and hash-based reproducibility."
        ),
        "InclusionCriteria": (
            "Include atoms about Source_Manifest, SourceRef, ContentHash, source "
            "catalog/database, local index snapshots, source_v2 retrieval, BM25, "
            "embeddings, chunk identity, section nodes, source-copy policy, "
            "manifest hashes, and retrieval rebuild policy."
        ),
        "Exclusions": (
            "Exclude generic deterministic tools, generic validation scripts, "
            "extraction pipelines, domain-engine profile/artifact boundaries, and "
            "semantic domain claims that merely cite a source."
        ),
        "Query": (
            "SourceRef ContentHash source manifest source catalog source database "
            "local index source_v2 retrieval BM25 dense embeddings chunk section "
            "node review html anchor telemetry hash reproducibility snapshot"
        ),
    },
    "CAT-006": {
        "Name": "Audit, Review, Reconciliation, and Evaluation",
        "ScopeDescription": (
            "Independent checks over governed state: audits, reviews, "
            "reconciliation, evaluation reports, findings, closure checks, QA "
            "reports, evidence bundles, validation verdicts, and blocker "
            "disposition. This category owns review judgment, not the extraction "
            "or publication operation being reviewed."
        ),
        "InclusionCriteria": (
            "Include atoms about AUDIT_* agents, REVIEW, RECONCILIATION, "
            "EVALUATION*, findings registers, evidence sweeps, closure audits, "
            "validation verdicts, review gates, QA reports, and post-author review."
        ),
        "Exclusions": (
            "Exclude source catalog/index machinery, extraction mechanics, "
            "decomposition-specific lifecycle machinery, and synthesis package "
            "assembly unless the atom is primarily an independent check."
        ),
        "Query": (
            "audit review reconciliation evaluation findings closure verdict "
            "blocker QA report evidence bundle validation conformance coverage "
            "assessment backcheck disposition gate"
        ),
    },
    "CAT-007": {
        "Name": "Publication, Aggregation, Hypergraph, and Synthesis",
        "ScopeDescription": (
            "Downstream synthesis and publication packages assembled from "
            "accepted upstream truth: DBM publication, aggregation, hypergraph "
            "snapshots, concordance, semantic matrices, content digests, and "
            "derived publication artifacts."
        ),
        "InclusionCriteria": (
            "Include atoms about DBM_PUBLISHER, AGGREGATION, DOMAIN_HYPERGRAPH, "
            "publication packages, semantic lensing/matrix build, concordance, "
            "content digest, derived package status, and synthesis outputs."
        ),
        "Exclusions": (
            "Exclude upstream decomposition truth, independent audit/review truth, "
            "and generic TASK/skill contract mechanics except where an atom "
            "describes how downstream packages consume or assemble them."
        ),
        "Query": (
            "publish publication DBM aggregation hypergraph synthesis concordance "
            "semantic matrix lens content digest derived package snapshot "
            "publication artifact evidence bundle"
        ),
    },
    "CAT-008": {
        "Name": "Document, Asset, Drawing, and Engineering-Data Extraction",
        "ScopeDescription": (
            "Source and engineering-artifact extraction workflows: PDF-to-Markdown, "
            "page transcription, equation extraction/audit mechanics, "
            "figure/table/image handling, drawing extraction, P&ID symbol work, "
            "equipment extraction, estimate extraction, and external extraction "
            "tool integration."
        ),
        "InclusionCriteria": (
            "Include atoms about PDF2MD, page rasters, folios, figures, tables, "
            "equations, crops, bounding boxes, drawing extraction, P&ID valves, "
            "equipment extraction, estimate extraction, asset manifests, and "
            "external extraction tools."
        ),
        "Exclusions": (
            "Exclude generic TASK/skill contract atoms, independent audit/review "
            "closure, publication synthesis, and source-index infrastructure "
            "unless the atom specifically governs extraction work."
        ),
        "Query": (
            "PDF2MD page raster folio equation figure table image crop bounding "
            "box drawing extraction P&ID valve equipment estimate asset manifest "
            "transcription external tools"
        ),
    },
    "CAT-009": {
        "Name": "Coordination, Change, Scheduling, and Deliverable Workflows",
        "ScopeDescription": (
            "Human-facing and project-execution workflows: orchestration, "
            "preparation, change management, scheduling, working items, "
            "deliverable tasks, dependency handling, handoff state, INIT-TASK "
            "coordination, and operating cadence."
        ),
        "InclusionCriteria": (
            "Include atoms about ORCHESTRATOR, PREPARATION, CHANGE, schedule workflows, "
            "WORKING_ITEMS, HELP_HUMAN, deliverable workflows, dependency "
            "registers, handoff state, INIT-TASK coordination, and control loops."
        ),
        "Exclusions": (
            "Exclude leaf worker method contracts, extraction workflows, "
            "publication packages, and product/work-surface boundary descriptions "
            "unless the atom is principally about coordination or change flow."
        ),
        "Query": (
            "orchestration preparation change management scheduling working items "
            "deliverable workflow dependencies handoff state INIT-TASK "
            "coordination execution control loop cadence"
        ),
    },
    "CAT-010": {
        "Name": "Work-Surface, Project, Product, and Integration Boundaries",
        "ScopeDescription": (
            "The organization of Chirality domains, projects, app/export surfaces, "
            "Domain Engine integration, OpenPipeStress integration, private/public "
            "repository boundaries, active work-surface registry documents, and "
            "profile/protected-path boundaries."
        ),
        "InclusionCriteria": (
            "Include atoms about domains/, projects/, work-surface registry, "
            "chirality-app-dev, chirality-piping, public export boundary, Domain "
            "Engine, OpenPipeStress integration, repository organization, "
            "profile artifacts, protected paths, and private/project workspace "
            "limits."
        ),
        "Exclusions": (
            "Exclude legal license terms, generic source-index infrastructure, "
            "and ordinary coordination workflow unless the atom is primarily "
            "about repository topology, product boundary, or integration scope."
        ),
        "Query": (
            "work surface domains projects chirality app dev piping Domain Engine "
            "OpenPipeStress integration public export boundary repository "
            "organization private workspace profile artifact protected path"
        ),
    },
    "CAT-011": {
        "Name": "Legal, License, and Public-Release Boundaries",
        "ScopeDescription": (
            "License terms and explicit legal/public-release obligations, including "
            "the repository license, copyright grants, warranty disclaimers, "
            "liability limits, public legal notices, and professional-engineering "
            "license clause statements."
        ),
        "InclusionCriteria": (
            "Include atoms about LICENSE.md, MIT license permissions, copyright, "
            "warranty disclaimer, liability limitation, public release legal "
            "notice, license notices, and explicit professional-engineering "
            "clause language."
        ),
        "Exclusions": (
            "Exclude generic reliability, high-stakes, compliance, permission-map, "
            "profile, private/public workspace, and professional-practice atoms "
            "unless the atom is explicitly legal or license-focused."
        ),
        "Query": (
            "LICENSE MIT license copyright permission warranty liability legal "
            "notice public release professional engineering clause license terms"
        ),
    },
}


BOUNDARY_DECISIONS: list[dict[str, str]] = [
    {
        "RuleID": "G3BR-001",
        "Decision": "Primary-function routing",
        "AppliesTo": "All categories",
        "Rule": "Assign by the atom's principal function, not every keyword it touches.",
    },
    {
        "RuleID": "G3BR-002",
        "Decision": "Normative governance boundary",
        "AppliesTo": "CAT-002 vs operational categories",
        "Rule": "Agent architecture, authority, precedence, invariants, and governance grammar route to CAT-002; specific agent procedures route to their operational category.",
    },
    {
        "RuleID": "G3BR-003",
        "Decision": "Decomposition boundary",
        "AppliesTo": "CAT-003 vs CAT-004/CAT-006/CAT-007/CAT-008/CAT-009",
        "Rule": "Decomposition lifecycle, atomization, ledgers, KTY/category/subject assignment, and scope-change remediation planning route to CAT-003.",
    },
    {
        "RuleID": "G3BR-004",
        "Decision": "Generic execution contract boundary",
        "AppliesTo": "CAT-004 vs domain-operation categories",
        "Rule": "Generic TASK, skill metadata, brief-schema, runtime override, and tool-policy content routes to CAT-004; domain-specific operations route to the domain operation category.",
    },
    {
        "RuleID": "G3BR-005",
        "Decision": "Extraction boundary",
        "AppliesTo": "CAT-008 vs CAT-004/CAT-006",
        "Rule": "Transcription, extraction, crops, bboxes, drawings, assets, equations, equipment, and estimates route to CAT-008; independent review of those outputs routes to CAT-006.",
    },
    {
        "RuleID": "G3BR-006",
        "Decision": "Audit/review boundary",
        "AppliesTo": "CAT-006 vs CAT-001/CAT-003/CAT-007/CAT-008",
        "Rule": "Independent checks, findings, verdicts, QA, closure, review gates, and evaluation route to CAT-006 even when the checked object belongs elsewhere.",
    },
    {
        "RuleID": "G3BR-007",
        "Decision": "Publication/synthesis boundary",
        "AppliesTo": "CAT-007 vs CAT-003/CAT-006",
        "Rule": "DBM, aggregation, hypergraph, concordance, semantic matrix, and publication packages route to CAT-007; upstream decomposition truth and independent review do not.",
    },
    {
        "RuleID": "G3BR-008",
        "Decision": "Work-surface boundary",
        "AppliesTo": "CAT-010 vs CAT-003/CAT-005/CAT-009/CAT-011",
        "Rule": "Repository topology, domains/, projects/, exports, Domain Engine, OpenPipeStress, profile artifacts, and protected paths route to CAT-010 unless explicitly legal/license text.",
    },
    {
        "RuleID": "G3BR-009",
        "Decision": "Narrow source-fidelity boundary",
        "AppliesTo": "CAT-005 vs tools/extraction/validation",
        "Rule": "CAT-005 is limited to SourceRefs, ContentHash, manifests, source catalogs, indexes, chunks, retrieval, anchors, hashes, telemetry, and reproducibility.",
    },
    {
        "RuleID": "G3BR-010",
        "Decision": "Narrow legal/license boundary",
        "AppliesTo": "CAT-011 vs professional/boundary categories",
        "Rule": "CAT-011 is limited to LICENSE, MIT permissions, copyright, warranty, liability, public legal notices, and explicit license-clause atoms.",
    },
    {
        "RuleID": "G3BR-011",
        "Decision": "No atom splits in this refinement",
        "AppliesTo": "All 881 ambiguous findings",
        "Rule": "Existing ambiguous findings are resolved as forced category decisions; UnitStatement text and ContentHash values are unchanged.",
    },
    {
        "RuleID": "G3BR-012",
        "Decision": "Dense threshold remains human-gated",
        "AppliesTo": "Category_Scope_Ratification.csv",
        "Rule": "The default 0.75 cosine threshold remains recorded; any calibrated dense basis requires explicit human approval before Gate 3 closure.",
    },
]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--domain-root", type=Path)
    ap.add_argument("--repo-root", type=Path, default=Path("."))
    ap.add_argument("--snapshot", type=Path)
    ap.add_argument("--timestamp", default=None)
    ap.add_argument("--cosine-threshold", type=float, default=0.75)
    args = ap.parse_args()

    try:
        domain_root = resolve_domain_root(args.domain_root)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    decomp_root = domain_root / "_Decomposition"
    timestamp = args.timestamp or datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    generated_iso = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    snapshot = resolve_snapshot_path(args.snapshot, domain_root)

    category_rows = refine_categories(read_csv(decomp_root / "Category_Register.csv"))
    ledger_rows, assignment_changes = refine_ledger(
        read_csv(decomp_root / "Domain_Ledger_Gate3_Category_Draft.csv")
    )
    findings_rows = resolve_findings(
        read_csv(decomp_root / "Category_Assignment_Findings.csv"),
        ledger_rows,
        assignment_changes,
    )
    ratification_rows = ratify_categories(
        snapshot=snapshot,
        category_rows=category_rows,
        ledger_rows=ledger_rows,
        cosine_threshold=args.cosine_threshold,
    )
    assignment_summary_rows = build_assignment_summary(category_rows, ledger_rows, findings_rows, ratification_rows)
    findings_summary_rows = build_findings_summary(category_rows, findings_rows, assignment_changes)

    write_csv(decomp_root / "Category_Register.csv", category_rows)
    write_csv(decomp_root / "Domain_Ledger_Gate3_Category_Draft.csv", ledger_rows)
    write_csv(decomp_root / "Category_Assignment_Findings.csv", findings_rows)
    write_csv(decomp_root / "Category_Assignment_Summary.csv", assignment_summary_rows)
    write_csv(decomp_root / "Category_Assignment_Findings_Summary.csv", findings_summary_rows)
    write_csv(decomp_root / "Category_Scope_Ratification.csv", ratification_rows)
    write_csv(decomp_root / "Category_Boundary_Decisions.csv", BOUNDARY_DECISIONS)
    write_calibration_note(decomp_root / "Gate3_Ratification_Calibration.md", ratification_rows, generated_iso)
    write_review_packet(decomp_root / "Category_Assignment_Review_Packet.md", category_rows, findings_rows, assignment_changes, generated_iso)

    snapshot_dir = decomp_root / "gate3_categories" / f"GATE3_CATEGORY_REFINEMENT_{timestamp}"
    snapshot_dir.mkdir(parents=True, exist_ok=False)
    for filename in [
        "Category_Register.csv",
        "Domain_Ledger_Gate3_Category_Draft.csv",
        "Category_Assignment_Findings.csv",
        "Category_Assignment_Summary.csv",
        "Category_Assignment_Findings_Summary.csv",
        "Category_Scope_Ratification.csv",
        "Category_Boundary_Decisions.csv",
        "Gate3_Ratification_Calibration.md",
        "Category_Assignment_Review_Packet.md",
    ]:
        (snapshot_dir / filename).write_text((decomp_root / filename).read_text(encoding="utf-8"), encoding="utf-8")

    write_gate3_report(snapshot_dir / "GATE3_CATEGORY_REFINEMENT.md", ratification_rows, findings_rows, assignment_changes, generated_iso, snapshot)
    write_handoff(snapshot_dir / "HANDOFF_STATE.md", ratification_rows, findings_rows, generated_iso, snapshot)
    (decomp_root / "gate3_categories" / "_LATEST_GATE3_PROPOSAL.md").write_text(
        f"Latest: {snapshot_dir.name}\nUpdated: {generated_iso}\nStatus: OPEN_PENDING_CALIBRATED_RATIFICATION_APPROVAL\n",
        encoding="utf-8",
    )

    print(f"Wrote Gate 3 category refinement snapshot: {snapshot_dir}")
    print(f"Assignment changes: {len(assignment_changes)}")
    print(f"Open assignment findings: {sum(1 for r in findings_rows if r.get('Status', '').startswith('OPEN'))}")
    print(f"Blocking scope verdicts: {sum(1 for r in ratification_rows if r.get('Blocking') == 'YES')}")
    return 0


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        raise ValueError(f"no rows to write: {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def refine_categories(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    refined = []
    for row in rows:
        cat_id = row["CategoryID"]
        replacement = CATEGORY_REFINEMENTS[cat_id]
        updated = dict(row)
        for key in ("Name", "ScopeDescription", "InclusionCriteria", "Exclusions", "Query"):
            updated[key] = replacement[key]
        refined.append(updated)
    return refined


def has_any(text: str, needles: list[str]) -> bool:
    return any(needle in text for needle in needles)


def has_token_signal(text: str, needles: list[str]) -> bool:
    for needle in needles:
        pattern = r"(?<![a-z0-9])" + re.escape(needle) + r"(?![a-z0-9])"
        if re.search(pattern, text):
            return True
    return False


def dominant_source_categories(rows: list[dict[str, str]]) -> dict[str, str]:
    by_source: dict[str, Counter[str]] = defaultdict(Counter)
    for row in rows:
        if row.get("InOutStatus") == "IN":
            by_source[row["SourceDoc"]][row.get("CategoryID", "")] += 1
    result = {}
    for source_doc, counts in by_source.items():
        non_legal = Counter({cat: count for cat, count in counts.items() if cat != "CAT-011"})
        result[source_doc] = (non_legal or counts).most_common(1)[0][0]
    return result


def classify_row(row: dict[str, str], source_dominant: dict[str, str]) -> tuple[str, str, str]:
    current = row.get("CategoryID", "")
    source_doc = row.get("SourceDoc", "")
    atom_id = row.get("AtomicUnitID", "")
    text = row.get("UnitStatement", "")
    lower = text.lower()

    if row.get("InOutStatus") != "IN":
        return current, "", "OUT/TBD rows remain unassigned."
    if source_doc == "SRC-LICENSE":
        return "CAT-011", "G3BR-010", "LICENSE.md rows are explicit license/legal terms."
    if atom_id == "HBA-RT007-00145":
        return "CAT-011", "G3BR-010", "README license statement is explicitly legal/license-focused."
    if source_doc == "SRC-TOOLS-RETRIEVAL-README":
        return "CAT-005", "G3BR-009", "Retrieval README rows are the source_v2 retrieval contract."
    if source_doc.startswith("SRC-EXPORTS-") and (
        "top-level path contains" in lower or "public export" in lower or "export" in lower
    ):
        return "CAT-010", "G3BR-008", "Export reports describe public/product work-surface topology."
    if "domains/" in lower or "projects/" in lower or "work-surface" in lower or "work surface" in lower:
        return "CAT-010", "G3BR-008", "domains/projects/work-surface topology routes to CAT-010."

    if current == "CAT-011":
        if has_any(lower, ["license", "copyright", "warranty", "liability", "permission is granted", "mit license", "legal notice"]):
            return "CAT-011", "G3BR-010", "Atom is explicitly legal/license-focused."
        if has_any(lower, ["permission map", "write permission", "protected path", "domain engine", "profile", "workspace"]):
            return "CAT-010", "G3BR-008", "Permission/profile/workspace atom is a boundary topic, not license law."
        if has_any(lower, ["reliability", "hallucination", "calibration", "safety integrity", "safety as", "risk", "public welfare", "professional responsibility", "legally defensible", "legal status", "compliance"]):
            return "CAT-001", "G3BR-010", "Professional/legal-risk foundation is not an explicit license term."
        if has_any(lower, ["review", "audit", "check", "evaluat", "finding", "qa", "validity", "validation"]):
            return "CAT-006", "G3BR-010", "Review/evaluation atom is not an explicit license term."
        return source_dominant.get(source_doc, current), "G3BR-010", "Non-license CAT-011 false positive routed to source-dominant category."

    if current == "CAT-005":
        if source_doc == "SRC-AGENTS-AGENT-SCOPE-CHANGE":
            if has_any(lower, ["validate", "validation", "closure", "post-change"]):
                return "CAT-006", "G3BR-006", "Scope-change validation/closure routes to audit/review."
            return "CAT-003", "G3BR-003", "KTY remediation manifests are decomposition/scope-change machinery."
        if source_doc == "SRC-AGENTS-AGENT-DOMAIN-ENGINE":
            return "CAT-010", "G3BR-008", "Domain-engine artifact/profile rows define integration boundaries."
        if source_doc == "SRC-SKILLPACK-DOMAIN-PROSE-VALIDATE":
            return "CAT-008", "G3BR-005", "Prose validation worker rows describe extraction/re-extraction workflow."
        if source_doc == "SRC-README" and has_any(lower, ["export", "public export"]):
            return "CAT-010", "G3BR-008", "README export rows describe public/product boundary."
        if source_doc == "SRC-CHIRALITY-FRAMEWORK":
            return "CAT-001", "G3BR-007", "Epistemic retrieval concept is professional/epistemic foundation."

        source_terms = [
            "sourceref",
            "source ref",
            "contenthash",
            "content hash",
            "source database",
            "source catalog",
            "source_v2",
            "retrieval",
            "bm25",
            "embedding",
            "index",
            "chunks",
            "section nodes",
            "source manifest",
            "manifest hash",
            "catalog",
            "local index",
            "_localindexes",
            "telemetry",
            "provenance",
            "hash",
            "reproducib",
            "supersession",
        ]
        if has_any(lower, source_terms):
            return "CAT-005", "G3BR-009", "Atom is source-fidelity/retrieval infrastructure."
        extraction_terms = [
            "pdf",
            "pdf2md",
            "raster",
            "page",
            "markdown",
            "asset",
            "figure",
            "table",
            "image",
            "equation",
            "bbox",
            "crop",
            "drawing",
            "titleblock",
            "valve",
            "zingg",
            "extraction",
        ]
        if has_token_signal(lower, extraction_terms):
            return "CAT-008", "G3BR-005", "Extraction mechanics route to CAT-008."
        if has_any(lower, ["audit", "review", "findings", "qa", "coverage", "closure"]):
            return "CAT-006", "G3BR-006", "Audit/review validation routes to CAT-006."
        if has_any(lower, ["validate", "validation", "scaffold", "tool", "script", "schema", "enum", "id format", "csv", "snapshot", "status", "folder", "creates", "writes", "generates", "merge"]):
            return "CAT-004", "G3BR-004", "Generic deterministic tool mechanics route to CAT-004."
        if has_any(lower, ["export", "public", "domain profile", "protected path", "model state", "run id"]):
            return "CAT-010", "G3BR-008", "Integration/profile provenance rows route to CAT-010."
    return current, "G3BR-001", "Primary-function assignment retained."


def refine_ledger(rows: list[dict[str, str]]) -> tuple[list[dict[str, str]], dict[str, dict[str, str]]]:
    source_dominant = dominant_source_categories(rows)
    changes: dict[str, dict[str, str]] = {}
    for row in rows:
        old = row.get("CategoryID", "")
        new, rule_id, note = classify_row(row, source_dominant)
        if row.get("InOutStatus") != "IN":
            row["CategoryID"] = ""
            continue
        if new != old:
            changes[row["AtomicUnitID"]] = {
                "OldCategoryID": old,
                "NewCategoryID": new,
                "RuleID": rule_id,
                "Note": note,
            }
            row["CategoryID"] = new
            row["CategoryAssignmentStatus"] = "REFINED_GATE3"
            row["CategoryAssignmentMethod"] = "BOUNDARY_RULE_REFINEMENT"
            row["CategoryAssignmentConfidence"] = "MEDIUM"
            row["CategoryAssignmentRationale"] = f"{rule_id}: {note}"
            row["DecisionRef"] = append_token(row.get("DecisionRef", ""), rule_id)
    return rows, changes


def append_token(raw: str, token: str) -> str:
    tokens = [part.strip() for part in raw.replace(",", ";").split(";") if part.strip()]
    if token not in tokens:
        tokens.append(token)
    return ";".join(tokens)


def resolve_findings(
    findings: list[dict[str, str]],
    ledger_rows: list[dict[str, str]],
    changes: dict[str, dict[str, str]],
) -> list[dict[str, str]]:
    final_cat = {row["AtomicUnitID"]: row.get("CategoryID", "") for row in ledger_rows}
    resolved: list[dict[str, str]] = []
    for row in findings:
        atom_id = row["AtomicUnitID"]
        prior = row.get("AssignedCategoryID", "")
        final = final_cat.get(atom_id, prior)
        change = changes.get(atom_id)
        rule_id = change["RuleID"] if change else rule_for_finding(row, final)
        note = change["Note"] if change else "Forced category decision retained under Gate 3 boundary rules."
        resolved.append(
            {
                "FindingID": row["FindingID"],
                "AtomicUnitID": atom_id,
                "SourceDoc": row["SourceDoc"],
                "PriorAssignedCategoryID": prior,
                "AssignedCategoryID": final,
                "CandidateCategoryIDs": row.get("CandidateCategoryIDs", ""),
                "FindingType": row.get("FindingType", ""),
                "Severity": row.get("Severity", "ADVISORY"),
                "Status": "RESOLVED_FORCED_DECISION",
                "Evidence": row.get("Evidence", ""),
                "Recommendation": "No atom split in this refinement; assignment resolved by primary-function boundary rule.",
                "ResolutionRuleID": rule_id,
                "ResolutionNote": note,
            }
        )
    return resolved


def rule_for_finding(row: dict[str, str], final: str) -> str:
    cats = {row.get("AssignedCategoryID", ""), final}
    for token in row.get("CandidateCategoryIDs", "").split(";"):
        if ":" in token:
            cats.add(token.split(":", 1)[0].strip())
    if "CAT-011" in cats:
        return "G3BR-010" if final == "CAT-011" else "G3BR-008"
    if "CAT-005" in cats:
        return "G3BR-009"
    if "CAT-008" in cats:
        return "G3BR-005"
    if "CAT-006" in cats:
        return "G3BR-006"
    if "CAT-007" in cats:
        return "G3BR-007"
    if "CAT-004" in cats:
        return "G3BR-004"
    if "CAT-003" in cats:
        return "G3BR-003"
    if "CAT-002" in cats:
        return "G3BR-002"
    return "G3BR-001"


def ratify_categories(
    snapshot: Path,
    category_rows: list[dict[str, str]],
    ledger_rows: list[dict[str, str]],
    cosine_threshold: float,
) -> list[dict[str, str]]:
    import bm25s
    from fastembed import TextEmbedding

    atom_to_category = {
        row["AtomicUnitID"]: row["CategoryID"]
        for row in ledger_rows
        if row.get("InOutStatus") == "IN" and row.get("CategoryID")
    }
    by_category: dict[str, set[str]] = defaultdict(set)
    for atom_id, category_id in atom_to_category.items():
        by_category[category_id].add(atom_id)

    con = sqlite3.connect(str(snapshot / "catalog.sqlite"))
    con.row_factory = sqlite3.Row
    chunk_rows = [
        dict(row)
        for row in con.execute(
            """
            SELECT ir.row_index, c.atomic_unit_id, c.chunk_type
            FROM index_rows ir
            JOIN chunks c ON c.chunk_id = ir.chunk_id
            WHERE ir.index_name = 'source_v2'
              AND c.archive_state = 'ACTIVE'
            ORDER BY ir.row_index
            """
        ).fetchall()
    ]
    con.close()
    row_to_atom = {
        int(row["row_index"]): row["atomic_unit_id"]
        for row in chunk_rows
        if row["chunk_type"] == "LEDGER_ATOM" and row["atomic_unit_id"]
    }
    atom_to_row = {atom_id: row for row, atom_id in row_to_atom.items()}
    atom_rows = np.asarray(sorted(row_to_atom), dtype=np.int64)
    bm25 = bm25s.BM25.load(str(snapshot / "bm25"))
    row_count = len(chunk_rows)

    meta = json.loads((snapshot / "meta.json").read_text(encoding="utf-8"))
    retrieval_meta = meta.get("retrieval_index", {})
    dense_status = retrieval_meta.get("status") or "UNKNOWN"
    embeddings_path = retrieval_meta.get("embeddings_norm")
    embeddings = None
    model = None
    if embeddings_path and (snapshot / embeddings_path).exists():
        embeddings = np.load(snapshot / embeddings_path)
        model = TextEmbedding(model_name=retrieval_meta.get("embedding_model") or "BAAI/bge-base-en-v1.5")

    out: list[dict[str, str]] = []
    for category in category_rows:
        cat_id = category["CategoryID"]
        mapped_atoms = sorted(by_category.get(cat_id, set()))
        mapped_rows = [atom_to_row[a] for a in mapped_atoms if a in atom_to_row]
        k = max(50, 2 * len(mapped_atoms))
        query = " ".join(
            [
                category["Name"],
                category["ScopeDescription"],
                category["InclusionCriteria"],
                category["Exclusions"],
                category["Query"],
            ]
        )

        bm25_atoms = bm25_atom_topk(bm25, query, row_count, row_to_atom, k)
        bm25_hits = len(set(bm25_atoms) & set(mapped_atoms))

        dense_atoms: list[str] = []
        cosine_stats = empty_cosine_stats()
        dense_hits = 0
        below = ""
        if embeddings is not None and model is not None:
            qv = np.asarray(next(iter(model.embed([query]))), dtype=np.float32)
            norm = np.linalg.norm(qv)
            if norm > 0:
                qv = qv / norm
            sims = embeddings @ qv
            dense_atoms = dense_atom_topk(sims, atom_rows, row_to_atom, k)
            dense_hits = len(set(dense_atoms) & set(mapped_atoms))
            if mapped_rows:
                mapped_sims = sims[np.asarray(mapped_rows, dtype=np.int64)]
                cosine_stats = cosine_summary(mapped_sims)
                below = str(int(np.sum(mapped_sims < cosine_threshold)))

        verdict = "SCOPE_REFINEMENT_NEEDED"
        blocking = "YES"
        notes = (
            "Gate 3 boundary rules applied and assignment findings resolved. "
            "Default 0.75 cosine threshold still blocks closure pending explicit "
            "human approval of a calibrated dense-ratification basis."
        )
        out.append(
            {
                "CategoryID": cat_id,
                "Name": category["Name"],
                "MappedInAtoms": str(len(mapped_atoms)),
                "ScopeQuery": query,
                "BM25TopK": str(k),
                "BM25TopKAssignedHits": str(bm25_hits),
                "BM25PrecisionAtK": ratio(bm25_hits, k),
                "BM25CategoryRecallAtK": ratio(bm25_hits, len(mapped_atoms)),
                "BM25AssignmentMissCount": str(max(0, len(mapped_atoms) - bm25_hits)),
                "DenseIndexStatus": dense_status,
                "DenseTopK": str(k if embeddings is not None else 0),
                "DenseTopKAssignedHits": str(dense_hits if embeddings is not None else ""),
                "DensePrecisionAtK": ratio(dense_hits, k) if embeddings is not None else "",
                "DenseCategoryRecallAtK": ratio(dense_hits, len(mapped_atoms)) if embeddings is not None else "",
                "DenseAssignmentMissCount": str(max(0, len(mapped_atoms) - dense_hits)) if embeddings is not None else "",
                "CosineThreshold": f"{cosine_threshold:.2f}",
                "CosineBelowThresholdCount": below,
                "CosineMin": cosine_stats["min"],
                "CosineP05": cosine_stats["p05"],
                "CosineP25": cosine_stats["p25"],
                "CosineMedian": cosine_stats["median"],
                "CosineP75": cosine_stats["p75"],
                "CosineMax": cosine_stats["max"],
                "Verdict": verdict,
                "Blocking": blocking,
                "Notes": notes,
            }
        )
    return out


def bm25_atom_topk(bm25: Any, query: str, row_count: int, row_to_atom: dict[int, str], k: int) -> list[str]:
    import bm25s

    tokens = bm25s.tokenize([query], stopwords="en", show_progress=False)
    docs, _scores = bm25.retrieve(tokens, k=row_count, show_progress=False)
    atoms: list[str] = []
    seen: set[str] = set()
    for row_index in docs[0]:
        atom_id = row_to_atom.get(int(row_index))
        if atom_id and atom_id not in seen:
            atoms.append(atom_id)
            seen.add(atom_id)
            if len(atoms) >= k:
                break
    return atoms


def dense_atom_topk(sims: np.ndarray, atom_rows: np.ndarray, row_to_atom: dict[int, str], k: int) -> list[str]:
    atom_sims = sims[atom_rows]
    kk = min(k, atom_sims.shape[0])
    if kk == 0:
        return []
    part = np.argpartition(-atom_sims, kk - 1)[:kk]
    ordered = part[np.argsort(-atom_sims[part])]
    return [row_to_atom[int(atom_rows[i])] for i in ordered]


def empty_cosine_stats() -> dict[str, str]:
    return {key: "" for key in ["min", "p05", "p25", "median", "p75", "max"]}


def cosine_summary(values: np.ndarray) -> dict[str, str]:
    return {
        "min": f"{float(np.min(values)):.4f}",
        "p05": f"{float(np.quantile(values, 0.05)):.4f}",
        "p25": f"{float(np.quantile(values, 0.25)):.4f}",
        "median": f"{float(np.median(values)):.4f}",
        "p75": f"{float(np.quantile(values, 0.75)):.4f}",
        "max": f"{float(np.max(values)):.4f}",
    }


def ratio(num: int, denom: int) -> str:
    if denom <= 0:
        return "0.0000"
    return f"{num / denom:.4f}"


def build_assignment_summary(
    category_rows: list[dict[str, str]],
    ledger_rows: list[dict[str, str]],
    findings_rows: list[dict[str, str]],
    ratification_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    counts = Counter(row["CategoryID"] for row in ledger_rows if row.get("InOutStatus") == "IN")
    open_findings = Counter(
        row["AssignedCategoryID"] for row in findings_rows if row.get("Status", "").startswith("OPEN")
    )
    resolved_findings = Counter(
        row["AssignedCategoryID"] for row in findings_rows if row.get("Status", "").startswith("RESOLVED")
    )
    verdicts = {row["CategoryID"]: row["Verdict"] for row in ratification_rows}
    blocking = {row["CategoryID"]: row["Blocking"] for row in ratification_rows}
    return [
        {
            "CategoryID": row["CategoryID"],
            "Name": row["Name"],
            "InAtoms": str(counts[row["CategoryID"]]),
            "OpenAssignmentFindings": str(open_findings[row["CategoryID"]]),
            "ResolvedAssignmentFindings": str(resolved_findings[row["CategoryID"]]),
            "ScopeVerdict": verdicts.get(row["CategoryID"], ""),
            "Blocking": blocking.get(row["CategoryID"], ""),
        }
        for row in category_rows
    ]


def build_findings_summary(
    category_rows: list[dict[str, str]],
    findings_rows: list[dict[str, str]],
    changes: dict[str, dict[str, str]],
) -> list[dict[str, str]]:
    category_names = {row["CategoryID"]: row["Name"] for row in category_rows}
    changes_by_new_category = Counter(change["NewCategoryID"] for change in changes.values())
    by_cat: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in findings_rows:
        by_cat[row["AssignedCategoryID"]].append(row)
    out = []
    for cat_id in category_names:
        rows = by_cat.get(cat_id, [])
        out.append(
            {
                "CategoryID": cat_id,
                "CategoryName": category_names[cat_id],
                "OpenFindingCount": str(sum(1 for row in rows if row["Status"].startswith("OPEN"))),
                "ResolvedFindingCount": str(sum(1 for row in rows if row["Status"].startswith("RESOLVED"))),
                "ChangedAssignmentCount": str(changes_by_new_category[cat_id]),
                "TopSourceDocs": join_counts(Counter(row["SourceDoc"] for row in rows), 8),
                "TopAlternateCategories": top_alternates(rows, cat_id),
                "RecommendedReviewMode": "resolved by Gate 3 boundary rule; spot-check changed assignments and dense calibration basis",
            }
        )
    return out


def join_counts(counter: Counter[str], limit: int) -> str:
    return "; ".join(f"{key}:{value}" for key, value in counter.most_common(limit))


def top_alternates(rows: list[dict[str, str]], assigned: str) -> str:
    counter: Counter[str] = Counter()
    for row in rows:
        for token in row.get("CandidateCategoryIDs", "").split(";"):
            if ":" not in token:
                continue
            cat_id, _score = token.split(":", 1)
            cat_id = cat_id.strip()
            if cat_id and cat_id != assigned:
                counter[cat_id] += 1
    return join_counts(counter, 8)


def write_calibration_note(path: Path, ratification_rows: list[dict[str, str]], generated_iso: str) -> None:
    lines = [
        "# Gate 3 Dense Ratification Calibration Note",
        "",
        f"Generated: {generated_iso}",
        "",
        "This note records the Gate 3 dense-ratification basis after category boundary refinement. It is not a Gate 3 acceptance record.",
        "",
        "The default cosine threshold remains `0.75`. Under that threshold every Category remains blocking because query-to-atom cosine scores for this corpus/model sit well below `0.75` even after scope refinement. The threshold therefore behaves as an uncalibrated diagnostic, not as a usable pass/fail floor for this source_v2 index.",
        "",
        "Gate 3 can close only after the human explicitly accepts a calibrated dense-ratification basis or directs further refinement. No atom text was split or edited in this refinement.",
        "",
        "| CategoryID | Mapped IN | Dense recall | Cosine p05 | Cosine median | Cosine max | Default verdict |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    for row in ratification_rows:
        lines.append(
            f"| `{row['CategoryID']}` | {row['MappedInAtoms']} | {row['DenseCategoryRecallAtK']} | "
            f"{row['CosineP05']} | {row['CosineMedian']} | {row['CosineMax']} | {row['Verdict']} |"
        )
    lines.extend(
        [
            "",
            "Proposed calibrated basis for human review:",
            "",
            "- Treat dense cosine as corpus-relative evidence over `LEDGER_ATOM` chunks, not as a universal absolute semantic-similarity threshold.",
            "- Keep the 11-category flat partition and primary-function boundary rules as the controlling semantic decision surface.",
            "- Use BM25/dense recall and cosine distribution outliers to guide spot review, while requiring explicit human acceptance before replacing the default `0.75` closure threshold.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_review_packet(
    path: Path,
    category_rows: list[dict[str, str]],
    findings_rows: list[dict[str, str]],
    changes: dict[str, dict[str, str]],
    generated_iso: str,
) -> None:
    by_cat = defaultdict(list)
    for row in findings_rows:
        by_cat[row["AssignedCategoryID"]].append(row)
    changes_by_new_category = Counter(change["NewCategoryID"] for change in changes.values())
    lines = [
        "# Gate 3 Category Assignment Review Packet",
        "",
        f"Generated: {generated_iso}",
        "",
        "## Purpose",
        "",
        "This packet summarizes the Gate 3 assignment refinement. It is a review aid, not an acceptance record.",
        "",
        "## Current Counts",
        "",
        f"- Original ambiguous assignment findings: {len(findings_rows)}",
        f"- Open ambiguous assignment findings: {sum(1 for row in findings_rows if row['Status'].startswith('OPEN'))}",
        f"- Resolved forced decisions: {sum(1 for row in findings_rows if row['Status'].startswith('RESOLVED'))}",
        f"- Assignment changes applied to draft ledger: {len(changes)}",
        "- Atom splits: 0",
        "",
        "## Category Summary",
        "",
        "| CategoryID | Category | Resolved findings | Changed assignments | Top source docs |",
        "|---|---|---:|---:|---|",
    ]
    for category in category_rows:
        cat_id = category["CategoryID"]
        rows = by_cat.get(cat_id, [])
        changed = changes_by_new_category[cat_id]
        lines.append(
            f"| `{cat_id}` | {category['Name']} | {len(rows)} | {changed} | {join_counts(Counter(row['SourceDoc'] for row in rows), 6)} |"
        )
    lines.extend(
        [
            "",
            "## Boundary Decisions",
            "",
        ]
    )
    for decision in BOUNDARY_DECISIONS:
        lines.append(f"- `{decision['RuleID']}` {decision['Decision']}: {decision['Rule']}")
    if changes:
        lines.extend(["", "## Changed Assignment Samples", ""])
        for atom_id, change in list(changes.items())[:50]:
            lines.append(
                f"- `{atom_id}` `{change['OldCategoryID']}` -> `{change['NewCategoryID']}` by `{change['RuleID']}`: {change['Note']}"
            )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_gate3_report(
    path: Path,
    ratification_rows: list[dict[str, str]],
    findings_rows: list[dict[str, str]],
    changes: dict[str, dict[str, str]],
    generated_iso: str,
    snapshot: Path,
) -> None:
    lines = [
        "# Gate 3 Category Refinement - Chirality DOMAIN_DECOMP",
        "",
        f"Generated: {generated_iso}",
        "",
        "## Status",
        "",
        "Gate 3 remains open. Category scopes and primary-function boundary rules were refined, all existing ambiguous assignment findings were closed as forced decisions, and category-scope ratification was rerun against the current source_v2 index.",
        "",
        f"Source index snapshot: `{snapshot}`",
        "",
        "No atom text was split or edited; no source catalog rebuild is required for this refinement.",
        "",
        "## Results",
        "",
        f"- Assignment changes applied: {len(changes)}",
        f"- Open assignment findings: {sum(1 for row in findings_rows if row['Status'].startswith('OPEN'))}",
        f"- Resolved assignment findings: {sum(1 for row in findings_rows if row['Status'].startswith('RESOLVED'))}",
        f"- Blocking scope verdicts under default 0.75 cosine threshold: {sum(1 for row in ratification_rows if row['Blocking'] == 'YES')}",
        "",
        "| CategoryID | Mapped IN | Dense recall | Cosine median | Verdict |",
        "|---|---:|---:|---:|---|",
    ]
    for row in ratification_rows:
        lines.append(
            f"| `{row['CategoryID']}` | {row['MappedInAtoms']} | {row['DenseCategoryRecallAtK']} | {row['CosineMedian']} | {row['Verdict']} |"
        )
    lines.extend(
        [
            "",
            "## Gate 3 Closure Condition",
            "",
            "Gate 3 cannot close until the human explicitly accepts a calibrated dense-ratification basis or directs further category refinement.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_handoff(
    path: Path,
    ratification_rows: list[dict[str, str]],
    findings_rows: list[dict[str, str]],
    generated_iso: str,
    snapshot: Path,
) -> None:
    lines = [
        "# Gate 3 Handoff State - Category Refinement",
        "",
        f"Generated: {generated_iso}",
        "",
        "## Verdict",
        "",
        "Gate 3 is OPEN. Category boundary refinement is complete, and ambiguous assignment findings are resolved by forced decisions. Closure remains blocked by default dense-ratification threshold calibration.",
        "",
        "## Accepted Upstream Snapshot(s)",
        "",
        "- `domains/chirality/_Decomposition/gate_snapshots/GATE2_PHASE2_20260614T204403Z/`",
        "- `domains/chirality/_Decomposition/gate_snapshots/GATE2_PHASE2_SOURCE_UNIT_AUTHORITY_20260614T211725Z/`",
        f"- `{snapshot}` (`READY`, BM25 + dense)",
        "",
        "## Current Gate 3 Artifacts",
        "",
        "- `domains/chirality/_Decomposition/Category_Register.csv`",
        "- `domains/chirality/_Decomposition/Domain_Ledger_Gate3_Category_Draft.csv`",
        "- `domains/chirality/_Decomposition/Category_Scope_Ratification.csv`",
        "- `domains/chirality/_Decomposition/Category_Assignment_Findings.csv`",
        "- `domains/chirality/_Decomposition/Category_Boundary_Decisions.csv`",
        "- `domains/chirality/_Decomposition/Gate3_Ratification_Calibration.md`",
        "",
        "## Rerun Requirements",
        "",
        "- If the human accepts a calibrated dense basis without atom text edits, no source index rebuild is required.",
        "- If any atom is split or any UnitStatement changes, rebuild the source database and retrieval index before ratification resumes.",
        "- If category scopes or assignments change again, rerun this refinement/ratification helper.",
        "",
        "## Remaining Blockers",
        "",
        f"- Blocking scope verdicts under default threshold: {sum(1 for row in ratification_rows if row['Blocking'] == 'YES')}",
        f"- Open ambiguous assignment findings: {sum(1 for row in findings_rows if row['Status'].startswith('OPEN'))}",
        "- Human has not yet accepted a calibrated dense-ratification threshold/basis for Gate 3 closure.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
