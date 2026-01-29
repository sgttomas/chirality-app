# Basis of Estimate (BOE)

## Snapshot Identification

| Field | Value |
|-------|-------|
| Snapshot ID | EST_PKG07_DRAFT_2026-01-28_2332 |
| Estimate Label | PKG07_DRAFT |
| Pricing Date | 2026-01 (January 2026 dollars) |
| Currency | CAD |
| Package Scope | PKG-07 Rail Works (4 deliverables) |
| Run Status | WARNINGS |

## Currency & Conversion

- **Currency:** CAD (Canadian dollars)
- **Evidence:** Project location is Fraser Surrey Terminal, Surrey, BC, Canada (decomposition Section 1)
- **Conversion:** None required; single-currency estimate
- **Decision:** D-001 (currency selection)

## Scope Inclusions

This estimate includes the following CBS buckets for PKG-07:

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
| Track subgrade preparation | Assumed in PKG-02 Earthworks per D-013 |
| Track drainage systems | Assumed in PKG-03 Underground Utilities per D-014 |
| Track electrical bonding/grounding | Assumed in PKG-17 Electrical per A-021 |
| Track switches/turnouts | Scope TBD in ER per A-020 |
| Escalation | escalation_mode = NONE per config |
| Taxes | Excluded from base estimate |

## PKG-07 Physical Scope

**From decomposition (test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:259):**
- New rail tracks 6 & 7
- Track 5 restoration and modifications
- Associated ballast works
- End stops

**Key project parameter (README.md:38):**
- 32 railcar unloading stations

**Scope interpretation:**
- Tracks 6 & 7 support the 32-car unloading capacity
- Track 5 is existing infrastructure requiring restoration/modifications
- Track 6 was previously removed in PKG-01 Demolition scope
- New Track 6 & 7 construction enables Phase 1 operations

## Contracting Assumptions

| Assumption | Value | Decision Ref |
|------------|-------|--------------|
| Contract type | Design & Build (D&B) | decomposition Section 1 |
| Contractor responsibility | Full design and construction | decomposition Section 1.2 |
| Track layout design | Contractor to perform | DEL-07.01 |
| Track geometry calculations | Contractor to perform | DEL-07.03 |
| Rail procurement | Contractor to procure | CBS includes MAT + P |
| Scope split assumptions | Subgrade in PKG-02; drainage in PKG-03 | D-013, D-014 |

## Location / Productivity Assumptions

| Assumption | Value | Decision Ref |
|------------|-------|--------------|
| Location | Fraser Surrey Terminal, Surrey, BC | decomposition |
| Productivity factor | 1.0 (BC lower mainland baseline) | D-006 |
| Site access | Work at operating terminal; coordination required | D-007, A-019 |
| Working hours | Standard shifts assumed; may need night/weekend work | D-007 |
| Terminal operations impact | Active rail operations; safety protocols apply | A-019, R-005 |

## Quantities Basis

**Track lengths (Decision D-002, D-003):**
- Track 6 (new): 500 linear meters
- Track 7 (new): 500 linear meters
- Track 5 (restoration): 300 linear meters
- **Total:** 1,300 linear meters

**Basis:** 32 railcar capacity at ~15m/car spacing suggests ~500m per unloading track. Track 5 restoration assumed at 60% of new track length (partial scope).

**Ballast quantities (Decision D-004):**
- 1,300m track × 1.5 m³/m = 1,950 m³
- **Basis:** Typical rail ballast section (300mm depth × 3m width average)

**End stops (Decision D-005):**
- 4 units (2 tracks × 2 ends each for Tracks 6 & 7)
- **Basis:** New tracks require end stops; Track 5 restoration may use existing

**Other components:**
- Ties/sleepers at typical spacing for track length
- Fasteners as percentage of rail cost (20%)
- Survey, testing, inspection as allowances based on track extent

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
| MAT | 15% | +10% (100% allowance) | 25% | All material allowances; rail pricing uncertain |
| CD | 20% | +10% (100% allowance) | 30% | All CD allowances; terminal access risk |
| CI | 20% | +10% (100% allowance) | 30% | Derived from CD |
| PM | 10% | +5% (factor-derived) | 15% | Factor-based |
| P | 10% | +5% (factor-derived) | 15% | Factor-based |
| COM | 25% | +5% (factor-derived) | 30% | Testing scope uncertainty |

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
| No track layout design | Unable to confirm track lengths | Provide design drawings (DEL-07.01) |
| No Track 5 condition assessment | Restoration scope unknown | Provide condition survey and assessment |
| No track geometry calculations | Ballast design assumptions only | Complete calculations (DEL-07.03) |
| No vendor quotes | All rail/materials as allowances | Obtain budgetary quotes from rail suppliers |
| No rate tables | Labor rates assumed | Provide project rate library |
| No rail specification | Rail type/grade assumed | Develop specification (DEL-07.02) |
| Scope boundaries unclear | Interface assumptions with PKG-02/03/17/34 | Confirm scope splits in ER |

## References

| Document | Description |
|----------|-------------|
| Decision_Log.md | All decisions D-001 through D-014 |
| Assumptions_Log.md | All assumptions A-001 through A-022 |
| Detail.csv | Line item detail with traceability |
| QA_Report.md | Quality checks and completeness metrics |
| Risk_Register.md | Risk factors and contingency basis |
