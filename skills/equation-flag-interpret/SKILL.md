---
name: equation-flag-interpret
description: Convert one human-written natural-language correction note about one display equation into a corrected LaTeX expression. Per-flag bounded dispatch invoked by EQUATION_AUDIT during Phase 3a, one TASK per flagged entry whose `description` is prose rather than LaTeX.
compatibility: Chirality TASK; invoked by EQUATION_AUDIT for per-flag interpretation in Phase 3a
metadata:
  chirality-skill-version: "1"
  chirality-task-profile: NONE
---

# SKILL — equation-flag-interpret

## Purpose

Read one flagged-equation entry — comprising the current (incorrect) LaTeX expression, the human's natural-language description of what is wrong or how to fix it, and optionally the source page raster for visual context — and emit ONE corrected LaTeX expression as a small JSON file at `OUTPUT_PATH`.

This skill replaces the deterministic-tool subprocess fork that the legacy `process_flagged.py --interpret` flag used (`tools/equation_audit/process_flagged.py` shelled out to the `claude` CLI in Sonnet mode). That pattern violated workflow-component standard R12 (LLM reasoning inside a deterministic tool). All such reasoning now happens here, inside a bounded TASK skill loaded by the persona.

## Suitable agent shells

- `TASK` in generic shell mode, spawned by the `EQUATION_AUDIT` persona.

Not the right fit for:
- batch re-interpretation across many equations (run one TASK per entry; the persona orchestrates)
- equation re-extraction or page-level re-OCR (use `audit_equations.py` + `equation-bbox-detect` instead)
- modifying anything other than one corrected LaTeX expression (no scope creep — this skill emits exactly one corrected LaTeX, nothing else)

## Inputs

### Required (via `RuntimeOverrides`)

- `EQUATION_KEY` — the `<page>:<hash>` key identifying the flagged entry in `flagged.json`
- `PAGE_NUM` — the page the equation appears on (1-indexed)
- `EQUATION_HASH` — the 12-char hex hash of the current (incorrect) LaTeX
- `CURRENT_LATEX` — the current (incorrect) LaTeX expression as a literal block
- `FLAG_NOTE` — the human's natural-language description of the correction
- `OUTPUT_PATH` — absolute path where the interpreted-LaTeX JSON will be written

### Optional

- `PAGE_IMAGE_PATH` — absolute path to the page raster (PNG). Use ONLY to disambiguate symbols the note references implicitly. Do NOT re-OCR the page; trust `CURRENT_LATEX` as the authoritative transcription baseline.

## Runtime overrides

| Key | Meaning | Default | Allowed values |
|---|---|---|---|
| `EQUATION_KEY` | `<page>:<hash>` identifier | **Required** | `<int>:<12-hex>` |
| `PAGE_NUM` | Page number | **Required** | Positive integer |
| `EQUATION_HASH` | Hash of current LaTeX | **Required** | 12 lowercase hex chars |
| `CURRENT_LATEX` | Original (incorrect) LaTeX | **Required** | Non-empty string |
| `FLAG_NOTE` | Human correction note | **Required** | Non-empty string |
| `OUTPUT_PATH` | Where to write the interpreted JSON | **Required** | Parent dir exists; `.json` |
| `PAGE_IMAGE_PATH` | Optional page PNG for visual disambiguation | None | Existing `.png` file |

## Read boundary

Reads are limited to:

- `PAGE_IMAGE_PATH` (if provided) — the single page PNG, multimodal load.

