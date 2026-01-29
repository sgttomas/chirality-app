# Basis of Estimate (BOE)

## Snapshot Identification

| Field | Value |
|-------|-------|
| Snapshot ID | EST_PKG09_DRAFT_2026-01-28_2332 |
| Estimate Label | PKG09_DRAFT |
| Pricing Date | 2026-01 (January 2026 dollars) |
| Currency | CAD |
| Package Scope | PKG-09 Marine Outfitting (5 deliverables) |
| Run Status | WARNINGS |

## Currency & Conversion

- **Currency:** CAD (Canadian dollars)
- **Evidence:** Project location is Fraser Surrey Terminal, Surrey, BC, Canada (decomposition Section 1)
- **Conversion:** None required; single-currency estimate
- **Decision:** D-001 (currency selection)

## Scope Inclusions

This estimate includes the following CBS buckets for PKG-09:

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

### Scope Elements (from Decomposition PKG-09)

- **Fenders:** Marine fender system including fender units, chains, anchor pads, frontal frames, mounting hardware
- **Bollards:** Mooring bollards (tee-head or horn type) with foundations/anchorages, proof load testing provisions
- **Ladders:** Ship-to-shore access ladders with safety features (cages, rest platforms per codes)
- **Life-saving equipment:** Life rings, buoys, rescue equipment, mounting hardware per marine safety regulations
- **Existing Berth 10 upgrades and repairs:** Modifications, repairs, refurbishments to existing marine outfitting at Berth 10

## Scope Exclusions

| Exclusion | Rationale |
|-----------|-----------|
| Owner's costs | Not in Contractor scope per decomposition Section 1.2 |
| Land acquisition | Not in Contractor scope |
| Financing costs | Not in Contractor scope |
| Permits obtained by Employer | Per decomposition Section 1.2 |
| Marine structures (PKG-08) | Separate package; structural capacity provided by PKG-08 |
| Fender design verification (DEL-08.08) | PKG-08 deliverable; PKG-09 implements results |
| Berthing energy calculations (DEL-08.06) | PKG-08 deliverable; PKG-09 implements results |
| Mooring analysis (DEL-08.09) | PKG-08 deliverable; PKG-09 implements results |
| Nitrogen supply skid | Employer-supplied per decomposition Section 1.2 |
| Escalation | escalation_mode = NONE per config |
| Taxes | Excluded from base estimate |

## Contracting Assumptions

| Assumption | Value | Decision Ref |
|------------|-------|--------------|
| Contract type | Design & Build (D&B) | decomposition Section 1 |
| Contractor responsibility | Full design, procurement, installation | decomposition Section 1.2 |
| Marine structure interface | Structural capacity provided by PKG-08 | D-002 |
| Berthing design basis | Provided by PKG-08 berthing energy/mooring analyses | D-003 |
| Existing Berth 10 condition | Assumed minor repairs; no major structural work | A-020 |

## Location / Productivity Assumptions

| Assumption | Value | Decision Ref |
|------------|-------|--------------|
| Location | Fraser Surrey Terminal, Surrey, BC | decomposition |
| Productivity factor | 1.0 (BC lower mainland baseline) | D-004 |
| Marine access | Barge/water-based installation access for fenders/bollards | D-005 |
| Working hours | Standard 8-10 hour shifts; marine work tide constraints | D-006 |
| Seasonal constraints | Marine installation limited to favorable weather/tides (May-October typical) | A-021 |

## Pricing Sources Hierarchy

1. **Quotes/Vendor Budgets:** None available
2. **Project Rate Tables:** None provided
3. **Allowances:** All line items priced via allowances (fallback typical model)

**Decision:** D-007 — All pricing uses allowances due to absence of vendor quotes or rate tables.

## Quantity Basis

Quantities are parametric estimates based on:
- Typical marine transload facility outfitting requirements
- Industry-standard fender/bollard spacing and sizing for vessels up to Panamax class
- Deliverable document scope descriptions
- PKG-08 Marine Structures interfaces (assumed berth length ~150m for Phase 1)

| Item | Estimated Quantity | Basis | Decision Ref |
|------|-------------------|-------|--------------|
| Marine fenders | 12 units | Typical spacing 10-15m on 150m berth face | A-001 |
| Mooring bollards | 8 units | Typical 4 bow + 4 stern for Panamax vessel | A-002 |
| Ship-to-shore ladders | 4 units | Typical 2 per berth side for safe access | A-003 |
| Life-saving equipment | 1 LS | Life rings, buoys, rescue equipment per safety codes | A-004 |
| Berth 10 repairs | 1 LS | Minor repairs/refurbishment allowance | A-005 |

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
| MAT | 15% | +10% (100% allowance) | 25% | All material allowances; marine equipment |
| CD | 20% | +10% (100% allowance) | 30% | All CD allowances; marine installation |
| CI | 20% | +10% (factor-derived) | 30% | Derived from CD |
| PM | 10% | +5% (factor-derived) | 15% | Factor-based |
| P | 10% | +5% (factor-derived) | 15% | Factor-based |
| COM | 25% | +5% (factor-derived) | 30% | Factor-based; proof load testing |

**Decision:** D-009 — Contingency rates elevated due to 100% allowance-based estimate and marine installation complexity.

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
| No berthing analysis results (DEL-08.06) | Fender sizing/type based on assumptions | Provide PKG-08 berthing energy calculations |
| No mooring analysis results (DEL-08.09) | Bollard capacities assumed | Provide PKG-08 mooring analysis |
| No fender deflection data (DEL-08.07) | Fender performance assumptions only | Provide PKG-08 fender system analysis |
| No marine structure details (DEL-08.01) | Interface assumptions only | Provide PKG-08 marine structure drawings |
| No vendor quotes | All equipment as allowances | Obtain budgetary quotes from marine equipment suppliers |
| No rate tables | Labor rates assumed | Provide project rate library |
| No Berth 10 condition survey | Repair scope assumed minor | Provide condition assessment/survey |

## References

| Document | Description |
|----------|-------------|
| Decision_Log.md | All decisions D-001 through D-010 |
| Assumptions_Log.md | All assumptions A-001 through A-025+ |
| Detail.csv | Line item detail with traceability |
| Summary.md | Cost summaries and confidence metrics |
