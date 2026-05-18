# pdf2md — Tool Policy

## Preferred tool order

1. `tools/pdf2md/rasterize_pdf.py`
2. direct page interpretation by the agent
3. `tools/pdf2md/postprocess_page.py`
4. `tools/reporting/clean_pdf2md_output.py`
5. `tools/pdf2md/assemble_markdown.py`
6. final `tools/reporting/clean_pdf2md_output.py`

## Allowed deterministic tools

### TASK-enforced
_Tools from the `allowed-tools` frontmatter; enforced by TASK shell at skill load time._

- `python3 tools/pdf2md/rasterize_pdf.py:*`
- `python3 tools/pdf2md/postprocess_page.py:*`
- `python3 tools/pdf2md/assemble_markdown.py:*`
- `python3 tools/reporting/clean_pdf2md_output.py:*`

### Operationally invoked
_Tools named in `## Tool usage` body; agent-guided, not TASK-enforced._

- None declared

## Expected use of reasoning

Reasoning is appropriate for:
- reconstructing diagram logic in prose, lists, or tables
- reflowing visually side-by-side tables into a different semantic layout when instructed
- spotting obvious OCR/interpretation defects

## Disallowed use

- No hidden reliance on tools outside the declared list unless the human expands `AllowedTools`.
- No sub-agent fanout under generic `TASK`.

## Write boundary

Writes should stay within:
- `OUTPUT_PATH`
- `WORK_DIR`
- or the `ScopePath` bounded local area

No writes elsewhere unless explicitly authorized by the brief.
