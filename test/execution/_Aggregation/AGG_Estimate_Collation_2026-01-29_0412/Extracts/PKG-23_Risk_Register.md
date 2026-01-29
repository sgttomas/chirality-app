# Risk Register

## Snapshot Identification

| Field | Value |
|-------|-------|
| Snapshot ID | EST_PKG23_DRAFT_2026-01-28_2400 |
| Package | PKG-23 Fire Protection |
| Date | 2026-01-28 |

## Risk Summary

| Category | Risk Count | Contingency Impact |
|----------|------------|-------------------|
| Scope Risk | 3 | $150,000 |
| Price Risk | 2 | $130,000 |
| Execution Risk | 3 | $160,000 |
| Interface Risk | 2 | $110,000 |
| **Total** | **10** | **$550,000** |

---

## Risk Entries

### R-001: Fire Water Demand Uncertainty

**Risk Driver:** Scope/Quantity

**Cause → Consequence:** Fire water demand calculation (DEL-23.03) not complete → Fire water loop sizing, hydrant quantity, and foam system capacity may be underestimated or overestimated.

**Affected Buckets (CBS/WBS):**
- MAT: Fire water piping, hydrants, foam equipment
- CD: Fire water loop installation, foam system installation
- E: Design calculations may require rework

**Suggested Mitigation:** Complete DEL-23.03 fire water demand calculations per NFPA 30 before finalizing material procurement; obtain budgetary quotes based on preliminary sizing.

**Contingency Handling:** 25% contingency applied to MAT bucket to account for quantity uncertainty.

---

### R-002: Fire Pump Requirement

**Risk Driver:** Scope

**Cause → Consequence:** Fire pump requirement not confirmed → If municipal water supply pressure is inadequate, dedicated fire pump may be required, adding $150,000-300,000 to estimate.

**Affected Buckets (CBS/WBS):**
- MAT: Fire pump, controller, accessories (potential addition)
- CD: Fire pump installation (potential addition)
- E: Additional design for fire pump room/enclosure

**Suggested Mitigation:** Confirm municipal fire water supply pressure and flow capacity early; complete DEL-23.03 hydraulic calculations; engage fire pump vendors for budgetary pricing if pump appears likely.

**Contingency Handling:** Fire pump excluded from base estimate per D-011; risk carried in contingency but may require scope addition if pump confirmed.

---

### R-003: Foam System Complexity

**Risk Driver:** Scope/Price

**Cause → Consequence:** Foam suppression system for 3 × 15,000 MT tanks is significant scope with specialized equipment → Foam equipment pricing uncertainty and installation complexity may result in cost overruns.

**Affected Buckets (CBS/WBS):**
- MAT: Foam proportioning system, foam chambers, foam concentrate
- CD: Foam system installation

**Suggested Mitigation:** Engage specialized foam system vendors early; obtain budgetary quotes for complete foam system package; consider design-build approach with foam system vendor.

**Contingency Handling:** 25% contingency applied to foam equipment (MAT); 30% contingency applied to foam installation (CD).

---

### R-004: Fire Alarm Integration Complexity

**Risk Driver:** Interface

**Cause → Consequence:** Fire alarm system integration with facility DCS (PKG-19) may be more complex than assumed → Additional integration engineering, programming, and testing may be required.

**Affected Buckets (CBS/WBS):**
- E: Additional integration engineering
- MAT: Additional interface hardware
- CD: Extended commissioning for integration testing
- COM: Additional testing time

**Suggested Mitigation:** Coordinate early with PKG-19 control systems design; define fire alarm-DCS interface requirements in DEL-23.02 specification; plan for integrated system testing.

**Contingency Handling:** 20% contingency applied to E bucket; 30% contingency applied to COM bucket.

---

### R-005: Fire Protection Equipment Lead Times

**Risk Driver:** Schedule/Price

**Cause → Consequence:** Specialized fire protection equipment (foam proportioning systems, addressable FACP, flame detectors) may have long lead times (12-20 weeks) → Late ordering may impact project schedule; expediting may increase costs.

**Affected Buckets (CBS/WBS):**
- P: Expediting costs
- MAT: Premium pricing for expedited delivery

**Suggested Mitigation:** Identify long-lead equipment early; place orders for critical equipment (foam proportioner, FACP) as soon as design is sufficiently complete; include lead time requirements in procurement specifications.

