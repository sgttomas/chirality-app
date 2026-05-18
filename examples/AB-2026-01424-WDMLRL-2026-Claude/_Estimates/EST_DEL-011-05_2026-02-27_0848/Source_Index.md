# Source Index

## Indexed Pricing Sources

| # | Source File | Source Type | Parsing Notes | Supports |
|---|---|---|---|---|
| PS-01 | PriceSources/Professional_Staff_Rates.csv | PARAMETRIC (rate table) | 25 rows; RoleID R-01 through R-25; HourlyRate_CAD column; all MEDIUM confidence | Professional staff hourly rates for management, design, construction, admin, specialty roles |
| PS-02 | PriceSources/Level_of_Effort.csv | PARAMETRIC (hours model) | Multi-row per deliverable; keyed by DeliverableID + RoleID; EstimatedHours column | Estimated hours per role per deliverable; DEL-011-05 has 6 rows (R-01, R-02, R-03, R-05, R-06, R-08) |
| PS-03 | PriceSources/Assumed_Project_Parameters.csv | PARAMETRIC (parameters) | 19 rows; project identity, location, schedule, facility dimensions, equipment counts, currency | Building dimensions (13,000 sqft, 35 ft ceiling), equipment (2x 5-ton cranes), cistern (50,000L), currency (CAD) |
| PS-04 | PriceSources/Structural_Concrete_Rates.csv | PARAMETRIC (rate table) | 8 items (SC-01 through SC-08); includes concrete, rebar, formwork, walls, stairs, embedded plates | Unit rates for concrete slab (m2), grade beam (m), footing concrete (m3), rebar (kg), formwork (m2), embedded plates (each) |
| PS-05 | PriceSources/Building_Envelope_Rates.csv | PARAMETRIC (rate table) | 6 items (BE-01 through BE-06); walls, roof, doors, flashing, glazing | Unit rates for insulated metal panels (m2), overhead doors (each), man doors (each), flashing (LS), windows (m2) |
| PS-06 | PriceSources/Construction_Labour_Rates.csv | PARAMETRIC (rate table) | 10 trades (T-01 through T-10); HourlyRate + BurdenMultiplier + FullyBurdenedRate_CAD | Fully burdened trade rates for carpenter, concrete finisher, ironworker, electrician, plumber, HVAC, operator, labourer, painter, drywaller |
| PS-07 | PriceSources/Equipment_Pricing.csv | ALLOWANCE (equipment pricing) | 3 items (EQ-01 through EQ-03); cranes, pressure washer, air compressor | Only EQ-02 (pressure washer) is wash-bay-related but is a building-wide equipment item — NOT included in this deliverable scope |

## Coverage Assessment

- **Well-supported**: Concrete work (slab, grade beam, rebar, formwork, embedded plates) via PS-04; Envelope work (walls, roof, overhead door, flashing) via PS-05; Construction labour via PS-06; Professional staff via PS-01 + PS-02.
- **Partially supported**: Mezzanine structural provisions, drainage slope formwork, gantry provisions — no specific rate; priced as PARAMETRIC allowances derived from comparable items.
- **Not supported**: Specific steel plate dimensions/grades (TBD in documents); wall construction material type (TBD); overhead door height (TBD).
