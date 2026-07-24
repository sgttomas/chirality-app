#!/usr/bin/env python3
"""Phase 3 brief-adoption tests: parsing, committed-adoption verification
(D-GOV-04 / K-AUTH-2), the `next` pick-list, and the CLI wiring.

Fixture idiom per test_abs_path_lint_fixtures.py: tmp git repos built from
string constants inside this test module (fixture identity on every git
call); all fixture content is repo-relative, so no synthetic absolute-path
prefix is needed.
"""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

import pytest

import brief_adoption
import cmd_brief
import cmd_next
import harness
from brief_adoption import parse_brief_markdown, verify_adoption
from harness_common import (
    GENERATED_ROOT_NAME,
    HarnessOperationalError,
    Severity,
)
from test_self_check_fixtures import (
    STATUS_MATCH,
    _write,
    build_mini_repo,
    build_project,
)

requires_git = pytest.mark.skipif(shutil.which("git") is None,
                                  reason="git not available")

LIVE_REPO = Path(__file__).resolve().parents[2]
live = pytest.mark.skipif(
    os.environ.get("CHIRALITY_SKIP_LIVE_TESTS") == "1"
    or not (LIVE_REPO / "projects" / "chirality-piping" / "_harness" / "adapter.yaml").is_file()
    or not (LIVE_REPO / "projects" / "chirality-app-dev" / "_harness" / "adapter.yaml").is_file(),
    reason="live pilot roots/manifests absent (or live tests disabled by env)",
)

# --- Fixture material -------------------------------------------------------------

FIXTURE_ACTORS_MD = '''# human_actors — fixture allowlist

## Actors

| Canonical name | Role | Matchable aliases | Git identity | Email | Effective |
|---|---|---|---|---|---|
| Fixture Owner | Owner | `fixture-owner`, `owner` | `Fixture Owner <owner@example.invalid>` | owner@example.invalid | 2026-07-01 |
'''

BRIEF_FIXTURE = '''# Tranche brief {tid} — {state}

- tranche_id: `{tid}`
- state: {state}
  - lifecycle: CANDIDATE → HUMAN_ADOPTED → EXECUTED → CHECKED → HUMAN_REVIEWED → CLOSED/SUPERSEDED
- objective: fixture objective — stated by the fixture author
- adopted_by: {adopted_by}
- adopted_on: {adopted_on}

## read_scope

- `projects/fixture/execution/DEL-01-01/**`

## write_scope

- `projects/fixture/execution/DEL-01-01/**`

## prohibited_paths

- `_DomainEngines/**`
- `docs/**`

## validations (declared, not run)

- none declared

## evidence_targets

- `_harness_generated/evidence/{tid}/` (under the declared generated root; D-GOV-01)

## stop_conditions

- an out-of-scope write attempt

## human_decision_points

- adoption of this brief itself (D-GOV-04)

---

Footer fixture: the cited sources govern on any disagreement.
'''

BRIEF_RELPATH = "docs/governance_harness/briefs/TRB-fixture-001.md"


def _git(repo: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", "-C", str(repo), "-c", "user.email=fixture@example.invalid",
         "-c", "user.name=Fixture", *args],
        check=True, capture_output=True, text=True)
    return proc.stdout.strip()


def build_adoption_repo(tmp_path: Path, with_allowlist: bool = True) -> Path:
    """A tmp git repo with the fixture identity allowlist committed (the
    committed-adoption verification substrate)."""
    repo = tmp_path / "repo"
    _write(repo / ".gitignore", GENERATED_ROOT_NAME + "/\n")
    if with_allowlist:
        _write(repo / "docs" / "governance_harness" / "human_actors.md",
               FIXTURE_ACTORS_MD)
    _git(repo, "init", "-q")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "fixture repo")
    return repo


