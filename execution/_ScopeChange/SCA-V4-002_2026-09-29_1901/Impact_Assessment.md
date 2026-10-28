# Impact assessment — SCA-V4-002, node P1

**Status: PROPOSED, revision 2. This revision folds in the CA1 closure audit
of SCA-V4-001.** This is the preparation for `scope-change` checkpoint groups
1 (the change and its impact) and 2 (the exact amendment and the propagation
plan). Nothing is applied.

- **Basis:** commit `102f09c1a`.
- **Authority:**
  - `APP-V4-SCA002-20260929/OWNER_DECISIONS.md` (the owner accepted the
    recorder's proposal: a closure audit and SCA-V4-002 preparation in
    parallel);
  - `APP-V4-BASIS-ALIGN-20260928/OWNER_DECISIONS.md` DECISION-8 (answer 3)
    and DECISION-10 (option A).
- **Method:** `workflows/scope-change` (WORKFLOW.md, resources/contract.md,
  resources/method.md). SoW edits are shaped for `workflows/scope-of-work`
  `MODE=REVISE` (WORKFLOW.md, resources/brief.md).
- **Companion files:**
  - [BASIS_AMENDMENT.md](BASIS_AMENDMENT.md): docs, decomposition, pointer
    and supersession edits;
  - [SOW_REVISIONS.md](SOW_REVISIONS.md): 26 SoW blocks;
  - [ARC_EFFECT.md](ARC_EFFECT.md): the four arcs, the SCC computation and
    the DAG-003 departure;
  - [OWNER_ITEMS.md](OWNER_ITEMS.md): the decisions.

## 1. Resolution (method step 1)

| Item | Value |
|---|---|
| `DECOMP_VARIANT` | `SOFTWARE` (as SCA-V4-001) |
| `CONTEXT_ROOT` | `projects/chirality-app-v4/execution/` |
| `DECOMPOSITION_PATH` | `execution/_Decomposition/SOFTWARE_DECOMP.md`. Its Change Register binds to `## Decision Log`, added by SCA-V4-001 D-15 |
| `AMENDMENT_ID` | **`SCA-V4-002`**. This is the output of `tools/query/scan_next_amendment_id.sh projects/chirality-app-v4/execution/_ScopeChange V4`, run directly under zsh. Without the prefix the helper returns `SCA-001`, because it counts only unqualified folders; the project uses the `V4` qualified form |
| Pointer posture (group 3) | `ACCEPTED_PREDECESSOR`. `_ScopeChange/_LATEST.md` names `SCA-V4-001_2026-09-28_2155` and stays unchanged until group-3 acceptance |
| Predecessor's closure | `OPEN_PENDING_DERIVATIVE_CLOSURE`. The CA1 audit (`_Evaluation/ScopeClosureAudit/ScopeClosure_SCA-V4-001_2026-09-29_1222/`) returned **OPEN** because of ASC-ISS-001 (§9) |

## 2. Change intake (method step 2)

The request comes from the owner's recorded direction and scope. There is
no seed packet.

