# Operation-Policy and Human-Act Contract
- Contribution: DEL-04-01/ACT-POLICY-v0.2 (supersedes ACT-POLICY-v0.1, sha256 e6457535ef2ffae27efc426c454e7206928c4049272ad7af7adfd1b6368e3763)
- Status: DRAFT DEFINITION — proposed, unsupplied, not implemented, not accepted
- Serves: OUT-001, OUT-002, OUT-003; REQ-001…REQ-007; VER-001…VER-009 (AC-001…AC-009)
- Basis: repo 6e18505e3; ScopeOfWork.md sha256 fc1a0503abad4196e869402b664bd76280773d197b5c77994c34e858a406f5e6; `P/docs/PRD.md` §4.1 (V4-WF-02, -05), §4.3 (V4-EXE-02), §4.5 (V4-AUT-01…05), §4.7 (V4-REC-05), §9 (OQ-02, OQ-11), §10; `P/docs/HOST_INTEGRATION.md` §2 (V4-HI-02, -04), §3 (V4-HI-11, -12), §4 (V4-HI-20…25), §5 (V4-HI-30…33), §6 (V4-HI-40…42), §7 (V4-HI-50…52), §9 (V4-HI-70/71); `P/docs/EXAMINATION.md` V4-EXM-20, -21, -22, -25, -31; `P/execution/_Coordination/Acceptances/APP-V4-BASIS-20260926/DECISION_BRIEF.html#d3` (sha256 02d38cb18041c52989d8a2a0b969e6502ce4b25eec85fb0931bbbc100c4420e8); `P/conceptual/DECISIONS.md` OD-05, D-04; `P/conceptual/EXEMPLARS_AND_LESSONS.md` X-09, X-19, X-20; `P/execution/_Decomposition/Open_Issues.csv` OI-001, OI-002, OI-013, OI-014, OI-021; `P/execution/_Decomposition/External_Dependencies.csv` DEP-001
- Consumed inputs:
  - Owner decision `APP-V4-FIRST-INCREMENT-20260928-DECISION-1`: D2 (OI-001) and D3 (OI-002), from `AgentRuns/APP-V4-FIRST-INCREMENT-20260928/OWNER_DECISIONS.md` (sha256 f3f8e5f31ec87006fc9ab459c6ae57d08638439c234fa959ba2605914cf81f2e).
  - Integration resolutions R-1…R-9 from `R1_RESOLUTIONS.md` (sha256 2f9c7e72aa8362624ad830377a70077b27a27bf03871f8e87811a28e6e177ec4). This file owns R-1…R-4 and the DEL-04-01 parts of R-5/R-6.
  - V1 comparisons:
    - `comparisons/V1-A.md` (sha256 01811533bf0aedad5326d1517561187682a572ae3f47c5f8b8637e48cfe04c09);
    - `V1-B.md` (sha256 09eebfe0ed78058a412d83998277d1385d1c7d9b28d79b37a8726bb39b3c1cae);
    - `V1-C.md` (sha256 8d46258ad0120067f6472442de67feacba8405462b78abb8bac34be28a4a94a6).
  - DEL-03-01/C-v0.1 §4.1 and §10 fixture catalogue (sha256 c13518c9453e65a57f6e90ea87c9c4133cc1baea3af4629edb28acbf1d0a0b72), cited per R-9.
  - Other receivers' v0.1 designs are known only as V1 quoted them. Their v0.2 is not yet received.
- Receivers:
  - DEL-04-01 is not a SCC-CASE-002 member.
  - Receivers from `Dependencies.csv` DEP-04-01-012…016: DEL-02-01, DEL-02-03, DEL-03-01, DEL-04-02, DEL-04-03.
  - Receivers that declare this deliverable upstream in their own registers: DEL-03-02 (DEP-03-02-017), DEL-03-03 (DEP-03-03-008), DEL-05-01 (DEP-05-01-018), DEL-05-02 (DEP-05-02-008/-014/-015), DEL-01-04 (DEP-01-04-011), DEL-09-09 (DEP-09-09-010).
  - DEL-01-01 receives the D3 value (V1-A D-13).
  - Further declared consumers are listed in §10.3.

`P` = `projects/chirality-app-v4`. All element names in this document are
**semantic names, not wire names**. Examples are *act kind*, *decision actor*,
*recorder*, *recording mode*, *change-item content identity* and *treatment*.
This definition selects none of the following:
- a field name or type;
- a transport;
- a hash or canonicalization algorithm;
- persistence;
- process placement or shared-component placement (OI-013, OI-014).

Open policy appears only as `UNRESOLVED{…}`. It is never a permission, a
default choice or a pass.

---

## Changes from v0.1

| V1 item | How addressed in v0.2 |
|---|---|
| V1-A D-01 (BLOCKING), D-17, D-18, D-20; V1-C D-17 | §2.1 canonical names A1–A14 with alias map (R-1). "Accepting professional reliance" maps to A7 *rely*. "Accept" stays with A5 only. V4-CON-05/V4-HI-65 design-candidate approval is excluded from A6. A9 is a recording act with *recording mode* (direct capture \| faithful recording). A12 is a named act. The acts a checkpoint may require form a closed list: A4, A5, A6, A7, A12 (§4.1). |
| V1-A D-02; V1-B D-08 | The SWB model-change class is *may apply within granted autonomy*, marked DERIVED from V4-HI-41, with default *propose*. OI-021 additions are pending (§7, §8.3 record P-03). |
| V1-A D-03 | DERIVED reserved class for operations that perform or record A4–A7, A12 or A13 as the person's act (§8.3 record P-02). DEL-03-01 OP-C6 carries it. |
| V1-A D-04 | Channel off is reported as **channel not enabled**, distinct from **unavailable** (§5.3 rule 1, §6). FX-24 updated. |
| V1-A D-05, D-08 | Treatment → runtime-outcome map (§6, R-3). Treatment is resolved on the host route at validation and again at application. The in-flight rule is stated in §5.5. U-09 is closed. |
| V1-A D-06, D-07; V1-B D-12 | Cited, not redefined here. Requester and setting actor are separate. A person-set state needs A12 evidence. The grant has a scope element (R-8). U-08 is closed. |
| V1-A D-09; V1-C D-07 | An acceptance checkpoint forces the operation's treatment to *propose* (§4.4, DERIVED, R-5). New fixture FX-29. |
| V1-A D-10; V1-C D-03 | Decision pairs (A5 ↔ A10). For A4, A6, A7 and A12, not acting is a recorded decline or stop event, not an act (§2.3, §4.3). New fixtures FX-30 and FX-31. |
| V1-A D-11; V1-C D-06 | S3 and A9 reconciled. Any identified recorder distinct from the decision actor is a conformant record shape. Checkpoint satisfaction needs attributable evidence from the capturing surface (§4.5). The host's capture requirement is DEP-001. The OI-001 tag on recorder allocation is removed. |
| V1-A D-12; V1-B D-15 | "Checked" label rule (§9, R-4). New fixture FX-34. |
| V1-A D-13, D-14 | A14: affirmative answers come only from the person or the user's own Codex mode (D3). The App may only decline or return an error, under a named rule with truthful origin. DEL-01-01 is added as a V-21 consumer. New fixture FX-33. |
| V1-A D-15; V1-B D-23 | A11 *withdraw* is the proposer's act only. A person removing another party's proposal is A10 *reject* (R-1). A10 is DERIVED as reserved wherever A5 is. |
| V1-A D-16, D-24 | A host refusal is an A2 outcome (*refused*), never A10. Outcome vocabulary follows DEL-03-02 P §9 (R-7). |
| V1-A D-19 | §2.4 adds an optional *governing policy reference*. It is present when a catalog operation governed the act and may be absent for an act in the host UI with no operation. |
| V1-A D-21, D-22, D-23 | D-21 is resolved by the §4.5 evidence rule, applied uniformly to A4–A7. D-22: the grant value *propose* is distinguished from the *proposal only* class (§5.4). D-23: OI-002 is not a class value (§5.1). |
| V1-A D-25; V1-B D-01, D-10 (DEL-04-01 parts) | A5 binds to the change-item content identity (DEL-03-02), one binding per item. Batch or multi-row acceptance is one A5 listing several items, each with its own lapse. Applying an item does not lapse its acceptance. A basis failure goes to the stale rule. What purpose a multi-row A4 keeps after partial lapse is an owner question (U-03). |
| V1-A AB-01 | Unconfirmed or non-effective grant → no direct application; *propose* stays available (§5.3 rule 7). |
| V1-A AB-02 | Workflow registration is not added to R-1's canonical table. It is held as U-08 (DEL-04-01 with DEL-02-02, later undertaking under D1). |
| V1-A AB-03; V1-C D-05 | Lapse can happen at any time and is always recorded. A lapse before resume returns the checkpoint to waiting. Whether a lapse after resume re-holds the run is owned by DEL-02-03 (§4.3, U-10). |
| V1-A AB-04 | Consequence vocabulary is still open (U-02). The policy-class record keeps a consequence statement. |
| V1-A AB-05; V1-B X-10 | A14 settlements are never human-act records and never grant entries. Where they are recorded is DEL-04-03 with DEL-01-01 (U-07). |
| V1-A AB-06 | The host capture requirement per act kind is DEP-001 (U-04). |
| V1-A AB-07 | Consumers cite the *policy revision identity* of this contribution in their governing-policy element (§8.1). |
| V1-A AB-09 | OI-021 operation-specific additions are held as U-01. |
| V1-A AB-10; V1-B X-09 | D2 and D3 are carried as adopted decision records in §8.3 (P-01, P-04). |
| V1-A §5 rows for 04-01 | §3 "Not settled" is rewritten as "Adopted rulings". §10 owner questions are narrowed. FX-16, FX-18 and FX-23 are re-expected. U-01 and U-02 are rewritten. |
| V1-C AB-01 | Policy fact supplied: each change item has its own A5 or A10, and a still-queued item has neither (§4.3). How these combine into a checkpoint disposition is left with DEL-02-01, DEL-02-03 and DEL-03-02 (U-09). |
| V1-C AB-06 | A reserved-class entry may be offered to an agent, in which case invoking it yields *not permitted* plus A8. It may instead be withheld, reported as *not exposed on this surface*. It is never reported as *unavailable* (§6 rule 8). New fixture FX-35. |
| R-9 | Fixtures now use the DEL-03-01 §10 model FX-PIPE-01 and its entries OP-C1…C6. Divergences are stated (§13 preamble). |
| RF-01…RF-05 (register findings) | Not repaired here. They go to C1, per R1_RESOLUTIONS. F-1 retained. |

