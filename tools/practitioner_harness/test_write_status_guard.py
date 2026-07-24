#!/usr/bin/env python3
"""Tests for the write_status.sh precondition guard (tools/scaffolding/write_status.sh).

Subprocesses the zsh script inside tmp_path git repos with fixture adapter
manifests of both shapes (approval-SHA-declaring and not). Fixture manifests
are test material only — the live manifests under projects/*/_harness/ are
NOT read or written by these tests.
"""
from __future__ import annotations

import subprocess
import importlib.util
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "tools" / "scaffolding" / "write_status.sh"
MANIFEST_SHA_DECLARING = """\
schema: practitioner-harness-adapter/v1
project: fixture-app
guard_requires_committed_ruling_path: true
guard_requires_approval_sha: true
guard_approval_sha_field: "Checking Approval SHA"
"""

MANIFEST_NO_SHA_SCHEMA = """\
schema: practitioner-harness-adapter/v1
project: fixture-piping
guard_requires_committed_ruling_path: true
guard_requires_approval_sha: false
guard_approval_sha_field: ""
"""

STATUS_TEMPLATE = """\
# Status: DEL-01-01

**Current State:** {state}
**Last Updated:** 2026-06-01

## History
- 2026-06-01 — State set to {state} (HUMAN)
"""

RULING_REL = "projects/fixture/docs/D-01_fixture_ruling.md"


def _git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        [
            "git",
            "-c",
            "user.name=Fixture",
            "-c",
            "user.email=fixture@example.invalid",
            *args,
        ],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def make_repo(tmp_path: Path, manifest: str, state: str = "IN_PROGRESS"):
    """Build a tmp git repo with a fixture project tree, adapter manifest,
    committed ruling record, and a _STATUS.md at `state`.

    Returns (repo, deldir, head_sha).
    """
    repo = tmp_path / "repo"
    proj = repo / "projects" / "fixture"
    deldir = proj / "execution" / "PKG-01" / "1_Working" / "DEL-01-01_Fixture"
    deldir.mkdir(parents=True)
    harness = proj / "_harness"
    harness.mkdir()
    (harness / "adapter.yaml").write_text(manifest)
    ruling = repo / RULING_REL
    ruling.parent.mkdir(parents=True)
    ruling.write_text("# D-01 — fixture ruling record (test material)\n")
    (deldir / "_STATUS.md").write_text(STATUS_TEMPLATE.format(state=state))
    _git(repo, "init", "-q")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "fixture")
    head = _git(repo, "rev-parse", "HEAD")
    return repo, deldir, head


def run_guard(cwd: Path, *args) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["zsh", str(SCRIPT), *[str(a) for a in args]],
        cwd=cwd,
        capture_output=True,
        text=True,
    )


def read_status(deldir: Path) -> str:
    return (deldir / "_STATUS.md").read_text()


# ---------------------------------------------------------------------------
# Committed-ruling precondition
# ---------------------------------------------------------------------------


def test_refuse_checking_without_ruling(tmp_path):
    repo, deldir, head = make_repo(tmp_path, MANIFEST_SHA_DECLARING)
    before = read_status(deldir)
    result = run_guard(repo, deldir, "CHECKING", "human", "--approval-sha", head)
    assert result.returncode == 1
    assert "RULING_REQUIRED" in result.stderr
    assert read_status(deldir) == before, "refusal must leave _STATUS.md byte-identical"


def test_refuse_uncommitted_ruling_path(tmp_path):
    repo, deldir, head = make_repo(tmp_path, MANIFEST_SHA_DECLARING)
    untracked = repo / "projects" / "fixture" / "docs" / "untracked_note.md"
    untracked.write_text("not committed\n")
    before = read_status(deldir)
    result = run_guard(
        repo,
        deldir,
        "CHECKING",
        "human",
        "--ruling",
        "projects/fixture/docs/untracked_note.md",
        "--approval-sha",
        head,
    )
    assert result.returncode == 1
    assert "RULING_NOT_COMMITTED" in result.stderr
    assert read_status(deldir) == before


