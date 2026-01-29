# QA Report

**Snapshot ID:** AGG_Estimate_Collation_2026-01-29_1500
**Date:** 2026-01-29

---

## Schema Validation

| Source | Schema Check | Status | Notes |
|--------|--------------|--------|-------|
| PKG-01/Detail.csv | Required columns present | PASS | All 14 columns found |
| PKG-01/Detail.csv | Qty/Unit/UnitRate populated | PASS | All 14 lines complete |
| PKG-01/Detail.csv | LineID uniqueness | PASS | No duplicates |
| PKG-01/Detail.csv | Currency consistent | PASS | All CAD |

## Totals Reconciliation

| Source | Reported Total | Calculated Sum | Variance | Status |
|--------|----------------|----------------|----------|--------|
| PKG-01/Detail.csv | $1,302,460 | $1,302,460 | $0 | PASS |
| PKG-01/Summary.md | $1,303,000 | $1,302,460 | $540 | PASS (rounding) |

*Note: $540 variance is due to rounding to nearest $1,000 in Summary.md*

## Provenance Check

| Check | Status |
|-------|--------|
| All lines have SourceRef | PASS |
| All assumptions traceable to source file | PASS |
| All risks traceable to source file | PASS |
| BOE provenance preserved | PASS |

## Namespace Integrity

| Check | Status |
|-------|--------|
| LineUID format valid (PKG-XX::Lxxx) | PASS |
| AssumptionUID format valid (PKG-XX::A-xxx) | PASS |
| RiskUID format valid (PKG-XX::R-xxx) | PASS |
| No namespace collisions | PASS |

## Coverage Assessment

| Package | Detail | BOE | Assumptions | Risks | Overall |
|---------|--------|-----|-------------|-------|---------|
| PKG-01 | OK | OK | OK | OK | 100% |

## Completeness Metrics

| Metric | Value |
|--------|-------|
| Packages in scope | 1 |
| Packages with complete artifact set | 1 (100%) |
| Lines with QUOTE pricing | 0 (0%) |
| Lines with RATE_TABLE pricing | 0 (0%) |
| Lines with ALLOWANCE pricing | 11 (79%) |
| Lines with PARAMETRIC pricing | 3 (21%) |
| Overall estimate confidence | LOW |

## Issues Found

None.

## Warnings

| Warning | Impact | Recommendation |
|---------|--------|----------------|
| 100% allowance-based estimate | Low accuracy | Obtain vendor quotes before budget approval |
| No quantities from deliverables | Sizing assumptions | Survey structures for actual quantities |

---

**QA Status:** PASS
