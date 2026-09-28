# Operation-Policy and Human-Act Contract
- Contribution: DEL-04-01/ACT-POLICY-v0.3. It supersedes ACT-POLICY-v0.2 (sha256 e50f1fe2f5bb2e3280bc62175e5aeeaa4508eed713424d82c54536a9fb5993a9, committed at `28bd00499`), which superseded v0.1 (sha256 e6457535…3763).
- Status: DRAFT DEFINITION — proposed, unsupplied, not implemented, not accepted
- Serves: OUT-001, OUT-002, OUT-003; REQ-001…REQ-007; VER-001…VER-009 (AC-001…AC-009)
- Basis:
  - Repo 6e18505e3; ScopeOfWork.md sha256 fc1a0503abad4196e869402b664bd76280773d197b5c77994c34e858a406f5e6.
  - `P/docs/PRD.md` §4.1 (V4-WF-02, -05), §4.3 (V4-EXE-01, -02), §4.5 (V4-AUT-01…05), §4.7 (V4-REC-05), §9 (OQ-02, OQ-11), §10.
  - `P/docs/HOST_INTEGRATION.md` §2 (V4-HI-02, -04), §3 (V4-HI-11, -12), §4 (V4-HI-20…25), §5 (V4-HI-30…33), §6 (V4-HI-40…42), §7 (V4-HI-50…52), §9 (V4-HI-70/71).
  - `P/docs/EXAMINATION.md` V4-EXM-20, -21, -22, -25, -31.
  - `P/execution/_Coordination/Acceptances/APP-V4-BASIS-20260926/DECISION_BRIEF.html#d3` (sha256 02d38cb18041c52989d8a2a0b969e6502ce4b25eec85fb0931bbbc100c4420e8).
  - `P/conceptual/DECISIONS.md` OD-05, D-04; `P/conceptual/EXEMPLARS_AND_LESSONS.md` X-09, X-19, X-20.
  - `P/execution/_Decomposition/Open_Issues.csv` OI-001, OI-002, OI-013, OI-014, OI-021; `External_Dependencies.csv` DEP-001.
- Consumed inputs. All of the following were read from commit `28bd00499`; the working-tree copies were not used for siblings. Paths under `AgentRuns/APP-V4-FIRST-INCREMENT-20260928/`:
  - Owner decision `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` (D2 = OI-001, D3 = OI-002): `OWNER_DECISIONS.md` (sha256 f3f8e5f31ec87006fc9ab459c6ae57d08638439c234fa959ba2605914cf81f2e).
  - `R1_RESOLUTIONS.md` (sha256 2f9c7e72aa8362624ad830377a70077b27a27bf03871f8e87811a28e6e177ec4).
  - `R2_RESOLUTIONS.md` (sha256 77cfb845ec305365f12218f83f332069155de5f362139b7a6fe2bf12cdebd088). This file owns R2-1…R2-11 and the DEL-04-01 parts of R2-15…R2-21.
  - `reviews/IR1-A.md` (sha256 31b3c7f8493f05ee5fed6a11208f6811d2449d8a4fe72aae6300c2850b648284), all items addressed to DEL-04-01.
  - `reviews/IR1-B.md` §2.6 (B-M1, B-M9) and `reviews/IR1-C.md` IR1C-06, -07, -10, -22 and X-10, for items naming DEL-04-01.
  - V1-A/B/C, as in v0.2.
  - Sibling v0.2 text:
    - DEL-03-01/C-v0.2 `CATALOG_AND_READ_BASIS.md` (sha256 358182b18b1fe13f9af6e6f5a61c9ed57f91b6ab29ea0c9adab06fe0081d6d82), §2, §3.1, §4.1, §10 (shared fixture FX-PIPE-01, T1–T17, OP-C1…C9);
    - DEL-02-01/WD-v0.2 `WORKFLOW_DECLARATION.md` (sha256 c25bccc5f3ac02c84522148eeaa8a6ef0f5eb4a380686773cff45f57a448a55c), §4.3 and FB-03/FB-04.
  - Fixture IDs OP-C10 and OP-C11 are fixed by R2-21 and are not yet in C-v0.2.
- Receivers:
  - From `Dependencies.csv` DEP-04-01-012…016: DEL-02-01, DEL-02-03, DEL-03-01, DEL-04-02, DEL-04-03.
  - Declared upstream in the receivers' own registers:
    - DEL-03-02 (DEP-03-02-017);
    - DEL-03-03 (DEP-03-03-008);
    - DEL-05-01 (DEP-05-01-018);
    - DEL-05-02 (DEP-05-02-008/-014/-015);
    - DEL-01-04 (DEP-01-04-011);
    - DEL-09-09 (DEP-09-09-010).
  - DEL-01-01 receives the D3 value.
  - Further declared consumers are in §10.3.
  - DEL-04-01 is not a SCC-CASE-002 member.

`P` = `projects/chirality-app-v4`. Every element name in this document is a
**semantic name, not a wire name**. Examples: *act kind*, *decision actor*,
*recorder*, *recording mode*, *change-item content identity*, *treatment*,
*grant value*.

This definition selects none of the following:
- field names or types;
- transport;
- hash or canonicalization algorithm;
- persistence;
- process or shared-component placement (OI-013, OI-014).

Anything still open appears only as `UNRESOLVED{…}` or as a named relay
question. It is never a permission, a default or a pass.

---

## Changes from v0.2

| R2 / IR1 item | How addressed in v0.3 |
|---|---|
| R2-1; IR1A-01; IR1-B B-M1; IR1C-10 | The fifth class value is **no policy basis**, with a *reason* ∈ {omitted, unassigned, pending OI-021}. It is labeled INTEGRATION (R-3.5). The four V4-HI-02 values are labeled SETTLED (§5.1, §8.1). |
| R2-2; IR1A-08; X-1 | Reserved-operation rule restated as **perform**, not "perform or record", and A10 added (§5.3 rule 3, P-02). The conditions on a host-offered faithful-record operation are stated, and that question is routed to DEP-001. F-7 is closed. |
| R2-3; IR1A-16 | Disabling external access is also A13. It is labeled INTEGRATION, and only *enabling* is credited to D2e (§2.1, P-01). |
| R2-4; IR1A-02, -10, -21 | Reserved entries are always offered. An invocation returns *not permitted* and **offers** an A8 request; nothing is recorded automatically. *Not exposed on this surface* comes only from the host's exposure element. The loop reports its own *not offered*. §6 row 8 and FX-35 rewritten; U-11 closed. |
| R2-5; IR1A-03; IR1C-06; X-2 | **Act-declined event** for A4/A6/A7/A12, with elements and capture evidence. Its disposition is *resolved negatively*. Stopping work is a separate **run-ended event**, and the checkpoint stays *waiting* (§2.3, §4.3; FX-31, FX-40). |
| R2-6; IR1A-05; X-4 | New grant state **effective (policy default)**, which needs no A12. *not set* = no setting and no default. §5.3 rule 7 and FX-19 fixed. |
| R2-7; IR1A-04, -13; X-13 | A12 binds to the **setting content**. The established version, or a refusal by the control, is a relation on the act. A later A12 **supersedes** an earlier one and does not lapse it. A checkpoint that the superseded act performed stays *performed*. *superseded* added to the lapse-state vocabulary. A refused A12 at a checkpoint is held for DEL-02-03 (U-13). F-9 is closed into §2.5. |
| R2-8; X-3; IR1A-21 | A14 settlements are recorded only in run record R13. They never appear in R6, as a human-act record or as a grant. U-07 is closed; V-25 moves to the carried values. |
| R2-9; X-15 | Wording of rule 5 / P-06: proposing confers no permission; direct application is *not permitted*; an A12 that widens such a class is refused; the REQ-004 hold stands. Fixtures report these cases as **held**. F-5 is closed as confirmed. |
| R2-10; IR1C-22 | §4.1: a recognized act kind outside the list is **invalid** (WD FB-03). An unrecognized name is **not established** (WD FB-04). |
| R2-11; IR1A-16 | Attribution hygiene. P-04 credits D3 only with what D3 says; the App-rule restriction is labeled INTEGRATION (R-2). A13 disable is labeled INTEGRATION. The derived rules keep their DERIVED labels. |
| R2-12; IR1C-03 | §4.4: the **governing checkpoint constraint** travels with the change request. A direct request made under the constraint is *not permitted* and names it; it is never "drafted as a proposal". Relay question routed to DEP-001. Affected fixtures are **AWAITING INPUT** (FX-29). |
| R2-14 | §4.2: "objects changed by a named outcome" binds to the per-item resulting object identities that the applied outcome reports. |
| R2-15; IR1A-06 | §2.5: undo (a receipt that *reverses ⟨receipt⟩*) lapses acts bound to content it changes in the normal way. It does not lapse A5/A10 on the reversed item. OP-C10 Undo is used in FX-39. |
| R2-16 | FX-06 display: "accepted by ‹person› — not applied: refused — stale (both bases)". The A5 is not lapsed. |
| R2-17; IR1C-05; X-10 | §4.2: the subject class is independent of the reached-when kind. Referents now include **targets of the held call** and the **grant setting**. An A5 checkpoint uses kind (c) *proposal queued*. |
| R2-18 | §4.3: mixed item decisions cite WD §4.3.7 (PROPOSED). "Partial" is a per-item annotation. U-09 narrowed to DEL-02-03 confirmation. |
| R2-19; IR1A-09; IR1C-07 | §4.3: one lapse sequence. An **act-lapsed event** is recorded and the disposition returns to *waiting* ("waiting — lapsed at ‹t›"). After resume, re-hold belongs to DEL-02-03. *lapsed* as a standing disposition is used only when the run has ended. |
| R2-20 | §4.5: the capture-evidence reference is a relay question. Without it, no host-content checkpoint can be *performed*. The App-side equivalent is WD U-25. |
| R2-21; IR1A-07; IR1-B B-M9 | §7 and §13 re-pointed to C-v0.2 §10: FX-PIPE-01, T1–T17, PR-1/PR-2, RC-1…RC-3, OP-C1…C9, plus OP-C10/OP-C11. The v0.1/v0.2 meaning of OP-C5 is dropped (it is now "Set support stiffness"). OP-X1 is removed. Local cases are named `L-ACT-n` with reasons. |
| IR1A-12 | A9 recorder list no longer includes "the person"; self-recording is *direct capture* by the capturing surface. §2.4 adds A13 to the non-conformance list. Human-act record kinds exclude A9, which is carried as a recording mode, and A14. |
| IR1A-14 | The grant's direct/propose value is called the **grant value**. *Treatment* is kept for the §5.2 outcomes. |
| IR1A-17 | FX-16: the person's A12 widening of a no-policy-basis class is **refused (reason: no policy basis)**. |
| IR1A-18 | Run ended while waiting: covered in §4.3 and FX-40. |
| IR1A-20 | Finding F-10: SoW TBD-001/002, AC-004 and VER-004 wording predates DECISION-1 (routed to C1). |
| R3-1 (in place, no version bump) | §4.2 adds the subject class **objects a named output concerns**, bound through the subject content identities as read. This lets a review-only workflow require A4 on the rows it examined. INTEGRATION. |
| R3-2 (in place) | §4.2: *targets of the held call* is valid only with reached-when kind (a) *before dispatch*. Any other kind makes the checkpoint invalid. INTEGRATION. |
| R3-4 (in place) | §5.3 and P-03: an undo (OP-C10) is governed by the policy record and grant state of the operation whose receipt it reverses. It has no class of its own. The §8.3 fixture note for OP-C10 is updated to match. INTEGRATION. |

