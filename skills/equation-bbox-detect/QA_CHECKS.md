# QA CHECKS — equation-bbox-detect

## Output presence

- Exactly one file exists at `OUTPUT_PATH` after the run.
- No other files outside the declared write boundary were created or modified.

## Output JSON schema

The output file is a single JSON object (not a list, not a JSON-lines stream) with this shape:

| Field | Type | Required | Constraint |
|---|---|---|---|
| `page` | int | yes | Equals `PAGE_NUM` from the brief; ≥ 1 |
| `equations` | list[obj] | yes | Possibly empty; one entry per detected display equation |
| `error` | str | conditional | Present only on `FAILED_INPUTS` runs |

### `equations[*]` entry schema

| Field | Type | Required | Constraint |
|---|---|---|---|
| `index` | int | yes | 1-based; strictly increasing within `equations` |
| `bbox_norm` | list[float] | yes | Exactly 4 elements: `[x0, y0, x1, y1]`; each in `[0.0, 1.0]`; `x0 < x1`; `y0 < y1` |
| `latex_excerpt` | str | optional | First ~20 chars of visible math content; freeform hint, not authoritative |

## Coordinate invariants

For every `bbox_norm = [x0, y0, x1, y1]`:

- `0.0 ≤ x0 < x1 ≤ 1.0`
- `0.0 ≤ y0 < y1 ≤ 1.0`
- The four values are floats (not ints, not strings).
- The box is reasonably "tight" around the equation: width and height should each be at least ~1% of the page (extremely small boxes are likely detection errors).
- The box width should be at most ~95% of the page width (a display equation spanning nearly the full width is plausible, but spanning 100% suggests the box accidentally included surrounding prose).
- The box height should be at most ~25% of the page height for typical single-line display equations; multi-line equations may go higher but are bounded by ~50% of the page.

## Ordering invariants

- `equations[*].index` is 1-based and strictly increasing: `1, 2, 3, ...` with no gaps.
- Boxes are ordered top-to-bottom on the page: for any two consecutive entries `e[i]` and `e[i+1]`, `e[i].bbox_norm[1] ≤ e[i+1].bbox_norm[1]` (entries earlier in the list start no lower than entries later in the list).

## Non-overlap invariants

- Two distinct entries should not significantly overlap. Compute pairwise IoU (intersection-over-union) on `bbox_norm`. Any pair with IoU > 0.1 is a detection error — the worker should have merged them into one box.
- A display equation may have an equation number (e.g., `(1.5)`) at the far-right margin. The worker may include the number inside the box OR exclude it — both are acceptable, but the choice must be consistent across the page.

## Cross-check semantics

When `EXPECTED_EQUATION_HASHES` is non-empty:

- `len(equations)` SHOULD equal `len(EXPECTED_EQUATION_HASHES)`. A mismatch is non-fatal (the worker emits whatever it sees on the raster, which is the source of truth for cropping), but the persona surfaces the discrepancy for human review at Gate 2.
- The persona pairs `equations[i].latex_excerpt` against the `i`-th equation hash by position; a wildly different excerpt suggests the worker's top-to-bottom ordering disagreed with the MD's order, OR the page contains equations that didn't appear in the MD's display-equation extraction.

The worker is NOT responsible for resolving cross-check mismatches. It emits its bbox findings; the persona reconciles.

## Failure reporting

The worker reports a structured `RUN_STATUS`:

- `SUCCESS` — at least one display equation detected; bboxes emitted; all invariants pass
- `NO_FINDINGS` — page contains no display equations; `equations` is `[]`; valid for some pages
- `FAILED_INPUTS` — required inputs were missing or malformed; `equations: []` with an `error` field
- `FAILED` — unexpected failure (image unreadable, write-boundary violation, etc.)

The worker also reports:

- `PAGE_NUM`
- `EQUATION_COUNT`

## Defects that block downstream

These defects block `crop_equation_regions.py` from emitting valid crops (the persona must re-dispatch this skill or surface the entry for human attention):

- Output file missing or unparseable as JSON
- Top-level `page` ≠ `PAGE_NUM` (would cause the crop tool to write to the wrong page's filename)
- Any `bbox_norm` not in [0,1] or violating `x0 < x1` / `y0 < y1`
- Non-monotonic or gapped `index` values
- Two entries with IoU > 0.5 (severe overlap implies the same equation got boxed twice)
- Output written to a path other than `OUTPUT_PATH`

## Required evidence

- Worker stdout / `RUN_STATUS` captured by TASK is sufficient evidence for routine success.
- For `FAILED` and `FAILED_INPUTS` runs, the explanation accompanying `RUN_STATUS` is the evidence; the persona decides whether to re-dispatch with corrected inputs.
- For `NO_FINDINGS` runs (page has no display equations), the empty `equations` list is the evidence — the persona simply skips cropping for that page.
- For visual-quality checks (boxes too tight / too loose / cropping body text), the produced PNG crops under `audit/equations/working/crops/` are the evidence; the persona reviews them at Gate 2 alongside the audit HTML.
