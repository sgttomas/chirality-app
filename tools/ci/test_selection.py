"""Exercise real Git changes and the required-job result contract."""
from __future__ import annotations

import json
import os
import re
from pathlib import Path
import subprocess

import pytest
import yaml

from tools.ci import nightly_gate
from tools.ci import select_checks as subject


def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args]).decode().strip()


def write(repo, path, text="document\n"):
    target = repo / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text)
    return target


def commit(repo):
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", "fixture")
    return git(repo, "rev-parse", "HEAD")


@pytest.fixture
def repo(tmp_path):
    git(tmp_path, "init", "-q")
    git(tmp_path, "config", "user.name", "CI fixture")
    git(tmp_path, "config", "user.email", "ci@example.invalid")
    git(tmp_path, "config", "core.filemode", "true")
    write(tmp_path, ".fixture")
    commit(tmp_path)
    return tmp_path


def selection(repo, base):
    return subject.select(repo, "pull_request", base, commit(repo))


def test_prose_only_reports_every_path_and_commit_identity(repo):
    base = git(repo, "rev-parse", "HEAD")
    for path in subject.PROSE_PATHS:
        write(repo, path)
    result = selection(repo, base)
    assert result["mode"] == "prose" and result["run_product"] is False
    assert result["merge_base"] == result["base"] == base
    assert result["head"] == git(repo, "rev-parse", "HEAD")
    assert {item["path"] for item in result["changes"]} == subject.PROSE_PATHS
    assert all(item["reason"] and item["checks"] == "repository" for item in result["changes"])


def test_ordinary_prose_modification(repo):
    write(repo, "AGENTS.md")
    base = commit(repo)
    write(repo, "AGENTS.md", "revised instructions\n")
    result = selection(repo, base)
    assert result["run_product"] is False
    assert result["changes"][0]["status"] == "M"


@pytest.mark.parametrize("paths", [
    # PR149: project-reference corrections; both guides previously escalated.
    ["AGENTS.md", "README.md", "docs/OPERATING_METHOD.md", "docs/user-manual/README.md"],
    # PR148: the punchlist previously escalated this two-file change.
    ["execution/_Coordination/CURRENT_EXECUTION_BASIS.md",
     "execution/_Coordination/PUBLICATION_PUNCHLIST.md"],
])
def test_real_documentary_prs_do_not_select_product(repo, paths):
    for path in paths:
        write(repo, path)
    base = commit(repo)
    for path in paths:
        write(repo, path, "updated documentary text\n")
    result = selection(repo, base)
    assert not result["run_product"]
    assert {item["path"] for item in result["changes"]} == set(paths)


def test_pr162_typed_headers_and_adoption_still_select_product(repo):
    # Complete PR162 path set: metadata prose mixed with workflow/validator inputs.
    paths = [
        '.github/workflows/governance-harness.yml',
        'AGENTS.md',
        'docs/ARCHITECTURE.md',
        'docs/CI_SELECTION.md',
        'docs/EXAMINATION.md',
        'docs/HOST_INTEGRATION.md',
        'docs/OPERATING_METHOD.md',
        'docs/PRD.md',
        'docs/user-manual/README.md',
        'docs/user-manual/creating-workflows.md',
        'docs/user-manual/finding-conversations.md',
        'docs/user-manual/sending-and-interrupting.md',
        'docs/user-manual/setting-up.md',
        'docs/user-manual/using-workflows.md',
        'docs/user-manual/workflows/define-work.md',
        'docs/user-manual/workflows/engineering-planning.md',
        'execution/PKG-10/DEL-10-01/Work/LIBRARY_V3_RECEIVING.md',
        'execution/PKG-10/DEL-10-01/deliverable.yaml',
        'execution/_Coordination/CURRENT_EXECUTION_BASIS.md',
        'init/README.md',
        'init/init-prompt.md',
        'loop/LOOP_INIT.md',
        'reference/library-v3.0.0/MANIFEST.json',
        'reference/library-v3.0.0/README.md',
        'reference/library-v3.0.0/document-metadata.schema.json',
        'reference/library-v3.0.0/source/LICENSE.md',
        'reference/library-v3.0.0/source/agents/AGENT_HELPS_HUMANS.md',
        'reference/library-v3.0.0/source/agents/AGENT_HELP_HUMAN.md',
        'reference/library-v3.0.0/source/agents/AGENT_INTERLOCUTOR.md',
        'reference/library-v3.0.0/source/agents/AGENT_TASK.md',
        'reference/library-v3.0.0/source/agents/AGENT_WORKING_ITEMS.md',
        'reference/library-v3.0.0/source/agents/registry.json',
        'reference/library-v3.0.0/source/tools/validation/build_workflow_index.py',
        'reference/library-v3.0.0/source/tools/validation/validate_agent_instructions.py',
        'reference/library-v3.0.0/source/tools/workflow_runtime/resolve_workflow.py',
        'tools/deliverables/README.md',
        'tools/validation/test_document_metadata.py',
        'tools/validation/test_library_v2_1_operational_adoption.py',
        'tools/validation/test_library_v3_operational_adoption.py',
    ]
    base = git(repo, "rev-parse", "HEAD")
    for path in paths:
        write(repo, path)
    result = selection(repo, base)
    assert result["mode"] == "product" and result["run_product"]
    assert {item["path"] for item in result["changes"]} == set(paths)
    assert next(item for item in result["changes"]
                if item["path"] == ".github/workflows/governance-harness.yml")["checks"] == "product"


def test_tracked_path_completeness_and_unknown_full_fallback(repo, monkeypatch):
    (repo / ".fixture").unlink()
    write(repo, "AGENTS.md")
    write(repo, "app/new-module.rs")
    base = commit(repo)
    assert subject.inventory(repo) == {"tracked_paths": 2, "unmatched": [], "collisions": [], "links": []}
    path = "new-domain/README.md"
    write(repo, path)
    result = selection(repo, base)
    assert result["run_product"]
    assert result["changes"][0]["rule"] == "unmatched"
    assert subject.inventory(repo)["unmatched"] == [path]
    command = ["python3", str(Path(subject.__file__)), "inventory", "--repo", str(repo)]
    failed = subprocess.run(command, capture_output=True, text=True)
    assert failed.returncode == 2 and path in failed.stdout
    # An intentional rule, not the full-coverage fallback, clears completeness.
    monkeypatch.setattr(subject, "PROSE_PATHS", subject.PROSE_PATHS | {path})
    assert subject.inventory(repo)["unmatched"] == []


def test_repository_has_no_unclassified_tracked_paths():
    assert subject.inventory(Path(subject.__file__).resolve().parents[2])["unmatched"] == []


@pytest.mark.parametrize("path", [
    "new-domain/README.md", ".github/ISSUE_TEMPLATE/README.md", "init/new-guide.md",
    "loop/new-input.json", "new-root.rs",
    # Retired entry and record locations no longer have a rule.
    "init/init-prompt.md", "loop/LOOP_INIT.md", "conceptual/DECISIONS.md",
    "foundation/thesis/README.md",
])
def test_unknowns_anywhere_keep_every_product_job(repo, path):
    base = git(repo, "rev-parse", "HEAD")
    write(repo, "tools/deliverables/README.md")
    write(repo, path)
    result = selection(repo, base)
    assert result["mode"] == "product" and result["run_product"]
    unknown = next(item for item in result["changes"] if item["path"] == path)
    assert unknown["rule"] == "unmatched" and unknown["checks"] == "product"


