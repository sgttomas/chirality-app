# Basis of Estimate (BOE)

## Snapshot Identification

| Field | Value |
|-------|-------|
| Snapshot ID | EST_PKG14_DRAFT_2026-01-28_2400 |
| Estimate Label | PKG14_DRAFT |
| Pricing Date | 2026-01 (January 2026 dollars) |
| Currency | CAD |
| Package Scope | PKG-14 Process Piping (8 deliverables) |
| Run Status | WARNINGS |

## Currency & Conversion

- **Currency:** CAD (Canadian dollars)
- **Evidence:** Project location is Fraser Surrey Terminal, Surrey, BC, Canada (decomposition Section 1)
- **Conversion:** None required; single-currency estimate
- **Decision:** D-001 (currency selection)

## Scope Inclusions

This estimate includes the following CBS buckets for PKG-14:

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

### Scope Elements (from Decomposition PKG-14)

- **Headers** — main product collection headers from railcar unloading to storage tanks
- **Export lines** — single-wall product piping from tank farm discharge to marine loading interface
- **Recycle lines** — return and recirculation piping for tank transfers and line drainback
- **Nitrogen distribution** — N2 piping network from Employer skid to tanks, marine loading, and blanketing points
- **Pipe supports** — all process piping supports including racks, guides, anchors, and expansion provisions

### System Description

The process piping system transfers CSD canola oil through the facility flow path:
1. **Rail Unloading Header System:** 32 railcar unloading stations on 2 tracks flow by gravity to collection headers
2. **Tank Farm Piping:** Inlet headers to 3 × 15,000 MT storage tanks with outlet manifolding
3. **Export System:** Pump discharge piping to marine loading system (interface with PKG-11 double-walled pipe)
4. **Recirculation:** Tank-to-tank transfer and line drain capability
5. **Nitrogen System:** Inert gas distribution for blanketing and purging operations

### Objectives Served

Per decomposition Section 6:
- OBJ-2 Throughput Capacity (1,000,000 MT/annum) — piping system sized for design rates
- OBJ-4 Operational Flexibility — multiple operating modes via piping configuration
- OBJ-8 Future Expandability (Phase 2) — Phase 2 connection provisions per DEL-14.01

## Scope Exclusions

| Exclusion | Rationale |
|-----------|-----------|
| Owner's costs | Not in Contractor scope per decomposition Section 1.2 |
| Land acquisition | Not in Contractor scope |
| Financing costs | Not in Contractor scope |
| Permits obtained by Employer | Per decomposition Section 1.2 |
| Nitrogen supply skid | Employer-supplied per DEC-07; piping distribution only |
| Railcar unloading arms (PKG-10) | Separate package; flange connection at header |
| Double-walled export pipe (PKG-11) | In PKG-11; single-wall pipe to interface point |
| Storage tanks (PKG-13) | Separate package; nozzle connection only |
| Pumps (PKG-15) | Separate package; piping to suction/discharge nozzles |
| Valves (PKG-16) | Separate package; valve bodies and actuators |
| Control systems (PKG-19) | Separate package; signal interfaces only |
| Instrumentation (PKG-20) | Separate package; process connections only |
| Escalation | escalation_mode = NONE per config |
| Taxes | Excluded from base estimate |

## Contracting Assumptions

| Assumption | Value | Decision Ref |
|------------|-------|--------------|
| Contract type | Design & Build (D&B) | decomposition Section 1 |
| Contractor responsibility | Full design and construction | decomposition Section 1.2 |
| Piping fabrication | Shop prefabrication with field assembly | D-002 |
| Welding | Coded welders per ASME B31.3 | D-003 |
| NDE requirements | 100% RT for headers; visual + spot RT for laterals | D-004 |
| Insulation | Heat tracing and insulation for cold weather protection | A-008 |

## Location / Productivity Assumptions

