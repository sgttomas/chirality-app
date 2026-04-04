# Chapter 4 — Architecture

---

## 4.1 Overview

This chapter presents the technical architecture of the Chirality project execution system. Architecture, in this context, refers not only to the structural layout of components but to the set of load-bearing decisions that determine what the system is capable of enforcing, and what it cannot. The organization of this chapter mirrors the layered nature of the design itself: the foundational decision (§4.2) establishes the substrate upon which every other mechanism rests; the entity model (§4.3) defines what exists in the system; the lifecycle state machine (§4.4) governs how entities evolve; the agent type hierarchy (§4.5) partitions authority and responsibility; the write scope architecture (§4.6) creates formal fault containment zones; the invariant system (§4.7) makes the constraints binding across all layers; the orchestration model (§4.8) coordinates agent execution across sessions; and the brief and output contracts (§4.9) standardize the input and output boundaries of individual agent runs.

Each section demonstrates how the architecture operationalizes one or more of the four philosophical pillars established in Chapter 3: the ontological commitment to filesystem-native domain representation, the epistemological commitment to evidence-grounded and auditable claims, the praxiological commitment to bounded, gate-controlled execution, and the axiological commitment to human authority and professional responsibility. The architecture is not a technical substrate to which these principles are subsequently applied — they are the structural logic from which the architecture is built.

---

## 4.2 The Foundational Decision: Filesystem as State

### 4.2.1 The Graph Model

The Chirality system represents project state as an implicit graph encoded entirely in git-tracked files. This is the load-bearing architectural decision, identified as such in both DIRECTIVE.md §2.1 and DBM §1.1. Every other architectural capability depends upon it; none could be preserved if state migrated to an external system.

The graph model is formally stated as follows:

- **Nodes** are deliverable folders and package folders. Each folder on the filesystem corresponds to an entity in the project domain.
- **Edges** are rows in `Dependencies.csv` registers. Each row encodes a directed relationship between a host deliverable and a target entity, classified as either a tree edge (ANCHOR class) or a directed acyclic graph edge (EXECUTION class). The two edge classes together form a knowledge graph: the tree preserves stable definitional intent; the DAG captures execution-time couplings.
- **Properties** are plain markdown files within each node folder. The files `_STATUS.md`, `_CONTEXT.md`, `_DEPENDENCIES.md`, `_REFERENCES.md`, and the four-document kit (Datasheet, Specification, Guidance, Procedure) carry the identity, lifecycle state, traceability, and technical content of each deliverable.

This formulation means the project graph has no representation other than the filesystem itself. There is no translation layer, no secondary index, and no remote service. An agent, a human, and a static analysis tool all observe the same structure and parse the same files.

### 4.2.2 Why This Decision Is Load-Bearing

DIRECTIVE.md §2.1 provides the canonical statement: "Every capability the system provides — V-model traceability, immutable snapshots, change propagation tracking, content-addressed approval, and the complete audit trail — depends on state being in git-tracked files. If state moved to a database, every one of these capabilities would need to be rebuilt."

This claim merits unpacking. Each named capability derives from the filesystem commitment:

- **V-model traceability** is achievable because ANCHOR-class dependency rows in each deliverable's `Dependencies.csv` link back up the decomposition tree to scope items (`SOW-NNN`) and objectives (`OBJ-NNN`). These links are stable, human-readable, and directly inspectable. In a database-backed system, this traceability chain would require a separate schema and synchronization discipline.
- **Immutable snapshots** are achievable because the filesystem natively supports append-only history through timestamped directories. A snapshot folder, once created, is never modified. The git history provides an independent record of when it was created and what it contained.
- **Change propagation tracking** is achievable because the staleness invariants (K-STALE-1, K-STALE-2) can be computed by traversing the EXECUTION-class dependency graph encoded in `Dependencies.csv` files. Every dependency that might be affected by an upstream change is identifiable without querying a service.
- **Content-addressed approval** is achievable because git commit SHAs provide a stable, unforgeable identifier for any version of any file. Approvals recorded in versioned files bind to the SHA of the approved content; if the content changes, the SHA changes, and the approval is voided. This is enforced by invariant K-AUTH-2.
- **The audit trail** is git history. No additional logging infrastructure is required. Every agent write, human edit, and approval record is a versioned commit observable through standard tools.

[COMPARE: External-database agent frameworks (LangChain, AutoGen, CrewAI) typically maintain agent state in memory or external stores; compare their auditability and reproducibility properties against the filesystem-native approach]

[RATIONALE: The choice to forgo an external database is not primarily a simplicity argument — it is an auditability argument. The forensic property of git history is identical to what a regulated environment requires for design record keeping.]

### 4.2.3 What the Filesystem Commitment Enables and Precludes

The filesystem commitment enables:
- Offline operation without infrastructure dependencies
- Agent execution by any compliant LLM runtime capable of reading and writing files
- Human inspection of all state without specialized tooling
- Direct integration with existing engineering document management workflows

The filesystem commitment precludes:
- External databases as sources of execution truth
- Server-side session state that diverges from on-disk content
- Hidden agent memory that persists across sessions outside versioned files
- Centralised dependency graphs that must be kept synchronized with deliverable-local registers

