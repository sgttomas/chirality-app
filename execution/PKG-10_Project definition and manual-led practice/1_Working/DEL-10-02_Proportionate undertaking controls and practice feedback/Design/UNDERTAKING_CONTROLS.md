# Undertaking controls and practice feedback — conventions over existing records

- **Contribution:** DEL-10-02/UC-v0.1 (new). It serves OUT-001 (§2, §3, §8),
  OUT-002 (§4) and OUT-003 (§5, §6, §7); verification design is in §10.
- **Status: DRAFT DEFINITION, frozen with EB-v0.3** for RV3 (one freeze,
  per the coordinator's direction after RV3's EB-v0.2 addendum). Owner O-E (Type 2 TASK, Claude
  Opus 5.5), run `APP-V4-DESIGN-PASS-4-20261003`, 2026-10-04.
- **What it is (R23-31.1):** conventions and an index over the project's
  existing undertaking records. It creates no new register and no parallel
  tracking system (V4-OPS-31). Root governance already settles most of the
  practice, and this file says so instead of restating it.
- **Basis:**
  - this deliverable's `ScopeOfWork.md`, sha256
    `d93ec4c043b783c01675e7fe27023969ae68a6cd7907ceb76f91b426ccc20fad`
    (INIT contract; no SCA-V4-001/002/003 block changed it);
  - `docs/OPERATING_METHOD.md` `98836b52…` (V4-OPS-02, 03, 20–23, 30–32, 34);
  - the manual editions bound for this run in `RUN/BASIS_BINDING.md`
    (`93160e1d…`): Field Book v1 `cf4bd6c2…`, Agent User Manual v3
    `df0297c5…`, Consolidated v7 `0aafefb1…`. Sections are cited as F §n,
    U §n and M §n.
- **Rulings (by ID):** R23-31 (items 1, 2, 4, 5, 6), R23-35, R23-38, R23-41
  (frozen bytes are kept; path-limited commit at freeze), R23-42.2; owner act
  B-18 of EB (`OWNER_DECISIONS_2.md`, review independence).
- **Labels:** SETTLED (a Root text or accepted record settles it); DERIVED;
  INTEGRATION; PROPOSED. **States** and **Inference** are kept apart.
- **Paths:** `E/` = `projects/chirality-app-v4/execution/`; `RUN/` =
  `E/_Coordination/AgentRuns/APP-V4-DESIGN-PASS-4-20261003/`.

## 1. Who writes what

| Record | Writer | Rule |
|---|---|---|
| Work graph, BRIEFS, DISPATCH, run notes (`PRACTICE_NOTES.md`, §5) | HELP_HUMAN as maintainer (WORKING_ITEMS function; R23-31.2) | One owner for shared writes (F §5.3; SPEC §9.8) |
| Owner records `RUN/OWNERS/O-x.md` (briefs received, freezes, returns) | Each owner, its own file only | §3 |
| Reviews `RUN/reviews/` | The reviewer | §4.2 |
| Owner acts | Transcribed by HELP_HUMAN into OWNER_DECISIONS files | Recorder ≠ actor (REQ-003) |
| This file | O-E | Proposals to the maintainer go through `O-E.md` |

## 2. Controls map: the SoW's reader/use table bound to actual records (OUT-001; REQ-001, REQ-003; AC-001, AC-003)

| SoW record | Reader and consumption point (SoW) | Actual record in this project | Settled by | Gap |
|---|---|---|---|---|
| Current undertaking graph and coordination choice | Manager, returning coordinator, successor: entry, selection, return, recovery | `E/_Coordination/WorkGraphs/<undertaking>/WORK_GRAPH.md`: nine graphs. Pass 4's carries the method, graph basis (DAG-004), coordination section, owners and nodes (outcome, write scope, needs, check, state) | SPEC §9.8; `construct-local-work-graph` §§3–4; LOOP_INIT §1 | None for structure. The graph's "basis" line names DAG-004 and methods; the manual binding is in BASIS_BINDING (R23-35) |
| Bounded brief and original return | Executor, receiving manager, examiner: before execution and at return | Survey-level briefs in `RUN/BRIEFS.md`; dispatch summaries in `RUN/DISPATCH.md`; owner freeze and return records in `RUN/OWNERS/`; reader dispatch records `RUN/RR-*/DISPATCH_RECORD.md` | F §5.3 brief fields; U §10; SPEC §9.8 | **G-1** (§3): standing owners' unit briefs arrive by message and are not preserved as files |
| Candidate-bound capability and check account | Manager, examiner, human: assignment, review, repair, reliance | DISPATCH's mechanism line; the RR dispatch records' "Enforcement limit"; each review's header (reviewer, model, separation, hashes reviewed) | V4-OPS-30, 34; U §3, §10; R23-31.6 | **G-2** (§4): no single per-run account; pieces are spread across files |
| Git history and reviewed PRs | Reviewer, integrator, successor: change review, integration, recovery | Git and the run's PRs (tranche 1: PR 1077; D-GOV-52: PR 1079) | V4-OPS-31; root merge policy | None |
| Node practice note and its disposition | Manager and owner; method author or consumer if a change is selected: at the stage discussion | **None yet.** Lessons exist as prose (RECEIPT "Coordinator lesson"; comparison §3) | V4-OPS-20, 21; R23-31.4 | **G-3** (§5–§7) |

