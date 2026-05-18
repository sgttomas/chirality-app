# Source Index -- EST_DEL-05-03_2026-02-18_1700

## Price Sources

### Source 1: Optional_Items_Pricing.csv

- **Path:** `_PriceSources/Optional_Items_Pricing.csv`
- **Type:** PARAMETRIC (parametric pricing table)
- **Format:** CSV, 19 rows, 10 columns
- **Relevant rows for DEL-05-03:**
  - **OPT-06** (AccessControl): Access control system (10-zone; main building) -- system -- RecommendedPrice $45,000 CAD -- Range $35,000-$55,000 -- PARAMETRIC, LOW confidence
  - **OPT-07** (AccessControl): Access control per additional zone (above 10) -- each -- RecommendedPrice $3,200 CAD -- Range $2,500-$4,000 -- PARAMETRIC, LOW confidence
- **Parsing notes:** Clean CSV; no encoding issues. ItemID field is unique. All prices appear to be in CAD (consistent with project currency).
- **What it supports:** Parametric pricing for access control system (base 10-zone) and per-zone incremental cost.
- **What it cannot support:** Does not provide vendor-specific quotes; does not confirm actual zone count; does not break down equipment vs. labor vs. software licensing.

### Source 2: Assumed_Project_Parameters.csv

- **Path:** `_PriceSources/Assumed_Project_Parameters.csv`
- **Type:** PARAMETRIC (project parameter assumptions)
- **Format:** CSV, 29 rows, 8 columns
- **Relevant rows for DEL-05-03:**
  - **PP-28**: Controlled access zones (if optional elected) = 10 each -- ASSUMPTION, LOW confidence
- **Parsing notes:** Clean CSV; no encoding issues.
- **What it supports:** Assumed quantity of controlled zones (10) for pricing calculation.
- **What it cannot support:** Does not confirm actual zone count (depends on DEL-02-01 floor plan).

## Dependency Evidence (read-only; not a pricing source)

- **Path:** `PKG-005_Optional Priced Items & Owner-Elected Additions/1_Working/DEL-05-03_Option - Access Control/Dependencies.csv`
- **Used for:** Blocker/readiness identification only (not unit rate evidence).
- **Key upstream blockers identified:**
  - DEP-05-03-003: Requires DEL-02-01 floor plan for zone mapping (PREREQUISITE)
  - DEP-05-03-004: Requires DEL-02-06 coordination for low-voltage power, conduit, network (INTERFACE)
