---
name: software-test-planning
description: Derive a risk-based verification plan and affected registered checks for a bounded software change. Use before implementation, at fan-in, or after a defect when test selection, evidence sufficiency, negative cases, or acceptance gates must be made explicit.
allowed-tools: python3 tools/software_workflow/discover_repository.py:*, python3 tools/software_workflow/select_affected_checks.py:*
metadata:
  chirality-skill-version: "1"
  chirality-task-profile: NONE
---

# Software test planning

## Method

1. Map the objective and changed surfaces to observable behavior and failure modes.
2. Use the accepted profile to select affected registered checks.
3. Add targeted tests for behavior not covered by registered checks.
4. Define unit, integration, contract, migration, UI, performance, or manual evidence only where risk warrants it.
5. State sequencing, prerequisites, pass criteria, and evidence outputs.

## Outputs

- risk-to-test matrix;
- affected registered check IDs with selection reasons;
- new or modified test cases;
- evidence and fan-in acceptance criteria;
- gaps requiring human disposition.

Safe for generic TASK with `ApplyEdits: false` unless test-file changes are separately authorized.
