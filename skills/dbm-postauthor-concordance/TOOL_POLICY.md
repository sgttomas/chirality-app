# TOOL POLICY - dbm-postauthor-concordance

## Preferred tool order

1. Run `tools/review/scan_section_coverage.py` with `--section-map` (required in pipeline mode).
2. Run `tools/review/extract_claims.py` — value/parameter/term extraction.
3. Run `tools/review/scan_tbd_markers.py` — TBD/TBC/ASSUMPTION marker scan with KB cross-ref.
4. Run `tools/review/check_body_thinness.py` with `--section-map` and `--schema`.
5. Read substrate outputs and authored sections alongside mapped KA artifacts for agent judgment.
6. Emit the 7 output files (6 evidence bundle + disposition artifact).

## Allowed deterministic tools

### TASK-enforced

- `python3 tools/review/scan_section_coverage.py:*`
- `python3 tools/review/extract_claims.py:*`
- `python3 tools/review/scan_tbd_markers.py:*`
- `python3 tools/review/check_body_thinness.py:*`

### Operationally invoked

- `tools/review/scan_section_coverage.py` — compare authored section headings against Publication_Schema.md, enriched by Section_Map.csv (run-specific authority).
- `tools/review/extract_claims.py` — locate engineering values, parameters, configuration statements, and controlled terms in authored text.
- `tools/review/scan_tbd_markers.py` — locate TBD/TBC/ASSUMPTION markers with KB cross-reference via Section_Map.csv Scoping.md discovery.
- `tools/review/check_body_thinness.py` — compute section body underdevelopment signals with mapped-artifact density ratios.

## Expected use of reasoning

- **Governed-truth comparison:** Read mapped KA artifacts (PRIMARY role) alongside authored sections. Judge whether governed design-basis content is materially represented.
- **Supersession compliance:** Verify authored content uses current values when Supersession_Map.csv is provided.
- **Materiality judgment:** Distinguish material engineering concerns from formatting variations.
- **Finding classification:** Assign 6-type taxonomy and severity. Cite governed evidence and trace to substrate.
- **Completeness assessment:** Judge section adequacy at the level expected for a senior-engineer Design Basis Memorandum.
- **Disposition preparation:** Write `Publication_Review_Disposition.csv` with agent-proposed dispositions and `HumanDisposition = TBD`.
- **Section QA cross-reference:** When SECTIONS_ROOT is available, cross-reference section-level QA artifacts from `dbm-section-publish` for additional context.

## Disallowed use

- No modification of section outputs, knowledge base, publication artifacts, or governed pointers.
- No dispatching other agents or skills.
- No inline reimplementation of deterministic checks that belong in the tool layer.
- No reading of raw source DBM files except through structured supersession map comparisons.
- No invention of engineering facts not present in the governed knowledge base.
- No automatic readiness verdicts, PASS/FAIL judgments, or blocking decisions.
- No pre-filling of `HumanDisposition` values — all rows emit as `TBD`.

## Write boundary

Writes are limited to the 7 output files, all under the REVIEW_OUTPUT_DIR specified in the brief:

- `Evidence_Bundle_Summary.md`
- `Section_Coverage.csv`
- `Draft_Claims.csv`
- `Body_Thinness.csv`
- `TBD_Inventory.csv`
- `Candidate_Findings.csv`
- `Publication_Review_Disposition.csv`

No other file may be created, modified, or deleted.
