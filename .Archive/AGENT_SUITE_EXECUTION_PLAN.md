# Agent Suite Execution Plan

## Scope

Slice mechanics for the 6-slice migration program. Defines sequencing, file ownership, parallelization scopes, serial integration stages, and verification steps.

Companion artifacts:
- `plans/AGENT_SUITE_CLASSIFICATION.md` — ruled classifications (what to do per agent)
- `plans/SEMANTIC_PIPELINE_ARCHITECTURE.md` — target model + rationale
- `plans/CHIRALITY_LENS_MIGRATION.md` — Slice 4 detail for CHIRALITY_LENS

---

## Orchestration model

Execution is run by **ONE controlling agent** (main-thread human + Claude) that owns:
- Critical path sequencing.
- All shared-file integration.
- Slice-level human checkpoints.

Subagents are used only for **disjoint work with non-overlapping write sets**. Because lock formalization is unresolved (`docs/PLAN.md:161`), explicit file ownership is required and adversarial overlap is forbidden.

### Shared files (orchestrator-owned; serial edits only)

| File | Touched by slices |
|---|---|
| `AGENTS.md` | 3b, 4b, 6 |
| `docs/PLAN.md` | 5 (roadmap entry) + 6 (status update) |
| `docs/REPO_INVENTORY.md` | 6 (after counts change) |
| `agents/AGENT_ORCHESTRATOR.md` | 2b ✓, 3b (ESTIMATING), 4b (C-pattern notes) |
| `agents/AGENT_TASK.md` | (reserved — unlikely to change in this program) |
| `agents/AGENT_EVALUATION.md` | 3b (CONTENT_DIGEST subagent refs) |
| `agents/AGENT_DELIVERABLE_TASK.md` | 4b (CHIRALITY_LENS family cross-reference) |
| `agents/AGENT_PDF2MD.md` | 3b (per-page dispatch rewrite) |
| `agents/AGENT_DRAWING_EXTRACT.md` | 3b (per-page dispatch rewrite) |
| `skills/semantic-lensing/SKILL.md` | 4b (cross-reference to lens-register) |
| `tools/REGISTRY.md` | 5b (new tool entry) + 6 (reconciliation) |
| `tools/EXTERNAL_TOOLS.md` | 2b ✓ (DOMAIN pipeline simplified) |
| `agents/AGENT_DOMAIN_DOCUMENTS.md` | 2b ✓ (pipeline chain + lifecycle) |

**Rule:** only the orchestrator edits these files. No concurrent subagent edits.

### Parallelizable scopes

| Scope | Granularity | Example |
|---|---|---|
| Read-only classification validation | Agent cluster | Review DECOMP*/PREP*/TASK*/AUDIT*/adjunct independently |
| Skill contract creation | `skills/<name>/` folder | One worker per new skill |
| Tool extraction | `tools/<category>/` | One worker per new tool |
| Agent wrapper rewrite (C-pattern) | One `AGENT_*.md` file | One worker per Type 2 wrapper |
| D-pattern additive notes | One `AGENT_*.md` file | One worker per audit agent |

**Rule:** each subagent receives explicit write paths; paths cannot overlap between concurrent subagents.

---

## Slice sequencing

```
Slice 1 ✓ (archives + non-agent relocations)
    ↓
Slice 2 ✓ (F-case rulings + ORCHESTRATOR contradiction fix)
    ↓
Slice 3 (B-conversions: 5 skills + shared-file dispatch updates)
    ↓
Slice 4 (C-pattern extractions for semantic pipeline + DEPENDENCIES)
    ↓       ↘
Slice 5a ← (parallel with 4 possible — independent; additive-only)
    ↓
Slice 5b (DOMAIN_HYPERGRAPH-D refactor: new tool + PROTOCOL rewrite)
    ↓
Slice 6 (shared-file reconciliation + inventory update)
```

Slice 5a (D-pattern additive notes on 4 audit agents) is independent and may run concurrently with Slice 4. Slice 5b (DOMAIN_HYPERGRAPH refactor) is a substantive non-additive agent rewrite + new tool creation; sequenced after Slice 5a for clarity but no hard dependency.

---

## Slice 1 — Archives + non-agent relocations ✓ COMPLETE

