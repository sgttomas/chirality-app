# DX return — DEL-03-04 Host boundary and integration guide

- Node DX (Type 2 TASK, Claude Code subagent dispatched by the HELP_HUMAN session; no descendants). Basis commit 2d5e6845c5 (SCA-V4-003 REVISE).
- Method: `workflows/dependency-extract/WORKFLOW.md`. MODE UPDATE, STRICTNESS CONSERVATIVE. SOURCE_DOCS `ScopeOfWork.md` only. DECOMPOSITION_PATH `execution/_Decomposition/SOFTWARE_DECOMP.md` (sha256 `983199cc…a70d`).
- Source `ScopeOfWork.md` SHA256 `aac10af880945a88cf514fcb07d13544800fb3785a550b1b6660062f0d65761d` (revised by SCA-V4-003 G-0304-01…04 (CLM-003, receiving-map row "Autonomy", AX-005)). It was not changed.
- Accepted register row: `Amendment_Actions.csv` row 13 — ScopeOfWork blocks G-0304-01..G-0304-04 (4) carrying S-04-1 S-04-2 S-04-3; register UPDATE rows R-04-1 R-04-2.
- Outputs (SHA256):
  - `Dependencies.csv` `1d5d7249385857afe9740fb1396e272fc21ee0133403c0cd0d50924c81b6dfc4`.
  - `_DEPENDENCIES.md` `c75ffb063258f7a155a780233000c8f011f60a41829e43dbd339831032770139`.
  - Run record `_run_records/dependency-extract-20261003-sca003.md` `da1ba36c2e3e79d8c4bd75234102559dbc70c44f9946b298a99b792849162c32`.

## Register result

The register holds 23 ACTIVE rows (4 ANCHOR, 19 EXECUTION) and 0 RETIRED. Before the run it held 23 ACTIVE rows.

| Change | Row | Class / type | Direction | Target | Evidence / what changed |
|---|---|---|---|---|---|
| updated | DEP-03-04-021 | EXECUTION / INTERFACE | UPSTREAM | DEL-01-01 | fields: Statement, SourceRef, EvidenceQuote, Notes |
| updated | DEP-03-04-022 | EXECUTION / INTERFACE | UPSTREAM | DEL-09-06 | fields: Statement, SourceRef, EvidenceQuote, Notes |
| updated | DEP-03-04-023 | EXECUTION / INTERFACE | UPSTREAM | DEL-09-09 | fields: SourceRef, EvidenceQuote, Notes |
| refreshed | 20 other ACTIVE rows | | | | LastSeen only |

All ACTIVE quotes are exact substrings of the current ScopeOfWork and at most 30 words. Declared mirrors: 0. The human-owned prefix of `_DEPENDENCIES.md` is byte-identical.

## Validators

- `validate_dependencies_schema.py`: exit 0 — VALID: projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-04_Host boundary and integration guide/Dependencies.csv /   Columns: 29 (29 required + 0 extension) /   Data rows: 23.
- `validate_enum.py`: 19 invocations, 19 PASS.
- `validate_id_format.sh`: 50 invocations, 50 PASS.
- Parent anchors (ACTIVE IMPLEMENTS_NODE): 1. Local checks: PASS. Warnings: none.

## Comparison with ARC_EFFECT and the accepted register

- **New arcs from this register:** none.
- **Expected and produced:** every ledger register row named in the accepted register row above, except as listed below; see Run Notes in `_DEPENDENCIES.md` for the row-by-row account.
- **Expected but missing:** none.
- **Produced but not named in the ledger (non-topological, required by the revised text):** DEP-03-04-023 re-quote (clause moved).

## Guards

- Guards (brief; SOW_REVISIONS_A/B "Extraction guards"; Handoff_State next-workflow row; ARC_EFFECT §3), checked graph-wide after the run: R17-10 holds (DEL-01-02 reaches only DEL-01-01, DEL-01-05, DEL-04-01; DEL-01-03 those and DEL-01-02); DEL-04-01 has no supplier; no SCC-002 member depends on DEL-09-06; N-12, N-B8, NR-03, NR-06 and NR-10 are absent; nothing names DEL-11-02.
