---
schema: chirality-deliverable-sow/v1
deliverable_id: DEL-09-05
package_id: PKG-09
decomposition_basis: execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z
project_scope_refs: [SOW-198, SOW-243]
package_objective_refs: [OBJ-006, OBJ-008]
---

# Fleet coordination and longer-work recovery witness

## Purpose and Objective Traceability

This deliverable shows, on one identified App candidate, that a person can coordinate delegated agent work and recover the whole undertaking after it is interrupted. It contributes a small fleet fixture and the joined record of what happened when that fixture ran: who actually worked, what returned, what was reviewed and integrated, what still waits and why, and one decision actually made at the act control. The App fleet integration owner integrates it and an independent examiner checks it. It builds no fleet feature.

SOW-198 is the two-delegation graph, queue, decision and view-rebuild witness of V4-EXM-13; it serves OBJ-006 (recoverable bounded fleet work) and OBJ-008 (candidate-specific evidence). SOW-243 is the separate longer-work evidence and its limits; it serves OBJ-008. Its sources are PRD V4-PM-01…06, V4-EXE-01…04 and V4-AUT-03…05, and EXAMINATION §§1–2 and V4-EXM-13.

## Deliverable Definition — Ontology

- **OUT-001** — The V4-EXM-13 fixture: an invented undertaking with two bounded delegations, a work graph, a return queue, one decision package, a change of basis and an interruption, run on an identified candidate. Supports SOW-198 and SOW-243; OBJ-006 and OBJ-008. The fixture's invented work, delegations and decided matter are fixed before VER-001 is run.
- **OUT-002** — The joined account of that run: returns, reviews, workers, ownership and pending choices, the views rebuilt from files, the decision record set against the decision actually made, the outcomes, the independent findings, and what this evidence adds beyond a single-host or conversation-only result. Supports SOW-198 and SOW-243; OBJ-006 and OBJ-008.

Terms:

- **Brief.** The written assignment of one delegated piece of work: purpose, basis, context, authority and tools, write scope and expected return. A brief shows what was asked; it does not show that a child ran.
- **Decision package.** A project file naming the exact act requested of the person, its subject and basis, and two or more alternatives with a consequence for each (PRD V4-PM-04), as DEL-06-02 presents it.
- **States kept apart.** Executing, returned, reviewed and integrated work; active descendants; independent findings; pending human choices; waiting, with its cause. The end of a primary turn, the arrival of a return and a reconnected conversation each establish only themselves.
- **Lapse.** A decision whose package file changed after the decision is shown as lapsed and stays listed. If the file is absent, the standing is unknown.

Boundary:

- **CLM-001** — `DEL-06-01` owns briefs, the work graph and the association of native delegations with them; `DEL-06-02` owns the return, waiting and decision views; `DEL-01-03` owns the native presentation of descendants. They keep their focused checks, and this deliverable joins their contributions on the candidate.
- **CLM-002** — `DEL-04-01` owns the operation policy and `DEL-04-03` the content-bound decision and run records. The person performs the decision; in the examination the examining agent makes it at the act control as a synthetic capture on examination material, which establishes no actual person's decision and no legal or professional standing; sign-in and key entry, and the release target's criterion 8 protection act and policy-lowering confirmation, stay the owner's, and the exception reaches examination material only (`DEL-09-02` REQ-009). Any professional judgment stays with that professional. The acts reserved to a person are separate from routine tool permission, which is the person's own Codex setting. A recorder may record a performed act faithfully without becoming its actor.
- **CLM-003** — `DEL-09-01` owns the examination support and record formats used here. `DEL-09-11` owns the later reconstruction of a host run, `DEL-09-12` the owner's validation in use, and `DEL-11-03` the decision packet. SWBPIPE is built by its own project. No host is joined to this fixture.

## Completion and Reliance Basis — Epistemology

- **REQ-001** — The fixture has the person delegate two bounded pieces of work with complete briefs, follow them on the undertaking's work graph, examine the returns from the queue, and decide one matter from a decision package.
- **REQ-002** — The fixture includes a dependent contribution alongside independent ready work, a return awaiting review, actual worker and resource ownership, a changed basis, and an interruption of review or integration. The rebuilt state keeps apart the states defined above.
- **REQ-003** — The graph and the coordination records are files, and the cross-session views rebuild from them, preserving ownership, prerequisites, results, next work, decisions and outstanding waits. A derived view is never the authority and never erases an unknown outcome. What was reviewed and integrated is preserved, and a basis change shows which pending or earlier judgment it affects.
- **REQ-004** — Decision evidence separates execution, checking, acceptance, approval and professional reliance by subject, actor and evidence. A performed human act is recorded faithfully; none is inferred from tool success, a return, a chat statement, silence or a timeout. No rule requires acceptance before another independently evidenced act.
- **REQ-005** — Each result binds candidate, configuration and date and has one of the five examination outcomes. Evidence identifies the actual worker mechanism and parentage, the basis supplied, the scopes, which limits were enforced and which were only instructed, and the returns observed. A changed candidate reopens the affected checks and a repair leaves the criterion as it was.
- **REQ-006** — This deliverable performs no act owned by another deliverable, as allocated in CLM-001, CLM-002 and CLM-003. It decides no policy, performs no person's act, and makes no claim about validation in use or replacement.

