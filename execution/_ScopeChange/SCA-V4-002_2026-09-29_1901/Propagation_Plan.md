# SCA-V4-002 — Propagation plan

**Standing: accepted at checkpoint group 2 (owner DECISION-2 of run
`APP-V4-SCA002-20260929`, 2026-09-29), as transcribed after the act** from
the accepted packet revision 2: OWNER_ITEMS.md Q-3 (sha256 `1d46458c…51a8`),
IMPACT_ASSESSMENT.md §§6–8 and 10 (sha256 `46444eab…0456`), BASIS_AMENDMENT.md
(sha256 `091871fd…4238`) and ARC_EFFECT.md §4 (sha256 `4b3aeec0…ddc0`). Where
this file and the packet differ, the packet governs. Execution-stage readings
are recorded separately in `Decision_Log.md`, not here.

This file was written before any SCA-V4-002 edit was applied.

Variant `SOFTWARE`; posture `ACCEPTED_PREDECESSOR` (predecessor
`SCA-V4-001_2026-09-28_2155`). All 16 actions are `MODIFY`: no `ADD`,
`REMOVE`, `RECLASSIFY`, `MERGE` or `SPLIT`, so there is no parent-closure
set, no child-closure remap and no folder relocation.

## 1. Write boundary (Q-3, named exactly)

The `AffectedFiles` of the 16-row register
([Amendment_Actions.csv](Amendment_Actions.csv)):

- `projects/chirality-app-v4/docs/HOST_INTEGRATION.md` (row 10; A-01);
- `execution/_Decomposition/Consolidated_Coverage.csv` (row 11; B-01),
  `Open_Issues.csv` (row 12; B-02), `SOFTWARE_DECOMP.md` (row 13; B-04),
  `Deliverables.csv` (row 14; B-05a),
  `checkpoint_snapshots/_LATEST_ACCEPTED.md` and `_LATEST.md` (row 15;
  B-06a, B-06b);
- the `_CONTEXT.md` of DEL-04-01 (rows 14 and 16; B-05b, B-06c) and of
  DEL-02-03, DEL-05-01, DEL-05-02 and DEL-09-07 (row 16; B-06c);
- the nine `ScopeOfWork.md` files of rows 1–9 (DEL-10-03, 02-01, 02-03,
  09-07, 01-04, 02-02, 03-03, 04-02, 01-01), applied only by
  `scope-of-work` MODE=REVISE, one brief per deliverable, closing with
  MODE=VERIFY.

Plus the SCA-V4-002 snapshot folders and pointers under
`execution/_ScopeChange/`, which include the SCA-V4-001 effective-state
record (C-02) and, after group 3, `_ScopeChange/_LATEST.md` (C-01).

Nothing else.

**Application route (Q-3).** The docs, decomposition and `_CONTEXT.md` edits
go into the candidate. The SoWs change only after group 3, by REVISE, with
`STATUS_POLICY=NO_STATUS_TOUCH`. Then the register UPDATE, the currency audit
and DAG-003.

## 2. Package roles and direct writes

| Surface | Package role | Classification | Edits | When |
|---|---|---|---|---|
| `docs/HOST_INTEGRATION.md` | authoritative carrier named in the group-2 boundary | DIRECT_EDIT | A-01 | candidate |
| `_Decomposition/Consolidated_Coverage.csv` | authoritative companion register | RECOMPUTE | B-01: the 31 HOST_INTEGRATION rows take the new SHA256, git blob and `SourceLine` n + 1 | candidate |
| `_Decomposition/Open_Issues.csv` | authoritative companion register | DIRECT_EDIT (field) | B-02: OI-012 `Consequence`; `Status` stays OPEN. B-03: none | candidate |
| `_Decomposition/Deliverables.csv` | authoritative companion register | DIRECT_EDIT (substring) | B-05a | candidate |
| DEL-04-01 `_CONTEXT.md` | variant-local metadata (default propagation write) | DIRECT_EDIT | B-05b (mirror), B-06c | candidate |
| DEL-02-03, DEL-05-01, DEL-05-02, DEL-09-07 `_CONTEXT.md` | same | DIRECT_EDIT | B-06c | candidate |
| `_Decomposition/_LATEST.md` | snapshot / handoff artifact (pointer) | DIRECT_EDIT | B-06b | candidate |
| `_Decomposition/checkpoint_snapshots/_LATEST_ACCEPTED.md` | snapshot / handoff artifact (pointer) | DIRECT_EDIT | B-06a | **with the SoW REVISEs, after group 3** (the file is bound in `_DAG/DAG-002/SOURCE_MANIFEST.sha256`) |
| `_Decomposition/SOFTWARE_DECOMP.md` | working surface | DIRECT_EDIT | B-04 | **after group-3 acceptance** |
| `_ScopeChange/_LATEST.md` | snapshot / handoff artifact | pointer write | C-01 | **after group-3 acceptance** |
| `_ScopeChange/_PostAcceptanceValidation/SCA-V4-001_{UTC}_EFFECTIVE_STATE/EFFECTIVE_STATE.md` | snapshot / handoff artifact (new, append-only) | new file | C-02 | after group-1 acceptance |
| SCA-V4-002 `Supersession_Delta.csv`, `Supersession_Map.csv` | snapshot / handoff artifact | new files | Part D: 17 `DL-` rows and D-014; the map accumulated from SCA-V4-001's map | candidate |
| 9 `ScopeOfWork.md` | authoritative carrier; changed by REVISE after group 3 | handoff (not written in the candidate) | SOW_REVISIONS, 26 blocks | after group 3 |
| `_Decomposition/Coverage_Telemetry.json` | derived companion | RECOMPUTE, **open** (`STALE_REBUILD_REQUIRED`, carried) | none here | out of scope |

