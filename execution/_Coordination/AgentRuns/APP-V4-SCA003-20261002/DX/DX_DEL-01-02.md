# DX return — DEL-01-02 Durable execution and request recovery

- Node DX (Type 2 TASK, Claude Code subagent dispatched by the HELP_HUMAN session; no descendants). Basis commit 2d5e6845c5 (SCA-V4-003 REVISE).
- Method: `workflows/dependency-extract/WORKFLOW.md`. MODE UPDATE, STRICTNESS CONSERVATIVE. SOURCE_DOCS `ScopeOfWork.md` only. DECOMPOSITION_PATH `execution/_Decomposition/SOFTWARE_DECOMP.md` (sha256 `983199cc…a70d`).
- Source `ScopeOfWork.md` SHA256 `6c62de1d749022a388d9a2c466655a35e06b0b9fa7779a7912f9df4424226a07` (revised by SCA-V4-003 G-0102-01…18 (16 definitions and AX-004)). It was not changed.
- Accepted register row: `Amendment_Actions.csv` row 2 — ScopeOfWork blocks G-0102-01..G-0102-18 (18) carrying SC3-01-02-1 SC3-01-02-2 SC3-01-02-3 SC3-01-02-4 SC3-01-02-5 SC3-01-02-6 SC3-01-02-7 SC3-01-02-8 SC3-01-02-9 SC3-01-02-10 SC3-01-02-11; register UPDATE rows R3-01-02-a R3-01-02-b R3-01-02-c R3-01-02-d R3-01-02-e R3-01-02-f R3-01-02-h.
- Outputs (SHA256):
  - `Dependencies.csv` `be62d3f0e769e82795a549d00c59a6b76799a97248903a80dcb380e0335f4ba2`.
  - `_DEPENDENCIES.md` `d9426b06f47c0795df1697331530ee9dd8172392ba3ff99b2f82481ff3fff453`.
  - Run record `_run_records/dependency-extract-20261003-sca003.md` `18f7ddc5760c1782d7e43f2b706522cfabc3c5bb71c74842435b972e1df61152`.

## Register result

The register holds 26 ACTIVE rows (17 ANCHOR, 9 EXECUTION) and 0 RETIRED. Before the run it held 21 ACTIVE rows.

| Change | Row | Class / type | Direction | Target | Evidence / what changed |
|---|---|---|---|---|---|
| updated | DEP-01-02-018 | EXECUTION / INTERFACE | UPSTREAM | DEL-01-01 | fields: Notes |
| updated | DEP-01-02-020 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-04-03 | fields: Notes |
| updated | DEP-01-02-021 | EXECUTION / CONSTRAINT | UPSTREAM | DEL-04-01 | fields: Statement, SourceRef, Notes |
| added | DEP-01-02-022 | EXECUTION / INTERFACE | DOWNSTREAM | DEL-01-03 | "serve App-v4 `DEL-01-04`, `DEL-01-03` and `DEL-09-02`," (6 words). EXPLICIT/HIGH |
| added | DEP-01-02-023 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-09-02 | "serve App-v4 `DEL-01-04`, `DEL-01-03` and `DEL-09-02`," (6 words). EXPLICIT/HIGH |
| added | DEP-01-02-024 | EXECUTION / INTERFACE | DOWNSTREAM | DEL-02-03 | "`DEL-02-03` (run tags and custody events)," (6 words). EXPLICIT/HIGH |
| added | DEP-01-02-025 | EXECUTION / INTERFACE | DOWNSTREAM | DEL-03-03 | "`DEL-03-03` (in-flight items and the relaunch fact)" (7 words). EXPLICIT/HIGH |
| added | DEP-01-02-026 | EXECUTION / INTERFACE | DOWNSTREAM | DEL-02-02 | "`DEL-02-02` (the definitions of a turn interrupt, a run end and a Codex stop, and App-start reconciliation)," (17 words). EXPLICIT/HIGH |
| refreshed | 18 other ACTIVE rows | | | | LastSeen only |

All ACTIVE quotes are exact substrings of the current ScopeOfWork and at most 30 words. Declared mirrors: 0. The human-owned prefix of `_DEPENDENCIES.md` is byte-identical.

## Validators

- `validate_dependencies_schema.py`: exit 0 — VALID: projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-02_Durable execution and request recovery/Dependencies.csv /   Columns: 29 (29 required + 0 extension) /   Data rows: 26.
- `validate_enum.py`: 20 invocations, 20 PASS.
- `validate_id_format.sh`: 41 invocations, 41 PASS.
- Parent anchors (ACTIVE IMPLEMENTS_NODE): 1. Local checks: PASS. Warnings: none.

## Comparison with ARC_EFFECT and the accepted register

- **New arcs from this register:** none (supplier-side mirrors of NR-01, NR-02, NR-04 only).
- **Expected and produced:** every ledger register row named in the accepted register row above, except as listed below; see Run Notes in `_DEPENDENCIES.md` for the row-by-row account.
- **Expected but missing:** none.
- **Produced but not named in the ledger (non-topological, required by the revised text):** DEP-01-02-020 Notes (OUT-004/REQ-006 narrowing; non-topological).

## Guards

- Guards (brief; SOW_REVISIONS_A/B "Extraction guards"; Handoff_State next-workflow row; ARC_EFFECT §3), checked graph-wide after the run: R17-10 holds (DEL-01-02 reaches only DEL-01-01, DEL-01-05, DEL-04-01; DEL-01-03 those and DEL-01-02); DEL-04-01 has no supplier; no SCC-002 member depends on DEL-09-06; N-12, N-B8, NR-03, NR-06 and NR-10 are absent; nothing names DEL-11-02.
