# SCA-V4-003 — Propagation plan

**Standing: accepted at checkpoint group 2 (owner DECISION-1 of run
`APP-V4-SCA003-20261002`, 2026-10-03), as transcribed after the act** from
the packet files the group-2 decision snapshot binds: OWNER_ITEMS.md Q-3 and
Q-16 (sha256 `72c53db2…db86`), IMPACT_ASSESSMENT.md §§6, 7, 8, 10 and 11
(`46ea15e5…35f3`), BASIS_AMENDMENT.md (`151bc6ff…35bf`) and ARC_EFFECT.md §§3–4
(`25073317…94e7`). No decision snapshot binds this file. Where it and the
packet differ, the packet governs. Execution-stage readings are in
`Decision_Log.md`.

Variant `SOFTWARE`; posture `ACCEPTED_PREDECESSOR` (predecessor
`SCA-V4-002_2026-09-29_1901`). All 23 actions are `MODIFY`: no `ADD`,
`REMOVE`, `RECLASSIFY`, `MERGE` or `SPLIT`, so there is no parent-closure
set, no child-closure remap, no folder relocation and no scaffolding.

## 1. Write boundary (Q-3, named exactly)

- **Direct candidate writes:** `execution/_Decomposition/Open_Issues.csv`
  (register rows 21 and 22; B-02 option B, B-03) and the SCA-V4-003 folders
  under `execution/_ScopeChange/` (decision snapshots, pointers, this
  candidate).
- **After group 1:** the SCA-V4-002 effective-state note (C-02), a new
  folder under `_ScopeChange/_PostAcceptanceValidation/`.
- **After group-3 acceptance (acceptance-conditional):**
  `execution/_Decomposition/SOFTWARE_DECOMP.md` `## Decision Log` (row 23;
  B-01) and `execution/_ScopeChange/_LATEST.md` (C-01).
- **After group 3, by their own workflows:** the 19 `ScopeOfWork.md` files
  (rows 1–17, 19, 20), by `scope-of-work` `MODE=REVISE`; the 20
  `Dependencies.csv` files and DEL-04-03's `_DEPENDENCIES.md`, by
  `dependency-extract` UPDATE. These are listed in the register's
  `AffectedFiles` so the register names every file each action changes.
- **Nothing else.** No basis document, other decomposition file,
  `_CONTEXT.md`, `_STATUS.md` or `_DAG` file.

## 2. Package roles and classification (IMPACT_ASSESSMENT §6)

| Surface | Package role | Classification |
|---|---|---|
| `_Decomposition/SOFTWARE_DECOMP.md` | working surface | DIRECT_EDIT, acceptance-conditional (B-01) |
| `_Decomposition/Open_Issues.csv` | authoritative companion register | DIRECT_EDIT (B-02, B-03) |
| `_Decomposition/Consolidated_Coverage.csv` | authoritative companion register | NO_CHANGE (no basis text changes) |
| `_Decomposition/Coverage_Telemetry.json` | derived companion | RECOMPUTE, open (`STALE_REBUILD_REQUIRED`, carried) |
| `ScopeLedger.csv`, `Deliverables.csv`, `Packages.csv`, `Objectives.csv`, `Vocabulary_Map.csv`, other registers | authoritative companion registers | NO_CHANGE |
| `checkpoint_snapshots/_LATEST_ACCEPTED.md`, `_Decomposition/_LATEST.md` | snapshot / handoff artifact | NO_CHANGE |
| 19 `ScopeOfWork.md` | authoritative carrier | handoff: REVISE after group 3 |
| 20 `Dependencies.csv`, DEL-04-03 `_DEPENDENCIES.md` | derived from the ScopeOfWork | downstream rerun (UPDATE) |
| Deliverable `_CONTEXT.md`, `_STATUS.md`, `_REFERENCES.md` | variant-local metadata | NO_CHANGE |
| Design files and the GUIDE pin table | derived production artifacts | STALE_REBUILD_REQUIRED after the REVISEs (re-pin) |
| DAG-003, CASE-002 | derived publication artifacts | DEPARTURE → DAG-004 |
| `_ScopeChange/_LATEST.md`, snapshots, `_PostAcceptanceValidation/` | snapshot / handoff artifact | pointer move after group 3; new folders |

## 3. Supersession (IMPACT_ASSESSMENT §7; BASIS_AMENDMENT Part D)

One `SUPERSESSION` row, D-021: GROUP3 canonical `Open_Issues.csv` OI-009
`Status` `OPEN` → `RESOLVED_BY_OWNER_DECISION`, bound to register row 21. The
ScopeOfWork edits and the OI-018 pointer bind none. The cumulative map is
accumulated from SCA-V4-002's `Supersession_Map.csv` (29 rows) with
`tools/coordination/accumulate_supersession_map.py`.

## 4. Acceptance-conditional edits (only after group-3 acceptance)

