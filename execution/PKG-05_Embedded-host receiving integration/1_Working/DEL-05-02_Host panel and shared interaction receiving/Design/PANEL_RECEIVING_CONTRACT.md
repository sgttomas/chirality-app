# Host panel and shared interaction receiving contract
- Contribution: DEL-05-02/PANEL-v0.3
- Status: DRAFT DEFINITION — proposed, unsupplied, not implemented, not accepted
- Serves: OUT-001, OUT-002, OUT-003, OUT-004 (conditional state only); REQ-001–REQ-006; AC-001–AC-007; VER-001–VER-007 (all of DEL-05-02)
- Basis: repo 6e18505e3 (accepted basis); ScopeOfWork.md sha256 5c554956e91b2d8d5056176f85717cbd0e17a2d2d2991a52ea4ff185ebfd40cb; P/docs/PRD.md §2.2 V4-HOST-01/04/05/06, §3.1 V4-EXT-01, §4.1 V4-WF-03–06, §4.5 V4-AUT-01–05, §4.7 V4-REC-01/03/05, §5 V4-CST-05, §9 OQ-02/OQ-11; P/docs/ARCHITECTURE.md §3 (V4-ARC-05, reuse candidates), §4, §5 V4-ARC-20; P/docs/HOST_INTEGRATION.md §1, V4-HI-02/04, V4-HI-10–12, V4-HI-20–25, V4-HI-30–33, V4-HI-40–42, V4-HI-70/71, §10 item 7; P/docs/EXAMINATION.md V4-EXM-01–03, V4-EXM-20–22; DECISION_BRIEF.html (sha256 02d38cb1…4c420e8) d2, d3, d5; APP-V4-CLARIFICATION-20260927/DIRECTION.md; SCC-CASE-002 Case_Datasheet M1/M4 rows; Open_Issues OI-013/014/021; External_Dependencies DEP-001; run folder OWNER_DECISIONS.md (sha256 f3f8e5f3…cf81f2e; decision `APP-V4-FIRST-INCREMENT-20260928-DECISION-1`, D2 and D3), R1_RESOLUTIONS.md (2f9c7e72…e177ec4), R2_RESOLUTIONS.md (77cfb845…cdebd088), comparisons/V1-A.md (01811533…e04c09), comparisons/V1-C.md (8d46258a…4a94a6), reviews/IR1-A.md (31b3c7f8…0b648284), reviews/IR1-B.md (70e4a4f6…2846), reviews/IR1-C.md (295e96b3…a426b9)
- Consumed inputs:
  - **Prior version.** DEL-05-02/PANEL-v0.2, sha256 0a8a0dbe…19a700, at commit `c387730fb`.
  - **Sibling v0.2 text read from commit `28bd00499`** (`git show`) at the joins:
    - DEL-03-01/C-v0.2 (358182b1…6d82): §3.1, §4.1, §10;
    - DEL-03-02/P-v0.2 (942c1a3a…8c89): §3.1, §3.3, §4.3–§4.5, §5, §9;
    - DEL-02-01/WD-v0.2 (c25bccc5…a55c): §3.4, §4.2.4, §4.3, §6;
    - DEL-04-01/ACT-POLICY-v0.2 (e50f1fe2…93a9): §2.3–§2.5, §4, §5, §6;
    - DEL-04-02 (3a4e8b01…329c): §3, §4.
  - **R2 v0.3 changes to those siblings.** Taken from R2_RESOLUTIONS, marked "per R2-n; to be confirmed at V2/IR2". This file has not read the siblings' v0.3 text.
  - **DEL-05-01/LOOP-v0.3.** Co-drafted by this executor.
  - **DEP-001.** Host panel/view evidence has not been received.
- Receivers: DEL-02-01 (OUT-003; REQ-005; VER-005) and DEL-05-01 (OUT-004; REQ-005; VER-007) per CASE-002 M1; W9 relay file (§8 questions); external SWBPIPE owner via App-manager preparation and human file relay (DEP-05-02-018); DEL-05-02 itself for OUT-003 (VER-002, VER-003, VER-005) and OUT-002/OUT-004 (VER-004, VER-006)

## 0. How to read this definition

- **Behaviour contract, not layout.** The following are the host owner's:
  - layout;
  - visual design;
  - table and view construction;
  - assembly (SoW CLM-001; ARCH §4; `UNRESOLVED{OI-013}`).
- **Semantic names only.** No wire fields, component names or types are
  selected. The same applies to persistence and placement (OI-013, OI-014).
- **Standing labels.**
  - **SETTLED**: accepted basis or DECISION-1, credited only with what it
    says (R2-11).
  - **DERIVED**, **INTEGRATION** (R-n / R2-n) and **PROPOSED** are used as
    in LOOP-v0.3 §0.
  - `UNRESOLVED{…}` is never a permission, a default or a pass.
- **Act names and labels.** Canonical A1–A14 (ACT §2.1). Unqualified
  "checked" means only A4. "Approval" means only A6. Agent work is
  "examination findings". Host results read "host checks passed: ‹named
  checks›" (R-4).
- **Fixture.** Cases cite **FX-PIPE-01** (C-v0.2 §10) identifiers:
  - workspace FX-W1, generation g1, run R-100, nozzles N-1/N-2, supports
    S-1…S-4, load case LC-1, Engineer A;
  - workflow `supports-adjust` (origin host, ⟨fx-root⟩, ⟨rev-3⟩);
  - operations OP-C1…OP-C9;
  - timeline T1–T17 and Tg; bases B1/B2; proposals PR-1/PR-2; receipts
    RC-1…RC-3.

  Per R2-21 the cases also use OP-C10 Undo, OP-C11 (*no policy basis*,
  pending OI-021) and exposure "exposed on all three surfaces" (fixture
  assumption). The v0.2 labels R-101/R-102, S-7…S-9 and "support-adjust" are
  removed. Where a case needs a second workflow, it is a local label
  `L-PANEL-n`, and the case says why. Nothing selects the first connected
  operation (`UNRESOLVED{OI-021}`).

## Changes from v0.2

