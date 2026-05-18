# pdf2md-page-full - Brief Schema

Use this skill with `TASK` for one PDF page image when the worker must produce
both the Markdown transcription and the page asset JSON from a single vision
read.

```md
PURPOSE: Transcribe one PDF page and identify page assets
RequestedBy: PDF2MD

ScopePath: /abs/path/to/pdf_work_dir
TaskSkill: pdf2md-page-full

Tasks:
  - Read one page raster exactly once
  - Write the page Markdown transcription
  - Write the bbox-normalized page asset JSON

ApplyEdits: true

AllowedWriteTargets:
  - "/abs/path/to/pdf_work_dir/page_0003.md"
  - "/abs/path/to/pdf_work_dir/page_0003_assets.json"

RuntimeOverrides:
  IMAGE_PATH: /abs/path/to/pdf_work_dir/page_0003.png
  OUTPUT_MD_PATH: /abs/path/to/pdf_work_dir/page_0003.md
  OUTPUT_JSON_PATH: /abs/path/to/pdf_work_dir/page_0003_assets.json
  DOC_STEM: MWK_1956
  PAGE_NUM: 3
  TOTAL_PAGES: 386
  ASSET_POLICY: prose-document-assets-v1

ExpectedOutputs:
  - /abs/path/to/pdf_work_dir/page_0003.md
  - /abs/path/to/pdf_work_dir/page_0003_assets.json
```

## Required fields

| Field | Value | Notes |
|---|---|---|
| `TaskSkill` | `pdf2md-page-full` | Must match skill folder name |
| `RuntimeOverrides.IMAGE_PATH` | Absolute path to page PNG | Must exist and end `.png` |
| `RuntimeOverrides.OUTPUT_MD_PATH` | Absolute path to page Markdown output | Parent directory must exist |
| `RuntimeOverrides.OUTPUT_JSON_PATH` | Absolute path to page asset JSON output | Parent directory must exist |
| `RuntimeOverrides.DOC_STEM` | Document stem | Used for downstream deterministic naming context |
| `RuntimeOverrides.PAGE_NUM` | 1-indexed page number | Positive integer |
| `RuntimeOverrides.TOTAL_PAGES` | Total page count | Positive integer, >= `PAGE_NUM` |

## Optional fields

| Field | Default | Notes |
|---|---|---|
| `RuntimeOverrides.ASSET_POLICY` | `prose-document-assets-v1` | Policy label echoed into JSON |

## TaskProfile

`NONE` - this skill runs in generic TASK shell mode without a profile.

## Read boundary

The skill reads only:

- `{IMAGE_PATH}`

It must not read neighbouring page images, page Markdown, manifests, sibling
outputs, or public asset folders.

## Write boundary

The skill writes only:

- `{OUTPUT_MD_PATH}`
- `{OUTPUT_JSON_PATH}`

## AllowedTools

Omit `AllowedTools`. This is a VLM-reasoning-only skill with no deterministic
tool dependency inside the TASK worker.
