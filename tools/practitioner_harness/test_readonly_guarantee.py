#!/usr/bin/env python3
"""Read-only guarantee: every harness command (inspection views, `next`,
brief generation and `brief --verify-adoption`) leaves every governed file
byte-identical, and all file writes land under the generated root."""

from __future__ import annotations

import hashlib
import shutil
from pathlib import Path

import pytest

import harness
from harness_common import GENERATED_ROOT_NAME
from test_brief_adoption import _git
from test_run_validations import BRIEF_RELPATH, build_run_repo
from test_self_check_fixtures import build_mini_repo

requires_git = pytest.mark.skipif(shutil.which("git") is None,
                                  reason="git not available")

LIVE_REPO = Path(__file__).resolve().parents[2]
LIVE_SAMPLE_GLOB = "projects/chirality-piping/execution/PKG-0*/1_Working/*/_STATUS.md"


def _hash_tree(root: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    for p in sorted(root.rglob("*")):
        if not p.is_file():
            continue
        if GENERATED_ROOT_NAME in p.parts:
            continue
        out[str(p.relative_to(root))] = hashlib.sha256(p.read_bytes()).hexdigest()
    return out


def _copy_real_samples(repo: Path) -> None:
    """Fold a few real corpus samples (paths with spaces) into the fixture."""
    samples = sorted(LIVE_REPO.glob(LIVE_SAMPLE_GLOB))[:3]
    for i, sample in enumerate(samples):
        dest = (repo / "projects" / "chirality-piping" / "execution"
                / "PKG-01_Fixture Pkg" / "1_Working"
                / f"DEL-01-9{i}_Real sample {sample.parent.name[:24]}"
                / "_STATUS.md")
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(sample, dest)


def test_all_commands_leave_governed_tree_byte_identical(tmp_path, capsys):
    repo = build_mini_repo(tmp_path)
    if LIVE_REPO.joinpath("projects", "chirality-piping").is_dir():
        _copy_real_samples(repo)
    before = _hash_tree(repo)
    assert before, "fixture tree must not be empty"

    commands = [
        ["status", "--project", "app-dev"],
        ["status", "--project", "piping"],
        ["status", "--domain-engines"],
        ["drift", "--all"],
        ["drift", "--all", "--include-domain-engines"],
        ["self-check"],
        ["self-check", "--root", str(repo / "_DomainEngines")],
        ["bridge-status"],
        ["next"],
        # The brief generate step writes ONLY under the generated root (the
        # declared write-posture exception, excluded from the hash) so the
        # verify-adoption step exercises a REAL verification of that file;
        # governed files must stay byte-identical throughout.
        ["brief", "--project", "piping", "--deliverable", "DEL-01-01",
         "--tranche-id", "TRB-readonly-001"],
        ["brief", "--verify-adoption",
         GENERATED_ROOT_NAME + "/briefs/TRB-readonly-001.md"],
        # run-validations in --list mode qualifies for the readonly suite:
        # nothing is executed and nothing is written (full runs do NOT
        # belong here — they execute declared commands and write evidence
        # records).
        ["run-validations", "--brief",
         GENERATED_ROOT_NAME + "/briefs/TRB-readonly-001.md", "--list"],
    ]
    for i, cmd in enumerate(commands):
        rc = harness.main([
            "--repo-root", str(repo),
            "--json-report", str(repo / GENERATED_ROOT_NAME / "reports"
                                 / f"run_{i:02d}.json"),
            *cmd])
        assert rc in (0, 1), cmd  # inspection may find, must not crash/refuse
        capsys.readouterr()

    after = _hash_tree(repo)
    assert after == before, "governed tree changed byte-wise"

    # All writes landed under the generated root.
    gen_root = repo / GENERATED_ROOT_NAME
    written = [p for p in gen_root.rglob("*") if p.is_file()]
    assert written, "expected JSON reports under the generated root"
    for p in written:
        assert GENERATED_ROOT_NAME in p.parts


@requires_git
def test_phase4_checks_read_governed_files_only(tmp_path, capsys):
    """scope-check, evidence-check, closeout-digest WITHOUT --write-digest,
    and coord-check read governed files only: the governed tree stays
    byte-identical and nothing lands under the generated root. (.git/ is
    excluded from the hash: `git status` refreshes the index stat cache; the
    read-only guarantee covers the governed working tree.)"""
    repo = build_run_repo(tmp_path, [{"cwd": ".", "command": "echo readonly"}])
    base = _git(repo, "rev-parse", "HEAD")
    dest = (repo / "projects" / "chirality-piping" / "execution"
            / "DEL-01-01" / "notes.md")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text("in-fence fixture change\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "in-fence change")

    def hash_tree() -> dict[str, str]:
        out: dict[str, str] = {}
        for p in sorted(repo.rglob("*")):
            if not p.is_file():
                continue
            if GENERATED_ROOT_NAME in p.parts or ".git" in p.parts:
                continue
            out[str(p.relative_to(repo))] = hashlib.sha256(
                p.read_bytes()).hexdigest()
        return out

    before = hash_tree()
    assert before, "fixture tree must not be empty"
    commands = [
        ["scope-check", "--brief", BRIEF_RELPATH, "--diff", f"{base}..HEAD"],
        ["evidence-check", "--brief", BRIEF_RELPATH],
        # closeout-digest WITHOUT --write-digest: reads only.
        ["closeout-digest", "--brief", BRIEF_RELPATH,
         "--diff", f"{base}..HEAD"],
        ["coord-check", "--diff", f"{base}..HEAD"],
    ]
    for cmd in commands:
        rc = harness.main(["--repo-root", str(repo), *cmd])
        assert rc in (0, 1), cmd  # inspection may find, must not crash/refuse
        capsys.readouterr()
    assert hash_tree() == before, "governed tree changed byte-wise"
    gen_root = repo / GENERATED_ROOT_NAME
    written = ([p for p in gen_root.rglob("*") if p.is_file()]
               if gen_root.exists() else [])
    assert written == [], "the three checks must write nothing by default"


def test_brief_writes_only_under_out_dir(tmp_path, capsys):
    repo = build_mini_repo(tmp_path)
    before = _hash_tree(repo)
    rc = harness.main([
        "--repo-root", str(repo), "brief", "--project", "piping",
        "--deliverable", "DEL-01-01", "--tranche-id", "TRB-fixture-001"])
    assert rc == 0
    capsys.readouterr()
    assert _hash_tree(repo) == before
    briefs = repo / GENERATED_ROOT_NAME / "briefs"
    assert (briefs / "TRB-fixture-001.md").is_file()
    assert (briefs / "TRB-fixture-001.json").is_file()
