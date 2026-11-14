---
schema: chirality-deliverable-sow/v1
deliverable_id: DEL-01-03
package_id: PKG-01
decomposition_basis: execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z
project_scope_refs: [SOW-001, SOW-003, SOW-004, SOW-006, SOW-014, SOW-128, SOW-129]
package_objective_refs: [OBJ-001, OBJ-002]
---

# DEL-01-03 — Native plans, tools and delegation views

## Purpose and Objective Traceability

This deliverable lets the person see what Codex is planning, doing and delegating, in Codex's own terms, and direct it. The App shows Codex's plans and their revisions, its tool activity with the outcome actually observed, and its sub-agents with their own state, and it offers plan mode as the way to ask for a plan and to leave it. Nothing is renamed into a Chirality vocabulary, and nothing is shown as done that was not observed.

It is the UX_UI_SLICE `DEL-01-03` of PKG-01 in the accepted decomposition, serving OBJ-001 (native tool use in the workflow-making loop) and OBJ-002 (native presentation and visible supplier version in the chosen architecture).

| Accepted scope | Contribution | Source |
|---|---|---|
| SOW-001 | The person directs work through truthful native views | PRD §1 |
| SOW-003 | Planning and plan revision | PRD V4-APP-01 |
| SOW-004 | Substantive tool activity and its outcomes | PRD V4-APP-01 |
| SOW-006 | Sub-agent activity and descendant identity | PRD V4-APP-01 |
| SOW-014 | Plans, tools and delegation in native form; requests and outcomes are `DEL-01-04`'s share | PRD V4-APP-04; ARCHITECTURE V4-ARC-05 |
| SOW-128 | Plan visibility and revision, and the visible supplier version; `DEL-01-01` supplies and verifies the version. Registry storage and checker implementation are design choices | ARCHITECTURE §3 |
| SOW-129 | The plan interaction the workflow-making experience receives; requests, outcomes, attachments and drafts are `DEL-01-04`'s share. Reuse of earlier interface code is conditional | ARCHITECTURE §3 |

Other sources are PRD V4-EXE-03, V4-AUT-03 and V4-ROLE-03, and the plan, tool and descendant observations of EXAMINATION V4-EXM-10, V4-EXM-11 and V4-EXM-13.

## Deliverable Definition — Ontology

- **OUT-001** — The native views: the plan view with its revisions, tool activity rows, the delegation view, and the supplier version line. Supports SOW-001, SOW-003, SOW-004, SOW-006, SOW-014, SOW-128, SOW-129; OBJ-001, OBJ-002.
- **OUT-002** — Presentation fixtures: exchanges recorded from the stock supplier at the pin for representative plans and revisions, tool outcomes and descendants, and the results of replaying them through the views on an identified candidate. Supports SOW-003, SOW-004, SOW-006, SOW-014, SOW-128; OBJ-001, OBJ-002.
- **OUT-003** — The native feature and optional-UI-reuse map, and what the views offer to receivers. The map names each required plan, tool and delegation interaction, who supplies and who receives it, the native type and version basis, and each decision to reuse or not reuse earlier code. The offers are the plan-mode element and item anchors for turn composition and request cards, the plan-revision reference for the workflow workspace, the delegation availability reading, and descendant identities for the fleet records. Supports SOW-003, SOW-006, SOW-014, SOW-128, SOW-129; OBJ-001, OBJ-002.

Terms:

- **Plan item.** The plan Codex produces in plan mode, one per plan-mode turn. It is kept in Codex history, and each completed plan item is one revision, identified from Codex's own thread, turn and item identities so that the same identity is derived live and from history.
- **Checklist.** The step list Codex may publish during a turn, sent whole each time. Each one received is a revision of that turn's checklist. Codex does not keep checklists in its history.
- **Plan-mode element.** The value this deliverable offers for a turn's collaboration mode: plan, default, "not offered" with its reason, or "no model selected". It never carries developer instructions, so Codex's built-in plan text and the conversation's guidance both stand.
- **Tool row.** One native tool item with its native status shown unchanged, and beside it a display state: in progress, waiting on a request, completed, failed, declined, interrupted, not completed (its turn ended with no completion observed) or unknown.
- **Descendant.** A sub-agent thread Codex started from a conversation, shown with the identity, parent, role and nickname Codex reports and the source of each. When a request arrives on its thread, its role and nickname are what the request card names as who asks (`DEL-01-04`).
- **Delegation availability.** A reading made at run time for a conversation. *Missing* when the selected model's multi-agent version is disabled or the effective configuration turns multi-agent off; *not established* when either was not read; otherwise *present*. Provider capabilities do not enter the reading.
- **Experimental.** A view element is labelled experimental only when it uses a protocol element that exists only in the experimental variant of the pin's generated output. At the pin this is plan mode.
- **Item anchor.** A reference to one native item by Codex's identities, used by request cards and act displays to point at the item they concern.

Boundary:

- **CLM-001** — The views render Codex's native items as delivered. Codex owns the engine; the Rust host reads from Codex and derives the view state in memory, and the web view presents it. This deliverable keeps no file and no copy of Codex history, and it starts no process, composes or sends no turn, answers no request and writes no record. Registry storage, checker implementation and reuse of earlier plan, version-check or interface code are design choices; reused code qualifies only by meeting these criteria on the candidate.
- **CLM-002** — `DEL-01-01` supplies native frames with generation and receipt position, the version identity record and its verification result. `DEL-01-02` supplies execution state, re-attachment after a window is lost, and recovery after a generation closes.
- **CLM-003** — Among native items, this deliverable renders shell commands, file changes, MCP and App-offered tool calls, delegation, planning, goals, web search, image, review and compaction items. `DEL-01-04` renders permission requests, questions to the person and turn outcomes, composes and sends turns using the plan-mode element, and captures any act. `DEL-02-02` owns the workflow-making journey that receives the plan interaction. `DEL-06-01` associates descendant identities with fleet records; fleet graph, return, waiting and decision views are PKG-06's. What this deliverable renders from an agent, a tool or Codex is never presented as the App's own words or controls.
- **CLM-004** — The person directs the work and is accountable for it. Execution, proposal acceptance, checking, approval and professional reliance are separate acts. Routine tool permission is the person's own Codex setting. An instruction to carry out a plan is ordinary conversation input, not a reserved act, unless a workflow checkpoint names an act.

## Completion and Reliance Basis — Epistemology

