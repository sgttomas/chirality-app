# BRIEF SCHEMA — equation-bbox-detect

## Brief structure

The brief is an INIT-TASK shape rendered by `tools/equation_audit/build_equation_bbox_brief.py`. The worker receives the brief verbatim via TASK.

```yaml
PURPOSE: Detect display-equation bounding boxes on page <N> and emit normalized coordinates for downstream cropping
RequestedBy: EQUATION_AUDIT
ActingSurface: TASK+equation-bbox-detect

ScopePath: <absolute path to the page-work directory>
TaskSkill: equation-bbox-detect

AllowedWriteTargets:
  - "<OUTPUT_PATH>"

RuntimeOverrides:
  IMAGE_PATH: <absolute path to page_NNNN.png>
  PAGE_MD_PATH: <absolute path to per-page Markdown>
  PAGE_NUM: <int>
  OUTPUT_PATH: <absolute path to page_NNNN_eq_bboxes.json>
  EXPECTED_EQUATION_HASHES:
    - <12-hex>
    - <12-hex>
    # ... or `[]` if not provided

CustomInstructions:
  - Identify each DISPLAY equation visible on the page raster (block-level math, typically set off from running prose).
  - Do NOT box inline equations or symbols inside running text.
  - Emit normalized coordinates [x0,y0,x1,y1] in [0,1] relative to the page raster's width/height.
  - Boxes should tightly enclose the display equation without including the surrounding paragraph text.
  - The 'index' field is 1-based, ordered top-to-bottom on the page.
  - Include a 'latex_excerpt' field with the first ~20 characters of the visible LaTeX/symbolic content for cross-check against expected hashes.
  - If a page has no display equations, write {"page": <num>, "equations": []} and return RUN_STATUS=NO_FINDINGS.

ExpectedOutputs:
  - <OUTPUT_PATH>
```

## Required RuntimeOverrides

| Key | Type | Constraint |
|---|---|---|
| `IMAGE_PATH` | str | absolute path to existing `.png` file |
| `PAGE_MD_PATH` | str | absolute path to existing `.md` file |
| `PAGE_NUM` | int | ≥ 1; matches the `NNNN` in `IMAGE_PATH` |
| `OUTPUT_PATH` | str | absolute path; parent directory must exist; ends in `.json` |

## Optional RuntimeOverrides

| Key | Type | Constraint |
|---|---|---|
| `EXPECTED_EQUATION_HASHES` | list[str] | each element is a 12-lowercase-hex string |

## Output schema

The worker writes a single JSON object to `OUTPUT_PATH` matching the schema `tools/equation_audit/crop_equation_regions.py` consumes:

```json
{
  "page": 5,
  "equations": [
    {
      "index": 1,
      "bbox_norm": [0.12, 0.21, 0.85, 0.27],
      "latex_excerpt": "\\frac{2}{\\sqrt{3}} Y ="
    },
    {
      "index": 2,
      "bbox_norm": [0.18, 0.42, 0.78, 0.46],
      "latex_excerpt": "d\\epsilon/\\sigma ="
    }
  ]
}
```

When no display equations are found:

```json
{"page": 5, "equations": []}
```

On a failed run (inputs missing or malformed):

```json
{"page": 5, "equations": [], "error": "<short reason>"}
```

## Coordinate conventions

- Origin `(0, 0)` is top-left of the page raster.
- `(1, 1)` is bottom-right.
- `bbox_norm = [x0, y0, x1, y1]` where `x0 < x1` and `y0 < y1`.
- All four values are floats in the closed interval `[0.0, 1.0]`.
- The downstream consumer (`crop_equation_regions.py`) adds a small padding ring (default 0.005) before cropping, so the worker's boxes should be visually-tight rather than padded.

## Status reporting

The worker returns one of:

- `RUN_STATUS=SUCCESS` — at least one display equation detected; bboxes emitted
- `RUN_STATUS=NO_FINDINGS` — no display equations on this page; empty `equations` list emitted
- `RUN_STATUS=FAILED_INPUTS` — required inputs missing or malformed; partial JSON emitted with `error`
- `RUN_STATUS=FAILED` — unexpected failure

Plus: `PAGE_NUM`, `EQUATION_COUNT`.

## Cross-check semantics

When `EXPECTED_EQUATION_HASHES` is non-empty, the worker is expected to surface its findings in an order that allows the persona to cross-check `latex_excerpt` against the corresponding extracted equation:

- The persona pairs `equations[i].latex_excerpt` against the `i`-th equation in `equations.jsonl` for the page (both are top-to-bottom ordered).
- The persona does NOT require an exact match (page rasters are often slightly different from MD-extracted LaTeX), but flags large mismatches for human review.

The worker does NOT need to compute hashes itself. The `EXPECTED_EQUATION_HASHES` list is for the persona's cross-check after the dispatch completes.
