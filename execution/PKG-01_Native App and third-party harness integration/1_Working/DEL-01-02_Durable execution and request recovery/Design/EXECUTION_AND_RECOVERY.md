# Durable execution and request recovery
- Contribution: DEL-01-02/RECOVERY-v0.1 (first version; no earlier Design file exists for this deliverable)
- Status: DRAFT DEFINITION — proposed, unsupplied, not implemented, not accepted. Beside it: three PROPOSED schemas (JSON Schema 2020-12), each with a valid and an invalid example instance, and a local design prototype in `prototype/` (not product code, not an App candidate; R12-3)
- Produced by: run `APP-V4-DESIGN-PASS-3-20261001`, node D1 (Type 2 TASK; Claude Opus 5.5, high effort), 2026-10-01, under BRIEFS "D — design nodes, round 1", row D1
- Serves: OUT-001 (custody of execution and outstanding requests: definition only), OUT-002 (interruption, re-attachment, restart and relaunch: definition only), OUT-003 (settlement and observation-loss fixtures: designed, some run against the prototype, none against a candidate), OUT-004 (unknown-outcome, evidence-handoff and optional-reuse account); REQ-001…REQ-009; AC-001…AC-009 through designed cases for VER-001…VER-009
- Phase: V4-WF-05 as amended by SCA-V4-001 (Phase 1). Neither the App nor a host's loop holds a run at a checkpoint, so nothing in this file interrupts, declines or pauses because of a checkpoint (DECISION-K1 K1-1; HOSTING §6.7; EXEC RC-4). Every interrupt here is the person's act or a quit the person confirmed.
- Basis, pinned by current bytes (`shasum -a 256` in the working tree, 2026-10-01): `docs/PRD.md` bb6e786f7a6c01dc5ce2f16f58e6c600989a12808ff47ce4fd87924bcc6c49bd (§2.1 V4-APP-01, §4.3 V4-EXE-01…04); `docs/ARCHITECTURE.md` 317d5789272c5206599936fa9b4e68551b30016d226b88039f0153afa02d828c (§3 "Properties the App must hold", reuse candidates); `docs/HOST_INTEGRATION.md` d4331c39db7f452cd3ba72fdfa4bad540a6053931218359a93646971acb28d9f (V4-HI-30…33, through CLM-004); `docs/EXAMINATION.md` 471798bc2f2dc0202ae40d9d5cf033a22ae41af2a0afdf58032cf37a687957d0 (§2, V4-EXM-11); all as amended by SCA-V4-001 and SCA-V4-002, neither of which touches the clauses cited here. This deliverable's `ScopeOfWork.md` 057ae2fdf4c3e98c961214739d2170a7c8ab29a530208f0c476af15125d6c6b4 (INIT, unrevised) and `Dependencies.csv` 84451e124cf2718581a4e86c97e62d4598838ac202ec371ddc12f2e4ebc55948 (the bytes DAG-003 records). DAG-003 `HANDOFF_STATE.md` 56d849b6d078d8d5282beb054d612f7fa058d30db408c48dc3900d10f67bb0b0 (its `MANIFEST.sha256` checks 37/37 OK).
- Run inputs (paths under `_Coordination/AgentRuns/APP-V4-DESIGN-PASS-3-20261001/`): `BRIEFS.md` b261394112d7264ef0b87ced64a513eccf0cb41dc96c8dfc8ec955ca62fb05c1; `OWNER_DECISIONS.md` 9d18c40dd7d894dc20b9edd2803dc6ab63f1deeadb79919411ea71f2ef248b1b (DECISION-K3 as revised: K-4 binding here); `R17_RESOLUTIONS.md` b0af81bcbad9bc52fddc99119c42a19019a9b174677d5b92a0a2f5c8b4f8e198 (R17-3, R17-4, R17-5, R17-9, R17-10, R17-13…R17-15); `DECISIONS_PENDING.md` 431ec4eb22a0b91323b2f33118c6820527fa9effc85de9e847a221a9023fdd86 (K-4 wording; Part 2); `SURVEY/S1-A.md` 8f021191f20e4a7e1e6b51fdcfb729bb9a562f3e4c6dd7144be937d77151e8ca (Part 1, the starting list §1.6). Earlier rulings R1–R16 and the owner decisions of every earlier App v4 run stand (BRIEFS common rules).
- First-increment files read (cited by version label and section; not edited, R17-14): DEL-01-01 HOSTING-BOUNDARY-v0.8 `HOSTING_BOUNDARY.md` 3cf0381c42358fec4a2088ab3886e14b66d6d2020482c72e195fda068a6d78b1; PIN-SPIKE-v0.1 0e090a4ca14e3ec323e8302ea4bc4e1fefc66bee50d0d3247e1cd0ddc04eb115; `OBS_1_0.158.0.md` 7b984b541edca0b14534d29115e77642c587a32f830bdf25a94a7ecca882cc43; DEL-02-03 EXEC-v0.6 64e732d502d0b91da00e62069be1b77b61d1e84986b3744bc117b6e67524fa38; DEL-04-03 RS-v0.8 b25cc90e9e252f50f30fcaed7faf230ec7bbf4689dcc2cd90deb35c7dcf7f47b; DEL-03-03 ADAPTER-v0.6 7cad04c873c0f1154a7a8ea8427772497a863f57167d420c485ea00373acca0c; DEL-04-01 ACT-POLICY-v0.8 `ACT_AND_POLICY_CONTRACT.md` 6fb6b9e883fa8d20da42c659de0485de0cb2a109a94c94364f16abde1dcc2b4a (§10.1 V-21 only); DEL-09-09 XT-v0.6 `EXTERNAL_TRACE_CASES.md` daf6c9c946ec15207b5e10321e36301a7fc9a8e103607c8befe8133fcccb5777 (XC-06 only).
- Supplier facts: HOSTING v0.8, PIN-SPIKE, OBS-1/OBS-1b, and the generated TypeScript at 0.158.0 in the session scratchpad (`…/scratchpad/codex-0.158.0/committed-ts-moved-out/`, read only). The 25 TS files this file cites were checked against `DEL-01-01/Design/generated/0.158.0/MANIFEST.sha256`: 25/25 OK (`shasum -a 256 -c` on the matching manifest lines). Labels per R17-13: `observed`, `observed-in-generated-types`, `inference`. The Codex binary was not run; no model was run; no network was used.
- Receivers (live ACTIVE execution rows; DAG-003 layer): DEL-01-04 via DEP-01-02-019 (mirror of DEP-01-04-008; admitted): state and request interfaces, observed events, unknown outcomes. DEL-04-03 via DEP-01-02-020 (admitted): compact observation evidence and outcome gaps. DEL-01-03 via its DEP-01-03-012 (admitted; no mirror here): execution and outstanding-request/recovery state. DEL-09-02 via its DEP-09-02-010 (admitted; no mirror here): the recovery contribution and focused checks. Offered without a register row (Design reliance only; see §14): DEL-02-03 (EXEC §2.7, AE-6, RE-4), DEL-03-03 (ADAPTER PI-6, XF-41), DEL-09-09 (XT XC-06, L-XT-3). Suppliers: DEL-01-01 via DEP-01-02-018 (admitted); DEL-04-01 via DEP-01-02-021 (admitted; constraint).
- **Reading of the ScopeOfWork (R17-15).** The INIT ScopeOfWork is unrevised and lags in five places; this file reads it as follows and the return file proposes the text for SCA-V4-003. (1) REQ-002, AC-002, VER-002 "explicit stop" / "native stop" is read as **interrupting a turn** (§2 DEF-3, R17-3), kept distinct from ending a run and stopping the Codex process. (2) REQ-005, AC-006 continuation after quit is read with K-4: quit asks first, live turns are recorded "interrupted by quit", and relaunch shows them with an offer to resume. (3) CLM-004 and TBD-003 ("no blanket reserved-act/classifier policy has been settled") are read as overtaken for this scope by first-increment DECISION-1 D2 and D3 and ACT §10.1 V-21: no App rule answers a tool-permission request affirmatively. (4) TBD-001 is read with D4 (0.158.0 is the definition and generation pin, not qualification) and R17-5 (O-1 process division, PROPOSED). (5) REQ-006 and OUT-004's evidence handoff is read as narrowed by R9-7 (supplier facts go DEL-01-01 → DEL-04-03 directly) and by R17-4 and R17-10 (DEL-01-02 offers its own custody facts; it writes nothing in DEL-04-03's format).

---

## 0. Reading this definition

**Standing labels for design content** (R9 as used by R17): **SETTLED** (an
accepted text or owner decision says it), **DERIVED** (follows from those),
**INTEGRATION** (the integrator's choice, open to the owner), **PROPOSED** (a
design structure of this file, decided by no one). A section or row without
a label is PROPOSED.

**Supplier facts** carry `observed` (seen live at OBS-1 or OBS-1b, one local
pair, not qualification), `observed-in-generated-types` (present in the
0.158.0 generated types; behaviour not seen) or `inference`. A cell whose
answer the local observation node OBS-2 is expected to give is marked
**OBS-2 pending** with its item (O-1…O-7 of R17-16); round 2 restates it.

