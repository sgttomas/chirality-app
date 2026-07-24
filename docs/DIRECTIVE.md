# DIRECTIVE — Founding Intent, Scope, and Constraints

> **Status: RATIFIED — owner ratification 2026-07-11 (`CONTRACT.md` / K-AUTH-1).** Owner direction of record (2026-07-11, in-session, Ryan Tufts): "You can now take all the `docs/` out of the DRAFT state, making them authoritative." This document is accepted root governance in full. Provenance: it re-established the monorepo-root governance layer (root `docs/` was hollowed out during the four-repo merge; see `plans/monorepo_root_governance_and_path_anchoring_2026-06-15.md`), authored from the prior root canon (`.archive/DIRECTIVE.md`), updated to the current merged-monorepo topology and the live instruction surface (`AGENTS.md`, `agents/`). **Ratification history:** per D-GOV-05 (`docs/governance_harness/_DECISIONS/D-GOV-05_minimal_governance_basis.md`, ruled by owner 2026-07-01), the source-of-truth and human-authority rules this directive expresses (§2.1, §2.3) were ratified first as the minimal harness basis; the 2026-07-11 full ratification subsumes that partial basis.

This document captures the founding intent, design philosophy, and structural constraints of the Chirality agent operating system. It is the "why" document — the principles that govern all other governance documents, agent instructions, and operational decisions.

**Authority chain.** `DIRECTIVE.md` (this document — *why*) establishes the principles. `CONTRACT.md` binds them as K-* invariants. `SPEC.md` defines physical structures, formats, and path anchoring. `TYPES.md` defines canonical vocabulary. D-GOV-10 rules that workflow-component design be externalized; the exact `WORKFLOW_COMPONENT_STANDARD.md` text is a candidate pending explicit owner acceptance. `PLAN.md` records the active roadmap. `AGENTS.md` and `agents/` are the live instruction surface; `skills/` and `tools/` are method and deterministic layers. Where a candidate or lower document conflicts with ratified governance, ratified governance controls and the conflict is surfaced.

---

## 1. Founding Intent

Chirality is a governed, filesystem-native agent operating system for deliverable-heavy professional work. It is maintained as a private canonical monorepo whose root is the **shared instruction surface** — a release-managed agent operating system (`AGENTS.md`, `agents/`, `skills/`, `tools/`, root `docs/`, `init/`) — that serves multiple project and domain **working-roots** nested under `projects/*` and `domains/*`. The same instruction surface is also packaged as a desktop harness that runs agents against a user-selected working folder.

The core insight: **if the filesystem is the database, architecture is a state-and-authority specification, not a service mesh.**

The system exists to:

- **Accelerate deliverable-heavy work** (EPC, design-build, software, domain-knowledge, proposals, and similar environments) by structuring agent workflows around production deliverables and decomposed knowledge.
- **Make agentic work auditable and controllable** so that outputs can be relied upon in professional, regulated, and high-stakes contexts.
- **Keep humans in charge** at every decision gate, while letting agents handle the mechanical work of drafting, extracting, reconciling, decomposing, and organizing.

---

## 2. Design Philosophy

The design philosophy rests on four foundational pillars. These are not a classification imposed after the fact — they are the structural logic the architecture follows, and they determine what the system is capable of, what it enforces, and what it makes visible.

### The Four Pillars

**Ontology — what exists in the system.**

The system's domain model is defined entirely through filesystem structures. Deliverable folders are nodes. Dependency rows in CSV registers are edges. Markdown files carry properties — identity, lifecycle state, context, references, working memory. The entity hierarchy (packages containing deliverables; categories containing knowledge types), stable identifiers (assigned once, persistent across renames), enumerated types, and the lifecycle state machine form the ontological layer.

This ontology is not a schema imposed on a database — it IS the filesystem. There is no separate representation. The folder structure is the project structure. The file contents are the project state. This means the ontology is directly inspectable by humans, agents, and tools alike, with no translation layer.

**Epistemology — what can be known, and how.**

This is the system's most distinctive and load-bearing contribution.

