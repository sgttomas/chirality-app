---
name: pdf2md-page
description: Convert a single PDF page PNG to raw Markdown via multimodal vision. Use when PDF2MD orchestrator spawns per-page fanout; one image in, one markdown file out, no post-processing.
compatibility: Chirality TASK; invoked by PDF2MD orchestrator for per-page fanout (sibling to skills/pdf2md/ which excludes page-level fanout)
metadata:
  chirality-skill-version: "1"
  chirality-task-profile: NONE
---

# SKILL — pdf2md-page

## Purpose

Convert **one PDF page image** to clean, well-structured Markdown using the agent's multimodal Read tool (VLM vision). Spawned by the PDF2MD orchestrator as per-page fanout. Reads one PNG, writes one `.md` file, returns a status.

This skill is intentionally minimal: its entire value is the multimodal perception step — reading a page image and transcribing its contents to Markdown. All cleanup, coordination, and assembly are the PDF2MD orchestrator's responsibility.

## Suitable agent shells

- `TASK` in generic shell mode, spawned by the PDF2MD orchestrator

Not the right fit for:
- whole-PDF conversion (use `skills/pdf2md/` or the full PDF2MD persona instead)
- post-processing, cleanup, or assembly (PDF2MD handles those in its own phases)
- any task that needs cross-page context

## Relationship to `skills/pdf2md/`

This skill is the **per-page fanout companion** to `skills/pdf2md/`.

- `skills/pdf2md/` handles whole-PDF orchestration (rasterization, post-processing, assembly) in a single bounded run and explicitly excludes page-level fanout.
- `skills/pdf2md-page/` (this skill) handles exactly one page per invocation, spawned in parallel by the PDF2MD orchestrator.

The two skills compose: the PDF2MD persona rasterizes the PDF, spawns one `TASK` + `pdf2md-page` invocation per page image, collects the per-page Markdown outputs, then runs its own post-processing and assembly phases.

## Inputs

### Required

- `RuntimeOverrides.IMAGE_PATH` — absolute path to the page PNG file
- `RuntimeOverrides.OUTPUT_PATH` — absolute path where the page Markdown will be written
- `RuntimeOverrides.PAGE_NUM` — 1-indexed page number
- `RuntimeOverrides.TOTAL_PAGES` — total pages in the document

### Optional

- None. This skill has no optional runtime overrides.

## Runtime overrides

| Key | Meaning | Default | Allowed values |
|---|---|---|---|
| `IMAGE_PATH` | Absolute path to the page PNG file | **Required** | Must exist and have `.png` extension |
| `OUTPUT_PATH` | Absolute path to write the page Markdown | **Required** | Parent directory must exist |
| `PAGE_NUM` | 1-indexed page number | **Required** | Positive integer |
| `TOTAL_PAGES` | Total pages in the document | **Required** | Positive integer, >= `PAGE_NUM` |

## Read boundary

Reads are limited to exactly one file:

- `{RuntimeOverrides.IMAGE_PATH}` — the single page PNG

The skill must NOT read any other file. Zero cross-page context.

## Write boundary

Writes are limited to exactly one file:

- `{RuntimeOverrides.OUTPUT_PATH}` — the page Markdown (or a failure placeholder)

The output filename is deterministic: it is precisely `OUTPUT_PATH` as provided in the brief.

## Tool usage

- No deterministic tools. This is a VLM-reasoning-only skill.
- The `allowed-tools` frontmatter field is intentionally omitted.
- The agent uses its native `Read` tool for multimodal PNG input and its native `Write` tool for the single output file.

Disallowed behavior:

- MUST NOT run `postprocess_page.py` or any other cleanup tool. Post-processing is PDF2MD's responsibility.
- MUST NOT read any file other than `IMAGE_PATH`.
- MUST NOT write any file other than `OUTPUT_PATH`.
- MUST NOT widen scope beyond the designated page.

## Method

### Step 1 — Validate inputs

1. Confirm `IMAGE_PATH` exists and is a `.png` file.
2. Confirm `OUTPUT_PATH` parent directory exists.
3. If `IMAGE_PATH` does not exist: write `*[Page {PAGE_NUM}: image not found]*` to `OUTPUT_PATH` and return `RUN_STATUS=FAILED_INPUTS`.

