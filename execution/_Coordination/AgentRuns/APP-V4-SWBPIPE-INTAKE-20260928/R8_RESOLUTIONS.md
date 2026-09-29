# R8 intake rulings — SWBPIPE answers under the owner's phased direction

Integrator: HELP_HUMAN.

**Inputs:**

- [INTAKE_MAP.md](INTAKE_MAP.md) (I2, 221 rows);
- SWBPIPE's delivered answers (`RELAY_ANSWERS_SWBPIPE.md` sha256 `6f01add3…`,
  #1047);
- owner [DECISION-3 and DECISION-4](OWNER_DECISIONS.md).

**Delta check.** I2 read the earlier copy (`64ea4e59…`). The delivered text adds
clarifications and citations only: the persistence of the live-controller
activation, T3's integrity standing values, T9 and both-entry definitions,
RUNTIME-ADOPT contingency, and PB-TBD-002 ownership. No answer changed, and no
I2 row changes class.

R1–R7 stand except where amended here. Labels are as before (SETTLED, DERIVED,
INTEGRATION, PROPOSED). SETTLED here means *by DECISION-3 or DECISION-4*.

## R8-1 Phased checkpoints (DECISION-4 D4-1) — SETTLED; framing is INTEGRATION

**Phase 1 (this increment).** A workflow's declared checkpoints are **plan
guidance**:

- The declaration still states the required act, reached-when, subject and
  held actions (WD §4.3).
- The person and the agent plan around it. The agents manage any pause, hold
  point or gate themselves.
- Neither the App nor a host's embedded loop enforces a hold, blocks a run, or
  reports a workflow *unsupported* because a hold cannot be enforced.
- The required-tool check (V4-WF-04) is unchanged.

**In force in Phase 1:**

- A human act is recorded as done **only when the person performs it**
  (V4-WF-05, second half; R3/R4 act-evidence rules). An agent never records a
  human act on the person's behalf.
- **Reserved acts stand** (DECISION-1 D2): the five acts remain the person's,
  and a host enforces its own list through its operations (V4-HI-30).
  Examples: SWBPIPE's Apply is A5 in the person's hands, and enabling external
  access is A13 (R8-6).
- A checkpoint's arrival and the act that answers it may still be **recorded**
  (RS), so the person and the agent can see where the plan paused and what
  was done. Recording is observation, not enforcement.
  - *Action during hold* stops being a violation marker. It becomes an
    optional plain annotation, "continued past ‹checkpoint› before ‹act›".

**Governance phase (later, per workflow that needs it).** The following are
**retained as the governance-phase definition**. They are relabelled, not
deleted:

- the hold machine (EXEC §4.x HD states, re-hold, lapse);
- hold support (EXEC §3.6, the four values, HS-1…HS-5 as amended by R6-1 and
  R7-3);
- R2-12 carriage assurance;
- the R4-8 *unsupported* reason, and the LOOP §2.4.4 host-loop hold.

A workflow opts in by declaring its checkpoints **governed**, a new optional
declaration flag in WD, PROPOSED. Phase 1 honours the flag only as guidance.
The governance phase enforces it. Every workflow that needs governance must
be serveable by these definitions, so WD keeps every field they consume.

**V4-WF-05's first half is phased, not withdrawn.** Each affected file records
this, and it is flagged for the next accepted-basis update.

## R8-2 SWBPIPE SQ-02 and the hold values — INTEGRATION

- SQ-02's answer, "route (iv), none planned", is recorded as the
  **governance-phase input**. Under the retained rules, a governed checkpoint
  holding only host operations on X would be *not enforceable* against SWBPIPE
  (I2 R8-Q1 reading adopted for that phase). A later SWBPIPE decision to plan
  a route is a revision trigger.
- **I2 R8-Q-HS4 adopted for the governance phase:** SQ-11 is now answered for
  SWBPIPE (no exposure element; only `position.x` on X). So HS-4 no longer
  masks SWBPIPE entries, and HS-3 (c) decides.
