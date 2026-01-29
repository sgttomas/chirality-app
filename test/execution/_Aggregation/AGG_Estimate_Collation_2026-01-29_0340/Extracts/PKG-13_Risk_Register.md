# Risk Register

## PKG-13 Storage Tanks Estimate

### Snapshot Identification

| Field | Value |
|-------|-------|
| Snapshot ID | EST_PKG13_DRAFT_2026-01-28_2400 |
| Estimate Label | PKG13_DRAFT |
| Date | 2026-01-28 |

---

## Risk Entries

### R-001: Steel Price Volatility

| Field | Value |
|-------|-------|
| Risk Driver | Price uncertainty |
| Cause → Consequence | Steel commodity market fluctuations → Tank supply cost could vary ±20% |
| Affected CBS/WBS | MAT ($9.6M tank supply) |
| Suggested Mitigation | Lock in steel pricing early; consider price escalation clause; obtain firm quotes |
| Contingency Handling | 25% MAT contingency ($2.96M) partially covers steel volatility |

---

### R-002: Tank Fabricator Capacity

| Field | Value |
|-------|-------|
| Risk Driver | Schedule uncertainty |
| Cause → Consequence | Limited qualified API 650 fabricators → Longer lead time or premium pricing |
| Affected CBS/WBS | MAT, CD |
| Suggested Mitigation | Early engagement with fabricators (Matrix, CB&I, Tarsco, CST); pre-qualify vendors |
| Contingency Handling | Contingency covers potential premium; schedule float needed |

---

### R-003: Seismic Design Complexity

| Field | Value |
|-------|-------|
| Risk Driver | Scope uncertainty |
| Cause → Consequence | BC seismic requirements per API 650 Appendix E → Increased anchorage, thicker shells |
| Affected CBS/WBS | E, MAT, CD |
| Suggested Mitigation | Complete seismic analysis early; confirm site class and design parameters |
| Contingency Handling | Elevated E contingency (20%) covers additional design; MAT contingency covers material |

---

### R-004: Foundation Interface

| Field | Value |
|-------|-------|
| Risk Driver | Interface uncertainty |
| Cause → Consequence | Foundation design (PKG-05) not coordinated → Tank erection delays, rework |
| Affected CBS/WBS | CD |
| Suggested Mitigation | Early coordination with PKG-05; define foundation tolerances; hold point for acceptance |
| Contingency Handling | CD contingency (30%) covers interface issues |

---

### R-005: Geotechnical Conditions

| Field | Value |
|-------|-------|
| Risk Driver | Quantity uncertainty |
| Cause → Consequence | Unknown bearing capacity → Foundation changes, settlement concerns |
| Affected CBS/WBS | CD (interface with PKG-05) |
| Suggested Mitigation | Complete geotechnical investigation; coordinate with DEL-02.04 |
| Contingency Handling | Foundation costs in PKG-05; interface impacts in PKG-13 contingency |

---

### R-006: Internal Coating Quality

| Field | Value |
|-------|-------|
| Risk Driver | Quality uncertainty |
| Cause → Consequence | Food-grade coating defects → Rework, delays, product contamination risk |
| Affected CBS/WBS | MAT, CD, COM |
| Suggested Mitigation | Pre-qualify coating system; specify application QC requirements; witness coating |
| Contingency Handling | COM contingency covers additional inspection and cleaning |

---

### R-007: Agitator Selection

| Field | Value |
|-------|-------|
| Risk Driver | Scope uncertainty |
| Cause → Consequence | Agitator type/size TBD → Design changes, procurement delays |
| Affected CBS/WBS | MAT, E |
| Suggested Mitigation | Finalize agitator selection in DEL-13.02 early; engage OEM suppliers |
| Contingency Handling | E contingency covers additional design effort |

---

### R-008: Weather Impacts

| Field | Value |
|-------|-------|
| Risk Driver | Productivity uncertainty |
| Cause → Consequence | BC weather (rain, wind) → Erection delays, productivity loss |
| Affected CBS/WBS | CD, CI |
| Suggested Mitigation | Weather windows in schedule; protective measures for welding |
| Contingency Handling | CI contingency (30%) covers weather-related indirect costs |

---

### R-009: Heavy Lift Availability

