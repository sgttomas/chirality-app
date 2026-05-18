from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path


VALIDATION_DIR = Path(__file__).resolve().parent
if str(VALIDATION_DIR) not in sys.path:
    sys.path.insert(0, str(VALIDATION_DIR))

from validate_domain_decomposition_integrity import (  # noqa: E402
    REQUIRED_SNAPSHOT_ARTIFACTS,
    load_required,
    resolve_required_paths,
    validate_coverage,
    validate_domain_rows,
    validate_required_files,
    validate_snapshot,
)


TOOL = VALIDATION_DIR / "validate_domain_decomposition_integrity.py"


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = list(rows[0].keys()) if rows else []
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_valid_decomposition(root: Path) -> None:
    write_csv(root / "annex_categories.csv", [{"CategoryID": "CAT-001", "CategoryName": "Process"}])
    write_csv(root / "annex_knowledge_types.csv", [{
        "KnowledgeTypeID": "KTY-01",
        "ParentCategoryID": "CAT-001",
        "Name": "Example KTY",
        "SupportsObjectives": "OBJ-001",
    }])
    write_csv(root / "annex_knowledge_subjects.csv", [{
        "SubjectID": "SUB-01",
        "ParentKnowledgeTypeID": "KTY-01",
        "CategoryID": "CAT-001",
        "UnitStatus": "IN",
    }])
    write_csv(root / "annex_domain_ledger.csv", [{
        "UnitID": "HBK-0001",
        "InOutStatus": "IN",
        "CategoryID": "CAT-001",
        "KnowledgeTypeID(s)": "KTY-01",
        "SubjectID(s)": "SUB-01",
        "ObjectiveID(s)": "OBJ-001",
    }])
    write_csv(root / "annex_objectives.csv", [{
        "ObjectiveID": "OBJ-001",
        "MappedKnowledgeTypes": "KTY-01",
    }])
    write_csv(root / "annex_coverage_telemetry.csv", [
        {"Metric": "UnitCount", "Value": "1"},
        {"Metric": "INUnitCount", "Value": "1"},
        {"Metric": "TBDUnitCount", "Value": "0"},
        {"Metric": "OUTUnitCount", "Value": "0"},
        {"Metric": "CategoryCount", "Value": "1"},
        {"Metric": "KnowledgeTypeCount", "Value": "1 active / 1 total"},
        {"Metric": "SubjectCount", "Value": "1"},
        {"Metric": "ObjectiveCount", "Value": "1"},
        {"Metric": "UnassignedINUnits", "Value": "0"},
        {"Metric": "UnitsWithoutKnowledgeTypeMapping", "Value": "0"},
        {"Metric": "UnmappedObjectives", "Value": "0"},
    ])


def write_snapshot(snapshot: Path, supersession_binding_present: str) -> None:
    snapshot.mkdir(parents=True, exist_ok=True)
    for name in REQUIRED_SNAPSHOT_ARTIFACTS:
        if name == "Amendment_Actions.csv":
            continue
        (snapshot / name).write_text("ok\n", encoding="utf-8")
    write_csv(snapshot / "Amendment_Actions.csv", [{
        "AmendmentID": "SCA-001",
        "ActionSeq": "1",
        "ActionType": "MODIFY",
        "EntityType": "KNOWLEDGE_TYPE",
        "EntityID": "KTY-01",
        "SupersessionBindingPresent": supersession_binding_present,
    }])
    (snapshot.parent / "_LATEST.md").write_text(snapshot.name + "\n", encoding="utf-8")


def test_valid_domain_decomposition_has_no_findings(tmp_path: Path) -> None:
    root = tmp_path / "_Decomposition"
    write_valid_decomposition(root)

    paths, rows = load_required(root)
    findings = validate_domain_rows(paths, rows) + validate_coverage(paths, rows)

    assert findings == []


