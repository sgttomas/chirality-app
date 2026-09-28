# Autonomy and Standing Exchange
- Contribution: DEL-04-02/AS-v0.2
- Status: DRAFT DEFINITION — proposed, unsupplied, not implemented, not accepted
- Serves: OUT-002 (receiving-interface contract content); OUT-001 and OUT-003 (component behaviour and fixture design only — no component or fixture exists); REQ-001…REQ-007; AC-001…AC-007 via designed VER-001…VER-007
- Basis: repo 6e18505e3; ScopeOfWork.md sha256 23a28caabd61da20dc2efed722f7e487856ef4488ab4f3454be4ed3249725e21; `P/docs/PRD.md` §4.3 V4-EXE-02/03, §4.5 V4-AUT-01…05, §4.6 V4-PM-06, §4.7 V4-REC-01…05; `P/docs/HOST_INTEGRATION.md` §1, V4-HI-04, V4-HI-11/12, V4-HI-20…25, V4-HI-30…33, V4-HI-40…42, V4-HI-50…52, V4-HI-70/71, §11; `P/docs/ARCHITECTURE.md` §4, V4-ARC-20; `P/docs/EXAMINATION.md` V4-EXM-21/22; `P/docs/OPERATING_METHOD.md` V4-OPS-30…32; `DECISION_BRIEF.html` d2, d3; `OWNER_DIRECTIONS.md` J, O; `SCC-CASE-002/Case_Datasheet.md` M1 (DEL-04-03 and M1-P rows), M3; `_Decomposition/Open_Issues.csv` OI-001/002/013/014/021; `External_Dependencies.csv` DEP-001. Run folder `APP-V4-FIRST-INCREMENT-20260928`: `OWNER_DECISIONS.md` (DECISION-1; sha256 f3f8e5f31ec87006…), `R1_RESOLUTIONS.md` (sha256 2f9c7e72aa836262…), `comparisons/V1-A.md` (01811533bf0aedad…), `V1-B.md` (09eebfe0ed78058a…), `V1-C.md` (8d46258ad0120067…)
- Consumed inputs: DEL-04-02/AS-v0.1 (sha256 4c540c88fecfe701…, as compared in V1); DEL-04-03/RS-v0.2 (repaired concurrently by the same executor; its §8 is restated in §6 here). Owner rulings D2/D3 through DEL-04-01's adopted-decision record (R1_RESOLUTIONS R-2). Supplier v0.2 elements taken **from R1_RESOLUTIONS, not from the supplier files** (under concurrent repair, not read), each "per R1_RESOLUTIONS R-n; to be confirmed at IR1": DEL-04-01 canonical act names, label rule, treatment → runtime outcome map, checkpoint dispositions (R-1, R-3, R-4, R-5); DEL-03-02 §9 outcome taxonomy incl. application error, change-item content identity, direct-branch entry condition, two settings references (R-6, R-7, R-8); DEL-03-01 host-check basis, shared fixture FX-PIPE-01 (R-9).
- Receivers: CASE-002 M3 — DEL-04-03 (OUT-001/002; REQ-002; VER-001) receives settings-in; DEL-04-02 compares under OUT-003; REQ-002; VER-002. DEP-04-02-009 (DEL-04-03 downstream). DEL-03-02 (direct-branch entry on effective state; V1-B D-06), DEL-05-01 (grant in force per dispatch; V1-C AB-04) and DEL-05-02 (active scope display; V1-A RF-05/V1-C RF-4) — registered edges pending register repair at C1. Host builder via DEL-03-04 and the external SWBPIPE owner through human relay (DEP-04-02-010) — as questions, not assignments.

## Changes from v0.1

