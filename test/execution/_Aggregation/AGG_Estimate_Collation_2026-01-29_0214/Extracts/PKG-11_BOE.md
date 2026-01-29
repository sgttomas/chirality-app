# Basis of Estimate (BOE)

## Snapshot Identification

| Field | Value |
|-------|-------|
| Snapshot ID | EST_PKG11_DRAFT_2026-01-28_2359 |
| Estimate Label | PKG11_DRAFT |
| Pricing Date | 2026-01 (January 2026 dollars) |
| Currency | CAD |
| Package Scope | PKG-11 Marine Loading System (6 deliverables) |
| Run Status | WARNINGS |

## Currency & Conversion

- **Currency:** CAD (Canadian dollars)
- **Evidence:** Project location is Fraser Surrey Terminal, Surrey, BC, Canada (decomposition Section 1)
- **Conversion:** None required; single-currency estimate
- **Decision:** D-001 (currency selection)

## Scope Inclusions

This estimate includes the following CBS buckets for PKG-11:

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

### Scope Elements (from Decomposition PKG-11)

- **Powered loading arm** — articulated boom with powered slew/luff for vessel loading operations
- **Emergency release coupling (ERC)** — quick-disconnect for vessel drift protection
- **Double-walled export pipe** — primary containment with leak detection annulus from storage to loading arm
- **Leak detection system** — annulus monitoring, drip trays, sump instrumentation with ESD integration
- **Nitrogen supply provisions** — purge/blanketing connections for inert atmosphere (skid by Employer per DEC-07)
- **Operator shelter** — weather protection for loading personnel with controls interface

### Objectives Served

Per decomposition Section 6:
- OBJ-1 Safe & Reliable Operation
- OBJ-2 Throughput Capacity (1,000,000 MT/annum)
- OBJ-4 Operational Flexibility
- OBJ-7 Environmental Protection

## Scope Exclusions

| Exclusion | Rationale |
|-----------|-----------|
| Owner's costs | Not in Contractor scope per decomposition Section 1.2 |
| Land acquisition | Not in Contractor scope |
| Financing costs | Not in Contractor scope |
| Permits obtained by Employer | Per decomposition Section 1.2 |
| Nitrogen supply skid | Employer-supplied per DEC-07; connection only in scope |
| Marine structures/jetty (PKG-08) | Separate package; loading arm foundation interface only |
| Storage tanks (PKG-13) | Separate package; piping tie-in interface only |
| Process piping beyond loading area (PKG-14) | Separate package; pipe routing interface |
| Control system (PKG-19) | Separate package; signal interfaces only |
| Escalation | escalation_mode = NONE per config |
| Taxes | Excluded from base estimate |

## Contracting Assumptions

| Assumption | Value | Decision Ref |
|------------|-------|--------------|
| Contract type | Design & Build (D&B) | decomposition Section 1 |
| Contractor responsibility | Full design and construction | decomposition Section 1.2 |
| Loading arm supply | OEM supply with Contractor installation | D-002 |
| Marine structure foundations | By PKG-08 Marine Structures | D-003 |
| Nitrogen skid | Employer-supplied; connection by Contractor | DEC-07 (decomposition) |
| Interface coordination | Contractor responsibility | decomposition |

## Location / Productivity Assumptions

| Assumption | Value | Decision Ref |
|------------|-------|--------------|
| Location | Fraser Surrey Terminal, Berth 10, Surrey, BC | decomposition |
| Productivity factor | 1.0 (BC lower mainland baseline) | D-004 |
| Site access | Marine/jetty access; coordination with terminal operations | D-005 |
| Working hours | Standard 8-10 hour shifts; marine work may require tide windows | D-006 |
| Weather constraints | Marine work subject to weather windows | A-016 |

## Pricing Sources Hierarchy

1. **Quotes/Vendor Budgets:** None available
2. **Project Rate Tables:** None provided
3. **Allowances:** All line items priced via allowances (fallback typical model)

**Decision:** D-007 — All pricing uses allowances due to absence of vendor quotes or rate tables.

## Quantity Basis

All quantities are parametric estimates based on:
- Typical marine loading arm installations for similar product terminals
- Double-walled pipe routing assumptions (~150m from tank farm to berth)
- Deliverable document scope descriptions
- Industry typical values for leak detection and operator shelter

| Item | Estimated Quantity | Basis | Decision Ref |
|------|-------------------|-------|--------------|
| Marine loading arm | 1 unit | Single berth, single product | A-001 |
| Emergency release coupling | 1 unit | Integral with loading arm | A-001 |
| Double-walled export pipe | 150 lm | Tank farm to berth routing estimate | A-002 |
| Leak detection (annulus) | 1 system | Continuous annulus monitoring | A-003 |
| Leak detection (drip trays) | 3 zones | Loading arm, pipe expansion, sump | A-003 |
| Sump pump | 1 unit | Single containment sump | A-004 |
| Operator shelter | 1 unit | Weather protection with controls | A-005 |
| Nitrogen connection | 1 set | Connection to Employer skid | A-006 |

## Indirects Model

**Method:** Factor-based (fallback typical model)

| Factor | Rate | Base | Decision Ref |
|--------|------|------|--------------|
| Construction Indirects (CI) | 0.18 | CD | D-008 |
| Procurement Services (P) | 0.02 | MAT | D-008 |
| EPCM/PM | 0.06 | CD + CI + MAT | D-008 |
| Commissioning (COM) | 0.04 | CD + CI + MAT | D-008 (elevated for marine loading) |

## Contingency Method

**Method:** PCT_BY_BUCKET (percentage by CBS bucket)

| CBS | Base % | Allowance Adjustment | Final % | Rationale |
|-----|--------|---------------------|---------|-----------|
| E | 10% | +10% (100% allowance) | 20% | All engineering allowances |
| MAT | 15% | +10% (100% allowance) | 25% | All material allowances; equipment pricing uncertain |
| CD | 20% | +10% (100% allowance) | 30% | Marine installation uncertainty |
| CI | 20% | +10% (factor-derived) | 30% | Derived from CD |
| PM | 10% | +5% (factor-derived) | 15% | Factor-based |
| P | 10% | +5% (factor-derived) | 15% | Factor-based |
| COM | 25% | +5% (factor-derived) | 30% | Commissioning complexity for marine loading |

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
| No marine loading arm vendor quotes | Equipment pricing highly uncertain ($800k-$1.5M range) | Obtain budgetary quotes from marine loading arm OEMs (FMC, SVT, Emco Wheaton) |
| No double-walled pipe pricing | Specialty pipe cost assumed | Obtain quotes for lined/double-walled construction |
| No berth layout drawings | Pipe routing assumed at 150m | Provide DEL-11.01 drawings with routing |
| No vessel manifold data | Loading arm envelope assumed | Provide design vessel data for DEL-11.03 calculations |
| No leak detection specification | System scope assumed | Complete DEL-11.02 leak detection requirements |
| Deliverables in INITIALIZED state | Scope not finalized | Progress deliverables to IN_PROGRESS |
| Marine structure interface undefined | Foundation/support costs in PKG-08 | Coordinate with PKG-08 for interface definition |

## References

| Document | Description |
|----------|-------------|
| Decision_Log.md | All decisions D-001 through D-010 |
| Assumptions_Log.md | All assumptions A-001 through A-020+ |
| Detail.csv | Line item detail with traceability |
| QA_Report.md | Quality checks and completeness metrics |
| Risk_Register.md | Risk factors and contingency basis |
