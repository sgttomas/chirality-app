---
schema: chirality-deliverable-sow/v1
deliverable_id: DEL-09-07
package_id: PKG-09
decomposition_basis: execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z
project_scope_refs: [SOW-199, SOW-200, SOW-201, SOW-202, SOW-239]
package_objective_refs: [OBJ-004, OBJ-005, OBJ-008]
---

# DEL-09-07 — Local host candidate qualification

## Purpose and Objective Traceability

This deliverable qualifies one identified pair of App and SWBPIPE candidates by observing the local host activity on them: an engineer asks SWBPIPE's embedded agent, running on a local model, to change an invented piping model, reviews and accepts the proposal row by row, and a solve follows. It contributes the four coordinated cases V4-EXM-20, V4-EXM-21, V4-EXM-22 and V4-EXM-23 with their candidate-bound results, and one dossier that joins them with SWBPIPE's own receipts and traffic observation. The App connected-activity examination owner coordinates it, SWBPIPE's owner supplies execution, traffic and receipts, and an independent examiner checks the dossier. It builds nothing in either application.

It serves OBJ-004 (host meaning and authority), OBJ-005 (attributable autonomy) and OBJ-008 (candidate-specific evidence). Its sources are PRD V4-HOST-01/02, V4-PAR-01…04, V4-AUT-01…05, V4-WF-05, V4-REC-01…05, HOST_INTEGRATION V4-HI-10…12, 20…25, 30…33, 40…42 and 70…71, and EXAMINATION §§1–2 and §4. This deliverable is outside App v4's release: the live SWBPIPE journey it examines is SWBPIPE's requirement, and work on it is undertaken in support of SWBPIPE. AC-002 and AC-003 state that result.

| Assigned scope | Local contribution | Output |
|---|---|---|
| SOW-199 | Invented piping model, catalog reads, a supports and run-adjustment proposal, row acceptance and rejection, application and solve; views, origins, receipts and stale refusal | OUT-001; OUT-002 |
| SOW-200 | An engineer-edited model checked without changing the tables; findings refer to rows and results | OUT-001; OUT-002 |
| SOW-201 | One low-consequence class applied directly, geometry proposed, origins and undo, and a human checkpoint | OUT-001; OUT-002 |
| SOW-202 | All host traffic during the journey observed against the selected model service and the destinations the person allowed | OUT-001; OUT-002 |
| SOW-239 | Intervening edits and recovery of actual host outcomes and receipts | OUT-001; OUT-002 |

## Deliverable Definition — Ontology

- **OUT-001** — The four coordinated cases V4-EXM-20…23 and one result record for each planned part on the identified candidates. Supports SOW-199, SOW-200, SOW-201, SOW-202 and SOW-239; OBJ-004, OBJ-005 and OBJ-008.
- **OUT-002** — One local qualification dossier: the identification of both candidates, a manifest linking the cases to the original model basis, the proposed, accepted, rejected and applied rows, the solve and checking evidence, the policy and checkpoints in force, the traffic observation, origins and undo, the host's receipts and the human acts. It states the gaps and the candidates' standing. Supports SOW-199, SOW-200, SOW-201, SOW-202 and SOW-239; OBJ-004, OBJ-005 and OBJ-008.

Terms:

- **Read basis.** Workspace identity, generation, model revision and canonical content hash of what the agent read. A proposal is bound to its read basis, and a later selection never retargets it.
- **Outcome meanings.** `success` means an operation ran. A submitted proposal stays queued until the host records its acceptance and application. An outcome that was not observed is unknown.
- **Separate acts.** Applying, accepting an edit, checking, engineering approval and professional reliance are separate acts; evidence of one establishes none of the others, and none is required before another independently evidenced act.
- **Traffic observation.** A record of every network destination the host contacted during one run, with the selected model service, the destinations the person allowed and the boundary of what could be observed.

Boundary:

- **CLM-001** — The App connected-activity examination owner is responsible for this qualification. Feature owners keep their own checks. Examination happens as contributions become available on the candidates.
- **CLM-002** — SWBPIPE's own project builds the host: its model store, catalog and views, its validation, application and solve route, its loop and panel, its enforcement of network destinations, origins, undo and receipts. The host offers, records and presents human acts; the person performs them and sets the autonomy for each operation class. For the first increment's App and shared contracts, five acts are reserved to a person: marking checked, accepting a proposal where autonomy requires it, engineering approval, professional reliance, and changing the grant or enabling external access; hosts have no classifier permission mode, and SWBPIPE model changes default to proposals. The host adopts, names and enforces its own list, and SWBPIPE's adoption is part of its contribution.
- **CLM-003** — `DEL-09-06` owns the definition of the activity examined here (its operation, autonomy and environment), the reusable method and the workflow round trip, and the receiving of SWBPIPE's catalog; this deliverable uses them. External control, catalog extension and the later Domains activity are examined elsewhere. Reconstruction a week later is `DEL-09-11`'s.
- **CLM-004** — SWBPIPE's contribution is needed before the connected examination. A prepared file, an inspected source or a component pass is neither a delivery nor a joined witness. Coordination with SWBPIPE is relayed by the human through repository files.
- **CLM-005** — What is qualified is the observed meaning, outcome and standing of operations on the candidates, in the terms defined above.

## Completion and Reliance Basis — Epistemology