---

## 1. Purpose and reading

This contract gives consumers one meaning for:

- what an agent may do directly, what it must propose, and what only the
  person may do;
- which act happened, who performed it, what it concerned, and what evidence
  supports it.

It carries the owner's rulings D2 and D3 as adopted policy records. It performs
no human act and implements no host facility. It does not claim that SWBPIPE
has adopted or enforces any value (DEP-001).

Standing labels:

| Label | Meaning here |
|---|---|
| **SETTLED** | Stated in the accepted composite (B-ACCEPT) and cited |
| **ADOPTED** | Owner ruling `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` (D2 and D3), for App/shared contracts in the first increment |
| **DERIVED** | A direct consequence of settled or adopted clauses. The derivation is shown so a receiver can reject it. |
| **INTEGRATION** | A design choice by the R1 integrator (R1_RESOLUTIONS). It is reviewable at IR1 and open to owner revision. |
| **PROPOSED** | A design choice of this contribution, open to review |
| **UNRESOLVED{…}** | An open item with owner and point of need (UNRESOLVED table) |

---

## 2. Acts — canonical names, actor, subject, evidence

**Rule.** Evidence of one act kind never establishes another. The absence of
one act kind does not, by itself, invalidate an independently evidenced act of
another kind (REQ-002; AX-002). There is no automatic promotion between act
kinds and no universal acceptance prerequisite.

### 2.1 Canonical names and alias map (R-1)

Every consumer uses the canonical name. Basis wording listed as an alias maps
to that name. A name that is not recognized remains **not established** and is
never matched to a nearby act kind.

| ID | Canonical name | Aliases in the basis mapped to it | Decision actor | Subject | Supporting evidence | Does **not** establish | Policy standing | Basis |
|---|---|---|---|---|---|---|---|---|
| A1 | **propose** | draft/submit a proposal | Agent (embedded or external) or the person | One proposal of one or more change items against a cited read basis. Each item has targets, old and new values and a reason. | Host proposal record with origin and relied-on basis; lifecycle state | Acceptance, application, checking, approval, reliance | Agent-available | V4-HI-21, -23, -24, -25; d3 |
| A2 | **apply** | execute an operation; direct application | The person; an agent under an effective direct treatment; the host route after acceptance | The operation invocation and its effect on identified objects | Host receipt, origin mark and observed outcome per DEL-03-02 P §9 (R-7) | That any person accepted, checked, approved or relied on anything | Governed by treatment (§5) | V4-HI-20, -22, -23, -25, -71; d3 |
| A3 | **examine** | agent check, examination, findings | Agent | Identified rows, results or models, by read basis | Findings attached by reference, with grounds and limitations. No table change. | A4, A5, A6, A7 | Agent-available | d3; V4-EXM-21 |
| A4 | **mark checked** | marking work checked | The person | Identified host rows/objects or App file content, with scope and purpose | Attributable act evidence from the capturing surface (§4.5), bound to subject content identity | A5, A6, A7 | **Reserved** (ADOPTED D2a) | V4-AUT-03; V4-HI-30, -32; V4-REC-05; X-20 |
| A5 | **accept** | accept an edit; accept a proposed edit; acceptance of a proposed edit | The person | One or more identified **change items**, each bound to its change-item content identity (§2.5) | Attributable act evidence from the capturing surface, listing the items. The label shown is "accept". | A6, A4, A2 (application has its own receipt) | **Reserved** wherever the active autonomy requires a proposal (ADOPTED D2b) | V4-HI-23, -25, -33, -41; d3 |
| A6 | **approve** | engineering approval (V4-HI-30/33) | The accountable person | Identified engineering content or design | A separate attributable approval record | A7 or any certification unless separately stated | **Reserved** (ADOPTED D2c) | V4-HI-30, -33; V4-AUT-03 |
| A7 | **rely** | professional reliance; "accepting professional reliance" (d3; V4-CON-05 wording) | The accountable professional only | A result relied on for a stated professional purpose | The professional's own attributable statement | Anything about agent output. It is never inferred from A1–A6. | **Reserved** (ADOPTED D2d; SETTLED V4-AUT-05, V4-HI-30) | V4-AUT-05; X-09 |
| A8 | **request** | prepare or request a person's act | Agent | A decision request naming the exact act kind, subject and purpose | The request and its content | Anything. A request is never the act. | Agent-available | V4-AUT-03; V4-HI-31; V4-PM-04 |
| A9 | **record** | faithful recording (actor ≠ recorder); direct capture | *Recorder*: the capturing surface, the host facility, the App, an agent, or the person | An actually performed act of kind A4–A7, A10, A12 or A13 | Reference to the act's own evidence, plus recorder identity and *recording mode* ∈ {direct capture, faithful recording} | The act itself. **A9 is a recording act by the recorder, not a decision act.** On its own it never satisfies a checkpoint (§4.5). | Any identified recorder distinct from the decision actor is a conformant record shape (SETTLED S3). Host capture requirement: DEP-001. | SoW REQ-002; d3; V4-HI-31; R-1; R-5 |
| A10 | **reject** | reject a proposal or proposed item; a person removing another party's proposal | The person | One or more identified change items | Host lifecycle record `rejected` with the actor | Anything beyond non-acceptance of those items | DERIVED: **reserved** wherever A5 is. It is the decision pair of A5. | V4-HI-23; V4-EXM-20; R-1 |
| A11 | **withdraw** | withdraw one's own proposal | The proposer only | Its own proposal | Host lifecycle record `withdrawn` | A human decision on the proposal's merit | Proposer's act | V4-HI-23; R-1 |
| A12 | **set grant** | set or change the autonomy grant | The person | Operation classes, treatment and person-set scope (§5.4) | Attributable act evidence from the control surface, referenced from the run's settings | That an agent's request (A8) established anything | **Reserved** (ADOPTED D2e) | V4-AUT-01; V4-HI-40, -41 |
| A13 | **enable external access** | enable or disable external-agent access | The person | The host's external interface on this machine | Recorded enablement or disablement | Any grant for an operation class | **Reserved** (ADOPTED D2e); off by default and local (SETTLED) | V4-HI-52 |
| A14 | **answer tool permission** | harness "approval" of tool use; routine tool permission | The person, or the user's own Codex permission mode inside the supplier (D3) | One tool-execution request | Request settlement: answered, or explicitly declined or errored. Never settled by silence or timeout. | Any of A4–A7, A12 or A13, or a host-operation grant | ADOPTED D3. The App never answers affirmatively by rule. An App decline or error is allowed only under a named rule with truthful origin. Hosts have no classifier mode. | V4-AUT-04; V4-EXE-02; D3; R-2; R-10 |

Alias exclusions (R-1):

- **Design-candidate approval** is a separate act of a later increment, outside
  this one (V4-CON-05; V4-HI-65 "design candidate for human approval"). It is
  **not** A6.
