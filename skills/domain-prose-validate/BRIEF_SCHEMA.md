# domain-prose-validate - Brief Schema

Use this skill with `TASK` like this. It is normally spawned by the Gate 1.5-P Stage 1 orchestration helper (one TASK per page, fanned out in parallel):

```md
PURPOSE: Independently re-extract one PDF page's prose, equations, and asset placeholders for Gate 1.5-P comparison
RequestedBy: DOMAIN_DECOMP (Gate 1.5-P Stage 1)

ScopePath: /abs/path/to/_Sources/BookX
TaskSkill: domain-prose-validate

Tasks:
  - Read one page raster and the asset bbox hints for that page
  - Produce an independent Markdown re-extract: prose, $$...$$ display equations, and [FIGURE:]/[TABLE:]/[IMAGE:] placeholders in reading order
  - Do not read any pre-existing per-page Markdown or the assembled book Markdown

ApplyEdits: true

AllowedWriteTargets:
  - "/abs/path/to/_Sources/BookX/audit/prose_validation_extracts/page_0047.reextract.md"

RuntimeOverrides:
  IMAGE_PATH: /abs/path/to/_Sources/BookX_pdf2md_work/page_0047.png
  ASSET_BBOX_HINTS_PATH: /abs/path/to/_Sources/BookX/audit/prose_validation_extracts/page_0047.hints.json
  OUTPUT_PATH: /abs/path/to/_Sources/BookX/audit/prose_validation_extracts/page_0047.reextract.md
  PAGE_NUM: 47

ExpectedOutputs:
  - /abs/path/to/_Sources/BookX/audit/prose_validation_extracts/page_0047.reextract.md
```

## Required fields

| Field | Value | Notes |
|---|---|---|
| `TaskSkill` | `domain-prose-validate` | Must match skill folder name |
| `RuntimeOverrides.IMAGE_PATH` | Absolute path to the page PNG | Must exist, must have `.png` extension |
| `RuntimeOverrides.ASSET_BBOX_HINTS_PATH` | Absolute path to the per-page bbox-hints JSON | Must exist, must have `.json` extension |
| `RuntimeOverrides.OUTPUT_PATH` | Absolute path to the `.reextract.md` file | Parent directory must exist |
| `RuntimeOverrides.PAGE_NUM` | 1-indexed page number | Positive integer |

## Optional fields

None. Stage 1 has no policy knobs; all knobs (canonicalization version, noise floor, equation-content threshold) live in Stage 2's deterministic comparator.

## TaskProfile

`NONE` - this skill runs in generic TASK shell mode without a profile.

## Read boundary

The skill reads only:

- `{IMAGE_PATH}`
- `{ASSET_BBOX_HINTS_PATH}`

It must **not** read any pre-existing `page_*.md`, the assembled `<book>.md`, neighbouring page images, sibling manifests, or audit sidecars. Reading the original extract would defeat the confirmation-bias break that is the entire point of Gate 1.5-P Stage 1.

## Write boundary

The skill writes only:

- `{OUTPUT_PATH}`

## Output format

`OUTPUT_PATH` is a Markdown file containing the page body only (no frontmatter, no `# Page N` heading, no metadata):

- Prose paragraphs in reading order, preserving printed line breaks within paragraphs.
- Display equations as `$$...$$` blocks on their own line(s) at the reading-order position.
- Inline equations as `$...$` within prose.
- Asset placeholders on their own line in the canonical form:
  - `[FIGURE: <caption text as printed>]`
  - `[TABLE: <caption text as printed>]`
  - `[IMAGE: <one-line visual description>]`
- File ends with a single trailing newline.

## `ASSET_BBOX_HINTS_PATH` shape

```json
{
  "page": 47,
  "assets": [
    {"kind": "fig", "asset_id": "BookX_p0047_fig01", "bbox_norm": [0.1, 0.2, 0.9, 0.5]},
    {"kind": "tbl", "asset_id": "BookX_p0047_tbl01", "bbox_norm": [0.1, 0.55, 0.9, 0.85]}
  ]
}
```

Hints are consumed for **guidance only** — to set expectations about which placeholder kinds appear and where. `asset_id` MUST NOT appear in the output Markdown. Caption text comes from the raster, not the hints file.

## AllowedTools

Omit `AllowedTools`. This is a VLM-reasoning-only skill with no deterministic tool dependencies.

## CustomInstructions

Usually unnecessary. If used, keep them run-specific and do not restate the whole skill contract. Good examples:

- "Two-column page: emit left column fully before right column."
- "Page has a marginal footnote rule — emit footnote text as a final paragraph after the body prose."
- "If a table caption is in a non-Latin script, transliterate inside the `[TABLE: ...]` placeholder and add `(transliterated)`."
