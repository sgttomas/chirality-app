# DX return — DEL-02-01 Portable workflow contract and shared allocation

- Node DX (Type 2 TASK, Claude Code subagent dispatched by the HELP_HUMAN session; no descendants). Basis commit 2d5e6845c5 (SCA-V4-003 REVISE).
- Method: `workflows/dependency-extract/WORKFLOW.md`. MODE UPDATE, STRICTNESS CONSERVATIVE. SOURCE_DOCS `ScopeOfWork.md` only. DECOMPOSITION_PATH `execution/_Decomposition/SOFTWARE_DECOMP.md` (sha256 `983199cc…a70d`).
- Source `ScopeOfWork.md` SHA256 `9479fc882decd3721a346ff5723751091db9965a65d6078baf6562ed1779bd49` (revised by SCA-V4-003 G-0201-01…03 (CLM-002, AX-007)). It was not changed.
- Accepted register row: `Amendment_Actions.csv` row 6 — ScopeOfWork blocks G-0201-01..G-0201-03 (3) carrying SC2-02-01-1 SC2-02-01-2; register UPDATE rows R2-02-01-a..f R2-02-01-g R2-02-01-h RP1-MX-0201.
- Outputs (SHA256):
  - `Dependencies.csv` `99db38e1e55e04aac0c8b207b98b423d21b9133cf271d67d5c202088454741d4`.
  - `_DEPENDENCIES.md` `24ce369b6ca32ae0a1a1a81a50a0561ab1b93e65313f41587ca17539d48ce461`.
  - Run record `_run_records/dependency-extract-20261003-sca003.md` `4a3e7f46884a70435c17c2af561df9325bccf855525457b8cf6a5b0787c2a343`.

## Register result

The register holds 40 ACTIVE rows (16 ANCHOR, 24 EXECUTION) and 0 RETIRED. Before the run it held 29 ACTIVE rows.

