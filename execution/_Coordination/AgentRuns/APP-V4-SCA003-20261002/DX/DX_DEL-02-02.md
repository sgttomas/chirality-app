# DX return — DEL-02-02 Workflow-making workspace and registration

- Node DX (Type 2 TASK, Claude Code subagent dispatched by the HELP_HUMAN session; no descendants). Basis commit 2d5e6845c5 (SCA-V4-003 REVISE).
- Method: `workflows/dependency-extract/WORKFLOW.md`. MODE UPDATE, STRICTNESS CONSERVATIVE. SOURCE_DOCS `ScopeOfWork.md` only. DECOMPOSITION_PATH `execution/_Decomposition/SOFTWARE_DECOMP.md` (sha256 `983199cc…a70d`).
- Source `ScopeOfWork.md` SHA256 `fe9f9bd923f94ed314aba054d5d04e4e803ca4ec0456bd5d11d94df355198d51` (revised by SCA-V4-003 G-0202-01…09 (CLM-002, CLM-003, REQ-001, REQ-002, REQ-003, REQ-008, AX-005)). It was not changed.
- Accepted register row: `Amendment_Actions.csv` row 7 — ScopeOfWork blocks G-0202-01..G-0202-09 (9) carrying SC3-02-02-1 SC3-02-02-2 SC3-02-02-3 SC3-02-02-4 SC3-02-02-10 SC3-02-02-11 SC3-02-02-12 P1-03; register UPDATE rows NR-04 SC3-02-02-6 SC3-02-02-7 SC3-02-02-9 R3-02-02-a..c R3-02-02-d.
- Outputs (SHA256):
  - `Dependencies.csv` `a97be837fd0dfe9c6dc2b402876e6454130a68da288b68d6c0d1abf4b0806c62`.
  - `_DEPENDENCIES.md` `0024dccb4c06675af1a339f44e41573d353f04d0ba98e257adc85729c09482be`.
  - Run record `_run_records/dependency-extract-20261003-sca003.md` `d7f3c9bd81a67975eae0cd3b978d82466f76458d57b52e267a47330592316122`.

## Register result

The register holds 23 ACTIVE rows (11 ANCHOR, 12 EXECUTION) and 1 RETIRED. Before the run it held 18 ACTIVE rows.

| Change | Row | Class / type | Direction | Target | Evidence / what changed |
|---|---|---|---|---|---|
| updated | DEP-02-02-013 | EXECUTION / INTERFACE | UPSTREAM | DEL-01-04 | fields: Statement, SourceRef, Notes |
| updated | DEP-02-02-015 | EXECUTION / INTERFACE | UPSTREAM | DEL-02-03 | fields: Statement, SourceRef, Notes |
| updated | DEP-02-02-016 | EXECUTION / INTERFACE | UPSTREAM | DEL-04-01 | fields: Statement, Notes |
| updated | DEP-02-02-017 | EXECUTION / INTERFACE | UPSTREAM | DEL-04-03 | fields: Statement, Notes |
| added | DEP-02-02-020 | EXECUTION / INTERFACE | UPSTREAM | DEL-01-02 | "A run in the chain ends only as `DEL-01-02` defines ending a run, distinct from interrupting a turn or stopping Codex," (21 words). EXPLICIT/HIGH |
| added | DEP-02-02-021 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-01-04 | "and the workspace's draft, registration and selection contract by `DEL-01-04`, `DEL-02-03` and `DEL-09-06`, each of which declares it upstream in its own register." (23 words). EXPLICIT/HIGH |
| added | DEP-02-02-022 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-02-03 | "the run text and its supply-check record are received by `DEL-02-03`, `DEL-01-04` (turn composition) and `DEL-04-03` (supplied-workflow evidence)," (18 words). EXPLICIT/HIGH |
| added | DEP-02-02-023 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-09-06 | "and the workspace's draft, registration and selection contract by `DEL-01-04`, `DEL-02-03` and `DEL-09-06`, each of which declares it upstream in its own register." (23 words). EXPLICIT/HIGH |
| added | DEP-02-02-024 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-04-03 | "the run text and its supply-check record are received by `DEL-02-03`, `DEL-01-04` (turn composition) and `DEL-04-03` (supplied-workflow evidence)," (18 words). EXPLICIT/HIGH |
| refreshed | 14 other ACTIVE rows | | | | LastSeen only |

All ACTIVE quotes are exact substrings of the current ScopeOfWork and at most 30 words. Declared mirrors: 0. The human-owned prefix of `_DEPENDENCIES.md` is byte-identical.

## Validators

- `validate_dependencies_schema.py`: exit 0 — VALID: projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-02_Workflow-making workspace and registration/Dependencies.csv /   Columns: 29 (29 required + 0 extension) /   Data rows: 24.
- `validate_enum.py`: 22 invocations, 22 PASS.
- `validate_id_format.sh`: 38 invocations, 38 PASS.
- Parent anchors (ACTIVE IMPLEMENTS_NODE): 1. Local checks: PASS. Warnings: none.

## Comparison with ARC_EFFECT and the accepted register

- **New arcs from this register:** NR-04 DEL-02-02 → DEL-01-02 (admitted).
- **Expected and produced:** every ledger register row named in the accepted register row above, except as listed below; see Run Notes in `_DEPENDENCIES.md` for the row-by-row account.
- **Expected but missing:** none.
- **Produced but not named in the ledger (non-topological, required by the revised text):** none.

## Guards

- Guards (brief; SOW_REVISIONS_A/B "Extraction guards"; Handoff_State next-workflow row; ARC_EFFECT §3), checked graph-wide after the run: R17-10 holds (DEL-01-02 reaches only DEL-01-01, DEL-01-05, DEL-04-01; DEL-01-03 those and DEL-01-02); DEL-04-01 has no supplier; no SCC-002 member depends on DEL-09-06; N-12, N-B8, NR-03, NR-06 and NR-10 are absent; nothing names DEL-11-02.