### Slice 1a: Archive EQUIPMENT_EXTRACT + TASK_ESTIMATING_TEMPLATE ✓

**Executed 2026-04-04.** Both files archived via `git mv` to `.Archive/`. Grep verified no live runtime references outside planning artifacts + historical snapshots.

### Slice 1b: Relocate AUDIT_AGENT.md + MEMORY_TEMPLATE.md ✓

**Executed 2026-04-04.** Rulings: `docs/rubrics/AUDIT_AGENT.md` + `docs/templates/MEMORY_TEMPLATE.md` (new directories created).

Cross-references updated:
- `agents/AGENT_AUDIT_AGENTS.md` — 5 references updated to `docs/rubrics/AUDIT_AGENT.md`
- `agents/AGENT_PREPARATION.md:478` — updated to `docs/templates/MEMORY_TEMPLATE.md`
- `docs/DBM_Agent_Instruction_Architecture.md:114` — metadata note rewritten to reflect new locations
- `agents/AGENT_DELIVERABLE_TASK.md` — verified no references (none required)

Historical audit snapshots in `examples/AB-2026-01424-*/AUDIT_NEW_AGENTS_2026-03-29_1930/` preserved unchanged (immutable records).

---

## Slice 2 — F-case rulings + ORCHESTRATOR contradiction fix ✓ COMPLETE

### Slice 2a: Rule F-cases (DOMAIN_HYPERGRAPH, ESTIMATE_PREP) ✓

**Executed 2026-04-04.** Rulings recorded in `plans/AGENT_SUITE_CLASSIFICATION.md`:

- **DOMAIN_HYPERGRAPH → D.** Extract PROTOCOL Steps 4-8 (SHA1 hashing, CSV construction, referential integrity, delta computation, snapshot publish) as new deterministic tool `tools/aggregation/build_hypergraph.py`. Steps 0-3 (scope resolution, folder/context/scoping interpretation, ledger schema tolerance) remain LLM. Consistent with user's ruling: "deterministic tools limited strictly to clear deterministic uses; default to LLM if uncertain." Non-additive refactor → **Slice 5b**.
- **ESTIMATE_PREP → B.** One skill `skills/estimate-prep/` with `PHASE=SCAFFOLD|BOE` brief parameter (B1 form). Human gate is between runs (external to each phase), not inside a run — fits the skill model. Expanded to **Slice 3a** (5th skill).

Status: 48/48 ruled; 0 provisional. Category tally updated: B 4→5, D 5→6, F 2→0.

### Slice 2b: Fix ORCHESTRATOR DOMAIN contradiction ✓

**Executed 2026-04-04.** Ruling: **Direction (b) — DOMAIN skips CHIRALITY_LENS.**

Edits applied:
- `agents/AGENT_ORCHESTRATOR.md` L264 (Precondition) + L268 (dependency chain): rewritten to reflect DOMAIN completes in Phase 2.2 (DOMAIN_DOCUMENTS `RUN_PASSES=FULL`), not Phase 2.5.
- `agents/AGENT_DOMAIN_DOCUMENTS.md` L31 (pipeline chain): removed `CHIRALITY_FRAMEWORK → CHIRALITY_LENS` from DOMAIN chain.
- `agents/AGENT_DOMAIN_DOCUMENTS.md` L34 (lifecycle): removed SEMANTIC_READY state from DOMAIN lifecycle expectation.
- `agents/AGENT_DOMAIN_DOCUMENTS.md` L63 (ALLOW_OVERWRITE_STATES default): removed SEMANTIC_READY for consistency.
- `tools/EXTERNAL_TOOLS.md` L60-99: DOMAIN pipeline diagram + table simplified to linear 5-step flow (Steps 4-5 semantic pipeline removed).

CHIRALITY_LENS DOMAIN variant sections deferred to Slice 4 (C-migration) per user ruling — avoids touching the file twice.

### Verification (Slice 2) ✓

- `plans/AGENT_SUITE_CLASSIFICATION.md` shows 48/48 ruled; F section marked resolved.
- ORCHESTRATOR Phase 2.4, Phase 2.5, Phase 2.6 DOMAIN handling consistent across all references.
- DOMAIN_DOCUMENTS pipeline chain + lifecycle + overwrite-states all aligned.
- EXTERNAL_TOOLS DOMAIN pipeline diagram + table renumbered and simplified.

