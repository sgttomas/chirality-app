
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
  **Correction (integrator, after return):** the workflow's brief schema
  admits only `NO_STATUS_TOUCH` for REVISE. All four groups treated it that
  way: no `_STATUS.md` was written.
- **Write target:** that deliverable's `ScopeOfWork.md` only.
- **Git:** read-only. No network.

Groups:

| Group | Deliverables |
|---|---|
| RV-1 | DEL-04-01, DEL-04-02, DEL-04-03, DEL-01-01 |
| RV-2 | DEL-02-01, DEL-02-03, DEL-05-01, DEL-05-02 |
| RV-3 | DEL-03-01, DEL-03-02, DEL-03-03, DEL-03-04 |
| RV-4 | DEL-09-06, DEL-09-07, DEL-09-09, DEL-08-01 |

## DX — dependency-extract UPDATE for 18 deliverables (three groups; one deliverable per brief)

Shared runtime overrides:

- `SCOPE`: one deliverable ID per brief.
- `MODE`: UPDATE.
- `STRICTNESS`: CONSERVATIVE.
- **`SOURCE_DOCS`: `ScopeOfWork.md` only (explicit).** The `Design/` DRAFT
  files are **not** extraction sources. This follows `_COORDINATION.md`:
  "Agent-proposed candidates derive from local SoWs and accepted interfaces".
  Node P2 also found that extracting from Design would pull DEL-04-01 or
  DEL-09-06 into SCC-002.
- `ANCHOR_DOC`: ScopeOfWork.md.
- `DECOMPOSITION_PATH`: `execution/_Decomposition/SOFTWARE_DECOMP.md`.

**Guard.** The pointers in DEL-05-01 TBD-003, DEL-05-02 TBD-003 and DEL-09-09
CLM-004 to DEL-09-06's relay file are stated as "a coordination route, not an
input this deliverable consumes". Do not extract them as an input or
prerequisite on DEL-09-06.

**Write scope:** that deliverable's `Dependencies.csv`, `_DEPENDENCIES.md` and
`_run_records/`.

**After extraction** (a coordinator check, not an extraction input): compare
the resulting ACTIVE rows with `DAG_PREP/proposed_rows/<DEL>.csv` and
REGISTER_CHANGES.md. Report every row that was expected and not produced, and
every row that was produced and not expected.

Groups:

| Group | Deliverables |
|---|---|
| DX-1 | DEL-04-01, DEL-04-02, DEL-04-03, DEL-01-01, DEL-01-04, DEL-02-02 |
| DX-2 | DEL-02-01, DEL-02-03, DEL-05-01, DEL-05-02, DEL-03-01, DEL-03-02 |
| DX-3 | DEL-03-03, DEL-03-04, DEL-09-06, DEL-09-07, DEL-09-09, DEL-08-01 |

### DX guard wording, as first dispatched to DX-3, and the ruling (V12 F7)

**Dispatched:** "DEL-09-06 must not gain rows that consume any SCC-002
member (DEL-09-06 stays outside SCC-002)."

**Integrator ruling (on DX-3's stop):** the intended guard is that no row
makes an SCC-002 member depend on DEL-09-06, and that DEL-09-06 has no
DOWNSTREAM row to an SCC-002 member. DEL-09-06 consuming SCC-002 members is
allowed: those are arcs N-19, N-C1…N-C4 and N-08, in the accepted set.