| # | Item (OWNER_DECISIONS "Scope … as decided so far") | Source | Status in this packet |
|---|---|---|---|
| 1 | DEL-10-03 REQ-005 "local-first" | DECISION-8 answer 3; DECISION-10 | Decided scope |
| 2 | Consumption sentences for N-18, N-21, N-24, X-1 "where the dependency is real" | DECISION-10 option A | Decided scope; all four recommended kept (Q-4) |
| 3a | DEL-09-07, DEL-01-04 and DEL-02-02 SoW text on OI-001/002/012 | DECISION-10 (C2-5 carried items) | Decided scope |
| 3b | DEL-03-03 CLM-002 tail | same | Decided scope |
| 3c | The A17b line join | same | Decided scope |
| 4 | Open_Issues OI-001/002 status | V13 F3: to be proposed, not assumed | **Proposed** (Q-5) |
| 5a | V13 F2: `_ScopeChange/_LATEST.md` in §11.2 form | V13 | Decided scope (pointer write) |
| 5b | V13 F1: group-3 manifest label | V13 | Disclosed only |
| P-1 | Same-class sentences in DEL-04-02 CLM-004 and the DEL-01-01 [N] line | Found here | **Proposed** (Q-6) |
| P-2 | OI-012 Consequence pointer | Found here | **Proposed** (Q-7) |
| CA-1 | ASC-ISS-001: path-level supersession rows | CA1 | **Proposed** (Q-10) |
| CA-2 | ASC-ISS-002: DEL-04-01 description "checkpoints override autonomy" | CA1 | **Proposed** (Q-11) |
| CA-3 | ASC-ISS-003: SCA-V4-001 effective-state record, with the pointer fix | CA1 | **Proposed** (Q-13) |
| CA-6 | ASC-ISS-006: reading rule for the accepted-decomposition pointers | CA1 | **Proposed** (Q-12) |
| CA-7, CA-8, CA-9 | ASC-ISS-007 (DEP-09-07-016 Notes); ASC-ISS-008 (34 quotes); ASC-ISS-009 (Phase 5.7/3.1 and NO_STATUS_TOUCH) | CA1 | Propagation plan items (§7), not amendment actions |
| — | ASC-ISS-004 (Coverage_Telemetry) and ASC-ISS-005 (17 Design re-pins) | CA1 | **Out of scope**; sequenced after SCA-V4-002 (§8) |

## 3. Atomic actions and the proposed register

### 3.1 Actions (the future `Intake_Actions.csv`, with Status = PROPOSED)

All actions are `MODIFY`. There is no ADD, REMOVE, RECLASSIFY, MERGE or
SPLIT. No ID is created, retired or renumbered, and no parent partition is
touched, so there is no child-closure set.

| Seq | Entity | Change | Packet ref | Owner item |
|---|---|---|---|---|
| 1 | DEL-10-03 | SoW REQ-005: local-first → D4-3 wording; AX-005 | F-1003-01…02 | Q-2 |
| 2 | DEL-02-01 | SoW CLM-002 consumption sentence (N-18); AX-006 | F-0201-01…02 | Q-4 |
| 3 | DEL-02-03 | SoW CLM-002 consumption sentence (N-21, N-24, X-1); AX-005 | F-0203-01…02 | Q-4 |
| 4 | DEL-09-07 | SoW CLM-002, TBD-002, TBD-003; AX-005 | F-0907-01…04 | Q-2 |
| 5 | DEL-01-04 | SoW CLM-005, VER-005, TBD-001, TBD-002, TBD-004; AX-004 | F-0104-01…06 | Q-2 |
| 6 | DEL-02-02 | SoW TBD-001, TBD-002; AX-004 | F-0202-01…03 | Q-2 |
| 7 | DEL-03-03 | SoW CLM-002 tail, REQ-005; AX-005 | F-0303-01…03 | Q-2 |
| 8 | DEL-04-02 | SoW CLM-004; AX-005 | F-0402-01…02 | Q-6 |
| 9 | DEL-01-01 | SoW [N] line; AX-006 | F-0101-01…02 | Q-6 |
| 10 | docs/HOST_INTEGRATION.md#status | Line layout | A-01 | Q-2, Q-8 |
| 11 | Consolidated_Coverage.csv | RECOMPUTE, 31 rows | B-01 | Q-3 |
| 12 | OI-012 | Consequence pointer | B-02 | Q-7 |
| 13 | SOFTWARE_DECOMP.md#decision-log | Change Register entry | B-04 | Q-3 |
| 14 | DEL-04-01 | Deliverables.csv Description and `_CONTEXT.md` mirror | B-05 | Q-11 |
| 15 | `_Decomposition` pointers | Reading-rule note | B-06a/b | Q-12 |
| 16 | five `_CONTEXT.md` basis lines | Reading-rule note | B-06c | Q-12 |

If Q-5 option B is chosen, a row 17 is added: MODIFY OTHER OI-001/OI-002
Status, ScopeChanging NO.

