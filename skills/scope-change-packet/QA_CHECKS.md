# QA CHECKS — scope-change-packet

## Required Checks

- Required ten packet files exist.
- Required CSV columns are present.
- Every `Proposed_SCA_Actions.csv` row has non-empty `EvidenceRefs`.
- Every affected deliverable ID exists in the current decomposition authority or is explicitly marked `TBD`.
- Packet text does not claim:
  - dependency rows were changed;
  - SCC closure was achieved;
  - SCOPE_CHANGE was initiated;
  - project-wide blocked/unblocked state is reportable.
- PKG-00 contains no `Dependencies.csv`.
- `SCOPE_CHANGE_INIT.md` states that human initiation is required.

## Readiness Verdict

Use one of:

- `READY_FOR_HUMAN_REVIEW`
- `SELECTED_FOR_SCOPE_CHANGE_INTAKE`
- `BLOCKED_TBD`

`READY_FOR_HUMAN_REVIEW` requires all required files, evidence-backed proposed actions, and no blocking validator failures. It means the packet is structurally complete enough for review.

`SELECTED_FOR_SCOPE_CHANGE_INTAKE` is not a TASK-authored default. Use it only after a human explicitly selects the packet as a SCOPE_CHANGE seed. It does not bypass SCOPE_CHANGE gates.
