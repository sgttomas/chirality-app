# Operation-Policy and Human-Act Contract
- Contribution: DEL-04-01/ACT-POLICY-v0.1
- Status: DRAFT DEFINITION — proposed, unsupplied, not implemented, not accepted
- Serves: OUT-001, OUT-002, OUT-003; REQ-001…REQ-007; VER-001…VER-009 (AC-001…AC-009)
- Basis: repo 6e18505e3; ScopeOfWork.md sha256 fc1a0503abad4196e869402b664bd76280773d197b5c77994c34e858a406f5e6; `P/docs/PRD.md` §4.1 (V4-WF-05), §4.5 (V4-AUT-01…05), §4.7 (V4-REC-05), §9 (OQ-02, OQ-11), §10; `P/docs/HOST_INTEGRATION.md` §2 (V4-HI-02, -04), §3 (V4-HI-12), §4 (V4-HI-20…25), §5 (V4-HI-30…33), §6 (V4-HI-40…42), §7 (V4-HI-50…52), §9 (V4-HI-70/71); `P/docs/EXAMINATION.md` V4-EXM-20, -21, -22, -25, -31; `P/execution/_Coordination/Acceptances/APP-V4-BASIS-20260926/DECISION_BRIEF.html#d3` (sha256 02d38cb18041c52989d8a2a0b969e6502ce4b25eec85fb0931bbbc100c4420e8); `P/conceptual/DECISIONS.md` OD-05, D-04; `P/conceptual/EXEMPLARS_AND_LESSONS.md` X-09, X-19, X-20; `P/execution/_Decomposition/Open_Issues.csv` OI-001, OI-002, OI-013, OI-014, OI-021; `P/execution/_Decomposition/External_Dependencies.csv` DEP-001
- Consumed inputs: accepted basis only; DEL-03-01 (catalog human-act class), DEL-03-02 (proposal lifecycle and outcomes), DEL-04-02 (grant display states), DEL-04-03 (human-act record), DEL-02-01 (checkpoint declaration) referenced by accepted meaning, to be reconciled at V1
- Receivers: DEL-04-01 is not a SCC-CASE-002 member. Receivers from `Dependencies.csv` DEP-04-01-012…016: DEL-02-01, DEL-02-03, DEL-03-01, DEL-04-02, DEL-04-03. Receivers that declare this deliverable upstream in their own registers: DEL-03-02 (DEP-03-02-017), DEL-03-03 (DEP-03-03-008), DEL-05-01 (DEP-05-01-018), DEL-05-02 (DEP-05-02-008/-014/-015), DEL-01-04 (DEP-01-04-011), DEL-09-09 (DEP-09-09-010); further declared consumers in §8.3

`P` = `projects/chirality-app-v4`. All element names in this document (for
example *act kind*, *decision actor*, *recorder*, *subject content identity*,
*treatment*) are **semantic names, not wire names**. This definition selects no
field name, type, transport, hash or canonicalization algorithm, persistence,
process placement or shared-component placement (OI-013, OI-014). Unruled
policy appears only as `UNRESOLVED{OI-nnn}`. It is never a permission, a
default choice or a pass.

---

## 1. Purpose and reading

This contract gives consumers one meaning for:

- what an agent may do directly, what it must propose, and what only the
  person may do;
- which act happened, who performed it, what it concerned, and what evidence
  supports it.

It defines meanings, the grant model, the policy-class record and the
conformance fixtures. It does not adopt the always-reserved list (OI-001) or
the classifier-permission treatment (OI-002). It performs no human act and
implements no host facility. Where the accepted basis already settles a
distinction, §3 states it as settled and cites it. Everything else is marked.

Three standing labels are used:

| Label | Meaning here |
|---|---|
| **SETTLED** | Stated in the accepted composite (B-ACCEPT) and cited |
| **DERIVED** | A direct consequence of settled clauses; the derivation is shown so a receiver can reject it |
| **UNRESOLVED{…}** | An open issue or an unassigned design detail with its owner and point of need (§11) |

---

## 2. Act taxonomy — actor, subject, evidence

Each *act kind* below has its own actor, subject and evidence. **Evidence of
one act kind never establishes another.** The absence of one act kind does not,
by itself, invalidate an independently evidenced act of another kind (REQ-002;
AX-002). There is no automatic promotion between act kinds and no universal
acceptance prerequisite.

### 2.1 Core act kinds