### 3.2 Proposed register (the future `Amendment_Actions.csv`, group 2)

- **ScopeChanging:** `YES` only for DEL-10-03, because REQ-005's model
  direction changes. Every other row aligns text or records a dependency
  with the accepted basis.
- **Reopening:** no deliverable is ISSUED or CHECKING, so no row authorizes a
  reopening.
- **SupersessionBindingPresent:** `YES` only on row 14, which has its own
  `D-014` delta row (BASIS_AMENDMENT Part D). The 17 path-level rows for
  SCA-V4-001 are decision-log-only (`DL-…`) and bind no row here.
- **DownstreamReruns:** comma-separated, per the contract schema. SCA-V4-001
  used `;` (V11 F5).
- **Draft bytes:** sha256 `dafa622e…af13` (scratch
  `Amendment_Actions.draft.csv`). The final register drops conditional rows
  the owner declines and renumbers only if rows are dropped before
  acceptance.

```csv
AmendmentID,ActionSeq,ActionType,EntityType,EntityID,Description,AffectedFiles,DownstreamReruns,SupersessionBindingPresent,ScopeChanging
{AMENDMENT_ID},1,MODIFY,DELIVERABLE,DEL-10-03,ScopeOfWork REQ-005: 'local-first' aligned with DECISION-4 D4-3 (F-1003-01..02),projects/chirality-app-v4/execution/PKG-10_Project definition and manual-led practice/1_Working/DEL-10-03_Shared commitments and consumer responsibility account/ScopeOfWork.md,"project-setup(INCREMENTAL),scope-of-work(REVISE),dependency-extract(UPDATE)",NO,YES
{AMENDMENT_ID},2,MODIFY,DELIVERABLE,DEL-02-01,ScopeOfWork CLM-002: consumption sentence for arc N-18 (F-0201-01..02),projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-01_Portable workflow contract and shared allocation/ScopeOfWork.md,"project-setup(INCREMENTAL),scope-of-work(REVISE),dependency-extract(UPDATE),project-dag(currency),project-dag(SUCCESSOR)",NO,NO
{AMENDMENT_ID},3,MODIFY,DELIVERABLE,DEL-02-03,ScopeOfWork CLM-002: consumption sentence for arcs N-21 N-24 X-1 (F-0203-01..02),projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-03_Workflow execution compatibility and round-trip support/ScopeOfWork.md,"project-setup(INCREMENTAL),scope-of-work(REVISE),dependency-extract(UPDATE),project-dag(currency),project-dag(SUCCESSOR)",NO,NO
{AMENDMENT_ID},4,MODIFY,DELIVERABLE,DEL-09-07,ScopeOfWork CLM-002 TBD-002 TBD-003: OI-001/OI-002 aligned with DECISION-1 D2/D3 (F-0907-01..04),projects/chirality-app-v4/execution/PKG-09_Candidate examination and connected journeys/1_Working/DEL-09-07_Local host candidate qualification/ScopeOfWork.md,"project-setup(INCREMENTAL),scope-of-work(REVISE),dependency-extract(UPDATE)",NO,NO
{AMENDMENT_ID},5,MODIFY,DELIVERABLE,DEL-01-04,ScopeOfWork CLM-005 VER-005 TBD-001 TBD-002 TBD-004: OI-001/002/012 aligned with DECISION-1 D2-D4 (F-0104-01..06),"projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/ScopeOfWork.md","project-setup(INCREMENTAL),scope-of-work(REVISE),dependency-extract(UPDATE)",NO,NO
{AMENDMENT_ID},6,MODIFY,DELIVERABLE,DEL-02-02,ScopeOfWork TBD-001 TBD-002: OI-001/002/012 aligned with DECISION-1 D2-D4 (F-0202-01..03),projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-02_Workflow-making workspace and registration/ScopeOfWork.md,"project-setup(INCREMENTAL),scope-of-work(REVISE),dependency-extract(UPDATE)",NO,NO
{AMENDMENT_ID},7,MODIFY,DELIVERABLE,DEL-03-03,ScopeOfWork CLM-002 tail and REQ-005: what remains open (F-0303-01..03),projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-03_Local external-agent receiving adapter/ScopeOfWork.md,"project-setup(INCREMENTAL),scope-of-work(REVISE),dependency-extract(UPDATE)",NO,NO
{AMENDMENT_ID},8,MODIFY,DELIVERABLE,DEL-04-02,ScopeOfWork CLM-004: same-class correction (F-0402-01..02; conditional Q-6),"projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-02_Visible autonomy and result standing/ScopeOfWork.md","project-setup(INCREMENTAL),scope-of-work(REVISE),dependency-extract(UPDATE)",NO,NO
{AMENDMENT_ID},9,MODIFY,DELIVERABLE,DEL-01-01,ScopeOfWork source line [N]: D4 pin (F-0101-01..02; conditional Q-6),projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-01_Stock Codex hosting and supplier contract/ScopeOfWork.md,"project-setup(INCREMENTAL),scope-of-work(REVISE),dependency-extract(UPDATE)",NO,NO
{AMENDMENT_ID},10,MODIFY,OTHER,docs/HOST_INTEGRATION.md#status,Line layout: the A17b join (A-01),projects/chirality-app-v4/docs/HOST_INTEGRATION.md,audit-decomp,NO,NO
{AMENDMENT_ID},11,MODIFY,OTHER,Consolidated_Coverage.csv,RECOMPUTE of the 31 HOST_INTEGRATION rows after A-01 (B-01),projects/chirality-app-v4/execution/_Decomposition/Consolidated_Coverage.csv,audit-decomp,NO,NO
{AMENDMENT_ID},12,MODIFY,OTHER,OI-012,Consequence pointer to DECISION-1 D4; status stays OPEN (B-02; conditional Q-7),projects/chirality-app-v4/execution/_Decomposition/Open_Issues.csv,,NO,NO
{AMENDMENT_ID},13,MODIFY,OTHER,SOFTWARE_DECOMP.md#decision-log,Change Register entry (B-04; acceptance-conditional),projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md,,NO,NO
{AMENDMENT_ID},14,MODIFY,DELIVERABLE,DEL-04-01,Deliverables.csv Description checkpoint clause with governance-phase qualifier and _CONTEXT.md mirror (B-05; ASC-ISS-002; conditional Q-11),"projects/chirality-app-v4/execution/_Decomposition/Deliverables.csv;projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-01_Operation-policy and human-act distinctions/_CONTEXT.md","audit-decomp,dependency-extract(UPDATE)",YES,NO
{AMENDMENT_ID},15,MODIFY,OTHER,_Decomposition pointers#reading-rule,Reading-rule note on the accepted-decomposition pointers (B-06a/b; ASC-ISS-006; conditional Q-12; B-06a timed with the DAG-003 departure),projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/_LATEST_ACCEPTED.md;projects/chirality-app-v4/execution/_Decomposition/_LATEST.md,project-dag(currency),NO,NO
{AMENDMENT_ID},16,MODIFY,OTHER,_CONTEXT.md#accepted-basis,Reading-rule note on five _CONTEXT.md Accepted-basis lines (B-06c; ASC-ISS-006; conditional Q-12),"projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-03_Workflow execution compatibility and round-trip support/_CONTEXT.md;projects/chirality-app-v4/execution/PKG-05_Embedded-host receiving integration/1_Working/DEL-05-01_Minimal-loop and model receiving contract/_CONTEXT.md;projects/chirality-app-v4/execution/PKG-05_Embedded-host receiving integration/1_Working/DEL-05-02_Host panel and shared interaction receiving/_CONTEXT.md;projects/chirality-app-v4/execution/PKG-09_Candidate examination and connected journeys/1_Working/DEL-09-07_Local host candidate qualification/_CONTEXT.md;projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-01_Operation-policy and human-act distinctions/_CONTEXT.md",,NO,NO
```