| Field | Value |
|-------|-------|
| Risk Driver | Schedule uncertainty |
| Cause → Consequence | Large crane availability → Erection schedule delays, premium costs |
| Affected CBS/WBS | CD |
| Suggested Mitigation | Early crane booking; develop erection sequence to minimize crane time |
| Contingency Handling | Crane allowance ($420k) includes mobilization margin |

---

### R-010: NDE Findings

| Field | Value |
|-------|-------|
| Risk Driver | Quality uncertainty |
| Cause → Consequence | Weld defects found during NDE → Repair delays, additional testing |
| Affected CBS/WBS | CD |
| Suggested Mitigation | Qualified welders; pre-production weld tests; in-process inspection |
| Contingency Handling | CD contingency covers repair allowance |

---

### R-011: Hydrostatic Test Water

| Field | Value |
|-------|-------|
| Risk Driver | Logistics uncertainty |
| Cause → Consequence | Water supply/disposal challenges → Test delays, environmental constraints |
| Affected CBS/WBS | CD, COM |
| Suggested Mitigation | Confirm water source; plan disposal; consider sequential testing to reuse water |
| Contingency Handling | Test allowance includes water logistics |

---

### R-012: Phase 2 Interface Scope Creep

| Field | Value |
|-------|-------|
| Risk Driver | Scope uncertainty |
| Cause → Consequence | Phase 2 requirements undefined → Additional provisions, design changes |
| Affected CBS/WBS | MAT, E |
| Suggested Mitigation | Define Phase 2 requirements early; limit scope to stub connections |
| Contingency Handling | Phase 2 allowance ($45k) is minimal; scope creep could add cost |

---

## Risk Summary

| ID | Risk | Likelihood | Impact | CBS/WBS | Mitigation Priority |
|----|------|------------|--------|---------|---------------------|
| R-001 | Steel price volatility | HIGH | HIGH | MAT | HIGH |
| R-002 | Fabricator capacity | MEDIUM | HIGH | MAT, CD | HIGH |
| R-003 | Seismic complexity | MEDIUM | MEDIUM | E, MAT, CD | MEDIUM |
| R-004 | Foundation interface | MEDIUM | MEDIUM | CD | HIGH |
| R-005 | Geotechnical conditions | MEDIUM | MEDIUM | CD | MEDIUM |
| R-006 | Coating quality | LOW | MEDIUM | MAT, COM | MEDIUM |
| R-007 | Agitator selection | MEDIUM | LOW | MAT, E | MEDIUM |
| R-008 | Weather impacts | MEDIUM | MEDIUM | CD, CI | LOW |
| R-009 | Heavy lift availability | LOW | MEDIUM | CD | LOW |
| R-010 | NDE findings | LOW | MEDIUM | CD | MEDIUM |
| R-011 | Hydro test water | LOW | LOW | CD, COM | LOW |
| R-012 | Phase 2 scope creep | LOW | LOW | MAT, E | LOW |

---

## Contingency Summary

| CBS | Base Amount | Contingency % | Contingency Amount | Key Risk Drivers |
|-----|-------------|---------------|--------------------|--------------------|
| E | $580,000 | 20% | $116,000 | R-003, R-007, R-012 |
| MAT | $11,855,000 | 25% | $2,964,000 | R-001, R-002, R-006 |
| CD | $5,100,000 | 30% | $1,530,000 | R-004, R-005, R-008, R-010 |
| CI | $918,000 | 30% | $275,000 | R-008 |
| PM | $1,020,000 | 15% | $153,000 | General project risk |
| P | $237,000 | 15% | $36,000 | R-002 |
| COM | $535,000 | 30% | $161,000 | R-006, R-011 |
| **Total** | **$20,245,000** | **25.9%** | **$5,235,000** | |

---

## Contingency Adequacy Assessment

| Scenario | Impact | Coverage |
|----------|--------|----------|
| Steel +15% | +$1.44M | Covered by MAT contingency |
| Steel +25% | +$2.4M | Partially covered; MAT contingency is $2.96M |
| Tank erection +20% | +$510k | Covered by CD contingency |
| Seismic design adds 10% to MAT | +$960k | Covered by MAT contingency |
| Weather delays 10% to CD | +$510k | Covered by CD/CI contingency |
| Combined moderate impacts | +$2-3M | Within total contingency |
| Combined severe impacts | +$4-5M | Approaches contingency limit |

**Assessment:** Contingency is adequate for moderate risk scenario but would be stressed under severe combined impacts. Steel price volatility (R-001) is the dominant risk.
