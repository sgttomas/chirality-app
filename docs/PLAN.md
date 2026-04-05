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
| QA Contract sections added | PREPARATION, 4_DOCUMENTS, CHIRALITY_FRAMEWORK, CHIRALITY_LENS |
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

**Status:** Complete (2026-04-04). 48/48 agents classified and ruled; 6 slices executed; 5 B-conversions + 5 C-pattern wrappers live; 1 new deterministic tool created (`tools/aggregation/build_hypergraph.py`); shared-file cross-references integrated; inventory reconciled.

**Intent (achieved):** Clarified boundaries between persona agents, bounded task agents, repo-native skills, and deterministic tools. Factored method logic downward into skills/tools while preserving pipeline-stage identities. Consistent with the compositional model: shell + profile + skill + tool + brief.

**Outcomes:**
- **Slice 1** (archives + non-agent relocations): 2 archived (EQUIPMENT_EXTRACT, TASK_ESTIMATING_TEMPLATE); 2 relocated (`docs/rubrics/AUDIT_AGENT.md`, `docs/templates/MEMORY_TEMPLATE.md`).
- **Slice 2** (F-case rulings + ORCHESTRATOR DOMAIN contradiction): DOMAIN_HYPERGRAPH → D, ESTIMATE_PREP → B. DOMAIN pipeline simplified — skips CHIRALITY_FRAMEWORK/LENS (Direction b). 6 files updated for consistency.
- **Slice 3** (B-conversions): 5 new skills created (`content-digest`, `estimate-snapshot`, `pdf2md-page`, `drawing-extract-page`, `estimate-prep`); 5 source agents archived. Companion docs for `estimate-prep` (SCHEMA_ANNEX, BOE_STRUCTURE, INDEX_MD_CONTRACT). Shared-file dispatches updated.
- **Slice 4** (C-pattern extractions): 5 new skills created (`semantic-matrix-build`, `lens-register`, `four-documents`, `domain-documents`, `dependency-extract`); 5 wrapper agents rewrote as thin dispatch shims (headers byte-identical). Cross-references integrated in ORCHESTRATOR, DELIVERABLE_TASK, `skills/semantic-lensing/SKILL.md`.
- **Slice 5a** (D-pattern additive notes): 4 audit agents annotated with explicit tool invocations (+37 lines, 0 deletions). Closure fix: reconciled stale `tools/query/` → `tools/evaluation/` path drift (6 references across 3 files) + fixed `validate_id_format.sh` signature bug.
- **Slice 5b** (DOMAIN_HYPERGRAPH-D refactor): created `tools/aggregation/build_hypergraph.py` (deterministic SHA1-based hypergraph construction + 9 QA checks + delta computation); rewrote AGENT_DOMAIN_HYPERGRAPH.md PROTOCOL Steps 4-8 as tool-invocation blocks. Steps 0-3 + SPEC + STRUCTURE + RATIONALE byte-identical.
- **Slice 6** (reconciliation + inventory): REPO_INVENTORY updated (39 agents / 15 skills / 50 tools); docs/PLAN.md marked complete.

**Final repo state:** 39 live agents (down from 48); 15 repo-native skills (up from 5); 50 registered tools (up from 49).

**Companion artifacts:**
- `plans/AGENT_SUITE_CLASSIFICATION.md` — ruled per-agent classification matrix (48/48, zero provisional)
- `plans/SEMANTIC_PIPELINE_ARCHITECTURE.md` — two-contract semantic-lensing model + ORCHESTRATOR contradiction ruling
- `plans/AGENT_SUITE_EXECUTION_PLAN.md` — slice mechanics, file ownership, parallelization, verification (all slices marked complete)
- `plans/CHIRALITY_LENS_MIGRATION.md` — detailed Slice 4 migration (staged C end state with path to full normalization)

**Deferred items (not in migration scope):**
- Full normalization (B end state) of C-pattern wrappers — requires whole-pipeline unit migration decision.
- Frontend dispatch logic for archived ESTIMATE_PREP UI references (`frontend/app/page.tsx`, `frontend/components/PipelineView.tsx`) — requires separate frontend work.
- CONFIDENCE enum mismatch reconciliation (`validate_enum.py` uses MEDIUM vs Detail.csv uses MED) — out of scope.

---

EOF
