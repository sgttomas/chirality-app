# TOOL POLICY — scc-resolution-case

## Tool Posture

Reasoning-first case organization. No deterministic helper is required to author case files.

## Preferred Validation

After case creation or update, run:

```sh
python3 tools/validation/validate_scc_resolution_case.py <case-folder>
```

Do not claim validator PASS unless it actually ran and passed.

## Disallowed Tool Effects

- No writes outside `CASE_PATH` and scoped `_run_records/`.
- No mutation of product deliverables.
- No mutation of `Dependencies.csv`.
- No mutation of `_ScopeChange/`, `_Reconciliation/`, or decomposition authority.

