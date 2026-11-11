---
schema: chirality-deliverable-sow/v1
deliverable_id: DEL-03-03
package_id: PKG-03
decomposition_basis: execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z
project_scope_refs: [SOW-148, SOW-183, SOW-184]
package_objective_refs: [OBJ-004]
---

# Local external-agent receiving adapter

## Purpose and Objective Traceability

This deliverable contributes the App's side of external host access. Once the person has enabled it, the Chirality App's Codex can inspect a host and submit to it through the host's catalog-derived, machine-local MCP or command-line interface, and until then the App sends that host nothing. What the App receives over the channel keeps the meaning the host gave it: the operation, its availability, the read's standing and basis, the host's validation and autonomy rules, the acts reserved to the person, and outcomes no stronger than the host reported. The App external-host integration owner produces it; the host owner supplies the endpoint.

It serves OBJ-004 (shared operation meaning, host authority and recovery). Its sources are PRD V4-PAR-01…05, V4-AUT-01…05 and V4-HOST-02; ARCHITECTURE V4-ARC-21; HOST_INTEGRATION V4-HI-20…25, V4-HI-30…33, V4-HI-40…42 and V4-HI-50…52; and EXAMINATION V4-EXM-25. The draft 4.0.0 release target names no exit criterion for this deliverable.

| Assigned scope | Local contribution | Output |
|---|---|---|
| SOW-148 | The App's native Codex access configuration and receiving for a host's catalog-derived MCP server or command-line interface | OUT-001; OUT-002; OUT-003 |
| SOW-183 | The same validation, autonomy and reserved-act rules on the external channel as for the catalog's other consumers | OUT-001; OUT-002; OUT-003 |
| SOW-184 | Access machine-local and off until the person enables it, with disabled and unavailable access reported as such | OUT-001; OUT-002; OUT-003 |

## Deliverable Definition — Ontology

- **OUT-001** — The App-side configuration of Codex's native MCP or command-line access to the host interface the host selects, and the receiving adapter as far as one is needed, using the catalog and proposal contracts. It adds no second transport, no server of the App's own and no second route to the host's objects. Supports SOW-148, SOW-183 and SOW-184; OBJ-004.
- **OUT-002** — The enablement and operation-policy interface definition: the person's enablement, disabled and unavailable behaviour, what enabling does and does not grant, the App's and the host's responsibilities, how the original basis and outcomes are handled, and the open choices at their points of need. Supports SOW-148, SOW-183 and SOW-184; OBJ-004.
- **OUT-003** — External consumer contract fixtures and their results for the App receiving boundary: disabled and unavailable access, enabled inspection and submission, policy behaviour and truthful outcomes. Each result states whether the endpoint was a host's or a simulation. Supports SOW-148, SOW-183 and SOW-184; OBJ-004.

Terms:

- **Native paths.** The two ways the App's Codex reaches a host endpoint through its own capability: a configured MCP server whose tools the model calls, or the host's command-line interface run through Codex command execution. The host chooses which it offers.
- **Host enablement record.** The person's act of enabling or disabling the host's external interface on this machine, as the host's own facility captures it. Enabling and disabling are reserved to the person.
- **App-side access configuration.** Whether the App's Codex is configured to reach that endpoint, where, and at whose direction. It is an ordinary configuration change made at the person's direction and is never evidence of enablement.
- **Channel state.** Disabled; enabled; or endpoint unavailable. Enabled holds only while the host enablement record is in force, the App-side configuration is present and the endpoint is reachable. Where the App cannot observe the host's record the channel is shown as unconfirmed and treated as disabled. The channel state never replaces a request's own outcome.
- **Machine-local.** The endpoint is a local process, a local socket or a loopback origin on the person's machine.
- **External dispatch record.** What the App records from one native item it observed: the path, the kind of request, the operation and catalog edition, the requested mode and proposal identity, the native status, the outcome with who reported it, the host's result where one was isolated, and the limits of the evidence. A native completion alone establishes no host outcome.
- **Checkpoint observation.** What the adapter observes on the channel about a declared checkpoint (a proposal queued, an act observed, an item leaving, an observation lost or recovered) and passes to `DEL-02-03`. The adapter evaluates no arrival, disposition or hold.
- **Model destination.** Where the content of an App conversation goes: the model the person selected for it. The App records the destination the supplier reported, at the scope it was reported, and shows it in the channel status.

