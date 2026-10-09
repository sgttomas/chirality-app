# Project execution basis and manual application — the account

- **Contribution:** DEL-10-01/EB-v0.4. It supersedes EB-v0.3 (sha256
  `e9f7e9a6100f805d1bfd992bc681056d3ef68b21c203750d69b1a3def6f904ee`,
  committed at `d0e88a52f1`; RV3: READY, addendum 2), which superseded
  EB-v0.2 (sha256
  `f9b8911f027880a72ca08149a42b19c4dc814c35cac7153f64db6cd8778cd61f`,
  committed at `d43665498d`). That superseded EB-v0.1 (sha256
  `e24101b210b9ef16347d9747169034b19b1f1ef5971e7cc31039b97cbc013baa`,
  which the isolated reader RR-EB1 read). See "Changes". It serves OUT-001
  (§2, §3), OUT-002 (§4, §5) and OUT-003 (§6); verification design is in §8.
- **Status:** DRAFT DEFINITION, unit EB-1 of run
  `APP-V4-DESIGN-PASS-4-20261003`, owner O-E (Type 2 TASK, Claude Opus 5.5),
  2026-10-04. It records no act, adopts nothing and accepts nothing.
- **What it is (R23-31.1):** an index over the project's existing records.
  The records are the authority, and this file restates none of their
  decisions. Where this file and a record differ, the record governs and
  this file is in error.
- **Basis:**
  - this deliverable's `ScopeOfWork.md`, sha256
    `7a89fc3874386d42aacd2ddbc2b10b96fca2dac126ff9a8c4c717a89d22b9b47`
    (INIT contract; no SCA-V4-001/002/003 block changed it, so R23-5's re-pin
    has no block to read);
  - `docs/OPERATING_METHOD.md`, sha256 `98836b5240ed235e…` (V4-OPS-01, 04,
    10–14, 31–34, §7).
- **Rulings (cited by ID, R23-21):** R23-28, R23-30, R23-31 (items 1, 2, 5),
  R23-32 (F-R16), R23-34 (item 9), R23-35 (which supersedes R23-31 item 3),
  R23-38 and R23-42 (item 1).
- **Labels:** SETTLED, DERIVED, INTEGRATION and PROPOSED, as in R9.
  **States** marks what a record says. **Inference** marks O-E's reading.
  **Checked by O-E** marks a fact O-E established with a tool (Git, hashing)
  that no supplied record states.
- **Paths:** relative to the repository root unless they start with `E/`
  (`projects/chirality-app-v4/execution/`) or `RUN/`
  (`E/_Coordination/AgentRuns/APP-V4-DESIGN-PASS-4-20261003/`).

## 1. Who does what here

| Act | Actor | Record |
|---|---|---|
| Choosing the manuals as core practice | The owner, in the accepted basis (directions A/C; OPERATING_METHOD §1) | Acceptance records; CURRENT_EXECUTION_BASIS states it |
| Consequential adoption or departure | The owner (CLM-004; V4-OPS-13) | The owner's decision record |
| Recording edition identities; each undertaking's basis binding (R23-35) | The "project-definition manager": HELP_HUMAN in the WORKING_ITEMS function (R23-31.2). WORKING_ITEMS wrote CURRENT_EXECUTION_BASIS | `E/_Coordination/CURRENT_EXECUTION_BASIS.md`; per-run binding files such as `RUN/BASIS_BINDING.md` |
| Preparing this account and proposing changes to the above | O-E | This file; `RUN/OWNERS/O-E.md` |
| Lifecycle transitions | WORKING_ITEMS (here HELP_HUMAN; R23-28, R23-31.9, R23-34.9) | `_STATUS.md` |

## 2. The basis chain (OUT-001; REQ-001, REQ-006; AC-001, AC-006)

Each row is an act a record states. The "Recorder" column says who
transcribed the act and who wrote the record, as the record says; where a
record does not name its writer, the row says so. Exact words are quoted
where short. In every case custody is a transcription of chat text: no
record claims a raw platform export, and none claims platform
authentication.