def test_refuse_nonexistent_ruling_path(tmp_path):
    repo, deldir, head = make_repo(tmp_path, MANIFEST_SHA_DECLARING)
    before = read_status(deldir)
    result = run_guard(
        repo,
        deldir,
        "CHECKING",
        "human",
        "--ruling",
        "projects/fixture/docs/no_such_file.md",
        "--approval-sha",
        head,
    )
    assert result.returncode == 1
    assert "RULING_PATH_MISSING" in result.stderr
    assert read_status(deldir) == before


# ---------------------------------------------------------------------------
# Approval-SHA precondition (adapter-declared)
# ---------------------------------------------------------------------------


def test_refuse_missing_sha_on_sha_declaring_root(tmp_path):
    repo, deldir, _head = make_repo(tmp_path, MANIFEST_SHA_DECLARING)
    before = read_status(deldir)
    result = run_guard(repo, deldir, "CHECKING", "human", "--ruling", RULING_REL)
    assert result.returncode == 1
    assert "APPROVAL_SHA_REQUIRED" in result.stderr
    assert read_status(deldir) == before


def test_refuse_malformed_sha_on_sha_declaring_root(tmp_path):
    repo, deldir, _head = make_repo(tmp_path, MANIFEST_SHA_DECLARING)
    before = read_status(deldir)
    result = run_guard(
        repo,
        deldir,
        "CHECKING",
        "human",
        "--ruling",
        RULING_REL,
        "--approval-sha",
        "xyz-not-hex",
    )
    assert result.returncode == 1
    assert "INVALID_APPROVAL_SHA" in result.stderr
    assert read_status(deldir) == before


def test_refuse_unreachable_sha_on_sha_declaring_root(tmp_path):
    repo, deldir, _head = make_repo(tmp_path, MANIFEST_SHA_DECLARING)
    before = read_status(deldir)
    result = run_guard(
        repo,
        deldir,
        "CHECKING",
        "human",
        "--ruling",
        RULING_REL,
        "--approval-sha",
        "deadbeefdeadbeefdeadbeefdeadbeefdeadbeef",
    )
    assert result.returncode == 1
    assert "APPROVAL_SHA_UNREACHABLE" in result.stderr
    assert read_status(deldir) == before


def test_checking_success_on_sha_declaring_root_updates_fields(tmp_path):
    repo, deldir, head = make_repo(tmp_path, MANIFEST_SHA_DECLARING)
    result = run_guard(
        repo,
        deldir,
        "CHECKING",
        "human",
        "--ruling",
        RULING_REL,
        "--approval-sha",
        head,
    )
    assert result.returncode == 0, result.stderr
    text = read_status(deldir)
    assert "**Current State:** CHECKING" in text
    assert f"**Checking Approval SHA:** {head}" in text
    assert f"**Authorization Basis:** ruling: {RULING_REL}" in text
    assert "State set to CHECKING (human)" in text
    assert "Status: DEL-01-01" in result.stdout


def test_no_sha_schema_root_proceeds_with_review(tmp_path):
    repo, deldir, _head = make_repo(tmp_path, MANIFEST_NO_SHA_SCHEMA)
    result = run_guard(repo, deldir, "CHECKING", "human", "--ruling", RULING_REL)
    assert result.returncode == 0, result.stderr
    assert "REVIEW" in result.stderr
    assert "no approval-SHA schema" in result.stderr
    text = read_status(deldir)
    assert "**Current State:** CHECKING" in text
    assert "State set to CHECKING (human)" in text
    # No field updates on roots without a declared approval-SHA schema.
    assert "Checking Approval SHA" not in text
    assert "Authorization Basis" not in text


# ---------------------------------------------------------------------------
# State machine
# ---------------------------------------------------------------------------


