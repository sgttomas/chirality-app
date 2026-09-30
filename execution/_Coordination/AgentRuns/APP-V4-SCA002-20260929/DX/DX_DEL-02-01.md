# DX return — DEL-02-01 Portable workflow contract and shared allocation

- Node DX (Type 2 TASK, Claude Code subagent launched by the run coordinator; no descendants). Basis commit 1efd4bcda.
- Method: `workflows/dependency-extract/WORKFLOW.md`. MODE UPDATE, STRICTNESS CONSERVATIVE. SOURCE_DOCS `ScopeOfWork.md` only. DECOMPOSITION_PATH `execution/_Decomposition/SOFTWARE_DECOMP.md`.
- Source `ScopeOfWork.md` SHA256 `ef360edf28f5f463ae961495e04e566ab9ec9d56c0a4fd4f35e67b87adb82f17` (revised by SCA-V4-002 F-0201-01/F-0201-02). It was not changed.
- Outputs (SHA256):
  - `Dependencies.csv` `d3946a9e0c2bd7b37cb18355abc3b2a2f563ef0b886b500162b550d6ac1db10a`.
  - `_DEPENDENCIES.md` `983396d0744698cbc6c639c47e1d3d0ba0da837ff15ec7d51aae6d5dab5bf4dc`.
  - Run record `_run_records/dependency-extract-20260929-sca002.md` `eaa508e255133208a5f771780e691a4f45b074fe45f201f7b0411c72bf0f9e78`.

## Register result

The register holds 29 ACTIVE rows (16 ANCHOR, 13 EXECUTION) and 0 RETIRED. Before the run it held 28 ACTIVE rows.

| Change | Row | Class / type | Direction | Target | Evidence |
|---|---|---|---|---|---|
| added | DEP-02-01-029 | EXECUTION / INTERFACE | UPSTREAM | DEL-03-02 | CLM-002 "Checkpoint subject binding and item-level decisions consume `DEL-03-02`'s change-item content identities, per-item dispositions, all-items-decided indication, item-left events and applied-outcome object identities; this contract does not define them." (27 words, verbatim). EXPLICIT/HIGH |
| updated | none | | | | |
| refreshed | 28 other rows | 16 ANCHOR, 12 EXECUTION | — | — | LastSeen only |
| retired | none | | | | |

Declared mirrors: 0. Two "None declared" placeholders were skipped. The human-owned prefix is byte-identical.

## Validators

- `validate_dependencies_schema.py`: VALID (29 columns, 29 rows).
- `validate_enum.py`: 23 invocations, all PASS.
- `validate_id_format.sh`: 59 invocations, all PASS.
- Local checks: PASS (unique IDs, DEP prefix, one parent anchor, verbatim quotes of at most 30 words, target placement, no duplicate typed-target keys, ID resolution in the current companion CSVs).
- Warnings: none.

## Comparison with ARC_EFFECT

- **Expected and produced:** N-18 DEL-02-01 → DEL-03-02, as DEP-02-01-029 (1 UPSTREAM INTERFACE row; ARC_EFFECT §4 expected "DEL-02-01: 1"). The reverse row DEP-03-02-027 (N-B3) already exists, so N-18 now forms a reciprocal pair inside SCC-002, as ARC_EFFECT §3 predicts.
- **Expected but missing:** none.
- **Produced but unexpected:** none. No other arc changed.

## Guards

- No row on DEL-09-06 in either direction. N-12 (DEL-03-02 → DEL-04-03) and N-B8 (DEL-03-03 → DEL-04-03) do not involve this register. DEL-02-01 has no DOWNSTREAM row to DEL-04-01, so DEL-04-01 gains no supplier here. Not triggered.