NO_CHANGE: `ScopeLedger.csv`, `Packages.csv`, `Vocabulary_Map.csv`,
`Objectives.csv`, `Allocation_Rationale.csv`, `Source_*.csv`,
`Scope_Classification.csv`, `ContextBudgetQA.csv`,
`External_Dependencies.csv`, `Companion_Inventory.csv`; `docs/PRD.md`,
`docs/ARCHITECTURE.md`, `docs/EXAMINATION.md`; every `_STATUS.md`.

## 3. Acceptance-conditional edits (applied only after group-3 acceptance)

| Edit | Target | Slot rule |
|---|---|---|
| B-04 | `_Decomposition/SOFTWARE_DECOMP.md`: the SCA-V4-002 entry after the SCA-V4-001 entry of `## Decision Log` | `{ACCEPT_DATE}`, `{AMENDMENT_SNAPSHOT}` from the group-3 record; `{Q6_CLAUSE}`, `{Q7_CLAUSE}`, `{Q11_CLAUSE}`, `{Q12_CLAUSE}` and `{Q10_CLAUSE}` take their "accepted" values (BASIS_AMENDMENT B-04 "Slot rules"); Q-5 option B was not chosen, so nothing is appended for it |
| C-01 | `_ScopeChange/_LATEST.md`, whole file, in SPEC §11.2 form | BASIS_AMENDMENT Part C "Slot rules"; cites the C-02 record in `{SCA001_CLOSURE}` and `{OPEN_LIST}` |

B-06a carries no token, but it is also not applied in the candidate; see §2.

## 4. Deliverable `MODIFY` actions and lifecycle (IMPACT_ASSESSMENT §10)

| Deliverables | `_STATUS.md` | Consequence |
|---|---|---|
| DEL-02-01, 02-03, 03-03, 04-02, 01-01 (REVISE); DEL-04-01, 05-01, 05-02 (`_CONTEXT.md` only) | IN_PROGRESS | REVISE admits IN_PROGRESS |
| DEL-10-03, 09-07, 01-04, 02-02 | INITIALIZED | REVISE admits INITIALIZED |

No affected deliverable is CHECKING or ISSUED. No register row authorizes a
reopening; no `write_status.sh --amendment` path arises. No `_STATUS.md` is
written by this amendment.

## 5. Sequence (IMPACT_ASSESSMENT §7)

1. **Group 1 accepted:** write the group-1 decision snapshot, to be committed
   before the next stage (Q-14); write the SCA-V4-001 effective-state record
   (C-02, Q-13).
2. **Group 2 accepted:** write the group-2 decision snapshot, binding
   `Amendment_Actions.csv` by hash, to be committed before application.
3. **Candidate** `_ScopeChange/SCA-V4-002_2026-09-29_1901/`:
   - apply A-01, B-01, B-02, B-05 and B-06b/c;
   - write `Supersession_Delta.csv` and accumulate `Supersession_Map.csv`
     with the prior map;
   - run the post-change `audit-decomp` over the baseline's scope (PKG-01,
     02, 03, 04, 05, 09, 10);
   - dispatch an independent review;
   - write `Handoff_State.md` and `RUN_SUMMARY.md` with a "carried from
     predecessor" section.
4. **Group 3 accepted:** apply B-04 and C-01; run the post-acceptance
   validation under `_PostAcceptanceValidation/SCA-V4-002_{UTC}/`.
