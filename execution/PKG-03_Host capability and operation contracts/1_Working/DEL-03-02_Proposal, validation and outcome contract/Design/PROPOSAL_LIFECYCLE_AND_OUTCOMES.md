# Proposal, validation and outcome contract
- Contribution: DEL-03-02/P-v0.1
- Status: DRAFT DEFINITION — proposed, unsupplied, not implemented, not accepted
- Serves: OUT-001 (proposal, relied-on basis, origin and outcome schema meaning), OUT-002 (lifecycle, one route, actor parity, host ownership and receiving interfaces), OUT-003 (designed contract fixtures); REQ-001–REQ-013; AC-001–AC-014; VER-001–VER-014
- Basis: repo 6e18505e3; ScopeOfWork.md sha256 42328987c71dd243323805faf2634067cca0113b81ca93d4d129193b2a71128a; `P/docs/HOST_INTEGRATION.md` (sha256 08c8fc7d…60da) §1, §§3–5 (V4-HI-11, V4-HI-20–25, V4-HI-30–33), §6 V4-HI-40–42, §7 V4-HI-50–52, §9 V4-HI-70–71, §10, §11; `P/docs/PRD.md` V4-PAR-04, V4-AUT-01–05, V4-REC-01, V4-CST-05/06, §9 OQ-02/OQ-11; `P/docs/ARCHITECTURE.md` V4-ARC-20; `P/docs/EXAMINATION.md` V4-EXM-20/22/25; DECISION_BRIEF #d2/#d3/#d4/#d5; SCC-CASE-002 Case_Datasheet rows M1-P, M3-CP (sha256 6acdc6c4…a71a6); Open_Issues OI-001/002/003/014/021
- Consumed inputs: DEL-03-01/C-v0.1 (co-developed in this run: operation identity/version, input/effects/errors, availability results, read basis descriptor and relied-on basis reference, `CATALOG_AND_READ_BASIS.md` §§3–5); DEL-04-01 referenced by accepted meaning only (act names, class values), to be reconciled at V1; DEL-04-02 autonomy-grant meaning referenced by accepted meaning (V4-HI-40–42), to be reconciled at V1; host facilities (route, views, receipts, act recording): not supplied (DEP-03-02-023)
- Receivers: DEL-04-02 (OUT-001, OUT-002; REQ-003–005; VER-003–005) via DEP-03-02-018; DEL-04-03 (OUT-001, OUT-002, OUT-004; REQ-002, REQ-003, REQ-005; VER-001, VER-004, VER-006) via DEP-03-02-019; DEL-03-03 (OUT-001, OUT-003; REQ-001, REQ-004; VER-001, VER-004) via DEP-03-02-020; DEL-05-01 (OUT-001, OUT-003; REQ-003, REQ-007; VER-008); DEL-05-02 (OUT-001, OUT-003; REQ-001–003; VER-001–003); DEL-09-09 (OUT-001; REQ-001, REQ-004; VER-001, VER-004) via DEP-03-02-022; DEL-03-01 (OUT-001, OUT-003; REQ-001, REQ-004; VER-004) as the M3-CP return (DEP-03-01-026); DEL-03-04 responsibility map via DEP-03-02-021; external host proposal-view receiving via DEP-03-02-024

## 0. How to read this definition

This is the 60% semantic definition of how a change, by a person or an
agent, is proposed or applied through a host, and how its outcome is
reported. Element names are **semantic labels, not wire names**. No
proposal-identity representation, schema encoding, duplicate-effect
mechanism, outcome-recovery mechanism, storage engine, transport field, retry
budget or retention interval is selected (TBD-002; DEP-03-02-026), and no
component placement (OI-014; DEP-03-02-025). Unruled policy appears only as
`UNRESOLVED{OI-nnn}`.

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
| S-P8 | Queued ≠ applied; applied edit ≠ engineering approval; a receipt records the operation outcome, not an act of acceptance | #d3 "Preserve the meanings through the UI" |
| S-P9 | Acceptance of a proposed edit is not engineering approval; the interface says "accept", never "approve", for proposals | V4-HI-33 |
| S-P10 | Agents never record a human act as performed when it was not | V4-HI-31; V4-AUT-03 |
| S-P11 | A human act binds to content and lapses visibly when content changes | V4-HI-32 |
| S-P12 | Domain truth and validation stay in the host; Chirality never presents agent output as the host's accepted result | V4-REC-01; V4-CST-05 |
| S-P13 | Workflow checkpoints override autonomy: the run waits for the person's act | V4-HI-42 |

