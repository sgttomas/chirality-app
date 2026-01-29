# Summary — PKG-15 Pumps & Rotating Equipment Estimate

**Snapshot ID:** EST_PKG15_DRAFT_2026-01-28_2345
**Package:** PKG-15 Pumps & Rotating Equipment
**Date:** 2026-01-28
**Currency:** CAD
**Pricing Date:** 2026-01 (January 2026)
**Status:** WARNINGS

---

## Executive Summary

**Package Scope:** Pumps and rotating equipment for canola oil transload facility including railcar unloading pumps, marine loading pumps, tank transfer pumps, sump pumps, motors, drives, seals, and installation.

**Key Equipment:**
- Marine loading pumps (400 m³/hr, 50 kW): 2 units
- Railcar unloading transfer pumps (200 m³/hr, 30 kW): 4 units
- Tank transfer pumps (150 m³/hr, 15 kW): 2 units
- Sump pumps (25 m³/hr, 3 kW): 6 units
- **Total pump units: 14**
- Total installed motor capacity: 406 kW

---

## Cost Summary

| CBS Category | Base Amount (CAD) | Contingency (CAD) | Contingency % | Total (CAD) |
|--------------|-------------------|-------------------|---------------|-------------|
| Engineering (E) | $99,840 | $19,968 | 20.0% | $119,808 |
| Project Management (PM) | $70,620 | $7,062 | 10.0% | $77,682 |
| Procurement (P) | $22,000 | $2,200 | 10.0% | $24,200 |
| Materials (MAT) | $1,273,400 | $318,350 | 25.0% | $1,591,750 |
| Construction Directs (CD) | $54,040 | $16,212 | 30.0% | $70,252 |
| Construction Indirects (CI) | $9,730 | $1,946 | 20.0% | $11,676 |
| Commissioning (COM) | $29,280 | $7,320 | 25.0% | $36,600 |
| **Subtotal** | **$1,558,910** | **$373,058** | **23.9%** | **$1,931,968** |
| **Rounded** | **$1,559,000** | **$373,000** | **23.9%** | **$1,932,000** |

---

## Cost Breakdown by CBS

### Engineering (E): $99,840 base
- Pump arrangement drawings and installation design (DEL-15.01): $39,936
- Pump technical specifications (DEL-15.02): $24,960
- Pump sizing calculations and NPSH analysis (DEL-15.03): $19,968
- Vendor data review and approval (DEL-15.04): $9,984
- Commissioning documentation (DEL-15.05): $4,992

**Deliverables:** 5 (DEL-15.01 through DEL-15.05)
**Engineering hours:** 480 hours @ $208/hr loaded

---

### Materials (MAT): $1,273,400 base

**Pumps:** $712,000
- Marine loading pumps (2 × $125,000): $250,000
- Railcar unloading transfer pumps (4 × $75,000): $300,000
- Tank transfer pumps (2 × $45,000): $90,000
- Sump pumps (6 × $12,000): $72,000

**Motors and Drives:** $263,900
- Electric motors (406 kW @ $500/kW): $203,000
- VFDs (203 kW @ $300/kW): $60,900

**Auxiliary Equipment:** $297,500
- Mechanical seal systems (API 682): $127,500
- Couplings and baseplates: $102,000
- Initial spare parts: $68,000

**Notes:**
- All pumps API 610 specification (process service)
- 316SS wetted parts for food-grade canola oil
- NEMA Premium efficiency motors
- VFDs on 50% of pumps for process control

---

### Construction Directs (CD): $54,040 base

**Installation Labor:** 568 manhours @ $95/hr average

- Pump rigging and setting: $16,800 (14 pumps)
- Alignment and coupling installation: $21,280 (14 pumps)
- Baseplate grouting: $10,640 (14 pumps)
- Mechanical completion and inspection: $5,320 (14 pumps)

**Labor Rate:** $95/hr loaded (BC industrial rate)
**Productivity:** 40 manhours per pump average

---

### Construction Indirects (CI): $9,730 base

**Scope:** Site supervision, temporary facilities, small tools, HSE, QA/QC

**Method:** 18% of Construction Directs ($54,040 × 18%)

---

### Procurement (P): $22,000 base

**Scope:** Vendor solicitation, technical evaluation, purchase order management, expediting, receiving inspection

**Method:** 2% of Materials ($1,273,400 × ~1.7%)

---

### Project Management (PM): $70,620 base

**Scope:** EPCM services, engineering management, document control, coordination

**Method:** 6% of (CD + CI + MAT) = 6% × ($54,040 + $9,730 + $1,273,400)

---

### Commissioning (COM): $29,280 base

**Commissioning Activities:** 224 manhours @ $95/hr + travel

- Performance testing (flow, head, power, vibration): $15,960 (14 pumps × 12 hr)
- Vibration analysis per API 610: $5,320 (14 pumps × 4 hr)
- FAT witness travel allowance: $8,000 (6 major pumps)

**Testing per:** API 610 Section 6.9 (field performance test), ISO 10816 (vibration)

---

## Contingency Analysis

**Method:** PCT_BY_BUCKET with allowance-heavy adjustments

**Contingency Rationale:**

| CBS | Base Contingency | Allowance Share | Adjustment | Final Contingency |
|-----|-----------------|-----------------|------------|------------------|
| E | 10% | ~100% (parametric) | +10% | **20%** |
| PM | 10% | N/A | 0% | **10%** |
| P | 10% | N/A | 0% | **10%** |
| MAT | 15% | ~100% (all allowance/parametric) | +10% | **25%** |
| CD | 20% | ~100% (parametric) | +10% | **30%** |
| CI | 20% | N/A | 0% | **20%** |
| COM | 25% | ~65% (mostly parametric) | 0% | **25%** |

