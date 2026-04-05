# PLAN — Development Roadmap

This document captures the development roadmap for the Chirality project execution system. It summarizes what has been codified, identifies future hardening candidates, and provides sequencing rationale.

---

## 1. Completed: System Hardening

The working system has been codified into formal governance documents and aligned to the active agent framework.

### Governance Documents Written

| Document | Purpose | Status |
|----------|---------|--------|
| `docs/SPEC.md` | Physical structures, file formats, Dependencies.csv v3.1 schema, folder layout, validation checklist | Complete |
| `docs/TYPES.md` | Domain vocabulary, hierarchy, stable IDs, dependency vocabulary, agent roles, lifecycle states | Complete |
| `docs/DIRECTIVE.md` | Founding intent, design philosophy, professional responsibility model, scope, constraints | Complete |
| `docs/CONTRACT.md` | Invariant catalog (21 K-* invariants), change policy, enforcement map | Complete |
| `docs/PLAN.md` | This document | Complete |

### Governance Alignment

Current governance documents are internally aligned on the core model:
- Hierarchy is flat `package->deliverable` across `docs/TYPES.md`, `docs/SPEC.md`, and `docs/CONTRACT.md`
- Authoritative execution state is file-based (`_STATUS.md`, `_DEPENDENCIES.md`, `Dependencies.csv`)
- Invariant catalog is centralized in `docs/CONTRACT.md`
- Agent role boundaries and write scopes are defined by the active `AGENT_*.md` instruction suite

### Agent Instruction Hardening

| Change | Agents Affected |
|--------|-----------------|
| QA Contract sections added | PREPARATION, 4_DOCUMENTS, CHIRALITY_FRAMEWORK, CHIRALITY_LENS (wrappers since archived — see §6) |
| Output Persistence notes added | ORCHESTRATOR, RECONCILIATION |

Agent instruction consistency: 92% → estimated 95%+ after hardening.

---

## 2. Existing Tooling

### Validation + Example Assets

- `examples/` provides concrete execution-root samples with package/deliverable structures and semantic artifacts (`_SEMANTIC.md`) for regression and conformance testing.
- `frontend/docs/harness/` documents SDK runtime validation and CI integration for harness behavior.
- `frontend/scripts/validate-harness-*.mjs` provides repeatable local and CI validation gates.

### Desktop Frontend (`frontend/`)

Next.js + Electron desktop app with:
- Session/turn API (`/api/harness/session/*`, `/api/harness/turn`)
- Streaming event protocol (SSE)
- Multimodal turn input via server-resolved file attachments (image/document/text)
  - `attachment-resolver.ts` — server-side file reader with classification, budget enforcement, and partial failure handling
  - `FilePicker.tsx` — self-contained file picker modal with multi-select, extension filtering, and directory navigation
  - ChatPanel attachment pipeline — draft preservation with optimistic UI rollback on send failure
- Portal-to-Pipeline navigation with deliverable-scoped `TASK*` variants (`pkg::id` composite keys)
  - Deliverable row click in PORTAL routes to PIPELINE `TASK*` and selects the corresponding deliverable key
  - `TASK*` is deliverables-only (no fallback static variants); selector shows explicit loading and empty states
  - Stale deliverable variant keys are cleared when root changes or deliverable fetch fails
- Shared deliverables state at page-level (`page.tsx`) used by both PORTAL and PIPELINE views
- Live project-directory refresh in `FileTree`
  - Periodic polling plus focus/visibility refresh to pick up external filesystem changes
- Desktop packaging (macOS `.dmg`, Windows `.exe`)
- Harness validation automation
- Operator Toolkit panel for per-turn harness options + local presets
  - Visibility is controlled from `CONFIG` ("Show Tool Kit sidebar") and persisted in local storage
- Resizable multi-pane layout improvements
  - High-visibility drag handles, keyboard resize support, and collapse/expand affordances
- Theme hardening
  - Light mode uses non-orange accent text for readability
  - Assistant and user chat bubbles use role-specific low-contrast surfaces with left/right alignment for quick scanning
  - Assistant messages render GitHub-flavored markdown in-chat, with ANSI fallback for terminal-style tool output
  - Top-banner status noise was removed; update messaging only appears when an update is actually available
  - Header brand tile uses the macOS app icon asset with rounded-square treatment

