import csv
import importlib.util
import json
import sys
from pathlib import Path

import pytest


MODULE_PATH = Path(__file__).with_name("analyze_agentic_runtime.py")
SPEC = importlib.util.spec_from_file_location("analyze_agentic_runtime", MODULE_PATH)
assert SPEC and SPEC.loader
runtime = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = runtime
SPEC.loader.exec_module(runtime)


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value) + "\n", encoding="utf-8")


def write_catalog(path: Path, evidence_path: str, needle: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=runtime.EVENT_COLUMNS)
        writer.writeheader()
        writer.writerow(
            {
                "event_id": "EV-001",
                "wave": "A1",
                "package": "APP-PKG-01",
                "deliverable": "DEL-01-01",
                "stage": "author",
                "category": "BRIEF_OR_INPUT",
                "subtype": "missing_input",
                "scope_kind": "child",
                "affected_units": "1",
                "substantive_impact": "NONE",
                "detected_by": "tool_guard",
                "outcome": "failed_closed_then_passed",
                "evidence_path": evidence_path,
                "evidence_needle": needle,
            }
        )


def synthetic_corpus(tmp_path: Path) -> tuple[Path, Path, Path, Path]:
    repo = tmp_path / "repo"
    run = repo / "execution" / "_Coordination" / "AgentRuns" / "RUN"
    package = run / "instances" / "WORKING-A1-PKG01"
    write_json(
        package / "STATUS.json",
        {
            "package": "APP-PKG-01",
            "status": "PASS",
            "terminal": True,
            "members": 1,
            "mapping_rows": 3,
            "source_lines": 10,
            "replacement_rows": 5,
            "rollback_rows": 5,
            "project_writes": 0,
        },
    )
    for child in ("AUTHOR-DEL-01-01", "VERIFY-DEL-01-01", "VERIFY-DEL-01-01-R1"):
        child_root = package / "children" / child
        child_root.mkdir(parents=True)
        (child_root / "LAUNCH_BRIEF.md").write_text("brief\n", encoding="utf-8")
    write_json(
        package / "children" / "AUTHOR-DEL-01-01" / "STATUS.json",
        {"status": "SUCCESS", "terminal": True, "verdict": "PASS"},
    )
    write_json(
        package / "children" / "VERIFY-DEL-01-01" / "STATUS.json",
        {"status": "SUCCESS_MANAGER_EVIDENCE_CLOSEOUT", "terminal": True, "verdict": "PASS"},
    )
    write_json(
        package / "PROJECT_CHECKS.json",
        {
            "results": [
                {"id": "test", "status": "PASS", "exit_code": 0, "duration_seconds": 2.0},
                {"id": "premerge", "status": "FAIL", "exit_code": 1, "duration_seconds": 0.5},
            ]
        },
    )
    evidence = package / "CHECKS.md"
    evidence.write_text("The input was missing and failed closed.\n", encoding="utf-8")
    catalog = repo / "catalog.csv"
    write_catalog(catalog, evidence.relative_to(repo).as_posix(), "input was missing")
    output = repo / "analysis"
    return repo, run, catalog, output


def test_analyze_synthetic_corpus(tmp_path: Path) -> None:
    repo, run, catalog, output = synthetic_corpus(tmp_path)
    summary = runtime.analyze(repo, run, catalog, output, include_git_runtime=False)
    assert summary["inventory"]["members"] == 1
    assert summary["children"]["baseline_child_roles"] == 2
    assert summary["children"]["documented_attempts"] == 3
    assert summary["children"]["extra_documented_attempts"] == 1
    assert summary["children"]["manager_evidence_closeouts"] == 1
    assert summary["project_checks"]["invocations"] == 2
    assert summary["project_checks"]["failures"] == 1
    assert summary["events"]["episodes"] == 1
    assert (output / "summary.json").is_file()
    assert (output / "events.csv").is_file()
    assert (output / "report.md").is_file()
    assert (output / "MANIFEST.tsv").is_file()


def test_rejects_unbound_event_needle(tmp_path: Path) -> None:
    repo, run, catalog, output = synthetic_corpus(tmp_path)
    rows = list(csv.DictReader(catalog.open(encoding="utf-8")))
    rows[0]["evidence_needle"] = "not present"
    with catalog.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=runtime.EVENT_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
    with pytest.raises(runtime.AnalysisError, match="needle absent"):
        runtime.analyze(repo, run, catalog, output, include_git_runtime=False)


def test_wilson_zero_failures_has_nonzero_upper_bound() -> None:
    interval = runtime.wilson_interval(0, 47)
    assert interval["low"] == 0.0
    assert 0.07 < interval["high"] < 0.08
