# Chapter 8 — Implementation and Validation

---

## 8.1 Introduction

The preceding chapters of this thesis establish the philosophical commitments (Chapter 3), architectural decisions (Chapter 4), contract framework (Chapter 5), decomposition system (Chapter 6), and professional practice model (Chapter 7) that together define the Chirality project execution system at the specification level. The purpose of this chapter is to demonstrate that these specifications have been realized as working software. The theoretical framework is not an aspirational model; it has been instantiated in a deployable desktop application, a suite of 38 agent instruction files, a registry of 28 deterministic tools, and a governance hierarchy of formal documents that remain in active use on professional projects.

The chapter is organized as follows. Section 8.2 surveys the agent suite quantitatively, covering type distribution, class distribution, write scope distribution, and the orchestration graph that coordinates multi-agent workflows. Section 8.3 describes the deterministic tool layer — the LLM-independent operations that agents invoke during pipeline execution. Section 8.4 describes the desktop application that provides the runtime harness. Section 8.5 presents the validation mechanisms: internal conformance audits, harness SDK validation, and worked project examples. Section 8.6 provides an honest accounting of what is fully implemented versus what remains as specified-but-not-yet-automated future hardening. Section 8.7 summarizes the quantitative evidence for the claim that the architectural commitments are realizable.

Throughout this chapter, references to Appendix A (invariant catalog) and Appendix B (agent inventory) provide the detailed backing for summary claims made in the text.

---

## 8.2 Agent Suite

The Chirality system ships 38 agent instruction files organized according to the Type 0/1/2 hierarchy defined in Chapter 4 (§4.5) and catalogued in full in Appendix B. This section provides a quantitative characterization of that suite.

### 8.2.1 Type Distribution

The suite is distributed across three types as follows:

| Type | Count | Role |
|------|-------|------|
| Type 0 — Canonical Standards | 2 | Constitutional layer; defines invariant protocols |
| Type 1 — Interactive Personas | 14 | Gate-controlled, human-facing orchestrators |
| Type 2 — Bounded Task Agents | 22 | Brief-driven, straight-through specialists |
| **Total** | **38** | |

The Type 0 agents — HELPS_HUMANS and DECOMP_BASE — function as the architectural constitution. HELPS_HUMANS defines the nine workflow design requirements (R1–R9) and the universal structural template that every other agent must conform to. DECOMP_BASE defines the seven-gate decomposition protocol and the ten decomposition invariants (I1–I10) that all decomposition agents inherit. Neither agent writes project state; both exist solely to define the standards against which all downstream agents are validated.

The 14 Type 1 agents are interactive personas. They execute gate-controlled, multi-phase workflows in which humans make consequential decisions at each phase boundary. Type 1 agents may spawn Type 2 specialists and maintain orchestration state, but they may not approve deliverables for reliance or override Type 0 constraints.

The 22 Type 2 agents are brief-driven specialists. They accept structured INIT-TASK briefs, execute straight-through without mid-run gates, and produce auditable outputs consisting of either deliverable-local file writes or immutable snapshots in designated tool roots. Type 2 agents never spawn other agents. Invalid inputs cause a `FAILED_INPUTS` halt; missing data is marked `TBD` and execution continues conservatively.

### 8.2.2 Class and Write Scope Distribution

Agent classification along the AGENT_CLASS dimension divides the suite into PERSONA agents (conversational, gate-controlled interface) and TASK agents (brief-driven, straight-through execution). By design, all Type 1 agents carry AGENT_CLASS: PERSONA and all Type 2 agents carry AGENT_CLASS: TASK. The two Type 0 agents are also classed as PERSONA but carry WRITE_SCOPE: none — they produce standards, not project state.

Write scope distribution across the suite reflects the fault containment architecture described in Chapter 4 (§4.6). The eight declared write scope categories and their agent populations are:

| Write Scope | Agents |
|-------------|--------|
| `none` | HELPS_HUMANS, DECOMP_BASE, HELP_HUMAN |
| `repo-metadata-only` | DOMAIN_DECOMP, CONTEXT_TRANSPOSE |
| `project-level` | PROJECT_DECOMP, SOFTWARE_DECOMP, SCOPE_CHANGE, PREPARATION, ESTIMATE_PREP |
| `deliverable-local` | WORKING_ITEMS, 4_DOCUMENTS, DOMAIN_DOCUMENTS, CHIRALITY_FRAMEWORK, CHIRALITY_LENS, DEPENDENCIES, TASK, REVIEW |
| `tool-root-only` | ORCHESTRATOR, RECONCILIATION, CHANGE, SCHEDULING, ESTIMATING, AGGREGATION, AUDIT_AGENTS, AUDIT_DECOMP, AUDIT_DEP_CLOSURE, DOMAIN_HYPERGRAPH, AUDIT_HYPERGRAPH_CLOSURE |
| `workspace-scaffold-only` | PREPARATION (primary scaffold variant) |
| `knowledge-type-local` | DOMAIN_DOCUMENTS (knowledge artifact variant) |

This distribution reflects the system's core invariant K-WRITE-1 (Appendix A): every agent's write zone is declared in its header block, and no agent may write outside that declared zone. The separation between source truth (deliverable-local agents) and derived outputs (tool-root agents) creates the fault containment boundary discussed in Chapter 4 (§4.6.2): a failing Type 2 tool-root agent cannot corrupt source truth because its write scope physically excludes deliverable folders.

### 8.2.3 The 3×4 Agent Matrix

The 38 agents are organized within a 3×4 matrix that maps epistemic posture (rows) to functional role (columns):

|  | **Guiding** | **Applying** | **Judging** | **Reviewing** |
|:---|:---|:---|:---|:---|
| **Normative** | HELP | ORCHESTRATE | WORKING_ITEMS | AGGREGATE |
| **Operative** | DECOMP\* | PREP\* | TASK\* | AUDIT\* |
| **Evaluative** | AGENTS | DEPENDENCIES | CHANGE | RECONCILING |

The matrix serves a dual purpose. Architecturally, it ensures that every agent has a clear position within the system's epistemic and functional coordinate space, preventing role ambiguity as the suite grows. Operationally, it drives the desktop application's navigation routing: NORMATIVE and EVALUATIVE rows open interactive WORKBENCH sessions; the OPERATIVE row opens PIPELINE sessions with category selectors for the four pipeline taxonomies (DECOMP\*, PREP\*, TASK\*, AUDIT\*). The full per-agent classification with write scope, blocking policy, and primary outputs is provided in Appendix B.

---

### 8.2.4 Decomposition System

The decomposition system comprises three conforming variant agents — PROJECT_DECOMP, SOFTWARE_DECOMP, and DOMAIN_DECOMP — each inheriting from the DECOMP_BASE Type 0 standard. The conformance relationship is formally specified in DBM_Agent_Instruction_Architecture.md §8.5 (the Extension Contract) and operationalized in the seven-gate protocol:

| Gate | Name | Gate Question |
|------|------|---------------|
| 1 | Intake | "Does this reflect the source material and context as intended?" |
| 2 | Normalize | "Are the atomic units, classifications, and vocabulary correct?" |
| 3 | Objectives | "Do these objectives represent success as intended?" |
| 4 | Partitions | "Are partitions correct? Does each in-scope unit belong to exactly one?" |
| 5 | Production Units | "Are production units (granularity, types, responsibilities) acceptable?" |
| 6 | Coverage | "Are coverage, mappings, and open issues acceptable?" |
| 7 | Publish | "Is this the accepted basis for downstream work?" |

All three variants share this protocol verbatim. Domain-specific differentiation is provided through an Extension Contract that each variant must satisfy: entity binding tables (mapping abstract DECOMP_BASE terms to domain-specific equivalents), ID format specifications, production unit type taxonomies, and domain-specific telemetry extensions. The three variants differ along the following dimensions (see Chapter 6 for detailed treatment):

