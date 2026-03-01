# Source Index — EST_DEL-011-02_2026-02-27_0848

## Price Sources

| Source # | File Path | Source Type | Parsing Notes | Supports |
|---|---|---|---|---|
| PS-01 | PriceSources/Professional_Staff_Rates.csv | PARAMETRIC (rate table) | 25 roles with hourly rates in CAD; MEDIUM confidence | Professional staff labour costing (PM, CPM, Supt, QA/QC, HSE, Cost Est, Structural Eng) |
| PS-02 | PriceSources/Level_of_Effort.csv | PARAMETRIC (hours model) | Hours by deliverable and role; DEL-011-02 has 6 rows (R-01, R-02, R-03, R-05, R-06, R-08) | Professional staff hours allocation for DEL-011-02 |
| PS-03 | PriceSources/Assumed_Project_Parameters.csv | PARAMETRIC (parameters) | 19 project parameters; key: PP-10 floor area ~13,000 sqft, PP-11 ceiling 35ft, PP-17 currency CAD | Context and parametric inputs |
| PS-04 | PriceSources/Structural_Concrete_Rates.csv | PARAMETRIC / ALLOWANCE | 8 items; SC-08 specifically covers embedded steel plates (supply+install) at $250/EA ALLOWANCE LOW confidence | Steel plate unit pricing; concrete interface rates |
| PS-05 | PriceSources/Building_Envelope_Rates.csv | PARAMETRIC | 6 items for envelope components | Not directly applicable to DEL-011-02; no steel embedment rates |
| PS-06 | PriceSources/Construction_Labour_Rates.csv | PARAMETRIC | 10 trades with base and fully burdened rates; T-03 Ironworker $92.80/hr burdened; T-02 Concrete Finisher $77.50/hr burdened; T-08 Labourer $65.10/hr burdened | Construction trade labour rates for installation activities |
| PS-07 | PriceSources/Equipment_Pricing.csv | ALLOWANCE | 3 items; no specific steel plate handling equipment; EQ-01 crane pricing is for overhead cranes not mobile cranes | Limited applicability; mobile crane/telehandler rate estimated parametrically |

## Document Sources (Engineering Content)

| Source # | File Path | Type | Notes |
|---|---|---|---|
| DS-01 | DEL-011-02_Steel-Embedments/_CONTEXT.md | Context | Deliverable identity, PKG-011, SOW-0024 |
| DS-02 | DEL-011-02_Steel-Embedments/Datasheet.md | Datasheet | Attributes, quantities (TBD many), layout from Appendix B |
| DS-03 | DEL-011-02_Steel-Embedments/Specification.md | Specification | 12 requirements; verification matrix; standards |
| DS-04 | DEL-011-02_Steel-Embedments/Guidance.md | Guidance | Principles, considerations, 3 conflicts, trade-offs |
| DS-05 | DEL-011-02_Steel-Embedments/Procedure.md | Procedure | 15 steps in 4 phases; 10 prerequisites; verification; records |
| DS-06 | _Decomposition/WDMLRL_Decomposition_Claude.md | Decomposition | SOW-0024 scope; PKG-011 deliverables; WBS traceability |

## Coverage Gaps

- No direct steel plate material pricing per kg or per m2 in price sources. SC-08 provides a per-EA allowance ($250/EA) at LOW confidence, suitable only as a placeholder for individual plate installation.
- No mobile crane/telehandler rental rate in Equipment_Pricing.csv. Estimated parametrically.
- No welding inspector third-party rate in price sources. Estimated parametrically.
- No corrosion protection coating rates in price sources. Estimated as allowance.