- **Phase 1 changes no workflow result for hold reasons.** Files state
  E1/E1c/E1d/V-GR1 and the L-* cases in two parts:
  - **Phase 1:** checkpoints are guidance; the result depends only on the
    required tools and the channel state.
  - **Governance phase:** the I2 Part-2 values.
- **D6 is closed for Phase 1** by DECISION-4. It is re-opened only when the
  governance phase is taken up. EXEC U-E23 and GUIDE §2.13 re-point to it.

## R8-3 Staleness scope (I2 R8-Q2; §3 item 2) — INTEGRATION

R2-13 is amended:

- The App applies **per-item** staleness where the host supplies subject
  identities.
- Otherwise it receives and shows the **host's stated staleness scope**. For
  SWBPIPE, that scope is the whole model: any model change stales every queued
  proposal.
- The App never narrows a host's scope.
- The rule that de-duplication runs first is unchanged.

## R8-4 Whole-model identity (I2 R8-Q3; §3 item 3) — INTEGRATION

- A host's whole-model identity is received as the identity of every subject
  it covers. This errs toward reporting a lapse and never misses one.
- The App never computes identities itself.
- SWBPIPE does not yet meet V4-HI-32 (per-subject identity). This is recorded
  as an owner notice and an UNRESOLVED row (owner: SWBPIPE, PB-TBD-002 /
  DEL-16-03).

## R8-5 Outcome mapping (I2 R8-Q-item-1, R8-Q10, R8-Q13, R8-Q15; §3 items 1, 10) — INTEGRATION

| SWBPIPE term | App term | Condition |
|---|---|---|
| `unsupported_method` / `unsupported_change` | host-reported *not exposed on this surface* | Never *not permitted*. R2-4 (a named rule) is recorded as not met by this host |
| #885 `withdrawn` (the person cleared the queue) | the item left the queue, "cleared by the person, no decision record" | — |
| `validation_rejected` at Apply | *refused — invalid* at application | — |

- Neither `withdrawn` nor `validation_rejected` is ever A10 or A11.
- **Accept and apply** are one step on SWBPIPE, per batch, with no A10 record.
  The App keeps its meanings and records the missing counterparts.
- **Session undo** writes no receipt. R2-15 and R3-4 stand, and "reverses
  ⟨receipt⟩" is *not supplied* for SWBPIPE.

## R8-6 Enablement (SQ-28; I2 R8-Q4, R8-Q4b; §3 item 4) — INTEGRATION; Q4b deferred to the owner

- A13 (enabling external access) stays a reserved act (R8-1).
- SWBPIPE has no enablement facility, so its channel stays *not enabled*.
  Live XC/XF host variants carry the annotation "answered: not offered; host
  joins deferred (DECISION-3)" and keep the AWAITING INPUT token.
- `controller_unavailable` is reported as *endpoint unavailable*, and the
  channel shows *disabled*.
- If the host answers while no A13 is evidenced, an evidence limit is
  recorded.
- **Owner, deferred (R8-Q4b):** whether a launch environment variable the
  person sets counts as A13 evidence. Revisit when UI-SUCCESSOR resumes.

## R8-7 Relay and index hygiene (I2 R8-Q5, R8-Q6, R8-Q11, R8-Q14)

- **RELAY:** the relayed body (§0–§3) is not edited. Only its status line,
  UNRESOLVED rows and change rows change.
- **Standings:** move from *prepared*, *relay pending* and *not received* to
  **answered**. GUIDE §0 adds the *answered* standing.
- **PR #885:** recorded as deferred, with the owner's activation still in
  force. DEP-001 standing text is updated (I2 STD-5).
- **OI-003:** qualified as "App v4 OI-003" wherever text crosses projects.

## R8-8 Loop and panel (DECISION-4 D4-2) — SETTLED

