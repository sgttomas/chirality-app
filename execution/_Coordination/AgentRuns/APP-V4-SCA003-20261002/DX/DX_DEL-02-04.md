# DX return — DEL-02-04 Additive role selection and supply

- Node DX (Type 2 TASK, Claude Code subagent dispatched by the HELP_HUMAN session; no descendants). Basis commit 2d5e6845c5 (SCA-V4-003 REVISE).
- Method: `workflows/dependency-extract/WORKFLOW.md`. MODE UPDATE, STRICTNESS CONSERVATIVE. SOURCE_DOCS `ScopeOfWork.md` only. DECOMPOSITION_PATH `execution/_Decomposition/SOFTWARE_DECOMP.md` (sha256 `983199cc…a70d`).
- Source `ScopeOfWork.md` SHA256 `2327508f2290e7cf2528950d65bc331d72a80d8413a13fe31ea8f867cce4d176` (revised by SCA-V4-003 G-0204-01…13 (CLM-002, REQ-001/002/003, AC-001, AC-003, open-matter rows, TBD-001, AX-005)). It was not changed.
- Accepted register row: `Amendment_Actions.csv` row 9 — ScopeOfWork blocks G-0204-01..G-0204-13 (13) carrying SC3-02-04-1 SC3-02-04-2 SC3-02-04-4 SC3-02-04-5 SC3-02-04-6 SC3-02-04-7 SC3-02-04-9; register UPDATE rows SC3-02-04-8 R3-02-04-a..b R3-02-04-c R3-02-04-d.
- Outputs (SHA256):
  - `Dependencies.csv` `fe350addbe9664a37752120841e5289df58d5b724b38338c22405ccde87c8450`.
  - `_DEPENDENCIES.md` `97c1fc1f1ed9517aa03f9f798519f3252c9eede485f2c3c71af9f1e4467509c1`.
  - Run record `_run_records/dependency-extract-20261003-sca003.md` `7f09f3ad99d346d49a73b68fcab749e8f7170f9880aba3223e1c529dff52f3cf`.

## Register result

The register holds 19 ACTIVE rows (9 ANCHOR, 10 EXECUTION) and 0 RETIRED. Before the run it held 16 ACTIVE rows.

| Change | Row | Class / type | Direction | Target | Evidence / what changed |
|---|---|---|---|---|---|
| updated | DEP-02-04-010 | EXECUTION / INTERFACE | UPSTREAM | DEL-01-01 | fields: Statement, SourceRef, Notes |
| updated | DEP-02-04-016 | EXECUTION / CONSTRAINT | UPSTREAM | OI-018 | fields: Notes |
| added | DEP-02-04-017 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-03-04 | "Its role-guidance semantics are received by `DEL-03-04`, its supply obligations by `DEL-10-03`," (12 words). EXPLICIT/HIGH |
| added | DEP-02-04-018 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-10-03 | "Its role-guidance semantics are received by `DEL-03-04`, its supply obligations by `DEL-10-03`," (12 words). EXPLICIT/HIGH |
| added | DEP-02-04-019 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-01-04 | "its role list and guidance-changed signal by `DEL-01-04`, each of which declares it upstream in its own register." (18 words). EXPLICIT/HIGH |
| refreshed | 14 other ACTIVE rows | | | | LastSeen only |

All ACTIVE quotes are exact substrings of the current ScopeOfWork and at most 30 words. Declared mirrors: 0. The human-owned prefix of `_DEPENDENCIES.md` is byte-identical.

## Validators

- `validate_dependencies_schema.py`: exit 0 — VALID: projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-04_Additive role selection and supply/Dependencies.csv /   Columns: 29 (29 required + 0 extension) /   Data rows: 19.
- `validate_enum.py`: 22 invocations, 22 PASS.
- `validate_id_format.sh`: 33 invocations, 33 PASS.
- Parent anchors (ACTIVE IMPLEMENTS_NODE): 1. Local checks: PASS. Warnings: none.

## Comparison with ARC_EFFECT and the accepted register

- **New arcs from this register:** none.
- **Expected and produced:** every ledger register row named in the accepted register row above, except as listed below; see Run Notes in `_DEPENDENCIES.md` for the row-by-row account.
- **Expected but missing:** none.
- **Produced but not named in the ledger (non-topological, required by the revised text):** none.

## Guards

- Guards (brief; SOW_REVISIONS_A/B "Extraction guards"; Handoff_State next-workflow row; ARC_EFFECT §3), checked graph-wide after the run: R17-10 holds (DEL-01-02 reaches only DEL-01-01, DEL-01-05, DEL-04-01; DEL-01-03 those and DEL-01-02); DEL-04-01 has no supplier; no SCC-002 member depends on DEL-09-06; N-12, N-B8, NR-03, NR-06 and NR-10 are absent; nothing names DEL-11-02.
