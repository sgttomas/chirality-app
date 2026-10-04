# DX return — DEL-01-05 Native OAuth/sign-in, API-key and local-provider access

- Node DX (Type 2 TASK, Claude Code subagent dispatched by the HELP_HUMAN session; no descendants). Basis commit 2d5e6845c5 (SCA-V4-003 REVISE).
- Method: `workflows/dependency-extract/WORKFLOW.md`. MODE UPDATE, STRICTNESS CONSERVATIVE. SOURCE_DOCS `ScopeOfWork.md` only. DECOMPOSITION_PATH `execution/_Decomposition/SOFTWARE_DECOMP.md` (sha256 `983199cc…a70d`).
- Source `ScopeOfWork.md` SHA256 `2e134b572f2676ed4fe6daa892047e21e53a637f9901cba20f482a6637f7f3d3` (revised by SCA-V4-003 G-0105-01…16 (11 definitions; added REQ-010, AC-011, VER-011, matrix row, AX-006)). It was not changed.
- Accepted register row: `Amendment_Actions.csv` row 5 — ScopeOfWork blocks G-0105-01..G-0105-16 (16) carrying SC3-01-05-1 SC3-01-05-2 SC3-01-05-3 SC3-01-05-4 SC3-01-05-5 SC3-01-05-6 SC3-01-05-7 SC3-01-05-10 SC3-01-05-12 SC3-01-05-13; register UPDATE rows R3-01-05-a R3-01-05-b R3-01-05-c R3-01-05-d R3-01-05-e.
- Outputs (SHA256):
  - `Dependencies.csv` `7100a2e6fefa0879734d2461e9eceb1d2e86b9621a9b240c0ac7783ddc35bbca`.
  - `_DEPENDENCIES.md` `7fab9eef1d2fcc53c1f555880dbed9805990247e16ed41b4610ec12faff32b03`.
  - Run record `_run_records/dependency-extract-20261003-sca003.md` `77e02f53ae31e2b2b539dada12400d7130116533a206db5c12a9c2aaac973a78`.

## Register result

The register holds 17 ACTIVE rows (11 ANCHOR, 6 EXECUTION) and 0 RETIRED. Before the run it held 16 ACTIVE rows.

| Change | Row | Class / type | Direction | Target | Evidence / what changed |
|---|---|---|---|---|---|
| updated | DEP-01-05-012 | EXECUTION / PREREQUISITE | UPSTREAM | DEL-01-01 | fields: Notes |
| updated | DEP-01-05-015 | EXECUTION / CONSTRAINT | UPSTREAM | OI-009 | fields: TargetName, TargetLocation, Statement, SourceRef, EvidenceQuote, Notes |
| updated | DEP-01-05-016 | EXECUTION / CONSTRAINT | UPSTREAM | OI-010 | fields: TargetLocation, SourceRef, Notes |
| added | DEP-01-05-017 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-09-02 | "`DEL-09-02` receives the account/provider inputs and the focused sign-in and concurrent-mode checks for V4-EXM-12 and declares them upstream in its own register." (22 words). EXPLICIT/HIGH |
| refreshed | 13 other ACTIVE rows | | | | LastSeen only |

All ACTIVE quotes are exact substrings of the current ScopeOfWork and at most 30 words. Declared mirrors: 0. The human-owned prefix of `_DEPENDENCIES.md` is byte-identical.

## Validators

- `validate_dependencies_schema.py`: exit 0 — VALID: projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-05_Native OAuth-sign-in, API-key and local-provider access/Dependencies.csv /   Columns: 29 (29 required + 0 extension) /   Data rows: 17.
- `validate_enum.py`: 21 invocations, 21 PASS.
- `validate_id_format.sh`: 24 invocations, 24 PASS.
- Parent anchors (ACTIVE IMPLEMENTS_NODE): 1. Local checks: PASS. Warnings: none.

## Comparison with ARC_EFFECT and the accepted register

- **New arcs from this register:** none.
- **Expected and produced:** every ledger register row named in the accepted register row above, except as listed below; see Run Notes in `_DEPENDENCIES.md` for the row-by-row account.
- **Expected but missing:** R3-01-05-a: DOWNSTREAM row to DEL-01-01 — not grounded (DEL-01-01 named only as owner/supplier and in AX-004 joint scope); arc carried by DEP-01-01-024.
- **Produced but not named in the ledger (non-topological, required by the revised text):** none.

## Guards

- Guards (brief; SOW_REVISIONS_A/B "Extraction guards"; Handoff_State next-workflow row; ARC_EFFECT §3), checked graph-wide after the run: R17-10 holds (DEL-01-02 reaches only DEL-01-01, DEL-01-05, DEL-04-01; DEL-01-03 those and DEL-01-02); DEL-04-01 has no supplier; no SCC-002 member depends on DEL-09-06; N-12, N-B8, NR-03, NR-06 and NR-10 are absent; nothing names DEL-11-02.