The "Changes from v0.1" table at the end of this file is kept as history.
Where it conflicts with this table, this table governs.

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

| Label | Meaning here |
|---|---|
| **SETTLED** | Stated in the accepted composite (B-ACCEPT) and cited |
| **ADOPTED** | Owner ruling `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` (D2/D3), credited only with what it says (R2-11) |
| **DERIVED** | A direct consequence of settled or adopted clauses, with the derivation shown |
| **INTEGRATION** | An R1/R2 integrator choice. Reviewable, and open to owner revision. |
| **PROPOSED** | A design choice of this contribution or a sibling, open to review |
| **UNRESOLVED{…}** / relay question | An open item with owner and point of need |

---

## 2. Acts — canonical names, actor, subject, evidence

**Rule.**
- Evidence of one act kind never establishes another.
- The absence of one act kind does not, by itself, invalidate an independently
  evidenced act of another kind (REQ-002; AX-002).
- Acts are never promoted automatically into other acts, and there is no
  universal acceptance prerequisite.

### 2.1 Canonical names and alias map (R-1)

Every consumer uses the canonical name. An alias in the basis maps to its
canonical name.

| ID | Canonical name | Aliases in the basis | Decision actor | Subject | Supporting evidence | Does **not** establish | Policy standing | Basis |
|---|---|---|---|---|---|---|---|---|
| A1 | **propose** | draft/submit a proposal | Agent (embedded or external) or the person | One proposal of one or more change items against a cited read basis | Host proposal record with origin and relied-on basis; lifecycle state | Acceptance, application, checking, approval, reliance | Agent-available | V4-HI-21, -23, -24, -25; d3 |
| A2 | **apply** | execute an operation; direct application | The person; an agent under an effective direct treatment; the host route after acceptance | The operation invocation and its effect on identified objects | Host receipt, origin mark and observed outcome per DEL-03-02 P §9 (R-7), including the resulting object identities (R2-14) | That anyone accepted, checked, approved or relied | Governed by treatment (§5) | V4-HI-20, -22, -23, -25, -71 |
| A3 | **examine** | agent check, examination, findings | Agent | Identified rows, results or models, by read basis | Findings attached by reference; no table change | A4, A5, A6, A7 | Agent-available | d3; V4-EXM-21 |
| A4 | **mark checked** | marking work checked | The person | Identified host rows/objects or App file content, with scope and purpose | Capture evidence from the capturing surface (§4.5), bound to subject content identity | A5, A6, A7 | **Reserved** — ADOPTED D2a | V4-AUT-03; V4-HI-30, -32; V4-REC-05; X-20 |
| A5 | **accept** | accept an edit; accept a proposed edit | The person | One or more identified **change items** (§2.5) | Capture evidence listing the items; labeled "accept" | A6, A4, A2 | **Reserved** wherever the active autonomy requires a proposal — ADOPTED D2b | V4-HI-23, -25, -33, -41; d3 |
| A6 | **approve** | engineering approval (V4-HI-30/33) | The accountable person | Identified engineering content or design | A separate attributable approval record | A7 or any certification | **Reserved** — ADOPTED D2c | V4-HI-30, -33 |
| A7 | **rely** | professional reliance; "accepting professional reliance" (d3; V4-CON-05) | The accountable professional only | A result relied on for a stated professional purpose | The professional's own attributable statement | Anything about agent output | **Reserved** — ADOPTED D2d; SETTLED V4-AUT-05, V4-HI-30 | V4-AUT-05; X-09 |
| A8 | **request** | prepare or request a person's act | Agent | A request naming the exact act kind, subject and purpose | The request, with the requester identified | Anything. A request is never the act. | Agent-available. An A8 exists only when the agent actually issues it (R2-4). | V4-AUT-03; V4-HI-31; V4-PM-04 |
| A9 | **record** | faithful recording; direct capture | *Recorder*: the capturing surface (direct capture), or another identified party such as the host facility, the App or an agent (faithful recording). A person recording their own act is direct capture by the capturing surface. | An actually performed act of kind A4–A7, A10–A13, or an act-declined event | Reference to the act's evidence, recorder identity, and *recording mode* ∈ {direct capture, faithful recording} | The act itself. **A9 is a recording act, not a decision act**, and it never satisfies a checkpoint on its own. | Faithful recording by any identified recorder distinct from the decision actor is a conformant shape (SETTLED S3). Capture requirement: DEP-001. | SoW REQ-002; d3; V4-HI-31; R-1; R-5 |
| A10 | **reject** | reject a proposal or item; a person removing another party's proposal | The person | One or more identified change items | Host lifecycle record `rejected`, with actor | Anything beyond non-acceptance of those items | **Reserved** wherever A5 is — DERIVED (decision pair of A5; R-1) | V4-HI-23; V4-EXM-20 |
| A11 | **withdraw** | withdraw one's own proposal | The proposer only | Its own proposal | Host lifecycle record `withdrawn` | A decision on the proposal's merit | Proposer's act. It is a human-act record only when the person is the proposer. | V4-HI-23; R-1 |
| A12 | **set grant** | set or change the autonomy grant | The person | **Setting content**: operation classes, grant values and scope (§2.5, §5.4) | Capture evidence from the control surface. The version the control establishes, or the control's refusal, is a relation on the act. | That an agent's A8 established anything | **Reserved** — ADOPTED D2e | V4-AUT-01; V4-HI-40, -41 |
| A13 | **enable external access** (includes disabling) | enable or disable external-agent access | The person | The host's external interface on this machine (enablement setting) | Recorded enablement or disablement | Any grant for an operation class | Enabling: **reserved**, ADOPTED D2e. Disabling: **reserved**, INTEGRATION (R2-3). An agent may request either (A8). Off by default and local: SETTLED. | V4-HI-52 |
| A14 | **answer tool permission** | harness "approval" of tool use; routine tool permission | The person, or the user's own Codex permission mode inside the supplier | One tool-execution request | Request settlement: answered, or explicitly declined, or errored; never by silence or timeout. Recorded only in run record R13 (R2-8). | Any of A4–A7, A10, A12, A13, or a host-operation grant | ADOPTED D3: App modes are the user's Codex setting; hosts have no classifier mode. INTEGRATION (R-2): the App never answers affirmatively by rule; a decline or error is allowed only under a named rule with truthful origin. | V4-AUT-04; V4-EXE-02; D3 |

Alias exclusions (R-1):
- Design-candidate approval (V4-CON-05; V4-HI-65) is a separate act in a later
  increment. It is **not** A6.
- The word *accept* belongs to A5 alone.

Other human acts keep the attribution invariants but have no canonical name
here:
- workflow registration (V4-WF-02; U-08);
- stopping work (V4-EXE-01), which produces a run-ended event (§4.3);
- reserved coordination decisions (V4-PM-04).

### 2.2 Direct application is never acceptance

When an effective direct treatment lets an agent apply a change, the act is
A2. It is never recorded as A5. SETTLED S3 means an agent is never the
decision actor of A4–A7. D2(b) reserves A5 wherever the autonomy requires a
proposal. Wherever A5 is performed at all, only the person performs it
(finding F-6).

### 2.3 Decision pairs, act-declined events and run-ended events (R2-5)

| Required act | Positive | Negative | Standing of the negative |
|---|---|---|---|
| A5 | accept | A10 reject | An act, recorded per item |
| A4, A6, A7, A12 | the act | **act-declined event** | A recorded event. It is **not** an act of that kind and never satisfies anything that requires the act. |

- **Act-declined event** elements:
  - actor (the person);
  - declined act kind;
  - bound subject;
  - time;
  - capture evidence from the capturing surface. Faithful recording is a
    permitted record shape (§4.5).

  The event never records the declined act as performed. The name keeps it
  distinct from an A14 settlement `declined` (HOSTING §6), and from A10,
  which is recorded as "rejected the item", not "declined".
- **Run-ended event.** Stopping work (V4-EXE-01) is a separate action by the
  person. It is not a decline. A checkpoint that is waiting when the run ends
  stays **waiting**, with a run-ended event. A person who wants both
  declines, then stops, and both events are recorded.
- An act performed after its run has ended is recorded. It does not change
  the ended run's checkpoint disposition unless DEL-02-03 defines resumption
  (R2-5).

### 2.4 Recorded-act element meaning

This is the meaning DEL-04-03 receives. DEL-04-03 owns the format.

