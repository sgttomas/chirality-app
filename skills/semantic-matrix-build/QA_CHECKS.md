# semantic-matrix-build — QA Checks

Minimum checks for a valid run:

1. `deliverable_folder` exists and is a directory.
2. `_CONTEXT.md` exists in the deliverable folder.
3. `_SEMANTIC.md` is written to `{deliverable_folder}/_SEMANTIC.md`.
4. Output contains all eight derived matrices in sequence: C, F, D, K, G, X, T, E.
5. Canonical matrices A and B are reproduced as-is (not re-derived).
6. `_STATUS.md` is updated only on audit PASS (set/verified as `SEMANTIC_READY`); on FAIL, state is not advanced.
7. Production documents in the deliverable folder are not modified (read-only).
8. No files outside the deliverable folder were written.

## Structural invariants (all required)

| Check | Requirement |
|---|---|
| Matrix A canonical | Exact canonical values present, not re-derived |
| Matrix B canonical | Exact canonical values present, not re-derived |
| Eight derived matrices | C, F, D, K, G, X, T, E all present in order |
| Construction formula shown | Each derived matrix shows its construction formula |
| Full derivation work shown | Dot-product matrices (C, F, X, E) and addition matrix (D) include intermediate collections + all three interpretation steps for each cell |
| Result tables present | Each derived matrix has a completed Result table with row and column labels |
| Matrix Summary present | Final section contains all eight derived matrices in compact table form |
| Correct dimensions | Matrix dimensions match specification (C 3×4, F 3×4, D 3×4, K 4×3, G 3×4, X 4×4, T 4×4, E 4×4) |

## Semantic product validity (all required)

| Check | Requirement |
|---|---|
| All cells populated | No empty cells in any final matrix |
| Single unit per cell | Each cell contains exactly one semantic unit (a 2-5 word phrase), not a list |
| No algebra leaks | No `∩` or `Σ` operators in final cell values |
| No operator leaks | No `+` flanked by semantic terms in final cell values |
| No long expansions | No cell value exceeds ~80 characters |
| No axis tokens in output | Row/column labels do not appear in cell values |

## Interpretation validity (all required — "show all work")

| Check | Requirement |
|---|---|
| Step 1 explicit | Axis anchor `a = r * c` is computed and shown for each interpreted cell |
| Step 2 explicit | Every projection `p_t = a * t` is computed and shown for each contributor `t ∈ L` |
| Step 3 explicit | Centroid selection reasoning is provided for each interpreted cell |
| No shortcuts | Interpretation does not skip from Step 1 to Step 3 |
| All contributors projected | Every `t ∈ L` has a corresponding `p_t` in the working |

## Non-negotiable invariants (enumerated)

Each is a distinct check:

1. **Show all work (operations).** Every interpretation operation displays all three steps explicitly. Interpretations that skip steps are invalid.
2. **No particulars.** Outputs are types, categories, behaviors, and values—not specific instances, numbers, equipment tags, or code clauses.
3. **Semantic-algebra discipline.** The A, B → C, F, D, K, G, X, T, E matrix progression is followed in order; downstream matrices are not computed before upstream matrices are complete.
4. **Lens-not-authority separation.** The skill produces a semantic lens (`_SEMANTIC.md`), not an engineering authority. It does not decide design content or evidence-based claims.
5. **Deliverable-bound perspective.** The skill adopts exactly one deliverable's perspective per run. No cross-deliverable scanning or comparison.
6. **Semantic density over verbosity.** Final cell values are 2-5 word phrases. Working/outworking may be longer.
7. **Order of operations is strict.** Parentheses, then `*` left-to-right, then `+` left-to-right.
8. **List-valued operands require interpretation.** `I(r, c, L)` is applied before downstream use of any list-valued operand.
9. **Read-only on production documents.** The skill does not modify `Datasheet.md`, `Specification.md`, `Guidance.md`, `Procedure.md`, any `KA-*.md`, or `Scoping.md`.
10. **Latent axes.** Row and column labels condition the output but do not appear literally in cell values.
11. **Deliverable-local write scope.** Only `{deliverable_folder}/_SEMANTIC.md` and `{deliverable_folder}/_STATUS.md` may be written.
12. **No status regression.** `_STATUS.md` state is never regressed; on audit PASS state is set/verified as `SEMANTIC_READY`; on audit FAIL state is unchanged.

## Audit (mandatory before acceptance)

The skill must scan every cell in every Result table (matrices C, F, D, X, E) for these three failure patterns:

1. **Algebra leak:** cell value contains `∩` or `Σ`.
2. **Uninterpreted expansion:** cell value exceeds ~80 characters.
3. **Operator leak:** cell value contains `+` flanked by semantic terms.

If any cell fails:

- Mark the run **FAIL** (do not attempt to repair, re-derive, or re-audit).
- Leave `_STATUS.md` state unchanged; append a History entry noting the audit failure.
- Emit the run report with the failed matrix/cell(s) and the failure reason(s).
- End the run.

Only if all cells pass may the run proceed to `_STATUS.md` advancement.

## Source traceability (required)

The `_SEMANTIC.md` file must record provenance:

- `Inputs Read` block lists each file read with a SourceRef (file path + best-effort heading anchor or "location TBD").
- Production documents read are enumerated (or explicitly absent).
- The Perspective statement is deliverable-bound (derived from `_CONTEXT.md` + production documents).

A run that invents inputs or skips provenance is invalid.

## Evaluative judgment boundary (must NOT be present)

The `_SEMANTIC.md` file must NOT contain:

- Engineering correctness assessments
- Specific numeric values, equipment tags, or code clause citations (no particulars)
- Cross-deliverable comparisons
- Recommendations or authority claims
- Evaluative language about the deliverable's fitness

Those belong elsewhere in the pipeline (`lens-register` skill enrichment register; human engineering authority).

## Failure reporting

- If `_CONTEXT.md` is missing: report `FAILED_INPUTS` — the skill cannot operate without it.
- If `deliverable_folder` is not a directory: report `FAILED_INPUTS`.
- If a production document is missing: record its absence in `Inputs Read`; do not fail.
- If `_REFERENCES.md` is missing: note `not read`; do not fail.
- On audit FAIL: emit run report with failing matrix/cell(s) + reason(s); `_STATUS.md` state unchanged.

## Success case

A clean run reports:

- `RUN_STATUS=OK`
- Deliverable ID/name
- `_SEMANTIC.md` was written (path)
- Audit PASS
- `_STATUS.md` state set/verified as `SEMANTIC_READY`
- No failing cells or matrix construction errors
