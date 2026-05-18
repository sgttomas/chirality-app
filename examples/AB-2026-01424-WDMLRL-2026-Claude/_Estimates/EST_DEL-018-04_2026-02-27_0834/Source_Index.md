# Source Index — EST_DEL-018-04_2026-02-27_0834

## Price Sources Indexed

| # | Source File | Source Type | Parsing Notes | Supports |
|---|------------|-------------|---------------|----------|
| 1 | Professional_Staff_Rates.csv | RATE_TABLE | 25 roles; hourly rates in CAD; PARAMETRIC basis; MEDIUM confidence | Professional staff unit rates (PM, CPM, Superintendent, QA/QC, HSE, Surveyor, etc.) |
| 2 | Level_of_Effort.csv | PARAMETRIC | Deliverable-level hour allocations by role; DEL-018-04 has 6 role entries (R-01, R-02, R-03, R-05, R-06, R-08) | Staff hour quantities for DEL-018-04 |
| 3 | Assumed_Project_Parameters.csv | REFERENCE | 18 parameters; project identity, location, facility, equipment, currency | Project context (building area, crane specs, cistern, currency confirmation) |
| 4 | Earthwork_Civil_Rates.csv | RATE_TABLE | 4 items; units in m2 or m3; PARAMETRIC basis; MEDIUM confidence | Compaction/proof roll rate EC-03 ($4.00/m2) used for subgrade preparation |
| 5 | Paving_Surfacing_Rates.csv | RATE_TABLE | 4 items; units in m2 or m; PARAMETRIC basis; MEDIUM confidence | Concrete apron/approach slab PS-03 ($190/m2) used as proxy for cement pad pricing |
| 6 | Underground_Utility_Rates.csv | RATE_TABLE | 5 items; PARAMETRIC/ALLOWANCE basis; LOW-MEDIUM confidence | Not directly used for DEL-018-04 (utility work in DEL-018-06); referenced for completeness |
| 7 | Construction_Labour_Rates.csv | RATE_TABLE | 10 trades; hourly + fully burdened rates in CAD; PARAMETRIC basis; MEDIUM confidence | Concrete finisher T-02, Equipment Operator T-07, Labourer T-08, Ironworker T-03 rates used for parametric derivations |

## Deliverable Documents Read

| Document | Path | Status |
|----------|------|--------|
| _CONTEXT.md | PKG-018_Sitework & Civil Construction/1_Working/DEL-018-04_Pads/_CONTEXT.md | Read |
| Datasheet.md | PKG-018_Sitework & Civil Construction/1_Working/DEL-018-04_Pads/Datasheet.md | Read |
| Specification.md | PKG-018_Sitework & Civil Construction/1_Working/DEL-018-04_Pads/Specification.md | Read |
| Guidance.md | PKG-018_Sitework & Civil Construction/1_Working/DEL-018-04_Pads/Guidance.md | Read |
| Procedure.md | PKG-018_Sitework & Civil Construction/1_Working/DEL-018-04_Pads/Procedure.md | Read |

## Decomposition

| Document | Path | Status |
|----------|------|--------|
| WDMLRL_Decomposition_Claude.md | _Decomposition/WDMLRL_Decomposition_Claude.md | Read; DEL-018-04 found under PKG-018 covering SOW-0078 and SOW-0079 |

## Source Coverage Notes

- Underground_Utility_Rates.csv was indexed but not used for pricing DEL-018-04 items. It applies to DEL-018-06 (Utility Tie-Ins).
- No QUOTE-type sources were provided. All pricing is PARAMETRIC per BASIS_OF_ESTIMATE.
- Concrete pad pricing uses PS-03 (concrete apron/approach slab at $190/m2) as the closest available parametric proxy. This rate includes typical formwork, reinforcement, and placement for an exterior slab-on-grade.
- Gravel pad pricing excludes material cost (County/Landfill supplies gravel); only placement and compaction labour/equipment is priced.
