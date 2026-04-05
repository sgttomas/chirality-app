# lens-register — QA Checks

Minimum checks for a valid run:

1. `DeliverablePath` (or `deliverable_folder`) exists and is a readable directory.
2. `_SEMANTIC.md` is present in the deliverable folder (or the output is a blocking header file and the run stops).
3. `DECOMP_VARIANT` is `PROJECT`, `SOFTWARE`, or absent (default `PROJECT`). `DOMAIN` is refused — see "Unsupported variants" below.
4. `_SEMANTIC_LENSING.md` is written to `{deliverable_folder}/`.
5. No production documents (`Datasheet.md`, `Specification.md`, `Guidance.md`, `Procedure.md`) were modified.
6. `_SEMANTIC.md` was not modified.
7. No files outside `{deliverable_folder}/` were read or written.

## Structural invariants (all 8 required)

| # | Check | Validation |
|---|---|---|
| 1 | **Matrix coverage complete** | Every cell of each matrix (A, B, C, F, D, X, E) in `_SEMANTIC.md` has a Lens Coverage entry in `_SEMANTIC_LENSING.md` |
| 2 | **No invention** | All warranted items are grounded in evidence (citing production documents) or explicit absence (`MissingSlot`); no speculated content |
| 3 | **Provenance present** | Every warranted item has `SourcePath` + `SectionRef` (or `location TBD` / `entire document scanned`) |
| 4 | **Conflicts surfaced** | `Conflict` items have `Contenders` populated with two+ `path#section` entries and `HumanRuling = TBD` |
| 5 | **Summary consistent** | Summary block counts (total, by-document, by-matrix, by-type) match actual warranted items in the file |
| 6 | **Schema followed** | Output uses the exact STRUCTURE schema (file header, Summary, per-matrix Lens Coverage table + Warranted Items table) with the required column order |
| 7 | **One deliverable per run** | The run processed exactly one deliverable folder; no cross-deliverable scanning |
| 8 | **Read-only on production documents** | `Datasheet.md`, `Specification.md`, `Guidance.md`, `Procedure.md` (and `_SEMANTIC.md`) were not modified |

A run failing any of these invariants is invalid.

## Schema compliance

- **File header:** present with `Generated`, `Deliverable Folder`, `Inputs Read`, `Purpose`. `Warnings` block present when any document is missing or any matrix parse error occurred.
- **Summary block:** present before any matrix section. Counts are integers (0 permitted).
- **Matrix sections:** one per matrix in the fixed order A, B, C, F, D, X, E. Each contains:
  - A **Lens Coverage** table with one row per matrix cell (row-major), columns `LensKey`, `RowLabel`, `ColLabel`, `LensValue`, `ItemCount`, `CoverageStatus`, `Notes`.
  - A **Warranted Items** table (only if `ItemCount > 0` for any lens in that matrix), with columns `ItemID`, `LensKey`, `Type`, `AppliesToDoc`, `SuggestedEditDoc`, `CandidateInfo`, `WhyWarranted`, `SourcePath`, `SectionRef`, `Contenders`, `ProposedAuthority`, `HumanRuling`.
- **CoverageStatus enum:** `NO_ITEMS` | `HAS_ITEMS` | `MATRIX_ERROR` — no other values.
- **Type enum:** `MissingSlot` | `WeakStatement` | `Conflict` | `VerificationGap` | `RationaleGap` | `Normalization` | `TBD_Question` | `MatrixError` — no other values.

## No-invention rule

- Every warranted item must cite evidence from production documents or explicitly record absence (`MissingSlot` with searched doc(s) in `SourcePath`).
- Speculative or unsupported content MUST be converted to `Type=TBD_Question` with rationale and "who/what to consult".
- The skill MUST NOT introduce new numeric values or normative ("shall") requirements unless already present and being pointed to as a gap.
- The skill MUST NOT claim compliance with a standard whose text is not present.

## Human decision rights

- Conflicts are surfaced, not resolved. `HumanRuling` is always `TBD` unless a pre-existing human ruling is citable.
- The skill MUST NOT choose a "winner" when sources conflict.
- `ProposedAuthority` is PROPOSAL only; never asserted as authoritative.

## Unsupported variants

- **`DECOMP_VARIANT=DOMAIN` is not supported.** Per the Slice 2b ruling (Direction b), DOMAIN pipelines skip the semantic lensing step.
- **Refusal behavior:** If a brief passes `DECOMP_VARIANT=DOMAIN`, the skill MUST refuse gracefully:
  - Do not write `_SEMANTIC_LENSING.md`.
  - Return a `RUN_STATUS=REFUSED` (or equivalent) report to the invoker with the message: `DECOMP_VARIANT=DOMAIN is not supported by lens-register; DOMAIN pipelines skip the semantic lensing step.`
  - Do not modify any file in the deliverable folder.

## Failure reporting

- If `_SEMANTIC.md` is missing: write `_SEMANTIC_LENSING.md` with a blocking header ("Missing _SEMANTIC.md; run `semantic-matrix-build` skill first (ORCHESTRATOR Phase 2.3)") and stop. Report `RUN_STATUS=BLOCKED`.
- If `{deliverable_folder}` does not exist or is not readable: report `RUN_STATUS=FAILED_INPUTS`; do not write.
- If one or more production documents are missing: do not fail; record `[WARNING] MISSING_DOC: <filename>` in the output header and proceed with available docs.
- If a matrix cell is empty or malformed in `_SEMANTIC.md`: set `CoverageStatus=MATRIX_ERROR` for the affected `LensKey`, add a `Type=MatrixError` warranted item referencing `_SEMANTIC.md`, continue the run (do not fail).
- If `DECOMP_VARIANT=DOMAIN`: refuse gracefully (see "Unsupported variants" above).

## Success case

A clean run reports:

- `RUN_STATUS=OK`
- Deliverable ID/name
- `_SEMANTIC.md` was present and parsed
- Count of warranted items (total + by document + by matrix)
- List of any matrix parsing errors, missing docs, or severe conflicts detected
- Path to the written `_SEMANTIC_LENSING.md`

## Evidence required for each item

| Type | Minimum evidence |
|---|---|
| `Conflict` | Two+ `path#section` entries in `Contenders`; `HumanRuling=TBD` |
| `VerificationGap` | Citation of the normative requirement (`SourcePath`+`SectionRef`) whose acceptance is missing/ambiguous |
| `MissingSlot` | Doc(s) searched in `SourcePath`; section-or-"entire document scanned" in `SectionRef` |
| `WeakStatement` | Doc+section citation in `SourcePath`+`SectionRef` for the ambiguous language |
| `RationaleGap` | Doc+section citation for the decision/requirement lacking rationale |
| `Normalization` | Two+ locations where terminology diverges |
| `TBD_Question` | Rationale + "who/what to consult" in `CandidateInfo` |
| `MatrixError` | Reference to the cell in `_SEMANTIC.md` |
