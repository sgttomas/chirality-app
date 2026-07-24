# semantic-matrix-build — QA Checks

## Minimum checks for a valid run

1. `ScopePath` exists and is a directory.
2. `deliverable_folder` exists, is a directory, and resolves to `ScopePath`.
3. `_CONTEXT.md` exists in `deliverable_folder`.
4. `decomposition_path` is provided. If the file cannot be read, record that fact; do not invent decomposition content.
5. `_SEMANTIC.md` is written to `{deliverable_folder}/_SEMANTIC.md`.
6. Production documents are read-only.
7. No sibling deliverable folder is scanned.
8. No files outside the effective bounded task brief's write authorization are written.
9. All eight derived matrices appear in sequence: C, F, D, K, G, X, T, E.
10. Canonical matrices A and B are reproduced exactly and not re-derived.
11. Interpreted matrices C, F, D, X, and E include intermediate collections and all three interpretation steps for every cell.
12. Matrix Summary appears after `Matrix Z — Summary Boundary` and contains compact markdown tables for C, F, D, K, G, X, T, and E.
13. `STATUS_POLICY` is honored exactly.
14. Repo validator is run when available and permitted; if unavailable, the report says so.

## Structural invariants

| Check | Requirement |
|---|---|
| Header | Includes generated date, variant, perspective, framework, audit status, phase/status ruling, and Inputs Read. |
| Inputs Read | Lists `_CONTEXT.md`, `_STATUS.md`, `_REFERENCES.md`, `_DEPENDENCIES.md`, `MEMORY.md`, and production documents as read, not present, or absent. |
| SourceRefs | Use path + best-effort heading anchor when possible. |
| Matrix A | Exact canonical 3×4 Orientation values. |
| Matrix B | Exact canonical 4×4 Conceptualization values. |
| Matrix order | A, B, C, F, D, K, G, X, T, E, Matrix Z, Matrix Summary. |
| Result tables | Every matrix section has a Result table. |
| Summary tables | Summary uses markdown tables, not bullets. |
| Matrix Z | Present between Matrix E and Matrix Summary; not counted as a semantic matrix. |
| Correct dimensions | C 3×4, F 3×4, D 3×4, K 4×3, G 3×4, X 4×4, T 4×4, E 4×4. |

## Construction formulas

The section heading or construction note must show these formulas:

| Matrix | Required formula |
|---|---|
| C | `L_C(i,j) = Σ_k (A(i,k) * B(k,j)); C(i,j) = I(row_i, col_j, L_C(i,j))` |
| F | `L_F(i,j) = Σ_k (C(i,k) * B(k,j)); F(i,j) = I(row_i, col_j, L_F(i,j))` |
| D | `L_D(i,j) = A(i,j) + (resolution * F(i,j)); D(i,j) = I(row_i, col_j, L_D(i,j))` |
| K | `K(i,j) = D(j,i)` |
| G | remove `wisdom` row from B |
| X | `L_X(i,j) = Σ_k (K(i,k) * G(k,j)); X(i,j) = I(row_i, col_j, L_X(i,j))` |
| T | `T(i,j) = B(j,i)` |
| E | `L_E(i,j) = Σ_k (X(i,k) * T(k,j)); E(i,j) = I(row_i, col_j, L_E(i,j))` |

## Interpretation validity

For every interpreted cell in C, F, D, X, and E:

| Check | Requirement |
|---|---|
| Intermediate collection | Contains every contributor product required by the formula. |
| Step 1 explicit | Shows `r * c = <resolved anchor phrase>`. |
| Step 1 resolved | Anchor phrase is semantic; it is not merely `<row>-<column> coordinate frame`. |
| Step 2 explicit | Shows every `p_n = a * t_n`. |
| Step 2 resolved | Every projection ends with a resolved semantic phrase. Formula-only projections are invalid. |
| Step 2 complete | Every contributor in `L` has exactly one projection. |
| Step 3 explicit | Says `centroid selects <final phrase>` or equivalent. |
| Step 3 single | Selects one final phrase only. |
| No shortcut | The working does not jump from Step 1 to Step 3. |
| Explicit products | Uses `*` for semantic products. Do not use `x` or prose-only joins. |

## Semantic product validity

Final cells in Result tables and Matrix Summary must satisfy all checks.

