---
schema: chirality-deliverable-sow/v1
deliverable_id: DEL-09-09
package_id: PKG-09
decomposition_basis: execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z
project_scope_refs: [SOW-073, SOW-203, SOW-204]
package_objective_refs: [OBJ-004, OBJ-008]
---

# External control and catalog-extension trace

## Purpose and Objective Traceability

This deliverable examines the boundary at which SWBPIPE's operations are reached from outside it. It contributes two witnesses on identified App and SWBPIPE candidates. In the first, the App's Codex, with SWBPIPE's external interface enabled by the person, inspects the model and submits a proposal, and the engineer accepts it in SWBPIPE; the chain is followed from the basis originally inspected to the host's receipt. In the second, one newly added catalog operation is traced through the human interface, the embedded tools and the external adapter, with an account of what was generated and what extra work each surface took. That account is the evidence for the owner's decision on the catalog-extension promise. The App external-host examination owner integrates it. It builds neither application.

It serves OBJ-004 (shared operation meaning, host authority and recovery) and OBJ-008 (candidate-specific verification that does not overstate partial evidence). Its sources are PRD §§4.4–4.5, V4-PAR-05, OQ-02, OQ-10 and OQ-11, HOST_INTEGRATION V4-HI-01…04, 10…12, 20…25, 30…33, 40…42, 50…52 and 70…71, and EXAMINATION §§1–2, V4-EXM-24 and V4-EXM-25. The draft 4.0.0 release target names no exit criterion for this deliverable.

| Assigned scope | Local contribution | Output |
|---|---|---|
| SOW-073 | One newly added catalog operation traced across all three channels before any claim of extension or maintenance saving | OUT-002; OUT-003 |
| SOW-203 | The candidate's extension behaviour examined: generated surfaces, extra work and the disposition of the extension criterion | OUT-002; OUT-003 |
| SOW-204 | The App Codex external journey through host-enabled access, the engineer's actual acceptance and recovery from original basis to receipt | OUT-001 |

## Deliverable Definition — Ontology

- **OUT-001** — The V4-EXM-25 case suite and one result record per case on the identified candidates: inspection and submission by the App's Codex, the engineer's actual acceptance in SWBPIPE, and the chain from original basis through refusal or application to the host's receipt, including an intervening edit and a lost acknowledgment or interruption. Supports SOW-204; OBJ-004 and OBJ-008.
- **OUT-002** — The V4-EXM-24 trace: one newly added catalog operation followed through the human interface, the embedded tools and the external adapter on an identified candidate, with outcomes and availability compared on the same model revision and operation. Supports SOW-073 and SOW-203; OBJ-004 and OBJ-008.
- **OUT-003** — The work account and the extension-criterion disposition: every generated surface, every piece of additional adapter or interface work with its responsible contributor, and either the undecided promise or the actual decision to retain, narrow or defer it, with its consequences. Supports SOW-073 and SOW-203; OBJ-004 and OBJ-008.

Terms:

- **Channels.** The human interface, the embedded tools and the external adapter: three routes to the same operation, validation and application.
- **External control cases.** XC-00 identify the candidates; XC-01 access never enabled, unavailable, and enabled; XC-02 inspect, submit, accept, receipt; XC-03 an intervening edit makes the proposal stale; XC-04 a later selection cannot retarget; XC-05 duplicate submission; XC-06 lost acknowledgment and interruption; XC-07 unknown outcome; XC-08 accepted, then stale at application; XC-09 a positive faithful record of the acceptance and the false-attribution negatives; XC-10 the same route, policy and declared-checkpoint treatment as the embedded and human channels; XC-11 reads, checks and unavailability compared across channels; XC-12 access disabled while a proposal is queued.
- **The extension promise.** A new catalog operation becomes available to every actor without separate work. Whether it is retained, narrowed to generated surfaces or deferred is undecided (TBD-001).
- **Evidence kinds kept apart.** A test definition, a recorded replay, a live observation, an actual human act and a host receipt each keep their own identity in the evidence set. Only a joined witness on the actual host can pass a live case.

Boundary:

- **CLM-001** — The App external-host examination owner owns the case definitions, the coordination, the joined evidence and the coverage account. SWBPIPE's owner supplies channel outcomes. The owner decides the extension promise with the host contract owner.
- **CLM-002** — `DEL-03-01` owns the catalog, the read basis and the map of generated surfaces and adapter responsibility; `DEL-03-02` the meanings of proposal, validation and outcome; `DEL-03-03` the App's external receiving and configuration; `DEL-04-01` the operation policy; `DEL-04-02` the grant display; `DEL-04-03` the act and run records; `DEL-05-01` the embedded-loop requirements; `DEL-02-03` the per-surface compatibility report; `DEL-09-01` the examination support. Five acts are reserved to a person: marking checked, accepting a proposal where autonomy requires it, engineering approval, professional reliance, and changing the grant or enabling external access. Host content read over the external channel may reach the model the person selected; the App records the destination for each turn and shows it.
- **CLM-003** — SWBPIPE's own project builds the host's catalog and domain truth, its validation and application route, its endpoint, loop, panel and views, its origins and receipts, and the means by which it offers, presents and records human acts. The person enables external access, and the engineer accepts a proposal in SWBPIPE. Recording an act does not make the host or the recorder its actor. Professional reliance stays with the human, and certification or engineering approval with the accountable professional.
- **CLM-004** — The human relays files between the two projects. A prepared contract, a component pass or a received draft is no evidence of agreement, delivery, adoption or a completed connected witness; this examination's inputs are SWBPIPE's actual contributions.

## Completion and Reliance Basis — Epistemology

- **REQ-001** — Examination is bound to the identified App and SWBPIPE candidates, the operation and catalog contract, the model basis, the App's external receiving contribution, the operation policy in force, configuration and date.
- **REQ-002** — The App's Codex reaches the host through the catalog-derived machine-local MCP or CLI interface the host selected; this deliverable does not choose the transport. Access is off unless the person enables it, and disabled or unavailable access is reported as such. Enabled external operations use the same validation and application route, autonomy settings and reserved-act policy as the embedded and human channels. At a declared checkpoint the act is requested and recorded only when the person performs it; XC-10's checkpoint parts examine that recording, and a hold is examined only for a workflow that takes up the governance phase.
- **REQ-003** — The V4-EXM-25 witness is completed: the App's Codex inspects and submits a proposal, the engineer actually accepts it in SWBPIPE, and application is traced to the host's receipt. The original read basis (workspace identity, generation, model revision and canonical content identity) is kept through the chain, with origin and old and new values in the host's views. Only this joined witness passes; a definition, a component pass or an honest report of absence does not.
- **REQ-004** — The witness includes an intervening edit and a lost acknowledgment or interruption. A stale basis is refused with its reason; a later selection cannot retarget the proposal; submitting the same proposal twice has one domain effect, shown from the host's domain evidence, and where that effect is not observed the record says "one effect unevidenced". An outcome that cannot be observed stays unknown; a transport acknowledgment, deduplication or reconnection proves no domain outcome.
- **REQ-005** — Exactly one new catalog operation is traced across the three channels. Reads and standing, availability reasons, invalid and stale refusal, non-mutating checks, validation, old and new values, application and recovery are compared on the same model revision and operation. Generated behaviour and all additional work, including adapter work, are recorded. Shared schemas or common validation establish neither operational integration nor automatic extension.
- **REQ-006** — The original promise stays identifiable. If it is retained, addition without other changes is verified on all three surfaces with the same availability reasons. If it is narrowed or deferred, the chosen surfaces or staging, the decision actor and what is superseded are bound before that criterion is verified. Until a decision exists, the trace is evidence for it and passes no weaker criterion.
- **REQ-007** — Execution, a queued proposal, the acceptance of an edit, checking, engineering approval and professional reliance are kept distinct. An act actually performed is recorded faithfully, the decision actor apart from the recorder, with content, scope and purpose. No act is fabricated from a success, a receipt, a direct application or the agent's findings. The proposal control says accept, not approve. A content-bound act lapses visibly when its content changes, and acceptance of an edit is not required before an independently evidenced check.
- **REQ-008** — Each result binds candidate, configuration and date and has one of the five examination outcomes, with the host's receipts linked and never copied into a second store of truth. Material is invented. Replay and source evidence are kept apart from the live witness and the engineer's act. A changed candidate reopens the affected cases with criteria unchanged. Interface evidence follows the WebKit, Chromium and native package routes of DEL-09-01, and browser evidence never replaces a native observation.
- **REQ-009** — This deliverable performs no act owned by another, as allocated in CLM-001…CLM-004: it observes and faithfully records those contributions and neither implements, impersonates nor decides them.