Boundary:

- **CLM-001** — The App external-host integration owner owns the App's native access configuration, the receiving adapter, the enablement definition and the consumer fixtures. The host owner, SWBPIPE's own project for the first host, owns the endpoint or server, the catalog, domain objects and truth, validation, application, receipts and views.
- **CLM-002** — `DEL-03-01` owns the catalog and read-basis contract and `DEL-03-02` the proposal, validation and outcome contract; this adapter uses both unchanged. `DEL-04-01` owns the operation policy and reserved acts, `DEL-04-02` the visible autonomy state, `DEL-02-01` the checkpoint declarations, `DEL-02-03` checkpoint recording and, for a workflow that takes up the governance phase, holds. `DEL-01-01` owns the stock Codex child and its native MCP, command-execution and status surfaces, and `DEL-01-02` the state of a request in flight across an interruption or an App relaunch.
- **CLM-003** — The host offers, records and presents human acts; the person performs them, and professional reliance stays with the accountable professional. `DEL-09-09` owns the joined external witness and the catalog-extension trace on actual candidates; `DEL-04-03` writes the run record that the dispatch records enter.
- **CLM-004** — The host's contributions (endpoint, enablement facility, route, receipts) are needed where a connected journey or its examination relies on them. A fixture run against a simulation shows the App's receiving and nothing about a host.

## Completion and Reliance Basis — Epistemology

