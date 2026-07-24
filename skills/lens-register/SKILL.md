---
name: lens-register
description: Generate a matrix-organized, coverage-complete semantic lensing register (_SEMANTIC_LENSING.md) from _SEMANTIC.md + production documents. Setup-pipeline companion to the interactive semantic-lensing skill.
compatibility: Chirality TASK; dispatched by PROJECT_SETUP setup pipeline (Phase 2.4).
metadata:
  chirality-skill-version: "2"
  chirality-task-profile: NONE
---

# SKILL — lens-register

## Purpose

Produce a **matrix-organized lensing register** (`_SEMANTIC_LENSING.md`) that:

1. Uses each primary Result-table cell of matrices **A, B, C, F, D, X, E** from `_SEMANTIC.md` as a lens,
2. Applies each lens to the deliverable-local production documents, and
3. Records only warranted enrichment inputs with provenance, without rewriting the documents.

This is the **setup-pipeline, coverage-complete** contract in the semantic-lensing family. It is the normal PROJECT_SETUP Phase 2.4 skill. Its interactive counterpart is `semantic-lensing`, which produces human-facing proposals or reviews existing register entries. `lens-register` creates the register; `four-documents` Pass 3 consumes the register.

## Suitable agent shells

- `TASK` generic shell, no profile.

Typical dispatcher: PROJECT_SETUP Phase 2.4 dispatches TASK with `TaskSkill: lens-register`, `ScopePath={DELIVERABLE_PATH}`, `RuntimeOverrides.deliverable_folder={DELIVERABLE_PATH}`, and write authorization for `_SEMANTIC_LENSING.md`.

## Inputs

### Required

- `ScopePath` — absolute path to one production unit folder.
- `deliverable_folder` — absolute path to the same folder, normally supplied in `RuntimeOverrides`.
- `_SEMANTIC.md` in the deliverable folder.

### Optional

- `DECOMP_VARIANT` — `PROJECT` | `SOFTWARE` (default `PROJECT`). `DOMAIN` is not supported.
- `STATUS_POLICY` — default `NO_STATUS_TOUCH`.
- `PRODUCTION_FORMAT` — resolver-selected `LEGACY_FOUR_DOC`, `SOW_V1`, or
  authorized `MIGRATION_DUAL`; dual mode requires `FORMAT_AUTHORITY_REF`.
- `DeliverablePath` — compatibility alias only; does not affect TASK write authorization.

### Files read

Required:
- `{deliverable_folder}/_SEMANTIC.md` — source for lenses.

Contextual, read when present:
- `{deliverable_folder}/_CONTEXT.md`
- `{deliverable_folder}/_STATUS.md`
- `{deliverable_folder}/Datasheet.md`
- `{deliverable_folder}/Specification.md`
- `{deliverable_folder}/Guidance.md`
- `{deliverable_folder}/Procedure.md`
- `{deliverable_folder}/ScopeOfWork.md` — read instead of the legacy set for
  `SOW_V1`, or as the candidate replacement in authorized `MIGRATION_DUAL`
  with exact path-scoped authority.
- `{deliverable_folder}/_REFERENCES.md` — metadata only; do not follow external paths.

Missing production documents produce warnings, not failure.

## Runtime overrides

| Key | Meaning | Default | Allowed values |
|---|---|---|---|
| `deliverable_folder` | Skill-local scope anchor | required | absolute path equal to `ScopePath` |
| `DECOMP_VARIANT` | Decomposition pipeline variant | `PROJECT` | `PROJECT`, `SOFTWARE` |
| `STATUS_POLICY` | Lifecycle handling | `NO_STATUS_TOUCH` | `NO_STATUS_TOUCH` |

`DECOMP_VARIANT=DOMAIN` is refused because DOMAIN pipelines skip semantic lensing.

## Tool usage

Reasoning-first generation. Deterministic validation is optional but expected when the validator exists and the brief permits it.

