# DBM — Agent Instruction Architecture

This document is the design basis memorandum for the agent instruction system shipped with the Chirality App. It establishes the architectural basis — the principles, contracts, structures, and relationships — that govern how agent instruction files are designed, how agents relate to each other, and how the system maintains coherence at scale.

**Audience:** Anyone who will work with, extend, audit, or maintain the agent instruction suite.

**Scope:** The 38 agent instruction files (`AGENT_*.md`) in `agents/`, the two Type 0 canonical standards, and the governance contracts that bind them. This document does not cover the desktop application runtime, the harness SDK, or the UI — only the instruction architecture.

**Relationship to other governance documents:**

| Document | Role | Relationship to this DBM |
|----------|------|--------------------------|
| `DIRECTIVE.md` | Founding intent and design philosophy | This DBM operationalizes DIRECTIVE's principles into the agent instruction layer |
| `SPEC.md` | Physical structures, schemas, folder layouts | SPEC defines the filesystem contracts that agents write to; this DBM defines the agents themselves |
| `TYPES.md` | Domain vocabulary, ID formats, enums | TYPES defines the nouns; this DBM defines how agents use them |
| `CONTRACT.md` | K-* invariant catalog | This DBM maps K-* invariants to the agents that enforce them |
| `AGENTS.md` | Operator-facing index and rules of the road | AGENTS.md is the quick-reference; this DBM is the detailed basis |
| `SE_Design_Analysis.md` | Systems engineering design analysis | Characterizes the SE disciplines realized in this architecture; this DBM defines the architecture that the SE analysis examines |
| `PROFESSIONAL_ENGINEERING.md` | Professional practice standard (PPMP-referenced) | Traces the instruction architecture to APEGA regulatory obligations; maps direct supervision and control (§3.1.1) and thorough review (§3.1.2) to the governance mechanisms defined in this DBM |

---

## 1. Design Philosophy

The agent instruction architecture is governed by eight foundational principles derived from `DIRECTIVE.md`. These are not independent guidelines — they form a structural dependency chain where foundational decisions enable downstream capabilities. `DIRECTIVE.md` §2 frames these principles as instantiations of four philosophical pillars — ontology, epistemology, praxiology, and axiology — and identifies the epistemology (evidence-first knowledge architecture) as the system's most distinctive and load-bearing contribution. The eight principles below operationalize that framework into the instruction layer.

### 1.1 Filesystem Is the State

Project truth lives in git-tracked files. Agents do not maintain hidden databases, private state, or transient context that diverges from the filesystem. If it is not on disk, it does not exist for purposes of reliance.

This is the load-bearing architectural decision. The V-model traceability (§8), immutable snapshots (§1.7), change propagation tracking (K-STALE-1/2), content-addressed approval (K-AUTH-2), and the entire audit trail all depend on state being in git-tracked files. If state moved to a database, every one of these capabilities would need to be rebuilt. The filesystem choice is not a simplification — it is the mechanism that makes the SE apparatus work.

### 1.2 Human Authority at Every Gate

Humans own acceptance, rulings, conflict resolution, scope boundary changes, and publication approval. Agents execute bounded work and preserve provenance; they may propose but do not declare truth.

### 1.3 Evidence-First Epistemology

Every non-trivial claim includes a source path and best-effort section reference (or explicit `location TBD`). Epistemic labels — `FACT`, `ASSUMPTION`, `PROPOSAL`, `TBD` — are used to distinguish what is known from what is inferred.

This is the system's primary response to the fundamental limitation of LLM-based agents: hallucination. Rather than attempting to prevent unsupported claims (which is not reliably possible), the architecture requires provenance for every claim and makes unsupported claims structurally visible. K-PROV-1 (mandatory provenance), K-INVENT-1 (no invention), and K-CONFLICT-1 (conflict surfacing) enforce this collectively. The result is that gaps in evidence are findings — not hidden failures.

### 1.4 No Invention

When required information is missing, agents label it `TBD` and surface the gap as an open issue. They do not guess, default-fill, or silently infer. Missing data is a finding, not a problem to solve.

### 1.5 Write Quarantine

Every agent declares an explicit write scope. Tool roots (where derived outputs land) are isolated from source truth (where human-accepted deliverables live). No agent writes outside its declared scope. This creates formal fault containment zones — a Type 2 agent failure cannot corrupt source truth (see §7 for the full scope architecture).

### 1.6 Layered Abstraction (Type 0 / 1 / 2)

The system separates standards definition (Type 0) from interactive orchestration (Type 1) from bounded task execution (Type 2). Each layer has distinct responsibilities, constraints, and interaction patterns. See §2 for details.

### 1.7 Immutable Snapshots

Task agents that produce analysis outputs write to timestamped snapshot folders that are never modified after creation. Mutable pointer files (`_LATEST.md`) provide convenience access to the most recent snapshot. The snapshot trail is the audit trail. This is possible because state is in git-tracked files (§1.1) — the filesystem natively supports append-only history.

### 1.8 Least Structure That Works

Structure is added only when it reduces error or rework. Rigor scales with stakes. The system avoids premature abstraction and unnecessary ceremony while maintaining the controls required for professional and regulated environments.

---

## 2. Type Hierarchy

The agent system is organized into three types with distinct responsibilities, constraints, and interaction patterns.

### 2.1 Type 0 — Canonical Standards (Architect)

Type 0 agents define the invariant protocols and design standards that all downstream agents must conform to. They do not write project state. They are the constitutional layer.

| Agent | Role | What It Defines |
|-------|------|-----------------|
| **HELPS_HUMANS** | Workflow design standard | Agent Header Block, R1–R9 compliance requirements, 4-section structure, brief formats, QA contract, publication hygiene |
| **DECOMP_BASE** | Decomposition protocol standard | 7-gate protocol, I1–I10 invariants, entity schemas, extension contract, ledger/telemetry contracts |

