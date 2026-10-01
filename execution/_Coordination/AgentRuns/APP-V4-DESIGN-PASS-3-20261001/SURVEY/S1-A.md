# S1-A — Scoping survey: DEL-01-02 and DEL-01-03

Run `APP-V4-DESIGN-PASS-3-20261001`, node S1-A. Executor: Type 2 TASK (Claude
Opus 5.5, high effort), read-only on project state. Written 2026-10-01.
This file claims no SWBPIPE join, witness or adoption and changes no
register, ScopeOfWork, status, graph or Design file.

Paths are relative to `projects/chirality-app-v4/execution` unless they start
with `docs/` (then `projects/chirality-app-v4/docs/`).

## 0. What was read and how

| Input | How read | Identity checked |
|---|---|---|
| Run `BRIEFS.md` ("Common rules", "S1"), `OWNER_DECISIONS.md`, `DISPATCH.md` | Whole | sha256 prefixes `7ac504fb23ca97f3`, `ce37656640b824fd` |
| DEL-01-02 and DEL-01-03: `ScopeOfWork.md`, `Dependencies.csv`, `_DEPENDENCIES.md`, `_CONTEXT.md`, `_REFERENCES.md`, `_STATUS.md` | Whole | SoW sha256 `057ae2fdf4c3e98c…` and `b5d533cb3dbea97b…`; one commit each (`ddd721a90a`, `git log`); neither revised by SCA-V4-001/002 |
| `_DAG/DAG-003/HANDOFF_STATE.md`; `DependencyEdges.csv`, `CandidateEdges.csv`, `ExcludedRows.csv`, `DeliverableNodes.csv` (rows for these two) | Whole / by grep | `MANIFEST.sha256` and `SOURCE_MANIFEST.sha256` both pass (`shasum -a 256 -c`). The live registers of DEL-01-01…04, 02-02, 06-01, 09-02, 09-05 hash to the `SourceRegisterSHA256` values DAG-003 recorded, so DAG-003 is current for every row below |
| `_Decomposition/Open_Issues.csv`, `External_Dependencies.csv` DEP-005 | Whole / row | — |
| Second pass: `closeout/C1-A.md`, `C1-B.md`, `C1-C.md`, `CLOSEOUT_ACCOUNT.md`, `SURVEY/S1-F.md`, `DECISIONS_DRAFT.md`, `DECISIONS_PENDING.md` Part 3, `OWNER_DECISIONS.md` (DECISION-K1), `R9`, `R10`, `R13` | CLOSEOUT_ACCOUNT and OWNER_DECISIONS whole; the others by grep for both IDs and read around every hit | — |
| Earlier owner records: first-increment DECISION-1/2, intake DECISION-3/4/5 (by grep), R4 | Read at the cited items | — |
| First-increment Design files | `grep -c` of both IDs over every `PKG-*/1_Working/DEL-*/Design/*.md`; every hit read in context. HOSTING_BOUNDARY §1–§12 read whole; PIN_SPIKE P-08…P-15; OBS_1 by grep | HOSTING-BOUNDARY-v0.8 sha256 prefix `3cf0381c42358fec` |
| Generated protocol types at 0.158.0 | The committed JSON Schema bundles exist; the TS trees named in HOSTING's header exist in the session scratchpad (`…/scratchpad/codex-0.158.0/committed-ts-moved-out/{stable,experimental}/`). Read the TS files named in §1.5 and §2.5 | Not re-verified against `MANIFEST.sha256` in this node (COMMITTED_STATE.md records the parent's 1,605/1,605 check) |
| `docs/PRD.md` V4-APP-01/04, V4-EXE-01…04; `docs/ARCHITECTURE.md` §3 properties; `docs/EXAMINATION.md` V4-EXM-10/11/13 | Clause text | The amendments' `Amendment_Actions.csv` and `Amendment_Preview.md` touch none of these clauses (grep of clause IDs: only V4-HOST-01/02, V4-WF-05, V4-ARC-11/12, V4-EXM-20/22/23) |
| App v3 exemplar (`projects/chirality-app-dev`, `projects/chirality-runtime`) | File heads and grep | Evidence only, never a v4 commitment |

Reading conventions: **States** marks what a file says; **Inference** marks
mine.

---

# Part 1 — DEL-01-02 Durable execution and request recovery

Type BACKEND_FEATURE_SLICE; App execution/recovery owner; `_STATUS.md`
INITIALIZED (2026-09-27); no `Design/` folder. Register: 21 ACTIVE (17 anchor,
4 execution).

## 1.1 Obligations (31: 4 OUT, 9 REQ, 9 AC, 9 VER)

Basis keys: **EXE** = PRD V4-EXE-01…04; **APP** = PRD V4-APP-01/04; **A3** =
ARCHITECTURE §3 "Properties the App must hold" and reuse candidates; **EXM**
= EXAMINATION §2, V4-EXM-01…05, V4-EXM-11; **AUT** = PRD V4-AUT-03…05 with
HOST_INTEGRATION V4-HI-30…33; **H** = accepted HTML decisions 02/03/05;
**CL** = clarification direction (SOW-125).

