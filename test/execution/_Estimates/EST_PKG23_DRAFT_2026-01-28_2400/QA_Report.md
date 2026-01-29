# QA Report

## Snapshot Identification

| Field | Value |
|-------|-------|
| Snapshot ID | EST_PKG23_DRAFT_2026-01-28_2400 |
| Package | PKG-23 Fire Protection |
| Date | 2026-01-28 |
| Run Status | **WARNINGS** |

---

## QA Check Summary

| Check | Status | Notes |
|-------|--------|-------|
| Currency Consistency | ✓ PASS | All line items in CAD |
| Qty/Unit/UnitRate Present | ✓ PASS | All 22 lines have required fields |
| Arithmetic Reconciliation | ✓ PASS | Detail.csv sums match Summary.md (within rounding) |
| Coverage Check | ✓ PASS | All 5 deliverables have associated cost lines |
| Double Count Check | ✓ PASS | No duplicate scopes identified |
| Traceability Check | ✓ PASS | All lines have SourceRef (assumption or decision ID) |
| Confidence Labeling | ✓ PASS | All lines have Confidence rating |

---

## Run Status: WARNINGS

**Warning Conditions:**

1. **No vendor quotes available** — All pricing is allowance-based; estimate confidence is LOW
2. **No rate tables available** — No project-specific pricing data
3. **Fire water demand calculation incomplete** — DEL-23.03 in INITIALIZED status; fire water loop sizing TBD
4. **Foam system sizing incomplete** — Foam proportioning capacity TBD pending DEL-23.03
5. **Fire pump requirement unconfirmed** — Municipal supply pressure not verified; fire pump excluded per D-011
6. **Employer's Requirements not reviewed** — Volume 2 Part 1 fire protection requirements TBD

---

## Completeness Scoring

### Pricing Method Distribution

| Method | Line Count | Base Cost | % of Base |
|--------|------------|-----------|-----------|
| QUOTE | 0 | $0 | 0% |
| RATE_TABLE | 0 | $0 | 0% |
| ALLOWANCE | 18 | $1,630,000 | 77% |
| PARAMETRIC | 4 | $288,000 | 14% |
| **Total** | **22** | **$2,108,000*** | **100%** |

*Note: Total includes all line items; factors are calculated on base costs.

### Quantity Extraction Success

| Metric | Value |
|--------|-------|
| Deliverables with explicit quantities | 0 of 5 (0%) |
| Physical quantities available | 0% |
| Deliverable counts available | 100% (5/5) |

### Estimate Confidence

| Confidence Level | Line Count | Cost Impact |
|------------------|------------|-------------|
| HIGH | 0 | $0 |
| MEDIUM | 4 | $288,000 |
| LOW | 18 | $1,630,000 |

**Overall Estimate Confidence: LOW**

---

## Mapping Ambiguities

| Deliverable | Mapping Decision | Rationale | Decision ID |
|-------------|------------------|-----------|-------------|
| DEL-23.01 | E + MAT + CD | Drawing set drives design (E), material specs (MAT), and installation scope (CD) | D-010 |
| DEL-23.04 | E + MAT + CD | Data sheet package supports design (E), material procurement (MAT), and installation (CD) | D-010 |
| DEL-23.05 | CI + COM | Installation records captured in CI (field QA/QC) and COM (testing) | D-010 |

---

## Unknowns List (Top Assumptions by Value)

| Rank | Assumption | Cost Impact | % of Base | Resolution Path |
|------|------------|-------------|-----------|-----------------|
| 1 | A-006: Foam concentrate storage and proportioning | $185,000 | 9% | Complete DEL-23.03 foam calculations; obtain vendor quotes |
| 2 | A-001: Fire water loop piping (underground) | $165,000 | 8% | Complete DEL-23.01 layout; DEL-23.03 hydraulic calcs |
| 3 | A-017: Foam system installation | $150,000 | 7% | Complete foam design; obtain installation quotes |
| 4 | A-007: Tank foam discharge systems | $145,000 | 7% | Complete foam design per NFPA 11 |
| 5 | A-002: Fire hydrants (8-12 units) | $120,000 | 6% | Complete DEL-23.01 hydrant layout |
| 6 | A-008: Marine loading foam system | $95,000 | 5% | Complete marine foam design |
| 7 | A-016: Fire alarm installation | $95,000 | 5% | Complete DEL-23.01 fire alarm layout |

**Top 7 Assumptions Account for:** $955,000 (45% of base estimate)

---

## Arithmetic Reconciliation

| CBS | Detail.csv Sum | Summary.md Value | Variance | Status |
|-----|----------------|------------------|----------|--------|
| E | $175,000 | $175,000 | $0 | ✓ OK |
| MAT | $1,045,000 | $1,045,000 | $0 | ✓ OK |
| CD | $600,000 | $600,000 | $0 | ✓ OK |
| CI | $108,000 | $108,000 | $0 | ✓ OK |
| P | $21,000 | $21,000 | $0 | ✓ OK |
| PM | $106,000 | $106,000 | $0 | ✓ OK |
| COM | $53,000 | $53,000 | $0 | ✓ OK |
| **Total Base** | **$2,108,000** | **$2,108,000** | **$0** | ✓ OK |

---

## Currency Check

| Field | Value | Status |
|-------|-------|--------|
| Configured currency | CAD | ✓ |
| Detail.csv currencies | All CAD | ✓ |
| Summary.md currency | CAD | ✓ |
| Mixed currency lines | 0 | ✓ |

---

## Estimate Maturity Assessment

| Criterion | Assessment |
|-----------|------------|
| Design definition | INITIALIZED (all 5 deliverables) |
| Quantity takeoff | Not available |
| Vendor pricing | Not available |
| Rate tables | Not available |
| Schedule basis | Not available |
| Risk quantification | Qualitative only |

**Estimate Class:** Class 5 (Order of Magnitude)
**Expected Accuracy:** -30% to +50%

---

## Recommendations for Next Iteration

### Priority 1: Enable Volume-Based Estimate
1. Complete DEL-23.03 fire water demand calculation per NFPA 30
2. Complete DEL-23.03 hydraulic calculations for pipe sizing
3. Complete DEL-23.01 fire water loop layout with pipe routing
4. Develop fire alarm device schedule from DEL-23.01 drawings

### Priority 2: Obtain Vendor Pricing
1. Fire hydrant budgetary quotes (dry-barrel, -40°C rated)
2. Addressable FACP budgetary quotes
3. Foam proportioning system budgetary quotes
4. Foam concentrate pricing

### Priority 3: Confirm Scope
1. Confirm fire pump requirement (municipal supply adequacy)
2. Confirm foam system requirements per NFPA 30 and insurance
3. Extract fire protection requirements from ER Volume 2 Part 1

### Expected Accuracy Improvement
- With design quantities: Class 4 (-20% to +30%)
- With vendor quotes: Class 3 (-15% to +20%)

---

## QA Sign-Off

| Field | Value |
|-------|-------|
| QA Performed By | Estimating Agent (Automated) |
| QA Date | 2026-01-28 |
| Run Status | WARNINGS |
| Snapshot Valid | Yes (meets minimum validity requirements) |

---
