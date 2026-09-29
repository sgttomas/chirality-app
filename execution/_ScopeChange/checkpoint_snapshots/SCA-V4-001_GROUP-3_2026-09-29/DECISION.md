# SCA-V4-001 checkpoint group 3 — accepted audited poststate

Recorded 2026-09-29 by node AK2, a Type 2 TASK (Claude Code subagent; no
delegation) dispatched by the HELP_HUMAN integrator of run
`APP-V4-BASIS-ALIGN-20260928`, which presented checkpoint B to the owner.
This record transcribes the owner's act as it is recorded in the run's
`OWNER_DECISIONS.md`. It is not a new request for the same decision, and it
claims no inspection the owner did not perform.

## Custody of the act

| Item | Value |
|---|---|
| Record | `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-BASIS-ALIGN-20260928/OWNER_DECISIONS.md`, section "Checkpoint B: scope-change group 3 (owner, exact, 2026-09-29), DECISION-8" |
| Record sha256 at transcription | `752876c16f7f96ef5d63609d995596f1ac838152b561bc7b9c0b2aa6e3ddea10`. The working-tree file and the blob at `3d006a909` give the same hash |
| Commit that added DECISION-8 | `3d006a909d722606b2f69f8c71a7020e5c86a619` ("docs(app-v4): checkpoint B — SCA-V4-001 group 3 accepted (DECISION-8)", 2026-09-29 07:25:55 -0600). It changes only that file |
| Channel | As the record states, these are the owner's answers to a structured question in the active chat, transcribed by the recorder. AK2 did not observe the chat and relies on that record |
| Earlier acts in this amendment | DECISION-7 (groups 1 and 2), recorded in `../SCA-V4-001_GROUP-1_2026-09-28/` and `../SCA-V4-001_GROUP-2_2026-09-28/` |

## What the owner had in front of them

As recorded in DECISION-8 "Custody":
- the candidate at `230bf1e64`;
- `Handoff_State.md` and `RUN_SUMMARY.md` at `9ae24fc0f`;
- review V11, with the verdict READY FOR GROUP 3.

The commit `9ae24fc0f` → `3d006a909` changes only `OWNER_DECISIONS.md`, so
every presented file has its presented bytes at `3d006a909`.
`ACCEPTED_MANIFEST.csv` binds those bytes.

The presented `Handoff_State.md` (sha256 `17713b07…7e2c`) contains:
- the exact acceptance-conditional list H-1…H-5;
- the derivative-package table and the closure verdict
  `OPEN_PENDING_DERIVATIVE_CLOSURE`;
- the crosswalk for the action IDs;
- the residuals;
- the process disclosure (V11 F3).

The presented `RUN_SUMMARY.md` is sha256 `bdcd5ac4…d9efd5`.

## The owner's act (verbatim)

| Question presented | Owner's answer (exact label) |
|---|---|
| Checkpoint B (scope-change group 3 for SCA-V4-001): accept the applied, audited result? | "Accept (Recommended)" |
| Coverage_Telemetry.json goes stale; no writer: how to handle? | "Record as stale, fix later (Recommended)" |
| "local-first" outside this amendment (DEL-10-03 REQ-005; the SWBPIPE handoff note)? | "Small follow-on amendment (Recommended)" |

No correction or exception was recorded. The owner offered no correction to
the D-15 wording (V11 F7).

## Interpretation (recording role's reading, not owner text)