---

## Slice 3 — B-conversions + shared-file dispatch updates

### Slice 3a: B-conversions (parallel — 5 disjoint skill folders)

**Purpose:** Extract bounded methods to skills; archive source agents.

**Parallel workers (5, disjoint skill folders):**

| Worker | Creates | Archives | Invariants to preserve |
|---|---|---|---|
| 1 | `skills/content-digest/` | `agents/AGENT_CONTENT_DIGEST.md` → `.Archive/` | Read-only, single-deliverable, no invention, 7-section output |
| 2 | `skills/estimate-snapshot/` | `agents/AGENT_ESTIMATING.md` → `.Archive/` | BASIS_OF_ESTIMATE enum, snapshot immutability, provenance-first |
| 3 | `skills/pdf2md-page/` | `agents/AGENT_PDF2MD_PAGE.md` → `.Archive/` | Single-page scope, OUTPUT_PATH-only writes, VLM-reasoning contract |
| 4 | `skills/drawing-extract-page/` | `agents/AGENT_DRAWING_EXTRACT_PAGE.md` → `.Archive/` | Single-page scope, OUTPUT_PATH-only writes, crop-first multiblock extraction |
| 5 | `skills/estimate-prep/` (PHASE=SCAFFOLD\|BOE) | `agents/AGENT_ESTIMATE_PREP.md` → `.Archive/` | Write quarantine to `_EstimatePrep/`; snapshot immutability; phase separation (SCAFFOLD vs BOE distinct invocations); provenance mandatory; parametric-defaults-not-human-confirmation; no silent overrides |

Each skill includes `SKILL.md` + `BRIEF_SCHEMA.md` + `QA_CHECKS.md`. Validator run after each.

**Human checkpoint:** Approve each skill contract before workers proceed.

### Slice 3b: Serial shared-file updates (orchestrator-owned)

**Purpose:** Rewrite dispatch patterns in parent agents; update indexes.

**Serial actions (orchestrator):**

| File | Change | Reason |
|---|---|---|
| `agents/AGENT_EVALUATION.md` | Update `subagents:` frontmatter (remove CONTENT_DIGEST) + PROTOCOL Step 2 dispatch text | CONTENT_DIGEST now dispatched as TASK+skill |
| `agents/AGENT_ORCHESTRATOR.md` | Rewrite ESTIMATING pipeline references (~L318) | ESTIMATING now dispatched as TASK+skill |
| `agents/AGENT_PDF2MD.md` | Rewrite per-page dispatch (~L8, L93) from "spawn PDF2MD_PAGE sub-agents" to "spawn TASK with TaskSkill: pdf2md-page per page" | PDF2MD_PAGE no longer exists as agent |
| `agents/AGENT_DRAWING_EXTRACT.md` | Rewrite per-page dispatch (~L8, L116) similarly | DRAWING_EXTRACT_PAGE no longer exists as agent |
| ESTIMATE_PREP dispatch sites | Inventory invocation sites: AGENTS.md PREP* wildcard (L27) + Type 2 table (L81); frontend UI refs (`frontend/components/PipelineView.tsx`, `frontend/app/page.tsx` — verify if PREP* button dispatches agent directly). Replace agent-name dispatch with TASK+skill (`skills/estimate-prep/` with `PHASE` parameter). | ESTIMATE_PREP now dispatched as TASK+skill |
| `AGENTS.md` | Remove 5 archived agents from Type 2 table; update PREP*, TASK*, PDF2MD*, DRAWING_EXTRACT* wildcards (remove CONTENT_DIGEST, ESTIMATING, PDF2MD_PAGE, DRAWING_EXTRACT_PAGE, ESTIMATE_PREP) | Reflect archived state |

**Human checkpoint:** Approve each dispatch rewrite; confirm archive moves applied.

### Verification (Slice 3)

- `python3 tools/validation/validate_skill_metadata.py skills` passes.
- 5 new skills exist under `skills/<name>/` with required files.
- 5 archived agent files in `.Archive/`, byte-identical to pre-move.
- Grep for archived agent names: only `.Archive/` + historical docs + (possibly) AGENTS.md historical rows.
- EVALUATION subagent references, ORCHESTRATOR ESTIMATING refs, PDF2MD/DRAWING_EXTRACT dispatch sections, ESTIMATE_PREP invocation sites all reference skills, not archived agents.

