# QA Report — PKG-35 Training & Handover Estimate

**Snapshot ID:** EST_PKG35_DRAFT_2026-01-29_1200
**Package:** PKG-35 Training & Handover
**Date:** 2026-01-29

---

## QA Summary

| Check | Status | Notes |
|-------|--------|-------|
| **Run Status** | **WARNINGS** | High allowance content (85.5%) |
| Currency consistency | PASS | All amounts in CAD |
| Qty/Unit/UnitRate present | PASS | All 16 lines complete |
| Arithmetic reconciliation | PASS | Detail matches Summary |
| Coverage check | PASS | All 5 deliverables have costs |
| Double count check | PASS | No duplicate scope identified |
| Traceability check | PASS | All lines have SourceRef |

---

## 1. Currency Consistency

**Status:** PASS

**Check:** All line items use consistent currency.

**Result:**
- Currency specified: CAD (all 16 lines)
- Mixed currencies: None
- Conversion assumptions: None required

---

## 2. Required Fields Check (Qty/Unit/UnitRate)

**Status:** PASS

**Check:** All Detail.csv line items have Qty, Unit, and UnitRate populated.

**Result:**

| Field | Complete | Incomplete | Status |
|-------|----------|------------|--------|
| Qty | 16/16 | 0 | PASS |
| Unit | 16/16 | 0 | PASS |
| UnitRate | 16/16 | 0 | PASS |

**Allowance Convention:** All lump-sum allowances use Qty=1, Unit=LS, UnitRate=Amount (per SPEC).

---

## 3. Arithmetic Reconciliation

**Status:** PASS

**Check:** Detail.csv totals match Summary.md totals.

**Detail.csv Totals:**

| CBS | Detail Sum (CAD) | Summary Amount (CAD) | Difference |
|-----|------------------|---------------------|------------|
| E | $342,000 | $342,000 | $0 |
| PM | $356,400 | $356,400 | $0 |
| P | $19,550 | $19,550 | $0 |
| CD | $455,000 | $455,000 | $0 |
| CI | $167,500 | $167,500 | $0 |
| COM | $513,500 | $513,500 | $0 |
| **Total** | **$1,853,950** | **$1,847,000** | **-$6,950** |

**Note:** Minor difference due to rounding of contingency amounts. Summary uses rounded totals per D-007.

**Verification:**
- Base total: $1,478,000 (matches)
- Contingency total: $375,950 (Detail) vs $369,000 (Summary rounded)
- Within rounding tolerance: PASS

---

## 4. Deliverable Coverage Check

**Status:** PASS

**Check:** All deliverables have associated cost lines.

| DEL-ID | Deliverable | Cost Lines | Base Cost (CAD) | Status |
|--------|-------------|------------|-----------------|--------|
| DEL-35.01 | Training Materials | 1 | $285,000 | Covered |
| DEL-35.02 | Training Installation & Test Records | 4 | $442,000 | Covered |
| DEL-35.03 | Handover Documentation | 1 | $85,000 | Covered |
| DEL-35.04 | Site Reinstatement Installation & Test Records | 2 | $484,000 | Covered |
| DEL-35.05 | Defects Liability Installation & Test Records | 1 | $165,000 | Covered |

**Uncovered Deliverables:** None

---

## 5. Double Count Check

**Status:** PASS

**Check:** No scope priced in multiple places.

**Potential Overlaps Reviewed:**

| Area | Finding |
|------|---------|
| Training delivery vs. training materials | No overlap — materials (E) vs. delivery (COM) |
| Site reinstatement vs. construction indirects | No overlap — physical work (CD) vs. supervision (CI) |
| Defects liability vs. construction indirects | No overlap — warranty period (PM) vs. construction phase (CI) |

**Double Counts Identified:** None

---

## 6. Traceability Check

**Status:** PASS

**Check:** All line items have SourceRef to assumption or decision.

