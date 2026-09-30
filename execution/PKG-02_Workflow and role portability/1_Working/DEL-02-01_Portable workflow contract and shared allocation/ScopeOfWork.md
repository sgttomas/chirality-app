---
schema: chirality-deliverable-sow/v1
deliverable_id: DEL-02-01
package_id: PKG-02
decomposition_basis: projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z@941c4d35f994594ce8aacd81758ab39079bddad6
project_scope_refs: [SOW-021, SOW-022, SOW-037, SOW-038, SOW-039, SOW-042, SOW-043, SOW-044, SOW-045, SOW-145, SOW-146, SOW-147]
package_objective_refs: [OBJ-003, OBJ-004, OBJ-005]
---

# DEL-02-01 — Portable workflow contract and shared allocation

## Purpose and Objective Traceability

Define the portable workflow declaration and four-role receiving semantics used
by the Chirality App and host applications. Allocate shared types and components
against concrete consumer responsibilities while retaining undecided placement.
This is the API_CONTRACT contribution of PKG-02, owned by the App/shared
workflow-contract owner; affected consumer owners confirm their receiving
responsibilities.

The local contribution to OBJ-003 is a readable, source-compatible contract for
workflow declarations and roles. The contribution to OBJ-004 is accountable
shared-contract allocation at the catalog and host receiving interfaces. The
contribution to OBJ-005 is compatible checkpoint and human-act meaning, with
actual record-field ownership in PKG-04. This deliverable does not claim the
complete workflow-making experience, host implementation or joined qualification
required by those project objectives.

Source keys below resolve to repository-relative files, not supplier APIs:

- **Accepted decomposition:** `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/`; `DECISION.md` supplies the actual acceptance, and `canonical/Deliverables.csv` (DEL-02-01), `Packages.csv` (PKG-02), `Objectives.csv`, `ScopeLedger.csv`, `Open_Issues.csv` and `External_Dependencies.csv` supply the accepted assignments. Historical draft labels within frozen rows do not reverse that decision.
- **PRD:** `projects/chirality-app-v4/execution/_Coordination/Acceptances/APP-V4-BASIS-20260926/original-seed/PRD.md`.
- **Architecture:** `projects/chirality-app-v4/execution/_Coordination/Acceptances/APP-V4-BASIS-20260926/original-seed/ARCHITECTURE.md`.
- **Host integration:** `projects/chirality-app-v4/execution/_Coordination/Acceptances/APP-V4-BASIS-20260926/original-seed/HOST_INTEGRATION.md`.
- **Accepted decision brief:** `projects/chirality-app-v4/execution/_Coordination/Acceptances/APP-V4-BASIS-20260926/DECISION_BRIEF.html`, especially HTML-D02 (`#d2`) and HTML-D03 (`#d3`).
- **Clarification:** `projects/chirality-app-v4/execution/_Coordination/Changes/APP-V4-CLARIFICATION-20260927/DIRECTION.md`.
- **Setup authority:** `projects/chirality-app-v4/execution/_Coordination/_COORDINATION.md`; authoring uses INIT with NO_STATUS_TOUCH. A valid contract and independent check permit a separately recorded manager lifecycle act; they do not establish product completion, input availability or acceptance of a future graph.

| Accepted scope | Local contribution and source | Output |
|---|---|---|
| SOW-021 | Four roles receive through one host agent seat and the selected workflow; PRD V4-HOST-05. | OUT-001 |
| SOW-022 | Hosts retain their own workflows, skills and tools; PRD V4-HOST-06. | OUT-001 |
| SOW-037 | Compatible workflow/role/checkpoint meanings receive human-act recording semantics from PKG-04; PRD V4-SHR-01. | OUT-001, OUT-003 |
| SOW-038 | Open readable WORKFLOW.md, SKILL.md and AGENTS.md guidance; PRD V4-SHR-02 and Architecture §1 M-3. | OUT-001, OUT-002 |
| SOW-039 | Open tool schemas received through the PKG-03 capability contract; Architecture §1 M-3. | OUT-002 |
| SOW-042 | Prose method with declared expected inputs; PRD V4-WF-01. | OUT-002 |
| SOW-043 | Declared required host tools; PRD V4-WF-01. | OUT-002 |
| SOW-044 | Declared checkpoints requiring human acts; PRD V4-WF-01. | OUT-001, OUT-002 |
| SOW-045 | Declared returned outputs and evidence; PRD V4-WF-01. | OUT-002 |
| SOW-145 | Compatible workflow/checkpoint and role contracts, with record/catalog interfaces and justified reusable TypeScript types/components; Architecture V4-ARC-20 as qualified by HTML-D02. | OUT-003 |
| SOW-146 | Concrete repeated responsibility and maintenance needs justify shared execution; HTML-D02. | OUT-003 |
| SOW-147 | Allocation work is included; placement remains OI-014 until the responsible owners settle it; HTML-D02 and Clarification. | OUT-003 |

