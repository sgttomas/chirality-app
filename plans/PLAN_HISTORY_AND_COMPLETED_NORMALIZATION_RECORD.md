# PLAN History and Completed Normalization Record

**Status:** Historical record. This file preserves the major completed-work and migration material that previously lived in [`docs/PLAN.md`](../docs/PLAN.md) before that document was refactored into a lean active roadmap/index on 2026-04-06.

This is not the active roadmap. For current planning and active links, use [`docs/PLAN.md`](../docs/PLAN.md).

---

## 1. Completed: System Hardening

The working system was codified into formal governance documents and aligned to the active agent framework.

### Governance Documents Written

| Document | Purpose | Status |
|----------|---------|--------|
| `docs/SPEC.md` | Physical structures, file formats, Dependencies.csv v3.1 schema, folder layout, validation checklist | Complete |
| `docs/TYPES.md` | Domain vocabulary, hierarchy, stable IDs, dependency vocabulary, agent roles, lifecycle states | Complete |
| `docs/DIRECTIVE.md` | Founding intent, design philosophy, professional responsibility model, scope, constraints | Complete |
| `docs/CONTRACT.md` | Invariant catalog, change policy, enforcement map | Complete |
| `docs/PLAN.md` | Roadmap document at the time of capture | Complete at the time of capture |

### Governance Alignment

At the time of capture, the governance documents were aligned on the core model:

- hierarchy is flat `package -> deliverable` across `TYPES.md`, `SPEC.md`, and `CONTRACT.md`
- authoritative execution state is file-based (`_STATUS.md`, `_DEPENDENCIES.md`, `Dependencies.csv`)
- the invariant catalog is centralized in `docs/CONTRACT.md`
- agent role boundaries and write scopes are defined by the active `AGENT_*.md` instruction suite

### Agent Instruction Hardening

Historically completed hardening items included:

- QA contract sections added to PREPARATION and the now-archived wrapper lineage
- output-persistence notes added to ORCHESTRATOR and RECONCILIATION

---

## 2. Existing Tooling Snapshot at Time of Capture

### Validation + Example Assets

- `examples/` provided concrete execution-root samples for regression and conformance testing
- `frontend/docs/harness/` documented SDK runtime validation and CI integration for harness behavior
- `frontend/scripts/validate-harness-*.mjs` provided repeatable local and CI validation gates

### Desktop Frontend Snapshot

At the time of capture, the desktop frontend (`frontend/`) included:

- session/turn API (`/api/harness/session/*`, `/api/harness/turn`)
- SSE streaming
- multimodal turn input via server-resolved attachments
- portal-to-pipeline navigation
- shared deliverables state across PORTAL and PIPELINE
- live project-directory refresh in `FileTree`
- desktop packaging
- harness validation automation
- operator toolkit panel for per-turn harness options
- resizable multi-pane layout hardening
- theme hardening and chat rendering improvements

### Matrix Navigation + Pipeline Taxonomy Snapshot

At the time of capture, the desktop UI still exposed the older UI labels and wildcard selector model even after the canonical architecture matrix had been normalized in the docs. That divergence was explicitly tracked as deferred frontend work.

---

## 3. Hardening Status and Remaining Gaps at Time of Capture

This section preserved the then-current hardening backlog:

### 3.1 Content Hash Implementation for `_REFERENCES.md`

- Add SHA-256 content hashes for out-of-folder references
- Rationale: no-ghost-input and provenance hardening

### 3.2 Dependencies.csv Schema Linter

- Status at capture: implemented
- `tools/validation/validate_dependencies_schema.py` validated the v3.1 schema

### 3.3 Automated Folder Structure Validator

- Status at capture: partially implemented
- deliverable-level checks existed; full execution-root walkthrough remained open

### 3.4 On-Demand Dependency Graph Generation

- Status at capture: substantially implemented
- closure analysis existed; visualization-oriented export remained open

### 3.5 Lock Mechanism Formalization

- still deferred at time of capture

### 3.6 Run Record Persistence

- Status at capture: core implemented through `AGENT_TASK.md`
- downstream retrieval and rerun-management tooling remained open

