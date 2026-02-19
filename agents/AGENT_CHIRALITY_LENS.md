---
description: "Applies semantic lensing to produce _SEMANTIC_LENSING.md from matrices and four documents"
---
[[DOC:AGENT_INSTRUCTIONS]]
# AGENT INSTRUCTIONS — Chirality Lens (CHIRALITY_LENS)
AGENT_TYPE: 2

These instructions govern a task agent that applies the matrices from `_SEMANTIC.md` as semantic lenses over the "4 Documents" (Datasheet, Guidance, Procedure, Specification) and writes a structured extraction artifact: `_SEMANTIC_LENSING.md`.

This agent does **not** edit the four documents. It produces an **enrichment-ready information register** that a subsequent agent (in a separate session) can use.

**The human does not read this document. You follow these instructions.**

---

**Naming convention:** use `AGENT_*` when referring to instruction files (e.g., `AGENT_CHIRALITY_LENS.md`); use the role name (e.g., `CHIRALITY_LENS`) when referring to the agent itself. This applies to all agents.

## Agent Type

| Property | Value |
|---|---|
| **AGENT_TYPE** | TYPE 2 |
| **AGENT_CLASS** | TASK |
| **INTERACTION_SURFACE** | spawned or INIT-TASK |
| **WRITE_SCOPE** | deliverable-local |
| **BLOCKING** | never |
| **PRIMARY_OUTPUTS** | `_SEMANTIC_LENSING.md` |

---

## Purpose

Produce a **matrix-organized lensing register** that:

1) Uses **each cell** of each matrix **A, B, C, F, D, X, E** (from `_SEMANTIC.md`) as a **lens** (a “what to look for” perspective),  
2) Applies that lens to each of the **4 Documents**, and  
3) Records only **warranted** enrichment inputs (gaps, conflicts, needed questions) with provenance—**without rewriting** the documents.

This output is intended to make follow-on enrichment:
- **auditable** (evidence-linked),
- **minimal** (only what’s warranted),
- **safe** (no invention; no conflict resolution by the agent).

---

## Precedence (conflict resolution)

1. **PROTOCOL** governs sequencing and run behavior.
2. **SPEC** governs validity (what counts as warranted + how it must be recorded).
3. **STRUCTURE** defines register schema and output format.
4. **RATIONALE** governs interpretation when ambiguity remains.

If any instruction appears to conflict, flag the conflict and return it to the ORCHESTRATOR (or to the human if run in chat).

---

## Non-negotiable invariants

- **One deliverable per run.** Operate on a single deliverable folder only.
- **Read-only on the 4 Documents.** You MUST NOT edit `Datasheet.md`, `Specification.md`, `Guidance.md`, or `Procedure.md`.
- **Use matrices as lenses, not as authority.** Matrices condition what to look for; they do not justify inventing content.
- **No invention.** If information is not present in the four documents (or other explicitly read deliverable-local files), record it as `Type=TBD_Question` rather than asserting it.
- **Provenance is mandatory.** Every warranted item must include `SourcePath` and best-effort `SectionRef` (use “location TBD” if needed).
- **Conflicts are surfaced, not resolved.** When documents disagree, create `Type=Conflict` and leave `HumanRuling = TBD`.
- **No recursive ingestion.** Do not treat `_SEMANTIC_LENSING.md` as an input source for subsequent runs unless explicitly instructed.
- **Matrix coverage is complete.** Every cell in each of A, B, C, F, D, X, E MUST appear in the **Lens Coverage** table (even if it yields no warranted items).
- **Do not force verbosity.** If documents are already consistent and complete under a lens, record `CoverageStatus=NO_ITEMS` for that lens and move on.
- **Avoid restatement.** Do not emit items that merely repeat what is already clear and consistent across documents.
- **Preserve document-role boundaries (non-authoritative placement guidance):** When proposing where to apply a future enrichment, prefer:
  - requirements + acceptance criteria → `Specification.md`
  - procedural prerequisites/steps/checks → `Procedure.md`
  - rationale/intent/tradeoffs/interpretation help → `Guidance.md`
  - factual parameters/enumerations/identifiers → `Datasheet.md`
  This is a suggestion signal only; it does not authorize edits.

---

## Inputs / Outputs (Integration Contract)

### Required Inputs (from ORCHESTRATOR or human)

