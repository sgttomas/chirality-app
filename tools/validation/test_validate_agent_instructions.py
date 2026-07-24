#!/usr/bin/env python3

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import validate_agent_instructions as validator


VALID_AGENT = """---
description: "fixture"
---
[[DOC:AGENT_INSTRUCTIONS]]
# AGENT INSTRUCTIONS — TASK (Fixture)
AGENT_TYPE: 2

## Agent Type
| Property | Value |
|---|---|
| **AGENT_TYPE** | TYPE 2 |
| **AGENT_CLASS** | TASK |
| **INTERACTION_SURFACE** | INIT-TASK |
| **WRITE_SCOPE** | bounded-task-brief |
| **BLOCKING** | never |
| **PRIMARY_OUTPUTS** | fixture |

[[BEGIN:PROTOCOL]]
## PROTOCOL
[[END:PROTOCOL]]
[[BEGIN:SPEC]]
## SPEC
[[END:SPEC]]
[[BEGIN:STRUCTURE]]
## STRUCTURE
[[END:STRUCTURE]]
[[BEGIN:RATIONALE]]
## RATIONALE
[[END:RATIONALE]]
"""


class ValidateAgentInstructionsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "agents").mkdir()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def validate(self, text: str, name: str = "AGENT_TASK.md") -> list[validator.Finding]:
        path = self.root / "agents" / name
        path.write_text(text, encoding="utf-8")
        return validator.validate_file(path, self.root, {"R1", "R12", "R17"})

    def test_valid_task_fixture(self) -> None:
        self.assertEqual([], self.validate(VALID_AGENT))

    def test_package_level_type1_scope_is_valid(self) -> None:
        text = (
            VALID_AGENT.replace("— TASK (", "— WORKING_ITEMS (")
            .replace("AGENT_TYPE: 2", "AGENT_TYPE: 1")
            .replace("TYPE 2", "TYPE 1")
            .replace("| TASK |", "| PERSONA |")
            .replace("| INIT-TASK |", "| both |")
            .replace("| bounded-task-brief |", "| package-level |")
            .replace("| never |", "| allowed |")
        )
        self.assertEqual([], self.validate(text, "AGENT_WORKING_ITEMS.md"))

    def test_type_mismatch_is_error(self) -> None:
        findings = self.validate(VALID_AGENT.replace("AGENT_TYPE: 2", "AGENT_TYPE: 1"))
        self.assertIn("TYPE_MISMATCH", {item.code for item in findings})

    def test_non_task_type2_requires_requalification(self) -> None:
        text = VALID_AGENT.replace("— TASK (", "— AUDITOR (")
        findings = self.validate(text, "AGENT_AUDITOR.md")
        self.assertIn("TYPE2_REQUALIFICATION_REQUIRED", {item.code for item in findings})

    def test_ruled_dedicated_type2_approval_closes_warning(self) -> None:
        decisions = self.root / "docs" / "governance_harness" / "_DECISIONS"
        decisions.mkdir(parents=True)
        (decisions / "D-GOV-13_fixture.md").write_text(
            "# D-GOV-13\n\nStatus: RULED\n\n| Role | Basis |\n|---|---|\n| AUDITOR | stable contract |\n",
            encoding="utf-8",
        )
        text = VALID_AGENT.replace(
            'description: "fixture"',
            'description: "fixture"\ndedicated_agent2_approval: D-GOV-13',
        ).replace("— TASK (", "— AUDITOR (")
        self.assertEqual([], self.validate(text, "AGENT_AUDITOR.md"))

    def test_body_text_cannot_impersonate_dedicated_approval_frontmatter(self) -> None:
        text = VALID_AGENT.replace("— TASK (", "— AUDITOR (").replace(
            "## PROTOCOL",
            "```yaml\ndedicated_agent2_approval: D-GOV-13\n```\n## PROTOCOL",
        )
        findings = self.validate(text, "AGENT_AUDITOR.md")
        self.assertIn("TYPE2_REQUALIFICATION_REQUIRED", {item.code for item in findings})

    def test_all_positive_r_identifiers_are_checked_against_catalog(self) -> None:
        findings = self.validate(VALID_AGENT.replace("## PROTOCOL", "R117\n## PROTOCOL"))
        self.assertIn("R_ID_UNKNOWN", {item.code for item in findings})

    def test_missing_agent_reference_warns(self) -> None:
        text = VALID_AGENT.replace("## PROTOCOL", "See `AGENT_MISSING.md`.\n## PROTOCOL")
        findings = self.validate(text)
        self.assertIn("AGENT_REFERENCE_UNRESOLVED", {item.code for item in findings})

    def test_current_audit_output_must_use_evaluation_root(self) -> None:
        text = VALID_AGENT.replace("— TASK (", "— AUDIT_SAMPLE (").replace(
            "| bounded-task-brief |",
            "| tool-root-only (`{EXECUTION_ROOT}/_Reconciliation/Sample/`) |",
        )
        findings = self.validate(text, "AGENT_AUDIT_SAMPLE.md")
        self.assertIn("AUDIT_OUTPUT_ROOT_INVALID", {item.code for item in findings})

    def test_hierarchy_accepts_help_human_to_manager_to_task(self) -> None:
        task = self.root / "agents" / "AGENT_TASK.md"
        task.write_text(VALID_AGENT, encoding="utf-8")
        manager_text = (
            VALID_AGENT.replace('description: "fixture"', 'description: "fixture"\nsubagents: TASK\nallow_generalist_agent2: true')
            .replace("— TASK (", "— WORKING_ITEMS (")
            .replace("AGENT_TYPE: 2", "AGENT_TYPE: 1")
            .replace("TYPE 2", "TYPE 1")
            .replace("| TASK |", "| PERSONA |")
            .replace("| INIT-TASK |", "| both |")
            .replace("| never |", "| allowed |")
        )
        manager = self.root / "agents" / "AGENT_WORKING_ITEMS.md"
        manager.write_text(manager_text, encoding="utf-8")
        architect_text = (
            manager_text.replace("subagents: TASK", "subagents: WORKING_ITEMS")
            .replace("allow_generalist_agent2: true\n", "")
            .replace("— WORKING_ITEMS (", "— HELP_HUMAN (")
            .replace("AGENT_TYPE: 1", "AGENT_TYPE: 0")
            .replace("TYPE 1", "TYPE 0")
        )
        architect = self.root / "agents" / "AGENT_HELP_HUMAN.md"
        architect.write_text(architect_text, encoding="utf-8")
        self.assertEqual(
            [],
            validator.validate_hierarchy([architect, manager, task], self.root),
        )

    def test_hierarchy_rejects_agent0_to_agent2(self) -> None:
        task = self.root / "agents" / "AGENT_TASK.md"
        task.write_text(VALID_AGENT, encoding="utf-8")
        architect_text = (
            VALID_AGENT.replace('description: "fixture"', 'description: "fixture"\nsubagents: TASK')
            .replace("— TASK (", "— HELP_HUMAN (")
            .replace("AGENT_TYPE: 2", "AGENT_TYPE: 0")
            .replace("TYPE 2", "TYPE 0")
            .replace("| TASK |", "| PERSONA |")
            .replace("| INIT-TASK |", "| chat |")
            .replace("| never |", "| allowed |")
        )
        architect = self.root / "agents" / "AGENT_HELP_HUMAN.md"
        architect.write_text(architect_text, encoding="utf-8")
        findings = validator.validate_hierarchy([architect, task], self.root)
        self.assertIn("AGENT0_CHILD_TYPE", {item.code for item in findings})


if __name__ == "__main__":
    unittest.main()
