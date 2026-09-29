# Impact assessment — APP-V4-BASIS-ALIGN-20260928, node P1

**Status: PROPOSED. This is the scope-change checkpoint-group-1 preparation
(change intake and validation; impact assessment), with the group-2
propagation plan outline.** Nothing is applied. No decision snapshot is
written.

- **Executor:** node P1, a Type 2 TASK (Claude Code subagent). It does not
  delegate. Git was used read-only, with no network. Writes are confined to
  this `AMENDMENT_PACKET/` folder and a private scratch folder.
- **Method:** `chirality-root:bundled:workflow:scope-change`
  (`workflows/scope-change/WORKFLOW.md`, `resources/contract.md`,
  `resources/method.md`), checkpoint groups 1 and 2, preparation only. Also
  read: `workflows/scope-of-work/WORKFLOW.md` and `resources/brief.md` (so the
  SoW edits fit MODE=REVISE), and `docs/DELIVERABLE_SCOPE_OF_WORK_STANDARD.md`
  §§3–5, 8.
- **Basis commit:** `874508f16`. The working tree was clean at the start. All
  hashes below were computed at that commit. **Re-checked at `67a2fac4b`**
  (after the baseline commit and the IN_PROGRESS commit): no doc,
  decomposition or ScopeOfWork byte changed; only 14 `_STATUS.md` files did.
- **Revision 2 (this file, after the pre-change baseline, node P3):**
  - the Change Register binding is resolved by a new `## Decision Log`
    heading (COV-127);
  - the stale no-production sentence is corrected (COV-121);
  - the audit scope is set to seven packages;
  - COV-119/120 are recorded as pre-existing;
  - the lifecycle is updated for owner DECISION-6.
- **Companion files:** [BASIS_AMENDMENT.md](BASIS_AMENDMENT.md) (exact basis
  and decomposition text), [SOW_REVISIONS.md](SOW_REVISIONS.md) (exact
  ScopeOfWork text; the C1 refresh), [OWNER_ITEMS.md](OWNER_ITEMS.md)
  (decisions needed).

## 1. Resolution (method step 1)

| Variable | Value | Evidence |
|---|---|---|
| `DECOMP_VARIANT` | `SOFTWARE` | `_Decomposition/SOFTWARE_DECOMP.md`; method `chirality-root:bundled:workflow:software-decomp` (its line 9) |
| `CONTEXT_ROOT` | `projects/chirality-app-v4/execution/` | Variant default |
| `DECOMPOSITION_PATH` | `execution/_Decomposition/SOFTWARE_DECOMP.md` (the only `.md` there), plus the authoritative companion registers in `Companion_Inventory.csv` | — |
| `SCOPE_CHANGE_ROOT` | `execution/_ScopeChange/` | **Does not exist** |
| Candidate posture | **`FIRST_AMENDMENT`**: no `_LATEST.md` and no prior SCA. Group-3 preparation must not create `_LATEST.md` before acceptance | contract §"Candidate posture is exclusive" |
| `AMENDMENT_ID` | Next available: `SCA-001` unqualified, or `SCA-V4-001` with prefix `V4` (`tools/query/scan_next_amendment_id.sh execution/_ScopeChange V4`). **Recommended `SCA-V4-001`** (O-1). The helper was read, not run; the root is absent, so either stem starts at 001 | App v4 already cites chirality-app-dev's `SCA-APP-012` (SOFTWARE_DECOMP.md "carried decisions"). An unqualified ID invites confusion with other projects' `SCA-0NN` |
| `ALLOW_RENUMBERING` | `false`. No renumbering is proposed | — |
| `ALLOWED_PROPAGATION_WRITES` | The SOFTWARE default (the decomposition document, affected `_CONTEXT.md`), **plus the authoritative carriers the group-2 write boundary must name exactly:** the four `docs/` files and 16 `ScopeOfWork.md` files (§9) | contract §`ALLOWED_PROPAGATION_WRITES` |

**Semantic section binding** (by heading text, per
`workflows/audit-decomp/resources/contract.md#variant-section-binding`):

| Semantic section | Bound to | Note |
|---|---|---|
| Change Register | `SOFTWARE_DECOMP.md` § `## Decision Log`, **added by A30 (D-15)** | The software-decomp binding names "Decision Log" and/or "Revision History". The baseline (COV-127) found that no current `##` heading binds under the exact / prefix / substring rule: the nearest, "Artifact coverage and decision/change log", normalizes to "…decision/change log". A30 adds `## Decision Log`, which binds at rank 1 (exact), checked by simulating the rule on the dry-run output. No owner ruling is needed. The anchor is `SOFTWARE_DECOMP.md#decision-log` |
| Unit Ledger | `ScopeLedger.csv` (authoritative companion register) | — |
| Objectives | `Objectives.csv` | Unchanged |
| Primary Partitions | `Packages.csv` | PKG-05 description only, conditional (O-8) |
| Secondary Entities | `Deliverables.csv` | Descriptions and artifacts of DEL-02-03, DEL-05-01 and DEL-09-07 |
| Vocabulary Map | `Vocabulary_Map.csv` | "Declared checkpoint" |
| Coverage Basis | audit-decomp output | **Done:** pre-change baseline `BASELINE/coverage_summary.json` (sha256 `d8ac5c4d35012d6a6fb6a3ef2c509caba08a616c8e14a5601bff2a83ee9620f9`). Scope: PKG-01, 02, 03, 04, 05, 08, 09 (30 deliverables); 0 BLOCKER, 2 WARNING (COV-121, COV-127), 126 INFO |

## 2. Change intake (method step 2)

**The request** (owner, exact: "go ahead with the next undertaking as
recommended"; [OWNER_DECISIONS.md](../OWNER_DECISIONS.md)) has three
admitted, evidence-backed sources:

1. **Owner decisions not yet in the accepted basis.** These are recorded
   exactly in `AgentRuns/APP-V4-SWBPIPE-INTAKE-20260928/OWNER_DECISIONS.md`:
   DECISION-4 D4-1 (phased checkpoints; V4-WF-05's first half phased, not
   withdrawn), DECISION-4 D4-3 (OAuth or API key; no default) and DECISION-5
   (revised V4-HOST-02 and its effects). The run's receipt lists them under
   "For the next accepted-basis update". R8-1, R8-9 and R8-13 give the
   integrator's framing.
2. **The first closeout's SoW proposals.** These are C1-A, C1-B and C1-C (74
   items) with CLOSEOUT_ACCOUNT, written at candidates
   `d3cebd1cc`/`c7f5513db`/`816c917f0`. That was before R6–R8 and DECISION-3/4/5.
