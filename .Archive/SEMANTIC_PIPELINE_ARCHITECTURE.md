# Semantic Pipeline Architecture

## Scope

This document defines the **target model** and **rationale** for the semantic-lensing family and the PROJECT/SOFTWARE setup pipeline. It does **not** contain slice-level migration steps — those live in `plans/CHIRALITY_LENS_MIGRATION.md` and `plans/AGENT_SUITE_EXECUTION_PLAN.md`.

Companion: `plans/AGENT_SUITE_CLASSIFICATION.md` (per-agent rulings).

---

## Two-contract semantic-lensing family

The semantic-lensing family consists of **two distinct skills serving different consumers**, plus one pipeline-stage wrapper agent.

| Contract | Skill | Consumer | Output | Usage context |
|---|---|---|---|---|
| **Setup-time register** | `skills/lens-register/` (NEW) | ORCHESTRATOR Phase 2.4 via CHIRALITY_LENS wrapper | `_SEMANTIC_LENSING.md` (exhaustive coverage register) | Automated setup pipeline (PROJECT/SOFTWARE) |
| **Interactive enrichment** | `skills/semantic-lensing/` (EXISTING) | DELIVERABLE_TASK with `UseSemanticLensing: true` | PROPOSAL blocks with `Lens:` tags (+ optional register updates) | Interactive human-facing sessions |

### Relationship: sequential stages, not alternative modes

- `skills/lens-register/` **produces** the register.
- `skills/semantic-lensing/` **consumes** the register as a candidate worklist.

The reviewer's hypothesis that these are "two output modes of one method" was incorrect based on repo evidence:
- `AGENT_CHIRALITY_LENS.md` produces a matrix-organized register with **complete coverage** (every cell accounted for) — automated pipeline discipline.
- `skills/semantic-lensing/SKILL.md` produces **warranted-only** proposal blocks for human review — interactive workflow discipline.

The outputs diverge in completeness discipline, format, and consumer. They are genuinely different contracts.

---

## Invariants preserved

### lens-register (setup-time, exhaustive)

| Invariant | Source |
|---|---|
| Matrix coverage complete | Every cell of each matrix A, B, C, F, D, X, E has a Lens Coverage entry |
| No invention | Warranted items grounded in evidence or explicit absence |
| Provenance mandatory | Every item has `SourcePath` + best-effort `SectionRef` |
| Conflicts surfaced | Contenders cited; HumanRuling = TBD |
| Read-only on production documents | Writes only `_SEMANTIC_LENSING.md` |
| Register-output discipline | Lens Coverage table + Warranted Items table format |
| One deliverable per run | No cross-deliverable scanning |
| Avoid restatement | Only warranted items; NO_ITEMS coverage is valid |

### semantic-lensing (interactive, warranted-only proposals)

| Invariant | Source |
|---|---|
| Matrices are lenses, not authority | Tagging convention only |
| Lensing entries are candidates, not evidence | Cannot authorize new facts |
| PROPOSAL evidence-linked | Every proposal cites production document evidence |
| Lens tags canonical format | `Matrix.Row.Column` |
| Unknowns remain TBD | No invention to fill gaps |
| Conflicts surfaced not reconciled | NEEDS_HUMAN_RULING interface |
| `_SEMANTIC.md` read-only | Never modify the matrix definition |

### Shared invariants (both contracts)

- Deliverable-local scope (single folder per run).
- Deliverable-bound perspective (variant-aware for PROJECT/SOFTWARE/DOMAIN).
- Human decision rights preserved (HumanRuling = TBD for consequential choices).
- No recursive ingestion (skill outputs are not re-ingested as inputs unless explicitly instructed).

---

## Pipeline position (PROJECT/SOFTWARE)