| Edit | Target | Slots |
|---|---|---|
| B-01 | `SOFTWARE_DECOMP.md` Decision Log entry | `{ACCEPT_DATE}`, `{AMENDMENT_SNAPSHOT}`; clause slots fixed by DECISION-1 (group-2 `DECISION.md`) |
| C-01 | `_ScopeChange/_LATEST.md`, SPEC §11.2 form | `{AMENDMENT_SNAPSHOT}`, `{ACCEPT_DATE}`, `{CLOSURE_VERDICT}`, `{G1_DATE}` = `{G2_DATE}` = `2026-10-03`, `{C02_UTC}`, `{UTC}` |

## 5. Deliverable `MODIFY` actions and lifecycle

All 20 deliverables the register names (19 with a ScopeOfWork change plus
DEL-05-02) are IN_PROGRESS at the application basis `ec267bdb9f` (after the
Q-13 act of `baa6e618d7`); none is CHECKING or ISSUED, so the amendment
authorizes no reopening and holds nothing for a reversal. `ScopeChanging`
is `YES` on rows 2, 3, 4, 5, 7, 8, 9 and 10; it has no reopening effect here.
REVISE runs with `STATUS_POLICY=NO_STATUS_TOUCH`.

## 6. Sequence (IMPACT_ASSESSMENT §10)

1. Group 1 accepted: decision snapshot committed (`3e747b7685`); the
   SCA-V4-002 effective-state note.
2. Group 2 accepted: decision snapshot binding `Amendment_Actions.csv`
   (`9b7c2ce8…6d1c`), with the packet's exact blocks and edits, committed
   (`ec267bdb9f`).
3. This candidate: the Open_Issues edits; `Supersession_Delta.csv` and the
   accumulated map; the post-change `audit-decomp` over PKG-01, 02, 03, 04,
   05, 09 and 10; the independent review; `Handoff_State.md` and
   `RUN_SUMMARY.md`.
4. Group 3 accepted: B-01 and C-01; post-acceptance validation.
5. `project-setup` INCREMENTAL, citing the accepted snapshot:
   - `scope-of-work` `MODE=REVISE`, one deliverable per brief, then
     `MODE=VERIFY`, `STATUS_POLICY=NO_STATUS_TOUCH`, with `AMENDMENT_REF`,
     `REVISION_SCOPE` (that deliverable's G-blocks) and `PRIOR_CONTRACT_SHA256`
     (the SOW_REVISIONS summary hashes);
   - `dependency-extract` UPDATE for the 20 registers, with the guards of
     IMPACT §10 and ARC_EFFECT §3: DEL-04-01 gains no supplier; no SCC-002
     member gains a row on DEL-09-06; no DEL-01-02/01-03 row on the R17-10
     list; exactly the 10 new arcs of ARC_EFFECT §1.1; NR-03, NR-06 and NR-10
     not extracted; the 15 RP1-MX mirrors added;
   - `project-dag` currency audit, then TRIGGER=SUCCESSOR for DAG-004 (owner);
   - Design re-pins at the next design touch, GUIDE last;
   - `audit-scope-closure` against SCA-V4-003.

## 7. Downstream reruns and handoffs (not executed by the scope-change)

| Package | Owner | After group 3 | Next action |
|---|---|---|---|
| 19 ScopeOfWork | `project-setup` → `scope-of-work` | STALE until REVISE | REVISE + VERIFY |
| 20 registers | `dependency-extract` | STALE | UPDATE |
| DAG-003 | `project-dag` | CURRENT until the UPDATEs; then DEPARTURE | currency audit → DAG-004 (owner) |
| Design pins and GUIDE pin table | App v4 design undertaking | STALE after REVISE | re-pin at the next design touch |
| `Coverage_Telemetry.json` | decomposition owner | STALE_REBUILD_REQUIRED (carried) | bounded rebuild, outside SCA-V4-003 |

## 8. Closure validation lane

- Direct authoritative writes in the candidate: B-02, B-03; the delta and
  map.
- Not executed by the scope-change: every rerun in §7.
- Before group 3 can be presented: the post-change audit compared with the
  baseline, every difference attributed; the independent review.
- Expected closure verdict at group 3: `OPEN_PENDING_DERIVATIVE_CLOSURE`.

## 9. DAG impact (ARC_EFFECT §§3–4)

+10 arcs (5 admitted: NR-01, NR-02, NR-04, NR-05, NR-07; 5 held: R2-04-03-e,
R20-10, NR-08, NR-09, NR-4), 202 → 212; the six SCCs unchanged; the
admitted layer acyclic; DAG pending expected for DEL-01-02, 01-03, 01-04,
01-05, 02-01, 02-02, 02-03, 02-04, 03-03, 04-02 and 04-03. Nothing departs
until the REVISEs and UPDATEs change DAG-003's bound files.
