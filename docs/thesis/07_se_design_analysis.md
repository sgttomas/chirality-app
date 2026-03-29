# Chapter 7 — Systems Engineering Design Analysis

---

## 7.1 Introduction and Method

This chapter examines the Chirality agent instruction architecture through the lens of eight recognized systems engineering (SE) disciplines. The analysis treats the agent instruction files, governance documents, and the contracts that bind them as a coherent engineered system, and demonstrates that the SE disciplines embedded in that system are not compliance artifacts applied after the fact but are, in each case, the operative mechanism by which the system achieves its objectives.

The reference framework for SE discipline definitions throughout this chapter is the INCOSE Systems Engineering Handbook [CITE:INCOSE2023]. The analytical method is systematic examination with evidence traced to specific files, governance sections, and invariant identifiers drawn from the Chirality Contract document (`CONTRACT.md`). The full invariant catalog is reproduced in Appendix A; the complete agent inventory is provided in Appendix B.

Chapter 3 of this thesis established the four-pillar philosophical framework — ontology, epistemology, praxiology, and axiology — that governs all design decisions in Chirality. A recurring observation of this chapter is that each SE discipline, when instantiated in the Chirality architecture, serves one or more of those four pillars, and that the epistemology pillar is served most densely: configuration management, verification and validation, formal methods, and the evidence-first epistemology pattern described in Section 7.10 all draw their functional justification from the same epistemic premise — that the grounds for professional reliance must be structurally visible and auditable.

The scope of this analysis is the instruction architecture only: agent instruction files (`AGENT_*.md`), governance documents (`docs/`), and the invariant contracts that bind agent behavior. The analysis proceeds across eight disciplines — architecture and structural design, configuration management, verification and validation, safety and reliability engineering, requirements engineering, control theory, formal methods, and human factors — followed by a cross-cutting patterns synthesis and a concluding assessment.

---

## 7.2 Architecture and Structural Design

Architecture and structural design concerns the decomposition of a system into subsystems with defined boundaries, interfaces, and responsibilities, and the arrangement of those subsystems to achieve system-level properties [CITE:INCOSE2023]. In Chirality, structural design operates at three levels: separation of concerns, modularity and encapsulation, and interface contracts.

### 7.2.1 Layered Separation of Concerns

The Chirality architecture enforces three distinct separations, each of which eliminates a category of coupling failure.

**Instruction versus execution.** The instruction root — a release-managed agent operating system distributed with the application — is physically separated from the working root, the user-controlled filesystem directory where agents read and write project state. Agents read their governing instructions from one location and write state to another. This separation, stated in `DIRECTIVE.md` §2.6 and enforced by the runtime architecture, ensures that the rules governing agent behavior are stable across projects and releases while project execution remains fully filesystem-native. An agent cannot modify its own governing instructions during execution because those instructions reside in a separate, write-protected location.

**Source truth versus derived output.** Deliverable folders — the source truth of the project — are structurally isolated from tool roots, which contain agent-produced analysis and snapshots. Tool roots (`_Aggregation/`, `_Estimates/`, `_Reconciliation/`, `_Change/`, `_Schedule/`) are explicitly designated zones for derived output. Source truth contains only human-accepted deliverable content. The boundary is enforced by invariant K-WRITE-1: every agent declares its write scope in its header block, and no agent may write outside that declared zone. This prevents derived analysis from silently contaminating the authoritative project record.

**Authority versus execution.** The Type 0/1/2 hierarchy separates standards definition (Type 0 — Architect agents), orchestration (Type 1 — Manager agents), and bounded task execution (Type 2 — Specialist agents). Authority flows downward: Type 0 constraints govern Type 1 behavior; Type 1 orchestration governs Type 2 task scope. Escalation flows upward. No agent of any type can exceed its authority tier, and no agent of any type can bypass a human gate. This separation, defined in `TYPES.md` §4.3 and enforced by agent instruction constraints and human gate authority, provides a formal model of delegation that mirrors classical SE authority hierarchy [CITE:SE_textbook].

### 7.2.2 Modularity and Encapsulation

The atomic unit of work in the Chirality architecture is the **production unit folder** — a single deliverable or knowledge type. Each folder is self-contained, carrying identity (`_CONTEXT.md`), lifecycle state (`_STATUS.md`), dependency registers (`_DEPENDENCIES.md`, `Dependencies.csv`), references (`_REFERENCES.md`), working memory (`MEMORY.md`), and production documents. This encapsulation pattern, in which every module carries its own state and interface declarations internally, is consistent with information-hiding principles applied to system decomposition [CITE:SE_textbook].

Encapsulation is formally enforced by three invariant mechanisms. K-HIER-1 mandates a flat package-to-deliverable hierarchy — no nesting — ensuring that the system can never develop hidden coupling through intermediate levels. K-WRITE-1 restricts deliverable-local agents to writing only within their assigned folder. The WORKING_ITEMS invariant extends this by prohibiting cross-deliverable scanning or editing by default. The result is that a fault in any deliverable-local agent is structurally confined to that deliverable's folder; it cannot propagate to adjacent deliverables without an explicit cross-deliverable operation.

Cross-deliverable operations — reconciliation, aggregation, closure analysis — are explicit, opt-in, and write to isolated tool roots rather than to deliverable folders. This design ensures that integration operations are always auditable as distinct events in the project record, rather than being conflated with production work.

This structural design directly serves the ontology pillar of the Chirality philosophy (Chapter 3): the folder structure is the project structure, the file contents are the project state, and the ontological model is directly inspectable by humans, agents, and tools without a translation layer.

### 7.2.3 Interface Contracts

Interfaces between agents are defined by four mechanisms, each with explicit semantics.

| Interface Type | Artifact | Purpose |
|---|---|---|
| Identity contract | `_CONTEXT.md` | Declares what a deliverable is, who owns it, and what it traces to |
| Dependency contract | `Dependencies.csv` v3.1 (29 columns) | Machine-readable typed edges between deliverables |
| Coordination contract | `_COORDINATION.md` | Project-level choreography semantics |
| Brief contract | INIT-TASK briefs | Structured input for Type 2 agents with validated enumerations |

Every interface is machine-checkable and carries explicit preconditions and postconditions. The dependency contract, discussed further in Section 7.8.3 in the context of the formal type system, defines a 29-column schema with fully enumerated type domains covering dependency class, anchor type, direction, dependency type, target type, confidence, origin, explicitness, status, and satisfaction status. This level of interface specification is characteristic of safety-critical systems design, where ambiguous interfaces are a primary source of integration failure [CITE:SE_textbook].

The brief contract deserves particular attention from an architectural standpoint. By requiring that Type 2 agents receive structured inputs with validated enumerations rather than free-text instructions, the architecture eliminates a category of agent behavior variability at the interface. The brief is not a communication convenience — it is a formal input specification.

---

## 7.3 Configuration Management and Baseline Control

