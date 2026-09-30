# Scope Closure Audit — SCA-V4-001

**Audit Date:** 2026-09-29
**Closure Status:** CLOSED_WITH_OBSERVATIONS
**Amendment Date:** groups 1 and 2 accepted 2026-09-28 (DECISION-7); group 3 accepted 2026-09-29 (DECISION-8); snapshot folder `SCA-V4-001_2026-09-28_2155`
**Amendment Description:** App v4 basis alignment for owner decisions DEC-4 and DEC-5 (run `APP-V4-BASIS-ALIGN-20260928`):
- phased checkpoints (V4-WF-05);
- model access by OAuth sign-in or an API key, with no default (V4-HOST-01, V4-ARC-11);
- host-agent network destinations (V4-HOST-02, V4-ARC-12, V4-HI-70);
- "local-first" amended.

It makes 47 `MODIFY` actions and leaves the topology unchanged: 11 packages, 41 deliverables and 262 scope IDs.

**Auditor:** node CA3, run `APP-V4-SCA002-20260929`, a Type 2 TASK (Claude Code subagent). It did not delegate and wrote none of the audited files. Basis commit `a254be160` (started at `b99df0989`; see Brief); git read-only; no network.

**This snapshot supersedes** `ScopeClosure_SCA-V4-001_2026-09-29_1222/` (CA1, `OPEN`). See `SUPERSESSION_NOTE.md`.

**Verdict.** The amendment is implemented and its required reruns are
done, and the one finding that held CA1's verdict at `OPEN` is closed:
- all 47 actions are verified: the SCA-V4-001 result is reproduced byte for
  byte from git at its own commits, and every SCA-V4-001 text survives in the
  current bytes, which now also carry the accepted SCA-V4-002 edits;
- the 16 SoW REVISEs, the 18 dependency re-extractions and the DAG-002
  successor were completed against the amended basis by hash; DAG-002 has
  since been superseded by the accepted DAG-003 (SCA-V4-002's departure);
- all 22 `SupersessionBindingPresent = YES` actions are now bound at path
  level: 11 by SCA-V4-001's own `D-0NN` rows and 11 by SCA-V4-002's
  `DL-SCA-V4-001-…` rows, under the owner's ruling (DECISION-2 Q-10, option
  a; DECISION-3). The accumulated map (29 rows) reproduces with 0 findings;
- no orphan exists and no lifecycle state changed.

Status **CLOSED_WITH_OBSERVATIONS**: 0 CRITICAL, 0 MAJOR, 0 MINOR, 10
OBSERVATION; all 10 are `DETERMINATE`. Two obligations remain open as
owner-deferred work and are not claimed complete: `Coverage_Telemetry.json`
(ASC-ISS-004) and the 17 Design re-pins (ASC-ISS-005).

## Amendment Summary

**Register.** `_ScopeChange/SCA-V4-001_2026-09-28_2155/Amendment_Actions.csv`,
SHA-256 `069645d979efa1e0a20f50194acca08afa8715ce647f36ad507c5bf2b76f14d2`.
- **How it was resolved:** the amendment-qualified pointer
  `SCA-V4-001_GROUP-2_AUTHORIZED.md` leads to
  `checkpoint_snapshots/SCA-V4-001_GROUP-2_2026-09-28/ACCEPTED_MANIFEST.csv`.
  That manifest has exactly one `Amendment_Actions*.csv` row, with role
  `action register`; the hash was verified against the current bytes.
- **Not used:** `Intake_Actions.csv` (group-1 evidence). **Fallback:** none.

| Property | Value |
|---|---|
| Rows | 47, all `MODIFY` |
| `ScopeChanging` | `YES` on 30 |
| `SupersessionBindingPresent` | `YES` on 22 (1, 2, 3, 6, 8, 9, 10, 12, 15, 16, 18–26, 36, 42, 46) |
| Rows 1–17 | the four basis documents (BASIS_AMENDMENT Part A) |
| Rows 18–31 | the decomposition package (Part B) |
| Rows 32–47 | 16 `ScopeOfWork.md` contracts (SOW_REVISIONS) |