**Recovery tests.**
- *Basis and position (inference).* EB-1's isolated reader recovered the
  project's basis and position from records alone (R23-38.1).
- *The graph's own route (VER-001, walked 2026-10-04 by O-E on pass 4's
  `WORK_GRAPH.md` `34b2e489…`, as committed at `d43665498d`).*
  - **Holds:**
    - every node carries outcome, write scope, needs, check and state;
    - owners are in "Coordination";
    - the graph basis is DAG-004, current with no deliverable DAG pending;
    - it is plain Markdown, so it needs no fleet UI or PEC.
  - **Does not hold:** the current position. The header still reads
    "tranche 1". T2-S is `ACTIVE` and T2-E `PLANNED`, although the surveys
    returned, R23-31…R23-42 were ruled, three early units froze and EB-1
    passed. Tranche 2's owners (O-D, O-E, O-F) and the next safe action
    appear only in DISPATCH.
  - **Result.** A successor reading the graph alone would not find
    tranche 2's state (`construct-local-work-graph` §4: "Keep one current
    account of the ready work, holds and next safe action"; F §5.4: "Update
    the graph at meaningful returns"). AC-001 is partly met. This is recorded
    as PN-8.

## 3. Brief and return conventions (OUT-001; REQ-002; AC-002)

### 3.1 What the brief and return must carry

- **Brief.** SETTLED by F §5.3, whose fields are Purpose, Basis, Context,
  Authority and tools, Write scope, and Return. U §10 adds parent,
  exclusions, required checks and return path. REQ-002 adds "parent and
  mechanism" and the recipient.
- **Return.** REQ-002: outputs, candidate, executed checks, limitations,
  unresolved matters and continuation. The receiving manager examines the
  return against the brief and the current receiving state before claiming
  integration (U §10).

### 3.2 Practice in this run, checked element by element (states, from the records)

| Element | Where pass 4 carries it | Holds? |
|---|---|---|
| Purpose, basis, context | BRIEFS "Common rules" and the S1/S2 sections; R23 rulings cited by ID | Yes, for survey assignments |
| Parent and mechanism | BRIEFS header ("Parent: HELP_HUMAN … Executors are Type 2 TASK"); DISPATCH ("harness-native descendants (Claude Code Agent tool) … under D-GOV-35") | Yes |
| Authority and tools; reserved decisions | Common rules (read-only Git, no network unless granted, ruled items); WORK_GRAPH "Coordination" escalation conditions | Yes |
| Write scope | Per brief (`SURVEY/<ID>.md`); per owner in DISPATCH rows ("Write area: …") | Yes in DISPATCH. Later unit-level grants appear only in messages (G-1) |
| Checks | Brief items and owner freeze records | Yes |
| Return and recipient | Brief "Return"; owner freeze entries: path and sha256, claims, checks run, open | Yes. The freeze entries in `OWNERS/O-*.md` meet REQ-002's return elements |
| **The unit brief a standing owner receives** | The coordinator's message, summarised in a DISPATCH row | **G-1: not preserved as a file.** DISPATCH keeps a one-line summary; the write grants, escalation conditions and exclusions in the message exist only in the session |

### 3.3 G-1 convention (DERIVED)

The receiving owner records each unit brief it receives in its own
`OWNERS/O-x.md`, before work starts. The record is a faithful summary of:
- purpose;
- write grant and exclusions;
- the rulings it relies on;
- escalation conditions;
- the expected return;
- the date and the sender.

