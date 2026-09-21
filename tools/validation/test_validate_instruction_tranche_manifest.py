"""Tests for G4, the D-GOV-21 instruction-surface tranche manifest guard."""

import subprocess
import sys
from pathlib import Path

import yaml

import validate_instruction_tranche_manifest as g4


def _manifest(tranche_id: str = "T-DEMO", **overrides) -> dict:
    data = {
        "schema": "instruction-tranche-manifest/v1",
        "tranche_id": tranche_id,
        "title": "Demo tranche",
        "date": "2026-07-25",
        "instruction_surface_paths": ["tools/validation/demo.py"],
        "m2_gate": {
            "authorization": "owner direction of record, in-session 2026-07-25",
            "authorized_by": "Ryan Tufts",
            "authorization_date": "2026-07-25",
            "integration_owner": "HELP_HUMAN (Agent 0)",
            "merge_gate": "human-gated-pr",
            "self_merge": False,
        },
        "m6_notice": {
            "disposition": "none-required",
            "routed_to": [],
            "rationale": "No project loop pins the touched surfaces.",
        },
    }
    data.update(overrides)
    return data


def _write_manifest(root: Path, data: dict, stem: str | None = None) -> Path:
    stem = stem or str(data.get("tranche_id", "T-DEMO"))
    path = root / g4.MANIFEST_DIR_RELPATH / f"{stem}.yaml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    return path


def _git(root: Path, *args: str) -> str:
    out = subprocess.run(
        [
            "git",
            "-C",
            str(root),
            "-c",
            "user.name=Test",
            "-c",
            "user.email=test@example.invalid",
            "-c",
            "commit.gpgsign=false",
            *args,
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return out.stdout.strip()


def _init_repo(root: Path) -> None:
    _git(root, "init", "-q", "-b", "main")
    (root / "README.md").write_text("seed\n", encoding="utf-8")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "seed")


def _run_cli(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(Path(g4.__file__).resolve()), *args],
        cwd=root,
        capture_output=True,
        text=True,
    )


def test_block_when_manifest_directory_absent(tmp_path):
    code, lines = g4.check(tmp_path)
    assert code == 1
    assert any("does not exist" in line for line in lines)


def test_block_when_manifest_directory_empty(tmp_path):
    (tmp_path / g4.MANIFEST_DIR_RELPATH).mkdir(parents=True)
    code, lines = g4.check(tmp_path)
    assert code == 1
    assert any("silently emptied" in line for line in lines)


def test_pass_with_valid_manifest(tmp_path):
    _write_manifest(tmp_path, _manifest())
    code, lines = g4.check(tmp_path)
    assert code == 0, lines
    assert any("G4 PASS (CI mode)" in line for line in lines)


def test_block_on_unknown_schema(tmp_path):
    _write_manifest(tmp_path, _manifest(schema="tranche/v0"))
    code, lines = g4.check(tmp_path)
    assert code == 1
    assert any("this guard understands" in line for line in lines)


def test_block_on_missing_required_keys(tmp_path):
    data = _manifest()
    del data["m2_gate"]
    del data["date"]
    _write_manifest(tmp_path, data)
    code, lines = g4.check(tmp_path)
    assert code == 1
    assert any("missing required keys" in line for line in lines)


def test_block_when_tranche_id_does_not_match_filename(tmp_path):
    _write_manifest(tmp_path, _manifest("T-DEMO"), stem="T-OTHER")
    code, lines = g4.check(tmp_path)
    assert code == 1
    assert any("does not match the filename stem" in line for line in lines)


def test_block_on_bad_date(tmp_path):
    _write_manifest(tmp_path, _manifest(date="July 25 2026"))
    code, lines = g4.check(tmp_path)
    assert code == 1
    assert any("is not YYYY-MM-DD" in line for line in lines)


def test_pass_with_unquoted_yaml_dates(tmp_path):
    """Hand-authored manifests write `date: 2026-07-25`, which YAML parses as a
    date object; both that and the quoted string form are accepted."""
    path = tmp_path / g4.MANIFEST_DIR_RELPATH / "T-DATE.yaml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "schema: instruction-tranche-manifest/v1\n"
        "tranche_id: T-DATE\n"
        "title: Unquoted dates\n"
        "date: 2026-07-25\n"
        "instruction_surface_paths:\n"
        "  - tools/validation/demo.py\n"
        "m2_gate:\n"
        "  authorization: owner direction of record\n"
        "  authorized_by: Ryan Tufts\n"
        "  authorization_date: 2026-07-25\n"
        "  integration_owner: HELP_HUMAN (Agent 0)\n"
        "  merge_gate: human-gated-pr\n"
        "  self_merge: false\n"
        "m6_notice:\n"
        "  disposition: none-required\n"
        "  routed_to: []\n"
        "  rationale: nothing pins these surfaces\n",
        encoding="utf-8",
    )
    code, lines = g4.check(tmp_path)
    assert code == 0, lines


