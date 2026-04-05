# Agent Suite Classification (Ruled)

## Status

**Ruled:** 48 of 48 files.
**Provisional:** 0 files. (DOMAIN_HYPERGRAPH → D; ESTIMATE_PREP → B ruled in Slice 2a.)
**Basis:** `NEXT_INSTANCE_PROMPT.md` handoff (6 categories, 3 foundational questions, per-candidate justification schema).
**Companion artifacts:** `plans/SEMANTIC_PIPELINE_ARCHITECTURE.md` (target model), `plans/AGENT_SUITE_EXECUTION_PLAN.md` (slice mechanics), `plans/CHIRALITY_LENS_MIGRATION.md` (Slice 4 detail).

---

## Methodology

### Six categories (per handoff §Expected output)

| Cat | Label | Definition |
|---|---|---|
| **A** | Keep as agent | Agent preserved without method extraction. Three role subtypes: **persona** (authority surface), **stable shell** (execution substrate), **bounded task role** (reasoning-heavy brief-driven role not reducible to a pure skill). |
| **B** | Convert to skill | Method moves to `skills/`; agent archives; orchestrator dispatches TASK+skill directly. |
| **C** | Keep as agent, invoke skill(s) | **Staged compatibility layer** (not final normalized architecture). Identity preserved (pipeline-stage or matrix-cell); method extracted to skill; agent becomes thin wrapper dispatching TASK+skill internally. For Type 2 task agents this is shell-on-shell indirection — acceptable as migration step, but full-normalization end state is B. |
| **D** | Keep as agent, invoke deterministic tool(s) | Agent orchestrates tool invocations; core work is deterministic. |
| **E** | Archive / remove | Orphaned, superseded, or relic. |
| **F** | Needs decomposition (provisional) | Mixes agent + skill + tool concerns; decomposition required before final ruling. |

### Three foundational questions

For each file:
1. **Q1:** Is this fundamentally a persona / authority surface?
2. **Q2:** Is this fundamentally a reusable bounded method?
3. **Q3:** Is this fundamentally deterministic machinery?

Multiple YES → provisional F.

### A-subtype definitions

**persona (19):** Interactive, authority-bearing. Distinct interaction surface (chat, gate-controlled, or dispatched). Owns human decision gates or cross-artifact judgment.

**stable shell (1):** Execution substrate that loads profiles/skills at runtime. Only member: TASK.

**bounded task role (7):** Type 2 brief-driven agent kept as distinct identity because its method is reasoning-heavy, cross-cutting, or not suited to skill compression today.

### Per-candidate justification schema

For each non-trivial classification:
- **Why** it belongs in that category
- **Invariant/boundary** it satisfies
- **What breaks** if moved incorrectly
- **Migration path** (if any)

### Biases applied

- **Portal coherence:** matrix-portal agents biased toward A/C/D over B/E. "Do not silently collapse authority-bearing personas into skills." (handoff)
- **Pipeline coherence:** pipeline-stage agents in ORCHESTRATOR's setup sequence biased toward C (preserve identity, extract method to skill). Full B migration reserved for whole-pipeline unit migration.

---

## Classification Matrix

### Portal (8 files)
| Agent | Q1 | Q2 | Q3 | Cat | Subtype / Target |
|---|---|---|---|---|---|
| HELP_HUMAN | YES | no | no | A | persona |
| ORCHESTRATOR | YES | part | part | A | persona |
| WORKING_ITEMS | YES | no | no | A | persona |
| AGGREGATION | no | YES | part | A | bounded task role |
| HELPS_HUMANS | YES | no | no | A | persona (Type 0) |
| DEPENDENCIES | no | YES | part | **C** | → `skills/dependency-extract/` |
| CHANGE | YES | no | no | A | persona |
| RECONCILIATION | YES | no | no | A | persona |

