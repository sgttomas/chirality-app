# DX return — DEL-09-09 External control and catalog-extension trace

- Node DX (Type 2 TASK, Claude Code subagent dispatched by the HELP_HUMAN session; no descendants). Basis commit 2d5e6845c5 (SCA-V4-003 REVISE).
- Method: `workflows/dependency-extract/WORKFLOW.md`. MODE UPDATE, STRICTNESS CONSERVATIVE. SOURCE_DOCS `ScopeOfWork.md` only. DECOMPOSITION_PATH `execution/_Decomposition/SOFTWARE_DECOMP.md` (sha256 `983199cc…a70d`).
- Source `ScopeOfWork.md` SHA256 `fafd126f1743c18a3d9e79bef6023cbb94ddab0914634e052fb0114b8468786f` (revised by SCA-V4-003 G-0909-01…04 (OUT-001, OUT-003, REQ-001, AX-006)). It was not changed.
- Accepted register row: `Amendment_Actions.csv` row 20 — ScopeOfWork blocks G-0909-01..G-0909-04 (4) carrying S-0909-1 S-0909-2; register UPDATE rows R-0909-1 R-0909-2 R-0909-3.
- Outputs (SHA256):
  - `Dependencies.csv` `e439fb4c01d6cc4bb43eed680f785da4d2d9cc3600a48e7fc02683156e1ce895`.
  - `_DEPENDENCIES.md` `79e497b5a3664a8c007b570334145df9ce3d0ce003ba6ea8f94f038f5f277bcf`.
  - Run record `_run_records/dependency-extract-20261003-sca003.md` `e12ea3d17f0bb0630587569af7150acdedd96f7d4c1f1a89d5973124f94b2551`.

## Register result

The register holds 24 ACTIVE rows (6 ANCHOR, 18 EXECUTION) and 0 RETIRED. Before the run it held 24 ACTIVE rows.

| Change | Row | Class / type | Direction | Target | Evidence / what changed |
|---|---|---|---|---|---|
| updated | DEP-09-09-007 | EXECUTION / PREREQUISITE | UPSTREAM | DEL-03-01 | fields: Notes |
| updated | DEP-09-09-010 | EXECUTION / PREREQUISITE | UPSTREAM | DEL-04-01 | fields: Notes |
| updated | DEP-09-09-014 | EXECUTION / PREREQUISITE | UPSTREAM | DEP-001 | fields: Statement, Notes |
| refreshed | 21 other ACTIVE rows | | | | LastSeen only |

All ACTIVE quotes are exact substrings of the current ScopeOfWork and at most 30 words. Declared mirrors: 0. The human-owned prefix of `_DEPENDENCIES.md` is byte-identical.

## Validators

- `validate_dependencies_schema.py`: exit 0 — VALID: projects/chirality-app-v4/execution/PKG-09_Candidate examination and connected journeys/1_Working/DEL-09-09_External control and catalog-extension trace/Dependencies.csv /   Columns: 29 (29 required + 0 extension) /   Data rows: 24.
- `validate_enum.py`: 21 invocations, 21 PASS.
- `validate_id_format.sh`: 39 invocations, 39 PASS.
- Parent anchors (ACTIVE IMPLEMENTS_NODE): 1. Local checks: PASS. Warnings: none.

## Comparison with ARC_EFFECT and the accepted register

- **New arcs from this register:** none.
- **Expected and produced:** every ledger register row named in the accepted register row above, except as listed below; see Run Notes in `_DEPENDENCIES.md` for the row-by-row account.
- **Expected but missing:** none.
- **Produced but not named in the ledger (non-topological, required by the revised text):** none.

## Guards

- Guards (brief; SOW_REVISIONS_A/B "Extraction guards"; Handoff_State next-workflow row; ARC_EFFECT §3), checked graph-wide after the run: R17-10 holds (DEL-01-02 reaches only DEL-01-01, DEL-01-05, DEL-04-01; DEL-01-03 those and DEL-01-02); DEL-04-01 has no supplier; no SCC-002 member depends on DEL-09-06; N-12, N-B8, NR-03, NR-06 and NR-10 are absent; nothing names DEL-11-02.