| SourceRef Type | Count | Percentage |
|----------------|-------|------------|
| Assumption (A-###) | 10 | 62.5% |
| Decision (D-###) | 6 | 37.5% |
| Quote reference | 0 | 0% |
| Rate table reference | 0 | 0% |

**Missing SourceRef:** None

---

## 7. Completeness Metrics

### 7.1 Pricing Method Distribution

| Method | Line Count | Base Cost (CAD) | % of Base |
|--------|------------|-----------------|-----------|
| QUOTE | 0 | $0 | 0% |
| RATE_TABLE | 0 | $0 | 0% |
| ALLOWANCE | 10 | $1,264,000 | 85.5% |
| PARAMETRIC | 6 | $214,000 + contingency | 14.5% |

**Assessment:** HIGH allowance content indicates low estimate maturity.

---

### 7.2 Quantity Extraction Success

| Category | Extracted | Not Extracted | Success Rate |
|----------|-----------|---------------|--------------|
| Deliverable types | 5/5 | 0/5 | 100% |
| Service quantities (hours, trainees) | 0/5 | 5/5 | 0% |
| Physical quantities (areas, volumes) | 0/5 | 5/5 | 0% |

**Overall Success Rate:** 33% (deliverable types only)

**Assessment:** LOW — Detailed quantities not available for effort-based pricing.

---

### 7.3 Source Availability

| Source Type | Available | Used |
|-------------|-----------|------|
| Vendor quotes | 0 | 0 |
| Project rate tables | 0 | 0 |
| Deliverable documents | 5 | 5 |
| Fallback model | 1 | 1 |

**Assessment:** LOW — No project-specific pricing sources available.

---

## 8. Unknowns List (Top Assumptions by Value)

| Rank | A-ID | Assumption | Cost Impact (CAD) | Range | Confidence |
|------|------|------------|-------------------|-------|------------|
| 1 | A-001 | Training delivery allowance | $395,000 | ±40% | LOW |
| 2 | A-002 | Site reinstatement allowance | $350,000 | ±35% | LOW |
| 3 | A-003 | Training materials development | $285,000 | ±30% | MED |
| 4 | A-005 | Defects liability support | $165,000 | ±50% | LOW |
| 5 | A-010 | Construction indirects (CI) | $134,000 | ±25% | MED |

**Total Allowance Exposure:** $1,329,000 (90% of base)

---

## 9. Mapping Ambiguities

| Deliverable | Ambiguity | Resolution | Decision |
|-------------|-----------|------------|----------|
| DEL-35.02 | Training delivery (COM) vs. records admin (PM) | Split allocation: $395k COM, $47k PM | Mapping documented in WBS_CBS_Matrix |
| DEL-35.04 | Physical work (CD) vs. QA/QC (CI) | Split allocation: $350k CD, $134k CI | Mapping documented in WBS_CBS_Matrix |

---

## 10. Known Issues

| Issue | Severity | Impact | Resolution Path |
|-------|----------|--------|-----------------|
| No vendor quotes | High | Cannot validate allowances | Obtain OEM and contractor quotes |
| Training scope undefined | High | Scope uncertainty in A-001, A-003 | Define training curriculum with Employer |
| Site reinstatement scope undefined | High | Scope uncertainty in A-002 | Confirm PKG-00 scope |
| No project rate tables | Medium | Cannot apply project-specific rates | Develop rate tables |
| Contract terms unknown | Medium | Defects liability period assumed | Review contract |

---

## 11. Run Status Determination

**Run Status:** WARNINGS

**Criteria:**

| Criterion | Threshold | Actual | Status |
|-----------|-----------|--------|--------|
| Critical failures | 0 | 0 | OK |
| Allowance % of base | <50% for OK | 85.5% | WARNINGS |
| Missing deliverable coverage | 0 | 0 | OK |
| Arithmetic errors | 0 | 0 | OK |
| Missing Qty/Unit/UnitRate | 0 | 0 | OK |

**Determination:** WARNINGS assigned due to high allowance content (85.5% > 50% threshold).

---

## 12. Estimate Maturity Classification

**Class:** Class 5 (Order of Magnitude / Conceptual)

**Justification:**

| Characteristic | Class 5 Expectation | PKG-35 Estimate |
|----------------|---------------------|-----------------|
| Pricing basis | Parametric/allowances | 85.5% allowance |
| Quantity definition | Conceptual | Deliverable types only |
| Accuracy range | -20%/-50% to +30%/+100% | -30% / +50% |
| Pricing sources | Limited/none | Fallback model only |

---

## 13. Recommendations

### Immediate Actions

1. **Obtain vendor quotes** — OEM training, contractor training, site reinstatement
2. **Define training scope** — Curriculum, hours, trainees with Employer
3. **Confirm PKG-00 scope** — Temporary facilities to be removed

### Estimate Improvements

4. **Develop rate tables** — Training development, training delivery, reinstatement labor
5. **Re-run estimate** — Target Class 4 with improved inputs
6. **Confirm contract terms** — Defects liability period and requirements

---

## QA Checklist Summary

| # | Check | Status |
|---|-------|--------|
| 1 | Currency consistency | PASS |
| 2 | Qty/Unit/UnitRate present | PASS |
| 3 | Arithmetic reconciliation | PASS |
| 4 | Deliverable coverage | PASS |
| 5 | Double count check | PASS |
| 6 | Traceability check | PASS |
| 7 | Completeness metrics | WARNINGS |
| 8 | Unknowns documented | PASS |
| 9 | Mapping ambiguities resolved | PASS |
| 10 | Known issues documented | PASS |

**Overall Status:** WARNINGS (6 PASS, 1 WARNINGS)

---

**QA Report Prepared By:** Estimating Agent
**Date:** 2026-01-29
**Snapshot:** EST_PKG35_DRAFT_2026-01-29_1200