| Item | Change (section) |
|---|---|
| R2-1 | Class shown with five values including **no policy basis** (reason); *not permitted* displays name it (§3.3, PC-28) |
| R2-2; IR1A-08 | K-4 is restated as *performs*, including A10. The faithful-record operation conditions are a relay question (§3.4, §8) |
| R2-3 | External access enable/disable shown as the person's A13 (disable: INTEGRATION) (§5) |
| R2-4; IR1C-11 | Rejection kinds: loop-side **not offered** (before host validation); host-reported **not exposed on this surface** shown as a host outcome. Reserved entries: *not permitted* with A8 **offered** (§3.1, §3.3, K-4) |
| R2-5; IR1C-06; IR1A-03 | **Act-declined event** for A4, A6, A7 and A12 with capture evidence. It is separate from the **run-ended** event (W-5d, §5) |
| R2-6 | Grant state **effective (policy default)** added (§3.6) |
| R2-7 (PROPOSED) | A12 supersession shown. A refused A12 at a checkpoint is held for W7 (§3.5 W-5g, §5) |
| R2-9 | No-policy-basis wording. An A12 widening such a class is shown *refused (reason: no policy basis)*. Cases HELD (§3.6, PC-28) |
| R2-11; IR1C-17 | §1 attribution: no classifier mode is SETTLED (D3). No separate routine tool-permission layer is DERIVED |
| R2-12 | PC-24 is **AWAITING INPUT**. The not-permitted display names the governing checkpoint constraint (§3.3) |
| R2-13 | A resubmission shows the proposal's recorded state or outcome, never "stale" because of its own effects (§3.3, PC-10b) |
| R2-14 | Applied items show the resulting objects (created and changed identities) that bound checks refer to (§3.3) |
| R2-15 | Undo shown as "applied, then reversed by ⟨receipt⟩". Acts on changed content lapse normally (§3.3, PC-29) |
| R2-16; IR1-B X-8/B-m2/B-m13; IR1A-11 | **Stale after acceptance** display: "accepted by ‹person› — not applied: refused — stale (relied ‹B›, current ‹B′›)". The A5 is not lapsed. The open item is narrowed to host evidence (§3.3, PC-09b) |
| R2-17 | Checkpoint subject shown by its declared subject class (§3.5 W-5a) |
| R2-18; IR1C-02 | W-5f cites **WD §4.3.7**. "Partial" is a per-item annotation. Items that leave are shown. "All accepted" is never shown over a reduced subject |
| R2-19; IR1A-09 | Lapse before resume: "waiting — lapsed at ‹t›". *Lapsed* is a standing disposition only for ended runs (W-5e) |
| R2-20 (X-11, X-12, X-17); IR1C-08, IR1C-09 | Holding library shown beside origin and never part of identity equality. Run-end *waiting*, and the post-run act rule. The capture-evidence reference is a relay question (§3.2, W-5b, §8) |
| R2-21; IR1C-15; IR1-B B-M9/B-M10/B-m10 | All cases re-pointed to FX-PIPE-01. PC-22 uses OP-C9 (T15 scope) against OP-C4 geometry (§7) |
| IR1C-12 | **"Held at checkpoint (not dispatched)"** tool-activity state (§3.1) |
| IR1C-13 | "Runnable" rule restated in WD outcome terms: the requirement check *passes*, or a run-time hold (§3.2) |
| IR1C-14b | Checkpoint **purpose** and **scope** shown with every act request (W-5a) |
| IR1-B B-m8 | §3.3 origin adds seat role meaning and the two settings references |
| IR1-B B-m5 | Accounting states mapped to C's evidence labels (§7) |
| R3-1 (R3_RESOLUTIONS sha256 202d52c7…afbf; in place, no version bump) | W-5a lists subject classes, including **objects a named output concerns** (INTEGRATION) |
| R3-2 (in place) | W-5a: *targets of the held call* shown only with reached-when kind (a) (INTEGRATION) |

Changes from v0.1 are recorded in PANEL-v0.2 at commit `c387730fb`.

## 1. Scope

A host presents the agent through a panel for **conversation, workflow
selection, the proposal queue and checks**. The agent's work appears in the
host's own tables and views; there is no agent-private surface (V4-HOST-04,
SETTLED). The panel is where the person talks with the agent, selects its
method and decides. Results live in host objects shown in host views.

- Roles recede behind a single agent seat and the selected workflow
  (V4-HOST-05, SETTLED). Role selection is not a panel interaction.
- **Permission layer** (R2-11):
  - *No classifier permission mode in hosts; the SWB default proposal mode
    applies*: **SETTLED** (D3).
  - *No separate routine tool-permission prompts in the panel. Host
    operation authority is the person's grant plus adopted policy, resolved
    on the host route*: **DERIVED** from D3 with V4-HI-40/41.
  - Nothing the panel shows stands in for a reserved or professional act.

## 2. Definitions used by the receiving rules

| Term | Meaning |
|---|---|
| Host object | A domain object the host owns and stores (run R-100, supports S-1…S-4, load case LC-1). Domain truth stays in the host store (V4-REC-01; V4-CST-05) |
| Domain table | A host view of domain values. An examination never changes it (V4-EXM-21) |
| Host view | A table, view, diagnostic or result display the host gives the person (V4-HI-10) |
| Panel | The host-assembled surface for the four interactions. It lists, summarizes, links and offers host decisions. It holds no domain truth |
| Agent-private result surface | Any place where agent results or proposed changes are visible **only** outside host views, or differ from them. Prohibited (V4-HOST-04; SOW-020) |
| Alternate mutation route | Any path to host objects that bypasses the one validation/application route. Prohibited (V4-HI-20) |
| Findings location | Where A3 findings are held. Either (a) agent message content with references, or (b) host-held findings. `UNRESOLVED{C U-C5}` with the host owner |
| Reference | A pointer to a host object, view position, proposal, change item, receipt or record, followable into the host view. The panel shows references, not copies |

Panel content rules (PROPOSED):

- P-1. Everything shown about an agent result or a proposed change is
  reachable in a host view with the same content. For findings, the rows and
  results they reference must be reachable. Whether the finding text is
  there depends on the findings location.
- P-2. Summaries are allowed ("PR-2: 2 items on R-100"). The authoritative
  old and new values are shown in host views (V4-HI-24, SETTLED).
- P-3. The only mutation path is submission to the host route. Decision
  controls (accept, reject, mark checked, grant change) are host-offered and
  host-captured acts (§5).

