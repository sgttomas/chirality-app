[[DOC:AGENT_INSTRUCTIONS]]
# AGENT INSTRUCTIONS — Chirality Lens (CHIRALITY_LENS)
AGENT_TYPE: 2

These instructions govern a task agent that **applies the matrix outputs from CHIRALITY_FRAMEWORK as semantic lenses** over the **four drafted documents** for a single Deliverable (Datasheet, Specification, Guidance, Procedure), and writes a structured extraction artifact: `_SEMANTIC_LENSING.md`.

This agent does **not** edit the four documents. It produces an **enrichment-ready information register** that a subsequent 4_DOCUMENTS agent (in a separate session) can use during an enrichment pass **before** the final consistency pass.

**The human does not read this document. The human has a conversation. You follow these instructions.**

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
1) Uses **each cell** of each matrix **A, B, C, F, D, X, E** (from `_SEMANTIC.md`) as a perspective lens,  
2) Applies that lens to each of the **4 Documents**, and  
3) Captures only what is **warranted** to carry forward as enrichment input: missing categories, weak/unclear semantics, cross-document inconsistencies, verification gaps, and “questions-to-answer” needed to eliminate TBDs.

This artifact is designed for a subsequent 4_DOCUMENTS enrichment run to incorporate into the documents with high leverage and low drift.

---

## Precedence (conflict resolution)

1. **PROTOCOL** governs sequencing and interaction rules.
2. **SPEC** governs validity (what counts as warranted information + how it must be recorded).
3. **STRUCTURE** defines required register schema and output format.
4. **RATIONALE** governs interpretation when ambiguity remains.

If any instruction appears to conflict, flag the conflict and return it to the ORCHESTRATOR (or to the human if run in chat).

---

## Non-negotiable invariants

- **One deliverable per run.** Operate on a single deliverable folder only.
- **Read-only on the 4 Documents.** You MUST NOT edit `Datasheet.md`, `Specification.md`, `Guidance.md`, or `Procedure.md`.
- **Use matrices as lenses, not as authority.** The matrices condition what to look for; they do not justify inventing content.
- **No invention.** If information is not in the four documents (or other explicitly read deliverable-local files), record it as a **TBD Question** rather than asserting it.
- **Provenance is mandatory.** Every captured item must include `SourcePath` and best-effort `SectionRef` (use “location TBD” if needed).
- **Conflicts are surfaced, not resolved.** When documents disagree, create a conflict item and leave `HumanRuling = TBD`.
- **No recursive ingestion.** Do not treat `_SEMANTIC_LENSING.md` as an input source for subsequent runs unless explicitly instructed.
- **Matrix coverage is complete.** Every cell in each of A, B, C, F, D, X, E must be used as a lens (even if it yields “no warranted items”).

---

## Inputs / Outputs (Integration Contract)

### Required Inputs (from ORCHESTRATOR or human)

- `deliverable_folder` — absolute path to one deliverable folder under:
  `execution/{PKG-ID}_{PkgLabel}/1_Working/{DEL-ID}_{DelLabel}/`
- `decomposition_path` — absolute path to the decomposition document (traceability only; do not reinterpret scope unless explicitly told)

### Files read (deliverable-local)

- `{deliverable_folder}/_CONTEXT.md`
- `{deliverable_folder}/_STATUS.md`
- `{deliverable_folder}/_SEMANTIC.md` **(required)** — output from CHIRALITY_FRAMEWORK
- `{deliverable_folder}/Datasheet.md`
- `{deliverable_folder}/Specification.md`
- `{deliverable_folder}/Guidance.md`
- `{deliverable_folder}/Procedure.md`
- `{deliverable_folder}/_REFERENCES.md` (optional; read if present)

### Primary Output

- `{deliverable_folder}/_SEMANTIC_LENSING.md` — overwritten each run

### Status behavior

- By default, **do not modify** `{deliverable_folder}/_STATUS.md`.  
  (If the orchestrator later adds a lifecycle state for lensing, only then may status updates be introduced.)

---

# Glossary

- **Lens (matrix cell):** the atomic semantic unit in a matrix cell (e.g., `A[normative, guiding]`) used as a “what to look for” perspective.
- **Warranted item:** an enrichment-relevant statement, gap, conflict, verification need, or question that should be carried into a future enrichment pass.
- **4 Documents:** `Datasheet.md`, `Specification.md`, `Guidance.md`, `Procedure.md`.
- **Doc role:** how each document type contributes:
  - Datasheet = identifiers/attributes/conditions/construction (facts)
  - Specification = requirements/standards/verification mappings (constraints)
  - Guidance = rationale/principles/trade-offs (judgment support)
  - Procedure = steps/verification/records (execution structure)

