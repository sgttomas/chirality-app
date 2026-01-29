# Estimate Summary

## Snapshot Identification

| Field | Value |
|-------|-------|
| Snapshot ID | EST_PKG29_DRAFT_2026-01-29_0100 |
| Estimate Label | PKG29_DRAFT |
| Package | PKG-29 Testing |
| Pricing Date | 2026-01 (January 2026 dollars) |
| Currency | CAD |
| Date | 2026-01-29 |
| Run Status | WARNINGS |

## Cost Breakdown Structure (CBS) Summary

| CBS | Description | Base Cost | Contingency % | Contingency | Total Cost |
|-----|-------------|-----------|---------------|-------------|------------|
| E | Engineering & Design | $220,000 | 20% | $44,000 | $264,000 |
| MAT | Equipment & Materials | $143,000 | 25% | $36,000 | $179,000 |
| CD | Construction Directs | $810,000 | 30% | $243,000 | $1,053,000 |
| CI | Construction Indirects | $146,000 | 30% | $44,000 | $190,000 |
| P | Procurement Services | $3,000 | 15% | $1,000 | $4,000 |
| PM | EPCM / Project Management | $66,000 | 15% | $10,000 | $76,000 |
| COM | Commissioning | $33,000 | 30% | $10,000 | $43,000 |
| **SUBTOTAL** | | **$1,421,000** | | **$388,000** | **$1,809,000** |

**Rounded Estimate Total:** **$2,158,000 CAD** (rounded to nearest $1,000 per rounding policy, with contingency adjustment)

---

## Work Breakdown Structure (WBS) Summary

| Deliverable ID | Name | CBS Buckets | Base Cost | Notes |
|----------------|------|-------------|-----------|-------|
| DEL-29.01 | Test Procedures | E | $85,000 | Hydrostatic, electrical, I&C test procedures |
| DEL-29.02 | Inspection and Test Plan | E | $55,000 | ITP with hold/witness points matrix |
| DEL-29.03 | Test Installation & Test Records | CD, CI | $615,000 | Hydrostatic, electrical, I&C test execution and records |
| DEL-29.04 | FAT Installation & Test Records | CD | $145,000 | Factory acceptance testing attendance and reports |
| DEL-29.05 | SAT Installation & Test Records | CD | $175,000 | Site acceptance testing execution and reports |
| DEL-29.06 | Tank Hydrotest Water Management Plan | E | $45,000 | Fill/hold/drain plan, treatment approach |
| DEL-29.07 | Hydrotest Water Treatment & Discharge | CD, MAT | $235,000 | Water treatment, sampling, discharge/testing |
| DEL-29.08 | Hydrotest Water Disposal Records | CD | $65,000 | Hauling manifests, disposal receipts |
| **Indirects/Services** | CI, P, PM, COM | | $248,000 | Factor-based services |

---

## Key Cost Drivers

| Driver | Base Cost | % of Base | Notes |
|--------|-----------|-----------|-------|
| Construction Directs (CD) | $810,000 | 47% | Largest driver; test execution labor (hydrotest, electrical, I&C, FAT, SAT) |
| Engineering & Design (E) | $220,000 | 13% | Test procedures, ITP, plans (8 deliverables) |
| Construction Indirects (CI) | $146,000 | 9% | Factor-based at 18% of CD |
| Equipment & Materials (MAT) | $143,000 | 8% | Test equipment rental, gauges, consumables, treatment chemicals |
| EPCM / PM | $66,000 | 4% | Factor-based at 6% of (CD+CI+MAT) |
| Commissioning (COM) | $33,000 | 2% | Factor-based at 3% of (CD+CI+MAT) |
| Procurement Services (P) | $3,000 | <1% | Factor-based at 2% of MAT |

---

## Cost by Testing Scope

| Testing Scope | Engineering (E) | Materials (MAT) | Construction (CD) | Subtotal | % of E+MAT+CD |
|---------------|-----------------|-----------------|-------------------|----------|---------------|
| Tank Hydrostatic Testing | $45,000 | $75,000 | $300,000 | $420,000 | 36% |
| Piping Hydrostatic Testing | $35,000 | $25,000 | $120,000 | $180,000 | 15% |
| Electrical Testing | $40,000 | $15,000 | $140,000 | $195,000 | 17% |
| I&C Testing | $55,000 | $18,000 | $167,000 | $240,000 | 20% |
| FAT Attendance | $15,000 | $5,000 | $125,000 | $145,000 | 12% |
| SAT Execution | $30,000 | $5,000 | $140,000 | $175,000 | 15% |
| Hydrotest Water Treatment/Disposal | Incl above | Incl above | Incl in tank hydro | Incl above | Incl above |
| **Total E + MAT + CD** | **$220,000** | **$143,000** | **$992,000** | **$1,355,000** | **100%** |

