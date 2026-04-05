#!/usr/bin/env python3
"""
validate_build_hypergraph_fixture.py — Regression check for tools/aggregation/build_hypergraph.py.

Runs the hypergraph builder against two bundled fixtures and verifies:

1. Determinism: two runs on clean_minimal produce byte-identical nodes.csv,
   hyperedges.csv, incidence.csv; and identical hypergraph.json after
   stripping the non-deterministic `generated_at` timestamp.
2. Clean-run PASS coverage: the 8 non-ledger QA checks each emit a PASS row
   in QA_Report.md, and LEDGER_INTEGRITY does NOT appear (no ledger data).
3. Warning fixture: the missing-category fixture produces the expected
   warning codes AND still emits PASS rows for the unaffected checks.

Usage:
    python3 tools/validation/validate_build_hypergraph_fixture.py [--keep-tmp]

Exit codes:
    0 — all assertions passed
    1 — one or more assertions failed
    2 — setup error (fixtures missing, tool missing, etc.)
"""

import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import List, Set

REPO_ROOT = Path(__file__).resolve().parents[2]
TOOL_PATH = REPO_ROOT / "tools" / "aggregation" / "build_hypergraph.py"
FIXTURES_ROOT = REPO_ROOT / "tools" / "aggregation" / "testdata"

# Expected PASS codes on a clean run without ledger data.
CLEAN_PASS_CODES: Set[str] = {
    "SCHEMA_PRESENCE",
    "REFERENTIAL_INTEGRITY",
    "CATEGORY_MEMBERSHIP_INTEGRITY",
    "SUBJECT_ATTACHMENT",
    "ARTIFACT_ATTACHMENT",
    "BRIDGE_INTEGRITY",
    "ID_COLLISIONS",
    "EVIDENCE_COMPLETENESS",
}

# When the missing-category fixture runs, these checks should still PASS.
WARNING_FIXTURE_EXPECTED_PASS: Set[str] = {
    "SCHEMA_PRESENCE",
    "REFERENTIAL_INTEGRITY",
    "SUBJECT_ATTACHMENT",
    "ARTIFACT_ATTACHMENT",
    "BRIDGE_INTEGRITY",
    "ID_COLLISIONS",
    "EVIDENCE_COMPLETENESS",
}

# These warning codes must appear in the missing-category fixture run.
WARNING_FIXTURE_EXPECTED_WARNINGS: Set[str] = {
    "CATEGORY_REF_MISSING_NODE",
    "KTY_WITHOUT_CATEGORY",
}


def run_tool(staging_dir: Path, output_dir: Path, run_label: str) -> subprocess.CompletedProcess:
    cmd = [
        sys.executable,
        str(TOOL_PATH),
        "--staging-dir", str(staging_dir),
        "--output-dir", str(output_dir),
        "--run-label", run_label,
        "--execution-root", "execution",
    ]
    return subprocess.run(cmd, capture_output=True, text=True)


def parse_qa_codes_by_level(qa_report: Path) -> dict:
    """Return {level: set(codes)} from a QA_Report.md."""
    text = qa_report.read_text(encoding="utf-8")
    by_level: dict = {"BLOCKER": set(), "WARNING": set(), "PASS": set()}
    current_level = None
    for line in text.splitlines():
        header_match = re.match(r"^## (BLOCKER|WARNING|PASS)", line)
        if header_match:
            current_level = header_match.group(1)
            continue
        if current_level and line.startswith("- **"):
            code_match = re.match(r"^- \*\*([A-Z_]+)\*\*", line)
            if code_match:
                by_level[current_level].add(code_match.group(1))
    return by_level


def strip_generated_at(json_path: Path) -> dict:
    data = json.loads(json_path.read_text(encoding="utf-8"))
    data.pop("generated_at", None)
    return data


def assert_files_equal(path_a: Path, path_b: Path, label: str, failures: List[str]) -> None:
    if path_a.read_bytes() != path_b.read_bytes():
        failures.append(f"determinism: {label} differs between runs ({path_a} vs {path_b})")


