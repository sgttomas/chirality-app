# pdf2md-page-assets - QA Checks

Minimum checks for a valid run:

1. `IMAGE_PATH` exists and has a `.png` extension, or the skill returns `FAILED_INPUTS`.
2. `PAGE_MD_PATH` exists and has a `.md` extension, or the skill returns `FAILED_INPUTS`.
3. `OUTPUT_PATH` parent directory exists before write.
4. `OUTPUT_PATH` exists after the run and is non-empty.
5. `OUTPUT_PATH` parses with `json.loads`.
6. No files other than `IMAGE_PATH` and `PAGE_MD_PATH` were read.
7. No files other than `OUTPUT_PATH` were written.

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

Each item in `assets` must satisfy:

| Field | Requirement |
|---|---|
| `kind` | Exactly `fig`, `tbl`, or `img` (STRICT: aliases like `figure`/`image`/`table`/`diagram`/`plot`/`chart`/`logo`/`photo` are rejected by the downstream `materialize_page_assets.py`; alternate keys `type`/`subtype` are also rejected) |
| `ordinal` | Positive integer within `(page, kind)` reading order |
| `caption` | Visible caption or concise visual description (STRICT: `caption` is the ONLY accepted field name — `title`/`label`/`name` are rejected) |
| `slug` | Short ASCII-friendly advisory slug, or blank if uncertain |
| `bbox_norm` | Four numbers `[x0, y0, x1, y1]`, top-left origin, each in `[0,1]`, with `x0 < x1` and `y0 < y1` (STRICT: must be a JSON array, NOT a dict `{"x0": ..., ...}`) |
| `confidence` | `high`, `medium`, or `low` |
| `table_data` | Required for `tbl` when legible — structured object conforming to the `pdf2md-table/v1` schema in `SKILL.md` (STRICT: the legacy `csv_text` / `table_csv` fields are rejected by `materialize_page_assets.py`) |
| `needs_extraction` | Boolean, required on `tbl` entries that are visible but cannot be safely transcribed; in that case `table_data` MUST be omitted and an `issue` (e.g. `table_unreadable`) MUST be present |

### `table_data` structural checks

When a `tbl` entry carries a `table_data` block, the materializer enforces:

- `schema_version` is exactly `"pdf2md-table/v1"`.
- `rows` is a non-empty JSON array; each row is `{"cells": [...]}` with `cells` a JSON array.
- `header_rows` is an integer in `[0, len(rows)]`.
- Every index in `section_dividers` is in `[0, len(rows))`.
- For each cell: `value` present; `row_span`/`col_span` (if present) are integers ≥ 1; `type` (if present) is one of `text|number|fraction|missing|formula|boolean`; `is_header` (if present) is boolean.
- Every `footnote_markers` entry on any cell appears in the table-level `footnotes` array's `marker` set.
- No row's `row_span` extends across a `section_dividers` boundary.
- `continuation_of` is either `null` or an object with `doc_stem` (string), `page` (int), `tbl_ordinal` (int).

## Top-level shape strictness enforced downstream

`tools/pdf2md/materialize_page_assets.py` validates and aborts with an explicit error pointing at the SKILL contract if any of these shape defects are present:

- Top-level not a JSON object (must be a dict, not a list or scalar).
- Missing `assets` key.
- Sibling-keys legacy: `tables`, `figures`, or `images` appearing alongside `assets` at the top level. The canonical shape is the flat `assets: [...]` array; tables / figures / images are entries with `kind: "tbl" | "fig" | "img"`.
- `assets` not a JSON array.

The page-number field is `page` (not `page_num`).

## Inline placeholder drift (consumed by rewrite_inline_asset_refs.py)

The page Markdown emitted by the **`pdf2md-page` skill** (not this skill) carries the inline asset placeholders. Those placeholders MUST follow RULE 8 in `skills/pdf2md-page/SKILL.md`:

- `[FIGURE: <caption>]` — uppercase `FIGURE:` prefix is required.
- `[TABLE: <caption>]` — uppercase `TABLE:` prefix; appears immediately above the GFM/HTML transcription.
- `[<descriptor> <suffix>]` where suffix is one of `logo`/`emblem`/`seal`/`cover`/`photograph`/`photo`/`image`.

`tools/pdf2md/rewrite_inline_asset_refs.py` only rewrites these canonical shapes. Drift forms (e.g., `![Fig. 1.9 ...]` markdown-image syntax, bare-bracketed `[Fig. 1.1 ...]` without the `FIGURE:` prefix, lowercase prefixes) are surfaced as warnings on stderr — not silently rewritten — so the orchestrator and human reviewers can see when the `pdf2md-page` skill drifts from RULE 8.

## Failure posture

| Failure mode | Required output |
|---|---|
| Missing input file | `run_status: "FAILED_INPUTS"`, empty `assets`, issue naming the missing input |
| No extractable assets | `run_status: "NO_ASSETS"`, empty `assets`, no invented placeholders |
| Unreadable page image | `run_status: "FAILED"`, empty `assets`, issue explaining the problem |
| Partial table uncertainty | `run_status: "SUCCESS"` with the table entry carrying `needs_extraction: true`, NO `table_data` block, and an explicit issue such as `table_unreadable` or `possible_continuation` |

## Orchestrator-side checks

These checks belong to `PDF2MD`, not this skill:

- Running `materialize_page_assets.py` on every page asset JSON.
- Confirming crop PNGs exist for all non-skipped figure/image/table records.
- Confirming table XLSX files exist for table records that carry a `table_data` block (records flagged `needs_extraction: true` are exempt and do not require an XLSX).
- Aggregating the document asset manifest.
- Running `validate_assets.py` against the final assembled Markdown.
- Treating unresolved asset references as degraded output requiring human acknowledgment before downstream use.