Configuration management (CM) is the discipline of establishing and maintaining the integrity and traceability of a system's configuration items throughout the system lifecycle [CITE:INCOSE2023]. In Chirality, CM is not implemented as an add-on governance layer; it is the foundational architectural mechanism. The choice of git-tracked plain files as the sole state representation means that every CM function — baseline establishment, change control, status accounting, and audit — is natively provided by the version control system.

This design directly serves the epistemology pillar (Chapter 3): the principle that a decision or state change that is not recorded in a versioned file does not exist for purposes of reliance is an epistemological commitment, not merely an operational convenience.

### 7.3.1 Version Control as Event Store

`DIRECTIVE.md` §2.2 states: "Version control provides the development record: meaningful diffs for review, reproducibility, rollback, and audits that do not depend on vendor systems or transient chat context. If a decision is not in a versioned file, it does not exist for purposes of reliance."

All project state lives in git-tracked files. There is no external database. This architectural commitment produces four CM properties without requiring additional infrastructure: every state change produces a reviewable diff; every baseline is addressable by a git SHA; rollback is native via standard git operations; and the audit trail requires no special tooling. The design eliminates the synchronization burden that accompanies any architecture in which system state is distributed across a filesystem and a separate database.

The analogy to event sourcing in data engineering is direct: the git commit log is an append-only record of state transitions, and any historical project state can be reconstructed by replaying commits to any point in the history.

### 7.3.2 Content-Addressed Approval

Invariant K-AUTH-2 states: "Approvals bind to a specific git SHA. Content change after approval voids the approval." Invariant K-VAL-1 extends this: "A deliverable is dirty if any governed input has changed since its last approved SHA."

This constitutes a formal baseline control mechanism. An approved deliverable is frozen at a specific commit. Any subsequent modification to that deliverable's content invalidates the approval, requiring re-review before the deliverable can be relied upon. The integrity of the approval relationship is mechanically verifiable — it does not depend on process discipline or trust in the workflow. This property is significant in regulated environments, where the traceability of approval decisions to specific artifact versions is a compliance requirement, not merely best practice.

Content-addressed approval also serves the axiology pillar: it is an architectural enforcement of the principle that professional responsibility attaches to a specific, identified artifact, not to a deliverable concept in the abstract.

### 7.3.3 Change Propagation and Staleness Detection

K-STALE-1 states: "Upstream changes propagate staleness to all transitive dependent deliverables." K-STALE-2 states: "Stale items must be triaged by a human before being considered current."

This mechanism implements transitive change impact analysis as a first-class architectural function. When a deliverable changes, all downstream dependents — identified through the directed `Dependencies.csv` edge graph — are marked stale. Human triage resolves each stale item through one of three modes: no impact (flag cleared), needs rework, or needs review. This prevents the silent propagation of outdated assumptions through a dependency chain, which is among the most consequential failure modes in complex deliverable systems [CITE:Leveson2011].

The human triage requirement of K-STALE-2 is an intentional design decision. The system does not attempt to automatically classify the impact of upstream changes, because doing so would require the kind of engineering judgment that the axiology pillar explicitly reserves for qualified professionals.

### 7.3.4 Immutable Snapshots

K-SNAP-1 states: "Task agent outputs to tool roots are immutable snapshots. Pointer files (`_LATEST.md`) may be overwritten; snapshot folders must not."

Every analysis run — estimation, closure audit, reconciliation, review — produces a timestamped folder that is never subsequently modified. Pointer files provide convenience access to the most recent run without overwriting history. This append-only pattern ensures that the analytical record is complete: the progression of analysis across successive runs is preserved, enabling retrospective audit of how conclusions evolved. It also ensures that reruns are safe — an agent cannot corrupt a previous run by overwriting it.

---

## 7.4 Verification and Validation

Verification determines whether a system has been built correctly relative to its specifications; validation determines whether the correct system has been built relative to stakeholder needs [CITE:INCOSE2023]. In Chirality, verification and validation are implemented through a V-model decomposition and integration structure, formal stage-gate reviews, three complementary forms of coverage analysis, and a multi-layer traceability architecture.

### 7.4.1 The V-Model

The system implements a classic V-model: decomposition down the left side and integration with verification up the right. `AGENT_DECOMP_BASE.md` defines a seven-gate protocol that maps directly onto this structure.

**Decomposition (left leg)** — five phases drive requirements downward from source corpus to testable production units:

| Phase | Direction | Activity | Verification Question |
|---|---|---|---|
| 1. Intake | Downward | Capture source material | Does this reflect the source? |
| 2. Normalize | Downward | Source to atomic units and vocabulary | Are units and classifications correct? |
| 3. Objectives | Downward | Derive success criteria | Do objectives represent success? |
| 4. Partitions | Downward | Flat groupings with no overlap and no gaps | Is each unit in exactly one partition? |
| 5. Production Units | Downward | Operationalize partitions | Are granularity and types acceptable? |

**Integration and verification (right leg)** — two phases drive evidence upward toward a validated, publishable decomposition:

| Phase | Direction | Activity | Verification Question |
|---|---|---|---|
| 6. Coverage | Upward | Prove completeness; surface gaps | Are coverage and open issues acceptable? |
| 7. Publish | Upward | Finalize accepted decomposition | Is this the accepted basis for downstream work? |

Decomposition invariants I1 through I10 are maintained throughout all phases. Phase 6 produces machine-checkable coverage and telemetry metrics that make decomposition quality measurable and comparable across revisions.

The V-model mapping is not metaphorical. The decomposition protocol enforces bidirectional traceability: every production unit can be traced back to the atomic unit and source document that generated it, and every source requirement can be traced forward to the production unit that implements it. This is the formal basis for the Requirements Traceability Matrix described in Section 7.6.2.

### 7.4.2 Stage-Gate Reviews

`AGENT_REVIEW.md` implements a formal five-gate review process governing all lifecycle state transitions. Each gate has an assigned function and a defined authority allocation:

| Gate | Function | Authority |
|---|---|---|
| Gate 1 | Precondition check (lifecycle state, context validity) | Agent validates; human confirms scope |
| Gate 2 | Checklist generation from specification, decomposition, and dependencies | Agent derives; human confirms completeness |
| Gate 3 | Findings capture (iterative) | Human provides findings; agent records with evidence |
| Gate 4 | Disposition review | Human rules on all findings (PROPOSAL transitions to human decision) |
| Gate 5 | Lifecycle transition decision | Agent recommends; human approves |

Transition readiness criteria are severity-graded. The IN_PROGRESS to CHECKING transition requires that all CRITICAL findings have non-TBD human dispositions. The CHECKING to ISSUED transition requires that all CRITICAL findings be RESOLVED and all MAJOR findings be either RESOLVED or formally DEFERRED with documented rationale.