- **REQ-001** — The cases and the dossier identify both candidates, the date, configuration, harness and model versions, the local model server, the operation policy in force, the contribution actually received from SWBPIPE and its standing, the activity definition used, and, for each run, its date and everyone who took part in it (the person who acted, the host agent's session, the recorders, the assembler and the examiner). Each observation is bound to that basis.
- **REQ-002** — V4-EXM-20 uses an invented piping model and the embedded agent on the local model server, asked to add supports and adjust a run: the agent reads tables through the catalog and drafts a proposal; the engineer reviews the proposed rows with old and new values in the host's own tables, accepts some row by row, rejects one, and applies; a solve follows. Affected objects, reasons, origin marks and receipts are kept.
- **REQ-003** — The trace keeps the original read basis through proposal review, an intervening edit, the stale refusal with its reason, any redraft on a named new basis, application and solve, and the recovery of actual outcomes and receipts. Recovery of a conversation or a transport does not assert a host success or a human acceptance.
- **REQ-004** — V4-EXM-21 begins with a model the engineer edited and a request to check it. Findings attach to rows and results by reference and change no table. Each finding keeps the read basis it relied on and shows, in the host's own views, the standing of what it cites: current or historical, checks passed and known limits. A finding is never presented as a human Checked act, approval, certification, seal, code-compliance determination or professional reliance. A human act that was actually performed is recorded faithfully, its actor, content, scope and purpose kept apart from the recorder.
- **REQ-005** — Under an explicitly adopted operation policy, V4-EXM-22 allows direct application for one class of low-consequence operation and keeps proposals for model geometry. Direct application shows origin and undo; the setting for each class is visible and recorded with the run; and a declared workflow checkpoint requests the person's act and records it only when the person performs it, whatever the autonomy. Stopping the run at the checkpoint is examined only for a workflow that takes up the governance phase. The person can widen the setting from the proposal default, and running the case decides no reserved-act or routine-permission policy.
- **REQ-006** — V4-EXM-23 observes all host network traffic during V4-EXM-20 and establishes four things: requests go only to the model service the person selected and to destinations the person allowed, in advance or when the agent asked during its work; a declined request reaches no destination and is reported to the agent as "destination not allowed by the person"; nothing else is contacted unless the person turned it on; and every destination contacted is recorded and shown. The evidence addresses the host's actual native enforcement, and no schema, mock, browser-only witness or selected request log stands in for it. An outside process that is not sandboxed is examined within that stated limit.
- **REQ-007** — The dossier joins, by reference, the operations requested, the caller's and observer's authority, the original and current basis, the host's actual outcomes, the human decision actors, the recorder, origins and host receipts, with workflow and version, conversation, autonomy settings and model identity. The host's truth stays in its own store. A content-bound act visibly lapses when its content changes.
- **REQ-008** — Each planned part ends as passed, failed, blocked, not run or inconclusive, with its limits and with the checks a changed candidate reopens. Recorded exchanges are used where they can show a criterion; interface examination runs in WebKit and Chromium, and each targeted packaged application has a native smoke check that browser evidence never replaces. V4-EXM-20 must pass on the identified App and SWBPIPE candidates with a local model, as one completed live journey; an honest account of a partial or absent run does not meet it. No favourable engineering approval or reliance is required.
- **REQ-009** — This deliverable performs no act owned by another, as allocated in CLM-001, CLM-002 and CLM-003: it defines no activity, builds no host or feature behaviour, decides no policy, performs no person's act and assembles no decision packet.

- **AC-001** — The case definitions and the dossier identify both candidates, configuration and date, the SWBPIPE evidence received and the activity definition used, name the date and the participants of each run, and cover all five assigned scope items and the four scenarios. Verify by VER-001. [REQ-001]
- **AC-002** — On the identified candidates, with a local model and invented piping material, the V4-EXM-20 journey completes live: the request, catalog reads, a proposal shown in the host's tables with old and new values, some rows accepted one by one, one rejected, application, the following solve, origin marks and receipts. Verify by VER-002. [REQ-002; REQ-008]
- **AC-003** — The evidence traces the original read basis through an intervening edit to a stale refusal that states its reason, and on to actual application, outcome and receipt recovery. A redraft names its new basis, no selection retargets the old proposal, and an unavailable outcome is shown as unknown. Verify by VER-003. [REQ-003]
- **AC-004** — After the engineer's edit, the agent's findings attach by reference to rows and results, the tables are unchanged, each finding carries its read basis and the standing of the rows and results it cites, and no Checked act, acceptance, approval or reliance appears from a finding or a tool success. A human act actually performed in the scenario is recorded with its actor distinct from the recorder and its content, scope and purpose intact. Verify by VER-004. [REQ-004; REQ-007]
- **AC-005** — Under the recorded policy, one low-consequence class is applied directly with origin and undo, geometry is offered as proposals, the settings are visible and recorded with the run, and a workflow checkpoint's act is requested and recorded only when the person performs it. No case result stands as a decision on reserved-act or routine-permission policy. Verify by VER-005. [REQ-005]
- **AC-006** — Throughout the V4-EXM-20 run every destination the host contacted is the selected model service or one the person allowed, every one is recorded and shown, a declined request reached no destination and was reported to the agent in the stated words, and the evidence shows the host's native boundary enforcing it. An observation that is limited or missing leaves the criterion unmet. Verify by VER-006. [REQ-006]
- **AC-007** — One independently examined dossier links the cases and the host's receipts without replacing the host's own store, keeps operations, outcomes and human acts apart, keeps unknowns and limits, records the WebKit, Chromium and native package evidence, and names the checks a changed candidate reopens. It claims no standalone pass, replacement, release or professional reliance. Verify by VER-007. [REQ-007; REQ-008]
- **AC-008** — The dossier assigns every excluded act of REQ-009 to its owner and keeps each SWBPIPE contribution at the one standing DEL-09-06 defines. Verify by VER-008. [REQ-009; CLM-004]

## Production and Verification Method — Praxeology

The activity definition from DEL-09-06 and the contribution received from SWBPIPE fix the candidates and the operation policy before anything dependent is run. The cases are prepared here; SWBPIPE's execution, traffic and receipt observations arrive through the human; the dossier is assembled with linked evidence and an independent examiner checks the join. Records use the DEL-09-01 formats, with one identification record for the candidate pair. Tests implement the criteria above and add none.

- **VER-001** — Inspect the case plan and the dossier against the five scope items, V4-EXM-20…23 and the activity definition and configuration actually received.
- **VER-002** — With SWBPIPE's owner, observe the live embedded journey on the candidates: catalog reads, table views, each accepted row and the rejected row, the applied state, the solve result, origins and receipts. Confirm the request reached the person's acceptance.
- **VER-003** — Examine the original read basis and an intervening edit; observe the stale refusal and its reason; follow any proposal on a new basis to its outcome and receipt, including an interruption. Check that no reconnection or transport success supplied a missing host outcome.
- **VER-004** — Compare host table content before and after the check, follow the findings' references, and inspect the record of a performed human act (such as a row acceptance) against the act observed, with the fabrication negatives and the lapse after a content change.
- **VER-005** — Inspect the policy and run setting in force; observe the directly applied class with origin and undo, the geometry proposals and the checkpoint.
- **VER-006** — Receive the complete host network observation for the same run and compare every destination with the selected model service, the allowed destinations and grants in force, and the host's own destination record. State the boundary of the observation. A partial capture or a substitute fixture does not pass.
- **VER-007** — An independent examiner reconstructs the activity from the dossier and the linked host evidence and inspects configuration, outcomes, limits, browser and native coverage.
- **VER-008** — Review the account of acts against CLM-001…CLM-004 and the standing of each SWBPIPE contribution against DEL-09-06's definition and the evidence held.

## Governing Values and Decisions — Axiology

- **AX-001** — The host's actual permissions and capabilities bound what is examined. Semantic parity settles nothing about automatic catalog extension, and a shared contract assigns no common construction. No wire field, threshold or process gate is created here.
- **AX-002** — An observer, a requested operation, the host's actual outcome and a human act each keep their own identity and evidence. Better means more of the journey's facts supported by the host's own receipts and an outside traffic observation; never by taking the App's or the agent's report of an outcome in their place.
- **AX-003** — Criteria are kept through repair and evidence stays with the candidates it was observed on. Better means fewer unknown outcomes after an interruption; never by filling one from a conversation or transport recovery.
- **TBD-001** — The operation, the autonomy permitted and the candidate environment of the activity are undecided (owner, through the SWBPIPE session, with the App owner) and reach this deliverable through DEL-09-06. The supports and run adjustment of REQ-002 is the scenario as written; if a different operation is chosen, AC-002 is restated by the owner before it is examined. Additions to the reserved acts or to routine-permission treatment for that operation are decided with it, and a criterion that depends on one waits for it.

## Output and Evaluation Matrix

| Output | Objective refs | Requirement/claim refs | Acceptance refs | Verification refs | Evidence expectation |
|---|---|---|---|---|---|
| OUT-001 | OBJ-004; OBJ-005; OBJ-008 | REQ-001; CLM-001; CLM-004 | AC-001 | VER-001 | The case plan and dossier compared with the accepted decomposition's five scope items, EXAMINATION V4-EXM-20…23 and the activity definition and configuration actually received; the identifications checked against the candidate pair's identification record. |
| OUT-001 | OBJ-004; OBJ-008 | REQ-002; REQ-008 | AC-002 | VER-002 | Outside source: SWBPIPE's own tables, solve result and receipts, and what the examiner watched the engineer do. EXAMINATION V4-EXM-20 states the journey. |
| OUT-001 | OBJ-004; OBJ-008 | REQ-003 | AC-003 | VER-003 | Outside source: the host's own receipts and refusal reason. HOST_INTEGRATION V4-HI-21/23/70/71 state the expected behaviour. |
| OUT-001 | OBJ-004; OBJ-008 | REQ-004; REQ-007; CLM-005 | AC-004 | VER-004 | Outside source: host table content before and after, and the act the examiner watched. EXAMINATION V4-EXM-21 and HOST_INTEGRATION V4-HI-10…12 state the expected result. |
| OUT-001 | OBJ-005; OBJ-008 | REQ-005; CLM-002 | AC-005 | VER-005 | What the examiner observed in the host compared with the operation policy the host adopted, the person's recorded setting for each class, DEL-04-01's policy-class records and PRD V4-WF-05. |
| OUT-001 | OBJ-004; OBJ-008 | REQ-006 | AC-006 | VER-006 | Outside source: an observation of all the host's network traffic for the run, supplied by SWBPIPE's owner, set against the host's own destination record. PRD V4-HOST-02 states the four things to establish. |
| OUT-002 | OBJ-004; OBJ-005; OBJ-008 | REQ-007; REQ-008; CLM-003 | AC-007 | VER-007 | An independent examiner's reconstruction of the activity from the dossier, compared with the host's own receipts and with EXAMINATION §§1–2. A check that a record matches DEL-09-01's formats shows only that it is well formed. |
| OUT-002 | OBJ-004; OBJ-008 | REQ-009; CLM-001; CLM-002; CLM-003; CLM-004 | AC-008 | VER-008 | Each act the dossier excludes compared with its owner in CLM-001 to CLM-004 and in the accepted decomposition's rows; each SWBPIPE contribution's standing compared with the evidence held for it. |
