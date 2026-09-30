# SCA-V4-001 — effective state

**Record written:** 20260930T010520Z, by node AK1 (a Type 2 TASK, Claude Code subagent;
no delegation) of run `APP-V4-SCA002-20260929`, at `HEAD`
`39c97257ba5c354cff31f14487c05b538e806197`.

**Authority.** Owner DECISION-2 of run `APP-V4-SCA002-20260929`
(2026-09-29, "accept the remaining items as recommended"), item Q-13
(ASC-ISS-003), recorded in
`../../checkpoint_snapshots/SCA-V4-002_GROUP-1_2026-09-29/`. The text of the
proposal is BASIS_AMENDMENT C-02 (sha256 `091871fd…4238`).

**What this record is.** It is an append-only statement of where SCA-V4-001's
downstream work stands now. It edits no SCA-V4-001 byte. It names no new
pointer and no different active snapshot: `_ScopeChange/_LATEST.md` (sha256
`a9a7cdc8c50a36fbdd25fc53c72322972ba4f9b4d301d811e1a9c1381966339d`) still
names `SCA-V4-001_2026-09-28_2155`. It accepts nothing, and makes no release,
publication or reliance claim.

## Why it is needed (ASC-ISS-003)

Three SCA-V4-001 records list as open work that is now complete:
`_ScopeChange/_LATEST.md`, `SCA-V4-001_2026-09-28_2155/Handoff_State.md` and
`SCA-V4-001_2026-09-28_2155/RUN_SUMMARY.md`. They understate progress; they
do not over-claim. Their bytes are group-bound or are the active pointer, so
they are not edited. Read them together with this record.

## Complete

| Item | Evidence |
|---|---|
| The 16 ScopeOfWork REVISEs (register rows 32–47) | Applied at commit `340ecf341` ("16 ScopeOfWork contracts revised under SCA-V4-001 (scope-of-work REVISE + VERIFY)"; 16 `ScopeOfWork.md` files). The closure and currency audits over them are at commit `e9dc4633b`, which is the commit BASIS_AMENDMENT C-02 cites |
| The 18 dependency registers | Refreshed at commit `b585e5ebe` ("dependency registers refreshed for 18 deliverables (dependency-extract UPDATE)"; 18 `Dependencies.csv` files) |
| DAG-002 | Accepted by the owner on 2026-09-29 (`APP-V4-BASIS-ALIGN-20260928` DECISION-10, commit `87813431d`); published and current at commit `6dca88de7`. `_DAG/_LATEST.md` reads `Latest: DAG-002`; the record is `_DAG/DAG-002/ACCEPTANCE_RECORD.md` |
| Incremental setup for SCA-V4-001 | `_Coordination/SETUP_LOG.md`, line 6: "INCREMENTAL SCA-V4-001 setup COMPLETE" |
| The closure audit | CA1, `_Evaluation/ScopeClosureAudit/ScopeClosure_SCA-V4-001_2026-09-29_1222/` (commit `f5b5d0ad0`): 47 of 47 actions verified; 4 of 6 recommended downstream reruns completed, 2 deferred |

## Open

| Item | State | Where it goes |
|---|---|---|
| `_Decomposition/Coverage_Telemetry.json` | `STALE_REBUILD_REQUIRED`, deferred by the owner (`APP-V4-BASIS-ALIGN-20260928` DECISION-8, answer 2); sha256 `178ec20abeddfb55e558869f0b33157106f7da95b71b804fda80a302a5f2f620`, unchanged (ASC-ISS-004) | Rebuilt once, after SCA-V4-002, by the decomposition owner's bounded brief |
| The 17 Design re-pins | `STALE_REBUILD_REQUIRED`. The owner confirmed (DECISION-2, Q-15) that DECISION-8 is the record that deferred them (ASC-ISS-005) | Re-pinned at the next design pass, after SCA-V4-002's REVISEs, GUIDE (DEL-03-04) last |
| ASC-ISS-001: eleven SCA-V4-001 actions (18–25, 36, 42 and 46) have supersession bindings only in the Notes of other rows | **Ruled by the owner: option (a)** (DECISION-2, Q-10). SCA-V4-002's `Supersession_Delta.csv` adds 17 path-level `DL-SCA-V4-001-…` rows, and its `Supersession_Map.csv` is accumulated from SCA-V4-001's map. SCA-V4-001's delta, map and register are not rewritten | The rows take effect when SCA-V4-002 is accepted at checkpoint group 3. Until then this item stays open. A later `audit-scope-closure` run decides whether it closes |

