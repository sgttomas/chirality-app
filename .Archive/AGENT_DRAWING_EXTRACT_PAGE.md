---
description: "Extracts bounded structured data from a single engineering drawing page image using multimodal vision"
---
[[DOC:AGENT_INSTRUCTIONS]]
# AGENT INSTRUCTIONS — DRAWING_EXTRACT_PAGE (Single Page Drawing Data Extraction)
AGENT_TYPE: 2

These instructions govern a sub-agent that reads **one engineering drawing page image** and extracts **targeted structured information** from that page.

- Spawned by a drawing-aware persona or pipeline agent.
- **Read one image, write one structured output file.** No cross-page context.
- This agent is **not** a general page transcription agent. It performs **bounded extraction** against an explicit extraction mode.

**The human does not interact with this agent directly. The human has a conversation with the orchestrating persona. You follow these instructions.**

---

**Naming convention:** use `AGENT_*` when referring to instruction files (e.g., `AGENT_DRAWING_EXTRACT_PAGE.md`); use the role name (e.g., `DRAWING_EXTRACT_PAGE`) when referring to the agent itself.

## Agent Type

| Property | Value |
|---|---|
| **AGENT_TYPE** | TYPE 2 |
| **AGENT_CLASS** | TASK |
| **INTERACTION_SURFACE** | spawned |
| **WRITE_SCOPE** | OUTPUT_PATH only (single file) |
| **BLOCKING** | never |
| **PRIMARY_OUTPUTS** | `{OUTPUT_PATH}` — one page-level extraction artifact |

---

## Runtime Parameters

| Parameter | Required | Description |
|---|---|---|
| `IMAGE_PATH` | MUST | Absolute path to the drawing page PNG file |
| `HEADER_IMAGE_PATH` | SHOULD | Absolute path to the cropped top-header PNG for the same page |
| `TITLEBLOCK_IMAGE_PATH` | SHOULD | Absolute path to the cropped title-block PNG for the same page |
| `HEADER_SLICE_PATHS` | MAY | Ordered list of overlapping top-header slice PNGs for multiblock review |
| `OUTPUT_PATH` | MUST | Absolute path to write the extraction output |
| `PAGE_NUM` | MUST | 1-indexed page number |
| `TOTAL_PAGES` | MUST | Total pages in the source document |
| `EXTRACTION_MODE` | MUST | Extraction target definition; see supported modes below |
| `OUTPUT_FORMAT` | MUST | `markdown_stub` or `csv_row` |
| `SOURCE_PDF_NAME` | MAY | PDF filename for provenance in output |

### Supported extraction modes

| Mode | Meaning |
|---|---|
| `top_equipment_header_with_dwg` | Extract equipment numbers and names from the separated top-of-sheet equipment header, extract the page `DWG NO.`, and extract the title-block system name |

This agent MUST fail inputs for any extraction mode not explicitly supported by its instructions.

---

## Non-negotiable Invariants

- This agent MUST NOT behave like a full-page transcription agent. It performs only the extraction defined by `EXTRACTION_MODE`.
- This agent MUST NOT use any cross-page context.
- This agent MAY read only the current page image and current-page helper crops passed by the orchestrator: `IMAGE_PATH`, `HEADER_IMAGE_PATH`, `TITLEBLOCK_IMAGE_PATH`, and `HEADER_SLICE_PATHS`.
- This agent MUST extract `DWG NO.` whenever a supported extraction mode is run. `DWG NO.` is mandatory companion metadata.
- This agent MUST extract `system_name` from the title block whenever a supported extraction mode is run. `system_name` is mandatory companion metadata unless the run fails.
- This agent MUST distinguish between:
  - **findings present** and
  - **no relevant findings on the page**
- If no relevant extraction target is present, the agent MUST still write a valid output artifact and return `RUN_STATUS=NO_FINDINGS`.
- The agent MUST NOT infer equipment from repeated in-body references if the extraction mode is scoped to the separated top-of-sheet header region.
- Each invocation writes exactly one file: `OUTPUT_PATH`.
- This agent relies on the orchestrator for any deterministic PDF-level cross-checking such as `tools/drawing_extract/extract_pdf_titleblock_text.py`. It does not invoke PDF-level tools itself.

---

## Precedence

1. **PROTOCOL** — how to extract from the page
2. **SPEC** — what constitutes valid output
3. **STRUCTURE** — output schema requirements
4. **RATIONALE** — design intent

---

[[BEGIN:PROTOCOL]]
## PROTOCOL

### Step 1 — Validate inputs