## 1. Host authority map (REQ-002, REQ-013; VER-003, VER-014)

| Facility | Owner | This contract's role |
|---|---|---|
| Domain objects, store and truth | Host owner (SWBPIPE outside session) | None; reads through DEL-03-01 |
| Validation and the one application route | Host owner | Defines the receiving meaning of its outcomes |
| Receipts, origin marks, undo | Host owner | Refers to them; never manufactures one |
| Proposal views (old/new/objects/reason) | Host owner | Supplies the information the views need (§8; DEP-03-02-024) |
| Offering, recording and presenting human acts | Host owner (facility); the person (the act) | Consumes recorded acts as evidence; never creates one |
| Catalog and read basis meaning | DEL-03-01 | Consumed (§3.2) |
| Adopted operation policy and act names | DEL-04-01; unresolved values: owner with App/SWB contract owners | Consumed; `UNRESOLVED{OI-001/002}` where unruled |
| Autonomy settings display and standing receiving | DEL-04-02 | Supplied: origin and direct-autonomy semantics |
| Human-act and run-record format | DEL-04-03 | Supplied: outcomes and receipt links |
| External receiving adapter | DEL-03-03 (host owns endpoint) | Supplied: this same contract |
| Integrated host guide | DEL-03-04 | Supplied: responsibility map (this §1 and §13) |
| Joined external witness, extension trace | DEL-09-09 | Supplied: fixtures and outcome expectations |

A host-accepted result exists only where the host has recorded the relevant
act. Agent output without that record retains its actual standing
(*drafted*, *queued*, *finding*), never *accepted* (SOW-091).

## 2. One route and actor parity (REQ-001; SOW-070)

- Person, embedded agent and external agent submit changes to the **same**
  host validation/application route. The channel is attribution (§3.3), never
  a route selector.
- **Equivalence rule.** For equivalent operation identity/version, arguments,
  relied-on basis and applicable authority, every channel receives the same
  outcome and the same error meaning (identity and text).
- **Permitted difference** is authority only: autonomy grant, reserved acts
  and policy class (DEL-04-01; V4-HI-40, V4-HI-51). A difference arising from
  authority is reported as *not permitted* with the governing policy (or
  `UNRESOLVED{OI-001/002}`), never as a different validation error.
- No fixture or adapter may define an alternate agent mutation path, bypass
  validation, or apply outside the host route (AC-002).
- Person-origin changes use the same route; whether a person's direct edit is
  itself represented as a proposal is host practice. This contract requires
  only that it passes the same validation and yields the same basis check
  and outcome meanings.

## 3. Change request elements (OUT-001; REQ-003; SOW-170)

### 3.1 Proposal / change identity

| Semantic element | Meaning |
|---|---|
| Proposal identity | Stable identity of *this* proposal from drafting onward. It is the unit for one-effect (§7). A re-draft receives a **new** identity (§5) |
| Lineage | For a re-draft: the identity of the proposal it replaces and why (e.g. stale). Absent otherwise |
| Change items | One or more items, each with its own identity within the proposal (supports row-level acceptance, V4-HI-41; V4-EXM-20) |

Representation of identity is unselected (TBD-002).

### 3.2 Consumed catalog meaning (from DEL-03-01/C-v0.1)

| Element | From C | Rule here |
|---|---|---|
| Operation identity and version | C §3 #1 | The version the request was prepared for; not re-interpreted |
| Arguments | C §3 #3 | Checked against the catalog input schema before host domain validation (DEL-05-01 REQ-003) |
| Bound targets / affected objects | C §3 #3 target identification, #5 effects | Fixed at drafting (§6) |
| **Relied-on basis reference** | C §5.2 | The basis descriptor(s) — workspace identity, generation, model revision, canonical content identity — of the read(s) actually relied on; carried unchanged to every outcome; never replaced by a queue-time or application-time basis. A host-observed later basis may be recorded as a separate element |
| Errors, availability results | C §3 #7, §4.1 | Reused as outcome reasons (§9); no separate error vocabulary |

