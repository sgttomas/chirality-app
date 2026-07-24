from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "plans" / "reviews" / "PR188_multi_agent_review_2026-07-11.md"
DISPOSITION = ROOT / "docs" / "governance_harness" / "PR188_REVIEW_DISPOSITION.md"


def ids(text: str) -> set[str]:
    return set(re.findall(r"\b(?:C\d{2}|H\d{2}|V\d{2})\b", text))


def test_every_numbered_pr188_finding_has_a_disposition() -> None:
    source_ids = ids(SOURCE.read_text(encoding="utf-8"))
    disposition_ids = ids(DISPOSITION.read_text(encoding="utf-8"))

    expected = {
        *(f"C{number:02d}" for number in range(1, 62)),
        *(f"H{number:02d}" for number in range(1, 5)),
        *(f"V{number:02d}" for number in range(1, 9)),
    }

    assert source_ids == expected
    assert expected <= disposition_ids