| # | Act kind (accepted name) | Who may be the decision actor | Subject | Supporting evidence | What it does **not** establish | Basis |
|---|---|---|---|---|---|---|
| A1 | **Propose** (draft and submit a proposal) | Agent (embedded or external) or the person | One proposed change against a cited read basis: target objects, old and new values, reason | Host proposal record with origin and relied-on basis; lifecycle state (queued until acceptance and application are recorded) | Acceptance, application, checking, approval, reliance | V4-HI-21, -23, -24, -25; d3 |
| A2 | **Apply / execute** (run an operation that changes host state) | The person; an agent where the grant permits (direct application); the host's route after acceptance | The operation invocation and its effect on identified objects | Host receipt, origin mark and observed outcome (`applied`, refused with reason, or `outcome unknown`) | That any person accepted, checked, approved or relied on anything | V4-HI-20, -22, -23, -25, -71; d3 ("a receipt records the operation's outcome, not an act of acceptance") |
| A3 | **Examine** (agent examination of engineering work) | Agent | Identified rows, results or models, by read basis | Findings attached by reference, with grounds and limitations; no table change | A human checked mark, approval or acceptance | d3 ("the agent checking the engineer's work is itself a desired activity and need not modify the model"); V4-EXM-21 |
| A4 | **Mark checked** (human checking) | The person | Identified content, scope and purpose (for example one row's content) | Attributable host-recorded act bound to that content; lapses visibly on content change | Acceptance of any proposal; approval; reliance | V4-AUT-03; V4-HI-30 (distinct subject), -32; V4-REC-05; X-20 |
| A5 | **Accept** (accept a proposed edit) | The person | One or more identified proposals (row, multi-row or whole batch for SWB model changes) | Host-recorded acceptance bound to the proposals' content; the label shown is "accept" | Engineering approval; checking; application (application is A2 and has its own receipt) | V4-HI-23, -25, -33, -41; d3 |
| A6 | **Approve** (engineering approval) | The accountable person | Identified engineering content or design | A separate attributable approval record | Professional certification, sealing or code compliance unless the accountable professional separately states it | V4-HI-30 (distinct subject), -33; V4-AUT-03 |
| A7 | **Rely** (professional reliance) | The accountable professional only | A result relied on for a stated professional purpose | The professional's own attributable statement | Anything about agent output; it is never inferred from A1–A6 | V4-AUT-05; V4-HI-30 ("Professional reliance remains with the human"); X-09 |

### 2.2 Companion acts

| # | Act kind | Decision actor | Subject | Evidence | Standing / note |
|---|---|---|---|---|---|
| A8 | **Prepare / request a human decision** | Agent | A decision package naming the exact act requested (A4–A7, a checkpoint act, or a grant change) | The request and its content | SETTLED as permitted preparation (V4-AUT-03; V4-HI-31; V4-PM-04). A request is never the act. |
| A9 | **Faithfully record** an actually performed human act | *Recorder*: agent, host facility or person. The recorder is distinct from the *decision actor* of the recorded act. | A performed act of kind A4–A7 or a checkpoint act | Reference to the act's own evidence, plus recorder identity | SETTLED distinction (REQ-002; d3 "do not record them as performed by the person when they were not"; V4-HI-31). It grants no recording permission. Which recorders may record which act kinds: `UNRESOLVED{OI-001}` (operation-level allocation). |
| A10 | **Reject** a proposal | The person, as shown in V4-EXM-20 | One or more identified proposals | Host lifecycle `rejected` record | Lifecycle state SETTLED (V4-HI-23). Whether rejection is reserved to the person: `UNRESOLVED{OI-001}`. It is never attributed to the person unless the person performed it. |
| A11 | **Withdraw** a proposal | The proposer | Its own proposal | Host lifecycle `withdrawn` record | V4-HI-23. Not a human decision on the proposal's merit. |
| A12 | **Set or change the autonomy grant** | The person | Operation classes and person-set scope (§4) | Recorded grant with its run association | SETTLED that the grant is person-set, visible, changeable during work and recorded per run (V4-AUT-01; V4-HI-40, -41). DERIVED: an agent-originated change is a request (A8), not an effective grant. Whether a grant change is on the reserved list: `UNRESOLVED{OI-001}`. |
| A13 | **Enable external agent access** | The person | The host's external interface on this machine | Recorded enablement | SETTLED: off unless the person enables it; local to the machine (V4-HI-52). |
| A14 | **Answer a routine tool-permission request** (harness or host tool approval request) | The person | One tool execution request | The request settlement (answered or explicitly declined; never by silence or timeout) | SETTLED that it must not be confused with an attributable human or professional act (V4-AUT-04; V4-EXE-02). Its App/host treatment, including classifier-based modes: `UNRESOLVED{OI-002}`. |

Other human acts named elsewhere in the basis keep the same attribution
invariants but are not enumerated here. Examples are workflow registration
(V4-WF-02), stopping work (V4-EXE-01) and reserved coordination decisions
(V4-PM-04). This contract does not redefine them.

### 2.3 Declared checkpoints

A declared checkpoint is not an act kind. It is a point where a workflow
requires one named act kind (A4–A7, or another human act the workflow
declares). DEL-02-01 declares the checkpoint by the accepted act-kind name.
The run waits until the person performs the act; it does not record the act
as done before then (V4-WF-05; V4-HI-42). A checkpoint is satisfied only by
evidence of that act kind. Evidence of another act kind does not satisfy it,
for example an A2 receipt satisfying a checkpoint that requires A4.

### 2.4 Faithful recording — element meaning

A recorded human act carries at least these semantic elements. DEL-04-03 owns
the record format; this is the meaning DEL-04-03 receives:

- *act kind*: an accepted name from §2.1–2.2;
- *decision actor*: the person who actually performed the act;
- *recorder*: the party that wrote the record, which may differ from the decision actor;
- *subject content identity*, *scope* and *purpose* (V4-REC-05; V4-HI-32);
- *evidence reference*: the act's own evidence, linked and not copied (V4-HI-71);
- *lapse state* relative to current content (V4-HI-32).

A record whose decision actor is a person but has no evidence reference is not
a faithful recording. A record that names the recorder as the decision actor
of an A4–A7 act is not a faithful recording either.

---

## 3. Settled distinctions S1–S12

Each distinction below was checked against the cited bytes at repo 6e18505e3.

| ID | Settled distinction | Citation | Consequence for consumers |
|---|---|---|---|
| S1 | Graduated autonomy per kind of operation: the agent may propose for acceptance or apply directly within a scope the person sets, with origin marks, undo and later checking. | PRD V4-AUT-01; HI V4-HI-22, V4-HI-40; D-04 | Treatment is resolved per operation class and grant (§4). Direct application always carries origin, undo route and later-check route. |
| S2 | Every result's standing is visible (current/historical, checks passed, known limitations) so the person can judge the validation warranted. | PRD V4-AUT-02; HI V4-HI-12; X-19 | No presentation stronger than the evidence (DEL-04-02). |
| S3 | Agents may prepare checking, acceptance and reliance decisions. They must not represent an actual human act as performed when it was not. Faithfully recording an actually performed act is allowed, with decision actor ≠ recorder. | PRD V4-AUT-03; HI V4-HI-31; d3; SoW REQ-002 | A1/A8 permitted. Fabrication prohibited. A9 keeps actor and recorder separate. |
| S4 | Nothing the agent produces is presented as certified, sealed, approved or code-compliant. Such statements belong to the accountable professional. | PRD V4-AUT-05; X-09 | A7 is never inferred. Standing labels exclude these claims for agent output. |
| S5 | Operation `success` means the operation ran; it never means a person accepted anything. A submitted proposal reports "queued" until the host records acceptance and application. | HI V4-HI-23, V4-HI-25 | A2 and A5 are separate. Success-only paths never create A5. |
| S6 | A human act binds to the content, scope and purpose it concerns and lapses visibly when that content changes. | HI V4-HI-32; PRD V4-REC-05; X-20 | DEL-04-03 owns the lapse comparison. DEL-04-02 and DEL-05-02 display it. |
| S7 | Acceptance of a proposed edit is not engineering approval. The interface says "accept", never "approve", for proposals. | HI V4-HI-33 | Label rule in §7. |
| S8 | Hosts choose conservative defaults for consequential operations. For SWB model changes the default is proposal with row, multi-row or whole-batch acceptance, and the person may widen it. | HI V4-HI-41 | §5 example. Host adoption is external (DEP-001). |
| S9 | A workflow's declared checkpoints override autonomy: at a checkpoint the run waits for the person's act. | HI V4-HI-42; PRD V4-WF-05 | Step 2 of the resolution order (§4.3). |
| S10 | External agents act through the same catalog, validation, autonomy settings and reserved acts. They cannot perform an act reserved by the applicable policy. External access is off unless the person enables it, and it is local to the machine. | HI V4-HI-50, V4-HI-51, V4-HI-52 | DEL-03-03 and DEL-09-09 cases. The historical SWBPIPE no-external-apply design is scoped context only (V4-HI-51). |
| S11 | Agent examination of engineering work is its own useful activity and need not modify the model. | d3 ("Preserve the meanings through the UI"); V4-EXM-21 | A3 is distinct from A4. |
| S12 | Shared access does not transfer decision rights. | PRD §4.5 lead sentence; OD-05 | Parity of reads and operations never implies an agent's right to perform A4–A7. |

**Not settled.** Two sub-questions remain open: the exact always-reserved list
and operation-level allocation (OI-001), and the classifier-based routine
permission treatment (OI-002). D-04 states that the owner's words "are not
answered" on these sub-questions. PRD V4-AUT-03/-04, V4-HI-30/-31 and d3
restate them as open. d3's treatment table is "a proposed interpretation, not
an accepted new policy", and this contract does not adopt it as policy. The
original-seed V4-HI-30 "at least" list
(`…/APP-V4-BASIS-20260926/original-seed/HOST_INTEGRATION.md` lines 90–92) is
historical and **not ruled** (AX-001). The pending HELP_HUMAN recommendations
in `AgentRuns/APP-V4-FIRST-INCREMENT-20260928/DECISIONS_PENDING.md` D2/D3 have
no recorded owner answer, and this contract does not rely on them.

---

## 4. Autonomy-grant model

### 4.1 Inputs (semantic)

| Input | Meaning | Supplier |
|---|---|---|
| *operation identity* and *operation class* | Which catalog operation, and the host-named class it belongs to | DEL-03-01 catalog (V4-HI-01/02). The host names the classes (V4-HI-30). |
| *catalog human-act class* | One of: **none**; **may apply within granted autonomy**; **proposal only**; **reserved to the person**; or `UNRESOLVED{OI-001}` | Vocabulary SETTLED by V4-HI-02. Assignment of concrete operations is a policy value with a decision basis (§6). |
| *consequence statement* | Why the class sits where it does: effect, reversibility, available examination, intended delegation | Dimensions from d3 ("Reconsider when…"). No scale is selected. The concrete vocabulary is `UNRESOLVED` (U-06). |
| *person grant* | For each operation class: **direct** or **propose**, within a person-set scope | The person (A12), displayed by DEL-04-02 and recorded with the run by DEL-04-03 |
| *host default* | The conservative default treatment for a consequential class | Host (V4-HI-41). The SWB model-change default is accepted (§5). |
| *checkpoint state* | Whether the run is at a declared checkpoint and which act kind it requires | DEL-02-01 declaration; DEL-02-03 and DEL-05-01 execution |
| *actor* | The person, the embedded agent or an external agent | Host / loop |
| *external enablement* | Whether the person has enabled external access on this machine | The person (A13); the host |

### 4.2 Treatments (outputs)

| Treatment | Meaning |
|---|---|
| **execute** | Run with no associated human act (for example a read or an examination). The result carries its standing (S2). |
| **apply directly** | The agent applies through the host's one route, with origin, relied-on basis, undo route and later-check route (V4-HI-20…22). |
| **propose** | The V4-HI-23 lifecycle. Queued until acceptance and application are recorded (S5). |
| **request the person's act** | The agent may only prepare and request (A8). The person performs the act through the host facility. |
| **unavailable** | The operation is not offered, with the same reason the person would see (V4-HI-04, -52) |
| **no policy basis** — `UNRESOLVED{OI-001}` / `UNRESOLVED{OI-002}` | This contract supplies no treatment. Dependent implementation for that concrete operation awaits the decision (REQ-004). A fixture reports AWAITING-DECISION. Such an operation is never counted as permitted or passing. |

### 4.3 Resolution order for an agent actor

The first matching rule applies. Each rule cites its basis.

1. **External actor, access not enabled** → *unavailable*, with reason (S10; V4-HI-52).
2. **At a declared checkpoint** → *request the person's act* for the checkpoint's act kind. This overrides every grant, including a direct grant (S9).
3. **Act kind A4–A7 on any subject** (check, accept, approve, rely) → *request the person's act*. An agent is never the decision actor of these (S3, S4, S12). This is independent of OI-001: OI-001 decides which *operations* are always reserved; it cannot make an agent the performer of a human act.
4. **Catalog class = reserved** → *request the person's act* (S10 for external agents; V4-HI-30/-31). *Which* operations are reserved: `UNRESOLVED{OI-001}`, except that professional reliance is SETTLED as the professional's (S4; V4-HI-30).
5. **Catalog class `UNRESOLVED{OI-001}`, class omitted, or the operation needs a routine-permission treatment that is `UNRESOLVED{OI-002}`** → *no policy basis*. Omission is not permission (REQ-004).
6. **Catalog class = proposal only** → *propose*. No grant can widen it.
7. **Catalog class = may apply within granted autonomy**:
   - person grant = direct, and the operation is inside the person-set scope → *apply directly* (S1);
   - otherwise → *propose*. With no person grant recorded, the host's conservative default applies (S8). If the host has named no default for a consequential class, the result is *no policy basis* (U-07, host-owned, DEP-001) and not *apply directly*.
8. **Catalog class = none** → *execute*. DERIVED caution: V4-HI-02 does not say that "none" implies no effect. Assigning an effectful operation to "none" is a policy value that needs its own decision basis (§6).

For the **person** as actor, the person's operations use the same route and
validation (V4-HI-20). Agent grants do not gate them. The person's acts are
attributed to the person.

### 4.4 Person-set scope

- The grant is set by the person, per operation class, within a scope the
  person sets (V4-AUT-01; V4-HI-40). The scope's dimensions (for example model
  or workspace, object set, run, period) are shown only as examples here. The
  descriptor is a DEL-04-02/DEL-04-03 representation matter (U-08).