### DECOMP* (4 files) — all A (persona)
PROJECT_DECOMP, SOFTWARE_DECOMP, DOMAIN_DECOMP, SCOPE_CHANGE

### PREP* (4 files)
| Agent | Cat | Target |
|---|---|---|
| PREPARATION | **D** | invokes 7 scaffolding tools |
| 4_DOCUMENTS | **C** | → `skills/four-documents/` |
| DOMAIN_DOCUMENTS | **C** | → `skills/domain-documents/` |
| ESTIMATE_PREP | **B** | → `skills/estimate-prep/` (PHASE=SCAFFOLD\|BOE parameter) |

### TASK* (7 unique)
| Agent | Cat | Target |
|---|---|---|
| TASK | A | stable shell |
| DELIVERABLE_TASK | **C** | existing (→ skills/proposal-format + semantic-lensing) |
| CHIRALITY_FRAMEWORK | **C** | → `skills/semantic-matrix-build/` |
| CHIRALITY_LENS | **C** | → `skills/lens-register/` |
| ESTIMATING | **B** | → `skills/estimate-snapshot/` |
| DOMAIN_HYPERGRAPH | **D** | invokes new `tools/aggregation/build_hypergraph.py` |
| CONTENT_DIGEST | **B** | → `skills/content-digest/` |

### AUDIT* (10 files)
| Agent | Cat |
|---|---|
| AUDIT_AGENTS | A (bounded task role) |
| AUDIT_DECOMP | A (bounded task role) |
| AUDIT_DEP_CLOSURE | **D** |
| AUDIT_HYPERGRAPH_CLOSURE | **D** |
| AUDIT_GOVERNANCE | A (bounded task role) |
| AUDIT_EPISTEMIC | A (bounded task role) |
| AUDIT_SCOPE_CLOSURE | A (bounded task role) |
| EVALUATION_REPORT | A (bounded task role) |
| EVALUATION_STRUCTURE_AUDIT | **D** |
| EVALUATION_DEPENDENCY_AUDIT | **D** |

### Adjunct Pipeline (4 files)
| Agent | Cat | Target |
|---|---|---|
| PDF2MD | A (persona) | orchestrator |
| PDF2MD_PAGE | **B** | → `skills/pdf2md-page/` |
| DRAWING_EXTRACT | A (persona) | orchestrator |
| DRAWING_EXTRACT_PAGE | **B** | → `skills/drawing-extract-page/` |

### Adjunct Other (7 files)
| Agent | Cat |
|---|---|
| CONTEXT_TRANSPOSE | A (persona) |
| EVALUATION | A (persona) |
| REVIEW | A (persona) |
| SCHEDULING | A (persona) |
| SKILLMAKER | A (persona) |
| TOOLMAKER | A (persona) |
| EQUIPMENT_EXTRACT | **E** |

### Type 0 (1 file)
DECOMP_BASE — A (persona, Type 0 base specification)

### Non-agent files (3)
| File | Disposition |
|---|---|
| AUDIT_AGENT.md | relocation TBD (Slice 1b) — rubric worksheet |
| MEMORY_TEMPLATE.md | relocation TBD (Slice 1b) — artifact template |
| TASK_ESTIMATING_TEMPLATE.md | **E** (Slice 1a) — stale brief |

### Category tally

| Cat | Count | Notes |
|---|---|---|
| **A** | 27 | persona: 19 • stable shell: 1 • bounded task role: 7 |
| **B** | 5 | CONTENT_DIGEST, ESTIMATING, PDF2MD_PAGE, DRAWING_EXTRACT_PAGE, ESTIMATE_PREP |
| **C** | 6 | DELIVERABLE_TASK (existing), DEPENDENCIES, CHIRALITY_FRAMEWORK, CHIRALITY_LENS, 4_DOCUMENTS, DOMAIN_DOCUMENTS |
| **D** | 6 | PREPARATION, AUDIT_DEP_CLOSURE, AUDIT_HYPERGRAPH_CLOSURE, EVALUATION_STRUCTURE_AUDIT, EVALUATION_DEPENDENCY_AUDIT, DOMAIN_HYPERGRAPH |
| **E** | 2 | EQUIPMENT_EXTRACT, TASK_ESTIMATING_TEMPLATE |
| **F** | 0 | (resolved in Slice 2a) |
| Non-agent relocations | 2 | AUDIT_AGENT.md, MEMORY_TEMPLATE.md |

