# Source Index — EST_DEL-02-04_2026-02-18_1130

## Indexed Price Sources

### S-01: Structural_Concrete_Rates.csv
- **Path:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_PriceSources/Structural_Concrete_Rates.csv
- **Source Type:** Rate Table
- **Items Used:** SC-01 through SC-15
- **Parsing Notes:** Standard CSV; 15 line items with RateMin/RateMax/RecommendedRate columns. Unit rates include supply and placement (all-in rates).
- **Supports:** Foundation systems (spread footings SC-12, strip footings SC-13, screw piles SC-14), concrete slabs (SC-03, SC-04), formwork (SC-05, SC-06), reinforcing steel (SC-07), structural steel (SC-08, SC-09), roof framing (SC-10, SC-11), anchor bolts (SC-15).
- **Cannot Support:** Envelope cladding, glazing, doors, interior finishes.

### S-02: Building_Envelope_Rates.csv
- **Path:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_PriceSources/Building_Envelope_Rates.csv
- **Source Type:** Rate Table
- **Items Used:** BE-01 through BE-15
- **Parsing Notes:** Standard CSV; 15 line items. Rates are supply + install.
- **Supports:** Insulated metal wall panels (BE-01), metal cladding (BE-02), masonry base (BE-03), insulated roof panels (BE-04), insulation (BE-06, BE-07), air/vapour barrier (BE-08), glazing (BE-09, BE-10), hollow metal doors (BE-11, BE-12), hardware (BE-13), sealant (BE-14), flashing (BE-15).
- **Cannot Support:** Structural systems, interior finishes, overhead doors (car-wash grade).

### S-03: Interior_Architectural_Rates.csv
- **Path:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_PriceSources/Interior_Architectural_Rates.csv
- **Source Type:** Rate Table
- **Items Used:** IA-08
- **Parsing Notes:** Standard CSV; 25 line items. Only IA-08 (sealed concrete floor) is applicable to DEL-02-04 scope.
- **Supports:** Sealed concrete flooring for office/shared areas (IA-08).
- **Cannot Support:** Structural, envelope, or door systems. Interior partitions and finishes are DEL-02-01 scope.

### S-04: Mechanical_System_Rates.csv
- **Path:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_PriceSources/Mechanical_System_Rates.csv
- **Source Type:** Rate Table
- **Items Used:** None directly (sump assemblies are DEL-02-05)
- **Parsing Notes:** Standard CSV; 14 line items.
- **Supports:** Reference only. MS-10 (bay sump assembly) informs sump rough-in cost estimation but the assembly cost belongs to DEL-02-05.
- **Cannot Support:** DEL-02-04 scope items directly, except informational reference for sump rough-in.

### S-05: Electrical_System_Rates.csv
- **Path:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_PriceSources/Electrical_System_Rates.csv
- **Source Type:** Rate Table
- **Items Used:** None
- **Parsing Notes:** Standard CSV; 14 line items. Electrical scope is DEL-02-06.
- **Cannot Support:** DEL-02-04 scope.

### S-06: Equipment_Pricing.csv
- **Path:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_PriceSources/Equipment_Pricing.csv
- **Source Type:** Rate Table (equipment unit pricing)
- **Items Used:** EQ-01
- **Parsing Notes:** Standard CSV; 15 line items. EQ-01 provides overhead door pricing for main building (car-wash grade, 16x16, motorized, insulated, with windows).
- **Supports:** 8 overhead doors for main building bays (EQ-01 at $20,000 each).
- **Cannot Support:** Structural systems, envelope cladding, or design fees. Note: EQ-10 (bay sump assembly) is DEL-02-05 cost.

### S-07: Professional_Design_Fees.csv
- **Path:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_PriceSources/Professional_Design_Fees.csv
- **Source Type:** Rate Table (percentage-based fee structure)
- **Items Used:** DF-03
- **Parsing Notes:** Standard CSV; 8 line items. Fee percentages applied to construction cost of the applicable discipline scope.
- **Supports:** Structural engineering design fee (DF-03: 2.5% of structural construction cost).
- **Cannot Support:** Architectural fees (applied at PKG level), or other discipline fees outside DEL-02-04 scope.

### S-08: Construction_Labour_Rates.csv
- **Path:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_PriceSources/Construction_Labour_Rates.csv
- **Source Type:** Rate Table (labour reference)
- **Items Used:** Reference only (labour costs are embedded in all-in unit rates from other sources)
- **Parsing Notes:** Standard CSV; 15 trade rates. Fully burdened hourly rates for Alberta.
- **Supports:** Reference/validation of embedded labour in unit rates.
- **Cannot Support:** Direct pricing (unit rates in other sources are all-in including labour).

### S-09: Assumed_Project_Parameters.csv
- **Path:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_PriceSources/Assumed_Project_Parameters.csv
- **Source Type:** Parameters (quantities and areas)
- **Items Used:** PP-05, PP-07, PP-11, PP-12, PP-13, PP-18, PP-21
- **Parsing Notes:** Standard CSV; 29 parameters.
- **Supports:** Building area (PP-05: 18,000 sf), overhead door count (PP-13: 8), bay sump count (PP-18: 8), bay counts (PP-11: 4 fire, PP-12: 4 PW). PP-21 provides rough construction value ($6.6M for main PSB) used to cross-check design fee calculation.
- **Cannot Support:** Detailed dimensional quantities (lengths, heights, perimeters) which are derived assumptions.

## Sources Not Used (Excluded per Brief)

- All files under `_Estimates/`, `_Aggregation/`, `_Reconciliation/`, `_Archive/` are excluded per brief EXCLUSIONS.
