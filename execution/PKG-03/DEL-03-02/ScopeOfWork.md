---
schema: chirality-deliverable-sow/v1
deliverable_id: DEL-03-02
package_id: PKG-03
decomposition_basis: execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z
project_scope_refs: [SOW-070, SOW-090, SOW-091, SOW-170, SOW-171, SOW-172, SOW-173, SOW-174, SOW-175, SOW-176, SOW-177, SOW-178]
package_objective_refs: [OBJ-004, OBJ-005]
---

# Proposal, validation and outcome contract

## Purpose and Objective Traceability

This deliverable contributes one definition of how a change reaches a host and what may truthfully be said about it afterwards. A change by the person, by the host's embedded agent or by an external agent passes through the host's one validation and application route. Outside an autonomy the person has granted, it is a proposal whose every item the person decides. What is reported about it is never more than the host recorded: queued is not accepted, accepted is not applied, a success is not a person's act, and an outcome nobody observed stays unknown. The App/shared operation-contract owner produces the schemas, the lifecycle and route definition and the fixtures; each host owns its validation, application, receipts and views.

It serves OBJ-004 (shared operation meaning, host authority and recovery) and OBJ-005 (useful autonomy with attributable human acts and result standing). Its sources are PRD V4-PAR-04, V4-AUT-01, V4-AUT-03, V4-REC-01, V4-CST-05 and V4-CST-06, and HOST_INTEGRATION §1, V4-HI-11, V4-HI-20…25, V4-HI-30…33 and V4-HI-70…71. The draft 4.0.0 release target names no exit criterion for this deliverable; the live SWBPIPE journey of its criterion 5 ("controlled application, truthful outcomes") is judged in this contract's terms.

| Assigned scope | Local contribution | Output |
|---|---|---|
| SOW-070 | One host validation and application route for person and agents, with equivalent outcomes and errors | OUT-001; OUT-002; OUT-003 |
| SOW-090, SOW-091 | Domain truth and validation stay with the host; agent output is never the host's accepted result without the host's recorded act | OUT-002; OUT-003 |
| SOW-170 | An agent's change carries its origin, conversation, workflow run and relied-on basis | OUT-001 |
| SOW-171, SOW-172, SOW-178 | The proposal lifecycle, the unknown outcome, and queued until the host records acceptance and application | OUT-001; OUT-003 |
| SOW-173, SOW-174, SOW-175 | Stale refusal with re-draft, no retargeting, and one effect for a repeated submission | OUT-003 |
| SOW-176 | Old and new values, affected objects and reasons for the host's own views | OUT-001 |
| SOW-177 | Success means execution and implies no human acceptance | OUT-003 |

## Deliverable Definition — Ontology

- **OUT-001** — The schemas of a change request and of the state a host reports for it: target binding, relied-on basis, origin, per-item lifecycle and outcome, the change-item content identity the host assigns at first receipt, the host's receipt references, the old and new values a host's proposal view needs and, for a workflow that takes up the governance phase, the governing checkpoint constraint with its carriage assurance. Each has valid and invalid example documents and the rules a schema cannot express. Supports all twelve assigned scope items; OBJ-004 and OBJ-005.
- **OUT-002** — The lifecycle and route definition: the one validation and application route and the parity of actors on it, the distinction between a proposal and a direct application, which outcome claims are permitted, what the host owns, and the open choices at their points of need. Supports all twelve assigned scope items; OBJ-004 and OBJ-005.
- **OUT-003** — Contract fixtures and their expected observations for actor parity, origin and basis, the lifecycle, stale refusal, a later selection, repeated submission, unknown outcomes, host-view information and the reporting of execution against acceptance. They use invented material. Supports all twelve assigned scope items; OBJ-004 and OBJ-005.

Terms:

- **Change request.** One submission asking the host to change its objects, with a requested mode: *propose*, or *apply directly* under a grant.
- **Proposal identity.** Minted once before the first submission, by the proposer or by the host, and named as such. A retry after a lost acknowledgment keeps the identity and the content. A re-draft has a new identity and names the proposal it replaces and why. A submission that reuses an identity with different content is an *identity conflict*: it has no effect and changes nothing recorded.
- **Change item.** One change within a proposal, with its own identity. It is the unit of acceptance: the person accepts or rejects item by item, and one act may list several items.
- **Change-item content identity.** The host's identity of an item's content (operation and version, bound targets, old and new values, relied-on basis), assigned at first receipt. An acceptance or rejection binds to it and never carries to changed content.
- **Relied-on basis and targets.** The basis of each read the request relied on, as `DEL-03-01` defines it, and the subject content identities of each item's targets. They are fixed at drafting.
- **Origin.** Author type (person or agent), the channel (host interface, embedded agent or external agent), the conversation and workflow run, and the autonomy standing at drafting: the grant's display state, its value (direct or propose) and its settings reference.
- **Item states.** Drafted, validated, queued, accepted, applied, applied then reversed, rejected, withdrawn, left the queue, refused as stale, refused as invalid, refused as not permitted, and application error. *Outcome unknown* is an observer's statement laid over the last observed state; it changes no state.
- **Accept, reject, withdraw, refuse.** Accepting and rejecting are the person's acts, withdrawing is the proposer's, and refusing is the host's.
- **Item-left event.** The record that an item left the queue without a person's decision, with its cause (refused, withdrawn, or cleared by the person with no decision record), time and evaluated basis.
- **Derived proposal state.** A summary of the item states, their counts, whether any item is still open and whether every item is decided. It is never stronger than its items.
- **Applied association.** What ties an application to its request: the item, the relied-on basis, the receipt reference, the resulting objects where the host supplies them, and the branch, *after acceptance* or *direct under grant*.
- **Observation by identity.** A read of the route that returns the recorded state of a proposal, or *not known to host*. It has no effect and is never a submission.
- **De-duplication scope.** The extent within which a host evidences one effect per identity: durable, host session, a time window, or not stated.

Boundary:

- **CLM-001** — The App/shared operation-contract owner owns the schemas, the lifecycle and route definition and the fixtures.
- **CLM-002** — The host owner, SWBPIPE's own project for the first host, owns domain objects and truth, the host store, the catalog, validation, the one application route, receipts, the interface, and the offering, recording and presenting of human acts. The person performs those acts; owning the facility that records an act confers no ownership of the act.
- **CLM-003** — `DEL-03-01` owns operation identity and version, arguments, errors, availability and the read basis; this contract carries that basis into changes and defines no second basis authority. `DEL-02-01` owns workflow identity and checkpoint declarations; a governing checkpoint constraint derived from them applies only to a workflow that takes up the governance phase.
- **CLM-004** — `DEL-04-01` owns the operation policy and the distinctions between human acts. `DEL-04-02` owns the display of autonomy and standing. `DEL-04-03` owns the act and run records.
- **CLM-005** — `DEL-03-03` owns the App's external receiving and uses this same contract. `DEL-03-04` owns the host integration guide. `DEL-09-09` owns the joined external witness on actual candidates.
- **CLM-006** — A change outside a granted direct autonomy is a proposal. A result nobody observed is unknown whether or not it was applied. A success means the operation ran.

## Completion and Reliance Basis — Epistemology