def test_block_on_machine_absolute_declared_path(tmp_path):
    _write_manifest(tmp_path, _manifest(instruction_surface_paths=["/etc/passwd"]))
    code, lines = g4.check(tmp_path)
    assert code == 1
    assert any("not a repo-relative POSIX path" in line for line in lines)


def test_dot_github_workflows_is_instruction_surface():
    """Regression: naive `lstrip('./')` ate the leading dot of `.github/`, so CI
    wiring silently read as non-protected."""
    assert g4.intersects_instruction_surface(".github/workflows/governance-harness.yml")
    assert g4.intersects_instruction_surface("./.github/workflows/x.yml")
    assert g4.intersects_instruction_surface("AGENTS.md")
    assert not g4.intersects_instruction_surface("execution/_Coordination/x.md")
    assert not g4.intersects_instruction_surface("projects/demo/docs/x.md")


def test_claude_md_is_instruction_surface():
    """D-GOV-26 item 2: `CLAUDE.md` is the session-init instruction pointer that
    imports `AGENTS.md`, so a change to it is an instruction-surface change."""
    assert g4.intersects_instruction_surface("CLAUDE.md")
    assert g4.intersects_instruction_surface("./CLAUDE.md")
    assert not g4.intersects_instruction_surface("projects/demo/CLAUDE.md")


def test_canonical_and_legacy_skill_roots_are_instruction_surfaces():
    assert g4.intersects_instruction_surface(".agents/skills/researcher/SKILL.md")
    assert g4.intersects_instruction_surface("./.agents/skills/researcher/execution.json")
    assert g4.intersects_instruction_surface("skills/historical/SKILL.md")
    assert not g4.intersects_instruction_surface("projects/demo/.agents/skills/local/SKILL.md")


def test_diff_mode_blocks_uncovered_claude_md_change(tmp_path):
    _init_repo(tmp_path)
    _write_manifest(
        tmp_path, _manifest(instruction_surface_paths=["docs/governance_harness/"])
    )
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-q", "-m", "manifest")
    base = _git(tmp_path, "rev-parse", "HEAD")
    (tmp_path / "CLAUDE.md").write_text("@AGENTS.md\n", encoding="utf-8")
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-q", "-m", "pointer")
    head = _git(tmp_path, "rev-parse", "HEAD")
    code, lines = g4.check(tmp_path, base, head)
    assert code == 1
    assert any("CLAUDE.md" in line for line in lines)
    assert any("is not covered by any declared tranche manifest path" in line for line in lines)


def test_diff_mode_pass_when_claude_md_change_is_covered(tmp_path):
    _init_repo(tmp_path)
    _write_manifest(tmp_path, _manifest(instruction_surface_paths=["CLAUDE.md"]))
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-q", "-m", "manifest")
    base = _git(tmp_path, "rev-parse", "HEAD")
    (tmp_path / "CLAUDE.md").write_text("@AGENTS.md\n", encoding="utf-8")
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-q", "-m", "pointer")
    head = _git(tmp_path, "rev-parse", "HEAD")
    code, lines = g4.check(tmp_path, base, head)
    assert code == 0, lines


def test_note_on_over_declared_non_instruction_path(tmp_path):
    _write_manifest(
        tmp_path,
        _manifest(instruction_surface_paths=["tools/validation/demo.py", "execution/x.md"]),
    )
    code, lines = g4.check(tmp_path)
    assert code == 0, lines
    assert any("over-declaration" in line for line in lines)


def test_block_on_unknown_merge_policy(tmp_path):
    data = _manifest()
    data["m2_gate"]["merge_gate"] = "auto-merge"
    _write_manifest(tmp_path, data)
    code, lines = g4.check(tmp_path)
    assert code == 1
    assert any("requires 'human-gated-pr'" in line for line in lines)


def _owner_direction(**overrides) -> dict:
    """A complete m2_gate.owner_direction block (PRD annex 5.3.1)."""
    data = {
        "directed_by": "Ryan Tufts",
        "direction_date": "2026-07-29",
        "approved_source_sha": "a" * 40,
    }
    data.update(overrides)
    return data


