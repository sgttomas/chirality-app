# SCA-V4-002 — Decision log

**Standing: ACCEPTED amendment snapshot (posture `ACCEPTED_PREDECESSOR`);
checkpoint group 3 accepted by DECISION-3 on 2026-09-29.** Human decisions
are quoted exactly; execution-stage readings by nodes AK1 (before the act)
and AK2 (after it) are labeled as such and are not owner decisions.

## Human decisions

| Ref | Date | Checkpoint | Owner's words (exact) | Record |
|---|---|---|---|---|
| DIR-1 | 2026-09-29 | Direction to start | "Proposal accepted.  Proceed accordingly." | `AgentRuns/APP-V4-SCA002-20260929/OWNER_DECISIONS.md`, "Direction to start" |
| DECISION-2 | 2026-09-29 | K1: scope-change groups 1 and 2 | "accept the remaining items as recommended" | Same file (sha256 `2a1d24c1…7cf95`), added by commit `f061cf61e`. Recorded in `checkpoint_snapshots/SCA-V4-002_GROUP-1_2026-09-29/` and `SCA-V4-002_GROUP-2_2026-09-29/`. The owner decided while the pre-change baseline was still running (timing disclosure in the group-1 `DECISION.md`) |
| DECISION-3 | 2026-09-29 | K2: scope-change group 3 | "Accept (Recommended)" | Same file (sha256 `f2dda563…8ef3`), added by commit `851ec3d88`. Recorded in `checkpoint_snapshots/SCA-V4-002_GROUP-3_2026-09-29/`. The package presented was this candidate at `70376aff2` with its records at `ffdb56e1a` and review V14; the six-versus-seven-package audit scope (V14 R-3) was disclosed in the question |

Decision-log reference for the Part D supersession rows (Q-10): the 17
`DL-SCA-V4-001-…` rows in `Supersession_Delta.csv` bind no SCA-V4-002
register row. Their decision reference is DECISION-2, item Q-10, option (a),
as the owner accepted it ("accept the remaining items as recommended" over
OWNER_ITEMS Q-10 "(a): add 17 path-level rows now").

## Execution-stage records (node AK1, after DECISION-2)

- **E-1 · Order of writing.** Group-1 files (`Brief.md`,
  `Intake_Actions.csv`, `Impact_Assessment.md`, `Pre_Change_Coverage.json`)
  and the group-1 decision snapshot; then the SCA-V4-001 effective-state
  record (C-02); then the group-2 files (`Amendment_Actions.csv`,
  `Supersession_Delta.csv`, `Amendment_Preview.md`, `Propagation_Plan.md`)
  and the group-2 decision snapshot; then the application. No group-bound
  file describes a post-application state (V11 F3 lesson). AK1 has read-only
  git; the coordinating session commits each snapshot before the next
  stage's files (Q-14), for which the file lists are in the return.
- **E-2 · Applied** (`Evidence/Application/apply_sca002.py`,
  `apply_log.json`; a dry run to scratch first produced identical bytes):
  A-01 (result sha256 `d4331c39…`, git blob `f4a5281e…`, both equal to the
  packet's stated result); B-02 (OI-012 `Consequence`, whole field; `Status`
  OPEN); B-05a (`Deliverables.csv` DEL-04-01 `Description`, substring once);
  B-05b (DEL-04-01 `_CONTEXT.md` line 13, the same substring once; the
  `- **Description:**` bullet equals the CSV field before and after); B-06b
  (`_Decomposition/_LATEST.md`); B-06c (five `_CONTEXT.md` line 3). Every
  "old" block or value matched exactly once and its "new" text zero times
  before and once after; every target equalled its blob at `39c97257b`
  before the edit. The CSV writer reproduced each CSV target byte for byte
  before editing (CRLF, quoting).
- **E-3 · B-01 recompute.** The 31 HOST_INTEGRATION rows of
  `Consolidated_Coverage.csv` take SHA256 `d4331c39…`, `ReadSnapshot`
  `git-blob:f4a5281e…` and `SourceLine` n + 1 (all n ≥ 40), by the SCA-V4-001
  B8 rule (its Decision_Log E-4); the script checked each ID is on its new
  line. No other column or row changed; `Standing` untouched. 31/31.
- **E-4 · Held, not applied.** B-04 (`SOFTWARE_DECOMP.md` Decision Log
  entry; carries `{ACCEPT_DATE}` and `{AMENDMENT_SNAPSHOT}`): its old block
  occurs once in the candidate. C-01 (`_ScopeChange/_LATEST.md`): untouched
  (sha256 `a9a7cdc8…`). B-06a (`_LATEST_ACCEPTED.md`): untouched (sha256
  `d5d873b3…`); the packet times it with the SoW REVISEs because DAG-002's
  source manifest binds it; its old block occurs once. B-03: no edit (Q-5
  option A).
- **E-5 · Register and delta bytes.** `Amendment_Actions.csv` is the
  IMPACT_ASSESSMENT §3.2 block with `{AMENDMENT_ID}` filled (sha256
  `158702bf…`); the packet's draft hash `dafa622e…` is reproduced by the
  unfilled block. `Supersession_Delta.csv` is the Part D block with both
  tokens filled (sha256 `8c3f1a55…`); the draft hash `a14c4dd1…` likewise.
  `Intake_Actions.csv` is the same 16 rows with `ScopeChanging` blank and
  `Status` `PROPOSED`.
- **E-6 · Supersession map.** `tools/coordination/accumulate_supersession_map.py
  --prior-map SCA-V4-001_2026-09-28_2155/Supersession_Map.csv --delta
  Supersession_Delta.csv --output-map Supersession_Map.csv`: 29 rows (11 +
  18), 0 findings; `--check-map` passes. Each of the 18 superseded facts is a
  substring of a GROUP3 canonical field; each replacement is a substring of
  the current working field (D-014 after B-05a); no superseded fact remains
  in the working file.