These exclusions are not limitations — they are the mechanism by which the system's auditability guarantees are maintained. DIRECTIVE.md §2.5 states the principle directly: "If it is not in a versioned file, it does not exist for purposes of reliance." Any capability that would require violating this principle is, by architectural definition, outside the system's scope.

---

## 4.3 Entity Model and Domain Ontology

### 4.3.1 Project Hierarchy

The project hierarchy, defined in TYPES.md §1 and instantiated physically in SPEC.md §1, is deliberately flat: packages contain deliverables, and there are no intermediate levels. There are no phases, sub-packages, or task sub-levels within deliverables. This constraint is encoded as invariant K-HIER-1 and is enforced at the decomposition gate, during workspace scaffolding, and by human review of folder structures.

The hierarchy is:

```
{EXECUTION_ROOT}/
└── PKG-XX_{PkgLabel}/           # Package: a flat partition of project scope
    └── 1_Working/
        └── DEL-XX-YY_{DelLabel}/  # Deliverable: a unit of production
```

Each package represents a non-overlapping, gap-free partition of project scope. Every scope item (SOW item) belongs to exactly one package. Each deliverable belongs to exactly one package, has a responsible party, a type classification, and produces one or more anticipated artifacts. An artifact is any tangible output produced within a deliverable folder — including but not limited to the standard four-document kit.

[RATIONALE: The flat hierarchy is an explicit design choice that prioritizes automation reliability and coverage verifiability. Nested hierarchies introduce ambiguity in scope assignment and make machine-checkable completeness proofs significantly harder to construct. The flatness constraint enables the decomposition ledger (§8.3 of the DBM) to serve as a machine-checkable completeness artifact.]

### 4.3.2 Stable Identifiers

TYPES.md §2 establishes the identity system. Identifiers are assigned once and persist across renames, path changes, and structural reorganization. Path is explicitly characterized as a physical projection of the decomposition, not identity itself (K-ID-1). The canonical identifier formats are:

| Entity | Format | Example |
|--------|--------|---------|
| Package | `PKG-XX` | `PKG-01` |
| Deliverable | `DEL-XX-YY` | `DEL-01-01` |
| Dependency | `DEP-XX-YY-NNN` | `DEP-01-01-001` |
| Scope Item | `SOW-NNN` | `SOW-003` |
| Objective | `OBJ-NNN` | `OBJ-001` |

The ID coupling convention for deliverables — that the leading digits of a deliverable ID match the package digits — is deterministic and mechanically derivable from the decomposition, not from path traversal. This means that an agent can determine package membership from a deliverable ID alone, without filesystem access.

Folder names combine the stable identifier with a human-readable, filesystem-safe label (e.g., `PKG-01_Civil_Engineering/`). The canonical unsanitized name is preserved in the `_CONTEXT.md` file within each deliverable folder.

### 4.3.3 Deliverable Folder Layout and Minimum Viable Fileset

SPEC.md §2 defines the complete file inventory for a deliverable folder. The minimum viable fileset, created by the PREPARATION agent, consists of:

- `_STATUS.md` — Lifecycle state and history (canonical lifecycle indicator, per K-STATUS-1)
- `_CONTEXT.md` — Identity, decomposition pointer, scope traceability
- `_DEPENDENCIES.md` — Dependency summary with human-declared and agent-extracted zones
- `_REFERENCES.md` — Source document pointers
- `_SEMANTIC.md` (placeholder) — Semantic lens scaffold

The full initialized state adds the four-document kit produced by the 4_DOCUMENTS agent: `Datasheet.md`, `Specification.md`, `Guidance.md`, and `Procedure.md`. Optional files — `Dependencies.csv`, `_MEMORY.md`, `_SEMANTIC_LENSING.md` — are added by subsequent agents as work proceeds.

### 4.3.4 The Dual-Graph Model

TYPES.md §3 establishes the two classes of dependency relationships that together constitute the project knowledge graph.

**ANCHOR-class edges** are vertical tree edges connecting each deliverable upward to its definitional context. Every deliverable carries exactly one `IMPLEMENTS_NODE` row linking it to its parent package or WBS node, and zero or more `TRACES_TO_REQUIREMENT` rows linking it to scope items and objectives. The ANCHOR tree is the traceability backbone — it makes every unit of production traceable back to the requirements it is intended to satisfy.

**EXECUTION-class edges** are horizontal DAG edges capturing information flow and production dependencies between deliverables. These encode prerequisite relationships (what a deliverable needs before work can proceed), interface relationships (explicit data exchanges), handover relationships (outputs consumed as inputs), constraint relationships (conditions imposed by one deliverable on another), and enablement relationships (where one deliverable opens the path for downstream work).

The two graph structures serve fundamentally different purposes. The ANCHOR tree encodes static project topology — it is established at decomposition time and rarely changes. The EXECUTION DAG encodes dynamic production couplings — it evolves as agents extract more dependencies from deliverable content. Together they allow the system to answer both vertical questions (what requirement does this deliverable trace to?) and horizontal questions (what does this deliverable need before work can start?).

---

## 4.4 Lifecycle State Machine

### 4.4.1 The Six States

SPEC.md §3 and TYPES.md §5 define the deliverable lifecycle as a linear state machine with six states:

```
OPEN → INITIALIZED → SEMANTIC_READY → IN_PROGRESS → CHECKING → ISSUED
```

| State | Entry Condition |
|-------|----------------|
| `OPEN` | PREPARATION has created the folder and minimum viable fileset; no substantive content |
| `INITIALIZED` | 4_DOCUMENTS agent has generated the four-document kit (Datasheet, Specification, Guidance, Procedure) |
| `SEMANTIC_READY` | CHIRALITY_FRAMEWORK agent has generated `_SEMANTIC.md` |
| `IN_PROGRESS` | Human or WORKING_ITEMS agent has commenced active substantive work |
| `CHECKING` | Human has moved the deliverable to the review staging area |
| `ISSUED` | Human has approved the deliverable and released it for use |

### 4.4.2 Transition Rules and Authorized Actors

SPEC.md §3.3 defines transition authorization as follows:

| Transition | Authorized Actor |
|------------|-----------------|
| `→ OPEN` | PREPARATION only |
| `OPEN → INITIALIZED` | 4_DOCUMENTS only |
| `INITIALIZED → SEMANTIC_READY` | CHIRALITY_FRAMEWORK only |
| `INITIALIZED → IN_PROGRESS` | Human or WORKING_ITEMS (when semantic step is skipped) |
| `SEMANTIC_READY → IN_PROGRESS` | Human or WORKING_ITEMS |
| `IN_PROGRESS → CHECKING` | Human only |
| `CHECKING → ISSUED` | Human only |

The pattern is significant. Forward transitions through the early automated states (`OPEN`, `INITIALIZED`, `SEMANTIC_READY`) are agent-authorized — they confirm that specific mechanical preparation has completed. Forward transitions through the consequential states (`CHECKING`, `ISSUED`) are human-only. The final two transitions — moving to external review and releasing work for reliance — cannot be performed by any agent regardless of type. This is an architectural instantiation of the axiological commitment described in Chapter 3: agent execution is bounded; human authorization gates the boundary.

The `INITIALIZED → SEMANTIC_READY` transition is optional. If the semantic lensing step is omitted, deliverables may transition directly from `INITIALIZED → IN_PROGRESS`. This reflects the "least structure that works" principle (DBM §1.8): semantic enrichment is available when it adds value, but its absence does not block production.

### 4.4.3 Stage Gates vs. Lifecycle States

TYPES.md §5.2 draws an explicit distinction that is architecturally important. **Lifecycle states** track the production status of individual deliverables and are recorded in `_STATUS.md`. **Stage gates** (30%, 60%, 90%, IFC, and similar project-level milestones) are human-managed checkpoints that represent aggregate progress targets across a set of deliverables. Stage gates are not lifecycle states and are tracked separately in coordination records.

The distinction prevents a category error that is common in project management tooling: conflating the micro-level question (is this deliverable ready for review?) with the macro-level question (has the project reached a stage gate?). In the Chirality architecture, the answer to the first question is always obtained from `_STATUS.md`; the answer to the second requires aggregation across the project, which is the domain of the SCHEDULING and RECONCILIATION agents.

### 4.4.4 `_STATUS.md` as Canonical State Indicator

Invariant K-STATUS-1 states: "`_STATUS.md` is the canonical, human-readable lifecycle state file for each deliverable. No other file determines deliverable state." This invariant has practical implications for agent behavior: before any agent performs a lifecycle-relevant write, it must read `_STATUS.md` to determine whether the operation is valid for the current state. An attempt to initialize a deliverable that is already `IN_PROGRESS`, for example, must be flagged as a precondition failure.

The enforcement of K-STATUS-1 is distributed: it appears in the SPEC of every agent whose behavior varies by lifecycle state, and it is a first-order check in ORCHESTRATOR's context-sealing gate (K-SEAL-1).

### 4.4.5 The Interleaved Warrant Lifecycle

The deliverable lifecycle tracks production state. A second lifecycle — the **warrant lifecycle** — tracks the epistemic state of the claims within the deliverable. Chapter 3 (§3.2.2) defines six epistemic primitives (claim, warrant, status, gap, conflict, ruling) and a four-state warrant lifecycle:

```
UNWARRANTED → CITED → REVIEWED → AUTHENTICATED
```

The two lifecycles are interleaved: a deliverable in `IN_PROGRESS` contains claims in varying warrant states. The transition to `CHECKING` requires that critical claims have been warranted. The transition to `ISSUED` requires that the professional has authenticated the work — declaring the aggregate warrant state sufficient for reliance. The warrant lifecycle is formalized in `TYPES.md` §10 and developed in full in Chapter 5 (§5.5).

---

## 4.5 Agent Type Hierarchy

### 4.5.1 Structural Overview

The agent system is organized into three types with strictly partitioned responsibilities. The hierarchy is defined in DBM §2 and summarized in TYPES.md §4. It is not merely a labeling convention — it is the mechanism by which the system's authority model is enforced.

