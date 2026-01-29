# Basis of Estimate (BOE)

## Snapshot Identification

| Field | Value |
|-------|-------|
| Snapshot ID | EST_PKG20_DRAFT_2026-01-28_2400 |
| Estimate Label | PKG20_DRAFT |
| Pricing Date | 2026-01 (January 2026 dollars) |
| Currency | CAD |
| Package Scope | PKG-20 Field Instrumentation (5 deliverables) |
| Run Status | WARNINGS |

## Currency & Conversion

- **Currency:** CAD (Canadian dollars)
- **Evidence:** Project location is Fraser Surrey Terminal, Surrey, BC, Canada (decomposition Section 1)
- **Conversion:** None required; single-currency estimate
- **Decision:** D-001 (currency selection)

## Scope Inclusions

This estimate includes the following CBS buckets for PKG-20:

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

### Scope Elements (from Decomposition PKG-20)

- **Field instruments** — Level transmitters, pressure transmitters, temperature elements, flow indicators
- **Transmitters** — 4-20mA and HART protocol transmitters for all process measurements
- **Switches** — Level switches, pressure switches, temperature switches for alarms and interlocks
- **Instrument cabling** — Multi-conductor shielded cables for analog and digital signals
- **Junction boxes** — Field junction boxes, marshalling cabinets, instrument junction enclosures

### System Breakdown (Parametric Basis)

Per the facility scope from decomposition:
- **Storage Tanks (3 units)** — ~8 instruments per tank (level transmitters, level switches, temperature elements, pressure/vacuum)
- **Railcar Unloading (32 stations)** — Flow indicators and temperature at header connections
- **Marine Loading System** — Level, pressure, temperature, flow instrumentation
- **Transfer Piping** — Pressure, temperature, and flow instrumentation throughout
- **Pump Systems** — Suction/discharge pressure, vibration monitoring provisions

### Objectives Served

Per decomposition Section 6:
- OBJ-1 Safe & Reliable Operation
- OBJ-2 Throughput Capacity (instrumentation for operational control)
- OBJ-4 Operational Flexibility (instrumentation for multiple operating modes)

## Scope Exclusions

| Exclusion | Rationale |
|-----------|-----------|
| Owner's costs | Not in Contractor scope per decomposition Section 1.2 |
| Land acquisition | Not in Contractor scope |
| Financing costs | Not in Contractor scope |
| Permits obtained by Employer | Per decomposition Section 1.2 |
| Control systems (PKG-19) | DCS/PLC, HMI, cabinets in separate package |
| Custody transfer meters (PKG-12) | Flow meters in Product Transfer & Metering package |
| Fire detection instruments (PKG-23) | Fire Protection package includes detectors |
| Security system instruments (PKG-24) | Security Systems package includes sensors |
| Escalation | escalation_mode = NONE per config |
| Taxes | Excluded from base estimate |

## Contracting Assumptions

| Assumption | Value | Decision Ref |
|------------|-------|--------------|
| Contract type | Design & Build (D&B) | decomposition Section 1 |
| Contractor responsibility | Full design and construction | decomposition Section 1.2 |
| Instrument supply | Contractor procures from qualified vendors | D-002 |
| Instrument calibration | Vendor calibration with field verification | D-003 |
| Cable supply | Bulk cable supply by Contractor | D-004 |
| Junction boxes | NEMA 4X stainless or painted steel | D-005 |

## Location / Productivity Assumptions

| Assumption | Value | Decision Ref |
|------------|-------|--------------|
| Location | Fraser Surrey Terminal, Site-wide, Surrey, BC | decomposition |
| Productivity factor | 1.0 (BC lower mainland baseline) | D-006 |
| Site conditions | Operating terminal with active operations | A-001 |
| Working hours | Standard 8-10 hour shifts | D-007 |
| Cable routing | Mix of tray, conduit, and direct burial | A-002 |
| Instrument environment | Outdoor marine/industrial environment | A-003 |

