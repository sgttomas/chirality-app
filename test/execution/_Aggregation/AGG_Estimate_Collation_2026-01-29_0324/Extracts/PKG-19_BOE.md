# Basis of Estimate (BOE)

## Snapshot Identification

| Field | Value |
|-------|-------|
| Snapshot ID | EST_PKG19_DRAFT_2026-01-28_0015 |
| Estimate Label | PKG19_DRAFT |
| Pricing Date | 2026-01 (January 2026 dollars) |
| Currency | CAD |
| Package Scope | PKG-19 Control Systems (5 deliverables) |
| Run Status | WARNINGS |

## Currency & Conversion

- **Currency:** CAD (Canadian dollars)
- **Evidence:** Project location is Fraser Surrey Terminal, Surrey, BC, Canada (decomposition Section 1)
- **Conversion:** None required; single-currency estimate
- **Decision:** D-001 (currency selection)

## Scope Inclusions

This estimate includes the following CBS buckets for PKG-19:

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

### Scope Elements (from Decomposition PKG-19)

- **DCS/PLC System** — Distributed Control System or Programmable Logic Controller for facility control
- **HMI Workstations** — Operator workstations in control room (typically 2-3 redundant stations)
- **Remote HMIs** — Field operator interface stations at key process areas
- **I/O Racks** — Input/output modules for interfacing with field instrumentation
- **Historian** — Process data historian for data archiving, trending, and reporting
- **Operator Graphics** — HMI screen development for all process areas
- **Network Infrastructure** — Industrial Ethernet, fiber optic backbone, network switches
- **Control Cabinets** — Marshalling panels, I/O cabinets, junction boxes
- **Control System Software** — PLC/DCS application software, HMI graphics, historian configuration

### Control System Functional Scope

| Function | Description |
|----------|-------------|
| Railcar Unloading Control | 32 railcar position control, valve sequencing, flow monitoring |
| Storage Tank Control | 3 × 15,000 MT tanks (level, temperature, agitator control) |
| Marine Loading Control | Loading arm control, flow control, ship-shore interface |
| Custody Transfer | Metering interface (PKG-12) for billing accuracy (OBJ-10) |
| Process Interlocks | Safety interlocks, emergency shutdown coordination |
| Alarm Management | ISA 18.2 alarm management, event logging |

### Objectives Served

Per decomposition Section 6:
- OBJ-1 Safe & Reliable Operation
- OBJ-4 Operational Flexibility
- OBJ-10 Custody Transfer Accuracy

## Scope Exclusions

| Exclusion | Rationale |
|-----------|-----------|
| Owner's costs | Not in Contractor scope per decomposition Section 1.2 |
| Land acquisition | Not in Contractor scope |
| Financing costs | Not in Contractor scope |
| Permits obtained by Employer | Per decomposition Section 1.2 |
| Field instrumentation (PKG-20) | Separate package; I/O interface only |
| Electrical power distribution (PKG-17) | Separate package; power supply interface only |
| Safety Instrumented System (SIS) | If SIS required, to be priced separately; assume BPCS only |
| Communications & IT infrastructure (PKG-25) | Separate package; interface only |
| Security systems (PKG-24) | Separate package |
| Escalation | escalation_mode = NONE per config |
| Taxes | Excluded from base estimate |

## Contracting Assumptions

| Assumption | Value | Decision Ref |
|------------|-------|--------------|
| Contract type | Design & Build (D&B) | decomposition Section 1 |
| Contractor responsibility | Full design, supply, install, commission | decomposition Section 1.2 |
| Control system vendor | Single-vendor integrated DCS/PLC solution | D-002 |
| Control system platform | Modern DCS/PLC (e.g., Honeywell, Emerson, ABB, Siemens class) | D-003 |
| HMI platform | Vendor-integrated HMI with DCS/PLC | D-004 |
| Historian platform | Vendor-integrated or OSIsoft PI class | D-005 |
| Software development | By control system vendor or integrator | D-006 |

## Location / Productivity Assumptions

| Assumption | Value | Decision Ref |
|------------|-------|--------------|
| Location | Fraser Surrey Terminal, Surrey, BC | decomposition |
| Productivity factor | 1.0 (BC lower mainland baseline) | D-007 |
| Control room location | MCC building per PKG-21/22 | A-001 |
| Site access | Normal industrial access | A-002 |
| Working hours | Standard 8-10 hour shifts | D-008 |

## Pricing Sources Hierarchy

1. **Quotes/Vendor Budgets:** None available
2. **Project Rate Tables:** None provided
3. **Allowances:** All line items priced via allowances (fallback typical model)

**Decision:** D-009 — All pricing uses allowances due to absence of vendor quotes or rate tables.

## Quantity Basis

All quantities are parametric estimates based on:
- Facility control scope (32 railcar stations, 3 storage tanks, marine loading)
- Typical I/O count estimation (~500-800 I/O points for this facility size)
- Industry typical values for DCS/PLC systems of similar scope

| Item | Estimated Quantity | Basis | Decision Ref |
|------|-------------------|-------|--------------|
| DCS/PLC controllers | 2 (redundant pair) | Typical for facility size | A-003 |
| HMI workstations | 3 stations | 2 control room + 1 engineering | A-004 |
| Remote HMI panels | 3 units | Railcar, tank farm, marine areas | A-005 |
| I/O points (estimated) | 600-800 points | 32 railcars + 3 tanks + marine + metering | A-006 |
| I/O modules (typical) | 40-50 modules | Based on I/O count estimate | A-007 |
| Historian tags | 400-600 tags | Process and calculated tags | A-008 |
| Network switches | 8-10 units | Control room + field locations | A-009 |
| Fiber optic runs | 2,000 m | Tank farm to control room + marine | A-010 |
| Control cabinets | 6-8 cabinets | Main panel + field JBs | A-011 |
| HMI graphics screens | 40-60 screens | Facility overview + area + equipment | A-012 |

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
| MAT | 15% | +10% (100% allowance) | 25% | Control system pricing variable by vendor |
| CD | 20% | +10% (100% allowance) | 30% | Installation productivity uncertainty |
| CI | 20% | +10% (factor-derived) | 30% | Derived from CD |
| PM | 10% | +5% (factor-derived) | 15% | Factor-based |
| P | 10% | +5% (factor-derived) | 15% | Factor-based |
| COM | 25% | +5% (factor-derived) | 30% | Control system commissioning complexity |

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
| No control system vendor quotes | Hardware and software pricing uncertain | Obtain budgetary quotes from DCS/PLC vendors (Honeywell, Emerson, ABB, Siemens, Yokogawa) |
| I/O count not finalized | I/O rack quantity uncertain | Complete PKG-20 field instrumentation design |
| Control strategies not defined | Software development scope uncertain | Complete process P&IDs (PKG-14) and control narratives |
| No HMI graphics standards | HMI development effort uncertain | Define project HMI style guide |
| Historian tag count TBD | Historian sizing uncertain | Complete I/O list and identify calculated tags |
| SIS scope not confirmed | Potential for separate SIS if required | Confirm SIL requirements from HAZOP (PKG-27) |
| Network architecture not defined | Network equipment count uncertain | Complete control system architecture design |
| Deliverables in INITIALIZED state | Scope not finalized | Progress deliverables to IN_PROGRESS |

## References

| Document | Description |
|----------|-------------|
| Decision_Log.md | All decisions D-001 through D-012 |
| Assumptions_Log.md | All assumptions A-001 through A-020 |
| Detail.csv | Line item detail with traceability |
| QA_Report.md | Quality checks and completeness metrics |
| Risk_Register.md | Risk factors and contingency basis |