Total: **48** ✓

---

## Per-Candidate Justifications

### A — persona (shared rationale)

**Why A:** Distinct interaction surface, human decision gates or cross-artifact authority, not reducible to a bounded method. The agent's identity IS the authority role.

**Invariant:** Human decision rights preserved; authority separation (lifecycle gates, governance, acceptance); distinct scope boundary.

**What breaks if converted to skill:** Collapses authority-bearing persona into method-pack; loses gate discipline; human dispatch becomes ambiguous.

**Migration path:** None. Keep as-is.

**Members (19):** HELP_HUMAN, ORCHESTRATOR, WORKING_ITEMS, HELPS_HUMANS (Type 0), CHANGE, RECONCILIATION, PROJECT_DECOMP, SOFTWARE_DECOMP, DOMAIN_DECOMP, SCOPE_CHANGE, CONTEXT_TRANSPOSE, EVALUATION, REVIEW, SCHEDULING, SKILLMAKER, TOOLMAKER, PDF2MD, DRAWING_EXTRACT, DECOMP_BASE (Type 0).

### A — stable shell

**TASK**

**Why A:** The canonical execution substrate. Loads profiles + skills at runtime; provides scope boundaries + brief normalization + run-record contract. Not a method; not a persona; a platform.

**Invariant:** Shell hard-boundary discipline; skills + profiles are subordinate and cannot widen scope.

**What breaks if converted:** Circular dependency — the shell can't load itself as a skill. The compositional model (shell + profile + skill + tool + brief) loses its foundation.

**Migration path:** None. Structurally required.

### A — bounded task role (individual rationale)

**AGGREGATION** (portal: NORMATIVE/REVIEWING)

Multi-purpose aggregation role with 5 mission profiles (Estimate_Collation, Doc_Index, Register_Summary, CrossFile_QA, General_Aggregation). Agent instructions explicitly avoid prescribing implementation; the role IS the cross-cutting aggregator. Portal position reinforces distinct identity.

- **Invariant:** Filesystem-as-state, snapshot immutability, traceability (SourcePath + SectionRef), no-invention, conflict transparency, portal REVIEWING authority.
- **Breaks if converted:** 5 profiles have different schemas/dedup/conflict rules; single-skill conflation loses discipline.
- **Migration path:** None immediate. Re-evaluate when individual mission profiles mature to stable brief schemas + QA contracts.

**AUDIT_AGENTS**

Rubric-driven audit using `AUDIT_AGENT.md` worksheet. Reasoning-heavy conformance assessment produces patch plans + issue logs. The rubric-driven judgment is the identity.

- **Invariant:** Rubric discipline; issue-logged, non-destructive audit output.
- **Breaks if converted:** Patch-plan judgment reduces to mechanical checks; audit loses reasoning depth.
- **Migration path:** Future re-evaluation possible if the rubric becomes a deterministic checklist.

**AUDIT_DECOMP**

Variant-aware coverage audit (PROJECT/SOFTWARE/DOMAIN). 9 core interpretive checks tie decomposition documents to filesystem state.

- **Invariant:** Variant-binding discipline; interpretive checks not reducible to file-existence tests.
- **Breaks if converted:** Variant-specific reasoning flattens; coverage judgments become mechanical.
- **Migration path:** None immediate.

**AUDIT_GOVERNANCE**

Repo-wide meta audit of governance document suite (DIRECTIVE/CONTRACT/SPEC/TYPES/AGENTS). Cross-document consistency reasoning.

