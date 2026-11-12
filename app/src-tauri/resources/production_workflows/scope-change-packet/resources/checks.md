# QA CHECKS — scope-change-packet

## Required Checks

- Required ten packet files exist.
- Required CSV columns are present. `SCOPE_CHANGE_Checkpoint` is required; the legacy name `SCOPE_CHANGE_Gate` is accepted in its place on historical packets.
- Every `Proposed_SCA_Actions.csv` row has non-empty `EvidenceRefs`.
- Every affected deliverable ID exists in the current decomposition authority or is explicitly marked `TBD`.
- Packet text does not claim:
  - local need declarations were changed;
  - SCC closure was achieved;
  - WORKING_ITEMS (workflow: scope-change) was initiated;
  - project-wide blocked/unblocked state is reportable.
- The packet creates no dependency declarations or central dependency map; all local needs remain read-only.
- `SCOPE_CHANGE_INIT.md` states that human initiation is required.

## Readiness Verdict

Use one of:

- `READY_FOR_HUMAN_REVIEW`
- `SELECTED_FOR_SCOPE_CHANGE_INTAKE`
- `BLOCKED_TBD`

`READY_FOR_HUMAN_REVIEW` requires all required files, evidence-backed proposed actions, and no blocking validator failures. It means the packet is structurally complete enough for review.

`SELECTED_FOR_SCOPE_CHANGE_INTAKE` is not a TASK-authored default. Use it only after a human explicitly selects the packet as a WORKING_ITEMS (workflow: scope-change) seed. It does not bypass the WORKING_ITEMS (workflow: scope-change) checkpoint groups.
