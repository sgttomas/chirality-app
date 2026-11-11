---
schema: chirality-deliverable-sow/v1
deliverable_id: DEL-06-02
package_id: PKG-06
decomposition_basis: execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z
project_scope_refs: [SOW-085, SOW-086, SOW-087, SOW-088, SOW-089]
package_objective_refs: [OBJ-006]
---

# Return, waiting and human-decision workspace

## Purpose and Objective Traceability

This deliverable is where the person coordinating delegated work sees what has come back, what is waiting and why, and what is theirs to decide. It contributes three views in the App, each rebuilt from files whenever it is read: the queue of returns awaiting examination; every selected work item with the cause its records give for its state; and each decision prepared for the person, naming the exact act asked, the alternatives and their consequences, with the decision the person actually made once it is recorded. The views hold nothing of their own. Closing the App, losing a conversation or discarding a view loses no coordination state, and nothing a view shows makes a return reviewed, a piece of work integrated or a decision made.

It is the UX_UI_SLICE `DEL-06-02` of PKG-06 in the accepted decomposition, owned by the App fleet-experience owner, serving OBJ-006 (bounded fleet work and its decisions recoverable from file-based coordination records).

| Accepted scope | Contribution | Source |
|---|---|---|
| SOW-085 | Returned work awaiting examination is a visible queue | PRD V4-PM-03 |
| SOW-086 | Waiting work is explained by its cause | PRD V4-PM-03 |
| SOW-087 | Decision packages state the exact act, the alternatives and the consequences | PRD V4-PM-04 |
| SOW-088 | Coordination status is recovered across sessions from files | PRD V4-PM-05 |
| SOW-089 | Coordination views are built from files, can be rebuilt and are never the authority | PRD V4-PM-06 |

Other sources are PRD V4-AUT-03, V4-CON-03, V4-REC-02, V4-REC-03 and V4-REC-05; HOST_INTEGRATION V4-HI-33 and V4-HI-62; ARCHITECTURE §3, which keeps conversation recovery apart from recovery of an undertaking; and EXAMINATION V4-EXM-13.

## Deliverable Definition — Ontology

- **OUT-001** — The return-review queue and the waiting view. Supports SOW-085, SOW-086, SOW-088, SOW-089; OBJ-006.
- **OUT-002** — The decision-package view. Supports SOW-087, SOW-088, SOW-089; OBJ-006.
- **OUT-003** — Queue, waiting, decision and cross-session rebuild fixtures, with their results on an identified candidate. Supports SOW-085, SOW-086, SOW-087, SOW-088, SOW-089; OBJ-006.
- **OUT-004** — The derivation account: for each thing a view shows, the files it comes from, what is never an input, and who owns the review, the integration and the decision that the view displays. Supports SOW-085, SOW-086, SOW-087, SOW-088, SOW-089; OBJ-006.

Terms:

- **Return-review queue.** One row for each recorded return that no integration record names, including several returns on one item. A row enters only on a return record and leaves only on an integration record that names that return. It shows the item and its outcome; its state (awaiting review; reviewed, findings to repair; review not concluded; reviewed, awaiting integration); who returned the work and who recorded the return; the reviewer, once a review is recorded; who examines it; and its source records.
- **Who examines.** The examiner as the records establish it. Where no record establishes one, the row says the examiner is not established. The item's owner is never shown in the examiner's place.
- **Waiting view.** Every selected item of the current graph, with its owner, what comes next and the causes its records give, each cause quoting its source record:

  | Shown as | When |
  |---|---|
  | done | an integration of its return, or an external result, is recorded |
  | returned | a return is recorded and not integrated |
  | unknown | a need cannot be established, the brief it names cannot be found, or the records were not fully read |
  | waiting | a need is outstanding, or an external owner has recorded no result |
  | ready | every need is satisfied and no dispatch, return or integration is recorded |

  Unknown takes precedence over waiting. An item with a dispatch observed and no return shows what was last observed of the child, or that observation ended, and is never shown as ready or returned. A cause the records do not give is shown as not established.