**Handoff records read (Pass 0.7), in order of currency:**
1. the snapshot's `Handoff_State.md` (`ef587edd…1ef79`, unchanged since DECISION-8);
2. the checkpoint-group `Handoff_State.md` and `DECISION.md` files (groups 1–3), unchanged;
3. `_PostAcceptanceValidation/SCA-V4-001_20260929T132946Z/` (43/43 PASS), unchanged;
4. **new:** `_PostAcceptanceValidation/SCA-V4-001_20260930T010520Z_EFFECTIVE_STATE/EFFECTIVE_STATE.md`
   (node AK1; authority DECISION-2 Q-13). It records the completed reruns, the
   two owner deferrals, and the ASC-ISS-001 ruling, and it changes no
   SCA-V4-001 byte;
5. **new:** `_ScopeChange/SCA-V4-002_2026-09-29_1901/Handoff_State.md`
   (ACCEPTED, "Carried from the predecessor") and `_ScopeChange/_LATEST.md`
   (`Latest: SCA-V4-002_2026-09-29_1901`; "Accepted predecessor:
   SCA-V4-001_2026-09-28_2155");
6. **new:** run `OWNER_DECISIONS.md` DECISION-2, DECISION-3 and DECISION-4.

Every deferral cited below names its deciding record: DECISION-8 answer 2
(Coverage_Telemetry) and DECISION-8 as confirmed by DECISION-2 Q-15 (Design
re-pins).

**Manifests and recency.** The group-1, group-2 and group-3
`ACCEPTED_MANIFEST.csv` rows are as CA1 reported (the only later differences
are the append-only `OWNER_DECISIONS.md` and the post-act H-1…H-4 targets that
the group-3 DECISION expects). The amendment date is not in the future.

## Pass 1 — Action Verification

**Method.** The CA1 method is reproduced and extended:
1. Reconstruct the SCA-V4-001 result from the accepted packet (`BASIS_AMENDMENT.md`
   old→new blocks on the preimage `f4ba34c2c`; the 162 SoW E-block pairs on
   `a0af39f8c`) and compare with the bytes at `102f09c1a`, the commit CA1
   audited. **Result: 5/5 Part A files and 16/16 SoWs byte-equal.** CA1's
   verification is reproduced from git history.
2. Compare the reconstruction with the current bytes. Where they differ, test
   every SCA-V4-001 `new` block for presence in the current file, and explain
   each absence against SCA-V4-002's accepted packet (`BASIS_AMENDMENT.md`
   `091871fd…4238`, `SOW_REVISIONS.md` `440d4d50…d00d`) and RV returns.
3. Part B: re-run the field and mirror checks on the current CSVs and
   `_CONTEXT.md` files (script `verify_partB.py`, `03aeb822…`).
- **Scripts:** `verify_pass1_ca3.py` and `verify_partB.py` in the session
  scratchpad `CA3/` (hashes in `QA_Report.md`).

