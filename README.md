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

The system ships 37 agent instruction files organized across a 3x4 matrix:

|  | Guiding | Applying | Judging | Reviewing |
|:---|:---|:---|:---|:---|
| **Normative** | HELP | ORCHESTRATE | WORKING_ITEMS | AGGREGATE |
| **Operative** | DECOMP | PREP | TASK | AUDIT |
| **Evaluative** | AGENTS | DEPENDENCIES | CHANGE | RECONCILING |

Normative and Evaluative agents open interactive workbench sessions. Operative agents run as pipelines.

The suite covers decomposition (3 domain variants sharing a common 7-gate protocol), workspace scaffolding, document drafting, dependency extraction, semantic analysis, cost estimation, scheduling, review, change management, reconciliation, and project evaluation.

See [`AGENTS.md`](AGENTS.md) for the full agent index and classification. See [`docs/DBM_Agent_Instruction_Architecture.md`](docs/DBM_Agent_Instruction_Architecture.md) for the design basis.

---

## Deterministic Tools

The `tools/` directory contains 28 shell scripts and Python utilities that agents invoke via Bash during pipeline execution. These tools codify the LLM-independent operations — filesystem scaffolding, schema validation, CSV aggregation, graph analysis — so that agents reserve LLM reasoning for content that requires judgment.

The tool registry at [`tools/REGISTRY.md`](tools/REGISTRY.md) indexes all available tools. 21 of 37 agent instruction files reference tools from the registry in their PROTOCOL sections.

---

## Governance Documents

The `docs/` directory contains the formal specification hierarchy:

| Document | Purpose |
|----------|---------|
| [`DIRECTIVE.md`](docs/DIRECTIVE.md) | Founding intent, design philosophy, professional responsibility model, scope, and structural constraints |
| [`SPEC.md`](docs/SPEC.md) | Physical structures, file formats, schemas (Dependencies.csv v3.1), folder layout, and validation checklists |
| [`TYPES.md`](docs/TYPES.md) | Domain vocabulary, stable identifier formats, enumerated types, agent roles, and lifecycle states |
| [`CONTRACT.md`](docs/CONTRACT.md) | Invariant catalog (20 K-* invariants) with enforcement map |
| [`PLAN.md`](docs/PLAN.md) | Development roadmap and future hardening candidates |
| [`DBM_Agent_Instruction_Architecture.md`](docs/DBM_Agent_Instruction_Architecture.md) | Design basis memorandum for the full instruction architecture |
| [`SE_Design_Analysis.md`](docs/SE_Design_Analysis.md) | Systems engineering design analysis across eight SE disciplines |
| [`CHIRALITY_THEORY.md`](CHIRALITY_THEORY.md) | The Chirality Theory: knowledge as warranted accountability, four pillars, epistemic ontology |
| [`PROFESSIONAL_ENGINEERING.md`](PROFESSIONAL_ENGINEERING.md) | Professional practice standard for AI agent governance under APEGA |

---

## Invariant System

The architecture is governed by three layers of formally stated invariants:

- **R1–R9 (Workflow Design Requirements)** — Apply to all agents. Defined in `AGENT_HELPS_HUMANS.md`.
- **I1–I10 (Decomposition Invariants)** — Apply to all decomposition agents. Defined in `AGENT_DECOMP_BASE.md`.
- **K-\* (System-Wide Invariants)** — 20 named invariants covering hierarchy, authority, sealing, dependencies, status, staleness, gates, merge, provenance, and write scope. Defined in [`docs/CONTRACT.md`](docs/CONTRACT.md).

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
  agents/              37 agent instruction files (AGENT_*.md)
  tools/               28 deterministic tools + REGISTRY.md (shell scripts, Python utilities)
    scaffolding/       Package, deliverable, tool root, snapshot folder creation
    query/             Workspace state, amendment ID scanning
    validation/        Enum, ID format, schema, fileset, doc kit checks
    reporting/         CSV merge, WBS/CBS summarization, coverage, INDEX.md generation
    coordination/      Dependency graph analysis (SCC, orphans, hubs)
    evaluation/        Digest coverage, file inventory, lifecycle states, dependency checks
  docs/                Governance documents (DIRECTIVE, SPEC, TYPES, CONTRACT, PLAN, DBM, SE Analysis)
  frontend/            Next.js + Electron desktop application
  examples/            Execution-root samples for regression and conformance testing
  AGENTS.md            Agent index and matrix
  INIT.md              Agent bootstrap context
  WHAT-IS-AN-AGENT.md  Conceptual primer on the Type 0/1/2 model
  PROFESSIONAL_ENGINEERING.md  Standard for AI in regulated engineering practice
  LICENSE.md           MIT License + Professional Engineering Clause
```

---

## Design Philosophy

The architecture rests on four philosophical pillars: an **ontology** (what exists — the filesystem-as-graph where folders are nodes, dependency rows are edges, and markdown files carry properties), an **epistemology** (what can be known — mandatory provenance, no invention, conflict surfacing, and epistemic labeling that makes the certainty of every claim transparent), a **praxiology** (how work is done — gate-controlled workflows, write quarantine, brief-driven pipelines, and the Type 0/1/2 authority hierarchy), and an **axiology** (what the system values — public welfare first, professional responsibility non-transferable, evidence over plausibility).

The foundational decision is that the filesystem is the database. This is not a simplification. It is the mechanism that makes everything else work: V-model traceability, immutable snapshots, change propagation, content-addressed approval, and a complete audit trail that requires no infrastructure beyond version control.

The most distinctive pillar is the epistemology. The fundamental problem of using LLMs in professional practice is not that they produce bad outputs — it is that bad outputs are indistinguishable from good ones by inspection. Chirality's response is not to make the model more reliable, which cannot be guaranteed. It is to make the epistemic status of every claim transparent and auditable — provenance is mandatory, unknowns become TBD rather than guesses, conflicts are surfaced rather than silently resolved, and every claim carries an epistemic label (FACT, ASSUMPTION, PROPOSAL, TBD). The result: gaps in evidence are findings, not hidden failures.

The systems engineering disciplines that govern this architecture are not a compliance layer applied to an agent system — they ARE the agent system. The instruction files are formal specifications that define interfaces, state machines, invariants, containment zones, and authority boundaries. The governance documents form a coherent specification hierarchy: intent, physical structures, vocabulary, and binding invariants.

The four-document kit that agents produce for every deliverable — Datasheet (ontology), Specification (epistemology), Guidance (axiology), Procedure (praxiology) — mirrors the philosophical structure of the system itself. The system practices what it produces.

The architecture exists so that a licensed professional can direct AI agents with the same rigor applied to managing any engineering team — and can authenticate the resulting work product under duty of care, backed by an auditable record. See [`docs/DIRECTIVE.md`](docs/DIRECTIVE.md) §2 for the full philosophical foundation.

> AI can accelerate engineering work. It cannot inherit professional responsibility.

---

## License

MIT License + Professional Engineering Clause. See [LICENSE.md](LICENSE.md).

Copyright (c) 2026 Ryan Tufts
