# DX return — DEL-09-07 Local host candidate qualification

- Node DX (Type 2 TASK, Claude Code subagent launched by the run coordinator; no descendants). Basis commit 1efd4bcda.
- Method: `workflows/dependency-extract/WORKFLOW.md`. MODE UPDATE, STRICTNESS CONSERVATIVE. SOURCE_DOCS `ScopeOfWork.md` only. DECOMPOSITION_PATH `execution/_Decomposition/SOFTWARE_DECOMP.md`.
- Source `ScopeOfWork.md` SHA256 `813ef0f3ebcbc000df3a54093f15a0cfe9b2a75c8f6bb69a6648b1eec8e0395a` (revised by SCA-V4-002 F-0907-01…04). It was not changed.
- Outputs (SHA256):
  - `Dependencies.csv` `9010b0aa3e1c7d1edf8644003ed278224aec4d17200a427b64b8fd2b295d1c78`.
  - `_DEPENDENCIES.md` `1db55615f0f39a6a4aacca5ab744647e1f0e3e1c5d2662592c95d7b2c5365cd0`.
  - Run record `_run_records/dependency-extract-20260929-sca002.md` `04331f7e5e4d82562ceac45995325e9eb5e99a297f652c5fee93d3b891d086a0`.

## Register result

The register holds 25 ACTIVE rows (10 ANCHOR, 15 EXECUTION) and 0 RETIRED, as before the run.

| Change | Row | Class / type | Direction | Target | What changed |
|---|---|---|---|---|---|
| added | none | | | | |
| updated (ASC-ISS-007) | DEP-09-07-016 | EXECUTION / PREREQUISITE | UPSTREAM | EXTERNAL DEP-001 | Notes restated against the revised SoW: complete same-run host-network observation showing requests only to the selected model service and person-allowed destinations, declined requests reaching no destination, every destination contacted recorded and shown, native enforcement evidence; the pre-SCA-V4-001 "candidate/run/configured endpoint" sentence is superseded and marked as history. Statement, quote, type, target, maturity and closure unchanged |
| updated (re-quoted) | DEP-09-07-022 | EXECUTION / CONSTRAINT | UPSTREAM | EXTERNAL OI-001 | Revised TBD-002 (D2 ruling): narrowed to uncovered matters; quote "PRD OQ-02 still requires an examination criterion that depends on such an uncovered operation to await its disposition." |
| updated (re-quoted) | DEP-09-07-023 | EXECUTION / CONSTRAINT | UPSTREAM | EXTERNAL OI-002 | Revised TBD-003 (D3 ruling): narrowed to criteria outside the ruling; quote "a dependent examination criterion outside that ruling is fixed only after its disposition; unrelated verification and definition remain possible." |
| updated | DEP-09-07-020 | EXECUTION / PREREQUISITE | UPSTREAM | EXTERNAL (adopted autonomy policy and run setting) | Notes only |
| refreshed | 21 other rows | | | | LastSeen only |
| retired | none | | | | |

IMPACT §5 expected rows 022 (OI-001) and 023 (OI-002) to lose their quote: both were re-quoted in place because each revised TBD keeps a residual owner-held constraint with a stated point of need (unlike DEL-01-04 TBD-002, whose OI-002 row was retired). All 25 quotes are verbatim. Declared mirrors: 0. The human-owned prefix is byte-identical.

## Validators

- `validate_dependencies_schema.py`: VALID (29 columns, 25 rows).
- `validate_enum.py`: 23 invocations, all PASS.
- `validate_id_format.sh`: 43 invocations, all PASS.
- Local checks: PASS. Warnings: none.

## Comparison with ARC_EFFECT

- ARC_EFFECT §4 lists DEL-09-07 under "Changed bound files, no arc change (evidence drift only)". Produced: no arc change (all changed rows are EXTERNAL). Expected but missing: none. Produced but unexpected: none.

## Guards

- DEL-09-07 is not an SCC-002 member. Its only DEL-09-06 row (DEP-09-07-011) is DEL-09-07 consuming DEL-09-06 (existing, unchanged); no row makes an SCC-002 member depend on DEL-09-06 and DEL-09-06 gains no DOWNSTREAM row. No row to DEL-04-01. Not triggered.
