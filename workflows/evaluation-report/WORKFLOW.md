---
name: evaluation-report
description: Evaluate one dimension against an accepted rubric and return a supported score.
---

# evaluation-report

Evaluate one dimension against an accepted rubric and return a supported score.

TASK executes this bounded contribution and returns evidence to its caller.

## Method

1. Confirm the dimension, accepted rubric, frozen evidence, scope, and required checks.
2. Apply every selected check and record supporting evidence, unavailable checks, and interpretation limits.
3. Derive the dimension score from the rubric, preserving critical findings and missing evidence.
4. Return the scored report and structured result for the manager’s cross-dimension synthesis.

## Resources

Load [inputs, modes, and output contracts](resources/contract.md) when framing the assignment. Use [the detailed method](resources/method.md) for the current stage. Resolve tool commands against the declared tool root.
