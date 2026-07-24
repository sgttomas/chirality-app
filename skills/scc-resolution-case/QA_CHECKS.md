# QA CHECKS — scc-resolution-case

## Required Checks

- Required case files exist.
- Required CSV columns are present.
- `CaseState` is one of the canonical lifecycle states.
- Every candidate remedy has evidence or a `TBD` reason.
- Every owner handoff names an owning workflow.
- Case text does not claim SCC closure unless cited DepClosure evidence proves it.
- PKG-00 contains no `Dependencies.csv`.
- Seed packets, when present, are labeled seed evidence and not active SCOPE_CHANGE intake.

## Closure Boundary

`CLOSED_BY_DEPCLOSURE` is valid only when `Case_QA.md` cites a follow-up DepClosure snapshot proving the SCC is absent or otherwise formally accepted by the owning reconciliation workflow.