---

## Slice 4 — C-pattern extractions (semantic pipeline + DEPENDENCIES)

### Slice 4a: Parallel C-pattern work (5 skills + 5 wrappers = 10 disjoint write sets)

**Purpose:** Extract methods to skills; rewrite agents as thin dispatch shims (non-additive allowed).

**Parallel workers (skill creation + wrapper rewrites):**

| Worker pair | Creates skill | Rewrites wrapper | Invariants |
|---|---|---|---|
| 1a/1b | `skills/semantic-matrix-build/` | `agents/AGENT_CHIRALITY_FRAMEWORK.md` | Show all work; no particulars; semantic-algebra discipline; lens-not-authority separation |
| 2a/2b | `skills/lens-register/` | `agents/AGENT_CHIRALITY_LENS.md` | Matrix coverage complete; no invention; provenance mandatory; conflicts surfaced |
| 3a/3b | `skills/four-documents/` (pass modes TBD) | `agents/AGENT_4_DOCUMENTS.md` | Four-doc kit discipline; Pass 1/2/3 progression; deliverable-local |
| 4a/4b | `skills/domain-documents/` | `agents/AGENT_DOMAIN_DOCUMENTS.md` | Knowledge Type schema; variable artifact set; KA-* naming |
| 5a/5b | `skills/dependency-extract/` | `agents/AGENT_DEPENDENCIES.md` | Anchor × Execution edge typing; Dependencies.csv v3.1; evidence-first; enum normalization |

**Wrapper rewrite pattern (non-additive):**
- Header (AGENT_TYPE, AGENT_CLASS, WRITE_SCOPE, BLOCKING, etc.) preserved byte-identical.
- PROTOCOL body replaced with TASK+skill dispatch + skill reference.
- RATIONALE notes extraction to skill.
- Original PROTOCOL inline prose may be deleted (skill is the authority).

**Human checkpoint:** Approve each skill contract + each wrapper rewrite.

### Slice 4b: Serial shared-file updates (orchestrator-owned)

**Purpose:** Apply cross-references to shared files; semantic-lensing skill cross-ref.

**Serial actions:**

| File | Change |
|---|---|
| `agents/AGENT_ORCHESTRATOR.md` | Update Phase 2.3/2.4/2.2/2.5 text noting wrappers internally dispatch TASK+skill (documentation only; dispatch chain unchanged) |
| `agents/AGENT_DELIVERABLE_TASK.md` | Add CHIRALITY_LENS family cross-reference at line ~225 (note lens-register is setup-time counterpart) |
| `skills/semantic-lensing/SKILL.md` | Add cross-reference note: lens-register produces the register this skill consumes as worklist |
| `AGENTS.md` | TASK* wildcard preserved in staged end state (no removal of CHIRALITY_FRAMEWORK, CHIRALITY_LENS, 4_DOCUMENTS, DOMAIN_DOCUMENTS, DEPENDENCIES) |

**Human checkpoint:** Approve cross-references.

### Verification (Slice 4)

- 5 new skills under `skills/<name>/`; validator passes.
- 5 wrapper agents rewritten to thin dispatch shims; header invariants preserved.
- Cross-references in DELIVERABLE_TASK + semantic-lensing/SKILL.md point to lens-register.
- ORCHESTRATOR Phase 2.2/2.3/2.4/2.5 still reference wrapper agents (staged end state).
- AGENTS.md TASK* wildcard unchanged.

---

## Slice 5 — D-pattern work

### Slice 5a: D-pattern tool-invocation notes (4 audits, additive-only)

#### Purpose

Add explicit tool-invocation references to PROTOCOL sections of 4 audit agents. **Additive-only** edits.

#### Parallel workers (4 independent agents)