### Matrix Navigation + Pipeline Taxonomy

> **Note:** This section describes the current desktop UI. After the full-normalization work recorded in §6, the canonical architecture matrix (in `AGENTS.md` and the three-layer HELPS_HUMANS governance) has diverged from the UI — the UI still shows UI labels (`HELP`, `ORCHESTRATE`, `AGENTS`, `DEPENDENCIES`, `RECONCILING`) and the `PREP*`/`TASK*` wildcards, whereas the canonical matrix uses agent role names and collapsed cells (`PREPARATION`, `TASK`, empty `EVALUATIVE × APPLYING`). UI normalization is deferred to a separate frontend slice (see §6 "Deferred").

The desktop UI uses a 3x4 matrix to route operator intent into WORKBENCH or PIPELINE.

- Columns (shared): `GUIDING`, `APPLYING`, `JUDGING`, `REVIEWING`
- Rows:
  - `NORMATIVE` -> opens `WORKBENCH`
  - `OPERATIVE` -> opens `PIPELINE`
  - `EVALUATIVE` -> opens `WORKBENCH`

Matrix cells:

| Row | Guiding | Applying | Judging | Reviewing |
|-----|---------|----------|---------|-----------|
| `NORMATIVE` | `HELP` | `ORCHESTRATE` | `WORKING_ITEMS` | `AGGREGATE` |
| `OPERATIVE` | `DECOMP*` | `PREP*` | `TASK*` | `AUDIT*` |
| `EVALUATIVE` | `AGENTS` | `DEPENDENCIES` | `CHANGE` | `RECONCILING` |

PIPELINE category model:

- `DECOMP*`
- `PREP*`
- `TASK*`
- `AUDIT*`

Option policy:

- Requested but unsupported variants remain visible as disabled entries.
- Disabled entries are intentionally non-selectable and rendered as "coming soon".

`TASK*` selector model:

- Uses split selectors instead of one mixed list:
  - `Task Agent` (static options)
  - `Scope` selectors (dynamic options)
- Dynamic scope sources:
  - Deliverables scanned from the selected working root
  - Knowledge types scanned from canonical deliverable file types
- Knowledge-type scope is shown only when a knowledge decomposition marker is found in `_Decomposition`.

---

## 3. Hardening Status and Remaining Gaps

Ordered by priority (highest first). Some items below are now implemented or partially implemented; the status line records the current state and any remaining gap.

### 3.1 Content Hash Implementation for `_REFERENCES.md`

**What:** Add SHA-256 content hashes for out-of-folder references, aligned with no-ghost-input constraints (`K-GHOST-1`) and provenance requirements (`K-PROV-1`).

**Why:** Currently `_REFERENCES.md` lists paths and descriptions but does not verify that referenced content hasn't changed since sealing. Content hashes would enable automated integrity checking.

**Effort:** Medium. Requires changes to PREPARATION (hash computation on scaffold), ORCHESTRATOR (hash verification before pipeline runs), and tooling (hash generation/verification scripts).

### 3.2 Dependencies.csv Schema Linter

**Status:** Implemented. `tools/validation/validate_dependencies_schema.py` validates against the v3.1 schema (29 columns). Registered in `tools/REGISTRY.md`.

**What:** Deterministic validation of `Dependencies.csv` files against the v3.1 schema defined in `docs/SPEC.md` Section 6.

**Why:** This closes a previously identified gap and enables CI-level validation and drift detection across deliverables.

**Remaining gap:** None identified for the core capability. Future follow-on work in this area would be broader aggregation or reporting, not basic schema validation.

### 3.3 Automated Folder Structure Validator

**Status:** Partially implemented. `tools/validation/check_min_viable_fileset.sh` and `tools/validation/check_four_documents.sh` verify core file presence per deliverable. Full execution-root walkthrough against SPEC §12 is not yet a standalone tool.

