# Minimal-loop and model receiving contract
- Contribution: DEL-05-01/LOOP-v0.3
- Status: DRAFT DEFINITION — proposed, unsupplied, not implemented, not accepted
- Serves: OUT-001, OUT-002, OUT-003, OUT-004; REQ-001–REQ-007; AC-001–AC-009; VER-001–VER-009 (all of DEL-05-01)
- Basis: repo 6e18505e3 (accepted basis); ScopeOfWork.md sha256 6fbbb580bdacb7f34b4df98a826519a28c087aff6e589ad27330ee556a83b568; P/docs/PRD.md §2.2 V4-HOST-01/02/03/04, §4.1 V4-WF-03/05, §4.5 V4-AUT-01/03/04/05, §4.7 V4-REC-03/04/05, §6, §9 OQ-02/OQ-11; P/docs/ARCHITECTURE.md §3 (V4-ARC-01/04), §4 (V4-ARC-10–14, host-agent properties), §5 V4-ARC-20, §6; P/docs/HOST_INTEGRATION.md §1, V4-HI-02/04, V4-HI-10–12, V4-HI-20–25, V4-HI-30–33, V4-HI-40–42, §8.1 closing paragraph, V4-HI-70/71; P/docs/EXAMINATION.md V4-EXM-01–03, V4-EXM-20–23; DECISION_BRIEF.html (sha256 02d38cb1…4c420e8) d2, d3, d5; APP-V4-CLARIFICATION-20260927/DIRECTION.md; SCC-CASE-002 Case_Datasheet M1/M4 rows; Open_Issues OI-003/013/014/021; External_Dependencies DEP-001; run folder OWNER_DECISIONS.md (sha256 f3f8e5f3…cf81f2e; decision `APP-V4-FIRST-INCREMENT-20260928-DECISION-1`, D2 and D3), R1_RESOLUTIONS.md (sha256 2f9c7e72…e177ec4), R2_RESOLUTIONS.md (sha256 77cfb845…cdebd088), comparisons/V1-A.md (01811533…e04c09), comparisons/V1-C.md (8d46258a…4a94a6), reviews/IR1-A.md (31b3c7f8…0b648284), reviews/IR1-B.md (70e4a4f6…2846), reviews/IR1-C.md (295e96b3…a426b9)
- Consumed inputs:
  - **Prior version.** DEL-05-01/LOOP-v0.2, sha256 1151d432…18762c9, at commit `c387730fb`.
  - **Sibling v0.2 text read from commit `28bd00499`** (`git show`) at the joins:
    - DEL-03-01/C-v0.2 `CATALOG_AND_READ_BASIS.md`, sha256 358182b1…6d82: §3.1, §4.1, §9, §10;
    - DEL-03-02/P-v0.2 `PROPOSAL_LIFECYCLE_AND_OUTCOMES.md`, sha256 942c1a3a…8c89: §3.1, §3.3, §4.3–§4.5, §5, §9;
    - DEL-02-01/WD-v0.2 `WORKFLOW_DECLARATION.md`, sha256 c25bccc5…a55c: §3.4, §4.2.4, §4.3, §6;
    - DEL-04-01/ACT-POLICY-v0.2 `ACT_AND_POLICY_CONTRACT.md`, sha256 e50f1fe2…93a9: §2.3–§2.5, §4, §5, §6;
    - DEL-04-02 `AUTONOMY_AND_STANDING_EXCHANGE.md`, sha256 3a4e8b01…329c: §3, §4.
  - **R2 v0.3 changes to those siblings.** These are not yet written by their owners. They are taken from R2_RESOLUTIONS and marked "per R2-n; to be confirmed at V2/IR2":
    - the five class values;
    - the governing checkpoint constraint in P §3.3;
    - resulting objects in the applied outcome;
    - OP-C10/OP-C11 and fixture exposure;
    - *effective (policy default)*;
    - the act-declined event name.
  - **DEL-05-02/PANEL-v0.3.** Co-drafted by this executor.
  - **Missing inputs.** DEP-05-01-024 has an UNKNOWN supplier and is not supplied. DEP-001 host evidence has not been received.
- Receivers: DEL-02-01 (OUT-001, OUT-003; REQ-002, REQ-005; VER-005) and DEL-05-02 (OUT-001, OUT-003; REQ-001, REQ-005; VER-001, VER-005) per CASE-002 M1/M4; DEL-02-03 (hold machine, W7); DEL-09-06/W9 relay file (§13 questions); external SWBPIPE owner via App-manager preparation and human file relay (DEP-05-01-021); DEL-05-01 itself for OUT-003 when host evidence arrives

## 0. How to read this definition

- **Semantic names only.** Names such as "call correlation identity",
  "catalog edition", "entry version", "subject content identity", "grant in
  force" or "governing checkpoint constraint" are semantic element names. They
  are not wire fields or types. The following are not selected:
  - transport;
  - protocol version;
  - hash or canonicalization algorithm;
  - persistence;
  - thread or process placement;
  - shared-component placement (OI-013, OI-014, DEL-03-01 TBD-003,
    DEL-03-02 TBD-002).
- **Standing labels.**
  - **SETTLED:** accepted basis or owner decision
    `APP-V4-FIRST-INCREMENT-20260928-DECISION-1`, credited only with what it
    says (R2-11).
  - **DERIVED:** follows from cited rules.
  - **INTEGRATION:** an integrator ruling (R-n / R2-n).
  - **PROPOSED:** this file's own proposal.
  - `UNRESOLVED{…}` is never a permission, a default or a pass.
- **Act names.** DEL-04-01 canonical names A1–A14 (ACT §2.1). Unqualified
  "checked" means only A4. "Approval" means only A6 (R-4).
- **Fixture.** Cases use the shared fixture **FX-PIPE-01** of DEL-03-01/C-v0.2
  §10, and cite its identifiers. The fixture contents:
  - workspace FX-W1, generation g1;
  - run R-100 between nozzles N-1/N-2;
  - supports S-1…S-4;
  - load case LC-1;
  - Engineer A;
  - workflow `supports-adjust` (origin *host*);
  - entries OP-C1…OP-C9;
  - timeline T1–T17 and Tg;
  - bases B1 (r12) and B2 (r13);
  - proposals PR-1, PR-2;
  - receipts RC-1…RC-3.

  **OP-C10 Undo** and **OP-C11** (class *no policy basis*, reason *pending
  OI-021*) are used per R2-21. So is the fixture exposure value **exposed on
  all three surfaces**, a fixture assumption.

  The v0.2 labels that collided with C (R-101, R-102, N-10…N-40, S-7…) are
  removed. The following cases keep **local labels `L-LOOP-n`**, because
  FX-PIPE-01 has no subject for them:
  - parse-level cases (MC);
  - endpoint cases (MS);
  - responsiveness cases (RS).

  None of this selects the first connected operation
  (`UNRESOLVED{OI-021}`).
- **Who builds what.** This contract states what the App/shared side needs
  from a host loop and how that is checked. The SWBPIPE loop, native layer,
  parser, persistence, panel and treatment enforcement belong to the external
  host owner (SoW CLM-001; HI §1; ARCH §4).

## Changes from v0.2

