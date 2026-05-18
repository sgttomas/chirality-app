# QA_CHECKS — semantic-lensing

## Minimum output validity

| Check | Validation |
|---|---|
| Lens tags present | Every proposal includes `Lens: <Matrix.Row.Column>` |
| Lens tags valid | Matrix letter exists in `_SEMANTIC.md` |
| Evidence grounded | Proposals cite production documents or accessible sources, not lensing entries |
| No invention | Content not supported by evidence is `TBD`, not fabricated |
| Conflicts surfaced | Contradictions between lensing entries and source material are in `NEEDS_HUMAN_RULING` |
| Scope respected | Only matrices in `ActiveMatrices` were processed (when specified) |
| `_SEMANTIC.md` unmodified | Read-only constraint honored |

## Failure reporting

- If `_SEMANTIC.md` is missing: report in `MISSING` — the skill cannot operate without it
- If `_SEMANTIC_LENSING.md` is missing and the brief expects enrichment processing: report in `MISSING` — skill falls back to initial lens analysis only
- If no meaningful lens findings exist: state this explicitly rather than padding output

## Evidence requirements

- Each incorporated lensing entry must trace to a source or production document location
- The lensing entry itself (`_SEMANTIC_LENSING.md` row) is a worklist pointer, not evidence
- Record which lensing entries were processed and their disposition (incorporated, converted to TBD, discarded)
