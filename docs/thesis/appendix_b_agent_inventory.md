# Appendix B — Agent Inventory

This appendix provides the complete classification of the 37 agent instruction files in the Chirality agent suite. The inventory is organized across four sections: the two-dimensional agent matrix that positions agents by epistemic posture and functional role; the complete classification table enumerating each agent's type, class, interaction surface, write scope, blocking behavior, and primary outputs; the spawning graph showing orchestration dependencies among Type 1 and Type 2 agents; and the variant coverage matrix showing which agents operate across the PROJECT, SOFTWARE, and DOMAIN decomposition variants.

---

## B.1 The Agent Matrix

The agent matrix organizes the suite along two axes drawn from the Chirality semantic framework. The row axis represents **epistemic posture** — the agent's relationship to validated knowledge: NORMATIVE agents operate on established project facts; OPERATIVE agents execute bounded work within a defined scope; EVALUATIVE agents assess and interrogate what has been produced. The column axis represents **functional role** — the agent's mode of action: GUIDING provides orientation and routing; APPLYING executes transformations; JUDGING makes structured assessments; REVIEWING synthesizes and reconciles across boundaries.

The matrix position of each cell names an abstract functional role rather than a single agent — individual agents in the index are instantiations of these roles. The asterisk (*) in the OPERATIVE row indicates that each cell in that row is populated by a family of variant-specific agents (e.g., DECOMP\* encompasses PROJECT_DECOMP, SOFTWARE_DECOMP, and DOMAIN_DECOMP).

The two interaction modes follow from row membership: the NORMATIVE and EVALUATIVE rows open in **WORKBENCH** (interactive conversational sessions); the OPERATIVE row opens in **PIPELINE** (brief-driven task execution with category dropdowns).

|  | **GUIDING** | **APPLYING** | **JUDGING** | **REVIEWING** |
|:---|:---|:---|:---|:---|
| **NORMATIVE** | HELP | ORCHESTRATE | WORKING_ITEMS | AGGREGATE |
| **OPERATIVE** | DECOMP\* | PREP\* | TASK\* | AUDIT\* |
| **EVALUATIVE** | AGENTS | DEPENDENCIES | CHANGE | RECONCILING |

---

## B.2 Complete Classification Table

The following table enumerates all 37 agent instruction files in the `agents/` directory. Each row records the agent's position in the type hierarchy (Type 0 = canonical standard, Type 1 = interactive persona, Type 2 = bounded task agent), its class (PERSONA for conversational agents; TASK for straight-through execution agents), its interaction surface (how the agent is invoked), its declared write scope (the filesystem area the agent may write to), whether the agent may block for human input, and its primary outputs. The write scope declaration is a formal architectural constraint: no agent may write outside its declared scope, enforcing fault containment across the suite.

The six agents in the evaluation subsystem (EVALUATION, TOOLMAKER, CONTENT_DIGEST, EVALUATION_REPORT, EVALUATION_STRUCTURE_AUDIT, EVALUATION_DEPENDENCY_AUDIT) were added to the suite subsequent to the initial publication of the DBM and are included here for completeness.