The fundamental problem of using LLMs in professional practice is not that they produce bad outputs — it is that bad outputs are indistinguishable from good ones by inspection. LLM outputs are plausible by construction. The system's response is not to make the model more reliable, which cannot be guaranteed. It is to make the epistemic status of every claim transparent and auditable, so that a qualified professional can determine what to rely on.

Four architectural mechanisms enforce this:

*Mandatory provenance.* Every non-trivial governed claim must cite its source file and section reference, or carry an explicit `location TBD` marker. A claim without provenance is structurally visible as ungrounded. Enforced by invariant K-PROV-1.

*No invention.* When required information is missing, agents label it `TBD` and surface the gap as an open issue. They do not guess, default-fill, or silently infer. Missing data is a finding, not a problem to solve. Enforced by invariant K-INVENT-1.

*Conflict surfacing.* When sources disagree, agents produce a Conflict Table with the competing claims, pointers to their sources, and a `HumanRuling = TBD` column. Agents never silently resolve contradictions — the human owns the ruling. Enforced by invariant K-CONFLICT-1.

*Epistemic labeling.* Every non-trivial claim is classified: FACT (directly observed in source text with citation), ASSUMPTION (reasonable inference grounded in cited material and requiring validation), PROPOSAL (suggestion requiring human decision), or TBD (unknown or unwarranted placeholder requiring resolution). The licensed professional does not need to guess whether a value is grounded or inferred — the label tells them.

Together, these mechanisms mean that gaps in evidence are findings, not hidden failures. The system does not try to prevent hallucination — it requires provenance, making unsupported claims structurally visible. This is what makes thorough review tractable in professional practice: the evidence trail is not a byproduct of the workflow, it is the workflow.

Two additional epistemic commitments complete the picture:

*Filesystem is the single source of truth.* If a decision, approval, or state change is not recorded in a versioned file, it does not exist for purposes of reliance. There is no hidden memory, no transient chat context, no external database that could diverge from the filesystem. What is on disk is what is true.

*Content-addressed approval.* Approvals bind to a specific git SHA. If the content changes after approval, the approval is void. This makes the integrity of the approval relationship mechanically verifiable — not dependent on trust or process discipline alone.

The formal epistemic ontology and warrant lifecycle are defined in `CHIRALITY_FRAMEWORK.md` §3.3 and `TYPES.md` §10. In summary: the epistemic layer operates on claims, warrants, statuses, gaps, conflicts, and rulings; a claim without warrant is a visible gap rather than a hidden omission; and claims progress through `UNWARRANTED → CITED → REVIEWED → AUTHENTICATED` as professionals assess and then bind themselves to specific content. The deliverable lifecycle tracks production state; the warrant lifecycle tracks the epistemic state of the claims within that work.

**Praxiology — how work is done.**

The operational model distinguishes external standards from three runtime positions: Agent 0 Supervising Architect, Agent 1 Manager, and Agent 2 Specialist. HELP_HUMAN is the sole Agent 0; a human may instead enter through any Agent 1. Agent 0 delegates only to Agent 1, Agent 1 delegates bounded work to Agent 2, and Agent 2 does not delegate. Capabilities are explicit rather than inherited: named children use their approved role policy, generalists are bounded by their parent and brief, and no child capability becomes available to its parent. Escalation flows upward, and no agent may bypass a human gate or approve professional reliance. Agent 2 may be TASK plus a skill and brief, an ephemeral bounded generalist, or an explicitly approved dedicated specialist.

Multi-agent workflows may use terminal fan-out/fan-in, supervised
parent-mediated many-to-many agency, or any dependency-valid mixture of
sequential and concurrent actions. The human may prescribe the graph or
delegate its selection. Agent 0 owns cross-package coordination; Agent 1 owns
coordination within its activated scope; durable artifacts and Git state
complement live agency.

Gate-controlled workflows ensure that humans make consequential decisions at defined junctions. Brief-driven pipelines make agent execution bounded, repeatable, and auditable — Type 2 agents receive structured inputs and return structured outputs with no mid-run human decisions required. Write quarantine contains failures within declared zones: every agent has an explicit write scope, tool roots are isolated from source truth, and no agent writes outside its declared zone.

