# Agent Suite Migration — Session Handoff (HISTORICAL / CLOSED)

> **STATUS: CLOSED (2026-04-04).** The Agent Suite Classification and Migration workstream is complete. All 6 slices executed; all tasks closed. See `docs/PLAN.md` §5 for the completed-state summary. This file is preserved for historical reference only — **do not use it as live guidance for new work.** Content below describes the state partway through the migration and is now stale.

## Context

You are continuing the Agent Suite Classification and Migration workstream. Prior sessions:

**Session 1:**
- Ruled the classification (46 of 48 files; 2 provisional F-cases).
- Created 4 `plans/` artifacts + added a roadmap entry to `docs/PLAN.md`.

**Session 2 (most recent):**
- Executed Slices 1a, 1b, 2a, 2b, 3a, 3b.
- Ruled remaining F-cases (DOMAIN_HYPERGRAPH → D, ESTIMATE_PREP → B).
- Ruled ORCHESTRATOR DOMAIN contradiction (Direction b: DOMAIN skips CHIRALITY_LENS).
- Created 5 new B-skills + archived 5 source agents.
- Updated execution plan with scope expansions.
- Created task #16 (Slice 5b) for DOMAIN_HYPERGRAPH-D refactor.
- Created task #17 (CONFIDENCE enum cleanup — out of scope).

Your task is to execute the remaining slices (4a → 4b → 5a → 5b → 6) against the ruled plan.

---

## Read order (orientation)

Read, in order:

1. `INIT.md`
2. `agents/AGENT_HELPS_HUMANS.md` (adopt HELPS_HUMANS posture)
3. `docs/PLAN.md` §5 "In Progress: Agent Suite Classification and Migration"
4. `plans/AGENT_SUITE_CLASSIFICATION.md` (48/48 ruled classification matrix)
5. `plans/SEMANTIC_PIPELINE_ARCHITECTURE.md` (target model + resolved ORCHESTRATOR contradiction)
6. `plans/AGENT_SUITE_EXECUTION_PLAN.md` (slice mechanics with Slices 1-3 marked complete)
7. `plans/CHIRALITY_LENS_MIGRATION.md` (Slice 4 CHIRALITY_LENS detail)
8. This file (`plans/AGENT_SUITE_SESSION_HANDOFF.md`)

---

## State — what's done

| Slice | Status | Details |
|---|---|---|
| 1a | ✓ complete | Archived AGENT_EQUIPMENT_EXTRACT, TASK_ESTIMATING_TEMPLATE |
| 1b | ✓ complete | Relocated AUDIT_AGENT.md → `docs/rubrics/`, MEMORY_TEMPLATE.md → `docs/templates/` |
| 2a | ✓ complete | DOMAIN_HYPERGRAPH → D, ESTIMATE_PREP → B rulings recorded |
| 2b | ✓ complete | Direction (b) — DOMAIN skips CHIRALITY_LENS; 6 files updated |
| 3a | ✓ complete | 5 new B-skills created (content-digest, estimate-snapshot, pdf2md-page, drawing-extract-page, estimate-prep + 3 companion docs) |
| 3b | ✓ complete | 6 dispatch-rewrite files updated; AGENTS.md wildcards + Type 2 table updated; 5 agents archived |
| 4a | pending | C-pattern extractions (5 skills + 5 wrappers) |
| 4b | pending | Serial shared-file updates for C-pattern |
| 5a | pending | D-pattern additive notes (4 audits) |
| 5b | pending | DOMAIN_HYPERGRAPH-D refactor (new tool + PROTOCOL rewrite) |
| 6 | pending | Shared-file reconciliation + inventory |

Use `TaskList` to see current task state. Tasks 6-11 complete; Tasks 12-17 pending.

---

## Rulings captured (user-approved)

### Slice 2a (F-case resolutions)
- **DOMAIN_HYPERGRAPH → D.** Extract PROTOCOL Steps 4-8 (SHA1 hyperedge IDs, CSV construction, referential integrity, delta computation, snapshot publish) as new `tools/aggregation/build_hypergraph.py`. Steps 0-3 remain LLM. Non-additive refactor → **Slice 5b**.
- **ESTIMATE_PREP → B.** Single skill `skills/estimate-prep/` with `PHASE=SCAFFOLD|BOE` parameter (B1 form). Human gate is between runs, not inside a run.