def check_clean_minimal(tmp_root: Path, failures: List[str]) -> None:
    staging = FIXTURES_ROOT / "clean_minimal" / "Evidence"
    if not staging.is_dir():
        failures.append(f"fixture missing: {staging}")
        return
    out1 = tmp_root / "clean_minimal_run1"
    out2 = tmp_root / "clean_minimal_run2"
    out1.mkdir(parents=True, exist_ok=True)
    out2.mkdir(parents=True, exist_ok=True)

    result1 = run_tool(staging, out1, "CLEAN_TEST")
    result2 = run_tool(staging, out2, "CLEAN_TEST")
    if result1.returncode != 0:
        failures.append(f"clean_minimal run 1 failed: {result1.stderr.strip()}")
        return
    if result2.returncode != 0:
        failures.append(f"clean_minimal run 2 failed: {result2.stderr.strip()}")
        return

    # Determinism: CSV files must be byte-identical
    for name in ("nodes.csv", "hyperedges.csv", "incidence.csv"):
        assert_files_equal(out1 / name, out2 / name, name, failures)

    # Determinism: hypergraph.json identical after stripping generated_at
    json1 = strip_generated_at(out1 / "hypergraph.json")
    json2 = strip_generated_at(out2 / "hypergraph.json")
    if json1 != json2:
        failures.append("determinism: hypergraph.json differs between runs (after stripping generated_at)")

    # Clean-run PASS coverage
    by_level = parse_qa_codes_by_level(out1 / "QA_Report.md")
    missing_passes = CLEAN_PASS_CODES - by_level["PASS"]
    if missing_passes:
        failures.append(f"clean_minimal: missing PASS rows for checks: {sorted(missing_passes)}")

    # LEDGER_INTEGRITY should NOT appear (fixture has no ledger rows)
    if "LEDGER_INTEGRITY" in by_level["PASS"]:
        failures.append("clean_minimal: LEDGER_INTEGRITY PASS emitted but fixture has no ledger rows")

    # No warnings or blockers expected on clean fixture
    if by_level["WARNING"]:
        failures.append(f"clean_minimal: unexpected warnings emitted: {sorted(by_level['WARNING'])}")
    if by_level["BLOCKER"]:
        failures.append(f"clean_minimal: unexpected blockers emitted: {sorted(by_level['BLOCKER'])}")


def check_warning_missing_category(tmp_root: Path, failures: List[str]) -> None:
    staging = FIXTURES_ROOT / "warning_missing_category" / "Evidence"
    if not staging.is_dir():
        failures.append(f"fixture missing: {staging}")
        return
    out = tmp_root / "warning_missing_category_run"
    out.mkdir(parents=True, exist_ok=True)

    result = run_tool(staging, out, "WARNING_TEST")
    if result.returncode != 0:
        failures.append(f"warning_missing_category run failed: {result.stderr.strip()}")
        return

    by_level = parse_qa_codes_by_level(out / "QA_Report.md")

    # Expected warning codes must all be present
    missing_warnings = WARNING_FIXTURE_EXPECTED_WARNINGS - by_level["WARNING"]
    if missing_warnings:
        failures.append(f"warning_missing_category: expected warnings not emitted: {sorted(missing_warnings)}")

    # Unaffected PASS checks must still appear
    missing_passes = WARNING_FIXTURE_EXPECTED_PASS - by_level["PASS"]
    if missing_passes:
        failures.append(f"warning_missing_category: unaffected PASS rows missing: {sorted(missing_passes)}")

    # CATEGORY_MEMBERSHIP_INTEGRITY should NOT PASS (that's the check detecting the drift)
    if "CATEGORY_MEMBERSHIP_INTEGRITY" in by_level["PASS"]:
        failures.append("warning_missing_category: CATEGORY_MEMBERSHIP_INTEGRITY spuriously PASSed despite missing-category fixture")


def main() -> int:
    parser = argparse.ArgumentParser(description="Regression check for build_hypergraph.py")
    parser.add_argument("--keep-tmp", action="store_true", help="Keep temporary output directories for inspection")
    args = parser.parse_args()

    if not TOOL_PATH.exists():
        print(f"ERROR: tool not found at {TOOL_PATH}", file=sys.stderr)
        return 2
    if not FIXTURES_ROOT.is_dir():
        print(f"ERROR: fixtures directory not found at {FIXTURES_ROOT}", file=sys.stderr)
        return 2

    failures: List[str] = []
    with tempfile.TemporaryDirectory(prefix="hg_fixture_", delete=not args.keep_tmp) as tmp_dir:
        tmp_root = Path(tmp_dir)
        check_clean_minimal(tmp_root, failures)
        check_warning_missing_category(tmp_root, failures)
        if args.keep_tmp:
            print(f"(kept temp outputs at {tmp_root})", file=sys.stderr)

    if failures:
        print("FAIL build_hypergraph fixture regression check:", file=sys.stderr)
        for f in failures:
            print(f"  - {f}", file=sys.stderr)
        return 1

    print("PASS build_hypergraph fixture regression check: determinism + clean-run PASS coverage + warning detection verified")
    return 0


if __name__ == "__main__":
    sys.exit(main())