- The word **accept** belongs to A5 alone. Basis wording such as "accepting
  professional reliance" maps to A7 *rely*.

Other human acts named in the basis keep the same attribution invariants but
are not given canonical names here:

- workflow registration (V4-WF-02) — U-08;
- stopping work (V4-EXE-01);
- reserved coordination decisions (V4-PM-04).

### 2.2 Direct application is never acceptance

When an effective direct treatment lets an agent apply a change, the act is
A2. It is never recorded as A5. SETTLED S3: an agent is never the decision
actor of A4–A7. D2(b) reserves A5 wherever the autonomy requires a proposal.
Wherever A5 is performed, only the person performs it.

### 2.3 Decision pairs and decline events (R-5)

| Required act | Positive | Negative | Standing of the negative |
|---|---|---|---|
| A5 | accept | A10 reject | A10 is an act (the decision pair). Per item. |
| A4, A6, A7, A12 | the act | **decline/stop event** by the person | A recorded event. It is **not** an act of that kind and does not satisfy anything that requires the act. |

A decline event records its actor, subject and time. It never records the
declined act as performed.

### 2.4 Recorded-act element meaning

This is the meaning DEL-04-03 receives. DEL-04-03 owns the format.

| Element | Meaning | Presence |
|---|---|---|
| *act kind* | A canonical name from §2.1 | Always |
| *decision actor* | The person who actually performed the act | Always |
| *recorder* and *recording mode* | Who wrote the record; direct capture or faithful recording (A9) | Always |
| *subject content identity*, *scope*, *purpose* | What the act concerned (§2.5) | Always |
| *evidence reference* | Evidence of the act from the capturing surface, linked and not copied (V4-HI-71) | Always. Without it, a person-attributed record is not a conformant record. |
| *lapse state* | Relative to current content (V4-HI-32) | When applicable |
| *governing policy reference* | Policy-class record and policy revision identity (§8.1) under which a catalog operation governed the act | Optional. Present when a catalog operation governed the act. |

These records are non-conformant:

- a record that names the recorder as the decision actor of an A4–A7, A10 or A12 act;
- a record whose person-attributed act has no evidence reference.

### 2.5 Content binding and lapse (S6; R-6)

| Act | Bound content (c₀ source) | Lapse |
|---|---|---|
| A5, A10 | **Change-item content identity** (DEL-03-02): operation identity and version, bound targets, old and new values, relied-on basis | Per item. **Applying the accepted item does not lapse the acceptance.** A basis failure between acceptance and application falls under the stale rule (DEL-03-02 U-P3), not lapse. A re-draft is a new proposal, and the earlier acceptance does not carry over. |
| A4, A6, A7 on host content | **Subject content identity** (DEL-03-01), one per object or row, host-supplied | Per subject. A change to the bound row lapses the act for that row. An unrelated edit elsewhere does not. |
| A4, A6, A7 on App files | File content identity (DEL-04-03) | Per file or scope |
| A12, A13 | The setting the act establishes | PROPOSED: a later A12 or A13 supersedes the earlier one. No lapse is defined. |

- Batch or multi-row acceptance is one A5 act listing several items. Each item
  is bound and lapses on its own (R-6; V4-HI-41).
- Row-by-row acceptance is one A5 per item.
- What purpose a **multi-row A4** keeps after some of its rows lapse is an
  owner question (U-03).
- Every content identity carries its identity-method designation. The
  algorithm is unselected (R-6).

---

## 3. Settled distinctions S1–S12 and adopted rulings

Each distinction below was checked against the cited bytes at repo 6e18505e3.

| ID | Settled distinction | Citation | Consequence for consumers |
|---|---|---|---|
| S1 | Graduated autonomy per kind of operation: the agent proposes for acceptance or applies directly within a scope the person sets, with origin marks, undo and later checking. | PRD V4-AUT-01; HI V4-HI-22, -40; D-04 | Treatment per class and grant (§5). Direct application carries origin, undo route and later-check route. |
| S2 | Every result's standing is visible so the person can judge the validation warranted. | PRD V4-AUT-02; HI V4-HI-12; X-19 | No presentation stronger than the evidence (DEL-04-02) |
| S3 | Agents may prepare checking, acceptance and reliance decisions. They must not represent an act as performed when it was not. Faithfully recording an actually performed act is allowed, with actor ≠ recorder. | PRD V4-AUT-03; HI V4-HI-31; d3; SoW REQ-002 | A1/A8 are permitted. Fabrication is prohibited. A9 is a record shape. |
| S4 | Nothing the agent produces is presented as certified, sealed, approved or code-compliant. | PRD V4-AUT-05; X-09 | A7 is never inferred. Standing labels exclude these claims. |
| S5 | `success` means the operation ran, never that a person accepted anything. A proposal is "queued" until acceptance and application are recorded. | HI V4-HI-23, -25 | A2 ≠ A5 |
| S6 | A human act binds to its content, scope and purpose and lapses visibly when that content changes. | HI V4-HI-32; PRD V4-REC-05; X-20 | §2.5 |
| S7 | Acceptance of a proposed edit is not engineering approval. Proposals say "accept", never "approve". | HI V4-HI-33 | §9 |
| S8 | Conservative defaults for consequential operations. SWB model changes default to proposal with row, multi-row or whole-batch acceptance, and the person may widen it. | HI V4-HI-41 | §7 |
| S9 | Declared checkpoints override autonomy. The run waits for the person's act. | HI V4-HI-42; PRD V4-WF-05 | §4 |
| S10 | External agents act through the same catalog, validation, autonomy settings and reserved acts. They cannot perform a reserved act. External access is off unless enabled, and it is local. | HI V4-HI-50…52 | §5.3 rules 1 and 4 |
| S11 | Agent examination is its own useful activity and need not modify the model. | d3; V4-EXM-21 | A3 ≠ A4 |
| S12 | Shared access does not transfer decision rights. | PRD §4.5 lead; OD-05 | Parity never gives an agent A4–A7 |

**Adopted rulings (DECISION-1).** These supersede v0.1's "Not settled"
paragraph and the pending status of DECISIONS_PENDING D2/D3.

- **D2 (OI-001), first increment, App/shared contracts.** The following are
  reserved to the person:
  - (a) marking work checked;
  - (b) accepting a proposal wherever the active autonomy requires a proposal;
  - (c) engineering approval;
  - (d) relying on a result for a professional purpose;
  - (e) changing the autonomy grant or enabling external-agent access.

  No grant widens past a reserved act or a declared checkpoint. The host names
  and enforces its own list (V4-HI-30). Operation-specific additions come when
  the concrete SWB operation is selected (OI-021). The ruling does not show
  host adoption or enforcement (DEP-001).
- **D3 (OI-002).** In the App, routine tool-permission and sandbox modes,
  including any classifier-based mode, remain the user's own Codex setting per
  project and turn. They govern tool execution only and never stand in for a
  reserved or professional act. Hosts have no classifier permission mode in
  the first increment; the SWB default proposal mode applies (V4-HI-41).

**Historical, still not ruled.** The original-seed V4-HI-30 "at least" list
(`…/original-seed/HOST_INTEGRATION.md` lines 90–92) and the V4-AUT-04 prior
drafting default remain historical (AX-001). D2 and D3 are the governing
values. d3's treatment table remains a proposed interpretation only.

---

## 4. Checkpoints (R-5)

DEL-02-01 declares checkpoints. DEL-05-01 evaluates them in hosts. DEL-02-03
owns the hold machine (W7). This section supplies the act-policy meaning they
consume.

### 4.1 Acts a checkpoint may require (closed list)

A declared checkpoint requires exactly one of **A4, A5, A6, A7 or A12**
(DERIVED from R-1 and V1-A D-20). A declaration naming any other act kind, or
an unrecognized name, is reported **not established** (DEL-02-01 FB-04). A9,
A8, A2 and A14 are never checkpoint acts.

### 4.2 Reached-when and subject binding

- Each checkpoint declares an observable *reached-when* condition. The meaning
  alone is declared; the representation is not. The condition is one of:
  - before dispatch of a named required-tool reference;
  - on observed production of a named declared output;
  - on an observed host outcome of a named operation (for example, proposal
    queued).

  A run that ends without the condition being observed reports the checkpoint
  **not reached**, never satisfied.
- The checkpoint's subject is bound at run time to an observable referent: the
  proposal and its change items, the output, or the rows produced. The
  satisfying act must be bound to that same referent's content (§2.5).

### 4.3 Dispositions and negatives

Shared vocabulary: **waiting · performed · resolved negatively · lapsed · not
reached · unknown**.

- **performed** requires evidence of the required act kind on the bound
  subject (§4.5).
- **resolved negatively**:
  - for A5, an A10 on the subject's items;
  - for A4, A6, A7 or A12, a recorded decline/stop event (§2.3).

  The declaration's "on negative decision" path governs what happens next.
  A negative never counts as *performed*.
