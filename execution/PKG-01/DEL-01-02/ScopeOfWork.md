---
schema: chirality-deliverable-sow/v1
deliverable_id: DEL-01-02
package_id: PKG-01
decomposition_basis: execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z
project_scope_refs: [SOW-007, SOW-008, SOW-060, SOW-061, SOW-062, SOW-063, SOW-064, SOW-065, SOW-066, SOW-122, SOW-123, SOW-124, SOW-125]
package_objective_refs: [OBJ-001, OBJ-002, OBJ-005]
---

# DEL-01-02 — Durable execution and request recovery

## Purpose and Objective Traceability

This deliverable keeps work going when nobody is watching it and keeps the App truthful about what happened. Closing a window ends observation and nothing else. Work stops only when the person stops it. After a window is lost, a Codex process stops or the App is relaunched, the person sees the actual state read back from Codex, sees every request that was left unanswered as unanswered, and can continue the conversation with what went before in view.

It is the BACKEND_FEATURE_SLICE `DEL-01-02` of PKG-01 in the accepted decomposition, serving OBJ-001 (recoverable interaction in the workflow-making loop), OBJ-002 (main-process execution in the chosen architecture) and OBJ-005 (truthful request and outcome evidence).

| Accepted scope | Contribution | Source |
|---|---|---|
| SOW-060, SOW-122 | Window loss ends observation; main-process work and requests survive | PRD V4-EXE-01; ARCHITECTURE §3 properties |
| SOW-007, SOW-061 | Interruption is the person's explicit act | PRD V4-APP-01, V4-EXE-01 |
| SOW-063, SOW-064 | Every request is answered or explicitly declined; silence never approves | PRD V4-EXE-02 |
| SOW-123 | An unknown server request gets an explicit error | ARCHITECTURE §3 properties |
| SOW-062, SOW-124 | Recovery reads actual state and outstanding requests from Codex | PRD V4-EXE-01; ARCHITECTURE §3 properties |
| SOW-008, SOW-066 | After a restart the conversation continues with prior events accessible | PRD V4-APP-01, V4-EXE-04 |
| SOW-065 | Observed events and unknown outcomes stay distinct | PRD V4-EXE-03 |
| SOW-125 | The required restart and request behaviour holds whatever code implements it | ARCHITECTURE §3 reuse candidates |

Its examination scenario is EXAMINATION V4-EXM-11.

## Deliverable Definition — Ontology

- **OUT-001** — Main-process custody of each Codex child's work and outstanding requests across the loss of any window, including answer and decline handling and the record of an unknown request's error. Supports SOW-060, SOW-063, SOW-064, SOW-122, SOW-123; OBJ-001, OBJ-002, OBJ-005.
- **OUT-002** — The person's interrupt of a turn, the question asked before a quit or a Codex stop with live work, the stop that follows, and recovery of each conversation after a Codex restart or an App relaunch. Supports SOW-007, SOW-008, SOW-061, SOW-062, SOW-066, SOW-124; OBJ-001, OBJ-002.
- **OUT-003** — The settlement and observation-loss fixtures: stand-in supplier peers and recorded exchanges that drive each failure transition, and the results of running them on an identified candidate. Supports SOW-007, SOW-008, SOW-060, SOW-061, SOW-062, SOW-063, SOW-064, SOW-065, SOW-066, SOW-122, SOW-123, SOW-124; OBJ-001, OBJ-002, OBJ-005.
- **OUT-004** — The App ledger and the custody facts handed to receivers: custody events, stop requests, request endings and owners' tags, in this deliverable's own format. Supports SOW-063, SOW-064, SOW-065, SOW-124, SOW-125; OBJ-001, OBJ-002, OBJ-005.

Terms. These are the definitions other scopes rely on.