def test_block_on_self_merge(tmp_path):
    """The preserved failing mode: self_merge true with no direction declared."""
    data = _manifest()
    data["m2_gate"]["self_merge"] = True
    _write_manifest(tmp_path, data)
    code, lines = g4.check(tmp_path)
    assert code == 1
    assert any("forbids self-merge" in line for line in lines)


def test_pass_self_merge_with_complete_owner_direction(tmp_path):
    data = _manifest()
    data["m2_gate"]["self_merge"] = True
    data["m2_gate"]["owner_direction"] = _owner_direction()
    _write_manifest(tmp_path, data)
    code, lines = g4.check(tmp_path)
    assert code == 0, lines
    assert any("owner direction" in line and "Ryan Tufts" in line for line in lines)


def test_pass_owner_direction_with_self_merge_false(tmp_path):
    """A recorded direction does not require self_merge true; the default stands."""
    data = _manifest()
    data["m2_gate"]["owner_direction"] = _owner_direction()
    _write_manifest(tmp_path, data)
    code, lines = g4.check(tmp_path)
    assert code == 0, lines


def test_block_on_incomplete_owner_direction(tmp_path):
    data = _manifest()
    data["m2_gate"]["self_merge"] = True
    direction = _owner_direction()
    del direction["direction_date"]
    data["m2_gate"]["owner_direction"] = direction
    _write_manifest(tmp_path, data)
    code, lines = g4.check(tmp_path)
    assert code == 1
    assert any("owner_direction missing keys" in line for line in lines)
    assert any("forbids self-merge" in line for line in lines)


def test_block_on_malformed_direction_date(tmp_path):
    data = _manifest()
    data["m2_gate"]["self_merge"] = True
    data["m2_gate"]["owner_direction"] = _owner_direction(
        direction_date="July 29 2026"
    )
    _write_manifest(tmp_path, data)
    code, lines = g4.check(tmp_path)
    assert code == 1
    assert any("direction_date" in line and "not YYYY-MM-DD" in line for line in lines)


def test_block_on_malformed_direction_sha(tmp_path):
    data = _manifest()
    data["m2_gate"]["self_merge"] = True
    data["m2_gate"]["owner_direction"] = _owner_direction(approved_source_sha="abc123")
    _write_manifest(tmp_path, data)
    code, lines = g4.check(tmp_path)
    assert code == 1
    assert any("not a full 40-hex SHA" in line for line in lines)


def test_block_on_empty_directed_by(tmp_path):
    data = _manifest()
    data["m2_gate"]["self_merge"] = True
    data["m2_gate"]["owner_direction"] = _owner_direction(directed_by="   ")
    _write_manifest(tmp_path, data)
    code, lines = g4.check(tmp_path)
    assert code == 1
    assert any("directed_by must be a non-empty string" in line for line in lines)


def test_block_on_empty_authorization(tmp_path):
    data = _manifest()
    data["m2_gate"]["authorization"] = "   "
    _write_manifest(tmp_path, data)
    code, lines = g4.check(tmp_path)
    assert code == 1
    assert any("m2_gate.authorization must be a non-empty string" in line for line in lines)


def test_block_on_unknown_m6_disposition(tmp_path):
    data = _manifest()
    data["m6_notice"]["disposition"] = "later"
    _write_manifest(tmp_path, data)
    code, lines = g4.check(tmp_path)
    assert code == 1
    assert any("m6_notice.disposition" in line for line in lines)


def test_block_when_routed_names_no_notice(tmp_path):
    data = _manifest()
    data["m6_notice"]["disposition"] = "routed"
    _write_manifest(tmp_path, data)
    code, lines = g4.check(tmp_path)
    assert code == 1
    assert any("names no notice" in line for line in lines)


def test_block_when_routed_notice_missing(tmp_path):
    data = _manifest()
    data["m6_notice"]["disposition"] = "routed"
    data["m6_notice"]["routed_to"] = ["projects/demo/NOTICE.md"]
    _write_manifest(tmp_path, data)
    code, lines = g4.check(tmp_path)
    assert code == 1
    assert any("does not exist" in line for line in lines)


def test_pass_when_routed_notice_exists(tmp_path):
    notice = tmp_path / "projects" / "demo" / "NOTICE.md"
    notice.parent.mkdir(parents=True, exist_ok=True)
    notice.write_text("# notice\n", encoding="utf-8")
    data = _manifest()
    data["m6_notice"]["disposition"] = "routed"
    data["m6_notice"]["routed_to"] = ["projects/demo/NOTICE.md"]
    _write_manifest(tmp_path, data)
    code, lines = g4.check(tmp_path)
    assert code == 0, lines