| V1 item | Change in v0.2 |
|---|---|
| V1-A D-01; V1-C D-17 (R-1) | Canonical act names A1–A14; "accept an edit" → A5 accept; faithful recording → A9 record |
| V1-A D-02, §5 rows; V1-B D-08, §5 rows (R-2) | Blanket `UNRESOLVED{OI-001}` removed. Model-change class = *may apply within granted autonomy* (DERIVED, V4-HI-41) with default *propose*; reserved acts per D2; "policy unresolved" narrowed to "no policy basis" for operation-specific additions pending OI-021 |
| V1-A D-05 (R-3) | Treatment resolved on the host route; direct request without effective direct → *not permitted*, never converted; no policy basis → direct not permitted, propose available |
| V1-A D-06; V1-B D-12 (R-8, D2e) | Display states split: *requested by agent (A8)* vs *set by person, not yet confirmed*; only the person changes the grant (A12); settings-in carries requester and setting actor separately and splits setting act reference from establishment evidence |
| V1-A D-07 (R-8) | Grant **scope** element added to the grant, each display state and settings-in |
| V1-A D-08; V1-B D-07 (R-3.6, R-8) | Two settings references per operation; queued proposal unaffected by narrowing; not-yet-applied operation re-resolved at application; U-06 aligned |
| V1-A D-09 (R-5) | A checkpoint requiring A5 on an operation's result forces *propose*; F6 rewritten to an A4 checkpoint on applied rows |
| V1-A D-10 (R-5) | Negative branch: A10 for A5 checkpoints; decline/stop event for A4/A6/A7; dispositions waiting · performed · resolved negatively · lapsed · not reached · unknown |
| V1-A D-11 (R-5) | Checkpoint discharge requires capturing-surface evidence; faithful records are conformant shape |
| V1-A D-12; V1-B D-15 (R-4) | Facet renamed "host checks passed: ‹named checks›", each with evaluated basis; a check on an earlier basis shown historical; "later-check route" implies no act |
| V1-A §5 row 04-02 U-02 (D3) | Routine tool permission: App = user's Codex setting, hosts = none; grant governs host operations only; still not shown as a grant |
| V1-A AB-01 | *Unconfirmed* rule now DERIVED from R-8 (direct only when effective direct); host enforcement stays the host's |
| V1-A AB-04 | Consequence vocabulary carried as a scope slot; open with DEL-04-01 |
| V1-B D-06 (R-8) | Direct branch only in the *effective* direct state; origin records the display state |
| V1-B D-10 (R-6) | Acceptance unit = change item; row labels map to change items |
| V1-B D-11 | *Not set* and *refused (reason)* added to settings-in |
| V1-B D-13 | Record-out fields consumed (bound subject, c₀/c₁ with method, recording mode, evidence references, act class, checkpoint events) |
| V1-B D-14 | Lapse vocabulary adopted from RS-v0.2 §7; *not yet evaluated* never shown as not lapsed |
| V1-B D-17, D-18 | Origin elements per DEL-03-02; undo is a change through the one route, *undone* = applied (receipt) |
| V1-B D-20 (R-9) | Fixtures use FX-PIPE-01 and DEL-03-01 operation references; local divergences stated |
| V1-B §4 X-03 | Settings version in force at application: host-reported or *unconfirmed* |
| V1-C D-11, D-12 (R-7) | Outcome display adopts DEL-03-02 §9 incl. application error effect; item dispositions; outcome unknown attributed to its reporter |

## 0. Reading this definition

- Element and state names are **semantic, not wire names**. No field
  spelling, type, transport, persistence, placement, layout or timing
  threshold is selected (SoW REQ-006; OI-013; OI-014).
- **Act names are canonical (R1_RESOLUTIONS R-1):** A1 propose · A2 apply ·
  A3 examine · A4 mark checked · A5 accept · A6 approve (engineering approval
  only) · A7 rely · A8 request · A9 record · A10 reject · A11 withdraw · A12 set
  grant · A13 enable external access · A14 answer tool permission.
- **Labels (R-4):** unqualified "checked" means only A4; host results say
  "host checks passed: ‹named checks›"; agent work is "examination" /
  "findings"; "approval" means only A6; harness tool-use prompts are "tool
  permission" (A14); "accept" is A5 only.
- Examples use the invented model **FX-PIPE-01**; they are **fixture
  subjects**.

## 1. Settled distinctions relied on