| # | Act and date | Actor | Exact words (short) or where they are | Recorder / record | Subject | What it did not decide (as the record states) |
|---|---|---|---|---|---|---|
| B-1 | Composite basis accepted, 2026-09-26 | Owner | "I accept this revised PRD and companion seed set as the basis for Chirality App v4.0 decomposition, including its stated open matters and external dependencies. Proceed with decomposition and project definition." (message M/U4) | WORKING_ITEMS under HELP_HUMAN; `E/_Coordination/Acceptances/APP-V4-BASIS-20260926/ACCEPTANCE.md`, `OWNER_DIRECTIONS.md` | APP-V4-BASIS-20260926 (`COMPOSITE_BASIS.json`) | That the owner saw the later consolidated bytes; an unseen ScopeLedger, packages or snapshots |
| B-2 | Revalidation clarification, 2026-09-27 | Owner | "Yes that matches. I accept your recommendations and planned courses of action. …" | Transcribed by HELP_HUMAN for WORKING_ITEMS; written by WORKING_ITEMS ("WORKING_ITEMS authored this bounded correction"); `E/_Coordination/Changes/APP-V4-CLARIFICATION-20260927/DIRECTION.md` | The revalidation recommendations and the conditional-reuse interpretation | Unseen revised Group1 bytes |
| B-3 | Group1 confirmed | Owner | "Confirm the revised Group 1 package" | HELP_HUMAN relayed to WORKING_ITEMS; `E/_Decomposition/checkpoint_snapshots/GROUP1-20260927T222641Z/DECISION.md` | Candidate 2 (234 IN / 15 OUT / 13 TBD) | "does not accept unseen Packages/Deliverables, settle the carried technical choices, activate setup or establish provider readiness" |
| B-4 | Group2 approved | Owner | "Okay then I have enough to accept all five recommendations and approve the group 2." | Supplied by HELP_HUMAN; `…/GROUP2-20260927T233018Z/DECISION.md` | The presented and discussed Group2 content | "not newly generated Candidate2 hashes"; "not Group3/final-decomposition acceptance …" |
| B-5 | Final decomposition accepted (Group3); recorded 2026-09-28 00:10:55 UTC (a recording time, not the act's time) | Owner | "The human accepts it as the basis for downstream use." (recorded as exact, though worded in the third person) | HELP_HUMAN relayed ("the parent"). **The record does not name its writer.** `…/GROUP3-20260928T001055Z/DECISION.md` | `APP-V4-GROUP3-20260927-CANDIDATE-1`: reader `b5bd5ca2…`, manifest `7ad67229…`; 11 packages, 41 deliverables, 262 scope IDs | Coordination policy, dependencies, a future DAG, the 30% position, implementation |
| B-6 | Initial setup approved | Owner | "Approve the recommended setup plan" | HELP_HUMAN relayed. **The record does not name its writer.** `E/_Coordination/_COORDINATION.md` | `INITIAL_SETUP_PROPOSAL_2026-09-27.md` (`7183957c…`): DEPENDENCY_TRACKED, FULL_GRAPH, INITIAL | Later project-dag basis and version decisions |
| B-7 | 30% gate completed; DAG-001 accepted. Then a hold on the originating session | Owner (Ryan) | "I have reviewed and now approve the 30% package, marking the gate complete and opening up the next phase of work towards the 60% gate." Then "DO NOT BEGIN THE WORK TOWARDS 60%.  We are handing that off." and "finish your tasks that were interrupted." | `/root`, completing an interrupted WORKING_ITEMS closeout; `E/_DAG/DAG-001/ACCEPTANCE_RECORD.md` | APP-V4-30PCT-20260928-CANDIDATE-1 / DAG-001 | Satisfied dependencies, closed SCCs, advanced lifecycles, selected policies, release |
| B-8 | SCA-V4-001 group 3 accepted, 2026-09-29 | Owner | "Accept (Recommended)" (exact label, as transcribed in the record's "The owner's act (verbatim)") | Node AK2 (Type 2), from run `APP-V4-BASIS-ALIGN-20260928`'s OWNER_DECISIONS, DECISION-8; `E/_ScopeChange/checkpoint_snapshots/SCA-V4-001_GROUP-3_2026-09-29/DECISION.md` | The audited poststate | "any edit not on the acceptance-conditional list" (its "It does not authorize" list) |
| B-9 | SCA-V4-002 group 3 accepted, 2026-09-29 | Owner | "Accept (Recommended)" (exact label, as transcribed) | Node AK2, from run `APP-V4-SCA002-20260929`'s OWNER_DECISIONS, DECISION-3; `…/SCA-V4-002_GROUP-3_2026-09-29/DECISION.md` | The audited poststate | "any edit not on the acceptance-conditional list"; no register or `_DAG/` write |
| B-10 | SCA-V4-003 group 3 accepted, 2026-10-03 | Owner | "I accept the audited result." | Node AK2, from run `APP-V4-SCA003-20261002`'s DECISION-2. The writer of that OWNER_DECISIONS is not named in the supplied records. `…/SCA-V4-003_GROUP-3_2026-10-03/DECISION.md` | The audited poststate; closure `OPEN_PENDING_DERIVATIVE_CLOSURE` | "any edit not on the presented acceptance-time list"; no ScopeOfWork, register or `_DAG/` write |
| B-11 | DAG-004 accepted, 2026-10-03; covers project-dag checkpoints 1 and 2 | Owner | "I accept DAG-004." | Node D2 (Type 2), from run `APP-V4-SCA003-20261002`'s DECISION-3 (the owner's chat message to HELP_HUMAN); D2 "did not witness the chat". `E/_DAG/DAG-004/ACCEPTANCE_RECORD.md` | The 33 files of `REVIEW_PACKET.md`, assembled on basis `75764184…` | Any satisfied dependency, lifecycle change, lifted hold, gate passage, schedule, closed SCC or resolved issue (its "This acceptance does not" list) |
| B-12 | Pass-4 direction, 2026-10-03 | Owner | "1 yes, 2 no rewrite, 3 go, 4 A+C" | HELP_HUMAN; `RUN/OWNER_DECISIONS.md` "Direction" | Four items: (1) DEL-09-02's OI-009 wording carried to the next amendment; (2) Git history not rewritten; (3) HELP_HUMAN prepares the AGENTS.md instruction-change package; (4) design pass 4 (A) and a Codex 0.160.0 version-advance check (C) | Applying the instruction change ("a later owner act", B-16); the download (B-13) |
| B-13 | Download for the version check, 2026-10-03 | Owner | "yes, download it" | HELP_HUMAN; `RUN/OWNER_DECISIONS.md` "Download for the version-advance check" | One named file, `codex-0.160.0-darwin-arm64.tgz`, to the session scratch folder only | "Any other download, or a sign-in" |
| B-14 | Coordination method directed, 2026-10-03 | Owner | "ensure you read the new `coodinated-knowledge-work` and apply it …", then "`coordinated-knowledge-work` (spelling corrected)" | HELP_HUMAN, which selected the source-qualified identity and recorded its hash; `RUN/OWNER_DECISIONS.md` "Coordination method" | `bundled:chirality-root/coordinated-knowledge-work` (§3.2) | — |
| B-15 | Scope of owner questions, 2026-10-03 | Owner | "I don't want to expand governance structures and bring in human decision making where it doesn't belong." | HELP_HUMAN; `RUN/OWNER_DECISIONS.md` | How HELP_HUMAN brings matters to the owner; K-1…K-10 returned to HELP_HUMAN | — |
| B-16 | D-GOV-52 application approved, 2026-10-04 | Owner | "I approve A1 and B1, go ahead" | HELP_HUMAN; `RUN/OWNER_DECISIONS_2.md`. Also in tranche `docs/governance_harness/tranche_manifests/ROOT-DGOV52-APPLICATION-20261004.yaml`, `m2_gate`, which does not name its own writer | `AGENTS.proposed.patch` (A1 + B1) applied to Root `AGENTS.md` (result sha256 `f96feb19…`, as the manifest states) | App v4's adoption (HELP_HUMAN's R23-30); U-A9 (HELP_HUMAN); App v3's and Runtime's receiving decisions (R23-32 F-R16: "notice delivered; receiving decision not recorded") |
| B-17 | Tranche 2 started, 2026-10-04 | Owner | "Proceed accordingly." | HELP_HUMAN; `RUN/OWNER_DECISIONS_2.md` | Tranche 2 under the same method and rulings | — |
| B-18 | Review independence for design units, 2026-10-04 | Owner | "Same-session review is acceptable.  It's a practical concession to making the logistics easier." | HELP_HUMAN; `RUN/OWNER_DECISIONS_2.md` "Review independence for design units" | R23-31.5 confirmed as the owner's practice for design units: a same-model reviewer instance in the HELP_HUMAN session is acceptable when it did not author the work and its identity is reported | A claim of model-family independence; V4-OPS-34 for product candidates (EXP §7, R23-12), which is unchanged |
| B-19 | App v4 loop entry revised, 2026-09-28 (listed last; it predates B-8) | Owner (Ryan) | The tranche manifest records the owner's request: "Owner copied init/ and loop/ from chirality-app-dev, reset receipts, and requested: Revise the documents accordingly for the new project folder." | `docs/governance_harness/tranche_manifests/APP-V4-LOOP-ENTRY-20260928.yaml` `m2_gate`: `authorized_by: Ryan`, `integration_owner: Codex HELP_HUMAN /root`, `merge_gate: owner-authorized-pr`, `self_merge: true`. **The manifest does not name its own writer.** Committed in `afc65e2b22` and merged in PR #1037 | The revision of `init/` and `loop/` for App v4, including LOOP_INIT's v4 text (whose bytes have not changed since that commit) | **Not stated by any record: that the owner reviewed or approved the resulting text** (R23-42.1). The owner requested the revision; Codex HELP_HUMAN wrote and self-merged it under the owner-authorized PR gate |

