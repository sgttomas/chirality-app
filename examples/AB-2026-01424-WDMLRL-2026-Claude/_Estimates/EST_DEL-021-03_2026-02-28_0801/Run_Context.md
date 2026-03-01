# Run Context

| Field | Value |
|---|---|
| RunID | EST_DEL-021-03_2026-02-28_0801 |
| AsOf | 2026-02-28T08:01:00-07:00 |
| Scope | DEL-021-03 (Insurance Package) |
| ScopeResolvedSummary | 1 deliverable in PKG-021 (Bonding, Insurance & Warranty) |
| BASIS_OF_ESTIMATE | PARAMETRIC |
| CURRENCY | CAD |
| PRICE_SOURCES | Professional_Staff_Rates.csv, Level_of_Effort.csv, Assumed_Project_Parameters.csv, Fees_Permits_Insurance.csv |
| DECOMPOSITION_PATH | _Decomposition/WDMLRL_Decomposition_Claude.md |
| FALLBACK_POLICY | ALLOW_PARAMETRIC |
| ALLOW_MIXED_METHODS | TRUE |
| UPDATE_LATEST_POINTER | FALSE |
| Rounding | NONE |
| OUTPUT_LABEL | DEL-021-03 |
| PriorRunID | EST_DEL-021-03_2026-02-26_2233 |
| Warnings | None |

## Resolved Defaults

- RUN_ROOT: `/Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude`
- ESTIMATES_ROOT: `/Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/_Estimates`
- Snapshot path: `_Estimates/EST_DEL-021-03_2026-02-28_0801/`

## Documents Read

| Document | Status |
|---|---|
| _CONTEXT.md | Read |
| Datasheet.md | Read |
| Specification.md | Read |
| Guidance.md | Read |
| Procedure.md | Read |
| Decomposition | Read (DEL-021-03 section, PKG-021, SOW-0102, SOW-0103) |
| Prior snapshot Detail.csv | Read (EST_DEL-021-03_2026-02-26_2233) |

## Re-run Context

This is a re-run of the DEL-021-03 estimate. The prior run (EST_DEL-021-03_2026-02-26_2233) left 3 insurance premium lines as TBD because no pricing data was available for WCB, E&O, and Employer's Liability coverages. Since that run, rows FP-06, FP-07, and FP-08 have been added to Fees_Permits_Insurance.csv, providing parametric recommended rates for these coverages. This re-run resolves all 3 TBD lines.