## 3. The four interactions, plus checkpoints and grant

### 3.1 Conversation

| Aspect | Receiving requirement |
|---|---|
| Person does | Writes; reads; follows references; cancels a turn |
| Panel presents | <ul><li>**Message stream** with speaker (LOOP §2.1). Completion standing: streaming, complete, truncated, interrupted, cancelled or failed.</li><li>**Tool activity** (LOOP §2.3):<ul><li>requested;</li><li>**rejected before host validation**, with the kind: unparseable/truncated, **not offered**, schema, or offer out of date;</li><li>**held at checkpoint (not dispatched)**, naming the checkpoint (IR1C-12);</li><li>dispatched;</li><li>host outcome in P §9 terms, including a **host-reported *not exposed on this surface***;</li><li>*outcome unknown*, with reporter and last observed state.</li></ul></li><li>**A8 requests**, shown only when issued, with requester, purpose and scope.</li><li>**Model setting indicator** (LOOP §5.1): local; cloud chosen, key supplied; cloud chosen, key absent; unconfigured. No key content.</li><li>**"Model request refused at boundary"**.</li></ul> |
| Host objects/results | References only. Basis and standing as given (V4-HI-11/12), e.g. B1 at T3 |
| Consumed definitions | LOOP messages, events and settings; C basis and standing; P §9; DEL-04-03 conversation reference |
| Responsible | App/shared: this requirement. Host owner: assembly and persistence (`UNRESOLVED{OI-013}`) |
| Must not | Present prose as a host result. Show a rejected or held call as executed. Show success as acceptance. Show an A8 request as the act |
| Unresolved | OI-013; DEP-05-01-024 (via LOOP) |

### 3.2 Workflow selection

| Aspect | Receiving requirement |
|---|---|
| Person does | Chooses the workflow for a run; sees what it needs, where it stops, and why |
| Panel presents | <ul><li>**Identity**: {kind, origin, source root, name, revision} + derived-from (WD §6.1). An unadapted carried workflow keeps its origin. A host adaptation is a new host-origin identity with derived-from. There is no "App-origin".</li><li>**Holding library** beside the origin for any carried workflow, so that a *project*-origin workflow held in a host library is legible. It **never takes part in identity equality**. Collision reports list the holding library with each origin (R2-20; WD §6.4 U-24; PROPOSED until W7).</li><li>**Declared checkpoints**: name; required act (A4, A5, A6, A7 or A12); reached-when; subject class; scope; **purpose**; negative path.</li><li>**Required tools**, each with its WD §4.2.4 outcome: *present*; *missing*; *not exposed on this surface*; *version mismatch*; *present, currently unavailable* (with reason); *channel not enabled*; *not established* (with reason). Each is shown with its **necessity** (required, or optional with the stated effect).</li><li>**Workflow-level states** (WD §3.4, §4.7): *declared*; *declared empty*; *requirements undeclared*; *unsupported* (with reason).</li></ul> |
| Runnable rule (IR1C-13) | The panel shows the **requirement check passes** only when every reference whose necessity is *required* is *present* or *present, currently unavailable*. The latter is shown as a **run-time hold** with its reason, not as missing. Any other outcome for a required reference means the check does not pass, and the reason is shown. A workflow with *requirements undeclared* stays **selectable**, labeled "requirements undeclared — check not established". It is never labeled runnable-by-check or "no requirements". *Unsupported* is shown with its reason |
| Host objects/results | The run is associated with the selected identity tuple (V4-HI-70) |
| Consumed definitions | WD declaration, identity, §4.2.4 and §3.4 vocabulary; C exposure element 9; ACT act names; DEL-04-03 run record |
| Responsible | App/shared: this requirement. Host owner: assembly, host workflows, evaluation of outcomes |
| Must not | Silently rebind a selection. Collapse *not established*, *not exposed* or *currently unavailable* into present/absent. Show a failed check as a pass |
| Unresolved | Which party evaluates outcomes in the host; a DEL-02-03 checker is relevant only if OI-014 allocates one |

### 3.3 Proposal queue

| Aspect | Receiving requirement |
|---|---|
| Person does | Reviews proposed changes in host tables. Accepts item by item, several items, or a batch (V4-HI-41). Rejects. Opens objects |
| Panel presents | <ul><li>Per proposal: reference; **per change item**: objects, old/new values (in host views), reason, current disposition; stale indication; lineage for a re-draft (PR-2 ← PR-1, T9).</li><li>Proposal state **derived from items, never stronger** (P §4.3).</li><li>**Origin** (P §3.3): author type; seat; **seat role meaning** (or unknown); channel; conversation; workflow identity tuple; run; standing at drafting (grant display state); **settings reference at route decision**; **settings reference at application** (host-reported, or *unconfirmed*); reason (IR1-B B-m8).</li><li>Relied-on basis.</li><li>Outcomes per P §9 and C §4.1 unchanged: queued; accepted (A5, actor); rejected (A10, actor); withdrawn (A11); applied with receipt and branch (direct under grant / after acceptance) with **resulting objects** (created and changed identities, R2-14); application error (effect none/partial/unknown); refused — invalid; refused — stale (both bases); unavailable; not permitted (naming governing treatment, policy record, or **governing checkpoint constraint**, and the class value including **no policy basis (reason)**); channel not enabled; not exposed on this surface (host-reported); error; outcome unknown (reporter, last observed state).</li><li>Every non-success shows the evaluated basis. Decision wording is **accept**, never approve (V4-HI-33, SETTLED).</li></ul> |
| Stale after acceptance (R2-16) | An accepted item refused stale at application is shown as **"accepted by ‹person› — not applied: refused — stale (relied ‹B›, current ‹B′›)"**. The A5 is **not lapsed** and stays bound to its item content. The item's state is never "accepted" alone, nor "applied". A re-draft shows no carried acceptance. The checkpoint effect follows W-5f |
| Resubmission (R2-13) | A resubmission of the same proposal identity shows that proposal's recorded state or outcome, e.g. PR-2 item 1 applied with RC-1 at T13. It is never shown as stale because of its own effects |
| Undo (R2-15) | An applied change later undone shows **"applied, then reversed by ⟨receipt⟩"** (T16 RC-2, reversed by RC-3 at T17). Acts bound to content the undo changed are shown lapsed, as for any change |
| Host objects/results | Proposed items appear in host tables as proposed (V4-EXM-20). Applied changes carry receipts and origin marks (V4-HI-22/71) |
| Acceptance unit | The change item (P §3.1 rules 1–3). A batch is one A5 listing items, each item-bound, with per-item lapse. Applying an accepted item does not lapse the A5 |
| Direct autonomy and checkpoints | Direct application shows only in an *effective* grant state whose value is direct (R-8; R2-6), with origin, undo route and later-examination route (P §4.4). Under a declared A5 checkpoint, a direct request shows **not permitted**, naming the **governing checkpoint constraint** (R2-12). It never appears as a silently created proposal |
| Consumed definitions | P lifecycle, §9, identities, lineage, stale, no retargeting, one effect (host obligation), undo; C basis; ACT names, wording and treatment map; DEL-04-03 act record and lapse |
| Responsible | App/shared: this requirement. Host owner: tables/views, route, treatment, receipts, capture of A5/A10 (HI §1) |
| Must not | Show queued as applied, or accepted as applied before the receipt. Call a host refusal "rejected". Re-draft or retarget from the panel: a re-draft is the agent's new proposal with lineage. Show a proposal state stronger than its items. Use "approve" |
| Unresolved | Host evidence that application re-checks the basis (DEP-001; P U-P3, narrowed per R2-16). Proposal identity and duplicate mechanics (TBD-002) |