**Key constraint:** Where any `AGENT_*` file disagrees with a Type 0 standard, the other file must be edited to conform.

### Formal Authority Properties

The type hierarchy enforces three authority invariants that the entire system depends on:

1. **Type 2 cannot escalate to Type 1 authority.** Specialists execute bounded briefs and return outputs — they cannot initiate gate reviews, spawn other agents, or make scope decisions.
2. **Type 1 cannot override Type 0 constraints.** Managers orchestrate within the rules defined by canonical standards — they cannot relax R1–R9, I1–I10, or K-* invariants.
3. **Human gates cannot be bypassed by any type.** No agent — regardless of type — can approve deliverables, issue work for reliance, resolve conflicts authoritatively, or commit to the baseline without explicit human authorization.

### 2.2 Type 1 — Interactive Personas (Manager)

Type 1 agents are human-facing. They run conversational, gate-controlled workflows where the human makes consequential decisions and the agent handles orchestration, routing, and structured output.

**Characteristics:**
- `AGENT_CLASS: PERSONA`, `INTERACTION_SURFACE: chat`, `BLOCKING: allowed`
- Multi-phase workflows with explicit gate questions at each phase
- May spawn Type 2 agents
- Own orchestration decisions but not engineering content
- Produce guidance, run plans, briefs, and structured cards

**Count:** 14 agents (see §5 for inventory).

### 2.3 Type 2 — Bounded Task Agents (Specialist)

Type 2 agents are brief-driven specialists that run straight-through without human interaction. They receive structured inputs (INIT-TASK briefs), produce auditable outputs, and return status to their invoking agent.

**Characteristics:**
- `AGENT_CLASS: TASK`, `INTERACTION_SURFACE: INIT-TASK or spawned`, `BLOCKING: never`
- Straight-through execution (no mid-run gates)
- Produce immutable snapshots or deliverable-local file writes
- Never spawn other agents
- If inputs are invalid: `FAILED_INPUTS` (halt). If data missing: `TBD` (continue conservatively)

**Count:** 19 agents (see §5 for inventory).

**Note:** The `agents/` directory also contains supporting template files (`MEMORY_TEMPLATE.md`, `TASK_ESTIMATING_TEMPLATE.md`) that are not agent instructions but are consumed by agents at runtime.

---

## 3. Structural Template

Every agent instruction file follows a universal skeleton mandated by `AGENT_HELPS_HUMANS.md`.

### 3.1 File Anatomy

```
---
description: "<one-line description for UI labels>"
---
[[DOC:AGENT_INSTRUCTIONS]]
# AGENT INSTRUCTIONS — <AGENT_NAME> (<Role Description>)
AGENT_TYPE: <0 | 1 | 2>

## Agent Type
| Property            | Value |
|---------------------|-------|
| AGENT_TYPE          | ...   |
| AGENT_CLASS         | ...   |
| INTERACTION_SURFACE | ...   |
| WRITE_SCOPE         | ...   |
| BLOCKING            | ...   |
| PRIMARY_OUTPUTS     | ...   |

## Precedence (conflict resolution)
1. PROTOCOL > 2. SPEC > 3. STRUCTURE > 4. RATIONALE

## Non-negotiable invariants
- <bulleted list; 5–14 items per agent>

[[BEGIN:PROTOCOL]]
## PROTOCOL
<Operational workflow: steps, phases, gates, or functions>
[[END:PROTOCOL]]

[[BEGIN:SPEC]]
## SPEC
<Validity requirements and invalid states>
[[END:SPEC]]

[[BEGIN:STRUCTURE]]
## STRUCTURE
<File schemas, templates, output formats>
[[END:STRUCTURE]]

[[BEGIN:RATIONALE]]
## RATIONALE
<Design intent — non-normative>
[[END:RATIONALE]]
```

### 3.2 Agent Header Block (6 Required Fields)

| Field | Valid Values | Semantics |
|-------|-------------|-----------|
| `AGENT_TYPE` | `TYPE 0`, `TYPE 1`, `TYPE 2` | Position in the layered hierarchy |
| `AGENT_CLASS` | `PERSONA`, `TASK` | Conversational interface vs straight-through execution |
| `INTERACTION_SURFACE` | `chat`, `INIT-TASK`, `spawned`, `both` | How the agent is invoked |
| `WRITE_SCOPE` | `none`, `repo-wide`, `project-level`, `deliverable-local`, `tool-root-only`, `repo-metadata-only`, `workspace-scaffold-only`, `knowledge-type-local` | What filesystem area the agent may write to |
| `BLOCKING` | `never`, `allowed` | Whether the agent may pause for human input |
| `PRIMARY_OUTPUTS` | Free text | What the agent produces |

### 3.3 The Four Standard Sections

| Section | Governs | Precedence Rank |
|---------|---------|-----------------|
| **PROTOCOL** | Sequencing and interaction rules — how to run the process | 1 (highest) |
| **SPEC** | Validity — pass/fail requirements; what is considered correct | 2 |
| **STRUCTURE** | Allowed entities, relationships, schemas, templates | 3 |
| **RATIONALE** | Interpretation when ambiguity remains — design values and intent | 4 (lowest) |

All sections are bounded by `[[BEGIN:X]]...[[END:X]]` delimiters for machine parseability.

### 3.4 Type 1 vs Type 2 Structural Differences

| Aspect | Type 1 (Persona) | Type 2 (Task) |
|--------|------------------|---------------|
| PROTOCOL style | Multi-phase gated workflow with human gates | Straight-through numbered steps; no mid-run gates |
| Input format | Natural language conversation | Structured parameter table (INIT-TASK brief) |
| Output format | Conversational guidance + structured cards | File writes + run report (PASS/FAIL) |
| Sub-agent spawning | May spawn Type 2 agents | Never spawns others |
| Preamble sections | Foundations, glossary, perspective, coordination rules | Runtime parameters table, glossary |

