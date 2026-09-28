# Autonomy and Standing Exchange
- Contribution: DEL-04-02/AS-v0.3
- Status: DRAFT DEFINITION — proposed, unsupplied, not implemented, not accepted
- Serves: OUT-002 (receiving-interface contract content); OUT-001 and OUT-003 (component behaviour and fixture design only — no component or fixture exists); REQ-001…REQ-007; AC-001…AC-007 via designed VER-001…VER-007
- Basis: repo 6e18505e3 (accepted basis); ScopeOfWork.md sha256 23a28caabd61da20dc2efed722f7e487856ef4488ab4f3454be4ed3249725e21; `P/docs/PRD.md` §4.3 V4-EXE-01…03, §4.5 V4-AUT-01…05, §4.6 V4-PM-06, §4.7 V4-REC-01…05; `P/docs/HOST_INTEGRATION.md` §1, V4-HI-04, V4-HI-11/12, V4-HI-20…25, V4-HI-30…33, V4-HI-40…42, V4-HI-50…52, V4-HI-70/71, §11; `P/docs/ARCHITECTURE.md` §4, V4-ARC-20; `P/docs/EXAMINATION.md` V4-EXM-21/22; `P/docs/OPERATING_METHOD.md` V4-OPS-30…32; `DECISION_BRIEF.html` d2, d3; `OWNER_DIRECTIONS.md` J, O; `SCC-CASE-002/Case_Datasheet.md` M1, M3; `_Decomposition/Open_Issues.csv` OI-001/002/013/014/021; `External_Dependencies.csv` DEP-001. Run folder `APP-V4-FIRST-INCREMENT-20260928`: `OWNER_DECISIONS.md` (DECISION-1; sha256 f3f8e5f31ec87006fc9ab459c6ae57d08638439c234fa959ba2605914cf81f2e); `R1_RESOLUTIONS.md` (2f9c7e72aa8362624ad830377a70077b27a27bf03871f8e87811a28e6e177ec4); `R2_RESOLUTIONS.md` (77cfb845ec305365f12218f83f332069155de5f362139b7a6fe2bf12cdebd088); `reviews/IR1-A.md` (31b3c7f8493f05ee5fed6a11208f6811d2449d8a4fe72aae6300c2850b648284), `IR1-B.md` (70e4a4f6d88f475687a9fde56a566a6913081dd3dd560402c1db8996dffd2846), `IR1-C.md` (295e96b3f5871cdf4142df169dc8811cef0aa38e7a7eb1930b246f60f0a426b9); V1-A/B/C as cited in AS-v0.2
- Consumed inputs: DEL-04-02/AS-v0.2 (sha256 3a4e8b01366c229c463f805aef402edd378a9491ed692f778b89b94a777a329c, commit c387730fb); DEL-04-03/RS-v0.3 (aligned concurrently by the same executor; its §8 is byte-identical to §6 here). Sibling v0.2 text read from commit **28bd00499** (`git show`, not the working tree): DEL-03-01/C-v0.2 sha256 358182b18b1fe13f9af6e6f5a61c9ed57f91b6ab29ea0c9adab06fe0081d6d82 (§4.1, §5.3, §6.2, §10); DEL-03-02/P-v0.2 sha256 942c1a3ab5ad7bda865640067f0fd550d7cfd1acd8f6ee228f6906452adf8c89 (§3.3, §4, §9); DEL-04-01/ACT-POLICY-v0.2 sha256 e50f1fe2f5bb2e3280bc62175e5aeeaa4508eed713424d82c54536a9fb5993a9 (§2, §4, §5.4–§6, §8). Where R2 amends those texts (R2-1…R2-21) the ruling is applied and marked "per R2-n"; sibling v0.3 text was not read.
- Receivers: CASE-002 M3 — DEL-04-03 (OUT-001/002; REQ-002; VER-001) receives settings-in; DEL-04-02 compares under OUT-003; REQ-002; VER-002. DEP-04-02-009 (DEL-04-03 downstream). DEL-03-02 (direct-branch entry; P §4.4), DEL-05-01 (grant in force per dispatch) and DEL-05-02 (active scope display) — register edges pending at C1. Host builder via DEL-03-04 and the external SWBPIPE owner through human relay (DEP-04-02-010) — as questions, not assignments.

## Changes from v0.2

The v0.1 → v0.2 change table is preserved in AS-v0.2 at commit `c387730fb`.

