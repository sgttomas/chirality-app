from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

import pytest

import cmd_self_check
from surface_roles import (
    SurfaceRole,
    classify_surface,
    load_project_policy,
    normalize_repo_relative_path,
)
from test_self_check_fixtures import _write, build_mini_repo


PROJECT_REL = "projects/chirality-piping"
AGENTRUN = (
    "projects/chirality-piping/execution/_Coordination/AgentRuns/R10"
)
ABS = "/Users/fixture/worktree/projects/chirality-piping"


def _policy(repo: Path, overrides=None, exceptions=None) -> Path:
    path = repo / PROJECT_REL / "validation" / "portability_policy.json"
    _write(path, json.dumps({
        "schema_version": 1,
        "project_root": PROJECT_REL,
        "historical_role_overrides": overrides or [],
        "control_path_exceptions": exceptions or [],
    }, indent=2) + "\n")
    return path


def _entry(repo: Path, rel: str, entry_type: str, role: str) -> dict[str, str]:
    return {
        "path": rel,
        "sha256": hashlib.sha256((repo / rel).read_bytes()).hexdigest(),
        "entry_type": entry_type,
        "role": role,
        "reason": "Immutable fixture migration record.",
        "authority": "Fixture owner approval.",
    }


def _portability_findings(report):
    return [f for f in report.findings if f.code in {
        "ABS_PATH_IN_PROJECT_SURFACE",
        "ABS_PATH_IN_UNCLASSIFIED_SURFACE",
    } or f.code.startswith("PORTABILITY_POLICY_")]


def test_structural_roles_use_control_precedence_and_fail_closed():
    assert classify_surface(f"{AGENTRUN}/LAUNCH_BRIEF.md").role is SurfaceRole.CONTROL
    assert classify_surface(f"{AGENTRUN}/RETURN.md").role is SurfaceRole.EVIDENCE
    assert classify_surface(
        f"{AGENTRUN}/_run_records/LAUNCH_BRIEF.md").role is SurfaceRole.CONTROL
    unknown = classify_surface(f"{AGENTRUN}/CAPTURE.json")
    assert unknown.role is SurfaceRole.UNCLASSIFIED
    assert unknown.active is True
    assert classify_surface(f"{AGENTRUN}/PREFLIGHT_FINAL.json").role is (
        SurfaceRole.UNCLASSIFIED)
    assert classify_surface(f"{AGENTRUN}/RETURNED.md").role is (
        SurfaceRole.UNCLASSIFIED)
    assert classify_surface(f"{AGENTRUN}/LAUNCH_BRIEF.md.bak").role is (
        SurfaceRole.UNCLASSIFIED)


@pytest.mark.parametrize("name", [
    "NOT_A_RETURN.md",
    "RETURN_INSTRUCTIONS.md",
    "HANDOFF_INSTRUCTIONS.md",
    "SECRET_SUMMARY.md",
    "ARBITRARY_RESULT.json",
    "UNREGISTERED_MANIFEST.yaml",
])
def test_misleading_evidence_token_names_remain_unclassified(name: str):
    classification = classify_surface(f"{AGENTRUN}/{name}")
    assert classification.role is SurfaceRole.UNCLASSIFIED
    assert classification.active is True


@pytest.mark.parametrize("name", [
    "RETURN.md",
    "RETURN_V1.md",
    "RETURN_V12.md",
    "HANDOFF_STATE.md",
    "STATUS.json",
    "STATUS_V2.json",
    "RUN_RECORD.md",
    "INTERRUPTION_RECORD.md",
    "TOOL_ERROR_RECORD.md",
])
def test_exact_registered_evidence_records_are_evidence(name: str):
    assert classify_surface(f"{AGENTRUN}/{name}").role is SurfaceRole.EVIDENCE


@pytest.mark.parametrize("name", [
    "return.md",
    "Return.md",
    "status.json",
    "STATUS_V0.json",
    "STATUS_V01.json",
    "RETURN_V1.JSON",
    "RETURN_V1.json",
    "STATUS_V1.md",
    "RETURN.md.bak",
    "ARBITRARY.txt",
])
def test_case_near_matches_and_unknown_extensions_fail_closed(name: str):
    assert classify_surface(f"{AGENTRUN}/{name}").role is SurfaceRole.UNCLASSIFIED


@pytest.mark.parametrize("value", [
    "/projects/example/file.md",
    "projects/example/../file.md",
    "projects/example/./file.md",
    "projects//example/file.md",
    r"projects\example\file.md",
])
def test_path_normalization_rejects_noncanonical_values(value: str):
    with pytest.raises(ValueError):
        normalize_repo_relative_path(value)