def _add_brief(repo: Path, state: str = "HUMAN_ADOPTED",
               adopted_by: str = "fixture-owner", adopted_on: str = "2026-07-02",
               tid: str = "TRB-fixture-001", relpath: str = BRIEF_RELPATH,
               commit: bool = True) -> Path:
    path = repo / relpath
    _write(path, BRIEF_FIXTURE.format(
        tid=tid, state=state, adopted_by=adopted_by, adopted_on=adopted_on))
    if commit:
        _git(repo, "add", "-f", relpath)  # -f: reaches the gitignored scratch root too
        _git(repo, "commit", "-q", "-m", f"brief {tid}")
    return path


def _findings(findings, code):
    return [f for f in findings if f.code == code]


# --- (a) CANDIDATE: fence inactive, INFO, no refusal, no identity check ------------

@requires_git
def test_candidate_brief_is_inactive_info_no_refusal(tmp_path):
    # Allowlist deliberately ABSENT: no identity check runs on a candidate
    # (no human is attributed), so no refusal either.
    repo = build_adoption_repo(tmp_path, with_allowlist=False)
    path = _add_brief(repo, state="CANDIDATE",
                      adopted_by="TBD — placeholder", adopted_on="TBD")
    fence, findings, refusal = verify_adoption(path, repo)
    assert refusal is None
    assert fence.fence_active is False
    assert fence.cap_reason and "D-GOV-04" in fence.cap_reason
    assert fence.bound_sha == ""
    hits = _findings(findings, "BRIEF_NOT_ADOPTED")
    assert len(hits) == 1 and hits[0].severity is Severity.INFO
    assert "fences nothing" in hits[0].message
    assert "cap at REVIEW" in hits[0].message


# --- (b) HUMAN_ADOPTED + committed + matched actor: fence active, SHA-bound --------

@requires_git
def test_adopted_committed_matched_actor_activates_fence(tmp_path):
    repo = build_adoption_repo(tmp_path)
    path = _add_brief(repo, state="HUMAN_ADOPTED", adopted_by="fixture-owner")
    # A later unrelated commit must not move the brief's publication commit.
    _write(repo / "unrelated.md", "unrelated\n")
    _git(repo, "add", "unrelated.md")
    _git(repo, "commit", "-q", "-m", "unrelated")
    fence, findings, refusal = verify_adoption(path, repo)
    assert refusal is None
    assert findings == []
    assert fence.fence_active is True
    assert fence.cap_reason == ""
    assert fence.adopted_by_canonical == "Fixture Owner"
    expected = _git(repo, "log", "-1", "--format=%H", "--", BRIEF_RELPATH)
    assert fence.bound_sha == expected
    assert fence.bound_sha != _git(repo, "rev-parse", "HEAD")
    facts = {f.fact_id: f for f in fence.facts}
    assert facts["brief.adoption_bound_sha"].value == expected
    assert "K-AUTH-2" in facts["brief.adoption_bound_sha"].caveat


# --- (c) untracked -> ADOPTION_NOT_COMMITTED REVIEW --------------------------------

@requires_git
def test_adopted_but_untracked_is_review_not_committed(tmp_path):
    repo = build_adoption_repo(tmp_path)
    path = _add_brief(repo, commit=False)
    fence, findings, refusal = verify_adoption(path, repo)
    assert refusal is None
    assert fence.fence_active is False
    assert fence.bound_sha == ""
    hits = _findings(findings, "ADOPTION_NOT_COMMITTED")
    assert len(hits) == 1 and hits[0].severity is Severity.REVIEW
    assert "D-GOV-04" in hits[0].message
    assert hits[0].invariant == "K-AUTH-2"


# --- (d) tracked but dirty -> ADOPTION_UNCOMMITTED_EDITS REVIEW --------------------

@requires_git
def test_adopted_tracked_but_dirty_is_review_uncommitted_edits(tmp_path):
    repo = build_adoption_repo(tmp_path)
    path = _add_brief(repo)
    path.write_text(path.read_text(encoding="utf-8") + "\npost-adoption edit\n",
                    encoding="utf-8")
    fence, findings, refusal = verify_adoption(path, repo)
    assert refusal is None
    assert fence.fence_active is False
    assert fence.bound_sha == ""
    hits = _findings(findings, "ADOPTION_UNCOMMITTED_EDITS")
    assert len(hits) == 1 and hits[0].severity is Severity.REVIEW
    assert "K-AUTH-2" in hits[0].message