3. **Later SoW wording findings:** EXEC F-29, CA F-22, GUIDE G-12 and LOOP G-6
   (with GUIDE G-6 and F-16, ACT F-20, PANEL F-9, ADAPTER F-13's R8 note).

**Currency of the C1 inputs.** Each of the 14 SoWs hashes identically to the
hash C1 compared (for example, DEL-02-03 `9a921ba5…b7fb`). No SoW changed
after C1. The Design files did change (R6–R8), so every C1 item was refreshed
against them (SOW_REVISIONS §"C1 disposition register").

**Not in this assessment:** register rows, arcs and DAG-002 (node P2);
lifecycle recording (an owner item, O-16); host joins, SWBPIPE, PEC and
Domains work (excluded by the graph); new design content.

## 3. Atomic actions (method step 2; the future `Intake_Actions.csv`)

All actions are **MODIFY**. There is no ADD, REMOVE, RECLASSIFY, MERGE or
SPLIT, so no parent-closure set arises. `EntityType` `OTHER` is used for the
basis documents, ledger rows and registers, which the enum does not name.

| # | ActionType | EntityType | EntityID | RequestedChange | AffectedSections |
|---|---|---|---|---|---|
| A01 | MODIFY | OTHER | `docs/PRD.md#V4-WF-05` | First half phased to the governance layer; second half in force (DECISION-4 D4-1) | PRD §4.1 |
| A02 | MODIFY | OTHER | `docs/PRD.md#V4-HOST-01` | Local or cloud by the person's choice; no default; OAuth or API key (D4-3) | PRD §2.2 |
| A03 | MODIFY | OTHER | `docs/PRD.md#V4-HOST-02` | Replace with the DECISION-5 wording, verbatim | PRD §2.2 |
| A04 | MODIFY | OTHER | `docs/PRD.md#2.2` | "local-first agent" → an agent on a model the person chooses (consequential, D4-3) | PRD §2.2 introduction |
| A05 | MODIFY | OTHER | `docs/PRD.md#OQ-03` | "local-operation privacy constraints" → V4-HOST-02 host-agent constraints (consequential, DECISION-5) | PRD §9 |
| A06 | MODIFY | OTHER | `docs/PRD.md#1.1` | Purpose quotation "runs local-first" → "on a model the person chooses … no default". **Conditional (O-8)** | PRD §1.1 |
| A07 | MODIFY | OTHER | `docs/PRD.md#status;#0` | Amendment note; new source key DEC-4/DEC-5 and its link (acceptance-conditional) | PRD status paragraph, §0, link definitions |
| A08 | MODIFY | OTHER | `docs/ARCHITECTURE.md#V4-ARC-11` | No default; OAuth or API key (D4-3) | ARCH §4 |
| A09 | MODIFY | OTHER | `docs/ARCHITECTURE.md#V4-ARC-12` | Native layer allows the selected service and allowed destinations, records them, and keeps keys and credentials out of the script (D4-3; DECISION-5) | ARCH §4 |
| A10 | MODIFY | OTHER | `docs/ARCHITECTURE.md#host-agent-properties` | First property replaced by the DECISION-5 effects | ARCH §4 |
| A11 | MODIFY | OTHER | `docs/ARCHITECTURE.md#1;#2` | Priority 3 description; diagram label (consequential) | ARCH §1, §2 |
| A12 | MODIFY | OTHER | `docs/HOST_INTEGRATION.md#V4-HI-42` | The checkpoint wait phased; the act is recorded only when performed; reserved acts bind (D4-1) | HI §6 |
| A13 | MODIFY | OTHER | `docs/HOST_INTEGRATION.md#8.1` | V4-HOST-02 reference: Domains only as an allowed destination (DECISION-5) | HI §8.1 |
| A14 | MODIFY | OTHER | `docs/HOST_INTEGRATION.md#V4-HI-70` | Run record adds each host-agent destination contacted (consequential, DECISION-5 "recorded") | HI §9 |
| A15 | MODIFY | OTHER | `docs/EXAMINATION.md#V4-EXM-22` | V4-WF-05 verification wording phased (D4-1) | EXAM §4 |
| A16 | MODIFY | OTHER | `docs/EXAMINATION.md#V4-EXM-23` | Verifies the revised V4-HOST-02 (DECISION-5) | EXAM §4 |
| A17 | MODIFY | OTHER | `docs/{ARCHITECTURE,HOST_INTEGRATION,EXAMINATION}.md#status` | Amendment note (acceptance-conditional) | Status paragraphs |
| A18 | MODIFY | OTHER | `SOW-015` | ScopeItemStatement and DecisionRef (D-01) | Scope Ledger |
| A19 | MODIFY | OTHER | `SOW-016` | (D-02) | Scope Ledger |
| A20 | MODIFY | OTHER | `SOW-017` | (D-03) | Scope Ledger |
| A21 | MODIFY | OTHER | `SOW-052` | (D-04) | Scope Ledger |
| A22 | MODIFY | OTHER | `SOW-137` | (D-05) | Scope Ledger |
| A23 | MODIFY | OTHER | `SOW-138` | (D-06) | Scope Ledger |
| A24 | MODIFY | OTHER | `SOW-201` | (D-07) | Scope Ledger |
| A25 | MODIFY | OTHER | `SOW-202` | (D-08) | Scope Ledger |
| A26 | MODIFY | VOCAB_TERM | `Declared checkpoint` | Notes phased (D-09) | Vocabulary Map |
| A27 | MODIFY | PACKAGE | `PKG-05` | Description drops "local-first" (D-13). **Conditional (O-8)** | Primary Partitions; `_CONTEXT.md` of DEL-05-01, DEL-05-02 |
| A28 | MODIFY | OTHER | `OI-001` | Consequence points to DECISION-1 D2; stays OPEN (D-14a). **Conditional (O-17)** | Open_Issues.csv |
| A29 | MODIFY | OTHER | `OI-002` | Consequence points to DECISION-1 D3; stays OPEN (D-14b). **Conditional (O-17)** | Open_Issues.csv |
| A30 | MODIFY | OTHER | `SOFTWARE_DECOMP.md#decision-log` | New `## Decision Log` section holding the amendment entry (D-15; acceptance-conditional; resolves COV-127); correct the stale no-production sentence in "Checkpoint and next stage" (D-16; COV-121) | Change Register; "Checkpoint and next stage" |
| A31 | MODIFY | OTHER | `Consolidated_Coverage.csv` | RECOMPUTE hashes, lines and standing after A01–A17 (B8) | Companion register |
| A32 | MODIFY | DELIVERABLE | `DEL-04-01` | SoW E-0401-01…11 | ScopeOfWork.md |
| A33 | MODIFY | DELIVERABLE | `DEL-04-02` | SoW E-0402-01…08 | ScopeOfWork.md |
| A34 | MODIFY | DELIVERABLE | `DEL-04-03` | SoW E-0403-01…05 | ScopeOfWork.md |
| A35 | MODIFY | DELIVERABLE | `DEL-02-01` | SoW E-0201-01…09 | ScopeOfWork.md |
| A36 | MODIFY | DELIVERABLE | `DEL-02-03` | SoW E-0203-01…13; Deliverables.csv D-10a/b; `_CONTEXT.md` | ScopeOfWork.md; Secondary Entities |
| A37 | MODIFY | DELIVERABLE | `DEL-03-01` | SoW E-0301-01…07 | ScopeOfWork.md |
| A38 | MODIFY | DELIVERABLE | `DEL-03-02` | SoW E-0302-01…07 | ScopeOfWork.md |
| A39 | MODIFY | DELIVERABLE | `DEL-03-03` | SoW E-0303-01…07 | ScopeOfWork.md |
| A40 | MODIFY | DELIVERABLE | `DEL-03-04` | SoW E-0304-01…07 | ScopeOfWork.md |
| A41 | MODIFY | DELIVERABLE | `DEL-01-01` | SoW E-0101-01…04 | ScopeOfWork.md |
| A42 | MODIFY | DELIVERABLE | `DEL-05-01` | SoW E-0501-01…15; Deliverables.csv D-11a–d; `_CONTEXT.md` | ScopeOfWork.md; Secondary Entities |
| A43 | MODIFY | DELIVERABLE | `DEL-05-02` | SoW E-0502-01…07; `_CONTEXT.md` (only if A27) | ScopeOfWork.md |
| A44 | MODIFY | DELIVERABLE | `DEL-09-06` | SoW E-0906-01…06 | ScopeOfWork.md |
| A45 | MODIFY | DELIVERABLE | `DEL-09-09` | SoW E-0909-01…06 | ScopeOfWork.md |
| A46 | MODIFY | DELIVERABLE | `DEL-09-07` | SoW E-0907-01…10; Deliverables.csv D-12a–c; `_CONTEXT.md`. **Conditional (O-19)** | ScopeOfWork.md; Secondary Entities |
| A47 | MODIFY | DELIVERABLE | `DEL-08-01` | SoW E-0801-01…02. **Conditional (O-18)** | ScopeOfWork.md |

### 3.1 Proposed register columns (group 2; the future `Amendment_Actions.csv`)

`ScopeChanging` is proposed for the owner to accept with the register. None
of these deliverables is ISSUED, so no row authorizes a reopening.
`SupersessionBindingPresent` is `YES` where §7 has a row.

```csv
AmendmentID,ActionSeq,ActionType,EntityType,EntityID,Description,AffectedFiles,DownstreamReruns,SupersessionBindingPresent,ScopeChanging
{AMENDMENT_ID},1,MODIFY,OTHER,docs/PRD.md#V4-WF-05,V4-WF-05 first half phased to the governance layer (DECISION-4 D4-1),projects/chirality-app-v4/docs/PRD.md,audit-decomp,YES,YES
{AMENDMENT_ID},2,MODIFY,OTHER,docs/PRD.md#V4-HOST-01,No default between local and cloud; OAuth sign-in or API key (DECISION-4 D4-3),projects/chirality-app-v4/docs/PRD.md,audit-decomp,YES,YES
{AMENDMENT_ID},3,MODIFY,OTHER,docs/PRD.md#V4-HOST-02,Revised wording of DECISION-5,projects/chirality-app-v4/docs/PRD.md,audit-decomp,YES,YES
{AMENDMENT_ID},4,MODIFY,OTHER,docs/PRD.md#2.2,Consequential: agent on a model the person chooses,projects/chirality-app-v4/docs/PRD.md,,NO,NO
{AMENDMENT_ID},5,MODIFY,OTHER,docs/PRD.md#OQ-03,Consequential: V4-HOST-02 host-agent constraint,projects/chirality-app-v4/docs/PRD.md,,NO,NO
{AMENDMENT_ID},6,MODIFY,OTHER,docs/PRD.md#1.1,Purpose quotation: no local default (conditional O-8),projects/chirality-app-v4/docs/PRD.md,,YES,NO
{AMENDMENT_ID},7,MODIFY,OTHER,docs/PRD.md#status,Amendment note and source key DEC-4/DEC-5,projects/chirality-app-v4/docs/PRD.md,,NO,NO
{AMENDMENT_ID},8,MODIFY,OTHER,docs/ARCHITECTURE.md#V4-ARC-11,No default; OAuth or API key,projects/chirality-app-v4/docs/ARCHITECTURE.md,audit-decomp,YES,YES
{AMENDMENT_ID},9,MODIFY,OTHER,docs/ARCHITECTURE.md#V4-ARC-12,Allowed destinations enforced and recorded; credentials out of script,projects/chirality-app-v4/docs/ARCHITECTURE.md,audit-decomp,YES,YES
{AMENDMENT_ID},10,MODIFY,OTHER,docs/ARCHITECTURE.md#host-agent-properties,DECISION-5 effects,projects/chirality-app-v4/docs/ARCHITECTURE.md,,YES,YES
{AMENDMENT_ID},11,MODIFY,OTHER,docs/ARCHITECTURE.md#1,Consequential: priority 3 text and diagram label,projects/chirality-app-v4/docs/ARCHITECTURE.md,,NO,NO
{AMENDMENT_ID},12,MODIFY,OTHER,docs/HOST_INTEGRATION.md#V4-HI-42,Checkpoint wait phased (DECISION-4 D4-1),projects/chirality-app-v4/docs/HOST_INTEGRATION.md,audit-decomp,YES,YES
{AMENDMENT_ID},13,MODIFY,OTHER,docs/HOST_INTEGRATION.md#8.1,V4-HOST-02 reference for Domains,projects/chirality-app-v4/docs/HOST_INTEGRATION.md,,NO,NO
{AMENDMENT_ID},14,MODIFY,OTHER,docs/HOST_INTEGRATION.md#V4-HI-70,Run record adds host-agent destinations,projects/chirality-app-v4/docs/HOST_INTEGRATION.md,,NO,YES
{AMENDMENT_ID},15,MODIFY,OTHER,docs/EXAMINATION.md#V4-EXM-22,Checkpoint verification phased,projects/chirality-app-v4/docs/EXAMINATION.md,audit-decomp,YES,YES
{AMENDMENT_ID},16,MODIFY,OTHER,docs/EXAMINATION.md#V4-EXM-23,Verifies revised V4-HOST-02,projects/chirality-app-v4/docs/EXAMINATION.md,audit-decomp,YES,YES
{AMENDMENT_ID},17,MODIFY,OTHER,docs/*.md#status,Amendment notes,projects/chirality-app-v4/docs/ARCHITECTURE.md;projects/chirality-app-v4/docs/HOST_INTEGRATION.md;projects/chirality-app-v4/docs/EXAMINATION.md,,NO,NO
{AMENDMENT_ID},18,MODIFY,OTHER,SOW-015,Scope row D-01,projects/chirality-app-v4/execution/_Decomposition/ScopeLedger.csv,audit-decomp,YES,YES
{AMENDMENT_ID},19,MODIFY,OTHER,SOW-016,Scope row D-02,projects/chirality-app-v4/execution/_Decomposition/ScopeLedger.csv,audit-decomp,YES,YES
{AMENDMENT_ID},20,MODIFY,OTHER,SOW-017,Scope row D-03,projects/chirality-app-v4/execution/_Decomposition/ScopeLedger.csv,audit-decomp,YES,YES
{AMENDMENT_ID},21,MODIFY,OTHER,SOW-052,Scope row D-04,projects/chirality-app-v4/execution/_Decomposition/ScopeLedger.csv,audit-decomp,YES,YES
{AMENDMENT_ID},22,MODIFY,OTHER,SOW-137,Scope row D-05,projects/chirality-app-v4/execution/_Decomposition/ScopeLedger.csv,audit-decomp,YES,YES
{AMENDMENT_ID},23,MODIFY,OTHER,SOW-138,Scope row D-06,projects/chirality-app-v4/execution/_Decomposition/ScopeLedger.csv,audit-decomp,YES,YES
{AMENDMENT_ID},24,MODIFY,OTHER,SOW-201,Scope row D-07,projects/chirality-app-v4/execution/_Decomposition/ScopeLedger.csv,audit-decomp,YES,YES
{AMENDMENT_ID},25,MODIFY,OTHER,SOW-202,Scope row D-08,projects/chirality-app-v4/execution/_Decomposition/ScopeLedger.csv,audit-decomp,YES,YES
{AMENDMENT_ID},26,MODIFY,VOCAB_TERM,Declared checkpoint,Notes phased D-09,projects/chirality-app-v4/execution/_Decomposition/Vocabulary_Map.csv,,YES,NO
{AMENDMENT_ID},27,MODIFY,PACKAGE,PKG-05,Description D-13 (conditional O-8),projects/chirality-app-v4/execution/_Decomposition/Packages.csv,,NO,NO
{AMENDMENT_ID},28,MODIFY,OTHER,OI-001,Consequence pointer D-14a (conditional O-17),projects/chirality-app-v4/execution/_Decomposition/Open_Issues.csv,,NO,NO
{AMENDMENT_ID},29,MODIFY,OTHER,OI-002,Consequence pointer D-14b (conditional O-17),projects/chirality-app-v4/execution/_Decomposition/Open_Issues.csv,,NO,NO
{AMENDMENT_ID},30,MODIFY,OTHER,SOFTWARE_DECOMP.md#decision-log,New Decision Log section with the amendment entry; COV-121 sentence corrected,projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md,,NO,NO
{AMENDMENT_ID},31,MODIFY,OTHER,Consolidated_Coverage.csv,RECOMPUTE after doc edits,projects/chirality-app-v4/execution/_Decomposition/Consolidated_Coverage.csv,audit-decomp,NO,NO
{AMENDMENT_ID},32,MODIFY,DELIVERABLE,DEL-04-01,SoW revision,ScopeOfWork.md,project-setup(INCREMENTAL);scope-of-work(REVISE),NO,NO
{AMENDMENT_ID},33,MODIFY,DELIVERABLE,DEL-04-02,SoW revision,ScopeOfWork.md,project-setup(INCREMENTAL);scope-of-work(REVISE),NO,NO
{AMENDMENT_ID},34,MODIFY,DELIVERABLE,DEL-04-03,SoW revision,ScopeOfWork.md,project-setup(INCREMENTAL);scope-of-work(REVISE),NO,YES
{AMENDMENT_ID},35,MODIFY,DELIVERABLE,DEL-02-01,SoW revision,ScopeOfWork.md,project-setup(INCREMENTAL);scope-of-work(REVISE),NO,YES
{AMENDMENT_ID},36,MODIFY,DELIVERABLE,DEL-02-03,SoW revision; Deliverables.csv; _CONTEXT.md,ScopeOfWork.md;Deliverables.csv;_CONTEXT.md,project-setup(INCREMENTAL);scope-of-work(REVISE),YES,YES
{AMENDMENT_ID},37,MODIFY,DELIVERABLE,DEL-03-01,SoW revision,ScopeOfWork.md,project-setup(INCREMENTAL);scope-of-work(REVISE),NO,YES
{AMENDMENT_ID},38,MODIFY,DELIVERABLE,DEL-03-02,SoW revision,ScopeOfWork.md,project-setup(INCREMENTAL);scope-of-work(REVISE),NO,YES
{AMENDMENT_ID},39,MODIFY,DELIVERABLE,DEL-03-03,SoW revision,ScopeOfWork.md,project-setup(INCREMENTAL);scope-of-work(REVISE),NO,YES
{AMENDMENT_ID},40,MODIFY,DELIVERABLE,DEL-03-04,SoW revision,ScopeOfWork.md,project-setup(INCREMENTAL);scope-of-work(REVISE),NO,YES
{AMENDMENT_ID},41,MODIFY,DELIVERABLE,DEL-01-01,SoW revision,ScopeOfWork.md,project-setup(INCREMENTAL);scope-of-work(REVISE),NO,NO
{AMENDMENT_ID},42,MODIFY,DELIVERABLE,DEL-05-01,SoW revision; Deliverables.csv; _CONTEXT.md,ScopeOfWork.md;Deliverables.csv;_CONTEXT.md,project-setup(INCREMENTAL);scope-of-work(REVISE),YES,YES
{AMENDMENT_ID},43,MODIFY,DELIVERABLE,DEL-05-02,SoW revision,ScopeOfWork.md;_CONTEXT.md,project-setup(INCREMENTAL);scope-of-work(REVISE),NO,YES
{AMENDMENT_ID},44,MODIFY,DELIVERABLE,DEL-09-06,SoW revision,ScopeOfWork.md,project-setup(INCREMENTAL);scope-of-work(REVISE),NO,YES
{AMENDMENT_ID},45,MODIFY,DELIVERABLE,DEL-09-09,SoW revision,ScopeOfWork.md,project-setup(INCREMENTAL);scope-of-work(REVISE),NO,YES
{AMENDMENT_ID},46,MODIFY,DELIVERABLE,DEL-09-07,SoW revision; Deliverables.csv; _CONTEXT.md (conditional O-19),ScopeOfWork.md;Deliverables.csv;_CONTEXT.md,project-setup(INCREMENTAL);scope-of-work(REVISE),YES,YES
{AMENDMENT_ID},47,MODIFY,DELIVERABLE,DEL-08-01,SoW revision (conditional O-18),ScopeOfWork.md,project-setup(INCREMENTAL);scope-of-work(REVISE),NO,NO
```

This block illustrates the columns. At group-2 finalization, `AffectedFiles`
takes each deliverable's full repository path. Values that contain a comma
are quoted. A value's leading or trailing spaces are removed (contract §
schema).

