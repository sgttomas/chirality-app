# Systems Engineering Design Analysis — Agent Instruction Architecture

This document analyzes the Chirality agent instruction architecture through the lens of eight recognized systems engineering disciplines. The analysis treats the governed agent instruction suite (see [`AGENTS.md`](../AGENTS.md) for the current index; [`REPO_INVENTORY.md`](REPO_INVENTORY.md) for current counts) and their governance documents as an engineered system and traces the SE content to specific files, sections, and invariant IDs.

The architecture rests on four philosophical pillars — ontology, epistemology, praxiology, and axiology — formalized in `DIRECTIVE.md` §2. The claim developed in that section is that the four pillars are generative in an architectural sense: given a commitment to professional accountability in the context of AI agent systems, the SE disciplines identified in this analysis are strongly motivated by the four-pillar commitments and repeatedly selected as the mechanisms that make those commitments operational in Chirality. This analysis provides the evidence for that claim by demonstrating that each SE discipline is present, that each traces to one or more pillars, and that no discipline is found that does not serve a pillar.

**Scope:** The instruction architecture only — agent instruction files (`AGENT_*.md`), governance documents (`docs/`), and the contracts that bind them.

**Method:** Systematic analysis across eight SE disciplines, with evidence traced to specific files, sections, and invariant IDs.

---

## 1. Architecture & Structural Design

### 1.1 Layered Separation of Concerns

The system enforces three distinct separations:

**Instruction vs Execution.** The instruction root (release-managed agent OS) is physically separated from the working root (user-controlled project state). Agents read instructions from one location and write state to another. This is stated in `DIRECTIVE.md` §2.6 and enforced by the runtime architecture.

**Source Truth vs Derived Output.** Deliverable folders (source truth) are structurally isolated from tool roots (derived outputs). Tool roots (`_Aggregation/`, `_Estimates/`, `_Reconciliation/`, `_Change/`, `_Schedule/`) contain agent-produced analysis and snapshots. Source truth contains human-accepted deliverable content. The boundary is enforced by K-WRITE-1: every agent declares its write scope and cannot cross into another zone.

**Authority vs Execution.** The Type 0/1/2 hierarchy separates standards definition from orchestration from bounded task execution. Authority flows downward (Type 0 constrains Type 1, Type 1 constrains Type 2); escalation flows upward. This is stated in `TYPES.md` §4.3 and enforced by agent instruction constraints and human gate authority.

### 1.2 Modularity & Encapsulation

The atomic unit of work is the **production unit folder** — a single deliverable or knowledge type. Each folder is self-contained: identity (`_CONTEXT.md`), lifecycle state (`_STATUS.md`), dependencies (`_DEPENDENCIES.md`, `Dependencies.csv`), references (`_REFERENCES.md`), working memory (`MEMORY.md`), and production documents.

Encapsulation is enforced by:
- K-HIER-1: flat package→deliverable hierarchy (no nesting)
- K-WRITE-1: deliverable-local agents write only within their assigned folder
- WORKING_ITEMS invariant: no cross-deliverable scanning/editing by default

Cross-deliverable operations (reconciliation, aggregation, closure analysis) are explicit, opt-in, and write to isolated tool roots — never to deliverable folders.

### 1.3 Interface Contracts

Interfaces between agents are defined by four mechanisms:

| Interface Type | Artifact | Purpose |
|---------------|----------|---------|
| **Identity contract** | `_CONTEXT.md` | Declares what a deliverable is, who owns it, what it traces to |
| **Dependency contract** | `Dependencies.csv` v3.1 (29 columns) | Machine-readable typed edges between deliverables |
| **Coordination contract** | `_COORDINATION.md` | Project-level choreography semantics |
| **Brief contract** | INIT-TASK briefs | Structured input for Type 2 agents with validated enums |

Every interface is machine-checkable and has explicit preconditions and postconditions (see §7).

---

## 2. Configuration Management & Baseline Control

### 2.1 Version Control as Event Store

