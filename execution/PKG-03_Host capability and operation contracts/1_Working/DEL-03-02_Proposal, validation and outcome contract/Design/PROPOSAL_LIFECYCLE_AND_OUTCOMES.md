# Proposal, validation and outcome contract
- Contribution: DEL-03-02/P-v0.2
- Status: DRAFT DEFINITION — proposed, unsupplied, not implemented, not accepted
- Serves: OUT-001 (proposal, relied-on basis, origin, change-item content identity and outcome schema meaning), OUT-002 (lifecycle, one route, actor parity, host ownership and receiving interfaces), OUT-003 (designed contract fixtures); REQ-001–REQ-013; AC-001–AC-014; VER-001–VER-014
- Basis: repo 6e18505e3; ScopeOfWork.md sha256 42328987c71dd243323805faf2634067cca0113b81ca93d4d129193b2a71128a; `P/docs/HOST_INTEGRATION.md` (sha256 08c8fc7d…60da) §1, §§3–5 (V4-HI-11, V4-HI-20–25, V4-HI-30–33), §6 V4-HI-40–42, §7 V4-HI-50–52, §9 V4-HI-70–71, §10, §11; `P/docs/PRD.md` V4-PAR-04, V4-AUT-01–05, V4-REC-01, V4-CST-05/06, §9 OQ-02/OQ-11; `P/docs/ARCHITECTURE.md` V4-ARC-20; `P/docs/EXAMINATION.md` V4-EXM-20/22/25; DECISION_BRIEF #d2/#d3/#d4/#d5; SCC-CASE-002 Case_Datasheet rows M1-P, M3-CP (sha256 6acdc6c4…a71a6); owner decision `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` (OWNER_DECISIONS.md sha256 f3f8e5f3…81f2e) D2/D3; R1_RESOLUTIONS.md (sha256 2f9c7e72…7ec4) R-1–R-9; comparisons V1-A (01811533…4c09), V1-B (09eebfe0…1cae), V1-C (8d46258a…94a6)
- Consumed inputs: DEL-03-01/C-v0.2 (co-revised in this run: operation identity/version, input/effects/errors with effect statements, §4.1 non-success results, read basis with method designation, subject content identities, relied-on basis reference, exposure, shared fixture catalogue FX-PIPE-01 — `CATALOG_AND_READ_BASIS.md` §§3–5, §10); DEL-04-01 meaning as fixed by R1_RESOLUTIONS R-1 (A1–A14), R-2 (D2/D3), R-3 (treatment → outcome map), R-4 (labels), R-5 (checkpoints) — DEL-04-01/ACT-POLICY-v0.2 not read (concurrent repair), to be reconciled at V2; DEL-04-02 grant display states and settings references as fixed by R-8, by R1 meaning; DEL-02-01 workflow identity {kind, origin, source root, name, revision} + derived-from as fixed by R-9, by R1 meaning; host facilities (route, views, receipts, act capture): not supplied (DEP-03-02-023)
- Receivers: DEL-04-02 (OUT-001, OUT-002; REQ-003–005; VER-003–005) via DEP-03-02-018; DEL-04-03 (OUT-001, OUT-002, OUT-004; REQ-002, REQ-003, REQ-005; VER-001, VER-004, VER-006) via DEP-03-02-019; DEL-03-03 (OUT-001, OUT-003; REQ-001, REQ-004; VER-001, VER-004) via DEP-03-02-020; DEL-05-01 (OUT-001, OUT-003; REQ-003, REQ-007; VER-008); DEL-05-02 (OUT-001, OUT-003; REQ-001–003; VER-001–003); DEL-09-09 (OUT-001; REQ-001, REQ-004; VER-001, VER-004) via DEP-03-02-022; DEL-03-01 (OUT-001, OUT-003; REQ-001, REQ-004; VER-004) as the M3-CP return (DEP-03-01-026); DEL-03-04 responsibility map via DEP-03-02-021; DEL-02-01 / DEL-02-03 (acceptance-checkpoint constraint, item dispositions); external host proposal-view receiving via DEP-03-02-024

## 0. How to read this definition

This is the 60% semantic definition of how a change, by a person or an
agent, is proposed or applied through a host, and how its outcome is
reported. Element names are **semantic labels, not wire names**. No
proposal-identity representation, content-identity method, schema encoding,
duplicate-effect mechanism, outcome-recovery mechanism, storage engine,
transport field, retry budget or retention interval is selected (TBD-002;
DEP-03-02-026), and no component placement (OI-014; DEP-03-02-025). Unruled
policy appears only as `UNRESOLVED{OI-nnn}`. **DERIVED** and **INTEGRATION**
markings follow R1_RESOLUTIONS.

§9 is the **canonical outcome taxonomy** for proposals and operations
(R-7). DEL-04-03, DEL-05-01 and DEL-05-02 adopt it and C-v0.2 §4.1
unchanged. Fixtures use the shared catalogue FX-PIPE-01 (C-v0.2 §10); step
labels T1… refer to its timeline.

Settled distinctions relied on (cited, not re-decided):

