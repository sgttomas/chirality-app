# Minimal-loop and model receiving contract
- Contribution: DEL-05-01/LOOP-v0.2
- Status: DRAFT DEFINITION — proposed, unsupplied, not implemented, not accepted
- Serves: OUT-001, OUT-002, OUT-003, OUT-004; REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, REQ-006, REQ-007; AC-001–AC-009; VER-001–VER-009 (all of DEL-05-01)
- Basis: repo 6e18505e3; ScopeOfWork.md sha256 6fbbb580bdacb7f34b4df98a826519a28c087aff6e589ad27330ee556a83b568; P/docs/PRD.md §2.2 V4-HOST-01/02/03/04, §4.1 V4-WF-03/05, §4.5 V4-AUT-01/03/04/05, §4.7 V4-REC-03/04/05, §6, §9 OQ-02/OQ-11; P/docs/ARCHITECTURE.md §3 (V4-ARC-01/04), §4 (V4-ARC-10–14 and host-agent properties), §5 V4-ARC-20, §6; P/docs/HOST_INTEGRATION.md §1, V4-HI-02/04, V4-HI-10–12, V4-HI-20–25, V4-HI-30–33, V4-HI-40–42, §8.1 closing paragraph, V4-HI-70/71; P/docs/EXAMINATION.md V4-EXM-01–03, V4-EXM-20–23; DECISION_BRIEF.html (sha256 02d38cb1…4c420e8) d2, d3, d5; APP-V4-CLARIFICATION-20260927/DIRECTION.md; SCC-CASE-002 Case_Datasheet M1/M4 rows; Open_Issues OI-003/013/014/021; External_Dependencies DEP-001; run folder OWNER_DECISIONS.md (sha256 f3f8e5f3…cf81f2e; decision `APP-V4-FIRST-INCREMENT-20260928-DECISION-1`, D2 and D3), R1_RESOLUTIONS.md (sha256 2f9c7e72…e177ec4), comparisons/V1-A.md (sha256 01811533…e04c09), comparisons/V1-C.md (sha256 8d46258a…4a94a6)
- Consumed inputs:
  - Prior version: DEL-05-01/LOOP-v0.1 (sha256 fd80420c…46bc55c4).
  - Supplier elements taken from R1_RESOLUTIONS, and from quotes in V1-A/V1-C, **not** read from the supplier files; all to be confirmed at IR1:
    - DEL-04-01 act names A1–A14, class values and adopted D2/D3 records (R-1, R-2);
    - treatment → outcome map (R-3);
    - DEL-02-01 checkpoint reached-when, subject binding and dispositions (R-5);
    - DEL-03-02/P §9 and DEL-03-01/C §4.1 outcomes (R-7);
    - DEL-04-02 grant display states and scope (R-8);
    - workflow identity tuple, generation/revision, per-surface exposure and fixture FX-PIPE-01 (R-9).
  - Supplier versions compared at V1: DEL-02-01/WD-v0.1, DEL-03-01/C-v0.1, DEL-03-02/P-v0.1, DEL-04-01/ACT-POLICY-v0.1, DEL-01-01/HOSTING-BOUNDARY-v0.1.
  - DEL-05-02/PANEL-v0.2: co-drafted by the same executor; compared independently at V1 (J5).
  - DEP-05-01-024 model-interface/protocol basis: UNKNOWN supplier, not supplied.
  - DEP-001 host evidence: not received.
- Receivers: DEL-02-01 (OUT-001, OUT-003; REQ-002, REQ-005; VER-005) and DEL-05-02 (OUT-001, OUT-003; REQ-001, REQ-005; VER-001, VER-005) per CASE-002 M1/M4; DEL-02-03 (hold machine confirmation, W7); external SWBPIPE owner via App-manager preparation and human file relay (CASE-002 M4; DEP-05-01-021); DEL-05-01 itself for OUT-003/VER-001–009 when host evidence arrives

## 0. How to read this definition

- **Semantic names only.** Names such as "call correlation identity",
  "argument text", "termination reason", "catalog edition", "entry version",
  "subject content identity" or "grant in force" are semantic element names.
  They are not wire fields, JSON/TS types or message names.
  - This definition selects none of the following: transport, protocol
    version, hash or canonicalization algorithm, persistence technology,
    thread/process placement, shared-component placement (OI-013, OI-014,
    DEL-03-01 TBD-003, DEL-03-02 TBD-002).
- **Standing.**
  - Every statement is a proposed receiving requirement.
  - "Settled" marks a distinction fixed by the accepted basis or by owner
    decision `APP-V4-FIRST-INCREMENT-20260928-DECISION-1`, with citation.
  - "Per R1_RESOLUTIONS R-n; to be confirmed at IR1" marks an integration
    ruling or a supplier v0.2 element that this file adopts without having
    read the supplier's v0.2 text.
  - `UNRESOLVED{…}` is never a permission, a default or a pass.
- **Act names.** This file uses DEL-04-01's canonical act names and IDs A1–A14
  (per R1_RESOLUTIONS R-1; to be confirmed at IR1). Unqualified "checked" means
  only A4, and "approval" only A6 (R-4).
- **Fixture subjects.** The shared invented fixture is **FX-PIPE-01**, owned by
  DEL-03-01 §10 (per R1_RESOLUTIONS R-9; to be confirmed at IR1). This executor
  has not read that catalogue.
  - Identifiers used below are provisional labels: runs `R-101`, `R-102`;
    nodes `N-10`…`N-40`; supports `S-1`…; basis generation `g1`; model
    revisions `r12` → `r13`. Each is to be mapped to its FX-PIPE-01 entry at
    IR1.
  - Fixtures that need parse-level, endpoint or responsiveness subjects
    that FX-PIPE-01 may not contain keep local labels, and say so.
  - None of these select the first connected operation
    (`UNRESOLVED{OI-021}`).
- **Who builds what.** This contract states what the App/shared side needs
  from a host loop, and how that will be checked. It does not construct the
  SWBPIPE loop, native layer, parser, persistence or panel. Those belong to the
  external host owner (SoW CLM-001; HI §1; ARCH §4).

## Changes from v0.1

| V1 item | Change made (section) |
|---|---|
| V1-A D-01, D-17, D-18, D-20; R-1 | Canonical act names A1–A14 throughout. The checkpoint act list is closed to A4, A5, A6, A7, A12 (§2.4, §9) |
| V1-A D-02, D-03, D-23; V1-C §6 rows; R-2 | Class values come from DEL-04-01's policy-class record. Model-change operations: *may apply within granted autonomy*, default *propose* (DERIVED). Operations performing A4–A7/A12/A13: *reserved to the person*. OI-002 removed as a class value. Open part narrowed to OI-021 additions, consequence vocabulary and host capture (§2.2, §9, UNRESOLVED) |
| V1-A D-04, D-05, D-08; R-3 | Treatment is resolved on the host route; the loop relays intent. The runtime outcome map is added. Standing at drafting and at resolution are both recorded (§6 V-5, §6.1) |
| V1-A D-10; V1-C D-03 | Negative decisions: A10 for A5, a decline/stop event for A4/A6/A7, and the declared negative path (§2.4 C-5) |
| V1-A D-11, D-21; V1-C D-06; R-5 | Satisfying evidence comes from the capturing surface. A9 alone never satisfies (§2.4 C-2, §9 A-3) |
| V1-A D-12; R-4 | "Examination/findings" label for agent work; "host checks passed: ‹named checks›" (§2.3, §9) |
| V1-A D-24; V1-C D-11, D-12; R-7 | P §9 and C §4.1 adopted unchanged. Accepted/rejected/withdrawn are relayed with actor. Loop-reported *outcome unknown* is a fourth tool-result class. Application error is added (§2.2 TL-2, §2.3) |
| V1-A AB-03; V1-C D-05 | Lapse at any time after performance; re-hold owned by DEL-02-03 (§2.4 C-4) |
| V1-A AB-09 | Operation-specific reserved additions are held on OI-021 (UNRESOLVED) |
| V1-C D-01 (BLOCKING); R-5 | Loop evaluation of the three reached-when kinds, including the never-met case (§2.4.1) |
| V1-C D-02; R-5, R-6 | Subject binding to a run-observable referent and its content identity (§2.4.2) |
| V1-C D-04; R-5 | Disposition vocabulary: waiting · performed · resolved negatively · lapsed · not reached · unknown (§2.4) |
| V1-C D-07; R-5 | An acceptance checkpoint forces *propose* on the host route. The loop carries the constraint with the dispatch (§2.4 C-6; finding G-1) |
| V1-C D-10; R-9 | Workflow identity tuple {kind, origin, source root, name, revision} (+ derived-from) (§2.1) |
| V1-C D-13, D-27 | "Catalog edition" and "entry version". Edition pre-screen is optional and loop-side. Entry-version mismatch is a host error (§6 O-3) |
| V1-C D-14; R-9 | FX-D2 is now revision r12 → r13 within g1. FX-D3 is added for a generation change (§11) |
| V1-C D-15 | How findings reach the panel (§2.3 E-5) |
| V1-C D-16 | Supplied-guidance identity recorded in the run association (§2.1) |
| V1-C D-18 | "Validated call" renamed "schema-conformant call" (§2.2) |
| V1-C D-21 | OI-013 added to the checkpoint-execution and declaration rows (§10.1) |
| V1-C D-22 | App Responses-API statement marked dated and unobserved (§1) |
| V1-C D-26 | Offering carries all C elements 1–8 plus per-surface exposure. Availability is re-evaluated at request (§2.2) |
| V1-C AB-01 | Mixed item-level decisions at an A5 checkpoint: held as UNRESOLVED; the loop relays per-item dispositions |
| V1-C AB-02, AB-03, AB-04; R-7, R-8 | Every dispatch carries origin, seat role meaning and the grant in force (§6.2) |
| V1-C AB-05; R-7 | A retry keeps the proposal identity. A re-draft is a new proposal with lineage (§6.3) |
| V1-C AB-06; R-3, R-9 | Reserved-class and unexposed entries at offering and at call (§2.2 TL-5) |
| V1-C AB-12 | Event gaps closed: V-2 rejection, edition pre-screen, A10/A11 relays, act requested outside checkpoints, run ended (§2.3) |
| V1-C AB-13 | T-OPEN-1 restated against P one-proposal-with-items (§7, UNRESOLVED) |
| V1-C AB-14; D3 | No routine or classifier permission layer in the host loop (§9 A-5) |

