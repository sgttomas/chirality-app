# content-digest — QA Checks

Minimum checks for a valid run:

1. `DELIVERABLE_PATH` exists and is a directory (or absence is reported as `FAILED_INPUTS`).
2. Parent directory of `OUTPUT_PATH` exists before the skill writes to it.
3. The output digest file was written to `OUTPUT_PATH`.
4. The output file contains all seven required sections, in order: Identity, Scope, Document Kit Summary, Dependencies, References, Semantic, Quality Observations.
5. No files in `DELIVERABLE_PATH` were written or modified.
6. No files outside `DELIVERABLE_PATH` were read.

## Structural invariants (all required)

| Check | Requirement |
|---|---|
| Seven sections present | Identity, Scope, Document Kit Summary, Dependencies, References, Semantic, Quality Observations — all present in order |
| Identity sourced | Package, Discipline, Type, Responsible values come from `_CONTEXT.md` (or marked `not present`) |
| Scope sourced | Description, Acceptance Criteria, SOW IDs, OBJ IDs come from `_CONTEXT.md` (or marked `not present`) |
| Dependency counts stated | Upstream count and downstream count present as integers |
| Key dependencies named | Top 3-5 upstream and downstream names listed, or explicitly marked empty |
| References enumerated | Every reference in `_REFERENCES.md` appears in the References section (or absence reported) |
| Semantic flagged | `_SEMANTIC.md present: YES/NO` present; framework type if identifiable |

A run missing any of the seven sections is invalid.

## Source traceability (required)

Every claim in the digest must trace to the read source:

- Identity fields appear in `_CONTEXT.md`
- Document Kit summaries reflect content from the first 80 lines of each kit file
- Dependency metadata appears in `_DEPENDENCIES.md`
- References appear in `_REFERENCES.md`
- Semantic framework claims appear in `_SEMANTIC.md` (first 40 lines)

A digest that contains invented content is invalid.

## No-invention rule

- Missing information MUST be noted as `not present` or `TBD in source`.
- Do not speculate about the deliverable's intent.
- Do not fill gaps from general knowledge.
- Do not infer SOW/OBJ IDs — list only what `_CONTEXT.md` states.

## Quality Observations specificity

Items in the Quality Observations section must be specific:

- TBD items: quote the TBD text or its location
- ASSUMPTION labels: name the assumption
- Placeholders: identify the document and section
- Conflict Table entries: cite the entry ID or row
- Enrichment markers: cite the marker code (e.g., `A-001`)
- Inconsistencies: name both documents and the specific discrepancy

Vague judgments like "documents seem thin" or "appears incomplete" are invalid. If a deliverable has no quality flags, state `No quality observations recorded.` explicitly.

## Evaluative judgment boundary (must NOT be present)

The digest must NOT contain:

- Engineering correctness assessments
- Dimension scoring or rating
- Cross-deliverable comparisons
- Recommendations for remediation
- Evaluative language about the deliverable's fitness

Those belong to EVALUATION_REPORT, not content-digest.

## Failure reporting

- If `_CONTEXT.md` is missing: report in `FAILED_INPUTS` — the skill cannot operate without it
- If `DELIVERABLE_PATH` is not a directory: report `FAILED_INPUTS`
- If parent of `OUTPUT_PATH` does not exist: report `FAILED_INPUTS`
- If a kit document is missing: note `not present` in the corresponding Document Kit entry, do not fail
- If `_SEMANTIC.md` is missing: note `_SEMANTIC.md present: NO`, do not fail

## Success case

A clean run reports:

- `RUN_STATUS=OK`
- Output file path
- List of files read (with note on which were absent)
- Count of quality observations recorded (integer)
- No warnings (or explicit statement that none were encountered)
