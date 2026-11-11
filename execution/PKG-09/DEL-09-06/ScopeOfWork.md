---
schema: chirality-deliverable-sow/v1
deliverable_id: DEL-09-06
package_id: PKG-09
decomposition_basis: execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z
project_scope_refs: [SOW-040, SOW-041, SOW-236, SOW-237, SOW-238, SOW-240, SOW-241]
package_objective_refs: [OBJ-001, OBJ-004, OBJ-008]
---

# Connected activity contract and workflow round trip

## Purpose and Objective Traceability

This deliverable defines the first activity in which the App and SWBPIPE work together, a model adjustment and check on an invented piping model, and shows that a workflow made in the App can be carried to the host, refined there and used again in the App. It contributes the activity's definition and handoff, the reusable workflow, the round-trip witness on identified App and host candidates, and the account of what SWBPIPE has been asked for, has answered, has delivered and has had examined. The App connected-activity integration owner integrates it; the human relays between the two projects. It builds neither application.

It serves OBJ-004 (one coordinated activity with a receiving contract), OBJ-008 (candidate-specific round-trip evidence with honest limits) and OBJ-001 (workflow portability, with the standalone core loop preserved). Its sources are PRD §3–3.1, V4-WF-01…06, V4-AUT-01…05, V4-EXT-01 and OQ-11, HOST_INTEGRATION §1 and §11, and EXAMINATION V4-EXM-14 and §4. The draft 4.0.0 release target names this deliverable, with DEL-09-07, for the live SWBPIPE journey (criterion 5): one live embedded journey from a person's request to that person's acceptance. This deliverable supplies the activity that journey runs and the receiving of SWBPIPE's contributions; DEL-09-07 observes the journey.

| Assigned scope | Local contribution | Output |
|---|---|---|
| SOW-040; SOW-041 | The four user activities connected through the App and SWBPIPE, with the App's workflow-making kept alongside host activity | OUT-001 |
| SOW-236 | The connected model-adjustment and checking activity, its reusable method and the first App/host handoff | OUT-001; OUT-002; OUT-003 |
| SOW-237 | Contributions and their examination staged without losing the complete first activity or holding independent App work | OUT-001; OUT-003 |
| SOW-238 | Assumptions, tool needs, revision and actual human checkpoints carried across both applications | OUT-002; OUT-003 |
| SOW-240 | The increment's scope, accountable owners and checks set before it runs | OUT-001; OUT-004 |
| SOW-241 | Questions, commitments received and evidence accounted for through human-relayed files | OUT-004 |

## Deliverable Definition — Ontology

- **OUT-001** — The connected increment's definition: the one complete first activity, the four user activities it connects, which contributions are the App's, which are shared and which are SWBPIPE's, the owner and check for each, and the App/host handoff. Supports SOW-040, SOW-041, SOW-236, SOW-237 and SOW-240; OBJ-001, OBJ-004 and OBJ-008.
- **OUT-002** — A reusable model-adjustment and checking workflow that states its assumptions, required inputs and host tools, declared human checkpoints and returned outputs and evidence, with a source-qualified revision history, usable in both applications. Supports SOW-236 and SOW-238; OBJ-004 and OBJ-008.
- **OUT-003** — The V4-EXM-14 round-trip witness on identified App and host candidates, with one result record per case. Supports SOW-236, SOW-237 and SOW-238; OBJ-004 and OBJ-008.
- **OUT-004** — The contribution account: every question put to SWBPIPE, every answer, commitment and contribution received, the checks that receive SWBPIPE's catalog, and what is still missing and who owns it. Supports SOW-240 and SOW-241; OBJ-004 and OBJ-008.

Terms:

- **The four user activities.** The practitioner changes and checks a model and works with results and reports; the workflow maker develops, reuses and refines a method; the application builder realises catalog operations and tools; the coordinator bounds work, receives returns and decides.
- **The first activity.** On the host: inspect the model, propose a change, check without changing anything, meet an intervening edit, and reach an outcome with its receipt. Adding supports and adjusting a run is the proposed fixture, not a selected operation (TBD-001).
- **Four facts kept apart.** For a workflow crossing the boundary: the bytes selected and resolved; what was actually supplied; what the provider adopted; and the behaviour observed. A portable file or a successful registration shows none of the last three.
- **Round-trip cases.** W14-00 identify both candidates; W14-01 transfer the reviewed workflow unadapted; W14-02 adapt it on the host; W14-03 required tools available, and an explicit unsupported-capability outcome; W14-04 a declared checkpoint under direct autonomy; W14-05 a real human act recorded faithfully, with the fabrication negatives; W14-06 content changed after an act; W14-07 interruption and replay; W14-08 supplied, adopted and observed compared; W14-09 the host's refinement made usable in the App; W14-10 revision and replay history.
- **Contribution standing.** Each contribution from SWBPIPE has exactly one standing: prepared (an App file exists); relayed (its delivery to the SWBPIPE session was observed); answered (an answer returned, with its source and custody); committed (an explicit commitment by the SWBPIPE owner); delivered (an identified contribution exists); adopted (the App's receiving side records its use); examined (a candidate-bound observation with an outcome). A stated intention is answered, not committed.

Boundary:

- **CLM-001** — The scope is one complete first connected activity, built up in stages as inputs become usable. A defined contract or an inspected source is not a completed activity.
- **CLM-002** — The App connected-activity integration owner owns the activity definition, the App and shared contribution, the handoff, the V4-EXM-14 witness and the contribution account, and keeps the four user activities connected.
- **CLM-003** — The feature owners build and check what the activity uses: `DEL-02-01` workflow declaration, identity and revision; `DEL-02-02` review and registration; `DEL-02-03` transfer, adaptation and execution compatibility; `DEL-03-01`, `DEL-03-02` and `DEL-03-03` the catalog and read basis, proposals and outcomes, and external receiving; `DEL-04-01` operation policy, `DEL-04-02` the visible autonomy grant and `DEL-04-03` act and run records; `DEL-05-01` the loop and model requirements and `DEL-05-02` the panel; `DEL-01-01` the observation of the guidance actually carried to the supplier and of the model and destination each turn reached, which `DEL-04-03`'s run record holds; `DEL-09-01` the examination support. Host content read over the external channel may reach the model the person selected; the App records that destination for each turn and shows it, and applies no gate.
- **CLM-004** — SWBPIPE's own project builds SWBPIPE: its domain objects and catalog, validation and application, views, receipts, loop and panel, its realisation of workflows and tools, and its evidence of execution. The host offers, presents and records human acts; the person performs them.
- **CLM-005** — The owner, through the SWBPIPE session and with the App owner, chooses the operation, the autonomy permitted and the environment (TBD-001). For the first increment, five acts are reserved to a person: marking checked, accepting a proposal where autonomy requires it, engineering approval, professional reliance, and changing the grant or enabling external access. In the App, routine tool permission is the person's own Codex setting; in that increment hosts have no classifier mode. Each host adopts, names and enforces its own list, and SWBPIPE's adoption is part of its contribution. Accountable people perform their own checking, acceptance, approval and reliance.
- **CLM-006** — `DEL-09-02` qualifies the standalone App; `DEL-09-07` qualifies the local host journeys V4-EXM-20…23, using the activity defined here; `DEL-09-09` examines external control and catalog extension; `DEL-09-05` examines longer-work recovery; `DEL-11-03` prepares the decision packet. Within `app/supplier_checks/`, this deliverable owns the checks that receive SWBPIPE's catalog and compare it with the App's projection; DEL-09-07 relies on them and owns none.

## Completion and Reliance Basis — Epistemology

- **REQ-001** — The definition covers the complete first activity and the App and shared contribution, with basis, owners, outputs, interfaces and examination, and coordinates the separately owned scenarios of CLM-006 without reducing the increment to unconnected component checks.
- **REQ-002** — The workflow states its assumptions, inputs, required host tools, human checkpoints and returned outputs and evidence. Source-qualified selection and revisions survive transfer to the host, adaptation and refinement there, and reuse in the App, with the four facts kept apart.
- **REQ-003** — The round trip exercises required-tool availability, an explicit unsupported-capability outcome, checkpoint identity, interruption, and revision and replay history. A missing capability is visible and fabricates no tool execution. A declared checkpoint's act is requested, and recorded only when the person performs it, whatever the autonomy. A checkpoint holds the run only in a workflow that takes up the governance phase; otherwise it is plan guidance and neither application holds. History keeps what actually ran and what remains unknown.
- **REQ-004** — The operation policy, the autonomy granted and each content-bound human act are carried through the handoff and the record. Execution, acceptance of an edit, checking, approval and professional reliance stay distinct, each with its own actor and evidence; success establishes none of them, and none is required before another independently evidenced act. A person's actual act is recorded faithfully with actor, subject and recorder distinguished, and a change of content visibly changes the act's standing.
- **REQ-005** — Human-relayed repository files carry every question and contribution, and each contribution holds one standing as defined above, bound to its supplier, its revision and its limits. A prepared handoff is never reported as a commitment or a delivery, and unknown custody stays unknown.
- **REQ-006** — Connected work is staged around the inputs that actually exist, while the complete first activity and the standalone core loop are both kept. The first activity needs neither a connector nor Domains. Independent App definition and construction do not wait for the joined witness.
- **REQ-007** — OUT-003 is complete only with the actual joined round trip on identified candidates. Each case ends as passed, failed, blocked, not run or inconclusive, bound to candidate, configuration (harness and model versions, model server) and date; no test double, replay or component pass stands for a case, and an honest account of absence does not complete the witness. Verification material is invented. A changed candidate reopens the affected cases with their criteria unchanged.
- **REQ-008** — This deliverable performs no act owned by another, as allocated in CLM-003, CLM-004, CLM-005 and CLM-006. It stays responsible for defining and joining those contributions and for OUT-003.

- **AC-001** — The definition accounts for all seven assigned scope items, the four user activities, one complete first activity, each contribution as the App's, shared or SWBPIPE's, and an owner and a check for each. The operation, the autonomy permitted and the candidate environment it names are the ones the owner chose; any not yet chosen is stated as unchosen. Verify by VER-001. [REQ-001]
- **AC-002** — The workflow identifies its reviewed source and revision, assumptions, inputs and tools, declared checkpoints and expected outputs and evidence, and defines adaptation on the host and refinement back to the App so that no same-name entry is silently rebound and no earlier basis is lost. Verify by VER-002. [REQ-002]
- **AC-003** — On identified App and host candidates, the reviewed workflow is carried to the host, adapted and refined there, and made usable in the App (W14-00, W14-01, W14-02, W14-08, W14-09), with the four facts each separately evidenced, and with interruption and revision and replay history (W14-07, W14-10). Verify by VER-003. [REQ-002; REQ-003; REQ-007]
- **AC-004** — In the same round trip: an available required tool runs and a missing capability yields an explicit unsupported outcome (W14-03); a declared checkpoint's act is not recorded until the person performs it, under direct autonomy (W14-04); a performed act is recorded with its subject and actor, apart from its recorder, and no act appears from tool success or absence (W14-05); and after the content changes, the earlier act remains in the history with changed standing and no current approval is shown (W14-06). Verify by VER-004. [REQ-003; REQ-004]
- **AC-005** — Every contribution in the account holds exactly one standing, supported by the evidence that standing requires, and every missing contribution has an owner or a stated unresolved allocation. A delivered contribution is identified by the supplier revision it came from. Verify by VER-005. [REQ-005]
- **AC-006** — The staged account keeps independent App work, the complete first activity and the separately owned examinations, requires neither a connector nor Domains to begin, and states each input's actual standing. Verify by VER-006. [REQ-006; CLM-006]
- **AC-007** — Every case record binds its observation to candidate, configuration and date and classes it honestly. A case rests on native or connected execution where it requires it, never on browser or replay evidence, and no favourable approval is inferred. Verify by VER-007. [REQ-007]
- **AC-008** — The definition and the account keep each excluded act with its owner and keep the integration owner responsible for the whole join. They decide no policy and assert no acceptance, release, replacement or professional reliance. Verify by VER-008. [REQ-008]

## Production and Verification Method — Praxeology

The definition and the questions come first, from the accepted basis. The owner's choices of operation, autonomy and environment and SWBPIPE's answers are obtained through the human before the dependent definition is closed or anything is run. The workflow is authored and reviewed through the App's own workflow-making. The round trip is run when its contributions exist. No round-trip case joins a SWBPIPE candidate live while the owner holds SWBPIPE joins; only the owner releases that hold, by resuming SWBPIPE UI-SUCCESSOR work. Catalog receiving is an offline check of files SWBPIPE delivered against the revision the App adopted.

- **VER-001** — Inspect the definition against the seven scope items and trace each user activity and the complete activity to an output, an owner and a check. Compare the operation, autonomy and environment named with the owner's recorded choices.
- **VER-002** — Examine the workflow and its transfer contract against PRD V4-WF-01…06 and the App's receiving interface: identity, reviewed original bytes, declarations and revision history on both sides, and the treatment of missing tools and checkpoints.
- **VER-003** — Run and inspect the round trip on the identified candidates, following the workflow to the host and back. Compare selected, supplied and adopted bases with the behaviour observed, and examine interruption and history.
- **VER-004** — Within the round trip, inspect the tool cases, the checkpoint under direct autonomy, the record of a real performed act against the act observed, the fabrication negatives, and the standing of the act after the content changes.
- **VER-005** — Trace each contribution from question to its present standing and compare the standing claimed with the evidence held. Run the catalog receiving checks over SWBPIPE's delivered files.
- **VER-006** — Review the staged account against PRD §2.3, §3.1 and §8 and CLM-006, tracing each dependent connected step to its actual inputs.
- **VER-007** — Audit the case records against EXAMINATION §§1–2: identity, invented material, provenance and route, outcome and remaining gaps. A claim of completion fails if it rests on inspection, a handoff, a historical pass or a not-run record.
- **VER-008** — Review each act named in REQ-008 against its owner, and each output for a transferred act, a fabricated acceptance or an undecided policy treated as decided.

## Governing Values and Decisions — Axiology

- **AX-002** — Meaning is kept reliable across the boundary between applications. Resolution, supply, adoption and behaviour are separate facts, and so are execution and human acts. Better means more of a workflow's declared meaning observed to behave the same in both applications; never by reporting compatibility from a file or a registration.
- **AX-003** — One owner is accountable for the complete first activity while SWBPIPE and the separate examinations keep their own. Independent work proceeds, and a missing dependent contribution is stated. Common meaning does not require common construction.
- **AX-006** — Records expose evidence and limits. Better means more contributions at a later standing with the evidence that standing requires; never by raising a standing on an intention, a relayed file or a prepared handoff.
- **TBD-001** — The operation, the autonomy permitted, the candidate environment and the externally supplied interfaces of the first activity are undecided (owner, through the SWBPIPE session, with the App owner). OUT-001 and OUT-002 cannot be closed, and no round-trip case can be run, before they are chosen. Additions to the reserved acts or to routine-permission treatment for that operation are decided with it.
- **TBD-003** — Whether SWBPIPE will provide a place to receive an App workflow, and a host act facility that returns a reference to its capture evidence, is its owner's decision. Until both exist, the round-trip cases that need them are blocked.

## Output and Evaluation Matrix

| Output | Objective refs | Requirement/claim refs | Acceptance refs | Verification refs | Evidence expectation |
|---|---|---|---|---|---|
| OUT-001 | OBJ-001; OBJ-004; OBJ-008 | CLM-001; CLM-002; REQ-001 | AC-001 | VER-001 | The definition compared with the accepted decomposition's DEL-09-06 row and its seven scope items, and the operation, autonomy and environment it names compared with the owner's choice as relayed from the SWBPIPE session; a choice not yet made can only be shown as unchosen. |
| OUT-002 | OBJ-004; OBJ-008 | CLM-003; REQ-002 | AC-002 | VER-002 | The workflow and its transfer contract examined against PRD V4-WF-01…06 and the App's receiving interface; the reviewed bytes on each side compared directly. |
| OUT-003 | OBJ-004; OBJ-008 | REQ-002; REQ-003; REQ-007 | AC-003 | VER-003 | Outside source: what SWBPIPE, a product this project does not build, adopted and did, reported in its own records and receipts. EXAMINATION V4-EXM-14 states the round trip. |
| OUT-003 | OBJ-004; OBJ-008 | CLM-005; REQ-003; REQ-004 | AC-004 | VER-004 | Outside source: the act the examiner watched the person perform and the host's own receipt. PRD V4-WF-04/05 and V4-AUT-03 state what must and must not be recorded. |
| OUT-004 | OBJ-004; OBJ-008 | CLM-004; REQ-005 | AC-005 | VER-005 | Outside source: SWBPIPE's relayed answers and delivered files at its own revision. The catalog receiving checks also compare the delivered files with the App's own projection of them; that comparison guards only against change. |
| OUT-001 | OBJ-001; OBJ-004; OBJ-008 | CLM-006; REQ-006 | AC-006 | VER-006 | The staged account reviewed against PRD §2.3, §3.1 and §8 on staging and on what the first activity requires, with each dependent step traced to the inputs that actually exist. |
| OUT-003 | OBJ-004; OBJ-008 | REQ-007 | AC-007 | VER-007 | The case records audited by an independent reviewer against EXAMINATION §§1–2 and the candidates' identification records. |
| OUT-001 | OBJ-001; OBJ-004; OBJ-008 | CLM-002; CLM-003; CLM-004; CLM-005; CLM-006; REQ-008 | AC-008 | VER-008 | Each act the definition and the account exclude compared with its owner in CLM-003 to CLM-006 and in the accepted decomposition's rows for those deliverables and DEP-001. |