The five-gate structure is an instantiation of the stage-gate principle in SE practice [CITE:INCOSE2023]: consequential decisions are partitioned into sequential checkpoints at which accumulated evidence is evaluated before progression. In the Chirality implementation, no gate can be bypassed — K-AUTH-1 reserves the transition decision to a human at Gate 5, and the praxiology pillar (Chapter 3) enforces this as a structural property of the architecture, not merely a procedural guideline.

### 7.4.3 Coverage Analysis

Three complementary forms of coverage verification exist in the Chirality system.

**Decomposition coverage** (DECOMP_BASE Phase 6) verifies that every in-scope atomic unit is mapped to exactly one partition and at least one production unit. Gaps are recorded as open issues with stable identifiers. Coverage is reported as a machine-checkable metric across the decomposition ledger.

**Dependency coverage** (DEPENDENCIES Function 5) verifies that every active dependency row has associated evidence — an `EvidenceFile` field and a `SourceRef` field, or an explicit `location TBD` marker. Floating nodes, deliverables without an `IMPLEMENTS_NODE` anchor row, generate structured warnings. This form of coverage serves K-PROV-1: the provenance of every dependency claim must be traceable to a source.

**Review coverage** (REVIEW Gate 2) verifies that the review checklist addresses acceptance criteria, objectives, cross-document consistency, dependency satisfaction, and TBD inventory. Each checklist item carries a stable identifier from one of six namespaces (AP-NNN, AC-NNN, OC-NNN, XD-NNN, DS-NNN, TB-001), enabling traceability of review findings to specific checklist items and therefore to the requirements or criteria they address.

The three forms of coverage are complementary rather than redundant. Decomposition coverage addresses structural completeness; dependency coverage addresses evidential grounding; review coverage addresses acceptance criterion satisfaction. Together, they implement a multi-axis verification regime in which no single coverage measure can be satisfied while the others are deficient.

### 7.4.4 Traceability Architecture

Traceability flows through three mechanisms that together form a complete chain from source requirement to delivered artifact.

**Scope traceability** (`_CONTEXT.md`): Every deliverable traces to scope items (SOW-IDs), objectives (OBJ-IDs), and the decomposition document. This is the deliverable-level instance of the traceability relationship.

**Requirement traceability** (`Dependencies.csv` ANCHOR rows): `IMPLEMENTS_NODE` rows connect each deliverable to its parent package or WBS node (exactly one per deliverable). `TRACES_TO_REQUIREMENT` rows connect deliverables to requirements, objectives, and scope items (zero or more per deliverable). Together, these anchor rows form the machine-checkable backbone of the Requirements Traceability Matrix (RTM).

**Provenance traceability** (K-PROV-1): Every extracted dependency row must cite its evidence — `EvidenceFile` plus `SourceRef`, or an explicit `location TBD` marker. Every non-trivial claim in production documents requires a source citation or explicit epistemic label. This extends traceability from the structural (deliverable-to-requirement) to the epistemic (claim-to-source).

The Decomposition Ledger serves as the system-level RTM: a machine-checkable table mapping every atomic unit through partitions to production units with objective linkage. The cross-reference from Chapter 5 (Epistemic Architecture) is direct — the traceability architecture is the implementation of the epistemic pillar's provenance mandate.

---

## 7.5 Safety and Reliability Engineering

Safety engineering addresses the prevention of conditions that could cause harm, loss, or mission failure [CITE:Leveson2011]. In agent-based systems, the analogous concern is the prevention of conditions that could cause erroneous, unsanctioned, or unauditable agent action. The Chirality architecture approaches this through three mechanisms: fault containment zones that structurally bound the impact of any agent failure, a failure mode visibility protocol that makes failures explicit rather than hiding them in recovery logic, and context sealing invariants that prevent agents from operating on undeclared or unvalidated inputs.

### 7.5.1 Fault Containment Zones

The write scope architecture creates formal fault containment zones with precisely bounded failure impact:

| Containment Zone | Assigned Agents | Maximum Failure Impact |
|---|---|---|
| Deliverable-local | WORKING_ITEMS, TASK, 4_DOCUMENTS, DEPENDENCIES, CHIRALITY_FRAMEWORK, CHIRALITY_LENS | Limited to one production unit folder |
| Tool-root | ORCHESTRATOR, ESTIMATING, AGGREGATION, AUDIT_*, SCHEDULING | Limited to one tool root; source truth untouched |
| Repository (approval-gated) | CHANGE | Requires explicit human approval token per action |
| Read-only | HELP_HUMAN, HELPS_HUMANS, DECOMP_BASE | Zero write impact |

This zoning architecture is a direct application of the fault containment region concept in safety engineering [CITE:Leveson2011]: the system is partitioned such that a failure within any zone cannot propagate to adjacent zones without crossing a boundary enforced by an independent mechanism. In the Chirality implementation, the boundary between the tool-root zone and source truth is enforced by K-WRITE-1, not by process discipline — an agent structurally cannot write outside its declared write scope.

The CHANGE agent occupies a distinctive position in this architecture. It is the sole path from derived analysis output to committed repository state, and every action requires an explicit human approval token (APPROVE: or APPROVE_DESTRUCTIVE:). A Type 2 agent failure cannot corrupt source truth because no Type 2 agent has a write path to source truth. The CHANGE agent's approval gate is the sole crossing point, and it requires active human authorization.

### 7.5.2 Failure Mode Visibility

The Chirality safety architecture makes failures explicit rather than attempting to prevent them or hide them in recovery logic. This reflects a key principle of safety-critical systems design: a system that fails visibly and detectably is safer than a system that attempts silent recovery [CITE:Leveson2011].

| Failure Mode | Design Response | Mechanism |
|---|---|---|
| Missing data | Mark `TBD`; surface as open issue | K-INVENT-1 |
| Conflicting sources | Produce Conflict Table; human rules | K-CONFLICT-1 |
| Invalid inputs | `FAILED_INPUTS` (halt, do not guess) | Type 2 agent convention |
| Unresolvable dependency target | `TargetType=UNKNOWN`; preserve raw reference | DEPENDENCIES Function 2 |
| Missing decomposition | `[WARNING] MISSING_DECOMPOSITION`; skip validation | DEPENDENCIES Pass 1 |
| Lifecycle state violation | Warn, do not block (human decides) | REVIEW Gate 1 |

The consistent pattern is that failures are visible findings, not hidden recovery attempts. Every form of uncertainty is labeled — FACT, ASSUMPTION, PROPOSAL, or TBD — per the epistemic label system defined in `TYPES.md` §10 and described further in Section 7.8.3 of this chapter. An agent that encounters missing data does not default-fill or infer; it marks the gap and surfaces it as an open issue. This behavior is enforced by K-INVENT-1 as a structural constraint across all agent types.

The `FAILED_INPUTS` halt behavior is particularly significant. When a Type 2 agent receives inputs that fail validation, the correct response is to halt and report the specific validation failure, not to attempt execution on invalid data. This fail-fast behavior ensures that input validation failures are detected at the earliest possible point in the workflow, before they can propagate into outputs.

