# lens-register — QA Checks

## Minimum checks for a valid run

1. `ScopePath` exists and is a readable directory.
2. `deliverable_folder` resolves to the same directory as `ScopePath`.
3. `_SEMANTIC.md` is present in the deliverable folder, or the output is a blocking header file and the run stops.
4. `DECOMP_VARIANT` is `PROJECT`, `SOFTWARE`, or absent (default `PROJECT`). `DOMAIN` is refused.
5. `_SEMANTIC_LENSING.md` is written to `{deliverable_folder}/_SEMANTIC_LENSING.md` unless the run is refused before output or fails input validation.
6. No production documents were modified.
7. `_SEMANTIC.md` was not modified.
8. `_STATUS.md` was not modified (`STATUS_POLICY=NO_STATUS_TOUCH`).
9. No files outside `{deliverable_folder}/` were read or written, except TASK's own run-record handling inside `{deliverable_folder}/_run_records/`.
10. If `python3 tools/validation/validate_lens_register.py {deliverable_folder}` is available and permitted, it passes before the run reports validator PASS.
11. If the validator is unavailable or not permitted, the run reports `Validator: NOT_RUN` and does not claim validator PASS.

## Structural invariants

| # | Check | Validation |
|---|---|---|
| 1 | **Matrix coverage complete** | Every cell of each lensed matrix A, B, C, F, D, X, E has a Lens Coverage entry. |
| 2 | **Structural matrices excluded** | K, G, and T are not lensed; they are transposes/truncations and would duplicate D/B coverage. |
| 3 | **Primary result tables only** | Lenses are parsed from primary Result tables, not derivation tables, Matrix Summary, Matrix Z, or compact summary duplicates. |
| 4 | **No invention** | Warranted items are grounded in production-document evidence or explicit absence. |
| 5 | **Provenance present** | Every warranted item has `SourcePath` + `SectionRef` or accepted absence wording. |
| 6 | **Conflicts surfaced** | Conflict items have two or more contenders and `HumanRuling=TBD`. |
| 7 | **Summary consistent** | Summary counts match the actual warranted items in the file. |
| 8 | **Schema followed** | Output uses the exact STRUCTURE schema and required column order. |
| 9 | **One deliverable per run** | The run processes exactly one deliverable folder; no cross-deliverable scanning. |
| 10 | **Read-only protected files** | Production docs, `_SEMANTIC.md`, and `_STATUS.md` are not modified. |
| 11 | **Lens-specific no-item notes** | `NO_ITEMS` rows explain the specific lens/document-role outcome; repeated boilerplate is invalid. |

A run failing any required invariant is invalid, except where failure behavior explicitly defines a blocking/refusal output.

## Matrix parsing rules

The skill must parse `_SEMANTIC.md` as follows:

- Process only these matrices: A, B, C, F, D, X, E.
- Ignore structural matrices K, G, T.
- Ignore `Matrix Z — Summary Boundary` if present.
- Ignore `Matrix Summary` and all compact summary tables/lists.
- Ignore derivation-work tables and intermediate collections.
- Use the first complete `### Result` table inside each required matrix section as the authoritative lens table.
- If a matrix Result table is missing, malformed, or has empty cells, create `MATRIX_ERROR` coverage rows and `Type=MatrixError` items referencing `_SEMANTIC.md`.

## Schema compliance

- **File header:** present with `Generated`, `Deliverable Folder`, `DECOMP_VARIANT`, `StatusPolicy`, `Validator`, `Inputs Read`, `Purpose`, and `Warnings` when applicable.
- **Summary block:** present before any matrix section. Counts are integers (0 permitted).
- **Matrix sections:** one per matrix in fixed order A, B, C, F, D, X, E. Each contains:
  - a **Lens Coverage** table with one row per matrix cell, row-major;
  - a **Warranted Items** table only when at least one item exists for that matrix.
