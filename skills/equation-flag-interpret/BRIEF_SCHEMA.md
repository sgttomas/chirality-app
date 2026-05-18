# BRIEF SCHEMA — equation-flag-interpret

## Brief structure

The brief is an INIT-TASK shape rendered by `tools/equation_audit/build_equation_interpret_brief.py`. The worker receives the brief verbatim via TASK.

```yaml
PURPOSE: Interpret the human's natural-language correction note for the equation on page <N> (hash <H>) and emit a corrected LaTeX expression
RequestedBy: EQUATION_AUDIT
ActingSurface: TASK+equation-flag-interpret

ScopePath: <absolute path to audit/equations/working/ folder>
TaskSkill: equation-flag-interpret

AllowedWriteTargets:
  - "<OUTPUT_PATH>"

RuntimeOverrides:
  EQUATION_KEY: <page>:<hash>
  PAGE_NUM: <int>
  EQUATION_HASH: <12-hex>
  CURRENT_LATEX: |-
    <original LaTeX>
  FLAG_NOTE: |-
    <human's natural-language correction note>
  PAGE_IMAGE_PATH: <optional absolute path to page PNG>
  OUTPUT_PATH: <absolute path to per-flag JSON output>

CustomInstructions:
  - Read CURRENT_LATEX and FLAG_NOTE together; the note describes what is wrong with CURRENT_LATEX or how to correct it.
  - Emit ONE corrected LaTeX expression. Do not invent unrelated content; preserve the equation's structure and only apply the note's correction.
  - If PAGE_IMAGE_PATH is provided, use it only to disambiguate symbols when the note is ambiguous.
  - Write a single JSON object to OUTPUT_PATH with keys: key, page, hash, current_latex, interpreted_latex, source_note.
  - If the note is too ambiguous to interpret unambiguously, set interpreted_latex to the empty string and add a 'reason' field; do not guess.

ExpectedOutputs:
  - <OUTPUT_PATH>
```

## Required RuntimeOverrides

| Key | Type | Constraint |
|---|---|---|
| `EQUATION_KEY` | str | `<int>:<12-hex>` |
| `PAGE_NUM` | int | ≥ 1 |
| `EQUATION_HASH` | str | exactly 12 lowercase hex chars; equals the hash portion of `EQUATION_KEY` |
| `CURRENT_LATEX` | str | non-empty; the original (incorrect) LaTeX |
| `FLAG_NOTE` | str | non-empty; the human's correction note (prose or LaTeX) |
| `OUTPUT_PATH` | str | absolute path; parent directory must exist; ends in `.json` |

## Optional RuntimeOverrides

| Key | Type | Constraint |
|---|---|---|
| `PAGE_IMAGE_PATH` | str | absolute path to an existing `.png` file |

## Output schema

The worker writes a single JSON object to `OUTPUT_PATH`:

```json
{
  "key": "5:b4fcc24a1569",
  "page": 5,
  "hash": "b4fcc24a1569",
  "current_latex": "\\frac{2}{\\sqrt{3}} Y = \\sigma_1 - \\sigma_3 = 1.155 Y \\qquad (1.5)",
  "interpreted_latex": "\\frac{2}{\\sqrt{3}} Y = \\sigma_1 - \\sigma_3 \\approx 1.15 Y \\qquad (1.5)",
  "source_note": "the 1.155 should be approximated as 1.15"
}
```

When the note is too ambiguous to interpret unambiguously, the worker emits an empty `interpreted_latex` and a `reason`:

```json
{
  "key": "12:abcdef012345",
  "page": 12,
  "hash": "abcdef012345",
  "current_latex": "x = y + z",
  "interpreted_latex": "",
  "source_note": "the symbol on the right is wrong",
  "reason": "Note does not specify which symbol on the right (y or z) is incorrect or what it should be replaced with"
}
```

## Status reporting

The worker returns one of:

- `RUN_STATUS=SUCCESS` — `interpreted_latex` is non-empty
- `RUN_STATUS=NO_FINDINGS` — ambiguous note; `interpreted_latex` is empty with a `reason`
- `RUN_STATUS=FAILED_INPUTS` — required input missing
- `RUN_STATUS=FAILED` — unexpected failure

Plus: `EQUATION_KEY`, `PAGE_NUM`, `EQUATION_HASH`.
