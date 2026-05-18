from __future__ import annotations

import csv
import sys
from pathlib import Path


COORDINATION_DIR = Path(__file__).resolve().parent
if str(COORDINATION_DIR) not in sys.path:
    sys.path.insert(0, str(COORDINATION_DIR))

from accumulate_supersession_map import SUPERSESSION_COLUMNS, compare_maps, load_all  # noqa: E402


def row(decision_id: str) -> dict[str, str]:
    values = {column: "" for column in SUPERSESSION_COLUMNS}
    values.update({
        "AmendmentID": "SCA-001",
        "DecisionID": decision_id,
        "SupersededAuthorityRole": "SOURCE_DBM",
        "SupersededAuthorityPath": "_Sources/source.md",
        "SupersededAuthorityRef": "section 1",
        "SupersededFactKey": f"FACT_{decision_id}",
        "SupersededFactTextOrValue": "old",
        "OverrideType": "SUPERSESSION",
        "ReplacementFactTextOrValue": "new",
        "AppliesToRoots": "Root",
        "AppliesToFacilities": "03-25",
    })
    return values


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=SUPERSESSION_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def test_load_all_merges_and_deduplicates_rows(tmp_path: Path) -> None:
    prior = tmp_path / "prior.csv"
    delta = tmp_path / "delta.csv"
    write_csv(prior, [row("D-001")])
    write_csv(delta, [row("D-001"), row("D-002")])

    rows = load_all([prior], [delta])

    assert [r["DecisionID"] for r in rows] == ["D-001", "D-002"]


def test_compare_maps_reports_missing_expected_row(tmp_path: Path) -> None:
    check_map = tmp_path / "Supersession_Map.csv"
    write_csv(check_map, [row("D-001")])

    findings = compare_maps([row("D-001"), row("D-002")], check_map)

    assert len(findings) == 1
    assert findings[0].category == "MISSING_EXPECTED_ROW"
    assert findings[0].severity == "CRITICAL"


def test_allow_empty_returns_header_only_rows() -> None:
    assert load_all([], [], allow_empty=True) == []