- LOOP and PANEL keep V4-ARC-10 (D-20). They add a note: SWBPIPE's recorded
  embedded direction ("embedded Runtime", RUNTIME-ADOPT; D-58) predates D-20,
  and should be updated to the v4 loop when UI-SUCCESSOR resumes. That update
  is SWBPIPE's to make.
- The same note goes in the SWBPIPE handoff (`HANDOFF_SWBPIPE_DOMAINS.md`).
- **Seats (I2 R8-Q9):** keep SEAT-1…3, and note SWBPIPE's single agent panel as
  the likely counterpart.
- **LOOP §2.4.4 host-loop hold:** relabelled to the governance phase (R8-1).
  In Phase 1 the host loop does not enforce holds.

## R8-9 Model access (DECISION-4 D4-3) — SETTLED; V4-HOST-02 pending clarification

- A cloud model is reached by **OAuth sign-in or an API key**. There is **no
  default** between local and cloud, only options the person chooses among.
- LOOP's endpoint and key cases, and HOSTING where it describes host model
  access, add OAuth and drop "local by default".
- The V4-HOST-01 revision is flagged for the next accepted-basis update.
- **Owner, pending:** whether to keep V4-HOST-02 ("sends no data to any
  destination other than the configured model server").
- SWBPIPE's DEC-051 is compatible with D4-3 on choice. It is recorded as a
  note, not a conflict.

## R8-10 Other consequences (I2 Part 4) — record only

- **No capability catalog on SWBPIPE.** SWBPIPE has no per-operation identity
  or version, so WD required-tool references cannot resolve against it.
- **No host workflow library.** OUT-003's round trip cannot complete against
  SWBPIPE.
- **OI-021 stays open.** The candidate operations are recorded.
- **Strict preflight (I2 R8-Q12).** The agent never adds fields the host
  schema lacks.
- **Grant display (I2 R8-Q16).** "Host fixed treatment: every change waits for
  Apply" is the grant display for a host without grants. PROPOSED; can be
  deferred.

## Application

- **Version bumps:** Wave-1 files → v0.6; EXEC, ADAPTER, CA and XT → v0.4;
  GUIDE → v0.3.
- **RELAY:** status and ledger only (R8-7).
- **Each file:**
  - add a "## Changes from ‹prev›" table keyed by R8 IDs;
  - recast hold-support passages as **governance phase (retained)**, with a
    Phase-1 statement beside them;
  - apply the I2 A/V rows as ruled above (V rows about hold values become
    governance-phase values).
- **Owner files:** EXEC first (the phasing and hold values); WD next (the
  guidance semantics and the `governed` flag); then all other files. GUIDE is
  re-pinned last.

## R8-11 A1 residuals (integrator, after EXEC-v0.4 / WD-v0.6)

1. **PH-6 and PH-8 are confirmed (INTEGRATION).**
   - Recording that an act's standing *lapsed* when its subject changed is
     record truthfulness (V4-REC-05), not enforcement, so it continues in
     Phase 1.
   - Disposition words may label records.
   - Re-hold, which stops a run again after a lapse, is governance-phase only.
2. **Binding in Phase 1 (INTEGRATION).**
   - D2's "no autonomy grant widens past a reserved act" binds, and the host
     enforces it through its operations.
   - Its "or a declared checkpoint" half, WD I-7 and V4-HI-42, are **guidance
     in Phase 1**. The host's own treatment decides. They bind only for
     governed checkpoints in the governance phase.
3. **Phase-1 consequences confirmed.**
   - An invalid checkpoint declaration is reported as a **declaration finding**
     (invalid, with its FB code). It gives no hold-support value and does not
     make the workflow *not established* in Phase 1.
   - MT-15 and L-WDEX-15 stay *not established* in Phase 1. The reason is the
     unresolved harness-capability reference (U-08), a required-tool matter,
     not a hold.
4. **SoW wording.** The EXEC REQ-002, REQ-003 and AC-002 wording that assumes
   the run waits (EXEC F-29) is carried to the successor SoW route as a
   proposal. No SoW is edited.
5. **Fixture values read as if governed.** The governance-phase values on X
   read the fixture's checkpoints as if they were governed. Say so where the
   values are stated.
6. **Accepted:** the R8-2 override of I2 P2.16's wording.

## R8-12 A2–A5 residuals (integrator)

1. **Phase-1 lapse label (A2 vs A4).**
   - In Phase 1, a lapse after the resume point is recorded as **"act lapsed
     at ‹t›"**. Nothing says "waiting" and nothing is re-held.
   - A new act is recorded when performed.
   - LOOP G-7 and PANEL F-10 change from "waiting — lapsed at ‹t›" to this
     label. RS L-12 and AS OV-5 add it.
2. **FX-C9 / PC-24 confirmed.** When the active grant lets the host apply
   directly, no proposal arises and no A5 is required (D2: "wherever the
   active autonomy requires a proposal"). The checkpoint is guidance in
   Phase 1.
3. **C §8 map cells stay *unagreed*.**
   - The map records the host's agreement. SWBPIPE described its state; it
     agreed to nothing.
   - The note beneath the map is kept.
4. **ADAPTER F-22.** The channel state (*disabled*) and a request outcome
   (*endpoint unavailable*) are different facts and are shown together. No
   new channel state is added.
5. **Evidence-limit labels.** "host reachable without evidenced A13" and
   "constraint not carriable on this host" are adopted in RS R11. The second
   is backed by R8-10's principle.
6. **ADAPTER F-24.** Under R8-4, a whole-model identity satisfies RD-2 for a
   host that supplies only that, so a SWBPIPE read can be cited.
7. **Closing pass (node A6):**
   - EXEC U-E24 is closed in place by R8-11 item 2.
   - RELAY: the header's consumed-inputs line ("none received") and VC-R-04's
     expected text are corrected. These are App metadata; R8-7 protects only
     the relayed question body, §0–§3.
   - Sibling version citations across CA, XT, LOOP, PANEL and the others are
     refreshed to the post-R8 versions.
   - GUIDE → v0.3, re-pinned last.

## R8-13 Host-agent network destinations (DECISION-5) — SETTLED; the act mapping is INTEGRATION

- **LOOP §5.1 (network rules NW-*).** Implement DECISION-5:
  - two-level allow list;
  - model service always allowed;
  - MCP only if stateless 2026-07-28;
  - in-work request with scopes once / run / always;
  - decline outcome "destination not allowed by the person";
  - the always-off list;
  - every destination recorded and shown;
  - the limit on outside processes;
  - Phase-1 and governance-phase split.

  Retire the V4-HOST-02 "pending" markers and replace them with the revised
  text, flagged for the accepted-basis update.
- **ACT.** Granting a network destination (allow-list edit or in-work grant)
  is a person-only act. It is mapped as an **A12 grant change**, with subclass
  "network-destination grant": D2 (e) already reserves changing the autonomy
  grant. It is never performed by an agent.
- **AS.** The grant display shows the allow list (categories and named
  entries) and the in-work grants with their scopes.
- **RS.**
  - New record elements: destination contacted (per request: destination,
    category, allowing grant or list entry); destination grant (scope, time,
    source: list or in-work); destination declined.
  - An outside process is recorded with its declared destinations and an
    evidence limit, "process network not observed", when it is not sandboxed.
- **PANEL.** The settings surface for the allow list, the in-work request
  prompt with scopes, and the destinations-contacted display.
- **HOSTING.** Adds a note that DECISION-5 governs host agents only; the App's
  Codex keeps the person's own configuration.
- **GUIDE.** Receives these in the host checklist; re-pinned last.
- **Removed:** the V4-HOST-02 "pending" markers in C §4.1 and ADAPTER §3.4.
