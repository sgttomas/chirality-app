# AGENTS — Agent Index

This file indexes the agent suite. For classification semantics, see `docs/TYPES.md` §4. For the full design basis, see `docs/DBM_Agent_Instruction_Architecture.md`.

Use `AGENT_*` for instruction files (e.g., `AGENT_CHANGE.md`). Use the role name for the agent itself (e.g., `CHANGE`). All files are in `agents/`.

---

## Agent Matrix

Rows describe epistemic posture; columns describe functional role. NORMATIVE and EVALUATIVE rows open in WORKBENCH (interactive). OPERATIVE row opens in PIPELINE (task execution).

Read structurally, the rows also form a governance grammar: NORMATIVE defines rules and standards, OPERATIVE executes bounded work within them, and EVALUATIVE audits, reconciles, and judges the results.

|  | **GUIDING** | **APPLYING** | **JUDGING** | **REVIEWING** |
| --- | --- | --- | --- | --- |
| **NORMATIVE** | HELP_HUMAN | ORCHESTRATOR | WORKING_ITEMS | AGGREGATION |
| **OPERATIVE** | DECOMP\* | PREPARATION | TASK | AUDIT\* |
| **EVALUATIVE** | HELPS_HUMANS | — | CHANGE | RECONCILIATION |

### Operative Row — Pipeline Categories

The OPERATIVE row opens in PIPELINE (task execution). The `PREPARATION` and `TASK` cells name canonical shells directly. Wildcard cells (`DECOMP*`, `AUDIT*`, `PDF2MD*`, `DRAWING_EXTRACT*`) still expand to agent groups, grouped by `PipelineCategory` (see `TYPES.md` §9.2).

**DECOMP\*:** PROJECT_DECOMP, SOFTWARE_DECOMP, DOMAIN_DECOMP, SCOPE_CHANGE

**PDF2MD\*:** PDF2MD

**DRAWING_EXTRACT\*:** DRAWING_EXTRACT

**AUDIT\*:** AUDIT_AGENTS, AUDIT_DECOMP, AUDIT_DEP_CLOSURE, AUDIT_HYPERGRAPH_CLOSURE, AUDIT_GOVERNANCE, AUDIT_EPISTEMIC, AUDIT_SCOPE_CLOSURE, EVALUATION_REPORT, EVALUATION_STRUCTURE_AUDIT, EVALUATION_DEPENDENCY_AUDIT

Other live task-family agents (DELIVERABLE_TASK, AGGREGATION, DOMAIN_HYPERGRAPH) are indexed below by type. Canonical methods previously exposed through archived wrapper agents are now dispatched via `TASK` + `TaskSkill: <name>` (see "TASK Skill Capabilities" below).

---

## Agent Index

### Type 0 — Canonical Standards

| Agent | Instruction File | Role |
| --- | --- | --- |
| HELPS_HUMANS | `AGENT_HELPS_HUMANS.md` | Workflow design standard governing agents, skills, and tools; all workflow components must conform |
| DECOMP_BASE | `AGENT_DECOMP_BASE.md` | Decomposition protocol standard (7-gate, I1–I10) |

### Type 1 — Interactive Personas

