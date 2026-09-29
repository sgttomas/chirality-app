# Group-3 handoff — SCA-V4-001

**Decision.** Checkpoint group 3 is accepted, as recorded in `DECISION.md` and
`ACCEPTED_MANIFEST.csv`. The owner act is DECISION-8, 2026-09-29: "Accept
(Recommended)"; "Record as stale, fix later (Recommended)"; "Small follow-on
amendment (Recommended)". The acceptance covers:
- the candidate at `230bf1e64`, with `Handoff_State.md` and `RUN_SUMMARY.md`
  at `9ae24fc0f`;
- the acceptance-conditional list H-1…H-5 in that `Handoff_State.md`.

There is no group-3 correction.

**Next steps, in order.** Each is performed exactly as listed:
1. this folder;
2. H-1 (A07), H-2 (A17a–c) and H-3 (D-15), applied from `BASIS_AMENDMENT.md`.
   The tokens are `{AMENDMENT_ID}` = `SCA-V4-001`, `{ACCEPT_DATE}` =
   `2026-09-29` and `{AMENDMENT_SNAPSHOT}` = `SCA-V4-001_2026-09-28_2155`.
   Each filled "old" block must match exactly once;
3. H-4, the second B8 recompute of `Consolidated_Coverage.csv`. SHA256,
   ReadSnapshot and SourceLine are recomputed; `Standing` already carries
   "amended by SCA-V4-001";
4. finalizing `SCA-V4-001_2026-09-28_2155/` as the accepted snapshot, which
   updates its `Handoff_State.md`, `RUN_SUMMARY.md` and `Decision_Log.md`.
   Its group-1 and group-2 bound files are not rewritten. Then
   `_ScopeChange/_LATEST.md`;
5. H-5, the append-only record
   `_ScopeChange/_PostAcceptanceValidation/SCA-V4-001_{UTC}/`, with the
   audit-decomp rerun over PKG-01, 02, 03, 04, 05, 08 and 09 written to the
   run folder's `POSTACCEPT/`.

**Active snapshot after the pointer move.**
`execution/_ScopeChange/SCA-V4-001_2026-09-28_2155/`. Its `Handoff_State.md`
carries:
- the post-acceptance state fields;
- the derivative-package table;
- the closure verdict;
- the residuals.

**State fields after application.**

| Field | Value |
|---|---|
| `DecompositionTruthState` | `COMPLETE` (after H-1…H-4) |
| `DerivativePackageState` | `INCOMPLETE` (Coverage_Telemetry.json `STALE_REBUILD_REQUIRED`) |
| `ContentRemediationState` | `NOT_REQUIRED` |
| `DownstreamRerunState` | `IN_PROGRESS` (propagation authorized by DECISION-8; no rerun has completed) |
| `MetadataAlignmentState` | `NOT_REQUIRED` |
| `AuditState` | as recorded by H-5 |
| `AdjustedAuditState` | as recorded by H-5 |
| `ReadyForNextPhase` | `NOT_APPLICABLE` |

**Closure verdict:** `OPEN_PENDING_DERIVATIVE_CLOSURE`.

**Next owning workflows:**
1. `project-setup` in `INCREMENTAL` mode, which routes `scope-of-work`
   MODE=REVISE for the 16 SoWs, one deliverable per brief, each closing with
   MODE=VERIFY;
2. `dependency-extract` per deliverable, for the register rows;
3. `project-dag`: the DAG-001 currency audit, then the DAG-002 candidate for
   owner checkpoint C;
4. the decomposition owner, for `Coverage_Telemetry.json`;
5. `audit-scope-closure`, as the post-acceptance closure check;
6. SCA-V4-002 (`scope-change`), after SCA-V4-001 closes.

**Still unauthorized:**
- any edit not on the acceptance-conditional list;
- `Coverage_Telemetry.json` under SCA-V4-001;
- DEL-10-03 REQ-005 under SCA-V4-001;
- lifecycle or `_STATUS.md` changes;
- DAG-002 acceptance;
- release.