| Item | Change (section) |
|---|---|
| R2-1; IR1A-01; IR1-B B-M1; IR1C-10 | Five class values, including **no policy basis** with a *reason* sub-element ∈ {omitted, unassigned, pending OI-021}, labeled INTEGRATION. The v0.2 "four values" statement is removed (§2.2) |
| R2-2; IR1A-08 | The reserved-operation rule is restated as *performs* A4, A5, A6, A7, A10, A12 or A13 (act state). A host-offered faithful-record operation is a relay question (§2.2, §13) |
| R2-3 | Disabling external access is a person's setting change recorded as A13 (INTEGRATION) (§9) |
| R2-4; IR1A-02, IR1A-10; IR1-B B-M5; IR1C-11 | The V-2 split replaces v0.2's "exposed" filter: loop-side **not offered** vs host-reported **not exposed on this surface** (relayed). Reserved entries are always offered. A8 is *offered*, not recorded automatically (§2.2 TL-1, TL-5; §6) |
| R2-5; IR1A-03; IR1C-06; X-2 | Name is **act-declined event**, for A4, A6, A7 and A12, with capture evidence. It is separate from the run-ended event (§2.3, C-5) |
| R2-6; IR1A-05 | Grant state **effective (policy default)** added to the carried grant states. A default opens direct only when the policy default is *direct*; none exists in the first increment (O-6) |
| R2-7 (PROPOSED) | A12 checkpoint subject = setting content. A later A12 supersedes and does not lapse. A refused A12 at a checkpoint is held for W7 (§2.4.2, C-8) |
| R2-8 | A14/R13 is not applicable in host-loop runs (§9 A-5) |
| R2-9; IR1-A X-15 | No-policy-basis wording is applied. Fixtures report such cases as **held** (O-4, FX-NP1) |
| R2-10 | An act kind outside the checkpoint list is *invalid*; an unrecognized name is *not established* (§2.4) |
| R2-11; IR1C-17 | D3 attribution corrected in A-5 and §1 (SETTLED vs DERIVED) |
| R2-12; IR1C-03; IR1-B X-9 | **Governing checkpoint constraint** {workflow run, checkpoint name, required act A5, operation} is carried on dispatch. A direct request is *not permitted*, naming the constraint. Relay question added. FX-C9 is AWAITING INPUT (C-6, §6.2, §13) |
| R2-13 | Identity-based de-duplication precedes the basis check. The per-item basis check uses the subject content identities of the item's relied-on targets (§6.3; FX-O1) |
| R2-14; IR1-B (resulting objects) | Applied outcome carries the resulting objects and their post-application subject content identities. They are used for subject binding and reached-when kind (c) (TL-4, §2.4.2) |
| R2-15 | Undo reported as applied, with **reverses ⟨receipt⟩**. Acts on content the undo changes lapse normally (§2.3; FX-UNDO) |
| R2-17; IR1C-01, IR1C-05 | The loop binds the **declared subject class**, independent of the reached-when kind. There are five subject classes. The A5 declaration rule (kind (c) *proposal queued*) is consumed (§2.4.1–§2.4.2) |
| R2-18; IR1C-02 | C-7 cites **WD §4.3.7** (proposed). "Partial" is a per-item annotation. Item-left events are shown. "All accepted" is never claimed over a reduced subject |
| R2-19; IR1C-07; IR1A-09 | Lapse before resume: an **act-lapsed event** is recorded and the disposition returns to *waiting* ("waiting — lapsed at ‹t›"). *Lapsed* as a standing disposition is used only when the run has ended (C-4) |
| R2-20 (X-11, X-12, X-17, X-18); IR1C-08; IR1A-18 | <ul><li>The holding library is carried in the run association and never enters identity equality.</li><li>A reached, unperformed checkpoint stays *waiting* at run end, with a run-ended event. A post-run act does not change the ended run's disposition.</li><li>Relay questions: capture-evidence reference; per-turn supplied-guidance source and content identity (*unknown* where not recordable)</li></ul> (§2.1, §2.4.1, §13) |
| R2-21; IR1C-15; IR1-B B-M9/B-M10 | All fixtures re-pointed to C-v0.2 §10 identifiers plus OP-C10/OP-C11. Colliding labels removed. Local `L-LOOP-n` only where needed, with the reason (§0, §5.2, §7, §8, §11) |
| IR1C-14a | The declared-checkpoint element set now includes scope, purpose, actor requirement, on mixed decision and expected act evidence. The "act requested" event carries purpose and scope (§2.4, §2.3) |
| IR1C-16; IR1-B B-m7 | MC-8 adopts P §3.1 rule 5: separate proposals unless a call explicitly names the proposal it extends (§7) |
| IR1-B B-m5 | Evidence-label mapping to C's *illustrative / test-double / actual host* (§12) |
| IR1-B B-m6 | FX-D1 re-pointed to the element-7 error E-location-occupied (*refused — invalid*). The precondition "location on run" gives *unavailable* (FX-D1b) |
| IR1-B B-m11 | FX-U2 re-pointed to C T8 (OP-C2 "No current solve for LC-1 at this revision"). No UI gesture is used |
| IR1-A X-15 label | O-4's no-policy-basis rule is labeled INTEGRATION (R-3.5) |
| R3-1 (R3_RESOLUTIONS sha256 202d52c7…afbf; in place, no version bump) | Subject class **objects a named output concerns** added to §2.4.2 (INTEGRATION) |
| R3-2 (in place) | *Targets of the held call* is valid only with reached-when kind (a). Any other combination is invalid and reported, not evaluated (§2.4.2; INTEGRATION) |
| DEL-03-01 F-R2-2 check (in place) | Confirmed: the loop never labels an entry it did not offer *not exposed*. Element-9 exclusions surface loop-side only as **not offered**. Made explicit in TL-1 |

Changes from v0.1 are recorded in LOOP-v0.2 at commit `c387730fb`.

## 1. Position: host loop versus the App's Codex path

The host loop and the App's harness are different model interfaces. They
are never merged (SoW REQ-002; ARCH §§3, 4, 6; PRD §6).

| Aspect | Chirality App (not this contract) | Host embedded loop (this contract) |
|---|---|---|
| Agent runtime | Stock Codex App Server, owned by the App process (V4-ARC-01). Definition pin 0.158.0 (D4) | Minimal Chirality agent loop in the host (V4-ARC-10) |
| Model interface | Codex's published protocol. ARCH §6 records a dated assumption that local providers serve the Responses API that Codex requires. It is **unobserved** on an identified candidate (HOSTING L-2/P-11 as quoted in V1-C D-22) | OpenAI-compatible Chat Completions with tool calls (V4-ARC-10) |
| Credentials | Held by Codex (V4-ARC-04) | Held by the host native layer, outside the interface script (V4-ARC-12) |
| Tools and permission | Codex tools. Routine tool permission and sandbox modes are the user's own Codex setting (D3, SETTLED) | Host catalog entries offered as tools (V4-ARC-13). **No classifier permission mode** (D3, SETTLED). No separate routine tool-permission layer (DERIVED from D3 with V4-HI-40/41; §9 A-5) |
| Replaceability | Harness pinned and upgraded deliberately (V4-CST-03) | Loop replaceable behind the four-subject boundary in §2 (V4-ARC-14) |

Consequences:

1. A local server that serves both interfaces does not join them.
2. The App's Codex protocol types are not the host loop's types. The loop's
   detailed representation waits for DEP-05-01-024.
3. PRD §6 excludes a Chirality-owned loop for the App. The minimal loop has
   **host consumers only**. SWBPIPE is the only identified one; OI-005 is
   open (§10).
4. Pi is a possible later replacement behind §2. It is not a current
   dependency (V4-ARC-14).

## 2. The replaceable boundary: four subjects

