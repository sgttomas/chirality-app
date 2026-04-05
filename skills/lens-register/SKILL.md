---
name: lens-register
description: Generate a matrix-organized, coverage-complete semantic lensing register (_SEMANTIC_LENSING.md) from _SEMANTIC.md + production documents. Setup-pipeline companion to the interactive semantic-lensing skill.
compatibility: Chirality TASK; invoked by CHIRALITY_LENS wrapper during ORCHESTRATOR setup pipeline.
metadata:
  chirality-skill-version: "1"
  chirality-task-profile: NONE
---

# SKILL — lens-register

## Purpose

Produce a **matrix-organized lensing register** (`_SEMANTIC_LENSING.md`) that:

1. Uses **each cell** of each matrix **A, B, C, F, D, X, E** (from `_SEMANTIC.md`) as a **lens** (a "what to look for" perspective),
2. Applies that lens to each of the **production documents**, and
3. Records only **warranted** enrichment inputs (gaps, conflicts, needed questions) with provenance — **without rewriting** the documents.

This output is intended to make follow-on enrichment:
- **auditable** (evidence-linked),
- **minimal** (only what's warranted),
- **safe** (no invention; no conflict resolution by the skill).

This is the **setup-pipeline, coverage-complete** contract in the semantic-lensing family. Its interactive counterpart is `skills/semantic-lensing/`, which consumes this register as a candidate worklist.

## Suitable agent shells

- `TASK` (generic shell mode, no profile)

Typical dispatcher: `CHIRALITY_LENS` wrapper, invoked by ORCHESTRATOR Phase 2.4 (one dispatch per deliverable).

## Inputs

### Required

- `DeliverablePath` (or `deliverable_folder`) — absolute path to one production unit folder

### Optional

- `DECOMP_VARIANT` — `PROJECT` | `SOFTWARE` (default `PROJECT`). DOMAIN is not supported; see QA_CHECKS.md for refusal behavior.

### Files read (deliverable-local)

Required:
- `{deliverable_folder}/_SEMANTIC.md` (source for the lenses — if missing, write blocking header and stop)

Contextual (if missing, degrade with warnings and proceed):
- `{deliverable_folder}/_CONTEXT.md`
- `{deliverable_folder}/_STATUS.md`
- Production documents: `Datasheet.md`, `Specification.md`, `Guidance.md`, `Procedure.md`

Optional:
- `{deliverable_folder}/_REFERENCES.md` (read if present; list pointers but do not expand scope unless explicitly instructed)

## Runtime overrides

| Key | Meaning | Default | Allowed values |
|---|---|---|---|
| `DECOMP_VARIANT` | Variant of decomposition pipeline | `PROJECT` | `PROJECT`, `SOFTWARE` |

## Tool usage

This is a reasoning-only skill. No deterministic tools are required or allowed.

- Preferred tools: none (reasoning-first extraction)
- `allowed-tools` frontmatter field intentionally omitted

Disallowed behavior:
- No writing to any file outside `{deliverable_folder}/_SEMANTIC_LENSING.md`
- No modification of production documents (`Datasheet.md`, `Specification.md`, `Guidance.md`, `Procedure.md`)
- No modification of `_SEMANTIC.md` under any circumstances
- No cross-deliverable scanning or comparison
- No modification of `_STATUS.md` (unless orchestrator later adds a lifecycle state for lensing)

## Outputs

- `{deliverable_folder}/_SEMANTIC_LENSING.md` — overwritten each run

## Non-negotiable invariants

- **One deliverable per run.** Operate on a single deliverable folder only.
- **Read-only on production documents.** You MUST NOT edit any production documents (`Datasheet.md`, `Specification.md`, `Guidance.md`, `Procedure.md`).
- **Use matrices as lenses, not as authority.** Matrices condition what to look for; they do not justify inventing content.
- **No invention.** If information is not present in the production documents (or other explicitly read deliverable-local files), record it as `Type=TBD_Question` rather than asserting it.
- **Provenance is mandatory.** Every warranted item must include `SourcePath` and best-effort `SectionRef` (use "location TBD" if needed).
- **Conflicts are surfaced, not resolved.** When documents disagree, create `Type=Conflict` and leave `HumanRuling = TBD`.
- **No recursive ingestion.** Do not treat `_SEMANTIC_LENSING.md` as an input source for subsequent runs unless explicitly instructed.
- **Matrix coverage is complete.** Every cell in each of A, B, C, F, D, X, E MUST appear in the **Lens Coverage** table (even if it yields no warranted items).
- **Do not force verbosity.** If documents are already consistent and complete under a lens, record `CoverageStatus=NO_ITEMS` for that lens and move on.
- **Avoid restatement.** Do not emit items that merely repeat what is already clear and consistent across documents.
- **Preserve document-role boundaries (non-authoritative placement guidance):** When proposing where to apply a future enrichment, prefer placement by document role:
  - normative content (requirements, acceptance criteria) → `Specification.md`
  - operational content (prerequisites, steps, checks) → `Procedure.md`
  - directional content (rationale, tradeoffs, interpretation) → `Guidance.md`
  - descriptive content (parameters, enumerations, identifiers) → `Datasheet.md`
  This is a suggestion signal only; it does not authorize edits.

## Precedence (conflict resolution)

1. **PROTOCOL** governs sequencing and run behavior.
2. **SPEC** governs validity (what counts as warranted + how it must be recorded).
3. **STRUCTURE** defines register schema and output format.
4. **RATIONALE** governs interpretation when ambiguity remains.

If any instruction appears to conflict, flag the conflict and return it to the invoker.

## Glossary

- **Lens (matrix cell):** the atomic semantic unit in a matrix cell (e.g., `A[normative, guiding]`) used as a "what to look for" perspective.
- **LensKey:** canonical identifier for a lens cell: `M:[RowLabel]:[ColLabel]`.
- **Warranted item:** a gap/conflict/question that is actionable for a later enrichment pass, grounded by evidence or explicit absence.
- **Production Documents:** `Datasheet.md`, `Specification.md`, `Guidance.md`, `Procedure.md`.

---

## PROTOCOL — Straight-through Lensing Procedure

### Step 0 — Safety checks

1. Confirm `{deliverable_folder}` exists and is readable.
2. If `DECOMP_VARIANT=DOMAIN` is passed: refuse gracefully (see QA_CHECKS.md for refusal behavior). DOMAIN pipelines skip the semantic lensing step.
3. Confirm `_SEMANTIC.md` exists.
   - If missing: write `_SEMANTIC_LENSING.md` with a blocking header ("Missing _SEMANTIC.md; run CHIRALITY_FRAMEWORK first") and stop.
4. Confirm production documents exist.
   - If one or more are missing: do **not** fail the run. Record `[WARNING] MISSING_DOC: <filename>` in the output header and proceed with available docs.

### Step 1 — Read context + inputs

Read, in order:
1. `_CONTEXT.md` (deliverable identity + description)
2. `_STATUS.md` (record current state; do not change it)
3. `_SEMANTIC.md` (extract matrices A, B, C, F, D, X, E)
4. The production documents that exist (`Datasheet.md`, `Specification.md`, `Guidance.md`, `Procedure.md`)
5. `_REFERENCES.md` (if present; list but do not expand scope unless told)

### Step 2 — Parse matrices into a lens inventory (coverage scaffold)

For each matrix `M ∈ {A, B, C, F, D, X, E}` in `_SEMANTIC.md`:

- Extract:
  - matrix name
  - row labels (in order)
  - column labels (in order)
  - cell values (atomic semantic units)

- Construct a **Lens Coverage** row for every cell (row-major, deterministic):
  - `LensKey = M:[RowLabel]:[ColLabel]`
  - `LensValue = cell value`
  - Initialize `ItemCount=0`
  - Initialize `CoverageStatus=NO_ITEMS`

If a matrix cell is empty or malformed:
- Set `CoverageStatus=MATRIX_ERROR` for that `LensKey`,
- Add a `Type=MatrixError` warranted item referencing `_SEMANTIC.md`,
- Continue (do not fail the run).

### Step 3 — Apply lenses to the production documents and record warranted items

For each `LensKey` in the lens inventory:

1. **Scan** the production documents and ask: "What becomes salient under this lens?"
2. Record only what meets the warranted threshold (below).
3. Update the Lens Coverage row (`ItemCount`, `CoverageStatus`) accordingly.

**Warranted threshold (tight filter):** create an item only when at least one is true:

- `Conflict`: two+ documents (or two+ locations) make incompatible claims about the same thing (include contenders).
- `VerificationGap`: a normative requirement exists but acceptance/verification is missing or ambiguous.
- `MissingSlot`: a category suggested by the lens is absent where it would reasonably belong (record as absence; do not invent content).
- `WeakStatement`: language is materially ambiguous/vague in a way that could change implementation decisions.
- `RationaleGap`: a decision/requirement exists without enough explanation to interpret safely (prefer Guidance as suggested placement).
- `Normalization`: terminology or naming is inconsistent across documents in a way that risks drift.
- `TBD_Question`: a necessary input is missing and must be sourced externally or from references.

**How to write `CandidateInfo` (enrichment-ready, non-destructive):**
- Phrase as a minimal *additive* suggestion (e.g., "Add acceptance criteria for …", "Clarify definition of …", "Record TBD: …").
- Do not draft full paragraphs.
- Do not introduce new numeric values or "shall" requirements unless they already exist and you are only pointing to the gap.

**Provenance for absence (`MissingSlot`):**
- `SourcePath` must include the doc(s) you searched.
- `SectionRef` can be:
  - a specific heading where it would belong, or
  - `entire document scanned` if no better anchor exists.

**Conflict handling:**
- Populate `Contenders` with two+ `path#section` entries.
- Set `HumanRuling=TBD` (unless a human ruling exists elsewhere and you can cite it).

### Step 4 — Write `_SEMANTIC_LENSING.md`

Write/overwrite `{deliverable_folder}/_SEMANTIC_LENSING.md` using the schema in STRUCTURE.

### Step 5 — Report completion (to invoker)

Report:
- Deliverable ID/name
- Whether `_SEMANTIC.md` was present and parsed
- Count of warranted items (total + by document + by matrix)
- Any matrix parsing errors, missing docs, or severe conflicts detected

---

## SPEC — Validity Requirements

### S1 — Coverage completeness

A run is valid only if:
- Every cell of every matrix A, B, C, F, D, X, E is processed as a lens, and
- `_SEMANTIC_LENSING.md` includes a **Lens Coverage** entry for each `LensKey` with:
  - `CoverageStatus` (`NO_ITEMS|HAS_ITEMS|MATRIX_ERROR`), and
  - `ItemCount` (0 permitted).

### S2 — No-invention constraint

A recorded warranted item must be one of:
- Gap / normalization / weak-statement item with provenance, or
- A conflict grounded in at least two cited contenders, or
- A question-to-answer (`Type=TBD_Question`) with rationale and where to look.

No speculation or baseless assumptions. Use `TBD` instead, to draw the human's attention.

### S3 — Provenance constraint

Every warranted item MUST include:
- `SourcePath` (file path(s)), and
- best-effort `SectionRef` (heading anchor; or `location TBD` / `entire document scanned`).

### S4 — Human decision rights preserved

The skill MUST NOT:
- Choose a "winner" when sources conflict
- Introduce new requirements or numeric values
- Claim compliance with a standard whose text is not present

Instead:
- Capture conflict items with `HumanRuling = TBD`
- Capture questions with a clear "who/what to consult"

### S5 — Output stability

The output must be:
- deterministically structured (stable ordering),
- easy for a future agent to consume,
- consistent with STRUCTURE tables (no alternate table formats).

---

## STRUCTURE — Output File Schema (`_SEMANTIC_LENSING.md`)

### File header (required)

```markdown
# Semantic Lensing Register: [Production Unit ID] [Name]

**Generated:** [YYYY-MM-DD]
**Deliverable Folder:** [path]
**Warnings:** [optional; e.g., MISSING_DOC, MATRIX_ERROR]

**Inputs Read:**
- _CONTEXT.md — [SourceRef]
- _STATUS.md — [SourceRef]
- _SEMANTIC.md — [SourceRef]
- Datasheet.md — [SourceRef or "missing"]
- Specification.md — [SourceRef or "missing"]
- Guidance.md — [SourceRef or "missing"]
- Procedure.md — [SourceRef or "missing"]
- _REFERENCES.md — [SourceRef or "not present / not read"]

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.
```

### Summary block (required)

```markdown
## Summary

- Total warranted items: N
- By document:
  - Datasheet: n
  - Specification: n
  - Guidance: n
  - Procedure: n
- By matrix:
  - A: n  B: n  C: n  F: n  D: n  X: n  E: n
- By type:
  - Conflict: n
  - VerificationGap: n
  - MissingSlot: n
  - WeakStatement: n
  - RationaleGap: n
  - Normalization: n
  - TBD_Question: n
  - MatrixError: n
- Notable conflicts: n
- Matrix parse errors: n
```

### Matrix sections (required)

For each matrix M in this order: **A, B, C, F, D, X, E**:

```markdown
## Matrix M — [Matrix Name]

### Lens Coverage (required)
| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| M:[r]:[c] | r | c | ... | 0 | NO_ITEMS | ... |

CoverageStatus enum:
- NO_ITEMS
- HAS_ITEMS
- MATRIX_ERROR

### Warranted Items (only if any exist for this matrix)
| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:[r]:[c] | VerificationGap | Specification | Specification | Add acceptance criteria for ... | ... | ... | ... | ... | ... | TBD |
```

#### Column requirements (Warranted Items)

- `ItemID`: unique within the file (recommend `A-001`, `A-002`, ..., then `B-001`, etc.)
- `LensKey`: `M:[RowLabel]:[ColLabel]`
- `Type` (enum):
  - `MissingSlot`
  - `WeakStatement`
  - `Conflict`
  - `VerificationGap`
  - `RationaleGap`
  - `Normalization`
  - `TBD_Question`
  - `MatrixError`
- `AppliesToDoc`: where the issue is observed (`Datasheet` | `Specification` | `Guidance` | `Procedure` | `Multi` | `NA`)
- `SuggestedEditDoc`: where a later enrichment pass should *prefer* to place the fix (same filename convention | `Multi` | `TBD`)
- `CandidateInfo`: short, enrichment-ready phrasing (not full prose); may include "TBD: …" question wording
- `WhyWarranted`: 1–2 sentences explaining gap/conflict/leverage
- `SourcePath`: file path(s)
- `SectionRef`: best-effort headings; use "location TBD" or "entire document scanned" if needed
- `Contenders`: only for conflicts; include two+ `path#section` entries
- `ProposedAuthority`: PROPOSAL only; never authoritative
- `HumanRuling`: always `TBD` unless a human has already ruled elsewhere (then cite where)

#### SuggestedEditDoc heuristic (non-authoritative)

Use the least-surprising placement guidance. Typical mappings:
- `VerificationGap` → `Specification` (and/or `Procedure` if the missing item is an execution check)
- `RationaleGap` → `Guidance`
- `Normalization` → usually `Guidance` (vocabulary note) + wherever the term appears
- `WeakStatement` → same doc where it appears, unless it belongs elsewhere by role
- `MissingSlot` → `TBD` or best-fit doc role
- `Conflict` / `TBD_Question` / `MatrixError` → `NA` or `TBD` as applicable

### SourceRef convention

Use file path + best-effort heading anchors (or "location TBD") to record provenance. You are recording traceability, not claiming these sources "prove" the matrices.

---

## RATIONALE — Why this skill exists

- **Bridges semantic partitions to document enrichment.** `_SEMANTIC.md` provides structured semantic partitions; lensing translates that into actionable enrichment targets for the production documents.
- **Reduces drift without rewriting.** The register captures only what is warranted, avoiding restatement and minimizing semantic churn.
- **Protects human authority.** Conflicts and consequential choices are surfaced for human ruling; the skill does not decide.
- **Improves rerunnability.** When documents evolve, the register can be regenerated to reflect current gaps and conflicts with stable coverage accounting.

**Value hierarchy:**
1. Provenance + no invention
2. Cross-document consistency support
3. Coverage completeness across all matrix cells
4. Density and usability of `CandidateInfo` for downstream enrichment

## QA expectations

See `QA_CHECKS.md` for the full invariant list and refusal behavior.

## See also

- `skills/semantic-lensing/SKILL.md` — interactive proposal workflow consuming the register
- `agents/AGENT_CHIRALITY_LENS.md` — wrapper dispatching this skill via ORCHESTRATOR Phase 2.4
- `plans/SEMANTIC_PIPELINE_ARCHITECTURE.md` — two-contract architecture