def test_backward_transition_refused(tmp_path):
    repo, deldir, _head = make_repo(tmp_path, MANIFEST_SHA_DECLARING, state="IN_PROGRESS")
    before = read_status(deldir)
    result = run_guard(repo, deldir, "INITIALIZED", "human")
    assert result.returncode == 1
    assert "BACKWARD_TRANSITION" in result.stderr
    assert read_status(deldir) == before


def test_skip_transition_refused(tmp_path):
    repo, deldir, head = make_repo(tmp_path, MANIFEST_SHA_DECLARING, state="OPEN")
    before = read_status(deldir)
    result = run_guard(
        repo,
        deldir,
        "CHECKING",
        "human",
        "--ruling",
        RULING_REL,
        "--approval-sha",
        head,
    )
    assert result.returncode == 1
    assert "TRANSITION_NOT_ALLOWED" in result.stderr
    assert read_status(deldir) == before


def test_non_human_actor_at_checking_refused(tmp_path):
    repo, deldir, head = make_repo(tmp_path, MANIFEST_SHA_DECLARING)
    before = read_status(deldir)
    result = run_guard(
        repo,
        deldir,
        "CHECKING",
        "PROJECT_SETUP",
        "--ruling",
        RULING_REL,
        "--approval-sha",
        head,
    )
    assert result.returncode == 1
    assert "UNAUTHORIZED_ACTOR" in result.stderr
    assert read_status(deldir) == before


def test_human_alias_actors_accepted_at_checking(tmp_path):
    for actor in ("USER", "operator", "Human (Ryan)"):
        repo, deldir, head = make_repo(
            tmp_path / actor.replace(" ", "_").replace("(", "").replace(")", ""),
            MANIFEST_SHA_DECLARING,
        )
        result = run_guard(
            repo,
            deldir,
            "CHECKING",
            actor,
            "--ruling",
            RULING_REL,
            "--approval-sha",
            head,
        )
        assert result.returncode == 0, f"{actor}: {result.stderr}"


def test_same_state_reassert_allowed_with_warn(tmp_path):
    repo, deldir, _head = make_repo(tmp_path, MANIFEST_SHA_DECLARING, state="IN_PROGRESS")
    result = run_guard(repo, deldir, "IN_PROGRESS", "TASK+working-items")
    assert result.returncode == 0, result.stderr
    assert "WARN" in result.stderr
    assert "same-state re-assert" in result.stderr
    text = read_status(deldir)
    assert text.count("State set to IN_PROGRESS") == 2
    assert "**Current State:** IN_PROGRESS" in text


def test_forward_step_allowed_for_scaffold_actor(tmp_path):
    repo, deldir, _head = make_repo(tmp_path, MANIFEST_SHA_DECLARING, state="OPEN")
    result = run_guard(repo, deldir, "INITIALIZED", "TASK+four-documents")
    assert result.returncode == 0, result.stderr
    assert "**Current State:** INITIALIZED" in read_status(deldir)


def test_invalid_state_is_usage_error(tmp_path):
    repo, deldir, _head = make_repo(tmp_path, MANIFEST_SHA_DECLARING)
    result = run_guard(repo, deldir, "NOT_A_STATE", "human")
    assert result.returncode == 2
    assert "Invalid state" in result.stderr


# ---------------------------------------------------------------------------
# New-file creation
# ---------------------------------------------------------------------------


def test_new_file_creation_at_open_allowed(tmp_path):
    repo, deldir, _head = make_repo(tmp_path, MANIFEST_SHA_DECLARING)
    fresh = deldir.parent / "DEL-01-02_Fresh"
    fresh.mkdir()
    result = run_guard(repo, fresh, "OPEN", "PREPARATION")
    assert result.returncode == 0, result.stderr
    text = read_status(fresh)
    assert "**Current State:** OPEN" in text
    assert "State set to OPEN (PREPARATION)" in text
    assert "Status: DEL-01-02" in result.stdout