| Item | One line | Rests on |
|---|---|---|
| OUT-001 | Main-process execution and outstanding-request custody code at the stock-Codex boundary, incl. answer/decline and unknown-request errors | EXE-01/02; A3 |
| OUT-002 | Interruption, reconnect and relaunch/continuation code keeping observation loss, explicit stop and restart recovery distinct | APP-01; EXE-01/04; A3 |
| OUT-003 | Candidate-bound settlement and observation-loss fixtures with interruption/reconnect/relaunch/missing-ack evidence | EXM |
| OUT-004 | Unknown-outcome and optional-reuse documentation, incl. state and compact-evidence handoff; no competing transcript, no new act schema | EXE-03; A3; CL; H 05 |
| REQ-001 | Child, protocol session and request register in the main process; window close/reload/hide is not a stop | EXE-01; A3 bullet 1 |
| REQ-002 | Explicit native interruption; stop request, transmission and observed interruption distinct; primary-turn end ≠ descendants stopped | EXE-01; APP-01; EXM-11 |
| REQ-003 | Answer or explicitly decline every request; outstanding requests survive observation loss; silence/timeout/reconnect/restart never grant | EXE-02; A3 bullet 2; H 03 |
| REQ-004 | Explicit error for an unknown server request; reply write/local settlement ≠ acknowledgment | A3 bullets 2–3; EXE-03 |
| REQ-005 | Recover actual Codex state and outstanding requests on reconnect; continue with prior-event access after quit/relaunch; no claim the old process survives quit | EXE-01/04; A3 bullet 3; EXM-11 |
| REQ-006 | Supply observed events and explicit unknowns to UI and evidence interface; faithful actual human acts with actor ≠ recorder; no manufactured acts; conversation recovery ≠ undertaking recovery | EXE-03; AUT; A3 bullet 4; H 05 |
| REQ-007 | Preserve restart/request behaviour whether or not v3 client logic is reused; record reuse assessment; no v3 Runtime service | CL; A3 reuse; V4-ARC-03 |
| REQ-008 | Fixtures and candidate-bound evidence for the coupled failure transitions, with pass/fail/blocked/not-run/inconclusive | EXM §2, EXM-11 |
| REQ-009 | Perform no act owned by DEL-01-01, DEL-01-04, DEL-04-03 or DEL-04-01 | Deliverables rows; AUT |
| AC-001 | Close/hide/reload leaves work and approvals in main-process custody; nothing inferred from visibility | REQ-001 |
| AC-002 | Explicit stop distinguishable from observation loss; outcome reflects observed interruption or uncertainty, incl. active descendant | REQ-002 |
| AC-003 | Grants, denials, answers, explicit declines; outstanding state survives observation loss; silence/timeout/recovery never approve | REQ-003 |
| AC-004 | Unknown request gets explicit error; missing ack stays unobserved after a write or settlement | REQ-004 |
| AC-005 | Recovered execution/request state after reconnect is grounded in Codex observations; stale rendered/transcript state establishes nothing | REQ-005 (reconnect) |
| AC-006 | After quit/relaunch the person continues and sees prior events; recovered / outstanding / unavailable stay distinct | REQ-005 (continuation) |
| AC-007 | Handoff keeps observed events and unknowns, faithful actual human response with actor ≠ recorder; fabrications and stronger claims rejected | REQ-006 |
| AC-008 | Fixtures cover window loss, interruption, known/unknown requests, denial, timeout, reconnect, restart, missing ack on identified candidates | REQ-008 |
| AC-009 | Documentation accounts for unknown outcomes, interfaces, four artifact classes, optional reuse, open means, named owners | REQ-007, REQ-009 |
| VER-001 | Observe custody with ongoing work and an outstanding approval across close/hide/reload; inspect for emitted stop/approval | AC-001; EXM-11 |
| VER-002 | Deliberate native stop traced to observed result; contrast observer loss and unavailable stop ack; separately active descendant | AC-002; EXM-11 |
| VER-003 | Grant, deny, answer, decline; interrupt observation while outstanding; silence/timeout negatives | AC-003 |
| VER-004 | Unknown server request at the boundary; unavailable ack after write/settlement | AC-004 |
| VER-005 | Disconnect/reconnect with deliberately stale local state; compare with Codex observations | AC-005 |
| VER-006 | Quit and relaunch the native App; continue; inspect prior-event access and outstanding/unknown state | AC-006; EXM-11 |
| VER-007 | Inspect the handoff: actual human act positive; absent act, transport-only success, lost ack, conversation-only recovery negatives | AC-007 |
| VER-008 | Review fixture inventory and candidate-bound results against REQ-001…006 | AC-008; EXM |
| VER-009 | Review documentation against the DEL-01-02 row, SOW-125, CL and A3; trace each excluded act to its owner | AC-009 |

**Overtaken or constrained by later amendments, decisions and rulings**
(the SoW itself is unrevised):

- **TBD-001 (OI-012, DEP-005).** Overtaken in part: first-increment
  DECISION-1 **D4** selected Codex 0.158.0 as the *definition/generation*
  pin; the qualification pin and re-examination before implementation stay
  under OI-012 (`Open_Issues.csv` OI-012 Consequence). OI-008 stays open;
  HOSTING §12 holds a proposal (O-1).