### Step 2 — Read and convert the page image

1. Use the `Read` tool to load `IMAGE_PATH`. The `Read` tool handles PNG images as multimodal (vision) input.
2. Examine the page image and convert its contents to Markdown following these rules precisely:

**RULE 1 — TEXT PRESERVATION**
- Preserve ALL text content completely and accurately.
- Maintain the reading order as a human would read the page.
- Correct obvious OCR-like errors only if you are completely certain.

**RULE 2 — STRUCTURE**
- Use `#` for the main page title (at most one per page).
- Use `##` for major sections, `###` for subsections, `####` for minor headings.
- Use `-` for unordered lists and `1. 2. 3.` for ordered lists.
- Preserve list nesting with indentation.
- Use `**bold**` and `*italic*` to match the visual emphasis.

**RULE 3 — TABLES**
- Convert tables to GFM pipe format.
- Add alignment markers (`:---`, `:---:`, `---:`) matching visual alignment.
- If a table is too complex for pipe format, use HTML `<table>` markup.

**RULE 4 — CODE**
- Wrap code blocks in triple backticks with language identifier.
- Wrap inline code in single backticks.

**RULE 5 — FORMULAS**
- Render mathematical expressions using LaTeX: `$inline$` and `$$display$$`.

**RULE 6 — WHAT TO IGNORE**
- Page numbers (bottom/top of page).
- Repeated headers/footers that appear on every page.
- Decorative borders and lines that carry no content meaning.

**RULE 7 — OUTPUT FORMAT**
- Output ONLY the Markdown content.
- Do NOT wrap in ` ```markdown ``` ` fences.
- Do NOT add commentary or explanations.
- Do NOT add "Page X of Y" markers.
- Start directly with the page content.

### Step 3 — Write output and return status

1. Write the Markdown to `OUTPUT_PATH` using the `Write` tool.
2. If conversion succeeded: return `RUN_STATUS=SUCCESS` with the page number and a brief note (e.g., "Page 3/42: 1,247 chars").
3. If the image could not be interpreted (blank page, unreadable scan): write `*[Page {PAGE_NUM}: content not extractable]*` to `OUTPUT_PATH` and return `RUN_STATUS=FAILED`.

## Outputs

- `{OUTPUT_PATH}` — Markdown text for one page (or a failure placeholder)

## Return value

The skill returns to the caller:

- `RUN_STATUS`: `SUCCESS` | `FAILED` | `FAILED_INPUTS`
- `PAGE_NUM`: the page number processed
- `CHARS`: approximate character count of the output

## Non-negotiable constraints

- **Single-page scope.** One page in, one markdown snippet out. No cross-page context.
- **OUTPUT_PATH-only writes.** Write scope is strictly the designated `OUTPUT_PATH` for this page.
- **Single-file reads.** Read scope is strictly `IMAGE_PATH`. No other files may be read.
- **Raw VLM output only.** No post-processing, no cleanup rules applied. PDF2MD handles that.
- **No invention.** The agent does not add content that is not visible in the image. No hallucinated text, URLs, or structural elements.
- **Content fidelity.** All visible text, tables, and structural elements from the page image must be represented. Missing content is a defect.
- **Deterministic output filename.** The output is written to exactly `OUTPUT_PATH` as provided in the brief; the skill does not derive or modify the filename.
- **Failure placeholders.** On read failure or extraction failure, write a placeholder line to `OUTPUT_PATH` and return the appropriate failure status. Never leave `OUTPUT_PATH` unwritten.

## QA expectations

- `OUTPUT_PATH` exists after the run and is non-empty.
- No files other than `OUTPUT_PATH` were written.
- No files other than `IMAGE_PATH` were read.
- Output is raw VLM Markdown (no post-processing applied, no fences, no commentary).
- All visible page content is represented in the Markdown.
- No invented content beyond what is visible in the image.
- Failure cases produce a placeholder line at `OUTPUT_PATH` and an explicit `FAILED` or `FAILED_INPUTS` status.
