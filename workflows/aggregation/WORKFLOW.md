---
name: aggregation
description: Combine selected records into a traceable cross-scope view, including estimate collation.
---

# aggregation

Combine selected records into a traceable cross-scope view, including estimate collation.

TASK executes this bounded contribution and returns evidence to its caller.

## Method

1. Freeze the source manifest and previous accepted aggregate, defining stable namespaced record keys and the conflict policy.
2. Apply the selected collation profile, validating row eligibility, units, and currency before computing totals.
3. Merge incrementally from the selected inputs; expose duplicate keys, changed values, excluded rows, and unresolved conflicts.
4. Publish a new derivative snapshot with source hashes, exact coverage, and any explicitly authorized pointer update.

## Resources

Load [inputs, modes, and output contracts](resources/contract.md) when framing the assignment. Use [the detailed method](resources/method.md) for the current stage. Resolve tool commands against the declared tool root.
