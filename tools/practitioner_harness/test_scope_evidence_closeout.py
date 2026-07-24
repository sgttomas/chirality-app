#!/usr/bin/env python3
"""Phase 4 tests for scope-check, evidence-check, and closeout-digest: the
fence matcher, the two-and-only-two BLOCK conditions (only the scope-check
one lives here; the mutation BLOCK is covered in test_run_validations),
D-GOV-08 Option B evidence completeness, and the composed digest.

Fixture idiom per test_run_validations.py: tmp git repos from string
constants; every declared validation command is harmless (`echo …`); the
real pilot manifests are never executed.
"""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

import cmd_closeout
import cmd_evidence_check
import cmd_scope_check
import evidence_records
import harness
import scope_fence
from harness_common import (
    GENERATED_ROOT_NAME,
    HarnessOperationalError,
    Severity,
    compute_exit_code,
    find_claim_language,
)
from test_brief_adoption import _git
from test_run_validations import (
    ADAPTER_TEMPLATE,
    BRIEF_RELPATH,
    DECLARED_IN,
    PROJECT_REL,
    TID,
    _yaml_commands,
    build_run_repo,
)
from test_self_check_fixtures import _write

requires_git = pytest.mark.skipif(shutil.which("git") is None,
                                  reason="git not available")

ECHO_CMD = {"cwd": ".", "command": "echo happy-one"}
IN_FENCE_REL = PROJECT_REL + "/execution/DEL-01-01/notes.md"
OUT_OF_FENCE_REL = PROJECT_REL + "/stray_governed.md"


# --- helpers -------------------------------------------------------------------

def _head(repo: Path) -> str:
    return _git(repo, "rev-parse", "HEAD")


def _commit_file(repo: Path, relpath: str, text: str = "fixture content\n",
                 message: str = "fixture commit") -> None:
    _write(repo / relpath, text)
    _git(repo, "add", relpath)
    _git(repo, "commit", "-q", "-m", message)


def _scope(repo: Path, diff_range: str):
    return cmd_scope_check.run_scope_check(
        repo, repo / BRIEF_RELPATH, diff_range)


def _evidence(repo: Path):
    return cmd_evidence_check.run_evidence_check(
        repo, repo / BRIEF_RELPATH, repo / GENERATED_ROOT_NAME,
        harness._alias_by_root(repo))


def _closeout(repo: Path, diff_range: str, write_digest: bool = False):
    return cmd_closeout.run_closeout_digest(
        repo, repo / BRIEF_RELPATH, diff_range, repo / GENERATED_ROOT_NAME,
        harness._alias_by_root(repo), write_digest=write_digest)


def _make_record(repo: Path, command: str = "echo happy-one", *,
                 captured_at: str | None = None,
                 changed_paths: list[dict] | None = None,
                 exit_code: int | None = 0,
                 timed_out: bool = False) -> Path:
    """One evidence record via Implementer A's writer (the real write path);
    captured_at optionally overridden AFTER build (build stamps now-UTC)."""
    record = evidence_records.build_evidence_record(
        tranche_id=TID, brief_source_path=BRIEF_RELPATH,
        brief_state="HUMAN_ADOPTED", brief_bound_sha="abc123",
        fence_active=True, command=command, cwd=".",
        declared_in=DECLARED_IN, exit_code=exit_code, timed_out=timed_out,
        duration_seconds=0.01, tool_versions={}, stdout="", stderr="",
        pre_run_porcelain=[], post_run_porcelain=[],
        changed_paths=changed_paths or [])
    if captured_at is not None:
        record["captured_at"] = captured_at
    json_path, _md = evidence_records.write_evidence_record(
        record, repo / GENERATED_ROOT_NAME, repo)
    return json_path


def _findings(report, code):
    return [f for f in report.findings if f.code == code]


# --- fence matcher unit tests -----------------------------------------------------

def test_matcher_trailing_double_star_is_strictly_under():
    assert scope_fence.pattern_matches("a/b/**", "a/b/c.md")
    assert scope_fence.pattern_matches("a/b/**", "a/b/c/d/e.md")
    assert not scope_fence.pattern_matches("a/b/**", "a/b")  # never the dir itself
    assert not scope_fence.pattern_matches("a/b/**", "a/bc/d.md")
    assert scope_fence.pattern_matches("**", "anything/at/all.md")
    # A trailing '/' is the subtree, like '/**'.
    assert scope_fence.pattern_matches("a/b/", "a/b/c.md")
    assert not scope_fence.pattern_matches("a/b/", "a/b")