| Item | Change in v0.3 |
|---|---|
| R2-1; IR1A-01 | Five class values; **no policy basis** with *reason*, INTEGRATION (§0, §2) |
| R2-2; IR1A-08 | Reserved operations are those that **perform** A4, A5, A6, A7, A10, A12 or A13 (§2) |
| R2-3; IR1A-16 | Disabling external access recorded as A13, INTEGRATION (§0, §2) |
| R2-4; IR1A-02, IR1A-10 | Reserved entries always offered; agent call → *not permitted* with an A8 **offered** (F11b) |
| R2-5; IR1A-03, IR1A-18; IR1C-06, IR1C-08 | **Act-declined event** for A4, A6, A7, A12 → *resolved negatively*; **run-ended event** separate, checkpoint stays *waiting*; post-end acts (§4, DS-5, F14) |
| R2-6; IR1A-05 | Display state **effective (policy default)**, no A12; settings-in slot for policy-class record and default; *not set* = no setting and no default (§3, §6, F1) |
| R2-7; IR1A-04, IR1A-13 | A12 binds to setting content; later A12 **supersedes**; *superseded* in the human-act facet; checkpoint performed by earlier A12 stays performed (§5, §8, F15) |
| R2-8 | A14 never shown as a grant or act; recorded only in RS R13 (§2) |
| R2-9; IR1A-17 | No policy basis: direct *not permitted*; A12 widening refused (reason: no policy basis); fixtures **held** (§2, F3b) |
| R2-12; IR1-B X-9 | Direct request under a governing checkpoint constraint → *not permitted* naming the constraint; not a conversion; F6b **AWAITING INPUT** until host evidence (§2, §4, F6b) |
| R2-15; IR1-B B-m3 | Route/outcome facet shows **"applied, then reversed by ⟨receipt⟩"**; undo relation *reverses ⟨receipt⟩*; acts on content the undo changes lapse (§7, §8) |
| R2-16; IR1A-11; IR1-B B-m13/X-8 | Display **"accepted by ‹person› — not applied: refused — stale (relied ‹B›, current ‹B′›)"**; A5 not lapsed (§8, F13) |
| R2-17 | Checkpoint subject class shown independently of reached-when; includes held-call targets and grant setting (§4) |
| R2-18 | Mixed items: per-item *partial* annotation; item-left events shown; never "all accepted" over a reduced subject (§4) |
| R2-19; IR1A-09; IR1C-07 | Lapse before resume → "waiting — lapsed at ‹t›"; *lapsed* standing disposition only for ended runs (§4) |
| R2-21; IR1A-07; IR1-B B-M8, X-6 | Fixtures re-pointed to C-v0.2 §10 identifiers plus OP-C10/OP-C11; local cases `L-AS-n`; **F9 no longer calls the OP-C3 examination "host checks passed"** — uses T1 host checks "equilibrium", "unit consistency" and T4 A3 findings (§11) |
| IR1-B B-m13 | §8 lists the non-success outcomes shown (not offered, unavailable, not exposed, channel not enabled, not permitted, refused — invalid / stale, application error, outcome unknown with observer) |
| IR1A-14 | "Treatment (direct / propose)" for the grant renamed **grant value**; *treatment* reserved for host resolution |
| IR1A-20 | SoW TBD-001/002 still read OI-001/OI-002 as open — C1 pointer (finding only) |
| IR1A-21 | U-03 closed as confirmed by IR1 except as amended by R2 |

## 0. Reading this definition

- Element and state names are **semantic, not wire names**. No field
  spelling, type, transport, persistence, placement, layout or timing
  threshold is selected (SoW REQ-006; OI-013; OI-014).
- **Act names (DEL-04-01 §2.1):** A1 propose · A2 apply · A3 examine · A4 mark
  checked · A5 accept · A6 approve · A7 rely · A8 request · A9 record · A10
  reject · A11 withdraw · A12 set grant · A13 enable external access · A14
  answer tool permission.
- **Labels (R-4):** unqualified "checked" means only A4; host results say
  "host checks passed: ‹named checks›"; agent work is "examination" /
  "findings"; "approval" means only A6; "tool permission" is A14; "accept" is
  A5 only.
- **Class values (R2-1):** none · may apply within granted autonomy · proposal
  only · reserved to the person (SETTLED, V4-HI-02) · **no policy basis** with
  reason ∈ {omitted, unassigned, pending OI-021} (INTEGRATION).
- **Grant value** (direct / propose) is what the person sets; **treatment** is
  what the host route resolves (IR1A-14).
