# Source Index

## Indexed Price Sources

### 1. Professional_Staff_Rates.csv

| Attribute | Value |
|---|---|
| **Path** | `_PriceSources/Professional_Staff_Rates.csv` |
| **Source Type** | Rate Table |
| **Content** | 30 roles with RoleID, Role name, Category, HourlyRate_CAD, Basis (all MARKET except R-30 N/A), Confidence (all MEDIUM except R-30 N/A) |
| **Parsing Notes** | Standard CSV; header row; no blanks; all rates in CAD |
| **Supports** | Hourly rate lookup for all professional staff roles in the estimate |
| **Limitations** | Rates are MARKET basis with MEDIUM confidence; no escalation clause; no overtime/premium rates defined |

### 2. Level_of_Effort.csv

| Attribute | Value |
|---|---|
| **Path** | `_PriceSources/Level_of_Effort.csv` |
| **Source Type** | Rate Table (effort hours component) |
| **Content** | 73 rows mapping Execution/DeliverableID/RoleID to EstimatedHours; filtered for Execution=6b |
| **Parsing Notes** | Standard CSV; header row; Basis column is PARAMETRIC for all rows; multiple roles per deliverable |
| **Supports** | Hour quantities for each role on each deliverable |
| **Limitations** | Hours are PARAMETRIC basis (professional judgment, not measured); single-point estimates without range |

### 3. Assumed_Project_Parameters.csv

| Attribute | Value |
|---|---|
| **Path** | `_PriceSources/Assumed_Project_Parameters.csv` |
| **Source Type** | Parametric / Reference Parameters |
| **Content** | 29 parameters covering duration, area, quantities, and financial assumptions |
| **Parsing Notes** | Standard CSV; header row; mixed confidence levels |
| **Supports** | Context parameters for scope validation (e.g., building areas, lifespan targets). Not directly used for pricing DEL-05-01 line items. |
| **Limitations** | Many parameters are ASSUMPTION or LOW confidence; financial parameters are order-of-magnitude only |

## Source Coverage for DEL-05-01

DEL-05-01 has 1 role assignment in Level_of_Effort.csv:
- R-04 (Architect - Project): 10 hours

Rate for R-04 confirmed in Professional_Staff_Rates.csv: $145/hr CAD.

All line items for DEL-05-01 are fully supported by the two rate table sources.
