# DX return — DEL-05-01 Minimal-loop and model receiving contract

- Node DX (Type 2 TASK, Claude Code subagent dispatched by the HELP_HUMAN session; no descendants). Basis commit 2d5e6845c5 (SCA-V4-003 REVISE).
- Method: `workflows/dependency-extract/WORKFLOW.md`. MODE UPDATE, STRICTNESS CONSERVATIVE. SOURCE_DOCS `ScopeOfWork.md` only. DECOMPOSITION_PATH `execution/_Decomposition/SOFTWARE_DECOMP.md` (sha256 `983199cc…a70d`).
- Source `ScopeOfWork.md` SHA256 `6fdf4d59e91c0f2ccc91f71950e60f0e2cd5d9549b5fffdfc01eacadab094fa1` (revised by SCA-V4-003 G-0501-01…04 (OUT-002, CLM-002, TBD-003, AX-005)). It was not changed.
- Accepted register row: `Amendment_Actions.csv` row 17 — ScopeOfWork blocks G-0501-01..G-0501-04 (4) carrying S-0501-1 P1-10; register UPDATE rows R-0501-1 R-0501-2 R-0501-3 R-0501-4 R-0501-5.
- Outputs (SHA256):
  - `Dependencies.csv` `9cf716c18b0077d6084c1d79693248d3b829d83c30ac822b97ed887101f0eb70`.
  - `_DEPENDENCIES.md` `59ce3dc2a206589eecc42ea919b45fd5ec65a4ca2e3839ca7694177561f23658`.
  - Run record `_run_records/dependency-extract-20261003-sca003.md` `f0493cc867bfa49c92f07e1775f15c942b200120cdff0e5746e50d6338df4dfe`.

## Register result

The register holds 27 ACTIVE rows (13 ANCHOR, 14 EXECUTION) and 0 RETIRED. Before the run it held 25 ACTIVE rows.

| Change | Row | Class / type | Direction | Target | Evidence / what changed |
|---|---|---|---|---|---|
| updated | DEP-05-01-014 | EXECUTION / INTERFACE | UPSTREAM | DEL-03-01 | fields: Notes |
| updated | DEP-05-01-024 | EXECUTION / PREREQUISITE | UPSTREAM | Adopted host model-interface and detailed protocol/fixture b | fields: SourceRef, EvidenceQuote, Notes |
| updated | DEP-05-01-025 | EXECUTION / INTERFACE | UPSTREAM | DEL-04-02 | fields: Notes |
| added | DEP-05-01-026 | EXECUTION / INTERFACE | UPSTREAM | DEL-01-05 | "It also receives App v4 `DEL-01-05`'s local-server capability requirements and qualification limits (its capability handoff) as information, keeping the App's provider interface distinct from a host's model interface;" (28 words). EXPLICIT/HIGH |
| added | DEP-05-01-027 | EXECUTION / HANDOVER | DOWNSTREAM | DEP-001 | "Coordinate host questions through the authorized human-relayed file path in Acceptance J/O; preparation of a file is not delivery or adoption." (21 words). EXPLICIT/MEDIUM |
| refreshed | 22 other ACTIVE rows | | | | LastSeen only |

All ACTIVE quotes are exact substrings of the current ScopeOfWork and at most 30 words. Declared mirrors: 0. The human-owned prefix of `_DEPENDENCIES.md` is byte-identical.

## Validators

- `validate_dependencies_schema.py`: exit 0 — VALID: projects/chirality-app-v4/execution/PKG-05_Embedded-host receiving integration/1_Working/DEL-05-01_Minimal-loop and model receiving contract/Dependencies.csv /   Columns: 29 (29 required + 0 extension) /   Data rows: 27.
- `validate_enum.py`: 24 invocations, 24 PASS.
- `validate_id_format.sh`: 42 invocations, 42 PASS.
- Parent anchors (ACTIVE IMPLEMENTS_NODE): 1. Local checks: PASS. Warnings: none.

## Comparison with ARC_EFFECT and the accepted register

- **New arcs from this register:** none.
- **Expected and produced:** every ledger register row named in the accepted register row above, except as listed below; see Run Notes in `_DEPENDENCIES.md` for the row-by-row account.
- **Expected but missing:** none.
- **Produced but not named in the ledger (non-topological, required by the revised text):** none.

## Guards

- Guards (brief; SOW_REVISIONS_A/B "Extraction guards"; Handoff_State next-workflow row; ARC_EFFECT §3), checked graph-wide after the run: R17-10 holds (DEL-01-02 reaches only DEL-01-01, DEL-01-05, DEL-04-01; DEL-01-03 those and DEL-01-02); DEL-04-01 has no supplier; no SCC-002 member depends on DEL-09-06; N-12, N-B8, NR-03, NR-06 and NR-10 are absent; nothing names DEL-11-02.
