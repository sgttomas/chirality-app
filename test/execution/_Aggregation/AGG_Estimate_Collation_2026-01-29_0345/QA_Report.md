# QA Report

**Snapshot ID:** AGG_Estimate_Collation_2026-01-29_0345  
**Date:** 2026-01-29 03:45  
**Pipeline:** EstimateCollation_PhaseByPackage

---

## Overall Status

**RUN_STATUS:** OK

All validation checks passed. No errors or warnings detected for PKG-31.

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

**PKG-31 Statistics:**
- Line items: 18
- Schema compliance: 100%

---

## Data Quality

### UID Uniqueness

**Status:** PASS

- ✓ All LineUIDs are unique (PKG-31:: namespace applied)
- ✓ No UID collisions detected across 32 packages (815 total lines)

### Financial Validation

**Status:** PASS

**PKG-31 Totals:**
- Detail.csv line item sum: $754,150 CAD
- Summary.md base estimate: $755,000 CAD (rounded)
- Variance: $850 (0.1%, within rounding tolerance)

**Cumulative Totals:**
- Project_Detail.csv sum: $89,350,006 CAD
- Cumulative CBS total: $89,350,006 CAD
- Variance: $0 (exact match)

---

## Coverage

### Artifact Availability

**PKG-31 Artifacts:**
- ✓ Detail.csv (18 lines)
- ✓ BOE.md (present)
- ✓ Assumptions_Log.md (6 assumptions)
- ✓ Risk_Register.md (8 risks)
- ✓ Decision_Log.md (9 decisions)

**Status:** COMPLETE (all required artifacts present)

### Deliverable Coverage

**PKG-31 Deliverables:** 11  
**Detail.csv coverage:** 18 line items  
**Coverage ratio:** 1.6 line items per deliverable

**Note:** 7 line items have WBS_DeliverableID = N/A (document control, printing, and other package-level activities).

---

## Conflicts & Duplicates

### Conflicts

**Status:** NONE

No conflicts detected between PKG-31 and prior packages.

### Duplicates

**Status:** NONE

No duplicate line items detected.

---

## Data Provenance

**PKG-31 Source:**
- Estimate snapshot: EST_PKG31_DRAFT_2026-01-29_1030
- Extract path: Extracts/PKG-31_*.{csv,md}
- All line items traceable to source

---

## Recommendations

1. **Estimate maturity:** PKG-31 is at DRAFT status with MEDIUM-LOW confidence due to 100% parametric/allowance pricing. Consider updating estimate once:
   - Drawing count is confirmed (currently estimated at 275 sheets)
   - Equipment list is finalized (currently estimated at 90 items)
   - System breakdown is confirmed (currently estimated at 12 systems)

2. **Obtain vendor quotes** for printing/binding services to replace allowance-based pricing.

3. **Monitor quantity assumptions:** Equipment count (48% cost impact) and systems count (22% cost impact) are primary cost drivers with MEDIUM-LOW confidence.

---

## Summary

**Overall Assessment:** PASS

PKG-31 aggregation completed successfully with no errors or data quality issues. All required artifacts present and schema-compliant.

**Next:** Ready for next package assignment.

---

**QA Completed:** 2026-01-29 03:45  
**Status:** OK
