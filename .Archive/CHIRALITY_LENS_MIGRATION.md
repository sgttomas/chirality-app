# CHIRALITY_LENS Migration (Slice 4 detail)

## Scope

Step-by-step migration for CHIRALITY_LENS C-pattern extraction. Covers actions, downstream file changes with line references, compatibility behavior, and verification. Does **not** restate architectural rationale — see `plans/SEMANTIC_PIPELINE_ARCHITECTURE.md` for target model.

Part of **Slice 4** in `plans/AGENT_SUITE_EXECUTION_PLAN.md`. This document focuses on CHIRALITY_LENS specifically; parallel C-pattern migrations (CHIRALITY_FRAMEWORK, 4_DOCUMENTS, DOMAIN_DOCUMENTS, DEPENDENCIES) follow analogous patterns.

---

## End state

### Staged C (this migration)

- `agents/AGENT_CHIRALITY_LENS.md` retained as pipeline-stage agent (thin dispatch shim).
- `skills/lens-register/` created with full method contract.
- ORCHESTRATOR Phase 2.4 continues to spawn CHIRALITY_LENS.
- CHIRALITY_LENS internally dispatches TASK + `TaskSkill: lens-register`.
- `AGENTS.md` TASK* wildcard preserves CHIRALITY_LENS.

### Full normalization B (deferred — not this migration)

If later ruled for whole-pipeline unit migration:
- CHIRALITY_LENS wrapper archives to `.Archive/`.
- ORCHESTRATOR Phase 2.4 dispatches TASK directly.
- `AGENTS.md` TASK* wildcard loses CHIRALITY_LENS entry.
- This document extends with B-migration steps at that time.

---

## Migration actions (staged C)

### Step 1 — Create `skills/lens-register/`

Create folder and files:
- `skills/lens-register/SKILL.md`
- `skills/lens-register/BRIEF_SCHEMA.md`
- `skills/lens-register/QA_CHECKS.md`

**`SKILL.md` frontmatter:**
```yaml
---
name: lens-register
description: Generate a matrix-organized, coverage-complete semantic lensing register (_SEMANTIC_LENSING.md) from _SEMANTIC.md + production documents. Setup-pipeline companion to the interactive semantic-lensing skill.
compatibility: Chirality TASK; invoked by CHIRALITY_LENS wrapper during ORCHESTRATOR setup pipeline.
metadata:
  chirality-skill-version: "1"
  chirality-task-profile: (none — invoked directly via TASK shell)
---
```

**`SKILL.md` body:** Migrate PROTOCOL from `AGENT_CHIRALITY_LENS.md` Steps 0-5 verbatim, adapting references from "agent" to "skill". Preserve:
- Straight-through lensing procedure (Steps 0-5)
- Matrix-cell traversal (A, B, C, F, D, X, E)
- Warranted-threshold filter (Conflict, VerificationGap, MissingSlot, WeakStatement, RationaleGap, Normalization, TBD_Question, MatrixError)
- Provenance requirements (SourcePath + SectionRef)
- Output file schema (`_SEMANTIC_LENSING.md` header + summary + per-matrix Lens Coverage + Warranted Items tables)

**`BRIEF_SCHEMA.md`:** document required/optional brief fields:
```markdown
# lens-register — Brief Schema

## Required
- `DeliverablePath` (or `deliverable_folder`) — absolute path to one production unit folder

## Optional
- `DECOMP_VARIANT` — PROJECT | SOFTWARE | DOMAIN (default PROJECT)
```

**`QA_CHECKS.md`:** preserve all 8 invariants from `AGENT_CHIRALITY_LENS.md`:
1. Matrix coverage complete (every cell has a Lens Coverage entry)
2. No invention (warranted items grounded in evidence or explicit absence)
3. Provenance present (SourcePath + SectionRef or "location TBD")
4. Conflicts surfaced (Contenders populated; HumanRuling = TBD)
5. Summary consistent (counts match actual items)
6. Schema followed (exact STRUCTURE schema)
7. One deliverable per run (no cross-deliverable scanning)
8. Read-only on production documents

### Step 2 — Run skill validator

```sh
python3 tools/validation/validate_skill_metadata.py skills
```

Must pass. Fix any validation errors before proceeding.

### Step 3 — Rewrite `agents/AGENT_CHIRALITY_LENS.md` as thin wrapper

**Preserve (byte-identical):**
- Frontmatter description
- `[[DOC:AGENT_INSTRUCTIONS]]` marker
- Title: `# AGENT INSTRUCTIONS — Chirality Lens (CHIRALITY_LENS)`
- `AGENT_TYPE: 2`
- Full Agent Type table (TYPE 2 / TASK / spawned or INIT-TASK / deliverable-local / never / `_SEMANTIC_LENSING.md`)
- Naming convention notice

**Replace (non-additive rewrite):**
- Purpose section
- Precedence / Non-negotiable invariants / Glossary
- PROTOCOL Steps 0-5
- SPEC S1-S5
- STRUCTURE file schema

