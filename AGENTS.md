# AGENTS — Agent Index

This file indexes the agent suite. For classification semantics, see `docs/TYPES.md` §4. For the full design basis, see `docs/DBM_Agent_Instruction_Architecture.md`.

Use `AGENT_*` for instruction files (e.g., `AGENT_CHANGE.md`). Use the role name for the agent itself (e.g., `CHANGE`). All files are in `agents/`.

---

## Agent Matrix

Rows describe epistemic posture; columns describe functional role. NORMATIVE and EVALUATIVE rows open in WORKBENCH (interactive). OPERATIVE row opens in PIPELINE (task execution).

Read structurally, the rows also form a governance grammar: NORMATIVE defines rules and standards, OPERATIVE executes bounded work within them, and EVALUATIVE audits, reconciles, and judges the results.

### Governance Integration Rules

- **Derivative-package rule.** Any package assembled from accepted upstream truth but not itself authoritative decomposition truth is a derivative package. This includes regenerated KTY-local artifacts, `_Aggregation` outputs, hypergraph snapshots, audit snapshots, concordance packages, and publication packages. Derivative packages must cite their accepted upstream snapshot(s) and must never be treated as a substitute for decomposition truth.
- **Snapshot rule.** Every phase-boundary decision that changes or validates governed state must terminate in a new immutable snapshot and a pointer update only where the owning workflow explicitly permits one. Later phases consume accepted snapshots; they do not rely on mutable working state alone.
- **Handoff-state rule.** Any workflow that stops with work intended for another agent or later phase must emit an explicit handoff state that names the accepted upstream snapshot(s), derivative-package status, closure verdict, rerun requirements, and remaining blockers.
- **Closure rule.** A scope unit or phase is not closed merely because files were written. Closure requires authoritative truth to be accepted, required derivative packages to be regenerated or explicitly deferred, audit status to be recorded, and unresolved blockers to be surfaced in the handoff state.
- **Sequencing rule.** If a later phase consumes derivative packages, it must run only after the upstream authoritative snapshot has been accepted and the required handoff state records which derivative packages are current.

|  | **GUIDING** | **APPLYING** | **JUDGING** | **REVIEWING** |
| --- | --- | --- | --- | --- |
| **NORMATIVE** | HELP_HUMAN | ORCHESTRATOR | WORKING_ITEMS | AGGREGATION |
| **OPERATIVE** | DECOMP\* | PREPARATION | TASK | AUDIT\* |
| **EVALUATIVE** | HELPS_HUMANS | DBM_PUBLISHER | CHANGE | RECONCILIATION |

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
| DOMAIN_ENGINE | `AGENT_DOMAIN_ENGINE.md` | Domain-engine integration manager; profiles, protected paths, adapter workflows, operation proposals, and human-gated domain handoffs |
| CONTEXT_TRANSPOSE | `AGENT_CONTEXT_TRANSPOSE.md` | Cross-context structural transposition |
| REVIEW | `AGENT_REVIEW.md` | Formal 5-gate review for lifecycle transitions |
| SCHEDULING | `AGENT_SCHEDULING.md` | Schedule generation from dependency graph |
| EVALUATION | `AGENT_EVALUATION.md` | Project evaluation orchestration |
| TOOLMAKER | `AGENT_TOOLMAKER.md` | Deterministic tool design and implementation |
| SKILLMAKER | `AGENT_SKILLMAKER.md` | Skill design, governance, and subsystem ownership |
| PDF2MD | `AGENT_PDF2MD.md` | Native PDF-to-Markdown conversion pipeline; orchestrates rasterization, batch VLM dispatch, post-processing, optional prose asset materialization, assembly |
| EQUATION_AUDIT | `AGENT_EQUATION_AUDIT.md` | Post-PDF2MD equation-review loop; iterates extract → human review → interpret prose notes → apply fixes → re-extract → backcheck → close, terminating in an immutable snapshot under `audit/equations/snapshots/`. Dispatches `equation-flag-interpret` per prose-shaped flag and `equation-bbox-detect` per page when crops are enabled |
| DRAWING_EXTRACT | `AGENT_DRAWING_EXTRACT.md` | Drawing-type-aware extraction pipeline; core-vs-repertoire split orchestrates rasterization, target-appropriate crops/tiles, target-specific TASK skill dispatch per (drawing_type × extraction_target), deterministic QA, target-driven assembly, and optional PFD-equipment merge. DRAWING_SET, PFD, and P_AND_ID targets are implemented; ISOMETRIC/GA remain stubbed fail-fast |
| DBM_PUBLISHER | `AGENT_DBM_PUBLISHER.md` | Publish one rewritten DBM from approved DOMAIN state using frozen planning artifacts, direct section dispatch, package assembly, and post-authoring evidence-bundle review |

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

