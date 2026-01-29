# Risk Register — PKG-22 Building Interior & MEP

**Snapshot ID:** EST_PKG22_DRAFT_2026-01-28_2358
**Package:** PKG-22 Building Interior & MEP
**Date:** 2026-01-28

---

## Purpose

This document identifies and assesses risks that affect the PKG-22 estimate, including pricing uncertainty, scope uncertainty, execution risks, and interface risks.

---

## Risk Entries

### R-001: Building Size Uncertainty

**Risk Driver:** Scope / Quantity

**Cause:** No building design drawings available from PKG-21 (DEL-21.01 INITIALIZED); building floor area assumption (300 m²) may vary significantly

**Consequence:** MEP system sizes and costs scale directly with building area; ±33% building size variation → ±25-35% cost variation for MEP systems

**Affected Buckets:** MAT (all MEP systems), CD (all MEP installation), E (design effort scales with building size)

**Suggested Mitigation:** Complete PKG-21 DEL-21.01 building design drawings to determine actual floor area and room layouts before finalizing MEP design

**Contingency Handling:** Included in elevated MAT/CD contingency rates (25-30%)

**Cross-reference:** A-022 (building size assumption), D-012 (building size decision)

---

### R-002: HVAC Load Calculation Uncertainty

**Risk Driver:** Scope / Quantity / Price

**Cause:** No HVAC load calculations available (DEL-22.03 INITIALIZED); building envelope properties, internal gains, and occupancy TBD

**Consequence:** HVAC equipment capacity may be undersized or oversized; ±20-40% equipment size variation → ±15-30% HVAC cost variation

**Affected Buckets:** MAT (HVAC equipment L-006), CD (HVAC installation L-011)

**Suggested Mitigation:** Complete DEL-22.03 HVAC load calculations using building design from PKG-21 and occupancy data from Employer's Requirements

**Contingency Handling:** Included in MAT/CD contingency (25-30%); HVAC allowance sized for mid-range capacity

**Cross-reference:** A-001 (HVAC capacity assumption)

---

### R-003: Fire Suppression System Scope Uncertainty

**Risk Driver:** Scope / Regulatory

**Cause:** No NFPA 13 hydraulic calculations (DEL-22.03 INITIALIZED); occupancy classification TBD; fire water supply adequacy TBD (coordination with PKG-23 required)

**Consequence:** Sprinkler system design density, pipe sizing, and hydraulic demand may vary; inadequate fire water supply may require fire pump addition (+$80k-$150k)

**Affected Buckets:** MAT (fire suppression L-008), CD (fire suppression installation L-013)

**Suggested Mitigation:**
1. Confirm building occupancy classification per NBC 2020
2. Complete DEL-22.03 fire protection hydraulic calculations
3. Coordinate with PKG-23 to verify site fire water supply adequacy (pressure and flow)
4. Early engagement with AHJ (Authority Having Jurisdiction) for code interpretation

**Contingency Handling:** Included in MAT/CD contingency (25-30%); fire pump excluded from base estimate (potential add)

**Cross-reference:** A-003 (fire suppression assumption), A-016 (PKG-23 interface)

---

### R-004: Vendor Quote Unavailability

**Risk Driver:** Price

**Cause:** No vendor quotes available for HVAC equipment, fire suppression system, or plumbing equipment; 100% allowance-based pricing

**Consequence:** Actual equipment pricing may vary ±20-40% from allowances; market pricing volatility for HVAC equipment (supply chain, demand fluctuations)

**Affected Buckets:** MAT (all equipment L-006 through L-010)

**Suggested Mitigation:** Obtain budgetary quotes from at least 2-3 vendors for major equipment (HVAC, fire suppression, plumbing) to validate allowances

**Contingency Handling:** Included in MAT contingency (25%); elevated due to 100% allowance pricing

**Cross-reference:** A-001, A-002, A-003 (equipment allowances), D-008 (no quotes decision)

---

### R-005: Construction Labor Availability and Rates (BC Lower Mainland)

**Risk Driver:** Price / Productivity

