# AGENTS — Agent Index

This file indexes the agent suite. For classification semantics, see `docs/TYPES.md` §4. For the full design basis, see `docs/DBM_Agent_Instruction_Architecture.md`.

Use `AGENT_*` for instruction files (e.g., `AGENT_CHANGE.md`). Use the role name for the agent itself (e.g., `CHANGE`). All files are in `agents/`.

---

## Agent Matrix

Rows describe epistemic posture; columns describe functional role. NORMATIVE and EVALUATIVE rows open in WORKBENCH (interactive). OPERATIVE row opens in PIPELINE (task execution).

|  | **GUIDING** | **APPLYING** | **JUDGING** | **REVIEWING** |
| --- | --- | --- | --- | --- |
| **NORMATIVE** | HELP_HUMAN | ORCHESTRATOR | WORKING_ITEMS | AGGREGATION |
| **OPERATIVE** | DECOMP\* | PREP\* | TASK\* | AUDIT\* |
| **EVALUATIVE** | HELPS_HUMANS | DEPENDENCIES | CHANGE | RECONCILIATION |

### Operative Row — Pipeline Categories

The OPERATIVE row opens in PIPELINE (task execution). Each wildcard cell expands to the agents listed below, grouped by `PipelineCategory` (see `TYPES.md` §9.2).

**DECOMP\*:** PROJECT_DECOMP, SOFTWARE_DECOMP, DOMAIN_DECOMP, SCOPE_CHANGE

**PREP\*:** PREPARATION, 4_DOCUMENTS, DOMAIN_DOCUMENTS, ESTIMATE_PREP, PDF2MD_PAGE

**TASK\*:** TASK, CHIRALITY_FRAMEWORK, CHIRALITY_LENS, DEPENDENCIES, ESTIMATING, AGGREGATION, DOMAIN_HYPERGRAPH, CONTENT_DIGEST

**AUDIT\*:** AUDIT_AGENTS, AUDIT_DECOMP, AUDIT_DEP_CLOSURE, AUDIT_HYPERGRAPH_CLOSURE, AUDIT_GOVERNANCE, AUDIT_EPISTEMIC, AUDIT_SCOPE_CLOSURE, EVALUATION_REPORT, EVALUATION_STRUCTURE_AUDIT, EVALUATION_DEPENDENCY_AUDIT

---

## Agent Index

### Type 0 — Canonical Standards

| Agent | Instruction File | Role |
| --- | --- | --- |
| HELPS_HUMANS | `AGENT_HELPS_HUMANS.md` | Workflow design standard; all agents must conform |
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
| PDF2MD | `AGENT_PDF2MD.md` | Native PDF-to-Markdown conversion pipeline; orchestrates rasterization, batch VLM dispatch, post-processing, assembly |

### Type 2 — Bounded Task Agents

| Agent | Instruction File | Role |
| --- | --- | --- |
| PREPARATION | `AGENT_PREPARATION.md` | Scaffold package/deliverable folders |
| 4_DOCUMENTS | `AGENT_4_DOCUMENTS.md` | Draft four-document kit |
| DOMAIN_DOCUMENTS | `AGENT_DOMAIN_DOCUMENTS.md` | Knowledge artifact files for domain decompositions |
| CHIRALITY_FRAMEWORK | `AGENT_CHIRALITY_FRAMEWORK.md` | Semantic analysis (`_SEMANTIC.md`) |
| CHIRALITY_LENS | `AGENT_CHIRALITY_LENS.md` | Semantic lensing narrative |
| DEPENDENCIES | `AGENT_DEPENDENCIES.md` | Dependency register extraction (CSV v3.1) |
| ESTIMATING | `AGENT_ESTIMATING.md` | Parameterized cost estimation snapshots |
| ESTIMATE_PREP | `AGENT_ESTIMATE_PREP.md` | Pricing library and BOE scaffold |
| AGGREGATION | `AGENT_AGGREGATION.md` | Cross-scope synthesis snapshots |
| TASK | `AGENT_TASK.md` | Brief-driven deliverable-local execution |
| AUDIT_AGENTS | `AGENT_AUDIT_AGENTS.md` | Agent instruction conformance audit |
| AUDIT_DECOMP | `AGENT_AUDIT_DECOMP.md` | Decomposition coverage audit |
| AUDIT_DEP_CLOSURE | `AGENT_AUDIT_DEP_CLOSURE.md` | Dependency closure audit |
| DOMAIN_HYPERGRAPH | `AGENT_DOMAIN_HYPERGRAPH.md` | Hypergraph snapshot generation |
| AUDIT_HYPERGRAPH_CLOSURE | `AGENT_AUDIT_HYPERGRAPH_CLOSURE.md` | Hypergraph closure audit |
| AUDIT_GOVERNANCE | `AGENT_AUDIT_GOVERNANCE.md` | Governance document consistency audit |
| AUDIT_EPISTEMIC | `AGENT_AUDIT_EPISTEMIC.md` | Deliverable epistemic ontology audit |
| AUDIT_SCOPE_CLOSURE | `AGENT_AUDIT_SCOPE_CLOSURE.md` | Scope change closure audit |
| CONTENT_DIGEST | `AGENT_CONTENT_DIGEST.md` | Per-deliverable structured content digest |
| EVALUATION_REPORT | `AGENT_EVALUATION_REPORT.md` | Scored dimension evaluation |
| EVALUATION_STRUCTURE_AUDIT | `AGENT_EVALUATION_STRUCTURE_AUDIT.md` | Structural validation |
| EVALUATION_DEPENDENCY_AUDIT | `AGENT_EVALUATION_DEPENDENCY_AUDIT.md` | Dependency validation |
| PDF2MD_PAGE | `AGENT_PDF2MD_PAGE.md` | Single-page PDF-to-Markdown via multimodal vision; spawned per page by PDF2MD |

---

EOF