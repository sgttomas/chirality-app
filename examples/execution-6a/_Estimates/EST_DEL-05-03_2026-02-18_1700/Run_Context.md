# Run Context -- EST_DEL-05-03_2026-02-18_1700

## Identifiers

- **RunID:** EST_DEL-05-03_2026-02-18_1700
- **AsOf:** 2026-02-18T17:00:00-07:00
- **Agent:** ESTIMATING (Type 2)

## Brief Inputs (resolved)

| Field | Value |
|---|---|
| **Scope** | DEL-05-03 only (PKG-005) |
| **ScopeResolvedSummary** | 1 deliverable in scope; 0 excluded; 0 blocked |
| **BASIS_OF_ESTIMATE** | QUOTE (validated enum) |
| **CURRENCY** | CAD |
| **FALLBACK_POLICY** | ALLOW_ALLOWANCE |
| **ALLOW_MIXED_METHODS** | TRUE |
| **ROUNDING** | DOLLAR |
| **UPDATE_LATEST_POINTER** | FALSE |
| **OUTPUT_LABEL** | DEL-05-03 |

## Resolved Paths

| Input | Resolved Path | Status |
|---|---|---|
| **RUN_ROOT** | `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a` | EXISTS |
| **ESTIMATES_ROOT** | `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_Estimates/` | EXISTS |
| **DECOMPOSITION_PATH** | `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_Decomposition/Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md` | LOADED |
| **DEPENDENCY_SOURCES** | AUTO -- read `Dependencies.csv` from DEL-05-03 deliverable folder | LOADED (9 rows; 2 ANCHOR + 7 EXECUTION) |
| **PRICE_SOURCES[0]** | `_PriceSources/Optional_Items_Pricing.csv` | LOADED (19 rows) |
| **PRICE_SOURCES[1]** | `_PriceSources/Assumed_Project_Parameters.csv` | LOADED (29 rows) |

## Scope Resolution

| DeliverableID | PackageID | Path | InScope | Notes |
|---|---|---|---|---|
| DEL-05-03_Optional-Access-Control | PKG-005 | `PKG-005_Optional Priced Items & Owner-Elected Additions/1_Working/DEL-05-03_Option - Access Control/` | TRUE | Optional priced item; covers SOW-0502 |

## Basis-of-Estimate Resolution

- **Declared basis:** QUOTE
- **Actual method used:** PARAMETRIC (fallback)
- **Reason for fallback:** Brief explicitly states "No vendor quote exists. Use parametric pricing from Optional_Items_Pricing.csv." FALLBACK_POLICY=ALLOW_ALLOWANCE and ALLOW_MIXED_METHODS=TRUE permit fallback to PARAMETRIC.
- **Fallback logged in:** Decision_Log.md (DEC-RUN-001)

## CBS Mapping Rule

No explicit `CBSHint` is present in the decomposition for DEL-05-03. CBS is assigned deterministically as follows:
- Access control equipment and system = `26 05 00` (Electronic Access Control and Intrusion Detection) per UniFormat II convention
- Installation labor is bundled into the system price per OPT-06/OPT-07 (lump sum inclusive)

## Warnings

- [WARNING] BASIS_MISMATCH: Declared QUOTE but no vendor quotes exist; all lines priced as PARAMETRIC per fallback policy.
- [WARNING] QUANTITY_TBD: Number of controlled zones/doors is assumed at 10 per PP-28; actual count depends on DEL-02-01 floor plan (DEP-05-03-003).
- [WARNING] LOW_CONFIDENCE: All price source lines for AccessControl category are rated LOW confidence.
