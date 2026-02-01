# Chirality App

A multi-agent framework for EPC (Engineering, Procurement, Construction) and design-build projects.

Chirality App provides a structured, deliverable-centric approach to producing engineering and project documentation using coordinated AI agents. Work is organized around **deliverables** that progress through a defined lifecycle, with clear boundaries between local (single-deliverable) and cross-project operations.

## Core Concepts

### Project Decomposition
Every project starts with a **decomposition document** produced by PROJECT_DECOMP through a gate-controlled conversation. The decomposition includes:

- **Structured Scope of Work (SSOW)** — Normalized, atomic scope items with stable IDs
- **Scope Ledger** — Machine-checkable table mapping every scope item to exactly one Package and (best-effort) to Deliverables
- **Packages** — Flat partitions of scope (no nesting; no overlaps; no gaps)
- **Deliverables** — Units of production within each Package, with types, responsibilities, and anticipated Artifacts
- **Objectives** — Success criteria derived from scope, mapped to supporting Deliverables
- **Vocabulary Map** — Canonical terms and synonyms to prevent semantic drift
- **Coverage & Telemetry** — Metrics summary (counts, gaps, open issues) that makes decomposition quality measurable across revisions

The decomposition is the source of truth that initializes all downstream agent workflows. Its stable IDs enable longitudinal tracking and cross-deliverable reconciliation.

### Filesystem as State
Project truth lives on disk. Agents read and write files directly—there is no hidden database or divergent state. The folder structure itself encodes project status.

### Deliverable Lifecycle
Each deliverable progresses through local lifecycle states:

```
OPEN → INITIALIZED → SEMANTIC_READY → IN_PROGRESS → CHECKING → ISSUED
```

- `OPEN`: Folder exists, no content yet
- `INITIALIZED`: Draft documents generated
- `SEMANTIC_READY`: Semantic lens (`_SEMANTIC.md`) generated (optional step)
- `IN_PROGRESS`: Active human + agent work
- `CHECKING`: Under review
- `ISSUED`: Released

Stage gates (30/60/90/IFC) are human-managed milestones, separate from lifecycle states.

### Coordination Modes
The framework separates how teams coordinate from how dependencies are tracked:

| Coordination Representation | Description |
|---|---|
| Schedule-first | Gantt/stage gates drive sequencing |
| Declared deps | Explicit interface-critical edges only |
| Full graph | Complete dependency DAG |

| Dependency Tracking Mode | Behavior |
|---|---|
| `NOT_TRACKED` | No blocker analysis |
| `DECLARED` | Advisory blockers from declared edges |
| `FULL_GRAPH` | Full DAG analysis |

Most EPC projects work best with **Schedule-first** + **NOT_TRACKED** or **DECLARED**.

## Agents

Agents are described in `AGENTS.md`.

Agent instruction files are located in `agents/`.

## Deliverable Folder Structure

Each deliverable folder contains:

```
{PKG-ID}_{PkgLabel}/
└── 1_Working/
    └── {DEL-ID}_{DelLabel}/
        ├── _CONTEXT.md        # Identity + decomposition pointer
        ├── _DEPENDENCIES.md   # Dependency mode + declared edges
        ├── _STATUS.md         # Lifecycle state + history
        ├── _REFERENCES.md     # Source document pointers
        ├── _SEMANTIC.md       # Semantic lens (optional)
        ├── Datasheet.md       # Key parameters and data
        ├── Specification.md   # Technical requirements
        ├── Guidance.md        # Design guidance and rationale
        └── Procedure.md       # Execution procedures
```

Project-level outputs live in separate tool roots:
- `execution/_Aggregation/` — Aggregation snapshots
- `execution/_Estimates/` — Cost estimate snapshots
- `execution/_Reconciliation/` — Reconciliation reports

## Regulated, High-Stakes, and Professional-Responsibility Environments

Many EPC and design-build programs run in environments where deliverables are:

- **Safety-significant** (people, environment, critical infrastructure)
- **Contractually binding** (scope, acceptance, claims, and payment milestones often depend on document content)
- **Subject to codes/standards, regulator expectations, and internal QA** (document control, traceability, configuration management)
- Produced under **high professional responsibility** (engineering duty of care; formal review and sign-off)

In these settings, “agentic workflows” are only valuable if they are **auditable, controllable, and review-friendly**. Chirality’s approach is intentionally conservative: agents accelerate production, but the project truth remains explicit in files, and humans remain the accountable validators.

