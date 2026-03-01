# Source Index — EST_DEL-011-01_2026-02-27_0845

## Pricing Sources

| # | Source File | Source Type | Parsing Notes | Supports |
|---|---|---|---|---|
| 1 | `PriceSources/Professional_Staff_Rates.csv` | RATE_TABLE | 25 roles with hourly rates in CAD; PARAMETRIC basis | Professional staff line items (ITM-022 through ITM-027) |
| 2 | `PriceSources/Level_of_Effort.csv` | PARAMETRIC | Hours by deliverable x role; DEL-011-01 has 6 role entries totalling 38 hours | Quantity basis for professional staff hours |
| 3 | `PriceSources/Assumed_Project_Parameters.csv` | PARAMETRIC | 19 project parameters including building dimensions, crane count, cistern size | Quantity derivation for building footprint (PP-10: ~13000 sqft), ceiling height (PP-11: 35 ft), cranes (PP-12: 2 EA), cistern (PP-14: 50000L) |
| 4 | `PriceSources/Structural_Concrete_Rates.csv` | RATE_TABLE | 8 concrete/rebar/formwork items with min/max/recommended rates in CAD | Concrete slab (SC-01), grade beam (SC-02), footings (SC-03), rebar (SC-04), formwork (SC-05), CIP walls (SC-06), stairs (SC-07), embedded plates (SC-08) |
| 5 | `PriceSources/Building_Envelope_Rates.csv` | RATE_TABLE | 6 envelope items with min/max/recommended rates in CAD | Wall panels (BE-01), roof panels (BE-02), overhead doors (BE-03 context), man doors (BE-04), flashing (BE-05), windows (BE-06) |
| 6 | `PriceSources/Construction_Labour_Rates.csv` | RATE_TABLE | 10 trades with base + burdened rates in CAD | Carpenter (T-01), concrete finisher (T-02), ironworker (T-03), labourer (T-08) |
| 7 | `PriceSources/Equipment_Pricing.csv` | ALLOWANCE | 3 equipment items with min/max/recommended prices | Overhead cranes (EQ-01 -- context only for DEL-016-01); wash bay/compressor not directly used for DEL-011-01 |

## Document Sources (Quantity Takeoff)

| # | Document | Path | Used For |
|---|---|---|---|
| 1 | Datasheet.md | `PKG-011.../DEL-011-01_Superstructure/Datasheet.md` | Attributes, quantities, materials, construction elements |
| 2 | Specification.md | `PKG-011.../DEL-011-01_Superstructure/Specification.md` | Requirements (REQ-011-01-01 through REQ-011-01-18), scope boundaries, verification |
| 3 | Guidance.md | `PKG-011.../DEL-011-01_Superstructure/Guidance.md` | Principles, considerations, trade-offs, conflict table |
| 4 | Procedure.md | `PKG-011.../DEL-011-01_Superstructure/Procedure.md` | Work steps (32 steps in 6 phases), prerequisites, verification, records |
| 5 | _CONTEXT.md | `PKG-011.../DEL-011-01_Superstructure/_CONTEXT.md` | Deliverable ID, name, package, discipline, type |

## Decomposition Source

| # | Document | Used For |
|---|---|---|
| 1 | `_Decomposition/WDMLRL_Decomposition_Claude.md` | PKG-011 definition, DEL-011-01 SOW mapping (SOW-0022), WBS traceability |

## Sources Not Used (present in PRICE_SOURCES but not applicable)

- `Equipment_Pricing.csv` EQ-01 (crane supply/install) -- relevant to DEL-016-01 not DEL-011-01
- `Equipment_Pricing.csv` EQ-02, EQ-03 (wash bay equipment, compressor) -- not in DEL-011-01 scope