- For an A5 checkpoint over several change items, each item carries its own A5
  or A10. An item that is still queued carries neither. How mixed item
  outcomes combine into one checkpoint disposition is owned by DEL-02-01 with
  DEL-02-03 and DEL-03-02 (U-09).
- **lapsed**:
  - Lapse can happen at any time after performance, and it is always recorded
    and presented.
  - A lapse before the run resumes returns the checkpoint to *waiting*
    (DERIVED from S6 and S9).
  - Whether a lapse after resume re-opens the hold is owned by DEL-02-03
    (U-10).
- **unknown** is used when observation was lost. It is never shown as
  *performed*.

### 4.4 An acceptance checkpoint forces proposal (DERIVED from V4-HI-42 + D2b)

If a declared checkpoint requires A5 on an operation's result, that
operation's treatment in that run is **propose**, whatever the grant. A direct
request for it is *not permitted* (§6). A workflow that wants direct
application followed by a person's act must instead require A4 on the applied
rows.

### 4.5 Which evidence satisfies a checkpoint

- Any identified recorder distinct from the decision actor is a conformant
  **record shape** (A9, SETTLED S3).
- **Satisfaction** requires attributable act evidence from the **capturing
  surface**:
  - the host's act facility, for acts on host content (V4-HI-31);
  - the App interface, for acts in the App.
- A faithful record by another recorder is valid as a record, and it must cite
  that evidence. The loop resumes on the capturing-surface evidence, never on
  an agent-authored record alone.
- Any host-specific capture requirement belongs to the host (DEP-001; U-04).

---

## 5. Autonomy-grant model

### 5.1 Inputs (semantic)

| Input | Meaning | Supplier |
|---|---|---|
| *operation identity* and *operation class* | The catalog operation and its host-named class | DEL-03-01 (V4-HI-01/02). The host names classes (V4-HI-30). |
| *catalog human-act class* | none \| may apply within granted autonomy \| proposal only \| reserved to the person \| *no policy basis* | Vocabulary SETTLED by V4-HI-02. Values come from §8 records. OI-002 is **not** a class value (D3; R-2). |
| *consequence statement* | Effect, reversibility, available examination, intended delegation (d3 dimensions) | Vocabulary open (U-02) |
| *grant state* for the class | effective \| requested by agent (A8) \| set by person, not yet confirmed \| unconfirmed \| not set \| refused (reason); each with treatment direct/propose and scope | DEL-04-02 (R-8). A person-set state requires A12 evidence. |
| *host default* | Conservative default for a consequential class | Host (V4-HI-41). SWB model change: §7. |
| *checkpoint state* | Whether a declared checkpoint applies and which act it requires | DEL-02-01; DEL-02-03; DEL-05-01 |
| *actor* | The person, the embedded agent or an external agent | Host route |
| *external enablement* | A13 state on this machine | The person; the host |

### 5.2 Treatments

| Treatment | Meaning |
|---|---|
| **execute** | Run with no associated human act, for example a read or A3. The result carries its standing (S2). |
| **apply directly** | The agent applies (A2) through the host's one route, with origin, relied-on basis, undo route and later-check route (V4-HI-20…22) |
| **propose** | The V4-HI-23 lifecycle. The proposal is queued until acceptance and application are recorded (S5). |
| **request the person's act** | The agent may only request (A8). The person performs the act through the capturing surface. |

### 5.3 Resolution order for an agent actor

**Where it is resolved.** Treatment is resolved on the **host route**, first at
validation and again at application (V4-HI-20/22/40). The loop (DEL-05-01) and
the external adapter (DEL-03-03) relay the actor's intent. They do not decide
treatment (R-3.1, INTEGRATION).

The first matching rule applies.

1. **External actor, A13 not performed (access off)** → outcome *channel not
   enabled* (§6). SETTLED S10; V4-HI-52.
2. **A declared checkpoint applies**:
   - at a checkpoint, the run waits for the required act → *request the
     person's act* (S9);
   - an A5 checkpoint on this operation's result forces *propose* (§4.4).
3. **The operation performs or records A4–A7, A12 or A13 as the person's act**
   → *request the person's act*. SETTLED S3 and S4; ADOPTED D2. The operation
   carries the class *reserved to the person* (§8.3 P-02).
4. **Catalog class = reserved to the person** → *request the person's act*.
   ADOPTED D2; S10 for external agents. Operation-specific additions are
   pending OI-021 (U-01).
5. **Catalog class = *no policy basis*** → direct is **not permitted**, and
   *propose* is available (R-3.5, INTEGRATION; conservative default, V4-HI-41).
   A class is *no policy basis* when it is omitted, unassigned, or
   `UNRESOLVED{OI-021}` for a concrete operation. This never counts as a
   permission to apply, and it never counts as a conformance pass for
   dependent production (REQ-004; F-5).
6. **Catalog class = proposal only** → *propose*. No grant can widen it.
7. **Catalog class = may apply within granted autonomy**:
   - grant state **effective** with treatment *direct*, and the operation
     inside the person-set scope → *apply directly* (S1; R-8);
   - any other grant state (requested by agent, set but not confirmed,
     unconfirmed, not set, refused), or treatment *propose* → *propose*. Where
     no grant is set, the host's conservative default applies (S8). If a
     consequential class has no host-named default, it is treated as rule 5
     (U-06).
8. **Catalog class = none** → *execute*. DERIVED caution: V4-HI-02 does not say
   that "none" implies no effect. An effectful operation assigned "none" needs
   its own decision basis (§8).

For the **person** as actor, operations go through the same route and
validation (V4-HI-20). Agent grants do not gate the person. The person's acts
are attributed to the person. A person performing A12 or A13 is the reserved
act itself.

### 5.4 Person-set scope and grant states

- The grant is set by the person (A12), per operation class, with a **scope**
  element. The dimensions are representation-neutral: for example model or
  workspace, object set, run, period, consequence (R-8). U-08 of v0.1 is
  closed.
- The grant value **propose** (the person keeps proposals, as in V4-EXM-22
  "keeps proposals for model geometry") differs from the catalog class
  **proposal only**. The person can widen the first but not the second.
- Settings-in carries **requester** and **setting actor** separately. An
  agent-originated change is *requested by agent (A8)*. It is not effective
  until the person performs A12 (D2e; R-8).
- The treatment recorded for an operation is the one the host route resolved.
  Two settings references are recorded per operation (R-8):
  - the one in force at the route decision (validation);
  - the one in force at application, as host-reported. Otherwise it is
    **unconfirmed**.

  When the proposal's standing at drafting differs from the treatment at
  resolution, both are recorded (R-3.6). A later change never re-labels an
  earlier operation.

### 5.5 Changes during work (R-3.6, R-3.7)

These rules are INTEGRATION. Host enforcement is DEP-001.

- Narrowing a grant:
  - leaves an already-queued proposal unaffected;
  - means an operation not yet applied is re-resolved at application. A direct
    request that no longer has an effective direct treatment is *not
    permitted* and is never converted into a proposal.
- Widening never converts a queued proposal into direct application.

### 5.6 Widening rule

The person may widen the grant (S8; SOW-182) by performing A12. A widened
grant:

| # | Cannot | Basis |
|---|---|---|
| W-a | make an agent the decision actor of A4–A7, A10 or A12, or fabricate any human act | S3, S4; D2 |
| W-b | bypass a declared checkpoint, including the forced *propose* of §4.4 | S9; D2 |
| W-c | authorize a reserved act or operation for any agent, embedded or external | D2; S10; REQ-006 |
| W-d | convert a **proposal only** class to direct | V4-HI-02 |
| W-e | turn a *no policy basis* class into direct application | REQ-004; R-3.5 |
| W-f | enable external access. That is A13, a separate reserved act. | V4-HI-52; D2e |
| W-g | confer professional standing | S4 |
| W-h | drop the origin, undo and later-check obligations of direct application | S1; V4-HI-22 |
| W-i | convert a queued proposal into direct application | R-3.7 |
| W-j | affect routine tool permission (A14), which is the user's Codex setting | D3 |

---

## 6. Treatment → runtime outcome map (R-3)

Runtime non-success outcomes use DEL-03-01 §4.1 unchanged. Proposal and
operation outcomes use DEL-03-02 P §9 (R-7).

