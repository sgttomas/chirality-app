# V1-B — Receiver comparison: catalog, proposal, record, autonomy

- Run: APP-V4-FIRST-INCREMENT-20260928, node V1-B (CASE-002 Open_Questions Q-03)
- Reviewer: independent Type 2 reviewer (Claude Code `Agent` subagent). The reviewer
  did not write any compared design and did not delegate.
- Status: REVIEW RECORD. It compares definitions only. It accepts nothing,
  changes no design, and runs no fixture.
- Read from the working tree on 2026-09-28 (sha256 of the bytes read):

| Contribution | File | sha256 |
|---|---|---|
| DEL-03-01/C-v0.1 | `PKG-03…/DEL-03-01…/Design/CATALOG_AND_READ_BASIS.md` (423 lines) | `c13518c9453e65a57f6e90ea87c9c4133cc1baea3af4629edb28acbf1d0a0b72` |
| DEL-03-02/P-v0.1 | `PKG-03…/DEL-03-02…/Design/PROPOSAL_LIFECYCLE_AND_OUTCOMES.md` (447 lines) | `313487c05bef9dff6cb75a0543d563193542e519749cb6d17be4657598319bce` |
| DEL-04-03/RS-v0.1 | `PKG-04…/DEL-04-03…/Design/RECORD_SEMANTICS.md` (329 lines) | `1e4bb89e648f08915ba7ed472e176b5a8e9d9dba051d7964d79cb85d4c26c462` |
| DEL-04-02/AS-v0.1 | `PKG-04…/DEL-04-02…/Design/AUTONOMY_AND_STANDING_EXCHANGE.md` (252 lines) | `4c540c88fecfe7019148c5749fcadd48c43ebdf2a1b70df45e960f714308bd01` |
| Owner rulings | `OWNER_DECISIONS.md` (DECISION-1, D1–D4) | `f3f8e5f31ec87006fc9ab459c6ae57d08638439c234fa959ba2605914cf81f2e` |
| CASE-002 datasheet | `_DAG/cases/SCC-CASE-002/Case_Datasheet.md` rows M1 (DEL-04-03), M1-C, M1-P, M3 (both), M3-CP | `6acdc6c4e484ab7b46ba7d45a347961bc69b3e624bd29ef58a613ec6c66a71a6` (matches the prefix the designs cite) |

The ScopeOfWork hashes stated in all four design headers match the current
files: DEL-03-01 `179a6d35…6b84`, DEL-03-02 `42328987…128a`, DEL-04-02
`23a28caa…5e21`, DEL-04-03 `74d42c38…40c1`.

Severity key. **BLOCKING**: the two sides would give different verdicts on
the same fixture. The receiver cannot use the supplied meaning until one side
changes. **MAJOR**: a meaning is missing or conflicting in a way that would
make a receiver's VER case unsound or would strengthen standing. **MINOR**:
wording, vocabulary, fixture or completeness repair with no change in
verdict.

## 1. Q-03 answer per join

| Join | Supplier → receiver (version as read) | Receiver OUT/REQ/VER that consumes it | Version the receiver itself declares it consumed | Check performed here |
|---|---|---|---|---|
| J1 C → P (forward; DEP-03-01-023 / DEP-03-02-016) | C-v0.1 → P-v0.1 | DEL-03-02 OUT-001, OUT-002; REQ-003; VER-004 (M1-C) | P header: "DEL-03-01/C-v0.1 (co-developed in this run…)". Both were written by the same W3 executor, so no independent check existed before this review | Element-by-element: identity/version, arguments/targets, effects, errors, availability, basis, relied-on reference |
| J2 P → C (M3-CP return; DEP-03-01-026) | P-v0.1 §11 → C-v0.1 §9 / VC-C-04 | DEL-03-01 OUT-001, OUT-003; REQ-001, REQ-004; VER-004 (M3-CP) | C header: "DEL-03-02/P-v0.1 (co-developed…)" | P §11 step table compared with C §9 needs table and VC-C-04 |
| J3 P → DEL-04-03 (DEP-03-02-019) | P-v0.1 → RS-v0.1 | DEL-04-03 OUT-001, OUT-002, OUT-004; REQ-002, REQ-003, REQ-005; VER-001, VER-004, VER-006 (M1-P) | RS header: "accepted basis only … DEL-03-02 … referenced by accepted meaning". **RS has not consumed P-v0.1** | P §3.3, §4, §5, §7, §9, §10 compared with RS §5, §6, §9 |
| J4 P → DEL-04-02 (DEP-03-02-018) | P-v0.1 → AS-v0.1 | DEL-04-02 OUT-001, OUT-002; REQ-003, REQ-004, REQ-005; VER-003–005 (M1-P) | AS header: "DEL-03-02 (direct-autonomy branch, outcomes, origin) … by accepted meaning only". **AS has not consumed P-v0.1** | P §3.3, §4.4, §9 compared with AS §3, §5, §7, §8 |
| J5 DEL-04-02 ↔ DEL-04-03 (M3; DEP-04-02-008/009, DEP-04-03-014) | AS-v0.1 §6 ↔ RS-v0.1 §8 | DEL-04-03 OUT-001/002; REQ-002; VER-001 (settings-in). DEL-04-02 OUT-001/003; REQ-002/004/005; VER-002/004/005 (record-out) | Each consumed the other's v0.1 concurrently. Both were written by the same W2 executor ("unreviewed") | Exchange texts diffed. Exchange compared with each side's own states and inventory |
| J6 C → DEL-04-03 (content identity for lapse; R7 basis) | C-v0.1 §5, §6 → RS-v0.1 §5, §7 | DEL-04-03 REQ-002, REQ-004; VER-001, VER-003 (not a registered join, see RF-04) | RS: accepted meaning only | C §5.1 compared with RS L-1…L-9, E4 |
| J7 C → DEL-04-02 (standing facets) | C-v0.1 §6 → AS-v0.1 §8 | DEL-04-02 REQ-004; VER-004 (not a registered join, see RF-05) | AS: accepted meaning only | C §6.2 compared with AS §8 |