### Slice 2b (ORCHESTRATOR DOMAIN contradiction)
- **Direction (b):** DOMAIN skips CHIRALITY_LENS. Files updated:
  - `agents/AGENT_ORCHESTRATOR.md` L264 (Precondition: Phase 2.2, not 2.5) + L268 (dependency chain: no CHIRALITY_FRAMEWORK/LENS)
  - `agents/AGENT_DOMAIN_DOCUMENTS.md` L31 (pipeline chain) + L34 (lifecycle: no SEMANTIC_READY) + L63 (ALLOW_OVERWRITE_STATES default)
  - `tools/EXTERNAL_TOOLS.md` L60-99 (DOMAIN pipeline simplified to 5-step linear flow)
- **CHIRALITY_LENS DOMAIN variant sections:** deferred to Slice 4 (C-migration); will strip DOMAIN support as part of lens-register skill creation.

### Slice 3a (companion docs for estimate-prep)
- Extracted source agent's Schema Annex + BOE structure + INDEX.md contract to three companion docs in `skills/estimate-prep/`:
  - `SCHEMA_ANNEX.md` (9 CSV families)
  - `BOE_STRUCTURE.md` (BOE_Scaffold + BASIS_OF_ESTIMATE + Run_Context + Publish_Manifest contracts)
  - `INDEX_MD_CONTRACT.md` (7-section INDEX.md contract)

### Out-of-scope cleanup items (created as tasks)
- **Task #17 (CONFIDENCE enum cleanup):** `tools/validation/validate_enum.py` uses `MEDIUM`; Detail.csv schema uses `MED`. Reconcile separately; outside Agent Suite Migration scope.
- **Frontend dispatch logic (flagged, not tracked as task):** `frontend/app/page.tsx:70` + `frontend/components/PipelineView.tsx:42` still reference `AGENT_ESTIMATE_PREP.md`. UI displays "ESTIMATE_PREP" as a TASK* button; dispatch logic needs to route to TASK+skill instead of the archived agent. Requires frontend work.

---

## Rulings still required (by slice)

### Slice 4a — 4_DOCUMENTS skill structure (user should rule)
- **Option A:** One skill `skills/four-documents/` with `PASS=1|2|3` brief parameter
- **Option B:** Three pass-specific skills (`skills/four-documents-pass1/`, `-pass2/`, `-pass3/`)

Defer to user at start of Slice 4a execution.

### Slice 4 — CHIRALITY_LENS DOMAIN variant stripping
- Strip DOMAIN variant support from `skills/lens-register/` SKILL.md at creation time (consistent with Direction b from Slice 2b). No additional ruling required; direction is already locked.

---

## Next action

**Begin Slice 4a:** parallel C-pattern extractions. 5 disjoint workers create skills + rewrite their wrapper agents. See `plans/AGENT_SUITE_EXECUTION_PLAN.md` Slice 4a for the worker-pair table.

Steps:
1. Ask user to rule 4_DOCUMENTS skill structure (Option A vs B).
2. Dispatch 5 parallel workers:
   - Worker 1: `skills/semantic-matrix-build/` + rewrite `agents/AGENT_CHIRALITY_FRAMEWORK.md`
   - Worker 2: `skills/lens-register/` + rewrite `agents/AGENT_CHIRALITY_LENS.md` (strip DOMAIN variant)
   - Worker 3: `skills/four-documents/` (or 3 variants) + rewrite `agents/AGENT_4_DOCUMENTS.md`
   - Worker 4: `skills/domain-documents/` + rewrite `agents/AGENT_DOMAIN_DOCUMENTS.md`
   - Worker 5: `skills/dependency-extract/` + rewrite `agents/AGENT_DEPENDENCIES.md`
3. User reviews each skill contract + each wrapper rewrite.
4. User approves → proceed to Slice 4b (serial shared-file cross-references).

C-pattern rules:
- Wrapper headers preserved byte-identical (AGENT_TYPE, AGENT_CLASS, WRITE_SCOPE, BLOCKING).
- PROTOCOL body replaced with TASK+skill dispatch reference (non-additive rewrite allowed).
- Agent remains in AGENTS.md TASK* wildcard (staged compatibility layer).
- See `plans/CHIRALITY_LENS_MIGRATION.md` for detailed pattern reference.

---

## Execution style