@pytest.mark.parametrize("path", [
    "app/src/new.rs", "docs/document-metadata.schema.json", "tools/ci/select_checks.py",
    "reference/library-v3.1.0/README.md",
])
def test_new_documentary_exceptions_do_not_swallow_product_domains(repo, path):
    base = git(repo, "rev-parse", "HEAD")
    write(repo, "docs/OPERATING_METHOD.md")
    write(repo, path)
    result = selection(repo, base)
    assert result["run_product"]
    assert next(item for item in result["changes"] if item["path"] == path)["rule"] == "product-domain"


@pytest.mark.parametrize("path", [
    "app/src/App.tsx", "app/src-tauri/src/hosting.rs", "app/package-lock.json",
    ".github/workflows/governance-harness.yml", "tools/ci/select_checks.py",
    "tools/ci/test_selection.py", ".gitattributes", "unknown.md",
    "app/src-tauri/resources/AGENTS.md", "workflows/example/WORKFLOW.md",
    "app/packaging/README.md",
    "README.MD", "docs/CI_SELECTION.md.py", "unusual\npath\r.md",
])
def test_unknown_product_inputs_and_mixed_changes_keep_product(repo, path):
    base = git(repo, "rev-parse", "HEAD")
    write(repo, "AGENTS.md")
    write(repo, path)
    result = selection(repo, base)
    assert result["run_product"] is True and result["mode"] == "product"
    assert {item["path"] for item in result["changes"]} == {"AGENTS.md", path}
    assert next(item for item in result["changes"] if item["path"] == path)["checks"] == "product"


def test_complete_diff_exceeds_api_page_and_keeps_odd_names(repo):
    base = git(repo, "rev-parse", "HEAD")
    paths = {f"unknown/{index:03}.md" for index in range(120)} | {"unknown/line\nname.md"}
    for path in paths:
        write(repo, path)
    result = selection(repo, base)
    assert {item["path"] for item in result["changes"]} == paths
    assert result["run_product"]


def test_rename_looks_at_old_and_new_path(repo):
    write(repo, "app/src-tauri/resources/AGENTS.md")
    base = commit(repo)
    (repo / "app/src-tauri/resources/AGENTS.md").rename(repo / "AGENTS.md")
    result = selection(repo, base)
    assert result["run_product"]
    assert {(item["path"], item["status"]) for item in result["changes"]} == {
        ("app/src-tauri/resources/AGENTS.md", "D"), ("AGENTS.md", "A"),
    }


@pytest.mark.parametrize("kind", ["delete", "executable", "symlink"])
@pytest.mark.parametrize("relative", ["README.md", "tools/deliverables/README.md",
                                     "execution/_Coordination/PUBLICATION_PUNCHLIST.md"])
def test_deletion_and_type_or_mode_changes_at_allowed_path_keep_product(repo, kind, relative):
    path = write(repo, relative)
    base = commit(repo)
    if kind == "delete":
        path.unlink()
    elif kind == "executable":
        path.chmod(0o755)
    else:
        path.unlink()
        path.symlink_to(".fixture")
    assert selection(repo, base)["run_product"]


def test_merge_base_excludes_base_only_changes_but_keeps_entire_pr(repo):
    original = git(repo, "rev-parse", "HEAD")
    git(repo, "checkout", "-qb", "base-only")
    write(repo, "app/src/base-only.rs")
    base = commit(repo)
    git(repo, "checkout", "-qb", "pr", original)
    write(repo, "README.md")
    commit(repo)
    write(repo, "AGENTS.md")
    result = selection(repo, base)
    assert result["run_product"] is False
    assert result["merge_base"] == original
    assert {item["path"] for item in result["changes"]} == {"README.md", "AGENTS.md"}


def test_empty_change_and_manual_dispatch_keep_product(repo):
    head = git(repo, "rev-parse", "HEAD")
    assert subject.select(repo, "pull_request", head, head)["run_product"]
    assert subject.select(repo, "workflow_dispatch", "", head)["run_product"]


@pytest.mark.parametrize("bad", ["", "HEAD", "--help", "f" * 40])
def test_bad_or_missing_revision_is_failure(repo, bad):
    with pytest.raises((ValueError, subprocess.CalledProcessError)):
        subject.select(repo, "pull_request", bad, git(repo, "rev-parse", "HEAD"))


def test_unrelated_history_and_unsupported_event_fail(repo):
    base = git(repo, "rev-parse", "HEAD")
    git(repo, "checkout", "--orphan", "unrelated")
    write(repo, ".fixture", "other root\n")
    head = commit(repo)
    with pytest.raises(subprocess.CalledProcessError):
        subject.select(repo, "pull_request", base, head)
    with pytest.raises(ValueError):
        subject.select(repo, "push", "", head)


def test_ambiguous_merge_base_fails(repo):
    original = git(repo, "rev-parse", "HEAD")
    tree = git(repo, "rev-parse", "HEAD^{tree}")
    left = git(repo, "commit-tree", tree, "-p", original, "-m", "left")
    right = git(repo, "commit-tree", tree, "-p", original, "-m", "right")
    base = git(repo, "commit-tree", tree, "-p", left, "-p", right, "-m", "base merge")
    head = git(repo, "commit-tree", tree, "-p", right, "-p", left, "-m", "head merge")
    with pytest.raises(ValueError, match="unambiguous"):
        subject.select(repo, "pull_request", base, head)


@pytest.mark.parametrize("raw", [
    b"bad\0path\0", b"bad\0path", b"bad\0", b"\0\0", b"garbage",
])
def test_malformed_diff_fails(raw):
    with pytest.raises(ValueError):
        subject.parse_changes(raw)


def needs(product="true", mode="product", result="success"):
    return {
        "change-selection": {"result": "success", "outputs": {
            "selection_mode": mode, "run_product": product,
        }},
        "repository-checks": {"result": "success", "outputs": {}},
        "app-v4": {"result": result},
    }


def test_aggregate_accepts_only_selected_success_or_explicit_prose_skip():
    subject.require_success(needs())
    subject.require_success(needs("false", "prose", "skipped"))


@pytest.mark.parametrize("result", ["failure", "cancelled", "skipped", "", None])
def test_selected_product_must_succeed(result):
    with pytest.raises(ValueError):
        subject.require_success(needs(result=result))


@pytest.mark.parametrize("result", ["failure", "cancelled", "success", "", None])
def test_prose_skip_is_explicit_and_never_accepts_failure(result):
    with pytest.raises(ValueError):
        subject.require_success(needs("false", "prose", result))


def test_aggregate_rejects_failed_repository_and_invalid_or_missing_outputs():
    examples = [{}, {"app-v4": {}}, needs("", ""), needs("false", "product"),
                needs("true", "prose"), needs("False", "prose")]
    for job in ["change-selection", "repository-checks"]:
        for status in ["failure", "cancelled", "skipped", "", None]:
            for selected in [needs("false", "prose", "skipped"), needs()]:
                selected[job]["result"] = status
                examples.append(selected)
    value = needs()
    del value["change-selection"]["outputs"]
    examples.append(value)
    # Selection decides alone: outputs on repository-checks are never read.
    value = needs()
    value["repository-checks"]["outputs"] = value["change-selection"].pop("outputs")
    examples.append(value)
    for job in ["change-selection", "repository-checks", "app-v4"]:
        value = needs()
        del value[job]
        examples.append(value)
    value = needs()
    value["unexpected"] = {"result": "success"}
    examples.append(value)
    for value in examples:
        with pytest.raises(ValueError):
            subject.require_success(value)