**What:** Deliverable-level structural validation against the core required files, with a remaining gap for a full execution-root walkthrough against the checklist in `docs/SPEC.md` Section 12.

**Why:** Core file presence is now checkable outside agent runs, but a single execution-root validator would simplify pre-run checks and CI integration.

**Remaining effort:** Low. The remaining validation rules are fully defined; the missing piece is consolidation into one standalone execution-root walk.

### 3.4 On-Demand Dependency Graph Generation

**Status:** Substantially implemented. `tools/coordination/analyze_dep_closure.py` aggregates Dependencies.csv files and produces closure analysis (JSON summary + 6 CSV reports covering orphans, cycles/SCC, hubs, bidirectional pairs, and coverage). Visualization-oriented export (e.g., Mermaid) is not yet built.

**What:** Project-level dependency aggregation and closure analysis from deliverable-local `Dependencies.csv` files, with a remaining gap for visualization-oriented export (e.g., Mermaid).

**Why:** The analytical closure capability now exists without introducing a maintained central graph artifact. Additional export formats would improve visualization and critical-path-oriented review.

**Remaining effort:** Medium. The remaining work is graph-export formatting rather than core traversal or closure analysis.

### 3.5 Lock Mechanism Formalization

**What:** Formalize a deliverable-level lock mechanism for concurrent task execution.

**Why:** Concurrent agent execution on the same deliverable is prevented by convention but not enforced. A lock mechanism (e.g., `.lock` file with lease semantics) would enable safe parallel pipeline execution.

**Effort:** Medium-high. Requires lock acquisition/release protocol, orphan recovery, and integration into agent instructions.

### 3.6 Run Record Persistence

**Status:** Core implemented. `agents/AGENT_TASK.md` defines a persistent run-record contract: YAML frontmatter schema (13 fields), Markdown body (10 headings), storage at `{ScopePath}/_run_records/TASK_RUN_*.md`, two-phase lifecycle (PENDING at normalization, final status at completion). Downstream audit trail queries and rerun management tooling remain future work.

**What:** Unified persistent run records for `TASK` executions, with remaining gaps in downstream audit-trail query and rerun-management tooling.

**Why:** Core persistence now exists at the task-shell level. Follow-on tooling would improve retrieval, cross-run reporting, and rerun operations.

**Remaining effort:** Medium. The remaining work is downstream tooling on top of the established run-record contract.

### 3.7 Staleness Calculation Tooling

**What:** Implement staleness propagation and triage tooling based on dependency edges and baseline SHAs.

**Why:** Staleness is a contract commitment (K-STALE-1, K-STALE-2) but currently relies on human observation. Automated staleness detection from the dependency graph + git SHAs would make the system's integrity guarantees enforceable.

**Effort:** High. Depends on 3.4 (dependency graph generation) and 3.6 (run records with baseline SHAs).

---

## 4. Sequencing Rationale

The remaining gaps build on the currently available capabilities in this order:

1. **Content hashes** (3.1) — enables no-ghost-inputs enforcement.
2. **Full execution-root folder walkthrough** (remaining gap in 3.3) — extends existing per-deliverable checks into one standalone validator.
3. **Visualization-oriented dependency export** (remaining gap in 3.4) — builds on existing closure analysis.
4. **Lock mechanism** (3.5) — enables safe parallel execution.
5. **Audit-trail query + rerun tooling** (remaining gap in 3.6) — builds on the existing run-record contract.
6. **Staleness calculation** (3.7) — depends on dependency analysis plus run-record/baseline machinery; completes the governance loop.

---

## 5. Completed: Agent Suite Classification and Migration

**Status:** Complete (2026-04-04). 48/48 agents classified and ruled; 6 slices executed; 5 B-conversions + 5 C-pattern wrappers live (C-pattern wrappers subsequently normalized and archived — see §6); 1 new deterministic tool created (`tools/aggregation/build_hypergraph.py`); shared-file cross-references integrated; inventory reconciled.

**Intent (achieved):** Clarified boundaries between persona agents, bounded task agents, repo-native skills, and deterministic tools. Factored method logic downward into skills/tools while preserving pipeline-stage identities. Consistent with the compositional model: shell + profile + skill + tool + brief.