## 4. Validation (method step 3)

| Check | Result |
|---|---|
| MODIFY: each referenced entity exists | **PASS.** The docs contain V4-WF-05, V4-HOST-01/02, V4-ARC-11/12, V4-HI-42, V4-HI-70 and V4-EXM-22/23. SOW-015/016/017/052/137/138/201/202, the vocabulary term, PKG-05, OI-001/OI-002 and the 16 deliverables exist; none is retired |
| MODIFY: the changes are to valid fields | **PASS.** Ledger `ScopeItemStatement` and `DecisionRef`; vocabulary `Notes`; Deliverables `Description` and `AnticipatedArtifacts`; Packages description; Open_Issues `Consequence`; SoW sections and IDs under SOW_V1 |
| Exact "old" text | **PASS.** By script, every Part A block and all 124 SoW E-blocks (162 replacements) occur exactly once and apply in order. Every Part B field value and substring equals the parsed CSV value, and the `_CONTEXT.md` mirrors hold each substring once |
| Revised SoWs are valid | **PASS, all 16.** `tools/scope_of_work/validate_scope_of_work.py` on the revised copies returned `PASS format=SOW_V1` (with the tokens replaced by placeholders) |
| Boundary-owner resolution | **PASS, all 16.** `check_boundary_owner_resolution.py`: 0 contracts failing and 0 requirements citing no claim, before and after. Dependency: E-0402-03 passes only together with E-0402-02 (O-11) |
| Stable IDs | **PASS.** No ID is renumbered, reused or removed. New local IDs are TBD-004 (DEL-04-01, DEL-02-01), TBD-006 (DEL-04-02, DEL-02-03), TBD-003 (DEL-09-06), TBD-005 (DEL-09-09) and one AX per SoW. Each is the next free number |
| Parent closure | **N/A.** There is no structural action |
| SOFTWARE-specific rules | **PASS.** No package or deliverable lineage change. Deliverable kind and granularity are unchanged (DEL-02-03 stays BACKEND_FEATURE_SLICE, DEL-05-01 API_CONTRACT, DEL-09-07 TEST_SUITE). No package-discipline isolation rule is touched |
| Contract-level change | **None.** No ontology, vocabulary set or section contract changes. "Declared checkpoint" keeps its term and gains the phased reading |
| Supersession | **Required.** Rows are drafted in §7 |

