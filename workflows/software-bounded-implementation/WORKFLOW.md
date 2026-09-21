---
name: software-bounded-implementation
description: Implement one sealed software change within explicit write targets and acceptance criteria, then produce normalized verification
  evidence. Use for bounded features, repairs, refactors, migrations, or documentation changes after the owning manager freezes scope.
---

# Software bounded implementation

## Method

1. Confirm the sealed objective, accepted basis, write targets, exclusions, and acceptance checks.
2. Inspect the smallest relevant implementation and test surface.
3. Make the minimum coherent change; preserve unrelated user work.
4. Add or update tests proportionate to behavior and risk.
5. Select and run only registered checks authorized by the brief.
6. Validate changed paths against the write fence and return the diff, evidence, residual risks, and blockers.

Do not change scope, public contracts, migrations, shared ownership, or acceptance criteria silently. Report those needs to the parent.

## Outputs

- implemented files and behavioral summary;
- normalized check evidence references;
- write-scope validation;
- unresolved risks, follow-up, and coordination notices.

Safe for generic TASK only with explicit write targets and `ApplyEdits: true`.