---

## 4. Contract Framework

Three layers of contracts govern agent behavior. They are complementary and non-overlapping.

### 4.1 R1–R9: Workflow Design Requirements (from HELPS_HUMANS)

These requirements apply to all agents and to the design of new agent workflows.

| ID | Requirement | Rule |
|----|-------------|------|
| **R1** | Human decision rights are explicit | Human-owned decisions are enumerated and preserved |
| **R2** | Task agents are straight-through | Task agents run without requiring mid-run human decisions |
| **R3** | Write quarantine is enforced | Every agent has an explicit write scope; tool roots are isolated from source truth |
| **R4** | Snapshots are immutable | Each run produces a new snapshot folder; pointer files may be overwritten; snapshots may not |
| **R5** | Provenance is mandatory | Aggregated/extracted data includes `SourcePath` and best-effort `SectionRef` |
| **R6** | No invention behavior is defined | Missing data becomes `TBD` with assumptions captured |
| **R7** | Conflicts/duplicates are surfaced | The system does not hide or silently resolve discrepancies |
| **R8** | Brief-driven execution exists | Pipelines have a defined brief format (INIT-TASK) and deterministic outputs |
| **R9** | Publication is hygienic | Version control publishing is reviewable and non-destructive by default |

### 4.2 I1–I10: Decomposition Invariants (from DECOMP_BASE)

These invariants apply to all decomposition agents (PROJECT_DECOMP, SOFTWARE_DECOMP, DOMAIN_DECOMP) and are verified by AUDIT_DECOMP.

| ID | Invariant | Rule |
|----|-----------|------|
| **I1** | Human-validated decomposition | Confirmed by human at defined gates; no gate may be skipped |
| **I2** | No invention | Do not create units, objectives, or artifacts beyond source material; unknowns → `TBD` |
| **I3** | Partitions are flat | No nested partitions; additional granularity via additional partitions at the same level |
| **I4** | No overlap / no gaps | Every IN-scope atomic unit assigned to exactly one partition |
| **I5** | Stable identifiers | Once assigned, IDs remain stable unless human explicitly requests renumbering |
| **I6** | Deterministic ID coupling | Production unit IDs mechanically derived from parent partition IDs |
| **I7** | Objective mapping is best-effort | Unmapped objectives surfaced as open issues |
| **I8** | Traceable rationale | Non-trivial assignment decisions recorded as explicit decisions |
| **I9** | Ledger + telemetry | Every decomposition includes a machine-checkable ledger and Coverage & Telemetry summary |
| **I10** | Vocabulary discipline | Every decomposition includes a Vocabulary Map; canonical terms used consistently |

### 4.3 K-* Invariants: System-Wide Enforcement (from CONTRACT.md)

The `K-*` invariants are defined in `CONTRACT.md`. Their enforcement is distributed across the agent suite:

| K-* Group | Invariants | Primary Enforcing Agents |
|-----------|-----------|--------------------------|
| Hierarchy & Identity | K-HIER-1, K-ID-1 | PROJECT_DECOMP, PREPARATION |
| Authority & Approval | K-AUTH-1, K-AUTH-2, K-BIND-1 | REVIEW, CHANGE (approval gates) |
| Sealing & Context | K-SEAL-1, K-GHOST-1 | Type 2 agents (check lifecycle state before writes) |
| Dependencies | K-DEP-1, K-DEP-2 | DEPENDENCIES, AUDIT_DEP_CLOSURE |
| Status | K-STATUS-1 | PREPARATION, 4_DOCUMENTS, CHIRALITY_FRAMEWORK, REVIEW |
| Staleness & Validation | K-STALE-1, K-STALE-2, K-VAL-1 | AUDIT_DEP_CLOSURE, RECONCILIATION; future tooling (SHA comparison) |
| Gates | K-GATE-1 | ORCHESTRATOR, SCHEDULING |
| Merge | K-MERGE-1 | CHANGE |
| Provenance | K-PROV-1 | DEPENDENCIES (every row must cite evidence) |
| Invention | K-INVENT-1 | Universal (all agents) |
| Conflicts | K-CONFLICT-1 | Universal (all agents) |
| Write scope | K-WRITE-1 | Universal (WRITE_SCOPE declaration per agent) |
| Snapshots | K-SNAP-1 | All snapshot-producing agents |

### 4.4 Normative Keywords

Per HELPS_HUMANS, agent instructions use these keywords with defined meaning:

| Keyword | Meaning |
|---------|---------|
| **MUST** / **MUST NOT** | Mandatory for compliance |
| **SHOULD** / **SHOULD NOT** | Recommended best practice |
| **MAY** | Optional |

---

## 5. Agent Inventory

### 5.1 Complete Classification Table

