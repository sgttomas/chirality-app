# Aggregation Plan — PKG-32 Regulatory & Permits

**Snapshot ID:** AGG_Estimate_Collation_2026-01-29_0353
**Date:** 2026-01-29 03:53
**Pipeline:** EstimateCollation_PhaseByPackage (Incremental)

---

## What Was Done

This aggregation run collated estimate artifacts for **PKG-32 Regulatory & Permits** and incorporated them into the cumulative project-level estimate package.

### Artifacts Processed

**Source estimate snapshot:** `EST_PKG32_DRAFT_2026-01-29_0016`

**Files read and extracted:**
- `Detail.csv` (14 line items)
- `BOE.md` (Basis of Estimate)
- `Assumptions_Log.md` (13 assumptions)
- `Risk_Register.md` (8 risks)
- `Decision_Log.md` (12 decisions)

**Prior packages incorporated:** PKG-00 through PKG-31 (32 packages)

---

## Cumulative Statistics

### Package Progress

| Metric | Count |
|--------|-------|
| **Packages completed** | **33 of ~36** |
| **Progress** | **91.7%** |

**Completed packages:** PKG-00 through PKG-32 (33 packages)

### Line Item Statistics

| Metric | Prior (32 pkgs) | PKG-32 | Cumulative (33 pkgs) |
|--------|-----------------|--------|----------------------|
| **Line items** | 815 | 14 | **829** |
| **Deliverables** | 176 | 8 | **184** |

### Financial Summary (Base Estimate)

| CBS Category | Prior Amount (CAD) | PKG-32 Amount (CAD) | Cumulative Amount (CAD) | % of Total |
|--------------|-------------------|---------------------|-------------------------|------------|
| CD (Construction Directs) | $26,583,520 | $0 | $26,583,520 | 29.7% |
| CI (Construction Indirects) | $5,250,193 | $90,000 | $5,340,193 | 6.0% |
| COM (Commissioning) | $2,534,949 | $7,000 | $2,541,949 | 2.8% |
| E (Engineering) | $7,726,165 | $135,000 | $7,861,165 | 8.8% |
| FRT (Freight) | $233,000 | $0 | $233,000 | 0.3% |
| MAT (Materials) | $41,020,185 | $25,000 | $41,045,185 | 45.8% |
| P (Procurement) | $886,346 | $1,700 | $888,046 | 1.0% |
| PM (Project Management) | $5,115,648 | $15,000 | $5,130,648 | 5.7% |
| **TOTAL** | **$89,350,006** | **$273,700** | **$89,623,706** | **100%** |

**Note:** Base estimate shown (excludes contingency). With contingency, PKG-32 total is $338,000 CAD.

### Estimate Totals with Contingency

| Metric | PKG-32 |
|--------|--------|
| Base estimate | $273,700 |
| Contingency (23%) | $64,300 |
| **Total estimate** | **$338,000** |

**Cumulative total with contingency (estimated):** $113.7M CAD

---

## PKG-32 Summary

### Package Details

**Package ID:** PKG-32  
**Package Name:** Regulatory & Permits  
**Estimate Snapshot:** EST_PKG32_DRAFT_2026-01-29_0016

### Scope

PKG-32 covers all regulatory permits, authority approvals, code compliance, and inspections including:
- Permit applications (VFPA PER, DFO, Transport Canada, building, fire, environmental)
- Permit receipt, tracking, and compliance management
- Regulatory/environmental consultant support
- Compliance monitoring and documentation (VFPA, DFO, TC, code)
- Correspondence register and filing
- Certificate of occupancy and regulatory closeout

### Cost Breakdown

| CBS | Base (CAD) | % |
|-----|------------|---|
| Engineering (E) | $135,000 | 49.3% |
| Construction Indirects (CI) | $90,000 | 32.9% |
| Materials (MAT) | $25,000 | 9.1% |
| Project Management (PM) | $15,000 | 5.5% |
| Commissioning (COM) | $7,000 | 2.6% |
| Procurement (P) | $1,700 | 0.6% |
| **Total** | **$273,700** | **100%** |

### Key Drivers

1. **Permit application engineering** ($75,000) - Preparation and submission for 5-8 major permits
2. **Regulatory/environmental consultants** ($60,000) - Specialist support for complex regulatory environment
3. **Compliance monitoring** ($90,000) - QA/QC for VFPA, DFO, TC, and code compliance
4. **Permit fees** ($25,000) - Contractor-responsible permit application fees

### Confidence & Maturity

**Confidence:** LOW (85% allowance-based, no vendor quotes)

**Primary Risks:**
- Permit count and scope uncertainty (permit list TBD)
- Permit condition complexity (permits not yet issued)
- Authority approval timeline variability
- Regulatory consultant scope creep

**Status:** DRAFT (WARNINGS - 85% allowance-based pricing)

---

## Quality Metrics

| Metric | Status |
|--------|--------|
| Schema validation | PASS (all line items have Qty, Unit, UnitRate) |
| UID uniqueness | PASS (PKG-32:: namespace applied) |
| Required artifacts | PASS (Detail, BOE, Assumptions, Risks, Decisions present) |
| Conflicts detected | NONE |
| Duplicates detected | NONE |
| Missing artifacts | NONE |

---

## Next Steps

**Remaining packages:** PKG-34, PKG-36 (~3 packages estimated)

**Next package:** To be assigned by user

**Pipeline completion:** 91.7% (33 of ~36 packages)

---

**Aggregation completed:** 2026-01-29 03:53  
**RUN_STATUS:** OK
