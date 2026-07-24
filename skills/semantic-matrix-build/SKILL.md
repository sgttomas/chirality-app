---
name: semantic-matrix-build
description: Generate one deliverable-local semantic lens (_SEMANTIC.md) by adopting canonical matrices A and B and deriving C, F, D, K, G, X, T, and E with explicit semantic-algebra working.
compatibility: Chirality TASK generic shell; normally dispatched by PROJECT_SETUP setup pipeline Phase 2.3 with ScopePath set to one deliverable folder.
metadata:
  chirality-skill-version: "2"
  chirality-task-profile: NONE
---

# SKILL — semantic-matrix-build

## Purpose

Generate `_SEMANTIC.md`, a deliverable-local semantic lens for one production unit.

The lens is **deliverable-conditioned**: `_CONTEXT.md` and production documents shape the vocabulary and perspective. The lens is **not deliverable-literal**: matrix cells are semantic categories, types, behaviors, and values, not restated requirements, implementation details, code clauses, file paths, event-name lists, numbers, or engineering judgments.

Each run starts from canonical Matrix A and Matrix B, then derives exactly these matrices in order:

`C, F, D, K, G, X, T, E`

The output is one file:

`{deliverable_folder}/_SEMANTIC.md`

## Runtime shell

Use `TASK` in generic shell mode with `ScopePath` set to the deliverable folder. This skill is fully controlled by its brief and method contract.

Normal dispatch shape:

```yaml
TaskSkill: semantic-matrix-build
ScopePath: /absolute/path/to/one/deliverable-folder
RuntimeOverrides:
  deliverable_folder: /absolute/path/to/one/deliverable-folder
  decomposition_path: /absolute/path/to/decomposition.md
  DECOMP_VARIANT: SOFTWARE
  STATUS_POLICY: PRESERVE_CURRENT
```

## Method boundary

This skill is a method pack loaded by TASK. It is not a persona agent.

The skill may narrow runtime behavior but must not widen the effective bounded task brief's write authorization. If TASK and this skill disagree about write authorization or tool use, the narrower instruction wins and the run report must surface the contradiction.

## Precedence

1. TASK hard authorization boundary and active brief
2. This SKILL.md method contract
3. QA_CHECKS.md validity contract
4. TOOL_POLICY.md tool contract
5. BRIEF_SCHEMA.md dispatch examples

If instructions conflict, do not silently reconcile. Report the contradiction.

## Inputs

### Required

- `ScopePath` — TASK local scope root; must resolve to the same folder as `deliverable_folder`.
- `deliverable_folder` — absolute path to exactly one deliverable / production unit folder.
- `decomposition_path` — absolute path to the decomposition document used for traceability only.

### Required runtime override

- `DECOMP_VARIANT` — `PROJECT`, `SOFTWARE`, or `DOMAIN`.

If absent, default to `PROJECT`, but report the default in the run report.

- `PRODUCTION_FORMAT` — resolver-selected `LEGACY_FOUR_DOC`, `SOW_V1`, or
  authorized `MIGRATION_DUAL`. Dual mode also requires `FORMAT_AUTHORITY_REF`, an exact
  in-scope path, and `STATUS_POLICY=NO_STATUS_TOUCH`; otherwise fail closed.

### Status policy runtime override

`STATUS_POLICY` controls `_STATUS.md` behavior.

| Value | Meaning |
|---|---|
| `PRESERVE_CURRENT` | Default for PROJECT_SETUP Phase 2.3. Do not change lifecycle state. Record the ruling in `_SEMANTIC.md` and the run report. |
| `ADVANCE_ON_PASS` | On audit PASS, set or verify `Current State: SEMANTIC_READY`, but only if TASK write authorization allows `_STATUS.md` edits. |
| `NO_STATUS_TOUCH` | Do not edit `_STATUS.md` at all. Record status untouched in `_SEMANTIC.md` and the run report. |

If `STATUS_POLICY=ADVANCE_ON_PASS` but `_STATUS.md` editing is not authorized by TASK/brief, do not edit status. Report `NEEDS_HUMAN_RULING` or `FAILED_INPUTS` according to TASK's run-report convention.

## Files to read

Read only inside `deliverable_folder`, except the decomposition document used for traceability.

Read in this order when present:

1. `_CONTEXT.md` — required. If missing, fail with `FAILED_INPUTS`.
2. `_STATUS.md` — lifecycle state and phase history.
3. `_REFERENCES.md` — source corpus and source-state warnings.
4. `_DEPENDENCIES.md` — dependency notes; do not infer blockers from it.
5. `MEMORY.md` — if absent, record `not present` in Inputs Read.
6. Production documents:
   - `PROJECT` / `SOFTWARE`: `Datasheet.md`, `Specification.md`, `Guidance.md`, `Procedure.md`
   - `SOW_V1` or authorized `MIGRATION_DUAL`: `ScopeOfWork.md`; treat its four named
     philosophical sections and registered IDs as the production contract.
   - `DOMAIN`: all non-metadata `.md` files not prefixed with `_`, typically `Scoping.md` and `KA-*.md`

Missing production documents are recorded as absent; they do not fail the run. Do not read sibling deliverable folders. Do not compare across deliverables.
The resolver must select exactly one accepted format. `MIGRATION_DUAL`
requires exact path-scoped authority; missing, partial, invalid, ambiguous, or
unauthorized dual input fails closed.

## Write scope

May write only inside `deliverable_folder`:

- `_SEMANTIC.md` — primary output; overwrite allowed.
- `_STATUS.md` — only if `STATUS_POLICY` requires it and TASK/brief authorizes it.

Never modify production documents, `_CONTEXT.md`, `_REFERENCES.md`, `_DEPENDENCIES.md`, `MEMORY.md`, or files outside the scope.

## Deliverable perspective

Write a 1–3 sentence Perspective near the top of `_SEMANTIC.md`.

The Perspective must:

- name what the deliverable is for at a semantic level;
- identify the kinds of knowledge the lens must carry;
- include relevant source-state caveats at a category level when present;
- avoid engineering correctness claims;
- avoid exact code clauses, exact event-name lists, exact file paths, line numbers, implementation paths, and other particulars.

Good pattern:

> This deliverable frames the runtime boundary as a product-owned contract that keeps adapter behavior replaceable while preserving product-owned turn semantics. Its knowledge must carry API shape, adapter quarantine, event compatibility, conformance expectations, and unresolved source-state caveats without treating provider-specific details as public authority.

Bad patterns:

- Too generic: “This deliverable creates a semantic lens for knowledge work.”
- Too literal: “This deliverable validates `session:init`, `chat:delta`, and `/api/...` by implementing file X.”

## Semantic product style

Final matrix cells must be:

- deliverable-conditioned;
- category-level, not requirement-level;
- one phrase only;
- 2–5 words;
- preferably 2–3 words when meaning remains complete;
- free of row/column axis labels;
- free of `∩`, `Σ`, unresolved `+`, or raw formula text.

Target style examples:

| Too generic | Too literal | Better |
|---|---|---|
| adequate evidence | SDK-backed adapter test output | runtime proof |
| complete record | route/SSE event preservation checklist | compatibility record |
| quality review | acceptance of exact PRD hash warning | source-state assurance |
| process audit | Section 8 harness CI premerge summary | summary integrity check |

## Semantic algebra

### Multiplication `*`

Semantic multiplication combines two semantic units into their intersection.

Examples:

- `sufficient * reason = justification`
- `necessary * condition = prerequisite`
- `practical * knowledge = skill`

### Addition `+`

Semantic addition groups terms into a collection. It must not leak into final cell values.

### Interpretation `I(r, c, L)`

Every list-valued cell must be interpreted into one atomic semantic unit.

For every interpreted cell, show exactly these three steps.

#### Step 1 — Axis anchor

Compute and resolve the axis product:

`a = r * c = <resolved anchor phrase>`

The anchor phrase should be semantic, not merely `<row>-<column> coordinate frame`.

Example:

`normative * necessity = binding need`

#### Step 2 — Projected contributors

For every contributor `t_n` in `L`, compute and resolve:

`p_n = a * t_n = <anchor phrase> * <contributor phrase> = <resolved projection phrase>`

A projection that only restates the formula is incomplete. Each projection must have a resolved phrase before Step 3.

Good:

`p1 = binding need * policy fact = rule entry`

Bad:

`p1 = (normative * necessity) * (policy threshold * essential fact)`

#### Step 3 — Centroid attractor

Select one final cell phrase:

`centroid selects <final phrase>`

The phrase must capture the shared semantic core of all resolved projections. It must not enumerate contributors.

## Matrix construction rules

### Matrix A — Orientation (canonical, 3×4)