def test_cli_emits_report_and_outputs_only_on_success(repo, tmp_path):
    base = git(repo, "rev-parse", "HEAD")
    write(repo, "AGENTS.md")
    head = commit(repo)
    output, summary = tmp_path / "outputs", tmp_path / "summary"
    script = Path(subject.__file__)
    command = ["python3", str(script), "select", "--event", "pull_request", "--repo", str(repo),
               "--head", head, "--github-output", str(output), "--summary", str(summary)]
    passed = subprocess.run([*command, "--base", base], capture_output=True, text=True)
    assert passed.returncode == 0, passed.stderr
    assert json.loads(passed.stdout)["mode"] == "prose"
    assert output.read_text() == "selection_mode=prose\nrun_product=false\n"
    assert '"path": "AGENTS.md"' in summary.read_text()
    output.unlink()
    failed = subprocess.run([*command, "--base", "not-a-sha"], capture_output=True)
    assert failed.returncode == 2
    assert not output.exists()
    env = {**os.environ, "RESULTS": json.dumps(needs("false", "prose", "skipped"))}
    assert subprocess.run(["python3", str(script), "gate"], env=env, capture_output=True).returncode == 0
    env["RESULTS"] = "not JSON"
    assert subprocess.run(["python3", str(script), "gate"], env=env, capture_output=True).returncode == 2


def test_workflow_always_runs_selection_and_checks_only_explicit_exclusion():
    root = Path(subject.__file__).resolve().parents[2]
    workflow = yaml.safe_load((root / ".github/workflows/governance-harness.yml").read_text())
    # PyYAML 1.1 treats the bare workflow key 'on' as True.
    trigger = workflow.get("on", workflow.get(True))
    assert trigger["pull_request"] is None
    jobs = workflow["jobs"]
    repo = jobs["repository-checks"]
    assert any("python tools/ci/select_checks.py inventory" in step.get("run", "")
               for step in repo["steps"])
    # Repository checks run unconditionally, in parallel with the product jobs.
    assert "needs" not in repo and "if" not in repo and "outputs" not in repo
    assert not any(step.get("id") == "selection" for step in repo["steps"])
    selecting = jobs["change-selection"]
    assert "needs" not in selecting and "if" not in selecting
    assert next(step for step in selecting["steps"] if "uses" in step)["with"]["fetch-depth"] == 0
    select_step = next(step for step in selecting["steps"] if step.get("id") == "selection")
    assert '--base "$BASE" --head "$HEAD"' in select_step["run"]
    assert select_step["env"]["BASE"] == "${{ github.event.pull_request.base.sha }}"
    assert selecting["outputs"] == {
        "selection_mode": "${{ steps.selection.outputs.selection_mode }}",
        "run_product": "${{ steps.selection.outputs.run_product }}",
    }
    assert jobs["app-v4"]["needs"] == "change-selection"
    assert jobs["app-v4"]["if"] == "needs.change-selection.outputs.run_product == 'true'"
    assert jobs["app-v4"]["uses"] == "./.github/workflows/app-v4.yml"
    assert set(jobs) == {"change-selection", "repository-checks", "app-v4", "harness"}
    gate = jobs["harness"]
    assert gate["if"] == "always()"
    assert set(gate["needs"]) == {"change-selection", "repository-checks", "app-v4"}
    assert gate["steps"][-1]["env"]["RESULTS"] == "${{ toJSON(needs) }}"
    assert gate["steps"][-1]["run"] == "python3 tools/ci/select_checks.py gate"


def test_repository_checks_test_the_merge_and_selection_stays_on_the_head():
    # A command main adds names a file a branch cut before it lacks: repository
    # checks therefore run on the event's merge commit, never on the head.
    root = Path(subject.__file__).resolve().parents[2]
    jobs = yaml.safe_load((root / ".github/workflows/governance-harness.yml").read_text())["jobs"]
    head = "${{ github.event.pull_request.head.sha || github.sha }}"

    def checkout(job):
        steps = jobs[job]["steps"]
        assert steps[0]["uses"] == "actions/checkout@v4", job
        assert [step for step in steps if "actions/checkout" in step.get("uses", "")] == steps[:1], job
        return steps[0]["with"]

    assert checkout("repository-checks") == {"ref": "${{ github.sha }}", "fetch-depth": 0}
    assert checkout("change-selection") == {"ref": head, "fetch-depth": 0}
    assert checkout("harness") == {"ref": head}
    steps = jobs["repository-checks"]["steps"]
    named = steps[1]
    assert named["name"] == "Name the commits under test"
    assert "git rev-parse HEAD^2" in named["run"] and "git rev-parse HEAD^1" in named["run"]
    assert named["env"]["PR_HEAD"] == "${{ github.event.pull_request.head.sha }}"
    # The conflict and credential checks examine the pull request's own change.
    conflict = next(step for step in steps if step.get("name") == "Conflict and credential checks")
    assert conflict["env"]["HEAD_SHA"] == head
    for script in ("validate_conflict_markers.py", "validate_run_record_leaks.py"):
        assert f'python tools/validation/{script} --base "$BASE" --head "$HEAD_SHA"' in conflict["run"]
    assert "--head HEAD" not in conflict["run"]


def test_product_workflow_gates_every_job_and_assigns_each_lib_cohort_once():
    root = Path(subject.__file__).resolve().parents[2]
    jobs = yaml.safe_load((root / ".github/workflows/app-v4.yml").read_text())["jobs"]
    gate = jobs.pop("result")
    assert gate["if"] == "always()" and set(gate["needs"]) == set(jobs)
    focused = {"rust-integration", "rust-lib-node", "sources-packaging"}
    assert set(jobs) == focused | {"product"}
    assert jobs["product"]["if"] == "github.event_name == 'workflow_dispatch' || inputs.full_suite"
    assert all(jobs[name]["if"] == "github.event_name != 'workflow_dispatch' && !inputs.full_suite"
               for name in focused)
    shards = [jobs[name]["env"]["LIB_COHORTS"].split() for name in ("rust-integration", "rust-lib-node")]
    cohorts = [cohort for shard in shards for cohort in shard]
    assert all(shards) and len(cohorts) == len(set(cohorts))
    for name in ("rust-integration", "rust-lib-node"):
        run = next(step["run"] for step in jobs[name]["steps"] if "$LIB_COHORTS" in step.get("run", ""))
        assert run.startswith("set -f\nfor cohort in $LIB_COHORTS; do\n")
        assert '--lib "$cohort" -- --test-threads=1\ndone' in run