- **AC-001** — The input account identifies the candidates, configuration and date, the original read basis, the common operation boundary, the receiving contracts and the policy in force, with what SWBPIPE actually supplied kept apart from what is open or unavailable. Verify by VER-001. [REQ-001]
- **AC-002** — With access never enabled the App makes no host request and reports the channel as not enabled; with the host's access off or unavailable that is reported as such; and once the person enables it, the App's Codex reaches the host only through the host's catalog, validation and application route under the same autonomy and reserved-act policy (XC-01, XC-10, XC-12). Verify by VER-002. [REQ-002]
- **AC-003** — On the identified candidates the chain is observed whole: inspection and submission by the App's Codex, the proposal reported as queued and never as accepted, the engineer's acceptance in SWBPIPE, application and the host's receipt, with the original basis, the origin and the old and new values in the host's views (XC-00, XC-02). Verify by VER-003. [REQ-003]
- **AC-004** — After an intervening edit the proposal is refused as stale against the originally inspected basis, with its reason; a later selection does not retarget it; after a lost acknowledgment or an interruption the outcome reported is the one read from the host's receipt, or unknown; and a repeated submission shows one domain effect in the host's evidence, or is recorded as "one effect unevidenced" (XC-03…XC-08). Verify by VER-004. [REQ-004]
- **AC-005** — One new operation is traced on all three channels on the identified candidate, and the comparison covers availability, reads and standing, non-mutating checks, invalid and stale refusal, validation, old and new values, application and recovery, with each generated surface and each piece of additional work named and each gap or non-comparable observation kept (XC-11). Verify by VER-005. [REQ-005]
- **AC-006** — The extension account states the original promise and the decision actually made on it, and verifies exactly that criterion: availability without other changes on all three surfaces if retained, or the bound surfaces and staging if narrowed or deferred. With no decision, it reports the trace and claims no extension pass and no saving. Verify by VER-006. [REQ-006]
- **AC-007** — The engineer's actual acceptance is recorded with actor, recorder, bound content, scope and purpose; and a queued state, a success, a receipt, the agent's findings or model text saying the engineer accepted produce no acceptance, check, approval or reliance. The proposal control is labelled accept, a changed content shows the act as lapsed, and an independently evidenced check is recorded without requiring a prior acceptance (XC-09). Verify by VER-007. [REQ-007]
- **AC-008** — Every result states candidate, configuration, date and standing, links the host's receipts, keeps definition, replay, source, live and human-act evidence apart, and lists the cases a changed candidate reopens. Verify by VER-008. [REQ-008]
- **AC-009** — The account assigns each excluded act of REQ-009 to its owner and each received contribution to its evidence. Verify by VER-009. [REQ-009]

## Production and Verification Method — Praxeology

The examination owner first binds the upstream contributions and the open decisions and prepares the cases. SWBPIPE's evidence arrives through the human. Cases run only when the operation, the policy, the host environment and the contributions exist. The two witnesses are joined around the same operation boundary and may share one evidence set. Result records and the work account have one defined form, checked against its rules before they are relied on, and a rehearsal on a test double never counts toward a witness.

- **VER-001** — Inspect the input account against the catalog, proposal and receiving contracts, the policy in force and the candidate evidence supplied.
- **VER-002** — On the candidates, exercise access never enabled, unavailable and enabled by the person, and disabling while a proposal is queued; compare the external route with the host's catalog, validation and autonomy policy. Record which interface the host selected.
- **VER-003** — Observe the inspect and submit journey and the engineer's acceptance in SWBPIPE, then reconcile the host's views, the original basis and the origin with the application and the host's receipt. Identify the human actor apart from the recording mechanism.
- **VER-004** — Exercise an intervening edit, a later selection, a repeated submission and a lost acknowledgment or interruption. Compare the original basis with the refusal or application and the host's receipt, judging one domain effect from the host's domain evidence.
- **VER-005** — Trace the one new operation through the three channels on the same model revision, compare each category of REQ-005, inspect the generated and adapted surfaces, and reconcile the additional work with its contributor.
- **VER-006** — Compare the trace and the work account with the original promise and with the decision made on it, or state that none exists.
- **VER-007** — Inspect the record of the real acceptance against the act observed, and apply each false-attribution negative. No professional act is manufactured to complete a test.
- **VER-008** — Audit the results against EXAMINATION V4-EXM-01…05: identity, outcomes, evidence kinds and routes, receipt references and reopened cases.
- **VER-009** — An independent reviewer inspects the account of acts against CLM-001…CLM-004 and REQ-009.