**Order of the DAG successors (states, from the records and Git).**
- DAG-002 was accepted 2026-09-29, between B-8 and B-9. It was published
  before SCA-V4-002's group-3 act.
- DAG-003 was accepted 2026-09-29, after B-9.

Their records are in `E/_DAG/`.

### 2.1 Acts that are not the owner's (REQ-006; AC-006 negative cases)

| Item | Actor | Record | Not to be read as |
|---|---|---|---|
| R23 rulings (R23-1 onward; the file is append-only) | HELP_HUMAN | `RUN/R23_RESOLUTIONS.md` | Owner decisions. The owner returned K-1…K-10 to HELP_HUMAN (B-15). Some rulings carry an owner act forward (R23-11 from "1 yes"; R23-30 after B-16) without becoming one |
| INITIALIZED → IN_PROGRESS for tranche 1, PKG-10 and five tranche-2 deliverables | WORKING_ITEMS function (HELP_HUMAN), by `write_status.sh` | R23-28; R23-31.9; R23-34.9 | Owner acts; or evidence that any input is satisfied |
| App v4's adoption of D-GOV-52; U-A9 "yes" | HELP_HUMAN | R23-30 | The owner's own adoption decision. B-16 approved the Root application, on terms that included HELP_HUMAN ruling U-A9 |
| The first statement on review independence (R23-31.5) | HELP_HUMAN | R23-31.5 | It *was* HELP_HUMAN's ruling. The **owner then confirmed it (B-18)**, so the practice now rests on the owner's act |
| Passing checks, merges, written proposals | Agents and CI | — | Human acceptance (CLM-004, REQ-006) |