### 3.7 Staleness Calculation Tooling

- still deferred at time of capture

---

## 4. Sequencing Rationale Preserved from the Previous Roadmap

The preserved dependency order was:

1. content hashes
2. full execution-root folder walkthrough
3. visualization-oriented dependency export
4. lock mechanism
5. audit-trail query and rerun tooling
6. staleness calculation

This sequencing rationale was retained here as historical context for the old roadmap.

---

## 5. Completed: Agent Suite Classification and Migration

**Status at capture:** Complete (2026-04-04).

### Intent Achieved

The migration clarified boundaries between:

- persona agents
- bounded task agents
- repo-native skills
- deterministic tools

The working principle was the compositional model:

- shell
- profile
- skill
- tool
- brief

### Historical Outcomes Preserved

- archival and relocation of legacy and non-agent items
- F-case rulings and ORCHESTRATOR DOMAIN contradiction resolution
- B-conversions into skills (`content-digest`, `estimate-snapshot`, `pdf2md-page`, `drawing-extract-page`, `estimate-prep`)
- C-pattern extraction work that was later superseded by full normalization
- D-pattern additive tool notes for audit agents
- `build_hypergraph.py` creation and `DOMAIN_HYPERGRAPH` refactor
- inventory reconciliation at slice close

### Historical Deferred Items Preserved

The original record preserved these deferred items from that migration stage:

- full normalization of C-pattern wrappers
- frontend cleanup for archived ESTIMATE_PREP references
- `build_hypergraph.py` regression-hardening follow-ons

Those items were later partly or fully addressed by the subsequent normalization slice recorded below.

---

## 6. Completed: Full Normalization of C-Pattern Wrappers + HELPS_HUMANS Governance Extension

**Status at capture:** Complete (2026-04-04).

### Intent Achieved

This slice:

- collapsed the staged C-pattern wrappers into the canonical dispatch path
- normalized dispatch to `ORCHESTRATOR -> TASK + TaskSkill -> skill contract`
- made HELPS_HUMANS the explicit top-level standard governing agents, skills, and tools

### Historical Outcomes Preserved

- 5 C-pattern wrappers archived
- ORCHESTRATOR phases rewritten to dispatch TASK + skill directly
- matrix normalization in `AGENTS.md`
- actor-attribution policy normalized for skills
- HELPS_HUMANS extended with skill and tool governance outcomes
- SKILLMAKER and TOOLMAKER explicitly subordinated to HELPS_HUMANS
- DBM scope broadened to workflow-component architecture
- supporting governance docs updated across `skills/`, `tools/`, `README.md`, and `AGENTS.md`

### Historical Deferred Items Preserved

At the close of that slice, the preserved deferred items were:

- frontend wrapper-reference cleanup in `frontend/components/PipelineView.tsx`, `frontend/components/WorkbenchView.tsx`, and `frontend/app/page.tsx`
- structural TOOL_POLICY.md validator follow-on and broader R11 tool-contract enforcement

### Historical Follow-ups Resolved After Slice Close

The previous roadmap also preserved these already-resolved follow-ups:

- thesis corpus normalization from wrapper-agent references to canonical `TASK+<skill>` forms
- TOOL_POLICY.md constitutional conformance across the live skill corpus
- validator enforcement of required TOOL_POLICY.md presence

---

## 7. Relationship to Current Planning

Use this file for:

- historical migration context
- references to completed normalization slices
- older notes that were previously embedded in `docs/PLAN.md`

Use the following for active planning:

- [`docs/PLAN.md`](../docs/PLAN.md) — active roadmap and plan index
- [`plans/TYPE2_RATIONALIZATION_MASTER_PLAN.md`](../plans/TYPE2_RATIONALIZATION_MASTER_PLAN.md) — current architecture direction for Type 2 rationalization
- [`plans/AUDIT_WORKFLOW_NORMALIZATION_PLAN.md`](../plans/AUDIT_WORKFLOW_NORMALIZATION_PLAN.md)
- [`plans/EVALUATION_WORKFLOW_NORMALIZATION_PLAN.md`](../plans/EVALUATION_WORKFLOW_NORMALIZATION_PLAN.md)

---
