# Basis of Estimate (BOE)

## Snapshot Identification

| Field | Value |
|-------|-------|
| Snapshot ID | EST_PKG04_DRAFT_2026-01-28_2350 |
| Estimate Label | PKG04_DRAFT |
| Pricing Date | 2026-01 (January 2026 dollars) |
| Currency | CAD |
| Package Scope | PKG-04 Pavement & Surfacing (4 deliverables) |
| Run Status | WARNINGS |

## Currency & Conversion

- **Currency:** CAD (Canadian dollars)
- **Evidence:** Project location is Fraser Surrey Terminal, Surrey, BC, Canada (decomposition Section 1)
- **Conversion:** None required; single-currency estimate
- **Decision:** D-001 (currency selection)

## Scope Inclusions

This estimate includes the following CBS buckets for PKG-04:

| CBS | Description | Included |
|-----|-------------|----------|
| E | Engineering & Design | Yes |
| PM | Project Management / EPCM | Yes |
| P | Procurement Services | Yes |
| MAT | Equipment & Materials | Yes |
| CD | Construction Directs | Yes |
| CI | Construction Indirects | Yes |
| COM | Commissioning / Testing | Yes |
| CONT | Contingency | Yes |

### Scope Elements (from Decomposition PKG-04)

- Asphalt paving (roadways, hardstand areas, operational surfaces)
- Concrete surfacing (heavy load areas, chemical exposure zones)
- Curbs and gutters (perimeter containment, drainage conveyance)
- Sidewalks (personnel access routes)
- Parking areas (vehicle parking with stall dimensions and circulation)
- Line marking (traffic control, safety delineation, operational guidance)
- Phase 2 expansion corridor provisions per OBJ-8

## Scope Exclusions

| Exclusion | Rationale |
|-----------|-----------|
| Owner's costs | Not in Contractor scope per decomposition Section 1.2 |
| Land acquisition | Not in Contractor scope |
| Financing costs | Not in Contractor scope |
| Permits obtained by Employer | Per decomposition Section 1.2 |
| Off-site roadway improvements | Public right-of-way (Owner scope) |
| Escalation | escalation_mode = NONE per config |
| Taxes | Excluded from base estimate |
| Earthworks/subgrade (PKG-02) | Separate package; interface only |
| Underground utilities (PKG-03) | Separate package; drainage tie-ins only |

## Contracting Assumptions

| Assumption | Value | Decision Ref |
|------------|-------|--------------|
| Contract type | Design & Build (D&B) | decomposition Section 1 |
| Contractor responsibility | Full design and construction | decomposition Section 1.2 |
| Subgrade preparation | By PKG-02 Earthworks | D-002 |
| Drainage infrastructure | By PKG-03 Underground Utilities | D-003 |
| Interface coordination | Contractor responsibility | decomposition |

## Location / Productivity Assumptions

| Assumption | Value | Decision Ref |
|------------|-------|--------------|
| Location | Fraser Surrey Terminal, Surrey, BC | decomposition |
| Productivity factor | 1.0 (BC lower mainland baseline) | D-004 |
| Site access | Assumed standard access via Elevator Road | D-005 |
| Working hours | Standard 8-10 hour shifts assumed | D-006 |
| Seasonal constraints | Paving limited to dry season (May-October typical) | A-015 |

## Pricing Sources Hierarchy

1. **Quotes/Vendor Budgets:** None available
2. **Project Rate Tables:** None provided
3. **Allowances:** All line items priced via allowances (fallback typical model)

**Decision:** D-007 — All pricing uses allowances due to absence of vendor quotes or rate tables.

## Quantity Basis

All quantities are parametric estimates based on:
- Total site area of ~7 hectares (from PKG-02 scope)
- Industrial transload facility typical pavement coverage ratios
- Deliverable document scope descriptions

| Item | Estimated Quantity | Basis | Decision Ref |
|------|-------------------|-------|--------------|
| Asphalt paving | 35,000 m² | 50% of 7 ha site for roadways/hardstand | A-001 |
| Concrete surfacing | 10,000 m² | Heavy load/chemical exposure zones | A-002 |
| Curbs and gutters | 2,500 lm | Perimeter and internal road delineation | A-003 |
| Sidewalks | 600 m² | Limited personnel areas (~200 lm × 3m) | A-004 |
| Parking area | 2,000 m² | ~50 vehicle stalls plus circulation | A-005 |
| Line marking | 6,000 lm | Traffic control, safety, parking stalls | A-006 |

## Indirects Model

**Method:** Factor-based (fallback typical model)

| Factor | Rate | Base | Decision Ref |
|--------|------|------|--------------|
| Construction Indirects (CI) | 0.18 | CD | D-008 |
| Procurement Services (P) | 0.02 | MAT | D-008 |
| EPCM/PM | 0.06 | CD + CI + MAT | D-008 |
| Commissioning (COM) | 0.03 | CD + CI + MAT | D-008 |

## Contingency Method

**Method:** PCT_BY_BUCKET (percentage by CBS bucket)

| CBS | Base % | Allowance Adjustment | Final % | Rationale |
|-----|--------|---------------------|---------|-----------|
| E | 10% | +10% (100% allowance) | 20% | All engineering allowances |
| MAT | 15% | +10% (100% allowance) | 25% | All material allowances |
| CD | 20% | +10% (100% allowance) | 30% | All CD allowances |
| CI | 20% | +10% (factor-derived) | 30% | Derived from CD |
| PM | 10% | +5% (factor-derived) | 15% | Factor-based |
| P | 10% | +5% (factor-derived) | 15% | Factor-based |
| COM | 25% | +5% (factor-derived) | 30% | Factor-based |

**Decision:** D-009 — Contingency rates elevated due to 100% allowance-based estimate.

## Escalation Method

- **Mode:** NONE
- **Rationale:** Pricing date is current (January 2026); no escalation applied per config
- **Decision:** D-010

## Rounding Policy

- **Rounding:** Nearest $1,000 CAD
- **Decision:** Per _CONFIG.md

## Completeness Metrics

| Metric | Value |
|--------|-------|
| Lines priced by QUOTE | 0% |
| Lines priced by RATE_TABLE | 0% |
| Lines priced by ALLOWANCE/PARAMETRIC | 100% |
| Deliverables with explicit quantities | 0% |
| Overall confidence | LOW |

## Known Gaps

| Gap | Impact | Resolution Path |
|-----|--------|-----------------|
| No pavement layout drawings | Quantities based on area ratios | Provide DEL-04.01 drawings with area calculations |
| No geotechnical data for subgrade | Pavement thickness assumptions only | Provide geotechnical report (PKG-02) |
| No traffic loading data | Pavement design assumptions only | Provide traffic study or ER loading requirements |
| No vendor quotes | All paving/materials as allowances | Obtain budgetary quotes from paving contractors |
| No rate tables | Labor rates assumed | Provide project rate library |

## References

| Document | Description |
|----------|-------------|
| Decision_Log.md | All decisions D-001 through D-010 |
| Assumptions_Log.md | All assumptions A-001 through A-020+ |
| Detail.csv | Line item detail with traceability |
| QA_Report.md | Quality checks and completeness metrics |
| Risk_Register.md | Risk factors and contingency basis |
