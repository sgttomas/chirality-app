# Run Context

| Field | Value |
|---|---|
| **RunID** | EST_DEL-03-02_2026-02-18_1955 |
| **AsOf** | 2026-02-18T19:55:20Z |
| **Scope** | DEL-03-02 |
| **ScopeResolvedSummary** | 1 deliverable in scope; 0 excluded; 0 blocked |
| **BASIS_OF_ESTIMATE** | RATE_TABLE |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv, Level_of_Effort.csv, Assumed_Project_Parameters.csv |
| **DECOMPOSITION_PATH** | _Decomposition/Penhold_PSB_Project_Decomposition_v2.md (v2.3 FINAL) |
| **DEPENDENCY_SOURCES** | AUTO (read DEL-03-02/Dependencies.csv -- 18 rows found) |
| **FALLBACK_POLICY** | STRICT |
| **ALLOW_MIXED_METHODS** | FALSE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | DOLLAR |
| **Warnings** | None |

## Scope Resolution

| DeliverableID | PackageID | Path | InScope | Notes |
|---|---|---|---|---|
| DEL-03-02 | PKG-003 | PKG-003_Design_Brief/1_Working/DEL-03-02_CivilDesignBrief/ | TRUE | Civil Design Brief -- T2 Narrative |

## CBS Mapping Rule

No explicit `CBSHint` was present in the decomposition for DEL-03-02. The following deterministic mapping rule is applied:

- **All design brief narrative deliverables** (PKG-003) are mapped to CBS = `PROF_SERVICES` (professional services -- design team labor for narrative/document production).
- This is consistent with the deliverable type ("Design Brief / Narrative") and the responsible party (Civil Engineer).

## Price Source Resolution

- **Level_of_Effort.csv**: provides estimated hours per role per deliverable. DEL-03-02 has 1 row: R-07 (Civil Engineer Senior) at 10 hours.
- **Professional_Staff_Rates.csv**: provides hourly rates per role. R-07 = $155/hr CAD, Basis = MARKET, Confidence = MEDIUM.
- **Assumed_Project_Parameters.csv**: provides project-level parameters. Not directly used for DEL-03-02 line-item pricing but confirmed for context (PP-09: 12-acre site, PP-10: 4.5 acres developed area).

## Method Note

The `Level_of_Effort.csv` file labels its own basis as "PARAMETRIC" in the `Basis` column (indicating the hours were estimated parametrically). However, the **estimating method applied in this run** is `RATE_TABLE`: hours from Level_of_Effort.csv are multiplied by unit rates from Professional_Staff_Rates.csv to produce priced line items. This is consistent with `BASIS_OF_ESTIMATE = RATE_TABLE` because the pricing mechanism is rate-times-quantity from a rate table. The hour quantities are treated as the best available level-of-effort estimate from the provided sources.