- Examples are **fixture subjects** from DEL-03-01 §10 (FX-PIPE-01).

## 1. Settled distinctions relied on

| # | Settled distinction | Citation |
|---|---|---|
| S1 | The person sets, per class of operation, direct application or proposal within a scope the person sets; visible, changeable during work, recorded with each run | V4-HI-40; V4-AUT-01 |
| S2 | Conservative defaults for consequential operations; SWB model changes default to proposal with row / multi-row / whole-batch acceptance; the person may widen | V4-HI-41 |
| S3 | Declared checkpoints override autonomy: the run waits for the person's act | V4-HI-42 |
| S4 | Direct application is marked with origin, can be undone and checked later | V4-HI-22; V4-AUT-01 |
| S5 | `success` means it ran; a proposal is "queued" until the host records acceptance and application | V4-HI-25 |
| S6 | Results carry standing — current/historical, checks passed, known limitations — never presented with more confidence than the host gives | V4-HI-12; V4-AUT-02 |
| S7 | A human act binds to content and lapses visibly when it changes | V4-HI-32 |
| S8 | "accept", never "approve", for proposals | V4-HI-33 |
| S9 | No fabricated human act; faithful recording of a performed act is permitted | V4-HI-31; d3 |
| S10 | Acts are distinct; no acceptance-first chain | d3; V4-AUT-03 |
| S11 | Nothing agent-produced is shown as certified, sealed, approved or code-compliant | V4-AUT-05 |
| S12 | Every request answered or explicitly declined; silence never implies approval; unobserved outcomes are unknown | V4-EXE-02/03 |
| S13 | Reserved to the person: A4; A5 wherever autonomy requires a proposal; A6; A7; changing the grant (A12); enabling external access (A13). No grant widens past a reserved act or declared checkpoint. The host names and enforces its own list; SWBPIPE adoption is not shown | OWNER_DECISIONS D2; V4-HI-30; DEP-001 |
| S14 | App routine tool-permission/sandbox modes are the user's own Codex setting per project/turn and govern tool execution only; hosts have no classifier permission mode in the first increment; the SWB default proposal mode applies | OWNER_DECISIONS D3 |

## 2. Grant model received

Received from DEL-04-01 §5 and §8; this deliverable renders and exchanges it.

- **Grant** (semantic): for each operation class *k*, a **grant value**
  ∈ {direct, propose} within a **scope** *σ* (dimensions: model/workspace,
  object set, run, period, consequence — representation-neutral; R-8), set by
  the person through **A12**. The consequence vocabulary is open (U-02).
- **Governs host operations only.** Routine tool permission (A14) is the App
  user's own Codex setting (S14) and is never shown as a grant or an act; it is
  recorded only in RS R13 (R2-8). Hosts have none.
- **Reserved.** ADOPTED by D2: A4, A5 (where autonomy requires a proposal),
  A6, A7, A12, enabling external access. DERIVED: A10 wherever A5 is (R-1); any
  operation that **performs** A4, A5, A6, A7, A10, A12 or A13 (R2-2).
  INTEGRATION: disabling external access is also a person's A13 (R2-3). No grant
  widens past these. Reserved entries are always offered to the agent; a call
  returns *not permitted* with an A8 **offered** — never withheld, never "not
  exposed" or "unavailable" for a class reason (R2-4).
- **Model-change class** (SWB; DEL-04-01 P-03): *may apply within granted
  autonomy* (DERIVED from V4-HI-41), default grant value *propose*, acceptance
  by row / multi-row / whole batch with the change item as unit (R-6).
  Operation-specific additions await OI-021.
- **No policy basis** (INTEGRATION, R-3.5; R2-9): proposing stays available
  but confers no permission — any effect needs the person's A5 and host
  application. Direct is *not permitted*; an A12 widening the class is
  **refused (reason: no policy basis)**. Shown as "no policy basis — held
  (reason)". Fixtures report **held**, never pass.
- **Treatment resolution** is on the host route at validation and again at
  application (R-3.1). A direct request without an *effective* direct grant
  value is *not permitted* naming the governing treatment; never silently
  converted into a proposal (R-3.3).
- **Governing checkpoint constraint** (R2-12): if a declared checkpoint
  requires A5 on an operation's result, the dispatch carries {workflow run,
  checkpoint name, required act A5, operation}; a direct request under it is
  *not permitted* naming the constraint as the governing treatment. The display
  shows the constraint and its cause. Whether the host receives the constraint
  or evaluates its own copy is a relay question (U-12).

