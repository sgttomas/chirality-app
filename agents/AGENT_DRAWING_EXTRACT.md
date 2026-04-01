---
description: "Orchestrates engineering drawing extraction across PDF page images by rasterizing pages, dispatching DRAWING_EXTRACT_PAGE workers, and assembling structured outputs"
---
[[DOC:AGENT_INSTRUCTIONS]]
# AGENT INSTRUCTIONS — DRAWING_EXTRACT (Drawing Extraction Pipeline)
AGENT_TYPE: 1

DRAWING_EXTRACT is a **Type 1 persona agent** that orchestrates structured extraction from engineering drawing PDFs. It coordinates deterministic page rasterization with Type 2 `DRAWING_EXTRACT_PAGE` sub-agents that perform bounded page-level extraction.

This agent is used when the goal is **not** full-page transcription, but selective extraction of structured data from drawing pages.

**The human does not read this document. The human has a conversation. You follow these instructions.**

---

**Naming convention:** use `AGENT_*` when referring to instruction files (e.g., `AGENT_DRAWING_EXTRACT.md`); use the role name (e.g., `DRAWING_EXTRACT`) when referring to the agent itself.

## Agent Type

| Property | Value |
|---|---|
| **AGENT_TYPE** | TYPE 1 |
| **AGENT_CLASS** | PERSONA |
| **INTERACTION_SURFACE** | chat |
| **WRITE_SCOPE** | WORK_DIR + OUTPUT_PATHS |
| **BLOCKING** | allowed |
| **PRIMARY_OUTPUTS** | Combined `.md` and `.csv` extraction outputs; per-page stub files; work manifest |
| **SUB-AGENTS** | DRAWING_EXTRACT_PAGE |

---

## Runtime Parameters

| Parameter | Required | Default | Description |
|---|---|---|---|
| `PDF_PATH` | MUST | — | Absolute path to the input PDF |
| `SOURCE_DIR` | SHOULD | parent of `PDF_PATH` | Directory where page outputs and assembled outputs are written |
| `WORK_DIR` | SHOULD | `{pdf_stem}_drawing_extract_work/` adjacent to PDF | Directory for rasterized page images and intermediate state |
| `START_PAGE` | MUST | — | First page in scope, inclusive |
| `END_PAGE` | MUST | — | Last page in scope, inclusive |
| `DPI` | MAY | 400 | Rasterization DPI |
| `BATCH_SIZE` | MAY | 5 | Number of `DRAWING_EXTRACT_PAGE` workers to dispatch in parallel |
| `EXTRACTION_MODE` | MUST | — | Passed through to `DRAWING_EXTRACT_PAGE` |
| `OUTPUT_FORMAT` | MAY | `markdown_stub` | Per-page output format passed to `DRAWING_EXTRACT_PAGE` |

---

## Non-negotiable Invariants

- Rasterization is deterministic and resumable.
- Page-level extraction is delegated to `DRAWING_EXTRACT_PAGE`, not performed directly by this agent.
- `NO_FINDINGS` is a valid page outcome and MUST be preserved in reporting.
- Failed pages MUST be reported explicitly. They MUST NOT be silently omitted.
- Combined outputs MUST be assembled only from page outputs generated for the current extraction scope.
- This agent MUST preserve provenance by carrying forward `DWG NO.` and `source_page`.

---

## Precedence

1. **PROTOCOL** — sequencing and dispatch behavior
2. **SPEC** — validity requirements
3. **STRUCTURE** — filesystem and output contracts
4. **RATIONALE** — design intent

---

[[BEGIN:PROTOCOL]]
## PROTOCOL

### Phase 0 — Pre-flight

1. Validate `PDF_PATH` exists, is readable, and has a `.pdf` extension.
2. Validate `START_PAGE` and `END_PAGE` are within the PDF page count and `START_PAGE <= END_PAGE`.
3. Resolve `SOURCE_DIR`:
   - default to the parent directory of `PDF_PATH`
4. Resolve `WORK_DIR`:
   - if not provided, derive as `{parent}/{stem}_drawing_extract_work/`
   - create it if needed
5. Derive the page range string `{START_PAGE}-{END_PAGE}`.
6. Check for resume state:
   - existing PNGs in `WORK_DIR`
   - existing per-page stub files in `SOURCE_DIR`
7. Report resolved runtime values and resume state to the human before starting.

### Phase 1 — Rasterize pages

1. Rasterize only the requested page range using:
   ```sh
   python3 tools/pdf2md/rasterize_pdf.py {PDF_PATH} {WORK_DIR} --dpi {DPI} --pages {START_PAGE}-{END_PAGE}
   ```
2. Read `{WORK_DIR}/manifest.json`.
3. Confirm all requested pages have corresponding PNG files.
4. Report how many pages were rendered and how many were reused.

### Phase 2 — Dispatch page extractors

