---
name: audit-agents
description: Assess role instructions against a named design basis and propose evidence-linked repairs.
---

# audit-agents

Assess role instructions against a named design basis and propose evidence-linked repairs.

TASK executes this bounded contribution and returns evidence to its caller.

## Method

1. Select conformance or authorized redesign in the brief and freeze the instruction sources and accepted criteria.
2. Run the instruction validator, then inspect the semantic rubric with paired subject-and-criterion evidence.
3. Classify findings and produce a prioritized patch plan; in conformance mode prefer the smallest coherent repair.
4. Return complete scope coverage and distinguish missing-input checks from completed checks and proposals.

## Resources

Load [inputs, modes, and output contracts](resources/contract.md) when framing the assignment. Use [the detailed method](resources/method.md) for the current stage. Resolve tool commands against the declared tool root.
