# DX return — DEL-03-01 Capability catalog and read-basis contract

- Node DX (Type 2 TASK, Claude Code subagent dispatched by the HELP_HUMAN session; no descendants). Basis commit 2d5e6845c5 (SCA-V4-003 REVISE).
- Method: `workflows/dependency-extract/WORKFLOW.md`. MODE UPDATE, STRICTNESS CONSERVATIVE. SOURCE_DOCS `ScopeOfWork.md` only. DECOMPOSITION_PATH `execution/_Decomposition/SOFTWARE_DECOMP.md` (sha256 `983199cc…a70d`).
- Source `ScopeOfWork.md` SHA256 `48f0496c88b52a48aa86c606d3879b1bc09b9fd8631e765cf06ab02d168c1b6c` (revised by SCA-V4-003 G-0301-01…08 (CLM-002, OUT-001, OUT-003, REQ-001, REQ-002, AX-005)). It was not changed.
- Accepted register row: `Amendment_Actions.csv` row 10 — ScopeOfWork blocks G-0301-01..G-0301-08 (8) carrying S-01-1 S-01-2 S-01-3 S-01-5 P1-06; register UPDATE rows R-01-1 R-01-2 R-01-3.
- Outputs (SHA256):
  - `Dependencies.csv` `01962fe8fecd10f1bf2018c72eaf36f0f74a8f969fb7d950b82959e0b5859c86`.
  - `_DEPENDENCIES.md` `ac82054da93d0b8068a37a94f478dbdf2196ef1b70238655bb475835319619ae`.
  - Run record `_run_records/dependency-extract-20261003-sca003.md` `94f8d8b76b78859081d4767cf889df26cd0e79748d4abc665cdca4cd226e8133`.

## Register result

The register holds 41 ACTIVE rows (21 ANCHOR, 20 EXECUTION) and 1 RETIRED. Before the run it held 31 ACTIVE rows.

| Change | Row | Class / type | Direction | Target | Evidence / what changed |
|---|---|---|---|---|---|
| retired | DEP-03-01-022 | EXECUTION / HANDOVER | DOWNSTREAM | PKG-02 | see Notes (retired_by recorded) |
| updated | DEP-03-01-025 | EXECUTION / PREREQUISITE | UPSTREAM | SWBPIPE | fields: SourceRef, Notes |
| added | DEP-03-01-032 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-02-01 | "This contract is also received by App v4 `DEL-02-01` (tool descriptors for required-tool declarations)," (14 words). EXPLICIT/HIGH |
| added | DEP-03-01-033 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-02-03 | "`DEL-02-03` (capability semantics for required-tool checks)," (6 words). EXPLICIT/HIGH |
| added | DEP-03-01-034 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-03-03 | "`DEL-03-03` and `DEL-03-04` (catalog/read-basis definitions)," (5 words). EXPLICIT/HIGH |
| added | DEP-03-01-035 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-03-04 | "`DEL-03-03` and `DEL-03-04` (catalog/read-basis definitions)," (5 words). EXPLICIT/HIGH |
| added | DEP-03-01-036 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-04-02 | "`DEL-04-02` (read-basis and standing facets)," (5 words). EXPLICIT/HIGH |
| added | DEP-03-01-037 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-04-03 | "`DEL-04-03` (subject content identities and method designations)," (7 words). EXPLICIT/HIGH |
| added | DEP-03-01-038 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-05-01 | "`DEL-05-01` (schemas and catalog identity for loop validation)," (8 words). EXPLICIT/HIGH |
| added | DEP-03-01-039 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-05-02 | "`DEL-05-02` (panel receiving)," (3 words). EXPLICIT/HIGH |
| added | DEP-03-01-040 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-09-06 | "`DEL-09-06` (the connected activity)," (4 words). EXPLICIT/HIGH |
| added | DEP-03-01-041 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-09-09 | "`DEL-09-09` (the external trace)" (4 words). EXPLICIT/HIGH |
| added | DEP-03-01-042 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-10-03 | "`DEL-10-03` (the shared account), each of which declares it upstream in its own register." (14 words). EXPLICIT/HIGH |
| refreshed | 29 other ACTIVE rows | | | | LastSeen only |

All ACTIVE quotes are exact substrings of the current ScopeOfWork and at most 30 words. Declared mirrors: 0. The human-owned prefix of `_DEPENDENCIES.md` is byte-identical.

## Validators

- `validate_dependencies_schema.py`: exit 0 — VALID: projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-01_Capability catalog and read-basis contract/Dependencies.csv /   Columns: 29 (29 required + 0 extension) /   Data rows: 42.
- `validate_enum.py`: 25 invocations, 25 PASS.
- `validate_id_format.sh`: 62 invocations, 62 PASS.
- Parent anchors (ACTIVE IMPLEMENTS_NODE): 1. Local checks: PASS. Warnings: none.

## Comparison with ARC_EFFECT and the accepted register

- **New arcs from this register:** none.
- **Expected and produced:** every ledger register row named in the accepted register row above, except as listed below; see Run Notes in `_DEPENDENCIES.md` for the row-by-row account.
- **Expected but missing:** none.
- **Produced but not named in the ledger (non-topological, required by the revised text):** DEP-03-01-025 Notes also record the REQ-002 destination elements (non-topological).

## Guards

- Guards (brief; SOW_REVISIONS_A/B "Extraction guards"; Handoff_State next-workflow row; ARC_EFFECT §3), checked graph-wide after the run: R17-10 holds (DEL-01-02 reaches only DEL-01-01, DEL-01-05, DEL-04-01; DEL-01-03 those and DEL-01-02); DEL-04-01 has no supplier; no SCC-002 member depends on DEL-09-06; N-12, N-B8, NR-03, NR-06 and NR-10 are absent; nothing names DEL-11-02.