- **Ready, with a limit.** While a child is observed that no record ties to a brief, no row is presented as plainly ready: each ready row carries a stated limit that a dispatch for the item may be unrecorded. Ready describes file prerequisites only and grants no permission.
- **Incomplete records.** While any coordination-log line is unread, records conflict, or the files changed during the read, no row is ready, every row that is not done is unknown, and the queue is marked incomplete. An empty or short queue is then never presented as the whole.
- **Decision package.** A project file an agent prepares for a decision reserved to the person. It names the exact act requested, its subject, its purpose and scope, the basis that reserves the decision, and two or more alternatives, each with its consequences. It holds nothing its recorder supplies and is no record of any act. It reaches the view through the request record that cites it by path and content identity.
- **Decision row.** One row for each package. A *pending* row shows the exact act requested, the subject, purpose, scope and basis, and every alternative with its consequences. A row is *decided* only when a recorded act of the person, of the kind the package names, cites the package's request and, for a decide act, chooses an alternative the package names. It then shows the alternative chosen, the person as decision actor with the identity marked not verified, the recorder separately, the capture time and the lapse state. An act of another kind, or one that chooses an alternative the package does not name, is listed and decides nothing.
- **Several decisions.** A later decision on the same package supersedes an earlier one only where the records themselves establish their order; file order, timestamps and identifiers do not. Decisions whose order the records do not establish are shown unresolved. A correction stands in place of the entry it corrects, and both stay listed.
- **Lapse.** A decided row shows the lapse state that `DEL-04-03`'s reading gives for the package file's current content against the content the decision was bound to: an absent file shows lapsed (subject absent), and an identity that is not comparable or not obtainable shows unknown. A lapsed decision stays listed.
- **Never an input.** Conversation text, including an agent's statement that work is done or that the person decided; Codex's native status, except as the fleet records hold it; an answer to a supplier's question; and any connector's projection.

Boundary:

- **CLM-001** — `DEL-06-01` owns the fleet records: their formats, the reading of them as one snapshot with its limits, which graph is current, which entries are App observations, and what satisfies each kind of need. This deliverable evaluates and presents, and writes no fleet record. A native observation is evidence of its own subject and of nothing about return, review or integration.
- **CLM-002** — `DEL-04-01` owns the names of the acts and the rule for their wording. `DEL-04-03` owns the request, act and lapse records and the reading of them. `DEL-01-04` owns the App act control: from a pending row the person can open that control on the package, and the control composes its own offer and captures the act. This deliverable captures nothing and operates no control. The person performs the decision, and the accountable professional owns professional reliance.
- **CLM-003** — Managers own review and integration and record their own; the views show those records. `DEL-09-05` owns the joined fleet and longer-work witness on a candidate, and the fixtures here are local to these views.
- **CLM-004** — `DEL-07-02` owns the connector standing vocabulary and the source-file route. `DEL-10-02` owns file-native undertaking practice and `DEL-10-04` the project dependency graph; neither waits for these views. A connector is an input only where a work item declares a need on its record.

## Completion and Reliance Basis — Epistemology

- **REQ-001** — The queue shows each return awaiting examination with its recorded ownership and its review standing. A child Codex reports completed, an ended observation, a success message, a rebuild or the removal of an item from the graph never moves a return into or out of the queue and never marks it reviewed or integrated. [SOW-085; PRD V4-PM-03; CLM-001; CLM-003]
- **REQ-002** — The waiting view explains each selected item by the cause its records evidence, with the item's owner. Dependent work, ready work and returned work stay distinguishable. A missing record, an unread line, absent act records, or a connector that is absent or limited produces a stated limit, and never readiness, an empty queue or permission. [SOW-086; PRD V4-PM-03, V4-CON-03; HOST_INTEGRATION V4-HI-62; CLM-001]
- **REQ-003** — A decision package is shown with the exact act requested, its subject and basis, its alternatives and their consequences, and whether it is pending or decided. Accepting a proposed edit reads "accept" and never "approve"; choosing an alternative reads "decide". Applying an operation, accepting an edit, checking, approval and professional reliance are shown as separate acts with their own actors and evidence, and neither an operation's success nor a view shows any of them. [SOW-087; PRD V4-PM-04, V4-AUT-03; HOST_INTEGRATION V4-HI-33; CLM-002]
- **REQ-004** — An act a person performed is presented from its record, with the decision actor apart from the recorder and with its content, scope and purpose binding and its lapse visible. No act is shown that no record holds. Each evidenced act keeps its own standing, and the view requires no act to precede another. [SOW-087; SOW-089; PRD V4-AUT-03, V4-REC-05; CLM-002]
- **REQ-005** — The views are derived, each time they are read, from the project's fleet files, the decision packages in the project and the App's records store, and they keep no state of their own. Rebuilt in another session from the same files they show the same rows, preserving ownership, returns awaiting review, what was reviewed and integrated, pending decisions and the items a changed basis affects. Reading or rendering a view writes no file and no record and performs no act. A recovered conversation or a native observation is never shown as recorded coordination. [SOW-088; SOW-089; PRD V4-PM-05, V4-PM-06, V4-REC-02, V4-REC-03; CLM-001; CLM-002; CLM-003]
- **REQ-006** — The views need no connector. A connector need is shown from the declared standing of its record and never from the record's presence, and satisfying it makes no item ready while another need is outstanding. A connector's absence or limited standing cancels no manager's review or integration ownership. [SOW-088; SOW-089; PRD V4-CON-03; HOST_INTEGRATION V4-HI-62; CLM-003; CLM-004]
- **REQ-007** — This deliverable shall perform no act owned by another deliverable. Defining, reading and writing the fleet records belongs to `DEL-06-01` (CLM-001). Naming the acts belongs to `DEL-04-01`, the request, act and lapse records to `DEL-04-03`, and capturing a person's act to `DEL-01-04` (CLM-002). The joined fleet witness belongs to `DEL-09-05` (CLM-003). Connector standing and the source-file route belong to `DEL-07-02`, undertaking practice to `DEL-10-02` and the project dependency graph to `DEL-10-04` (CLM-004). Review and integration stay with the managers who perform them (CLM-003); the decision stays with the person and professional reliance with the accountable professional (CLM-002).

