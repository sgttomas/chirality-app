# QA Report

## PKG-21: Building Structures & Envelope

**Snapshot ID:** EST_PKG21_DRAFT_2026-01-28_0030

---

## Run Status

| Field | Value |
|-------|-------|
| RUN_STATUS | **WARNINGS** |
| Reason | 100% allowance/parametric pricing; no vendor quotes or rate tables |

---

## QA Checks

### Currency Consistency

| Check | Status | Notes |
|-------|--------|-------|
| Single currency used | PASS | All line items in CAD |
| Currency matches config | PASS | _CONFIG.md specifies CAD |
| No mixed currencies | PASS | N/A |

---

### Line Item Completeness

| Check | Status | Notes |
|-------|--------|-------|
| All lines have Qty | PASS | 26/26 lines have Qty populated |
| All lines have Unit | PASS | 26/26 lines have Unit populated |
| All lines have UnitRate | PASS | 26/26 lines have UnitRate populated |
| All lines have Amount | PASS | 26/26 lines have Amount populated |
| All lines have SourceRef | PASS | 26/26 lines reference A-### or D-### |

---

### Arithmetic Reconciliation

| Check | Status | Notes |
|-------|--------|-------|
| Line amounts = Qty × UnitRate | PASS | All calculations verified |
| CBS subtotals match Detail sum | PASS | See breakdown below |
| Summary totals match Detail | PASS | Base $1,591,000 verified |

**CBS Verification:**

| CBS | Detail.csv Sum | Summary Amount | Match |
|-----|----------------|----------------|-------|
| E | $178,000 | $178,000 | PASS |
| PM | $67,000 | $67,000 | PASS |
| P | $14,000 | $14,000 | PASS |
| MAT | $892,000 | $892,000 | PASS |
| CD | $345,000 | $345,000 | PASS |
| CI | $62,000 | $62,000 | PASS |
| COM | $33,000 | $33,000 | PASS |
| **Total** | **$1,591,000** | **$1,591,000** | **PASS** |

---

### Coverage Check

| Check | Status | Notes |
|-------|--------|-------|
| All deliverables have cost lines | PASS | 6/6 deliverables covered |
| All CBS buckets populated | PASS | E, PM, P, MAT, CD, CI, COM all have lines |
| No $0 line items | PASS | All amounts > $0 |

**Deliverable Coverage:**

| Deliverable | Line Items | Status |
|-------------|------------|--------|
| DEL-21.01 | L-001 | COVERED |
| DEL-21.02 | L-002 | COVERED |
| DEL-21.03 | L-003 | COVERED |
| DEL-21.04 | L-004 | COVERED |
| DEL-21.05 | L-025 | COVERED |
| DEL-21.06 | L-005 | COVERED |

---

### Double Count Check

| Check | Status | Notes |
|-------|--------|-------|
| No duplicate line items | PASS | Each scope element priced once |
| Building excluded from PKG-22 | PASS | MEP systems not in PKG-21 scope |
| Foundations not in PKG-05 | VERIFY | Building foundations in PKG-21; check interface with PKG-05 |

**Potential Interface Note:** PKG-05 (Concrete Structures) includes foundations and equipment pads. Building foundations are included in PKG-21 per building scope. Verify no overlap.

---

### Traceability Check

| Check | Status | Notes |
|-------|--------|-------|
| All line items have SourceRef | PASS | All reference A-### or D-### |
| All assumptions logged | PASS | A-001 through A-023 in Assumptions_Log.md |
| All decisions logged | PASS | D-001 through D-012 in Decision_Log.md |
| BOE complete | PASS | All required sections present |

---

## Completeness Metrics

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| % Priced by QUOTE | 0% | >50% | FAIL |
| % Priced by RATE_TABLE | 0% | >25% | FAIL |
| % Priced by ALLOWANCE/PARAMETRIC | 100% | <50% | FAIL |
| Deliverables with explicit quantities | 0% | >50% | FAIL |
| Line items with LOW confidence | 92% | <30% | FAIL |
| Line items with MEDIUM confidence | 8% | >40% | FAIL |
| Line items with HIGH confidence | 0% | >30% | FAIL |

**Assessment:** Estimate maturity is LOW. All pricing is based on parametric/allowance methods with no project-specific data.

---

## Unknowns List (Top Assumptions by Value)

| Rank | ID | Description | Amount | % of Base |
|------|-----|-------------|--------|-----------|
| 1 | A-001 | MCC building PEMB supply | $390,000 | 24.5% |
| 2 | A-002 | Operator shelters (4 units) | $180,000 | 11.3% |
| 3 | A-016 | PEMB erection labor | $108,000 | 6.8% |
| 4 | A-003 | Engineering design drawings | $85,000 | 5.3% |
| 5 | A-012 | Foundation materials | $85,000 | 5.3% |
| 6 | A-008 | Insulated metal panels | $72,000 | 4.5% |
| 7 | PM factor | Project management | $67,000 | 4.2% |
| 8 | A-015 | Foundation installation | $65,000 | 4.1% |
| 9 | CI factor | Construction indirects | $62,000 | 3.9% |
| 10 | A-017 | Envelope installation | $57,000 | 3.6% |

**Top 10 unknowns represent 74% of base estimate.**

---

## Mapping Ambiguities

| Item | Issue | Resolution |
|------|-------|------------|
| Building foundations | Could be PKG-05 or PKG-21 scope | Included in PKG-21 per building package convention; verify no overlap |
| Operator shelter HVAC | Building or MEP scope? | Basic heating included in shelter supply; full MEP in PKG-22 |
| Protective coatings | Could be PKG-26 scope | Building-specific coatings in PKG-21; general coatings in PKG-26 |

---

## Issues and Warnings

### Critical Issues

None.

### Warnings

| ID | Warning | Impact | Mitigation |
|----|---------|--------|------------|
| W-001 | 100% allowance/parametric pricing | HIGH — Estimate accuracy is Class 5 | Obtain vendor quotes |
| W-002 | MCC building size assumed | HIGH — Primary cost driver | Confirm size per electrical layout |
| W-003 | No geotechnical data | MEDIUM — Foundation type uncertain | Obtain geotech recommendations |
| W-004 | Operator shelter quantity assumed | MEDIUM — May need more shelters | Confirm per PKG-10 layout |

### Informational

| ID | Note |
|----|------|
| I-001 | Estimate suitable for order-of-magnitude budgeting only |
| I-002 | Re-run estimate after obtaining building size and vendor quotes |
| I-003 | Consider design-assist with PEMB supplier for better pricing |

---

## Recommendations for Next Run

1. **Obtain MCC building size** from PKG-17 electrical equipment layout
2. **Request budget quotes** from PEMB suppliers (Butler, Nucor, VP Buildings, etc.)
3. **Obtain geotechnical recommendations** for foundation type
4. **Confirm operator shelter count** per PKG-10 railcar unloading design
5. **Add project-specific rate tables** to `_RateTables/` folder

---

**QA Performed by:** ESTIMATING Agent
**Date:** 2026-01-28
**Snapshot:** EST_PKG21_DRAFT_2026-01-28_0030