### 7.5.3 Context Sealing

Two invariants bound what a Type 2 agent can see and when it is permitted to run.

K-SEAL-1 states: "No Type 2 agent execution before context is sealed and gate-approved by a human." The sealing operation requires that all inputs be explicitly declared via `_REFERENCES.md` and deliverable folder contents, and that a human confirm the sealed context before execution begins. This prevents agents from operating on an incomplete or evolving input set — a condition that, in an LLM-based system, is a primary source of unpredictable behavior.

K-GHOST-1 states: "Type 2 agent context is limited to folder contents and declared references. No ghost inputs." Ghost inputs — sources of information available to an agent at execution time but not declared in the sealed context — are structurally prohibited. The agent may not consult undeclared prior context, informal communications, or any information source not explicitly listed in `_REFERENCES.md`.

Together, K-SEAL-1 and K-GHOST-1 implement a formal context boundary analogous to the environmental control requirements imposed on safety-critical software [CITE:Leveson2011]. The context of execution is defined, bounded, and approved before execution begins.

---

## 7.6 Requirements Engineering

Requirements engineering encompasses the processes of eliciting, analyzing, specifying, verifying, and managing requirements throughout the system lifecycle [CITE:INCOSE2023]. In Chirality, requirements engineering is instantiated as a systematic decomposition protocol, a three-layer traceability matrix, and an explicit acceptance criteria allocation mechanism.

### 7.6.1 Hierarchical Decomposition and Allocation

The decomposition protocol (`AGENT_DECOMP_BASE.md`) implements formal requirements decomposition through four levels of progressive refinement:

```
Source Corpus (scope of work / handbook)
  → Atomic Units (normalized, testable statements)
    → Partitions (flat groupings; no overlap; no gaps)
      → Production Units (bounded work items with typed artifacts)
```

Each level corresponds to a level of requirements abstraction: the source corpus provides the raw requirements input; atomic units are the elementary, normalized, testable statements that result from decomposition; partitions are the functional groupings that structure allocation; and production units are the bounded work items to which requirements are allocated for execution.

Allocation is explicit and machine-verifiable. Invariant I4 mandates that every in-scope atomic unit map to exactly one partition; invariant I7 mandates (best-effort) that every in-scope atomic unit map to at least one production unit. The Decomposition Ledger is the formal allocation record, providing a machine-checkable table of the complete allocation from atomic unit through partition to production unit with objective linkage.

This protocol directly instantiates the requirements decomposition principle [CITE:SE_textbook]: requirements at one level are systematically derived from and traceable to requirements at the level above, and the decomposition is complete (no requirements are lost) and consistent (no requirements conflict).

### 7.6.2 Requirements Traceability Matrix

The system implements a three-layer Requirements Traceability Matrix (RTM) that provides bidirectional traceability from source requirements to delivered artifacts.

**Layer 1 — Decomposition Ledger:** Maps atomic units to partitions to production units to objectives. Machine-checkable. Required columns include UnitID, InOutStatus, PartitionID, ProductionUnitID(s), and ObjectiveID(s). This layer covers the full depth of the requirements hierarchy from source requirement to production unit.

**Layer 2 — ANCHOR rows in `Dependencies.csv`:** `IMPLEMENTS_NODE` rows (exactly one per deliverable) trace each deliverable to its parent package in the WBS. `TRACES_TO_REQUIREMENT` rows (zero or more per deliverable) trace deliverables to scope items, objectives, and requirements. This layer connects the production unit to the structural WBS and to the formal requirement record.

**Layer 3 — `_CONTEXT.md` Scope Traceability section:** Links each deliverable to its source scope items and objectives at the deliverable level. This layer provides human-readable traceability at the point of use — within the deliverable folder itself — without requiring navigation to a separate RTM document.

The three layers are complementary. The Decomposition Ledger provides coverage verification; the ANCHOR rows provide machine-checkable structural linkage; and the `_CONTEXT.md` section provides local, human-accessible traceability. Together, they satisfy the requirement that traceability be complete, consistent, and accessible at the level of abstraction at which it is needed.

### 7.6.3 Acceptance Criteria Allocation

`_CONTEXT.md` includes an explicit Acceptance Criteria section containing pass/fail conditions derived from the decomposition document. This section is created by the PREPARATION agent from decomposition metadata — that is, acceptance criteria are derived systematically from requirements rather than authored independently.

Acceptance criteria are verified at two points in the review process: at Gate 2 (checklist generation), where the REVIEW agent derives a checklist from the acceptance criteria and the human confirms its completeness; and at Gate 5 (transition readiness), where criterion satisfaction is a precondition for the CHECKING to ISSUED transition. This allocation pattern ensures that every acceptance criterion is both derived from requirements (traceability downward) and verified before issuance (verification upward), completing the V-model relationship.

---

## 7.7 Control Theory

Control theory provides the analytical framework for designing systems that maintain desired behavior in the presence of disturbances and feedback [CITE:SE_textbook]. In Chirality, the project execution workflow across sessions instantiates a closed-loop feedback control system with defined control variables, set points, sensors, and actuators.

### 7.7.1 The Control Loop

The system implements a closed-loop feedback control architecture spanning the complete project execution cycle:

```
ORCHESTRATOR (Plant Setup)
  → WORKING_ITEMS (Actuator — produces content)
    → DEPENDENCIES rerun (Sensor — updates dependency state)
      → RECONCILIATION (Comparator — surfaces deviations)
        → CHANGE (Output — commits to baseline)
          → ORCHESTRATOR scan (Feedback — reports new state)
```

Each element of this loop has a defined control function. The ORCHESTRATOR initializes the plant state — the workspace configuration and coordination representation — and provides the periodic scan that closes the loop by reporting current system state. WORKING_ITEMS is the primary actuator, producing content that advances deliverables toward their set points. The DEPENDENCIES rerun after content changes functions as a sensor, updating the dependency state to reflect the new system state. RECONCILIATION is the comparator, differencing actual dependency state against expected dependency state and surfacing deviations as findings. CHANGE commits accepted states to baseline, making the output permanent. The ORCHESTRATOR scan then reports the new baseline state as feedback to the next iteration.

### 7.7.2 Control Variables and Set Points

The system manages five primary control variables, each with a defined set point, sensor, and actuator:

| Controlled Variable | Set Point | Sensor | Actuator |
|---|---|---|---|
| Lifecycle state | ISSUED | `_STATUS.md` | REVIEW gate |
| Dependency closure | All active dependencies satisfied | `Dependencies.csv` | RECONCILIATION |
| Decomposition fidelity | Zero unassigned atomic units | Decomposition Ledger | Human correction |
| Work availability | No blocked deliverables | Blocker analysis | Tier sequencing |
| Artifact completeness | All anticipated artifacts present | Folder scan | WORKING_ITEMS |

