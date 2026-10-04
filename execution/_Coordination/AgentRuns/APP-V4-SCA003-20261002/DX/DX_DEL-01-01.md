# DX return — DEL-01-01 Stock Codex hosting and supplier contract

- Node DX (Type 2 TASK, Claude Code subagent dispatched by the HELP_HUMAN session; no descendants). Basis commit 2d5e6845c5 (SCA-V4-003 REVISE).
- Method: `workflows/dependency-extract/WORKFLOW.md`. MODE UPDATE, STRICTNESS CONSERVATIVE. SOURCE_DOCS `ScopeOfWork.md` only. DECOMPOSITION_PATH `execution/_Decomposition/SOFTWARE_DECOMP.md` (sha256 `983199cc…a70d`).
- Source `ScopeOfWork.md` SHA256 `bbc81a8d31eeacab3497acf297c8c6eeac7b2f6febda5381f332ec14b8f65d02` (revised by SCA-V4-003 G-0101-01…04 (CLM-004 receivers sentence P1-09, CLM-005 harness-capability supply S-11-1, TBD-002 observation pointers S-11-2, AX-007)). It was not changed.
- Accepted register row: `Amendment_Actions.csv` row 1 — ScopeOfWork blocks G-0101-01..G-0101-04 (4) carrying S-11-1 S-11-2 P1-09; register UPDATE rows R-11-1 R-11-2 R-11-3.
- Outputs (SHA256):
  - `Dependencies.csv` `5a5a60c555247a56c637e7d57289545caa8462186793444da06b1e90decb9e38`.
  - `_DEPENDENCIES.md` `40d7a588d110fcfc82dccbd2f6a30dcaa333614bb2312247bc80633d2789bf60`.
  - Run record `_run_records/dependency-extract-20261003-sca003.md` `73f81e6353c44b93cc6bde05d3dc938baa318d9be9389365dbbe87e1d75b6467`.

## Register result

The register holds 32 ACTIVE rows (15 ANCHOR, 17 EXECUTION) and 0 RETIRED. Before the run it held 24 ACTIVE rows.

| Change | Row | Class / type | Direction | Target | Evidence / what changed |
|---|---|---|---|---|---|
| updated | DEP-01-01-017 | EXECUTION / CONSTRAINT | UPSTREAM | chirality-app-v4:OI-012 | fields: SourceRef, Notes |
| updated | DEP-01-01-018 | EXECUTION / PREREQUISITE | UPSTREAM | chirality-app-v4:DEP-005 | fields: Notes |
| updated | DEP-01-01-022 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-01-05 | fields: Notes |
| added | DEP-01-01-025 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-02-01 | "This deliverable supplies the harness-capability meaning of the selected pin (the supplier's item kinds, server requests and client methods grouped by capability, with their standing) to `DEL-02-01`," (27 words). EXPLICIT/HIGH |
| added | DEP-01-01-026 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-02-03 | "`DEL-02-03` (observed supplier facts, as capability information for App-side execution compatibility)," (11 words). EXPLICIT/HIGH |
| added | DEP-01-01-027 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-03-03 | "`DEL-03-03` (supplier MCP/dynamic-tool surfaces and channel-status facts at the definition pin)," (11 words). EXPLICIT/HIGH |
| added | DEP-01-01-028 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-03-04 | "`DEL-03-04` (native surfaces for optional external access)," (7 words). EXPLICIT/HIGH |
| added | DEP-01-01-029 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-09-06 | "`DEL-09-06` (App-side supplied-guidance and model-destination evidence)," (6 words). EXPLICIT/HIGH |
| added | DEP-01-01-030 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-06-01 | "`DEL-06-01` and `DEL-09-01` (the selected Codex pin, before protocol generation and qualification)" (12 words). EXPLICIT/HIGH |
| added | DEP-01-01-031 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-09-01 | "`DEL-06-01` and `DEL-09-01` (the selected Codex pin, before protocol generation and qualification)" (12 words). EXPLICIT/HIGH |
| added | DEP-01-01-032 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-09-02 | "`DEL-09-02` (the hosting/protocol contribution and scoped feature checks, before its joined native/protocol witness);" (13 words). EXPLICIT/HIGH |
| refreshed | 21 other ACTIVE rows | | | | LastSeen only |

All ACTIVE quotes are exact substrings of the current ScopeOfWork and at most 30 words. Declared mirrors: 0. The human-owned prefix of `_DEPENDENCIES.md` is byte-identical.

## Validators

- `validate_dependencies_schema.py`: exit 0 — VALID: projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-01_Stock Codex hosting and supplier contract/Dependencies.csv /   Columns: 29 (29 required + 0 extension) /   Data rows: 32.
- `validate_enum.py`: 22 invocations, 22 PASS.
- `validate_id_format.sh`: 51 invocations, 51 PASS.
- Parent anchors (ACTIVE IMPLEMENTS_NODE): 1. Local checks: PASS. Warnings: none.

## Comparison with ARC_EFFECT and the accepted register

- **New arcs from this register:** none.
- **Expected and produced:** every ledger register row named in the accepted register row above, except as listed below; see Run Notes in `_DEPENDENCIES.md` for the row-by-row account.
- **Expected but missing:** R-11-1: DOWNSTREAM rows to DEL-02-04 and DEL-04-03 (2 of 10) — not grounded by a receiving sentence (CLM-005 names both only as owners); arcs carried by DEP-02-04-010 and DEP-04-03-027.
- **Produced but not named in the ledger (non-topological, required by the revised text):** none.

## Guards

- Guards (brief; SOW_REVISIONS_A/B "Extraction guards"; Handoff_State next-workflow row; ARC_EFFECT §3), checked graph-wide after the run: R17-10 holds (DEL-01-02 reaches only DEL-01-01, DEL-01-05, DEL-04-01; DEL-01-03 those and DEL-01-02); DEL-04-01 has no supplier; no SCC-002 member depends on DEL-09-06; N-12, N-B8, NR-03, NR-06 and NR-10 are absent; nothing names DEL-11-02.