- **Invariant:** Governance document coherence; repo-wide scope distinct from project-instance audits.
- **Breaks if converted:** Cross-document reasoning flattens into pairwise diff-checks.
- **Migration path:** None.

**AUDIT_EPISTEMIC**

Claim-level reasoning audit against TYPES.md §10 epistemic ontology. 7-pass structure; evaluates label coverage, provenance, gaps, conflicts, warrant state.

- **Invariant:** Claim-level reasoning; epistemic ontology conformance.
- **Breaks if converted:** Claim-level judgment reduces to label-counting; epistemic audit loses interpretive depth.
- **Migration path:** None.

**AUDIT_SCOPE_CLOSURE**

Amendment verification dispatched by RECONCILIATION. Verifies SCOPE_CHANGE outcome — that a scope change has been fully propagated.

- **Invariant:** Scope-change lifecycle closure; distinct from structural audits.
- **Breaks if converted:** Lifecycle reasoning flattens; amendment-specific checks lost.
- **Migration path:** None.

**EVALUATION_REPORT**

Dimension scoring pipeline. Reads evidence + applies checks + writes scored report. Interpretive judgment (not just schema validation).

- **Invariant:** Dimension-scoring discipline; evidence-linked judgment; distinct from mechanical audits.
- **Breaks if converted:** Scoring judgment reduces to pass/fail counting; interpretive weight lost.
- **Migration path:** None immediate. Re-evaluate alongside EVALUATION orchestrator changes.

---

### B — Convert to skill (individual rationale)

**CONTENT_DIGEST → `skills/content-digest/`**

- **Why B:** Type 2, Haiku-sized, brief-driven, single-folder scope, read-only structured extraction with no engineering judgment. Dispatched by EVALUATION (orchestrator), not ORCHESTRATOR (setup pipeline). Identity is the digest method; no pipeline-stage role to preserve.
- **Invariant:** Read-only, single-deliverable scope, no invention, "semantic matching not deep reasoning."
- **Breaks if moved incorrectly:** As agent, duplicates skill-catalog capability; EVALUATION dispatches ad-hoc. As converted without preserving boundedness, cross-deliverable scanning could creep in.
- **Migration path:** Create `skills/content-digest/` with 8-file read protocol + 7-section output structure. Archive agent. Update `AGENT_EVALUATION.md` subagent dispatch. Remove from AGENTS.md Type 2 table + TASK* wildcard.

**ESTIMATING → `skills/estimate-snapshot/`**

- **Why B:** Type 2, tool-root-only writes, brief-driven estimate snapshot generation. NOT part of ORCHESTRATOR setup pipeline (invoked separately for estimating). Bounded method with parameterized brief (BASIS_OF_ESTIMATE enum).
- **Invariant:** Snapshot immutability; BASIS_OF_ESTIMATE controlled enum; provenance-first; no-invention; confidence rules.
- **Breaks if moved incorrectly:** As agent, duplicates skill capability. As converted without BASIS enum discipline, basis selection becomes ambiguous.
- **Migration path:** Create `skills/estimate-snapshot/` preserving BASIS_OF_ESTIMATE enum discipline. Archive agent. **Rewrite ESTIMATING pipeline references in `AGENT_ORCHESTRATOR.md` (~L318).** Update AGENTS.md.

**PDF2MD_PAGE → `skills/pdf2md-page/`**

- **Why B:** Type 2 spawned-only, OUTPUT_PATH-only writes, per-page bounded VLM conversion. Per user's ruling: own sibling skill (not folded into existing `skills/pdf2md/` which excludes page-fanout).
- **Invariant:** Single-page scope; OUTPUT_PATH-only write discipline; VLM-reasoning contract.
- **Breaks if moved incorrectly:** Without parent orchestrator dispatch rewrite, PDF2MD can't spawn pages; page fanout breaks.
- **Migration path:** Create `skills/pdf2md-page/`. Archive agent. **Rewrite `AGENT_PDF2MD.md` dispatch (~L8,93) from "spawn PDF2MD_PAGE sub-agents" to "spawn TASK with TaskSkill: pdf2md-page per page".** Update AGENTS.md.