| # | Settled distinction | Citation |
|---|---|---|
| S1 | The person sets, per class of operation, direct application or proposal within a scope the person sets; the setting is visible, changeable during work and recorded with each run | V4-HI-40; V4-AUT-01 |
| S2 | Conservative defaults for consequential operations; SWB model changes default to proposal with row / multi-row / whole-batch acceptance; the person may widen | V4-HI-41 |
| S3 | Declared checkpoints override autonomy: the run waits for the person's act | V4-HI-42 |
| S4 | Direct application is marked with origin, can be undone and can be checked later | V4-HI-22; V4-AUT-01 |
| S5 | `success` means it ran; a submitted proposal is "queued" until the host records acceptance and application | V4-HI-25 |
| S6 | Results carry standing — current/historical, checks passed, known limitations — never presented with more confidence than the host gives | V4-HI-12; V4-AUT-02 |
| S7 | A human act binds to content and lapses visibly when that content changes | V4-HI-32 |
| S8 | "accept", never "approve", for proposals | V4-HI-33 |
| S9 | No fabricated human act; faithful recording of a performed act is permitted | V4-HI-31; d3 |
| S10 | Acts are distinct; no universal acceptance-first chain | d3; V4-AUT-03 |
| S11 | Nothing agent-produced is shown as certified, sealed, approved or code-compliant | V4-AUT-05 |
| S12 | Every request answered or explicitly declined; silence never implies approval; unobserved outcomes are unknown | V4-EXE-02/03 |
| S13 | Reserved to the person: A4; A5 wherever autonomy requires a proposal; A6; A7; A12 and A13. No grant widens past a reserved act or declared checkpoint. The host names and enforces its own list; SWBPIPE adoption is not shown | OWNER_DECISIONS D2; V4-HI-30; DEP-001 |
| S14 | App routine tool-permission/sandbox modes are the user's own Codex setting, governing tool execution only; hosts have no classifier mode in the first increment; the SWB default proposal mode applies | OWNER_DECISIONS D3 |

## 2. Grant model received

Received from DEL-04-01; this deliverable renders and exchanges it.

- **Grant** (semantic): for each operation class *k*, a treatment *t(k)* ∈
  {direct, propose} within a **scope** *σ*, set by the person (A12).
  Scope dimensions are representation-neutral: model/workspace, object set,
  run, period, consequence (R-8). The consequence vocabulary is open (U-02).
- **Governs host operations only** (R-2 D3 bullet). Routine tool permission
  (A14) is the App user's own Codex setting (S14) and is not shown as a grant;
  hosts have none.
- **Policy bound (S13).** An agent never performs A4–A7, A12 or A13; a grant
  cannot widen past them or past a declared checkpoint. A catalog operation
  whose effect is to perform or record those acts as the person's carries class
  *reserved to the person* (R-2).
- **Model-change class** (SWB): *may apply within granted autonomy*, DERIVED
  from V4-HI-41, with accepted default setting *propose* and acceptance by
  row / multi-row / whole batch (acceptance unit = change item, R-6). Operation-
  specific additions await OI-021.
- **No policy basis** (operation-specific additions pending OI-021): direct not
  permitted, propose available (R-3.5). Shown as a class annotation, not a
  grant state.
- **Treatment resolution** happens on the host route at validation and again at
  application (R-3.1). A direct request without an *effective* direct treatment
  returns *not permitted* naming the governing treatment; it is never silently
  converted into a proposal (R-3.3).
- **Acceptance checkpoint forces propose** (R-5): if a declared checkpoint
  requires A5 on an operation's result, that operation's treatment is *propose*
  regardless of the grant; the display shows the override and its cause.

## 3. Grant display states

Per class and scope. Display is derived; the control (App or host) is the
authority for the current grant; the run record for what was recorded.

| State (R-8) | Entry evidence | Shown as | Direct branch? |
|---|---|---|---|
| **effective** | Control confirms the setting in force, and an A12 record of the person's setting exists (or the value is the policy default) | Treatment and scope | Yes, if treatment is direct |
| **requested by agent** | Agent A8 request; no person act | "Agent requests ‹t, σ›" beside the effective value | No |
| **set by person, not yet confirmed by control** | A12 record exists; control has not confirmed | "Set by you — not yet in force" | No — prior effective value governs |
| **unconfirmed** | Last-known value without current confirmation (reconnect, host unreachable, conflicting reports) | Last-known value labelled "unconfirmed" | No (DERIVED from R-8: direct only when effective direct) |
| **not set** | No setting and no default supplied | "not set" | No |
| **refused (reason)** | Control refused the person's setting | Reason, beside the still-effective value | No |