**Names.** Element and state names here (*custody*, *stop request*,
*generation*, *ledger*) are semantic names of this design, not wire fields,
types, files or storage choices. Supplier method and field names are quoted
as supplier facts at 0.158.0 and select nothing. "The App" means the App's
main process (Rust host) unless the interface is named; the placement is
R17-5's PROPOSED O-1 division, stated separately from the requirements so
that a different OI-008 answer moves code, not obligations.

**What this file does not contain.** Product code, a persistence technology,
wire fields of Chirality's own, timing numbers (the ScopeOfWork's Praxeology
forbids inventing them: open numbers appear as TEST VALUES in the prototype
only), request cards and outcome presentation (DEL-01-04), record formats and
the run-record writer (DEL-04-03), policy (DEL-04-01), recovery of a
branching undertaking (REQ-006 forbids the claim; PKG-06, DEL-09-05).

## 1. What this deliverable is

The App's main process owns one stock Codex App Server child, its protocol
session and the register of outstanding server requests (ARCH §3; HOSTING
H2, H3). DEL-01-01 defines that boundary for the life of one child
(*generation*). This deliverable owns what lasts **longer than a
generation or a window**:

1. **Custody across observer loss**: a window closing, hiding or reloading
   changes nothing the supplier is sent (REQ-001; §5 SQ-W).
2. **The person's interrupt of a turn**, with its request, transmission and
   observed result kept apart (REQ-002; §3.4).
3. **Quit**, asked first when work is live (K-4), and the stop of the Codex
   process that follows (§5 SQ-Q).
4. **Recovery** of each conversation's actual state from Codex after a
   supplier restart or an App relaunch, with every outstanding request of a
   closed generation shown as ended, never answered (REQ-003, REQ-005;
   §5 SQ-X, SQ-R).
5. **The App ledger**: the pointers and App-observed facts the App keeps
   across relaunch, labelled as such and never treated as authority for what
   Codex holds (R17-4; §7).
6. **Custody facts handed to receivers** in this deliverable's own format
   (REQ-006; §8).

**Reconciliation with HOSTING §6.5 (closes HOSTING U-14 and F-01 from this
side; DERIVED from HOSTING §6.5 and DEL-01-02 REQ-004).** Accepted as
HOSTING proposes it: DEL-01-01 creates every register entry at receipt and
writes the explicit error to an unfamiliar request at once (HOSTING R1, R2),
defines entry meaning, classification, R1–R9 and the answer write path, and
witnesses the unknown-request path at the protocol seam. DEL-01-02 owns
custody of entries across observation loss, restart and relaunch, the
cross-generation view (§3.5), the ledger summary of each entry (§7), the
stop-time handling (U-10, §6) and the settlement and observation-loss
fixtures (§11). REQ-004 is met by consuming the DEL-01-01 path, recording
its result (RQ-08) and examining it in VC-R-04; DEL-01-02 writes no error of
its own. No second error path exists.

## 2. Stops, losses and run ends (R17-3; DEL-01-02 owns these definitions)

R17-3 (INTEGRATION, from DECISIONS_PENDING Part 2, not objected to) makes
"stop" three operations and says observer loss and connection loss are not
stops. The definitions below are the ones other files cite.