| Agent | Type | Class | Surface | Write Scope | Blocking | Primary Outputs |
|-------|------|-------|---------|-------------|----------|-----------------|
| **HELPS_HUMANS** | 0 | PERSONA | chat | none | — | Workflow design standards |
| **DECOMP_BASE** | 0 | PERSONA | chat | none | — | Decomposition protocol standard |
| **HELP_HUMAN** | 1 | PERSONA | chat | none (drafts briefs) | never | Run plans, briefs, checklists, next-step cards |
| **ORCHESTRATOR** | 1 | PERSONA | chat | tool-root (`_Coordination/`) | allowed | `_COORDINATION.md`, `NEXT_INSTANCE_PROMPT.md`, `NEXT_INSTANCE_STATE.md`; spawns setup pipelines |
| **WORKING_ITEMS** | 1 | PERSONA | chat | deliverable-local | allowed | Updated deliverable artifacts, `MEMORY.md` |
| **RECONCILIATION** | 1 | PERSONA | chat | tool-root (`_Reconciliation/`) | allowed | Run summaries, handoff requests |
| **CHANGE** | 1 | PERSONA | chat | tool-root (`_Change/`) + repo (approval-gated) | allowed | Git state reports; approved file/git actions |
| **PROJECT_DECOMP** | 1 | PERSONA | chat | project-level | allowed | SSOW decomposition document |
| **SOFTWARE_DECOMP** | 1 | PERSONA | chat | project-level | allowed | Software decomposition with Context Envelopes |
| **DOMAIN_DECOMP** | 1 | PERSONA | chat | repo-metadata-only | allowed | SDO domain decomposition document |
| **SCOPE_CHANGE** | 1 | PERSONA | chat | project-level | allowed (5 gates) | Amended decomposition, impact assessment, propagation record |
| **CONTEXT_TRANSPOSE** | 1 | PERSONA | chat | repo-metadata-only | allowed (7 gates) | CTSP snapshot, patch plan |
| **REVIEW** | 1 | PERSONA | chat | deliverable-local + tool-root | allowed (5 gates) | Review checklist, finding register, lifecycle transition record |
| **SCHEDULING** | 1 | PERSONA | chat | tool-root (`_Schedule/`) | allowed (5 gates) | Schedule structure, Gantt, critical path report |
| **EVALUATION** | 1 | PERSONA | chat | tool-root (`_Evaluation/`) | allowed | `EVALUATION_PROTOCOL.md`, `EVALUATION_REPORT.md`, pointers to Type 2 outputs |
| **TOOLMAKER** | 1 | PERSONA | chat | repo-wide | allowed | Shell scripts, Python utilities, skill templates, tool registry |
| **PREPARATION** | 2 | TASK | spawned | workspace-scaffold-only | never | Package/deliverable/category/KT folders with minimum viable fileset |
| **4_DOCUMENTS** | 2 | TASK | spawned | deliverable-local | never | Datasheet, Specification, Guidance, Procedure; `_STATUS.md` update |
| **DOMAIN_DOCUMENTS** | 2 | TASK | spawned | knowledge-type-local | never | `Scoping.md` + variable `KA-*.md` Knowledge Artifacts |
| **CHIRALITY_FRAMEWORK** | 2 | TASK | spawned/INIT | deliverable-local | never | `_SEMANTIC.md`; `_STATUS.md` → SEMANTIC_READY |
| **CHIRALITY_LENS** | 2 | TASK | spawned/INIT | deliverable-local | never | `_SEMANTIC_LENSING.md` |
| **DEPENDENCIES** | 2 | TASK | INIT-TASK | deliverable-local (dep artifacts only) | never | `Dependencies.csv`, `_DEPENDENCIES.md` |
| **ESTIMATING** | 2 | TASK | INIT-TASK | tool-root (`_Estimates/`) | never | Estimate snapshot (Summary, Detail.csv, QA, logs) |
| **ESTIMATE_PREP** | 2 | TASK | INIT-TASK | tool-root (`_EstimatePrep/`) | never | 18-file pricing library, BOE scaffold/full |
| **AGGREGATION** | 2 | TASK | INIT-TASK | tool-root (`_Aggregation/`) | never | Aggregation snapshot (indexes, registers, rollups) |
| **TASK** | 2 | TASK | INIT-TASK | deliverable-local | never | Proposals; optional authorized edits |
| **AUDIT_AGENTS** | 2 | TASK | INIT-TASK | tool-root (`_Reconciliation/AgentAudit/`) | never | Audit report, issue log, patch plan |
| **AUDIT_DECOMP** | 2 | TASK | INIT-TASK | tool-root (`_Reconciliation/DecompCoverage/`) | never | Coverage report, issue log CSV, coverage matrix, summary JSON |
| **AUDIT_DEP_CLOSURE** | 2 | TASK | INIT-TASK | tool-root (`_Reconciliation/DepClosure/`) | never | Closure report, issue log, JSON summary, analysis script |
| **DOMAIN_HYPERGRAPH** | 2 | TASK | INIT-TASK | tool-root (`_Aggregation/Hypergraph/`) | never | Hypergraph snapshot: `nodes.csv`, `hyperedges.csv`, `incidence.csv`, `hypergraph.json`, QA + evidence |
| **AUDIT_HYPERGRAPH_CLOSURE** | 2 | TASK | INIT-TASK | tool-root (`_Reconciliation/HypergraphClosure/`) | never | Closure report, issue log, JSON summary, analysis script |
| **AUDIT_GOVERNANCE** | 2 | TASK | INIT-TASK | tool-root (`_Reconciliation/GovernanceAudit/`) | never | Governance audit report, issue log CSV, summary JSON, QA report |
| **AUDIT_EPISTEMIC** | 2 | TASK | INIT-TASK | tool-root (`_Reconciliation/EpistemicAudit/`) | never | Epistemic audit report, issue log CSV, summary JSON, QA report |
| **AUDIT_SCOPE_CLOSURE** | 2 | TASK | INIT-TASK | tool-root (`_Reconciliation/ScopeClosureAudit/`) | never | Scope closure report, issue log CSV, summary JSON, QA report |
| **CONTENT_DIGEST** | 2 | TASK | INIT-TASK | tool-root (`_Evaluation/content-digests/`) | never | `{DEL-ID}.md` — structured content digest for one deliverable |
| **EVALUATION_REPORT** | 2 | TASK | INIT-TASK | tool-root (`_Evaluation/reports/`) | never | `DIM-{NN}_{DimensionName}.md` — scored dimension evaluation report |
| **EVALUATION_STRUCTURE_AUDIT** | 2 | TASK | INIT-TASK | tool-root (`_Evaluation/reports/`) | never | Structure audit report with file counts, lifecycle state distribution, violation list |
| **EVALUATION_DEPENDENCY_AUDIT** | 2 | TASK | INIT-TASK | tool-root (`_Evaluation/reports/`) | never | Dependency audit report with per-deliverable schema check, anchor check, evidence check |

