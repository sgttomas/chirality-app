---
name: review
description: Guide evidence review and human disposition for a deliverable lifecycle transition.
metadata:
  category: Review and validation
  applicability: Review evidence and obtain human disposition for a deliverable lifecycle transition.
  kind: instruction
  surface: workflow
---

# review

For repository development, follow the project's `AGENTS.md` for lifecycle and
record procedures. Select this formal product-review method only when the
assignment calls for it. Keep routine development records under those project
instructions rather than creating lifecycle status files for this method.

Guide evidence review and human disposition for one deliverable's lifecycle
transition under `docs/COMPATIBILITY_FORMATS.md#historical-specification` §3.3–3.4: a candidacy check for entry to
`CHECKING`, the check of a frozen `CHECKING` candidate toward `ISSUED`, and
the human-ruled reversal `CHECKING → IN_PROGRESS` for an unsuccessful or
withdrawn check.

WORKING_ITEMS coordinates this undertaking and assigns bounded contributions to TASK.

## Method

1. Confirm the transition, current lifecycle state, owning-loop fences, accepted criteria, and exact source bindings.
2. For entry to `CHECKING`, establish a current candidate-bound account showing no unfulfilled production obligation and a declared checking basis; there is no deferral path into `CHECKING`.
3. Populate the checklist, capture findings, and obtain human dispositions through the five gates.
4. At Gate 5, check current owner holds and product issuance boundaries, record the human decision (freeze with the frozen candidate SHA, issuance, reversal, or decline), finalize a new immutable review snapshot, and update only the authorized pointer.

## Resources

Load [inputs, modes, and output contracts](resources/contract.md) when framing the assignment. Use [the detailed method](resources/method.md) for the current stage. Resolve tool commands against `{INSTRUCTION_ROOT}`.
