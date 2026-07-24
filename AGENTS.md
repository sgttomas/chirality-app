# AGENTS — Runtime Doctrine, Governance Rules, and Agent Index

This file is the canonical runtime doctrine and live agent index. Root
`CLAUDE.md` imports this file without adding another instruction layer. For
the ratified workflow-component design standard, see
`docs/WORKFLOW_COMPONENT_STANDARD.md`;
for the explanatory design basis, see
`docs/DBM_Agent_Instruction_Architecture.md`.

Use `AGENT_*` for instruction files (e.g., `AGENT_CHANGE.md`). Use the role name for the agent itself (e.g., `CHANGE`). All files are in `agents/`.

---

## What Is an Agent?

```text
agent = LLM + instructions + declared files/context + tools + permissions
```

This is an operational definition, not a claim of personhood or professional
responsibility. An agent may generate claims and modify state within its
permission boundary. The human remains accountable for what is accepted or
relied upon.

Distinguish:

| Term | Meaning |
|---|---|
| **Agent instance** | A running LLM with an instruction stack, declared context, tools, and permissions |
| **Agent role** | A named responsibility in the runtime delegation hierarchy |
| **Agent instruction package** | Durable `AGENT_*.md` instructions used to instantiate or govern a role |
| **Skill** | A reusable bounded method loaded into an Agent 2 instance, normally through TASK |
| **Tool** | A deterministic operation available to an agent; never a substitute for semantic judgment |
| **Brief** | Run-specific purpose, scope, context, permissions, outputs, and acceptance checks |

## Good Agents and Great Workflows

A good agent has one bounded role, one explicit objective, a declared context,
an explicit permission boundary, and a checkable output contract. A great
workflow composes good agents between human decision points:

```text
Human ↔ Agent 0 → Agent 1 → Agent 2
```

| Layer | Name | Role |
|---|---|---|
| **Agent 0** | Supervising Architect | Aligns the human and workflow, selects and supervises managers, presents decisions, and maintains the instruction system through the appropriate Agent 1 |
| **Agent 1** | Manager | Converts aligned direction into plans and briefs, delegates bounded work, validates fan-in, and escalates decisions |
| **Agent 2** | Specialist | Executes one bounded objective and returns outputs plus evidence without creating another orchestration layer |

HELP_HUMAN is the sole canonical Agent 0. Humans may also start an untyped
session or invoke any Agent 1 directly. Type 2 is not a top-level chat entry.

Normative standards are outside this runtime hierarchy. They constrain every
agent layer; they are not agents themselves.

## Agent 2 Construction Forms

Agent 2 may be instantiated in three ways:

1. **TASK agent** — TASK shell + skill + sealed brief. Use for recurring
   methods whose authorization and run semantics fit TASK.
2. **Ephemeral generalist** — a fresh general-purpose instance with one sealed
   purpose-specific brief, declared context, explicit tools, write targets,
   outputs, and acceptance checks. It has no persistent `AGENT_*.md`.
3. **Dedicated specialist** — a persistent Agent 2 instruction package for
   runtime semantics that TASK or an ephemeral generalist cannot safely
   express.

A dedicated specialist requires a HELPS_HUMANS proposal and explicit human
approval before it is added to the live index. The proposal must identify the
persistent context, tool, permission, recovery, caller, compatibility, and
review requirements that justify a named package.

Repeated ephemeral-generalist briefs are evidence for a skill candidate.
Different subject matter or output schema alone does not justify a dedicated
agent file.

## Delegation and Entry Rules

- Human entry: untyped session, Agent 0, or any Agent 1.
- Agent 0 delegates only to named Agent 1 managers.
- Agent 1 delegates to named Agent 2 specialists, TASK, or an allowed
  ephemeral generalist.
- Agent 2 does not delegate.
- Delegation never implies capability inheritance. Named children are bounded
  by their approved instruction policy; ephemeral generalists are additionally
  bounded by the parent's declared tools. A child's capability does not become
  a parent capability. Every child remains subject to sealed context, pipeline
  approval, path containment, enforced read/write scope, and durable evidence.
