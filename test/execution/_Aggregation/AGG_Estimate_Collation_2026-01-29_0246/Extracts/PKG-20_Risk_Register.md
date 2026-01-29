# Risk Register — PKG-20 Field Instrumentation

## Overview

This register identifies risks that could impact the PKG-20 Field Instrumentation estimate. Each risk is assigned a unique ID (R-###) and includes mitigation recommendations and contingency handling.

---

## Risks

### R-001: Instrument Count Uncertainty

| Field | Value |
|-------|-------|
| Risk Driver | Scope/Quantity |
| Cause | P&IDs not issued; instrument count estimated parametrically |
| Consequence | Actual instrument count could vary ±30% from estimate |
| Affected CBS/WBS | MAT, CD, COM |
| Probability | High |
| Impact | Medium |
| Suggested Mitigation | Develop preliminary instrument index from process scope |
| Contingency Handling | 25% contingency on MAT; 30% on CD |

---

### R-002: Cable Routing and Length Uncertainty

| Field | Value |
|-------|-------|
| Risk Driver | Scope/Quantity |
| Cause | Cable routing not designed; lengths estimated from typical runs |
| Consequence | Actual cable quantity could vary ±40% |
| Affected CBS/WBS | MAT, CD |
| Probability | High |
| Impact | Medium |
| Suggested Mitigation | Complete cable schedule and routing study |
| Contingency Handling | 25% contingency on MAT; 30% on CD |

---

### R-003: Hazardous Area Classification

| Field | Value |
|-------|-------|
| Risk Driver | Scope |
| Cause | Hazardous area classification study not complete |
| Consequence | Instruments may require explosion-proof ratings (cost premium 2-3×) |
| Affected CBS/WBS | MAT |
| Probability | Medium |
| Impact | High |
| Suggested Mitigation | Complete hazardous area classification study |
| Contingency Handling | Contingency covers potential upgrade to Ex-rated instruments |

---

### R-004: Instrument Vendor Lead Times

| Field | Value |
|-------|-------|
| Risk Driver | Schedule |
| Cause | Specialized instruments may have long lead times |
| Consequence | Schedule delays or premium for expedited delivery |
| Affected CBS/WBS | P, MAT |
| Probability | Medium |
| Impact | Medium |
| Suggested Mitigation | Early procurement; use standard instrument types where possible |
| Contingency Handling | Procurement contingency (15%) covers expediting |

---

### R-005: Control System Integration

| Field | Value |
|-------|-------|
| Risk Driver | Interface |
| Cause | PKG-19 Control Systems scope and I/O requirements not defined |
| Consequence | Rework, additional junction boxes, or cable changes |
| Affected CBS/WBS | E, MAT, CD |
| Probability | Medium |
| Impact | Medium |
| Suggested Mitigation | Early coordination with PKG-19 for I/O list and cable requirements |
| Contingency Handling | 20% contingency on E; allowance for interface rework |

---

### R-006: Marine Environment Corrosion

| Field | Value |
|-------|-------|
| Risk Driver | Technical |
| Cause | Fraser River waterfront location exposes instruments to salt air |
| Consequence | Premium materials required; maintenance implications |
| Affected CBS/WBS | MAT |
| Probability | High |
| Impact | Low |
| Suggested Mitigation | Specify marine-grade materials (SS 316, NEMA 4X) |
| Contingency Handling | SS materials included in base estimate |

---

### R-007: Site Access During Operations

| Field | Value |
|-------|-------|
| Risk Driver | Productivity |
| Cause | Active terminal operations may restrict work areas/hours |
| Consequence | Reduced productivity; extended installation duration |
| Affected CBS/WBS | CD, CI |
| Probability | Medium |
| Impact | Medium |
| Suggested Mitigation | Coordinate access windows with Terminal operations |
| Contingency Handling | CI factor (18%) and 30% CD contingency |

---

### R-008: Calibration Equipment Availability

| Field | Value |
|-------|-------|
| Risk Driver | Resources |
| Cause | Specialized calibration equipment required for 106 instruments |
| Consequence | Rental costs or delays if equipment unavailable |
| Affected CBS/WBS | CD |
| Probability | Low |
| Impact | Low |
| Suggested Mitigation | Reserve calibration equipment early; consider third-party calibration |
| Contingency Handling | Calibration cost allowance at $280/instrument |

---

### R-009: Canola Oil Product Compatibility

| Field | Value |
|-------|-------|
| Risk Driver | Technical |
| Cause | Instrument wetted materials must be compatible with edible oil |
| Consequence | Material upgrades or coating requirements |
| Affected CBS/WBS | MAT |
| Probability | Low |
| Impact | Low |
| Suggested Mitigation | Confirm material compatibility in DEL-20.02 |
| Contingency Handling | SS 316 materials assumed in base estimate |

---

### R-010: Loop Testing Coordination

| Field | Value |
|-------|-------|
| Risk Driver | Interface |
| Cause | Loop testing requires coordination with PKG-19 DCS team |
| Consequence | Delays if DCS not ready; rework if loops misconfigured |
| Affected CBS/WBS | CD, COM |
| Probability | Medium |
| Impact | Medium |
| Suggested Mitigation | Develop integrated commissioning schedule with PKG-19 |
| Contingency Handling | COM elevated to 4% for I&C; 30% contingency |

---

### R-011: Instrument Supply Chain Disruption

| Field | Value |
|-------|-------|
| Risk Driver | Procurement |
| Cause | Global supply chain variability for instrumentation |
| Consequence | Price increases or delivery delays |
| Affected CBS/WBS | MAT |
| Probability | Medium |
| Impact | Medium |
| Suggested Mitigation | Qualified vendor list; early commitment on long-lead items |
| Contingency Handling | 25% contingency on MAT |

---

### R-012: Winter Weather Impact

| Field | Value |
|-------|-------|
| Risk Driver | Productivity |
| Cause | Outdoor installation during BC winter (rain, cold) |
| Consequence | Reduced productivity; weather delays |
| Affected CBS/WBS | CD |
| Probability | Medium |
| Impact | Low |
| Suggested Mitigation | Schedule sensitive work for favorable weather; weather protection |
| Contingency Handling | 30% contingency on CD |

---

## Risk Summary

| Risk Level | Count | Description |
|------------|-------|-------------|
| High Probability / High Impact | 0 | — |
| High Probability / Medium Impact | 2 | R-001, R-002 |
| Medium Probability / High Impact | 1 | R-003 |
| Medium Probability / Medium Impact | 5 | R-004, R-005, R-007, R-010, R-011 |
| Low/Medium Probability / Low Impact | 4 | R-006, R-008, R-009, R-012 |

## Contingency Allocation

Based on risk assessment, contingency is allocated as follows:

| CBS | Base Contingency | Risk Adjustment | Final Contingency |
|-----|------------------|-----------------|-------------------|
| E | 10% | +10% (allowance) | 20% |
| MAT | 15% | +10% (R-001, R-002, R-003, R-011) | 25% |
| CD | 20% | +10% (R-001, R-002, R-007, R-012) | 30% |
| CI | 20% | +10% (factor-derived) | 30% |
| PM | 10% | +5% (factor-derived) | 15% |
| P | 10% | +5% (R-004) | 15% |
| COM | 25% | +5% (R-010) | 30% |

**Overall Contingency:** ~26.6% ($408,000)

---

## Risk Monitoring Recommendations

1. **Monthly Review** — Update risk register as design progresses
2. **P&ID Completion** — R-001 and R-002 can be closed when P&IDs issued
3. **Hazardous Area Study** — R-003 can be closed when study complete
4. **Vendor Qualification** — R-004 and R-011 monitored through procurement
5. **Coordination Meetings** — R-005 and R-010 addressed through PKG-19 interface meetings

---

*Risk Register generated by ESTIMATING Agent | 2026-01-28*
