# QA CHECKS — equation-flag-interpret

## Output presence

- Exactly one file exists at `OUTPUT_PATH` after the run.
- No other files outside the declared write boundary were created or modified.

## Output JSON schema

The output file is a single JSON object (not a list, not a JSON-lines stream) containing these fields:

| Field | Type | Required | Constraint |
|---|---|---|---|
| `key` | str | yes | Matches `EQUATION_KEY` from the brief; shape `<int>:<12-hex>` |
| `page` | int | yes | Equals `PAGE_NUM` from the brief; ≥ 1 |
| `hash` | str | yes | Equals `EQUATION_HASH`; exactly 12 lowercase hex chars |
| `current_latex` | str | yes | Equals `CURRENT_LATEX` verbatim |
| `interpreted_latex` | str | yes | Non-empty LaTeX on SUCCESS; empty string on NO_FINDINGS |
| `source_note` | str | yes | Equals `FLAG_NOTE` verbatim |
| `reason` | str | conditional | Required when `interpreted_latex` is empty; absent when non-empty |

## LaTeX-shape invariants (when `interpreted_latex` is non-empty)

- Does NOT begin or end with `$$` or `$`. The downstream `process_flagged.py` substitutes the interpreted LaTeX INSIDE the existing `$$...$$` delimiters in per-page Markdown; including delimiters here would double-wrap.
- Does NOT contain Markdown code fences (no triple-backticks).
- Does NOT contain surrounding quote marks added by the worker.
- Is syntactically valid LaTeX as KaTeX would parse it. Common allowed commands include `\frac`, `\sqrt`, `\sigma`, `\alpha`, `\ell`, `\qquad`, `\cdot`, `\sum`, `\int`, `\to`, etc.

## Note-fidelity invariants

For every successful interpretation:

- Every character of `current_latex` that the note does NOT target appears verbatim in `interpreted_latex`. The skill must not "improve" surrounding LaTeX.
- The equation's numbering tag (e.g., `\qquad (1.5)`) is preserved exactly if present in `CURRENT_LATEX`.
- The structural shape (left-hand side, equals sign, right-hand side; fractions; products; etc.) is preserved unless the note explicitly restructures the expression.
- The output is NOT identical to `current_latex` — that would mean no correction was applied. (Exception: the skill may emit identical output if it determines the note proposes no change; this is `RUN_STATUS=NO_FINDINGS` with a `reason`.)

## Ambiguity handling

A note is treated as ambiguous (and `interpreted_latex` left empty) when ANY of the following hold:

- The note references "the symbol" / "the term" / "the variable" without specifying which.
- The note describes a correction whose target cannot be uniquely identified in `CURRENT_LATEX`.
- The note describes a correction that requires information not present in `CURRENT_LATEX`, `FLAG_NOTE`, or (if provided) `PAGE_IMAGE_PATH`.
- Multiple equally-valid interpretations of the note exist.

For ambiguous notes, `interpreted_latex` is the empty string and `reason` is a short, specific explanation (≤ 50 words). The persona surfaces ambiguity at Gate 5 rather than allowing a guess to flow through.

## Failure reporting

The worker reports a structured `RUN_STATUS`:

- `SUCCESS` — `interpreted_latex` non-empty; all checks above pass
- `NO_FINDINGS` — note too ambiguous; `interpreted_latex` empty with `reason`
- `FAILED_INPUTS` — required inputs were missing or malformed
- `FAILED` — interpretation failed for an unexpected reason

The worker also reports:

- `EQUATION_KEY`
- `PAGE_NUM`
- `EQUATION_HASH`

## Defects that block downstream

These defects block `process_flagged.py` from applying the fix (the persona must re-dispatch this skill or surface the entry for human attention):

- Output file missing or unparseable as JSON
- `interpreted_latex` contains `$$` delimiters or code fences
- `interpreted_latex` is non-empty but not syntactically valid LaTeX
- `key`, `page`, or `hash` does not match the brief
- A non-targeted character was changed (note-fidelity violation)
- Output written to a path other than `OUTPUT_PATH`

## Required evidence

- Worker stdout / `RUN_STATUS` captured by TASK is sufficient evidence for routine success.
- For `FAILED` and `FAILED_INPUTS` runs, the explanation accompanying `RUN_STATUS` is the evidence; the persona decides whether to re-dispatch with corrected inputs.
- For `NO_FINDINGS` runs, the `reason` field IS the evidence — the persona surfaces it at Gate 5.