## 3. Grant display states

Per class and scope. Display is derived; the control (App or host) is the
authority for the current grant; the run record for what was recorded.

| State (R-8; R2-6) | Entry evidence | Shown as | Direct branch? |
|---|---|---|---|
| **effective** | A12 record of the person's setting **and** control confirmation | Grant value and scope, "set by you" | Yes, if grant value is direct |
| **effective (policy default)** | Policy-class record with a default value; no A12 required; no setting actor, no requester | Default value, "policy default (‹record›)" | Only if the record's default is *direct* — none exists in the first increment |
| **requested by agent** | Agent A8 request; no person act | "Agent requests ‹value, σ›" beside the effective value | No |
| **set by person, not yet confirmed by control** | A12 record; no control confirmation yet | "Set by you — not yet in force" | No — prior state governs |
| **unconfirmed** | Last-known value without current confirmation (reconnect, host unreachable, conflicting reports) | Last-known value, "unconfirmed" | No |
| **not set** | No person setting and no policy default | "not set" | No |
| **refused (reason)** | Control refused the person's A12 (e.g. "no policy basis") | Reason beside the still-governing state | No |

Transitions: agent A8 → *requested by agent* (governing state unchanged).
Person A12 → *set by person, not yet confirmed* → confirm → *effective*;
refuse → *refused (reason)*; no answer → remains unconfirmed-by-control, never
promoted (S12). Any state → loss of confirmation → *unconfirmed*. A later A12
on an overlapping class and scope supersedes the earlier one (R2-7). An
operation result never moves a class to *effective* or widens it (REQ-001).

## 4. Checkpoint overlay

- Indicator per declared checkpoint, separate from the grant: **not reached** ·
  **waiting** · **performed** (act ⟨ref⟩) · **resolved negatively** (A10, or an
  **act-declined event** for A4, A6, A7 or A12) · **lapsed** · **unknown**.
- The **subject class** is shown as its own element, independent of the
  reached-when kind (R2-17): change items of a named proposal · named output ·
  objects changed by a named outcome · targets of the held call · grant
  setting. An A5 checkpoint uses reached-when *proposal queued* and its subject
  is that proposal's change items.
- *Reached* only on the declared observable condition; a run ending without it
  → **not reached**.
- *Performed* requires a human-act record of the declared kind bound to the
  subject referent, supported by **capture evidence** from the capturing
  surface (host act facility for host content; App interface for App acts). A
  faithful record by another recorder is valid as a record and must cite that
  evidence. A grant, an operation success or A3 findings never discharge it.
- **Negative.** An act-declined event → *resolved negatively*; the
  declaration's "on negative decision" path governs next (R2-5).
- **Run ended while waiting.** A separate **run-ended event** is shown; the
  checkpoint stays **waiting**. An act performed after the run ended is shown
  against the bound subject but does not change the ended run's disposition
  unless DEL-02-03 defines resumption (U-11).
- **Mixed items at an A5 checkpoint** (R2-18, PROPOSED per WD §4.3.7): each
  item shows A5, A10 or its **item-left** event (stale refusal, A11, host
  refusal); "partial" is a per-item annotation, not a disposition; a
  *performed* over a reduced subject is never shown as "all accepted".
- **Lapse** (R2-19): the performing act's lapse is shown as an **act-lapsed
  event**. Before resume the indicator returns to "waiting — lapsed at ‹t›".
  After resume, re-hold is DEL-02-03's (W7); until defined, the indicator shows
  "performed" with the act-lapsed event (U-13). *Lapsed* as a standing
  disposition appears only for a checkpoint whose run has ended.
- **A12 checkpoint**: a later A12 superseding the performing one leaves the
  checkpoint *performed*, with the supersession shown (R2-7). Whether an A12
  the control refused can count is held for DEL-02-03 (U-14).
- The grant display and the checkpoint indicator never merge into one
  "allowed" signal.

## 5. During-work change sequence

1. Only the person changes the grant (A12, S13). An agent may prepare or ask
   (A8): *requested by agent*; settings-in carries requester = agent, no
   setting actor, no A12 reference.
2. The person sets ‹value, σ›: A12 record bound to the **setting content**
   (classes, grant values, scope) (R2-7); display *set by person, not yet
   confirmed*; settings-in carries requester = person, setting actor = person,
   setting act reference ⟨A12⟩.
