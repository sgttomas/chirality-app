# DX return — DEL-04-01 Operation-policy and human-act distinctions

- Node DX (Type 2 TASK, Claude Code subagent dispatched by the HELP_HUMAN session; no descendants). Basis commit 2d5e6845c5 (SCA-V4-003 REVISE).
- Method: `workflows/dependency-extract/WORKFLOW.md`. MODE UPDATE, STRICTNESS CONSERVATIVE. SOURCE_DOCS `ScopeOfWork.md` only. DECOMPOSITION_PATH `execution/_Decomposition/SOFTWARE_DECOMP.md` (sha256 `983199cc…a70d`).
- Source `ScopeOfWork.md` SHA256 `2cd1dc9e542a9ee38ee0dd2a217bd717ecd960b2df009f59b4b2c562d350d862` (revised by SCA-V4-003 G-0401-01…04 (CLM-002, REQ-002; added TBD-005, AX-006)). It was not changed.
- Accepted register row: `Amendment_Actions.csv` row 14 — ScopeOfWork blocks G-0401-01..G-0401-04 (4) carrying SC2-04-01-1 SC2-04-01-3 SC2-04-01-4; register UPDATE rows R2-04-01-a R2-04-01-c R-03-2 RP1-MX-0401.
- Outputs (SHA256):
  - `Dependencies.csv` `bde049827079db9afa16a46a3a752a1f9cfbd92156655502553cbe421fa986c9`.
  - `_DEPENDENCIES.md` `5b7749437b88653e2f89a702ee0c3ac31d5c18fb40dd2a4c6263049f23fc148e`.
  - Run record `_run_records/dependency-extract-20261003-sca003.md` `7faca28ea60779697077a8b87d07050f4ede9b1eeff56dbca3700b772dbd7a5d`.

## Register result

The register holds 33 ACTIVE rows (11 ANCHOR, 22 EXECUTION) and 0 RETIRED. Before the run it held 29 ACTIVE rows.

| Change | Row | Class / type | Direction | Target | Evidence / what changed |
|---|---|---|---|---|---|
| updated | DEP-04-01-022 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-03-02 | fields: SourceRef, EvidenceQuote, Notes |
| updated | DEP-04-01-023 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-03-03 | fields: SourceRef, EvidenceQuote, Notes |
| updated | DEP-04-01-024 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-03-04 | fields: SourceRef, EvidenceQuote, Notes |
| updated | DEP-04-01-025 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-05-01 | fields: SourceRef, EvidenceQuote, Notes |
| updated | DEP-04-01-026 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-05-02 | fields: SourceRef, EvidenceQuote, Notes |
| updated | DEP-04-01-027 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-09-09 | fields: SourceRef, EvidenceQuote, Notes |
| added | DEP-04-01-030 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-09-06 | "It also supplies policy meaning to App v4 `DEL-03-02`, `DEL-03-03`, `DEL-03-04`, `DEL-05-01`, `DEL-05-02`, `DEL-09-06` and `DEL-09-09`, each of which declares it upstream in its own register." (26 words). EXPLICIT/HIGH |
| added | DEP-04-01-031 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-02-02 | "This contract supplies that distinction to App v4 `DEL-02-02`, whose registration it governs (`DEL-02-02/REQ-002`, `DEL-02-02/AC-006`), and to `DEL-01-04`, whose App act control captures it" (24 words). EXPLICIT/HIGH |
| added | DEP-04-01-032 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-01-04 | "This contract supplies that distinction to App v4 `DEL-02-02`, whose registration it governs (`DEL-02-02/REQ-002`, `DEL-02-02/AC-006`), and to `DEL-01-04`, whose App act control captures it" (24 words). EXPLICIT/HIGH |
| added | DEP-04-01-033 | EXECUTION / CONSTRAINT | UPSTREAM | Owner with the host policy owner — adopted consequence vocab | "The consequence dimension of operation classes (REQ-001, OUT-002) has no adopted vocabulary." (12 words). EXPLICIT/HIGH |
| refreshed | 23 other ACTIVE rows | | | | LastSeen only |

All ACTIVE quotes are exact substrings of the current ScopeOfWork and at most 30 words. Declared mirrors: 0. The human-owned prefix of `_DEPENDENCIES.md` is byte-identical.

## Validators

- `validate_dependencies_schema.py`: exit 0 — VALID: projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-01_Operation-policy and human-act distinctions/Dependencies.csv /   Columns: 29 (29 required + 0 extension) /   Data rows: 33.
- `validate_enum.py`: 21 invocations, 21 PASS.
- `validate_id_format.sh`: 54 invocations, 54 PASS.
- Parent anchors (ACTIVE IMPLEMENTS_NODE): 1. Local checks: PASS. Warnings: none.

## Comparison with ARC_EFFECT and the accepted register

- **New arcs from this register:** none.
- **Expected and produced:** every ledger register row named in the accepted register row above, except as listed below; see Run Notes in `_DEPENDENCIES.md` for the row-by-row account.
- **Expected but missing:** none.
- **Produced but not named in the ledger (non-topological, required by the revised text):** DEP-04-01-022…027 re-quotes (supply sentence now names DEL-09-06).

## Guards

- Guards (brief; SOW_REVISIONS_A/B "Extraction guards"; Handoff_State next-workflow row; ARC_EFFECT §3), checked graph-wide after the run: R17-10 holds (DEL-01-02 reaches only DEL-01-01, DEL-01-05, DEL-04-01; DEL-01-03 those and DEL-01-02); DEL-04-01 has no supplier; no SCC-002 member depends on DEL-09-06; N-12, N-B8, NR-03, NR-06 and NR-10 are absent; nothing names DEL-11-02.
