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


def selection(repo, base, event="pull_request"):
    return subject.select(repo, event, base, commit(repo))


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
    assert subject.inventory(repo) == {"tracked_paths": 2, "unmatched": []}
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
    "app/src/new.rs", "docs/PRD.md", "tools/ci/select_checks.py",
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


@pytest.mark.parametrize("event", ["pull_request", "merge_group"])
def test_merge_queue_candidate_selects_like_a_pull_request(repo, event):
    base = git(repo, "rev-parse", "HEAD")
    write(repo, "AGENTS.md", "revised instructions\n")
    prose = selection(repo, base, event)
    assert (prose["mode"], prose["merge_base"]) == ("prose", base)
    write(repo, "app/src/new.rs")
    product = selection(repo, base, event)
    assert product["run_product"] and {c["path"] for c in product["changes"]} == {"AGENTS.md", "app/src/new.rs"}


def test_empty_change_and_manual_dispatch_keep_product(repo):
    head = git(repo, "rev-parse", "HEAD")
    assert subject.select(repo, "pull_request", head, head)["run_product"]
    assert subject.select(repo, "merge_group", head, head)["run_product"]
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
    for event in ("push", "merge_queue", "pull_request_target"):
        with pytest.raises(ValueError):
            subject.select(repo, event, "", head)


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
    assert trigger["merge_group"] == {"types": ["checks_requested"]}
    assert set(trigger) == {"pull_request", "merge_group", "workflow_dispatch"}
    # Superseded PR runs may cancel; a queue candidate's own group never does.
    assert_concurrency(workflow["concurrency"], "governance-harness-")
    jobs = workflow["jobs"]
    assert "if" not in jobs["repository-checks"]
    repo = jobs["repository-checks"]
    assert any("python tools/ci/select_checks.py inventory" in step.get("run", "")
               for step in repo["steps"])
    select_step = next(step for step in repo["steps"] if step.get("id") == "selection")
    assert '--base "$BASE" --head "$HEAD"' in select_step["run"]
    assert select_step["env"] == {
        "EVENT": "${{ github.event_name }}",
        "BASE": "${{ github.event.pull_request.base.sha || github.event.merge_group.base_sha }}",
        "HEAD": "${{ github.event.pull_request.head.sha || github.event.merge_group.head_sha || github.sha }}",
    }
    checkouts = [step["with"]["ref"] for job in jobs.values() for step in job.get("steps", [])
                 if step.get("uses", "").startswith("actions/checkout@")]
    assert checkouts and set(checkouts) == {HEAD_REF}
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


HEAD_REF = "${{ github.event.pull_request.head.sha || github.event.merge_group.head_sha || github.sha }}"
QUEUE_BRANCH = "refs/heads/gh-readonly-queue/main/pr-7-" + "a" * 40
# Contexts per event; a manual dispatch may target the temporary queue branch.
CONTEXTS = {
    "pull_request": {"github.event_name": "pull_request", "github.event.pull_request.number": "7",
                     "github.ref": "refs/pull/7/merge", "github.run_id": "101"},
    "merge_group": {"github.event_name": "merge_group", "github.ref": QUEUE_BRANCH, "github.run_id": "102"},
    "merge_group_rerun": {"github.event_name": "merge_group", "github.ref": QUEUE_BRANCH, "github.run_id": "103"},
    "workflow_dispatch": {"github.event_name": "workflow_dispatch", "github.ref": QUEUE_BRANCH,
                          "github.run_id": "104"},
}


def evaluate(expression, context):
    """Evaluate the concurrency expression's `a || b && c || ...` forms with GitHub's truthiness."""
    def term(text):
        text = text.strip()
        if text.startswith("format('queue-{0}', ") and text.endswith(")"):
            return "queue-" + context[text[len("format('queue-{0}', "):-1]]
        if " == " in text:
            left, right = text.split(" == ")
            return context.get(left.strip()) == right.strip().strip("'")
        return context.get(text, "")
    for alternative in expression.split("||"):
        value = None
        for part in alternative.split("&&"):
            value = term(part)
            if not value:
                break
        if value:
            return value
    return ""


def assert_concurrency(block, prefix):
    assert set(block) == {"group", "cancel-in-progress"}
    group = block["group"]
    assert group.startswith(prefix + "${{ ") and group.endswith(" }}")
    expression = group[len(prefix) + 4:-3]
    keys = {event: evaluate(expression, context) for event, context in CONTEXTS.items()}
    assert keys["pull_request"] == "7"
    assert keys["workflow_dispatch"] == QUEUE_BRANCH
    # Every queue run has its own group, distinct from a dispatch on its branch.
    assert keys["merge_group"] == "queue-102" and len(set(keys.values())) == len(keys)
    assert block["cancel-in-progress"] == "${{ github.event_name == 'pull_request' }}"


def test_product_workflow_inherits_the_callers_event_and_never_cancels_queue_runs():
    root = Path(subject.__file__).resolve().parents[2]
    workflow = yaml.safe_load((root / ".github/workflows/app-v4.yml").read_text())
    # Called by the harness for pull_request and merge_group; a trigger of its own
    # would start a second, unselected run in the same concurrency group.
    assert set(workflow.get("on", workflow.get(True))) == {"workflow_call", "workflow_dispatch"}
    assert_concurrency(workflow["concurrency"], "app-v4-")
    checkouts = [step["with"]["ref"] for job in workflow["jobs"].values() for step in job.get("steps", [])
                 if step.get("uses", "").startswith("actions/checkout@")]
    assert len(checkouts) == 4 and set(checkouts) == {HEAD_REF}


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
        assert run.startswith("set -f\nfor cohort in $LIB_COHORTS; do\n")
        assert '--lib "$cohort" -- --test-threads=1\ndone' in run


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