**Contingency Handling:** 15% contingency applied to P bucket; price escalation risk covered in MAT contingency.

---

### R-006: Terminal Operations Interference

**Risk Driver:** Execution

**Cause → Consequence:** Fire protection installation work (especially fire water loop excavation) may conflict with ongoing terminal operations (OBJ-5) → Reduced productivity, night work premiums, extended schedule.

**Affected Buckets (CBS/WBS):**
- CD: Reduced productivity, shift premiums
- CI: Extended supervision, additional coordination

**Suggested Mitigation:** Develop detailed installation sequence coordinated with terminal operations; identify work windows during lower activity periods; plan for night work for critical tie-ins.

**Contingency Handling:** 30% contingency applied to CD and CI buckets.

---

### R-007: Underground Utility Conflicts

**Risk Driver:** Execution

**Cause → Consequence:** Fire water loop excavation may encounter unknown utilities or require modifications to avoid conflicts with other underground systems (PKG-03, PKG-17) → Rework, redesign, additional excavation.

**Affected Buckets (CBS/WBS):**
- CD: Rework, additional excavation
- E: Design modifications

**Suggested Mitigation:** Coordinate fire water loop routing with PKG-03 underground utilities and PKG-17 electrical duct banks; obtain utility locates before excavation; consider shared trenching opportunities.

**Contingency Handling:** 30% contingency applied to CD bucket; 20% contingency applied to E bucket.

---

### R-008: Escalation Risk

**Risk Driver:** Price

**Cause → Consequence:** Estimate is in January 2026 dollars with no escalation → 2-3 year construction duration may result in 3-6% annual cost increases not captured in estimate.

**Affected Buckets (CBS/WBS):**
- All buckets: Escalation affects all costs

**Suggested Mitigation:** Track inflation indices for fire protection equipment and construction labor; consider escalation allowance for multi-year procurement/construction; lock pricing with early POs where possible.

**Contingency Handling:** Escalation not included in contingency per D-007; potential $120,000-350,000 addition over 2-3 year project duration.

---

### R-009: Code Compliance Requirements

**Risk Driver:** Scope

**Cause → Consequence:** Final code compliance review by AHJ (Authority Having Jurisdiction) may require additional fire protection measures beyond NFPA minimums → Additional equipment, design revisions.

**Affected Buckets (CBS/WBS):**
- E: Design revisions
- MAT: Additional equipment
- CD: Additional installation

**Suggested Mitigation:** Engage with local AHJ (Surrey Fire Department, VFPA) early in design; confirm fire protection requirements; review insurance requirements.

**Contingency Handling:** 20% contingency applied to E bucket; 25% contingency applied to MAT bucket.

---

### R-010: Marine Environment Corrosion

**Risk Driver:** Execution/Lifecycle

**Cause → Consequence:** Marine terminal environment (salt air, humidity) accelerates corrosion of fire protection equipment → Premium materials or coatings may be required; replacement cycles may be shorter.

**Affected Buckets (CBS/WBS):**
- MAT: Marine-grade equipment premiums
- E: Enhanced corrosion protection specifications

**Suggested Mitigation:** Specify marine-grade fire hydrants, stainless steel fasteners, and enhanced coatings in DEL-23.02; consider galvanized or stainless steel pipe for exposed above-ground piping.

**Contingency Handling:** Material pricing assumptions (A-009) include allowance for marine-grade equipment; 25% contingency applied to MAT bucket.

---

## Contingency Summary by CBS

| CBS | Base Cost | Risk Drivers | Contingency % | Contingency Amount |
|-----|-----------|--------------|---------------|-------------------|
| E | $175,000 | R-001, R-004, R-007, R-009 | 20% | $35,000 |
| MAT | $1,045,000 | R-001, R-003, R-005, R-009, R-010 | 25% | $261,000 |
| CD | $600,000 | R-001, R-003, R-006, R-007 | 30% | $180,000 |
| CI | $108,000 | R-006 | 30% | $32,000 |
| P | $21,000 | R-005 | 15% | $3,000 |
| PM | $106,000 | General management risk | 15% | $16,000 |
| COM | $53,000 | R-004 | 30% | $16,000 |
| **Total** | **$2,108,000** | | **26%** | **$543,000** |

---