**Outcomes:**
- **Slice 1** (archives + non-agent relocations): 2 archived (EQUIPMENT_EXTRACT, TASK_ESTIMATING_TEMPLATE); 2 relocated (`docs/rubrics/AUDIT_AGENT.md`, `docs/templates/MEMORY_TEMPLATE.md`).
- **Slice 2** (F-case rulings + ORCHESTRATOR DOMAIN contradiction): DOMAIN_HYPERGRAPH → D, ESTIMATE_PREP → B. DOMAIN pipeline simplified — skips CHIRALITY_FRAMEWORK/LENS (Direction b). 6 files updated for consistency.
- **Slice 3** (B-conversions): 5 new skills created (`content-digest`, `estimate-snapshot`, `pdf2md-page`, `drawing-extract-page`, `estimate-prep`); 5 source agents archived. Companion docs for `estimate-prep` (SCHEMA_ANNEX, BOE_STRUCTURE, INDEX_MD_CONTRACT). Shared-file dispatches updated.
- **Slice 4** (C-pattern extractions): 5 new skills created (`semantic-matrix-build`, `lens-register`, `four-documents`, `domain-documents`, `dependency-extract`); 5 wrapper agents rewrote as thin dispatch shims (headers byte-identical). Cross-references integrated in ORCHESTRATOR, DELIVERABLE_TASK, `skills/semantic-lensing/SKILL.md`. **Superseded by §6:** C-pattern wrappers archived; skills now dispatched directly through TASK.
- **Slice 5a** (D-pattern additive notes): 4 audit agents annotated with explicit tool invocations (+37 lines, 0 deletions). Closure fix: reconciled stale `tools/query/` → `tools/evaluation/` path drift (6 references across 3 files) + fixed `validate_id_format.sh` signature bug.
- **Slice 5b** (DOMAIN_HYPERGRAPH-D refactor): created `tools/aggregation/build_hypergraph.py` (deterministic SHA1-based hypergraph construction + 9 QA checks + delta computation); rewrote AGENT_DOMAIN_HYPERGRAPH.md PROTOCOL Steps 4-8 as tool-invocation blocks. Steps 0-3 + SPEC + STRUCTURE + RATIONALE byte-identical.
- **Slice 6** (reconciliation + inventory): `docs/REPO_INVENTORY.md` updated and reconciled to the governed repo state at slice close; `docs/PLAN.md` marked complete.

**Final repo state:** See `docs/REPO_INVENTORY.md` for current governed counts. The migration reduced the live indexed agent suite, expanded the repo-native skill set, and added new deterministic tooling.

**Companion artifacts** (archived to `.Archive/` after completion):
- `.Archive/AGENT_SUITE_CLASSIFICATION.md` — ruled per-agent classification matrix (48/48, zero provisional)
- `.Archive/SEMANTIC_PIPELINE_ARCHITECTURE.md` — two-contract semantic-lensing model + ORCHESTRATOR contradiction ruling
- `.Archive/AGENT_SUITE_EXECUTION_PLAN.md` — slice mechanics, file ownership, parallelization, verification
- `.Archive/CHIRALITY_LENS_MIGRATION.md` — detailed Slice 4 migration (staged C end state; path to full normalization B documented)
- `.Archive/AGENT_SUITE_SESSION_HANDOFF.md` — session handoff (marked HISTORICAL / CLOSED)

**Deferred items (not in migration scope):**
- Full normalization (B end state) of C-pattern wrappers — **Completed in §6.** See §6 for outcomes.
- Frontend dispatch logic for archived ESTIMATE_PREP UI references (`frontend/app/page.tsx`, `frontend/components/PipelineView.tsx`) — requires separate frontend work (see §6 for expanded scope after wrapper archival).
- Residual `build_hypergraph.py` regression-hardening gaps — tracked in `plans/BUILD_HYPERGRAPH_DELTA_FIXTURE_PLAN.md` (delta-path fixture) and `plans/KTY_SUPPORTS_OBJ_LEDGER_ABSENT_FIXTURE_PLAN.md` (ledger-absent `KTY_SUPPORTS_OBJ` independence fixture).

