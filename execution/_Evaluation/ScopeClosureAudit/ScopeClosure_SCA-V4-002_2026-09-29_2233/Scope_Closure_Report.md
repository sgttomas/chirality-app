# Scope Closure Audit — SCA-V4-002

**Audit Date:** 2026-09-29
**Closure Status:** CLOSED_WITH_OBSERVATIONS
**Amendment Date:** 2026-09-29 (groups 1–2 accepted by DECISION-2; group 3 accepted by DECISION-3, both 2026-09-29; snapshot `SCA-V4-002_2026-09-29_1901`)
**Amendment Description:** The App v4 follow-on alignment (Brief.md): 16 `MODIFY` actions, no structural change. Nine ScopeOfWork contracts (DEL-10-03 REQ-005 "local-first" aligned with DECISION-4 D4-3; the consumption sentences behind arcs N-18, N-21, N-24 and X-1; OI-001/002/012 text in DEL-09-07, DEL-01-04 and DEL-02-02; the DEL-03-03 CLM-002 tail; the DEL-04-02 and DEL-01-01 same-class corrections), the HOST_INTEGRATION line layout with the 31-row recompute, the OI-012 pointer, the Change Register entry, the DEL-04-01 checkpoint clause with its mirror, and the reading-rule notes. Topology unchanged: 11 packages, 41 deliverables, 262 scope IDs.

