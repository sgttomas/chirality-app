# DX return — DEL-04-02 Visible autonomy and result standing

- Node DX (Type 2 TASK, Claude Code subagent dispatched by the HELP_HUMAN session; no descendants). Basis commit 2d5e6845c5 (SCA-V4-003 REVISE).
- Method: `workflows/dependency-extract/WORKFLOW.md`. MODE UPDATE, STRICTNESS CONSERVATIVE. SOURCE_DOCS `ScopeOfWork.md` only. DECOMPOSITION_PATH `execution/_Decomposition/SOFTWARE_DECOMP.md` (sha256 `983199cc…a70d`).
- Source `ScopeOfWork.md` SHA256 `e130ef7dc92ac865631002a9ab77fc2aedb16d6b0e0a568d7c62f8a8bb1c3fc5` (revised by SCA-V4-003 G-0402-01…02 (CLM-002, AX-006)). It was not changed.
- Accepted register row: `Amendment_Actions.csv` row 15 — ScopeOfWork blocks G-0402-01..G-0402-02 (2) carrying SC2-04-02-1; register UPDATE rows R2-04-02-a..c.
- Outputs (SHA256):
  - `Dependencies.csv` `26a1b49bf8b5c2ff546b2b28e536dd3ac7b8d5fc9899f7ef903e497fd86e6405`.
  - `_DEPENDENCIES.md` `c3882663fd64e377b550c58377732a3bea0f239e568a35ac0c61e879a7b82a0a`.
  - Run record `_run_records/dependency-extract-20261003-sca003.md` `2f0f16e599f067036646cea77db9936fda43e0856b51e0b15525ae1e2aae296b`.

## Register result

The register holds 28 ACTIVE rows (6 ANCHOR, 22 EXECUTION) and 0 RETIRED. Before the run it held 25 ACTIVE rows.

| Change | Row | Class / type | Direction | Target | Evidence / what changed |
|---|---|---|---|---|---|
| added | DEP-04-02-026 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-03-04 | "`DEL-03-04`, `DEL-09-06` and `DEL-09-09` also declare it upstream in their own registers." (12 words). EXPLICIT/HIGH |
| added | DEP-04-02-027 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-09-06 | "`DEL-03-04`, `DEL-09-06` and `DEL-09-09` also declare it upstream in their own registers." (12 words). EXPLICIT/HIGH |
| added | DEP-04-02-028 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-09-09 | "`DEL-03-04`, `DEL-09-06` and `DEL-09-09` also declare it upstream in their own registers." (12 words). EXPLICIT/HIGH |
| refreshed | 25 other ACTIVE rows | | | | LastSeen only |

All ACTIVE quotes are exact substrings of the current ScopeOfWork and at most 30 words. Declared mirrors: 0. The human-owned prefix of `_DEPENDENCIES.md` is byte-identical.

## Validators

- `validate_dependencies_schema.py`: exit 0 — VALID: projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-02_Visible autonomy and result standing/Dependencies.csv /   Columns: 29 (29 required + 0 extension) /   Data rows: 28.
- `validate_enum.py`: 22 invocations, 22 PASS.
- `validate_id_format.sh`: 45 invocations, 45 PASS.
- Parent anchors (ACTIVE IMPLEMENTS_NODE): 1. Local checks: PASS. Warnings: none.

## Comparison with ARC_EFFECT and the accepted register

- **New arcs from this register:** none.
- **Expected and produced:** every ledger register row named in the accepted register row above, except as listed below; see Run Notes in `_DEPENDENCIES.md` for the row-by-row account.
- **Expected but missing:** none.
- **Produced but not named in the ledger (non-topological, required by the revised text):** none.

## Guards

- Guards (brief; SOW_REVISIONS_A/B "Extraction guards"; Handoff_State next-workflow row; ARC_EFFECT §3), checked graph-wide after the run: R17-10 holds (DEL-01-02 reaches only DEL-01-01, DEL-01-05, DEL-04-01; DEL-01-03 those and DEL-01-02); DEL-04-01 has no supplier; no SCC-002 member depends on DEL-09-06; N-12, N-B8, NR-03, NR-06 and NR-10 are absent; nothing names DEL-11-02.
