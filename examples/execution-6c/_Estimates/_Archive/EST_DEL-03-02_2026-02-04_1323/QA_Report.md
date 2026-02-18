# QA Report
## DEL-03-02: DetailedDesignAndConstructionDocsPlan
## Snapshot: EST_DEL-03-02_2026-02-04_1323

---

## QA Status Summary

| Metric | Status |
|--------|--------|
| **RUN_STATUS** | WARNINGS |
| **Critical Failures** | 0 |
| **Warnings** | 4 |
| **Currency Consistency** | PASS |
| **Schema Compliance** | PASS |
| **Arithmetic Reconciliation** | PASS (within rounding) |

---

## Check 1: Currency Consistency

| Check | Result |
|-------|--------|
| **Status** | PASS |
| **Currency Used** | CAD |
| **Mixed Currencies** | None |
| **Conversion Required** | No |

All line items are denominated in CAD per operator directive.

---

## Check 2: Qty/Unit/UnitRate Schema Compliance

| Check | Result |
|-------|--------|
| **Status** | PASS |
| **Total Line Items** | 15 |
| **Lines with Qty** | 15 (100%) |
| **Lines with Unit** | 15 (100%) |
| **Lines with UnitRate** | 15 (100%) |

All line items comply with required Qty/Unit/UnitRate schema.

---

## Check 3: Arithmetic Reconciliation

| Check | Result |
|-------|--------|
| **Status** | PASS (within rounding) |

### Detail.csv Sum Verification

| CBS | Line Items | Sum from Detail.csv |
|-----|------------|---------------------|
| E | L001-L011, L014 | $6,250 |
| PM | L012-L013 | $1,000 |
| CONT | L015 | $1,100 |
| **TOTAL** | | **$8,350** |

### Summary.md Comparison

| Item | Summary Amount | Detail Sum | Variance |
|------|----------------|------------|----------|
| E | $6,250 | $6,250 | $0 |
| PM | $1,000 | $1,000 | $0 |
| CONT | $1,100 | $1,100 | $0 |
| **TOTAL** | **$8,400** | **$8,350** | **$50** |

**Variance Explanation:** $50 variance is within rounding policy (nearest $100). Summary total rounded to $8,400.

---

## Check 4: Coverage Check

| Check | Result |
|-------|--------|
| **Status** | PASS |
| **Deliverables in Scope** | 1 (DEL-03-02) |
| **Deliverables with Cost Lines** | 1 (100%) |

All in-scope deliverables have associated cost lines.

---

## Check 5: Double Count Heuristics

| Check | Result |
|-------|--------|
| **Status** | PASS |
| **Potential Overlaps Identified** | 0 |

No scope priced in multiple places. Work elements are discrete and non-overlapping.

---

## Check 6: Mapping Ambiguities

| Issue | Description | Resolution |
|-------|-------------|------------|
| Landscape scope | Discipline count assumes 6 (including landscape) but landscape flagged as TBD | Included per D-004; will adjust if resolved out of scope |
| Third-party code review | Strategy documented but not mandated | Included per D-006; plan describes approach only |

---

## Unknowns List (Top Assumptions/Allowances by Value)

| Rank | Assumption ID | Description | Cost Impact | Confidence |
|------|---------------|-------------|-------------|------------|
| 1 | A-001 | Design Manager rate $175/hr | $5,250 | MED |
| 2 | A-003 | Technical Staff rate $100/hr | $1,700 | MED |
| 3 | A-005 | Discipline Scope Matrix effort (8 hrs) | $1,400 | MED |
| 4 | A-006 | QA/QC Checkpoint Table effort (6 hrs) | $1,050 | MED |
| 5 | A-016 | Design Manager Review effort (4 hrs) | $700 | MED |

---

## Completeness Metrics

| Metric | Value |
|--------|-------|
| **% Lines priced by QUOTE** | 0% |
| **% Lines priced by RATE_TABLE** | 0% |
| **% Lines priced by ALLOWANCE** | 100% |
| **% Deliverables with explicit quantities** | 100% |
| **Overall Confidence** | LOW-MEDIUM |

---

## Warnings

### Warning 1: All Pricing by Allowance

| Severity | WARNING |
|----------|---------|
| **Description** | No vendor quotes or rate tables available; all pricing based on allowance assumptions |
| **Impact** | Estimate accuracy dependent on assumed rates |
| **Recommended Action** | Provide rate tables in _RateTables/ folder for future runs |

### Warning 2: TBD Items Unresolved

| Severity | WARNING |
|----------|---------|
| **Description** | Multiple TBD items in source documents (landscape scope, third-party code review, RFP Section 7.1.8) |
| **Impact** | Scope may change when items resolved |
| **Recommended Action** | Resolve TBD items through human ruling; re-run estimate when resolved |

### Warning 3: RFP Requirements Not Directly Verified

| Severity | WARNING |
|----------|---------|
| **Description** | RFP Section 7.1.8 specific text not accessible; requirements inferred from decomposition |
| **Impact** | Plan may not fully address all RFP requirements |
| **Recommended Action** | Review actual RFP Section 7.1.8 text; validate plan against requirements |

### Warning 4: Post-Award Costs Excluded

| Severity | WARNING |
|----------|---------|
| **Description** | Estimate covers proposal phase plan production only; excludes post-award design execution |
| **Impact** | Total project design cost significantly higher |
| **Recommended Action** | Create separate estimate for post-award execution if required |

---

## Document Control

| Property | Value |
|----------|-------|
| **Created** | 2026-02-04 |
| **Agent** | ESTIMATING (Type 2) |
| **Snapshot** | EST_DEL-03-02_2026-02-04_1323 |
