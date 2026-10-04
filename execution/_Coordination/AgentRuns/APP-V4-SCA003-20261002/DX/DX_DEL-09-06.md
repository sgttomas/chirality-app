# DX return — DEL-09-06 Connected activity contract and workflow round trip

- Node DX (Type 2 TASK, Claude Code subagent dispatched by the HELP_HUMAN session; no descendants). Basis commit 2d5e6845c5 (SCA-V4-003 REVISE).
- Method: `workflows/dependency-extract/WORKFLOW.md`. MODE UPDATE, STRICTNESS CONSERVATIVE. SOURCE_DOCS `ScopeOfWork.md` only. DECOMPOSITION_PATH `execution/_Decomposition/SOFTWARE_DECOMP.md` (sha256 `983199cc…a70d`).
- Source `ScopeOfWork.md` SHA256 `8edc7b3cfedb7c0bf645805650bea42a6f7dddd15b87f5293189210f5cb361a3` (revised by SCA-V4-003 G-0906-01…05 (CLM-003, OUT-003, REQ-008, TBD-003, AX-005)). It was not changed.
- Accepted register row: `Amendment_Actions.csv` row 19 — ScopeOfWork blocks G-0906-01..G-0906-05 (5) carrying S-0906-1 S-0906-2 S-0906-3; register UPDATE rows R2-04-03-g R-0906-1 R-0906-2 R-0906-3.
- Outputs (SHA256):
  - `Dependencies.csv` `50f7528d3bf41e4c99cb591bd4d1ac5f98f6d28dbd7136be4f1b693ae6ab4e47`.
  - `_DEPENDENCIES.md` `501e45981941c55c61013539aad970df9713f1b397058a2f3a4ac595887b45d1`.
  - Run record `_run_records/dependency-extract-20261003-sca003.md` `70782788cea0971b8e7d12c416bdb9b784a9cd6545ecad9e94fa70780015ae0d`.

## Register result

The register holds 35 ACTIVE rows (11 ANCHOR, 24 EXECUTION) and 0 RETIRED. Before the run it held 34 ACTIVE rows.

| Change | Row | Class / type | Direction | Target | Evidence / what changed |
|---|---|---|---|---|---|
| updated | DEP-09-06-015 | EXECUTION / INTERFACE | UPSTREAM | DEL-04-03 | fields: RequiredMaturity, Notes |
| updated | DEP-09-06-019 | EXECUTION / PREREQUISITE | UPSTREAM | DEP-001 | fields: SourceRef, Notes |
| updated | DEP-09-06-027 | EXECUTION / INTERFACE | UPSTREAM | DEL-03-01 | fields: Notes |
| added | DEP-09-06-035 | EXECUTION / INTERFACE | UPSTREAM | DEL-09-01 | "App DEL-09-01 supplies reusable candidate-examination support and the evidence protocol (candidate, date and configuration identification; outcome states; replay, browser and native marking) that the joined witness uses." (27 words). EXPLICIT/HIGH |
| refreshed | 31 other ACTIVE rows | | | | LastSeen only |

All ACTIVE quotes are exact substrings of the current ScopeOfWork and at most 30 words. Declared mirrors: 0. The human-owned prefix of `_DEPENDENCIES.md` is byte-identical.

## Validators

- `validate_dependencies_schema.py`: exit 0 — VALID: projects/chirality-app-v4/execution/PKG-09_Candidate examination and connected journeys/1_Working/DEL-09-06_Connected activity contract and workflow round trip/Dependencies.csv /   Columns: 29 (29 required + 0 extension) /   Data rows: 35.
- `validate_enum.py`: 23 invocations, 23 PASS.
- `validate_id_format.sh`: 55 invocations, 55 PASS.
- Parent anchors (ACTIVE IMPLEMENTS_NODE): 1. Local checks: PASS. Warnings: none.

## Comparison with ARC_EFFECT and the accepted register

- **New arcs from this register:** none.
- **Expected and produced:** every ledger register row named in the accepted register row above, except as listed below; see Run Notes in `_DEPENDENCIES.md` for the row-by-row account.
- **Expected but missing:** none.
- **Produced but not named in the ledger (non-topological, required by the revised text):** none.

## Guards

- Guards (brief; SOW_REVISIONS_A/B "Extraction guards"; Handoff_State next-workflow row; ARC_EFFECT §3), checked graph-wide after the run: R17-10 holds (DEL-01-02 reaches only DEL-01-01, DEL-01-05, DEL-04-01; DEL-01-03 those and DEL-01-02); DEL-04-01 has no supplier; no SCC-002 member depends on DEL-09-06; N-12, N-B8, NR-03, NR-06 and NR-10 are absent; nothing names DEL-11-02.
