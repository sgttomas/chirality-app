from pathlib import Path

import tools.source_catalog.research_packet as rp

# rp.__file__ = <repo>/tools/source_catalog/research_packet.py -> repo root is parents[2].
_AGENT_RESEARCH = Path(rp.__file__).resolve().parents[2] / "agents" / "AGENT_RESEARCH.md"


def test_agent_research_doc_headers_match_packet_constants():
    """The AGENT_RESEARCH.md STRUCTURE block restates the packet column headers in prose.
    The tools import these constants, but the doc copy is unguarded — assert each canonical
    header appears verbatim in the doc so the agent contract and the tools cannot drift."""
    lines = {ln.strip() for ln in _AGENT_RESEARCH.read_text(encoding="utf-8").splitlines()}
    for label, cols in {
        "Query_Log": rp.QUERY_LOG_COLUMNS,
        "Evidence_Map": rp.EVIDENCE_MAP_COLUMNS,
        "Conflicts": rp.CONFLICT_COLUMNS,
        "Amendment_Candidates": rp.AMENDMENT_CANDIDATE_COLUMNS,
        "Open_Questions": rp.OPEN_QUESTION_COLUMNS,
    }.items():
        header = ",".join(cols)
        assert header in lines, (
            f"{label} header drifted: AGENT_RESEARCH.md is missing the canonical line "
            f"'{header}'. Update the doc STRUCTURE block or research_packet.py so they agree."
        )


def test_packet_slug_lowercases_and_underscores():
    assert rp.packet_slug("Demo Topic!") == "demo_topic"
    assert rp.packet_slug("Runtime  Stabilization") == "runtime_stabilization"
    assert rp.packet_slug("---") == "untitled"


def test_evidence_map_appends_new_columns_at_end():
    # The three new columns must be appended (never inserted) so positional readers don't break.
    assert rp.EVIDENCE_MAP_COLUMNS[-3:] == ["VerificationSource", "AssertionMode", "LoadBearing"]
    assert rp.EVIDENCE_MAP_COLUMNS[:18][-1] == "Limitations"


def test_query_log_columns_are_canonical():
    assert rp.QUERY_LOG_COLUMNS == [
        "QueryID", "UTC", "DomainRoot", "Snapshot", "Mode",
        "Query", "Filters", "K", "ResultCount", "Notes",
    ]


def test_amendment_candidate_columns_present():
    assert rp.AMENDMENT_CANDIDATE_COLUMNS[0] == "AmendmentID"
    assert "RecommendedRoute" in rp.AMENDMENT_CANDIDATE_COLUMNS
    assert "LoadBearing" in rp.AMENDMENT_CANDIDATE_COLUMNS


def test_packet_csv_files_cover_the_five_csvs():
    assert set(rp.PACKET_CSV_FILES) == {
        "Query_Log.csv", "Evidence_Map.csv", "Conflicts.csv",
        "Amendment_Candidates.csv", "Open_Questions.csv",
    }