### 3.4 Checks

| Subject | Actor | Panel label and presentation | Host objects/results | Consumed |
|---|---|---|---|---|
| A3 examine (e.g. OP-C3 at T4, span S-2→S-3 exceeds the limit) | Agent | "Examination findings", referencing rows/results and the read basis (B1). Standing: agent findings | Domain tables unchanged. Location per §2 | C basis/standing; U-C5; LOOP E-5; DEL-04-03 |
| Host check results (e.g. T1 "equilibrium", "unit consistency" at r12) | Host | "Host checks passed: ‹named checks›", each with its evaluated basis. Currency is shown (LC-1 historical at r13, T6) | Host results | C standing |
| A4 mark checked (e.g. T2 on S-2) | Person (D2a, SETTLED); host act facility captures it | "Checked by Engineer A", with bound subject content (⟨S-2@r12⟩) and state | Content-bound act record | ACT A4; DEL-04-03 |

Rules:

- K-1. Findings are never shown as A4 or A6. "Checked" is used only for A4
  (R-4).
- K-2. An examination changes no domain table. PC-12 compares before and
  after.
- K-3. An A4 lapses visibly when its bound content changes, at any time
  after performance. T14 (S-2 edited at r15) lapses T2's A4. T6 (S-3 edited)
  does not.
- K-4. An operation that **performs** A4, A5, A6, A7, A10, A12 or A13 has
  class **reserved to the person** (R2-2, DERIVED; D2 SETTLED for the acts).
  Examples are OP-C6, OP-C7 and OP-C8.
  - Reserved entries are always offered (R2-4). An agent call shows *not
    permitted*, and an A8 request is **offered**. An A8 is shown only if the
    agent issues one.
  - No faithful record is made through a reserved operation. A host
    faithful-record operation, if any, meets the four R2-2 conditions (§8
    Q-5).
  - Host adoption of the list is DEP-001. Hosts have no classifier mode
    (D3).

### 3.5 Declared checkpoints in the panel

This section consumes LOOP-v0.3 §2.4, WD §4.3 and ACT §4.

- W-5a. **Reached.**
  - Shown only when the loop reports that the reached-when condition was
    observed.
  - The display shows: the required act kind; the observed event; the bound
    subject by its **declared subject class** (R2-17) and content
    identities; the declared **purpose** and **scope** (IR1C-14b); the
    actor requirement.
  - The subject classes shown are:
    - change items of a named proposal;
    - named output;
    - objects changed by a named outcome;
    - **objects a named output concerns** (R3-1), e.g. the rows OP-C3
      examined at T4, shown with their subject content identities as read;
    - targets of the held call, shown only with reached-when kind (a)
      (R3-2);
    - grant setting.
  - Never inferred from stage or model text.
- W-5b. **Dispositions.**
  - The vocabulary is *waiting* · *performed* · *resolved negatively* ·
    *lapsed* · *not reached* · *unknown*.
  - At run end:
    - *not reached* if the condition was never observed;
    - *unknown* if the observation was lost;
    - **waiting** if the checkpoint was reached but not performed, shown with
      the **run-ended** event and never as performed (R2-5; R2-20).
  - An act the person performs after the run ended is shown as a recorded
    act against the bound subject. It does not change the ended run's
    disposition unless DEL-02-03 defines resumption.
- W-5c. **Clearing.**
  - *Performed* only on capturing-surface evidence of the specified kind, on
    the bound subject content.
  - A faithful record (A9) citing that evidence may be shown as a record
    (W-2). It never clears a checkpoint by itself.
  - Without a host capture-evidence reference (§8 Q-2), no host-content
    checkpoint can show *performed*.
- W-5d. **Negative decisions** (R2-5).
  - For A5 the negative is A10.
  - For A4, A6, A7 and A12 it is an **act-declined event**, captured by the
    host act facility. It is not an act of the declined kind.
  - The disposition is *resolved negatively*. The panel shows the declared
    negative path, or "run stopped".
  - Stopping the work is a separate **run-ended** event. A checkpoint
    waiting at that moment stays *waiting*.
- W-5e. **Lapse** (R2-19).
  - An **act-lapsed event** is always shown.
  - Before resume, the disposition reads **"waiting — lapsed at ‹t›"**, and a
    new act on current content is needed.
  - After resume, the lapse is shown. Re-hold belongs to DEL-02-03.
  - *Lapsed* appears as a standing disposition only for a checkpoint whose
    run has ended.
- W-5f. **Mixed item decisions at an A5 checkpoint** follow **WD §4.3.7**
  (PROPOSED there; DEL-02-03 confirms at W7; R2-18):
  - all bound items have A5 → *performed*;
  - any item undecided → *waiting*;
  - all decided, at least one A10 → *resolved negatively*, with a per-item
    **partial** annotation.
  - Items that left without a decision (stale, A11, host refusal) are shown
    with their event.
  - A *performed* over a reduced subject is **never** shown as "all
    accepted".
  - Example: FX-PIPE-01 T11 (item 1 A5, item 2 A10) gives *resolved
    negatively (partial: item 1 accepted)*.
