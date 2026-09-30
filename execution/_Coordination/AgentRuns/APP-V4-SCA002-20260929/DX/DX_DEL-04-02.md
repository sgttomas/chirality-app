# DX return — DEL-04-02 Visible autonomy and result standing

- Node DX (Type 2 TASK, Claude Code subagent launched by the run coordinator; no descendants). Basis commit 1efd4bcda.
- Method: `workflows/dependency-extract/WORKFLOW.md`. MODE UPDATE, STRICTNESS CONSERVATIVE. SOURCE_DOCS `ScopeOfWork.md` only. DECOMPOSITION_PATH `execution/_Decomposition/SOFTWARE_DECOMP.md`.
- Source `ScopeOfWork.md` SHA256 `f16ffa8a33cbfb2e78a8e916e90aff9fb44ad20adf94fe61a559a213f5564460` (revised by SCA-V4-002 F-0402-01/F-0402-02, Q-6 accepted). It was not changed.
- Outputs (SHA256):
  - `Dependencies.csv` `05ffc9c7b274b464ed26709e1c54f536c65704ce7c0b9f6febe2c399a47bcb44`.
  - `_DEPENDENCIES.md` `273ce8247920fa927378fd36159dcda4ad2ac62b118c25d4dd6a683a7198689f`.
  - Run record `_run_records/dependency-extract-20260929-sca002.md` `95ac5b780c57bd71805f61924c25e5e245c13993715965cab4e743db63868ba9`.

## Register result

The register holds 25 ACTIVE rows (6 ANCHOR, 19 EXECUTION) and 0 RETIRED, as before the run.

| Change | Rows | What changed |
|---|---|---|
| added | none | |
| re-quoted (ASC-ISS-008) | DEP-04-02-011, -012, -015, -016, -017, -018, -019, -020, -021, -022, -023 | EvidenceQuote now carries the SoW's inline-code backticks (for example `` App v4 `DEL-03-02` ``). Notes record the re-quote. 015–017 are exactly 30 words |
| re-quoted (ASC-ISS-008) | DEP-04-02-025 | EvidenceQuote now carries the SoW's bold markers: `**Owner:** the owner, when a workflow needs enforced checkpoints. **Point of need:** before hold-display fixtures run.` |
| updated | DEP-04-02-007 (UPSTREAM PREREQUISITE DEL-04-01) | SourceRef/Notes only, for the revised CLM-004 (rulings D2/D3; residual matters with the Owner with App/SWB contract owners; OI-021 additions already carried by DEP-04-02-024) |
| refreshed | 12 other rows | LastSeen only |
| retired | none | |

All 12 listed by V12 F1 for this register (011, 012, 015–023, 025) are done; all 25 ACTIVE quotes are now exact substrings of the SoW. Declared mirrors: 0. The human-owned prefix is byte-identical.

## Validators

- `validate_dependencies_schema.py`: VALID (29 columns, 25 rows).
- `validate_enum.py`: 22 invocations, all PASS.
- `validate_id_format.sh`: 43 invocations, all PASS.
- Local checks: PASS (including verbatim-quote check on every ACTIVE row). Warnings: none.

## Comparison with ARC_EFFECT

- ARC_EFFECT §4: "the registers of DEL-04-01, DEL-04-02 and DEL-04-03, re-quoted exactly (ASC-ISS-008; V12 F1: 34 quotes). Their arcs do not change", and DEL-04-02 changes bytes for the Q-6 text edit. Produced: 12 re-quotes, no arc change. Expected but missing: none. Produced but unexpected: none.

## Guards

- No row on DEL-09-06. N-12 and N-B8 do not involve this register. The DOWNSTREAM rows 019–023 supply DEL-05-01, DEL-05-02, DEL-03-02, DEL-03-03 and DEL-02-03 (existing arcs N-05/N-07 family); no DOWNSTREAM row to DEL-04-01, so DEL-04-01 gains no supplier. Not triggered.