No receiver in J3, J4, J6 or J7 consumed an identified supplier version before
V1. This review is the first comparison of those meanings. Within J1/J2 and
J5 the two sides agree largely because each had one author. That agreement
is recorded below, but it is not independent evidence.

## 2. Agreements

| # | Join | Element | Supplier section | Receiver section |
|---|---|---|---|---|
| A-01 | J1 | The four basis elements have the same semantic names and meanings: workspace identity, generation, model revision, canonical content identity | C §5.1 | P §3.2 "Relied-on basis reference" |
| A-02 | J1, J3 | The relied-on basis is carried unchanged and is never recomputed at queue, acceptance or application. A later host-observed basis is a separate element | C §5.2 bullets 1–2 | P §3.2, §5 "No silent refresh"; RS §5 "not a later queue-time basis, HI §11 limit" |
| A-03 | J1 | Operation identity/version stays distinct from the basis. A request carries the version it was prepared for, with no reinterpretation | C §2 invariant 3, §7 row 1 | P §3.2 row 1 |
| A-04 | J1 | Targets are fixed at drafting, and a later selection never retargets | C §4.3 | P §6 |
| A-05 | J1/J2 | A stale refusal shows the relied-on and current bases with a reason. A re-draft is a new identity with lineage | C §9 "Proposal input C needs" rows 2–3 | P §5, §3.1 |
| A-06 | J1 | Unavailable, not permitted and channel not enabled are distinct from each other and from success. Authority is the only permitted channel difference | C §4.1 | P §2 "Permitted difference", §9 rows 1–3 |
| A-07 | all | `success` establishes execution only | C §6.2 rule 1 | P S-P7, §9; RS D5, OE-1; AS S5, DS-3 |
| A-08 | J1 | U-C3 (stale rule) and U-C4 (multi-read reliance) are held open jointly | C UNRESOLVED | P UNRESOLVED last row |
| A-09 | J2 | The M3-CP scenario and comparison positions match (read, proposal reference, refusal with both bases, re-draft, receipt). C implements no proposal behaviour, and AC-004 stays held until an executable return exists | C §9 "Return", VC-C-04 | P §11 |
| A-10 | J1/J2 | The SWBPIPE queue-time-basis limit is recorded as a receiving risk, not as a host assignment | C §5.2 "Receiving risk" | P §12 row 1 |
| A-11 | J3 | "Queued" needs a host acknowledgement. Transport completion does not show it | P §4.1 rule 1 | RS §5 queued row; VC-11 |
| A-12 | J3 | "Applied" needs a host receipt reference. Receipts are linked, not copied | P §4.1 rule 2, §13 | RS FA-3, §9, VC-03 |
| A-13 | J3 | "Accepted" needs evidence of a human act and is never inferred from success or application | P §10 "Accept a proposed edit" | RS §5 accepted row, HA-1 |
| A-14 | J3 | "Outcome unknown" is never inferred away. A later observation is recorded separately with its own basis and is not back-filled | P §4.1 rule 3 | RS E5, VC-10 |
| A-15 | J3 | A re-draft is a new entry and does not overwrite the old one | P §5 | RS OE-2 |
| A-16 | J4 | The four abstract host contributions for direct application: origin mark, undo route, later-check route, receipt | P §4.4 bullet 2 | AS §7 table |
| A-17 | J4 | Direct application records no acceptance. The word is "accept", never "approve" | P §4.4 bullet 1, E-2 row 4 | AS §8 origin/route facet, DS-1 |
| A-18 | J4 | A checkpoint overrides the grant, and the run waits for the person's act | P §4.4 bullet 4 (S-P13) | AS §4 |
| A-19 | J5 | The settings-in, record-out and comparison texts match word for word in substance. Authority split: the control holds the current grant, the record holds what was recorded, and the display is derived | AS §6 | RS §8 |
| A-20 | J5 | A checkpoint is discharged only by a human-act record reference of the declared kind | AS §4 | RS R8 |
| A-21 | J7 | Standing facets for currency, limitations and agent findings (not a human act) | C §6.2 rows 1, 3, 5 | AS §8 Temporal, Limitations, Agent examination |
| A-22 | J6 | A carried act is shown lapsed when bound content changes. C carries acts and never creates them | C §6.2 rules 3–4 | RS L-6, HA-2 |
| A-23 | J3/J4 | Item-level dispositions exist, and a derived proposal state is never stronger than its items | P §4.3 | RS §6.1 Scope, L-7; AS §2 granularity |
| A-24 | all | No representation, algorithm, identity form or placement is selected | C §0 | P §0; RS §0; AS §0 |

