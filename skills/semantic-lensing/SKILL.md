---
name: semantic-lensing
description: Apply semantic lensing analysis to deliverable documents using _SEMANTIC.md matrices. Treats lensing entries as a candidate worklist, tags proposals with matrix coordinates, and optionally updates lens artifacts.
compatibility: Chirality TASK generic shell; reasoning-only (no deterministic tools).
metadata:
  chirality-skill-version: "1"
  chirality-task-profile: NONE
---

# SKILL — semantic-lensing

## Purpose

Apply semantic lensing analysis to deliverable-local production documents using `_SEMANTIC.md` as the lens reference and `_SEMANTIC_LENSING.md` as the enrichment worklist.

This skill provides the structured method for interactive semantic lensing analysis. When loaded, it supplies the matrix interpretation, tagging conventions, and proposal workflow.

This skill is the **optional interactive proposal/review tool**, not the regular PROJECT_SETUP enrichment step. In the regular PROJECT/SOFTWARE setup workflow:

- `skills/lens-register/` is the pipeline producer of `_SEMANTIC_LENSING.md`.
- The resolver-selected production skill applies `_SEMANTIC_LENSING.md` as an enrichment worklist.
- `skills/semantic-lensing/` is loaded only when a WORKING_ITEMS or TASK run needs human-facing `PROPOSAL:` blocks, focused review, or optional lens artifact updates.

Put another way, `_SEMANTIC_LENSING.md` becomes useful through enrichment of
the selected production contract. This skill may also consume the same file,
but only for interactive review. Both paths treat entries as candidates, not evidence.

This skill is the **interactive, proposal-producing** contract in the semantic-lensing family. Its setup-time counterpart is `skills/lens-register/`, which generates the matrix-organized register consumed by the selected production skill and optionally by this skill.

## Suitable agent shells

- `TASK` (generic shell, no profile)

## Inputs

### Required

- `ScopePath`
- `RuntimeOverrides.DELIVERABLE_PATH`
- `_SEMANTIC.md` must exist in the deliverable folder (read-only)
- `ProductionFormat` — resolver-selected `LEGACY_FOUR_DOC`, `SOW_V1`, or authorized `MIGRATION_DUAL`.
- `FormatAuthorityRef` — required only for `MIGRATION_DUAL` and bound to exact
  accepted path-scoped migration authority.

### Optional

- `_SEMANTIC_LENSING.md` — enrichment worklist (if absent, skill generates initial lens analysis only)
- `ActiveMatrices` — restrict analysis to named matrices (default: all matrices found in `_SEMANTIC.md`)
- `FocusLensTags` — restrict processing to specific `Matrix.Row.Column` tags
- `AllowLensLogUpdate` — permit creating/updating `_SEMANTIC_LENSING.md`
- `AllowTransferableContextUpdate` — permit creating/updating `_TRANSFERABLE_CONTEXT.md`
- `UseSemanticLensing` — accepted compatibility flag; loading this skill is the actual method selector

## Runtime overrides

| Key | Meaning | Default |
|---|---|---|
| `ActiveMatrices` | Restrict to named matrices (e.g., `A,B,F`) | all matrices in `_SEMANTIC.md` |
| `FocusLensTags` | Process only entries matching these tags | all entries |
| `LensDepth` | `shallow` (tag only) or `deep` (tag + cross-document analysis) | `deep` |

## Tool usage

This is a reasoning-only skill. No deterministic tools are required or allowed.

Preferred method:
- read `_SEMANTIC.md` to understand the matrix structure and question framework
- read the production documents under `RuntimeOverrides.DELIVERABLE_PATH`
- resolve production documents from `ProductionFormat`: the four legacy files
  in legacy mode, or validated `ScopeOfWork.md` in SOW/authorized dual mode
- if `_SEMANTIC_LENSING.md` exists, read each entry as a candidate improvement
- generate proposals with `Lens:` tags grounded in evidence from the production documents
- do not treat lensing entries as evidence — they are candidates only

Disallowed behavior:
- no treating `_SEMANTIC.md` or `_SEMANTIC_LENSING.md` as evidence authority
- no inventing facts to fill lens-identified gaps — use `TBD`
- no widening scope beyond the single deliverable
- no edits to `_SEMANTIC.md` under any circumstances

## Outputs

- `PROPOSAL:` blocks with `Lens: <Matrix.Row.Column>` tags for each finding
- `MISSING:` items where lens-identified content gaps exist
- `NEEDS_HUMAN_RULING:` items where lensing surfaces contradictions
- optionally updated `_SEMANTIC_LENSING.md` (when `AllowLensLogUpdate: true`)
- optionally updated `_TRANSFERABLE_CONTEXT.md` (when `AllowTransferableContextUpdate: true`)
- optional `MEMORY.md` update only when explicitly authorized by the brief

## Method: matrix interpretation

Matrices in `_SEMANTIC.md` (commonly A, B, C, F, D, X, E) are a tagging and analysis convention, not a requirement for completion. Each matrix cell is a question-shaping lens:

- **Use matrices to identify** what questions the deliverable should answer
- **Use matrix coordinates** (`Matrix.Row.Column`) to tag proposals so findings are traceable to the analysis framework
- **Do not require** every matrix cell to yield a finding — empty cells are normal
- **Do not invent** content to fill matrix gaps; use `TBD` and note the lens coordinate

## Method: enrichment workflow (when `_SEMANTIC_LENSING.md` exists)

Each row in `_SEMANTIC_LENSING.md` is a candidate improvement with an item type. Process each entry:

1. Read the entry and identify the target document section(s) or candidate
   Scope-of-Work claim IDs
2. Read the target section(s) in the production documents
3. If the entry is supported by evidence from sources or production documents: generate a `PROPOSAL:` with the lens tag, evidence, and proposed change
4. If the entry identifies a real gap: generate a `PROPOSAL:` with `TBD` content and the lens tag
5. If the entry conflicts with source material: add to `NEEDS_HUMAN_RULING`
6. If the entry cannot be grounded: convert to `TBD` or discard with a note

Item types and their handling:
- `Conflict` — surface with both contenders cited; do not resolve silently
- `WeakStatement` — propose strengthening with source evidence, or mark `TBD`
- `Normalization` — propose terminology/format alignment across documents
- `MissingSlot` — propose content grounded in source, or mark `TBD`
- `RationaleGap` — propose rationale from source guidance, or mark `TBD`
- `VerificationGap` — propose verification approach tied to requirements
- `TBD_Question` — attempt resolution from accessible sources; if unresolvable, retain as `TBD`

## Non-negotiable constraints

- `_SEMANTIC.md` is read-only — never modify it
- Lensing entries are candidates, not evidence — they cannot authorize new facts
- Every proposal must cite evidence from production documents or accessible sources
- Lens tags must use the `Matrix.Row.Column` format
- Unknowns remain `TBD`
- Conflicts must be surfaced, not reconciled silently
- Dual mode fails closed without exact accepted authority and path membership;
  it never treats the candidate as an accepted baseline.

## QA expectations

- Every proposal includes a `Lens:` tag with a valid matrix coordinate
- Proposals that incorporate lensing entries cite the underlying source, not the lensing entry itself
- `_SEMANTIC_LENSING.md` entries that were processed are noted as incorporated, converted to TBD, or discarded with reason
- No content was invented from lensing entries alone
- If `ActiveMatrices` or `FocusLensTags` were set, only the specified scope was processed
