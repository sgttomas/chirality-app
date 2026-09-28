# Host panel and shared interaction receiving contract
- Contribution: DEL-05-02/PANEL-v0.2
- Status: DRAFT DEFINITION — proposed, unsupplied, not implemented, not accepted
- Serves: OUT-001, OUT-002, OUT-003, OUT-004 (conditional state only); REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, REQ-006; AC-001–AC-007; VER-001–VER-007 (all of DEL-05-02)
- Basis: repo 6e18505e3; ScopeOfWork.md sha256 5c554956e91b2d8d5056176f85717cbd0e17a2d2d2991a52ea4ff185ebfd40cb; P/docs/PRD.md §2.2 V4-HOST-01/04/05/06, §3.1 V4-EXT-01, §4.1 V4-WF-03–06, §4.5 V4-AUT-01–05, §4.7 V4-REC-01/03/05, §5 V4-CST-05, §9 OQ-02/OQ-11; P/docs/ARCHITECTURE.md §3 (V4-ARC-05, reuse candidates), §4 (host implementation choices), §5 V4-ARC-20; P/docs/HOST_INTEGRATION.md §1, V4-HI-02/04, V4-HI-10–12, V4-HI-20–25, V4-HI-30–33, V4-HI-40–42, V4-HI-70/71, §10 item 7; P/docs/EXAMINATION.md V4-EXM-01–03, V4-EXM-20–22; DECISION_BRIEF.html (sha256 02d38cb1…4c420e8) d2, d3, d5; APP-V4-CLARIFICATION-20260927/DIRECTION.md; SCC-CASE-002 Case_Datasheet M1/M4 rows; Open_Issues OI-013/014/021; External_Dependencies DEP-001; run folder OWNER_DECISIONS.md (sha256 f3f8e5f3…cf81f2e; decision `APP-V4-FIRST-INCREMENT-20260928-DECISION-1`, D2 and D3), R1_RESOLUTIONS.md (sha256 2f9c7e72…e177ec4), comparisons/V1-A.md (sha256 01811533…e04c09), comparisons/V1-C.md (sha256 8d46258a…4a94a6)
- Consumed inputs:
  - Prior version: DEL-05-02/PANEL-v0.1 (sha256 07c1e1c5…be66f1e).
  - Supplier elements taken from R1_RESOLUTIONS and from V1-A/V1-C quotes, **not** read from supplier files; all to be confirmed at IR1:
    - DEL-04-01 act names A1–A14, class values, adopted D2/D3 and the treatment → outcome map (R-1, R-2, R-3);
    - DEL-04-01 label rule (R-4);
    - DEL-02-01 checkpoint reached-when, subject binding and dispositions (R-5), and the required-tool outcome vocabulary WD §4.2.4/§3.4 (V1-C D-08);
    - DEL-03-01/DEL-03-02 content identities and acceptance unit (R-6);
    - P §9 / C §4.1 outcomes (R-7);
    - DEL-04-02 grant display states and scope (R-8);
    - workflow identity tuple, generation/revision, exposure and FX-PIPE-01 (R-9).
  - Supplier versions compared at V1: DEL-02-01/WD-v0.1, DEL-03-01/C-v0.1, DEL-03-02/P-v0.1, DEL-04-01/ACT-POLICY-v0.1.
  - DEL-05-01/LOOP-v0.2: co-drafted by the same executor; compared independently at V1 (J5, v0.1).
  - DEP-001 host panel/view evidence: not received.
- Receivers: DEL-02-01 (OUT-003; REQ-005; VER-005) and DEL-05-01 (OUT-004; REQ-005; VER-007) per CASE-002 M1; external SWBPIPE owner via App-manager preparation and human file relay (CASE-002 M4; DEP-05-02-018); DEL-05-02 itself for OUT-003 (REQ-002, REQ-003, REQ-005; VER-002, VER-003, VER-005) and OUT-002/OUT-004 (REQ-004; VER-004, VER-006)

## 0. How to read this definition

- **Behaviour contract, not layout.** This contract defines what the panel
  must let the person do and see, and how it relates to the host's own
  objects. Layout, visual design, table/view construction and assembly are
  the host owner's (SoW CLM-001; ARCH §4; `UNRESOLVED{OI-013}`).
- **Semantic names only.** Names such as "proposal reference", "change
  item", "old value", "reason", "standing", "receipt reference", "subject
  content identity", "grant display state" are semantic element names. They
  are not wire fields, component names or types.
- **Standing.**
  - "Settled" means fixed by the accepted basis or by owner decision
    `APP-V4-FIRST-INCREMENT-20260928-DECISION-1`, with citation.
  - "Per R1_RESOLUTIONS R-n; to be confirmed at IR1" marks an adopted
    integration ruling or supplier v0.2 element that this executor has not
    read in the supplier's own text.
  - `UNRESOLVED{…}` is never a permission, a default or a pass.
- **Act names and labels.** Canonical act names A1–A14 (per R1_RESOLUTIONS
  R-1; to be confirmed at IR1). Unqualified "checked" means only A4.
  "Approval" means only A6. Agent work is "examination"/"findings". Host
  results say "host checks passed: ‹named checks›" (R-4).
- **Fixture subjects.** The shared fixture is **FX-PIPE-01**, owned by
  DEL-03-01 §10 (R-9). This executor has not read it. The identifiers used
  here are provisional labels, to be mapped at IR1: runs `R-101`/`R-102`;
  nodes `N-10`…`N-40`; supports `S-1`…; basis g1 with model revisions
  r12 → r13; OP-C6 "Mark row checked". They do not select the first
  connected operation (`UNRESOLVED{OI-021}`; PRD OQ-11).

## Changes from v0.1