The set points are not aspirational targets — they are the preconditions for project completion. A project that has reached its set points across all five variables is, by definition, complete: all deliverables are issued, all dependencies are satisfied, all requirements are allocated, no deliverables are blocked, and all artifacts are present.

The control variable framework also illustrates why the epistemology pillar is so load-bearing. Each sensor in the table reads from a file-based state record. If those records are not accurate — if approvals are not content-addressed, if dependency states are not current, if lifecycle states do not reflect actual deliverable condition — the control system is operating on false sensor readings. The CM mechanisms described in Section 7.3 and the epistemic controls described in Section 7.10 are prerequisites for control system integrity.

### 7.7.3 Open-Loop versus Closed-Loop Segments

The control architecture includes both open-loop and closed-loop segments, serving different functional purposes.

**Open-loop (within a session):** WORKING_ITEMS produces content within a single deliverable without cross-deliverable feedback. The agent is bounded by its deliverable scope and session objective. There is no real-time sensor reading from the broader project state. This open-loop characteristic is intentional — it prevents agents from being distracted by or making decisions based on the state of other deliverables during focused production work.

**Closed-loop (across sessions):** The handoff mechanism (`NEXT_INSTANCE_STATE.md`) carries state between sessions. DEPENDENCIES reruns after content changes update the dependency graph with current evidence. RECONCILIATION detects integration defects by comparing the updated dependency graph against expected satisfaction states. ORCHESTRATOR scans compute work availability for the next tier. The closed loop operates at the session boundary, not within a session.

This architectural choice — confining closed-loop feedback to session boundaries — is consistent with a broader safety principle: feedback should be deferred to a point at which it can be evaluated with appropriate scope and authority. Real-time feedback within a production session would require the agent to make scope decisions it is not authorized to make.

### 7.7.4 Human Authority as the Halting Condition

The ORCHESTRATOR invariant states: "Human authority is the halting condition." Every iteration of the control loop requires human confirmation at gates. The system cannot autonomously advance tiers, approve deliverables, or resolve conflicts. Human gates function as the comparator authority in the control loop — the system proposes a state and the human decides whether to advance, hold, or redirect.

This design reflects a fundamental principle of human-in-the-loop control system design [CITE:SE_textbook]: in systems where the consequences of error are significant, the human controller should be positioned to observe, evaluate, and intervene at every control cycle. The halting condition ensures that the control loop cannot run away — that the system cannot perform unbounded autonomous execution regardless of context.

---

## 7.8 Formal Methods

Formal methods are mathematical techniques for specifying, developing, and verifying software and systems, encompassing formal specification languages, type systems, invariant calculi, and state machine models [CITE:INCOSE2023]. In Chirality, formal methods are instantiated at the level of natural-language specifications rather than mathematical notation, but the structural characteristics — invariants, preconditions, postconditions, type systems, and state machines — are present in form if not in symbolic representation.

### 7.8.1 The Three-Layer Invariant System

The architecture defines three layers of formally stated invariants, each governing a different scope and enforced at different points in the workflow.

**I1–I10 (Decomposition invariants)** are structural constraints on the decomposition process: flat partitions (I1), no gaps (I2), stable IDs (I3), exactly one partition per atomic unit (I4), deterministic coupling (I5), vocabulary discipline (I6), and production unit coverage (I7–I10). These invariants are enforced by decomposition agents during execution and verified by the AUDIT_DECOMP agent post-execution.

**R1–R9 (Workflow design requirements)** are behavioral constraints on all agents in the system: human decision rights (R1), straight-through task execution (R2), write quarantine (R3), immutable snapshots (R4), mandatory provenance (R5), no invention (R6), conflict surfacing (R7), brief-driven execution (R8), and hygienic publication (R9). These invariants are enforced by agent instruction design — they are embedded in the instruction logic of every agent rather than checked by a separate auditing mechanism.

**K-* (System-wide invariants)** form the twenty-three named, stable invariants catalogued in `CONTRACT.md`, covering the full scope of system behavior: hierarchy (K-HIER-1, K-ID-1), authority (K-AUTH-1, K-AUTH-2, K-BIND-1), sealing (K-SEAL-1, K-GHOST-1), dependencies (K-DEP-1, K-DEP-2), status (K-STATUS-1), staleness (K-STALE-1, K-STALE-2, K-VAL-1), gates (K-GATE-1), merge (K-MERGE-1), provenance (K-PROV-1), invention (K-INVENT-1), conflicts (K-CONFLICT-1), write scope (K-WRITE-1), and snapshots (K-SNAP-1). K-* identifiers are stable and never reused; retired invariants are preserved in the catalog with retirement rationale.

The three-layer structure is an instance of defense-in-depth specification: decomposition invariants govern the internal structure of the requirements model; workflow design requirements govern the behavioral properties of agents; and system-wide invariants govern the global properties of the filesystem-as-state-machine. No single invariant violation can compromise all three layers simultaneously.

The full invariant catalog is reproduced in Appendix A.

### 7.8.2 Preconditions and Postconditions

Each ORCHESTRATOR function is specified with explicit preconditions and postconditions, enabling formal reasoning about state transitions:

| Function | Precondition | Postcondition |
|---|---|---|
| 1. Initialize | Decomposition document exists | `_COORDINATION.md` exists; coordination representation recorded |
| 2. Scaffold | Function 1 complete; tool roots exist | All deliverables initialized; semantic artifacts generated |
| 3. Scan and Report | Deliverables have `_STATUS.md` | State reported; blockers computed (if mode enabled) |
| 4. Estimating | BOE, INDEX.md, and price sources exist | Estimation snapshots per tier |
| 5. Control Loop | Function 1 complete | Handoff artifacts created; ownership boundary clear |

Type 2 agents enforce preconditions as input validation at the start of execution: invalid inputs produce a `FAILED_INPUTS` halt. Missing optional data permits continued execution with `TBD` marking and structured warnings. This behavior is consistent with the Design by Contract methodology [CITE:SE_textbook]: the agent is obligated to verify that its preconditions are met before execution and to guarantee its postconditions upon successful completion.

### 7.8.3 The Formal Type System

The architecture defines a comprehensive type system through fully enumerated domains, spanning four areas of the system model.

**Decomposition ontology** defines the core entity types:

```
AtomicUnit     = { id, statement, status: IN | OUT | TBD, sourceRef }
Partition      = { id, name, scopeDesc, inclusions, exclusions }
ProductionUnit = { id, name, parentPartition, type, responsible, artifacts }
Objective      = { id, statement, mappedUnits }
```

**Dependency type system** defines the relational structure of the knowledge graph:

```
DependencyClass    : ANCHOR | EXECUTION
AnchorType         : IMPLEMENTS_NODE | TRACES_TO_REQUIREMENT | NOT_APPLICABLE
Direction          : UPSTREAM | DOWNSTREAM
DependencyType     : PREREQUISITE | INTERFACE | HANDOVER | CONSTRAINT | ENABLES | OTHER
TargetType         : DELIVERABLE | PACKAGE | WBS_NODE | REQUIREMENT | DOCUMENT
                     | EQUIPMENT | EXTERNAL | UNKNOWN
Confidence         : HIGH | MEDIUM | LOW
Origin             : DECLARED | EXTRACTED
Explicitness       : EXPLICIT | IMPLICIT
Status             : ACTIVE | RETIRED
SatisfactionStatus : TBD | PENDING | IN_PROGRESS | SATISFIED | WAIVED | NOT_APPLICABLE
```

**Review type system** defines the structure of the review and findings process:

```
ReviewType          : SELF_CHECK | PEER_REVIEW | IDC | INDEPENDENT_VERIFICATION
FindingSeverity     : CRITICAL | MAJOR | MINOR | OBSERVATION
FindingDisposition  : ACCEPT_AS_IS | REVISE | DEFER | NOT_APPLICABLE | WITHDRAWN
FindingStatus       : OPEN | RESOLVED | DEFERRED | WITHDRAWN
```

**Epistemic label system** defines the epistemological status of every non-trivial claim:

```
EpistemicLabel : FACT | ASSUMPTION | PROPOSAL | TBD
```

The epistemic label system warrants particular attention. The four labels form a complete and mutually exclusive classification of the epistemological status of any claim in the system:

- FACT: directly observed in source text, with citation
- ASSUMPTION: reasonable inference not directly stated, requiring validation
- PROPOSAL: agent suggestion requiring human decision
- TBD: unknown, placeholder requiring resolution

These labels are not documentation conventions — they are enforced behavioral categories. K-INVENT-1 prohibits agents from generating claims that belong in the FACT category without evidence, and K-CONFLICT-1 requires that conflicting FACT claims be surfaced rather than silently resolved. The type system gives the epistemic architecture its operational teeth.

The types defined in this system are not merely documentation — they constrain agent behavior through enumeration validation, schema checking, and conditional logic embedded in agent protocols. An agent that encounters a value outside the defined enumeration for a field does not guess; it marks the value as UNKNOWN and records a warning.

### 7.8.4 The Lifecycle State Machine

The deliverable lifecycle is a formal state machine with defined states, authorized transitions, and transition actors:

```
OPEN
  ─[PREPARATION]─→ INITIALIZED
  ─[4_DOCUMENTS / DOMAIN_DOCUMENTS]─→ SEMANTIC_READY
  ─[CHIRALITY_FRAMEWORK]─→ IN_PROGRESS
  ─[human]─→ CHECKING
  ─[REVIEW + human approval]─→ ISSUED
  ─[human]─→ (re-open or archive)
```

K-STATUS-1 designates `_STATUS.md` as the canonical lifecycle state indicator for every deliverable. Transitions are forward-only under normal operation. Every transition is recorded in the append-only History section of `_STATUS.md` with date, actor, and rationale. The REVIEW process at Gate 5 is the sole authorized path from CHECKING to ISSUED, and that gate requires human approval. This state machine model directly serves the axiology pillar: it enforces the non-delegable professional responsibility for approval by making the ISSUED state unreachable without human action.

---

## 7.9 Human Factors and Decision Authority

Human factors engineering addresses the allocation of functions between humans and automated systems, the design of interfaces that support human performance, and the management of cognitive workload in complex operational environments [CITE:INCOSE2023]. In Chirality, human factors considerations are not confined to interface design; they are embedded in the fundamental architecture through explicit decision authority allocation, structural cognitive load management, and configurable rigor scaling.

### 7.9.1 Decision Authority Allocation

The system defines an explicit allocation of decision authority between humans and agents. This allocation reflects the professional responsibility model articulated in the axiology pillar (Chapter 3) and enforced by invariants K-AUTH-1 and K-BIND-1.

**Human-owned decisions** (K-AUTH-1, `DIRECTIVE.md` §3.2):
- Scope and boundary decisions
- Selection of governing codes, standards, and design basis
- Hazard and risk acceptance, including residual risk statements
- Conflict adjudication where professional judgment is required
- Approval, issuance, signature, seal, and transmittal for reliance

**Agent-executable actions** (bounded, brief-driven):
- Workspace scaffolding and initialization
- Bulk document drafting
- Dependency extraction and register maintenance
- Coverage analysis and reconciliation reporting
- Estimation and scheduling (derived outputs, not authoritative determinations)
- Aggregation and collation

The allocation boundary is not merely procedural — it is architecturally enforced. K-AUTH-1 states that only humans author binding approval records. K-BIND-1 states that approvals are always binding and only binding. No agent instruction can produce an output that satisfies these invariants without a human performing the approval action. The design makes it structurally impossible for an agent to exceed its allocated authority, not merely policy-prohibited.

### 7.9.2 Cognitive Load Management

The architecture reduces cognitive load through five structural mechanisms, each of which converts a category of cognitive demand into a structural property of the system.

**Epistemic transparency.** Every claim is labeled FACT, ASSUMPTION, PROPOSAL, or TBD. The qualified professional does not need to interrogate an output to determine whether a value is grounded in evidence or inferred — the label carries that information. This eliminates the metacognitive overhead of evaluating claim reliability and replaces it with the lower-cost task of checking label consistency. This mechanism is enforced by K-INVENT-1 and K-CONFLICT-1 and is discussed at length in Chapter 5 (Epistemic Architecture).

**Conflict surfacing.** Contradictions between sources are not resolved silently. The Conflict Table pattern — structured rows with ConflictID, Key, Contenders, ProposedAuthority, and HumanRuling=TBD — presents disagreements in a format that requires minimal cognitive effort to adjudicate. The human must rule, but the ruling is framed as a binary or categorical choice given prepared alternatives, not as unstructured synthesis of contradictory material.

**Working memory externalization.** `MEMORY.md` (per deliverable) and `NEXT_INSTANCE_STATE.md` (per session) externalize context that would otherwise be lost between sessions. Content is organized by semantic topic: Key Decisions, Domain Context, Open Items, Proposal History, and Interface Notes. This structured externalization reduces the recollection burden at session resumption — the human and the incoming agent instance do not reconstruct context from scattered notes; they read a structured record.

**Vocabulary canonicalization.** The Vocabulary Map, required in every decomposition, defines canonical terms and maps synonyms. This prevents semantic drift across team members, sessions, and agent instances. Vocabulary discipline reduces the interpretive overhead of reading deliverable content and review findings.

**Flat hierarchy.** K-HIER-1 enforces a single level of nesting — packages containing deliverables, with no further nesting. The human can comprehend the complete project structure without navigating a deep tree. Deep hierarchies impose navigational overhead that is particularly costly in review contexts, where the reviewer must hold the project structure in working memory while evaluating individual artifacts.