def test_pass_when_missing_routed_notice_has_commit_pinned_external_route(tmp_path):
    data = _manifest()
    data["m6_notice"]["disposition"] = "routed"
    data["m6_notice"]["routed_to"] = ["domains/demo/NOTICE.md"]
    data["external_notice_routes"] = [
        {
            "source": "domains/demo/NOTICE.md",
            "repository": "example/private-domains",
            "path": "domains/demo/NOTICE.md",
            "commit": "a" * 40,
        }
    ]
    _write_manifest(tmp_path, data)
    code, lines = g4.check(tmp_path)
    assert code == 0, lines
    assert any("externalized to example/private-domains" in line for line in lines)


def test_block_when_external_route_is_not_commit_pinned(tmp_path):
    data = _manifest()
    data["m6_notice"]["disposition"] = "routed"
    data["m6_notice"]["routed_to"] = ["domains/demo/NOTICE.md"]
    data["external_notice_routes"] = [
        {
            "source": "domains/demo/NOTICE.md",
            "repository": "example/private-domains",
            "path": "domains/demo/NOTICE.md",
            "commit": "main",
        }
    ]
    _write_manifest(tmp_path, data)
    code, lines = g4.check(tmp_path)
    assert code == 1
    assert any("commit must be a full 40-hex SHA" in line for line in lines)


def test_pending_disposition_passes_with_note(tmp_path):
    data = _manifest()
    data["m6_notice"]["disposition"] = "pending"
    _write_manifest(tmp_path, data)
    code, lines = g4.check(tmp_path)
    assert code == 0, lines
    assert any("completed by the accepting agent at fan-in" in line for line in lines)