| Element | Meaning | Presence |
|---|---|---|
| *act kind* | One of A4, A5, A6, A7, A10, A12, A13, or A11 when the person is the proposer; or the act-declined event with its declined kind. A9 is carried as *recording mode*. A14 is never a human-act record (R2-8). | Always |
| *decision actor* | The person who actually performed the act | Always |
| *recorder* and *recording mode* | Who wrote the record; direct capture or faithful recording | Always |
| *subject content identity*, *scope*, *purpose* | What the act concerned (§2.5) | Always |
| *evidence reference* | Capture evidence from the capturing surface, linked and not copied (V4-HI-71) | Always. Without it, the record is non-conformant. |
| *lapse state* | Relative to current content (V4-HI-32). *superseded* for A12/A13. | When applicable |
| *governing policy reference* | The policy-class record and policy revision identity (§8.1) | Optional. Present when a catalog operation governed the act. |

A record is non-conformant if it names the recorder as the decision actor of
an A4–A7, A10, A12 or A13 act, or if its person-attributed act has no evidence
reference.

### 2.5 Content binding, lapse and supersession (S6; R-6; R2-7; R2-15)

| Act | Bound content (c₀ source) | Change rule |
|---|---|---|
| A5, A10 | **Change-item content identity** (DEL-03-02): operation identity and version, bound targets, old/new values, relied-on basis | See the notes on A5 and A10 below. |
| A4, A6, A7 on host content | **Subject content identity** (DEL-03-01 §5.3), per object or row, host-supplied | Per subject. A change to a bound row lapses the act for that row; an unrelated edit does not. An **undo** that changes a bound row lapses the act in the normal way (R2-15; V4-HI-32). |
| A4, A6, A7 on App files | File content identity (DEL-04-03) | Per file or scope |
| A12 | **Setting content**: classes, grant values, scope | PROPOSED (R2-7). Not lapse-evaluated. A later A12 on overlapping classes and scope **supersedes** it, and the record shows *superseded by ⟨act⟩*. A checkpoint the earlier A12 performed stays *performed*, with the supersession shown. Operations are governed by the grant state in force at route decision and at application. |
| A13 | Enablement setting content | PROPOSED. A later A13 supersedes it; no lapse. |

Notes:
- A5 and A10 are evaluated per item.
  - Applying the accepted item does not lapse the acceptance.
  - A basis failure between acceptance and application falls under the stale
    rule (DEL-03-02 U-P3). It is not a lapse. The display is "accepted by
    ‹person› — not applied: refused — stale (both bases)" (R2-16).
  - Undoing the applied item (a receipt that *reverses ⟨receipt⟩*) does not
    lapse A5 or A10 on that item (R2-15).
  - A re-draft is a new proposal. The earlier acceptance does not carry over.
- Acceptance granularity:
  - Batch or multi-row acceptance is one A5 act listing several items, each
    bound to its own item and lapsing on its own.
  - Row-by-row acceptance is one A5 per item.
- What purpose a multi-row A4 keeps after partial lapse is an owner question
  (U-03).
- Every content identity carries its identity-method designation. The
  algorithm is unselected.
- The lapse-state vocabulary is DEL-04-03's. This contract adds
  **superseded** for A12/A13 (IR1A-13).

---

## 3. Settled distinctions S1–S12 and adopted rulings

Each was checked against the cited bytes at repo 6e18505e3.

| ID | Settled distinction | Citation | Consequence |
|---|---|---|---|
| S1 | Graduated autonomy per kind of operation. The agent proposes or applies directly within a scope the person sets, with origin, undo and later checking. | V4-AUT-01; V4-HI-22, -40; D-04 | §5; direct application carries origin, undo route and later-check route |
| S2 | Every result's standing is visible. | V4-AUT-02; V4-HI-12; X-19 | No presentation stronger than the evidence |
| S3 | Agents may prepare checking, acceptance and reliance decisions. They must not represent an act as performed when it was not. Faithful recording of a performed act is allowed, with actor ≠ recorder. | V4-AUT-03; V4-HI-31; d3; SoW REQ-002 | A1/A8 permitted; fabrication prohibited; A9 is a record shape |
| S4 | No agent output is presented as certified, sealed, approved or code-compliant. | V4-AUT-05; X-09 | A7 is never inferred |
| S5 | `success` means the operation ran. It never means acceptance; a proposal stays queued until acceptance and application are recorded. | V4-HI-23, -25 | A2 ≠ A5 |
| S6 | A human act binds to its content, scope and purpose, and lapses visibly when that content changes. | V4-HI-32; V4-REC-05; X-20 | §2.5 |
| S7 | Proposals say "accept", never "approve". | V4-HI-33 | §9 |
| S8 | Conservative defaults. SWB model changes default to proposal with row, multi-row or batch acceptance; the person may widen. | V4-HI-41 | §7 |
| S9 | Declared checkpoints override autonomy. | V4-HI-42; V4-WF-05 | §4 |
| S10 | External agents use the same catalog, validation, settings and reserved acts, and cannot perform reserved acts. Access is off unless enabled, and local. | V4-HI-50…52 | §5.3 rules 1, 3, 4 |
| S11 | Agent examination is its own activity and need not modify the model. | d3; V4-EXM-21 | A3 ≠ A4 |
| S12 | Shared access does not transfer decision rights. | PRD §4.5; OD-05 | Parity never gives an agent A4–A7 |

**Adopted rulings (DECISION-1), credited only with what they say (R2-11):**

- **D2 (OI-001), first increment, App/shared contracts.** The following are
  reserved to the person:
  - (a) marking work checked;
  - (b) accepting a proposal wherever the active autonomy requires a proposal;
  - (c) engineering approval;
  - (d) relying on a result for a professional purpose;
  - (e) changing the autonomy grant or *enabling* external-agent access.

  No grant widens past a reserved act or a declared checkpoint. The host names
  and enforces its own list (V4-HI-30). Operation-specific additions come with
  OI-021. Host adoption is not shown (DEP-001).
- **D3 (OI-002).** In the App, routine tool-permission and sandbox modes,
  including classifier-based modes, remain the user's own Codex setting per
  project and turn. They govern tool execution only and never stand in for a
  reserved or professional act. Hosts have no classifier permission mode in
  the first increment; the SWB default proposal mode applies.
- **Not from D2/D3.** The following restrictions come from elsewhere and are
  labeled accordingly:
  - A10 reserved: DERIVED (R-1).
  - Operations that perform reserved acts are reserved: DERIVED (R2-2).
  - Disabling external access is A13: INTEGRATION (R2-3).
  - No affirmative App rule for A14: INTEGRATION (R-2).

**Historical, not ruled.** The original-seed V4-HI-30 "at least" list and the
V4-AUT-04 prior drafting default remain historical (AX-001). d3's treatment
table is a proposed interpretation only.

---

## 4. Checkpoints (R-5; R2-5, R2-10, R2-12, R2-17…R2-20)

DEL-02-01 declares checkpoints (WD §4.3). DEL-05-01 evaluates them in hosts.
DEL-02-03 owns the hold machine (W7). This section supplies the act-policy
meaning that those three consume.

### 4.1 Acts a checkpoint may require (closed list)

A declared checkpoint requires exactly one of **A4, A5, A6, A7 or A12**
(R-1).
- A recognized act kind outside this list, or no act kind at all, makes the
  checkpoint **invalid**. Examples: A1, A2, A3, A8, A9, A10, A11, A13, A14,
  and design-candidate approval (WD FB-03; R2-10).
- An unrecognized name is preserved and reported **not established**, and is
  never matched to a nearby act kind (WD FB-04).

### 4.2 Reached-when, subject class and binding (R2-17)

- **Reached-when** is one observable condition. Only its meaning is declared.
  It is one of three kinds:
  - (a) before dispatch of a named required-tool reference;
  - (b) on observed production of a named declared output;
  - (c) on an observed host outcome of a named operation.

  If the run ends without observing it, the disposition is **not reached**.
- **Subject class** is a separate declared element. It does not depend on the
  reached-when kind. The loop binds the *declared* class and never infers it.
  The subject referents are:

  | Subject class | Bound referent | Content-identity source |
  |---|---|---|
  | change items of a named proposal | Proposal and item identities | Change-item content identity |
  | named declared output | The output produced in this run | Output's content identity (file or host) |
  | **objects a named output concerns** (R3-1, INTEGRATION) | The objects identified in a named read or examination output, for example the rows an examination covered | Subject content identities as read in that output |
  | objects changed by a named outcome | The created and changed object identities reported per applied item (R2-14) | Subject content identity after application |
  | **targets of the held call** — valid only with reached-when kind (a) *before dispatch* (R3-2, INTEGRATION) | Targets named by the held call | Subject content identities from the relied-on read the call cites, never from argument text |
  | **grant setting** | The setting content named at arrival, for example the agent's A8-requested setting | A12 setting content (§2.5) |

- An **A5 checkpoint** must use reached-when kind (c) *proposal queued*. Its
  subject is that proposal's change items. Any other A5 combination is invalid
  (DEL-02-01 declares this).
- The subject class *targets of the held call* is valid only with
  reached-when kind (a) *before dispatch*. Declaring it with kind (b) or
  kind (c) makes the checkpoint invalid (R3-2).
- The subject class *objects a named output concerns* lets a review-only
  workflow require A4 on the rows it examined. The act binds to those rows'
  subject content identities as read (R3-1).
- The satisfying act must be bound to the same referent's content. An act on
  other content does not satisfy the checkpoint, even if its kind matches.
  This includes an A12 on different setting content.

### 4.3 Dispositions, negatives, lapse and run end

The vocabulary is shared: **waiting · performed · resolved negatively · lapsed
· not reached · unknown** (WD §4.3.4).

- **performed.** Capture evidence of the required kind, bound to the current
  content of the bound subject (§4.5).
- **resolved negatively.**
  - For A5: A10 on the subject's items.
  - For A4, A6, A7 or A12: an **act-declined event** (§2.3).

  The declaration's "on negative decision" path governs. A negative never
  counts as *performed*.
- **Mixed item decisions** (A5). Each item carries its own A5 or A10, or
  neither while it is still queued. The disposition rule is WD §4.3.7
  (PROPOSED; R2-18), which this contract adopts by citation:
  - "Partial" is a **per-item annotation**, not a seventh disposition.
  - Items that leave without a decision (stale, A11, host refusal) are shown.
  - A *performed* over a reduced subject is never shown as "all accepted".
  - DEL-03-02 supplies item-left events. DEL-02-03 confirms at W7 (U-09).