- **AC-001** — Given a recorded return with no integration, the queue shows it awaiting review with who returned it, who recorded it and who examines it. A return for which no record establishes an examiner shows the examiner as not established, and never the item's owner in that place. A child reported completed with no return recorded is not queued. The row leaves only when an integration naming that return is recorded. Verify by VER-001. [REQ-001]
- **AC-002** — In a fixture holding an item that waits on another item, one that waits on a decision the person has not yet made, one returned and one with every need met, the first two are shown waiting, the third returned and the fourth ready, each with its cause and its owner. With a child observed that no record ties to a brief, the item with every need met is not presented as plainly ready: if shown ready, it carries a stated limit that a dispatch for it may be unrecorded. With one log line made unreadable, no item is ready and the queue is marked incomplete. With the act records absent, the decision wait is unknown and not ready. Verify by VER-002. [REQ-002]
- **AC-003** — A pending package is shown with the exact act, subject, purpose, basis and every alternative with its consequences, as its file states them; an alternative with no consequence is shown as having none stated; and a package that asks for acceptance of a proposal reads "accept" and nowhere "approve". Verify by VER-003. [REQ-003]
- **AC-004** — A decision the person performed at the App act control is shown decided, with the alternative chosen, the person as actor with identity not verified, and the recorder apart. After the package file is edited the decision is shown lapsed and is still listed. An agent's message claiming a decision, a tool's success, an act of another kind that cites the package, and an act choosing an alternative the package does not name each leave the row pending. A separately recorded act is shown without any decision being required before it. Verify by VER-004. [REQ-003; REQ-004]
- **AC-005** — The views rebuilt in a separate session from the same files show the same rows, and every input file is byte for byte unchanged by the rebuild. After an interruption and a changed basis, the rebuilt views show the return, the review and integration recorded, the owners, the waiting causes and the pending decisions as the records hold them, with the changed basis marked on the items it names and an ended observation shown as an unknown outcome. A recovered conversation adds nothing to them. Verify by VER-005. [REQ-005]
- **AC-006** — With no connector and no connector record present, the views are rebuilt from the files. For an item that declares a connector need: a missing record shows it waiting; an unreadable record, one whose standing does not conform, or one from another connector shows it unknown; a record whose standing supports reliance shows the need satisfied, with any claim not relied on and any source-file route still needed named; and the item is not ready while another of its needs is outstanding. No other row changes. Verify by VER-006. [REQ-006]
- **AC-007** — The derivation account names, for each element a view shows, its source records, what is never an input and the owner of each act displayed. None of the acts REQ-007 leaves elsewhere is produced by this deliverable's code, and the fixture results are reported as results for these views, never as the joined fleet witness. Verify by VER-007. [REQ-007]

## Production and Verification Method — Praxeology

The Rust host derives every view from one snapshot of the files, and the web view presents what it is handed and supplies no path. Each row carries its source records, so that what a row says can be traced to a file and a line. Reading the decision view records no request and repairs no record; recording is a separate operation of the record writer. Fixtures use invented records. A test cannot press the person's confirmation: a check that stands in for it examines presentation only, and the positive case of AC-004 needs an act a person performed. No layout is fixed here.

