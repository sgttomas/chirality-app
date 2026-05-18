# Source Index — EST_DEL-012-03_2026-02-27_0630

## Price Sources Indexed

### Source 1 — Professional_Staff_Rates.csv
- **Path:** `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv`
- **Type:** Rate Table (parametric)
- **Content:** 25 professional staff roles with RoleID, Role name, Category, HourlyRate_CAD, Basis (all PARAMETRIC), Confidence (all MEDIUM)
- **Used for:** DL-001 through DL-006 (professional staff line items)
- **Coverage:** Fully covers all professional staff roles allocated to DEL-012-03 in Level_of_Effort.csv
- **Limitations:** Rates are parametric estimates at MEDIUM confidence; not vendor-quoted

### Source 2 — Level_of_Effort.csv
- **Path:** `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv`
- **Type:** Parametric LOE model
- **Content:** Estimated hours by role per deliverable across the entire project. DEL-012-03 has 6 rows: R-01 (6 hr), R-02 (8 hr), R-03 (10 hr), R-05 (4 hr), R-06 (6 hr), R-08 (4 hr)
- **Used for:** Hour quantities for ITM-001 through ITM-006
- **Coverage:** Provides professional staff hours only. Does not include construction trade labour or material quantities.
- **Limitations:** LOE model does not include construction labour hours; those are derived parametrically from area quantities

### Source 3 — Assumed_Project_Parameters.csv
- **Path:** `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv`
- **Type:** Parametric parameters
- **Content:** 19 project-level parameters including building area (~13,000 sq ft), ceiling height (35 ft), crane capacity, cistern volume, currency (CAD)
- **Used for:** Context validation; office floor area assumption derived from building context (PP-10, PP-11)
- **Coverage:** Building-level parameters; does not provide room-level dimensions for the office
- **Limitations:** Office-specific floor area not available — must be assumed (see ASM-001)

### Source 4 — Interior_Architectural_Rates.csv
- **Path:** `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Interior_Architectural_Rates.csv`
- **Type:** Rate Table (parametric)
- **Content:** 5 interior fit-out items: partitions (IA-01, $90/m2), paint (IA-02, $12/m2), ceilings (IA-03, $80/m2), flooring (IA-04, $70/m2), millwork (IA-05, $11,000 LS)
- **Used for:** DL-007 through DL-010 (material rates), DL-018 (millwork allowance)
- **Coverage:** Covers the major interior finish categories applicable to the office
- **Limitations:** Rates are parametric at MEDIUM confidence (LOW for millwork). Unit rates include material only or material + basic install — see individual line notes

### Source 5 — Construction_Labour_Rates.csv
- **Path:** `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Construction_Labour_Rates.csv`
- **Type:** Rate Table (parametric)
- **Content:** 10 construction trades with base hourly rates, burden multipliers, and fully-burdened CAD rates
- **Used for:** DL-012 through DL-023 (construction trade labour and parametric item pricing)
- **Coverage:** Covers carpenter (T-01), electrician (T-04), plumber (T-05), drywaller (T-10), painter (T-09), labourer (T-08)
- **Limitations:** Rates are parametric at MEDIUM confidence. Flooring installer not explicitly listed — carpenter rate used as proxy

## Deliverable Documents (Read-Only; Quantity Takeoff Source)

| Document | Path | Role |
|---|---|---|
| _CONTEXT.md | `PKG-012_.../DEL-012-03_Office/_CONTEXT.md` | Deliverable identity, scope, key requirements |
| Datasheet.md | `PKG-012_.../DEL-012-03_Office/Datasheet.md` | Attributes, quantities, materials, conditions |
| Specification.md | `PKG-012_.../DEL-012-03_Office/Specification.md` | Requirements (REQ-001 through REQ-014), standards, verification |
| Guidance.md | `PKG-012_.../DEL-012-03_Office/Guidance.md` | Principles, trade-offs, design rationale |
| Procedure.md | `PKG-012_.../DEL-012-03_Office/Procedure.md` | Work steps, prerequisites, verification activities |

## Decomposition (Read-Only; WBS Traceability)

| Document | Path | Role |
|---|---|---|
| WDMLRL_Decomposition_Claude.md | `_Decomposition/WDMLRL_Decomposition_Claude.md` | PKG-012 / DEL-012-03 identity, SOW-0031, OBJ-001 |
