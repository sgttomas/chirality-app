# Source Index — EST_DEL-011-06_2026-02-27_0600

## Price Sources

| # | File | Source Type | Parsing Notes | Supports |
|---|---|---|---|---|
| PS-1 | Professional_Staff_Rates.csv | PARAMETRIC rate table | 25 roles with hourly rates in CAD; Basis=PARAMETRIC, Confidence=MEDIUM | Management and professional staff labour pricing (ITM-017) |
| PS-2 | Level_of_Effort.csv | PARAMETRIC level-of-effort model | Hours by role per deliverable; DEL-011-06 has 6 role entries totaling 38 hours | Staff hours allocation for DEL-011-06 (ITM-017) |
| PS-3 | Assumed_Project_Parameters.csv | Project parameters | 18 parameters covering identity, location, facility, equipment, schedule, currency | Context parameters; facility area ~13,000 sqft, 35' ceiling, 2 x 5-ton cranes |
| PS-4 | Structural_Concrete_Rates.csv | PARAMETRIC rate table | 8 items covering concrete, rebar, formwork, embedded steel | Pit concrete (ITM-002, ITM-003), formwork (ITM-004), rebar (ITM-005), stairs (ITM-010) |
| PS-5 | Building_Envelope_Rates.csv | PARAMETRIC rate table | 6 items covering envelope panels, doors, glazing, flashing | Limited applicability to service pit — not directly used for pit scope |
| PS-6 | Construction_Labour_Rates.csv | PARAMETRIC rate table | 10 trades with hourly and fully-burdened rates in CAD | Trade labour pricing for concrete work, ironwork, general labour (ITM-019) |
| PS-7 | Equipment_Pricing.csv | ALLOWANCE | 3 items (cranes, wash bay, compressor); ALLOWANCE basis, LOW confidence | Not directly applicable to service pit deliverable |

## Document Sources (Deliverable Content)

| Document | Path | Used For |
|---|---|---|
| _CONTEXT.md | PKG-011_.../DEL-011-06_Service-Pit/_CONTEXT.md | Deliverable identification, description, anticipated artifacts |
| Datasheet.md | PKG-011_.../DEL-011-06_Service-Pit/Datasheet.md | Attributes, quantities, materials, conditions, construction details |
| Specification.md | PKG-011_.../DEL-011-06_Service-Pit/Specification.md | Requirements, standards, verification criteria |
| Guidance.md | PKG-011_.../DEL-011-06_Service-Pit/Guidance.md | Principles, trade-offs, design rationale, conflict table |
| Procedure.md | PKG-011_.../DEL-011-06_Service-Pit/Procedure.md | Work steps, prerequisites, verification, records |

## Notes

- Building_Envelope_Rates.csv and Equipment_Pricing.csv have minimal direct applicability to the service pit scope. Building_Envelope_Rates.csv does not contain pit-specific rates. Equipment_Pricing.csv contains crane pricing which is out-of-scope for this deliverable.
- Structural_Concrete_Rates.csv is the primary construction cost source, providing rates for concrete walls (SC-06), slab (SC-01), formwork (SC-05), rebar (SC-04), and stairs (SC-07).
- Construction_Labour_Rates.csv provides trade labour rates for concrete finishers (T-02), labourers (T-08), and ironworkers (T-03).
- All quantities are parametric estimates based on assumed pit dimensions (12m L x 1.5m W x 1.5m D). Actual dimensions TBD pending IFC structural drawings (DEL-002-06).
