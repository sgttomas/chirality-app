# DX return — DEL-04-03 Content-bound decisions and compact run records

- Node DX (Type 2 TASK, Claude Code subagent launched by the run coordinator; no descendants). Basis commit 1efd4bcda.
- Method: `workflows/dependency-extract/WORKFLOW.md`. MODE UPDATE, STRICTNESS CONSERVATIVE. SOURCE_DOCS `ScopeOfWork.md` only. DECOMPOSITION_PATH `execution/_Decomposition/SOFTWARE_DECOMP.md`.
- Source `ScopeOfWork.md` SHA256 `ceecddbb67a86f744b413bb08b08c27017a82ebee8500f7600faf8d880fbaa47` (unchanged since SCA-V4-001, commit 340ecf341; not revised by SCA-V4-002). It was not changed.
- Outputs (SHA256):
  - `Dependencies.csv` `f40bc8889830c6f67b048851ecf4b6e0425f9db154b8756d48a85c9130ce70cf`.
  - `_DEPENDENCIES.md` `d1235d024947b801c4c8045cadaac5d9d9ca95c4c89202f4430ea9841be71c64`.
  - Run record `_run_records/dependency-extract-20260929-sca002.md` `4fc87d0ece413c9022701954ebeda618c6e46433eb048f957db17cd3ee229bff`.

## Register result

The register holds 33 ACTIVE rows (10 ANCHOR, 23 EXECUTION) and 0 RETIRED, as before the run.

| Change | Rows | What changed |
|---|---|---|
| added | none | |
| re-quoted (ASC-ISS-008) | DEP-04-03-019, -021, -022, -023, -024, -025, -026, -027, -028, -029, -030, -031, -032 | EvidenceQuote now carries the SoW's inline-code backticks (for example `` from App `DEL-04-01`, ``; `` (`DEL-09-06`, `DEL-09-09`) ``; `` `DEL-05-01` (`APP-V4-SWBPIPE-INTAKE-20260928-DECISION-5`) ``). Notes record the re-quote |
| updated | none other | |
| refreshed | 20 other rows | LastSeen only |
| retired | none | |

All 13 listed by V12 F1 for this register (019, 021–032) are done; all 33 ACTIVE quotes are now exact substrings of the SoW. Declared mirrors: 0. The human-owned prefix is byte-identical.

## Validators

- `validate_dependencies_schema.py`: VALID (29 columns, 33 rows).
- `validate_enum.py`: 22 invocations, all PASS.
- `validate_id_format.sh`: 62 invocations, all PASS.
- Local checks: PASS (including verbatim-quote check on every ACTIVE row). Warnings: none.

## Comparison with ARC_EFFECT

- ARC_EFFECT §4: DEL-04-03 re-quoted exactly, "Their arcs do not change". Produced: 13 re-quotes, no arc change. Expected but missing: none. Produced but unexpected: none.

## Guards

- **N-12 (DEL-03-02 → DEL-04-03) and N-B8 (DEL-03-03 → DEL-04-03) stay absent:** no DOWNSTREAM row to DEL-03-02 or DEL-03-03 (the rows to them, 024 and 026, are UPSTREAM: DEL-04-03 consuming). 
- **DEL-09-06:** the only row is DOWNSTREAM DEP-04-03-031 (DEL-09-06 consumes this record contract; N-08, allowed by the integrator ruling); no UPSTREAM row to DEL-09-06, so no SCC-002 member depends on DEL-09-06 here.
- **DEL-04-01:** the row (021) is UPSTREAM; no DOWNSTREAM row to DEL-04-01, so DEL-04-01 gains no supplier. Not triggered.