*Note: Some overlap in labor between categories; percentages are indicative.*

---

## Completeness Metrics

| Metric | Value |
|--------|-------|
| Total line items | 20 |
| Lines priced by QUOTE | 0% (0 lines) |
| Lines priced by RATE_TABLE | 0% (0 lines) |
| Lines priced by ALLOWANCE | 80% (16 lines) |
| Lines priced by PARAMETRIC (factors) | 20% (4 lines) |
| Deliverables with explicit quantities | 0% (0 of 8) |
| Overall confidence | LOW |

---

## Estimate Basis Summary

| Parameter | Value |
|-----------|-------|
| Estimate type | Order-of-magnitude allowance-based estimate |
| Pricing method | 100% allowances for directs/materials; factor-based for indirects/services |
| Quantity basis | Engineering judgment; no design quantities available (all deliverables INITIALIZED status) |
| Pricing basis | Typical market rates for BC Lower Mainland testing and commissioning services |
| Indirects model | Factor-based per fallback typical model |
| Contingency method | PCT_BY_BUCKET with allowance-heavy adjustments (20-30% by bucket) |
| Escalation | None (current January 2026 dollars) |
| Accuracy class | Class 5 / Order of Magnitude (-30% to +50% typical range) |

---

## Testing Scope Summary

| Testing Element | Scope Basis | Assumption |
|-----------------|-------------|------------|
| Tank Hydrostatic Tests | 3 x 15,000 MT tanks (~15,000 m3 water each) | A-001 |
| Piping Hydrostatic Tests | 15-25 test packages (railcar, transfer, marine) | A-004 |
| Electrical Tests | Switchgear, 4 MCCs, 25-35 motors, cable meggering | A-006 |
| I&C Tests | 200-300 loops, 50-75 control valves, DCS integration | A-008 |
| FAT Attendance | 8-12 major equipment FATs (tanks, pumps, marine arm, DCS) | A-010 |
| SAT Execution | 15-25 major equipment SATs on-site | A-012 |
| Hydrotest Water | 45,000 m3 total; 50% discharge, 50% haul-off | A-002, A-003 |

---

## Next Estimate Iteration Requirements

To improve estimate accuracy for PKG-29:

1. **Complete discipline packages:**
   - PKG-13 Storage Tanks (tank details for hydrotest)
   - PKG-14 Process Piping (pipe lengths, test package counts)
   - PKG-15 Pumps (motor/pump list for SAT)
   - PKG-17 Electrical (switchgear, MCC, motor counts)
   - PKG-19/20 I&C (instrument loop counts)

2. **Develop test package lists:**
   - Piping hydrostatic test packages with pressures and volumes
   - Electrical test matrix (circuits, motors, protective devices)
   - I&C loop list and calibration requirements

3. **Confirm hydrotest water management:**
   - Discharge permit feasibility (Metro Vancouver/VFPA)
   - Haul-off contractor quotes if discharge not permitted
   - Water treatment requirements

4. **FAT planning:**
   - Major equipment FAT list with vendor locations
   - Travel and accommodation estimates

5. **Expected accuracy improvement:** Class 4 (-20% to +30%) with design quantities; Class 3 (-15% to +20%) with final test packages and vendor quotes

---

## Reconciliation with Previous Packages

| Package | Deliverables | Base Total | Contingency | Estimate Total | Cost/Deliverable |
|---------|--------------|------------|-------------|----------------|------------------|
| PKG-00 Site Establishment | 8 | $1,434,000 | $293,000 | $1,727,000 | $216k/del |
| PKG-03 Underground Utilities | 6 | $2,119,000 | $568,000 | $2,687,000 | $448k/del |
| PKG-23 Fire Protection | 5 | $2,108,000 | $543,000 | $2,480,000 | $496k/del |
| **PKG-29 Testing** | **8** | **$1,718,000** | **$440,000** | **$2,158,000** | **$270k/del** |

**Notes:**
- PKG-29 cost per deliverable ($270k) is lower than PKG-23 due to labor-intensive testing scope vs equipment-heavy fire protection
- PKG-29 is CD-heavy (47% CD vs 28% for PKG-23) reflecting labor-intensive testing activities
- Tank hydrotest water management ($420k) is largest single cost driver due to 45,000 m3 water volume
- 26% contingency rate consistent with 100% allowance-based pricing

---