## 3. Pins and basis bindings (OUT-001; REQ-002; AC-002)

### 3.1 Manual editions and the definition-run methods

**States.**
1. *Selection, recording and scope.* CURRENT_EXECUTION_BASIS says "The
   human selected the three manuals as core practice in the accepted basis".
   WORKING_ITEMS, as the "Owning project-definition manager named by
   OI-017", "records the following existing edition choices and exact
   identities", which "were already named in the supplied basis and targeted
   task briefs". HELP_HUMAN confirmed the scope ("this App-v4 definition
   run/current execution basis only"), recorded there as "a parent
   clarification of the existing direction".
2. *Later undertakings.* The record also says "a later undertaking or
   changed source must bind its own applicable basis before reliance". OI-017
   stands at `RESOLVED_FOR_CURRENT_DEFINITION_RUN`.

**Checked by O-E** (2026-10-04, `prototype/eb1_check.py`, P-1/P-2): every
row below equals today's bytes and the bytes at Git
`ffb2b6289dde79a35f22f5d87256df0aa4d3289a`, the commit CURRENT_EXECUTION_BASIS
names.

| Identity | Path | sha256 | Standing |
|---|---|---|---|
| Project Management, Consolidated v7 | `docs/alignment-manual/Project_Management_for_Human_Agent_Teams_Consolidated_v7.md` | `0aafefb12e9aa728592fb9e5b268ec4c9fba51d61401bb11bef8613e7f095032` | Chosen by the owner as core practice; edition recorded |
| Field Book v1 | `docs/alignment-manual/Project_Management_for_Human_Agent_Teams_Field_Book_v1.md` | `cf4bd6c237f614ab34234f02694f7ef10b6cc0c77c2cc482d4a9ccb992ea2a55` | Same |
| Agent User Manual v3 | `docs/alignment-manual/CHIRALITY_AGENT_USER_MANUAL_v3.md` | `df0297c5d77440df531e0cd38497eefb227ee465e376cbe56c7ba07f9bee0cde` | Same |
| `chirality-root:bundled:workflow:project-setup` | `workflows/project-setup/WORKFLOW.md` | `7aa4c30a09183b83341937960a637a89eb8da2f8800aa88a12ec8de7ab14dd6d` | Selected route, recorded |
| `preparation` (kind skill, bundled, chirality-root) | `.agents/skills/preparation/SKILL.md` | `0662dc88b5c1deff27280480395d355e5b073a3eb5eb9887f1459861ced96d38` | Recorded |
| `…:workflow:scope-of-work` | `workflows/scope-of-work/WORKFLOW.md` | `84dadde4c573b1d3d9ecd65e1e1be12efee1a95299b4115806c02e9c9cdebc2b` | Recorded |
| `…:workflow:dependency-extract` | `workflows/dependency-extract/WORKFLOW.md` | `e5523ebabccf44337ec531280d4d91be2ce7ff1477bd39568a18bb0c4c9f18c3` | Recorded |
| `…:workflow:audit-dep-closure` | `workflows/audit-dep-closure/WORKFLOW.md` | `b436fa343058795398633410bd9e0abd19a37dc5b2869c14617016df5e63fcb1` | Recorded |
| `…:workflow:project-dag` | `workflows/project-dag/WORKFLOW.md` | `e5db36606e71e5057f35d848c3a52f0e4aaca1198d3fe9e758f47cc1501a5a0b` | Recorded |