| Item | Effect |
|---|---|
| Audited poststate | The candidate at `230bf1e64` is accepted as presented. That covers the Part A and Part B edits, the B7 mirrors, the first B8 recompute, the supersession map and the post-change audit. So are its closure verdict `OPEN_PENDING_DERIVATIVE_CLOSURE` and its explicitly open downstream obligations |
| Acceptance-conditional list | H-1 (A07, three pairs), H-2 (A17a–c) and H-3 (D-15) are applied exactly, from `BASIS_AMENDMENT.md` (sha256 `04bdc916…24cf`). The tokens are `{AMENDMENT_ID}` = `SCA-V4-001`, `{ACCEPT_DATE}` = `2026-09-29` (DECISION-8 "Effects") and `{AMENDMENT_SNAPSHOT}` = `SCA-V4-001_2026-09-28_2155`. H-4 is the second B8 recompute of `Consolidated_Coverage.csv`. H-5 is the post-acceptance record under `_ScopeChange/_PostAcceptanceValidation/`, with an audit-decomp rerun over the seven packages. D-15 is applied verbatim, including "where accepted" (V11 F7) |
| Accepted amendment snapshot | The candidate folder `_ScopeChange/SCA-V4-001_2026-09-28_2155/`, already in the contract's form `SCA-{NNN}_{YYYY-MM-DD}_{HHMM}`, is finalized as the immutable accepted snapshot. `_ScopeChange/_LATEST.md` is created and names it. Its group-1 and group-2 bound files are not rewritten. Only its unbound status records are updated after this act: `Handoff_State.md`, `RUN_SUMMARY.md` and `Decision_Log.md` |
| Supersession | The 11 `Supersession_Delta.csv` bindings take effect when `_LATEST.md` names this snapshot, through the accumulated `Supersession_Map.csv` (sha256 `e8e43320…a801`) |
| Coverage_Telemetry.json (answer 2) | `STALE_REBUILD_REQUIRED`, owned by the decomposition owner, and fixed later by a bounded brief that names the writer and the exact bytes. The group-2 write boundary is not extended, and the file is not written under SCA-V4-001. The closure verdict stays `OPEN_PENDING_DERIVATIVE_CLOSURE` |
| "local-first" residuals (answer 3) | A follow-on amendment, SCA-V4-002, follows after SCA-V4-001 closes, for DEL-10-03 `ScopeOfWork.md` REQ-005. The `_Coordination/HANDOFF_SWBPIPE_DOMAINS.md` l.22 note is carried with the next relay to SWBPIPE. Neither is edited under SCA-V4-001 |
| Other residuals | `Allocation_Rationale.csv` stays NO_CHANGE (historical). The zsh note on `tools/query/scan_next_amendment_id.sh` is a tooling observation. Any fix would need separately authorized Root tooling work |
| Reopening | No affected deliverable is `ISSUED` (14 IN_PROGRESS, 2 INITIALIZED; Propagation_Plan §4). This acceptance authorizes no `ISSUED → IN_PROGRESS` reopening, and no `write_status.sh --amendment` path arises |

## What this acceptance authorizes and does not authorize

It authorizes:
- this decision folder;
- H-1…H-4 exactly as listed, and the H-5 post-acceptance record;
- finalizing `SCA-V4-001_2026-09-28_2155/` as the accepted snapshot, and
  `_ScopeChange/_LATEST.md`;
- the downstream propagation recorded in DECISION-8 "Effects", each through
  its owning workflow and its own brief, in this order:
  1. `project-setup` in `INCREMENTAL` mode, which routes `scope-of-work`
     MODE=REVISE for the 16 SoWs, one deliverable per brief;
  2. then the dependency-register rows (`dependency-extract`);
  3. then the DAG-001 currency audit and the DAG-002 candidate, for owner
     checkpoint C.

It does not authorize:
- any edit not on the acceptance-conditional list;
- any write to `Coverage_Telemetry.json` under SCA-V4-001;
- any edit to DEL-10-03's `ScopeOfWork.md` or to `HANDOFF_SWBPIPE_DOMAINS.md`
  under SCA-V4-001;
- any `_STATUS.md` or lifecycle change;
- acceptance of DAG-002, which is owner checkpoint C;
- any release, publication or reliance claim.

The standing Git authorization governs commits and merges. This TASK makes
none.

## Basis

- Accepted group-1 snapshot `checkpoint_snapshots/SCA-V4-001_GROUP-1_2026-09-28/`
  (`DECISION.md` `f72b3ddc4625053a8a39f28cf6aedb730d6d0534d92420a75ca58995f8490d69`,
  `ACCEPTED_MANIFEST.csv` `1f821246558e148691181225164889bbe6c3bb34434dfd1a533d9c03ce88484a`).
- Accepted group-2 snapshot `checkpoint_snapshots/SCA-V4-001_GROUP-2_2026-09-28/`
  (`DECISION.md` `ab945602193aafe62558060197c898e62914010cfa72fcfc14a1c8a086b26103`,
  `ACCEPTED_MANIFEST.csv` `309274f89efb91d68e28495b137273b1f290a429e9e2c9e26813d10e6829af9a`).
  It binds the register `Amendment_Actions.csv` at
  `069645d979efa1e0a20f50194acca08afa8715ce647f36ad507c5bf2b76f14d2`, which is
  unchanged.
- Pointer posture `FIRST_AMENDMENT`. `_ScopeChange/_LATEST.md` is absent
  before this act, and no predecessor exists.
- Evidence base: commit `3d006a909`, working tree clean.