- **PROJECT_DECOMP** targets EPC and design-build work. Atomic units are scope items (SOW-####); production units are deliverables (DEL-XXX-YY). The worked examples in `examples/execution-6a` through `examples/execution-6c` are all PROJECT_DECOMP instances.
- **SOFTWARE_DECOMP** targets software development. It introduces Context Envelope sizing (S/M/L/XL) as a mandatory telemetry extension, constraining the volume of context passed to each Type 2 agent run.
- **DOMAIN_DECOMP** targets handbook and knowledge domain work. Atomic units are handbook units (HBK-####); production units are knowledge types (KTY-CC-TT). Domain decompositions do not produce dependency graphs; they produce hypergraph representations via the DOMAIN_HYPERGRAPH agent.

The three-variant design satisfies the decomposition system's principal engineering requirement: a single, auditable, gate-controlled protocol that scales across fundamentally different work domains without requiring domain-specific variants of the downstream agent suite.

---

### 8.2.5 Orchestration Architecture

The spawning graph defines which Type 1 agents may invoke which Type 2 agents and under what conditions. The graph is reproduced from DBM_Agent_Instruction_Architecture.md §6.1:

```
ORCHESTRATOR (Type 1) ──spawns──┬── PREPARATION
                                ├── 4_DOCUMENTS
                                ├── DOMAIN_DOCUMENTS
                                ├── CHIRALITY_FRAMEWORK
                                ├── CHIRALITY_LENS
                                ├── DOMAIN_HYPERGRAPH [DOMAIN variant only]
                                ├── ESTIMATING
                                └── AGGREGATION

WORKING_ITEMS (Type 1) ──spawns──── TASK

RECONCILIATION (Type 1) ──spawns──┬── AUDIT_DEP_CLOSURE
                                  ├── AUDIT_AGENTS
                                  ├── AUDIT_DECOMP
                                  └── AUDIT_HYPERGRAPH_CLOSURE [DOMAIN variant only]
```

HELP_HUMAN, CHANGE, REVIEW, SCOPE_CHANGE, CONTEXT_TRANSPOSE, SCHEDULING, and EVALUATION are all Type 1 agents that operate as leaves or as handoff coordinators rather than primary spawners. CHANGE, in particular, requires explicit approval tokens before any state-changing action, providing the highest-control gate in the system.

Session continuity across agent invocations is maintained through two durable filesystem artifacts: `NEXT_INSTANCE_PROMPT.md` (stable session startup instructions, modified only on protocol changes) and `NEXT_INSTANCE_STATE.md` (mutable state pointer, updated by WORKING_ITEMS at each session handoff). This control loop — described in Chapter 4 (§4.8) — enables multi-session project execution without hidden state.

Four distinct spawning mechanisms govern how Type 1 agents invoke Type 2 agents. ORCHESTRATOR uses human-gated phases, pausing between each sequential spawning decision. WORKING_ITEMS uses pre-authorized dispatch, autonomously invoking TASK agents after the human confirms the session objective. RECONCILIATION uses a human-directed toolbelt: the human specifies which agents are authorized before any dispatch occurs, and at most one task agent runs per cycle by default. CHANGE uses approval-gate execution, requiring explicit `APPROVE:` tokens that enumerate specific actions before any filesystem or git change proceeds.

---

### 8.2.6 Evaluation Subsystem

The EVALUATION agent (Type 1) provides a structured project evaluation capability introduced in the most recent development cycle. EVALUATION is an orchestrator: it dispatches four Type 2 subagents across an execution root and synthesizes their findings into a scored assessment.

| Subagent | Function |
|----------|----------|
| CONTENT_DIGEST | Per-deliverable structured content digest; provides input for evaluation scoring |
| EVALUATION_REPORT | Scored dimension evaluation against rubric criteria |
| EVALUATION_STRUCTURE_AUDIT | Structural validation (folder layout, minimum viable fileset, naming conventions) |
| EVALUATION_DEPENDENCY_AUDIT | Dependency validation (schema compliance, anchor presence, evidence coverage) |

The evaluation subsystem operates against a dedicated `_Evaluation/` tool root within the execution root. The `examples/AB-2026-01424-WDMLRL-2026-Claude/` example project contains a fully executed evaluation run, including content digests, evaluation reports, and an `EVALUATION_PROTOCOL.md` that documents the protocol applied.

---

## 8.3 Deterministic Tools

The `tools/` directory contains 28 deterministic tools — shell scripts and Python utilities — that agents invoke during pipeline execution. These tools are indexed in `tools/REGISTRY.md` and maintained by the TOOLMAKER agent (Type 1, AGENT_TOOLMAKER.md).

### 8.3.1 Category Distribution

| Category | Count | Representative Operations |
|----------|-------|--------------------------|
| Scaffolding | 6 | Package/deliverable folder creation; status file writes; snapshot folder creation |
| Query | 2 | Workspace state counts; scope change ID scanning |
| Validation | 5 | Enum value checking; ID format validation; Dependencies.csv schema validation; fileset checks |
| Reporting | 6 | CSV merge with provenance; INDEX.md generation; WBS/CBS summarization; coverage matrices |
| Coordination | 1 | Full dependency graph analysis (SCC, orphans, hubs, bidirectional pairs) |
| Evaluation | 8 | Digest coverage verification; lifecycle state extraction; dependency schema checks; agent output extraction |
| **Total** | **28** | |

The validation category is architecturally significant. `validate_enum.py` checks a value against 24 named enumeration sets defined in TYPES.md, enforcing schema discipline across all agent writes. `validate_dependencies_schema.py` validates a Dependencies.csv file against the v3.1 schema — all 29 required columns — providing deterministic schema compliance checking without requiring LLM reasoning. `check_min_viable_fileset.sh` verifies the five required metadata files are present in a deliverable folder. These three tools together instantiate a substantial portion of the validation criteria defined in SPEC.md §12.

The coordination category contains a single but structurally important tool: `analyze_dep_closure.py`. This tool performs a complete dependency graph analysis across an execution root, detecting strongly connected components (cycles), identifying orphan deliverables (nodes with no dependency edges), performing hub analysis, and checking bidirectional pair symmetry. It produces a `closure_summary.json` and six CSV reports. This tool is invoked by the AUDIT_DEP_CLOSURE agent and supports the RECONCILIATION orchestration workflow.

### 8.3.2 The LLM Boundary

The tool registry makes explicit a design principle stated in Chapter 4 (§4.3): the system separates operations that require language model reasoning from operations that do not. The 28 tools handle the mechanical side — filesystem traversal, schema validation, CSV aggregation, dependency graph construction, lifecycle state extraction. Agents handle content reasoning — interpreting source documents, extracting semantic dependencies, drafting document kits, synthesizing findings.

This boundary is consequential for reliability and auditability. Deterministic tool outputs are reproducible: given identical inputs, the same tool will produce the same output. LLM reasoning is not reproducible in this sense. By pushing all reproducible operations into deterministic tools, the architecture concentrates non-determinism in the places where it is unavoidable (content judgment) and eliminates it from the places where it is unacceptable (schema validation, scaffolding, graph analysis).

As of the current implementation, 21 of the 38 agent instruction files reference tools from the registry in their PROTOCOL sections. The remaining 17 either operate entirely through LLM reasoning (content-producing agents such as WORKING_ITEMS, 4_DOCUMENTS, and CHIRALITY_FRAMEWORK) or reference tools indirectly through RECONCILIATION orchestration.

### 8.3.3 Backlog

The REGISTRY.md maintains an explicit backlog of six tools identified as useful but deferred. Deferral criteria are formally stated: a backlog tool is promoted when either a second agent needs the same operation, or an existing agent's inline implementation diverges across runs and requires standardization. This discipline prevents premature abstraction while providing a traceable record of known gaps. [TODO: verify backlog promotion criteria are being applied consistently as new agents are added]

---

## 8.4 Desktop Application

The `frontend/` directory contains a Next.js and Electron desktop application that provides the runtime harness for all agent interactions. This application packages the agent operating system (instruction files, governance documents) and exposes them through a structured user interface while keeping the working root (the user's project directory) fully under user control.

### 8.4.1 Architecture

The application is built on a Next.js frontend rendered inside an Electron shell, enabling deployment as a native desktop application for both macOS (`.dmg`) and Windows (`.exe`). The core session management layer is exposed through two API routes: a session management endpoint (`/api/harness/session/*`) and a turn execution endpoint (`/api/harness/turn`). The session and turn API uses Server-Sent Events (SSE) for streaming — agent responses are surfaced progressively rather than buffered to completion.

The instruction root / working root separation is enforced at the application level. The instruction root (the agent operating system: all `AGENT_*.md` files, governance documents, and the INIT.md bootstrap context) is bundled with the application and release-managed. The working root is a user-selected filesystem path where agents read and write project state. An agent operating on a project never modifies the instruction root; conversely, updating the agent operating system requires a new application release, not a filesystem edit in the working root. This separation is the technical realization of the architectural commitment described in Chapter 4 (§4.2): the agent OS is stable and auditable; the project workspace is mutable and user-controlled.

### 8.4.2 Matrix-Based Navigation

Navigation is organized around the 3×4 agent matrix. The PORTAL view displays the full matrix; operators select a cell to initiate a session. Routing is deterministic: cells in the NORMATIVE and EVALUATIVE rows open a WORKBENCH view (interactive persona sessions); cells in the OPERATIVE row open a PIPELINE view (task execution with category selectors).

The PIPELINE view exposes four category selectors corresponding to the OPERATIVE row's matrix columns: DECOMP\*, PREP\*, TASK\*, and AUDIT\*. Within each category, an agent selector lists the available agents; within TASK\*, a scope selector presents deliverables dynamically scanned from the working root, allowing the operator to target a specific deliverable for a TASK agent run. Portal-to-Pipeline navigation is supported: clicking a deliverable row in the PORTAL routes directly to the PIPELINE TASK\* view with that deliverable pre-selected.

### 8.4.3 Multimodal Input

Turn input supports multimodal content through a server-resolved file attachment pipeline. Operators may attach images, documents, or text files to a turn; the attachment resolver (`attachment-resolver.ts`) reads the files server-side, classifies them by type, enforces budget constraints on total attached content, and handles partial failure gracefully (a failed attachment does not abort the turn). The `FilePicker.tsx` component provides a self-contained file picker modal with multi-select, extension filtering, and directory navigation.

### 8.4.4 Operator Toolkit

An Operator Toolkit panel provides per-turn harness options, with local presets persisted across sessions. Toolkit visibility is controlled through application configuration ("Show Tool Kit sidebar") and stored in local storage. The panel is designed for operators who need to configure agent behavior — context depth, tool authorizations, or execution constraints — on a per-turn basis without modifying instruction files.

---

## 8.5 Validation

Validation in the Chirality system operates across four distinct layers: agent instruction conformance checking, decomposition and dependency graph auditing, harness SDK runtime validation, and worked project examples. These layers are complementary: each addresses a different class of potential failure.

### 8.5.1 Internal Validation Mechanisms

**AUDIT_AGENTS** (Type 2) performs conformance checking of agent instruction files against the AGENT_HELPS_HUMANS.md standard. Given a list of agent files, a canonical file, and a rubric, it produces an audit report, an issue log, and a patch plan. This mechanism enforces the structural template mandated by the Type 0 standard at the text level: header block completeness, section boundary markers, non-negotiable invariant declarations, and WRITE_SCOPE declarations. AUDIT_AGENTS writes to `_Reconciliation/AgentAudit/` as an immutable snapshot, providing a durable record of conformance state at any point in the development cycle.

**AUDIT_DECOMP** (Type 2) verifies decomposition coverage: that every in-scope atomic unit identified in the decomposition ledger has been assigned to a partition and production unit, that ledger columns meet the minimum specification, and that the Coverage and Telemetry section is present and populated. It produces a coverage report, an issue log CSV, a coverage matrix, and a `coverage_summary.json`. AUDIT_DECOMP is also triggered as a precondition check by the REVIEW agent before lifecycle transitions are permitted, creating a hard gate: a decomposition that fails coverage audit cannot advance through the formal 5-gate review.

**AUDIT_DEP_CLOSURE** (Type 2) performs dependency graph analysis using the `analyze_dep_closure.py` tool. The analysis covers: schema validation of all Dependencies.csv files in scope, identification of orphan deliverables (no dependency edges, either incoming or outgoing), strongly connected component detection (cycles in the dependency DAG, which violate the expected acyclic structure), hub identification (nodes with unusually high edge degree), and bidirectional pair symmetry checking. Results are written to `_Reconciliation/DepClosure/` as an immutable snapshot. This agent directly enforces K-DEP-1 (deliverable-local dependency registers are authoritative) and contributes to K-DEP-2 (dependency references must resolve to existing deliverable IDs) by surfacing unresolvable targets.

**Folder Structure Validation Checklist.** SPEC.md §12 defines a formal validation checklist for execution roots, package folders, and deliverable folders. A valid execution root must contain at least one `PKG-XX_{Label}/` folder, a `_Decomposition/` folder with at least one decomposition document, and an `INIT.md` file. A valid deliverable folder must contain `_STATUS.md` with a valid lifecycle state, `_CONTEXT.md` with header fields matching the decomposition, `_DEPENDENCIES.md`, and `_REFERENCES.md`. An initialized deliverable (state ≥ `INITIALIZED`) must additionally contain the four-document kit: `Datasheet.md`, `Specification.md`, `Guidance.md`, and `Procedure.md`. A dependency-tracked deliverable must additionally contain `Dependencies.csv` with valid v3.1 schema headers. The tools `check_min_viable_fileset.sh`, `check_four_documents.sh`, and `validate_dependencies_schema.py` provide deterministic checks against these criteria.

**Dependencies.csv Schema Validation.** The v3.1 schema (SPEC.md §6) defines 29 required columns, a set of enumerated column values, identity rules (exactly one IMPLEMENTS_NODE anchor per deliverable), and provenance requirements (K-PROV-1: every extracted row must cite `EvidenceFile` and `SourceRef` or explicitly state `location TBD`). The evaluation tooling includes `check_dependency_schema.sh` and `check_implements_node.sh` for per-project automated schema compliance checks.

### 8.5.2 Harness Validation

The frontend SDK runtime is validated through a dedicated harness validation framework documented in `frontend/docs/harness/`. The framework comprises:

- **`validate-harness-section8.mjs`** — the canonical runtime validation script, verifying the SDK API surface against defined test cases
- **`validate-harness-premerge.mjs`** — a CI-optimized pre-merge wrapper that validates the Section 8 summary schema, checking that required SDK test IDs are present and that no legacy test IDs from earlier API versions appear
- **`validate-toolkit.mjs`** — operator toolkit panel validation

The CI integration (`harness_ci_integration.md`) specifies a pre-merge workflow: the frontend server is started, a readiness poll confirms the session API is reachable, the premerge validation script runs, and the summary artifact (`frontend/artifacts/harness/section8/latest/summary.json`) is uploaded. Any validation failure, missing summary artifact, or invalid summary shape causes the CI job to fail non-zero. This provides a repeatable gate against regressions in the harness SDK API contract.

### 8.5.3 Example Projects

The `examples/` directory contains five execution-root samples that serve as regression and conformance test cases:

- **`execution-6a`** — a design-build project (Penhold Public Services Building) with 6 packages (PKG-001 through PKG-006) covering general requirements, main building, site and civil works, cold storage building, optional items, and exclusions. Includes aggregation snapshots and a completed decomposition document (Phase 7).
- **`execution-6b`** — a proposal project with 10 packages covering compliance, conceptual design, design brief, sustainability, durability, delivery plan, construction methodology, commissioning, schedule, and due diligence.
- **`execution-6c`** — a related proposal with 9 packages, including a `_Change/` tool root demonstrating the change management workflow in a populated state.
- **`AB-2026-01424-WDMLRL-2026-Claude`** — a multi-discipline design project (7+ packages covering architectural, structural, mechanical, electrical, civil, plumbing, and landscape design) with a fully populated `_Evaluation/` tree including content digests, evaluation reports, reconciliation artifacts, and a scope change directory. This example demonstrates the most complete feature coverage, including the evaluation subsystem, reconciliation, and scope change workflows.
- **`_PriceSources`** — a shared price source library referenced by the cost estimation workflows.

These examples function as regression tests for agent instruction changes: if a modified agent instruction produces structurally invalid output against an established example project, the deviation is detectable. They also serve as conformance tests for the validation tooling, since the SPEC.md §12 checklist can be exercised against known-valid execution roots. The presence of `execution-6c`'s populated `_Change/` directory and `AB-2026-01424-WDMLRL-2026-Claude`'s `_Evaluation/` directory means that the evaluation and change management subsystems, which were added more recently, have documented execution traces against real project structures.

---

## 8.6 Current State and Implementation Gaps

An honest assessment of the implementation requires distinguishing between three states: fully implemented and actively exercised, specified and structurally present but not yet automated, and deferred to future development cycles with sequencing rationale.

### 8.6.1 Fully Implemented

The following capabilities are fully implemented and demonstrated in the example projects:

- The 38-agent instruction suite (all agent files present, conformance verified by AUDIT_AGENTS)
- The 28-tool registry (all tools present, registered, and referenced in agent PROTOCOL sections where applicable)
- The three-variant decomposition system (PROJECT_DECOMP, SOFTWARE_DECOMP, DOMAIN_DECOMP) sharing the DECOMP_BASE 7-gate protocol
- The orchestration spawning graph and session handoff mechanism
- The evaluation subsystem (EVALUATION + 4 subagents, with example execution traces)
- The dependency graph analysis pipeline (AUDIT_DEP_CLOSURE + `analyze_dep_closure.py`)
- The decomposition coverage audit (AUDIT_DECOMP)
- The agent conformance audit (AUDIT_AGENTS)
- The desktop application with matrix navigation, WORKBENCH/PIPELINE routing, SSE streaming, multimodal input, and desktop packaging
- The harness SDK validation framework and CI integration
- The governance document hierarchy (DIRECTIVE, SPEC, TYPES, CONTRACT, PLAN, DBM)

### 8.6.2 Specified but Not Yet Fully Automated

The invariant system defines enforcement that is partially carried by instruction text rather than by automated runtime checks. CONTRACT.md §2 identifies this distribution explicitly:

| Enforcement Point | Invariants Checked |
|-------------------|-------------------|
| Agent instructions (compile-time) | K-GHOST-1, K-WRITE-1, K-SNAP-1, K-PROV-1, K-INVENT-1, K-CONFLICT-1, K-DEP-1, K-DEP-2 |
| ORCHESTRATOR (runtime) | K-SEAL-1, K-GATE-1, K-HIER-1 |
| Human review (gate) | K-AUTH-1, K-AUTH-2, K-BIND-1, K-STALE-2, K-MERGE-1, K-VAL-1, K-STATUS-1 |
| Future tooling (automated) | K-STALE-1, K-VAL-1, K-MERGE-1, K-AUTH-2, K-DEP-2 |

The "agent instructions (compile-time)" enforcement category means that compliance depends on the agent reading and following its instruction file correctly — not on a runtime enforcement engine that would reject non-compliant behavior. Similarly, "human review (gate)" means that the human operator is the enforcement mechanism for several invariants, not automated checking. This is a deliberate design choice documented in DIRECTIVE.md (human authority at every gate), but it has a practical consequence: the system's invariant coverage depends on the quality and consistency of agent instruction following, which cannot be guaranteed to be identical across runs.

The five invariants identified for future tooling enforcement — K-STALE-1 (staleness propagation), K-VAL-1 (dirty-state detection via SHA comparison), K-MERGE-1 (pre-merge SHA verification), K-AUTH-2 (content-addressed approval binding), and K-DEP-2 (dependency ID resolution) — are fully specified in CONTRACT.md but currently rely on human review and agent self-enforcement rather than automated checking. This represents the most significant gap between the architectural specification and the implemented enforcement layer.

### 8.6.3 Future Hardening Candidates

PLAN.md §3 identifies seven future hardening candidates, ordered by priority:

1. **Content Hash Implementation for `_REFERENCES.md`** — SHA-256 content hashes for out-of-folder references, enabling automated integrity checking against K-GHOST-1 (no ghost inputs). Currently, `_REFERENCES.md` lists paths but does not verify that referenced content has not changed since sealing. Classified as medium effort.

2. **Dependencies.csv Schema Linter** — a standalone validation script for CI-level schema compliance checking. The schema (SPEC.md §6, 29 columns) is fully specified; the linter does not exist as a CI artifact, though the evaluation tool `check_dependency_schema.sh` provides an agent-invocable equivalent. Classified as low effort.

3. **Automated Folder Structure Validator** — a standalone script that walks an execution root and validates each deliverable folder against SPEC.md §12. The validation rules are fully defined; the script does not exist as a standalone CI artifact. Classified as low effort.

4. **On-Demand Dependency Graph Generation** — aggregation of deliverable-local `Dependencies.csv` files into a project-level dependency graph (JSON or Mermaid) for visualization and critical path analysis. The `analyze_dep_closure.py` tool performs graph analysis but does not produce a visualization-ready output format. Classified as medium effort.

5. **Lock Mechanism Formalization** — a deliverable-level lock mechanism preventing concurrent agent execution against the same deliverable. Currently prevented by convention in the instruction architecture but not enforced mechanically. Classified as medium-high effort.

6. **Run Record Persistence** — a unified pipeline run record schema per Type 2 agent execution. Currently, execution history is distributed across `_STATUS.md` history entries and tool root snapshot folders without a unified per-run record. Classified as medium effort.

7. **Staleness Calculation Tooling** — automated staleness propagation from the dependency graph combined with baseline SHA tracking. This is the highest-complexity item because it depends on items 4 (dependency graph generation) and 6 (run records with baseline SHAs). Classified as high effort.

### 8.6.4 Summary Assessment

The architecture's central claim — that a formally specified invariant system, applied through a layered agent hierarchy against a filesystem-native state model, can provide the auditability and authority controls required for professional practice — is substantiated in the current implementation at the level of instruction architecture and deterministic tooling. The 20 K-* invariants catalogued in CONTRACT.md (Appendix A), the 9 R-series workflow design requirements, and the 10 I-series decomposition invariants are all stated, mapped to enforcing agents or mechanisms, and covered by at least one validation pathway.

However, it would be inaccurate to characterize the current implementation as providing a verified runtime enforcement engine. The invariant system is enforced by a combination of instruction text (agents follow their specifications), deterministic tools (mechanical operations are performed correctly and reproducibly), human gates (consequential decisions are owned by licensed professionals), and a partial suite of automated audits (AUDIT_AGENTS, AUDIT_DECOMP, AUDIT_DEP_CLOSURE, and the evaluation subsystem). There is no runtime monitor that intercepts agent actions and rejects those that violate declared write scopes. There is no automated staleness propagation that flags downstream deliverables when an upstream deliverable changes. The sealing invariant (K-SEAL-1) depends on ORCHESTRATOR reading and enforcing its own protocol, not on a guard that prevents file writes before seal conditions are met.

This gap is honest and deliberate. DIRECTIVE.md §2.8 (Least Structure That Works) explicitly states: "Structure is added only when it reduces error or rework. Rigor scales with stakes." The current enforcement model — instruction text plus deterministic tools plus human gates — is sufficient for the professional practice context in which the system is deployed, where the primary actors are licensed professionals who have accepted personal responsibility for the work product. The future hardening candidates address the remaining automation gaps in priority order; they do not change the fundamental architecture, they complete it.

[TODO: Characterize the actual error rates observed in practice — do the instruction-text enforcement mechanisms show measurable conformance rates across example project executions? This would provide empirical validation for the claim that instruction-level enforcement is sufficient.]

---

## 8.7 Summary

This chapter has presented the concrete implementation of the architectural commitments described in Chapters 3 through 7. The quantitative evidence for realizability is as follows:

| Dimension | Count |
|-----------|-------|
| Agent instruction files | 38 |
| Deterministic tools (REGISTRY.md) | 28 |
| K-* invariants (CONTRACT.md) | 20 |
| Workflow design requirements (R1–R9) | 9 |
| Decomposition invariants (I1–I10) | 10 |
| Contract layers | 3 (R-series, I-series, K-series) |
| Enforcement layers (CONTRACT.md §2) | 4 (agent instructions, runtime, human review, future tooling) |
| Decomposition variants | 3 (PROJECT, SOFTWARE, DOMAIN) |
| Agent matrix cells | 12 (3 rows × 4 columns) |
| Tool registry categories | 6 |
| Example execution roots | 4 substantive projects |
| Future hardening candidates (PLAN.md §3) | 7 |

The implementation demonstrates that the philosophical commitments of Chapter 3 — filesystem-native ontology, evidence-first epistemology, gate-controlled praxiology, and human-authority axiology — are not merely aspirational. Each is instantiated in working software: the filesystem-as-graph in the execution root structure and dependency schema; the evidence-first epistemology in the mandatory provenance requirements of Dependencies.csv and the `TBD`/`FACT`/`ASSUMPTION`/`PROPOSAL` labeling system; the gate-controlled praxiology in the 7-gate decomposition protocol, the Type 1 multi-phase workflows, and the CHANGE approval token system; and the human-authority axiology in the invariants K-AUTH-1 and K-AUTH-2 and the professional responsibility model of Chapter 7.

The system's most significant implementation gap — that five invariants depend on future automated tooling rather than currently deployed checks — represents a known and sequenced development commitment, not an architectural deficiency. The gap does not undermine the system's professional usefulness in its current state; it bounds the claims that can be made about automated enforcement completeness. The architecture is complete; its automated enforcement coverage is partial and traceable.

A complete per-agent classification with type, class, interaction surface, write scope, blocking policy, and primary outputs is provided in Appendix B. The full invariant catalog with enforcement mappings is provided in Appendix A.
