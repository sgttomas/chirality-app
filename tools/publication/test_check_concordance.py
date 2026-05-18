from __future__ import annotations

import sys
from pathlib import Path


PUBLICATION_DIR = Path(__file__).resolve().parent
if str(PUBLICATION_DIR) not in sys.path:
    sys.path.insert(0, str(PUBLICATION_DIR))

from check_concordance import compare_values, evaluate_register  # noqa: E402


def test_compare_exact():
    assert compare_values("EXACT", "", "450 psig", "450 PSIG")


def test_compare_round_n():
    assert compare_values("ROUND_N", "1", "450.04", "450.0")


def test_compare_token_match():
    assert compare_values("TOKEN_MATCH", "", "West Doe 04-25", "west-doe 04 25")


def test_referred_passes():
    register = [{"AssertionKey": "A", "AuthoritySectionID": "SEC-01", "RequiredSectionIDs": "SEC-02", "ComparisonRule": "EXACT"}]
    assertions = {
        "SEC-01": {"A": [{"AssertionKey": "A", "AssertionStatus": "ASSERTED", "NormalizedValue": "X"}]},
        "SEC-02": {"A": [{"AssertionKey": "A", "AssertionStatus": "REFERRED", "NormalizedValue": ""}]},
    }
    findings, metrics = evaluate_register(register, assertions)
    assert findings == []
    assert metrics["passed_assertions"] == 1


def test_missing_authority_finding():
    register = [{"AssertionKey": "A", "AuthoritySectionID": "SEC-01", "RequiredSectionIDs": "", "ComparisonRule": "EXACT"}]
    findings, _ = evaluate_register(register, {})
    assert findings[0]["FindingType"] == "MISSING_AUTHORITY_ASSERTION"
    assert findings[0]["Blocking"] == "TRUE"


def test_omitted_blocking_produces_finding():
    register = [{"AssertionKey": "A", "AuthoritySectionID": "SEC-01", "RequiredSectionIDs": "SEC-02", "ComparisonRule": "EXACT"}]
    assertions = {
        "SEC-01": {"A": [{"AssertionKey": "A", "AssertionStatus": "ASSERTED", "NormalizedValue": "X"}]},
        "SEC-02": {"A": [{"AssertionKey": "A", "AssertionStatus": "OMITTED_BLOCKING", "NormalizedValue": ""}]},
    }
    findings, _ = evaluate_register(register, assertions)
    assert findings[0]["FindingType"] == "OMITTED_BLOCKING"
    assert findings[0]["Blocking"] == "TRUE"


def test_omitted_with_rationale_non_blocking():
    register = [{"AssertionKey": "A", "AuthoritySectionID": "SEC-01", "RequiredSectionIDs": "SEC-02", "ComparisonRule": "EXACT"}]
    assertions = {
        "SEC-01": {"A": [{"AssertionKey": "A", "AssertionStatus": "ASSERTED", "NormalizedValue": "X"}]},
        "SEC-02": {"A": [{"AssertionKey": "A", "AssertionStatus": "OMITTED_WITH_RATIONALE", "NormalizedValue": ""}]},
    }
    findings, _ = evaluate_register(register, assertions)
    assert findings[0]["FindingType"] == "OMITTED_WITH_RATIONALE"
    assert findings[0]["Blocking"] == "FALSE"