Transitions: agent A8 → *requested by agent* (no change to effective). Person
A12 → *set by person, not yet confirmed* → control confirms → *effective*;
control refuses → *refused (reason)* and the prior state stays; no answer →
remains unconfirmed-by-control, never promoted (S12). Any state → loss of
confirmation → *unconfirmed* → confirm → *effective*. An operation result
never moves a class to *effective* or widens it (REQ-001).

## 4. Checkpoint overlay

- Indicator per declared checkpoint, separate from the grant: **not reached** ·
  **waiting** · **performed** (act ⟨ref⟩) · **resolved negatively** (A10, or a
  decline/stop event for A4/A6/A7) · **lapsed** · **unknown** (R-5).
- *Reached* only on the declaration's observable *reached-when* condition; if
  the run ends without it, **not reached**, never satisfied.
- *Performed* requires a human-act record of the declared kind (A4, A5, A6, A7
  or A12) bound to the checkpoint's run-time subject referent, supported by
  attributable evidence from the **capturing surface** (host act facility for
  host content; App interface for App acts). A faithful record (A9) by another
  recorder is valid as a record and must cite that evidence. A direct grant,
  an operation success or A3 findings never discharge it.
- A decline/stop event is not an act of the declared kind; the declaration's
  "on negative decision" path governs next. Lapse of the performing act moves
  the indicator to **lapsed**; re-hold is DEL-02-03's.
- The grant display and the checkpoint indicator never merge into a single
  "allowed" signal.

## 5. During-work change sequence

1. Only the person changes the grant (A12, reserved, S13). An agent may prepare
   or ask (A8): display *requested by agent*; settings-in sends requester =
   agent, no setting actor, no A12 reference.
2. The person sets ‹t, σ› in the control: A12 record written; display *set by
   person, not yet confirmed*; settings-in sends requester = person, setting
   actor = person, setting act reference ⟨A12⟩.
3. Control establishes → new settings version ⟨set:n+1⟩, *effective*;
   settings-in sends establishment evidence. Control refuses → *refused
   (reason)*; settings-in sends the refusal.
4. In-flight effect (R-3.6; DEL-04-01 policy plus host enforcement, DEP-001):
   an already-queued proposal is unaffected; an operation not yet applied is
   re-resolved at application. Each operation carries two settings references
   — at route decision (validation) and in force at application (host-reported,
   otherwise *unconfirmed*).
5. Widening never converts a queued proposal into direct application or into
   acceptance (R-3.7). Narrowing never relabels an applied change's origin or
   route.

Failure behaviour: control unreachable → *unconfirmed*; conflicting App and
host reports → both shown, *unconfirmed*, defect observation returned; record
write fails → comparison *missing in record* (§6).

## 6. Settings-in / record-out exchange with DEL-04-03 (CASE-002 M3)

Identical to DEL-04-03/RS-v0.2 §8. A data exchange, not an ordering between
human acts and not a second record authority.

**Settings-in (DEL-04-02 → DEL-04-03 writer), per run and per change:** run
identity; settings version identity; **scope** (representation-neutral
dimensions, e.g. model/workspace, object set, run, period, consequence); per
operation class — treatment (direct / propose) and policy basis (DEL-04-01
record reference, or "no policy basis"); display state (effective · requested
by agent · set by person, not yet confirmed by control · unconfirmed · not set
· refused (reason)); **requester** (person, or agent via A8); **setting actor**
(the person, only where an A12 exists); **setting act reference** (A12 record);
**establishment evidence** (control confirmation) or refusal reason; order
relative to operation entries; source of control (App or host).

**Record-out (DEL-04-03 reader → DEL-04-02), per run:** record identity and
format version; recorded settings versions with the fields above; per
operation entry the two settings references, route, outcome, item
dispositions, receipt/origin references and evaluated/relied/current bases;
act and decline-event records with actor, recorder, **recording mode**, kind,
**act class**, **bound subject**, scope, purpose, **c₀/c₁ with method
designations**, lapse state and **evidence references with resolution
status**; **checkpoint events** (R8); evidence limits.

