from pathlib import Path

import validate_instruction_entrypoints as validator


REPO_ROOT = Path(__file__).resolve().parents[2]


def test_accepts_exact_import(tmp_path: Path) -> None:
    (tmp_path / "AGENTS.md").write_text("# doctrine\n", encoding="utf-8")
    (tmp_path / "CLAUDE.md").write_text("@AGENTS.md\n", encoding="utf-8")
    assert validator.validate(tmp_path) == []


def test_rejects_added_instruction_layer(tmp_path: Path) -> None:
    (tmp_path / "AGENTS.md").write_text("# doctrine\n", encoding="utf-8")
    (tmp_path / "CLAUDE.md").write_text("@AGENTS.md\nextra\n", encoding="utf-8")
    assert validator.validate(tmp_path) == [
        "CLAUDE.md must contain exactly '@AGENTS.md\\n'"
    ]


def _write_project(
    tmp_path: Path,
    *,
    project_name: str = "chirality-app-dev",
    entry_role: str = "HELP_HUMAN",
    project_agents_text: str = (
        "one package-scoped instance\nTerminal fan-out/fan-in\n"
        "supervised many-to-many\nSOFTWARE_WORKFLOW_PROFILE.md\n"
    ),
    loop_text: str = "# Loop\n\n## 7. Per-run steer\n",
    workplan_text: str = "# Standing workplan\n",
) -> Path:
    (tmp_path / "AGENTS.md").write_text("# doctrine\n", encoding="utf-8")
    (tmp_path / "CLAUDE.md").write_text("@AGENTS.md\n", encoding="utf-8")
    project = tmp_path / "projects" / project_name
    (project / "init").mkdir(parents=True)
    (project / "loop").mkdir()
    (project / "AGENTS.md").write_text(project_agents_text, encoding="utf-8")
    prompt = (
        "<init-prompt>\n"
        "Resolve `REPO_ROOT` with `git rev-parse --show-toplevel`.\n\n"
        f"Set `WORKING_ROOT` to `{{REPO_ROOT}}/projects/{project_name}`.\n\n"
        "Read `{REPO_ROOT}/AGENTS.md`.\n"
        f"Read `{{REPO_ROOT}}/agents/AGENT_{entry_role}.md`.\n\n"
        f"Act as `{entry_role}` for `{{WORKING_ROOT}}`.\n\n"
        "Read `{WORKING_ROOT}/loop/LOOP_INIT.md` and follow it.\n"
        "</init-prompt>\n"
    )
    (project / "init" / "init-prompt.md").write_text(prompt, encoding="utf-8")
    (tmp_path / "init").mkdir()
    (tmp_path / "init" / "init-prompt.md").write_text(
        f"# Root launcher catalog\n\n{prompt}", encoding="utf-8"
    )
    (project / "loop" / "LOOP_INIT.md").write_text(loop_text, encoding="utf-8")
    (project / "loop" / "WORKPLAN_2026-07-18_test.md").write_text(
        workplan_text, encoding="utf-8"
    )
    (project / "software-workflow.json").write_text(
        '{"schema":"chirality-software-workflow/v1"}\n', encoding="utf-8"
    )
    return project


def test_accepts_help_human_entry_with_separated_loop(tmp_path: Path) -> None:
    _write_project(tmp_path)
    assert validator.validate(tmp_path) == []


def test_accepts_thin_project_agents_with_canonical_runtime_reference(
    tmp_path: Path,
) -> None:
    _write_project(
        tmp_path,
        project_name="chirality-piping",
        entry_role="WORKING_ITEMS",
        project_agents_text=(
            "Root `AGENTS.md` and canonical `agents/AGENT_*.md` packages govern "
            "runtime roles, selection, delegation, and orchestration.\n"
            "Software work follows `docs/SOFTWARE_WORKFLOW_PROFILE.md`.\n"
        ),
    )
    assert validator.validate(tmp_path) == []


def test_rejects_project_agents_without_software_profile_reference(
    tmp_path: Path,
) -> None:
    project = _write_project(
        tmp_path,
        project_agents_text=(
            "Root `AGENTS.md` and canonical agent packages govern runtime "
            "roles and orchestration.\n"
        ),
    )
    assert validator.validate(tmp_path) == [
        f"{project.relative_to(tmp_path)}/AGENTS.md is missing "
        "'software_workflow_profile.md'"
    ]