## 1. Position: host loop versus the App's Codex path

The host loop and the App's harness are different model interfaces. This or
any consuming contract must not merge them (SoW REQ-002; ARCH §§3, 4, 6;
PRD §6).

| Aspect | Chirality App (not this contract) | Host embedded loop (this contract) |
|---|---|---|
| Agent runtime | Stock Codex App Server, owned by the App process (V4-ARC-01); definition pin 0.158.0 (D4) | Minimal Chirality agent loop in the host (V4-ARC-10) |
| Model interface | Codex's published protocol. Codex speaks to its providers. ARCH §6 records a dated assumption that local providers serve the Responses API Codex requires. It is **unobserved** on an identified candidate (DEL-01-01 HOSTING L-2/P-11 as quoted in V1-C D-22). The W11 observations were not read here | OpenAI-compatible Chat Completions with tool calls (V4-ARC-10) |
| Credentials | Held by Codex (V4-ARC-04) | Held by the host native layer, outside the interface script (V4-ARC-12) |
| Tools and permission | Codex tools. Routine tool permission and sandbox modes are the user's own Codex setting (D3). The host catalog is reachable through an MCP server or CLI when the person enables it (A13; V4-HI-50; DEL-03-03) | Host catalog operations offered as tools (V4-ARC-13). No classifier or routine permission mode (D3); see §9 A-5 |
| Replaceability | Harness pinned and upgraded deliberately (V4-CST-03) | Loop replaceable behind the four-subject boundary in §2 (V4-ARC-14) |

Consequences:

1. A local server that serves both interfaces does not join them. The App's
   provider selection and the host's model selection remain separate settings
   with separate owners.
2. The App's Codex protocol types are not the host loop's types. The host
   loop's detailed representation waits for DEP-05-01-024.
3. PRD §6 excludes a Chirality-owned loop for the App. At v4.0 the minimal
   loop therefore has **host consumers only**. SWBPIPE is the only
   identified host; further hosts are open (OQ-04 / OI-005). §10 uses this.
4. Pi is a possible later replacement behind the §2 boundary. It is not a
   current dependency (V4-ARC-14; ARCH §6).

## 2. The replaceable boundary: four subjects

