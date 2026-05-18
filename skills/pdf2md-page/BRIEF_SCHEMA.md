# pdf2md-page — Brief Schema

Use this skill with `TASK` like this (typically spawned by the PDF2MD orchestrator, one invocation per page):

```md
PURPOSE: Convert one PDF page image to raw Markdown
RequestedBy: PDF2MD

ScopePath: /abs/path/to/pdf_work_dir
TaskSkill: pdf2md-page

Tasks:
  - Read the page image and transcribe its contents to Markdown per the 8 conversion rules

ApplyEdits: true

AllowedWriteTargets:
  - "/abs/path/to/pdf_work_dir/pages/page_003.md"

RuntimeOverrides:
  IMAGE_PATH: /abs/path/to/pdf_work_dir/pages/page_003.png
  OUTPUT_PATH: /abs/path/to/pdf_work_dir/pages/page_003.md
  PAGE_NUM: 3
  TOTAL_PAGES: 42

ExpectedOutputs:
  - /abs/path/to/pdf_work_dir/pages/page_003.md
```

## Required fields

| Field | Value | Notes |
|---|---|---|
| `TaskSkill` | `pdf2md-page` | Must match skill folder name |
| `RuntimeOverrides.IMAGE_PATH` | Absolute path to the page PNG | Must exist, must have `.png` extension |
| `RuntimeOverrides.OUTPUT_PATH` | Absolute path to the page `.md` | Parent directory must exist |
| `RuntimeOverrides.PAGE_NUM` | 1-indexed page number | Positive integer |
| `RuntimeOverrides.TOTAL_PAGES` | Total pages in the document | Positive integer, >= `PAGE_NUM` |

## Optional fields

None. This skill has no optional brief fields and no optional runtime overrides.

## TaskProfile

`NONE` — this skill runs in generic TASK shell mode without a profile.

## Read boundary

The skill reads only:

- `{IMAGE_PATH}`

It must NOT read any other file, including neighbouring page images, manifests, or sibling markdown.

## Write boundary

The skill writes only:

- `{OUTPUT_PATH}`

The output filename is deterministic — it is precisely the `OUTPUT_PATH` supplied in the brief. The skill does not derive or modify the filename.

## AllowedTools

Omit `AllowedTools`. This is a VLM-reasoning-only skill with no deterministic tool dependencies; the skill uses only the agent's native `Read` (multimodal) and `Write` tools.

## Notes

- `ScopePath` should normally be the PDF working directory so that `IMAGE_PATH` and `OUTPUT_PATH` both resolve within scope.
- `ApplyEdits: true` is appropriate because this skill is expected to write the per-page Markdown artifact.
- One invocation processes one page. The PDF2MD orchestrator spawns one task per page for parallel fanout.
- The orchestrator is responsible for post-processing (`postprocess_page.py`), assembly (`assemble_markdown.py`), and final cleanup. This skill emits raw VLM Markdown only.
- On any failure, the skill still writes a placeholder line to `OUTPUT_PATH` so that the orchestrator's assembly step can account for the missing page.
