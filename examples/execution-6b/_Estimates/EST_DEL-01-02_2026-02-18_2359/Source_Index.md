# Source Index -- DEL-01-02

**RunID:** EST_DEL-01-02_2026-02-18_2359

---

## Price Sources

| # | Source Path | Source Type | Parsing Notes | Supports |
|---|---|---|---|---|
| 1 | `_PriceSources/Professional_Staff_Rates.csv` | Rate Table | 30 roles with RoleID, Role, Category, HourlyRate_CAD, Basis, Confidence. All rates MARKET basis, MEDIUM confidence. | Hourly rates for R-22 ($105/hr) and R-02 ($175/hr) used in DEL-01-02 pricing |
| 2 | `_PriceSources/Level_of_Effort.csv` | Level of Effort (hours by role by deliverable) | 73 rows across 38 deliverables. Basis = PARAMETRIC. DEL-01-02 has 2 rows. | Hours for R-22 (16h) and R-02 (4h) for DEL-01-02 |
| 3 | `_PriceSources/Assumed_Project_Parameters.csv` | Project Parameters | 29 parameters covering duration, area, quantities, financial estimates. | Context only for DEL-01-02; no direct pricing impact |

## Decomposition Source

| Source Path | Version | Status |
|---|---|---|
| `_Decomposition/Penhold_PSB_Project_Decomposition_v2.md` | v2.3 FINAL | Accepted basis for WBS IDs, package/deliverable mapping, scope item linkages |

## Dependency Source

| Source Path | Schema | Row Count |
|---|---|---|
| `DEL-01-02_FormalSubmissionPackage/Dependencies.csv` | v3.1 | 18 dependencies (4 ANCHOR, 14 EXECUTION) |

## Source Limitations

- Rate table rates are MARKET basis with MEDIUM confidence; no firm-specific rate cards provided.
- Level of effort hours are PARAMETRIC basis; represent professional judgment estimates, not actuals.
- No prior project actuals or historical data provided for benchmarking.