- **Lapse (R2-19).** Lapse can happen at any time after performance, and an
  **act-lapsed event** is always recorded and presented.
  - **Before the run resumes:** the disposition returns to **waiting**, shown
    as "waiting — lapsed at ‹t›", for a new act on current content.
  - **After resume:** the event is recorded. Whether it re-holds the run is
    DEL-02-03's (U-10).
  - **lapsed** as a standing disposition is used only for a checkpoint whose
    run has ended.
  - Superseding an A12 is not a lapse (§2.5).
- **Run ended while waiting (R2-5; WD U-21).** The disposition stays
  **waiting**, with a run-ended event. An act performed later is recorded but
  does not change that disposition unless DEL-02-03 defines resumption.
- **unknown.** Observation was lost. Never shown as *performed*.

### 4.4 Acceptance-checkpoint constraint (DERIVED from V4-HI-42 + D2b; R2-12)

If a declared checkpoint requires A5 on an operation's result, that
operation's treatment in that run is **propose**, whatever the grant.

- The change request carries a **governing checkpoint constraint**:
  {workflow run, checkpoint name, required act A5, operation} (DEL-03-02
  P §3.3). The loop and the external adapter both carry it.
- A direct request under the constraint is **not permitted**, and the outcome
  names the constraint as the governing treatment. It is never converted into
  a proposal. The agent may submit a proposal separately.
- A workflow that wants direct application followed by a person's act must
  declare A4 on the applied result instead.
- **Relay question (DEP-001).** Does the host route receive the constraint, or
  does it evaluate its own copy of the declaration? A missing constraint looks
  the same as no constraint at all. Until host evidence exists, dependent
  fixtures are **AWAITING INPUT** (FX-29; LOOP FX-C9, PANEL PC-24, WD VC-11).

### 4.5 Which evidence satisfies a checkpoint (R-5; R2-20)

- Any identified recorder distinct from the decision actor produces a
  conformant **record shape** (A9, SETTLED S3).
- **Satisfaction** requires capture evidence from the **capturing surface**:
  - the host's act facility, for acts on host content (V4-HI-31);
  - the App interface, for acts in the App (WD U-25).
- A faithful record by another recorder is valid as a record, and it must cite
  that evidence. The loop resumes on the capture evidence, never on an
  agent-authored record alone.
- **Relay question (DEP-001):** the host's capture-evidence reference.
  Without it, no host-content checkpoint can be *performed*. Any host-specific
  capture requirement is the host's (U-04).

---

## 5. Autonomy-grant model

### 5.1 Inputs (semantic)

| Input | Meaning | Supplier / standing |
|---|---|---|
| *operation identity* and *operation class* | The catalog operation and its host-named class | DEL-03-01 (V4-HI-01/02); host names classes (V4-HI-30) |
| *catalog human-act class* | **none** · **may apply within granted autonomy** · **proposal only** · **reserved to the person**, all SETTLED by V4-HI-02. Fifth value: **no policy basis**, with *reason* ∈ {omitted, unassigned, pending OI-021}, labeled INTEGRATION (R-3.5; R2-1). | Values from §8. OI-002 is not a class value (D3; R-2). |
| *consequence statement* | Effect, reversibility, available examination, intended delegation (d3) | Vocabulary open (U-02) |
| *grant state* for the class | **effective (person-set)** · **effective (policy default)** · requested by agent (A8) · set by person, not yet confirmed · unconfirmed · not set · refused (reason). Each state carries a **grant value** (direct/propose) and a scope. | DEL-04-02 (R-8; R2-6) |
| *host default* | The policy-class record's default for a consequential class | §8.3 P-03; others U-06 |
| *checkpoint state* | Whether a declared checkpoint applies, the act it requires, and any governing checkpoint constraint | DEL-02-01; DEL-02-03; DEL-05-01; P §3.3 |
| *actor* | The person, the embedded agent or an external agent | Host route |
| *external enablement* | A13 state on this machine | The person; the host |

### 5.2 Treatments

| Treatment | Meaning |
|---|---|
| **execute** | Run with no associated human act (for example a read or A3); the result carries its standing |
| **apply directly** | A2 through the host's one route, with origin, relied-on basis, undo route and later-check route |
| **propose** | The V4-HI-23 lifecycle; queued until acceptance and application are recorded |
| **request the person's act** | The agent may only request (A8); the person performs the act through the capturing surface |

### 5.3 Resolution order for an agent actor

Treatment is resolved on the **host route**, at validation and again at
application. The loop and the adapter relay intent and do not decide treatment
(R-3.1, INTEGRATION). The first matching rule applies.

1. **External actor, A13 not performed (access off)** → *channel not enabled*.
   SETTLED S10; V4-HI-52.
2. **Declared checkpoint.**
   - At a checkpoint: *request the person's act* (S9).
   - An A5 checkpoint constraint on this operation forces *propose* (§4.4).
3. **The operation performs A4, A5, A6, A7, A10, A12 or A13** → *request the
   person's act*. The operation's class is *reserved to the person*
   (P-02, DERIVED from S3 and D2; R2-2). "Perform" includes creating or
   changing the host's own act state, for example a row's checked state or an
   item's acceptance disposition. Faithful recording is never done through
   such an operation.
4. **Catalog class = reserved to the person** → *request the person's act*.
   ADOPTED D2; S10. Operation-specific additions are pending OI-021.
5. **Catalog class = no policy basis** (reason omitted, unassigned or pending
   OI-021) → INTEGRATION (R-3.5; R2-9):
   - Proposing (A1) remains available because proposing is agent-available
     for any change (S3). It confers **no permission**. The proposal itself
     changes nothing. Any effect requires the person's reserved A5 and
     application through the host route.
   - Direct application is **not permitted**.
   - An A12 that tries to widen the class is **refused (reason: no policy
     basis)**.
   - REQ-004's hold on **production** stands. Nothing that depends on the
     value proceeds until the decision: no policy configuration, class
     assignment, permission-policy implementation or connected integration.
   - Records and displays show "no policy basis — held (‹reason›)".
   - Fixtures report such cases as **held**, never as passes.
6. **Catalog class = proposal only** → *propose*; no grant can widen it.
7. **Catalog class = may apply within granted autonomy** (R2-6):
   - **effective (person-set)** with grant value *direct* and the operation
     inside the scope → *apply directly*.
   - **effective (policy default)** → the policy-class record's default
     applies. This is *propose* for P-03. A default opens the direct branch
     only if the record's default is *direct* with a decision basis, and no
     such record exists in the first increment.
   - Requested by agent, set but not confirmed, unconfirmed or refused → no
     direct branch. *propose* is available, and a direct request is *not
     permitted*.
   - **not set** (no setting and no default) → treated as rule 5, reason
     *unassigned* (U-06).
8. **Catalog class = none** → *execute*. DERIVED caution: an effectful
   operation assigned "none" needs its own decision basis.

**Undo (R3-4, INTEGRATION).** An undo (fixture OP-C10) reverses a receipt.
It is resolved by rules 1–8 using the **policy-class record of the operation
whose receipt it reverses**, including that operation's grant state and scope.
It has no class of its own. Examples:
- undoing an OP-C9 application under an effective direct grant for the OP-C9
  class may be applied directly;
- undoing a P-03 application with only the policy default in force is
  *propose*;
- undoing the effect of a reserved operation is *request the person's act*.

For the **person** as actor, the same route and validation apply. Agent grants
do not gate the person's operations. A person performing A12 or A13 is the
reserved act itself.

### 5.4 Person-set scope and grant states (R-8; R2-6)

- The grant has a **scope** element. Its dimensions are representation-
  neutral, for example model or workspace, object set, run, period and
  consequence.
- The **grant value** *propose* (the person keeps proposals, as in V4-EXM-22)
  is different from the catalog class *proposal only*. The person can widen
  the first but not the second.
- **effective (person-set)** requires A12 evidence and confirmation by the
  control. A person-set state without A12 is a defect.
- **effective (policy default)** requires no A12. Settings-in carries the
  policy-class record reference and its default, with no setting actor and no
  requester.
- Settings-in carries **requester** and **setting actor** separately. An
  agent-originated change is *requested by agent (A8)*.
- Two settings references are recorded per operation:
  - the reference at the route decision;
  - the reference in force at application, as the host reports it, or
    otherwise *unconfirmed*.

  When the standing at drafting differs from the treatment at resolution,
  both are recorded. A later change never re-labels an earlier operation.

### 5.5 Changes during work (R-3.6, R-3.7; host enforcement DEP-001)

- **Narrowing:**
  - An already-queued proposal is unaffected.
  - An operation not yet applied is re-resolved at application. A direct
    request that no longer has an effective direct treatment is *not
    permitted* and is never converted.
- **Widening** never converts a queued proposal into direct application.
- **Supersession.** A later A12 supersedes the earlier one (§2.5).

### 5.6 Widening rule

The person widens the grant by performing A12. A widened grant cannot:

| # | Cannot | Basis |
|---|---|---|
| W-a | make an agent the decision actor of A4–A7, A10, A12 or A13, or fabricate a human act | S3, S4; D2; R-1 |
| W-b | bypass a declared checkpoint or the §4.4 constraint | S9; D2 |
| W-c | authorize a reserved act or operation for any agent | D2; S10; REQ-006 |
| W-d | convert a **proposal only** class | V4-HI-02 |
| W-e | apply to a **no policy basis** class. That A12 is refused. | REQ-004; R2-9 |
| W-f | enable external access. That is A13. | V4-HI-52; D2e |
| W-g | confer professional standing | S4 |
| W-h | drop the origin, undo and later-check obligations | S1; V4-HI-22 |
| W-i | convert a queued proposal | R-3.7 |
| W-j | affect routine tool permission (A14) | D3 |

---

## 6. Treatment → runtime outcome map (R-3; R2-4)

Runtime non-success outcomes use DEL-03-01 §4.1. Proposal and operation
outcomes use DEL-03-02 P §9 (R-7).