def test_matcher_case_variant_paths_never_match():
    # The fence is what the human adopted — case-exact (D-GOV-04).
    assert not scope_fence.pattern_matches("projects/x/**", "Projects/x/a.md")
    assert not scope_fence.pattern_matches("projects/x/**", "projects/X/a.md")
    assert not scope_fence.pattern_matches("docs/*.md", "docs/A.MD")
    judged = scope_fence.judge_path(
        "Docs/notes.md", ["Docs2/**"], ["docs/**"])
    assert judged.judgment == scope_fence.JUDGMENT_OUTSIDE_WRITE_SCOPE
    assert judged.matched_pattern == ""


def test_matcher_nested_and_leading_double_star():
    assert scope_fence.pattern_matches("a/**/b/**", "a/x/y/b/z.md")
    assert scope_fence.pattern_matches("a/**/b/**", "a/b/z.md")  # zero segments
    assert not scope_fence.pattern_matches("a/**/b/**", "a/x/b")  # strictly under b
    assert scope_fence.pattern_matches("**/tests/*.py", "tests/test_x.py")
    assert scope_fence.pattern_matches("**/tests/*.py", "pkg/sub/tests/test_x.py")
    assert not scope_fence.pattern_matches("**/tests/*.py", "pkg/tests/sub/test_x.py")


def test_matcher_star_question_within_segment_and_dotfiles():
    assert scope_fence.pattern_matches("docs/*.md", "docs/a.md")
    assert not scope_fence.pattern_matches("docs/*.md", "docs/sub/a.md")  # * stays in-segment
    assert scope_fence.pattern_matches("docs/?.md", "docs/a.md")
    assert not scope_fence.pattern_matches("docs/?.md", "docs/ab.md")  # ? is one char
    assert not scope_fence.pattern_matches("docs/?.md", "docs/sub/a.md")
    # Dotfiles: no hidden-file carve-out is invented.
    assert scope_fence.pattern_matches("docs/**", "docs/.hidden")
    assert scope_fence.pattern_matches("docs/*", "docs/.hidden")
    assert scope_fence.pattern_matches("**/.gitignore", ".gitignore")
    assert scope_fence.pattern_matches("**/.gitignore", "sub/dir/.gitignore")


def test_matcher_deny_wins_over_allow():
    write_scope = ["a/**"]
    prohibited = ["a/secret/**"]
    judged = scope_fence.judge_path("a/secret/x.md", write_scope, prohibited)
    assert judged.judgment == scope_fence.JUDGMENT_PROHIBITED
    assert judged.matched_pattern == "a/secret/**"
    judged = scope_fence.judge_path("a/ok.md", write_scope, prohibited)
    assert judged.judgment == scope_fence.JUDGMENT_IN_WRITE_SCOPE
    assert judged.matched_pattern == "a/**"
    judged = scope_fence.judge_path("b/x.md", write_scope, prohibited)
    assert judged.judgment == scope_fence.JUDGMENT_OUTSIDE_WRITE_SCOPE


# --- scope-check -------------------------------------------------------------------