| Check | Requirement |
|---|---|
| Populated | No empty final cells. |
| Single unit | Exactly one semantic unit, not a list. |
| Length | 2–5 words, except canonical inherited B/G/T values. |
| Dense | Prefer 2–3 words when complete. |
| No algebra leak | No `∩` or `Σ`. |
| No operator leak | No unresolved `+` flanked by semantic terms. |
| No long expansion | No final cell exceeds about 80 characters. |
| No axis tokens | Row/column labels for that cell do not appear literally in its final value. |
| No particulars | No exact code clauses, event-name lists, file paths, implementation paths, numeric requirements, equipment tags, or other instances. |
| No authority claims | No engineering correctness, recommendations, fitness judgments, or acceptance rulings. |

## Deliverable-conditioning validity

The lens must be relevant to the deliverable without becoming a requirements summary.

| Failure pattern | Invalid example | Better pattern |
|---|---|---|
| Too generic | `adequate evidence` for many unrelated cells | `runtime proof`, `summary integrity`, `source assurance` |
| Too literal | exact API method, route, event name, or file path in a cell | category phrase such as `contract boundary`, `compatibility proof` |
| Requirement restatement | a SHALL-style or test-case phrase | semantic type/category phrase |
| Source warning ignored | perspective omits known source-state caveat category | perspective mentions unresolved source-state caveats without particulars |

## Audit procedure

Audit after generating all Result tables and Matrix Summary.

Scan final cell values in:

- C Result and Summary C;
- F Result and Summary F;
- D Result and Summary D;
- K Result and Summary K;
- G Result and Summary G;
- X Result and Summary X;
- T Result and Summary T;
- E Result and Summary E.

Fail immediately if any final cell violates semantic product validity.

On audit FAIL:

1. Mark the run `FAIL`.
2. Do not repair, regenerate, or re-audit within the same run.
3. Do not advance status.
4. If `_SEMANTIC.md` is written, its header must show `Audit: FAIL`.
5. The run report must list matrix, cell, value, and reason.

On audit PASS:

1. Mark `_SEMANTIC.md` `Audit: PASS`.
2. Apply `STATUS_POLICY` exactly.
3. Run repo validator when available and permitted.
4. Report validator result or `validator not available`.

## Status policy checks

| Policy | Required behavior |
|---|---|
| `PRESERVE_CURRENT` | Do not change lifecycle state. Header/run report says state preserved by runtime policy. |
| `ADVANCE_ON_PASS` | On audit PASS, set/verify `SEMANTIC_READY` only if `_STATUS.md` edit is authorized. On FAIL, unchanged. |
| `NO_STATUS_TOUCH` | Do not edit `_STATUS.md` at all. |

No status regression is ever allowed.

## File-scope checks

| Check | Requirement |
|---|---|
| Production docs | Not modified. |
| `_CONTEXT.md` | Not modified. |
| `_REFERENCES.md` | Not modified. |
| `_DEPENDENCIES.md` | Not modified. |
| `MEMORY.md` | Not modified by this skill. |
| Sibling folders | Not read or written. |
| `_STATUS.md` | Modified only when status policy and TASK authorization allow it. |
| `_SEMANTIC.md` | Created/overwritten only inside `deliverable_folder`. |

## Failure reporting

| Situation | Report |
|---|---|
| `deliverable_folder` missing/not directory | `FAILED_INPUTS` |
| `_CONTEXT.md` missing | `FAILED_INPUTS` |
| `decomposition_path` omitted | `FAILED_INPUTS` |
| `ScopePath` and `deliverable_folder` disagree | `FAILED_INPUTS` |
| Required write target unauthorized | `FAILED_INPUTS` or TASK authorization violation, according to TASK rules |
| Production doc missing | Record absent; continue |
| `_REFERENCES.md` missing | Record not present; continue |
| `MEMORY.md` missing | Record not present; continue |
| Audit fail | `FAIL`, with matrix/cell/reason |
| Validator unavailable | Report unavailable; do not claim validator PASS |

## Success report

A clean run reports:

- `RUN_STATUS=SUCCESS` or the local TASK success token;
- deliverable ID/name;
- `DECOMP_VARIANT`;
- `_SEMANTIC.md` path;
- Audit PASS;
- validator PASS or validator unavailable;
- status policy and actual status action;
- no production document modifications;
- no out-of-scope writes;
- no failing cells.