| Agent | Type | Class | Surface | Write Scope | Blocking | Primary Outputs |
|-------|:----:|-------|---------|-------------|:--------:|-----------------|
| **HELPS_HUMANS** | 0 | PERSONA | chat | none | — | Workflow design standards |
| **DECOMP_BASE** | 0 | PERSONA | chat | none | — | Decomposition protocol standard |
| **HELP_HUMAN** | 1 | PERSONA | chat | none (drafts briefs) | never | Run plans, briefs, checklists, next-step cards |
| **ORCHESTRATOR** | 1 | PERSONA | chat | tool-root (`_Coordination/`) | allowed | `_COORDINATION.md`, `NEXT_INSTANCE_PROMPT.md`, `NEXT_INSTANCE_STATE.md`; spawns setup pipelines |
| **WORKING_ITEMS** | 1 | PERSONA | chat | deliverable-local | allowed | Updated deliverable artifacts, `MEMORY.md` |
| **RECONCILIATION** | 1 | PERSONA | chat | tool-root (`_Reconciliation/`) | allowed | Run summaries, handoff requests |
| **CHANGE** | 1 | PERSONA | chat | tool-root (`_Change/`) + repo (approval-gated) | allowed | Git state reports; approved file/git actions |
| **PROJECT_DECOMP** | 1 | PERSONA | chat | project-level | allowed | SSOW decomposition document |
| **SOFTWARE_DECOMP** | 1 | PERSONA | chat | project-level | allowed | Software decomposition with Context Envelopes |
| **DOMAIN_DECOMP** | 1 | PERSONA | chat | repo-metadata-only | allowed | SDO domain decomposition document |
| **SCOPE_CHANGE** | 1 | PERSONA | chat | project-level | allowed (5 gates) | Amended decomposition, impact assessment, propagation record |
| **CONTEXT_TRANSPOSE** | 1 | PERSONA | chat | repo-metadata-only | allowed (7 gates) | CTSP snapshot, patch plan |
| **REVIEW** | 1 | PERSONA | chat | deliverable-local + tool-root | allowed (5 gates) | Review checklist, finding register, lifecycle transition record |
| **SCHEDULING** | 1 | PERSONA | chat | tool-root (`_Schedule/`) | allowed (5 gates) | Schedule structure, Gantt, critical path report |
| **EVALUATION** | 1 | PERSONA | chat | tool-root (`_Evaluation/`) | allowed | `EVALUATION_PROTOCOL.md`, `EVALUATION_REPORT.md`, pointers to Type 2 outputs |
| **TOOLMAKER** | 1 | PERSONA | chat | repo-wide (tools directory + agent instruction updates) | allowed | Shell scripts, Python utilities, skill templates, tool registry |
| **PREPARATION** | 2 | TASK | spawned | workspace-scaffold-only | never | Package/deliverable/category/KT folders with minimum viable fileset |
| **4_DOCUMENTS** | 2 | TASK | spawned | deliverable-local | never | Datasheet, Specification, Guidance, Procedure; `_STATUS.md` update |
| **DOMAIN_DOCUMENTS** | 2 | TASK | spawned | knowledge-type-local | never | `Scoping.md` + variable `KA-*.md` Knowledge Artifacts |
| **CHIRALITY_FRAMEWORK** | 2 | TASK | spawned/INIT | deliverable-local | never | `_SEMANTIC.md`; `_STATUS.md` → SEMANTIC_READY |
| **CHIRALITY_LENS** | 2 | TASK | spawned/INIT | deliverable-local | never | `_SEMANTIC_LENSING.md` |
| **DEPENDENCIES** | 2 | TASK | INIT-TASK | deliverable-local (dep artifacts only) | never | `Dependencies.csv`, `_DEPENDENCIES.md` |
| **ESTIMATING** | 2 | TASK | INIT-TASK | tool-root (`_Estimates/`) | never | Estimate snapshot (Summary, Detail.csv, QA, logs) |
| **ESTIMATE_PREP** | 2 | TASK | INIT-TASK | tool-root (`_EstimatePrep/`) | never | 18-file pricing library, BOE scaffold/full |
| **AGGREGATION** | 2 | TASK | INIT-TASK | tool-root (`_Aggregation/`) | never | Aggregation snapshot (indexes, registers, rollups) |
| **TASK** | 2 | TASK | INIT-TASK | deliverable-local | never | Proposals; optional authorized edits |
| **AUDIT_AGENTS** | 2 | TASK | INIT-TASK | tool-root (`_Reconciliation/AgentAudit/`) | never | Audit report, issue log, patch plan |
| **AUDIT_DECOMP** | 2 | TASK | INIT-TASK | tool-root (`_Reconciliation/DecompCoverage/`) | never | Coverage report, issue log CSV, coverage matrix, summary JSON |
| **AUDIT_DEP_CLOSURE** | 2 | TASK | INIT-TASK | tool-root (`_Reconciliation/DepClosure/`) | never | Closure report, issue log, JSON summary, analysis script |
| **DOMAIN_HYPERGRAPH** | 2 | TASK | INIT-TASK | tool-root (`_Aggregation/Hypergraph/`) | never | Hypergraph snapshot: `nodes.csv`, `hyperedges.csv`, `incidence.csv`, `hypergraph.json`, QA + evidence |
| **AUDIT_HYPERGRAPH_CLOSURE** | 2 | TASK | INIT-TASK | tool-root (`_Reconciliation/HypergraphClosure/`) | never | Closure report, issue log, JSON summary, analysis script |
| **CONTENT_DIGEST** | 2 | TASK | INIT-TASK | tool-root (`_Evaluation/content-digests/`) | never | `{DEL-ID}.md` — structured content digest for one deliverable |
| **EVALUATION_REPORT** | 2 | TASK | INIT-TASK | tool-root (`_Evaluation/reports/`) | never | `DIM-{NN}_{DimensionName}.md` — scored dimension evaluation report |
| **EVALUATION_STRUCTURE_AUDIT** | 2 | TASK | INIT-TASK | tool-root (`_Evaluation/reports/`) | never | Structure audit report with file counts, lifecycle state distribution, violation list |
| **EVALUATION_DEPENDENCY_AUDIT** | 2 | TASK | INIT-TASK | tool-root (`_Evaluation/reports/`) | never | Dependency audit report with per-deliverable schema check, anchor check, evidence check |