These five mechanisms collectively implement a cognitive architecture in which the system absorbs the burden of state-keeping, conflict detection, and vocabulary management, leaving the human's cognitive resources available for the judgment-intensive tasks that only qualified professionals can perform.

### 7.9.3 Configurable Rigor

K-GATE-1 states: "Gates are dynamic per project instance. Minimum required gates: seal transition + pipeline run approval. Additional gates are project-configurable."

The coordination representation is human-chosen among three modes: `SCHEDULE_FIRST` (lightweight, schedule-oriented), `DECLARED` (dependency-declared, moderate rigor), and `FULL_GRAPH` (complete dependency graph, maximum rigor). Dependency tracking mode similarly scales: `NOT_TRACKED`, `DECLARED`, or `FULL_GRAPH`. When set to `NOT_TRACKED`, the system does not compute blockers, avoiding false precision in contexts where the dependency structure is not yet well-enough understood to support reliable blocker analysis.

This configurability allows teams to match system rigor to project requirements and maturity — a recognition that imposing maximum rigor uniformly is itself a cognitive load burden. A team in early scoping work does not benefit from the same gate density as a team in final deliverable review.

---

## 7.10 Cross-Cutting Patterns

The eight SE disciplines analyzed in Sections 7.2 through 7.9 are not independent. Four cross-cutting architectural patterns underlie and connect them, providing the structural logic that makes the disciplines coherent as a system rather than as a collection of independent governance mechanisms.

### 7.10.1 Tree × DAG Knowledge Architecture

The dependency model separates structural identity from execution coupling through a dual-graph architecture.

The **tree structure** is defined by ANCHOR rows in `Dependencies.csv`. Specifically, exactly one `IMPLEMENTS_NODE` row per deliverable connects each deliverable to its parent package in the WBS hierarchy. The tree is stable and normative — it defines what a deliverable IS within the project structure, independent of its current execution state or dependency relationships. Changes to the tree represent scope changes, which require human authorization.

The **DAG structure** is defined by EXECUTION rows in `Dependencies.csv`. These many-to-many rows capture information flow between deliverables: prerequisites, interfaces, handovers, constraints, enabling relationships. The DAG is current and operative — it defines what a deliverable NEEDS at any given point in the project. The DAG evolves as the project progresses and dependencies become satisfied, retired, or newly identified.

This dual-graph model prevents scope drift (the tree is stable and scope-change-controlled) while supporting dynamic execution planning (the DAG evolves freely within the current scope). The formal separation also enables the two forms of traceability to function independently: structural traceability (deliverable to WBS node) operates on the tree; execution dependency analysis operates on the DAG.

The tree × DAG architecture directly serves the ontology pillar: the tree defines the stable ontological structure of the project (what entities exist and how they are organized), while the DAG defines the current epistemological and praxiological state (what is known about the relationships between entities and what must be done before each entity can be completed).

### 7.10.2 Distributed Authority with On-Demand Aggregation

K-DEP-1 states: "Deliverable-local `_DEPENDENCIES.md` and `Dependencies.csv` are authoritative for dependencies. There is no central dependency graph; aggregation is on-demand."

Each deliverable maintains its own dependency register. There is no central database. Cross-deliverable views — closure analysis, aggregation reports, reconciliation summaries — are produced on demand by read-only agents and materialized as immutable snapshots in tool roots. This architectural choice has two significant consequences.

First, it eliminates the synchronization burden of a centralized graph. The dependency graph is always current because it is derived from the files that define it, not copied into a separate representation that must be kept consistent. Any aggregation is a fresh derivation from current source data, not a query against a potentially stale cache.

Second, it distributes authority correctly. The team member responsible for a deliverable maintains that deliverable's dependency register. They do not submit changes to a central graph administrator; they update their local register, and aggregation picks up the change on the next run. This distribution of authority is consistent with the accountability structure of professional deliverable work, in which the deliverable owner is responsible for understanding and declaring what their deliverable depends on.

This pattern directly serves both the ontology pillar (the dependency register is part of the deliverable's intrinsic state) and the praxiology pillar (authority over a deliverable's dependency state is vested in the deliverable owner, not in a central system).

### 7.10.3 Evidence-First Epistemology as Safety Mechanism

The epistemic controls — K-PROV-1, K-INVENT-1, and K-CONFLICT-1 — function collectively as a safety mechanism against the primary failure mode of LLM-assisted systems.

K-PROV-1 (mandatory provenance) ensures that every claim can be audited back to its source. K-INVENT-1 (no invention) ensures that gaps in evidence are visible rather than papered over with plausible-sounding approximations. K-CONFLICT-1 (conflicts surfaced) ensures that disagreements between sources reach the human decision-maker rather than being silently resolved by the agent.

The system does not attempt to prevent hallucination — a problem that cannot be solved by architectural means alone. Instead, it requires provenance for every claim, making unsupported claims structurally visible. A claim without provenance is not merely a concern — it is a detectable anomaly in the K-PROV-1 framework, identifiable by inspection or audit. This reframes the problem: rather than trying to produce correct LLM outputs, the system makes incorrect or unsupported outputs findable.

This mechanism is the deepest expression of the epistemology pillar in the Chirality architecture. Chapter 5 (Epistemic Architecture) develops this theme at length. The observation made here, from the SE perspective, is that this epistemological commitment functions as a safety mechanism: it bounds the propagation of false information through the project record in the same way that fault containment zones bound the propagation of computational failures. Plausible-sounding but unsupported claims, like agent write-scope violations, cannot silently cross the boundary into the authoritative record.

### 7.10.4 Multi-Layer Enforcement

`CONTRACT.md` §2 defines four enforcement layers, each checking a specific subset of invariants at a specific point in the workflow:

| Enforcement Layer | Timing | Invariants Checked |
|---|---|---|
| Agent instructions (design-time) | When instruction files are authored | K-GHOST-1, K-WRITE-1, K-SNAP-1, K-PROV-1, K-INVENT-1, K-CONFLICT-1, K-DEP-1, K-DEP-2 |
| ORCHESTRATOR (runtime) | During workspace initialization and pipeline execution | K-SEAL-1, K-GATE-1, K-HIER-1 |
| Human review (gate) | At every gate decision | K-AUTH-1, K-AUTH-2, K-BIND-1, K-STALE-2, K-MERGE-1, K-VAL-1, K-STATUS-1 |
| Future tooling (automated) | Continuous or on-demand | K-STALE-1, K-VAL-1, K-MERGE-1, K-AUTH-2, K-DEP-2 |

This defense-in-depth enforcement strategy ensures that no single enforcement failure can compromise system integrity. The invariants governing agent behavior (K-GHOST-1, K-WRITE-1) are enforced at design time — in the agent instructions themselves — so that a runtime enforcement failure does not create an opportunity for violation. The invariants governing authority and approval (K-AUTH-1, K-AUTH-2, K-BIND-1) are enforced at human review gates, where the human serves as both the enforcement mechanism and the accountable decision-maker. Future tooling enforcement handles invariants that require automated computation (transitive staleness, SHA comparison) which is not yet practical to check at the other enforcement layers.

