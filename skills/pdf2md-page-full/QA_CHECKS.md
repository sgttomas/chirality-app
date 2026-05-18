# pdf2md-page-full - QA Checks

Minimum checks for a valid run:

1. `IMAGE_PATH` exists and has a `.png` extension, or the skill returns
   `FAILED_INPUTS`.
2. `OUTPUT_MD_PATH` parent directory exists before write.
3. `OUTPUT_JSON_PATH` parent directory exists before write.
4. `OUTPUT_MD_PATH` exists after the run and is non-empty unless the page has no
   recoverable text, in which case it must contain the skill's failure marker.
5. `OUTPUT_JSON_PATH` exists after the run, is non-empty, and parses with
   `json.loads`.
6. No files other than `IMAGE_PATH` were read.
7. No files other than `OUTPUT_MD_PATH` and `OUTPUT_JSON_PATH` were written.

## Markdown checks

- Output is raw Markdown, not fenced in a Markdown code block.
- Reading order follows the visible page.
- Tables are transcribed as GFM or HTML tables and have a matching `[TABLE: ...]`
  placeholder.
- Figures use `[FIGURE: ...]` placeholders.
- Non-table/non-figure images use the descriptor placeholder forms defined in
  `SKILL.md`.

## JSON shape checks

The output JSON must include:

| Field | Requirement |
|---|---|
| `schema_version` | `pdf2md-page-assets/v1` |
| `run_status` | `SUCCESS`, `NO_ASSETS`, `FAILED`, or `FAILED_INPUTS` |
| `doc_stem` | Echo of runtime override |
| `page` | Echo of `PAGE_NUM` |
| `total_pages` | Echo of `TOTAL_PAGES` |
| `asset_policy` | Echo of `ASSET_POLICY` or default |
| `assets` | List, possibly empty |
| `issues` | List, possibly empty |

## Asset row checks

Each item in `assets` must satisfy the same canonical shape used by
`pdf2md-page-assets`:

- `kind` is exactly `fig`, `tbl`, or `img`.
- `ordinal` is a positive integer within `(page, kind)` reading order.
- `caption` is the visible caption or concise visual description.
- `bbox_norm` is `[x0, y0, x1, y1]` with normalized coordinates and strict
  ordering.
- `confidence` is `high`, `medium`, or `low`.
- `tbl` entries use structured `table_data` when legible, or
  `needs_extraction: true` with an issue when not safely transcribable.

## Failure posture

| Failure mode | Required output |
|---|---|
| Missing image or invalid output paths | Markdown failure marker plus JSON with `run_status: "FAILED_INPUTS"` |
| Page read succeeds but no assets exist | Markdown transcription plus JSON with `run_status: "NO_ASSETS"` and empty `assets` |
| Visual interpretation fails | Best-effort Markdown/failure marker plus JSON with `run_status: "FAILED"` and issue details |