def test_block_on_unparseable_manifest(tmp_path):
    path = tmp_path / g4.MANIFEST_DIR_RELPATH / "T-BAD.yaml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("schema: [unterminated\n", encoding="utf-8")
    code, lines = g4.check(tmp_path)
    assert code == 1
    assert any("unparseable" in line for line in lines)


def test_diff_mode_pass_when_change_is_covered(tmp_path):
    _init_repo(tmp_path)
    _write_manifest(
        tmp_path,
        _manifest(instruction_surface_paths=["tools/validation/", "docs/governance_harness/"]),
    )
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-q", "-m", "manifest")
    base = _git(tmp_path, "rev-parse", "HEAD")
    tool = tmp_path / "tools" / "validation" / "demo.py"
    tool.parent.mkdir(parents=True, exist_ok=True)
    tool.write_text("# demo\n", encoding="utf-8")
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-q", "-m", "tool")
    head = _git(tmp_path, "rev-parse", "HEAD")
    code, lines = g4.check(tmp_path, base, head)
    assert code == 0, lines
    assert any("G4 PASS (diff mode)" in line for line in lines)


def test_diff_mode_blocks_uncovered_instruction_surface_change(tmp_path):
    _init_repo(tmp_path)
    _write_manifest(
        tmp_path, _manifest(instruction_surface_paths=["docs/governance_harness/"])
    )
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-q", "-m", "manifest")
    base = _git(tmp_path, "rev-parse", "HEAD")
    agents = tmp_path / "AGENTS.md"
    agents.write_text("# changed doctrine\n", encoding="utf-8")
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-q", "-m", "doctrine")
    head = _git(tmp_path, "rev-parse", "HEAD")
    code, lines = g4.check(tmp_path, base, head)
    assert code == 1
    assert any("is not covered by any declared tranche manifest path" in line for line in lines)


def test_candidate_range_diff_blocks_when_only_historical_manifest_covers_change(tmp_path):
    """CI must not let an old exact-path declaration stand in for this tranche."""
    _init_repo(tmp_path)
    _write_manifest(tmp_path, _manifest(instruction_surface_paths=["AGENTS.md"]))
    (tmp_path / "AGENTS.md").write_text("# original doctrine\n", encoding="utf-8")
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-q", "-m", "historical manifest")
    base = _git(tmp_path, "rev-parse", "HEAD")
    (tmp_path / "AGENTS.md").write_text("# changed doctrine\n", encoding="utf-8")
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-q", "-m", "unmanifested doctrine change")
    head = _git(tmp_path, "rev-parse", "HEAD")

    legacy_code, legacy_lines = g4.check(tmp_path, base, head)
    assert legacy_code == 0, legacy_lines

    result = _run_cli(
        tmp_path,
        "--base",
        base,
        "--head",
        head,
        "--added-manifests-only",
    )
    assert result.returncode == 1
    assert "G4 BLOCK (diff mode)" in result.stdout
    assert "adds no schema-readable tranche manifest" in result.stdout
    assert "AGENTS.md" in result.stdout


def test_candidate_range_diff_blocks_modified_historical_manifest_reuse(tmp_path):
    _init_repo(tmp_path)
    manifest = _write_manifest(
        tmp_path,
        _manifest(
            instruction_surface_paths=[
                "AGENTS.md",
                "docs/governance_harness/tranche_manifests/T-DEMO.yaml",
            ]
        ),
    )
    (tmp_path / "AGENTS.md").write_text("# original doctrine\n", encoding="utf-8")
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-q", "-m", "historical manifest")
    base = _git(tmp_path, "rev-parse", "HEAD")

    manifest.write_text(manifest.read_text(encoding="utf-8") + "# reused\n", encoding="utf-8")
    (tmp_path / "AGENTS.md").write_text("# changed doctrine\n", encoding="utf-8")
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-q", "-m", "reuse historical manifest")
    head = _git(tmp_path, "rev-parse", "HEAD")

    result = _run_cli(
        tmp_path,
        "--base",
        base,
        "--head",
        head,
        "--added-manifests-only",
    )
    assert result.returncode == 1
    assert "adds no schema-readable tranche manifest" in result.stdout
    assert "AGENTS.md" in result.stdout


def test_candidate_range_diff_passes_with_added_manifest(tmp_path):
    _init_repo(tmp_path)
    _write_manifest(tmp_path, _manifest("T-HISTORICAL"))
    (tmp_path / "AGENTS.md").write_text("# original doctrine\n", encoding="utf-8")
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-q", "-m", "historical state")
    base = _git(tmp_path, "rev-parse", "HEAD")

    _write_manifest(
        tmp_path,
        _manifest(
            "T-CANDIDATE",
            instruction_surface_paths=[
                "AGENTS.md",
                "docs/governance_harness/tranche_manifests/T-CANDIDATE.yaml",
            ],
        ),
    )
    (tmp_path / "AGENTS.md").write_text("# changed doctrine\n", encoding="utf-8")
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-q", "-m", "manifested doctrine change")
    head = _git(tmp_path, "rev-parse", "HEAD")

    result = _run_cli(
        tmp_path,
        "--base",
        base,
        "--head",
        head,
        "--added-manifests-only",
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "G4 PASS (diff mode)" in result.stdout
    assert "checked against 1 manifest(s)" in result.stdout


def test_candidate_range_diff_preserves_whole_corpus_schema_validation(tmp_path):
    _init_repo(tmp_path)
    _write_manifest(tmp_path, _manifest("T-HISTORICAL", schema="tranche/v0"))
    (tmp_path / "AGENTS.md").write_text("# original doctrine\n", encoding="utf-8")
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-q", "-m", "invalid historical state")
    base = _git(tmp_path, "rev-parse", "HEAD")

    _write_manifest(
        tmp_path,
        _manifest(
            "T-CANDIDATE",
            instruction_surface_paths=[
                "AGENTS.md",
                "docs/governance_harness/tranche_manifests/T-CANDIDATE.yaml",
            ],
        ),
    )
    (tmp_path / "AGENTS.md").write_text("# changed doctrine\n", encoding="utf-8")
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-q", "-m", "manifested doctrine change")
    head = _git(tmp_path, "rev-parse", "HEAD")

    result = _run_cli(
        tmp_path,
        "--base",
        base,
        "--head",
        head,
        "--added-manifests-only",
    )
    assert result.returncode == 1
    assert "manifest T-HISTORICAL.yaml: schema is 'tranche/v0'" in result.stdout


def test_candidate_range_diff_ignores_non_instruction_change_without_new_manifest(tmp_path):
    _init_repo(tmp_path)
    _write_manifest(tmp_path, _manifest())
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-q", "-m", "historical manifest")
    base = _git(tmp_path, "rev-parse", "HEAD")
    record = tmp_path / "execution" / "_Coordination" / "RECORD.md"
    record.parent.mkdir(parents=True, exist_ok=True)
    record.write_text("# record\n", encoding="utf-8")
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-q", "-m", "coordination only")
    head = _git(tmp_path, "rev-parse", "HEAD")

    result = _run_cli(
        tmp_path,
        "--base",
        base,
        "--head",
        head,
        "--added-manifests-only",
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "0 on the instruction surface, checked against 0 manifest(s)" in result.stdout


def test_diff_mode_ignores_non_instruction_surface_change(tmp_path):
    _init_repo(tmp_path)
    _write_manifest(tmp_path, _manifest())
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-q", "-m", "manifest")
    base = _git(tmp_path, "rev-parse", "HEAD")
    record = tmp_path / "execution" / "_Coordination" / "RECORD.md"
    record.parent.mkdir(parents=True, exist_ok=True)
    record.write_text("# record\n", encoding="utf-8")
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-q", "-m", "record")
    head = _git(tmp_path, "rev-parse", "HEAD")
    code, lines = g4.check(tmp_path, base, head)
    assert code == 0, lines


def test_diff_mode_operational_on_unknown_tranche(tmp_path):
    _init_repo(tmp_path)
    _write_manifest(tmp_path, _manifest())
    code, lines = g4.check(tmp_path, "HEAD", "HEAD", tranche="T-NOT-DECLARED")
    assert code == 2
    assert any("no manifest declares tranche_id" in line for line in lines)


def test_diff_mode_operational_on_bad_refs(tmp_path):
    _init_repo(tmp_path)
    _write_manifest(tmp_path, _manifest())
    code, lines = g4.check(tmp_path, "no-such-ref", "HEAD")
    assert code == 2
    assert any("OPERATIONAL" in line for line in lines)


def test_cli_rejects_half_specified_diff_mode():
    assert g4.main(["--base", "HEAD~1"]) == 2


def test_cli_rejects_candidate_range_selection_without_diff_mode():
    assert g4.main(["--added-manifests-only"]) == 2


def test_cli_rejects_tranche_and_candidate_range_selection_together():
    assert (
        g4.main(
            [
                "--base",
                "HEAD",
                "--head",
                "HEAD",
                "--tranche",
                "T-DEMO",
                "--added-manifests-only",
            ]
        )
        == 2
    )


def test_governance_harness_ci_wires_candidate_range_diff_mode():
    workflow = (
        g4.repo_root() / ".github" / "workflows" / "governance-harness.yml"
    ).read_text(encoding="utf-8")
    assert (
        "G4_BASE_REF: ${{ github.event.pull_request.base.sha || github.event.before }}"
        in workflow
    )
    assert '--base "${G4_BASE_REF}" --head HEAD --added-manifests-only' in workflow
    assert "--base HEAD^ --head HEAD --added-manifests-only" in workflow


def test_live_repo_lane_b_manifest_exists_and_passes():
    """The G4 discipline applied to itself: this tranche's own manifest must be
    present and schema-valid in the live checkout (packet §5.3 G4)."""
    root = g4.repo_root()
    manifest = root / g4.MANIFEST_DIR_RELPATH / "ROOT-LANE-B-20260725.yaml"
    assert manifest.is_file()
    code, lines = g4.check(root)
    assert code == 0, lines
    assert any("ROOT-LANE-B-20260725" in line for line in lines)


def test_standing_owner_authorization_needs_no_per_merge_sha(tmp_path):
    data = _manifest()
    data["m2_gate"].update(merge_gate="owner-authorized-pr", self_merge=True)
    _write_manifest(tmp_path, data)
    code, lines = g4.check(tmp_path)
    assert code == 0, lines
    assert "owner_direction" not in data["m2_gate"]


def test_standing_authorization_still_requires_recorded_scope_authority(tmp_path):
    data = _manifest()
    data["m2_gate"].update(merge_gate="owner-authorized-pr", self_merge=True, authorization="")
    _write_manifest(tmp_path, data)
    code, lines = g4.check(tmp_path)
    assert code == 1
    assert any("m2_gate.authorization must be a non-empty string" in line for line in lines)


def test_standing_authorization_rejects_non_boolean_self_merge(tmp_path):
    data = _manifest()
    data["m2_gate"].update(merge_gate="owner-authorized-pr", self_merge="yes")
    _write_manifest(tmp_path, data)
    code, lines = g4.check(tmp_path)
    assert code == 1


def test_malformed_merge_policy_returns_block_instead_of_crashing(tmp_path):
    for value in (["owner-authorized-pr"], {"mode": "owner-authorized-pr"}):
        data = _manifest()
        data["m2_gate"]["merge_gate"] = value
        _write_manifest(tmp_path, data)
        code, lines = g4.check(tmp_path)
        assert code == 1
        assert any("m2_gate.merge_gate" in line for line in lines)
