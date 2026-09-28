# Host panel and shared interaction receiving contract
- Contribution: DEL-05-02/PANEL-v0.1
- Status: DRAFT DEFINITION — proposed, unsupplied, not implemented, not accepted
- Serves: OUT-001, OUT-002, OUT-003, OUT-004 (conditional state only); REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, REQ-006; AC-001–AC-007; VER-001–VER-007 (all of DEL-05-02)
- Basis: repo 6e18505e3; ScopeOfWork.md sha256 5c554956e91b2d8d5056176f85717cbd0e17a2d2d2991a52ea4ff185ebfd40cb; P/docs/PRD.md §2.2 V4-HOST-04/05/06, §3.1 V4-EXT-01, §4.1 V4-WF-03–06, §4.5 V4-AUT-01–05, §4.7 V4-REC-03/05, §5 V4-CST-05, §9 OQ-02/OQ-11; P/docs/ARCHITECTURE.md §4 (host implementation choices), §5 V4-ARC-20; P/docs/HOST_INTEGRATION.md §1, V4-HI-02/04, V4-HI-10–12, V4-HI-20–25, V4-HI-30–33, V4-HI-40–42, V4-HI-70/71, §10 item 7; P/docs/EXAMINATION.md V4-EXM-01–03, V4-EXM-20–22; DECISION_BRIEF.html (sha256 02d38cb1…4c420e8) d2, d3, d5; APP-V4-CLARIFICATION-20260927/DIRECTION.md; SCC-CASE-002 Case_Datasheet M1/M4 rows; Open_Issues OI-001/002/013/014/021; External_Dependencies DEP-001
- Consumed inputs: accepted basis only. DEL-02-01 (workflow declaration and source identity), DEL-03-01/C (catalog entry, read basis, standing), DEL-03-02/P (proposal lifecycle per V4-HI-23, outcomes, host-view information per V4-HI-24), DEL-04-01 (act and operation-policy distinctions), DEL-04-03 (record semantics: actor/recorder, content binding, lapse) are referenced by accepted meaning only, to be reconciled at V1. DEL-05-01/LOOP-v0.1 (loop messages/tools/events/checkpoints) was co-drafted in this run by the same executor; its independent comparison belongs to V1. DEP-001 host panel/view evidence: not received.
- Receivers: DEL-02-01 (OUT-003; REQ-005; VER-005) and DEL-05-01 (OUT-004; REQ-005; VER-007) per CASE-002 M1; external SWBPIPE owner via App-manager preparation and human file relay (CASE-002 M4; DEP-05-02-018); DEL-05-02 itself for OUT-003 (REQ-002, REQ-003, REQ-005; VER-002, VER-003, VER-005) and OUT-002/OUT-004 (REQ-004; VER-004, VER-006)

## 0. How to read this definition

- **Behaviour contract, not layout.** This defines what the panel must let
  the person do and see, and how it relates to the host's own objects. The
  host owner decides layout, visual design, table/view construction and
  assembly (SoW CLM-001; ARCH §4; `UNRESOLVED{OI-013}`).
- **Semantic names only.** Names such as "proposal reference", "affected
  objects", "old value", "new value", "reason", "standing", "receipt
  reference" and "bound content identity" are semantic element names. They
  are not wire fields, component names or types. No transport, persistence,
  component library or placement is selected (OI-013, OI-014).
- **Standing.** "Settled" marks a distinction fixed by the accepted basis,
  with its citation. Other requirements are proposed for V1 review.
  `UNRESOLVED{…}` is never a permission, a default or a pass.
- **Fixture subjects.** Examples use an invented piping model (runs `R-101`,
  `R-102`; nodes `N-10`…`N-40`; supports `S-1`…). They do not select the
  first connected operation (`UNRESOLVED{OI-021}`; PRD OQ-11).

## 1. Scope

A host presents the agent through a panel for **conversation, workflow
selection, the proposal queue and checks**. The agent's work appears in the
host's own tables and views, and there is no agent-private surface
(V4-HOST-04, settled). The panel is where the person talks with the agent,
selects its method and makes decisions. It is **not** where agent results
live. Results live in host objects and are shown in host views.