| # | Situation on the host route | Runtime outcome | Also |
|---|---|---|---|
| 1 | External actor and A13 not performed | **channel not enabled** | Never *unavailable* |
| 2 | Failed catalog precondition | **unavailable**, with reason (HI-04 parity, identical for H, E and X) | Only this case is *unavailable* |
| 3 | Treatment *execute* | Operation result with standing | — |
| 4 | Treatment *apply directly* | P §9 outcome: applied with receipt; refused with reason; application error with an effect statement (none, partial or unknown); outcome unknown, attributed to the observer that lost observation | Origin, basis, grant references (§5.4) |
| 5 | Treatment *propose* | P §9 lifecycle: queued, then accepted (A5) or rejected (A10) or withdrawn (A11) or stale, and then applied with receipt | "Queued" until recorded (S5) |
| 6 | Direct requested without an effective direct treatment (rules 5 and 7, or §5.5 narrowing) | **not permitted**, naming the governing treatment and policy-class record | Never silently converted to a proposal. The agent may submit a proposal separately. |
| 7 | Treatment *request the person's act* (rules 2–4) | **not permitted**, naming the governing record | An A8 request to the person |
| 8 | Reserved-class entry offered to an agent (V1-C AB-06) | If offered: invocation → row 7. If withheld: **not exposed on this surface** (R-9). | Never *unavailable*. DEL-05-01 with DEL-03-01 chooses offer or withhold. |
| 9 | Any other failure | **error** | Evaluated basis on every non-success (R-7) |

A host refusal on validation is the outcome *refused* (A2). It is never A10
*reject* (R-7).

---

## 7. SWB model-change class — DERIVED class, accepted default

> **Class value DERIVED** from V4-HI-41 "the person may widen it". A widenable
> class is neither *proposal only* nor *reserved*, so it is *may apply within
> granted autonomy*. **Default ACCEPTED** (V4-HI-41, via B-ACCEPT).
> Operation-specific additions are pending OI-021. Host adoption and
> enforcement are **not evidenced** (DEP-001).

The policy-class record for this class is P-03 in §8.3.

Semantics:

- Row-by-row acceptance is one A5 per change item. Multi-row or whole-batch
  acceptance is one A5 act listing several items. Each item is bound to its
  own change-item content identity and lapses on its own (§2.5).
- Batch acceptance is not A4 or A6 of any row.
- Acceptance is not application. The host route applies the item, or refuses
  it as stale with both bases (V4-HI-23; P §9). The receipt belongs to A2.
- A5 on SWB model-change proposals is reserved to the person (D2b). A10 is
  reserved with it (DERIVED, R-1).

**Fixture subject (invented material; DEL-03-01 §10 FX-PIPE-01).** Run R-100,
supports S-1…S-4, revision r12. With no widening, the agent drafts proposal
P-1 with two change items:

- item 1: OP-C4 "Add support" S-5 on R-100;
- item 2: OP-C5 "Adjust run node elevation".

Both items are *propose*. Engineer A accepts item 1 (A5) and rejects item 2
(A10). The host applies item 1 and issues a receipt, which belongs to A2.
Applying item 1 does not lapse its A5.

The run record shows:

- A1 by the agent;
- A5 and A10 by Engineer A, recorded by the host facility (direct capture) or
  faithfully by the agent citing the host evidence;
- A2 through the host route, with the receipt referenced.

It shows no A4, A6 or A7.

---

## 8. Policy representation (OUT-002)

### 8.1 Policy-class record — element meaning

| Element | Meaning |
|---|---|
| *policy revision identity* | Identifies the policy content consumers cite in their governing-policy element (V1-A AB-07). This contribution's revision is DEL-04-01/ACT-POLICY-v0.2 plus its content identity. The method is unselected. |
| *class identity* | Host-named operation class (V4-HI-30), or an act-defined class (P-02) |
| *covered operations* | Catalog operation identities and versions (DEL-03-01) |
| *consequence statement* | Rationale in d3 dimensions |
| *catalog human-act class* | none / may apply within granted autonomy / proposal only / reserved to the person / *no policy basis* |
| *default treatment* | For "may apply" classes |
| *widenable* | yes (bounded by §5.6) / no |
| *acceptance granularity* | Where proposals apply |
| *actors covered* | The person, the embedded agent, external agents (same settings and reserved acts: V4-HI-50) |
| ***decision basis*** | The accepted requirement or recorded decision act fixing the value: identity, decision actor, recorder, date and custody. For open values: the open item, its owner and its point of need. |
| *decision standing* | settled-by-basis \| **adopted decision** \| DERIVED \| accepted default (host adoption unevidenced) \| INTEGRATION \| `UNRESOLVED{…}` |
| *host adoption* | Evidenced only by DEP-001 host evidence. Currently **unevidenced** for every record. |
| *consumers* | §10 |

Rules:

- No value is carried without a decision basis. Historical drafts, fixture
  expectations and pending recommendations are not a basis (AC-007).
- An open value names its item, owner and point of need. It is never rendered
  as a permission, default or pass.

### 8.2 Decision record — DECISION-1

| Element | Value |
|---|---|
| Identity | `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` |
| Decision actor | The owner (Ryan) |
| Recorder | HELP_HUMAN (Claude Code session). Faithful recording: actor ≠ recorder. |
| Date | 2026-09-28 |
| Custody | The owner's answers to a structured chat question, transcribed. Not a platform export; no platform timestamp. |
| Source | `AgentRuns/APP-V4-FIRST-INCREMENT-20260928/OWNER_DECISIONS.md` (sha256 f3f8e5f3…81f2e); package `DECISIONS_PENDING.md` at `8d3c66542` |
| Scope | First increment, App/shared contracts |
| Not established | SWBPIPE adoption or enforcement (DEP-001); `Open_Issues.csv` rewrite (closeout C1) |

### 8.3 Adopted and derived policy-class records