| # | Name | What it is | What it is not | Record it leaves |
|---|---|---|---|---|
| **DEF-1** | Observer loss | A window closes, hides or reloads, or the channel between the interface and the main process is lost (for example the web view process restarts) | Not a stop, not an observation loss for any record: the main process keeps observing the supplier. Hiding is not even a detach (OA-04) | None in any record; an operational log at most |
| **DEF-2** | Connection loss | In the O-1 arrangement (R17-5) there are two connections. Interface ↔ main process: its loss is DEF-1. Main process ↔ supplier: a standard-input/output pipe whose life equals the child's, so its loss is the child's end (DEF-5b). No third connection exists. "Reconnect" in the ScopeOfWork therefore means DEF-1 re-attachment (§5 SQ-W) and recovery after DEF-5 (§5 SQ-X, SQ-R) | Not a stop | As DEF-1 or DEF-5b |
| **DEF-3** | **Interrupt a turn** (R17-3 operation 1) | The person's act on one live turn of one conversation: the App sends `turn/interrupt` {threadId, turnId} (stable, empty result; `observed-in-generated-types`). The turn ends as the supplier reports it; the conversation, and any workflow run in it, continues | Not a run end (EXEC RE-4). Not a human act of R-1's list (A1–A15): no human-act record is written for it. Not an approval or a decline of any request | A stop request (§3.4), cause *person-interrupt*, actor the person marked *identity not verified* (K1-4) |
| **DEF-4** | **End a run** (R17-3 operation 2) | The person ends a workflow run explicitly, through DEL-02-03's run end (EXEC AE-7, RE-6). DEL-01-02 neither performs nor records it | Nothing in this file ends a run: not DEF-1, DEF-3, DEF-5, DEF-6 or DEF-7 (SETTLED by R17-3) | EXEC's `run_ended` (not this file's) |
| **DEF-5** | **Stop the Codex process** (R17-3 operation 3) | (a) *Deliberate*: the App stops its child (HOSTING §4.5), after a confirmed quit (DEF-6) or the person's explicit restart of Codex. (b) *Unexpected*: the child ends with no App stop record (HOSTING §4.3) | Neither ends a run. Neither answers any request | HOSTING's stop record and lifecycle events; here an `observation_lost` custody event and, for every outstanding entry, `request_ended_unanswered` |
| **DEF-6** | App quit | The person quits the App. With live work (a live turn, an outstanding request, or an active delegated child observed) the App asks first, listing them; if the person confirms, each live turn is interrupted (DEF-3, cause *quit*) and then the process is stopped (DEF-5a) (SETTLED by K-4; sequence PROPOSED, §5 SQ-Q). Closing the last window is DEF-1, not quit | Not a run end. No unattended execution after quit is promised (HOSTING §4.5; REQ-005) | `quit_requested`, `quit_answered`, `session_ended` in the ledger; stop requests with cause *quit*; turn labels "interrupted by quit" |
| **DEF-7** | App relaunch | A new App session. The earlier process and its child do not survive (REQ-005's own limit) | Not recovery of a branching undertaking (REQ-006) | `session_started` with the reading of the previous session's end (§3.1) |

**Mapping to the texts that use "stop"** (each re-pointed by node F, §14):

| Text | Reading under DEF-1…DEF-7 |
|---|---|
| V4-EXE-01 "stopping work is an explicit act" | DEF-3 or DEF-6, both explicit; DEF-1 never |
| V4-EXM-11 "the person stops a turn" | DEF-3 |
| HOSTING §4.5 "A stop is an explicit act (person quits the App or chooses stop)"; §4.6 stop operation "The person: quit or stop (V4-EXE-01)" | DEF-5a, reached through DEF-6 or the person's explicit Codex restart. A turn stop is DEF-3, which never stops the process |
| EXEC AE-7 "The person's stop (V4-EXE-01)"; RE-6 "*The person* names the person's own stop" | DEF-4 only. A DEF-3 interrupt, a quit or a supplier exit is never a run end; a relaunch leaves the run interrupted (RE-4) |
| RS §3 run-ended event "That the run stopped (V4-EXE-01)" | DEF-4 only |

## 3. States

Five stateful things are owned here. Each table row is one transition; the
prototype's model holds the same rows and checks this file against them
(C-10). "Recorded" names what is written: L = the App ledger (§7),
E = a custody event (§8), S = a stop-request record (§3.4). Transitions not
in a table are refused.

### 3.1 App session (AS)

| State | Meaning |
|---|---|
| starting | The App process has started; the ledger is being read |
| running | The App is usable. The supplier's own state is HOSTING's (§4.1) and is not repeated here |
| quit-confirming | The person asked to quit while live work was observed; the App shows the list and waits for the person's answer |
| quitting | Interrupting live turns, then stopping the supplier |
| ended | A `session_ended` record was written |

At start the App reads the previous session's end from the ledger: **clean**
(a `session_ended` after a quit with no live work), **quit-with-live-work**
(the person confirmed a quit whose list was not empty), **system-terminated**
(the system ended the App and allowed a final write), **ended-without-record**
(no `session_ended`: the App was killed or crashed), or **none**.

| ID | From | Event | Guard | To | Recorded / told |
|---|---|---|---|---|---|
| AS-01 | — | app-launched | — | starting | L `session_started` with the previous session's end reading |
| AS-02 | starting | ledger-opened | — | running | Per-conversation recovery queued (CV-19, CV-20); RQ-06 and SR-08 for the previous session's open items; E `app_restart_interruption` per conversation that had live work at the end |
| AS-03 | running | quit-requested | no live turn, no outstanding entry, no active child observed | quitting | L `quit_requested` with empty lists; nothing is asked |
| AS-04 | running | quit-requested | live work observed | quit-confirming | L `quit_requested` with the lists shown; the person is asked (K-4) |
| AS-05 | quit-confirming | person-cancelled | — | running | L `quit_answered` *cancelled*; nothing is sent to the supplier |
| AS-06 | quit-confirming | person-confirmed | — | quitting | L `quit_answered` *confirmed*; SR-01 for each live turn, cause *quit* |
| AS-07 | quit-confirming | live-work-changed | — | quit-confirming | L `quit_requested` with the updated lists (the earlier entry stays); the question stays open: no timeout, no automatic quit |
| AS-08 | quitting | interrupts-settled-or-wait-ended | every quit stop request settled, or the quit wait limit passed (U-R4) | quitting | HOSTING stop (§4.6) with the reason "quit confirmed by the person" |
| AS-09 | quitting | supplier-stopped | HOSTING `stopped` (LT-23, or LT-20…LT-22 with no child) | ended | L `session_ended` *quit*, with each quit stop request's state |
| AS-10 | running, quit-confirming, quitting | system-termination-notice | the system allows a final write | ended | L `session_ended` *system-terminated*; then HOSTING stop as the system allows |

A session that ends without AS-09 or AS-10 (killed, crashed, power lost) is
read at the next start as *ended-without-record* (AS-01).

### 3.2 Conversation (CV)

A conversation is one Codex thread the App started or resumed, keyed by the
supplier's thread identity. Its *execution* is read from Codex's own
`ThreadStatus` (`notLoaded` · `idle` · `systemError` · `active` with
`activeFlags` `waitingOnApproval` · `waitingOnUserInput`) and `TurnStatus`
(`completed` · `interrupted` · `failed` · `inProgress`)
(`observed-in-generated-types`; `waitingOnApproval` `observed` at OBS-1b
OB-3).

| State | Meaning | What the App shows (meaning only; DEL-01-04 presents) |
|---|---|---|
| indexed | Known to the App; not loaded in the current generation; nothing to recover | The conversation, readable from Codex history |
| recovery-pending | The last session or generation left it unsettled; waiting for `ready` | "Recovering…" with the App's last observation, labelled as such |
| recovering | Recovery reads in flight | As above |
| unavailable | Codex could not return its history | "Earlier events unavailable: ‹reason›", with a retry |
| loaded-idle | Loaded in the current generation, no live turn | Idle |
| turn-live | A turn in progress; sub-state from `activeFlags` | Working; "waiting for you" when a flag is set |
| interrupt-pending | A stop request was sent for the live turn and no final status is observed yet | Stopping |
| system-error | Codex reports `systemError` for the thread | The supplier's report, as received |
| observation-lost | Its generation closed while it was loaded | "Codex stopped" with the live turn's outcome *unknown* until recovered |

| ID | From | Event | Guard | To | Recorded / told |
|---|---|---|---|---|---|
| CV-01 | indexed | thread-loaded | `thread/resume` result observed in the ready generation, on the person's choice | loaded-idle | L `conversation_index` |
| CV-02 | loaded-idle | turn-started | `turn/started` observed | turn-live | L `conversation_index` (the live turn) |
| CV-03 | turn-live | thread-status-changed | `active` with flags | turn-live | Flags updated |
| CV-04 | turn-live | interrupt-sent | SR-02 | interrupt-pending | S (SR-02) |
| CV-05 | turn-live | turn-completed | `turn/completed` observed | loaded-idle | E `turn_outcome` *observed*; L `conversation_index` |
| CV-06 | interrupt-pending | turn-completed | `turn/completed` observed | loaded-idle | E `turn_outcome` *observed* with the stop request's cause; S (SR-06 or SR-07) |
| CV-07 | interrupt-pending | interrupt-refused | SR-05 | turn-live | The person is told the supplier's error; S (SR-05) |
| CV-08 | loaded-idle, system-error | generation-closed | HOSTING LT-12 or LT-23 | observation-lost | E `observation_lost` |
| CV-09 | turn-live | generation-closed | as CV-08 | observation-lost | E `observation_lost` with the live turn and in-flight items; the turn's outcome is *unknown* |
| CV-10 | interrupt-pending | generation-closed | as CV-08 | observation-lost | As CV-09; S (SR-08) |
| CV-11 | observation-lost | supplier-ready | HOSTING `ready(g′)` | recovering | Recovery reads sent (§5 SQ-X) |
| CV-12 | recovery-pending | supplier-ready | HOSTING `ready(g)` | recovering | As CV-11 |
| CV-13 | recovering | read-completed | `thread/read` and `thread/turns/list` results observed | indexed | E `observation_recovered` *accessible*; E `turn_outcome` for the turn last seen live (*recovered-from-supplier*, or *unknown*); S (SR-09) where it applies |
| CV-14 | recovering | read-failed | an error or no result | unavailable | E `observation_recovered` *unavailable* with the reason |
| CV-15 | unavailable | retry-requested | the person, or the next `ready` | recovering | As CV-11 |
| CV-16 | loaded-idle, turn-live | system-error-reported | `ThreadStatus` `systemError` | system-error | L `conversation_index` |
| CV-17 | system-error | thread-status-changed | `idle` or `active` | loaded-idle | — |
| CV-18 | loaded-idle | thread-closed | `thread/closed` observed | indexed | L `conversation_index` |
| CV-19 | — | session-started | the ledger's last observation of it is unsettled (a live turn, or observation-lost, recovery-pending, recovering, unavailable or interrupt-pending) | recovery-pending | — |
| CV-20 | — | session-started | otherwise | indexed | — |
| CV-21 | — | thread-started | `thread/start` result observed (a new conversation; DEL-01-04 and DEL-01-05 own the start, K-3) | loaded-idle | L `conversation_index` |
| CV-22 | recovering | generation-closed | the supplier ends during recovery | recovery-pending | — (recovery restarts at the next `ready`) |

A conversation loaded when a quit stops the supplier ends in
observation-lost (CV-08) and is read again at relaunch (CV-19): a cheap,
truthful check rather than an assumption that nothing changed.

### 3.3 Observer attachment (OA)

One per interface observer (a window's conversation view). Within a
generation the main process keeps a bounded **journal** of the frames it
delivered, by receipt position (HOSTING §5 Order), so that a re-attaching
observer can be given exactly what it missed. The journal is the protocol
session's working memory, not a copy of the conversation: it is never
written to disk and ends with the generation (R17-4). Its size is a TEST
VALUE (U-R4; v3's 10 minutes is historical only).

| ID | From | Event | Guard | To | Recorded / told |
|---|---|---|---|---|---|
| OA-01 | detached | attach | the observer's last position is in the current generation and still in the journal | attached | Replay of every frame after the position, then live frames: no gap, no duplicate |
| OA-02 | detached | attach | no position, a closed generation's position, or a position older than the journal | attached | A snapshot of current state (§4 `observe`) and Codex history reads; a gap marker "earlier events rebuilt from Codex history" |
| OA-03 | attached | observer-lost | DEF-1 (close, reload, channel loss) | detached | Nothing sent to the supplier; register unchanged (RQ-02) |
| OA-04 | attached | window-hidden | — | attached | Nothing: hiding is not detaching |
| OA-05 | attached | generation-closed | HOSTING LT-12 or LT-23 | attached | E `observation_lost` delivered, then the recovery events |

On every attach the observer's rendered execution state is replaced by the
snapshot: a stale rendered or cached state never establishes an outcome
(AC-005).

### 3.4 Stop request (SR)

One record per request to interrupt one turn (DEF-3), whether the person
pressed stop (cause *person-interrupt*) or confirmed a quit (cause *quit*).
It is written **before** the supplier request is sent, as HOSTING writes its
stop record first (§4.5 step 1), and again at each transition (append-only;
format `recovery.stop-request.schema.json`). It keeps three things apart, as
REQ-002 asks: the **request** (who, when, why), the **transmission** (*send*
and the supplier's *response*: `result` · `error` · `unknown-no-response`)
and the **observed result** (*turnOutcome* from `turn/completed`, with its
source). An empty result to `turn/interrupt` is the supplier accepting the
request, not the turn being interrupted.

| ID | From | Event | Guard | To | Recorded / told |
|---|---|---|---|---|---|
| SR-01 | — | interrupt-requested | the conversation is turn-live and the turn is in progress in the ready generation | requested | S written before anything is sent; actor the person, *identity not verified* (K1-4) |
| SR-02 | requested | write-succeeded | HOSTING §5.1 send, initiator `person-directed`, written | sent | S with the client-request reference; CV-04 |
| SR-03 | requested | write-failed-or-not-ready | HOSTING `write-failed` or `refused-not-sent(not-ready)` | not-sent | S; the person is told "stop not sent"; the conversation stays as observed |
| SR-04 | sent | result-observed | empty result | accepted | S (the request was accepted; nothing is yet known about the turn) |
| SR-05 | sent | error-observed | error response | refused | S with the supplier's message; CV-07; the person is told |
| SR-06 | sent, accepted, refused | turn-completed-interrupted | `turn/completed` status `interrupted` | settled | S outcome *interrupted* (*observed*); items completed after the request, recorded as observed, never as prevented (HOSTING §6.7 HP-2); delegated children observed active at that moment |
| SR-07 | sent, accepted, refused | turn-completed-other | status `completed` or `failed` | settled | S with that outcome: "completed (stop requested)" or "failed (stop requested)" |
| SR-08 | sent, accepted, refused | generation-closed | no `turn/completed` observed before the generation closed | outcome-unknown | S outcome *unknown*; response *unknown-no-response* if still pending; cause *quit* reads "interrupted by quit (final status not observed)" |
| SR-09 | outcome-unknown | recovery-read | Codex history reports a final status for the turn | outcome-recovered | S with that status, source *recovered-from-supplier* |
| SR-10 | sent | wait-limit | the caller's wait ended (TEST VALUE) | sent | S `waitingEnded`; nothing else changes (HOSTING H10) |
| SR-11 | requested, sent, accepted | interrupt-requested-again | — | same | Refused `stop-already-requested`; no second send |
| SR-12 | settled | response-observed | the response arrives after `turn/completed` | settled | S response recorded; the outcome is unchanged |

**Labels** (the `outcomeLabel` element; meanings for DEL-01-04): *interrupted
by the person*; *completed (stop requested)*; *failed (stop requested)*;
*outcome unknown (stop requested)*; *interrupted by quit* (K-4); *completed
(quit requested)*; *failed (quit requested)*; *interrupted by quit (final
status not observed)*. After a relaunch, Codex's own reported status is
shown beside the App's label (E `observation_recovered` `appReading`), so
"interrupted by quit; Codex reports: interrupted" and "interrupted by quit;
Codex reports: inProgress" stay distinguishable.

**Descendants** (REQ-002: "primary-turn completion shall not imply every
descendant has stopped"). At each settled outcome the record lists the
delegated child threads (`Thread.parentThreadId`, `observed-in-generated-types`;
delegation views are DEL-01-03's, experimental under K-5) that were observed
with a live turn at that moment. Whether `turn/interrupt` on the parent stops
them is **OBS-2 pending (O-4)**; the record states what was observed and
nothing more. Background terminals (`thread/backgroundTerminals/list`,
experimental-only) are reported the same way only where the experimental
opt-in is declared; supplier process descendants are HOSTING's H11 census.

### 3.5 Outstanding requests across generations (RQ)

HOSTING §6.2 owns the register's states for one generation. This table adds
the custody view: which entries are still **listed** for the person and which
are **closed**, across observer loss, generation close and relaunch.

| ID | From | Event | Guard | To | Recorded / told |
|---|---|---|---|---|---|
| RQ-01 | — | entry-outstanding | HOSTING RT-04 | listed | L `register_entry_summary` (no native parameters) |
| RQ-02 | listed | observer-lost | DEF-1 | listed | Nothing: the entry stays outstanding with no window (HOSTING R6) |
| RQ-03 | listed | entry-settled | HOSTING RT-07, RT-08, RT-09 or RT-10 | closed | L summary with the end (*answered* · *declined* · *settle-write-failed* · *resolved-by-supplier*), origin and write result. *resolved-by-supplier* is never shown as an answer (R17-9) |
| RQ-04 | listed | generation-closed | HOSTING RT-11 | closed | L summary *ended-unanswered(process-exit)* with its context (*supplier-exit* · *supplier-stop* · *app-quit* · *system-termination*); E `request_ended_unanswered` |
| RQ-05 | closed | generation-closed | a reply was written (answered or declined) and no acknowledgment was observed | closed | L summary acknowledgment *not-observed*; E `acknowledgment_not_observed` |
| RQ-06 | listed | session-start-reading | the previous session ended without a record with this entry listed | closed | L summary *ended-unanswered(process-exit)*, context *app-ended-without-record*; E `request_ended_unanswered` |
| RQ-07 | — | entry-outstanding-same-item | after a resume, a new entry's subject item equals a closed entry's item | listed | L summary with "same item reference as ‹entry›": an observed equality of the reference, never "the same request". **OBS-2 pending (O-2)**: whether Codex raises a pending request again on resume |
| RQ-08 | — | entry-errored-at-receipt | HOSTING RT-02 or RT-03 (DEL-01-01 wrote the explicit error) | closed | L summary *errored* with origin |
| RQ-09 | closed | acknowledgment-observed | `serverRequest/resolved` after the written reply (HOSTING RT-12, RT-13) | closed | L summary acknowledgment *observed* |

Refused, and so not in the table: answering a closed entry (HOSTING R4
`generation-closed`); answering an entry of an earlier session (it is not in
the register: `no-such-request`); any automatic decline after a period
(U-11, §6); an App decline at quit (U-10, §6).

## 4. Interfaces

### 4.1 Offered

Semantic operations; the transport between interface and main process is
unselected (HOSTING §1). Each failure row says who is told and what is left.

| Operation | Caller | Accepted when | Result | Failure behaviour |
|---|---|---|---|---|
| **observe** (conversation or all, from a position) | DEL-01-04 (views, request cards), DEL-01-03 (execution-state stream; DEP-01-03-012) | Any state | A snapshot (per conversation: CV state, live turn, flags, listed entries, last recovery event, stop requests) then frames and custody events in order (OA-01, OA-02) | Position outside the journal or in a closed generation → snapshot and gap marker (OA-02). Generation closes → `observation_lost`, then recovery events (OA-05) |
| **detach** (observer) | The interface | attached | OA-03; nothing sent to the supplier | — |
| **list outstanding** (conversation, optional) | DEL-01-04 | Any state | Listed entries of the ready generation (HOSTING §6.4 list outstanding) and closed entries of earlier generations and sessions with their end, from the ledger | Ledger unreadable → listed entries only, and "requests of earlier sessions not available" |
| **interrupt turn** (conversation, turn, actor) | DEL-01-04's stop control (the person's act); DEL-01-03's delegation view for a child thread | CV turn-live, the turn in progress in the ready generation; or a delegated child thread's turn observed live in the ready generation (`thread/started` with `parentThreadId`, then `turn/started`; PROPOSED, not run in the prototype; O-4 pending) | A stop-request identity; SR transitions follow | Refused with a reason: `no-live-turn` (the turn already ended: its outcome is returned), `stop-already-requested` (SR-11), `conversation-not-loaded`, `supplier-not-ready`. Write fails → SR-03 |
| **quit: assess, ask, answer** | The App shell; DEL-01-04 presents the question | AS running | Lists of live turns, listed entries and active children (AS-03 or AS-04); the person's answer (AS-05, AS-06) | Ledger write fails → the question is still asked and the quit proceeds on confirmation; the next start reads *ended-without-record* (truthful). The question has no timeout |
| **assess live work** (the assessment half of the row above, on its own) | Any caller that must ask first with live work, as K-4 does (for example DEL-01-05 before a sign-out or key removal) | Any state | The same three lists, as a runtime value; nothing is recorded and nothing changes | — |
| **resume conversation** (conversation, optional resume inputs) | DEL-01-04, on the person's choice | CV indexed; supplier ready | CV-01. Resume inputs are runtime values the caller hands over (the model choice from DEL-01-05, K-3; guidance from DEL-02-04, K-9); with none, no override is sent, so resume never changes the thread's model or guidance silently | `thread/resume` error → stays indexed, the error is shown. Not ready → refused `supplier-not-ready`. Never automatic; no prompt is re-sent (HOSTING §4.4) |
| **recovery status / retry** (conversation) | DEL-01-04, DEL-01-03; retry by the person | Any; retry in unavailable | The CV state and the last `observation_recovered` | Retry fails → stays unavailable |
| **tag / look up** (conversation, owner, opaque value) | A run starter (DEL-02-03's App writer, EXEC RE-4), DEL-03-03 | Any | Stored in the ledger and returned; DEL-01-02 never interprets a tag (R17-10) | Ledger write fails → the tag lives in memory only; after relaunch the lookup returns nothing and the receiver falls back (EXEC RE-4 "interruption not recovered") |
| **custody events** (stream) | DEL-04-03's writer (DEP-01-02-020), DEL-02-03's recorder, DEL-03-03, DEL-01-03, DEL-01-04 | Any | `recovery.custody-event` records (§8) | A receiver that misses events re-reads them from the stream position; events are App-observed facts, never authority for Codex's content |
| **descendants** (conversation) | DEL-01-03, DEL-01-04 | Any | Child threads observed with a live turn; background terminals where the experimental opt-in is declared; HOSTING's process census (H11) | None observed is reported as "none observed", never "none" |

**Placement (R17-5, PROPOSED).** The main process holds custody, the
journal, stop requests, the ledger and recovery; the interface holds only
its observer's position and what it renders. The stop control, the quit
question and every display are DEL-01-04's. The act control is not involved:
an interrupt and a quit are not reserved acts.

### 4.2 Consumed

| From | What | Row / standing |
|---|---|---|
| DEL-01-01 (HOSTING S-1) | Lifecycle operations and events (§4.6, §4.7), the stop record, generation tagging (H5), client-request send and records (§5.1), register operations (§6.4), exit and descendant facts | DEP-01-02-018, admitted |
| DEL-04-01 (ACT §10.1 V-21) | P-04 routine tool permission (D3): the person's own Codex setting; no App rule answers a tool-permission request affirmatively | DEP-01-02-021, admitted (constraint) |
| Runtime values, not production inputs (R17-10) | The person's identity as DEL-01-04 observes it (K1-4); resume inputs from DEL-01-05 and DEL-02-04; tags from receivers | No row; none is consumed as a contribution |

## 5. Operating sequences, with failure at each step

"Record" names what is left; "Next" what happens after a failure.

**SQ-W — Window closes, hides or reloads, then re-attaches (REQ-001, AC-001).**

| Step | Action | Record | Failure · who reports · record · next |
|---|---|---|---|
| W-1 | Window closes or reloads (DEF-1) | OA-03 | — |
| W-2 | Supplier frames keep arriving; the main process journals them and keeps the register | Journal; RQ-02 | The journal fills · the main process · oldest frames drop · the next attach is OA-02 |
| W-3 | A request arrives with no window (R1, R6) | RQ-01 | — (the request waits; DEL-01-04 may show an App-level indicator, §14) |
| W-4 | The window re-attaches with its last position | OA-01 or OA-02; snapshot | Position outside the journal · the main process · gap marker · Codex reads fill the view |
| W-5 | The view replaces its rendered execution state with the snapshot | — | — |

Nothing in SQ-W writes to the supplier (HOSTING H2): the prototype counts
zero frames sent across W-1…W-5 (C-01).

**SQ-I — The person interrupts a turn (REQ-002, AC-002; DEF-3).**

| Step | Action | Record | Failure · who reports · record · next |
|---|---|---|---|
| I-1 | The person presses stop on a live turn | — | No live turn · DEL-01-02 · refusal `no-live-turn` with the turn's outcome · nothing |
| I-2 | Stop request written | SR-01 | Ledger write fails · DEL-01-02 · the record lives in memory, the person is told the stop is not recorded · the stop still proceeds (the person's act is not blocked by bookkeeping) |
| I-3 | `turn/interrupt` sent | SR-02; CV-04 | Write fails or not ready · HOSTING · SR-03 · the person may press again (a new record) |
| I-4 | Response | SR-04 or SR-05 | Error · HOSTING · SR-05, CV-07, the person sees the error · the turn continues as observed. No response · — · SR-10 at the wait limit · the record stays *sent* |
| I-5 | `turn/completed` | SR-06 or SR-07; CV-06; E `turn_outcome` | Never observed and the generation closes · — · SR-08 · recovery (SQ-X) may give SR-09 |
| I-6 | Descendants at that moment | S `descendantsActiveAtOutcome` | Children keep running (O-4) · — · reported active · DEL-01-03 shows them; nothing infers their stop |

What `turn/interrupt` does live at 0.158.0 is **OBS-2 pending (O-1)**: when
the empty result arrives, whether `turn/completed` reports `interrupted`,
which items still complete, and what happens to a request pending in that
turn (resolved by the supplier, or left pending). The prototype runs SQ-I
under every combination of these (C-02); the labels stay truthful in each.

**SQ-Q — The person quits (DEF-6; K-4).**

| Step | Action | Record | Failure · who reports · record · next |
|---|---|---|---|
| Q-1 | The person chooses quit | AS-03 or AS-04; L `quit_requested` | Ledger write fails · — · none · the question is still asked |
| Q-2 | With live work, the App asks, listing live turns, listed requests and active children; it waits with no timeout | AS-04; AS-07 on change | — |
| Q-3a | The person cancels | AS-05 | — · nothing was sent |
| Q-3b | The person confirms | AS-06 | — |
| Q-4 | Each live turn is interrupted (SQ-I with cause *quit*) | SR-01…SR-07 | As SQ-I |
| Q-5 | Wait until each quit stop request settles or the quit wait limit passes (U-R4) | AS-08 | A turn never settles · — · its record stays *sent* · Q-6 makes it SR-08 |
| Q-6 | HOSTING stop (§4.5): stop record, polite end, then forced end of the whole tree after the grace period | HOSTING LT-17…LT-23; CV-08…CV-10; RQ-04 (context *app-quit*); SR-08 for unsettled ones | The tree outlives the grace period · HOSTING · `forcedAfterGrace` · `stopped` |
| Q-7 | Session ends | AS-09; L `session_ended` | Ledger write fails · — · none · the next start reads *ended-without-record* |

Requests still listed at Q-6 are **not** declined by the App: they end
*ended-unanswered(process-exit)* with context *app-quit*, and the quit
question had listed them (U-10, §6). The system may terminate the App
without waiting (logout, shutdown): AS-10 if a final write is possible,
otherwise *ended-without-record*.

**SQ-R — Relaunch and continue (DEF-7; REQ-005, AC-006; V4-EXE-04).**

| Step | Action | Record | Failure · who reports · record · next |
|---|---|---|---|
| R-1 | App starts; reads the ledger; previous session's end read | AS-01, AS-02; L `session_started` | Ledger unreadable or missing · DEL-01-02 · `session_started` *none* and the reason · conversations are listed from `thread/list` only, labelled "App history unavailable" (U-R2) |
| R-2 | Open items of the previous session closed: listed entries (RQ-06), unsettled stop requests (SR-08); `app_restart_interruption` per conversation with live work at the end | E per item | — |
| R-3 | HOSTING start → `ready(g1)` (a new generation, unique across sessions: §14 H-5) | HOSTING LT-01…LT-09 | Supplier refused or halted · HOSTING · lifecycle event · conversations stay recovery-pending, shown with the App's last observation labelled as such |
| R-4 | For each recovery-pending conversation: `thread/read` (metadata) then `thread/turns/list` (descending) | CV-12, CV-13 or CV-14; SR-09 | Read error (thread deleted, home changed, K-1) · — · CV-14 · retry (CV-15) |
| R-5 | Show each conversation with its readings: "interrupted by quit; Codex reports: ‹status›", "outcome unknown", "earlier events unavailable", and old requests "ended unanswered (App quit)" or "(App ended without a record)" | — | — |
| R-6 | The person chooses to continue one: `thread/resume` | CV-01 | Resume error · — · stays indexed · the error is shown |
| R-7 | Codex may raise a request again on resume (**OBS-2 pending, O-2**) | RQ-01 or RQ-07 | — (a new entry of the new generation; the old one stays ended) |
| R-8 | The person sends a message: a new turn | CV-02 | — |

Prior events are read from Codex (`thread/read`, `thread/turns/list`,
`thread/items/list`), never from the ledger: the ledger holds none (§7).
`thread/read` with `includeTurns` is marked deprecated for paginated threads
in the generated types, which advise a metadata read and paging
(`observed-in-generated-types`). OBS-1 observed that `turn/completed` carries
only a summary of items (`itemsView` *summary*), so full history needs item
reads (HOSTING §10.1). Which status Codex's history reports for a turn that
was live when its process ended is **OBS-2 pending (O-2)**: the design shows
whatever Codex reports beside the App's own reading (C-05, C-07 run all
three possibilities: *interrupted*, *inProgress*, turn absent).

**SQ-X — The supplier exits unexpectedly and restarts (DEF-5b; REQ-005,
AC-005).** HOSTING §4.3 closes the generation (LT-12), ends client requests
`unknown-no-response`, entries `ended-unanswered(process-exit)`, and restarts
within its bound (§4.4).

| Step | Action | Record | Failure · who reports · record · next |
|---|---|---|---|
| X-1 | HOSTING announces `exited-unexpectedly(g)` | CV-08…CV-10; RQ-04, RQ-05; SR-08; E `observation_lost` with live turns and in-flight items | — |
| X-2 | Observers are told (OA-05) | — | — |
| X-3 | HOSTING restarts → `ready(g+1)` | CV-11 | Bound reached → `halted-after-repeated-failure` · HOSTING · lifecycle event · conversations stay observation-lost, "Codex not running; restart needed" (the person's explicit restart, LT-16) |
| X-4 | Recovery reads as R-4 | CV-13 or CV-14; SR-09 | As R-4 |
| X-5 | The supplier ends again during recovery | CV-22 | — · reads resume at the next `ready` |

Nothing is resumed and no prompt is re-sent (HOSTING §4.4); the person
continues as in R-6…R-8.

**SQ-S — Re-attachment against deliberately stale state (VER-005).** A view
holding a stale rendered state (for example "turn completed; request
answered") re-attaches after a loss. OA-01 or OA-02 replace every execution
fact with the snapshot and Codex reads; the stale state is never compared
into an outcome (C-01, C-05).

**SQ-U — An unknown server request (REQ-004).** DEL-01-01 writes the explicit
error at receipt (HOSTING R1, R2); DEL-01-02 records RQ-08. A write failure is
HOSTING's `write-failed`, shown as such.

**SQ-A — An acknowledgment that never arrives (REQ-004, AC-004).** The
person's answer is written (RQ-03); `serverRequest/resolved` after a written
reply is the acknowledgment observation (HOSTING RT-12 reading, adopted here
as PROPOSED; observed once, OBS-1b OB-4). If the generation closes first,
RQ-05 records *not-observed* and E `acknowledgment_not_observed`; the answer
is never reported as received.

## 6. Decisions inside the deliverable

| Item | Decision | Standing | Why |
|---|---|---|---|
| **U-10** Stop-time handling of outstanding entries (HOSTING §4.5 step 2) | No App decline at stop or quit. Entries still listed when the process stops end *ended-unanswered(process-exit)* with their context; at a quit, the question listed them first | PROPOSED (closes U-10 from this side) | An App decline would record an answer, under a named rule, to a request the person never decided; R17-9 keeps a pending request waiting. *ended-unanswered* says exactly what happened, and K-4 shows the person the requests before the quit. Interrupting the turn first gives the supplier the chance to resolve them itself (RT-10), which is recorded as such (O-1 pending) |
| **U-11** Any automatic decline after a period, including the native `timed_out` form | None | INTEGRATION (R17-9: "A pending request waits") | V4-EXE-02 |
| **U-16** Supplier descendants on stop, restart and overlap (with the App implementation owner) | At a deliberate stop (quit or the person's restart): the whole tree is ended, as HOSTING §4.5 step 3 says. After an unexpected exit, before `g+1` starts: surviving descendants are recorded and shown to the person with what HOSTING's census observes (command line, age), with a person's action to end them; the App does not end them by rule, and `g+1` starts alongside after an overlap wait (TEST VALUE) | PROPOSED (with the App implementation owner) | Ending a process the agent started is an act on the person's work; a plugin-sync `git` holding Codex's own lock (HOSTING H11, S-F-06) is not the App's to kill. v3's descendant tracker was "deliberately not an orphan killer" (historical evidence only) |
| **U-09** Acknowledgment observation | Adopt HOSTING's RT-12/RT-13 reading: `serverRequest/resolved` after a written reply is an acknowledgment observation; with none before the generation closes, *not-observed*. *not-observable-at-pin* is reserved for a kind for which OBS-2 shows no notification follows a reply | PROPOSED (narrows U-09; the before-reply trigger is O-3) | REQ-004 |
| **U-14 / F-01** Unknown-request split | HOSTING §6.5 accepted (§1) | DERIVED | — |
| **U-05** Restart bound, grace period; here also the quit wait limit, the journal size and the stop wait limit | Rules defined; numbers open (TEST VALUES in the prototype) | Open (App implementation owner) | The ScopeOfWork forbids inventing timing numbers |
| Recovery reads are App-initiated | `thread/read` and `thread/turns/list` after `ready` carry initiator `app-rule:recovery-read` (HOSTING §5); resume carries `person-directed` | PROPOSED | Reads change nothing in Codex; resume loads the thread and is the person's choice |
| Generation identity across sessions | A generation's identity includes the App session, so nothing of one session's generation can be taken for another's | PROPOSED (join H-5) | H5 is stated per spawn; the ledger outlives the process |

## 7. Data and persistence: what the App keeps (R17-4; TBD-002)

**Rule (DERIVED from ARCH §3 "rather than a Chirality copy of the
transcript"; R17-4).** Conversation content is read back from Codex. The App
keeps only pointers and its own observations, labelled *App-observed*, and
never uses them as authority for what Codex holds.

The **App ledger** (`recovery.app-ledger-entry.schema.json`): append-only,
one entry per line, as RS §13.1 option S-A; its location and technology are
unselected (TBD-002 stays with the App execution/recovery owner and the
supplier-integration owner).

| Entry kind | What it holds | Used for |
|---|---|---|
| `session_started` | Session identity, App candidate identity, the previous session's end reading | AS-01; R-1 |
| `quit_requested`, `quit_answered`, `session_ended` | The lists the person was shown, the person's answer (actor *identity not verified*), the quit stop requests' states | K-4 record; relaunch reading |
| `conversation_index` | Thread identity, the App's project reference, opaque receiver tags, the App's last observation of its execution state (with the live or lost turn and its cause), the last generation it was loaded in | Which conversations are the App's; what to recover; tag lookup |
| `register_entry_summary` | Generation, request identity, method, subject references (thread, turn, item), custody state, end, origin, write result, acknowledgment | Ended-unanswered display after relaunch; RQ-07 |
| `stop_request` | The stop-request record (its own schema) | SR history across relaunch |
| `lifecycle_ref` | Generation and HOSTING transition identity | Linking custody to HOSTING's lifecycle records |

**Never kept** (the schema refuses them; C-11 checks the file): message or
reasoning text, item content, command lines, tool arguments or results, plan
content (DEL-01-03 shows checklist revisions Codex does not keep as "not
recoverable after relaunch", R17-4), request payloads, file contents.
Request cards after a relaunch show an ended request by its references; its
content, where Codex's history still has the item, is read from Codex.

**Standing of each source after a relaunch:**

| Fact | Source | Shown as |
|---|---|---|
| Messages, items, turns and their status | Codex (`thread/read`, `thread/turns/list`, `thread/items/list`) | Codex's history |
| Which conversations are the App's | Ledger index (the App's own list; `thread/list` would also show the person's CLI threads if K-1 shares the session store, **OBS-2 pending, O-6**) | The App's list |
| A turn that was live at the end | Ledger (App-observed) beside Codex's reported status | "interrupted by quit; Codex reports: …", "outcome unknown", never one stated as the other |
| Requests of the previous session | Ledger summaries | "ended unanswered (‹context›)"; never answerable |
| Tags (for example a run reference) | Ledger | Returned to the receiver that set them |

Retention and deletion of ledger entries are open (U-R3).

## 8. Formats and the evidence handoff

### 8.1 Formats (PROPOSED; R17-1; validated by the prototype, C-09)

| File | `$id` | What it is | Example instances |
|---|---|---|---|
| `recovery.stop-request.schema.json` | `urn:chirality:app-v4:del-01-02:stop-request:0.1` | One stop-request record (§3.4) | `…example.valid.json`: a person's interrupt, settled *interrupted*, one item completed after the request, one child still active. `…example.invalid.json`: *settled* with outcome source *not-observed* (a settled outcome must be observed) |
| `recovery.custody-event.schema.json` | `urn:chirality:app-v4:del-01-02:custody-event:0.1` | The custody facts offered to receivers: `observation_lost`, `observation_recovered`, `turn_outcome`, `request_ended_unanswered`, `acknowledgment_not_observed`, `app_restart_interruption`. Every event has standing `App-observed` | Valid: an `observation_lost` after a supplier exit with a live turn, an in-flight MCP call and an outstanding approval. Invalid: an `observation_lost` with cause `window-closed` (observer loss is not observation loss, DEF-1) |
| `recovery.app-ledger-entry.schema.json` | `urn:chirality:app-v4:del-01-02:app-ledger-entry:0.1` | The App ledger (§7) | Valid: a `register_entry_summary` ended unanswered at a supplier exit. Invalid: a summary carrying the request's native parameters (a command line): content is never copied |

No kind in these formats is a human act, an approval, an acceptance, a run
end or an operation outcome; the schemas have no place for one (C-08 checks
eight constructed stronger claims, all refused). Identities are opaque;
supplier identities are carried as data.

### 8.2 Handoff map (closes RS U-20 from this side; REQ-006, AC-007)

DEL-01-02 writes nothing in DEL-04-03's format (R17-10: that would make
DEL-01-02 consume DEL-04-03 and form an SCC). It offers the custody events;
each receiver maps them. This table is what DEL-01-02 proposes each receiver
does with them (node F edits the receivers' files, §14).

| Custody fact | Receiver and where it lands | Decided by the receiver |
|---|---|---|
| `observation_lost` | DEL-02-03 recorder: EXEC AE-6 → CE-13 `observation_lost` for each run whose conversation it names (through the tag lookup); the recorder decides *deciding* (V18-3 m-3). DEL-03-03: `inFlightItems` → PI-6 *outcome unknown*, last observed *submitted*. DEL-01-03, DEL-01-04: display | Whether a loss decides an arrival; the adapter outcome |
| `observation_recovered` | DEL-02-03: CE-14 with each recovered observation's own time (RP-1). DEL-01-04: "recovered from Codex" or "earlier events unavailable" | — |
| `turn_outcome` | DEL-01-04 and DEL-01-03 display; DEL-02-03 may read it for AW-12 (the named item never completes). Not a run end, never RS `run_ended` | — |
| `request_ended_unanswered` | DEL-04-03: RS R13 tool-permission settlement *ended unanswered (process exit)* for A14 kinds in App runs (a value R13 does not yet have, §14 J-RS-2); DEL-01-04 display | RS's spelling |
| `acknowledgment_not_observed` | DEL-04-03: RS R11 "lost acknowledgement" on the run whose conversation it names | — |
| `app_restart_interruption` | DEL-04-03: RS R11 "App-restart interruption" on relaunch (R13-2; RS §14.3 FC-9). DEL-02-03: the run stays interrupted (RE-4) and may continue as the same run when the person continues the conversation. DEL-03-03: PI-6 | Whether the run continues |
| Stop request (cause, actor, outcome) | DEL-01-04 display. DEL-04-03 decides whether an App run's record carries a turn interrupt (U-R6); it is never a human-act record and never `run_ended` | Whether RS records it |

The R13 feed beyond DEL-01-01's observed facts (RS U-20) is therefore exactly
two facts: requests ended unanswered by a generation close or an App end,
and lost acknowledgments. Settlements by the person, by App rules and by the
supplier stay DEL-01-01 → DEL-04-03 directly (R9-7). An actual human answer
keeps its actor as DEL-01-04 supplied it to DEL-01-01 (HOSTING §6.4); the
ledger stores origin only and never re-attributes an answer (C-08).

## 9. Supplier facts relied on, and what OBS-2 settles

| Fact at 0.158.0 | Standing | Used in |
|---|---|---|
| `turn/interrupt` {threadId, turnId}, empty result; stable | `observed-in-generated-types`; live effect not observed (HOSTING §6.7 HP-2, U-19) | DEF-3; SR |
| `TurnStatus` completed · interrupted · failed · inProgress; `turn/completed` carries the turn | Types; `completed` observed (OBS-1) | CV-05, CV-06; SR-06, SR-07 |
| `ThreadStatus` notLoaded · idle · systemError · active{waitingOnApproval · waitingOnUserInput}; `thread/status/changed` | Types; `active` [waitingOnApproval] observed (OBS-1b OB-3) | CV-03, CV-16, CV-17 |
| `thread/resume`: "If thread_id identifies a running thread, app-server rejoins that thread"; configuration overrides; `excludeTurns`; backwards cursors | Types (doc comment); post-restart not observed (P-13) | R-6; CV-01 |
| `thread/read` {includeTurns}, `thread/turns/list`, `thread/items/list`; full-history hydration marked deprecated | Types | R-4; CV-13 |
| `thread/closed` notification; `thread/unsubscribe` status notLoaded · notSubscribed · unsubscribed; `thread/loaded/list` | Types | CV-18 |
| `Thread.parentThreadId` ("only set if this thread is a subagent"); `ThreadSourceKind` subAgent… | Types | Descendants (§3.4) |
| `thread/backgroundTerminals/list` · `terminate` · `clean` | Experimental-only types | Descendants (§3.4), with the opt-in only |
| `serverRequest/resolved` {threadId, requestId} | Types; once after a written reply (OBS-1b OB-4) | RQ-03, RQ-09 |
| A known request is created before its item continues; order around an approval | Observed once (OBS-1b OB-3) | RQ-01 |

**OBS-2 pending cells** (R17-13; round 2 restates them from `OBS_2_0.158.0.md`):

| Cell | Item | What the design does meanwhile |
|---|---|---|
| SQ-I I-4, I-5; SR-04…SR-07 | **O-1** response timing, final turn status, items completing after the request | All four constructed variants run (C-02) |
| §6 U-10 rationale; RQ-03 | **O-1** a request pending in the interrupted turn: resolved by the supplier, or left pending | Both run (C-02, C-06) |
| SR-09; R-4; R-5; C-05, C-07 | **O-2** what history shows for a turn live when the process ended | Three variants run |
| RQ-07; R-7 | **O-2** whether a pending request is raised again on resume | Both run (C-06) |
| R-4 order | **O-2** whether `thread/read` works before `thread/resume` in a new process | Designed read-first; if not, R-4 resumes first, which loads the thread but sends no turn |
| U-09 before-reply trigger | **O-3** | RT-10 reading kept |
| §3.4 descendants; I-6 | **O-4** whether children stop with the parent's interrupt; whether a child thread is readable | Both run (C-02); readability is DEL-01-03's |
| Resume inputs | **O-5** resume with changed `developerInstructions` | DEL-01-02 passes what DEL-02-04 hands over; adoption is never claimed (HOSTING §8.2) |
| §7 standing table | **O-6** whether App and CLI share a session store under K-1 | The App's own index decides which conversations are its; unaffected |

## 10. Optional-reuse account (REQ-007, AC-009)

v3 code is historical evidence of behaviour (`projects/chirality-runtime`,
`projects/chirality-app-dev`), never a v4 commitment (CLM-005; BRIEFS common
rules). No reuse is proposed; the receiving contract above stands whether or
not any is chosen (REQ-007). Assessment, file heads read:

| v3 source | What it did | Against this contract |
|---|---|---|
| `chirality-runtime/packages/daemon/src/turn-registry.ts` | A separate Runtime service owned every active turn; closing a subscription never affected the turn; explicit stop was `interrupt`; missed frames recovered by sequence; 10-minute retention | Behaviour reference for OA-01 and DEF-3. The owner (a separate service) is excluded (V4-ARC-03; CLM-005); here the main process owns custody (R17-5) |
| `daemon/src/codex-supervisor.ts` | One long-lived app-server; `interrupt` sent `turn/interrupt`; "after a restart every thread needs `thread/resume`"; "Codex 0.154 ignores hot resume overrides"; unknown requests answered -32601 | Resume-after-restart agrees with R-6, but v4 resumes only on the person's choice. The override note bears on O-5. The -32601 path conflated "no live turn" with "unknown" (HOSTING F-02); not carried |
| `core/src/session-store.ts` `markInterruptedOnShutdown` | Recorded `turn.interrupted` on shutdown or crash | **Not carried**: v4 records "interrupted" only when observed or when the person confirmed a quit with the turn listed; after a crash the outcome is *unknown* until Codex's history says otherwise (REQ-002, REQ-006) |
| `core/src/descendant-tracker.ts` | Process census, "deliberately not an orphan killer" | Agrees with U-16 (§6) |
| `chirality-app-dev/frontend/src/lib/shell/turn-phase.ts` | Phases idle · preparing · working · waiting · reconnecting · stopping; outcomes completed · interrupted · failed · unknown; "a lost connection is a phase … never an outcome" | A vocabulary candidate for DEL-01-04. Gap: its label "Stopped" for *interrupted* does not say who or why; v4 labels carry the cause (§3.4) |

## 11. Verification

### 11.1 Designed cases

"Needs" says what a case requires to run: **D** the prototype's stub and
model (runs now); **F** a recorded-exchange fixture (HOSTING §9); **P** the
person; **C** an App candidate; **O** an OBS-2 observation. "Ran (model)"
means the rules ran as written against the stub; it passes no VER criterion.

| Case | Setup | Action | Expected | Needs | Status | Serves |
|---|---|---|---|---|---|---|
| VC-R-01 Custody across observer loss | A live turn, an outstanding approval, an attached window | Close, hide, reload, re-attach (in and beyond the journal) | Zero frames sent; the approval stays listed; replay without gap or duplicate; hide changes nothing; beyond the journal, a gap marker and Codex reads | D; then C, P | Ran (model) C-01 | VER-001 |
| VC-R-02 Interrupt traced to its result | A live turn with a pending request and a delegated child | The person interrupts; presses again; contrast with a window close | Request, transmission and result kept apart; labels per §3.4; a second press refused; a child observed active is reported, never assumed stopped; a window close produces no stop request | D under the O-1 and O-4 variants; then O, C, P | Ran (model) C-02, 16 combinations and a write failure | VER-002 |
| VC-R-03 Request settlement | Five requests (two A14, user input, elicitation, one left alone) | Grant, deny, answer, App-rule decline, App-rule affirmative, second answer, silence, observer loss, exit | Truthful origins; affirmative App rule refused `origin-not-permitted`; silence answers nothing; observer loss changes nothing; exit ends the silent one unanswered and refuses later answers `generation-closed` | D; then F (X-04, X-05, X-06), C, P | Ran (model) C-03 | VER-003 |
| VC-R-04 Unknown request and lost acknowledgment | An unfamiliar method; a written answer whose acknowledgment never comes | The double raises them; the process ends | Explicit error at receipt (DEL-01-01); RQ-08; `acknowledgment_not_observed`; never "received" | D; then F (X-07), C | Ran (model) C-04 | VER-004 |
| VC-R-05 Restart and recovery against stale state | A live turn, an outstanding request, an in-flight item, a stale rendered "done" | Supplier exit; restart; recovery read; a read failure and retry; an exit during recovery | `observation_lost` with the live turn and in-flight item; outcome from Codex or *unknown* under each O-2 variant; stale state replaced; no prompt re-sent; unavailable → retry; CV-22 | D; then F (X-09, X-10), O (O-2), C | Ran (model) C-05 | VER-005 |
| VC-R-06 Quit and relaunch (K-4) | Live work | Quit, cancel, quit, change, confirm; relaunch; continue | The question lists live work; cancel sends nothing; confirm interrupts then stops; labels per O-1 variant; relaunch reads *quit-with-live-work*; recovery from Codex; resume only on the person's choice; old request never answerable; a re-raised request is a new entry; quit with nothing live asks nothing; system termination read at relaunch | D; then O (O-1, O-2), C, P | Ran (model) C-06 | VER-006 |
| VC-R-07 App ended without a record | A live turn, a pending stop, a listed request | The App is killed; relaunch | *ended-without-record*; RQ-06; SR-08; SR-09 where Codex reports a final status | D; then O, C | Ran (model) C-07 | VER-006 |
| VC-R-08 Handoff makes no stronger claim | The custody formats; an actual answer by the person | Offer eight constructed stronger claims; inspect the person's answer | All eight refused; the person's answer keeps origin `person-via-interaction`; no human-act, run-end or approval kind | D | Ran (model) C-08 | VER-007 |
| VC-R-09 Formats | The three schemas and their examples | Validate | Valid examples valid, invalid ones invalid for their stated reason; every emitted record valid | D | Ran C-09 (and every case) | VER-008 |
| VC-R-10 Tables equal the model | This file and the model | Compare the 58 rows | Equal | D | Ran C-10 | VER-008 |
| VC-R-11 No content copy | A run with content | Search the ledger | No content | D | Ran C-11 | VER-007, VER-009 |
| VC-R-12 Fixture inventory | §11 and the candidate results | Review against REQ-001…REQ-006 | Each case has a recorded result with candidate, pin and configuration (EXM §2); none borrowed from history | C | Not run (no candidate) | VER-008 |
| VC-R-13 Documentation review | This file | Review against the DEL-01-02 row, SOW-125, the clarification, ARCH §3; trace each excluded act (§12) | Owners and open means named | Review | Not run | VER-009 |
| VC-R-14 Native witness (V4-EXM-11) | A candidate App, a model the person chooses, invented material | During V4-EXM-10's run: stop a turn, close and reopen the window, deny one approval and grant another, quit (confirming the question) and relaunch, continue | As VC-R-01…07, observed natively; browser evidence alone never stands for it (ScopeOfWork Praxeology) | C, P | Not run | VER-001…VER-006 |

### 11.2 The prototype (R12-1, R12-3)

`prototype/` holds: `supplier_stub.py` (an in-memory stand-in for the parts
of Codex this design relies on, every behaviour `constructed`, with the
variant axes of the OBS-2 pending cells); `recovery_model.py` (the five
tables and the sequences of this file, over a simplified stand-in for HOSTING
S-1); `run_cases.py` (cases C-01…C-12). The JSON Schema validator is
DEL-01-01's `prototype/jsonschema_subset.py` (sha256
486e9286e5aa56888b5473f1c08493a115591255685a8a7bb88b93ff2cacffc0), imported
read-only. Python 3 standard library only; no package installed; no network;
Codex never started.

**Run of 2026-10-01** (`python3 run_cases.py` in `Design/prototype/`;
macOS Darwin 25.6.0, Python 3.13.7; output in
`prototype/results/RUN_2026-10-01.txt`): 12 results, 12 as expected. C-02
ran 16 interrupt-variant combinations plus a write failure; C-05 and C-07
ran the three O-2 history variants; C-06 ran six quit-variant combinations;
C-12 found every one of the 58 table rows taken at least once.

**Not claimed.** The stub is not the supplier. A case passing under every
variant shows the labels stay truthful whatever OBS-2 finds; it does not
show which variant is true, and it qualifies nothing.

## 12. Owner and act boundary (REQ-009, AC-009)

| Act | Owner | This file |
|---|---|---|
| Interrupt a turn (DEF-3) | The person | Carries it; records the request, transmission and result |
| Quit (DEF-6) | The person | Asks first with live work (K-4); records the answer |
| End a run (DEF-4) | The person, through DEL-02-03 | None |
| Answer a request (A14, person input) | The person via DEL-01-04 → DEL-01-01 (HOSTING §6.4) | Custody of the entry; never answers |
| Supplier pin, protocol generation, the boundary's rules | DEL-01-01 | Consumes |
| Request cards, outcome views, the quit question's presentation, the stop control | DEL-01-04 | Offers state and operations |
| Record format, writer and reader | DEL-04-03 | Offers custody facts |
| Policy (P-04 routine tool permission) | DEL-04-01 (D3) | Consumes; no App rule answers A14 affirmatively |
| Persistence technology, Rust/TypeScript division, timing numbers | App implementation owner (TBD-001, TBD-002, OI-008, U-05) | Requirements only |
| A4–A7, A12, A13, A15 | The person (reserved) | None; nothing here stands for any of them |

## 13. Findings

- **F-R1 "Stop" had three meanings across the first-increment files**
  (S1-A A-1; S-2). Resolved by R17-3 and §2; the re-pointing is node F's
  (§14).
- **F-R2 Window close is not observation loss.** Several texts speak of
  "observation lost" (EXEC CE-13, AE-6; HOSTING §4.6 "observer loss loses
  nothing"). In the App the main process keeps observing when a window
  closes, so no record should carry an observation loss for DEF-1; only a
  generation end is one. The custody schema refuses `window-closed` as a
  cause.
- **F-R3 The interrupt's empty result is not the interruption.** The
  generated `TurnInterruptResponse` is an empty object; only `turn/completed`
  reports the status. A design that read the result as "stopped" would claim
  more than it observed (REQ-002).
- **F-R4 Recovery after quit needs App-kept pointers.** Without the ledger
  index the App cannot say which conversations were live at quit, and
  `thread/list` alone cannot separate App threads from CLI threads if K-1
  shares the session store. The index is App-observed and holds no content,
  which R17-4 allows.
- **F-R5 Run ↔ thread association without a cycle.** EXEC RE-4 and RP-1
  assume the App can find a run's thread after relaunch (S1-A S-5). Holding
  that association inside DEL-01-02 as a run concept would make DEL-01-02
  consume DEL-02-03 (an SCC by DAG-003; checked by script, §14). Opaque tags
  set by the run starter at run time keep the direction consumer → DEL-01-02.
- **F-R6 Generation identity must be unique across App sessions** for the
  ledger to keep H5's "nothing crosses generations" after a relaunch (join
  H-5).
- **F-R7 A turn reported `inProgress` after its process ended** is possible
  in principle (O-2); the design shows it as *outcome unknown* with Codex's
  report beside it, never as running.

## 14. Joins (summary; the return file `D/D1.md` lists them for node F)

- **HOSTING (DEL-01-01):** §4.5 and §4.6 cite DEF-3/DEF-5/DEF-6 (H-1); U-10
  closed by §6 (H-2); U-14 and F-01 closed by §1 (H-3); §4.6 "observer loss
  loses nothing" and §5 Order cite OA-01/OA-02, journal plus Codex reads
  (H-4); H5 generation identity unique across App sessions (H-5); U-09
  narrowed, U-11 closed, U-16 proposal (H-6); §6.4 "read settlement …
  DEL-01-02 (… outside this increment, D1)" and S-1/S-7 "outside this
  increment" wording now point here (H-7).
- **EXEC (DEL-02-03):** AE-7 and RE-6 cite DEF-4 and say an interrupt, quit or
  exit is not a run end (E-1); AE-6 cites the custody events and DEF-2 (E-2);
  §2.7 "custody across restart are DEL-01-02's (HOSTING S-1, outside this
  increment)" re-points here, with the tag lookup (E-3).
- **RS (DEL-04-03):** the run-ended event cites DEF-4 (J-RS-1); R13 gains the
  settlement *ended unanswered (process exit)* and its supplier "DEL-01-02
  (custody facts)" (J-RS-2); U-20 closed by §8.2 (J-RS-3); §10 and §10.1 rows
  for DEL-01-02 cite this file (J-RS-4).
- **ADAPTER (DEL-03-03):** PI-6, XF-41 and its UNRESOLVED row re-point from
  "AWAITING INPUT (DEL-01-02, later)" to §8.2 (`observation_lost`
  `inFlightItems`, `app_restart_interruption`) (J-AD-1).
- **XT (DEL-09-09):** XC-06 L-XT-3 custody note re-points here (J-XT-1).
- **Not first-increment (round-1 siblings):** DEL-01-04 places the stop
  control, the quit question, an App-level indicator of requests waiting with
  no window, and the labels of §3.4 (J-04); DEL-01-03 consumes the
  execution-state stream and descendant report and shows checklist revisions
  as "not recoverable after relaunch" (J-03).

## UNRESOLVED

| Item | Owner | Point of need | Effect here |
|---|---|---|---|
| U-R1 OBS-2 items O-1, O-2, O-3, O-4, O-6 (§9) | OBS-2 node, then round 2 | Before fixtures are recorded | Cells marked; every variant designed and run against the stub |
| U-R2 Ledger lost or unreadable at relaunch: list conversations from `thread/list`, labelled "App history unavailable" (PROPOSED); whether that list is filtered by project `cwd` | App execution/recovery owner | Before implementation | R-1 failure row |
| U-R3 Ledger retention and deletion; what a person's deletion of a conversation removes | App execution/recovery owner, with the owner for privacy | Before implementation | Not designed |
| U-R4 Numbers: quit wait limit, stop wait limit, journal size, overlap wait (with HOSTING U-05) | App implementation owner | Before implementation | TEST VALUES in the prototype only |
| U-R5 More than one App window on one conversation: each is an observer (OA per window); whether two windows may both show the stop control | DEL-01-04 | Before DEL-01-04's design | OA is per observer already |
| U-R6 Whether RS records a turn interrupt in an App run, and how | DEL-04-03 | Node F or later | Offered (§8.2) |
| U-R7 TBD-002 persistence technology and location | App execution/recovery owner with the supplier-integration owner | Before implementation | Format PROPOSED only |
| U-R8 OI-008 process division (O-1 PROPOSED, R17-5) | App implementation owner (phase review) | Before architecture production | Requirements stated apart from placement |
| U-R10 Whether the journal of a **closed** generation stays re-readable for the rest of the App session (it would let DEL-01-03 replay checklist plan updates after a supplier restart, NPTD RV-4 and D2's J-3). This file says no: OA-02 rebuilds from Codex history, so checklist revisions of a closed generation are "not recoverable" as after a relaunch. Keeping them would stay within R17-4 (memory only) at the cost of the journal bound | Integrator, with DEL-01-03 | Node F | OA-02 as written |
| U-R11 Other deliverables' App-kept records (for example DEL-02-04's supply-record log, D6) are kept by their owners, not in this ledger: holding another deliverable's format here would make DEL-01-02 consume it, and DEL-02-04, DEL-02-02 and DEL-04-02 all reach DEL-01-02 in DAG-003 (an SCC). The relaunch sequence offers what they need as runtime values: R-6's resume inputs and the `observation_recovered` events | Integrator | Node F | §7 lists only this deliverable's entries |
| U-R9 The person's explicit "restart Codex" control (DEF-5a outside a quit): whether DEL-01-05 (settings changes) or DEL-01-04 offers it; it asks first with live work, as quit does (PROPOSED) | DEL-01-04 / DEL-01-05 | Their design | DEF-5a covers it |