Roles recede in hosts behind a single agent seat and the selected workflow
(V4-HOST-05, settled). The panel therefore shows one agent. Role selection
is not a panel interaction.

## 2. Definitions used by the receiving rules

| Term | Meaning in this contract |
|---|---|
| Host object | A domain object the host owns and stores (a run, node, support, load case, result set). Host domain truth stays in the host's store (V4-REC-01; V4-CST-05) |
| Host view | A table, view, diagnostic or result display the host provides to the person for its own objects, the same one the person uses without the agent (V4-HI-10) |
| Panel | The host-assembled surface for the four interactions. It may list, summarize, link and offer decisions. It holds no domain truth |
| Agent-private result surface | Any place where the agent's results, proposed changes or findings are visible **only** outside the host's own views, or where their content differs from what the host's views show. Prohibited (V4-HOST-04; SOW-020) |
| Alternate mutation route | Any path by which a change reaches host objects without the host's one validation and application route. Prohibited (V4-HI-20) |
| Reference | A pointer from the panel to a host object, view position, proposal, receipt or record that the person can follow into the host's own view. Proposed rule: the panel shows references, not copies of domain values |

Panel content rules (derived from V4-HOST-04, V4-HI-10/24; proposed):

- P-1. Everything the panel shows about an agent result, proposal or
  finding is reachable in a host view with the same content.
