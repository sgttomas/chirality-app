# Run Context

## Run Identity

- **RunID:** EST_DEL-05-02_2026-02-18_1600
- **AsOf:** 2026-02-18T16:00:00-07:00
- **Agent:** ESTIMATING (Type 2)

## Brief Inputs (resolved)

| Field | Value |
|---|---|
| **Scope** | DEL-05-02 (Option -- Yard Lighting Per Light), PKG-005 |
| **ScopeResolvedSummary** | 1 deliverable in scope; 0 excluded; 0 blocked |
| **BASIS_OF_ESTIMATE** | RATE_TABLE (validated) |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | (1) `_PriceSources/Optional_Items_Pricing.csv`; (2) `_PriceSources/Assumed_Project_Parameters.csv` |
| **DECOMPOSITION_PATH** | `_Decomposition/Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md` (loaded) |
| **DEPENDENCY_SOURCES** | AUTO -- loaded `Dependencies.csv` from DEL-05-02 working folder |
| **FALLBACK_POLICY** | STRICT |
| **ALLOW_MIXED_METHODS** | FALSE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | DOLLAR |
| **OUTPUT_LABEL** | DEL-05-02 |

## Scope Resolution

| DeliverableID | PackageID | Path | InScope | Notes |
|---|---|---|---|---|
| DEL-05-02 | PKG-005 | `PKG-005_.../1_Working/DEL-05-02_Option - Yard Lighting (Per Light)/` | TRUE | Optional priced item; unit rate per light |

## CBS Mapping Rule

No explicit `CBSHint` is present in the decomposition for DEL-05-02. CBS codes are assigned deterministically as follows:

- **26-ELEC** -- Electrical: yard lighting pole/fixture/base/wiring (CSI Division 26 -- Electrical)
- **26-COND** -- Electrical: conduit run from panel to first pole (CSI Division 26 -- Electrical, underground conduit)

These CBS codes are derived from CSI MasterFormat Division 26 (Electrical) as the most appropriate classification for exterior site lighting scope.

## Warnings

- Price source `Optional_Items_Pricing.csv` tags its values with `Basis=PARAMETRIC` (indicating how the source rates were developed). This run consumes those rates as a RATE_TABLE for pricing purposes. See Decision_Log.md DEC-EST-001.
- Quantity of yard light poles is ASSUMED at 12 per PP-20 (LOW confidence). Actual quantity depends on site layout from DEL-03-01 (not yet finalized).
- Conduit run length from panel to first pole is ASSUMED at 100 lm based on brief statement that fence line is approximately 100 m from nearest structure. Actual length TBD pending site plan.
