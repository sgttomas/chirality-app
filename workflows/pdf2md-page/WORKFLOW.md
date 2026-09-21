---
name: pdf2md-page
description: "LEGACY Markdown-only page transcription for explicitly selected historical PDF resume contracts; new conversion runs use pdf2md-page-full."
---

# pdf2md-page

Load [CONTRACT.md](CONTRACT.md) when preparing the brief or validating the result; it contains the input schema, output checks, and tool responsibilities. Resolve repository commands against the brief's declared tool root.

Status: LEGACY. Use for explicitly selected historical or resume contracts; the current orchestration selects the replacement workflow.

## Purpose

Convert **one PDF page image** to clean, well-structured Markdown using the agent's multimodal Read tool (VLM vision). Selected by WORKING_ITEMS only for a legacy page-conversion contract. Reads one PNG, writes one `.md` file, returns a status.

This workflow is intentionally minimal: its entire value is the multimodal perception step — reading a page image and transcribing its contents to Markdown. All cleanup, coordination, and assembly are the pdf2md-orchestration orchestrator's responsibility.

## Relationship to `workflows/pdf2md/`

This workflow preserves the old Markdown-only page contract. The bounded `pdf2md` workflow performs its own page transcription; the manager uses `pdf2md-orchestration` for fanout.

- `workflows/pdf2md/` handles whole-PDF orchestration (rasterization, post-processing, assembly) in a single bounded run and explicitly excludes page-level fanout.
- `workflows/pdf2md-page/` (this workflow) handles exactly one page per invocation, spawned in parallel by the pdf2md-orchestration orchestrator.

For a legacy resume contract, WORKING_ITEMS may dispatch this Markdown-only worker and the legacy asset worker separately. New orchestration uses `pdf2md-page-full` for the paired outputs.

## Inputs

### Required

- `RuntimeOverrides.IMAGE_PATH` — absolute path to the page PNG file
- `RuntimeOverrides.OUTPUT_PATH` — absolute path where the page Markdown will be written
- `RuntimeOverrides.PAGE_NUM` — 1-indexed page number
- `RuntimeOverrides.TOTAL_PAGES` — total pages in the document

### Optional

- None. This workflow has no optional runtime overrides.

## Runtime overrides

| Key | Meaning | Default | Allowed values |
|---|---|---|---|
| `IMAGE_PATH` | Absolute path to the page PNG file | **Required** | Must exist and have `.png` extension |
| `OUTPUT_PATH` | Absolute path to write the page Markdown | **Required** | Parent directory must exist |
| `PAGE_NUM` | 1-indexed page number | **Required** | Positive integer |
| `TOTAL_PAGES` | Total pages in the document | **Required** | Positive integer, >= `PAGE_NUM` |

## Read boundary

Task-data reads are limited to exactly one file:

- `{RuntimeOverrides.IMAGE_PATH}` — the single page PNG

The workflow must NOT read any other file. Zero cross-page context.

## Write boundary

Writes are limited to exactly one file:

- `{RuntimeOverrides.OUTPUT_PATH}` — the page Markdown (or a failure placeholder)

The output filename is deterministic: it is precisely `OUTPUT_PATH` as provided in the brief.

## Tool usage

- No deterministic tools. This is a VLM-reasoning-only workflow.
- The agent uses its native `Read` tool for multimodal PNG input and its native `Write` tool for the single output file.

Disallowed behavior:

- MUST NOT run `postprocess_page.py` or any other cleanup tool. Post-processing is pdf2md-orchestration's responsibility.
- Read task data only from `IMAGE_PATH`; role, workflow, and brief context are supplied separately.
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
- Also emit a `[TABLE: <visible caption>]` placeholder line immediately above the GFM/HTML transcription, per RULE 8. The inline GFM and the placeholder are both required.

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

**RULE 8 — ASSET PLACEHOLDERS**

Every visible figure, table, or non-text image on the page MUST be marked with a deterministic placeholder so downstream tooling (`tools/pdf2md/rewrite_inline_asset_refs.py`) can rewrite each placeholder to a working asset link. Placeholders are part of the Markdown content (RULE 7 still applies — no external commentary), and they appear in document reading order at the position of the asset on the page.

Required placeholder formats:

- **Figures (captioned plots, diagrams, charts, schematics, illustrations):**
  - Format: `[FIGURE: <full visible caption text including the figure number>]`
  - Example: `[FIGURE: Fig. 1.1 Yield stress-strain curve of copper in compression. After Cook and Larke [1].]`
  - One placeholder per visible figure. If a caption spans multiple lines on the page, join them into one line inside the brackets.
  - The leading `FIGURE:` token is REQUIRED — it is what the downstream rewriter keys on. Do not substitute `Figure:` (camelcase), `FIG:`, or omit it. Citations like `[1]` inside the caption are fine; the rewriter handles one level of nested brackets.

- **Tables (any tabular data, captioned or not):**
  - Format: `[TABLE: <full visible caption text, OR a brief summary if no caption>]`
  - Example: `[TABLE: Table 4.2 Comparison of stress values - Guided Cantilever vs General Analytical]`
  - The placeholder appears IMMEDIATELY ABOVE the GFM/HTML transcription required by RULE 3. Both surfaces are required: the placeholder for the asset rewriter, the GFM/HTML for human readability.
  - The leading `TABLE:` token is REQUIRED.

- **Non-figure non-table images (cover logos, decorative emblems, photographs, equation plates, etc.):**
  - Format: `[<short descriptor> logo]` / `[<descriptor> emblem]` / `[<descriptor> seal]` / `[<descriptor> cover]` / `[<descriptor> photograph]` / `[<descriptor> photo]` / `[<descriptor> image]`.
  - Example: `[Kellogg logo]`, `[Cover image]`, `[ASME emblem]`.
  - Use the trailing keyword that best describes the asset. The rewriter recognizes `logo`, `emblem`, `seal`, `cover`, `photograph`, `photo`, and `image`.

What MUST NOT happen:

- Do NOT describe a figure or table only in prose ("As shown in Fig. 1.4, the curve...") without also emitting the bracketed placeholder. The asset would land in a trailing "Unmatched Page Assets" block at downstream assembly, which produces noisier final Markdown.
- Do NOT use `![Fig. ...](...)` markdown-image syntax for figures — those are not the canonical placeholder shape. Use `[FIGURE: ...]`.
- Do NOT skip the placeholder for the cover-page logo or other oddball images on the assumption that they are "decorative" (RULE 6 ignores page numbers and repeating headers/footers, NOT one-off images).
- Do NOT invent placeholders for assets that are not visible on the page.

### Step 3 — Write output and return status

1. Write the Markdown to `OUTPUT_PATH` using the `Write` tool.
2. If conversion succeeded: return `RUN_STATUS=SUCCESS` with the page number and a brief note (e.g., "Page 3/42: 1,247 chars").
3. If the image could not be interpreted (blank page, unreadable scan): write `*[Page {PAGE_NUM}: content not extractable]*` to `OUTPUT_PATH` and return `RUN_STATUS=FAILED`.

## Outputs

- `{OUTPUT_PATH}` — Markdown text for one page (or a failure placeholder)

## Return value

The workflow returns to the caller:

- `RUN_STATUS`: `SUCCESS` | `FAILED` | `FAILED_INPUTS`
- `PAGE_NUM`: the page number processed
- `CHARS`: approximate character count of the output

## Non-negotiable constraints

- **Single-page scope.** One page in, one markdown snippet out. No cross-page context.
- **OUTPUT_PATH-only writes.** Write scope is strictly the designated `OUTPUT_PATH` for this page.
- **Single-file reads.** Read scope is strictly `IMAGE_PATH`. No other files may be read.
- **Raw VLM output only.** No post-processing, no cleanup rules applied. pdf2md-orchestration handles that.
- **No invention.** The agent does not add content that is not visible in the image. No hallucinated text, URLs, or structural elements.
- **Content fidelity.** All visible text, tables, and structural elements from the page image must be represented. Missing content is a defect.
- **Deterministic output filename.** The output is written to exactly `OUTPUT_PATH` as provided in the brief; the workflow does not derive or modify the filename.
- **Failure placeholders.** On read failure or extraction failure, write a placeholder line to `OUTPUT_PATH` and return the appropriate failure status. Never leave `OUTPUT_PATH` unwritten.

## QA expectations

- `OUTPUT_PATH` exists after the run and is non-empty.
- No files other than `OUTPUT_PATH` were written.
- No task data outside `IMAGE_PATH` were read.
- Output is raw VLM Markdown (no post-processing applied, no fences, no commentary).
- All visible page content is represented in the Markdown.
- No invented content beyond what is visible in the image.
- Failure cases produce a placeholder line at `OUTPUT_PATH` and an explicit `FAILED` or `FAILED_INPUTS` status.