@pytest.mark.parametrize("full_route, focused, full, passes", [
    ("false", "success success success", "skipped", True),
    ("false", "success failure success", "skipped", False),
    ("false", "success skipped success", "skipped", False),
    ("false", "success success cancelled", "skipped", False),
    ("false", "success success success", "success", False),
    ("false", "", "", False),
    ("true", "skipped skipped skipped", "success", True),
    ("true", "skipped skipped skipped", "failure", False),
    ("true", "success skipped skipped", "success", False),
])
def test_product_result_job_accepts_only_the_event_route(full_route, focused, full, passes):
    root = Path(subject.__file__).resolve().parents[2]
    gate = yaml.safe_load((root / ".github/workflows/app-v4.yml").read_text())["jobs"]["result"]
    env = gate["steps"][-1]["env"]
    assert env["FULL_ROUTE"] == "${{ github.event_name == 'workflow_dispatch' || inputs.full_suite }}"
    assert env["FOCUSED"] == ("${{ needs.rust-integration.result }} ${{ needs.rust-lib-node.result }}"
                              " ${{ needs.sources-packaging.result }}")
    assert env["FULL"] == "${{ needs.product.result }}"
    result = subprocess.run(["bash", "-e", "-c", gate["steps"][-1]["run"]], capture_output=True,
                            env={**os.environ, "FULL_ROUTE": full_route, "FOCUSED": focused, "FULL": full})
    assert (result.returncode == 0) is passes


def test_nightly_workflow_calls_the_full_route_only_after_its_gate():
    root = Path(subject.__file__).resolve().parents[2]
    product = yaml.safe_load((root / ".github/workflows/app-v4.yml").read_text())
    full_suite = product.get("on", product.get(True))["workflow_call"]["inputs"]["full_suite"]
    assert full_suite["type"] == "boolean" and full_suite["default"] is False
    workflow = yaml.safe_load((root / ".github/workflows/nightly-full-suite.yml").read_text())
    trigger = workflow.get("on", workflow.get(True))
    # Runs daily and on demand, not on PRs or merge groups: nothing can require it.
    assert set(trigger) == {"schedule", "workflow_dispatch"}
    assert trigger["schedule"] == [{"cron": "0 9 * * *"}]
    assert workflow["permissions"] == {"contents": "read"}
    assert workflow["concurrency"] == {
        "group": "nightly-full-suite-${{ github.ref }}", "cancel-in-progress": False}
    jobs = workflow["jobs"]
    assert set(jobs) == {"changed", "full-suite", "report"}
    assert {"harness"}.isdisjoint({name for name in jobs} | {job.get("name") for job in jobs.values()})
    assert jobs["changed"]["permissions"] == {"actions": "read", "contents": "read"}
    assert jobs["changed"]["outputs"] == {"run": "${{ steps.decide.outputs.run }}"}
    step = next(step for step in jobs["changed"]["steps"] if step.get("id") == "decide")
    assert "python3 tools/ci/nightly_gate.py" in step["run"]
    assert step["env"]["EVENT"] == "${{ github.event_name }}"
    assert step["env"]["HEAD"] == "${{ github.sha }}"
    assert step["env"]["RUN_ID"] == "${{ github.run_id }}"
    assert jobs["full-suite"] == {
        "needs": "changed", "if": "needs.changed.outputs.run == 'true'",
        "uses": "./.github/workflows/app-v4.yml", "with": {"full_suite": True}}
    assert nightly_gate.WORKFLOW == "nightly-full-suite.yml"
    assert product["jobs"]["product"]["name"] == nightly_gate.PRODUCT_JOB


def test_full_route_has_time_to_finish_the_full_rust_suite():
    root = Path(subject.__file__).resolve().parents[2]
    jobs = yaml.safe_load((root / ".github/workflows/app-v4.yml").read_text())["jobs"]
    focused = [jobs[name]["timeout-minutes"] for name in ("rust-integration", "rust-lib-node", "sources-packaging")]
    assert jobs["product"]["timeout-minutes"] >= 120
    assert jobs["product"]["timeout-minutes"] > max(focused)


def nightly_jobs():
    root = Path(subject.__file__).resolve().parents[2]
    return yaml.safe_load((root / ".github/workflows/nightly-full-suite.yml").read_text())["jobs"]


def test_only_the_nightly_report_job_can_write_issues():
    jobs = nightly_jobs()
    assert jobs["report"]["permissions"] == {"actions": "read", "contents": "read", "issues": "write"}
    assert all("issues" not in job.get("permissions", {}) for name, job in jobs.items() if name != "report")
    assert jobs["report"]["needs"] == ["changed", "full-suite"]
    checkout = jobs["report"]["steps"][0]
    assert checkout["with"]["fetch-depth"] == 0 and checkout["with"]["persist-credentials"] is False
    step = jobs["report"]["steps"][-1]
    assert step["run"].startswith("python3 -m tools.ci.nightly_report ")
    assert step["env"]["SUITE_RESULT"] == "${{ needs.full-suite.result }}"
    assert step["env"]["GATE_RESULT"] == "${{ needs.changed.result }}"


@pytest.mark.parametrize("ref, gate_output, suite, reports", [
    ("refs/heads/main", "true", "failure", True),
    # A timed-out job surfaces as failure or cancelled; both report.
    ("refs/heads/main", "true", "cancelled", True),
    # A gate that failed or was cancelled leaves no output and the suite skipped.
    ("refs/heads/main", "", "skipped", True),
    ("refs/heads/main", "true", "success", False),
    # The scheduled skip: a verdict already exists for this commit.
    ("refs/heads/main", "false", "skipped", False),
    # A dispatch on another branch is not a run on main.
    ("refs/heads/topic", "true", "failure", False),
])
def test_nightly_report_runs_on_every_outcome_but_success_and_a_scheduled_skip(ref, gate_output, suite, reports):
    condition = nightly_jobs()["report"]["if"]
    assert condition.startswith("always() && ")
    python = condition.replace("always()", "True").replace("&&", " and ")
    for name, value in (("github.ref", ref), ("needs.changed.outputs.run", gate_output),
                        ("needs.full-suite.result", suite)):
        python = python.replace(name, repr(value))
    assert eval(python) is reports


def runs(*items):
    return {"workflow_runs": [
        {"id": run_id, "head_sha": sha, "suite": suite, "event": event[0] if event else "schedule"}
        for run_id, sha, suite, *event in items]}


@pytest.mark.parametrize("event, recorded, expected", [
    ("workflow_dispatch", None, True),
    # A manual run ignores any earlier verdict.
    ("workflow_dispatch", runs((8, "head", "success", "schedule")), True),
    ("schedule", None, True),
    ("schedule", runs(), True),
    ("schedule", runs((8, "head", "success")), False),
    ("schedule", runs((8, "head", "failure")), False),
    ("schedule", runs((8, "old", "success")), True),
    ("schedule", runs((8, "old", "failure")), True),
    # A verdict on this commit from any trigger is enough.
    ("schedule", runs((8, "head", "success", "workflow_dispatch")), False),
    ("schedule", runs((8, "head", "failure", "workflow_dispatch")), False),
    ("schedule", runs((8, "old", "success", "workflow_dispatch")), True),
    # No concluded product job is no verdict: gate or runner failure, or a skipped suite.
    ("schedule", runs((8, "head", None, "workflow_dispatch")), True),
    ("schedule", runs((8, "head", "cancelled", "workflow_dispatch"), (7, "old", "success")), True),
    ("schedule", runs((8, "head", "skipped"), (7, "head", "success", "workflow_dispatch")), False),
    # Any verdict on this commit counts, not only the newest one.
    ("schedule", runs((8, "old", "success"), (7, "head", "success")), False),
    # The current run is never its own predecessor.
    ("schedule", runs((9, "head", "success")), True),
])
def test_nightly_gate_skips_only_a_scheduled_run_on_a_commit_with_a_verdict(event, recorded, expected):
    run, reason = nightly_gate.decide(event, "head", 9, recorded)
    assert run is expected and reason