1. Confirm `IMAGE_PATH` exists and is a `.png` file.
2. If provided, confirm `HEADER_IMAGE_PATH`, `TITLEBLOCK_IMAGE_PATH`, and each path in `HEADER_SLICE_PATHS` exist and are `.png` files.
3. Confirm `OUTPUT_PATH` parent directory exists.
3. Confirm `EXTRACTION_MODE` is supported.
4. Confirm `OUTPUT_FORMAT` is `markdown_stub` or `csv_row`.
5. If inputs are invalid, write a failure placeholder to `OUTPUT_PATH` and return `RUN_STATUS=FAILED_INPUTS`.

### Step 2 — Read and inspect the page image

1. Use the Read tool to load `IMAGE_PATH`.
2. If provided, also load `HEADER_IMAGE_PATH`, `TITLEBLOCK_IMAGE_PATH`, and `HEADER_SLICE_PATHS`.
3. Identify the following page regions as needed by the extraction mode:
   - the **top-of-sheet separated equipment header region**
   - the **title block / `DWG NO.` region**
   - the **title block title region** containing:
     - project line: `4-25 WEST DOE 300 MMSCFD DEEPCUT GAS PLANT`
     - system-name line
     - suffix line such as `PROCESS FLOW DIAGRAM`
4. Prefer helper crops over the full-page image for bounded reading:
   - use `TITLEBLOCK_IMAGE_PATH` first for `DWG NO.` and `system_name`
   - use `HEADER_IMAGE_PATH` and `HEADER_SLICE_PATHS` first for equipment findings
   - use the full-page image only to resolve current-page spatial context when a helper crop is insufficient
5. Ignore decorative borders, general process lines, and repeated in-body equipment tags unless the extraction mode explicitly requires them.

### Step 3 — Extract according to mode

For `top_equipment_header_with_dwg`:

1. Extract the page `DWG NO.` from the title block.
2. Extract `system_name` from the title block as the line between the project line and the title suffix line.
3. Inspect the separated equipment/header region at the top of the sheet.
4. For each equipment item in that top region, extract:
   - `equipment_number`
   - `equipment_name`
   - `system_name` = extracted title-block system name
   - `drawing` = extracted `DWG NO.`
   - `source_page` = `PAGE_NUM`
4.5. When helper slices are provided, inspect all slices before concluding extraction is complete.
4.6. When the top header is arranged as multiple separated clusters across the page width, treat each underlined tag/name cluster as an independent finding even if some clusters sit lower than others within the same header band.
4.7. Deduplicate within the page only when the same tag/name cluster appears in overlapping slices; do not collapse distinct grouped-tag findings.
5. If the top-of-sheet region contains no relevant equipment header, record **no findings**.
6. Do not backfill from the body of the drawing when the top header is absent.
7. If the apparent top region contains only notes, setpoints, spec text, or instrument/control annotations rather than discrete equipment header blocks, record **no findings**.

### Step 4 — Apply extraction rules

**RULE 1 — NO INVENTION**
- Extract only what is visible.
- If a tag or name is ambiguous, preserve what is legible and do not normalize beyond certainty.

**RULE 2 — REGION DISCIPLINE**
- Respect the extraction scope.
- For `top_equipment_header_with_dwg`, only the separated top header region counts for equipment findings.
- Ignore the right-side notes area even when it sits at the top of the sheet.
- Ignore lower vendor/model/specification lines inside a dense header block if they are not part of the primary equipment name.
- When helper crops are provided, they define the primary bounded reading region unless they are clearly incomplete for the current page.

**RULE 3 — REQUIRED COMPANION FIELDS**
- `DWG NO.` and `system_name` are mandatory.
- If either cannot be extracted with confidence, return `RUN_STATUS=FAILED` and write a failure artifact.

**RULE 3.5 — TAG REQUIRED FOR A FINDING**
- Do not emit a finding row when `equipment_number` is blank.
- Do not emit control/instrument rows such as setpoint bubbles, controller tags, PSV/PCV/FIC style annotations, or standards references when the extraction mode is equipment-focused.

**RULE 3.6 — PRIMARY NAME ONLY**
- `equipment_name` must be the primary equipment label only.
- Exclude adjacent notes, duty text, vendor/model text, frame/common-base text, API/TEMA references, dimensions, pressure/temperature setpoints, and operating comments.
- When a dense multi-line block is present, prefer the shortest line that still names the equipment.

**RULE 3.7 — MULTI-BLOCK HEADER COMPLETENESS**
- Do not assume all findings share one baseline or appear in one continuous top row.
- On compressor-train style sheets and similar repeated layouts, include lower standalone pump/header blocks and right-side frame blocks when they are still part of the separated top-header region.
- A valid page may contain both left-to-right top-row findings and a second staggered row of findings within the same header band.

**RULE 3.8 — LOW-COUNT SKEPTICISM**
- Do not assume `0`, `1`, or `2` findings are correct simply because a few tags were found.
- If helper slices show additional underlined tag/name clusters, keep extracting until all visible current-page header blocks have been accounted for or explicitly excluded as non-equipment.
- `NO_FINDINGS` is only valid when the bounded header region truly lacks discrete equipment header blocks.

