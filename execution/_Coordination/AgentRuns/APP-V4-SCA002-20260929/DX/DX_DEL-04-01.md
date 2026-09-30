# DX return — DEL-04-01 Operation-policy and human-act distinctions

- Node DX (Type 2 TASK, Claude Code subagent launched by the run coordinator; no descendants). Basis commit 1efd4bcda.
- Method: `workflows/dependency-extract/WORKFLOW.md`. MODE UPDATE, STRICTNESS CONSERVATIVE. SOURCE_DOCS `ScopeOfWork.md` only. DECOMPOSITION_PATH `execution/_Decomposition/SOFTWARE_DECOMP.md`.
- Source `ScopeOfWork.md` SHA256 `ac043e54e396f9155e3d1b02d61ca7333350a812c7db3d5bb26c80d6fc3bb875` (unchanged since SCA-V4-001, commit 340ecf341; not revised by SCA-V4-002). It was not changed.
- Outputs (SHA256):
  - `Dependencies.csv` `d3892649dbc008d81b9a183d34c44cf68e0765d886a04dce924e69f456c5c9c1`.
  - `_DEPENDENCIES.md` `b504a28b63a3940479a636700b81428f4e107881253d133be632bd6601fe2db6`.
  - Run record `_run_records/dependency-extract-20260929-sca002.md` `7d267c8816d2d1167a98ec0f5e2cd15e61f85e9da2edb8a4564ab991accd6126`.

## Register result

The register holds 29 ACTIVE rows (11 ANCHOR, 18 EXECUTION) and 0 RETIRED, as before the run.

| Change | Rows | What changed |
|---|---|---|
| added | none | |
| re-quoted (ASC-ISS-008) | DEP-04-01-017, -018, -022, -023, -024, -025, -026, -027, -029 | EvidenceQuote now carries the SoW's inline-code backticks (for example `` App v4 `DEL-03-02`, `DEL-03-03`, … ``; `` `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2 ``). Notes record the re-quote |
| updated | none other | |
| refreshed | 20 other rows | LastSeen only |
| retired | none | |

All 9 listed by V12 F1 for this register (017, 018, 022–027, 029) are done; all 29 ACTIVE quotes are now exact substrings of the SoW. Declared mirrors: 0. The human-owned prefix is byte-identical.

## Validators

- `validate_dependencies_schema.py`: VALID (29 columns, 29 rows).
- `validate_enum.py`: 21 invocations, all PASS.
- `validate_id_format.sh`: 56 invocations, all PASS.
- Local checks: PASS (including verbatim-quote check on every ACTIVE row). Warnings: none.

## Comparison with ARC_EFFECT

- ARC_EFFECT §4: "the registers of DEL-04-01, DEL-04-02 and DEL-04-03, re-quoted exactly … Their arcs do not change. For DEL-04-01 the guard applies: the UPDATE adds no row that makes it consume anything." Produced: 9 re-quotes, no arc change. Expected but missing: none. Produced but unexpected: none.

## Guards

- **DEL-04-01 gains no supplier row from an SCC-002 member: confirmed.** After the run the register has no ACTIVE UPSTREAM row with a DELIVERABLE target at all (7 UPSTREAM rows, all EXTERNAL). DEL-04-01 keeps 0 deliverable suppliers. Its 11 DOWNSTREAM HANDOVER rows (to DEL-02-01, 02-03, 03-01, 03-02, 03-03, 03-04, 04-02, 04-03, 05-01, 05-02, 09-09) are consumers depending on DEL-04-01, unchanged. No row on DEL-09-06. Not triggered.
