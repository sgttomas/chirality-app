# pdf2md-page-assets - Brief Schema

Use this skill with `TASK` like this. It is normally spawned by the `PDF2MD` orchestrator after the page has been transcribed and cleaned:

```md
PURPOSE: Identify extractable prose-document assets on one PDF page
RequestedBy: PDF2MD

ScopePath: /abs/path/to/pdf_work_dir
TaskSkill: pdf2md-page-assets

Tasks:
  - Read one page raster and its clean Markdown context
  - Identify visible figures, tables, and other meaningful images
  - Emit bbox-normalized asset records and table CSV text per the skill contract

ApplyEdits: true

AllowedWriteTargets:
  - "/abs/path/to/pdf_work_dir/page_0003_assets.json"

RuntimeOverrides:
  IMAGE_PATH: /abs/path/to/pdf_work_dir/page_0003.png
  PAGE_MD_PATH: /abs/path/to/pdf_work_dir/page_0003.md
  OUTPUT_PATH: /abs/path/to/pdf_work_dir/page_0003_assets.json
  DOC_STEM: MWK_1956
  PAGE_NUM: 3
  TOTAL_PAGES: 386
  ASSET_POLICY: prose-document-assets-v1

ExpectedOutputs:
  - /abs/path/to/pdf_work_dir/page_0003_assets.json
```

## Required fields

| Field | Value | Notes |
|---|---|---|
| `TaskSkill` | `pdf2md-page-assets` | Must match skill folder name |
| `RuntimeOverrides.IMAGE_PATH` | Absolute path to the page PNG | Must exist, must have `.png` extension |
| `RuntimeOverrides.PAGE_MD_PATH` | Absolute path to clean page Markdown | Must exist, must have `.md` extension |
| `RuntimeOverrides.OUTPUT_PATH` | Absolute path to page asset JSON | Parent directory must exist |
| `RuntimeOverrides.DOC_STEM` | Document stem | Used for context only; deterministic tools assign final IDs |
| `RuntimeOverrides.PAGE_NUM` | 1-indexed page number | Positive integer |
| `RuntimeOverrides.TOTAL_PAGES` | Total pages in the document | Positive integer, >= `PAGE_NUM` |

## Optional fields

| Field | Default | Notes |
|---|---|---|
| `RuntimeOverrides.ASSET_POLICY` | `prose-document-assets-v1` | Policy label echoed into JSON |

## TaskProfile

`NONE` - this skill runs in generic TASK shell mode without a profile.

## Read boundary

The skill reads only:

- `{IMAGE_PATH}`
- `{PAGE_MD_PATH}`

It must not read neighbouring page images, manifests, sibling markdown, or public asset folders.

## Write boundary

The skill writes only:

- `{OUTPUT_PATH}`

## AllowedTools

Omit `AllowedTools`. This is a VLM-reasoning-only skill with no deterministic tool dependencies.

## Recommended brief-builder

The orchestrator should prefer:

```sh
python3 tools/pdf2md/build_page_assets_brief.py --work-dir WORK_DIR --doc-stem DOC_STEM --page PAGE_NUM --total-pages TOTAL_PAGES
```

The brief-builder emits the required INIT-TASK shape and reduces prompt drift.

## CustomInstructions

Usually unnecessary. If used, keep them run-specific and do not restate the whole skill contract. Good examples:

- "Treat cover-page publisher marks as `img`, not `fig`."
- "For tables, include the visible title/caption in `caption`; do not invent units."
- "If a table spans outside this page, extract only visible rows and add issue `possible_continuation`."
