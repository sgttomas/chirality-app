# Chirality

A formally specified agent operating system for deliverable-heavy professional work.

Chirality is a desktop harness for running AI agents against a user-selected folder on the local filesystem. It bundles a release-managed instruction architecture inside the app and lets users point the runtime at any working directory where agents read and write state as plain files.

The core insight: **if the filesystem is the database, architecture is a state-and-authority specification, not a service mesh.**

---

## What This System Does

Chirality accelerates deliverable-heavy work — EPC, design-build, proposals, domain knowledge curation, and similar environments — by structuring agent workflows around production deliverables. It makes agentic work auditable and controllable so that outputs can be relied upon in professional, regulated, and high-stakes contexts.

Agents decompose scope into packages and deliverables, scaffold workspaces, draft document kits, extract and track dependencies, perform semantic analysis, reconcile across deliverables, generate cost estimates and schedules, and manage change — all under human authority at every decision gate.

---

## Architecture

### Filesystem Is the State

All project truth lives in git-tracked plain files. There is no external database. Deliverable folders contain identity, lifecycle state, dependencies, references, working memory, and production documents. Agents traverse this implicit graph on demand. Analysis artifacts are materialized as markdown and CSV and git-committed for auditability.

If a decision is not in a versioned file, it does not exist for purposes of reliance.

### Instruction Root / Working Root Separation

The system separates the agent operating system (release-managed instruction files and governance documents bundled with the app) from the working root (user-selected filesystem location where agents execute). This preserves a stable agent OS while keeping project execution fully filesystem-native in user-controlled folders.

### Type 0 / 1 / 2 Agent Hierarchy

Agents are organized into three types with distinct responsibilities:

| Type | Role | Function |
|------|------|----------|
| **Type 0 — Architect** | Defines and maintains invariant protocols and design standards | Constitutional layer; all other agents must conform |
| **Type 1 — Manager** | Interactive personas with gate-controlled workflows | Orchestrates work, spawns specialists, human-facing |
| **Type 2 — Specialist** | Brief-driven, straight-through task execution | Bounded scope, no mid-run gates, auditable outputs |

Authority flows downward; escalation flows upward. A Type 2 agent cannot modify rules set by Type 0. A Type 1 agent cannot approve deliverables for external reliance. Human gates cannot be bypassed by any type.

### Deliverable Lifecycle

Production units progress through a local lifecycle tracked in `_STATUS.md`:

```
OPEN -> INITIALIZED -> SEMANTIC_READY -> IN_PROGRESS -> CHECKING -> ISSUED
```

Stage gates (30/60/90/IFC) are human-managed milestones and are not lifecycle states.

---

## Agent Suite

The system ships 29 agent instruction files organized across a 3x4 matrix:

|  | Guiding | Applying | Judging | Reviewing |
|:---|:---|:---|:---|:---|
| **Normative** | HELP | ORCHESTRATE | WORKING_ITEMS | AGGREGATE |
| **Operative** | DECOMP | PREP | TASK | AUDIT |
| **Evaluative** | AGENTS | DEPENDENCIES | CHANGE | RECONCILING |

Normative and Evaluative agents open interactive workbench sessions. Operative agents run as pipelines.

### Decomposition Agents

Three decomposition variants share a common 7-gate protocol (`DECOMP_BASE`):

- **PROJECT_DECOMP** — EPC / design-build projects (Packages / Deliverables)
- **SOFTWARE_DECOMP** — Software development (Work Domain Packages / Deliverables with Context Envelope sizing)
- **DOMAIN_DECOMP** — Handbook / knowledge domains (Categories / Knowledge Types)

### Preparation and Document Agents

- **PREPARATION** — Scaffolds package and deliverable folders with minimum viable fileset
- **4_DOCUMENTS** — Drafts the standard four-document kit (Datasheet, Specification, Guidance, Procedure)
- **DOMAIN_DOCUMENTS** — Produces scoping and knowledge artifact files for domain decompositions
- **CHIRALITY_FRAMEWORK / CHIRALITY_LENS** — Semantic analysis and enrichment

### Execution Agents

- **WORKING_ITEMS** — Interactive deliverable-scoped content production
- **TASK** — Brief-driven execution against authorized deliverable-local files
- **DEPENDENCIES** — Extracts and maintains structured dependency registers (29-column CSV v3.1 schema)
- **ESTIMATING / ESTIMATE_PREP** — Parameterized cost estimation
- **SCHEDULING** — Schedule generation from the dependency graph
- **SCOPE_CHANGE** — Change impact assessment and decomposition amendment

### Quality and Coordination Agents

