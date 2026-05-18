# pdf2md-folio-extract - QA Checks

Minimum checks for a valid run:

1. `IMAGE_PATH` exists and has a `.png` extension, or the skill returns `FAILED_INPUTS`.
2. `OUTPUT_PATH` parent directory exists before write.
3. `OUTPUT_PATH` exists after the run and is non-empty.
4. `OUTPUT_PATH` parses with `json.loads`.
5. No files other than `IMAGE_PATH` were read.
6. No files other than `OUTPUT_PATH` were written.

## JSON shape checks

The output JSON must include exactly these top-level fields:

| Field | Requirement |
|---|---|
| `schema_version` | Exactly `"pdf2md-folio-extract/v1"` |
| `run_status` | One of `"SUCCESS"`, `"NO_FOLIO"`, `"FAILED"`, `"FAILED_INPUTS"` |
| `page` | Integer; equals runtime `PAGE_NUM` (field name is `page`, NOT `page_num`) |
| `page_label` | JSON string when `run_status == "SUCCESS"`, JSON `null` otherwise |
| `page_label_source` | Exactly `"vlm"` |
| `location` | One of `"top-left"`, `"top-center"`, `"top-right"`, `"bottom-left"`, `"bottom-center"`, `"bottom-right"` when `page_label` is a string; JSON `null` otherwise |
| `confidence` | One of `"high"`, `"medium"`, `"low"` |
| `rationale` | Non-empty string; one short sentence |

## Field-value strictness

- `schema_version` is a literal — `"pdf2md-folio/v1"`, `"v1"`, or other shortened forms are rejected.
- `run_status` uppercase literals only — `"ok"`, `"success"`, `"none"`, `"done"` are rejected.
- `page_label` MUST be the verbatim visible glyph; downstream tools rely on the exact surface form:
  - Roman numerals stay Roman (`"xiv"`, not `"14"`).
  - Case is preserved (`"xiv"` vs. `"XIV"`).
  - Section prefixes are kept (`"B-3"`, not `"3"`).
  - No zero-padding (`"7"`, not `"007"`).
- `page_label_source` is always the literal `"vlm"` from this skill, including on failure rows.
- `location` and `page_label` co-vary: both are `null` together, or both are non-null together. A `null` `page_label` with a non-null `location` is invalid, and vice versa.

## Folio-invention guard

The most important QA invariant for this skill:

- A `SUCCESS` row's `page_label` MUST be visible on the page image.
- It MUST NOT be derived from `PAGE_NUM` (the physical sequence index).
- It MUST NOT be inferred from neighbouring pages' numbering.
- When no folio is visibly printed, the correct emission is `NO_FOLIO` with `page_label: null` and `location: null` — never a fabricated label.

## Failure posture

| Failure mode | Required output |
|---|---|
| Missing or wrong-extension `IMAGE_PATH` | `run_status: "FAILED_INPUTS"`, `page_label: null`, `location: null`, rationale naming the missing input |
| `OUTPUT_PATH` parent directory missing | `run_status: "FAILED_INPUTS"`, `page_label: null`, `location: null`, rationale naming the issue |
| No folio printed on the page | `run_status: "NO_FOLIO"`, `page_label: null`, `location: null`, rationale explaining (blank page / cover / chapter opener / etc.) |
| Page image unreadable or corrupt | `run_status: "FAILED"`, `page_label: null`, `location: null`, rationale explaining the problem |

## Orchestrator-side checks

These checks belong to `PDF2MD`, not this skill:

- Running the folio-extract skill across every page in parallel.
- Aggregating per-page folio JSON into a document-level folio map.
- Reconciling Roman-numeral front matter against Arabic body numbering.
- Detecting suspicious jumps in the folio sequence and surfacing them for review.
- Propagating `page_label` into downstream per-page asset records.
- Treating unresolved or contradictory folio reports as degraded output requiring human acknowledgment before downstream use.