5. **`project-setup` INCREMENTAL**, citing the accepted snapshot:
   - **REVISE** for the nine SoWs, each brief carrying `AMENDMENT_REF`,
     `REVISION_SCOPE`, `PRIOR_CONTRACT_SHA256`, `SOURCE_STATE` and
     `STATUS_POLICY=NO_STATUS_TOUCH` (ASC-ISS-009);
   - **register UPDATE** (`dependency-extract`, from ScopeOfWork.md only) for
     the revised deliverables, and for DEL-04-01, DEL-04-02 and DEL-04-03 to
     re-quote the 34 EvidenceQuote cells exactly (ASC-ISS-008); the DEL-09-07
     brief restates the DEP-09-07-016 Notes (ASC-ISS-007);
   - **guards in every brief:** DEL-04-01 gains no consumed input; no
     SCC-002 member gains a row on DEL-09-06; N-12 and N-B8 stay absent; the
     four new sentences yield exactly N-18, N-21, N-24 and X-1; replaced
     OI-constraint rows are re-quoted or retired `source_revised`;
   - **B-06a** is applied here, with the REVISEs;
   - the `project-dag` currency audit, then `TRIGGER=SUCCESSOR` for DAG-003,
     for the owner's acceptance;
   - `audit-scope-closure` against SCA-V4-002;
   - the Phase 5.7 report and the Phase 3.1 coordination refresh, then the
     SETUP_LOG line (ASC-ISS-009).
6. **After SCA-V4-002 (outside it):** the `Coverage_Telemetry.json` rebuild;
   the 17 Design re-pins, GUIDE last; the SWBPIPE "local-first" note with
   the next relay.

## 6. Downstream reruns and handoffs (not executed by the scope-change)

| Package / surface | Owner | Status after group 3 | Required action |
|---|---|---|---|
| 9 `ScopeOfWork.md` | `project-setup` INCREMENTAL → `scope-of-work` | STALE until REVISE | REVISE + VERIFY |
| Registers of those deliverables plus DEL-04-01/02/03 | `dependency-extract` | STALE | UPDATE (§5) |
| DAG-002 | `project-dag` | CURRENT until REVISE; then DEPARTURE | currency audit → DAG-003 (owner) |
| `Consolidated_Coverage.csv` | scope-change | CURRENT (B-01 in the candidate) | none |
| `Coverage_Telemetry.json` | decomposition owner | `STALE_REBUILD_REQUIRED` (carried; ASC-ISS-004) | bounded brief after SCA-V4-002; out of scope |
| 17 Design files | App v4 design undertaking | `STALE_REBUILD_REQUIRED` (ASC-ISS-005) | re-pin at the next design pass, after the REVISEs; out of scope |
| SCA-V4-001 records | scope-change | understated (ASC-ISS-003) | the C-02 effective-state record |

Expected closure verdict at group 3: `OPEN_PENDING_DERIVATIVE_CLOSURE`.

## 7. Closure validation lane

Before group 3:
1. an `audit-decomp` post-change run over the baseline's seven packages,
   compared with `BASELINE/coverage_summary.json`, every difference
   attributed;
2. the `Consolidated_Coverage.csv` recompute check (31 rows, three columns);
3. the `_DAG/DAG-002/SOURCE_MANIFEST.sha256` check;
4. an independent review of the candidate.

After the REVISE runs: `validate_scope_of_work.py` and
`check_boundary_owner_resolution.py` on each revised SoW, and a diff that
confines each SoW change to its `REVISION_SCOPE`.

## 8. DAG impact (ARC_EFFECT §§3–4)

`_DAG/DAG-002/SOURCE_MANIFEST.sha256` binds 130 paths: the 41
`ScopeOfWork.md`, `Dependencies.csv` and `_DEPENDENCIES.md`, the GROUP3
canonical CSVs and `DECISION.md`, `_LATEST_ACCEPTED.md` and
`_Coordination/_COORDINATION.md`. The basis docs, the working decomposition
files, `_Decomposition/_LATEST.md` and `_CONTEXT.md` are not bound, so the
candidate application leaves DAG-002 current. B-06a and the SoW REVISEs
change bound entries; they fall inside one departure.

Expected DAG-003: +4 held arcs inside SCC-002 (N-18, N-21, N-24, X-1), 0
removed, 124 admitted arcs unchanged, the six SCCs unchanged.

## 9. Checkpoint recording

One owner act addressing both subjects is recorded in two immutable decision
snapshots, `SCA-V4-002_GROUP-1_2026-09-29` and
`SCA-V4-002_GROUP-2_2026-09-29`. The group-2 snapshot binds
`Amendment_Actions.csv` by hash. Each snapshot is to be committed before the
next stage consumes it (Q-14).