This contract defines no separate basis authority (CLM-003).

### 3.3 Origin and attribution

| Semantic element | Meaning | Source |
|---|---|---|
| Author type | person or agent | V4-HI-21 |
| Author identity | The person, or the agent seat/role instance that drafted | V4-HI-21; V4-HOST-05 |
| Channel | host interface, embedded agent, external agent | V4-PAR-02 (attribution only) |
| Conversation | Conversation the agent change came from | V4-HI-21 |
| Workflow run | Workflow identity and version, and run identity | V4-HI-21; V4-HI-70 |
| Autonomy standing at drafting | The person's grant in force for this operation class (DEL-04-02), or *proposal required*; or `UNRESOLVED{OI-001}` where the class is unruled | V4-HI-40 |
| Reason | Why the change is proposed, in the proposer's words | V4-HI-24 |

Origin is preserved through submission, every lifecycle transition and
outcome reporting, and is linked (not copied) into the run record by
DEL-04-03 (V4-HI-70–71).

### 3.4 Change item content

| Semantic element | Meaning |
|---|---|
| Affected object | Identity of the object changed |
| Attribute | What of the object changes (or *created* / *removed*) |
| Old value | Value as of the relied-on basis |
| New value | Proposed value |
| Item reason | Optional item-specific reason |

## 4. Lifecycle (REQ-004, REQ-005, REQ-011; SOW-171, SOW-172, SOW-178)

### 4.1 Proposal states (outside granted direct autonomy)

```text
drafted ─► validated ─► queued ─► accepted ─► applied (receipt)
                          ├─► rejected
                          ├─► withdrawn
                          └─► stale  (relied-on basis no longer holds)
overlay: any submitted step whose outcome cannot be observed ─► outcome unknown
```

| State | Meaning | Entered by (actor) | Evidence |
|---|---|---|---|
| drafted | Proposal composed with operation, arguments, targets, relied-on basis, origin, items | Proposer (agent or person) | Proposal content |
| validated | The host's validation route found it valid against the relied-on basis | Host | Host validation outcome |
| queued | Submitted and held by the host for the person's decision | Host (on proposer's submission) | Host queue record |
| accepted | The person accepted the proposal or some items ("accept", S-P9) | **The person**; host records | Host-recorded acceptance act, bound to proposal content (S-P11) |
| applied (receipt) | The host applied the accepted change through its one route | Host | **Receipt**; resulting revision |
| rejected | Not accepted | The person (act recorded by host) or host refusal on validation at application (U-P5) | Host record with actor and reason |
| withdrawn | Proposer or person withdrew it before application | Actor identified (class for agent withdrawal: `UNRESOLVED{OI-001}`, U-P6) | Host record |
| stale | Relied-on basis no longer holds; refused with reason (§5) | Host | Host refusal with both bases |
| outcome unknown (overlay) | A submission, acceptance-to-application or direct application was sent but its result cannot be observed | Reporter (App/adapter/loop) | Absence of observation; the last observed state |

Settled reporting rules:

1. A submitted proposal reports **queued** until the host records acceptance
   and application (S-P7). A successful *submit* is reported as queued, never
   as applied or accepted.
2. **Accepted alone is not applied.** The accepted stage may be reported
   separately; *applied* is reported only with a host **receipt** reference
   (REQ-011).
3. **Outcome unknown** is reported whenever the outcome cannot be observed,
   including when execution may have occurred. It is not inferred to be
   applied, failed, rejected or accepted from missing observation (REQ-005).
   It is resolved only by a later host observation (e.g. re-reading the
   proposal state or the model with a new basis), which is reported with its
   own basis; recovery mechanics are unselected (TBD-002).

### 4.2 Transition gaps in the source lifecycle (proposed handling, host input needed)

