# DX return — DEL-01-03 Native plans, tools and delegation views

- Node DX (Type 2 TASK, Claude Code subagent dispatched by the HELP_HUMAN session; no descendants). Basis commit 2d5e6845c5 (SCA-V4-003 REVISE).
- Method: `workflows/dependency-extract/WORKFLOW.md`. MODE UPDATE, STRICTNESS CONSERVATIVE. SOURCE_DOCS `ScopeOfWork.md` only. DECOMPOSITION_PATH `execution/_Decomposition/SOFTWARE_DECOMP.md` (sha256 `983199cc…a70d`).
- Source `ScopeOfWork.md` SHA256 `0056ec198e855080da740e2fb72a3e0a37fcd304c58cca537d4ad56a11c46069` (revised by SCA-V4-003 G-0103-01…11 (10 definitions and AX-004)). It was not changed.
- Accepted register row: `Amendment_Actions.csv` row 3 — ScopeOfWork blocks G-0103-01..G-0103-11 (11) carrying SC3-01-03-1 SC3-01-03-2 SC3-01-03-3 SC3-01-03-4 SC3-01-03-5 SC3-01-03-6 SC3-01-03-7 SC3-01-03-8; register UPDATE rows R3-01-03-a..c R3-01-03-d R3-01-03-e R3-01-03-f.
- Outputs (SHA256):
  - `Dependencies.csv` `8b56b4cf3f6892e9a6700009a63176dc7382ac8ba52994b6a7817522620dc6ad`.
  - `_DEPENDENCIES.md` `c31cbc9dac3512d3cea2739bcd47eac5996f1d9b27f943e36c6665506e55f367`.
  - Run record `_run_records/dependency-extract-20261003-sca003.md` `15c26fc09a7ae3232fb1cd7b0aed8818378110a1eff9288c09b66a3ad43c75c7`.

## Register result

The register holds 22 ACTIVE rows (10 ANCHOR, 12 EXECUTION) and 0 RETIRED. Before the run it held 18 ACTIVE rows.

| Change | Row | Class / type | Direction | Target | Evidence / what changed |
|---|---|---|---|---|---|
| updated | DEP-01-03-011 | EXECUTION / PREREQUISITE | UPSTREAM | DEL-01-01 | fields: Notes |
| updated | DEP-01-03-017 | EXECUTION / CONSTRAINT | UPSTREAM | OI-001;OI-002 | fields: Statement, SourceRef, EvidenceQuote, Notes |
| added | DEP-01-03-019 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-06-01 | "its delegation identities are received by App `DEL-06-01`;" (8 words). EXPLICIT/HIGH |
| added | DEP-01-03-020 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-09-02 | "its views and checks are received by `DEL-09-02` and `DEL-09-05` before their witnesses." (13 words). EXPLICIT/HIGH |
| added | DEP-01-03-021 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-09-05 | "its views and checks are received by `DEL-09-02` and `DEL-09-05` before their witnesses." (13 words). EXPLICIT/HIGH |
| added | DEP-01-03-022 | EXECUTION / INTERFACE | DOWNSTREAM | DEL-01-04 | "This slice's plan-mode element, item anchors and delegation availability are received by App `DEL-01-04`, which composes turns and request cards from them;" (22 words). EXPLICIT/HIGH |
| refreshed | 16 other ACTIVE rows | | | | LastSeen only |

All ACTIVE quotes are exact substrings of the current ScopeOfWork and at most 30 words. Declared mirrors: 0. The human-owned prefix of `_DEPENDENCIES.md` is byte-identical.

## Validators

- `validate_dependencies_schema.py`: exit 0 — VALID: projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-03_Native plans, tools and delegation views/Dependencies.csv /   Columns: 29 (29 required + 0 extension) /   Data rows: 22.
- `validate_enum.py`: 23 invocations, 23 PASS.
- `validate_id_format.sh`: 34 invocations, 34 PASS.
- Parent anchors (ACTIVE IMPLEMENTS_NODE): 1. Local checks: PASS. Warnings: none.

## Comparison with ARC_EFFECT and the accepted register

- **New arcs from this register:** none (supplier-side mirror of NR-05 only).
- **Expected and produced:** every ledger register row named in the accepted register row above, except as listed below; see Run Notes in `_DEPENDENCIES.md` for the row-by-row account.
- **Expected but missing:** none.
- **Produced but not named in the ledger (non-topological, required by the revised text):** none.

## Guards

- Guards (brief; SOW_REVISIONS_A/B "Extraction guards"; Handoff_State next-workflow row; ARC_EFFECT §3), checked graph-wide after the run: R17-10 holds (DEL-01-02 reaches only DEL-01-01, DEL-01-05, DEL-04-01; DEL-01-03 those and DEL-01-02); DEL-04-01 has no supplier; no SCC-002 member depends on DEL-09-06; N-12, N-B8, NR-03, NR-06 and NR-10 are absent; nothing names DEL-11-02.