@pytest.mark.parametrize("name", [
    "NOT_A_RETURN.md",
    "RETURN_INSTRUCTIONS.md",
    "HANDOFF_INSTRUCTIONS.md",
    "SECRET_SUMMARY.md",
    "ARBITRARY_RESULT.json",
    "UNREGISTERED_MANIFEST.yaml",
])
def test_every_verifier_counterexample_is_actionable_in_self_check(
        tmp_path: Path, name: str):
    repo = build_mini_repo(tmp_path)
    _policy(repo)
    _write(repo / AGENTRUN / name, json.dumps({"cwd": ABS}) + "\n")

    report, _ = cmd_self_check.run_self_check(repo, repo / PROJECT_REL)

    hits = [f for f in report.findings
            if f.code == "ABS_PATH_IN_UNCLASSIFIED_SURFACE"]
    assert [(f.source_path, f.source_line) for f in hits] == [
        (f"{AGENTRUN}/{name}", 1)]


def test_active_launch_brief_portability_and_evidence_behavior(tmp_path: Path):
    repo = build_mini_repo(tmp_path)
    _policy(repo)
    _write(repo / AGENTRUN / "LAUNCH_BRIEF.md", "Root: {REPO_ROOT}\n")
    _write(repo / AGENTRUN / "RETURN.md", f"Ran at {ABS}\n")

    report, _ = cmd_self_check.run_self_check(repo, repo / PROJECT_REL)

    assert _portability_findings(report) == []

    _write(repo / AGENTRUN / "LAUNCH_BRIEF.md", f"Root: {ABS}\n")
    report, _ = cmd_self_check.run_self_check(repo, repo / PROJECT_REL)
    hits = [f for f in report.findings if f.code == "ABS_PATH_IN_PROJECT_SURFACE"]
    assert [(f.source_path, f.source_line) for f in hits] == [
        (f"{AGENTRUN}/LAUNCH_BRIEF.md", 1)]


def test_unknown_active_agentruns_artifact_fails_closed(tmp_path: Path):
    repo = build_mini_repo(tmp_path)
    _policy(repo)
    _write(repo / AGENTRUN / "CAPTURE.json", json.dumps({"cwd": ABS}) + "\n")

    report, _ = cmd_self_check.run_self_check(repo, repo / PROJECT_REL)

    hits = [f for f in report.findings
            if f.code == "ABS_PATH_IN_UNCLASSIFIED_SURFACE"]
    assert len(hits) == 1
    assert hits[0].source_path == f"{AGENTRUN}/CAPTURE.json"


def test_hash_bound_role_override_and_control_exception(tmp_path: Path):
    repo = build_mini_repo(tmp_path)
    capture_rel = f"{AGENTRUN}/CAPTURE.json"
    control_rel = f"{AGENTRUN}/ORCHESTRATION_PLAN.md"
    _write(repo / capture_rel, json.dumps({"cwd": ABS}) + "\n")
    _write(repo / control_rel, f"Historical root: {ABS}\n")
    _policy(
        repo,
        [_entry(repo, capture_rel, "historical_role_override", "EVIDENCE")],
        [_entry(repo, control_rel, "control_path_exception", "CONTROL")],
    )

    loaded = load_project_policy(repo, repo / PROJECT_REL)
    assert loaded.issues == ()
    report, _ = cmd_self_check.run_self_check(repo, repo / PROJECT_REL)
    assert _portability_findings(report) == []
    invariant = next(f for f in report.facts
                     if f.fact_id.endswith("semantic_invariants"))
    assert invariant.value.endswith("acknowledged_control=1")

    _write(repo / capture_rel, json.dumps({"cwd": ABS, "drift": True}) + "\n")
    loaded = load_project_policy(repo, repo / PROJECT_REL)
    assert [issue.code for issue in loaded.issues] == [
        "PORTABILITY_POLICY_HASH_DRIFT"]


def test_ledger_rejects_duplicate_missing_authority_and_stale_entry(tmp_path: Path):
    repo = build_mini_repo(tmp_path)
    rel = f"{AGENTRUN}/CAPTURE.json"
    _write(repo / rel, "portable capture\n")
    entry = _entry(repo, rel, "historical_role_override", "EVIDENCE")
    entry["authority"] = ""
    _policy(repo, [entry, dict(entry)])

    codes = {issue.code for issue in load_project_policy(
        repo, repo / PROJECT_REL).issues}

    assert "PORTABILITY_POLICY_SCHEMA" in codes
    assert "PORTABILITY_POLICY_DUPLICATE" in codes


def test_unrelated_evidence_growth_does_not_change_semantic_invariant(tmp_path: Path):
    repo = build_mini_repo(tmp_path)
    _policy(repo)
    _write(repo / AGENTRUN / "RETURN.md", f"Run one: {ABS}\n")
    first, _ = cmd_self_check.run_self_check(repo, repo / PROJECT_REL)
    first_value = next(f.value for f in first.facts
                       if f.fact_id.endswith("semantic_invariants"))
    _write(repo / AGENTRUN / "instances" / "child" / "RETURN.md",
           f"Run two: {ABS}\n")
    second, _ = cmd_self_check.run_self_check(repo, repo / PROJECT_REL)
    second_value = next(f.value for f in second.facts
                        if f.fact_id.endswith("semantic_invariants"))

    assert first_value == second_value == (
        "unacknowledged_control=0; active_unclassified=0; "
        "policy_issues=0; acknowledged_control=0")


