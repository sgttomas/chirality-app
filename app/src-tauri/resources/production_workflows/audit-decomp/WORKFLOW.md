---
name: audit-decomp
description: Reconcile accepted decomposition with materialized scope and current derivative evidence.
metadata:
  kind: instruction
  surface: workflow
---

# audit-decomp

Reconcile accepted decomposition with materialized scope and current derivative evidence.

TASK executes this bounded contribution and returns evidence to its caller.

## Method

1. Resolve the variant and bind semantic sections by heading text using the contract’s Variant Section Binding algorithm.
2. Bind the companion registers named in the package inventory, then compare declared partitions and production units with folders in both directions (using `tools/evaluation/audit_structure.py` for inventory and lifecycle) and inspect identity, context, artifacts, and objective coverage.
3. Check current derivatives and handoff state against their accepted source snapshot; use `tools/validation/validate_domain_decomposition_integrity.py` for its registered DOMAIN checks. Classify findings explained by an accepted decision as `EXPECTED_CONSEQUENCE`.
4. Emit the canonical coverage matrix, findings, and closure-readiness result, disclosing partial parses and unavailable checks. The invoking manager, not the TASK, moves `_LATEST.md` after 0 BLOCKERs when its brief authorizes it.

## Resources

Load [inputs, modes, and output contracts](resources/contract.md) when framing the assignment. Use [the detailed method](resources/method.md) for the current stage. Resolve tool commands against the declared tool root.