| ActionSeq | ActionType | EntityID | Expected | Actual | Status |
|---|---|---|---|---|---|
| 1–7 | MODIFY | docs/PRD.md (V4-WF-05, V4-HOST-01/02, §2.2, OQ-03, §1.1, status) | A01–A07 applied | Reconstruction equals `102f09c1a` and equals the current file (`bb6e786f…`); 8/8 blocks present | VERIFIED |
| 8–11 | MODIFY | docs/ARCHITECTURE.md (V4-ARC-11/12, host-agent properties, §1) | A08–A11 applied | Reconstruction equals `102f09c1a` and the current file (`317d5789…`); 5/5 blocks present | VERIFIED |
| 12–14 | MODIFY | docs/HOST_INTEGRATION.md (V4-HI-42, §8.1, V4-HI-70) | A12–A14 applied | Reconstruction equals `102f09c1a`; the current file (`d4331c39…`) differs only by SCA-V4-002 action 10 (A-01, the A17b line join: one line split in two, no word changed); 4/4 SCA-V4-001 blocks present | VERIFIED |
| 15–16 | MODIFY | docs/EXAMINATION.md (V4-EXM-22/23) | A15–A16 applied | Reconstruction equals `102f09c1a` and the current file (`471798bc…`); 3/3 blocks present | VERIFIED |
| 17 | MODIFY | docs/*.md#status | A17a-c (H-2) applied | As rows 8–16; the A17b status line is the one SCA-V4-002 re-laid out | VERIFIED |
| 18–25 | MODIFY | SOW-015, -016, -017, -052, -137, -138, -201, -202 | D-01…D-08 statements | Current `ScopeLedger.csv` (`d8136297…`, unchanged) equals the packet value on all 8; `DecisionRef` = `APP-V4-BASIS-20260926;{DECISION};SCA-V4-001` | VERIFIED |
| 26 | MODIFY | Declared checkpoint | D-09 | `Vocabulary_Map.csv` Notes equals the packet value | VERIFIED |
| 27 | MODIFY | PKG-05 | D-13 (+B7 DEL-05-01/05-02) | `Packages.csv` carries the new text, old absent; both mirrors match | VERIFIED |
| 28–29 | MODIFY | OI-001, OI-002 | D-14a/b, Status OPEN | `Open_Issues.csv` Consequence equals the packet value; Status `OPEN` (SCA-V4-002 changed only OI-012) | VERIFIED |
| 30 | MODIFY | SOFTWARE_DECOMP.md#decision-log | D-15 + D-16 (H-3) | The SCA-V4-001 entry is present verbatim in `## Decision Log`; the file (`ea3388bc…`) differs from `102f09c1a` only by the appended SCA-V4-002 entry (B-04, H-1 of DECISION-3) | VERIFIED |
| 31 | MODIFY | Consolidated_Coverage.csv | B8 x2 (H-4) | 144/144 rows: `SHA256` equals the current document hash; the 9 `Standing` "amended by SCA-V4-001" marks (V4-WF-05, HOST-01/02, ARC-11/12, HI-42/70, EXM-22/23) stand. The file (`36677365…`) was recomputed by SCA-V4-002 B-01 for the 31 HOST_INTEGRATION rows after A-01 | VERIFIED |
| 32 | MODIFY | DEL-04-01 | 13 pairs | Prior `fc1a0503…` = packet; reconstruction = `102f09c1a` = current `ac043e54…` | VERIFIED |
| 33 | MODIFY | DEL-04-02 | 10 pairs | Reconstruction = `102f09c1a` (`e077f20a…`); current `f16ffa8a…` = SCA-V4-002 RV result, whose `PRIOR_CONTRACT_SHA256` = `e077f20a…`. SCA-V4-002 action 8 revised CLM-004 and added AX-005 only; the SCA-V4-001 CLM-002 text is unchanged | VERIFIED |
| 34 | MODIFY | DEL-04-03 | 6 pairs | Reconstruction = `102f09c1a` = current `ceecddbb…` | VERIFIED |
| 35 | MODIFY | DEL-02-01 | 9 pairs | Reconstruction = `102f09c1a` (`6ccc860b…`); current `ef360edf…` = SCA-V4-002 RV result (prior `6ccc860b…`); 9/9 SCA-V4-001 blocks present | VERIFIED |
| 36 | MODIFY | DEL-02-03 | 14 pairs + D-10a/b | Reconstruction = `102f09c1a` (`a4ffcd87…`); current `0006521b…` = SCA-V4-002 RV result (prior `a4ffcd87…`). SCA-V4-002 action 3 (F-0203-01) inserted the consumption sentence into CLM-002; all 8 sentences of the SCA-V4-001 E-0203-04 text survive in that line; 13/14 other blocks present verbatim; D-10a/b and mirrors hold | VERIFIED |
| 37–40 | MODIFY | DEL-03-01, -02, -04 (and -03) | 9/10/10 pairs | DEL-03-01 `9ada531b…`, DEL-03-02 `35609151…`, DEL-03-04 `895f004e…`: reconstruction = current. DEL-03-03: reconstruction = `102f09c1a` (`fdd22e25…`); current `93faf918…` = SCA-V4-002 RV result (prior `fdd22e25…`); 10/10 SCA-V4-001 blocks present | VERIFIED |
| 41 | MODIFY | DEL-01-01 | 4 pairs | Reconstruction = `102f09c1a` (`f65dc666…`); current `9945e72b…` = SCA-V4-002 RV result (prior `f65dc666…`); 4/4 blocks present | VERIFIED |
| 42 | MODIFY | DEL-05-01 | 19 pairs + D-11a-d | Reconstruction = `102f09c1a` = current `9b2379a1…`; mirrors hold | VERIFIED |
| 43 | MODIFY | DEL-05-02 | 16 pairs + D-13 | Reconstruction = `102f09c1a` = current `beb9c66c…`; mirror holds | VERIFIED |
| 44 | MODIFY | DEL-09-06 | 11 pairs | Reconstruction = `102f09c1a` = current `287d47a1…` | VERIFIED |
| 45 | MODIFY | DEL-09-09 | 8 pairs | Reconstruction = `102f09c1a` = current `e887a579…` | VERIFIED |
| 46 | MODIFY | DEL-09-07 | 11 pairs + D-12a-c | Reconstruction = `102f09c1a` (`53b51d30…`); current `813ef0f3…` = SCA-V4-002 RV result (prior `53b51d30…`); 11/11 blocks present; D-12a-c and mirrors hold | VERIFIED |
| 47 | MODIFY | DEL-08-01 | 2 pairs | Reconstruction = `102f09c1a` = current `df279586…` | VERIFIED |

**Result:** 47/47 VERIFIED; 0 DISCREPANCY; 0 NOT_EXECUTED; 0 DEFERRED; 0
SUPERSEDED. No SCA-V4-001 action was withdrawn or replaced by SCA-V4-002;
where SCA-V4-002 touched the same file, its edits are additive or elsewhere,
and the SCA-V4-001 text is present. Two `new` blocks (DEL-04-02 E-0402-02,
DEL-05-02 E-0502-02 second pair) are not contiguous substrings at
`102f09c1a` either, because later E-blocks in the same packet re-edit the
same text; the sequential reconstruction is byte-equal, so they are verified
by that route. All 16 SoWs validate (`validate_scope_of_work.py` PASS;
`check_boundary_owner_resolution.py` exit 0) on the current bytes.

## Pass 2 — Downstream Rerun Verification

**Sources:** the register's `DownstreamReruns`; `RUN_SUMMARY.md` "Open
downstream work"; `Propagation_Plan.md` §5–§7; the group-3 DECISION.md; the
effective-state record; SCA-V4-002's Handoff_State "Carried from the
predecessor".

| Agent / workflow | Scope | Evidence | Status |
|---|---|---|---|
| `audit-decomp` (rows 1–3, 8, 9, 12, 15, 16, 18–25, 31) | the seven baseline packages | POSTACCEPT of `APP-V4-BASIS-ALIGN-20260928` bound the SCA-V4-001 hashes (CA1, reproduced by V13). Since then SCA-V4-002's BASELINE, POSTCHANGE and POSTACCEPT runs bind the current documents: 0 BLOCKER, 38 WARNING, 100 INFO; forward, reverse and objective coverage 100 % | COMPLETED |
| `project-setup` INCREMENTAL → `scope-of-work` REVISE + VERIFY (rows 32–47) | 16 deliverables | Commit `340ecf341`; `RV/RV-1…4` of the BASIS-ALIGN run bind prior = packet and result = SCA-V4-001 hashes; reproduced in Pass 1 from git. Six of the 16 were revised again under SCA-V4-002 with `PRIOR_CONTRACT_SHA256` = the SCA-V4-001 result (RV_DEL-01-01, -02-01, -02-03, -03-03, -04-02, -09-07; each PASS, `_STATUS.md` unchanged) | COMPLETED |
| `dependency-extract` UPDATE (Propagation_Plan §5; DECISION-9) | the 16 plus DEL-01-04 and DEL-02-02 | Commit `b585e5ebe`; all 18 `dependency-extract-20260929.md` records bind the SCA-V4-001 SoW, `SOFTWARE_DECOMP.md` `7434058…` and `ScopeLedger.csv` `d8136297…`. Now every one of the 41 registers has a run record binding its **current** SoW hash: 11 through `dependency-extract-20260929-sca002.md` (SCA-V4-002 UPDATE, also binding the current `SOFTWARE_DECOMP.md` `ea3388bc…`), 30 through their earlier records. DAG-003's `SOURCE_MANIFEST.sha256` binds all 41 registers and 41 SoWs at current hashes (130/130 OK) | COMPLETED |
| `project-dag` currency audit → DAG-002 successor | full graph | DAG-002 accepted under DECISION-10 (`_DAG/DAG-002/ACCEPTANCE_RECORD.md`; `MANIFEST.sha256` 37/37 OK; `audit_dag.py --canonical --strict` exit 0 on the current tree). It has since **departed** on SCA-V4-002's four arcs (currency `CURRENCY_APP_V4_SCA002_2026-09-29_2057`: DEPARTURE, 5 DAG pending; DAG-002 `SOURCE_MANIFEST` now 98 OK / 32 changed) and is **superseded by DAG-003**, accepted under DECISION-4 and published at `a254be160` (`_DAG/_LATEST.md` `Latest: DAG-003`; DAG-003 `MANIFEST` 37/37, `SOURCE_MANIFEST` 130/130, strict audit exit 0; currency `CURRENCY_APP_V4_DAG003_ACCEPTED_2026-09-29_2218`: CURRENT, no DAG pending) | COMPLETED; then SUPERSEDED_BY:DAG-003 (DECISION-4) — ASC-ISS-010 |
| `Coverage_Telemetry.json` RECOMPUTE | the decomposition owner | Unchanged at `178ec20a…f620`. DECISION-8 answer 2 "Record as stale, fix later"; carried by the effective-state record and SCA-V4-002 Handoff_State | DEFERRED_BY_HUMAN (ASC-ISS-004) |
| Design re-pins | App v4 design undertaking | 17 Design files still pin superseded basis-document hashes and/or their pre-revision SoW hash (same 17 as CA1; list below). Deciding record: DECISION-8, confirmed by the owner at DECISION-2 Q-15 | DEFERRED_BY_HUMAN (ASC-ISS-005) |

**Not counted as reruns:** this audit; SCA-V4-002 and the SWBPIPE relay
note (residuals outside SCA-V4-001, DECISION-8 answer 3).

**SETUP_LOG.** `_Coordination/SETUP_LOG.md` line 6 still reads
"INCREMENTAL SCA-V4-001 setup COMPLETE; run record
`AgentRuns/APP-V4-BASIS-ALIGN-20260928/`…", and every DECISION-9 plan item is
evidenced above. No SCA-V4-002 line has been appended yet (that belongs to
SCA-V4-002's audit; ASC-ISS-009 unchanged).

**The 17 stale Design files** (of 37 files under `Design/`, 19 Markdown):
DEL-01-01 `HOSTING_BOUNDARY.md`, `PIN_SPIKE_0.158.0.md`; DEL-02-01
`EXAMPLES.md`, `WORKFLOW_DECLARATION.md`; DEL-02-03
`EXECUTION_COMPATIBILITY.md`; DEL-03-01 `CATALOG_AND_READ_BASIS.md` (HI);
DEL-03-02 `PROPOSAL_LIFECYCLE_AND_OUTCOMES.md` (HI); DEL-03-03
`ADAPTER_ENABLEMENT_AND_RECEIVING.md` (PRD, ARCHITECTURE, HI, EXAMINATION);
DEL-03-04 `HOST_INTEGRATION_GUIDE.md` (HI); DEL-04-01
`ACT_AND_POLICY_CONTRACT.md`; DEL-04-02 `AUTONOMY_AND_STANDING_EXCHANGE.md`;
DEL-04-03 `RECORD_SEMANTICS.md`; DEL-05-01 `LOOP_RECEIVING_CONTRACT.md`;
DEL-05-02 `PANEL_RECEIVING_CONTRACT.md`; DEL-09-06
`CONNECTED_ACTIVITY_CONTRACT.md`, `RELAY_QUESTIONS_SWBPIPE.md` (PRD, HI,
EXAMINATION); DEL-09-09 `EXTERNAL_TRACE_CASES.md` (PRD, HI, EXAMINATION).
Seven of them (DEL-01-01 x2, DEL-02-01 x2, DEL-02-03, DEL-03-03, DEL-04-02)
now also lag the SCA-V4-002 revision of their SoW, which strengthens the
accepted sequencing (re-pin once, after SCA-V4-002, GUIDE last).

## Pass 3 — Orphaned References

No `REMOVE`, `MERGE`, `SPLIT` or `RECLASSIFY` action; no entity retired.
- **Scan:** all 41 `Dependencies.csv` (826 rows) with
  `analyze_dep_closure.py` (`2b8de3cb…`) on the current tree:
  `orphan_count` 0, `implements_node_missing` 0, `schema_invalid` 0,
  `orphan_dependencies` PASS. Its `subject_status` FAIL comes from the six
  admitted cycles (`circular_dependencies` BLOCKER, pre-existing) and, at the
  time of the run, the DAG-002 departure (`dag_currency` WARNING); its
  `accepted_dag` block (added arcs, DAG pending) is identical to the recorded
  `CURRENCY_APP_V4_SCA002_2026-09-29_2057/Evidence/analyzer.stdout.json`.
- **Names:** no deliverable or package name changed; no `TargetName` is stale.
- **Anchor rows:** the rows on the 8 amended ledger IDs carry the amended
  statements (unchanged `ScopeLedger.csv`).

No orphaned references were detected.

**Residual wording outside the register** (ASC-ISS-007, OBSERVATION):
- DEL-10-03 REQ-005 "local-first": revised under SCA-V4-002 action 1; the
  phrase is absent from the current SoW;
- DEP-09-07-016 Notes: restated at SCA-V4-002's re-extraction; the old
  "candidate/run/configured endpoint" wording survives only inside a History
  clause marked "superseded (ASC-ISS-007)";
- `HANDOFF_SWBPIPE_DOMAINS.md` line 22 "local-first host operation": still
  present, carried to the next relay as accepted (DECISION-8);
- `Allocation_Rationale.csv`: NO_CHANGE as accepted (history).

## Pass 4 — Decomposition Consistency

The variant is SOFTWARE; the DOMAIN integrity validator does not apply.

1. **Change Log.** `## Decision Log` holds the SCA-V4-001 entry verbatim
   (H-3, D-15/D-16), followed by the SCA-V4-002 entry (B-04). The file is
   bound by SCA-V4-002's post-acceptance validation (check 2d) and by the
   11 `sca002` run records.
2. **Scope Ledger.** `ScopeLedger.csv` is byte-unchanged since CA1
   (`d8136297…`): the 8 amended statements and `DecisionRef` values stand;
   totals IN 234, OUT 15, TBD 13.
3. **Packages.** None added or removed; the PKG-05 description is amended (D-13).
4. **Deliverables.** DEL-02-03, DEL-05-01 and DEL-09-07 carry D-10…D-12.
   DEL-04-01's "PKG-02 checkpoints override autonomy" is now "PKG-02
   checkpoint acts are never substituted by autonomy (holds only in the
   governance phase)" (SCA-V4-002 action 14, D-014), with its `_CONTEXT.md`
   mirror; ASC-ISS-002 is applied.
5. **Coverage.** `Pre_Change_Coverage.json` (= BASELINE: 0/2/126) →
   `Post_Change_Coverage.json` (= POSTCHANGE: 0/38/94) → BASIS-ALIGN
   POSTACCEPT (0/38/94) → SCA-V4-002 BASELINE (0/38/101) → POSTCHANGE
   (0/39/101) → POSTACCEPT (0/38/100): forward (partitions and production
   units), reverse and objective coverage 100 % throughout; no unassigned
   scope item; the 38 WARNINGs are the DECISION-6 lifecycle set (37) and the
   heading-binding warning. No regression is attributable to SCA-V4-001.

## Pass 5 — Context Metadata Consistency

**`_CONTEXT.md`.** All 41 checked against `Deliverables.csv` (every
non-empty column value of the row must occur in the file): 0 mismatches. The
DEL-04-01 mirror (D-014) holds.

**`_STATUS.md`.** 41/41 byte-unchanged since `67a2fac4b` (DECISION-6):
27 INITIALIZED, 14 IN_PROGRESS. SCA-V4-002's REVISEs ran `NO_STATUS_TOUCH`
(each RV return records the `_STATUS.md` hash unchanged). No deliverable is
CHECKING or ISSUED.

**Basis lines.** 36 `_CONTEXT.md` files name GROUP3 alone; the five that
carry amended text (DEL-02-03, DEL-04-01, DEL-05-01, DEL-05-02, DEL-09-07)
now add "Read it as amended by the active scope-change snapshot named in
`_ScopeChange/_LATEST.md`" (B-06c). ASC-ISS-006 is applied.

## Pass 6 — Supersession Binding Completeness

This pass ran because 22 register rows have `SupersessionBindingPresent = YES`.

1. **D-{ActionSeq} derivation.** 11 of 22 have their own SCA-V4-001 row
   (D-001, 002, 003, 006, 008, 009, 010, 012, 015, 016, 026). The other 11
   (actions 18–25, 36, 42, 46) are now bound at path level by the 17
   `DL-SCA-V4-001-A{NN}[-D-xx]` rows of `SCA-V4-002/Supersession_Delta.csv`,
   which the method accepts as the producer-side convention for
   decision-log-only bindings, and which the owner ruled (DECISION-2 Q-10,
   option a) and accepted into effect (DECISION-3). Each names the GROUP3
   canonical `ScopeLedger.csv` (SOW-015…202) or `Deliverables.csv`
   (DEL-02-03 D-10a/b, DEL-05-01 D-11a-d, DEL-09-07 D-12a-c) as
   `SupersededAuthorityPath` and the row/column/substring as
   `SupersededAuthorityRef`. **ASC-ISS-001 is closed**; both sides of the
   CA1 conflict are now satisfied: the accepted record stands unchanged, and
   the path-level binding exists.
2. **Authority paths.** All 11 SCA-V4-001 paths resolve (CA1, unchanged
   files). All 18 SCA-V4-002 rows: the path exists; the superseded fact
   occurs, whitespace-normalized, in the GROUP3 canonical file; the
   replacement occurs in the current working file; the superseded text does
   not survive in the current file.
3. **References.** All 29 `SupersededAuthorityRef` values are non-empty;
   every row is `SUPERSESSION`.
4. **Accumulator** (`accumulate_supersession_map.py`, `d967144d…`):
   - SCA-V4-001 alone (reproducing CA1): `--delta` SCA-V4-001,
     `--check-map` SCA-V4-001: 11 rows, 0 findings; output byte-identical to
     `SCA-V4-001/Supersession_Map.csv` (`e8e43320…a801`);
   - chained: `--prior-map` SCA-V4-001's map, `--delta` SCA-V4-002's delta,
     `--check-map` SCA-V4-002's map: 29 rows, 0 findings; output
     byte-identical to `SCA-V4-002/Supersession_Map.csv` (`45502bf5…eb93`).
     This snapshot's `Expected_Supersession_Map.csv` and
     `Supersession_Map_Findings.csv` are that run's outputs.
5. **Applicability.** Blank `AppliesToRoots`, `AppliesToFacilities` and
   `AppliesToSections` on all 29 rows: global scope, valid for SOFTWARE.

**Visibility.** `_Decomposition/_LATEST.md` and
`checkpoint_snapshots/_LATEST_ACCEPTED.md` now carry the reading rule
"as amended by the active scope-change snapshot named in
`_ScopeChange/_LATEST.md`" (B-06a/b). `_LATEST_ACCEPTED.md` is bound at its
noted state by DAG-003's `SOURCE_MANIFEST.sha256`. ASC-ISS-006 is applied.

**Readiness.** `ReadyForNextPhase` is `NOT_APPLICABLE`; no record claims
`PUBLICATION_GATED`.

## Pass 7 — KTY Content Remediation Verification

NOT_APPLICABLE: SOFTWARE variant; no `KTY_Remediation_Manifest.csv`;
`ContentRemediationState` `NOT_REQUIRED`. No `.Archive/` input surfaces exist.

## Readiness reconciliation

| Claim | Where | Reconciled with |
|---|---|---|
| SCA-V4-001 closure verdict `OPEN_PENDING_DERIVATIVE_CLOSURE`; `DerivativePackageState` INCOMPLETE; `DownstreamRerunState` IN_PROGRESS | the accepted `Handoff_State.md` as restated by `EFFECTIVE_STATE.md`; `_ScopeChange/_LATEST.md` "Accepted predecessor" | **Consistent.** The record lists the completed reruns and the two deferred ones; INCOMPLETE and IN_PROGRESS hold for Coverage_Telemetry and the Design re-pins. ASC-ISS-003 is closed |
| "ASC-ISS-001 closes on this acceptance, to be confirmed by a superseding audit-scope-closure snapshot for SCA-V4-001" | DECISION-3 "Effects"; SCA-V4-002 Handoff_State; `_ScopeChange/_LATEST.md` | **Confirmed by this snapshot** (Pass 6) |
| "INCREMENTAL SCA-V4-001 setup COMPLETE" | `SETUP_LOG.md` | **Consistent** |
| DAG-003 "CURRENT; no deliverable is DAG pending" | `_Evaluation/DAGCurrency/_LATEST.md` | **Reproduced** (manifests and strict audit rerun) |
| "No release, publication or reliance claim" | `_ScopeChange/_LATEST.md`, `EFFECTIVE_STATE.md` | **Consistent** |

## Closure Determination

| Severity | Count | Findings |
|---|---|---|
| CRITICAL | 0 | — |
| MAJOR | 0 | — |
| MINOR | 0 | — |
| OBSERVATION | 10 | ASC-ISS-001 (closed), 002 (applied), 003 (recorded), 004 (DEFERRED_BY_HUMAN), 005 (DEFERRED_BY_HUMAN), 006 (applied), 007 (applied; SWBPIPE line carried), 008 (applied), 009 (unchanged), 010 (DAG-002 superseded by DAG-003) |

Uncertainty is recorded separately from severity: 10 DETERMINATE, 0 UNKNOWN.
The two CA1 items that were UNKNOWN are now determinate: the owner ruled
ASC-ISS-001 and confirmed the ASC-ISS-005 deferral record; ASC-ISS-002 and
ASC-ISS-006 were applied by accepted edits rather than interpreted.

**Status: CLOSED_WITH_OBSERVATIONS.** All required checks are complete; zero
CRITICAL or MAJOR; observations only. This status does not claim that the
deferred obligations are complete:
- `_Decomposition/Coverage_Telemetry.json` rebuild (DECISION-8 answer 2);
- the 17 Design re-pins (DECISION-8; DECISION-2 Q-15).

It accepts nothing and makes no release, publication or reliance claim.

## Recommendations

1. **ASC-ISS-004 and ASC-ISS-005 (deferred).** Keep the owner's sequencing:
   rebuild `Coverage_Telemetry.json` once, after SCA-V4-002, by the
   decomposition owner's bounded brief, then rerun audit-decomp to close
   COV-119/120; re-pin the 17 Design files once, against the SCA-V4-002
   revised SoWs, GUIDE (DEL-03-04) last.
2. **ASC-ISS-009.** At SCA-V4-002's incremental setup, append its SETUP_LOG
   line with the Phase 5.7 report and Phase 3.1 refresh; nothing is owed for
   SCA-V4-001.
3. **ASC-ISS-007.** Carry the `HANDOFF_SWBPIPE_DOMAINS.md` line 22 wording
   with the next relay, as accepted.
4. **SCA-V4-002's own closure audit** (outside this scope) should note that
   8 of the 18 SCA-V4-001-era registers (DEL-03-01, -03-02, -03-04, -05-01,
   -05-02, -08-01, -09-06, -09-09) bind `SOFTWARE_DECOMP.md` at `7434058…`,
   the pre-B-04 hash; the only difference is the appended SCA-V4-002 Decision
   Log entry, and DAG-003 binds the registers themselves at current hashes.

**Rerun requirements.**
- **No rerun is required for SCA-V4-001:** the 16 REVISEs, the 18
  extractions, DAG-002 (superseded in the ordinary way by DAG-003), the
  POSTACCEPT audit-decomp and `Consolidated_Coverage.csv` are bound to the
  amended basis by hash and reproduced here.
- **Still required, as deferred work:** (i) the Coverage_Telemetry rebuild,
  then audit-decomp; (ii) the Design re-pins at the next design pass.
- **This audit** need not be rerun for SCA-V4-001 unless an input in
  `INPUT_MANIFEST.sha256` changes; the SCA-V4-002 closure audit is a separate
  run.