The allocation of invariants to enforcement layers is not arbitrary. Each invariant is assigned to the earliest and most reliable enforcement point available. Design-time enforcement is preferred because it prevents violations from arising at all; gate enforcement is preferred over post-hoc automated checking because it involves human judgment at the decision point.

---

## 7.11 Assessment

### 7.11.1 SE Disciplines as Coordination Mechanisms

The analysis presented in this chapter supports a central claim: the SE disciplines present in the Chirality architecture are not compliance artifacts applied to an agent system — they are the mechanism by which agents coordinate, the means by which failures are contained, and the basis on which humans maintain authority.

Architecture and structural design provide the physical and logical organization within which all other disciplines operate. The layered separation of concerns, the production unit encapsulation model, and the interface contract system define the boundaries that make fault containment zones meaningful and that give the configuration management discipline something stable to manage.

Configuration management is not an auditing overlay — it is the state representation itself. The choice of git-tracked plain files as the sole state store means that baseline control, change impact analysis, and audit trail are properties of the architecture, not products of a separate CM system. Every other discipline depends on this: V-model traceability requires that artifact states be versioned; formal methods require that invariants be checked against a well-defined state; control theory requires reliable sensor readings; human factors requires that decision context be externalized and preserved.

Verification and validation provide the integrating discipline — the mechanisms by which the decomposition structure (requirements engineering), the controlled state (control theory), and the formally specified behaviors (formal methods) are confirmed to have been achieved. The V-model, stage-gate reviews, coverage analysis, and traceability architecture are not independent verification tools; they are the instruments by which the system closes the loop from intent to evidence.

Safety and reliability engineering addresses the specific challenge of deploying agents in environments where failures have consequences. The fault containment zone architecture, failure mode visibility protocol, and context sealing invariants implement classical safety engineering principles [CITE:Leveson2011] adapted to the specific hazard profile of LLM-based agents: the risk that an agent, given ambiguous context or insufficient guidance, produces plausible-sounding outputs that are incorrect, unsupported, or unauthorized.

Requirements engineering provides the formal link between the project scope and the deliverable structure. The hierarchical decomposition protocol, RTM, and acceptance criteria allocation ensure that scope commitments are traceable to specific production units, and that those units are verified against their derivation before they are issued.

Control theory provides the analytical framework for understanding how the system behaves across multiple sessions and how it converges toward project completion. The closed-loop architecture, with human authority as the halting condition, ensures that the system makes bounded, directional progress without autonomous drift.

Formal methods provide the specification precision that makes all of the above testable and auditable. The invariant system, precondition and postcondition specifications, type system, and state machine model are the instruments by which the design intent is made precise enough to enforce. Without formal methods, the other disciplines would be expressed as guidelines; with them, they are verifiable constraints.

Human factors engineering provides the design logic for the human-agent interface. Decision authority allocation prevents scope creep of agent authority; cognitive load management ensures that human reviewers can perform their gate functions without being overwhelmed by unstructured information; configurable rigor allows the system to scale to project requirements rather than imposing uniform overhead.

### 7.11.2 Alignment with the Four-Pillar Framework

Each SE discipline implemented in the Chirality architecture serves one or more of the four philosophical pillars established in Chapter 3. The alignment is not coincidental — the pillars define what the system must achieve, and the SE disciplines provide the mechanisms by which those achievements are implemented.

**Ontology** is served primarily by architecture and structural design. The production unit folder as atomic module, the flat K-HIER-1 hierarchy, and the dual tree × DAG knowledge structure define the ontological model that the system operates on. The filesystem is the database, and the structural design defines what entities exist and how they are organized.

**Epistemology** is the most densely served pillar. Configuration management (content-addressed approval, immutable snapshots, the git event store), verification and validation (traceability, coverage analysis, the V-model), formal methods (the type system, invariants, preconditions and postconditions), and the evidence-first epistemology cross-cutting pattern all serve the epistemological goal: making the grounds for professional reliance structurally visible and auditable. The epistemology pillar is served more densely than any other because it is, as Chapter 3 argues, the load-bearing contribution of the system. The ontological, praxiological, and axiological structures exist to serve the epistemological mission.

**Praxiology** is served by control theory, requirements engineering, and the human factors decision authority allocation. The closed-loop control architecture, the brief-driven execution model, and the gate-controlled workflow structure define how work is done within the system. The write quarantine mechanism (K-WRITE-1, fault containment zones) implements the praxiological commitment to bounded, auditable execution.

**Axiology** is served by safety and reliability engineering, human factors decision authority allocation, and the formal invariants K-AUTH-1, K-AUTH-2, and K-BIND-1. The value commitment that professional responsibility is personal and non-delegable is enforced architecturally through the human gate requirement, the content-addressed approval mechanism, and the prohibition on agent-authored binding approval records. The axiology pillar is unusual in that its enforcement is not a matter of functional correctness — a system that violated K-AUTH-1 would still function — but of ethical and professional accountability. The architecture makes compliance the path of least resistance rather than requiring discipline against system affordances.

### 7.11.3 Summary Claim

The Chirality instruction architecture is, in its entirety, a systems engineering artifact. The instruction files are formal specifications defining interfaces, state machines, invariants, preconditions, postconditions, containment zones, and authority boundaries. The governance documents — `DIRECTIVE.md`, the specification (`SPEC.md`), the type system (`TYPES.md`), and `CONTRACT.md` — form a coherent specification hierarchy: intent, physical structures, vocabulary, and binding invariants.

What distinguishes this architecture from a conventional agent system is that the SE disciplines are not bolted on as compliance artifacts. They are the mechanism by which agents coordinate, the means by which failures are contained, and the basis on which humans maintain authority. The Type 0/1/2 hierarchy, the write scope architecture, the invariant system, the gate-controlled workflows, and the evidence-first epistemology are all instantiations of classical SE patterns adapted to the specific challenge of governing LLM-based agents in professional and regulated environments.

The practical implication is significant: the systems engineering content of this architecture is not incidental overhead. It is what makes the system capable of supporting professional reliance. A system without content-addressed approval cannot provide reliable baselines. A system without fault containment zones cannot bound agent failures. A system without the formal type system cannot enforce consistent behavior across agent instances. A system without human gates cannot maintain professional accountability. The SE disciplines are not qualities added to the system; they are the properties that define it.

Chapter 8 will examine the deployment architecture and operational considerations that determine how these design properties are realized in practice.

---

*This chapter is based on systematic analysis of all agent instruction files and governance documents in the Chirality repository. The full invariant catalog is provided in Appendix A. The complete agent inventory, including type classification and write scope for each agent, is provided in Appendix B.*