### What `WHAT-IS-AN-AGENT.md` means in high-stakes workflows

`WHAT-IS-AN-AGENT.md` frames a “great agent” as a **composed system** with clear layers:

- **Agent 0 / Type 0 (Architect):** defines and maintains the standards, contracts, and role boundaries
- **Agent 1 / Type 1 (Manager):** interprets intent, decomposes work, writes briefs, routes to Specialists, and merges results
- **Agent 2 / Type 2 (Specialist):** executes a narrow brief with minimal context and returns outputs + evidence

In regulated work, this layered design is prudent because it:

- Creates **separation of concerns** (policy/standards vs orchestration vs execution), making failures easier to localize and fix
- Enables **stateless, brief-driven Specialists**, reducing hidden context, reducing drift, and improving repeatability
- Supports **deterministic debugging** (“is this a standards problem, a routing problem, or an execution problem?”)
- Encourages **fan-out/fan-in** when appropriate, making reviews faster (specialists produce bounded artifacts that can be checked independently)

### What `AGENT_HELPS_HUMANS.md` means in high-stakes workflows

`AGENT_HELPS_HUMANS.md` is the workflow-design standard for writing agent instruction sets and pipelines. In high-stakes environments, it functions like a lightweight **quality system for agent behavior**, emphasizing:

- **Explicit contracts** (clear inputs, outputs, acceptance criteria)
- **Write scope discipline** (what an agent is allowed to modify, and when)
- **Provenance and evidence expectations** (what must be cited, what must be marked as TBD/assumption)
- **QA gates** (checking steps that prevent silent failure or silent “fixes”)
- **Snapshot-oriented outputs** (so review is anchored to stable artifacts, not transient chat context)

This is prudent because most real-world failures in regulated documentation are *not* “lack of content,” but:
- ambiguous scope,
- untraceable rationale,
- uncontrolled revisions,
- inconsistent terminology across disciplines,
- and weak handoffs between contributors.

### How this framework supports common regulated-controls expectations

Without claiming “automatic compliance,” the architecture supports the kinds of controls auditors and QA programs typically expect:

- **Traceability:** decomposition IDs, scope ledgers, references files, and deliverable-local context make “why is this requirement here?” answerable.
- **Document control:** “filesystem as state” and lifecycle gating align naturally with controlled document progression (draft → check → issue).
- **Configuration management:** snapshots and explicit change review reduce accidental drift and make diffs meaningful.
- **Verification & validation:** QA gates, conflict surfacing, and explicit uncertainty labeling create a reviewable V&V posture.
- **Segregation of duties:** Manager vs Specialist vs Human validator boundaries reduce the risk of one “all-powerful agent” making uncontrolled changes.
- **Information security & confidentiality:** least-privilege data handling and constrained write scopes reduce accidental exposure and unintended edits.

### Practical benefits for engineering + project management

When implemented with discipline, the combined effect is:

- **Faster production with fewer review cycles** (because outputs are structured for checking, not just generation)
- **Lower rework risk** via scope coverage telemetry and explicit gap surfacing
- **Improved interface management** (terminology discipline + reconciliation checkpoints reduce cross-deliverable contradictions)
- **Better change defensibility** (clear diffs, clear assumptions, clear provenance)
- **More reliable handover** (deliverables are self-describing via `_CONTEXT.md`, `_STATUS.md`, `_REFERENCES.md`)
- **Stronger audit readiness** (evidence, history, and decision points are preserved as artifacts)

### Responsible-use note (important)

This framework is designed to support professional responsibility, not replace it.

- Treat agent outputs as **drafts and structured assistance**, not authoritative engineering judgment.
- Keep **human review and sign-off** as the decision gate for safety, compliance, and contractual commitments.
- Align the workflow with your organization’s **QMS / document control / retention** requirements.

## Scaling 
This framework is intentionally designed to make scaling plausible because it treats:

- **The filesystem as the system state** (not chat memory)
- **Standard artifacts as the interface** between people and agents (the 4 Documents, lifecycle states, and optional `_SEMANTIC.md`)
- **Agent composition (0/1/2 layering)** as the control surface for separation of duties and debuggability

Below are the most evidently probable patterns (i.e., what teams commonly converge toward when a file-centric, contract-driven workflow is adopted).

### Pattern 1: Standardization reduces dependence on individual craft

The fastest path to team-scale reliability is usually to standardize:

- **Folder and artifact conventions** (so any contributor can locate “what matters” quickly)
- **The “4 Documents” baseline** (so every deliverable starts from a known structure)
- **Lifecycle transitions** (so “what stage are we in?” is unambiguous)
- **Brief + acceptance criteria format** (so Specialists can be swapped without losing intent)

As these conventions settle, the work shifts from “inventing how to proceed” to “executing a known playbook,” which is what scales across people.

### Pattern 2: Deliverable folders become “bootable experts” when filesystem state is treated as agent state

When a deliverable type has a well-established structure (and your team consistently maintains that structure), the folder stops being “a place where files live” and becomes a **portable expert context**.

In practice, a properly-scoped agent can behave *like an expert in that deliverable* because it can reliably load:

- the deliverable’s `_CONTEXT.md` (purpose, scope boundaries, interfaces, constraints),
- `_REFERENCES.md` (standards, upstream requirements, source documents),
- `_STATUS.md` (lifecycle state, open decisions, readiness),
- `_SEMANTIC.md` (if present: the project’s preferred framing, concepts, and “what questions matter here”),
- plus the “4 Documents” and any WORKING_ITEMS history.

That bundle acts like an “expert boot image”: it provides the *situated* project knowledge that usually lives in a senior person’s head (what matters, what’s in-bounds, what must be cited, what’s decided vs unresolved), while the model supplies general reasoning and drafting ability.

**Most probable outcomes when this is done well:**
- Specialists become **interchangeable** across people and sessions (less dependence on a single operator’s memory).
- New team members can “boot into” competent contribution faster (onboarding becomes reading + executing, not oral tradition).
- Outputs become more consistent across deliverables because the same state primitives and templates are always present.

### Pattern 3: “Context compounds” — the folder gets smarter as work progresses

Once the filesystem is the state, every iteration can add durable signal:

- resolved assumptions and decisions move from chat into `_CONTEXT.md` / the 4 Docs,
- citations and standards harden in `_REFERENCES.md`,
- recurring edge cases and definitions stabilize in `_SEMANTIC.md`,
- and lifecycle status makes readiness explicit.

Over time, this tends to shift work from “inventing how to do this deliverable” to “executing a known playbook,” and the playbook keeps improving. The practical effect is **fewer clarification loops** and **higher-quality first drafts**, because each new run inherits a richer, more accurate local context.

### Pattern 4: Cross-deliverable coherence becomes a scheduled activity

As more deliverables reach mature states, cross-scope agents become more reliable — but only if you treat coherence checks as **events**, not constant background noise. Common practice is to run reconciliation at:
- package freeze points,
- design review milestones,
- and pre-issuance checks.

### What you can realistically expect to improve over time

If the above patterns hold, the most realistic improvements are:

- **Lower onboarding time** for new contributors (because the state is in the folder, not in someone’s head)
- **More parallelism** (multiple deliverables worked concurrently without colliding)
- **Fewer review iterations** (because drafts are structured for checking and have explicit evidence/assumptions)
- **Higher consistency** across deliverables (terminology and intent converge through repeated use of the same structures)

### What can prevent scaling (and how this framework mitigates it)

Common scale blockers:
- **Uncontrolled instruction drift** (different operators “teach” different behaviors)
- **Skipping lifecycle states** (folders stop being trustworthy as a source of truth)
- **Over-broad write scopes** (agents change too much, too quickly, too quietly)
- **Implicit assumptions** (not captured in `_CONTEXT.md` / `_STATUS.md` / `_REFERENCES.md`)

Mitigations built into this approach:
- canonical standards (Agent 0),
- orchestration and gating (Agent 1),
- narrow execution (Agent 2),
- and auditability via stable artifacts.

## Documentation

- `AGENTS.md` — Operator-facing guide to agents and prompt templates
- `agents/AGENT_*.md` — Individual agent instruction files
- `WHAT-IS-AN-AGENT.md` — Architecture philosophy (layering, composition, debugging)
- `AGENT_HELPS_HUMANS.md` — Canonical workflow-design standard for agent instruction sets and pipelines
- `AUDIT_AGENT.md` — Audit rubric for coherence/conformance across AGENT_* files
- `INIT-PERSONA.md` — Manager-style session INIT (interpretation, orchestration, multi-step work)
- `INIT-TASK.md` — Specialist-style task INIT (brief-driven execution)
- `INIT-CUSTOM.md` — Template for bespoke INITs while remaining framework-consistent
