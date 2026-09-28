# Autonomy and Standing Exchange
- Contribution: DEL-04-02/AS-v0.1
- Status: DRAFT DEFINITION — proposed, unsupplied, not implemented, not accepted
- Serves: OUT-002 (receiving-interface contract content); OUT-001 and OUT-003 (component behaviour and fixture design only — no component or fixture exists); REQ-001…REQ-007; AC-001…AC-007 via designed VER-001…VER-007
- Basis: repo 6e18505e3; ScopeOfWork.md sha256 23a28caabd61da20dc2efed722f7e487856ef4488ab4f3454be4ed3249725e21; `P/docs/PRD.md` §4.3 V4-EXE-02/03, §4.5 V4-AUT-01…05, §4.6 V4-PM-06, §4.7 V4-REC-01…05; `P/docs/HOST_INTEGRATION.md` §1, V4-HI-11/12, V4-HI-21…25, V4-HI-30…33, V4-HI-40…42, V4-HI-50…52, V4-HI-70/71, §11; `P/docs/ARCHITECTURE.md` §4, V4-ARC-20; `P/docs/EXAMINATION.md` V4-EXM-21/22; `P/docs/OPERATING_METHOD.md` V4-OPS-30…32; `DECISION_BRIEF.html` d2, d3; `OWNER_DIRECTIONS.md` J, O; `SCC-CASE-002/Case_Datasheet.md` M1 (DEL-04-03 and M1-P rows), M3 (both rows); `_Decomposition/Open_Issues.csv` OI-001/002/013/014/021; `External_Dependencies.csv` DEP-001
- Consumed inputs: DEL-04-03/RS-v0.1 (drafted concurrently by the same W2 executor; unreviewed — its §8 exchange is restated in §6 here). DEL-04-01 (grant model, act kinds, act classes), DEL-03-02 (direct-autonomy branch, outcomes, origin) and DEL-03-01 (standing, read basis) referenced by accepted meaning only, to be reconciled at V1.
- Receivers: CASE-002 M3 — DEL-04-03 (OUT-001/002; REQ-002; VER-001) receives settings-in; DEL-04-02 itself compares under OUT-003; REQ-002; VER-002. Dependencies.csv — DEP-04-02-009 (DEL-04-03 downstream). Host builder via DEL-03-04 receiving matrix (autonomy and origin/undo rows) and the external SWBPIPE owner through human relay (DEP-04-02-010) — as questions, not assignments.

## 0. Reading this definition

- Element and state names are **semantic, not wire names**. No field
  spelling, type, transport, persistence, placement, layout or timing
  threshold is selected (SoW REQ-006; OI-013; OI-014).
- Act kinds use accepted-basis names: **propose**, **apply**, **examine**,
  **mark checked**, **accept an edit**, **approve**, **rely**, and **faithful
  recording** where actor ≠ recorder — to be reconciled with DEL-04-01 v0.1 at
  V1. Act-class values (none / may apply / proposal only / reserved) are
  `UNRESOLVED{OI-001}`.
- Examples use the invented model `FX-PIPE-01` and placeholder operations
  (`op:add-support`, `op:adjust-run`, `op:set-label`) pending OI-021; they are
  **fixture subjects**.

## 1. Settled distinctions relied on