**DRAWING_EXTRACT_PAGE → `skills/drawing-extract-page/`**

- **Why B:** Same pattern as PDF2MD_PAGE. Type 2 spawned-only, bounded per-page extraction. Per user's ruling: own sibling skill.
- **Invariant:** Single-page scope; OUTPUT_PATH-only writes; crop-first multiblock extraction contract.
- **Breaks if moved incorrectly:** Without parent orchestrator dispatch rewrite, DRAWING_EXTRACT can't spawn pages.
- **Migration path:** Create `skills/drawing-extract-page/`. Archive agent. **Rewrite `AGENT_DRAWING_EXTRACT.md` dispatch (~L8,116).** Update AGENTS.md.

**ESTIMATE_PREP → `skills/estimate-prep/`** (Slice 2a ruling: B1 — one skill with PHASE parameter)

- **Why B:** Type 2, `BLOCKING: never`, brief-driven, straight-through. "May propose, but MUST NOT decide" — no authority surface. Uses LLM reasoning (market benchmarks, parametric defaults) + invokes scaffolding tools + integrates multiple data sources. Human gate is BETWEEN phases (external to each run), not inside a run: "A single run MUST NOT span both phases." Each phase is a separate straight-through TASK invocation — fits the skill model.
- **Invariant:** Write quarantine to `_EstimatePrep/`; snapshots immutable; phase separation (SCAFFOLD vs BOE distinct invocations); parametric-defaults-are-not-human-confirmation; provenance mandatory (Basis + Confidence); no silent overrides; conflicts surfaced not resolved.
- **Breaks if moved incorrectly:** As two skills (B2), common setup duplicates; harder to enforce shared invariants. As agent, duplicates skill capability + adds indirection.
- **Migration path:** Create `skills/estimate-prep/` with `PHASE=SCAFFOLD|BOE` brief parameter. Preserve both phase protocols + schema annex. Archive agent. **Rewrite ESTIMATE_PREP dispatch references in parent files (e.g., invocations in ORCHESTRATOR/RECONCILIATION — to be inventoried in Slice 3b).** Update AGENTS.md.

---

### C — Keep as agent, invoke skill (individual rationale)

**DEPENDENCIES → `skills/dependency-extract/`** (portal: EVALUATIVE/APPLYING)

- **Why C:** Bounded extraction method on its own terms — favors B. But matrix-cell identity (EVALUATIVE/APPLYING) is load-bearing, and DEPENDENCIES is an ORCHESTRATOR subagent for dependency registers per deliverable. Pipeline coherence bias applies: preserve portal identity; extract method to skill.
- **Invariant:** Anchor × Execution edge typing; Dependencies.csv v3.1 schema discipline; deliverable-local scope; evidence-first provenance; enum normalization.
- **Breaks if moved to B without portal-cell update:** Matrix cell loses named role; ORCHESTRATOR dispatch pattern changes unilaterally.
- **Migration path (staged C):** Create `skills/dependency-extract/` with full v3.1 extraction method. Reduce `AGENT_DEPENDENCIES.md` to thin wrapper dispatching TASK+skill. Preserve `AGENTS.md` EVALUATIVE/APPLYING cell. Future B promotion deferred.

**CHIRALITY_FRAMEWORK → `skills/semantic-matrix-build/`**

