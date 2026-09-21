---
name: audit-decomp
description: Reconcile accepted decomposition with materialized scope and current derivative evidence.
---

# audit-decomp

Reconcile accepted decomposition with materialized scope and current derivative evidence.

TASK executes this bounded contribution and returns evidence to its caller.

## Method

1. Resolve the variant and bind semantic sections by heading text using the contract’s Variant Section Binding algorithm.
2. Compare declared partitions and production units with folders in both directions, then inspect identity, context, artifacts, and objective coverage.
3. Check current derivatives and handoff state against their accepted source snapshot; use the DOMAIN integrity tool for its registered checks.
4. Emit the canonical coverage matrix, findings, and closure-readiness result, disclosing partial parses and unavailable checks.

## Resources

Load [inputs, modes, and output contracts](resources/contract.md) when framing the assignment. Use [the detailed method](resources/method.md) for the current stage. Resolve tool commands against the declared tool root.
