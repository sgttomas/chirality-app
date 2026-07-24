---
name: software-repository-reconnaissance
description: Map a software repository's manifests, architecture, test surfaces, commands, ownership boundaries, and risks before planning or implementation. Use for unfamiliar repositories, novel stacks, package activation, or before sealing a software work brief.
allowed-tools: python3 tools/software_workflow/discover_repository.py:*, python3 tools/software_workflow/select_affected_checks.py:*
metadata:
  chirality-skill-version: "1"
  chirality-task-profile: NONE
---

# Software repository reconnaissance

## Method

1. Read the sealed brief, project instructions, accepted decomposition, and software profile.
2. Run deterministic repository discovery before broad manual exploration.
3. Trace only the manifests, entry points, interfaces, tests, generators, and dependency surfaces relevant to the package objective.
4. Separate observed facts, supported inferences, unknowns, and proposed follow-up.
5. Return a bounded map; do not implement changes.

## Required inputs

- project and package scope;
- accepted basis and objective;
- declared read scope;
- project-local software profile when present.

## Outputs

- component and dependency map;
- registered build/test/lint/typecheck surfaces;
- likely affected paths and checks;
- risks, unknowns, and human decision points;
- recommended Agent 2 task boundaries.

Safe for generic TASK with `ApplyEdits: false`. Never infer authority from a discovered command or file.