# --- (e) adopted_by not in allowlist -> refusal (and CLI exit 2) --------------------

@requires_git
def test_unmatched_actor_refuses_with_no_findings(tmp_path, capsys):
    repo = build_adoption_repo(tmp_path)
    path = _add_brief(repo, adopted_by="Some Stranger")
    fence, findings, refusal = verify_adoption(path, repo)
    assert refusal is not None
    assert "Some Stranger" in refusal and "D-GOV-04" in refusal
    assert findings == []  # refusals produce NO severity findings
    assert fence.fence_active is False
    rc = harness.main(["--repo-root", str(repo),
                       "brief", "--verify-adoption", BRIEF_RELPATH])
    assert rc == 2
    assert "D-GOV-04" in capsys.readouterr().err


@requires_git
def test_adopted_by_absent_refuses(tmp_path):
    repo = build_adoption_repo(tmp_path)
    path = _add_brief(repo, adopted_by="TBD — never filled")
    fence, findings, refusal = verify_adoption(path, repo)
    assert refusal is not None and "no adopted_by actor" in refusal
    assert findings == []


@requires_git
def test_tbd_prefixed_actor_is_a_real_unmatched_actor_not_absent(tmp_path):
    # "TBDenson" merely STARTS with the letters TBD — it is a real attributed
    # value (no word boundary after TBD), so the refusal names the unmatched
    # actor rather than reporting an absent one.
    repo = build_adoption_repo(tmp_path)
    path = _add_brief(repo, adopted_by="TBDenson")
    fence, findings, refusal = verify_adoption(path, repo)
    assert fence.adopted_by == "TBDenson"  # not swallowed as a placeholder
    assert refusal is not None
    assert "TBDenson" in refusal and "matches no allowlist entry" in refusal
    assert "no adopted_by actor" not in refusal
    assert findings == []


# --- (f) allowlist absent -> refusal (and CLI exit 2) -------------------------------

@requires_git
def test_allowlist_absent_refuses(tmp_path, capsys):
    repo = build_adoption_repo(tmp_path, with_allowlist=False)
    path = _add_brief(repo)
    fence, findings, refusal = verify_adoption(path, repo)
    assert refusal is not None and "D-GOV-04" in refusal
    assert findings == []
    assert fence.fence_active is False
    rc = harness.main(["--repo-root", str(repo),
                       "brief", "--verify-adoption", BRIEF_RELPATH])
    assert rc == 2
    assert "D-GOV-04" in capsys.readouterr().err


# --- (g) terminal state -> BRIEF_LIFECYCLE_TERMINAL, fence inactive ----------------

@requires_git
def test_closed_brief_is_terminal_and_inactive(tmp_path):
    repo = build_adoption_repo(tmp_path)
    path = _add_brief(repo, state="CLOSED")
    fence, findings, refusal = verify_adoption(path, repo)
    assert refusal is None
    assert fence.fence_active is False
    assert "no longer fences new work" in fence.cap_reason
    hits = _findings(findings, "BRIEF_LIFECYCLE_TERMINAL")
    assert len(hits) == 1 and hits[0].severity is Severity.INFO
    # The identity + committed checks still ran (a terminal brief still
    # claims adoption): committed clean -> the publication commit is bound.
    assert fence.adopted_by_canonical == "Fixture Owner"
    assert fence.bound_sha == _git(repo, "log", "-1", "--format=%H",
                                   "--", BRIEF_RELPATH)
    # The bound_sha fact carries the terminal caveat: the SHA binds the
    # committed adoption record, never an active fence.
    facts = {f.fact_id: f for f in fence.facts}
    caveat = facts["brief.adoption_bound_sha"].caveat
    assert "K-AUTH-2" in caveat
    assert "not an active fence" in caveat
    # And the rendered verify summary mirrors the caveat next to the SHA.
    md = cmd_brief.run_verify_adoption(repo, path).render_markdown()
    assert fence.bound_sha in md
    assert "not an active fence" in md