## 4. Validation (method step 3)

| # | Check | Result |
|---|---|---|
| V-1 | Every MODIFY entity exists: 10 deliverables, the docs file, 5 decomposition files, 6 `_CONTEXT.md` | PASS |
| V-2 | Lifecycle admits REVISE: DEL-02-01, 02-03, 03-03, 04-02 and 01-01 are IN_PROGRESS; DEL-10-03, 09-07, 01-04 and 02-02 are INITIALIZED; none is CHECKING or ISSUED | PASS. Read from each `_STATUS.md`. `_MEMORY.md`/`MEMORY.md` read where present, as context only |
| V-3 | DEL-09-07 CLM-002 carries the same OI-001/002 statement as TBD-002/003. It is aligned with them (F-0907-01), so the SoW does not contradict itself | Included within item 3a |
| V-4 | Other SoWs still say OI-001/OI-002 "remain OPEN": DEL-01-02, 01-03, 08-02, 09-02, 09-05, 09-11, 09-12 and 11-03 (later undertakings). They are consistent with the rows staying OPEN (Q-5 option A). Option B would contradict them | Recorded. **Not in scope** under option A |
| V-5 | Same-class defects in first-increment SoWs revised under SCA-V4-001: DEL-04-02 CLM-004 ("decides the unresolved … OI-001 and OI-002") and DEL-01-01 source [N] ("no selected version/environment is established"). Both contradict their own TBDs | **Proposed** (Q-6) |
| V-6 | Every "old" block occurs exactly once: 26 SoW blocks; A-01; B-02 (row-scoped); B-04; B-05a/b; B-06a/b/c (7 files) | PASS (`sow_dryrun.py`, `basis_dryrun.py`, direct counts) |
| V-7 | Every revised SoW validates: `validate_scope_of_work.py` gives 9/9 `SOW_V1`, valid, 0 issues; `check_boundary_owner_resolution.py` gives 9/9 exit 0. DEL-03-03 keeps its one pre-existing NOT_CHECKABLE (REQ-003), which is unchanged | PASS |
| V-8 | Frontmatter unchanged, 9/9; unfilled tokens 0 | PASS |
| V-9 | Mention check: the new text names no deliverable that its SoW did not already name, 0 in 9. No edit names DEL-09-06 or makes DEL-04-01 a consumer | PASS |
| V-10 | Supersession draft: 18/18 superseded facts found in the GROUP3 canonical files; 17/17 replacements found in the current files (D-014 still to be applied); accumulator exit 0, 29 rows, 0 findings | PASS |
| V-11 | The §11.2 pointer form is parsed by the registered `_latest_pointer_target`, and `_pointer_matches` is True. The current pointer gives `None` (V13 F2 confirmed) | PASS |
| V-12 | Package-discipline and deliverable-granularity rules: no deliverable's Type, Name, ResponsibleParty or granularity changes | PASS |