- **REQ-001** — Changes by the person, the embedded agent and an external agent pass through the same host validation and application route, with equivalent outcomes and errors for equivalent inputs, basis and authority. The contract defines no second route for agents. [SOW-070; V4-PAR-04; V4-HI-20]
- **REQ-002** — Domain truth and validation stay in the host's store and ownership, and an agent's output is never represented as the host's accepted result without the host's recorded act. [SOW-090, SOW-091; V4-REC-01; V4-CST-05]
- **REQ-003** — An agent's change carries its origin, its conversation and workflow run and the basis it relied on, unchanged through submission and every reported outcome. [SOW-170; V4-HI-21; V4-HI-11]
- **REQ-004** — Outside a granted direct autonomy a change moves from drafted to validated, queued, accepted and applied with a receipt, or leaves as rejected, withdrawn or stale. States apply per change item. A direct application under a grant is a separate branch and carries no acceptance. *Rejected* is only the person's rejection and *withdrawn* only the proposer's withdrawal. A host's refusal, stale or otherwise, is a refusal and never a rejection. A host outcome named rejected or withdrawn is received as the host reports it and is never read as the person's rejection or the proposer's withdrawal. [SOW-171; V4-HI-22…23]
- **REQ-005** — Where the outcome of a submission or an application cannot be observed, it is reported unknown, including when it may have been applied. Nothing is inferred from a missing observation. [SOW-172; V4-HI-23]
- **REQ-006** — A proposal whose relied-on basis no longer holds is refused as stale with its reason. It may be re-drafted on the current basis, and the re-draft is a different proposal. [SOW-173; V4-HI-23]
- **REQ-007** — A later change of selection never retargets a proposal: its affected objects are those bound at drafting. [SOW-174; V4-HI-23]
- **REQ-008** — Submitting the same proposal again has at most one application effect per change item. This is the host's obligation, which the contract makes testable: each submission is recorded on its own with only the effects observed, and shared validation is no evidence that it holds. [SOW-175; V4-HI-23]
- **REQ-009** — The contract gives the host's own proposal views the old and new values, the affected objects and the reason for each change. Presentation and receipts are the host's. [SOW-176; V4-HI-24]
- **REQ-010** — A reported success means the operation ran and never that a person accepted anything. Execution and human acts stay distinguishable. [SOW-177; V4-HI-25]
- **REQ-011** — A submitted proposal is reported queued until the host records acceptance and application. Neither an acceptance alone nor a successful submission is reported as applied, and an applied report refers to the host's receipt. [SOW-178; V4-HI-23, V4-HI-25]
- **REQ-012** — The contract takes the adopted operation classes and human-act distinctions from `DEL-04-01` and assigns no operation a class of its own. Accepting a proposal, checking, engineering approval and professional reliance stay distinct, and no act is attributed to a person who did not perform it. [V4-HI-30…33]
- **REQ-013** — This deliverable performs no act owned by another, as allocated in CLM-002…CLM-005: it defines no catalog, policy, autonomy display, record format, external adapter or guide, runs no joined examination, and builds no host store, validation, application, receipt, act recording or interface.

- **AC-001** — The schemas and the route and lifecycle definition account for all twelve assigned scope items and identify a proposal's targets, relied-on basis, origin, per-item lifecycle and outcome, each item's host-assigned content identity, and receipt and view information. A request or state document that lacks one of them is refused. No wire format or storage topology is selected. Verify by VER-001. [REQ-001…REQ-011]
- **AC-002** — Equivalent changes by the person, the embedded agent and an external agent name one host route and yield the same outcome and error meaning, including an invalid and a stale refusal. No fixture gives an agent a route of its own. Verify by VER-002. [REQ-001]
- **AC-003** — The definition leaves domain truth and validation with the host, and an agent's result with no recorded host act is never shown as the host's accepted result. Verify by VER-003. [REQ-002]
- **AC-004** — An agent-origin request keeps its conversation and workflow run and the exact basis it relied on through every state reported for it. A request that cites a basis or a target not observed in the reads it relied on is refused. Verify by VER-004. [REQ-003]
- **AC-005** — The fixtures distinguish every item state, and a direct application under a grant records no acceptance. A reported state whose accepted, rejected or withdrawn item lacks the act that makes it so, or whose derived state is stronger than its items, is refused. Verify by VER-005. [REQ-004]
- **AC-006** — An outcome that was not observed is reported unknown, whether the operation ran with its acknowledgment lost or its application was never established. A lost observation yields no success, failure or human act. Verify by VER-006. [REQ-005]
- **AC-007** — After a change that invalidates the relied-on basis, the earlier proposal is refused as stale with its reason, and the re-draft carries a new identity, its lineage and the current basis. Verify by VER-007. [REQ-006]
- **AC-008** — Changing the host's selection after drafting changes neither the proposal's bound targets nor the affected objects reported for it, and a state that applies an item against a basis the request did not cite is refused. Verify by VER-008. [REQ-007]
- **AC-009** — A repeated submission of the same proposal, including after a lost acknowledgment, shows at most one application effect per change item in the host's receipts. An observed second effect is recorded as the host's failed obligation and not hidden, and an outcome that cannot be established stays unknown. Verify by VER-009. [REQ-008; REQ-005]
- **AC-010** — The host-view cases carry each proposal's old values, new values, affected objects and reason, and name the host as the producer of the view and the receipt. Verify by VER-010. [REQ-009]
- **AC-011** — A success response establishes execution only. Each claimed human act rests on evidence of that act, and one act establishes no other. A host's application that records no attributable act is never received as a person's acceptance. Verify by VER-011. [REQ-010; REQ-002]
- **AC-012** — A submission is reported queued until the host records acceptance and application. Accepted-only, successful-submit and lost-observation cases claim no application, and an observed application names the host's receipt. Verify by VER-012. [REQ-011; REQ-005]
- **AC-013** — The policy interface distinguishes routine tool permission, a granted direct application, the acceptance of a proposal and the other human acts. It applies the adopted first-increment policy, leaves operation-specific additions open with their owner, and supplies no act and no blanket approval rule of its own. Verify by VER-013. [REQ-012]
- **AC-014** — Every act REQ-013 excludes resolves to its owner in CLM-002…CLM-005, and all twelve scope items stay covered by the schemas, the definition and the fixtures. Verify by VER-014. [REQ-013]