**Type 0 — Canonical Standards (Architect).** Type 0 agents define the invariant protocols and design standards that all downstream agents must conform to. They do not write project state. They are, in the DBM's terminology, the "constitutional layer" of the system. The Type 0 layer is composed of HELPS_HUMANS, which defines the workflow design standard (R1–R9, the four-section agent structure, brief formats, and QA contracts), and DECOMP_BASE, which defines the decomposition protocol standard (the seven-gate protocol, I1–I10 invariants, and the extension contract for decomposition variants). Where any agent instruction disagrees with a Type 0 standard, the agent instruction must be edited to conform — not the standard.

**Type 1 — Interactive Personas (Manager).** Type 1 agents are human-facing orchestrators. They run conversational, gate-controlled workflows where humans make consequential decisions and agents handle routing, structural output, and brief preparation. Type 1 agents may spawn Type 2 agents. They own orchestration decisions but do not own engineering content. See Appendix B for the complete inventory and `docs/REPO_INVENTORY.md` for current aggregate counts.

**Type 2 — Bounded Task Agents (Specialist).** Type 2 agents are brief-driven specialists operating in straight-through execution mode. They receive structured inputs (INIT-TASK briefs), produce auditable outputs, and return to their invoking agent without mid-run human interaction. Type 2 agents never spawn other agents. See Appendix B for the complete inventory and `docs/REPO_INVENTORY.md` for current aggregate counts.

[COMPARE: Multi-agent frameworks such as AutoGen and CrewAI support role differentiation among agents but do not enforce a strict constitutional hierarchy with write-scope enforcement and non-bypassable human gates; compare authority isolation properties]

### 4.5.2 Formal Authority Properties

DBM §2 identifies three authority invariants that the entire system depends upon:

1. **Type 2 cannot escalate to Type 1 authority.** Specialists execute bounded briefs and return outputs. They cannot initiate gate reviews, spawn other agents, or make scope decisions. A Type 2 agent that encounters a scope question must record it as `TBD` and surface it in the run report — it cannot route the question to a human directly.

2. **Type 1 cannot override Type 0 constraints.** Managers orchestrate within the rules established by canonical standards. They cannot relax the R1–R9 workflow requirements, the I1–I10 decomposition invariants, or any K-* invariant. An orchestration decision that would require violating a Type 0 constraint is not a valid orchestration decision.

3. **Human gates cannot be bypassed by any agent type.** No agent — regardless of type — can approve deliverables for external reliance, resolve conflicts authoritatively, commit to the baseline, or advance the lifecycle to `CHECKING` or `ISSUED`. These transitions are structurally unavailable to agents. The architecture does not merely recommend that agents defer to humans at these junctions; it removes the capability.

### 4.5.3 Classification Properties

Each agent instruction file declares six properties in a standardized header block (DBM §3.2):

| Property | Valid Values | Semantics |
|----------|-------------|-----------|
| `AGENT_TYPE` | `TYPE 0`, `TYPE 1`, `TYPE 2` | Position in the hierarchy |
| `AGENT_CLASS` | `PERSONA`, `TASK` | Conversational interface vs. straight-through execution |
| `INTERACTION_SURFACE` | `chat`, `INIT-TASK`, `spawned`, `both` | How the agent is invoked |
| `WRITE_SCOPE` | See §4.6 | What filesystem area the agent may write to |
| `BLOCKING` | `never`, `allowed` | Whether the agent may pause for human input |
| `PRIMARY_OUTPUTS` | Free text | What the agent produces |

These properties are not metadata — they are enforceable constraints. The `BLOCKING: never` property on all Type 2 agents means that no mid-run human decision is required or possible; a Type 2 agent that encounters an ambiguity must handle it conservatively (record as `TBD`) rather than pause the run. The `WRITE_SCOPE` property determines exactly which filesystem zones the agent may touch, as detailed in §4.6.

---

## 4.6 Write Scope Architecture

### 4.6.1 The Five Scope Categories

The write scope model, defined in DBM §7, enforces a formal separation between source truth and derived outputs. Every agent is assigned to exactly one of five scope categories. The category determines which portions of the filesystem the agent may modify; writes outside the declared scope are architectural violations of K-WRITE-1.

The five categories, from most to least restrictive, are:

- **NONE** — Read-only. The agent may draft content but may not write to any location. The human applies any output. Applies to: HELPS_HUMANS, DECOMP_BASE, HELP_HUMAN.
- **REPO-METADATA-ONLY** — May write to instruction files, README, and templates — not to execution truth. Applies to: DOMAIN_DECOMP, CONTEXT_TRANSPOSE.
- **PROJECT-LEVEL** — May write to decomposition documents, project metadata files, and folder scaffolding. Applies to: PROJECT_DECOMP, SOFTWARE_DECOMP, SCOPE_CHANGE, PREPARATION, ESTIMATE_PREP.
- **DELIVERABLE-LOCAL** — May write only within a single assigned production unit folder. Applies to: WORKING_ITEMS, 4_DOCUMENTS, DOMAIN_DOCUMENTS, CHIRALITY_FRAMEWORK, CHIRALITY_LENS, DEPENDENCIES, TASK, DELIVERABLE_TASK, REVIEW.
- **TOOL-ROOT-ONLY** — May write only to a specific designated tool root under `{EXECUTION_ROOT}/`. Applies to: ORCHESTRATOR (`_Coordination/`), RECONCILIATION (`_Reconciliation/`), CHANGE (`_Change/` plus repo files with approval gate), SCHEDULING (`_Schedule/`), ESTIMATING (`_Estimates/`), AGGREGATION (`_Aggregation/`), and the four audit agents.