The instruction root (release-managed agent operating system) is physically separated from the working root (user-controlled project state). This ensures that the rules governing agent behavior are stable across projects while execution remains fully filesystem-native. See §2.6.

**Axiology — what the system values.**

Public welfare is the first constraint. When tradeoffs exist between safety and commercial pressure, schedule, or convenience, safety prevails. This obligation is non-delegable to AI systems.

Professional responsibility is personal and non-transferable. A licensed professional retains decision rights for scope boundaries, governing codes and standards, hazard and risk acceptance, conflict adjudication, and approval for reliance. No AI system may claim to certify, approve, sign, seal, or issue engineering work for reliance. AI agent outputs are drafts and structured assistance — human acceptance is what makes them engineering work product.

Evidence is required, not plausibility. The hierarchy of authority in technical matters is: laws and regulations, codes and standards, project specifications, verified engineering analysis, professional judgment. Agent outputs carry no professional authority.

These values are not aspirational. They are enforced as architectural invariants (K-AUTH-1, K-AUTH-2, K-BIND-1) and as structural properties of the system (write quarantine, gate control, provenance requirements). A system that merely recommends these values would be a guideline. A system that enforces them architecturally is a governance framework.

### The Fractal Property

The selected PROJECT/SOFTWARE production contract mirrors the philosophical
structure of the system. In `SOW_V1`, the four practical lenses are sections
of one `ScopeOfWork.md`; transitional `LEGACY_FOUR_DOC` expresses the same
lenses across four files:

| Philosophical Pillar | Production-contract instantiation |
|---|---|
| Ontology — what is this thing? | **Datasheet** — key parameters, identification, structured metadata |
| Epistemology — what must be true? how do we verify? | **Specification** — technical requirements, acceptance criteria, scope definition |
| Axiology — why these choices? what principles govern? | **Guidance** — design rationale, best practices, contextual direction |
| Praxiology — how do we execute? | **Procedure** — step-by-step workflow, sequencing, checklists |

This is not a coincidence. The production contract reflects the philosophical
architecture because both emerge from the same responsibility question. The
file layout may transition; the four practical questions remain stable.

The system practices what it produces. Its governance documents follow the
same structure that it imposes through the production contract. This fractal
property is a sign of architectural coherence.

### How the Pillars Relate

The ontology, praxiology, and axiology exist to serve the epistemology.

The ontology gives the epistemic architecture something to operate on — without stable entities, identifiers, and state in files, there is nothing to attach provenance to.

The praxiology enforces the epistemic architecture through gates and write quarantine — without bounded execution and human gates, the epistemic controls would be suggestions rather than guarantees.

The axiology anchors the epistemic architecture in professional responsibility — without the value commitment that evidence matters more than plausibility, the epistemic mechanisms would be overhead rather than protection.

The epistemology is what makes Chirality a professional engineering tool rather than a productivity tool. Productivity tools optimize for output quality. Professional engineering tools optimize for knowing what you can rely on.

### The Pillars as the Ontology of Professional Accountability

The four pillars are not merely a classification scheme chosen for this project. In Chirality, they function as a compact and coherent framework for professional accountability. At every level where accountability must be made inspectable in this architecture, the same four questions must be answered:

- What exists? (ontology)
- What is warranted? (epistemology)
- How was the work done? (praxiology)
- What values governed the decisions? (axiology)

Missing any one creates a specific, identifiable accountability failure: without ontology, the professional does not know what they are responsible for; without epistemology, they do not know what to believe; without praxiology, they do not know how the work was performed; without axiology, they do not know why the decisions were made the way they were.

This is why the fractal property appears in Chirality. The four pillars recur at the governance level, at the agent instruction level, and at the document kit level because this architecture must answer the same four accountability questions at each level of abstraction.

### The Seven Principles

The principles that follow instantiate this framework. Each principle belongs to one or more pillars:

| Principle | Primary Pillar |
|---|---|
| §2.1 Filesystem Is the Database | Ontology |
| §2.2 Git Is the Event Store | Epistemology |
| §2.3 Human Authority at Every Gate | Praxiology, Axiology |
| §2.4 Evidence Over Plausibility | Epistemology, Axiology |
| §2.5 No Hidden Memory | Epistemology |
| §2.6 Separation of Instruction and Execution | Praxiology |
| §2.7 Governed State and Multi-Phase Closure | Praxiology, Epistemology |