def test_nightly_gate_writes_outputs_and_never_reads_runs_on_dispatch(tmp_path):
    recorded = tmp_path / "runs.json"
    recorded.write_text(json.dumps(runs((8, "head", "success"))))
    output, summary = tmp_path / "output", tmp_path / "summary"
    common = ["--head", "head", "--run-id", "9", "--repository", "owner/repo",
              "--github-output", str(output), "--summary", str(summary)]
    assert nightly_gate.main(["--event", "schedule", "--runs-json", str(recorded), *common]) == 0
    assert output.read_text() == "run=false\n"
    # Dispatch ignores the recorded runs and never calls gh.
    assert nightly_gate.main(["--event", "workflow_dispatch", "--runs-json", "/nonexistent", *common]) == 0
    assert output.read_text() == "run=false\nrun=true\n"
    assert summary.read_text().count("## Nightly full suite") == 2


@pytest.mark.parametrize("path", [
    "execution/PKG-10/DEL-10-01/ScopeOfWork.md",
    "execution/PKG-09/DEL-09-02/Work/README.md",
    "execution/PKG-09/DEL-09-01/Work/example.schema.json",
    "execution/_Coordination/nested/README.md",
])
def test_guarded_execution_namespace_is_documentary(repo, path):
    base = git(repo, "rev-parse", "HEAD")
    write(repo, path)
    result = selection(repo, base)
    assert not result["run_product"]
    assert result["changes"][0]["rule"] == "documentary"


def test_sweep_pr_paths_replay_without_product_code_changes():
    fixture = Path(__file__).with_name("fixtures") / "sweep-pr-paths.json"
    for pr in json.loads(fixture.read_bytes()):
        results = [subject.classify(change) for change in pr["changes"]]
        assert any(row["checks"] == "product" for row in results) == pr["selects_product"], pr["number"]


@pytest.mark.parametrize("returncode, stdout", [(1, ""), (0, "not json")])
def test_nightly_gate_runs_the_suite_when_earlier_runs_cannot_be_read(monkeypatch, returncode, stdout):
    calls = []

    def fake_run(command, **kwargs):
        calls.append(command)
        return subprocess.CompletedProcess(command, returncode, stdout, "refused")

    monkeypatch.setattr(nightly_gate.subprocess, "run", fake_run)
    assert nightly_gate.fetch("owner/repo", "head") is None
    assert calls == [["gh", "api", "repos/owner/repo/actions/workflows/nightly-full-suite.yml/runs"
                      "?branch=main&head_sha=head&status=completed&per_page=100"]]
    assert nightly_gate.decide("schedule", "head", 9, None)[0] is True


def product_jobs(name, status, conclusion):
    return {"jobs": [{"name": "Gate", "status": "completed", "conclusion": "success"},
                     {"name": name, "status": status, "conclusion": conclusion}]}


@pytest.mark.parametrize("jobs, expected", [
    (product_jobs("full-suite / App v4 product", "completed", "success"), "success"),
    (product_jobs("full-suite / App v4 product", "completed", "failure"), "failure"),
    (product_jobs("full-suite / App v4 product", "completed", "cancelled"), "cancelled"),
    (product_jobs("App v4 product", "completed", "success"), "success"),
    # Another job's failure, or a product job that has not finished, is no conclusion.
    (product_jobs("full-suite / App v4 checks", "completed", "failure"), None),
    (product_jobs("full-suite / App v4 product", "in_progress", None), None),
    ({"jobs": []}, None),
])
def test_suite_conclusion_reads_only_the_product_job(jobs, expected):
    assert nightly_gate.suite_conclusion(jobs) == expected


def test_nightly_gate_takes_the_verdict_from_each_runs_product_job(monkeypatch):
    def fake(path):
        if path.endswith("/runs/8/jobs?per_page=100"):
            return {"jobs": [{"name": "changed", "status": "completed", "conclusion": "failure"}]}
        if path.endswith("/runs/7/jobs?per_page=100"):
            return product_jobs("full-suite / App v4 product", "completed", "failure")
        return {"workflow_runs": [{"id": 8, "head_sha": "head", "conclusion": "failure"},
                                  {"id": 7, "head_sha": "head", "conclusion": "failure"}]}

    monkeypatch.setattr(nightly_gate, "gh_api", fake)
    recorded = nightly_gate.fetch("owner/repo", "head")
    assert [item["suite"] for item in recorded["workflow_runs"]] == [None, "failure"]
    assert nightly_gate.verdict_on("head", recorded, 9)["id"] == 7


def test_nightly_gate_runs_the_suite_when_a_runs_jobs_cannot_be_read(monkeypatch):
    monkeypatch.setattr(nightly_gate, "gh_api", lambda path: None if path.endswith("per_page=100") and "/jobs" in path
                        else {"workflow_runs": [{"id": 8, "head_sha": "head"}]})
    assert nightly_gate.fetch("owner/repo", "head") is None


# Consumed-input narrowing (docs/CI_SELECTION.md, "Inputs the macOS jobs do not
# consume"). Exact path sets of the three heads queued on 13 November 2026.
PR228_GOVERNING_TEXT = [
    "docs/EXAMINATION.md", "docs/RELEASE_TARGET_4.0.0.md",
    "execution/PKG-01/DEL-01-02/ScopeOfWork.md", "execution/PKG-01/DEL-01-04/ScopeOfWork.md",
    "execution/PKG-01/DEL-01-04/deliverable.yaml", "execution/PKG-02/DEL-02-02/ScopeOfWork.md",
    "execution/PKG-02/DEL-02-03/ScopeOfWork.md", "execution/PKG-09/DEL-09-01/ScopeOfWork.md",
    "execution/PKG-09/DEL-09-02/ScopeOfWork.md", "execution/PKG-09/DEL-09-02/deliverable.yaml",
    "execution/PKG-09/DEL-09-05/ScopeOfWork.md", "execution/PKG-09/DEL-09-05/deliverable.yaml",
]
PR267_PATHS = [
    "app/examination/candidate_identity/build_candidate.py", "app/examination/standalone/launch.py",
    "app/tests/candidate_identity_test.py", "app/tests/group_b_launch_home_test.py",
]
PR270_EXAMINATION = [
    "app/examination/standalone/operated/README.md", "app/examination/standalone/operated/detached.py",
    "app/examination/standalone/operated/first-use-setup.scenario.json",
    "app/examination/standalone/operated/replay.mjs", "app/examination/standalone/operated/stray.py",
    "app/examination/standalone/operated/walk.mjs", "app/examination/standalone/operated/watch.py",
    "app/tests/group_b_operated_fixtures/first-use-setup/views.json",
    "app/tests/group_b_operated_fixtures/first-use-setup/wrong.a-line-of-what-setup-will-do-missing.json",
    "app/tests/group_b_operated_fixtures/first-use-setup/wrong.a-sixth-line-in-what-setup-will-do.json",
    "app/tests/group_b_operated_fixtures/first-use-setup/wrong.another-control-begins-with-the-same-words.json",
    "app/tests/group_b_operated_fixtures/first-use-setup/wrong.location-outside-the-home.json",
    "app/tests/group_b_operated_fixtures/first-use-setup/wrong.review-available-before-any-choice.json",
    "app/tests/group_b_operated_fixtures/first-use-setup/wrong.review-available-with-existing-settings.json",
    "app/tests/group_b_operated_scenario_test.py", "execution/PKG-09/DEL-09-02/deliverable.yaml",
]
# Inside the class B roots but read by a step of a macOS product job.
MACOS_CONSUMED_IN_CLASS_ROOTS = [
    "app/examination/standalone/fixtures/revision-1/invented-pipe-inventory/WORKFLOW.md",
    "app/examination/standalone/fixtures/revision-1/invented-pipe-inventory/tally.py",
    "app/examination/standalone/fixtures/inputs/initial.csv",
    "app/tests/group_b_fixture_consumer.rs",
    "app/tests/group_b_fixtures/pkg.identity-record.valid.examples.json",
    "app/tests/group_b_sq_receiving_fixtures/development/selection.sha256",
    "app/tests/group_b_sq_receiving_fixtures/development/case.json",
]