| V1 item | Change made (section) |
|---|---|
| V1-A D-01, D-17, D-18, D-20; R-1 | Canonical act names in §3.4, §5 and the cases |
| V1-A D-03, D-23; V1-C §6 PANEL rows; R-2 | K-4: marking-checked operations are *reserved to the person* (D2a). OI-002 removed; hosts have no classifier mode (D3). PC-23 held only for OI-021 additions (§3.4, §5, PC-23) |
| V1-A D-10; V1-C D-03 | Negative decisions presented: A10 for A5; decline/stop for A4/A6/A7; the declared negative path (§3.5 W-5) |
| V1-A D-11, D-21; V1-C D-06; R-5 | **W-2 vs W-5 resolved.** W-2 presents any faithful record (A9) as a record, citing capture evidence. W-5 clears a checkpoint only on capturing-surface evidence. The approval row is aligned with the other reserved acts (§5) |
| V1-A D-12; R-4 | "Checked" labels restricted to A4; host checks and agent findings relabelled (§3.4) |
| V1-A D-22 | PC-22 reworded: "the grant keeps geometry at propose" |
| V1-A AB-06 | Host capture requirement per act kind recorded as DEP-001 (§5, UNRESOLVED) |
| V1-A AB-09 | OI-021 operation-specific additions held (UNRESOLVED) |
| V1-C D-01, D-02, D-04, D-05; R-5 | Checkpoint presentation: reached-when, bound subject, disposition vocabulary, lapse at any time (§3.5) |
| V1-C D-07; R-5 | An acceptance checkpoint forces proposal; a direct request shows *not permitted* (§3.3, PC-24) |
| V1-C D-08; R-9 | Required-tool outcome vocabulary and workflow-level states; *not exposed on this surface* vs *channel not enabled*. Closes most of v0.1 F-2 (§3.2, PC-05) |
| V1-C D-10; R-9 | Identity tuple; PC-04 uses origin classes; carried unadapted vs adapted (§3.2) |
| V1-C D-11; R-7; R-3 | Outcomes adopted unchanged from P §9 / C §4.1; *not permitted* names its treatment and policy record; "refused" vs "rejected" (§3.3) |
| V1-C D-15 | Findings location separated from domain tables; routed to C U-C5 and the host (§2, §3.4 K-2, H-3) |
| V1-C D-19 | "Failed" completion standing added (§3.1) |
| V1-C D-20 | All four model setting states and "model request refused at boundary" presented (§3.1) |
| V1-C D-23 | Re-draft shown as the agent's new proposal with lineage (§3.3, PC-09) |
| V1-C D-24; R-6 | Per-item dispositions; proposal state derived, never stronger than its items; H-2 adds origin, per-item state, stale indication; acceptance unit = change item (§3.3, §4) |
| V1-C D-25 | Accepted-then-basis-fails cites P U-P3 and the stale rule (R-6) |
| V1-C AB-01 | Mixed item decisions at an A5 checkpoint held; per-item display (§3.5) |
| V1-C AB-12 | "Act requested" (A8) presented outside checkpoints (§3.1, §5) |
| V1-C AB-14; D3 | No routine or classifier permission layer in hosts (§1) |
| R-8 (v0.1 F-3; V1-A D-06/D-07) | Grant display states and scope presented (§3.6, PC-22, PC-25); register gap noted (F-3) |
| R-9 (V1-C D-14 analogue) | PC-09 uses revision r12 → r13 within g1; generation-change case PC-26 |

## 1. Scope

A host presents the agent through a panel for **conversation, workflow
selection, the proposal queue and checks**. The agent's work appears in the
host's own tables and views, and there is no agent-private surface
(V4-HOST-04, settled). The panel is where the person talks with the agent,
selects its method and decides. Agent results are **not** held there. They
live in host objects, shown in host views.

- Roles recede behind a single agent seat and the selected workflow
  (V4-HOST-05, settled). The panel shows one agent. Role selection is not a
  panel interaction.
- **No routine or classifier permission layer in hosts** (D3, settled). The
  panel presents no tool-permission prompts. Host operation authority is the
  person's autonomy grant plus adopted policy, resolved on the host route. For
  SWB model changes the default setting is *propose* (V4-HI-41). Nothing the
  panel shows stands in for a reserved or professional act.

## 2. Definitions used by the receiving rules

| Term | Meaning in this contract |
|---|---|
| Host object | A domain object the host owns and stores (a run, node, support, load case, result set). Host domain truth stays in the host's store (V4-REC-01; V4-CST-05) |
| Domain table | A host view of host objects' domain values. An agent examination never changes it (V4-EXM-21) |
| Host view | A table, view, diagnostic or result display the host gives the person for its own objects. It is the same view the person uses without the agent (V4-HI-10) |
| Panel | The host-assembled surface for the four interactions. It may list, summarize, link and offer host decisions. It holds no domain truth |
| Agent-private result surface | Any place where the agent's results or proposed changes are visible **only** outside the host's own views, or where their content differs from the host's views. Prohibited (V4-HOST-04; SOW-020) |
| Alternate mutation route | Any path by which a change reaches host objects without the host's one validation and application route. Prohibited (V4-HI-20) |
| Findings location | Where agent examination findings (A3) are held: (a) agent message content with references into host views; or (b) host-held findings, if the host offers them. Which applies, and whether (b) is a change operation, is `UNRESOLVED{C U-C5}` with the host owner (V1-C D-15) |
| Reference | A pointer from the panel to a host object, view position, proposal, change item, receipt or record, which the person can follow into the host's own view. The panel shows references, not copies of domain values |

Panel content rules (derived from V4-HOST-04 and V4-HI-10/24; proposed):

- P-1. Everything the panel shows about an agent result or a proposed change
  is reachable in a host view with the same content. For findings, the rows
  and results they reference must be reachable in host views. Whether the
  finding text itself also appears in host views depends on the findings
  location.
