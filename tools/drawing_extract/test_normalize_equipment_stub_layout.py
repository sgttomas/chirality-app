from __future__ import annotations

import copy
import csv
import sys
from pathlib import Path

import pytest


DRAWING_EXTRACT_DIR = Path(__file__).resolve().parent
if str(DRAWING_EXTRACT_DIR) not in sys.path:
    sys.path.insert(0, str(DRAWING_EXTRACT_DIR))

from normalize_equipment_stub_layout import (  # noqa: E402
    build_column_order,
    parse_stub,
    parse_stub_text,
    render_stub,
    resolve_stub_path,
)
import report_stub_counts as report_mod  # noqa: E402
import sanitize_equipment_stubs as sanitize_mod  # noqa: E402
import validate_stub_format as validate_mod  # noqa: E402


PDF_STEM = "sample_pdf"
DRAWING_TYPE = "PFD"


def make_detailed_data(
    *,
    status: str = "SUCCESS",
    rows: list[list[str]] | None = None,
    source_page: int = 7,
    drawing: str = "PFD-1",
    system_name: str = "SYS",
) -> dict:
    requested_known_fields = [
        "equipment_type",
        "equipment_description",
        "capacity_text",
        "power_text",
    ]
    requested_extra_fields: list[dict[str, str]] = []
    return {
        "format_version": "v2",
        "drawing_type": DRAWING_TYPE,
        "extraction_target": "top_equipment_header_detailed",
        "source_pdf": "sample.pdf",
        "source_page": source_page,
        "requested_known_fields": requested_known_fields,
        "requested_extra_fields": requested_extra_fields,
        "required_fields": list(requested_known_fields),
        "drawing": drawing,
        "system_name": system_name,
        "status": status,
        "note": (
            "Top-of-sheet equipment header present."
            if status == "SUCCESS"
            else "No separated top-of-sheet equipment header was identified."
        ),
        "columns": build_column_order(
            "top_equipment_header_detailed",
            requested_known_fields,
            requested_extra_fields,
        ),
        "rows": rows
        if rows is not None
        else [
            [
                "T-100",
                "TEST TANK",
                system_name,
                drawing,
                "VESSEL",
                "VERTICAL TEST TANK",
                "10 m3",
                "5 kW",
            ]
        ],
    }


def make_basic_data(
    *,
    status: str = "SUCCESS",
    rows: list[list[str]] | None = None,
    source_page: int = 7,
    drawing: str = "PFD-1",
    system_name: str = "SYS",
    note: str | None = None,
) -> dict:
    return {
        "format_version": "v2",
        "drawing_type": DRAWING_TYPE,
        "extraction_target": "top_equipment_header_basic",
        "source_pdf": "sample.pdf",
        "source_page": source_page,
        "drawing": drawing,
        "system_name": system_name,
        "status": status,
        "note": note
        if note is not None
        else (
            "Top-of-sheet equipment header present."
            if status == "SUCCESS"
            else "No separated top-of-sheet equipment header was identified."
        ),
        "columns": build_column_order("top_equipment_header_basic"),
        "rows": rows
        if rows is not None
        else [["T-100", "TEST TANK", system_name, drawing]],
    }


def write_stub(source_dir: Path, data: dict, *, page_num: int = 7, compact_sep: bool = False) -> Path:
    stub_path = resolve_stub_path(
        source_dir,
        str(data["drawing_type"]),
        str(data["extraction_target"]),
        PDF_STEM,
        page_num,
    )
    stub_path.parent.mkdir(parents=True, exist_ok=True)
    rendered = render_stub(page_num, data)
    if compact_sep:
        rendered = rendered.replace(
            "| --- | --- | --- | --- | --- | --- | --- | --- |",
            "|---|---|---|---|---|---|---|---|",
        )
        rendered = rendered.replace(
            "| --- | --- | --- | --- |",
            "|---|---|---|---|",
        )
    stub_path.write_text(rendered, encoding="utf-8")
    return stub_path