3. Control establishes → new settings version, *effective*; the version is a
   relation on the A12, not its content. Control refuses → *refused (reason)*,
   also a relation on the A12.
4. In flight (R-3.6; DEL-04-01 §5.5; host enforcement DEP-001): an
   already-queued proposal is unaffected; an operation not yet applied is
   re-resolved at application. Two settings references per operation: at route
   decision (validation) and in force at application (host-reported, otherwise
   *unconfirmed*).
5. Widening never converts a queued proposal into direct application or
   acceptance (R-3.7). Narrowing never relabels an applied change.

Failure behaviour: control unreachable → *unconfirmed*; conflicting App and
host reports → both shown, *unconfirmed*, defect observation returned; record
write fails → comparison *missing in record* (§6).

## 6. Settings-in / record-out exchange with DEL-04-03 (CASE-002 M3)

Identical to DEL-04-03/RS-v0.3 §8. A data exchange, not an ordering between
human acts and not a second authority.

**Settings-in (DEL-04-02 → DEL-04-03 writer), per run and per change:** run
identity; settings version identity; **scope** (representation-neutral
dimensions, e.g. model/workspace, object set, run, period, consequence); per
operation class — **grant value** (direct / propose) and **class value**
(DEL-04-01 policy-class record reference; for *no policy basis*, its reason);
display state (effective · effective (policy default) · requested by agent ·
set by person, not yet confirmed by control · unconfirmed · not set · refused
(reason)); **requester** (person; agent via A8; *none — policy default*);
**setting actor** (the person, only where an A12 exists; *none — policy
default*); **setting act reference** (A12 record) — or, for *effective (policy
default)*, the **policy-class record reference and its default value** in its
place; **establishment evidence** (control confirmation) or refusal reason;
order relative to operation entries; source of control (App or host).

**Record-out (DEL-04-03 reader → DEL-04-02), per run:** record identity and
format version; recorded settings versions with the fields above; per
operation entry the two settings references, route, treatment at resolution,
governing checkpoint constraint, outcome, item dispositions with actors,
receipt/origin references, resulting objects, *reverses* relations and
evaluated/relied/current bases; human-act records, act-declined events and
act-lapsed events with actor, recorder, recording mode, kind, act class, bound
subject, scope, purpose, c₀/c₁ with method designations, lapse or supersession
state and capture evidence references with resolution status; checkpoint
events with subject class, disposition and run-ended events; evidence limits.

**Comparison (DEL-04-02)** per settings version: displayed vs recorded →
*match* · *mismatch* · *missing in record* · *missing in display*. Mismatch is
shown to the person and returned as a defect observation. The record is
authoritative for what was recorded; the control for the current grant; the
display is derived. Neither side auto-corrects the other. A person-set state
without an A12 reference, or an *effective (policy default)* state without a
policy-class record reference, is a defect, not an established setting.

## 7. Abstract host contribution for direct application

Per directly applied change (host implements; DEP-001; DEP-04-02-010). Not API
fields.

| Element | Meaning | Availability states shown | Never shown as |
|---|---|---|---|
| Origin reference | Host origin mark linked, compared with the request-side origin (DEL-03-02 §3.3: author type, author identity, seat role meaning, channel, conversation, workflow identity and run, standing at drafting, settings references, reason, governing checkpoint constraint) | supplied · missing · mismatch (evidence limit) | Inferred from the App's request log |
| Undo route | Host-owned route to undo this change | offered · not offered · unknown | "Available" without a host-supplied route |
| Later-check route | Access for later examination or checking; implies no act (R-4) | offered · not offered · unknown | A performed A4 or A3 |
| Receipt reference | Host receipt; applied-outcome association item ↔ relied-on basis ↔ receipt ↔ resulting revision ↔ **resulting objects** (R2-14) | supplied · missing · unresolvable | A copy; an acceptance |

**Undo interaction.** The person invokes the offered route → "undo requested"
→ the undo is a change through the one route (DEL-03-02 §4.5; fixture OP-C10)
with its own origin, basis check and outcome: *applied (receipt)* with
**reverses ⟨receipt⟩** · refused (reason) · application error (effect) ·
outcome unknown (observer, last observed state). Only an applied undo with its
receipt is completed; the reversed change then shows **"applied, then reversed
by ⟨receipt⟩"**. The undo erases no act record; A5/A10 on the reversed item are
not lapsed; acts bound to content the undo changes lapse normally (R2-15).

## 8. Result standing model

Separate facets, each no stronger than received (REQ-004). No synthesized
"verified" / "approved" label.