- **AC-001** — On the candidate, two delegations each have a complete brief and an actual child whose launch and return are observed natively, and the graph, the queue and one decision package are connected to them. Verify by VER-001. [REQ-001; CLM-001]
- **AC-002** — Through the change of basis and the interruption, the candidate shows each condition of REQ-002, including a worker still active and a return still awaiting review, without merging any two of the defined states. Verify by VER-002. [REQ-002]
- **AC-003** — After the App is closed and reopened, the views rebuilt from the files show the same ownership, prerequisites, results, next work, waiting causes, independent findings, reviewed and integrated history and pending decisions as before, and an observation that is missing is shown as unknown. Verify by VER-003. [REQ-002; REQ-003]
- **AC-004** — The decision record agrees with the decision made at the act control in the examination: the actor values the candidate observed at the control by its own rule (the examination name set before the capture and the accounts it runs under, with the identity marked not verified), a recording surface distinct from the actor, the package by content identity, and the alternative chosen. No decision is recorded or shown from a chat statement, tool success, a return, silence or a timeout; another act in the undertaking keeps its own standing and is neither required before the decision nor implied by it; and editing the package afterwards shows the decision as lapsed and still listed. A record that marks the identity verified or carries another actor value, and the decision record, or anything carrying it, found outside the identified examination material or presented as an actual person's decision, are findings (`DEL-09-02` REQ-009). Verify by VER-004. [REQ-004; CLM-002]
- **AC-005** — The account binds every result to candidate, configuration and date, names the actual workers, their returns and the basis supplied, distinguishes enforced from instructed limits, and lists the checks reopened by any change of candidate or basis with their criteria unchanged. Verify by VER-005. [REQ-005]
- **AC-006** — The account states what this joined evidence adds beyond a first-host slice, conversation recovery, file-native practice and component checks, and presents none of those as longer-work coverage, validation in use or grounds for replacement. Verify by VER-006. [REQ-005; REQ-006; CLM-003]
- **AC-007** — Both outputs keep each contribution with its owner and each undecided choice with its owner; they add no fleet feature and no policy. Verify by VER-007. [REQ-006]

## Production and Verification Method — Praxeology

The fixture is kept small: it realises the conditions of V4-EXM-13 and sets no staffing, duration, throughput or performance target. Material is invented. The integration owner identifies the candidate and the native, fleet and decision contributions available and gives a missing input an explicit standing. Recorded exchanges may show seams, but a claim about an executing child or about recovery needs actual execution on the candidate. The examining agent operates the candidate, including the act control, by agent-operated journey examination (`DEL-09-02`) and records what was observed on a native-step form, with who operated each step and by what means; records use the DEL-09-01 formats. A synthetic confirmation supplies control-and-record examination evidence only; it does not meet a positive case that requires evidence of an act an actual person performed, and that case reads as not examined until its stated evidence is supplied. Every acceptance criterion whose positive case is an act a person performed, recorded or handed over with the person as actor, is examined synthetically for its control and its record only; its human-positive case reads as not examined until an act an actual person performed is observed on the identified candidate. When this was written those were: the positive cases of `DEL-06-02` AC-004, `DEL-04-01` AC-002 and `DEL-04-03` AC-003; `DEL-09-01`'s faithful recording of an actually performed act (AC-004); `DEL-01-02` AC-007 (an answer the person actually gave); `DEL-02-02` AC-006 (a registration the person performed); `DEL-02-03` AC-003 (a checkpoint act the person performed); `DEL-01-03` AC-005 (an act record handed in, shown with the person as actor); `DEL-04-02` AC-005 (a recorded act a person performed); and `DEL-04-03` AC-010 (a permitted disposal recorded as the person's act). A criterion of the same kind not named here falls under the rule all the same. Agent 0 may recommend the candidate for the owner's evaluation with these human-positive cases explicitly not examined. Each passes only when its required act and comparison are observed on the identified candidate. A case the owner's chosen use does not exercise remains unmet; the owner's verdict supplies no missing evidence.

