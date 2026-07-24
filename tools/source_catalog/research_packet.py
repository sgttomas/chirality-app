#!/usr/bin/env python3
"""Canonical research-packet schema (single source of truth).

These constants mirror the packet contract defined in `agents/AGENT_RESEARCH.md`
(STRUCTURE block). `scaffold_research_packet.py` emits files with these headers and
`query_source_index.py` logs with `QUERY_LOG_COLUMNS`, so the agent doc and the tools
cannot silently diverge. If `AGENT_RESEARCH.md` STRUCTURE changes, update this module.

This file is importable data only (no LLM, no side effects).
"""
from __future__ import annotations

import re

QUERY_LOG_COLUMNS = [
    "QueryID", "UTC", "DomainRoot", "Snapshot", "Mode",
    "Query", "Filters", "K", "ResultCount", "Notes",
]

EVIDENCE_MAP_COLUMNS = [
    "EvidenceID", "ClaimID", "EvidenceLevel", "SourceKind", "ArtifactPath",
    "SourceDocID", "SourceRef", "AtomicUnitID", "SectionID", "CategoryID",
    "KnowledgeTypeID", "SubjectID", "RetrievalMode", "Rank", "Score",
    "QuotedOrParaphrasedEvidence", "Interpretation", "Limitations",
    "VerificationSource", "AssertionMode", "LoadBearing",
]

CONFLICT_COLUMNS = [
    "ConflictID", "ClaimID", "ConflictKind", "Description", "Contenders",
    "SourceRefs", "ProposedAuthority", "HumanRuling", "Limitations",
]

AMENDMENT_CANDIDATE_COLUMNS = [
    "AmendmentID", "ClaimID", "CandidateKind", "TargetSurface", "CurrentState",
    "ProposedChange", "EvidenceRefs", "LoadBearing", "VerificationSource",
    "RecommendedRoute", "HumanRuling", "Limitations",
]

OPEN_QUESTION_COLUMNS = [
    "OpenQuestionID", "ClaimID", "Question", "WhyItMatters", "EvidenceNeeded", "Status",
]

# filename -> header columns (CSV members of the packet, in canonical order)
PACKET_CSV_FILES: dict[str, list[str]] = {
    "Query_Log.csv": QUERY_LOG_COLUMNS,
    "Evidence_Map.csv": EVIDENCE_MAP_COLUMNS,
    "Conflicts.csv": CONFLICT_COLUMNS,
    "Amendment_Candidates.csv": AMENDMENT_CANDIDATE_COLUMNS,
    "Open_Questions.csv": OPEN_QUESTION_COLUMNS,
}

RESEARCH_NOTE_TEMPLATE = """# Research Note - {topic}

Status: DERIVATIVE_RESEARCH_PACKET

## Question

## Accepted Basis

## Short Answer

## Evidence

## Interpretation

## Caveats

## Open Questions

## Handoff / Next Action
"""

HANDOFF_STATE_TEMPLATE = """# Handoff State - {packet}

Status: DERIVATIVE_RESEARCH_PACKET (immutable run snapshot)

## Accepted Upstream Snapshot(s)

## Retrieval Snapshot(s)

## Derivative-Package Status

## Caveats

## Conflict Status

## Coverage Gaps

## Pointer Status

## Recommended Downstream Action
"""

LATEST_TEMPLATE = """# Latest Research Packet Pointer

This pointer is for discovery only. It is not substitute authority. Research packets are
derivative, immutable run snapshots.

Latest: {packet}/
Updated: {utc}
Topic: {topic}
"""


def packet_slug(value: str) -> str:
    """Lowercase, underscore-joined slug for RCH_<UTC>_<slug> (e.g. 'runtime_stabilization')."""
    token = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
    return token or "untitled"
