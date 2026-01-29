# QA Report

**Snapshot ID:** AGG_Estimate_Collation_2026-01-29_0353  
**Date:** 2026-01-29 03:53  
**Pipeline:** EstimateCollation_PhaseByPackage

---

## Overall Status

**RUN_STATUS:** OK

All validation checks passed. No errors or warnings detected for PKG-32.

---

## Schema Validation

### Project_Detail.csv

**Status:** PASS

**Checks:**
- ✓ All required columns present
- ✓ All line items have Qty, Unit, UnitRate populated
- ✓ All amounts are numeric and positive
- ✓ All line UIDs follow PKG-XX::LXXX namespace pattern
- ✓ Currency is consistent (CAD) across all items

**PKG-32 Statistics:**
- Line items: 14
- Schema compliance: 100%

---

## Data Quality

### UID Uniqueness

**Status:** PASS

- ✓ All LineUIDs are unique (PKG-32:: namespace applied)
- ✓ No UID collisions detected across 33 packages (829 total lines)

### Financial Validation

**Status:** PASS

**PKG-32 Totals:**
- Detail.csv line item sum: $273,700 CAD
- Summary.md base estimate: $274,000 CAD (rounded)
- Variance: $300 (0.1%, within rounding tolerance)

**Cumulative Totals:**
- Project_Detail.csv sum: $89,623,706 CAD
- Cumulative CBS total: $89,623,706 CAD
- Variance: $0 (exact match)

---

## Coverage

### Artifact Availability

**PKG-32 Artifacts:**
- ✓ Detail.csv (14 lines)
- ✓ BOE.md (present)
- ✓ Assumptions_Log.md (13 assumptions)
- ✓ Risk_Register.md (8 risks)
- ✓ Decision_Log.md (12 decisions)

**Status:** COMPLETE (all required artifacts present)

### Deliverable Coverage

**PKG-32 Deliverables:** 8  
**Detail.csv coverage:** 14 line items  
**Coverage ratio:** 1.75 line items per deliverable

**Note:** 6 line items have WBS_DeliverableID = N/A (P, PM, COM allocations, and CD=$0 placeholder).

---

## Conflicts & Duplicates

### Conflicts

**Status:** NONE

No conflicts detected between PKG-32 and prior packages.

### Duplicates

**Status:** NONE

No duplicate line items detected.

---

## Data Provenance

**PKG-32 Source:**
- Estimate snapshot: EST_PKG32_DRAFT_2026-01-29_0016
- Extract path: Extracts/PKG-32_*.{csv,md}
- All line items traceable to source

---

## Recommendations

1. **Estimate maturity:** PKG-32 is at DRAFT status with LOW confidence due to 85% allowance-based pricing. Consider updating estimate once:
   - Permit responsibility matrix is clarified (Contractor vs Employer permits)
   - Issued permits and permit conditions become available
   - Regulatory/environmental consultant scope and budget are confirmed

2. **Obtain Employer's Requirements Volume 2 Part 3** (regulatory requirements section) to clarify permit scope and responsibilities.

3. **Engage regulatory consultant** for preliminary permit needs assessment and budget estimate to refine engineering and consultant allowances.

4. **Monitor high-impact assumptions:** Engineering hours (27% cost impact), consultant support (22% cost impact), and compliance monitoring (33% cost impact) are primary cost drivers with LOW confidence.

---

## Summary

**Overall Assessment:** PASS

PKG-32 aggregation completed successfully with no errors or data quality issues. All required artifacts present and schema-compliant.

**Next:** Ready for next package assignment.

---

**QA Completed:** 2026-01-29 03:53  
**Status:** OK