### 5.2 The Agent Matrix

Agents are organized along two axes from the chirality semantic framework (Matrix A):

| | **GUIDING** | **APPLYING** | **JUDGING** | **REVIEWING** |
|:---|:---|:---|:---|:---|
| **NORMATIVE** | HELP | ORCHESTRATE | WORKING_ITEMS | AGGREGATE |
| **OPERATIVE** | DECOMP\* | PREP\* | TASK\* | AUDIT\* |
| **EVALUATIVE** | AGENTS | DEPENDENCIES | CHANGE | RECONCILING |

- **NORMATIVE** and **EVALUATIVE** rows → **WORKBENCH** page (interactive persona sessions)
- **OPERATIVE** row → **PIPELINE** page (pipeline execution with category dropdowns)

---

## 6. Orchestration Architecture

### 6.1 Spawning Graph

```
HELP_HUMAN (Type 1 — classifies intent, routes to agents; does not spawn)

ORCHESTRATOR (Type 1) ──spawns──┬── PREPARATION (Type 2)
                                ├── 4_DOCUMENTS (Type 2)
                                ├── DOMAIN_DOCUMENTS (Type 2)
                                ├── CHIRALITY_FRAMEWORK (Type 2)
                                ├── CHIRALITY_LENS (Type 2)
                                ├── DOMAIN_HYPERGRAPH (Type 2) [DOMAIN only; Phase 2.6]
                                ├── ESTIMATING (Type 2)
                                └── AGGREGATION (Type 2)

WORKING_ITEMS (Type 1) ──spawns──── TASK (Type 2)

RECONCILIATION (Type 1) ──spawns──┬── AUDIT_DEP_CLOSURE (Type 2)
                                  ├── AUDIT_AGENTS (Type 2)
                                  ├── AUDIT_DECOMP (Type 2)
                                  └── AUDIT_HYPERGRAPH_CLOSURE (Type 2) [DOMAIN only]

EVALUATION (Type 1) ──spawns──┬── CONTENT_DIGEST (Type 2)
                              ├── EVALUATION_REPORT (Type 2)
                              ├── EVALUATION_STRUCTURE_AUDIT (Type 2)
                              └── EVALUATION_DEPENDENCY_AUDIT (Type 2)

CHANGE (Type 1) ── leaf agent (spawns nothing; implements approved edits)

REVIEW (Type 1) ── triggers AUDIT_DECOMP as precondition check
SCOPE_CHANGE (Type 1) ── hands off to ORCHESTRATOR (for PREPARATION) + CHANGE (for commits)
CONTEXT_TRANSPOSE (Type 1) ── hands off to CHANGE (for publication)
SCHEDULING (Type 1) ── standalone (reads dependency graph; produces schedule artifacts)
TOOLMAKER (Type 1) ── standalone (designs and implements deterministic tools; hands off to CHANGE for publication)
```

### 6.2 Control Loop (Session Handoff)

The system maintains session continuity across agent invocations through two durable artifacts:

| Artifact | Owner | Mutability | Content |
|----------|-------|------------|---------|
| `NEXT_INSTANCE_PROMPT.md` | ORCHESTRATOR (creates) | Stable — updated only on protocol changes | Stable session startup instructions |
| `NEXT_INSTANCE_STATE.md` | ORCHESTRATOR (creates); WORKING_ITEMS (updates) | Mutable — updated at each session handoff | Current pointers, program state, active rulings, immediate next actions |

**Flow:** ORCHESTRATOR creates both files during workspace initialization → WORKING_ITEMS reads both at session start (Phase 0a) → WORKING_ITEMS updates `NEXT_INSTANCE_STATE.md` at session end (standing authorization) → CHANGE verifies state before committing.

### 6.3 Spawning Mechanisms

| Mechanism | Used By | Details |
|-----------|---------|---------|
| **Human-gated phases** | ORCHESTRATOR | Sequential phases with human confirmation between each; passes parameter sets to spawned agents |
| **Pre-authorized dispatch** | WORKING_ITEMS | TASK agents dispatched autonomously after human confirms session objective; no per-task approval |
| **Human-directed toolbelt** | RECONCILIATION | Only agents listed in human-provided TOOLBELT may be dispatched; formal 9-field brief schema; max one task per cycle by default |
| **Approval-gated execution** | CHANGE | Explicit approval tokens (`APPROVE:` / `APPROVE_DESTRUCTIVE:`) required before any state-changing action |

---

## 7. Write Scope Architecture

### 7.1 Scope Categories

The write scope model enforces separation between source truth and derived outputs.