- **Observer loss.** A window closes, hides or reloads, or the channel between the web view and the main process is lost. It is not a stop and sends nothing to Codex. Re-attachment resumes from the observer's position; where the position is no longer held, the observer gets a snapshot and a gap marker.
- **Interrupt a turn.** The person's act on one live turn. The turn ends as Codex reports it; the conversation, and any workflow run in it, continues. It is not a run end, not an approval or decline of any request, and not a reserved human act. A turn that Codex ends after the person's cancel answer to a tool-permission request is not an interrupt; its outcome carries that cause.
- **End a run.** Defined by `DEL-02-03`. Nothing in this deliverable ends a run: not an observer loss, an interrupt, a Codex stop, a quit or a relaunch.
- **Stop the Codex process.** For one App-owned Codex home. *Deliberate*: after a confirmed quit or the person's Stop Codex or Restart Codex; live turns are interrupted first, then the process tree is ended. *Unexpected*: the child ends with no App stop request. Neither ends a run and neither answers a request.
- **App quit.** The person quits. With a live turn, an outstanding request or an active delegated child, the App asks first and lists them. Closing the last window is an observer loss, not a quit.
- **Relaunch.** A new App session. The earlier processes do not survive, and no unattended execution after a quit is promised.
- **Request endings.** Answered or declined by the person; errored as unknown; resolved by Codex itself; *ended unanswered* when its process stopped; or *reply outcome unknown* when a reply's write was admitted but never observed.
- **App ledger.** The pointers and App-observed facts the App keeps across relaunch: conversations and their homes, generations, request summaries and endings, stop requests, session markers and tags. It is append-only, kept in a SQLite database in the App's own user data, and is operational state, not a record. It holds no conversation content and is never the authority for what Codex holds.
- **Tag.** An opaque value an owner attaches to a conversation, kept in order and never interpreted here. `DEL-02-03` tags a conversation with each run reference.

Boundary:

- **CLM-001** — One coupled lifecycle belongs here: custody across observer loss, the stop definitions, the question before a quit or stop, recovery, the ledger and the custody facts. It lasts longer than a generation or a window; the life of one generation is `DEL-01-01`'s.
- **CLM-002** — `DEL-01-01` creates every register entry at receipt, writes the explicit error to an unfamiliar request, defines entry meaning and the answer write path, and supplies lifecycle, exit and descendant facts. This deliverable keeps those entries in custody, records their endings and writes no error of its own.
- **CLM-003** — `DEL-01-04` presents request cards, the interrupt control, the quit question and Stop Codex and Restart Codex. `DEL-01-03` presents plans, tools and descendants. `DEL-04-03` owns the run-record format and writer and `DEL-04-01` the operation policy. `DEL-02-03` owns runs. `DEL-01-05` owns the App-owned homes.
- **CLM-004** — Execution, proposal acceptance, checking, approval and professional reliance are separate acts with their own actors. A recorded answer names the person who gave it apart from the recorder. Routine tool permission is the person's own Codex setting and never stands for a reserved act.
- **CLM-005** — The App is hosted directly on stock Codex. The v3 Runtime service and socket are not reinstated, and v3 client code is an optional source that qualifies only by meeting these criteria.

## Completion and Reliance Basis — Epistemology

- **REQ-001** — Each Codex child, its protocol session and its outstanding requests stay in main-process custody. Closing, hiding or reloading a window preserves ongoing work and outstanding approvals and sends Codex nothing. Window visibility and execution state are separate facts.
- **REQ-002** — The person can interrupt a live turn. The request, its transmission and the observed result are kept apart, and the turn is reported as Codex reported it or as unknown. With several windows on one conversation the first press settles the interrupt and a later press is refused with the turn's state. The end of a primary turn is never reported as the end of its descendants. Items a turn opened and did not complete are stated as not completed.
- **REQ-003** — Every request Codex raises is answered or explicitly declined through the native protocol, and stays outstanding across observer loss. The actual grant, denial, answer or decline is preserved. Silence, timeout, re-attachment and restart never approve. No request is declined automatically after any period, at a stop or at a quit; a request still pending when its process stops ends unanswered and is never answered afterwards, in that generation or a later one.
- **REQ-004** — The result of the explicit error written to an unknown server request is recorded and kept in custody. A local settlement or a reply write is never reported as an acknowledgment received.
- **REQ-005** — After a Codex restart or an App relaunch each conversation's state is read back from Codex, from the home it belongs to, and never rebuilt from an App copy. The person can continue the conversation with prior events accessible. A resume sends no changed guidance. When the person quits, or stops or restarts Codex, with live work, the App asks first and lists the live turns, outstanding requests and active children; on confirmation live turns are interrupted and recorded with that cause, and after relaunch they are shown as interrupted by the quit with an offer to resume. At a deliberate stop the supplier's whole process tree is ended; after an unexpected exit, surviving descendants are reported to the person and are not ended by rule.
- **REQ-006** — Receivers get observed events and explicitly unknown outcomes: custody events, stop requests, request endings and tags. Across relaunch the App keeps only pointers and App-observed facts, never conversation content. An evidenced human answer keeps its actor distinct from the recorder. Execution, transport success and recovery create no acceptance, checking, approval or reliance, and no independently evidenced act is left out of what is handed over because another act is absent. Recovery of a conversation is never presented as recovery of a branching undertaking's ownership, returns, review or active descendants.
- **REQ-007** — The restart and request-answering behaviour above holds on the stock supplier boundary, without the v3 Runtime service, whether or not v3 client logic is reused.
- **REQ-008** — Each failure transition of this lifecycle is exercised on the identified candidate, and each result is reported as passed, failed, blocked, not run or inconclusive, as observed.
- **REQ-009** — This deliverable performs no act that CLM-002 and CLM-003 give elsewhere: no pin selection or protocol generation, no card or view, no run-record format or writer, no policy, no run end.

