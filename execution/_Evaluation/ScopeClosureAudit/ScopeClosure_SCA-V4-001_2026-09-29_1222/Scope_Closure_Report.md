# Scope Closure Audit — SCA-V4-001

**Audit Date:** 2026-09-29
**Closure Status:** OPEN
**Amendment Date:** groups 1 and 2 accepted 2026-09-28 (DECISION-7); group 3 accepted 2026-09-29 (DECISION-8); snapshot folder `SCA-V4-001_2026-09-28_2155`
**Amendment Description:** App v4 basis alignment for owner decisions DEC-4 and DEC-5 (run `APP-V4-BASIS-ALIGN-20260928`):
- phased checkpoints (V4-WF-05);
- model access by OAuth sign-in or an API key, with no default (V4-HOST-01, V4-ARC-11);
- host-agent network destinations (V4-HOST-02, V4-ARC-12, V4-HI-70);
- "local-first" amended.

It makes 47 `MODIFY` actions and leaves the topology unchanged: 11 packages, 41 deliverables and 262 scope IDs.

**Auditor:** node CA1, run `APP-V4-SCA002-20260929`, a Type 2 TASK (Claude Code subagent). It did not delegate and wrote none of the audited files. Basis commit `102f09c1a`; git read-only; no network.

**Verdict.** The amendment's substance is implemented, and its required
reruns are done:
- all 47 actions are verified byte for byte against the accepted packet;
- the 16 SoW REVISEs, the 18 dependency re-extractions, and DAG-002 with its
  follow-up currency audit bind the amended basis by hash;
- no orphan exists, and no lifecycle state changed.

The status is **OPEN** because of one finding, ASC-ISS-001. Eleven actions
declare `SupersessionBindingPresent = YES` without their own
`Supersession_Delta.csv` row.
- **Severity:** the method rates this CRITICAL. Here that severity is
  **provisional**, and the finding carries `Assessment: UNKNOWN`.
- **Why it is uncertain:** the owner accepted, together with the register,
  an 11-row delta that covers those actions only in free-text Notes.
- **Who decides:** that conflict is for human triage.

If the owner rules the Notes coverage sufficient, the status becomes
`CLOSED_WITH_OBSERVATIONS`. Either way, two items stay open as deferred work:
Coverage_Telemetry and the Design re-pins.

## Amendment Summary

**Register.** `_ScopeChange/SCA-V4-001_2026-09-28_2155/Amendment_Actions.csv`,
SHA-256 `069645d979efa1e0a20f50194acca08afa8715ce647f36ad507c5bf2b76f14d2`.
- **How it was resolved:** the amendment-qualified pointer
  `SCA-V4-001_GROUP-2_AUTHORIZED.md` leads to
  `checkpoint_snapshots/SCA-V4-001_GROUP-2_2026-09-28/ACCEPTED_MANIFEST.csv`.
  That manifest has exactly one `Amendment_Actions*.csv` row, with role
  `action register`, and its hash was verified.
- **Not used:** `Intake_Actions.csv`, which is group-1 evidence.
- **Fallback:** none was needed.

| Property | Value |
|---|---|
| Rows | 47, all `MODIFY` |
| `ScopeChanging` | `YES` on 30 |
| `SupersessionBindingPresent` | `YES` on 22 (1, 2, 3, 6, 8, 9, 10, 12, 15, 16, 18–26, 36, 42, 46) |
| Rows 1–17 | the four basis documents (BASIS_AMENDMENT Part A) |
| Rows 18–31 | the decomposition package (Part B) |
| Rows 32–47 | 16 `ScopeOfWork.md` contracts (SOW_REVISIONS), routed `project-setup(INCREMENTAL);scope-of-work(REVISE)` |
| Row-to-edit crosswalk | Handoff_State "Crosswalk" (rows 7, 11, 17, 30, 31) |

**Handoff records read (Pass 0.7):**
- the snapshot's `Handoff_State.md`, finalized after DECISION-8;
- the checkpoint-group `Handoff_State.md` files (groups 1–3);
- `_PostAcceptanceValidation/SCA-V4-001_20260929T132946Z/` (43/43 PASS);
- `_ScopeChange/_LATEST.md`.

No later closeout or effective-state record exists under `_ScopeChange/`.
Dispositions come from DECISION-8, as recorded in the group-3 `DECISION.md`
and the accepted Handoff_State.

**Manifests.**
- **Group 1 (8 rows) and group 2 (9 rows):** every row equals its current
  bytes, except `OWNER_DECISIONS.md`. That file changed only because
  DECISION-8…10 were appended to it later.
- **Group 3 (36 rows):** the rows that changed are exactly the post-act
  H-1…H-4 targets and the finalized snapshot records. Its DECISION.md
  expects this, and V13 F1 covers the manifest label.
- **Pointers:** the pointer hash prefixes match the snapshot files.
- **Recency:** the amendment date is not in the future, so recency is
  context only.

