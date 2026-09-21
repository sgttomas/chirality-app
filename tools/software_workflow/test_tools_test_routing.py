#!/usr/bin/env python3
"""Drift guards for the tools/ test-routing profile.

The routing profile is a PR/session economy layered over the full gate
(pushes to main always run everything), but a stale profile could still
let a PR skip a suite it should have run. These tests pin the profile to
reality: every test-bearing tools/ directory must be routed, every rule
must reference real checks, and the selector + runner must agree with
the profile.
"""
from __future__ import annotations

import json
import importlib.util
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PROFILE_PATH = REPO_ROOT / "tools" / "tools-test-routing.json"
RUNNER = REPO_ROOT / "tools" / "run_affected_tests.py"


def load_runner():
    spec = importlib.util.spec_from_file_location("chirality_run_affected_tests", RUNNER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_profile() -> dict:
    return json.loads(PROFILE_PATH.read_text(encoding="utf-8"))


def test_bearing_dirs() -> set[str]:
    return {
        f"tools/{path.parent.name}"
        for path in (REPO_ROOT / "tools").glob("*/test_*.py")
    }


def test_profile_schema_loads_via_ratified_loader():
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    try:
        from software_workflow_common import load_profile as ratified_load
    finally:
        sys.path.pop(0)
    project_root, data = ratified_load(PROFILE_PATH)
    assert project_root == REPO_ROOT
    assert data["always_checks"]


def test_every_test_bearing_dir_is_routed():
    profile = load_profile()
    covered_dirs = {
        pytest_path
        for check in profile["checks"].values()
        for pytest_path in check["pytest_paths"]
    }
    missing = test_bearing_dirs() - covered_dirs
    assert not missing, (
        f"test-bearing dirs absent from the routing profile: {sorted(missing)} "
        "— add a check + path_rule to tools/tools-test-routing.json"
    )


def test_every_routed_check_dir_exists_and_bears_tests():
    profile = load_profile()
    for check_id, check in profile["checks"].items():
        for pytest_path in check["pytest_paths"]:
            directory = REPO_ROOT / pytest_path
            assert directory.is_dir(), f"{check_id}: {pytest_path} missing"
            assert list(directory.glob("test_*.py")), (
                f"{check_id}: {pytest_path} contains no test files"
            )


def test_every_non_always_check_is_reachable_by_some_rule():
    # software_workflow itself has no dedicated rule by design: its dir is
    # routing infrastructure, covered by the force-everything rule.
    profile = load_profile()
    always = set(profile["always_checks"])
    assert always <= set(profile["checks"])
    reachable: set[str] = set()
    for rule in profile["path_rules"]:
        reachable.update(rule["checks"])
    unrouted = set(profile["checks"]) - always - reachable
    assert not unrouted, (
        f"checks with neither always status nor any path rule: "
        f"{sorted(unrouted)}"
    )


def test_rules_reference_only_known_checks():
    profile = load_profile()
    known = set(profile["checks"])
    for rule in profile["path_rules"]:
        unknown = set(rule["checks"]) - known
        assert not unknown, f"rule {rule['paths']} references {sorted(unknown)}"


def _dry_run(*args: str) -> dict:
    result = subprocess.run(
        [sys.executable, str(RUNNER), "--dry-run", *args],
        capture_output=True, text=True, check=True, cwd=REPO_ROOT,
    )
    # Selection JSON is the only multi-line JSON object on stdout; it is
    # printed before the [run-affected] summary line.
    payload = result.stdout[result.stdout.index("{"):result.stdout.rindex("}") + 1]
    return json.loads(payload)


def test_runner_isolated_change_selects_core_plus_owner():
    selection = _dry_run("--paths", "tools/pdf2md/render_table_xlsx.py")
    assert set(selection["checks"]) == {
        "practitioner_harness", "validation", "pdf2md",
    }


def test_runner_unrelated_change_selects_core_only():
    selection = _dry_run("--paths", "docs/SOME_DOC.md")
    profile = load_profile()
    assert set(selection["checks"]) == set(profile["always_checks"])


def test_runner_routing_infrastructure_change_selects_everything():
    profile = load_profile()
    for trigger in ("tools/tools-test-routing.json",
                    "tools/run_affected_tests.py",
                    ".github/workflows/governance-harness.yml",
                    "tools/validation/conftest.py"):
        selection = _dry_run("--paths", trigger)
        assert set(selection["checks"]) == set(profile["checks"]), trigger


def test_runner_all_flag_covers_the_full_estate():
    selection = _dry_run("--all")
    assert set(selection["checks"]) == set(load_profile()["checks"])


def test_runner_streams_path_sets_larger_than_linux_argmax():
    runner = load_runner()
    paths = [f"domains/demo/deep/path/file-{index:05d}.md" for index in range(40_000)]
    selection = runner.select_checks(paths)
    assert selection["paths"] == paths
    assert set(selection["checks"]) == set(load_profile()["always_checks"])