**Type counts:** 2 Type 0 agents · 14 Type 1 agents · 21 Type 2 agents · **37 total**

---

## B.3 Spawning Graph

The spawning graph shows the orchestration relationships among Type 1 and Type 2 agents — specifically, which Type 1 agents are authorized to dispatch which Type 2 agents, and under what conditions. This graph enforces the authority hierarchy defined in §2 of the DBM: Type 2 agents never spawn other agents; Type 1 agents may spawn Type 2 agents but only within their designated orchestration scope; and no agent of any type may bypass human gates.

Agents annotated with `[DOMAIN only]` are dispatched exclusively when the active decomposition variant is DOMAIN. Agents annotated as `leaf` or `standalone` represent Type 1 agents that do not spawn Type 2 agents but instead produce outputs directly or hand off to a peer Type 1 agent via a defined protocol.

```
HELP_HUMAN (Type 1 — classifies intent, routes to agents; does not spawn)

ORCHESTRATOR (Type 1) ──spawns──┬── PREPARATION (Type 2)
                                ├── 4_DOCUMENTS (Type 2)
                                ├── DOMAIN_DOCUMENTS (Type 2)
                                ├── CHIRALITY_FRAMEWORK (Type 2)
                                ├── CHIRALITY_LENS (Type 2)
                                ├── DOMAIN_HYPERGRAPH (Type 2) [DOMAIN only; Phase 2.6]
                                ├── ESTIMATING (Type 2)
                                └── AGGREGATION (Type 2)

WORKING_ITEMS (Type 1) ──spawns──── TASK (Type 2)

RECONCILIATION (Type 1) ──spawns──┬── AUDIT_DEP_CLOSURE (Type 2)
                                  ├── AUDIT_AGENTS (Type 2)
                                  ├── AUDIT_DECOMP (Type 2)
                                  └── AUDIT_HYPERGRAPH_CLOSURE (Type 2) [DOMAIN only]

EVALUATION (Type 1) ──spawns──┬── CONTENT_DIGEST (Type 2)
                              ├── EVALUATION_REPORT (Type 2)
                              ├── EVALUATION_STRUCTURE_AUDIT (Type 2)
                              └── EVALUATION_DEPENDENCY_AUDIT (Type 2)

CHANGE (Type 1) ── leaf agent (spawns nothing; implements approved edits)

REVIEW (Type 1) ── triggers AUDIT_DECOMP as precondition check
SCOPE_CHANGE (Type 1) ── hands off to ORCHESTRATOR (for PREPARATION) + CHANGE (for commits)
CONTEXT_TRANSPOSE (Type 1) ── hands off to CHANGE (for publication)
SCHEDULING (Type 1) ── standalone (reads dependency graph; produces schedule artifacts)
TOOLMAKER (Type 1) ── standalone (produces tools directly; no Type 2 delegation)
```

