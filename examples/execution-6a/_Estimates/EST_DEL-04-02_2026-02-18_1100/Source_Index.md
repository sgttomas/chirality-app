# Source Index — EST_DEL-04-02_2026-02-18_1100

## Price Sources

### 1. Structural_Concrete_Rates.csv
- **Path:** _PriceSources/Structural_Concrete_Rates.csv
- **Type:** Rate Table
- **Items:** 16 line items (SC-01 through SC-15 plus anchors)
- **Supports:** Concrete aprons at overhead door openings (SC-04: heavy-duty slab-on-grade 200mm reinforced at $108/m2 recommended)
- **Cannot support:** Door pricing, hardware, weatherstripping
- **Parsing notes:** CSV with headers; columns include ItemID, Category, Description, Unit, RateMin, RateMax, RecommendedRate, Basis, Confidence, Notes

### 2. Building_Envelope_Rates.csv
- **Path:** _PriceSources/Building_Envelope_Rates.csv
- **Type:** Rate Table
- **Items:** 15 line items (BE-01 through BE-15)
- **Supports:** Person doors (BE-11: $1,800/each), door hardware sets (BE-13: $600/each), perimeter sealant/weatherstripping (BE-14: $16/lm), metal flashing and trim (BE-15: $32/lm)
- **Cannot support:** Overhead door pricing (use Equipment_Pricing.csv for overhead doors)
- **Parsing notes:** CSV with headers; same column structure as concrete rates

### 3. Equipment_Pricing.csv
- **Path:** _PriceSources/Equipment_Pricing.csv
- **Type:** Rate Table (equipment-level pricing)
- **Items:** 15 line items (EQ-01 through EQ-15)
- **Supports:** Overhead doors for cold storage (EQ-02: standard grade 16x16, motorized, insulated, windows at $13,500/each recommended; quantity 2 assumed)
- **Cannot support:** Person doors, concrete aprons, weatherstripping
- **Parsing notes:** CSV with headers; columns include PriceMin, PriceMax, RecommendedPrice, Quantity_Assumed
- **Note:** EQ-02 description explicitly states "Cold storage building: 2 doors; standard duty" -- direct match to DEL-04-02 scope

### 4. Construction_Labour_Rates.csv
- **Path:** _PriceSources/Construction_Labour_Rates.csv
- **Type:** Rate Table (labour rates)
- **Items:** 15 trades (T-01 through T-15)
- **Supports:** Installation labour for doors, hardware, concrete work. Key trades: T-02 Carpenter ($72/hr burdened) for door installation; T-04 Concrete Finisher ($68/hr burdened) for apron work; T-01 General Labourer ($55/hr burdened)
- **Cannot support:** Material pricing directly
- **Parsing notes:** CSV with headers; rates are fully burdened (includes benefits/WCB/overhead)

### 5. Assumed_Project_Parameters.csv
- **Path:** _PriceSources/Assumed_Project_Parameters.csv
- **Type:** Project Parameters (quantities and assumptions)
- **Items:** 29 parameters (PP-01 through PP-29)
- **Supports:** Confirms cold storage overhead door quantity = 2 (PP-14), cold storage footprint = 6,000 sf (PP-07), cold storage construction value parametric = $290,000 (PP-22)
- **Cannot support:** Direct unit pricing
- **Parsing notes:** CSV with headers; includes ParameterID, Category, Parameter, Value, Unit, Source, Confidence, Notes

## Dependency Sources

### Dependencies.csv (DEL-04-02)
- **Path:** DEL-04-02 folder / Dependencies.csv
- **Type:** Dependency Register (v3.1 schema)
- **Items:** 9 dependency rows (DEP-0402-A01 through DEP-0402-E09)
- **Used for:** Blocker detection and readiness assessment (NOT for pricing)
- **Key blockers identified:** None that prevent estimating; all dependencies are design-phase coordination items