### 4.6.2 The Write Scope Tree

DBM §7.1 presents the full assignment structure in a tree format:

```
NONE
├── HELPS_HUMANS
├── DECOMP_BASE
└── HELP_HUMAN

REPO-METADATA-ONLY
├── DOMAIN_DECOMP
└── CONTEXT_TRANSPOSE

PROJECT-LEVEL
├── PROJECT_DECOMP
├── SOFTWARE_DECOMP
├── SCOPE_CHANGE
├── PREPARATION
└── ESTIMATE_PREP

DELIVERABLE-LOCAL
├── WORKING_ITEMS (+NEXT_INSTANCE_STATE.md standing exception)
├── 4_DOCUMENTS
├── DOMAIN_DOCUMENTS
├── CHIRALITY_FRAMEWORK
├── CHIRALITY_LENS
├── DEPENDENCIES (dependency artifacts only)
├── TASK
└── REVIEW (+tool-root for snapshots)

REPO-WIDE
├── TOOLMAKER
└── SKILLMAKER

TOOL-ROOT-ONLY
├── ORCHESTRATOR         → _Coordination/
├── RECONCILIATION       → _Reconciliation/
├── CHANGE               → _Change/ (+repo files with approval gate)
├── SCHEDULING           → _Schedule/
├── ESTIMATING           → _Estimates/
├── AGGREGATION          → _Aggregation/
├── AUDIT_AGENTS         → _Reconciliation/AgentAudit/
├── AUDIT_DECOMP         → _Reconciliation/DecompCoverage/
├── AUDIT_DEP_CLOSURE    → _Reconciliation/DepClosure/
├── AUDIT_HYPERGRAPH_CLOSURE → _Reconciliation/HypergraphClosure/
├── AUDIT_GOVERNANCE     → _Reconciliation/GovernanceAudit/
├── AUDIT_EPISTEMIC      → _Reconciliation/EpistemicAudit/
├── AUDIT_SCOPE_CLOSURE  → _Reconciliation/ScopeClosureAudit/
├── DOMAIN_HYPERGRAPH    → _Aggregation/Hypergraph/
├── EVALUATION           → _Evaluation/
├── CONTENT_DIGEST       → _Evaluation/content-digests/
├── EVALUATION_REPORT    → _Evaluation/reports/
├── EVALUATION_STRUCTURE_AUDIT → _Evaluation/reports/
└── EVALUATION_DEPENDENCY_AUDIT → _Evaluation/reports/
```

### 4.6.3 The Six Write Scope Rules

DBM §7.2 states six rules that govern write scope enforcement across the agent suite:

1. Every agent declares its write scope in the Agent Header Block.
2. Deliverable-local agents cannot write outside their assigned production unit folder.
3. Tool-root agents write only to their designated tool root under `{EXECUTION_ROOT}/`.
4. Source truth (deliverable production documents) is never modified by tool-root agents.
5. `_STATUS.md` updates are restricted to designated agents (PREPARATION, 4_DOCUMENTS, CHIRALITY_FRAMEWORK, REVIEW) and only for forward lifecycle transitions.
6. Cross-deliverable scanning or editing is prohibited inside WORKING_ITEMS sessions unless the human explicitly requests a cross-check.

### 4.6.4 Write Scope as Fault Containment

The practical significance of write scope is containment. A failure in a Type 2 task agent — whether through model error, malformed input, or unexpected behavior — can corrupt only the zone to which that agent has write access. Because tool-root agents cannot write to source truth, and deliverable-local agents cannot write to other deliverables, the blast radius of any single agent failure is bounded by architectural construction.

This is the property DBM §1.5 refers to as "write quarantine": formal fault containment zones established not by runtime monitoring but by the structural impossibility of cross-zone writes. The distinction matters: a monitoring approach would detect the violation after it occurred; the write scope model prevents the violation from being representable. A Type 2 agent running under WORKING_ITEMS that attempts to modify a file in another deliverable's folder is not committing a policy violation — the action is outside its declared scope and should not occur in a conforming agent.

[COMPARE: LangChain agents and ReAct-style frameworks typically have broad tool access without formal zone partitioning; compare fault isolation properties under agent misbehavior]

[RATIONALE: The decision to declare write scope at the agent level rather than enforce it at the filesystem level (e.g., through OS permissions) is deliberate. Agent-level declaration makes the scope contract visible in the instruction file itself, auditable by any reader, and expressible with the semantics of the project domain — "deliverable-local" means something specific in terms of folder structure, which a generic OS permission model cannot express.]

---

## 4.7 Invariant System

### 4.7.1 Three Layers of Contracts

The Chirality system maintains agent behavior through three distinct layers of contracts, defined in DBM §4. Each layer addresses a different scope of concern, and they are complementary rather than overlapping.

