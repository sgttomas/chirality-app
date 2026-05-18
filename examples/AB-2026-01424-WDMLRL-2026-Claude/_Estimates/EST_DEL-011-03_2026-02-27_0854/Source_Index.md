# Source Index — EST_DEL-011-03_2026-02-27_0854

## Price Sources Indexed

| # | Source File | Source Type | Parsing Notes | Supports | Gaps |
|---|---|---|---|---|---|
| PS-01 | Professional_Staff_Rates.csv | Rate Table | 25 roles; CSV; HourlyRate_CAD column; all PARAMETRIC basis | Professional staff hourly rates (R-01 through R-25) | No gap for DEL-011-03 staff roles |
| PS-02 | Level_of_Effort.csv | Parametric Model | Large CSV; DeliverableID + RoleID + EstimatedHours; PARAMETRIC basis | Staff hours for DEL-011-03: R-01=6hr, R-02=8hr, R-03=10hr, R-05=4hr, R-06=6hr, R-08=4hr | No construction labour hours (derived parametrically) |
| PS-03 | Assumed_Project_Parameters.csv | Parametric Model | 18 parameters; project-level context | Building footprint (13000 sqft / ~1208 m2), ceiling height (35 ft), currency (CAD) | No direct pricing data; context only |
| PS-04 | Structural_Concrete_Rates.csv | Rate Table | 8 items; CSV; RecommendedRate column; PARAMETRIC/ALLOWANCE basis | SC-01 through SC-08: concrete slab, grade beam, footings, rebar, formwork, walls, stairs, embedded plates | Used for floor slope provisions and structural context |
| PS-05 | Building_Envelope_Rates.csv | Rate Table | 6 items; CSV; RecommendedRate column; PARAMETRIC/ALLOWANCE basis | BE-01 through BE-06: wall panels, roof panels, overhead doors, man doors, flashing, windows | **BE-03**: Primary rate for 24 ft class overhead doors ($19,000 each); ALLOWANCE basis, LOW confidence |
| PS-06 | Construction_Labour_Rates.csv | Rate Table | 10 trades; CSV; FullyBurdenedRate_CAD column; PARAMETRIC basis | T-01 Carpenter $80.60, T-02 Concrete Finisher $77.50, T-03 Ironworker $92.80, T-08 Labourer $65.10 | Door installer rate not explicitly provided; T-03 ironworker used as proxy |
| PS-07 | Equipment_Pricing.csv | Rate Table | 3 items; CSV; RecommendedPrice column; ALLOWANCE basis | EQ-01 (cranes), EQ-02 (wash bay), EQ-03 (compressor) | No direct equipment pricing applicable to DEL-011-03 scope (overhead doors are building components, not equipment) |

## Documents Read (Step 1)

| Document | File | Status |
|---|---|---|
| _CONTEXT.md | DEL-011-03_Repair-Bays/_CONTEXT.md | Read |
| Datasheet.md | DEL-011-03_Repair-Bays/Datasheet.md | Read |
| Specification.md | DEL-011-03_Repair-Bays/Specification.md | Read |
| Guidance.md | DEL-011-03_Repair-Bays/Guidance.md | Read |
| Procedure.md | DEL-011-03_Repair-Bays/Procedure.md | Read |
| Decomposition | _Decomposition/WDMLRL_Decomposition_Claude.md | Read (DEL-011-03 entries) |

## Key Pricing Decisions

- **Overhead door rate**: BE-03 at $19,000/each is an ALLOWANCE rate with LOW confidence. Exact door size/spec TBD per IFC drawings. This is the largest single line item category.
- **Door operators**: No explicit rate in price sources. Derived parametrically at $3,500/each based on industrial overhead door operator pricing for 24 ft class doors.
- **Safety devices**: No explicit rate in price sources. Derived parametrically at $750/each based on typical industrial door safety device packages.
- **Weather seals**: No explicit rate in price sources. Derived parametrically at $1,200/set based on seal sets for 24 ft class insulated industrial doors in cold climate.
- **Door frame structural**: $8,500/opening used, consistent with EST_DEL-011-01 structural rough opening rate.
- **Door installation labour**: T-03 ironworker rate ($92.80/hr) used as proxy for specialised door installer crew rate; actual installer rates TBD.