def test_legacy_domain_register_names_are_resolved(tmp_path: Path) -> None:
    root = tmp_path / "_Decomposition"
    write_csv(root / "DeepCut_Category_Register_v4.csv", [{"CategoryID": "CAT-001"}])
    write_csv(root / "DeepCut_Knowledge_Type_Register_v4.csv", [{
        "KnowledgeTypeID": "KTY-01",
        "ParentCategoryID": "CAT-001",
        "InOutStatus": "IN",
        "SupportsObjectives": "OBJ-001",
    }])
    write_csv(root / "DeepCut_Knowledge_Subject_Register_v4.csv", [{
        "SubjectID": "SUB-01",
        "ParentKnowledgeTypeID": "KTY-01",
        "InOutStatus": "IN",
    }])
    write_csv(root / "DeepCut_Domain_Ledger_v4.csv", [{
        "UnitID": "HBK-0001",
        "InOutStatus": "IN",
        "CategoryID": "CAT-001",
        "KnowledgeTypeID": "KTY-01",
        "SubjectID": "SUB-01",
        "ObjectiveIDs": "OBJ-001",
    }])
    write_csv(root / "DeepCut_Objective_Register_v4.csv", [{
        "ObjectiveID": "OBJ-001",
        "MappedKnowledgeTypes": "KTY-01",
    }])
    (root / "DeepCut_Coverage_Telemetry_v4.json").write_text(
        json.dumps({
            "UnitCount": 1,
            "INUnitCount": 1,
            "TBDUnitCount": 0,
            "OUTUnitCount": 0,
            "CategoryCount": 1,
            "KnowledgeTypeCount": 1,
            "SubjectCount": 1,
            "ObjectiveCount": 1,
            "UnassignedINUnits": 0,
            "UnitsWithoutKnowledgeTypeMapping": 0,
            "UnmappedObjectives": 0,
        }),
        encoding="utf-8",
    )

    paths, rows = load_required(root)
    findings = validate_domain_rows(paths, rows) + validate_coverage(paths, rows)

    assert paths["coverage"].suffix == ".json"
    assert findings == []


def test_active_kty_without_active_subject_is_blocking(tmp_path: Path) -> None:
    root = tmp_path / "_Decomposition"
    write_valid_decomposition(root)
    write_csv(
        root / "annex_knowledge_subjects.csv",
        [],
        ["SubjectID", "ParentKnowledgeTypeID", "CategoryID", "UnitStatus"],
    )

    paths, rows = load_required(root)
    findings = validate_domain_rows(paths, rows)

    assert any(f.category == "ACTIVE_KTY_WITHOUT_ACTIVE_SUBJECT" for f in findings)


def test_supersession_delta_required_only_when_action_declares_binding(tmp_path: Path) -> None:
    no_binding = tmp_path / "_ScopeChange" / "SCA-001_2026-04-21_1200"
    with_binding = tmp_path / "_ScopeChange" / "SCA-002_2026-04-21_1300"
    write_snapshot(no_binding, "NO")
    write_snapshot(with_binding, "YES")

    no_binding_findings = validate_snapshot(no_binding)
    with_binding_findings = validate_snapshot(with_binding)

    assert not any(f.category == "SUPERSESSION_DELTA_MISSING" for f in no_binding_findings)
    assert any(f.category == "SUPERSESSION_DELTA_MISSING" for f in with_binding_findings)


# ---------------------------------------------------------------------------
# Transitional dual-layout tests: --package-subfolder + auto-descent.
# ---------------------------------------------------------------------------


def test_annexes_at_root_resolve_directly(tmp_path: Path) -> None:
    """Regression: canonical layout (annexes at root) still resolves at root."""
    root = tmp_path / "_Decomposition"
    write_valid_decomposition(root)

    paths = resolve_required_paths(root)

    for name in ("ledger", "categories", "ktys", "subjects", "objectives", "coverage"):
        assert paths[name].parent == root, f"{name} should resolve from root"
        assert paths[name].exists(), f"{name} should exist at root"
    assert validate_required_files(paths) == []


def test_annexes_in_single_subfolder_auto_descend(tmp_path: Path) -> None:
    """A single non-hidden, non-_Archive subfolder containing annexes is auto-descended."""
    root = tmp_path / "_Decomposition"
    package = root / "PKG_v1"
    write_valid_decomposition(package)

    paths = resolve_required_paths(root)

    for name in ("ledger", "categories", "ktys", "subjects", "objectives", "coverage"):
        assert paths[name].parent == package, f"{name} should resolve from package subfolder"
        assert paths[name].exists()
    assert validate_required_files(paths) == []