| Pre-change baseline | **Done** (node P3). `BASELINE/coverage_summary.json` sha256 `d8ac5c4d…20f9`, `overall_status` WARNINGS: 0 BLOCKER; WARNINGs COV-121 and COV-127, both addressed by A30 |
| Change Register binding | **PASS after A30.** Before: no heading hits "decision log" or "revision history" at any rank. After the dry run: "decision log" hits exactly one heading at rank 1 (exact) |

**Errors:** none. **Warnings:** W-1 below. **Unknowns:** U-2 in §12 (U-1 and U-3 are resolved).

- **W-1.** `V4-HI-42`'s heading-level claim "declared checkpoints override
  autonomy" becomes "autonomy does not override declared checkpoints … act
  recorded only when performed". Its meaning in force is unchanged: autonomy
  never substitutes the act. Its hold meaning is phased. ACT S9 and the
  "or a declared checkpoint" half of DECISION-1 D2 carry the same phased
  reading (R8-11 item 2, INTEGRATION). DECISION-1 is an owner record; this
  amendment does not rewrite it (O-25).

## 5. Impact by lens (method, group-1 part B)

| Action group | 1. Decomposition structure | 2. Variant-local metadata | 3. Downstream consumers | 4. Invariant and telemetry risk |
|---|---|---|---|---|
| A01, A12, A15, A21, A26 (phased checkpoints) | SOW-052 statement; vocabulary Notes | DEL-02-03 `_CONTEXT.md` | SoWs DEL-02-01, 02-03, 03-03, 03-04, 04-01, 04-02, 05-01, 05-02, 09-06, 09-07. The Design files already carry the phasing (R8-1) but cite the old wording as "flagged": EXEC F-29, CA F-22, GUIDE G-12, WD U-33, ACT F-20/AP-11 and similar. They are closed by the next Design revision (downstream). The hold-related C1 arcs (§10) | Low. SOW-053 (the in-force half) is unchanged. OBJ-003 "truthful checkpoints" and OBJ-005 are still met |
| A02, A08, A18, A19, A23 (model access) | SOW-015/016/138 statements | DEL-05-01 `_CONTEXT.md` | SoWs DEL-05-01, 03-04. LOOP NW-1 and G-6, PANEL F-9 and GUIDE F-16 already follow D4-3. SOW-015's statement no longer "defaults" | Low. No objective changes. OBJ-002's "three user-selectable Codex access modes" concerns the App, not hosts |
| A03, A09, A10, A13, A14, A16, A20, A22, A25 (V4-HOST-02) | SOW-017/137/202 statements | DEL-05-01 and DEL-09-07 `_CONTEXT.md` | SoWs DEL-05-01, 03-03, 03-04, 04-03, 08-01, 09-07. LOOP §5.1 NW-8…NW-16, RS R15, AS §3, PANEL §3.8, ACT §2.7 and GUIDE B-11 already carry DECISION-5 in place (R8-13). **RELAY SQ-16 and SQ-30 keep the old wording as relayed**; R8-7 protects the relayed body. The DECISION-5 host obligations go to SWBPIPE in the next relay (downstream) | Medium. DEL-08-01 (Domains, excluded work) must change CLM-003 or contradict the basis (O-18) |
| A04–A06, A11, A27 (consequential "local-first" and "default" text) | PKG-05 description (conditional) | DEL-05-01 and DEL-05-02 `_CONTEXT.md` | Readers of PRD §1.1 and §2.2 and ARCH §1 | Low. The priority order (maintainability, functionality, local models and privacy) is unchanged |
| A28, A29 (OI-001/002 pointers) | Open_Issues Consequence | — | SoW TBD pointers (C1) | None. The status stays OPEN |
| A32–A47 (SoWs) | — | `ScopeOfWork.md` × 16 (authoritative carriers) | project-setup INCREMENTAL routes each to scope-of-work REVISE; registers and DAG (node P2) | DAG-001 currency departs (§10). The lifecycle is unchanged |

