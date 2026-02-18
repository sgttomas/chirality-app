# Source Index — EST_DEL-06-01_2026-02-18_1400

## Price Sources Used

| Source # | File | Source Type | Items Used | Supports |
|----------|------|-------------|-----------|----------|
| PS-1 | Professional_Staff_Rates.csv | RATE_TABLE | R-21 (Commissioning Lead, $140/hr), R-02 (Project Manager, $175/hr) | Hourly rates for all line items |
| PS-2 | Level_of_Effort.csv | RATE_TABLE (hours) | DEL-06-01/R-21 (16 hrs), DEL-06-01/R-02 (6 hrs) | Quantity (hours) for all line items |
| PS-3 | Assumed_Project_Parameters.csv | PARAMETRIC (context) | PP-04 (proposal preparation: 6 weeks) | Context for coordination overhead; not directly priced |

## Source Details

### PS-1: Professional_Staff_Rates.csv

- **Path:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_PriceSources/Professional_Staff_Rates.csv
- **Type:** Market-based hourly rate table (Alberta 2024)
- **Confidence:** MEDIUM (+/-20-30%)
- **Roles used for DEL-06-01:**
  - R-21 Commissioning Lead: $140/hr CAD (Category: Construction)
  - R-02 Project Manager: $175/hr CAD (Category: Management)
- **Parsing notes:** 30 roles defined; 2 applicable to DEL-06-01

### PS-2: Level_of_Effort.csv

- **Path:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_PriceSources/Level_of_Effort.csv
- **Type:** Planning-level effort estimates (hours per role per deliverable)
- **Confidence:** MEDIUM (+/-20-30%)
- **Rows used for DEL-06-01:**
  - Row 50: DEL-06-01, R-21 Commissioning Lead, 16 hours (PARAMETRIC basis)
  - Row 51: DEL-06-01, R-02 Project Manager, 6 hours (PARAMETRIC basis)
- **Parsing notes:** 65 rows total across 21 deliverables; 2 rows for DEL-06-01. LOE notes state "Consolidated: commissioning + training + closeout + deficiencies + warranty all in one DEL; more than any single 6b DEL-08-xx"

### PS-3: Assumed_Project_Parameters.csv

- **Path:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_PriceSources/Assumed_Project_Parameters.csv
- **Type:** Project-level parameters (context and calibration)
- **Confidence:** MEDIUM
- **Used for:** Context only (PP-04 proposal timeline = 6 weeks). Not directly referenced in any line item pricing.

## Dependency Evidence (read-only, not pricing)

| Source | Path | Usage |
|--------|------|-------|
| Dependencies.csv (DEL-06-01) | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/PKG-07_Commissioning, Closeout & Warranty/1_Working/DEL-06-01_CommissioningTrainingCloseoutWarrantyNarrative/Dependencies.csv | Blocker/readiness assessment only; not used for pricing |

## Sources NOT Used (in PRICE_SOURCES but not applicable to DEL-06-01)

- No construction pricing files needed (DEL-06-01 is pure proposal production cost)
- No Fees_Permits_Insurance.csv needed (no bond/insurance content in this deliverable)

---

**END OF SOURCE INDEX**
