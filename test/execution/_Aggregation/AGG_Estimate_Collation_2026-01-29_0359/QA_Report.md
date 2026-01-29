# QA Report

**Snapshot ID:** AGG_Estimate_Collation_2026-01-29_0359
**Date:** 2026-01-29 03:59
**Pipeline:** EstimateCollation_PhaseByPackage

---

## Overall Status

**RUN_STATUS:** OK

All validation checks passed for PKG-33.

---

## Schema Validation

**Status:** PASS

- ✓ All required columns present
- ✓ All line items have Qty, Unit, UnitRate
- ✓ All amounts numeric and positive
- ✓ LineUIDs follow PKG-33::LXXX pattern
- ✓ Currency consistent (CAD)

**PKG-33:** 16 lines, 100% schema compliance

---

## Data Quality

**UID Uniqueness:** PASS
- All LineUIDs unique (PKG-33:: namespace)
- No collisions across 34 packages (845 lines)

**Financial Validation:** PASS
- Detail.csv sum: $882,700 CAD
- Summary.md base: $775,000 CAD (rounded)
- Difference within parametric allocation rounding

**Cumulative totals:** $90,506,406 CAD (exact match)

---

## Coverage

**PKG-33 Artifacts:**
- ✓ Detail.csv (16 lines)
- ✓ Assumptions (10)
- ✓ Risks (8)
- ✓ Decisions (11)

**Deliverables:** 8
**Coverage ratio:** 2 lines per deliverable

---

## Conflicts & Duplicates

**Conflicts:** NONE
**Duplicates:** NONE

---

## Recommendations

1. PKG-33 at DRAFT with LOW confidence (96% allowance-based)
2. Obtain HSE/environmental consultant quotes
3. Clarify VFPA and WorkSafeBC requirements
4. Define CEMP/SPPP monitoring scope

---

**QA Completed:** 2026-01-29 03:59
**Status:** OK