```
NONE (read-only; may draft content for human to apply)
├── HELPS_HUMANS
├── DECOMP_BASE
└── HELP_HUMAN

REPO-METADATA-ONLY (instruction files, README, templates — not execution truth)
├── DOMAIN_DECOMP
├── CONTEXT_TRANSPOSE
└── TOOLMAKER

PROJECT-LEVEL (decomposition documents, metadata files, folder scaffolding)
├── PROJECT_DECOMP
├── SOFTWARE_DECOMP
├── SCOPE_CHANGE
├── PREPARATION
└── ESTIMATE_PREP

DELIVERABLE-LOCAL (single production unit folder only)
├── WORKING_ITEMS (+NEXT_INSTANCE_STATE.md standing exception)
├── 4_DOCUMENTS
├── DOMAIN_DOCUMENTS
├── CHIRALITY_FRAMEWORK
├── CHIRALITY_LENS
├── DEPENDENCIES (dep artifacts only)
├── TASK
└── REVIEW (+tool-root for snapshots)

TOOL-ROOT-ONLY (derived outputs under execution tool roots)
├── ORCHESTRATOR           → _Coordination/
├── RECONCILIATION         → _Reconciliation/
├── CHANGE                 → _Change/ (+repo files with approval gate)
├── SCHEDULING             → _Schedule/
├── ESTIMATING             → _Estimates/
├── AGGREGATION            → _Aggregation/
├── EVALUATION             → _Evaluation/
├── AUDIT_AGENTS           → _Reconciliation/AgentAudit/
├── AUDIT_DECOMP           → _Reconciliation/DecompCoverage/
├── AUDIT_DEP_CLOSURE      → _Reconciliation/DepClosure/
├── AUDIT_HYPERGRAPH_CLOSURE → _Reconciliation/HypergraphClosure/
├── DOMAIN_HYPERGRAPH      → _Aggregation/Hypergraph/
├── CONTENT_DIGEST         → _Evaluation/content-digests/
├── EVALUATION_REPORT      → _Evaluation/reports/
├── EVALUATION_STRUCTURE_AUDIT → _Evaluation/reports/
└── EVALUATION_DEPENDENCY_AUDIT → _Evaluation/reports/
```

### 7.2 Write Scope Rules

1. Every agent declares its write scope in the Agent Header Block.
2. Deliverable-local agents cannot write outside their assigned production unit folder.
3. Tool-root agents write only to their designated tool root under `{EXECUTION_ROOT}/`.
4. Source truth (deliverable production documents) is never modified by tool-root agents.
5. `_STATUS.md` updates are restricted to designated agents (PREPARATION, 4_DOCUMENTS, CHIRALITY_FRAMEWORK, REVIEW) and only for forward lifecycle transitions.
6. Cross-deliverable scanning/editing is prohibited inside WORKING_ITEMS sessions unless the human explicitly requests a cross-check.

---

## 8. Decomposition System

### 8.1 Base Protocol (DECOMP_BASE)

All decomposition agents conform to an invariant 7-gate conversational workflow:

| Phase | Name | Goal | Gate Question |
|-------|------|------|---------------|
| 1 | **Intake** | Capture source material faithfully | "Does this reflect the source material and context as intended?" |
| 2 | **Normalize** | Convert source → atomic units + vocabulary | "Are the atomic units, classifications (IN/OUT/TBD), and vocabulary correct?" |
| 3 | **Objectives** | Derive success criteria from source | "Do these objectives represent success as intended?" |
| 4 | **Partitions** | Flat groupings — no nesting, no overlaps, no gaps | "Are partitions correct? Does each IN-scope unit belong to exactly one?" |
| 5 | **Production Units** | Operationalize each partition into bounded work units | "Are production units (granularity, types, responsibilities) acceptable?" |
| 6 | **Coverage** | Prove completeness; surface gaps | "Are coverage, mappings, and open issues acceptable?" |
| 7 | **Publish** | Finalize as accepted decomposition | "Is this the accepted basis for downstream work?" |

### 8.2 Required Output Sections (All Decompositions)

Every decomposition document must include:

1. **Vocabulary Map** — canonical terms, synonyms, notes (prevents semantic drift)
2. **Decomposition Ledger** — machine-checkable table mapping every atomic unit to partition and production unit
3. **Coverage & Telemetry** — counts, gap metrics, open issue taxonomy
4. **Open Issues** — unresolved items referencing stable IDs
5. **Decision Log** — non-trivial assignment decisions for traceability

### 8.3 Ledger Contract

The Decomposition Ledger has these minimum columns:

`UnitID`, `InOutStatus` (IN|OUT|TBD), `UnitStatement`, `SourceRef`, `PartitionID`, `ProductionUnitID(s)`, `ObjectiveID(s)`, `DecisionRef`, `OpenIssue` (TRUE|FALSE), `Notes`

**Hard rule:** Every IN-scope UnitID has exactly one PartitionID.

### 8.4 Three Conforming Variants

| Dimension | PROJECT_DECOMP | SOFTWARE_DECOMP | DOMAIN_DECOMP |
|-----------|---------------|-----------------|---------------|
| **Domain** | EPC / design-build | Software development | Handbook / knowledge |
| **Source Corpus** | SOW (Scope of Work) | SOW (Scope of Work) | Handbook |
| **Structured Outline** | SSOW | SSOW | SDO |
| **Atomic Unit** | Scope Item (`SOW-####`) | Scope Item (`SOW-###`) | Handbook Unit (`HBK-####`) |
| **Partition** | Package (`PKG-XXX`, 3-digit) | Package (`PKG-XX`, 2-digit) | Category (`CAT-###`, 3-digit) |
| **Production Unit** | Deliverable (`DEL-XXX-YY_{desc}`) | Deliverable (`DEL-XX-YY`) | Knowledge Type (`KTY-CC-TT_{desc}`) |
| **ID coupling** | DEL first 3 digits = PKG digits | DEL first 2 digits = PKG digits | KTY `CC` = CAT index, `TT` = type index |
| **Production documents** | Fixed 4-doc set | Fixed 4-doc set | Variable Knowledge Artifacts |
| **Dependency graph** | Yes | Yes | No |
| **Unique constraint** | Discipline-exclusive design packages | Context Envelope sizing (S/M/L/XL mandatory) | Canonical knowledge schemas (5 types) |
| **Telemetry extension** | — | ContextEnvelopeCounts (S/M/L/XL breakdown) | — |

### 8.5 Extension Contract