- **AC-001** — With a turn running and an approval outstanding, closing, hiding and reloading the window leave the turn running and the approval pending under the main process, and nothing is written to Codex because of the window. Verify by VER-001. [REQ-001]
- **AC-002** — An interrupt the person makes is reported with its request, transmission and observed result; it is distinguishable from an observer loss and from a run end; the run it belongs to is still open; a descendant still active is shown as active; and a second press from another window is refused. Verify by VER-002. [REQ-002]
- **AC-003** — A grant, a denial, a question's answer and an explicit decline each reach Codex as given; a request left waiting through silence, a window loss and a re-attachment is still waiting; and a request pending at a stop is shown ended unanswered after restart and cannot be answered. Verify by VER-003. [REQ-003]
- **AC-004** — An unknown server request's explicit error and its result are held across window loss and relaunch, and a reply whose acknowledgment was not observed is not reported as acknowledged. Verify by VER-004. [REQ-004]
- **AC-005** — After a Codex restart, with stale rendered state and a stale ledger entry present, the state shown agrees with what Codex returns for that conversation, and where Codex returns nothing the outcome is shown unknown. Verify by VER-005. [REQ-005]
- **AC-006** — A quit with live work asks first and lists it; after confirmation and relaunch the person continues the conversation, sees what happened before, sees the turns the quit interrupted as interrupted by quit, sees no request answered that was pending at the stop, and the tags attached to the conversation before the quit are returned in the same order. After an unexpected exit a surviving descendant is reported and still running. Verify by VER-006. [REQ-005]
- **AC-007** — What receivers are handed contains only observed events and stated unknowns; an answer the person actually gave is handed over with the person as actor and the recorder distinct; no handed-over fact asserts a human act from execution success, a transport reply, a lost acknowledgment or a recovered conversation; an evidenced act is handed over whether or not any other act is evidenced; and the ledger holds no conversation content. Verify by VER-007. [REQ-006]
- **AC-008** — Window loss, interruption, known and unknown requests, denial, timeout, re-attachment, restart and missing acknowledgment each have a result on the identified candidate with one of the five outcomes. Verify by VER-008. [REQ-008]
- **AC-009** — The candidate meets AC-001 through AC-007 with Codex hosted directly by the App and no separate runtime service, and none of the acts in REQ-009 is produced by this deliverable's code. Verify by VER-009. [REQ-007, REQ-009]

## Production and Verification Method — Praxeology

Seam behaviour is driven by stand-in supplier peers and by exchanges recorded from the stock supplier. Interruption, quit and relaunch are witnessed on the native App; browser evidence does not stand in for a native restart. Every result names the candidate, the pin and the date. The fixtures realise these criteria and add no wire field or timing threshold of their own.