def test_new_file_creation_at_checking_refused(tmp_path):
    repo, deldir, head = make_repo(tmp_path, MANIFEST_SHA_DECLARING)
    fresh = deldir.parent / "DEL-01-03_Fresh"
    fresh.mkdir()
    result = run_guard(
        repo,
        fresh,
        "CHECKING",
        "human",
        "--ruling",
        RULING_REL,
        "--approval-sha",
        head,
    )
    assert result.returncode == 1
    assert "NEW_FILE_NOT_OPEN" in result.stderr
    assert not (fresh / "_STATUS.md").exists()


# ---------------------------------------------------------------------------
# Human override
# ---------------------------------------------------------------------------


def test_force_human_override_records_reason(tmp_path):
    repo, deldir, _head = make_repo(tmp_path, MANIFEST_SHA_DECLARING, state="IN_PROGRESS")
    reason = "reverting after human review of fixture drift"
    result = run_guard(
        repo,
        deldir,
        "INITIALIZED",
        "human",
        "--force-human-override",
        reason,
    )
    assert result.returncode == 0, result.stderr
    assert "OVERRIDE recorded" in result.stderr
    assert "BACKWARD_TRANSITION" in result.stderr
    text = read_status(deldir)
    assert "**Current State:** INITIALIZED" in text
    assert f"[override: {reason}]" in text


def test_force_human_override_requires_human_actor(tmp_path):
    repo, deldir, _head = make_repo(tmp_path, MANIFEST_SHA_DECLARING, state="IN_PROGRESS")
    before = read_status(deldir)
    result = run_guard(
        repo,
        deldir,
        "INITIALIZED",
        "PROJECT_SETUP",
        "--force-human-override",
        "should not apply",
    )
    assert result.returncode == 1
    assert "BACKWARD_TRANSITION" in result.stderr
    assert "does not normalize to HUMAN" in result.stderr
    assert read_status(deldir) == before


def test_force_human_override_never_overrides_usage_errors(tmp_path):
    repo, deldir, _head = make_repo(tmp_path, MANIFEST_SHA_DECLARING)
    result = run_guard(
        repo,
        deldir,
        "NOT_A_STATE",
        "human",
        "--force-human-override",
        "irrelevant",
    )
    assert result.returncode == 2


# ---------------------------------------------------------------------------
# Outside a git repo (export/staging context)
# ---------------------------------------------------------------------------


def _make_non_git_tree(tmp_path: Path, state: str) -> Path:
    plain = tmp_path / "plain"
    deldir = plain / "PKG-01" / "1_Working" / "DEL-09-01_NoRepo"
    deldir.mkdir(parents=True)
    (deldir / "_STATUS.md").write_text(STATUS_TEMPLATE.format(state=state))
    return deldir


def test_non_git_dir_skips_git_checks_with_review(tmp_path):
    deldir = _make_non_git_tree(tmp_path, "IN_PROGRESS")
    result = run_guard(tmp_path, deldir, "CHECKING", "human")
    assert result.returncode == 0, result.stderr
    assert "REVIEW: not a git repository" in result.stderr
    assert "**Current State:** CHECKING" in read_status(deldir)


def test_non_git_dir_state_machine_still_enforced(tmp_path):
    deldir = _make_non_git_tree(tmp_path, "OPEN")
    before = read_status(deldir)
    result = run_guard(tmp_path, deldir, "CHECKING", "human")
    assert result.returncode == 1
    assert "TRANSITION_NOT_ALLOWED" in result.stderr
    assert read_status(deldir) == before


def test_non_git_dir_actor_gate_still_enforced(tmp_path):
    deldir = _make_non_git_tree(tmp_path, "IN_PROGRESS")
    before = read_status(deldir)
    result = run_guard(tmp_path, deldir, "CHECKING", "PROJECT_SETUP")
    assert result.returncode == 1
    assert "UNAUTHORIZED_ACTOR" in result.stderr
    assert read_status(deldir) == before