| Id | Settled distinction | Source |
|---|---|---|
| S-P1 | Every change passes through the host's one validation and application route; no second route for agents | V4-HI-20; V4-PAR-04 |
| S-P2 | An agent's change carries origin (author type, conversation, workflow run) and the basis it relied on | V4-HI-21 |
| S-P3 | Under granted autonomy the agent may apply directly: origin-marked, undoable, checkable later | V4-HI-22; V4-AUT-01 |
| S-P4 | Otherwise a proposal: drafted → validated → queued → accepted → applied (receipt), with rejected / withdrawn / stale, and outcome unknown when unobservable | V4-HI-23 |
| S-P5 | Stale is refused with reason and may be re-drafted on the current basis; later selection never retargets; submitting the same proposal twice has one effect | V4-HI-23 |
| S-P6 | Host views show old and new values, affected objects and why | V4-HI-24 |
| S-P7 | `success` means it ran, never that a person accepted anything; a submitted proposal reports queued until the host records acceptance and application | V4-HI-25 |
| S-P8 | Queued ≠ applied; applied edit ≠ engineering approval; a receipt records the operation outcome, not an act of acceptance | #d3 |
| S-P9 | Acceptance of a proposed edit is not engineering approval; the interface says "accept", never "approve", for proposals | V4-HI-33 |
| S-P10 | Agents never record a human act as performed when it was not; faithful recording (A9) is a conformant record shape | V4-HI-31; V4-AUT-03; R-5 |
| S-P11 | A human act binds to content and lapses visibly when content changes | V4-HI-32 |
| S-P12 | Domain truth and validation stay in the host; Chirality never presents agent output as the host's accepted result | V4-REC-01; V4-CST-05 |
| S-P13 | Workflow checkpoints override autonomy; no grant widens past a reserved act or a declared checkpoint | V4-HI-42; D2 |
| S-P14 | Reserved to the person: A4 mark checked; A5 accept wherever the active autonomy requires a proposal; A6 approve; A7 rely; A12 set grant; A13 enable external access. A10 reject is reserved wherever A5 is (DERIVED). The host names and enforces its own list; SWBPIPE adoption is not evidenced | D2; R-1; V4-HI-30; DEP-001 |
| S-P15 | App routine tool permission/sandbox (A14) is the user's own Codex setting and governs tool execution only; hosts have no classifier permission mode; the SWB default proposal mode applies | D3; V4-HI-41 |

## 1. Host authority map (REQ-002, REQ-013; VER-003, VER-014)

| Facility | Owner | This contract's role |
|---|---|---|
| Domain objects, store and truth | Host owner (SWBPIPE outside session) | None; reads through DEL-03-01 |
| Validation, treatment resolution and the one application route | Host owner | Defines the receiving meaning of its outcomes |
| Receipts, origin marks, undo | Host owner | Refers to them; never manufactures one |
| Proposal views (old/new/objects/reason) | Host owner | Supplies the information the views need (§8; DEP-03-02-024) |
| Offering, capturing, recording and presenting human acts | Host owner (facility); the person (the act) | Consumes recorded acts as evidence; never creates one |
| Catalog, read basis, content identities | DEL-03-01 | Consumed (§3.2) |
| Act names, adopted class records, treatment → outcome map | DEL-04-01 (R-1–R-3); residual policy: owner with App/SWB contract owners | Consumed |
| Grant display states and settings versions | DEL-04-02 (R-8) | Supplied: origin and direct-autonomy semantics; consumes settings references |
| Human-act and run-record format | DEL-04-03 | Supplied: outcomes, receipt links, change-item content identity |
| Workflow identity; checkpoint declaration | DEL-02-01 (R-9, R-5) | Consumed in origin; §4.4 constraint supplied |
| External receiving adapter | DEL-03-03 (host owns endpoint) | Supplied: this same contract |
| Integrated host guide | DEL-03-04 | Supplied: §1 and §13 |
| Joined external witness, extension trace | DEL-09-09 | Supplied: fixtures and outcome expectations |

A host-accepted result exists only where the host has recorded the relevant
act. Agent output without that record retains its actual standing
(*drafted*, *queued*, *finding*), never *accepted* (SOW-091). A host refusal
is never a person's rejection (§4.1).

## 2. One route and actor parity (REQ-001; SOW-070)

- Person, embedded agent and external agent submit changes to the **same**
  host validation/application route. The channel is attribution (§3.3), never
  a route selector.
- **Treatment is resolved on the host route** at validation and again at
  application (R-3 point 1). The loop (DEL-05-01) and the external adapter
  (DEL-03-03) relay the actor's intent — *propose* or *apply directly* — and
  do not decide treatment.
- **Equivalence rule.** For equivalent operation identity/version, arguments,
  relied-on basis and applicable authority, every channel receives the same
  outcome and the same error meaning (identity and text).
- **Permitted difference is authority only** (grant, reserved acts, class).
  It is reported as *not permitted* naming the governing treatment and policy
  record (C-v0.2 §3.1), never as a different validation error. Per the R-3
  map:
  - a request to apply directly without an *effective direct* treatment →
    *not permitted*; it is never silently converted into a proposal
    (INTEGRATION);
  - a request to perform a reserved act (S-P14) as the person → *not
    permitted*, with an A8 *request* offered;
  - a class with *policy basis pending* (OI-021) → direct *not permitted*,
    propose available (INTEGRATION).
- A denial by the App user's Codex tool permission (A14) happens App-side
  before any host request and is not a host outcome (S-P15).
- No fixture or adapter may define an alternate agent mutation path, bypass
  validation, or apply outside the host route (AC-002).
- Person-origin changes use the same route and yield the same basis check
  and outcome meanings; whether a person's direct edit is represented as a
  proposal is host practice.

## 3. Change request elements (OUT-001; REQ-003; SOW-170)

### 3.1 Identities and the acceptance unit

| Semantic element | Meaning |
|---|---|
| Proposal identity | Stable identity of *this* proposal from drafting onward; the unit for one-effect (§7). A **retry** (resubmission after a lost acknowledgment or *outcome unknown*) keeps the same identity and unchanged content (R-7; V1-C AB-05). A **re-draft** receives a new identity (§5) |
| Lineage | For a re-draft: the identity of the proposal it replaces and why (e.g. stale) |
| Change items | One or more items, each with its own item identity within the proposal |
| **Change-item content identity** | An identity of the item's content: operation identity and version, bound targets, old values, new values and the relied-on basis. Method unselected; carries a method designation (C-v0.2 §5.1) (R-6; V1-B D-01) |

Rules (R-6):

1. **Acceptance unit = change item.** Row-by-row acceptance is one A5 per
   item. Batch or multi-row acceptance is one A5 act listing several items,
   each bound to its own change-item content identity, with per-item lapse
   (V4-HI-41).
2. **A5 and A10 bind to the change-item content identity**, not to model
   rows. Any change to an item's content (including a re-derived old value)
   is a different item content; an acceptance never carries to it.
3. **Applying the accepted item does not lapse the acceptance.** The item's
   content identity is unchanged by its own application.
