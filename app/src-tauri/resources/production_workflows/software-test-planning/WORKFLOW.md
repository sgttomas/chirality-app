---
name: software-test-planning
description: Derive a risk-based verification plan and affected registered checks for a bounded software change. Use before implementation, at fan-in, or after a defect when test selection, evidence sufficiency, negative cases, or acceptance gates must be made explicit.
metadata:
  kind: instruction
  surface: workflow
---

# Software test planning

## Method

1. Map the objective and changed surfaces to observable behavior and failure modes.
2. Where the assignment supplies acceptance criteria, give each criterion, and each distinct claim within it, a check of stated kind, and say how an implementation that misses the claim would fail it. The kinds are an executable check, a comparison with a named reference, and a judgment by a named role; `scope-of-work` defines them.
3. Use the accepted profile to select affected registered checks.
4. Add targeted tests for behavior not covered by registered checks.
5. Define unit, integration, contract, migration, UI, performance, or manual evidence only where risk warrants it.
6. State sequencing, prerequisites, pass criteria, and evidence outputs.

## Outputs

- for supplied acceptance criteria, a check of stated kind for each claim, with what it observes and what would make it fail;
- risk-to-test matrix;
- affected registered check IDs with selection reasons;
- new or modified test cases;
- evidence and fan-in acceptance criteria;
- gaps requiring human disposition.

Safe for generic TASK with `ApplyEdits: false` unless test-file changes are separately authorized.