def test_rejects_root_project_launcher_drift(tmp_path: Path) -> None:
    project = _write_project(tmp_path)
    (tmp_path / "init" / "init-prompt.md").write_text(
        "# Root launcher catalog\n\n"
        "<init-prompt>\n"
        "Set project path to `projects/chirality-app-dev`.\n"
        "Act as `HELP_HUMAN` for a divergent root launcher.\n"
        "</init-prompt>\n",
        encoding="utf-8",
    )
    assert validator.validate(tmp_path) == [
        f"{project.relative_to(tmp_path)}/init/init-prompt.md does not byte-match the "
        "tagged root launcher for projects/chirality-app-dev"
    ]


def test_stale_untagged_copy_cannot_mask_tagged_launcher_drift(tmp_path: Path) -> None:
    project = _write_project(tmp_path)
    local_prompt = (project / "init" / "init-prompt.md").read_text(encoding="utf-8")
    stale = local_prompt.replace("<init-prompt>", "<stale-copy>").replace(
        "</init-prompt>", "</stale-copy>"
    )
    (tmp_path / "init" / "init-prompt.md").write_text(
        "# Root launcher catalog\n\n"
        f"{stale}\n"
        "<init-prompt>\n"
        "Set project path to `projects/chirality-app-dev`.\n"
        "Act as `HELP_HUMAN` for a divergent root launcher.\n"
        "</init-prompt>\n",
        encoding="utf-8",
    )
    assert validator.validate(tmp_path) == [
        f"{project.relative_to(tmp_path)}/init/init-prompt.md does not byte-match the "
        "tagged root launcher for projects/chirality-app-dev"
    ]


def test_rejects_topology_section_for_help_human_entry(tmp_path: Path) -> None:
    project = _write_project(
        tmp_path,
        loop_text="# Loop\n\n## Multi-agent orchestration\n\nCanonical mechanics here.\n",
    )
    findings = validator.validate(tmp_path)
    assert findings == [
        f"{project.relative_to(tmp_path)}/loop/LOOP_INIT.md duplicates canonical "
        "runtime mechanics in section 'Multi-agent orchestration'"
    ]


def test_rejects_exact_runtime_role_routing_matrix_heading(tmp_path: Path) -> None:
    project = _write_project(
        tmp_path,
        loop_text="# Loop\n\n## Runtime role-routing matrix\n\nCanonical mechanics here.\n",
    )
    findings = validator.validate(tmp_path)
    assert findings == [
        f"{project.relative_to(tmp_path)}/loop/LOOP_INIT.md duplicates canonical "
        "runtime mechanics in section 'Runtime role-routing matrix'"
    ]


def test_rejects_named_role_routing_paragraph(tmp_path: Path) -> None:
    project = _write_project(
        tmp_path,
        workplan_text=(
            "# Standing workplan\n\n"
            "HELP_HUMAN launches WORKING_ITEMS for the selected packages.\n"
        ),
    )
    findings = validator.validate(tmp_path)
    assert findings == [
        f"{project.relative_to(tmp_path)}/loop/WORKPLAN_2026-07-18_test.md "
        "duplicates canonical role routing in paragraph: "
        "'HELP_HUMAN launches WORKING_ITEMS for the selected packages.'"
    ]


def test_rejects_two_mechanics_clusters_in_one_section(tmp_path: Path) -> None:
    project = _write_project(
        tmp_path,
        loop_text=(
            "# Loop\n\n## Execution\n\n"
            "Persist child sessions in the run record. Concurrent writes use an "
            "integration owner.\n"
        ),
    )
    findings = validator.validate(tmp_path)
    assert findings == [
        f"{project.relative_to(tmp_path)}/loop/LOOP_INIT.md duplicates canonical "
        "runtime mechanics clusters: child-session persistence, "
        "concurrent-write/fan-in ownership"
    ]


def test_mechanics_cluster_prose_is_case_insensitive(tmp_path: Path) -> None:
    cases = (
        (
            "Child sessions are persisted. Model assignment is recorded here.",
            "child-session persistence, model/capability assignment",
        ),
        (
            "Selection authority is recorded. Integration owner mechanics apply.",
            "selection-authority/posture, concurrent-write/fan-in ownership",
        ),
    )
    for index, (body, labels) in enumerate(cases):
        case_root = tmp_path / f"case-{index}"
        case_root.mkdir()
        project = _write_project(
            case_root,
            loop_text=f"# Loop\n\n## Execution\n\n{body}\n",
        )
        findings = validator.validate(case_root)
        assert findings == [
            f"{project.relative_to(case_root)}/loop/LOOP_INIT.md duplicates "
            f"canonical runtime mechanics clusters: {labels}"
        ]


