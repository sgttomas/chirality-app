# PLAN — Development Roadmap

This document captures the development roadmap for the Chirality project execution system. It summarizes what has been codified, identifies future hardening candidates, and provides sequencing rationale.

---

## 1. Completed: System Hardening

The working system has been codified into formal governance documents. The Charter has been updated to match reality.

### Governance Documents Written

| Document | Purpose | Status |
|----------|---------|--------|
| `docs/SPEC.md` | Physical structures, file formats, Dependencies.csv v3.1 schema, folder layout, validation checklist | Complete |
| `docs/TYPES.md` | Domain vocabulary, hierarchy, stable IDs, dependency vocabulary, agent roles, lifecycle states | Complete |
| `docs/DIRECTIVE.md` | Founding intent, design philosophy, professional responsibility model, scope, constraints | Complete |
| `docs/CONTRACT.md` | Invariant catalog (20 K-* invariants), change policy, enforcement map | Complete |
| `docs/PLAN.md` | This document | Complete |

### Charter Alignment

`CHARTER.md` has been revised to match the working system:
- Hierarchy updated from `phase->package->deliverable->task` to flat `package->deliverable`
- YAML references replaced with Markdown/CSV reality (`_STATUS.md`, `_DEPENDENCIES.md`, `Dependencies.csv`)
- Aspirational `schemas/`, `.project/`, `phases/` references removed
- Invariant catalog points to `docs/CONTRACT.md` as authoritative source
- Agent capabilities registry mapped to actual agent instruction files
- Definition of Done checklist updated

### Agent Instruction Hardening

| Change | Agents Affected |
|--------|-----------------|
| QA Contract sections added | PREPARATION, 4_DOCUMENTS, CHIRALITY_FRAMEWORK, CHIRALITY_LENS |
| Output Persistence notes added | ORCHESTRATOR, RECONCILIATION |

Agent instruction consistency: 92% → estimated 95%+ after hardening.

---

## 2. Existing Tooling

### Python Analysis Tools (`tools/`)

| Script | Purpose |
|--------|---------|
| `build_semantic_db.py` | Extracts semantic matrix cells from `_SEMANTIC.md` files into a structured database/CSV |
| `analyze_semantic_convergence.py` | Analyzes convergence patterns across semantic matrices |
| `collect_semantics.py` | Collects `_SEMANTIC.md` content across deliverables |
| `interpret_semantic_cells.py` | Interprets individual semantic matrix cells |

These tools support the semantic analysis pipeline: CHIRALITY_FRAMEWORK generates `_SEMANTIC.md` per deliverable, CHIRALITY_LENS produces `_SEMANTIC_LENSING.md`, and these Python tools enable cross-deliverable analysis.

### Desktop Frontend (`frontend/`)

Next.js + Electron desktop app with:
- Session/turn API (`/api/harness/session/*`, `/api/harness/turn`)
- Streaming event protocol (SSE)
- Desktop packaging (macOS `.dmg`, Windows `.exe`)
- Harness validation automation

---

## 3. Future Hardening Candidates

Ordered by priority (highest first):

### 3.1 Content Hash Implementation for `_REFERENCES.md`

**What:** Add SHA-256 content hashes for out-of-folder references, as described in the Charter's no-ghost-inputs principle (Section 4.1).

**Why:** Currently `_REFERENCES.md` lists paths and descriptions but does not verify that referenced content hasn't changed since sealing. Content hashes would enable automated integrity checking.

**Effort:** Medium. Requires changes to PREPARATION (hash computation on scaffold), ORCHESTRATOR (hash verification before pipeline runs), and tooling (hash generation/verification scripts).

### 3.2 Dependencies.csv Schema Linter

**What:** A validation script that reads `Dependencies.csv` files and checks them against the v3.1 schema defined in `docs/SPEC.md` Section 6.

**Why:** Schema violations are currently caught only by agent-internal quality checks. An external linter would enable CI-level validation and catch drift across deliverables.

**Effort:** Low. The schema is fully specified. Implementation is a Python script that validates column presence, enum values, identity rules, and provenance requirements.

### 3.3 Automated Folder Structure Validator

**What:** A script that walks the execution root and validates each deliverable folder against the checklist in `docs/SPEC.md` Section 12.

**Why:** Missing files or unexpected structures are currently detected only during agent runs. A standalone validator enables pre-run checks and CI integration.

**Effort:** Low. The validation rules are fully defined.

### 3.4 On-Demand Dependency Graph Generation

**What:** A tool that aggregates deliverable-local `Dependencies.csv` files into a project-level dependency graph (JSON or Mermaid).

**Why:** The system intentionally avoids a central dependency graph to prevent sync burden. However, on-demand generation from the authoritative local registers would enable visualization, critical path analysis, and cycle detection without maintaining a separate artifact.

**Effort:** Medium. Requires traversal of all `Dependencies.csv` files, ID resolution, and graph output format.

### 3.5 Lock Mechanism Formalization

**What:** Formalize the deliverable-level lock mechanism described in Charter Section 8.1.

**Why:** Concurrent agent execution on the same deliverable is prevented by convention but not enforced. A lock mechanism (e.g., `.lock` file with lease semantics) would enable safe parallel pipeline execution.

**Effort:** Medium-high. Requires lock acquisition/release protocol, orphan recovery, and integration into agent instructions.

### 3.6 Run Record Persistence

**What:** Formalize the pipeline run record schema described in Charter Section 5.

**Why:** Currently, pipeline runs are tracked in `_STATUS.md` history and `_DEPENDENCIES.md` run history, but there is no unified run record per Agent 2 execution. Formal run records would enable better audit trails and rerun management.

**Effort:** Medium. Requires schema definition, storage location decision, and integration into task agent protocols.

### 3.7 Staleness Calculation Tooling

**What:** Implement the staleness propagation and triage mechanism described in Charter Sections 7.1-7.3.

**Why:** Staleness is a charter commitment (K-STALE-1, K-STALE-2) but currently relies on human observation. Automated staleness detection from the dependency graph + git SHAs would make the system's integrity guarantees enforceable.

**Effort:** High. Depends on 3.4 (dependency graph generation) and 3.6 (run records with baseline SHAs).

---

## 4. Sequencing Rationale

The future candidates are ordered to build on each other:

1. **Schema linter + folder validator** (3.2, 3.3) — low effort, high immediate value, no dependencies
2. **Content hashes** (3.1) — enables no-ghost-inputs enforcement
3. **Dependency graph generation** (3.4) — enables visualization and analysis
4. **Lock mechanism** (3.5) — enables safe parallel execution
5. **Run records** (3.6) — enables audit trails
6. **Staleness calculation** (3.7) — depends on graph + run records; completes the governance loop

---

EOF