- **CLM-004, TBD-003 ("no blanket reserved-act/classifier policy has been
  settled").** Overtaken for the first increment's App/shared contracts by
  **D2** (five reserved acts) and **D3** (routine tool-permission and sandbox
  modes are the person's own Codex setting). OI-001/OI-002 rows stay OPEN by
  SCA-V4-002 Q-5 option A, and SCA-V4-002 `Impact_Assessment.md` V-4 records
  this SoW among those still saying "remain OPEN" (not in scope there). The
  "applicable adopted policy" DEP-01-02-021 waits for now exists as ACT §10.1
  V-21 (P-04 routine tool permission). HOSTING R7/R9 (INTEGRATION) narrow
  REQ-003: an affirmative A14 answer comes only from the person via DEL-01-04
  or from the person's own Codex mode inside the supplier; no App rule
  answers affirmatively.
- **REQ-002 under the phased checkpoint rule.** V4-WF-05 as amended
  (SCA-V4-001), intake DECISION-4 D4-1 ("I don't want checkpoints in
  workflows to be programmed into the app to respond in a certain manner")
  and DECISION-K1 K1-1 ("Neither the App nor a host's loop … pauses the
  run"): the only stop is the person's. HOSTING §6.7 "sends no
  `turn/interrupt`" at a checkpoint; EXEC RC-4 "Recording is not a
  reaction". Consistent with REQ-002; it forbids any App-initiated
  interruption.
- **REQ-006 / OUT-004 / DEP-01-02-020.** Ruling **R9-7** routes supplier
  facts (guidance, model destination, A14 settlements) from DEL-01-01 to
  DEL-04-03 *directly*; DEL-01-02's handoff is narrowed to custody-related
  observation (HOSTING S-7 "Not supplied here"; RS U-20). **R13-2** has the
  RS writer record the limit "App-restart interruption" on relaunch, which
  needs a relaunch fact from this deliverable.
- **Actor element (REQ-006).** DECISION-K1 **K1-4**: the App records the
  person's identity from what it can observe, marked "identity not verified".
  Applies to the actor DEL-01-04 supplies with an A14 answer.
- **Continuation (REQ-005).** R4-4 / EXEC §4.9 RE-1…RE-6 (PROPOSED standing):
  an ended run is never resumed; "an App restart … leaves the run
  interrupted and resumable as the same run" (RE-4). Not a contradiction, but
  it fixes what continuation means on the record side.
- **Not overtaken:** V4-HOST-01 "options, no default" (governs a host's
  agent; the App path's model choice is the person's, DEL-01-05);
  SC2-01-04-1 (act control proposed for DEL-01-04) changes no DEL-01-02
  obligation, since the act control raises no server request.

## 1.2 Joins

Every ACTIVE execution row in or out (anchors omitted). None of the arcs
below has an N-/X- label in DAG-003; DEL-01-02 is in no SCC.

| Row | Direction / type | Other end | DAG-003 | Contribution |
|---|---|---|---|---|
| DEP-01-02-018 | UPSTREAM INTERFACE | DEL-01-01 | **Admitted** (representative; DEP-01-01-019 is its MIRROR) | Stock process/protocol boundary and selected-version types |
| DEP-01-02-021 | UPSTREAM CONSTRAINT | DEL-04-01 | **Admitted**; DEL-04-01 has no DOWNSTREAM mirror (C1-A §4: noted, not proposed, D1) | Applicable adopted operation policy |
| DEP-01-02-019 | DOWNSTREAM INTERFACE | DEL-01-04 | **Admitted**; MIRROR of representative DEP-01-04-008 | State/request interfaces; observed events; unknown outcomes |
| DEP-01-02-020 | DOWNSTREAM HANDOVER | DEL-04-03 | **Admitted** (representative; DEL-04-03 has no counterpart row) | Compact observation evidence and outcome gaps |
| DEP-01-03-012 (in DEL-01-03) | DEL-01-03 → DEL-01-02 PREREQUISITE | DEL-01-03 | **Admitted**; no mirror in DEL-01-02 | Actual execution and outstanding-request/recovery state |
| DEP-09-02-010 (in DEL-09-02) | DEL-09-02 → DEL-01-02 PREREQUISITE | DEL-09-02 | **Admitted**; no mirror in DEL-01-02 | Recovery contribution and focused checks before V4-EXM-11 observations |

**What first-increment Design files already assume or require of DEL-01-02**
(quoted or closely paraphrased, by section):

- **HOSTING-BOUNDARY-v0.8 (DEL-01-01; admitted arc DEP-01-02-018).**
  - H3: "Durable custody across relaunch is DEL-01-02's (§6.5)."
  - §4.3 step 4: on unexpected exit, DEL-01-02 "owns recovery of actual
    thread/request state from the supplier after the next `ready`".
  - §4.5 step 2: outstanding entries at a deliberate stop "are either
    explicitly declined by the App with origin `app-rule:on-stop` or left to
    end with the process — a DEL-01-02 recovery decision (U-10)".
  - §4.6 "observe lifecycle": "Observer loss loses nothing: events are kept
    and re-read from a position (realization DEL-01-02's, §6.5)"; the failure
    table reports spawn, handshake, exit and forced-stop events "to DEL-01-02".
  - §5 Order: receipt positions support "re-attachment without gaps or
    duplicates (realization is DEL-01-02's, §6.5)".
  - §6.4: DEL-01-02 calls observe entries, list outstanding, and "read
    settlement and acknowledgment observation".
  - **§6.5 (the split, "to reconcile when DEL-01-02 is defined")**: DEL-01-01
    defines entry meaning, classification, R1–R9, the answer write path and
    generation tagging and witnesses the unknown-request path; DEL-01-02 owns
    custody across observation loss/reconnect/relaunch, recovery of
    outstanding requests from supplier state, register representation and
    persistence, stop-time handling (U-10), descendant handling (U-16) and the
    settlement fixtures.
  - §8 S-1 "Not supplied here: Durable custody, reconnect/relaunch,
    persistence, recovery reads, settlement fixtures, descendant policy".
  - §11: "Durable session/request custody, reconnect, relaunch, stop |
    DEL-01-02".
  - §12, open within O-1: "which interface component re-attaches after
    reload (DEL-01-02)".
  - UNRESOLVED naming DEL-01-02: U-05 (restart bound, grace period), U-09
    (acknowledgment mechanism), U-10, U-11 (any automatic decline), U-14
    (unknown-request split, F-01), U-16, U-26 (refusal order, custody side).
- **PIN_SPIKE_0.158.0** P-13: thread resume/read/list and subagent items are
  "DEL-01-02/DEL-01-03 inputs"; post-restart results not observed.
- **RECORD_SEMANTICS RS-v0.8 (DEL-04-03; admitted arc DEP-01-02-020).** R13
  supplier: "DEL-01-01 observed facts in this undertaking; DEL-01-02 later
  (D1)". §10 consumer table: DEL-01-02 consumes "R3/R4/R7/R13" and supplies
  "Observation evidence". §11 receiver table: "Compact observation evidence,
  observed events and outcome gaps (a later undertaking, D1; U-20)". U-20
  "R13 feed beyond DEL-01-01 observed facts", point of need "DEL-01-02
  definition". R11 lists "Lost acknowledgement" and, from R13-2, "App-restart
  interruption". Run-ended event: "That the run stopped (V4-EXE-01): who
  stopped it".
- **ACT-POLICY-v0.8 (DEL-04-01; admitted arc DEP-01-02-021).** §10.1 V-21
  (P-04 routine tool permission; D3 plus INTEGRATION) names DEL-01-02 among
  its receivers; §10.3 lists it as a declared consumer (DEP-01-02-021).
- **Design reliance with no register row** (Inference: candidates for a later
  `dependency-extract`, not decided here):
  - EXEC-v0.6 (DEL-02-03) §2.7: "The in-flight request register and custody
    across restart are DEL-01-02's (HOSTING S-1 …); the recorder only reads
    what is delivered"; AE-6 recovery "through thread reads"; RE-4 "an App
    restart … resumable as the same run"; AE-7 "Run ended: The person's stop
    (V4-EXE-01)".
  - ADAPTER-v0.6 (DEL-03-03) §5.x: "Custody of the in-flight native item
    across relaunch is DEL-01-02's (later undertaking, D1)"; XF-41 / L-ADAPTER-12
    "in-flight custody **AWAITING INPUT** (DEL-01-02 …)"; UNRESOLVED row
    "App restart: custody of an in-flight native item across relaunch (PI-6)".
  - XT-v0.6 (DEL-09-09) XC-06: App-restart variant L-XT-3 "not run …
    (custody DEL-01-02)".

## 1.3 Proposed contract changes already collected

**None.** No ScopeOfWork proposal in C1-A, C1-B or C1-C names DEL-01-02
(grep of all closeout files). Two register notes only:

- C1-A §4 and its R2 summary: DEL-04-01 → DEL-01-02 lacks a supplier-side
  mirror; "Outside mirrors noted, not proposed (D1)".
- C1-B §5.1/§5.3: the DEL-01-01/DEL-01-02 split on the unknown-request error
  "waits for DEL-01-02 (U-14)"; "Seams S-1…S-4 have no receiving comparison".

New candidates this survey sees (not collected; for SCA-V4-003 if the
integrator takes them): TBD-001 and TBD-003/CLM-004 pointers to D4, D2, D3
and ACT V-21 (as SCA-V4-002 did for DEL-01-04 and DEL-02-02); mirror rows
DOWNSTREAM → DEL-01-03 (of DEP-01-03-012) and → DEL-09-02 (of
DEP-09-02-010).

## 1.4 Open items and owner choices

| # | Item | Shapes design now? | Options (files) | Owner? |
|---|---|---|---|---|
| A-1 | **What "stop" means.** V4-EXM-11 says the person "stops a turn"; HOSTING §4.5/§4.6 define "stop" as ending the child ("The person: quit or stop (V4-EXE-01)"); EXEC AE-7 and RS's run-ended event read the person's stop (V4-EXE-01) as a **run end**, while RE-4 says an interruption is not a run end | **Yes**: states, operations and the record mapping differ | Turn interrupt (`turn/interrupt`), run end, and supplier stop as three distinct acts (Inference: what V4-EXM-11 and R4-4 together imply); or one "stop" that ends turn and run | Integrator can derive the turn/child distinction; **owner** if a turn stop is to end a workflow run |
| A-2 | **App quit with live work.** REQ-005 promises no survival through quit; HOSTING §4.5 "No unattended execution after quit is promised" | **Yes**: quit sequence, labels and VER-006 | (a) quit ends the child; the turn's outcome is *interrupted* or *unknown* as observed; (b) ask the person before quitting with a live turn or outstanding request; (c) interrupt the turn first, then end | **Owner** for (b) as product behaviour; otherwise DEL-01-02 |
| A-3 | **U-10 stop-time handling of outstanding entries** | Yes (one transition set) | Decline with `app-rule:on-stop`; or leave to end `ended-unanswered(process-exit)` (HOSTING §4.5) | DEL-01-02 (files) |
| A-4 | **U-11 any automatic decline after a period** (incl. native `timed_out`) | Yes (R3 path) | None (default); named-rule decline after a period, never affirmative | App implementation owner with DEL-01-02; Inference: "none" fits V4-EXE-02 most simply |
| A-5 | **Persistence (TBD-002) vs "no Chirality copy".** What the App keeps across relaunch: an index of the App's threads per project, stop records, lifecycle and register history, run↔thread association | **Yes**: data section and relaunch sequence | Derive everything from Codex reads (`thread/list`, `thread/read`, `thread/turns/list`, `thread/items/list`); or keep App-observed records, labelled non-authoritative, for facts Codex does not return | DEL-01-02 with DEL-01-01 (SoW); owner confirmation advisable because ARCH §3 says "rather than a Chirality copy of the transcript" |
| A-6 | **U-14 / F-01 unknown-request split** | Yes, small | Accept HOSTING §6.5 (DEL-01-01 writes the error at receipt; DEL-01-02 owns custody, evidence and fixtures), or amend | Both deliverable owners |
| A-7 | **U-09 acknowledgment observation.** RT-12/RT-13 read `serverRequest/resolved` after a written reply as an ack observation; observed once (OBS-1b OB-4); before-reply trigger unobserved | Partly (labels fixed, triggers open) | Adopt the PROPOSED reading; keep `not-observed` / `not-observable-at-pin` | DEL-01-02 with DEL-01-01 |
| A-8 | **U-16 descendant handling** on stop/restart/overlap; **U-05** bound numbers and grace period | U-16 yes (policy); U-05 no (numbers) | Wait, end, or start alongside surviving `git` descendants | DEL-01-02 with App implementation owner |
| A-9 | **Unobserved supplier behaviour (U-19)**: live effect of `turn/interrupt`; post-restart `thread/resume`/`thread/read`; whether pending approvals are re-raised after resume; `serverRequest/resolved` before a reply; resume-override adoption | Text can be written PROPOSED either way; verification standing depends on it | A bounded live observation like OBS-1 (local model, invented material), or design against the double only | **Owner** (DECISION-K1 K1-6 authorized one turn only; HOSTING §5.3 "No further live turn is authorized") |
| A-10 | **OI-008 Rust/TypeScript division** (HOSTING §12 O-1 recommended) | Partly: placement of custody and the re-attaching component | O-1 Rust envelope core; O-2 fully typed (O-3, O-4 set aside) | App implementation owner; phase-review item (DECISIONS_PENDING Part 3) |
| A-11 | **OI-009 account home** | Partly: which threads `thread/list` returns after relaunch (shared home shows the person's CLI threads), and the fresh-home fetch on first start | Shared; separate; shared configuration with separate sign-in (S1-F inference) | **Owner** with App implementation owner (phase review) |
| A-12 | **Evidence handoff content (RS U-20)** after R9-7: which RS elements DEL-01-02 feeds (R4 conversation reference; R11 "lost acknowledgement", "App-restart interruption"; run interruption facts for RE-4; R13 beyond DEL-01-01) | Yes | Name the elements and the route; DEL-04-03's writer reads them | DEL-01-02 with DEL-04-03 |
| A-13 | OI-001/OI-002 | No (ruled by D2/D3 for this scope) | — | Done; pointer only |
| A-14 | OI-012 qualification pin; DEP-005 | No for design; yes for qualification | — | App implementation owner |

## 1.5 What exists to build on

**Supplier facts (DEL-01-01, definition only, nothing qualified):**

- HOSTING §4: eleven lifecycle states, LT-01…LT-23 (all 23 exercised against
  the model, VC-27); stop record as the only evidence of a deliberate end
  (exit code is 0 for both input close and a signal, S-F-07); H11 process
  tree; restart never replays a prompt or re-answers an old request.
- HOSTING §5, §5.1–§5.2: client-request record, CR-01…CR-08, `unknown-no-response`
  on generation close, wait limit ends waiting only (H10).
- HOSTING §6: entry elements, classification, RT-01…RT-13, refusal order
  (U-26), R1–R9; `ended-unanswered(process-exit)` for every outstanding entry
  of a closed generation; H5 nothing crosses generations.
- Three PROPOSED schemas (`hosting.lifecycle-event`, `hosting.client-request-record`,
  `hosting.server-request-entry`), the supplier double and boundary model in
  `Design/prototype/` (run 2026-09-30, all cases as expected against the
  model; VC-06 restart bound, VC-14, VC-17 designed). Seam regression set X-09
  (child killed with an outstanding request) and X-10 (restart and recovery
  read) are designed, not runnable without a live turn.
- OBS-1/OBS-1b (one local pair, not qualification): OB-3 order around an
  approval (`thread/status/changed` [waitingOnApproval] → `item/started` →
  request → answer → `serverRequest/resolved` → …); OB-4 resolved 8 ms after
  a written accept; OBS-1 O-5: `turn/completed.turn.items` held only the last
  agentMessage (`itemsView: "summary"`), so a full history needs item reads.

**Generated types at 0.158.0 (TS, read in the scratchpad):**
`ThreadStatus` = notLoaded | idle | systemError | active{activeFlags:
waitingOnApproval | waitingOnUserInput}; `TurnStatus` = completed |
interrupted | failed | inProgress; `TurnInterruptParams` {threadId, turnId},
empty result; `ThreadResumeParams` doc: "If thread_id identifies a running
thread, app-server rejoins that thread", with configuration overrides and
`excludeTurns`; `ThreadResumeResponse` carries `turnsBackwardsCursor`,
`itemsBackwardsCursor`; `Thread.turns` populated only on resume, fork and
read (with `includeTurns`); `thread/turns/list`, `thread/items/list`,
`thread/loaded/list`, `thread/unsubscribe`; `ServerRequestResolvedNotification`
{threadId, requestId}. Nothing in the generated types says a pending server
request is re-raised on resume (Inference from absence; not observed).

**App v3 exemplar (evidence only):**

- `chirality-runtime/packages/daemon/src/turn-registry.ts`: "The Runtime
  service owns every active turn … closing a subscription never affects the
  turn. Explicit Stop is `interrupt`. Reopening a conversation recovers
  missed frames by sequence"; retention 10 min. Its owner was the separate
  Runtime service, which v4 excludes (CLM-005; V4-ARC-03).
- `codex-supervisor.ts`: one long-lived app-server; `interrupt` sends
  `turn/interrupt`; "after a restart every thread needs `thread/resume`";
  "Codex 0.154 ignores hot resume overrides"; unknown requests answered with
  -32601 (HOSTING F-02 records the v3 conflation).
- `core/src/session-store.ts` `markInterruptedOnShutdown`: records
  `turn.interrupted` and moves the session to *interrupted* on shutdown or
  crash.
- `core/src/descendant-tracker.ts`: process census, "deliberately not an
  orphan killer" (bears on U-16).
- `chirality-app-dev/frontend/src/lib/shell/turn-phase.ts`: phases idle,
  preparing, working, waiting, reconnecting, stopping; outcomes completed,
  interrupted, failed, unknown; "A lost connection is a phase … never an
  outcome … a turn the log cannot settle ends as `unknown`".
- HOSTING §12's reuse table already assesses `codex-app-server-client.ts` and
  `codex-supervisor.ts` as behaviour references with named gaps.

## 1.6 Design scope for this pass

Proposed: one Design file, `Design/EXECUTION_AND_RECOVERY.md`, with PROPOSED
schemas beside it only where a format is handed to a receiver.

1. **Header and reconciliation.** Basis pins; receivers from the live rows;
   accept or amend HOSTING §6.5 and close U-14/F-01 from this side.
2. **Three stops and two losses.** Define and keep apart: observer loss
   (window close/hide/reload), connection loss, turn interruption (the
   person's act; `turn/interrupt`), supplier stop (quit; HOSTING §4.5) and
   unexpected supplier exit (HOSTING §4.3). State which, if any, is a run end
   for DEL-02-03/DEL-04-03 (A-1).
3. **State model.** Per conversation: custody (Codex thread loaded / not
   loaded / unknown), execution (from `ThreadStatus` and `TurnStatus`),
   observer attachment, outstanding-request view across generations;
   stop-request record {requested, written, response, observed turn status
   or unknown}; App session state across quit and relaunch.
4. **Interfaces offered**, each with caller, result and failure behaviour:
   to DEL-01-04 (observe state, list outstanding, stop turn, answer routed to
   HOSTING §6.4), to DEL-01-03 (execution-state stream), to DEL-04-03
   (observation evidence, by RS element), plus what DEL-02-03 and DEL-03-03
   already read (offered only; no new row).
5. **Sequences with failure at each step:** window close/reload and
   re-attachment (by receipt position within a generation; by Codex reads
   beyond it); explicit stop; quit (A-2); relaunch and continue (resume or
   read; outstanding requests of the old generation shown ended, never
   answered); unexpected exit and restart (with HOSTING §4.3–§4.4);
   reconnect against deliberately stale local state; unknown request;
   lost acknowledgment.
6. **Transition tables** in HOSTING's style (IDs, guards, what is recorded,
   who is told), and the truthful labels (observed, recovered from supplier,
   unknown, unavailable, ended unanswered).
7. **Data and persistence** (A-5): what the App keeps, with what standing;
   what it never treats as authority.
8. **Decisions inside the deliverable:** U-10, U-11, U-16; U-05 numbers left
   open with test values.
9. **Evidence handoff map** to RS elements (A-12), closing RS U-20 from this
   side.
10. **Optional-reuse account** (REQ-007): v3 turn registry, supervisor resume,
    interrupted-on-shutdown, phase vocabulary, each against the receiving
    contract.
11. **Verification cases** VER-001…009 as designed cases, with supplier-double
    scenarios extending HOSTING's prototype (X-09, X-10 constructed variants)
    marked runnable or not; the native V4-EXM-11 witness plan; what a live
    observation would settle (A-9).
12. **UNRESOLVED and Findings.**

**Leave out:** product code; persistence technology, wire fields, timing
numbers (SoW Praxeology forbids inventing them); request cards and outcome
presentation (DEL-01-04); record format and writer (DEL-04-03); policy
(DEL-04-01); recovery of a branching undertaking, its descendants' returns
or fleet work (PKG-06, DEL-09-05; REQ-006 forbids the claim); qualification
on a candidate (none exists).

---

# Part 2 — DEL-01-03 Native plans, tools and delegation views

Type UX_UI_SLICE; App native-interaction owner; `_STATUS.md` INITIALIZED
(2026-09-27); no `Design/` folder. Register: 18 ACTIVE (10 anchor, 8
execution).

## 2.1 Obligations (25: 3 OUT, 8 REQ, 7 AC, 7 VER)

Basis keys as in §1.1, plus **A5** = ARCHITECTURE V4-ARC-05 and M-2;
**REC** = PRD V4-REC-03/05; **D** = Group3 Deliverables row and SOW-128/129.

| Item | One line | Rests on |
|---|---|---|
| OUT-001 | Code: native plan/revision and tool/delegation views, selected-version visibility, truthful activity/outcome, receiving interactions | APP-01/04; A5; A3; CL |
| OUT-002 | Test: pinned-native-item presentation fixtures and candidate-bound results | EXM §1–3; ARCH M-7 |
| OUT-003 | Doc: native feature and optional-UI-reuse map with owners, type/version basis, reuse decisions, open matters | A3 reuse; CL; Open_Issues |
| REQ-001 | Native plan creation and revision interaction; plan and revisions visible in native form; registry storage open | APP-01/04; D SOW-003/014/128/129; CL |
| REQ-002 | Substantive native tool activity and observed outcomes; unobserved stays unknown; no translation | APP-01/04; EXE-03; A5 |
| REQ-003 | Native subagent activity and descendant identity visible and usable by the fleet interface; primary completion ≠ descendants done | APP-01/04; A3; EXM-11/13 |
| REQ-004 | Identify the selected Codex version through the supplier boundary; experimental supplements distinguished; no verification claim against an unselected version | D SOW-128; A5; A3; OI-012/DEP-005 |
| REQ-005 | Keep execution, acceptance, checking, approval, reliance distinct; faithful display of a supplied actual human act, actor ≠ recorder; no acceptance-first order | AUT; REC; H 03 |
| REQ-006 | Feature/reuse map covers every interaction, receiving contributions, supplier identity, open choices; v3 code only as reuse candidates | D; A3; CL; EXM-03 |
| REQ-007 | Perform no act owned by DEL-01-01/02/04, DEL-02-02 or PKG-06; no new engine; no policy decision; no reliance act | Deliverables rows; ARCH M-2 |
| REQ-008 | Evidence bound to candidate, supplier/configuration and date; recorded exchanges; five outcome labels; WebKit, Chromium and packaged smoke | EXM-01…05; OI-015 (resolved by source) |
| AC-001 | Representative plans and revisions visible and interactive irrespective of registry implementation | REQ-001 |
| AC-002 | Tool activity and success/failure/unavailable outcomes render from native items; missing observation stays unknown | REQ-002 |
| AC-003 | Delegated work keeps native descendant identity and the fleet seam, incl. completed primary with an active descendant | REQ-003 |
| AC-004 | Presented version identity and types/fixtures match the supplied basis; missing/mismatch never "verified" | REQ-004 |
| AC-005 | Tool execution invents no human act; a separately evidenced act shown faithfully with actor ≠ recorder | REQ-005 |
| AC-006 | Map covers scope and artifacts, keeps conditional reuse, resolves exclusions to owners | REQ-006/007 |
| AC-007 | Fixture set and results meet REQ-008 without claiming the joined workflow, fleet or host journey | REQ-008 |
| VER-001 | Replay selected-version plan items and revisions; compare displayed sequence to source | AC-001; EXM-10 |
| VER-002 | Replay tool activity incl. unavailable result; inspect for renaming/translation | AC-002; EXM-02/11 |
| VER-003 | Delegated-work fixture with primary completion while a descendant runs; compare to display and fleet seam | AC-003; EXM-11/13 |
| VER-004 | Compare visible version and fixture/type identities to supplier input; exercise missing/mismatch | AC-004 |
| VER-005 | Fixtures: execution without act; attempted inference from a session entry; separately evidenced act | AC-005 |
| VER-006 | Review map against scope, clarification, CLM-001…004, issue rows; trace exclusions | AC-006 |
| VER-007 | Inspect fixture provenance and candidate/configuration/date/outcome; WebKit/Chromium/native standing | AC-007 |

**Overtaken or constrained:**

- **TBD-001 (OI-012).** As for DEL-01-02: D4 gives 0.158.0 as definition and
  generation pin; no qualification exists, so REQ-004's display can only say
  "definition pin, not qualified" (HOSTING §7.1 "expected distribution
  content identity: Not yet recorded").
- **CLM-004, AX-002, TBD-003 ("OI-001/002 remain open").** Overtaken for the
  first increment by D2/D3; rows stay OPEN by Q-5.
- **REQ-005 actor display.** K1-4: an App-captured act names the person with
  "identity not verified". Display wording follows it.
- **REQ-001 against the supplier.** HOSTING S-2 / P-10 (v0.8): each
  `turn/plan/updated` carries the whole plan with **no revision identity**;
  plan deltas must not be assumed to concatenate; plan mode is
  experimental-only (F-13). REQ-001 stands; the revision identity is
  DEL-01-03's to derive.
- **Vocabulary now fixed elsewhere (no arc).** WD-v0.8 §4.2.5 portable names
  `plan-update` (HCG-A09) and `agent-delegation` (HCG-A08) and HOSTING §8.4's
  groups define the native item set the views render; EXEC's presence rule is
  *inactive* for `plan-update`.
- **SC2-01-04-1 (act control for DEL-01-04).** Changes no DEL-01-03
  obligation, but REQ-005's "faithfully display" now has its only performed
  App-side route through DEL-01-04's control.

## 2.2 Joins

| Row | Direction / type | Other end | DAG-003 | Contribution |
|---|---|---|---|---|
| DEP-01-03-011 | UPSTREAM PREREQUISITE | DEL-01-01 | **Admitted** (representative; DEP-01-01-020 MIRROR) | Generated native types, selected identity, qualification evidence |
| DEP-01-03-012 | UPSTREAM PREREQUISITE | DEL-01-02 | **Admitted** (no mirror) | Actual execution and outstanding-request/recovery state |
| DEP-01-03-013 | DOWNSTREAM HANDOVER | DEL-02-02 | **Admitted**; MIRROR of representative DEP-02-02-012 | Native plan/tool interaction for the workflow-making journey |
| DEP-01-03-014 | DOWNSTREAM HANDOVER | PKG-06 (package) | **NOT_TOPOLOGICAL** (PACKAGE target, SR-2) | Native delegation identities and descendant activity |
| DEP-01-03-015 | UPSTREAM CONSTRAINT | OI-008 (App implementation owner) | NOT_TOPOLOGICAL (EXTERNAL) | Process division |
| DEP-01-03-016 | UPSTREAM CONSTRAINT | OI-014 | NOT_TOPOLOGICAL | Shared placement, only if common implementation |
| DEP-01-03-017 | UPSTREAM CONSTRAINT | OI-001;OI-002 | NOT_TOPOLOGICAL | Reserved acts / classifier (ruled for scope by D2/D3) |
| DEP-01-03-018 | UPSTREAM CONSTRAINT | OI-006 | NOT_TOPOLOGICAL | Further fleet scope, if pursued |
| DEP-06-01-007 (in DEL-06-01) | DEL-06-01 → DEL-01-03 INTERFACE | DEL-06-01 | **Admitted** (no deliverable-level mirror; DEP-01-03-014 is package-level) | Native supplier identities and actual child/parent evidence for record association |
| DEP-09-02-011 (in DEL-09-02) | DEL-09-02 → DEL-01-03 PREREQUISITE | DEL-09-02 | **Admitted** (no mirror) | View contribution and checks before V4-EXM-10 observations |
| DEP-09-05-008 (in DEL-09-05) | DEL-09-05 → DEL-01-03 PREREQUISITE | DEL-09-05 | **Admitted** (no mirror) | Descendant identity/activity presentation for the fleet witness |

**What first-increment Design files assume or require of DEL-01-03.** Only
DEL-01-01's files name it (grep: HOSTING 9 lines, PIN_SPIKE 4; every other
Design file 0):

- HOSTING §8 S-2: supplied = version identity record with each `ready(g)`;
  native plan items and plan updates "unchanged with generation and receipt
  position"; generic request path for plan interactions. **Not supplied:**
  "Revision identity (DEL-01-03 derives it from turn/item identities and
  receipt positions), registry, storage, export, UI, checker (SOW-128)".
- HOSTING §4.6: DEL-01-03 observes lifecycle "(the `ready(g)` record, S-2)"
  and reads version identity and verification result; "`unverifiable(<reason>)`
  is itself a result, never a pass".
- HOSTING §11: "Plan/tool/delegation presentation | DEL-01-03 | S-2 | Views,
  registry, revision identity, checker". §12 reuse table:
  `native-plan-registry.ts` is "DEL-01-03's decision; Tied to v3
  vocabulary/admission model". VC-09: plan updates native, whole-plan,
  "revision identity left to DEL-01-03".
- PIN_SPIKE P-10, P-13 and S-F-13: as above; "DEL-01-03 derives it".
- Indirect, no ID named: WD §4.2.5 and EXEC §3 presence rows for
  `plan-update` and `agent-delegation`; HOSTING §8.4 HCG-A08/A09 meanings.

The three consumers outside the first increment (DEL-02-02, DEL-06-01,
DEL-09-02/05) have no Design files.

## 2.3 Proposed contract changes already collected

**None.** No proposal in C1-A/B/C names DEL-01-03. C1-B §5.1 records only
that "At 0.158.0 plan updates carry no revision identity (P-10); DEL-01-03
derives one". New candidates (not collected): TBD-001/TBD-003/CLM-004/AX-002
pointers to D4, D2, D3; deliverable-level mirror rows for DEP-06-01-007,
DEP-09-02-011 and DEP-09-05-008.

## 2.4 Open items and owner choices

| # | Item | Shapes design now? | Options (files) | Owner? |
|---|---|---|---|---|
| B-1 | **Experimental opt-in.** Plan mode (`collaborationMode` on turn start), `multiAgentMode`, `collaborationMode/list`, `thread/settings/update` are experimental-only at 0.158.0 (HOSTING F-13, §7.3; U-21) | **Yes, most**: without the opt-in there is no native plan-mode plan item or plan-revision exchange, only the checklist `turn/plan/updated`; delegation mode cannot be set | Declare `experimentalApi` and accept the churn (HOSTING's route "accept the exposure and re-examine at each version"); or stable surfaces only | **Owner** (phase-review item 18 "experimental surface"; HOSTING U-21 "Owner visibility; App implementation owner at pin re-examination") |
| B-2 | **Plan revision identity and its durability.** S-2 assigns derivation "from turn/item identities and receipt positions"; receipt positions are per generation. `TurnPlanStep` occurs only in `TurnPlanUpdatedNotification` in the generated TS (checked: no thread item or history read carries it), so checklist revisions appear unrecoverable through App Server reads after a relaunch (Inference; not observed) | **Yes** | Derive {thread, turn, ordinal within turn} live and lose checklist history at relaunch (shown as unavailable); or keep an App-observed, non-authoritative revision record (SOW-128 "registry storage" choice) | DEL-01-03 with DEL-01-02; owner confirmation advisable (same tension as A-5) |
| B-3 | **Plan revision interaction.** How the person revises: a new turn in plan mode; answering a plan clarification (`item/tool/requestUserInput`, which is DEL-01-04's card); editing text then sending | Yes | As listed; live plan-revision request not observed (U-19) | DEL-01-03 |
| B-4 | **Whether "carry out this plan" is an act.** D2(b) reserves accepting a proposal "wherever the active autonomy requires a proposal"; in the App, autonomy for tools is the person's Codex setting (D3); R9/CAP-6: conversation input is never act evidence | Yes for REQ-005 wording and the plan view's controls | Conversation input only (Inference from D2, D3, R9, CAP-6); or an act captured through DEL-01-04's control | Integrator can derive; **owner** only if plan acceptance should be a recorded act |
| B-5 | **Split with DEL-01-04 and DEL-01-02.** DEL-01-04 owns "turn/outcome" presentation and requests; DEL-01-03 owns item-level tool outcomes; DEL-01-02 supplies execution state. Not yet drawn | Yes | Turn-level outcome and request cards at DEL-01-04; item-level activity at DEL-01-03; both read DEL-01-02 | Same owner role for both UX slices |
| B-6 | **Descendant visibility.** Whether the App receives child-thread notifications without subscribing, and what `agentsStates` shows after the parent turn completes: not observed. v3 showed "Observation ended with the parent turn. Later child activity is not recorded here." | Yes (labels, VER-003) | Read child threads (`parentThreadId`) on demand; label "last observed" | DEL-01-03; live observation needs **owner** (A-9) |
| B-7 | **Fleet seam to PKG-06 / DEL-06-01**: which native identities are exported (`agentThreadId`, `receiverThreadIds`, `parentThreadId`, `sessionId`, `agentPath`, nickname, role) | Yes, small | Export-only identity set; no import from PKG-06 (see §3 structural S-1) | DEL-01-03; OI-006 not needed |
| B-8 | **Plan → workflow draft seam to DEL-02-02**: what DEL-01-03 hands over (plan content, revision identity, source thread/turn) | Yes, small | — | DEL-01-03 with DEL-02-02 (S1-C) |
| B-9 | OI-008 | Partly (where revision derivation and view state live) | O-1 / O-2 | App implementation owner |
| B-10 | OI-014 shared placement | No (only on common implementation) | — | App/shared owners |
| B-11 | OI-006 further fleet scope | No (FEED, conditional) | — | Owner |
| B-12 | OI-012 qualification pin | No for design | — | App implementation owner |

## 2.5 What exists to build on

**Supplier facts (DEL-01-01):** S-2; HOSTING §8.4 Part A groups (HCG-A01…A17)
with meanings and availability signals; OBS-1b's command item (source
`agent` at start, `unifiedExecStartup` at completion; shell-wrapped command;
no output deltas; item announced in progress while approval pending, OB-2,
OB-3); OBS-1 O-5 (turn summary holds only the last message); §7.1 version
identity record and §7.2 verification rule.

**Generated types at 0.158.0 (TS):**
`TurnPlanUpdatedNotification` {threadId, turnId, explanation, plan:
[{step, status: pending | inProgress | completed}]}; plan item {id, text};
`PlanDeltaNotification` documented "EXPERIMENTAL … Clients should not assume
concatenated deltas match the completed plan item content";
`CollaborationMode` {mode: plan | default, settings} (experimental);
`collabAgentToolCall` {tool (nine `CollabAgentTool` values), status
inProgress | completed | failed | interrupted, senderThreadId,
receiverThreadIds, prompt, model, reasoningEffort, agentsStates:
{status pendingInit | running | interrupted | completed | errored | shutdown
| notFound, message}}; `subAgentActivity` {kind started | interacted |
interrupted | completed, agentThreadId, agentPath}; `Thread` {sessionId,
parentThreadId ("only set if this thread is a subagent"), agentNickname,
agentRole, cliVersion, status}; 19 item kinds in total.

**App v3 exemplar (evidence only):**

- `chirality-runtime/packages/core/src/native-plan-registry.ts`: an
  admission/qualification-gated "native Plan adapter" that "persists
  completed plan items"; `NativePlanRevision` = {revision: number,
  sourceEvent} (an ordinal per session).
- `chirality-app-dev/frontend/src/components/shell/native-plan-panel.tsx`:
  Plan tab with revisions, clarifications, plan-mode flag, export status and
  an execution record; `lib/harness/plan-executions.ts` keeps "which plan
  revision was sent for execution, in which turn, and how that turn ended"
  in local storage because the Runtime "has no notion of 'this turn executed
  revision N'".
- `tool-stream-view.tsx`, `subagent-stream-view.tsx` derive rows from
  `lib/shell/harness-event-views.ts`, which reads the bridged `HarnessEvent`
  stream: a translated vocabulary that V4-APP-04 and A5 exclude. Reusable
  as layout and truthfulness patterns only ("last observed", status badges).

## 2.6 Design scope for this pass

Proposed: one Design file, `Design/NATIVE_PLANS_TOOLS_DELEGATION.md`,
optionally with a small PROPOSED schema for the delegation-identity export
(the one seam a receiver outside PKG-01 reads).

1. **Header, receivers, basis pins**; the S-2 comparison from the receiving
   side (closes F-15 for S-2).
2. **Item scope table**: which native item kinds, notifications and requests
   each view renders, by HOSTING §8.4 group; the split with DEL-01-04 and
   DEL-01-02 (B-5).
3. **Plans**: the two native plan surfaces; revision identity rule and its
   durability (B-2); plan-revision interaction sequence (B-3); what is shown
   when deltas, updates or the plan item are missing; plan → draft seam
   (B-8); plan acceptance standing (B-4).
4. **Tool activity**: per-kind display states from the item lifecycle;
   *unknown* when a generation closes before `item/completed`; A14 origin
   shown only as the register supplies it; no translation.
5. **Delegation**: descendant identity model and states from
   `CollabAgentStatus` / `SubAgentActivityKind`; primary completed with an
   active descendant; "last observed" when observation ends; the export to
   PKG-06 (B-7).
6. **Version identity display**: `ready(g)` record, verification result,
   "definition pin, not qualified", mismatch and unverifiable displays.
7. **Truthful-actor rules** for the views (REQ-005), K1-4 wording.
8. **Sequences and failure behaviour**: reload, relaunch (what survives and
   what is shown unavailable), supplier exit mid-item, pin mismatch,
   experimental opt-in absent (B-1).
9. **Feature and optional-reuse map** (OUT-003): v3 plan panel, registry,
   executions record and stream views, each assessed.
10. **Fixtures and verification**: pinned-native-item fixtures constructed
    from the generated types (`constructed`/`mutated` labels as HOSTING
    §9.2), designed cases VER-001…007, WebKit/Chromium/packaged-smoke plan.
11. **UNRESOLVED and Findings.**

**Leave out:** visual design and UI code; registry storage technology and
any version checker (SOW-128 leaves them open; TBD-002); request cards,
turn outcomes and attachments (DEL-01-04); the workflow-making journey
(DEL-02-02); work-graph, return and decision views (PKG-06); host journeys.

---

# Part 3 — Across both deliverables

## 3.1 Owner choices, merged and ranked by how much design text depends on them

| Rank | Choice | Items | Why it ranks here |
|---|---|---|---|
| 1 | **Experimental opt-in** for plan mode and delegation mode | B-1 | Decides whether DEL-01-03 designs a plan-mode exchange and revision interaction at all, and the plan, delegation and version sections follow it |
| 2 | **Meaning of "stop", and App quit with live work** | A-1, A-2 | Sets DEL-01-02's states, operations and record mapping, and touches HOSTING §4.5/§4.6, EXEC AE-7/RE-6 and RS's run-ended event. The turn/child distinction is derivable; whether a turn stop ends a workflow run, and whether quit asks first, are product choices |
| 3 | **App-observed records vs derive-only** (persistence, plan-revision history, run↔thread association) | A-5, B-2 | Sets both files' data sections and relaunch sequences; reads against ARCH §3 "rather than a Chirality copy", so the owner should confirm the standing ("App-observed, not authority") |
| 4 | **A bounded live observation** (turn interrupt, resume after restart, re-raised requests, resolved-before-reply, child-thread notifications, plan updates after relaunch) | A-9, B-6 | Design text can be written PROPOSED either way; the observation decides how much stays PROPOSED and whether VER-002/005/006 and VER-003 have any observed basis before a candidate |
| 5 | **OI-008** Rust/TypeScript division (phase review) | A-10, B-9 | Placement of custody, re-attachment and revision derivation; O-1 is already recommended, so text changes are moderate |
| 6 | **Plan acceptance as an act** | B-4 | Derivable from D2, D3, R9 and CAP-6 as conversation input; owner needed only for the opposite answer |
| 7 | **OI-009** account home (phase review) | A-11 | Changes which threads the App lists after relaunch and the first-start fetch; small text |
| 8 | **U-11** any automatic decline after a period | A-4 | "None" fits V4-EXE-02; owner only if a timed decline is wanted |

Not owner choices (deliverable owners): A-3 (U-10), A-6 (U-14), A-7 (U-09),
A-8 (U-16, U-05), A-12 (RS U-20), B-3, B-5, B-7, B-8.

## 3.2 Structural questions that could force a later restructuring of a first-increment Design file

- **S-1 Cycle guard for these two (computed from DAG-003).** Across both
  layers, DEL-01-02 reaches only DEL-01-01, DEL-01-05 and DEL-04-01;
  DEL-01-03 reaches those and DEL-01-02. Paths exist to them from DEL-01-04,
  DEL-02-02, DEL-02-03, DEL-04-02, DEL-04-03 and DEL-06-01 (for example
  DEL-04-03 → DEL-01-02 admitted; DEL-04-03 → DEL-02-03 → DEL-02-02 →
  DEL-01-03 through held arcs). So any new row in which DEL-01-02 or DEL-01-03
  **consumes** one of those six forms an SCC: an SCC-forming departure for the
  owner and `scc-resolution-case`. The tempting cases are DEL-01-03 displaying
  human-act records (REQ-005; records are DEL-04-03's), fleet work-graph state
  (DEL-06-01) or checkpoint arrivals (DEL-02-03), and DEL-01-02 writing in
  DEL-04-03's format or taking DEL-01-04's identity scheme as an input. The
  design must keep these as offered interfaces or runtime values, not
  production inputs; otherwise RS §10/§11 and EXEC §2.7 receiver tables would
  have to be reworked. Checked by script over `DependencyEdges.csv` and
  `CandidateEdges.csv` (consumer → supplier).
- **S-2 The three senses of "stop"** (A-1). If DEL-01-02 defines the
  person's turn stop as `turn/interrupt` and not a run end, HOSTING §4.5/§4.6
  ("stop … The person: quit or stop (V4-EXE-01)") and its LT rows need the
  supplier stop renamed or narrowed; EXEC AE-7 and RE-6 and RS's run-ended
  event ("That the run stopped (V4-EXE-01)") need to say which act ends a
  run. `turn/interrupt` today appears in HOSTING only as the governance-phase
  HP-2 fact (§6.7).
- **S-3 Revision identity durability** (B-2). HOSTING S-2 and VC-09 tie
  DEL-01-03's revision identity to receipt positions, which do not survive a
  relaunch, and checklist plan updates have no history item at 0.158.0. If
  revisions must survive relaunch, either S-2's "Not supplied" cell changes
  or DEL-01-03 adds an App-observed record, which then needs a standing that
  fits ARCH §3 and DEL-01-02 REQ-005.
- **S-4 HOSTING §6.5 and the re-attachment realization** (A-6). If DEL-01-02
  re-attaches observers by re-reading Codex history rather than replaying a
  main-process event buffer, HOSTING §4.6 ("events are kept and re-read from
  a position") and §5 Order need a wording change. Small; not a
  restructuring.
- **S-5 Same-run resumption after relaunch** (EXEC RE-4, RP-1). EXEC assumes
  the App can re-associate a run with its Codex thread after a relaunch. If
  DEL-01-02 keeps no run↔thread association and the RS record's R4
  conversation reference is not enough to find the thread, RE-4's "resumable
  as the same run" falls back to "interruption not recovered" more often.
  EXEC already has that path, so no restructuring is expected.
- **S-6 Process division** (OI-008). HOSTING §12 calls O-1 a proposal; a
  different choice moves the register and re-attachment code and would reach
  both new files and HOSTING §1's diagram. This is already known (C1-B §5.3).

## 3.3 Limits

- The generated TS files were read from the session scratchpad and not
  re-hashed against `MANIFEST.sha256` in this node.
- First-increment Design files were searched by deliverable ID. A passage
  that relies on recovery or plan views without naming either ID would be
  missed unless it fell inside a block I read for another reason; EXEC's
  §2.7, §4.9 and §4.12 were found that way.
- "Not observed" and "not in the generated types" are statements about the
  pin's published types and the two OBS turns, not about Codex behaviour.
- Second-pass files other than CLOSEOUT_ACCOUNT and its OWNER_DECISIONS were
  read around grep hits, not whole.
