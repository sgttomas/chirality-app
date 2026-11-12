# equation-bbox-detect contract

## Brief

### Brief structure

The brief is an INIT-TASK shape rendered by `tools/equation_audit/build_equation_bbox_brief.py`. The worker receives the brief verbatim via TASK.

```yaml
PURPOSE: Detect display-equation bounding boxes on page <N> and emit normalized coordinates for downstream cropping
RequestedBy: WORKING_ITEMS
ParentWorkflow: equation-audit
ActingSurface: TASK+equation-bbox-detect

ScopePath: <absolute path to the page-work directory>
Workflow: equation-bbox-detect

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

### Required RuntimeOverrides

| Key | Type | Constraint |
|---|---|---|
| `IMAGE_PATH` | str | absolute path to existing `.png` file |
| `PAGE_MD_PATH` | str | absolute path to existing `.md` file |
| `PAGE_NUM` | int | ≥ 1; matches the `NNNN` in `IMAGE_PATH` |
| `OUTPUT_PATH` | str | absolute path; parent directory must exist; ends in `.json` |

### Optional RuntimeOverrides

| Key | Type | Constraint |
|---|---|---|
| `EXPECTED_EQUATION_HASHES` | list[str] | each element is a 12-lowercase-hex string |

### Output schema

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

### Coordinate conventions

- Origin `(0, 0)` is top-left of the page raster.
- `(1, 1)` is bottom-right.
- `bbox_norm = [x0, y0, x1, y1]` where `x0 < x1` and `y0 < y1`.
- All four values are floats in the closed interval `[0.0, 1.0]`.
- The downstream consumer (`crop_equation_regions.py`) adds a small padding ring (default 0.005) before cropping, so the worker's boxes should be visually-tight rather than padded.

### Status reporting

The worker returns one of:

- `RUN_STATUS=SUCCESS` — at least one display equation detected; bboxes emitted
- `RUN_STATUS=NO_FINDINGS` — no display equations on this page; empty `equations` list emitted
- `RUN_STATUS=FAILED_INPUTS` — required inputs missing or malformed; partial JSON emitted with `error`
- `RUN_STATUS=FAILED` — unexpected failure

Plus: `PAGE_NUM`, `EQUATION_COUNT`.

### Cross-check semantics

When `EXPECTED_EQUATION_HASHES` is non-empty, the worker is expected to surface its findings in an order that allows WORKING_ITEMS to cross-check `latex_excerpt` against the corresponding extracted equation:

- WORKING_ITEMS pairs `equations[i].latex_excerpt` against the `i`-th equation in `equations.jsonl` for the page (both are top-to-bottom ordered).
- WORKING_ITEMS does NOT require an exact match (page rasters are often slightly different from MD-extracted LaTeX), but flags large mismatches for human review.

The worker does NOT need to compute hashes itself. The `EXPECTED_EQUATION_HASHES` list is for WORKING_ITEMS’ cross-check after the dispatch completes.

## Acceptance

### Output presence

- Exactly one file exists at `OUTPUT_PATH` after the run.
- No other files outside the declared write boundary were created or modified.

### Output JSON schema

The output file is a single JSON object (not a list, not a JSON-lines stream) with this shape:

| Field | Type | Required | Constraint |
|---|---|---|---|
| `page` | int | yes | Equals `PAGE_NUM` from the brief; ≥ 1 |
| `equations` | list[obj] | yes | Possibly empty; one entry per detected display equation |
| `error` | str | conditional | Present only on `FAILED_INPUTS` runs |

#### `equations[*]` entry schema

| Field | Type | Required | Constraint |
|---|---|---|---|
| `index` | int | yes | 1-based; strictly increasing within `equations` |
| `bbox_norm` | list[float] | yes | Exactly 4 elements: `[x0, y0, x1, y1]`; each in `[0.0, 1.0]`; `x0 < x1`; `y0 < y1` |
| `latex_excerpt` | str | optional | First ~20 chars of visible math content; freeform hint, not authoritative |

### Coordinate invariants

For every `bbox_norm = [x0, y0, x1, y1]`:

- `0.0 ≤ x0 < x1 ≤ 1.0`
- `0.0 ≤ y0 < y1 ≤ 1.0`
- The four values are floats (not ints, not strings).
- The box is reasonably "tight" around the equation: width and height should each be at least ~1% of the page (extremely small boxes are likely detection errors).
- The box width should be at most ~95% of the page width (a display equation spanning nearly the full width is plausible, but spanning 100% suggests the box accidentally included surrounding prose).
- The box height should be at most ~25% of the page height for typical single-line display equations; multi-line equations may go higher but are bounded by ~50% of the page.

### Ordering invariants

- `equations[*].index` is 1-based and strictly increasing: `1, 2, 3, ...` with no gaps.
- Boxes are ordered top-to-bottom on the page: for any two consecutive entries `e[i]` and `e[i+1]`, `e[i].bbox_norm[1] ≤ e[i+1].bbox_norm[1]` (entries earlier in the list start no lower than entries later in the list).

### Non-overlap invariants

- Two distinct entries should not significantly overlap. Compute pairwise IoU (intersection-over-union) on `bbox_norm`. Any pair with IoU > 0.1 is a detection error — the worker should have merged them into one box.
- A display equation may have an equation number (e.g., `(1.5)`) at the far-right margin. The worker may include the number inside the box OR exclude it — both are acceptable, but the choice must be consistent across the page.

### Cross-check semantics

When `EXPECTED_EQUATION_HASHES` is non-empty:

- `len(equations)` SHOULD equal `len(EXPECTED_EQUATION_HASHES)`. A mismatch is non-fatal (the worker emits whatever it sees on the raster, which is the source of truth for cropping), but WORKING_ITEMS surfaces the discrepancy for human review at Gate 2.
- WORKING_ITEMS pairs `equations[i].latex_excerpt` against the `i`-th equation hash by position; a wildly different excerpt suggests the worker's top-to-bottom ordering disagreed with the MD's order, OR the page contains equations that didn't appear in the MD's display-equation extraction.

The worker is NOT responsible for resolving cross-check mismatches. It emits its bbox findings; WORKING_ITEMS reconciles.

### Failure reporting

The worker reports a structured `RUN_STATUS`:

- `SUCCESS` — at least one display equation detected; bboxes emitted; all invariants pass
- `NO_FINDINGS` — page contains no display equations; `equations` is `[]`; valid for some pages
- `FAILED_INPUTS` — required inputs were missing or malformed; `equations: []` with an `error` field
- `FAILED` — unexpected failure (image unreadable, write-boundary violation, etc.)

The worker also reports:

- `PAGE_NUM`
- `EQUATION_COUNT`

### Defects that block downstream

These defects block `crop_equation_regions.py` from emitting valid crops (WORKING_ITEMS must re-dispatch this workflow or surface the entry for human attention):

- Output file missing or unparseable as JSON
- Top-level `page` ≠ `PAGE_NUM` (would cause the crop tool to write to the wrong page's filename)
- Any `bbox_norm` not in [0,1] or violating `x0 < x1` / `y0 < y1`
- Non-monotonic or gapped `index` values
- Two entries with IoU > 0.5 (severe overlap implies the same equation got boxed twice)
- Output written to a path other than `OUTPUT_PATH`

### Required evidence

- Worker stdout / `RUN_STATUS` captured by TASK is sufficient evidence for routine success.
- For `FAILED` and `FAILED_INPUTS` runs, the explanation accompanying `RUN_STATUS` is the evidence; WORKING_ITEMS decides whether to re-dispatch with corrected inputs.
- For `NO_FINDINGS` runs (page has no display equations), the empty `equations` list is the evidence — WORKING_ITEMS simply skips cropping for that page.
- For visual-quality checks (boxes too tight / too loose / cropping body text), the produced PNG crops under `audit/equations/working/crops/` are the evidence; WORKING_ITEMS reviews them at Gate 2 alongside the audit HTML.

## Tool use

### Preferred tool order

This workflow is VLM-vision-reasoning over the page raster, optionally cross-checked against the per-page Markdown's equation list. There is no deterministic tool the worker runs from inside the dispatch. The surrounding pipeline runs deterministic tools (rasterization, equation extraction, brief building, cropping) outside the worker, on the orchestrator side.

### Allowed deterministic tools

#### Operationally invoked

The agent's native tools are available implicitly:

- `Read` — used to load `IMAGE_PATH` (multimodal PNG input) AND `PAGE_MD_PATH` (text input).
- `Write` — used to write the single `OUTPUT_PATH` JSON file.

No `Bash`, no shell-outs, no subprocess invocations.

### Surrounding deterministic tools (orchestrator-side, NOT worker-side)

| Tool | Owner | When |
|---|---|---|
| `tools/pdf2md/rasterize_pdf.py` | HELPS_HUMANS | pdf2md-orchestration Phase 1 — produces `page_NNNN.png` |
| `tools/equation_audit/audit_equations.py` | HELPS_HUMANS | equation-audit Phase 1 — extracts every display equation per page (text) and populates `EXPECTED_EQUATION_HASHES` |
| `tools/equation_audit/build_equation_bbox_brief.py` | HELPS_HUMANS | equation-audit Phase 1 — produces this workflow's brief |
| `tools/equation_audit/crop_equation_regions.py` | HELPS_HUMANS | equation-audit Phase 1 — consumes this workflow's output JSONs and emits per-equation PNG crops |

The worker never invokes any of the above. It writes its single JSON output; WORKING_ITEMS feeds it to `crop_equation_regions.py`.

### Expected use of reasoning

The worker uses VLM/text reasoning to:

1. **Read the page raster.** Use the multimodal `Read` tool to load `IMAGE_PATH`.
2. **Read the per-page Markdown for context.** Use the text `Read` tool to load `PAGE_MD_PATH`. The MD's `$$...$$` blocks indicate which equations to expect on this page.
3. **Identify display equations on the raster.** Distinguish display equations (centered, offset, often with equation numbers) from inline math (embedded in running prose). Display equations get boxed; inline math does NOT.
4. **Determine tight bounding rectangles.** For each display equation, find the smallest axis-aligned rectangle that fully encloses the equation's typeset content (including superscripts, subscripts, integral signs, etc.) but excludes surrounding paragraph text and equation numbers (when those appear in the far-right margin separately).
5. **Normalize coordinates.** Compute `[x0, y0, x1, y1]` as fractions of the page raster's width × height.
6. **Order top-to-bottom.** Assign 1-based `index` in vertical reading order.
7. **Capture a short excerpt.** Read the first ~20 characters of visible math content as `latex_excerpt` — for WORKING_ITEMS’ cross-check against `EXPECTED_EQUATION_HASHES`. This is a hint, not authoritative transcription.

### Disallowed use

- No deterministic tool invocation from inside the worker (no `Bash`, no `python3`, no shell-out, no subprocess).
- No writing outside `OUTPUT_PATH`.
- No reading outside `IMAGE_PATH` and `PAGE_MD_PATH`.
- No full transcription of equation content (that's `pdf2md-page`'s job).
- No boxing inline equations or symbols embedded in running prose.
- No boxing section headings, table cells, figure labels, page numbers, or running headers.
- No cross-page reasoning (one TASK = one page).
- No emission of pixel coordinates (normalized [0,1] only).
- No re-OCR of body text.

### Write boundary

Exactly one write per invocation:

```
<OUTPUT_PATH>
```

The path is absolute. Parent directory must exist; this workflow does not create directories.

If a write would violate the boundary, the worker returns `RUN_STATUS=FAILED` with an explanatory note and does NOT attempt a workaround.