- **E-7 · C-02 location.** BASIS_AMENDMENT gives the effective-state
  record's folder in two forms ("Edits at a glance": `SCA-V4-001_{UTC}/`;
  section C-02: `SCA-V4-001_{UTC}_EFFECTIVE_STATE/`). The section C-02 form
  was used: `_PostAcceptanceValidation/SCA-V4-001_20260930T010520Z_EFFECTIVE_STATE/EFFECTIVE_STATE.md`.
  The record also notes that C-02 cites `e9dc4633b` for the 16 REVISEs,
  while git shows the REVISE application at `340ecf341` and the registers at
  `b585e5ebe`, with `e9dc4633b` carrying the closure and currency audits over
  them. Both are reported for the dispatcher.
- **E-8 · Post-change audit.** `AgentRuns/APP-V4-SCA002-20260929/POSTCHANGE/`,
  same scope and byte-identical script as the baseline: 0 BLOCKER, 39
  WARNING, 101 INFO. `COMPARISON.md` attributes every difference. The one new
  WARNING (COV-139) is this candidate folder, which the unchanged script
  labels "historical residue" because `Handoff_State.md` and
  `RUN_SUMMARY.md` are not yet written; they follow the independent review.
  `Post_Change_Coverage.json` is the byte-identical copy of that run's
  `coverage_summary.json`. No new Check 5 finding; the DEL-04-01 mirror is
  exact.
- **E-9 · DAG-002 currency.** `shasum -a 256 -c
  _DAG/DAG-002/SOURCE_MANIFEST.sha256`: 130/130 OK after the application
  (`Evidence/Application/DAG_CURRENCY.txt`). No bound file was touched; no
  `_CONTEXT.md` is bound.
- **E-10 · Not touched.** No `ScopeOfWork.md`, `Dependencies.csv`,
  `_DEPENDENCIES.md`, `_DAG`, `_STATUS.md` or `Coverage_Telemetry.json`
  byte; `_ScopeChange/_LATEST.md` unchanged; no accepted-state marker.
- **E-11 · Baseline scope note.** IMPACT_ASSESSMENT §4 names six packages;
  the baseline and this audit use seven (PKG-05 for row 16). The packet
  bytes are not changed; the group-1 `DECISION.md` records it.
- **E-12 · Not yet written (group-3 preparation, after the independent
  review):** `Handoff_State.md` and `RUN_SUMMARY.md`.

## Execution-stage records (node AK2, after DECISION-3)

- **E-13 · Group-3 decision snapshot.**
  `checkpoint_snapshots/SCA-V4-002_GROUP-3_2026-09-29/` (`DECISION.md`,
  `ACCEPTED_MANIFEST.csv` with 61 rows hashed at `851ec3d88`,
  `Handoff_State.md`), transcribed from DECISION-3.
- **E-14 · H-1 applied** (B-04): `{ACCEPT_DATE}` = `2026-09-29`,
  `{AMENDMENT_SNAPSHOT}` = `SCA-V4-002_2026-09-29_1901`; the five clause
  slots filled because DECISION-2 declined no item (Q-6, Q-7, Q-10 (a),
  Q-11, Q-12 (a)); Q-5 option A appends nothing. The old block occurred once;
  the new block zero times before and once after. `SOFTWARE_DECOMP.md`
  sha256 `7434058164…5747` → `ea3388bcb0…9dd5`.
- **E-15 · H-2 applied** (C-01): `_ScopeChange/_LATEST.md` rewritten from
  the Part C text with `{CLOSURE_VERDICT}` = `OPEN_PENDING_DERIVATIVE_CLOSURE`,
  `{GROUP12_REFS}` = the two decision folders, `{SCA001_CLOSURE}` =
  `OPEN_PENDING_DERIVATIVE_CLOSURE` per the C-02 record at its committed
  path (V14 R-1), `{ARC_LIST}` = N-18, N-21, N-24 and X-1, `{OPEN_LIST}` =
  the open items of `Handoff_State.md` including the SCA-V4-001 items, and
  `{UTC}` = `20260930T021014Z`. sha256 `a9a7cdc8…339d` → `2b7938bc…0c2e1`.
  The registered parser `_latest_pointer_target` returns
  `SCA-V4-002_2026-09-29_1901`; `_pointer_matches` is True.
- **E-16 · H-3.** The B8 rule recomputed over all 144
  `Consolidated_Coverage.csv` rows against the post-H-1 documents changes no
  row; the register carries no `SOFTWARE_DECOMP.md` row. The file is
  unchanged (sha256 `36677365…13ea`).
- **E-17 · Finalized after the act:** this file, `Handoff_State.md` and
  `RUN_SUMMARY.md`. No group-1- or group-2-bound byte was rewritten.
- **E-18 · H-4.** The post-acceptance record
  `_PostAcceptanceValidation/SCA-V4-002_20260930T021014Z/` and the
  audit-decomp rerun `AgentRuns/APP-V4-SCA002-20260929/POSTACCEPT/` over the
  seven packages; results in those records.
- **E-19 · ASC-ISS-001** is closed by DECISION-3, pending the superseding
  `audit-scope-closure` snapshot for SCA-V4-001.
- **E-20 · Not written under this acceptance:** the 9 `ScopeOfWork.md`
  files (propagation stage 1, `scope-of-work` REVISE), B-06a (with them),
  any `Dependencies.csv`, `_DEPENDENCIES.md`, `_DAG/`, `_STATUS.md` or
  `Coverage_Telemetry.json` byte.