def test_child_session_schema_and_agentruns_cluster_forms(tmp_path: Path) -> None:
    cases = (
        "The child-session persistence schema is recorded. Integration owner "
        "mechanics apply.",
        "The run is recorded in AgentRuns/<RunID>. Integration owner mechanics "
        "apply.",
    )
    for index, body in enumerate(cases):
        case_root = tmp_path / f"case-{index}"
        case_root.mkdir()
        project = _write_project(
            case_root,
            loop_text=f"# Loop\n\n## Execution\n\n{body}\n",
        )
        findings = validator.validate(case_root)
        assert findings == [
            f"{project.relative_to(case_root)}/loop/LOOP_INIT.md duplicates "
            "canonical runtime mechanics clusters: child-session persistence, "
            "concurrent-write/fan-in ownership"
        ]


def test_allows_by_reference_citation(tmp_path: Path) -> None:
    _write_project(
        tmp_path,
        workplan_text=(
            "# Standing workplan\n\n"
            "Runtime hierarchy and delegation are governed by root `AGENTS.md`, "
            "the project `AGENTS.md`, and the active canonical agent instructions.\n"
        ),
    )
    assert validator.validate(tmp_path) == []


def test_allows_by_reference_citation_with_two_cluster_terms(tmp_path: Path) -> None:
    _write_project(
        tmp_path,
        workplan_text=(
            "# Standing workplan\n\n"
            "Child sessions and integration owner mechanics are governed by root "
            "`AGENTS.md`.\n"
        ),
    )
    assert validator.validate(tmp_path) == []


def test_citation_cannot_mask_named_persist_routing(tmp_path: Path) -> None:
    for index, verb in enumerate(("persist", "persists", "persisted", "persisting")):
        case_root = tmp_path / f"case-{index}"
        case_root.mkdir()
        project = _write_project(
            case_root,
            workplan_text=(
                "# Standing workplan\n\n"
                f"Per root AGENTS.md, HELP_HUMAN {verb} TASK child sessions.\n"
            ),
        )
        findings = validator.validate(case_root)
        assert any(
            finding.startswith(
                f"{project.relative_to(case_root)}/loop/"
                "WORKPLAN_2026-07-18_test.md duplicates canonical role routing"
            )
            for finding in findings
        )


def test_citation_cannot_mask_prescriptive_inflections(tmp_path: Path) -> None:
    project = _write_project(
        tmp_path,
        workplan_text=(
            "# Standing workplan\n\n"
            "Per root AGENTS.md, HELP_HUMAN records TASK child sessions and uses "
            "an integration owner.\n"
        ),
    )
    findings = validator.validate(tmp_path)
    rel = project.relative_to(tmp_path)
    assert any(
        finding.startswith(
            f"{rel}/loop/WORKPLAN_2026-07-18_test.md duplicates canonical "
            "runtime mechanics clusters"
        )
        for finding in findings
    )


def test_allows_ordinary_lowercase_task_and_isolated_terms(tmp_path: Path) -> None:
    _write_project(
        tmp_path,
        workplan_text=(
            "# Standing workplan\n\n"
            "This task records a work graph observation before fan-in.\n"
        ),
    )
    assert validator.validate(tmp_path) == []


def test_agent_names_are_case_sensitive(tmp_path: Path) -> None:
    _write_project(
        tmp_path,
        workplan_text=(
            "# Standing workplan\n\n"
            "help_human launches working_items for the selected packages.\n"
        ),
    )
    assert validator.validate(tmp_path) == []


def test_structural_checks_are_dormant_without_help_human_entry(tmp_path: Path) -> None:
    _write_project(
        tmp_path,
        project_name="chirality-piping",
        entry_role="WORKING_ITEMS",
        loop_text=(
            "# Loop\n\n## Multi-agent orchestration\n\n"
            "HELP_HUMAN launches WORKING_ITEMS. Persist child sessions and use "
            "an integration owner.\n"
        ),
    )
    assert validator.validate(tmp_path) == []


def test_help_human_activation_does_not_require_markdown_backticks(
    tmp_path: Path,
) -> None:
    project = _write_project(
        tmp_path,
        loop_text=(
            "# Loop\n\n## Runtime role-routing matrix\n\nCanonical mechanics here.\n"
        ),
    )
    for path in (
        project / "init" / "init-prompt.md",
        tmp_path / "init" / "init-prompt.md",
    ):
        text = path.read_text(encoding="utf-8")
        text = text.replace("`HELP_HUMAN`", "HELP_HUMAN").replace(
            "`{WORKING_ROOT}`", "{WORKING_ROOT}"
        )
        path.write_text(text, encoding="utf-8")
    findings = validator.validate(tmp_path)
    assert any("Runtime role-routing matrix" in finding for finding in findings)


def test_entire_current_repository_passes() -> None:
    assert validator.validate(REPO_ROOT) == []