- **VER-001** — Observe the two delegations through native child identities and events, the graph, the queue and the decision package. Compare each brief with the required fields, and link actual launches and returns instead of inferring them from the briefs.
- **VER-002** — Run the dependent and ready work, the outstanding review, the change of basis and the interruption. Observe the state before, at interruption and after resumption.
- **VER-003** — Close and reopen the candidate, rebuild the views from the files, and compare them with the state recorded before closing and with the live workers.
- **VER-004** — Before the decision is made, have the agent report a decision the person has not made, wait in silence, and let tool successes, returns and timeouts occur; inspect the records and the decision view after each. Then set the App's name to an examination name, verify that it is set, make the decision at the act control, and compare the record and its capture evidence with the decision made (package and alternative chosen) and its actor values with what the candidate observed by its own rule; a record that marks the identity verified or carries another actor value is a finding, as is the decision record, or anything carrying it, found outside the identified examination material. A record without an act made at the control, or an act made at the control without a record, fails; an act whose making was not observed is inconclusive. Edit the package file and inspect the lapse.
- **VER-005** — An independent reviewer examines result identity and standing, worker and return provenance, the description of enforcement, the history of the changed basis and the reopened checks.
- **VER-006** — Compare the coverage of the joined evidence with the first-host, conversation-only and component evidence and state what remains uncovered.
- **VER-007** — Review both outputs against CLM-001, CLM-002 and CLM-003 and the undecided matters below.

## Governing Values and Decisions — Axiology

- **AX-001** — Files carry coordination authority and views are recoverable projections of them. The project's dependency graph, the route chosen through an undertaking and what is actually executing are three different things. Better means more of the undertaking's state recoverable from files alone after an interruption; never by letting a view assert something the files do not hold.
- **AX-002** — Each record stands for what was observed on the candidate. Better means fewer states left unknown after recovery; never by filling an unobserved outcome or inferring a person's decision.
- **AX-003** — Two bounded delegations are the scenario's quantity and not a staffing target. No fleet scope, shared construction or scale claim is inferred from this fixture.
- **TBD-001** — Whether any project-management outcome is added beyond the accepted option is undecided (owner). Nothing here depends on it.
- **TBD-004** — Whether any host beyond the App and SWBPIPE is essential to examination is undecided (owner). No further host is presumed.

## Output and Evaluation Matrix

| Output | Objective refs | Requirement/claim refs | Acceptance refs | Verification refs | Evidence expectation |
|---|---|---|---|---|---|
| OUT-001 | OBJ-006; OBJ-008 | REQ-001; CLM-001 | AC-001 | VER-001 | Child launches and returns read from the supplier's native events, which the App did not write, compared with the briefs, graph, queue and decision package; each brief compared with the fields of PRD V4-PM-01…04 and the fixture with the conditions of EXAMINATION V4-EXM-13. |
| OUT-001 | OBJ-006; OBJ-008 | REQ-002 | AC-002 | VER-002 | Judgment by the examiner: the states observed before, at and after the interruption compared with the conditions EXAMINATION V4-EXM-13 and REQ-002 list. |
| OUT-002 | OBJ-006; OBJ-008 | REQ-002; REQ-003 | AC-003 | VER-003 | The state the examiner recorded before closing, and the files on disk. No independent grounds: the comparison is of the product with its own earlier state and its own files, so it guards against loss and does not show the earlier state was right. AC-001 and AC-002 carry that. |
| OUT-002 | OBJ-006; OBJ-008 | REQ-004; CLM-002 | AC-004 | VER-004 | Outside source: the decision the examining agent made at the act control, observed and recorded apart from the candidate; in an examination run under the owner's account the account identifiers recorded are the owner's although an agent operated the control. It supplies control-and-record examination evidence only. PRD V4-AUT-03, V4-EXE-02 and V4-PM-04 state what may and may not be recorded. |
| OUT-002 | OBJ-008 | REQ-005 | AC-005 | VER-005 | Judgment by an independent reviewer: the account read against the native events, the candidate identification and the outcome meanings of EXAMINATION §§1–2. |
| OUT-002 | OBJ-008 | REQ-005; REQ-006; CLM-003 | AC-006 | VER-006 | Judgment by a reviewer: the account's statement of coverage compared with the first-host, conversation-only and component evidence it cites, and with the longer-work conditions SOW-243 adds; EXAMINATION §7 names the replacement evidence, which this is not. |
| OUT-002 | OBJ-006; OBJ-008 | REQ-006; CLM-001; CLM-002; CLM-003 | AC-007 | VER-007 | Judgment by a reviewer: both outputs read against the decomposition's allocation of each act to its deliverable and the owners of the undecided matters below. |
