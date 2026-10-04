# Group-3 handoff — SCA-V4-003

**Decision.** Checkpoint group 3 is accepted, as recorded in `DECISION.md` and
`ACCEPTED_MANIFEST.csv`. The owner's act is DECISION-2, 2026-10-03
(America/Denver): "I accept the audited result." The acceptance covers:
- the candidate applied at `fa16393978`, with its records at `388fc730b9`;
- the acceptance-time list F-1…F-4 and H-1…H-3 in the presented
  `Handoff_State.md` (sha256 `4f3f31b9…c167`);
- the propagation route in that file (Q-3).

There is no group-3 correction.

**Next steps, in order.** Each step is performed exactly as listed:
1. this folder (F-1);
2. H-1 (B-01), applied from `BASIS_AMENDMENT.md` (`151bc6ff…35bf`):
   - `{ACCEPT_DATE}` = `2026-10-03` and `{AMENDMENT_SNAPSHOT}` =
     `SCA-V4-003_2026-10-03_1827`;
   - the four clause slots take the group-2 values;
   - the old block must match exactly once;
   - expected result sha256
     `983199cc22c84398000612cd95308c840ad011d302fe31ca110a5aa97e64a70d`;
3. H-2 (C-01): `_ScopeChange/_LATEST.md` is replaced by the C-01 text, with
   these slots:
   - `{AMENDMENT_SNAPSHOT}` = `SCA-V4-003_2026-10-03_1827`;
   - `{ACCEPT_DATE}` = `2026-10-03`;
   - `{CLOSURE_VERDICT}` = `OPEN_PENDING_DERIVATIVE_CLOSURE`;
   - `{G1_DATE}` = `{G2_DATE}` = `2026-10-03`;
   - `{C02_UTC}` = `20261004T002903Z`;
   - `{UTC}` = the H-3 record's stamp.

   The registered parser must resolve it to the accepted snapshot;
4. F-2…F-4: the accepted status lines of the snapshot's `Decision_Log.md`,
   `Handoff_State.md` and `RUN_SUMMARY.md`. Its group-1 and group-2 copies
   and transcriptions are not rewritten;
5. H-3: the append-only record
   `_ScopeChange/_PostAcceptanceValidation/SCA-V4-003_{UTC}/`, with the
   audit-decomp rerun written to `RUN/POSTACCEPT/`. It uses the unchanged
   baseline script over PKG-01, 02, 03, 04, 05, 09 and 10, compared with
   the simulation (`RUN/Application/SIMULATED_POSTACCEPT.md`; 0 / 51 / 77).

**Active snapshot after the pointer move:**
`execution/_ScopeChange/SCA-V4-003_2026-10-03_1827/`.

**State fields after application** (rule):

| Field | Value |
|---|---|
| DecompositionTruthState | COMPLETE (after H-1) |
| DerivativePackageState | INCOMPLETE (REVISEs, UPDATE, DAG-004, re-pins and Coverage_Telemetry.json open) |
| ContentRemediationState | NOT_REQUIRED |
| DownstreamRerunState | IN_PROGRESS (propagation authorized by DECISION-2) |
| MetadataAlignmentState | NOT_REQUIRED |
| AuditState, AdjustedAuditState | as recorded by H-3 |
| ReadyForNextPhase | NOT_APPLICABLE |

**Closure verdict (accepted):** OPEN_PENDING_DERIVATIVE_CLOSURE.

**Propagation authorized (DECISION-2 "Effects"), in order:**
1. `scope-of-work` MODE=REVISE for the 19 deliverables, one per brief. Each
   run closes with MODE=VERIFY, uses `STATUS_POLICY` `NO_STATUS_TOUCH`, and
   carries:
   - `AMENDMENT_REF`: SCA-V4-003, the accepted snapshot, the register row
     and the register hash `9b7c2ce8…6d1c`;
   - `REVISION_SCOPE`: the deliverable's G-blocks in SOW_REVISIONS_A or _B;
   - `PRIOR_CONTRACT_SHA256`: the packet's prior hash.
2. `dependency-extract` UPDATE for the 20 registers and DEL-04-03's
   `_DEPENDENCIES.md`, with the IMPACT §10 and ARC_EFFECT §3 guards.
3. `project-dag`: the DAG-003 currency audit, then TRIGGER=SUCCESSOR for the
   DAG-004 candidate, for the owner.
4. The decomposition owner, for `Coverage_Telemetry.json` (bounded brief).
5. The App v4 design undertaking, for the re-pins (GUIDE last).
6. `audit-scope-closure`, for SCA-V4-003.

**Still unauthorized:**
- any edit not on the acceptance-time list;
- `Coverage_Telemetry.json` under SCA-V4-003;
- any lifecycle or `_STATUS.md` change;
- DAG-004 acceptance;
- release.