**Pre-change baseline (method step 5): not yet run.**
- **What is needed:** an `audit-decomp` run over the affected packages
  (PKG-01, 02, 03, 04, 09 and 10) before group 1 is presented.
- **Possible reuse:** CA1's audit inputs may qualify if its recorded input
  hashes (`INPUT_MANIFEST.sha256`) equal the pre-change state, under the
  reuse rule in method step 5.
- **Why this node cannot do it:** it is a Type 2 node and does not delegate.

## 5. Impact by lens

**1. Decomposition structure.** No section, ID, row identity or mapping
changes. Only field text changes:
- Deliverables.csv DEL-04-01 Description (conditional);
- OI-012 Consequence (conditional);
- Consolidated_Coverage hashes and lines;
- the Decision Log entry.

**2. Variant-local metadata.** The `_CONTEXT.md` files change: DEL-04-01
(mirror plus reading rule) and DEL-02-03, 05-01, 05-02 and 09-07 (reading
rule). No `_STATUS.md` changes. REVISE is `NO_STATUS_TOUCH`.

**3. Downstream consumers.**
- 9 (or 7 without Q-6) SoWs, through REVISE.
- Registers:
  - `dependency-extract` UPDATE for those deliverables;
  - DEL-04-01, 04-02 and 04-03 for ASC-ISS-008.
  - **Rows expected to lose their quote**, to be re-quoted or retired
    `source_revised` with the successor row named:
    - DEL-01-04: DEP-01-04-013 (OI-001), -014 (OI-002) and -016 (OI-012);
    - DEL-09-07: DEP-09-07-022 (OI-001) and -023 (OI-002).
  - All five are EXTERNAL CONSTRAINT rows, so no arc changes. New EXTERNAL
    rows naming OI-021 may appear.
