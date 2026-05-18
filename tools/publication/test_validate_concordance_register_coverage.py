from __future__ import annotations

import sys
from pathlib import Path


PUBLICATION_DIR = Path(__file__).resolve().parent
if str(PUBLICATION_DIR) not in sys.path:
    sys.path.insert(0, str(PUBLICATION_DIR))

from validate_concordance_register_coverage import validate  # noqa: E402


REGISTER_HEADER = [
    "AssertionKey",
    "AssertionLabel",
    "AssertionDomain",
    "AssertionType",
    "CanonicalTerm",
    "Unit",
    "ComparisonRule",
    "ComparisonParameter",
    "AuthoritySectionID",
    "RequiredSectionIDs",
    "FacilityScope",
    "CurrentStateBasis",
    "DecisionRefs",
    "DiscoverySource",
    "NormalizationHint",
    "NormalizationContract",
    "Criticality",
    "SourceFidelityCritical",
    "SourceExpectedValue",
    "Notes",
]


def register_row(**overrides):
    row = {key: "X" for key in REGISTER_HEADER}
    row.update(
        {
            "AssertionKey": "A",
            "AuthoritySectionID": "SEC-01",
            "RequiredSectionIDs": "SEC-02",
            "SourceFidelityCritical": "NO",
            "SourceExpectedValue": "",
            "NormalizationContract": "EXACT",
        }
    )
    row.update(overrides)
    return row


def test_high_risk_covered_passes():
    risk = [{"RiskID": "R1", "CoverageStatus": "COVERED_BY_REGISTER", "RegisterAssertionKey": "A"}]
    section_map = [{"SectionID": "SEC-01", "ArtifactPath": "a.md", "MappingRole": "PRIMARY"}, {"SectionID": "SEC-02"}]
    findings = validate(risk, [register_row()], REGISTER_HEADER, section_map)
    assert findings == []


def test_high_risk_uncovered_blocks():
    risk = [{"RiskID": "R1", "CoverageStatus": "", "RegisterAssertionKey": ""}]
    findings = validate(risk, [register_row()], REGISTER_HEADER, [{"SectionID": "SEC-01"}, {"SectionID": "SEC-02"}])
    assert findings[0]["FindingType"] == "UNCOVERED_HIGH_RISK"
    assert findings[0]["Blocking"] == "TRUE"


def test_waiver_accepted():
    risk = [{"RiskID": "R1", "CoverageStatus": "WAIVED_WITH_RATIONALE", "WaiverReason": "Not cross-section."}]
    findings = validate(risk, [register_row()], REGISTER_HEADER, [{"SectionID": "SEC-01"}, {"SectionID": "SEC-02"}])
    assert findings == []


def test_deferred_blocking_accepted():
    risk = [{"RiskID": "R1", "CoverageStatus": "DEFERRED_BLOCKING"}]
    findings = validate(risk, [register_row()], REGISTER_HEADER, [{"SectionID": "SEC-01"}, {"SectionID": "SEC-02"}])
    assert findings == []


def test_retired_authority_detected():
    risk = [
        {
            "RiskID": "R1",
            "RiskClass": "RETIRED_CONTENT_REFERENCE",
            "CoverageStatus": "OUT_OF_SCOPE",
            "SourceArtifact": "/tmp/ka.md",
            "AffectedSectionIDs": "SEC-01",
        }
    ]
    section_map = [{"SectionID": "SEC-01", "ArtifactPath": "/tmp/ka.md", "MappingRole": "PRIMARY"}, {"SectionID": "SEC-02"}]
    findings = validate(risk, [register_row()], REGISTER_HEADER, section_map)
    assert any(row["FindingType"] == "RETIRED_ARTIFACT_MAPPED_AS_PRIMARY" for row in findings)


def test_source_fidelity_missing_value():
    findings = validate(
        [],
        [register_row(SourceFidelityCritical="YES", SourceExpectedValue="", Notes="")],
        REGISTER_HEADER,
        [{"SectionID": "SEC-01"}, {"SectionID": "SEC-02"}],
    )
    assert any(row["FindingType"] == "SOURCE_FIDELITY_EXPECTED_VALUE_MISSING" for row in findings)
