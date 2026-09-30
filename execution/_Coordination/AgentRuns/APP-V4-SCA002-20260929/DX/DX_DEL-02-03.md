# DX return — DEL-02-03 Workflow execution compatibility and round-trip support

- Node DX (Type 2 TASK, Claude Code subagent launched by the run coordinator; no descendants). Basis commit 1efd4bcda.
- Method: `workflows/dependency-extract/WORKFLOW.md`. MODE UPDATE, STRICTNESS CONSERVATIVE. SOURCE_DOCS `ScopeOfWork.md` only. DECOMPOSITION_PATH `execution/_Decomposition/SOFTWARE_DECOMP.md`.
- Source `ScopeOfWork.md` SHA256 `0006521b9bd96ea7ec98ecc5d9e6db794ecb331440c276006b444e7ee319726d` (revised by SCA-V4-002 F-0203-01/F-0203-02). It was not changed.
- Outputs (SHA256):
  - `Dependencies.csv` `f1a81f854d5923dd450a6eb709bfc623b3f778651787e6f4a09d0d48d5110f7e`.
  - `_DEPENDENCIES.md` `84dd2315380cbb117e386dc9f64aeb354df5cfc0ffab3bbf20038f39ddd2d422`.
  - Run record `_run_records/dependency-extract-20260929-sca002.md` `3f15850da5331df3dfa25a41d935585b2c49ab2cbc64a2383de313e9c3f5bfe3`.

## Register result

The register holds 25 ACTIVE rows (8 ANCHOR, 17 EXECUTION) and 2 RETIRED (015, 016, unchanged from SCA-V4-001). Before the run it held 22 ACTIVE rows.

| Change | Row | Class / type | Direction | Target | Evidence |
|---|---|---|---|---|---|
| added | DEP-02-03-025 | EXECUTION / INTERFACE | UPSTREAM | DEL-03-02 | CLM-002 "This slice consumes, and does not define: `DEL-03-02`'s per-item dispositions, item-left events, all-items-decided indication, change-item content identities and applied outcomes with their resulting objects," (24 words, verbatim). EXPLICIT/HIGH |
| added | DEP-02-03-026 | EXECUTION / INTERFACE | UPSTREAM | DEL-03-03 | CLM-002 "`DEL-03-03`'s observations of checkpoint arrivals and act records on the external channel, which this slice records (REQ-002, REQ-003);" (18 words). EXPLICIT/HIGH |
| added | DEP-02-03-027 | EXECUTION / INTERFACE | UPSTREAM | DEL-01-04 | CLM-002 "`DEL-01-04`'s App act control and person identity, for the App-side positive capture fixtures (OUT-003, VER-003), which await that later undertaking." (21 words). EXPLICIT/HIGH; Notes record the narrow scope (fixtures only) |
| updated | none | | | | |
| refreshed | 22 other ACTIVE rows | 8 ANCHOR, 14 EXECUTION | — | — | LastSeen only |
| retired | none this run | | | | |

Declared mirrors: 0. Two "None declared" placeholders were skipped. The human-owned prefix is byte-identical.

## Validators

- `validate_dependencies_schema.py`: VALID (29 columns, 27 rows).
- `validate_enum.py`: 25 invocations, all PASS.
- `validate_id_format.sh`: 52 invocations, all PASS.
- Local checks: PASS (unique IDs, DEP prefix, one parent anchor, verbatim quotes of at most 30 words, target placement, no duplicate typed-target keys, ID resolution in the current companion CSVs).
- Warnings: none.

## Comparison with ARC_EFFECT

- **Expected and produced:** N-21 DEL-02-03 → DEL-03-02 (DEP-02-03-025); N-24 DEL-02-03 → DEL-03-03 (DEP-02-03-026), which pairs with the existing DEP-03-03-014 (N-27) as ARC_EFFECT §3 predicts; X-1 DEL-02-03 → DEL-01-04 (DEP-02-03-027). ARC_EFFECT §4 expected "DEL-02-03: 3" UPSTREAM INTERFACE rows; exactly 3 were produced, one per arc (no split).
- **Expected but missing:** none.
- **Produced but unexpected:** none. No other arc changed. All three arcs have both ends in SCC-002.

## Guards

- No row on DEL-09-06 gained; the existing DOWNSTREAM HANDOVER DEP-02-03-014 to DEL-09-06 is DEL-09-06 consuming an SCC-002 member (N-19, allowed by the integrator ruling); DEL-02-03 does not depend on DEL-09-06. N-12 and N-B8 do not involve this register. No DOWNSTREAM row to DEL-04-01. Not triggered.
- The sentence names no DEL-04-01 or DEL-09-06 input, as SOW_REVISIONS "Extraction guards" states.