- **REQ-001** — The App receives through Codex's native tools against the host's catalog-derived MCP or command-line interface, using the catalog, read-basis, proposal and outcome meanings of CLM-002. Operation identity, the availability reason, the meaningful content and standing of a read, and the basis originally inspected are kept through submission, including for a non-mutating check where the host exposes one. [SOW-148, SOW-183; V4-ARC-21; V4-HI-50]
- **REQ-002** — External access is machine-local and off unless the person enables it. Disabled access is distinguished from access that is enabled but unavailable. Enabling grants no autonomy and changes no operation's class. Host content read over the channel may reach the model the person selected for the App conversation, cloud included; the App gates neither enablement nor requests on that destination, adds no other destination (no App relay, telemetry or remote endpoint), and records and shows the destination as information. A host may restrict its own channel. [SOW-184; V4-HI-52; V4-HI-40; owner ruling on model destination, APP-V4-FIRST-INCREMENT-20260928-DECISION-2 D5]
- **REQ-003** — An enabled request passes through the host's same validation and application route under the same autonomy and reserved-act rules as the catalog's other consumers. A direct application is made only under a direct treatment in effect within the person's grant and the host's policy; otherwise the direct request is *not permitted*, never silently converted, and the agent may propose. Routine tool permission is the person's own Codex setting and stands for no human act. A workflow checkpoint keeps its required act: the agent carrying out the workflow asks for it, the App records the request where it can identify it and the act only when the person performs it, and the App claims no hold; a hold on this channel belongs to the governance phase and to `DEL-02-03`. [SOW-183; V4-HI-20…23, V4-HI-30…42, V4-HI-50…51]
- **REQ-004** — The adapter keeps the outcome contract: a stale basis is refused with its reason, a later selection does not retarget, a repeated submission has at most one effect per item (the host's obligation, to be evidenced by the host), and an outcome that cannot be observed is unknown. A transport success, a queued status or a receipt fabricates no acceptance, check, approval or professional reliance. A human act the host evidences may be recorded faithfully, with its actor apart from its recorder and bound to its content; no act supplies another, and none is made a prerequisite of another independently evidenced act. [SOW-183; V4-HI-21…25, V4-HI-30…33, V4-HI-70…71]
- **REQ-005** — This deliverable performs no act owned by another, as allocated in CLM-001…CLM-003: it writes no catalog or proposal contract, builds no endpoint, server, catalog or domain implementation, validates or applies nothing, issues no receipt, presents no host view, performs no human act, rules no policy and runs no joined examination. It may use, link and faithfully record what it is supplied.
- **REQ-006** — The definition and the fixture results identify the endpoint actually used or the simulation in its place, the contract and policy relied on and the App candidate. They state which surfaces are generated from the catalog and what receiving work the adapter still does, and keep the open choices open. [V4-HI-03, V4-HI-50…52; V4-EXM-24…25]

- **AC-001** — On an identified App candidate, the App's Codex inspects and submits against a catalog-derived host interface over the native path the host offers, and operation identity, availability reason, read standing and the originally inspected basis arrive unchanged. The evidence says whether the endpoint was a host's or simulated. Verify by VER-001. [REQ-001]
- **AC-002** — While access is disabled the App reports the channel as disabled and makes no request to the host; for a request an agent originates, the host's own refusal is the authoritative off. After the person enables access, an unreachable endpoint or an unavailable operation is reported as such, with the catalog's reason where the host gives one. The endpoint is on the person's machine, and enabling grants no autonomy and adds no destination beyond the conversation's selected model. Verify by VER-002. [REQ-002]
- **AC-003** — Under an identified operation policy, an external request follows the host's one route and distinguishes a granted direct operation, a proposal-only operation, a reserved act and a workflow checkpoint. There is no second route to the host's objects, and no policy is decided here. Verify by VER-003. [REQ-003]
- **AC-004** — Over the channel, a stale proposal is refused with its reason, a later selection leaves the original target, a repeated submission follows the one-effect contract, and an unobserved acknowledgment leaves the outcome unknown. A native completion or a transport success is never reported as the host's outcome. Verify by VER-004. [REQ-004]
- **AC-005** — A success, a queued status or a receipt produces no attributed human act; an act actually performed and bound to its content is kept, with its actor apart from its recorder. A separately evidenced check, approval or reliance is neither inferred nor erased, and none waits on an unrelated acceptance. Verify by VER-005. [REQ-004]
- **AC-006** — The definition names the owner of every act REQ-005 excludes, the contracts and policy it relies on, each open matter with its owner and point of need, and the host contribution a joined witness needs. Transport, authentication and wire details are those agreed between the App external-host integration owner and the host owner (TBD-007), and are stated as open until agreed; the definition adds no wire field of its own and no common service. Verify by VER-006. [REQ-005; REQ-006]
- **AC-007** — The fixture set covers AC-001…AC-005, each result naming its candidate, contract, policy and whether a host or a simulation answered, and states what the generated surfaces supply and what adapter work remains. Verify by VER-007. [REQ-006]

## Production and Verification Method — Praxeology

The App receives the seam the host offers; it does not choose the transport. It configures access only at the person's direction in the App, observes the native items Codex reports and records them. A channel status and a dispatch record are documents with schemas, valid and invalid instances and rules a schema cannot state: an enabled channel has an enablement record in force, a present configuration and a reachable local endpoint; a host outcome is reported only where the host's own result supports it, and otherwise the outcome is unknown. A host document is passed on as supplied. Fixtures use the invented catalogue and simulated host of `DEL-03-01`.

- **VER-001** — Executable check (observes catalog inspection, a non-mutating read or check and a proposal submission over a native path against an identified endpoint or the simulated host): identity, availability, standing and original basis compared with the catalog and proposal contracts.
- **VER-002** — Executable check (observes the App's outgoing requests and the reported channel state with access disabled, enabled by the person, and enabled but unavailable): no App request while disabled, the host's refusal recorded as the authoritative off for an agent's request, truthful unavailability, a local endpoint, and no grant or destination added. On a fixture it observes the App only.
- **VER-003** — Executable check (observes a permitted direct operation, a proposal-only operation, a refused reserved act and a checkpoint whose act is recorded only when performed, under an identified policy), with judgment by an independent reviewer that the App holds no second route. Enforcement by a host is judged from that host's evidence.
- **VER-004** — Executable check (observes what the App reports after an intervening edit, a later selection, a repeated submission and a lost acknowledgment or interruption), compared with the outcome contract of `DEL-03-02`.
- **VER-005** — Executable check (observes the records produced from a success, a queued status and a receipt with no act, and from an act the host evidences): no fabricated attribution, and the performed act kept with actor, content and recorder.
- **VER-006** — Judgment by an independent reviewer: reads the definition against CLM-001…CLM-004, the decomposition's allocation and each open matter below, one excluded act at a time.
- **VER-007** — Judgment by an independent reviewer: inspects the fixture inventory and results for coverage of AC-001…AC-005 and for the candidate, contract, policy and host-or-simulation statement on each.

## Governing Values and Decisions — Axiology

- **AX-001** — The host's policy governs its own channel. No universal ban on external application is read into this contract, and graduated autonomy changes no host's operative policy until that host adopts it. Better means more of what an external request does decided by the host's stated rule and reported with it; never by the App deciding a reserved act or a class.
- **AX-002** — Shared meaning leaves the host's authority whole. Better means more of what crosses the channel arriving as the host stated it, with its reporter and its limits; never by reporting a native success, a configuration or a fixture pass as a host outcome, an enablement or a person's act.
- **TBD-003** — Whether a new catalog operation reaches every actor without separate work is undecided (owner with the host contract owner). This adapter's account of generated surfaces and remaining work is evidence for that decision.
- **TBD-005** — Where shared contracts and components are placed is unagreed (App/shared contract owners). Nothing here presumes a common service.
- **TBD-006** — The operation, the autonomy permitted and the candidate environment of the first connected activity are undecided (owner, through the SWBPIPE session, with the App owner), as are any operation-specific reserved acts. Whether a host adopts and enforces the reserved acts is that host's to evidence.
- **TBD-007** — Which native path a host offers, the transport and its locality, caller authentication, how origin, grant and proposal identity are carried, and the wire schemas are unselected (App external-host integration owner with the host owner). They are settled before an implementation or a qualification depends on them.
- **TBD-008** — Whether a host provides a facility by which the person enables external access and which returns a reference to its capture evidence is that host's decision; without one the channel stays disabled. Whether a launch setting the person makes outside such a facility counts as evidence of enablement is undecided (owner).

## Output and Evaluation Matrix

| Output | Objective refs | Requirement/claim refs | Acceptance refs | Verification refs | Evidence expectation |
|---|---|---|---|---|---|
| OUT-001 | OBJ-004; SOW-148; SOW-183 | REQ-001; CLM-001; CLM-002 | AC-001 | VER-001 | Owner ruling: HOST_INTEGRATION V4-HI-50 and V4-HI-10…12 say what must arrive unchanged. The comparison is against the host's own documents; on the simulated host it guards the App's receiving against change. |
| OUT-001 | OBJ-004; SOW-184 | REQ-002; CLM-001 | AC-002 | VER-002 | Owner ruling: HOST_INTEGRATION V4-HI-52 for locality and default-off; the owner's first-increment ruling on model destination for the selected-model flow and the absence of any other destination. The App's silence is observed on its outgoing requests; the authoritative off is the host's own refusal, which the product does not write. |
| OUT-001 | OBJ-004; SOW-183 | REQ-003; CLM-002; CLM-003 | AC-003 | VER-003 | Owner ruling: HOST_INTEGRATION V4-HI-20…23, V4-HI-30…42 and V4-HI-50…51. Host enforcement is read from the host's evidence. |
| OUT-003 | OBJ-004; SOW-183 | REQ-004; CLM-002; CLM-004 | AC-004 | VER-004 | Owner ruling: HOST_INTEGRATION V4-HI-23. The expected outcomes are those the proposal contract's fixtures state; a durable single effect is read from a host's receipts. |
| OUT-003 | OBJ-004; SOW-183 | REQ-004; CLM-003 | AC-005 | VER-005 | Owner ruling: HOST_INTEGRATION V4-HI-25 and V4-HI-30…33 and PRD V4-AUT-03…05. |
| OUT-002 | OBJ-004; SOW-148; SOW-183; SOW-184 | REQ-005; REQ-006; CLM-001; CLM-002; CLM-003; CLM-004 | AC-006 | VER-006 | Owner ruling: the accepted decomposition's allocation of each act and the open issues' named owners. |
| OUT-003 | OBJ-004; SOW-148; SOW-183; SOW-184 | REQ-006; CLM-004 | AC-007 | VER-007 | Owner ruling: EXAMINATION V4-EXM-25 says what the joined witness needs. The results themselves are the product's own and guard only against change. |