**Comparison (DEL-04-02)** per settings version: displayed vs recorded →
*match* · *mismatch* · *missing in record* · *missing in display*. Mismatch is
shown to the person and returned as a defect observation. The record is
authoritative for what was recorded; the control for the current grant; the
display is derived. Neither side auto-corrects the other. A person-set state
without an A12 reference is a defect, not an established setting.

## 7. Abstract host contribution for direct application

Per directly applied change (host implements; DEP-001; DEP-04-02-010). Not API
fields.

| Element | Meaning | Availability states shown | Never shown as |
|---|---|---|---|
| Origin reference | Host origin mark linked (not copied), compared with the request-side origin (author type, seat/role instance, channel, conversation, workflow run, grant display state at drafting, reason — DEL-03-02) | supplied · missing · mismatch (evidence limit) | Inferred from the App's request log |
| Undo route | Host-owned route to undo this change | offered · not offered · unknown | "Available" without a host-supplied route |
| Later-check route | Access for later examination or checking; implies no act (R-4) | offered · not offered · unknown | A performed A4 or A3 |
| Receipt reference | Host receipt; applied outcome associates item ↔ relied-on basis ↔ receipt ↔ resulting revision | supplied · missing · unresolvable | A copy; an acceptance |

**Undo interaction.** Person invokes the offered route → "undo requested" →
the undo is a change through the one route with its own origin, basis check
and outcome (V1-B D-18; DEL-03-02 to confirm at IR1): *undone* = applied
(receipt) · refused (reason) · application error (effect) · outcome unknown
(reporter, last observed state). Only *undone with receipt* is completed.

## 8. Result standing model

Separate facets, each no stronger than received (REQ-004). No synthesized
"verified" / "approved" label.

| Facet | Values | Source | Rule |
|---|---|---|---|
| Temporal | **current** · **historical** · unknown | Host standing; read basis (DEL-03-01) | Historical results carry the basis they describe |
| Host checks | **"host checks passed: ‹named checks›"**, each with its evaluated basis · none reported · unknown | Host result standing | A check evaluated on an earlier basis is shown **historical** beside a current result. Never labelled "checked" (R-4) |
| Limitations | **limited** (host-known limitations listed) · none reported · unknown | Host | Verbatim; not softened |
| Human acts | Act kind + actor + recorder + recording mode + lapse state: not lapsed · lapsed · lapsed (subject absent) · partially lapsed · matches c₀ again after observed lapse · unknown (incomparable) · unknown (unavailable) · not yet evaluated | DEL-04-03 record-out | *Not yet evaluated* never rendered as not lapsed; lapsed acts show original content (c₀) |
| Agent examination | A3 findings by reference | Agent (V4-EXM-21) | "Examination" / "findings", never a human act |
| Evidence completeness | complete as stated · **missing** (named) · **unknown** (unobserved outcome, attributed to its reporter) | Record-out evidence limits | Always visible |
| Route and outcome | direct under ⟨set⟩ · proposal with per-item dispositions; outcome per DEL-03-02 §9 incl. *application error* (effect none / partial / unknown) | DEL-03-02; record | Derived proposal state never stronger than its items; queued ≠ applied; applied ≠ accepted |

The person uses these facets to decide the validation warranted (V4-AUT-02);
the display makes no reliance decision.

## 9. Act-distinction display rules

- **DS-1** One label per canonical act kind; "accept" only for A5, "reject" for
  A10; "approval" only for A6 with its accountable person; "rely" for A7;
  "tool permission" for A14 (R-4).
- **DS-2** Actor and recorder both shown when they differ (A9, recording mode
  faithful recording).
- **DS-3** No act displayed without a received act record. Proposal, success,
  grant, receipt, findings, A8 request, A14 settlement, silence or timeout
  display as what they are.