**Follow-ups resolved after migration close:**
- CONFIDENCE enum reconciled to `{HIGH, MEDIUM, LOW}` canonical across validator + all skills (commit 676a907).
- Post-migration review fixes (commit 45bd9a1): `build_hypergraph.py` QA checks now emit explicit PASS rows per agent contract; `AGENT_EVALUATION.md` path drift fixed; session-handoff artifact marked CLOSED.
- Regression guard expansion (commits 71ecaae, ce673be): `validate_build_hypergraph_fixture.py` now covers determinism, clean-run PASS coverage, warning detection, ledger/objectives path coverage, semicolon-list normalization equivalence, and `UNIT_MULTIPLE_CATEGORIES` blocker detection.

---

## 6. Completed: Full Normalization of C-Pattern Wrappers + HELPS_HUMANS Governance Extension

**Status:** Complete (2026-04-04). 5 C-pattern wrappers archived; ORCHESTRATOR phases rewritten to dispatch TASK+skill directly; matrix normalized in AGENTS.md; HELPS_HUMANS extended to govern agents, skills, and tools as a single top-level standard.

**Intent (achieved):** Closed the deferred item from §5 — collapsed the staged C-pattern wrappers into the canonical dispatch path (ORCHESTRATOR → TASK + TaskSkill → skill contract), dropping one layer of indirection. In the same slice, made the implicit Type 0 → Type 1 governance hierarchy explicit across three workflow-component layers (agents, skills, tools).

**Outcomes:**
- **Archival:** 5 wrapper agents moved to `.Archive/agents/` with timestamp suffix (all 4 collisions with pre-migration fat-agent archives resolved via `.archived_2026-04-04` suffix; `AGENT_DOMAIN_DOCUMENTS.md` had no collision).
- **ORCHESTRATOR rewrite:** Phases 2.2, 2.3, 2.4, 2.5 rewritten as direct TASK+skill dispatch blocks; 5 "Wrapper note (staged C)" paragraphs removed; subagents frontmatter updated to `PREPARATION, DOMAIN_HYPERGRAPH, TASK`; Phase 2.6 DOMAIN_DOCUMENTS references updated to `domain-documents` skill.
- **Variant-rejection relocation:** Verified `four-documents` and `domain-documents` skills already contain authoritative `DECOMP_VARIANT` rejection (returning `UNSUPPORTED_VARIANT`); defense-in-depth preserved.
- **Actor-attribution policy:** Established canonical rule — `RequestedBy:` = dispatching persona; acting surface = `TASK+<skill-name>`; historical run records unchanged. Applied across all 5 skill folders' SKILL.md + BRIEF_SCHEMA.md + QA_CHECKS.md.
- **Matrix normalization (AGENTS.md):** `PREP*` → `PREPARATION`, `TASK*` → `TASK`, `EVALUATIVE × APPLYING` empty; wildcard expansion lines removed for collapsed cells; new "TASK Skill Capabilities" section added listing 11 canonical skills.
- **Cross-reference updates:** Wrapper role names replaced with TASK+skill equivalents across agents (AGENT_ORCHESTRATOR, AGENT_PREPARATION, AGENT_DELIVERABLE_TASK, AGENT_SCHEDULING, AGENT_REVIEW, AGENT_CHANGE, AGENT_SCOPE_CHANGE, AGENT_AUDIT_DEP_CLOSURE, AGENT_AUDIT_SCOPE_CLOSURE, AGENT_HELP_HUMAN), governance docs (SPEC.md, TYPES.md, CONTRACT.md, SE_Design_Analysis.md, REPO_INVENTORY.md count decrement 39→34), skill internal docs (all 5 skill folders), and tool docs (EXTERNAL_TOOLS.md, write_status.sh comments).
- **HELPS_HUMANS governance extension (Part 6):** Applicability extended to three workflow-component layers; "Design Outcomes for Skill Contracts" and "Design Outcomes for Tool Contracts" subsections added; PROTOCOL Step 4 extended with skill/tool classification routing; SPEC extended with R10 (skill tool policy), R11 (tool contract), R12 (skill/tool boundary).
- **SKILLMAKER + TOOLMAKER subordination:** Both Type 1 managers now cite HELPS_HUMANS as parent Type 0 standard explicitly; DBM §2.1 Type 0 table updated to list both managers as subordinate to HELPS_HUMANS.
- **DBM scope broadened:** Retitled to "Workflow-Component Architecture"; §1 scope expanded to three layers; §4 R1–R9 → R1–R12.
- **Supporting governance chain updated:** skills/README.md, skills/SKILL_TEMPLATE.md, tools/REGISTRY.md preamble, README.md architecture matrix + HELPS_HUMANS scope, AGENTS.md Type 0 row text.