- **Lens Coverage columns:** `LensKey`, `RowLabel`, `ColLabel`, `LensValue`, `ItemCount`, `CoverageStatus`, `Notes`.
- **Warranted Items columns:** `ItemID`, `LensKey`, `Type`, `AppliesToDoc`, `SuggestedEditDoc`, `CandidateInfo`, `WhyWarranted`, `SourcePath`, `SectionRef`, `Contenders`, `ProposedAuthority (PROPOSAL)`, `HumanRuling`.
- **CoverageStatus enum:** `NO_ITEMS` | `HAS_ITEMS` | `MATRIX_ERROR`.
- **Type enum:** `MissingSlot` | `WeakStatement` | `Conflict` | `VerificationGap` | `RationaleGap` | `Normalization` | `TBD_Question` | `MatrixError`.

## NO_ITEMS note discipline

Every `NO_ITEMS` row must contain a lens-specific note. Invalid boilerplate includes:

- `No warranted items found.`
- `No issues.`
- `N/A.`

Valid examples:

- `Requirement and verification roles already align under this lens.`
- `Datasheet attributes already cover the descriptive role; no gap detected.`
- `Guidance rationale is present and consistent with procedure checks.`
- `No production document presented a conflict or missing slot for this lens.`

## No-invention rule

- Every warranted item must cite evidence from production documents or explicitly record absence.
- Speculative or unsupported content must become `Type=TBD_Question`.
- The skill must not introduce new numeric values, new normative requirements, or acceptance claims.
- The skill must not claim compliance with a standard whose text is not present.
- `_SEMANTIC.md` and `_SEMANTIC_LENSING.md` are not evidence sources for engineering facts.

## Human decision rights

- Conflicts are surfaced, not resolved.
- `HumanRuling` is always `TBD` unless a pre-existing human ruling is citable.
- `ProposedAuthority` is always `PROPOSAL`; never authoritative.

## Unsupported variants

`DECOMP_VARIANT=DOMAIN` is not supported. If passed:

- Do not write `_SEMANTIC_LENSING.md`.
- Do not modify any file.
- Return `RUN_STATUS=REFUSED` with the message: `DECOMP_VARIANT=DOMAIN is not supported by lens-register; DOMAIN pipelines skip the semantic lensing step.`

## Failure reporting

- If `_SEMANTIC.md` is missing: write `_SEMANTIC_LENSING.md` with a blocking header: `Missing _SEMANTIC.md; run semantic-matrix-build first (PROJECT_SETUP Phase 2.3)` and stop. Report `RUN_STATUS=BLOCKED`.
- If `{deliverable_folder}` does not exist or is not readable: report `RUN_STATUS=FAILED_INPUTS`; do not write.
- If a production document is missing: record `[WARNING] MISSING_DOC: <filename>` in the output header and continue.
- If a matrix cell is empty or malformed: set `CoverageStatus=MATRIX_ERROR`, add a `Type=MatrixError` item, and continue.
- If validator is unavailable: report `Validator: NOT_RUN`; do not call the run validator-passed.
- If validator fails: report `RUN_STATUS=FAILED` with validator errors.

## Success case

A clean run reports:

- `RUN_STATUS=OK`
- Deliverable ID/name
- `_SEMANTIC.md` was present and parsed from primary Result tables
- Count of warranted items total + by document + by matrix + by type
- Matrix parsing errors, missing docs, and conflicts, if any
- Path to `_SEMANTIC_LENSING.md`
- `Validator: PASS` or `Validator: NOT_RUN — <reason>`
- `_STATUS.md` unchanged
- No production documents modified

## Evidence required for each item

| Type | Minimum evidence |
|---|---|
| `Conflict` | Two+ `path#section` entries in `Contenders`; `HumanRuling=TBD`. |
| `VerificationGap` | Citation of the normative requirement whose acceptance is missing/ambiguous. |
| `MissingSlot` | Doc(s) searched in `SourcePath`; section or `entire document scanned` in `SectionRef`. |
| `WeakStatement` | Doc+section citation for ambiguous language. |
| `RationaleGap` | Doc+section citation for decision/requirement lacking rationale. |
| `Normalization` | Two+ locations where terminology diverges. |
| `TBD_Question` | Rationale and who/what to consult in `CandidateInfo`. |
| `MatrixError` | Reference to the affected cell in `_SEMANTIC.md`. |
