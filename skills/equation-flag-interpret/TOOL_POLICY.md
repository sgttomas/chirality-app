# TOOL POLICY — equation-flag-interpret

## Preferred tool order

This skill is reasoning-only over the brief's inputs. There is no deterministic tool the worker runs from inside the dispatch. The surrounding pipeline runs deterministic tools (brief building, schema validation, fix application, re-extraction) outside the worker, on the orchestrator side.

## Allowed deterministic tools

### TASK-enforced

None. The `allowed-tools` frontmatter field is intentionally omitted from `SKILL.md`. TASK does not whitelist any tool for this skill.

### Operationally invoked

The agent's native tools are available implicitly:

- `Read` — used to load `PAGE_IMAGE_PATH` (multimodal PNG input) when provided, ONLY for symbol disambiguation.
- `Write` — used to write the single `OUTPUT_PATH` JSON file.

No `Bash`, no shell-outs, no subprocess invocations.

## Surrounding deterministic tools (orchestrator-side, NOT worker-side)

| Tool | Owner | When |
|---|---|---|
| `tools/equation_audit/build_equation_interpret_brief.py` | HELPS_HUMANS | EQUATION_AUDIT Phase 3a — produces this skill's brief |
| `tools/equation_audit/validate_flagged_schema.py` | HELPS_HUMANS | EQUATION_AUDIT Phase 3b — confirms every flagged entry now has a LaTeX-shaped description before fixes apply |
| `tools/equation_audit/process_flagged.py` | HELPS_HUMANS | EQUATION_AUDIT Phase 3c — applies the fixes deterministically |
| `tools/equation_audit/audit_equations.py` | HELPS_HUMANS | EQUATION_AUDIT Phase 4 — re-extracts equations and emits backcheck.json |

The worker never invokes any of the above. It writes its single JSON output; the persona merges that JSON back into `flagged.json`'s `description` field and proceeds.

## Expected use of reasoning

The worker uses LLM reasoning to:

1. **Parse the human note.** Identify the intent: replacement, insertion, deletion, restructuring, or symbol substitution.
2. **Locate the affected part of `CURRENT_LATEX`.** Knowing the original expression's structure (fractions, sums, equations of motion, etc.).
3. **Apply the change.** Preserve every unrelated character; modify only what the note targets.
4. **Optionally consult `PAGE_IMAGE_PATH`** to disambiguate symbols when the note is unclear (e.g., "the second symbol" without specifying which).
5. **Produce syntactically valid LaTeX.** Outputs that fail KaTeX parsing will be caught downstream and re-dispatched.
6. **Refuse to guess.** If the note remains ambiguous after Step 4, emit an empty `interpreted_latex` with an explicit `reason`. The persona surfaces ambiguity at Gate 5.

## Disallowed use

- No deterministic tool invocation from inside the worker (no `Bash`, no `python3`, no shell-out, no subprocess).
- No writing outside `OUTPUT_PATH`.
- No reading outside `PAGE_IMAGE_PATH` (and only when explicitly provided in the brief).
- No `$$` delimiters or Markdown code fences in the emitted LaTeX.
- No re-OCR of the page image (the original `CURRENT_LATEX` is authoritative — the page image is for disambiguation only).
- No batch processing (one TASK = one equation; the persona dispatches one TASK per flagged entry).
- No editing the page Markdown directly (`process_flagged.py` owns that write).
- No mutation of `flagged.json` (the persona merges this skill's output back; the skill writes only to `OUTPUT_PATH`).

## Write boundary

Exactly one write per invocation:

```
<OUTPUT_PATH>
```

The path is absolute. Parent directory must exist; this skill does not create directories.

If a write would violate the boundary, the worker returns `RUN_STATUS=FAILED` with an explanatory note and does NOT attempt a workaround.