---

## B.4 Variant Coverage Matrix

The variant coverage matrix records which agents operate within each of the three decomposition variants — PROJECT (EPC/design-build), SOFTWARE (software development), and DOMAIN (handbook/knowledge domain) — and which agents are variant-independent. Variant-independent agents either operate at a layer above any specific decomposition context (e.g., CHANGE, which manages git state regardless of project type) or define the standards to which all variants conform (e.g., HELPS_HUMANS, DECOMP_BASE).

Agents that support multiple variants use `DECOMP_VARIANT` auto-detection at runtime: a folder name prefix of `KTY-` indicates DOMAIN variant; otherwise PROJECT or SOFTWARE is inferred from the decomposition structure. Cells marked `yes` indicate the agent is designed and tested to operate correctly within that variant. Cells marked `—` indicate the agent does not apply to that variant, either because the artifact types it consumes do not exist in that variant (e.g., DEPENDENCIES does not operate in DOMAIN, which has no dependency graph) or because the agent is variant-agnostic.

| Agent | PROJECT | SOFTWARE | DOMAIN | Variant-Independent |
|-------|:-------:|:--------:|:------:|:-------------------:|
| **DECOMP agents** | PROJECT_DECOMP | SOFTWARE_DECOMP | DOMAIN_DECOMP | — |
| **ORCHESTRATOR** | yes | yes | yes | — |
| **PREPARATION** | yes | yes | yes | — |
| **4_DOCUMENTS** | yes | yes | — | — |
| **DOMAIN_DOCUMENTS** | — | — | yes | — |
| **CHIRALITY_FRAMEWORK** | yes | yes | yes | — |
| **CHIRALITY_LENS** | yes | yes | yes | — |
| **DEPENDENCIES** | yes | yes | — | — |
| **ESTIMATING** | yes | yes | — | — |
| **ESTIMATE_PREP** | yes | yes | — | — |
| **SCHEDULING** | yes | yes | — | — |
| **AGGREGATION** | yes | yes | yes | — |
| **AUDIT_DEP_CLOSURE** | yes | yes | — | — |
| **DOMAIN_HYPERGRAPH** | — | — | yes | — |
| **AUDIT_HYPERGRAPH_CLOSURE** | — | — | yes | — |
| **AUDIT_DECOMP** | yes | yes | yes | — |
| **WORKING_ITEMS** | yes | yes | yes | — |
| **TASK** | yes | yes | yes | — |
| **REVIEW** | yes | yes | yes | — |
| **SCOPE_CHANGE** | yes | yes | — | — |
| **RECONCILIATION** | yes | yes | yes | — |
| **EVALUATION** | yes | yes | yes | — |
| **CONTENT_DIGEST** | yes | yes | yes | — |
| **EVALUATION_REPORT** | yes | yes | yes | — |
| **EVALUATION_STRUCTURE_AUDIT** | yes | yes | yes | — |
| **EVALUATION_DEPENDENCY_AUDIT** | yes | yes | — | — |
| **CHANGE** | — | — | — | yes |
| **HELP_HUMAN** | — | — | — | yes |
| **TOOLMAKER** | — | — | — | yes |
| **HELPS_HUMANS** | — | — | — | yes |
| **DECOMP_BASE** | — | — | — | yes |
| **AUDIT_AGENTS** | — | — | — | yes |
| **CONTEXT_TRANSPOSE** | — | — | — | yes |
