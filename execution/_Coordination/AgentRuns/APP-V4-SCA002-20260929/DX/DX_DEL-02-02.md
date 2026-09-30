# DX return — DEL-02-02 Workflow-making workspace and registration

- Node DX (Type 2 TASK, Claude Code subagent launched by the run coordinator; no descendants). Basis commit 1efd4bcda.
- Method: `workflows/dependency-extract/WORKFLOW.md`. MODE UPDATE, STRICTNESS CONSERVATIVE. SOURCE_DOCS `ScopeOfWork.md` only. DECOMPOSITION_PATH `execution/_Decomposition/SOFTWARE_DECOMP.md`.
- Source `ScopeOfWork.md` SHA256 `5814116909db8120c1fe888ba021ca60ad139ea0b36cc89fe7e93ed00235924a` (revised by SCA-V4-002 F-0202-01/02/03). It was not changed.
- Outputs (SHA256):
  - `Dependencies.csv` `be14a079c872695ee6720c75bfe96b91dbac6ad4c228fb577ee044f1e32f7e0a`.
  - `_DEPENDENCIES.md` `379ef690d62b11ba4836e33434f6804d0026cbb4068bc6cdbafc8fd33373c624`.
  - Run record `_run_records/dependency-extract-20260929-sca002.md` `5ab464ca0c32b7724988d0739abf781edb359e47549e23334e4ab90490524677`.

## Register result

The register holds 18 ACTIVE rows (11 ANCHOR, 7 EXECUTION) and 1 RETIRED (019, unchanged), as before the run.

| Change | Row | Class / type | Direction | Target | What changed |
|---|---|---|---|---|---|
| added | none | | | | |
| updated | DEP-02-02-016 | EXECUTION / INTERFACE | UPSTREAM | DEL-04-01 | Notes only: revised TBD-001 records the D2/D3 rulings, residual broader decisions with the owner and affected App/SWB contract owners, OI-021 additions. Quote unchanged |
| refreshed | 17 other ACTIVE rows | | | | LastSeen only |
| retired | none this run | | | | |

This register carries no EXTERNAL OI rows (prior-run reading: points of need, not inputs), so the TBD-001/TBD-002 revisions change no quote. All 18 ACTIVE quotes are verbatim. Declared mirrors: 0. The human-owned prefix is byte-identical.

## Validators

- `validate_dependencies_schema.py`: VALID (29 columns, 19 rows).
- `validate_enum.py`: 22 invocations, all PASS.
- `validate_id_format.sh`: 41 invocations, all PASS.
- Local checks: PASS. Warnings: none.

## Comparison with ARC_EFFECT

- ARC_EFFECT §4 lists DEL-02-02 under "Changed bound files, no arc change (evidence drift only)". Produced: no arc change. Expected but missing: none. Produced but unexpected: none.

## Guards

- No row on DEL-09-06; no DOWNSTREAM row to DEL-04-01; N-12/N-B8 not involved. Not triggered.