- **Why C:** Preserves pipeline-stage identity (ORCHESTRATOR Phase 2.3 spawns CHIRALITY_FRAMEWORK). Method is bounded (matrix algebra A,B → C,F,D,K,G,X,T,E) and extractable, but pipeline-stage dispatch is load-bearing.
- **Invariant:** "Show all work" (operation display); "no particulars" (types not instances); semantic-algebra discipline; lens-not-authority separation; deliverable-bound perspective.
- **Breaks if moved to B without pipeline-unit migration:** Phase 2.3 dispatch diverges from Phase 2.4 (CHIRALITY_LENS); mixed pipeline architecture; 4_DOCUMENTS Pass 3 dependency chain inconsistent.
- **Migration path (staged C):** Create `skills/semantic-matrix-build/` with full matrix-algebra PROTOCOL. Reduce agent to thin wrapper. No change to ORCHESTRATOR dispatch or AGENTS.md wildcard.

**CHIRALITY_LENS → `skills/lens-register/`**

- **Why C:** Preserves pipeline-stage identity (ORCHESTRATOR Phase 2.4 spawns CHIRALITY_LENS to generate `_SEMANTIC_LENSING.md`; 4_DOCUMENTS Pass 3 consumes it). Method is bounded (matrix-cell lensing over production documents) but pipeline-stage dispatch is load-bearing. Distinct from `skills/semantic-lensing/` (interactive proposals) — two-contract family.
- **Invariant:** Matrix coverage complete (every cell accounted for); no-invention; provenance mandatory; conflicts surfaced not resolved; register-output discipline.
- **Breaks if moved to B without pipeline-unit migration:** Phase 2.4 dispatch breaks; 4_DOCUMENTS Pass 3 input chain breaks.
- **Migration path (staged C):** See `plans/CHIRALITY_LENS_MIGRATION.md` for full slice detail.

**4_DOCUMENTS → `skills/four-documents/`**

- **Why C:** Pipeline-stage agent (ORCHESTRATOR Phases 2.2 Pass 1/2 + 2.5 Pass 3). 3-pass enrichment method is recurring and extractable. Pipeline coherence bias preserves agent identity.
- **Invariant:** Four-document kit discipline (Datasheet/Specification/Guidance/Procedure); Pass 1/2/3 progression; deliverable-local scope; no cross-deliverable editing.
- **Breaks if moved to B without pipeline-unit migration:** ORCHESTRATOR Phases 2.2 + 2.5 dispatch break; Pass 3 dependency on `_SEMANTIC_LENSING.md` chain breaks.
- **Migration path (staged C):** Create `skills/four-documents/` (one skill with pass modes OR three pass-specific skills — ruling deferred to Slice 4). Reduce agent to thin wrapper. Preserve ORCHESTRATOR dispatch.

**DOMAIN_DOCUMENTS → `skills/domain-documents/`**

- **Why C:** DOMAIN analog of 4_DOCUMENTS. Pipeline-stage agent (ORCHESTRATOR setup for DOMAIN variants). Variable KA drafting method driven by decomposition Knowledge Subjects.
- **Invariant:** Knowledge Type schema discipline; variable artifact set; KA-* file naming; Knowledge-Subject-to-Artifact mapping.
- **Breaks if moved to B without pipeline-unit migration:** DOMAIN setup pipeline breaks.
- **Migration path (staged C):** Create `skills/domain-documents/`. Reduce agent to thin wrapper.

**DELIVERABLE_TASK — C (existing, gold-standard)**

Already implements the C pattern: invokes `skills/proposal-format/` and `skills/semantic-lensing/` via TaskSkill. No change required.

---

### D — Keep as agent, invoke tool(s) (individual rationale)

**PREPARATION**

- **Why D:** Already tool-orchestrating — invokes 7 scaffolding tools (`scaffold_package.sh`, `scaffold_deliverable.sh`, `scaffold_tool_root.sh`, `write_status.sh`, `validate_id_format.sh`, `check_min_viable_fileset.sh`, and task-variant helpers). Narrow LLM seam remains for `_CONTEXT.md` metadata extraction from decomposition document.
- **Invariant:** Idempotent scaffolding; minimum viable fileset; structural-only (no content drafting); source-faithful `_CONTEXT.md`.
- **Breaks if converted:** Tool invocations become LLM reasoning — violates LLM Boundary; idempotency guarantees weaken.
- **Migration path:** None immediate — agent already compliant. Future micro-skill candidate for `_CONTEXT.md` population from decomposition (low priority).