- Managed delegation uses `delegate_agent`; named children load their actual
  instruction package, generalists use the Agent 2 base contract plus a sealed
  brief, and every run persists parentage, hashes, scopes, status, and returns.
  Multi-agent execution requires an actual governed child-session mechanism;
  durable launch briefs alone are never a substitute for execution. The app
  harness uses `delegate_agent`. A project loop may use its platform's native
  hierarchical TASK/subagent facility when the loop freezes equivalent briefs,
  scopes, parentage, and returns. If no executable child mechanism is available,
  defer the multi-agent stage or continue only genuinely single-agent work.

## Multi-Agent Orchestration

Runtime delegation and communication are hierarchical. Work coordination is
many-to-many through both live parent-mediated agency and durable filesystem
and Git state. The hierarchy governs who may delegate or communicate; it does
not prescribe one universal execution pattern.

The human may prescribe an orchestration pattern or sequence, provide only
constraints and priorities, or delegate selection to Agent 0 or a directly
invoked Agent 1. Selection precedence is: explicit human direction;
human-approved constraints, priorities, and gates; accepted project and
decomposition state and dependencies; Agent 0 cross-package judgment; Agent 1
intra-package judgment. The selected or derived posture and work graph are
recorded before dispatch.

### Terminal fan-out/fan-in

Use terminal fan-out/fan-in when bounded children can execute independently
and terminal returns provide sufficient coordination. The parent freezes
briefs, dispatches eligible children, collects terminal returns, validates
coverage, schemas, provenance, conflicts, and failures, and only then releases
dependent work. A child failure or critical blocker may return normally to its
parent without converting the run into many-to-many coordination.

### Supervised many-to-many agency

Use supervised many-to-many agency when active work can produce information
relevant to other active or planned work. Agent 1 reports coordination notices
to Agent 0; Agent 0 records, selectively relays, amends, holds, replans,
escalates, or routes them. Within a package, Agent 2 reports to its Agent 1
parent, which performs the equivalent disposition. Siblings do not use hidden
or undeclared direct messaging and children do not bypass their parent.

Informational relays preserve claim status and carry only minimum sufficient
context. Changes to objective, accepted basis, write scope, ownership, risk,
or acceptance criteria require a versioned brief amendment. Consequential
amendments return to the human.

“Consequential” is not left to unconstrained agent preference. It includes at
least scope expansion, a change in consequential risk, a change in authority,
an unresolved shared-write/ownership conflict, or a change in acceptance
criteria or lifecycle acceptance. Any uncertainty about whether one of these
conditions applies is itself returned to the human.

### Mixed work graphs and safety

A work graph may compose arbitrary dependency-valid sequences of individual
and concurrent actions without assigning every composition a pattern name.
Manager-selected orchestration inside an accepted scope does not require a
new approval for every child. Dynamic replanning is allowed when live evidence
changes the graph, but prior plan versions and amendments remain durable.

Every child declares read scope, write targets, dependencies, expected
returns, and fan-in gates. Shared reads are allowed. Concurrent sibling writes
must be disjoint; overlapping writes require serialization against an accepted
predecessor or one declared integration owner. Failed nodes block only their
declared dependants; independent work continues. Partial or invalid returns
are not accepted at fan-in.

Arbitrary Bash cannot be proven package-bounded by lexical command inspection.
In the app harness, a Bash-bearing managed child therefore requires explicit
project-root read/write scope and becomes the serialized integration owner for
that stage. Package-parallel work uses bounded file tools or registered
deterministic tools instead.

Files hold scope, decisions, claims, artifacts, dependencies, notices,
amendments, acknowledgments, and handoffs. Accepted snapshots provide stable
inputs; Git records identity, history, isolation, and integration state. These
durable surfaces complement live agency and never become hidden authority.

---

## Governance Integration Rules