def modified(repo, paths):
    for path in paths:
        write(repo, path)
    base = commit(repo)
    for path in paths:
        write(repo, path, "revised\n")
    return selection(repo, base)


def test_governing_text_alone_pr228_selects_no_product_job(repo):
    result = modified(repo, PR228_GOVERNING_TEXT)
    assert result["mode"] == "prose" and result["run_product"] is False
    assert {item["path"] for item in result["changes"]} == set(PR228_GOVERNING_TEXT)
    docs = [item for item in result["changes"] if item["path"].startswith("docs/")]
    assert docs and all(item["rule"] == "governing-text" for item in docs)


@pytest.mark.parametrize("path", [
    "docs/PRD.md", "docs/new-guide.md", "docs/user-manual/workflows/new.md",
])
def test_new_governing_text_document_alone_selects_no_product_job(repo, path):
    base = git(repo, "rev-parse", "HEAD")
    write(repo, path)
    result = selection(repo, base)
    assert result["run_product"] is False
    assert result["changes"][0]["rule"] == "governing-text"


def test_examination_tooling_alone_pr270_selects_no_product_job(repo):
    base = git(repo, "rev-parse", "HEAD")
    write(repo, "execution/PKG-09/DEL-09-02/deliverable.yaml")
    base = commit(repo)
    for path in PR270_EXAMINATION:
        write(repo, path, "revised\n")
    result = selection(repo, base)
    assert result["mode"] == "prose" and result["run_product"] is False
    assert {item["path"] for item in result["changes"]} == set(PR270_EXAMINATION)
    tooling = [item for item in result["changes"] if item["path"].startswith("app/")]
    assert len(tooling) == 15 and all(item["rule"] == "examination" for item in tooling)


def test_examination_launcher_and_its_test_alone_select_no_product_job(repo):
    result = modified(repo, ["app/examination/standalone/launch.py", "app/tests/group_b_launch_home_test.py"])
    assert result["run_product"] is False
    assert {item["rule"] for item in result["changes"]} == {"examination"}


def test_pr267_keeps_product_because_candidate_identity_is_a_macos_input(repo):
    result = modified(repo, PR267_PATHS)
    assert result["mode"] == "product" and result["run_product"] is True
    rules = {item["path"]: (item["rule"], item["checks"]) for item in result["changes"]}
    assert rules["app/tests/candidate_identity_test.py"] == ("product-domain", "product")
    assert rules["app/examination/candidate_identity/build_candidate.py"] == ("product-domain", "product")
    assert rules["app/examination/standalone/launch.py"] == ("examination", "repository")


@pytest.mark.parametrize("path", MACOS_CONSUMED_IN_CLASS_ROOTS)
def test_class_root_paths_a_macos_job_reads_keep_product(repo, path):
    result = modified(repo, [path])
    assert result["run_product"] is True
    assert result["changes"][0]["rule"] == "product-domain"


@pytest.mark.parametrize("product", [
    "app/src/App.tsx", "app/src-tauri/src/lib.rs", "app/src-tauri/Cargo.lock", "app/package-lock.json",
    "app/src-tauri/schemas/RS_RECORD.schema.json", "app/src-tauri/resources/instructions/AGENTS.md",
    "app/tests/candidate_identity_test.py", "app/tests/fixtures/FX-DP1/MANIFEST.sha256",
    "app/examination/repin.py", "app/examination/pins.lock.json",
    "app/examination/native_forms/pre_run_form.py", "app/tests/examination_repin_test.py",
    *MACOS_CONSUMED_IN_CLASS_ROOTS,
])
def test_mixed_class_change_with_any_product_input_keeps_full_product(repo, product):
    base = git(repo, "rev-parse", "HEAD")
    for path in ["docs/PRD.md", "app/examination/standalone/launch.py",
                 "app/tests/group_b_launch_home_test.py", "execution/PKG-09/DEL-09-02/ScopeOfWork.md", product]:
        write(repo, path)
    result = selection(repo, base)
    assert result["mode"] == "product" and result["run_product"] is True
    assert next(item for item in result["changes"] if item["path"] == product)["checks"] == "product"


@pytest.mark.parametrize("path", [
    # Other file types inside the class roots.
    "docs/document-metadata.schema.json", "docs/check.py", "docs/PRD.md.py", "docs/notes.txt",
    "app/examination/standalone/run.sh", "app/examination/standalone/data.csv",
    "app/tests/group_b_new.rs", "app/tests/group_b_operated_fixtures/case.txt",
    "app/tests/group_b_operated_fixtures/MANIFEST.sha256",
    # Lookalikes of the class roots.
    "app/docs/PRD.md", "app/examination/standalone.py",
    "app/examination/standalone-other/launch.py", "app/examination/native_forms/native_form.py",
    "app/examination/STANDALONE/launch.py", "app/tests/group_bx_test.py", "app/tests/group_b",
    "app/tests/nested/group_b_new_test.py", "app/tests/group-b_new_test.py",
    "app/src-tauri/tests/group_b_new_test.py", "tools/group_b_new_test.py",
    # Unknown paths.
    "new-domain/README.md", "unknown.md",
])
def test_lookalikes_other_types_and_unknowns_beside_a_class_keep_product(repo, path):
    base = git(repo, "rev-parse", "HEAD")
    write(repo, "docs/PRD.md")
    write(repo, "app/tests/group_b_launch_home_test.py")
    write(repo, path)
    result = selection(repo, base)
    assert result["run_product"] is True
    assert next(item for item in result["changes"] if item["path"] == path)["checks"] == "product"


@pytest.mark.parametrize("path", [
    # Case variants; a case-insensitive fixture filesystem cannot hold them beside docs/.
    "Docs/PRD.md", "DOCS/PRD.md", "docs/PRD.MD", "App/tests/group_b_new_test.py",
    "app/Examination/standalone/launch.py", "app/tests/GROUP_B_new_test.py",
    "app/examination/standalone/launch.PY",
])
def test_case_variants_of_a_class_are_product(path):
    change = {"path": path, "status": "A", "old_mode": "000000", "new_mode": "100644"}
    assert subject.classify(change)["checks"] == "product"