| Facet | Values | Source | Rule |
|---|---|---|---|
| Temporal | **current** · **historical** · unknown | Host standing; read basis (DEL-03-01 §6.2) | Historical results carry their basis |
| Host checks | **"host checks passed: ‹named checks›"**, each with its evaluated basis · none reported · unknown | Host result standing | A check evaluated on an earlier basis is shown **historical**. Never "checked"; agent examination is never shown here |
| Limitations | **limited** (host-known limitations) · none reported · unknown | Host | Verbatim |
| Human acts | Act kind, actor, recorder, recording mode, and state: not lapsed · lapsed · lapsed (subject absent) · partially lapsed · matches c₀ again after observed lapse · unknown (incomparable) · unknown (unavailable) · not yet evaluated; for A12/A13: current · **superseded by ⟨act⟩** | DEL-04-03 record-out | *Not yet evaluated* never shown as not lapsed; lapsed acts show c₀ |
| Agent examination | A3 findings by reference (e.g. OP-C3) | Agent | "Examination" / "findings", never a human act or host check |
| Evidence completeness | complete as stated · **missing** (named) · **unknown** (unobserved outcome, with its **observer**) | Record-out evidence limits | Always visible |
| Route and outcome | direct under ⟨set⟩ · proposal with per-item dispositions and actors. Outcomes per DEL-03-02 §9 / DEL-03-01 §4.1: not offered (loop-side) · unavailable · not exposed on this surface · channel not enabled · not permitted (naming treatment, policy record or checkpoint constraint) · refused — invalid · refused — stale (relied and current bases) · queued · accepted · rejected · withdrawn · applied (receipt) · **applied, then reversed by ⟨receipt⟩** · application error (effect none / partial / unknown) · outcome unknown (observer) | DEL-03-02; record | Derived proposal state never stronger than its items; queued ≠ applied; applied ≠ accepted. Accepted then stale: **"accepted by ‹person› — not applied: refused — stale (relied ‹B›, current ‹B′›)"**, A5 shown not lapsed; a re-draft shows no carried acceptance (R2-16) |

The person uses these facets to decide the validation warranted (V4-AUT-02);
the display makes no reliance decision.

## 9. Act-distinction display rules

- **DS-1** One label per act kind; "accept" only for A5, "reject" for A10;
  "approval" only for A6 with its accountable person; "rely" for A7; "tool
  permission" for A14.
- **DS-2** Actor and recorder both shown when they differ (A9 faithful
  recording).
- **DS-3** No act displayed without a received act record with capture
  evidence. Proposal, success, grant, receipt, findings, A8 request, A14
  settlement, silence or timeout display as what they are.
- **DS-4** Absence of an A5 does not invalidate an independently evidenced act.
- **DS-5** An act-declined event is shown as "declined ‹act kind›", never as
  the act; a run-ended event is shown separately and resolves nothing.

## 10. Excluded acts and owners (REQ-007)