## Pass 1 — Action Verification

**Method.**
- **Part A and D-15/D-16:**
  1. Parse the old→new blocks of `BASIS_AMENDMENT.md` (`04bdc916…24cf`).
  2. Fill the tokens: `SCA-V4-001`, `2026-09-29` and `SCA-V4-001_2026-09-28_2155`.
  3. Apply the blocks to the preimage at `f4ba34c2c`; each old block matches
     exactly once.
  4. Compare the result with the current file.
- **Part B:** check each field or substring against the current CSV, and each
  B7 mirror against the current `_CONTEXT.md`.
- **SoWs:** apply each deliverable's E-blocks from `SOW_REVISIONS.md`
  (`9b4d700d…7d27b`; 162 pairs) to its SoW at `a0af39f8c`, and compare the
  result with the current file. The prior hash at `a0af39f8c` equals the
  packet summary in 16/16 cases.
- **Scripts:** `verify_pass1.py` (`3291e34f…`) and `verify_partB.py`
  (`03aeb822…`), in the session scratchpad `CA1/`.

| ActionSeq | ActionType | EntityID | Expected | Actual | Status |
|---|---|---|---|---|---|
| 1 | MODIFY | docs/PRD.md#V4-WF-05 | A01 applied to `PRD.md` | Packet reconstruction from preimage `f4ba34c2c` equals current file byte for byte | VERIFIED |
| 2 | MODIFY | docs/PRD.md#V4-HOST-01 | A02/A03 applied to `PRD.md` | Packet reconstruction from preimage `f4ba34c2c` equals current file byte for byte | VERIFIED |
| 3 | MODIFY | docs/PRD.md#V4-HOST-02 | A02/A03 applied to `PRD.md` | Packet reconstruction from preimage `f4ba34c2c` equals current file byte for byte | VERIFIED |
| 4 | MODIFY | docs/PRD.md#2.2 | A04 applied to `PRD.md` | Packet reconstruction from preimage `f4ba34c2c` equals current file byte for byte | VERIFIED |
| 5 | MODIFY | docs/PRD.md#OQ-03 | A05 applied to `PRD.md` | Packet reconstruction from preimage `f4ba34c2c` equals current file byte for byte | VERIFIED |
| 6 | MODIFY | docs/PRD.md#1.1 | A06 applied to `PRD.md` | Packet reconstruction from preimage `f4ba34c2c` equals current file byte for byte | VERIFIED |
| 7 | MODIFY | docs/PRD.md#status | A07 (3 pairs; H-1) applied to `PRD.md` | Packet reconstruction from preimage `f4ba34c2c` equals current file byte for byte | VERIFIED |
| 8 | MODIFY | docs/ARCHITECTURE.md#V4-ARC-11 | A08/A09 applied to `ARCHITECTURE.md` | Packet reconstruction from preimage `f4ba34c2c` equals current file byte for byte | VERIFIED |
| 9 | MODIFY | docs/ARCHITECTURE.md#V4-ARC-12 | A08/A09 applied to `ARCHITECTURE.md` | Packet reconstruction from preimage `f4ba34c2c` equals current file byte for byte | VERIFIED |
| 10 | MODIFY | docs/ARCHITECTURE.md#host-agent-properties | A10 applied to `ARCHITECTURE.md` | Packet reconstruction from preimage `f4ba34c2c` equals current file byte for byte | VERIFIED |
| 11 | MODIFY | docs/ARCHITECTURE.md#1 | A11a+A11b applied to `ARCHITECTURE.md` | Packet reconstruction from preimage `f4ba34c2c` equals current file byte for byte | VERIFIED |
| 12 | MODIFY | docs/HOST_INTEGRATION.md#V4-HI-42 | A12 applied to `HOST_INTEGRATION.md` | Packet reconstruction from preimage `f4ba34c2c` equals current file byte for byte | VERIFIED |
| 13 | MODIFY | docs/HOST_INTEGRATION.md#8.1 | A13 applied to `HOST_INTEGRATION.md` | Packet reconstruction from preimage `f4ba34c2c` equals current file byte for byte | VERIFIED |
| 14 | MODIFY | docs/HOST_INTEGRATION.md#V4-HI-70 | A14 applied to `HOST_INTEGRATION.md` | Packet reconstruction from preimage `f4ba34c2c` equals current file byte for byte | VERIFIED |
| 15 | MODIFY | docs/EXAMINATION.md#V4-EXM-22 | A15 applied to `EXAMINATION.md` | Packet reconstruction from preimage `f4ba34c2c` equals current file byte for byte | VERIFIED |
| 16 | MODIFY | docs/EXAMINATION.md#V4-EXM-23 | A16 applied to `EXAMINATION.md` | Packet reconstruction from preimage `f4ba34c2c` equals current file byte for byte | VERIFIED |
| 17 | MODIFY | docs/*.md#status | A17a-c (H-2) applied to `ARCHITECTURE/HOST_INTEGRATION/EXAMINATION` | Packet reconstruction from preimage `f4ba34c2c` equals current file byte for byte | VERIFIED |
| 18 | MODIFY | SOW-015 | D-01 field value | Current field equals the packet new value; old value absent | VERIFIED |
| 19 | MODIFY | SOW-016 | D-02 field value | Current field equals the packet new value; old value absent | VERIFIED |
| 20 | MODIFY | SOW-017 | D-03 field value | Current field equals the packet new value; old value absent | VERIFIED |
| 21 | MODIFY | SOW-052 | D-04 field value | Current field equals the packet new value; old value absent | VERIFIED |
| 22 | MODIFY | SOW-137 | D-05 field value | Current field equals the packet new value; old value absent | VERIFIED |
| 23 | MODIFY | SOW-138 | D-06 field value | Current field equals the packet new value; old value absent | VERIFIED |
| 24 | MODIFY | SOW-201 | D-07 field value | Current field equals the packet new value; old value absent | VERIFIED |
| 25 | MODIFY | SOW-202 | D-08 field value | Current field equals the packet new value; old value absent | VERIFIED |
| 26 | MODIFY | Declared checkpoint | D-09 field value | Current field equals the packet new value; old value absent | VERIFIED |
| 27 | MODIFY | PKG-05 | D-13 (+B7 DEL-05-01/05-02) field value | Current field equals the packet new value; old value absent; B7 mirrors match | VERIFIED |
| 28 | MODIFY | OI-001 | D-14a (Status OPEN) field value | Current field equals the packet new value; old value absent | VERIFIED |
| 29 | MODIFY | OI-002 | D-14b (Status OPEN) field value | Current field equals the packet new value; old value absent | VERIFIED |
| 30 | MODIFY | SOFTWARE_DECOMP.md#decision-log | D-16 + D-15 (H-3) | Reconstruction equals current `SOFTWARE_DECOMP.md` (`7434058…7e5747`); `## Decision Log` entry names SCA-V4-001, 2026-09-29 and the snapshot | VERIFIED |
| 31 | MODIFY | Consolidated_Coverage.csv | B8 x2 (H-4) | 144/144 rows re-derived: SHA256, git blob and SourceLine match current documents; Standing "amended by SCA-V4-001" on the 9 named IDs | VERIFIED |
| 32 | MODIFY | DEL-04-01 | DEL-04-01 ScopeOfWork.md per SOW_REVISIONS (13 pairs) | Prior `fc1a0503…` = packet summary; applying the E-blocks reproduces current `ac043e54…` byte for byte; 0 unfilled tokens; validate_scope_of_work PASS, boundary check exit 0 | VERIFIED |
| 33 | MODIFY | DEL-04-02 | DEL-04-02 ScopeOfWork.md per SOW_REVISIONS (10 pairs) | Prior `23a28caa…` = packet summary; applying the E-blocks reproduces current `e077f20a…` byte for byte; 0 unfilled tokens; validate_scope_of_work PASS, boundary check exit 0 | VERIFIED |
| 34 | MODIFY | DEL-04-03 | DEL-04-03 ScopeOfWork.md per SOW_REVISIONS (6 pairs) | Prior `74d42c38…` = packet summary; applying the E-blocks reproduces current `ceecddbb…` byte for byte; 0 unfilled tokens; validate_scope_of_work PASS, boundary check exit 0 | VERIFIED |
| 35 | MODIFY | DEL-02-01 | DEL-02-01 ScopeOfWork.md per SOW_REVISIONS (9 pairs) | Prior `080d7f5a…` = packet summary; applying the E-blocks reproduces current `6ccc860b…` byte for byte; 0 unfilled tokens; validate_scope_of_work PASS, boundary check exit 0 | VERIFIED |
| 36 | MODIFY | DEL-02-03 | DEL-02-03 ScopeOfWork.md per SOW_REVISIONS (14 pairs) + D-10a/b in Deliverables.csv and _CONTEXT.md | Prior `9a921ba5…` = packet summary; applying the E-blocks reproduces current `a4ffcd87…` byte for byte; 0 unfilled tokens; validate_scope_of_work PASS, boundary check exit 0; mirrors match | VERIFIED |
| 37 | MODIFY | DEL-03-01 | DEL-03-01 ScopeOfWork.md per SOW_REVISIONS (9 pairs) | Prior `179a6d35…` = packet summary; applying the E-blocks reproduces current `9ada531b…` byte for byte; 0 unfilled tokens; validate_scope_of_work PASS, boundary check exit 0 | VERIFIED |
| 38 | MODIFY | DEL-03-02 | DEL-03-02 ScopeOfWork.md per SOW_REVISIONS (10 pairs) | Prior `42328987…` = packet summary; applying the E-blocks reproduces current `35609151…` byte for byte; 0 unfilled tokens; validate_scope_of_work PASS, boundary check exit 0 | VERIFIED |
| 39 | MODIFY | DEL-03-03 | DEL-03-03 ScopeOfWork.md per SOW_REVISIONS (10 pairs) | Prior `5ac5db97…` = packet summary; applying the E-blocks reproduces current `fdd22e25…` byte for byte; 0 unfilled tokens; validate_scope_of_work PASS, boundary check exit 0 | VERIFIED |
| 40 | MODIFY | DEL-03-04 | DEL-03-04 ScopeOfWork.md per SOW_REVISIONS (10 pairs) | Prior `203c0928…` = packet summary; applying the E-blocks reproduces current `895f004e…` byte for byte; 0 unfilled tokens; validate_scope_of_work PASS, boundary check exit 0 | VERIFIED |
| 41 | MODIFY | DEL-01-01 | DEL-01-01 ScopeOfWork.md per SOW_REVISIONS (4 pairs) | Prior `eddd122c…` = packet summary; applying the E-blocks reproduces current `f65dc666…` byte for byte; 0 unfilled tokens; validate_scope_of_work PASS, boundary check exit 0 | VERIFIED |
| 42 | MODIFY | DEL-05-01 | DEL-05-01 ScopeOfWork.md per SOW_REVISIONS (19 pairs) + D-11a-d in Deliverables.csv and _CONTEXT.md | Prior `6fbbb580…` = packet summary; applying the E-blocks reproduces current `9b2379a1…` byte for byte; 0 unfilled tokens; validate_scope_of_work PASS, boundary check exit 0; mirrors match | VERIFIED |
| 43 | MODIFY | DEL-05-02 | DEL-05-02 ScopeOfWork.md per SOW_REVISIONS (16 pairs) + D-13 in _CONTEXT.md | Prior `5c554956…` = packet summary; applying the E-blocks reproduces current `beb9c66c…` byte for byte; 0 unfilled tokens; validate_scope_of_work PASS, boundary check exit 0; mirrors match | VERIFIED |
| 44 | MODIFY | DEL-09-06 | DEL-09-06 ScopeOfWork.md per SOW_REVISIONS (11 pairs) | Prior `511f2c00…` = packet summary; applying the E-blocks reproduces current `287d47a1…` byte for byte; 0 unfilled tokens; validate_scope_of_work PASS, boundary check exit 0 | VERIFIED |
| 45 | MODIFY | DEL-09-09 | DEL-09-09 ScopeOfWork.md per SOW_REVISIONS (8 pairs) | Prior `082db8fa…` = packet summary; applying the E-blocks reproduces current `e887a579…` byte for byte; 0 unfilled tokens; validate_scope_of_work PASS, boundary check exit 0 | VERIFIED |
| 46 | MODIFY | DEL-09-07 | DEL-09-07 ScopeOfWork.md per SOW_REVISIONS (11 pairs) + D-12a-c in Deliverables.csv and _CONTEXT.md | Prior `36cc2e24…` = packet summary; applying the E-blocks reproduces current `53b51d30…` byte for byte; 0 unfilled tokens; validate_scope_of_work PASS, boundary check exit 0; mirrors match | VERIFIED |
| 47 | MODIFY | DEL-08-01 | DEL-08-01 ScopeOfWork.md per SOW_REVISIONS (2 pairs) | Prior `581b399f…` = packet summary; applying the E-blocks reproduces current `df279586…` byte for byte; 0 unfilled tokens; validate_scope_of_work PASS, boundary check exit 0 | VERIFIED |

**Result:** 47/47 VERIFIED; 0 DISCREPANCY; 0 NOT_EXECUTED.
- **Part A:** all 5 reconstructed files equal their current bytes. These are
  the H-1…H-3 result hashes in Handoff_State.
- **SoWs:** the 16 reconstructions are all byte-equal.
- **Part B:** all 21 packet rows and all 11 B7 mirrors hold.
- **Conditional rows:** O-8, O-17, O-18 and O-19 were accepted, so rows 6,
  27–29, 46 and 47 should be applied, and they are.
- **Open_Issues:** OI-001/002 `Status` stays OPEN, as accepted.

## Pass 2 — Downstream Rerun Verification

**Sources:**
- the register's `DownstreamReruns` column;
- `RUN_SUMMARY.md` "Open downstream work";
- `Propagation_Plan.md` §5–§7;
- the group-3 DECISION.md.

| Agent / workflow | Scope | Evidence | Status |
|---|---|---|---|
| `audit-decomp` (register rows 1–3, 8, 9, 12, 15, 16, 18–25, 31) | the seven baseline packages (O-20) | See **audit-decomp evidence** below | COMPLETED |
| `project-setup` INCREMENTAL → `scope-of-work` REVISE + VERIFY (rows 32–47) | 16 deliverables, one per brief | See **SoW REVISE evidence** below | COMPLETED |
| `dependency-extract` UPDATE (Propagation_Plan §5; DECISION-9 FULL_GRAPH refresh) | the 16, plus neighbours DEL-01-04 and DEL-02-02 | See **dependency-extract evidence** below | COMPLETED |
| `project-dag` currency audit → DAG-002 successor (checkpoint C) | full graph | See **DAG-002 evidence** below | COMPLETED |
| `Coverage_Telemetry.json` RECOMPUTE | the decomposition owner | Unchanged at `178ec20a…`. DECISION-8 answer 2: "Record as stale, fix later (Recommended)" | DEFERRED_BY_HUMAN (ASC-ISS-004) |
| Design re-pins | App v4 design undertaking | 17 Design files still pin superseded hashes (list below). The group-3 accepted Handoff_State says "at the next design pass" | DEFERRED_BY_HUMAN (ASC-ISS-005; the deferral basis is UNKNOWN) |

**audit-decomp evidence.**
- **Runs:** `POSTCHANGE/` and `POSTACCEPT/`.
- **Binding:** POSTACCEPT `coverage_summary.json` binds four current files:
  - `SOFTWARE_DECOMP.md` `7434058…`;
  - `ScopeLedger.csv` `d8136297…`;
  - `Deliverables.csv` `2480cbef…`;
  - `Consolidated_Coverage.csv` `4eee4bcb…`, which carries the current
    hashes of all four documents.
- **Result:** 0 BLOCKER, 38 WARNING and 94 INFO. Forward, reverse and
  objective coverage stay 100 %. The Change Register part of COV-131 is
  closed.
- **Reproduced:** V13 reproduced it byte for byte.

**SoW REVISE evidence.**
- **Returns:** each `RV/RV-1…4_*.md` binds the prior hash (equal to the
  packet), the full current SoW hash and a VERIFY PASS.
- **Reconstruction:** this audit's independent reconstruction is byte-equal
  (Pass 1).
- **Validators, rerun here:** `validate_scope_of_work.py` gives PASS
  (`SOW_V1`) on all 16, and `check_boundary_owner_resolution.py` exits 0 on
  all 16.
- **Lifecycle:** no `_STATUS.md` changed since `67a2fac4b` (41/41).
- **Independent check:** V12 §1 verified the revisions independently.

**dependency-extract evidence.**
- **Run records:** all 18 `_run_records/dependency-extract-20260929.md`
  files bind the post-change hashes: the full current `ScopeOfWork.md` hash,
  `SOFTWARE_DECOMP.md` `7434058…` and `ScopeLedger.csv` `d8136297…`. The DX
  returns agree.
- **Anchor rows:** the rows on the 8 amended ledger IDs carry the current
  ScopeLedger statements (8/8).
- **Closure snapshot:**
  `_Evaluation/DepClosure/CLOSURE_APP_V4_BASISALIGN_2026-09-29_0855`.
- **Quote fidelity:** see ASC-ISS-008.

**DAG-002 evidence.**
- **Acceptance:** DAG-002 was accepted under DECISION-10
  (`_DAG/DAG-002/ACCEPTANCE_RECORD.md`), and `_DAG/_LATEST.md` reads
  `Latest: DAG-002`.
- **Rerun here:**
  - `SOURCE_MANIFEST.sha256`: 130/130 OK. It binds the 16 revised SoWs and
    the 18 registers at their current hashes;
  - `MANIFEST.sha256`: 37/37 OK;
  - DAG-001 `MANIFEST.sha256`: 61/61 OK;
  - `audit_dag.py --canonical --strict`: exit 0.
- **Analyzer:** `analyze_dep_closure.py` (`2b8de3cb…`), run with the
  recorded arguments, gives `NO_DEPARTURE_FOUND`, 0 DAG pending and 41
  registers. Its stdout is byte-identical to the follow-up currency audit's
  `analyzer.stdout.json` (`CURRENCY_APP_V4_DAG002_ACCEPTED_2026-09-29_1050`).

**Not counted as reruns:**
- this audit (`audit-scope-closure`);
- SCA-V4-002 and the SWBPIPE relay note. Both are residuals outside
  SCA-V4-001 (DECISION-8 answer 3).

**SETUP_LOG.** `_Coordination/SETUP_LOG.md` line 6 reads:

> "[2026-09-29] — INCREMENTAL SCA-V4-001 setup COMPLETE; run record `AgentRuns/APP-V4-BASIS-ALIGN-20260928/` …"

- **Form:** it follows the contract form
  `INCREMENTAL [ID] setup COMPLETE; run record [path]`.
- **COMPLETE is supported:** every DECISION-9 plan item is evidenced above:
  - REVISE and VERIFY for all 16;
  - extraction for all 18;
  - the closure and currency audits;
  - the DAG-002 candidate and its acceptance.
- **Process gap:** the Phase 5.7 report and the Phase 3.1 refresh artifacts
  are absent (ASC-ISS-009, OBSERVATION).

**The 17 stale Design files.** Each pins one or both of the following:
- superseded basis-document hashes: PRD `657593ce`, ARCHITECTURE
  `c3ae766e`, HOST_INTEGRATION `08c8fc7d` (HI) or EXAMINATION `1b156553`;
- its own deliverable's pre-revision SoW hash.

Where a file pins basis documents, they are named in brackets:
- DEL-01-01: `HOSTING_BOUNDARY.md`, `PIN_SPIKE_0.158.0.md`;
- DEL-02-01: `EXAMPLES.md`, `WORKFLOW_DECLARATION.md`;
- DEL-02-03: `EXECUTION_COMPATIBILITY.md`;
- DEL-03-01: `CATALOG_AND_READ_BASIS.md` (HI);
- DEL-03-02: `PROPOSAL_LIFECYCLE_AND_OUTCOMES.md` (HI);
- DEL-03-03: `ADAPTER_ENABLEMENT_AND_RECEIVING.md` (PRD, ARCHITECTURE, HI, EXAMINATION);
- DEL-03-04: `HOST_INTEGRATION_GUIDE.md` (HI);
- DEL-04-01: `ACT_AND_POLICY_CONTRACT.md`;
- DEL-04-02: `AUTONOMY_AND_STANDING_EXCHANGE.md`;
- DEL-04-03: `RECORD_SEMANTICS.md`;
- DEL-05-01: `LOOP_RECEIVING_CONTRACT.md`;
- DEL-05-02: `PANEL_RECEIVING_CONTRACT.md`;
- DEL-09-06: `CONNECTED_ACTIVITY_CONTRACT.md` and `RELAY_QUESTIONS_SWBPIPE.md` (PRD, HI, EXAMINATION);
- DEL-09-09: `EXTERNAL_TRACE_CASES.md` (PRD, HI, EXAMINATION).

None pins the amended hashes. The count of 17 matches Handoff_State.

## Pass 3 — Orphaned References

The amendment has no `REMOVE`, `MERGE`, `SPLIT` or `RECLASSIFY` action, so
no entity ID is retired.
- **Scan:** all 41 `Dependencies.csv` files (822 rows), with
  `analyze_dep_closure.py`: `orphan_count` 0, `implements_node_missing` 0,
  and 0 schema-invalid registers.
- **Names:** no deliverable or package name changed, so no `TargetName` is
  stale.
- **Anchor rows:** the rows on the amended ledger IDs carry the amended
  statements.

No orphaned references were detected.

**Residual wording outside the register** (ASC-ISS-007, OBSERVATION):
- DEL-10-03 REQ-005, routed to SCA-V4-002;
- `HANDOFF_SWBPIPE_DOMAINS.md` line 22, carried to the next relay;
- `Allocation_Rationale.csv`, NO_CHANGE as accepted;
- the DEP-09-07-016 Notes.

## Pass 4 — Decomposition Consistency

The variant is SOFTWARE, so the DOMAIN integrity validator does not apply.

1. **Change Log.** The `## Decision Log` section of `SOFTWARE_DECOMP.md`
   holds the entry "SCA-V4-001 (2026-09-29) … Snapshot:
   `../_ScopeChange/SCA-V4-001_2026-09-28_2155`" (H-3, D-15). It binds at
   rank exact (POSTACCEPT). D-16 was applied.
2. **Scope Ledger.**
   - SOW-015, -016, -017, -052, -137, -138, -201 and -202 carry the amended
     statements.
   - Their `DecisionRef` values are
     `APP-V4-BASIS-20260926;{DECISION};SCA-V4-001`.
   - No mapping, count or status changed. The totals are IN 234, OUT 15 and
     TBD 13, as in the baseline.
3. **Packages.** None was added or removed. The PKG-05 description is
   amended (D-13).
4. **Deliverables.** DEL-02-03, DEL-05-01 and DEL-09-07 are amended
   (D-10…D-12). One unamended row keeps a phrase that the amendment treated
   as superseded elsewhere: DEL-04-01, "PKG-02 checkpoints override autonomy"
   (**ASC-ISS-002**, MINOR, UNKNOWN).
5. **Coverage.** Compared across `Pre_Change_Coverage.json` (= BASELINE),
   `Post_Change_Coverage.json` (= POSTCHANGE) and POSTACCEPT:
   - forward coverage (partitions and production units), reverse coverage
     and objective coverage are 100 % throughout;
   - there are no new unassigned scope items;
   - WARNING rose from 2 to 38. That is attributed to the DECISION-6
     lifecycle (37, Check 6) and to residual COV-131 (pre-existing heading
     bindings);
   - COV-119/120 stay open with Coverage_Telemetry (ASC-ISS-004).

   No regression is attributable to the amendment.

## Pass 5 — Context Metadata Consistency

**`_CONTEXT.md`.** All 41 files were checked, not only the 16 affected,
against `Deliverables.csv` and `Packages.csv`. The fields checked were:
- Name, Description, Type and ResponsibleParty;
- AnticipatedArtifacts, CoversScopeItems and SupportsObjectives;
- ScopeDescription.

There are 0 mismatches, so the B7 mirrors are complete and no other mirror
drifted.

**`_STATUS.md`.**
- Among the 16 affected deliverables: 14 IN_PROGRESS, and 2 INITIALIZED
  (DEL-09-07, DEL-08-01).
- Overall: 27 INITIALIZED and 14 IN_PROGRESS.
- Every `_STATUS.md` is byte-unchanged since `67a2fac4b` (DECISION-6).
- No deliverable is CHECKING or ISSUED, so no reopening applies.

**Basis lines.** Every `_CONTEXT.md` names `GROUP3-20260928T001055Z` as its
accepted basis and does not mention the active amendment (ASC-ISS-006,
OBSERVATION).

## Pass 6 — Supersession Binding Completeness

This pass ran because 22 register rows have
`SupersessionBindingPresent = YES`.

1. **D-{ActionSeq} derivation: 11 of 22 match.**
   - **With their own row:** D-001, 002, 003, 006, 008, 009, 010, 012, 015,
     016 and 026.
   - **With no own row:** actions 18, 19, 20, 21, 22, 23, 24, 25, 36, 42
     and 46.
   - **Where those 11 are named instead:** only in the Notes of other rows:
     D-001 (21, 36), D-002 (18, 19, 42), D-003 (20, 42, 46), D-009 (22, 23),
     D-015 (24, 46) and D-016 (25).
   - **Missing authority paths:** no row names the GROUP3 canonical
     `ScopeLedger.csv` or `Deliverables.csv` as `SupersededAuthorityPath`.
     The ScopeLedger authority appears only as free text in
     `SupersededAuthorityRef`, and the Deliverables.csv authority only in
     Notes.
   - **Finding:** **ASC-ISS-001**, CRITICAL (provisional, from the method
     table), with `Assessment: UNKNOWN`.
   - **Both sides of the conflict:**
     - the method and the scope-change contract require one D-0NN row per
       YES action;
     - the accepted group-2 record (DECISION-7) binds this 11-row delta
       together with the 22-YES register, and V11 §3 accepted the Notes
       convention.

     This audit does not choose between them.
2. **Authority paths.** All 11 `SupersededAuthorityPath` values resolve.
   - **Original facts:** each occurs, whitespace-normalized, in its
     authority file: the original seed for D-001…D-016, and the GROUP3
     canonical `Vocabulary_Map.csv` for D-026.
   - **Replacements:** each occurs in the current file. For D-006 this holds
     once blockquote markers are removed.
   - **Superseded text:** no original survives in the current files.
3. **References.** All 11 `SupersededAuthorityRef` values are non-empty, and
   every row is `SUPERSESSION`.
4. **Accumulator.** This is the first amendment, so there is no prior map.
   - **Run:** `accumulate_supersession_map.py` (`d967144d…`) with `--delta`,
     `--check-map` and `--output-findings`.
   - **Result:** 11 rows and 0 findings.
   - **Map:** `Expected_Supersession_Map.csv` is byte-identical to the
     snapshot's `Supersession_Map.csv`.
5. **Applicability.** `AppliesToRoots`, `AppliesToFacilities` and
   `AppliesToSections` are blank on every row. That means global scope,
   which is valid for a SOFTWARE decomposition with no roots or facilities.

**Visibility.**
- The decomposition pointer `checkpoint_snapshots/_LATEST_ACCEPTED.md` names
  GROUP3 only.
- `_Decomposition/_LATEST.md` reads `Latest: (none)`.
- The only route to the active supersession is `_ScopeChange/_LATEST.md`
  (ASC-ISS-006).

**Readiness.** `ReadyForNextPhase` is `NOT_APPLICABLE`, and no record claims
`PUBLICATION_GATED`. So no readiness claim conflicts with ASC-ISS-001.

## Pass 7 — KTY Content Remediation Verification

NOT_APPLICABLE:
- the variant is SOFTWARE;
- there is no `KTY_Remediation_Manifest.csv`;
- no KTY-local content impact is recorded (Handoff_State
  `ContentRemediationState` is `NOT_REQUIRED`).

There are no `.Archive/` input surfaces to inspect.

## Readiness reconciliation

| Claim | Where | Reconciled with |
|---|---|---|
| `OPEN_PENDING_DERIVATIVE_CLOSURE`; `DerivativePackageState` INCOMPLETE; `DownstreamRerunState` IN_PROGRESS | `_ScopeChange/_LATEST.md`, `Handoff_State.md`, `RUN_SUMMARY.md` | **Understated.** Three of the listed derivatives are now complete: the SoWs, the registers and DAG-002. Still open: Coverage_Telemetry, the Design re-pins, and this audit's ASC-ISS-001. There is no over-claim (ASC-ISS-003) |
| "SCA-V4-001's closure verdict is OPEN_PENDING_DERIVATIVE_CLOSURE. Still open: Coverage_Telemetry.json rebuild; audit-scope-closure; Design files re-pinning" | `RECEIPT.md` "Open", after the V13 F4 fix | **Consistent.** No record yet mentions ASC-ISS-001 |
| "for that derivative only" | DAG-002 `HANDOFF_STATE.md`; DECISION-8 Effects | **Understates the open set** (V13 F4). The DAG-002 copy is immutable and stays as written |
| "INCREMENTAL SCA-V4-001 setup COMPLETE" | `SETUP_LOG.md` | **Consistent.** Every plan item is evidenced |
| DAG-002 "CURRENT; nothing DAG pending" | `_Evaluation/DAGCurrency/_LATEST.md` | **Reproduced** |
| "No release, publication or reliance claim" | `_ScopeChange/_LATEST.md` | **Consistent.** None was found |

## Closure Determination

| Severity | Count | Findings |
|---|---|---|
| CRITICAL | 1 | ASC-ISS-001 (provisional; UNKNOWN) |
| MAJOR | 0 | — |
| MINOR | 2 | ASC-ISS-002 (UNKNOWN), ASC-ISS-003 |
| OBSERVATION | 6 | ASC-ISS-004 (DEFERRED_BY_HUMAN), ASC-ISS-005 (DEFERRED_BY_HUMAN; UNKNOWN), ASC-ISS-006 (UNKNOWN), ASC-ISS-007, ASC-ISS-008, ASC-ISS-009 |

Uncertainty is recorded separately from severity: 4 findings are UNKNOWN
and 5 are DETERMINATE.

**Status: OPEN.** One CRITICAL finding remains, and it alone determines the
status. All required checks are complete.

**Open work, whatever the status:**
- the Coverage_Telemetry.json rebuild (DECISION-8);
- the Design re-pins (17 files);
- SCA-V4-002 (DECISION-8 and DECISION-10).

## Recommendations

**1. ASC-ISS-001 (human triage first).** Decide whether the Notes-level
coverage of actions 18–25, 36, 42 and 46 satisfies the binding. Two routes:
- **(a) Bind them at path level through SCA-V4-002.**
  - SCA-V4-002 adds rows, for example `DL-{reference}` rows citing those
    SCA-V4-001 actions.
  - Each row names a GROUP3 canonical file as `SupersededAuthorityPath`:
    `ScopeLedger.csv` for SOW-015, -016, -017, -052, -137, -138, -201 and
    -202, or `Deliverables.csv` for the DEL-02-03, DEL-05-01 and DEL-09-07
    substrings.
  - Then re-accumulate the cumulative map, with `--prior-map` set to
    SCA-V4-001's map.
- **(b) Record an owner ruling** that accepts the convention for SCA-V4-001.
  Any change to the method or the contract is separate Root work.

Either way, the immutable SCA-V4-001 files stay as they are. Afterwards,
rerun this audit as a superseding snapshot.

**2. ASC-ISS-003.** After this audit, write a new SCA-V4-001 effective-state
or closeout record under `_ScopeChange/`. It should:
- record the four completed reruns with their hash-bearing evidence;
- cite this snapshot;
- list the items that remain open.

At the next pointer write, add the `Latest:`/`Updated:` lines (V13 F2).

**3. ASC-ISS-002.** In SCA-V4-002, propose a D-row for the DEL-04-01
description, with its `_CONTEXT.md` mirror. Alternatively, record that the
phrase stands.

**4. ASC-ISS-004 and ASC-ISS-005.** Sequence both after SCA-V4-002:
- **Coverage_Telemetry.json:** rebuild it once, through the bounded brief
  the owner directed, then run audit-decomp.
- **Design files:** re-pin them once, against SCA-V4-002's revised SoWs.
  Re-pin GUIDE last.

**5. ASC-ISS-006, -007, -008 and -009.** Fold these into SCA-V4-002:
- the reading-rule note, timed with DAG-003;
- a restatement of the DEP-09-07-016 Notes, when DEL-09-07 is re-extracted;
- exact re-quoting in DEL-04-01, DEL-04-02 and DEL-04-03;
- at its incremental setup: the Phase 5.7 report and the Phase 3.1 refresh,
  with `NO_STATUS_TOUCH`.

**Rerun requirements.**
- **No rerun is required for:**
  - the 16 SoW REVISEs, the 18 extractions, DAG-002 and its currency audit;
  - the POSTACCEPT audit-decomp and `Consolidated_Coverage.csv`.

  Each is bound to the current amended basis by hash, and the reruns here
  reproduce them.
- **Required:**
  - (i) this audit, as a superseding snapshot, after the ASC-ISS-001
    disposition and the ASC-ISS-003 record;
  - (ii) the Coverage_Telemetry rebuild, then audit-decomp, when the
    owner's brief issues;
  - (iii) the Design re-pins, at the next design pass.
- **When this snapshot goes stale:** this snapshot's `INPUT_MANIFEST.sha256`
  decides whether it is still current. Any SCA-V4-002 edit to a listed input
  makes it stale for those inputs.