@pytest.mark.parametrize("kind", ["delete", "executable", "symlink"])
@pytest.mark.parametrize("relative", [
    "docs/PRD.md", "app/examination/standalone/launch.py", "app/tests/group_b_launch_home_test.py",
    "app/tests/group_b_operated_fixtures/first-use-setup/views.json",
])
def test_deletion_and_type_or_mode_changes_in_a_class_keep_product(repo, kind, relative):
    path = write(repo, relative)
    base = commit(repo)
    if kind == "delete":
        path.unlink()
    elif kind == "executable":
        path.chmod(0o755)
    else:
        path.unlink()
        path.symlink_to(Path(os.path.relpath(repo / ".fixture", path.parent)))
    assert selection(repo, base)["run_product"]


@pytest.mark.parametrize("old, new", [
    ("app/examination/standalone/launch.py", "app/src-tauri/launch.py"),
    ("app/src-tauri/resources/instructions/new.md", "docs/new.md"),
    ("app/tests/candidate_identity_test.py", "app/tests/group_b_candidate_test.py"),
    ("docs/PRD.md", "app/examination/standalone/PRD.md"),
    ("app/tests/group_b_fixtures/x.json", "app/tests/group_b_operated_fixtures/x.json"),
])
def test_renames_into_out_of_or_between_classes_keep_product(repo, old, new):
    write(repo, old)
    base = commit(repo)
    target = repo / new
    target.parent.mkdir(parents=True, exist_ok=True)
    (repo / old).rename(target)
    result = selection(repo, base)
    assert result["run_product"] is True
    assert {item["status"] for item in result["changes"]} == {"D", "A"}


@pytest.mark.parametrize("path", [
    "tools/ci/select_checks.py", "tools/ci/test_selection.py",
    ".github/workflows/governance-harness.yml", ".github/workflows/app-v4.yml",
    ".github/workflows/nightly-full-suite.yml", ".github/actions/app-v4-setup/action.yml",
])
def test_selector_rules_and_workflows_beside_a_class_keep_product(repo, path):
    base = git(repo, "rev-parse", "HEAD")
    for item in ["docs/PRD.md", "app/examination/standalone/launch.py", path]:
        write(repo, item)
    assert selection(repo, base)["run_product"] is True


def test_selection_document_keeps_its_existing_repository_route(repo):
    # docs/CI_SELECTION.md was already an audited documentary path; it keeps that route.
    result = modified(repo, ["docs/CI_SELECTION.md"])
    assert result["run_product"] is False and result["changes"][0]["rule"] == "documentary"


def test_repository_checks_run_every_consumer_of_the_narrowed_classes():
    # A narrowed class is safe only while the always-run job still runs what reads it.
    root = Path(subject.__file__).resolve().parents[2]
    jobs = yaml.safe_load((root / ".github/workflows/governance-harness.yml").read_text())["jobs"]
    steps = "\n".join(step.get("run", "") for step in jobs["repository-checks"]["steps"])
    job = jobs["repository-checks"]
    # A listed command must run unconditionally and its failure must fail the job.
    assert not {"if", "continue-on-error"} & set(job)
    assert all(not {"if", "continue-on-error"} & set(step) for step in job["steps"])
    assert all("|| true" not in step.get("run", "") for step in job["steps"])
    for command in [
        "python -m pytest -q app/tests/group_b*test.py",
        "python -m pytest -q app/tests/examination_repin_test.py",
        "python app/examination/repin.py --check",
        "python -m pytest -q tools/validation/test_document_metadata.py",
        "python -m tools.deliverables --project . check",
        "python tools/ci/check_execution_layout.py",
    ]:
        assert command in steps, command
    product = yaml.safe_load((root / ".github/workflows/app-v4.yml").read_text())["jobs"]
    runs = "\n".join(step.get("run", "") for job in product.values() for step in job.get("steps", []))
    # No macOS step names a class B path; the Group B suites are repository checks only.
    assert "group_b" not in runs and "standalone" not in runs and "docs/" not in runs


# Every file outside a narrowed class that names one of its paths, and why that
# reader is not a macOS product input (docs/CI_SELECTION.md mapping).
CLASS_REFERENCE = re.compile(r"group_b[_*]|standalone/|(?<![\w./-])docs/|\.\./docs/|[\"'](docs|standalone)[\"']")
KNOWN_REFERRERS = {
    ".github/workflows/governance-harness.yml": "repository-checks runs the Group B suites",
    "tools/ci/select_checks.py": "the selector's own rules",
    "tools/ci/test_selection.py": "the selector's own tests",
    "tools/validation/test_document_metadata.py": "repository check reading docs/*.md headers",
    "tools/library_workflows/test_bundle.py": "invented docs/ paths of a synthetic Library release",
    "app/tests/check_git_checkout_bytes.py": "invented docs/ control path in a temporary repository",
    "app/examination/repin.py": "pin check; runs in repository checks and examination_repin_test",
    "app/examination/pins.lock.json": "pin lock read by repin.py",
    "app/examination/native_forms/pre_run_form.py": "run only by group_b_native_forms_test",
    "app/examination/native_forms/pre_run_form.terms-v1.pins.json": "read by pre_run_form.py",
    "app/examination/native_forms/sources.terms-v1.json": "read by native_form.py",
    "app/examination/scripted_driver/proof.py": "reads the first-use scenario for the scripted driver's hosted job",
    ".github/workflows/app-scripted-driver.yml": "its path trigger names the first-use scenario its driver reads",
    "app/examination/sq_receiving/sq.step-map.json": "out_of_release names the release target as where it is stated; nothing reads that path from it",
    # Readers of in-root paths that stay product inputs.
    "tools/validation/test_library_v3_operational_adoption.py": "names the Library's own docs/ files",
    "app/src-tauri/src/lib.rs": "compiles group_b_fixture_consumer.rs (product input)",
    "app/tests/group_b_fixture_consumer.rs": "product input; reads standalone/fixtures/ (product input)",
    "app/packaging/static_distribution/test_s1_value_model.py": "reads group_b_fixtures/ (product input)",
    "app/tests/package_successor_receiving_fixtures.py": "reads group_b_sq_receiving_fixtures/ (product input)",
    # Ignored export generators: they write fixtures under an explicit root and read none.
    "app/src-tauri/src/hosting_s4_export.rs": "export_group_b_* generator name",
    "app/src-tauri/src/hosting_terminal_export.rs": "export_group_b_* generator name",
}
# Retained Library manifests name the Library repository's own docs/ files.
LIBRARY_MANIFEST = re.compile(r"reference/library-v[0-9.]+/MANIFEST\.json")
CODE_SUFFIXES = (".py", ".rs", ".mjs", ".cjs", ".js", ".ts", ".tsx", ".json", ".toml", ".sh", ".yml")


def test_no_unreviewed_reader_of_a_narrowed_class():
    root = Path(subject.__file__).resolve().parents[2]
    found = set()
    for path in git(root, "ls-files").splitlines():
        if (path.startswith(("docs/", "execution/", "app/src-tauri/resources/supplier/"))
                or subject.path_rule(path) == "examination" or not path.endswith(CODE_SUFFIXES)):
            continue
        if LIBRARY_MANIFEST.fullmatch(path):
            continue
        if CLASS_REFERENCE.search((root / path).read_text(errors="ignore")):
            found.add(path)
    # A new reader must be placed in docs/CI_SELECTION.md's mapping and here, or
    # the path it reads must stay a product input.
    assert found == set(KNOWN_REFERRERS)


