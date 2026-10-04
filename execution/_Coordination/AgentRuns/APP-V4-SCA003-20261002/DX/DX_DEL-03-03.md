# DX return — DEL-03-03 Local external-agent receiving adapter

- Node DX (Type 2 TASK, Claude Code subagent dispatched by the HELP_HUMAN session; no descendants). Basis commit 2d5e6845c5 (SCA-V4-003 REVISE).
- Method: `workflows/dependency-extract/WORKFLOW.md`. MODE UPDATE, STRICTNESS CONSERVATIVE. SOURCE_DOCS `ScopeOfWork.md` only. DECOMPOSITION_PATH `execution/_Decomposition/SOFTWARE_DECOMP.md` (sha256 `983199cc…a70d`).
- Source `ScopeOfWork.md` SHA256 `d76b053f4e97a466429e568a80b911b40550e4d8b97e634488d4aaf7de1e2e7a` (revised by SCA-V4-003 G-0303-01…05 (CLM-002, CLM-003, REQ-003, VER-002, AX-006)). It was not changed.
- Accepted register row: `Amendment_Actions.csv` row 12 — ScopeOfWork blocks G-0303-01..G-0303-05 (5) carrying S-03-1 S-03-2 S-03-3 S-03-4 S-03-5 P1-02 P1-08; register UPDATE rows R-03-1 R-03-2 R-03-3 R-03-4 R-03-5 R-03-6 NR-02.
- Outputs (SHA256):
  - `Dependencies.csv` `55979f4635682b1bb57db6accd282a030185008ab9a1311cd917459dddc11998`.
  - `_DEPENDENCIES.md` `7184613e16deb7405fd9a52adb6e536322d8c23e57bbc0d2e2f9ac4bd3b7e60e`.
  - Run record `_run_records/dependency-extract-20261003-sca003.md` `eb54926e4f7ebf2f8352e623967dd5d53ed603ef6ab65908f5c8312393488163`.

## Register result

The register holds 20 ACTIVE rows (5 ANCHOR, 15 EXECUTION) and 0 RETIRED. Before the run it held 14 ACTIVE rows.

| Change | Row | Class / type | Direction | Target | Evidence / what changed |
|---|---|---|---|---|---|
| updated | DEP-03-03-008 | EXECUTION / PREREQUISITE | UPSTREAM | DEL-04-01 | fields: RequiredMaturity, Notes |
| updated | DEP-03-03-009 | EXECUTION / PREREQUISITE | UPSTREAM | Codex native-tool capability for the selected local MCP or C | fields: Notes |
| updated | DEP-03-03-013 | EXECUTION / INTERFACE | UPSTREAM | DEL-01-01 | fields: Statement, SourceRef, EvidenceQuote, Notes |
| updated | DEP-03-03-014 | EXECUTION / INTERFACE | UPSTREAM | DEL-02-03 | fields: Statement, SourceRef, EvidenceQuote, Notes |
| added | DEP-03-03-015 | EXECUTION / INTERFACE | UPSTREAM | DEL-01-02 | "App `DEL-01-02`'s in-flight item state and relaunch fact for an external request whose Codex process stopped or whose App relaunched during submission," (22 words). EXPLICIT/HIGH |
| added | DEP-03-03-016 | EXECUTION / INTERFACE | UPSTREAM | DEL-04-02 | "App `DEL-04-02`'s visible autonomy state (grant display states and settings references)" (11 words). EXPLICIT/HIGH |
| added | DEP-03-03-017 | EXECUTION / INTERFACE | UPSTREAM | DEL-02-01 | "for the governance phase, App `DEL-02-01`'s declared checkpoint constraints," (9 words). EXPLICIT/HIGH |
| added | DEP-03-03-018 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-03-04 | "This adapter's external-agent receiving definition and evidence limits are received by App `DEL-03-04` (the integration guide)," (16 words). EXPLICIT/HIGH |
| added | DEP-03-03-019 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-04-03 | "its external dispatch entries by `DEL-04-03`," (6 words). EXPLICIT/HIGH |
| added | DEP-03-03-020 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-09-06 | "and its external-receiving meanings by `DEL-09-06`, each of which declares it upstream in its own register." (16 words). EXPLICIT/HIGH |
| refreshed | 10 other ACTIVE rows | | | | LastSeen only |

All ACTIVE quotes are exact substrings of the current ScopeOfWork and at most 30 words. Declared mirrors: 0. The human-owned prefix of `_DEPENDENCIES.md` is byte-identical.

## Validators

- `validate_dependencies_schema.py`: exit 0 — VALID: projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-03_Local external-agent receiving adapter/Dependencies.csv /   Columns: 29 (29 required + 0 extension) /   Data rows: 20.
- `validate_enum.py`: 21 invocations, 21 PASS.
- `validate_id_format.sh`: 38 invocations, 38 PASS.
- Parent anchors (ACTIVE IMPLEMENTS_NODE): 1. Local checks: PASS. Warnings: none.

## Comparison with ARC_EFFECT and the accepted register

- **New arcs from this register:** NR-02 DEL-03-03 → DEL-01-02 (admitted).
- **Expected and produced:** every ledger register row named in the accepted register row above, except as listed below; see Run Notes in `_DEPENDENCIES.md` for the row-by-row account.
- **Expected but missing:** R-03-1: DOWNSTREAM row to DEL-02-03 (1 of 4; N-24) — not grounded (DEL-02-03 named only as supplier/owner); arc carried by DEP-02-03-026.
- **Produced but not named in the ledger (non-topological, required by the revised text):** none.

## Guards

- Guards (brief; SOW_REVISIONS_A/B "Extraction guards"; Handoff_State next-workflow row; ARC_EFFECT §3), checked graph-wide after the run: R17-10 holds (DEL-01-02 reaches only DEL-01-01, DEL-01-05, DEL-04-01; DEL-01-03 those and DEL-01-02); DEL-04-01 has no supplier; no SCC-002 member depends on DEL-09-06; N-12, N-B8, NR-03, NR-06 and NR-10 are absent; nothing names DEL-11-02.