## Governing Values and Decisions — Axiology

- **AX-001** — Parity is about operation meaning, truthful standing and recovery, not identical gestures. Better means more categories of REQ-005 observed to agree across the three channels on the same revision; never by counting a shared schema, a transport or common validation as agreement.
- **AX-002** — The original promise stays visible until the owner decides it. Better means a more complete work account, with every generated surface and every piece of additional work named with its contributor; never by examining a criterion weaker than the one decided.
- **AX-003** — The person is the actor of every human act; the host offers and records it and the examiner preserves its evidence. The witness needs the engineer's actual acceptance and no favourable engineering approval or professional reliance. Better means more of each recorded act traced to the person who performed it; never by inferring an act from a success, a receipt or a record.
- **TBD-001** — Whether the extension promise is retained, narrowed to generated surfaces or deferred is undecided (owner with the host contract owner, with the App and SWBPIPE contract designers). AC-006 cannot pass a final criterion before the decision.
- **TBD-003** — The operation, the autonomy permitted and the candidate environment of the first connected activity are undecided (owner, through the SWBPIPE session, with the App owner). The live cases wait for them.
- **TBD-004** — Whether any host beyond the App and SWBPIPE is essential to examination is undecided (owner). No further host is presumed.
- **TBD-005** — Every live external case needs a facility in SWBPIPE by which the person enables external access and which returns a reference to its capture evidence. Whether SWBPIPE provides one is its owner's decision; without it the channel stays not enabled and the live cases are blocked. Live joins with SWBPIPE are held until the owner resumes SWBPIPE UI-SUCCESSOR; no live external-control or extension-trace case runs before then.

## Output and Evaluation Matrix

| Output | Objective refs | Requirement/claim refs | Acceptance refs | Verification refs | Evidence expectation |
|---|---|---|---|---|---|
| OUT-001 | OBJ-004; OBJ-008 | REQ-001; CLM-001; CLM-004 | AC-001 | VER-001 | Owner ruling: the accepted decomposition and EXAMINATION V4-EXM-24/25 state the inputs. What SWBPIPE supplied is read from its own delivered files. |
| OUT-001 | OBJ-004; OBJ-008 | REQ-002; CLM-003 | AC-002 | VER-002 | Owner ruling: HOST_INTEGRATION V4-HI-50…52 state the expected behaviour. It is observed on SWBPIPE's interface and on the App's outgoing requests, independently of the App's trace code. |
| OUT-001 | OBJ-004; OBJ-008 | REQ-003 | AC-003 | VER-003 | Owner ruling: EXAMINATION V4-EXM-25 states the chain. It is observed in SWBPIPE's own views and receipt and in the acceptance the examiner watched the engineer perform. |
| OUT-001 | OBJ-004; OBJ-008 | REQ-004 | AC-004 | VER-004 | Owner ruling: HOST_INTEGRATION V4-HI-23 states the expected refusal and single effect. They are observed in the host's domain evidence and receipts. |
| OUT-002 | OBJ-004; OBJ-008 | REQ-005 | AC-005 | VER-005 | Owner ruling: EXAMINATION V4-EXM-24 states what is compared. It is observed in the host's behaviour on each of its three surfaces for the same operation and revision. |
| OUT-003 | OBJ-004; OBJ-008 | REQ-006 | AC-006 | VER-006 | Owner ruling: the original promise in PRD V4-PAR-05 and the owner's decision on it. |
| OUT-001 | OBJ-004; OBJ-008 | REQ-007; CLM-003 | AC-007 | VER-007 | Owner ruling: PRD V4-AUT-03…05 and V4-REC-05 state what may be recorded. The App's record is set against the act the examiner watched the engineer perform. |
| OUT-001 | OBJ-008 | REQ-008 | AC-008 | VER-008 | Owner ruling: EXAMINATION V4-EXM-01…05. The record-format checks compare the product's own schemas and guard only against change. |
| OUT-003 | OBJ-004; OBJ-008 | REQ-009; CLM-001; CLM-002; CLM-003; CLM-004 | AC-009 | VER-009 | Owner ruling: the accepted decomposition's allocation of each act. |