```
ORCHESTRATOR Phase 2.1  PREPARATION (scaffolds deliverable folders + minimum viable fileset)
                 Phase 2.2  4_DOCUMENTS Pass 1 + Pass 2 (initial drafts + structure)
                 Phase 2.3  CHIRALITY_FRAMEWORK → _SEMANTIC.md (matrix algebra)
                 Phase 2.4  CHIRALITY_LENS → _SEMANTIC_LENSING.md   ← lens-register skill
                 Phase 2.5  4_DOCUMENTS Pass 3 (consumes lensing register for enrichment)
```

Downstream consumption:
- **DELIVERABLE_TASK** (interactive) may load `skills/semantic-lensing/` to generate PROPOSAL blocks from the register + optionally update it.
- **4_DOCUMENTS Pass 3** consumes the register for automated enrichment application.

---

## Two acceptable end states

### Staged end state (C pattern) — this session's target

- `agents/AGENT_CHIRALITY_LENS.md` retained as pipeline-stage agent wrapper.
- Method extracted to `skills/lens-register/`.
- Wrapper dispatches TASK+skill internally; ORCHESTRATOR continues to spawn CHIRALITY_LENS externally.
- `AGENTS.md` TASK* wildcard preserves CHIRALITY_LENS.
- Parallel C-pattern for CHIRALITY_FRAMEWORK, 4_DOCUMENTS, DOMAIN_DOCUMENTS.

**Why staged:** Preserves pipeline-stage dispatch identity. Compatible with current ORCHESTRATOR without major refactor. Enables future B promotion as a unit.

**Shell-on-shell indirection is acceptable as migration step.** It is **not** the final normalized architecture. This is called out explicitly per handoff guidance.

### Full normalization end state (B pattern) — deferred

- ORCHESTRATOR Phase 2.3 dispatches TASK with `TaskSkill: semantic-matrix-build` directly.
- ORCHESTRATOR Phase 2.4 dispatches TASK with `TaskSkill: lens-register` directly.
- ORCHESTRATOR Phases 2.2 + 2.5 dispatch TASK with `TaskSkill: four-documents` directly (with pass parameter).
- `agents/AGENT_CHIRALITY_FRAMEWORK.md`, `AGENT_CHIRALITY_LENS.md`, `AGENT_4_DOCUMENTS.md`, `AGENT_DOMAIN_DOCUMENTS.md` all archive.
- `AGENTS.md` TASK* wildcard entries removed for these.
- ORCHESTRATOR `subagents:` frontmatter updated.

**Why deferred:** Full normalization requires migrating the whole PROJECT/SOFTWARE setup pipeline as a unit. Partial B migration (e.g., converting CHIRALITY_LENS alone) produces a mixed architecture where some pipeline stages are named agents and others are TASK+skill dispatches. That mixed architecture is harder to reason about than either all-C or all-B.

**Trigger for full normalization commitment:** A future governance decision that the whole semantic pipeline migrates together, with explicit approval to refactor ORCHESTRATOR's pipeline-dispatch section.

---

## ORCHESTRATOR DOMAIN contradiction (repo defect)

### Defect

`agents/AGENT_ORCHESTRATOR.md` contains contradictory statements about whether DOMAIN runs CHIRALITY_LENS:

**Line ~218 (Phase 2.4 Action):**
> "**DOMAIN_DECOMP:** Skip this phase. DOMAIN variants do not use the semantic lensing pipeline."

**Line ~264-268 (Phase 2.6 DOMAIN_HYPERGRAPH prereqs):**
> "DOMAIN_HYPERGRAPH reads the final state of Category/Knowledge Type folders — after PREPARATION scaffolded them, DOMAIN_DOCUMENTS drafted and enriched them, and the semantic pipeline (CHIRALITY_FRAMEWORK → **CHIRALITY_LENS** → DOMAIN_DOCUMENTS Pass 3) has completed."

Phase 2.4 says DOMAIN skips CHIRALITY_LENS; Phase 2.6 names CHIRALITY_LENS in DOMAIN's dependency chain. These cannot both be correct.

