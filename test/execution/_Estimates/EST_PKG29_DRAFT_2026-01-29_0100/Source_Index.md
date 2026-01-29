# Source Index — PKG-29 Testing

**Snapshot ID:** EST_PKG29_DRAFT_2026-01-29_0100
**Package:** PKG-29 Testing
**Date:** 2026-01-29

---

## Summary

| Source Type | Count | Coverage |
|-------------|-------|----------|
| Vendor quotes | 0 | 0% |
| Budgetary quotes | 0 | 0% |
| Rate tables | 0 | 0% |
| Historical data | 0 | 0% |
| Deliverable documents | 8 | Scope only |
| Decomposition | 1 | Scope only |
| Fallback typical model | 1 | 100% pricing |

**Primary Pricing Basis:** Fallback typical model (no project-specific pricing sources found)

---

## Pricing Sources (Priority Order)

### 1. Vendor Quotes

**Status:** None found

**Searched locations:**
- `execution/_Estimates/_RateTables/` — no files
- Deliverable folders — no vendor documentation
- `_REFERENCES.md` files — no pricing references

**Impact:** Cannot validate material or equipment pricing

**Recommendation:** Obtain budgetary quotes for:
- Test equipment rental (hydrostatic pumps, gauges, recorders)
- Electrical test equipment rental (meggers, hi-pot, relay testers)
- I&C test equipment rental (calibrators, HART communicators)
- Hydrotest water treatment chemicals
- Hydrotest water haul-off disposal

---

### 2. Rate Tables / Cost Libraries

**Status:** None found

**Searched locations:**
- `execution/_Estimates/_RateTables/` — folder empty
- Project workspace — no rate files found

**Impact:** Cannot apply unit rates; using LS allowances

**Recommendation:** Develop rate tables for:
- Testing labor rates (hydrotest crew, electrical, I&C)
- Test equipment rental rates
- FAT travel and per diem rates
- Water disposal rates ($/m3)

---

### 3. Historical Data

**Status:** None found

**Impact:** No benchmarking data available

**Recommendation:** Collect historical testing costs from similar projects

---

## Quantity Sources

### Deliverable Documents (Scope Only)

| Source | Path | Information Extracted |
|--------|------|----------------------|
| Decomposition | `test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` | PKG-29 scope: hydrostatic, electrical, I&C, FAT, SAT; 8 deliverables |
| DEL-29.01 | `execution/PKG-29_Testing/1_Working/DEL-29.01_Test_Procedures/` | Scope: test procedure types |
| DEL-29.02 | `execution/PKG-29_Testing/1_Working/DEL-29.02_Inspection_and_Test_Plan/` | Scope: ITP with hold/witness points |
| DEL-29.03 | `execution/PKG-29_Testing/1_Working/DEL-29.03_Test_Installation_Test_Records/` | Scope: test record types |
| DEL-29.04 | `execution/PKG-29_Testing/1_Working/DEL-29.04_FAT_Installation_Test_Records/` | Scope: FAT records |
| DEL-29.05 | `execution/PKG-29_Testing/1_Working/DEL-29.05_SAT_Installation_Test_Records/` | Scope: SAT records |
| DEL-29.06 | `execution/PKG-29_Testing/1_Working/DEL-29.06_Tank_Hydrotest_Water_Management_Plan/` | Scope: hydrotest water management |
| DEL-29.07 | `execution/PKG-29_Testing/1_Working/DEL-29.07_Hydrotest_Water_Treatment_Discharge/` | Scope: treatment and discharge |
| DEL-29.08 | `execution/PKG-29_Testing/1_Working/DEL-29.08_Hydrotest_Water_Disposal_Records/` | Scope: disposal records |

**Quantities Extracted:** Deliverable counts only; physical quantities TBD

---

### Related Package Information

| Package | Information Needed | Status |
|---------|-------------------|--------|
| PKG-13 Storage Tanks | Tank dimensions, hydrotest parameters | TBD |
| PKG-14 Process Piping | Pipe lengths, test package counts | TBD |
| PKG-15 Pumps | Motor/pump list for SAT | TBD |
| PKG-17 Electrical | Switchgear, MCC, motor counts | TBD |
| PKG-19 Control Systems | DCS I/O counts, control valve counts | TBD |
| PKG-20 Field Instrumentation | Instrument loop counts | TBD |
| PKG-23 Fire Protection | Fire water loop testing scope | TBD |

**Impact:** Cannot extract physical quantities without discipline package completion

---

## Fallback Typical Model (Applied)

**Source:** AGENT_ESTIMATING fallback typical model (lines 623-691)

**Components Used:**

| Component | Factor/Value | Application |
|-----------|--------------|-------------|
| CI factor | 18% of CD | L-019 |
| P factor | 2% of MAT | L-020 |
| PM factor | 6% of (CD+CI+MAT) | L-021 |
| COM factor | 3% of (CD+CI+MAT) | L-022 |
| Contingency baseline | 20% E, 25% MAT, 30% CD/CI/COM, 15% P/PM | Per CBS bucket |
| Allowance adjustment | +5% if AllowanceShare >= 50% | Applied to all buckets |

**Transparency:** All fallback model uses labeled as PARAMETRIC or ALLOWANCE with LOW/MED confidence

---

## Documents Not Found / Not Available

| Document | Expected Location | Impact |
|----------|-------------------|--------|
| Employer's Requirements Vol 2 Part 1 | `test/Volume_2_Part_1_Employers_Requirements.pdf` | Testing/QA requirements TBD |
| Employer's Requirements Vol 2 Part 2 | `test/Volume_2_Part_2_Employers_Requirements.pdf` | Testing/QA requirements TBD |
| Employer's Requirements Vol 2 Part 3 | `test/Volume_2_Part_3_Employers_Requirements.pdf` | Testing/QA requirements TBD |
| Test equipment rental quotes | Not provided | Pricing TBD |
| Disposal contractor quotes | Not provided | Pricing TBD |
| Treatment chemical quotes | Not provided | Pricing TBD |

---

## Source Priority Applied

Per AGENT_ESTIMATING protocol:

1. **Vendor quotes:** Not available → Skip
2. **Rate tables:** Not available → Skip
3. **Historical data:** Not available → Skip
4. **Allowances:** Applied for all line items → Mark ALLOWANCE, Confidence=LOW
5. **Fallback factors:** Applied for indirects → Mark PARAMETRIC, Confidence=MEDIUM

**Decision:** D-008 (use fallback model due to no pricing sources)

---

**Source Index Prepared By:** Estimating Agent
**Date:** 2026-01-29
**Pricing Sources Found:** 0