@requires_git
def test_scope_check_in_fence_diff_clean_with_blind_spot(tmp_path, capsys):
    repo = build_run_repo(tmp_path, [ECHO_CMD])
    base = _head(repo)
    _commit_file(repo, IN_FENCE_REL)
    rc = harness.main(["--repo-root", str(repo), "scope-check",
                       "--brief", BRIEF_RELPATH, "--diff", f"{base}..HEAD"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "SCOPE_VIOLATION" not in out
    assert "PROHIBITED_PATH_TOUCHED" not in out
    assert "in_write_scope" in out
    # The fixed blind-spot statement and the K-GATE-1 note, in EVERY output.
    assert "Blind spots" in out and "revert games" in out
    assert "never lifecycle judgment" in out
    report = _scope(repo, f"{base}..HEAD")
    assert report.findings == []  # clean adoption + in-fence diff


@requires_git
def test_scope_check_out_of_fence_active_fence_blocks_exit_1(tmp_path, capsys):
    repo = build_run_repo(tmp_path, [ECHO_CMD])
    base = _head(repo)
    _commit_file(repo, OUT_OF_FENCE_REL)
    report = _scope(repo, f"{base}..HEAD")
    hits = _findings(report, "SCOPE_VIOLATION")
    assert len(hits) == 1 and hits[0].severity is Severity.BLOCK
    assert hits[0].source_path == OUT_OF_FENCE_REL
    assert "objective tracked-path violation" in hits[0].message
    assert compute_exit_code(report.findings) == 1
    rc = harness.main(["--repo-root", str(repo), "scope-check",
                       "--brief", BRIEF_RELPATH, "--diff", f"{base}..HEAD"])
    assert rc == 1
    capsys.readouterr()


@requires_git
def test_scope_check_candidate_brief_caps_block_to_review(tmp_path, capsys):
    # BLOCK discipline: the scope BLOCK exists ONLY against an active fence;
    # against a CANDIDATE it is created as BLOCK and capped at REVIEW with
    # the fence's cap_reason recorded (D-GOV-04).
    repo = build_run_repo(tmp_path, [ECHO_CMD],
                          brief_state="CANDIDATE",
                          adopted_by="TBD — placeholder")
    base = _head(repo)
    _commit_file(repo, OUT_OF_FENCE_REL)
    report = _scope(repo, f"{base}..HEAD")
    hits = _findings(report, "SCOPE_VIOLATION")
    assert len(hits) == 1 and hits[0].severity is Severity.REVIEW
    assert "D-GOV-04" in hits[0].caveat  # the cap_reason, recorded
    assert compute_exit_code(report.findings) == 0
    rc = harness.main(["--repo-root", str(repo), "scope-check",
                       "--brief", BRIEF_RELPATH, "--diff", f"{base}..HEAD"])
    assert rc == 0
    capsys.readouterr()
    rc = harness.main(["--repo-root", str(repo), "--strict", "scope-check",
                       "--brief", BRIEF_RELPATH, "--diff", f"{base}..HEAD"])
    assert rc == 1
    capsys.readouterr()


@requires_git
def test_scope_check_prohibited_path_touched(tmp_path, capsys):
    # write_scope `**` covers the touched path TOO, so deny-wins is
    # exercised through the integration path (not only the matcher unit
    # test): the prohibited_paths match governs the judgment.
    repo = build_run_repo(tmp_path, [ECHO_CMD], write_scope="**")
    base = _head(repo)
    _commit_file(repo, "docs/new_note.md")  # fixture brief prohibits docs/**
    assert scope_fence.pattern_matches("**", "docs/new_note.md")  # in-scope too
    report = _scope(repo, f"{base}..HEAD")
    hits = _findings(report, "PROHIBITED_PATH_TOUCHED")
    assert len(hits) == 1 and hits[0].severity is Severity.BLOCK
    assert "`docs/**`" in hits[0].message
    assert not _findings(report, "SCOPE_VIOLATION")  # deny wins, judged once
    rows = {row["path"]: row for row in report.extras["scope_check"]["changed"]}
    assert rows["docs/new_note.md"]["judgment"] == scope_fence.JUDGMENT_PROHIBITED
    assert rows["docs/new_note.md"]["matched_pattern"] == "docs/**"
    # The gate: BLOCK -> exit 1, direct and through the CLI (D-GOV-02).
    assert compute_exit_code(report.findings) == 1
    rc = harness.main(["--repo-root", str(repo), "scope-check",
                       "--brief", BRIEF_RELPATH, "--diff", f"{base}..HEAD"])
    assert rc == 1
    capsys.readouterr()


@requires_git
def test_scope_check_untracked_out_of_fence_is_review_never_block(tmp_path):
    repo = build_run_repo(tmp_path, [ECHO_CMD])
    _write(repo / PROJECT_REL / "untracked_stray.txt", "stray\n")
    report = _scope(repo, "HEAD..HEAD")  # valid, empty diff range
    hits = _findings(report, "SCOPE_VIOLATION")
    assert len(hits) == 1 and hits[0].severity is Severity.REVIEW
    assert hits[0].source_path == PROJECT_REL + "/untracked_stray.txt"
    assert "outside the objective tracked-path" in hits[0].caveat
    # Even with an ACTIVE fence, an observed-untracked path never BLOCKs.
    assert report.summary["fence_active"] is True
    assert compute_exit_code(report.findings) == 0


@requires_git
def test_scope_check_rename_judges_both_sides(tmp_path):
    repo = build_run_repo(tmp_path, [ECHO_CMD])
    base = _head(repo)
    dest_dir = repo / PROJECT_REL / "execution" / "DEL-01-01"
    dest_dir.mkdir(parents=True)
    _git(repo, "mv", PROJECT_REL + "/tracked.md",
         PROJECT_REL + "/execution/DEL-01-01/tracked.md")
    _git(repo, "commit", "-q", "-m", "move into fence")
    report = _scope(repo, f"{base}..HEAD")
    rows = {row["path"]: row for row in report.extras["scope_check"]["changed"]}
    # Both sides judged: the old (out-of-fence) path violates, the new
    # (in-fence) path is in write_scope.
    assert rows[PROJECT_REL + "/tracked.md"]["judgment"] == "outside_write_scope"
    assert (rows[PROJECT_REL + "/execution/DEL-01-01/tracked.md"]["judgment"]
            == "in_write_scope")
    hits = _findings(report, "SCOPE_VIOLATION")
    assert [f.source_path for f in hits] == [PROJECT_REL + "/tracked.md"]


@requires_git
def test_scope_check_bad_diff_range_is_operational_exit_2(tmp_path, capsys):
    repo = build_run_repo(tmp_path, [ECHO_CMD])
    with pytest.raises(HarnessOperationalError) as exc:
        _scope(repo, "no-such-rev..HEAD")
    assert "K-INVENT-1" in str(exc.value)
    rc = harness.main(["--repo-root", str(repo), "scope-check",
                       "--brief", BRIEF_RELPATH,
                       "--diff", "no-such-rev..HEAD"])
    assert rc == 2
    assert "ERROR" in capsys.readouterr().err
    # Option-shaped ranges are refused outright (never passed to git).
    with pytest.raises(HarnessOperationalError):
        _scope(repo, "--all")


@requires_git
def test_scope_check_identity_refusal_exits_2_judges_nothing(tmp_path, capsys):
    repo = build_run_repo(tmp_path, [ECHO_CMD], adopted_by="Some Stranger")
    rc = harness.main(["--repo-root", str(repo), "scope-check",
                       "--brief", BRIEF_RELPATH, "--diff", "HEAD..HEAD"])
    assert rc == 2
    captured = capsys.readouterr()
    assert "D-GOV-04" in captured.err
    assert "no path was judged" in captured.out
    assert "Blind spots" in captured.out  # stated even on refusal


# --- evidence-check ------------------------------------------------------------------

@requires_git
def test_evidence_satisfied_by_harness_record(tmp_path, capsys):
    repo = build_run_repo(tmp_path, [ECHO_CMD])
    _make_record(repo, "echo happy-one")
    report = _evidence(repo)
    assert not _findings(report, "EVIDENCE_MISSING")
    assert not _findings(report, "EVIDENCE_STALE")
    facts = [f for f in report.facts
             if f.fact_id == "evidence_check.01.record"]
    assert len(facts) == 1
    assert facts[0].value.startswith("exit 0; captured_at ")
    assert "001_echo_happy_one.json" in facts[0].source_path
    assert "never lifecycle" in facts[0].caveat  # two-class self-exclusion
    assert report.summary["coverage"] == (
        "1 of 1 declared validation commands have harness-captured "
        "evidence records")
    # No commits touch DEL-01-01/** in this fixture -> staleness N/A, stated.
    hits = _findings(report, "EVIDENCE_STALENESS_NOT_APPLICABLE")
    assert len(hits) == 1 and hits[0].severity is Severity.NOT_APPLICABLE
    assert compute_exit_code(report.findings) == 0
    rc = harness.main(["--repo-root", str(repo), "evidence-check",
                       "--brief", BRIEF_RELPATH])
    assert rc == 0
    out = capsys.readouterr().out
    assert "Provenance ladder" in out
    assert "never sufficiency" in out


@requires_git
def test_evidence_missing_is_review_0_default_1_strict(tmp_path, capsys):
    repo = build_run_repo(tmp_path, [ECHO_CMD])
    report = _evidence(repo)
    hits = _findings(report, "EVIDENCE_MISSING")
    assert len(hits) == 1 and hits[0].severity is Severity.REVIEW
    assert "echo happy-one" in hits[0].message
    assert "never pass silently" in hits[0].message
    assert hits[0].source_path == DECLARED_IN
    assert report.summary["coverage"].startswith("0 of 1")
    rc = harness.main(["--repo-root", str(repo), "evidence-check",
                       "--brief", BRIEF_RELPATH])
    assert rc == 0
    capsys.readouterr()
    rc = harness.main(["--repo-root", str(repo), "--strict", "evidence-check",
                       "--brief", BRIEF_RELPATH])
    assert rc == 1
    capsys.readouterr()


@requires_git
def test_evidence_stale_when_scope_commit_is_newer(tmp_path):
    repo = build_run_repo(tmp_path, [ECHO_CMD])
    # Record captured long ago; then a commit touches a write_scope path
    # AFTER that captured_at.
    _make_record(repo, "echo happy-one",
                 captured_at="2020-01-01T00:00:00+00:00")
    _commit_file(repo, IN_FENCE_REL, message="newer scope change")
    report = _evidence(repo)
    hits = _findings(report, "EVIDENCE_STALE")
    assert len(hits) == 1 and hits[0].severity is Severity.REVIEW
    assert "2020-01-01T00:00:00+00:00" in hits[0].message  # names the capture time
    assert "OLDER than the newest commit" in hits[0].message
    assert _git(repo, "rev-parse", "HEAD")[:12] in hits[0].message
    assert not _findings(report, "EVIDENCE_MISSING")
    assert not _findings(report, "EVIDENCE_STALENESS_NOT_APPLICABLE")
    assert compute_exit_code(report.findings) == 0  # REVIEW, never BLOCK


@requires_git
def test_evidence_unparseable_record_is_labeled_never_guessed(tmp_path):
    repo = build_run_repo(tmp_path, [ECHO_CMD])
    _write(repo / GENERATED_ROOT_NAME / "evidence" / TID / "junk.json",
           "not json at all")
    report = _evidence(repo)
    hits = _findings(report, "EVIDENCE_UNPARSEABLE")
    assert len(hits) == 1 and hits[0].severity is Severity.REVIEW
    assert "labeled, never guessed" in hits[0].message
    # The command still has no matching record -> also MISSING; no crash.
    assert _findings(report, "EVIDENCE_MISSING")
    assert compute_exit_code(report.findings) == 0


@requires_git
def test_evidence_no_validations_is_not_applicable(tmp_path):
    repo = build_run_repo(tmp_path, [])
    report = _evidence(repo)
    hits = _findings(report, "EVIDENCE_CHECK_NOT_APPLICABLE")
    assert len(hits) == 1 and hits[0].severity is Severity.NOT_APPLICABLE
    assert "nothing to verify" in hits[0].message
    assert not _findings(report, "EVIDENCE_MISSING")
    assert report.summary["coverage"].startswith("0 of 0")
    assert compute_exit_code(report.findings, strict=True) == 0


@requires_git
def test_evidence_mutation_flagged_record_is_review(tmp_path):
    repo = build_run_repo(tmp_path, [ECHO_CMD])
    _make_record(repo, "echo happy-one", changed_paths=[
        {"path": PROJECT_REL + "/tracked.md",
         "classification": "unexpected_tracked_change"}])
    report = _evidence(repo)
    hits = _findings(report, "EVIDENCE_RECORD_FLAGGED")
    assert len(hits) == 1 and hits[0].severity is Severity.REVIEW
    assert "unexpected_tracked_change" in hits[0].message
    assert "human review required" in hits[0].message
    # Evidence-check NEVER blocks — not even on a mutation-flagged record
    # (the BLOCK lives in run-validations, at capture time).
    assert all(f.severity is not Severity.BLOCK for f in report.findings)
    assert compute_exit_code(report.findings) == 0


@requires_git
def test_evidence_external_target_ladder_rungs(tmp_path):
    repo = build_run_repo(tmp_path, [ECHO_CMD])
    brief = repo / BRIEF_RELPATH
    text = brief.read_text(encoding="utf-8").replace(
        "## evidence_targets\n\n",
        "## evidence_targets\n\n"
        "- `" + PROJECT_REL + "/_validation/report.txt`\n")
    brief.write_text(text, encoding="utf-8")
    _git(repo, "add", BRIEF_RELPATH)
    _git(repo, "commit", "-q", "-m", "declare external evidence target")
    _make_record(repo, "echo happy-one")
    # Rung 3: the declared external target is ABSENT -> reported missing,
    # never accepted on narrative.
    report = _evidence(repo)
    absent = [f for f in _findings(report, "EVIDENCE_MISSING")
              if "_validation/report.txt" in f.message]
    assert len(absent) == 1 and absent[0].severity is Severity.REVIEW
    # Rung 2: the artifact exists -> satisfies at REVIEW, never silently.
    _write(repo / PROJECT_REL / "_validation" / "report.txt", "external\n")
    report = _evidence(repo)
    hits = _findings(report, "EVIDENCE_EXTERNAL_ARTIFACT")
    assert len(hits) == 1 and hits[0].severity is Severity.REVIEW
    assert "satisfies at REVIEW" in hits[0].message
    assert not [f for f in _findings(report, "EVIDENCE_MISSING")
                if "_validation/report.txt" in f.message]


def test_scope_pathspec_prefix_derivation():
    # Fence globs are never handed to git verbatim (git pathspec `*`
    # semantics differ from the fence matcher's): each entry reduces to its
    # literal directory prefix before the first wildcard-bearing component.
    assert cmd_evidence_check._scope_pathspecs(
        ["projects/x/execution/**"]) == (["projects/x/execution"], False)
    assert cmd_evidence_check._scope_pathspecs(["docs/*.md"]) == (["docs"], False)
    assert cmd_evidence_check._scope_pathspecs(["docs/v?/notes.md"]) == (["docs"], False)
    assert cmd_evidence_check._scope_pathspecs(
        ["a/**/b/**", "a/c.md"]) == (["a", "a/c.md"], False)
    # An all-wildcard entry covers the whole repo: pathspec `.`, labeled.
    assert cmd_evidence_check._scope_pathspecs(["**"]) == (["."], True)
    assert cmd_evidence_check._scope_pathspecs(["**/tests/*.py"]) == (["."], True)
    assert cmd_evidence_check._scope_pathspecs(["projects/x/**", "**"]) == (["."], True)
    # Empty scope: nothing to date; never a whole-repo guess.
    assert cmd_evidence_check._scope_pathspecs([]) == ([], False)


@requires_git
def test_evidence_stale_fires_for_whole_repo_write_scope(tmp_path):
    # A bare `**` write_scope reduces to NO literal directory prefix. The
    # old prefix reduction dated nothing (silent NOT_APPLICABLE even though
    # the scope covers the whole repo); now staleness is dated against the
    # newest commit in the whole repository (git pathspec `.`) and the
    # output says so — labeled, never silent (K-INVENT-1).
    repo = build_run_repo(tmp_path, [ECHO_CMD], write_scope="**")
    # `**` resolves under no pilot project root; register the repo root
    # itself as this fixture's project root and give it a manifest.
    _write(repo / "_harness" / "adapter.yaml",
           ADAPTER_TEMPLATE.format(commands=_yaml_commands([ECHO_CMD])))
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "root-level adapter manifest")
    _make_record(repo, "echo happy-one",
                 captured_at="2020-01-01T00:00:00+00:00")
    _commit_file(repo, "unrelated/afterthought.md",
                 message="newest repo commit, outside any literal prefix")
    report = cmd_evidence_check.run_evidence_check(
        repo, repo / BRIEF_RELPATH, repo / GENERATED_ROOT_NAME,
        {repo.resolve(): "repo-root"})
    assert not _findings(report, "EVIDENCE_STALENESS_NOT_APPLICABLE")
    hits = _findings(report, "EVIDENCE_STALE")
    assert len(hits) == 1 and hits[0].severity is Severity.REVIEW
    assert "2020-01-01T00:00:00+00:00" in hits[0].message
    assert _git(repo, "rev-parse", "HEAD")[:12] in hits[0].message
    assert "WHOLE" in hits[0].caveat and "pathspec `.`" in hits[0].caveat
    assert "pathspec `.`" in report.render_markdown()  # stated, not silent
    assert compute_exit_code(report.findings) == 0  # REVIEW, never BLOCK


# --- evidence-read containment (fail-closed; D-GOV-01 / K-WRITE-2) -----------------

@requires_git
def test_evidence_read_out_dir_outside_repo_refuses_exit_2(tmp_path, capsys):
    # (a) out_dir OUTSIDE the repo entirely: fail-closed refusal, never an
    # empty (or worse, trusted) read — harness-captured evidence provenance
    # exists only under the declared generated root. CLI exit 2 for BOTH
    # evidence-check and closeout-digest.
    repo = build_run_repo(tmp_path, [ECHO_CMD])
    outside = tmp_path / "elsewhere"
    _write(outside / "evidence" / TID / "001_echo_happy_one.json", "{}")
    with pytest.raises(HarnessOperationalError) as exc:
        evidence_records.load_evidence_records(repo, outside, TID)
    assert "generated root" in str(exc.value)
    assert "provenance" in str(exc.value)
    rc = harness.main(["--repo-root", str(repo), "--out-dir", str(outside),
                       "evidence-check", "--brief", BRIEF_RELPATH])
    assert rc == 2
    assert "ERROR" in capsys.readouterr().err
    rc = harness.main(["--repo-root", str(repo), "--out-dir", str(outside),
                       "closeout-digest", "--brief", BRIEF_RELPATH,
                       "--diff", "HEAD..HEAD"])
    assert rc == 2
    assert "ERROR" in capsys.readouterr().err


@requires_git
def test_evidence_read_out_dir_inside_repo_outside_generated_root_refuses(
        tmp_path, capsys):
    # (b) out_dir INSIDE the repo but outside {repo}/_harness_generated:
    # same fail-closed refusal and exit 2 — the read side uses the same
    # containment semantics as the write side (ensure_generated_scope).
    repo = build_run_repo(tmp_path, [ECHO_CMD])
    inside_repo = repo / "docs"
    with pytest.raises(HarnessOperationalError) as exc:
        evidence_records.load_evidence_records(repo, inside_repo, TID)
    assert "generated root" in str(exc.value)
    rc = harness.main(["--repo-root", str(repo),
                       "--out-dir", str(inside_repo),
                       "evidence-check", "--brief", BRIEF_RELPATH])
    assert rc == 2
    assert "ERROR" in capsys.readouterr().err
    rc = harness.main(["--repo-root", str(repo),
                       "--out-dir", str(inside_repo),
                       "closeout-digest", "--brief", BRIEF_RELPATH,
                       "--diff", "HEAD..HEAD"])
    assert rc == 2
    assert "ERROR" in capsys.readouterr().err


@requires_git
def test_evidence_read_generated_root_out_dir_unchanged(tmp_path):
    # (c) the declared generated root as out_dir: unchanged behavior — a
    # present record loads PARSED; a missing tranche directory INSIDE the
    # generated root stays an empty list (never a refusal).
    repo = build_run_repo(tmp_path, [ECHO_CMD])
    _make_record(repo, "echo happy-one")
    loaded = evidence_records.load_evidence_records(
        repo, repo / GENERATED_ROOT_NAME, TID)
    assert [r.parse_status for r in loaded] == ["PARSED"]
    assert evidence_records.load_evidence_records(
        repo, repo / GENERATED_ROOT_NAME, "TRB-absent-999") == []


@requires_git
def test_evidence_read_symlinked_generated_root_refuses(tmp_path):
    # A symlinked generated root refuses on read exactly as on write:
    # capture provenance cannot be trusted through a relocated boundary.
    repo = build_run_repo(tmp_path, [ECHO_CMD])
    relocated = tmp_path / "relocated_generated"
    relocated.mkdir()
    (repo / GENERATED_ROOT_NAME).symlink_to(relocated)
    with pytest.raises(HarnessOperationalError) as exc:
        evidence_records.load_evidence_records(
            repo, repo / GENERATED_ROOT_NAME, TID)
    assert "symlink" in str(exc.value)
    assert "provenance" in str(exc.value)


@requires_git
def test_evidence_identity_refusal_exits_2(tmp_path, capsys):
    repo = build_run_repo(tmp_path, [ECHO_CMD], adopted_by="Some Stranger")
    rc = harness.main(["--repo-root", str(repo), "evidence-check",
                       "--brief", BRIEF_RELPATH])
    assert rc == 2
    captured = capsys.readouterr()
    assert "D-GOV-04" in captured.err
    assert "nothing was verified" in captured.out


# --- closeout-digest ------------------------------------------------------------------

@requires_git
def test_closeout_composes_both_checks_and_dedups(tmp_path):
    # CANDIDATE brief: both sub-checks emit BRIEF_NOT_ADOPTED; the digest
    # unions findings deduplicated by (code, source, line) -> exactly once.
    repo = build_run_repo(tmp_path, [ECHO_CMD],
                          brief_state="CANDIDATE",
                          adopted_by="TBD — placeholder")
    base = _head(repo)
    _commit_file(repo, OUT_OF_FENCE_REL)
    report = _closeout(repo, f"{base}..HEAD")
    codes = [f.code for f in report.findings]
    assert codes.count("BRIEF_NOT_ADOPTED") == 1  # deduped across sub-checks
    assert codes.count("SCOPE_VIOLATION") == 1    # from scope-check
    assert codes.count("EVIDENCE_MISSING") == 1   # from evidence-check
    md = report.render_markdown()
    assert "Changed files by fence classification" in md
    assert "Evidence records captured" in md
    assert "Open human decision points (copied from the brief)" in md
    assert "adoption of this brief itself" in md  # copied brief content
    assert "Blind spots" in md and "revert games" in md
    assert "never a lifecycle transition" in md
    # Capped REVIEW (candidate fence) -> exit 0.
    assert compute_exit_code(report.findings) == 0


@requires_git
def test_closeout_write_digest_lands_under_generated_root(tmp_path):
    repo = build_run_repo(tmp_path, [ECHO_CMD])
    base = _head(repo)
    _commit_file(repo, IN_FENCE_REL)
    _make_record(repo, "echo happy-one")
    report = _closeout(repo, f"{base}..HEAD", write_digest=True)
    digest = repo / GENERATED_ROOT_NAME / "closeout" / f"{TID}.md"
    assert digest.is_file()
    assert report.summary["digest_written"] == (
        GENERATED_ROOT_NAME + f"/closeout/{TID}.md")
    text = digest.read_text(encoding="utf-8")
    assert text.startswith("> **Generated view — not authority.**")
    assert "Blind spots" in text
    assert "never a lifecycle transition" in text
    # No lifecycle-transition claims anywhere in the digest.
    assert find_claim_language(text) == []


@requires_git
def test_closeout_without_flag_writes_nothing(tmp_path):
    repo = build_run_repo(tmp_path, [ECHO_CMD])
    _closeout(repo, "HEAD..HEAD")
    assert not (repo / GENERATED_ROOT_NAME / "closeout").exists()


@requires_git
def test_closeout_downgrades_subcheck_block_and_never_gates(tmp_path, capsys):
    # Adopted brief + out-of-fence committed change: scope-check is the
    # GATE (exit 1); closeout-digest on the SAME state is a composition and
    # never a gate — the composed BLOCK is carried downgraded to REVIEW
    # with the gating command named, so the digest exits 0 (D-GOV-02: exit
    # 1 iff a BLOCK finding is in the digest's own report).
    repo = build_run_repo(tmp_path, [ECHO_CMD])
    base = _head(repo)
    _commit_file(repo, OUT_OF_FENCE_REL)
    rc = harness.main(["--repo-root", str(repo), "scope-check",
                       "--brief", BRIEF_RELPATH, "--diff", f"{base}..HEAD"])
    assert rc == 1  # the gate, unchanged
    capsys.readouterr()
    report = _closeout(repo, f"{base}..HEAD")
    hits = _findings(report, "SCOPE_VIOLATION")
    assert len(hits) == 1 and hits[0].severity is Severity.REVIEW
    assert "Reported at BLOCK by scope-check" in hits[0].caveat
    assert "never a gate" in hits[0].caveat
    assert "run scope-check for the gating exit code" in hits[0].caveat
    assert all(f.severity is not Severity.BLOCK for f in report.findings)
    assert compute_exit_code(report.findings) == 0
    rc = harness.main(["--repo-root", str(repo), "closeout-digest",
                       "--brief", BRIEF_RELPATH, "--diff", f"{base}..HEAD"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "Reported at BLOCK by scope-check" in out  # information kept visible


@requires_git
def test_closeout_cli_exit_pins_0_and_2_never_1_by_composition(tmp_path, capsys):
    repo = build_run_repo(tmp_path, [ECHO_CMD])
    base = _head(repo)
    _commit_file(repo, IN_FENCE_REL)
    # 0: in-fence change; missing evidence is REVIEW.
    rc = harness.main(["--repo-root", str(repo), "closeout-digest",
                       "--brief", BRIEF_RELPATH, "--diff", f"{base}..HEAD"])
    assert rc == 0
    out = capsys.readouterr().out
    assert find_claim_language(out) == []
    # Still 0 with an out-of-fence tracked change against the ACTIVE fence:
    # the composed scope-check BLOCK is downgraded to REVIEW (the digest is
    # never a gate; scope-check carries the gating exit code).
    _commit_file(repo, OUT_OF_FENCE_REL)
    rc = harness.main(["--repo-root", str(repo), "closeout-digest",
                       "--brief", BRIEF_RELPATH, "--diff", f"{base}..HEAD",
                       "--write-digest"])
    assert rc == 0
    capsys.readouterr()
    assert (repo / GENERATED_ROOT_NAME / "closeout" / f"{TID}.md").is_file()
    # --strict escalates REVIEW findings to exit 1, as everywhere else.
    rc = harness.main(["--repo-root", str(repo), "--strict", "closeout-digest",
                       "--brief", BRIEF_RELPATH, "--diff", f"{base}..HEAD"])
    assert rc == 1
    capsys.readouterr()
    # 2: unresolvable range is operational.
    rc = harness.main(["--repo-root", str(repo), "closeout-digest",
                       "--brief", BRIEF_RELPATH, "--diff", "bogus..HEAD"])
    assert rc == 2
    assert "ERROR" in capsys.readouterr().err


@requires_git
def test_closeout_identity_refusal_runs_no_subcheck(tmp_path, capsys):
    repo = build_run_repo(tmp_path, [ECHO_CMD], adopted_by="Some Stranger")
    rc = harness.main(["--repo-root", str(repo), "closeout-digest",
                       "--brief", BRIEF_RELPATH, "--diff", "HEAD..HEAD",
                       "--write-digest"])
    assert rc == 2
    captured = capsys.readouterr()
    assert "D-GOV-04" in captured.err
    assert "no digest was written" in captured.out
    assert not (repo / GENERATED_ROOT_NAME / "closeout").exists()