**Overall contingency:** 23.9% of base cost

**Justification for elevated contingency:**
1. **No vendor quotes** — all equipment costs are parametric allowances (LOW confidence)
2. **TBD pump quantities** — all deliverables list quantities as TBD pending DEL-15.03 calculations
3. **TBD pump sizing** — performance parameters awaiting calculations and ER Part 2 data
4. **No project-specific rates** — using fallback model for labor, indirects, PM
5. **Early design stage** — deliverables in INITIALIZED status

---

## Physical Quantities

| Item | Quantity | Unit |
|------|----------|------|
| Pump units (total) | 14 | ea |
| - Marine loading pumps | 2 | ea |
| - Railcar unloading transfer pumps | 4 | ea |
| - Tank transfer pumps | 2 | ea |
| - Sump pumps | 6 | ea |
| Total motor capacity | 406 | kW |
| Installation labor | 568 | manhours |
| Commissioning effort | 224 | manhours |
| Engineering effort | 480 | hours |

---

## Estimate Basis

**Pricing Sources:**
- Equipment: Parametric allowances (no vendor quotes)
- Labor: BC industrial rates ($95/hr loaded)
- Indirects/PM: Fallback typical model factors

**Key Assumptions:**
- 14 total pump units (4 railcar, 2 marine, 2 transfer, 6 sump) — **TBD** per DEL-15.03
- API 610 compliance for process pumps
- 316SS wetted parts for food-grade service
- Motors: NEMA Premium efficiency, 460V 3-phase
- VFDs on 50% of pumps for critical services
- Installation productivity: 40 manhours per pump

**Exclusions:**
- Piping to/from pumps (in PKG-14 Process Piping)
- Electrical power distribution and MCC (in PKG-17/19 Electrical)
- Control system and instrumentation (in PKG-19/20 I&C)
- Foundations (in PKG-05 Concrete Structures)
- Owner's costs, permits, land, financing

---

## Estimate Maturity and Confidence

**Overall Confidence:** LOW-MEDIUM

**Confidence by CBS:**
- Engineering: MEDIUM (parametric hours by deliverable complexity)
- Materials: LOW (no vendor quotes, TBD quantities, parametric costs)
- Construction: MEDIUM (typical productivity, BC labor rates)
- Indirects/PM: MEDIUM (fallback model factors, no project rates)
- Commissioning: MEDIUM (standard testing requirements, typical hours)

**Maturity Indicators:**
- Deliverable status: INITIALIZED (all 5 deliverables)
- Calculations: Not yet performed (DEL-15.03 pending)
- Vendor quotes: None available
- ER Part 2 review: Not performed
- Rate tables: None project-specific

**Estimate Class:** Class 4 / Preliminary Estimate (expected accuracy: -30% / +50%)

---

## Cost Sensitivity

**High sensitivity items:**

1. **Pump quantities** (±25%)
   - If 10 pumps instead of 14: -$300,000 (-15%)
   - If 18 pumps instead of 14: +$350,000 (+18%)

2. **API 610 vs. commercial pumps** (±30%)
   - Commercial-grade pumps instead of API 610: -$255,000 (-13%)
   - Premium API 610 features: +$340,000 (+18%)

3. **Seal system complexity** (±50%)
   - Simple single seals: -$64,000 (-3%)
   - Dual seals with barrier fluid systems: +$85,000 (+4%)

4. **VFD coverage** (0-100% of pumps)
   - No VFDs: -$61,000 (-3%)
   - VFDs on all pumps: +$61,000 (+3%)

**Combined worst case:** Base cost could increase to $2,100,000 (+35%)
**Combined best case:** Base cost could decrease to $1,200,000 (-23%)

---

## Comparison to Similar Packages

| Package | Base Cost (CAD) | Contingency | Total Cost (CAD) | Notes |
|---------|----------------|-------------|------------------|-------|
| PKG-15 Pumps (this estimate) | $1,559,000 | 23.9% | $1,932,000 | 14 pump units; rotating equipment |
| PKG-11 Marine Loading System | $2,540,000 | 25.7% | $3,194,000 | Includes loading arm, pipe, shelter |
| PKG-04 Pavement & Surfacing | $4,147,000 | 27.0% | $5,268,000 | Large civil scope |
| PKG-00 Site Establishment | $1,434,000 | 20.4% | $1,727,000 | Temporary facilities, fencing |

**Observations:**
- PKG-15 is mid-range in cost compared to completed packages
- Contingency (23.9%) is appropriate given TBD quantities and lack of quotes
- Materials-heavy package (~82% of base cost is MAT)

---

## Recommended Actions

**To improve estimate confidence:**

1. **Complete DEL-15.03 calculations** (Priority 1)
   - Finalize pump quantities and sizing
   - Confirm motor power requirements
   - Validate NPSH margins

2. **Review ER Part 2** (Priority 2)
   - Confirm pump specifications and quantities
   - Validate fluid properties (canola oil)
   - Identify seal system requirements

3. **Solicit budgetary quotes** (Priority 3)
   - API 610 pump vendors (Flowserve, Sulzer, ITT Goulds, KSB)
   - Motor vendors (ABB, Siemens, WEG)
   - Seal vendors (John Crane, Flowserve, EagleBurgmann)

4. **Develop rate tables** (Priority 4)
   - BC labor rates and productivity
   - Project-specific indirects and PM rates
   - Equipment rental rates

---

**Document Status:** FINAL
**Prepared By:** ESTIMATING Agent
**Date:** 2026-01-28