Use these exact values. Do not derive or edit them.

| | **guiding** | **applying** | **judging** | **reviewing** |
|---|---|---|---|---|
| **normative** | prescriptive direction | mandatory practice | compliance determination | regulatory audit |
| **operative** | procedural direction | practical execution | performance assessment | process audit |
| **evaluative** | value orientation | merit application | worth determination | quality appraisal |

### Matrix B — Conceptualization (canonical, 4×4)

Use these exact values. Do not derive or edit them.

| | **necessity** | **sufficiency** | **completeness** | **consistency** |
|---|---|---|---|---|
| **data** | essential fact | adequate evidence | comprehensive record | reliable measurement |
| **information** | essential signal | adequate context | comprehensive account | coherent message |
| **knowledge** | fundamental understanding | competent expertise | thorough mastery | coherent understanding |
| **wisdom** | essential discernment | adequate judgment | holistic insight | principled reasoning |

### Matrix C — Formulation (3×4)

Columns: `necessity`, `sufficiency`, `completeness`, `consistency`  
Rows: `normative`, `operative`, `evaluative`

Formula:

`L_C(i,j) = Σ_k (A(i,k) * B(k,j))`  
`C(i,j) = I(row_i, col_j, L_C(i,j))`

### Matrix F — Requirements (3×4)

Columns: `necessity`, `sufficiency`, `completeness`, `consistency`  
Rows: `normative`, `operative`, `evaluative`

Formula:

`L_F(i,j) = Σ_k (C(i,k) * B(k,j))`  
`F(i,j) = I(row_i, col_j, L_F(i,j))`

### Matrix D — Objectives (3×4)

Columns: `guiding`, `applying`, `judging`, `reviewing`  
Rows: `normative`, `operative`, `evaluative`

Formula:

`L_D(i,j) = A(i,j) + (resolution * F(i,j))`  
`D(i,j) = I(row_i, col_j, L_D(i,j))`

For D, use exactly two contributors in `L_D`: the A cell and the resolution-transformed F cell.

### Matrix K — Transpose of D (4×3)

Formula:

`K(i,j) = D(j,i)`

Rows: `guiding`, `applying`, `judging`, `reviewing`  
Columns: `normative`, `operative`, `evaluative`

### Matrix G — Truncation of B (3×4)

Formula:

Remove the `wisdom` row from B.

Rows: `data`, `information`, `knowledge`  
Columns: `necessity`, `sufficiency`, `completeness`, `consistency`

### Matrix X — Verification (4×4)

Rows: `guiding`, `applying`, `judging`, `reviewing`  
Columns: `necessity`, `sufficiency`, `completeness`, `consistency`

Formula:

`L_X(i,j) = Σ_k (K(i,k) * G(k,j))`  
`X(i,j) = I(row_i, col_j, L_X(i,j))`

### Matrix T — Transpose of B (4×4)

Formula:

`T(i,j) = B(j,i)`

Rows: `necessity`, `sufficiency`, `completeness`, `consistency`  
Columns: `data`, `information`, `knowledge`, `wisdom`

### Matrix E — Evaluation (4×4)

Rows: `guiding`, `applying`, `judging`, `reviewing`  
Columns: `data`, `information`, `knowledge`, `wisdom`

Formula:

`L_E(i,j) = Σ_k (X(i,k) * T(k,j))`  
`E(i,j) = I(row_i, col_j, L_E(i,j))`

## Output format

Write `_SEMANTIC.md` in this order.

