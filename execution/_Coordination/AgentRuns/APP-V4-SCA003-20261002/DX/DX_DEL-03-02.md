# DX return — DEL-03-02 Proposal, validation and outcome contract

- Node DX (Type 2 TASK, Claude Code subagent dispatched by the HELP_HUMAN session; no descendants). Basis commit 2d5e6845c5 (SCA-V4-003 REVISE).
- Method: `workflows/dependency-extract/WORKFLOW.md`. MODE UPDATE, STRICTNESS CONSERVATIVE. SOURCE_DOCS `ScopeOfWork.md` only. DECOMPOSITION_PATH `execution/_Decomposition/SOFTWARE_DECOMP.md` (sha256 `983199cc…a70d`).
- Source `ScopeOfWork.md` SHA256 `e2f8d49de699fd661988cdbe73c340d7b8aaef0dc14d1b8d5732a57e1be5a21f` (revised by SCA-V4-003 G-0302-01…04 (OUT-001, CLM-004, AX-005)). It was not changed.
- Accepted register row: `Amendment_Actions.csv` row 11 — ScopeOfWork blocks G-0302-01..G-0302-04 (4) carrying S-02-1 S-02-2 P1-07; register UPDATE rows R-02-1 R-02-2 R-02-3.
- Outputs (SHA256):
  - `Dependencies.csv` `20904d9eef8db1f28a2a8e3b1865ae6f8d14faab50e2fdda19b8161b2a4292f3`.
  - `_DEPENDENCIES.md` `dc4c8c57aa2a3b878cc1c837fdc8e724be3ced9cae991b33f88d4ae3fc76e908`.
  - Run record `_run_records/dependency-extract-20261003-sca003.md` `cb1b66681184fa69cde664f1d6545c08dbadf87067e5eabc1c39766341ff92c8`.

## Register result

The register holds 34 ACTIVE rows (15 ANCHOR, 19 EXECUTION) and 0 RETIRED. Before the run it held 27 ACTIVE rows.

| Change | Row | Class / type | Direction | Target | Evidence / what changed |
|---|---|---|---|---|---|
| added | DEP-03-02-028 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-02-01 | "Its proposal, validation and outcome meanings are also received by `DEL-02-01` and `DEL-02-03` (item dispositions and content identities for checkpoint subjects)," (21 words). EXPLICIT/HIGH |
| added | DEP-03-02-029 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-02-03 | "Its proposal, validation and outcome meanings are also received by `DEL-02-01` and `DEL-02-03` (item dispositions and content identities for checkpoint subjects)," (21 words). EXPLICIT/HIGH |
| added | DEP-03-02-030 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-05-01 | "`DEL-05-01` (the loop boundary), `DEL-05-02` (panel receiving), `DEL-09-06` (the connected activity) and `DEL-10-03` (the shared account), each of which declares it upstream in its own register." (26 words). EXPLICIT/HIGH |
| added | DEP-03-02-031 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-05-02 | "`DEL-05-01` (the loop boundary), `DEL-05-02` (panel receiving), `DEL-09-06` (the connected activity) and `DEL-10-03` (the shared account), each of which declares it upstream in its own register." (26 words). EXPLICIT/HIGH |
| added | DEP-03-02-032 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-09-06 | "`DEL-05-01` (the loop boundary), `DEL-05-02` (panel receiving), `DEL-09-06` (the connected activity) and `DEL-10-03` (the shared account), each of which declares it upstream in its own register." (26 words). EXPLICIT/HIGH |
| added | DEP-03-02-033 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-10-03 | "`DEL-05-01` (the loop boundary), `DEL-05-02` (panel receiving), `DEL-09-06` (the connected activity) and `DEL-10-03` (the shared account), each of which declares it upstream in its own register." (26 words). EXPLICIT/HIGH |
| added | DEP-03-02-034 | EXECUTION / INTERFACE | UPSTREAM | DEL-04-02 | "It consumes `DEL-04-02`'s visible autonomy state (grant display states, grant value and scope, settings version identities) for origin and standing at drafting." (22 words). EXPLICIT/HIGH |
| refreshed | 27 other ACTIVE rows | | | | LastSeen only |

All ACTIVE quotes are exact substrings of the current ScopeOfWork and at most 30 words. Declared mirrors: 0. The human-owned prefix of `_DEPENDENCIES.md` is byte-identical.

## Validators

- `validate_dependencies_schema.py`: exit 0 — VALID: projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-02_Proposal, validation and outcome contract/Dependencies.csv /   Columns: 29 (29 required + 0 extension) /   Data rows: 34.
- `validate_enum.py`: 22 invocations, 22 PASS.
- `validate_id_format.sh`: 54 invocations, 54 PASS.
- Parent anchors (ACTIVE IMPLEMENTS_NODE): 1. Local checks: PASS. Warnings: none.

## Comparison with ARC_EFFECT and the accepted register

- **New arcs from this register:** none.
- **Expected and produced:** every ledger register row named in the accepted register row above, except as listed below; see Run Notes in `_DEPENDENCIES.md` for the row-by-row account.
- **Expected but missing:** R-02-1: DOWNSTREAM row to DEL-03-01 — not grounded (DEL-03-01 named only as supplier); arc carried by DEP-03-01-026.
- **Produced but not named in the ledger (non-topological, required by the revised text):** none.

## Guards

- Guards (brief; SOW_REVISIONS_A/B "Extraction guards"; Handoff_State next-workflow row; ARC_EFFECT §3), checked graph-wide after the run: R17-10 holds (DEL-01-02 reaches only DEL-01-01, DEL-01-05, DEL-04-01; DEL-01-03 those and DEL-01-02); DEL-04-01 has no supplier; no SCC-002 member depends on DEL-09-06; N-12, N-B8, NR-03, NR-06 and NR-10 are absent; nothing names DEL-11-02.