- **Derivative-package rule.** Any package assembled from accepted upstream truth but not itself authoritative decomposition truth is a derivative package. This includes regenerated KTY-local artifacts, `_Aggregation` outputs, hypergraph snapshots, audit snapshots, concordance packages, and publication packages. Derivative packages must cite their accepted upstream snapshot(s) and must never be treated as a substitute for decomposition truth.
- **Snapshot rule.** Every phase-boundary decision that changes or validates governed state must terminate in a new immutable snapshot and a pointer update only where the owning workflow explicitly permits one. Later phases consume accepted snapshots; they do not rely on mutable working state alone.
- **Handoff-state rule.** Any workflow that stops with work intended for another agent or later phase must emit an explicit handoff state that names the accepted upstream snapshot(s), derivative-package status, closure verdict, rerun requirements, and remaining blockers.
- **Closure rule.** A scope unit or phase is not closed merely because files were written. Closure requires authoritative truth to be accepted, required derivative packages to be regenerated or explicitly deferred, audit status to be recorded, and unresolved blockers to be surfaced in the handoff state.
- **Sequencing rule.** If a later phase consumes derivative packages, it must run only after the upstream authoritative snapshot has been accepted and the required handoff state records which derivative packages are current.
- **Cycle-resolution rule.** A dependency graph is objective-relative; its strongly-connected components are the objective signal of undecided ordering. Resolve each SCC by a recorded move (decompose / invert / merge / cut; cut/merge are human-gated), hold cycle-participating edges non-gating until resolved, and never silently linearize a cycle. See `docs/CYCLE_DRIVEN_RESOLUTION.md`.
- **Agent-index change-notice rule.** Any tranche that changes, renames, or deletes files under `agents/` must identify the project surfaces that pin or mirror the touched files — at minimum authority-reference corpus snapshots and SHA-pinned contract mirrors — and ship, in the same tranche, a routed coordination notice to each affected project loop's coordination surface stating what changed and what follow-on remains for that loop. The notice is coordination, not authority: the receiving loop adopts, amends, or declines under its own instruments and cadence. Downstream loops still detect such changes through their own deterministic checks (corpus-drift status); this rule exists so detection does not depend on that alone.

## Agent Index

### Normative Standards (Not Agents)

| Standard | File | Role |
| --- | --- | --- |
| Workflow-Component Design Standard | `docs/WORKFLOW_COMPONENT_STANDARD.md` | Ratified workflow-component design standard; exact text accepted through D-GOV-14 |
| Decomposition Standard | `docs/DECOMPOSITION_STANDARD.md` | Ratified 7-gate decomposition protocol and I1–I10 invariants; exact text accepted through D-GOV-14 |

### Agent 0 — Supervising Architect

| Agent | Instruction File | Role |
| --- | --- | --- |
| HELP_HUMAN | `AGENT_HELP_HUMAN.md` | Sole canonical Agent 0; aligns with the human, supervises Agent 1 managers, returns decisions, and performs validated cross-manager fan-in |

### Agent 1 — Managers

