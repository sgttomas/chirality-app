---
name: pdf2md
description: Convert a bounded PDF source into Markdown using deterministic PDF tooling plus direct agent interpretation where needed. Use for single-run PDF-to-Markdown tasks under TASK when full PDF2MD orchestration is unnecessary.
compatibility: Chirality TASK generic shell; local repo tools only.
allowed-tools: python3 tools/pdf2md/rasterize_pdf.py:*, python3 tools/pdf2md/postprocess_page.py:*, python3 tools/pdf2md/assemble_markdown.py:*, python3 tools/reporting/clean_pdf2md_output.py:*
metadata:
  chirality-skill-version: "1"
  chirality-task-profile: NONE
---

# SKILL — pdf2md

## Purpose

Convert a bounded PDF source into Markdown using deterministic PDF tooling plus direct agent interpretation where needed.

This skill is for **single-run bounded conversion**, not multi-agent orchestration.

## Suitable agent shells

- `TASK` in generic shell mode

Not the best fit for:
- page-fanout orchestration
- multi-batch sub-agent conversion
- long-running manager-style workflows

For those, use the dedicated `PDF2MD` persona pipeline instead.

## Inputs

### Required

- `RuntimeOverrides.PDF_PATH`
- `RuntimeOverrides.OUTPUT_PATH`

### Optional

- `RuntimeOverrides.WORK_DIR`
- `RuntimeOverrides.DPI`
- `RuntimeOverrides.PAGES`
- `RuntimeOverrides.SEPARATOR`
- `CustomInstructions`

## Runtime overrides

| Key | Meaning | Default |
|---|---|---|
| `PDF_PATH` | Absolute path to input PDF | required |
| `OUTPUT_PATH` | Absolute path to final Markdown output | required |
| `WORK_DIR` | Directory for PNGs and intermediate page markdown | `{pdf_stem}_pdf2md_work` adjacent to PDF |
| `DPI` | Rasterization DPI | `300` |
| `PAGES` | Page selection (`all`, `5`, `3-15`, `1,3,5`) | `all` |
| `SEPARATOR` | Assembly separator | `---` |

## Tool usage

Preferred deterministic tools:
- `tools/pdf2md/rasterize_pdf.py`
- `tools/pdf2md/postprocess_page.py`
- `tools/pdf2md/assemble_markdown.py`
- `tools/reporting/clean_pdf2md_output.py`

The skill may also use direct agent reading/reasoning for:
- page-level Markdown drafting
- diagram-to-logic rewriting
- table reshaping when visual layout should not be preserved literally

Disallowed behavior under generic `TASK`:
- spawning sub-agents for per-page fanout
- widening writes outside the PDF-local working scope

## Outputs

- Final assembled Markdown at `OUTPUT_PATH`
- `manifest.json` in `WORK_DIR`
- Per-page `.md` files in `WORK_DIR`
- A structured run report from `TASK`

## Non-negotiable constraints

- Do not silently drop failed pages.
- Preserve custom instructions for special page handling when the brief provides them.
- Prefer semantic reconstruction over visual mimicry for diagrams when instructed.
- Surface partial success explicitly.

## QA expectations

- Output file exists and is non-empty.
- `manifest.json` exists.
- Failed pages, if any, are reported.
- Custom instructions affecting page interpretation are reflected in the output.