- P-2. The panel may show a short summary of a proposal (e.g. "3 supports
  on R-101"). The authoritative old and new values are shown in the host's
  own views (V4-HI-24, settled).
- P-3. The panel never offers a control that changes host objects except by
  submitting to the host's one route. Decision controls (accept, reject) are
  host-offered acts recorded by the host (§5).

## 3. The four interactions: trace to consumed definitions and host objects

### 3.1 Conversation

| Aspect | Receiving requirement |
|---|---|
| Person does | Writes to the agent; reads replies; follows references into host views; cancels a turn |
| Panel presents | Message stream in order, with speaker (DEL-05-01/LOOP §2.1). Streaming standing (streaming, complete, truncated, interrupted, cancelled). Tool activity as events: requested, rejected before host validation (with reason), dispatched, host outcome (DEL-05-01/LOOP §2.3). Model setting indicator: local, or cloud chosen by the person (V4-HOST-01), with no key content |
| Host objects/results | References only. Reads cite the basis and standing they describe (V4-HI-11/12, DEL-03-01/C); the panel shows the standing given and nothing stronger (V4-AUT-02) |
| Consumed definitions | DEL-05-01/LOOP messages and events; DEL-03-01/C basis and standing; DEL-04-03 conversation reference in the run record |
| Responsible | App/shared: this requirement. Host owner: assembly and conversation persistence (`UNRESOLVED{OI-013}`) |
| Must not | Present agent prose as a host result; show a rejected tool call as executed; show "success" as acceptance (V4-HI-25) |
| Unresolved | Persistence (OI-013). Loop event representation (DEP-05-01-024 via DEL-05-01) |

### 3.2 Workflow selection

| Aspect | Receiving requirement |
|---|---|
| Person does | Chooses the workflow the agent follows for a run; sees what it needs and where it will stop |
| Panel presents | Available workflows with source-qualified identity (origin, name, revision), so same-named workflows from different sources stay distinguishable (V4-WF-03 via DEL-02-01). The host's own workflows (V4-HOST-06) and workflows carried from the App (V4-WF-06) are both shown with origin. Declared checkpoints and the act each requires (DEL-02-01; act kinds per DEL-04-01). Required host tools, and whether each is present in this host (V4-WF-04) |
| Host objects/results | The run is associated with the selected workflow identity and version, recorded with the run (V4-HI-70) |
| Consumed definitions | DEL-02-01 declaration and source identity. DEL-03-01/C, because required tools are capability references into the catalog. DEL-04-01 act names. DEL-04-03 run record (workflow and version) |
| Responsible | App/shared: this requirement. Host owner: assembly and the host's own workflows |
| Must not | Silently rebind a selected workflow to a same-named one from another source. Present a workflow as runnable when a required tool is absent |
| Unresolved | Missing-tool determination is DEL-02-03 behaviour (V4-WF-04), which is not a consumed input in this SoW's CLM-002. See finding F-2 |

### 3.3 Proposal queue

| Aspect | Receiving requirement |
|---|---|
| Person does | Reviews proposed changes in the host's tables; accepts row by row, several rows or the whole batch; rejects; opens the affected objects (V4-HI-41, the SWB default by owner direction, settled as that default) |
| Panel presents | Each proposal with: proposal reference; lifecycle state per V4-HI-23 (drafted, validated, queued, accepted, applied with receipt; or rejected, withdrawn, stale, outcome unknown); affected objects; the reason; origin (agent, conversation, workflow run, per V4-HI-21); relied-on basis. Old and new values are shown in the host's views (P-2). Decision wording is **accept**, never approve (V4-HI-33, settled) |
| Host objects/results | Proposed rows are shown in the host's own tables as proposed (V4-EXM-20 "proposed rows and old and new values in the host's own tables"). Applied changes carry host receipts and origin marks (V4-HI-22/71) |
| Consumed definitions | DEL-03-02/P lifecycle, outcome taxonomy, host-view information, stale refusal and re-draft, no retargeting, one effect on repeated submission. DEL-03-01/C basis. DEL-04-01 accept wording and act distinctions. DEL-04-03 act record and lapse |
| Responsible | App/shared: this requirement. Host owner: tables/views, the validation/application route, receipts, and the offering and recording of acceptance (HI §1) |
| Must not | Show queued as applied (V4-HI-25). Show accepted as applied before the receipt. Show a stale proposal as acceptable; it is refused with its reason and may be re-drafted on the current basis (V4-HI-23). Retarget a proposal to a later selection (V4-HI-23). Use "approve" |
| Unresolved | What happens to an accepted-but-unapplied proposal whose basis changes: for DEL-03-02/P at V1. Proposal identity and duplicate mechanics (DEL-03-02 TBD-002) |

### 3.4 Checks

"Checks" covers three different subjects. They are kept apart (V4-EXM-21;
V4-AUT-03; d3, settled):

| Subject | Actor | Panel presents | Host objects/results | Consumed definitions |
|---|---|---|---|---|
| Agent check (the person asks the agent to check work) | Agent | Findings, each attached by reference to host rows/results, with the finding's standing (agent finding) | Findings reference rows/results. **Host tables are not changed** by a check (V4-EXM-21) | DEL-03-01/C read basis and standing; DEL-05-01/LOOP events; DEL-04-03 record |
| Host check results (validation diagnostics, the host's own checks on results) | Host | The host's result standing: current or historical, checks passed, known limitations (V4-HI-12) | Host results and diagnostics | DEL-03-01/C standing |
| Human checking act (marking work checked) | Person; host records | The act, with actor, the bound content and its current state (valid or lapsed) | Content-bound act record (V4-HI-32, V4-REC-05) | DEL-04-01 act kind; DEL-04-03 act record and lapse |

Receiving requirements:

- K-1. An agent finding is never displayed or recorded as a human Checked
  act or an approval (V4-EXM-21, V4-AUT-03/05, settled).
- K-2. A requested agent check produces no change to host tables. The
  receiving case compares table content before and after (PC-12).
- K-3. A human checking act lapses visibly when its bound content changes
  (V4-HI-32, settled).
- K-4. Which operations reserve marking checked to the person, and whether
  any classifier-based permission affects checking, are
  `UNRESOLVED{OI-001}` and `UNRESOLVED{OI-002}`. The panel carries
  DEL-04-01's adopted policy and has no default.

## 4. Host tables and views: no agent-private surface

| Rule | Source | Rejection case |
|---|---|---|
| H-1 Agent work and proposed changes appear in the host's own tables/views | V4-HOST-04; SOW-020 (settled) | PC-13: a result visible only in the panel |
| H-2 Proposals show old and new values, affected objects and reason in host views | V4-HI-24 (settled) | PC-06 negative variant: values only in panel |
| H-3 Check findings refer to host rows/results and their standing | SoW REQ-002; V4-EXM-21 | PC-12 |
| H-4 No alternate mutation route | V4-HI-20 (settled) | PC-14: panel control writes to host objects directly |
| H-5 The panel keeps consumed basis, outcome and receipt references. It invents no independent domain truth | SoW REQ-002; V4-HI-71; V4-CST-05 | PC-15: panel shows a value the host store does not hold |
| H-6 Agent reads show the same views and standing marks the person sees | V4-HI-10; V4-PAR-03 | PC-02 |

## 5. Acts, wording and lapse

Settled distinctions (V4-HI-25/30–33; V4-AUT-01–05; d3 "Preserve the meanings
through the UI"):

| Subject | Actor | Recorder | Panel wording / presentation | Never inferred from |
|---|---|---|---|---|
| Execution (operation ran) | Host on the agent's call | Host | "ran", with outcome | — |
| Direct application under granted autonomy | Agent within the person's grant | Host (origin mark, undo) | "applied by agent", with origin and undo (V4-HI-22) | — |
| Queued proposal | Host | Host | "queued" | Success |
| Acceptance of a proposed edit | Person | Host (or a faithful recorder) | "accept" / "accepted by <person>" | Success, queueing, receipt |
| Application of an accepted proposal | Host | Host | "applied", with receipt reference | Acceptance alone |
| Agent check findings | Agent | Host / record | "finding" | — |
| Marking checked | Person | Host (or a faithful recorder) | "checked by <person>", with bound content | Findings, success, acceptance |
| Approval | Person | Host | Presented only as a recorded act of the person | Anything the agent produces (V4-AUT-05) |
| Professional reliance | Accountable professional | Host, if recorded | Recorded act only | Any other act |

Receiving requirements:

- W-1. Proposal decisions say **accept**, never approve (V4-HI-33, settled).
- W-2. The panel can present an act the person actually performed that an
  agent or host recorded. It shows the **actor** (the person) apart from the
  **recorder** (SoW REQ-003; DEL-04-03). It never presents an act that was
  not performed (V4-HI-31, settled).
- W-3. An act binds to its content. When that content changes, the panel
  shows the act as lapsed and does not hide it (V4-HI-32, V4-REC-05,
  settled).
- W-4. No act is taken as proof of another. The panel imposes no rule that
  acceptance must come before an independently evidenced checking, approval
  or reliance act (SoW REQ-003).
- W-5. A declared workflow checkpoint shows as "waiting for <act kind>". It
  clears only on the host's record of that act (V4-WF-05, V4-HI-42;
  DEL-05-01/LOOP §2.4).
- W-6. Operation-specific reserved-act and classifier treatment is carried,
  not decided: `UNRESOLVED{OI-001}`, `UNRESOLVED{OI-002}`.

## 6. Reusable-component allocation account (OUT-002) and conditional OUT-004

Common construction needs a concrete, agreed, repeated responsibility and
receiving consumers (Clarification; V4-ARC-20; d2; SoW REQ-004). The table
lists **candidates** for OI-014/OI-013 discussion. None is agreed.

| Candidate responsibility | Possible consumers | Repeated? | Agreement | Standing |
|---|---|---|---|---|
| Act and lapse presentation (actor/recorder, bound content, lapsed) | SWBPIPE host panel; App standing/act display (DEL-04-02 OUT-001, App/shared components where allocation justifies) | Plausible: the same meaning is shown in two expressions | None | Proposed candidate; question for DEL-04-02 and DEL-04-03 at V1 |
| Source-qualified workflow identity presentation | SWBPIPE host panel; App workflow experience (DEL-02-02) | Plausible | None | Proposed candidate; DEL-02-01 OUT-003 responsibility map |
| Proposal lifecycle state presentation (queued / accepted / applied / stale / unknown) | SWBPIPE host panel; any later host (OI-005 open). The App has no host proposal queue | Not established: one identified consumer | None | Not proposed |
| Tool-activity presentation of loop events | SWBPIPE host panel. The App presents Codex items natively (V4-ARC-05), not loop events | Not established | None | Not proposed |
| Conversation rendering | SWBPIPE host panel; the App uses Codex-native presentation | Not established | None | Not proposed |

OUT-004 conditional state: **no reusable panel component is selected,
agreed or implemented.** OUT-004 becomes an implementation obligation only
for a contribution selected under an actual responsibility and receiving
agreement (SoW AC-006). Existing v3 interface pieces (ARCH §3 reuse
candidates) are optional reuse sources. They are not selections.

Host construction boundary: host panel assembly, layout, tables/views,
domain construction and conversation persistence stay with the external
host owner (SoW CLM-001; HI §1; ARCH §4). Neither this account nor a
prepared handoff transfers them.

| Open issue | Owner | Point of need | What it holds here |
|---|---|---|---|
| OI-013 | Shared contract owner with SWB implementation owner | Before shared/host implementation boundary contracts | Panel assembly and the host/common construction boundary for the panel-receiving portion |
| OI-014 | App/shared contract owners | Before structural/production contract allocation | Whether any candidate above becomes a shared component, and where it lives |

## 7. Receiving case inventory (OUT-003)

All cases are **DESIGNED — UNEXECUTED**. None has a host candidate
(DEP-001 not received), and none has supplied versions of the consumed
definitions (V1 pending). A missing input is not a passed case (SoW VER-005).

| Case | Interaction | Stimulus (fixture subject) | Expected result | Inputs needed to execute | Serves |
|---|---|---|---|---|---|
| PC-01 | Conversation | Agent answers with a read of `R-101` supports | Reply references host view rows; basis and standing shown as given | C, LOOP, host views | VER-001, VER-002 |
| PC-02 | Conversation | Agent reads a historical result | Shown as historical, never current (V4-HI-12) | C, host results | VER-002 |
| PC-03 | Conversation | Loop rejects a truncated tool call | Panel shows "rejected before host validation", not executed | LOOP (DEL-05-01 MC-1), DEP-05-01-024 | VER-001 |
| PC-04 | Workflow selection | Two workflows named "support-adjust", one host-origin and one App-origin | Both shown with origin and revision; the selection binds to the chosen one | DEL-02-01, host workflow list | VER-001 |
| PC-05 | Workflow selection | Selected workflow requires a tool absent in this host | Absence shown; not presented as runnable | DEL-02-03 behaviour (F-2), C | VER-001 |
| PC-06 | Proposal queue | Agent proposes supports `S-7`, `S-8`, `S-9` on `R-101` | Proposed rows with old/new values, objects and reason appear in host tables; panel lists 3 queued proposals with references. Negative variant: values appear only in panel → fail | P, C, host tables | VER-002 |
| PC-07 | Proposal queue | Person accepts `S-7` and `S-8` row by row and rejects `S-9` | "Accept" wording; `S-7`/`S-8` accepted then applied with receipt references; `S-9` rejected; origin marks on applied rows | P, host route/receipts, actual person act | VER-002, VER-003 |
| PC-08 | Proposal queue | Operation reports success on submission | Panel shows "queued", not "applied" or "accepted" (V4-HI-25) | P | VER-003 |
| PC-09 | Proposal queue | Person edits `N-30` after the agent proposed `S-7` there | Proposal shown stale with reason; re-draft offered on the current basis; not retargeted (V4-EXM-20 "stale proposal refused") | P, C, host | VER-002 |
| PC-10 | Proposal queue | Application outcome cannot be observed | Shown as "outcome unknown", not applied or failed | P | VER-002 |
| PC-11 | Proposal queue | Any proposal decision control | Wording is "accept"; "approve" anywhere in proposal decisions fails | P, DEL-04-01 | VER-003 |
| PC-12 | Checks | Person asks the agent to check `R-102` | Findings attach to rows/results by reference; table content identical before and after; findings not shown as "checked" | C, LOOP, host | VER-002, VER-003 |
| PC-13 | Rejection | Agent result visible only in the panel (no host view) | Fails H-1 | Host | VER-002 |
| PC-14 | Rejection | Panel control writes to host objects outside the host route | Fails H-4 | Host | VER-002 |
| PC-15 | Rejection | Panel shows a value the host store does not hold | Fails H-5 | Host | VER-002 |
| PC-16 | Acts | Model text says "the engineer checked `R-102`" | No act presented; negative passes only if nothing is shown as performed | LOOP, DEL-04-03 | VER-003 |
| PC-17 | Acts | Agent success, queueing or receipt only | No acceptance, check, approval or reliance presented | P, DEL-04-01 | VER-003 |
| PC-18 | Acts (positive) | The person actually marks `R-102` checked; an agent or host records it | Presented with actor = person, recorder distinct, bound content, evidence reference | DEL-04-03, host recording, **actual human act** (DEP-05-02-017) | VER-003 |
| PC-19 | Acts (positive) | Independently evidenced checking act with no preceding proposal acceptance | Presented as that act; no synthetic acceptance prerequisite | DEL-04-03, actual human act (DEP-05-02-017) | VER-003 |
| PC-20 | Lapse | `R-102` content changes after the check in PC-18 | Act shown lapsed, visibly | DEL-04-03, host | VER-003 |
| PC-21 | Checkpoint | Run reaches a declared "mark checked before issue" checkpoint (invented) | Panel shows waiting for that act kind; clears only on the host's record of it | DEL-02-01, DEL-02-03, LOOP | VER-003 |
| PC-22 | Autonomy | Person allows direct application for one low-consequence class; geometry stays proposal-only (V4-EXM-22 shape) | Direct changes show origin and undo; geometry changes go to the queue | P, DEL-04-01 adopted policy, host | VER-003 |
| PC-23 | Policy-dependent | Any operation-specific reserved-act or classifier case | **Held**: `UNRESOLVED{OI-001}` / `UNRESOLVED{OI-002}`; no expected result asserted | Owner decision | VER-003 |

Case accounting states used when results arrive: DEFINED; EXECUTED on an
identified candidate (with configuration and date, V4-EXM-01); LIMITED
(executed with stated gaps); AWAITING INPUT (named input); HELD (policy
decision). Present state: PC-01…PC-22 DEFINED/AWAITING INPUT; PC-23 HELD.

## 8. Concrete questions prepared for the external host owner

These are prepared for App-manager preparation and human relay (SoW CLM-005;
DEP-05-02-018). Writing them here is not delivery, agreement or adoption.
W9 owns the relay file.

1. Which host views show proposed rows with old and new values, and how does
   the panel reference a position in them (H-1, H-2, PC-06)?
2. Where does the host offer and record acceptance, rejection and marking
   checked, and how does its record keep actor and recorder apart (W-2)?
3. How does the host show lapse of a content-bound act (W-3, PC-20)?
4. How does the host present outcome unknown and stale refusal (PC-09,
   PC-10)?
5. Which host workflows exist, and how does the host show a workflow's
   origin and revision (PC-04)?
6. What conversation persistence and panel assembly does the host owner
   intend (OI-013)? The answer is informational for the receiving contract.

## UNRESOLVED

| Item | Owner | Point of need | Effect on this definition |
|---|---|---|---|
| OI-013 panel assembly, host/common construction boundary, conversation persistence | Shared contract owner with SWB implementation owner | Before shared/host implementation boundary contracts | Behaviour only; no layout, assembly or persistence stated |
| OI-014 shared contract/component placement | App/shared contract owners | Before structural/production contract allocation | §6 candidates are unagreed; OUT-004 conditional, no component |
| OI-001 always-reserved acts | Owner with App/SWB contract owners | Before operation-policy production contracts | K-4, W-6; PC-23 held |
| OI-002 classifier routine permissions | Owner with App/SWB contract owners | Before permission-policy implementation | K-4, W-6; PC-23 held |
| OI-021 / PRD OQ-11 first connected activity | Owner via outside SWB session and App/shared owner (OQ-11: App manager, human and external SWBPIPE owner) | Before connected-activity SoW and execution / dependent implementation or live connected examination | Fixture subjects only; no operation selected |
| DEP-001 host panel/view and interaction evidence | SWBPIPE outside implementation session | Before corresponding connected-journey integration/examination and fallback-replacement decision | All PC cases unexecuted |
| DEP-05-02-017 actual human act for positive cases | Person performing the act | When PC-18/PC-19 execute | Positive cases defined, not executable |
| Accepted-but-unapplied proposal whose basis changes | DEL-03-02 owner | V1 | §3.3 unresolved row |
| Missing-tool determination for workflow selection | DEL-02-03 owner; interface not in SoW CLM-002 (F-2) | V1 / next SoW revision decision | PC-05 depends on an unlisted input |
| Active autonomy scope display in the panel | DEL-04-02 owner; interface not in SoW CLM-002 (F-3) | V1 | PC-22 depends on an unlisted input |
| Reconciliation of all consumed meanings (declaration, C, P, acts, records, LOOP) | Respective App-v4 owners | V1 | Names used here are accepted meanings, not supplied versions |

## Verification cases

Designed, not run.

| Case | Procedure | Expected result | Serves |
|---|---|---|---|
| VC-01 | Trace §3.1–3.4 one by one to V4-HOST-04/SOW-019 and to the CLM-002 definitions, host objects/results and responsible participants | All four interactions present; each names consumed definitions, host objects, responsibility and missing inputs (F-2, F-3 visible) | VER-001 |
| VC-02 | Review §2, §4 and PC-06, PC-09, PC-10, PC-12–PC-15 against V4-HI-10–25 and V4-EXM-20/21; on a host candidate, observe proposed-row views, old/new values, reason, basis, receipts and check-without-change | Rules H-1…H-6 each have a positive or rejection case; until a candidate exists, all labeled DESIGNED — UNEXECUTED | VER-002 |
| VC-03 | Review §5, §3.4 and PC-07, PC-08, PC-11, PC-16–PC-23 against V4-HI-25/30–33/40–42/70–71, d3, V4-AUT-01–05, using the DEL-04-01 and DEL-04-03 versions at V1 | "Accept" wording; actor/recorder distinct; lapse visible; no cross-act inference; positive cases wait for an actual act; policy cases held | VER-003 |
| VC-04 | Compare §6 with D anticipated artifacts, the Clarification, V4-ARC-20 and OI-013/014 | Each candidate names consumers and repeated responsibility or "not established"; none recorded as agreed; host construction external | VER-004 |
| VC-05 | Account for PC-01…PC-23: consumed-definition identity, candidate binding, state | Every case in one accounting state; no missing input counted as a pass | VER-005 |
| VC-06 | Inspect OUT-004 state | Recorded as conditional with no component, owner allocation open at OI-013/OI-014 | VER-006 |
| VC-07 | Review every excluded act in SoW REQ-006 one for one against §3 "Responsible" rows, §6 and §8 | Each act kept with its owner; no host construction, policy decision or human act performed or claimed here | VER-007 |

## Findings for V1 (not scope changes)

- F-1. The same executor drafted both DEL-05-01/LOOP-v0.1 and this file.
  The reciprocal M1 join (CASE-002 F-020/F-023) therefore needs an
  independent comparison at V1.
- F-2. V4-WF-04 missing-tool determination (DEL-02-03 behaviour) is needed
  for the workflow-selection interaction. DEL-02-03 is not among this SoW's
  CLM-002 consumed definitions or its Dependencies.csv rows.
- F-3. Visible active autonomy scope (V4-HI-40; DEL-04-02) bears on the
  proposal queue and PC-22. DEL-04-02 is not among this SoW's CLM-002
  definitions.
- F-4. The SoW cites PRD OQ-11 for the first connected activity, while the
  decomposition's open-issue register carries it as OI-021 with a
  differently worded owner. Both are recorded above. Same matter, two
  identifiers.