## 3. Disagreements

### D-01 BLOCKING (J3, J6; item-level acceptance and lapse): what an "accept an edit" act binds to

- P §4.1 "accepted" row: "Host-recorded acceptance act, bound to proposal
  content (S-P11)". P §4.2: "treatment of the recorded acceptance (which
  lapses under S-P11 if content changed) are **U-P3**". P §5: "Any acceptance
  recorded on the stale proposal does not carry over (it bound to other
  content)".
- RS E1: "Act record ⟨act:1⟩: kind **accept an edit** … subject ⟨prop:1⟩
  rows S-103/S-104, c₀ ⟨cid:p1-103,104⟩". RS L-1: "For host content, c₁ comes
  from the host's read basis (DEL-03-01 canonical content identity); for App
  files, from the file content identity." RS VC-09: "⟨act:1⟩ then S-104 edited
  → Partially lapsed listing S-104".
- C §5.1 defines content identity only for "the content actually read". It
  defines none for a proposal or a change item.

**Conflict.** No file defines a content identity for a proposal or a change
item, yet P and RS both bind acceptance to one. The sources give different
answers:

- RS E1 binds the act to proposal content. Under that binding, an edit to the
  model row S-104 leaves c₁ unchanged, so the act is not lapsed.
- RS VC-09 and L-1 draw c₁ from the host read basis. Under that binding the
  act is lapsed.
- If acceptance binds to model rows, the host's own application of the
  accepted item changes that row. The acceptance would then lapse the moment
  it is applied.
- P U-P3 cannot be stated coherently until the binding is fixed.

**Resolution.**

- **DEL-03-02 changes.** Define a semantic *change-item content identity*
  covering operation identity/version, bound targets, old/new values and the
  relied-on basis, with the method unselected. Make it the bound content of
  "accept an edit". State that applying the accepted item does not lapse the
  acceptance. State that a basis failure between acceptance and application
  is handled under the stale rule and U-P3, not by model-row lapse, unless
  the owner rules otherwise.
- **DEL-04-03 changes.** Add a third c₁ source to L-1 (change-item content
  identity from DEL-03-02). Restate VC-09 either as an edit to a proposal
  item, or as a *mark checked* act on model rows if the aim is model-row
  partial lapse. Mirror U-P3 (see X-04).

### D-02 BLOCKING (J6): subject-scoped content identity for lapse

- RS L-1: "Obtain c₁ for exactly the bound subject and scope — not the
  workspace generation or model revision (an unrelated edit elsewhere must not
  lapse a row-bound act). For host content, c₁ comes from the host's read basis
  (DEL-03-01 canonical content identity)". RS E4: "host read basis gives c₁
  ⟨cid:r102b⟩".
- C §5.1 "Canonical content identity": "An identity of the content actually
  read … **scope** (whole model vs the view/rows read) is a host input (F-C3)".
  C §5.1 rule 5 allows one descriptor per view, not per row.