- No deterministic tool is required to generate `_SEMANTIC_LENSING.md`.
- Optional validators may be used after generation:
  - `python3 tools/validation/validate_lens_register.py {deliverable_folder}`
  - `python3 tools/validation/validate_semantic_pipeline_scope.py {deliverable_folder} --step lens`
- Do not claim validator PASS unless the validator actually ran and passed.

The `allowed-tools` frontmatter field is intentionally omitted; TASK may still enforce a brief-provided allowlist.

## Outputs

Skill-authored output:

- `{deliverable_folder}/_SEMANTIC_LENSING.md` — overwritten each run.

TASK shell output:

- `{deliverable_folder}/_run_records/TASK_RUN_*.md` — TASK run record.

## Non-negotiable invariants

- **One deliverable per run.** Operate on exactly one folder.
- **Read-only production documents.** Do not edit `Datasheet.md`, `Specification.md`, `Guidance.md`, or `Procedure.md`.
- **SOW target IDs.** In `SOW_V1` or authorized migration-dual mode, apply lenses to
  `ScopeOfWork.md` and record `AppliesToSection`, `TargetClaimRef`, and
  `SuggestedTargetSection`; do not invent a second claim registry.
- **Read-only `_SEMANTIC.md`.** It is a lens source, not an output target or engineering authority.
- **Read-only `_STATUS.md`.** Normal Phase 2.4 policy is `NO_STATUS_TOUCH`.
- **No external expansion.** Do not follow `_REFERENCES.md` paths or read outside the deliverable folder.
- **Use lenses, not authority.** Matrix cells shape what to look for; they do not justify inventing content.
- **No invention.** Unknowns become `TBD_Question`; gaps become `MissingSlot`; conflicts become `Conflict`.
- **Provenance required.** Every warranted item has `SourcePath` and `SectionRef` or explicit absence provenance.
- **Conflicts surfaced, not resolved.** `HumanRuling=TBD` unless a prior human ruling is cited.
- **Matrix coverage complete.** Every cell in A, B, C, F, D, X, E appears in Lens Coverage.
- **Structural matrices excluded.** K and T are transposes; G is a truncation. They are not lensed because doing so duplicates D/B coverage.
- **Parser hygiene.** Ignore derivation tables, Matrix Summary, and Matrix Z. Parse only primary Result tables.
- **No boilerplate NO_ITEMS.** Notes must be lens-specific.

## Precedence

1. **PROTOCOL** governs sequencing and run behavior.
2. **SPEC** governs validity.
3. **STRUCTURE** defines output schema.
4. **RATIONALE** governs interpretation when ambiguity remains.

If instructions conflict, flag the conflict and return it to the invoker.

## Glossary

| Term | Meaning |
|---|---|
| Lens | A matrix Result-table cell used as a question-shaping perspective. |
| LensKey | Canonical identifier: `M:[RowLabel]:[ColLabel]`. |
| Warranted item | A grounded gap, conflict, weak statement, normalization risk, rationale gap, verification gap, or TBD question. |
| Production documents | `Datasheet.md`, `Specification.md`, `Guidance.md`, `Procedure.md`. |
| Structural matrices | K, G, T; excluded from lensing because they duplicate predecessor content. |

---

## PROTOCOL — Straight-through lens-register procedure

### Step 0 — Safety checks

1. Resolve `ScopePath` and `deliverable_folder`; they must identify the same readable directory.
2. If `DECOMP_VARIANT=DOMAIN`, refuse gracefully and do not write files.
3. Confirm `_SEMANTIC.md` exists.
   - If missing, write `_SEMANTIC_LENSING.md` with a blocking header and stop.
4. Confirm production documents exist.
   - Missing production documents produce `[WARNING] MISSING_DOC: <filename>` and the run proceeds with available documents.
5. Confirm no write target outside `_SEMANTIC_LENSING.md` and TASK `_run_records/` is required.

### Step 1 — Read context and inputs

Read, in order:

1. `_CONTEXT.md` if present.
2. `_STATUS.md` if present; record state but do not change it.
3. `_SEMANTIC.md`.
4. Existing production documents.
5. `_REFERENCES.md` if present; list as metadata only and do not follow external paths.

### Step 2 — Parse matrices into a lens inventory

For each matrix `M ∈ {A, B, C, F, D, X, E}`:

1. Locate the matrix section.
2. Locate the first primary `### Result` table in that section.
3. Extract row labels, column labels, and cell values.
4. Create one Lens Coverage row per cell, row-major:
   - `LensKey = M:[RowLabel]:[ColLabel]`
   - `LensValue = cell value`
   - `ItemCount=0`
   - `CoverageStatus=NO_ITEMS`
   - `Notes=<lens-specific initial note>`

Ignore:

- derivation/intermediate work tables;
- Matrix Summary;
- Matrix Z;
- structural matrices K, G, T.

If a required matrix or cell is malformed, record `MATRIX_ERROR` and continue.

### Step 3 — Apply lenses and record warranted items

For each `LensKey`:

1. Scan the production documents.
2. Ask: what gap, conflict, ambiguity, missing verification, missing rationale, or terminology risk becomes salient under this lens?
3. Record an item only when it meets the warranted threshold.
4. Update `ItemCount`, `CoverageStatus`, and `Notes`.

Warranted item types:

- `Conflict`
- `VerificationGap`
- `MissingSlot`
- `WeakStatement`
- `RationaleGap`
- `Normalization`
- `TBD_Question`
- `MatrixError`

Tight filter:

- Do not record restatements.
- Do not pad the register for coverage.
- Do not create items simply because a lens exists.
- If documents are already clear and aligned under a lens, record `NO_ITEMS` with a specific note.

### Step 4 — Write `_SEMANTIC_LENSING.md`

Write or overwrite `{deliverable_folder}/_SEMANTIC_LENSING.md` using the STRUCTURE schema.

### Step 5 — QA and optional validation

1. Confirm protected files were not modified.
2. Confirm coverage completeness and schema compliance.
3. Run `validate_lens_register.py` if available and permitted.
4. Report validator status as `PASS`, `FAILED`, or `NOT_RUN`.
5. Return run report to TASK/PROJECT_SETUP.

---

## SPEC — Validity requirements

### S1 — Coverage completeness

Every cell of A, B, C, F, D, X, and E must appear in Lens Coverage. Zero-item cells are valid when their notes are lens-specific.

### S2 — No invention

A warranted item must be grounded in production-document evidence or explicit absence. Use `TBD_Question` when required information is absent or external.

### S3 — Provenance

Every warranted item includes:

- `SourcePath`;
- `SectionRef`;
- `Contenders` when conflict exists.

### S4 — Human decision rights

The skill must not choose a winner, introduce requirements, or assert compliance. Human rulings remain `TBD` unless already citable.

### S5 — Output stability

Output must use stable ordering and exact table schemas.

### S6 — Scope discipline

The run must not read sibling deliverables or external references; `_REFERENCES.md` is metadata only.

### S7 — Status discipline

`_STATUS.md` is not changed by `lens-register`.

---

## STRUCTURE — Output file schema

### File header

```markdown
# Semantic Lensing Register: [Production Unit ID] [Name]

**Generated:** [YYYY-MM-DD]
**DECOMP_VARIANT:** [PROJECT|SOFTWARE]
**Deliverable Folder:** [path]
**StatusPolicy:** NO_STATUS_TOUCH
**Validator:** PASS | FAILED | NOT_RUN — [reason]
**Warnings:** [optional warning list]

**Inputs Read:**
- _CONTEXT.md — [SourceRef or not present]
- _STATUS.md — [SourceRef or not present]
- _SEMANTIC.md — [SourceRef]
- Datasheet.md — [SourceRef or missing]
- Specification.md — [SourceRef or missing]
- Guidance.md — [SourceRef or missing]
- Procedure.md — [SourceRef or missing]
- _REFERENCES.md — [SourceRef or not present / not read]

**Purpose:** Apply semantic-matrix-build Result-table cells as lenses over production documents, capturing warranted enrichment inputs for a later enrichment pass.
```