**AUDIT_DEP_CLOSURE**

- **Why D:** Runs `analyze_dep_closure.py` and interprets output. Tool-first orchestration pattern. Interpretation is bounded (closure analysis, orphan/cycle/hub detection from CSV reports).
- **Invariant:** Tool-first execution; deterministic closure analysis; bounded interpretation of tool outputs.
- **Breaks if converted:** Graph-analysis tool becomes LLM reasoning — wasteful and error-prone.
- **Migration path:** None immediate. Slice 5 adds explicit tool-invocation reference to PROTOCOL (additive-only). Future candidate for skill wrapper if the tool-sequence pattern consolidates further.

**AUDIT_HYPERGRAPH_CLOSURE**

Same pattern as AUDIT_DEP_CLOSURE — deterministic closure analysis with preserved script + bounded interpretation.

**EVALUATION_STRUCTURE_AUDIT**

- **Why D:** Haiku-sized, deterministic file-existence + lifecycle enum checks. Runs `find`/`ls`/`grep` + existing validation tools (`count_deliverable_files.sh`, `extract_lifecycle_states.sh`, `validate_enum.py`, etc.). Report compilation is mechanical.
- **Invariant:** Read-only, exhaustive (every deliverable checked), deterministic.
- **Breaks if converted:** Tool orchestration flattens into LLM reasoning; determinism lost.
- **Migration path:** Slice 5 adds explicit tool references to PROTOCOL. Future tool extraction candidate: report-assembly helper.

**EVALUATION_DEPENDENCY_AUDIT**

- **Why D:** Same pattern as EVALUATION_STRUCTURE_AUDIT. Haiku; runs `validate_dependencies_schema.py`, `check_implements_node.sh`, `check_evidence_coverage.sh`, `validate_enum.py`, `analyze_dep_closure.py`.
- **Invariant:** Read-only, exhaustive, schema-aware, deterministic.
- **Breaks if converted:** As above.
- **Migration path:** Slice 5 + future report-assembly tool extraction.

**DOMAIN_HYPERGRAPH** (Slice 2a ruling: Option D — decomposed with new tool)

- **Why D:** PROTOCOL splits at "after interpretation, structured data is processed deterministically." Steps 0-3 (scope resolution, folder/context/scoping interpretation, ledger schema tolerance) use LLM for fuzzy parsing with documented fallback rules. Steps 4-8 (nodes table construction, SHA1 hyperedge ID generation, incidence, referential integrity checks, delta computation, snapshot publish) are deterministic algorithms — the RATIONALE literally says "Determinism and immutable snapshots preserve trust: a run is a reproducible measurement."
- **Per user ruling:** Deterministic tools limited strictly to clear deterministic uses; default to LLM if uncertain. Steps 4-8 clearly qualify; Steps 0-3 remain LLM.
- **Invariant:** Read-only on Category/KTY folders; evidence-first (SourcePath + SourceRef); no invention; deterministic IDs; immutable snapshots; variant discipline.
- **Breaks if moved incorrectly:** As agent-only (A), deterministic hashing/CSV construction remains in LLM reasoning — wasteful and error-prone, violates user's "strict deterministic" guidance. As pure tool (B or fully deterministic), interpretation of variable `_CONTEXT.md` / `Scoping.md` formats + schema-tolerant ledger parsing becomes brittle.
- **Migration path:** Create `tools/aggregation/build_hypergraph.py` that accepts staging CSVs (categories, knowledge_types, subject_artifact_mapping, ledger_rows) + config and produces the full snapshot (nodes.csv, hyperedges.csv, incidence.csv, hypergraph.json, QA_Report.md). Refactor AGENT_DOMAIN_HYPERGRAPH Steps 4-8 to invoke the tool. Register the tool in `tools/REGISTRY.md`. **This is more than an additive-only Slice 5 D-pattern note — it's a non-trivial agent refactor.** See Execution Plan scope update.