The owner's file is its own write area, so this needs no new record and no
maintainer write. It preserves the "actual supplied basis" REQ-002 asks for.
Like a decision record, it is the receiver's transcription, not the
sender's bytes (U §10: retain the original return and record the parent's
assessment separately). O-E applies it from its next unit.

## 4. Capability and independent-check account (OUT-002; REQ-004, REQ-005; AC-004, AC-005)

### 4.1 Form (R23-31.6: a short section of each run's DISPATCH or BRIEFS; DERIVED)

| Field | Content | Standing to state |
|---|---|---|
| Mechanism | Parent, delegation mechanism (D-GOV-35 class), agent type, model as exposed | Host-reported or recorded |
| Host capability | What the host actually enforces: filesystem reach, network, tools, approvals | Host-reported, observed or **unknown** |
| Instruction-only limits | Fences, read-only Git, no network, no delegation, data-not-instructions | **Instruction-asserted**, never "enforced" because they were followed (V4-OPS-30; U §3) |
| How fences were checked | For example `git status` after each return, hash checks at freeze | Observed |
| Shared resources | Worktree and branch; shared stash; concurrent owners; uncommitted working files other owners may change | Host-reported or observed |
| Review separation | Per review: reviewer instance, whether it authored the subject, model identity as exposed, session. For design units, same-session same-model review is the owner's accepted practice (B-18), a logistics concession and not a claim of model-family independence. For product candidates: EXP §7 | Recorded |
| Unknown or untested | What was not established | Explicit |

### 4.2 Worked instance for pass 4 (proposed text for HELP_HUMAN's DISPATCH; R23-31.2)

