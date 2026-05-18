---
name: pdf2md
description: Convert a bounded PDF source into Markdown by combining deterministic PDF tooling (rasterize, post-process, assemble) with the agent's multimodal vision for per-page transcription. Use for single-run TASK-shell conversions where the full PDF2MD persona orchestration is unnecessary.
compatibility: Chirality TASK generic shell; local repo tools only.
allowed-tools: python3 tools/pdf2md/rasterize_pdf.py:*, python3 tools/pdf2md/postprocess_page.py:*, python3 tools/pdf2md/assemble_markdown.py:*, python3 tools/reporting/clean_pdf2md_output.py:*
metadata:
  chirality-skill-version: "1"
  chirality-task-profile: NONE
---

# SKILL — pdf2md

## Purpose

Convert one bounded PDF into a single assembled Markdown file under TASK in a single run, using a **hybrid pipeline**:

- **Deterministic tools** (Python, no LLM API calls) handle the mechanical work: rasterization, the 10-rule post-processor, header/footer stripping, and final assembly.
- **The agent's multimodal vision** (the native `Read` tool against per-page PNGs) handles per-page transcription — the perception task that no deterministic OCR/text-layer reader can do robustly across scanned engineering documents.

This split is the same skill/tool boundary the `PDF2MD` persona enforces (`agents/AGENT_PDF2MD.md`). The persona fans transcription out to many `TASK + pdf2md-page` dispatches in parallel and runs the deterministic tools as pipeline stages; this skill collapses both halves into one bounded TASK invocation. The hybrid is principled, not a relaxation: deterministic tools stay deterministic (no LLM inside them); the VLM reasoning lives inside the TASK shell that loads this skill.

## When VLM transcription is required vs. optional