## 6. Package-role classification and derivative surfaces

| Surface | Package role | Classification | Authority basis |
|---|---|---|---|
| `docs/PRD.md`, `ARCHITECTURE.md`, `HOST_INTEGRATION.md`, `EXAMINATION.md` | Accepted-basis carrier outside the decomposition package; treated as a **working surface** named in the group-2 boundary | DIRECT_EDIT | DECISION-4, DECISION-5; APP-V4-BASIS-20260926 |
| `_Decomposition/SOFTWARE_DECOMP.md` | working surface | DIRECT_EDIT: a new `## Decision Log` section (D-15) and one corrected sentence (D-16) | this amendment; baseline COV-121, COV-127 |
| `ScopeLedger.csv`, `Vocabulary_Map.csv`, `Deliverables.csv`, `Packages.csv` (cond.), `Open_Issues.csv` (cond.) | authoritative companion register | DIRECT_EDIT (field level) | DECISION-4, DECISION-5, DECISION-1 |
| `Consolidated_Coverage.csv` | authoritative companion register (hash-bound aliases) | RECOMPUTE | the doc edits |
| `Coverage_Telemetry.json` | derived check artifact | RECOMPUTE (by the post-change baseline) | audit-decomp |
| `Allocation_Rationale.csv`, `Source_Coverage.csv`, `Scope_Classification.csv`, `Source_Sections.csv`, `Objectives.csv`, `ContextBudgetQA.csv`, `External_Dependencies.csv`, `Companion_Inventory.csv` | authoritative companion register | NO_CHANGE | Historical rationale, or original-seed pointers |
| `checkpoint_snapshots/GROUP3-…` and pointers | snapshot / handoff artifact | NO_CHANGE (immutable) | — |
| 16 × `ScopeOfWork.md` | authoritative carrier (deliverable scope), named in the group-2 boundary | DIRECT_EDIT **by scope-of-work REVISE**, one brief each (owner direction) | this amendment |
| `_CONTEXT.md` of DEL-02-03, 05-01, 05-02, 09-07 | working surface (variant default write) | DIRECT_EDIT | mirrors B3/B4 |
| Design files of the 14 (EXEC, WD, ACT, AS, RS, C, P, ADAPTER, GUIDE, HOSTING, LOOP, PANEL, CA, RELAY, XT) | derived publication artifacts of the SoWs and basis | **STALE_REBUILD_REQUIRED** (they pin old SoW and doc hashes, and carry "flagged for the next accepted-basis update" notes) | downstream Design revision; not edited here |
| `Dependencies.csv`, `_DEPENDENCIES.md` | authoritative companion register (per deliverable) | NO_CHANGE by this amendment; register changes go by the node-P2 route | — |
| `_DAG/DAG-001/*` | snapshot / handoff artifact | NO_CHANGE. Its currency departs (§10) | — |
| `_Coordination/HANDOFF_SWBPIPE_DOMAINS.md`; the RELAY file | coordination artifacts | NO_CHANGE (the relayed body is protected, R8-7). The next relay carries the DECISION-5 obligations | — |