**Cause:** BC Lower Mainland tight labor market; construction labor demand may affect availability and rates; MEP trades (HVAC, plumber, sprinkler fitter, electrician) particularly affected

**Consequence:** Labor rates may increase 10-20% beyond assumptions; productivity may decrease if less-experienced labor used; schedule delays if labor unavailable

**Affected Buckets:** CD (all installation L-011 through L-015)

**Suggested Mitigation:**
1. Early contractor engagement to secure labor commitments
2. Consider pre-fabrication and modularization to reduce field labor
3. Flexible scheduling to accommodate labor availability

**Contingency Handling:** Included in CD contingency (30%); labor rate assumptions based on current BC union rates

**Cross-reference:** A-010 (labor rate assumptions), A-012 (productivity assumptions)

---

### R-006: PKG-21 Building Structure Coordination

**Risk Driver:** Interface / Schedule

**Cause:** Building structure design (PKG-21) not available; MEP equipment supports, penetrations, and clearances TBD

**Consequence:** MEP design rework if coordination issues arise; potential equipment relocation or design changes; field coordination conflicts → schedule delays and rework costs

**Affected Buckets:** E (potential rework), CD (potential field rework), schedule impact

**Suggested Mitigation:**
1. Establish interdisciplinary coordination process early
2. 3D BIM coordination between PKG-21 and PKG-22
3. Hold coordination workshops before finalizing designs

**Contingency Handling:** Rework risk included in E/CD contingency (20-30%); schedule buffer recommended

**Cross-reference:** A-017 (PKG-21 coordination assumption)

---

### R-007: PKG-19 Control System Interface Scope Split

**Risk Driver:** Scope / Interface

**Cause:** Control system scope split between PKG-19 (BAS/DCS) and PKG-22 (HVAC equipment controls) not clearly defined

**Consequence:** Scope gaps or overlaps; control system integration issues; additional costs for interface equipment or programming

**Affected Buckets:** MAT (potential control interface equipment), E (potential additional engineering for control integration)

**Suggested Mitigation:**
1. Clarify control system scope split in Employer's Requirements or design basis
2. Early coordination workshop between PKG-19 and PKG-22 disciplines
3. Define interface points and responsibilities in control system specification

**Contingency Handling:** Included in MAT contingency (25%); control interface allowance in HVAC equipment pricing

**Cross-reference:** A-014 (control system interface assumption)

---

### R-008: Escalation Risk (2-3 Year Project Duration)

**Risk Driver:** Price / Schedule

**Cause:** Estimate priced in January 2026 dollars; no escalation included; project execution over 2-3 years expected

**Consequence:** Material and labor cost escalation 3-6% per year → $84k-$202k potential escalation exposure over 2-3 years for PKG-22

**Affected Buckets:** All (primarily MAT and CD)

**Suggested Mitigation:**
1. Early procurement of long-lead equipment (HVAC, fire suppression)
2. Fixed-price contracts where possible
3. Escalation clauses in contracts for labor and commodity materials

**Contingency Handling:** NOT included in base estimate; escalation risk noted as separate exposure

**Estimated Exposure:** 3% annual escalation × $1,687k base × 2.5 years midpoint = $126k exposure

**Cross-reference:** D-003 (pricing date), D-009 (escalation mode NONE)

---

### R-009: Interior Finishes Scope Definition

**Risk Driver:** Scope

**Cause:** Interior finishes scope interpretation based on limited information; finish levels and extent TBD

**Consequence:** Actual finishes may be higher or lower specification than assumed; finish area may vary ±20-30%

**Affected Buckets:** MAT (finishes L-010), CD (finishes installation L-015)

**Suggested Mitigation:** Complete PKG-21/PKG-22 building design with finish schedules; clarify finish levels with Owner (industrial vs. commercial vs. architectural grade)

**Contingency Handling:** Included in MAT/CD contingency (25-30%); industrial-grade finishes assumed

**Cross-reference:** A-005 (interior finishes assumption), D-013 (finishes scope interpretation)

---

### R-010: Plumbing Fixture Count and Hot Water Requirements

**Risk Driver:** Scope / Quantity