VLM (the agent's vision) is **required** for any page where deterministic text extraction would lose fidelity. In practice:

| Page contains | VLM required? | Why |
|---|---|---|
| Scanned-image pages with no embedded text layer | **Yes** | No text to extract; only the raster |
| Figures, photographs, diagrams, schematics | **Yes** | Caption + asset placeholder need to be emitted in reading order; deterministic readers miss the asset |
| Tables (any non-trivial layout) | **Yes** | Column alignment and merged cells survive vision better than naive PDF text extraction |
| Equations (display or inline) | **Yes** | LaTeX reconstruction from a glyph stream is unreliable; vision sees the typeset form |
| Pure prose pages with a clean embedded text layer | Optional | VLM yields higher quality but is slower and more expensive; tool-only is acceptable when the embedded text matches the typeset content |

Default to VLM. Tool-only extraction is a possible optimization for clean-prose corpora but should be opted into per page or per source, not assumed.

## Suitable agent shells

- `TASK` in generic shell mode

Not the best fit for:
- per-page fan-out across many pages (use the `PDF2MD` persona — it batches via `TaskSkill: pdf2md-page`)
- documents with rich asset mode (figures/tables to crop and materialize; use `ASSET_MODE=prose` under the persona's Phase 3.5)
- equation audit / fix loop (use `EQUATION_AUDIT` after assembly)

## Inputs

### Required

- `RuntimeOverrides.PDF_PATH` — absolute path to the input PDF
- `RuntimeOverrides.OUTPUT_PATH` — absolute path for the final assembled Markdown

### Optional

- `RuntimeOverrides.WORK_DIR` — defaults to `{pdf_stem}_pdf2md_work/` adjacent to the PDF
- `RuntimeOverrides.DPI` — rasterization DPI (default `300`)
- `RuntimeOverrides.PAGES` — page selection (default `all`)
- `RuntimeOverrides.SEPARATOR` — page separator in the assembled output (default `---`)
- `CustomInstructions` — caller-supplied notes for page-specific handling

## Runtime overrides

| Key | Meaning | Default |
|---|---|---|
| `PDF_PATH` | Absolute path to input PDF | **Required** |
| `OUTPUT_PATH` | Absolute path to final Markdown output | **Required** |
| `WORK_DIR` | Directory for PNGs and intermediate page markdown | `{pdf_stem}_pdf2md_work` adjacent to PDF |
| `DPI` | Rasterization DPI | `300` |
| `PAGES` | Page selection (`all`, `5`, `3-15`, `1,3,5`) | `all` |
| `SEPARATOR` | Assembly separator | `---` |

## Method (the hybrid pipeline)

### Step 1 — Rasterize (deterministic tool)

```sh
python3 tools/pdf2md/rasterize_pdf.py {PDF_PATH} {WORK_DIR} --dpi {DPI} [--pages {PAGES}]
```

Reads `manifest.json` after the run; it records `pdf_sha256` + `dpi` (for resume-safety) and the canonical page list.

### Step 2 — Per-page transcription (VLM via the agent's Read tool)

For each `page_{NNNN}.png` listed in the manifest where `page_{NNNN}.md` does not already exist:

1. Use the `Read` tool to load the page PNG (multimodal).
2. Transcribe its contents to Markdown following the same 8 conversion rules used by the `pdf2md-page` skill (see `skills/pdf2md-page/SKILL.md` § Step 2). Quoted summary:
   - **RULE 1 — Text:** preserve all visible text in reading order.
   - **RULE 2 — Structure:** Markdown headings, lists, emphasis.
   - **RULE 3 — Tables:** GFM pipe format (or HTML when too complex), with a `[TABLE: <caption>]` placeholder above the transcription.
   - **RULE 4 — Code:** fenced blocks with language identifier.
   - **RULE 5 — Formulas:** LaTeX inside `$inline$` and `$$display$$`.
   - **RULE 6 — Ignore:** page numbers, running headers/footers, decorative borders.
   - **RULE 7 — Output format:** raw Markdown only — no surrounding fences, no commentary.
   - **RULE 8 — Asset placeholders:** every visible figure, table, and oddball image gets a `[FIGURE: ...]` / `[TABLE: ...]` / `[<descriptor> logo]` placeholder in document reading order.
3. Write the result to `{WORK_DIR}/page_{NNNN}.md`.

If `CustomInstructions` adjusts any rule for this brief (e.g., "rewrite diagrams as numbered procedural steps"), honor it.

### Step 3 — Post-process (deterministic tool)

For each per-page Markdown:

```sh
python3 tools/pdf2md/postprocess_page.py {WORK_DIR}/page_{NNNN}.md
python3 tools/reporting/clean_pdf2md_output.py {WORK_DIR}/page_{NNNN}.md
```

The first applies 10-rule cleanup to VLM output (fence stripping, table-syntax repair, hallucinated-image removal, etc.). The second strips repeated page headers/footers.

### Step 4 — Assemble (deterministic tool)

```sh
python3 tools/pdf2md/assemble_markdown.py {WORK_DIR} {OUTPUT_PATH} --separator "{SEPARATOR}"
python3 tools/reporting/clean_pdf2md_output.py {OUTPUT_PATH}
```

The second clean pass catches cross-page header/footer patterns visible only after assembly.

### Step 5 — Report

Return a structured run report:

- pages converted (counts: success / fail / reused)
- output bytes
- failed page numbers, if any
- assembled output path

## Tool usage

The frontmatter `allowed-tools` constrains TASK whitelisting:

- `tools/pdf2md/rasterize_pdf.py` — Step 1
- `tools/pdf2md/postprocess_page.py` — Step 3
- `tools/pdf2md/assemble_markdown.py` — Step 4
- `tools/reporting/clean_pdf2md_output.py` — Step 3 + Step 4

The agent's native `Read` and `Write` tools are also used (for Step 2's multimodal page loads and per-page MD writes).

### Disallowed behavior

- Spawning sub-agents for per-page fan-out — that pattern is reserved for the `PDF2MD` persona via `TaskSkill: pdf2md-page`.
- Writing outside `{WORK_DIR}` and `{OUTPUT_PATH}`.
- Embedding LLM reasoning inside any of the deterministic tool invocations — the tools must stay deterministic. The hybrid pattern is: tools deterministic, VLM transcription inside the TASK shell.
- Asset mode (figure/table cropping + manifest generation) — that's the persona's Phase 3.5 work, not this skill's.
- Equation audit / fix loop — that's `EQUATION_AUDIT`'s job after assembly.

## Outputs

- Final assembled Markdown at `OUTPUT_PATH`
- `manifest.json` in `WORK_DIR` (rasterizer output)
- Per-page `.md` files in `WORK_DIR`
- A structured run report from `TASK`

## Non-negotiable constraints

- **Hybrid stays separated.** Deterministic tools never embed LLM reasoning; VLM transcription never invokes shell subprocesses. The boundary is the same as `pdf2md-page`'s.
- **Reading-order discipline (Step 2).** Per-page transcription emits content in document reading order; asset placeholders appear at the position of the asset on the page.
- **No silent page drops.** Failed pages get a placeholder line (`*[Page N: conversion unavailable]*`) and are reported in the run report. They are not omitted from the assembled output.
- **Resume-safe.** Re-running with matching `(pdf_sha256, dpi)` reuses existing PNGs and per-page MDs. The rasterizer + manifest model handles this.
- **Custom instructions are honored.** If the brief contains `CustomInstructions` for page-specific handling, the per-page transcription reflects them.

## QA expectations

- `OUTPUT_PATH` exists and is non-empty.
- `{WORK_DIR}/manifest.json` exists and records `pdf_sha256`, `dpi`, `pages_rendered`.
- For every page in `manifest.json:pages_rendered`, either a per-page `.md` exists OR a placeholder for that page appears in `OUTPUT_PATH`.
- Failed pages, if any, are surfaced in the run report — never silently dropped.
- The per-page Markdowns pass the 8 conversion rules' QA (no surrounding code fences; tables have GFM-compatible separators with placeholders; equations use `$..$` / `$$..$$`).
- Custom instructions affecting page interpretation are reflected in the output.