---

### 2.1 Filesystem Is the Database

Authoritative project state lives entirely in git-tracked files. There is no separate database holding authoritative state, no server state, no configuration files that diverge from the filesystem — nothing outside git-tracked files serves as a source of authoritative project truth. Rebuildable, gitignored local projections (regenerated from the files by one command, never cited as authority) are permitted per D-GOV-01 (`docs/governance_harness/_DECISIONS/D-GOV-01_substrate_authority.md`, ruled 2026-07-01); engine-owned domain stores are governed by the K-DOMAIN family (`CONTRACT.md` §1.12).

- **Nodes:** Deliverable folders, package folders.
- **Edges:** Rows in `Dependencies.csv`, ANCHOR rows connecting tree to graph.
- **Properties:** Markdown files (`_STATUS.md`, `_CONTEXT.md`, `Datasheet.md`, etc.).

Agents traverse this implicit graph on-demand. Analysis artifacts are materialized as markdown/CSV and git-committed for auditability.

This is the load-bearing architectural decision. Every capability the system provides — V-model traceability, immutable snapshots, change propagation tracking, content-addressed approval, and the complete audit trail — depends on state being in git-tracked files. If state moved to a database, every one of these capabilities would need to be rebuilt. The filesystem choice is not a simplification — it is the mechanism that makes the systems engineering apparatus work.

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
- Claims calibrated to their warrant, scope, and jurisdiction. Where evidence supports only an interpretation, local implementation, or hypothesis, the claim must be framed that way.

### 2.5 No Hidden Memory

If it is not in a versioned file, it does not exist. Agents must not maintain a hidden database or private state that diverges from the filesystem.

Clarification:

- This constraint applies to **authoritative project execution state** (deliverables, dependencies, approvals, issued artifacts, and gate-relevant records).
- Non-authoritative operator convenience state (for example UI panel state, local turn-option presets, and other ephemeral runtime preferences) MAY be stored outside project files.
- Such convenience state MUST NOT be treated as project truth and MUST NOT override contract/governance enforcement.

### 2.6 Separation of Instruction and Execution

The system separates the **instruction root** (the release-managed agent operating system) from the **working root** (the project state agents read and write):

- **Instruction root:** the shared, release-managed surface — `AGENTS.md`, `agents/`, `skills/`, `tools/`, root `docs/`, and `init/`. In this monorepo it is the repository root; in deployable desktop builds it is the app bundle, where `agents/`, `skills/`, `tools/`, `docs/`, and `init/` are packaged as `instruction-root/`.
- **Working root:** the filesystem location where agents execute and create or update governed state. One instruction root serves **many** working roots — each `projects/<name>/` and `domains/<name>/` in this monorepo, or a user-selected folder under the desktop harness.

This preserves a single stable agent operating system across many projects and domains while keeping execution fully filesystem-native in user-controlled state. A working root MUST NOT be located inside the instruction root.

DIRECTIVE establishes the separation as a value; `SPEC.md` (Root Model and Path Anchoring) binds the paths — including the rule that a task's write scope must resolve within the active checkout, which is what makes per-working-root isolation (including git worktrees) safe.

### 2.7 Governed State and Multi-Phase Closure

Work that spans phases or hands off between agents is governed by integration rules defined in `AGENTS.md`:

- **Derivative packages** must cite their accepted upstream snapshot(s) and must never substitute for authoritative truth.
- Every **phase-boundary decision** that changes or validates governed state terminates in an immutable **snapshot**; later phases consume accepted snapshots, not mutable working state.
- Any workflow that stops with work intended for a later phase emits an explicit **handoff state** (accepted snapshots, derivative-package status, closure verdict, rerun requirements, remaining blockers).
- **Closure** requires accepted truth, regenerated or explicitly deferred derivatives, recorded audit status, and surfaced unresolved blockers — not merely that files were written.
- Dependency **cycles** are resolved by a recorded move (decompose / invert / merge / cut; cut and merge are human-gated), never silently linearized.