With (approximate body):
```markdown
## Purpose

CHIRALITY_LENS is a thin pipeline-stage wrapper that preserves dispatch identity for ORCHESTRATOR Phase 2.4. The lensing method is defined in `skills/lens-register/SKILL.md`. When invoked, this agent dispatches TASK with `TaskSkill: lens-register` for the assigned deliverable.

## Integration Contract

Inputs (unchanged):
- `deliverable_folder` — absolute path to one production unit folder
- `DECOMP_VARIANT` (optional) — PROJECT | SOFTWARE | DOMAIN

Outputs (unchanged):
- `{deliverable_folder}/_SEMANTIC_LENSING.md`

## Behavior

This agent dispatches a single TASK run with:
- `TaskProfile: (none)`
- `TaskSkill: lens-register`
- `ScopePath: {deliverable_folder}`
- `DECOMP_VARIANT: {variant}`

The skill's SKILL.md + QA_CHECKS.md define the method, invariants, and output schema. This wrapper adds no decision rights, no authority surface, and no content beyond dispatch identity.

## Pipeline position

Invoked by ORCHESTRATOR Phase 2.4. Produces `_SEMANTIC_LENSING.md` which is consumed by 4_DOCUMENTS Pass 3 (Phase 2.5) and optionally by DELIVERABLE_TASK with `UseSemanticLensing: true` (via `skills/semantic-lensing/`).

## See also
- `skills/lens-register/SKILL.md` — method contract
- `skills/semantic-lensing/SKILL.md` — interactive proposal workflow consuming the register
- `plans/SEMANTIC_PIPELINE_ARCHITECTURE.md` — two-contract architecture
```

**Rationale for non-additive rewrite:** per `plans/AGENT_SUITE_EXECUTION_PLAN.md` cross-cutting rules, Slice 4 C-pattern wrappers explicitly allow non-additive rewrites. The wrapper's value is dispatch identity + cross-references; method content belongs in the skill.

### Step 4 — Update `agents/AGENT_ORCHESTRATOR.md` (dispatch-note touch)

**File:** `agents/AGENT_ORCHESTRATOR.md`
**Section:** Phase 2.4 (line ~238-246)
**Change:** Add dispatch-note after existing action:

Existing text:
```
- Spawn CHIRALITY_LENS for each deliverable (pass `DECOMP_VARIANT`) to generate `_SEMANTIC_LENSING.md`.
- CHIRALITY_LENS does not edit production documents; it produces a read-only enrichment register.
```

Add (staged end state):
```
- CHIRALITY_LENS is a thin pipeline-stage wrapper; it internally dispatches TASK with `TaskSkill: lens-register`. See `skills/lens-register/SKILL.md` for the method contract and `plans/SEMANTIC_PIPELINE_ARCHITECTURE.md` for the two-contract architecture.
```

**Scope:** documentation note only; dispatch chain unchanged. No frontmatter `subagents:` change (CHIRALITY_LENS still in list).

### Step 5 — Update `agents/AGENT_DELIVERABLE_TASK.md` (cross-reference)

**File:** `agents/AGENT_DELIVERABLE_TASK.md`
**Section:** "Optional semantic lensing mode" (line ~225-235)
**Change:** Add cross-reference after existing `> Extracted:` note:

Add (after the existing extraction block at line ~227):
```
> **Family context:** `skills/semantic-lensing/` is the interactive proposal-producing path. Its setup-time counterpart is `skills/lens-register/` (invoked by CHIRALITY_LENS in ORCHESTRATOR Phase 2.4), which produces the `_SEMANTIC_LENSING.md` register that this skill consumes as a candidate worklist. See `plans/SEMANTIC_PIPELINE_ARCHITECTURE.md`.
```

### Step 6 — Update `skills/semantic-lensing/SKILL.md` (cross-reference)

**File:** `skills/semantic-lensing/SKILL.md`
**Section:** Purpose (line ~12-16)
**Change:** Add cross-reference after existing purpose statement:

After existing line ~16:
```
This skill is the **interactive, proposal-producing** contract in the semantic-lensing family. Its setup-time counterpart is `skills/lens-register/`, which generates the matrix-organized register (`_SEMANTIC_LENSING.md`) that this skill consumes as a candidate worklist. Both skills are documented in `plans/SEMANTIC_PIPELINE_ARCHITECTURE.md`.
```

### Step 7 — `AGENTS.md` (no change)

In the staged end state, `AGENTS.md` TASK* wildcard preserves CHIRALITY_LENS. No edits to AGENTS.md required for Slice 4 CHIRALITY_LENS migration.

(Full normalization would remove CHIRALITY_LENS from TASK* wildcard — deferred.)

---

## Downstream file inventory (with line references)