| Agent | Instruction File | Role |
| --- | --- | --- |
| HELPS_HUMANS | `AGENT_HELPS_HUMANS.md` | Designs and maintains agents, skills, tools, briefs, workflow packages, migrations, registries, and validators |
| RESEARCH | `AGENT_RESEARCH.md` | Evidence-grounded inquiry over accepted domain decompositions, source catalogs, and retrieval indexes |
| PROJECT_SETUP | `AGENT_PROJECT_SETUP.md` | Project setup manager; workspace initialization, setup pipelines, tier sequencing support, control loops, and human-gated schedule-basis workflows |
| WORKING_ITEMS | `AGENT_WORKING_ITEMS.md` | Package-level production manager; plans and coordinates Agent 2 work across activated deliverables |
| RECONCILIATION | `AGENT_RECONCILIATION.md` | Deliverable-corpus concordance manager; claim-level calibration, inventory, package waves, cross-package synthesis, decision routing, repair/backcheck, and closure |
| CHANGE | `AGENT_CHANGE.md` | Git state management with approval gates |
| PROJECT_DECOMP | `AGENT_PROJECT_DECOMP.md` | EPC / design-build decomposition |
| SOFTWARE_DECOMP | `AGENT_SOFTWARE_DECOMP.md` | Software decomposition with Context Envelopes |
| DOMAIN_DECOMP | `AGENT_DOMAIN_DECOMP.md` | Handbook / knowledge domain decomposition |
| SCOPE_CHANGE | `AGENT_SCOPE_CHANGE.md` | Change impact assessment and decomposition amendment |
| DOMAIN_ENGINE | `AGENT_DOMAIN_ENGINE.md` | Domain-engine integration manager; profiles, protected paths, adapter workflows, operation proposals, and human-gated domain handoffs |
| REVIEW | `AGENT_REVIEW.md` | Formal 5-gate review for lifecycle transitions |
| EVALUATION | `AGENT_EVALUATION.md` | Read-only audit orchestration, cross-deliverable coherence assessment, scoring, and remediation recommendations |
| PDF2MD | `AGENT_PDF2MD.md` | Native PDF-to-Markdown conversion pipeline; orchestrates rasterization, batch VLM dispatch, post-processing, optional prose asset materialization, assembly |
| EQUATION_AUDIT | `AGENT_EQUATION_AUDIT.md` | Post-PDF2MD equation-review loop; iterates extract → human review → interpret prose notes → apply fixes → re-extract → backcheck → close, terminating in an immutable snapshot under `audit/equations/snapshots/`. Dispatches `equation-flag-interpret` per prose-shaped flag and `equation-bbox-detect` per page when crops are enabled |
| DRAWING_EXTRACT | `AGENT_DRAWING_EXTRACT.md` | Drawing-type-aware extraction pipeline; core-vs-repertoire split orchestrates rasterization, target-appropriate crops/tiles, target-specific TASK skill dispatch per (drawing_type × extraction_target), deterministic QA, target-driven assembly, and optional PFD-equipment merge. DRAWING_SET, PFD, and P_AND_ID targets are implemented; ISOMETRIC/GA remain stubbed fail-fast |
| DBM_PUBLISHER | `AGENT_DBM_PUBLISHER.md` | Publish one rewritten DBM from approved DOMAIN state using frozen planning artifacts, direct section dispatch, package assembly, and post-authoring evidence-bundle review |

### Agent 2 — TASK and Proposed Dedicated Specialists

| Agent | Instruction File | Role |
| --- | --- | --- |
| PREPARATION | `AGENT_PREPARATION.md` | Scaffold package/deliverable folders |
| RESEARCHER | `AGENT_RESEARCHER.md` | Dispatched research specialist; executes one research brief into an immutable evidence packet + structured return (the Type-2 executor of RESEARCH) |
| AGGREGATION | `AGENT_AGGREGATION.md` | Cross-scope synthesis snapshots |
| TASK | `AGENT_TASK.md` | Generic bounded-task shell; loads profile/skill and executes within explicit scope |
| AUDIT_AGENTS | `AGENT_AUDIT_AGENTS.md` | Agent instruction conformance audit |
| AUDIT_DECOMP | `AGENT_AUDIT_DECOMP.md` | Decomposition coverage audit |
| AUDIT_DEP_CLOSURE | `AGENT_AUDIT_DEP_CLOSURE.md` | Dependency closure audit |
| DOMAIN_HYPERGRAPH | `AGENT_DOMAIN_HYPERGRAPH.md` | Hypergraph snapshot generation |
| AUDIT_HYPERGRAPH_CLOSURE | `AGENT_AUDIT_HYPERGRAPH_CLOSURE.md` | Hypergraph closure audit |
| AUDIT_GOVERNANCE | `AGENT_AUDIT_GOVERNANCE.md` | Governance document consistency audit |
| AUDIT_EPISTEMIC | `AGENT_AUDIT_EPISTEMIC.md` | Deliverable epistemic ontology audit |
| AUDIT_SCOPE_CLOSURE | `AGENT_AUDIT_SCOPE_CLOSURE.md` | Scope change closure audit |
| EVALUATION_REPORT | `AGENT_EVALUATION_REPORT.md` | Scored dimension evaluation |
| EVALUATION_STRUCTURE_AUDIT | `AGENT_EVALUATION_STRUCTURE_AUDIT.md` | Structural validation |
| EVALUATION_DEPENDENCY_AUDIT | `AGENT_EVALUATION_DEPENDENCY_AUDIT.md` | Dependency validation |