- DAG: the currency audit → DEPARTURE → DAG-003 (ARC_EFFECT §4).
- CASE-002 gains evidence rows.

**4. Invariant and telemetry risk.**
- No orphan risk; no parent entity is touched.
- `Coverage_Telemetry.json` is already STALE_REBUILD_REQUIRED. This
  amendment changes its inputs again: Consolidated_Coverage, and Open_Issues
  only if Q-5 option B is chosen. The rebuild follows SCA-V4-002 (§8).

**The four arcs.** They add 4 held arcs inside SCC-002; SCC membership is
unchanged (ARC_EFFECT §3).

## 6. Package roles, derivative surfaces and supersession

| Surface | Package role | Classification |
|---|---|---|
| `SOFTWARE_DECOMP.md` | working surface | DIRECT_EDIT (B-04) |
| `Deliverables.csv`, `Open_Issues.csv` | authoritative companion register | DIRECT_EDIT (B-05a, B-02; conditional) |
| `Consolidated_Coverage.csv` | authoritative companion register | RECOMPUTE (B-01) |
| `Coverage_Telemetry.json` | derived companion | RECOMPUTE, **open** (STALE_REBUILD_REQUIRED, carried) |
| `checkpoint_snapshots/_LATEST_ACCEPTED.md`, `_Decomposition/_LATEST.md` | snapshot / handoff artifact (pointer) | DIRECT_EDIT (B-06a/b; conditional) |
| `docs/HOST_INTEGRATION.md` | authoritative carrier named in the group-2 boundary | DIRECT_EDIT (A-01) |
| 9 `ScopeOfWork.md` | authoritative carrier; changed by REVISE after group 3 | handoff (not written in the candidate) |
| 6 `_CONTEXT.md` | variant-local metadata (default propagation write) | DIRECT_EDIT |
| `ScopeLedger.csv`, `Packages.csv`, `Vocabulary_Map.csv`, `Objectives.csv`, `Allocation_Rationale.csv`, `Source_*.csv`, `Scope_Classification.csv`, `ContextBudgetQA.csv`, `External_Dependencies.csv`, `Companion_Inventory.csv` | registers | NO_CHANGE |
| Registers, DAG-002, CASE-002 | derived publication artifacts | downstream reruns |
| `_ScopeChange/_LATEST.md`, snapshots, `_PostAcceptanceValidation/` | snapshot / handoff artifact | acceptance-conditional (C-01, C-02) |

**Supersession.**
- **New override:** one, row 14 (D-014: GROUP3 `Deliverables.csv` DEL-04-01
  "PKG-02 checkpoints override autonomy;").
- **Path-level rows:** 17 `DL-SCA-V4-001-A…` rows bind SCA-V4-001's
  existing overrides (ASC-ISS-001 option (a)).
- **Map:** accumulated from SCA-V4-001's map as the prior; 29 rows in
  scratch.
- **The SoW edits bind nothing.** They carry an accepted basis and supersede
  no admitted authority fact. The authority facts behind the DEL-10-03 edit
  (V4-HOST-01 default; the purpose "local-first") are already bound (D-002,
  D-006).

## 7. Propagation plan (group-2 part B)

**Write boundary (for Q-3).** It is exactly the files named in the register
AffectedFiles, plus the SCA-V4-002 snapshot folders and pointers under
`_ScopeChange/`. Nothing else.

**Sequence.**

