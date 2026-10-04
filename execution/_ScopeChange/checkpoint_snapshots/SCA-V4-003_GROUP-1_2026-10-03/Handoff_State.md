# Group-1 handoff — SCA-V4-003

**Decision.** Checkpoint group 1 is accepted, as recorded in `DECISION.md`
and `ACCEPTED_MANIFEST.csv` (owner act 2026-10-03, DECISION-1 of run
`APP-V4-SCA003-20261002`: "accept the remaining items as recommended"). The
accepted change is the 191 INCLUDE rows of `LEDGER.csv` (sha256
`e28661cd…5f12`), all `MODIFY`, with Q-1, Q-2, Q-4 to Q-12 and Q-14 to Q-17 as
recommended.

**Outside the amendment.** Q-13 (six deliverables INITIALIZED →
IN_PROGRESS) was accepted as a separate act and recorded by HELP_HUMAN at
`baa6e618d7`. It is not an amendment action and is not bound here.

**Next owning stage.** Group-2 preparation would consume this snapshot. The
same owner act accepted group 2, recorded in
`../SCA-V4-003_GROUP-2_2026-10-03/`; the execution stage (AK1 stage 2)
consumes that snapshot. The SCA-V4-002 effective-state note (BASIS_AMENDMENT
C-02, with V23b's n-1 correction already in the packet bytes) is written
after this snapshot is committed.

**Status of later stages.**

| Stage | State |
|---|---|
| Exact amendment and propagation decision | Accepted by the same act (group-2 snapshot) |
| SCA-V4-002 effective-state note (C-02) | Not written at this record |
| Canonical application | Not started at this record |
| Current basis | GROUP3 (`_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z`) as amended by SCA-V4-001 and SCA-V4-002; working package at `7fea17baaf` |
| Pointer posture for group 3 | `ACCEPTED_PREDECESSOR`; `_ScopeChange/_LATEST.md` names `SCA-V4-002_2026-09-29_1901` and is not moved |
| Accepted predecessor's closure | `OPEN_PENDING_DERIVATIVE_CLOSURE` (derivatives only; IMPACT_ASSESSMENT §9) |

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

**Remains unauthorized by group 1 alone:** any write to a basis document,
the decomposition package (including `Open_Issues.csv`), any `ScopeOfWork.md`,
`_CONTEXT.md`, `_STATUS.md`, `Dependencies.csv`, `_DEPENDENCIES.md` or `_DAG`
file; any move of `_LATEST.md`.

**Pointer.** `_ScopeChange/SCA-V4-003_GROUP-1_AUTHORIZED.md` is to be written
after this snapshot is complete (method, part A). It lies outside AK1's
write fence; HELP_HUMAN writes it or authorizes it.

**Commit sequence (Q-16).** This snapshot is to be committed before the next
stage uses it. AK1 has read-only git and makes no commit; HELP_HUMAN commits.

Reopen only on a material departure from the accepted impact assessment or
ledger.
