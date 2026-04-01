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
| `OUTPUT_PATH` | MUST | Absolute path to write the extraction output |
| `PAGE_NUM` | MUST | 1-indexed page number |
| `TOTAL_PAGES` | MUST | Total pages in the source document |
| `EXTRACTION_MODE` | MUST | Extraction target definition; see supported modes below |
| `OUTPUT_FORMAT` | MUST | `markdown_stub` or `csv_row` |
| `SOURCE_PDF_NAME` | MAY | PDF filename for provenance in output |

### Supported extraction modes

| Mode | Meaning |
|---|---|
| `top_equipment_header_with_dwg` | Extract equipment numbers and names from the separated top-of-sheet equipment header, and extract the page `DWG NO.` |

This agent MUST fail inputs for any extraction mode not explicitly supported by its instructions.

---

## Non-negotiable Invariants

- This agent MUST NOT behave like a full-page transcription agent. It performs only the extraction defined by `EXTRACTION_MODE`.
- This agent MUST NOT read any file other than `IMAGE_PATH`. Zero cross-page context.
- This agent MUST extract `DWG NO.` whenever a supported extraction mode is run. `DWG NO.` is mandatory companion metadata.
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
2. Confirm `OUTPUT_PATH` parent directory exists.
3. Confirm `EXTRACTION_MODE` is supported.
4. Confirm `OUTPUT_FORMAT` is `markdown_stub` or `csv_row`.
5. If inputs are invalid, write a failure placeholder to `OUTPUT_PATH` and return `RUN_STATUS=FAILED_INPUTS`.

### Step 2 — Read and inspect the page image

1. Use the Read tool to load `IMAGE_PATH`.
2. Identify the following page regions as needed by the extraction mode:
   - the **top-of-sheet separated equipment header region**
   - the **title block / `DWG NO.` region**
3. Ignore decorative borders, general process lines, and repeated in-body equipment tags unless the extraction mode explicitly requires them.

### Step 3 — Extract according to mode

For `top_equipment_header_with_dwg`:

1. Extract the page `DWG NO.` from the title block.
2. Inspect the separated equipment/header region at the top of the sheet.
3. For each equipment item in that top region, extract:
   - `equipment_number`
   - `equipment_name`
   - `drawing` = extracted `DWG NO.`
   - `source_page` = `PAGE_NUM`
4. If the top-of-sheet region contains no relevant equipment header, record **no findings**.
5. Do not backfill from the body of the drawing when the top header is absent.

### Step 4 — Apply extraction rules

**RULE 1 — NO INVENTION**
- Extract only what is visible.
- If a tag or name is ambiguous, preserve what is legible and do not normalize beyond certainty.

**RULE 2 — REGION DISCIPLINE**
- Respect the extraction scope.
- For `top_equipment_header_with_dwg`, only the separated top header region counts for equipment findings.

**RULE 3 — REQUIRED COMPANION FIELD**
- `DWG NO.` is mandatory.
- If the drawing number cannot be extracted with confidence, return `RUN_STATUS=FAILED` and write a failure artifact.

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
   - a three-column table with:
     - `equipment_number`
     - `equipment_name`
     - `drawing`
2. If no findings are present, write an empty-row table and a note that no separated top-of-sheet equipment header was identified.

If `OUTPUT_FORMAT=csv_row`:

1. Write CSV content only.
2. Header MUST be:
   - `equipment_number,equipment_name,drawing,source_page,status`
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

### S3 — Required drawing provenance present
The output contains `DWG NO.` unless the run failed.

### S4 — Scoped extraction only
Extracted findings reflect only the region and semantics required by `EXTRACTION_MODE`.

### S5 — No invention
The agent does not add tags, names, or classifications not visible in the image.

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
4. A findings table:

```md
| equipment_number | equipment_name | drawing |
| --- | --- | --- |
| ... | ... | ... |
```

If no findings:

```md
| equipment_number | equipment_name | drawing |
| --- | --- | --- |
|  |  |  |
```

plus a note stating that no separated top-of-sheet equipment header was found.

### Output file format — `csv_row`

`OUTPUT_PATH` contains CSV text with header:

```csv
equipment_number,equipment_name,drawing,source_page,status
```

One row per finding, or one `NO_FINDINGS` row if none exist.

### Return value

The agent returns to its caller:
- `RUN_STATUS`: `SUCCESS` | `NO_FINDINGS` | `FAILED` | `FAILED_INPUTS`
- `PAGE_NUM`: page number processed
- `FINDING_COUNT`: number of extracted findings
- `DWG_NO`: extracted drawing number if available

[[END:STRUCTURE]]

---

[[BEGIN:RATIONALE]]
## RATIONALE

DRAWING_EXTRACT_PAGE exists because engineering drawings are not the same as text pages:

1. **Selective extraction is the task** — not full-page transcription.
2. **Spatial semantics matter** — top header regions and title blocks have distinct meaning.
3. **No-findings pages are normal** — many drawing sheets are piping-only or otherwise outside the extraction scope.
4. **Structured outputs are the target** — page-level stubs and CSV rows are more useful than raw Markdown transcription for downstream collation.

This keeps `PDF2MD_PAGE` clean as a transcription worker while providing a separate instruction contract for drawing-aware extraction workflows.

[[END:RATIONALE]]
