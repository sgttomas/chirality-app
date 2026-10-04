# DX return — DEL-02-03 Workflow execution compatibility and round-trip support

- Node DX (Type 2 TASK, Claude Code subagent dispatched by the HELP_HUMAN session; no descendants). Basis commit 2d5e6845c5 (SCA-V4-003 REVISE).
- Method: `workflows/dependency-extract/WORKFLOW.md`. MODE UPDATE, STRICTNESS CONSERVATIVE. SOURCE_DOCS `ScopeOfWork.md` only. DECOMPOSITION_PATH `execution/_Decomposition/SOFTWARE_DECOMP.md` (sha256 `983199cc…a70d`).
- Source `ScopeOfWork.md` SHA256 `625b299ec1d48de1b80dff74796774cc95ee466870bec06a196e16b840af6e5f` (revised by SCA-V4-003 G-0203-01…13 (Purpose first sentence, SOW-052 row, CLM-002, CLM-003, REQ-002, REQ-007, AC-002, VER-002, VER-006, TBD-006, AX-006)). It was not changed.
- Accepted register row: `Amendment_Actions.csv` row 8 — ScopeOfWork blocks G-0203-01..G-0203-13 (13) carrying SC2-02-03-1 SC2-02-03-2 SC2-02-03-3 SC2-02-03-4 SC2-02-03-5 SC2-02-03-6 P1-01; register UPDATE rows R2-02-03-a R2-02-03-b..i R2-02-03-j NR-01 SC3-02-02-9 RP1-MX-0203.
- Outputs (SHA256):
  - `Dependencies.csv` `a80b1e31a963a437f9edab021a065e9f86bea9328b86d9d981c654e53c428549`.
  - `_DEPENDENCIES.md` `c1e32e57f6567bafbd49a54cb543f56eb1fdae4c55eaa103000ddfd200d22ad9`.
  - Run record `_run_records/dependency-extract-20261003-sca003.md` `0688ef0693b1eff73b07f496537e8fd09e7eb23ac09b6a84f65fa3f6d4634f00`.

## Register result

The register holds 38 ACTIVE rows (8 ANCHOR, 30 EXECUTION) and 2 RETIRED. Before the run it held 25 ACTIVE rows.

