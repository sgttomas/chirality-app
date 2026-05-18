# Chirality

Chirality is a governed, filesystem-native agent operating system for deliverable-heavy professional work.

It is built for work where outputs need to be inspectable, reviewable, and suitable for human professional judgment: EPC and design-build execution, proposals, domain knowledge curation, document production, extraction, audit, review, and publication workflows.

The core insight:

> If the filesystem is the database, architecture is a state-and-authority specification, not a service mesh.

Chirality is not an autonomous swarm. It is an instruction architecture, tool layer, and desktop harness for directing AI agents under explicit scope, evidence, write-boundary, snapshot, and human-gate rules.

AI can accelerate professional work. It cannot inherit professional responsibility.

---

## What This Repository Contains

This repository publishes the current public operating-system surface for Chirality:

- agent instruction contracts in `agents/`
- repo-native task skills in `skills/`
- deterministic tools in `tools/`
- governance and specification documents in `docs/`
- root-level professional and theoretical framing documents
- sanitized examples under `examples/`
- a Next.js/Electron frontend harness under `frontend/`

The public architecture is intentionally file-first. Agents, skills, and tools operate against a user-selected working root where state is represented as ordinary files and folders. The frontend is a harness for selecting a root, starting sessions, routing work, streaming turns, and packaging the instruction root for desktop use.

---

## Core Model

### Filesystem As State

Project truth lives in git-tracked plain files. Packages, deliverables, references, dependency registers, review records, snapshots, and publication outputs are readable by humans, agents, and deterministic tools without a separate application database.

If a decision is not in a versioned file, it does not exist for purposes of reliance.

### Git As Event Record

Git provides the development record: diffs, review surfaces, rollback points, and content identity. Human approval records bind to specific content, not to a vague conversational state.

### Instruction Root And Working Root

Chirality separates:

- the **instruction root**: release-managed instructions, governance docs, skills, tools, and bootstrap files
- the **working root**: the user-selected project filesystem where agents read and write governed state

That separation keeps the agent operating system stable while execution remains local, inspectable, and under the user's control.

### No Hidden Authoritative Memory

Runtime convenience state may exist for the harness, but authoritative project state must be written to files. Chat context, model memory, browser storage, and application preferences do not override governed project files.

### Human Gates

Agents propose, extract, draft, reconcile, validate, and report. Humans decide, approve, adjudicate conflicts, accept residual risk, and issue work for reliance.

No agent may certify, approve, sign, seal, or issue professional work product.

---

## Epistemic Architecture

Chirality is designed around a professional-accountability problem: model output can sound plausible even when it is unsupported. The system response is not to treat plausibility as reliability. It makes the warrant state of claims visible.

The main mechanisms are:

- **Mandatory provenance:** governed claims cite evidence or carry an explicit missing-location marker.
- **No invention:** unknowns become `TBD`, not guessed values.
- **Conflict surfacing:** contradictory sources produce visible conflicts for human ruling.
- **Epistemic labels:** claims are classified as `FACT`, `ASSUMPTION`, `PROPOSAL`, or `TBD`.

The warrant lifecycle is:

```text
UNWARRANTED -> CITED -> REVIEWED -> AUTHENTICATED
```

The production lifecycle for deliverables is tracked separately:

```text
OPEN -> INITIALIZED -> SEMANTIC_READY -> IN_PROGRESS -> CHECKING -> ISSUED
```

Stage gates such as 30%, 60%, 90%, or IFC are project milestones, not lifecycle states.

---

## Governance Model

Chirality uses three layers of formal constraints:

- **R1-R12:** workflow-component design requirements for agents, skills, and tools, defined by `agents/AGENT_HELPS_HUMANS.md`
- **I1-I10:** decomposition invariants, defined by `agents/AGENT_DECOMP_BASE.md`
- **21 K-* invariants:** system-wide invariants for hierarchy, authority, sealing, dependencies, status, staleness, gates, merge, provenance, claim strength, write scope, and snapshots, defined by `docs/CONTRACT.md`

The architecture also follows five integration rules:

- **Derivative-package rule:** generated packages cite accepted upstream truth and do not replace it.
- **Snapshot rule:** phase-boundary decisions terminate in immutable snapshots and controlled pointer updates where permitted.
- **Handoff-state rule:** unfinished work intended for later phases records upstream snapshots, derivative status, closure verdict, rerun requirements, and blockers.
- **Closure rule:** files being written is not enough; closure requires accepted truth, derivative-package handling, audit state, and surfaced blockers.
- **Sequencing rule:** later phases consume accepted snapshots, not mutable working state alone.

These rules are governance commitments and engineering controls. They are not claims that every future check is hard-enforced by a verified runtime engine.

---

## Agents, Skills, And Tools

### Agents

Agents are instruction contracts: model posture, role, authority, write scope, interaction surface, protocol, and output expectations. The live agent index is `AGENTS.md`; the instruction files live under `agents/`.

The Type 0 / Type 1 / Type 2 model is the authority model:

| Type | Role | Responsibility |
| --- | --- | --- |
| Type 0 | Standards | Define invariant protocols and design standards |
| Type 1 | Managers and personas | Interpret intent, orchestrate workflows, route bounded work, and interact with humans |
| Type 2 | Specialists | Execute bounded briefs and return outputs with evidence |

The matrix in `AGENTS.md` is a governance and routing view. It should not be read as identical to `AGENT_TYPE`, Workbench, or Pipeline behavior in every case.

### TASK

`TASK` is the canonical bounded Type 2 execution shell. It receives structured briefs, resolves scope, hydrates a selected skill when `TaskSkill` is provided, runs within explicit write boundaries, and records durable run output.

### Skills

Skills are repo-native method packs, not agents. A skill tells `TASK` what recurring task shape it is handling, what inputs and runtime overrides matter, which tools are allowed or preferred, what outputs are expected, and how QA should be performed.

The live skill registry is the set of immediate `skills/*/SKILL.md` folders governed by `skills/README.md`. Current registry count: **35 valid skills**.

Each governed skill folder contains:

```text
SKILL.md
BRIEF_SCHEMA.md
TOOL_POLICY.md
QA_CHECKS.md
```

### Tools

Tools are deterministic helpers for repeatable operations: scaffolding, schema validation, PDF and drawing processing, dependency analysis, hypergraph construction, publication assembly, retrieval indexing, source cataloging, and test-surface discovery.

Tools should do deterministic work. LLM reasoning belongs in agents and skills.

`tools/REGISTRY.md` is the curated tool index. The repository also includes validation surfaces that discover current tests and check skill metadata.

---

## Major Workflow Surfaces

Chirality's current public surface includes:

- decomposition workflows for project, software, and domain structures
- workspace scaffolding for packages, deliverables, and tool roots
- document-kit production using Datasheet, Specification, Guidance, and Procedure artifacts
- dependency extraction and closure analysis
- semantic matrix and lensing workflows
- PDF-to-Markdown conversion using `PDF2MD` with `TASK + pdf2md-page-full`
- drawing extraction workflows with deterministic assembly and QA
- equation audit workflows with human review and bounded correction interpretation
- scope-change, remediation, and closure workflows
- domain hypergraph generation
- DBM publication from accepted upstream state
- governance, dependency, epistemic, scope, structure, and evaluation audits

Derivative outputs from these workflows must cite the accepted upstream snapshot they consume. They are evidence packages, reports, indexes, or publication products; they are not substitutes for authoritative decomposition truth.

---

## Frontend Harness

The `frontend/` directory contains a Next.js/Electron harness for operating the instruction architecture against a selected project root. At a concept level, it provides:

- project-root selection
- instruction-root loading
- Workbench and Pipeline routing
- session and turn APIs with streaming events
- operator controls for per-turn harness options
- desktop packaging configuration

Frontend implementation details and selector normalization are expected to continue changing. The architectural source of truth remains the instruction, governance, skill, and tool surface described above.

---

## Governance Documents

Start with these documents:

| Document | Purpose |
| --- | --- |
| `INIT.md` | Bootstrap context and authoritative reading path |
| `AGENTS.md` | Agent matrix, live agent index, and governance integration rules |
| `docs/DIRECTIVE.md` | Founding intent, design philosophy, professional responsibility model, and constraints |
| `docs/SPEC.md` | Physical structures, file formats, schemas, folder layout, frontend contracts, and validation checklists |
| `docs/TYPES.md` | Canonical vocabulary, stable identifiers, enumerated types, roles, and lifecycle states |
| `docs/CONTRACT.md` | 21 K-* invariants and enforcement map |
| `docs/PLAN.md` | Published architectural direction and roadmap themes |
| `docs/DBM_Agent_Instruction_Architecture.md` | Design basis for the workflow-component architecture |
| `CHIRALITY_FRAMEWORK.md` | Theory of professional accountability, knowledge, warrants, and the four pillars |
| `PROFESSIONAL_ENGINEERING.md` | Professional practice standard for governed AI agent use in regulated engineering practice |

The explanatory thesis material under `docs/thesis/` provides broader design argument and context. Live membership and registry questions should be answered from the current root indexes and live folders.

---

## Project Layout

```text
chirality-app/
  agents/       Agent instruction files
  skills/       Repo-native TASK method packs
  tools/        Deterministic tools and validators
  docs/         Governance, specifications, roadmap, and design basis
  examples/     Sanitized example workspaces and artifacts
  frontend/     Next.js/Electron harness
  init/         Session bootstrap and handoff notes

  AGENTS.md
  INIT.md
  CHIRALITY_FRAMEWORK.md
  PROFESSIONAL_ENGINEERING.md
  LICENSE.md
```

---

## Validation

Useful repository-level checks include:

```sh
python3 tools/validation/validate_skill_metadata.py skills
python3 tools/validation/discover_test_surfaces.py . --text
```

The first validates the live skill registry and companion-file contracts. The second reports test surfaces and suggested runner commands by repository convention.

---

## License

MIT License + Professional Engineering Clause. See `LICENSE.md`.

Copyright (c) 2026 Ryan Tufts
