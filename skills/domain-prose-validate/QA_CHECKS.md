# domain-prose-validate - QA Checks

Minimum checks for a valid run:

1. `IMAGE_PATH` exists and has a `.png` extension, or the skill aborts without writing.
2. `ASSET_BBOX_HINTS_PATH` exists and has a `.json` extension, or the skill aborts without writing.
3. `OUTPUT_PATH` parent directory exists before write.
4. `OUTPUT_PATH` exists after the run and is non-empty.
5. `OUTPUT_PATH` ends with a single trailing newline (`\n`).
6. No files other than `IMAGE_PATH` and `ASSET_BBOX_HINTS_PATH` were read. **In particular, no `page_*.md`, no assembled `<book>.md`, and no audit sidecar was opened.** This is the load-bearing anti-confirmation-bias invariant of Gate 1.5-P Stage 1.
7. No files other than `OUTPUT_PATH` were written.

## Output body checks

The output Markdown body must satisfy:

| Check | Requirement |
|---|---|
| No frontmatter | The file must not begin with a YAML frontmatter block (`---`). The body is page content only. |
| No metadata heading | The file must not include a `# Page N`, `## Page N`, or other page-identifying heading. |
| Display equations | Standalone equations appear as `$$...$$` blocks on their own line(s), surrounded by blank lines. |
| Inline equations | Equations embedded in prose appear as `$...$` (single-dollar). |
| Asset placeholder syntax | Each asset placeholder is on its own line, surrounded by blank lines, and uses exactly one of: `[FIGURE: <text>]`, `[TABLE: <text>]`, `[IMAGE: <text>]`. The prefix is uppercase, followed by a colon and a single space. |
| No image / link syntax for assets | The output must not contain `![alt](path)` image syntax or `[XLSX](path)` link syntax. Asset references use the bracketed placeholder form only. |
| No asset IDs | The output must not contain `asset_id` values copied from `ASSET_BBOX_HINTS_PATH` (e.g. `BookX_p0047_fig01`). |

## Placeholder-count consistency

Compare the placeholder counts in `OUTPUT_PATH` against `ASSET_BBOX_HINTS_PATH`:

| Hints entry kind | Placeholder form | Expected relationship |
|---|---|---|
| `kind == "fig"` | `[FIGURE: ...]` | Count should match within reasonable tolerance |
| `kind == "tbl"` | `[TABLE: ...]` | Count should match within reasonable tolerance |
| `kind == "img"` | `[IMAGE: ...]` | Count should match within reasonable tolerance |

Note: a count mismatch is **not** a skill-level failure — it is exactly the signal Gate 1.5-P Stage 2 needs to surface as a structural fail for the page. The QA check exists so the orchestrator can flag implausibly large drift (e.g. zero placeholders emitted when the hints file lists four assets) for orchestrator-side review before invoking the comparator.

## Failure posture

| Failure mode | Required behavior |
|---|---|
| Missing input file (`IMAGE_PATH` or `ASSET_BBOX_HINTS_PATH`) | Abort without writing. The orchestrator will treat the absent re-extract as a Stage 2 structural fail for the page. |
| Unreadable page raster | Abort without writing, or write only the legible portion with no fabricated content. Do not paraphrase or summarize unreadable regions. |
| Confirmation-bias breach (asked to read a `page_*.md` or `<book>.md`) | Refuse the read. The skill MUST NOT consult any prior extract under any circumstance. |
| Hints file is empty or has zero assets | Emit prose + equations only. Do not synthesize asset placeholders to match an imagined manifest. |
| Hints file references kinds not in `{fig, tbl, img}` | Ignore the unknown kind. Stage 2 will surface the mismatch. |

## Orchestrator-side checks

These checks belong to the Gate 1.5-P orchestration, not this skill:

- Building the per-page `ASSET_BBOX_HINTS_PATH` from the asset manifest before dispatch.
- Verifying `OUTPUT_PATH` was created and is non-empty after each TASK completes.
- Confirming no `page_*.md` was opened during the TASK (audit-log inspection where available).
- Running `tools/source_audit/compare_extracts.py` against each `(page_NNNN.md, page_NNNN.reextract.md)` pair to produce `prose_validation.json` (Stage 2).
- Dispatching `pdf2md-page-assets` re-extraction for pages flagged with structural fails (Stage 3).
- Dispatching `equation-flag-interpret` for equation-content proposals before writing to `equations_backcheck.json` with `source: "1.5-P-machine"` (Stage 3).
