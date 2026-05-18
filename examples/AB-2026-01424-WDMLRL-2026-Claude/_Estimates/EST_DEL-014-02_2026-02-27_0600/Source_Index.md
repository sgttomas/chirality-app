# Source Index — EST_DEL-014-02_2026-02-27_0600

## Price Sources Indexed

| # | Source File | Source Type | Items Supported | Parsing Notes |
|---|---|---|---|---|
| PS-01 | `PriceSources/Professional_Staff_Rates.csv` | RATE_TABLE | ITEM-011 through ITEM-016 (professional staff hourly rates) | 25 roles with hourly rates in CAD; used R-01, R-02, R-03, R-05, R-06, R-08 |
| PS-02 | `PriceSources/Level_of_Effort.csv` | PARAMETRIC | ITEM-011 through ITEM-016 (estimated hours per role per deliverable) | Filtered for DEL-014-02: 6 role entries with estimated hours |
| PS-03 | `PriceSources/Assumed_Project_Parameters.csv` | PARAMETRIC | Context parameters: tank capacity (PP-15: 2,000 US gal), currency (PP-17: CAD) | 19 parameters; PP-15 directly relevant to septic scope |
| PS-04 | `PriceSources/Underground_Utility_Rates.csv` | PARAMETRIC | ITEM-001 (UU-04: septic tank supply + set), ITEM-002 (UU-02: sanitary line) | 5 items; UU-02 and UU-04 directly applicable |
| PS-05 | `PriceSources/Construction_Labour_Rates.csv` | RATE_TABLE | ITEM-017 (T-05 Plumber), ITEM-018 (T-07 Equipment Operator), ITEM-019 (T-08 Labourer) | 10 trades with base and fully burdened rates |
| PS-06 | `PriceSources/Equipment_Pricing.csv` | ALLOWANCE | Not directly applicable to DEL-014-02 (crane and shop equipment only) | 3 items; no septic-specific equipment |

## Deliverable Documents Read

| Document | Path | Items Derived |
|---|---|---|
| `_CONTEXT.md` | `PKG-014_.../DEL-014-02_Septic/_CONTEXT.md` | Deliverable identification, SOW-0043, objectives |
| `Datasheet.md` | `PKG-014_.../DEL-014-02_Septic/Datasheet.md` | Tank attributes, conditions, construction details (ITEM-001, ITEM-002) |
| `Specification.md` | `PKG-014_.../DEL-014-02_Septic/Specification.md` | Requirements, scope inclusions/exclusions, verification (ITEM-006, ITEM-007) |
| `Guidance.md` | `PKG-014_.../DEL-014-02_Septic/Guidance.md` | Principles, trade-offs, alarm/monitoring consideration (ITEM-010) |
| `Procedure.md` | `PKG-014_.../DEL-014-02_Septic/Procedure.md` | Work steps, prerequisites, closeout (ITEM-003 through ITEM-005, ITEM-008, ITEM-009, ITEM-017 through ITEM-020) |

## Decomposition Reference

| Document | Path | Usage |
|---|---|---|
| `WDMLRL_Decomposition_Claude.md` | `_Decomposition/WDMLRL_Decomposition_Claude.md` | WBS traceability: PKG-014 = Plumbing & Water Systems Installation; DEL-014-02 = Septic System; SOW-0043 |

## Coverage Gaps

| Gap | Impact | Recommendation |
|---|---|---|
| No direct quote for septic holding tank | UU-04 provides a parametric range ($18,000–$42,000, recommended $29,000) — used as PARAMETRIC estimate | Obtain supplier quote for actual tank material once DEL-006-05 specifies material |
| No rate for existing tank removal activities | Demolition and disposal costs derived parametrically | Obtain subcontractor quote for existing tank removal |
| Equipment rental rates not provided | Excavator rental not in Equipment_Pricing.csv (cranes only) | Equipment cost absorbed into lump-sum excavation items |
| Sanitary line run length unknown | Assumed 15 m parametric estimate | Confirm actual run length from IFC drawings (DEL-006-05) |