A conforming decomposition agent must provide:

1. Reference to `AGENT_DECOMP_BASE.md` (state conformance)
2. Entity binding table (abstract → domain-specific terms)
3. ID formats and width specifications
4. Production unit type taxonomy
5. Phase-specific extensions (domain actions, outputs, gate language)
6. WRITE_SCOPE declaration
7. Domain-specific fields, anti-patterns, and SPEC requirements
8. Domain-specific telemetry fields

### 8.6 How Variants Combine

- **SOFTWARE_DECOMP extends any branch.** If a branch has software to build, SOFTWARE_DECOMP decomposes that software component. Can recursively extend other SOFTWARE_DECOMP branches.
- **DOMAIN_DECOMP runs parallel to any branch.** It captures the knowledge domain a branch operates within — orthogonal to the work decomposition. Can recursively parallel other DOMAIN_DECOMP branches.

---

## 9. Brief & Output Contracts

### 9.1 INIT-TASK Brief Format (Type 2 Standard)

All Type 2 agents accept a structured brief. The recommended template:

```
PURPOSE: <what the run is for>
SCOPE: <deliverable IDs / package IDs / paths>
WHERE_TO_LOOK: <roots / patterns>
OUTPUT_LABEL: <optional>
CONFIG: <optional; validated enums driving behavior>
CONSTRAINTS: <schema, naming, maturity>
EXCLUSIONS: <paths / patterns>
NOTES: <anything else>
```

### 9.2 Agent-Specific Brief Extensions

| Agent | Key Additional Parameters |
|-------|--------------------------|
| **PREPARATION** | Task type (A–G), PKG_ID, DEL_ID, CAT_ID, KTY_ID |
| **4_DOCUMENTS** | DELIVERABLE_PATH, DECOMPOSITION_REF, RUN_PASSES (FULL/P1_P2/P3_ONLY), ALLOW_OVERWRITE_STATES, DECOMP_VARIANT |
| **DOMAIN_DOCUMENTS** | KTY_PATH, UNIT_SCOPE (EXAMPLES_ONLY/ALL_MAPPED), ARTIFACT_NAMING, MAX_ARTIFACTS |
| **DEPENDENCIES** | MODE (UPDATE/RESET_EXTRACTED), STRICTNESS (CONSERVATIVE/AGGRESSIVE), CONSUMER_CONTEXT, SOURCE_DOCS |
| **CHIRALITY_FRAMEWORK** | deliverable_folder, decomposition_path, DECOMP_VARIANT |
| **CHIRALITY_LENS** | deliverable_folder, DECOMP_VARIANT |
| **ESTIMATING** | BASIS_OF_ESTIMATE (QUOTE/RATE_TABLE/HISTORICAL/PARAMETRIC/ALLOWANCE), CURRENCY, PRICE_SOURCES |
| **ESTIMATE_PREP** | PHASE (SCAFFOLD/BOE), PROJECT_CONTEXT, HUMAN_PRICING |
| **AGGREGATION** | PURPOSE, PIPELINE_ID, currency normalization policy |
| **TASK** | DeliverablePath, ApplyEdits, UseSemanticLensing, permission flags |
| **AUDIT_AGENTS** | FILES_TO_AUDIT, CANON_FILE, RUBRIC_FILE |
| **AUDIT_DECOMP** | DECOMPOSITION_PATH, DECOMP_VARIANT, SCOPE |
| **AUDIT_DEP_CLOSURE** | SCOPE, EDGE_FILTER, HUB_THRESHOLD |
| **DOMAIN_HYPERGRAPH** | EXECUTION_ROOT, SCOPE (CAT/KTY IDs or ALL), DECOMPOSITION_PATH, LEDGER_PATH, OBJECTIVE_MAP_PATH |
| **AUDIT_HYPERGRAPH_CLOSURE** | HYPERGRAPH_REF, REQUIRE_LEDGER_CHECKS, STRICT_MODE |

### 9.3 RECONCILIATION's Formal Brief Schema (Most Structured)

RECONCILIATION defines a 9-field schema for all Type 2 dispatches:

```
REQUESTED_BY, RUN_LABEL, EXECUTION_ROOT, SCOPE, INPUT_ARTIFACTS,
OUTPUT_REQUIREMENTS, ACCEPTANCE_CRITERIA, CONSTRAINTS, ESCALATION
```

### 9.4 Snapshot Output Convention

All snapshot-producing agents follow this pattern:

```
{TOOL_ROOT}/{AGENT_PREFIX}_{RUN_LABEL}_{YYYY-MM-DD}_{HHMM}/
├── Brief.md              # Verbatim brief inputs
├── RUN_SUMMARY.md        # What happened
├── QA_Report.md          # Schema validity, coverage, provenance, warnings
├── Decision_Log.md       # Non-trivial decisions
├── <agent-specific outputs>
└── Evidence/             # (where applicable) supporting CSV/data files

{TOOL_ROOT}/_LATEST.md    # Mutable pointer to latest snapshot
```

**Rules:**
- Each run writes a new snapshot folder with unique timestamp
- Snapshots are never modified or overwritten after creation
- `_LATEST.md` may be overwritten; it is a convenience pointer
- Snapshots form an immutable audit trail

---

## 10. Variant Coverage Matrix

Not all agents operate across all decomposition variants.

