# decomposition-package-review — QA Checks

Minimum checks for a valid run:

1. `ROOT_PATH`, `DECOMPOSITION_ROOT`, and `SCOPE_CHANGE_ROOT` exist.
2. The active snapshot was either resolved from `_LATEST.md` or explicitly
   provided, and the report says which one was used.
3. The report at `REVIEW_OUTPUT_PATH` exists and states one of:
   - `READY`
   - `READY_WITH_GAPS`
   - `BLOCKED`
4. Findings distinguish:
   - `DECOMP_LOCAL_REPAIR`
   - `SNAPSHOT_REPAIR`
   - `DOWNSTREAM_RERUN`
   - `HUMAN_DECISION_REQUIRED`
5. Every blocking or material-warning finding cites a local surface path.
6. `REVIEW_ONLY` runs modify no package-local truth.
7. `REVIEW_AND_REPAIR` runs modify only explicitly authorized files under
   `_Decomposition/` or `_ScopeChange/`.

## Blocking conditions that must surface

A run is invalid if any of these occurred but were not reported:

- active snapshot resolution failed or was ambiguous
- duplicated package-local truth surfaces materially disagree
- the active snapshot is incomplete
- `RUN_SUMMARY.md` or `Handoff_State.md` claims a phase the package evidence
  does not support
- a write target falls outside the authorized package-local paths

## Optional structured-output validation

If `FINDINGS_CSV_PATH` is provided:

- the file exists
- each row includes `Severity`, `FindingClass`, `SurfacePath`, and `Summary`

If `PARITY_MATRIX_PATH` is provided:

- the file exists
- each row includes `SurfacePath`, `ParityStatus`, and `RequiredAction`

## Success case

A clean run reports:

- the reviewed root
- the active snapshot path
- package verdict
- whether any repairs were applied
- whether downstream reruns remain

If no material issues remain, the report must say so explicitly.
