# Source Index

## Pricing Sources Used

### 1. Optional_Items_Pricing.csv

- **Path:** `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_PriceSources/Optional_Items_Pricing.csv`
- **Source Type:** Parametric pricing table (treated as quote-equivalent retail pricing per DEC-EST-001)
- **Rows Used:** OPT-12 through OPT-17 (6 rows; all Appliances category)
- **Parsing Notes:** CSV with columns ItemID, Category, Description, Unit, PriceMin, PriceMax, RecommendedPrice, Basis, Confidence, Notes. Used `RecommendedPrice` column for all line items.
- **What it supports:** Complete appliance list pricing (equipment + installation) for DEL-05-06.
- **What it cannot support:** Vendor-specific quotes, delivery charges (not itemized), sales tax, or brand-specific pricing.

### 2. Assumed_Project_Parameters.csv

- **Path:** `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_PriceSources/Assumed_Project_Parameters.csv`
- **Source Type:** Project parameters (quantities, areas, durations)
- **Rows Used:** None directly for pricing. Used indirectly to confirm no conflicting quantity assumptions.
- **What it supports:** Confirms general project context (building areas, bay counts, etc.).
- **What it cannot support:** Not a pricing source; no unit rates or amounts used from this file.

## Dependency Sources Used

### 3. Dependencies.csv (DEL-05-06)

- **Path:** `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/PKG-005_Optional Priced Items & Owner-Elected Additions/1_Working/DEL-05-06_Option - Appliances & Laundry/Dependencies.csv`
- **Source Type:** Dependency register (v3.1 schema; 10 rows)
- **Usage:** Blocker/readiness analysis only. Not used for pricing.
- **Key findings:** No unresolved blockers that prevent estimating. Scope boundary with DEL-05-07 (FF&E) is clear. Base building rough-in (DEL-02-05, DEL-02-06) is upstream interface but does not affect price.

## Decomposition Source

### 4. Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md

- **Path:** `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_Decomposition/Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md`
- **Source Type:** Project decomposition (stable IDs)
- **Usage:** Confirmed DEL-05-06 identity, scope mapping (SOW-0505), package assignment (PKG-005), and objective linkage (OBJ-010).
