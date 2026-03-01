# Source Index — EST_DEL-007-03_2026-02-27_0630

## Price Sources Indexed

### Source 1: Professional_Staff_Rates.csv

| Field | Value |
|---|---|
| **Path** | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv` |
| **Source Type** | Rate Table (PARAMETRIC) |
| **Parsing Notes** | CSV with columns: RoleID, Role, Category, HourlyRate_CAD, Basis, Confidence, Notes. 25 roles defined. |
| **Supports** | Hourly rates for all professional staff roles. Used to price ITEM-001 (R-01 PM @ $165/hr), ITEM-002 (R-08 CE @ $135/hr), ITEM-003 through ITEM-008 (R-19 LA @ $135/hr). |
| **Limitations** | Rates are PARAMETRIC basis with MEDIUM confidence. No escalation or regional adjustment factors included. |

### Source 2: Level_of_Effort.csv

| Field | Value |
|---|---|
| **Path** | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv` |
| **Source Type** | Parametric Model (Level of Effort) |
| **Parsing Notes** | CSV with columns: Execution, DeliverableID, DeliverableName, RoleID, Role, EstimatedHours, Basis, Notes. Rows filtered for DEL-007-03. |
| **Supports** | Hour allocations for DEL-007-03: R-01 Project Manager (6 hr), R-08 Cost Estimator (4 hr), R-19 Landscape Architect (70 hr). Total: 80 hr. |
| **Limitations** | Hours are PARAMETRIC basis. The 70 hr Landscape Architect allocation is a single lump; sub-allocation to Procedure Steps 1-6 is an estimate-agent assumption (see Assumptions_Log.md ASM-002). |

### Source 3: Assumed_Project_Parameters.csv

| Field | Value |
|---|---|
| **Path** | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv` |
| **Source Type** | Project Parameters |
| **Parsing Notes** | CSV with columns: ParameterID, Category, Parameter, Value, Unit, Source, Confidence, Notes. 19 parameters. |
| **Supports** | Confirms project identity (PP-01/02), location (PP-03/04), currency (PP-17: CAD), contract form (PP-06: CCDC 14-2013), and completion deadline (PP-07: 2026-12-31). Provides context but no direct pricing data for DEL-007-03. |
| **Limitations** | No landscape-specific parameters (e.g., planting area, species count) are included. Parameters are contextual, not pricing inputs for this deliverable. |

### Source 4: Professional_Design_Fees.csv

| Field | Value |
|---|---|
| **Path** | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Design_Fees.csv` |
| **Source Type** | Parametric Fee Model |
| **Parsing Notes** | CSV with columns: ItemID, Discipline, Description, FeePercentMin, FeePercentMax, RecommendedPercent, FeeBase, Basis, Confidence, Notes. 5 discipline fee items. |
| **Supports** | Not directly used for DEL-007-03 pricing. No landscape-specific design fee line exists. The Level_of_Effort.csv (hourly allocation) approach was used instead. |
| **Limitations** | No landscape design fee percentage is defined in this source. If a fee-based approach were desired, a landscape-specific row would need to be added. |

## Source Coverage Summary

| Item Range | Primary Pricing Source | Rate Source | Coverage |
|---|---|---|---|
| ITEM-001 (PM) | Level_of_Effort.csv (6 hr) | Professional_Staff_Rates.csv R-01 ($165/hr) | Full |
| ITEM-002 (CE) | Level_of_Effort.csv (4 hr) | Professional_Staff_Rates.csv R-08 ($135/hr) | Full |
| ITEM-003 to ITEM-008 (LA) | Level_of_Effort.csv (70 hr total) | Professional_Staff_Rates.csv R-19 ($135/hr) | Full (sub-allocation is assumed) |
