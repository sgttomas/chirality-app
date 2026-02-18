# Run Context

| Field | Value |
|---|---|
| **RunID** | EST_DEL-10-01_2026-02-18_1900 |
| **AsOf** | 2026-02-18T19:00:00 |
| **Scope** | DEL-10-01 |
| **ScopeResolvedSummary** | 1 deliverable in scope; 0 excluded; 0 blocked |
| **BASIS_OF_ESTIMATE** | RATE_TABLE |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv; Level_of_Effort.csv; Assumed_Project_Parameters.csv |
| **DECOMPOSITION_PATH** | _Decomposition/Penhold_PSB_Project_Decomposition_v2.md (v2.3 FINAL) |
| **DEPENDENCY_SOURCES** | AUTO (read DEL-10-01/Dependencies.csv; 12 rows loaded) |
| **FALLBACK_POLICY** | STRICT |
| **ALLOW_MIXED_METHODS** | FALSE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | DOLLAR |
| **Warnings** | None |

## Resolved Paths

| Source | Resolved Path |
|---|---|
| Professional_Staff_Rates.csv | `_PriceSources/Professional_Staff_Rates.csv` |
| Level_of_Effort.csv | `_PriceSources/Level_of_Effort.csv` |
| Assumed_Project_Parameters.csv | `_PriceSources/Assumed_Project_Parameters.csv` |
| Decomposition | `_Decomposition/Penhold_PSB_Project_Decomposition_v2.md` |
| Dependencies (DEL-10-01) | `PKG-010_.../DEL-10-01_.../Dependencies.csv` |

## CBS Mapping Rule

No explicit `CBSHint` is present in the decomposition for DEL-10-01. CBS is assigned as follows:

| CBS Code | Rule | Rationale |
|---|---|---|
| `PROF-PM` | Project Manager hours on risk register | PM role; management and coordination labor |
| `PROF-CM` | Construction Manager hours on risk register | CM role; construction risk input labor |

This mapping is deterministic: each role's `Category` in Professional_Staff_Rates.csv drives the CBS prefix (`PROF` = professional services), and the role abbreviation suffixes it.

## Pricing Method

Cost = Hours (from Level_of_Effort.csv, filtered to DEL-10-01) x Hourly Rate (from Professional_Staff_Rates.csv, matched on RoleID).

Both sources are local files provided in `PRICE_SOURCES`. `Method = RATE_TABLE` for all line items, consistent with `BASIS_OF_ESTIMATE = RATE_TABLE`.