| Act | Owner |
|---|---|
| Define/carry adopted policy (incl. DECISION-1 records) | DEL-04-01 |
| Record format, writer/reader, lapse handling | DEL-04-03 |
| Host controls, validation/application, origin marks, undo, receipts, host panel/loop; offering/recording/presenting host acts; enforcing its own reserved list | Responsible host owner; SWBPIPE outside session |
| OI-001 / OI-002 (App/shared level) | Decided by the Owner, DECISION-1 D2/D3 (the SoW's TBD-001/002 still read open — C1 pointer, IR1A-20); operation-specific additions: Owner via outside SWB session and App/shared owner (OI-021) |
| Resolve OI-013 | Shared contract owner with SWB implementation owner |
| Resolve OI-014 | App/shared contract owners |
| Set the grant (A12); enable or disable external access (A13); perform any human act | The person |
| Professional reliance; certification, sealing, approval, code-compliance statements | Accountable professional |

## 11. Fixture scenarios (designed; fixture subjects)

Identifiers are DEL-03-01/C-v0.2 §10 (commit 28bd00499): FX-PIPE-01, R-100,
S-1…S-4, Engineer A, B1/B2, PR-1/PR-2, RC-1…RC-3, T1–T17, OP-C1…OP-C9, plus
**OP-C10 Undo** and **OP-C11** (*no policy basis*, pending OI-021) fixed by
R2-21. Settings versions are named by the step that establishes them
(⟨set-T15⟩). Local cases are `L-AS-n`, each saying why.

| F | Scenario | Expected display / exchange |
|---|---|---|
| F1 | Run start: OP-C4/C5/C9 class *may apply*, no A12; OP-C11 *no policy basis*; OP-C6/C7/C8 reserved | OP-C4/C5/C9 **effective (policy default): propose** with P-03 reference, no setting actor; OP-C11 "no policy basis — held (pending OI-021)"; OP-C6/7/8 reserved, offered |
| F2 | T15: Engineer A A12 → OP-C9 class direct, scope object set "support labels on R-100", model/workspace FX-W1; control confirms | *set by person, not yet confirmed* → **effective: direct**; settings-in A12 ref, then establishment evidence; record-out *match* |
| F3 | Agent A8 asks to widen OP-C4 to direct | *requested by agent*; no A12; OP-C4 stays effective (policy default): propose |
| F3b | Engineer A A12 widening OP-C11 to direct | **refused (reason: no policy basis)**; fixture result **held** |
| F4 | Host unreachable after T15 (L-AS-1: C has no outage step) | OP-C9 → *unconfirmed*; no direct branch |
| F5 | Record write for ⟨set-T15⟩ fails (L-AS-2: record-side failure, not on C's timeline) | *missing in record* surfaced |
| F6 | A4 checkpoint, subject class "objects changed by a named outcome" = T16 resulting objects (S-4 label) | *waiting* until an A4 with capture evidence; grant does not discharge; act-declined event → *resolved negatively* |
| F6b | A5 checkpoint on OP-C4's result while OP-C4 were effective direct (L-AS-3) | Direct request *not permitted* naming the governing checkpoint constraint; not converted. **AWAITING INPUT** until host evidence (R2-12) |
| F7 | T16 direct OP-C9 (RC-2, origin, undo route, later-check route); T17 OP-C10 undo → RC-3 reverses RC-2 | Four elements supplied; T16 change shown **"applied, then reversed by RC-3"** |
| F8 | T16 with acknowledgement lost (L-AS-4: C's T13 loss is on the proposal path) | Undo route *unknown*; outcome unknown, observer loop; settings at application *unconfirmed* |
| F9 | Standing: T1 host checks passed "equilibrium", "unit consistency" at r12; after T6 (r13) those results historical; T8 OP-C2 *unavailable*; T4 OP-C3 **A3 findings**; T2 A4 on S-2 not lapsed at r13, **lapsed** at T14 | Host checks shown with basis r12 and **historical** at r13; T4 shown as "agent examination — findings", **never "host checks passed"**; unavailable with reason; lapse with c₀ |
| F10 | Distinctions: T2 A4 (host capture) plus App-agent faithful record; T5 proposal only; T16 success; T15 grant only; T4 findings; A14 answered by user's Codex mode; A4 without A5 | Actor and recorder shown; negatives show no act; A14 not a grant or act |
| F11 | Agent requests OP-C4 directly while effective (policy default): propose | *not permitted* naming P-03 treatment; no proposal created |
| F11b | Agent calls OP-C6 "Mark row checked" | *not permitted*, A8 offered; no automatic A8 record |
| F12 | L-AS-5 (why: narrowing has no C step): after T15, a direct OP-C9 not yet applied when Engineer A's A12 narrows OP-C9 to propose | Re-resolved at application → *not permitted*; two settings references shown; queued PR-2 unaffected |
| F13 | L-AS-6 (declared divergence per IR1A-07): after T11, intervening edit to PR-2 item 1's target before application | "accepted by Engineer A — not applied: refused — stale (relied B2, current ‹B′›)"; A5 not lapsed |
| F14 | L-AS-7 (why: C has no declared checkpoints): A12 checkpoint on the agent-requested setting; Engineer A declines → act-declined event; variant: nobody acts and the run ends | *resolved negatively*; variant: **waiting** + run-ended event |
| F15 | L-AS-8: F12's A12 supersedes T15's A12, which performed an A12 checkpoint | T15 act shown **superseded**; checkpoint stays *performed* with supersession shown |

## UNRESOLVED

| Item | Owner | Point of need | Effect on this definition |
|---|---|---|---|
| U-01 Operation-specific reserved additions and class assignments `OI-021` | Owner via outside SWB session and App/shared owner | Before connected-activity SoW and execution | "No policy basis — held" for pending operations |
| U-02 Consequence vocabulary | DEL-04-01 with host policy owner | Before class assignment in DEL-03-01 | Scope slot only |
| U-04 Host enforcement of *unconfirmed*, re-resolution at application, de-duplication | Responsible host owner (DEP-001) | Before connected integration | App display rule DERIVED; host behaviour unevidenced |
| U-05 Host origin, undo, later-check route, receipt, resulting objects, host-check basis `DEP-001` | SWBPIPE outside implementation session | Before corresponding connected-journey integration/examination and fallback-replacement decision | All host elements are fixture |
| U-06 Settings version in force at application | Responsible host owner (DEP-001) | Before connected integration | *unconfirmed* unless reported |
| U-07 Host capture requirement and capture-evidence reference | Host owner (DEP-001; R2-20 relay) | Before host act-recording integration | Without it no host-content checkpoint reaches *performed* |
| U-08 Component placement / host panel assembly `OI-014`, `OI-013` | App/shared contract owners; shared contract owner with SWB implementation owner | Before structural/production contract allocation (OI-014); before shared/host implementation boundary contracts (OI-013) | OUT-001 components only "where justified" |
| U-09 Mixed item decisions at an A5 checkpoint (R2-18, PROPOSED per WD §4.3.7) | DEL-02-01 with DEL-02-03 and DEL-03-02 | W7 | Per-item display only |
| U-10 Record representation for the exchange | DEL-04-03 (RS U-04) | Before writer implementation | Semantic only |
| U-11 Resumption of an ended run; post-end acts | DEL-02-03 | W7 | Ended-run disposition unchanged |
| U-12 Host receipt of the governing checkpoint constraint (R2-12) | Host owner (relay) | Before connected integration | F6b AWAITING INPUT |
| U-13 Checkpoint display after lapse following resume | DEL-02-03 | W7 | "performed" + act-lapsed event |
| U-14 Whether a refused A12 counts at an A12 checkpoint (R2-7) | DEL-02-03 | W7 | Refusal shown as relation; checkpoint effect held |
| U-15 Register edges to DEL-03-02, DEL-05-01, DEL-05-02 | Register owner | Closeout C1 | Receivers listed as pending |

Closed in v0.3: U-03 (IR1A-21).

## Verification cases (designed, not run)

| Case | Input | Expected result | Serves |
|---|---|---|---|
| VC-01 Scope before/after change | F1, F2 | Visible grant value and scope equal the effective grant; default shown as *effective (policy default)* without A12 | VER-001 (AC-001) |
| VC-02 Agent request, refusal, no policy basis | F3, F3b; a success in a propose class | No widening; F3b refused and **held** | VER-001 (AC-001) |
| VC-03 Checkpoint not discharged by autonomy | F6, F6b, F14 | Waiting until capture-evidenced act; act-declined → resolved negatively; run-ended → waiting; F6b not permitted with constraint (AWAITING INPUT) | VER-001 (AC-001) |
| VC-04 No direct conversion; reserved entries offered | F11, F11b | *not permitted*; no proposal or A8 created automatically | VER-001 (AC-001) |
| VC-05 Settings-in / record-out match | F1, F2 | Match incl. scope, requester, setting actor, A12 or policy-record reference | VER-002 (AC-002) |
| VC-06 Missing / unconfirmed / in-flight | F4, F5, F12 | *unconfirmed*, *missing in record*; two settings references; queued proposal unchanged | VER-002 (AC-002) |
| VC-07 Origin/undo/later-check; reversal | F7 | Elements traced to host fixture evidence; "applied, then reversed by RC-3" only with RC-3 | VER-003 (AC-003) |
| VC-08 Absent host capability | F8 | Undo unknown; outcome unknown with observer; nothing counted as available | VER-003 (AC-003) |
| VC-09 Standing facets | F9, F13 | Each facet equals supplied evidence; r12 checks historical at r13; OP-C3 shown as findings, not host checks; stale-after-accept wording | VER-004 (AC-004) |
| VC-10 Act distinctions, labels, supersession | F10, F15 | Faithful record positive; negatives show no act; labels per R-4; A14 not a grant; superseded A12 shown, checkpoint stays performed | VER-005 (AC-005) |
| VC-11 Owner and open-choice trace | §10, UNRESOLVED | Each REQ-007 act traced; D2/D3 cited only for what they say; OI owners and points of need match register; no host delivery claimed | VER-006 (AC-006) |
| VC-12 Suite coverage | VC-01…VC-10 | Each AC-001…AC-005 covered; results bound to an identified candidate; held and AWAITING INPUT cases never counted as passes | VER-007 (AC-007) |
