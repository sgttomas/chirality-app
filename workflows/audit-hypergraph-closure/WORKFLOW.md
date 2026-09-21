---
name: audit-hypergraph-closure
description: Assess whether a graph snapshot’s structure and coverage match its declared source basis.
---

# audit-hypergraph-closure

Assess whether a graph snapshot’s structure and coverage match its declared source basis.

TASK executes this bounded contribution and returns evidence to its caller.

## Method

1. Freeze the graph snapshot and accepted upstream basis; inventory available tables and optional ledger inputs.
2. Inspect incidence, arity, entity membership, partition boundaries, knowledge subjects, and materialization bridges using the current builder vocabulary.
3. Record missing required data as incomplete checks and absent optional data as skipped checks.
4. Report full finding counts separately from displayed rows and distinguish audit completion from graph acceptance.

## Resources

Load [inputs, modes, and output contracts](resources/contract.md) when framing the assignment. Use [the detailed method](resources/method.md) for the current stage. Resolve tool commands against the declared tool root.