| Change | Row | Class / type | Direction | Target | Evidence / what changed |
|---|---|---|---|---|---|
| updated | DEP-02-01-025 | EXECUTION / INTERFACE | UPSTREAM | DEL-01-01 | fields: Statement, SourceRef, Notes |
| updated | DEP-02-01-027 | EXECUTION / INTERFACE | DOWNSTREAM | DEL-03-03 | fields: RequiredMaturity, SatisfactionStatus, Notes |
| added | DEP-02-01-030 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-02-02 | "This contract is received by `DEL-02-02`, `DEL-02-03`, `DEL-02-04`, `DEL-03-02`, `DEL-03-04`, `DEL-05-01`, `DEL-05-02`, `DEL-08-02`, `DEL-09-02`, `DEL-09-06` and `DEL-10-03`, each of which declares it upstream in its own register." (27 words). EXPLICIT/HIGH |
| added | DEP-02-01-031 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-02-03 | "This contract is received by `DEL-02-02`, `DEL-02-03`, `DEL-02-04`, `DEL-03-02`, `DEL-03-04`, `DEL-05-01`, `DEL-05-02`, `DEL-08-02`, `DEL-09-02`, `DEL-09-06` and `DEL-10-03`, each of which declares it upstream in its own register." (27 words). EXPLICIT/HIGH |
| added | DEP-02-01-032 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-02-04 | "This contract is received by `DEL-02-02`, `DEL-02-03`, `DEL-02-04`, `DEL-03-02`, `DEL-03-04`, `DEL-05-01`, `DEL-05-02`, `DEL-08-02`, `DEL-09-02`, `DEL-09-06` and `DEL-10-03`, each of which declares it upstream in its own register." (27 words). EXPLICIT/HIGH |
| added | DEP-02-01-033 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-03-02 | "This contract is received by `DEL-02-02`, `DEL-02-03`, `DEL-02-04`, `DEL-03-02`, `DEL-03-04`, `DEL-05-01`, `DEL-05-02`, `DEL-08-02`, `DEL-09-02`, `DEL-09-06` and `DEL-10-03`, each of which declares it upstream in its own register." (27 words). EXPLICIT/HIGH |
| added | DEP-02-01-034 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-03-04 | "This contract is received by `DEL-02-02`, `DEL-02-03`, `DEL-02-04`, `DEL-03-02`, `DEL-03-04`, `DEL-05-01`, `DEL-05-02`, `DEL-08-02`, `DEL-09-02`, `DEL-09-06` and `DEL-10-03`, each of which declares it upstream in its own register." (27 words). EXPLICIT/HIGH |
| added | DEP-02-01-035 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-05-01 | "This contract is received by `DEL-02-02`, `DEL-02-03`, `DEL-02-04`, `DEL-03-02`, `DEL-03-04`, `DEL-05-01`, `DEL-05-02`, `DEL-08-02`, `DEL-09-02`, `DEL-09-06` and `DEL-10-03`, each of which declares it upstream in its own register." (27 words). EXPLICIT/HIGH |
| added | DEP-02-01-036 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-05-02 | "This contract is received by `DEL-02-02`, `DEL-02-03`, `DEL-02-04`, `DEL-03-02`, `DEL-03-04`, `DEL-05-01`, `DEL-05-02`, `DEL-08-02`, `DEL-09-02`, `DEL-09-06` and `DEL-10-03`, each of which declares it upstream in its own register." (27 words). EXPLICIT/HIGH |
| added | DEP-02-01-037 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-08-02 | "This contract is received by `DEL-02-02`, `DEL-02-03`, `DEL-02-04`, `DEL-03-02`, `DEL-03-04`, `DEL-05-01`, `DEL-05-02`, `DEL-08-02`, `DEL-09-02`, `DEL-09-06` and `DEL-10-03`, each of which declares it upstream in its own register." (27 words). EXPLICIT/HIGH |
| added | DEP-02-01-038 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-09-02 | "This contract is received by `DEL-02-02`, `DEL-02-03`, `DEL-02-04`, `DEL-03-02`, `DEL-03-04`, `DEL-05-01`, `DEL-05-02`, `DEL-08-02`, `DEL-09-02`, `DEL-09-06` and `DEL-10-03`, each of which declares it upstream in its own register." (27 words). EXPLICIT/HIGH |
| added | DEP-02-01-039 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-09-06 | "This contract is received by `DEL-02-02`, `DEL-02-03`, `DEL-02-04`, `DEL-03-02`, `DEL-03-04`, `DEL-05-01`, `DEL-05-02`, `DEL-08-02`, `DEL-09-02`, `DEL-09-06` and `DEL-10-03`, each of which declares it upstream in its own register." (27 words). EXPLICIT/HIGH |
| added | DEP-02-01-040 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-10-03 | "This contract is received by `DEL-02-02`, `DEL-02-03`, `DEL-02-04`, `DEL-03-02`, `DEL-03-04`, `DEL-05-01`, `DEL-05-02`, `DEL-08-02`, `DEL-09-02`, `DEL-09-06` and `DEL-10-03`, each of which declares it upstream in its own register." (27 words). EXPLICIT/HIGH |
| refreshed | 27 other ACTIVE rows | | | | LastSeen only |

All ACTIVE quotes are exact substrings of the current ScopeOfWork and at most 30 words. Declared mirrors: 0. The human-owned prefix of `_DEPENDENCIES.md` is byte-identical.

## Validators

- `validate_dependencies_schema.py`: exit 0 — VALID: projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-01_Portable workflow contract and shared allocation/Dependencies.csv /   Columns: 29 (29 required + 0 extension) /   Data rows: 40.
- `validate_enum.py`: 23 invocations, 23 PASS.
- `validate_id_format.sh`: 65 invocations, 65 PASS.
- Parent anchors (ACTIVE IMPLEMENTS_NODE): 1. Local checks: PASS. Warnings: none.

## Comparison with ARC_EFFECT and the accepted register

- **New arcs from this register:** none.
- **Expected and produced:** every ledger register row named in the accepted register row above, except as listed below; see Run Notes in `_DEPENDENCIES.md` for the row-by-row account.
- **Expected but missing:** none.
- **Produced but not named in the ledger (non-topological, required by the revised text):** none.

## Guards

- Guards (brief; SOW_REVISIONS_A/B "Extraction guards"; Handoff_State next-workflow row; ARC_EFFECT §3), checked graph-wide after the run: R17-10 holds (DEL-01-02 reaches only DEL-01-01, DEL-01-05, DEL-04-01; DEL-01-03 those and DEL-01-02); DEL-04-01 has no supplier; no SCC-002 member depends on DEL-09-06; N-12, N-B8, NR-03, NR-06 and NR-10 are absent; nothing names DEL-11-02.