- W-5g. **A12 checkpoints** (R2-7, PROPOSED).
  - The subject is the setting content (classes, grant value, scope).
  - A later A12 shows the earlier one **superseded**, not lapsed. A
    checkpoint it performed stays *performed*, with the supersession shown.
  - A refused A12 at a checkpoint is held for W7.

### 3.6 Active autonomy grant (DEL-04-02; R-8; R2-6)

The grant is shown per class and scope, from DEL-04-02 §3 with R2-6 applied:

| State | Shown as | Direct branch? |
|---|---|---|
| effective (person-set) | Grant value and scope; A12 reference | Yes, if the value is direct |
| **effective (policy default)** | "Default: ‹value› (policy ‹record›)". No A12, no setting actor | Only if the policy default is *direct*. None is in the first increment (SWB default *propose*) |
| requested by agent | "Agent requests ‹value, scope›", beside the effective value | No |
| set by person, not yet confirmed by control | "Set by you — not yet in force" | No; the prior effective value governs |
| unconfirmed | Last-known value labeled "unconfirmed" | No |
| not set | "not set" (no setting and no default) | No |
| refused (reason) | Reason beside the still-effective value. Includes **"refused — no policy basis"** for an A12 widening a *no policy basis* class (R2-9) | No |

- Grant changes are A12, reserved (D2e). An agent's change is shown only as
  a request (A8).
- The grant display and the checkpoint indicator never merge into a single
  "allowed" signal (DEL-04-02 §4).
- This consumption is not in this SoW's CLM-002 or register (finding F-3 →
  C1).

## 4. Host tables and views: no agent-private surface

| Rule | Source | Rejection case |
|---|---|---|
| H-1 Agent results and proposed changes appear in host tables/views | V4-HOST-04; SOW-020 (SETTLED) | PC-13 |
| H-2 Per change item, host views show old/new values, objects, reason, origin, item state, stale indication | V4-HI-24; P §8 | PC-06 negative variant |
| H-3 Findings reference host rows/results and standing; domain tables unchanged; location per §2 | V4-EXM-21; C U-C5 | PC-12 |
| H-4 No alternate mutation route | V4-HI-20 (SETTLED) | PC-14 |
| H-5 No invented domain truth; references kept | V4-HI-71; V4-CST-05 | PC-15 |
| H-6 Agent reads show the same views and standing marks | V4-HI-10; V4-PAR-03 | PC-02 |

## 5. Acts, wording and lapse

| Act / event | Actor | Capture / recorder | Panel wording | Never inferred from |
|---|---|---|---|---|
| A2 apply (direct under grant) | Agent within an effective direct grant; host applies | Host (origin mark, undo) | "applied by agent under grant" (T16) | — |
| Undo (OP-C10) | Actor per its treatment | Host | "applied, then reversed by ⟨receipt⟩" (T17) | — |
| A1 propose → queued | Agent | Host | "queued" (T10) | Success |
| A5 accept (per item) | Person (D2b) | Host act facility; A9 as record shape | "accepted by Engineer A" (T11 item 1) | Success, queueing, receipt |
| A10 reject | Person | Host act facility | "rejected by Engineer A" (T11 item 2) | A host refusal |
| A11 withdraw | Proposer | Host | "withdrawn by ‹proposer›" | — |
| A2 apply (after acceptance) | Host | Host | "applied" + receipt (T12 RC-1) | Acceptance alone |
| A3 examine | Agent | Host / record | "examination findings" (T4) | — |
| A4 mark checked | Person (D2a) | Host act facility; A9 as record shape | "checked by Engineer A" + bound content (T2) | Findings, success, acceptance |
| A6 approve | Person (D2c) | Host act facility; A9 as record shape | "approved by ‹person›" | Agent output (V4-AUT-05) |
| A7 rely | Accountable professional (D2d) | Host act facility; A9 as record shape | Recorded act only | Other acts |
| Act-declined event | Person (A4/A6/A7/A12 not performed) | Host act facility | "declined ‹act› — ‹subject›" | — |
| Run-ended event | Loop or person stop | Loop | "run ended (‹cause›)" | — |
| A8 request | Agent | Loop/record | "‹act› requested by agent", only when issued | Performance; automatic creation |
| A12 set grant | Person (D2e) | Host | "grant set by Engineer A" (T15); "superseded by ‹act›" | An agent request |
| A13 external access | Person. Enable: D2e (SETTLED). Disable: INTEGRATION (R2-3) | Host/App | "external access enabled/disabled by ‹person›" | An agent request |

Rules:

- W-1. Proposal decisions say **accept**, never approve (V4-HI-33). The word
  "approval" is used only for A6.
- W-2. **Record presentation.**
  - For any recorded act, the panel shows the **actor** (the person), the
    **recorder**, the **recording mode** (direct capture or faithful
    recording) and the **capture-evidence reference** (V4-HI-31; ACT §2.4).
  - A record without capture evidence is shown as "record without capture
    evidence". It has no act standing and clears nothing (W-5c).
  - Unperformed acts are never presented.
  - A host capture requirement per act kind is DEP-001.
- W-3. **Content binding and lapse.**
  - Binding: A5/A10 to the change-item content identity; A4/A6/A7 to the
    subject content identity; A12 to the setting content (PROPOSED).
  - Lapse is shown at any time after performance. A12 is superseded, not
    lapsed.
  - Stale after acceptance is not a lapse (R2-16).
- W-4. No act proves another. There is no acceptance-first rule
  (SoW REQ-003).
- W-5. Checkpoints are presented per §3.5.
- W-6. D2 reserved acts are SETTLED for App/shared contracts, and hosts have
  no classifier mode (D3). Still open: OI-021 additions and host adoption
  (DEP-001).

## 6. Reusable-component allocation account (OUT-002) and conditional OUT-004