- **Historical, not adopted.** The source-checked research revision
  `e548d4cfada4d2105de6231516dc6e5fc4bd4689` (V4-OPS-11) and the original
  seed's candidate pins.
- **A read is not adoption.** A task that reads a manual records the read in
  its own ledger (CURRENT_EXECUTION_BASIS).

### 3.2 Methods selected by later undertakings

These methods are not in CURRENT_EXECUTION_BASIS. Their selection is
recorded in each undertaking's own records, and this table indexes those
records. The "Same bytes at `ffb2b628`?" column is **checked by O-E**; no
supplied record states it.

| Identity | Path | sha256 today | Same bytes at `ffb2b628`? | Where the selection is recorded |
|---|---|---|---|---|
| `chirality-root:bundled:workflow:construct-local-work-graph` | `workflows/construct-local-work-graph/WORKFLOW.md` | `fa04e1347f8594654e81e5c097414f8b6f602560fe15267a374145f43ae3a4c9` | Yes | LOOP_INIT §1; each work graph's "Method" line; pass 4: `RUN/BASIS_BINDING.md` |
| `…:workflow:scope-change` | `workflows/scope-change/WORKFLOW.md` | `b5fd144603c70e977a59988cb7dfe94dd710cac28db97a19f35c437399efbca9` | Yes | The SCA runs' graphs |
| `…:workflow:scc-resolution-case` | `workflows/scc-resolution-case/WORKFLOW.md` | `66b7aae75c9470710b40e93af206aec525d14d3269f1a139ef38874fc43e8590` | Yes | Case contracts under `E/_DAG/cases/` |
| `…:workflow:bounded-reconciliation` | `workflows/bounded-reconciliation/WORKFLOW.md` | `c7798c0ae59860f193d60f007996a215327c54e3e4dbd8eb0e62b57aab0f11bc` | Yes | The first-increment graph and the BRIEFS of the first increment and passes 2 and 3. LOOP_INIT §3 names it for closeout. **No pass-4 record selects it** |
| `bundled:chirality-root/coordinated-knowledge-work` | `workflows/coordinated-knowledge-work/WORKFLOW.md` | `44049bcd38b88378cd757ea34516f01edb0b0e93d8e9e3ac2b47ac61c9271b18` | **No: absent there** (added later on main by `1b0b1c5469`) | `RUN/OWNER_DECISIONS.md` "Coordination method", with this hash (B-14); `RUN/BASIS_BINDING.md` |

### 3.3 Binding an undertaking's basis (R23-35, superseding R23-31.3)

1. **States.** CURRENT_EXECUTION_BASIS: "a later undertaking or changed
   source must bind its own applicable basis before reliance". OI-017: "A
   later or changed basis needs its own deliberate pins before reliance".
2. **The rule (R23-35, DERIVED).**
   - Each later undertaking writes its own short basis binding before
     reliance.
   - It may bind by reference to the recorded pins after re-hashing them.
   - A changed edition gets a deliberate re-pin before reliance (V4-OPS-11:
     "adopt changed editions deliberately").
   - A newly selected method is bound by its source-qualified identity and
     sha256.
3. **Pass 4's binding.** `RUN/BASIS_BINDING.md` (sha256
   `93160e1de17aa7ca5fe99c8948b7f2c59ff9e98d7b19330d123238e504b38a37`),
   written by HELP_HUMAN as the project-definition manager, binds:
   - all nine recorded pins by reference, re-hashed and unchanged;
   - the two methods the run selected, `construct-local-work-graph` and
     `coordinated-knowledge-work`.

   It was written late. The run had not bound its basis when it started,
   and RR-EB1 found the gap. The bytes did not change during the run, so no
   tranche-1 result changes. The gap is recorded, not hidden (R23-35.3).
4. **Checked by O-E.** `prototype/eb1_check.py` P-4 confirms each hash in
   BASIS_BINDING.md equals today's bytes and this file's §3.1/§3.2.
5. **Earlier undertakings (R23-38.5).**
   - **No retroactive bindings are made;** no agreed condition requires them.
   - **No later undertaking cites the pins.** No later work graph, BRIEFS or
     DISPATCH cites CURRENT_EXECUTION_BASIS or the manual hashes (RV3's grep;
     only the project-definition graph does). They reached the manuals
     through LOOP_INIT's "Operating basis" pointer.
   - **Observation, checked by O-E with Git.** Every method the first
     increment and passes 2–3 used is byte-identical at `ffb2b628` and today
     (§3.1, §3.2). Their reliance was therefore on the recorded bytes, though
     no binding record of theirs states it.