| # | Settled distinction | Citation |
|---|---|---|
| S1 | The person sets, per class of operation, direct application or proposal; the setting is visible, can change during work and is recorded with each run | V4-HI-40; V4-AUT-01 |
| S2 | Conservative defaults for consequential operations; SWB model changes default to proposal with row / multi-row / whole-batch acceptance; the person may widen | V4-HI-41 (accepted default) |
| S3 | Declared workflow checkpoints override autonomy: the run waits for the person's act | V4-HI-42 |
| S4 | Direct application is marked with origin, can be undone and can be checked later | V4-HI-22; V4-AUT-01 |
| S5 | `success` means it ran; a submitted proposal is "queued" until the host records acceptance and application | V4-HI-25 |
| S6 | Results carry standing — current/historical, checks passed, known limitations — and are not presented with more confidence than the host gives | V4-HI-12; V4-AUT-02 |
| S7 | A human act binds to content and lapses visibly when that content changes | V4-HI-32 |
| S8 | Proposal decisions say "accept", never "approve"; accepting an edit is not engineering approval | V4-HI-33 |
| S9 | No fabricated human act; faithful recording of an actually performed act is permitted | V4-HI-31; d3 |
| S10 | Propose, apply, examine, mark checked, accept an edit, approve, rely are distinct; no universal acceptance-first chain | d3; V4-AUT-03 |
| S11 | Nothing agent-produced is shown as certified, sealed, approved or code-compliant | V4-AUT-05 |
| S12 | Every request is answered or explicitly declined; silence or timeout never implies approval; unobserved outcomes are unknown | V4-EXE-02/03 |

## 2. Grant model received

The grant is received from DEL-04-01; this deliverable renders and exchanges it.

- **Grant** (semantic): for each operation class *k*, a treatment *t(k)* ∈
  {direct, propose}, set by the person, within the policy's allowable range.
- **Policy bound**: classes whose adopted policy is *reserved* or *proposal
  only* cannot be widened to direct by the person's grant; which classes
  those are is `UNRESOLVED{OI-001}`. Until adopted, such a class is displayed
  as **policy unresolved** and receives no direct treatment by default,
  omission or display (DEL-04-01 SoW REQ-004).
- **Checkpoint override** (S3) is not part of the grant; it is a separate
  overlay (§4).
- **Routine tool permission** (e.g. harness approval modes) is a different
  subject from autonomy over host operations and from any human act; its
  treatment is `UNRESOLVED{OI-002}` and it is not shown inside this autonomy
  display as a grant.
- **Accepted default example (SWB, V4-HI-41)**: class "model change" →
  propose; acceptance granularity row / multi-row / whole batch. A person
  widening it is a recorded person's setting act (§5).

## 3. Grant display states

Per class, the display shows one state. Display is derived; the App or host
control is the authority for the current grant; the run record is the
authority for what was recorded (V4-PM-06).

