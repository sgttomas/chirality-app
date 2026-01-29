# QA Report

## Snapshot Identification

| Field | Value |
|-------|-------|
| Snapshot ID | EST_PKG06_DRAFT_2026-01-28_2333 |
| Estimate Label | PKG06_DRAFT |
| Package Scope | PKG-06 Structural Steelwork |
| QA Status | PASS (with warnings) |
| Run Status | WARNINGS |

---

## QA Checks Performed

### 1. Currency Consistency

**Check:** All line items use the same currency (CAD).

**Result:** PASS

**Details:** All 21 line items in Detail.csv have Currency = CAD. No currency conversion required.

---

### 2. Qty/Unit/UnitRate Completeness (Hard Requirement)

**Check:** Every line item has non-empty Qty, Unit, and UnitRate fields.

**Result:** PASS

**Details:** All 21 line items have populated Qty, Unit, UnitRate, and Amount fields. Allowance/parametric lines use Qty=1, Unit=LS convention per SPEC requirements.

---

### 3. Arithmetic Reconciliation (Detail → Summary)

**Check:** Sum of Detail.csv line items matches Summary.md CBS totals.

**Result:** PASS

**Reconciliation:**

| CBS | Detail.csv Sum (CAD) | Summary.md Total (CAD) | Variance |
|-----|---------------------:|-----------------------:|----------|
| E | $89,000 | $89,000 | $0 |
| PM | $120,000 | $120,000 | $0 |
| P | $27,000 | $27,000 | $0 |
| MAT | $1,301,000 | $1,301,000 | $0 |
| CD | $611,000 | $611,000 | $0 |
| CI | $115,000 | $115,000 | $0 |
| COM | $60,000 | $60,000 | $0 |
| **Base Total** | **$2,323,000** | **$2,323,000** | **$0** |

**Contingency Reconciliation:**

| CBS | Contingency (Detail calc) | Contingency (Summary) | Variance |
|-----|-------------------------:|----------------------:|----------|
| E | $17,800 (20% × $89k) | $17,800 | $0 |
| PM | $18,000 (15% × $120k) | $18,000 | $0 |
| P | $4,050 (15% × $27k) | $4,100 | $50 (rounding) |
| MAT | $325,250 (25% × $1,301k) | $325,300 | $50 (rounding) |
| CD | $183,300 (30% × $611k) | $183,300 | $0 |
| CI | $34,500 (30% × $115k) | $34,500 | $0 |
| COM | $18,000 (30% × $60k) | $18,000 | $0 |
| **Contingency Total** | **$600,900** | **$601,000** | **$100 (rounding)** |

**Total Estimate:** $2,323,000 + $601,000 = $2,924,000 (within rounding tolerance of $1,000)

---

### 4. Coverage Check (Deliverables → Cost Lines)

**Check:** All deliverables have associated cost line items.

**Result:** PASS

**Deliverable Coverage:**

| Deliverable ID | Deliverable Name | Line Items | Base Cost (CAD) |
|----------------|------------------|------------|----------------:|
| DEL-06.01 | Structural Steel Design Drawing Set | L001 | $45,000 |
| DEL-06.02 | Structural Steel Technical Specification | L002 | $12,000 |
| DEL-06.03 | Structural Steel Design Calculations | L003 | $18,000 |
| DEL-06.04 | Structural Steel Data Sheet Package | L004 | $6,000 |
| DEL-06.05 | Structural Steel Installation & Test Records | L005 | $8,000 |

All 5 deliverables have explicit engineering cost line items. Construction/materials scope (L006-L021) is package-level (not tied to individual deliverables) per standard practice.

---

### 5. Double-Count Heuristics

**Check:** No scope appears to be priced in multiple line items.

**Result:** PASS (no double-counts detected)

**Review:**
- Engineering deliverables (L001-L005) are distinct document production efforts
- Materials (L006, L009, L011, L013, L014) are distinct item categories (structural steel, handrail, grating, stairs/gangways, pipe supports)
- Construction directs (L007, L008, L010, L012, L015, L016, L017) are distinct installation activities
- Indirects/services (L018-L021) are factor-based and do not overlap with directs

---

### 6. Traceability Check

**Check:** All line items have SourceRef populated (file path, assumption ID, or decision ID).

**Result:** PASS

**Details:**
- 17 line items (L001-L017) have SourceRef = A-### (Assumptions_Log.md)
- 4 line items (L018-L021) have SourceRef = D-009 (Decision_Log.md, factor-based indirects)
- All SourceRef values map to valid entries in Decision_Log.md or Assumptions_Log.md

---

### 7. Completeness Scoring

**Metric:** Percentage of estimate priced by method.

**Result:**

| Method | Line Count | Base $ (CAD) | % of Base |
|--------|------------|-------------:|----------:|
| QUOTE | 0 | $0 | 0% |
| RATE_TABLE | 0 | $0 | 0% |
| ALLOWANCE | 17 | $1,880,000 | 81% |
| PARAMETRIC | 4 | $443,000 | 19% |
| **Total** | **21** | **$2,323,000** | **100%** |

**Deliverables with Explicit Quantities:** 0 of 5 (0%)

