from __future__ import annotations

import sys
from pathlib import Path


PUBLICATION_DIR = Path(__file__).resolve().parent
if str(PUBLICATION_DIR) not in sys.path:
    sys.path.insert(0, str(PUBLICATION_DIR))

from validate_source_supersession import find_applicable_supersession, validate  # noqa: E402


def test_find_applicable_supersession_treats_blank_sections_as_global():
    rows = [
        {
            "AmendmentID": "SCA-001",
            "DecisionID": "D-001",
            "SupersededFactKey": "FACT_A",
            "OverrideType": "SUPERSESSION",
            "ReplacementFactTextOrValue": "replacement a",
            "AppliesToRoots": "West_Doe_Deepcut_DBM",
            "AppliesToFacilities": "04-25",
            "AppliesToSections": "",
        }
    ]

    row = find_applicable_supersession(
        rows,
        root_name="West_Doe_Deepcut_DBM",
        facility_id="04-25",
        section_id="SEC-08",
    )

    assert row is not None
    assert row["SupersededFactKey"] == "FACT_A"


def test_validate_prefers_superseded_fact_key_bridge_and_reports_pass_overridden():
    source_fidelity_keys = {
        "ASSERTION_KEY_A": {
            "AssertionKey": "ASSERTION_KEY_A",
            "AuthoritySectionID": "SEC-08",
            "SourceExpectedValue": "source value",
            "SupersededFactKey": "FACT_A",
        }
    }
    section_assertions = {
        "SEC-08": [
            {
                "AssertionKey": "ASSERTION_KEY_A",
                "AssertionStatus": "ASSERTED",
                "NormalizedValue": "replacement value",
            }
        ]
    }
    supersession_map = {
        "FACT_A": [
            {
                "AmendmentID": "SCA-001",
                "DecisionID": "D-001",
                "SupersededFactKey": "FACT_A",
                "OverrideType": "SUPERSESSION",
                "ReplacementFactTextOrValue": "replacement value",
                "AppliesToRoots": "West_Doe_Deepcut_DBM",
                "AppliesToFacilities": "04-25",
                "AppliesToSections": "",
            }
        ]
    }

    findings, metrics = validate(
        source_fidelity_keys,
        section_assertions,
        supersession_map,
        root_name="West_Doe_Deepcut_DBM",
        facility_id="04-25",
    )

    assert metrics["pass_overridden"] == 1
    assert metrics["unmatched_divergence"] == 0
    assert findings[0]["FindingType"] == "PASS_OVERRIDDEN"


def test_validate_blocks_when_root_facility_filter_excludes_binding():
    source_fidelity_keys = {
        "ASSERTION_KEY_A": {
            "AssertionKey": "ASSERTION_KEY_A",
            "AuthoritySectionID": "SEC-08",
            "SourceExpectedValue": "source value",
            "SupersededFactKey": "FACT_A",
        }
    }
    section_assertions = {
        "SEC-08": [
            {
                "AssertionKey": "ASSERTION_KEY_A",
                "AssertionStatus": "ASSERTED",
                "NormalizedValue": "replacement value",
            }
        ]
    }
    supersession_map = {
        "FACT_A": [
            {
                "AmendmentID": "SCA-001",
                "DecisionID": "D-001",
                "SupersededFactKey": "FACT_A",
                "OverrideType": "SUPERSESSION",
                "ReplacementFactTextOrValue": "replacement value",
                "AppliesToRoots": "West_Doe_Comp_and_Liquids_DBM",
                "AppliesToFacilities": "03-25",
                "AppliesToSections": "",
            }
        ]
    }

    findings, metrics = validate(
        source_fidelity_keys,
        section_assertions,
        supersession_map,
        root_name="West_Doe_Deepcut_DBM",
        facility_id="04-25",
    )

    assert metrics["pass_overridden"] == 0
    assert metrics["unmatched_divergence"] == 1
    assert findings[0]["FindingType"] == "UNMATCHED_SOURCE_DIVERGENCE"
