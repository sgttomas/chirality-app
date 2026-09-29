# Group-1 handoff — SCA-V4-001

**Decision.** Checkpoint group 1 is accepted, as recorded in `DECISION.md`
and `ACCEPTED_MANIFEST.csv` (owner act 2026-09-28, DECISION-7: "accept the
remaining items as recommended"). The accepted change is the 47-action
`MODIFY` set of IMPACT_ASSESSMENT revision 2, with O-8 and O-17 included.

**Next owning stage.** Group-2 preparation would consume this snapshot. The
same owner act accepted group 2, recorded in
`../SCA-V4-001_GROUP-2_2026-09-28/`; the execution stage consumes that
snapshot.

**Status of later stages.**

| Stage | State |
|---|---|
| Exact amendment and propagation decision | Accepted by the same act (group-2 snapshot) |
| Canonical application | Not started at this record |
| Current basis | `_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z` (accepted decomposition) with the working package at `f4ba34c2c` |
| Pointer posture for group 3 | `FIRST_AMENDMENT` (`_LATEST.md` absent) |

**State fields (at this record).**

| Field | Value |
|---|---|
| `DecompositionTruthState` | `NOT_STARTED` |
| `DerivativePackageState` | `INCOMPLETE` |
| `ContentRemediationState` | `NOT_REQUIRED` |
| `DownstreamRerunState` | `FROZEN` |
| `MetadataAlignmentState` | `NOT_REQUIRED` |
| `AuditState` | `NOT_RUN` (post-change) |
| `AdjustedAuditState` | `NOT_RUN` |
| `ReadyForNextPhase` | `NOT_APPLICABLE` |

**Remains unauthorized by group 1 alone:** any write to the docs,
decomposition package, `_CONTEXT.md`, `ScopeOfWork.md`, `_STATUS.md`,
`Dependencies.csv`, `_DEPENDENCIES.md` or `_DAG`; `_LATEST.md`.

Reopen only on a material departure from the accepted impact assessment.