def test_stale_override_and_non_normalized_path_are_rejected(tmp_path: Path):
    repo = build_mini_repo(tmp_path)
    rel = f"{AGENTRUN}/CAPTURE.json"
    _write(repo / rel, "portable capture\n")
    stale = _entry(repo, rel, "historical_role_override", "EVIDENCE")
    bad_path = dict(stale)
    bad_path["path"] = f"{PROJECT_REL}/validation/../CAPTURE.json"
    _policy(repo, [stale, bad_path])

    codes = {issue.code for issue in load_project_policy(
        repo, repo / PROJECT_REL).issues}

    assert "PORTABILITY_POLICY_STALE" in codes
    assert "PORTABILITY_POLICY_PATH" in codes


def test_missing_target_and_structural_role_mismatch_are_rejected(tmp_path: Path):
    repo = build_mini_repo(tmp_path)
    return_rel = f"{AGENTRUN}/RETURN.md"
    _write(repo / return_rel, f"Ran at {ABS}\n")
    wrong_role = _entry(
        repo, return_rel, "historical_role_override", "EVIDENCE")
    missing = {
        "path": f"{AGENTRUN}/MISSING.json",
        "sha256": "0" * 64,
        "entry_type": "historical_role_override",
        "role": "EVIDENCE",
        "reason": "Missing fixture target.",
        "authority": "Fixture owner approval.",
    }
    _policy(repo, [wrong_role, missing])

    codes = {issue.code for issue in load_project_policy(
        repo, repo / PROJECT_REL).issues}

    assert "PORTABILITY_POLICY_ROLE_MISMATCH" in codes
    assert "PORTABILITY_POLICY_TARGET_MISSING" in codes


def test_raw_evidence_attributes_preserve_diff_check_boundary(tmp_path: Path):
    repo = tmp_path / "repo"
    project = repo / PROJECT_REL
    project.mkdir(parents=True)
    attributes = (
        "validation/evidence/reproduction/REPRO_DEL0904_*/stdout/*.txt "
        "-diff -merge -text\n"
        "validation/evidence/reproduction/REPRO_DEL0904_*/stderr/*.txt "
        "-diff -merge -text\n"
    )
    _write(project / ".gitattributes", attributes)
    subprocess.run(["git", "-C", str(repo), "init", "-q"], check=True)
    subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
    subprocess.run([
        "git", "-C", str(repo), "-c", "user.name=fixture",
        "-c", "user.email=fixture@example.com", "commit", "-qm", "base",
    ], check=True)
    evidence = (
        project / "validation/evidence/reproduction/"
        "REPRO_DEL0904_20260719T000000Z_fixture/stdout/result.txt"
    )
    evidence.parent.mkdir(parents=True)
    evidence.write_bytes(b"byte-exact output\n\n")
    subprocess.run(["git", "-C", str(repo), "add", str(evidence)], check=True)
    clean = subprocess.run(
        ["git", "-C", str(repo), "diff", "--cached", "--check"],
        capture_output=True, text=True, check=False)
    assert clean.returncode == 0, clean.stdout + clean.stderr
    attr = subprocess.run([
        "git", "-C", str(repo), "check-attr", "diff", "merge", "text",
        "--", str(evidence.relative_to(repo)),
    ], capture_output=True, text=True, check=True).stdout
    assert "diff: unset" in attr
    assert "merge: unset" in attr
    assert "text: unset" in attr

    authored = project / "AUTHORED.md"
    authored.write_bytes(b"trailing whitespace \n")
    subprocess.run(["git", "-C", str(repo), "add", str(authored)], check=True)
    bad = subprocess.run(
        ["git", "-C", str(repo), "diff", "--cached", "--check"],
        capture_output=True, text=True, check=False)
    assert bad.returncode != 0
    assert "trailing whitespace" in bad.stdout


def test_untracked_active_managed_control_is_checked_before_commit(tmp_path: Path):
    repo = build_mini_repo(tmp_path)
    _policy(repo)
    subprocess.run(["git", "-C", str(repo), "init", "-q"], check=True)
    subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
    subprocess.run([
        "git", "-C", str(repo), "-c", "user.name=fixture",
        "-c", "user.email=fixture@example.com", "commit", "-qm", "base",
    ], check=True)
    _write(repo / AGENTRUN / "LAUNCH_BRIEF.md", f"Root: {ABS}\n")

    report, _ = cmd_self_check.run_self_check(repo, repo / PROJECT_REL)

    hits = [f for f in report.findings if f.code == "ABS_PATH_IN_PROJECT_SURFACE"]
    assert [f.source_path for f in hits] == [f"{AGENTRUN}/LAUNCH_BRIEF.md"]
