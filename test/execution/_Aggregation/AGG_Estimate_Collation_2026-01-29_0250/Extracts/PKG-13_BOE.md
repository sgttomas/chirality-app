# Basis of Estimate (BOE)

## Snapshot Identification

| Field | Value |
|-------|-------|
| Snapshot ID | EST_PKG13_DRAFT_2026-01-28_2400 |
| Estimate Label | PKG13_DRAFT |
| Pricing Date | 2026-01 (January 2026 dollars) |
| Currency | CAD |
| Package Scope | PKG-13 Storage Tanks (6 deliverables) |
| Run Status | WARNINGS |

## Currency & Conversion

- **Currency:** CAD (Canadian dollars)
- **Evidence:** Project location is Fraser Surrey Terminal, Surrey, BC, Canada (decomposition Section 1)
- **Conversion:** None required; single-currency estimate
- **Decision:** D-001 (currency selection)

## Scope Inclusions

This estimate includes the following CBS buckets for PKG-13:

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

### Scope Elements (from Decomposition PKG-13)

- **3 × 15,000 MT API 650 Storage Tanks** — Atmospheric vertical cylindrical tanks for CSD canola oil storage
- **Tank internals** — Internal ladders, platforms, access equipment, drain sumps
- **3 × Agitators** — Side-entry or top-mounted agitators for product mixing (one per tank)
- **Overflow protection system** — High-level protection with instrumentation and alarms
- **Water draw-off system** — Bottom water removal system for product quality
- **Tank appurtenances** — Nozzles, manholes, vents, pressure/vacuum relief, gauging
- **Phase 2 connections** — Blind flanges and provisions for future expansion
- **Internal coating** — Food-grade epoxy or phenolic coating system
- **External coating** — Environmental coating system

### Objectives Served

Per decomposition Section 6:
- OBJ-1 Safe & Reliable Operation
- OBJ-3 Storage Capacity (45,000 MT)
- OBJ-8 Future Expandability (Phase 2)

## Scope Exclusions

| Exclusion | Rationale |
|-----------|-----------|
| Owner's costs | Not in Contractor scope per decomposition Section 1.2 |
| Land acquisition | Not in Contractor scope |
| Financing costs | Not in Contractor scope |
| Permits obtained by Employer | Per decomposition Section 1.2 |
| Tank foundations (PKG-05) | Concrete structures separate package; interface only |
| Tank farm piping (PKG-14) | Process piping separate package; nozzle interface only |
| Instrumentation (PKG-20) | Field instrumentation separate package; nozzle provisions only |
| Coatings application (PKG-26) | Protective coatings package if separated; estimate assumes tank vendor scope |
| Fire protection foam systems (PKG-23) | Separate specialty package |
| Dyke/bund walls (PKG-05) | Concrete structures separate package |
| Escalation | escalation_mode = NONE per config |
| Taxes | Excluded from base estimate |

## Contracting Assumptions

| Assumption | Value | Decision Ref |
|------------|-------|--------------|
| Contract type | Design & Build (D&B) | decomposition Section 1 |
| Contractor responsibility | Full design and construction | decomposition Section 1.2 |
| Tank supply | Field-erected by qualified tank fabricator | D-002 |
| Tank fabrication | Shop-fabricated shell courses, field-erected | D-003 |
| Agitator supply | OEM supply with Contractor installation | D-004 |
| Internal coating | By tank vendor as part of tank supply | D-005 |
| External coating | By tank vendor or coating contractor | D-006 |

## Location / Productivity Assumptions

| Assumption | Value | Decision Ref |
|------------|-------|--------------|
| Location | Fraser Surrey Terminal, Tank Farm Area, Surrey, BC | decomposition |
| Productivity factor | 1.0 (BC lower mainland baseline) | D-007 |
| Site access | Heavy equipment access for tank erection | A-020 |
| Working hours | Standard 8-10 hour shifts | D-008 |
| Crane availability | Large crawler crane (200+ ton) for erection | A-021 |
| Laydown area | Adequate laydown assumed for plate staging | A-022 |

## Pricing Sources Hierarchy

1. **Quotes/Vendor Budgets:** None available
2. **Project Rate Tables:** None provided
3. **Allowances:** All line items priced via allowances (fallback typical model)

**Decision:** D-009 — All pricing uses allowances due to absence of vendor quotes or rate tables.

## Quantity Basis