- **REQ-001** — The person can ask for a plan, revise it, and tell Codex to carry it out, and the observed plan and its revisions stay visible in native form. Leaving plan mode sends the default mode explicitly. Plan items are recovered from Codex history after a relaunch or a Codex restart; checklist revisions, which Codex does not keep, are not copied and are shown as not recoverable.
- **REQ-002** — Substantive tool activity and its observed outcomes are shown from native items. A result Codex did not supply is shown as not supplied; an item whose completion was not observed is shown not completed or unknown, never failed or succeeded. An unfamiliar item kind is shown as unfamiliar with its native content inspectable, never dropped and never mapped to a known kind. A tool result is never presented as a different act.
- **REQ-003** — Sub-agent activity and descendant identities stay visible and are available to the fleet records. Every value an agent, a tool or Codex supplies in the activity (messages, plans, reasoning, output, tool and server names, arguments, paths, diffs, and a descendant's role and nickname) is shown as text the App did not write, marked in what is seen and in what the accessibility layer reports, with its line breaks and control characters made visible and never acted on, so that nothing in the activity can pass for a card or for the App's own words (PRD V4-PM-07). A completed primary turn implies nothing about its descendants: no return, review or integration is inferred. Delegation by an agent given TASK guidance is shown and labelled "stated, not enforced"; the App does not override the person's Codex configuration to prevent it. When delegation is missing the delegation view is absent and one line says why; when it is not established the view appears only if delegation items arrive.
- **REQ-004** — The views show the supplier version and its verification standing as supplied, and are built from the types generated at the pin. "Verified" is shown only from a verified result; an unverified development run is shown as such; a missing or mismatched basis is never shown as compatible. Experimental elements are labelled, and the App is fully usable without them.
- **REQ-005** — The views keep the actor, subject and evidence of each act separate. No act is derived from a native item, a tool success, elapsed time or a session entry; a tool-permission settlement is shown only as that, with its origin; a Codex goal status is never shown as a run end or an act. An act record handed to the views is shown with the person as actor, marked "identity not verified", and the recorder distinct. No order among independently evidenced acts is imposed.
- **REQ-006** — The plan-mode element, item anchors, plan-revision reference, delegation availability and descendant identities are offered in forms their receivers can use without reading this deliverable's view state, and a receiver can check an offered identity against the Codex identities it was derived from. The map accounts for every required plan, tool and delegation interaction, its supplier and receiver, and each reuse decision; similarity of source or an earlier pass qualifies no reused code.
- **REQ-007** — This deliverable performs no act that CLM-002 and CLM-003 give elsewhere, substitutes no agent engine for Codex, decides no policy and performs no person's act.
- **REQ-008** — Presentation checks replay exchanges recorded from the stock supplier at the pin, cover WebKit and Chromium with the packaged App's smoke witness, and report each result as passed, failed, blocked, not run or inconclusive on an identified candidate, naming the candidate, the configuration (supplier pin, model and model server) and the date of each result.

- **AC-001** — On the candidate a plan made in plan mode and each revision are shown as Codex produced them, in order; "carry out this plan" leaves plan mode; and after a relaunch the plan items are shown again from Codex history while checklist revisions are shown as not recoverable. Verify by VER-001. [REQ-001]
- **AC-002** — Successful, failed, declined, interrupted and not-completed tool items and an item with no result supplied are each shown with the native status and the matching display state, an unobserved completion is shown unknown, and an unfamiliar item is shown as unfamiliar with its content. Verify by VER-002. [REQ-002]
- **AC-003** — A delegated child is shown with its identity, parent, role and nickname as Codex reports them, marked as text the App did not write, the source of each, and its state, including a child still active after its parent's turn completed; no return, review or integration is shown that was not observed; a child of a TASK-guided agent carries the "stated, not enforced" label; the three availability readings each produce their stated view; and a message, plan or output that reproduces a card's words or imitates a control is shown inside text marked as the agent's, with no control, heading or App sentence made from it. Verify by VER-003. [REQ-003]
- **AC-004** — The version line agrees with the version identity record supplied; a mismatch, an unverifiable distribution and an unverified development run are each shown as such; and with the experimental opt-in not declared the plan control is absent and every other view still works. Verify by VER-004. [REQ-004]
- **AC-005** — A tool success with no act evidence, a session entry and a completed goal each produce no shown act; an act record handed in is shown with the person as actor, the recorder distinct and its content, scope and purpose; and a record naming the recorder as actor is not shown as an act. Verify by VER-005. [REQ-005]
- **AC-006** — Each offered value validates against the form its receiver uses, each offered identity recomputes from the Codex identities it names, the map names every interaction of REQ-001 through REQ-005 with its supplier, receiver and reuse decision, and none of the acts in REQ-007 is produced by this deliverable's code. Verify by VER-006. [REQ-006, REQ-007]
- **AC-007** — The fixtures cover AC-001 through AC-005 in WebKit and Chromium with the packaged App's smoke witness, name the candidate, configuration and date, and report one of the five outcomes for each case. Verify by VER-007. [REQ-008]

## Production and Verification Method — Praxeology

The host derives view state from native frames in the order received, and the views rebuild from Codex history after a generation closes. Reads the views need go through the boundary's request path and are attributed to the person's press or to a named App rule. Fixtures use invented material and exchanges recorded from the stock supplier; a recorded exchange shows presentation, not that the supplier behaves so on a live candidate.

- **VER-001** — Comparison with the recorded supplier frames and Codex's history: replay plan items and revisions through the views, exercise ask, revise and carry out, relaunch, and compare what is shown with the source items and their order.
- **VER-002** — Comparison with the recorded supplier frames: replay each tool outcome case, an item with no result, an item whose turn ended without completion, a generation closed before completion and an unfamiliar item kind.
- **VER-003** — Comparison with the supplier's native delegation events and thread reads: replay a delegation in which the primary turn completes while a child is active, a delegation from a TASK-guided thread, and the three availability readings.
- **VER-004** — Comparison with the version identity record: present verified, mismatch, unverifiable and unverified-development records, and a ready announcement without the experimental opt-in.
- **VER-005** — Executable check (observes what the views show for supplied records): present tool success alone, a session entry, a completed goal, an act record with actor and recorder distinct, and a record naming the recorder as actor.
- **VER-006** — Executable check (validates offered values against the receivers' forms and recomputes offered identities), plus judgment by an independent reviewer reading the map against the accepted decomposition's `DEL-01-03` row and tracing each act of REQ-007 to its owner's code.
- **VER-007** — Judgment by an independent reviewer: read fixture provenance and the candidate's results across both engines and the packaged witness.

## Governing Values and Decisions — Axiology

- **AX-001** — Codex's own items, unchanged. Better means more of what Codex produces visible in its native form with less view code that depends on one pin, and never by translating an item into another vocabulary, hiding an unfamiliar one or adding a second harness.
- **AX-002** — The person directs from what was observed. Better means fewer rows left unknown or not completed where Codex did report an outcome, and never by showing an outcome, a return or an act that was not observed.
- **TBD-002** — Where shared contracts and interface components live is undecided (App and shared-contract owners). The required behaviour does not depend on it.
- **TBD-004** — Whether fleet management goes beyond the accepted option is undecided (owner). Delegation visibility and the identities offered to the fleet records are included regardless; no further fleet feature is.

## Output and Evaluation Matrix

| Output | Objective refs | Requirement/claim refs | Acceptance refs | Verification refs | Evidence expectation |
|---|---|---|---|---|---|
| OUT-001 | OBJ-001, OBJ-002 | REQ-001, CLM-001 | AC-001 | VER-001 | Outside source: plan items as the stock supplier sent them, recorded at the pipe, and Codex's own history after relaunch. |
| OUT-001 | OBJ-001 | REQ-002, CLM-001 | AC-002 | VER-002 | Outside source: tool items and statuses as the stock supplier sent them. PRD V4-EXE-03 states that an unobserved outcome is unknown. |
| OUT-001 | OBJ-001 | REQ-003, CLM-003 | AC-003 | VER-003 | The supplier's native delegation events and thread reads, compared with the identity, parent, role, nickname and state each view shows; and, for each availability reading, the model and configuration reads the reading was made from, compared with the view shown under the rule of the Delegation availability term. |
| OUT-001 | OBJ-001, OBJ-002 | REQ-004, CLM-002 | AC-004 | VER-004 | Outside source: the supplier binary's own version report as carried in the version identity record, and the stable and experimental variants of the pin's generated output. |
| OUT-001 | OBJ-001 | REQ-005, CLM-004 | AC-005 | VER-005 | What the views show for each supplied record, compared with PRD V4-AUT-03 and V4-REC-03 on what may not be shown as an act. The positive case is an act record written outside this deliverable; synthetic fixture acts show presentation only and are not real acts. |
| OUT-003 | OBJ-001, OBJ-002 | REQ-006, REQ-007, CLM-002, CLM-003 | AC-006 | VER-006 | Outside source: `DEL-01-04`'s and `DEL-06-01`'s need statements and the Codex identities in the recorded frames, from which offered identities are recomputed. Validation against the plan-revision reference schema, which the product itself defines, shows consistency with that form only; whether it serves the receiver is read from the receiver's need. An independent reviewer compares the map with the accepted decomposition's `DEL-01-03` row and traces each act to its owner against the decomposition's allocation. |
| OUT-002 | OBJ-001, OBJ-002 | REQ-008 | AC-007 | VER-007 | An independent reviewer's reading of fixture provenance and the candidate's results in WebKit, Chromium and the packaged App, compared with the outcome labels of EXAMINATION §1 and the engines, packaged witness and result identification of EXAMINATION §2. Browser results do not stand in for the packaged witness. |