### Fix direction (user ruling required in Slice 2b)

**Option (a): DOMAIN runs CHIRALITY_LENS.**
- Remove "DOMAIN skips" from Phase 2.4.
- Add DOMAIN-specific lensing logic (matrices for DOMAIN Knowledge Types; production documents = KA-*.md + Scoping.md).
- Keep Phase 2.6 DOMAIN_HYPERGRAPH prereqs as-is.

**Option (b): DOMAIN skips CHIRALITY_LENS.**
- Keep Phase 2.4 "DOMAIN skips" statement.
- Remove "CHIRALITY_LENS" from Phase 2.6 DOMAIN dependency chain.
- Update Phase 2.6 DOMAIN_HYPERGRAPH prereqs to reflect only PREPARATION + DOMAIN_DOCUMENTS + CHIRALITY_FRAMEWORK (DOMAIN_DOCUMENTS Pass 3 may still follow FRAMEWORK without lensing).

### Scope of fix

Documentation fix in `agents/AGENT_ORCHESTRATOR.md`. May require companion updates to:
- `agents/AGENT_DOMAIN_HYPERGRAPH.md` (prerequisite documentation)
- `agents/AGENT_DOMAIN_DOCUMENTS.md` (Pass 3 behavior if lensing is absent)
- `agents/AGENT_CHIRALITY_LENS.md` (variant-awareness section — currently mentions DOMAIN; if option b, remove or narrow)

### When to fix

**Before Slice 4 (CHIRALITY_LENS migration)** — ensures the migration plan reflects the correct DOMAIN path. Fix lives in Slice 2b.

---

## C-pattern as staged compatibility layer (explicit)

The C pattern for Type 2 task agents (CHIRALITY_FRAMEWORK, CHIRALITY_LENS, 4_DOCUMENTS, DOMAIN_DOCUMENTS, DEPENDENCIES) is **shell-on-shell indirection**: a Type 2 agent wrapping a TASK+skill dispatch.

This is acceptable as a **migration step** because:
- It preserves the agent's identity as a named dispatch target for pipeline/matrix-cell consumers.
- It extracts the method into a reusable skill that other agents could invoke.
- It avoids the big-bang rewrite of ORCHESTRATOR's pipeline-dispatch section.

It is **not** the final normalized architecture because:
- Type 2 agent wrapping TASK+skill duplicates shell behavior — the wrapper adds no decision rights, no authority surface, no cross-artifact reasoning beyond what TASK provides.
- Operators/agents reading the agent file see a dispatch shim instead of the method itself.
- Two places (agent wrapper + skill) can diverge if not maintained carefully.

**Future normalization path:** when the whole PROJECT/SOFTWARE setup pipeline is ruled for unit migration, the C-wrappers archive and ORCHESTRATOR dispatches TASK+skill directly. At that point the compositional model is uniform: shell + profile + skill + tool + brief, with no intermediate Type 2 wrappers.

---

## Cross-reference to classification

Agents classified as C with skills in this family:

| Agent | Target skill | Pipeline phase |
|---|---|---|
| CHIRALITY_FRAMEWORK | `skills/semantic-matrix-build/` | Phase 2.3 |
| CHIRALITY_LENS | `skills/lens-register/` | Phase 2.4 |
| 4_DOCUMENTS | `skills/four-documents/` (pass modes TBD) | Phases 2.2 + 2.5 |
| DOMAIN_DOCUMENTS | `skills/domain-documents/` | DOMAIN setup phases |
| DEPENDENCIES | `skills/dependency-extract/` | Not in semantic pipeline (matrix cell preservation) |

These are all C for the same reason: **pipeline or matrix-cell identity is load-bearing; method is extractable.**

---

## Change Log

- **2026-04-04:** Initial architecture document. C-pattern staged end state ruled; B-pattern full normalization deferred. ORCHESTRATOR DOMAIN contradiction documented; fix direction deferred to Slice 2b.