**Final repo state:** 5 Type 2 wrappers archived; indexed agent count 39 → 34; matrix cells `PREPARATION` and `TASK` name canonical shells directly; `EVALUATIVE × APPLYING` cell intentionally empty. HELPS_HUMANS is now the single Type 0 standard governing agents + skills + tools. See `docs/REPO_INVENTORY.md` for current governed counts.

**Deferred items (not in slice scope):**
- **Frontend wrapper-reference cleanup** — `frontend/components/PipelineView.tsx`, `frontend/components/WorkbenchView.tsx`, `frontend/app/page.tsx` still list archived wrapper names. Mirrors Slice 3's ESTIMATE_PREP frontend deferral. The UI matrix in `docs/PLAN.md:77` (Matrix Navigation + Pipeline Taxonomy) diverges from the canonical architecture matrix until this frontend slice closes.
- **Structural TOOL_POLICY.md validator + R11 tool-contract** — TOOL_POLICY.md **presence** is machine-enforced (slice closed 2026-04-04). Remaining enforcement is tiered: Tier 1 deterministic structural checks (scoped in `plans/TOOL_POLICY_TIER1_VALIDATOR_PLAN.md`, ready to execute); Tier 2 LLM-based semantic audit (deferred until drift evidence surfaces); Tier 3 human judgment (already in place via gate review); R11 tool-contract extensions remain deferred as separate tool-layer scope.

**Follow-ups resolved after slice close:**
- **Thesis corpus normalization** — 3 parallel Haiku subagents + manual corrections replaced wrapper agent references in `docs/thesis/04_architecture.md`, `07_se_design_analysis.md`, `08_implementation.md`, `05_epistemic_architecture.md`, `appendix_a_invariant_catalog.md`, `appendix_b_agent_inventory.md` with canonical `TASK+<skill>` forms. Archived-wrapper table rows removed from `appendix_b_agent_inventory.md`. Only remaining wrapper-name matches in `docs/thesis/` are the philosophical `CHIRALITY_FRAMEWORK.md` methodology-document reference (false positive, preserved).
- **TOOL_POLICY.md constitutional conformance** (2026-04-04). HELPS_HUMANS's "Design Outcomes for Skill Contracts" declared TOOL_POLICY.md required but subsystem documentation (`skills/README.md`, `AGENT_SKILLMAKER.md`, `SKILL_TEMPLATE.md`) described it as optional, the validator did not check for it, and 13 of 15 skills lacked the file. Resolved by: (a) backfilling TOOL_POLICY.md for the 13 missing skills via 4 parallel general-purpose subagents (each file uses canonical 5 H2 + 2 H3 headings and applies the two-part tool derivation rule distinguishing TASK-enforced `allowed-tools` frontmatter from operationally invoked helpers), (b) normalizing the 2 pre-existing TOOL_POLICY.md files (`deliverable-consistency`, `pdf2md`) to canonical headings, (c) updating subsystem documentation (`skills/README.md`, `agents/AGENT_SKILLMAKER.md`, `skills/SKILL_TEMPLATE.md`) to declare TOOL_POLICY.md required + specify canonical heading schema, (d) extending `tools/validation/validate_skill_metadata.py` to enforce TOOL_POLICY.md presence (check #11). The HELPS_HUMANS → SKILLMAKER → skill-corpus hierarchy is now actually enforced, not just declared.

---

EOF