| Worker | Agent | Add tool-invocation notes for |
|---|---|---|
| 1 | `agents/AGENT_AUDIT_DEP_CLOSURE.md` | `analyze_dep_closure.py` + closure report consumption |
| 2 | `agents/AGENT_AUDIT_HYPERGRAPH_CLOSURE.md` | analogous hypergraph closure tools |
| 3 | `agents/AGENT_EVALUATION_STRUCTURE_AUDIT.md` | `count_deliverable_files.sh`, `extract_lifecycle_states.sh`, `validate_enum.py`, `count_workspace_state.sh` |
| 4 | `agents/AGENT_EVALUATION_DEPENDENCY_AUDIT.md` | `validate_dependencies_schema.py`, `check_implements_node.sh`, `check_evidence_coverage.sh`, `validate_enum.py`, `analyze_dep_closure.py` |

PREPARATION already compliant — no Slice 5a work.

#### Edit discipline

**Strictly additive.** Diff may only:
- Add explicit tool references to PROTOCOL steps.
- Add `> Tool invocation:` notes.
- Add tool registry links.

Diff may NOT:
- Delete existing PROTOCOL content.
- Rewrite method prose.
- Change header invariants.

**Human checkpoint:** Confirm additive-only diffs.

#### Verification (Slice 5a)

- Diff of each modified agent: only additive references; no content deletions.
- Header invariants byte-identical.

#### Slice 5a closure — tool path canonicalization

**Executed 2026-04-04.** While dispatching workers, discovered a concentrated prose-vs-filesystem drift in the evaluation instruction family: four audit PROTOCOL steps referenced `tools/query/{count_deliverable_files,extract_lifecycle_states,check_implements_node,check_evidence_coverage}.sh` — but those tools actually live at `tools/evaluation/...`. Workers adhered to additive-only discipline by adding canonical-path sidenotes alongside the stale prose. Reviewer flagged this produced contradictory paths in the same PROTOCOL step.

Corrections applied as Slice 5a closure (path rewrites ARE additive-discipline-compliant since tool paths are not method content):

| File | Change |
|---|---|
| `agents/AGENT_EVALUATION_STRUCTURE_AUDIT.md` | Rewrote 2 stale `tools/query/...` refs (Steps 2, 3) to canonical `tools/evaluation/...`; removed 4 now-redundant worker sidenotes |
| `agents/AGENT_EVALUATION_DEPENDENCY_AUDIT.md` | Rewrote 2 stale `tools/query/...` refs (Steps 3, 4) to canonical `tools/evaluation/...`; removed 2 now-redundant worker sidenotes; fixed `validate_id_format.sh {id_value}` → `{ID_TYPE} {ID_VALUE}` signature bug (Step 5) |
| `agents/AGENT_EVALUATION_REPORT.md` | Rewrote 2 stale `tools/query/...` refs (Step 2) — not in original Slice 5a scope but same drift |

**Explicit non-scope** (preserved as-is — legitimate query-tool paths):
- `tools/query/count_workspace_state.sh`
- `tools/query/scan_next_amendment_id.sh`

**Verification:**
- `rg 'tools/query/(count_deliverable_files|extract_lifecycle_states|check_implements_node|check_evidence_coverage)\.sh' agents` → 0 matches
- `rg 'validate_id_format\.sh \{id_value\}' agents` → 0 matches
- Legitimate query-tool references preserved (7 occurrences across ORCHESTRATOR, EVALUATION, STRUCTURE_AUDIT, REPORT, SCOPE_CHANGE, HYPERGRAPH_CLOSURE).

---

### Slice 5b: DOMAIN_HYPERGRAPH-D refactor (non-additive)

#### Purpose

Per Slice 2a ruling (DOMAIN_HYPERGRAPH → D): extract PROTOCOL Steps 4-8 into a new deterministic tool; rewrite agent to invoke the tool for deterministic work while preserving LLM interpretation in Steps 0-3. This is **not additive-only** — PROTOCOL Steps 4-8 get substantively rewritten as tool-invocation blocks.

#### Actions (serial within slice; touches disjoint files)