- P-2. The panel may summarize a proposal (for example, "3 supports on
  R-101"). The authoritative old and new values are shown in the host's own
  views (V4-HI-24, settled).
- P-3. The panel offers no control that changes host objects except by
  submission to the host's one route. The decision controls (accept, reject,
  mark checked, grant change) are host-offered and host-captured acts (§5).

## 3. The four interactions, plus checkpoints and grant

### 3.1 Conversation

| Aspect | Receiving requirement |
|---|---|
| Person does | Writes to the agent; reads replies; follows references into host views; cancels a turn |
| Panel presents | <ul><li>**Message stream** in order, with speaker (DEL-05-01/LOOP §2.1). Completion standing: streaming, complete, truncated, interrupted, cancelled or failed.</li><li>**Tool activity** (LOOP §2.3): requested; rejected before host validation, with reason and the kind of rejection (unparseable/truncated, unknown or unoffered, schema, offer out of date); dispatched; host outcome in P §9 terms; *outcome unknown* attributed to its reporter.</li><li>**Act requests** (A8), wherever they occur.</li><li>**Model setting indicator** (LOOP §5.1): local; cloud chosen, key supplied; cloud chosen, key absent (no requests); unconfigured (no requests). No key content is shown.</li><li>**"Model request refused at boundary"** with the refused destination or "key absent".</li></ul> |
| Host objects/results | References only. Reads cite the basis and standing they describe (V4-HI-11/12; DEL-03-01/C). The panel shows the standing given, and nothing stronger (V4-AUT-02) |
| Consumed definitions | DEL-05-01/LOOP messages, events and model settings; DEL-03-01/C basis and standing; DEL-03-02/P §9 outcomes; DEL-04-03 conversation reference |
| Responsible | App/shared: this requirement. Host owner: assembly and conversation persistence (`UNRESOLVED{OI-013}`) |
| Must not | Present agent prose as a host result. Show a rejected call as executed. Show "success" as acceptance (V4-HI-25). Show an A8 request as the act |
| Unresolved | Persistence (OI-013); loop event representation (DEP-05-01-024 via DEL-05-01) |

### 3.2 Workflow selection