These rules make multi-agent, multi-phase work auditable end to end. See `AGENTS.md` (Governance Integration Rules) and `CONTRACT.md`.

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

- Project decomposition (`PROJECT_DECOMP`) — from messy scope of work to structured packages and deliverables.
- Software decomposition (`SOFTWARE_DECOMP`) — software work with context envelopes.
- Domain / knowledge decomposition (`DOMAIN_DECOMP`) — handbooks and knowledge domains into categories, knowledge types, and atomic units.
- Workspace scaffolding (folder creation, metadata file initialization).
- Document kit drafting (Datasheet, Specification, Guidance, Procedure).
- Dependency extraction and tracking; cross-deliverable reconciliation.
- Semantic analysis (lensing and enrichment).
- Source extraction, cataloging, and retrieval (PDF, drawing, and equation pipelines; source catalogs; retrieval indexes).
- Cost estimation (parameterized by basis of estimate) and schedule generation (parameterized by scheduling basis).
- Publication assembly (DBM publishing) from accepted decomposition state.
- Aggregation, audit, and evaluation.
- Change management support and git-based version control hygiene.

### 4.2 Out of Scope

- Automated approval or issuance of deliverables.
- Financial transactions or binding commitments.
- Safety-critical decisions without human review.
- Replacing professional judgment in regulated practice.
- External system integration (databases, APIs, cloud services) as a source of authoritative project truth.

---

## 5. Structural Constraints

These constraints are hard to change later. They define the boundaries of the system's architecture.

| Constraint | Rationale |
|---|---|
| No external database dependency | Filesystem is the single source of authoritative truth; rebuildable gitignored projections permitted, never authoritative — per D-GOV-01 (`docs/governance_harness/_DECISIONS/D-GOV-01_substrate_authority.md`); eliminates sync burden |
| No external server requirement | Desktop-first and offline-capable; the opt-in per-user Chirality runtime daemon is a local process over a Unix-domain socket, not remote infrastructure or a source of authoritative project truth |
| All state as plain files | Human-readable, git-trackable, tool-agnostic |
| Git-trackable artifacts only | Auditability, reproducibility, rollback, diff-based review |
| Flat package hierarchy | No nesting; simplifies automation, coverage checking, and scope assignment |
| Deliverable-local dependency registers | No central dependency graph to maintain; aggregation is on-demand |
| Immutable snapshots for task agent outputs | Reruns are safe; historical outputs are preserved |
| Instruction root separate from working root | Agent instructions are release-managed; project data is user-controlled |
| One shared instruction root serves many working roots | A single release-managed agent OS governs many projects and domains without per-workspace instruction drift |
| Task write scope resolves within the active checkout | Enables per-working-root and git-worktree isolation; prevents cross-workspace writes (see `SPEC.md` Root Model and Path Anchoring) |

---

## 6. Responsible Use

This framework is designed to support professional responsibility, not replace it.

- Treat agent outputs as drafts and structured assistance.
- Keep human review and sign-off as the decision gate for safety, compliance, and contractual commitments.
- Do not rely on agent outputs without independent verification appropriate to the stakes.

---

## 7. Shared Runtime Direction

Under D-GOV-20, Chirality’s executable agent harness is a root-owned
`runtime/` workspace. One opt-in per-user daemon owns engines, credentials,
sessions, delegation, tools, interruption, turn admission, and local-model
residency. Desktop, CLI, and registered project surfaces are clients of that
single owner.

The daemon’s user-data files are operational state, not project authority.
Governed truth remains in checkout-contained manifests, instructions,
decisions, execution trees, AgentRuns, evidence, and Git. Agent 0/1/2 roles
remain authority contracts independent of engines and models; actual runtime
attribution is recorded without creating durable model-to-role doctrine.

Local control is authenticated HTTP/1.1 over a protected Unix-domain socket
only. The initial local pilot permits one explicitly resident authenticated
loopback oMLX model and one bounded read-only Pi Agent 2 child under a real
Agent 1. It does not authorize automatic fallback or switching, multiple
primary local models, remote oMLX, local Agent 1, production domain mutation,
release, publication, issuance, or professional reliance.