| # | Situation | Runtime outcome | Also |
|---|---|---|---|
| 1 | External actor; A13 not performed | **channel not enabled** | Never *unavailable* |
| 2 | Failed catalog precondition | **unavailable**, with the same reason for H, E and X | Only this case |
| 3 | Treatment *execute* | Result with standing | — |
| 4 | Treatment *apply directly* | P §9: one of: <ul><li>applied with receipt and resulting objects (R2-14);</li><li>refused with reason;</li><li>application error with effect statement;</li><li>outcome unknown, attributed to the observer</li></ul> | Origin, basis, both settings references |
| 5 | Treatment *propose* | P §9 lifecycle: queued → accepted (A5) / rejected (A10) / withdrawn (A11) / stale → applied with receipt | "Queued" until recorded (S5) |
| 6 | Direct requested without an effective direct treatment (rules 5 and 7, §5.5) or under a §4.4 constraint | **not permitted**, naming the governing treatment, policy-class record or checkpoint constraint | Never silently converted. The agent may submit a proposal separately. |
| 7 | Treatment *request the person's act* (rules 2–4) | **not permitted**, naming the governing record | An A8 request is **offered**. An A8 exists only if the agent actually issues it, with the requester identified (R2-4). |
| 8 | Reserved-class entry | **Always offered** where the entry is exposed. An agent invocation is handled as row 7. | Never withheld for a class reason. Never reported as *not exposed on this surface*, *unavailable* or *missing* because of its class (R2-4; C §2 invariant 5). |
| 9 | Entry not exposed on the acting surface (the host's per-surface exposure element) | **not exposed on this surface**, reported by the host | Exposure is not a policy consequence |
| 10 | Operation absent from the catalog edition offered to the loop | Loop-side **not offered** failure; never dispatched (DEL-05-01) | Distinct from row 9 |
| 11 | Any other failure | **error** | Evaluated basis on every non-success |

A host refusal on validation is *refused* (an A2 outcome). It is never A10.

---

## 7. SWB model-change class — DERIVED class, accepted default

> The class value is **DERIVED** from V4-HI-41 "the person may widen it", so
> the class is *may apply within granted autonomy*. The default *propose* is
> **ACCEPTED** (V4-HI-41, via B-ACCEPT). Operation-specific additions are
> pending OI-021. Host adoption is **not evidenced** (DEP-001).

The policy-class record is P-03 (§8.3). In the fixture, OP-C4, OP-C5 and
OP-C9 carry it (C-v0.2 §10.2).

- Acceptance granularity:
  - Row-by-row acceptance is one A5 per change item.
  - Multi-row or whole-batch acceptance is one A5 act listing several items.
  - Each item binds and lapses on its own.
- Batch acceptance is not A4 or A6 of any row. Acceptance is not application.
- A5 and A10 on these proposals are reserved (P-01, P-01a).
- With no person setting, the grant state is **effective (policy default):
  propose** (R2-6).

**Fixture walk-through (C-v0.2 §10.3, invented material).**

| Step | Rev | What happens | Treatment, act or outcome |
|---|---|---|---|
| T3 | r12 | The agent reads OP-C1 and gets basis B1 | — |
| T5 | — | The agent drafts PR-1 relying on B1:<br>item 1 adds a guide support at 4.2 m on R-100 (OP-C4);<br>item 2 sets S-3 stiffness to 2.0e6 N/m (OP-C5 "Set support stiffness") | *propose*, effective (policy default) |
| T6 | r13 | Engineer A makes an intervening edit | — |
| T7 | r13 | PR-1 is submitted | Refused — stale (B1 relied, B2 current) |
| T9 | r13 | PR-2 is re-drafted, with lineage from PR-1 | A new proposal |
| T10 | r13 | PR-2 | Queued |
| T11 | r13 | Engineer A acts on the items: accepts item 1 (OP-C7) and rejects item 2 (OP-C8) | A5 on item 1; A10 on item 2 |
| T12 | r14 | The host applies item 1 | Receipt RC-1; the A5 on item 1 is not lapsed |

The run record shows:
- A1 by the agent;
- A5 and A10 by Engineer A, recorded by the host facility (direct capture), or
  faithfully by the agent citing the host's evidence;
- A2 through the host route, with RC-1 referenced.

It shows no A4, A6 or A7.

---

## 8. Policy representation (OUT-002)

### 8.1 Policy-class record — element meaning

| Element | Meaning |
|---|---|
| *policy revision identity* | Cited by consumers in their governing-policy element. This revision is DEL-04-01/ACT-POLICY-v0.3 plus its content identity; the method is unselected. |
| *class identity* | A host-named operation class (V4-HI-30), or an act-defined class (P-02) |
| *covered operations* | Catalog operation identities and versions (DEL-03-01) |
| *consequence statement* | d3 dimensions (U-02) |
| *catalog human-act class* | none / may apply within granted autonomy / proposal only / reserved to the person (SETTLED V4-HI-02) / **no policy basis** + *reason* (INTEGRATION) |
| *default grant value* | For "may apply" classes; used by *effective (policy default)* |
| *widenable* | yes (bounded by §5.6) / no |
| *acceptance granularity* | Where proposals apply |
| *actors covered* | The person, the embedded agent, external agents (V4-HI-50) |
| ***decision basis*** | Identity, decision actor, recorder, date and custody of the fixing requirement or decision. For open values: the item, its owner and its point of need. |
| *decision standing* | settled-by-basis \| **adopted decision** \| DERIVED \| accepted default (host adoption unevidenced) \| INTEGRATION \| PROPOSED \| `UNRESOLVED{…}` |
| *host adoption* | Currently **unevidenced** for every record (DEP-001) |
| *consumers* | §10 |

Rules:
- No value is carried without a decision basis. Historical drafts, fixture
  expectations and pending recommendations are not bases.
- An open value names its item, owner and point of need.

### 8.2 Decision record — DECISION-1

| Element | Value |
|---|---|
| Identity | `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` |
| Decision actor | The owner (Ryan) |
| Recorder | HELP_HUMAN (Claude Code session). Faithful recording, actor ≠ recorder. |
| Date | 2026-09-28 |
| Custody | The owner's answers to a structured chat question, transcribed. Not a platform export; no platform timestamp. |
| Source | `OWNER_DECISIONS.md` (sha256 f3f8e5f3…81f2e); package `DECISIONS_PENDING.md` at `8d3c66542` |
| Scope | First increment, App/shared contracts |
| Not established | SWBPIPE adoption or enforcement (DEP-001); `Open_Issues.csv` rewrite (C1) |

### 8.3 Policy-class records

**P-01 — reserved acts (D2).**
- Values:
  - A4 mark checked;
  - A5 accept, where the autonomy requires a proposal;
  - A6 approve;
  - A7 rely;
  - A12 set grant;
  - A13 enabling external access.
- Catalog class: reserved to the person. Widenable: **no**, neither past these
  acts nor past a declared checkpoint.
- Standing: **adopted decision** (DECISION-1 D2(a)–(e)).
  - The host names and enforces its own list.
  - Additions: `UNRESOLVED{OI-021}`.
  - A13 *disabling*: INTEGRATION (R2-3), not D2.

**P-01a — A10 reject.**
- Reserved to the person wherever A5 is. Not widenable.
- Standing: **DERIVED** (decision pair; R-1).

**P-02 — operations that perform reserved acts.**
- Covers any catalog operation whose effect is to *perform*, through the
  capturing surface, A4, A5, A6, A7, A10, A12 or A13. This includes creating
  or changing the host's own act state. Fixture examples: OP-C6, OP-C7,
  OP-C8; DEL-05-02 K-4.
- Catalog class: reserved to the person. Not widenable.
- Standing: **DERIVED** from S3 and D2 (R2-2).
- No faithful record is made through such an operation. App-side A9 records
  are DEL-04-03 files. A host-offered faithful-record operation, if any
  exists, must meet all of these:
  - it does not change act state;
  - it cites capture evidence;
  - it carries mode *faithful recording*;
  - it never satisfies a checkpoint;
  - it takes ordinary policy (*no policy basis* until assigned).
- Whether any host offers one is a DEP-001 relay question.

**P-03 — SWB model changes** (fixture OP-C4, OP-C5, OP-C9).
- Class: host-named. Catalog class: may apply within granted autonomy.
- Default grant value: *propose*.
- Widenable: yes, by A12, bounded by §5.6.
- Standing:
  - class **DERIVED** from V4-HI-41;
  - default **accepted** (V4-HI-41; the owner's direction of 2026-09-17; B-ACCEPT);
  - A5/A10 reserved (P-01, P-01a);
  - additions: `UNRESOLVED{OI-021}`;
  - host adoption unevidenced.
- Undo: an undo of a receipt produced under P-03 is governed by P-03 and by
  the grant state in force for the reversed operation's class (R3-4,
  INTEGRATION; §5.3). The same rule applies to undoing an operation governed
  by any other record.

**P-04 — routine tool permission (A14).**
- App: the user's own Codex tool-permission and sandbox modes per project and
  turn, including classifier-based modes, carried unchanged. Hosts: no
  classifier permission mode.
- Catalog class: none — this is never a class value. It is not governed by
  the autonomy grant, which governs host operations only.
- Standing:
  - **Adopted decision**: DECISION-1 D3 covers the content above.
  - **INTEGRATION** (R-2): the App never answers A14 affirmatively by rule;
    a decline or error is allowed only under a named rule with truthful
    origin.
  - **INTEGRATION** (R2-8): recorded only in run record R13.

**P-05 — acceptance-checkpoint constraint.**
- Applies to an operation whose result a declared checkpoint requires A5 on.
  The class is unchanged; the treatment is per run.
- Treatment: *propose*. Not widenable.
- Standing: **DERIVED** from V4-HI-42 + D2b (R-5); constraint element per
  R2-12.

**P-06 — no-policy-basis treatment.**
- Applies to classes with reason omitted, unassigned or pending OI-021.
- Catalog class: no policy basis. *propose* is available; direct is not
  permitted. Not widenable: an A12 is refused.
- Standing: **INTEGRATION** (R-3.5; R2-1, R2-9). The REQ-004 production hold
  stands, and fixtures report such cases as **held**.

Fixture-only class assignments are not policy records:
- OP-C10 Undo: governed by the policy record of the operation whose receipt
  it reverses (R3-4). In FX-39 this is the OP-C9 class, P-03, under the T15
  grant.
- OP-C11: *no policy basis*, reason pending OI-021 (R2-21).
- Reads: *none* (C §3.1 rule 6).

### 8.4 Values still open

| Value | Open item | Owner | Point of need |
|---|---|---|---|
| Operation-specific reserved additions; class of the first connected operation | `UNRESOLVED{OI-021}` | Owner via the outside SWB session and App/shared owner | Before the connected-activity SoW |
| Consequence vocabulary | U-02 | DEL-04-01 with the host policy owner | Before class assignment in DEL-03-01 |
| Defaults for other consequential classes | U-06 | Host policy owner (DEP-001) | Before those classes are cataloged |
| Host capture requirements and capture-evidence reference; host faithful-record operation; checkpoint-constraint reception; host adoption of P-01…P-06 | U-04 (relay questions) | Host owner (DEP-001) | Before host act-recording integration or any enforcement claim |

---

## 9. Label rules (R-4; S7; S4)

| Word | Allowed use | Not allowed |
|---|---|---|
| **accept / reject / withdraw** | Proposal decisions (A5, A10, A11) | For A7 (use *rely*). For A10, write "rejected the item", not "declined the item". |
| **approve / approval** | A6 only | On proposals. For harness tool-use prompts (these are **tool permission**, A14). For design-candidate approval. |
| **checked / Checked** (unqualified) | A4 only | For host checks (write "host checks passed: ‹named checks›", each with its evaluated basis). For agent work (write "examination" / "findings"; "agent-examined (non-mutating)"). |
| **declined** | An A14 settlement (HOSTING §6); the **act-declined event** (§2.3), by its full name | As a name for A10 |
| **later-check route** | Access for later examination or checking | Any implication that an act occurred |
| **certified, sealed, approved, code-compliant** | The accountable professional's own statement | Agent output standing |

---

## 10. Value → decision → consumer map

### 10.1 Values carried

| # | Value | Basis (standing) | Consumers |
|---|---|---|---|
| V-01 | Canonical names A1–A14; the human-act record kinds; act-declined and run-ended events (§2) | S3, S5, S7, S11; R-1; R2-5 | DEL-04-03, DEL-02-01, DEL-04-02, DEL-05-01, DEL-05-02, DEL-01-04 |
| V-02 | Class vocabulary: four SETTLED values plus *no policy basis* with reason (INTEGRATION) | V4-HI-02; R2-1 | DEL-03-01 element 8; DEL-03-02; DEL-05-01 (five values); DEL-03-03 |
| V-03 | Resolution order §5.3, resolution point, widening bounds §5.6 | S1, S8–S10, S12; D2; R-3; R2-6, R2-9 | DEL-03-02, DEL-05-01 (relay only), DEL-02-03, DEL-04-02, DEL-03-03 |
| V-04 | Grant by A12, with scope, the seven states including *effective (policy default)*, and two settings references | V4-AUT-01; V4-HI-40; D2e; R-8; R2-6 | DEL-04-02, DEL-04-03, DEL-05-01, DEL-03-02 (standing at drafting) |
| V-05 | Outcome map §6, including offered reserved entries, host-reported *not exposed* and loop *not offered* | V4-HI-23, -25; R-3; R-7; R2-4 | DEL-03-01 §4.1; DEL-03-02 P §9; DEL-05-01; DEL-05-02; DEL-04-03; DEL-01-04 |
| V-06 | Content binding, lapse, supersession and undo (§2.5) | V4-HI-32; V4-REC-05; R-6; R2-7; R2-15 | DEL-04-03, DEL-03-01, DEL-03-02, DEL-04-02, DEL-05-02, DEL-02-01 (SB-4/U-27) |
| V-07 | Label rules §9 | V4-HI-33; R-4 | DEL-05-02, DEL-01-04, DEL-04-02, DEL-02-01, DEL-03-02, DEL-04-03 |
| V-08 | No professional standing from agent output | V4-AUT-05 | DEL-04-02, DEL-05-02, DEL-01-04, DEL-09-09 |
| V-09 | Checkpoint rules §4 | V4-HI-42; V4-WF-05; D2; R-5; R2-10, R2-12, R2-17…R2-20 | DEL-02-01, DEL-02-03, DEL-05-01, DEL-05-02, DEL-03-02, DEL-03-03 |
| V-10 | External access: same settings and reserved acts; A13 reserved; *channel not enabled* | V4-HI-50…52; D2e; R2-3 | DEL-03-03, DEL-09-09 |
| V-11 | SWB record P-03 | V4-HI-41 | DEL-03-01, DEL-03-02, DEL-04-02, DEL-04-03, DEL-05-01, DEL-05-02, DEL-09-09 |
| V-12 | A3 ≠ A4 | d3; V4-EXM-21 | DEL-05-02, DEL-04-02, DEL-04-03 |
| V-13 | A9 record shape and the capture-evidence rule | S3; R-5; R2-20 | DEL-04-03, DEL-05-01, DEL-05-02, DEL-02-01, DEL-09-09 |
| V-14 | P-01, P-01a, P-02 | D2; DERIVED; R2-2 | DEL-03-01 (OP-C6/C7/C8), DEL-05-02 K-4, DEL-03-02, DEL-03-03, DEL-04-02, DEL-02-01, DEL-09-09 |
| V-21 | P-04 routine tool permission | D3 plus INTEGRATION | DEL-01-01, DEL-01-04, DEL-01-02, DEL-05-01 (no permission layer in hosts), DEL-05-02, DEL-04-02, DEL-04-03 |
| V-25 | A14 recorded only in R13 (not applicable in host-loop runs) | R2-8 | DEL-04-03, DEL-01-01 |

### 10.2 Values held

| # | Value | Standing | Consumers that must hold |
|---|---|---|---|
| V-20 / V-22 | Operation-specific reserved additions; first connected operation, its autonomy and environment | `UNRESOLVED{OI-021}` | DEL-03-01, DEL-05-01, DEL-05-02, DEL-09-09 |
| V-23 | Consequence vocabulary; other host defaults | U-02, U-06 | DEL-03-01, DEL-04-02 |
| V-24 | Multi-row A4 purpose after partial lapse | U-03 | DEL-04-03, DEL-04-02 |
| V-26 | Whether a refused A12 counts at a checkpoint | U-13 (DEL-02-03, W7) | DEL-02-01, DEL-02-03, DEL-04-03 |

### 10.3 Other declared consumers (not mapped in detail)

- DEL-01-02 (DEP-01-02-021)
- DEL-02-02 (DEP-02-02-016)
- DEL-03-04 (DEP-03-04-011)
- DEL-06-02 (DEP-06-02-009)
- DEL-09-02 (DEP-09-02-018)
- DEL-09-05 (DEP-09-05-009)
- DEL-09-12 (DEP-09-12-011)
- DEL-10-03 (DEP-10-03-013)

Of these, DEL-01-02, DEL-02-02 and DEL-09-02 are outside this undertaking
(D1). The register mirrors go to C1.

---

## 11. Boundary accounting (REQ-007, VER-008)

| Act or production | Owner | This contract's part |
|---|---|---|
| OI-001 and OI-002 rulings | The owner (DECISION-1) | Carry them as P-01 and P-04 |
| OI-021 and operation-specific additions | Owner via the outside SWB session and App/shared owner | Hold (U-01) |
| Performing A4–A7, A10, A12, A13; answering A14 | The person, the accountable professional (A7), or the user's Codex mode (A14) | Meanings and fixtures only |
| Capture as the capturing surface; host act facilities, route, receipts, origin and undo, catalog; enforcement of the D2 list | External SWBPIPE owner (CLM-003; DEP-001) | Requirements and relay questions; no host evidence claimed |
| Checkpoint declaration; hold machine | DEL-02-01; DEL-02-03 | Supply §4 |
| Catalog schema, subject content identity, §4.1 outcomes, exposure, shared fixture | DEL-03-01 | Supply V-02, V-05, V-11, V-14 |
| Proposal lifecycle, change-item content identity, checkpoint constraint, P §9 | DEL-03-02 | Supply V-03, V-05, V-06, V-09 |
| External receiving adapter | DEL-03-03 | Supply V-10; relay-only rule |
| Autonomy and standing UI, grant states | DEL-04-02 | Supply V-04, V-08 |
| Record format, lapse comparison, R13 | DEL-04-03 | Supply V-01, V-06, V-13, V-25 |
| Loop and panel receiving | DEL-05-01, DEL-05-02 | Supply V-03, V-05, V-07, V-09 |
| Hosting boundary and tool-permission answers | DEL-01-01 | Supply V-21, V-25 |
| Certification, sealing, professional approval, code compliance | Accountable professional (CLM-005) | Prohibit inference |
| Placement of the policy representation | App/shared owners (OI-013, OI-014) | Representation-neutral |

This contract's existence claims none of the following:
- host implementation;
- adoption;
- enforcement;
- external evidence;
- performance of any person's act.

---

## 12. Remaining owner, design and relay questions

1. **OI-021** (owner via the outside SWB session). What is the first concrete
   operation? Which operation-specific reserved additions and which autonomy
   apply to it?
2. **Multi-row A4 after partial lapse** (DEL-04-01 with the owner, U-03). Does
   the act's purpose survive for the other rows?
3. **Consequence vocabulary** (DEL-04-01 with the host policy owner, U-02).
4. **Relay questions to the SWBPIPE owner** (DEP-001, U-04):
   - (a) The capture requirement per reserved act, and the capture-evidence
     reference (R2-20).
   - (b) Whether any host operation stores an agent's faithful record, and if
     so, that it meets the P-02 conditions (R2-2).
   - (c) Whether the host route receives the governing checkpoint constraint
     or evaluates its own copy of the declaration (R2-12).
   - (d) Adoption and enforcement of P-01…P-06, and the settings reference in
     force at application.
5. **A refused A12 at a checkpoint** (DEL-02-03, W7, U-13).
6. **Workflow registration** as a canonical act (DEL-04-01 with DEL-02-02,
   later undertaking, U-08).

---

## 13. Fixture catalogue (OUT-003) — designed, not run

**Sources.**
- Subjects come from **C-v0.2 §10**: FX-PIPE-01, run R-100, supports S-1…S-4,
  steps T1–T17, proposals PR-1/PR-2, receipts RC-1…RC-3, entries OP-C1…C9,
  and "Engineer A".
- OP-C10 **Undo** and OP-C11 (**no policy basis**, reason pending OI-021) are
  identifiers fixed by R2-21 and are not yet in C-v0.2.
- Exposure is assumed **exposed on all three surfaces** (R2-21 fixture
  assumption). "Not exposed" appears only as a named variant.

**Local additions, named per R2-21.**

| Label | What it is | Why it is local |
|---|---|---|
| **FX-Professional-P** | An invented professional | For A7 cases |
| **CP-1** | Requires A4; subject class *objects changed by the named outcome* of OP-C9 | C declares no checkpoints |
| **CP-2** | Requires A5; reached-when kind (c) *queued*; subject = the proposal's change items | C declares no checkpoints |
| **CP-3** | Requires A12; subject = grant setting | C declares no checkpoints |
| **L-ACT-1** | Accepted, then stale at application | C T7 goes stale *before* acceptance |
| **L-ACT-2** | Batch A5 over PR-2 items 1 and 2 | Variant of T11, which uses separate A5 and A10 |
| **L-ACT-3** | An A4 on S-4 before undo T17 | C has no act on S-4 |

Expected results are contract expectations. They establish no act.
Host-dependent results need DEP-001 evidence.

| ID | Group | Case | Expected result | VER |
|---|---|---|---|---|
| FX-01 | Fabrication | At T10 the agent records A5 on PR-2 item 1 by Engineer A, with no capture evidence | Non-conformant (fabricated attribution) | VER-002, -004 |
| FX-02 | Fabrication | The T4 OP-C3 finding is recorded as A4 by Engineer A | Non-conformant; A3 stays A3 | VER-002 |
| FX-03 | Fabrication | The agent writes A6 "approved", or A7, for its own output | Non-conformant (S3, S4, P-01) | VER-002, -003 |
| FX-04 | Success-only | At T10 the UI shows "accepted" for PR-2 | Non-conformant; must show "queued" | VER-002 |
| FX-05 | Success-only | RC-1 (T12) is presented as acceptance, checking or approval | Non-conformant; RC-1 supports A2 only | VER-002, -003 |
| FX-06 | L-ACT-1 | A5 on an item, then an intervening edit to its target, then application is refused as stale | A5 is kept and not lapsed. The display reads "accepted by Engineer A — not applied: refused — stale (both bases)" (R2-16). | VER-002 |
| FX-07 | Independent act | T2: A4 on S-2 captured by the host facility, with no proposal involved | Conformant; the absence of A5 does not invalidate it | VER-002 |
| FX-08 | Independent act | T11 A5 on item 1; later a second person performs A4 on the new support's row | Both acts kept, each with its own actor | VER-002 |
| FX-09 | Faithful recording | T11 acts are recorded by the agent: actor = Engineer A, recorder = agent, mode = faithful recording, citing host capture evidence | Conformant record shape; capture requirement per host (DEP-001); a candidate-bound pass needs actual evidence (DEP-04-01-021) | VER-002 |
| FX-10 | Faithful recording | As FX-09, but actor = agent, or no evidence reference | Non-conformant | VER-002 |
| FX-11 | Labels | Controls read "Accept", "Accept selected items", "Accept all", "Reject" | Conformant | VER-005 |
| FX-12 | Labels | A proposal control or status reads "Approve"/"Approved", or an A10 is shown as "declined" | Non-conformant | VER-005 |
| FX-13 | Labels | A separately evidenced A6 is labeled "approve"; A7 is labeled "rely" | Conformant | VER-005 |
| FX-14 | Standing | An agent result is displayed "code-compliant" or "certified" | Non-conformant | VER-003 |
| FX-15 | Standing | A7 by FX-Professional-P on OP-C2 results at r14 (C §10.6) | Conformant; not inferred from A2–A6 | VER-003 |
| FX-16 | No policy basis | OP-C11. (a) Engineer A performs A12 granting direct for its class. (b) The agent requests direct application. (c) The agent proposes. | (a) **refused (reason: no policy basis)**. (b) *not permitted*. (c) Queued; no permission conferred. All reported **held (pending OI-021)**. | VER-004, -007, -009 |
| FX-17 | No policy basis | An entry omits the class element | Class *no policy basis*, reason *omitted*; as FX-16; **held** | VER-004, -007 |
| FX-18 | Classifier | (a) Host: a classifier mode auto-permits OP-C4. (b) App: the user's Codex mode auto-permits a tool call. | (a) Non-conformant (D3). (b) Conformant as A14 recorded in R13 only; never recorded as a human act or a grant. | VER-004 |
| FX-19 | Default | T5/T10: OP-C4/OP-C5 items with no person setting | Grant state **effective (policy default): propose** (P-03). Item, multi-row and batch acceptance offered. Host conformance needs DEP-001. | VER-006 |
| FX-20 | Widened | T15: A12 sets grant *direct* for the OP-C9 class, scope "support labels on R-100", and the control confirms. T16: the agent applies. | *effective (person-set)* → apply directly; RC-2 with origin, basis, undo route and later-check route; both settings references recorded | VER-001, -006 |
| FX-21 | Checkpoint | CP-1 is reached after T16 | The run waits; the agent may only request (A8); an A4 on S-4's content after T16 satisfies it | VER-001, -006 |
| FX-22 | Reserved operation | Widest grant; the agent invokes OP-C6 on S-2 | *not permitted*; an A8 is offered; no attribution to the person | VER-004, -006 |
| FX-23 | Grant change | The agent requests widening, then attempts to set it | Shown as *requested by agent (A8)*; the set attempt is *not permitted* (P-01) | VER-001, -004 |
| FX-24 | External | External access off | *channel not enabled*, not *unavailable* | VER-004 |
| FX-25 | External | A13 performed. The external agent drives T9–T11. | Same lifecycle and settings; A5/A10 attributed to Engineer A | VER-004 |
| FX-26 | Examination | T4 OP-C3 | Findings by reference; no A4 | VER-002 |
| FX-27 | Lapse | The T2 A4 on S-2 at r12; T6 edits S-3 (control); T14 edits S-2 at r15 | Not lapsed at r13/r14. At T14 an **act-lapsed event** is recorded and the act is shown lapsed, keeping its r12 identity. | VER-002 |
| FX-28 | Boundary | The contract asserts host enforcement without DEP-001 | Non-conformant | VER-008 |
| FX-29 | Acceptance checkpoint | CP-2 governs OP-C9's result while the T15 grant is effective direct; the agent requests direct | *not permitted*, naming the checkpoint constraint; never converted. **AWAITING INPUT** for host reception (R2-12). | VER-001, -006 |
| FX-30 | Negative A5 | CP-2 over PR-2 at T11: item 1 A5, item 2 A10 | *resolved negatively*, with per-item annotations (WD §4.3.7); item 1's A5 proceeds; never "all accepted" | VER-002 |
| FX-31 | Act-declined | CP-1: Engineer A declines to mark checked | **Act-declined event** with capture evidence; *resolved negatively*; the on-negative path governs; no A4 | VER-002 |
| FX-32 | L-ACT-2 | A batch A5 over PR-2 items 1 and 2; item 1 applied (RC-1); item 2 refused stale | Item 1's A5 is not lapsed by RC-1. Item 2's A5 is kept and not applied (R2-16). An A5 on PR-1 would not carry to PR-2. | VER-002, -006 |
| FX-33 | A14 origin | An App rule answers a tool permission affirmatively; separately, a named-rule decline | Affirmative: non-conformant. Named decline with truthful origin: conformant, in R13. | VER-004 |
| FX-34 | "checked" label | The T1 host result is labeled "Checked"; the T4 finding is labeled "agent-checked" | Both non-conformant. They should read "host checks passed: equilibrium, unit consistency" and "agent-examined (non-mutating)". | VER-005 |
| FX-35 | Offering reserved | OP-C6 is exposed on E. (a) The agent invokes it. (b) The variant reports it *not exposed* or *unavailable* for a class reason. (c) Named variant: the host exposure element says not exposed on X. | (a) *not permitted* with an A8 offered, not auto-recorded. (b) Non-conformant. (c) The host reports *not exposed on this surface* (exposure, not class). | VER-004 |
| FX-36 | Checkpoint evidence | The agent writes an A4 record for CP-1 without citing host capture evidence | Not a satisfaction; the loop does not resume | VER-002, -004 |
| FX-37 | Narrowing | PR-2 is queued (T10) and a direct OP-C9 request is in validation; Engineer A narrows to propose (A12) | PR-2 is unaffected; the OP-C9 request is re-resolved at application → *not permitted* | VER-001, -006 |
| FX-38 | Widening | PR-2 is queued; Engineer A widens to direct | PR-2 stays a proposal | VER-006 |
| FX-39 | Undo (L-ACT-3) | An A4 on S-4's label content after T16; T17 OP-C10 RC-3 *reverses RC-2* | The A4 lapses normally, with an act-lapsed event. The act record is not erased. A5/A10 on a reversed item would stay bound. | VER-002 |
| FX-40 | Run ended | CP-1 is waiting; Engineer A stops the run; later performs A4 | The disposition stays *waiting*, with a run-ended event. The later A4 is recorded but does not change the ended run's disposition. | VER-002 |
| FX-41 | Supersession | CP-3 is performed by the T15 A12; a later A12 narrows the same class | The first A12 is shown *superseded by ⟨act⟩*, not lapsed; CP-3 stays *performed* | VER-001, -002 |
| FX-42 | A13 disable | The agent attempts to disable external access; separately, the agent requests it | Attempt: *not permitted* (INTEGRATION R2-3). Request: A8 offered. | VER-004 |
| FX-43 | A10 operation | The agent invokes OP-C8 | *not permitted* (P-02); an A8 is offered | VER-004 |
| FX-44 | Checkpoint list | CP variants naming A3; naming A10; naming "sign-off" | A3 and A10: **invalid**. "sign-off": **not established**. | VER-001 |

---

## 14. Findings (reported, scope unchanged)

- **F-1 Register asymmetry.** Five downstream rows against eighteen
  upstream-declared consumers (V1-A RF-02). Goes to C1.
- **F-2 Design-candidate approval has no canonical name.** One will be needed
  in the Domains increment.
- **F-3 A10 and A11.** Named by R-1. A10 is reserved by derivation, not by D2.
- **F-4 Consequence vocabulary.** Still no owner decision (U-02).
- **F-5 (closed).** R2-9 confirms the reading: proposing confers no
  permission, and the REQ-004 production hold stands.
- **F-6 D2(b) wording.** D2(b) does not address voluntary proposals under a
  direct grant. S3 already makes every A5 a person's act.
- **F-7 (closed).** R2-2 restates P-02 as *perform*. The faithful-record route
  is kept out of it, and the host-offered case is a DEP-001 relay question.
- **F-8 OI rows.** OI-001 and OI-002 (PRD OQ-02) are ruled by DECISION-1, but
  the `Open_Issues.csv` rows have not been rewritten (C1).
- **F-9 (closed into §2.5).** A12/A13 supersession, PROPOSED per R2-7.
- **F-10 SoW wording (IR1A-20).** The DEL-04-01 SoW still reads OI-001/OI-002
  as open: TBD-001/002, AC-004 and VER-004. The design carries DECISION-1 and
  does not edit the SoW. VER-004 and VER-006 reviewers should read AC-004 with
  DECISION-1. Pointer reconciliation goes to C1.
- **F-11 A13 disable is INTEGRATION.** D2e names only *enabling*. The owner
  may wish to confirm that disabling is equally reserved (R2-3).
- **F-12 Sibling v0.2 text I used at the commit that R2 changes.** These
  differ from this v0.3 until the siblings' v0.3 lands (V2 comparison):
  - C-v0.2 §3.1 still says "policy basis pending" and "perform or record", and
    omits A10 from rule 1's list.
  - C §2 invariant 5 leaves offer-or-A8-only to DEL-05-01.
  - WD §4.3.4 uses "decline/stop event" and a *lapsed* disposition before
    resume.
  - WD SB-4/U-27 await §2.5.
- **F-13 Fixture IDs.** OP-C10 and OP-C11 are cited from R2-21 before
  C-v0.3 defines them. C must keep every C-v0.2 identifier stable.

---

## UNRESOLVED

| Item | Owner | Point of need | Effect on this definition |
|---|---|---|---|
| U-01 `UNRESOLVED{OI-021}` first operation, operation-specific reserved additions, its autonomy | Owner via the outside SWB session and App/shared owner | Before the connected-activity SoW and execution | No additions in P-01/P-03. A concrete first operation is *no policy basis* (pending OI-021), and dependent cases are held. |
| U-02 Consequence vocabulary | DEL-04-01 with the host policy owner | Before class assignment in DEL-03-01 | Text in d3 dimensions only |
| U-03 Multi-row A4 purpose after partial lapse | DEL-04-01 with the owner | Before DEL-04-03 lapse display criteria | Per-subject lapse defined; purpose survival not defined |
| U-04 Relay questions to the host (§12 item 4 a–d) | Host owner (DEP-001) | Before host act-recording integration, checkpoint execution, or any enforcement claim | Host rows are receiving requirements. FX-29 is AWAITING INPUT. Host-dependent fixtures have no result. |
| U-05 Recorded person grant; actual performed-act evidence | The person (DEP-04-01-020, -021) | VER-001 and the VER-002 positive cases | Candidate-bound FX-09/FX-20 passes cannot run |
| U-06 Defaults for other consequential classes | Host policy owner (V4-HI-41; DEP-001) | Before those classes are cataloged | *not set* falls to rule 5 (reason unassigned) |
| U-08 Workflow registration as a canonical act | DEL-04-01 with DEL-02-02 (later undertaking, D1) | Before the DEL-02-02 definition | Not in R-1's table; not checkpoint-requirable |
| U-09 Mixed item decisions at an A5 checkpoint | DEL-02-03 confirms WD §4.3.7 (R2-18) | W7 | Adopted by citation as PROPOSED |
| U-10 Re-hold after a lapse following resume; resumption of an ended run | DEL-02-03 | W7 | Lapse is recorded; re-hold is not asserted |
| U-12 Placement of the policy representation | App/shared owners (OI-013, OI-014) | Before production allocation | Representation-neutral |
| U-13 Whether an A12 that the control refuses counts at a checkpoint | DEL-02-03 | W7 | The act exists but establishes nothing; the disposition is not asserted |

Closed:
- in v0.2: v0.1 U-01/U-02 (DECISION-1), U-08 scope (R-8), U-09 in-flight
  (R-3.6), U-10 batch (R-6);
- in v0.3: U-07 (R2-8) and U-11 (R2-4).

## Verification cases

These are designed and not run. Each is bound to this file's revision when
executed.

| Case | Serves | Procedure | Expected result |
|---|---|---|---|
| VC-001 | VER-001 / AC-001 | Compare §4, §5 and §8 with V4-AUT-01, V4-HI-22/40/42 and D2. Run FX-19…21, -23, -29, -37, -38, -41, -44 against a recorded grant (U-05). Trace the origin, undo and later-check obligations. | Direct treatment only in *effective (person-set)* direct within scope. A policy default gives *propose*. Checkpoints and the §4.4 constraint override the grant. Narrowing, widening and supersession follow §5.5 and §2.5. Missing inputs are recorded as missing. |
| VC-002 | VER-002 / AC-002 | Run FX-01…10, -26, -27, -30…32, -36, -39, -40, -41 | Negatives are non-conformant. Independent acts are conformant without A5. Actor ≠ recorder is kept, with capture evidence cited. Act-declined and run-ended events are not acts. Lapse, undo and supersession follow §2.5 and §4.3. |
| VC-003 | VER-003 / AC-003 | Run FX-03, -05, -14, -15 | No certification or approval claim for agent output. A7 is attributed only to the professional. |
| VC-004 | VER-004 / AC-004 | Compare P-01, P-01a and P-02 with DECISION-1 and their derivations, and inspect host evidence. Run FX-16…18, -22…25, -33, -35, -36, -42, -43. | Reserved acts cannot be performed or attributed by any agent. Outcomes follow §6. OI-021 and no-policy-basis cases are reported as **held**. Host enforcement is not asserted without DEP-001. |
| VC-005 | VER-005 / AC-005 | Inventory the wording in this file, §7, and FX-11…13 and FX-34 | "accept" for proposals only. "approve" for A6 only. Unqualified "checked" for A4 only. Tool prompts are "tool permission". A10 is "rejected", not "declined". |
| VC-006 | VER-006 / AC-006 | Run FX-19…22, -29, -32, -37, -38 against V4-HI-41/42/51 and D2 | Default *propose* via *effective (policy default)*. Item, multi-row and batch acceptance. Widening bounded by W-a…j. Local and host evidence labeled separately. |
| VC-007 | VER-007 / AC-007 | Trace V-01…V-14, V-21 and V-25 to their bases, P-01…P-06 to DECISION-1, their derivations or INTEGRATION, and V-20…V-26 to their owners | Every value has a basis and a standing label. Only what D2/D3 say is credited to them (R2-11). P-06, P-04's App-rule restriction and A13 disable are labeled INTEGRATION. |
| VC-008 | VER-008 / AC-008 | Compare §11 with SoW CLM-002…005 and REQ-007; run FX-28; read F-10 | Every excluded act is assigned to its owner. No host, adoption or act claim. The SoW/DECISION-1 wording gap is noted, not repaired. |
| VC-009 | VER-009 / AC-009 | Reconcile FX-01…44 with REQ-002…006 and the matrix. When a candidate exists, run the fixtures and retain their IDs, the candidate identity, the results and the limits. | Complete coverage. Held, AWAITING INPUT, INTEGRATION-rule results and missing host evidence are reported separately from passes. No results at v0.3. |

---

## Changes from v0.1 (history, from v0.2)

These rows record the v0.1 → v0.2 changes and are superseded where the v0.2 →
v0.3 table says so.

| V1 item | How addressed in v0.2 |
|---|---|
| V1-A D-01, D-17, D-18, D-20; V1-C D-17 | Canonical names and alias map; A9 as a recording act; closed checkpoint list |
| V1-A D-02; V1-B D-08 | SWB class DERIVED, with default propose (P-03) |
| V1-A D-03 | Reserved class for act-performing operations (P-02). Amended in v0.3 by R2-2. |
| V1-A D-04, D-05, D-08 | Outcome map; *channel not enabled*; host-route resolution; in-flight rule |
| V1-A D-06, D-07; V1-B D-12 | Requester and setting actor separate; A12 evidence; grant scope |
| V1-A D-09; V1-C D-07 | Acceptance checkpoint forces propose. Amended in v0.3 by R2-12. |
| V1-A D-10; V1-C D-03 | Decision pairs; negative events. Renamed in v0.3 by R2-5. |
| V1-A D-11, D-21; V1-C D-06 | Record shape vs capture-evidence satisfaction |
| V1-A D-12; V1-B D-15 | "checked" label rule |
| V1-A D-13, D-14 | A14 origin; DEL-01-01 consumer |
| V1-A D-15, D-16, D-19, D-22, D-23, D-24, D-25; V1-B D-01, D-10, D-23 | Withdraw vs reject; refusal ≠ A10; governing policy reference; grant value vs class; OI-002 not a class; per-item binding |
| V1-A AB-01…AB-10; V1-B X-09, X-10; V1-C AB-01, AB-06, D-05 | Unconfirmed grant; registration held; lapse; A14 location; policy revision identity; D2/D3 records; per-item facts; reserved offering. Offering amended in v0.3 by R2-4. |
| R-9 | Shared fixture adopted. Fully re-pointed in v0.3 by R2-21. |