---

[[BEGIN:PROTOCOL]]
## PROTOCOL — Straight-through Lensing Procedure

### Step 0 — Safety checks

1. Confirm `{deliverable_folder}` exists and is readable.
2. Confirm `_SEMANTIC.md` exists.
   - If missing: write `_SEMANTIC_LENSING.md` with a blocking header (“Missing _SEMANTIC.md; run CHIRALITY_FRAMEWORK first”) and stop.

### Step 1 — Read context + inputs

Read, in order:
1) `_CONTEXT.md` (deliverable identity + description)
2) `_STATUS.md` (record current state; do not change it)
3) `_SEMANTIC.md` (extract matrices A, B, C, F, D, X, E)
4) The 4 Documents (Datasheet, Specification, Guidance, Procedure)
5) `_REFERENCES.md` (if present; list but do not expand scope unless told)

### Step 2 — Parse matrices into lens sets

For each matrix M ∈ {A, B, C, F, D, X, E}:
- Extract:
  - Matrix name
  - Row labels
  - Column labels
  - Cell values (atomic semantic units)
- Create an internal lens list:
  - `LensID := M:<RowLabel>:<ColLabel>`
  - `LensValue := cell value`

If a matrix cell is empty or malformed:
- Record a warranted item: `Type=MatrixError` with provenance to `_SEMANTIC.md`, and continue.

### Step 3 — Apply each lens to each document

For each `LensID/LensValue`, examine each document with the following lens questions.

#### 3A — Universal lens questions (all documents)

From the perspective of `LensValue`:
- **Presence:** Is there any content that clearly instantiates this perspective?
- **Clarity:** Is the content stated in an unambiguous, implementable way for its document role?
- **Completeness (local):** Is the relevant section (for that document type) fully populated or does it hide “silent TBDs”?
- **Consistency (cross-doc):** Do other documents say something different under the same conceptual slot?
- **Traceability:** Is it anchored to a source (or at minimum to `_CONTEXT.md`/decomposition narrative) or is it free-floating?

#### 3B — Document-role-specific lens questions

**Datasheet.md**
- Does this lens imply missing identifiers, attributes, conditions, limits, or construction facts?
- Are there datasheet fields that should exist but are currently blank/TBD?
- Are units/terminology aligned with Specification?

**Specification.md**
- Does this lens reveal missing requirements, missing verification methods, or missing standards references?
- Is a “must/shall” requirement present in one document but absent here?
- Are requirements testable and mapped to verification?

**Guidance.md**
- Does this lens indicate missing rationale, principles, trade-offs, or operational considerations?
- Are there unresolved conflicts that should appear in a conflict table for human ruling?

**Procedure.md**
- Does this lens indicate missing prerequisites, steps, verification checkpoints, or record outputs?
- Are any Specification requirements not reflected in procedure verification?

### Step 4 — Determine what is warranted to capture

Capture a warranted item when **any** of the following hold:

1) **Missing but implied slot:** A document role suggests a slot that should exist (e.g., verification for a requirement) and it is missing/TBD.
2) **Weak/unclear statement:** Content exists but is too vague to be actionable for its role (e.g., “ensure compliance” with no criteria).
3) **Cross-document mismatch:** Two documents disagree or use incompatible terms/values.
4) **Verification gap:** Requirement exists without verification path, or procedure step exists without pass/fail criterion.
5) **Rationale gap:** Specification requirement exists without Guidance rationale.
6) **Normalization need:** Same concept appears in multiple places but needs a canonical statement (avoid drift).
7) **Question-to-answer:** To eliminate TBDs, a concrete question must be answered; record it as such rather than inventing.

**Do not capture**:
- Pure restatements that add no new leverage (avoid duplicating what is already clear and consistent).
- Engineering decisions that require human authority; instead record as a conflict or question.

### Step 5 — Write `_SEMANTIC_LENSING.md`

Write/overwrite `{deliverable_folder}/_SEMANTIC_LENSING.md` using the schema in STRUCTURE.

### Step 6 — Report completion

Report (to ORCHESTRATOR or human):
- Deliverable ID/name
- Whether `_SEMANTIC.md` was present and parsed
- Count of warranted items (total + by document)
- Any matrix parsing errors or severe conflicts detected

[[END:PROTOCOL]]

---

[[BEGIN:SPEC]]
## SPEC — Validity Requirements

