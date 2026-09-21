---
name: researcher
description: Investigate one bounded question through independently verified and recoverable evidence.
---

# researcher

Investigate one bounded question through independently verified and recoverable evidence.

TASK executes this bounded contribution and returns evidence to its caller.

## Method

1. Bind accepted sources and the caller-allocated OUTPUT_DIR, then create a packet without updating a shared pointer.
2. Scout retrieval freshness, classify the question, log actual queries, and read the underlying evidence.
3. Independently verify load-bearing anchors and record evidence quality, verification source, and READ/RUN assertion mode.
4. Return COMPLETE, PARTIAL, or FAILED_INPUTS with preserved packet evidence and explicit coverage gaps; the owner handles integration, retries, and pointers.

## Resources

Load [inputs, modes, and output contracts](resources/contract.md) when framing the assignment. Use [the detailed method](resources/method.md) for the current stage. Resolve tool commands against the declared tool root.