All quantities are parametric estimates based on:
- API 650 typical tank sizing for 15,000 MT canola oil capacity (~16,300 m³ at SG 0.92)
- Typical tank dimensions: ~30m diameter × ~24m shell height per tank
- Industry typical values for agitators, appurtenances, coatings
- Deliverable document scope descriptions

| Item | Estimated Quantity | Basis | Decision Ref |
|------|-------------------|-------|--------------|
| API 650 tanks | 3 units | Decomposition 3 × 15,000 MT | Decomposition |
| Tank capacity each | 16,300 m³ | 15,000 MT ÷ 0.92 SG | A-001 |
| Tank diameter | ~30 m | Typical D/H optimization | A-002 |
| Tank shell height | ~24 m | Typical D/H optimization | A-002 |
| Tank shell courses | 8 courses | ~3m plate heights typical | A-003 |
| Bottom plate area | ~710 m² per tank | π × 15² | Calculated |
| Shell plate area | ~2,260 m² per tank | π × 30 × 24 | Calculated |
| Roof area | ~710 m² per tank | Cone roof assumed | A-004 |
| Total steel weight | ~420 tonnes per tank | Typical for API 650 | A-005 |
| Agitators | 3 units | One per tank | Decomposition |
| Agitator power | ~75 HP each | Side-entry typical | A-006 |
| Nozzles | 18-24 per tank | Typical API 650 | A-007 |
| Manholes | 2 per tank (shell + roof) | API 650 standard | A-008 |
| Internal coating | ~3,680 m² per tank | Shell + bottom + roof | A-009 |
| External coating | ~2,970 m² per tank | Shell + roof | A-010 |

## Indirects Model

**Method:** Factor-based (fallback typical model)

| Factor | Rate | Base | Decision Ref |
|--------|------|------|--------------|
| Construction Indirects (CI) | 0.18 | CD | D-010 |
| Procurement Services (P) | 0.02 | MAT | D-010 |
| EPCM/PM | 0.06 | CD + CI + MAT | D-010 |
| Commissioning (COM) | 0.03 | CD + CI + MAT | D-010 |

## Contingency Method

**Method:** PCT_BY_BUCKET (percentage by CBS bucket)

| CBS | Base % | Allowance Adjustment | Final % | Rationale |
|-----|--------|---------------------|---------|-----------|
| E | 10% | +10% (100% allowance) | 20% | All engineering allowances |
| MAT | 15% | +10% (100% allowance) | 25% | All material allowances; tank steel pricing volatile |
| CD | 20% | +10% (100% allowance) | 30% | Field erection productivity uncertainty |
| CI | 20% | +10% (factor-derived) | 30% | Derived from CD |
| PM | 10% | +5% (factor-derived) | 15% | Factor-based |
| P | 10% | +5% (factor-derived) | 15% | Factor-based |
| COM | 25% | +5% (factor-derived) | 30% | Hydrostatic test complexity |

**Decision:** D-011 — Contingency rates elevated due to 100% allowance-based estimate.

## Escalation Method

- **Mode:** NONE
- **Rationale:** Pricing date is current (January 2026); no escalation applied per config
- **Decision:** D-012

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
| No tank vendor quotes | Tank supply pricing highly uncertain ($2.5-4M/tank range) | Obtain budgetary quotes from API 650 tank fabricators (Matrix Service, CB&I, Tarsco, CST) |
| No agitator vendor quotes | Agitator cost assumed | Obtain quotes from SPX, Chemineer, Philadelphia Mixing |
| Tank geometry not finalized | Shell weight and cost assumed | Complete DEL-13.03 design calculations |
| Product specification TBD | Internal coating selection assumed | Confirm canola oil properties for coating spec |
| Seismic design not complete | Anchorage costs may increase | Complete seismic analysis per API 650 Appendix E |
| Foundation interface TBD | Tank settlement and anchor design assumed | Coordinate with PKG-05 for foundation requirements |
| Deliverables in INITIALIZED state | Scope not finalized | Progress deliverables to IN_PROGRESS |
| No geotechnical data | Foundation design assumptions | Coordinate with DEL-02.04 geotechnical report |

## References

| Document | Description |
|----------|-------------|
| Decision_Log.md | All decisions D-001 through D-012 |
| Assumptions_Log.md | All assumptions A-001 through A-025+ |
| Detail.csv | Line item detail with traceability |
| QA_Report.md | Quality checks and completeness metrics |
| Risk_Register.md | Risk factors and contingency basis |