1. **Group 1 accepted:**
   - write the group-1 decision snapshot and commit it (Q-14);
   - write the SCA-V4-001 effective-state record (C-02, Q-13), recording the
     owner's ASC-ISS-001 ruling.
2. **Group 2 accepted:** write the group-2 decision snapshot, binding
   `Amendment_Actions.csv` by hash, and commit it.
3. **Candidate `_ScopeChange/SCA-V4-002_{date}_{HHMM}/`,** posture
   `ACCEPTED_PREDECESSOR`:
   - apply A-01, B-01, B-02, B-05 and B-06b/c;
   - write `Supersession_Delta.csv` (Part D) and accumulate
     `Supersession_Map.csv` with the prior map;
   - run the post-change `audit-decomp` (same package scope as the
     baseline);
   - dispatch an independent review;
   - write Handoff_State and RUN_SUMMARY with a "carried from predecessor"
     section.
4. **Group 3 accepted:**
   - apply B-04 and C-01;
   - run the post-acceptance validation under
     `_PostAcceptanceValidation/SCA-V4-002_{UTC}/`.
5. **`project-setup` INCREMENTAL**, citing the accepted snapshot:
   - **REVISE:** `scope-of-work` `MODE=REVISE`, one deliverable per brief,
     for the 9 (or 7) SoWs, each closing with `MODE=VERIFY`. Each brief
     carries `AMENDMENT_REF` (ID, snapshot, register row, register hash),
     `REVISION_SCOPE` (from SOW_REVISIONS), `PRIOR_CONTRACT_SHA256`,
     `SOURCE_STATE` and **`STATUS_POLICY=NO_STATUS_TOUCH`**. Setting it
     explicitly avoids the DECISION-9 "PRESERVE_CURRENT" slip
     (**ASC-ISS-009**; V13 N4).
   - **Register UPDATE:** `dependency-extract` UPDATE, from ScopeOfWork.md
     only, for:
     - the revised deliverables;
     - **DEL-04-01, DEL-04-02 and DEL-04-03, to re-quote the 34 backtick-less
       EvidenceQuote cells exactly** (**ASC-ISS-008**; V12 F1). The rows are
       DEL-04-01 017, 018, 022–027, 029; DEL-04-02 011, 012, 015–023, 025;
       and DEL-04-03 019, 021–032.
     - The DEL-09-07 brief restates the **DEP-09-07-016 Notes** against the
       revised SoW (**ASC-ISS-007**).
   - **Guards carried into every brief:**
     - DEL-04-01 gains no consumed input;
     - no SCC-002 member gains a row on DEL-09-06;
     - N-12 and N-B8 stay absent;
     - the four new sentences are expected to yield exactly N-18, N-21,
       N-24 and X-1;
     - replaced OI-constraint rows are re-quoted or retired
       `source_revised`.
   - **B-06a** (`_LATEST_ACCEPTED.md`) is applied here, with the REVISEs,
     so that one currency audit takes it up.
   - **Currency and successor:** the `project-dag` currency audit, then
     TRIGGER=SUCCESSOR for DAG-003, for the owner's acceptance.
   - **Closure check:** `audit-scope-closure` against SCA-V4-002.
   - **Reports (ASC-ISS-009):** the **Phase 5.7 "Incremental setup for
     SCA-V4-002" report** and the **Phase 3.1 coordination refresh** are
     written as run artifacts. Then the SETUP_LOG line.
6. **After SCA-V4-002 (outside it):**
   - the Coverage_Telemetry rebuild by the decomposition owner's bounded
     brief, once;
   - the Design re-pins at the next design pass, GUIDE last;
   - the SWBPIPE "local-first" note with the next relay.

## 8. Derivative-package status after the amendment