| Aspect | Receiving requirement |
|---|---|
| Person does | Chooses the workflow the agent follows for a run; sees what it needs and where it will stop |
| Panel presents | <ul><li>**Available workflows** with the full identity {kind, origin, source root, name, revision}, plus derived-from (V4-WF-03). The origin class is one of project, user, bundled or host.</li><li>A workflow carried from the App **unadapted keeps its original origin**. A **host adaptation** is a new identity with host origin and derived-from. There is no "App-origin" class (per R1_RESOLUTIONS R-9; to be confirmed at IR1).</li><li>**Same-named workflows** from different sources stay distinguishable.</li><li>**Declared checkpoints**: required act kind (A4, A5, A6, A7 or A12), reached-when condition, subject referent and negative path (R-5).</li><li>**Required host tools**, each with its outcome from WD §4.2.4 as adopted: *present*; *missing* (not in the catalog); *not exposed on this surface*; *version mismatch*; *present, currently unavailable* (with the catalog's unavailable reason); *channel not enabled* (a channel that is off, distinct from exposure, C §4.1); *not established* (with reason).</li><li>**Workflow-level states** (WD §3.4, §4.7): *requirements declared*; *declared empty*; *requirements undeclared* (never shown as "no requirements"); *unsupported* (with reason).</li></ul> |
| Host objects/results | The run is associated with the selected workflow identity (the tuple above), recorded with the run (V4-HI-70) |
| Consumed definitions | DEL-02-01 declaration, identity and outcome vocabulary (V1-C D-08). DEL-03-01/C, because required tools are capability references with per-surface exposure (R-9). DEL-04-01 act names. DEL-04-03 run record |
| Responsible | App/shared: this requirement. Host owner: assembly, the host's own workflows, and the evaluation producing each outcome |
| Must not | Silently rebind a selection to a same-named workflow from another source. Present a workflow as runnable unless every required tool is *present*. Collapse *not established*, *not exposed* or *currently unavailable* into present/absent |
| Unresolved | Which party computes the outcomes in the host. The vocabulary is consumed from DEL-02-01; a shared checker from DEL-02-03 is relevant only if OI-014 allocates one (V1-C D-08; WD A-5) |

### 3.3 Proposal queue

| Aspect | Receiving requirement |
|---|---|
| Person does | Reviews proposed changes in the host's tables. Accepts item by item, several items, or the whole batch (V4-HI-41). Rejects. Opens the affected objects |
| Panel presents | Each proposal shows:<ul><li>proposal reference;</li><li>**per change item**: affected objects, old/new values (in host views, P-2), reason, current item disposition;</li><li>proposal state **derived from its items and never stronger than them** (P §4.3);</li><li>origin: author type, seat, channel, conversation, workflow run with identity tuple, autonomy standing at drafting (V4-HI-21; P §3.3);</li><li>relied-on basis;</li><li>stale indication;</li><li>lineage where the proposal is a re-draft.</li></ul>Lifecycle states follow V4-HI-23 / P §4.1. Outcomes follow P §9 and C §4.1 unchanged (per R1_RESOLUTIONS R-7; to be confirmed at IR1): queued; accepted (A5, actor); rejected (A10, actor); withdrawn (A11, proposer); applied with receipt, showing the branch (direct under grant, or after acceptance); application error (effect none/partial/unknown); refused on validation, including stale with both bases; unavailable; not permitted (naming governing treatment and policy record); channel not enabled; not exposed on this surface; error; outcome unknown (attributed to its reporter, with last observed state). Every non-success shows the evaluated basis. Decision wording is **accept**, never approve (V4-HI-33, settled) |
| Host objects/results | Proposed items appear in the host's own tables as proposed (V4-EXM-20). Applied changes carry host receipts and origin marks (V4-HI-22/71) |
| Acceptance unit | The **change item** (R-6, per R1_RESOLUTIONS; to be confirmed at IR1). Row-by-row acceptance is one A5 per item. Batch or multi-row acceptance is one A5 listing several items, each bound to its change-item content identity, with per-item lapse. Applying an accepted item does not lapse the acceptance |
| Consumed definitions | DEL-03-02/P lifecycle, §9 outcomes, change-item content identity, stale refusal, re-draft lineage, no retargeting, one effect per proposal identity (a host obligation). DEL-03-01/C basis. DEL-04-01 names, wording and treatment map. DEL-04-03 act record and lapse |
| Responsible | App/shared: this requirement. Host owner: tables/views; the validation and application route; treatment resolution; receipts; offering and capturing A5/A10 (HI §1) |
| Must not | <ul><li>Show queued as applied (V4-HI-25), or accepted as applied before the receipt.</li><li>Show a host refusal as "rejected" ("rejected" is only A10).</li><li>Show a stale proposal as acceptable. It is refused with its reason (V4-HI-23).</li><li>Re-draft or retarget from the panel. A re-draft is the **agent's new proposal**, with a new identity, lineage to the refused one and fresh validation on the current basis (P §5; V1-C D-23).</li><li>Show a proposal state stronger than its items.</li><li>Use "approve".</li></ul> |
| Direct autonomy and checkpoints | Direct application is shown only when the grant display state is **effective** and direct (R-8), with origin, undo route and later-examination route (P §4.4). If a declared checkpoint requires A5 on an operation's result, that operation is forced to *propose* (R-5). An agent request to apply it directly is shown as *not permitted*, never as a silently created proposal (R-3) |
| Unresolved | Accepted-but-unapplied item whose basis fails before application: stale rule per P U-P3 (owner: host owner with DEL-03-02 and DEL-04-03). Proposal identity/duplicate mechanics (DEL-03-02 TBD-002) |

### 3.4 Checks

"Checks" covers three different subjects. They are kept apart (V4-EXM-21;
V4-AUT-03; d3; R-4 labels, settled):

| Subject | Actor | Panel label and presentation | Host objects/results | Consumed definitions |
|---|---|---|---|---|
| A3 examine: the person asks the agent to examine work | Agent | "Examination findings". Each finding references host rows/results and the read basis examined. Standing: agent findings | Findings reference rows/results. **Domain tables are not changed** by an examination (V4-EXM-21). Where findings are held follows the findings location (§2) | DEL-03-01/C basis and standing; C U-C5; LOOP E-5; DEL-04-03 record |
| Host check results: validation diagnostics, and the host's checks on results | Host | "Host checks passed: ‹named checks›", each with its evaluated basis. Standing: current or historical, checks passed, known limitations (V4-HI-12) | Host results and diagnostics | DEL-03-01/C standing |
| A4 mark checked | Person (reserved, D2a); captured by the host's act facility | "Checked by ‹person›", with bound subject content and current state (performed / lapsed) | Content-bound act record (V4-HI-32, V4-REC-05) | DEL-04-01 A4; DEL-04-03 act record and lapse |

Receiving requirements:

- K-1. Agent findings are never displayed or recorded as A4 or A6. The
  unqualified word "checked" is used only for A4 (V4-EXM-21, V4-AUT-03/05;
  R-4).
- K-2. A requested examination makes no change to domain tables. The
  receiving case compares domain-table content before and after (PC-12).
  Where findings are then held is the separate matter of the findings
  location.
- K-3. An A4 lapses visibly whenever its bound subject content changes, at
  any time after performance (V4-HI-32; R-5).
- K-4. A catalog operation whose effect is to perform or record A4, such as
  FX-PIPE-01 OP-C6 "Mark row checked", carries class **reserved to the
  person** (D2a; per R1_RESOLUTIONS R-2; to be confirmed at IR1).
  - An agent call to it is shown as *not permitted*, plus an A8 request.
  - The host names and enforces its own list (V4-HI-30). Host adoption is
    DEP-001.
  - Hosts have no classifier mode (D3).

### 3.5 Declared checkpoints in the panel

Per R1_RESOLUTIONS R-5 (to be confirmed at IR1), consuming DEL-05-01/LOOP
§2.4:

- W-5a. **Reached.**
  - A checkpoint is shown as reached only when the loop reports that its
    reached-when condition was observed.
  - The panel shows: the required act kind; the observed event that met the
    condition; the bound subject (change items, rows or output, with content
    identity).
  - The panel never marks a checkpoint reached from stage text or model
    text.
- W-5b. **Dispositions.**
  - Shared vocabulary: *waiting* · *performed* · *resolved negatively* ·
    *lapsed* · *not reached* · *unknown*.
  - *Not reached* and *unknown* are shown at run end. Neither is ever shown
    as performed.
- W-5c. **Clearing.**
  - A checkpoint shows *performed* only on attributable act evidence from the
    **capturing surface** (the host's act facility for acts on host content),
    for the specified act kind on the bound subject content.
  - A faithful record (A9) by another recorder, cited against that capture
    evidence, may be shown as a record (W-2). It does not clear the
    checkpoint on its own.
  - An agent-authored record without capture evidence clears nothing.
- W-5d. **Negative decisions.**
  - For A5 the negative is A10 reject. For A4/A6/A7 it is a recorded
    decline/stop event, which is not an act of that kind.
  - Either way the disposition is *resolved negatively*, and the panel shows
    the declared negative path (or "run stopped").
- W-5e. **Lapse** is shown whenever it occurs.
  - Before resume, the checkpoint returns to waiting for a new act on the
    current content.
  - After resume, the panel shows the lapse. Whether the run re-holds is
    DEL-02-03's (W7).
- W-5f. **Mixed item decisions at an A5 checkpoint.** The panel shows
  per-item dispositions. Whether the checkpoint is then performed, resolved
  negatively or waiting is `UNRESOLVED{V1-C AB-01}` (DEL-02-01 with DEL-02-03
  and DEL-03-02).

### 3.6 Active autonomy grant (per R1_RESOLUTIONS R-8; to be confirmed at IR1)

The proposal queue and direct application depend on the grant in force
(V4-HI-40). The panel presents it as DEL-04-02 defines it:

- **Display states**:
  - effective;
  - requested by agent (A8; no person act);
  - set by person, not yet confirmed by control;
  - unconfirmed;
  - not set;
  - refused (with reason).
- **Scope** of the grant, with representation-neutral dimensions (for
  example: model/workspace, object set, run, period, consequence).
- **Grant changes.** A grant change is A12, reserved to the person (D2e) and
  captured by the host. An agent's request for a change is shown as a
  request (A8), never as a changed grant.
- **Direct application** is shown as available only in the *effective*
  direct state.

This contract presents the grant. It does not construct grant controls
(DEL-04-02 and the host). The consumption is not yet in this SoW's CLM-002 or
register (finding F-3).

## 4. Host tables and views: no agent-private surface

| Rule | Source | Rejection case |
|---|---|---|
| H-1 Agent results and proposed changes appear in the host's own tables/views | V4-HOST-04; SOW-020 (settled) | PC-13: a result visible only in the panel |
| H-2 Proposals show, per change item, old and new values, affected objects, reason, origin, current item state and stale indication, in host views | V4-HI-24 (settled); P §8 (V1-C D-24) | PC-06 negative variant: values only in the panel |
| H-3 Findings reference host rows/results and their standing. Domain tables stay unchanged. Findings location per §2 | SoW REQ-002; V4-EXM-21; C U-C5 | PC-12 |
| H-4 No alternate mutation route | V4-HI-20 (settled) | PC-14: a panel control writes to host objects directly |
| H-5 The panel keeps consumed basis, outcome and receipt references and invents no domain truth | SoW REQ-002; V4-HI-71; V4-CST-05 | PC-15: the panel shows a value the host store does not hold |
| H-6 Agent reads show the same views and standing marks the person sees | V4-HI-10; V4-PAR-03 | PC-02 |

## 5. Acts, wording and lapse

Settled distinctions: V4-HI-25/30–33; V4-AUT-01–05; d3; D2. Names follow
R1_RESOLUTIONS R-1 and are to be confirmed at IR1.

| Act | Actor | Capture / recorder | Panel wording | Never inferred from |
|---|---|---|---|---|
| A2 apply (direct under grant) | Agent within an effective grant; host applies | Host (origin mark, undo) | "applied by agent under grant", with origin and undo (V4-HI-22) | — |
| A1 propose → queued | Agent | Host | "queued" | Success |
| A5 accept (per change item) | Person (reserved where autonomy requires a proposal, D2b) | Host act facility; faithful recorder (A9) allowed as record shape | "accept" / "accepted by ‹person›" | Success, queueing, receipt |
| A10 reject | Person | Host act facility | "rejected by ‹person›" | A host refusal |
| A11 withdraw | Proposer | Host | "withdrawn by ‹proposer›" | — |
| A2 apply (after acceptance) | Host | Host | "applied", with receipt reference | Acceptance alone |
| A3 examine | Agent | Host / record | "examination findings" | — |
| A4 mark checked | Person (reserved, D2a) | Host act facility; A9 allowed as record shape | "checked by ‹person›", with bound content | Findings, success, acceptance |
| A6 approve | Person (reserved, D2c) | Host act facility; A9 allowed as record shape (aligned with A4/A5; V1-A D-21) | "approved by ‹person›" | Anything the agent produces (V4-AUT-05) |
| A7 rely | Accountable professional (reserved, D2d) | Host act facility; A9 allowed as record shape | Recorded act only | Any other act |
| A8 request | Agent | Loop/record | "‹act kind› requested by agent" | Performance of the act |
| A12 set grant | Person (reserved, D2e) | Host | "grant set by ‹person›" | An agent request |

Receiving requirements:

- W-1. Proposal decisions say **accept**, never approve (V4-HI-33, settled).
  "Approval" appears only for A6 (R-4).
- W-2. **Record presentation (resolved with W-5).** The panel can present an
  act the person actually performed that was recorded by any identified
  recorder.
  - The panel shows the **actor** (the person), the **recorder**, the
    **recording mode** (direct capture or faithful recording) and the
    **capture evidence** reference (V4-HI-31; A9; R-5).
  - A faithful record that cites no capture evidence is shown as "record
    without capture evidence". It supports no checkpoint and no act
    standing (W-5c).
  - The panel never presents an act that was not performed.
  - Whether a particular host requires capture by its own facility for a
    given act kind is DEP-001 (V1-A AB-06).
- W-3. An act binds to its content: change-item content identity for
  A5/A10, and subject content identity for A4/A6/A7 (R-6).
  - When that content changes, the panel shows the act as lapsed, at any
    time after performance (V4-HI-32, V4-REC-05; R-5).
  - A basis failure between acceptance and application is a stale refusal,
    not a lapse (P U-P3).
- W-4. No act is taken as proof of another. There is no rule that acceptance
  must precede an independently evidenced A4, A6 or A7 (SoW REQ-003).
- W-5. Checkpoints are presented per §3.5.
- W-6. The reserved acts of D2 are settled for App/shared contracts, and
  hosts have no classifier mode (D3). Still open:
  - operation-specific additions, `UNRESOLVED{OI-021}`;
  - host adoption and capture requirements, DEP-001.

## 6. Reusable-component allocation account (OUT-002) and conditional OUT-004

Common construction needs a concrete, agreed, repeated responsibility and
receiving consumers (Clarification; V4-ARC-20; d2; SoW REQ-004). The table
lists **candidates** only. None is agreed.

| Candidate responsibility | Possible consumers | Repeated? | Agreement | Standing |
|---|---|---|---|---|
| Act and lapse presentation (actor, recorder, recording mode, capture evidence, bound content, lapsed) | SWBPIPE host panel; App standing/act display (DEL-04-02 OUT-001, where allocation justifies) | Plausible | None | Proposed candidate; question for DEL-04-02/DEL-04-03 |
| Grant display state and scope presentation (R-8) | SWBPIPE host panel; App autonomy display (DEL-04-02) | Plausible | None | Proposed candidate; question for DEL-04-02 |
| Source-qualified workflow identity and required-tool outcome presentation | SWBPIPE host panel; App workflow experience (DEL-02-02, a later undertaking per D1) | Plausible | None | Proposed candidate; DEL-02-01 OUT-003 map |
| Proposal item-disposition presentation | SWBPIPE host panel; later hosts (OI-005). The App has no host proposal queue | Not established | None | Not proposed |
| Tool-activity presentation of loop events | SWBPIPE host panel. The App presents Codex items natively (V4-ARC-05) | Not established | None | Not proposed |
| Conversation rendering | SWBPIPE host panel. The App uses Codex-native presentation | Not established | None | Not proposed |

**OUT-004 conditional state: no reusable panel component is selected, agreed
or implemented.** OUT-004 becomes an implementation obligation only for a
contribution selected under an actual responsibility and receiving agreement
(SoW AC-006). The v3 interface pieces (ARCH §3) are optional reuse sources,
not selections.

**Host construction boundary.** Host panel assembly, layout, tables/views,
domain construction, conversation persistence, treatment resolution and act
capture stay with the external host owner (SoW CLM-001; HI §1; ARCH §4).

| Open issue | Owner | Point of need | What it holds here |
|---|---|---|---|
| OI-013 | Shared contract owner with SWB implementation owner | Before shared/host implementation boundary contracts | Panel assembly and the host/common construction boundary |
| OI-014 | App/shared contract owners | Before structural/production contract allocation | Whether any candidate becomes shared, and where it lives |

## 7. Receiving case inventory (OUT-003)

All cases are **DESIGNED — UNEXECUTED**. There is no host candidate (DEP-001
not received), and supplier v0.2 versions are to be confirmed at IR1. A
missing input is not a passed case (SoW VER-005).

| Case | Interaction | Stimulus (provisional label; FX-PIPE-01 mapping at IR1) | Expected result | Inputs needed to execute | Serves |
|---|---|---|---|---|---|
| PC-01 | Conversation | Agent answers with a read of `R-101` supports | Reply references host view rows; basis and standing shown as given | C, LOOP, host views | VER-001, VER-002 |
| PC-02 | Conversation | Agent reads a historical result | Shown as historical, never current (V4-HI-12) | C, host results | VER-002 |
| PC-03 | Conversation | Loop rejects a truncated tool call | "Rejected before host validation: truncated", not executed | LOOP MC-1, DEP-05-01-024 | VER-001 |
| PC-03b | Conversation | Model setting "cloud chosen, key absent"; loop attempts a turn | Indicator shows key absent; "model request refused at boundary"; no key content | LOOP §5, host | VER-001 |
| PC-04 | Workflow selection | Two workflows named "support-adjust": one origin *user* (carried unadapted from the App), one origin *host* (host adaptation, derived-from the first) | Both shown with the full identity tuple; the adaptation shows derived-from; the selection binds to the chosen revision | DEL-02-01, host workflow list | VER-001 |
| PC-05 | Workflow selection | Required tools: one *present*, one *not exposed on this surface*, one *present, currently unavailable*; a second workflow has *requirements undeclared* | Each outcome shown distinctly with reason; the first workflow is not shown runnable; the second shows "requirements undeclared", not "no requirements" | DEL-02-01 vocabulary, C exposure, host evaluation | VER-001 |
| PC-06 | Proposal queue | Agent proposes supports `S-7`, `S-8`, `S-9` on `R-101` as three change items | Proposed items with old/new values, objects, reason, origin and item state in host tables; proposal state derived from items. Negative variant: values only in the panel → fail | P, C, host tables | VER-002 |
| PC-07 | Proposal queue | Person accepts `S-7` and `S-8` item by item and rejects `S-9` | "Accept" wording; two A5 acts, each item-bound; `S-9` rejected (A10, actor shown); `S-7`/`S-8` applied with receipts and origin marks; proposal state never stronger than items | P, host route/receipts, actual person acts | VER-002, VER-003 |
| PC-07b | Proposal queue | Person accepts `S-7`, `S-8`, `S-9` as one batch | One A5 listing three items, each bound to its change-item content identity; per-item lapse possible | P, DEL-04-03 | VER-003 |
| PC-08 | Proposal queue | Operation reports success on submission | Shown "queued", not "applied" or "accepted" (V4-HI-25) | P | VER-003 |
| PC-09 | Proposal queue | Basis g1/r12; person edits `N-30` (model revision r13 within g1) after the agent proposed `S-7` there | Refused as stale, showing both bases. A re-draft appears as the agent's **new** proposal with lineage to the refused one. No panel re-draft or retarget | P, C, host | VER-002 |
| PC-10 | Proposal queue | Application outcome cannot be observed | "Outcome unknown", attributed to its reporter, with last observed state; not applied or failed | P, LOOP | VER-002 |
| PC-11 | Proposal queue | Any proposal decision control | Wording is "accept"; any "approve" in proposal decisions fails | P, DEL-04-01 | VER-003 |
| PC-12 | Checks | Person asks the agent to examine `R-102` | Findings reference rows/results and basis; domain-table content identical before and after; labeled "examination findings", never "checked". Findings location noted per §2 | C, LOOP, host; C U-C5 | VER-002, VER-003 |
| PC-12b | Checks | Host validation passes on `R-102` | "Host checks passed: ‹named checks›", with evaluated basis; not "checked" | C | VER-003 |
| PC-13 | Rejection | Agent result visible only in the panel (no host view) | Fails H-1 | Host | VER-002 |
| PC-14 | Rejection | Panel control writes to host objects outside the host route | Fails H-4 | Host | VER-002 |
| PC-15 | Rejection | Panel shows a value the host store does not hold | Fails H-5 | Host | VER-002 |
| PC-16 | Acts | Model text says "the engineer checked `R-102`" | No act presented; passes only if nothing is shown as performed | LOOP, DEL-04-03 | VER-003 |
| PC-17 | Acts | Agent success, queueing or receipt only | No A4–A7 presented | P, DEL-04-01 | VER-003 |
| PC-18 | Acts (positive) | The person actually performs A4 on `R-102` through the host's act facility; an agent or host also records it | Actor = person; recorder shown; recording mode; capture evidence reference; bound subject content | DEL-04-03, host capture, **actual human act** (DEP-05-02-017) | VER-003 |
| PC-18b | Acts (negative) | Agent-authored faithful record of an A4 the person mentioned, with no capture evidence | Shown as "record without capture evidence"; no act standing; no checkpoint cleared | DEL-04-03 | VER-003 |
| PC-19 | Acts (positive) | Independently evidenced A4 with no preceding A5 | Presented as A4; no synthetic acceptance prerequisite | DEL-04-03, actual human act (DEP-05-02-017) | VER-003 |
| PC-20 | Lapse | `R-102` content changes after PC-18, both before and after the run resumed | Act shown lapsed in both cases; before resume the checkpoint returns to waiting; after resume re-hold per DEL-02-03 | DEL-04-03, host, DEL-02-03 | VER-003 |
| PC-21 | Checkpoint | Run with a declared A4 checkpoint, reached-when "after proposal applied" (invented) | Shown reached only on the observed outcome; waiting for A4 on the bound rows; cleared only by host-captured A4 on that content | DEL-02-01, DEL-02-03, LOOP | VER-003 |
| PC-21b | Checkpoint | Same run cancelled before the condition occurs | Checkpoint shown *not reached* at run end; never performed | LOOP | VER-003 |
| PC-21c | Checkpoint | A6 checkpoint; the person records a decline | *Resolved negatively*; declared negative path shown; no A6 | DEL-02-01, DEL-04-01 | VER-003 |
| PC-22 | Autonomy | Person allows direct application for one low-consequence class; **the grant keeps geometry at propose** (V4-EXM-22 shape) | Direct changes show origin and undo; geometry changes go to the queue; grant shown *effective* with scope | P, DEL-04-01 policy, DEL-04-02 states, host | VER-003 |
| PC-23 | Policy-dependent | An operation-specific reserved addition for the first connected operation | **Held**: `UNRESOLVED{OI-021}`; no expected result asserted | Owner decision via OI-021 | VER-003 |
| PC-24 | Checkpoint vs grant | Declared A5 checkpoint on a change; grant is effective direct; agent requests direct application | Shown *not permitted*, naming treatment; no silent proposal; the agent's proposal, if made, queues and the checkpoint waits | R-3/R-5, P, host | VER-003 |
| PC-25 | Grant | Agent requests widening; separately, the person sets a change that the control has not yet confirmed | First shown "requested by agent" (A8), grant unchanged; second shown "set by person, not yet confirmed by control"; neither enables direct application | DEL-04-02, host | VER-003 |
| PC-26 | Proposal queue | Host restore starts generation g2 after a proposal citing g1/r12 | Refusal shows both bases; meaning per DEL-03-01/03-02 at IR1 | C, P, host | VER-002 |
| PC-27 | Reserved operation | Agent calls OP-C6 "Mark row checked" | *Not permitted*, naming treatment and policy record; A8 request shown; no A4 | C, DEL-04-01, host | VER-003 |

Case accounting states: DEFINED; EXECUTED on an identified candidate (with
configuration and date, V4-EXM-01); LIMITED; AWAITING INPUT (named input);
HELD (named decision). Present state: all cases DEFINED/AWAITING INPUT except
PC-23, which is HELD on OI-021.

## 8. Concrete questions prepared for the external host owner

These questions are prepared for App-manager preparation and human relay (SoW
CLM-005; DEP-05-02-018). Writing them here is not delivery, agreement or
adoption. W9 owns the relay file.

1. Which host views show proposed change items with old and new values, and
   how does the panel reference a position in them (H-1, H-2, PC-06)?
2. Where does the host offer and capture A5, A10, A4 and A12? Does it require
   capture by its own facility for each act kind? How does its record keep
   actor, recorder and recording mode apart (W-2)?
3. How does the host show lapse of a content-bound act (W-3, PC-20)?
4. How does the host present outcome unknown, stale refusal with both bases,
   and not permitted with the governing treatment (PC-09, PC-10, PC-24)?
5. Which host workflows exist, and how does the host show a workflow's full
   identity, including derived-from (PC-04)?
6. Does the host hold agent examination findings, and if so, where? Does it
   treat storing them as a change (C U-C5; PC-12)?
7. Which list of reserved acts does the host name and enforce (V4-HI-30; D2),
   and how does it present the grant display states (PC-22, PC-25)?
8. What conversation persistence and panel assembly does the host owner
   intend (OI-013)? This question is informational.

## Findings

- F-1 (retained). One executor drafted both LOOP and PANEL. V1-C J5 compared
  v0.1 independently. The v0.2 pair needs IR1 review of the same join.
- F-2 (mostly closed by V1-C D-08). The panel consumes DEL-02-01's
  required-tool outcome vocabulary, which is a CLM-002 input. A DEL-02-03
  checker is relevant only if OI-014 allocates one.
- F-3 (open; R-8 applied). The panel presents DEL-04-02 grant states and
  scope, per R-8. DEL-04-02 is not in this SoW's CLM-002 or Dependencies.csv
  (V1-C RF-4; V1-A RF-05). Routed to closeout C1 for the register or SoW
  decision. Scope is not changed here.
- F-4 (retained). PRD OQ-11 and OI-021 name the same matter (V1-C RF-9;
  C1).
- F-5 (new). R-5 requires capturing-surface evidence to clear a checkpoint.
  The panel therefore depends on each host act facility exposing a capture
  evidence reference that a panel can cite. This is not yet among the
  DEP-001 items listed in the SoW. It is carried as question 2 in §8.

## UNRESOLVED

| Item | Owner | Point of need | Effect on this definition |
|---|---|---|---|
| OI-013 panel assembly, host/common construction boundary, conversation persistence | Shared contract owner with SWB implementation owner | Before shared/host implementation boundary contracts | Behaviour only; no layout, assembly or persistence |
| OI-014 shared contract/component placement | App/shared contract owners | Before structural/production contract allocation | §6 candidates unagreed; OUT-004 conditional, no component |
| OI-021 / PRD OQ-11 first connected activity; operation-specific reserved additions (D2) | Owner via outside SWB session and App/shared owner (OQ-11: App manager, human and external SWBPIPE owner) | Before connected-activity SoW and execution / dependent implementation or live connected examination | PC-23 held; fixture subjects provisional |
| DEP-001 host panel/view, act capture, treatment resolution, adoption of its reserved-act list | SWBPIPE outside implementation session | Before corresponding connected-journey integration/examination and fallback-replacement decision | All PC cases unexecuted |
| DEP-05-02-017 actual human act for positive cases | Person performing the act | When PC-07, PC-18 and PC-19 execute | Positive cases defined, not executable |
| C U-C5 findings location and whether host-held findings are a change | DEL-03-01 with host owner | Before PC-12 execution | P-1 and H-3 applied to referenced rows only |
| V1-C AB-01 mixed item decisions at an A5 checkpoint | DEL-02-01 with DEL-02-03 and DEL-03-02 | Before PC-07 as a checkpoint case | W-5f per-item display only |
| Re-hold after post-resume lapse | DEL-02-03 (W7) | W7 | W-5e shows lapse only |
| Accepted item whose basis fails before application (P U-P3) | Host owner with DEL-03-02 and DEL-04-03 | Before dependent fixtures | Shown as stale refusal, not lapse |
| Which party evaluates required-tool outcomes in the host | Host owner; DEL-02-03 only if OI-014 allocates a shared checker | Before PC-05 execution | Vocabulary consumed; evaluator open |
| DEL-04-02 consumption (F-3) | Register owner / SoW decision at C1 | C1 | §3.6 applied per R-8 pending that decision |
| Consequence vocabulary for class assignment | DEL-04-01 with host policy owner | Before class assignment | Classes shown as supplied |
| FX-PIPE-01 mapping of provisional labels | DEL-03-01 with this owner | IR1 | Labels provisional |
| All R1_RESOLUTIONS-derived elements | Respective owners | IR1 | Adopted, not yet confirmed against supplier v0.2 text |

## Verification cases

These cases are designed, not run.

| Case | Procedure | Expected result | Serves |
|---|---|---|---|
| VC-01 | Trace §3.1–3.4, plus §3.5 and §3.6, one at a time to V4-HOST-04/SOW-019 and to the consumed definitions, host objects/results and responsible participants | All four interactions present; each names its consumed definitions (with R-n markers), host objects, responsibility and missing inputs (F-3 visible) | VER-001 |
| VC-02 | Review §2, §4 and PC-06, PC-09, PC-10, PC-12–PC-15, PC-26 against V4-HI-10–25 and V4-EXM-20/21. On a host candidate, observe item views, old/new values, reason, origin, bases, receipts and examination without table change | Each of H-1…H-6 has a positive or a rejection case; until a candidate exists, all DESIGNED — UNEXECUTED | VER-002 |
| VC-03 | Review §3.3–§3.6, §5 and PC-07/07b/08/11/12b/16–25/27 against V4-HI-25/30–33/40–42/70–71, d3, V4-AUT-01–05, D2/D3, and the DEL-04-01/04-02/04-03 versions at IR1 | "Accept" wording; canonical names; actor, recorder and capture shown; W-2/W-5 consistent; lapse at any time; negatives shown; no cross-act inference; OI-021 cases held only | VER-003 |
| VC-04 | Compare §6 with D anticipated artifacts, the Clarification, V4-ARC-20 and OI-013/014 | Each candidate names consumers and repeated responsibility, or "not established"; none agreed; host construction external | VER-004 |
| VC-05 | Account for PC-01…PC-27: consumed-definition identity, candidate binding, state | Every case is in one accounting state; no missing input is counted as a pass | VER-005 |
| VC-06 | Inspect the OUT-004 state | Conditional, no component, allocation open at OI-013/OI-014 | VER-006 |
| VC-07 | Review every excluded act in SoW REQ-006 against the §3 "Responsible" rows, §6 and §8 | Each act kept with its owner; no host construction, policy decision or human act performed or claimed here | VER-007 |