**R1–R9: Workflow Design Requirements** (from HELPS_HUMANS). These nine requirements apply to all agents and to the design of any new agent workflow. They establish universal baseline obligations: that human decision rights are explicit (R1), that task agents run straight-through without mid-run gates (R2), that write quarantine is enforced (R3), that snapshots are immutable (R4), that provenance is mandatory (R5), that no-invention behavior is defined (R6), that conflicts and duplicates are surfaced (R7), that brief-driven execution exists (R8), and that publication is hygienic and non-destructive by default (R9).

**I1–I10: Decomposition Invariants** (from DECOMP_BASE). These ten invariants apply specifically to all decomposition agents (PROJECT_DECOMP, SOFTWARE_DECOMP, DOMAIN_DECOMP) and are verified by AUDIT_DECOMP. They govern: human-validated decomposition gates (I1), no-invention in scope assignment (I2), flat partition structure (I3), no overlaps and no gaps (I4), stable identifiers (I5), deterministic ID coupling (I6), best-effort objective mapping (I7), traceable rationale (I8), machine-checkable ledger and telemetry (I9), and vocabulary discipline (I10).

**K-* Invariants: System-Wide Enforcement** (from CONTRACT.md). The K-* catalog defines system-wide binding constraints. The full catalog is reproduced in Appendix A; the groupings and their primary enforcing agents are summarized below.

| K-* Group | Invariants | Primary Enforcement |
|-----------|-----------|---------------------|
| Hierarchy & Identity | K-HIER-1, K-ID-1 | PROJECT_DECOMP, PREPARATION |
| Authority & Approval | K-AUTH-1, K-AUTH-2, K-BIND-1 | REVIEW, CHANGE (approval gates) |
| Sealing & Context | K-SEAL-1, K-GHOST-1 | ORCHESTRATOR, Type 2 agents |
| Dependencies | K-DEP-1, K-DEP-2 | DEPENDENCIES, AUDIT_DEP_CLOSURE |
| Status | K-STATUS-1 | PREPARATION, 4_DOCUMENTS, CHIRALITY_FRAMEWORK, REVIEW |
| Staleness & Validation | K-STALE-1, K-STALE-2, K-VAL-1 | AUDIT_DEP_CLOSURE, RECONCILIATION; future tooling |
| Gates | K-GATE-1 | ORCHESTRATOR, SCHEDULING |
| Merge | K-MERGE-1 | CHANGE |
| Provenance | K-PROV-1 | DEPENDENCIES (every row must cite evidence) |
| Invention | K-INVENT-1 | Universal (all agents) |
| Conflicts | K-CONFLICT-1 | Universal (all agents) |
| Write Scope | K-WRITE-1 | Universal (declared per agent) |
| Snapshots | K-SNAP-1 | All snapshot-producing agents |

### 4.7.2 Four Enforcement Layers

CONTRACT.md §2 defines the enforcement map. The K-* invariants are not enforced by a single centralized mechanism; they are distributed across four enforcement layers at different points in the system's operation:

**Compile-time (agent instructions).** The invariants K-GHOST-1, K-WRITE-1, K-SNAP-1, K-PROV-1, K-INVENT-1, K-CONFLICT-1, K-DEP-1, and K-DEP-2 are enforced by the content of the agent instruction files themselves. When an agent instruction is written to conform with these invariants, the agent's behavior is constrained at the point of instruction — before any runtime invocation. This is "compile-time" in the sense that the constraint is baked into the specification the agent operates from.

**Runtime (ORCHESTRATOR).** The invariants K-SEAL-1, K-GATE-1, and K-HIER-1 are enforced by ORCHESTRATOR during active session management. ORCHESTRATOR checks that context is sealed and gate-approved before dispatching any Type 2 agent, and that gate structure conforms to the project's configured gate map.

**Human gate.** The invariants K-AUTH-1, K-AUTH-2, K-BIND-1, K-STALE-2, K-MERGE-1, K-VAL-1, and K-STATUS-1 are enforced through human review at defined gates. These invariants govern decisions that cannot be delegated to automated systems: binding approvals, staleness triage, merge authorization, and lifecycle state management for consequential transitions.

**Future tooling (automated).** K-STALE-1, K-VAL-1, K-MERGE-1, K-AUTH-2, and K-DEP-2 are identified as candidates for automated tooling — specifically for SHA comparison, staleness computation, and dependency resolution validation. The current architecture makes these checks tractable by ensuring all relevant state is in git-tracked files; the tooling has not yet been implemented.

This distribution of enforcement is architecturally significant. It means that no single failure mode — a misbehaving agent, a human error, a tool gap — can violate all constraints simultaneously. The layers are complementary and partially redundant.

[RATIONALE: The decision to enforce many invariants at the agent-instruction level rather than at runtime provides a stronger guarantee than runtime-only enforcement: an instruction-level constraint means the agent cannot describe a conforming execution path that violates the invariant, rather than merely detecting the violation after the fact. The tradeoff is that instruction-level enforcement depends on the quality of the agent instructions themselves, which requires the Type 0 canonical standards and the AUDIT_AGENTS agent to maintain.]

---

## 4.8 Orchestration and Control Loop

### 4.8.1 The Spawning Graph

DBM §6.1 defines the spawning graph — the complete map of which agents may initiate which other agents:

```
HELP_HUMAN (Type 1) — classifies intent and routes; does not spawn

ORCHESTRATOR (Type 1) ──spawns──┬── PREPARATION
                                ├── 4_DOCUMENTS
                                ├── DOMAIN_DOCUMENTS
                                ├── CHIRALITY_FRAMEWORK
                                ├── CHIRALITY_LENS
                                ├── DOMAIN_HYPERGRAPH (DOMAIN variant; Phase 2.6)
                                ├── ESTIMATING
                                └── AGGREGATION

WORKING_ITEMS (Type 1) ──spawns──── TASK

RECONCILIATION (Type 1) ──spawns──┬── AUDIT_DEP_CLOSURE
                                  ├── AUDIT_AGENTS
                                  ├── AUDIT_DECOMP
                                  ├── AUDIT_EPISTEMIC
                                  ├── AUDIT_GOVERNANCE
                                  ├── AUDIT_SCOPE_CLOSURE
                                  └── AUDIT_HYPERGRAPH_CLOSURE (DOMAIN variant)

EVALUATION (Type 1) ──spawns──┬── CONTENT_DIGEST
                              ├── EVALUATION_REPORT
                              ├── EVALUATION_STRUCTURE_AUDIT
                              └── EVALUATION_DEPENDENCY_AUDIT

CHANGE (Type 1) — leaf agent; implements approved edits; spawns nothing
TOOLMAKER (Type 1) — standalone; designs and implements deterministic tools
SKILLMAKER (Type 1) — standalone; designs and governs repo-native skills

REVIEW (Type 1) — triggers AUDIT_DECOMP as a precondition check
SCOPE_CHANGE (Type 1) — hands off to ORCHESTRATOR + CHANGE
CONTEXT_TRANSPOSE (Type 1) — hands off to CHANGE for publication
SCHEDULING (Type 1) — standalone; reads dependency graph; produces schedule artifacts
```

The spawning graph is acyclic by construction: no Type 2 agent spawns any other agent, and the Type 1 agents that do spawn Type 2 agents do not spawn each other. This property means that execution trees are bounded in depth and that no runaway spawning cascade is architecturally possible.

### 4.8.2 Session Handoff Mechanism

The system maintains continuity across agent sessions through two durable artifacts maintained by ORCHESTRATOR (DBM §6.2):

| Artifact | Mutability | Content |
|----------|-----------|---------|
| `NEXT_INSTANCE_PROMPT.md` | Stable — updated only on protocol changes | Session startup instructions |
| `NEXT_INSTANCE_STATE.md` | Mutable — updated at each session handoff | Current pointers, program state, active rulings, immediate next actions |

The session handoff flow is: ORCHESTRATOR creates both files during workspace initialization → WORKING_ITEMS reads both at the start of each session (Phase 0a) → WORKING_ITEMS updates `NEXT_INSTANCE_STATE.md` at session end → CHANGE verifies state before committing.

This mechanism solves a fundamental limitation of LLM-based agent systems: the absence of persistent memory across session boundaries. Rather than relying on the LLM's context window to retain program state, the system externalizes that state to versioned files. Any future session that reads these files acquires the same program state as if it had been running continuously. The guarantee is not a property of the language model — it is a property of the filesystem.

### 4.8.3 The Control Loop

The operational control loop in a running project follows the sequence:

1. **ORCHESTRATOR** initializes the workspace and session handoff artifacts; manages gate sequence.
2. **WORKING_ITEMS** reads session state and executes deliverable-level work; dispatches TASK agents pre-authorizedly.
3. **DEPENDENCIES** reruns are triggered after content changes to keep dependency registers current.
4. **RECONCILIATION** aggregates and audits across the project; dispatches audit agents to produce closure reports and coverage analyses.
5. **CHANGE** receives approved commit instructions and applies them to the repository, requiring explicit approval tokens before any state-changing action.
6. The loop returns to WORKING_ITEMS for the next session, with updated state in `NEXT_INSTANCE_STATE.md`.

This loop is not continuous — it is human-triggered at each session. The architecture does not run agents autonomously between human interactions. Each session starts when a human opens the workbench and ends when they commit and close.

### 4.8.4 Spawning Mechanisms

DBM §6.3 defines four distinct spawning mechanisms, each with different authorization requirements:

| Mechanism | Used By | Authorization Required |
|-----------|---------|----------------------|
| **Human-gated phases** | ORCHESTRATOR | Explicit human confirmation at each sequential phase |
| **Pre-authorized dispatch** | WORKING_ITEMS | Human confirms session objective once; TASK agents dispatched autonomously within session |
| **Human-directed toolbelt** | RECONCILIATION | Human provides TOOLBELT list of authorized agents; one task per cycle by default |
| **Approval-gated execution** | CHANGE | Explicit approval tokens required per action (`APPROVE:` or `APPROVE_DESTRUCTIVE:`) |

The progressive reduction in per-action authorization overhead is deliberate: ORCHESTRATOR phases are high-stakes and infrequent; WORKING_ITEMS task dispatch is routine and repetitive. Requiring explicit human confirmation at every TASK dispatch in a working session would impose ceremony with no corresponding safety benefit. Conversely, CHANGE applies the most stringent authorization requirement because its operations modify repository state — an action that, if incorrect, may require recovery operations.