@requires_git
def test_terminal_and_untracked_cap_reasons_both_survive(tmp_path):
    # SUPERSEDED + untracked: the committedness cap_reason must survive the
    # terminal note (both cap this brief), and the findings pair stays
    # [REVIEW ADOPTION_NOT_COMMITTED, INFO BRIEF_LIFECYCLE_TERMINAL].
    repo = build_adoption_repo(tmp_path)
    path = _add_brief(repo, state="SUPERSEDED", commit=False)
    fence, findings, refusal = verify_adoption(path, repo)
    assert refusal is None
    assert fence.fence_active is False
    assert fence.bound_sha == ""
    assert "untracked" in fence.cap_reason  # committedness reason kept
    assert "no longer fences new work" in fence.cap_reason  # terminal note appended
    assert [(f.severity, f.code) for f in findings] == [
        (Severity.REVIEW, "ADOPTION_NOT_COMMITTED"),
        (Severity.INFO, "BRIEF_LIFECYCLE_TERMINAL")]


# --- (h) unknown state -> operational error (CLI exit 2) ---------------------------

@requires_git
def test_unknown_state_is_operational_error(tmp_path, capsys):
    repo = build_adoption_repo(tmp_path)
    _add_brief(repo, state="ADOPTED")  # not in the brief lifecycle vocabulary
    with pytest.raises(HarnessOperationalError) as exc:
        verify_adoption(repo / BRIEF_RELPATH, repo)
    assert "ADOPTED" in str(exc.value)
    rc = harness.main(["--repo-root", str(repo),
                       "brief", "--verify-adoption", BRIEF_RELPATH])
    assert rc == 2
    assert "ERROR" in capsys.readouterr().err


def test_missing_tranche_id_or_state_is_operational_error():
    with pytest.raises(HarnessOperationalError, match="tranche_id"):
        parse_brief_markdown("# brief\n\n- state: CANDIDATE\n")
    with pytest.raises(HarnessOperationalError, match="state"):
        parse_brief_markdown("# brief\n\n- tranche_id: `TRB-x`\n")


# --- (i) parse exactness ------------------------------------------------------------

PARSE_EXACTNESS_MD = '''# Tranche brief TRB-parse-001 — CANDIDATE

- tranche_id: `TRB-parse-001`
- state: CANDIDATE
  - lifecycle: CANDIDATE → HUMAN_ADOPTED → …
  - (brief lifecycle is metadata on harness artifacts only)
- objective: fixture objective with a colon: kept verbatim
  - source: none — never invented (K-INVENT-1)
- adopted_by: TBD — on adoption, replace with an allowlisted actor
- adopted_on: TBD

## source_basis

- status: Current State 'CHECKING' (line 3)
  - source: `projects/fixture/_STATUS.md`

## read_scope

- `projects/fixture/execution/DEL-01-01/**`
- `projects/fixture/execution/DEL-01-01/_REFERENCES.md (declared references surface)`
  - source: deliverable directory located via manifest `status_glob` (`execution/*/_STATUS.md`)

## write_scope

- `projects/fixture/execution/DEL-01-01/**`
  - source: plan v3 tranche-brief schema

## prohibited_paths

- `_DomainEngines/**`
- `docs/**`
  - source: profile `protected_write_paths`

## validations (declared, not run)

- python3 -m pytest -q tests (cwd: .) — declared in the adapter manifest; NOT run by this command
  - source: `projects/fixture/_harness/adapter.yaml`

## evidence_targets

- `_harness_generated/evidence/TRB-parse-001/` (under the declared generated root; D-GOV-01)

## stop_conditions

- an out-of-scope write attempt (outside write_scope or into prohibited_paths)

## human_decision_points

- adoption of this brief itself (human edits state to HUMAN_ADOPTED and commits; D-GOV-04)
'''


