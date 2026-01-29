# QA Report — PKG-00 & PKG-01 Cumulative Aggregation

**Snapshot ID:** AGG_Estimate_Collation_2026-01-29_0120
**Date:** 2026-01-29
**Packages:** PKG-00 + PKG-01

---

## QA Status: PASSED

All quality checks completed successfully.

---

## Validation Summary

| Check Category | PKG-00 | PKG-01 | Status |
|----------------|--------|--------|--------|
| Schema Validation | 18/18 | 14/14 | ✓ PASSED |
| Artifact Completeness | 7/7 | 7/7 | ✓ PASSED |
| Provenance | 18/18 | 14/14 | ✓ PASSED |
| Namespacing | 39 UIDs | 34 UIDs | ✓ PASSED |
| Financial Rollup | Valid | Valid | ✓ PASSED |
| Conflicts | 0 | 0 | ✓ PASSED |
| Duplicates | 0 | 0 | ✓ PASSED |

---

## Cumulative Statistics

**Total Line Items:** 32 (all with Qty/Unit/UnitRate populated)
**Total Assumptions:** 24 (all documented with resolution paths)
**Total Risks:** 17 (all documented with mitigation strategies)
**Total Decisions:** 18

**Financial Validation:**
- PKG-00 base: $1,434,000 ✓
- PKG-01 base: $1,303,000 ✓
- Cumulative base: $2,737,000 ✓
- Cumulative total: $3,356,000 ✓

---

## Data Quality

**Confidence:** LOW (both packages 100% allowance-based)
**Maturity:** Class 5 (Order of Magnitude)
**Allowance Share:** 87.7% PKG-00, 100% PKG-01

**Warnings:**
- High reliance on allowances without vendor quotes
- Major cost drivers have wide uncertainty ranges

---

**QA Report Prepared By:** Aggregation Agent
**Date:** 2026-01-29 01:20
