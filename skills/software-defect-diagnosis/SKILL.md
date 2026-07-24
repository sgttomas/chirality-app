---
name: software-defect-diagnosis
description: Reproduce, isolate, and explain a software defect using bounded evidence without assuming repair authority. Use for failing tests, regressions, runtime errors, performance anomalies, or conflicting reports that require a causal diagnosis before implementation.
allowed-tools: python3 tools/software_workflow/discover_repository.py:*, python3 tools/software_workflow/select_affected_checks.py:*, python3 tools/software_workflow/run_registered_checks.py:*
metadata:
  chirality-skill-version: "1"
  chirality-task-profile: NONE
---

# Software defect diagnosis

## Method

1. Freeze the observed symptom, environment, expected behavior, and reproduction boundary.
2. Reproduce with the narrowest registered check or deterministic probe available.
3. Reduce competing hypotheses through evidence, tracing inputs to the earliest divergent state.
4. Distinguish root cause, contributing conditions, consequences, and unknowns.
5. Return repair options and verification needs; do not edit unless the brief separately authorizes implementation.

## Outputs

- reproduction result and evidence;
- causal chain with confidence and alternatives considered;
- affected surfaces and likely dependants;
- bounded repair options and regression-test recommendation.

Safe for generic TASK with `ApplyEdits: false`.