4. **A host view row** presents one or more change items (e.g. a new support
   row plus its stiffness). The row is presentation; decisions are per item
   (V1-B D-10).
5. **Sibling drafts (proposed, V1-C AB-13).** Several tool calls in one model
   response that each draft changes form separate proposals unless a draft
   explicitly names the proposal it extends. Grouping mechanics are
   DEL-05-01's with this contract (U-P9).

### 3.2 Consumed catalog meaning (from DEL-03-01/C-v0.2)

| Element | From C | Rule here |
|---|---|---|
| Operation identity and version | C §3 #1 | The version the request was prepared for; not re-interpreted |
| Arguments | C §3 #3 | Checked against the catalog input schema before host domain validation (DEL-05-01 REQ-003) |
| Bound targets / affected objects | C §3 #3, #5 | Fixed at drafting (§6) |
| **Relied-on basis reference** | C §5.4 | The basis descriptor(s) — workspace identity, generation, model revision, canonical content identity, method designation — of the read(s) actually relied on; carried unchanged to every outcome; never replaced by a queue-time or application-time basis, which may be recorded as a separate element |
| Subject content identities of affected objects | C §5.3 | Used for the stale check where the host's rule is content-based (U-C3); old values are as of the relied-on basis |
| Errors, §4.1 results, exposure | C §3 #7, §4.1, #9 | Reused as outcome reasons (§9); no separate vocabulary |

This contract defines no separate basis authority (CLM-003).

### 3.3 Origin and attribution

| Semantic element | Meaning | Source |
|---|---|---|
| Author type | person or agent | V4-HI-21 |
| Author identity | The person, or the agent seat instance | V4-HI-21; V4-HOST-05 |
| Seat role meaning | The role meaning in force for the seat, or *unknown* if it cannot be determined (V1-C AB-02) | DEL-02-01 SEAT-1 |
| Channel | host interface, embedded agent, external agent | V4-PAR-02 (attribution only) |
| Conversation | Conversation the agent change came from | V4-HI-21 |
| Workflow identity | {kind, origin, source root, name, revision} plus derived-from where adapted. An unadapted carried workflow keeps its original origin; host adaptation creates a new identity with host origin and derived-from. "App-origin" is not an origin class (R-9; V1-C D-10) | DEL-02-01 §6.1 |
| Workflow run identity | The run within that workflow | V4-HI-21; V4-HI-70 |
| Standing at drafting | DEL-04-02 grant display state (effective · requested by agent · set by person, not yet confirmed · unconfirmed · not set · refused) and treatment for the operation class, as known when drafted | R-8; R-3 point 6 |
| Settings reference at route decision | The DEL-04-02 settings version identity used when the host resolved treatment at validation | R-8; V1-B D-07 |
| Settings reference at application | The settings version in force at application, **host-reported**; otherwise *unconfirmed* | R-8; V1-B D-07 |
| Reason | Why the change is proposed, in the proposer's words | V4-HI-24 |

Origin is preserved through submission, every lifecycle transition and
outcome reporting. Every dispatch carries origin, seat role meaning and the
grant in force (R-7). The App-side request origin (all elements above) is
recorded by DEL-04-03; the **host origin mark** is linked, not copied, and a
mismatch between the two is an evidence limit (V4-HI-71; V1-B D-17).

### 3.4 Change item content

