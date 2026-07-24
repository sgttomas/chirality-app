from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import validate_path_anchors as validator


SCRIPT = Path(__file__).with_name("validate_path_anchors.py")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def findings_for(tmp_path: Path) -> list[dict[str, object]]:
    return validator.scan(tmp_path)["findings"]


def test_flags_home_paths_in_agent_instructions(tmp_path: Path) -> None:
    write(tmp_path / "agents/AGENT_TEST.md", "Read `/Users/example/repo/agents/AGENT_TASK.md`.\n")

    findings = findings_for(tmp_path)

    assert len(findings) == 1
    assert findings[0]["path"] == "agents/AGENT_TEST.md"
    assert findings[0]["match"] == "/Users/example/repo/agents/AGENT_TASK.md"


def test_accepts_repo_root_tokens_in_active_prompts(tmp_path: Path) -> None:
    write(
        tmp_path / "projects/example/execution/_Coordination/NEXT_INSTANCE_PROMPT.md",
        "Read `{REPO_ROOT}/agents/AGENT_WORKING_ITEMS.md`.\n",
    )
    write(
        tmp_path / "projects/example/init/init-prompt.md",
        "Set `WORKING_ROOT` to `{REPO_ROOT}/projects/example`.\n",
    )

    assert findings_for(tmp_path) == []


def test_ignores_archives_run_records_plans_and_decisions(tmp_path: Path) -> None:
    ignored_text = "Historical path: `/Users/example/repo/projects/example`.\n"
    write(tmp_path / "plans/path-plan.md", ignored_text)
    write(tmp_path / "projects/example/.archive/execution/_Coordination/NEXT_INSTANCE_PROMPT.md", ignored_text)
    write(tmp_path / "projects/example/execution/_Coordination/_DECISIONS/D-01.md", ignored_text)
    write(tmp_path / "projects/example/execution/PKG/DEL/_run_records/TASK_RUN.md", ignored_text)
    write(tmp_path / "domains/example/_Decomposition/dispatch_briefs/UNIT.md", ignored_text)
    write(tmp_path / "exports/example/export.md", ignored_text)

    assert findings_for(tmp_path) == []


def test_cli_returns_nonzero_for_findings(tmp_path: Path) -> None:
    write(tmp_path / "init/init-prompt.md", "Read `/home/example/repo/agents/AGENT_TASK.md`.\n")

    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(tmp_path), "--text"],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 1
    assert "FAIL:" in result.stdout
    assert "init/init-prompt.md:1" in result.stdout


def test_shared_roles_allow_evidence_and_fail_unknown_agentruns(tmp_path: Path) -> None:
    project = tmp_path / "projects/example"
    write(project / "validation/portability_policy.json", json.dumps({
        "schema_version": 1,
        "project_root": "projects/example",
        "historical_role_overrides": [],
        "control_path_exceptions": [],
    }) + "\n")
    run = project / "execution/_Coordination/AgentRuns/R10"
    write(run / "LAUNCH_BRIEF.md", "Root: {REPO_ROOT}\n")
    write(run / "RETURN.md", "Ran at /Users/example/repo\n")
    write(run / "CAPTURE.json", '{"cwd":"/Users/example/repo"}\n')

    report = validator.scan(tmp_path)

    assert report["finding_count"] == 1
    assert report["findings"][0]["path"].endswith("CAPTURE.json")
    assert report["semantic_invariants"] == {
        "unacknowledged_control": 0,
        "active_unclassified": 1,
        "policy_issues": 0,
        "acknowledged_control": 0,
    }