| Record | Class / value | Catalog class | Default | Widenable | Decision standing and basis |
|---|---|---|---|---|---|
| **P-01** Reserved acts (D2) | A4 mark checked; A5 accept (where the autonomy requires a proposal); A6 approve; A7 rely; A12 set grant; A13 enable external access | Reserved to the person | — | **No.** No grant widens past these or past a declared checkpoint. | **Adopted decision**: DECISION-1 D2(a)–(e). The host names and enforces its own list (V4-HI-30). Operation-specific additions: `UNRESOLVED{OI-021}`. |
| **P-01a** Reject | A10 | Reserved to the person wherever A5 is | — | No | **DERIVED** from D2b and R-1 (decision pair) |
| **P-02** Act-performing operations | Any catalog operation whose effect is to perform or record A4–A7, A12 or A13 as the person's act, for example DEL-03-01 OP-C6 "Mark row checked" and DEL-05-02 K-4 | Reserved to the person | — | No | **DERIVED** from S3 and D2 (R-2). Agent faithful records (A9) are not produced through such an operation (F-7). |
| **P-03** SWB model changes (for example OP-C4, OP-C5) | Host-named class | May apply within granted autonomy | propose | Yes, by A12, bounded by §5.6 | Class **DERIVED** from V4-HI-41. Default **accepted** (V4-HI-41, the owner's direction of 2026-09-17, B-ACCEPT). A5/A10 reserved (P-01, P-01a). Additions: `UNRESOLVED{OI-021}`. Host adoption unevidenced. |
| **P-04** Routine tool permission (D3) | App: the user's own Codex tool-permission and sandbox modes per project and turn, including classifier-based modes, carried unchanged. Hosts: no classifier permission mode. | Not a catalog class. Never a class value (R-2). | — | Not governed by the autonomy grant, which governs host operations only | **Adopted decision**: DECISION-1 D3. The App never answers A14 affirmatively by rule; a decline or error is allowed only under a named rule with truthful origin (R-2). |
| **P-05** Acceptance-checkpoint override | An operation whose result a declared checkpoint requires A5 on | — (per-run treatment) | propose | No | **DERIVED** from V4-HI-42 and D2b (R-5) |
| **P-06** No-policy-basis treatment | Omitted, unassigned, or pending-OI-021 classes | *no policy basis* | propose available; direct not permitted | No | **INTEGRATION** R-3.5; V4-HI-41 conservative default (F-5) |

### 8.4 Values still open

| Value | Open item | Owner | Point of need |
|---|---|---|---|
| Operation-specific reserved additions and the class of the first connected operation | `UNRESOLVED{OI-021}` | Owner via the outside SWB session and App/shared owner | Before the connected-activity SoW |
| Consequence vocabulary | U-02 | DEL-04-01 with the host policy owner | Before class assignment in DEL-03-01 |
| Defaults for consequential classes other than SWB model change | U-06 | Host policy owner (DEP-001) | Before those classes are cataloged |
| Host capture requirement per act kind; host adoption of P-01…P-06 | U-04 | Host owner (DEP-001) | Before host act-recording integration or any enforcement claim |

---

## 9. Label rules (R-4; S7; S4)

| Word | Allowed use | Not allowed |
|---|---|---|
| **accept / reject / withdraw** | Proposal decisions (A5, A10, A11) | For A7. "Accepting professional reliance" is labeled *rely*. |
| **approve / approval** | Only A6, a separately evidenced engineering approval | On any proposal control, status or record (S7). For harness tool-use prompts, which are **tool permission** (A14). For design-candidate approval, which is a separate later-increment act. |
| **checked / Checked** (unqualified) | Only A4 | For host checks, which say **"host checks passed: ‹named checks›"**, each with its evaluated basis. For agent work, which is **"examination" / "findings"** (A3). DEL-02-01's "agent-checked" becomes "agent-examined (non-mutating)". |
| **later-check route** | Access for later examination or checking | Any implication that an act occurred |
| **certified, sealed, approved, code-compliant** | Only in the accountable professional's own statement (A7 context) | Agent output standing (S4; X-09) |

---

## 10. Value → decision → consumer map

### 10.1 Values carried

| # | Value | Decision basis (standing) | Consumers and use |
|---|---|---|---|
| V-01 | Canonical act names A1–A14, aliases and actor/subject/evidence meanings (§2) | S3, S5, S7, S11; d3; SoW REQ-002; R-1 (settled-by-basis; names INTEGRATION) | **DEL-04-03**: act kind, actor ≠ recorder, recording mode. **DEL-02-01**: checkpoint act from the §4.1 list. **DEL-04-02**, **DEL-05-02**: display. **DEL-01-04**: labels. **DEL-05-01**: act and outcome events, including A10 and A11. |
| V-02 | Class vocabulary with *no policy basis*; OI-002 is not a class value | V4-HI-02; R-2; R-3.5 | **DEL-03-01**: entry element 8. **DEL-03-02**: branch. **DEL-03-03**: carry to the external receiver. |
| V-03 | Resolution order §5.3, resolution point, widening bounds §5.6 | S1, S8–S10, S12; D2; R-3 | **DEL-03-02**: direct branch and *not permitted*. **DEL-05-01**: relay only, checkpoint subject. **DEL-02-03**: hold. **DEL-04-02**: effective vs other states. **DEL-03-03**: relay only. |
| V-04 | Grant by A12 with scope, states and two settings references | V4-AUT-01; V4-HI-40; D2e; R-8 | **DEL-04-02**: states and scope. **DEL-04-03**: settings references and A12 record. **DEL-05-01**: grant in force on dispatch. |
| V-05 | Success ≠ acceptance; outcome map §6 | V4-HI-23, -25; R-3; R-7 | **DEL-03-01** §4.1; **DEL-03-02** P §9; **DEL-05-01**; **DEL-05-02**; **DEL-04-03**; **DEL-01-04** |
| V-06 | Content binding and per-item or per-subject lapse (§2.5) | V4-HI-32; V4-REC-05; R-6 | **DEL-04-03**: L-1 c₁ sources. **DEL-03-01**: subject content identity. **DEL-03-02**: change-item content identity. **DEL-04-02**, **DEL-05-02**: display. |
| V-07 | Label rules §9 | V4-HI-33; R-4 | **DEL-05-02**, **DEL-01-04**, **DEL-04-02**, **DEL-02-01**, **DEL-03-02**, **DEL-04-03** |
| V-08 | No professional standing from agent output | V4-AUT-05 | **DEL-04-02**, **DEL-05-02**, **DEL-01-04**, **DEL-09-09** |
| V-09 | Checkpoint rules §4 | V4-HI-42; V4-WF-05; D2; R-5 | **DEL-02-01**: declaration. **DEL-02-03**: hold machine. **DEL-05-01**: evaluation and resume on capturing-surface evidence. **DEL-05-02**: disposition display. |
| V-10 | External access: same settings and reserved acts; A13 reserved; *channel not enabled* | V4-HI-50…52; D2e | **DEL-03-03**; **DEL-09-09** |
| V-11 | SWB model-change record P-03 | V4-HI-41 (DERIVED class; accepted default) | **DEL-03-01** OP-C4/C5; **DEL-03-02**; **DEL-04-02**; **DEL-04-03**; **DEL-05-01**; **DEL-05-02**; **DEL-09-09** |
| V-12 | A3 is distinct from A4 | d3; V4-EXM-21 | **DEL-05-02**; **DEL-04-02**; **DEL-04-03** |
| V-13 | A9 record shape and the capturing-surface evidence rule | S3; R-5 | **DEL-04-03**, **DEL-05-01**, **DEL-05-02**, **DEL-02-01**, **DEL-09-09** |
| V-14 | Reserved acts P-01, P-01a and act-performing operations P-02 | D2 (adopted); DERIVED | **DEL-03-01** OP-C6; **DEL-05-02** K-4, W-6, PC-23; **DEL-03-02**; **DEL-03-03**; **DEL-04-02**; **DEL-02-01**; **DEL-09-09** |
| V-21 | Routine tool permission P-04 | D3 (adopted) | **DEL-01-01** (H9, R7), **DEL-01-04**, **DEL-01-02**, **DEL-05-01** (hosts: no permission layer), **DEL-05-02**, **DEL-04-02** (not a grant), **DEL-04-03** (not a human act) |

### 10.2 Values held

| # | Value | Standing | Consumers that must hold |
|---|---|---|---|
| V-20 | Operation-specific reserved additions for the first connected operation | `UNRESOLVED{OI-021}` | DEL-03-01, DEL-05-01, DEL-05-02, DEL-09-09 |
| V-22 | First connected operation, its permitted autonomy, environment | `UNRESOLVED{OI-021}` | DEL-03-01, DEL-09-09, DEL-05-01, DEL-05-02 |
| V-23 | Consequence vocabulary; other host defaults | U-02, U-06 | DEL-03-01, DEL-04-02 |
| V-24 | Multi-row A4 purpose after partial lapse | U-03 | DEL-04-03, DEL-04-02 |
| V-25 | Recording location of A14 settlements | U-07 | DEL-04-03, DEL-01-01, DEL-01-02 |

### 10.3 Other declared consumers (not mapped in detail)

These deliverables declare DEL-04-01 upstream in their own registers:

- DEL-01-02 (DEP-01-02-021);
- DEL-02-02 (DEP-02-02-016);
- DEL-03-04 (DEP-03-04-011);
- DEL-06-02 (DEP-06-02-009);
- DEL-09-02 (DEP-09-02-018);
- DEL-09-05 (DEP-09-05-009);
- DEL-09-12 (DEP-09-12-011);
- DEL-10-03 (DEP-10-03-013).

DEL-01-02, DEL-02-02 and DEL-09-02 are outside this undertaking under D1.
DEL-09-11 receives records through DEL-04-03. Register mirrors (V1-A RF-02)
go to C1.

---

## 11. Boundary accounting (REQ-007, VER-008)

| Act or production | Owner | This contract's part |
|---|---|---|
| OI-001, OI-002 rulings | The owner. Done: DECISION-1 D2/D3. | Carry them as records P-01, P-04 |
| OI-021 and operation-specific additions | Owner via the outside SWB session and App/shared owner | Hold (U-01) |
| Performing A4–A7, A10, A12, A13; answering A14 | The person, the accountable professional for A7, or the user's Codex mode for A14 | Meanings and fixtures only |
| Recording as the capturing surface; host act facilities, validation route, receipts, origin and undo, catalog, enforcement of the D2 list | External SWBPIPE owner (CLM-003; DEP-001) | Requirements and receiving cases. No host evidence claimed. |
| Checkpoint declaration / execution and hold machine | DEL-02-01 / DEL-02-03 | Supply §4 |
| Catalog schema, subject content identity, §4.1 outcomes, shared fixture | DEL-03-01 | Supply V-02, V-14, V-11 |
| Proposal lifecycle, change-item content identity, P §9 | DEL-03-02 | Supply V-03, V-05, V-06 |
| External receiving adapter | DEL-03-03 | Supply V-10, relay-only rule |
| Autonomy/standing UI and grant states | DEL-04-02 | Supply V-04, V-08 |
| Record format, lapse comparison, A14 record location | DEL-04-03 (with DEL-01-01 for A14) | Supply V-01, V-06, V-13 |
| Loop and panel receiving | DEL-05-01, DEL-05-02 | Supply V-03, V-05, V-07, V-09 |
| Hosting boundary and tool-permission answers | DEL-01-01 | Supply V-21 |
| Certification, sealing, professional approval, code compliance | Accountable professional (CLM-005) | Prohibit inference (S4) |
| Placement of the policy representation | App/shared owners (OI-013, OI-014) | Representation-neutral |

The existence of this contract claims none of the following:
- host implementation;
- adoption;
- enforcement;
- external evidence;
- performance of any person's act.

---

## 12. Remaining owner and design questions

OI-001 and OI-002 are answered for the first increment by DECISION-1. What
remains:

1. **OI-021** (owner via the outside SWB session). Which concrete SWB operation
   is first? Which operation-specific reserved additions and which autonomy
   beyond the V4-HI-41 default apply to it?
2. **Multi-row A4 after partial lapse** (DEL-04-01 with the owner, U-03). When
   one row of a multi-row checked act lapses, does the act's purpose survive
   for the other rows, or does the whole act lapse for that purpose?
3. **Consequence vocabulary** (DEL-04-01 with the host policy owner, U-02).
   Which dimensions and values define consequence classes, and does the
   App/shared contract or each host name them?
4. **Host capture requirement** (host, DEP-001, U-04). For each reserved act,
   must the host's own facility capture it, or does the host accept App-captured
   evidence for acts on its content?
5. **Workflow registration** (DEL-04-01 with DEL-02-02, later undertaking,
   U-08). Does V4-WF-02 registration get a canonical act name and a place in
   the checkpoint list?
6. **A14 record location** (DEL-04-03 with DEL-01-01, U-07).

---

## 13. Fixture catalogue (OUT-003) — designed, not run

- Subjects are the invented DEL-03-01 §10 fixture **FX-PIPE-01**: run R-100,
  supports S-1…S-4, revisions r12 and r13, entries OP-C1…C6, "Engineer A".
- Divergences from that fixture:
  - **OP-X1** "Renumber nodes" is an invented entry added here. DEL-03-01 §10
    has no entry without a policy basis, and FX-16 needs one.
  - **FX-Professional-P** is added for A7.
  - Checkpoints **CP-1…CP-3** are invented. They are consistent in meaning
    with DEL-02-01 E1 as quoted by V1.
- Expected results are contract expectations. They establish no human act.
  Host-dependent results need DEP-001 evidence.

| ID | Group | Case | Expected result | VER |
|---|---|---|---|---|
| FX-01 | Fabrication | The agent drafts P-1. The run record shows A5 by Engineer A without capturing-surface evidence. | Non-conformant: fabricated attribution | VER-002, -004 |
| FX-02 | Fabrication | An agent OP-C3 finding on S-3 is recorded as A4 by Engineer A | Non-conformant. A3 stays A3. | VER-002 |
| FX-03 | Fabrication | The agent writes A6 "approved" for its own output | Non-conformant (S3, S4, P-01) | VER-002, -003 |
| FX-04 | Success-only | Submitting P-1 returns `success`. The UI or record shows "accepted". | Non-conformant. Must show "queued" (S5). | VER-002 |
| FX-05 | Success-only | The receipt for item 1 is presented as acceptance, checking or approval | Non-conformant. The receipt supports A2 only. | VER-002, -003 |
| FX-06 | Success-only | A5 on item 1; an intervening edit at r13, then application is refused as stale | A5 kept and bound to its change item (not lapsed). A2 *refused* with both bases. No application claimed (R-6, R-7). | VER-002 |
| FX-07 | Independent act | Engineer A edits S-2 directly (no proposal), then performs A4 on S-2 | Conformant A4. The absence of A5 does not invalidate it. | VER-002 |
| FX-08 | Independent act | Item 1 accepted (A5); S-5 later checked by a second person (A4) | Both kept, each with its own actor | VER-002 |
| FX-09 | Faithful recording | Engineer A accepts items in the host. The agent records A5: actor = Engineer A, recorder = agent, mode = faithful recording, citing the host act evidence and item identities. | Conformant record shape. Capture requirement per host (DEP-001). A candidate-bound pass needs actual act evidence (DEP-04-01-021). | VER-002 |
| FX-10 | Faithful recording | As FX-09, but actor = agent, or no evidence reference | Non-conformant | VER-002 |
| FX-11 | Labels | Proposal controls "Accept", "Accept selected items", "Accept all", "Reject" | Conformant | VER-005 |
| FX-12 | Labels | A proposal control or status reads "Approve" or "Approved" | Non-conformant | VER-005 |
| FX-13 | Labels | A separately evidenced A6 labeled "approve"; A7 labeled "rely", not "accept reliance" | Conformant | VER-005 |
| FX-14 | Standing | Agent result displayed "code-compliant" or "certified" | Non-conformant (S4) | VER-003 |
| FX-15 | Standing | A7 statement by FX-Professional-P on OP-C2 results | Conformant. Not inferred from A2–A6. | VER-003 |
| FX-16 | No policy basis | OP-X1 has no class. The person performs A12 granting direct for it. The agent requests direct. | *not permitted* (§6 row 6). The agent may propose. The result is reported under INTEGRATION rule P-06 and is not counted as an adopted-class pass. | VER-004, -007, -009 |
| FX-17 | No policy basis | An entry omits the class element | As FX-16. Omission is never permission. | VER-004, -007 |
| FX-18 | Classifier | (a) Host: a classifier mode auto-permits OP-C4. (b) App: the user's Codex mode auto-permits a tool call. | (a) Non-conformant: hosts have no classifier mode (D3). (b) Conformant as A14 only; never recorded as A4–A7, A12 or A13. | VER-004 |
| FX-19 | Default | OP-C4 on FX-PIPE-01 with no grant set | *propose*. Item, multi-row and batch acceptance offered (P-03). Host conformance needs DEP-001. | VER-006 |
| FX-20 | Widened | Engineer A performs A12: OP-C4 class direct, scope FX-PIPE-01. The control confirms it (effective). | The agent applies with origin, basis, undo route and later-check route. Settings references at validation and application are recorded. | VER-001, -006 |
| FX-21 | Checkpoint | Grant effective direct. CP-1 requires A4 on the rows applied by OP-C4 and is reached. | Run waits. The agent may only request (A8). | VER-001, -006 |
| FX-22 | Reserved | Widest grant. The agent invokes a reliance operation on OP-C2 results. | *not permitted* plus A8. No attribution. | VER-004, -006 |
| FX-23 | Grant change | The agent requests widening, and then attempts to set it | Request shown as *requested by agent (A8)*. The set attempt is *not permitted* (D2e, P-01). | VER-001, -004 |
| FX-24 | External | External access off (A13 not performed) | *channel not enabled*, not *unavailable* | VER-004 |
| FX-25 | External | A13 performed. The external agent submits P-1. Engineer A accepts in the host. | Same lifecycle and settings as embedded. A5 attributed to Engineer A. | VER-004 |
| FX-26 | Examination | The agent runs OP-C3 on the engineer's edits | Findings by reference. No table change. No A4. | VER-002 |
| FX-27 | Lapse | A4 on S-2 at r12. S-2 stiffness changes at r13. S-3 is edited as a control. | S-2's act is lapsed and keeps its r12 identity. It is not lapsed by the S-3 edit (subject content identity). | VER-002 |
| FX-28 | Boundary | The contract asserts host enforcement without DEP-001 evidence | Non-conformant (REQ-007) | VER-008 |
| FX-29 | Acceptance checkpoint | CP-2 requires A5 on OP-C5's result. The grant is effective direct for OP-C5. The agent requests direct. | Treatment forced to *propose* (§4.4). The direct request is *not permitted*. | VER-001, -006 |
| FX-30 | Negative A5 | At CP-2 Engineer A rejects the item (A10) | Disposition *resolved negatively*. The declared on-negative path governs. Never *performed*. | VER-002 |
| FX-31 | Decline | CP-1 requires A4. Engineer A declines. | Decline event recorded. It is not A4. The checkpoint is not satisfied, and the on-negative path governs. | VER-002 |
| FX-32 | Item binding | Batch A5 over items 1 and 2. Item 1 is applied. Item 2 is re-drafted as a new proposal P-2. | The A5 on item 1 is not lapsed by its application. The A5 on item 2 does not carry to P-2. | VER-002, -006 |
| FX-33 | A14 origin | An App rule answers a tool permission affirmatively; separately, an App rule declines one with a named rule | Affirmative: non-conformant. Decline under a named rule with truthful origin: conformant. | VER-004 |
| FX-34 | "checked" label | A host result shows "Checked" for its equilibrium check; an agent result shows "agent-checked" | Both non-conformant. The host result must read "host checks passed: equilibrium check"; the agent result must read "agent-examined (non-mutating)". | VER-005 |
| FX-35 | Offering reserved | OP-C6 is offered to an agent and invoked; separately, OP-C6 is withheld | Invoked: *not permitted* plus A8. Withheld: *not exposed on this surface*. *unavailable*: non-conformant. | VER-004 |
| FX-36 | Checkpoint evidence | The agent writes an A4 record for CP-1 without citing host act-facility evidence | Not a satisfaction. The loop does not resume. | VER-002, -004 |
| FX-37 | Narrowing | A queued P-1 exists and a direct OP-C4 application is in validation. Engineer A narrows the grant to propose (A12). | P-1 is unaffected. The direct operation is re-resolved at application: *not permitted*, not converted. | VER-001, -006 |
| FX-38 | Widening | A queued P-1 exists. Engineer A widens to direct. | P-1 stays a proposal (R-3.7). | VER-006 |

---

## 14. Findings (reported, scope unchanged)

- **F-1 Register asymmetry (unchanged).** DEL-04-01's `Dependencies.csv` names
  five downstream consumers. Eighteen deliverables have ACTIVE upstream rows
  targeting DEL-04-01 (V1-A RF-02). This goes to C1.
- **F-2 Approval overload.** This is now handled by §9 and R-4.
  Design-candidate approval (V4-CON-05 / V4-HI-65) has no canonical name. It
  will need one when the Domains increment is defined.
- **F-3 Reject and withdraw.** These are not in the SoW taxonomy and not in the
  D2 list. They are named by R-1, and A10 is reserved by derivation. The
  derivation is agreed.
- **F-4 Consequence vocabulary.** It still has no owner decision (U-02), even
  though the SoW requires policy "by operation and consequence".
- **F-5 R-3.5 tension with SoW REQ-004.** R-3.5 lets an agent *propose* for a
  *no policy basis* class. It is applied. REQ-004 says a concrete unruled
  operation "shall await the applicable … decision before dependent
  operation-policy production", and "omission … shall not be treated as
  permission".
  - Proposing grants no application.
  - A5 remains reserved.
  - Dependent production is still held by REQ-004.

  The runtime proposal path is therefore a candidate behavior, not a
  conformance pass. IR1 or the owner may wish to confirm this reading.
- **F-6 D2(b) wording.** D2(b) reserves A5 "wherever the active autonomy
  requires a proposal". It does not speak to voluntary proposals under a
  direct grant. S3 already makes every A5 a person's act (§2.2). A host list
  that transcribes D2(b) literally should be read with S3.
- **F-7 Record operation vs faithful recording.** P-02 reserves catalog
  operations that *record* a person's act, while A9 lets agents faithfully
  record. The two coexist only because agent faithful records live in App/run
  records (DEL-04-03) that cite capturing-surface evidence, not in a host
  catalog operation. DEL-03-01 and DEL-04-03 should keep that separation
  explicit.
- **F-8 OI rows not yet rewritten.** PRD OQ-02 corresponds to OI-001 and
  OI-002, both now ruled for the first increment by DECISION-1. The
  `Open_Issues.csv` rows are not rewritten (C1). Consumers citing OQ-02,
  OI-001 or OI-002 should cite DECISION-1 through P-01 and P-04.
- **F-9 A12/A13 binding.** The basis defines no lapse for A12 or A13. The
  supersession rule in §2.5 is PROPOSED.

---

## UNRESOLVED

| Item | Owner | Point of need | Effect on this definition |
|---|---|---|---|
| U-01 `UNRESOLVED{OI-021}` first connected operation, operation-specific reserved additions and its autonomy | Owner via the outside SWB session and App/shared owner | Before the connected-activity SoW and execution | P-03 and P-01 carry no operation-specific additions. A concrete first operation's class is *no policy basis* until then. V-20 and V-22 are held. |
| U-02 Consequence vocabulary | DEL-04-01 with the host policy owner | Before class assignment in DEL-03-01 | Consequence is text in d3 dimensions only |
| U-03 Multi-row A4 purpose after partial lapse | DEL-04-01 with the owner | Before DEL-04-03 lapse display criteria are fixed | Per-subject lapse is defined. Survival of the act's purpose is not. |
| U-04 Host capture requirements per act kind; host adoption and enforcement of P-01…P-06; host-reported settings at application | Host owner (DEP-001) | Before host act-recording integration or any enforcement claim | Host rows are receiving requirements. Host-dependent fixtures have no result. |
| U-05 Recorded person grant; actual performed-act evidence | The person (DEP-04-01-020, -021) | VER-001 and the VER-002 positive cases | The candidate-bound FX-09/FX-20 passes cannot run |
| U-06 Conservative defaults for consequential classes other than SWB model change | Host policy owner (V4-HI-41; DEP-001) | Before those classes are cataloged | §5.3 rule 7 falls back to rule 5 (P-06) |
| U-07 Where A14 settlements are recorded | DEL-04-03 with DEL-01-01 | DEL-04-03 record v0.2 | A14 is never a human-act or grant record. Its location is open. |
| U-08 Workflow registration (V4-WF-02) as a canonical act | DEL-04-01 with DEL-02-02 (later undertaking, D1) | Before the DEL-02-02 definition | Not in R-1's table and not checkpoint-requirable |
| U-09 Mixed item-level decisions into one A5 checkpoint disposition | DEL-02-01 with DEL-02-03 and DEL-03-02 | Before the DEL-02-03 hold design (W7) | §4.3 supplies per-item facts only |
| U-10 Re-hold after a lapse that follows resume | DEL-02-03 (W7) | Before the hold machine | Lapse is recorded at any time. Re-hold is not asserted. |
| U-11 Offer vs withhold of reserved-class entries | DEL-05-01 with DEL-03-01 | DEL-05-01 v0.2 | Both are conformant per §6 row 8 |
| U-12 Placement of the policy representation | App/shared owners (OI-013, OI-014) | Before production allocation | Representation-neutral |

Closed since v0.1:
- v0.1 U-01/U-02 (OI-001/OI-002): closed by DECISION-1.
- v0.1 U-08 (scope): closed by R-8.
- v0.1 U-09 (in-flight): closed by R-3.6, with host enforcement moved to U-04.
- v0.1 U-10 (batch act unit): closed by R-6.

## Verification cases

These are designed and not run. Each binds to this file's revision when
executed.

| Case | Serves | Procedure | Expected result |
|---|---|---|---|
| VC-001 | VER-001 / AC-001 | Compare §4, §5 and §8 with V4-AUT-01, V4-HI-22/40/42 and D2. Run FX-20, -21, -23, -29, -37 and -38 against a recorded person grant (U-05). Trace origin, undo and later-check obligations to DEL-03-02, DEL-04-02 and the host. | Every direct treatment traces to an effective A12 grant within scope. Checkpoints override the grant, and an A5 checkpoint forces *propose*. Narrowing and widening behave per §5.5. A missing grant is recorded as missing. |
| VC-002 | VER-002 / AC-002 | Exercise FX-01…10, -26, -27, -30, -31, -32 and -36. Inspect actor, subject and evidence per canonical act kind. | Negatives are non-conformant. FX-07 and FX-08 are conformant without A5. FX-09 keeps actor ≠ recorder and cites capturing-surface evidence. Declines are events, not acts. Item binding is per R-6. The candidate-bound FX-09 pass waits for U-05. |
| VC-003 | VER-003 / AC-003 | Exercise FX-03, -05, -14, -15 and -22 against V4-AUT-05 | No certification, sealing, approval or code-compliance claim is made for agent output. A7 is attributed only to its professional. |
| VC-004 | VER-004 / AC-004 | For each record in P-01, P-01a and P-02, compare with DECISION-1 and inspect host enforcement evidence. Exercise FX-16…18, -22…25, -33, -35 and -36. For OI-021 cases, check the owner and point of need. | Adopted reserved acts cannot be performed or attributed by any agent. The outcomes follow §6. Host enforcement is not asserted without DEP-001. OI-021 cases are reported as held, not passed. |
| VC-005 | VER-005 / AC-005 | Inventory proposal-decision, approval and "checked" wording in this file, §7 and FX-11…13 and FX-34 | "accept" for proposals only. "approve" for A6 only. Unqualified "checked" for A4 only. Tool prompts are "tool permission". |
| VC-006 | VER-006 / AC-006 | Exercise FX-19…22, -29, -32, -37 and -38. Compare with V4-HI-41/42/51 and D2. | Default *propose*. Item, multi-row and batch acceptance. Widening bounded by W-a…j. Local contract evidence and host evidence are labeled separately. |
| VC-007 | VER-007 / AC-007 | Trace V-01…V-14 and V-21 to their bases, and P-01…P-06 to DECISION-1, derivations or R-3.5. Trace V-20…V-25 to open items and owners. | Every carried value has a basis and a standing label. No value comes from a historical list, a pending recommendation or a fixture. The INTEGRATION record P-06 is labeled as such. |
| VC-008 | VER-008 / AC-008 | Compare §11 with SoW CLM-002…005 and REQ-007. Run FX-28. | Each excluded act is assigned to its owner. No host, adoption or act claim is made. |
| VC-009 | VER-009 / AC-009 | Reconcile FX-01…38 with REQ-002…006 and the matrix. When a candidate exists, run the applicable fixtures and keep fixture IDs, candidate identity, results and limits. | Coverage is complete. OI-021 holds, INTEGRATION-rule results and missing host evidence are reported separately from passes. No results exist at v0.2. |