## Pricing Sources Hierarchy

1. **Quotes/Vendor Budgets:** None available
2. **Project Rate Tables:** None provided
3. **Allowances:** All line items priced via allowances (fallback typical model)

**Decision:** D-008 — All pricing uses allowances due to absence of vendor quotes or rate tables.

## Quantity Basis

All quantities are parametric estimates based on:
- Facility scope from decomposition (3 tanks, 32 railcar stations, marine loading system)
- Typical instrumentation density for edible oil transload facilities
- Industry typical instrument counts and cable run lengths
- Deliverable document scope descriptions

| Item | Estimated Quantity | Basis | Decision Ref |
|------|-------------------|-------|--------------|
| Tank instruments | 24 units | 3 tanks × 8 instruments each | A-004 |
| Railcar unloading instruments | 40 units | 32 stations + headers | A-005 |
| Marine loading instruments | 12 units | Loading arm + platform | A-006 |
| Transfer/piping instruments | 30 units | Pumps, headers, transfer lines | A-007 |
| Total field instruments | ~106 units | Sum of above | Calculated |
| Instrument cable | ~8,000 m | Typical for facility size | A-008 |
| Junction boxes | ~25 units | Distribution throughout site | A-009 |
| Instrument tubing/fittings | 1 lot | Process connections | A-010 |

## Indirects Model

**Method:** Factor-based (fallback typical model)

| Factor | Rate | Base | Decision Ref |
|--------|------|------|--------------|
| Construction Indirects (CI) | 0.18 | CD | D-009 |
| Procurement Services (P) | 0.02 | MAT | D-009 |
| EPCM/PM | 0.06 | CD + CI + MAT | D-009 |
| Commissioning (COM) | 0.04 | CD + CI + MAT | D-009 |

Note: Commissioning factor elevated to 4% for I&C (loop testing and calibration intensive).

## Contingency Method

**Method:** PCT_BY_BUCKET (percentage by CBS bucket)

| CBS | Base % | Allowance Adjustment | Final % | Rationale |
|-----|--------|---------------------|---------|-----------|
| E | 10% | +10% (100% allowance) | 20% | All engineering allowances |
| MAT | 15% | +10% (100% allowance) | 25% | Instrument selection not finalized |
| CD | 20% | +10% (100% allowance) | 30% | Installation productivity uncertainty |
| CI | 20% | +10% (factor-derived) | 30% | Derived from CD |
| PM | 10% | +5% (factor-derived) | 15% | Factor-based |
| P | 10% | +5% (factor-derived) | 15% | Factor-based |
| COM | 25% | +5% (factor-derived) | 30% | Loop testing complexity |

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
| No instrument index | Instrument count estimated parametrically | Develop preliminary instrument index from P&IDs |
| No vendor quotes | Instrument pricing uncertain | Obtain budgetary quotes from Emerson, Endress+Hauser, Siemens |
| Cable routing not designed | Cable quantities estimated | Complete cable schedule from DEL-20.01 |
| P&IDs not issued | Instrument selection assumed | Issue P&IDs from PKG-14 DEL-14.01 |
| Junction box locations TBD | JB count estimated | Complete DEL-20.01 drawings |
| Deliverables in INITIALIZED state | Scope not finalized | Progress deliverables to IN_PROGRESS |
| Integration with PKG-19 TBD | Control system interface undefined | Coordinate with Control Systems package |
| Hazardous area classification TBD | Instrument ratings assumed | Complete hazardous area study |

## References

| Document | Description |
|----------|-------------|
| Decision_Log.md | All decisions D-001 through D-011 |
| Assumptions_Log.md | All assumptions A-001 through A-020 |
| Detail.csv | Line item detail with traceability |
| QA_Report.md | Quality checks and completeness metrics |
| Risk_Register.md | Risk factors and contingency basis |
