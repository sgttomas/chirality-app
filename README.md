# Chirality

A formally specified agent operating system for deliverable-heavy professional work.

Chirality is a desktop harness for running AI agents against a user-selected folder on the local filesystem. It bundles a release-managed instruction architecture inside the app and lets users point the runtime at any working directory where agents read and write state as plain files.

The core insight: **if the filesystem is the database, architecture is a state-and-authority specification, not a service mesh.**

---

## What This System Does

Chirality accelerates deliverable-heavy work — EPC, design-build, proposals, domain knowledge curation, and similar environments — by structuring agent workflows around production deliverables. It makes agentic work auditable and controllable so that outputs can be relied upon in professional, regulated, and high-stakes contexts.

Agents decompose scope into packages and deliverables, scaffold workspaces, draft document kits, extract and track dependencies, perform semantic analysis, reconcile across deliverables, generate cost estimates and schedules, and manage change — all under human authority at every decision gate.

Chirality is intentionally opinionated. Its controls were shaped by recurrent failure modes in real deliverable work: unclear authority, undocumented decisions, broken traceability, overwritten state, silent contradictions, and plausible but weakly grounded claims. Each major constraint exists to make one of those failures harder to repeat.

It is presented here as one rigorous, governance-first implementation for AI-assisted deliverable work, not as the only possible model.

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

### Agents, Teams, and Governance

In Chirality, "agent" first has a narrow technical meaning: `LLM + instructions + access to files + use of tools`. In regulated practice, those same agents are also treated as "others" whose work a human professional supervises, reviews, and decides whether to rely on.

Once those agents are arranged into Type 0 / 1 / 2 roles, decomposition trees, lifecycle states, dependency links, reviews, and change controls, the system becomes a form of project management. This is not an accidental resemblance. The folder structure is the project structure, and the project structure is part of the epistemic architecture.

The same pattern appears in governance. Chirality distinguishes normative, operative, and evaluative roles so that rule-setting, execution, and review are related but not collapsed. This is one reason the system's matrix and hierarchy feel closer to an organization than to a loose collection of prompts.

### Deliverable Lifecycle

Production units progress through a local lifecycle tracked in `_STATUS.md`:

```
OPEN -> INITIALIZED -> SEMANTIC_READY -> IN_PROGRESS -> CHECKING -> ISSUED
```

Stage gates (30/60/90/IFC) are human-managed milestones and are not lifecycle states.

---

## Agent Suite

The system ships agent instruction files organized across a 3x4 matrix (see [`AGENTS.md`](AGENTS.md) for the full index and current count):

|  | **Guiding** | **Applying** | **Judging** | **Reviewing** |
|:---|:---|:---|:---|:---|
| **Normative** | HELP_HUMAN | ORCHESTRATOR | WORKING_ITEMS | AGGREGATION |
| **Operative** | DECOMP\* | PREPARATION | TASK | AUDIT\* |
| **Evaluative** | HELPS_HUMANS | — | CHANGE | RECONCILIATION |

Normative and Evaluative agents open interactive workbench sessions. Operative agents run as pipelines.

The suite covers decomposition (3 domain variants sharing a common 7-gate protocol), workspace scaffolding, document drafting, dependency extraction, semantic analysis, cost estimation, scheduling, review, change management, reconciliation, and project evaluation. Reusable bounded-task methods are codified as repo-native skills under `skills/`.

See [`AGENTS.md`](AGENTS.md) for the full agent index and classification. See [`docs/DBM_Agent_Instruction_Architecture.md`](docs/DBM_Agent_Instruction_Architecture.md) for the design basis. See [`docs/REPO_INVENTORY.md`](docs/REPO_INVENTORY.md) for current governed counts.

---

## Deterministic Tools

The `tools/` directory contains deterministic tools that agents invoke during pipeline execution. These tools codify LLM-independent operations — filesystem scaffolding, schema validation, CSV aggregation, graph analysis, PDF conversion, drawing extraction — so that agents reserve LLM reasoning for content that requires judgment.

The tool registry at [`tools/REGISTRY.md`](tools/REGISTRY.md) indexes all available tools. Many agent instructions reference tools from the registry in their PROTOCOL sections. See [`docs/REPO_INVENTORY.md`](docs/REPO_INVENTORY.md) for the current tool count.

---

## Governance Documents

The repo's governance and specification documents include:

| Document | Purpose |
|----------|---------|
| [`DIRECTIVE.md`](docs/DIRECTIVE.md) | Founding intent, design philosophy, professional responsibility model, scope, and structural constraints |
| [`SPEC.md`](docs/SPEC.md) | Physical structures, file formats, schemas (Dependencies.csv v3.1), folder layout, and validation checklists |
| [`TYPES.md`](docs/TYPES.md) | Domain vocabulary, stable identifier formats, enumerated types, agent roles, and lifecycle states |
| [`CONTRACT.md`](docs/CONTRACT.md) | Invariant catalog (21 K-* invariants) with enforcement map |
| [`PLAN.md`](docs/PLAN.md) | Development roadmap, hardening status, and remaining gaps |
| [`DBM_Agent_Instruction_Architecture.md`](docs/DBM_Agent_Instruction_Architecture.md) | Design basis memorandum for the full instruction architecture |
| [`SE_Design_Analysis.md`](docs/SE_Design_Analysis.md) | Systems engineering design analysis across eight SE disciplines |
| [`REPO_INVENTORY.md`](docs/REPO_INVENTORY.md) | Canonical mutable counts for indexed agents, repo-native skills, and registered deterministic tools |
| [`CHIRALITY_FRAMEWORK.md`](CHIRALITY_FRAMEWORK.md) | Philosophical framework: knowledge as warranted accountability, four pillars, epistemic ontology |
| [`PROFESSIONAL_ENGINEERING.md`](PROFESSIONAL_ENGINEERING.md) | Professional practice standard for AI agent governance under APEGA |

---

## Invariant System

The architecture is governed by three layers of formally stated invariants:

- **R1–R12 (Workflow-Component Design Requirements)** — Apply to all agents, skills, and tools. Defined in `AGENT_HELPS_HUMANS.md`.
- **I1–I10 (Decomposition Invariants)** — Apply to all decomposition agents. Defined in `AGENT_DECOMP_BASE.md`.
- **K-\* (System-Wide Invariants)** — 21 named invariants covering hierarchy, authority, sealing, dependencies, status, staleness, gates, merge, provenance, claim strength, and write scope. Defined in [`docs/CONTRACT.md`](docs/CONTRACT.md).

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
  agents/              Agent instruction files (AGENT_*.md)
  skills/              Repo-native skills (reusable bounded-task methods)
  tools/               Deterministic tools + REGISTRY.md (organized by category)
  docs/                Governance documents (DIRECTIVE, SPEC, TYPES, CONTRACT, PLAN, DBM, SE Analysis)
  frontend/            Next.js + Electron desktop application
  AGENTS.md            Agent index and matrix
  INIT.md              Agent bootstrap context
  PROFESSIONAL_ENGINEERING.md  Standard for AI in regulated engineering practice
  LICENSE.md           MIT License + Professional Engineering Clause
```

---

## Design Philosophy

The architecture rests on four philosophical pillars: an **ontology** (what exists — the filesystem-as-graph where folders are nodes, dependency rows are edges, and markdown files carry properties), an **epistemology** (what can be known — mandatory provenance, no invention, conflict surfacing, and epistemic labeling that makes the certainty of every claim transparent), a **praxiology** (how work is done — gate-controlled workflows, write quarantine, brief-driven pipelines, and the Type 0/1/2 authority hierarchy), and an **axiology** (what the system values — public welfare first, professional responsibility non-transferable, evidence over plausibility).

The foundational decision is that the filesystem is the database. This is not a simplification. It is the mechanism that enables the system's approach to V-model traceability, immutable snapshots, change propagation, content-addressed approval, and a complete audit trail that requires no infrastructure beyond version control.

The most distinctive pillar is the epistemology. Chirality does not assume model output is trustworthy by inspection. Instead, it makes the status of claims structurally visible: provenance is mandatory, unknowns become `TBD` rather than guesses, conflicts are surfaced rather than silently resolved, and claims are labeled as `FACT`, `ASSUMPTION`, `PROPOSAL`, or `TBD`.

The systems engineering disciplines that govern this architecture are integral to the agent system, not a compliance layer applied after the fact. The four-document kit that agents produce for every deliverable — Datasheet (ontology), Specification (epistemology), Guidance (axiology), Procedure (praxiology) — mirrors the same structure. The system practices what it produces.

The architecture exists so that a licensed professional can direct AI agents with the same rigor applied to managing any engineering team — and can authenticate the resulting work product under duty of care, backed by an auditable record. See [`CHIRALITY_FRAMEWORK.md`](CHIRALITY_FRAMEWORK.md) for the philosophical account of knowledge, agency, project management, and governance, and [`docs/DIRECTIVE.md`](docs/DIRECTIVE.md) §2 for the system design principles derived from it.

> AI can accelerate engineering work. It cannot inherit professional responsibility.

---

## License

MIT License + Professional Engineering Clause. See [LICENSE.md](LICENSE.md).

Copyright (c) 2026 Ryan Tufts
