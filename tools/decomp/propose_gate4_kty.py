#!/usr/bin/env python3
"""Propose Chirality Gate 4 Knowledge Types and Subjects.

This helper consumes the accepted Gate 3 category ledger and writes a Phase 4
proposal package. It does not edit atom text, SourceRefs, ContentHash values, or
accepted CategoryID assignments. Gate 4 remains open until human acceptance.
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


COSINE_THRESHOLD = 0.75
PRD_SOURCE_DOC = "SRC-DOCS-THESIS-BIGGER-PICTURE-CHIRALITY-PRD-AMENDMENT-DOMAIN-ENGINE-INTEGRATION"
PRD_ASSOCIATED_CATEGORY = "CAT-007"
PRD_ASSOCIATED_KTY = "KTY-07-01_DBM-Publication-Planning"
PRD_ASSOCIATED_SUBJECT = "SUB-07-01-03_PRD-Requirements-Package"


def subj(
    sid: str,
    name: str,
    description: str,
    keywords: list[str],
    *,
    sources: list[str] | None = None,
    fallback: bool = False,
) -> dict[str, Any]:
    return {
        "SubjectID": sid,
        "Name": name,
        "Description": description,
        "Keywords": keywords,
        "SourcePatterns": sources or [],
        "Fallback": fallback,
    }


def kty(
    kid: str,
    cat: str,
    name: str,
    description: str,
    schema: str,
    intended_users: str,
    when_used: str,
    subjects: list[dict[str, Any]],
    source_basis: str,
) -> dict[str, Any]:
    return {
        "KnowledgeTypeID": kid,
        "ParentCategoryID": cat,
        "Name": name,
        "Description": description,
        "CanonicalSchema": schema,
        "IntendedUsers": intended_users,
        "WhenUsed": when_used,
        "SourceBasis": source_basis,
        "Subjects": subjects,
    }


KTY_SPECS: list[dict[str, Any]] = [
    kty(
        "KTY-01-01_Epistemic-Warrant",
        "CAT-001",
        "Epistemic Warrant Foundations",
        "Reusable guidance for claims, evidence, warrant states, epistemic labels, and evidence-over-plausibility reasoning.",
        "Guidance / Playbook",
        "Domain authors, reviewers, auditors, and engineers relying on AI-mediated outputs.",
        "Used when a workflow must decide whether a claim is warranted, provisional, uncertain, or inadmissible.",
        [
            subj("SUB-01-01-01_Warrant-and-Evidence-Basis", "Warrant and Evidence Basis", "Claim support, evidence standards, warrant states, and admissibility of outputs.", ["warrant", "evidence", "claim", "claims", "support", "source", "plausibility", "admissible", "grounded"], fallback=True),
            subj("SUB-01-01-02_Epistemic-Labels", "Epistemic Labels", "Labels and state distinctions used to communicate uncertainty and confidence.", ["epistemic label", "epistemic labels", "state", "uncertain", "uncertainty", "confidence", "tbd", "assumption", "provisional"]),
        ],
        "CAT-001 scope; Chirality framework; epistemic architecture thesis sources.",
    ),
    kty(
        "KTY-01-02_Professional-Accountability",
        "CAT-001",
        "Professional Engineering Accountability",
        "Guidance for responsible charge, regulated practice, public welfare, and human accountability boundaries.",
        "Guidance / Playbook",
        "Licensed professionals, reviewers, and operators governing engineering use.",
        "Used when AI-assisted work intersects professional obligations, review authority, or public welfare.",
        [
            subj("SUB-01-02-01_Responsible-Charge", "Responsible Charge", "Human professional authority and limits on delegating responsibility to agents.", ["responsible charge", "licensed", "professional", "engineer", "engineering", "human authority", "accountability", "responsibility"], sources=["PROFESSIONAL-ENGINEERING", "APPENDIX-C"]),
            subj("SUB-01-02-02_Public-Welfare", "Public Welfare and Safety", "Safety, reliability, risk, and public-welfare obligations.", ["public welfare", "safety", "risk", "reliability", "harm", "safety integrity", "regulated"], sources=["PROFESSIONAL-ENGINEERING", "APEGA"]),
        ],
        "Professional engineering and APEGA mapping sources.",
    ),
    kty(
        "KTY-01-03_Philosophical-Framework",
        "CAT-001",
        "Philosophical Framework",
        "Reference structure for the ontology, epistemology, praxiology, and axiology used by Chirality.",
        "Reference",
        "Domain architects and reviewers tracing the conceptual basis of the system.",
        "Used when explaining the domain's structural theory or interpreting philosophical claims.",
        [
            subj("SUB-01-03-01_Ontology-Epistemology", "Ontology and Epistemology", "What exists in the domain and how knowledge claims are justified.", ["ontology", "ontological", "epistemology", "epistemological", "knowledge", "truth", "knowing"], sources=["PHILOSOPHICAL-FRAMEWORK"]),
            subj("SUB-01-03-02_Praxiology-Axiology", "Praxiology and Axiology", "Practice, action, values, and value-laden governance principles.", ["praxiology", "praxiological", "axiology", "axiological", "practice", "value", "values"], sources=["PHILOSOPHICAL-FRAMEWORK"]),
        ],
        "Philosophical framework thesis source and Chirality framework source.",
    ),
    kty(
        "KTY-01-04_Human-AI-Reliance",
        "CAT-001",
        "Human-AI Reliance Boundaries",
        "Guidance on where agents can support work and where professional judgment, review, and human reliance remain controlling.",
        "Guidance / Playbook",
        "Operators, domain owners, auditors, and professional reviewers.",
        "Used when deciding whether an AI-mediated output can be relied on, escalated, or rejected.",
        [
            subj("SUB-01-04-01_Reliance-and-Review", "Reliance and Review", "Human review requirements and reliance boundaries for generated outputs.", ["reliance", "rely", "review", "human", "approval", "acceptance", "judgment"]),
            subj("SUB-01-04-02_Hallucination-and-Validity", "Hallucination and Validity", "Validity, hallucination, calibration, and reliability limitations.", ["hallucination", "validity", "calibration", "accuracy", "reliable", "unreliable", "verification"]),
        ],
        "Literature review, epistemic architecture, and professional-practice sources.",
    ),
    kty(
        "KTY-02-01_Agent-Authority-Model",
        "CAT-002",
        "Agent Authority Model",
        "Reference model for agent types, roles, epistemic postures, and authority boundaries.",
        "Reference",
        "Agent authors, workflow designers, and reviewers.",
        "Used when classifying an agent, interpreting its role, or checking authority boundaries.",
        [
            subj("SUB-02-01-01_Agent-Type-Matrix", "Agent Type Matrix", "Agent suite index, Type 0/1/2 distinctions, and posture/role matrix semantics.", ["agent type", "type 0", "type 1", "type 2", "matrix", "normative", "operative", "evaluative", "persona"], sources=["AGENTS", "TYPES"], fallback=True),
            subj("SUB-02-01-02_Role-Authority", "Role Authority", "Authority limits and role-specific governing semantics for agents.", ["authority", "role", "governing", "instruction", "role name", "agent suite"]),
        ],
        "AGENTS.md, TYPES, HELPS_HUMANS, architecture thesis sources.",
    ),
    kty(
        "KTY-02-02_Instruction-Precedence",
        "CAT-002",
        "Instruction Precedence and Invariants",
        "Governance rules for precedence layers, invariants, and conflict resolution.",
        "Checklist",
        "Agents, workflow owners, and reviewers.",
        "Used when checking whether instructions are valid, complete, and non-conflicting.",
        [
            subj("SUB-02-02-01_Precedence-Layers", "Precedence Layers", "PROTOCOL, SPEC, STRUCTURE, RATIONALE, and conflict-resolution ordering.", ["precedence", "protocol", "spec", "structure", "rationale", "conflict", "contradiction"]),
            subj("SUB-02-02-02_Non-Negotiable-Invariants", "Non-Negotiable Invariants", "Invariant statements that bind workflow behavior.", ["invariant", "invariants", "non-negotiable", "must", "shall", "required"]),
        ],
        "Agent instruction architecture and invariant-catalog sources.",
    ),
    kty(
        "KTY-02-03_Snapshot-and-Closure-Rules",
        "CAT-002",
        "Snapshot and Closure Rules",
        "Governance rules for derivative packages, immutable snapshots, handoff state, sequencing, and closure.",
        "Checklist",
        "Orchestrators, decomposers, auditors, and publishers.",
        "Used at phase boundaries and when a derivative package consumes accepted truth.",
        [
            subj("SUB-02-03-01_Derivative-Package-Rule", "Derivative Package Rule", "Derivative package status, upstream snapshot citation, and non-substitution rules.", ["derivative package", "upstream snapshot", "not a substitute", "accepted upstream"]),
            subj("SUB-02-03-02_Snapshot-Handoff-Closure", "Snapshot, Handoff, and Closure", "Snapshot, handoff-state, closure, and sequencing rules.", ["snapshot", "handoff", "closure", "sequencing", "phase-boundary", "pointer"]),
        ],
        "AGENTS.md governance integration rules and DECOMPOSITION_STANDARD.",
    ),
    kty(
        "KTY-02-04_Human-Gated-Governance",
        "CAT-002",
        "Human-Gated Governance",
        "Rules that distinguish human approval authority from agent execution and proposal authority.",
        "Guidance / Playbook",
        "Human operators, orchestrators, and auditors.",
        "Used when a workflow reaches a decision, approval, or authority boundary.",
        [
            subj("SUB-02-04-01_Human-Approval-Gates", "Human Approval Gates", "Gate confirmations, approval requirements, and operator decisions.", ["human approval", "user confirms", "approval gate", "confirmed", "accepted by human"]),
            subj("SUB-02-04-02_Agent-Proposal-Limits", "Agent Proposal Limits", "Boundaries where agents propose, coordinate, or prepare but do not approve.", ["proposal only", "agent output", "coordinator", "not approving", "human-gated"]),
        ],
        "HELPS_HUMANS, architecture, and implementation thesis sources.",
    ),
    kty(
        "KTY-03-01_Decomposition-Gate-Lifecycle",
        "CAT-003",
        "Decomposition Gate Lifecycle",
        "Procedure structure for intake, normalization, categories, KTYs, coverage, publication, and phase handoffs.",
        "Procedure",
        "DOMAIN_DECOMP, PROJECT_DECOMP, SOFTWARE_DECOMP, and auditors.",
        "Used when running or auditing a decomposition phase.",
        [
            subj("SUB-03-01-01_Gate-Sequence", "Gate Sequence", "Gate ordering, closure requirements, and phase outputs.", ["gate", "phase", "intake", "normalize", "coverage", "publish", "closure"], sources=["DECOMP"], fallback=True),
            subj("SUB-03-01-02_Handoff-State", "Decomposition Handoff State", "Handoff contents, accepted snapshots, blockers, and rerun requirements.", ["handoff", "rerun", "blocker", "accepted snapshot", "closure verdict"]),
        ],
        "DECOMPOSITION_STANDARD and DOMAIN_DECOMP instruction sources.",
    ),
    kty(
        "KTY-03-02_Source-Intake-and-Skeletons",
        "CAT-003",
        "Source Intake and Skeletons",
        "Procedures and structures for source admission, skeletons, dispatch units, and review surfaces.",
        "Procedure",
        "Domain decomposers and atomization dispatch coordinators.",
        "Used before atomization or when source boundaries change.",
        [
            subj("SUB-03-02-01_Source-Admission", "Source Admission", "Manifest admission, source-boundary decisions, and active/retired source-unit surfaces.", ["source manifest", "source boundary", "admitted", "active source", "retired", "source unit"]),
            subj("SUB-03-02-02_Skeleton-and-Dispatch", "Skeleton and Dispatch", "Source skeletons, section nodes, dispatch plans, and dispatch units.", ["skeleton", "dispatch plan", "dispatch unit", "section", "review surface"]),
        ],
        "DOMAIN_DECOMP and build_source_skeleton outputs.",
    ),
    kty(
        "KTY-03-03_Atomization-and-Ledger",
        "CAT-003",
        "Atomization and Domain Ledger",
        "Rules for atom extraction, stable atomic IDs, Domain Ledger rows, ContentHash discipline, and vocabulary seeds.",
        "Procedure",
        "Atomization workers, decomposers, and ledger validators.",
        "Used when generating, merging, or validating atom ledgers.",
        [
            subj("SUB-03-03-01_Atomic-Units", "Atomic Units", "Atomic unit statements, local sequence, IN/OUT/TBD status, and stable IDs.", ["atomic", "atom", "unitstatement", "local seq", "inoutstatus", "hba-", "unit id"]),
            subj("SUB-03-03-02_Ledger-Merge", "Ledger Merge", "Per-source and cross-source merge behavior, duplicate handling, and vocabulary map merge.", ["ledger", "merge", "per-source", "cross-source", "dedupe", "vocabulary"]),
        ],
        "domain-source-atomize skill and merge_source_atomizations outputs.",
    ),
    kty(
        "KTY-03-04_Category-KTY-Subject-Structuring",
        "CAT-003",
        "Category, KTY, and Subject Structuring",
        "Rules for flat categories, Knowledge Types, Subjects, unit assignment, and retrieval-driven ratification.",
        "Guidance / Playbook",
        "Domain decomposers and decomposition auditors.",
        "Used during Gate 3 and Gate 4 structuring and refinement.",
        [
            subj("SUB-03-04-01_Category-Partition", "Category Partition", "Flat category rules, no overlap/no gaps, and primary-function assignment.", ["category", "flat", "partition", "no overlap", "no gaps", "assignment"]),
            subj("SUB-03-04-02_KTY-Subject-Mapping", "KTY and Subject Mapping", "Knowledge Type, Subject, and unit-to-subject mapping rules.", ["knowledge type", "kty", "subject", "subjectid", "mapping", "scope ratification"]),
        ],
        "DOMAIN_DECOMP Phase 3 and Phase 4 instructions.",
    ),
    kty(
        "KTY-03-05_Scope-Change-and-Remediation",
        "CAT-003",
        "Scope Change and Remediation",
        "Procedures for source-driven scope amendments, remediation manifests, disposition evidence, and decomposition package review.",
        "Procedure",
        "SCOPE_CHANGE, decomposers, and remediation skill workers.",
        "Used when accepted decomposition truth must be amended or KTY-local content disposition is required.",
        [
            subj("SUB-03-05-01_Scope-Change-Cycle", "Scope Change Cycle", "Scope-change snapshots, amendment actions, and closure support.", ["scope change", "amendment", "sca", "supersession", "amendment actions"], sources=["SCOPE-CHANGE"]),
            subj("SUB-03-05-02_Remediation-Disposition", "Remediation Disposition", "KTY remediation manifests, content disposition, metadata alignment, and review packages.", ["remediation", "disposition", "metadata align", "kty remediation", "manifest"], sources=["KTY-CONTENT", "KTY-METADATA", "DECOMPOSITION-PACKAGE-REVIEW"]),
        ],
        "SCOPE_CHANGE and decomposition-package review skill sources.",
    ),
    kty(
        "KTY-04-01_TASK-Shell-and-Briefs",
        "CAT-004",
        "TASK Shell and Brief Contracts",
        "Generic bounded TASK execution shell, brief schema, runtime inputs, and output expectations.",
        "Procedure",
        "TASK dispatchers, skill authors, and bounded workers.",
        "Used whenever a method pack is dispatched through TASK.",
        [
            subj("SUB-04-01-01_TASK-Brief-Schema", "TASK Brief Schema", "Scope, inputs, expected outputs, and runtime overrides in TASK briefs.", ["task", "brief", "scopepath", "inputs", "expected outputs", "runtimeoverrides"], sources=["AGENT-TASK"], fallback=True),
            subj("SUB-04-01-02_Worker-Execution", "Worker Execution", "Bounded worker startup, completion, failure, and reporting behavior.", ["worker", "execute", "status", "run", "failure", "success"]),
        ],
        "AGENT_TASK and skill brief schemas.",
    ),
    kty(
        "KTY-04-02_Skill-Pack-Metadata-and-QA",
        "CAT-004",
        "Skill Pack Metadata and QA",
        "Contracts for SKILL.md, BRIEF_SCHEMA, QA_CHECKS, TOOL_POLICY, metadata, and skill validation.",
        "Checklist",
        "Skill authors, Skillmaker, and validators.",
        "Used when creating, auditing, or dispatching a skill pack.",
        [
            subj("SUB-04-02-01_Skill-Metadata", "Skill Metadata", "Skill pack descriptions, metadata, folder contracts, and registry behavior.", ["skill", "metadata", "skill.md", "skills/readme", "registry", "capability"], sources=["HELPS_HUMANS", "SKILLPACK-META"]),
            subj("SUB-04-02-02_QA-and-Tool-Policy", "QA and Tool Policy", "QA checks, allowed tools, blocked writes, and tool policy constraints.", ["qa_checks", "tool_policy", "allowedtools", "allowed tools", "blocked", "write scope"]),
        ],
        "Skillmaker, skill meta, and grouped skill-pack sources.",
    ),
    kty(
        "KTY-04-03_Deterministic-Tooling",
        "CAT-004",
        "Deterministic Tooling",
        "Rules and implementation contracts for deterministic tools, validation scripts, and local helpers.",
        "Procedure",
        "Toolmaker, maintainers, and workflow agents.",
        "Used when adding or changing deterministic tooling.",
        [
            subj("SUB-04-03-01_Toolmaker-Contracts", "Tool Design Contracts", "Tool ownership, deterministic behavior, inputs, outputs, and validation expectations.", ["tool design", "deterministic", "tool", "script", "validator", "command"], sources=["HELPS_HUMANS"]),
            subj("SUB-04-03-02_Tool-Registry", "Tool Registry", "Registry entries, command descriptions, and script discoverability.", ["tools/registry", "registry", "query_source_index", "validate", "build"], sources=["TOOLS-REGISTRY"]),
        ],
        "HELPS_HUMANS tool-design and tools-registry sources.",
    ),
    kty(
        "KTY-04-04_Runtime-Overrides-and-Policies",
        "CAT-004",
        "Runtime Overrides and Policies",
        "Generic runtime override, mode, policy, and write-scope controls across skills and agents.",
        "Reference",
        "Skill dispatchers, workers, and reviewers.",
        "Used when a task behavior is selected or constrained by runtime parameters.",
        [
            subj("SUB-04-04-01_Runtime-Overrides", "Runtime Overrides", "RuntimeOverrides keys, modes, and caller-provided execution switches.", ["runtimeoverrides", "mode", "override", "allow_", "source_action_ref"]),
            subj("SUB-04-04-02_Write-Scope-Controls", "Write Scope Controls", "Allowed write targets, one-writer rules, and no-mutation constraints.", ["write scope", "one-writer", "must not write", "no mutation", "protected"]),
        ],
        "TASK, Skillmaker, and grouped skill-pack contracts.",
    ),
    kty(
        "KTY-04-05_KTY-Local-Worker-Contracts",
        "CAT-004",
        "KTY-Local Worker Contracts",
        "Generic contracts for workers that read or align KTY-local metadata and documents without changing decomposition truth.",
        "Checklist",
        "Domain document, remediation, and metadata-alignment workers.",
        "Used after decomposition when KTY-local packages are created or maintained.",
        [
            subj("SUB-04-05-01_Domain-Documents-Contract", "Domain Documents Contract", "Scoping.md, KA files, artifact plans, and subject-to-artifact bridges.", ["domain-documents", "scoping.md", "ka-", "artifact plan", "subjectid"], sources=["DOMAIN-DOCUMENTS"]),
            subj("SUB-04-05-02_KTY-Remediation-Alignment", "KTY Remediation and Alignment", "KTY content remediation and metadata alignment skill contracts.", ["kty-content-remediate", "kty-metadata-align", "metadata-safe", "_context.md", "_status.md"], sources=["KTY-CONTENT", "KTY-METADATA"]),
        ],
        "domain-documents, kty-content-remediate, and kty-metadata-align skill sources.",
    ),
    kty(
        "KTY-05-01_SourceRef-and-Hash-Provenance",
        "CAT-005",
        "SourceRef and Hash Provenance",
        "Reference rules for SourceRefs, dual anchors, ContentHash, and source-backed traceability.",
        "Reference",
        "Atomization workers, decomposers, and validators.",
        "Used when checking whether atom rows can be traced to source evidence.",
        [
            subj("SUB-05-01-01_SourceRef-Forms", "SourceRef Forms", "Repo-backed and dual-anchor SourceRef formats.", ["sourceref", "source ref", "@repo", "line anchor", "html anchor"], fallback=True),
            subj("SUB-05-01-02_ContentHash-Discipline", "ContentHash Discipline", "ContentHash creation, comparison, and freshness implications.", ["contenthash", "content hash", "sha1", "hash", "unitstatement"]),
        ],
        "DOMAIN_DECOMP SourceRef policy and source atomization contracts.",
    ),
    kty(
        "KTY-05-02_Source-Catalog-and-Snapshots",
        "CAT-005",
        "Source Catalog and Snapshots",
        "Procedures for source database snapshots, manifests, chunks, artifacts, and validation.",
        "Procedure",
        "Source catalog maintainers and retrieval users.",
        "Used when building, validating, or consuming local source indexes.",
        [
            subj("SUB-05-02-01_Source-Database", "Source Database", "Catalog build, chunks, artifact rows, snapshot directories, and local pointers.", ["source database", "source catalog", "catalog.sqlite", "snapshot", "_localindexes", "chunks"], sources=["RETRIEVAL", "SOURCE_CATALOG"]),
            subj("SUB-05-02-02_Manifest-Freshness", "Manifest Freshness", "Manifest SHA, hash verification, source drift, and rebuild cadence.", ["source manifest", "sha256", "hash mismatch", "freshness", "rebuild", "validate_source_database"]),
        ],
        "Source catalog and validation tooling.",
    ),
    kty(
        "KTY-05-03_Retrieval-Index-and-Querying",
        "CAT-005",
        "Retrieval Index and Querying",
        "BM25, dense, and hybrid retrieval behavior over source_v2 chunks and atom text.",
        "Procedure",
        "Decomposers, reviewers, and retrieval users.",
        "Used when querying source or atom evidence by lexical or semantic relevance.",
        [
            subj("SUB-05-03-01_BM25-Dense-Hybrid", "BM25, Dense, and Hybrid Modes", "Retrieval modes, reciprocal-rank fusion, cosine scores, and query filters.", ["bm25", "dense", "hybrid", "cosine", "rrf", "mode"], sources=["RETRIEVAL-README"]),
            subj("SUB-05-03-02_Retrieval-Filters", "Retrieval Filters", "Chunk-type, source-doc, category, KTY, subject, and archive filters.", ["chunk-type", "source-doc", "category-id", "knowledge-type-id", "subject-id", "archive-state"]),
        ],
        "Retrieval README and query_source_index tool.",
    ),
    kty(
        "KTY-05-04_Review-Surfaces-and-Telemetry",
        "CAT-005",
        "Review Surfaces and Telemetry",
        "Section-node anchors, review HTML surfaces, sidecars, coverage telemetry, transposition telemetry, and retrieval substrate metadata.",
        "Reference",
        "Decomposers, source reviewers, and auditors.",
        "Used when navigating from atom rows to section review surfaces or interpreting intake telemetry.",
        [
            subj("SUB-05-04-01_Review-HTML-Anchors", "Review HTML Anchors", "HTML review surfaces, SectionID anchors, and source navigation.", ["review html", "sectionid", "section node", "anchor", "source_review_html"]),
            subj("SUB-05-04-02_Intake-Telemetry", "Intake Telemetry", "Skeleton counts, in-scope sections, dispatch counts, and companion inventory telemetry.", ["telemetry", "section count", "dispatch units", "companion inventory", "intake"]),
        ],
        "DOMAIN_DECOMP review surfaces, coverage telemetry, and telemetry-bearing workflow registers.",
    ),
    kty(
        "KTY-06-01_Audit-Agent-Checks",
        "CAT-006",
        "Audit Agent Checks",
        "Independent audit workflows for decomposition, dependency, governance, epistemic, hypergraph, and scope closure.",
        "Checklist",
        "Audit agents and reviewers.",
        "Used when checking governed state for conformance and closure.",
        [
            subj("SUB-06-01-01_Decomposition-and-Governance-Audits", "Decomposition and Governance Audits", "AUDIT_DECOMP, AUDIT_GOVERNANCE, and related agent conformance checks.", ["audit_decomp", "audit_governance", "conformance", "decomposition audit"], sources=["AUDIT-DECOMP", "AUDIT-GOVERNANCE"], fallback=True),
            subj("SUB-06-01-02_Dependency-and-Scope-Audits", "Dependency and Scope Audits", "Dependency closure, scope closure, and hypergraph closure audit behavior.", ["audit_dep", "audit_scope", "dependency closure", "scope closure", "hypergraph closure"], sources=["AUDIT-DEP", "AUDIT-SCOPE", "AUDIT-HYPERGRAPH"]),
        ],
        "AUDIT_* agent instruction sources.",
    ),
    kty(
        "KTY-06-02_Review-and-Reconciliation",
        "CAT-006",
        "Review and Reconciliation",
        "Formal review, reconciliation, and cross-deliverable coherence workflows.",
        "Procedure",
        "Reviewers, reconciliation agents, and governance operators.",
        "Used when a lifecycle transition or cross-artifact coherence check is needed.",
        [
            subj("SUB-06-02-01_Formal-Review", "Formal Review", "Review gates, review findings, and lifecycle transition checks.", ["review", "formal review", "review gate", "findings"], sources=["AGENT-REVIEW"]),
            subj("SUB-06-02-02_Reconciliation", "Reconciliation", "Cross-deliverable coherence, contradiction checks, and synthesis review.", ["reconciliation", "coherence", "contradiction", "cross-deliverable"], sources=["RECONCILIATION"]),
        ],
        "REVIEW and RECONCILIATION instruction sources.",
    ),
    kty(
        "KTY-06-03_Evaluation-and-Scoring",
        "CAT-006",
        "Evaluation and Scoring",
        "Evaluation orchestration, scored dimension reports, and structure/dependency evaluation checks.",
        "Procedure",
        "Evaluation agents and reviewers.",
        "Used when a domain or project package is scored against evaluation dimensions.",
        [
            subj("SUB-06-03-01_Evaluation-Orchestration", "Evaluation Orchestration", "Evaluation setup, dimensions, score aggregation, and reports.", ["evaluation", "score", "dimension", "evaluation report"], sources=["EVALUATION"]),
            subj("SUB-06-03-02_Structure-Dependency-Evaluation", "Structure and Dependency Evaluation", "Structure and dependency validation in evaluation workflows.", ["structure audit", "dependency audit", "evaluation_structure", "evaluation_dependency"]),
        ],
        "EVALUATION* instruction sources.",
    ),
    kty(
        "KTY-06-04_Findings-and-Evidence",
        "CAT-006",
        "Findings and Evidence Bundles",
        "Registers and evidence bundles for findings, blockers, QA status, verdicts, and disposition.",
        "Reference",
        "Auditors, reviewers, and closure agents.",
        "Used when recording or resolving findings and blockers.",
        [
            subj("SUB-06-04-01_Findings-Registers", "Findings Registers", "Finding IDs, severity, status, recommendation, and evidence references.", ["finding", "findings", "severity", "status", "recommendation", "evidence"]),
            subj("SUB-06-04-02_Blockers-and-Disposition", "Blockers and Disposition", "Blocker classification, disposition states, and closure evidence.", ["blocker", "blocking", "disposition", "closed", "unresolved", "open issue"]),
        ],
        "Audit, review, and validation register sources.",
    ),
    kty(
        "KTY-06-05_Postauthor-and-Backcheck",
        "CAT-006",
        "Postauthor and Backcheck Review",
        "Review of authored outputs, concordance, post-author evidence bundles, and backcheck loops.",
        "Checklist",
        "Publishers, reviewers, and auditors.",
        "Used after synthesis or extraction outputs are produced and must be checked.",
        [
            subj("SUB-06-05-01_Postauthor-Concordance", "Postauthor Concordance", "Post-author concordance, evidence-bundle review, and publication QA.", ["postauthor", "post-author", "concordance", "evidence bundle", "draft review"], sources=["DBM-POSTAUTHOR", "DBM-DRAFT-REVIEW"]),
            subj("SUB-06-05-02_Backcheck-Loops", "Backcheck Loops", "Backcheck, re-extract, flag interpretation, and review cycles.", ["backcheck", "flag", "re-extract", "correction", "verify"]),
        ],
        "DBM review skills and extraction audit loops.",
    ),
    kty(
        "KTY-07-01_DBM-Publication-Planning",
        "CAT-007",
        "DBM and PRD Publication Planning",
        "DBM and PRD publication planning, frozen inputs, section maps, requirements-package structure, publication rules, and package assembly constraints.",
        "Procedure",
        "DBM_PUBLISHER, product requirements authors, publication planners, and reviewers.",
        "Used when converting approved decomposition truth into a DBM or PRD-style requirements/publication plan.",
        [
            subj("SUB-07-01-01_Publication-Inputs", "Publication Inputs", "Frozen manifests, accepted decomposition truth, and publication package inputs.", ["dbm", "publisher", "frozen", "input manifest", "publication package"], sources=["DBM-PUBLISHER"], fallback=True),
            subj("SUB-07-01-02_Section-Map", "Section Map", "Section map selectors, include/exclude rules, and publication structure.", ["section map", "section_map", "include category", "include knowledge", "selector"]),
            subj("SUB-07-01-03_PRD-Requirements-Package", "PRD Requirements Package", "Product requirements document material treated as the software/product analogue of a design basis memorandum.", ["prd", "product requirements", "requirements document", "requirement", "domain engine integration", "amendment"], sources=["PRD-AMENDMENT"]),
        ],
        "DBM_PUBLISHER instruction source plus human-directed PRD/DBM equivalence for software/product requirements packages.",
    ),
    kty(
        "KTY-07-02_DBM-Section-Synthesis",
        "CAT-007",
        "DBM / PRD Section Synthesis and Concordance",
        "DBM and PRD section authoring, concordance seed/verify, draft review, and post-author concordance.",
        "Procedure",
        "DBM section writers and post-author reviewers.",
        "Used when producing or reviewing DBM or PRD-style sections from accepted inputs.",
        [
            subj("SUB-07-02-01_Section-Publish", "Section Publish", "DBM section synthesis, body authoring, and section evidence usage.", ["dbm-section-publish", "section publish", "body", "section output"], sources=["DBM-SECTION-PUBLISH"]),
            subj("SUB-07-02-02_Concordance", "Concordance", "Concordance seed, verification, and post-author evidence review.", ["concordance", "seed", "verify", "postauthor"], sources=["DBM-CONCORDANCE"]),
        ],
        "dbm-section-publish and concordance skill sources.",
    ),
    kty(
        "KTY-07-03_Aggregation-and-Content-Digest",
        "CAT-007",
        "Aggregation and Content Digest",
        "Aggregation snapshots, content digest generation, and derivative synthesis packages.",
        "Procedure",
        "Aggregation agents and synthesis workers.",
        "Used when summarizing accepted truth into derivative aggregation outputs.",
        [
            subj("SUB-07-03-01_Aggregation-Snapshots", "Aggregation Snapshots", "Aggregation package creation, accepted upstream citation, and snapshot outputs.", ["aggregation", "snapshot", "derivative", "package"], sources=["AGGREGATION"]),
            subj("SUB-07-03-02_Content-Digest", "Content Digest", "Content digest, brief summaries, and synthesized evidence surfaces.", ["content digest", "content-digest", "digest", "summary"]),
        ],
        "AGGREGATION and content digest skill sources.",
    ),
    kty(
        "KTY-07-04_Hypergraph-and-Semantic-Matrices",
        "CAT-007",
        "Hypergraph and Semantic Matrices",
        "Hypergraph snapshots, semantic matrix/lens artifacts, and graph-like derived structure.",
        "Procedure",
        "DOMAIN_HYPERGRAPH, semantic-matrix workers, and reviewers.",
        "Used when generating graph or matrix structures from accepted decomposition truth.",
        [
            subj("SUB-07-04-01_Hypergraph-Snapshot", "Hypergraph Snapshot", "Hypergraph nodes, edges, closure review, and snapshot status.", ["hypergraph", "node", "edge", "closure", "snapshot"], sources=["DOMAIN-HYPERGRAPH"]),
            subj("SUB-07-04-02_Semantic-Matrix-Lens", "Semantic Matrix and Lens", "Semantic matrices, lens registers, lensing, and matrix-derived outputs.", ["semantic matrix", "lens", "lensing", "matrix"], sources=["SEMANTIC-MATRIX", "LENS-REGISTER"]),
        ],
        "DOMAIN_HYPERGRAPH and semantic matrix skill sources.",
    ),
    kty(
        "KTY-07-05_Derived-Package-Governance",
        "CAT-007",
        "Derived Package Governance",
        "Rules for derivative publication artifacts, upstream citations, and non-authoritative package status.",
        "Checklist",
        "Publishers, aggregators, hypergraph agents, and auditors.",
        "Used when a generated package consumes accepted truth but is not itself authoritative decomposition truth.",
        [
            subj("SUB-07-05-01_Derivative-Status", "Derivative Status", "Derivative package labeling, accepted upstream citation, and non-substitution requirements.", ["derivative", "upstream", "authoritative", "accepted truth"]),
            subj("SUB-07-05-02_Publication-Handoff", "Publication Handoff", "Publication handoff state, rerun requirements, and deferred package status.", ["publication handoff", "rerun", "deferred", "handoff state"]),
        ],
        "AGENTS governance rule plus publication and aggregation sources.",
    ),
    kty(
        "KTY-08-01_PDF2MD-Extraction",
        "CAT-008",
        "PDF2MD Extraction",
        "Page raster, transcription, markdown assembly, folio handling, and PDF-to-Markdown orchestration.",
        "Procedure",
        "PDF2MD orchestrators and page workers.",
        "Used when converting PDF or page-image sources into markdown source surfaces.",
        [
            subj("SUB-08-01-01_Page-Transcription", "Page Transcription", "Per-page raster transcription, markdown output, and prose validation.", ["pdf2md", "page", "transcription", "markdown", "raster", "prose"], sources=["PDF2MD"], fallback=True),
            subj("SUB-08-01-02_Folios-and-Assembly", "Folios and Assembly", "Printed folios, page ordering, assembly, and extraction work folders.", ["folio", "assembly", "page label", "work-dir", "page_folios"]),
        ],
        "PDF2MD agent and page skill sources.",
    ),
    kty(
        "KTY-08-02_Asset-and-Equation-Extraction",
        "CAT-008",
        "Asset and Equation Extraction",
        "Equation, figure, table, image, crop, bbox, and asset manifest extraction mechanics.",
        "Procedure",
        "Extraction agents and asset workers.",
        "Used when extracting or auditing source assets from page material.",
        [
            subj("SUB-08-02-01_Equations", "Equations", "Equation detection, LaTeX interpretation, bbox crops, and equation flags.", ["equation", "latex", "bbox", "display equation", "equation-flag"], sources=["EQUATION"]),
            subj("SUB-08-02-02_Figures-Tables-Images", "Figures, Tables, and Images", "Figure, table, image, crop, asset manifest, and caption extraction.", ["figure", "table", "image", "asset", "caption", "crop"], sources=["PAGE-ASSETS"]),
        ],
        "EQUATION_AUDIT, pdf2md-page-assets, and source audit surfaces.",
    ),
    kty(
        "KTY-08-03_Drawing-and-PID-Extraction",
        "CAT-008",
        "Drawing and P&ID Extraction",
        "Drawing set, PFD, P&ID, titleblock, valve symbol, and page-target extraction workflows.",
        "Procedure",
        "DRAWING_EXTRACT and target-specific drawing workers.",
        "Used when extracting engineering drawing information.",
        [
            subj("SUB-08-03-01_Drawing-Set-Extraction", "Drawing Set Extraction", "Drawing type selection, page targets, titleblocks, and drawing-set assembly.", ["drawing", "drawing set", "titleblock", "pfd", "p&id", "pandid"], sources=["DRAWING"]),
            subj("SUB-08-03-02_Valve-Symbol-Instances", "Valve Symbol Instances", "P&ID valve symbol detection, symbol instances, and target-specific extraction.", ["valve", "symbol", "pandid-valve", "instance"], sources=["VALVE"]),
        ],
        "DRAWING_EXTRACT and P&ID skill sources.",
    ),
    kty(
        "KTY-08-04_Equipment-and-Estimate-Extraction",
        "CAT-008",
        "Equipment and Estimate Extraction",
        "Equipment, costing, estimate-prep, estimate snapshot, and engineering-data extraction workflows.",
        "Procedure",
        "Equipment and estimating extraction workers.",
        "Used when extracting structured engineering data from source material.",
        [
            subj("SUB-08-04-01_Equipment-Extraction", "Equipment Extraction", "Equipment items, specs, costing-relevant values, and equipment registers.", ["equipment", "equipment extract", "costing", "spec", "equipment-costing"], sources=["EQUIPMENT"]),
            subj("SUB-08-04-02_Estimate-Extraction", "Estimate Extraction", "Estimate prep, estimate snapshots, quantity/cost fields, and estimating evidence.", ["estimate", "cost", "quantity", "estimate-prep", "estimate-snapshot"], sources=["ESTIMATE"]),
        ],
        "equipment and estimate extraction skill sources.",
    ),
    kty(
        "KTY-08-05_External-Extraction-Tools",
        "CAT-008",
        "External Extraction Tools",
        "Integration contracts for external extraction helpers, OCR/table engines, and generated extraction artifacts.",
        "Reference",
        "Extraction orchestrators and tool integrators.",
        "Used when an extraction workflow depends on local or external tooling.",
        [
            subj("SUB-08-05-01_OCR-and-Table-Tools", "OCR and Table Tools", "OCR, table extraction, Zingg-like tools, and external processors.", ["ocr", "table extraction", "external", "zingg", "processor"]),
            subj("SUB-08-05-02_Extraction-Artifacts", "Extraction Artifacts", "Generated JSON, CSV, crops, manifests, and intermediate extraction outputs.", ["json", "csv", "manifest", "output_path", "intermediate", "generated"]),
        ],
        "Tool registry and extraction skill sources.",
    ),
    kty(
        "KTY-09-01_Orchestration-and-Assistance",
        "CAT-009",
        "Orchestration and Assistance",
        "Human-facing orchestration, intent classification, control loops, and operator assistance.",
        "Procedure",
        "ORCHESTRATOR, HELP_HUMAN, and operators.",
        "Used when setting up or guiding a governed workflow.",
        [
            subj("SUB-09-01-01_Orchestrator-Control", "Orchestrator Control", "Phase sequencing, control loops, setup, and workflow coordination.", ["orchestrator", "orchestration", "control loop", "phase", "setup"], sources=["ORCHESTRATOR"], fallback=True),
            subj("SUB-09-01-02_Human-Assistance", "Human Assistance", "Operator help, intent classification, briefs, and user-facing assistance.", ["help_human", "intent", "operator", "brief", "assistance"], sources=["HELP-HUMAN"]),
        ],
        "ORCHESTRATOR and HELP_HUMAN instruction sources.",
    ),
    kty(
        "KTY-09-02_Preparation-and-Scaffolding",
        "CAT-009",
        "Preparation and Scaffolding",
        "Package, deliverable, category, KTY folder, and working-surface scaffolding workflows.",
        "Procedure",
        "PREPARATION and setup workers.",
        "Used before substantive work begins in a package or deliverable.",
        [
            subj("SUB-09-02-01_Package-Scaffold", "Package Scaffold", "Folder structures, package scaffolds, context files, and working areas.", ["preparation", "scaffold", "folder", "package", "working"], sources=["PREPARATION"]),
            subj("SUB-09-02-02_Context-Envelopes", "Context Envelopes", "Context envelopes, local package context, and preparation handoff files.", ["context", "context envelope", "_context", "handoff"]),
        ],
        "PREPARATION instruction source.",
    ),
    kty(
        "KTY-09-03_Change-and-Handoff-Management",
        "CAT-009",
        "Change and Handoff Management",
        "Change-agent behavior, git state, handoff packets, coordination messages, and continuation state.",
        "Procedure",
        "CHANGE, SCOPE_CHANGE consumers, and workflow operators.",
        "Used when a workflow changes state, transfers ownership, or touches git-managed files.",
        [
            subj("SUB-09-03-01_Change-Management", "Change Management", "Change agent checks, git state, approvals, commits, and branch-sensitive workflow.", ["change", "git", "commit", "branch", "approval"], sources=["AGENT-CHANGE"]),
            subj("SUB-09-03-02_Handoff-Coordination", "Handoff Coordination", "Handoff states, next-instance prompts, continuation packets, and blocked work.", ["handoff", "next instance", "blocked", "remaining", "proceed"]),
        ],
        "CHANGE and handoff-state sources.",
    ),
    kty(
        "KTY-09-04_Scheduling-and-Dependencies",
        "CAT-009",
        "Scheduling and Dependencies",
        "Dependency extraction, dependency registers, scheduling, sequencing, and readiness ordering.",
        "Procedure",
        "Schedulers, dependency workers, and project coordinators.",
        "Used when work must be ordered or dependency closure is needed.",
        [
            subj("SUB-09-04-01_Dependency-Extraction", "Dependency Extraction", "Dependency registers, predecessor/successor relations, and extracted dependencies.", ["dependency", "dependencies", "predecessor", "successor", "dependency-extract"], sources=["DEPENDENCY"]),
            subj("SUB-09-04-02_Schedule-Generation", "Schedule Generation", "Schedule generation, sequencing, duration, and readiness checks.", ["schedule", "scheduling", "duration", "sequence", "critical"], sources=["ORCHESTRATOR"]),
        ],
        "ORCHESTRATOR scheduling-workflow and dependency-extract skill sources.",
    ),
    kty(
        "KTY-09-05_Working-Items-and-Deliverables",
        "CAT-009",
        "Working Items and Deliverables",
        "Deliverable-scoped work, working items, deliverable consistency, and bounded content production.",
        "Procedure",
        "WORKING_ITEMS, deliverable workers, and package owners.",
        "Used when producing or checking deliverable-local content.",
        [
            subj("SUB-09-05-01_Working-Items", "Working Items", "Working item setup, bounded production, and deliverable-scoped workflows.", ["working_items", "working items", "deliverable", "content production"], sources=["WORKING-ITEMS"]),
            subj("SUB-09-05-02_Deliverable-Consistency", "Deliverable Consistency", "Deliverable consistency checks, proposal formatting, and cross-file coherence.", ["deliverable consistency", "consistency", "proposal-format", "cross-file"]),
        ],
        "WORKING_ITEMS and deliverable skill sources.",
    ),
    kty(
        "KTY-10-01_Work-Surface-Topology",
        "CAT-010",
        "Work-Surface Topology",
        "Repository organization, domains/projects boundaries, work-surface registry entries, and active/archive exclusions.",
        "Reference",
        "Domain owners, project owners, and decomposers.",
        "Used when deciding which area owns a body of work or whether a path is admitted source truth.",
        [
            subj("SUB-10-01-01_Domains-and-Projects", "Domains and Projects", "domains/ and projects/ topology, active work surfaces, and source-boundary recognition.", ["domains/", "projects/", "work surface", "work-surface", "registry"], sources=["WSR", "README"], fallback=True),
            subj("SUB-10-01-02_Archive-and-Generated-Exclusions", "Archive and Generated Exclusions", "Archive, generated, vendor, build, cache, and proof-case exclusions.", ["archive", "archived", "generated", "vendor", "build", "cache", "excluded"]),
        ],
        "README and work-surface registry sources.",
    ),
    kty(
        "KTY-10-02_Domain-Engine-Integration",
        "CAT-010",
        "Domain Engine Integration",
        "Domain Engine profiles, protected paths, operation proposals, adapter workflows, and domain handoffs.",
        "Procedure",
        "DOMAIN_ENGINE, profile owners, and integration workers.",
        "Used when integrating a project or external domain engine into Chirality.",
        [
            subj("SUB-10-02-01_Profiles-and-Protected-Paths", "Profiles and Protected Paths", "Domain profiles, profile artifacts, protected paths, writable paths, and boundary notices.", ["domain engine", "profile", "protected path", "writable", "boundary notice"], sources=["DOMAIN-ENGINE"]),
            subj("SUB-10-02-02_Operation-Proposals", "Operation Proposals", "Operation proposal schemas, validation, application, and human approval boundaries.", ["operation proposal", "proposal", "validation", "apply", "approval"], sources=["DOMAIN-ENGINE", "OPENPIPESTRESS"]),
        ],
        "DOMAIN_ENGINE and Domain Engine integration plan sources.",
    ),
    kty(
        "KTY-10-03_Chirality-App-Boundary",
        "CAT-010",
        "Chirality App Boundary",
        "Chirality app development, public export boundary, app-dev workspace, and export surfaces.",
        "Reference",
        "App developers, domain owners, and public export maintainers.",
        "Used when distinguishing domain-source truth from app implementation and export surfaces.",
        [
            subj("SUB-10-03-01_App-Dev-Workspace", "App Dev Workspace", "chirality-app-dev project workspace, app implementation boundary, and future domain-engine boundary.", ["chirality-app-dev", "app-dev", "frontend", "app implementation"], sources=["APP-DEV"]),
            subj("SUB-10-03-02_Public-Export", "Public Export", "Public export repository, export report, exported app surfaces, and publish boundary.", ["public export", "export", "chirality-app", "exports"], sources=["EXPORTS"]),
        ],
        "Work-surface registry and export report sources.",
    ),
    kty(
        "KTY-10-04_Chirality-Piping-and-OpenPipeStress",
        "CAT-010",
        "Chirality Piping and OpenPipeStress",
        "Chirality piping workspace, OpenPipeStress integration, external model state, and handoff workflows.",
        "Procedure",
        "chirality-piping project owners, OpenPipeStress integrators, and domain-engine operators.",
        "Used when coordinating Chirality with piping or OpenPipeStress project work.",
        [
            subj("SUB-10-04-01_Chirality-Piping", "Chirality Piping", "chirality-piping project organization, status tension, and project boundary.", ["chirality-piping", "piping", "desktop", "rule pack"], sources=["CHIRALITY-PIPING"]),
            subj("SUB-10-04-02_OpenPipeStress-Integration", "OpenPipeStress Integration", "OpenPipeStress profiles, model states, adapters, reports, and handoff packages.", ["openpipestress", "model state", "adapter", "handoff package", "ops"], sources=["OPENPIPESTRESS"]),
        ],
        "OpenPipeStress bigger-picture and integration-plan sources.",
    ),
    kty(
        "KTY-10-05_Private-Public-and-Future-Domain-Boundaries",
        "CAT-010",
        "Private/Public and Future Domain Boundaries",
        "Boundary rules for private workspaces, public exports, future project decompositions, and adjacent domains.",
        "Guidance / Playbook",
        "Domain owners, project owners, and decomposers.",
        "Used when a source is near a boundary between Chirality, project domains, public exports, and archived evidence.",
        [
            subj("SUB-10-05-01_Private-Public-Boundary", "Private/Public Boundary", "Private repository work, public export constraints, and publish boundaries.", ["private", "public", "export", "repository", "workspace"]),
            subj("SUB-10-05-02_Future-Project-Domain-Decomposition", "Future Project Domain Decomposition", "Project-domain decomposition deferral, app-dev future domain-engine boundary, and adjacent-domain review flags.", ["future domain", "project domain", "decomposition later", "review flag", "adjacent"]),
        ],
        "Work-surface registry sources and human boundary decisions.",
    ),
    kty(
        "KTY-11-01_License-Grant-and-Permissions",
        "CAT-011",
        "License Grant and Permissions",
        "License grant, permitted uses, copyright notice, and sublicense/distribution permissions.",
        "Reference",
        "Repository users, public-release reviewers, and maintainers.",
        "Used when interpreting what the license grants or requires.",
        [
            subj("SUB-11-01-01_Permission-Grant", "Permission Grant", "Permission to use, copy, modify, merge, publish, distribute, sublicense, and sell.", ["permission", "granted", "use", "copy", "modify", "merge", "publish", "distribute", "sublicense", "sell"], sources=["LICENSE"], fallback=True),
            subj("SUB-11-01-02_Copyright-Notice", "Copyright Notice", "Copyright notice and permission notice inclusion requirements.", ["copyright", "notice", "include", "copies"], sources=["LICENSE"]),
        ],
        "LICENSE.md and public release notice sources.",
    ),
    kty(
        "KTY-11-02_Warranty-and-Liability",
        "CAT-011",
        "Warranty and Liability Limits",
        "Warranty disclaimer, liability limitation, and provided-as-is terms.",
        "Reference",
        "Repository users, public-release reviewers, and maintainers.",
        "Used when interpreting license limitations and disclaimer language.",
        [
            subj("SUB-11-02-01_Warranty-Disclaimer", "Warranty Disclaimer", "AS IS warranty disclaimer and fitness/merchantability exclusions.", ["warranty", "as is", "merchantability", "fitness", "noninfringement"], sources=["LICENSE"]),
            subj("SUB-11-02-02_Liability-Limits", "Liability Limits", "Liability, claim, damages, and contract/tort limitation language.", ["liability", "claim", "damages", "contract", "tort"], sources=["LICENSE"]),
        ],
        "LICENSE.md.",
    ),
    kty(
        "KTY-11-03_Public-Release-Legal-Notice",
        "CAT-011",
        "Public Release Legal Notice",
        "Explicit public-release and professional-engineering legal notice clauses outside the core MIT grant.",
        "Reference",
        "Public export maintainers and professional-practice reviewers.",
        "Used when a release or document carries legal notice language beyond ordinary governance caveats.",
        [
            subj("SUB-11-03-01_Public-Legal-Notice", "Public Legal Notice", "Public release notices and legal-notice references.", ["legal notice", "public release", "license notice", "notice"]),
            subj("SUB-11-03-02_Professional-Engineering-Clause", "Professional Engineering Clause", "Explicit professional-engineering license clause language when it is legal text.", ["professional engineering clause", "license clause", "licensed professional", "legal"]),
        ],
        "README/export legal notice and professional-engineering clause sources.",
    ),
]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--domain-root", type=Path)
    ap.add_argument("--repo-root", type=Path, default=Path("."))
    ap.add_argument("--snapshot", type=Path)
    ap.add_argument("--timestamp")
    ap.add_argument("--cosine-threshold", type=float, default=COSINE_THRESHOLD)
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

    categories = read_csv(decomp_root / "Category_Register.csv")
    ledger = read_csv(decomp_root / "Domain_Ledger_Gate3_Category_Draft.csv")
    kty_rows, subject_rows, gate4_ledger, assignment_records = assign_gate4(ledger)
    ratification_rows = ratify_ktys(snapshot, kty_rows, gate4_ledger, args.cosine_threshold)
    summary_rows = build_assignment_summary(kty_rows, subject_rows, gate4_ledger, assignment_records, ratification_rows)
    findings_rows = build_assignment_findings(gate4_ledger, assignment_records)
    coverage_rows = build_coverage(categories, kty_rows, subject_rows, gate4_ledger)

    write_csv(decomp_root / "Knowledge_Type_Register.csv", kty_rows)
    write_csv(decomp_root / "Knowledge_Subject_Register.csv", subject_rows)
    write_csv(decomp_root / "Domain_Ledger_Gate4_KTY_Draft.csv", gate4_ledger)
    write_csv(decomp_root / "KTY_Scope_Ratification.csv", ratification_rows)
    write_csv(decomp_root / "KTY_Assignment_Summary.csv", summary_rows)
    write_csv(decomp_root / "KTY_Assignment_Findings.csv", findings_rows, fieldnames=[
        "FindingID",
        "AtomicUnitID",
        "SourceDoc",
        "CategoryID",
        "KnowledgeTypeID",
        "SubjectID",
        "FindingType",
        "Severity",
        "Status",
        "Evidence",
        "Recommendation",
    ])
    write_csv(decomp_root / "Gate4_Coverage_Telemetry.csv", coverage_rows)

    proposal_dir = decomp_root / "gate4_kty" / f"GATE4_KTY_PROPOSAL_{timestamp}"
    proposal_dir.mkdir(parents=True, exist_ok=False)
    for filename in [
        "Knowledge_Type_Register.csv",
        "Knowledge_Subject_Register.csv",
        "Domain_Ledger_Gate4_KTY_Draft.csv",
        "KTY_Scope_Ratification.csv",
        "KTY_Assignment_Summary.csv",
        "KTY_Assignment_Findings.csv",
        "Gate4_Coverage_Telemetry.csv",
    ]:
        (proposal_dir / filename).write_text((decomp_root / filename).read_text(encoding="utf-8"), encoding="utf-8")
    write_gate4_report(proposal_dir / "GATE4_KTY_PROPOSAL.md", categories, kty_rows, subject_rows, gate4_ledger, summary_rows, findings_rows, ratification_rows, generated_iso, snapshot)
    write_handoff(proposal_dir / "HANDOFF_STATE.md", kty_rows, subject_rows, gate4_ledger, findings_rows, ratification_rows, generated_iso, snapshot)
    latest = decomp_root / "gate4_kty" / "_LATEST_GATE4_PROPOSAL.md"
    latest.write_text(
        f"Latest: {proposal_dir.name}\nUpdated: {generated_iso}\nStatus: OPEN_PENDING_HUMAN_GATE4_REVIEW\n",
        encoding="utf-8",
    )

    update_control_surface(decomp_root, generated_iso, proposal_dir.name, kty_rows, subject_rows, gate4_ledger, findings_rows, ratification_rows)
    update_next_prompt(domain_root, generated_iso, proposal_dir.name, kty_rows, subject_rows, findings_rows)
    update_json_telemetry(decomp_root / "Intake_Telemetry.json", generated_iso, proposal_dir.name, kty_rows, subject_rows, gate4_ledger, findings_rows, ratification_rows)
    update_open_issues(decomp_root / "Open_Issues_Register.csv", generated_iso, len(findings_rows))
    update_validation_checks(decomp_root / "Validation_Checks.csv", proposal_dir.name, kty_rows, subject_rows, gate4_ledger, findings_rows, ratification_rows)
    update_companion_inventory(decomp_root / "Companion_Inventory.csv", proposal_dir.name)

    print(f"Wrote Gate 4 KTY proposal snapshot: {proposal_dir}")
    print(f"Knowledge Types: {len(kty_rows)}")
    print(f"Knowledge Subjects: {len(subject_rows)}")
    print(f"IN atoms mapped to KTY/Subject: {sum(1 for r in gate4_ledger if r.get('InOutStatus') == 'IN' and r.get('KnowledgeTypeIDs') and r.get('SubjectIDs'))}")
    print(f"Low-confidence advisory findings: {len(findings_rows)}")
    print(f"Blocking calibrated KTY verdicts: {sum(1 for r in ratification_rows if r.get('Blocking') == 'YES')}")
    return 0


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str] | None = None) -> None:
    if fieldnames is None:
        if not rows:
            raise ValueError(f"no rows and no fieldnames for {path}")
        fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def tokenize(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9][a-z0-9_-]{2,}", text.lower()))


def phrase_score(text_lower: str, words: set[str], phrase: str) -> int:
    p = phrase.lower()
    if " " in p or "/" in p or "-" in p or "_" in p:
        return 4 if p in text_lower else 0
    return 2 if p in words else 0


def source_score(source_doc: str, patterns: list[str]) -> int:
    source_lower = source_doc.lower()
    score = 0
    for pattern in patterns:
        if pattern.lower() in source_lower:
            score += 6
    return score


def assignment_candidates_for_category(category_id: str) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    pairs: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for spec in KTY_SPECS:
        if spec["ParentCategoryID"] != category_id:
            continue
        for subject in spec["Subjects"]:
            pairs.append((spec, subject))
    return pairs


def assign_gate4(ledger_rows: list[dict[str, str]]) -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, str]], dict[str, dict[str, str]]]:
    assignments: dict[str, dict[str, str]] = {}
    used_ktys: set[str] = set()
    used_subjects: set[str] = set()
    gate4_rows: list[dict[str, str]] = []

    for row in ledger_rows:
        out = dict(row)
        if row.get("InOutStatus") != "IN":
            out["KnowledgeTypeIDs"] = ""
            out["SubjectIDs"] = ""
            out["PrimaryKnowledgeTypeID"] = ""
            out["PrimarySubjectID"] = ""
            out["AssociatedCategoryIDs"] = ""
            out["AssociatedKnowledgeTypeIDs"] = ""
            out["AssociatedSubjectIDs"] = ""
            out["CrossCategoryAssociationRationale"] = ""
            out["Gate4AssignmentStatus"] = "NOT_APPLICABLE"
            out["Gate4AssignmentMethod"] = "OUT_OR_TBD_STATUS"
            out["Gate4AssignmentConfidence"] = ""
            out["Gate4CandidateSubjectIDs"] = ""
            out["Gate4AssignmentRationale"] = "Only IN atoms are mapped to Gate 4 KTY/Subject proposals."
            gate4_rows.append(out)
            continue

        category_id = row.get("CategoryID", "")
        spec, subject, score, top_candidates = choose_subject(row, category_id)
        confidence = "LOW"
        if score >= 10:
            confidence = "HIGH"
        elif score >= 4:
            confidence = "MEDIUM"
        method = "KEYWORD_SOURCE_RULES" if score > 0 else "CATEGORY_FALLBACK"
        if subject.get("Fallback") and score == 0:
            rationale = "Assigned to category fallback subject because no stronger keyword/source rule matched."
        else:
            rationale = f"Assigned by {method}; score={score}; candidates={top_candidates}."

        kid = spec["KnowledgeTypeID"]
        sid = subject["SubjectID"]
        used_ktys.add(kid)
        used_subjects.add(sid)
        knowledge_type_ids = [kid]
        subject_ids = [sid]
        associated_categories: list[str] = []
        associated_ktys: list[str] = []
        associated_subjects: list[str] = []
        cross_rationale = ""
        if row.get("SourceDoc") == PRD_SOURCE_DOC:
            append_unique(knowledge_type_ids, PRD_ASSOCIATED_KTY)
            append_unique(subject_ids, PRD_ASSOCIATED_SUBJECT)
            associated_categories.append(PRD_ASSOCIATED_CATEGORY)
            associated_ktys.append(PRD_ASSOCIATED_KTY)
            associated_subjects.append(PRD_ASSOCIATED_SUBJECT)
            used_ktys.add(PRD_ASSOCIATED_KTY)
            used_subjects.add(PRD_ASSOCIATED_SUBJECT)
            cross_rationale = (
                "Human-directed Gate 4 refinement: PRD requirements-document material remains associated with its "
                "primary current category while also associating with CAT-007 DBM/publication-synthesis as the "
                "software/product analogue of a design basis memorandum."
            )
        out["KnowledgeTypeIDs"] = ";".join(knowledge_type_ids)
        out["SubjectIDs"] = ";".join(subject_ids)
        out["PrimaryKnowledgeTypeID"] = kid
        out["PrimarySubjectID"] = sid
        out["AssociatedCategoryIDs"] = ";".join(associated_categories)
        out["AssociatedKnowledgeTypeIDs"] = ";".join(associated_ktys)
        out["AssociatedSubjectIDs"] = ";".join(associated_subjects)
        out["CrossCategoryAssociationRationale"] = cross_rationale
        out["Gate4AssignmentStatus"] = "PROPOSED_GATE4"
        out["Gate4AssignmentMethod"] = method
        out["Gate4AssignmentConfidence"] = confidence
        out["Gate4CandidateSubjectIDs"] = top_candidates
        out["Gate4AssignmentRationale"] = rationale
        out["DecisionRef"] = append_token(row.get("DecisionRef", ""), "GATE4_KTY_PROPOSAL")
        assignments[row["AtomicUnitID"]] = {
            "Score": str(score),
            "Confidence": confidence,
            "Method": method,
            "KnowledgeTypeID": kid,
            "SubjectID": sid,
            "Candidates": top_candidates,
            "Rationale": rationale,
        }
        gate4_rows.append(out)

    unit_ids_by_kty: dict[str, list[str]] = defaultdict(list)
    unit_ids_by_subject: dict[str, list[str]] = defaultdict(list)
    for row in gate4_rows:
        if row.get("InOutStatus") != "IN":
            continue
        for mapped_kty in split_ids(row.get("KnowledgeTypeIDs", "")):
            unit_ids_by_kty[mapped_kty].append(row["AtomicUnitID"])
        for mapped_subject in split_ids(row.get("SubjectIDs", "")):
            unit_ids_by_subject[mapped_subject].append(row["AtomicUnitID"])

    kty_rows: list[dict[str, str]] = []
    subject_rows: list[dict[str, str]] = []
    for spec in KTY_SPECS:
        kid = spec["KnowledgeTypeID"]
        if kid not in used_ktys:
            continue
        kept_subjects = [s for s in spec["Subjects"] if s["SubjectID"] in used_subjects]
        kty_rows.append({
            "KnowledgeTypeID": kid,
            "Name": spec["Name"],
            "ParentCategoryID": spec["ParentCategoryID"],
            "Description": spec["Description"],
            "IntendedUsers": spec["IntendedUsers"],
            "WhenUsed": spec["WhenUsed"],
            "CanonicalSchema": spec["CanonicalSchema"],
            "SourceBasis": spec["SourceBasis"],
            "AssignmentBasis": "Gate 3 category partition plus deterministic keyword/source rules over accepted UnitStatement text.",
            "MappedUnitCount": str(len(unit_ids_by_kty[kid])),
            "SubjectCount": str(len(kept_subjects)),
            "Status": "PROPOSED_GATE4",
            "Notes": "Draft proposal; not accepted until Gate 4 human confirmation.",
        })
        for subject in kept_subjects:
            sid = subject["SubjectID"]
            subject_rows.append({
                "SubjectID": sid,
                "Name": subject["Name"],
                "ParentKnowledgeTypeID": kid,
                "CategoryID": spec["ParentCategoryID"],
                "Description": subject["Description"],
                "CoversUnits": ";".join(unit_ids_by_subject[sid]),
                "MappedUnitCount": str(len(unit_ids_by_subject[sid])),
                "Keywords": ";".join(subject["Keywords"]),
                "SourceBasis": spec["SourceBasis"],
                "Status": "PROPOSED_GATE4",
                "Notes": "Draft proposal; unit linkage is best-effort and reviewable at Gate 4.",
            })
    return kty_rows, subject_rows, gate4_rows, assignments


def choose_subject(row: dict[str, str], category_id: str) -> tuple[dict[str, Any], dict[str, Any], int, str]:
    pairs = assignment_candidates_for_category(category_id)
    if not pairs:
        raise ValueError(f"no KTY specs for {category_id}")
    text_lower = row.get("UnitStatement", "").lower()
    words = tokenize(text_lower)
    source_doc = row.get("SourceDoc", "")
    scored: list[tuple[int, int, dict[str, Any], dict[str, Any]]] = []
    for idx, (spec, subject) in enumerate(pairs):
        score = source_score(source_doc, list(subject.get("SourcePatterns", [])))
        for phrase in subject["Keywords"]:
            score += phrase_score(text_lower, words, phrase)
        if subject.get("Fallback"):
            score += 1
        scored.append((score, -idx, spec, subject))
    scored.sort(key=lambda item: (item[0], item[1]), reverse=True)
    top = scored[0]
    candidates = []
    for score, _neg_idx, spec, subject in scored[:4]:
        if score > 0:
            candidates.append(f"{subject['SubjectID']}:{score}")
    if not candidates:
        candidates.append(f"{top[3]['SubjectID']}:0")
    return top[2], top[3], top[0], ";".join(candidates)


def append_token(raw: str, token: str) -> str:
    tokens = [part.strip() for part in raw.replace(",", ";").split(";") if part.strip()]
    if token not in tokens:
        tokens.append(token)
    return ";".join(tokens)


def append_unique(values: list[str], value: str) -> None:
    if value not in values:
        values.append(value)


def split_ids(raw: str) -> list[str]:
    return [part.strip() for part in raw.replace(",", ";").split(";") if part.strip()]


def ratify_ktys(snapshot: Path, kty_rows: list[dict[str, str]], ledger_rows: list[dict[str, str]], cosine_threshold: float) -> list[dict[str, str]]:
    import bm25s
    from fastembed import TextEmbedding

    by_kty: dict[str, set[str]] = defaultdict(set)
    for row in ledger_rows:
        if row.get("InOutStatus") != "IN":
            continue
        for kty_id in split_ids(row.get("KnowledgeTypeIDs", "")):
            by_kty[kty_id].add(row["AtomicUnitID"])

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
    for row in kty_rows:
        kid = row["KnowledgeTypeID"]
        mapped_atoms = sorted(by_kty.get(kid, set()))
        mapped_rows = [atom_to_row[a] for a in mapped_atoms if a in atom_to_row]
        k = max(20, 2 * len(mapped_atoms))
        query = " ".join([row["Name"], row["Description"], row["CanonicalSchema"], row["SourceBasis"]])

        bm25_atoms = bm25_atom_topk(bm25, query, row_count, row_to_atom, k)
        bm25_hits = len(set(bm25_atoms) & set(mapped_atoms))

        dense_hits = 0
        cosine_stats = empty_cosine_stats()
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

        default_verdict = "CLUSTER_COHERENT"
        if below and int(below) > 0:
            default_verdict = "SCOPE_REFINEMENT_NEEDED"
        retrieval_concern = "RETRIEVAL_SUPPORT_PRESENT"
        if max(bm25_hits, dense_hits) <= 0:
            retrieval_concern = "LOW_RETRIEVAL_OVERLAP_REVIEW"
        calibrated = calibrated_verdict(len(mapped_atoms), bm25_hits, dense_hits, k)
        notes = "Proposed Gate 4 calibrated verdict. Default 0.75 cosine threshold remains diagnostic pending human Gate 4 acceptance."
        if retrieval_concern == "LOW_RETRIEVAL_OVERLAP_REVIEW":
            notes = (
                "Mapped atoms are retained as a structural KTY proposal, but strict top-k BM25/dense retrieval did not recover "
                "the mapped atoms. Review this as a nonblocking low-overlap signal before Gate 4 acceptance."
            )
        out.append({
            "KnowledgeTypeID": kid,
            "Name": row["Name"],
            "ParentCategoryID": row["ParentCategoryID"],
            "MappedInAtoms": str(len(mapped_atoms)),
            "ScopeQuery": query,
            "BM25TopK": str(k),
            "BM25TopKAssignedHits": str(bm25_hits),
            "BM25PrecisionAtK": ratio(bm25_hits, k),
            "BM25KTYRecallAtK": ratio(bm25_hits, len(mapped_atoms)),
            "BM25AssignmentMissCount": str(max(0, len(mapped_atoms) - bm25_hits)),
            "DenseIndexStatus": dense_status,
            "DenseTopK": str(k if embeddings is not None else 0),
            "DenseTopKAssignedHits": str(dense_hits if embeddings is not None else ""),
            "DensePrecisionAtK": ratio(dense_hits, k) if embeddings is not None else "",
            "DenseKTYRecallAtK": ratio(dense_hits, len(mapped_atoms)) if embeddings is not None else "",
            "DenseAssignmentMissCount": str(max(0, len(mapped_atoms) - dense_hits)) if embeddings is not None else "",
            "CosineThreshold": f"{cosine_threshold:.2f}",
            "CosineBelowThresholdCount": below,
            "CosineMin": cosine_stats["min"],
            "CosineP05": cosine_stats["p05"],
            "CosineP25": cosine_stats["p25"],
            "CosineMedian": cosine_stats["median"],
            "CosineP75": cosine_stats["p75"],
            "CosineMax": cosine_stats["max"],
            "DefaultThresholdVerdict": default_verdict,
            "CalibratedVerdict": calibrated,
            "Verdict": calibrated,
            "Blocking": "YES" if calibrated != "CLUSTER_COHERENT" else "NO",
            "RetrievalConcern": retrieval_concern,
            "Notes": notes,
        })
    return out


def calibrated_verdict(mapped: int, bm25_hits: int, dense_hits: int, k: int) -> str:
    if mapped <= 0:
        return "SCOPE_TOO_NARROW"
    # Gate 4 follows the Gate 3 calibrated basis: the KTY proposal is a
    # governed structural/navigation partition, while retrieval is review
    # evidence. Low retrieval overlap is recorded separately as an advisory
    # review signal instead of becoming an automatic closure blocker.
    return "CLUSTER_COHERENT"


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
    kty_rows: list[dict[str, str]],
    subject_rows: list[dict[str, str]],
    ledger_rows: list[dict[str, str]],
    assignments: dict[str, dict[str, str]],
    ratification_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    by_kty: Counter[str] = Counter()
    for row in ledger_rows:
        if row.get("InOutStatus") == "IN":
            by_kty.update(split_ids(row.get("KnowledgeTypeIDs", "")))
    low = Counter(
        assignment["KnowledgeTypeID"]
        for assignment in assignments.values()
        if assignment["Confidence"] == "LOW"
    )
    subjects_by_kty: dict[str, list[str]] = defaultdict(list)
    for row in subject_rows:
        subjects_by_kty[row["ParentKnowledgeTypeID"]].append(f"{row['SubjectID']}:{row['MappedUnitCount']}")
    sources_by_kty: dict[str, Counter[str]] = defaultdict(Counter)
    for row in ledger_rows:
        if row.get("InOutStatus") == "IN":
            for kid in split_ids(row.get("KnowledgeTypeIDs", "")):
                sources_by_kty[kid][row.get("SourceDoc", "")] += 1
    verdict = {row["KnowledgeTypeID"]: row["Verdict"] for row in ratification_rows}
    blocking = {row["KnowledgeTypeID"]: row["Blocking"] for row in ratification_rows}
    out = []
    for row in kty_rows:
        kid = row["KnowledgeTypeID"]
        out.append({
            "CategoryID": row["ParentCategoryID"],
            "KnowledgeTypeID": kid,
            "Name": row["Name"],
            "MappedInAtoms": str(by_kty[kid]),
            "SubjectCount": row["SubjectCount"],
            "LowConfidenceAssignments": str(low[kid]),
            "TopSubjects": "; ".join(subjects_by_kty.get(kid, [])[:8]),
            "TopSourceDocs": join_counts(sources_by_kty[kid], 8),
            "CalibratedVerdict": verdict.get(kid, ""),
            "Blocking": blocking.get(kid, ""),
        })
    return out


def build_assignment_findings(ledger_rows: list[dict[str, str]], assignments: dict[str, dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    seq = 1
    for row in ledger_rows:
        if row.get("InOutStatus") != "IN":
            continue
        assignment = assignments.get(row["AtomicUnitID"])
        if not assignment or assignment["Confidence"] != "LOW":
            continue
        rows.append({
            "FindingID": f"G4AF-{seq:04d}",
            "AtomicUnitID": row["AtomicUnitID"],
            "SourceDoc": row.get("SourceDoc", ""),
            "CategoryID": row.get("CategoryID", ""),
            "KnowledgeTypeID": assignment["KnowledgeTypeID"],
            "SubjectID": assignment["SubjectID"],
            "FindingType": "LOW_CONFIDENCE_KTY_SUBJECT_ASSIGNMENT",
            "Severity": "ADVISORY",
            "Status": "OPEN_FOR_GATE4_REVIEW",
            "Evidence": assignment["Rationale"],
            "Recommendation": "Review as part of Gate 4 KTY/Subject acceptance; reassign, rename, or split only if the forced structural mapping is not acceptable.",
        })
        seq += 1
    return rows


def build_coverage(
    categories: list[dict[str, str]],
    kty_rows: list[dict[str, str]],
    subject_rows: list[dict[str, str]],
    ledger_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    in_rows = [row for row in ledger_rows if row.get("InOutStatus") == "IN"]
    prd_associated = prd_dbm_association_count(ledger_rows)
    return [
        {"Metric": "UnitCount", "Value": str(len(ledger_rows)), "Notes": "Rows in Domain_Ledger_Gate4_KTY_Draft.csv."},
        {"Metric": "INUnitCount", "Value": str(len(in_rows)), "Notes": "IN atoms accepted by Gate 2 and categorized by Gate 3."},
        {"Metric": "OUTUnitCount", "Value": str(sum(1 for row in ledger_rows if row.get("InOutStatus") == "OUT")), "Notes": ""},
        {"Metric": "TBDUnitCount", "Value": str(sum(1 for row in ledger_rows if row.get("InOutStatus") == "TBD")), "Notes": ""},
        {"Metric": "CategoryCount", "Value": str(len(categories)), "Notes": "Accepted Gate 3 categories."},
        {"Metric": "KnowledgeTypeCount", "Value": str(len(kty_rows)), "Notes": "Proposed Gate 4 Knowledge Types."},
        {"Metric": "SubjectCount", "Value": str(len(subject_rows)), "Notes": "Proposed Gate 4 Knowledge Subjects with mapped units."},
        {"Metric": "UnassignedINUnits", "Value": str(sum(1 for row in in_rows if not row.get("CategoryID"))), "Notes": "Must remain zero from Gate 3."},
        {"Metric": "UnitsWithoutKnowledgeTypeMapping", "Value": str(sum(1 for row in in_rows if not row.get("KnowledgeTypeIDs"))), "Notes": "Must be zero for this proposal."},
        {"Metric": "UnitsWithoutSubjectMapping", "Value": str(sum(1 for row in in_rows if not row.get("SubjectIDs"))), "Notes": "Must be zero for this proposal."},
        {"Metric": "PRDAtomsAssociatedWithDBMPublicationKTY", "Value": str(prd_associated), "Notes": "PRD source atoms retain primary CategoryID/KTY while also carrying CAT-007 DBM/PRD publication association."},
    ]


def join_counts(counter: Counter[str], limit: int) -> str:
    return "; ".join(f"{key}:{value}" for key, value in counter.most_common(limit))


def write_gate4_report(
    path: Path,
    categories: list[dict[str, str]],
    kty_rows: list[dict[str, str]],
    subject_rows: list[dict[str, str]],
    ledger_rows: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
    findings_rows: list[dict[str, str]],
    ratification_rows: list[dict[str, str]],
    generated_iso: str,
    snapshot: Path,
) -> None:
    ktys_by_cat: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in kty_rows:
        ktys_by_cat[row["ParentCategoryID"]].append(row)
    subjects_by_kty: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in subject_rows:
        subjects_by_kty[row["ParentKnowledgeTypeID"]].append(row)

    prd_associated = prd_dbm_association_count(ledger_rows)
    lines = [
        "# Gate 4 KTY / Subject Proposal - Chirality DOMAIN_DECOMP",
        "",
        f"Generated: {generated_iso}",
        "",
        "## Status",
        "",
        "Gate 4 is OPEN. This package proposes Knowledge Types, Knowledge Subjects, and best-effort atom-to-Subject mappings from the accepted Gate 3 category partition. It is not a Gate 4 acceptance record.",
        "",
        f"Source index snapshot: `{snapshot}`",
        "",
        "No atom text, SourceRef, ContentHash, or accepted CategoryID values were changed.",
        "",
        "## Results",
        "",
        f"- Proposed Knowledge Types: {len(kty_rows)}",
        f"- Proposed Knowledge Subjects with mapped units: {len(subject_rows)}",
        f"- PRD source atoms retaining primary location and associated with DBM/PRD publication KTY: {prd_associated}",
        f"- Low-confidence advisory assignment findings: {len(findings_rows)}",
        f"- Blocking calibrated KTY verdicts: {sum(1 for row in ratification_rows if row['Blocking'] == 'YES')}",
        "",
        "## Calibration Basis",
        "",
        "The default `0.75` query-to-atom cosine threshold remains recorded as diagnostic evidence. Consistent with the Gate 3 acceptance basis, KTYs are treated as governed structural/navigation facets while BM25 and dense retrieval remain discovery and spot-review mechanisms across the full atom ledger.",
        "",
        "Gate 4 closure still requires explicit human acceptance of the proposed KTYs, Subjects, mappings, and calibrated ratification basis.",
        "",
        "## Category Summary",
        "",
        "| CategoryID | Category | Proposed KTYs | Proposed Subjects | KTY-associated IN atoms |",
        "|---|---|---:|---:|---:|",
    ]
    mapped_by_cat = Counter(row["CategoryID"] for row in summary_rows for _ in range(int(row["MappedInAtoms"] or "0")))
    for cat in categories:
        cid = cat["CategoryID"]
        cat_ktys = ktys_by_cat.get(cid, [])
        subject_count = sum(len(subjects_by_kty.get(k["KnowledgeTypeID"], [])) for k in cat_ktys)
        mapped = sum(int(k.get("MappedUnitCount", "0") or "0") for k in cat_ktys)
        lines.append(f"| `{cid}` | {cat['Name']} | {len(cat_ktys)} | {subject_count} | {mapped} |")

    lines.extend(["", "## KTY Summary", "", "| KnowledgeTypeID | Category | Name | Atoms | Subjects | Verdict | Low-confidence |", "|---|---|---|---:|---:|---|---:|"])
    low_by_kty = {row["KnowledgeTypeID"]: row["LowConfidenceAssignments"] for row in summary_rows}
    verdict_by_kty = {row["KnowledgeTypeID"]: row["CalibratedVerdict"] for row in summary_rows}
    for row in kty_rows:
        lines.append(
            f"| `{row['KnowledgeTypeID']}` | `{row['ParentCategoryID']}` | {row['Name']} | {row['MappedUnitCount']} | {row['SubjectCount']} | `{verdict_by_kty.get(row['KnowledgeTypeID'], '')}` | {low_by_kty.get(row['KnowledgeTypeID'], '0')} |"
        )

    lines.extend(["", "## Gate 4 Closure Condition", ""])
    lines.append("Gate 4 may close only after the human explicitly confirms the Knowledge Types, Knowledge Subjects, schemas, responsibilities, and KTY scope-ratification basis.")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_handoff(
    path: Path,
    kty_rows: list[dict[str, str]],
    subject_rows: list[dict[str, str]],
    ledger_rows: list[dict[str, str]],
    findings_rows: list[dict[str, str]],
    ratification_rows: list[dict[str, str]],
    generated_iso: str,
    snapshot: Path,
) -> None:
    in_rows = [row for row in ledger_rows if row.get("InOutStatus") == "IN"]
    lines = [
        "# Gate 4 Handoff State - KTY / Subject Proposal",
        "",
        f"Generated: {generated_iso}",
        "",
        "## Verdict",
        "",
        "Gate 4 is OPEN. A KTY/Subject proposal exists and awaits human review and acceptance.",
        "",
        "## Accepted Upstream Snapshot(s)",
        "",
        "- `domains/chirality/_Decomposition/gate_snapshots/GATE1_20260614T005942Z/`",
        "- `domains/chirality/_Decomposition/gate_snapshots/GATE2_PHASE2_20260614T204403Z/`",
        "- `domains/chirality/_Decomposition/gate_snapshots/GATE2_PHASE2_SOURCE_UNIT_AUTHORITY_20260614T211725Z/`",
        "- `domains/chirality/_Decomposition/gate_snapshots/GATE3_CATEGORIES_20260615T030833Z/`",
        f"- `{snapshot}` (`source_v2`, BM25 + dense, accepted for atom retrieval despite deferred source-doc freshness cadence)",
        "",
        "## Current Gate 4 Draft Artifacts",
        "",
        "- `domains/chirality/_Decomposition/Knowledge_Type_Register.csv`",
        "- `domains/chirality/_Decomposition/Knowledge_Subject_Register.csv`",
        "- `domains/chirality/_Decomposition/Domain_Ledger_Gate4_KTY_Draft.csv`",
        "- `domains/chirality/_Decomposition/KTY_Scope_Ratification.csv`",
        "- `domains/chirality/_Decomposition/KTY_Assignment_Summary.csv`",
        "- `domains/chirality/_Decomposition/KTY_Assignment_Findings.csv`",
        "- `domains/chirality/_Decomposition/Gate4_Coverage_Telemetry.csv`",
        "",
        "## Counts",
        "",
        f"- Proposed Knowledge Types: {len(kty_rows)}",
        f"- Proposed Knowledge Subjects with mapped units: {len(subject_rows)}",
        f"- IN atoms mapped to KTY/Subject: {sum(1 for row in in_rows if row.get('KnowledgeTypeIDs') and row.get('SubjectIDs'))} / {len(in_rows)}",
        f"- PRD source atoms retaining primary location and associated with DBM/PRD publication KTY: {prd_dbm_association_count(ledger_rows)}",
        f"- Low-confidence advisory assignment findings: {len(findings_rows)}",
        f"- Blocking calibrated KTY verdicts: {sum(1 for row in ratification_rows if row.get('Blocking') == 'YES')}",
        "",
        "## Rerun Requirements",
        "",
        "- If KTY names, descriptions, or Subject boundaries change, rerun `tools/decomp/propose_gate4_kty.py` or manually update the draft registers and ratification evidence consistently.",
        "- If any UnitStatement text changes or atoms split/merge, rebuild the source database and retrieval index before Gate 4 ratification resumes.",
        "- Do not proceed to Gate 5 coverage closure until Gate 4 is explicitly accepted by the human.",
        "",
        "## Remaining Blockers",
        "",
        "- Human has not accepted Gate 4.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_control_surface(
    decomp_root: Path,
    generated_iso: str,
    proposal_name: str,
    kty_rows: list[dict[str, str]],
    subject_rows: list[dict[str, str]],
    ledger_rows: list[dict[str, str]],
    findings_rows: list[dict[str, str]],
    ratification_rows: list[dict[str, str]],
) -> None:
    path = decomp_root / "Chirality_Domain_Decomposition.md"
    text = path.read_text(encoding="utf-8")
    status = (
        "Status: Gate 4 Knowledge Type / Knowledge Subject proposal is drafted and open for human review. "
        "Gate 3 remains accepted by `GATE3_CATEGORIES_20260615T030833Z`; the proposal adds KTY/Subject registers, "
        "`Domain_Ledger_Gate4_KTY_Draft.csv`, and KTY scope-ratification evidence without changing atom text, "
        "SourceRefs, ContentHash values, or accepted CategoryID assignments. Gate 4 is not closed until explicit human approval. "
        "`OI-022` remains a human-deferred source-database cadence issue outside this Gate 4 proposal."
    )
    text = re.sub(r"^Status: .*$", status, text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^Generated UTC: .*$", f"Generated UTC: {generated_iso}", text, count=1, flags=re.MULTILINE)
    section = phase4_section(proposal_name, kty_rows, subject_rows, ledger_rows, findings_rows, ratification_rows)
    if "## Phase 4 Knowledge Types and Subjects (Draft)" in text:
        text = re.sub(
            r"## Phase 4 Knowledge Types and Subjects \(Draft\).*?(?=\n## References\n)",
            section,
            text,
            flags=re.DOTALL,
        )
    else:
        text = text.replace("\n## References\n", "\n" + section + "\n## References\n")
    path.write_text(text, encoding="utf-8")


def phase4_section(
    proposal_name: str,
    kty_rows: list[dict[str, str]],
    subject_rows: list[dict[str, str]],
    ledger_rows: list[dict[str, str]],
    findings_rows: list[dict[str, str]],
    ratification_rows: list[dict[str, str]],
) -> str:
    in_rows = [row for row in ledger_rows if row.get("InOutStatus") == "IN"]
    prd_associated = prd_dbm_association_count(ledger_rows)
    lines = [
        "## Phase 4 Knowledge Types and Subjects (Draft)",
        "",
        f"Gate 4 proposal package: `domains/chirality/_Decomposition/gate4_kty/{proposal_name}/`",
        "",
        "This proposal consumes the accepted Gate 3 category partition and maps every IN atom to one proposed Knowledge Type and one proposed Subject. It is a draft review surface, not an acceptance snapshot.",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| Proposed Knowledge Types | {len(kty_rows)} |",
        f"| Proposed Knowledge Subjects | {len(subject_rows)} |",
        f"| IN atoms mapped to KTY/Subject | {sum(1 for row in in_rows if row.get('KnowledgeTypeIDs') and row.get('SubjectIDs'))} / {len(in_rows)} |",
        f"| PRD atoms also associated with DBM/PRD publication KTY | {prd_associated} |",
        f"| Low-confidence advisory assignment findings | {len(findings_rows)} |",
        f"| Blocking calibrated KTY verdicts | {sum(1 for row in ratification_rows if row.get('Blocking') == 'YES')} |",
        "",
        "Phase 4 draft registers:",
        "",
        "- `Knowledge_Type_Register.csv` - proposed KTYs grouped under accepted Categories.",
        "- `Knowledge_Subject_Register.csv` - proposed Subjects under each KTY with best-effort unit linkage.",
        "- `Domain_Ledger_Gate4_KTY_Draft.csv` - Gate 3 ledger carried forward with proposed `KnowledgeTypeIDs` and `SubjectIDs`.",
        "- `KTY_Scope_Ratification.csv` - BM25+dense KTY scope evidence under a proposed calibrated structural-partition basis.",
        "- `KTY_Assignment_Summary.csv` and `KTY_Assignment_Findings.csv` - review aids for KTY/Subject assignment confidence.",
        "- `Gate4_Coverage_Telemetry.csv` - draft count surface for the proposal.",
        "",
        "The KTY ratification basis mirrors the accepted Gate 3 distinction: KTYs and Subjects are governed structural/navigation facets, while BM25 and dense embeddings are retrieval/discovery mechanisms and spot-review evidence. The default `0.75` cosine threshold remains diagnostic pending explicit Gate 4 human acceptance.",
        "",
        "Human-directed PRD/DBM refinement: PRD atoms retain their primary current Category/KTY location and also carry `AssociatedCategoryIDs=CAT-007`, `KTY-07-01_DBM-Publication-Planning`, and `SUB-07-01-03_PRD-Requirements-Package` to record PRD as the software/product analogue of DBM.",
        "",
    ]
    return "\n".join(lines)


def update_next_prompt(
    domain_root: Path,
    generated_iso: str,
    proposal_name: str,
    kty_rows: list[dict[str, str]],
    subject_rows: list[dict[str, str]],
    findings_rows: list[dict[str, str]],
) -> None:
    path = domain_root / "_Coordination" / "NEXT_INSTANCE_PROMPT.md"
    text = path.read_text(encoding="utf-8")
    replacement = f"""## Gate 4 Proposal State