**Conflict.** C supplies at most one content identity per read or view. RS
needs one per bound subject: per row, and per element for L-7. If the read
basis identity covers a whole view, the E4 control ("S-101 edited instead →
⟨act:3⟩ not lapsed") gives the wrong verdict. RS AC-004/VER-003 cannot be met
from C's elements. V4-HI-32's own example is "a row's content hash".

**Resolution. DEL-03-01 changes.** Add a *subject content identity* element:
per object/row in a read result, host-supplied, with the method unselected.
Keep it distinct from the read-basis canonical content identity, and route
its scope as a host input under U-C2/U-C3. **DEL-04-03** then cites that
element in L-1 instead of "the host's read basis".

### D-03 MAJOR (J6): no identity-method designation

- RS L-2: "If m₁ ≠ m₀ or the methods cannot be shown comparable →
  **unknown (incomparable)**". RS §10 PKG-03 row: DEL-03-01 "Supplies back:
  Canonical content identity method (m)".
- C §5.1: "computed by a host canonicalization … **Algorithm and
  canonicalization unselected**". No element names which method produced a
  given identity.

**Conflict.** Without a method designation carried with every content
identity, L-2 can never establish comparability. Every lapse evaluation
therefore resolves to *unknown (incomparable)*, and VC-07's positive branch
cannot pass.

**Resolution. DEL-03-01 changes.** Add a semantic *identity method
designation* that accompanies each content identity (basis-level and
subject-level). The algorithm stays unselected.

### D-04 MAJOR (J3): the record's outcome vocabulary is narrower than P's taxonomy

- P §9 lists these outcomes: unavailable, not permitted, channel not enabled,
  invalid, stale, queued, accepted, applied (receipt), rejected, withdrawn,
  outcome unknown, success (operation).
- P §4.2 adds a refusal before queueing ("the proposal stays *drafted*").
- P §4.3 adds per-item dispositions.
- P §4.4 adds direct-branch "refused (invalid | stale | not permitted)".
- P §9 gives outcome unknown "Only the last observed state".
- P §5 refusal content: "**relied-on basis** (unchanged); **current basis**".
- RS §5 table covers only: drafted/validated, queued, accepted, applied,
  applied (direct), rejected/withdrawn, stale (refused) ("Host refusal with
  reason"), outcome unknown.
- RS R7 is "One entry per requested operation", which includes reads, but
  RS §5 carries only a "relied-on read basis".

**Conflict.** The following cannot be recorded:

- the pre-execution refusals
- read and check outcomes, with their *observed* basis
- item-level dispositions
- the last observed state for an unknown outcome
- the current basis in a stale refusal

The last gap means the run record cannot carry the M3-CP trace (VC-C-04),
which DEL-09-11 would need to reconstruct.

**Resolution. DEL-04-03 changes.** Adopt P §9 by reference, adding:

- per-item disposition entries
- "last observed state" on outcome unknown
- relied and current bases on stale entries
- an *observed basis* element for read and check entries

### D-05 MAJOR (J1): P has no application-time error outcome

- C §3 element 7: "Every error … including whether any effect may have
  occurred … an error whose effect is unobservable routes to DEL-03-02
  *outcome unknown*". C §4.1 Error "Carries … any partial-effect statement".
- P §9 has only "invalid | Host validation refused with catalog error |
  Nothing applied".

**Conflict.** A declared error raised during application (for example
fixture E-location-occupied surfacing at apply) with a known *none* or
*partial* effect has no outcome in P. C routes only the unobservable case.

**Resolution. DEL-03-02 changes.** Add an *application error* outcome
carrying the C error identity and an effect statement: none, partial (with
receipt references), or unknown (which goes to the overlay). Keep *invalid*
for validation refusal only.

### D-06 MAJOR (J4): the direct-branch entry condition ignores grant display states

- P §4.4: "Where the person has granted direct application for the operation
  class". P §3.3: "The person's grant in force for this operation class
  (DEL-04-02), or *proposal required*".
- AS §3: *requested-unestablished* "No — the prior effective value governs".
  *unconfirmed* "Treated as the most conservative of last-known and default".
  *not set* / *policy unresolved* "No direct treatment".

**Conflict.** P does not say that only an *effective* direct treatment admits
the direct branch. Read literally, P would enter the branch on a requested
but unestablished widening, or on an unconfirmed grant.

**Resolution. DEL-03-02 changes.** Enter the direct branch only when the
DEL-04-02 state for the class is *effective* with treatment *direct*. Every
other state takes the proposal route. The origin element should record that
display state.

### D-07 MAJOR (J3, J4, J5): which settings version governs, and when

- P §3.3: "Autonomy standing **at drafting**". P §4.4: "A grant changed during
  work … applies from the change onward; the standing actually in force **at
  application** is what is recorded".
- RS §5: "settings version governing the **route decision**".
- AS §5 step 4: "Which version governed an operation already evaluated or in
  flight is a **host fact** the host must report per operation; if not
  reported … *unconfirmed* (no inference)". AS §5 step 5: "widening never
  converts a queued proposal into an applied change or an acceptance".
- P has no settings-version identity and does not state step 5's rule.

**Conflict.** The files name three different moments (drafting, route
decision, application). P assumes that the standing at application is known,
while AS says it is unconfirmed unless the host reports it.

**Resolution. DEL-03-02 changes.** Use DEL-04-02's *settings version
identity* in two elements:

- the version at the route decision
- the version in force at application, which is host-reported or else
  *unconfirmed*

P should also adopt AS §5 step 5. **DEL-04-03** carries both elements in R7.

### D-08 MAJOR (J1, J4, J3; changed by D2): whether model changes can be direct in fixtures

- C §10.1 OP-C4 "Add support": "`UNRESOLVED{OI-001}`; accepted V4-HI-41
  default setting = proposal (widenable by person)".
- P §4.4: "Where the class is `UNRESOLVED{OI-001}`, the direct branch is not
  exercised in any conformance claim."
- AS §2: "Until adopted, such a class is displayed as **policy unresolved**
  and receives no direct treatment". Yet AS F2 has the person widen
  `op:add-support` to direct, and "control confirms ⟨set:2⟩". AS F7 and RS E5
  ("Direct `op:add-support` under ⟨set:2⟩") exercise it.

**Conflict.** C and P forbid a direct model-change fixture, while AS and RS
depend on one. AS is also internally inconsistent: F1 shows model change as
"*effective: propose*", which treats it as adopted.

**D2 effect.** D2 reserves *acts*, not operations: "(b) accepting a proposal
wherever the active autonomy requires a proposal". A model change therefore
looks like "may apply within granted autonomy", with a V4-HI-41 default of
proposal and "Operation-specific additions … when the concrete SWB operation
is selected (OI-021)". That supports AS/RS.

**Resolution. DEL-03-01 and DEL-03-02 change in R1**, once DEL-04-01 carries
the D2 representation. The fixtures in all four files should read "class per
DECISION-1 D2; operation-specific additions pending OI-021; not SWBPIPE
adoption (DEP-001)".

### D-09 MAJOR (J3): the duplicate-submission recording rule assumes the outcome

- RS OE-3: "duplicate submission produces one entry with one effect
  reference; the mechanism is DEL-03-02's".
- RS R7: "One entry per requested operation". RS D7: "Only observed events
  are shown as having happened".
- P §7: "Effect count **observed** … a repeat submission reports the existing
  state". P VC-P-09: "record exercised scope without global exactly-once
  claim".

**Conflict.** OE-3 writes the one-effect obligation into the record as fact
and collapses the repeated request. If the host produced two effects, the
record would hide it, and the reconstruction reader would lose the retry.

**Resolution. DEL-04-03 changes.** Give each submission its own R7 entry
referencing the same proposal identity. Record only the effect references
actually observed (the same receipt, two receipts, or unknown).

### D-10 MINOR (J3, J4; item granularity): acceptance unit, row versus change item

- AS §2: "acceptance granularity row / multi-row / whole batch".
- RS §6.1 Scope: "rows 3, 5; whole batch".
- P §3.1: "Change items … supports row-level acceptance". P §3.4 defines an
  item as affected object + attribute.

**Conflict.** Two items can touch one row, as in P E-1 where S-3 has a
stiffness item. The mapping from a view row to change items is undefined.

**Resolution. DEL-03-02** defines the acceptance unit as change items, with
a host view row being a presentation of one or more items. **DEL-04-03**
expresses scope in item identities, and **DEL-04-02** maps its labels to
that.

### D-11 MAJOR (J5): settings-in cannot carry every display state or a refusal

- AS §3 has five states: effective, requested-unestablished, unconfirmed,
  **not set**, **policy unresolved**. AS §5 step 3: "On refuse → reason
  displayed; settings-in **sends the refusal**".
- AS §6 / RS §8 settings-in carries display state "(effective /
  requested-unestablished / unconfirmed)" and treatment "(direct / propose /
  class unresolved)". It has no *not set* and no refusal/reason element.
- RS R6 lists the same three states.

**Conflict.** "Not set" cannot be told apart from *missing in record*. A
refusal described in AS §5 has nowhere to go. This bears on AC-002, "missing
or unconfirmed settings remain explicit".

**Resolution. DEL-04-02** owns the value list: add *not set* and a *refused
(reason)* event to settings-in. **DEL-04-03** mirrors both in R6 and §8.

### D-12 MAJOR (J5; changed by D2(e)): who may change the grant, and how it is recorded

- AS §3 *requested-unestablished* entry evidence: "Person (**or an agent on
  the person's request**) submitted a change". Compare AS §5 step 1: "an
  agent may *prepare* or *ask for* a change but cannot perform it".
- AS U-04 and RS HA-5/U-08: "Whether it is also a named act kind is a
  DEL-04-01 reconciliation point".
- The settings-in element list has one "establishing evidence reference" for
  both the person's control event (AS §5 step 2) and the control confirmation
  (step 3).

**D2(e)** reserves "changing the autonomy grant or enabling external-agent
access" to the person. An agent submitting the change to the control would
be performing that reserved act, and the grant change is now a reserved
human act.

**Resolution. DEL-04-02** limits entry to the person's own control act.
**DEL-04-03** records the grant change as a human-act record, with the kind
name from DEL-04-01, referenced from R6. **Both sides** split settings-in
into a *setting act reference* and *establishment evidence*.

### D-13 MINOR (J5): record-out omits fields the display needs

- RS §8 / AS §6 record-out: "act records with actor, recorder, kind, scope,
  purpose and lapse evaluation; evidence limits".
- AS F9 expects "lapsed act shown lapsed **with original content**". AS §4
  displays checkpoint state. DEL-04-02 VER-004 compares "changed-content
  lapse received from the record owner".

**Conflict.** Record-out lacks bound subject, bound content identity (c₀ and
the compared c₁), recording mode, evidence references with resolution
status, act class and R8 checkpoint events.

**Resolution. DEL-04-03** adds these to record-out, and DEL-04-02 mirrors
them.

### D-14 MINOR (J5): lapse-state vocabulary

- AS §8 Human acts: "**not lapsed** · **lapsed** · partially lapsed ·
  unknown".
- RS §7: "not lapsed · lapsed · lapsed (subject absent) · partially lapsed ·
  unknown (incomparable) · unknown (unavailable) · not yet evaluated".

**Resolution. DEL-04-02** adopts the RS list. *Not yet evaluated* must never
render as *not lapsed*.

### D-15 MAJOR (J7): host checks lack a per-check basis, and "checked" is overloaded

- C §6.2: "Checks passed | Each named host check that the result passed,
  **with the basis it was run against**".
- AS §8 Host checks: "**checked** (list of host checks passed, each named)".
  It has no basis, and the value "checked" is shared with the human act
  *mark checked* (reserved by D2(a)).

**Conflict.** A check that passed on r12 would show as "checked" beside a
current r13 result. That is stronger than received, contrary to DEL-04-02
REQ-004.

**Resolution. DEL-04-02** changes as follows:

- rename the facet value to "host checks passed"
- carry each check's basis
- show a check run on an earlier basis as historical

### D-16 MINOR (J7, J6): C carries only a subset of the act fields

- C §6.2: "act name (DEL-04-01), decision actor (the person), recorder where
  distinct, content binding and lapse state (DEL-04-03)".
- RS §6.1 and DEL-04-03 REQ-004 require content, **scope and purpose**.

**Conflict.** A carried act without scope can be read as covering the whole
table.

**Resolution. DEL-03-01** carries the RS §6.1 element set by reference, at
minimum scope, purpose, recording mode and evidence limits.

### D-17 MINOR (J3, J4): origin elements

- P §3.3 origin: author type, author identity (seat/role instance), channel,
  conversation, workflow run, autonomy standing, reason. P says origin is
  "linked (not copied) into the run record".
- RS §5: "*origin* (agent author type, conversation and run …)" plus
  "*origin-mark reference*". Person-origin is absent.
- AS §7 origin reference: "agent author type, conversation, workflow run,
  relied-on basis".

**Resolution.**

- **DEL-04-03** records the App's own request-side origin, with all P §3.3
  elements, including channel and person author type. It links the host
  origin mark, and treats any mismatch between the two as an evidence limit.
- **DEL-03-02** clarifies that "linked, not copied" applies to the host
  origin mark.

### D-18 MINOR (J4, J3): undo is undefined in P

- AS §7: "the undo is itself a change with its own origin and is passed to
  the record (DEL-04-03 R7)". Its outcomes are *undone* / *refused* /
  *outcome unknown*.
- P never mentions undo. RS R7 has no "undoes ⟨entry⟩" relation.

**Resolution. DEL-03-02** states that an undo is a change through the one
route (§2), with its own origin, basis check and outcome, and maps *undone*
to applied (receipt). **DEL-04-03** adds the relation.

### D-19 MINOR (J2): evidence-class labels

- C Verification header: "*schema fixture*, *adapter result* or *actual host
  observation*".
- P §11 and the M3-CP datasheet row: "*illustrative*, *test-double* …
  *actual host*".

**Resolution. DEL-03-01** uses P's labels for VC-C-04, or states the mapping.

### D-20 MINOR (all): the fixtures diverge

- C §10.4: "Row S-2 … shown **lapsed** at r13 because S-2's stiffness
  changed".
- P §11 step 3: "Person edits S-3 in host UI | model now r13".
- RS uses rows S-101…S-105 and basis ⟨ws:1, gen:7, rev:m7⟩. AS uses
  `op:add-support`, `op:adjust-run` and `op:set-label` rather than OP-C1…C6.

**Conflict.** One invented model carries three vocabularies and a
contradictory r12 → r13 change. That blocks a single trace from M3-CP into
the record (VC-C-04 → RS E1/E4).

**Resolution. DEL-03-01's §10** becomes the shared fixture catalogue with one
revision timeline. The other three files re-label to it.

### D-21 MINOR (J1): non-success outcomes should carry the evaluated basis

- C §5.1 rule 4: "Unavailable and error results carry the basis they were
  evaluated against".
- P §9's unavailable, not permitted and invalid rows do not say so.

**Resolution. DEL-03-02** adds the evaluated basis to those outcomes, and
DEL-04-03 records it.

### D-22 MINOR (J2): whether a "receipt cites" the basis

- C §9: "Receipt reference to the relied-on basis and to the resulting
  revision". VC-C-04: "receipt cites the applied proposal's relied basis".
- P §11 step 9: "receipt cites P-2, item 1, relied B2, resulting r14".
- P §1: receipts are host-owned, and the contract "never manufactures one".

**Conflict.** The phrasing assigns receipt content to the host.

**Resolution. DEL-03-02** defines the *applied outcome* as associating
proposal/item identity, relied-on basis, receipt reference and resulting
revision. **DEL-03-01's VC-C-04** compares that association and records
whether the host receipt itself carries the basis, as a host observation.

### D-23 MINOR (J3): actors for rejection and withdrawal

- RS §5: "Person rejected / proposer withdrew | Rejection act record / host
  withdrawal record".
- P §4.1: rejected by "The person … or host refusal on validation at
  application (U-P5)". Withdrawn by "Proposer or person".

**Resolution. DEL-04-03** records the actor per P and keeps a host refusal
distinct from a person's rejection act.

## 4. Absent inputs

| # | Absent input | Owner | Point of need | Effect |
|---|---|---|---|---|
| X-01 | Change-item content identity (D-01) | DEL-03-02, with the host owner for how it is produced (DEP-03-02-023) | R1 v0.2, before DEL-04-03 VC-09 and P U-P3 are designed | Acceptance lapse cannot be evaluated |
| X-02 | Host subject/row content identity and its scope (D-02; C U-C2/U-C3; V4-HI-32 "a row's content hash") | Host owner / SWBPIPE (DEP-03-01-025), with DEL-03-01 | Before lapse conformance (DEL-04-03 VER-003) and stale-rule implementation | Row-scoped lapse and the unrelated-edit control rest on fixtures only |
| X-03 | The settings version governing each in-flight operation (AS U-06) | Host owner (DEP-001; DEP-04-02-010) | Before connected integration | P §4.4 "standing in force at application" is unconfirmed until reported |
| X-04 | P U-P3 (basis fails after *accepted*, before *applied*) is not mirrored in RS UNRESOLVED | Host owner with DEL-03-02 and DEL-04-03 | R1 | The record has no disposition for that case |
| X-05 | Lapse under restore/revert or a new generation: content returning to c₀ after a lapse; C "generation" when a restore starts a new lineage | Host owner (U-C2 generation) with DEL-04-03 (L-5/L-8) | Before lapse display criteria are fixed (with RS U-07) | Under RS L-5 an act could silently "un-lapse". Not ruled anywhere |
| X-06 | C U-C5 (are host-stored agent findings a change operation?) is not mirrored in RS R10 or AS §8 "Agent examination" | Host owner | Before V4-EXM-21 fixture binding | The record and display of findings may later need a change outcome and basis |
| X-07 | Staleness of a non-mutating check that cites a relied-on basis. C §5.2 includes "a non-mutating check that relies on a prior read", but P covers changes only | DEL-03-01 | R1 | No defined behaviour for OP-C3 when its cited basis no longer holds |
| X-08 | An executable M3-CP return: a candidate-bound test-double observation | DEL-03-02 (DEP-03-01-026) | Before AC-004/VER-004 is claimed | Only a designed comparison exists (both sides agree) |
| X-09 | DEL-04-01's adopted class representation that carries D2/D3 | DEL-04-01 (R1) | Before C/P/AS/RS replace `UNRESOLVED{OI-001/002}` | D-08, D-12 and §5 below depend on it |
| X-10 | Where a D3 routine tool-permission decision (the App user's Codex setting) is recorded. RS U-02 says "whether it appears in R6 is open" | DEL-04-03 with DEL-01-01 | Before OUT-001 configuration | Under D3 it is not autonomy, so R6 is the wrong home. Location is unassigned |

## 5. Where owner rulings D2/D3 change v0.1 statements

The v0.1 drafts predate DECISION-1. R1 applies these changes through
DEL-04-01's adopted representation. None of them shows that SWBPIPE has
adopted the list (D2: "does not show that SWBPIPE has adopted this list";
V4-HI-30 "The host names and enforces its own list").

| File § | v0.1 statement | Ruling | Change needed |
|---|---|---|---|
| C §3 #8 class handling; UNRESOLVED OI-001 row | Class values "`UNRESOLVED{OI-001}` … where no adopted assignment exists" | D2 | Carry the five reserved acts. Operation-specific additions stay open until OI-021 |
| C §10.1 OP-C6 "Mark row checked" | "`UNRESOLVED{OI-001}`" | D2(a) | Change to *reserved to the person* |
| C §10.1 OP-C4/C5 | "`UNRESOLVED{OI-001}`; … default setting = proposal" | D2(b) | Change to *may apply within granted autonomy*, default proposal (V4-HI-41), with additions pending OI-021 (D-08) |
| C §4.1 "Not permitted"; UNRESOLVED OI-002 row | "cannot name a classifier rule" | D3 | No classifier mode in hosts, so a host *not permitted* never cites one. A denial by the App user's Codex tool permission is App-side tool execution, not a host outcome |
| P §3.3 "Autonomy standing at drafting"; §4.4 last bullet; §9 not permitted; §10 closing rules; UNRESOLVED OI-001/002 | "`UNRESOLVED{OI-001}` … `UNRESOLVED{OI-002}`" | D2, D3 | Replace these with the D2 reserved acts and the D3 host rule |
| P U-P6 / §4.1 withdrawn row | Agent withdrawal "`UNRESOLVED{OI-001}`" | D2 | Withdrawal and rejection are not among the five reserved acts. U-P6 continues as an operation-specific or host question (V4-HI-30), not OI-001 |
| AS §2 policy bound; §3 *policy unresolved*; F1 `op:set-label`; U-01 | Classes "`UNRESOLVED{OI-001}`" | D2 | Keep *policy unresolved* only for operation-specific additions pending OI-021 |
| AS §2 "Routine tool permission … `UNRESOLVED{OI-002}`"; U-02 | Open | D3 | It is the App user's own Codex setting, governs tool execution only, and is absent in hosts. It is still not shown as a grant (the v0.1 exclusion survives) |
| AS §3 requested-unestablished "or an agent on the person's request"; U-04 | Agent may submit a change; act kind open | D2(e) | Only the person changes the grant, and it is a reserved act (D-12) |
| RS §0 / §6.1 Act class; HA-6; U-01 | "`UNRESOLVED{OI-001}` throughout" | D2 | Carry the D2 values with the decision-basis reference `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` |
| RS HA-5 / U-08 (grant change as act kind) | Open | D2(e) | Record it as a human-act record (kind name from DEL-04-01) |
| RS U-02 | Routine permission "not recorded as a human act; whether it appears in R6 is open" | D3 | The first clause is confirmed. R6 is not its home (X-10) |

## 6. Register findings (`Dependencies.csv`, rows checked)

Rows checked: DEL-03-01 DEP-03-01-022…030; DEL-03-02 DEP-03-02-016…026;
DEL-04-02 DEP-04-02-007…014; DEL-04-03 DEP-04-03-011…020 (ANCHOR rows
excluded).

| # | Finding | Rows | Kind |
|---|---|---|---|
| RF-01 | DEP-03-02-018 (DEL-03-02 DOWNSTREAM HANDOVER → DEL-04-02, "standing and direct-autonomy origin semantics") has no UPSTREAM mirror in DEL-04-02. DEL-04-02's source table (key U) cites only DEL-04-01 and DEL-04-03, although CASE-002 M1-P names DEL-04-02 REQ-003–005/VER-003–005 as a receiver of P | DEP-03-02-018; DEP-04-02-007…014 | Missing mirror; SoW source gap (reported, not changed) |
| RF-02 | DEP-03-02-019 (→ DEL-04-03, "outcome semantics and host receipt links") has no UPSTREAM mirror in DEL-04-03. DEL-04-03 SoW REQ-005 frames PKG-03 only as a consumer | DEP-03-02-019; DEP-04-03-011…020 | Missing mirror; SoW framing gap |
| RF-03 | DEP-04-03-012 (DEL-04-03 DOWNSTREAM INTERFACE → PKG-03, "basis/receipts") has no UPSTREAM mirror in DEL-03-01 or DEL-03-02. The datasheet's M1 DEL-04-03 receivers omit PKG-03. Yet C §6.2 consumes act records and lapse state, and P §4.1 consumes acceptance acts | DEP-04-03-012; DEP-03-01-022…030; DEP-03-02-016…026 | Missing mirror; datasheet row gap |
| RF-04 | No row in either direction for C → DEL-04-03 content identity and read basis, which RS L-1, R7 and §10 depend on (D-02, D-03). The M1-C receivers omit DEL-04-03 | none exists | Missing dependency row |
| RF-05 | No row for C → DEL-04-02 standing meaning (C §6.2 → AS §8; DEL-04-02 REQ-004). The M1-C receivers omit DEL-04-02 | none exists | Missing dependency row |
| RF-06 | DEL-03-02 has no UPSTREAM row from DEL-04-02, although P §13 says "Expect from DEL-04-02: Grant in force per operation class; during-work changes" (D-06, D-07). DEP-03-02-017 covers DEL-04-01 only | DEP-03-02-016…026 | Missing dependency row (the P ↔ DEL-04-02 exchange runs both ways) |
| RF-07 | DEP-04-02-009 (DEL-04-02 DOWNSTREAM INTERFACE → DEL-04-03, settings-in) has no UPSTREAM mirror in DEL-04-03, though RS R6 consumes it. The datasheet records only the DEP-04-03-014 / DEP-04-02-008 pair | DEP-04-02-009; DEP-04-03-011…020 | Missing mirror |
| RF-08 | DEP-03-01-026 (DEL-03-01 UPSTREAM INTERFACE ← DEL-03-02, the M3-CP return) has no DOWNSTREAM mirror in DEL-03-02, although P's header names the return. The datasheet line mirroring C/P pairs lists only DEP-03-01-023 / DEP-03-02-016 | DEP-03-01-026; DEP-03-02-016…026 | Missing mirror |
| RF-09 | DEL-03-02 rows carry SatisfactionStatus `TBD`. The DEL-03-01, DEL-04-02 and DEL-04-03 rows carry `PENDING` | DEP-03-02-016…026 | Register value inconsistency (minor) |

These go to the register owner and closeout (C1). R1 design repair does not
edit registers.

## 7. Prioritized repair list for R1

1. **D-01 (DEL-03-02, then DEL-04-03). BLOCKING.** Define the change-item
   content identity and the accept-an-edit binding. State that application
   does not lapse acceptance. Rewrite RS E1, L-1 and VC-09. Mirror U-P3
   (X-01, X-04). Settle the row-versus-item unit at the same time (D-10).
2. **D-02 and D-03 (DEL-03-01, then DEL-04-03). BLOCKING/MAJOR.** Add a
   subject-scoped content identity and an identity-method designation to C,
   and re-point RS L-1 and L-2 to them. Keep the scope as a host input
   (X-02).
3. **Apply D2/D3 (§5), via DEL-04-01's representation, in all four files.**
   This includes D-08 (model-change class and the direct fixtures) and D-12
   (only the person changes the grant; the grant change is a recorded
   reserved act; split the setting act reference from the establishment
   evidence).
4. **D-04 (DEL-04-03) and D-05 (DEL-03-02).** Unify the outcome vocabulary:
   RS adopts P §9 with item dispositions, last observed state, both stale
   bases and the observed basis for reads. P adds an application-error
   outcome with an effect statement.
5. **D-06 and D-07 (DEL-03-02, mirrored in DEL-04-03 R7).** The direct
   branch applies only on an *effective* direct state. Record two settings
   versions (route decision; in force at application, host-reported or
   unconfirmed). Widening never converts a queued proposal.
6. **D-11 and D-13 (DEL-04-02 and DEL-04-03 M3 exchange).** Add *not set*,
   *refused (reason)* and the act reference. Extend record-out with bound
   subject, c₀/c₁, recording mode, evidence references, act class and R8
   checkpoints.
7. **D-09 (DEL-04-03 OE-3).** Record each submission separately, with only
   the effects actually observed.
8. **D-15 (DEL-04-02).** Rename to "host checks passed" and carry a basis per
   check.
9. **MINOR items.** D-14 lapse vocabulary; D-16 C act fields; D-17 origin;
   D-18 undo; D-19 evidence labels; D-20 one shared fixture catalogue and
   timeline, owned by C §10; D-21 evaluated basis on refusals; D-22
   applied-outcome association rather than receipt content; D-23
   rejection/withdrawal actors.
10. **Open items to carry forward.** X-05 (restore/generation and lapse),
    X-06, X-07, X-10. Register findings RF-01…RF-09 go to C1 and the
    register owner.

## 8. Counts

- Agreements: 24.
- Disagreements: 23 in total (BLOCKING 2, MAJOR 10, MINOR 11).
  - BLOCKING: D-01, D-02.
  - MAJOR: D-03, D-04, D-05, D-06, D-07, D-08, D-09, D-11, D-12, D-15.
  - MINOR: D-10, D-13, D-14, D-16, D-17, D-18, D-19, D-20, D-21, D-22, D-23.
- Absent inputs: 10 (X-01…X-10).
- D2/D3 effect rows: 12.
- Register findings: 9 (RF-01…RF-09).