No other reads. The skill MUST NOT:
- read `flagged.json` itself (the brief embeds the entry's fields verbatim)
- read other pages
- read `equations.jsonl` or any other audit artifact
- cross-reference earlier equations on the page or other pages

## Write boundary

Writes are limited to exactly one file:

- `OUTPUT_PATH` — the interpreted-LaTeX JSON

No other side effects.

## Tool usage

- No deterministic tools are invoked. This is a reasoning-only skill (optionally augmented by the multimodal Read tool when `PAGE_IMAGE_PATH` is provided).
- The `allowed-tools` frontmatter field is intentionally omitted.

Disallowed behavior:

- MUST NOT shell out to any subprocess or external command.
- MUST NOT invent equation content not implied by the note.
- MUST NOT re-extract or re-OCR the page — `CURRENT_LATEX` is authoritative.
- MUST NOT widen the correction beyond what the note describes.
- MUST NOT write any file other than `OUTPUT_PATH`.

## Method

### Step 1 — Validate inputs

1. Confirm `CURRENT_LATEX` and `FLAG_NOTE` are non-empty.
2. Confirm `OUTPUT_PATH` parent directory exists.
3. If any required input is missing, write `{"key": "<EQUATION_KEY>", "interpreted_latex": "", "reason": "missing required input"}` to `OUTPUT_PATH` and return `RUN_STATUS=FAILED_INPUTS`.

### Step 2 — Read the note and the LaTeX together

1. Examine `CURRENT_LATEX` to understand the equation's current structure.
2. Read `FLAG_NOTE` as a directive about what is wrong or how to fix it. Common note shapes:
   - **Replacement note** — "denominator should be 2 not 3"
   - **Insertion note** — "missing a sigma in the second term"
   - **Symbol-substitution note** — "numerator should be ℓ (cursive ell) not e"
   - **Restructuring note** — "left side should be Y/2 not Y"
3. If `PAGE_IMAGE_PATH` is provided AND the note's intent is ambiguous (e.g., it references "the symbol on the left" without specifying which), use the Read tool to load the PNG. Use the image only to disambiguate — do not re-OCR.

### Step 3 — Synthesize the corrected LaTeX

1. Start from `CURRENT_LATEX` and apply ONLY the change the note describes.
2. Preserve every other element of the original expression verbatim (subscripts, superscripts, numbering tags like `\qquad (1.5)`, spacing commands, fraction structures, etc.).
3. The output is a single LaTeX expression — NO `$$` delimiters, NO Markdown code fences, NO commentary, NO surrounding quotes.
4. The output must be syntactically valid LaTeX (parsable by KaTeX). When in doubt about a non-standard symbol, prefer a standard equivalent (e.g., `\ell` for cursive ell, `\beta` for beta).

### Step 4 — Handle ambiguity

If after Step 2 + Step 3 the note remains too ambiguous to interpret unambiguously, DO NOT GUESS:

1. Set `interpreted_latex` to the empty string.
2. Add a `reason` field describing the ambiguity.

The persona then surfaces the ambiguity to the human at Gate 5 (Verify backcheck) rather than applying a guessed fix.

### Step 5 — Write outputs

1. Write `OUTPUT_PATH` as a single JSON object with the schema below.

```json
{
  "key": "<EQUATION_KEY>",
  "page": <PAGE_NUM>,
  "hash": "<EQUATION_HASH>",
  "current_latex": "<CURRENT_LATEX>",
  "interpreted_latex": "<corrected LaTeX | empty if ambiguous>",
  "source_note": "<FLAG_NOTE>",
  "reason": "<optional; populated only when interpreted_latex is empty>"
}
```

### Step 6 — Return status

Return one of:

- `RUN_STATUS=SUCCESS` — `interpreted_latex` is non-empty and applies the note's correction.
- `RUN_STATUS=NO_FINDINGS` — note was too ambiguous; `interpreted_latex` is empty with a `reason`.
- `RUN_STATUS=FAILED_INPUTS` — required inputs were missing.
- `RUN_STATUS=FAILED` — interpretation failed for an unexpected reason (encoding, write boundary violation, etc.).

Also return: `EQUATION_KEY`, `PAGE_NUM`, `EQUATION_HASH`.

## Non-negotiable constraints

- **One-equation discipline.** Exactly one corrected LaTeX expression per invocation. No batch processing.
- **CURRENT_LATEX is authoritative.** Do not re-transcribe the equation from the page image; trust the brief's input.
- **Note-fidelity.** Apply ONLY the change the note describes. Do not "improve" surrounding LaTeX, do not normalize unrelated symbols, do not strip the equation's numbering tag.
- **No invention.** If the note does not specify a change for some part of the expression, that part stays exactly as it appears in `CURRENT_LATEX`.
- **No `$$` delimiters in output.** `process_flagged.py` substitutes the corrected LaTeX INSIDE the existing `$$...$$` delimiters in per-page Markdown.
- **Write-path-only writes.** Exactly one file is written per invocation. No other side effects.

## QA expectations

- Exactly one file exists at `OUTPUT_PATH` after the run.
- The file is valid JSON; top-level is a single object (not a list).
- `key`, `page`, `hash`, `current_latex`, `interpreted_latex`, `source_note` keys all present.
- `interpreted_latex` is either non-empty LaTeX OR explicitly empty with a `reason` field.
- If non-empty, `interpreted_latex` contains no `$$` delimiters, no Markdown code fences, no surrounding quotes.
- `RUN_STATUS` is one of: `SUCCESS`, `NO_FINDINGS`, `FAILED_INPUTS`, `FAILED`.

## Relationship to EQUATION_AUDIT

This skill is the per-flag worker invoked by the `EQUATION_AUDIT` persona during Phase 3a. The persona:

- iterates the (validated) `flagged.json`, detecting entries whose `description` is prose-shaped (via `tools/equation_audit/validate_flagged_schema.py`),
- renders one INIT-TASK brief per such entry via `tools/equation_audit/build_equation_interpret_brief.py`,
- dispatches one `TASK + equation-flag-interpret` invocation per brief,
- collects the per-flag JSON outputs and merges each `interpreted_latex` back into `flagged.json`'s `description` field for that key,
- re-runs `validate_flagged_schema.py` (Phase 3b) — at this point every description must be LaTeX-shaped,
- runs `process_flagged.py` (Phase 3c) to apply the fixes deterministically.

This skill is a sibling of `pdf2md-page` and `drawing-extract-page` — same per-item fanout pattern, but per-flag interpretation instead of per-page extraction.