## 4. Handoff for an arriving setup or local-SoW author, or a manager (OUT-002; REQ-003; AC-003)

| Need | Use | Source of the rule |
|---|---|---|
| Accepted scope and structure | `E/_Decomposition/checkpoint_snapshots/_LATEST_ACCEPTED.md` → Group3, **read as amended** by the snapshot `E/_ScopeChange/_LATEST.md` names (SCA-V4-003; closure `OPEN_PENDING_DERIVATIVE_CLOSURE`) | `_LATEST_ACCEPTED.md` "Reading rule" |
| Production order | `E/_DAG/_LATEST.md` → DAG-004 and its `HANDOFF_STATE.md`; currency from `E/_Evaluation/DAGCurrency/_LATEST.md` | SPEC §5.4, §11.2; LOOP_INIT "Project pointers" |
| Whether an input is met | The live local `Dependencies.csv` and `_DEPENDENCIES.md`. The DAG promotes no satisfaction | DAG-004 handoff "Reading rule" 2 |
| What a deliverable owes | Its `ScopeOfWork.md`, read with later decisions (R23-7) | V4-OPS-01 |
| Lifecycle | `_STATUS.md`. INITIALIZED means a checked contract exists, nothing more | `_COORDINATION.md` "Accepted rules"; SPEC §3.2 |
| Folders | `1_Working/` (active), `2_Checking/` (review staging), `3_Issued/` (released) | SPEC folder table; V4-OPS-01 |
| Manuals and methods | §3: CURRENT_EXECUTION_BASIS, **plus a basis binding of your own undertaking before reliance** (R23-35) | CURRENT_EXECUTION_BASIS; R23-35 |
| How to run an undertaking | `loop/LOOP_INIT.md`, then the undertaking's current work graph | LOOP_INIT |