| Change | Row | Class / type | Direction | Target | Evidence / what changed |
|---|---|---|---|---|---|
| updated | DEP-02-03-003 | ANCHOR / OTHER | UPSTREAM | SOW-052 | fields: SourceRef, EvidenceQuote, Notes |
| updated | DEP-02-03-010 | EXECUTION / INTERFACE | UPSTREAM | DEL-02-02 | fields: Statement, Notes |
| updated | DEP-02-03-025 | EXECUTION / INTERFACE | UPSTREAM | DEL-03-02 | fields: EvidenceQuote, Notes |
| updated | DEP-02-03-027 | EXECUTION / INTERFACE | UPSTREAM | DEL-01-04 | fields: Statement, SourceRef, EvidenceQuote, Notes |
| added | DEP-02-03-028 | EXECUTION / INTERFACE | UPSTREAM | DEL-01-02 | "`DEL-01-02`'s custody events (observation lost and recovered, App-restart interruption) and its run-reference tag and look-up," (15 words). EXPLICIT/HIGH |
| added | DEP-02-03-029 | EXECUTION / INTERFACE | UPSTREAM | DEL-04-02 | "`DEL-04-02`'s grant display states (including *set by person, not yet confirmed*, *unconfirmed* and *refused*), for recording A12 checkpoints (REQ-002, REQ-003);" (20 words). EXPLICIT/HIGH |
| added | DEP-02-03-030 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-02-01 | "This slice's report, recording meanings and transfer contract are received by `DEL-02-01`, `DEL-02-02`, `DEL-03-03`, `DEL-03-04`, `DEL-04-02`, `DEL-04-03`, `DEL-05-01`, `DEL-05-02`," (19 words). EXPLICIT/HIGH |
| added | DEP-02-03-031 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-02-02 | "This slice's report, recording meanings and transfer contract are received by `DEL-02-01`, `DEL-02-02`, `DEL-03-03`, `DEL-03-04`, `DEL-04-02`, `DEL-04-03`, `DEL-05-01`, `DEL-05-02`," (19 words). EXPLICIT/HIGH |
| added | DEP-02-03-032 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-03-03 | "This slice's report, recording meanings and transfer contract are received by `DEL-02-01`, `DEL-02-02`, `DEL-03-03`, `DEL-03-04`, `DEL-04-02`, `DEL-04-03`, `DEL-05-01`, `DEL-05-02`," (19 words). EXPLICIT/HIGH |
| added | DEP-02-03-033 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-03-04 | "This slice's report, recording meanings and transfer contract are received by `DEL-02-01`, `DEL-02-02`, `DEL-03-03`, `DEL-03-04`, `DEL-04-02`, `DEL-04-03`, `DEL-05-01`, `DEL-05-02`," (19 words). EXPLICIT/HIGH |
| added | DEP-02-03-034 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-04-02 | "This slice's report, recording meanings and transfer contract are received by `DEL-02-01`, `DEL-02-02`, `DEL-03-03`, `DEL-03-04`, `DEL-04-02`, `DEL-04-03`, `DEL-05-01`, `DEL-05-02`," (19 words). EXPLICIT/HIGH |
| added | DEP-02-03-035 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-04-03 | "This slice's report, recording meanings and transfer contract are received by `DEL-02-01`, `DEL-02-02`, `DEL-03-03`, `DEL-03-04`, `DEL-04-02`, `DEL-04-03`, `DEL-05-01`, `DEL-05-02`," (19 words). EXPLICIT/HIGH |
| added | DEP-02-03-036 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-05-01 | "This slice's report, recording meanings and transfer contract are received by `DEL-02-01`, `DEL-02-02`, `DEL-03-03`, `DEL-03-04`, `DEL-04-02`, `DEL-04-03`, `DEL-05-01`, `DEL-05-02`," (19 words). EXPLICIT/HIGH |
| added | DEP-02-03-037 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-05-02 | "This slice's report, recording meanings and transfer contract are received by `DEL-02-01`, `DEL-02-02`, `DEL-03-03`, `DEL-03-04`, `DEL-04-02`, `DEL-04-03`, `DEL-05-01`, `DEL-05-02`," (19 words). EXPLICIT/HIGH |
| added | DEP-02-03-038 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-09-02 | "`DEL-09-02`, `DEL-09-06`, `DEL-09-09` and `DEL-10-03`, each of which declares it upstream in its own register." (15 words). EXPLICIT/HIGH |
| added | DEP-02-03-039 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-09-09 | "`DEL-09-02`, `DEL-09-06`, `DEL-09-09` and `DEL-10-03`, each of which declares it upstream in its own register." (15 words). EXPLICIT/HIGH |
| added | DEP-02-03-040 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-10-03 | "`DEL-09-02`, `DEL-09-06`, `DEL-09-09` and `DEL-10-03`, each of which declares it upstream in its own register." (15 words). EXPLICIT/HIGH |
| refreshed | 21 other ACTIVE rows | | | | LastSeen only |

All ACTIVE quotes are exact substrings of the current ScopeOfWork and at most 30 words. Declared mirrors: 0. The human-owned prefix of `_DEPENDENCIES.md` is byte-identical.

## Validators

- `validate_dependencies_schema.py`: exit 0 — VALID: projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-03_Workflow execution compatibility and round-trip support/Dependencies.csv /   Columns: 29 (29 required + 0 extension) /   Data rows: 40.
- `validate_enum.py`: 25 invocations, 25 PASS.
- `validate_id_format.sh`: 66 invocations, 66 PASS.
- Parent anchors (ACTIVE IMPLEMENTS_NODE): 1. Local checks: PASS. Warnings: none.

## Comparison with ARC_EFFECT and the accepted register

- **New arcs from this register:** NR-01 DEL-02-03 → DEL-01-02 (admitted).
- **Expected and produced:** every ledger register row named in the accepted register row above, except as listed below; see Run Notes in `_DEPENDENCIES.md` for the row-by-row account.
- **Expected but missing:** none.
- **Produced but not named in the ledger (non-topological, required by the revised text):** DEP-02-03-025 re-quote (sentence opening moved); DEP-02-03-003 anchor re-quote (SOW-052 row reworded).

## Guards

- Guards (brief; SOW_REVISIONS_A/B "Extraction guards"; Handoff_State next-workflow row; ARC_EFFECT §3), checked graph-wide after the run: R17-10 holds (DEL-01-02 reaches only DEL-01-01, DEL-01-05, DEL-04-01; DEL-01-03 those and DEL-01-02); DEL-04-01 has no supplier; no SCC-002 member depends on DEL-09-06; N-12, N-B8, NR-03, NR-06 and NR-10 are absent; nothing names DEL-11-02.
