# Estimate Summary

## PKG-11 Marine Loading System

### Snapshot Identification

| Field | Value |
|-------|-------|
| Snapshot ID | EST_PKG11_DRAFT_2026-01-28_2359 |
| Estimate Label | PKG11_DRAFT |
| Pricing Date | 2026-01 |
| Currency | CAD |
| Run Status | WARNINGS |

### Summary by CBS

| CBS | Description | Base Amount | Contingency % | Contingency | Total |
|-----|-------------|-------------|---------------|-------------|-------|
| E | Engineering & Design | $125,000 | 20% | $25,000 | $150,000 |
| MAT | Equipment & Materials | $1,485,000 | 25% | $371,000 | $1,856,000 |
| CD | Construction Directs | $595,000 | 30% | $179,000 | $774,000 |
| CI | Construction Indirects | $107,000 | 30% | $32,000 | $139,000 |
| PM | Project Management / EPCM | $119,000 | 15% | $18,000 | $137,000 |
| P | Procurement Services | $30,000 | 15% | $5,000 | $35,000 |
| COM | Commissioning / Testing | $79,000 | 30% | $24,000 | $103,000 |
| **SUBTOTAL** | | **$2,540,000** | | **$654,000** | **$3,194,000** |

### Summary by WBS (Deliverable)

| WBS ID | Deliverable | CBS | Base Amount |
|--------|-------------|-----|-------------|
| DEL-11.01 | Marine Loading Design Drawing Set | E | $45,000 |
| DEL-11.02 | Marine Loading Technical Specification | E | $25,000 |
| DEL-11.03 | Marine Loading Design Calculations | E | $20,000 |
| DEL-11.04 | Marine Loading Data Sheet Package | E | $8,000 |
| DEL-11.05 | Marine Loading Installation & Test Records | E | $15,000 |
| DEL-11.06 | Marine Loading Arm OEM Qualification Package | E | $12,000 |
| N/A | Marine Loading Arm (supply) | MAT | $950,000 |
| N/A | Double-Walled Pipe (supply + install) | CD, MAT | $405,000 |
| N/A | Leak Detection System (supply + install) | CD, MAT | $120,000 |
| N/A | Sump (supply + install) | CD, MAT | $70,000 |
| N/A | Operator Shelter (supply + install) | CD, MAT | $100,000 |
| N/A | Nitrogen Connection (supply + install) | CD, MAT | $30,000 |
| N/A | Pipe Supports (supply + install) | CD, MAT | $80,000 |
| N/A | E&I (supply + install) | CD, MAT | $165,000 |
| N/A | Loading Arm Installation | CD | $120,000 |
| N/A | Testing & Inspection | CD | $40,000 |
| N/A | Construction Indirects | CI | $107,000 |
| N/A | Project Management | PM | $119,000 |
| N/A | Procurement | P | $30,000 |
| N/A | Commissioning | COM | $79,000 |
| | **TOTAL** | | **$2,540,000** |

### Cost Breakdown

| Category | Amount | % of Base |
|----------|--------|-----------|
| Engineering (Deliverables) | $125,000 | 4.9% |
| Materials | $1,485,000 | 58.5% |
| Construction Directs | $595,000 | 23.4% |
| Indirects & Services | $335,000 | 13.2% |
| **Base Estimate** | **$2,540,000** | **100%** |
| Contingency | $654,000 | 25.7% |
| **Total Estimate** | **$3,194,000** | **125.7%** |

### Major Cost Drivers

| Item | Amount | % of Base | Notes |
|------|--------|-----------|-------|
| Marine Loading Arm (supply) | $950,000 | 37.4% | Single largest cost element; highly equipment-dependent |
| Double-Walled Pipe (supply + install) | $405,000 | 15.9% | 150 lm @ ~$2,700/lm all-in |
| E&I (supply + install) | $165,000 | 6.5% | Power and instrumentation for loading arm |
| Loading Arm Installation | $120,000 | 4.7% | Heavy lift marine installation |
| Leak Detection System | $120,000 | 4.7% | 3-zone monitoring with ESD integration |
| Project Management/EPCM | $119,000 | 4.7% | 6% factor on base |

### Confidence Assessment

| Aspect | Rating | Notes |
|--------|--------|-------|
| Quantities | LOW | All assumed from parametric model; pipe routing TBD |
| Pricing | LOW | All allowances; no OEM quotes for loading arm |
| Scope definition | LOW | Deliverables in INITIALIZED state |
| Marine conditions | MEDIUM | Terminal location known; access logistics TBD |
| Loading arm selection | LOW | No OEM selection; wide price range possible |
| **Overall** | **LOW** | Placeholder estimate only |

### Key Assumptions

1. Single marine loading arm for Berth 10 (canola oil service)
2. Loading arm is OCIMF-compliant powered articulated boom with ERC
3. Double-walled export pipe routing of ~150 lm from tank farm to loading position
4. Leak detection system with 3 zones (annulus, drip trays, containment sump)
5. Operator shelter is prefabricated unit with HVAC and controls interface
6. Nitrogen supply skid is Employer-furnished; connection only in Contractor scope (DEC-07)
7. Loading arm foundation by PKG-08 Marine Structures (interface only)
8. BC lower mainland productivity factors (1.0 baseline)
9. Marine work subject to weather windows and terminal operational constraints
10. Standard equipment ratings (no special exotic materials for canola oil)

### Exclusions

- Owner's costs
- Land acquisition
- Permits obtained by Employer
- Nitrogen supply skid (Employer-furnished per DEC-07)
- Marine structures/jetty (PKG-08)
- Storage tanks (PKG-13)
- Process piping beyond loading area (PKG-14)
- Control system (PKG-19) — signals interface only
- Escalation
- Taxes

### Interface Packages

| Package | Interface | Cost Impact |
|---------|-----------|-------------|
| PKG-08 Marine Structures | Loading arm foundation; pipe supports on jetty | Foundation in PKG-08 |
| PKG-13 Storage Tanks | Export pipe tie-in at tank outlet | Flange connection only |
| PKG-14 Process Piping | Pipe routing coordination | Header connection |
| PKG-19 Control Systems | Leak detection signals; loading arm controls | Signal cable termination |
| PKG-20 Field Instrumentation | Level/pressure instruments | Instruments in PKG-20 |
| PKG-03 Underground Utilities | Containment sump drainage | Drain connection |

### Recommendations

1. **Priority:** Obtain budgetary quotes from marine loading arm OEMs (FMC Technologies, SVT, Emco Wheaton, Woodfield)
2. **Priority:** Complete berth layout to confirm pipe routing length and loading arm position
3. Obtain design vessel data (manifold heights, beam, positions) for DEL-11.03 envelope calculations
4. Confirm nitrogen supply interface details with Employer (pressure, flow, connection point)
5. Coordinate PKG-08 for loading arm foundation design requirements
6. Progress deliverables from INITIALIZED to IN_PROGRESS with defined scope
7. Develop DEL-11.06 OEM qualification requirements for procurement

---

*Estimate prepared per AGENT_ESTIMATING straight-through pipeline. All amounts in CAD, rounded to nearest $1,000.*