## Production and Verification Method — Praxeology

The schemas are JSON Schema documents with valid and invalid instances; their property names are this contract's labels and select no wire format, storage topology, transport field or placement. The meanings taken from the catalog and the policy contracts are used as their owners state them. A received request or host state is kept as supplied beside anything derived from it. Rules a schema cannot state are part of the contract: a request cites only bases and targets observed in the reads it relied on; item identities are unique; an item's operation is a change entry of the catalog discovered; a reported state names the same proposal, only its items, and the acts its states require. Where a host publishes its own operation cases, they are received in this contract's terms exactly as the host states them; SWBPIPE's operation corpus is the first such source. A fixture result holds for the double or host it ran on.

- **VER-001** — Executable check (observes each example and altered request and state document accepted or refused) and comparison with a named reference (the twelve scope items and HOST_INTEGRATION V4-HI-20…25): coverage of targets, basis, origin, lifecycle, outcome, receipt and view information.
- **VER-002** — Comparison with a named reference (the same change on the three channels, for the same operation, basis and authority, including invalid and stale inputs): route identity, errors and outcome meaning.
- **VER-003** — Executable check (observes how an agent result with no recorded host act is reported), with judgment by an independent reviewer of the definition's host-ownership statements.
- **VER-004** — Executable check (observes origin, conversation, workflow run and basis on a request and on each state reported for it, and the refusal of a request citing an unobserved basis or target).
- **VER-005** — Executable check (observes the item states along the success, rejected, withdrawn and stale branches and a direct application under a grant, and the refusal of a state whose acts or derived state do not fit its items).
- **VER-006** — Executable check (observes what is reported when the acknowledgment of an executed operation is lost and when an application is never established): unknown in both, with the last observed state.
- **VER-007** — Executable check (observes the refusal after the basis changes, its reason, and the identity, lineage and basis of the re-draft).
- **VER-008** — Executable check (observes the bound targets and reported affected objects before and after a change of selection, and the refusal of an application against an uncited basis).
- **VER-009** — Executable check (observes the application effects and receipts after the same proposal is submitted again, including after a lost acknowledgment); on a double it observes the contract's expectation, and one effect on a host is judged from that host's receipts.
- **VER-010** — Comparison with a named reference (HOST_INTEGRATION V4-HI-24): old values, new values, affected objects and reason in the proposal-view examples, and the host named as producer.
- **VER-011** — Executable check (observes what a success with no act evidence and a single separately evidenced act each establish) and comparison with a named reference (SWBPIPE's operation corpus at its commit `8212c765ec0bcc812ad4c4f7079bc661b55d70ab`): no case of a host apply is received as a person's acceptance.
- **VER-012** — Executable check (observes the report for submitted, accepted-only, accepted-and-applied and interrupted-observation cases against the host state supplied).
- **VER-013** — Judgment by an independent reviewer: reads the policy interface and its direct, proposal, routine-permission and human-act cases against CLM-004 and the adopted policy of `DEL-04-01`.
- **VER-014** — Judgment by an independent reviewer: maps each excluded act to its owner and each scope item to the output that covers it.

## Governing Values and Decisions — Axiology

- **AX-001** — The host owns truth and the one route; the contract reports what the host recorded. Better means more of what is reported about a change traceable to a host record or receipt; never by reporting queued as accepted, accepted as applied, or an unobserved outcome as anything but unknown.
- **AX-002** — Autonomy is useful within the person's grant, and each human act keeps its own evidence. Better means fewer unnecessary proposals for what the person has granted; never by letting a grant, a success or a routine permission stand for acceptance, checking, approval or professional reliance.
- **TBD-001** — Which concrete operations carry a class beyond the adopted first-increment policy is undecided (owner, through the SWBPIPE session, with the App owner). No unruled operation's permission or act class is selected here, and whether a host adopts and enforces the policy is that host's to evidence.
- **TBD-002** — The representation of proposal identity and change-item content identity, the schema encoding, how one effect is enforced and how an outcome is recovered are unagreed (the contract and host owners), as is the placement of shared contracts (App/shared contract owners). What a record states for a repeated submission when a host states no de-duplication scope is likewise unsettled. REQ-003…REQ-011 hold whatever is chosen.
- **TBD-003** — The operation, the autonomy permitted and the candidate environment of the first connected activity are undecided (owner, through the SWBPIPE session, with the App owner), and the host's route, views, receipts and act records are SWBPIPE's to supply. Receiving on that host waits for them.
- **TBD-004** — Whether a new catalog operation reaches every actor without separate work is undecided (owner with the host contract owner). Route parity and the proposal invariants above hold either way.

## Output and Evaluation Matrix

| Output | Objective refs | Requirement/claim refs | Acceptance refs | Verification refs | Evidence expectation |
|---|---|---|---|---|---|
| OUT-001 | OBJ-004; OBJ-005 | CLM-001; CLM-003; CLM-004; CLM-006; REQ-001; REQ-002; REQ-003; REQ-004; REQ-005; REQ-006; REQ-007; REQ-008; REQ-009; REQ-010; REQ-011 | AC-001 | VER-001 | Owner ruling: the twelve accepted scope items and HOST_INTEGRATION V4-HI-20…25. The example documents are the product's own and guard only against change. |
| OUT-003 | OBJ-004 | REQ-001; CLM-002; CLM-005 | AC-002 | VER-002 | Owner ruling: PRD V4-PAR-04 and HOST_INTEGRATION V4-HI-20. On the simulated host the comparison guards against change; a host's own route on its three channels is the independent comparison. |
| OUT-002 | OBJ-004; OBJ-005 | REQ-002; CLM-002 | AC-003 | VER-003 | Owner ruling: PRD V4-REC-01 and V4-CST-05. |
| OUT-001 | OBJ-004; OBJ-005 | REQ-003; CLM-003; CLM-004 | AC-004 | VER-004 | Owner ruling: HOST_INTEGRATION V4-HI-21 and V4-HI-11. The expected basis is the one the fixture's reads state. |
| OUT-003 | OBJ-004 | REQ-004; CLM-006 | AC-005 | VER-005 | Owner ruling: the lifecycle drawn in HOST_INTEGRATION V4-HI-23 and V4-HI-22. |
| OUT-003 | OBJ-004 | REQ-005; CLM-006 | AC-006 | VER-006 | Owner ruling: HOST_INTEGRATION V4-HI-23, "if the outcome cannot be observed → outcome unknown". |
| OUT-003 | OBJ-004 | REQ-006; CLM-003 | AC-007 | VER-007 | Owner ruling: HOST_INTEGRATION V4-HI-23. |
| OUT-003 | OBJ-004 | REQ-007 | AC-008 | VER-008 | Owner ruling: HOST_INTEGRATION V4-HI-23, "a later selection never retargets a proposal". |
| OUT-003 | OBJ-004 | REQ-008; REQ-005 | AC-009 | VER-009 | Owner ruling: HOST_INTEGRATION V4-HI-23. The effect count on a host comes from that host's receipts, which the product does not write. |
| OUT-001 | OBJ-004 | REQ-009; CLM-002 | AC-010 | VER-010 | Owner ruling: HOST_INTEGRATION V4-HI-24. |
| OUT-003 | OBJ-004; OBJ-005 | REQ-010; REQ-002; CLM-004 | AC-011 | VER-011 | Owner ruling: HOST_INTEGRATION V4-HI-25 and PRD V4-AUT-03. Outside source for the host-apply negative: SWBPIPE's own operation corpus, whose expected outcomes SWBPIPE wrote. |
| OUT-003 | OBJ-004; OBJ-005 | REQ-011; REQ-005; CLM-006 | AC-012 | VER-012 | Owner ruling: HOST_INTEGRATION V4-HI-23 and V4-HI-25. |
| OUT-002 | OBJ-004; OBJ-005 | REQ-012; CLM-004; AX-002 | AC-013 | VER-013 | Owner ruling: the adopted first-increment policy as PRD V4-AUT-03 and V4-AUT-04 state it. |
| OUT-002 | OBJ-004; OBJ-005 | REQ-013; CLM-001; CLM-002; CLM-003; CLM-004; CLM-005 | AC-014 | VER-014 | Owner ruling: the accepted decomposition's allocation of each act. |