1. **Formalize staging CSV schemas** — tool inputs in `{snapshot}/Evidence/` directly (no `_staging/` subfolder; existing Evidence files get strict column contracts):

   | File | Status | Purpose | Columns |
   |---|---|---|---|
   | `discovered_categories.csv` | **required** | CATEGORY nodes | CategoryID, CategoryName, SourcePath, SourceRef, Notes |
   | `discovered_knowledge_types.csv` | **required** | KNOWLEDGE_TYPE nodes + IN_CATEGORY edges | KnowledgeTypeID, Name, CategoryID, Discipline, Type, Responsible, Description, AnticipatedArtifacts (informational only — **not** used for artifact construction), DecompositionRef, SourcePath, SourceRef, Notes |
   | `discovered_knowledge_subjects.csv` | conditional | KNOWLEDGE_SUBJECT nodes + HAS_SUBJECT edges | SubjectID, SubjectName, KnowledgeTypeID, SourcePath, SourceRef, Notes |
   | `artifact_enumeration.csv` | conditional | KNOWLEDGE_ARTIFACT nodes + HAS_ARTIFACT edges | ArtifactID, ArtifactLabel, KnowledgeTypeID, Filename, ArtifactSource (SCOPING_PLAN\|ANTICIPATED\|PRESENT), SourcePath, SourceRef, Notes |
   | `subject_artifact_mapping.csv` | conditional | SUBJECT_MATERIALIZED_AS edges | SubjectID, ArtifactID, KnowledgeTypeID, SourcePath, SourceRef, Notes |
   | `discovered_ledger_rows.csv` | optional | ATOMIC_UNIT nodes + LEDGER_ROW edges | AtomicUnitID, UnitStatement, CategoryID, KnowledgeTypeIDs (semicolon-sep), ObjectiveIDs (semicolon-sep), SourcePath, SourceRef, Notes |
   | `discovered_objectives.csv` | optional | OBJECTIVE nodes | ObjectiveID, Label, SourcePath, SourceRef, Notes |
   | `kty_supports_obj.csv` | optional | KTY_SUPPORTS_OBJ edges (ledger-independent) | KnowledgeTypeID, ObjectiveID, SourcePath, SourceRef, Notes |

   **Tool behavior when a conditional/optional file is absent:** skip the corresponding node type and edge emissions; emit a note in `QA_Report.md`. Required files absent → `FAILED_INPUTS`.

   **List normalization (before edge construction):** for semicolon-separated fields (`KnowledgeTypeIDs`, `ObjectiveIDs`), trim whitespace, dedupe, sort ascending. Ensures determinism independent of source ordering.

2. **Create `tools/aggregation/build_hypergraph.py`** — narrow scope: deterministic graph construction + QA only:
   - **Reads** staging CSVs from `--staging-dir`
   - **Writes** `nodes.csv`, `hyperedges.csv`, `incidence.csv`, `hypergraph.json`, `QA_Report.md` to `--output-dir`
   - Deterministic hyperedge ID generation:
     ```
     canonical = HyperedgeType + "|" + "|".join(sorted(f"{Role}:{NodeID}" for edge incidences)) + "|" + SourcePath + "|" + SourceRef
     HyperedgeID = f"HGE-{HyperedgeType}-{sha1(canonical.encode('utf-8')).hexdigest()[:12]}"
     ```
   - Incidence ordinals computed post-hash from sorted order
   - Referential integrity + schema + category/subject/artifact/ledger integrity + 9 QA checks (from agent Step 6 prose)
   - Optional delta computation when `--prior-snapshot` provided
   - **Explicit non-scope:** does NOT invoke `scaffold_tool_root.sh`, `create_snapshot_folder.sh`, or `update_latest_pointer.sh`. Agent retains orchestration.

3. **Refactor `agents/AGENT_DOMAIN_HYPERGRAPH.md` PROTOCOL:**
   - Steps 0-3: retain LLM interpretation (scope resolution, folder/context/scoping/ledger parsing with schema tolerance); emit the 8 staging CSVs to `{snapshot}/Evidence/` with formalized column contracts.
   - Steps 4-7: replace inline algorithm with tool invocation block. Tool reads Evidence/ + writes final outputs to snapshot root.
   - Step 8: retain scaffolding + pointer-update orchestration; add explicit copy of `tools/aggregation/build_hypergraph.py` to `{snapshot}/build_hypergraph.py` per existing STRUCTURE promise; record tool path + git commit SHA in `Decision_Log.md`.
   - Header invariants (AGENT_TYPE, AGENT_CLASS, WRITE_SCOPE, BLOCKING) preserved byte-identical.
   - SPEC, STRUCTURE, RATIONALE intact.