- The grant is visible, can change during work, and is recorded with each run
  (V4-HI-40). The treatment recorded for each operation is the one in effect
  when that operation was resolved. DERIVED from "recorded with each run" and
  S5: a later change never re-labels an earlier operation.
- An agent-originated grant change is a request (A8) until the person sets it.
  DEL-04-02 shows it as requested and not established (DEL-04-02 REQ-001).
- The effect of a mid-run narrowing on proposals already queued, or on a
  direct application already in flight, is `UNRESOLVED` (U-09; DEL-04-02 with
  DEL-03-02).

### 4.5 Widening rule

The person may widen granted autonomy (S8; SOW-182). Widening is bounded.
A widened grant:

| # | Cannot | Basis |
|---|---|---|
| W-a | make an agent the decision actor of A4–A7, or fabricate any human act | S3, S4 |
| W-b | bypass a declared checkpoint | S9 |
| W-c | authorize an act or operation reserved by the adopted policy, for any agent, embedded or external | S10; REQ-006 |
| W-d | convert a **proposal only** class to direct | V4-HI-02 class meaning |
| W-e | turn a class that is `UNRESOLVED{OI-001}` or `UNRESOLVED{OI-002}` into a permission. The person's widening is recorded, but its effect for that operation remains *no policy basis* | REQ-004 |
| W-f | enable external access implicitly. Enabling is its own act (A13) | V4-HI-52 |
| W-g | confer professional standing on results produced under it | S4 |
| W-h | drop the origin, undo and later-check obligations of direct application | S1; V4-HI-22 |

