# equation-flag-interpret contract

## Brief

### Brief structure

The brief is an INIT-TASK shape rendered by `tools/equation_audit/build_equation_interpret_brief.py`. The worker receives the brief verbatim via TASK.

```yaml
PURPOSE: Interpret the human's natural-language correction note for the equation on page <N> (hash <H>) and emit a corrected LaTeX expression
RequestedBy: WORKING_ITEMS
ParentWorkflow: equation-audit
ActingSurface: TASK+equation-flag-interpret

ScopePath: <absolute path to audit/equations/working/ folder>
Workflow: equation-flag-interpret

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

### Required RuntimeOverrides

| Key | Type | Constraint |
|---|---|---|
| `EQUATION_KEY` | str | `<int>:<12-hex>` |
| `PAGE_NUM` | int | ≥ 1 |
| `EQUATION_HASH` | str | exactly 12 lowercase hex chars; equals the hash portion of `EQUATION_KEY` |
| `CURRENT_LATEX` | str | non-empty; the original (incorrect) LaTeX |
| `FLAG_NOTE` | str | non-empty; the human's correction note (prose or LaTeX) |
| `OUTPUT_PATH` | str | absolute path; parent directory must exist; ends in `.json` |

### Optional RuntimeOverrides

| Key | Type | Constraint |
|---|---|---|
| `PAGE_IMAGE_PATH` | str | absolute path to an existing `.png` file |

### Output schema

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

### Status reporting

The worker returns one of:

- `RUN_STATUS=SUCCESS` — `interpreted_latex` is non-empty
- `RUN_STATUS=NO_FINDINGS` — ambiguous note; `interpreted_latex` is empty with a `reason`
- `RUN_STATUS=FAILED_INPUTS` — required input missing
- `RUN_STATUS=FAILED` — unexpected failure

Plus: `EQUATION_KEY`, `PAGE_NUM`, `EQUATION_HASH`.

## Acceptance

### Output presence

- Exactly one file exists at `OUTPUT_PATH` after the run.
- No other files outside the declared write boundary were created or modified.

### Output JSON schema

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

### LaTeX-shape invariants (when `interpreted_latex` is non-empty)

- Does NOT begin or end with `$$` or `$`. The downstream `process_flagged.py` substitutes the interpreted LaTeX INSIDE the existing `$$...$$` delimiters in per-page Markdown; including delimiters here would double-wrap.
- Does NOT contain Markdown code fences (no triple-backticks).
- Does NOT contain surrounding quote marks added by the worker.
- Is syntactically valid LaTeX as KaTeX would parse it. Common allowed commands include `\frac`, `\sqrt`, `\sigma`, `\alpha`, `\ell`, `\qquad`, `\cdot`, `\sum`, `\int`, `\to`, etc.

### Note-fidelity invariants

For every successful interpretation:

- Every character of `current_latex` that the note does NOT target appears verbatim in `interpreted_latex`. The workflow must not "improve" surrounding LaTeX.
- The equation's numbering tag (e.g., `\qquad (1.5)`) is preserved exactly if present in `CURRENT_LATEX`.
- The structural shape (left-hand side, equals sign, right-hand side; fractions; products; etc.) is preserved unless the note explicitly restructures the expression.
- The output is NOT identical to `current_latex` — that would mean no correction was applied. (Exception: the workflow may emit identical output if it determines the note proposes no change; this is `RUN_STATUS=NO_FINDINGS` with a `reason`.)

### Ambiguity handling

A note is treated as ambiguous (and `interpreted_latex` left empty) when ANY of the following hold:

- The note references "the symbol" / "the term" / "the variable" without specifying which.
- The note describes a correction whose target cannot be uniquely identified in `CURRENT_LATEX`.
- The note describes a correction that requires information not present in `CURRENT_LATEX`, `FLAG_NOTE`, or (if provided) `PAGE_IMAGE_PATH`.
- Multiple equally-valid interpretations of the note exist.

For ambiguous notes, `interpreted_latex` is the empty string and `reason` is a short, specific explanation (≤ 50 words). WORKING_ITEMS surfaces ambiguity through the human review surface before schema validation and fix application.

### Failure reporting

The worker reports a structured `RUN_STATUS`:

- `SUCCESS` — `interpreted_latex` non-empty; all checks above pass
- `NO_FINDINGS` — note too ambiguous; `interpreted_latex` empty with `reason`
- `FAILED_INPUTS` — required inputs were missing or malformed
- `FAILED` — interpretation failed for an unexpected reason

The worker also reports:

- `EQUATION_KEY`
- `PAGE_NUM`
- `EQUATION_HASH`

### Defects that block downstream

These defects block `process_flagged.py` from applying the fix (WORKING_ITEMS must re-dispatch this workflow or surface the entry for human attention):

- Output file missing or unparseable as JSON
- `interpreted_latex` contains `$$` delimiters or code fences
- `interpreted_latex` is non-empty but not syntactically valid LaTeX
- `key`, `page`, or `hash` does not match the brief
- A non-targeted character was changed (note-fidelity violation)
- Output written to a path other than `OUTPUT_PATH`

### Required evidence

- Worker stdout / `RUN_STATUS` captured by TASK is sufficient evidence for routine success.
- For `FAILED` and `FAILED_INPUTS` runs, the explanation accompanying `RUN_STATUS` is the evidence; WORKING_ITEMS decides whether to re-dispatch with corrected inputs.
- For `NO_FINDINGS` runs, the `reason` field IS the evidence — WORKING_ITEMS surfaces it for human clarification before retrying interpretation.

## Tool use

### Preferred tool order

This workflow is reasoning-only over the brief's inputs. There is no deterministic tool the worker runs from inside the dispatch. The surrounding pipeline runs deterministic tools (brief building, schema validation, fix application, re-extraction) outside the worker, on the orchestrator side.

### Allowed deterministic tools

#### Operationally invoked

The agent's native tools are available implicitly:

- `Read` — used to load `PAGE_IMAGE_PATH` (multimodal PNG input) when provided, ONLY for symbol disambiguation.
- `Write` — used to write the single `OUTPUT_PATH` JSON file.

No `Bash`, no shell-outs, no subprocess invocations.

### Surrounding deterministic tools (orchestrator-side, NOT worker-side)

| Tool | Owner | When |
|---|---|---|
| `tools/equation_audit/build_equation_interpret_brief.py` | HELPS_HUMANS | equation-audit Phase 3a — produces this workflow's brief |
| `tools/equation_audit/validate_flagged_schema.py` | HELPS_HUMANS | equation-audit Phase 3b — confirms every flagged entry now has a LaTeX-shaped description before fixes apply |
| `tools/equation_audit/process_flagged.py` | HELPS_HUMANS | equation-audit Phase 3c — applies the fixes deterministically |
| `tools/equation_audit/audit_equations.py` | HELPS_HUMANS | equation-audit Phase 4 — re-extracts equations and emits backcheck.json |

The worker never invokes any of the above. It writes its single JSON output; WORKING_ITEMS merges that JSON back into `flagged.json`'s `description` field and proceeds.

### Expected use of reasoning

The worker uses LLM reasoning to:

1. **Parse the human note.** Identify the intent: replacement, insertion, deletion, restructuring, or symbol substitution.
2. **Locate the affected part of `CURRENT_LATEX`.** Knowing the original expression's structure (fractions, sums, equations of motion, etc.).
3. **Apply the change.** Preserve every unrelated character; modify only what the note targets.
4. **Optionally consult `PAGE_IMAGE_PATH`** to disambiguate symbols when the note is unclear (e.g., "the second symbol" without specifying which).
5. **Produce syntactically valid LaTeX.** Outputs that fail KaTeX parsing will be caught downstream and re-dispatched.
6. **Refuse to guess.** If the note remains ambiguous after Step 4, emit an empty `interpreted_latex` with an explicit `reason`. WORKING_ITEMS surfaces ambiguity for human clarification before retrying interpretation.

### Disallowed use

- No deterministic tool invocation from inside the worker (no `Bash`, no `python3`, no shell-out, no subprocess).
- No writing outside `OUTPUT_PATH`.
- No reading outside `PAGE_IMAGE_PATH` (and only when explicitly provided in the brief).
- No `$$` delimiters or Markdown code fences in the emitted LaTeX.
- No re-OCR of the page image (the original `CURRENT_LATEX` is authoritative — the page image is for disambiguation only).
- No batch processing (one TASK = one equation; WORKING_ITEMS dispatches one TASK per flagged entry).
- No editing the page Markdown directly (`process_flagged.py` owns that write).
- No mutation of `flagged.json` (WORKING_ITEMS merges this workflow's output back; the workflow writes only to `OUTPUT_PATH`).

### Write boundary

Exactly one write per invocation:

```
<OUTPUT_PATH>
```

The path is absolute. Parent directory must exist; this workflow does not create directories.

If a write would violate the boundary, the worker returns `RUN_STATUS=FAILED` with an explanatory note and does NOT attempt a workaround.
