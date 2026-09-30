# DX return — DEL-01-01 Stock Codex hosting and supplier contract

- Node DX (Type 2 TASK, Claude Code subagent launched by the run coordinator; no descendants). Basis commit 1efd4bcda.
- Method: `workflows/dependency-extract/WORKFLOW.md`. MODE UPDATE, STRICTNESS CONSERVATIVE. SOURCE_DOCS `ScopeOfWork.md` only. DECOMPOSITION_PATH `execution/_Decomposition/SOFTWARE_DECOMP.md`.
- Source `ScopeOfWork.md` SHA256 `9945e72b04b4f45c4c641a5248cca8bc2ac40bf4897d1018c5ab59eba307cc75` (revised by SCA-V4-002 F-0101-01/F-0101-02, Q-6 accepted). It was not changed.
- Outputs (SHA256):
  - `Dependencies.csv` `9fdb3ce3d8c180f58bf64d9fcf3476e3835dd6c8641bf4f4f203bc10f1f13d08`.
  - `_DEPENDENCIES.md` `e0d6d2c711befb59d5b8985fda08ed4b2fe59fc1f2bd44657271554f70c9779a`.
  - Run record `_run_records/dependency-extract-20260929-sca002.md` `2b4fe5147226e0fb11ef05b65fefbb329b0f626d63fb70f5175c0afa1f7a87d3`.

## Register result

The register holds 24 ACTIVE rows (15 ANCHOR, 9 EXECUTION) and 0 RETIRED, as before the run.

| Change | Row | Class / type | Direction | Target | What changed |
|---|---|---|---|---|---|
| added | none | | | | |
| updated | DEP-01-01-017 | EXECUTION / CONSTRAINT | UPSTREAM | EXTERNAL OI-012 | SourceRef/Notes: the revised [N] source line now agrees with CLM-003/REQ-006/TBD-002 (0.158.0 definition/generation pin, D4; no implementation/qualification version or environment) |
| updated | DEP-01-01-018 | EXECUTION / PREREQUISITE | UPSTREAM | EXTERNAL DEP-005 | SourceRef/Notes: same [N] line |
| refreshed | 22 other rows | | | | LastSeen only |
| retired | none | | | | |

All 24 quotes remain verbatim. Declared mirrors: 0. The human-owned prefix is byte-identical.

## Validators

- `validate_dependencies_schema.py`: VALID (29 columns, 24 rows).
- `validate_enum.py`: 22 invocations, all PASS.
- `validate_id_format.sh`: 45 invocations, all PASS.
- Local checks: PASS. Warnings: none.

## Comparison with ARC_EFFECT

- ARC_EFFECT §4 lists DEL-01-01 under "Changed bound files, no arc change (evidence drift only)" if Q-6 is accepted. Produced: no arc change. Expected but missing: none. Produced but unexpected: none.

## Guards

- DEL-01-01 is not an SCC-002 member (it is in {01-01, 01-05}). No row on DEL-09-06; no DOWNSTREAM row to DEL-04-01; N-12/N-B8 not involved. Not triggered.