Narrowing is always available to the person (V4-HI-40 "can change during
work"). Its in-flight effect is U-09.

---

## 5. SWB default — accepted default, labeled

> **ACCEPTED DEFAULT** (V4-HI-41, via B-ACCEPT). Host adoption and
> enforcement belong to the external SWBPIPE owner and are **not evidenced**
> (DEP-001: owner reports building before agent-action integration). The
> concrete first operation is `UNRESOLVED{OI-021}`.

Policy-class record for this default (semantic elements, §6):

| Element | Value |
|---|---|
| Class | SWB model changes (host-named class; concrete operations listed by the host catalog) |
| Catalog human-act class | may apply within granted autonomy |
| Default treatment | propose |
| Acceptance granularity offered | row-by-row; multi-row selection; whole batch |
| Widening | Permitted by the person, bounded by §4.5 |
| Consequence statement | Consequential host model change (V4-HI-41) |
| Decision basis | V4-HI-41 ("following the owner's direction of 2026-09-17"), accepted in composite APP-V4-BASIS-20260926 |
| Decision standing | accepted default. Receiving host adoption is unevidenced (V4-HI-51 last sentence; DEP-001). |
| Reserved sub-acts within the class | `UNRESOLVED{OI-001}` |
| First concrete operation and its permitted autonomy | `UNRESOLVED{OI-021}` |
| Consumers | DEL-03-01, DEL-03-02, DEL-04-02, DEL-05-02, DEL-09-09 (§8) |

Semantics of the acceptance granularity:

- Row, multi-row or whole-batch acceptance is one or more A5 acts by the
  person. Each accepted proposal row is bound to its own proposed content (S6).
- Whole-batch acceptance accepts each included row's proposed content. It is
  not a checked mark (A4) or an approval (A6) of any row.
- Whether a batch acceptance is recorded as one act covering many subjects or
  as several acts is a DEL-04-03 representation choice (U-10). Both must keep
  per-row subject identity.
- Acceptance is not application. The host's route then applies, or refuses a
  stale proposal with its reason (V4-HI-23). The receipt belongs to A2.

**Fixture subject (invented material, not real engineering data).** Model
`FX-MODEL-A`, an invented three-run piping model. The agent proposes adding
support `FX-S-101` at node 40 and changing run `FX-R-3` elevation from 3.20 m
to 3.35 m, as two proposal rows. With no widening, both are *propose*. The
engineer accepts row 1 and rejects row 2 (A5, A10). The host applies row 1
and issues receipt `FX-RCPT-1`. The run record shows A1 (agent), A5
(engineer; recorder = agent or host), A2 (host route; receipt referenced).
It shows no A4, A6 or A7.

---

## 6. Policy-class record meaning (OUT-002)

Each concrete policy value carried to consumers is a **policy-class record**
with these semantic elements:

| Element | Meaning |
|---|---|
| *policy revision identity* | Identifies the policy content consumers cite. The algorithm is unselected. |
| *class identity* | The host-named operation class (V4-HI-30) |
| *covered operations* | Catalog operation identities and versions (DEL-03-01) |
| *consequence statement* | The rationale in d3 dimensions (§4.1) |
| *catalog human-act class* | none / may apply within granted autonomy / proposal only / reserved / `UNRESOLVED{OI-001}` |
| *default treatment* | For "may apply" classes: the conservative default (S8) |
| *widenable* | yes (bounded by §4.5) / no |
| *acceptance granularity* | Where proposals apply (for example row, multi-row, batch) |
| *actors covered* | The person, the embedded agent and external agents. SETTLED that external agents get the same settings and reserved acts (V4-HI-50). |
| ***decision basis*** | Reference to the accepted requirement or the recorded decision act that fixes this value: its identity, decision actor and date. For an unresolved value: the OI, its owner and its point of need. |
| *decision standing* | **settled-by-basis** \| **accepted default (host adoption unevidenced)** \| **adopted decision** \| `UNRESOLVED{OI-nnn}` |
| *consumers* | The deliverables that act on the value (§8) |

Rules:

- No value is carried without a decision basis. A value whose basis is a
  fixture expectation, a historical draft (for example the original-seed
  "at least" list or the V4-AUT-04 prior drafting default) or a pending
  recommendation has **no** decision basis (AC-007).
- An `UNRESOLVED` value names its OI, owner and point of need. It is never
  rendered as a permission, default or pass.
- **Adopted decision** is currently empty. No OI-001/OI-002/OI-021 decision is
  recorded at repo 6e18505e3.

---

## 7. Label rule ("accept", not "approve")

- Every proposal decision control, status and record label uses **accept**,
  **reject** and **withdraw**. None uses "approve" or "approval" (S7; REQ-005).
- The word **approve** is used only for A6, a separately evidenced engineering
  approval.
- Terms that collide with "approve" (finding F-2):
  - Harness tool-permission requests are called "approvals" in PRD V4-EXE-02,
    V4-REP-01 and V4-EXM-11. They are A14 (routine tool permission), not A5 or
    A6. Their App/host treatment is `UNRESOLVED{OI-002}`. Consumers should not
    display a proposal decision with the same control or wording as a tool
    permission request.
  - Domains "design candidate for human approval" (V4-HI-65, later increment)
    is its own act with distinct identity. It is not A5, and it is outside this
    first increment.
- Standing labels for agent output never include "certified", "sealed",
  "approved" or "code-compliant" (S4; X-09).

---

## 8. Value → decision → consumer map

### 8.1 Values carried now

| # | Value | Decision basis (standing) | Consumers and what each does with it |
|---|---|---|---|
| V-01 | Act kinds A1–A14 and their actor/subject/evidence meanings | S3, S5, S7, S11; d3; SoW REQ-002 (settled-by-basis; names proposed here) | **DEL-04-03**: record act kind by name, decision actor ≠ recorder. **DEL-02-01**: checkpoints name the required act kind. **DEL-04-02**, **DEL-05-02**: display. **DEL-01-04**: UI labels and attribution. |
| V-02 | Catalog human-act class vocabulary (none / may apply / proposal only / reserved) | V4-HI-02 (settled-by-basis) | **DEL-03-01**: entry element. **DEL-03-02**: branch between direct and proposal lifecycle. **DEL-03-03**: carry to the external receiver. |
| V-03 | Resolution order §4.3 and widening bounds §4.5 | S1, S8, S9, S10, S12 (settled-by-basis; order proposed here) | **DEL-03-02**: direct-autonomy branch. **DEL-05-01**: loop dispatch and checkpoint events. **DEL-02-03**: checkpoint hold. **DEL-04-02**: effective vs requested display. |
| V-04 | Grant is person-set per class, visible, changeable during work, recorded per run | V4-AUT-01; V4-HI-40 (settled-by-basis) | **DEL-04-02**: show and change. **DEL-04-03**: record with run. **DEL-05-01**: consult per operation. |
| V-05 | Success ≠ acceptance; queued until recorded | V4-HI-23, -25 (settled-by-basis) | **DEL-03-02**: outcome taxonomy. **DEL-05-01**: event meaning. **DEL-05-02**: queue display. **DEL-04-03**: record outcomes including `unknown`. **DEL-01-04**: outcome presentation. |
| V-06 | Content binding and visible lapse | V4-HI-32; V4-REC-05 (settled-by-basis) | **DEL-04-03**: lapse comparison. **DEL-04-02**: standing `lapsed`. **DEL-05-02**: lapse links. |
| V-07 | "accept" wording for proposals | V4-HI-33 (settled-by-basis) | **DEL-05-02**, **DEL-01-04**, **DEL-04-02**: labels. **DEL-03-02**: lifecycle names. **DEL-04-03**: act-kind name A5. |
| V-08 | No professional standing from agent output | V4-AUT-05 (settled-by-basis) | **DEL-04-02**: standing ceiling. **DEL-05-02**, **DEL-01-04**: labels. **DEL-09-09**: examination criterion. |
| V-09 | Checkpoints override autonomy | V4-HI-42; V4-WF-05 (settled-by-basis) | **DEL-02-01**: declaration. **DEL-02-03**: execution hold. **DEL-05-01**: checkpoint subject. |
| V-10 | External: same settings and reserved acts; no reserved act; access off by default and machine-local | V4-HI-50…52 (settled-by-basis) | **DEL-03-03**: enablement states and refusal. **DEL-09-09**: external-route cases. |
| V-11 | SWB model change: propose by default; row/multi-row/batch accept; widenable | V4-HI-41 (accepted default; host adoption unevidenced, DEP-001) | **DEL-03-01**: class and default. **DEL-03-02**: acceptance granularity. **DEL-04-02**: default display. **DEL-05-02**: row, multi-row and batch controls. **DEL-09-09**: joined witness. |
| V-12 | Agent examination is distinct from human checking | d3; V4-EXM-21 (settled-by-basis) | **DEL-05-02**: findings by reference. **DEL-04-02**: standing. **DEL-04-03**: not recorded as A4. |
| V-13 | Faithful recording with decision actor ≠ recorder | SoW REQ-002; d3; V4-HI-31 (settled-by-basis) | **DEL-04-03**: record elements (§2.4). **DEL-05-02**: host-captured acts. **DEL-09-09**: evidence of the engineer's actual acceptance. |

### 8.2 Values not carried (open)

| # | Value | Standing | Consumers that must hold |
|---|---|---|---|
| V-20 | Always-reserved operations and act kinds, by concrete operation and consequence; reject (A10) and grant change (A12) membership; recorder allocation (A9) | `UNRESOLVED{OI-001}` | DEL-03-01 (class assignment), DEL-03-02, DEL-03-03, DEL-04-02, DEL-05-02, DEL-09-09, DEL-02-01 (checkpoint examples only where the act is settled) |
| V-21 | Routine tool-permission treatment (App and host), including classifier-based modes; relation of A14 to run and act records | `UNRESOLVED{OI-002}` | DEL-01-04, DEL-01-02, DEL-05-01, DEL-03-03, DEL-04-03 |
| V-22 | First connected operation, its permitted autonomy and candidate environment | `UNRESOLVED{OI-021}` | DEL-03-01, DEL-09-09, DEL-05-01, DEL-05-02 |
| V-23 | Consequence vocabulary; host defaults for consequential classes other than SWB model change | U-06, U-07 (host policy owner, DEP-001) | DEL-03-01, DEL-04-02 |

### 8.3 Other declared consumers (not mapped in detail in v0.1)

These deliverables also declare DEL-04-01 upstream in their own registers:
DEL-01-02 (DEP-01-02-021), DEL-02-02 (DEP-02-02-016), DEL-03-04
(DEP-03-04-011), DEL-06-02 (DEP-06-02-009), DEL-09-02 (DEP-09-02-018),
DEL-09-05 (DEP-09-05-009), DEL-09-12 (DEP-09-12-011) and DEL-10-03
(DEP-10-03-013). Each consumes V-01…V-13 as applicable and holds on
V-20…V-23. DEL-09-11 receives records through DEL-04-03, not directly. See
finding F-1.

---

## 9. Boundary accounting (REQ-007, VER-008)

| Act or production | Owner | This contract's part |
|---|---|---|
| Deciding OI-001, OI-002 (and OI-021's autonomy) | Owner with App/SWB contract owners (CLM-004; OI-021 with the outside SWB session) | State the questions (§10). Hold dependent values. |
| Performing A4–A7, A10, A12, A13, A14 | The person, or the accountable professional for A7 | None. Define meanings and fixtures only. |
| Offering, recording and presenting human acts in the host; validation/application route; receipts; origin/undo; host catalog; host enforcement | External SWBPIPE owner (CLM-003; DEP-001) | Requirements and receiving cases. No host evidence claimed. |
| Checkpoint declarations | DEL-02-01 | Supply act-kind names (V-01, V-09) |
| Checkpoint execution and compatibility | DEL-02-03 | Supply hold rule (V-03, V-09) |
| Catalog/read-basis schema, including the class element | DEL-03-01 | Supply vocabulary and adopted values (V-02, V-11) |
| Proposal lifecycle and outcome contract | DEL-03-02 | Supply branch and wording meaning (V-03, V-05, V-07) |
| External receiving adapter | DEL-03-03 | Supply V-10 |
| Autonomy/standing receiving UI | DEL-04-02 | Supply V-03, V-04, V-08 |
| Human-act/run record format, reader/writer, lapse | DEL-04-03 | Supply V-01, V-06, V-13 |
| Loop and panel receiving contracts | DEL-05-01, DEL-05-02 | Supply V-03, V-05, V-07, V-09 |
| Certification, sealing, professional approval, code compliance | Accountable professional (CLM-005) | Prohibit inference (S4) |
| Placement of any shared policy representation | App/shared owners (OI-013, OI-014) | Representation-neutral here |

The existence of this contract claims no host implementation, adoption,
enforcement, external evidence, or performance of any person's act.

---

## 10. Owner questions (for OI-001, OI-002, OI-021 — not decided here)

**OI-001 — always-reserved acts.** Owner with App/SWB contract owners. Point of
need: before operation-policy production contracts.

1. For the first connected operation (once OI-021 fixes it), which operations
   in its class are **reserved to the person** regardless of any grant, and
   which are **proposal only**?
2. Is there an App/shared minimum reserved list that every host inherits, with
   hosts adding their own (V4-HI-30 "a host names…")? Or is the list entirely
   host-named per operation?
3. Is changing the autonomy grant (A12) reserved to the person as an operation
   class, beyond the settled fact that the effective grant is person-set?
4. Is rejecting a proposal (A10) reserved to the person, or may an agent
   reject, for example its own superseded proposal, as distinct from withdrawal
   (A11)?
5. For each human act kind A4–A7, may an agent act as **recorder** (A9) of the
   person's actually performed act, or must the host facility record it?
6. Which consequence dimensions (effect, reversibility, available examination,
   intended delegation, or others) define classes, and who names the
   vocabulary: the App/shared contract or each host?
7. Should the settled point that professional reliance remains with the human
   (V4-HI-30, V4-AUT-05) appear as an explicit **reserved** catalog class on
   every host that exposes a reliance-expressing operation?

**OI-002 — classifier-based routine permissions.** Owner with App/SWB contract
owners. Point of need: before permission-policy implementation.

1. In the App, what treatment do harness routine tool-permission modes get,
   including any classifier-based mode? The prior drafting default "user
   setting in the App" is an option, not policy (V4-AUT-04).
2. In hosts, is any classifier-based routine permission mode allowed, and for
   which catalog classes, if any?
3. When a tool call both needs a routine permission (A14) and performs a
   catalog operation with a human-act class, is it confirmed that both apply
   independently, with neither satisfying the other?
4. Are A14 settlements recorded only as run-record operation events, or may
   they appear in the human-act record at all?

**OI-021 — first connected activity.** Owner via the outside SWB session and
the App/shared owner.

1. Which concrete SWB model-change operation is first, and what autonomy
   (beyond the V4-HI-41 default) is permitted for it in the candidate
   environment?

---

## 11. Fixture catalogue (OUT-003) — designed, not run

All subjects are invented fixture material (`FX-` prefix). Expected results
are contract expectations. They decide no OI and establish no human act.
AWAITING-DECISION marks a case that cannot pass until its OI is ruled.
Host-dependent results need DEP-001 evidence.

| ID | Group | Case | Expected result | VER |
|---|---|---|---|---|
| FX-01 | Fabrication | The agent drafts proposal FX-P-1. The run record shows A5 "accepted by FX-Engineer-E" with no host acceptance evidence. | Non-conformant: fabricated attribution | VER-002, -004 |
| FX-02 | Fabrication | Agent examination findings on row FX-R-12 are recorded as A4 by the engineer | Non-conformant. A3 stays A3. | VER-002 |
| FX-03 | Fabrication | The agent writes A6 "approved" for its own design output | Non-conformant (S3, S4) | VER-002, -003 |
| FX-04 | Success-only | Submitting FX-P-1 returns `success`. The UI or record shows "accepted". | Non-conformant. Must show "queued" (S5). | VER-002 |
| FX-05 | Success-only | Receipt FX-RCPT-1 is presented as acceptance, checking or approval | Non-conformant. The receipt supports A2 only. | VER-002, -003 |
| FX-06 | Success-only | Acceptance recorded; application refused as stale after an intervening edit | Conformant only if A5 is kept, A2 shows refusal with reason, and no application is claimed | VER-002 |
| FX-07 | Independent act | The engineer edits FX-R-12 directly (no proposal), then marks it checked | Conformant A4. Absence of A5 does not invalidate it. | VER-002 |
| FX-08 | Independent act | Row accepted (A5), later checked by a second person (A4) | Both retained with their own actors. Neither implies the other. | VER-002 |
| FX-09 | Faithful recording | The engineer accepts rows 1–3 in the host view. The agent records A5 with decision actor = engineer, recorder = agent, evidence reference = host acceptance record, and per-row content identity. | Conformant as a record shape. Actor ≠ recorder is preserved. No recording permission is inferred (`UNRESOLVED{OI-001}` Q5). A candidate-bound pass needs actual act evidence (DEP-04-01-021). | VER-002 |
| FX-10 | Faithful recording | Same as FX-09 but decision actor = agent, or no evidence reference | Non-conformant | VER-002 |
| FX-11 | "accept" wording | Proposal controls "Accept", "Accept selected rows", "Accept all", "Reject" | Conformant | VER-005 |
| FX-12 | "accept" wording | A proposal control or status reads "Approve" / "Approved" | Non-conformant | VER-005 |
| FX-13 | "accept" wording | A separately evidenced A6 on engineering content is labeled "approve" | Conformant. It is not a proposal. | VER-005 |
| FX-14 | Standing | Agent result displayed "code-compliant" or "certified" | Non-conformant (S4) | VER-003 |
| FX-15 | Standing | A professional's A7 statement on result FX-RES-2, attributed to FX-Professional-P | Conformant. Not inferred from A2–A6. | VER-003 |
| FX-16 | Unresolved ≠ permission | Catalog entry FX-OP-renumber has class `UNRESOLVED{OI-001}`. The person grants direct for its class. The agent applies. | No pass. Reported AWAITING-DECISION{OI-001}. Direct application not counted as permitted. | VER-004, -007, -009 |
| FX-17 | Unresolved ≠ permission | Catalog entry FX-OP-annotate omits the class element | Same as FX-16. Omission is not permission. | VER-004, -007 |
| FX-18 | Unresolved ≠ permission | A tool call needs a routine permission, and a classifier mode auto-grants it | The contract gives no treatment: AWAITING-DECISION{OI-002}. The settlement is never recorded as A4–A7. | VER-004 |
| FX-19 | Default | SWB model change on FX-MODEL-A with no widening | Propose. Row, multi-row and batch acceptance offered (S8). Host conformance needs DEP-001. | VER-006 |
| FX-20 | Widened | The person widens FX-class "support add" to direct, scoped to FX-MODEL-A | The agent applies with origin, basis, undo route and later-check route. The run record shows the grant in effect. Host claims need DEP-001. | VER-001, -006 |
| FX-21 | Widening bound | Grant direct; the run reaches checkpoint FX-CP-1 requiring A4 before solve | Run waits. The agent may request only (S9). | VER-001, -006 |
| FX-22 | Widening bound | Widest grant; the agent attempts A7 on FX-RES-2 | Refused. No attribution to the person (S4, S10). | VER-004, -006 |
| FX-23 | Widening bound | The agent requests a widening for its own class | Shown as requested and not established. Not effective. Reserved status `UNRESOLVED{OI-001}` Q3. | VER-001 |
| FX-24 | External | External access not enabled | Unavailable, with reason (S10) | VER-004 |
| FX-25 | External | Enabled. The external agent submits a proposal. The engineer accepts in the host. | Same lifecycle and settings as embedded. A5 attributed to the engineer. | VER-004 |
| FX-26 | Examination | The agent checks the engineer's edits to FX-R-12 | Findings by reference. No table change. No A4 (S11). | VER-002 |
| FX-27 | Lapse | A4 on FX-R-12 with content c1; the row changes to c2 | A4 shown lapsed for c2, retaining its c1 identity (S6) | VER-002 |
| FX-28 | Boundary | The contract document asserts host enforcement without DEP-001 evidence | Non-conformant (REQ-007) | VER-008 |

---

## 12. Findings (reported, scope unchanged)

- **F-1** The consumer registers are asymmetric. This deliverable's
  `Dependencies.csv` (DEP-04-01-012…016) and SoW CLM-002 name five downstream
  consumers. Eighteen deliverables have an ACTIVE upstream row targeting
  DEL-04-01 in their own registers (§8). DEL-04-03 refers to it through an
  OI constraint row. The receiver lists may need reconciling at V1 or by
  WORKING_ITEMS.
- **F-2** The word "approval" is overloaded across the basis. Harness
  tool-permission "approvals" (V4-EXE-02, V4-REP-01, V4-EXM-11), engineering
  approval (V4-HI-30/33) and Domains design-candidate approval (V4-HI-65) are
  different subjects. REQ-005 governs proposals only. DEL-01-04 and DEL-05-02
  need the §7 distinction.
- **F-3** V4-HI-23 includes `rejected` and `withdrawn`, but the SoW taxonomy
  (REQ-002) does not name reject or withdraw acts. They are added here as A10
  and A11, with their reserved status left open (OI-001 Q4).
- **F-4** The basis requires policy "by operation and consequence" but supplies
  no consequence vocabulary. Its owner is unclear: DEL-04-01, the host policy
  owner, or OI-001 (U-06).
- **F-5** OUT-002 names an "adopted policy-class representation". At v0.1 its
  adopted-decision set is empty. Only settled-by-basis values and the
  V4-HI-41 accepted default can be carried.
- **F-6** PRD OQ-02 corresponds to decomposition OI-001 and OI-002 together.
  Consumers citing OQ-02 should cite the specific OI.

---

## UNRESOLVED

| Item | Owner | Point of need | Effect on this definition |
|---|---|---|---|
| U-01 `UNRESOLVED{OI-001}` always-reserved operations and act kinds (§10) | Owner with App/SWB contract owners | Before operation-policy production contracts | Treatment step 4 has no concrete members apart from professional reliance. V-20 is not carried. FX-16/17/23 are AWAITING-DECISION. |
| U-02 `UNRESOLVED{OI-002}` routine tool-permission treatment, App and host | Owner with App/SWB contract owners | Before permission-policy implementation | A14 is defined only negatively. V-21 is not carried. FX-18 is AWAITING-DECISION. |
| U-03 `UNRESOLVED{OI-021}` first operation and its permitted autonomy | Owner via the outside SWB session and the App/shared owner | Before connected-activity SoW and execution | §5 cannot name a concrete operation. V-22 is not carried. |
| U-04 Host adoption and enforcement evidence for V4-HI-41/-50…52 and host act facilities | External SWBPIPE owner (DEP-001) | Before any host enforcement or connected-behavior claim | Host rows are receiving requirements only. Host-dependent fixtures have no result. |
| U-05 Recorded person grant; actual performed-act evidence | The person (DEP-04-01-020, -021) | VER-001 and the VER-002 positive case | VER-001 comparison and the FX-09 candidate-bound pass cannot run |
| U-06 Consequence vocabulary and scale | DEL-04-01 with host policy owner; owner if OI-001 Q6 decides it | Before class assignment in DEL-03-01 | Consequence is text with d3 dimensions only |
| U-07 Conservative defaults for consequential classes other than SWB model change | Host policy owner (V4-HI-41; DEP-001) | Before those classes are cataloged | Step 7 without a default yields no policy basis |
| U-08 Grant scope descriptor dimensions | DEL-04-02 with DEL-04-03 | M3 settings-in / record-out exchange | Scope examples are illustrative only |
| U-09 In-flight effect of a mid-run grant narrowing | DEL-04-02 with DEL-03-02 | Before during-work change is implemented | Only "effective at resolution time" is defined |
| U-10 Batch acceptance as one act or many | DEL-04-03 | Record format v0.2 | Per-row subject identity is required either way |
| U-11 Placement of the policy representation (shared type, library or per-host) | App/shared owners (OI-013, OI-014) | Before production allocation | Representation-neutral |

## Verification cases

Designed, not run. Each binds to this file's revision when executed.

| Case | Serves | Procedure | Expected result |
|---|---|---|---|
| VC-001 | VER-001 / AC-001 | Compare §4 and §6 with V4-AUT-01 and V4-HI-22/40/42. Run FX-20, -21, -23 against a recorded person grant (U-05). Trace origin, undo and later-check obligations to DEL-03-02, DEL-04-02 and the host. | Every direct treatment traces to a person-set grant. Checkpoints override. Obligations named per consumer. Missing grant evidence recorded as missing. |
| VC-002 | VER-002 / AC-002 | Exercise FX-01…10, -26, -27. Inspect actor, subject and evidence per act kind. | Negatives non-conformant. FX-07/08 conformant without A5. FX-09 keeps actor ≠ recorder. The candidate-bound FX-09 pass waits for U-05. |
| VC-003 | VER-003 / AC-003 | Exercise FX-03, -05, -14, -15, -22 against V4-AUT-05 | No certification, sealing, approval or code-compliance claim for agent output. A7 attributed only to its professional. |
| VC-004 | VER-004 / AC-004 | For each adopted reserved case, compare with its decision basis and inspect host evidence. For each unruled case, check the OI, owner and point of need. Exercise FX-16…18, -22, -24, -25. | Currently only professional reliance is settled. All others report `UNRESOLVED{OI-001/002}`, not passes. Host enforcement is not asserted without DEP-001. |
| VC-005 | VER-005 / AC-005 | Inventory proposal-decision wording in this file, the §5 example and FX-11…13 | "accept" everywhere for proposals. "approve" only for A6. Collision F-2 recorded. |
| VC-006 | VER-006 / AC-006 | Exercise FX-19…22 and compare with V4-HI-41/42/51 | Default is propose, with row, multi-row and batch acceptance. Widening is bounded by W-a…h. Results labeled local contract evidence vs host evidence. |
| VC-007 | VER-007 / AC-007 | Trace V-01…V-13 to their decision bases, and V-20…V-23 to their OIs and owners | Every carried value has a basis. No inferred reserved list or classifier value. |
| VC-008 | VER-008 / AC-008 | Compare §9 with SoW CLM-002…005 and REQ-007. Run FX-28. | Each excluded act is assigned to its owner. No host, adoption or act claim. |
| VC-009 | VER-009 / AC-009 | Reconcile FX-01…28 with REQ-002…006 and the matrix. When a candidate exists, run the applicable fixtures and retain fixture IDs, candidate identity, results and limits. | Coverage complete. AWAITING-DECISION and missing host evidence reported separately from passes. No results exist at v0.1. |