### Summary block

```markdown
## Summary

- Total warranted items: N
- By document:
  - Datasheet: n
  - Specification: n
  - Guidance: n
  - Procedure: n
  - Multi: n
  - NA: n
- By matrix:
  - A: n
  - B: n
  - C: n
  - F: n
  - D: n
  - X: n
  - E: n
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

### Matrix sections

For each matrix in order: A, B, C, F, D, X, E.

```markdown
## Matrix M — [Matrix Name]

### Lens Coverage
| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| M:[r]:[c] | r | c | ... | 0 | NO_ITEMS | lens-specific note |

### Warranted Items
| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:[r]:[c] | VerificationGap | Specification | Specification | Add acceptance criteria for ... | ... | ... | ... | ... | PROPOSAL | TBD |
```

Omit `### Warranted Items` for a matrix only when no warranted items exist for that matrix.

#### Lens Coverage columns

- `LensKey`: `M:[RowLabel]:[ColLabel]`
- `RowLabel`: row label from matrix Result table
- `ColLabel`: column label from matrix Result table
- `LensValue`: cell value
- `ItemCount`: integer count of warranted items for the lens
- `CoverageStatus`: `NO_ITEMS` | `HAS_ITEMS` | `MATRIX_ERROR`
- `Notes`: lens-specific note; no boilerplate

#### Warranted Items columns

- `ItemID`: unique within file, recommended `{Matrix}-{000}`.
- `LensKey`: matching Lens Coverage key.
- `Type`: one allowed item type.
- `AppliesToDoc`: `Datasheet` | `Specification` | `Guidance` | `Procedure` | `Multi` | `NA`.
- `SuggestedEditDoc`: best-fit later enrichment target, or `TBD` / `NA`.
- `CandidateInfo`: short enrichment-ready phrasing; not full prose.
- `WhyWarranted`: 1–2 sentence rationale.
- `SourcePath`: file path(s) searched or cited.
- `SectionRef`: heading anchor, `location TBD`, or `entire document scanned`.
- `Contenders`: two or more `path#section` entries for conflicts; blank otherwise.
- `ProposedAuthority (PROPOSAL)`: always `PROPOSAL` for proposed authority placement.
- `HumanRuling`: `TBD` unless a prior human ruling is cited.

### SuggestedEditDoc heuristic

- `VerificationGap` → `Specification` and/or `Procedure`.
- `RationaleGap` → `Guidance`.
- `Normalization` → `Guidance` plus affected documents as needed.
- `WeakStatement` → same document where the ambiguity appears unless role placement suggests otherwise.
- `MissingSlot` → best-fit document role or `TBD`.
- `Conflict`, `TBD_Question`, `MatrixError` → `NA` or `TBD`.

### SourceRef convention

Use file path + best-effort heading anchors, or `location TBD`. SourceRefs record traceability; they do not make matrices authoritative.

---

## RATIONALE

`_SEMANTIC.md` partitions the deliverable's semantic space. `lens-register` turns those partitions into a bounded, evidence-linked worklist for later enrichment without editing the production documents.

Value hierarchy:

1. Provenance and no invention
2. Scope discipline
3. Coverage completeness
4. Register usability
5. Semantic density

## QA expectations

See `QA_CHECKS.md`.

## See also

- `skills/semantic-matrix-build/SKILL.md` — produces `_SEMANTIC.md`
- `skills/semantic-lensing/SKILL.md` — interactive proposal workflow consuming this register
- `skills/four-documents/SKILL.md` — Pass 3 consumer of `_SEMANTIC_LENSING.md`
- `agents/AGENT_PROJECT_SETUP.md` — dispatches this skill via TASK in Phase 2.4
