# Group-1 handoff — SCA-V4-002

**Decision.** Checkpoint group 1 is accepted, as recorded in `DECISION.md`
and `ACCEPTED_MANIFEST.csv` (owner act 2026-09-29, DECISION-2: "accept the
remaining items as recommended"). The accepted change is the 16-action
`MODIFY` set of IMPACT_ASSESSMENT revision 2, with Q-4 (all four arcs), Q-5
option A, Q-6, Q-7, Q-10 option (a), Q-11, Q-12 option (a) and Q-13.

**Timing.** The owner decided while the pre-change baseline was still
running. The baseline then completed and changed nothing in the packet; see
`DECISION.md`, "Timing disclosure". This snapshot was written after the
baseline completed and before application.

**Next owning stage.** Group-2 preparation would consume this snapshot. The
same owner act accepted group 2, recorded in
`../SCA-V4-002_GROUP-2_2026-09-29/`; the execution stage consumes that
snapshot. The SCA-V4-001 effective-state record (C-02) is written after this
snapshot.

**Status of later stages.**

| Stage | State |
|---|---|
| Exact amendment and propagation decision | Accepted by the same act (group-2 snapshot) |
| Canonical application | Not started at this record |
| Current basis | GROUP3 (`_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z`) as amended by SCA-V4-001; working package at `39c97257b` |
| Pointer posture for group 3 | `ACCEPTED_PREDECESSOR`; `_ScopeChange/_LATEST.md` names `SCA-V4-001_2026-09-28_2155` and is not moved |
| Accepted predecessor's closure | `OPEN_PENDING_DERIVATIVE_CLOSURE` (CA1 verdict OPEN) |

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
`Dependencies.csv`, `_DEPENDENCIES.md` or `_DAG`; any move of `_LATEST.md`.

**Commit sequence (Q-14).** This snapshot is to be committed before the next
stage's files. AK1 has read-only git and makes no commit; the coordinating
session commits.

Reopen only on a material departure from the accepted impact assessment.