- **DS-4** Absence of an A5 does not invalidate an independently evidenced
  act (e.g. A4 on the person's own edit).
- **DS-5** A decline/stop event is shown as a decline, never as the declined
  act.

## 10. Excluded acts and owners (REQ-007)

| Act | Owner |
|---|---|
| Define/carry adopted operation policy (incl. D2/D3 record) | DEL-04-01 |
| Record format, writer/reader, lapse handling | DEL-04-03 |
| Host controls, validation/application, origin marks, undo, receipts, host panel/loop; offering/recording/presenting host acts; enforcing its own reserved list | Responsible host owner; SWBPIPE outside session |
| OI-001 / OI-002 (App/shared level) | Decided by the Owner, DECISION-1 D2/D3; operation-specific additions: Owner via outside SWB session and App/shared owner (OI-021) |
| Resolve OI-013 | Shared contract owner with SWB implementation owner |
| Resolve OI-014 | App/shared contract owners |
| Set the grant (A12); enable external access (A13); perform any human act | The person |
| Professional reliance; certification, sealing, approval, code-compliance statements | Accountable professional |

## 11. Fixture scenarios (designed; fixture subjects)

Model **FX-PIPE-01**; operations per DEL-03-01 §10 as quoted in V1-B (OP-C3
check, OP-C4 add support, OP-C5 model change, OP-C6 mark row checked).
**Local divergence (R-9):** row labels S-1…S-5, proposal P-2 and settings
⟨set:n⟩ are local; the shared v0.2 timeline was under concurrent repair and is
aligned at IR1. "OP-X" is a placeholder for an operation-specific addition
pending OI-021.

| F | Scenario | Expected display / exchange |
|---|---|---|
| F1 | Run start ⟨set:1⟩: OP-C4/C5 effective *propose* (default), scope "FX-PIPE-01, this run"; OP-X has no policy basis; OP-C6 reserved | OP-C4/C5 *effective: propose*; OP-X "no policy basis — propose available, direct not permitted"; OP-C6 not grantable |
| F2 | Person A12 widens OP-C4 to direct, scope "S-1…S-5, this run"; control confirms ⟨set:2⟩ | *set by person, not yet confirmed* → *effective*; settings-in: A12 ref, then establishment evidence; record-out *match* |
| F3 | Agent A8 asks to widen OP-C5 | *requested by agent*; no A12; agent still proposes |
| F3b | Person sets; control refuses ("scope exceeds model lock", fixture reason) | *refused (reason)*; prior effective stays; refusal in settings-in |
| F4 | Host unreachable after F2 | OP-C4 → *unconfirmed*; direct not permitted; record shows unconfirmed interval |
| F5 | Record write for ⟨set:2⟩ fails | *missing in record* surfaced |
| F6 | Checkpoint requiring A4 on rows applied by direct OP-C4 | *waiting* until A4 act ref with capturing-surface evidence; direct grant does not discharge; a decline → *resolved negatively* (decline), not performed |
| F6b | Checkpoint requiring A5 on OP-C4's result while OP-C4 is effective direct | Treatment forced to *propose* for that operation, cause shown |
| F7 | Direct OP-C4 with origin, undo, later-check route, receipt | All supplied; undo *undone* only on receipt |
| F8 | Direct change with no undo route and lost acknowledgement | Undo *not offered*/*unknown*; outcome unknown, reporter loop; in-force settings *unconfirmed* |
| F9 | Results: current + "host checks passed: spacing (r13)"; the same check at r12 beside an r13 result; historical; limited; A4 partially lapsed; application error (partial) | Each facet as received; r12 check shown historical; lapse with c₀; partial effect with receipts |
| F10 | Distinctions: A9 faithful record of engineer's A4; proposal only; success only; grant only; findings only; A14 answered by user's Codex mode; A4 without A5 | Positive shows actor and recorder; negatives show no act; A14 not shown as grant or act |
| F11 | Agent requests direct application of OP-C5 while effective *propose* | *not permitted* naming ⟨set:1⟩ and the policy record; no proposal silently created |
| F12 | ⟨set:2⟩ narrowed while P-2 queued and a direct OP-C4 not yet applied | P-2 unchanged; the OP-C4 re-resolved at application → not permitted; two settings references shown |

## UNRESOLVED

| Item | Owner | Point of need | Effect on this definition |
|---|---|---|---|
| U-01 Operation-specific reserved additions and class assignments `OI-021` | Owner via outside SWB session and App/shared owner | Before connected-activity SoW and execution | "No policy basis" annotation for pending operations |
| U-02 Consequence vocabulary (scope dimension; classes) | DEL-04-01 with host policy owner (V1-A AB-04) | Before class assignment in DEL-03-01 | Consequence carried as a scope slot |
| U-03 Supplier v0.2 elements taken from R1_RESOLUTIONS (R-1, R-3…R-9) | DEL-04-01, DEL-03-02, DEL-03-01, DEL-02-01 | IR1 | Names, states and outcomes confirmed or repaired at IR1 |
| U-04 Host enforcement of *unconfirmed* and of re-resolution at application | Responsible host owner (DEP-001) | Before connected integration | App display rule DERIVED; host behaviour unevidenced |
| U-05 Host origin, undo, later-check route, receipt, host check basis supply `DEP-001` | SWBPIPE outside implementation session | Before corresponding connected-journey integration/examination and fallback-replacement decision | All host elements are fixture |
| U-06 Settings version in force at application (host-reported) | Responsible host owner (DEP-001; V1-B X-03) | Before connected integration | Displayed *unconfirmed* unless reported |
| U-07 Host capture requirement per act kind | Host owner (DEP-001; V1-A AB-06) | Before host act-recording integration | Faithful records shown as conformant shape |
| U-08 Component placement / host panel assembly `OI-014`, `OI-013` | App/shared contract owners; shared contract owner with SWB implementation owner | Before structural/production contract allocation (OI-014); before shared/host implementation boundary contracts (OI-013) | OUT-001 components only "where justified" |
| U-09 Mixed item decisions at an acceptance checkpoint (V1-C AB-01) | DEL-02-01 with DEL-02-03 and DEL-03-02 | Before VC-07/VC-09 and FX-C fixtures | §4 shows item dispositions; checkpoint verdict for mixed items open |
| U-10 Record representation for the exchange | DEL-04-03 (RS-v0.2 U-04) | Before writer implementation | Exchange is semantic only |
| U-11 Register edges to DEL-03-02, DEL-05-01, DEL-05-02 (V1-A RF-05; V1-B RF-01, RF-06; V1-C RF-4/RF-5) | Register owner at C1 | Closeout C1 | Receivers listed in header as pending register repair |

## Verification cases (designed, not run)

| Case | Input | Expected result | Serves |
|---|---|---|---|
| VC-01 Scope before/after change | F1, F2 | Visible treatment and scope equal the effective grant before and after | VER-001 (AC-001) |
| VC-02 Agent request and refusal are not grants | F3, F3b; a success in a propose class | No widening shown; success changes no state | VER-001 (AC-001) |
| VC-03 Checkpoint not discharged by autonomy | F6, F6b | Waiting until capturing-surface-evidenced act; decline shown as resolved negatively; A5 checkpoint forces propose | VER-001 (AC-001) |
| VC-04 No direct conversion | F11 | *not permitted* with governing treatment; no proposal created | VER-001 (AC-001) |
| VC-05 Settings-in / record-out match | F2 | Displayed and recorded versions match with scope, requester, setting actor, A12 reference | VER-002 (AC-002) |
| VC-06 Missing / unconfirmed / in-flight | F4, F5, F12 | *unconfirmed*, *missing in record* explicit; two settings references; queued proposal unchanged | VER-002 (AC-002) |
| VC-07 Origin/undo/later-check present | F7 | Four elements traced to host fixture evidence; undo completed only with receipt | VER-003 (AC-003) |
| VC-08 Absent host capability | F8 | Undo not offered/unknown; outcome unknown with reporter; nothing counted as available | VER-003 (AC-003) |
| VC-09 Standing facets | F9 | Each facet equals supplied evidence; earlier-basis check shown historical; lapse and unknown visible; no synthesized label | VER-004 (AC-004) |
| VC-10 Act distinctions and labels | F10 | Positive faithful record; negatives show no act; labels per R-4; A14 not a grant | VER-005 (AC-005) |
| VC-11 Owner and open-choice trace | §10, UNRESOLVED | Each REQ-007 act traced to owner; D2/D3 cited to DECISION-1; OI owners/points of need match register; no host delivery claimed | VER-006 (AC-006) |
| VC-12 Suite coverage | VC-01…VC-10 | Each AC-001…AC-005 covered; results bound to identified candidate; local results separate from host witness | VER-007 (AC-007) |