def run_cli(main_func, argv: list[str], monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(sys, "argv", ["prog", *argv])
    return main_func()


def test_parse_stub_text_accepts_compact_separator_same_as_spaced():
    data = make_detailed_data()
    spaced = render_stub(7, data)
    compact = spaced.replace(
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
        "|---|---|---|---|---|---|---|---|",
    )

    parsed_spaced = parse_stub_text(spaced, 7)
    parsed_compact = parse_stub_text(compact, 7)

    assert parsed_spaced["rows"] == parsed_compact["rows"]
    assert len(parsed_compact["rows"]) == 1


def test_parse_stub_text_skips_mismatched_column_count_rows():
    text = """---
drawing_type: PFD
extraction_target: top_equipment_header_basic
source_pdf: sample.pdf
source_page: 7
drawing: PFD-1
system_name: SYS
status: SUCCESS
---

# Page 7 — PFD top_equipment_header_basic

| equipment_number | equipment_name | system_name | drawing |
| --- | --- | --- | --- |
| T-100 | TEST TANK | SYS |

- note
- Extraction status: `SUCCESS`
"""
    parsed = parse_stub_text(text, 7)
    assert parsed["status"] == "SUCCESS"
    assert parsed["rows"] == []


def test_parse_stub_text_preserves_empty_table_status():
    data = make_detailed_data(status="NO_FINDINGS", rows=[[""] * 8])
    parsed = parse_stub_text(render_stub(7, data), 7)
    assert parsed["status"] == "NO_FINDINGS"
    assert parsed["rows"] == [[""] * 8]


def test_parse_stub_text_supports_inline_yaml_lists():
    parsed = parse_stub_text(render_stub(7, make_detailed_data()), 7)
    assert parsed["requested_known_fields"] == [
        "equipment_type",
        "equipment_description",
        "capacity_text",
        "power_text",
    ]


def test_parse_stub_text_supports_block_yaml_lists():
    text = """---
drawing_type: PFD
extraction_target: top_equipment_header_detailed
source_pdf: sample.pdf
source_page: 7
requested_known_fields:
  - equipment_type
  - power_text
requested_extra_fields:
  - name: vendor_text
    description: Vendor note
required_fields:
  - equipment_type
drawing: PFD-1
system_name: SYS
status: SUCCESS
---

# Page 7 — PFD top_equipment_header_detailed

| equipment_number | equipment_name | system_name | drawing | equipment_type | power_text | vendor_text |
| --- | --- | --- | --- | --- | --- | --- |
| T-100 | TEST TANK | SYS | PFD-1 | VESSEL | 5 kW | ACME |

- note
- Extraction status: `SUCCESS`
"""
    parsed = parse_stub_text(text, 7)
    assert parsed["requested_known_fields"] == ["equipment_type", "power_text"]
    assert parsed["requested_extra_fields"] == [
        {"name": "vendor_text", "description": "Vendor note"}
    ]
    assert parsed["required_fields"] == ["equipment_type"]


def test_parse_stub_text_supports_quoted_yaml_values():
    text = """---
drawing_type: PFD
extraction_target: top_equipment_header_basic
source_pdf: "sample file.pdf"
source_page: 7
drawing: "PFD:1"
system_name: "SYS #1"
status: SUCCESS
---

# Page 7 — PFD top_equipment_header_basic

| equipment_number | equipment_name | system_name | drawing |
| --- | --- | --- | --- |
| T-100 | TEST TANK | SYS #1 | PFD:1 |

- note
- Extraction status: `SUCCESS`
"""
    parsed = parse_stub_text(text, 7)
    assert parsed["source_pdf"] == "sample file.pdf"
    assert parsed["drawing"] == "PFD:1"
    assert parsed["system_name"] == "SYS #1"


def test_parse_stub_and_render_round_trip_is_parse_equivalent(tmp_path: Path):
    source_dir = tmp_path / "_Sources"
    source_dir.mkdir()
    original = make_detailed_data()
    stub_path = write_stub(source_dir, original)

    parsed = parse_stub(stub_path, 7)
    rendered = render_stub(7, parsed)
    reparsed = parse_stub_text(rendered, 7)

    assert reparsed["columns"] == parsed["columns"]
    assert reparsed["rows"] == parsed["rows"]
    assert rendered == stub_path.read_text(encoding="utf-8")


def test_compact_separator_round_trip_remains_lossless(tmp_path: Path):
    source_dir = tmp_path / "_Sources"
    source_dir.mkdir()
    original = make_detailed_data()
    stub_path = write_stub(source_dir, original, compact_sep=True)

    parsed = parse_stub(stub_path, 7)
    rendered = render_stub(7, parsed)
    reparsed = parse_stub_text(rendered, 7)

    assert len(parsed["rows"]) == 1
    assert reparsed["rows"] == parsed["rows"]


def test_sanitizer_guard_preserves_success_stub_when_parser_reads_zero_rows(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
):
    source_dir = tmp_path / "_Sources"
    source_dir.mkdir()
    stub_path = write_stub(source_dir, make_detailed_data())
    original = stub_path.read_text(encoding="utf-8")
    malformed = original.replace(
        "| equipment_number | equipment_name | system_name | drawing | equipment_type | equipment_description | capacity_text | power_text |",
        "| equipment_number | equipment_name | system_name | drawing | equipment_type | equipment_description | capacity_text |",
    )
    stub_path.write_text(malformed, encoding="utf-8")

    exit_code = run_cli(
        sanitize_mod.main,
        [
            "--source-dir",
            str(source_dir),
            "--drawing-type",
            DRAWING_TYPE,
            "--extraction-target",
            "top_equipment_header_detailed",
            "--pdf-stem",
            PDF_STEM,
            "--start-page",
            "7",
            "--end-page",
            "7",
        ],
        monkeypatch,
    )

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "guard_violations=7" in captured.out
    # The stub has finding_count=1 but parses to 0 meaningful rows, so
    # the partial-loss guard fires (finding_count mismatch). Either guard
    # message confirms the stub was NOT overwritten.
    assert "Stub NOT overwritten" in captured.err
    assert stub_path.read_text(encoding="utf-8") == malformed


def test_sanitizer_allows_legitimate_success_to_no_findings(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    source_dir = tmp_path / "_Sources"
    source_dir.mkdir()
    write_stub(
        source_dir,
        make_basic_data(rows=[["PSV-100", "PRESSURE SAFETY VALVE", "SYS", "PFD-1"]]),
    )

    exit_code = run_cli(
        sanitize_mod.main,
        [
            "--source-dir",
            str(source_dir),
            "--drawing-type",
            DRAWING_TYPE,
            "--extraction-target",
            "top_equipment_header_basic",
            "--pdf-stem",
            PDF_STEM,
            "--start-page",
            "7",
            "--end-page",
            "7",
        ],
        monkeypatch,
    )

    parsed = parse_stub(
        resolve_stub_path(source_dir, DRAWING_TYPE, "top_equipment_header_basic", PDF_STEM, 7),
        7,
    )
    assert exit_code == 0
    assert parsed["status"] == "NO_FINDINGS"
    assert parsed["system_name"] == "SYS"


def test_sanitizer_no_findings_stub_passes_through_unchanged(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
):
    source_dir = tmp_path / "_Sources"
    source_dir.mkdir()
    stub_path = write_stub(
        source_dir,
        make_basic_data(status="NO_FINDINGS", rows=[["", "", "SYS", ""]]),
    )
    original = stub_path.read_text(encoding="utf-8")

    exit_code = run_cli(
        sanitize_mod.main,
        [
            "--source-dir",
            str(source_dir),
            "--drawing-type",
            DRAWING_TYPE,
            "--extraction-target",
            "top_equipment_header_basic",
            "--pdf-stem",
            PDF_STEM,
            "--start-page",
            "7",
            "--end-page",
            "7",
        ],
        monkeypatch,
    )

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "updated=0" in captured.out
    assert stub_path.read_text(encoding="utf-8") == original


def test_report_stub_counts_no_round_trip_loss_for_canonical_and_compact(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    source_dir = tmp_path / "_Sources"
    source_dir.mkdir()
    write_stub(source_dir, make_basic_data(), page_num=7)
    write_stub(source_dir, make_basic_data(source_page=8), page_num=8, compact_sep=True)
    output_csv = tmp_path / "report.csv"

    exit_code = run_cli(
        report_mod.main,
        [
            "--source-dir",
            str(source_dir),
            "--drawing-type",
            DRAWING_TYPE,
            "--extraction-target",
            "top_equipment_header_basic",
            "--pdf-stem",
            PDF_STEM,
            "--start-page",
            "7",
            "--end-page",
            "8",
            "--output-csv",
            str(output_csv),
        ],
        monkeypatch,
    )

    with output_csv.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    assert exit_code == 0
    assert [row["round_trip_row_loss"] for row in rows] == ["", ""]


def test_report_stub_counts_surfaces_round_trip_row_loss_via_monkeypatch(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    source_dir = tmp_path / "_Sources"
    source_dir.mkdir()
    write_stub(source_dir, make_basic_data(), page_num=7)
    output_csv = tmp_path / "report.csv"

    original_parse_stub_text = report_mod.parse_stub_text

    def lossy_parse_stub_text(text: str, page_num: int):
        parsed = original_parse_stub_text(text, page_num)
        parsed = copy.deepcopy(parsed)
        parsed["rows"] = []
        return parsed

    monkeypatch.setattr(report_mod, "parse_stub_text", lossy_parse_stub_text)

    exit_code = run_cli(
        report_mod.main,
        [
            "--source-dir",
            str(source_dir),
            "--drawing-type",
            DRAWING_TYPE,
            "--extraction-target",
            "top_equipment_header_basic",
            "--pdf-stem",
            PDF_STEM,
            "--start-page",
            "7",
            "--end-page",
            "7",
            "--output-csv",
            str(output_csv),
        ],
        monkeypatch,
    )

    with output_csv.open(encoding="utf-8", newline="") as handle:
        row = next(csv.DictReader(handle))

    assert exit_code == 0
    assert row["round_trip_row_loss"] == "1 -> 0"


def test_validate_stub_format_passes_for_success_stub_with_rows(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    source_dir = tmp_path / "_Sources"
    source_dir.mkdir()
    write_stub(source_dir, make_basic_data(), page_num=7)

    exit_code = run_cli(
        validate_mod.main,
        [
            "--source-dir",
            str(source_dir),
            "--drawing-type",
            DRAWING_TYPE,
            "--extraction-target",
            "top_equipment_header_basic",
            "--pdf-stem",
            PDF_STEM,
            "--start-page",
            "7",
            "--end-page",
            "7",
        ],
        monkeypatch,
    )

    assert exit_code == 0


def test_validate_stub_format_fails_for_success_stub_with_zero_rows(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    source_dir = tmp_path / "_Sources"
    source_dir.mkdir()
    stub_path = write_stub(source_dir, make_basic_data(), page_num=7)
    malformed = stub_path.read_text(encoding="utf-8").replace(
        "| equipment_number | equipment_name | system_name | drawing |",
        "| equipment_number | equipment_name | system_name |",
    )
    stub_path.write_text(malformed, encoding="utf-8")

    exit_code = run_cli(
        validate_mod.main,
        [
            "--source-dir",
            str(source_dir),
            "--drawing-type",
            DRAWING_TYPE,
            "--extraction-target",
            "top_equipment_header_basic",
            "--pdf-stem",
            PDF_STEM,
            "--start-page",
            "7",
            "--end-page",
            "7",
        ],
        monkeypatch,
    )

    assert exit_code == 1


# ---------------------------------------------------------------------------
# Regression: West Doe equipment names that were falsely dropped
# ---------------------------------------------------------------------------

WEST_DOE_REGRESSION_NAMES = [
    # (equipment_number, equipment_name) — all must survive sanitization
    ("V-2174-2", "PACKING VENT/DRAIN SEPARATION POT"),
    ("V-5110-2", "HEAT MEDIUM EXPANSION TANK"),
    ("MX-6727-2/6728-2", "CONDENSATE WATER WASH MIXERS"),
    ("AC-6821-2/6826-2", "CONDENSATE DEHYDRATOR OVERHEAD CONDENSER"),
    ("V-9350-2/9360-1", "HYDROGEN PEROXIDE REACTORS"),
    ("V-6830-2", "CONDENSATE DEHYDRATOR REFLUX ACCUMULATOR"),
    ("T-6800-2", "CONDENSATE DEHYDRATOR"),
    ("V-4210-1", "AIR RECEIVER (WET)"),
    ("V-4240-1", "AIR RECEIVER (DRY)"),
    ("F-4220/4230-1", "INSTRUMENT AIR DRYER"),
    ("E-7240-1", "STABILIZER FEED/BOT EXCH."),
    ("V-6160-1", "MERCURY REMOVAL UNIT"),
    ("V-9360-1/9370-1/9380-1", "LPG PRODUCT STORAGE"),
    ("E-5370-1/5375-1", "LEAN/RICH AMINE EXCHANGERS"),
    ("T-5350-1", "AMINE REGENERATOR"),
    ("V-5345-1", "AMINE REFLUX ACCUMULATOR"),
    ("T-6260-1", "DEETHANIZER"),
    ("T-6500-1", "DEBUTANIZER"),
    ("V-6530-1", "DEBUTANIZER REFLUX ACCUMULATOR"),
    ("F-5910-1/5920-1", "MOLE SIEVE INLET FILTER/COALESCER"),
]


def test_sanitizer_preserves_west_doe_equipment_names():
    """Regression: every name that was falsely dropped by the removed allowlist
    must survive the current sanitizer."""
    rows = [
        [tag, name, "SYS", "PFD-1", "", "", "", ""]
        for tag, name in WEST_DOE_REGRESSION_NAMES
    ]
    kept, actions = sanitize_mod.sanitize_rows(rows)
    kept_tags = {row[0] for row in kept}
    dropped_tags = {
        a["equipment_number"]
        for a in actions
        if a["action"] == "dropped"
    }
    assert dropped_tags == set(), (
        f"Regression: these tags were falsely dropped: {dropped_tags}"
    )
    assert len(kept) == len(WEST_DOE_REGRESSION_NAMES)


# ---------------------------------------------------------------------------
# finding_count: partial row loss detection
# ---------------------------------------------------------------------------


def test_finding_count_persists_through_render_parse_round_trip():
    """finding_count is written to frontmatter and read back."""
    data = make_detailed_data(
        rows=[["V-1-1", "VESSEL", "SYS", "PFD-1", "VESSEL", "", "", ""]],
    )
    rendered = render_stub(7, data)
    reparsed = parse_stub_text(rendered, 7)
    assert reparsed["finding_count"] == 1


def test_missing_finding_count_parses_as_none():
    """Stubs without finding_count parse with finding_count=None, which the
    sanitizer and validator treat as untrusted for SUCCESS stubs."""
    text = """---
drawing_type: PFD
extraction_target: top_equipment_header_basic
source_pdf: test.pdf
source_page: 7
drawing: PFD-1
system_name: SYS
status: SUCCESS
---

# Page 7 — PFD top_equipment_header_basic

| equipment_number | equipment_name | system_name | drawing |
| --- | --- | --- | --- |
| V-1-1 | VESSEL | SYS | PFD-1 |

-
- Extraction status: `SUCCESS`
"""
    parsed = parse_stub_text(text, 7)
    assert parsed["finding_count"] is None


def test_validator_fails_success_stub_without_finding_count(tmp_path, monkeypatch):
    """SUCCESS stubs must carry finding_count; missing it is a validation failure."""
    source_dir = tmp_path / "_Sources"
    source_dir.mkdir()
    data = make_detailed_data(
        rows=[["V-1-1", "VESSEL", "SYS", "PFD-1", "VESSEL", "", "", ""]],
    )
    stub_path = write_stub(source_dir, data, page_num=7)
    # Strip finding_count from frontmatter
    text = stub_path.read_text()
    lines = [l for l in text.splitlines() if not l.startswith("finding_count:")]
    stub_path.write_text("\n".join(lines))

    exit_code = run_cli(
        validate_mod.main,
        [
            "--source-dir", str(source_dir),
            "--drawing-type", DRAWING_TYPE,
            "--extraction-target", "top_equipment_header_detailed",
            "--pdf-stem", PDF_STEM,
            "--start-page", "7",
            "--end-page", "7",
        ],
        monkeypatch,
    )
    assert exit_code == 1


def test_validator_catches_partial_row_loss(tmp_path, monkeypatch):
    """Validator fails when finding_count > parsed meaningful rows."""
    source_dir = tmp_path / "_Sources"
    source_dir.mkdir()
    data = make_detailed_data(
        rows=[["V-1-1", "VESSEL", "SYS", "PFD-1", "VESSEL", "", "", ""]],
    )
    stub_path = write_stub(source_dir, data, page_num=7)
    # Overwrite finding_count to 3 (simulating page worker claimed 3 but only 1 survived)
    text = stub_path.read_text()
    stub_path.write_text(text.replace("finding_count: 1", "finding_count: 3"))

    exit_code = run_cli(
        validate_mod.main,
        [
            "--source-dir", str(source_dir),
            "--drawing-type", DRAWING_TYPE,
            "--extraction-target", "top_equipment_header_detailed",
            "--pdf-stem", PDF_STEM,
            "--start-page", "7",
            "--end-page", "7",
        ],
        monkeypatch,
    )
    assert exit_code == 1


def test_validator_passes_when_finding_count_matches(tmp_path, monkeypatch):
    """Validator passes when finding_count matches parsed rows."""
    source_dir = tmp_path / "_Sources"
    source_dir.mkdir()
    data = make_detailed_data(
        rows=[
            ["V-1-1", "VESSEL", "SYS", "PFD-1", "VESSEL", "", "", ""],
            ["P-2-1", "PUMP", "SYS", "PFD-1", "PUMP", "", "", ""],
        ],
    )
    write_stub(source_dir, data, page_num=7)

    exit_code = run_cli(
        validate_mod.main,
        [
            "--source-dir", str(source_dir),
            "--drawing-type", DRAWING_TYPE,
            "--extraction-target", "top_equipment_header_detailed",
            "--pdf-stem", PDF_STEM,
            "--start-page", "7",
            "--end-page", "7",
        ],
        monkeypatch,
    )
    assert exit_code == 0