| Field | Pass 4 | Source |
|---|---|---|
| Mechanism | HELP_HUMAN (Claude Code session) dispatches harness-native descendants via the Agent tool, D-GOV-35, agent type `type2-opus-high` (Claude Opus 5.5) | DISPATCH header; reviews' identity lines |
| Host capability | The host does not restrict reads ("Enforcement limit: the host does not restrict reads", RR-EB1 dispatch record). Write and network limits were not observed to be host-enforced for these agents | RR dispatch records; **unknown** beyond that |
| Instruction-only limits | Common rules; each unit's write grant | BRIEFS; messages (G-1) |
| How fences were checked | "Fences are verified afterwards by `git status`"; owners' hash checks at freeze | DISPATCH header; OWNERS files |
| Shared resources | One worktree on branch `claude/dgov52-agents-md-app-v4`. Its git stash is shared with the main checkout and other worktrees (host-reported to O-E's session). Several owners write concurrently. Run files (R23, OWNER_DECISIONS_2, WORK_GRAPH) are uncommitted working bytes that change under readers (EB-1: R23 drift after dispatch). The tranche-1 mid-repair checkpoint moved HEAD under owners' pins (PN-4) | Host context of O-E's session; `git status`; RECEIPT |
| Review separation | RV, RV2 and RV3 are fresh instances that did not author their subjects, Claude Opus 5.5 as exposed, within the HELP_HUMAN session (B-18). Readers RR-E, RR-F, RR-EB1, RR-EUF1 and RR-EUD1 are fresh instances given exactly the supplied files, with separation resting on the brief and the reader's own report | Review headers; RR dispatch records |
| Unknown or untested | Whether any agent read outside its set beyond its own report; host-level write isolation | — |

### 4.3 Independent-check account per unit

A review record already carries what REQ-005 needs:
- the subject hashes;
- the basis read;
- the reviewer, its separation and model identity;
- the findings with their severity;
- what was not checked.

RV3-EB1 is an example. The owner's freeze entry binds the candidate. The
owner's repair and the reviewer's confirmation close each finding
(`coordinated-knowledge-work` §3). **No new form is needed.** One gap shows
in practice, and it is PN-3: a review and a cold read ran in parallel on the
same frozen bytes, and the review did not see the reader's result.

## 5. Practice-note convention (OUT-003; REQ-006; AC-006; V4-OPS-20; R23-31.4)

- **Where.** One file per run, `AgentRuns/<RunID>/PRACTICE_NOTES.md`, written
  by the run's maintainer. The graph node it concerns links to it.
  Participants propose notes through their own records (for an owner, its
  `OWNERS/O-x.md`). This is DERIVED: a project-local convention that changes
  no Root template, since making it reusable would be a Root workflow
  revision through `create-workflow`.
- **When.** Only when practice actually proved useful, ill-fitting or
  ambiguous. No note per action and no invented examples (V4-OPS-20; AC-006).
  A matter the owner has already settled and said not to raise again is not
  re-noted (B-18).
- **Fields:**

| Field | Content |
|---|---|
| ID, node, date | Stable ID; the graph node; observation date |
| Observer | Who observed it (actor), and who recorded it if different |
| Conditions | What happened, from records |
| Practice exercised | Manual section and edition (bound pin), and the method if any |
| Class | `useful` · `ill-fitting` · `ambiguous` |
| Consequence | Effect on the work |
| Evidence | Record paths, rulings, hashes |
| Inference | Kept separate from the observation |
| Proposed treatment | PROPOSED only: `no change` · `project-local adjustment` · `proposed manual revision` · `scoped departure` |
| Disposition | `pending` (stage discussion, §7) · `settled by <record>` where an existing act already settled it · `applied locally by <record>` for an adjustment within the manager's authority |

## 6. Seed notes (drafted here; for HELP_HUMAN to enter into `RUN/PRACTICE_NOTES.md`)

**Shared attributes.**
- *Observers.* O-E observed PN-1, PN-2 and PN-3. The others are recorded by
  HELP_HUMAN in RECEIPT, R23 or OWNER_DECISIONS, as their evidence column
  shows.
- *Disposition.* `pending` unless stated otherwise.
- *Manual loci.* They cite the bound editions. Where a Root method governs
  the practice, it is named too.

| ID | Node | Conditions (states) | Practice exercised | Class | Consequence | Evidence | Proposed treatment |
|---|---|---|---|---|---|---|---|
| PN-1 | T2-E (EB-1) | O-E hashed the working bytes at freeze but wrote the account and key from earlier reads. The hashed `OWNER_DECISIONS_2.md` and R23 already held content O-E had not read | F §5.4 ("Preserve the actual inputs, candidate …"); M §5.4 (a stale summary treated as authority); U §10 (a changed file does not prove receipt) | ill-fitting: hash checks were in place, but the reading step was not | One wrong critical key item (K7.d) and five account defects; caught by the cold reader and RV3 | `eb1/EB1_COMPARISON.md` §3; R23-38.2 | Project-local adjustment: before freezing, re-read the changed sections of every hashed record the unit relies on ("hash the bytes you actually read", R23-38.2). O-E applies it from now on |
| PN-2 | T2-S / run start | Pass 4 did not bind its basis when it started. CURRENT_EXECUTION_BASIS requires "a later undertaking … must bind its own applicable basis before reliance". RR-EB1 found the gap; it was closed late | F §5.1 (read the accepted basis); U §10 ("preserve the supplied basis and actual method identity"); V4-OPS-11 | useful: the manuals already state it; the run's start step lacked it | None to results (bytes unchanged); a gap in records | R23-35; `RUN/BASIS_BINDING.md` | Project-local adjustment: the maintainer writes the binding at each undertaking's start. Making it a LOOP_INIT step would change a project instruction, which is a decision for the stage discussion |
| PN-3 | T2-E (EB-1) | RV3 reviewed EB-v0.1 for correctness while RR-EB1 read it cold. Both found the same defects; RV3's review was of bytes already superseded by EB-v0.2 when it returned | F §5.4 (independent review of the identified contribution); U §10 ("A queue of unexamined returns needs review … capacity"); `coordinated-knowledge-work` §3 | ambiguous: the methods do not order a cold read against a review | Duplicate findings; a second review round on v0.2 | `reviews/RV3-EB1.md`; `eb1/EB1_COMPARISON.md`; DISPATCH RV3 row | Project-local adjustment, for the manager: give the reviewer the reader's scored result, or start the review after scoring |
| PN-4 | D (tranche 1) | A working checkpoint taken mid-repair moved HEAD under owners' pins | F §5.3 (shared writes under one owner; control shared resources); U §10 (serialised use of shared resources) | useful: a lesson | Pins were invalidated, and a re-pin was needed | RECEIPT "Coordinator lesson"; DISPATCH O-B row | Disposition: `applied locally by RECEIPT` ("Later checkpoints were taken at quiet points") |
| PN-5 | E (tranche 1) | The early path (one decision package carried end to end) exposed three things that separate unit reviews had not found: the request body's real home, a faulty ruling (R23-18 item 3, superseded by R23-24), and an unspecified digest serialisation | F §5.4 ("Exercise connected behavior …"); `coordinated-knowledge-work` §1 | useful | Defects caught before dependent work expanded | RECEIPT "The early path"; R23-24 | No change; the method already prescribes it. Reused in tranche 2 (EB-1, EU-D1, EU-F1) |
| PN-6 | E (tranche 1) | A comparison checker agreed only with its own author's constructed accounts until an isolated reader's real account exposed RC-6 and RC-9 | M §1.5 (examining work received from an other); `coordinated-knowledge-work` §1 (shared basis) | useful | Checker repaired; standing check widened to independent accounts | RECEIPT; `RUN/E/RR-E/RESULT.md` | No change. O-E applied it to EB-1's checker (negative cases, `O-E.md`) |
| PN-7 | K (tranche 1) | HELP_HUMAN put ten questions to the owner (K-1…K-10) that the established ontology and earlier decisions already settled. The owner redirected | F §2 ("Carry routine work forward within existing authority. Bring decisions reserved to the human as concrete choices …") | ill-fitting: practice departed from the manual's guidance, then was corrected | Owner attention spent; the "week later" addition withdrawn (R23-6) | `OWNER_DECISIONS.md` "Scope of owner questions"; R23-8…R23-14 | Disposition: `settled by OWNER_DECISIONS.md "Scope of owner questions"` (B-15) |
| PN-8 | T2-S / T2-E | The pass-4 graph was committed at `d43665498d` with its tranche-1 state. Tranche 2's returns, rulings, owners and early units are carried in DISPATCH, not in the graph (VER-001 walk, §2) | F §5.4 ("Update the graph at meaningful returns"); `construct-local-work-graph` §4 | ill-fitting: the current-state record moved to DISPATCH | A successor's recovery from the graph alone misses tranche 2 | §2 VER-001 walk; DISPATCH rows S2…O-E | Project-local adjustment, for the maintainer: update the graph's T2 nodes at each ruling or freeze, keeping DISPATCH as the event log |

**Inference.** PN-1, PN-2, PN-3 and PN-8 call for project-local adjustments
within the manager's authority (F §2) and need no owner act now. PN-2's
loop-step form is the only one whose adoption would change an instruction.

**Manual-locus check (VER-006, done 2026-10-04 by O-E).** Each quotation in
the table was compared against the bound editions:
- F §2, §5.1, §5.3 and §5.4;
- U §3 and §10;
- M §1.5 and §5.4.

Each cited passage says what the note attributes to it. The editions'
hashes are unchanged (EB §3.1; BASIS_BINDING).

## 7. Stage disposition (OUT-003; REQ-007; AC-007; DEP-10-02-013)

- **Who decides (SETTLED; reserved to the person).** REQ-007 says the manager
  "shall bring the relevant practice notes to the owner and preserve their
  actual disposition". DEL-10-02's ResponsibleParty is "human at applicable
  stage decisions". The point of need is the stage discussion at the 60%
  assessment (LOOP_INIT).
- **Package form (PROPOSED).** One table: note ID, class, proposed
  treatment, affected scope, and the decision asked for. The disposition
  values are:
  - proposed manual revision, after which OI-020 applies: owner, "Before
    revising manuals from feedback";
  - scoped departure, stating which work it governs and which it does not;
  - no change;
  - pending.

  Notes already settled or applied locally are listed for information,
  with no decision asked.
- **Recording.** The owner's answer goes into the run's OWNER_DECISIONS file
  (recorder HELP_HUMAN), and each note's disposition field points to it. A
  proposed revision does not amend a manual. A scoped departure does not
  govern other consumers (REQ-007).
- **Carried open:**
  - OI-019 (owner with execution manager, "When consequential gap affects
    selected work"). None of PN-1…PN-7 is a consequential gap in a manual;
    each is covered by existing guidance or a method;
  - OI-020;
  - OI-018 (remainder).

## 8. DAG use and the SCC-CASE-006 pair (REQ-001; CLM-003)

- **Use.**
  - Graph-based selection uses the accepted current DAG. Pass 4's graph
    names "Graph basis: DAG-004".
  - Currency comes from `E/_Evaluation/DAGCurrency/_LATEST.md`
    (CURRENT_WITH_EVIDENCE_DRIFT; no deliverable DAG pending).
  - Satisfaction is read from live registers (DAG-004 handoff, reading
    rule 2). This is SETTLED: SPEC §5.4; `construct-local-work-graph` §2.
- **The cycle with DEL-10-04.** DEP-10-02-012 and DEP-10-04-006 are held in
  SCC-005 (SCC-CASE-006, R1). Under R1, the subset of control records graph
  production consumes is:
  - the current work graphs;
  - this file's §2 map;
  - the capability account (§4).

  DEL-10-04's mapping unit names its use of them. No cut or merge is needed
  (R23-31; S2-E E2-9).

## 9. Receiving practitioner observations (DEP-09-12-012)

DEL-09-12 hands over method observations and dispositions. They enter as
practice notes (§5) with `Observer` set to the practitioner and the
DEL-09-12 record as evidence. Their dispositions follow §7. Practitioner
validation remains DEL-09-12's (R23-32; OI-016 (App v4)). Nothing waits on it
here.

## 10. Verification design (VER-001…VER-008)

| VER | How | Worked case | Status |
|---|---|---|---|
| VER-001 | Walk a graph: outcome, input grounds, owner, permitted action, check, continuation; accepted-DAG currency; usable without fleet UI or PEC | Pass 4's `WORK_GRAPH.md` | **Done.** Structure holds; the current position is stale (§2, PN-8) |
| VER-002 | Compare an arrangement, a brief and its return with F §5.3 and U §§3, 10 | §3.2 (survey briefs); O-E's G-1 record of the R23-38 brief (`O-E.md` "Brief received") with its frozen return | **Done** for both cases |
| VER-003 | Reader/use table vs record set; positive faithful-recording case (B-18: recorder HELP_HUMAN, actor owner); negative case (a passing check presented as acceptance) | §2; EB §2.1 | **Done.** Positive: `OWNER_DECISIONS_2.md` keeps the owner's exact words, recorder HELP_HUMAN and custody, apart from HELP_HUMAN's earlier R23-31.5. Negative: tranche 1's RECEIPT reports review verdicts ("READY", "P1 … MERGE") and states "Nothing is implemented, built, signed or qualified", with no acceptance claimed from a check |
| VER-004 | Brief vs actual host permissions; challenge "worktree = sandbox" and "instruction = enforcement" | §4.2 | Drafted |
| VER-005 | Follow candidate bindings through review and backcheck | RV3-EB1 → EB-v0.2 → RV3 on v0.2 | Waiting for RV3 |
| VER-006 | Each note traced to node, conditions, evidence, manual section and edition | §6 | **Done** (§6 manual-locus check) |
| VER-007 | Dispositions vs decision evidence | PN-4 and PN-7 (settled); the rest pending | At the stage discussion |
| VER-008 | `tools/scope_of_work/check_boundary_owner_resolution.py` (sha256 `22ef57e0…`) plus semantic follow-up | All four PKG-10 SoWs: 1 boundary requirement checked each, 0 failing, 0 citing no claim. Semantic follow-up: §1's writer table and §7 leave DEL-10-01, DEL-10-04, DEL-06-01/02, host enforcement, the examiner and the person their acts | **Done** |

## 11. Proposals to HELP_HUMAN (through `O-E.md`; coordination records are yours)

- **P-E4.** Create `RUN/PRACTICE_NOTES.md` with PN-1…PN-8 (§6) and link it
  from the pass-4 graph.
- **P-E5.** Add §4.2's capability account to DISPATCH.
- **P-E6.** Take up the PN-3 adjustment for the next review that runs
  beside a cold read.

## 12. Open matters

| Matter | Owner | Point of need |
|---|---|---|
| G-1 applied by O-E (`O-E.md` "Brief received"); whether other owners adopt it | HELP_HUMAN | Next unit briefs |
| PN-8: updating the pass-4 graph's T2 nodes | HELP_HUMAN (graph maintainer) | Next graph update |
| VER-005 (review and backcheck binding), VER-007 (dispositions at the stage discussion) | O-E; owner at the stage discussion | RV3's return on this unit; 60% stage discussion |
| Stage disposition of PN-1…PN-3, PN-5, PN-6, PN-8 | Owner (§7) | 60% stage discussion |