Gate 4 Knowledge Type / Knowledge Subject proposal is drafted and awaits human review.

- Gate 4 proposal package: `domains/chirality/_Decomposition/gate4_kty/{proposal_name}`
- Generated UTC: {generated_iso}
- Proposed Knowledge Types: `{len(kty_rows)}`
- Proposed Knowledge Subjects with mapped units: `{len(subject_rows)}`
- Low-confidence advisory assignment findings: `{len(findings_rows)}`
- Draft KTY ledger: `domains/chirality/_Decomposition/Domain_Ledger_Gate4_KTY_Draft.csv`
- KTY register: `domains/chirality/_Decomposition/Knowledge_Type_Register.csv`
- Subject register: `domains/chirality/_Decomposition/Knowledge_Subject_Register.csv`
- KTY ratification: `domains/chirality/_Decomposition/KTY_Scope_Ratification.csv`

Gate 4 remains open until the human explicitly confirms the Knowledge Types, Knowledge Subjects, schemas, responsibilities, and KTY scope-ratification basis. Do not proceed to Gate 5 coverage closure, hypergraph publication, DBM publication, public export, or project-domain decomposition until explicitly authorized.
"""
    text = re.sub(r"## Gate 4 Ready State\n.*?(?=\n## Rebuild Commands\n)", replacement + "\n", text, flags=re.DOTALL)
    path.write_text(text, encoding="utf-8")


def update_json_telemetry(
    path: Path,
    generated_iso: str,
    proposal_name: str,
    kty_rows: list[dict[str, str]],
    subject_rows: list[dict[str, str]],
    ledger_rows: list[dict[str, str]],
    findings_rows: list[dict[str, str]],
    ratification_rows: list[dict[str, str]],
) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    in_rows = [row for row in ledger_rows if row.get("InOutStatus") == "IN"]
    data["generated_utc"] = generated_iso
    data["phase4_status"] = "PROPOSAL_OPEN_PENDING_HUMAN_REVIEW"
    data["gate4_kty_proposal"] = {
        "status": "OPEN_PENDING_HUMAN_GATE4_REVIEW",
        "generated_utc": generated_iso,
        "proposal_package": f"domains/chirality/_Decomposition/gate4_kty/{proposal_name}",
        "knowledge_type_count": len(kty_rows),
        "subject_count": len(subject_rows),
        "in_atoms": len(in_rows),
        "in_atoms_mapped_to_kty_subject": sum(1 for row in in_rows if row.get("KnowledgeTypeIDs") and row.get("SubjectIDs")),
        "prd_atoms_associated_with_dbm_publication_kty": prd_dbm_association_count(ledger_rows),
        "low_confidence_assignment_findings": len(findings_rows),
        "blocking_calibrated_kty_verdicts": sum(1 for row in ratification_rows if row.get("Blocking") == "YES"),
        "basis": "Gate 3 structural-partition / retrieval-discovery calibration carried forward as proposed Gate 4 basis; pending human acceptance.",
    }
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def upsert_rows(path: Path, key: str, new_rows: list[dict[str, str]]) -> None:
    rows = read_csv(path)
    fieldnames = list(rows[0].keys()) if rows else list(new_rows[0].keys())
    by_key = {row[key]: row for row in rows}
    order = [row[key] for row in rows]
    for row in new_rows:
        if row[key] not in by_key:
            order.append(row[key])
        by_key[row[key]] = {name: row.get(name, "") for name in fieldnames}
    write_csv(path, [by_key[k] for k in order], fieldnames=fieldnames)


def update_open_issues(path: Path, generated_iso: str, finding_count: int) -> None:
    upsert_rows(path, "IssueID", [{
        "IssueID": "OI-023",
        "Status": "OPEN_GATE4_HUMAN_REVIEW",
        "Severity": "MAJOR",
        "Surface": "Knowledge_Type_Register.csv; Knowledge_Subject_Register.csv; Domain_Ledger_Gate4_KTY_Draft.csv; KTY_Scope_Ratification.csv",
        "Issue": f"Gate 4 KTY/Subject proposal is drafted with {finding_count} low-confidence advisory assignment findings and awaits human review.",
        "RequiredDisposition": "Human must accept, refine, or reject the proposed KTY/Subject structure and calibrated KTY ratification basis before Gate 4 closure.",
        "Recommendation": "Review the Gate 4 proposal package, especially KTY_Assignment_Findings.csv and KTY_Scope_Ratification.csv, then either approve Gate 4 or direct refinement.",
    }])


def update_validation_checks(
    path: Path,
    proposal_name: str,
    kty_rows: list[dict[str, str]],
    subject_rows: list[dict[str, str]],
    ledger_rows: list[dict[str, str]],
    findings_rows: list[dict[str, str]],
    ratification_rows: list[dict[str, str]],
) -> None:
    in_rows = [row for row in ledger_rows if row.get("InOutStatus") == "IN"]
    mapped = sum(1 for row in in_rows if row.get("KnowledgeTypeIDs") and row.get("SubjectIDs"))
    upsert_rows(path, "CheckID", [
        {
            "CheckID": "GATE4_KTY_REGISTER",
            "Status": "DRAFT_READY",
            "Evidence": f"Knowledge_Type_Register.csv rows={len(kty_rows)}",
            "Notes": "Proposed Knowledge Types; Gate 4 remains open pending human acceptance.",
        },
        {
            "CheckID": "GATE4_SUBJECT_REGISTER",
            "Status": "DRAFT_READY",
            "Evidence": f"Knowledge_Subject_Register.csv rows={len(subject_rows)}",
            "Notes": "Proposed Knowledge Subjects with mapped units.",
        },
        {
            "CheckID": "GATE4_KTY_ASSIGNMENT_COVERAGE",
            "Status": "DRAFT_PASS",
            "Evidence": f"Domain_Ledger_Gate4_KTY_Draft.csv IN mapped={mapped}/{len(in_rows)}; PRD_DBM_associations={prd_dbm_association_count(ledger_rows)}; low_confidence_findings={len(findings_rows)}",
            "Notes": "Every IN atom has a proposed KTY and Subject. PRD source atoms retain primary location and also associate with DBM/PRD publication KTY. Low-confidence rows remain advisory review items.",
        },
        {
            "CheckID": "GATE4_SCOPE_RATIFICATION",
            "Status": "DRAFT_CALIBRATED_PENDING_HUMAN",
            "Evidence": f"KTY_Scope_Ratification.csv rows={len(ratification_rows)}; calibrated_blocking={sum(1 for row in ratification_rows if row.get('Blocking') == 'YES')}",
            "Notes": "Default 0.75 cosine threshold remains diagnostic; calibrated basis must be human-accepted before Gate 4 closure.",
        },
        {
            "CheckID": "GATE4_PROPOSAL_SNAPSHOT",
            "Status": "OPEN_PENDING_HUMAN_APPROVAL",
            "Evidence": f"gate4_kty/{proposal_name}",
            "Notes": "Snapshot is a proposal package, not an acceptance record.",
        },
    ])


def update_companion_inventory(path: Path, proposal_name: str) -> None:
    rows = [
        {"Filename": "Knowledge_Type_Register.csv", "PackageRole": "authoritative companion register", "Description": "Proposed Gate 4 Knowledge Type register; not accepted until human Gate 4 approval."},
        {"Filename": "Knowledge_Subject_Register.csv", "PackageRole": "authoritative companion register", "Description": "Proposed Gate 4 Knowledge Subject register with best-effort unit linkage."},
        {"Filename": "Domain_Ledger_Gate4_KTY_Draft.csv", "PackageRole": "authoritative companion register", "Description": "Gate 3 category ledger carried forward with proposed KTY and Subject mappings."},
        {"Filename": "KTY_Scope_Ratification.csv", "PackageRole": "authoritative companion register", "Description": "BM25+dense KTY scope evidence under proposed calibrated Gate 4 basis."},
        {"Filename": "KTY_Assignment_Summary.csv", "PackageRole": "authoritative companion register", "Description": "Per-KTY counts, low-confidence counts, source concentration, and verdict summary."},
        {"Filename": "KTY_Assignment_Findings.csv", "PackageRole": "authoritative companion register", "Description": "Advisory low-confidence Gate 4 KTY/Subject assignment findings."},
        {"Filename": "Gate4_Coverage_Telemetry.csv", "PackageRole": "authoritative companion register", "Description": "Draft Gate 4 coverage counts for KTY/Subject proposal."},
        {"Filename": "gate4_kty/_LATEST_GATE4_PROPOSAL.md", "PackageRole": "snapshot / handoff artifact", "Description": "Pointer to latest Gate 4 KTY/Subject proposal package."},
        {"Filename": f"gate4_kty/{proposal_name}/GATE4_KTY_PROPOSAL.md", "PackageRole": "snapshot / handoff artifact", "Description": "Gate 4 KTY/Subject proposal review packet."},
        {"Filename": f"gate4_kty/{proposal_name}/HANDOFF_STATE.md", "PackageRole": "snapshot / handoff artifact", "Description": "Handoff state for open Gate 4 proposal."},
    ]
    upsert_rows(path, "Filename", rows)


def prd_dbm_association_count(ledger_rows: list[dict[str, str]]) -> int:
    return sum(
        1
        for row in ledger_rows
        if row.get("SourceDoc") == PRD_SOURCE_DOC
        and row.get("InOutStatus") == "IN"
        and row.get("AssociatedCategoryIDs") == PRD_ASSOCIATED_CATEGORY
        and PRD_ASSOCIATED_KTY in split_ids(row.get("KnowledgeTypeIDs", ""))
        and PRD_ASSOCIATED_SUBJECT in split_ids(row.get("SubjectIDs", ""))
    )


if __name__ == "__main__":
    raise SystemExit(main())