Evidence base: project state at `a254be16060692633600bcb5c5aab925f4d26926`. During this run `HEAD` moved to `a5a4deaa72d3c7060523393131b48b6cfd0d018c`, which changes only `_Evaluation/ScopeClosureAudit/ScopeClosure_SCA-V4-001_2026-09-29_2221/` (node CA3's snapshot) and `AgentRuns/APP-V4-SCA002-20260929/DISPATCH.md`; no audited project-state byte differs between the two commits. Audited by node CA2 (Type 2 TASK, no delegation) of run `APP-V4-SCA002-20260929`; read-only on project state. Every input read is hashed in `INPUT_MANIFEST.sha256`.

**Relation to the amendment's own verdict.** The accepted `Handoff_State.md` and `_ScopeChange/_LATEST.md` carry the scope-change verdict `OPEN_PENDING_DERIVATIVE_CLOSURE`. This audit's `CLOSED_WITH_OBSERVATIONS` is the contract's closure status: every required check is complete and no CRITICAL or MAJOR finding remains. It does not claim that the owner-deferred derivatives (Coverage_Telemetry.json, the 17 Design re-pins) are complete; they are listed as open work with their deciding records. The two vocabularies are different instruments and do not conflict.

---

## Amendment Summary

**Register resolution.** The accepted checkpoint-group-2 snapshot is `checkpoint_snapshots/SCA-V4-002_GROUP-2_2026-09-29/` (named by `_ScopeChange/SCA-V4-002_GROUP-2_AUTHORIZED.md`). Its `ACCEPTED_MANIFEST.csv` binds exactly one `Amendment_Actions*.csv` row: `SCA-V4-002_2026-09-29_1901/Amendment_Actions.csv`, role "action register", SHA-256 `158702bf610777e008e304268fcbd967756f9186ded946942430a391957c579d`. Recomputed here: equal. The group-3 manifest rebinds the same hash. `Intake_Actions.csv` (16 `PROPOSED` rows) is group-1 evidence and was not used as the register.

| Seq | Type | Entity | Description (register) | Downstream reruns (register) | Supersession | ScopeChanging |
|---|---|---|---|---|---|---|
| 1 | MODIFY | DEL-10-03 | ScopeOfWork REQ-005 "local-first" aligned with DECISION-4 D4-3 (F-1003-01..02) | project-setup(INCREMENTAL), scope-of-work(REVISE), dependency-extract(UPDATE) | NO | YES |
| 2 | MODIFY | DEL-02-01 | CLM-002 consumption sentence for arc N-18 | + project-dag(currency), project-dag(SUCCESSOR) | NO | NO |
| 3 | MODIFY | DEL-02-03 | CLM-002 consumption sentence for arcs N-21, N-24, X-1 | + project-dag(currency), project-dag(SUCCESSOR) | NO | NO |
| 4 | MODIFY | DEL-09-07 | CLM-002, TBD-002, TBD-003: OI-001/OI-002 aligned with DECISION-1 D2/D3 | REVISE, UPDATE | NO | NO |
| 5 | MODIFY | DEL-01-04 | CLM-005, VER-005, TBD-001/002/004: OI-001/002/012 aligned with D2–D4 | REVISE, UPDATE | NO | NO |
| 6 | MODIFY | DEL-02-02 | TBD-001, TBD-002: OI-001/002/012 aligned with D2–D4 | REVISE, UPDATE | NO | NO |
| 7 | MODIFY | DEL-03-03 | CLM-002 tail and REQ-005 | REVISE, UPDATE | NO | NO |
| 8 | MODIFY | DEL-04-02 | CLM-004 same-class correction (conditional Q-6) | REVISE, UPDATE | NO | NO |
| 9 | MODIFY | DEL-01-01 | Source line D4 pin (conditional Q-6) | REVISE, UPDATE | NO | NO |
| 10 | MODIFY | docs/HOST_INTEGRATION.md#status | Line layout, the A17b join (A-01) | audit-decomp | NO | NO |
| 11 | MODIFY | Consolidated_Coverage.csv | RECOMPUTE of the 31 HOST_INTEGRATION rows (B-01) | audit-decomp | NO | NO |
| 12 | MODIFY | OI-012 | Consequence pointer to DECISION-1 D4; status stays OPEN (B-02) | — | NO | NO |
| 13 | MODIFY | SOFTWARE_DECOMP.md#decision-log | Change Register entry (B-04; acceptance-conditional) | — | NO | NO |
| 14 | MODIFY | DEL-04-01 | Deliverables.csv Description checkpoint clause with `_CONTEXT.md` mirror (B-05) | audit-decomp, dependency-extract(UPDATE) | YES | NO |
| 15 | MODIFY | _Decomposition pointers#reading-rule | Reading-rule note on `_LATEST_ACCEPTED.md` (B-06a) and `_LATEST.md` (B-06b) | project-dag(currency) | NO | NO |
| 16 | MODIFY | _CONTEXT.md#accepted-basis | Reading-rule note on five `_CONTEXT.md` Accepted-basis lines (B-06c) | — | NO | NO |

**Handoff records read (Pass 0 step 7).** `SCA-V4-002_2026-09-29_1901/Handoff_State.md`, `RUN_SUMMARY.md` and `Decision_Log.md` (finalized after DECISION-3); the three checkpoint snapshots' `DECISION.md`, `ACCEPTED_MANIFEST.csv` and `Handoff_State.md`; `_PostAcceptanceValidation/SCA-V4-002_20260930T021014Z/` (47/47 PASS); the SCA-V4-001 effective-state record `_PostAcceptanceValidation/SCA-V4-001_20260930T010520Z_EFFECTIVE_STATE/EFFECTIVE_STATE.md`; `AgentRuns/APP-V4-SCA002-20260929/OWNER_DECISIONS.md` (DIR-1, DECISION-2, DECISION-3, DECISION-4) and `DISPATCH.md`; `_DAG/DAG-003/ACCEPTANCE_RECORD.md` and `HANDOFF_STATE.md`. Amendment recency is context only (folder date 2026-09-29, not in the future).

**Deciding records for deferrals** (Pass 2 uses these): `Coverage_Telemetry.json` — `APP-V4-BASIS-ALIGN-20260928` DECISION-8 answer 2 ("Record as stale, fix later"), carried by SCA-V4-002 `Handoff_State.md` ("Derivative packages") and excluded from authorization by the group-3 `DECISION.md` ("does not authorize … any write to `Coverage_Telemetry.json`"); the 17 Design re-pins — DECISION-8, confirmed as the deciding record by DECISION-2 over OWNER_ITEMS Q-15 ("accept the remaining items as recommended").

---

## Pass 1 — Action Verification

Method: each `AffectedFiles` path was hashed at `HEAD` and compared with the accepted result (the group-3 `ACCEPTED_MANIFEST.csv` for candidate edits; the post-acceptance record for H-1; the RV records for the SoWs; the B-06a block for `_LATEST_ACCEPTED.md`), and the accepted "new" text from `BASIS_AMENDMENT.md` (sha256 `091871fd…4238`, bound at group 2) was searched in the current bytes.

| Seq | Type | Entity | Expected | Actual | Status |
|---|---|---|---|---|---|
| 1 | MODIFY | DEL-10-03 | REQ-005 revised per F-1003-01/02; AX-005 added; `_STATUS.md` untouched | `ScopeOfWork.md` sha256 `31bc607d…4166` = `RV/RV_DEL-10-03.md` "Revised" hash; RV PRIOR `4e16817e…5f92` = group-3 manifest prior; VERIFY PASS; unchanged since `1efd4bcda`; `_STATUS.md` INITIALIZED, not in the 39c97257b..HEAD diff | VERIFIED |
| 2 | MODIFY | DEL-02-01 | CLM-002 sentence (N-18) per F-0201-01/02 | sha256 `ef360edf…2f17` = RV revised; prior `6ccc860b…f0dc` = manifest; VERIFY PASS | VERIFIED |
| 3 | MODIFY | DEL-02-03 | CLM-002 sentence (N-21, N-24, X-1) per F-0203-01/02 | sha256 `0006521b…726d` = RV revised; prior `a4ffcd87…c0e` = manifest; VERIFY PASS | VERIFIED |
| 4 | MODIFY | DEL-09-07 | F-0907-01..04 | sha256 `813ef0f3…395a` = RV revised; prior `53b51d30…cba0` = manifest; VERIFY PASS | VERIFIED |
| 5 | MODIFY | DEL-01-04 | F-0104-01..06 | sha256 `0cdb44e2…69cd` = RV revised; prior `7261a58f…60a` = manifest; VERIFY PASS | VERIFIED |
| 6 | MODIFY | DEL-02-02 | F-0202-01..03 | sha256 `58141169…924a` = RV revised; prior `b0a1a8a4…95ec` = manifest; VERIFY PASS | VERIFIED |
| 7 | MODIFY | DEL-03-03 | F-0303-01..03 | sha256 `93faf918…1a93` = RV revised; prior `fdd22e25…2881` = manifest; VERIFY PASS | VERIFIED |
| 8 | MODIFY | DEL-04-02 | F-0402-01/02 (Q-6 accepted) | sha256 `f16ffa8a…4460` = RV revised; prior `e077f20a…22f9` = manifest; VERIFY PASS | VERIFIED |
| 9 | MODIFY | DEL-01-01 | F-0101-01/02 (Q-6 accepted) | sha256 `9945e72b…cc75` = RV revised; prior `f65dc666…acc9` = manifest; VERIFY PASS | VERIFIED |
| 10 | MODIFY | HOST_INTEGRATION.md | A-01 new block once, old block absent; sha256 `d4331c39…8d9f`; 274 lines | new block 1, old 0; sha256 `d4331c39db7f452cd3ba72fdfa4bad540a6053931218359a93646971acb28d9f`; 274 lines; equals group-3 manifest | VERIFIED |
| 11 | MODIFY | Consolidated_Coverage.csv | 31 HOST_INTEGRATION rows: SHA256 `d4331c39…`, `git-blob:f4a5281e…`, SourceLine n+1; nothing else changed | 31/31 rows carry the new SHA256 and blob; 31/31 IDs are on their `SourceLine`; 0 non-HI rows differ from `39c97257b`; 144 rows; sha256 `36677365…13ea` = manifest and H-3 | VERIFIED |
| 12 | MODIFY | OI-012 | `Consequence` = the B-02 whole new value; `Status` OPEN; 23 OPEN | field equals the new value exactly; OPEN; 23 OPEN rows; OI-001/OI-002 OPEN (B-03 option A, no edit); sha256 `a1178218…80f0` = manifest | VERIFIED |
| 13 | MODIFY | SOFTWARE_DECOMP.md | B-04 entry after the SCA-V4-001 entry with `{ACCEPT_DATE}` 2026-09-29, `{AMENDMENT_SNAPSHOT}` `SCA-V4-002_2026-09-29_1901`, five clause slots filled; no unfilled token | the filled entry occurs exactly once; no `{…}` token remains; sha256 `ea3388bcb05b2280bd7d5…` = post-acceptance record H-1 (the group-3 manifest binds the pre-H-1 bytes `74340581…5747`, as its Role column states) | VERIFIED |
| 14 | MODIFY | DEL-04-01 | Deliverables.csv Description and `_CONTEXT.md` line 13 carry "PKG-02 checkpoint acts are never substituted by autonomy (holds only in the governance phase);" once; old substring absent; mirror equal | CSV new 1 / old 0; `_CONTEXT.md` new 1 / old 0; line 13 = `- **Description:** ` + CSV field; sha256 `552df060…6bf3` and `2a01a70b…2247` = manifest; register UPDATE run for DEL-04-01 (DX) | VERIFIED |
| 15 | MODIFY | `_LATEST_ACCEPTED.md`, `_LATEST.md` | B-06a appended (with the REVISEs); B-06b applied in the candidate; parser-safe | B-06a block present once; sha256 `6ef9c0ba…` (changed from `d5d873b3…` at `1efd4bcda`, bound by DAG-003 `SOURCE_MANIFEST.sha256`, 130/130 OK); B-06b present once, exactly one `Latest:` line; sha256 `b1b8410b…ccc3` = manifest | VERIFIED |
| 16 | MODIFY | five `_CONTEXT.md` | B-06c line 3 in DEL-02-03, 05-01, 05-02, 09-07, 04-01; the other 36 untouched | exactly those 5 files carry the new line; 36 carry the old line; all five hashes equal the manifest | VERIFIED |

16 of 16 VERIFIED; 0 DISCREPANCY; 0 NOT_EXECUTED; 0 DEFERRED_BY_HUMAN; 0 SUPERSEDED. The candidate application log (`Evidence/Application/apply_log.json`) lists the ten candidate edits and the four held items (B-03, B-04, B-06a, C-01); the held items were applied later as recorded (H-1 at `af918ee50`; B-06a at `1efd4bcda`; C-01 at `af918ee50`; B-03 no edit by Q-5 option A). No `_STATUS.md` changed between `39c97257b` and `HEAD` (0 files), consistent with `NO_STATUS_TOUCH` and Propagation_Plan §4.

---

## Pass 2 — Downstream Rerun Verification

Sufficiency was judged from input-hash binding and scope, not dates.

| Agent / workflow | Scope | Evidence of completion | Status |
|---|---|---|---|
| `scope-of-work` MODE=REVISE + VERIFY (rows 1–9) | 9 SoWs, 26 blocks, `NO_STATUS_TOUCH` | `AgentRuns/…/RV/RV_DEL-*.md` (9): each binds `SOW_REVISIONS.md` `440d4d50…d00d`, the register `158702bf…`, `PRIOR_CONTRACT_SHA256` equal to the group-3 manifest prior, and a revised hash equal to the current bytes; VERIFY checks 3, 4, 8, 9, 13, 16, 18–22 PASS; validators 9/9. Commit `1efd4bcda`. No SoW changed since | COMPLETED |
| `dependency-extract` MODE=UPDATE (rows 1–9, 14; DEL-04-02/04-03 re-quoting per ASC-ISS-008; DEP-09-07-016 per ASC-ISS-007) | 11 registers | `DX/DX_DEL-*.md` (11) + `DX_SCC-CHECK.md`: each binds the revised `ScopeOfWork.md` hash (all 11 equal current), output hashes equal current `Dependencies.csv`, `_DEPENDENCIES.md` and `_run_records/dependency-extract-20260929-sca002.md`; schema/enum/ID validators PASS; EVQ/DRB 0/0 over 41 registers; 820/820 quotes verbatim; exactly N-18, N-21, N-24, X-1 added; guards held. Commit `8cd783d8d`; no register changed since | COMPLETED |
| `project-dag` currency (rows 2, 3, 15) | DAG-002 vs post-REVISE/UPDATE basis | `_Evaluation/DAGCurrency/CURRENCY_APP_V4_SCA002_2026-09-29_2057/` at `8cd783d8d`: DEPARTURE, +4 held / 0 removed, 5 DAG pending; `_LATEST_ACCEPTED.md` drift classified as evidence drift. Then `CURRENCY_APP_V4_DAG003_ACCEPTED_2026-09-29_2218/`: CURRENT, 0 pending; DAG-003 `SOURCE_MANIFEST.sha256` 130/130 OK (re-run here: 130 OK) | COMPLETED |
| `project-dag` TRIGGER=SUCCESSOR (rows 2, 3) | DAG-003 | Candidate at `b547125db` on basis `8cd783d8d`; V15 READY; owner DECISION-4 "Accept DAG-003 (Recommended)"; published at `HEAD` with `ACCEPTANCE_RECORD.md`, `HANDOFF_STATE.md` (V15 O-1 count corrected at line 149), `MANIFEST.sha256` 37/37 OK (re-run here); `_DAG/_LATEST.md` = `PROPOSED_LATEST.md` with the date filled | COMPLETED |
| `audit-decomp` (rows 10, 11, 14) | PKG-01, 02, 03, 04, 05, 09, 10 | `AgentRuns/…/POSTACCEPT/` (H-4): `INPUT_MANIFEST.sha256` binds HOST_INTEGRATION `d4331c39…`, Consolidated_Coverage `36677365…`, Deliverables `552df060…`, Open_Issues `a1178218…`, SOFTWARE_DECOMP `ea3388bc…`, `_Decomposition/_LATEST.md` `b1b8410b…` and the five `_CONTEXT.md` at their current hashes; 0 BLOCKER, 38 WARNING, 100 INFO; COV-139 absent. It predates the REVISEs and B-06a, which these rows do not require (ASC-ISS-005) | COMPLETED |
| `project-setup` INCREMENTAL (rows 1–9) | wrapper of the propagation | Substantive steps (REVISE, B-06a, UPDATE, currency, DAG-003, this audit) complete as above. The closing records — Phase 5.7 "Incremental setup for SCA-V4-002" report, Phase 3.1 coordination refresh, `SETUP_LOG.md` line — are absent: `SETUP_LOG.md` ends at the SCA-V4-001 line; `_COORDINATION.md` has no SCA-V4-002 or DAG-003 reference. Propagation_Plan §5 step 5 sequences them after `audit-scope-closure` | NO_EVIDENCE for the closing records, by the accepted sequence (ASC-ISS-002) |
| Decomposition owner: `Coverage_Telemetry.json` rebuild | derived companion | sha256 `178ec20abeddfb55…f620`, unchanged; POSTACCEPT still carries COV-119/120 | DEFERRED_BY_HUMAN — DECISION-8 answer 2 (`APP-V4-BASIS-ALIGN-20260928`), carried by SCA-V4-002 `Handoff_State.md`; group-3 `DECISION.md` withholds the write (ASC-ISS-003) |
| App v4 design undertaking: 17 Design re-pins | 17 files (CA1 list) | The same 17 files still pin pre-SCA-V4-001 values (7 pin the superseded basis-document hashes; none pins an SCA-V4-002 prior SoW hash or the pre-A-01 HOST_INTEGRATION hash, so the set did not grow). No design pass since | DEFERRED_BY_HUMAN — DECISION-8, confirmed by DECISION-2 over OWNER_ITEMS Q-15 (ASC-ISS-004) |
| `audit-scope-closure`, superseding snapshot for SCA-V4-001 (ASC-ISS-001 confirmation) | SCA-V4-001 | `ScopeClosure_SCA-V4-001_2026-09-29_2221/` (node CA3): CLOSED_WITH_OBSERVATIONS, 0/0/0/10; `SUPERSESSION_NOTE.md` names the superseded `…_1222` snapshot; written in parallel with this audit and complete at the time of this write | COMPLETED |
| Estimation / schedule reruns | — | none recommended; no `_Estimates/` or `_Schedule/` exists | NOT_APPLICABLE |

Recommended: 9 (the 9 RV and 11 DX runs counted as one rerun class each). Completed: 6. Deferred by human: 2. Pending by accepted sequence: 1 (the setup closing records).

---

## Pass 3 — Orphaned References

No `REMOVE`, `MERGE`, `SPLIT` or `RECLASSIFY` action; no entity ID is retired and no name changed (`Deliverables.csv` Name column equals the GROUP3 canonical for all 41).

- **Scan:** all 41 `Dependencies.csv` (820 ACTIVE rows) read here: 0 rows target a `DEL-` ID absent from `Deliverables.csv`; 0 `TargetName` values differ from the current Name. The registered analyzer's snapshot `_Evaluation/DepClosure/CLOSURE_APP_V4_SCA002_2026-09-29_2056/` at `8cd783d8d` (the same register bytes as `HEAD`): orphans 0, outside-scope 0, anchors 41/41.
- **Superseded wording outside the register** (carried from CA1 ASC-ISS-007): DEL-10-03 REQ-005 now reads "minimal host loop … local or cloud model the person chooses" (fixed by row 1); `DEP-09-07-016` Notes restated (DX); `_Coordination/HANDOFF_SWBPIPE_DOMAINS.md` line 22 ("local-first host operation") is carried with the next SWBPIPE relay (DECISION-8); `_Decomposition/Allocation_Rationale.csv` keeps pre-amendment description quotes as `NO_CHANGE` history (accepted); the Design files that say "Declared checkpoints override …" / "local-first" are inside the deferred re-pin set; `conceptual/` files are history. Recorded as ASC-ISS-006 (OBSERVATION).

No orphaned references detected.

---

## Pass 4 — Decomposition Consistency

- **Change Log:** the SCA-V4-002 entry is present once in `SOFTWARE_DECOMP.md` `## Decision Log` after the SCA-V4-001 entry, with the accepted date, snapshot name and the five clause texts; no unfilled token.
- **Scope Ledger / Packages:** no ADD/REMOVE/RECLASSIFY; `ScopeLedger.csv`, `Packages.csv` and the other NO_CHANGE registers are not in the `39c97257b..HEAD` diff; POSTACCEPT check 7e: 11 packages, 41 deliverables, 10 objectives, 262 scope items, 262 ledger rows.
- **Deliverables section:** `Deliverables.csv` differs from the GROUP3 canonical only in the Description of DEL-02-03, DEL-05-01, DEL-09-07 (SCA-V4-001) and DEL-04-01 (this amendment, D-014).
- **Coverage:** `Pre_Change_Coverage.json` 0 BLOCKER / 38 WARNING / 101 INFO → `Post_Change_Coverage.json` 0 / 39 / 101 (the one new WARNING, COV-139, was the candidate's unwritten records, classified EXPECTED_CONSEQUENCE and closed) → POSTACCEPT 0 / 38 / 100. Forward, reverse, context-fidelity and objective coverage 100 % throughout; no new unassigned scope item; the 38 WARNINGs are pre-existing (37 lifecycle, COV-137).
- **Observation (ASC-ISS-005):** no `audit-decomp` has run over the state after the REVISEs and B-06a; the register does not require one for rows 1–9 or 15, and the post-REVISE validation lane (Propagation_Plan §7) ran in the RV records. The inherited audit script's `FIRST_AMENDMENT`-era heuristic (false BLOCKER on the `**Accepted predecessor:**` line) is disclosed in `POSTACCEPT/COMPARISON.md` and V15 O-2; the next run under `ACCEPTED_PREDECESSOR` posture needs the (f)/(g) adjustments or a script fix.
- **Observation (ASC-ISS-007, handed over by CA3):** the eight registers re-extracted under SCA-V4-001 but not under SCA-V4-002 (DEL-03-01, 03-02, 03-04, 05-01, 05-02, 08-01, 09-06, 09-09) carry run records (`dependency-extract-20260929.md`) binding `SOFTWARE_DECOMP.md` at its pre-B-04 hash `74340581…5747`; the 11 SCA-V4-002 records bind the current `ea3388bc…9dd5`; the 23 never-re-extracted registers bind the pre-SCA-V4-001 hash `9d44c2ad…` from 2026-09-27. B-04 adds only the Change Register entry and row 13 lists no dependency-extract rerun; no row, quote, arc or verdict depends on it (820/820 quotes verbatim; DAG-003 CURRENT). Evidence drift, not a required rerun.
- DOMAIN validator: not applicable (SOFTWARE).

---

## Pass 5 — Context Metadata Consistency

Twelve affected deliverables: the nine of rows 1–9 and DEL-04-01, DEL-05-01, DEL-05-02 (rows 14, 16).

| Check | Result |
|---|---|
| `_CONTEXT.md` `Name` and `PackageID` equal `Deliverables.csv` | 12/12 |
| Accepted-basis line 3 | the five files of row 16 carry the reading rule; the other seven (rows 1–9 not in row 16) keep the unamended line, as B-06c specifies ("the other 36 are left alone") |
| DEL-04-01 Description mirror | `_CONTEXT.md` line 13 equals the CSV field |
| Discipline / Type / Responsible | not modified by the amendment; not checked beyond Name/Package |
| Scope Traceability | no SOW/OBJ mapping changed (Scope Ledger unchanged) |
| `_STATUS.md` lifecycle | unchanged bytes for all 41 (0 in the diff); DEL-02-01, 02-03, 03-03, 04-02, 01-01, 04-01, 05-01, 05-02 IN_PROGRESS; DEL-10-03, 09-07, 01-04, 02-02 INITIALIZED, as Propagation_Plan §4 lists; no history line expected under `NO_STATUS_TOUCH` |
| SoW frontmatter `decomposition_basis` | unchanged (O-22), all nine |

No finding.

---

## Pass 6 — Supersession Binding Completeness

Run because row 14 has `SupersessionBindingPresent = YES`.

1. **Register binding:** row 14 → `D-014` present in `Supersession_Delta.csv` (AmendmentID SCA-V4-002). The other 17 rows are `DL-SCA-V4-001-A18 … A25`, `A36-D-10a/b`, `A42-D-11a..d`, `A46-D-12a..c`: decision-log-only bindings for SCA-V4-001 actions 18–25, 36, 42, 46 under DECISION-2 Q-10 option (a) (Decision_Log "Decision-log reference"), the accepted `DL-{reference}` convention. No SCA-V4-002 action lacks its row.
2. **Paths:** all 18 `SupersededAuthorityPath` values resolve (`checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/ScopeLedger.csv` ×8, `canonical/Deliverables.csv` ×10).
3. **Refs:** all 18 `OverrideType = SUPERSESSION`; every `SupersededAuthorityRef` names a row ID and column (and a substring where applicable); none empty. Checked here: each superseded fact is a substring of its canonical field (18/18); each replacement is a substring of the current working field (18/18); no superseded fact survives in the working field.
4. **Accumulation:** `tools/coordination/accumulate_supersession_map.py --prior-map SCA-V4-001_2026-09-28_2155/Supersession_Map.csv --delta SCA-V4-002_2026-09-29_1901/Supersession_Delta.csv --check-map SCA-V4-002_2026-09-29_1901/Supersession_Map.csv` (outputs in this folder): 29 rows (11 + 18), 0 findings, exit 0; `Expected_Supersession_Map.csv` sha256 equals the snapshot's map (`45502bf5…eb93`). Prior map hash `e8e43320…a801` equals the group-2 manifest binding. No reconstruction was needed.
5. **Applicability:** `AppliesToRoots`, `AppliesToFacilities` and `AppliesToSections` are blank on all 29 rows: global scope, as CA1 read it for SCA-V4-001; SOFTWARE has no root/facility vocabulary. Not a finding.

The bindings are active: `_ScopeChange/_LATEST.md` names `SCA-V4-002_2026-09-29_1901` (`Latest:` line; registered parser resolves it per the post-acceptance record 3i). This confirms, from the SCA-V4-002 side, the path-level binding CA3's snapshot relies on for closing SCA-V4-001's ASC-ISS-001.

No finding.

---

## Pass 7 — KTY Content Remediation Verification

NOT_APPLICABLE: `DECOMP_VARIANT = SOFTWARE`; no `KTY_Remediation_Manifest.csv`; `ContentRemediationState` NOT_REQUIRED in every handoff record; no `.Archive/` surface in scope.

---

## Closure Determination

| Severity | Count | Issues |
|---|---|---|
| CRITICAL | 0 | — |
| MAJOR | 0 | — |
| MINOR | 1 | ASC-ISS-001 |
| OBSERVATION | 7 | ASC-ISS-002 … ASC-ISS-008 |

All eight findings are `Assessment: DETERMINATE`.

**Closure Status: CLOSED_WITH_OBSERVATIONS.** All 16 accepted actions are verified against the filesystem; every register-listed rerun that the accepted records require is complete against the amended basis with matching input hashes (REVISE, UPDATE, currency, DAG-003, audit-decomp over the candidate targets); the supersession binding is complete and active; no orphaned reference exists; the decomposition and context metadata are consistent. The one MINOR finding is that the amendment's own handoff records now understate progress (they still list the REVISEs, B-06a, the register UPDATE and DAG-003 as open). The deferred obligations — `Coverage_Telemetry.json` and the 17 Design re-pins — remain open work under the owner's DECISION-8 and are not claimed complete. The `project-setup` closing records follow this audit by the accepted sequence.

This snapshot does not supersede an earlier SCA-V4-002 audit (none exists). It does not decide SCA-V4-001; that amendment's current snapshot is `ScopeClosure_SCA-V4-001_2026-09-29_2221/` (node CA3), written in parallel. Two amendments now each have a current closure snapshot in this folder; `_LATEST.md` names this one as the latest and links the other.

---

## Recommendations

1. **ASC-ISS-001 (MINOR).** Record SCA-V4-002's completed propagation in an append-only effective-state or closeout record under `_ScopeChange/` (the C-02 pattern: `_PostAcceptanceValidation/SCA-V4-002_{UTC}_EFFECTIVE_STATE/EFFECTIVE_STATE.md`), citing this snapshot, `RV/`, `DX/`, `CURRENCY_APP_V4_SCA002_2026-09-29_2057`, `_DAG/DAG-003/ACCEPTANCE_RECORD.md` and `CURRENCY_APP_V4_DAG003_ACCEPTED_2026-09-29_2218`; or fold the same facts into the next `_ScopeChange/_LATEST.md` write. Do not edit the group-bound bytes.
2. **ASC-ISS-002.** Write the Phase 5.7 "Incremental setup for SCA-V4-002" report and the Phase 3.1 coordination refresh, then append the `SETUP_LOG.md` line, citing this snapshot (Propagation_Plan §5 step 5).
3. **ASC-ISS-003 (deferred).** Rebuild `Coverage_Telemetry.json` once, by the decomposition owner's bounded brief, now that SCA-V4-002's inputs are settled; then rerun `audit-decomp` over the post-REVISE state (item 5) to close COV-119/120.
4. **ASC-ISS-004 (deferred).** Re-pin the 17 Design files once, against the SCA-V4-002 texts, at the next design pass, GUIDE (DEL-03-04) last.
5. **ASC-ISS-005.** At the next `audit-decomp`, use a script generation carrying the (f)/(g) adjustments or a fixed base script (Root tooling, outside this amendment), so the `**Accepted predecessor:**` line is not read as a second active snapshot.
6. **ASC-ISS-006.** Keep the recorded dispositions; carry the SWBPIPE handoff wording with the next relay (DECISION-8). No amendment action.
7. **ASC-ISS-007.** No rerun for closure. Each of the eight registers rebinds `SOFTWARE_DECOMP.md` at its next UPDATE; a whole-set refresh is not warranted by a Decision Log entry alone. (The `DISPATCH.md` K3/D2/CA3/CA2 rows observed stale at `a254be160` were updated at `a5a4deaa7`.)
8. **ASC-ISS-008.** None beyond this `_LATEST.md`: it names this snapshot as latest and links the SCA-V4-001 snapshot; a later reader should resolve each amendment's snapshot by its `ScopeClosure_{AMENDMENT_ID}_*` prefix.

**Rerun of this audit.** Required when any hash in `INPUT_MANIFEST.sha256` changes, in particular after items 1–4; its date does not decide sufficiency.

This snapshot accepts nothing and makes no release, publication or reliance claim.
