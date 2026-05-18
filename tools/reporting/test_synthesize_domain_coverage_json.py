from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path


TOOL = Path(__file__).resolve().parent / "synthesize_domain_coverage_json.py"


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def test_synthesizes_coverage_json_with_manifest_rollup(tmp_path: Path) -> None:
    decomposition = tmp_path / "_Decomposition"
    snapshot = tmp_path / "_ScopeChange" / "SCA-001_2026-04-21_1200"
    output = snapshot / "Post_Change_Coverage.json"

    write_csv(decomposition / "annex_coverage_telemetry.csv", [
        {"Metric": "UnitCount", "Value": "2"},
        {"Metric": "Revision", "Value": "SCA-001"},
        {"Metric": "OpenIssuesByType", "Value": "{\"TBD\": 1}"},
    ])
    write_csv(snapshot / "KTY_Remediation_Manifest.csv", [{
        "CONTENT_DISPOSITION_STATE": "VERIFIED",
        "FACTUAL_USE_GATE": "ALLOW_FACTUAL_USE",
    }])

    result = subprocess.run(
        [
            sys.executable,
            str(TOOL),
            "--decomposition-root",
            str(decomposition),
            "--scope-change-snapshot",
            str(snapshot),
            "--output-json",
            str(output),
        ],
        check=False,
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0, result.stderr
    data = json.loads(output.read_text(encoding="utf-8"))
    assert data["UnitCount"] == 2
    assert data["Revision"] == "SCA-001"
    assert data["OpenIssuesByType"] == {"TBD": 1}
    assert data["KTYRemediationManifestRows"] == 1
    assert data["ContentRemediationState"] == "COMPLETE"


def test_missing_manifest_state_is_explicit(tmp_path: Path) -> None:
    decomposition = tmp_path / "_Decomposition"
    output = tmp_path / "Pre_Change_Coverage.json"
    write_csv(decomposition / "annex_coverage_telemetry.csv", [{"Metric": "UnitCount", "Value": "1"}])

    result = subprocess.run(
        [
            sys.executable,
            str(TOOL),
            "--decomposition-root",
            str(decomposition),
            "--missing-manifest-state",
            "NOT_FORMALIZED",
            "--output-json",
            str(output),
        ],
        check=False,
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0, result.stderr
    data = json.loads(output.read_text(encoding="utf-8"))
    assert data["KTYRemediationManifestExists"] is False
    assert data["ContentRemediationState"] == "NOT_FORMALIZED"


def test_reads_legacy_coverage_telemetry_json(tmp_path: Path) -> None:
    decomposition = tmp_path / "_Decomposition"
    output = tmp_path / "coverage.json"
    decomposition.mkdir(parents=True)
    (decomposition / "DeepCut_Coverage_Telemetry_v4.json").write_text(
        json.dumps({"Revision": "v4", "UnitCount": 7}),
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            str(TOOL),
            "--decomposition-root",
            str(decomposition),
            "--output-json",
            str(output),
        ],
        check=False,
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0, result.stderr
    data = json.loads(output.read_text(encoding="utf-8"))
    assert data["Revision"] == "v4"
    assert data["UnitCount"] == 7


# ---------------------------------------------------------------------------
# Transitional dual-layout tests: --package-subfolder + auto-descent.
# ---------------------------------------------------------------------------


def test_auto_descend_into_single_subfolder(tmp_path: Path) -> None:
    """A single eligible subfolder containing coverage telemetry is auto-descended."""
    decomposition = tmp_path / "_Decomposition"
    package = decomposition / "PKG_v1"
    output = tmp_path / "coverage.json"
    write_csv(package / "annex_coverage_telemetry.csv", [
        {"Metric": "UnitCount", "Value": "3"},
    ])

    result = subprocess.run(
        [
            sys.executable,
            str(TOOL),
            "--decomposition-root",
            str(decomposition),
            "--output-json",
            str(output),
        ],
        check=False,
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0, result.stderr
    assert "[INFO] Resolved annexes from package subfolder: PKG_v1" in result.stderr
    data = json.loads(output.read_text(encoding="utf-8"))
    assert data["UnitCount"] == 3


def test_archive_sibling_excluded_from_descent(tmp_path: Path) -> None:
    """`_Archive/` is excluded from candidate set; descent still picks the only payload subfolder."""
    decomposition = tmp_path / "_Decomposition"
    package = decomposition / "PKG_v1"
    output = tmp_path / "coverage.json"
    write_csv(package / "annex_coverage_telemetry.csv", [
        {"Metric": "UnitCount", "Value": "5"},
    ])
    (decomposition / "_Archive").mkdir()
    write_csv(decomposition / "_Archive" / "Coverage_Telemetry_old.csv", [
        {"Metric": "UnitCount", "Value": "999"},
    ])

    result = subprocess.run(
        [
            sys.executable,
            str(TOOL),
            "--decomposition-root",
            str(decomposition),
            "--output-json",
            str(output),
        ],
        check=False,
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0, result.stderr
    data = json.loads(output.read_text(encoding="utf-8"))
    assert data["UnitCount"] == 5  # Confirms _Archive was not chosen.


def test_ambiguous_subfolders_require_explicit_flag(tmp_path: Path) -> None:
    """Two subfolders with candidates yield error without flag; explicit flag resolves."""
    decomposition = tmp_path / "_Decomposition"
    pkg_a = decomposition / "PKG_A"
    pkg_b = decomposition / "PKG_B"
    output = tmp_path / "coverage.json"
    write_csv(pkg_a / "annex_coverage_telemetry.csv", [{"Metric": "UnitCount", "Value": "10"}])
    write_csv(pkg_b / "annex_coverage_telemetry.csv", [{"Metric": "UnitCount", "Value": "20"}])

    # Without flag: ambiguous → falls through to canonical-path lookup → FileNotFoundError → exit 1.
    ambiguous = subprocess.run(
        [
            sys.executable,
            str(TOOL),
            "--decomposition-root",
            str(decomposition),
            "--output-json",
            str(output),
        ],
        check=False,
        text=True,
        capture_output=True,
    )
    assert ambiguous.returncode == 1
    assert "ERROR" in ambiguous.stderr

    # With flag: resolves to PKG_A.
    explicit = subprocess.run(
        [
            sys.executable,
            str(TOOL),
            "--decomposition-root",
            str(decomposition),
            "--package-subfolder",
            "PKG_A",
            "--output-json",
            str(output),
        ],
        check=False,
        text=True,
        capture_output=True,
    )
    assert explicit.returncode == 0, explicit.stderr
    assert "[INFO] Resolved annexes from package subfolder: PKG_A" in explicit.stderr
    data = json.loads(output.read_text(encoding="utf-8"))
    assert data["UnitCount"] == 10


def test_nonexistent_package_subfolder_fails(tmp_path: Path) -> None:
    """CLI: nonexistent --package-subfolder yields exit 1 with clear error."""
    decomposition = tmp_path / "_Decomposition"
    output = tmp_path / "coverage.json"
    write_csv(decomposition / "annex_coverage_telemetry.csv", [{"Metric": "UnitCount", "Value": "1"}])

    result = subprocess.run(
        [
            sys.executable,
            str(TOOL),
            "--decomposition-root",
            str(decomposition),
            "--package-subfolder",
            "DOES_NOT_EXIST",
            "--output-json",
            str(output),
        ],
        check=False,
        text=True,
        capture_output=True,
    )

    assert result.returncode == 1
    assert "DOES_NOT_EXIST" in result.stderr