| Candidate responsibility | Possible consumers | Repeated? | Agreement | Standing |
|---|---|---|---|---|
| Act, lapse and supersession presentation (actor, recorder, recording mode, capture evidence) | SWBPIPE host panel; App standing/act display (DEL-04-02 OUT-001) | Plausible | None | Proposed candidate |
| Grant display state and scope presentation, including policy default | SWBPIPE host panel; App autonomy display (DEL-04-02) | Plausible | None | Proposed candidate |
| Workflow identity, holding library and required-tool outcome presentation | SWBPIPE host panel; App workflow experience (DEL-02-02, later undertaking per D1) | Plausible | None | Proposed candidate (WD §9 map) |
| Proposal item-disposition presentation | SWBPIPE panel; later hosts (OI-005). The App has no host queue | Not established | None | Not proposed |
| Tool-activity presentation | SWBPIPE panel. The App presents Codex items natively (V4-ARC-05) | Not established | None | Not proposed |
| Conversation rendering | SWBPIPE panel. The App is Codex-native | Not established | None | Not proposed |

**OUT-004 conditional state.** No reusable panel component is selected,
agreed or implemented (SoW AC-006). v3 interface pieces (ARCH §3) are optional
reuse sources.

**Host construction boundary.** The following stay with the external host
owner (SoW CLM-001; HI §1):

- host panel assembly and layout;
- tables and views;
- domain construction;
- conversation persistence;
- treatment resolution;
- act capture.

| Open issue | Owner | Point of need | What it holds here |
|---|---|---|---|
| OI-013 | Shared contract owner with SWB implementation owner | Before shared/host implementation boundary contracts | Panel assembly; host/common construction boundary |
| OI-014 | App/shared contract owners | Before structural/production allocation | Whether any candidate becomes shared, and where |

## 7. Receiving case inventory (OUT-003)

All cases are **DESIGNED — UNEXECUTED**: no host candidate exists (DEP-001),
and the sibling v0.3 elements are to be confirmed. A missing input is not a
pass (SoW VER-005).

Accounting states (IR1-B B-m5; mapping owned by C):

| State | Meaning |
|---|---|
| DEFINED | Corresponds to C *illustrative* |
| EXECUTED (test double) | Corresponds to C *test-double* |
| EXECUTED (candidate) | Corresponds to C *actual host*, with configuration and date (V4-EXM-01) |
| LIMITED | Executed with stated gaps |
| AWAITING INPUT | Waiting for a named input |
| HELD | Waiting for a named decision; never a pass |