---

### E — Archive (individual rationale)

**EQUIPMENT_EXTRACT**

- **Why E:** Orphaned (zero external references; not listed in AGENTS.md). 1:1 superseded by `skills/equipment-extract/` — the skill's method matches the agent's PROTOCOL step-for-step.
- **Invariant satisfied by skill:** Read-only on KTY folders; no invention; exact tags; complete coverage.
- **Breaks if kept:** Dead instruction file; confusion between agent and skill method ownership.
- **Migration path:** `git mv agents/AGENT_EQUIPMENT_EXTRACT.md .Archive/`.

**TASK_ESTIMATING_TEMPLATE.md**

- **Why E:** Stale brief-authoring template. References non-existent `AGENT_ESTIMATING_GENERIC.md`. Superseded by TASK shell's `INIT-TASK` brief schema.
- **Breaks if kept:** Dead references mislead operators; template is unused.
- **Migration path:** Confirm unused via grep + user ruling. `git mv .../TASK_ESTIMATING_TEMPLATE.md .Archive/`.

---

### F — Resolved (Slice 2a)

Both former F-cases resolved per user rulings on 2026-04-04. See B (ESTIMATE_PREP) and D (DOMAIN_HYPERGRAPH) sections above for final justifications.

- **DOMAIN_HYPERGRAPH → D:** Extract Steps 4-8 as `tools/aggregation/build_hypergraph.py`; preserve LLM interpretation in Steps 0-3. Consistent with ruling "deterministic tools limited strictly to clear deterministic uses; default to LLM if uncertain."
- **ESTIMATE_PREP → B:** One skill `skills/estimate-prep/` with `PHASE=SCAFFOLD|BOE` parameter. Human gate is between runs (external), not inside a run — consistent with skill model.

---

## Non-agent file relocations (Slice 1b)

### AUDIT_AGENT.md (rubric worksheet)

**Current state:** `agents/AUDIT_AGENT.md`. Not an agent (no `AGENT_TYPE:` header, no `[[DOC:AGENT_INSTRUCTIONS]]` marker). Used as `RUBRIC_FILE` input by AGENT_AUDIT_AGENTS.

**Relocation candidate:** `docs/rubrics/AUDIT_AGENT.md`.

**Required cross-reference update:** `agents/AGENT_AUDIT_AGENTS.md` RUBRIC_FILE input description (line ~89).

**Slice 1b ruling required.**

### MEMORY_TEMPLATE.md (artifact template)

**Current state:** `agents/MEMORY_TEMPLATE.md`. Not an agent (lacks AGENT_TYPE header). Used by PREPARATION + DELIVERABLE_TASK as `_MEMORY.md` / `MEMORY.md` template schema.

**Relocation candidate:** `docs/templates/MEMORY_TEMPLATE.md`.

**Required cross-reference update:** `agents/AGENT_PREPARATION.md` MEMORY_TEMPLATE reference (line ~478); `agents/AGENT_DELIVERABLE_TASK.md` MEMORY sections if applicable.

**Slice 1b ruling required.**

---

## Change Log

- **2026-04-04:** Initial ruled classification. 46 of 48 ruled; 2 provisional (DOMAIN_HYPERGRAPH, ESTIMATE_PREP).
- **2026-04-04:** Slice 2a F-case resolutions. DOMAIN_HYPERGRAPH → D (decomposed with new `tools/aggregation/build_hypergraph.py`); ESTIMATE_PREP → B (one skill with `PHASE=SCAFFOLD|BOE` parameter). 48/48 ruled; 0 provisional. Category tally updated: B 4→5, D 5→6, F 2→0.