| Assumption | Value | Decision Ref |
|------------|-------|--------------|
| Location | Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC | decomposition |
| Productivity factor | 1.0 (BC lower mainland baseline) | D-005 |
| Site access | Industrial port with established access roads | D-006 |
| Working conditions | Outdoor work; weather-sensitive during winter | A-022 |
| Working hours | Standard 8-10 hour shifts; overtime for schedule recovery | D-007 |

## Pricing Sources Hierarchy

1. **Quotes/Vendor Budgets:** None available
2. **Project Rate Tables:** None provided
3. **Allowances:** All line items priced via allowances (fallback typical model)

**Decision:** D-008 — All pricing uses allowances due to absence of vendor quotes or rate tables.

## Quantity Basis

All quantities are parametric estimates based on:
- Facility layout for 32 railcar unloading stations on 2 tracks
- 3 × 15,000 MT storage tank configuration
- Typical pipeline terminal piping arrangements
- Process flow requirements for 1,000,000 MT/annum throughput

| Item | Estimated Quantity | Basis | Decision Ref |
|------|-------------------|-------|--------------|
| Rail unloading headers (16-20 inch) | 250 lm | 2 tracks × ~125m collection headers | A-001 |
| Header laterals (8-10 inch) | 100 lm | 32 stations × ~3m each | A-001 |
| Tank inlet headers (16-20 inch) | 150 lm | Tank farm distribution manifold | A-002 |
| Tank outlet manifold (16-20 inch) | 100 lm | 3 tanks to pump suction | A-002 |
| Export piping (12-16 inch) | 350 lm | Pump discharge to PKG-11 interface | A-003 |
| Recycle piping (8-12 inch) | 150 lm | Return lines and tank transfer | A-004 |
| Nitrogen distribution (2-4 inch) | 400 lm | N2 to tanks, marine loading, headers | A-005 |
| Small bore utility (1-2 inch) | 200 lm | Drains, vents, sample points | A-006 |
| Pipe supports | 300 units | Approx 1 per 5-6 lm for major lines | A-007 |
| **Total piping** | **~1,700 lm** | All process piping in PKG-14 scope | D-009 |

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
| E | 10% | +10% (100% allowance) | 20% | All engineering allowances; transient analysis complexity |
| MAT | 15% | +10% (100% allowance) | 25% | All material allowances; large diameter pipe costs |
| CD | 20% | +10% (100% allowance) | 30% | Pipe fabrication/welding uncertainty |
| CI | 20% | +10% (factor-derived) | 30% | Derived from CD |
| PM | 10% | +5% (factor-derived) | 15% | Factor-based |
| P | 10% | +5% (factor-derived) | 15% | Factor-based |
| COM | 25% | +5% (factor-derived) | 30% | Piping commissioning, flushing, testing |

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
| No P&IDs or piping GAs | Layout/routing unknown; quantities assumed | Complete DEL-14.01 drawings |
| No line list | Pipe sizes and specs not confirmed | Complete DEL-14.04 line list |
| No stress analysis | Support quantities and expansion provisions assumed | Complete DEL-14.03 stress analysis |
| No transient studies | Surge protection requirements unknown | Complete DEL-14.06, DEL-14.07 |
| No piping material spec | Material allowances based on typical carbon steel | Complete DEL-14.02 specification |
| Deliverables in INITIALIZED state | Scope not finalized | Progress deliverables to IN_PROGRESS |
| Tank nozzle locations undefined | Tank farm piping layout assumed | Coordinate with PKG-13 for nozzle schedule |
| Rail unloading header routing unknown | Header length assumed from track geometry | Coordinate with PKG-10 for header interface |

## References

| Document | Description |
|----------|-------------|
| Decision_Log.md | All decisions D-001 through D-012 |
| Assumptions_Log.md | All assumptions A-001 through A-025+ |
| Detail.csv | Line item detail with traceability |
| QA_Report.md | Quality checks and completeness metrics |
| Risk_Register.md | Risk factors and contingency basis |
