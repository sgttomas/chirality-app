
## RV — scope-of-work REVISE under SCA-V4-001 (four groups; one deliverable per brief)

Shared fields for every brief:

- **PURPOSE:** one PROJECT/SOFTWARE REVISE operation.
- **MODE:** REVISE, closing with VERIFY.
- **SOURCE_STATE:** the deliverable's current `_STATUS.md` state.
- **AMENDMENT_REF:** SCA-V4-001; snapshot
  `execution/_ScopeChange/SCA-V4-001_2026-09-28_2155/` (group 3 accepted,
  DECISION-8); the action row naming the deliverable in `Amendment_Actions.csv`
  (sha256 `069645d9…`).
- **REVISION_SCOPE:** exactly the E-blocks for that deliverable in
  `AMENDMENT_PACKET/SOW_REVISIONS.md` (sha256 `9b4d700d…`, bound by the
  group-2 manifest).
- **PRIOR_CONTRACT_SHA256:** computed at dispatch, and it must equal the hash
  that SOW_REVISIONS records.
- **STATUS_POLICY:** PRESERVE_CURRENT. Frontmatter is unchanged (O-22).
- **Write target:** that deliverable's `ScopeOfWork.md` only.
- **Git:** read-only. No network.

Groups:

| Group | Deliverables |
|---|---|
| RV-1 | DEL-04-01, DEL-04-02, DEL-04-03, DEL-01-01 |
| RV-2 | DEL-02-01, DEL-02-03, DEL-05-01, DEL-05-02 |
| RV-3 | DEL-03-01, DEL-03-02, DEL-03-03, DEL-03-04 |
| RV-4 | DEL-09-06, DEL-09-07, DEL-09-09, DEL-08-01 |