| Agent | PROJECT | SOFTWARE | DOMAIN | Variant-Independent |
|-------|:-------:|:--------:|:------:|:-------------------:|
| **DECOMP agents** | PROJECT_DECOMP | SOFTWARE_DECOMP | DOMAIN_DECOMP | — |
| **ORCHESTRATOR** | yes | yes | yes | — |
| **PREPARATION** | yes | yes | yes | — |
| **4_DOCUMENTS** | yes | yes | — | — |
| **DOMAIN_DOCUMENTS** | — | — | yes | — |
| **CHIRALITY_FRAMEWORK** | yes | yes | yes | — |
| **CHIRALITY_LENS** | yes | yes | yes | — |
| **DEPENDENCIES** | yes | yes | — | — |
| **ESTIMATING** | yes | yes | — | — |
| **ESTIMATE_PREP** | yes | yes | — | — |
| **SCHEDULING** | yes | yes | — | — |
| **AGGREGATION** | yes | yes | yes | — |
| **AUDIT_DEP_CLOSURE** | yes | yes | — | — |
| **DOMAIN_HYPERGRAPH** | — | — | yes | — |
| **AUDIT_HYPERGRAPH_CLOSURE** | — | — | yes | — |
| **AUDIT_DECOMP** | yes | yes | yes | — |
| **WORKING_ITEMS** | yes | yes | yes | — |
| **TASK** | yes | yes | yes | — |
| **REVIEW** | yes | yes | yes | — |
| **SCOPE_CHANGE** | yes | yes | — | — |
| **RECONCILIATION** | yes | yes | yes | — |
| **CHANGE** | — | — | — | yes |
| **HELP_HUMAN** | — | — | — | yes |
| **HELPS_HUMANS** | — | — | — | yes |
| **DECOMP_BASE** | — | — | — | yes |
| **AUDIT_AGENTS** | — | — | — | yes |
| **CONTEXT_TRANSPOSE** | — | — | — | yes |

Agents that support multiple variants use `DECOMP_VARIANT` auto-detection: folder name prefix `KTY-` → DOMAIN; otherwise PROJECT/SOFTWARE.

---

## 11. Canonical Patterns

These recurring design patterns appear across the agent suite and define the system's behavioral vocabulary.

### 11.1 Immutable Snapshot + Pointer

All Type 2 agents that produce analysis outputs write to a timestamped snapshot folder that is never modified. A mutable `_LATEST.md` pointer file provides convenient access to the most recent snapshot. The snapshot trail is the audit trail.

### 11.2 Evidence-First Epistemology

Every non-trivial claim includes `SourcePath` + `SectionRef` (or explicit `location TBD`). Epistemic labels distinguish known facts from inferences: `FACT`, `ASSUMPTION`, `PROPOSAL`, `TBD`. No agent may claim certainty without evidence.

### 11.3 Conflict Table

When sources disagree, agents produce a Conflict Table:

| Column | Content |
|--------|---------|
| ConflictID | Stable identifier |
| Key | What is in conflict |
| Contenders | Paths/references to competing claims |
| ProposedAuthority | Agent's recommendation (labeled PROPOSAL) |
| HumanRuling | Remains `TBD` until human decides |

Agents never silently resolve conflicts. The human owns the ruling.

### 11.4 Gate-Controlled Workflow (Type 1)

Type 1 agents use numbered phases with explicit gate questions. Each gate pauses for human confirmation. No gate may be skipped. The gate question makes the decision explicit and recorded.

### 11.5 Straight-Through Execution (Type 2)

Type 2 agents run start-to-finish without human interaction. Invalid inputs → `FAILED_INPUTS` (halt). Missing data → `TBD` (continue conservatively). Output includes a run report with PASS/FAIL status and warnings.

### 11.6 Session Handoff (Control Loop)

ORCHESTRATOR creates durable handoff artifacts → WORKING_ITEMS reads at session start and updates at session end → CHANGE verifies state before commit. This enables continuity across sessions without hidden state.

### 11.7 Write Quarantine

Every agent declares an explicit write scope. Tool roots are isolated from source truth. Deliverable-local agents write only within their assigned folder. Cross-deliverable writes require explicit routing (RECONCILIATION → CHANGE with approval gate).

### 11.8 No-Autopilot Rule (RECONCILIATION)

RECONCILIATION dispatches at most one Type 2 task per cycle unless the human provides a multi-step run plan. If the TOOLBELT (list of authorized agents) is missing, RECONCILIATION proposes a minimal toolbelt and stops. This prevents runaway orchestration.

### 11.9 Approval Gate (CHANGE)

CHANGE requires explicit approval tokens before any state-changing action:
- Standard: `APPROVE: <explicit action list>`
- Heightened: `APPROVE_DESTRUCTIVE: <explicit action list>` (for force-push, hard reset, etc.)

"Yes" alone is insufficient. The human must enumerate what is approved.

---

## 12. Design Outcomes Required for New Workflows

Per HELPS_HUMANS, any new workflow specification must produce these 8 design outcomes:

1. **System map** — agents, tool roots, lifecycle states, key artifacts
2. **Human agency map** — what humans decide vs what agents execute
3. **Permission map** — write zones; which agents may write where
4. **Brief format** — INIT-TASK template for each straight-through pipeline
5. **Snapshot contract** — what each run writes; how `_LATEST` pointers behave
6. **Schemas** — for registers/tables (required columns, keys, enums)
7. **QA contract** — coverage reporting, conflict surfacing, provenance requirements
8. **Runbooks** — minimal human steps + rerun loop

---

*This document was produced by systematic research across all 38 agent instruction files and the governance documents in `docs/`. The operational architecture described here is what results when the four philosophical pillars — ontology, epistemology, praxiology, and axiology (`DIRECTIVE.md` §2) — are implemented as an agent instruction system. The systems engineering disciplines that pervade this architecture — formal interface contracts, invariant systems, fault containment zones, V-model traceability, gate-controlled workflows, and evidence-first epistemology — are not compliance artifacts applied after the fact. They are the necessary consequences of the four-pillar commitments: the only way those commitments can be made architecturally real. See `SE_Design_Analysis.md` for the detailed characterization and the generative mapping from pillars to SE disciplines.*