The boundary is the set of meanings a loop implementation must accept and
produce. A replacement (Pi's libraries, another library or a rewrite)
conforms when it preserves these meanings, whatever its code shape.

### 2.1 Messages and run association

| Semantic element | Meaning | Consumed from |
|---|---|---|
| Conversation identity | The conversation the message belongs to. Stable across interface reloads while the conversation exists | Record meaning: DEL-04-03 (V4-HI-70) |
| Speaker kind | Person; agent; tool result; supplied guidance (workflow, role or host instructions) | This contract. Guidance source: DEL-02-01 |
| Content | Text or structured content of the turn. For the agent: streamed increments plus a completed form | This contract |
| Completion standing | Streaming, complete, truncated, interrupted, cancelled or failed | This contract |
| Workflow identity (run association) | {kind, origin, source root, name, revision} plus derived-from, for the selected workflow (V4-WF-03). The origin class is project, user, bundled or host. An unadapted carried workflow keeps its original origin. A host adaptation is a new identity with host origin and derived-from | DEL-02-01 identity (per R1_RESOLUTIONS R-9; to be confirmed at IR1) |
| Run identity | The workflow run this conversation turn belongs to, if any | DEL-04-03 run record |
| Seat role meaning | The role meaning the single agent seat carries for this run (V4-HOST-05). If it cannot be determined, the record says **unknown** | DEL-02-01 SEAT-1. Mapping: U-09 with DEL-02-01, the SWB owner and DEL-02-04 (V1-C AB-02) |
| Supplied-guidance identity | For each turn: the identity and revision (content identity; method designated, algorithm unselected) of each guidance input actually supplied to the model. This is evidence for DEL-02-01's *supplied* link | This contract, as the host-side supplier (V1-C D-16) |
| Model configuration reference | The model setting in force when the turn was produced (§5). Never contains a key | This contract; DEL-04-03 "model used" |

Loop obligations:

- M-1. Preserve the order and speaker of every message sent to or received
  from the model.
- M-2. Distinguish a completed agent message from a streamed partial one. A
  partial message that ends without completion is truncated, interrupted,
  cancelled or failed, never complete.
- M-3. Conversation content is operational state. A loop or harness
  conversation store is never the authority for a human act (V4-REC-03,
  settled).
- M-4. Conversation persistence, storage and lifetime stay with the host
  owner (`UNRESOLVED{OI-013}`). The boundary requires only that the
  conversation identity can be cited by the run record and the panel.
- M-5. Record supplied guidance as it was **actually supplied** each turn,
  not as it was configured at launch. If a turn's supplied guidance cannot be
  determined, record *unknown*.

### 2.2 Tools

| Semantic element | Meaning | Consumed from |
|---|---|---|
| Catalog edition | Identity of the adopted catalog state from which offerings were made. One semantic name on both sides | DEL-03-01/C (proposed there, F-C6; V1-C D-13/D-27) |
| Tool offering | One catalog entry offered to the model, with all C elements: <ol><li>identity and entry version</li><li>purpose</li><li>input schema</li><li>availability and unavailable reason as evaluated at offering</li><li>effects</li><li>result schema with standing</li><li>errors</li><li>human-act class with its decision basis</li></ol> Plus the entry's exposure on the embedded surface | DEL-03-01/C §3 (V4-HI-02). Exposure: per R1_RESOLUTIONS R-9. Class: DEL-04-01 policy-class record (R-2). All to be confirmed at IR1 |
| Tool call | A request from the model to run one offered operation: call correlation identity; operation reference; argument text; parse state (§7) | This contract. Representation per DEP-05-01-024 |
| Schema-conformant call | A tool call whose argument text parsed completely and conformed to the input schema of the named entry version, bound to the catalog edition and entry version offered. **Not** P's lifecycle state *validated*, which only the host route produces | This contract (§6; V1-C D-18) |
| Tool result | What the loop returns to the model for a call; one of four classes (TL-2) | Host outcomes: DEL-03-02/P §9 and DEL-03-01/C §4.1, adopted unchanged (per R1_RESOLUTIONS R-7; to be confirmed at IR1) |

Class values carried on offerings (per R1_RESOLUTIONS R-2; to be confirmed at IR1):

- **Vocabulary.** The four V4-HI-02 values: *none*; *may apply within granted
  autonomy*; *proposal only*; *reserved to the person*. Each carries its
  decision basis.
- **SWB model-change operations.** *May apply within granted autonomy*,
  marked DERIVED from V4-HI-41 ("the person may widen it"). The accepted
  default setting is *propose*.
- **Operations that perform or record a person's act.** An operation whose
  effect is to perform or record A4–A7, A12 or A13 as the person's act is
  *reserved to the person* (D2, settled for App/shared contracts). An example
  is FX-PIPE-01 OP-C6 "Mark row checked".
- **Still open.**
  - Operation-specific additions: `UNRESOLVED{OI-021}`.
  - Consequence vocabulary: DEL-04-01 with the host policy owner.
  - Host adoption of the list: DEP-001.
  - The host names and enforces its own list (V4-HI-30). D2 does not show
    that SWBPIPE has adopted it.
- There is no OI-002 class value (D3).

Loop obligations:

- TL-1. Offer only entries derived from the adopted catalog and exposed on
  the embedded surface. An operation unavailable to the person is
  unavailable to the agent, with the same reason (V4-HI-04, settled). The
  loop does not invent a tool that has no catalog entry.
  - Availability shown at offering is historical. It is re-evaluated at
    request on the host route (C §7; V1-C D-26).
- TL-2. Every tool result returned to the model states its class. The
  classes are never collapsed into one "error" or "success". The four classes:
  1. **Loop-side failure, not dispatched**: §6 V-1 to V-3, or the optional
     edition pre-screen.
  2. **Host non-success outcome**: unavailable, not permitted, channel not
     enabled, not exposed on this surface, refused on validation (including
     stale), error, application error.
  3. **Host outcome**: success (ran), queued, accepted, rejected, withdrawn,
     applied with receipt.
  4. **Dispatched, outcome not observed**: reported by the loop as *outcome
     unknown*, attributed to the loop as observer, with the last observed
     state (R-7; P §4.1 overlay).
- TL-3. A host outcome keeps its lifecycle meaning. "Success" means the
  operation ran. A submitted proposal reports "queued" until the host records
  acceptance and application (V4-HI-25, settled). The loop never rewrites
  queued as applied, applied as accepted, or refused as rejected. "Rejected"
  is only A10 (R-7).
- TL-4. Reads return the basis they describe and their standing
  (V4-HI-11/12). The basis is workspace identity, generation, model revision,
  and canonical content identity with its method designation. Where the host
  supplies them, reads also carry per-object **subject content identity**
  (R-6). The loop passes basis, standing and subject identities through
  unchanged. A later call cites the basis it relied on.
- TL-5. Reserved-class and unexposed entries (V1-C AB-06; R-3, R-9):
  - The loop does not decide treatment and does not withhold an exposed
    entry on its own reading of its class.
  - An agent call to an entry whose treatment forbids the requested mode
    returns the host's **not permitted**, naming the governing treatment and
    policy record. The call to a reserved entry is recorded as an A8 request
    for the person's act (R-3.4). No act is performed.
  - An entry not exposed on the embedded surface is reported as *not exposed
    on this surface*. That is distinct from *missing* and from *channel not
    enabled*.

### 2.3 Events

Events are the loop's observable account of what happened. The panel
(DEL-05-02) and the run record (DEL-04-03) consume them. Each event states its
**subject**, **actor**, **reporter** (who observed it) and the **evidence** it
rests on. An event is evidence of what the loop observed; it is never itself a
human act.

| Event meaning (semantic) | Subject | Actor / reporter | Evidence it may carry |
|---|---|---|---|
| Turn started / completed / cancelled / failed | Conversation turn | Person (request) or agent / loop | Message references |
| Model stream progress | Agent message | Model / loop | Partial content; standing "streaming" only |
| Model request refused at boundary | Model request | Host native layer | Refused destination or "key absent"; never key content (§5) |
| Model interface failure | Model request | Model server or transport / loop | Termination reason as reported (§7) |
| Tool call received | Tool call | Model / loop | Correlation identity; operation reference; parse state |
| Tool call rejected: unparseable or truncated | Tool call | Loop | Parse state and reason; "not dispatched" |
| Tool call rejected: unknown or unoffered operation | Tool call | Loop | Operation reference; catalog edition; "not dispatched" |
| Tool call rejected: schema | Tool call | Loop | Catalog edition, entry version, schema reason; "not dispatched" |
| Offer out of date (optional edition pre-screen) | Tool call | Loop | Offered edition vs current edition; "not dispatched; re-offer" |
| Tool call dispatched to host | Schema-conformant call | Loop | Dispatch record (§6.2) |
| Host outcome | Operation/proposal | Host | P §9 outcome unchanged: item dispositions, last observed state, evaluated basis on every non-success, both bases on stale refusal, receipt reference and branch on application |
| Outcome not observed | Dispatched call | Loop (as observer) | Last observed state; "outcome unknown" |
| Proposal decision relayed | Proposal / change items | Person (A5 accept, A10 reject) or proposer (A11 withdraw); host records | Host act record reference; item list; change-item content identity per item |
| Examination findings | Agent examination (A3) | Agent | Findings with references to rows/results and the read basis examined; standing "agent findings" (E-5) |
| Checkpoint reached | Declared checkpoint | Loop | Checkpoint reference; reached-when kind; the observed event that met it; bound subject referent (§2.4) |
| Checkpoint disposition changed | Declared checkpoint | Loop | New disposition; evidence reference |
| Act requested (A8), at a checkpoint or elsewhere | Act kind and subject | Agent (request only) | Request text; content it concerns |
| Human act observed | Actual act | Person (actor); capturing surface (host act facility) records it | Capture evidence reference; recording mode; bound content (V4-HI-32) |
| Decline/stop observed | Person's decision not to perform A4/A6/A7 | Person; host records | Host record reference. Not an act of that kind (R-5) |
| Act lapsed | Previously performed act | Host (reports change) | Changed content identity; any time after performance (R-5) |
| Grant change observed | Autonomy grant | Person (A12), host records; or agent request (A8) | Display state per R-8; A12 act evidence if person-set |
| Run ended | Workflow run | Loop | Final state; disposition of every declared checkpoint (including *not reached* and *unknown*); unknown outcomes stay unknown |

Loop obligations:

- E-1. Emit an event only for something the loop actually observed or did.
  An absent observation stays absent and is not filled by inference
  (SoW AC-009).
- E-2. The "human act observed" and "proposal decision relayed" events relay
  host-recorded acts. The loop never originates them from model text, a tool
  success, a queue position or a receipt (V4-HI-25/31, V4-AUT-03, settled).
- E-3. Events carry references to host receipts, hashes and origin marks.
  They never copy them (V4-HI-71, settled).
- E-4. The event set must cover the run record's inventory (V4-HI-70):
  - workflow identity;
  - conversation;
  - autonomy settings (grant change events, plus the grant in force on each
    dispatch);
  - operations requested and their outcomes;
  - receipt references;
  - human acts;
  - model used;
  - supplied guidance.

  The field-level mapping is DEL-04-03's.
- E-5. Findings reach the panel in one of two ways (V1-C D-15):
  - (a) As agent message content, with references to host rows/results and
    the read basis examined, emitted as "examination findings".
  - (b) As a host outcome, if the host offers an operation that holds
    findings.

  Whether host-held findings count as a change operation is
  `UNRESOLVED{C U-C5}` with the host owner. In neither route does an
  examination change domain tables (V4-EXM-21). Findings are never labeled
  "checked" (R-4).

### 2.4 Checkpoints

A checkpoint is a point declared in a workflow at which the run waits for a
specified human act (V4-WF-05, V4-HI-42, settled).

| Semantic element | Meaning | Consumed from |
|---|---|---|
| Declared checkpoint | The workflow's declaration: required act kind; reached-when condition; subject referent class; path on negative decision | DEL-02-01 (per R1_RESOLUTIONS R-5; to be confirmed at IR1) |
| Required act kind | One of A4 mark checked, A5 accept, A6 approve, A7 rely, A12 set grant (closed list). All are reserved to the person (D2) | DEL-04-01 (R-1, R-2) |
| Disposition | waiting · performed · resolved negatively · lapsed · not reached · unknown | Shared vocabulary (R-5). DEL-02-03 owns the hold machine (W7) |
| Satisfying evidence | Attributable act evidence from the **capturing surface**: the host's act facility for acts on host content | R-5; V4-HI-31; DEL-04-03 act record |

#### 2.4.1 Reached-when evaluation by the loop (resolves V1-C D-01)

The loop keeps the set of declared checkpoints for the run. It evaluates each
one's reached-when condition **only against events it has observed** (E-1).
It never evaluates against model text, stage descriptions or the model's
claims.

| Reached-when kind (R-5) | Evaluated when | Loop behaviour on match |
|---|---|---|
| (a) Before dispatch of a named required-tool reference | After a call to that operation passes V-1 to V-3 (§6) and **before** V-4 dispatch | Hold the schema-conformant call undispatched. Return a tool result telling the model the run is held at a checkpoint (loop-side, not a failure of the call). Bind the subject to the held call's targets (§2.4.2). After *performed*, dispatch the **same** held call unchanged. A different call is a new call, and the act does not carry over |
| (b) Observed production of a named declared output | When an observed event establishes the output: a host outcome producing it, or a completed agent message designated by the declaration as that output. A model statement that the output exists does not count | Stop acting on the run. Bind the subject to the output's content identity |
| (c) Observed host outcome of a named operation (e.g. proposal queued) | When the host outcome for that operation matches the named outcome | Stop acting on the run. Bind the subject to the proposal's change items, or to the rows produced, as the outcome identifies them |

When a condition matches, the loop emits "checkpoint reached", sets the
disposition to *waiting* and stops acting on the run (C-1).

**Never met.**

- If the run ends (the model ends its turn sequence, the person cancels, or a
  failure ends the run) without the condition being observed, the
  checkpoint's disposition is **not reached**. It is never *performed* or
  satisfied. "Run ended" reports it.
- If the observation that would decide the condition was lost, the
  disposition is **unknown**, not *not reached*. For example, kind (c) where
  the named operation's outcome is *outcome unknown*.
- A later workflow step that depends on an unreached checkpoint is not
  performed. What the declaration does next is DEL-02-01's and DEL-02-03's.

#### 2.4.2 Subject binding (resolves V1-C D-02)

At match, the loop binds the checkpoint's subject to a run-observable referent
and its content identity (R-5, R-6):

| Referent | Content identity used |
|---|---|
| Proposal change items (kind c, or an A5 checkpoint) | Change-item content identity per item (DEL-03-02; R-6): operation identity and version, bound targets, old/new values, relied-on basis |
| Rows/objects produced or targeted (kinds a and c; acts A4, A6, A7) | Subject content identity per object (DEL-03-01; R-6), with method designation |
| Declared output (kind b) | The output's content identity (host-supplied, or file content identity for App files, R-6) |

A human act satisfies the checkpoint only if its evidence concerns the same
referent and the same content identity. An act on other content, even of the
right kind, does not satisfy it.

#### 2.4.3 Loop obligations

- C-1. At a reached checkpoint the loop stops acting on the run. A checkpoint
  overrides autonomy (V4-HI-42, settled). No grant widens past a reserved act
  or a declared checkpoint (D2).
- C-2. The disposition becomes *performed* only on capturing-surface
  evidence of the **specified** act on the bound subject content. The
  capturing surface is the host's act facility for acts on host content
  (R-5).
  - A faithful record (A9) by another recorder, with actor ≠ recorder, is a
    valid record shape when it cites that capture evidence. On its own it
    never satisfies the checkpoint.
  - The following never satisfy it: model text; tool success; agent
    findings; an A8 request; an agent-authored record alone; an act of a
    different kind.
  - Any further host-specific capture requirement is the host's (DEP-001).
- C-3. The checkpoint requires its own act and nothing more. No general rule
  says acceptance must precede checking, approval or reliance (SoW REQ-007,
  AC-008).
- C-4. **Lapse at any time** (V1-A AB-03; V1-C D-05; R-5).
  - Whenever the host reports that the bound content changed after the act,
    the loop emits "act lapsed" and sets the disposition to *lapsed*.
  - Before the run has resumed, a lapsed act no longer satisfies the
    checkpoint. The loop waits for a new act on the current content.
  - After resume, the loop records and relays the lapse. Whether the run
    re-holds is DEL-02-03's hold machine; the loop does not re-open a run on
    its own.
  - For A5, applying the accepted item does not lapse the acceptance. A basis
    failure between acceptance and application follows the stale rule
    (R-6; P U-P3). It is not a lapse.
- C-5. **Negative decisions** (V1-A D-10; V1-C D-03; R-5):
  - For A5, the negative is A10 reject. The disposition becomes *resolved
    negatively*.
  - For A4, A6 and A7, the person's decision not to act is a recorded
    decline/stop event. It is not an act of that kind and does not satisfy
    the checkpoint. The disposition becomes *resolved negatively*.
  - The loop then follows the declaration's "on negative decision" path. If
    none is declared, the run stops.
- C-6. **Acceptance checkpoint forces proposal** (DERIVED from V4-HI-42 and
  D2b; R-5).
  - Where a declared checkpoint requires A5 on an operation's result, that
    operation's treatment is *propose* whatever the grant.
  - Treatment is resolved on the host route (R-3). So the loop carries the
    constraint "declared checkpoint requires A5 on this result" in the
    dispatch record (§6.2), and the host route resolves treatment.
  - An agent request to apply directly in that case returns **not
    permitted**. The loop never converts it into a proposal (R-3.3).
  - See finding G-1.
- C-7. **Mixed item decisions.** At an A5 checkpoint where some items are
  accepted, some rejected and some still queued, the loop relays per-item
  dispositions. Whether the checkpoint then counts as performed, resolved
  negatively or waiting is `UNRESOLVED{V1-C AB-01}` (DEL-02-01 with DEL-02-03
  and DEL-03-02). The loop does not decide it.

## 3. Operating sequence (one turn)

This is a semantic sequence. The placement of each step (interface thread,
worker, native layer) is owner-selected (`UNRESOLVED{OI-013}`).

```text
person message ─► loop composes request (messages + offerings from catalog edition K, + supplied guidance, identity recorded)
   ─► native layer checks destination; attaches key if cloud (§5) ─► model server
   ◄─ streamed content and/or tool calls, then a termination reason
for each tool call:
   V-1 parse completeness (§7) ── fail ─► loop-side failure; not dispatched
   V-2 operation offered in K and exposed ── no ─► loop-side failure; not dispatched
   V-3 input schema of offered entry version ── fail ─► loop-side failure; not dispatched
   [reached-when kind (a) matches?] ─► hold call; checkpoint waiting (§2.4.1)
   dispatch with dispatch record (§6.2) ─► host route: V-4 validation, V-5 treatment + application/proposal
   ◄─ host outcome (P §9) or no observation ─► tool result class 2/3/4 (TL-2)
   [reached-when kinds (b)/(c) match?] ─► checkpoint waiting (§2.4.1)
loop repeats until the model ends, the person cancels, or a failure ends the turn;
run end reports every checkpoint disposition (not reached / unknown included)
```

## 4. Minimal Chat Completions capability

The receiving contract needs the capabilities below from the model interface,
stated semantically. The supplier, protocol version and payload details are
`UNRESOLVED{DEP-05-01-024}`.

| Capability | Why needed | Settled or open |
|---|---|---|
| Submit an ordered conversation and a set of tool offerings | Messages and tools subjects | Settled need (V4-ARC-10) |
| Receive assistant content incrementally | Responsiveness (§8) and panel conversation | Settled need (ARCH §4 streaming) |
| Receive tool calls with correlation identity, operation name and argument text, possibly in fragments | Tools subject; §7 assembly | Settled need. Fragment representation open (DEP-05-01-024) |
| Receive a termination reason that distinguishes complete, length-truncated and error | §7 truncation detection | Need settled; representation open (DEP-05-01-024) |
| Return a tool result for a correlation identity, including a "held at checkpoint" result | Tools subject; §2.4.1 (a) | Settled need |
| Several tool calls in one response: whether supported and how | §7 MC-8 | `UNRESOLVED{DEP-05-01-024}` |

No provider, server product, model or version is selected. The ARCH §6 list
(oMLX, LM Studio, Ollama) is a dated assumption. A candidate server needs the
selected interface/tool-call qualification.

## 5. Model selection, destination and key boundary

### 5.1 Settings (semantic)

| Model setting state | Meaning |
|---|---|
| Local (default) | A user-controlled local model server is configured. This is the default (V4-HOST-01) |
| Cloud chosen, key supplied | The person chose a cloud model and supplied an API key (V4-HOST-01) |
| Cloud chosen, key absent | Chosen, but no key supplied. No request may be made |
| Unconfigured | No usable model server. No request may be made. There is no silent cloud fallback |

Settled rules:

- N-1. Local is the default. Cloud is used only on the **person's** choice
  **and** a supplied key (V4-HOST-01, V4-ARC-11).
- N-2. In local operation, no agent data goes to any destination other than
  the configured model server (V4-HOST-02).
- N-3. The loop's requests pass through the host's native layer. The native
  layer enforces the configured endpoint and holds any key outside the
  interface script (V4-ARC-12).

Derived receiving requirements (proposed):

- N-4. Model and endpoint settings change only by the person's act through
  the host. Model output, tool arguments and workflow text cannot change
  them.
- N-5. A failed or unreachable local server is reported. It is never answered
  by switching to a cloud model.
- N-6. The key never appears in interface-script memory, messages, events,
  run records, panel content or error text. Events say only "key present" or
  "key absent".
- N-7. The native layer is the **enforcement point**. Interface-script
  checks are not evidence of enforcement (SoW AC-002).

Open matters:

- `UNRESOLVED{N-OPEN-1}`: which endpoints count as a "user-controlled local
  model server". Same machine only, or a user-controlled machine on a local
  network?
- `UNRESOLVED{N-OPEN-2}`: the permitted destination set in cloud-chosen
  operation. The proposed reading is "only the chosen cloud endpoint".
- `UNRESOLVED{N-OPEN-3}`: traffic caused by tools rather than the loop, such
  as a later Domains query tool. HI §8.1 says the Domains direction does not
  relax V4-HOST-02. It is not covered here, and it is not a permission.

### 5.2 Case matrix (OUT-002 fixtures / OUT-003 conformance)

| Case | Setting / stimulus | Expected receiving result | Evidence needed for a host claim |
|---|---|---|---|
| MS-01 | Local default; person asks for a model-table read | Requests go only to the configured local server | Observed destinations with configuration (V4-EXM-01, V4-EXM-23) |
| MS-02 | Unconfigured | No model request; person told no model is configured; no cloud fallback | Observed absence of requests |
| MS-03 | Person chooses cloud and supplies key | Requests go to the chosen endpoint through the native layer; key never visible to script | Native-layer trace; script-side inspection |
| MS-04 | Cloud chosen, key absent | No request; failure reported | Observed absence of requests |
| MS-05 | Model output or tool argument asks the loop to use another endpoint | Refused (N-4); setting unchanged; event recorded | Setting before/after; event |
| MS-06 | Local operation; loop or library attempts a request to another destination (local label: a hard-coded telemetry URL in a test double) | Refused by the native layer; reported; no data sent | Native-layer refusal plus network capture |
| MS-07 | Interface script attempts to read the key | Key not available to the script | Script-side inspection |
| MS-08 | Cloud request fails with an authentication error | Error reported without key content | Error text, event and record inspection |
| MS-09 | Local server unreachable | Failure reported; no cloud switch | Observed destinations; event |
| MS-10 | Person switches cloud → local mid-conversation | Later requests go only to the local server; change attributed to the person | Destinations before/after; setting-change record |
| MS-11 | Endpoint on another machine configured as "local" | `UNRESOLVED{N-OPEN-1}`: held | — |

## 6. Validation order, treatment and dispatch

Settled:

- Tool arguments are checked against the adopted catalog schemas before the
  host's own validation runs (V4-ARC-13; SOW-139).
- Every change then passes through the host's one validation and application
  route (V4-HI-20).
- Treatment (direct, propose, not permitted) is resolved **on the host route**
  at validation and again at application. The loop relays the actor's intent
  and does not decide treatment (per R1_RESOLUTIONS R-3; to be confirmed at
  IR1).

| Step | Check | Performed by | On failure |
|---|---|---|---|
| V-1 | Parse completeness (§7) | Loop | Loop-side failure "malformed/truncated"; not dispatched |
| V-2 | Operation resolution: named operation offered from edition K and exposed on the embedded surface | Loop | Loop-side failure "unknown or unoffered operation"; not dispatched |
| V-3 | Input schema of the offered entry version | Loop | Loop-side failure "schema", with reason; not dispatched |
| V-4 | Host validation: availability re-evaluated at request, preconditions, basis currency, entry version, domain rules | Host route | Host non-success outcome: unavailable; refused (e.g. invalid, stale with both bases); error, including entry-version mismatch per C element 7 / U-C6 |
| V-5 | Treatment resolution and application or proposal | Host route | Not permitted, naming treatment and policy record; application error (effect none/partial/unknown); or host outcome |

### 6.1 Receiving requirements

- O-1. V-3 always runs before V-4. A call that fails V-1 to V-3 never reaches
  V-4.
- O-2. Passing V-3 is not host validation, not application and not a human
  act (SoW REQ-003, CLM-004). A schema-conformant call can still be refused at
  V-4 or not permitted at V-5.
- O-3. **Edition and entry version** (V1-C D-13/D-27).
  - The dispatch carries the catalog edition and entry version offered.
  - The loop *may* pre-screen for an edition change before dispatch. If it
    finds one, it reports a loop-side "offer out of date; re-offer".
  - Entry-version mismatch detected by the host is a host error, per C
    element 7. The exact rule is U-C6, a host input.
- O-4. The treatment → outcome map is adopted unchanged (per R1_RESOLUTIONS
  R-3; to be confirmed at IR1):
  - Apply directly without an effective *direct* treatment → **not
    permitted**. It is never silently converted into a proposal.
  - A call that would perform the person's reserved act → **not permitted**,
    plus an A8 request.
  - A class with no policy basis → direct not permitted, propose available
    (V4-HI-41).
  - Widening a grant never converts a queued proposal into direct
    application.
- O-5. The loop records, or relays for the record, the standing **at
  drafting** (the grant in force carried on dispatch) and the host-reported
  treatment **at resolution** (validation and application) whenever they
  differ (R-3.6; R-8).
  - An in-flight grant narrowing leaves an already-queued proposal
    unaffected.
  - An operation not yet applied is re-resolved at application by the host
    (DEL-04-01 policy plus host enforcement; DEP-001).
- O-6. The direct branch applies only when the grant display state is
  **effective** and direct (R-8). *Requested by agent*, *set by person, not yet
  confirmed by control*, *unconfirmed*, *not set* and *refused* never support
  direct application. The host route decides; the loop carries the state.

### 6.2 Dispatch record (every dispatch)

Per V1-C AB-02/03/04 and R1_RESOLUTIONS R-7/R-8 (to be confirmed at IR1), every
dispatched call carries:

| Element | Meaning |
|---|---|
| Origin | Author type (agent); author identity (the seat); channel (embedded); conversation identity; run identity; workflow identity tuple (§2.1) (V4-HI-21; P §3.3) |
| Seat role meaning | As in §2.1, or *unknown* |
| Grant in force | Reference to the autonomy settings at drafting, with display state and scope (R-8), as the loop last observed them |
| Requested mode | Apply directly or propose, as expressed by the call or the operation's catalog meaning. Representation per DEL-03-01/03-02 |
| Checkpoint constraint | Present if a declared checkpoint requires A5 on this operation's result (C-6) |
| Relied-on basis | The basis the call cites, with method designations (TL-4) |
| Catalog edition and entry version offered | O-3 |
| Proposal identity | For a resubmission, the existing proposal identity (§6.3); otherwise assigned per DEL-03-02 |
| Correlation identity | The model's call correlation identity |

### 6.3 Retry, resubmission and re-draft (V1-C AB-05)

- R-a. **Retry keeps proposal identity** (R-7). A resubmission of the same
  proposal carries the same proposal identity. This holds whether the loop
  re-dispatches after a transport failure, or the agent resubmits by citing
  the proposal identity. The loop never mints a new identity for a
  resubmission.
  - "One effect per proposal identity" is a host obligation to be evidenced
    (DEP-001). It is not recorded as fact.
  - Each submission is recorded separately, with only the effects actually
    observed.
- R-b. **After outcome unknown**, the loop first seeks observation of the
  outcome (for example, a read of the proposal's state) before any
  resubmission. The mechanism is DEL-03-02 TBD-002 / U-P1.
- R-c. **A re-draft is a new proposal.** After a stale refusal, a re-draft is a
  new proposal with lineage to the refused one. It must rest on a fresh read of
  the current basis. It is not a retry, and it is never a retarget (V4-HI-23).

## 7. Malformed and truncated tool calls

Settled: truncated or malformed tool calls are reported failures. They are
never executed as empty arguments (ARCH §4; SOW-142).

| ID | Condition (semantic) | Expected handling |
|---|---|---|
| MC-1 | Termination reason says length truncation while a call's argument text is incomplete | Failure "truncated"; not dispatched; three reports |
| MC-2 | Stream interrupted during argument text | Failure "interrupted"; not dispatched |
| MC-3 | Argument text complete but not parseable as a structured value | Failure "malformed"; not dispatched |
| MC-4 | Parses, but is not the structured form an argument set requires | Failure "malformed"; not dispatched |
| MC-5 | Operation reference missing, empty, not offered or not exposed | Failure at V-2; not dispatched |
| MC-6 | Argument text absent or empty | Never coerced to an empty argument set. Treated as malformed until DEP-05-01-024 says how an explicit "no arguments" is expressed (`UNRESOLVED{DEP-05-01-024}`) |
| MC-7 | Two calls in one response share a correlation identity | Failure for both; not dispatched (proposed) |
| MC-8 | Several calls in one response, one malformed | The malformed call is not dispatched. Whether valid siblings run is `UNRESOLVED{T-OPEN-1}`. Proposed: each sibling runs on its own validation and is a separate operation or proposal. The loop never merges sibling calls into one proposal with items. Items come only from one call's arguments per DEL-03-02 (V1-C AB-13) |
| MC-9 | Loop "repairs" incomplete text (closes brackets, fills defaults) | Prohibited. The model may issue a new call, which is a new call with its own identity |

Failure reporting has three distinct recipients:

1. **The model** receives a class-1 tool result (TL-2) with the reason.
2. **The event stream / panel** receives "tool call rejected" with parse
   state and "not dispatched".
3. **The run record** records the operation as requested with outcome "not
   executed: rejected before host validation" (DEL-04-03).

**Dispatch observation.** For each rejected case, the receiving check is that
the host route received no call for that correlation identity. A valid
comparison call (FX-V1) shows that dispatch does happen for legitimate input
(SoW AC-005).

## 8. Responsiveness: observation protocol (no numeric thresholds)

Settled: the loop does not block the host's interface. Long parsing and model
streaming run off the interface's main thread where the host needs it
(ARCH §4). Placement is the host owner's choice (`UNRESOLVED{OI-013}`). This
contract sets **no** latency or frame-time threshold (SoW REQ-004, AC-006).
Any quantitative criterion needs an owner decision (`UNRESOLVED{R-OPEN-1}`).

| ID | Load | Concurrent person interaction to attempt |
|---|---|---|
| RS-1 | Long model stream (local label: a long explanatory answer) | Scroll and select rows in a host table; open another host view; type in a host field |
| RS-2 | Tool call with large argument text and a large read result (local label: all nodes of a large invented model; FX-PIPE-01 may be too small, which is why it diverges) | Same interactions, during parse and result handling |
| RS-3 | Stream in progress | Cancel the turn. Cancel takes effect and the interface stays usable |
| RS-4 | Stream in progress while the host runs its own work (e.g. a host recalculation) | Interact with host views that do not depend on that work |

Each observation records:

- candidate identity (host build, loop implementation and version);
- configuration (model server, model, local or cloud) and date (V4-EXM-01);
- environment (machine, OS, webview engine);
- the host owner's placement and parsing choice, as reported;
- each interaction attempted, with the observer's account: usable; usable
  with described degradation; blocked; not observed;
- any host-produced measurement, as observed, with no threshold applied;
- limitations.

Verdict language: "continued usability observed for scenarios X on candidate
Y". A document review or a fixture run never supports "responsive" for an
actual host.

## 9. Distinct acts at the loop boundary

Settled distinctions: V4-HI-25/30–33, V4-AUT-03/05, V4-WF-05, d3. Canonical
names per R1_RESOLUTIONS R-1, to be confirmed at IR1.

| Act / subject | Actor | What the loop may emit | Never emitted or inferred |
|---|---|---|---|
| A1 propose | Agent (or person) | Dispatch; host outcome "queued" | Acceptance |
| A2 apply (direct under grant) | Agent within an effective grant; host applies | Host outcome "applied", branch *direct under grant*, receipt, origin, undo route, later-examination route | Acceptance, checking, approval |
| A2 apply (after acceptance) | Host | Host outcome "applied", branch *after acceptance*, receipt | Approval |
| A3 examine | Agent | "Examination findings" (E-5) | "Checked" |
| A4 mark checked | Person (reserved, D2a); capturing surface records | Relayed "human act observed" | Creation by the agent; inference from findings |
| A5 accept | Person (reserved where autonomy requires a proposal, D2b); per change item | Relayed "proposal decision relayed" | Inference from success, queueing or receipt |
| A6 approve | Person (reserved, D2c) | Relayed act only | Any agent statement of approval, certification or compliance (V4-AUT-05) |
| A7 rely | Person (reserved, D2d) | Relayed act only | Reliance inferred from any other act |
| A8 request | Agent | "Act requested" | Performance of the act |
| A9 record | Any identified recorder, actor ≠ recorder | Recording mode (direct capture / faithful recording) carried on relayed acts | Satisfaction of a checkpoint by itself |
| A10 reject | Person wherever A5 is reserved | Relayed with actor | "Rejected" for a host refusal |
| A11 withdraw | Proposer | Relayed with actor | — |
| A12 set grant | Person (reserved, D2e) | "Grant change observed" with A12 evidence | A grant change from an agent request (A8) |
| A13 enable external access | Person (reserved, D2e) | Not a loop event (external channel) | — |
| A14 answer tool permission | Not applicable in the host loop (§9 A-5) | — | — |

- A-1. Evidence of one act never establishes another (SoW CLM-004).
- A-2. An agent may request an act (A8) and prepare the person's decision. It
  never records the act as performed (V4-HI-31).
- A-3. A relayed act carries its actor (the person), its recorder, the
  recording mode and the capture evidence reference. Only capture evidence
  from the capturing surface satisfies a checkpoint (C-2).
- A-4. Reserved acts per D2 are settled for App/shared contracts. Still open:
  - operation-specific additions, `UNRESOLVED{OI-021}`;
  - host adoption and enforcement of its own list, DEP-001.
- A-5. **No routine or classifier permission layer in the host loop** (D3,
  settled; V1-C AB-14).
  - Host operation authority is the person's autonomy grant plus the adopted
    policy, resolved on the host route. For SWB model changes the default
    setting is *propose* (V4-HI-41).
  - The loop presents no tool-permission prompts, and nothing in the loop
    stands in for a reserved or professional act.
  - A14 concerns the App's Codex only.

## 10. Owner-allocation and open-choice account (OUT-004)

### 10.1 Responsibility map

| Responsibility | App/shared (this DEL-05-01) | Other App-v4 owner | External host owner (SWBPIPE) | Open issue / point of need | Current standing |
|---|---|---|---|---|---|
| Loop receiving requirements, fixtures, conformance cases | Owns (OUT-001–003) | — | Receives through relay | — | This v0.2 draft |
| Loop construction | Excluded | — | Owns | OI-013, before shared/host implementation boundary contracts | Owner-reported building (DEP-001) |
| Loop placement | Excluded; requires §8 outcome only | — | Selects | OI-013 | Open |
| Streaming and tool-call parsing implementation | Excluded; requires §7 outcomes only | — | Owns | OI-013 | Open |
| Conversation persistence | Excluded; requires a citable identity (M-4) | Record reference: DEL-04-03 | Owns | OI-013 | Open |
| Panel assembly | Excluded | Panel receiving: DEL-05-02 | Owns | OI-013 | Open |
| Native networking, endpoint enforcement, key custody | Excluded; defines §5 cases | — | Owns | N-OPEN-1/2, before conformance cases | Not received |
| Treatment resolution (validation, application) | Excluded; relays intent (§6) | Policy: DEL-04-01 | Host route enforces | DEP-001 | Not received |
| Catalog schemas, read basis, exposure | Consumes | DEL-03-01 | Implements host catalog | DEL-03-01 TBD-003 | v0.2 elements per R-6/R-9; IR1 |
| Proposal/validation/outcome meaning | Consumes | DEL-03-02 | Implements route/receipts | DEL-03-02 TBD-002 | P §9 per R-7; IR1 |
| Workflow/role/checkpoint declarations | Consumes | DEL-02-01 | Host workflows (V4-HOST-06) | OI-014; OI-013 (host side) | Reached-when/subject/dispositions per R-5; IR1 |
| Checkpoint execution/hold machine | Evaluates reached-when in hosts (§2.4.1) | DEL-02-03 (W7) | Host execution | OI-013 | Pending W7 |
| Operation-policy and act distinctions | Consumes | DEL-04-01 (carries adopted D2/D3) | Enforces its own list; offers/records acts | OI-021 additions; consequence vocabulary | D2/D3 adopted; IR1 |
| Autonomy grant display states and scope | Carries on dispatch | DEL-04-02 (R-8) | Controls and enforcement | No register row (V1-C RF-5; C1) | Per R-8; IR1 |
| Record format and act records | Consumes | DEL-04-03 | Supplies receipts, actual acts | — | IR1 |
| Model-interface / protocol fixture basis | Receives or agrees at fixture use | — | Possibly (unknown) | DEP-05-01-024, supplier UNKNOWN | Not supplied |
| Actual host evidence | Receives; audits (VER-009) | Joined witness: DEL-09-06 | Supplies | DEP-001 | Not received |
| Common (shared) loop implementation | Not allocated | OI-014 owners | — | OI-014 / OI-013 | No agreed repeated responsibility |
| Human acts | None | — | Offers, records, presents | — | Performed by the person only |

### 10.2 Common-implementation assessment

A common implementation needs a concrete, agreed, repeated responsibility
(Clarification; V4-ARC-20; d2).

- The App runs no Chirality loop (PRD §6). The minimal loop has one
  identified consumer, SWBPIPE. Additional hosts are open (OI-005).
- Candidate repeated parts, for later OI-014 consideration only:
  - (a) the parse-completeness check;
  - (b) catalog-schema argument checking. The external adapter (DEL-03-03)
    might also need it; that has not been compared.
- Assessment: **no repeated responsibility is established, and no common loop
  implementation is proposed.** Candidate (b) remains a question for
  DEL-03-01/DEL-03-03 (V1-C D-28 notes that C holds it as a question).

### 10.3 Required inputs and their standing

| Input | Supplier | Needed for | Standing at v0.2 |
|---|---|---|---|
| Catalog entry elements 1–8, edition, exposure, read basis, subject content identity, method designation | DEL-03-01/C | §2.2, §6, fixtures | C-v0.1 compared at V1; v0.2 elements per R-6/R-9; confirm at IR1 |
| Outcome taxonomy, change-item content identity, proposal identity, lineage | DEL-03-02/P | TL-2, §2.3, §6, §6.3, C-4 | P-v0.1 compared; P §9 per R-7; confirm at IR1 |
| Checkpoint reached-when, subject referent, negative path, identity tuple | DEL-02-01 | §2.1, §2.4 | WD-v0.1 compared; per R-5/R-9; confirm at IR1 |
| Hold machine | DEL-02-03 | §2.4 C-4, C-7 | Not drafted (W7) |
| Act names, class values, adopted D2/D3, treatment map | DEL-04-01 | §2.2, §6, §9 | ACT-POLICY-v0.1 compared; per R-1/R-2/R-3; confirm at IR1 |
| Grant display states and scope | DEL-04-02 | §6.2, O-6 | Per R-8; no register row (C1) |
| Record inventory, act record, recording mode | DEL-04-03 | §2.1, §2.3, §7 | Per R-6/R-8; confirm at IR1 |
| Panel receiving needs | DEL-05-02 | §2.3, §7 | PANEL-v0.2, same executor; V1 J5 compared v0.1 |
| Model-interface identity and representation | UNKNOWN (DEP-05-01-024) | §4, MC-6, MC-8, executable fixtures | Not supplied |
| Host candidate and observations | SWBPIPE (DEP-001) | VER-001/002/004/005/006/009 host claims | Not received; owner-reported building |

## 11. Fixture inventory (OUT-002, designed)

Every fixture names its **catalog basis** (a DEL-03-01/C version, and
FX-PIPE-01 entries) and its **model-interface basis** (DEP-05-01-024, currently
UNKNOWN). Until both are supplied, fixtures are case designs. They are not
executable and carry no field names. Subjects are provisional labels, to be
mapped to FX-PIPE-01 at IR1 (§0).

| Fixture | Subject | Input | Expected result | Serves |
|---|---|---|---|---|
| FX-V1 | Read run `R-101` supports | Complete, schema-conformant call | Dispatched with dispatch record (§6.2); host read with basis, standing and subject content identities | VER-004, VER-005 comparison |
| FX-V2 | Propose support `S-7` at node `N-30` on `R-101`; grant effective, setting *propose* | Schema-conformant call | Dispatched; host outcome "queued"; no acceptance event | VER-004, VER-008 |
| FX-V3 | Same, requested mode *apply directly*; grant display state *requested by agent* | Schema-conformant call | Host **not permitted** (O-6); not converted to a proposal | VER-004, VER-008 |
| FX-S1 | Node given as a number where the schema requires a node reference | Schema-invalid | Rejected at V-3; not dispatched | VER-004 |
| FX-S2 | Required argument missing | Schema-invalid | Rejected at V-3 | VER-004 |
| FX-D1 | Support at node `N-99`, not on `R-101` | Schema-conformant, domain-invalid | Passes V-3. Host **refused** at V-4 with reason and evaluated basis | VER-004 |
| FX-D2 | Proposal citing basis g1/r12, after an intervening edit made model revision r13 within g1 | Schema-conformant, stale | Host refuses as stale, reporting both bases. A re-draft is a new proposal with lineage (§6.3 R-c) | VER-004 |
| FX-D3 | Proposal citing g1/r12 after a host restore started generation g2 | Lineage change | Host refusal reporting both bases (meaning per DEL-03-01/03-02 at IR1) | VER-004 |
| FX-U1 | Operation not in the catalog | Unknown operation | Rejected at V-2 | VER-005 |
| FX-U2 | Operation unavailable to the person ("select a load case first") | Unavailable | Host **unavailable**, same reason the person sees (V4-HI-04) | VER-004 |
| FX-U3 | Entry not exposed on the embedded surface | Not exposed | Rejected at V-2 / reported *not exposed on this surface*, distinct from missing | VER-004 |
| FX-R1 | Agent calls OP-C6 "Mark row checked" on `R-102` (reserved to the person) | Reserved entry | Host **not permitted**, naming treatment and policy record; A8 request event; no A4 | VER-008 |
| FX-O1 | Dispatch of FX-V2; connection lost before any host reply | Unobserved outcome | Tool result class 4, *outcome unknown*, reporter = loop, last observed state "dispatched". A resubmission keeps the same proposal identity after an observation attempt (§6.3) | VER-005, VER-009 |
| FX-M1…M9 | Cases MC-1…MC-9 (local labels; parse-level) | Malformed/truncated | As §7; not dispatched; three reports | VER-005 |
| FX-N1…N11 | Cases MS-01…MS-11 (local labels; endpoint-level) | Settings/destinations | As §5.2 | VER-001, VER-002 |
| FX-C1 | Checkpoint requiring A4 on rows produced, reached-when (c) "after proposal applied" (invented) | Kind (c) match | Waiting; subject bound to rows' subject content identities; performed only on host-captured A4 on those rows | VER-008 |
| FX-C2 | Same checkpoint; model text says "the engineer has checked this" | Model assertion | Still waiting; no act event | VER-008 |
| FX-C3 | A4 performed on `N-30`, then `N-30` edited (before resume, then variant after resume) | Content change | *Lapsed*. Before resume: waits for a new act. After resume: lapse relayed; re-hold per DEL-02-03 | VER-008 |
| FX-C4 | Independently evidenced A4, no preceding A5 | Independent act | Performed; no synthetic acceptance prerequisite | VER-008 |
| FX-C5 | Checkpoint requiring A5 on proposal items; person rejects (A10) | Negative decision | *Resolved negatively*; declared negative path followed, or run stops if none | VER-008 |
| FX-C6 | Checkpoint requiring A6; person records a decline | Decline/stop | *Resolved negatively*; not an A6; declared path followed | VER-008 |
| FX-C7 | Checkpoint reached-when (c) "proposal queued"; run cancelled before any proposal | Never met | Run ended with checkpoint *not reached*, never satisfied | VER-008 |
| FX-C8 | Checkpoint requiring A4 on the targeted rows' current content, reached-when (a) "before dispatch of OP-C4" (invented) | Kind (a) match | Call held undispatched; subject bound to the targeted rows' subject content identities; after host-captured A4 on that content, the same held call is dispatched unchanged | VER-008 |
| FX-C9 | A5 checkpoint on an operation; grant is direct | Forced proposal (C-6) | Dispatch carries the checkpoint constraint. An agent request for direct returns not permitted; a proposal is queued and the checkpoint waits | VER-008 |
| FX-C10 | A faithful record (A9) by the agent of an A4 the person said they did, with no capture evidence | Record without capture | Valid record shape only if it cites capture evidence. Here: checkpoint stays waiting | VER-008 |

## 12. Evidence standing labels

Every OUT-003 result carries exactly one of these labels; they are never
merged (V4-EXM-02/03; SoW AC-002, AC-009).

| Label | Means | Can support |
|---|---|---|
| CONTRACT-REVIEWED | This document inspected against its sources | Completeness of the receiving expectation |
| FIXTURE-EXECUTED | A fixture ran against a test double or recorded exchange, with identified catalog and model-interface bases | That the fixture's expectation holds for that double; nothing about the host |
| HOST-OBSERVED | Observed on an identified host candidate and configuration | Conformance of that candidate only |
| NOT-OBSERVED | No observation | Nothing; recorded as a gap |

Owner-reported construction (DEP-001's current standing) is none of these.

## Findings raised in R1

- G-1 (applied, with a finding). R-5 says an acceptance checkpoint forces
  *propose*. R-3 says treatment is resolved on the host route. The host route
  can resolve that only if it learns of the workflow's checkpoint constraint.
  No resolution names who carries it. This file carries it in the dispatch
  record (C-6, §6.2). DEL-04-01/DEL-03-02 should confirm at IR1 that the host
  route receives and honours it. The host's side is DEP-001.
- G-2. R-5 lists subject referents (change items, output, rows produced).
  Reached-when kind (a) "before dispatch" has no produced referent. This file
  binds kind (a) to the held call's targets (§2.4.1). DEL-02-01 should
  confirm.
- G-3. FX-C8 shows that a kind (a) checkpoint cannot sensibly require A5,
  because no change items exist before dispatch. DEL-02-01 may want a
  declaration rule that A5 checkpoints use kind (c).
- G-4. The loop carries DEL-04-02 grant states (R-8), but neither DEL-05-01 nor
  DEL-05-02 has a register row to DEL-04-02 (V1-C RF-5; V1-A RF-05). The
  resolution goes to C1.
- G-5. Supplied-guidance identity (§2.1 M-5) adds a per-turn recording duty to
  the host loop. It is required by DEL-02-01's *supplied* link (V1-C D-16).
  The host capability is DEP-001.

## UNRESOLVED

| Item | Owner | Point of need | Effect on this definition |
|---|---|---|---|
| OI-013 loop placement, parsing, persistence, panel assembly | Shared contract owner with SWB implementation owner | Before shared/host implementation boundary contracts | Outcomes only (M-4, §7, §8); no placement |
| OI-014 shared contract/component placement | App/shared contract owners | Before structural/production contract allocation | No common loop; candidate (b) is a question only |
| DEP-05-01-024 model-interface identity and protocol/fixture representation | UNKNOWN supplier; App/shared embedded-integration owner receives or agrees | At fixture/conformance use | §4 semantic only; MC-6, MC-8 held; no fixture executable |
| DEP-001 SWBPIPE host candidate and evidence (including host adoption of the D2 list, capture requirements, treatment enforcement, one effect per proposal identity) | SWBPIPE outside implementation session | Before corresponding connected integration/examination and fallback-replacement decision | All host conformance NOT-OBSERVED |
| OI-021 first connected operation; operation-specific reserved additions (D2) | Owner via outside SWB session and App/shared owner | Before connected-activity SoW and execution | Fixture subjects only; class values for FX-PIPE-01 entries pending additions |
| Consequence vocabulary for class assignment | DEL-04-01 with host policy owner | Before class assignment in DEL-03-01 | Class values carried as supplied |
| V1-C AB-01 mixed item decisions at an A5 checkpoint | DEL-02-01 with DEL-02-03 and DEL-03-02 | Before FX-C5/C9 and PC-07 fixtures | C-7: relayed, not decided |
| Hold machine and re-hold after post-resume lapse | DEL-02-03 (W7) | W7 | C-4 relays; no re-open by the loop |
| C U-C5: whether host-held findings are a change operation | DEL-03-01 with host owner | Before findings route (b) is used | E-5 route (b) conditional |
| G-1 carriage of the checkpoint constraint to the host route | DEL-04-01/DEL-03-02 with host owner | IR1 | C-6 / §6.2 element proposed |
| Proposal identity and resubmission mechanics (U-P1, TBD-002) | DEL-03-02 with host owner | Before FX-O1 execution | §6.3 states meaning only |
| Entry-version mismatch rule (C U-C6) | Host input via DEL-03-01 | Before FX-D-series execution | O-3 |
| N-OPEN-1 "user-controlled local model server" endpoints | App/shared embedded-integration owner with SWBPIPE owner; owner if V4-HOST-02's meaning is affected | Before endpoint-enforcement conformance cases are finalized | MS-11 held |
| N-OPEN-2 cloud-chosen destinations | Same | Same | MS-03 proposed |
| N-OPEN-3 tool-caused traffic | Tool's receiving-contract owner; Domains allocation open (OQ-03) | Before any network-using host tool | Out of scope; not a permission |
| T-OPEN-1 valid siblings beside a malformed call | App/shared embedded-integration owner with DEL-03-02 and host owner | Before FX-M8 is finalized | Proposed answer only |
| R-OPEN-1 quantitative responsiveness criterion | Owner, if wanted | Before any numeric criterion | None set |
| Seat role meaning mapping (U-09) | DEL-02-01 with SWB owner and DEL-02-04 | Before run-record fixtures | *unknown* allowed |
| FX-PIPE-01 mapping of provisional fixture labels | DEL-03-01 (fixture owner) with this owner | IR1 | Labels provisional |
| All R1_RESOLUTIONS-derived elements | Respective owners | IR1 | Adopted, not yet confirmed against supplier v0.2 text |

## Verification cases

These cases are designed, not run.

| Case | Procedure | Expected result | Serves |
|---|---|---|---|
| VC-01 | Trace §5.1 and MS-01…MS-10 to V4-HOST-01/02 and V4-ARC-11. Check that each has an expected outcome and an evidence type naming configuration and observed destinations | Every rule traced; MS-11 held; host observations NOT-OBSERVED | VER-001 |
| VC-02 | Inspect N-3, N-6, N-7 and MS-03/06/07/08 against V4-ARC-12 | Native layer named as the enforcement point; §12 labels applied; no host claim | VER-002 |
| VC-03 | Review §1, §2 and §4 for the four subjects, minimal Chat Completions capability, the distinct App Codex path (Responses API marked unobserved), open supplier/version/wire choices, and Pi excluded | All present; no field names; DEP-05-01-024 marked | VER-003 |
| VC-04 | Review §6 and FX-S/D/U/V3 against C §4.1 and P §9 as supplied at IR1. With a host trace, check V-3 precedes and prevents V-4, treatment is resolved on the host route, and outcomes are not collapsed | O-1 to O-6 hold; FX-D1 refused after V-3; FX-D2 uses revision within g1; FX-V3 not permitted | VER-004 |
| VC-05 | Exercise FX-M1…M9, FX-V1 and FX-O1 against a test double once DEP-05-01-024 and a C version exist | Zero dispatch for rejected calls; FX-V1 dispatched; three reports; FX-O1 class 4 with loop as reporter; label FIXTURE-EXECUTED | VER-005 |
| VC-06 | Review §8. On receipt of host observations, check candidate, configuration and placement choice | Protocol complete; no threshold; results limited to observed scenarios | VER-006 |
| VC-07 | Compare §10 one-for-one with SoW CLM-001/002/003, REQ-006, OI-013/014, DEP-001 and the Clarification | Every excluded act has its owner; no common construction allocated; OI tags present (incl. OI-013 on declaration/hold rows) | VER-007 |
| VC-08 | Review §2.3, §2.4, §9 and FX-C1…C10, FX-V2, FX-R1 against the DEL-04-01, DEL-04-03, DEL-02-01 and DEL-02-03 versions at IR1/W7 | Reached-when evaluated only on observed events; never-met gives *not reached* or *unknown*; subject binding enforced; capture evidence required; negatives follow the declared path; lapse at any time; no cross-act inference; reserved entries not permitted plus A8 | VER-008 |
| VC-09 | Audit every claim and later OUT-003 result for a §12 label and exact source/candidate identity, and every R1-derived element for IR1 confirmation | No HOST-OBSERVED claim without candidate evidence; DEP-001 standing not treated as evidence; R-n elements marked | VER-009 |