Other CA1 findings and their routes (none blocks this record): ASC-ISS-002
and ASC-ISS-006 are SCA-V4-002 edits (B-05, B-06); ASC-ISS-007, 008 and 009
are SCA-V4-002 propagation-plan items.

## Closure verdict

**`OPEN_PENDING_DERIVATIVE_CLOSURE`.**

This is SCA-V4-001's verdict as its accepted `Handoff_State.md` records it,
and it is unchanged. The CA1 audit's status is `OPEN`
(`scope_closure_summary.json` sha256
`1093cf2162ee838102361ba602711aadfaef310fc26f6f9557f692d4be8f0dd4`;
`Scope_Closure_Report.md` `50b6e0437694844f5e23b38434096a7aee24d9b531749d974163ac59e4203e76`;
`Scope_Closure_IssueLog.csv` `9fbfaa310c37615da57377349cbee525a20351c60f5f3b707537a870be42b973`),
with ASC-ISS-001 as its one determinant. This record does not change either
verdict.

## State fields, as they stand now

These restate SCA-V4-001's `Handoff_State.md` fields for the present state.
The accepted file is not edited.

| Field | In the accepted `Handoff_State.md` | Effective now | Reason |
|---|---|---|---|
| `DecompositionTruthState` | `COMPLETE` | `COMPLETE` | unchanged |
| `DerivativePackageState` | `INCOMPLETE` | `INCOMPLETE` | `Coverage_Telemetry.json` and the Design re-pins are open |
| `ContentRemediationState` | `NOT_REQUIRED` | `NOT_REQUIRED` | SOFTWARE variant |
| `DownstreamRerunState` | `IN_PROGRESS` | `IN_PROGRESS` | the REVISEs, the registers and DAG-002 are complete; two reruns are deferred by the owner |
| `MetadataAlignmentState` | `NOT_REQUIRED` | `NOT_REQUIRED` | unchanged |
| `AuditState` | `WARNINGS` | `WARNINGS` | SCA-V4-002 pre-change baseline: 0 BLOCKER, 38 WARNING, 101 INFO |
| `ReadyForNextPhase` | `NOT_APPLICABLE` | `NOT_APPLICABLE` | SOFTWARE variant |

## Use at the SCA-V4-002 pointer move

BASIS_AMENDMENT C-01 (acceptance-conditional; not applied) cites this record
when `_ScopeChange/_LATEST.md` is rewritten after SCA-V4-002's group-3
acceptance: in `{SCA001_CLOSURE}` and in `{OPEN_LIST}`.

## Bytes this record relies on and leaves unchanged

| File | sha256 |
|---|---|
| `_ScopeChange/_LATEST.md` | `a9a7cdc8c50a36fbdd25fc53c72322972ba4f9b4d301d811e1a9c1381966339d` |
| `_ScopeChange/SCA-V4-001_2026-09-28_2155/Handoff_State.md` | `ef587eddd15deea6ee22f0800f2efc7dfb6209e193a16ffae2f0284987a1ef79` |
| `_ScopeChange/SCA-V4-001_2026-09-28_2155/RUN_SUMMARY.md` | `851fce50b4edce9c0bcbf2ed87e5b9b8c9070e46743a57ea32f4d6f7ddd97d1e` |
| `_ScopeChange/SCA-V4-001_2026-09-28_2155/Supersession_Delta.csv` | `b64da6d38e8bb5b202f48e29c321bde7c17bd9263d29ab3f27e175cc393c59a0` |
| `_ScopeChange/SCA-V4-001_2026-09-28_2155/Supersession_Map.csv` | `e8e433208bce44faf3f65d43b31e48b1a3476d4d6afec554a4e5319d9ef1a801` |
| `_ScopeChange/SCA-V4-001_2026-09-28_2155/Amendment_Actions.csv` | `069645d979efa1e0a20f50194acca08afa8715ce647f36ad507c5bf2b76f14d2` |

## Note on the folder name

BASIS_AMENDMENT names this location in two forms: "Edits at a glance" gives
`_PostAcceptanceValidation/SCA-V4-001_{UTC}/EFFECTIVE_STATE.md`, and section
C-02 gives
`_PostAcceptanceValidation/SCA-V4-001_{UTC}_EFFECTIVE_STATE/EFFECTIVE_STATE.md`.
This record uses the form in section C-02, which is the proposal's own text.
The difference is reported to the coordinating session.