**Cause:** No plumbing layout or fixture schedule (DEL-22.01 INITIALIZED); building occupancy and hot water requirements TBD

**Consequence:** Fixture count may vary ±30-50%; hot water heater may not be required (savings) or larger capacity required (cost increase)

**Affected Buckets:** MAT (plumbing L-007), CD (plumbing installation L-012)

**Suggested Mitigation:** Confirm building occupancy type and occupant count; determine hot water requirements (handwashing only vs. showers/cleanup)

**Contingency Handling:** Included in MAT/CD contingency (25-30%); mid-range fixture count assumed

**Cross-reference:** A-002 (plumbing fixtures assumption)

---

### R-011: Fire Alarm System Interface (PKG-23 vs PKG-22)

**Risk Driver:** Scope / Interface

**Cause:** Fire alarm system scope split between PKG-23 (site fire protection) and PKG-22 (building fire suppression) not clearly defined

**Consequence:** Scope gap for fire alarm panel, detection devices, and monitoring; potential additional costs for fire alarm system

**Affected Buckets:** MAT (potential fire alarm panel and devices $15k-$35k)

**Suggested Mitigation:** Clarify fire alarm system scope; coordinate with PKG-23 deliverables; confirm if building fire alarm panel included in PKG-22 or PKG-23

**Contingency Handling:** Included in MAT contingency (25%); fire alarm interface allowed in fire suppression system pricing (L-008)

**Cross-reference:** A-003 (fire suppression assumption note on fire alarm interface)

---

### R-012: Commissioning and Testing Scope (PKG-30 vs PKG-22)

**Risk Driver:** Scope / Interface

**Cause:** Commissioning scope split between PKG-30 (overall commissioning) and PKG-22 (MEP system commissioning) not clearly defined; testing scope in DEL-22.05 TBD

**Consequence:** Commissioning effort may be underestimated or duplicated; independent commissioning agent costs TBD

**Affected Buckets:** COM (commissioning L-019); potential additional commissioning agent costs

**Suggested Mitigation:** Clarify commissioning scope and responsibilities; coordinate with PKG-30 deliverables; confirm if independent commissioning agent required

**Contingency Handling:** Included in COM contingency (30%); factor-based COM allowance assumes contractor-led commissioning

**Cross-reference:** A-013 (testing and commissioning scope assumption)

---

## Risk Summary by Category

| Category | Number of Risks | Primary Impact | Mitigation Priority |
|----------|----------------|----------------|---------------------|
| Scope / Quantity | 6 | High | High (complete design; clarify requirements) |
| Price / Market | 3 | High | High (obtain vendor quotes; monitor market) |
| Interface / Coordination | 4 | Medium | High (establish coordination processes early) |
| Regulatory / Code | 1 | Medium | Medium (engage AHJ early) |
| Schedule | 2 | Medium | Medium (early procurement; coordination) |

---

## Quantified Risk Exposure Summary

| Risk ID | Description | Probability | Impact Range | Expected Value |
|---------|-------------|-------------|--------------|----------------|
| R-001 | Building size ±33% | High | ±$420k-$590k | Mitigated by contingency |
| R-002 | HVAC capacity ±20% | Medium | ±$88k-$136k | Mitigated by contingency |
| R-003 | Fire pump addition | Low | $80k-$150k | Not included; potential add |
| R-004 | Vendor pricing ±20% | Medium | ±$135k | Mitigated by contingency |
| R-005 | Labor rate +10-20% | Medium | $63k-$126k | Mitigated by contingency |
| R-008 | Escalation 3-6%/yr | High | $84k-$202k | NOT mitigated; separate exposure |
| R-011 | Fire alarm scope gap | Low | $15k-$35k | Mitigated by contingency |

**Note:** Contingency covers identified risks R-001, R-002, R-004, R-005, R-011. Escalation (R-008) and fire pump (R-003) are separate exposures not included in base estimate.

---

**Risk Register Prepared By:** Estimating Agent
**Date:** 2026-01-28
**Snapshot:** EST_PKG22_DRAFT_2026-01-28_2358
**Status:** Complete (12 risks identified and assessed)