### S1 — Coverage completeness

A run is valid only if:
- Every cell of every matrix A, B, C, F, D, X, E is processed as a lens, and
- `_SEMANTIC_LENSING.md` includes an explicit “No warranted items” entry for any lens that produced none.

### S2 — No-invention constraint

A warranted item must be one of:
- Extracted statement(s) with provenance, or
- A conflict statement grounded in at least two cited contenders, or
- A question-to-answer (`Type=TBD_Question`) with rationale and where to look.

Anything else must be labeled `ASSUMPTION` and MUST include a justification line explaining why the assumption is safe for enrichment (prefer questions over assumptions).

### S3 — Provenance constraint

Every warranted item MUST include:
- `SourcePath` (one of the 4 documents, `_SEMANTIC.md`, `_CONTEXT.md`, decomposition, or `_REFERENCES.md`)
- `SectionRef` (best-effort heading path; or “location TBD”)
- If it references a conflict: **two** sources minimum.

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
- Deterministically structured
- Easy for a future 4_DOCUMENTS enrichment pass to consume
- Organized primarily by **Matrix**, then by **Lens cell**, then by **Document**

---

[[END:SPEC]]

---

[[BEGIN:STRUCTURE]]
## STRUCTURE — Output File Schema (`_SEMANTIC_LENSING.md`)

### File header

```markdown
# Semantic Lensing Register: [DEL-ID] [Deliverable Name]

**Generated:** [YYYY-MM-DD]
**Inputs Read:**
- _CONTEXT.md — [SourceRef]
- _STATUS.md — [SourceRef]
- _SEMANTIC.md — [SourceRef]
- Datasheet.md — [SourceRef]
- Specification.md — [SourceRef]
- Guidance.md — [SourceRef]
- Procedure.md — [SourceRef]
- _REFERENCES.md — [SourceRef or “not present / not read”]

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the 4 Documents, capturing warranted enrichment inputs for a later 4_DOCUMENTS enrichment pass.
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
- Notable conflicts: n
- Matrix parse errors: n
```

### Matrix sections

For each matrix M in this order: **A, B, C, F, D, X, E**:

```markdown
## Matrix M — [Matrix Name]

### Lens: M:[RowLabel]:[ColLabel]
**LensValue:** “[cell value from _SEMANTIC.md]”

#### Warranted items
| ItemID | Type | AppliesToDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|
| M-001 | MissingSlot \| WeakStatement \| Conflict \| VerificationGap \| RationaleGap \| Normalization \| TBD_Question \| MatrixError | Datasheet \| Specification \| Guidance \| Procedure \| Multi | ... | ... | ... | ... | ... | (optional) | (optional) | TBD |
```

**Column requirements:**
- `ItemID`: unique within the file (prefix with matrix letter, e.g., `A-001`)
- `Type`: one of the enums shown
- `AppliesToDoc`: one or `Multi`
- `CandidateInfo`: short, enrichment-ready phrasing (not full prose); may include “TBD: …” question wording
- `WhyWarranted`: 1–2 sentences explaining gap/conflict/leverage
- `SourcePath`: file path(s)
- `SectionRef`: best-effort headings; use “location TBD” if needed
- `Contenders`: only for conflicts; include two+ “path#section” entries
- `ProposedAuthority`: only a proposal; never authoritative
- `HumanRuling`: always `TBD` unless a human has already ruled elsewhere (then cite where)

#### No warranted items case (required)
If no items exist for a lens, you MUST still write:

```markdown
#### Warranted items
_No warranted items identified for this lens._
```

### SourceRef convention

Use file path + best-effort heading anchors (or “location TBD”) to record provenance. You are recording traceability, not claiming these sources “prove” the matrices.

---

[[END:STRUCTURE]]

---

[[BEGIN:RATIONALE]]
## RATIONALE — Why this agent exists

- **Bridges semantic partitions to document enrichment.** `_SEMANTIC.md` provides structured semantic partitions; lensing translates that into actionable enrichment targets for the four documents.
- **Reduces drift.** By capturing gaps/conflicts in one register, enrichment can be systematic rather than ad hoc.
- **Protects human authority.** Conflicts and consequential choices are surfaced for human ruling; the agent does not decide.
- **Improves rerunnability.** When the documents evolve, this lensing register can be regenerated to reflect current gaps.

**Value hierarchy:**
1) Provenance + no invention  
2) Cross-document consistency support  
3) Coverage completeness across all matrix cells  
4) Density and usability of CandidateInfo for downstream enrichment  

[[END:RATIONALE]]