**Do not redo:**
- Seed, decomposition or setup approval for unchanged definition
  (`_COORDINATION.md`: "No repeated preparation-stage permission question is
  required").
- Re-asking "whether the manuals are core governance or whether
  decomposition may proceed" (OPERATING_METHOD §7).
- Rebuilding the DAG for a new session (DAG-004 `HANDOFF_STATE.md`: "A new
  session is not, by itself, a reason to rebuild"; LOOP_INIT §1: "Graph
  revision is driven by changed relationships or scope, not session entry").
- Re-raising review independence for design units (B-18: "not raised
  again").
- Treating INITIALIZED or a valid contract as delivered input.

## 5. Developmental positions (OUT-002; REQ-004; AC-004)

- **SETTLED.** Field Book §1 defines Conceptual, FEED, 30%, 60%, 90% and
  100% by what each establishes. "Percentage labels describe development
  positions. They do not measure effort, code, or tasks completed. … Parts of
  a project may occupy different positions." V4-OPS-04 says the same.
- **States: the project's position.** The 30% gate is complete (B-7). Work
  toward 60% is under way. Field Book §1: 60% needs "Developed design and
  interfaces; an execution route for which further structural changes are no
  longer anticipated". The human assesses it (LOOP_INIT; Field Book §1: "The
  human decides whether to advance, qualify, redirect, or require further
  work"). No supplied record shows it assessed.
- **Steering toward 60% (states).**
  - The originating session was held off (B-7).
  - The first undertaking toward 60% records its scope choice in
    `E/_Coordination/AgentRuns/APP-V4-FIRST-INCREMENT-20260928/OWNER_DECISIONS.md`
    DECISION-1 (recorder HELP_HUMAN). The question was "Which scope should
    this first 60% undertaking take?"; the answer was "A: App/host spine
    (Recommended)".
  - Its question notes that "Wave 1 is already running". The steering that
    started that wave is not indexed here.
- **Uneven maturity, by example.** The production DAG, a 30% item, was
  constructed and examined before the gate, and accepted in the act that
  completed it (B-7). It has since been succeeded three times. Some
  deliverables have Design files and are IN_PROGRESS while others are
  INITIALIZED; read each from its `_STATUS.md`. Project position, a
  deliverable's lifecycle, an assignment's completion and acceptance are
  four different things.

## 6. Manual purpose, application and departures (OUT-003; REQ-005; AC-005)

| Practice or mechanism | Purpose kept | Actual treatment | Departure? | Record |
|---|---|---|---|---|
| Field Book as route, Consolidated by reasoning, User Manual for repository application | Proportionate, sourced practice | Applied; LOOP_INIT names the sections | No | V4-OPS-10; LOOP_INIT "Manual-led v4 practice" |
| D-12's "manuals guide work graphs" | Manual-led practice | Directions A/C make the manuals core working governance | Superseded, already decided | OPERATING_METHOD §1 (the direction text is in the acceptance's `DECISION_BRIEF.html`) |
| Root-first precedence hierarchy (original seed) | Clear authority | Human direction governs; Root location gives no precedence | Superseded, already decided | V4-OPS-12; A/C and HTML-D01 (accepted under J, B-1) |
| Thin-loop-file default | A light project entry | Not mandatory | Already decided | V4-OPS-14 |
| Seed carry/port wording for SOW-125–129 | Preserve required behaviour | Old client, registry and UI code are optional reuse candidates; the wording stays in the seed | Already decided | B-2 `DIRECTION.md` "Settled treatment applied" |
| Dated App-v3 entry pointers in the manuals (User Manual §14) | Correct project entry | App v4 enters by its own `init/` and LOOP_INIT | Already treated | LOOP_INIT: "Their examples and dated App-v3 entry pointers are not v4 product requirements or automatic adoption of another project's controls." LOOP_INIT's v4 text was written at the owner's request under the tranche manifest's `m2_gate` (B-19). No record shows the owner reviewed the resulting text |
| Per-manual-rule features, a copied corpus, a new precedence tree | — | Excluded | Already decided | PKG-10 package exclusions; V4-OPS-12/13 |
| MEMORY files | A local run index | Excluded at setup ("no … unsolicited MEMORY file"); LOOP_INIT §5 adds terse entries prospectively | No conflict ("does not retroactively add MEMORY work to the completed setup undertaking") | `_COORDINATION.md`; LOOP_INIT §5 |
| Legacy four-document kit; semantic-lensing pipeline; schedules and estimates | — | Not selected | Already decided at setup | `_COORDINATION.md` "Accepted rules" |
| Estimation, scheduling and risk practice where a method is silent | Treat consequential gaps | Open (PRD OQ-05) | Pending, OI-019: owner with execution manager, "When consequential gap affects selected work" | V4-OPS-22; `Open_Issues.csv` |
| Manual revision from feedback | Improve the method | Open | Pending, OI-020: owner, "Before revising manuals from feedback" | V4-OPS-23 |
| Independent review with the Codex preference (V4-OPS-34) | Independent checking | Design units: a same-model reviewer instance in the HELP_HUMAN session that did not author the work, identity reported. Product candidates: the Codex preference, unchanged | **Settled by the owner (B-18)**, "a practical concession to making the logistics easier"; not a claim of model-family independence | `RUN/OWNER_DECISIONS_2.md`; R23-31.5; EXP §7; R23-12 |
| Human decisions only where reserved | Keep the person on reserved acts | HELP_HUMAN rules matters the texts do not reserve | No; this is the owner's direction | B-15; R23-8…R23-14 |
| Receiving a changed shared instruction (V4-OPS-14) | Deliberate adoption | D-GOV-52: Root applied it (B-16). App v4 adopted it by R23-30. App v3 and Runtime: "notice delivered; receiving decision not recorded" (R23-32 F-R16) | No | Tranche manifest; App v4 notice; R23-30; R23-32 |
| Binding each undertaking's basis | Recoverable reliance | Pass 4 did not bind its basis at its start; bound late in `RUN/BASIS_BINDING.md` | A gap in practice, closed, not a departure (R23-35) | R23-35; BASIS_BINDING.md |
| Coordination method added mid-project | Usable results before multiplying work | `coordinated-knowledge-work`, directed by the owner, recorded with its hash | No | B-14; BASIS_BINDING.md |

**No departure now awaits the owner.**

## 7. Consumers and handovers (REQ-007; AC-007)

| Reader | Uses | Join |
|---|---|---|
| DEL-10-02 (undertaking controls) | §3 (manual sections and editions for practice notes; the binding step); §4 | DEP-10-02-011, admitted |
| DEL-10-03 (responsibility account) | §3, before relying on editions | DEP-10-03-017, admitted |
| DEL-10-04 (production DAG) | §2 and §4 at graph production | DEP-10-04-005, admitted |
| DEL-11-01 (continuity) | §3, keeping a run's selection distinct from adoption or instruction supply | DEP-11-01-009, admitted |
| DEL-11-02 (adoption) | §6's instruction-receiving row, B-16 and F-R16, when a consumer transitions (DEP-006) | DEP-10-01-020, admitted |
| An arriving author or manager | §4, §5 | DEP-10-01-021, not topological |

## 8. Verification design (VER-001…VER-008)

| VER | How | Status |
|---|---|---|
| VER-001 | Follow each B-row to its record; check actor, subject and limits | RR-EB1 (EB-v0.1): `eb1/EB1_COMPARISON.md` |
| VER-002 | `prototype/eb1_check.py` P-1…P-4. After a read, run it in `--post-dispatch` mode. In default mode, M-2 fails on every input-set item changed since the read, which is intended, not a regression | PASS at freeze (mode named in `RUN/OWNERS/O-E.md`) |
| VER-003 | Walk §4 as an arriving reader | RR-EB1 Q6: all MATCH |
| VER-004 | §5 compared with Field Book §1, Consolidated §1.7, User Manual §5 | Field Book §1 checked by O-E. RV3 spot-checked M §1.7 and U §5 (no conflict apart from the DAG timing, now repaired). O-E's own record of M §1.7 and U §5 is open |
| VER-005 | §6 compared with the three manuals and V4-OPS-10…13 | Rows sourced; per-row manual-section comparison open |
| VER-006 | Positive cases B-5, B-11, B-16 (actor ≠ recorder, custody kept); negative cases in §2.1 | RR-EB1 Q4 and Q7 (see the comparison on K7.d) |
| VER-007 | §7 against the nine scope rows and DEP-006 | Open |
| VER-008 | `tools/scope_of_work/check_boundary_owner_resolution.py` plus semantic follow-up | Open |

## 9. Open matters

| Matter | Owner | Point of need |
|---|---|---|
| VER-004, 005, 007 and 008 not run | O-E | Before this file is offered for the 60% review |
| OI-018 (remainder), OI-019, OI-020, OI-024, DEP-006 | As `Open_Issues.csv` and `External_Dependencies.csv` state | Their own points of need |

## Changes

**EB-v0.4 (2026-10-04), RV3-EB1 addendum 2 notes (EB-v0.3 READY):**

| Change | Cause |
|---|---|
| B-19's recorder cell: "The manifest does not name its own writer", as B-16 says of the D-GOV-52 manifest | N-b |
| §8 VER-002: default-mode M-2 "fails on every input-set item changed since the read" | N-a |

**EB-v0.3 (2026-10-04), after RV3-EB1 and its addendum (EB-v0.2 READY;
residuals planned in `RUN/OWNERS/O-E.md`), R23-38 and R23-42:**

| Change | Cause |
|---|---|
| B-19 added: LOOP_INIT's decision record (tranche manifest `m2_gate`), with exactly what it states and does not state. §6 row and §9 corrected | EB1-R6, EB2-R1, R23-42.1 |
| §3.3 item 5 follows R23-38.5 (no retroactive bindings; the byte-identical observation; RV3's grep fact). §9's binding row dropped | EB2-R2, R23-38.5 |
| Stated limits filled for B-3, B-4, B-8, B-9, B-10 | EB1-R7 |
| B-2 writer (WORKING_ITEMS); B-6 "does not name its writer" | EB1-R8 |
| B-7 carries the hold; DAG-002/003 placed correctly; §5 names the first-increment steering record and what is not indexed | EB1-R9 |
| §5 DAG timing: "constructed and examined before the gate; accepted in the act that completed it" | EB1-R12 |
| B-8 and B-9 quote "Accept (Recommended)" from the in-set records | EB1-R13 |
| §2.1 "R23-1 onward" | EB1-R14 |
| §8 VER-002 names the checker's mode; VER-004 cites RV3's spot check | Addendum note; N3 |
| Checker P-3 extended to the six method hashes | N4 |

**EB-v0.2 (2026-10-04), after RR-EB1 (`eb1/EB1_COMPARISON.md`) and R23-35:**

| Change | Cause |
|---|---|
| §1 and §3.1: the owner chose the manuals; WORKING_ITEMS recorded the editions; HELP_HUMAN confirmed the scope | D-2 |
| §3.3 rewritten to R23-35; pass 4's `BASIS_BINDING.md` indexed; §4 row "Manuals and methods" | D-3, R23-35 |
| B-18 added (owner's review-independence act); §2.1 and §6 rows corrected; "do not redo" gains B-18 | D-1 |
| B-12 completed (items 1–3); B-13 added (download approval); B-16 limit adds F-R16; §6 instruction row adds F-R16; §2.1 lifecycle row adds R23-34.9 | D-4 |
| §4: the DAG-rebuild source is now DAG-004 `HANDOFF_STATE.md` and LOOP_INIT §1, not DEL-10-04 REQ-007 | D-4 |
| Git-derived facts marked "Checked by O-E" (§3.1, §3.2, §6 LOOP_INIT row) | D-5 |
| §3.2 bounded-reconciliation row: no pass-4 record selects it | D-5 |
| §6 rows added: D-12, seed carry/port wording, basis binding | Reader's Q8 found them in the records |
| B-numbers after B-12 shift by one | Insertion of B-13 |