An Agent 2 may instead be an ephemeral bounded generalist. That form has no persistent instruction file and is governed by the sealed brief contract above. The named dedicated specialists in this table are approved by D-GOV-13 and remain executable only when their declared parent, context, tool, permission, and write-scope gates pass.

### TASK Skill Capabilities

`TASK` dispatches repo-native method packs through `TaskSkill: <name>`. The authoritative skill inventory is the set of immediate `skills/` subdirectories that contain `SKILL.md`, governed by `skills/README.md` and validated by `tools/validation/validate_skill_metadata.py`.

This file is not the complete skill registry. It lists only canonical dispatch relationships needed to understand the agent architecture. For full membership, folder contracts, legacy status, and discovery rules, read `skills/README.md` and the target skill folder.

| Dispatcher | Canonical TASK skill relationships |
|---|---|
| PROJECT_SETUP | Dispatches setup, decomposition-support, document-production, semantic, dependency, and estimation skills as required by the active phase. See `skills/README.md` and live `skills/*/SKILL.md` files for the current inventory. |
| SCOPE_CHANGE | Dispatches bounded remediation and decomposition-package review skills for closure support. |
| WORKING_ITEMS | Manages one activated package and dispatches deliverable production, consistency, proposal-format, equipment, content-digest, and the five `software-*` skills according to its work graph. Software activations conform to `docs/SOFTWARE_WORKFLOW_PROFILE.md`; no SOFTWARE_DEV persona is live. |
| PDF2MD | Dispatches `TASK + pdf2md-page` for per-page transcription and, when `ASSET_MODE=prose`, `TASK + pdf2md-page-assets` for page-bounded asset discovery. `TASK + pdf2md` is available for smaller single-run conversions where full PDF2MD orchestration is unnecessary. |
| EQUATION_AUDIT | Dispatches `TASK + equation-flag-interpret` per flagged equation whose `description` is a natural-language note (one TASK per such entry, in Phase 3a); when `ENABLE_CROPS=true`, also dispatches `TASK + equation-bbox-detect` per page that contains display equations (Phase 1). |
| DRAWING_EXTRACT | Dispatches target-specific drawing skills, including `drawing-extract-page`, `drawing-titleblock-page`, and `pandid-valve-symbol-instance`, according to the `(DRAWING_TYPE, EXTRACTION_TARGET)` registry in `AGENT_DRAWING_EXTRACT.md`. |
| DBM_PUBLISHER | Dispatches `TASK + dbm-section-publish` for section synthesis, `TASK + dbm-publish` for package assembly/readiness artifacts, and `TASK + dbm-postauthor-concordance` for post-authoring evidence-bundle review. It may dispatch `TASK + dbm-concordance-verify` when optional semantic cross-section review is selected. |
| DOMAIN_DECOMP | Dispatches `TASK + domain-source-atomize` once per skeleton-dispatch-unit during Phase 2 (per-source fan-out, ~15k MD tokens per unit, ~85–125 dispatches across a 5-book corpus). The dispatch plan is produced by `tools/decomp/build_source_skeleton.py`; per-unit briefs are rendered by `tools/decomp/build_atomization_brief.py`. Per-unit CSVs are merged into per-source then cross-source ledgers via `tools/decomp/merge_source_atomizations.py`. |

Do not infer active skill status from older narrative lists. If `AGENTS.md`, `skills/README.md`, and live skill folders disagree, treat the live skill folder plus `skills/README.md` as the current skill registry and surface the discrepancy.

---

## Shared Runtime Doctrine

D-GOV-20 establishes root `runtime/` as the generic executable agent-runtime
workspace. One opt-in per-user daemon owns engines, credentials, sessions,
delegation, tools, turn locks, interruption, and model residency. Registered
projects retain checkout-contained authority; daemon user-data state is
operational only. Agent 0/1/2 roles remain authority contracts independent of
models, while every run records its actual engine/provider/model.

Project/domain adapters retain their own deterministic acts, data boundaries,
human gates, and evidence. Generic runtime transport never grants project
authority. Public export may include generic runtime/CLI/contracts/safe
adapters but excludes credentials, machine state, downloaded models, and
private project adapters/evidence.

---

EOF