| State | Entry evidence | Shown as | Governs agent route? |
|---|---|---|---|
| **effective** | Control reports the setting in force (App control confirmation, or host confirmation for host-controlled classes) and it matches the person's setting act | Treatment *t(k)* | Yes |
| **requested-unestablished** | Person (or an agent on the person's request) submitted a change; control has not confirmed it in force, or refused it | Requested value beside the still-effective value, labelled "requested — not in force" | No — the prior effective value governs |
| **unconfirmed** | A value is known only from an earlier state (after reconnect, host unreachable, cache), with no current confirmation | Last-known value labelled "unconfirmed" | Treated as the most conservative of last-known and default until confirmed (proposal where uncertain) — proposed rule; host enforcement is the host's |
| **not set** | No setting and no default supplied | "not set" | No direct treatment |
| **policy unresolved** | Class's adopted policy absent `UNRESOLVED{OI-001}` | "policy unresolved" | No direct treatment |

Transitions: not set / effective —(person requests)→ requested-unestablished
—(control confirms)→ effective; —(control refuses, with reason)→ previous
state + refusal shown; —(no answer)→ remains requested-unestablished, never
promoted (S12). Any state —(loss of confirmation)→ unconfirmed —(confirm)→
effective. An operation result (e.g. a direct application that succeeded)
never moves a class to effective or widens it (SoW REQ-001).

## 4. Checkpoint overlay

- A declared checkpoint (DEL-02-01 declaration; DEL-02-03 hold) is shown as
  its own indicator: *not reached* · *waiting for the person's act* ·
  *discharged by act ⟨ref⟩*.
- *Discharged* requires a human-act record reference (DEL-04-03 RS-v0.1 §6)
  of the declared act kind. A direct grant for the class, an operation
  success or an agent examination does not discharge it.
- The autonomy display and checkpoint indicator never merge into a single
  "allowed" signal.

## 5. During-work change sequence

1. Person opens the control for class *k* and chooses a new treatment. The
   person is the setting actor; an agent may *prepare* or *ask for* a change
   but cannot perform it (S9).
2. Display: *k* → requested-unestablished; settings-in (§6) sends the request
   with state requested-unestablished and establishing evidence "person's
   control event ⟨ref⟩".
3. Control (App or host) establishes or refuses. On establish → new settings
   version ⟨set:n+1⟩, state effective, establishing evidence = control
   confirmation ⟨ref⟩; settings-in sends it. On refuse → reason displayed;
   settings-in sends the refusal.
4. From establishment onward the agent route for *k* follows ⟨set:n+1⟩. Which
   version governed an operation already evaluated or in flight is a **host
   fact** the host must report per operation; if not reported, the operation
   entry's governing version is *unconfirmed* (no inference).
5. Narrowing never retroactively changes an applied change's origin or route;
   widening never converts a queued proposal into an applied change or an
   acceptance (S5).

Failure behaviour: control unreachable → unconfirmed; conflicting reports
from App and host control → both shown, class treated as unconfirmed, defect
observation returned; record write fails → display shows "not recorded" for
that settings version (§6 comparison *missing in record*).

## 6. Settings-in / record-out exchange with DEL-04-03 (CASE-002 M3)

Identical to DEL-04-03/RS-v0.1 §8. A data exchange, not an ordering between
human acts and not a second record authority.

**Settings-in (DEL-04-02 → DEL-04-03 writer), per run and per change:** run
identity; settings version identity; per class — treatment (direct / propose /
class unresolved) and display state (effective / requested-unestablished /
unconfirmed); setting actor (the person); establishing evidence reference;
order relative to operation entries; source of control (App or host).

**Record-out (DEL-04-03 reader → DEL-04-02), per run:** record identity and
format version; recorded settings versions with states; each operation
entry's governing settings version, route, outcome and receipt/origin
references; act records with actor, recorder, kind, scope, purpose and lapse
evaluation; evidence limits.

**Comparison (DEL-04-02)** per settings version: displayed vs recorded →
*match* · *mismatch* · *missing in record* · *missing in display*. Mismatch is
shown to the person and returned as a defect observation; neither side is
auto-corrected. A missing or unconfirmed setting is never displayed as
established.

## 7. Abstract host contribution for direct application

Abstract elements the host supplies per directly applied change (host
implements; DEP-001; DEP-04-02-010). Not API fields.

| Element | Meaning | Availability states shown | Never shown as |
|---|---|---|---|
| Origin reference | Host origin mark: agent author type, conversation, workflow run, relied-on basis (V4-HI-21) | supplied · missing | Inferred from the App's own request log |
| Undo route | Host-owned route to undo this change | offered · not offered · unknown | "Available" without a host-supplied route |
| Check route | Host-owned access for later checking of this change/result | offered · not offered · unknown | A performed check |
| Receipt reference | Host receipt for the application | supplied · missing · unresolvable | A copy of the receipt; an acceptance |

**Undo interaction**: person invokes the offered undo route → display
"undo requested" → host outcome: *undone* (host receipt ⟨ref⟩) · *refused*
(reason) · *outcome unknown* (no observation, S12). Only *undone with receipt*
is displayed as completed; the undo is itself a change with its own origin
and is passed to the record (DEL-04-03 R7).

**Check route**: opening it gives access; it does not create a mark checked
act. A human check becomes visible only when a human-act record of kind mark
checked is received (§9).

## 8. Result standing model

Standing is shown as separate facets, each "no stronger than received"
(REQ-004). No facet combination is summarized into a synthesized
"verified/approved" label.

| Facet | Values | Source | Rule |
|---|---|---|---|
| Temporal | **current** · **historical** · unknown | Host standing (V4-HI-12); read basis (DEL-03-01) | Historical results carry the basis they describe |
| Host checks | **checked** (list of host checks passed, each named) · none reported · unknown | Host result standing | "Checked" here means *host checks passed*; it is labelled as such and is distinct from a human mark checked act and from agent examination |
| Limitations | **limited** (host-known limitations listed) · none reported · unknown | Host result standing | Shown verbatim from host; not softened |
| Human acts | act kind + actor + recorder + lapse state per act (**not lapsed** · **lapsed** · partially lapsed · unknown) | DEL-04-03 record-out | Act kinds displayed separately (§9) |
| Agent examination | findings attached by reference | Agent (V4-EXM-21) | Labelled "agent examination", never a human act |
| Evidence completeness | complete as stated · **missing** (named item) · **unknown** (unobserved outcome) | Record-out evidence limits; outcome unknown | Missing/unknown always visible, never blank |
| Origin/route | direct under ⟨set⟩ · proposal ⟨prop⟩ + lifecycle state | DEL-03-02 outcome; record | "Queued" is not "applied"; "applied" is not "accepted" |

The person uses these facets to decide the validation warranted (V4-AUT-02);
the display makes no reliance decision.

## 9. Act-distinction display rules

- DS-1 One label per act kind; "accept" for proposal decisions, never
  "approve" (S8). Engineering approval and professional reliance, when
  evidenced, have their own labels and name their accountable person (S11).
- DS-2 Actor and recorder are both shown when they differ (faithful
  recording).
- DS-3 No act is displayed without a received act record; agent proposal,
  operation success, grant, receipt, examination findings, silence or
  timeout display as what they are (S5, S9, S12).
- DS-4 Absence of an accept record does not mark an independently evidenced
  act (e.g. mark checked on the person's own edit) as invalid (S10).

## 10. Excluded acts and owners (REQ-007)

| Act | Owner |
|---|---|
| Define/carry adopted operation policy | DEL-04-01 |
| Record format, writer/reader, lapse handling | DEL-04-03 |
| Host controls, validation/application, origin marks, undo, receipts, host panel/loop; offering/recording/presenting host acts | Responsible host owner; SWBPIPE outside session |
| Decide OI-001 / OI-002 | Owner with App/SWB contract owners |
| Resolve OI-013 | Shared contract owner with SWB implementation owner |
| Resolve OI-014 | App/shared contract owners |
| Set the autonomy grant; perform any human act | The person |
| Professional reliance; certification, sealing, approval, code-compliance statements | Accountable professional |

## 11. Fixture scenarios (designed; fixture subjects)

| F | Scenario | Expected display / exchange |
|---|---|---|
| F1 | Start run with ⟨set:1⟩: model change → propose (S2 default); `op:set-label` class → policy unresolved | Model change *effective: propose*; set-label *policy unresolved*, no direct route |
| F2 | Mid-run, person widens `op:add-support` class to direct; control confirms ⟨set:2⟩ | requested-unestablished → effective; two settings-in messages; record-out shows both; comparison *match* |
| F3 | Person requests widening; control never answers | Stays requested-unestablished; agent still proposes; settings-in carries unestablished state |
| F4 | Host becomes unreachable after F2 | Class → unconfirmed; conservative route; record shows unconfirmed interval |
| F5 | Record write for ⟨set:2⟩ fails | Comparison *missing in record* surfaced; display does not claim recorded |
| F6 | Checkpoint "review adjusted run" reached while `op:adjust-run` is direct | Checkpoint *waiting*; direct grant does not discharge it; discharge only with act record ref |
| F7 | Direct `op:add-support` applied with origin, undo route, check route, receipt | All four shown as supplied; person undoes → *undone* only on host receipt |
| F8 | Direct change with no undo route and lost acknowledgement | Undo *not offered*/*unknown*; outcome unknown; receipt missing |
| F9 | Results: one current + host checks passed; one historical; one limited; one with mark checked act lapsed after edit; one outcome unknown | Each facet shown as received; lapsed act shown lapsed with original content; unknown visible; no synthesized "verified" |
| F10 | Act distinctions: faithful recording of engineer's mark checked (actor ≠ recorder); agent proposal only; success only; grant only; examination only; independent mark checked with no accept | Positive shows actor and recorder; negatives show no human act; independent act shown without accept |

## UNRESOLVED

| Item | Owner | Point of need | Effect on this definition |
|---|---|---|---|
| U-01 Act-class values / reserved list `UNRESOLVED{OI-001}` | Owner with App/SWB contract owners; carried by DEL-04-01 | Before operation-policy production contracts | Classes shown *policy unresolved*; no direct treatment |
| U-02 Routine tool/classifier permissions `UNRESOLVED{OI-002}` | Owner with App/SWB contract owners | Before permission-policy implementation | Not shown as autonomy grant |
| U-03 Grant model and act-kind names | DEL-04-01 v0.1 | V1 comparison | §2, §9 to be reconciled |
| U-04 Whether autonomy grant/change is a named act kind | DEL-04-01 with DEL-04-03 | V1 comparison | Recorded with person as setting actor; kind name open |
| U-05 Conservative rule for *unconfirmed* (§3) | DEL-04-01 policy with host owner | Before OUT-001 construction | Proposed only; host enforcement governs |
| U-06 Which settings version governs in-flight operations | Responsible host owner (DEP-001) | Before connected integration | Displayed *unconfirmed* unless host reports |
| U-07 Host origin, undo, check route, receipt supply `DEP-001` | SWBPIPE outside implementation session | Before corresponding connected-journey integration/examination and fallback-replacement decision | All host elements are fixture; none received |
| U-08 Component placement / host panel assembly `OI-014`, `OI-013` | App/shared contract owners; shared contract owner with SWB implementation owner | Before structural/production contract allocation (OI-014); before shared/host implementation boundary contracts (OI-013) | OUT-001 components only "where justified" |
| U-09 First connected operation `OI-021` | Owner via outside SWB session and App/shared owner | Before connected-activity SoW and execution | Placeholder operations in fixtures |
| U-10 Record representation for exchange | DEL-04-03 (RS-v0.1 U-04) | Before writer implementation | Exchange is semantic only |

## Verification cases (designed, not run)

| Case | Input | Expected result | Serves |
|---|---|---|---|
| VC-01 Scope before/after change | F1, F2 | Visible scope equals effective grant before and after; policy-unresolved class shows no direct route | VER-001 (AC-001) |
| VC-02 Unestablished change / result not a grant | F3; plus a successful operation in a propose class | No widening shown; success does not change state | VER-001 (AC-001) |
| VC-03 Checkpoint not discharged by autonomy | F6 | Checkpoint waiting until act record ref received | VER-001 (AC-001) |
| VC-04 Settings-in / record-out match | F2 | Displayed and recorded settings versions match; same run identity | VER-002 (AC-002) |
| VC-05 Missing / unconfirmed | F4, F5 | *unconfirmed* and *missing in record* explicit; no second record authority | VER-002 (AC-002) |
| VC-06 Origin/undo/check present | F7 | Four elements traced to host fixture evidence; undo completed only with receipt | VER-003 (AC-003) |
| VC-07 Absent host capability | F8 | Undo not offered/unknown; outcome unknown; nothing counted as available | VER-003 (AC-003) |
| VC-08 Standing facets | F9 | Each facet equals supplied evidence; lapsed and unknown visible; no synthesized label | VER-004 (AC-004) |
| VC-09 Act distinctions and labels | F10 | Positive faithful recording; negatives show no act; "accept" label only for proposals | VER-005 (AC-005) |
| VC-10 Owner and open-choice trace | §10, UNRESOLVED | Each REQ-007 act traced to owner; OI owners/points of need match register verbatim; no host delivery claimed | VER-006 (AC-006) |
| VC-11 Suite coverage | VC-01…VC-09 | Each AC-001…AC-005 covered; results bound to identified candidate; local results separate from host witness | VER-007 (AC-007) |