4. **Register in `tools/REGISTRY.md`** under new `## Aggregation` section with purpose, inputs, outputs, determinism guarantee.

5. **Determinism verification** — tool produces deterministic outputs: same staging inputs → byte-identical CSV files + canonical hypergraph JSON (excluding `generated_at` timestamp). Compare via SHA256 hashes on CSVs + normalized JSON.

**Worker model:** Serial (single worker owns both tool file + agent rewrite + registry entry).
**Human checkpoint:** Approve staging CSV schemas; approve tool spec; approve agent rewrite diff.

#### Edit discipline

**Non-additive allowed** for PROTOCOL Steps 4-8 rewrite (per C-pattern precedent from Slice 4a). Preserve:
- Header invariants byte-identical.
- PROTOCOL Steps 0-3 intact (only LLM interpretation; no changes to those steps).
- SPEC, STRUCTURE, RATIONALE sections intact.

Diff may:
- Replace inline algorithm prose in Steps 4-8 with tool-invocation blocks.
- Add references to `tools/aggregation/build_hypergraph.py` and staging CSV schemas.

#### Verification (Slice 5b)

- `tools/aggregation/build_hypergraph.py` exists, is executable, produces deterministic outputs (same inputs → same outputs verified by hash).
- `tools/REGISTRY.md` contains new entry.
- `agents/AGENT_DOMAIN_HYPERGRAPH.md` header byte-identical to pre-refactor; PROTOCOL Steps 0-3 unchanged; Steps 4-8 reference tool.
- Running DOMAIN_HYPERGRAPH against an example DOMAIN execution root still produces valid snapshot (end-to-end integration test).

---

## Slice 6 — Shared-file reconciliation + inventory ✓ COMPLETE

**Executed 2026-04-04.** Final reconciliation applied:
- `AGENTS.md`: verified — Slice 3b already removed 5 archived B-converted agents; C-wrappers preserved in TASK* wildcard per staged end state; no further edits required.
- `docs/REPO_INVENTORY.md`: updated counts — Indexed agents 44→39, Repo-native skills 5→15, Registered tools 55→50.
- `tools/REGISTRY.md`: verified — new `## Aggregation` section with `build_hypergraph.py` entry (added in Slice 5b).
- `docs/PLAN.md` §5: roadmap entry marked Complete with per-slice outcome summary + deferred items flagged.
- **Grep sweep:** zero live references in `agents/` or `AGENTS.md` to 6 archived agents (EQUIPMENT_EXTRACT, CONTENT_DIGEST, ESTIMATING, PDF2MD_PAGE, DRAWING_EXTRACT_PAGE, ESTIMATE_PREP).
- **Skill validator:** 15/15 PASS.

### Purpose

Final reconciliation: ensure AGENTS.md matches live state, update docs/REPO_INVENTORY.md, update docs/PLAN.md roadmap entry with final status, grep sweep for dangling references.

### Actions (serial, orchestrator)

1. **AGENTS.md reconciliation:**
   - Type 2 table: remove 5 archived B-converted agents (CONTENT_DIGEST, ESTIMATING, PDF2MD_PAGE, DRAWING_EXTRACT_PAGE, ESTIMATE_PREP).
   - PREP* wildcard: remove ESTIMATE_PREP.
   - TASK* wildcard: remove CONTENT_DIGEST, ESTIMATING; preserve CHIRALITY_FRAMEWORK, CHIRALITY_LENS, 4_DOCUMENTS, DOMAIN_DOCUMENTS, DEPENDENCIES (C-wrappers).
   - PDF2MD* wildcard: remove PDF2MD_PAGE.
   - DRAWING_EXTRACT* wildcard: remove DRAWING_EXTRACT_PAGE.
   - AUDIT* wildcard: no changes (D-patterns preserved).
2. **docs/REPO_INVENTORY.md update:**
   - Recount agents (was 48, now 41 live + 7 archived: +ESTIMATE_PREP to archive count after Slice 3a).
   - Update skill count (was 5, now 15: +content-digest, +estimate-snapshot, +pdf2md-page, +drawing-extract-page, +estimate-prep, +semantic-matrix-build, +lens-register, +four-documents, +domain-documents, +dependency-extract).
   - Update tool count (+1: `tools/aggregation/build_hypergraph.py` from Slice 5b).
