# DIRECTIVE — Founding Intent, Scope, and Constraints

This document captures the founding intent, design philosophy, and structural constraints of the Chirality project execution system. It is the "why" document — the principles that govern all other governance documents, agent instructions, and operational decisions.

---

## 1. Founding Intent

Chirality is a desktop harness for running AI agents against a user-selected folder on the local filesystem. It bundles a release-managed "agent operating system" (instructions + framework docs) inside the app, and lets users point the runtime at any working directory where agents read/write state as plain files.

The core insight: **if the filesystem is the database, architecture is a state-and-authority specification, not a service mesh.**

The system exists to:

- **Accelerate deliverable-heavy work** (EPC, design-build, proposals, and similar environments) by structuring agent workflows around production deliverables.
- **Make agentic work auditable and controllable** so that outputs can be relied upon in professional, regulated, and high-stakes contexts.
- **Keep humans in charge** at every decision gate, while letting agents handle the mechanical work of drafting, extracting, reconciling, and organizing.

---

## 2. Design Philosophy

### 2.1 Filesystem Is the Database

Project state lives entirely in git-tracked files. There is no separate database, no server state, no configuration files that diverge from the filesystem.

- **Nodes:** Deliverable folders, package folders.
- **Edges:** Rows in `Dependencies.csv`, ANCHOR rows connecting tree to graph.
- **Properties:** Markdown files (`_STATUS.md`, `_CONTEXT.md`, `Datasheet.md`, etc.).

Agents traverse this implicit graph on-demand. Analysis artifacts are materialized as markdown/CSV and git-committed for auditability.

### 2.2 Git Is the Event Store

Version control provides the development record: meaningful diffs for review, reproducibility, rollback, and audits that do not depend on vendor systems or transient chat context.

If a decision is not in a versioned file, it does not exist for purposes of reliance.

### 2.3 Human Authority at Every Gate

Agents propose; humans approve. Professional liability is personal and non-transferable.

- Only humans author binding approval records.
- Approvals bind to a specific git SHA — content change after approval voids it.
- Human review and sign-off is the decision gate for safety, compliance, and contractual commitments.

### 2.4 Evidence Over Plausibility

Engineering does not accept "sounds right." The system requires:

- Inputs and sources (provenance is mandatory).
- Assumptions explicitly labeled (not hidden in prose).
- Conflicts surfaced, not silently resolved.
- Unknown values become `TBD`, not guessed.

### 2.5 No Hidden Memory

If it is not in a versioned file, it does not exist. Agents must not maintain a hidden database or private state that diverges from the filesystem.

Clarification:

- This constraint applies to **authoritative project execution state** (deliverables, dependencies, approvals, issued artifacts, and gate-relevant records).
- Non-authoritative operator convenience state (for example UI panel state, local turn-option presets, and other ephemeral runtime preferences) MAY be stored outside project files.
- Such convenience state MUST NOT be treated as project truth and MUST NOT override contract/governance enforcement.

### 2.6 Separation of Instruction and Execution

In deployable desktop builds, the system separates:

- **Instruction root:** Release-managed app bundle containing `AGENTS.md`, `README.md`, `agents/*`, and framework docs.
- **Working root (`projectRoot`):** User-selected filesystem location where agents execute and create/update deliverable state.

This preserves a stable agent operating system while keeping project execution fully filesystem-native in user-controlled folders.

---

## 3. Professional Responsibility Model

This section applies when the system is used in environments where deliverables are safety-significant, contractually binding, subject to codes/standards, or produced under professional responsibility.

### 3.1 AI Outputs Are Drafts

Agent outputs are drafts and structured assistance, not authoritative engineering judgment. Human acceptance is what makes them engineering work product.

### 3.2 The Engineer-of-Record Principle

A licensed professional retains decision rights for:

- Scope and boundary decisions.
- Selection of governing codes, standards, and design basis.
- Hazard and risk acceptance, including residual risk statements.
- Conflict adjudication where judgment is required.
- Approval, issuance, signature, seal, and transmittal for reliance.

No AI system may claim to certify, approve, sign, seal, or issue engineering work for reliance.

### 3.3 Competence Includes Tool Competence

An engineer must not use an agent to perform work they are not competent to verify manually. Using AI you cannot adequately verify is a competence failure.

### 3.4 Hierarchy of Authority

In technical matters, agents and engineers follow:

1. Laws and regulations
2. Codes and standards
3. Project specifications / design basis (approved for use)
4. Verified engineering analysis + published literature
5. Professional judgment

Agent outputs carry no professional authority. They are decision support unless explicitly accepted and issued by an accountable professional.

---

## 4. Scope of the System

### 4.1 In Scope

- Project decomposition (from messy scope of work to structured packages and deliverables)
- Workspace scaffolding (folder creation, metadata file initialization)
- Document kit drafting (Datasheet, Specification, Guidance, Procedure)
- Dependency extraction and tracking
- Semantic analysis (lensing and enrichment)
- Cross-deliverable reconciliation
- Cost estimation (parameterized by basis of estimate)
- Schedule generation (parameterized by scheduling basis)
- Aggregation and reporting
- Change management support
- Git-based version control hygiene

### 4.2 Out of Scope

- Automated approval or issuance of deliverables
- Financial transactions or binding commitments
- Safety-critical decisions without human review
- Replacing professional judgment in regulated practice
- External system integration (databases, APIs, cloud services)

---

## 5. Structural Constraints

These constraints are hard to change later. They define the boundaries of the system's architecture.

| Constraint | Rationale |
|-----------|-----------|
| No external database dependency | Filesystem is the single source of truth; eliminates sync burden |
| No server requirement | Desktop-first; works offline; no infrastructure to manage |
| All state as plain files | Human-readable, git-trackable, tool-agnostic |
| Git-trackable artifacts only | Auditability, reproducibility, rollback, diff-based review |
| Flat package hierarchy | No nesting; simplifies automation, coverage checking, and scope assignment |
| Deliverable-local dependency registers | No central dependency graph to maintain; aggregation is on-demand |
| Immutable snapshots for task agent outputs | Reruns are safe; historical outputs are preserved |
| Instruction root separate from working root | Agent instructions are release-managed; project data is user-controlled |

---

## 6. Responsible Use

This framework is designed to support professional responsibility, not replace it.

- Treat agent outputs as drafts and structured assistance.
- Keep human review and sign-off as the decision gate for safety, compliance, and contractual commitments.
- Do not rely on agent outputs without independent verification appropriate to the stakes.

---

EOF