def test_parse_exactness_backticks_parentheticals_subbullets():
    fence = parse_brief_markdown(PARSE_EXACTNESS_MD)
    assert fence.tranche_id == "TRB-parse-001"
    assert fence.state == "CANDIDATE"
    assert fence.objective == "fixture objective with a colon: kept verbatim"
    assert fence.adopted_by == "" and fence.adopted_on == ""  # TBD -> absent
    # Backticks stripped; a parenthetical INSIDE the backticks is entry text.
    assert fence.read_scope == [
        "projects/fixture/execution/DEL-01-01/**",
        "projects/fixture/execution/DEL-01-01/_REFERENCES.md "
        "(declared references surface)",
    ]
    assert fence.write_scope == ["projects/fixture/execution/DEL-01-01/**"]
    # Sub-bullets ("  - source: ...") never leak into the entries.
    assert fence.prohibited_paths == ["_DomainEngines/**", "docs/**"]
    # Plain-text entries kept whole (mid-string parentheticals intact).
    assert fence.validations == [
        "python3 -m pytest -q tests (cwd: .) — declared in the adapter "
        "manifest; NOT run by this command",
    ]
    # Trailing parenthetical AFTER the closing backtick is tolerated/dropped.
    assert fence.evidence_targets == [
        "_harness_generated/evidence/TRB-parse-001/"]
    assert fence.stop_conditions == [
        "an out-of-scope write attempt (outside write_scope or into "
        "prohibited_paths)"]
    assert fence.human_decision_points == [
        "adoption of this brief itself (human edits state to HUMAN_ADOPTED "
        "and commits; D-GOV-04)"]
    assert fence.fence_active is False  # parsing never activates a fence


STATE_BULLET_AFTER_HEADING_MD = '''# Tranche brief TRB-parse-002 — CANDIDATE

- tranche_id: `TRB-parse-002`
- state: CANDIDATE

## stop_conditions

- state: HUMAN_ADOPTED

## human_decision_points

- adopted_by: fixture-owner
'''


def test_state_shaped_bullet_after_first_heading_never_overrides_header():
    # Header bullets are read only BEFORE the first H2 heading: a
    # `- state:`-shaped bullet inside a later section is ordinary entry text
    # and must not override the header state (or any other header field).
    fence = parse_brief_markdown(STATE_BULLET_AFTER_HEADING_MD)
    assert fence.state == "CANDIDATE"
    assert fence.adopted_by == ""  # section bullet never fills a header field
    assert fence.stop_conditions == ["state: HUMAN_ADOPTED"]
    assert fence.human_decision_points == ["adopted_by: fixture-owner"]


# --- (j) adopted brief inside the scratch root -> ADOPTION_IN_SCRATCH_DIR ----------

@requires_git
def test_adopted_brief_in_scratch_dir_never_exists_for_reliance(tmp_path):
    repo = build_adoption_repo(tmp_path)
    rel = GENERATED_ROOT_NAME + "/briefs/TRB-fixture-001.md"
    # Even force-added AND committed: a scratch-root adoption does not exist
    # for reliance (D-GOV-04) — the location check wins.
    path = _add_brief(repo, relpath=rel, commit=True)
    fence, findings, refusal = verify_adoption(path, repo)
    assert refusal is None
    assert fence.fence_active is False
    hits = _findings(findings, "ADOPTION_IN_SCRATCH_DIR")
    assert len(hits) == 1 and hits[0].severity is Severity.REVIEW
    assert "scratch directory" in hits[0].message
    assert "D-GOV-04" in hits[0].message
    assert fence.bound_sha == ""


@requires_git
def test_case_variant_scratch_dir_is_still_scratch(tmp_path):
    # A case-variant spelling of the scratch root (physically the scratch
    # tree on macOS's case-insensitive default filesystem) must classify as
    # scratch — the check casefolds path components (fail-closed for
    # adoption), so it never yields an active fence on any platform.
    repo = build_adoption_repo(tmp_path)
    rel = "_HARNESS_GENERATED/briefs/TRB-u.md"
    path = _add_brief(repo, relpath=rel, commit=True)
    fence, findings, refusal = verify_adoption(path, repo)
    assert refusal is None
    assert fence.fence_active is False
    hits = _findings(findings, "ADOPTION_IN_SCRATCH_DIR")
    assert len(hits) == 1 and hits[0].severity is Severity.REVIEW
    assert fence.bound_sha == ""


