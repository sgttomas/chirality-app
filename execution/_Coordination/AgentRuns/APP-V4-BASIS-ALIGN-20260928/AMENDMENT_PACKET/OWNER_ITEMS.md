# Owner items — APP-V4-BASIS-ALIGN-20260928, checkpoint K1 (scope-change groups 1 and 2)

## Summary for the owner's review (one page)

**What this packet does.** It brings the accepted App v4 basis in line with
three decisions you have already made. Nothing is applied until you accept
it.
- **Checkpoints are phased** (DECISION-4). Today a workflow's checkpoints are
  plan guidance: the act is still requested, and it is recorded as done only
  when you perform it, but nothing stops or blocks a run. Enforced holds are
  kept as a later layer for the workflows that need them. They are not
  deleted.
- **Model access** (DECISION-4). A host's agent runs on a local or a cloud
  model, whichever you choose. There is no default. A cloud model is reached
  by OAuth sign-in or an API key.
- **Network destinations** (DECISION-5). V4-HOST-02 takes your approved
  wording, word for word: the agent contacts only the model service you chose
  and destinations you allow, in advance or when it asks. Only you grant.
  Only stateless MCP is allowed. Nothing is contacted silently, and every
  destination is recorded and shown.

**Where it changes text.**
- The PRD, ARCHITECTURE, HOST_INTEGRATION and EXAMINATION requirements that
  state these three points.
- Eight scope rows, one vocabulary term and three deliverable descriptions in
  the decomposition that say the same things.
- 16 deliverable Scopes of Work. These also take the first closeout's
  corrections (74 proposals: 45 as written and 29 updated for these
  decisions), mostly pointing old "open" policy questions at your DECISION-1
  rulings.
- Two housekeeping fixes that the pre-change audit found in
  `SOFTWARE_DECOMP.md`:
  - it gains a `Decision Log` heading, so each amendment has a place the
    method can find;
  - a stale sentence that says no deliverable folders exist is corrected.

**Why now.** Design work since the first increment already follows these
decisions, but the accepted texts still say "the run waits", "local by
default" and "configured model server only". Later work would otherwise build
on words you have overruled.

**What you asked about: the four corrections that widen or sharpen scope
(O-9).** I recommend adopting all four:
- **S-01-4:** reads carry an identity for each object, or SWBPIPE's single
  model identity for all of them. Two other contracts already rely on this
  to detect stale proposals and lapsed acts.
- **S-01-5:** each operation says on which surface it is exposed. SWBPIPE's
  answers already use this idea.
- **S-02-3:** "a repeated submission has one effect" becomes "at most one
  effect per item — a host promise we test and record". The App cannot
  itself guarantee a fact about the host.
- **S-03-2:** the external channel states your D5 flexibility (content may
  reach the model you picked, with no gate) and the revised V4-HOST-02.

**Already decided (DECISION-6):**
- the 14 deliverables are IN_PROGRESS;
- the 41-arc set is accepted, with X-1 kept and the disputed arc left out
  (O-16, O-27 to O-30);
- the pre-change audit is done (O-20).

**What stays open after this.**
- Taking up the governance layer for enforced checkpoints: when, and for
  which workflows.
- Operation-specific reserved acts (OI-021).
- SWBPIPE host joins, deferred until you resume UI-SUCCESSOR.
- The DAG-002 acceptance at checkpoint B.
- The Design files' re-pinning to the amended texts.

**What you need to answer now.** Use the quick sheet below. "Accept the
remaining items as recommended" covers everything still open.

---

**Status: PROPOSED, revision 2** (after the pre-change baseline and owner
DECISION-6). These are the decisions the owner is asked to make at the
grouped checkpoint K1. Each has a concrete recommendation. Items marked
**required** are ones the scope-change contract reserves to the owner. The
others resolve conditional edits or confirm a reading. Items marked
**DECIDED** or **DONE** record what has already happened.

Evidence: [IMPACT_ASSESSMENT.md](IMPACT_ASSESSMENT.md),
[BASIS_AMENDMENT.md](BASIS_AMENDMENT.md),
[SOW_REVISIONS.md](SOW_REVISIONS.md). Node P2 prepares the register, arc and
DAG-002 items (including the disputed arc) separately.