| Case | Interaction | Stimulus (FX-PIPE-01) | Expected result | Inputs needed | Serves |
|---|---|---|---|---|---|
| PC-01 | Conversation | T3 agent reads OP-C1 for R-100 | Reply references host rows S-1…S-4; basis B1 and standing as given | C, LOOP, host views | VER-001/002 |
| PC-02 | Conversation | Agent reads OP-C2 LC-1 results at r13 after T6 | Shown historical, never current (V4-HI-12) | C, host | VER-002 |
| PC-03 | Conversation | Loop rejects a truncated call (LOOP MC-1) | "Rejected before host validation: truncated" | LOOP, DEP-05-01-024 | VER-001 |
| PC-03b | Conversation | Setting "cloud chosen, key absent" | Indicator; "model request refused at boundary"; no key content | LOOP §5, host | VER-001 |
| PC-03c | Conversation | Kind (a) checkpoint holds an OP-C5 call (LOOP FX-C8) | "Held at checkpoint (not dispatched)", naming the checkpoint | LOOP | VER-001 |
| PC-03d | Conversation | Call to a name absent from the offered edition; separately, host returns *not exposed* for an OP-C2 variant | First: "rejected before host validation: not offered". Second: host outcome "not exposed on this surface" | LOOP, C, host | VER-001 |
| PC-04 | Workflow selection | `supports-adjust` (origin host, ⟨rev-3⟩), plus a local **`L-PANEL-1`**: a same-named workflow with origin *project*, carried unadapted into the host library. A second workflow is needed for the collision, and FX-PIPE-01 has one | Both shown with the full tuple. `L-PANEL-1` shows **holding library** = host library, beside origin *project*. The collision lists both. The selection binds to the chosen tuple; the holding library does not affect equality | WD, host library | VER-001 |
| PC-05 | Workflow selection | `supports-adjust` requires OP-C1 (*present*), OP-C4 (*present*) and OP-C2 (*present, currently unavailable* at T8); `L-PANEL-1` has *requirements undeclared* | The first workflow's requirement check **passes**, with a run-time hold on OP-C2 ("No current solve for LC-1 at this revision"). `L-PANEL-1` is selectable, "requirements undeclared — check not established" | WD, C, host | VER-001 |
| PC-05b | Workflow selection | Named exposure variant: OP-C4 not exposed on the embedded surface | Required reference *not exposed on this surface*; check does not pass; reason shown | WD, C | VER-001 |
| PC-06 | Proposal queue | T10 PR-2 queued: item 1 new support on R-100 (OP-C4); item 2 S-3 stiffness (OP-C5) | Items with old/new, objects, reason, origin (incl. seat role meaning, settings references) and item state in host tables. State derived. Negative variant: values only in the panel → fail | P, C, host | VER-002 |
| PC-07 | Proposal queue | T11: Engineer A accepts item 1, rejects item 2; T12 applies item 1 | "Accept" wording. Item 1 A5 then applied (RC-1) with **resulting objects** (new support identity). Item 2 rejected (A10, actor). State never stronger than items | P, host, actual acts | VER-002/003 |
| PC-07b | Proposal queue | Variant: Engineer A accepts both PR-2 items as one batch | One A5 listing two items, each item-bound; per-item lapse possible | P, DEL-04-03 | VER-003 |
| PC-08 | Proposal queue | T10 submission reports success | "Queued", not applied or accepted | P | VER-003 |
| PC-09 | Proposal queue | T7: PR-1 relies on B1 (r12); T6 edited S-3 (r13) | "Refused — stale" with B1 and B2. T9 PR-2 shown as the agent's **new** proposal with lineage to PR-1. No panel re-draft or retarget | P, C, host | VER-002 |
| PC-09b | Proposal queue | Variant: item 1 of PR-2 accepted, then S-3 edited before application | "Accepted by Engineer A — not applied: refused — stale (relied B2, current ‹B′›)". A5 not lapsed; state not "accepted" or "applied" (R2-16) | P, host | VER-002/003 |
| PC-10 | Proposal queue | T13: acknowledgment of T12 lost and unobservable | "Outcome unknown", reporter and last observed state | P, LOOP | VER-002 |
| PC-10b | Proposal queue | T13: resubmission of PR-2 with the same identity | Recorded outcome shown (item 1 applied, RC-1). Never "stale" because of its own effect (R2-13) | P, host | VER-002 |
| PC-11 | Proposal queue | Any proposal decision control | "Accept"; any "approve" fails | P, ACT | VER-003 |
| PC-12 | Checks | T4: agent examines spacing with OP-C3 | Findings reference rows and B1. Domain tables identical before and after. Labeled "examination findings", never "checked" | C, LOOP, host, U-C5 | VER-002/003 |
| PC-12b | Checks | T1 host checks at r12 | "Host checks passed: equilibrium, unit consistency", evaluated at r12; historical after T6 | C | VER-003 |
| PC-13 | Rejection | Agent result visible only in the panel | Fails H-1 | Host | VER-002 |
| PC-14 | Rejection | Panel control writes outside the host route | Fails H-4 | Host | VER-002 |
| PC-15 | Rejection | Panel shows a value the host store lacks | Fails H-5 | Host | VER-002 |
| PC-16 | Acts | Model text: "Engineer A checked S-2" | No act presented | LOOP, DEL-04-03 | VER-003 |
| PC-17 | Acts | Success, queueing or receipt only | No A4–A7 presented | P, ACT | VER-003 |
| PC-18 | Acts (positive) | T2: Engineer A marks S-2 checked via the host facility; also recorded by another recorder | Actor, recorder, recording mode, capture-evidence reference, bound ⟨S-2@r12⟩ | DEL-04-03, host capture, **actual act** (DEP-05-02-017) | VER-003 |
| PC-18b | Acts (negative) | An agent-authored record of that A4 with no capture evidence | "Record without capture evidence"; no standing; clears nothing | DEL-04-03 | VER-003 |
| PC-19 | Acts (positive) | T2's A4 with no preceding A5 | Presented as A4; no acceptance prerequisite | DEL-04-03, actual act | VER-003 |
| PC-20 | Lapse | T6 (S-3 edited), then T14 (S-2 edited) | T2's A4 is unchanged after T6 and **lapsed** after T14. At a checkpoint: "waiting — lapsed at T14" before resume; after resume, lapse shown and re-hold per DEL-02-03 | DEL-04-03, host, DEL-02-03 | VER-003 |
| PC-21 | Checkpoint | Declared A4 checkpoint, reached-when *applied* for PR-2, subject class "objects changed by a named outcome" | Reached at T12; subject = the new support from RC-1; purpose and scope shown; cleared only by host-captured A4 on that content | WD, DEL-02-03, LOOP | VER-003 |
| PC-21b | Checkpoint | The same run stopped before T12 | *Not reached* at run end | LOOP | VER-003 |
| PC-21c | Checkpoint | A6 checkpoint; Engineer A declines | Act-declined event; *resolved negatively*; declared path | WD, ACT | VER-003 |
| PC-21d | Checkpoint | PC-21 reached, then the run ended without the act; Engineer A marks the new support checked afterwards | *Waiting* with the run-ended event. The later A4 is shown against the subject, and the run's disposition is unchanged | LOOP, DEL-02-03 | VER-003 |
| PC-21e | Checkpoint | A5 checkpoint, reached-when *PR-2 queued*; T11 | *Resolved negatively*, partial: item 1 accepted (WD §4.3.7) | WD, P | VER-003 |
| PC-21f | Checkpoint | A12 checkpoint; T15 A12 performed; a later A12 on an overlapping scope | *Performed*; then "superseded by ‹act›", not lapsed (PROPOSED) | ACT, DEL-04-02 | VER-003 |
| PC-22 | Autonomy | T15: Engineer A sets OP-C9 direct for scope "support labels on R-100"; OP-C4 geometry stays at *effective (policy default)* propose | T16 OP-C9 applied with origin and undo. An OP-C4 change goes to the queue. Grant display per class and scope. Scope expression per C T15 in R-8 dimensions (R2-21) | P, ACT, DEL-04-02, host | VER-003 |
| PC-23 | Policy-dependent | Operation-specific reserved addition for the first connected operation | **HELD** `UNRESOLVED{OI-021}` | Owner decision | VER-003 |
| PC-24 | Checkpoint vs grant | A5 checkpoint on OP-C4's result; grant effective direct; agent requests direct | *Not permitted*, naming the governing checkpoint constraint; no silent proposal. **AWAITING INPUT** (R2-12; host constraint handling, §8 Q-1) | P, ACT, host | VER-003 |
| PC-25 | Grant | Agent requests widening OP-C4; separately, Engineer A sets a change not yet confirmed | "Agent requests …" (A8), grant unchanged; "Set by you — not yet in force"; neither enables direct | DEL-04-02, host | VER-003 |
| PC-26 | Proposal queue | Tg: restore to g2 after a proposal citing B1 | Refusal with both bases; meaning per U-C2 | C, P, host | VER-002 |
| PC-27 | Reserved operation | Agent calls OP-C6 on S-2 | *Not permitted*, naming reserved class and policy record; A8 offered, shown only if issued; no A4 | C, ACT, host | VER-003 |
| PC-28 | No policy basis | Agent requests OP-C11 direct; Engineer A attempts A12 widening it | *Not permitted* "no policy basis (pending OI-021)". Proposal possible, with no effect until A5 and application. A12 shown *refused — no policy basis*. **HELD** (R2-9) | ACT, DEL-04-02 | VER-003 |
| PC-29 | Undo | T17: Engineer A undoes RC-2 via OP-C10 | "Applied, then reversed by RC-3". Acts on S-4's label content shown lapsed if any | P, host | VER-002 |

Present state: every case is DEFINED or AWAITING INPUT, except PC-23 and PC-28
(HELD) and PC-24 (AWAITING INPUT on host constraint evidence).

## 8. Concrete questions prepared for the external host owner

These are prepared for App-manager preparation and human relay (SoW CLM-005;
DEP-05-02-018). Writing them is not delivery, agreement or adoption. W9 owns
the relay file. They are shared with LOOP-v0.3 §13 where marked.