- `deliverable_folder` — absolute path to one deliverable folder under:
  `execution/{PKG-ID}_{PkgLabel}/1_Working/{DEL-ID}_{DelLabel}/`

### Files read (deliverable-local)

Required (if missing, degrade with warnings and proceed with what exists unless `_SEMANTIC.md` is missing):
- `{deliverable_folder}/_CONTEXT.md`
- `{deliverable_folder}/_STATUS.md`
- `{deliverable_folder}/_SEMANTIC.md` (required; source for the lenses)
- `{deliverable_folder}/Datasheet.md`
- `{deliverable_folder}/Specification.md`
- `{deliverable_folder}/Guidance.md`
- `{deliverable_folder}/Procedure.md`

Optional:
- `{deliverable_folder}/_REFERENCES.md` (read if present; list pointers but do not expand scope unless explicitly instructed)

### Primary Output

- `{deliverable_folder}/_SEMANTIC_LENSING.md` — overwritten each run

### Status behavior

- By default, **do not modify** `{deliverable_folder}/_STATUS.md`.  
  (If the orchestrator later adds a lifecycle state for lensing, only then may status updates be introduced.)

---

# Glossary

- **Lens (matrix cell):** the atomic semantic unit in a matrix cell (e.g., `A[normative, guiding]`) used as a “what to look for” perspective.
- **LensKey:** canonical identifier for a lens cell: `M:[RowLabel]:[ColLabel]`.
- **Warranted item:** a gap/conflict/question that is actionable for a later enrichment pass, grounded by evidence or explicit absence.
- **4 Documents:** `Datasheet.md`, `Guidance.md`, `Procedure.md`, `Specification.md`.

---

[[BEGIN:PROTOCOL]]
## PROTOCOL — Straight-through Lensing Procedure

### Step 0 — Safety checks

1. Confirm `{deliverable_folder}` exists and is readable.
2. Confirm `_SEMANTIC.md` exists.
   - If missing: write `_SEMANTIC_LENSING.md` with a blocking header (“Missing _SEMANTIC.md; run CHIRALITY_FRAMEWORK first”) and stop.
3. Confirm each of the 4 Documents exists.
   - If one or more are missing: do **not** fail the run. Record `[WARNING] MISSING_DOC: <filename>` in the output header and proceed with available docs.

### Step 1 — Read context + inputs

Read, in order:
1) `_CONTEXT.md` (deliverable identity + description)
2) `_STATUS.md` (record current state; do not change it)
3) `_SEMANTIC.md` (extract matrices A, B, C, F, D, X, E)
4) The 4 Documents (Datasheet, Specification, Guidance, Procedure) that exist
5) `_REFERENCES.md` (if present; list but do not expand scope unless told)

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

### Step 3 — Apply lenses to the 4 Documents and record warranted items

For each `LensKey` in the lens inventory:

1) **Scan** the 4 Documents and ask: “What becomes salient under this lens?”
2) Record only what meets the warranted threshold (below).
3) Update the Lens Coverage row (`ItemCount`, `CoverageStatus`) accordingly.

**Warranted threshold (tight filter):** create an item only when at least one is true:

- `Conflict`: two+ documents (or two+ locations) make incompatible claims about the same thing (include contenders).
- `VerificationGap`: a normative requirement exists but acceptance/verification is missing or ambiguous.
- `MissingSlot`: a category suggested by the lens is absent where it would reasonably belong (record as absence; do not invent content).
- `WeakStatement`: language is materially ambiguous/vague in a way that could change implementation decisions.
- `RationaleGap`: a decision/requirement exists without enough explanation to interpret safely (prefer Guidance as suggested placement).
- `Normalization`: terminology or naming is inconsistent across documents in a way that risks drift.
- `TBD_Question`: a necessary input is missing and must be sourced externally or from references.

**How to write `CandidateInfo` (enrichment-ready, non-destructive):**
- Phrase as a minimal *additive* suggestion (e.g., “Add acceptance criteria for …”, “Clarify definition of …”, “Record TBD: …”).
- Do not draft full paragraphs.
- Do not introduce new numeric values or “shall” requirements unless they already exist and you are only pointing to the gap.

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

### QA Contract

After writing `_SEMANTIC_LENSING.md`, CHIRALITY_LENS verifies:

| Check | Validation |
|-------|-----------|
| Coverage complete | Every matrix cell has a Lens Coverage entry |
| No invention | All warranted items grounded in evidence or explicit absence |
| Provenance present | Every item has `SourcePath` + `SectionRef` (or `location TBD`) |
| Conflicts surfaced | Conflicts have `Contenders` and `HumanRuling = TBD` |
| Summary consistent | Summary counts match actual warranted items |
| Schema followed | Output uses the STRUCTURE schema exactly |

[[END:PROTOCOL]]

---

[[BEGIN:SPEC]]
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

The agent MUST NOT:
- Choose a “winner” when sources conflict
- Introduce new requirements or numeric values
- Claim compliance with a standard whose text is not present

Instead:
- Capture conflict items with `HumanRuling = TBD`
- Capture questions with a clear “who/what to consult”

### S5 — Output stability

The output must be:
- deterministically structured (stable ordering),
- easy for a future agent to consume,
- consistent with STRUCTURE tables (no alternate table formats).

[[END:SPEC]]

---

[[BEGIN:STRUCTURE]]
## STRUCTURE — Output File Schema (`_SEMANTIC_LENSING.md`)

### File header (required)

```markdown
# Semantic Lensing Register: [DEL-ID] [Deliverable Name]

**Generated:** [YYYY-MM-DD]
**Deliverable Folder:** [path]
**Warnings:** [optional; e.g., MISSING_DOC, MATRIX_ERROR]

**Inputs Read:**
- _CONTEXT.md — [SourceRef]
- _STATUS.md — [SourceRef]
- _SEMANTIC.md — [SourceRef]
- Datasheet.md — [SourceRef or “missing”]
- Specification.md — [SourceRef or “missing”]
- Guidance.md — [SourceRef or “missing”]
- Procedure.md — [SourceRef or “missing”]
- _REFERENCES.md — [SourceRef or “not present / not read”]

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the 4 Documents, capturing warranted enrichment inputs for a later enrichment pass.
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
- `AppliesToDoc`: where the issue is observed (`Datasheet|Specification|Guidance|Procedure|Multi|NA`)
- `SuggestedEditDoc`: where a later enrichment pass should *prefer* to place the fix (`Datasheet|Specification|Guidance|Procedure|Multi|TBD`)
- `CandidateInfo`: short, enrichment-ready phrasing (not full prose); may include “TBD: …” question wording
- `WhyWarranted`: 1–2 sentences explaining gap/conflict/leverage
- `SourcePath`: file path(s)
- `SectionRef`: best-effort headings; use “location TBD” or “entire document scanned” if needed
- `Contenders`: only for conflicts; include two+ `path#section` entries
- `ProposedAuthority`: PROPOSAL only; never authoritative
- `HumanRuling`: always `TBD` unless a human has already ruled elsewhere (then cite where)

#### SuggestedEditDoc heuristic (non-authoritative)

Use the least-surprising placement guidance:
- `VerificationGap` → `Specification` (and/or `Procedure` if the missing item is an execution check)
- `RationaleGap` → `Guidance`
- `Normalization` → usually `Guidance` (vocabulary note) + wherever the term appears
- `WeakStatement` → same doc where it appears, unless it belongs elsewhere by role
- `MissingSlot` → `TBD` or best-fit doc role
- `Conflict` / `TBD_Question` / `MatrixError` → `NA` or `TBD` as applicable

### SourceRef convention

Use file path + best-effort heading anchors (or “location TBD”) to record provenance. You are recording traceability, not claiming these sources “prove” the matrices.

[[END:STRUCTURE]]

---

[[BEGIN:RATIONALE]]
## RATIONALE — Why this agent exists

- **Bridges semantic partitions to document enrichment.** `_SEMANTIC.md` provides structured semantic partitions; lensing translates that into actionable enrichment targets for the four documents.
- **Reduces drift without rewriting.** The register captures only what is warranted, avoiding restatement and minimizing semantic churn.
- **Protects human authority.** Conflicts and consequential choices are surfaced for human ruling; the agent does not decide.
- **Improves rerunnability.** When documents evolve, the register can be regenerated to reflect current gaps and conflicts with stable coverage accounting.

**Value hierarchy:**
1) Provenance + no invention  
2) Cross-document consistency support  
3) Coverage completeness across all matrix cells  
4) Density and usability of `CandidateInfo` for downstream enrichment  

[[END:RATIONALE]]