## 7. Supersession_Delta (draft rows; required by the contract)

Each amended fact overrides a fact of the accepted composite's original
seed (`execution/_Coordination/Acceptances/APP-V4-BASIS-20260926/original-seed/`).
`SupersededAuthorityRole` is `OTHER` (the accepted product basis).
`AppliesToRoots`, `AppliesToFacilities` and `AppliesToSections` are empty:
the binding applies globally.

| DecisionID | SupersededAuthorityRef | SupersededFactKey | Original (abridged) | OverrideType | Replacement (abridged) |
|---|---|---|---|---|---|
| D-001 | original-seed/PRD.md#V4-WF-05 (line 159); ScopeLedger SOW-052 | V4_WF_05_CHECKPOINT_HOLD | "The product holds a workflow's declared checkpoints … the run waits" | SUPERSESSION (phased: in force again for workflows in the governance phase) | Act requested and recorded only when performed; holding phased to the governance layer (DECISION-4 D4-1) |
| D-002 | original-seed/PRD.md#V4-HOST-01; ScopeLedger SOW-015, SOW-016 | V4_HOST_01_MODEL_DEFAULT | Local model server by default; cloud only with an API key | SUPERSESSION | Local or cloud by the person's choice, no default; OAuth or API key (D4-3) |
| D-003 | original-seed/PRD.md#V4-HOST-02; ScopeLedger SOW-017 | V4_HOST_02_DESTINATIONS | "In local operation … no data to any destination other than the configured model server" | SUPERSESSION | DECISION-5 wording (selected service + person-allowed destinations; record and show) |
| D-008 | original-seed/ARCHITECTURE.md#V4-ARC-11 | V4_ARC_11_MODEL_DEFAULT | Local model server by default | SUPERSESSION | As D-002 |
| D-009 | original-seed/ARCHITECTURE.md#V4-ARC-12; ScopeLedger SOW-137, SOW-138 | V4_ARC_12_NETWORK | Native layer enforces the configured endpoint; key outside script | SUPERSESSION | Native layer allows the selected service and allowed destinations, records them; key or sign-in credential outside script |
| D-010 | original-seed/ARCHITECTURE.md §4 host-agent property | HOST_AGENT_LOCAL_ONLY_PROPERTY | "In local operation it makes no network request other than to the configured model server" | SUPERSESSION | DECISION-5 effects |
| D-012 | original-seed/HOST_INTEGRATION.md#V4-HI-42 | V4_HI_42_CHECKPOINT_OVERRIDE | "at a checkpoint the run waits" | SUPERSESSION | As D-001 |
| D-015 | original-seed/EXAMINATION.md#V4-EXM-22; ScopeLedger SOW-201 | V4_EXM_22_CHECKPOINT_STOPS_RUN | "A workflow checkpoint stops the run" | SUPERSESSION | As D-001, for the examination |
| D-016 | original-seed/EXAMINATION.md#V4-EXM-23; ScopeLedger SOW-202 | V4_EXM_23_ENDPOINT_ONLY | "no request goes anywhere but the configured model server" | SUPERSESSION | Verifies the revised V4-HOST-02 |
| D-006 | original-seed/PRD.md §1 purpose (conditional O-8) | PURPOSE_LOCAL_FIRST | "runs local-first" | SUPERSESSION | "on a model the person chooses … no default" |
| D-026 | Vocabulary_Map "Declared checkpoint" | VOCAB_DECLARED_CHECKPOINT | "Run waits for an identified human act …" | SUPERSESSION | Phased reading |

`DecisionID` uses `D-{ActionSeq}` of the basis action. Each row also covers
the ledger and deliverable actions named in its reference: A18–A25, and A36,
A42 and A46 for their Deliverables.csv text. Those register rows are marked
`SupersessionBindingPresent` `YES` accordingly. `Supersession_Map.csv` is
cumulative and starts with these rows, since this is the first amendment.

## 8. Derivative-package status after the amendment