V4-HI-23 draws rejected / withdrawn / stale from *queued*. It does not name:

| Gap | Proposed contract handling (v0.1) | Status |
|---|---|---|
| Validation fails before queueing | Reported as a **refusal outcome** with the catalog error (C §3 #7); the proposal stays *drafted* (not validated); no queue entry | Proposed; host confirmation U-P4 |
| Stale detected at validation (before queue) | Stale refusal (§5) | Proposed; follows HI §10 item 3 "check it on every change" |
| Basis no longer holds after *accepted*, before *applied* | Application must not proceed on a basis that no longer holds (HI §10 item 3). Name of the resulting disposition and treatment of the recorded acceptance (which lapses under S-P11 if content changed) are **U-P3** | Unresolved |
| Withdrawal before queueing | Discarding a draft; no host record required | Proposed |
| Partial acceptance of items | §4.3 | Proposed |

### 4.3 Item-level acceptance (V4-HI-41; V4-EXM-20)

The accepted SWBPIPE default for model changes is proposal with row-by-row,
multi-row or whole-batch acceptance (V4-HI-41). Therefore:

- Each change item carries its own disposition (accepted, rejected,
  withdrawn, stale, applied with receipt, outcome unknown).
- The proposal's reported state is derived and never stronger than its
  items: e.g. "3 of 4 items accepted, 1 rejected; 3 applied (receipt R-…)".
- Whether items may be applied separately, or accepted items are applied as
  one host application, is a host input (U-P7). One-effect (§7) holds per
  item and per proposal.

### 4.4 Direct-autonomy branch (V4-HI-22; S-P3)

Where the person has granted direct application for the operation class:

```text
drafted ─► validated ─► applied (receipt, origin mark, undo route, later-check route)
                ├─► refused (invalid | stale | not permitted)
overlay: unobservable ─► outcome unknown
```

- No *queued* or *accepted* state exists and **no acceptance is recorded or
  implied**. Reports never say "accepted" for a direct application.
- The application carries: origin (§3.3), the grant it relied on (DEL-04-02
  standing at application), relied-on basis, receipt, origin mark, undo route
  and later-check route (abstract host contributions; host-owned).
- The basis check applies exactly as for proposals.
- A workflow checkpoint overrides the grant: the run waits for the person's
  act (S-P13).
- A grant changed during work (V4-HI-40) applies from the change onward; the
  standing actually in force at application is what is recorded. Where the
  class is `UNRESOLVED{OI-001}`, the direct branch is not exercised in any
  conformance claim.

## 5. Stale refusal and re-draft (REQ-006; SOW-173)

- **Trigger.** The relied-on basis (§3.2) no longer holds when the host checks
  it (validation, queue, or application). Which change counts as "no longer
  holds" — any model revision, or a change to relied-on content — is
  **U-C3** (shared with DEL-03-01).
- **Refusal content.** State *stale*; reason (what changed, where known);
  **relied-on basis** (unchanged); **current basis** observed by the host;
  affected items.
- **No silent refresh.** The host or any consumer never rewrites the
  relied-on basis to the current one and proceeds.
- **Re-draft.** Permitted only as a **separately identified** proposal: new
  proposal identity, lineage to the stale one, a new relied-on basis from a
  new read, re-derived old values, and fresh validation. Any acceptance
  recorded on the stale proposal does not carry over (it bound to other
  content, S-P11).

## 6. No retargeting (REQ-007; SOW-174)

- Bound targets and affected objects are fixed at drafting from explicit
  target identification (C §4.3), including a person's selection resolved at
  drafting.
- A later selection change in any surface never changes a proposal's bound
  targets, items or reported affected objects. A change of intended target is
  a new proposal.

## 7. Repeated submission → one effect (REQ-008; SOW-175)

- **Obligation.** Submitting the same proposal (same proposal identity) more
  than once, including retry after a lost acknowledgment, produces at most
  one application effect per item.
- **Testable form.** Effect count observed in the host model/receipts for the
  proposal identity equals the number of distinct applications (0 or 1 per
  item); a repeat submission reports the existing state (queued, applied with
  the *same* receipt, etc.).
- **Mechanism unselected.** Deduplication key, storage, retention and retry
  policy are TBD-002 / DEP-03-02-026. Shared validation alone is not evidence
  that one-effect holds; transport deduplication is not evidence of a
  one-domain-effect outcome (V4-EXM-25).
- **Unobservable repeat.** If neither the first nor the repeat result can be
  observed, report **outcome unknown**; do not infer one effect or zero.
- A re-draft (§5) is a different proposal and not a repeat.

## 8. Host proposal-view information (REQ-009; SOW-176)

The host shows, in its own tables/views (V4-HI-24; V4-HOST-04: no
agent-private surface), for each proposal and item:

| Information | Supplied by this contract | Presented by |
|---|---|---|
| Old value (as of relied-on basis) | §3.4 | Host |
| New value | §3.4 | Host |
| Affected objects | §3.4 / §6 | Host |
| Why (reason) | §3.3 / §3.4 | Host |
| Origin (author, conversation, workflow run) | §3.3 | Host |
| Current state per item | §4 | Host |
| Stale indication with current value where it differs | §5 | Host |

Presentation, receipts and the acceptance control are host-owned
(DEP-03-02-024). The acceptance control says "accept", never "approve"
(S-P9). A live UI witness is host-owned evidence, separate from this
information contract.

## 9. Outcome taxonomy (REQ-005, REQ-010, REQ-011; SOW-172, SOW-177, SOW-178)

| Outcome | Meaning | Establishes | Does **not** establish |
|---|---|---|---|
| unavailable | Catalog precondition failed (C §4) | Nothing executed | — |
| not permitted | Actor lacks authority (reserved / outside grant / `UNRESOLVED{OI-001/002}`) | Nothing executed | — |
| channel not enabled | External access off (V4-HI-52) | Nothing executed | — |
| invalid | Host validation refused with catalog error | Nothing applied | — |
| stale | Relied-on basis no longer holds | Nothing applied | — |
| queued | Host holds proposal for decision | Submission received | Acceptance, application |
| accepted | Host recorded the person's acceptance | That act by that person on that content | Application, checking, approval, reliance |
| applied (receipt) | Host applied; receipt exists | Execution and resulting revision | Acceptance (in direct branch), checking, approval, reliance |
| rejected | Host recorded rejection with actor | That rejection | — |
| withdrawn | Withdrawn by identified actor | That withdrawal | — |
| outcome unknown | Result unobservable | Only the last observed state | Applied, failed, accepted or rejected |
| success (operation) | The operation ran (S-P7) | Execution | Any human act |

## 10. Execution versus human acts (REQ-010, REQ-012; SOW-177; #d3)

Act names are DEL-04-01's accepted names by meaning, to be reconciled at V1.

| Subject | Actor | Evidence required | Never inferred from |
|---|---|---|---|
| Propose (draft/submit) | Agent or person | Proposal content and queue record | — |
| Validate / apply | Host route | Validation outcome; receipt | — |
| Direct application under grant | Agent within person's grant | Receipt, origin mark, grant in force | — and it implies no acceptance |
| Accept a proposed edit | The person | Host-recorded act bound to proposal content | Success, submit, queue, application, agent report |
| Reject a proposed edit | The person (or host refusal, U-P5) | Host-recorded act or refusal | Absence of acceptance |
| Mark checked | The person | Host-recorded checked act bound to content | Agent finding, success, acceptance |
| Engineering approval | The person/accountable professional | Its own record | Acceptance of an edit (S-P9) |
| Professional reliance | Accountable professional | Its own record | Any of the above |
| Agent finding | Agent | Finding by reference | — and it is not a checked act |
| Faithful recording of an actual act | Recorder (host or agent) ≠ decision actor (person) | Reference to the host's record of the act | — |

Rules: one act never establishes another; no synthetic prerequisite between
acts is introduced; which acts are always reserved remains
`UNRESOLVED{OI-001}`, and classifier-based routine permission
`UNRESOLVED{OI-002}` (REQ-012). A still-unresolved policy does not become a
universal permission prompt or a fabricated act (AX-002).

## 11. M3-CP read-then-action comparison design (return to DEL-03-01)

This is the distinct return retained from SCC-CASE-004 (CASE-002 M3-CP;
DEP-03-01-026). It supplies DEL-03-01 with designed refusal/application
behavior and a comparison plan; DEL-03-01 compares basis elements only and
implements none of this behavior.

**Scenario (invented fixture; see §14):**

| Step | Action | Basis observed | Proposal reference | Expected P behavior |
|---|---|---|---|---|
| 1 | Agent reads supports table (OP-C1) | B1 = FX-W1/g1/r12/⟨c12⟩ | — | — |
| 2 | Agent drafts P-1: add support on R-100 near S-3; move S-3 stiffness | — | P-1 relies on B1 | drafted, items bound to R-100/S-3 |
| 3 | Person edits S-3 in host UI (intervening edit) | model now r13 | P-1 still relies on B1 | — |
| 4 | Agent submits P-1 | host observes B2 = …/r13/⟨c13⟩ | B1 | **stale refusal**: reason "S-3 changed since r12", relied B1, current B2 |
| 5 | Agent re-reads supports table | B2 | — | — |
| 6 | Agent drafts P-2 (lineage: P-1, stale) | — | P-2 relies on B2 | new identity; old values re-derived at r13 |
| 7 | Submit P-2 | B2 | B2 | validated → **queued** (not applied) |
| 8 | Person accepts item 1, rejects item 2 | — | B2 | item 1 accepted; item 2 rejected |
| 9 | Host applies item 1 | new r14 | B2 | **applied**, receipt cites P-2, item 1, relied B2, resulting r14 |
| 10 | Acknowledgment of step 9 lost; agent resubmits P-2 | — | B2 | one effect; repeat reports existing receipt, or **outcome unknown** if unobservable |

**Comparison DEL-03-01 performs (VC-C-04):** for each of workspace identity,
generation, model revision, canonical content identity — compare the value at
read (1, 5), in the proposal reference (2, 6), in the refusal (4: relied and
current), and in the receipt (9). Expected: P-1's reference equals B1 at
every step; the refusal shows B1 and B2 distinctly; P-2 references B2 only;
the receipt references B2 and the resulting r14; no step rewrites a
reference.

**Evidence labels (required at execution):** *illustrative* (this table),
*test-double* (App-side fixture against a simulated host) or *actual host*
(candidate-bound SWBPIPE observation, DEL-09-09). The first executable return
is a candidate-bound test-double observation; it is not host evidence.

## 12. Receiving risks from SWBPIPE source limits (HI §11, `e548d4cf`)

Recorded as risks for receiving and the joined witness, not as host
assignments:

| Observed limit | Risk to this contract | Where checked |
|---|---|---|
| Queue-time basis differs from original external inspection basis | Stale check against queue-time basis would silently substitute a later basis (violates §3.2, §5) | DEL-09-09 VER-004; VC-P-04/07 against actual host |
| No durable exactly-once domain outcome established; runtime transport is not a joined live mutation path | §7 one-effect not evidenced by transport dedup or shared validation | DEL-09-09 VER-008; VC-P-09 |
| Stronger frozen-review checks not assumed for every route | Validation parity (§2) may differ by route | VC-P-02 against actual host |
| Workflow resolution ≠ provider adoption | Origin's workflow identity may not reflect adopted behavior | DEL-04-03 record comparison |

Later mainline or external-session changes need a targeted applicability
check before reliance (HI §11).

## 13. Interfaces provided and expected

| Direction | Counterpart | Content |
|---|---|---|
| Expect from | DEL-03-01/C-v0.1 | Operation identity/version, input/effects/errors, availability results, basis descriptor, relied-on basis reference (§3.2) |
| Expect from | DEL-04-01 | Adopted class values and act names (accept, reject, mark checked, approve, rely, withdraw) or `UNRESOLVED{OI-001/002}` |
| Expect from | DEL-04-02 | Grant in force per operation class; during-work changes |
| Expect from | Host owner | Route, validation outcomes, receipts, origin marks, undo route, views, recorded acts, stale rule (U-C3), generation meaning |
| Provide to | DEL-04-02 | Direct-autonomy origin semantics (§4.4), standing per outcome (§9) |
| Provide to | DEL-04-03 | Outcome taxonomy (§9), receipt references (link, not copy), origin (§3.3), act/evidence table (§10) |
| Provide to | DEL-03-03 | This contract unchanged for the external channel; *channel not enabled* and *not permitted* outcomes |
| Provide to | DEL-05-01 / DEL-05-02 | Proposal elements for loop tools; queue/state/old-new/reason for the panel; "accept" wording |
| Provide to | DEL-03-04 | §1 authority map and this table |
| Provide to | DEL-09-09 | §11 scenario, §12 risks, VC-P cases and expected outcomes |
| Provide to | DEL-03-01 | M3-CP return (§11) |
| Provide to | Host proposal views | §8 information |

## 14. Examples (invented fixture subjects)

All material is **invented**: model FX-PIPE-01, operations OP-C1…C6 as
defined in DEL-03-01/C-v0.1 §10, invented people ("Engineer A") and values.
Labels are fixture labels, not identities, wire names or SWBPIPE
commitments.

**E-1 Proposal P-2 as the host view would show it (after §11 step 7):**

| Item | Object | Attribute | Old (at r13) | New | Why | Origin | State |
|---|---|---|---|---|---|---|---|
| 1 | new support on R-100 at 4.2 m | created | — | guide support | Span S-2→S-3 exceeds spacing check (OP-C3 finding) | agent, conversation K-7, workflow "supports-adjust" v0.3 run 12 | queued |
| 2 | S-3 | stiffness | rigid | 2.0e6 N/m | Reduce thermal restraint | same | queued |

**E-2 Truthful reports:**

| Situation | Correct report | Incorrect report |
|---|---|---|
| Submit succeeded | "P-2 queued (2 items); awaiting your decision" | "P-2 applied" / "accepted" |
| Engineer A accepted item 1 only; not yet applied | "Item 1 accepted by Engineer A; not yet applied" | "Item 1 applied" |
| Applied with receipt | "Item 1 applied, receipt ⟨R-…⟩, now r14" | "Item 1 approved" |
| Direct application under grant for a low-consequence class | "Applied under your grant; origin-marked; undo available" | "Accepted" |
| Acknowledgment lost | "Outcome unknown; last observed: queued" | "Applied" or "failed" |

## UNRESOLVED

| Item | Owner | Point of need | Effect on this definition |
|---|---|---|---|
| `UNRESOLVED{OI-001}` always-reserved acts per operation (incl. who may withdraw/reject) | Owner with App/SWB contract owners; carried by DEL-04-01 | Before operation-policy production contract | *Not permitted* outcome and direct branch cannot be exercised for unruled classes; no act class selected |
| `UNRESOLVED{OI-002}` classifier routine-permission treatment | Owner with App/SWB contract owners | Before permission-policy implementation | Kept distinct from human acts (§10) |
| `UNRESOLVED{OI-003}` extension promise | Owner with host contract owner | Before extension claim | Not decided here; route parity (§2) required regardless |
| `UNRESOLVED{OI-014}` shared contract/component placement | App/shared contract owners (DEP-03-02-025) | Before structural/production allocation | No placement implied |
| `UNRESOLVED{OI-021}` first connected operation, autonomy, environment | Owner via outside SWB session and App/shared owner | Before connected SoW/execution | §11/§14 invented only |
| U-P1 Proposal identity representation, encoding, duplicate-effect enforcement, outcome-recovery mechanics (TBD-002) | Relevant contract and host owners (DEP-03-02-026) | Before dependent implementation | §7 obligation testable; mechanism open |
| U-P2 Actual host route, views, receipts, act recording (DEP-001) | Host owner / SWBPIPE (DEP-03-02-023) | When integration/witness relies on them | All behavior here is receiving meaning; no host conformance claimed |
| U-P3 Disposition when basis fails after *accepted*, before *applied* | Host owner with DEL-03-02, DEL-04-03 (lapse) | Before application-path implementation | §4.2 requires no application; name/treatment open |
| U-P4 Validation failure before queueing: state treatment | Host owner | Before adapter implementation | Proposed: refusal, remains drafted |
| U-P5 Whether the host may *reject* (vs refuse) at application, and its actor labeling | Host owner; DEL-04-01 act names | Before outcome recording | Rejected carries actor; host refusal kept distinct from person's rejection |
| U-P6 Who may withdraw (agent own-proposal vs person) | Owner with App/SWB contract owners (OI-001 lineage); DEL-04-01 | Before withdrawal implementation | Actor recorded; class unset |
| U-P7 Item application grouping (separate vs one application of accepted items) | Host owner | Before application-path implementation | Item-level dispositions defined; grouping open |
| U-C3 / U-C4 (shared with DEL-03-01) stale rule and multi-read reliance | Host owner with DEL-03-01/DEL-03-02 | Before stale implementation | §5 trigger defined abstractly |

## Verification cases

Designed, **not run**. Evidence class to be labeled at execution:
*illustrative*, *test-double*, *actual host* (VER-002, VER-009 require it).

| Case | Design | Expected result | Serves |
|---|---|---|---|
| VC-P-01 Coverage | Map §§1–13 to the twelve scope rows (SOW-070, 090, 091, 170–178), V4-HI-20–25 and C-v0.1 elements | Every scope row covered; every representation choice named as open with owner | VER-001 |
| VC-P-02 Channel parity | Same OP-C4 request, arguments, basis, authority via person, embedded, external; plus invalid and stale variants | One route identity; identical outcome/error meanings; only authority-derived *not permitted* differs, with policy cited; no alternate agent path | VER-002 |
| VC-P-03 Host authority / no upgraded result | Agent drafts and submits P-2; no host acceptance recorded | Reported *queued*; never *accepted* or host-accepted; domain truth only in host | VER-003 |
| VC-P-04 Origin and basis preservation | Trace P-2 from draft to receipt | Author type, conversation, workflow run/version, channel and relied basis B2 identical at every step and in outcome | VER-004 |
| VC-P-05 Lifecycle branches + direct case | Exercise queued→accepted→applied; rejected; withdrawn; stale; and a direct application under grant | Each state with its evidence; applied carries receipt; direct case records no acceptance | VER-005 |
| VC-P-06 Unknown outcomes | (a) applied but acknowledgment lost; (b) submission whose application is not established | Both report *outcome unknown* with last observed state; no inferred success, failure or human act | VER-006 |
| VC-P-07 Stale and re-draft | §11 steps 1–6 | Refusal with reason, B1 and B2; P-2 new identity, lineage to P-1, relies on B2 | VER-007 |
| VC-P-08 No retargeting | Draft for S-3; person selects S-4; submit and inspect | Bound targets and affected objects remain S-3/R-100 | VER-008 |
| VC-P-09 One effect | Submit P-2 twice; retry after lost acknowledgment | One application per item; repeat returns same receipt; unobservable case stays unknown; record exercised scope without global exactly-once claim | VER-009 |
| VC-P-10 Host view info | Inspect E-1 against V4-HI-24 | Old, new, affected objects, reason, origin present; host named as view/receipt producer | VER-010 |
| VC-P-11 Execution vs acts | Success without act evidence; separately evidenced acceptance, checked, approval, reliance | Success asserts execution only; each act claim backed by its own evidence; none inferred from another | VER-011 |
| VC-P-12 Queued/accepted/applied/unknown reporting | Submitted-only; accepted-only; accepted-and-applied; interrupted | queued; "accepted, not applied"; applied with receipt; unknown — compared against host records | VER-012 |
| VC-P-13 Policy interface | Review §§4.4, 9, 10 against CLM-004, #d3, OI-001/002 | Routine permission, direct application, acceptance and other acts distinct; unruled values shown as `UNRESOLVED{OI-001/002}`; no blanket approval policy | VER-013 |
| VC-P-14 Boundary audit | Check REQ-013 exclusions one-for-one against §1 and §13; run registered boundary-owner checker when available | Each excluded act resolves to its owner; twelve scope rows retained; no sibling/external completion claimed | VER-014 |