`TASK` dispatches repo-native method packs through `TaskSkill: <name>`. The authoritative skill inventory is the set of immediate `skills/` subdirectories that contain `SKILL.md`, governed by `skills/README.md` and validated by `tools/validation/validate_skill_metadata.py`.

This file is not the complete skill registry. It lists only canonical dispatch relationships needed to understand the agent architecture. For full membership, folder contracts, legacy status, and discovery rules, read `skills/README.md` and the target skill folder.

| Dispatcher | Canonical TASK skill relationships |
|---|---|
| ORCHESTRATOR | Dispatches setup, decomposition-support, document-production, semantic, dependency, and estimation skills as required by the active phase. See `skills/README.md` and live `skills/*/SKILL.md` files for the current inventory. |
| SCOPE_CHANGE | Dispatches bounded remediation and decomposition-package review skills for closure support. |
| WORKING_ITEMS / DELIVERABLE_TASK | Dispatch deliverable-local production, consistency, proposal-format, equipment, and content-digest skills when the brief selects them. |
| PDF2MD | Dispatches `TASK + pdf2md-page` for per-page transcription and, when `ASSET_MODE=prose`, `TASK + pdf2md-page-assets` for page-bounded asset discovery. `TASK + pdf2md` is available for smaller single-run conversions where full PDF2MD orchestration is unnecessary. |
| EQUATION_AUDIT | Dispatches `TASK + equation-flag-interpret` per flagged equation whose `description` is a natural-language note (one TASK per such entry, in Phase 3a); when `ENABLE_CROPS=true`, also dispatches `TASK + equation-bbox-detect` per page that contains display equations (Phase 1). |
| DRAWING_EXTRACT | Dispatches target-specific drawing skills, including `drawing-extract-page`, `drawing-titleblock-page`, and `pandid-valve-symbol-instance`, according to the `(DRAWING_TYPE, EXTRACTION_TARGET)` registry in `AGENT_DRAWING_EXTRACT.md`. |
| DBM_PUBLISHER | Dispatches `TASK + dbm-section-publish` for section synthesis, `TASK + dbm-publish` for package assembly/readiness artifacts, and `TASK + dbm-postauthor-concordance` for post-authoring evidence-bundle review. It may dispatch `TASK + dbm-concordance-verify` when optional semantic cross-section review is selected. |
| DOMAIN_DECOMP | Dispatches `TASK + domain-source-atomize` once per skeleton-dispatch-unit during Phase 2 (per-source fan-out, ~15k MD tokens per unit, ~85–125 dispatches across a 5-book corpus). The dispatch plan is produced by `tools/decomp/build_source_skeleton.py`; per-unit briefs are rendered by `tools/decomp/build_atomization_brief.py`. Per-unit CSVs are merged into per-source then cross-source ledgers via `tools/decomp/merge_source_atomizations.py`. |

Do not infer active skill status from older narrative lists. If `AGENTS.md`, `skills/README.md`, and live skill folders disagree, treat the live skill folder plus `skills/README.md` as the current skill registry and surface the discrepancy.

---

EOF