3. **tools/REGISTRY.md reconciliation:**
   - Verify `build_hypergraph.py` entry added in Slice 5b.
4. **docs/PLAN.md roadmap entry update:**
   - Change status to "Complete" with final rulings.
   - Link to plans/ artifacts.
5. **Grep sweep:**
   - For each archived/converted agent name: confirm only `.Archive/`, historical docs, or AGENTS.md historical rows reference it.
   - Zero live references in live agent instructions.

### Verification (Slice 6)

- AGENTS.md Type 2 table + wildcards reflect live state.
- REPO_INVENTORY.md counts reconciled.
- docs/PLAN.md roadmap entry marked complete.
- `python3 tools/validation/validate_skill_metadata.py skills` passes.
- Grep for archived agent names: zero live references.

---

## Cross-cutting rules

### Edit discipline (scoped by slice/pattern)

| Slice | Pattern | Discipline |
|---|---|---|
| 3a | B-conversion skills | Normal (skill creation from scratch) |
| 3b | Shared-file dispatch updates | Rewrites allowed (ORCHESTRATOR, PDF2MD, DRAWING_EXTRACT dispatch sections; ESTIMATE_PREP dispatch sites) |
| 4a | C-pattern wrappers | **Non-additive rewrites explicitly allowed.** Headers preserved; PROTOCOL replaced with TASK+skill dispatch. |
| 4b | Shared-file cross-references | Additive cross-reference notes |
| 5a | D-pattern tool-invocation notes | **Additive-only.** No PROTOCOL content deletions. |
| 5b | D-pattern agent refactor (DOMAIN_HYPERGRAPH) | **Non-additive rewrites for PROTOCOL Steps 4-8 only.** Headers byte-identical; Steps 0-3 + SPEC + STRUCTURE + RATIONALE intact. |
| All | Portal agent headers | Preserve AGENT_TYPE, AGENT_CLASS, INTERACTION_SURFACE, WRITE_SCOPE, BLOCKING byte-identical unless portal role is explicitly being revised. |

### Validator gate

After each slice touching `skills/`:
```sh
python3 tools/validation/validate_skill_metadata.py skills
```
Must pass before slice closes.

### Cross-reference grep

After each slice, grep for names of any file moved/archived:
- Confirm zero live references outside `.Archive/` + historical docs.
- Any hit outside allowed contexts is a failure signal; stop slice.

### Git hygiene

- Use `git mv` for all relocations (preserve history).
- Never `rm -f` on agent files.
- Each slice produces commits that can be reverted independently.
- Commit messages reference the slice number + slice name.

---

## Verification summary table

| Slice | Key verification |
|---|---|
| 1 ✓ | Archived files byte-identical; zero live references |
| 2 ✓ | All 48 files ruled (no provisional); ORCHESTRATOR DOMAIN consistent |
| 3 | Skill validator passes; 5 new skills exist; 5 agents archived; dispatches rewritten |
| 4 | Skill validator passes; 5 new skills exist; 5 wrappers rewritten; cross-refs in place |
| 5a | Additive-only diffs; header invariants unchanged |
| 5b | `build_hypergraph.py` exists + deterministic; DOMAIN_HYPERGRAPH PROTOCOL Steps 4-8 rewritten; header byte-identical; integration test passes |
| 6 | AGENTS.md matches live state; REPO_INVENTORY reconciled; REGISTRY.md updated; grep sweep clean |

---

## Change Log

- **2026-04-04:** Initial execution plan. 6-slice program with explicit file ownership, parallelization scopes, and verification gates.
- **2026-04-04:** Slice 1 + Slice 2 executed. Slice 2a rulings (DOMAIN_HYPERGRAPH → D, ESTIMATE_PREP → B) caused scope expansions: Slice 3a 4→5 skills (+estimate-prep); Slice 3b added ESTIMATE_PREP dispatch inventory; Slice 5 split into 5a (4 audits, additive-only) and 5b (DOMAIN_HYPERGRAPH-D refactor, non-additive PROTOCOL Steps 4-8 rewrite + new tool `tools/aggregation/build_hypergraph.py`); Slice 6 counts updated.