```markdown
# Semantic Lens: [ID] [Name]

**Generated:** [YYYY-MM-DD]
**DECOMP_VARIANT:** [PROJECT|SOFTWARE|DOMAIN]
**Perspective:** [1–3 sentences]
**Framework:** Chirality Semantic Algebra
**Audit:** [PASS|FAIL]
**Phase 2.3 Ruling:** [status policy statement]
**Inputs Read:**
- _CONTEXT.md — [SourceRef]
- _STATUS.md — [SourceRef or not present]
- _REFERENCES.md — [SourceRef or not present]
- _DEPENDENCIES.md — [SourceRef or not present]
- MEMORY.md — [SourceRef or not present]
- Datasheet.md — [SourceRef or absent]
- Specification.md — [SourceRef or absent]
- Guidance.md — [SourceRef or absent]
- Procedure.md — [SourceRef or absent]
- [DOMAIN files if applicable] — [SourceRef]

## Matrix A — Orientation (3x4) — Canonical
[canonical table]

## Matrix B — Conceptualization (4x4) — Canonical
[canonical table]

## Matrix C — Formulation (3x4)
### Construction: Dot product A · B
Intermediate collection and interpretation work for `L_C(i,j) = Σ_k (A(i,k) * B(k,j))`.
[work table]
### Result
[result table]

## Matrix F — Requirements (3x4)
...

## Matrix D — Objectives (3x4)
...

## Matrix K — Transpose of D (4x3)
...

## Matrix G — Truncation of B (3x4)
...

## Matrix X — Verification (4x4)
...

## Matrix T — Transpose of B (4x4)
...

## Matrix E — Evaluation (4x4)
...

---

## Matrix Z — Summary Boundary

This delimiter prevents summary tables from being parsed as part of Matrix E result work. It is not a semantic matrix.

## Matrix Summary

[All eight matrices C, F, D, K, G, X, T, E as compact markdown tables. No bullets. No derivation.]
```

### Work table format

Use this table shape for C, F, D, X, and E:

| Cell | Intermediate collection | Step 1 - Axis anchor | Step 2 - Projected contributors | Step 3 - Centroid attractor |
|---|---|---|---|---|
| C[normative,necessity] | ... | `normative * necessity = binding need` | `p1 = binding need * directive fact = source mandate`; ... | centroid selects `policy threshold` |

Requirements:

- The Cell label may contain row and column names.
- The final Result cell value must not contain row or column names.
- Step 2 must resolve every projected contributor into a phrase.
- Step 3 must name exactly one final phrase.

## SourceRef convention

Each `Inputs Read` line must use one of:

- absolute path + best-effort heading anchor;
- relative path + heading anchor when absolute path is unavailable;
- `not present`;
- `absent`;
- `location TBD` only when the file was read but no anchor can be determined.

Do not claim an input was read unless it was actually read.

## Audit before acceptance

Before reporting success, audit all final cell values in:

- every Result table for C, F, D, K, G, X, T, and E;
- every Matrix Summary table.

Fail the run if any final cell:

1. is empty;
2. is not one phrase;
3. is under 2 words or over 5 words, except canonical B/G/T cells inherited from B;
4. exceeds about 80 characters;
5. contains `∩` or `Σ`;
6. contains unresolved `+` between semantic terms;
7. contains a literal row or column axis token for that cell;
8. contains implementation particulars, exact event names, file paths, code clauses, numeric requirements, equipment tags, or engineering correctness claims.

If audit fails:

- mark `_SEMANTIC.md` Audit as `FAIL` if the file is written;
- do not advance status;
- do not repair and re-audit in the same run;
- report failing matrix/cell/reason in the TASK run report.

## Status handling

After audit:

- `STATUS_POLICY=PRESERVE_CURRENT`: do not change current lifecycle state. If `_STATUS.md` history edits are authorized, append a history note that semantic matrix was generated/validated and state was preserved by runtime policy. Otherwise only record this in `_SEMANTIC.md` and the run report.
- `STATUS_POLICY=ADVANCE_ON_PASS`: on audit PASS, set/verify `SEMANTIC_READY` only when `_STATUS.md` editing is authorized. On audit FAIL, leave state unchanged.
- `STATUS_POLICY=NO_STATUS_TOUCH`: do not edit `_STATUS.md`.

Never regress status.

## Run report

TASK's normal run report must include:

- `RUN_STATUS`
- deliverable ID/name
- resolved `deliverable_folder`
- `DECOMP_VARIANT`
- `_SEMANTIC.md` path
- audit PASS/FAIL
- status policy and actual status action
- validator result if the repo validator was available and run
- missing inputs
- failing cells, if any
- confirmation that production documents were not modified

## Validator

When running inside a repo that contains the validator and tool use is permitted, run:

```sh
python3 tools/validation/validate_semantic_matrix.py "{deliverable_folder}"
```

If the validator is unavailable, do not claim validator PASS. Report `validator not available`.

## DOMAIN variant note

The skill can run on `DOMAIN` folders only when explicitly dispatched. Standard PROJECT_SETUP DOMAIN setup may skip semantic lensing entirely. If invoked for DOMAIN, read the Knowledge Type's non-metadata markdown documents and use DOMAIN terminology in the header and perspective. The matrix algebra remains unchanged.
