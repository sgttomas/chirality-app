# Source Index: EST_DEL-03-02_2026-02-18_1130

## Price Sources

### 1. Earthwork_Civil_Rates.csv (PRIMARY)

| Field | Value |
|---|---|
| Path | _PriceSources/Earthwork_Civil_Rates.csv |
| Type | Rate table |
| Format | CSV; 11 line items (EC-01 through EC-11) |
| Parsing notes | All rates are RecommendedRate values in CAD. Columns: ItemID, Category, Description, Unit, RateMin, RateMax, RecommendedRate, Basis, Confidence, Notes |
| Supports | Clearing (EC-01), stripping (EC-02), excavation (EC-03), engineered fill (EC-04), building pad prep (EC-05), compaction (EC-06), erosion control (EC-07), drainage swales (EC-08), topsoil/seeding (EC-09), geotech investigation (EC-10), construction survey (EC-11) |
| Cannot support | Stormwater retention pond construction (no specific pond line item; pond priced via drainage swale rate + earthwork rates); pavement; utilities |

### 2. Assumed_Project_Parameters.csv (QUANTITY BASIS)

| Field | Value |
|---|---|
| Path | _PriceSources/Assumed_Project_Parameters.csv |
| Type | Parametric assumptions |
| Format | CSV; 29 parameters (PP-01 through PP-29) |
| Parsing notes | Provides area, quantity, and financial assumptions. Key items used: PP-05 (main building 18,000 sf), PP-07 (cold storage 6,000 sf), PP-09 (12 acres total), PP-10 (4.5 acres developed), PP-23 (site/civil estimated value $1,800,000) |
| Supports | Quantity derivations for clearing area, stripping volume, building pad area, earthwork volumes, drainage lengths, seeding area |
| Cannot support | Direct pricing (provides quantities only, not rates) |

### 3. Professional_Design_Fees.csv (CIVIL DESIGN)

| Field | Value |
|---|---|
| Path | _PriceSources/Professional_Design_Fees.csv |
| Type | Fee schedule |
| Format | CSV; 8 entries (DF-01 through DF-08) |
| Parsing notes | DF-02 provides civil engineering design fee as percentage of site/civil construction cost (2.0%–3.0%, recommended 2.5%) |
| Supports | Civil design fee for DEL-03-02 earthworks/drainage scope |
| Cannot support | Other discipline fees (architectural, structural, mechanical, electrical belong to other deliverables) |

### 4. Construction_Labour_Rates.csv (REFERENCE)

| Field | Value |
|---|---|
| Path | _PriceSources/Construction_Labour_Rates.csv |
| Type | Rate table |
| Format | CSV; 15 trade rates (T-01 through T-15) |
| Parsing notes | Key rates: T-08 Heavy Equipment Operator $75/hr, T-09 Light Equipment Operator $65/hr, T-15 Surveyor $69/hr. Used for validation only -- earthwork rates in Earthwork_Civil_Rates.csv are all-in unit rates that include labour. |
| Supports | Validation cross-check of earthwork rate table reasonableness |
| Cannot support | Direct pricing (earthwork rates are all-in composites) |

### 5. Paving_Surfacing_Rates.csv (NOT USED)

| Field | Value |
|---|---|
| Path | _PriceSources/Paving_Surfacing_Rates.csv |
| Type | Rate table |
| Not used | Pavement construction belongs to DEL-03-03 per cost ownership rules |

### 6. Underground_Utility_Rates.csv (NOT USED)

| Field | Value |
|---|---|
| Path | _PriceSources/Underground_Utility_Rates.csv |
| Type | Rate table |
| Not used | On-site utility distribution belongs to DEL-03-04 per cost ownership rules |

### 7. Fees_Permits_Insurance.csv (NOT USED)

| Field | Value |
|---|---|
| Path | _PriceSources/Fees_Permits_Insurance.csv |
| Type | Rate table |
| Not used | Environmental consultant fees belong to DEL-03-05; permits/bonds/insurance belong to PKG-001. No line items applicable to DEL-03-02. |

## Deliverable Documents (Read-Only Context)

| Document | Path | Used For |
|---|---|---|
| Datasheet.md | DEL-03-02 folder | Soil stratigraphy, earthworks parameters, drainage parameters, site conditions |
| Specification.md | DEL-03-02 folder | Requirements (REQ-3201 through REQ-3218), scope boundaries |
| _CONTEXT.md | DEL-03-02 folder | Deliverable identity and description |
| Dependencies.csv | DEL-03-02 folder | Blocker identification (DEP-0302-004, DEP-0302-005) |

## Decomposition (Read-Only Context)

| Document | Path | Used For |
|---|---|---|
| Decomposition FINAL v1.0 | _Decomposition/ folder | Package/deliverable IDs, scope item mapping, objective linkage |
