# Run Context

## Run Identity

| Field | Value |
|---|---|
| **RunID** | EST_DEL-05-07_2026-02-18_2200 |
| **AsOf** | 2026-02-18T22:00:00-07:00 |
| **Agent** | ESTIMATING (Type 2 Task Agent) |

## Inputs (as provided)

| Field | Value |
|---|---|
| **Scope** | DEL-05-07 only (PKG-005) |
| **ScopeResolvedSummary** | 1 deliverable in scope; 0 excluded; 0 blocked |
| **BASIS_OF_ESTIMATE** | ALLOWANCE |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | `_PriceSources/Optional_Items_Pricing.csv` (row OPT-18); `_PriceSources/Assumed_Project_Parameters.csv` |
| **DECOMPOSITION_PATH** | `_Decomposition/Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md` |
| **DEPENDENCY_SOURCES** | AUTO (read `DEL-05-07/Dependencies.csv`) |
| **FALLBACK_POLICY** | STRICT |
| **ALLOW_MIXED_METHODS** | FALSE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | DOLLAR |
| **OUTPUT_LABEL** | DEL-05-07 |

## Resolved Paths

| Item | Resolved Path |
|---|---|
| ESTIMATES_ROOT | `{RUN_ROOT}/_Estimates/` |
| Snapshot folder | `_Estimates/EST_DEL-05-07_2026-02-18_2200/` |
| Decomposition | `_Decomposition/Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md` |
| Price source 1 | `_PriceSources/Optional_Items_Pricing.csv` |
| Price source 2 | `_PriceSources/Assumed_Project_Parameters.csv` |
| Dependency source | `PKG-005_.../1_Working/DEL-05-07_.../Dependencies.csv` |

## Scope Resolution

| DeliverableID | PackageID | Path | InScope | Notes |
|---|---|---|---|---|
| DEL-05-07_Optional-FFandE-Allowance | PKG-005 | PKG-005_.../1_Working/DEL-05-07_Cash Allowance - FF&E (20k DB-allocated)/ | TRUE | Fixed $20,000 CAD cash allowance per DEC-005 |

## CBS Mapping Rule

CBS code `FF&E` assigned to DEL-05-07 based on the following deterministic rule:
- Deliverable type is a fixed cash allowance for furniture, fixtures, and equipment.
- No explicit `CBSHint` was present in the decomposition for this deliverable.
- CBS code `FF&E` is derived from the deliverable name and scope item category (SOW-0506, OPT-18 category = "FF&E").

## Warnings

None.