[COMPARE: Most agentic orchestration frameworks (e.g., AutoGen group chat, LangChain agents with tools) do not distinguish multiple authorization levels within a single agent type; compare their capacity to calibrate human oversight to the consequence level of individual operations]

---

## 4.9 Brief and Output Contracts

### 4.9.1 The INIT-TASK Brief Format

DBM §9.1 defines the standard input contract for all Type 2 agents. The INIT-TASK brief is a structured parameter table, not natural language. It may be supplied inline or through a file-based `INIT-TASK.md` surface, with inline fields taking precedence when both exist. It contains:

```
PURPOSE:           <what the run is for>
SCOPE:             <deliverable IDs / package IDs / paths>
WHERE_TO_LOOK:     <roots / patterns>
OUTPUT_LABEL:      <optional>
CONFIG:            <optional; validated enums driving behavior>
CONSTRAINTS:       <schema, naming, maturity>
EXCLUSIONS:        <paths / patterns>
NOTES:             <anything else>
```

Individual agents extend this base template with domain-specific parameters. The DEPENDENCIES agent, for example, adds `MODE` (UPDATE vs. RESET_EXTRACTED), `STRICTNESS` (CONSERVATIVE vs. AGGRESSIVE), and `SOURCE_DOCS`. The 4_DOCUMENTS agent adds `RUN_PASSES` (FULL, P1_P2, or P3_ONLY), `ALLOW_OVERWRITE_STATES`, and `DECOMP_VARIANT`.

The brief format serves three functions. First, it makes agent inputs deterministic and repeatable: two invocations with identical briefs on identical filesystem state should produce equivalent outputs. Second, it enables pre-flight validation: an agent that receives an incomplete or structurally invalid brief halts with a `FAILED_INPUTS` status rather than proceeding with partial information. Third, it creates an auditable record: the brief is written verbatim into the snapshot's `Brief.md` file, so the exact inputs to any run are preserved alongside its outputs.

### 4.9.2 Snapshot Output Convention

DBM §9.4 defines the output convention for all agents that produce analysis outputs to tool roots. The convention is:

```
{TOOL_ROOT}/{AGENT_PREFIX}_{RUN_LABEL}_{YYYY-MM-DD}_{HHMM}/
├── Brief.md              # Verbatim brief inputs
├── RUN_SUMMARY.md        # What happened, PASS/FAIL status
├── QA_Report.md          # Schema validity, coverage, provenance, warnings
├── Decision_Log.md       # Non-trivial decisions made during the run
├── <agent-specific outputs>
└── Evidence/             # (where applicable) supporting CSV/data files

{TOOL_ROOT}/_LATEST.md    # Mutable pointer to most recent snapshot
```

The design separates mutable from immutable state explicitly: the `_LATEST.md` pointer file is expected to be overwritten on each run; the snapshot folder is not. A reader who needs the current state of a tool root reads `_LATEST.md` for the pointer, then reads the referenced snapshot. A reader who needs the history of all runs reads the snapshot folders in chronological order.

### 4.9.3 The Immutability Rule

K-SNAP-1 states: "Task agent outputs to tool roots are immutable snapshots. Pointer files (`_LATEST.md`) may be overwritten; snapshot folders must not."

The rationale for this rule connects directly to the epistemological commitments described in Chapter 3. If a snapshot could be modified after creation, the relationship between a git commit containing the snapshot and the run that produced it would be ambiguous — the snapshot's content at commit time might not match its content at some later time. The immutability rule ensures that the git history is a faithful record: every version of every snapshot that was ever committed remains available and unchanged. This property is what makes the snapshot trail equivalent to an audit trail in a regulated-environment sense.

The rule also creates a safe re-run model. Because reruns produce new snapshots without modifying existing ones, it is always safe to re-run a task agent after input changes. The previous result is preserved; the new result is additional evidence, not a replacement. Human review of the diff between snapshots is sufficient to determine whether the rerun resolved the issue or introduced new findings.

---

## 4.10 Summary

The Chirality architecture is, at its core, a structure-as-governance system. Its capabilities do not arise from the sophistication of the individual agents but from the structural properties of the constraints under which those agents operate. The filesystem-as-state decision (§4.2) operationalizes the ontological pillar by making the project's domain model directly inspectable and version-controllable. The evidence-first design — mandatory provenance, explicit epistemic labels, immutable audit trails — operationalizes the epistemological pillar by making the reliability of every claim structurally visible rather than inferred. The agent type hierarchy and write scope architecture (§4.5, §4.6) operationalize the praxiological pillar by ensuring that bounded agents cannot exceed their authority, that failures are contained within declared zones, and that human gates are structural rather than advisory. The invariant system and the non-bypassable human gates on lifecycle transitions to CHECKING and ISSUED (§4.4, §4.7) operationalize the axiological pillar by encoding the values of professional responsibility — human authority, evidence over plausibility, and public welfare primacy — as architectural constraints that cannot be relaxed by any agent at any type level. The result is a system whose safety properties are not dependent on agent reliability, but on structural impossibility: the agents cannot approve deliverables, cannot escape their write zones, and cannot hide the epistemic status of their outputs, because the architecture does not permit these things. The governance is in the structure.

---
