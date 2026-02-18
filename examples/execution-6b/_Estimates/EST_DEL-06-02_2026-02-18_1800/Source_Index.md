# Source Index

## Indexed Price Sources

### Source 1: Professional_Staff_Rates.csv

| Field | Value |
|---|---|
| **Path** | `test/execution-6b/_PriceSources/Professional_Staff_Rates.csv` |
| **Type** | Rate Table |
| **Format** | CSV; 30 data rows + header |
| **Content** | Hourly rates (CAD) by RoleID for 30 professional staff roles |
| **Basis stated in file** | MARKET |
| **Confidence stated in file** | MEDIUM (all roles) |
| **Roles used for DEL-06-02** | R-03 (Design Manager, $165/hr), R-02 (Project Manager, $175/hr) |
| **Parsing notes** | Clean CSV; no missing values in used rows |
| **Supports** | Unit rate lookup for RATE_TABLE method |

### Source 2: Level_of_Effort.csv

| Field | Value |
|---|---|
| **Path** | `test/execution-6b/_PriceSources/Level_of_Effort.csv` |
| **Type** | Level of Effort (hours by deliverable and role) |
| **Format** | CSV; 73 data rows + header; filtered to Execution=6b |
| **Content** | Estimated hours per role per deliverable for execution-6b |
| **Basis stated in file** | PARAMETRIC (all rows) |
| **Confidence stated in file** | Not explicit per row; basis is PARAMETRIC |
| **Rows used for DEL-06-02** | Row 51: R-03 Design Manager, 10 hrs; Row 52: R-02 Project Manager, 4 hrs |
| **Parsing notes** | Clean CSV; no missing values in used rows |
| **Supports** | Quantity (hours) lookup per deliverable/role for cost calculation |

### Source 3: Assumed_Project_Parameters.csv

| Field | Value |
|---|---|
| **Path** | `test/execution-6b/_PriceSources/Assumed_Project_Parameters.csv` |
| **Type** | Project Parameters (contextual) |
| **Format** | CSV; 29 data rows + header |
| **Content** | Assumed project parameters (durations, areas, quantities, financial estimates) |
| **Supports** | Background context only; no direct pricing data used for DEL-06-02 |
| **Parsing notes** | Not used for pricing; included for completeness per brief |

## Sources NOT Available

None. All three provided price sources were readable and contained relevant data.

## Coverage Assessment

- **Rate coverage for DEL-06-02**: 2/2 roles have rates (100%)
- **Hours coverage for DEL-06-02**: 2/2 roles have hours (100%)
- **Missing sources**: None
