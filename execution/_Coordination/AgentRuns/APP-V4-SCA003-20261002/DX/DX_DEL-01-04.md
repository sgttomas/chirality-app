# DX return — DEL-01-04 Native requests, outcomes and attachments

- Node DX (Type 2 TASK, Claude Code subagent dispatched by the HELP_HUMAN session; no descendants). Basis commit 2d5e6845c5 (SCA-V4-003 REVISE).
- Method: `workflows/dependency-extract/WORKFLOW.md`. MODE UPDATE, STRICTNESS CONSERVATIVE. SOURCE_DOCS `ScopeOfWork.md` only. DECOMPOSITION_PATH `execution/_Decomposition/SOFTWARE_DECOMP.md` (sha256 `983199cc…a70d`).
- Source `ScopeOfWork.md` SHA256 `8434cc47ec28e1397e7dae548183543567f0b5fcfdefaebc0b44bc1f709aacf3` (revised by SCA-V4-003 G-0104-01…14 (CLM-001, CLM-004, OUT-002, REQ-001/002/005/006, VER-005; added OUT-005, REQ-008, AC-008, VER-008, matrix row, AX-005)). It was not changed.
- Accepted register row: `Amendment_Actions.csv` row 4 — ScopeOfWork blocks G-0104-01..G-0104-14 (14) carrying SC3-01-04-1 SC3-01-04-2 SC3-01-04-3 SC3-01-04-4 SC3-01-04-5 SC3-01-04-6 SC3-01-04-7 SC3-01-04-8 SC3-01-04-10 SC3-01-04-11 SC3-01-04-12 SC3-01-04-13; register UPDATE rows R2-01-04-a NR-05 NR-07 NR-08 NR-09 NR-4 R3-01-04-b SC3-01-04-9 R3-01-04-a.
- Outputs (SHA256):
  - `Dependencies.csv` `1c08dfda40c948d3accd723e2716ec9601e7f1da1614c686441ea59dc18db2e6`.
  - `_DEPENDENCIES.md` `3a92154ce6103a7c21aa36de3d90f3e1acec260783bf8e206a83cb7c9c9438be`.
  - Run record `_run_records/dependency-extract-20261003-sca003.md` `9c4f7b13871841bd59d78496845699bee0736a4a70d8ec9ff9b2a53b3599140c`.

## Register result

The register holds 25 ACTIVE rows (6 ANCHOR, 19 EXECUTION) and 1 RETIRED. Before the run it held 18 ACTIVE rows.

| Change | Row | Class / type | Direction | Target | Evidence / what changed |
|---|---|---|---|---|---|
| updated | DEP-01-04-009 | EXECUTION / INTERFACE | UPSTREAM | DEL-02-02 | fields: Statement, SourceRef, Notes |
| updated | DEP-01-04-010 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-02-02 | fields: Statement, SourceRef, Notes |
| updated | DEP-01-04-011 | EXECUTION / INTERFACE | UPSTREAM | DEL-04-01 | fields: Notes |
| updated | DEP-01-04-012 | EXECUTION / INTERFACE | UPSTREAM | DEL-04-03 | fields: Notes |
| updated | DEP-01-04-019 | EXECUTION / PREREQUISITE | UPSTREAM | Person performing the positive human-act case and separate f | fields: SourceRef, EvidenceQuote, Notes |
| added | DEP-01-04-020 | EXECUTION / INTERFACE | UPSTREAM | DEL-01-03 | "This slice composes the turns it sends, including the collaboration mode supplied by App `DEL-01-03` (sent explicitly after plan mode was used)" (22 words). EXPLICIT/HIGH |
| added | DEP-01-04-021 | EXECUTION / INTERFACE | UPSTREAM | DEL-01-05 | "A new conversation shows that no model is selected until the person chooses one, from the selection state App DEL-01-05 reports;" (21 words). EXPLICIT/HIGH |
| added | DEP-01-04-022 | EXECUTION / INTERFACE | UPSTREAM | DEL-04-02 | "the App's placement of the checkpoint overlay and standing facets defined by App `DEL-04-02`," (14 words). EXPLICIT/HIGH |
| added | DEP-01-04-023 | EXECUTION / INTERFACE | UPSTREAM | DEL-02-03 | "with the checkpoint display meanings of App `DEL-02-03`, whose behaviour in the App this slice owns." (16 words). EXPLICIT/HIGH |
| added | DEP-01-04-024 | EXECUTION / INTERFACE | UPSTREAM | DEL-02-04 | "A new conversation offers the roles App DEL-02-04 lists, with the registry's default preselected and clearable and no role allowed;" (20 words). EXPLICIT/HIGH |
| added | DEP-01-04-025 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-02-03 | "It is used by DEL-02-02 (A15) and DEL-02-03 (App-side positive capture fixtures), each of which declares it upstream in its own register;" (22 words). EXPLICIT/HIGH |
| added | DEP-01-04-026 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-09-02 | "This slice's native interaction view and scoped request/outcome checks are received by App `DEL-09-02` before its joined request witness," (19 words). EXPLICIT/HIGH |
| refreshed | 13 other ACTIVE rows | | | | LastSeen only |

All ACTIVE quotes are exact substrings of the current ScopeOfWork and at most 30 words. Declared mirrors: 0. The human-owned prefix of `_DEPENDENCIES.md` is byte-identical.

## Validators

- `validate_dependencies_schema.py`: exit 0 — VALID: projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Dependencies.csv /   Columns: 29 (29 required + 0 extension) /   Data rows: 26.
- `validate_enum.py`: 23 invocations, 23 PASS.
- `validate_id_format.sh`: 42 invocations, 42 PASS.
- Parent anchors (ACTIVE IMPLEMENTS_NODE): 1. Local checks: PASS. Warnings: none.

## Comparison with ARC_EFFECT and the accepted register

- **New arcs from this register:** NR-05 DEL-01-04 → DEL-01-03 (admitted), NR-07 → DEL-01-05 (admitted), NR-08 → DEL-04-02 (held), NR-09 → DEL-02-03 (held), NR-4 → DEL-02-04 (held).
- **Expected and produced:** every ledger register row named in the accepted register row above, except as listed below; see Run Notes in `_DEPENDENCIES.md` for the row-by-row account.
- **Expected but missing:** none.
- **Produced but not named in the ledger (non-topological, required by the revised text):** DEP-01-04-019 re-quote (VER-005 revised); DEP-01-04-011/-012 Notes (REQ-008 supplier basis).

## Guards

- Guards (brief; SOW_REVISIONS_A/B "Extraction guards"; Handoff_State next-workflow row; ARC_EFFECT §3), checked graph-wide after the run: R17-10 holds (DEL-01-02 reaches only DEL-01-01, DEL-01-05, DEL-04-01; DEL-01-03 those and DEL-01-02); DEL-04-01 has no supplier; no SCC-002 member depends on DEL-09-06; N-12, N-B8, NR-03, NR-06 and NR-10 are absent; nothing names DEL-11-02.