# ---------------------------------------------------------------------------
# Live export byte-identity
# ---------------------------------------------------------------------------


def test_canonical_and_staging_guard_byte_identity(tmp_path):
    exporter_path = REPO_ROOT / "exports" / "chirality-app" / "export_public.py"
    if not exporter_path.exists():
        pytest.skip("public export intentionally excludes the private export profile")
    spec = importlib.util.spec_from_file_location("chirality_public_export_guard", exporter_path)
    assert spec and spec.loader
    exporter = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(exporter)
    stage = tmp_path / "public-stage"
    exporter.build_stage(stage)
    staged_script = stage / "tools" / "scaffolding" / "write_status.sh"
    canonical = SCRIPT.read_bytes()
    staged = staged_script.read_bytes()
    assert canonical == staged


# ---------------------------------------------------------------------------
# Metacharacter safety + anchor fallback (adversarial-review findings)
# ---------------------------------------------------------------------------


MANIFEST_AMPERSAND_FIELD = """\
schema: practitioner-harness-adapter/v1
project: fixture-app
guard_requires_committed_ruling_path: true
guard_requires_approval_sha: true
guard_approval_sha_field: "R&D SHA"
"""


def test_ampersand_in_field_name_and_ruling_path_not_corrupted(tmp_path):
    """Regression: BSD sed '&' match-reference corrupted upsert lines."""
    repo, deldir, head = make_repo(tmp_path, MANIFEST_AMPERSAND_FIELD)
    ruling = repo / "projects" / "fixture" / "docs" / "D&X_ruling.md"
    ruling.write_text("# fixture ruling with ampersand (test material)\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "add ampersand ruling")
    head = _git(repo, "rev-parse", "HEAD")
    result = run_guard(
        repo, deldir, "CHECKING", "human",
        "--ruling", "projects/fixture/docs/D&X_ruling.md",
        "--approval-sha", head,
    )
    assert result.returncode == 0, result.stderr
    text = read_status(deldir)
    assert f"**R&D SHA:** {head}\n" in text
    assert "**Authorization Basis:** ruling: projects/fixture/docs/D&X_ruling.md\n" in text
    # exactly one occurrence each; no mangled duplication
    assert text.count("**R&D SHA:**") == 1
    assert text.count("**Authorization Basis:**") == 1
    # re-assert same state: replace branch, still exactly one line each
    result2 = run_guard(
        repo, deldir, "CHECKING", "human",
        "--ruling", "projects/fixture/docs/D&X_ruling.md",
        "--approval-sha", head,
    )
    assert result2.returncode == 0, result2.stderr
    text2 = read_status(deldir)
    assert text2.count("**R&D SHA:**") == 1
    assert text2.count("**Authorization Basis:**") == 1


def test_missing_last_updated_anchor_falls_back_to_current_state(tmp_path):
    """Regression: required fields were silently dropped (exit 0) when the
    status file had no '**Last Updated:**' line."""
    repo, deldir, head = make_repo(tmp_path, MANIFEST_SHA_DECLARING)
    status = deldir / "_STATUS.md"
    status.write_text(
        "# Status: DEL-01-01\n\n"
        "**Current State:** IN_PROGRESS\n\n"
        "## History\n"
        "- 2026-06-01 — State set to IN_PROGRESS (HUMAN)\n"
    )
    result = run_guard(
        repo, deldir, "CHECKING", "human",
        "--ruling", RULING_REL,
        "--approval-sha", head,
    )
    assert result.returncode == 0, result.stderr
    text = read_status(deldir)
    assert f"**Checking Approval SHA:** {head}\n" in text, (
        "required field silently dropped without Last Updated anchor"
    )
    assert "**Authorization Basis:**" in text