- **Q-1** (LOOP Q-1; R2-12). Does your route receive and honour a
  per-request governing checkpoint constraint? Or does it evaluate its own
  copy of the declaration? How would the panel see which?
- **Q-2** (LOOP Q-2; R2-20). For A4, A5, A10, A12 (and A6/A7 where
  offered), and for act-declined events, does your act facility expose a
  stable capture-evidence reference, citing act identity, actor, kind, bound
  content identity and time?
- **Q-3.** Which host views show proposed change items with old and new
  values? How does the panel reference a position in them?
- **Q-4.** How does the host show lapse, supersession (A12), stale after
  acceptance, and "applied, then reversed"?
- **Q-5** (LOOP Q-5; R2-2). Does the host offer any faithful-record
  operation? Does it meet the four R2-2 conditions?
- **Q-6.** Which host workflows exist? How does the host show identity,
  derived-from and holding library?
- **Q-7.** Does the host hold agent examination findings, and does storing
  them count as a change (C U-C5)?
- **Q-8.** Which reserved-act list does the host name and enforce (V4-HI-30;
  D2)? How does it present the grant states, including *effective (policy
  default)* and *refused — no policy basis*?
- **Q-9.** What conversation persistence and panel assembly are intended
  (OI-013)? This question is informational.

## Findings

- F-1 (retained). One executor drafted both LOOP and PANEL. IR1-C J3 found no
  hidden divergence at v0.2. The v0.3 pair needs the same independent check.
- F-2 (closed at v0.2; retained for trace). Required-tool vocabulary is
  consumed from DEL-02-01. A DEL-02-03 checker matters only under OI-014.
- F-3 (open). §3.6 consumes DEL-04-02. DEL-04-02 is not in this SoW's
  CLM-002 or register (V1-C RF-4; V1-A RF-05). Routed to C1; scope is
  unchanged here.
- F-4 (retained). OQ-11 and OI-021 are the same matter (C1).
- F-5 (retained, now R2-20). The panel depends on a host capture-evidence
  reference (Q-2). Register the missing DEP-001 item at C1.
- F-6 (new). The R2-4 wording "not exposed … reported by the host" means a
  host-returned *not exposed* is shown as a host outcome, while a name the
  loop never offered shows as a pre-validation rejection. IR1C-11 had
  proposed a loop-reported class-1 *not exposed*. R2-4 governs, and this file
  follows R2-4.

## UNRESOLVED

| Item | Owner | Point of need | Effect |
|---|---|---|---|
| OI-013 panel assembly, host/common boundary, persistence | Shared contract owner with SWB implementation owner | Before shared/host implementation boundary contracts | Behaviour only |
| OI-014 shared placement | App/shared contract owners | Before structural/production allocation | §6 candidates unagreed; OUT-004 conditional |
| OI-021 / OQ-11 first connected activity; operation-specific reserved additions; OP-C11 class | Owner via outside SWB session and App/shared owner (OQ-11: App manager, human and external SWBPIPE owner) | Before connected-activity SoW and execution / live examination | PC-23, PC-28 HELD |
| DEP-001 host panel/views, act capture (Q-2), constraint handling (Q-1), treatment, list adoption | SWBPIPE outside implementation session | Before corresponding integration/examination and fallback-replacement decision | All PC unexecuted; PC-24 AWAITING INPUT |
| DEP-05-02-017 actual human acts for positive cases | Person performing the act | When PC-07, PC-18, PC-19 and PC-21 execute | Defined only |
| C U-C5 findings location | DEL-03-01 with host owner | Before PC-12 execution | P-1/H-3 apply to referenced rows |
| WD §4.3.7 confirmation; resumption after run end; refused A12 at a checkpoint; re-hold after post-resume lapse; holding library (U-24) | DEL-02-03 (W7), DEL-02-01 | W7 | W-5b/e/f/g and §3.2 as PROPOSED |
| Host evidence that application re-checks the basis (P U-P3, narrowed) | Host owner (DEP-001) | Before PC-09b execution | Display defined |
| Which party evaluates required-tool outcomes in the host | Host owner; DEL-02-03 only under OI-014 | Before PC-05 execution | Vocabulary consumed |
| DEL-04-02 consumption (F-3) | Register owner / SoW decision at C1 | C1 | §3.6 applied pending |
| Consequence vocabulary | DEL-04-01 with host policy owner | Before class assignment | Classes as supplied |
| R2-n sibling v0.3 elements (five values, constraint, resulting objects, OP-C10/C11, exposure assumption, policy-default state, act-declined name, subject classes, T15 scope) | Respective owners | V2 / IR2 | Adopted; confirm against sibling v0.3 text |

## Verification cases

These are designed, not run.

| Case | Procedure | Expected | Serves |
|---|---|---|---|
| VC-01 | Trace §3.1–§3.6 to V4-HOST-04/SOW-019 and to the consumed definitions (C, P, WD, ACT and AS at `28bd00499`, plus R2-n) | All four interactions, plus checkpoints and grant. Consumed definitions named with versions; missing inputs visible | VER-001 |
| VC-02 | Review §2, §4 and PC-06/09/09b/10/10b/12–15/26/29 against V4-HI-10–25 and V4-EXM-20/21. On a candidate, observe them | H-1…H-6 each have a positive or rejection case. Stale-after-accept, resubmission and undo displays hold | VER-002 |
| VC-03 | Review §3.3–§3.6, §5 and PC-07/07b/08/11/12b/16–25/27/28 against the HI, AUT, D2/D3 and ACT/AS versions | "Accept" wording; actor, recorder and capture evidence shown; act-declined vs run-ended; run-end *waiting*; lapse per R2-19; §4.3.7 partial annotation; supersession; policy-default state; no-policy-basis HELD; OI-021 cases held | VER-003 |
| VC-04 | Compare §6 with the anticipated artifacts, the Clarification, V4-ARC-20 and OI-013/014 | Candidates name consumers or "not established"; none agreed; host construction external | VER-004 |
| VC-05 | Account for PC-01…PC-29 in the §7 states | One state each; no missing input counted as a pass | VER-005 |
| VC-06 | Inspect OUT-004 | Conditional; no component | VER-006 |
| VC-07 | Review SoW REQ-006 exclusions against §3 "Responsible", §6 and §8 | Each act kept with its owner; nothing performed or claimed here | VER-007 |
