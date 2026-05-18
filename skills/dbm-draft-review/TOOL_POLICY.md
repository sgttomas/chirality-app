# TOOL POLICY - dbm-draft-review

## Preferred tool order

1. Run `tools/review/scan_section_coverage.py` — structural coverage substrate.
2. Run `tools/review/extract_claims.py` — value/parameter/term extraction substrate.
3. Run `tools/review/scan_tbd_markers.py` — TBD/TBC/ASSUMPTION marker substrate.
4. Run `tools/review/check_body_thinness.py` — body underdevelopment signal substrate.
5. Read substrate outputs and draft sections alongside mapped KA artifacts for agent judgment.
6. Emit the 6 evidence bundle files.

## Allowed deterministic tools

### TASK-enforced

- `python3 tools/review/scan_section_coverage.py:*`
- `python3 tools/review/extract_claims.py:*`
- `python3 tools/review/scan_tbd_markers.py:*`
- `python3 tools/review/check_body_thinness.py:*`

### Operationally invoked

- `tools/review/scan_section_coverage.py` — compare draft section headings against Publication_Schema.md section table, optionally enriched by Section_Map.csv.
- `tools/review/extract_claims.py` — locate engineering values, design parameters, configuration statements, and controlled terms in draft text.
- `tools/review/scan_tbd_markers.py` — locate TBD/TBC/ASSUMPTION markers with line numbers and optional KB cross-reference.
- `tools/review/check_body_thinness.py` — compute section body underdevelopment signals (line counts, density ratios, table presence).

## Expected use of reasoning

- **Governed-truth comparison:** Read mapped KA artifacts (from Section_Map.csv, PRIMARY role) alongside draft sections. Judge whether governed design-basis content is materially represented — configurations, operating modes, interfaces, design parameters, tables.
- **Supersession compliance:** When Supersession_Map.csv is provided, verify draft uses current design-basis values, not superseded source wording.
- **Materiality judgment:** Decide which substrate signals represent material engineering concerns versus harmless formatting variations. A tool can extract "2 x 100%" from the draft; the agent decides whether it matches the governed "2 × 100% capacity air compressors in lead-lag operation."
- **Finding classification:** Assign the 6-type taxonomy and severity to each candidate finding. Provide rationale and evidence citations.
- **Completeness assessment:** Judge whether sections adequately represent their mapped KTY content at the level expected for a senior-engineer Design Basis Memorandum.
- **Evidence bundle assembly:** Write the Evidence_Bundle_Summary.md with narrative interpretation of substrate results and agent findings.

## Disallowed use

- No modification of the draft, knowledge base, publication artifacts, or governed pointers.
- No dispatching other agents or skills.
- No inline reimplementation of deterministic checks that belong in the tool layer (e.g., do not manually regex-scan for TBD markers when `scan_tbd_markers.py` does this).
- No reading of raw source DBM files except through structured supersession map comparisons.
- No invention of engineering facts not present in the governed knowledge base.
- No automatic readiness verdicts, PASS/FAIL judgments, or blocking decisions. Findings are candidates for human disposition.

## Write boundary

Writes are limited to the 6 evidence bundle files, all under the REVIEW_OUTPUT_DIR specified in the brief:

- `Evidence_Bundle_Summary.md`
- `Section_Coverage.csv`
- `Draft_Claims.csv`
- `Body_Thinness.csv`
- `TBD_Inventory.csv`
- `Candidate_Findings.csv`

No other file may be created, modified, or deleted.
