# Source Index

## Price Sources

| # | Source Path | Type | Parsing Notes | Supports |
|---|---|---|---|---|
| 1 | `_PriceSources/Optional_Items_Pricing.csv` | ALLOWANCE (row OPT-18) | CSV; 19 rows (header + 18 data rows). Row OPT-18 directly provides the FF&E cash allowance value. | DEL-05-07: fixed $20,000 CAD allowance (OPT-18). Confidence=HIGH. Basis=ALLOWANCE. |
| 2 | `_PriceSources/Assumed_Project_Parameters.csv` | PROJECT PARAMETERS | CSV; 29 rows (header + 28 data rows). Contains assumed project parameters (area, duration, quantities, financial estimates). | Context only for DEL-05-07. No direct pricing data used from this file for this deliverable. |

## Decomposition Source

| Source Path | Role |
|---|---|
| `_Decomposition/Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md` | Provides stable IDs: PKG-005, DEL-05-07_Optional-FFandE-Allowance, SOW-0506. Provides DEC-005 (FF&E = $20k cash allowance). |

## Dependency Source

| Source Path | Role |
|---|---|
| `DEL-05-07/Dependencies.csv` | 4 dependency rows (2 anchors, 2 execution). Used for blocker/readiness assessment. No pricing evidence derived from dependencies. |

## Key Evidence Linkage

| Evidence | Source | Detail |
|---|---|---|
| $20,000 fixed amount | `Optional_Items_Pricing.csv` row OPT-18 | `PriceMin=20000, PriceMax=20000, RecommendedPrice=20000, Basis=ALLOWANCE, Confidence=HIGH` |
| DEC-005 decision | Decomposition, Decision Log | "FF&E: treat as $20,000 cash allowance; DB allocates within allowance." |
| SOW-0506 scope | Decomposition, SSOW | "FF&E to be treated as a cash allowance of $20,000 (not included in base price); DB to allocate and manage within allowance." |
| Addendum 03 s1.18 | Dependencies.csv DEP-0507-E001 | "FF&E can be included as an additional item in the proposal but should not be included in the base costs." |
