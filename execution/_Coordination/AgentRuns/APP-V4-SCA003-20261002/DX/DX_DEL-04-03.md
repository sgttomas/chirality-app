# DX return — DEL-04-03 Content-bound decisions and compact run records

- Node DX (Type 2 TASK, Claude Code subagent dispatched by the HELP_HUMAN session; no descendants). Basis commit 2d5e6845c5 (SCA-V4-003 REVISE).
- Method: `workflows/dependency-extract/WORKFLOW.md`. MODE UPDATE, STRICTNESS CONSERVATIVE. SOURCE_DOCS `ScopeOfWork.md` only. DECOMPOSITION_PATH `execution/_Decomposition/SOFTWARE_DECOMP.md` (sha256 `983199cc…a70d`).
- Source `ScopeOfWork.md` SHA256 `b8b58d674e3ac2d86c53005951ca7182dcdeb810964901191afe14cec07afc66` (revised by SCA-V4-003 G-0403-01…06 (CLM-004, REQ-003, REQ-005, AX-005)). It was not changed.
- Accepted register row: `Amendment_Actions.csv` row 16 — ScopeOfWork blocks G-0403-01..G-0403-06 (6) carrying SC2-04-03-1 SC2-04-03-2 SC2-04-03-3 P1-05 R22-7-SoW; register UPDATE rows R2-04-03-a..d R2-04-03-e R2-04-03-f R2-04-03-g R2-04-03-h R20-10 R22-7-reg RP1-MX-0403.
- Outputs (SHA256):
  - `Dependencies.csv` `cff3c10a4b78624030a93ad544d58e527f786944e65ebba150a7f05be5639779`.
  - `_DEPENDENCIES.md` `ad54efd93ea473b1c768fdc6a48cab7f82e29b9846a8a6f4e3f00829e0d32a9d`.
  - Run record `_run_records/dependency-extract-20261003-sca003.md` `1339c698fd638ff0fc30d2cbb675bd7cbde1b917ae718d152648bcb1ebb2e633`.

## Register result

The register holds 45 ACTIVE rows (10 ANCHOR, 35 EXECUTION) and 0 RETIRED. Before the run it held 33 ACTIVE rows.