@requires_git
def test_symlinked_generated_root_never_breaks_unrelated_verification(tmp_path, capsys):
    # The scratch classifier is a lexical read-path check, decoupled from the
    # write guard: a symlinked _harness_generated/ (which the WRITE guard
    # refuses) must not make verification of an unrelated, correctly
    # committed brief fail.
    repo = build_adoption_repo(tmp_path)
    path = _add_brief(repo)
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    (repo / GENERATED_ROOT_NAME).symlink_to(elsewhere)
    fence, findings, refusal = verify_adoption(path, repo)
    assert refusal is None and findings == []
    assert fence.fence_active is True
    rc = harness.main(["--repo-root", str(repo),
                       "brief", "--verify-adoption", BRIEF_RELPATH])
    assert rc == 0
    assert "fence_active: True" in capsys.readouterr().out


# --- (j2) symlinked / ..-containing brief paths are refused (exit 2) ---------------

@requires_git
def test_untracked_symlink_to_committed_brief_is_refused(tmp_path, capsys):
    # An UNTRACKED symlink pointing at a committed adopted brief must never
    # verify (resolve() would silently follow it and report a different
    # source_path than the caller passed) — operational refusal, exit 2.
    repo = build_adoption_repo(tmp_path)
    _add_brief(repo)
    link = repo / "docs" / "link-brief.md"
    link.symlink_to(repo / BRIEF_RELPATH)
    with pytest.raises(HarnessOperationalError) as exc:
        verify_adoption(link, repo)
    assert "symlink" in str(exc.value)
    assert "link-brief.md" in str(exc.value)
    rc = harness.main(["--repo-root", str(repo),
                       "brief", "--verify-adoption", "docs/link-brief.md"])
    assert rc == 2
    captured = capsys.readouterr()
    assert "ERROR" in captured.err and "symlink" in captured.err
    assert "fence_active: True" not in captured.out  # never an active fence


@requires_git
def test_brief_inside_symlinked_subdirectory_is_refused(tmp_path):
    repo = build_adoption_repo(tmp_path)
    _add_brief(repo)
    link_dir = repo / "briefs_link"
    link_dir.symlink_to(repo / "docs" / "governance_harness" / "briefs")
    with pytest.raises(HarnessOperationalError) as exc:
        verify_adoption(link_dir / "TRB-fixture-001.md", repo)
    assert "briefs_link" in str(exc.value)
    assert "real committed path" in str(exc.value)


@requires_git
def test_dotdot_component_in_brief_path_is_refused(tmp_path):
    repo = build_adoption_repo(tmp_path)
    _add_brief(repo)
    with pytest.raises(HarnessOperationalError,
                       match=r"without \.\. components"):
        verify_adoption(Path("docs/../" + BRIEF_RELPATH), repo)


# --- (k) round-trip: run_brief output parses back ----------------------------------

def test_generated_brief_round_trips_through_parser(tmp_path):
    repo = build_mini_repo(tmp_path)
    piping = repo / "projects" / "chirality-piping"
    app_dev = repo / "projects" / "chirality-app-dev"
    report = cmd_brief.run_brief(
        repo, piping, [app_dev], deliverable="DEL-01-02", objective=None,
        tranche_id="TRB-round-trip-001", out_dir=repo / GENERATED_ROOT_NAME)
    md_rel = report.summary["written"][0]
    fence = parse_brief_markdown((repo / md_rel).read_text(encoding="utf-8"))
    payload = report.extras["brief"]
    assert fence.tranche_id == "TRB-round-trip-001"
    assert fence.state == "CANDIDATE"
    assert fence.adopted_by == "" and fence.adopted_on == ""  # TBD placeholders
    assert fence.read_scope == payload["read_scope"]
    assert fence.write_scope == payload["write_scope"]
    assert fence.prohibited_paths == payload["prohibited_paths"]
    assert fence.validations == payload["validations"]  # 'none declared' -> []
    assert fence.evidence_targets == payload["evidence_targets"]
    assert fence.stop_conditions == payload["stop_conditions"]
    assert fence.human_decision_points == payload["human_decision_points"]
    # And the verify command reads the generated candidate as exactly that.
    verify = cmd_brief.run_verify_adoption(repo, repo / md_rel)
    assert verify.summary["fence_active"] is False
    assert [f.code for f in verify.findings] == ["BRIEF_NOT_ADOPTED"]


