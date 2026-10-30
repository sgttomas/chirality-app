"""Exercise real Git changes and the required-job result contract."""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess

import pytest
import yaml

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


@pytest.mark.parametrize("path", [
    "app/src/App.tsx", "app/src-tauri/src/hosting.rs", "app/package-lock.json",
    ".github/workflows/governance-harness.yml", "tools/ci/select_checks.py",
    "tools/ci/test_selection.py", ".gitattributes", "unknown.md",
    "app/src-tauri/resources/AGENTS.md", "workflows/example/WORKFLOW.md",
    "execution/PKG-09/DEL-09-02/Design/README.md",
    "execution/PKG-04/DEL-04-03/Design/prototype/README.md",
    "execution/PKG-09/DEL-09-01/Design/example.schema.json",
    "execution/_Coordination/nested/README.md", "app/packaging/README.md",
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
def test_deletion_and_type_or_mode_changes_at_allowed_path_keep_product(repo, kind):
    path = write(repo, "README.md")
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
        "repository-checks": {"result": "success", "outputs": {
            "selection_mode": mode, "run_product": product,
        }},
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
    for status in ["failure", "cancelled", "skipped"]:
        value = needs("false", "prose", "skipped")
        value["repository-checks"]["result"] = status
        examples.append(value)
    value = needs()
    del value["repository-checks"]["outputs"]
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
    select_step = next(step for step in repo["steps"] if step.get("id") == "selection")
    assert '--base "$BASE" --head "$HEAD"' in select_step["run"]
    assert select_step["env"]["BASE"] == "${{ github.event.pull_request.base.sha }}"
    assert repo["outputs"] == {
        "selection_mode": "${{ steps.selection.outputs.selection_mode }}",
        "run_product": "${{ steps.selection.outputs.run_product }}",
    }
    assert jobs["app-v4"]["needs"] == "repository-checks"
    assert jobs["app-v4"]["if"] == "needs.repository-checks.outputs.run_product == 'true'"
    assert jobs["app-v4"]["uses"] == "./.github/workflows/app-v4.yml"
    gate = jobs["harness"]
    assert gate["if"] == "always()"
    assert set(gate["needs"]) == {"repository-checks", "app-v4"}
    assert gate["steps"][-1]["env"]["RESULTS"] == "${{ toJSON(needs) }}"
    assert gate["steps"][-1]["run"] == "python3 tools/ci/select_checks.py gate"


def test_product_workflow_gates_every_job_and_assigns_each_lib_cohort_once():
    root = Path(subject.__file__).resolve().parents[2]
    jobs = yaml.safe_load((root / ".github/workflows/app-v4.yml").read_text())["jobs"]
    gate = jobs.pop("result")
    assert gate["if"] == "always()" and set(gate["needs"]) == set(jobs)
    focused = {"rust-integration", "rust-lib-node", "sources-packaging"}
    assert set(jobs) == focused | {"product"}
    assert jobs["product"]["if"] == "github.event_name == 'workflow_dispatch'"
    assert all(jobs[name]["if"] == "github.event_name != 'workflow_dispatch'" for name in focused)
    shards = [jobs[name]["env"]["LIB_COHORTS"].split() for name in ("rust-integration", "rust-lib-node")]
    cohorts = [cohort for shard in shards for cohort in shard]
    assert all(shards) and len(cohorts) == len(set(cohorts))
    for name in ("rust-integration", "rust-lib-node"):
        run = next(step["run"] for step in jobs[name]["steps"] if "$LIB_COHORTS" in step.get("run", ""))
        assert run.startswith("set -f\n") and "--lib -- --test-threads=1 $LIB_COHORTS" in run


@pytest.mark.parametrize("dispatch, focused, full, passes", [
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
def test_product_result_job_accepts_only_the_event_route(dispatch, focused, full, passes):
    root = Path(subject.__file__).resolve().parents[2]
    gate = yaml.safe_load((root / ".github/workflows/app-v4.yml").read_text())["jobs"]["result"]
    env = gate["steps"][-1]["env"]
    assert env["FOCUSED"] == ("${{ needs.rust-integration.result }} ${{ needs.rust-lib-node.result }}"
                              " ${{ needs.sources-packaging.result }}")
    assert env["FULL"] == "${{ needs.product.result }}"
    result = subprocess.run(["bash", "-e", "-c", gate["steps"][-1]["run"]], capture_output=True,
                            env={**os.environ, "DISPATCH": dispatch, "FOCUSED": focused, "FULL": full})
    assert (result.returncode == 0) is passes
