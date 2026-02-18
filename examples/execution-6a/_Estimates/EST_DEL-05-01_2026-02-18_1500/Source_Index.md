# Source Index

## Pricing Sources

### Source 1: Optional_Items_Pricing.csv

| Field | Value |
|---|---|
| **Path** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_PriceSources/Optional_Items_Pricing.csv |
| **Source Type** | Parametric budget estimates (range-based; no formal model) |
| **Format** | CSV with columns: ItemID, Category, Description, Unit, PriceMin, PriceMax, RecommendedPrice, Basis, Confidence, Notes |
| **Relevant Rows** | OPT-01 (wash bay system), OPT-02 (plumbing/drainage), OPT-03 (environmental compliance) |
| **Supports** | All 3 line items in Detail.csv |
| **Cannot Support** | Does not provide vendor-quoted prices (all rows self-report as PARAMETRIC with LOW confidence). Does not resolve AEP regulatory requirements. |
| **Parsing Notes** | Clean CSV; 19 data rows total; 3 rows (OPT-01 through OPT-03) relevant to wash bay (Category=WashBay). All wash bay rows have Confidence=LOW. |

### Source 2: Assumed_Project_Parameters.csv

| Field | Value |
|---|---|
| **Path** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_PriceSources/Assumed_Project_Parameters.csv |
| **Source Type** | Project parameters and assumptions |
| **Format** | CSV with columns: ParameterID, Category, Parameter, Value, Unit, Source, Confidence, Notes |
| **Relevant Rows** | PP-12 (PW shop bays = 4 each, confirms one bay available for wash bay conversion) |
| **Supports** | Contextual validation only (confirms 4 PW bays, one potentially replaced by wash bay per SOW-0500) |
| **Cannot Support** | Does not provide pricing data for wash bay scope |
| **Parsing Notes** | Clean CSV; 29 data rows. Used for context/validation only, not pricing. |

## Dependency Source

| Field | Value |
|---|---|
| **Path** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/PKG-005_Optional Priced Items & Owner-Elected Additions/1_Working/DEL-05-01_Option - Built-in Wash Bay/Dependencies.csv |
| **Source Type** | Dependency register (schema v3.1) |
| **Relevant Rows** | 11 dependency rows (2 ANCHOR, 9 EXECUTION class) |
| **Used For** | Blocker/readiness identification only (not pricing evidence) |

## Decomposition Source

| Field | Value |
|---|---|
| **Path** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_Decomposition/Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md |
| **Version** | v1.0 (Phase 7 Published) |
| **Used For** | Package/deliverable ID validation, scope item confirmation (SOW-0500 -> PKG-005 / DEL-05-01) |