OUT-004 verifies these local contributions; its tests implement the accepted
meaning rather than creating additional scope.

## Deliverable Definition — Ontology

- **CLM-001** — The accepted DEL-02-01 row names an API_CONTRACT, the App/shared workflow-contract owner, confirmation by affected consumer owners, and four anticipated artifact classes: a workflow/role/checkpoint document, open declared-part schemas/examples, a shared responsibility map, and parser/consumer fixtures. Its ContextEnvelope M and PhaseHint are definition-planning context, not execution limits or readiness evidence. Source: Accepted decomposition, Deliverables.csv DEL-02-01 and Packages.csv PKG-02.
- **CLM-002** — Within the App v4 project, `DEL-03-01` owns capability-catalog/read-basis semantics and supplies required-tool capability descriptors; `DEL-04-01` defines and carries adopted operation policy and human-act distinctions, including the first-increment OI-001/OI-002 rulings (`APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2/D3); operation-specific additions remain with the owner via the outside SWB session (OI-021); `DEL-03-02` owns proposal/outcome semantics, including item dispositions, item-left events and the governing checkpoint constraint (governance phase); `DEL-01-01` supplies the harness capability inventory and supplied-guidance identity evidence; `DEL-03-03` receives the declared checkpoint constraints, for carriage on the external channel in the governance phase; `DEL-04-03` owns human-act/run record fields and App record handling; `DEL-05-01` owns minimal-loop receiving requirements and `DEL-05-02` owns host-panel receiving requirements. `DEL-02-02` owns App workflow authoring/review/registration experience, `DEL-02-03` owns workflow execution compatibility and transfer behavior, and `DEL-02-04` owns App role selection and additive supply. These are receiving interfaces, not transferred implementation assignments. Checkpoint subject binding and item-level decisions consume `DEL-03-02`'s change-item content identities, per-item dispositions, all-items-decided indication, item-left events and applied-outcome object identities; this contract does not define them. Source: Accepted decomposition, Deliverables.csv corresponding rows, Packages.csv PKG-02 through PKG-05 and Open_Issues.csv OI-001/OI-002.
- **CLM-003** — The external SWBPIPE implementation owner retains host-specific catalog, domain validation/application, receipts, loop, panel, tables and views. A host offers, records and presents human acts; the person performs their actual checking, proposal acceptance, approval or professional-reliance act. An accountable professional retains professional assertions. Source: Accepted decomposition DEP-001 and PKG-03/PKG-05 exclusions; Host integration §1 and V4-HI-30 through V4-HI-33; PRD V4-AUT-03/05 and V4-REC-05, qualified by HTML-D03 and the first-increment OI-001/OI-002 rulings in `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2/D3.
- **CLM-004** — Common meaning does not mandate a common executable service, repository location or shared implementation. HTML-D02 qualifies Architecture V4-ARC-20; OI-014 retains placement for App/shared contract owners, and OI-013 retains per-host loop placement/persistence for the shared contract owner with the SWB implementation owner. The Clarification keeps required definition/receiving work IN without deciding those means.
- **CLM-005** — App and host expressions use the same four roles: HELP_HUMAN for alignment, HELPS_HUMANS for design, WORKING_ITEMS for managed execution and TASK for bounded execution. Host presentation recedes behind one agent seat and the selected workflow. Workflow source identity distinguishes project, user, bundled and host-supplied origins; a same-named discovery cannot silently replace a selection. Source: PRD V4-HOST-05/06, V4-SHR-01/02, V4-WF-03 and V4-ROLE-01 through V4-ROLE-03; Accepted decomposition PKG-02 inclusion and DEL-02-01 interfaces. This is the contract receiving contribution to behavior implemented by the sibling owners in CLM-002.

- **OUT-001** — Portable workflow/role/checkpoint contract documenting common meanings, host-specific guidance, open readable sources, source identity and human-act receiving boundaries. Scope: SOW-021, SOW-022, SOW-037, SOW-038, SOW-044. Objectives: OBJ-003, OBJ-005. Basis: PRD V4-HOST-05/06, V4-SHR-01/02 and V4-WF-01; CLM-001, CLM-002, CLM-003, CLM-005.
- **OUT-002** — Open declared-part schemas and explanatory examples expressing expected inputs, required host tools, checkpoints requiring human acts, returned outputs and evidence alongside prose method guidance. The contract consumes open tool descriptors from the capability-catalog owner without inventing that owner's wire fields. Scope: SOW-038, SOW-039, SOW-042, SOW-043, SOW-044, SOW-045. Objective: OBJ-003. Basis: PRD V4-WF-01 and V4-SHR-02; Architecture §1 M-3; CLM-001, CLM-002.
- **OUT-003** — Shared contract/component responsibility map identifying each concrete consuming owner, repeated responsibility, maintenance rationale, candidate reusable TypeScript types/interface components, receiving contribution, ownership confirmation and decided or unresolved placement. Record and catalog semantics stay with their owners. Scope: SOW-037, SOW-145, SOW-146, SOW-147. Objectives: OBJ-003, OBJ-004, OBJ-005. Basis: Architecture V4-ARC-20 qualified by HTML-D02, OI-014 and Clarification; CLM-001 through CLM-004.
- **OUT-004** — Parser and consumer contract fixtures, with results bound to the actual contract/examples and identified consumers, demonstrating readable declarations and compatible role/checkpoint/source meaning at the local interfaces. Include negative or absent evidence cases where needed to expose unsupported claims. Scope: SOW-021, SOW-022, SOW-037, SOW-038, SOW-039, SOW-042, SOW-043, SOW-044, SOW-045, SOW-145, SOW-146, SOW-147. Objectives: OBJ-003, OBJ-004, OBJ-005. Basis: Accepted decomposition DEL-02-01 anticipated TEST artifact and verification statement; the source commitments mapped above.

## Completion and Reliance Basis — Epistemology

These are prospective completion criteria for the deliverable's products.
Initializing this ScopeOfWork defines them; it does not claim that schemas,
fixtures, a reusable component or receiving consumer already exists or passes.

- **REQ-001** — The portable contract shall retain the four meanings and host-specific guidance in CLM-005 while representing the host's single agent seat and selected workflow. WORKFLOW.md, SKILL.md and AGENTS.md remain open, readable guidance. Actual source origin and selected identity remain explicit when names collide; portability does not impose the App's role-selection UI on hosts or every manual practice. Source: PRD V4-HOST-05/06, V4-SHR-01/02 and V4-WF-03; Accepted decomposition PKG-02 and CLM-005.
- **REQ-002** — The declared part shall distinguish expected inputs, required host tools, checkpoints requiring human acts, returned outputs and returned evidence, with prose method guidance retained. Host-operation requirements shall refer to the capability meaning supplied by `DEL-03-01`; harness-capability requirements shall refer to capability meaning supplied through `DEL-01-01` (CLM-002). Tool schemas shall remain open. Examples shall expose these meanings without selecting unaccepted wire fields or supplier versions. Source: PRD V4-WF-01, Architecture §1 M-3 and Accepted decomposition DEL-02-01.
- **REQ-003** — Checkpoint declarations shall express the required human act without treating execution success, proposal acceptance, checking, approval and professional reliance as interchangeable. Each act retains its actor, subject and supporting evidence through the PKG-04 receiving contract; evidence for one act alone establishes none of the others. A required checkpoint's act is recorded as done only when the person actually performs it (holding the run until then is the governance-phase definition, TBD-004), but there is no synthetic rule requiring proposal acceptance before any other independently evidenced act. Host offering/recording/presentation does not make the host the person performing that act. Source: PRD V4-WF-01/05, V4-AUT-01/03/05 and V4-REC-05; Host integration V4-HI-31/33/42; HTML-D03; CLM-002, CLM-003.
- **REQ-004** — The contract shall preserve source-compatible declaration meaning for App and host consumers, including actual origins and revisions through the receiving interface, while making the returned output/evidence expectations distinguishable from observed production and human acts. Tests shall expose an unsupported success-to-act inference as incompatible; absent evidence remains absent. Source: Accepted decomposition DEL-02-01 verification, PRD V4-WF-01/03/06 and V4-EXE-03; CLM-002, CLM-005.
- **REQ-005** — Shared allocation shall name actual consumers, their repeated responsibilities and maintenance needs before justifying reusable types/components or shared execution. Workflow/checkpoint, role, record and catalog contract parts shall retain their semantic owners and explicit receiving responsibilities. Placement and any common implementation remain open where OI-014 or OI-013 is unresolved; documenting that open choice does not omit the included allocation result. Source: SOW-145, SOW-146, SOW-147; Architecture V4-ARC-20 as qualified by HTML-D02 and Clarification; CLM-002, CLM-004.
- **REQ-006** — This deliverable shall perform no act owned by another deliverable: catalog-semantic definition by `DEL-03-01`, proposal/outcome definition by `DEL-03-02`, external-channel constraint carriage by `DEL-03-03`, operation-policy contract definition and carrying adopted policy by `DEL-04-01`, human-act/run-field definition and record implementation by `DEL-04-03`, loop receiving design by `DEL-05-01`, panel receiving design by `DEL-05-02`, App workflow workspace/registration construction by `DEL-02-02`, execution/transfer implementation by `DEL-02-03`, and role selection/supply implementation by `DEL-02-04` remain with the owners named in CLM-002. Its responsibility map records and receives these contributions. Host catalog/domain/receipt/loop/panel construction remains with the external SWBPIPE implementation owner in CLM-003; actual human checking, acceptance, approval and professional reliance remain with the person, with professional assertions retained by the accountable professional in CLM-003. Shared placement decisions remain with the App/shared contract owners in CLM-004. Source: Accepted decomposition Deliverables.csv, Packages.csv, DEP-001, OI-014 and OI-013; HTML-D02/03.

- **AC-001** — OUT-001 describes the four role meanings, host single-seat treatment and host-owned workflows/skills/tools without erasing their source identities or making App UI a portability requirement; its guidance stays readable in the named open files. Verify by VER-001.
- **AC-002** — OUT-002 schemas and examples unambiguously express each V4-WF-01 declaration category with its prose method, keep tool schemas open, and identify the capability descriptor supplier without guessing its wire definition. Verify by VER-002.
- **AC-003** — OUT-001 and OUT-002 checkpoint examples distinguish execution, proposal acceptance, checking, approval and professional reliance; each claimed act has its own actor/subject/evidence, a required act cannot be inferred from success, and no universal acceptance-first dependency is imposed. Verify by VER-003.
- **AC-004** — OUT-001 and OUT-002 retain selected origin/revision and declared meanings across App/host receiving examples, including same-named origins, and distinguish promised output/evidence from observed production. Verify by VER-004.
- **AC-005** — OUT-003 identifies consuming owners and repeated responsibilities for every proposed shared contract/type/component, explains maintenance consequences, records confirmation or its absence, and preserves OI-014/OI-013 placement choices without presuming a service or transferring host ownership. Verify by VER-005.
- **AC-006** — OUT-003 maps every excluded act in REQ-006 to its named owner and receiving interface; no local contract completion is represented as that owner's implementation, adoption, qualified result or human act. Verify by VER-006.
- **AC-007** — OUT-004 supplies parser and consumer fixtures covering the local portable declaration, role/source, checkpoint and allocation obligations, with candidate identity, actual results and limitations; absent consumer inputs or execution are reported without claiming a joined host witness. Verify by VER-007.

- **TBD-001** — OI-014 remains OPEN: App/shared contract owners choose shared contract/component placement against actual consumers before structural/production contract allocation, and agree ownership before common implementation. OUT-003 is required; its final unresolved placements cannot be claimed settled by this initialization.
- **TBD-002** — OI-013 remains OPEN with the shared contract owner and SWB implementation owner before shared/host implementation boundary contracts. Host loop placement, parsing, persistence and panel assembly are receiving constraints here, not decisions this contract makes. DEP-001 currently records the outside SWB session building before agent-action integration; local definition proceeds, while actual host conformance waits for its relevant inputs.
- **TBD-003** — OI-001 and OI-002 were ruled for the first increment by `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2/D3 (carried by DEL-04-01). Operation-specific reserved additions remain with OI-021. False attribution is already prohibited; this document neither fixes a universal reserved list nor uses those open choices to defer independent definition. OI-018 retains instruction distribution/adoption mechanics with their owning parties; the open guidance requirement does not decide that mechanism.
- **TBD-004** — Declared checkpoints are phased (`APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4` D4-1). In the current phase a declared checkpoint is plan guidance. The declaration still states its required act, when it is reached, its subject and its held actions. The act is recorded only when the person performs it, and no hold support is assigned. Neither the App nor a host's embedded loop holds a run or reports a workflow unsupported because a hold cannot be enforced. Hold support and enforced holds (`DEL-02-03`) are kept as the governance-phase definition, so that every workflow needing governance can be served. App-side run holds (`APP-V4-FIRST-INCREMENT-20260928-DECISION-2` D6) are closed for the current phase. This contract consumes `DEL-02-03`'s statement of the current phase and, for the governance phase, its hold-support values; it does not define them. **Owner:** the owner, when a workflow needs enforced checkpoints. **Point of need:** before any checkpoint is claimed held.

No substantive source conflict is resolved by this contract. The original shared
layer wording is read through its accepted HTML-D02 qualification and the
Clarification. Current relevant OI-001/002/013/014/018 and DEP-001 rows agree with
the frozen basis; unrelated later receiving observations do not amend this
assignment.

## Production and Verification Method — Praxeology

Produce the documentation and declared-part examples from the mapped clauses.
Receive catalog descriptors, record semantics and host consumer needs from the
owners in CLM-002 and CLM-003. Name a missing contribution and its point of need
instead of choosing its definition. Prepare the allocation map against concrete
consumers; retain unresolved placement for the responsible owners. Build parser
and consumer fixtures against the resulting identified contract and examples,
then report results and remaining limits for independent examination.

- **VER-001** — Compare OUT-001 with PRD V4-HOST-05/06, V4-SHR-01/02 and V4-ROLE-01 through V4-ROLE-03 and the accepted local boundary. Inspect App/host reading examples for retained role meaning, host guidance and actual origins without an imposed App UI. Evidence: source-to-contract comparison and identified examples with discrepancies.
- **VER-002** — Inspect the declared-part schema/examples against PRD V4-WF-01 and Architecture M-3; exercise the parser fixtures to recover the declared inputs, tools, checkpoints, outputs and evidence alongside the prose. Compare tool references with the identified PKG-03 descriptor basis and record any missing supplier contribution. Evidence: schema/example identities, parsed results and compatibility findings.
- **VER-003** — Examine checkpoint and record-interface examples against HTML-D03, PRD V4-WF-05/V4-REC-05 and the received PKG-04 distinctions. Exercise separate evidenced acts, success without a human act, an unperformed required checkpoint and an independently evidenced check without prior proposal acceptance. Verify that each case reports only the evidenced act and, for a checkpoint in the governance phase, any actual hold. Evidence: case inputs, expected meanings, observed consumer results and absent-input limitations.
- **VER-004** — Compare App and host consumer readings of the same declaration and source-qualified examples, including same-named workflows from different origins and carried/adapted revisions. Check that meanings, selected origin/revision and promised-versus-observed evidence remain distinguishable. Evidence: source identities, received contract versions, comparison results and unsupported-consumer gaps; no joined round-trip qualification inferred.
- **VER-005** — Review OUT-003 against each named consumer responsibility, Architecture V4-ARC-20 as qualified by HTML-D02, OI-014 and OI-013. Inspect repeated work and maintenance rationale, confirmations and unsettled placement. Evidence: responsibility/allocation comparison with actual owner responses or explicit absence; no confirmation inferred from a document's existence.
- **VER-006** — Check REQ-006 act by act against CLM-002, CLM-003, CLM-004 and their accepted owner rows. Confirm that receiving obligations remain local while the named production, policy, host and human acts stay with their actual owners. Evidence: boundary comparison listing every act, owner, source and any mismatch, including the host-versus-person distinction.
- **VER-007** — Inspect the fixture inventory and actual parser/consumer results against REQ-001 through REQ-006 and the source mapping; verify that the identified contract/examples and declared consumer basis match the tested candidate. Record unexecuted cases, missing host inputs and open allocation limits explicitly. Evidence: candidate-bound fixture results and coverage account; local fixture success does not establish external implementation, release, adoption or professional reliance.

## Governing Values and Decisions — Axiology

- **AX-001** — Retain the accepted priority order of maintainability, functionality, then local models/data privacy. Share implementation only where repeated consumer responsibility and maintenance justify it; no service, supplier selection or fixed repository placement follows from the word shared. Basis: Architecture §1 and V4-ARC-20, HTML-D02, Clarification and CLM-004.
- **AX-002** — Preserve open readable guidance and actual source identity. Receiving compatibility is demonstrated against meaning and real consumers, not inferred from a matching filename. This contract defines portable declarations without creating a reusable workflow package or changing the governing workflow library. Basis: PRD V4-SHR-02, V4-WF-01/03 and HTML-D02.
- **AX-003** — Keep execution, proposal acceptance, checking, approval and professional reliance separately attributable. Their independence prevents success from manufacturing a human act and prevents one act's evidence from suppressing another independently evidenced act. Hosts offer, record and present; people perform their acts. Basis: HTML-D03, PRD V4-AUT-01/03/05, V4-REC-05 and the sealed assignment's pilot clarification.
- **AX-004** — Included outcomes remain required while open means remain open. Initialization is definition-only under the approved setup; lifecycle changes, graph acceptance, implementation, supplier experiments and external adoption require their own authorized work and actual evidence. Basis: Clarification, Accepted decomposition DECISION.md and Setup authority.
- **AX-005** — Revised under scope-change amendment `SCA-V4-001` (accepted snapshot `projects/chirality-app-v4/execution/_ScopeChange/SCA-V4-001_2026-09-28_2155`), applying `APP-V4-FIRST-INCREMENT-20260928-DECISION-1`, `APP-V4-FIRST-INCREMENT-20260928-DECISION-2` (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-FIRST-INCREMENT-20260928/OWNER_DECISIONS.md`) and `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4` (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-SWBPIPE-INTAKE-20260928/OWNER_DECISIONS.md`). Revised: CLM-002, CLM-003, REQ-002, REQ-003, REQ-006, VER-003 and TBD-003. Added: TBD-004 and AX-005. Removed: none.
- **AX-006** — Revised under scope-change amendment `SCA-V4-002` (accepted snapshot `projects/chirality-app-v4/execution/_ScopeChange/SCA-V4-002_2026-09-29_1901`), applying `APP-V4-BASIS-ALIGN-20260928-DECISION-10` (record `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-BASIS-ALIGN-20260928/OWNER_DECISIONS.md`), which routed this contract's statement of the proposal-contract outputs it consumes to this amendment. Revised: CLM-002. Added: AX-006. Removed: none.

## Output and Evaluation Matrix

| Output | Objective refs | Requirement/claim refs | Acceptance refs | Verification refs | Evidence expectation |
|---|---|---|---|---|---|
| OUT-001 | OBJ-003, OBJ-005 | REQ-001, CLM-001, CLM-005 | AC-001 | VER-001 | Source comparison and readable App/host role/guidance examples. |
| OUT-002 | OBJ-003 | REQ-002, CLM-001, CLM-002 | AC-002 | VER-002 | Identified schemas/examples, parser results and catalog descriptor basis or gap. |
| OUT-001 | OBJ-003, OBJ-005 | REQ-003, CLM-002, CLM-003 | AC-003 | VER-003 | Distinct-act/checkpoint cases and actual consumer outcomes or limits. |
| OUT-002 | OBJ-003 | REQ-003, CLM-002, CLM-003 | AC-003 | VER-003 | Declared checkpoint examples use the same distinct-act verification. |
| OUT-001 | OBJ-003, OBJ-005 | REQ-004, CLM-005 | AC-004 | VER-004 | Origin/revision and App/host declaration comparison; no assumed round-trip witness. |
| OUT-002 | OBJ-003 | REQ-004, CLM-005 | AC-004 | VER-004 | Declared-part examples retain the compared origin/revision and meanings. |
| OUT-003 | OBJ-003, OBJ-004, OBJ-005 | REQ-005, CLM-002, CLM-004, TBD-001, TBD-002 | AC-005 | VER-005 | Consumer responsibility and maintenance account, owner responses and open placements. |
| OUT-003 | OBJ-003, OBJ-004, OBJ-005 | REQ-006, CLM-002, CLM-003, CLM-004 | AC-006 | VER-006 | Act-by-act ownership/receiving comparison with cited authority. |
| OUT-004 | OBJ-003, OBJ-004, OBJ-005 | REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, REQ-006, CLM-001 | AC-007 | VER-007 | Candidate-bound fixture inventory/results, coverage, missing inputs and limits. |