| File | Action | Line refs (approximate) |
|---|---|---|
| `skills/lens-register/SKILL.md` | **Create** | new file |
| `skills/lens-register/BRIEF_SCHEMA.md` | **Create** | new file |
| `skills/lens-register/QA_CHECKS.md` | **Create** | new file |
| `agents/AGENT_CHIRALITY_LENS.md` | **Rewrite (non-additive)** | whole body; header preserved |
| `agents/AGENT_ORCHESTRATOR.md` | **Modify (additive note)** | ~L238-246 (Phase 2.4 action block) |
| `agents/AGENT_DELIVERABLE_TASK.md` | **Modify (additive cross-reference)** | ~L225-235 (Optional semantic lensing mode) |
| `skills/semantic-lensing/SKILL.md` | **Modify (additive cross-reference)** | ~L12-16 (Purpose) |
| `agents/AGENT_4_DOCUMENTS.md` | **Verify (likely no change)** | Pass 3 continues to consume `_SEMANTIC_LENSING.md` from its standard path |
| `AGENTS.md` | **No change** | CHIRALITY_LENS preserved in TASK* wildcard for staged end state |
| `docs/REPO_INVENTORY.md` | **No change now** | update in Slice 6 after all skill creations |

---

## Compatibility behavior during migration

### Runtime compatibility

- **ORCHESTRATOR dispatch unchanged:** "Spawn CHIRALITY_LENS for each deliverable" continues to work; the wrapper internally dispatches TASK+skill.
- **4_DOCUMENTS Pass 3 unchanged:** continues to consume `_SEMANTIC_LENSING.md` from the standard path; does not care whether it was produced by the pre-migration agent or post-migration wrapper+skill.
- **DELIVERABLE_TASK unchanged:** continues to optionally update `_SEMANTIC_LENSING.md` via `skills/semantic-lensing/` when authorized. The register it consumes may have been produced by either path.

### Output compatibility

The `_SEMANTIC_LENSING.md` output format is defined by the skill's QA_CHECKS.md (migrated verbatim from the agent's STRUCTURE section). Output schema is byte-compatible:
- File header (required)
- Summary block (required)
- Per-matrix sections (required): Lens Coverage table + Warranted Items table
- Column schema: ItemID, LensKey, Type, AppliesToDoc, SuggestedEditDoc, CandidateInfo, WhyWarranted, SourcePath, SectionRef, Contenders, ProposedAuthority, HumanRuling

### Backward compatibility window

During the migration slice:
- If any subagent reads the pre-migration `AGENT_CHIRALITY_LENS.md` after Step 3, it sees the thin wrapper (not the full method).
- If any human operator searches `agents/` for lensing method details, they will find the wrapper with a pointer to `skills/lens-register/SKILL.md`.
- No concurrent edit risk: Slice 4 is serialized per worker; wrapper rewrite completes before ORCHESTRATOR note is added.

---

## Verification steps

### After Step 1 (skill creation)

- `skills/lens-register/SKILL.md` exists with valid frontmatter (`name: lens-register`, `metadata.chirality-skill-version: "1"`).
- `BRIEF_SCHEMA.md` and `QA_CHECKS.md` present.
- Matrix coverage, no-invention, provenance, and conflict-surfacing invariants documented in QA_CHECKS.md.

### After Step 2 (validator)

```sh
python3 tools/validation/validate_skill_metadata.py skills
```
Returns zero errors.

### After Step 3 (wrapper rewrite)

- `agents/AGENT_CHIRALITY_LENS.md` Agent Type table byte-identical to pre-rewrite.
- Wrapper body ≤ 50 lines (thin dispatch shim).
- Contains explicit pointer to `skills/lens-register/SKILL.md`.
- No residual method prose that duplicates skill content.

### After Step 4 (ORCHESTRATOR note)

- Phase 2.4 text contains new dispatch-note paragraph referencing `skills/lens-register/`.
- Existing "Spawn CHIRALITY_LENS for each deliverable" text preserved.
- `subagents:` frontmatter unchanged.

### After Step 5 (DELIVERABLE_TASK cross-reference)

- "Optional semantic lensing mode" section contains new family-context note.
- Existing `> Extracted:` block preserved.

### After Step 6 (semantic-lensing skill cross-reference)

- `skills/semantic-lensing/SKILL.md` Purpose contains new family-context paragraph.

### Cross-slice verification

- Grep `CHIRALITY_LENS` across repo: references exist in ORCHESTRATOR, AGENTS.md, DELIVERABLE_TASK, examples/ (historical outputs); no dangling references.
- Grep `lens-register` across repo: references exist in ORCHESTRATOR, DELIVERABLE_TASK, semantic-lensing/SKILL.md, plans/.
- `python3 tools/validation/validate_skill_metadata.py skills` still passes after Steps 1-6.

---

## Rollback plan (if migration fails)

If Slice 4 CHIRALITY_LENS migration must be rolled back:

1. `git revert` the commit(s) for Steps 1-6.
2. Or manually:
   - Delete `skills/lens-register/` folder.
   - Restore `agents/AGENT_CHIRALITY_LENS.md` from git history.
   - Revert ORCHESTRATOR, DELIVERABLE_TASK, semantic-lensing cross-references.
3. Run validator + grep sweep to confirm clean state.

No data loss — original `_SEMANTIC_LENSING.md` outputs in `examples/` are unaffected.

---

## Change Log

- **2026-04-04:** Initial migration document. Staged C end state; 7 actions; downstream file inventory with line refs; rollback plan documented.