User preferences (from memory + session history):
- **Iterative plan review, sequencing discipline, no overclaims.**
- **Governance authority stays in main thread** — do not dispatch subagents for decisions (but parallel workers for disjoint execution work are OK and preferred for large parallel scopes like Slice 4a).
- **Pause at human checkpoints** per slice plan; present diffs/contracts for review; wait for approval.
- **Integrate external reviewer feedback substantively but justify independent calls.**
- User values architectural consistency; willing to make big changes when warranted.

Slice execution pattern:
1. Mark relevant TaskUpdate in_progress.
2. Execute slice actions (or dispatch parallel workers for disjoint work).
3. Run slice verification (validator, grep, diff checks per execution plan).
4. Present results + diffs for user review.
5. Mark task completed on user approval; pause at human checkpoints.
6. Report state concisely.

---

## Critical constraints

- **File ownership per worker** — no concurrent edits to shared files.
- **Shared files list (expanded):** `AGENTS.md`, `docs/PLAN.md`, `docs/REPO_INVENTORY.md`, `agents/AGENT_ORCHESTRATOR.md`, `agents/AGENT_TASK.md`, `agents/AGENT_EVALUATION.md`, `agents/AGENT_DELIVERABLE_TASK.md`, `agents/AGENT_PDF2MD.md`, `agents/AGENT_DRAWING_EXTRACT.md`, `skills/semantic-lensing/SKILL.md`, `tools/REGISTRY.md`, `tools/EXTERNAL_TOOLS.md`, `agents/AGENT_DOMAIN_DOCUMENTS.md`. Orchestrator-owned; serial edits only.
- **Edit discipline:**
  - **Slice 4a (C-pattern wrappers):** non-additive rewrites explicitly allowed (PROTOCOL body → TASK+skill dispatch shim)
  - **Slice 4b (shared-file cross-refs):** additive cross-reference notes
  - **Slice 5a (D-pattern audit notes):** strictly additive-only
  - **Slice 5b (DOMAIN_HYPERGRAPH refactor):** non-additive rewrites for PROTOCOL Steps 4-8 only; Steps 0-3 + SPEC + STRUCTURE + RATIONALE intact
  - Portal agent headers preserved byte-identical unless role is explicitly being revised
- **Validator gate:** `python3 tools/validation/validate_skill_metadata.py skills` must pass after each slice touching `skills/`.
- **Cross-reference grep:** after each slice, confirm zero dangling references to moved/archived files.

---

## Task tracker reference

Use `TaskList` to see current pending tasks.

| Task | Slice | Status | Purpose |
|---|---|---|---|
| 6 | 1a | ✓ | Archive EQUIPMENT_EXTRACT + TASK_ESTIMATING_TEMPLATE |
| 7 | 1b | ✓ | Relocate AUDIT_AGENT.md + MEMORY_TEMPLATE.md |
| 8 | 2a | ✓ | Rule F-cases (DOMAIN_HYPERGRAPH → D, ESTIMATE_PREP → B) |
| 9 | 2b | ✓ | Fix ORCHESTRATOR DOMAIN contradiction (Direction b) |
| 10 | 3a | ✓ | B-conversions (5 new skills + 3 companion docs) |
| 11 | 3b | ✓ | Serial shared-file updates + archives (5 agents) |
| 12 | 4a | pending | C-pattern extractions (5 skills + 5 wrappers) |
| 13 | 4b | pending | Serial shared-file updates for C-pattern |
| 14 | 5a | pending | D-pattern tool-invocation notes (4 audits, additive-only) |
| 16 | 5b | pending | DOMAIN_HYPERGRAPH-D refactor (create `tools/aggregation/build_hypergraph.py` + rewrite PROTOCOL Steps 4-8) |
| 15 | 6 | pending (blocked by 16) | Shared-file reconciliation + inventory |
| 17 | — | pending | Out-of-scope: CONFIDENCE enum mismatch (MEDIUM vs MED) |

---

## Change Log

- **2026-04-04:** Initial handoff. Tasks 1-5 complete; Slice 1a/1b rulings captured; Slice 1a is next.
- **2026-04-04 (Session 2):** Executed Slices 1-3 (tasks 6-11). Ruled Slice 2a F-cases, Slice 2b Direction b, Slice 3a companion docs. Created tasks #16 (5b refactor) and #17 (enum cleanup). Slice 4a is next.
