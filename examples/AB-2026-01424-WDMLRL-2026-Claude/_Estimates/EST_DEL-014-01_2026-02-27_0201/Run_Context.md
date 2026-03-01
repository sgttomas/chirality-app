# Run_Context.md

## Run Identity

| Field | Value |
|---|---|
| RunID | EST_DEL-014-01_2026-02-27_0201 |
| AsOf | 2026-02-27T09:01:32Z |
| Scope | DEL-014-01 |
| ScopeResolvedSummary | 1 deliverable (DEL-014-01: 50,000L Cistern & Distribution) in PKG-014 (Plumbing & Water Systems Installation) |
| BASIS_OF_ESTIMATE | PARAMETRIC |
| CURRENCY | CAD |
| FALLBACK_POLICY | ALLOW_PARAMETRIC |
| ALLOW_MIXED_METHODS | TRUE |
| UPDATE_LATEST_POINTER | FALSE |
| Rounding | NONE |
| OUTPUT_LABEL | DEL-014-01 |

## Resolved Paths

| Input | Resolved Path |
|---|---|
| RUN_ROOT | /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude |
| ESTIMATES_ROOT | {RUN_ROOT}/_Estimates |
| DECOMPOSITION_PATH | {RUN_ROOT}/_Decomposition/WDMLRL_Decomposition_Claude.md |
| DELIVERABLE_PATH | {RUN_ROOT}/PKG-014_Plumbing & Water Systems Installation/1_Working/DEL-014-01_Cistern |

## PRICE_SOURCES (resolved)

| PS-ID | File | Status |
|---|---|---|
| PS-STAFF | Professional_Staff_Rates.csv | OK — 25 roles loaded |
| PS-LOE | Level_of_Effort.csv | OK — 6 rows for DEL-014-01 |
| PS-PARAMS | Assumed_Project_Parameters.csv | OK — 19 parameters loaded |
| PS-UU | Underground_Utility_Rates.csv | OK — 5 items loaded; UU-05 directly applicable (cistern supply+set) |
| PS-LAB | Construction_Labour_Rates.csv | OK — 10 trades loaded; T-05 (Plumber) directly applicable |
| PS-EQ | Equipment_Pricing.csv | OK — 3 items loaded; EQ-02 (pressure washer) tangentially relevant |

## Warnings

- [WARNING] Tank type (above-grade vs below-grade) is TBD in Datasheet; cistern pricing based on UU-05 allowance which does not differentiate.
- [WARNING] Tank material (HDPE, concrete, fiberglass, steel) is TBD; affects pricing accuracy.
- [WARNING] Pump type, motor power, and electrical requirements are TBD; pump pricing is parametric estimate.
- [WARNING] Freeze protection requirements are TBD; parametric allowance applied.
- [WARNING] Pipe material and routing lengths are TBD; distribution piping estimated parametrically.
- [WARNING] Backflow prevention device type TBD; parametric allowance applied.
- [WARNING] Overflow mechanism specifics TBD; parametric allowance applied.
- [WARNING] Water quality classification (potable vs non-potable) unresolved; may affect scope and cost.
