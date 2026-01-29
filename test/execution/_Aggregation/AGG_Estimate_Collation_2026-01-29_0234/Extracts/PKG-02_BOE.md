# Basis of Estimate (BOE)

## Snapshot Identification

| Field | Value |
|-------|-------|
| Snapshot ID | EST_PKG02_DRAFT_2026-01-28_2330 |
| Estimate Label | PKG02_DRAFT |
| Pricing Date | 2026-01 (January 2026 dollars) |
| Currency | CAD |
| Package Scope | PKG-02 Earthworks & Ground Improvement (9 deliverables) |
| Run Status | WARNINGS |

## Currency & Conversion

- **Currency:** CAD (Canadian dollars)
- **Evidence:** Project location is Fraser Surrey Terminal, Surrey, BC, Canada (decomposition Section 1)
- **Conversion:** None required; single-currency estimate
- **Decision:** D-001 (currency selection)

## Scope Inclusions

This estimate includes the following CBS buckets for PKG-02:

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

## Scope Exclusions

| Exclusion | Rationale |
|-----------|-----------|
| Owner's costs | Not in Contractor scope per decomposition Section 1.2 |
| Land acquisition | Not in Contractor scope |
| Financing costs | Not in Contractor scope |
| Permits obtained by Employer | Per decomposition Section 1.2 |
| Escalation | escalation_mode = NONE per config |
| Taxes | Excluded from base estimate |

## Contracting Assumptions

| Assumption | Value | Decision Ref |
|------------|-------|--------------|
| Contract type | Design & Build (D&B) | decomposition Section 1 |
| Contractor responsibility | Full design and construction | decomposition Section 1.2 |
| Geotechnical investigation | Contractor to perform | D-002 |
| Surveying | Contractor to perform | D-003 |
| Ground improvement | Assumed required based on Fraser River delta location | D-004 |

## Location / Productivity Assumptions

| Assumption | Value | Decision Ref |
|------------|-------|--------------|
| Location | Fraser Surrey Terminal, Surrey, BC | decomposition |
| Productivity factor | 1.0 (BC lower mainland baseline) | D-005 |
| Site access | Assumed standard access via Elevator Road | D-006 |
| Working hours | Standard 8-10 hour shifts assumed | D-007 |
| Seasonal constraints | Wet season work may affect productivity | A-020 |

## Pricing Sources Hierarchy

1. **Quotes/Vendor Budgets:** None available
2. **Project Rate Tables:** None provided
3. **Allowances:** All line items priced via allowances (fallback typical model)

**Decision:** D-008 — All pricing uses allowances due to absence of vendor quotes or rate tables.

## Indirects Model

**Method:** Factor-based (fallback typical model)

| Factor | Rate | Base | Decision Ref |
|--------|------|------|--------------|
| Construction Indirects (CI) | 0.18 | CD | D-009 |
| Procurement Services (P) | 0.02 | MAT | D-009 |
| EPCM/PM | 0.06 | CD + CI + MAT | D-009 |
| Commissioning (COM) | 0.03 | CD + CI + MAT | D-009 |

## Contingency Method

**Method:** PCT_BY_BUCKET (percentage by CBS bucket)

| CBS | Base % | Allowance Adjustment | Final % | Rationale |
|-----|--------|---------------------|---------|-----------|
| E | 10% | +10% (100% allowance) | 20% | All engineering allowances |
| MAT | 15% | +10% (100% allowance) | 25% | All material allowances |
| CD | 20% | +10% (100% allowance) | 30% | All CD allowances |
| CI | 20% | +10% (100% allowance) | 30% | Derived from CD |
| PM | 10% | +5% (factor-derived) | 15% | Factor-based |
| P | 10% | +5% (factor-derived) | 15% | Factor-based |
| COM | 25% | +5% (factor-derived) | 30% | Factor-based |

**Decision:** D-010 — Contingency rates elevated due to 100% allowance-based estimate.

## Escalation Method

- **Mode:** NONE
- **Rationale:** Pricing date is current (January 2026); no escalation applied per config
- **Decision:** D-011

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
| No earthwork quantities (cut/fill volumes) | Unable to price earthwork by volume | Provide design drawings with quantity takeoff |
| No geotechnical data | Ground improvement scope unknown | Provide geotechnical investigation results |
| No site survey | Site grading extent unknown | Provide topographic survey |
| No vendor quotes | All equipment/services as allowances | Obtain budgetary quotes |
| No rate tables | Labor rates assumed | Provide project rate library |

## References

| Document | Description |
|----------|-------------|
| Decision_Log.md | All decisions D-001 through D-011 |
| Assumptions_Log.md | All assumptions A-001 through A-020+ |
| Detail.csv | Line item detail with traceability |
| QA_Report.md | Quality checks and completeness metrics |
| Risk_Register.md | Risk factors and contingency basis |
