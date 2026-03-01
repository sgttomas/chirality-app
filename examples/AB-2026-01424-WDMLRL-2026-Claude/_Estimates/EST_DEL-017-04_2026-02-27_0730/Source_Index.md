# Source Index — EST_DEL-017-04_2026-02-27_0730

## Pricing Sources

| # | Source File | Source Type | Parsing Notes | Supports |
|---|------------|-------------|---------------|----------|
| PS-1 | Professional_Staff_Rates.csv | RATE_TABLE | 25 roles with hourly rates in CAD; Basis=PARAMETRIC, Confidence=MEDIUM | Professional staff hourly rates for design, management, QA, HSE, and specialty roles |
| PS-2 | Level_of_Effort.csv | PARAMETRIC | Multi-deliverable hours table; DEL-017-04 has 6 rows (R-01, R-02, R-03, R-05, R-06, R-08) totalling 38 hours; Notes read "PKG-017 TBD -- TBD" indicating placeholder-level estimates | Professional staff hour allocations per deliverable per role |
| PS-3 | Assumed_Project_Parameters.csv | PARAMETRIC | 18 project-wide parameters; relevant: PP-10 (13000 sqft addition), PP-11 (35 ft ceiling), PP-17 (CAD currency) | Project context parameters; no direct pricing but informs parametric sizing |
| PS-4 | Interior_Architectural_Rates.csv | RATE_TABLE | 5 items: partitions (IA-01), paint (IA-02), suspended ceilings (IA-03), flooring (IA-04), millwork (IA-05); rates in CAD per m2 or LS; Basis=PARAMETRIC, Confidence=MEDIUM-LOW | Interior construction unit rates for partitions, finishes, ceilings, flooring |
| PS-5 | Construction_Labour_Rates.csv | RATE_TABLE | 10 trades with base hourly, burden multiplier, and fully burdened rates; Basis=PARAMETRIC, Confidence=MEDIUM | Construction trade labour rates (carpenter, electrician, plumber, HVAC, labourer, drywaller, painter) |

## Deliverable Documents (Read-Only, Not Pricing Sources)

| Document | Path | Role |
|----------|------|------|
| _CONTEXT.md | DEL-017-04_Locker-Room/_CONTEXT.md | Deliverable identity and scope context |
| Datasheet.md | DEL-017-04_Locker-Room/Datasheet.md | Attributes, quantities, materials, conditions |
| Specification.md | DEL-017-04_Locker-Room/Specification.md | Requirements, standards, verification criteria |
| Guidance.md | DEL-017-04_Locker-Room/Guidance.md | Design principles, trade-offs, considerations |
| Procedure.md | DEL-017-04_Locker-Room/Procedure.md | Work steps, prerequisites, verification activities |

## Source Coverage Assessment

| Coverage Area | Status | Notes |
|---------------|--------|-------|
| Professional staff rates | COVERED | PS-1 provides hourly rates for all roles referenced in PS-2 |
| Professional staff hours | COVERED (placeholder) | PS-2 provides hours but notes indicate TBD-level estimates |
| Interior architectural material rates | PARTIALLY COVERED | PS-4 covers partitions, paint, ceilings, flooring; does not cover doors, plumbing fixtures, electrical fixtures, lockers, laundry equipment |
| Construction labour rates | COVERED | PS-5 provides fully burdened rates for all relevant trades |
| Equipment/fixture unit costs (lockers, laundry, plumbing fixtures, lighting) | NOT COVERED | No pricing source provides unit costs for equipment or fixtures; parametric estimates used per FALLBACK_POLICY=ALLOW_PARAMETRIC |
| Subcontract pricing | NOT COVERED | No subcontractor quotes provided |