| Package | Owner | Status | Required action |
|---|---|---|---|
| Design definitions of the 14 deliverables (plus DEL-09-07 and DEL-08-01, which have none) | Each deliverable's Design owner (the graph maintainer dispatches) | STALE_REBUILD_REQUIRED | Next in-place pass: re-pin the SoW and doc hashes; close EXEC F-29, CA F-22, GUIDE G-12/G-6/F-16, LOOP G-6, WD U-33, ACT F-20, PANEL F-9 and the "flagged for the next accepted-basis update" notes. GUIDE is re-pinned last |
| Consolidated_Coverage.csv | Decomposition owner (in this amendment) | RECOMPUTE in the candidate | Script recompute (B8) |
| Coverage_Telemetry.json and the post-change baseline | audit-decomp (TASK) | STALE_REBUILD_REQUIRED (already stale before the amendment: COV-119, COV-120) | Post-change baseline, same seven-package scope as the pre-change baseline |
| DAG-001 (accepted graph) | project-dag (node P2 → D1) | Currency DEPARTURE on application | Currency audit, then the DAG-002 candidate |
| Registers (`Dependencies.csv`) | dependency-extract, per deliverable | Not changed by this amendment | Node P2 route. Several new-arc rows depend on SoW edits here (§10) |
| RELAY/SWBPIPE handoff | App manager / human | CURRENT as relayed; next relay pending | Carry DECISION-5 obligations (M7.9, HC-7.7…HC-7.9) when UI-SUCCESSOR resumes (DECISION-3) |

## 9. Propagation plan outline (group-2 part B)

**Write boundary proposed for the group-2 decision** (to be named exactly):

1. `projects/chirality-app-v4/docs/PRD.md`, `ARCHITECTURE.md`,
   `HOST_INTEGRATION.md`, `EXAMINATION.md`: Part A of BASIS_AMENDMENT.
2. `execution/_Decomposition/`: `SOFTWARE_DECOMP.md`, `ScopeLedger.csv`,
   `Vocabulary_Map.csv`, `Deliverables.csv`, `Consolidated_Coverage.csv`, and
   conditionally `Packages.csv` and `Open_Issues.csv`: Part B.
3. `_CONTEXT.md` of DEL-02-03, DEL-05-01, DEL-09-07, and DEL-05-02 (if O-8).
4. The 16 `ScopeOfWork.md` files: **applied by `scope-of-work` MODE=REVISE,
   one brief per deliverable** (owner direction). Each brief carries
   `AMENDMENT_REF` (ID, accepted group-3 snapshot, the deliverable's action
   row, register hash), `REVISION_SCOPE` (the list heading each deliverable in
   SOW_REVISIONS), `PRIOR_CONTRACT_SHA256` (SOW_REVISIONS summary),
   `SOURCE_STATE` (INITIALIZED or IN_PROGRESS; both are admitted),
   `STATUS_POLICY=NO_STATUS_TOUCH`, and a closing `MODE=VERIFY`.

**Ordering.** The scope-of-work workflow says REVISE applies when an accepted
amendment has group 3 accepted. The graph's node A* ("Apply") follows K1
(groups 1+2). Reconciling the two: the docs, decomposition and `_CONTEXT.md`
edits are the scope-change candidate poststate (group-3 preparation). The
REVISE briefs then run against the accepted group-3 snapshot, or, if the owner
so directs at K1, against the accepted group-2 snapshot as the candidate's
carrier writes (item O-3). The graph's K2 then also takes scope-change group
3.

**Not executed by this amendment:** register rows and new arcs (node P2,
dependency-extract, project-dag); lifecycle transitions (the human or
WORKING_ITEMS, O-16); Design re-pinning (downstream); the relay.

**Pre-existing findings, not amendment effects.** The pre-change baseline
records these conditions before any edit. The post-change comparison must
not attribute them to this amendment:
- **COV-119 (INFO).** `Coverage_Telemetry.json` counts 24 active open issues
  and resolved OI-015/OI-025. The working Open_Issues.csv has 23 OPEN, with
  OI-015, OI-017 and OI-025 non-OPEN. This is a later standing update against
  the frozen Group3 telemetry.
- **COV-120 (INFO).** The same telemetry still carries the candidate-era
  standing and the check `no_production_folders_or_SoWs_created=true`, while
  the 41 deliverable folders now exist.

Both are closed by the RECOMPUTE of `Coverage_Telemetry.json` (§8).
COV-122 to COV-126 (INFO) and the non-Change-Register part of COV-127 are
also pre-existing. The first concern pointers and later standing files; the
second, companion-register bindings through `Companion_Inventory.csv`. They
are routed to the decomposition owner as they stand.

**Closure validation before group 3:** an audit-decomp post-change baseline
over **the same seven-package scope as the pre-change baseline (PKG-01, 02,
03, 04, 05, 08, 09; 30 deliverables)**, compared with
`BASELINE/coverage_summary.json`. PKG-01 is included because A41 modifies
DEL-01-01. Expected changes: COV-121 and the Change Register part of COV-127
close, and COV-119/120 close on the telemetry recompute. After that:
- `validate_scope_of_work.py` and `check_boundary_owner_resolution.py` on
  each revised SoW;
- a diff that confines each SoW change to its REVISION_SCOPE;
- the Consolidated_Coverage recompute;
- an independent review of the candidate.

**Checkpoint grouping.** The graph presents scope-change groups 1 and 2
together at K1. The contract still requires two immutable decision snapshots,
`{AMENDMENT_ID}_GROUP-1_{date}` and `{AMENDMENT_ID}_GROUP-2_{date}`, each with
`DECISION.md`, `ACCEPTED_MANIFEST.csv` and `Handoff_State.md`. The group-2
snapshot binds the register `Amendment_Actions.csv` by hash. One owner act can
be recorded in both, provided it addresses both subjects.

## 10. DAG impact

**DAG-001 source bytes.** `SOURCE_MANIFEST.sha256` binds all 41
`ScopeOfWork.md`, `Dependencies.csv` and `_DEPENDENCIES.md` files, the Group3
snapshot's canonical CSVs and `DECISION.md`, `_LATEST_ACCEPTED.md` and
`_Coordination/_COORDINATION.md`. The manifest passes at `874508f16`
(`shasum -c`: 0 failures).

| Edit set | Changes DAG-001 source bytes? |
|---|---|
| SoW edits of **16 deliverables**: DEL-01-01, 02-01, 02-03, 03-01, 03-02, 03-03, 03-04, 04-01, 04-02, 04-03, 05-01, 05-02, 09-06, 09-09, and conditionally DEL-09-07 and DEL-08-01 | **Yes.** All 16 paths are in the manifest. Up to 16 of 41 SoW entries will fail, so the currency audit records a DEPARTURE |
| Basis docs (Part A) | No (not bound) |
| Working decomposition CSVs and `SOFTWARE_DECOMP.md` (Part B) | No. The manifest binds the immutable GROUP3 canonical copies, not the working files |
| `_CONTEXT.md` | No (not bound) |

