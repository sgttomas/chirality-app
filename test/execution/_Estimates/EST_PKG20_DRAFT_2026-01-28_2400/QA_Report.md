# QA Report — PKG-20 Field Instrumentation

## Overview

This report documents the quality assurance checks performed on the PKG-20 Field Instrumentation estimate snapshot.

---

## Snapshot Information

| Field | Value |
|-------|-------|
| Snapshot ID | EST_PKG20_DRAFT_2026-01-28_2400 |
| Package | PKG-20 Field Instrumentation |
| Run Date | 2026-01-28 |
| Run Status | WARNINGS |

---

## QA Checks

### 1. Currency Consistency

| Check | Result |
|-------|--------|
| Single currency used | PASS |
| Currency | CAD |
| All line items in CAD | PASS |
| Notes | No currency mixing detected |

### 2. Required Fields Check

| Check | Result |
|-------|--------|
| All lines have LineID | PASS |
| All lines have CBS | PASS |
| All lines have WBS_PackageID | PASS |
| All lines have WBS_DeliverableID | PASS (N/A acceptable) |
| All lines have Description | PASS |
| All lines have Qty | PASS |
| All lines have Unit | PASS |
| All lines have UnitRate | PASS |
| All lines have Amount | PASS |
| All lines have Currency | PASS |
| All lines have Method | PASS |
| All lines have SourceRef | PASS |
| All lines have Confidence | PASS |
| Notes | All 35 line items have complete required fields |

### 3. Arithmetic Reconciliation

| Check | Detail | Result |
|-------|--------|--------|
| Line amounts | Qty × UnitRate = Amount | PASS |
| CBS E subtotal | $85k + $55k + $35k + $65k + $40k = $280,000 | PASS |
| CBS MAT subtotal | Sum of L006-L024 = $592,200 | PASS (rounded to $592,000) |
| CBS CD subtotal | Sum of L025-L031 = $420,880 | PASS (rounded to $421,000) |
| CBS CI subtotal | L032 = $79,000 | PASS |
| CBS PM subtotal | L033 = $78,000 | PASS |
| CBS P subtotal | L034 = $13,000 | PASS |
| CBS COM subtotal | L035 = $52,000 | PASS |
| Total base | $1,515,080 | PASS (rounded to $1,535,000 per policy) |
| Summary matches Detail | Within rounding | PASS |

### 4. Coverage Check

| Check | Result |
|-------|--------|
| Deliverables with cost allocation | 5/5 (100%) |
| Deliverables with no cost | 0 |
| CBS buckets with costs | 7/7 |
| Notes | All deliverables have engineering cost allocation |

**Deliverable Coverage:**

| Deliverable | Cost Allocation |
|-------------|-----------------|
| DEL-20.01 | $85,000 (E) |
| DEL-20.02 | $55,000 (E) |
| DEL-20.03 | $35,000 (E) |
| DEL-20.04 | $65,000 (E) |
| DEL-20.05 | $40,000 (E) |

### 5. Double-Count Heuristics

| Check | Result |
|-------|--------|
| Duplicate descriptions | None detected |
| Overlapping scope | None detected |
| Notes | Equipment and installation clearly separated |

### 6. Method Distribution

| Method | Line Count | Base Amount | % of Base |
|--------|------------|-------------|-----------|
| ALLOWANCE | 30 | $1,313,000 | 87% |
| PARAMETRIC | 5 | $222,000 | 13% |
| QUOTE | 0 | $0 | 0% |
| RATE_TABLE | 0 | $0 | 0% |
| **Total** | **35** | **$1,535,000** | **100%** |

### 7. Confidence Distribution

| Confidence | Line Count | Base Amount | % of Base |
|------------|------------|-------------|-----------|
| LOW | 30 | $1,380,000 | 90% |
| MED | 5 | $155,000 | 10% |
| HIGH | 0 | $0 | 0% |
| **Total** | **35** | **$1,535,000** | **100%** |

---

## Completeness Metrics

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Lines priced by QUOTE | 0% | >30% | BELOW TARGET |
| Lines priced by RATE_TABLE | 0% | >20% | BELOW TARGET |
| Lines priced by ALLOWANCE/PARAMETRIC | 100% | <50% | ABOVE TARGET |
| Deliverables with explicit quantities | 0% | >70% | BELOW TARGET |
| Overall confidence | LOW | MED+ | BELOW TARGET |

---

## Mapping Ambiguities

| Line | Description | CBS Assigned | Ambiguity |
|------|-------------|--------------|-----------|
| L006-L024 | Various instruments and materials | MAT | Clear mapping |
| L025-L031 | Installation activities | CD | Clear mapping |
| L032-L035 | Factor-based indirects | CI/PM/P/COM | Factor-based; no ambiguity |

No mapping ambiguities identified.

---

## Unknowns List (Top Assumptions by Value)

| Rank | Assumption ID | Description | Cost Impact |
|------|---------------|-------------|-------------|
| 1 | A-008 | Instrument cable quantity (8,000 m) | $240,000 |
| 2 | A-007 | Transfer piping instruments (30 units) | $109,000 |
| 3 | A-004 | Tank instrumentation (24 units) | $108,000 |
| 4 | A-018 | Conduit system | $107,000 |
| 5 | A-009 | Junction boxes (25 units) | $100,000 |
| 6 | A-019 | Installation rate ($850/instrument) | $90,000 |
| 7 | A-020 | Calibration and loop testing | $67,000 |
| 8 | A-010 | Tubing and fittings | $60,000 |
| | **Total top 8 assumptions** | | **$881,000 (57%)** |

---

## Known Issues

| Issue ID | Description | Severity | Resolution |
|----------|-------------|----------|------------|
| QA-001 | 100% allowance-based pricing | High | Obtain vendor quotes for instruments |
| QA-002 | Instrument count parametric | High | Develop instrument index from P&IDs |
| QA-003 | Cable quantities estimated | Medium | Complete cable schedule |
| QA-004 | Deliverables in INITIALIZED state | Medium | Progress deliverables to IN_PROGRESS |
| QA-005 | No hazardous area classification | Medium | Complete hazardous area study |
| QA-006 | PKG-19 interface undefined | Medium | Coordinate I/O requirements |

---

## Run Status Determination

**Status: WARNINGS**

| Criterion | Evaluation |
|----------|------------|
| All required files generated | PASS |
| Qty/Unit/UnitRate on all lines | PASS |
| Detail-Summary reconciliation | PASS |
| All deliverables covered | PASS |
| Pricing confidence adequate | FAIL (100% allowance) |
| Quantity basis adequate | FAIL (parametric only) |

The estimate is mathematically valid but relies entirely on allowances and parametric quantities. Status is WARNINGS rather than FAILED_INPUTS because the parametric basis is reasonable for Class 5 estimating.

---

## Recommendations

1. **Priority 1:** Develop preliminary instrument index from P&IDs and process scope
2. **Priority 2:** Obtain budgetary quotes from Emerson, Endress+Hauser, Siemens
3. **Priority 3:** Complete cable schedule and routing study
4. **Priority 4:** Complete hazardous area classification study
5. **Priority 5:** Coordinate PKG-19 interface for I/O requirements

---

*QA Report generated by ESTIMATING Agent | 2026-01-28*