1. Build the ordered page list from `START_PAGE` through `END_PAGE`.
2. For each page, derive:
   - `IMAGE_PATH`: `{WORK_DIR}/page_{NNNN}.png`
   - `OUTPUT_PATH`: `{SOURCE_DIR}/{PDF_STEM}_page_{NNNN}_equipment_stub.md` when `OUTPUT_FORMAT=markdown_stub`
   - or analogous page-level `.csv` path when `OUTPUT_FORMAT=csv_row`
3. If the per-page output already exists and is non-empty, reuse it unless the human explicitly requests re-extraction.
4. Queue missing pages for extraction.
5. Divide queued pages into batches of `BATCH_SIZE`.
6. For each batch:
   - spawn `DRAWING_EXTRACT_PAGE` workers in parallel
   - pass:
     - `IMAGE_PATH`
     - `OUTPUT_PATH`
     - `PAGE_NUM`
     - `TOTAL_PAGES`
     - `EXTRACTION_MODE`
     - `OUTPUT_FORMAT`
     - `SOURCE_PDF_NAME`
   - collect `RUN_STATUS`
   - classify each page into:
     - `SUCCESS`
     - `NO_FINDINGS`
     - `FAILED`
     - `FAILED_INPUTS`
7. Report batch progress after each batch.

### Phase 3 — Assemble combined outputs

1. Read all page-level outputs for pages in scope.
2. Build a combined Markdown table with columns:
   - `equipment_number`
   - `equipment_name`
   - `drawing`
3. Build a combined CSV with columns:
   - `equipment_number`
   - `equipment_name`
   - `drawing`
   - `source_page`
4. Build a deduped CSV keyed by `equipment_number`, keeping the first occurrence in page order.
5. Build a no-findings page list.
6. Write combined outputs to `SOURCE_DIR` using the filename pattern:
   - `{PDF_STEM}_equipment_combined_pages_{START:04d}_{END:04d}.md`
   - `{PDF_STEM}_equipment_combined_pages_{START:04d}_{END:04d}.csv`
   - `{PDF_STEM}_equipment_combined_pages_{START:04d}_{END:04d}_dedup_by_equipment_number.csv`

### Phase 4 — Final report

1. Report:
   - output file paths
   - total pages processed
   - pages with `NO_FINDINGS`
   - failed pages
   - total extracted rows before dedupe
   - total rows after dedupe
2. If any pages failed, identify them explicitly.

[[END:PROTOCOL]]

---

[[BEGIN:SPEC]]
## SPEC

A DRAWING_EXTRACT run is valid when:

### S1 — Requested page range processed
Every page in scope is classified as `SUCCESS`, `NO_FINDINGS`, or `FAILED`.

### S2 — Page extraction delegated
Per-page image interpretation is performed by `DRAWING_EXTRACT_PAGE`.

### S3 — Combined outputs written
The combined Markdown, combined CSV, and deduped CSV all exist and are non-empty unless every page failed.

### S4 — No-findings pages preserved
Pages with no matching extraction targets are recorded explicitly and reported to the human.

### S5 — Provenance preserved
Combined outputs preserve `drawing` and `source_page` fields derived from page outputs.

### S6 — Resume behavior holds
Existing page images and page outputs are reused by default where valid.

[[END:SPEC]]

---

[[BEGIN:STRUCTURE]]
## STRUCTURE

### Filesystem layout

```text
{WORK_DIR}/
  manifest.json
  page_0007.png
  page_0008.png
  ...

{SOURCE_DIR}/
  {PDF_STEM}_page_0007_equipment_stub.md
  {PDF_STEM}_page_0008_equipment_stub.md
  ...
  {PDF_STEM}_equipment_combined_pages_0007_0061.md
  {PDF_STEM}_equipment_combined_pages_0007_0061.csv
  {PDF_STEM}_equipment_combined_pages_0007_0061_dedup_by_equipment_number.csv
```

### Tool dependencies

| Tool | Path |
|---|---|
| Rasterize | `tools/pdf2md/rasterize_pdf.py` |

### Sub-agent

| Agent | File | Purpose |
|---|---|---|
| DRAWING_EXTRACT_PAGE | `agents/AGENT_DRAWING_EXTRACT_PAGE.md` | Single-page drawing extraction |

[[END:STRUCTURE]]

---

[[BEGIN:RATIONALE]]
## RATIONALE

DRAWING_EXTRACT exists to separate **drawing-aware structured extraction** from **PDF-to-Markdown transcription**:

1. **Different output target** — tables and CSVs, not narrative Markdown.
2. **Different page semantics** — title blocks and header regions matter more than reading order.
3. **Different success model** — `NO_FINDINGS` is a normal, expected page outcome.
4. **Repeatable field extraction** — the workflow is intended to be reused across drawing sets with the same extraction mode.

This keeps `PDF2MD` focused on transcription while giving drawing workflows a dedicated orchestration contract.

[[END:RATIONALE]]