- **VER-001** — Executable check (observes the queue's rows for hand-written fleet records): a return awaiting review, a return for which no record establishes an examiner, a child reported completed with no return, and the same return after its integration is recorded.
- **VER-002** — Executable check (observes each item's shown state, causes and owner for a hand-written fixture): then with an unassociated child observed, with one log line made unreadable, and with the act records absent.
- **VER-003** — Comparison with a named reference (the package file as written): compare a pending row with its file element by element, and read every label on a package that asks for acceptance of a proposal.
- **VER-004** — Comparison with a named reference (a decision a person performed at the App act control, with its record): compare the decided row with that record and the observed act, edit the package file and read the lapse; plus an executable check of the four cases that must leave a row pending and of a separately recorded act.
- **VER-005** — Executable check (observes the rows of two rebuilds made in separate sessions from the same files, and the rows after an interruption and a changed basis against what the fixture's records were written to establish), with the input files' bytes compared before and after by a tool that imports no product code.
- **VER-006** — Executable check (observes the rows for a fixture with no connector, and for an item declaring a connector need whose record is missing, unreadable, nonconformant, from another connector, and supporting reliance with and without a claim not relied on).
- **VER-007** — Judgment by a named role (an independent reviewer): read the derivation account against the views' inputs in the product, trace each act of REQ-007 to its owner's code, and read the fixture reports for any claim beyond these views.

## Governing Values and Decisions — Axiology

- **AX-001** — The files hold the coordination and a view is a recoverable projection of them. Better means fewer rows left unknown where the records do establish the state; never by showing something the records do not hold.
- **AX-002** — The person's decision rights are untouched: a view prepares and presents and never performs. Better means the person has less to look up elsewhere before deciding, because the row gives the act, the basis, the alternatives, the consequences and the current standing; never by choosing or suggesting an alternative, implying a decision, or showing one act as another.
- **AX-003** — Limits are shown where they fall. Better means a larger share of unknown rows name the record that would settle them; never by hiding a limit to present a complete-looking queue.
- **AX-004** — Coordination is recovered from the project's files and the records store alone. Better means fewer view behaviours that depend on anything else; never by making a connector, a conversation or a running agent a condition of seeing what is owed.
- **AX-005** — An imported or recovered record stays what it is. Better means more of an imported undertaking's history can be read; never by showing a record that entered through an import package or a restored project identity as this App's observation or this person's act.
- **TBD-003** — Whether fleet management goes beyond the accepted option is undecided (owner; PRD OQ-06). No scheduling, staffing or further management feature is part of these views.
- **TBD-005** — Which record establishes who examines a return before a review of it is recorded is undecided (owner). Until decided a row names an examiner only where a record states one.

## Output and Evaluation Matrix

| Output | Objective refs | Requirement/claim refs | Acceptance refs | Verification refs | Evidence expectation |
|---|---|---|---|---|---|
| OUT-001 | OBJ-006 | REQ-001, CLM-001, CLM-003 | AC-001 | VER-001 | The queue's rows for fleet records written by hand as files, each to establish one stated fact, compared with those statements and not with an earlier queue. |
| OUT-001 | OBJ-006 | REQ-002, CLM-001 | AC-002 | VER-002 | Each item's shown state, causes and owner, compared with the state the fixture states in advance from the need definitions `DEL-06-01` owns and the waiting-view definitions above. |
| OUT-002 | OBJ-006 | REQ-003, CLM-002 | AC-003 | VER-003 | Each element of a pending row compared with the package file as its author wrote it, and every label on a package that asks for acceptance read against the wording REQ-003 requires. |
| OUT-002 | OBJ-006 | REQ-003, REQ-004, CLM-002 | AC-004 | VER-004 | The decided row compared with a decision a person performed at the act control and with its record, written by a writer this deliverable does not own; the cases that must leave a row pending checked executably against AC-004. A check that stands in for the person's confirmation examines presentation only. The decided row shows what the record of the act says; whether that record came from the App's own capture rests on `DEL-01-04`'s seal and is not established by the view. |
| OUT-001 | OBJ-006 | REQ-005, CLM-001, CLM-003 | AC-005 | VER-005 | The rows of each rebuild compared with what the fixture's records were written to establish; comparing two rebuilds with each other shows only consistency with the product's own earlier output. Input bytes are compared by a tool that imports no product code. |
| OUT-002 | OBJ-006 | REQ-005, CLM-002 | AC-005 | VER-005 | As the row above, for the decision rows. |
| OUT-001 | OBJ-006 | REQ-006, CLM-003, CLM-004 | AC-006 | VER-006 | Each row's state for the connector cases compared with the state stated in advance from the standing vocabulary `DEL-07-02` publishes; the connector records are written to that vocabulary outside this deliverable. |
| OUT-003 | OBJ-006 | REQ-007, CLM-003 | AC-007 | VER-007 | An independent reviewer reads the fixture reports for any claim beyond these views, including any claim to the joined fleet witness, which is `DEL-09-05`'s. |
| OUT-004 | OBJ-006 | REQ-007, CLM-001, CLM-002, CLM-003, CLM-004 | AC-007 | VER-007 | An independent reviewer compares the derivation account with the views' inputs found in the product and traces each act REQ-007 leaves elsewhere to its owner's code, against the allocation in the decomposition's Deliverables.csv and CLM-001 to CLM-004. |