| Change | Row | Class / type | Direction | Target | Evidence / what changed |
|---|---|---|---|---|---|
| updated | DEP-04-03-019 | EXECUTION / CONSTRAINT | UPSTREAM | Owner with affected App/SWB contract owners — OI-001/OI-002  | fields: SourceRef, Notes |
| updated | DEP-04-03-020 | EXECUTION / CONSTRAINT | UPSTREAM | Shared contract, SWB implementation and App/shared contract  | fields: SourceRef, Notes |
| updated | DEP-04-03-025 | EXECUTION / INTERFACE | UPSTREAM | DEL-02-03 | fields: Statement, SourceRef, EvidenceQuote, Notes |
| updated | DEP-04-03-031 | EXECUTION / INTERFACE | DOWNSTREAM | DEL-09-06 | fields: Notes |
| updated | DEP-04-03-033 | EXECUTION / CONSTRAINT | UPSTREAM | OI-021 | fields: SourceRef, Notes |
| added | DEP-04-03-034 | EXECUTION / INTERFACE | UPSTREAM | DEL-02-01 | "the workflow identity tuple and the checkpoint disposition vocabulary from `DEL-02-01`," (11 words). EXPLICIT/HIGH |
| added | DEP-04-03-035 | EXECUTION / INTERFACE | UPSTREAM | DEL-02-02 | "the per-run run-start text and run-end line with their content identity and supply-check record, the selection record and the A15 descriptor's reviewed-content and prior-revision relations from `DEL-02-02`," (27 words). EXPLICIT/HIGH |
| added | DEP-04-03-036 | EXECUTION / INTERFACE | UPSTREAM | DEL-02-04 | "the limit account and observations that a stated limit was not kept) from `DEL-02-04`," (14 words). EXPLICIT/HIGH |
| added | DEP-04-03-037 | EXECUTION / INTERFACE | DOWNSTREAM | DEL-02-01 | "App v4 `DEL-02-01`, `DEL-02-03` and `DEL-03-01` consume it at deliverable level, `DEL-03-04` (integration guide) declares it upstream," (17 words). EXPLICIT/HIGH |
| added | DEP-04-03-038 | EXECUTION / INTERFACE | DOWNSTREAM | DEL-02-03 | "App v4 `DEL-02-01`, `DEL-02-03` and `DEL-03-01` consume it at deliverable level, `DEL-03-04` (integration guide) declares it upstream," (17 words). EXPLICIT/HIGH |
| added | DEP-04-03-039 | EXECUTION / INTERFACE | DOWNSTREAM | DEL-03-01 | "App v4 `DEL-02-01`, `DEL-02-03` and `DEL-03-01` consume it at deliverable level, `DEL-03-04` (integration guide) declares it upstream," (17 words). EXPLICIT/HIGH |
| added | DEP-04-03-040 | EXECUTION / INTERFACE | DOWNSTREAM | DEL-03-04 | "App v4 `DEL-02-01`, `DEL-02-03` and `DEL-03-01` consume it at deliverable level, `DEL-03-04` (integration guide) declares it upstream," (17 words). EXPLICIT/HIGH |
| added | DEP-04-03-041 | EXECUTION / INTERFACE | DOWNSTREAM | DEL-01-04 | "and `DEL-01-04`, `DEL-02-02`, `DEL-09-02`, `DEL-09-05` and `DEL-10-03` do so in their own registers." (13 words). EXPLICIT/HIGH |
| added | DEP-04-03-042 | EXECUTION / INTERFACE | DOWNSTREAM | DEL-02-02 | "and `DEL-01-04`, `DEL-02-02`, `DEL-09-02`, `DEL-09-05` and `DEL-10-03` do so in their own registers." (13 words). EXPLICIT/HIGH |
| added | DEP-04-03-043 | EXECUTION / INTERFACE | DOWNSTREAM | DEL-09-02 | "and `DEL-01-04`, `DEL-02-02`, `DEL-09-02`, `DEL-09-05` and `DEL-10-03` do so in their own registers." (13 words). EXPLICIT/HIGH |
| added | DEP-04-03-044 | EXECUTION / INTERFACE | DOWNSTREAM | DEL-09-05 | "and `DEL-01-04`, `DEL-02-02`, `DEL-09-02`, `DEL-09-05` and `DEL-10-03` do so in their own registers." (13 words). EXPLICIT/HIGH |
| added | DEP-04-03-045 | EXECUTION / INTERFACE | DOWNSTREAM | DEL-10-03 | "and `DEL-01-04`, `DEL-02-02`, `DEL-09-02`, `DEL-09-05` and `DEL-10-03` do so in their own registers." (13 words). EXPLICIT/HIGH |
| refreshed | 28 other ACTIVE rows | | | | LastSeen only |

All ACTIVE quotes are exact substrings of the current ScopeOfWork and at most 30 words. Declared mirrors: 0. The human-owned prefix of `_DEPENDENCIES.md` is byte-identical.

## Validators

- `validate_dependencies_schema.py`: exit 0 — VALID: projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-03_Content-bound decisions and compact run records/Dependencies.csv /   Columns: 29 (29 required + 0 extension) /   Data rows: 45.
- `validate_enum.py`: 22 invocations, 22 PASS.
- `validate_id_format.sh`: 74 invocations, 74 PASS.
- Parent anchors (ACTIVE IMPLEMENTS_NODE): 1. Local checks: PASS. Warnings: none.

## Comparison with ARC_EFFECT and the accepted register

- **New arcs from this register:** R2-04-03-e DEL-04-03 → DEL-02-01 (held), R20-10 DEL-04-03 → DEL-02-02 (held).
- **Expected and produced:** every ledger register row named in the accepted register row above, except as listed below; see Run Notes in `_DEPENDENCIES.md` for the row-by-row account.
- **Expected but missing:** none.
- **Produced but not named in the ledger (non-topological, required by the revised text):** DEP-04-03-019/-020/-033 SourceRef line numbers.

## Guards

- Guards (brief; SOW_REVISIONS_A/B "Extraction guards"; Handoff_State next-workflow row; ARC_EFFECT §3), checked graph-wide after the run: R17-10 holds (DEL-01-02 reaches only DEL-01-01, DEL-01-05, DEL-04-01; DEL-01-03 those and DEL-01-02); DEL-04-01 has no supplier; no SCC-002 member depends on DEL-09-06; N-12, N-B8, NR-03, NR-06 and NR-10 are absent; nothing names DEL-11-02.