**Overall Confidence:** LOW (100% allowance/parametric-based; no vendor quotes or detailed design)

---

### 8. Known Issues and Warnings

#### WARNING 1: No Vendor Quotes

**Severity:** HIGH

**Description:** No vendor budgetary quotes available for structural steel fabrication, galvanizing, handrails, grating, or stairs/gangways.

**Impact:** All material costs (MAT = $1,301,000, 56% of base) are allowances with ±25-50% uncertainty.

**Mitigation:** Contingency increased to 25% on MAT bucket (vs 15% baseline).

**Resolution:** Obtain vendor budgetary quotes for structural steel supply/fabrication.

---

#### WARNING 2: No Design Drawings or Tonnage Estimate

**Severity:** HIGH

**Description:** Structural steel tonnage is an allowance (150 tonnes, Decision D-012) without design basis.

**Impact:** Tonnage may vary ±50% when design is complete, affecting MAT ($900k line item) and CD ($356k erection labor).

**Mitigation:** Contingency increased to 25% on MAT and 30% on CD.

**Resolution:** Provide structural steel design drawings (DEL-06.01) with member sizes/lengths or tonnage estimate from design calculations (DEL-06.03).

---

#### WARNING 3: No Project Rate Tables

**Severity:** MEDIUM

**Description:** Labor rates ($95/hr composite, $110/hr inspector, $140/hr documentation, $150/hr spec writing, $175/hr structural engineering) are assumed typical BC lower mainland rates without project-specific validation.

**Impact:** Labor cost lines (E, CD totaling ~$700k) have ±15-20% uncertainty.

**Mitigation:** Contingency applied (20-30% by CBS bucket).

**Resolution:** Provide project labor rates and equipment rental rates in config or rate table.

---

#### WARNING 4: No Productivity or Schedule Data

**Severity:** MEDIUM

**Description:** Steel erection productivity (25 hrs/tonne) is a typical range assumption without project-specific validation (site access, crane availability, schedule compression, etc.).

**Impact:** Construction directs (CD = $611k) may vary ±20-30% based on actual site conditions.

**Mitigation:** Contingency increased to 30% on CD.

**Resolution:** Provide erection productivity assumptions from project execution plan or historical data.

---

#### WARNING 5: Handrail, Grating, Stairs/Gangway Quantities are Rough Allowances

**Severity:** MEDIUM

**Description:** Handrail (400 m), grating (800 m²), and stairs/gangways (12 items) are allowances (Decisions D-013, Assumptions A-009, A-010, A-011) without layout drawings.

**Impact:** Combined allowance ~$368k may vary ±30-50% when layout is defined.

**Mitigation:** Contingency increased to 25-30% on MAT/CD.

**Resolution:** Provide platform/gangway layout drawings (DEL-06.01) and gangway data sheets (DEL-06.04).

---

## Unknowns List (Top Allowances by Value)

| Rank | Description | Allowance ID | Amount (CAD) | % of Base |
|------|-------------|--------------|-------------:|----------:|
| 1 | Structural steel material supply (150 tonnes) | A-006 | $900,000 | 39% |
| 2 | Structural steel erection labor (3,750 hrs) | A-007 | $356,000 | 15% |
| 3 | Stairs and gangways (12 items) | A-011 | $180,000 | 8% |
| 4 | Crane & equipment for steel erection | A-008 | $120,000 | 5% |
| 5 | Grating supply (800 m²) | A-010 | $96,000 | 4% |
| 6 | Pipe supports and racks | A-012 | $65,000 | 3% |
| 7 | Handrail supply (400 m) | A-009 | $60,000 | 3% |
| 8 | Grating installation (800 m²) | A-010 | $48,000 | 2% |
| 9 | Structural Steel Design Drawing Set | A-001 | $45,000 | 2% |
| 10 | Handrail installation (400 m) | A-009 | $28,000 | 1% |

**Top 10 allowances total:** $1,898,000 (82% of base estimate)

---

## Mapping Ambiguities

**None identified.** WBS → CBS mapping is straightforward for PKG-06 (engineering deliverables → E; construction/materials → MAT/CD/CI/PM/P/COM per standard CBS).

---

## QA Conclusion

**Overall QA Status:** PASS (with warnings)

**Run Status:** WARNINGS

**Confidence Level:** LOW

**Summary:**
- All hard requirements met (currency consistency, Qty/Unit/UnitRate populated, arithmetic reconciliation, traceability)
- No critical failures that prevent estimate use for budgeting/planning
- Multiple warnings related to estimate maturity (no vendor quotes, no design drawings, no project rates)
- Contingency percentages elevated (20-30%) to account for allowance-heavy estimate
- Estimate is suitable for preliminary budgeting but NOT suitable for procurement or commitment without further refinement

**Recommended Actions:**
1. Obtain structural steel design drawings (tonnage, member sizes, counts)
2. Obtain vendor budgetary quotes for fabrication, galvanizing, handrails, grating
3. Provide project labor rates and productivity assumptions
4. Provide platform/gangway layout drawings for quantity takeoff

---

**QA Report compiled:** 2026-01-28 23:33
**Reviewed by:** Estimating Agent (automated QA checks per AGENT_ESTIMATING.md PROTOCOL Function 4.1)