| Agent | Instruction File | Role |
| --- | --- | --- |
| HELP_HUMAN | `AGENT_HELP_HUMAN.md` | Operator assistance; classifies intent, drafts briefs |
| ORCHESTRATOR | `AGENT_ORCHESTRATOR.md` | Project setup, tier sequencing, control loops |
| WORKING_ITEMS | `AGENT_WORKING_ITEMS.md` | Deliverable-scoped content production |
| RECONCILIATION | `AGENT_RECONCILIATION.md` | Cross-deliverable coherence analysis |
| CHANGE | `AGENT_CHANGE.md` | Git state management with approval gates |
| PROJECT_DECOMP | `AGENT_PROJECT_DECOMP.md` | EPC / design-build decomposition |
| SOFTWARE_DECOMP | `AGENT_SOFTWARE_DECOMP.md` | Software decomposition with Context Envelopes |
| DOMAIN_DECOMP | `AGENT_DOMAIN_DECOMP.md` | Handbook / knowledge domain decomposition |
| SCOPE_CHANGE | `AGENT_SCOPE_CHANGE.md` | Change impact assessment and decomposition amendment |
| CONTEXT_TRANSPOSE | `AGENT_CONTEXT_TRANSPOSE.md` | Cross-context structural transposition |
| REVIEW | `AGENT_REVIEW.md` | Formal 5-gate review for lifecycle transitions |
| SCHEDULING | `AGENT_SCHEDULING.md` | Schedule generation from dependency graph |
| EVALUATION | `AGENT_EVALUATION.md` | Project evaluation orchestration |
| TOOLMAKER | `AGENT_TOOLMAKER.md` | Deterministic tool design and implementation |
| SKILLMAKER | `AGENT_SKILLMAKER.md` | Skill design, governance, and subsystem ownership |
| PDF2MD | `AGENT_PDF2MD.md` | Native PDF-to-Markdown conversion pipeline; orchestrates rasterization, batch VLM dispatch, post-processing, assembly |
| DRAWING_EXTRACT | `AGENT_DRAWING_EXTRACT.md` | Drawing extraction pipeline; orchestrates rasterization, crop-first multiblock page extraction, deterministic QA, and structured output assembly |

### Type 2 — Bounded Task Agents

| Agent | Instruction File | Role |
| --- | --- | --- |
| PREPARATION | `AGENT_PREPARATION.md` | Scaffold package/deliverable folders |
| AGGREGATION | `AGENT_AGGREGATION.md` | Cross-scope synthesis snapshots |
| TASK | `AGENT_TASK.md` | Generic bounded-task shell; loads profile/skill and executes within explicit scope |
| DELIVERABLE_TASK | `AGENT_DELIVERABLE_TASK.md` | Preserved deliverable-local SME helper workflow |
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

### TASK Skill Capabilities

Skills dispatched through TASK (via `TaskSkill: <name>`) codify recurring bounded methods. These methods were previously exposed as thin wrapper agents; they are now routed directly through the canonical TASK shell.

| Skill | Folder | Purpose | Typical dispatcher |
|---|---|---|---|
| four-documents | `skills/four-documents/` | Draft + enrich Datasheet/Specification/Guidance/Procedure | ORCHESTRATOR Phase 2.2 + 2.5 |
| domain-documents | `skills/domain-documents/` | Draft + verify Knowledge Artifacts for DOMAIN variants | ORCHESTRATOR Phase 2.2 |
| semantic-matrix-build | `skills/semantic-matrix-build/` | Generate `_SEMANTIC.md` semantic matrix | ORCHESTRATOR Phase 2.3 |
| lens-register | `skills/lens-register/` | Generate `_SEMANTIC_LENSING.md` enrichment register | ORCHESTRATOR Phase 2.4 |
| dependency-extract | `skills/dependency-extract/` | Extract `Dependencies.csv` v3.1 + `_DEPENDENCIES.md` | ORCHESTRATOR setup + control-loop refresh |
| semantic-lensing | `skills/semantic-lensing/` | Apply lensing register during content enrichment | DELIVERABLE_TASK, WORKING_ITEMS |
| content-digest | `skills/content-digest/` | Produce content digest snapshots | EVALUATION and others |
| estimate-snapshot | `skills/estimate-snapshot/` | Run per-deliverable estimate snapshots | ORCHESTRATOR Phase 4 (Estimating) |
| estimate-prep | `skills/estimate-prep/` | Prepare estimation inputs (BOE, INDEX.md) | ORCHESTRATOR pre-Phase-4 |
| pdf2md-page | `skills/pdf2md-page/` | Per-page VLM markdown extraction | PDF2MD orchestrator |
| drawing-extract-page | `skills/drawing-extract-page/` | Per-page equipment drawing extraction | DRAWING_EXTRACT orchestrator |

See `skills/README.md` for the full skill inventory and folder contract.

---

EOF
