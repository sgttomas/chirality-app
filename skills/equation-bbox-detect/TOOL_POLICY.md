# TOOL POLICY — equation-bbox-detect

## Preferred tool order

This skill is VLM-vision-reasoning over the page raster, optionally cross-checked against the per-page Markdown's equation list. There is no deterministic tool the worker runs from inside the dispatch. The surrounding pipeline runs deterministic tools (rasterization, equation extraction, brief building, cropping) outside the worker, on the orchestrator side.

## Allowed deterministic tools

### TASK-enforced

None. The `allowed-tools` frontmatter field is intentionally omitted from `SKILL.md`. TASK does not whitelist any tool for this skill.

### Operationally invoked

The agent's native tools are available implicitly:

- `Read` — used to load `IMAGE_PATH` (multimodal PNG input) AND `PAGE_MD_PATH` (text input).
- `Write` — used to write the single `OUTPUT_PATH` JSON file.

No `Bash`, no shell-outs, no subprocess invocations.

## Surrounding deterministic tools (orchestrator-side, NOT worker-side)

| Tool | Owner | When |
|---|---|---|
| `tools/pdf2md/rasterize_pdf.py` | TOOLMAKER | PDF2MD Phase 1 — produces `page_NNNN.png` |
| `tools/equation_audit/audit_equations.py` | TOOLMAKER | EQUATION_AUDIT Phase 1 — extracts every display equation per page (text) and populates `EXPECTED_EQUATION_HASHES` |
| `tools/equation_audit/build_equation_bbox_brief.py` | TOOLMAKER | EQUATION_AUDIT Phase 1 — produces this skill's brief |
| `tools/equation_audit/crop_equation_regions.py` | TOOLMAKER | EQUATION_AUDIT Phase 1 — consumes this skill's output JSONs and emits per-equation PNG crops |

The worker never invokes any of the above. It writes its single JSON output; the persona feeds it to `crop_equation_regions.py`.

## Expected use of reasoning

The worker uses VLM/text reasoning to:

1. **Read the page raster.** Use the multimodal `Read` tool to load `IMAGE_PATH`.
2. **Read the per-page Markdown for context.** Use the text `Read` tool to load `PAGE_MD_PATH`. The MD's `$$...$$` blocks indicate which equations to expect on this page.
3. **Identify display equations on the raster.** Distinguish display equations (centered, offset, often with equation numbers) from inline math (embedded in running prose). Display equations get boxed; inline math does NOT.
4. **Determine tight bounding rectangles.** For each display equation, find the smallest axis-aligned rectangle that fully encloses the equation's typeset content (including superscripts, subscripts, integral signs, etc.) but excludes surrounding paragraph text and equation numbers (when those appear in the far-right margin separately).
5. **Normalize coordinates.** Compute `[x0, y0, x1, y1]` as fractions of the page raster's width × height.
6. **Order top-to-bottom.** Assign 1-based `index` in vertical reading order.
7. **Capture a short excerpt.** Read the first ~20 characters of visible math content as `latex_excerpt` — for the persona's cross-check against `EXPECTED_EQUATION_HASHES`. This is a hint, not authoritative transcription.

## Disallowed use

- No deterministic tool invocation from inside the worker (no `Bash`, no `python3`, no shell-out, no subprocess).
- No writing outside `OUTPUT_PATH`.
- No reading outside `IMAGE_PATH` and `PAGE_MD_PATH`.
- No full transcription of equation content (that's `pdf2md-page`'s job).
- No boxing inline equations or symbols embedded in running prose.
- No boxing section headings, table cells, figure labels, page numbers, or running headers.
- No cross-page reasoning (one TASK = one page).
- No emission of pixel coordinates (normalized [0,1] only).
- No re-OCR of body text.

## Write boundary

Exactly one write per invocation:

```
<OUTPUT_PATH>
```

The path is absolute. Parent directory must exist; this skill does not create directories.

If a write would violate the boundary, the worker returns `RUN_STATUS=FAILED` with an explanatory note and does NOT attempt a workaround.
