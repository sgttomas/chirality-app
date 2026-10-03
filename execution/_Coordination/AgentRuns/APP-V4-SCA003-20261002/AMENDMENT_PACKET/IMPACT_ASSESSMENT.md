# Impact assessment — SCA-V4-003, node P1

**Status: PROPOSED.** Preparation for `scope-change` checkpoint group 1 (the
change and its impact), with the group-2 propagation outline that P2's exact
blocks complete. Nothing is applied: no ScopeOfWork, register,
`_DEPENDENCIES.md`, `_STATUS.md`, decomposition, DAG or basis file is changed
by this packet.

- **Basis:** HEAD `897a107cc9` (branch `claude/chirality-app-v4-60-percent-a41fd5`).
  While this node ran, HEAD moved to `eaa6a37730` (pass-3 closeout G, receipt
  and MEMORY rows; a merge of `main`; P3's baseline). `git diff 897a107cc9
  eaa6a37730` touches no `ScopeOfWork.md`, `Dependencies.csv`, `_STATUS.md`,
  `_Decomposition/`, `_DAG/` or `_ScopeChange/` file (checked), so every input
  this packet relies on for a commitment is unchanged. The G edits (RECOVERY,
  NIR, ROLE, GUIDE re-pin) are Design wording under R22-1…R22-3.
- **Authority:** `APP-V4-SCA003-20261002/OWNER_DECISIONS.md` (sha256
  `23d72f77…5f41`): the owner's "Proceed as recommended" (2026-10-01) and
  "yes, run the closeout" (2026-10-02); HELP_HUMAN's reading that SCA-V4-003
  carries passes 2 and 3's contract proposals, with each item's disposition
  put to the owner.
- **Method:** `workflows/scope-change` WORKFLOW.md (`b5fd1446…`),
  `resources/contract.md` (`3e097df0…`) and `resources/method.md`
  (`a3bb270b…`), read whole; groups 1 and 2 prepared together, as in
  SCA-V4-002. Model: run `APP-V4-SCA002-20260929` (its AMENDMENT_PACKET and
  DISPATCH).
- **Companion files:** [LEDGER.csv](LEDGER.csv) / [LEDGER.md](LEDGER.md)
  (209 proposals), [ARC_EFFECT.md](ARC_EFFECT.md), [OWNER_ITEMS.md](OWNER_ITEMS.md),
  [BASIS_AMENDMENT.md](BASIS_AMENDMENT.md). P2 writes the exact ScopeOfWork
  blocks (`SOW_REVISIONS_A.md`, `_B.md`) from the INCLUDE rows.

## 1. Resolution (method group 1 part A, steps 1 and 4)

| Item | Value |
|---|---|
| `DECOMP_VARIANT` | `SOFTWARE` (as SCA-V4-001 and SCA-V4-002) |
| `CONTEXT_ROOT` | `projects/chirality-app-v4/execution/` |
| `DECOMPOSITION_PATH` | `execution/_Decomposition/SOFTWARE_DECOMP.md`; Change Register binds to `## Decision Log` |
| `AMENDMENT_ID` | **`SCA-V4-003`**: output of `tools/query/scan_next_amendment_id.sh projects/chirality-app-v4/execution/_ScopeChange V4` (script sha256 `2310630d…9bdb`), run under zsh (exit 0). Under bash the script fails (it is a zsh script: `#!/bin/zsh`, zsh glob qualifiers). Without the prefix it returns `SCA-001`, because it counts only unqualified folders; the project uses the `V4` form |
| Pointer posture (group 3) | `ACCEPTED_PREDECESSOR`: `_ScopeChange/_LATEST.md` names `SCA-V4-002_2026-09-29_1901` and stays unchanged until group-3 acceptance |
| Predecessor's closure | `OPEN_PENDING_DERIVATIVE_CLOSURE`, for derivatives only (§9) |
| Accepted graph | DAG-003 (`_DAG/_LATEST.md`), currency CURRENT, 0 pending |

## 2. Change intake (step 2)

The request is the owner's recorded direction; there is no seed packet. Its
scope is the consolidated ledger of both design passes' closeout proposals.

| Source | What it supplies | Ledger rows |
|---|---|---:|
| Pass 2 `closeout/CLOSEOUT_ACCOUNT.md` with `C1-A/B/C.md` | 42 distinct ScopeOfWork items (43 listed), register items, 5 basis items, 1 new held arc | 96 |
| Pass 3 `closeout/C1-A.md`, `C1-B.md`, with `F/F0_JOINS.md` §3–§4, `D/D1…D6.md`, R17…R22 | 56 live ScopeOfWork items (plus 3 withdrawn), 2 Open_Issues items, register items incl. NR-01…NR-04, 1 basis consideration | 103 |
| This node | 9 grounding sentences (registers follow the ScopeOfWork; R22-4) and the Change Register entry | 10 |
| **Total** | | **209** |

**Dispositions recommended:** INCLUDE 185, DEFER 9, DROP 15.

| Kind | INCLUDE | DEFER | DROP | Total |
|---|---:|---:|---:|---:|
| ScopeOfWork | 101 | 3 | 7 | 111 |
| register | 81 | 3 | 5 | 89 |
| Open_Issues | 2 | 0 | 0 | 2 |
| basis | 0 | 3 | 3 | 6 |
| decomposition | 1 | 0 | 0 | 1 |

The DEFERs wait on owner decisions not yet taken (the A12 mapping: SC2-04-01-2,
R2-04-01-b, S-0502-1, R-0502-2; the protected criterion S-01-4), a register
owners' convention (R-02-4), or a later basis update (three basis items). The
DROPs are superseded, duplicated, withdrawn at source, recommended dropped by
their source, or not warranted (NR-03 under R22-4).

## 3. Atomic actions (the future `Intake_Actions.csv`, Status = PROPOSED)

All actions are `MODIFY`. No package or deliverable is added, removed,
reclassified, merged or split; no ID is created, retired or renumbered; no
parent partition is touched, so there is no child-closure set. (New register
row IDs are assigned by `dependency-extract`, as in SCA-V4-002.)

One action per affected entity, as in SCA-V4-002's register. The ledger rows
each action carries are its packet references.

| Seq | ActionType | EntityType | EntityID | Carries (INCLUDE rows) | ScopeChanging (provisional) |
|---|---|---|---|---|---|
| 1 | MODIFY | DELIVERABLE | DEL-01-01 | S-11-1, S-11-2, P1-09; registers R-11-1, -2, -3 | NO (pointer, clarification, receivers) |
| 2 | MODIFY | DELIVERABLE | DEL-01-02 | SC3-01-02-1…11; R3-01-02-a…f, -h | YES (K-4 quit; R17-3 three operations; L-1 one child per home) |
| 3 | MODIFY | DELIVERABLE | DEL-01-03 | SC3-01-03-1…8; R3-01-03-a…f | YES (K-5 usable without experimental surfaces; K-10 display) |
| 4 | MODIFY | DELIVERABLE | DEL-01-04 | SC3-01-04-1…8, -10…13; NR-05, NR-07, NR-08, NR-09, NR-4, R2-01-04-a, R3-01-04-a, -b, SC3-01-04-9 | **YES** (new act-control REQ/OUT/AC/VER, K1-4/K-8) |
| 5 | MODIFY | DELIVERABLE | DEL-01-05 | SC3-01-05-1…7, -10, -12, -13; R3-01-05-a…e | **YES** (new REQ-010 start-up traffic; Codex-account supply; API key in a second home) |
| 6 | MODIFY | DELIVERABLE | DEL-02-01 | SC2-02-01-1, -2; R2-02-01-a…h | NO |
| 7 | MODIFY | DELIVERABLE | DEL-02-02 | SC3-02-02-1…4, -10…12, P1-03; NR-04, R3-02-02-a…d, SC3-02-02-6, -7, -9 | **YES** (K-6 overwrite policy where REQ-003 selected none; K-7; L-4) |
| 8 | MODIFY | DELIVERABLE | DEL-02-03 | SC2-02-03-1…6, P1-01; NR-01, R2-02-03-a…j | YES (K1-1: the slice no longer requests the act) |
| 9 | MODIFY | DELIVERABLE | DEL-02-04 | SC3-02-04-1, -2, -4…7, -9; R3-02-04-a…d, SC3-02-04-8 | YES (no-role conversations; role fixed per conversation, L-2) |
| 10 | MODIFY | DELIVERABLE | DEL-03-01 | S-01-1, -2, -3, -5, P1-06; R-01-1, -2, -3 | YES if S-01-2/-3 are accepted (scope additions) |
| 11 | MODIFY | DELIVERABLE | DEL-03-02 | S-02-1, -2, P1-07; R-02-1, -2, -3 | NO |
| 12 | MODIFY | DELIVERABLE | DEL-03-03 | S-03-1…5, P1-02, P1-08; NR-02, R-03-1…6 | NO (alignment, corrections, K1-1) |
| 13 | MODIFY | DELIVERABLE | DEL-03-04 | S-04-1…3; R-04-1, -2 | NO |
| 14 | MODIFY | DELIVERABLE | DEL-04-01 | SC2-04-01-1, -3, -4; R2-04-01-a, -c | NO |
| 15 | MODIFY | DELIVERABLE | DEL-04-02 | SC2-04-02-1; R2-04-02-a…c | NO |
| 16 | MODIFY | DELIVERABLE | DEL-04-03 | SC2-04-03-1…3, P1-05; R2-04-03-a…h, R20-10 | NO (K1-4 identity recorded; receivers and suppliers named) |
| 17 | MODIFY | DELIVERABLE | DEL-05-01 | S-0501-1, P1-10; R-0501-1…5 | NO |
| 18 | MODIFY | DELIVERABLE | DEL-05-02 | registers only: R-0502-1 | NO |
| 19 | MODIFY | DELIVERABLE | DEL-09-06 | S-0906-1…3; R-0906-1…3 | NO |
| 20 | MODIFY | DELIVERABLE | DEL-09-09 | S-0909-1, -2; R-0909-1…3 | NO |
| 21 | MODIFY | OTHER | OI-009 | SC3-01-05-8 (form per Q-10) | NO |
| 22 | MODIFY | OTHER | OI-018 | OI-018-ptr (Consequence pointer; status unchanged) | NO |
| 23 | MODIFY | OTHER | SOFTWARE_DECOMP.md#decision-log | DC-01 Change Register entry (acceptance-conditional) | NO |

**ScopeChanging** is provisional: the group-2 register fixes it per row. It
has no reopening consequence here, because no deliverable is ISSUED (§8).
Rows 18 and 21–23 have no ScopeOfWork change. If the owner accepts a DEFER
item (Q-9, Q-7), its rows join actions 14, 18 and 10.

## 4. Validation (step 3)

| # | Check | Result |
|---|---|---|
| V-1 | Every MODIFY entity exists: 20 deliverable folders with `ScopeOfWork.md` and `Dependencies.csv`; OI-009 and OI-018 in `Open_Issues.csv`; `## Decision Log` in `SOFTWARE_DECOMP.md` | PASS (listed by `ls`; rows read) |
| V-2 | Lifecycle admits `scope-of-work` REVISE: of the 20 deliverables, 14 are IN_PROGRESS and 6 INITIALIZED; none is CHECKING or ISSUED (§8) | PASS (each `**Current State:**` line read) |
| V-3 | No ADD, REMOVE, RECLASSIFY, MERGE or SPLIT; no parent partition touched | PASS |
| V-4 | Package-discipline and deliverable-granularity rules: no deliverable's Type, Name, ResponsibleParty or granularity changes; no Deliverables.csv field changes | PASS |
| V-5 | Stable IDs: no ID created, retired or reused by the amendment itself; new register row IDs come from extraction | PASS |
| V-6 | SCC and guards over DAG-003 with every INCLUDE row: six SCCs unchanged singly, pairwise and together; admitted layer acyclic; R17-10, DEL-04-01 and DEL-09-06 guards hold | PASS (ARC_EFFECT §2–§3) |
| V-7 | Every INCLUDE register row has a ScopeOfWork sentence on its side, or one proposed in the ledger | PASS after P1-01…P1-10 (anchor check by script; ARC_EFFECT §1.2) |
| V-8 | Every proposal in the sources appears once in the ledger | PASS (ID index by script; LEDGER.md "Checks") |
| V-9 | Exact old → new blocks occur once and the revised SoWs validate | **Not done here**: P2's dry-run (`SOW_REVISIONS_A/B.md`) |

Note on V-2: the six INITIALIZED deliverables are the standalone-App set
(DEL-01-02, 01-03, 01-04, 01-05, 02-02, 02-04); the other 14 are IN_PROGRESS.
No `MEMORY.md` read was needed: this packet changes no `_STATUS.md`.

**Pre-change baseline (step 5): done by P3** (`RUN/BASELINE/`, committed at
`eaa6a37730`): `audit-decomp` over PKG-01, 02, 03, 04, 05, 09 and 10 (32
deliverables, covering all 20 targets): 0 BLOCKER, 35 WARNING, 93 INFO, 0
EXPECTED_CONSEQUENCE; reuse of the SCA-V4-002 audit not admissible (21 inputs
changed). Its findings that bear on this packet agree with it: the C1 records'
SoW and register hashes equal the pre-change bytes (20/20, 20/20); DAG-003
binds every target file; Check 5 MATCH for all 32 (this packet proposes no
`Deliverables.csv` or `_CONTEXT.md` edit); Open_Issues text edits change Check 9
wording, and a status change also moves COV-116's counts; R22-5 would turn 16
Check 6 INFO rows into WARNINGs (35 → 51), to be attributed to R22-5 in the
post-change comparison. The post-change audit reuses the same package scope.

## 5. Impact by semantic section (part B, four lenses)

**Change Register (`## Decision Log`).** One entry, acceptance-conditional
(DC-01), as SCA-V4-002 B-04.

**Unit Ledger (`ScopeLedger.csv`), Objectives, Packages, Deliverables.**
No change. No scope item changes its deliverable mapping. The act control
(SC3-01-04-1) is an obligation the owner directed into DEL-01-04's contract
(DECISION-K1 K1-4; DECISION-K3 K-8); its Deliverables.csv description
("native request, response, turn/outcome and attachment interactions"; "PKG-04
supplies act distinctions") does not contradict it, so no description edit is
proposed (BASIS_AMENDMENT §B).

**Open issues (`Open_Issues.csv`).** OI-009 (Status and Consequence, form per
Q-10) and OI-018 (Consequence pointer, status OPEN). OI-001/OI-002 stay OPEN
for wider scope (SC3-01-02-5, SC3-01-03-2 say "for this scope").

**Coverage / telemetry.** `Consolidated_Coverage.csv` NO_CHANGE (no basis
document changes). `Coverage_Telemetry.json` stays STALE_REBUILD_REQUIRED
(carried from SCA-V4-001/002; still `Revision G3-draft-1`, ActiveOpenIssueCount
24 against 23 OPEN rows today, checked). Option B of Q-10 widens the
difference by one.

**Lens 2, variant-local metadata.** No `_CONTEXT.md` changes (no
Deliverables.csv row changes; SCA-V4-001/002 precedent and pass-2 C1-A). No
`_STATUS.md` changes; REVISE runs `STATUS_POLICY=NO_STATUS_TOUCH`. The
lifecycle question R22-5 is a separate act (§8).

**Lens 3, downstream consumers.**
- 19 ScopeOfWork files through `scope-of-work` `MODE=REVISE` after group 3.
- 20 registers through `dependency-extract` UPDATE (the 19 plus DEL-05-02):
  10 new arcs, about 80 mirror rows, about 50 statement/notes rows; rows whose
  quote changes are re-quoted or retired `source_revised` with the successor
  named.
- DAG-003: currency audit → DEPARTURE → DAG-004 for the owner (ARC_EFFECT §4).
- **Design files pin their ScopeOfWork and register bytes** (for example ACT
  header line 10 pins DEL-04-01's SoW `ac043e54…`, checked; pass-3 C1-A: "Each
  Design header pins its ScopeOfWork and register by these bytes"). After the
  REVISEs and UPDATEs those pins go stale in the Design files of
  all 20 affected deliverables (each has a `Design/` folder), and GUIDE's
  25-row pin table follows. This is the same class as SCA-V4-001's 17 re-pins: a re-pin at the
  next design touch, GUIDE last.
- CASE-002 gains evidence rows for the five held arcs.

**Lens 4, invariant and telemetry risk.** No orphan risk; no parent entity.
Graph risk computed (ARC_EFFECT): no SCC change; 5 admitted arcs change the
admitted order (DEL-01-02, DEL-01-03, DEL-01-05 before the SCC-002 members
that consume them).

## 6. Package roles and derivative surfaces

| Surface | Package role | Classification |
|---|---|---|
| `_Decomposition/SOFTWARE_DECOMP.md` | working surface | DIRECT_EDIT (DC-01, acceptance-conditional) |
| `_Decomposition/Open_Issues.csv` | authoritative companion register | DIRECT_EDIT (OI-009, OI-018) |
| `_Decomposition/Consolidated_Coverage.csv` | authoritative companion register | NO_CHANGE |
| `_Decomposition/Coverage_Telemetry.json` | derived companion | RECOMPUTE, **open** (STALE_REBUILD_REQUIRED, carried) |
| `ScopeLedger.csv`, `Deliverables.csv`, `Packages.csv`, `Objectives.csv`, `Vocabulary_Map.csv`, other `_Decomposition` registers | authoritative companion registers | NO_CHANGE |
| `checkpoint_snapshots/_LATEST_ACCEPTED.md`, `_Decomposition/_LATEST.md` | snapshot / handoff artifact | NO_CHANGE (the reading rule added by SCA-V4-002 already covers later amendments) |
| 19 `ScopeOfWork.md` | authoritative carrier; changed by REVISE after group 3 (the group-2 boundary does not name them for direct edit, as SCA-V4-002) | handoff |
| 20 `Dependencies.csv` and `_DEPENDENCIES.md` | derived from the SoW by `dependency-extract` | downstream rerun |
| Deliverable `_CONTEXT.md`, `_STATUS.md`, `_REFERENCES.md` | variant-local metadata | NO_CHANGE |
| Design files and GUIDE pin table | derived production artifacts | STALE_REBUILD_REQUIRED after the REVISEs (re-pin) |
| DAG-003, CASE-002 | derived publication artifacts | DEPARTURE → successor |
| `_ScopeChange/_LATEST.md`, snapshots, `_PostAcceptanceValidation/` | snapshot / handoff artifact | acceptance-conditional pointer move; new snapshot folders |

## 7. Supersession bindings

- **ScopeOfWork edits bind nothing.** Each carries an accepted basis text, an
  owner decision (DECISION-K1, -K3 as revised, -L) or an integrator ruling,
  and none overrides an admitted authority fact. SCA-V4-002's precedent is the
  same. P2 confirms, block by block, that no exact block contradicts an
  admitted basis fact; S-01-4, which would sit against V4-HI-11, is DEFER.
- **OI-018 pointer:** none (SCA-V4-002 B-02 precedent: a Consequence pointer
  with status unchanged was not bound).
- **OI-009, if Q-10 option B is chosen:** one `SUPERSESSION` row binding
  `_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/Open_Issues.csv`
  OI-009 `Status` = `OPEN` (row present, checked) to its replacement value;
  `SupersessionBindingPresent = YES` on action 21. Under option A, none.
- **Map:** accumulate from SCA-V4-002's `Supersession_Map.csv` (29 rows) with
  `tools/coordination/accumulate_supersession_map.py`; with no delta, carry
  the prior rows forward through the same tool.

## 8. ISSUED-deliverable check and lifecycle

- **ISSUED / CHECKING:** none. Every deliverable's `**Current State:**` is
  IN_PROGRESS or INITIALIZED, and `grep -l -E 'ISSUED|CHECKING'` over all 41
  `_STATUS.md` files returns nothing. The amendment authorizes no reopening;
  `ScopeChanging` has no reopening effect.
- **R22-5 (lifecycle of the six standalone deliverables).** DEL-01-02,
  DEL-01-03, DEL-01-04, DEL-01-05, DEL-02-02 and DEL-02-04 are INITIALIZED
  (since 2026-09-27); both pass-3 C1 records find IN_PROGRESS truthful
  (owner-directed design work, Design at v0.2). The transition INITIALIZED →
  IN_PROGRESS is a Human or WORKING_ITEMS act (SPEC §3.2), not an amendment
  action, and is put to the owner with this first checkpoint (OWNER_ITEMS
  Q-13). REVISE with `NO_STATUS_TOUCH` is unaffected either way.

## 9. Predecessor closure state

- `_ScopeChange/_LATEST.md`: SCA-V4-002, closure
  `OPEN_PENDING_DERIVATIVE_CLOSURE`. Its latest effective-state record
  (`_PostAcceptanceValidation/SCA-V4-002_20260930T044342Z_EFFECTIVE_STATE/`)
  lists three open derivatives (owner-deferred, BASIS-ALIGN DECISION-8):
  the `Coverage_Telemetry.json` rebuild, the 17 Design re-pins, and the
  SWBPIPE "local-first" handoff line.
- Since that record: pass 2 states its Design headers pin the current SoW
  bytes (P2RUN C1-A "Inputs"), and its C1-C records the HANDOFF line fixed
  ("on a model the person chooses, local or cloud"). No effective-state record
  says so. `Coverage_Telemetry.json` is still `G3-draft-1` (checked).
- Closure audits: `_Evaluation/ScopeClosureAudit/ScopeClosure_SCA-V4-001_2026-09-29_2221`
  and `…SCA-V4-002_2026-09-29_2233` (both CLOSED_WITH_OBSERVATIONS, per the
  effective-state record).
- **Proposed:** an append-only effective-state note for SCA-V4-002 after
  group 1 (as SCA-V4-002 Q-13 did for SCA-V4-001), recording what pass 2 did
  and what stays open; the candidate Handoff_State carries the rest.

## 10. Propagation outline (group 2 part B; P2 completes the blocks)

**Write boundary (for Q-3).** The 19 ScopeOfWork files change only by REVISE
after group 3. Direct candidate writes: `Open_Issues.csv` (OI-009, OI-018) and
the SCA-V4-003 snapshot folders under `_ScopeChange/`; after group 3, the
Decision Log entry and the pointer. Nothing else.

1. **Group 1 accepted:** decision snapshot, committed before group 2 is used
   (SCA-V4-002 Q-14); the SCA-V4-002 effective-state note (§9).
2. **Group 2 accepted:** decision snapshot binding `Amendment_Actions.csv` by
   hash, with P2's exact blocks; committed.
3. **Candidate `_ScopeChange/SCA-V4-003_{date}_{HHMM}/`** (posture
   `ACCEPTED_PREDECESSOR`): apply the Open_Issues edits; supersession delta
   (if Q-10 B) and accumulated map; post-change `audit-decomp`; independent
   review; Handoff_State and RUN_SUMMARY.
4. **Group 3 accepted:** Decision Log entry and `_ScopeChange/_LATEST.md` in
   SPEC §11.2 form; post-acceptance validation.
5. **`project-setup` INCREMENTAL**, citing the accepted snapshot:
   - `scope-of-work` `MODE=REVISE`, one deliverable per brief, `MODE=VERIFY`
     after, `STATUS_POLICY=NO_STATUS_TOUCH`, with `AMENDMENT_REF`,
     `REVISION_SCOPE`, `PRIOR_CONTRACT_SHA256`;
   - `dependency-extract` UPDATE for the 20 registers. Guards in every brief:
     DEL-04-01 gains no supplier; no SCC-002 member gains a row on DEL-09-06;
     no DEL-01-02/01-03 row on the R17-10 list; the new sentences are expected
     to yield exactly the 10 new arcs of ARC_EFFECT §1.1; NR-03, NR-06, NR-10
     are not extracted;
   - `project-dag` currency audit, then TRIGGER=SUCCESSOR for DAG-004 (owner);
   - Design re-pin at the next design touch, GUIDE last;
   - `audit-scope-closure` against SCA-V4-003; the Phase 5.7 report and Phase
     3.1 refresh as run artifacts (SCA-V4-002 ASC-ISS-009 lesson).

## 11. Derivative-package status after the amendment (expected)

| Package | Owner | After group 3 | Next action |
|---|---|---|---|
| 19 ScopeOfWork | `project-setup` → `scope-of-work` | STALE until REVISE | REVISE + VERIFY |
| 20 registers | `dependency-extract` | STALE | UPDATE |
| DAG-003 | `project-dag` | CURRENT until the UPDATEs; then DEPARTURE | currency audit → DAG-004 (owner) |
| Design pins and GUIDE pin table | App v4 design undertaking | STALE after REVISE | re-pin at next design touch |
| `Coverage_Telemetry.json` | decomposition owner | STALE_REBUILD_REQUIRED (carried) | bounded rebuild, outside SCA-V4-003 |
| SCA-V4-002 records | scope-change | understated (§9) | effective-state note |

Expected closure verdict at group 3: `OPEN_PENDING_DERIVATIVE_CLOSURE`.

## 12. What this node did not prepare; unknowns

- The exact old → new blocks with their dry-run (P2). V-9 waits on P2. The
  pre-change baseline is P3's (§4).
- The wording of P1-01…P1-10: the ledger names the locus and the Design
  sections to draw from; P2 drafts.
- The OI-009 status token (Q-10) and the maturity values R-03-2 and
  R2-04-03-g set at extraction.
- Whether extraction splits any new arc into several rows (the arc set is
  what counts).
- Not read line by line: the Design files themselves (they were the C1
  records' subject); this node relied on the C1 records, F0 and the rulings,
  and checked by script the SoW mentions, `_STATUS.md` states, DAG-003 arcs
  and Open_Issues rows it states.