- **VER-001** — Executable check (observes the child process, the register and the bytes written to Codex): with work running and an approval pending, close, hide and reload the observer window and compare before and after.
- **VER-002** — Executable check (observes the interrupt request, its write and Codex's reported turn end): interrupt a turn, contrast an observer loss and a withheld acknowledgment, keep a descendant active past the primary turn's end, and press interrupt from a second window.
- **VER-003** — Comparison with the replies Codex actually received: exercise grant, denial, answer and decline, leave a request waiting through silence and a window loss, and stop the process with a request pending.
- **VER-004** — Executable check (observes the error frame and the reported settlement): send an unknown server request, lose the window and relaunch; withhold the acknowledgment of a written reply.
- **VER-005** — Comparison with Codex's own history: restart Codex with work and requests outstanding and with deliberately stale rendered and ledger state, and compare what is shown with what Codex returns.
- **VER-006** — Judgment by an examiner on the native App: quit with live work, confirm, relaunch, continue the conversation, look up the conversation's tags, and compare what is shown and returned with what the examiner saw and attached before the quit and with Codex's history; end the child unexpectedly with a descendant running.
- **VER-007** — Comparison with an act the examiner watched: hand over one actually given answer and cases with no human evidence, transport-only success, a lost acknowledgment and a recovered conversation; inspect the handed-over facts and the ledger's contents.
- **VER-008** — Judgment by an independent reviewer: read the candidate's results against the transitions AC-008 names and trace each to its observation.
- **VER-009** — Judgment by an independent reviewer: confirm the process topology on the candidate and trace each act of REQ-009 to its owner's code.

## Governing Values and Decisions — Axiology

- **AX-001** — Work survives everything except the person's own stop. Better means fewer ways a turn or a pending request can be lost to a window, a process exit or a relaunch, and never by answering, declining or resuming anything on the person's behalf.
- **AX-002** — Recover what was observed and keep what is unknown explicit. Better means fewer conversations and requests left unknown after recovery, and never by filling an unobserved outcome from a transcript copy, a local settlement or a reply write. No exactly-once effect on anything outside the App is promised.
- **AX-003** — The App keeps as little of Codex's content as it can. Better means a smaller ledger that still recovers every conversation, and never by keeping conversation content or treating the ledger as authority.
- **TBD-002** — How long ledger entries are kept, how they are deleted, and what a person's deletion of a conversation removes are undecided (execution/recovery owner, with the owner for privacy).

## Output and Evaluation Matrix

| Output | Objective refs | Requirement/claim refs | Acceptance refs | Verification refs | Evidence expectation |
|---|---|---|---|---|---|
| OUT-001 | OBJ-001, OBJ-002 | REQ-001, CLM-001 | AC-001 | VER-001 | The child's state as the operating system reports it and the bytes written at its pipe, before and after each window event, compared with PRD V4-EXE-01: work and the pending approval persist and nothing is written to Codex because of the window. |
| OUT-002 | OBJ-001 | REQ-002 | AC-002 | VER-002 | Outside source: the turn end Codex itself reports, and the frames recorded at the pipe. |
| OUT-001 | OBJ-001, OBJ-005 | REQ-003, CLM-004 | AC-003 | VER-003 | Outside source: the replies the supplier, or the stand-in peer, actually received. PRD V4-EXE-02 states what may never approve. |
| OUT-001 | OBJ-001, OBJ-002, OBJ-005 | REQ-004, CLM-002 | AC-004 | VER-004 | Outside source: the error frame and acknowledgment as recorded at the pipe. |
| OUT-002 | OBJ-001, OBJ-002 | REQ-005 | AC-005 | VER-005 | Outside source: Codex's own history for the conversation, read independently of the App's views and ledger. |
| OUT-002 | OBJ-001 | REQ-005 | AC-006 | VER-006 | Outside source: what the examiner observed before the quit, Codex's history, and the operating system's process list. EXAMINATION V4-EXM-11 states what must happen. |
| OUT-004 | OBJ-001, OBJ-005 | REQ-006, CLM-004 | AC-007 | VER-007 | Outside source: the answer the examiner watched the person give. PRD V4-EXE-03 and V4-AUT-03 state what may not be asserted. |
| OUT-003 | OBJ-001, OBJ-002, OBJ-005 | REQ-008 | AC-008 | VER-008 | An independent reviewer's reading of the candidate's results against the transitions named by the accepted decomposition's `DEL-01-02` row and EXAMINATION V4-EXM-11 and the outcome labels of EXAMINATION §1, tracing each result to an observation the product did not write. A result with no such observation establishes nothing about its transition. |
| OUT-004 | OBJ-001, OBJ-002, OBJ-005 | REQ-007, REQ-009, CLM-003, CLM-005 | AC-009 | VER-009 | An independent reviewer's inspection of the candidate's process topology against ARCHITECTURE V4-ARC-03, and trace of each act of REQ-009 to its owner's code, compared with the allocation in the accepted decomposition's Deliverables rows. |
