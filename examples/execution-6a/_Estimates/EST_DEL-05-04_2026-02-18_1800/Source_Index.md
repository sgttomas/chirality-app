# Source Index

## Indexed Price Sources

### Source 1: Optional_Items_Pricing.csv

- **Path:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_PriceSources/Optional_Items_Pricing.csv
- **Type:** Parametric pricing table
- **Format:** CSV, 19 rows (header + 18 data rows)
- **Relevant rows for DEL-05-04:**
  - **OPT-08** (Security category): Camera system (16 cameras; NVR; network) -- system price, RecommendedPrice=$50,000 CAD, range $40,000-$60,000, PARAMETRIC basis, LOW confidence
  - **OPT-09** (Security category): Monitoring service (annual) -- per year, RecommendedPrice=$5,400 CAD, range $3,600-$7,200, PARAMETRIC basis, LOW confidence
- **Parsing notes:** Clean CSV; all fields populated; prices are in CAD (implicit from project context).
- **What it supports:** Parametric pricing for camera system installation and annual monitoring -- the two cost categories required by RFP for DEL-05-04.
- **What it cannot support:** No vendor quote data; no detailed bill of materials; no site-specific camera placement quantities.

### Source 2: Assumed_Project_Parameters.csv

- **Path:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_PriceSources/Assumed_Project_Parameters.csv
- **Type:** Project parameter table (quantities, areas, durations, financial assumptions)
- **Format:** CSV, 30 rows (header + 29 data rows)
- **Relevant rows for DEL-05-04:**
  - **PP-29**: Security camera locations = 16 each, ASSUMPTION, LOW confidence. Breakdown: Exterior (8) + interior common areas (4) + apparatus bays (2) + entrances (2).
- **Parsing notes:** Clean CSV; all fields populated.
- **What it supports:** Assumed camera count underlying OPT-08 system pricing.
- **What it cannot support:** Not a pricing source per se; provides quantity assumptions only. Does not substitute for a vendor quote or site-specific design.

## Sources NOT Used (excluded per brief)

- Prior estimate snapshots under `_Estimates/` -- excluded per non-recursion invariant.
- Deliverable working files -- read-only for dependency context; not used as pricing evidence.

## Source Coverage Assessment

- Both line items (L-0504-01, L-0504-02) have traceable source references to `Optional_Items_Pricing.csv`.
- Provenance completeness: **100%** (2/2 lines have non-TBD SourceRef).
- Quality caveat: All source prices are PARAMETRIC with LOW confidence. No vendor quotes available.