# --- (l) next: counts, listing order, DEL-id rule, truncation ----------------------

def test_next_counts_listing_and_del_id_rule(tmp_path):
    repo = build_mini_repo(tmp_path)
    piping = repo / "projects" / "chirality-piping"
    # An active deliverable directory WITHOUT a DEL-NN-MM prefix.
    _write(piping / "execution" / "PKG-01_Fixture Pkg" / "1_Working"
           / "NOTDEL_misc" / "_STATUS.md", STATUS_MATCH)
    report = cmd_next.run_next(repo, [piping], harness._alias_by_root(repo))
    fact = next(f for f in report.facts
                if f.fact_id == "next.chirality-piping.state_counts")
    assert fact.value == "CHECKING=2, IN_PROGRESS=1, SEMANTIC_READY=1, UNPARSEABLE=1"
    assert "execution/PKG-*/1_Working/*/_STATUS.md" in fact.source_path
    assert report.findings == []  # a view, like status
    md = report.render_markdown()
    rows = [line for line in md.splitlines() if line.startswith("| `")]
    # Precedence order CHECKING > IN_PROGRESS > SEMANTIC_READY, then name.
    assert [r.split("|")[1].strip() for r in rows] == [
        "`DEL-01-02_Second fixture`", "`NOTDEL_misc`",
        "`DEL-01-01_Fixture deliverable with spaces`",
        "`DEL-01-03_Third fixture`"]
    assert ("`python3 tools/practitioner_harness/harness.py brief "
            "--project piping --deliverable DEL-01-02`") in rows[0]
    assert "no DEL-NN-MM id prefix" in rows[1]  # never invented
    assert "_STATUS.md:3" in rows[0]  # Current State source path:line
    assert "Truncated" not in md  # 4 active rows, under the cap


def test_next_lists_blocked_on_tokens_from_status(tmp_path):
    repo = build_mini_repo(tmp_path)
    piping = repo / "projects" / "chirality-piping"
    status = (
        piping
        / "execution"
        / "PKG-01_Fixture Pkg"
        / "1_Working"
        / "DEL-01-02_Second fixture"
        / "_STATUS.md"
    )
    status.write_text(
        status.read_text(encoding="utf-8").replace(
            "**Last Updated:** 2026-06-04",
            "**Last Updated:** 2026-06-04\n**blocked-on:** D-APP-47, D-30",
        ),
        encoding="utf-8",
    )

    report = cmd_next.run_next(repo, [piping], harness._alias_by_root(repo))
    md = report.render_markdown()

    assert "Blocked-On" in md
    assert "`D-APP-47`, `D-30`" in md


def test_next_truncation_is_explicit(tmp_path):
    repo = tmp_path / "repo"  # a bare tree: exactly 12 active deliverables
    build_project(repo, "chirality-app-dev", {
        f"DEL-03-{i:02d}_Fixture {i}": STATUS_MATCH for i in range(1, 13)
    }, baseline_mismatch=0, baseline_files=12)
    report = cmd_next.run_next(repo, [repo / "projects" / "chirality-app-dev"],
                               harness._alias_by_root(repo))
    md = report.render_markdown()
    rows = [line for line in md.splitlines() if line.startswith("| `")]
    assert len(rows) == 10  # capped
    assert "showing 10 of 12 active row(s); 2 row(s) omitted" in md
    assert report.summary["active.chirality-app-dev"] == 12


