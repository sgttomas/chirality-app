#!/usr/bin/env python3

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path


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

    def test_loop_register_level_type1_scope_is_valid(self) -> None:
        text = (
            VALID_AGENT.replace("— TASK (", "— TASK_MANAGEMENT (")
            .replace("AGENT_TYPE: 2", "AGENT_TYPE: 1")
            .replace("TYPE 2", "TYPE 1")
            .replace("| TASK |", "| PERSONA |")
            .replace("| INIT-TASK |", "| chat |")
            .replace("| bounded-task-brief |", "| loop-register-level |")
            .replace("| never |", "| allowed |")
        )
        self.assertEqual([], self.validate(text, "AGENT_TASK_MANAGEMENT.md"))

    def test_unrecognized_write_scope_is_invalid(self) -> None:
        findings = self.validate(
            VALID_AGENT.replace("| bounded-task-brief |", "| arbitrary-scope |")
        )
        self.assertIn("WRITE_SCOPE_INVALID", {item.code for item in findings})

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

    def test_hierarchy_accepts_help_human_to_manager_and_canonical_task(self) -> None:
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
            manager_text.replace("subagents: TASK", "subagents: WORKING_ITEMS, TASK")
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

    def test_hierarchy_rejects_agent0_to_non_task_agent2(self) -> None:
        specialist_text = VALID_AGENT.replace("— TASK (", "— SPECIALIST (")
        specialist = self.root / "agents" / "AGENT_SPECIALIST.md"
        specialist.write_text(specialist_text, encoding="utf-8")
        architect_text = (
            VALID_AGENT.replace(
                'description: "fixture"',
                'description: "fixture"\nsubagents: SPECIALIST',
            )
            .replace("— TASK (", "— HELP_HUMAN (")
            .replace("AGENT_TYPE: 2", "AGENT_TYPE: 0")
            .replace("TYPE 2", "TYPE 0")
            .replace("| TASK |", "| PERSONA |")
            .replace("| INIT-TASK |", "| chat |")
            .replace("| never |", "| allowed |")
        )
        architect = self.root / "agents" / "AGENT_HELP_HUMAN.md"
        architect.write_text(architect_text, encoding="utf-8")
        findings = validator.validate_hierarchy([architect, specialist], self.root)
        self.assertIn("AGENT0_CHILD_TYPE", {item.code for item in findings})

    def test_hierarchy_rejects_unresolved_agent0_child(self) -> None:
        architect_text = (
            VALID_AGENT.replace(
                'description: "fixture"',
                'description: "fixture"\nsubagents: MISSING',
            )
            .replace("— TASK (", "— HELP_HUMAN (")
            .replace("AGENT_TYPE: 2", "AGENT_TYPE: 0")
            .replace("TYPE 2", "TYPE 0")
            .replace("| TASK |", "| PERSONA |")
            .replace("| INIT-TASK |", "| chat |")
            .replace("| never |", "| allowed |")
        )
        architect = self.root / "agents" / "AGENT_HELP_HUMAN.md"
        architect.write_text(architect_text, encoding="utf-8")
        findings = validator.validate_hierarchy([architect], self.root)
        self.assertIn("SUBAGENT_ROLE_UNRESOLVED", {item.code for item in findings})

    def test_hierarchy_rejects_generalist_opt_in_on_agent2(self) -> None:
        task = self.root / "agents" / "AGENT_TASK.md"
        task.write_text(
            VALID_AGENT.replace(
                'description: "fixture"',
                'description: "fixture"\nallow_generalist_agent2: true',
            ),
            encoding="utf-8",
        )
        architect_text = (
            VALID_AGENT
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
        self.assertIn("GENERALIST_PARENT_TYPE", {item.code for item in findings})

    def test_hierarchy_keeps_agent1_to_agent1_rejected(self) -> None:
        manager_text = (
            VALID_AGENT.replace(
                'description: "fixture"',
                'description: "fixture"\nsubagents: REVIEW',
            )
            .replace("— TASK (", "— WORKING_ITEMS (")
            .replace("AGENT_TYPE: 2", "AGENT_TYPE: 1")
            .replace("TYPE 2", "TYPE 1")
            .replace("| TASK |", "| PERSONA |")
            .replace("| INIT-TASK |", "| both |")
            .replace("| never |", "| allowed |")
        )
        manager = self.root / "agents" / "AGENT_WORKING_ITEMS.md"
        manager.write_text(manager_text, encoding="utf-8")
        peer = self.root / "agents" / "AGENT_REVIEW.md"
        peer.write_text(
            manager_text.replace("subagents: REVIEW\n", "").replace(
                "— WORKING_ITEMS (", "— REVIEW ("
            ),
            encoding="utf-8",
        )
        architect = self.root / "agents" / "AGENT_HELP_HUMAN.md"
        architect.write_text(
            manager_text.replace("subagents: REVIEW\n", "")
            .replace("— WORKING_ITEMS (", "— HELP_HUMAN (")
            .replace("AGENT_TYPE: 1", "AGENT_TYPE: 0")
            .replace("TYPE 1", "TYPE 0"),
            encoding="utf-8",
        )
        findings = validator.validate_hierarchy([architect, manager, peer], self.root)
        self.assertIn("AGENT1_CHILD_TYPE", {item.code for item in findings})

    def test_hierarchy_keeps_agent2_delegation_rejected(self) -> None:
        task = self.root / "agents" / "AGENT_TASK.md"
        task.write_text(
            VALID_AGENT.replace(
                'description: "fixture"',
                'description: "fixture"\nsubagents: TASK',
            ),
            encoding="utf-8",
        )
        architect = self.root / "agents" / "AGENT_HELP_HUMAN.md"
        architect.write_text(
            VALID_AGENT.replace("— TASK (", "— HELP_HUMAN (")
            .replace("AGENT_TYPE: 2", "AGENT_TYPE: 0")
            .replace("TYPE 2", "TYPE 0")
            .replace("| TASK |", "| PERSONA |")
            .replace("| INIT-TASK |", "| chat |")
            .replace("| never |", "| allowed |"),
            encoding="utf-8",
        )
        findings = validator.validate_hierarchy([architect, task], self.root)
        self.assertIn("TYPE2_DELEGATION_DECLARED", {item.code for item in findings})

    def test_canonical_task_still_requires_task_class(self) -> None:
        findings = self.validate(VALID_AGENT.replace("| TASK |", "| PERSONA |"))
        self.assertIn("TYPE2_CLASS", {item.code for item in findings})

    def test_live_help_human_declares_narrow_agent0_direct_agent2_metadata(self) -> None:
        root = Path(validator.__file__).resolve().parents[2]
        import json
        role = json.loads((root / 'agents/registry.json').read_text())['roles']['HELP_HUMAN']
        self.assertIn('TASK', role['delegates_to'])
        self.assertTrue(role['allow_generalist_agent2'])
        self.assertTrue(role['direct_entry'])



if __name__ == "__main__":
    unittest.main()