A replacement loop (Pi's libraries, another library or a rewrite) conforms
when it preserves these meanings. Its code shape does not matter.

### 2.1 Messages and run association

| Semantic element | Meaning | Consumed from |
|---|---|---|
| Conversation identity | The conversation the message belongs to. Stable while it exists | DEL-04-03 (V4-HI-70) |
| Speaker kind | One of: person; agent; tool result; supplied guidance | This contract; guidance source DEL-02-01 |
| Content | Text or structured content. For the agent: streamed increments plus a completed form | This contract |
| Completion standing | Streaming, complete, truncated, interrupted, cancelled or failed | This contract |
| Workflow identity (run association) | {kind, origin, source root, name, revision} plus derived-from (V4-WF-03). Origin class is one of project, user, bundled or host. An unadapted carried workflow keeps its origin. A host adaptation is a new host-origin identity with derived-from. Example: FX-PIPE-01 `supports-adjust`: kind *workflow*, origin *host*, ⟨fx-root⟩, revision ⟨rev-3⟩ | WD §6.1 |
| Holding library | For a carried workflow, the host library that holds the copy actually read, at the listed, selected and resolved links. **It never takes part in identity equality** | WD §6.4 U-24; R2-20 (PROPOSED until W7) |
| Run identity | The workflow run, if any | DEL-04-03 |
| Seat role meaning | The role meaning the single seat carries for this run, or **unknown** | WD SEAT-1; P §3.3 |
| Supplied-guidance identity | Per turn, for each guidance input actually supplied to the model (workflow files, `SKILL.md`, `AGENTS.md`): its **source identity** (origin and name, or the workflow identity tuple) and its **content identity** with method designation. Where the host cannot record it, the value is **unknown** and is never inferred from configuration. Supplied ≠ adopted: whether the model took it up is not observed | R2-20; WD §6.2 *supplied* link; aligned with HOSTING §8.2 |
| Model configuration reference | The model setting in force (§5). Never contains a key | DEL-04-03 "model used" |

Loop obligations:

- M-1. Preserve the order and speaker of every message.
- M-2. A partial message that ends without completion is truncated,
  interrupted, cancelled or failed, never complete.
- M-3. The conversation store is operational state. It is never the
  authority for a human act (V4-REC-03, SETTLED).
- M-4. Persistence belongs to the host owner (`UNRESOLVED{OI-013}`). Only a
  citable conversation identity is required.
- M-5. Supplied guidance is recorded as actually supplied per turn, or as
  *unknown*. It is never recorded from launch configuration. The host's
  capability to record it is a relay question (§13 Q-4).

### 2.2 Tools

| Semantic element | Meaning | Consumed from |
|---|---|---|
| Catalog edition | Identity of the adopted catalog state from which offerings were made | C §2; one name on both sides |
| Tool offering | One catalog entry with all C elements 1–9:<ol><li>identity and entry version</li><li>purpose</li><li>input schema</li><li>availability and unavailable reason, as evaluated at offering (historical; re-evaluated at request)</li><li>effects</li><li>result schema with standing</li><li>errors with effect statements</li><li>class element (§3.1 sub-elements)</li><li>per-surface exposure</li></ol> | C §3, §3.1 |
| Tool call | Call correlation identity; operation reference; argument text; parse state (§7) | This contract. Representation per DEP-05-01-024 |
| Schema-conformant call | Parsed completely and conforming to the input schema of the named entry version in the offered edition. **Not** P's lifecycle state *validated* | This contract |
| Tool result | One of four classes (TL-2) | P §9 and C §4.1, unchanged (R-7) |

**Class element** (C §3.1, with R2-1 applied; five values):

| Value | Standing | Loop meaning |
|---|---|---|
| none | V4-HI-02 | Execute, e.g. reads. For FX-PIPE-01 reads and OP-C3, this is a fixture assumption |
| may apply within granted autonomy | V4-HI-02. For SWB model changes: DERIVED from V4-HI-41, default setting *propose* (C rule 2) | The host route resolves direct or propose from the grant state (ACT §5.3 rule 7) |
| proposal only | V4-HI-02 | Propose only; no grant widens it |
| reserved to the person | V4-HI-02. D2 lists the reserved acts (SETTLED). The operation rule is DERIVED (R2-2): an operation that **performs** A4, A5, A6, A7, A10, A12 or A13, including one that changes the host's own act state, is reserved | The agent receives *not permitted*, and an A8 request is **offered** (TL-5) |
| **no policy basis** | INTEGRATION (R2-1, from R-3.5), with *reason* ∈ {omitted, unassigned, pending OI-021} | Direct is **not permitted**. Proposing remains available but confers no permission, and any effect requires the person's A5 and host application. An A12 widening such a class is refused. Dependent production is held (REQ-004; R2-9) |

Every value carries the DEL-04-01 policy-class record reference and its
revision (C §3.1). Host adoption of any value is **not evidenced** (DEP-001).
The host names and enforces its own list (V4-HI-30). OI-002 is not a class
value (D3).

**Faithful-record operation** (R2-2). No faithful record is made through a
reserved operation. Any host-offered faithful-record operation must satisfy
all of the following:

- it does not change act state;
- it cites capture evidence;
- it never satisfies a checkpoint;
- it takes ordinary policy.

Whether any host offers one is §13 Q-5.

Loop obligations:

- TL-1. **Offering.** The loop offers every entry of the catalog edition
  that the host supplies for the embedded surface.
  - The loop never withholds an entry on its own reading of class or
    exposure (R2-4). Reserved entries are always offered.
  - If the host supplies an edition that already omits entries excluded by
    element 9 for the embedded surface, a call naming such an entry is a
    loop-side **not offered** failure (V-2). The loop never labels an entry
    it did not offer *not exposed on this surface*. That label appears only
    when the host returns it, and the loop relays it naming the host as
    reporter (C §4.1; DEL-03-01 F-R2-2).
  - An operation unavailable to the person is unavailable to the agent, with
    the same reason (V4-HI-04, SETTLED).
  - The loop never invents a tool without a catalog entry.
  - Availability shown at offering is historical. It is re-evaluated at
    request on the host route (C §7).
- TL-2. **Four tool-result classes**, never collapsed:
  1. **Loop-side failure, not dispatched:** §6 V-1 parse, V-2 *not
     offered*, V-3 schema, or the optional edition pre-screen.
  2. **Host non-success outcome:** unavailable; not permitted; channel not
     enabled; **not exposed on this surface** (host-reported, relayed);
     refused — invalid; refused — stale; error; application error.
  3. **Host outcome:** success (ran); queued; accepted; rejected; withdrawn;
     applied with receipt.
  4. **Dispatched, outcome not observed:** *outcome unknown*, reporter = the
     loop, with the last observed state.
- TL-3. Lifecycle meaning is preserved (V4-HI-25, SETTLED).
  - The loop never rewrites queued as applied, or applied as accepted.
  - It never rewrites refused as rejected; "rejected" is only A10 (R-7).
  - "Held at checkpoint" (§2.4.1 kind a) is a loop state. It is not a
    result class of the call.
- TL-4. **Basis and resulting objects.** Reads return their basis and
  standing (V4-HI-11/12):
  - the basis: workspace identity, generation, model revision, canonical
    content identity and method designation (C §5.1);
  - per-object **subject content identities** where the host supplies them
    (C §5.3).

  Applied outcomes carry the applied-outcome association (P §9). Per R2-14,
  to be confirmed at V2, they also carry the **created and changed object
  identities with their post-application subject content identities**. The
  loop passes all of these through unchanged. A later call cites the basis
  it relied on.
- TL-5. **Reserved entries and A8** (R2-4; IR1A-10).
  - An agent call to a reserved entry is dispatched like any other. The
    host route returns **not permitted**, naming the governing treatment and
    the policy record, and *offers* an A8 request.
  - The loop records no A8 automatically. An A8 exists only when the agent
    actually issues one, with the requester identified (§2.3).
  - A failed call is never turned into a request put to the person.

### 2.3 Events

Each event states its **subject**, **actor**, **reporter** and
**evidence**. An event is evidence of what the loop observed. It is never
itself a human act.

| Event meaning (semantic) | Subject | Actor / reporter | Evidence it may carry |
|---|---|---|---|
| Turn started / completed / cancelled / failed | Conversation turn | Person or agent / loop | Message references |
| Model stream progress | Agent message | Model / loop | Partial content ("streaming" only) |
| Model request refused at boundary | Model request | Host native layer | Refused destination or "key absent"; never key content |
| Model interface failure | Model request | Model server or transport / loop | Termination reason |
| Tool call received | Tool call | Model / loop | Correlation identity; operation reference; parse state |
| Tool call rejected: unparseable or truncated | Tool call | Loop | Parse state and reason; "not dispatched" |
| Tool call rejected: not offered | Tool call | Loop | Operation reference; catalog edition; "not dispatched" |
| Tool call rejected: schema | Tool call | Loop | Edition, entry version, schema reason; "not dispatched" |
| Offer out of date (optional edition pre-screen) | Tool call | Loop | Offered vs current edition; "not dispatched; re-offer" |
| Call held at checkpoint | Schema-conformant call | Loop | Checkpoint name; "held, not dispatched" (§2.4.1 kind a) |
| Tool call dispatched | Schema-conformant call | Loop | Dispatch record (§6.2) |
| Host outcome | Operation or proposal | Host | P §9 outcome unchanged: item dispositions, last observed state, evaluated basis on every non-success, both bases on stale, applied-outcome association with resulting objects (R2-14), **reverses ⟨receipt⟩** for an undo (R2-15) |
| Outcome not observed | Dispatched call | Loop (observer) | Last observed state; "outcome unknown" |
| Proposal decision relayed | Proposal items | Person (A5, A10) or proposer (A11); host records | Capture evidence reference; per-item change-item content identity |
| Item left subject | Bound change item | Host | Stale refusal, A11 or host refusal, per item (from DEL-03-02 item-left events, R2-18) |
| Examination findings | A3 examination | Agent | References to rows/results; read basis examined; "agent findings" (E-5) |
| Checkpoint reached | Declared checkpoint | Loop | Checkpoint name; the observed event that met reached-when; bound subject referents and content identities; **purpose** and **scope** |
| Checkpoint disposition changed | Declared checkpoint | Loop | New disposition; evidence reference; per-item annotation (A5) |
| A8 request issued | Act kind and subject | Agent (requester) | Request text; purpose and scope (at a checkpoint: the declared ones) |
| Human act observed | Actual act | Person (actor); capturing surface records | Capture evidence reference; recorder; recording mode; bound content |
| **Act-declined event** | A4, A6, A7 or A12 not performed | Person; capturing surface records | Declined act kind; bound subject; time; capture evidence (R2-5). Not an act of that kind |
| Act lapsed | Performed act | Host reports the change | Changed content identity; time (any time after performance) |
| Act superseded | Earlier A12 | Person (later A12) | Superseding act reference (R2-7, PROPOSED) |
| Grant change observed | Autonomy grant | Person (A12), host records | Display state per R-8/R2-6; A12 evidence if person-set |
| **Run ended** | Workflow run | Loop | Cause (model ended, person stopped, failure). Every declared checkpoint's disposition: *not reached*, *waiting*, *unknown*, *performed*, *resolved negatively*, or *lapsed* (only now as a standing disposition, R2-19). Unknown outcomes stay unknown |

Loop obligations:

- E-1. Emit only what was observed or done. An absent observation stays
  absent (SoW AC-009).
- E-2. Human-act, act-declined and proposal-decision events relay
  host-captured records. They never come from model text, success, queue
  position or a receipt (V4-HI-25/31, V4-AUT-03, SETTLED).
- E-3. References are carried, not copies (V4-HI-71, SETTLED).
- E-4. The events cover the run-record inventory (V4-HI-70):
  - workflow identity and holding library;
  - conversation;
  - autonomy settings (grant events plus the grant in force per dispatch);
  - operations and outcomes;
  - receipt references;
  - human acts and act-declined events;
  - model used;
  - supplied guidance.

  The field mapping is DEL-04-03's.
- E-5. Findings reach the panel in one of two ways:
  - (a) as agent message content with references;
  - (b) as a host outcome, if the host holds findings (`UNRESOLVED{C U-C5}`).

  An examination (A3, e.g. OP-C3 at T4) never changes domain tables. Its
  result is never labeled "checked" (R-4).

### 2.4 Checkpoints

A checkpoint is a declared point where the run waits for a specified human act
(V4-WF-05, V4-HI-42, SETTLED). The loop consumes the full WD §4.3.1 element
set (IR1C-14a).

| Declared element (WD §4.3.1) | Loop use |
|---|---|
| checkpoint name | Identity across interruption and replay |
| required act kind | One of A4, A5, A6, A7, A12. A recognized kind outside the list makes the checkpoint **invalid**. An unrecognized name is **not established** (R2-10). The loop evaluates neither case and reports it |
| reached-when | Kind (a), (b) or (c) (§2.4.1). Arrival only |
| subject (class) | Bound independently of reached-when (§2.4.2; R2-17) |
| scope | Extent of the subject covered (items, rows). Carried on the act request |
| purpose | Carried on the act request, and bound with the act (V4-REC-05) |
| actor requirement | "The person"; for A7, "the accountable professional". A class, not an identity |
| on negative decision | Path after A10 or an act-declined event. Absent: the run stops at the checkpoint |
| on mixed decision (A5, optional) | Per WD §4.3.7 |
| expected act evidence | The act record and its capturing surface |

Dispositions (shared): **waiting · performed · resolved negatively · lapsed ·
not reached · unknown**. DEL-02-03 owns the hold machine (W7).

#### 2.4.1 Reached-when evaluation by the loop

The loop evaluates each declared checkpoint's reached-when **only against
events it observed** (E-1; WD RW-1). It never uses model text, prose stage or
the model's claims.

| Kind | Evaluated when | Loop behaviour on match |
|---|---|---|
| (a) before dispatch of a named required-tool reference | After a call to that operation passes V-1 to V-3, and before dispatch | Hold the schema-conformant call undispatched. Emit "call held at checkpoint". Return to the model a tool result saying the run is held (a loop state, not a failure). After *performed*, dispatch the **same** held call unchanged. A different call is a new call, and the act does not carry to it |
| (b) observed production of a named declared output | An observed event establishes the output: a host outcome producing it, or a completed agent message the declaration designates as that output. A model statement that it exists does not count | Stop acting on the run |
| (c) observed host outcome of a named operation, e.g. *proposal queued* | The host outcome for that operation matches the named outcome | Stop acting on the run |

On a match the loop emits "checkpoint reached" with purpose, scope and the
bound subject. It sets *waiting* and stops acting on the run (C-1).

**Never met, run end and later acts** (WD §4.3.4; R2-5, R2-20):

- If the run ends without the condition having been observed, the checkpoint
  is **not reached**.
- If the deciding observation was lost (for example, kind (c) with *outcome
  unknown* for the named operation), the checkpoint is **unknown**.
- If the checkpoint was reached but the act was never performed, it stays
  **waiting** at run end. The run-ended event lists it. It is never
  performed or satisfied.
- A person's act performed **after** the run ended is recorded as a human
  act and relayed against the checkpoint's bound subject. It does not change
  the ended run's recorded disposition, unless DEL-02-03 (W7) defines
  resumption of an ended run.
- Stopping a run is a **run-ended event**. It is not an act-declined event
  (R2-5).

#### 2.4.2 Subject binding: the declared subject class (R2-17)

The loop binds the **declared subject class**. It never infers the class
from the reached-when kind (IR1C-01). The reached-when event provides arrival
and the referents the class names.

| Declared subject class (R2-17) | Bound referents and content identity |
|---|---|
| Change items of a named proposal | Proposal and item identities, and each item's **change-item content identity** (P §3.1) |
| Named output | The output and its content identity (host-supplied, or file content identity for App files) |
| Objects changed by a named outcome | The created and changed object identities in that outcome's applied-outcome association, with their **post-application subject content identities** (R2-14; C §5.3) |
| **Objects a named output concerns** (R3-1, INTEGRATION) | The objects identified in a named read or examination output (e.g. the rows OP-C3 examined at T4), bound through their **subject content identities as read** in that output's basis (C §5.3). Lets a review-only workflow require A4 on the rows it examined |
| Targets of the held call (**valid only with reached-when kind (a)**, R3-2, INTEGRATION) | The targets the held call names, bound through the **subject content identities of the relied-on read** that the call cites (C §5.3/§5.4). Argument text is never used. Declared with any other reached-when kind, the checkpoint is invalid, and the loop reports it without evaluating it |
| Grant setting (A12) | The **setting content**: classes, grant value and scope (R2-7, PROPOSED) |

- **A5 declaration rule** (R2-17): an A5 checkpoint uses reached-when kind
  (c) *proposal queued* for the operation whose result it concerns. Its
  subject is that proposal's change items. Any other A5 combination is
  invalid in the declaration (DEL-02-01), and the loop reports it.
- An act on other content, another proposal or another row set does not
  satisfy the checkpoint, even if the kind matches (WD SB-3).

#### 2.4.3 Loop obligations

- C-1. At a reached checkpoint the loop stops acting on the run. No grant
  widens past a reserved act or a declared checkpoint (D2, SETTLED;
  V4-HI-42).
- C-2. **Performed** requires capturing-surface evidence of the specified
  act kind, by a qualifying actor, bound to the current content of every
  bound referent in scope. The capturing surface is the host act facility
  for host content (ACT §4.5).
  - A faithful record (A9) citing that evidence is a valid record shape.
    Alone it never satisfies the checkpoint.
  - None of these satisfies it: model text, success, findings, an A8
    request, an agent-authored record, or another act kind.
  - Without a capture-evidence reference from the host (§13 Q-2), no
    host-content checkpoint can become *performed*. It stays *waiting*, or
    *unknown* after interruption.
- C-3. There is no synthetic ordering. For example, A5 is not required
  before A4 (WD I-3).
- C-4. **Lapse** (R2-19).
  - Whenever the host reports that bound content changed after the act, the
    loop records an **act-lapsed event**.
  - **Before the run resumes**, the disposition returns to **waiting**,
    shown as "waiting — lapsed at ‹t›". A new act on the current content is
    needed.
  - **After resume**, the lapse is recorded and relayed. Re-hold belongs to
    DEL-02-03; the loop does not re-open a run.
  - *Lapsed* as a standing disposition appears only for a checkpoint whose
    run has ended.
  - Applying an accepted item does not lapse A5. A basis failure between
    acceptance and application is stale, not lapse (P §4.2).
  - An undo (OP-C10) that changes bound content lapses acts normally
    (R2-15).
- C-5. **Negative decisions** (R2-5).
  - For A5, the negative decision is A10 (per item).
  - For A4, A6, A7 and A12, it is an **act-declined event** carrying capture
    evidence. That event is not an act of the declined kind.
  - Either case gives the disposition **resolved negatively**. The declared
    *on negative decision* path is then followed; if none is declared, the
    run stops.
- C-6. **Governing checkpoint constraint** (R2-12; per R2-12, to be confirmed
  at V2).
  - Where a declared checkpoint requires A5 on an operation's result, every
    dispatch of that operation in that run carries the constraint
    {workflow run identity, checkpoint name, required act A5, operation
    reference}.
  - The host route resolves *propose*. A direct request is **not
    permitted**, naming the constraint as the governing treatment. It is
    never converted into a proposal.
  - The loop does not decide treatment (R-3.1).
  - A host that uses its own copy of the declaration still receives the
    constraint, for record comparison.
  - An omitted constraint is indistinguishable from none at the host. That
    omission is an App-side or loop defect and an evidence limit (§13 Q-1).
- C-7. **Mixed item decisions** at an A5 checkpoint follow **WD §4.3.7**
  (PROPOSED there; DEL-02-03 confirms at W7):
  - every bound item has A5 → *performed*;
  - any item undecided → *waiting*;
  - all items decided, at least one A10 → *resolved negatively*, with a
    per-item **partial** annotation if some items have A5.
  - Items that leave without a decision (stale, A11, host refusal) are
    relayed with their event.
  - A *performed* over a reduced subject is never reported as "all accepted"
    (R2-18).
- C-8. **A12 checkpoints** (R2-7, PROPOSED).
  - The act binds to setting content. A later A12 **supersedes** it and does
    not lapse it. A checkpoint the earlier A12 performed stays *performed*,
    and the supersession is shown.
  - Whether an A12 that the control refuses counts at a checkpoint is held
    for DEL-02-03 (W7).

## 3. Operating sequence (one turn)

The steps below are semantic. Their placement is owner-selected
(`UNRESOLVED{OI-013}`).

```text
person message ─► request (messages + offerings of edition K + supplied guidance, identities recorded)
   ─► native layer: destination check; key if cloud (§5) ─► model server
   ◄─ streamed content and/or tool calls, then termination reason
for each tool call:
   V-1 parse ── fail ─► class 1, not dispatched
   V-2 operation in offered edition K? ── no ─► class 1 "not offered", not dispatched
   V-3 input schema ── fail ─► class 1, not dispatched
   [kind (a) checkpoint on this operation?] ─► hold call; checkpoint waiting
   dispatch with dispatch record (§6.2) ─► host route V-4/V-5
   ◄─ host outcome (class 2/3, incl. relayed "not exposed") or none (class 4)
   [kinds (b)/(c) match?] ─► checkpoint waiting; subject bound per declared class
run end ─► run-ended event with every checkpoint disposition
```

## 4. Minimal Chat Completions capability

| Capability | Why | Settled or open |
|---|---|---|
| Submit an ordered conversation and tool offerings | Messages, tools | Settled need (V4-ARC-10) |
| Receive assistant content incrementally | §8; panel | Settled need |
| Receive tool calls (correlation identity, name, argument text, possibly fragmented) | Tools; §7 | Need settled; fragment representation open (DEP-05-01-024) |
| Termination reason that distinguishes complete, length-truncated and error | §7 | Need settled; representation open |
| Return a tool result for a correlation identity, including "held at checkpoint" | Tools; §2.4.1 (a) | Settled need |
| Several tool calls per response | §7 MC-8 | `UNRESOLVED{DEP-05-01-024}` |

No provider, server, model or version is selected. ARCH §6 names are dated
assumptions.

## 5. Model selection, destination and key boundary

### 5.1 Settings (semantic)

| State | Meaning |
|---|---|
| Local (default) | User-controlled local model server configured (V4-HOST-01) |
| Cloud chosen, key supplied | The person chose cloud and supplied a key |
| Cloud chosen, key absent | No request may be made |
| Unconfigured | No request may be made; there is no cloud fallback |

- **SETTLED.**
  - N-1: local is the default. Cloud is used only on the person's choice
    plus a key (V4-HOST-01, V4-ARC-11).
  - N-2: in local operation, the only destination is the configured server
    (V4-HOST-02).
  - N-3: requests go through the native layer, which enforces the endpoint
    and holds the key outside the script (V4-ARC-12).
- **PROPOSED.**
  - N-4: settings change only by the person's act.
  - N-5: there is no cloud switch on a local failure.
  - N-6: the key never appears in script memory, messages, events, records,
    the panel or errors.
  - N-7: the native layer is the enforcement point.
- **Open.**
  - `UNRESOLVED{N-OPEN-1}`: what counts as "user-controlled local" endpoints.
  - `UNRESOLVED{N-OPEN-2}`: cloud-chosen destinations.
  - `UNRESOLVED{N-OPEN-3}`: tool-caused traffic (e.g. a later Domains query).
    Not a permission.

### 5.2 Case matrix

These are endpoint-level local cases, labeled `L-LOOP-MS-n`, because
FX-PIPE-01 has no network subjects.

| Case | Setting / stimulus | Expected | Evidence for a host claim |
|---|---|---|---|
| MS-01 | Local default; the person asks for an OP-C1 read of R-100 | Only the configured local server is contacted | Observed destinations with configuration (V4-EXM-01/23) |
| MS-02 | Unconfigured | No request; notice; no fallback | Observed absence |
| MS-03 | Cloud chosen, key supplied | Chosen endpoint via the native layer; key not visible to script | Native trace; script inspection |
| MS-04 | Cloud chosen, key absent | No request; failure reported | Observed absence |
| MS-05 | Model output asks for another endpoint | Refused; setting unchanged; event | Setting before/after |
| MS-06 | Local operation; a test-double library attempts a telemetry request (`L-LOOP-MS-06`) | Refused by the native layer; nothing sent | Native refusal plus capture |
| MS-07 | Script attempts to read the key | Not available | Script inspection |
| MS-08 | Cloud auth error | Reported without key content | Error, event, record |
| MS-09 | Local server unreachable | Failure; no cloud switch | Destinations; event |
| MS-10 | Person switches cloud → local | Only local afterwards; change attributed to the person | Destinations; setting record |
| MS-11 | "Local" endpoint on another machine | Held on `UNRESOLVED{N-OPEN-1}` | — |

## 6. Validation order, treatment and dispatch

SETTLED: catalog-schema checking comes before the host's validation
(V4-ARC-13), and there is one route (V4-HI-20). INTEGRATION (R-3.1):
treatment is resolved on the host route at validation and again at
application. The loop relays intent.

| Step | Check | By | On failure |
|---|---|---|---|
| V-1 | Parse completeness (§7) | Loop | Class 1 "malformed/truncated" |
| V-2 | The named operation is an entry of the catalog edition offered to the loop | Loop | Class 1 **not offered** (R2-4). Never dispatched |
| V-3 | Input schema of the offered entry version | Loop | Class 1 "schema" |
| V-4 | Host validation: exposure on this surface; availability re-evaluated; preconditions; basis currency; entry version; domain rules | Host route | Class 2: **not exposed on this surface** (host-reported, relayed); unavailable (declared precondition, HI-04 parity); refused — invalid (element-7 error); refused — stale (both bases); error, including entry-version mismatch (C element 7, U-C6) |
| V-5 | Treatment and application or proposal | Host route | Class 2 *not permitted* (naming the treatment, the policy record or the governing checkpoint constraint); application error (effect none/partial/unknown); or a class 3 outcome |

### 6.1 Receiving requirements

- O-1. V-3 always runs before V-4. A call that fails V-1 to V-3 never reaches
  V-4.
- O-2. A schema-conformant call is not validation, application or a human act
  (SoW REQ-003).
- O-3. The dispatch carries the catalog edition and entry version offered.
  An optional pre-screen may report "offer out of date" on the loop side.
  An entry-version mismatch is a host error (C element 7; U-C6).
- O-4. Treatment → outcome map, consumed from ACT §6 (INTEGRATION, R-3;
  R2-4):
  - direct without an effective direct treatment → *not permitted*, never
    converted;
  - reserved → *not permitted*, and an A8 request is offered;
  - **no policy basis** → direct *not permitted*, proposing available
    (INTEGRATION, R-3.5). Proposing confers no permission. Any effect
    requires A5 and host application. Dependent production stays held
    (REQ-004; R2-9);
  - widening never converts a queued proposal.
- O-5. Standing at drafting (the grant in force carried on dispatch) and the
  host-reported treatment at resolution (validation, application) are both
  recorded when they differ (R-3.6).
  - Narrowing leaves a queued proposal unaffected.
  - An unapplied operation is re-resolved at application (DEP-001).
- O-6. **Grant states carried** (R-8; R2-6):
  - effective (person-set);
  - **effective (policy default)**;
  - requested by agent;
  - set by person, not yet confirmed by control;
  - unconfirmed;
  - not set;
  - refused (reason).

  The direct branch applies only in an *effective* state whose grant value
  is direct. *Effective (policy default)* opens direct only if the policy
  record's default is *direct*; no such default exists in the first increment
  (the SWB default is *propose*). The host route decides; the loop carries.

### 6.2 Dispatch record (every dispatch)

| Element | Meaning |
|---|---|
| Origin | Author type (agent); author identity (seat); channel (embedded); conversation; run identity; workflow identity tuple; holding library (V4-HI-21; P §3.3) |
| Seat role meaning | Per §2.1, or *unknown* |
| Grant in force | Settings reference, display state (O-6) and scope, as last observed |
| Requested mode | Apply directly or propose, as the call or the entry's meaning expresses it |
| Governing checkpoint constraint | Per C-6, where applicable (R2-12) |
| Relied-on basis | As cited, with method designations; per-target subject content identities |
| Catalog edition and entry version | O-3 |
| Proposal identity | The existing identity for a resubmission (§6.3); otherwise per DEL-03-02 |
| Reason | The proposer's reason (P §3.3) |
| Correlation identity | The model's call identity |

### 6.3 Retry, resubmission and re-draft

- R-a. **Retry keeps the proposal identity** (R-7; P §3.1). A resubmission,
  whether by the loop after a transport failure or by the agent citing the
  proposal identity, carries the same identity and unchanged content. The
  loop never mints a new identity for a retry.
- R-b. **De-duplication precedes the basis check** (R2-13, INTEGRATION).
  - A resubmission of a known proposal identity returns that proposal's
    recorded state or outcome, e.g. the applied association with RC-1 at
    T13.
  - It is never refused as stale because of its own effects.
  - One effect per identity is a host obligation to be evidenced (DEP-001,
    §13 Q-6). Each submission is recorded with only observed effects.
- R-c. **Per-item basis check** (R2-13). Staleness compares the **subject
  content identities of the item's relied-on targets**, not the global
  revision. Applying sibling items of the same proposal does not make
  remaining items stale unless they share targets. The host rule is still
  U-C3.
- R-d. **After outcome unknown**, the loop seeks observation before
  resubmitting. The mechanism is DEL-03-02 U-P1/TBD-002.
- R-e. **A re-draft is a new proposal** with lineage, a fresh read and new
  change-item content identities, as for T9's PR-2 relative to PR-1. No
  acceptance carries over, and there is no retarget (V4-HI-23).

## 7. Malformed and truncated tool calls

SETTLED: truncated or malformed calls are reported failures, never executed as
empty arguments (ARCH §4; SOW-142). These are parse-level local cases,
`L-LOOP-MC-n`, because FX-PIPE-01 has no model-output subjects.

| ID | Condition | Expected handling |
|---|---|---|
| MC-1 | Length truncation while argument text is incomplete | Failure "truncated"; not dispatched; three reports |
| MC-2 | Stream interrupted during argument text | Failure "interrupted"; not dispatched |
| MC-3 | Complete but not parseable | Failure "malformed" |
| MC-4 | Parses, but not the required structured form | Failure "malformed" |
| MC-5 | Operation reference missing, empty, or not in the offered edition | V-2 **not offered**; not dispatched |
| MC-6 | Argument text absent or empty | Never coerced to empty arguments. Treated as malformed until DEP-05-01-024 says how "no arguments" is expressed |
| MC-7 | Two calls share a correlation identity | Failure for both (PROPOSED) |
| MC-8 | Several calls in one response, one of them malformed | The malformed call is not dispatched. Proposed: valid siblings run, each on its own validation (`UNRESOLVED{T-OPEN-1}`). **Grouping follows P §3.1 rule 5**: sibling calls form separate proposals, unless a call explicitly names an existing proposal it extends. That is the drafter's choice, not a loop merge. Grouping mechanics: U-P9 |
| MC-9 | The loop "repairs" incomplete text | Prohibited. A re-issued call is a new call |

Reports go to three recipients:

1. the model (class 1 result);
2. the event stream / panel ("tool call rejected", "not dispatched");
3. the run record (requested; "not executed: rejected before host
   validation").

Dispatch observation: zero host-route calls for a rejected correlation
identity. FX-V1 is the valid comparison.

## 8. Responsiveness: observation protocol (no numeric thresholds)

SETTLED: the loop does not block the host interface; long parsing and
streaming run off the main thread where needed (ARCH §4). Placement is the
host owner's (`UNRESOLVED{OI-013}`). No threshold is set
(`UNRESOLVED{R-OPEN-1}`).

| ID | Load | Concurrent interaction |
|---|---|---|
| RS-1 | A long model stream (`L-LOOP-RS-1`; no FX-PIPE-01 subject) | Scroll and select in the OP-C1 supports table for R-100; open the LC-1 results view; type in a host field |
| RS-2 | A large read result (`L-LOOP-RS-2`: a large invented model. FX-PIPE-01's four supports are too small, hence the divergence) | The same interactions, during parse and result handling |
| RS-3 | Stream in progress | Cancel. It takes effect, and the interface stays usable |
| RS-4 | Stream during host work (e.g. a new solve of LC-1) | Interact with independent views |

Each observation records:

- the candidate;
- the configuration and date (V4-EXM-01);
- the environment;
- the owner's placement choice;
- each interaction and its account (usable, degraded, blocked or not
  observed);
- any host measurement, as observed;
- limitations.

Verdict form: "continued usability observed for X on candidate Y".

## 9. Distinct acts at the loop boundary

| Act | Actor | What the loop may emit | Never |
|---|---|---|---|
| A1 propose | Agent or person | Dispatch; "queued" | Acceptance |
| A2 apply (direct under grant) | Agent within an effective direct grant; host applies | "applied", branch *direct under grant*, receipt, origin, undo route, later-examination route (T16, RC-2) | Acceptance, checking, approval |
| A2 apply (after acceptance) | Host | "applied", branch *after acceptance*, receipt (T12, RC-1) | Approval |
| Undo (OP-C10) | Actor per its treatment; host applies | "applied", **reverses ⟨receipt⟩** (T17, RC-3 reverses RC-2) | Erasure of earlier records |
| A3 examine | Agent | "examination findings" (T4) | "Checked" |
| A4 mark checked | Person (D2a, SETTLED) | Relayed "human act observed" (T2) | Creation by the agent; inference from findings |
| A5 accept | Person where autonomy requires a proposal (D2b, SETTLED); per item | Relayed decision (T11 item 1) | Inference from success, queue or receipt |
| A6 approve | Person (D2c, SETTLED) | Relayed act only | Any agent statement of approval (V4-AUT-05) |
| A7 rely | Accountable professional (D2d, SETTLED) | Relayed act only | Inference from another act |
| A8 request | Agent | "A8 request issued", only when issued | Performance; automatic creation |
| A9 record | Identified recorder, actor ≠ recorder | Recording mode on relayed acts | Checkpoint satisfaction alone |
| A10 reject | Person wherever A5 is reserved | Relayed with actor (T11 item 2) | "Rejected" for a host refusal |
| A11 withdraw | Proposer | Relayed with actor | — |
| A12 set grant | Person (D2e, SETTLED) | "Grant change observed" (T15); supersession (R2-7) | A grant change from an A8 |
| A13 enable/disable external access | Person. Enabling: D2e, SETTLED. Disabling as A13: INTEGRATION (R2-3) | Not a loop event (external channel). An agent may request it (A8) | — |
| A14 tool permission | App only | Not applicable in host-loop runs. R13 is not applicable (R2-8) | — |

- A-1. Evidence of one act never establishes another.
- A-2. An agent may request (A8) and prepare. It never records an act as
  performed (V4-HI-31).
- A-3. Relayed acts carry actor, recorder, recording mode and a
  capture-evidence reference. Only capture evidence satisfies a checkpoint.
- A-4. Still open:
  - operation-specific reserved additions (`UNRESOLVED{OI-021}`);
  - host adoption and capture requirements (DEP-001).
- A-5. **Permission layer** (R2-11 attribution):
  - *No classifier permission mode in hosts; the SWB default proposal mode
    applies*: **SETTLED** (D3).
  - *No separate routine tool-permission layer in the host loop. Host
    operation authority is the person's grant plus adopted policy, resolved
    on the host route*: **DERIVED** from D3 with V4-HI-40/41.
  - The loop presents no tool-permission prompts. Nothing in the loop stands
    in for a reserved or professional act.

## 10. Owner-allocation and open-choice account (OUT-004)

### 10.1 Responsibility map

| Responsibility | This DEL-05-01 | Other App-v4 owner | External host (SWBPIPE) | Open issue / point of need | Standing |
|---|---|---|---|---|---|
| Loop receiving requirements, fixtures, cases | Owns | — | Receives through relay | — | v0.3 draft |
| Loop construction, placement, parsing, persistence | Excluded; requires outcomes only | — | Owns and selects | OI-013 | Owner-reported building (DEP-001) |
| Panel assembly | Excluded | DEL-05-02 (receiving) | Owns | OI-013 | Open |
| Native networking, endpoint, key | Excluded; defines §5 cases | — | Owns | N-OPEN-1/2 | Not received |
| Treatment resolution, exposure evaluation, de-duplication | Excluded; relays | ACT (policy), C/P | Host route | DEP-001; §13 | Not received |
| Catalog, read basis, exposure, fixture | Consumes | DEL-03-01 | Implements | TBD-003 | C-v0.2 read; R2 additions to confirm |
| Proposal and outcomes | Consumes | DEL-03-02 | Route, receipts | TBD-002 | P-v0.2 read; R2-12/13/14 to confirm |
| Declarations | Consumes | DEL-02-01 | Host workflows | OI-014; OI-013 | WD-v0.2 read; R2-17 to confirm |
| Hold machine | Evaluates reached-when in hosts | DEL-02-03 (W7) | Host execution | OI-013 | Pending W7 |
| Act policy | Consumes | DEL-04-01 | Enforces own list; offers and captures acts | OI-021; consequence vocabulary | ACT-v0.2 read; R2-1…R2-10 to confirm |
| Grant display states | Carries | DEL-04-02 | Controls | Register gap (C1) | AS-v0.2 read; R2-6 to confirm |
| Record format | Consumes | DEL-04-03 | Receipts, acts | — | Per R-n / R2-n |
| Model-interface basis | Receives or agrees | — | Unknown | DEP-05-01-024 (UNKNOWN) | Not supplied |
| Host evidence | Receives, audits | Joined witness DEL-09-06 | Supplies | DEP-001 | Not received |
| Common loop implementation | Not allocated | OI-014 owners | — | OI-014/013 | No agreed repeated responsibility |
| Human acts | None | — | Offers, captures, presents | — | Person only |

### 10.2 Common-implementation assessment

- The App runs no Chirality loop, so SWBPIPE is the one identified consumer
  (OI-005 open).
- Two candidate repeated parts exist, for OI-014 consideration only:
  - (a) parse completeness;
  - (b) catalog-schema checking, which might also serve DEL-03-03 (C holds
    this as a question).
- **No repeated responsibility is established. No common loop is proposed.**

### 10.3 Required inputs and standing

| Input | Supplier | Standing at v0.3 |
|---|---|---|
| Entry elements 1–9; five class values; edition; exposure; basis; subject identities; FX-PIPE-01 | DEL-03-01 | C-v0.2 read at `28bd00499`. R2-1/R2-21 additions pending C-v0.3 |
| Outcomes; identities; constraint; resulting objects; de-duplication | DEL-03-02 | P-v0.2 read. R2-12/13/14 pending P-v0.3 |
| Checkpoint elements; subject classes; §4.3.7; identity tuple; holding library | DEL-02-01 | WD-v0.2 read. R2-17/20 pending WD-v0.3 |
| Hold machine; resumption after run end; refused A12 | DEL-02-03 | Not drafted (W7) |
| Act names; decline; treatment map; reserved operations | DEL-04-01 | ACT-v0.2 read. R2-1…R2-10 pending |
| Grant states incl. policy default | DEL-04-02 | AS-v0.2 read. R2-6 pending |
| Record inventory | DEL-04-03 | Per R-n / R2-n |
| Panel needs | DEL-05-02 | PANEL-v0.3, same executor |
| Model interface | UNKNOWN (DEP-05-01-024) | Not supplied |
| Host candidate and evidence | SWBPIPE (DEP-001) | Not received |

## 11. Fixture inventory (OUT-002, designed)

Every fixture names its catalog basis and its model-interface basis. The
catalog basis is C-v0.2 FX-PIPE-01, plus OP-C10/OP-C11 per R2-21. The
model-interface basis is DEP-05-01-024, currently UNKNOWN. Until both are
supplied, the fixtures are case designs. Fixture exposure is "exposed on all
three surfaces" (a fixture assumption, R2-21) unless a variant is named.

| Fixture | FX-PIPE-01 subject | Input | Expected result | Serves |
|---|---|---|---|---|
| FX-V1 | T3: OP-C1 read of R-100 | Schema-conformant call | Dispatched; basis B1 with subject content identities per row | VER-004/005 |
| FX-V2 | T9–T10: PR-2 (item 1 via OP-C4 add support; item 2 via OP-C5 S-3 stiffness), relying on B2 | Schema-conformant call | Dispatched; "queued"; no acceptance event | VER-004/008 |
| FX-V3 | OP-C9 label S-4, requested direct **before** T15 (grant *effective (policy default)* propose) | Direct request | *Not permitted* (O-6); not converted | VER-004/008 |
| FX-V4 | T16: OP-C9 label S-4 "G-4" after T15 (effective direct) | Direct request | Applied, branch *direct under grant*, RC-2, origin mark, undo route; no acceptance | VER-004/008 |
| FX-S1 | OP-C5 stiffness given as text | Schema-invalid | Rejected at V-3 | VER-004 |
| FX-S2 | OP-C4 with the location missing | Schema-invalid | Rejected at V-3 | VER-004 |
| FX-D1 | OP-C4 at an occupied location on R-100 | Element-7 error | *Refused — invalid* (E-location-occupied) with evaluated basis | VER-004 |
| FX-D1b | OP-C4 at a location not on R-100 | Declared precondition | *Unavailable* "Location is not on run R-100" (HI-04 parity) | VER-004 |
| FX-D2 | T7: PR-1 relying on B1 (r12) after T6 (S-3 edited, r13) | Stale | *Refused — stale*, with B1 and B2; re-draft is PR-2 with lineage (T9) | VER-004 |
| FX-D3 | Tg: generation g2 after restore | Lineage change | Refusal reporting both bases; meaning per U-C2 | VER-004 |
| FX-U1 | A name absent from the offered edition | Not offered | Class 1 at V-2; not dispatched | VER-005 |
| FX-U2 | T8: OP-C2 for LC-1 at r13 | Unavailable | *Unavailable* "No current solve for LC-1 at this revision", evaluated B2 | VER-004 |
| FX-U3 | Named variant: OP-C2 not exposed on the embedded surface | Host exposure | Dispatched; host returns *not exposed on this surface*, relayed as class 2 | VER-004 |
| FX-R1 | Agent calls OP-C6 on S-2 | Reserved entry | *Not permitted*, naming reserved class and policy record; A8 offered, not recorded unless issued; no A4 | VER-008 |
| FX-R2 | Agent calls OP-C7 to accept PR-2 item 1 | Reserved entry | *Not permitted*; no A5 | VER-008 |
| FX-NP1 | OP-C11 (no policy basis, pending OI-021) requested direct; then proposed | Class no policy basis | Direct *not permitted*; proposal queues with no effect until A5 and application. **Case state HELD** (R2-9) | VER-004 |
| FX-O1 | T13: acknowledgment of T12 lost; resubmit PR-2 with the same identity | Retry | De-duplication returns the recorded outcome (RC-1). Never stale for its own effects. If unobservable: class 4, reporter loop | VER-005/009 |
| FX-UNDO | T17: OP-C10 undo RC-2 | Undo | Applied RC-3 **reverses RC-2**. Acts bound to the changed label lapse normally | VER-008 |
| FX-M1…M9 | MC-1…MC-9 (`L-LOOP-MC-n`) | Malformed | As §7 | VER-005 |
| FX-N1…N11 | MS-01…MS-11 (`L-LOOP-MS-n`) | Settings | As §5.2 | VER-001/002 |
| FX-C1 | Checkpoint A4; reached-when (c) *applied* for PR-2; subject class "objects changed by a named outcome" | Kind (c) | Waiting. Subject = objects created or changed by RC-1 (new support), by post-application subject content identities (R2-14). Performed only on host-captured A4 on those | VER-008 |
| FX-C2 | The same checkpoint; model text claims it was checked | Assertion | Still waiting | VER-008 |
| FX-C3 | FX-C1 performed; then the new support is edited (variant of T14), before resume and after resume | Lapse | Before resume: act-lapsed event, then "waiting — lapsed at ‹t›". After resume: lapse relayed; re-hold per DEL-02-03. At run end with no new act: *lapsed* | VER-008 |
| FX-C4 | T2: A4 on S-2, with no A5 anywhere | Independent act | Performed on its own evidence | VER-008 |
| FX-C5 | A5 checkpoint, reached-when (c) *PR-2 queued* (T10); subject PR-2 change items; T11 accept item 1, reject item 2 | Mixed | *Resolved negatively*, **partial** annotation (item 1 A5) per WD §4.3.7; *on mixed decision* path if declared | VER-008 |
| FX-C6 | A6 checkpoint; the person declines | Act-declined | *Resolved negatively*; no A6; negative path | VER-008 |
| FX-C6b | A12 checkpoint; the person declines | Act-declined | *Resolved negatively* | VER-008 |
| FX-C7 | Checkpoint reached-when (c) *queued*; run stopped before any proposal | Never met | *Not reached* at run end | VER-008 |
| FX-C7b | Checkpoint reached and waiting; run ended; the person performs the act afterwards | Post-run act | Run-ended event with *waiting*. The later act is recorded and relayed against the subject; the ended run's disposition is unchanged | VER-008 |
| FX-C8 | Checkpoint A4, reached-when (a) before dispatch of OP-C5; subject class "targets of the held call" | Kind (a) | Call held. Subject = S-3 by its subject content identity in the relied-on read B2. After host-captured A4 on that content, the same held call is dispatched | VER-008 |
| FX-C9 | A5 checkpoint on OP-C4's result; grant effective direct; direct requested | Constraint | Dispatch carries the governing checkpoint constraint; *not permitted* naming it. **AWAITING INPUT** (R2-12; §13 Q-1) | VER-008 |
| FX-C10 | Agent-authored A9 of an A4, with no capture evidence | Record only | Checkpoint stays waiting | VER-008 |
| FX-C11 | A12 checkpoint, subject class grant setting; T15 A12 performed; later A12 on an overlapping scope | Supersession | *Performed*; later shown as superseded, not lapsed (R2-7 PROPOSED). A refused-A12 variant is held for W7 | VER-008 |
| FX-C12 | FX-C5 variant: item 2 refused stale before a decision; item 1 A5 | Item left | Item 2 left with its event; *performed* over a reduced subject, **never** "all accepted" | VER-008 |
| FX-C13 | Declaration with required act A10 (recognized, not allowed); a declaration with an unrecognized act name | Invalid / not established | Checkpoint reported *invalid* / *not established*; not evaluated (R2-10) | VER-008 |

## 12. Evidence standing labels

| LOOP label | C/P label (IR1-B B-m5; mapping owned by C) | Can support |
|---|---|---|
| CONTRACT-REVIEWED | illustrative | Completeness of the expectation |
| FIXTURE-EXECUTED | test-double | The expectation on that double only |
| HOST-OBSERVED | actual host | That candidate only |
| NOT-OBSERVED | (none) | Nothing; recorded as a gap |
| HELD | (case state) | Nothing. A decision is pending (e.g. FX-NP1, R2-9) |

Owner-reported construction (DEP-001) is none of these.

## 13. Relay questions prepared (for W9; not delivery)

These are prepared for App-manager preparation and human relay to the SWBPIPE
owner (DEP-001; DEP-05-01-021). Writing them is not delivery, agreement or
adoption.

- **Q-1 (R2-12).** Can your validation/application route receive a
  per-request **governing checkpoint constraint** and resolve *propose* from
  it? Or does the host evaluate its own copy of the selected workflow's
  declaration? What evidence will show which? An omitted constraint is
  indistinguishable from none.
- **Q-2 (R2-20; X-17).** For each act your act facility captures (A4, A5,
  A10, A12, and A6/A7 where offered), does it expose a stable
  **capture-evidence reference**? The reference would cite act identity,
  actor, act kind, bound content identity and time. Without one, no
  host-content checkpoint can become *performed*.
- **Q-3 (R2-14).** Does an applied outcome identify the created and changed
  objects, with their post-application subject content identities?
- **Q-4 (R2-20; X-18).** Can the host loop record, per turn, the source
  identity and content identity (with method designation) of each guidance
  input it supplies? Where it cannot, the record says *unknown*.
- **Q-5 (R2-2).** Does the host offer any faithful-record operation? If so,
  does it meet the four R2-2 conditions?
- **Q-6 (R2-13).** Does the host de-duplicate by proposal identity before the
  basis check, and compare per-item target subject content identities for
  staleness?
- **Q-7 (R2-4).** Does the host report *not exposed on this surface* from its
  exposure element? Which entries does it supply to the embedded surface?

## UNRESOLVED

| Item | Owner | Point of need | Effect |
|---|---|---|---|
| OI-013 loop placement, parsing, persistence, panel assembly | Shared contract owner with SWB implementation owner | Before shared/host implementation boundary contracts | Outcomes only |
| OI-014 shared placement | App/shared contract owners | Before structural/production allocation | No common loop |
| DEP-05-01-024 model interface and representation | UNKNOWN supplier; App/shared embedded-integration owner receives or agrees | At fixture/conformance use | §4 semantic; MC-6, MC-8 held; no fixture executable |
| DEP-001 host evidence, including Q-1…Q-7 | SWBPIPE outside implementation session | Before corresponding integration/examination and fallback-replacement decision | All host conformance NOT-OBSERVED; FX-C9 AWAITING INPUT |
| OI-021 first connected operation; operation-specific reserved additions; OP-C11 class | Owner via outside SWB session and App/shared owner | Before connected SoW and execution | FX-NP1 HELD; fixtures invented |
| Consequence vocabulary | DEL-04-01 with host policy owner | Before class assignment | Classes as supplied |
| WD §4.3.7 confirmation; resumption after run end; refused A12 at a checkpoint; re-hold after post-resume lapse | DEL-02-03 (W7) | W7 | C-4, C-7, C-8 and FX-C7b relay only |
| C U-C5 findings location | DEL-03-01 with host owner | Before E-5 route (b) is used | E-5 conditional |
| C U-C3 / R2-13 staleness rule host confirmation | Host owner with DEL-03-01/03-02 | Before FX-D2/FX-O1 execution | §6.3 R-c meaning only |
| C U-C6 entry-version mismatch | Host input | Before FX-D-series execution | O-3 |
| U-P1 / TBD-002 resubmission mechanics; U-P9 sibling grouping | DEL-03-02 with DEL-05-01 and host owner | Before FX-O1 / FX-M8 | Meaning only |
| N-OPEN-1/2/3 endpoints, cloud destinations, tool traffic | App/shared embedded-integration owner with SWBPIPE owner; owner if V4-HOST-02 is affected | Before endpoint cases are finalized | MS-11 held |
| T-OPEN-1 valid siblings beside a malformed call | This owner with DEL-03-02 and host owner | Before FX-M8 | Proposed |
| R-OPEN-1 quantitative responsiveness | Owner, if wanted | Before any numeric criterion | None set |
| Seat role mapping (U-09) | DEL-02-01 with SWB owner and DEL-02-04 | Before record fixtures | *unknown* allowed |
| Holding library (U-24) | DEL-02-01 / DEL-02-03 | W7 | PROPOSED carriage |
| R2-n sibling v0.3 elements (five values, constraint element, resulting objects, OP-C10/C11, exposure assumption, policy-default state, act-declined name, subject classes) | Respective owners | V2 / IR2 | Adopted here; confirm against sibling v0.3 text |

## Verification cases

These are designed, not run.

| Case | Procedure | Expected result | Serves |
|---|---|---|---|
| VC-01 | Trace §5.1 and MS-01…MS-10 to V4-HOST-01/02 and V4-ARC-11 | Every rule traced; MS-11 held; host observations NOT-OBSERVED | VER-001 |
| VC-02 | Inspect N-3/N-6/N-7 and MS-03/06/07/08 against V4-ARC-12 | Native layer is the enforcement point; labels applied | VER-002 |
| VC-03 | Review §1, §2 and §4 | Four subjects; the App path is distinct (Responses API unobserved); DEP-05-01-024 open; Pi excluded; D3 attribution per R2-11 | VER-003 |
| VC-04 | Review §6 and the FX-V/S/D/U/NP fixtures against C §4.1 and P §9 (v0.3 when supplied) | V-2 split holds; "not exposed" only host-reported; five class values; O-1…O-6 hold; FX-D1/D1b distinguish invalid from unavailable; FX-D2 is a revision within g1 | VER-004 |
| VC-05 | Exercise FX-M, FX-V1, FX-U1 and FX-O1 against a test double once DEP-05-01-024 and C are supplied | Zero dispatch for rejected calls; de-duplication before the basis check; class 4 reporter is the loop | VER-005 |
| VC-06 | Review §8. On host observations, check candidate, configuration and placement | No threshold; results limited to observed scenarios | VER-006 |
| VC-07 | Compare §10 with SoW CLM-001/002/003, REQ-006, OI-013/014, DEP-001 and the Clarification | Every excluded act has its owner; no common construction allocated | VER-007 |
| VC-08 | Review §2.3, §2.4, §9 and FX-C1…C13, FX-R1/R2 and FX-UNDO against the ACT, WD, P and AS versions (v0.3 when supplied) and W7 | Declared subject class bound; reached-when observed-only; run-end *waiting* and post-run acts per R2-20; act-declined for A4/A6/A7/A12; lapse per R2-19; mixed items per WD §4.3.7; A12 supersession; A8 offered only; constraint carried | VER-008 |
| VC-09 | Audit every claim for a §12 label and an exact identity. Audit every R2-n element for V2/IR2 confirmation | No HOST-OBSERVED claim without candidate evidence; HELD cases not counted as passes | VER-009 |