`DIRECTIVE.md` §2.2 states: "Version control provides the development record: meaningful diffs for review, reproducibility, rollback, and audits that do not depend on vendor systems or transient chat context. If a decision is not in a versioned file, it does not exist for purposes of reliance."

All project state lives in git-tracked files. There is no external database. This means:
- Every state change produces a reviewable diff
- Every baseline is a git SHA
- Rollback is native (git revert/reset)
- Audit trail requires no special infrastructure

### 2.2 Content-Addressed Approval

K-AUTH-2: "Approvals bind to a specific git SHA. Content change after approval voids the approval."

This is a formal baseline control mechanism. An approved deliverable is frozen at a specific commit. Any subsequent modification invalidates the approval, requiring re-review. K-VAL-1 extends this: "A deliverable is dirty if any governed input has changed since its last approved SHA."

### 2.3 Change Propagation & Staleness

K-STALE-1: "Upstream changes propagate staleness to all transitive dependent deliverables."
K-STALE-2: "Stale items must be triaged by a human before being considered current."

This implements transitive change impact analysis. When a deliverable changes, all downstream dependents (via `Dependencies.csv` edges) are marked stale. Human triage resolves each stale item with one of three modes: no impact (clear flag), needs rework, or needs review. This prevents silent propagation of outdated assumptions.

### 2.4 Immutable Snapshots

K-SNAP-1: "Task agent outputs to tool roots are immutable snapshots. Pointer files (`_LATEST.md`) may be overwritten; snapshot folders must not."

Every analysis run (estimation, closure audit, reconciliation, review) produces a timestamped folder that is never modified. This creates an append-only audit trail. Pointer files provide convenience access to the most recent run without destroying history. The pattern is analogous to event sourcing in data engineering.

---

## 3. Verification & Validation

### 3.1 The V-Model

The system implements a classic V-model: decomposition down the left side, integration and verification up the right.

**Decomposition (left leg)** — `AGENT_DECOMP_BASE.md` defines a 7-gate protocol:

| Phase | Direction | Activity | Gate |
|-------|-----------|----------|------|
| 1. Intake | Down | Capture source material | "Does this reflect the source?" |
| 2. Normalize | Down | Source → atomic units + vocabulary | "Are units and classifications correct?" |
| 3. Objectives | Down | Derive success criteria | "Do objectives represent success?" |
| 4. Partitions | Down | Flat groupings (no overlap, no gaps) | "Is each unit in exactly one partition?" |
| 5. Production Units | Down | Operationalize partitions | "Are granularity and types acceptable?" |

**Integration and verification (right leg):**

| Phase | Direction | Activity | Gate |
|-------|-----------|----------|------|
| 6. Coverage | Up | Prove completeness; surface gaps | "Are coverage and open issues acceptable?" |
| 7. Publish | Up | Finalize accepted decomposition | "Is this the accepted basis for downstream work?" |

Invariants I1–I10 are maintained throughout. Phase 6 produces machine-checkable Coverage & Telemetry metrics that make decomposition quality measurable across revisions.

### 3.2 Stage-Gate Reviews

`AGENT_REVIEW.md` implements a formal 5-gate review process for lifecycle transitions:

| Gate | Function | Authority |
|------|----------|-----------|
| Gate 1 | Precondition check (lifecycle state, context validity) | Agent validates; human confirms scope |
| Gate 2 | Checklist generation from spec/decomposition/dependencies | Agent derives; human confirms completeness |
| Gate 3 | Findings capture (iterative) | Human provides findings; agent records with evidence |
| Gate 4 | Disposition review | Human rules on all findings (PROPOSAL → human decision) |
| Gate 5 | Lifecycle transition decision | Agent recommends; human approves |

Transition readiness criteria are severity-based:
- **IN_PROGRESS → CHECKING:** All CRITICAL findings must have non-TBD human disposition
- **CHECKING → ISSUED:** All CRITICAL findings RESOLVED; all MAJOR findings RESOLVED or DEFERRED with documented rationale

### 3.3 Coverage Analysis

Three forms of coverage verification exist:

**Decomposition coverage** (DECOMP_BASE Phase 6): Every IN-scope atomic unit mapped to exactly one partition and at least one production unit. Gaps are open issues with stable IDs.

**Dependency coverage** (DEPENDENCIES Function 5): Every active dependency row has evidence (EvidenceFile + SourceRef). Floating nodes (deliverables without an IMPLEMENTS_NODE anchor) generate warnings.

**Review coverage** (REVIEW Gate 2): Checklists are derived from acceptance criteria, objectives, cross-document consistency, dependency satisfaction, and TBD inventory. Each item has a stable ID (AP-NNN, AC-NNN, OC-NNN, XD-NNN, DS-NNN, TB-001).

### 3.4 Traceability

Traceability flows through three mechanisms:

**Scope traceability** (`_CONTEXT.md`): Every deliverable traces to scope items (SOW-IDs), objectives (OBJ-IDs), and the decomposition document.

**Requirement traceability** (`Dependencies.csv` ANCHOR rows): `TRACES_TO_REQUIREMENT` rows connect deliverables to requirements, objectives, and scope items. `IMPLEMENTS_NODE` rows connect deliverables to their parent package/WBS node.

**Provenance traceability** (K-PROV-1): Every extracted dependency row must cite evidence (`EvidenceFile` + `SourceRef` or explicit `location TBD`). Every non-trivial claim in production documents requires a source citation or explicit epistemic label.

The Decomposition Ledger serves as the Requirements Traceability Matrix (RTM) — a machine-checkable table mapping every atomic unit through partitions to production units with objective linkage.

---

## 4. Safety & Reliability Engineering

### 4.1 Fault Containment Zones

The write scope architecture creates formal fault containment:

| Containment Zone | Agents | Failure Impact |
|-----------------|--------|----------------|
| Deliverable-local | WORKING_ITEMS, TASK, DELIVERABLE_TASK, 4_DOCUMENTS, DEPENDENCIES, CHIRALITY_FRAMEWORK, CHIRALITY_LENS | Limited to one production unit folder |
| Tool-root | ORCHESTRATOR, ESTIMATING, AGGREGATION, AUDIT_*, SCHEDULING | Limited to one tool root; source truth untouched |
| Repo (approval-gated) | CHANGE | Requires explicit human approval token per action |
| Read-only | HELP_HUMAN, HELPS_HUMANS, DECOMP_BASE | Zero write impact |

A Type 2 agent failure cannot corrupt source truth — it writes to an isolated tool root or a single deliverable folder. The CHANGE agent's approval gate (APPROVE: / APPROVE_DESTRUCTIVE:) is the sole path from derived output to committed state.

### 4.2 Failure Mode Visibility

The system makes failures explicit rather than preventing them:

| Failure Mode | Design Response | Mechanism |
|-------------|----------------|-----------|
| Missing data | Mark `TBD`; surface as open issue | K-INVENT-1 |
| Conflicting sources | Produce Conflict Table; human rules | K-CONFLICT-1 |
| Invalid inputs | `FAILED_INPUTS` (halt, don't guess) | Type 2 agent convention |
| Unresolvable dependency target | `TargetType=UNKNOWN`; preserve raw reference | DEPENDENCIES Function 2 |
| Missing decomposition | `[WARNING] MISSING_DECOMPOSITION`; skip validation | DEPENDENCIES Pass 1 |
| Lifecycle state violation | Warn, don't block (human decides) | REVIEW Gate 1 |

The pattern: failures are visible findings, not hidden recovery attempts. Every uncertainty is labeled (`FACT`, `ASSUMPTION`, `PROPOSAL`, `TBD`) per `TYPES.md` §10.

### 4.3 Context Sealing

K-SEAL-1: "No Type 2 agent execution before context is sealed and gate-approved by a human."
K-GHOST-1: "Type 2 agent context is limited to folder contents + declared references. No ghost inputs."

These invariants bound what a Type 2 agent can see and when it can run. Context must be explicitly sealed (all inputs declared via `_REFERENCES.md` and deliverable folder contents) and human-approved before any specialist agent executes. This prevents agents from operating on incomplete or undeclared context.

---

## 5. Requirements Engineering

### 5.1 Hierarchical Decomposition & Allocation

The decomposition protocol (`AGENT_DECOMP_BASE.md`) implements formal requirements decomposition:

```
Source Corpus (SOW/Handbook)
  → Atomic Units (normalized, testable statements)
    → Partitions (flat groupings; no overlap; no gaps)
      → Production Units (bounded work items with typed artifacts)
```

Allocation is explicit: every IN-scope atomic unit maps to exactly one partition (I4) and at least one production unit (I7, best-effort). The Decomposition Ledger is the formal allocation record.

### 5.2 Requirements Traceability Matrix

The system implements an RTM through three layers:

1. **Decomposition Ledger:** Maps atomic units → partitions → production units → objectives. Machine-checkable. Required columns: UnitID, InOutStatus, PartitionID, ProductionUnitID(s), ObjectiveID(s).

2. **ANCHOR rows in Dependencies.csv:** `IMPLEMENTS_NODE` (exactly one per deliverable) traces to parent package. `TRACES_TO_REQUIREMENT` (zero or more) traces to scope items, objectives, requirements.

3. **`_CONTEXT.md` Scope Traceability section:** Links each deliverable to its source scope items and objectives.

### 5.3 Acceptance Criteria Allocation

`_CONTEXT.md` includes an explicit "Acceptance Criteria" section containing pass/fail conditions derived from the decomposition document. Created by PREPARATION from decomposition metadata. Verified by REVIEW at Gate 2 (checklist generation) and Gate 5 (transition readiness).

---

## 6. Control Theory

### 6.1 The Control Loop

The system implements a closed-loop feedback control system across sessions:

```
ORCHESTRATOR (Plant Setup)
  → WORKING_ITEMS (Actuator — produces content)
    → DEPENDENCIES rerun (Sensor — updates dependency state)
      → RECONCILIATION (Comparator — surfaces deviations)
        → CHANGE (Output — commits to baseline)
          → ORCHESTRATOR scan (Feedback — reports new state)
```

**Control variables and set points:**

| Controlled Variable | Set Point | Sensor | Actuator |
|--------------------|-----------|--------|----------|
| Lifecycle state | ISSUED | `_STATUS.md` | REVIEW gate |
| Dependency closure | All active deps satisfied | `Dependencies.csv` | RECONCILIATION |
| Decomposition fidelity | Zero unassigned units | Decomposition Ledger | Human correction |
| Work availability | No blocked deliverables | Blocker analysis | Tier sequencing |
| Artifact completeness | All anticipated artifacts present | Folder scan | WORKING_ITEMS |

### 6.2 Open-Loop vs Closed-Loop Segments

**Open-loop (within a session):** WORKING_ITEMS produces content within a single deliverable without cross-deliverable feedback. Bounded by deliverable scope and session objective.

**Closed-loop (across sessions):** The handoff mechanism (`NEXT_INSTANCE_STATE.md`) carries state between sessions. DEPENDENCIES rerun after content changes updates the dependency graph. RECONCILIATION detects integration defects. ORCHESTRATOR scan computes work availability for the next tier.

### 6.3 Human Authority as the Halting Condition

ORCHESTRATOR invariant: "Human authority is the halting condition."

Every control loop iteration requires human confirmation at gates. The system cannot autonomously advance tiers, approve deliverables, or resolve conflicts. Human gates function as the decision authority in the control loop — the system proposes; the human decides whether to continue, hold, or redirect.

---

## 7. Formal Methods

### 7.1 Invariant System

The architecture defines three layers of formally stated invariants:

**I1–I10 (Decomposition invariants):** Structural constraints on decomposition (flat partitions, no gaps, stable IDs, deterministic coupling, vocabulary discipline). Enforced by decomposition agents; verified by AUDIT_DECOMP.

**R1–R9 (Workflow design requirements):** Behavioral constraints on all agents (human decision rights, straight-through tasks, write quarantine, immutable snapshots, provenance, no invention, conflict surfacing, brief-driven execution, hygienic publication). Enforced by agent instructions.

**K-* (System-wide invariants):** 21 named, stable invariants covering hierarchy, authority, sealing, dependencies, status, staleness, gates, merge, provenance, invention, conflicts, claim strength, write scope, and snapshots. Defined in `CONTRACT.md` with enforcement points.

### 7.2 Preconditions and Postconditions

Each ORCHESTRATOR function has explicit pre/postconditions:

| Function | Precondition | Postcondition |
|----------|-------------|---------------|
| 1. Initialize | Decomposition document exists | `_COORDINATION.md` exists; coordination representation recorded |
| 2. Scaffold | Function 1 complete; tool roots exist | All deliverables initialized; semantic artifacts generated |
| 3. Scan & Report | Deliverables have `_STATUS.md` | State reported; blockers computed (if mode enabled) |
| 4. Estimating | BOE + INDEX.md + price sources exist | Estimation snapshots per tier |
| 5. Control Loop | Function 1 complete | Handoff artifacts created; ownership boundary clear |

Type 2 agents enforce preconditions as input validation: invalid inputs → `FAILED_INPUTS` (halt). Missing optional data → continue with `TBD` marking and warnings.

### 7.3 Type System

The architecture defines a formal type system through enumerated domains:

**Decomposition ontology:**
```
AtomicUnit    = {id, statement, status: IN|OUT|TBD, sourceRef}
Partition     = {id, name, scopeDesc, inclusions, exclusions}
ProductionUnit = {id, name, parentPartition, type, responsible, artifacts}
Objective     = {id, statement, mappedUnits}
```

**Dependency type system:**
```
DependencyClass  : ANCHOR | EXECUTION
AnchorType       : IMPLEMENTS_NODE | TRACES_TO_REQUIREMENT | NOT_APPLICABLE
Direction        : UPSTREAM | DOWNSTREAM
DependencyType   : PREREQUISITE | INTERFACE | HANDOVER | CONSTRAINT | ENABLES | OTHER
TargetType       : DELIVERABLE | PACKAGE | WBS_NODE | REQUIREMENT | DOCUMENT | EQUIPMENT | EXTERNAL | UNKNOWN
Confidence       : HIGH | MEDIUM | LOW
Origin           : DECLARED | EXTRACTED
Explicitness     : EXPLICIT | IMPLICIT
Status           : ACTIVE | RETIRED
SatisfactionStatus : TBD | PENDING | IN_PROGRESS | SATISFIED | WAIVED | NOT_APPLICABLE
```

**Review type system:**
```
ReviewType        : SELF_CHECK | PEER_REVIEW | IDC | INDEPENDENT_VERIFICATION
FindingSeverity   : CRITICAL | MAJOR | MINOR | OBSERVATION
FindingDisposition : ACCEPT_AS_IS | REVISE | DEFER | NOT_APPLICABLE | WITHDRAWN
FindingStatus     : OPEN | RESOLVED | DEFERRED | WITHDRAWN
```

**Epistemic labels:**
```
EpistemicLabel : FACT | ASSUMPTION | PROPOSAL | TBD
```

These types are not merely documentation — they constrain agent behavior through enum validation, schema checking, and conditional logic within agent protocols.

### 7.4 The State Machine

The deliverable lifecycle is a formal state machine with authorized transition actors:

```
OPEN ──[PREPARATION]──→ INITIALIZED ──[4_DOCUMENTS/DOMAIN_DOCUMENTS]──→
  SEMANTIC_READY ──[CHIRALITY_FRAMEWORK]──→ IN_PROGRESS ──[human]──→
    CHECKING ──[REVIEW + human approval]──→ ISSUED ──[human]──→
```

K-STATUS-1 makes `_STATUS.md` the canonical state indicator. Transitions are forward-only under normal operation. Each transition is recorded in the append-only History section with date, actor, and rationale.

---

## 8. Human Factors & Decision Authority

### 8.1 Decision Authority Allocation

The system explicitly separates what humans decide from what agents execute:

**Human-owned decisions (K-AUTH-1, `DIRECTIVE.md` §3.2):**
- Scope and boundary decisions
- Selection of governing codes, standards, design basis
- Hazard and risk acceptance
- Conflict adjudication and rulings
- Approval, issuance, signature

**Agent-executable actions (bounded, brief-driven):**
- Scaffolding and initialization
- Bulk document drafting
- Dependency extraction and register maintenance
- Coverage analysis and reconciliation reporting
- Estimation and scheduling (derived, not authoritative)
- Aggregation and collation

The split is enforced by K-AUTH-1 ("Only humans author binding approval records") and K-BIND-1 ("Approvals are always binding and only binding").

### 8.2 Cognitive Load Management

The architecture reduces cognitive load through:

**Epistemic transparency.** Every claim is labeled: FACT, ASSUMPTION, PROPOSAL, or TBD. The human does not need to guess whether a value is grounded or inferred — the label tells them. Enforced by K-INVENT-1 and K-CONFLICT-1.

**Conflict surfacing.** Contradictions are not resolved silently. The Conflict Table pattern (ConflictID, Key, Contenders, ProposedAuthority, HumanRuling=TBD) presents disagreements in a structured format that requires minimal effort to adjudicate.

**Working memory externalization.** `MEMORY.md` (per deliverable) and `NEXT_INSTANCE_STATE.md` (per session) externalize context that would otherwise be lost between sessions. Organized by semantic topic: Key Decisions, Domain Context, Open Items, Proposal History, Interface Notes.

**Vocabulary canonicalization.** The Vocabulary Map (required in every decomposition) defines canonical terms and maps synonyms. This prevents semantic drift across team members and sessions.

**Flat hierarchy.** K-HIER-1 enforces a single level of nesting (packages → deliverables). The human can comprehend the full project structure without navigating a deep tree.

### 8.3 Configurable Rigor

K-GATE-1: "Gates are dynamic per project instance. Minimum required gates: seal transition + pipeline run approval. Additional gates are project-configurable."

The coordination representation is human-chosen (`SCHEDULE_FIRST` | `DECLARED` | `FULL_GRAPH`), allowing teams to match system rigor to project needs. Dependency tracking mode (`NOT_TRACKED` | `DECLARED` | `FULL_GRAPH`) similarly scales — when set to `NOT_TRACKED`, the system does not compute blockers, avoiding false precision.

---

## 9. Cross-Cutting Patterns

### 9.1 Tree x DAG Knowledge Architecture

The dependency model separates structural identity from execution coupling:

- **Tree (ANCHOR rows):** Connects deliverables to the definition hierarchy (WBS/SSOW nodes, requirements). Exactly one `IMPLEMENTS_NODE` per deliverable. Stable, normative — defines what a deliverable IS.
- **DAG (EXECUTION rows):** Captures information flow between deliverables (prerequisites, interfaces, handovers, constraints). Many-to-many. Current, operative — defines what a deliverable NEEDS.

This dual-graph model prevents scope drift (tree is stable) while supporting dynamic execution planning (DAG evolves).

### 9.2 Distributed Authority with On-Demand Aggregation

K-DEP-1: "Deliverable-local `_DEPENDENCIES.md` and `Dependencies.csv` are authoritative. There is no central dependency graph; aggregation is on-demand."

Each deliverable maintains its own dependency register. There is no central database. Cross-deliverable views (closure analysis, aggregation) are produced on demand by read-only agents and materialized as immutable snapshots in tool roots. This eliminates synchronization burden — the graph is always current because it is derived from files, not copied into a database.

### 9.3 Evidence-First Epistemology as Safety Mechanism

The epistemic controls (K-PROV-1, K-INVENT-1, K-CONFLICT-1) function as a safety mechanism:

- **K-PROV-1** (provenance mandatory) ensures that every claim can be audited back to its source
- **K-INVENT-1** (no invention) ensures that gaps in evidence are visible, not papered over
- **K-CONFLICT-1** (conflicts surfaced) ensures that disagreements reach the human decision-maker

Together, these prevent the most common failure mode in LLM-assisted systems: plausible-sounding output that is not grounded in evidence. The system does not try to prevent hallucination — it requires provenance, making unsupported claims structurally visible.

### 9.4 Multi-Layer Enforcement

`CONTRACT.md` §2 defines four enforcement layers:

| Layer | Timing | Invariants Checked |
|-------|--------|-------------------|
| Agent instructions (design-time; constrains intent, not guaranteed behavior) | When instruction files are written | K-GHOST-1, K-WRITE-1, K-SNAP-1, K-PROV-1, K-INVENT-1, K-CONFLICT-1, K-DEP-1, K-DEP-2 |
| ORCHESTRATOR (runtime) | During workspace initialization and pipeline execution | K-SEAL-1, K-GATE-1, K-HIER-1 |
| Human review (gate) | At every gate decision | K-AUTH-1, K-AUTH-2, K-BIND-1, K-STALE-2, K-MERGE-1, K-VAL-1, K-STATUS-1 |
| Future tooling (automated) | Continuous/on-demand | K-STALE-1, K-VAL-1, K-MERGE-1, K-AUTH-2, K-DEP-2 |

This defense-in-depth strategy ensures that no single enforcement failure can compromise system integrity.

---

## 10. Assessment

The systems engineering content of this architecture is not incidental — it is the architecture. The instruction files are formal specifications that define interfaces, state machines, invariants, preconditions, postconditions, containment zones, and authority boundaries. The governance documents (`DIRECTIVE.md`, `SPEC.md`, `TYPES.md`, `CONTRACT.md`) form a coherent specification hierarchy: intent → physical structures → vocabulary → binding invariants.

What distinguishes this from a conventional agent system is that the SE disciplines are not bolted on as compliance artifacts — they are the mechanism by which agents coordinate, the means by which failures are contained, and the basis on which humans maintain authority. The Type 0/1/2 hierarchy, the write scope architecture, the invariant system, the gate-controlled workflows, and the evidence-first epistemology are all instances of classical SE patterns adapted to the specific challenge of governing LLM-based agents in professional and regulated environments.

### 10.1 The Generative Relationship

The eight SE disciplines identified in this analysis were not selected from a handbook and applied to the architecture. They emerged as one coherent way of operationalizing the four-pillar commitments formalized in `DIRECTIVE.md` §2.

When the architecture committed to stable, inspectable state in git-tracked files (ontology), configuration management and baseline control followed as the natural mechanisms for maintaining integrity over versioned state. When it committed to mandatory provenance and epistemic transparency (epistemology), verification and validation, formal methods, and the evidence-first patterns followed as the mechanisms that make the grounds for reliance auditable. When it committed to bounded, gate-controlled execution (praxiology), safety engineering, control theory, and the fault containment architecture followed as the mechanisms that contain the behavior of probabilistic agents. When it committed to non-delegable professional responsibility (axiology), human factors design and decision authority allocation followed as the mechanisms that preserve human accountability.

The mapping is not coincidental:

| Pillar Commitment | SE Disciplines That Follow |
|---|---|
| Ontology (stable, inspectable state) | Architecture and structural design; configuration management |
| Epistemology (evidence-first, auditable knowledge) | Verification and validation; formal methods; requirements traceability |
| Praxiology (bounded, gate-controlled execution) | Safety and reliability engineering; control theory |
| Axiology (non-delegable professional responsibility) | Human factors; decision authority allocation |

Each SE discipline serves one or more pillars. No SE discipline was found that does not serve a pillar. In Chirality, the SE disciplines are the formal expression of the philosophical commitments and the principal mechanisms by which those commitments are made architecturally real.

This means that systems engineering, in the context of professional AI agent governance, is not incidental in Chirality. It is the architecture's chosen means of taking professional accountability seriously. The four pillars strongly predict what kinds of SE disciplines should be present; this analysis confirms that prediction within this implementation.

---

*Produced by systematic analysis of the governed agent instruction suite and governance documents in the Chirality App repository. See `AGENTS.md` for the current agent index.*