def test_next_unmapped_root_never_fabricates_a_command(tmp_path):
    # A project root with NO entry in harness.py PROJECT_ALIASES: the row is
    # emitted with a labeled no-alias note — a `brief --project` command line
    # is never fabricated (K-INVENT-1).
    repo = build_mini_repo(tmp_path)
    unmapped = build_project(repo, "chirality-unmapped", {
        "DEL-09-01_Unmapped fixture": STATUS_MATCH,
    }, baseline_mismatch=0, baseline_files=1)
    report = cmd_next.run_next(repo, [unmapped], harness._alias_by_root(repo))
    md = report.render_markdown()
    rows = [line for line in md.splitlines() if line.startswith("| `")]
    assert len(rows) == 1 and "DEL-09-01" in rows[0]
    assert "brief --project" not in md  # no fabricated command anywhere
    assert "no CLI alias is registered" in rows[0]
    assert "K-INVENT-1" in rows[0]


# --- (m) CLI wiring -----------------------------------------------------------------

@live
def test_cli_next_exits_0_on_live_repo(capsys):
    assert harness.main(["--repo-root", str(LIVE_REPO), "next"]) == 0
    out = capsys.readouterr().out
    assert "practitioner-selected" in out


def test_cli_next_exits_0_on_fixture_repo(tmp_path, capsys):
    repo = build_mini_repo(tmp_path)
    assert harness.main(["--repo-root", str(repo), "next"]) == 0
    capsys.readouterr()


@requires_git
def test_cli_review_verify_exits_0_default_and_1_strict(tmp_path, capsys):
    # A REVIEW-producing verify run (untracked HUMAN_ADOPTED brief): REVIEW
    # is exit 0 by default and exit 1 only under --strict (D-GOV-02).
    repo = build_adoption_repo(tmp_path)
    _add_brief(repo, commit=False)
    rc = harness.main(["--repo-root", str(repo),
                       "brief", "--verify-adoption", BRIEF_RELPATH])
    assert rc == 0
    assert "ADOPTION_NOT_COMMITTED" in capsys.readouterr().out
    rc = harness.main(["--repo-root", str(repo), "--strict",
                       "brief", "--verify-adoption", BRIEF_RELPATH])
    assert rc == 1
    capsys.readouterr()


@requires_git
def test_cli_clean_committed_adoption_exits_0_no_refusal(tmp_path, capsys):
    # Happy path: clean committed adoption, matched actor -> exit 0, active
    # fence in the report, and NOTHING on stderr (no identity refusal).
    repo = build_adoption_repo(tmp_path)
    _add_brief(repo)
    rc = harness.main(["--repo-root", str(repo),
                       "brief", "--verify-adoption", BRIEF_RELPATH])
    assert rc == 0
    captured = capsys.readouterr()
    assert captured.err == ""
    assert "fence_active: True" in captured.out


def test_cli_verify_adoption_missing_path_exits_2(tmp_path, capsys):
    repo = build_mini_repo(tmp_path)
    rc = harness.main(["--repo-root", str(repo), "brief",
                       "--verify-adoption", "docs/briefs/absent.md"])
    assert rc == 2
    assert "ERROR" in capsys.readouterr().err


def test_cli_verify_adoption_rejects_generate_flags(tmp_path, capsys):
    repo = build_mini_repo(tmp_path)
    rc = harness.main(["--repo-root", str(repo), "brief",
                       "--verify-adoption", "docs/briefs/x.md",
                       "--deliverable", "DEL-01-02"])
    assert rc == 2
    err = capsys.readouterr().err
    assert "takes only the brief path" in err and "--deliverable" in err


def test_cli_brief_generate_still_requires_project_and_deliverable(tmp_path, capsys):
    repo = build_mini_repo(tmp_path)
    rc = harness.main(["--repo-root", str(repo), "brief"])
    assert rc == 2
    assert "requires --project and --deliverable" in capsys.readouterr().err
