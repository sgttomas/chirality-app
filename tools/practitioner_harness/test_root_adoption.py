#!/usr/bin/env python3
"""Root working-root adoption tests (`--project root` / `chirality-root`).

Covers the four surfaces the adoption touches:

1. alias resolution — `root`/`chirality-root` resolve to the repository root,
   and the root is deliberately absent from the brief-fence alias table;
2. adapter load + normalization — `root-harness-adapter/v1` at
   `execution/_harness/adapter.yaml` is validated strictly and mapped into the
   loader's internal shape, with location/schema disagreement and ambiguous
   double registration refused;
3. `status` / `drift` against a tmp fixture tree, and the refusals for the
   commands that cannot meaningfully operate on the root;
4. LIVE-tree pins (53 status files, 0 mismatches, 53 historical RETIRED + 0 active), the
   same conscious pin discipline `test_live_baseline.py` applies to app-dev
   0/53 and piping 0/101 — a change here is a conscious pin update in the same
   PR, never a silent one.

`tools/validation/validate_root_harness_adapter.py` (G1) remains the root
adapter's authority; nothing here restates or relaxes its checks.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

import adapter_loader
import adapter_project
import brief_adoption
import cmd_drift
import cmd_run_validations
import cmd_status
import harness
from harness_common import HarnessOperationalError

LIVE_REPO = Path(__file__).resolve().parents[2]

ROOT_ADAPTER_YAML = '''# Root harness adapter (fixture).
schema: root-harness-adapter/v1
product: {product}
working_root: "{working_root}"
execution_root: execution
prd: docs/PRD_ROOT.md
coordination: execution/_Coordination/CURRENT_WORKPLAN.md
decision_register: docs/governance_harness/_DECISIONS/_REGISTER.md
status_glob: execution/PKG-*/1_Working/DEL-*/_STATUS.md
states:
  - OPEN
  - INITIALIZED
  - SEMANTIC_READY
  - IN_PROGRESS
  - CHECKING
  - ISSUED
parser_dialect: prose-bullet-v1
exclude_globs:
  - ".archive/**"
baselines:
  status_files: {status_files}
  status_mismatch: {status_mismatch}
  pinned_at: {pinned_at}
'''

STATUS_OPEN = '''# Status: {del_id}

**Current State:** OPEN
**Last Updated:** 2026-07-25

## History
- 2026-07-25 - State set to OPEN (materialization)
'''

STATUS_MISMATCH = '''# Status: {del_id}

**Current State:** OPEN
**Last Updated:** 2026-07-25

## History
- 2026-07-25 - State set to OPEN (materialization)
- 2026-07-25 - State moved to IN_PROGRESS (fixture drift)
'''


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def build_root_repo(
    tmp_path: Path,
    statuses: dict[str, str] | None = None,
    status_files: int = 2,
    status_mismatch: int = 0,
    product: str = "chirality-root",
    working_root: str = ".",
) -> Path:
    """A minimal ROOT working root: adapter at `execution/_harness/adapter.yaml`,
    a PRD, a coordination surface, a decision register, and `PKG-*/1_Working/
    DEL-*/_STATUS.md` deliverables."""
    repo = tmp_path / "repo"
    repo.mkdir(exist_ok=True)
    _write(repo / "execution" / "_harness" / "adapter.yaml",
           ROOT_ADAPTER_YAML.format(
               product=product, working_root=working_root,
               status_files=status_files, status_mismatch=status_mismatch,
               pinned_at="653fabc9b3e8abf369f5e776a7d3ee24bf235e7a"))
    _write(repo / "docs" / "PRD_ROOT.md",
           "# PRD (fixture)\n\n**Status:** ADOPTION-READY (fixture)\n")
    _write(repo / "execution" / "_Coordination" / "CURRENT_WORKPLAN.md",
           "# Workplan (fixture)\n\nStatus: ACTIVE (fixture)\n")
    _write(repo / "docs" / "governance_harness" / "_DECISIONS" / "_REGISTER.md",
           "# Register\n\n| ID | Decision | State |\n|---|---|---|\n"
           "| D-GOV-21 | Fixture | RULED |\n")
    if statuses is None:
        statuses = {
            "DEL-01-01_First": STATUS_OPEN,
            "DEL-01-02_Second": STATUS_OPEN,
        }
    for name, template in statuses.items():
        _write(repo / "execution" / "PKG-01_Fixture Pkg" / "1_Working" / name
               / "_STATUS.md", template.format(del_id=name.split("_")[0]))
    return repo


# --- 1. alias resolution --------------------------------------------------------

def test_root_aliases_resolve_to_the_repository_root(tmp_path):
    repo = build_root_repo(tmp_path)
    for alias in harness.ROOT_ALIASES:
        assert harness._project_root(repo, alias) == repo
    # No malformed `…/.` join: the resolved path is the repo root itself.
    assert "." not in harness._project_root(repo, "root").parts


def test_root_aliases_are_registered_and_observable_but_not_full_citizens():
    assert set(harness.ROOT_ALIASES) <= set(harness.PROJECT_ALIASES)
    assert all(harness.PROJECT_ALIASES[a] == harness.ROOT_RELPATH
               for a in harness.ROOT_ALIASES)
    assert set(harness.ROOT_ALIASES) <= set(harness.OBSERVABLE_PROJECTS)
    assert not set(harness.ROOT_ALIASES) & set(harness.FULL_CITIZENSHIP_PROJECTS)


def test_root_is_excluded_from_the_brief_fence_alias_table(tmp_path):
    """The reverse alias table is also the brief-fence resolution table; the
    repository root would prefix-match every write_scope entry."""
    repo = tmp_path / "repo"
    repo.mkdir()
    by_root = harness._alias_by_root(repo)
    assert repo.resolve() not in by_root
    assert set(by_root.values()) == {"pec", "piping", "app-dev", "runtime"}


def test_fence_resolution_still_refuses_paths_outside_a_project(tmp_path):
    """Regression pin: adding the root alias must not turn this refusal into a
    catch-all match on the repository root."""
    repo = tmp_path / "repo"
    (repo / "projects" / "chirality-piping").mkdir(parents=True)
    fence = brief_adoption.BriefFence(
        tranche_id="TRB-FIXTURE", state="HUMAN_ADOPTED",
        write_scope=["docs/governance_harness/whatever.md"])
    with pytest.raises(HarnessOperationalError) as exc:
        cmd_run_validations._resolve_project_root(
            repo, fence, harness._alias_by_root(repo))
    assert "registered pilot project root" in str(exc.value)


# --- 2. adapter load + normalization --------------------------------------------

def test_root_adapter_loads_and_normalizes_into_the_internal_shape(tmp_path):
    repo = build_root_repo(tmp_path, status_files=2, status_mismatch=0)
    m = adapter_loader.load_adapter(repo)
    assert m.kind == adapter_loader.KIND_ROOT
    assert m.schema == adapter_loader.ROOT_ADAPTER_SCHEMA
    # product -> project; prd -> plan.
    assert m.project == "chirality-root"
    assert m.plan == "docs/PRD_ROOT.md"
    # baselines.* -> drift_baseline_*.
    assert m.drift_baseline_files == 2
    assert m.drift_baseline_mismatch == 0
    assert m.baseline_pinned_at == "653fabc9b3e8abf369f5e776a7d3ee24bf235e7a"
    # Root-only declarations preserved.
    assert m.working_root == "." and m.execution_root == "execution"
    # Absent fields are marked absent, never guessed.
    assert m.dag_pointer == "" and m.declares_dag_pointer() is False
    assert m.validation_commands == [] and m.declares_validation_commands() is False
    assert m.states[0] == "OPEN" and m.states[-1] == "ISSUED"
    assert m.exclude_globs == [".archive/**"]
    assert m.manifest_path == repo / "execution" / "_harness" / "adapter.yaml"
    assert m.manifest_relpath(repo) == "execution/_harness/adapter.yaml"


def test_project_manifest_still_reports_kind_project(tmp_path):
    from test_self_check_fixtures import build_mini_repo
    repo = build_mini_repo(tmp_path)
    m = adapter_loader.load_adapter(repo / "projects" / "chirality-piping")
    assert m.kind == adapter_loader.KIND_PROJECT
    assert m.declares_dag_pointer() is True
    assert m.manifest_relpath(repo) == "projects/chirality-piping/_harness/adapter.yaml"


@pytest.mark.parametrize("key", [
    "product", "working_root", "execution_root", "prd", "coordination",
    "decision_register", "status_glob", "states", "parser_dialect", "baselines",
])
def test_root_adapter_missing_required_key_is_operational_error(tmp_path, key):
    repo = build_root_repo(tmp_path)
    manifest = repo / "execution" / "_harness" / "adapter.yaml"
    lines = manifest.read_text(encoding="utf-8").splitlines()
    kept: list[str] = []
    dropping = False
    for line in lines:
        if line.startswith(f"{key}:"):
            dropping = True
            continue
        if dropping and (line.startswith(" ") or line.startswith("-")):
            continue
        dropping = False
        kept.append(line)
    manifest.write_text("\n".join(kept) + "\n", encoding="utf-8")
    with pytest.raises(HarnessOperationalError) as exc:
        adapter_loader.load_adapter(repo)
    assert key in str(exc.value)


@pytest.mark.parametrize("baseline_key", ["status_files", "status_mismatch", "pinned_at"])
def test_root_adapter_missing_baseline_key_is_operational_error(tmp_path, baseline_key):
    repo = build_root_repo(tmp_path)
    manifest = repo / "execution" / "_harness" / "adapter.yaml"
    manifest.write_text("\n".join(
        line for line in manifest.read_text(encoding="utf-8").splitlines()
        if not line.strip().startswith(f"{baseline_key}:")) + "\n", encoding="utf-8")
    with pytest.raises(HarnessOperationalError) as exc:
        adapter_loader.load_adapter(repo)
    assert baseline_key in str(exc.value)


def test_root_adapter_non_integer_baseline_is_operational_error(tmp_path):
    repo = build_root_repo(tmp_path)
    manifest = repo / "execution" / "_harness" / "adapter.yaml"
    manifest.write_text(
        manifest.read_text(encoding="utf-8").replace(
            "status_files: 2", 'status_files: "forty-five"'),
        encoding="utf-8")
    with pytest.raises(HarnessOperationalError) as exc:
        adapter_loader.load_adapter(repo)
    assert "must be an integer" in str(exc.value)


def test_root_adapter_mismatch_exceeding_files_is_operational_error(tmp_path):
    repo = build_root_repo(tmp_path, status_files=2, status_mismatch=3)
    with pytest.raises(HarnessOperationalError) as exc:
        adapter_loader.load_adapter(repo)
    assert "exceeds" in str(exc.value)


def test_root_adapter_working_root_must_be_dot(tmp_path):
    repo = build_root_repo(tmp_path, working_root="execution")
    with pytest.raises(HarnessOperationalError) as exc:
        adapter_loader.load_adapter(repo)
    assert "working_root" in str(exc.value)


def test_project_schema_at_the_root_location_is_refused(tmp_path):
    """No silent fallback between the two shapes: location and schema agree or
    the loader refuses."""
    repo = build_root_repo(tmp_path)
    manifest = repo / "execution" / "_harness" / "adapter.yaml"
    manifest.write_text(
        manifest.read_text(encoding="utf-8").replace(
            "root-harness-adapter/v1", "practitioner-harness-adapter/v1"),
        encoding="utf-8")
    with pytest.raises(HarnessOperationalError) as exc:
        adapter_loader.load_adapter(repo)
    assert "location and schema must agree" in str(exc.value)


def test_root_schema_at_the_project_location_is_refused(tmp_path):
    project = tmp_path / "proj"
    _write(project / "_harness" / "adapter.yaml",
           ROOT_ADAPTER_YAML.format(
               product="chirality-root", working_root=".", status_files=0,
               status_mismatch=0, pinned_at="653fabc"))
    with pytest.raises(HarnessOperationalError) as exc:
        adapter_loader.load_adapter(project)
    assert "location and schema must agree" in str(exc.value)


def test_both_registered_locations_present_is_ambiguous(tmp_path):
    from test_self_check_fixtures import ADAPTER_YAML
    repo = build_root_repo(tmp_path)
    _write(repo / "_harness" / "adapter.yaml", ADAPTER_YAML.format(
        project="chirality-root", baseline_mismatch=0, baseline_files=2,
        requires_sha="false", sha_field=""))
    with pytest.raises(HarnessOperationalError) as exc:
        adapter_loader.load_adapter(repo)
    assert "Ambiguous adapter registration" in str(exc.value)


def test_absent_manifest_names_both_registered_locations(tmp_path):
    empty = tmp_path / "empty"
    empty.mkdir()
    with pytest.raises(HarnessOperationalError) as exc:
        adapter_loader.load_adapter(empty)
    message = str(exc.value)
    assert "_harness/adapter.yaml" in message
    assert "execution/_harness/adapter.yaml" in message


def test_absent_dag_pointer_is_reported_not_applicable(tmp_path):
    repo = build_root_repo(tmp_path)
    manifest = adapter_loader.load_adapter(repo)
    facts = adapter_project.dag_pointer_facts(manifest, repo)
    assert len(facts) == 1
    fact = facts[0]
    assert fact.fact_id == "dag.pointer"
    assert fact.parse_status == "NOT_APPLICABLE"
    assert "not declared by this adapter schema" in fact.value
    # The manifest itself is cited — never an empty or joined-empty path.
    assert fact.source_path == "execution/_harness/adapter.yaml"


# --- 3. status / drift / refusals on a fixture tree ------------------------------

def test_status_root_fixture_reports_the_states_and_the_prd(tmp_path):
    repo = build_root_repo(tmp_path)
    report = cmd_status.run_status_project(repo, repo)
    md = report.render_markdown()
    assert "# Status — chirality-root" in md
    assert "PRD posture" in md
    assert "`docs/PRD_ROOT.md`: artifact present" in md
    assert "| OPEN | 2 |" in md
    assert "not declared by this adapter schema (root-harness-adapter/v1)" in md
    assert report.summary["status_files"] == 2
    assert report.summary["project"] == "chirality-root"


def test_drift_root_fixture_measures_and_cites_the_root_adapter(tmp_path):
    repo = build_root_repo(tmp_path, statuses={
        "DEL-01-01_First": STATUS_OPEN,
        "DEL-01-02_Second": STATUS_MISMATCH,
    }, status_files=2, status_mismatch=0)
    report = cmd_drift.run_drift(repo, [repo])
    assert report.summary["files_total"] == 2
    assert report.summary["mismatches_total"] == 1
    baseline = [f for f in report.findings if f.code == "DRIFT_BASELINE_COMPARISON"]
    assert len(baseline) == 1
    assert baseline[0].source_path == "execution/_harness/adapter.yaml"
    assert "chirality-root: measured 1 mismatch(es) over 2 file(s)" in baseline[0].message


def test_cli_status_and_drift_accept_both_root_aliases(tmp_path, capsys):
    repo = build_root_repo(tmp_path)
    for alias in harness.ROOT_ALIASES:
        assert harness.main(["--repo-root", str(repo), "status",
                             "--project", alias]) == 0
        assert "| OPEN | 2 |" in capsys.readouterr().out
        assert harness.main(["--repo-root", str(repo), "drift",
                             "--project", alias]) == 0
        assert "| chirality-root | 2 | 2 | 0 " in capsys.readouterr().out


def test_cli_brief_refuses_root_with_a_named_reason(tmp_path, capsys):
    repo = build_root_repo(tmp_path)
    rc = harness.main(["--repo-root", str(repo), "brief", "--project", "root",
                       "--deliverable", "DEL-01-01"])
    assert rc == 2
    err = capsys.readouterr().err
    assert "brief does not support --project root" in err
    assert "declares no dag_pointer" in err
    assert "Traceback" not in err


def test_cli_next_refuses_root_with_a_named_reason(tmp_path, capsys):
    repo = build_root_repo(tmp_path)
    rc = harness.main(["--repo-root", str(repo), "next", "--project", "root"])
    assert rc == 2
    err = capsys.readouterr().err
    assert "next does not support --project root" in err
    assert "status --project root" in err


def test_cli_drift_all_with_root_refuses_rather_than_dropping_it(tmp_path, capsys):
    repo = build_root_repo(tmp_path)
    rc = harness.main(["--repo-root", str(repo), "drift", "--project", "root",
                       "--all"])
    assert rc == 2
    assert "must be requested on its own" in capsys.readouterr().err


def test_cli_drift_all_default_scope_excludes_the_root(tmp_path, capsys):
    """Default `drift` behaviour for the pilot projects is untouched."""
    from test_self_check_fixtures import build_mini_repo
    repo = build_mini_repo(tmp_path)
    assert harness.main(["--repo-root", str(repo), "drift", "--all"]) == 0
    out = capsys.readouterr().out
    assert "chirality-root" not in out


# --- 4. LIVE-tree pins ----------------------------------------------------------

live_root = pytest.mark.skipif(
    os.environ.get("CHIRALITY_SKIP_LIVE_TESTS") == "1"
    or not (LIVE_REPO / "execution" / "_harness" / "adapter.yaml").is_file(),
    reason="live root adapter absent (or live tests disabled by env)",
)


def _fact(report, fact_id):
    for f in report.facts:
        if f.fact_id == fact_id:
            return f
    raise AssertionError(f"fact {fact_id} missing: {[f.fact_id for f in report.facts]}")


@live_root
def test_live_root_adapter_pins_53_files_0_mismatch():
    """Conscious pin after the bounded SCA-004 Phase-3 R7 initialization
    (2026-08-23): 6 packages / 53 deliverables, all 53 INITIALIZED.
    A live-root change updates this pin in the same PR — never silently."""
    manifest = adapter_loader.load_adapter(LIVE_REPO)
    assert manifest.kind == adapter_loader.KIND_ROOT
    assert manifest.project == "chirality-root"
    assert manifest.drift_baseline_files == 53
    assert manifest.drift_baseline_mismatch == 0


@live_root
def test_live_root_drift_baseline_0_of_53():
    report = cmd_drift.run_drift(LIVE_REPO, [LIVE_REPO])
    value = _fact(report, "drift.chirality-root").value
    assert "files=53" in value
    assert "matches=53" in value
    assert "mismatches=0" in value
    # The seven Phase-3 lifecycle records now carry the minimum parseable
    # house fields and one state-bearing history entry each.
    assert "unparseable_docs=0" in value
    assert "no_state_assertion=0" in value
    assert report.summary["files_total"] == 53
    assert report.summary["mismatches_total"] == 0
    # The measurement agrees with the adapter's recorded pin.
    baseline = [f for f in report.findings if f.code == "DRIFT_BASELINE_COMPARISON"]
    assert len(baseline) == 1
    assert baseline[0].source_path == "execution/_harness/adapter.yaml"
    assert "measured 0 mismatch(es) over 53 file(s) vs recorded baseline 0/53" \
        in baseline[0].message


@live_root
def test_live_root_status_reports_53_historical_retired_0_active_and_no_dag_pointer():
    # Live pin: the 53 accepted SCA-005 historical sources are RETIRED.
    # Root has no active product carriers; observation grants no activation.
    # A change to the live root tree updates this pin in the same PR.
    report = cmd_status.run_status_project(LIVE_REPO, LIVE_REPO)
    md = report.render_markdown()
    assert "# Status — chirality-root" in md
    assert "| RETIRED | 53 |" in md
    assert "Historical source census (not active workload)" in md
    assert "Historical sources have no production eligibility" in md
    assert "| INITIALIZED |" not in md
    assert "| IN_PROGRESS |" not in md
    assert "| OPEN |" not in md
    assert report.summary["status_files"] == 53
    assert "not declared by this adapter schema (root-harness-adapter/v1)" in md


@live_root
def test_live_root_cli_status_and_drift_exit_zero(capsys):
    assert harness.main(["--repo-root", str(LIVE_REPO), "status",
                         "--project", "root"]) == 0
    capsys.readouterr()
    assert harness.main(["--repo-root", str(LIVE_REPO), "drift",
                         "--project", "root"]) == 0
    capsys.readouterr()


def test_explicit_unknown_root_mode_is_refused(tmp_path):
    repo = tmp_path / "root"
    path = repo / "execution/_harness/adapter.yaml"
    path.parent.mkdir(parents=True)
    path.write_text(ROOT_ADAPTER_YAML.format(product="chirality-root", working_root=".",
        status_files=53, status_mismatch=0, pinned_at="fixture") + "mode: unregistered-mode\n")
    with pytest.raises(HarnessOperationalError, match="Unknown explicit Root mode"):
        adapter_loader.load_adapter(repo)

def test_root_legacy_shape_cannot_hide_governance_state_without_mode(tmp_path):
    repo=build_root_repo(tmp_path)
    path=repo/'execution/_harness/adapter.yaml'
    with path.open('a') as out:out.write('\ngovernance_state: {path: state.json, sha256: fixture}\n')
    with pytest.raises(HarnessOperationalError,match='explicit governance-only mode'):
        adapter_loader.load_adapter(repo)

def test_runtime_aliases_are_ordinary_project_observation_entries(tmp_path):
    for alias in ('runtime','chirality-runtime'):
        assert harness.PROJECT_ALIASES[alias]=='projects/chirality-runtime'
        assert alias in harness.OBSERVABLE_PROJECTS
        assert alias not in harness.ROOT_ALIASES
    assert harness.PROJECT_ALIASES['runtime']!='.'