@pytest.mark.parametrize("paths", [PR228_GOVERNING_TEXT, PR270_EXAMINATION])
def test_narrowed_selection_reaches_a_harness_that_still_requires_repository_checks(repo, tmp_path, paths):
    base = git(repo, "rev-parse", "HEAD")
    for path in paths:
        write(repo, path)
    head = commit(repo)
    output = tmp_path / "outputs"
    command = ["python3", str(Path(subject.__file__)), "select", "--event", "pull_request",
               "--repo", str(repo), "--base", base, "--head", head, "--github-output", str(output)]
    assert subprocess.run(command, capture_output=True).returncode == 0
    outputs = dict(line.split("=", 1) for line in output.read_text().splitlines())
    assert outputs == {"selection_mode": "prose", "run_product": "false"}

    def gate(repository, product):
        results = {"change-selection": {"result": "success", "outputs": outputs},
                   "repository-checks": {"result": repository}, "app-v4": {"result": product}}
        subject.require_success(results)

    gate("success", "skipped")  # the product jobs correctly not selected
    for repository in ["failure", "cancelled", "skipped", None]:
        with pytest.raises(ValueError):
            gate(repository, "skipped")  # the jobs that run every reader must pass
    for product in ["success", "failure", "cancelled", None]:
        with pytest.raises(ValueError):
            gate("success", product)  # an unexpected product run is not accepted either


# B1: a path a checkout may fold onto a protected input is never narrowed.
def plumb(repo, entries):
    """Commit entries {path: (mode, bytes)} through the index, not the file system,
    so names a case- or normalization-insensitive volume would merge stay distinct."""
    git(repo, "config", "core.precomposeunicode", "false")  # Git on macOS would precompose NFD names
    for path, (mode, data) in entries.items():
        oid = subprocess.run(["git", "-C", str(repo), "hash-object", "-w", "--stdin"], input=data,
                             capture_output=True, check=True).stdout.decode().strip()
        git(repo, "update-index", "--add", "--cacheinfo", f"{mode},{oid},{path}")
    git(repo, "commit", "-qm", "plumbed")
    return git(repo, "rev-parse", "HEAD")


PROTECTED_FILE = "app/tests/group_b_fixtures/pkg.identity-record.valid.examples.json"
LONG_S_ALIAS = "app/tests/group_b_fixtureſ/pkg.identity-record.valid.examples.json"
CASE_ALIAS = "app/tests/group_b_Fixtures/pkg.identity-record.valid.examples.json"


@pytest.mark.parametrize("alias", [LONG_S_ALIAS, CASE_ALIAS])
def test_reviewer_alias_of_a_protected_input_selects_product_and_is_refused(repo, alias):
    base = plumb(repo, {PROTECTED_FILE: ("100644", b"{}\n")})
    head = plumb(repo, {alias: ("100644", b"{\"changed\": true}\n")})
    result = subject.select(repo, "pull_request", base, head)
    assert result["mode"] == "product" and result["run_product"] is True
    assert [change["checks"] for change in result["changes"]] == ["product"]
    found = subject.inventory(repo)
    directory = "app/tests/" + alias.split("/")[2]
    assert sorted([directory, "app/tests/group_b_fixtures"]) in found["collisions"]
    command = ["python3", str(Path(subject.__file__)), "inventory", "--repo", str(repo)]
    refused = subprocess.run(command, capture_output=True, text=True)
    assert refused.returncode == 2 and "collide" in refused.stderr


@pytest.mark.parametrize("path", [
    "docs/PRÉ.md", "docs/PRÉ.md", "execution/PKG-01/DEL-01-01/ScopeſOfWork.md",
    "AGENTS​.md", "app/examination/standalone/launcħ.py", "app/tests/group_b_а_test.py",
    "app/tests/group_b_operated_fixtures/viｅws.json",
])
def test_non_ascii_spelling_of_any_narrowing_rule_keeps_product(repo, path):
    head = plumb(repo, {path: ("100644", b"text\n")})
    result = subject.select(repo, "pull_request", git(repo, "rev-parse", "HEAD~1"), head)
    assert result["run_product"] is True
    assert result["changes"][0]["reason"] == "Only printable ASCII paths can skip product verification"


@pytest.mark.parametrize("path", [
    "app/tests/GROUP_B_FIXTURES/x.json", "app/tests/group_b_FIXTURES/x.json",
    "app/tests/group_b_Fixture_Consumer.rs.json", "app/examination/standalone/Fixtures/tally.py",
    "app/tests/group_b_SQ_receiving_fixtures/case.json",
])
def test_case_variants_of_protected_prefixes_keep_product(path):
    assert subject.path_rule(path) != "examination"


def test_collision_check_reads_the_tree_and_folds_case_normalization_and_format_characters(repo):
    plumb(repo, {"docs/A.md": ("100644", b"a\n"), "docs/a.md": ("100644", b"b\n"),
                 "docs/é.md": ("100644", b"c\n"), "docs/é.md": ("100644", b"d\n"),
                 "docs/z‍.md": ("100644", b"e\n"), "docs/z.md": ("100644", b"f\n")})
    assert subject.inventory(repo)["collisions"] == [
        ["docs/A.md", "docs/a.md"], ["docs/é.md", "docs/é.md"], ["docs/z.md", "docs/z‍.md"]]


# R2-B2 and links as a class. The inventory inspects committed modes 120000 and
# 160000, resolves no target, and rejects either anywhere in the tracked tree.
@pytest.mark.parametrize("link, mode, target", [
    # The reviewer's construction: a product test's directory linked to a class root.
    ("app/tests/r2-assets", "120000", "../examination/standalone"),
    ("app/tests/r2-assets", "120000", "../examination/standalone/"),
    ("app/tests/ancestor", "120000", "../examination"),
    ("app/src/notes.md", "120000", "../../docs/PRD.md"),
    ("app/src/unrelated.json", "120000", "../src-tauri/resources/x.json"),
    ("app/src/dangling.json", "120000", "../nowhere/absent.json"),
    ("app/tests/group_b_link_test.py", "160000", "0" * 39 + "1"),
])
def test_inventory_refuses_any_symbolic_link_or_gitlink(repo, link, mode, target):
    if mode == "160000":
        git(repo, "update-index", "--add", "--cacheinfo", f"{mode},{target},{link}")
        git(repo, "commit", "-qm", "gitlink")
    else:
        plumb(repo, {link: (mode, target.encode())})
    kind = "symbolic link" if mode == "120000" else "gitlink"
    assert subject.inventory(repo)["links"] == [f"{link} ({kind})"]
    command = ["python3", str(Path(subject.__file__)), "inventory", "--repo", str(repo)]
    refused = subprocess.run(command, capture_output=True, text=True)
    assert refused.returncode == 2 and "symbolic link or gitlink" in refused.stderr


def test_reviewer_link_consumer_commit_is_refused(repo):
    # R2-B2 as the reviewer built it: a product test reads through a directory link
    # to the standalone root. The commit adding the link is refused by the inventory.
    plumb(repo, {"app/examination/standalone/r2-input.json": ("100644", b"true\n"),
                 "app/tests/font_notice_test.py": ("100644", b"# reads r2-assets/r2-input.json\n")})
    plumb(repo, {"app/tests/r2-assets": ("120000", b"../examination/standalone")})
    assert subject.inventory(repo)["links"] == ["app/tests/r2-assets (symbolic link)"]
