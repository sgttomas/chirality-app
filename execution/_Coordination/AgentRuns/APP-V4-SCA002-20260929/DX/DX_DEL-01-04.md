# DX return — DEL-01-04 Native requests, outcomes and attachments

- Node DX (Type 2 TASK, Claude Code subagent launched by the run coordinator; no descendants). Basis commit 1efd4bcda.
- Method: `workflows/dependency-extract/WORKFLOW.md`. MODE UPDATE, STRICTNESS CONSERVATIVE. SOURCE_DOCS `ScopeOfWork.md` only. DECOMPOSITION_PATH `execution/_Decomposition/SOFTWARE_DECOMP.md`.
- Source `ScopeOfWork.md` SHA256 `0cdb44e297010b70deb479ab647a165023846aa0943c3f9fc200407c708469cd` (revised by SCA-V4-002 F-0104-01…06). It was not changed.
- Outputs (SHA256):
  - `Dependencies.csv` `20ce3808597bf2833bba6c488ae3770c3b93260d4be229b6f89cedecdb0d5eaa`.
  - `_DEPENDENCIES.md` `18cbcd7342c3f06c855be298db4a6b0619220fa0f42b12aff71ed952477d7250`.
  - Run record `_run_records/dependency-extract-20260929-sca002.md` `d2babb8cc9b13c1652aa7b65822b3e2fc35a75546345e75c895ef64c44cf2e1d`.

## Register result

The register holds 18 ACTIVE rows (6 ANCHOR, 12 EXECUTION) and 1 RETIRED. Before the run it held 19 ACTIVE rows.

| Change | Row | Class / type | Direction | Target | What changed |
|---|---|---|---|---|---|
| added | none | | | | |
| updated (re-quoted) | DEP-01-04-013 | EXECUTION / CONSTRAINT | UPSTREAM | EXTERNAL OI-001 | Revised TBD-001: OI-001 ruled by D2; the row is narrowed to "Any matter the ruling does not cover stays with the **Owner with App/SWB contract owners**, point of need **Before operation-policy production contracts**." OI-021 additions carried in Statement/Notes (no owner or point of need for OI-021 in this SoW) |
| updated (re-quoted) | DEP-01-04-016 | EXECUTION / CONSTRAINT | UPSTREAM | EXTERNAL OI-012 | Revised TBD-004: 0.158.0 selected by D4; the row is narrowed to the implementation/qualification pin ("Remaining under OI-012, with the **App implementation owner**: … point of need **Before protocol generation and qualification**") |
| updated | DEP-01-04-011 | EXECUTION / INTERFACE | UPSTREAM | DEL-04-01 | SourceRef/Notes for revised CLM-005/VER-005 (rulings D2/D3 carried through the PKG-04 interface); named as successor of the retired OI-002 row |
| updated | DEP-01-04-018 | EXECUTION / PREREQUISITE | UPSTREAM | EXTERNAL DEP-005 | Notes only (quote unchanged) |
| retired | DEP-01-04-014 | EXECUTION / CONSTRAINT | UPSTREAM | EXTERNAL OI-002 | `retired_by=source_revised`: TBD-002 records OI-002 as ruled by D3 with no residual open part; successor DEP-01-04-011 (adopted result via DEL-04-01). Same treatment as DEP-02-03-016 under SCA-V4-001 |
| refreshed | 14 other rows | | | | LastSeen only |

IMPACT §5 expected exactly rows 013 (OI-001), 014 (OI-002) and 016 (OI-012) to lose their quote: 013 and 016 were re-quoted, 014 was retired `source_revised` with the successor named. No new EXTERNAL OI-021 row (see Run Notes). All 18 ACTIVE quotes are verbatim. Declared mirrors: 0. The human-owned prefix is byte-identical.

## Validators

- `validate_dependencies_schema.py`: VALID (29 columns, 19 rows).
- `validate_enum.py`: 23 invocations, all PASS.
- `validate_id_format.sh`: 33 invocations, all PASS.
- Local checks: PASS. Warnings: none.

## Comparison with ARC_EFFECT

- ARC_EFFECT §4: DEL-01-04 is DAG-pending as the supplier endpoint of X-1 (row in DEL-02-03: DEP-02-03-027) and "changes bytes for its text edits". All five affected rows here are EXTERNAL CONSTRAINT/PREREQUISITE or the existing DEL-04-01 interface, so no arc changes, as IMPACT §5 predicts. Expected and produced: no arc change here. Expected but missing: none. Produced but unexpected: none.

## Guards

- No row on DEL-09-06. No DOWNSTREAM row to DEL-04-01 (the DEL-04-01 row is UPSTREAM, DEL-01-04 consuming; existing arc). N-12/N-B8 not involved. Not triggered.