def test_archive_sibling_excluded_from_descent_candidates(tmp_path: Path) -> None:
    """`_Archive/` is excluded from candidate set; descent still picks the only payload subfolder."""
    root = tmp_path / "_Decomposition"
    package = root / "PKG_v1"
    write_valid_decomposition(package)
    (root / "_Archive").mkdir()
    # Even seeding a stale annex inside _Archive must not cause ambiguity.
    write_csv(root / "_Archive" / "annex_categories.csv", [{"CategoryID": "STALE-001"}])

    paths = resolve_required_paths(root)

    for name in ("ledger", "categories", "ktys", "subjects", "objectives", "coverage"):
        assert paths[name].parent == package
    assert validate_required_files(paths) == []


def test_ambiguous_subfolders_require_explicit_flag(tmp_path: Path) -> None:
    """When two subfolders both contain candidates, auto-descent declines to guess."""
    root = tmp_path / "_Decomposition"
    pkg_a = root / "PKG_A"
    pkg_b = root / "PKG_B"
    write_valid_decomposition(pkg_a)
    write_valid_decomposition(pkg_b)

    # Auto-descent should fall through; canonical paths surface MISSING_REQUIRED_FILE.
    paths = resolve_required_paths(root)
    findings = validate_required_files(paths)
    missing = [f for f in findings if f.category == "MISSING_REQUIRED_FILE"]
    assert len(missing) == 6, "All 6 annexes should be flagged missing under ambiguity"

    # Explicit --package-subfolder resolves cleanly.
    paths_a = resolve_required_paths(root, package_subfolder="PKG_A")
    assert validate_required_files(paths_a) == []
    for name in ("ledger", "categories", "ktys", "subjects", "objectives", "coverage"):
        assert paths_a[name].parent == pkg_a


def test_package_subfolder_pointing_at_nonexistent_dir_fails(tmp_path: Path) -> None:
    """CLI: nonexistent --package-subfolder yields exit code 1 with clear error."""
    root = tmp_path / "_Decomposition"
    write_valid_decomposition(root)

    result = subprocess.run(
        [
            sys.executable,
            str(TOOL),
            "--decomposition-root",
            str(root),
            "--package-subfolder",
            "DOES_NOT_EXIST",
            "--output-report",
            str(tmp_path / "report.md"),
            "--output-findings",
            str(tmp_path / "findings.csv"),
        ],
        check=False,
        text=True,
        capture_output=True,
    )

    assert result.returncode == 1, result.stdout + result.stderr
    assert "DOES_NOT_EXIST" in result.stderr


def test_cli_emits_info_log_on_auto_descent(tmp_path: Path) -> None:
    """Auto-descent must emit a stderr `[INFO] Resolved annexes from package subfolder: <name>` line."""
    root = tmp_path / "_Decomposition"
    package = root / "MyPackage_v1"
    write_valid_decomposition(package)

    result = subprocess.run(
        [
            sys.executable,
            str(TOOL),
            "--decomposition-root",
            str(root),
            "--output-report",
            str(tmp_path / "report.md"),
            "--output-findings",
            str(tmp_path / "findings.csv"),
        ],
        check=False,
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "[INFO] Resolved annexes from package subfolder: MyPackage_v1" in result.stderr


def test_cli_explicit_flag_matches_auto_descent_outputs(tmp_path: Path) -> None:
    """Auto-descent and explicit --package-subfolder produce identical outputs."""
    root = tmp_path / "_Decomposition"
    package = root / "MyPackage_v1"
    write_valid_decomposition(package)

    auto_findings = tmp_path / "auto_findings.csv"
    auto_report = tmp_path / "auto_report.md"
    explicit_findings = tmp_path / "explicit_findings.csv"
    explicit_report = tmp_path / "explicit_report.md"

    common_args = [
        sys.executable,
        str(TOOL),
        "--decomposition-root",
        str(root),
    ]

    auto = subprocess.run(
        common_args + [
            "--output-report", str(auto_report),
            "--output-findings", str(auto_findings),
        ],
        check=False, text=True, capture_output=True,
    )
    explicit = subprocess.run(
        common_args + [
            "--package-subfolder", "MyPackage_v1",
            "--output-report", str(explicit_report),
            "--output-findings", str(explicit_findings),
        ],
        check=False, text=True, capture_output=True,
    )

    assert auto.returncode == 0, auto.stderr
    assert explicit.returncode == 0, explicit.stderr
    assert auto_report.read_text() == explicit_report.read_text()
    assert auto_findings.read_text() == explicit_findings.read_text()