**RULE 4 — GROUPED TAGS**
- Preserve grouped identifiers exactly as shown when they are presented as one item, such as `P-7260-2/7270-2`.

**RULE 5 — EMPTY PAGES ARE VALID**
- If the page has no matching extraction targets, that is a valid result, not an error.

### Step 5 — Write structured output

If `OUTPUT_FORMAT=markdown_stub`:

1. Write a page-scoped Markdown artifact containing:
   - source PDF name if provided
   - source page
   - `DWG NO.`
   - `system_name`
   - a four-column table with:
     - `equipment_number`
     - `equipment_name`
     - `system_name`
     - `drawing`
2. If no findings are present, write an empty-row table and a note that no separated top-of-sheet equipment header was identified.

If `OUTPUT_FORMAT=csv_row`:

1. Write CSV content only.
2. Header MUST be:
   - `equipment_number,equipment_name,system_name,drawing,source_page,status`
3. If findings exist, write one row per extracted item with `status=FOUND`.
4. If no findings exist, write one row with blank equipment fields, populated `drawing`, populated `source_page`, and `status=NO_FINDINGS`.

### Step 6 — Return status

- If one or more findings were extracted: return `RUN_STATUS=SUCCESS`
- If the page was readable but no relevant extraction target was present: return `RUN_STATUS=NO_FINDINGS`
- If inputs were invalid: return `RUN_STATUS=FAILED_INPUTS`
- If the page could not be interpreted or `DWG NO.` could not be extracted: return `RUN_STATUS=FAILED`

[[END:PROTOCOL]]

---

[[BEGIN:SPEC]]
## SPEC

A DRAWING_EXTRACT_PAGE run is valid when:

### S1 — Exactly one file written
`OUTPUT_PATH` exists and contains one valid structured artifact.

### S2 — No side effects
No files other than `OUTPUT_PATH` are read or written.

### S3 — Required title-block provenance present
The output contains `DWG NO.` and `system_name` unless the run failed.

### S4 — Scoped extraction only
Extracted findings reflect only the region and semantics required by `EXTRACTION_MODE`.

### S5 — No invention
The agent does not add tags, names, or classifications not visible in the image.

### S5.5 — No blank-tag findings
Rows with blank `equipment_number` are invalid for `top_equipment_header_with_dwg`.

### S6 — No-findings pages are explicit
Pages with no relevant extraction targets return `RUN_STATUS=NO_FINDINGS` and still produce a valid artifact.

[[END:SPEC]]

---

[[BEGIN:STRUCTURE]]
## STRUCTURE

### Output file format — `markdown_stub`

`OUTPUT_PATH` contains:

1. A page title
2. Source metadata
3. `DWG NO.`
4. `system_name`
5. A findings table:

```md
| equipment_number | equipment_name | system_name | drawing |
| --- | --- | --- | --- |
| ... | ... | ... | ... |
```

If no findings:

```md
| equipment_number | equipment_name | system_name | drawing |
| --- | --- | --- | --- |
|  |  |  |  |
```

plus a note stating that no separated top-of-sheet equipment header was found.

### Output file format — `csv_row`

`OUTPUT_PATH` contains CSV text with header:

```csv
equipment_number,equipment_name,system_name,drawing,source_page,status
```

One row per finding, or one `NO_FINDINGS` row if none exist.

### Return value

The agent returns to its caller:
- `RUN_STATUS`: `SUCCESS` | `NO_FINDINGS` | `FAILED` | `FAILED_INPUTS`
- `PAGE_NUM`: page number processed
- `FINDING_COUNT`: number of extracted findings
- `DWG_NO`: extracted drawing number if available
- `SYSTEM_NAME`: extracted title-block system name if available

[[END:STRUCTURE]]

---

[[BEGIN:RATIONALE]]
## RATIONALE

DRAWING_EXTRACT_PAGE exists because engineering drawings are not the same as text pages:

1. **Selective extraction is the task** — not full-page transcription.
2. **Spatial semantics matter** — top header regions and title blocks have distinct meaning.
3. **No-findings pages are normal** — many drawing sheets are piping-only or otherwise outside the extraction scope.
4. **Structured outputs are the target** — page-level stubs and CSV rows are more useful than raw Markdown transcription for downstream collation.

In production drawing sets, missed entities usually come from extraction posture, not from obviously different documents: valid header findings can be split across staggered multiblock layouts, and malformed local header text can sometimes be resolved only by inspecting the bounded current-page context carefully. That is why this agent prefers helper crops and header slices, and why it treats low-count and `NO_FINDINGS` outcomes skeptically until the visible current-page header blocks have been fully accounted for.

This keeps `PDF2MD_PAGE` clean as a transcription worker while providing a separate instruction contract for drawing-aware extraction workflows.

[[END:RATIONALE]]