- **ORCHESTRATOR** — Coordinates project setup, tier sequencing, and control loops
- **RECONCILIATION** — Cross-deliverable coherence analysis
- **REVIEW** — Formal 5-gate review process for lifecycle transitions
- **CHANGE** — Git state management with explicit approval gates
- **AUDIT agents** — Conformance checking for decomposition, dependencies, agents, and hypergraph closure

---

## Governance Documents

The `docs/` directory contains the formal specification hierarchy:

| Document | Purpose |
|----------|---------|
| [`DIRECTIVE.md`](docs/DIRECTIVE.md) | Founding intent, design philosophy, professional responsibility model, scope, and structural constraints |
| [`SPEC.md`](docs/SPEC.md) | Physical structures, file formats, schemas (Dependencies.csv v3.1), folder layout, and validation checklists |
| [`TYPES.md`](docs/TYPES.md) | Domain vocabulary, stable identifier formats, enumerated types, agent roles, and lifecycle states |
| [`CONTRACT.md`](docs/CONTRACT.md) | Invariant catalog (23 K-* invariants) with enforcement map |
| [`PLAN.md`](docs/PLAN.md) | Development roadmap and future hardening candidates |
| [`DBM_Agent_Instruction_Architecture.md`](docs/DBM_Agent_Instruction_Architecture.md) | Design basis memorandum for the full instruction architecture |
| [`SE_Design_Analysis.md`](docs/SE_Design_Analysis.md) | Systems engineering design analysis across eight SE disciplines |

---

## Invariant System

The architecture is governed by three layers of formally stated invariants:

**R1-R9 (Workflow Design Requirements)** — Apply to all agents: human decision rights, straight-through tasks, write quarantine, immutable snapshots, mandatory provenance, no invention, conflict surfacing, brief-driven execution, hygienic publication.

**I1-I10 (Decomposition Invariants)** — Apply to all decomposition agents: human-validated decomposition, no invention, flat partitions, no overlap / no gaps, stable identifiers, deterministic ID coupling, objective mapping, traceable rationale, ledger + telemetry, vocabulary discipline.

**K-* (System-Wide Invariants)** — 23 named invariants defined in `CONTRACT.md` covering hierarchy, authority, sealing, dependencies, status, staleness, gates, merge, provenance, invention, conflicts, write scope, and snapshots.

Key invariants:

- **K-AUTH-1** — Only humans author binding approval records
- **K-GHOST-1** — Type 2 context is limited to folder contents + declared references
- **K-INVENT-1** — Unknown values become `TBD`, not guessed
- **K-PROV-1** — Every extracted dependency row must cite evidence
- **K-WRITE-1** — Every agent has an explicit write scope; no agent writes outside its declared zone

---

## Desktop Application

The `frontend/` directory contains a Next.js + Electron desktop application with:

- Matrix-based navigation routing agents to Workbench (interactive) or Pipeline (task execution) views
- Session and turn API with streaming event protocol (SSE)
- Multimodal turn input via server-resolved file attachments
- Pipeline category selectors (DECOMP, PREP, TASK, AUDIT) with dynamic scope resolution
- Operator Toolkit panel for per-turn harness options
- Desktop packaging for macOS (`.dmg`) and Windows (`.exe`)

---

## Project Structure

```
chirality-app/
  agents/              29 agent instruction files (AGENT_*.md)
  docs/                Governance documents (DIRECTIVE, SPEC, TYPES, CONTRACT, PLAN, DBM, SE Analysis)
  frontend/            Next.js + Electron desktop application
  examples/            Execution-root samples for regression and conformance testing
  design/              Design artifacts
  init/                Initialization resources
  AGENTS.md            Operator-facing agent index and rules of the road
  INIT.md              Agent bootstrap context
  WHAT-IS-AN-AGENT.md  Conceptual primer on the Type 0/1/2 model
  PROFESSIONAL_ENGINEERING.md  Standard for AI in regulated engineering practice
  LICENSE.md           MIT License + Professional Engineering Clause
```

---

## Design Philosophy

The systems engineering content of this architecture is not incidental — it is the architecture. The instruction files are formal specifications that define interfaces, state machines, invariants, preconditions, postconditions, containment zones, and authority boundaries.

What distinguishes Chirality from a conventional agent system is that SE disciplines are not bolted on as compliance artifacts — they are the mechanism by which agents coordinate, the means by which failures are contained, and the basis on which humans maintain authority.

AI outputs are drafts and structured assistance, not authoritative engineering judgment. Human acceptance is what makes them engineering work product.

> AI can accelerate engineering work. It cannot inherit professional responsibility.

---

## License

MIT License + Professional Engineering Clause. See [LICENSE.md](LICENSE.md).

Copyright (c) 2026 Ryan Tufts