| Package | Owner | Status after group 3 | Next action |
|---|---|---|---|
| 9 (or 7) SoWs | `project-setup` → `scope-of-work` | STALE until REVISE | REVISE + VERIFY |
| Registers of those deliverables plus DEL-04-01/02/03 | `dependency-extract` | STALE | UPDATE (§7) |
| DAG-002 | `project-dag` | CURRENT until REVISE; then DEPARTURE | currency audit → DAG-003 (owner) |
| `Consolidated_Coverage.csv` | scope-change | CURRENT (B-01 in the candidate) | none |
| `Coverage_Telemetry.json` | decomposition owner | STALE_REBUILD_REQUIRED (carried from SCA-V4-001; ASC-ISS-004) | bounded brief after SCA-V4-002 — **out of scope** |
| 17 Design files | App v4 design undertaking | STALE_REBUILD_REQUIRED (ASC-ISS-005) | re-pin at the next design pass, after the REVISEs — **out of scope** |
| SCA-V4-001 records | scope-change | understated (ASC-ISS-003) | C-02 effective-state record |

Expected closure verdict at group 3: `OPEN_PENDING_DERIVATIVE_CLOSURE`.

## 9. CA1 fold-in trace (SCA-V4-001 closure audit, verdict OPEN)

Source: `_Evaluation/ScopeClosureAudit/ScopeClosure_SCA-V4-001_2026-09-29_1222/`
(`Scope_Closure_Report.md` sha256 `50b6e043…3e76`, `Scope_Closure_IssueLog.csv`
`9fbfaa31…b973`). The audit was committed at `f5b5d0ad0`, after this
packet's basis. That commit changed no governed file (only `_Evaluation/`
and DISPATCH.md), so `102f09c1a` remains the basis for every edit.

| ASC-ISS | Severity | Where it lands | Owner item |
|---|---|---|---|
| 001 | CRITICAL (provisional) | BASIS_AMENDMENT Part D: 17 DL rows plus re-accumulation; `Decision_Log` reference | Q-10 (recommend (a)) |
| 002 | MINOR | B-05, register row 14, D-014 | Q-11 |
| 003 | MINOR | C-02 effective-state record, combined with C-01 (V13 F2) | Q-13 |
| 004 | OBSERVATION | Out of scope; sequenced after SCA-V4-002 (§8) | stated in OWNER_ITEMS |
| 005 | OBSERVATION | Out of scope; re-pin after the REVISEs (§8). CA1 asks the owner to confirm that DECISION-8 is the deciding record | stated in OWNER_ITEMS |
| 006 | OBSERVATION | B-06a/b/c, register rows 15–16; ARC_EFFECT §4 (manifest-bound `_LATEST_ACCEPTED.md`) | Q-12 (recommend (a)) |
| 007 | OBSERVATION | §7, DEL-09-07 re-extraction brief (DEP-09-07-016 Notes) | — |
| 008 | OBSERVATION | §7, UPDATE of DEL-04-01/02/03 (34 quotes); ARC_EFFECT §4 | — |
| 009 | OBSERVATION | §7, Phase 5.7 report, Phase 3.1 refresh, `STATUS_POLICY=NO_STATUS_TOUCH` | — |

## 10. Lifecycle and reopening

No deliverable is ISSUED or CHECKING, so the amendment authorizes no
reopening. REVISE runs `NO_STATUS_TOUCH`, and no `_STATUS.md` changes
anywhere in this amendment.

## 11. What this node could not prepare, and unknowns

- **The pre-change `audit-decomp` baseline** (§4). It needs a dispatched
  `audit-decomp`, or a documented reuse of CA1's inputs.
- **The decision snapshots, the candidate snapshot, the independent review
  and the post-change audit.** These belong to later stages.
- **Custody:** CA1's snapshot is cited at commit `f5b5d0ad0`, with the two
  hashes in §9.
- **Decision identity:** the full identity
  `APP-V4-BASIS-ALIGN-20260928-DECISION-10` is constructed on the earlier
  pattern; the record labels it "DECISION-10" (SOW_REVISIONS, "Reading this
  file").
- **Unknown until extraction:** the exact number of rows per new arc, and
  whether extractors add EXTERNAL OI-021 rows for DEL-01-04, DEL-09-07 and
  DEL-02-02.
