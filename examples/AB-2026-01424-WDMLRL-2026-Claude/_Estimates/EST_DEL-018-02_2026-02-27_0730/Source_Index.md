# Source Index — EST_DEL-018-02_2026-02-27_0730

## Price Sources

| # | Source File | Source Type | Parsing Notes | Supports |
|---|-----------|-------------|---------------|----------|
| 1 | `Professional_Staff_Rates.csv` | Rate Table (PARAMETRIC) | 25 roles with hourly rates in CAD; columns: RoleID, Role, Category, HourlyRate_CAD, Basis, Confidence, Notes | Professional staff labour pricing for PM, superintendent, estimator, QA/QC, HSE, civil engineer, landscape architect roles |
| 2 | `Level_of_Effort.csv` | Parametric Model | Hours by deliverable and role; columns: Execution, DeliverableID, DeliverableName, RoleID, Role, EstimatedHours, Basis, Notes | DEL-018-02 has 6 role assignments totaling 38 hours (R-01: 6h, R-02: 8h, R-03: 10h, R-08: 4h, R-06: 6h, R-05: 4h) |
| 3 | `Assumed_Project_Parameters.csv` | Parametric Parameters | 18 project parameters; columns: ParameterID, Category, Parameter, Value, Unit, Source, Confidence, Notes | PP-10 (13,000 sqft floor area) used as basis for site area parametric; PP-17 (CAD currency) |
| 4 | `Earthwork_Civil_Rates.csv` | Rate Table (PARAMETRIC) | 4 earthwork unit rates; columns: ItemID, Category, Description, Unit, RateMin, RateMax, RecommendedRate, Basis, Confidence, Notes | EC-01 (excavation), EC-02 (granular fill), EC-03 (compaction), EC-04 (topsoil strip — N/A, separate deliverable) |
| 5 | `Paving_Surfacing_Rates.csv` | Rate Table (PARAMETRIC) | 4 paving/surfacing unit rates | PS-01 through PS-04 — not directly applicable to DEL-018-02 (gravel/paving are in DEL-018-03/04) but PS-01 may inform landscape hard surface areas |
| 6 | `Underground_Utility_Rates.csv` | Rate Table (PARAMETRIC/ALLOWANCE) | 5 underground utility unit rates | Not directly applicable to DEL-018-02 (utility tie-ins are DEL-018-06) |
| 7 | `Construction_Labour_Rates.csv` | Rate Table (PARAMETRIC) | 10 trade rates with burden multiplier; columns: TradeID, Trade, HourlyRate_CAD, BurdenMultiplier, FullyBurdenedRate_CAD, Basis, Confidence, Notes | T-07 (Equipment Operator: $88.00/hr), T-08 (Labourer: $65.10/hr) applicable to grading; T-09 (Painter: $69.75/hr) may apply to landscape finishing |

## Document Sources (Deliverable Content)

| Document | Path | Notes |
|----------|------|-------|
| `_CONTEXT.md` | `PKG-018_Sitework & Civil Construction/1_Working/DEL-018-02_Grading-Landscape/_CONTEXT.md` | Deliverable identity and scope context |
| `Datasheet.md` | `PKG-018_Sitework & Civil Construction/1_Working/DEL-018-02_Grading-Landscape/Datasheet.md` | Attributes, quantities, conditions, construction elements |
| `Specification.md` | `PKG-018_Sitework & Civil Construction/1_Working/DEL-018-02_Grading-Landscape/Specification.md` | Requirements REQ-01 through REQ-09, standards, verification |
| `Guidance.md` | `PKG-018_Sitework & Civil Construction/1_Working/DEL-018-02_Grading-Landscape/Guidance.md` | Principles, considerations, trade-offs |
| `Procedure.md` | `PKG-018_Sitework & Civil Construction/1_Working/DEL-018-02_Grading-Landscape/Procedure.md` | Phases A through E, prerequisites, records |

## Decomposition Source

| Document | Path | Notes |
|----------|------|-------|
| Decomposition | `_Decomposition/WDMLRL_Decomposition_Claude.md` | PKG-018 structure, SOW-0076 mapping, WBS traceability |