**Arcs.** DAG-001 derives arcs only from register rows (`GRAPH_BASIS.md`
rules 1–7; the consumer's UPSTREAM row is the representative). **No SoW edit
here adds, removes or reverses an arc**, and this amendment edits no register.
Two SoW-level effects matter for node P2:

1. **Paired evidence for proposed arcs.** Under CONSERVATIVE extraction a new
   register row needs positive SoW evidence (C1-C conventions). These SoW
   edits supply it:

   | SoW edit | C1 arcs it grounds (consumer → supplier) |
   |---|---|
   | E-0402-02 (O-11) | N-01 DEL-04-02→03-01; N-02 DEL-04-02→02-03; receivers of N-03…N-07 |
   | E-0403-01 | N-10 →03-01; N-13 →02-03; N-14 →03-03; N-15 →01-01 (conditional) |
   | E-0201-01, -02, -03 | N-16 DEL-02-01→01-01; N-18 →03-02; the DEL-03-03 receiver of N-20 |
   | E-0203-04, -07 | N-21 DEL-02-03→03-02; N-07 →04-02; N-23 →01-01; N-24 →03-03 |
   | E-0304-06 (O-13) | N-B9 DEL-03-04→01-01; N-B10 →09-06; N-B11 →09-09 |
   | E-0501-06 | N-03 DEL-05-01→04-02 (R5-1-1) |
   | E-0502-02; E-0502-03 (O-12) | N-04 DEL-05-02→04-02; N-25 DEL-05-02→02-03 |
   | E-0906-03 | R9-6-1…3: DEL-09-06 → 02-01, 02-02, 03-01, 03-02, 03-03, 04-01, 04-02, 01-01 |
   | E-0909-04 | R9-9-1…3: DEL-09-09 → 05-01, 04-02, 02-03 |
   | **P2 grounding sentences** (added after node P2 reported): E-0301-07; E-0201-06; E-0201-01; E-0203-04; E-0303-07 with E-0303-04; E-0302-07; E-0402-08 (O-15); E-0403-01 | N-11; N-17; N-20; N-22; N-27 and N-B4; N-B3; R8-A; R8-B (ARC_ANALYSIS §2.3). E-0203-04 also grounds X-1 (O-28) |

   If the owner declines a conditional edit, its paired arc loses its SoW
   evidence (O-11, O-12, O-13, O-15). P2's refreshed set drops N-12 and N-B8.
   No edit here grounds them (SOW_REVISIONS §"Grounding for node P2's nine
   arcs").
2. **Changed grounds for the hold-related arcs.** Under DECISION-4, hold
   support and the hold machine are governance-phase. The SoW edits relabel
   them and keep them; nothing is deleted. The consumed meaning becomes
   "checkpoint recording, plus retained governance-phase hold definitions".
   These arcs keep a ground, and P2 has re-read them against the phased
   text: it amends the statements of N-02, N-13, N-17, N-25, N-26 and N-27 and
   drops N-B8. The SoW edits here use the same phased wording.
3. **The disputed arc DEL-03-02 → DEL-04-03 (C1-A N-12).** No SoW edit here
   bears on it (C1-B: P has no "Expect from DEL-04-03"). P2 recommends not
   proposing it, which matches the owner's lean.
4. **SCC guards.** No SoW edit adds an input to DEL-04-01, DEL-09-06 or
   DEL-01-01 from an SCC-002 member in the reverse direction. The three relay
   pointers inside SCC-002 member SoWs carry an explicit "coordination route,
   not an input" statement (ARC_ANALYSIS E-1). A before/after comparison of
   deliverable mentions per section confirms that the new mentions are only
   the intended ones.

## 11. Lifecycle and reopening

| Deliverables | `_STATUS.md` | Consequence |
|---|---|---|
| DEL-01-01, 02-01, 02-03, 03-01, 03-02, 03-03, 03-04, 04-01, 04-02, 04-03, 05-01, 05-02, 09-06, 09-09 | **IN_PROGRESS**, recorded under owner DECISION-6 (`APP-V4-BASIS-ALIGN-20260928` OWNER_DECISIONS, "Checkpoint A"; commit `67a2fac4b`) | REVISE admits IN_PROGRESS (`SOURCE_STATE`) |
| DEL-09-07, DEL-08-01 | **INITIALIZED** | REVISE admits INITIALIZED |

**REVISE preconditions still hold** for all 16:
- no deliverable is CHECKING or ISSUED, so there is no `UNSUPPORTED_STATE`,
  no reopening, and no `write_status.sh --amendment` path;
- each prior contract still validates and is byte-identical to the
  `PRIOR_CONTRACT_SHA256` in SOW_REVISIONS (re-checked at `67a2fac4b`);
- the briefs set `SOURCE_STATE` to IN_PROGRESS for the 14 and INITIALIZED
  for DEL-09-07 and DEL-08-01, with `STATUS_POLICY=NO_STATUS_TOUCH`.

## 12. Items the workflow requires that P1 could not prepare, and unknowns

- **U-1. Pre-change baseline (method step 5): RESOLVED.** Node P3 ran
  `audit-decomp` over PKG-01, 02, 03, 04, 05, 08 and 09 (30 deliverables) at
  basis `306291bdd`. Output: `BASELINE/coverage_summary.json` (sha256
  `d8ac5c4d35012d6a6fb6a3ef2c509caba08a616c8e14a5601bff2a83ee9620f9`),
  `overall_status` WARNINGS, 0 BLOCKER. The GROUP3 audit was not reused
  because three inputs differ. The post-change audit uses the same scope
  (§9).
- **U-2. Snapshot artifacts in `_ScopeChange/`.** `Brief.md`,
  `Intake_Actions.csv`, `Impact_Assessment.md`, `Amendment_Preview.md`,
  `Propagation_Plan.md`, `Amendment_Actions.csv`, `Supersession_Delta.csv`,
  `Supersession_Map.csv`, `Decision_Log.md` and the decision snapshots are not
  written: P1's write scope is this folder. Their full content is here (§§2–9)
  and in BASIS_AMENDMENT and SOW_REVISIONS. The integrator transcribes them
  into `execution/_ScopeChange/{AMENDMENT_ID}_…/` and
  `checkpoint_snapshots/` after the owner acts.
- **U-3. Change-register binding: RESOLVED by A30.** The baseline confirmed
  that the judgment binding failed under the exact rule (COV-127). A30 (D-15)
  adds `## Decision Log`, which binds exactly (§1).
- **Estimate and schedule staleness:** none. No estimate or schedule artifacts
  exist for App v4.
- **Orphan risk:** none. There is no REMOVE and no structural action.