## Quick answer sheet

If the owner accepts every recommendation still open, the reply can be:
"accept the remaining items as recommended". Declining an item drops only
the edits named against it. O-16, O-20 and O-27 to O-30 are already
decided or done.

| # | Decision | Recommendation | Required by |
|---|---|---|---|
| O-1 | Amendment identity | `SCA-V4-001`; first amendment | contract |
| O-2 | Scope of the change (group 1) | Accept: basis wording + decomposition rows + 16 SoWs | contract (group 1) |
| O-3 | Write boundary and application route (group 2) | Accept as listed; REVISE after group 3 | contract (group 2) |
| O-4 | V4-WF-05, V4-HI-42, V4-EXM-22 text | Accept | contract (group 2); DECISION-4 |
| O-5 | V4-HOST-01, V4-ARC-11 text | Accept | contract (group 2); DECISION-4 |
| O-6 | V4-HOST-02 (verbatim), V4-ARC-12, host-agent properties, V4-EXM-23 | Accept | contract (group 2); DECISION-5 |
| O-7 | Consequential basis edits | Accept | contract (group 2) |
| O-8 | "Local-first" in the purpose statement and PKG-05 | Amend both | owner's own text |
| O-9 | Four C1 items needing an owning decision | Adopt all four | C1 |
| O-10 | App records and shows the model destination (R5-4) | Confirm | C1 / R5-4 |
| O-11 | DEL-04-02 consumed and received directly | Direct | C1 (V1-A RF-05) |
| O-12 | PANEL consumes DEL-02-03 directly | Direct | C1 (S5-2-3 alternative) |
| O-13 | GUIDE consumes HOSTING, RELAY and XT | Adopt S-04-6 | C1 (S-04-6 / N-B9…N-B11) |
| O-14 | Host-agent destinations in the run record SoW | Adopt | DECISION-5 allocation |
| O-15 | DECISION-5 display in DEL-04-02 (arc R8-A) and other SoWs | Adopt the one DEL-04-02 sentence; no other change | P2 route (a) |
| O-16 | Lifecycle IN_PROGRESS for the 14 | **DECIDED** (DECISION-6): recorded, commit `67a2fac4b` | owner |
| O-17 | Open_Issues OI-001/OI-002 pointers | Include; status stays OPEN | C1 F-8 |
| O-18 | DEL-08-01 CLM-003 (Domains) | Include | consistency |
| O-19 | DEL-09-07 (V4-EXM-22/23 owner) | Include | consistency |
| O-20 | Pre-change baseline | **DONE**: `BASELINE/coverage_summary.json` sha256 `d8ac5c4d…`; 7 packages | contract (method step 5) |
| O-21 | Supersession bindings | Accept as SUPERSESSION | contract |
| O-22 | SoW frontmatter unchanged | Accept | REVISE step 3 |
| O-23 | `ScopeChanging` values | Accept as proposed | contract (group 2) |
| O-24 | Recording K1 as two decision snapshots | Accept | contract |
| O-25 | DECISION-1 D2 "or a declared checkpoint" in the current phase | Confirm the R8-11 reading | integration reading |
| O-26 | PRD V4-AUT-03/04 and OQ-02 "open detail" | Leave for a later update | — |
| O-27 | Disputed arc DEL-03-02 → DEL-04-03 | **DECIDED** (DECISION-6): not proposed | owner |
| O-28 | Arc X-1 from DEL-02-03 naming DEL-01-04 | **DECIDED** (DECISION-6): keep X-1 | owner |
| O-29 | Arc N-15 (RS consumes DEL-01-01 facts directly) | **DECIDED** (DECISION-6, 41-arc set): keep | owner |
| O-30 | Grounding route for P2's nine arcs | **DECIDED** (DECISION-6, 41-arc set): route (a), the SoW sentences drafted here | owner |

---

## A. Required by the scope-change contract

### O-1 · Amendment identity and posture — required

- **Question.** Which amendment ID should this first App v4 amendment take?
- **Facts.** `execution/_ScopeChange/` does not exist, so this is the
  `FIRST_AMENDMENT` posture: no `_LATEST.md` until group 3. The helper would
  give `SCA-001` (unqualified) or `SCA-V4-001` (prefix `V4`). App v4 records
  already cite chirality-app-dev's `SCA-APP-012`.
