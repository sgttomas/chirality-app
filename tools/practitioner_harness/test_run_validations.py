#!/usr/bin/env python3
"""Phase 4 run-validations tests: the mutation-control contract, evidence
records (practitioner-harness-evidence/v1), and the CLI wiring.

Fixture idiom per test_brief_adoption.py: tmp git repos built from string
constants inside this test module (fixture allowlist actor on every
adoption-claiming brief). Every declared validation command in these
fixtures is HARMLESS (`echo …`, `python3 -c …`); the real pilot manifests'
npm/pytest commands are never executed here.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

import cmd_run_validations
import evidence_records
import harness
import harness_template_cache
from harness_common import (
    GENERATED_ROOT_NAME,
    HarnessOperationalError,
    Severity,
    compute_exit_code,
)
from test_brief_adoption import FIXTURE_ACTORS_MD, _git
from test_self_check_fixtures import _write

requires_git = pytest.mark.skipif(shutil.which("git") is None,
                                  reason="git not available")

TID = "TRB-val-001"
BRIEF_RELPATH = "docs/governance_harness/briefs/TRB-val-001.md"
PROJECT_REL = "projects/chirality-piping"
DECLARED_IN = PROJECT_REL + "/_harness/adapter.yaml"

# All schema fields the shared evidence-record contract prescribes.
RECORD_FIELDS = {
    "schema", "tranche_id", "brief_source_path", "brief_state",
    "brief_bound_sha", "fence_active", "command", "cwd", "declared_in",
    "exit_code", "timed_out", "duration_seconds", "captured_at",
    "tool_versions", "stdout", "stdout_truncated", "stderr",
    "stderr_truncated", "pre_run_porcelain", "post_run_porcelain",
    "changed_paths", "disclaimer",
}

ADAPTER_TEMPLATE = '''# Harness configuration authority only (fixture).
schema: practitioner-harness-adapter/v1
project: chirality-piping
plan: docs/PLAN.md
coordination: execution/_Coordination/_COORDINATION.md
decision_register: execution/_Coordination/_DECISIONS/_REGISTER.md
dag_pointer: execution/_DAG/_LATEST.md
status_glob: "execution/PKG-*/1_Working/*/_STATUS.md"
states: [OPEN, INITIALIZED, SEMANTIC_READY, IN_PROGRESS, CHECKING, ISSUED]
parser_dialect: prose-bullet-v1
drift_baseline_mismatch: 0
drift_baseline_files: 0
validation_commands:
{commands}
'''

BRIEF_TEMPLATE = '''# Tranche brief {tid} — {state}

- tranche_id: `{tid}`
- state: {state}
- objective: fixture objective — stated by the fixture author
- adopted_by: {adopted_by}
- adopted_on: 2026-07-02

## read_scope

- `{write_scope}`

## write_scope

- `{write_scope}`

## prohibited_paths

- `docs/**`

## validations (declared, not run)

{validation_lines}

## evidence_targets

{evidence_target_lines}

## stop_conditions

- an out-of-scope write attempt

## human_decision_points

- adoption of this brief itself (D-GOV-04)

---

Footer fixture: the cited sources govern on any disagreement.
'''


def _yaml_commands(commands: list[dict]) -> str:
    lines = []
    for vc in commands:
        cwd = vc.get("cwd", ".")
        lines.append(f"  - {{cwd: \"{cwd}\", command: '{vc['command']}'}}")
    return "\n".join(lines)


def build_run_repo(
    tmp_path: Path,
    commands: list[dict],
    *,
    brief_state: str = "HUMAN_ADOPTED",
    adopted_by: str = "fixture-owner",
    with_allowlist: bool = True,
    gitignore_extra: str = "",
    brief_validation_lines: list[str] | None = None,
    write_scope: str = PROJECT_REL + "/execution/DEL-01-01/**",
    evidence_target_lines: list[str] | None = None,
) -> Path:
    """Tmp git repo: fixture allowlist, one pilot project with a manifest
    declaring HARMLESS validation commands, one committed brief, one tracked
    governed file the mutation tests can touch.

    Repos with identical build parameters are built once per session and
    copied per test (harness_template_cache); tests mutate their own copy."""
    if brief_validation_lines is None:
        brief_validation_lines = [
            f"- {vc['command']} (cwd: {vc.get('cwd', '.')}) — declared in "
            "the adapter manifest; NOT run by this command"
            for vc in commands
        ] or ["- none declared"]
    if evidence_target_lines is None:
        evidence_target_lines = [
            f"- `{GENERATED_ROOT_NAME}/evidence/{TID}/` (under the declared "
            "generated root; D-GOV-01)"]
    key = ("run_repo", json.dumps(commands, sort_keys=True), brief_state,
           adopted_by, with_allowlist, gitignore_extra,
           tuple(brief_validation_lines), write_scope,
           tuple(evidence_target_lines))

    def _build(repo: Path) -> None:
        _write(repo / ".gitignore", GENERATED_ROOT_NAME + "/\n" + gitignore_extra)
        if with_allowlist:
            _write(repo / "docs" / "governance_harness" / "human_actors.md",
                   FIXTURE_ACTORS_MD)
        _write(repo / PROJECT_REL / "_harness" / "adapter.yaml",
               ADAPTER_TEMPLATE.format(commands=_yaml_commands(commands)))
        _write(repo / PROJECT_REL / "tracked.md", "governed fixture file\n")
        _write(repo / BRIEF_RELPATH, BRIEF_TEMPLATE.format(
            tid=TID, state=brief_state, adopted_by=adopted_by,
            write_scope=write_scope,
            validation_lines="\n".join(brief_validation_lines),
            evidence_target_lines="\n".join(evidence_target_lines)))
        _git(repo, "init", "-q")
        _git(repo, "add", "-A")
        _git(repo, "commit", "-q", "-m", "fixture repo")

    return harness_template_cache.materialize(key, _build, tmp_path / "repo")


def _run_direct(repo: Path, timeout_seconds: int = 60, list_only: bool = False):
    return cmd_run_validations.run_run_validations(
        repo, repo / BRIEF_RELPATH, repo / GENERATED_ROOT_NAME,
        timeout_seconds=timeout_seconds, list_only=list_only,
        alias_by_root=harness._alias_by_root(repo))


def _record_files(repo: Path, suffix: str = ".json") -> list[Path]:
    records_dir = repo / GENERATED_ROOT_NAME / "evidence" / TID
    if not records_dir.is_dir():
        return []
    return sorted(records_dir.glob("*" + suffix))


def _findings(report, code):
    return [f for f in report.findings if f.code == code]


# --- (a) happy path -----------------------------------------------------------------

@requires_git
def test_happy_path_two_commands_two_records_exit_0(tmp_path, capsys):
    repo = build_run_repo(tmp_path, [
        {"cwd": ".", "command": "echo happy-one"},
        {"cwd": ".", "command": 'python3 -c "print(42)"'},
    ])
    rc = harness.main(["--repo-root", str(repo), "run-validations",
                       "--brief", BRIEF_RELPATH, "--timeout-seconds", "60"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "VALIDATION_MUTATED_GOVERNED_FILES" not in out
    assert "structural evidence only" in out

    jsons = _record_files(repo)
    assert [p.name for p in jsons] == [
        "001_echo_happy_one.json", "001_python3_c_print_42.json"]
    mds = _record_files(repo, ".md")
    assert [p.name for p in mds] == [
        "001_echo_happy_one.md", "001_python3_c_print_42.md"]

    echo_rec = json.loads(jsons[0].read_text(encoding="utf-8"))
    assert RECORD_FIELDS <= set(echo_rec)
    assert echo_rec["schema"] == "practitioner-harness-evidence/v1"
    assert echo_rec["tranche_id"] == TID
    assert echo_rec["brief_source_path"] == BRIEF_RELPATH
    assert echo_rec["brief_state"] == "HUMAN_ADOPTED"
    assert echo_rec["fence_active"] is True
    assert echo_rec["brief_bound_sha"] == _git(
        repo, "log", "-1", "--format=%H", "--", BRIEF_RELPATH)
    assert echo_rec["command"] == "echo happy-one"
    assert echo_rec["cwd"] == "."
    assert echo_rec["declared_in"] == DECLARED_IN
    assert echo_rec["exit_code"] == 0 and echo_rec["timed_out"] is False
    assert "happy-one" in echo_rec["stdout"]
    assert echo_rec["stdout_truncated"] is False
    assert echo_rec["duration_seconds"] >= 0
    assert "T" in echo_rec["captured_at"]  # ISO-8601 UTC
    assert isinstance(echo_rec["pre_run_porcelain"], list)
    assert isinstance(echo_rec["post_run_porcelain"], list)
    assert echo_rec["disclaimer"].startswith("Generated view — not authority.")

    py_rec = json.loads(jsons[1].read_text(encoding="utf-8"))
    assert "python3" in py_rec["tool_versions"]  # cheap probe, keyed on token
    assert "42" in py_rec["stdout"]

    # The md sibling carries the standard generated header + self-exclusion.
    md_text = mds[0].read_text(encoding="utf-8")
    assert "Generated view — not authority" in md_text
    assert "two-class self-exclusion" in md_text

    # The reader round-trips both as PARSED facts for this tranche.
    loaded = evidence_records.load_evidence_records(
        repo, repo / GENERATED_ROOT_NAME, TID)
    assert [r.parse_status for r in loaded] == ["PARSED", "PARSED"]


# --- (b) tracked-file mutation -> unconditional BLOCK -------------------------------

@requires_git
def test_tracked_file_mutation_blocks_and_record_still_written(tmp_path, capsys):
    repo = build_run_repo(tmp_path, [
        {"cwd": ".", "command": "echo mutated >> tracked.md"},
    ])
    rc = harness.main(["--repo-root", str(repo), "run-validations",
                       "--brief", BRIEF_RELPATH])
    assert rc == 1
    out = capsys.readouterr().out
    assert "VALIDATION_MUTATED_GOVERNED_FILES" in out
    assert "K-WRITE-2" in out
    # The record is still written, carrying the classification.
    jsons = _record_files(repo)
    assert len(jsons) == 1
    record = json.loads(jsons[0].read_text(encoding="utf-8"))
    assert {"path": PROJECT_REL + "/tracked.md",
            "classification": "unexpected_tracked_change"} in record["changed_paths"]


@requires_git
def test_mutation_block_is_unconditional_even_without_active_fence(tmp_path):
    # BLOCK discipline: governed-file mutation protects the substrate, not
    # the fence — the D-GOV-04 adoption cap never applies to it.
    repo = build_run_repo(tmp_path, [
        {"cwd": ".", "command": "echo mutated >> tracked.md"},
    ], brief_state="CANDIDATE", adopted_by="TBD — placeholder")
    report = _run_direct(repo)
    blocks = _findings(report, "VALIDATION_MUTATED_GOVERNED_FILES")
    assert len(blocks) == 1 and blocks[0].severity is Severity.BLOCK
    assert "adoption cap does not apply" in blocks[0].message
    assert compute_exit_code(report.findings) == 1
    fences = _findings(report, "VALIDATION_RUN_WITHOUT_ACTIVE_FENCE")
    assert len(fences) == 1 and fences[0].severity is Severity.REVIEW


# --- (b2) the evidence_targets exemption is fence-gated (K-WRITE-2 / D-GOV-04) ------

@requires_git
def test_unadopted_brief_evidence_targets_exempt_nothing(tmp_path, capsys):
    # run-validations deliberately runs on CANDIDATE/unadopted briefs, and a
    # brief's evidence_targets are agent-authorable text until a human
    # adopts the brief — so a CANDIDATE brief declaring a broad governed
    # evidence_target must NOT swallow governed-file mutations: the
    # unconditional mutation BLOCK is not suppressible by anything
    # agent-authored (K-WRITE-2; D-GOV-04).
    repo = build_run_repo(tmp_path, [
        {"cwd": ".", "command": "echo mutated >> tracked.md"},
    ], brief_state="CANDIDATE", adopted_by="TBD — placeholder",
        evidence_target_lines=[
            f"- `{PROJECT_REL}/**` (fixture: agent-declared broad target "
            "over a governed tree)"])
    rc = harness.main(["--repo-root", str(repo), "run-validations",
                       "--brief", BRIEF_RELPATH])
    assert rc == 1
    out = capsys.readouterr().out
    assert "VALIDATION_MUTATED_GOVERNED_FILES" in out
    record = json.loads(_record_files(repo)[0].read_text(encoding="utf-8"))
    assert {"path": PROJECT_REL + "/tracked.md",
            "classification": "unexpected_tracked_change"} in record["changed_paths"]


@requires_git
def test_adopted_brief_evidence_target_exempts_declared_governed_path(tmp_path):
    # The SAME write under a HUMAN_ADOPTED+committed brief whose
    # evidence_targets cover the path: a human adopted those targets
    # (D-GOV-04), so the changed path classifies as
    # expected_evidence_output — no BLOCK.
    repo = build_run_repo(tmp_path, [
        {"cwd": ".", "command": "echo mutated >> tracked.md"},
    ], evidence_target_lines=[
        f"- `{PROJECT_REL}/**` (fixture: human-adopted evidence target)"])
    report = _run_direct(repo)
    assert report.summary["fence_active"] is True
    assert not _findings(report, "VALIDATION_MUTATED_GOVERNED_FILES")
    assert compute_exit_code(report.findings) == 0
    record = json.loads(_record_files(repo)[0].read_text(encoding="utf-8"))
    assert {"path": PROJECT_REL + "/tracked.md",
            "classification": "expected_evidence_output"} in record["changed_paths"]


# --- (b3) already-dirty tracked files: content fingerprints, not status codes -------

@requires_git
def test_predirty_tracked_file_mutated_further_blocks(tmp_path, capsys):
    # A tracked file already " M" before the run keeps " M" when a command
    # appends to it — invisible to status-code diffing alone; the content
    # fingerprint comparison catches the mutation (K-WRITE-2).
    repo = build_run_repo(tmp_path, [
        {"cwd": ".", "command": "echo mutated-further >> tracked.md"},
    ])
    (repo / PROJECT_REL / "tracked.md").write_text(
        "governed fixture file\npre-dirty human edit\n", encoding="utf-8")
    rc = harness.main(["--repo-root", str(repo), "run-validations",
                       "--brief", BRIEF_RELPATH])
    assert rc == 1
    out = capsys.readouterr().out
    assert "VALIDATION_MUTATED_GOVERNED_FILES" in out
    record = json.loads(_record_files(repo)[0].read_text(encoding="utf-8"))
    assert {"path": PROJECT_REL + "/tracked.md",
            "classification": "unexpected_tracked_change"} in record["changed_paths"]


@requires_git
def test_predirty_tracked_file_untouched_is_not_flagged(tmp_path):
    # No false positive: the pre-dirty file's content fingerprints agree
    # pre/post when the command never touches it.
    repo = build_run_repo(tmp_path, [
        {"cwd": ".", "command": "echo untouched"},
    ])
    (repo / PROJECT_REL / "tracked.md").write_text(
        "governed fixture file\npre-dirty human edit\n", encoding="utf-8")
    report = _run_direct(repo)
    assert not _findings(report, "VALIDATION_MUTATED_GOVERNED_FILES")
    assert compute_exit_code(report.findings) == 0
    record = json.loads(_record_files(repo)[0].read_text(encoding="utf-8"))
    assert record["changed_paths"] == []


# --- (c) gitignored cache write -> ignored_cache, no BLOCK --------------------------

@requires_git
def test_gitignored_cache_write_is_ignored_cache_not_block(tmp_path):
    repo = build_run_repo(tmp_path, [
        {"cwd": ".", "command": "echo data > out.cachefile"},
    ], gitignore_extra="*.cachefile\n")
    report = _run_direct(repo)
    assert compute_exit_code(report.findings) == 0
    assert not _findings(report, "VALIDATION_MUTATED_GOVERNED_FILES")
    assert not _findings(report, "VALIDATION_UNTRACKED_OUTPUT")
    record = json.loads(_record_files(repo)[0].read_text(encoding="utf-8"))
    assert {"path": PROJECT_REL + "/out.cachefile",
            "classification": "ignored_cache"} in record["changed_paths"]
    # Surfaced as an INFO-class fact, not a finding.
    facts = [f for f in report.facts
             if f.fact_id == "run_validations.ignored_cache"]
    assert [f.value for f in facts] == [PROJECT_REL + "/out.cachefile"]


# --- (d) new untracked output -> REVIEW (0 default, 1 strict) -----------------------

@requires_git
def test_untracked_output_is_review_0_default_1_strict(tmp_path, capsys):
    repo = build_run_repo(tmp_path, [
        {"cwd": ".", "command": "echo stray > stray_output.txt"},
    ])
    rc = harness.main(["--repo-root", str(repo), "run-validations",
                       "--brief", BRIEF_RELPATH])
    assert rc == 0
    assert "VALIDATION_UNTRACKED_OUTPUT" in capsys.readouterr().out
    record = json.loads(_record_files(repo)[0].read_text(encoding="utf-8"))
    assert {"path": PROJECT_REL + "/stray_output.txt",
            "classification": "review_required_untracked"} in record["changed_paths"]
    # Remove the stray so the strict rerun observes the same NEW entry.
    (repo / PROJECT_REL / "stray_output.txt").unlink()
    rc = harness.main(["--repo-root", str(repo), "--strict", "run-validations",
                       "--brief", BRIEF_RELPATH])
    assert rc == 1
    capsys.readouterr()


# --- (e) timeout -> TIMED_OUT, exit_code null, never an invented outcome ------------

@requires_git
def test_timeout_recorded_as_timed_out_never_inferred(tmp_path):
    repo = build_run_repo(tmp_path, [
        {"cwd": ".", "command": 'python3 -c "import time; time.sleep(5)"'},
    ])
    report = _run_direct(repo, timeout_seconds=1)
    record = json.loads(_record_files(repo)[0].read_text(encoding="utf-8"))
    assert record["timed_out"] is True
    assert record["exit_code"] is None  # json null — never guessed
    md = report.render_markdown()
    assert "TIMED_OUT" in md
    assert "exit 0" not in md.split("## Runs")[1].split("##")[0]
    hits = _findings(report, "VALIDATION_COMMAND_TIMED_OUT")
    assert len(hits) == 1 and hits[0].severity is Severity.WARN
    assert compute_exit_code(report.findings) == 0
    # The md record sibling labels the outcome too.
    md_record = _record_files(repo, ".md")[0].read_text(encoding="utf-8")
    assert "TIMED_OUT" in md_record and "never" in md_record


# --- (f) --list runs nothing, writes nothing ----------------------------------------

@requires_git
def test_list_mode_runs_nothing_writes_nothing(tmp_path, capsys):
    repo = build_run_repo(tmp_path, [
        {"cwd": ".", "command": "echo listed > must_not_exist.txt"},
    ])
    rc = harness.main(["--repo-root", str(repo), "run-validations",
                       "--brief", BRIEF_RELPATH, "--list"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "echo listed > must_not_exist.txt" in out
    assert DECLARED_IN in out
    assert "nothing was executed and nothing was written" in out
    assert not (repo / PROJECT_REL / "must_not_exist.txt").exists()
    assert not (repo / GENERATED_ROOT_NAME).exists()  # no evidence dir at all


# --- (g) candidate brief: commands still run, capped semantics ----------------------

@requires_git
def test_candidate_brief_runs_with_review_and_inactive_fence_records(tmp_path):
    repo = build_run_repo(tmp_path, [
        {"cwd": ".", "command": "echo candidate-run"},
    ], brief_state="CANDIDATE", adopted_by="TBD — placeholder")
    report = _run_direct(repo)
    hits = _findings(report, "VALIDATION_RUN_WITHOUT_ACTIVE_FENCE")
    assert len(hits) == 1 and hits[0].severity is Severity.REVIEW
    assert "D-GOV-04" in hits[0].message
    assert "D-GOV-04" in hits[0].caveat  # the fence's cap_reason, recorded
    assert compute_exit_code(report.findings) == 0
    record = json.loads(_record_files(repo)[0].read_text(encoding="utf-8"))
    assert record["fence_active"] is False
    assert record["brief_state"] == "CANDIDATE"
    assert record["brief_bound_sha"] == ""
    assert "candidate-run" in record["stdout"]  # the command DID run


# --- (h) identity refusal: exit 2, nothing executed ---------------------------------

@requires_git
def test_identity_refusal_exits_2_and_executes_nothing(tmp_path, capsys):
    repo = build_run_repo(tmp_path, [
        {"cwd": ".", "command": "echo executed > refusal_marker.txt"},
    ], adopted_by="Some Stranger")
    rc = harness.main(["--repo-root", str(repo), "run-validations",
                       "--brief", BRIEF_RELPATH])
    assert rc == 2
    captured = capsys.readouterr()
    assert "D-GOV-04" in captured.err
    assert "no evidence record" in captured.out
    assert not (repo / PROJECT_REL / "refusal_marker.txt").exists()
    assert not (repo / GENERATED_ROOT_NAME / "evidence").exists()
    assert evidence_records.load_evidence_records(
        repo, repo / GENERATED_ROOT_NAME, TID) == []


# --- (i) stream truncation is explicit ----------------------------------------------

@requires_git
def test_stdout_over_200kb_is_truncated_with_marker(tmp_path):
    repo = build_run_repo(tmp_path, [
        {"cwd": ".",
         "command": 'python3 -c "import sys; sys.stdout.write(300000*chr(120))"'},
    ])
    _run_direct(repo)
    record = json.loads(_record_files(repo)[0].read_text(encoding="utf-8"))
    assert record["stdout_truncated"] is True
    assert record["stdout"].endswith(evidence_records.TRUNCATION_MARKER)
    assert len(record["stdout"].encode("utf-8")) < 300_000
    assert record["stderr_truncated"] is False


# --- (j) declaration drift: manifest governs ----------------------------------------

@requires_git
def test_declaration_drift_is_warn_manifest_governs(tmp_path):
    repo = build_run_repo(
        tmp_path,
        [{"cwd": ".", "command": "echo drift-cmd"}],
        brief_validation_lines=[
            "- pytest -q phantom (cwd: .) — declared in the adapter "
            "manifest; NOT run by this command"],
    )
    report = _run_direct(repo)
    hits = _findings(report, "VALIDATION_DECLARATION_DRIFT")
    assert len(hits) == 2  # manifest command not in brief text + vice versa
    assert all(h.severity is Severity.WARN for h in hits)
    assert all("adapter manifest governs" in h.message for h in hits)
    messages = " ".join(h.message for h in hits)
    assert "echo drift-cmd" in messages and "pytest -q phantom" in messages
    # The manifest-declared command still ran (it is the config authority).
    assert len(_record_files(repo)) == 1
    assert compute_exit_code(report.findings) == 0


# --- project resolution refuses rather than guesses ---------------------------------

@requires_git
def test_write_scope_outside_pilot_roots_is_operational_error(tmp_path, capsys):
    repo = build_run_repo(tmp_path, [
        {"cwd": ".", "command": "echo never-runs"},
    ], write_scope="elsewhere/nowhere/DEL-01-01/**")
    with pytest.raises(HarnessOperationalError) as exc:
        _run_direct(repo)
    assert "elsewhere/nowhere/DEL-01-01/**" in str(exc.value)
    rc = harness.main(["--repo-root", str(repo), "run-validations",
                       "--brief", BRIEF_RELPATH])
    assert rc == 2
    assert "ERROR" in capsys.readouterr().err
    assert not (repo / GENERATED_ROOT_NAME / "evidence").exists()


# --- evidence_records unit coverage --------------------------------------------------

def test_slug_and_ordinal_helpers(tmp_path):
    assert evidence_records.slug_for_command("echo happy-one") == "echo_happy_one"
    assert evidence_records.slug_for_command(
        'python3 -c "print(42)"') == "python3_c_print_42"
    assert evidence_records.slug_for_command("///") == "command"
    records_dir = tmp_path / "records"
    assert evidence_records.next_ordinal(records_dir, "echo_x") == 1
    records_dir.mkdir()
    (records_dir / "001_echo_x.json").write_text("{}", encoding="utf-8")
    (records_dir / "003_echo_x.json").write_text("{}", encoding="utf-8")
    (records_dir / "001_other.json").write_text("{}", encoding="utf-8")
    assert evidence_records.next_ordinal(records_dir, "echo_x") == 4
    assert evidence_records.next_ordinal(records_dir, "other") == 2


def test_truncate_stream_cap_and_marker():
    text, truncated = evidence_records.truncate_stream("short")
    assert (text, truncated) == ("short", False)
    text, truncated = evidence_records.truncate_stream("x" * 300_000)
    assert truncated is True
    assert text.endswith(evidence_records.TRUNCATION_MARKER)


def test_loader_labels_unparseable_never_crashes(tmp_path):
    repo = tmp_path / "repo"
    out_dir = repo / GENERATED_ROOT_NAME
    record = evidence_records.build_evidence_record(
        tranche_id=TID, brief_source_path=BRIEF_RELPATH,
        brief_state="HUMAN_ADOPTED", brief_bound_sha="abc123",
        fence_active=True, command="echo ok", cwd=".",
        declared_in=DECLARED_IN, exit_code=0, timed_out=False,
        duration_seconds=0.01, tool_versions={}, stdout="ok\n", stderr="",
        pre_run_porcelain=[], post_run_porcelain=[], changed_paths=[])
    evidence_records.write_evidence_record(record, out_dir, repo)
    records_dir = out_dir / "evidence" / TID
    _write(records_dir / "junk.json", "not json at all")
    _write(records_dir / "foreign.json",
           json.dumps({"schema": "someone-else/v9", "tranche_id": TID}))
    loaded = evidence_records.load_evidence_records(repo, out_dir, TID)
    by_status = {r.path.rsplit("/", 1)[-1]: r for r in loaded}
    assert by_status["001_echo_ok.json"].parse_status == "PARSED"
    assert by_status["001_echo_ok.json"].record["exit_code"] == 0
    assert by_status["junk.json"].parse_status == "UNPARSEABLE"
    assert "non-JSON" in by_status["junk.json"].note
    assert by_status["foreign.json"].parse_status == "UNPARSEABLE"
    assert "someone-else/v9" in by_status["foreign.json"].note
    # Missing directory: empty list, never a crash.
    assert evidence_records.load_evidence_records(
        repo, out_dir, "TRB-absent-999") == []


def test_evidence_record_carries_gen3_generated_view_marker(tmp_path):
    """Regression (bridge Loop 1, 2026-07-02): self-check GEN-3 BLOCKed the
    harness's own evidence JSONs (GENERATED_DISCLAIMER_MISSING) because the
    records lacked the `"authority_class": "generated_view"` marker that
    Report.to_json_dict envelopes carry."""
    from cmd_self_check import GENERATED_HEADER_SENTINEL

    repo = tmp_path / "repo"
    out_dir = repo / GENERATED_ROOT_NAME
    record = evidence_records.build_evidence_record(
        tranche_id=TID, brief_source_path=BRIEF_RELPATH,
        brief_state="HUMAN_ADOPTED", brief_bound_sha="abc123",
        fence_active=True, command="echo ok", cwd=".",
        declared_in=DECLARED_IN, exit_code=0, timed_out=False,
        duration_seconds=0.01, tool_versions={}, stdout="ok\n", stderr="",
        pre_run_porcelain=[], post_run_porcelain=[], changed_paths=[])
    assert record["authority_class"] == "generated_view"
    json_path, md_path = evidence_records.write_evidence_record(
        record, out_dir, repo)
    # The exact substring GEN-3 accepts for .json files under the generated
    # root (cmd_self_check GEN-3 labeling check).
    assert '"authority_class": "generated_view"' in json_path.read_text(
        encoding="utf-8")
    # The md summary carries the generated-view header sentinel.
    assert GENERATED_HEADER_SENTINEL in md_path.read_text(encoding="utf-8")