| Semantic element | Meaning |
|---|---|
| Item identity | Identity within the proposal |
| Operation | Catalog operation identity and version (C §3 #1) |
| Affected object | Identity of the object changed (bound target) |
| Attribute | What of the object changes (or *created* / *removed*) |
| Old value | Value as of the relied-on basis |
| New value | Proposed value |
| Item reason | Optional item-specific reason |
| Change-item content identity | §3.1 |

## 4. Lifecycle (REQ-004, REQ-005, REQ-011; SOW-171, SOW-172, SOW-178)

### 4.1 Proposal states (outside an effective direct treatment)

```text
drafted ─► validated ─► queued ─► accepted ─► applied (receipt)
   │           │           ├─► rejected   (A10, the person)
   │           │           ├─► withdrawn  (A11, the proposer)
   │           │           └─► refused — stale  (relied-on basis no longer holds)
   │           │  accepted ─► refused — stale (basis fails before application; §4.2)
   │           │  accepted ─► application error (effect: none | partial | unknown)
   └─► refused — invalid / stale / not permitted  (before queueing; stays drafted)
overlay: any submitted step whose outcome cannot be observed ─► outcome unknown (observer-attributed)
```

States and dispositions are **per change item**; the proposal state is
derived (§4.3).

| State / disposition | Meaning | Entered by (actor) | Evidence |
|---|---|---|---|
| drafted | Proposal composed with operation, arguments, targets, relied-on basis, origin, items | Proposer (A1) | Proposal content |
| validated | Host validation found it valid against the relied-on basis; treatment resolved | Host | Host validation outcome with treatment and settings reference |
| queued | Submitted and held by the host for the person's decision | Host (on proposer's submission) | Host queue acknowledgment |
| accepted | The person accepted the item ("accept", S-P9) | **The person (A5)**; host captures | Host-captured A5 bound to the change-item content identity |
| applied (receipt) | The host applied the accepted item through its one route | Host | Applied-outcome association (§9) incl. **receipt** reference |
| rejected | The person declined the item. **Only A10**; a person removing another's proposal is A10 (R-1) | **The person (A10)**; host captures | Host-captured A10 |
| withdrawn | The proposer withdrew its own proposal before application | **The proposer (A11)** | Host record |
| refused — stale / invalid / not permitted | Host refused on its route; not a person's act (V1-A D-16) | Host | Refusal with reason, evaluated basis; for stale both bases |
| application error | A declared error raised during application | Host | Error identity (C §3 #7) and effect statement: *none*, *partial* (with receipt references), or *unknown* (→ overlay) (V1-B D-05) |
| outcome unknown (overlay) | Result of a sent step cannot be observed | **The observer that lost observation** — loop, App adapter or host — attributed to it (R-7; V1-C D-12) | Absence of observation; last observed state |

Reporting rules:

1. A submitted proposal reports **queued** until the host records acceptance
   and application (S-P7). A successful *submit* is reported as queued, never
   as accepted or applied.
2. **Accepted alone is not applied.** *Applied* is reported only with a host
   receipt reference (REQ-011).
3. **Outcome unknown** is reported whenever the outcome cannot be observed,
   including when execution may have occurred; it is never inferred to be
   applied, failed, rejected or accepted. A later observation is reported
   separately with its own basis and does not back-fill the earlier report.
   Recovery mechanics are unselected (TBD-002).
4. Accepted, rejected and withdrawn are always relayed with their actor
   (A5/A10/A11) (R-7).

### 4.2 Transitions beyond the drawn source lifecycle

| Case | Contract handling (v0.2) | Status |
|---|---|---|
| Validation fails before queueing | *refused — invalid* with the catalog error; stays *drafted*; no queue entry | Proposed; host confirmation U-P4 |
| Stale detected at validation | *refused — stale* (§5) | Follows HI §10 item 3 |
| Basis no longer holds after *accepted*, before *applied* (was U-P3) | *refused — stale* at application under the stale rule (§5), **not** model-row lapse (R-6). The recorded A5 stays bound to its unchanged item content and is not lapsed; the item is not applied and a re-draft is a new item content, so the A5 does not carry | R-6 (INTEGRATION); host behavior evidence DEP-001 |
| Withdrawal before queueing | Discarding a draft; no host record required | Proposed |
| Treatment narrowed while in flight | Already-queued proposal unaffected; a not-yet-applied operation is re-resolved at application (R-3 point 6) | INTEGRATION; host enforcement DEP-001 |
| Treatment widened while in flight | Never converts a queued proposal into direct application or an acceptance (R-3 point 7) | INTEGRATION |

### 4.3 Item-level acceptance and derived proposal state (V4-HI-41; V4-EXM-20)

- Each change item carries its own disposition.
- The proposal's reported state is derived and never stronger than its
  items, e.g. "PR-2: item 1 accepted and applied (RC-1); item 2 rejected".
- Whether accepted items are applied separately or in one host application
  is a host input (U-P7). One-effect (§7) holds per item and per proposal.
- For a checkpoint requiring A5 on a proposal (DEL-02-01), this contract
  supplies per-item dispositions and an **all items decided** indication. How
  mixed item decisions map to checkpoint dispositions (waiting · performed ·
  resolved negatively · …, R-5) is owned by DEL-02-01 with DEL-02-03 (V1-C
  AB-01).

### 4.4 Direct-autonomy branch (V4-HI-22; S-P3)

Entry condition (V1-B D-06; R-8): the DEL-04-02 display state for the
operation class and scope is **effective** with treatment **direct**, as
resolved by the host at validation. Every other state (requested by agent;
set by person, not yet confirmed; unconfirmed; not set; refused; class
*policy basis pending*) takes the proposal route, and a direct request is
*not permitted* (§2). A person-set grant requires A12 act evidence (D2e).

```text
drafted ─► validated (treatment: direct) ─► applied (receipt, origin mark, undo route, later-check route)
                ├─► refused — invalid | stale | not permitted
                └─► application error (effect statement)
overlay: unobservable ─► outcome unknown (observer-attributed)
```

- No *queued* or *accepted* state exists and **no acceptance is recorded or
  implied**. Reports never say "accepted" for a direct application.
- The application carries origin (§3.3) including both settings references
  (at route decision; at application, host-reported or *unconfirmed*),
  relied-on basis, receipt, origin mark, undo route and later-check route
  (access for later examination or checking; implies no act, R-4). These are
  abstract host contributions, host-owned.
- The basis check applies exactly as for proposals.
- **Acceptance checkpoint forces proposal (R-5, DERIVED from V4-HI-42 + D2b).**
  If a declared workflow checkpoint requires A5 on an operation's result,
  that operation's treatment is *propose* regardless of the grant. The
  change is drafted as a proposal whose items are the checkpoint's bound
  subject; the direct branch is not entered. A checkpoint requiring A4 on
  applied rows does not force proposal; the run holds after application for
  the A4 (V1-C D-07).
- Any other declared checkpoint holds the run for the person's act (S-P13).

### 4.5 Undo (V1-B D-18)

- An undo is a **change through the one route** (§2): its own origin, its own
  relied-on basis and basis check, its own outcome, and its own receipt.
- "Undone" is reported as *applied (receipt)* of the undo change with a
  relation **reverses ⟨receipt⟩**. It may equally be *refused*, meet an
  *application error* or be *outcome unknown*.
- Undo does not erase or lapse an earlier act record; the reversed item's
  standing shows "applied, then reversed by ⟨receipt⟩". Whether the undo
  itself requires a proposal follows its operation's treatment. Undo route
  availability and scope are host-owned (U-P8).

## 5. Stale refusal, re-draft and retry (REQ-006; SOW-173)

- **Trigger.** The relied-on basis (§3.2) no longer holds when the host checks
  it (validation, queue, or application). What counts as "no longer holds" —
  any model revision, or a change to relied-on content judged by subject
  content identities — is **U-C3** (shared with DEL-03-01). A generation
  change makes revision comparison impossible and is handled under U-C2.
- **Refusal content.** *refused — stale*; reason (what changed, where known);
  **relied-on basis** (unchanged); **current basis** (evaluated basis);
  affected items.
- **No silent refresh.** No host or consumer rewrites the relied-on basis and
  proceeds.
- **Re-draft.** Only as a **separately identified** proposal: new proposal
  identity, lineage to the stale one, a new relied-on basis from a new read,
  re-derived old values, new change-item content identities, fresh
  validation. No acceptance carries over.
- **Retry is not re-draft.** A retry resubmits the same proposal identity and
  content without a new read; if its basis no longer holds it is refused
  stale like any submission.

## 6. No retargeting (REQ-007; SOW-174)

- Bound targets and affected objects are fixed at drafting from explicit
  target identification (C §4.3), including a person's selection resolved at
  drafting.
- A later selection change in any surface never changes a proposal's bound
  targets, items or reported affected objects. A change of intended target is
  a new proposal.

## 7. Repeated submission → one effect (REQ-008; SOW-175)

- **Obligation.** Submitting the same proposal identity more than once,
  including a retry after a lost acknowledgment, produces at most one
  application effect per item. This is a **host obligation to be evidenced**
  (DEP-001), not a recorded fact (R-7).
- **Recording.** Each submission is recorded separately, referencing the same
  proposal identity, with only the effects actually observed (the same
  receipt, two receipts, or unknown) (R-7; V1-B D-09).
- **Testable form.** Effect count observed in the host model/receipts for the
  proposal identity equals 0 or 1 per item; a repeat reports the existing
  state (queued, applied with the *same* receipt, etc.).
- **Mechanism unselected** (TBD-002). Shared validation or transport
  deduplication is not evidence of a one-domain-effect outcome (V4-EXM-25).
- **Unobservable repeat.** Report *outcome unknown* (observer-attributed); do
  not infer one effect or zero.
- A re-draft is a different proposal and not a repeat.

## 8. Host proposal-view information (REQ-009; SOW-176)

The host shows, in its own tables/views (V4-HI-24; V4-HOST-04: no
agent-private surface), for each proposal and item:

| Information | Supplied by this contract | Presented by |
|---|---|---|
| Old value (as of relied-on basis) | §3.4 | Host |
| New value | §3.4 | Host |
| Affected objects; which items a view row presents | §3.4; §3.1 rule 4 | Host |
| Why (reason) | §3.3 / §3.4 | Host |
| Origin (author, seat role, conversation, workflow identity and run) | §3.3 | Host |
| Current disposition per item, with actor for A5/A10/A11 | §4 | Host |
| Stale indication with current value where it differs | §5 | Host |
| Lineage for a re-draft | §3.1 | Host |

Presentation, receipts and the acceptance control are host-owned
(DEP-03-02-024). The control says "accept", never "approve" (S-P9). A live UI
witness is host-owned evidence.

## 9. Canonical outcome taxonomy (R-7; REQ-005, REQ-010, REQ-011; SOW-172, SOW-177, SOW-178)

Every non-success outcome carries the **evaluated basis** where the host
evaluated one (V1-B D-21). Outcomes apply per change item where items exist.

| Outcome | Meaning | Carries | Establishes | Does **not** establish |
|---|---|---|---|---|
| unavailable | Catalog precondition failed (C §4.1) | Reason, failed precondition, evaluated basis | Nothing executed | — |
| not permitted | Treatment forbids the requested mode (R-3) | Governing treatment, policy record, evaluated basis; A8 request for reserved acts | Nothing executed | — |
| channel not enabled | External access off (V4-HI-52); A13 not performed | Channel state | Nothing evaluated | — |
| not exposed on this surface | Entry not exposed on the acting surface (C §3 #9) | Entry, surface | Nothing evaluated | — |
| refused — invalid | Host validation refused with a catalog error | Error identity, evaluated basis | Nothing applied | — |
| refused — stale | Relied-on basis no longer holds | Reason, relied-on basis, current (evaluated) basis | Nothing applied | — |
| queued | Host holds the item for the person's decision | Host acknowledgment | Submission received | Acceptance, application |
| accepted | Host captured the person's A5 on the item | Actor, act reference, item content identity | That act by that person on that item content | Application, checking, approval, reliance |
| rejected | Host captured the person's A10 | Actor, act reference | That rejection | — |
| withdrawn | Proposer withdrew (A11) | Actor | That withdrawal | — |
| applied (receipt) | Host applied the item. **Applied-outcome association**: proposal/item identity, relied-on basis, receipt reference, resulting revision; branch *after acceptance* or *direct under grant* (with settings references) (V1-B D-22) | Association | Execution and resulting revision | Acceptance (direct branch), checking, approval, reliance |
| application error | Declared error during application | Error identity; effect *none* / *partial* (receipt references) / *unknown* | What the effect statement states | Any unstated effect |
| outcome unknown | Result unobservable | Observer, last observed state | Only the last observed state | Applied, failed, accepted or rejected |
| error (read/examination) | Declared error in a non-mutating operation (C §4.1) | Error identity, evaluated basis | — | — |
| success (operation) | The operation ran (S-P7) | Result | Execution | Any human act |

Whether the host receipt *itself* carries the relied-on basis is a host
observation recorded at comparison (C-v0.2 VC-C-04), not assumed.

## 10. Execution versus human acts (REQ-010, REQ-012; SOW-177; #d3)

Canonical act names (R-1).

| Subject | Actor | Evidence required | Never inferred from |
|---|---|---|---|
| A1 propose (draft/submit) | Agent or person | Proposal content; host queue acknowledgment | — |
| A2 apply (validation/application) | Host route on the actor's request | Validation outcome; receipt | — |
| Direct application under grant | Agent within an effective direct treatment | Receipt, origin mark, settings references | — and it implies no A5 |
| A3 examine | Agent | Findings by reference | — and it is never A4 |
| A4 mark checked (reserved) | The person | Host-captured act bound to subject content identity | Findings, success, acceptance |
| A5 accept (reserved where a proposal is required) | The person | Host-captured act bound to change-item content identity | Success, submit, queue, application, agent report |
| A10 reject (reserved wherever A5 is) | The person | Host-captured act | Absence of acceptance; host refusal |
| A11 withdraw | The proposer | Host record | — |
| A6 approve (reserved) | The person/accountable professional | Its own record | A5 (S-P9) |
| A7 rely (reserved) | Accountable professional | Its own record | Any of the above |
| A8 request | Agent | Request record | — it establishes nothing |
| A9 record (faithful recording) | Recorder ≠ decision actor | Reference to the capturing surface's evidence of the act | — it never satisfies a checkpoint by itself (R-5) |
| A12 set grant (reserved) | The person | Host/App control act evidence | Agent request (A8) |
| A14 answer tool permission | Person or the user's own Codex mode | App-side harness record | — never a professional act or A5 |

Rules: one act never establishes another; no synthetic prerequisite between
acts is introduced; checkpoint satisfaction requires attributable evidence
from the capturing surface — the host's act facility for acts on host content
(R-5). Whether a particular host requires capture by its own facility is a
host question (DEP-001). Operation-specific reserved additions await
`UNRESOLVED{OI-021}`.

## 11. M3-CP read-then-action comparison design (return to DEL-03-01)

This is the distinct return retained from SCC-CASE-004 (CASE-002 M3-CP;
DEP-03-01-026). It supplies DEL-03-01 with designed refusal/application
behavior and a comparison plan; DEL-03-01 compares basis elements only.
Steps are the FX-PIPE-01 timeline (C-v0.2 §10.3).

| Step | Action | Basis observed | Proposal reference | Expected P behavior |
|---|---|---|---|---|
| T3 | Agent reads supports table (OP-C1) | B1 = FX-W1/g1/r12/⟨v12⟩/⟨m-fx⟩ | — | — |
| T5 | Agent drafts PR-1: item 1 add support (OP-C4); item 2 S-3 stiffness (OP-C5) | — | PR-1 relies on B1 | drafted; items bound to R-100 / S-3; change-item content identities include B1 |
| T6 | Engineer A edits S-3 (intervening edit) | r13 (same generation g1) | PR-1 still relies on B1 | — |
| T7 | Agent submits PR-1 | host evaluates B2 = …/g1/r13/⟨v13⟩ | B1 | **refused — stale**: reason "S-3 changed since r12", relied B1, current B2 |
| T9 | Agent re-reads; drafts PR-2 (lineage PR-1, stale) | B2 | PR-2 relies on B2 | new proposal identity; old values re-derived at r13; new item content identities |
| T10 | Submit PR-2 | B2 | B2 | validated → **queued** (not applied) |
| T11 | Engineer A accepts item 1 (A5), rejects item 2 (A10) | — | B2 | item 1 accepted (bound to its item content identity); item 2 rejected |
| T12 | Host applies item 1 | resulting r14 | B2 | **applied**: association PR-2 / item 1 / B2 / RC-1 / r14; A5 not lapsed |
| T13 | Acknowledgment lost; agent retries PR-2 (same identity) | — | B2 | second submission recorded separately; repeat reports RC-1, or **outcome unknown** (observer: loop/agent) if unobservable |

**Comparison DEL-03-01 performs (C VC-C-04):** for each basis element and the
method designation, compare the value at read (T3, T9), in the proposal
reference (T5, T9), in the refusal (T7: relied and current), and in the
applied-outcome association (T12). Expected: PR-1's reference equals B1 at
every step; the refusal shows B1 and B2 distinctly; PR-2 references B2 only;
the association references B2 and r14; no step rewrites a reference; whether
RC-1 itself carries B2 is recorded as a host observation.

**Evidence labels:** *illustrative* (this table), *test-double* (App-side
fixture against a simulated host), *actual host* (candidate-bound SWBPIPE
observation, DEL-09-09). The first executable return is a candidate-bound
test-double observation; it is not host evidence (V1-B X-08).

## 12. Receiving risks from SWBPIPE source limits (HI §11, `e548d4cf`)

Recorded as risks for receiving and the joined witness, not host assignments:

| Observed limit | Risk to this contract | Where checked |
|---|---|---|
| Queue-time basis differs from original external inspection basis | Stale check against a queue-time basis would silently substitute a later basis (violates §3.2, §5) | DEL-09-09 VER-004; VC-P-04/07 against actual host |
| No durable exactly-once domain outcome established; runtime transport is not a joined live mutation path | §7 one-effect not evidenced by transport dedup or shared validation | DEL-09-09 VER-008; VC-P-09 |
| Stronger frozen-review checks not assumed for every route | Validation parity (§2) may differ by route | VC-P-02 against actual host |
| Workflow resolution ≠ provider adoption | Origin's workflow identity may not reflect adopted behavior | DEL-04-03 record comparison |

Later mainline or external-session changes need a targeted applicability
check before reliance (HI §11).

## 13. Interfaces provided and expected

| Direction | Counterpart | Content |
|---|---|---|
| Expect from | DEL-03-01/C-v0.2 | §3.2 elements; §4.1 results; content identities and method designation; exposure; FX-PIPE-01 |
| Expect from | DEL-04-01 | A1–A14 names; adopted class records (D2/D3) with revision identity; treatment → outcome map; residual `UNRESOLVED{OI-021}` additions |
| Expect from | DEL-04-02 | Grant display state and treatment per class and scope; settings version identities |
| Expect from | DEL-02-01 | Workflow identity; checkpoint declarations (required act, bound subject, reached-when) |
| Expect from | Host owner | Route, treatment resolution, validation outcomes, receipts, origin marks, undo route, views, captured acts, settings version at application, stale rule (U-C3), generation meaning (U-C2), one-effect evidence |
| Provide to | DEL-04-02 | Direct-branch entry condition and origin semantics (§4.4); standing per outcome (§9) |
| Provide to | DEL-04-03 | Canonical §9 taxonomy; per-submission recording (§7); applied-outcome association; change-item content identity for A5/A10 lapse (L-1); origin (§3.3); act/evidence table (§10); undo relation (§4.5) |
| Provide to | DEL-03-03 | This contract unchanged for the external channel; *channel not enabled*, *not exposed*, *not permitted* |
| Provide to | DEL-05-01 | §9 unchanged; observer-attributed *outcome unknown*; retry keeps proposal identity; origin, seat role and grant in force on every dispatch; sibling-draft rule (§3.1 rule 5) |
| Provide to | DEL-05-02 | Per-item dispositions with actors, lineage, stale indication, "accept" wording (§8) |
| Provide to | DEL-02-01 / DEL-02-03 | Acceptance-checkpoint-forces-proposal constraint (§4.4); per-item dispositions and all-items-decided indication (§4.3) |
| Provide to | DEL-03-04 | §1 authority map and this table |
| Provide to | DEL-09-09 | §11 scenario, §12 risks, VC-P cases and expected outcomes |
| Provide to | DEL-03-01 | M3-CP return (§11) |
| Provide to | Host proposal views | §8 information |

## 14. Examples (FX-PIPE-01 fixture subjects)

All material is **invented** and taken from the shared catalogue (C-v0.2
§10). Labels are fixture labels, not identities, wire names or SWBPIPE
commitments.

**E-1 PR-2 in the host view after T10:**

| Row | Item | Object | Attribute | Old (at r13) | New | Why | Origin | Disposition |
|---|---|---|---|---|---|---|---|---|
| new support | 1 | new support on R-100 at 4.2 m | created | — | guide support | Span S-2→S-3 exceeds limit (T4 finding) | agent seat (role: host agent), conversation K-7, workflow {workflow, host, ⟨fx-root⟩, supports-adjust, ⟨rev-3⟩} run 12 | queued |
| S-3 | 2 | S-3 | stiffness | value at r13 (Engineer A's T6 edit) | 2.0e6 N/m | Reduce thermal restraint | same | queued |

**E-2 Truthful reports:**

| Situation | Correct report | Incorrect report |
|---|---|---|
| T10 submit succeeded | "PR-2 queued (2 items); awaiting your decision" | "PR-2 applied" / "accepted" |
| After T11, before T12 | "Item 1 accepted by Engineer A, not yet applied; item 2 rejected by Engineer A" | "Item 1 applied"; "item 2 refused" |
| T12 | "Item 1 applied, receipt RC-1, now r14" | "Item 1 approved" |
| T16 direct application of OP-C9 under an effective direct grant | "Applied under your grant (settings ⟨set-2⟩); origin-marked; undo available" | "Accepted" |
| T13 acknowledgment lost | "Outcome unknown (observed by loop); last observed: accepted" | "Applied" or "failed" |
| OP-C4 requested directly at r13 with no effective direct grant | "Not permitted: add support requires a proposal under your current settings (default propose)" | Silent conversion to a proposal; "unavailable" |
| Workflow checkpoint requires A5 on OP-C4 while OP-C4 is granted direct | Drafted as a proposal; run waits for A5 | "Applied; checkpoint waiting" |
| T17 undo of RC-2 | "Label change RC-2 reversed by RC-3" | "RC-2 deleted" |

## Changes from v0.1

v0.1 = P-v0.1 (sha256 313487c0…9bce, 447 lines).

| V1 / R1 item | Change |
|---|---|
| R-1 (V1-A D-01, D-17, D-18, D-20) | Canonical names A1–A14 in §§4, 9, 10; S-P14 |
| R-2; V1-B D-08, §5 rows | D2/D3 applied: `UNRESOLVED{OI-001/002}` narrowed to OI-021 additions; OI-002 removed from *not permitted*; S-P14/S-P15 |
| R-3; V1-A D-05, D-08 | §2 treatment on host route; not-permitted cases; no silent conversion; §4.2 narrowing/widening rows |
| R-4 | "Later-check route" implies no act; A3 never A4 |
| R-5; V1-C D-07 | §4.4 acceptance checkpoint forces proposal; A4 checkpoint case; §10 capturing-surface evidence |
| R-6; V1-B D-01 (BLOCKING), D-10; X-01, X-04 | §3.1 change-item content identity; A5/A10 bind to it; application does not lapse; acceptance unit = change item; batch = one A5 listing items; U-P3 resolved as stale-at-application |
| R-7; V1-B D-04, D-05, D-09; V1-A D-16, D-24; V1-C D-11, D-12, AB-05 | §9 canonical taxonomy with *application error* (effect statement), *refused* vs *rejected*, actors for A5/A10/A11, observer-attributed unknown; §7 per-submission recording and host-obligation wording; retry keeps proposal identity |
| R-8; V1-B D-06, D-07; V1-A D-08 | §3.3 standing at drafting plus two settings references; §4.4 entry only on *effective direct* |
| R-9; V1-C D-10 | §3.3 workflow identity {kind, origin, source root, name, revision} + derived-from |
| R-9; V1-B D-20 | Fixtures re-labeled to FX-PIPE-01 timeline (T1–T17); proposals PR-1/PR-2; E-1 row/item mapping |
| V1-A D-15 | Withdraw = A11 proposer only; person removing another's proposal = A10 |
| V1-A D-16 | Host refusal removed from "rejected" |
| V1-B D-17 | Origin: App request-side recorded fully; host origin mark linked, not copied |
| V1-B D-18 | §4.5 undo as a change through the one route |
| V1-B D-21 | Evaluated basis on every non-success outcome |
| V1-B D-22 | Applied-outcome association replaces "receipt cites" |
| V1-B D-23 | Rejection/withdrawal actors stated for DEL-04-03 |
| V1-C AB-01 | §4.3 all-items-decided indication; mapping owner DEL-02-01/DEL-02-03 |
| V1-C AB-02, AB-03 | Seat role meaning; origin on every dispatch |
| V1-C AB-13 | §3.1 rule 5 sibling drafts (proposed; U-P9) |
| V1-B X-08; RF-08 | Executable return still absent; missing mirror row noted for C1 |

## UNRESOLVED

| Item | Owner | Point of need | Effect on this definition |
|---|---|---|---|
| `UNRESOLVED{OI-021}` operation-specific reserved additions; first connected operation, autonomy, environment | Owner via outside SWB session and App/shared owner | Before connected SoW/execution | Class for connected operations may gain reserved additions; §11/§14 invented only |
| Host adoption and enforcement of the D2 list and treatment resolution | Host owner / SWBPIPE (DEP-001) | Before host conformance | All treatment and act behavior is receiving meaning |
| `UNRESOLVED{OI-003}` extension promise | Owner with host contract owner | Before extension claim | Not decided here; route parity (§2) required regardless |
| `UNRESOLVED{OI-014}` shared contract/component placement | App/shared contract owners (DEP-03-02-025) | Before structural/production allocation | No placement implied |
| U-P1 Proposal identity and change-item content identity representation, encoding, duplicate-effect enforcement, outcome-recovery mechanics (TBD-002) | Relevant contract and host owners (DEP-03-02-026) | Before dependent implementation | §3.1, §7 obligations testable; mechanisms open |
| U-P2 Actual host route, views, receipts, act capture, settings version at application | Host owner / SWBPIPE (DEP-03-02-023) | When integration/witness relies on them | Settings reference at application is *unconfirmed* until host-reported |
| U-P3 (narrowed) Host evidence that application re-checks the basis after acceptance | Host owner (DEP-001) | Before application-path conformance | Contract rule fixed by R-6 (stale at application) |
| U-P4 Validation failure before queueing: state treatment | Host owner | Before adapter implementation | Proposed: refused, stays drafted |
| U-P5 Host refusal at application: whether the host distinguishes it from validation refusal in its records | Host owner | Before outcome recording | Refusals never recorded as A10 |
| U-P6 Operation-specific withdraw/reject rules beyond R-1 (not in the D2 list) | Host owner (V4-HI-30); OI-021 for the connected operation | Before withdrawal implementation | A11 proposer-only; A10 reserved wherever A5 is |
| U-P7 Item application grouping | Host owner | Before application-path implementation | Item-level dispositions defined |
| U-P8 Undo route availability, scope and treatment | Host owner | Before undo implementation | §4.5 semantics only |
| U-P9 Sibling-draft grouping mechanics | DEL-05-01 with DEL-03-02 | Before FX-M8 / loop fixtures | §3.1 rule 5 proposed |
| Mixed item decisions → checkpoint disposition (V1-C AB-01) | DEL-02-01 with DEL-02-03 | Before VC-07/VC-09, FX-C, PC-07 fixtures | P supplies per-item data only |
| U-C2 / U-C3 / U-C4 (shared with DEL-03-01) generation, stale rule, multi-read reliance | Host owner with DEL-03-01/DEL-03-02 | Before stale implementation | §5 trigger defined abstractly |
| Register: DOWNSTREAM mirror of DEP-03-01-026; mirrors to DEL-05-01/05-02; UPSTREAM row from DEL-04-02; SatisfactionStatus TBD vs PENDING (V1-B RF-06/08/09; V1-C RF-2) | Register owner at closeout C1 | C1 | None on content |

## Verification cases

Designed, **not run**. Evidence labels at execution: *illustrative*,
*test-double*, *actual host*. Steps refer to FX-PIPE-01 (C-v0.2 §10.3).

| Case | Design | Expected result | Serves |
|---|---|---|---|
| VC-P-01 Coverage | Map §§1–13 to the twelve scope rows (SOW-070, 090, 091, 170–178), V4-HI-20–25, C-v0.2 elements and R-1–R-9 | Every scope row covered; every representation choice named as open with owner; DERIVED/INTEGRATION markings match R1 | VER-001 |
| VC-P-02 Channel parity | Same OP-C4 proposal, arguments, basis, authority via person, embedded, external; plus invalid, stale, direct-without-grant variants | One route identity; identical outcome/error meanings; direct-without-grant → *not permitted* on every channel, never converted; only authority differs, with policy record cited | VER-002 |
| VC-P-03 Host authority / no upgraded result | T10 with no A5 captured | Reported *queued*; never *accepted*; domain truth only in host | VER-003 |
| VC-P-04 Origin and basis preservation | Trace PR-2 from T9 to T12 | Author type, seat role, channel, conversation, workflow identity (full) and run, standing at drafting, both settings references (application one *unconfirmed* unless host-reported), relied basis B2 identical at every step | VER-004 |
| VC-P-05 Lifecycle branches + direct case | T10→T11→T12; item 2 rejected; a withdrawn proposal; T7 stale; T16 direct; a direct request under *unconfirmed* grant | Each disposition with actor and evidence; applied carries association; T16 records no acceptance; unconfirmed grant → proposal route / not permitted for direct | VER-005 |
| VC-P-06 Unknown outcomes | (a) T12 applied but acknowledgment lost; (b) a submission whose application is not established; (c) application error with effect *unknown* | All report *outcome unknown*, attributed to the observer, with last observed state; no inferred success, failure or act | VER-006 |
| VC-P-07 Stale, re-draft, stale-after-accept | T5–T9; plus variant: basis fails between T11 and T12 | T7 refusal with reason, B1, B2; PR-2 new identity and lineage citing B2; variant → *refused — stale* at application, A5 not lapsed, item not applied, no carry to re-draft | VER-007 |
| VC-P-08 No retargeting | Draft PR-2; person selects S-4; submit and inspect | Bound targets and affected objects remain R-100/S-3 | VER-008 |
| VC-P-09 One effect | T13: retry PR-2 (same identity); variant with two host receipts observed | Each submission recorded separately; one effect → same RC-1; if two receipts observed, both recorded (host obligation failed, not hidden); unobservable → unknown; no global exactly-once claim | VER-009 |
| VC-P-10 Host view info | Inspect E-1 against V4-HI-24 and §8 | Old, new, affected objects, row/item mapping, reason, origin, per-item disposition, lineage present; host named as producer | VER-010 |
| VC-P-11 Execution vs acts | T12 success without act evidence beyond T11; separately evidenced A4, A6, A7 cases | Success asserts execution only; each act claim backed by its own evidence; A9 records cite capturing-surface evidence; none inferred from another | VER-011 |
| VC-P-12 Queued/accepted/applied/unknown reporting | T10; after T11; T12; T13 | queued; "accepted, not yet applied" with actor; applied with association; unknown — compared against host records | VER-012 |
| VC-P-13 Policy interface | Review §§2, 4.4, 9, 10 against CLM-004, #d3, D2/D3, R-2/R-3/R-5 | Routine tool permission (A14), direct application, A5 and other acts distinct; reserved acts per D2; acceptance checkpoint forces proposal; only OI-021 additions remain unresolved; no blanket approval policy | VER-013 |
| VC-P-14 Boundary audit | Check REQ-013 exclusions one-for-one against §1 and §13; run the registered boundary-owner checker when available | Each excluded act resolves to its owner; twelve scope rows retained; no sibling/external completion or SWBPIPE adoption claimed | VER-014 |