- **Recommendation.** **`SCA-V4-001`.** The ID is unambiguous across the
  projects that share this repository, and the contract admits a
  project-qualified form.

### O-2 · Scope of the change (checkpoint group 1) — required

- **Question.** Does the owner accept the proposed change and its impact
  (IMPACT_ASSESSMENT §§2–8)?
- **What it covers:**
  - the basis wording (A01–A17);
  - the matching decomposition rows (A18–A31): ScopeLedger SOW-015, -016,
    -017, -052, -137, -138, -201, -202; "Declared checkpoint";
    DEL-02-03/05-01/09-07 descriptions; a new `## Decision Log` section with
    the amendment entry (A30/D-15), which resolves the Change Register
    binding the baseline could not find (COV-127) without an owner ruling;
    the corrected no-production sentence (D-16, COV-121); the coverage
    recompute;
  - 16 SoW revisions (A32–A47).
- **Why the decomposition rows.** DECISION-4 notes that "a full scope change
  may not be needed". Without these rows, however, the Scope Ledger would
  state the old meanings ("wait", "defaults … local", "configured model
  server only"). The revised SoWs and the amended PRD would then cite a
  ledger that contradicts them.
- **Recommendation.** **Accept**, including the decomposition rows. All
  actions are MODIFY; no ID, mapping or count changes.

### O-3 · Write boundary and application route (checkpoint group 2) — required

- **Question.** Which files may the amendment write, and in what order is it
  applied?
- **Write boundary (named exactly):**
  - `docs/PRD.md`, `ARCHITECTURE.md`, `HOST_INTEGRATION.md`,
    `EXAMINATION.md`;
  - `execution/_Decomposition/SOFTWARE_DECOMP.md`, `ScopeLedger.csv`,
    `Vocabulary_Map.csv`, `Deliverables.csv`, `Consolidated_Coverage.csv`,
    and conditionally `Packages.csv` (O-8) and `Open_Issues.csv` (O-17);
  - the `_CONTEXT.md` of DEL-02-03, DEL-05-01, DEL-09-07, and DEL-05-02 (O-8);
  - the 16 `ScopeOfWork.md` files, applied only by `scope-of-work`
    MODE=REVISE, one brief per deliverable, closing with MODE=VERIFY.
- **Ordering tension.** The scope-of-work workflow says REVISE runs under an
  amendment with *group 3 accepted*. The graph applies after K1 (groups 1 and
  2).
- **Recommendation.**
  - Apply the docs, decomposition and `_CONTEXT.md` edits as the scope-change
    candidate poststate after K1.
  - Run the 16 REVISE briefs only after the owner accepts group 3.
  - Present group 3 (audited poststate) together with DAG-002 at K2, as the
    graph already plans.
- **Alternative.** Authorize the REVISE runs at K1 as candidate carrier
  writes. This is faster, but it departs from the scope-of-work
  precondition.

### O-4 · Phased-checkpoint text: V4-WF-05, V4-HI-42, V4-EXM-22 — required

- **Question.** Does the owner accept the exact text in BASIS_AMENDMENT A01,
  A12 and A15, and the matching SoW and ledger edits?
- **The text:**
  - the act is requested and recorded only when the person performs it;
  - holding the checkpoint is *phased to the governance layer, not
    withdrawn*;
  - in the current phase, neither the App nor a host's loop enforces a
    hold, blocks a run or reports *unsupported* for that reason;
  - the definitions are kept so that every workflow needing governance can be
    served;
  - reserved acts are unaffected.
- **Note.** The SoW text says "for a workflow that takes up the governance
  phase". It does not name WD's proposed `governed` flag, which is still
  PROPOSED.
- **Recommendation.** **Accept.** The text follows DECISION-4 D4-1 and its
  clarification point by point.

### O-5 · Model access text: V4-HOST-01, V4-ARC-11 — required

- **Question.** Does the owner accept A02 and A08?
- **The text.** Local or cloud, as the person chooses, with no default; a
  cloud model is reached by OAuth sign-in or an API key.
- **Recommendation.** **Accept** (DECISION-4 D4-3).

### O-6 · Network destinations: V4-HOST-02, V4-ARC-12, host-agent properties, V4-EXM-23 — required

- **Question.** Does the owner accept A03, A09, A10 and A16?
- **The text:**
  - V4-HOST-02 uses DECISION-5's wording verbatim (checked by script), with
    the PRD's usual "(D-18; DEC-5)" suffix;
  - the ARCHITECTURE host-agent properties carry the rest of DECISION-5: the
    two-level allow list; stateless MCP only (revision 2026-07-28);
    person-only grants scoped once, this run or always; only the requesting
    call waits; the decline message; the always-off list; record and show;
    the outside-process limit; the governance phase; and host agents only.
- **Recommendation.** **Accept.**

### O-7 · Consequential basis edits — required

- **Question.** Does the owner accept the edits that restate the same
  meanings elsewhere in the basis?
- **The edits:**
  - A04: PRD §2.2 intro, "local-first agent";
  - A05: PRD OQ-03;
  - A11: ARCHITECTURE §1 priority 3 and the diagram label;
  - A13: HOST_INTEGRATION §8.1 Domains paragraph;
  - A14: V4-HI-70, where the run record gains host-agent destinations;
  - A07 and A17: status notes and the DEC-4/DEC-5 source key.
- **Why.** Each would otherwise contradict A01–A16 inside the same accepted
  set.
- **Recommendation.** **Accept all.** A14 is the only edit that adds content,
  and it only names where DECISION-5's "recorded" lands.

### O-20 · Pre-change baseline (method step 5) — **DONE**

- **Done by node P3.** It ran `audit-decomp` over **PKG-01, 02, 03, 04, 05, 08
  and 09** (30 deliverables). PKG-01 is included because A41 modifies
  DEL-01-01. The GROUP3 audit was not reused because three inputs differ.
- **Output.** `BASELINE/coverage_summary.json`, sha256
  `d8ac5c4d35012d6a6fb6a3ef2c509caba08a616c8e14a5601bff2a83ee9620f9`.
  `overall_status` WARNINGS: 0 BLOCKER, 2 WARNING, 126 INFO.
- **The two warnings are addressed in this packet:**
  - COV-127 (Change Register binding): the new `## Decision Log` heading,
    D-15;
  - COV-121 (stale sentence): D-16.
- **Pre-existing findings.** COV-119/120 (stale telemetry) predate the
  amendment and close on the planned recompute (IMPACT_ASSESSMENT §9).
- **Post-change audit.** It uses the same seven-package scope, for a
  like-for-like comparison.

### O-21 · Supersession bindings — required

- **Question.** How should the bindings to the original seed be typed?
- **Facts.** The amended facts override original-seed facts of the accepted
  composite (IMPACT_ASSESSMENT §7, 11 rows).
- **Recommendation.** **Accept as `SUPERSESSION`.** For V4-WF-05 and V4-HI-42,
  the row notes that the original holds again for workflows in the
  governance phase. `SUPPLEMENTARY_EXTENSION` would understate the change for
  the current phase.

### O-23 · `ScopeChanging` values in the action register — required

- **Question.** Does the owner accept the values in IMPACT_ASSESSMENT §3.1?
- **The values.**
  - YES where a requirement or criterion changes meaning.
  - NO for pointer and wording lifts: DEL-04-01, DEL-04-02, DEL-01-01,
    DEL-08-01 and the notes.
- **Facts.** No deliverable is ISSUED, so no value authorizes a reopening.
- **Recommendation.** **Accept.**

### O-24 · Recording K1 — required

- **Question.** How is the single K1 act recorded?
- **Facts.** The contract requires two immutable snapshots:
  `SCA-V4-001_GROUP-1_{date}` and `SCA-V4-001_GROUP-2_{date}`, each with
  `DECISION.md`, `ACCEPTED_MANIFEST.csv` and `Handoff_State.md`. The group-2
  snapshot binds `Amendment_Actions.csv` by hash.
- **Recommendation.** **Accept.** One owner reply that addresses both
  subjects can be recorded in both snapshots.
- **Note.** DECISION-6 ("Checkpoint A", partial) answered only the lifecycle
  and the arc set. The owner's reply on the wording package was "I want to
  review the packet first". Groups 1 and 2 are therefore not yet accepted,
  and no group snapshot may be written from DECISION-6.

---

## B. C1 items that need an owning decision (CLOSEOUT_ACCOUNT)

### O-9 · Scope additions and protected criteria — four items, each adoptable separately

| C1 item | Edit | What it changes | Refresh | Recommendation |
|---|---|---|---|---|
| **S-01-4** DEL-03-01 REQ-004 (scope addition) | E-0301-04 | Each read row also carries a host-supplied subject content identity with its method designation | Amended for R8-4: a host's whole-model identity is received as each covered subject's identity; the App never computes identities. SWBPIPE supplies only that | **Adopt.** RS L-1 (lapse) and P's per-item stale rule depend on it; without it DEL-03-01 does not promise what two siblings consume |
| **S-01-5** DEL-03-01 REQ-002 (scope addition) | E-0301-05 | Adds host-declared exposure per consumer surface, independent of class | Kept. R8-5 now relies on it (SWBPIPE `unsupported_method` → "not exposed on this surface") | **Adopt** |
| **S-02-3** DEL-03-02 REQ-008 / AC-009 (protected criterion) | E-0302-03 | "Only one effect" becomes "at most one effect per change item, a host obligation made testable; an observed second effect is recorded as a failed obligation" | Kept | **Adopt.** The current wording promises a fact the App cannot establish (R-7) |
| **S-03-2** DEL-03-03 REQ-002 / AC-002 (protected criterion) | E-0303-02 | States D5 (content may reach the selected model; no gate; no added destination), App-side record and show, and the host's refusal as the authoritative "off" | Amended: V4-HOST-02 named "as revised by DECISION-5". The stale "host local operation … configured-model-server" sentence is removed | **Adopt** (with O-10) |

If the owner declines one, drop its edit and remove its IDs from that SoW's
AX line. The rest are unaffected.

### O-10 · Confirm the "record and show the model destination" reading for App runs

- **Question.** Does the owner confirm the recorder's reading of D5?
- **Facts.**
  - DECISION-2 D5 settles "no gate". "The App records the destination per
    turn and shows it" is the recorder's reading, labeled INTEGRATION by
    R5-4, and has not been confirmed by the owner.
  - DECISION-5 settles record-and-show for **host** agents only.
  - The reading is used in S-03-2, SC-04-03-3 (App part), S9-6-2 (a) and
    S9-9-5.
- **Recommendation.** **Confirm.** It matches DECISION-5's principle, gates
  nothing, and keeps the record truthful. If declined, the App-run
  record-and-show clauses become "may" statements, and the host-agent parts
  stand on DECISION-5.

### O-11 · DEL-04-02 visible autonomy: direct consumption and receivers (V1-A RF-05)

- **Question.** Do the siblings consume and receive DEL-04-02 directly, or
  through DEL-04-01/DEL-03-02?
- **The edits.** SC-04-02-2 names DEL-03-02, DEL-03-01 and DEL-02-03 as
  inputs, and DEL-05-01, DEL-05-02, DEL-03-02, DEL-03-03 and DEL-02-03 as
  receivers (E-0402-02). E-0402-03 names the matching owners in REQ-007. The
  boundary check passes only with both edits.
- **Facts.** All five designs already consume directly (AS U-15; LOOP O-6;
  PANEL §3.6; P §13; ADAPTER §5.5; EXEC §9.1).
- **Recommendation.** **Direct consumption.** It states what the designs do.
  The paired arcs (N-01…N-07) stay inside SCC-002, so SCC membership is
  unchanged (C1).
- **If declined:** also remove the DEL-03-01 and DEL-02-03 SoW paths from the
  source-key edit E-0402-01. They would otherwise still name those contracts
  as sources.

### O-12 · PANEL consumes DEL-02-03 directly, or only through DEL-05-01 (C1 S5-2-3 alternative)

- **Question.** Does PANEL consume EXEC's meanings directly, or only through
  LOOP?
- **Facts.** PANEL's current-phase display words apply EXEC PH-6…PH-8
  directly (PANEL F-10). The hold displays are governance phase (F-8).
- **Recommendation.** **Direct** (E-0502-03 as amended; arc N-25 inside
  SCC-002). **Alternative:** "only through DEL-05-01" drops E-0502-03 and the
  arc.

### O-13 · GUIDE's consumption of HOSTING, RELAY/answers and XT (C1 S-04-6, with N-B9…N-B11)

- **Question.** Is GUIDE's use of these files a declared consumption or a
  set of references?
- **Recommendation.** **Adopt S-04-6** as amended (it adds the recorded
  SWBPIPE answers, which GUIDE-v0.3 pins). GUIDE depends on these files for
  its matrix rows 1, 8 and 9.
- **Alternative (C1).** State them as references only. That drops E-0304-06,
  and P2 drops the three admitted-layer arcs.

---

## C. Allocation of DECISION-5 duties in SoWs

### O-14 · Host-agent destinations in the run record (DEL-04-03 REQ-002/CLM-002)

- **Question.** Should the run-record SoW list each host-agent destination
  contacted, with its allowing grant or list entry?
- **Facts.** DECISION-5 settles "every destination contacted is recorded".
  The allocation to RS R15 is R8-13 (INTEGRATION).
- **Recommendation.** **Adopt** E-0403-03 (with O-10 for the App part). It is
  the minimal SoW home for a settled record duty.

### O-15 · DECISION-5 display in DEL-04-02 (arc R8-A), and in other SoWs

- **Question.** Should the DECISION-5 display and grant duties be written
  into other SoWs now?
- **Facts.**
  - AS §3 (allow-list display), PANEL §3.8 (settings surface, in-work
    prompt) and ACT §2.7 already carry DECISION-5 in place.
  - The person-only grant maps to A12 under D2 (e) by R8-13 (INTEGRATION;
    ACT F-22).
  - The existing SoW requirements (DEL-04-02 REQ-001 "active person-granted
    autonomy scope"; DEL-05-02 interactions) already cover a grant display.
- **Recommendation (revised after node P2).**
  - **Adopt E-0402-08.** It is one DEL-04-02 CLM-002 sentence: AS consumes,
    from DEL-05-01, the allow list, in-work grants and contacted-destination
    record that DECISION-5 requires to be shown. It grounds P2's arc R8-A
    (candidate layer, SCC-neutral). It states settled content only; the A12
    mapping is not written into the SoW.
  - **No other SoW change** for DEL-04-01 or DEL-05-02 now. DEL-05-01 REQ-001
    (E-0501-09) already states "only the person grants a destination".
    Revisit when the A12 mapping is confirmed or at implementation.
  - If E-0402-08 is declined, R8-A is either declared by the owner or left
    out (P2 O-2).

---

## D. Confirmations the owner direction carried "to be confirmed"

### O-16 · Lifecycle: record IN_PROGRESS for the 14 first-increment deliverables — **DECIDED**

- **Decision.** Owner, exact: "Yes, record IN_PROGRESS (Recommended)"
  (DECISION-6, run OWNER_DECISIONS "Checkpoint A"). The 14 are recorded
  IN_PROGRESS at commit `67a2fac4b`.
- **Effect on this packet.** REVISE accepts IN_PROGRESS, so its
  preconditions still hold (IMPACT_ASSESSMENT §11). DEL-09-07 and DEL-08-01
  stay INITIALIZED, which REVISE also accepts.
- **Facts at the time of the recommendation.**
  - All 14 are INITIALIZED (`_STATUS.md`, 2026-09-27).
  - Authorized production has run in each Design folder, and C1 found
    IN_PROGRESS truthful for every one ("active human + agent work
    underway", TYPES; SPEC §3).
  - CHECKING is not warranted: outputs are partial and witnesses are unrun.
  - REVISE admits either state, so the SoW revisions do not depend on this
    transition.
- **Recommendation.** **Record IN_PROGRESS now** for DEL-01-01, 02-01, 02-03,
  03-01, 03-02, 03-03, 03-04, 04-01, 04-02, 04-03, 05-01, 05-02, 09-06 and
  09-09. The act belongs to the human or WORKING_ITEMS (`write_status.sh`,
  citing C1's lifecycle observations). DEL-09-07 and DEL-08-01 stay
  INITIALIZED.
- **Alternative.** Leave it for later, as the graph's completion condition 4
  permits.

### O-27 · Disputed arc DEL-03-02 → DEL-04-03 (C1-A N-12) — **DECIDED: not proposed** (DECISION-6)

- **Facts.** No SoW edit in this packet bears on it.
- **Recommendation.** Take node P2's analysis. The owner's recorded lean is
  "not proposed", which C1-B's reading supports: P receives acts from host
  capture, not from DEL-04-03.

### O-28 · Arc X-1: DEL-02-03 CLM-002 names DEL-01-04 (C1 SC-02-03-4) — **DECIDED: keep X-1** (DECISION-6)

- **Question.** Keep the clause "`DEL-01-04` (later undertaking) constructs the
  App act control" in DEL-02-03 CLM-002?
- **Facts.**
  - Node P2 found that extraction reads CLM-002 names as inputs, so this
    clause produces arc X-1 (DEL-02-03 → DEL-01-04). X-1 is not among C1's
    40 arcs.
  - EXEC §9.1 corroborates it. It lies inside SCC-002, so membership is
    unchanged, but it makes DEL-01-04 (not yet defined, D1) `DAG pending`.
- **Recommendation.** **Keep** (E-0203-04 as drafted). The consumption is
  real: EXEC's App-side capture requirements wait on DEL-01-04.
- **Alternative.** Move the clause to REQ-006 (exclusions), which
  extraction does not read as inputs. X-1 then drops.

### O-29 · Arc N-15: DEL-04-03 consumes DEL-01-01 supplier facts directly (C1 conditional) — **DECIDED: keep** (DECISION-6, the 41-arc set)

- **Question.** Does RS receive DEL-01-01's observed supplier facts
  directly?
- **Facts.** C1-A made N-15 conditional. The alternative is to let those
  facts reach RS through DEL-01-02 once DEL-01-02 is defined (D1 defers it).
  E-0403-01 keeps C1's clause "observed supplier facts … from `DEL-01-01`",
  and P2 keeps N-15 ("confirm at K1").
- **Recommendation.** **Keep.** RS R3, R5 and R13 are fed only by DEL-01-01
  in this increment (IR1A-19). Revisit when DEL-01-02 is defined.

### O-30 · Grounding route for node P2's nine arcs (P2 item O-2) — **DECIDED: route (a)** (DECISION-6, the 41-arc set)

- **Question.** How are the nine arcs grounded that the Design supports but
  no C1 correction states?
- **The arcs.** N-11, N-17, N-20, N-22, N-27, N-B3, N-B4, R8-A and R8-B.
- **Options (P2).**
  - (a) consumption sentences in the consumer SoWs, applied by REVISE;
  - (b) owner declarations in `_DEPENDENCIES.md`;
  - (c) leave them out.
- **Recommendation.** **(a).** The sentences are drafted and validated in
  SOW_REVISIONS §"Grounding for node P2's nine arcs": E-0301-07, E-0201-06,
  E-0201-01, E-0203-04, E-0303-07 with E-0303-04, E-0302-07, E-0402-08 and
  E-0403-01. Each traces to its Design basis and, where one exists, an owner
  decision. Every outcome is SCC-neutral (ARC_ANALYSIS §4).

---

## E. Consistency items outside the 14

### O-17 · Open_Issues OI-001/OI-002 pointers (C1-A F-8)

- **Question.** Should this amendment update the OI-001/OI-002 rows?
- **Facts.** The rows still read OPEN with no pointer to DECISION-1, while
  every SoW TBD now points to it.
- **Recommendation.** **Include** D-14a/b: the Consequence field names
  DECISION-1 D2/D3 and the OI-021 and DEP-001 residue. Status stays
  **OPEN**.

### O-18 · DEL-08-01 CLM-003 (Domains; PKG-08 work is excluded from this undertaking)

- **Question.** Should DEL-08-01's CLM-003 change?
- **Facts.** CLM-003 states the old V4-HOST-02 ("no data destination other
  than the configured model server"). The amended basis would contradict it.
- **Recommendation.** **Include E-0801-01.** It is a one-sentence consistency
  edit, not Domains design; REQ-006 and VER-006 stay as they are.
  Deferring it leaves an accepted SoW that contradicts the basis.

### O-19 · DEL-09-07 (owner of V4-EXM-22/23; SOW-201/202)

- **Question.** Should DEL-09-07 be revised in this amendment?
- **Facts.** Its REQ-005/006, AC-005/006 and VER-005/006 restate the old
  V4-EXM-22 ("checkpoint shall stop the run") and V4-EXM-23 ("no request
  anywhere except the configured model server").
- **Recommendation.** **Include** E-0907-01…10.

### O-8 · "Local-first" in the purpose statement and the PKG-05 description

- **Question.** Should "local-first" be amended in the purpose statement and
  in PKG-05?
- **Facts.** PRD §1.1 (the quoted purpose: "the agent runs local-first, on a
  model server the user controls") and Packages.csv PKG-05 ("minimal
  local-first host loop") both name a default that DECISION-4 D4-3 removes.
  The PRD §1.1 quotation is the owner's own purpose text.
- **Recommendation.** **Amend both** (A06: "runs on a model the person
  chooses — a model server the user controls or a cloud model — with no
  default"; D-13), with the `_CONTEXT.md` mirrors.
- **Alternative.** Keep the purpose text unchanged, as the owner's historical
  wording, and rely on V4-HOST-01 as amended. Then drop A06, D-13 and the
  DEL-05-02 `_CONTEXT.md` edit.

---

## F. Readings and deferrals to confirm

### O-22 · SoW frontmatter unchanged

- **Question.** Should `decomposition_basis` move to the amended snapshot?
- **Facts.** Several SoWs define their source keys ("G3", "B", "D") as the
  Group3 snapshot named in the frontmatter. Moving the basis would break
  those keys.
- **Recommendation.** **Keep** `decomposition_basis` at the GROUP3 snapshot
  in all 16 SoWs. Cite the amended rows and the amendment in the text and the
  new AX line instead.

### O-25 · DECISION-1 D2's "or a declared checkpoint" in the current phase

- **Question.** Does the owner confirm the reading of D2 for the current
  phase?
- **Facts.** D2 says: "No autonomy grant widens past a reserved act or a
  declared checkpoint." R8-11 item 2 (INTEGRATION) reads the checkpoint half
  as guidance in the current phase, binding only for governed checkpoints
  later. The reserved-act half binds now. V4-HI-42 (A12) is worded
  consistently. DECISION-1 is not rewritten.
- **Recommendation.** **Confirm the reading.**

### O-26 · PRD V4-AUT-03/04 and OQ-02 still read "open detail"

- **Question.** Should this amendment update the PRD's "open detail" markers
  for OQ-02?
- **Facts.** DECISION-1 D2/D3 ruled OI-001/OI-002 for the first increment
  only. The PRD's product-level OQ-02 remains broader.
- **Recommendation.** **Leave for a later basis update** (not in this
  amendment's request). The SoWs point to DECISION-1 where they carry the
  matter.

---

## What the workflow requires that P1 could not prepare

1. **Pre-change baseline:** DONE by node P3 (O-20). The post-change audit
   remains, over the same seven packages.
2. **Snapshot artifacts under `execution/_ScopeChange/`**: `Brief.md`,
   `Intake_Actions.csv`, `Impact_Assessment.md`, `Amendment_Preview.md`,
   `Propagation_Plan.md`, `Amendment_Actions.csv`, `Supersession_Delta.csv`,
   `Supersession_Map.csv`, `Decision_Log.md` and the group decision snapshots.
   They are outside P1's write scope. Their content is in this packet, for
   the integrator to transcribe after the owner acts.
3. **Change-register heading binding:** RESOLVED by A30/D-15. The new
   `## Decision Log` binds exactly under the audit-decomp rule (checked on
   the dry-run output).
4. **Register and arc consequences.** These are node P2's. IMPACT_ASSESSMENT
   §10 lists which SoW edits ground which proposed arcs, and which
   hold-related arcs should be re-read against the phased text.
