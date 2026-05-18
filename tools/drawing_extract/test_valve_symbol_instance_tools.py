from __future__ import annotations

import csv
import sys
from pathlib import Path

import pytest


DRAWING_EXTRACT_DIR = Path(__file__).resolve().parent
if str(DRAWING_EXTRACT_DIR) not in sys.path:
    sys.path.insert(0, str(DRAWING_EXTRACT_DIR))

import aggregate_valve_counts as aggregate_mod  # noqa: E402
import assign_valve_symbol_geometry_duplicates as geometry_mod  # noqa: E402
import assemble_valve_candidates_csv as assemble_mod  # noqa: E402
import flag_duplicate_valve_candidates as duplicate_mod  # noqa: E402
import validate_valve_tile_stub_format as validate_cli_mod  # noqa: E402
from valve_stub_layout import ValveStub, candidate_id, parse, render, validate  # noqa: E402


def run_cli(main_func, argv: list[str], monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(sys, "argv", ["prog", *argv])
    return main_func()


def candidate_row(**overrides: str) -> dict[str, str]:
    row = {
        "candidate_id": "",
        "source_page": "1",
        "dwg_no": "PID-1",
        "system_name": "SYS",
        "source_raster_path": "/tmp/page_0001.png",
        "tile_id": "page_0001_r01_c01",
        "tile_image_path": "/tmp/tile.png",
        "symbol_crop_path": "/tmp/crop.png",
        "context_crop_path": "/tmp/context.png",
        "center_x_px": "100",
        "center_y_px": "100",
        "bbox_x0_px": "90",
        "bbox_y0_px": "90",
        "bbox_x1_px": "110",
        "bbox_y1_px": "110",
        "symbol_class": "manual_block",
        "symbol_confidence": "medium",
        "count_include": "true",
        "review_status": "manual_review",
        "review_reason": "visible_valve_symbol",
        "visible_tag_text": "",
        "tag_status": "none",
        "tag_confidence": "TBD",
        "nearby_line_text": "",
        "valve_size_text": "",
        "valve_type_code": "",
        "valve_type_name": "",
        "actuation": "",
        "detail_confidence": "TBD",
        "issue_flags": "[]",
        "notes": "",
    }
    row.update(overrides)
    if not row["candidate_id"]:
        row["candidate_id"] = candidate_id(row["source_page"], row["center_x_px"], row["center_y_px"], row["symbol_class"])
    return row


def stub_with_rows(rows: list[dict[str, str]]) -> ValveStub:
    return ValveStub(
        source_pdf="sample.pdf",
        source_page=1,
        source_raster_path="/tmp/page_0001.png",
        extraction_target="valve_count_basic",
        mode="basic",
        tile_id="page_0001_r01_c01",
        tile_image_path="/tmp/tile.png",
        tile_grid="5x4",
        body_box_px=[0, 0, 1000, 1000],
        body_exclusions=["border", "titleblock"],
        read_box_px=[0, 0, 300, 300],
        emit_box_px=[0, 0, 200, 200],
        overlap_px=200,
        mini_grid="5x5",
        status="SUCCESS",
        finding_count=len(rows),
        rows=rows,
    )


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def test_symbol_instance_stub_round_trip_allows_tagless_visible_valve():
    model = stub_with_rows([candidate_row()])
    path_text = render(model)
    path = Path("/tmp/valve_symbol_instance_round_trip.md")
    path.write_text(path_text, encoding="utf-8")

    parsed = parse(path)
    errors, warnings = validate(parsed)

    assert errors == []
    assert warnings == []
    assert parsed.rows[0]["tag_status"] == "none"
    assert parsed.rows[0]["count_include"] == "true"


def test_validator_rejects_counted_non_valve_and_missing_pixel_location():
    bad = candidate_row(
        symbol_class="instrument_only",
        count_include="true",
        center_x_px="",
        candidate_id="bad",
    )
    errors, _warnings = validate(stub_with_rows([bad]))

    assert any("count_include=true requires a valve symbol_class" in error for error in errors)
    assert any("center_x_px must be a non-negative integer" in error for error in errors)


def test_validator_warns_tag_profile_without_changing_countability():
    row = candidate_row(visible_tag_text="27GA-A", tag_status="true_tag", tag_confidence="medium")
    errors, warnings = validate(stub_with_rows([row]))

    assert errors == []
    assert any("TAG_PROFILE_REVIEW" in warning for warning in warnings)
    assert row["count_include"] == "true"


def test_validate_and_assemble_symbol_instance_stub_round_trip(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    source_dir = tmp_path / "source"
    run_folder = source_dir / "P_AND_ID" / "valve_count_basic" / "RUN-TEST"
    run_folder.mkdir(parents=True)
    stub_path = run_folder / "sample_page_0001_tile_r01_c01_basic_stub.md"
    stub_path.write_text(render(stub_with_rows([candidate_row()])), encoding="utf-8")
    warnings_csv = tmp_path / "warnings.csv"
    output_csv = run_folder / "sample_candidates.csv"
    output_md = run_folder / "sample_candidates.md"

    assert run_cli(
        validate_cli_mod.main,
        [
            "--source-dir",
            str(source_dir),
            "--target",
            "valve_count_basic",
            "--mode",
            "basic",
            "--pdf-stem",
            "sample",
            "--start-page",
            "1",
            "--end-page",
            "1",
            "--run-folder",
            "RUN-TEST",
            "--warnings-csv",
            str(warnings_csv),
        ],
        monkeypatch,
    ) == 0
    assert run_cli(
        assemble_mod.main,
        [
            "--source-dir",
            str(source_dir),
            "--target",
            "valve_count_basic",
            "--mode",
            "basic",
            "--pdf-stem",
            "sample",
            "--start-page",
            "1",
            "--end-page",
            "1",
            "--output-csv",
            str(output_csv),
            "--output-md",
            str(output_md),
            "--run-folder",
            str(run_folder),
        ],
        monkeypatch,
    ) == 0

    assembled = read_csv(output_csv)
    assert assembled[0]["valve_schema_version"] == "symbol_instance_v1"
    assert assembled[0]["center_x_px"] == "100"


def test_duplicate_true_tag_review_ignores_repeated_line_spec_text(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    rows = [
        candidate_row(nearby_line_text="27GA-A", tag_status="line_spec_only", center_x_px="100", candidate_id="a"),
        candidate_row(nearby_line_text="27GA-A", tag_status="line_spec_only", center_x_px="200", candidate_id="b"),
        candidate_row(visible_tag_text="FCV-7211-1", tag_status="true_tag", center_x_px="300", candidate_id="c"),
        candidate_row(visible_tag_text="FCV-7211-1", tag_status="true_tag", center_x_px="400", candidate_id="d"),
    ]
    input_csv = tmp_path / "candidates.csv"
    output_csv = tmp_path / "duplicate_tags.csv"
    write_csv(input_csv, rows)

    assert run_cli(duplicate_mod.main, [str(input_csv), str(output_csv)], monkeypatch) == 0
    duplicates = read_csv(output_csv)

    assert len(duplicates) == 1
    assert duplicates[0]["visible_tag_text"] == "FCV-7211-1"


def test_geometry_duplicate_assignment_supersedes_adjacent_tile_observation(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    rows = [
        candidate_row(candidate_id="keep", center_x_px="100", center_y_px="100"),
        candidate_row(candidate_id="dupe", center_x_px="112", center_y_px="105", tile_id="page_0001_r01_c02"),
    ]
    input_csv = tmp_path / "candidates.csv"
    output_csv = tmp_path / "geometry_assigned.csv"
    duplicates_csv = tmp_path / "geometry_duplicates.csv"
    write_csv(input_csv, rows)

    assert run_cli(
        geometry_mod.main,
        [str(input_csv), str(output_csv), "--duplicates-csv", str(duplicates_csv)],
        monkeypatch,
    ) == 0

    assigned = read_csv(output_csv)
    duplicates = read_csv(duplicates_csv)
    assert assigned[1]["review_status"] == "superseded_duplicate"
    assert assigned[1]["count_include"] == "false"
    assert duplicates[0]["superseded_candidate_id"] == "dupe"


def test_aggregation_counts_only_count_include_true_and_reports_tag_quality(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    rows = [
        candidate_row(candidate_id="accepted", review_status="auto_accept", count_include="true", tag_status="none"),
        candidate_row(candidate_id="manual", center_x_px="140", review_status="manual_review", count_include="true", tag_status="line_spec_only", nearby_line_text="27GA-A"),
        candidate_row(candidate_id="rejected", center_x_px="180", review_status="human_reject", count_include="false", symbol_class="not_a_valve"),
        candidate_row(candidate_id="duplicate", center_x_px="220", review_status="superseded_duplicate", count_include="false"),
    ]
    input_csv = tmp_path / "candidates.csv"
    output_csv = tmp_path / "counts.csv"
    write_csv(input_csv, rows)

    assert run_cli(
        aggregate_mod.main,
        ["--candidates-csv", str(input_csv), "--output-csv", str(output_csv), "--start-page", "1", "--end-page", "1"],
        monkeypatch,
    ) == 0

    counts = read_csv(output_csv)
    assert counts[0]["accepted_count"] == "1"
    assert counts[0]["accepted_plus_manual_review_count"] == "2"
    assert counts[0]["human_reject_count"] == "1"
    assert counts[0]["superseded_duplicate_count"] == "1"
    assert counts[0]["line_spec_only_tag_count"] == "1"
