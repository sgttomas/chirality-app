# Basis of Estimate — PKG-01 Demolition & Removals

**Snapshot ID:** EST_PKG01_DRAFT_2026-01-28_2330
**Package:** PKG-01 Demolition & Removals
**Discipline:** Civil
**Date:** 2026-01-28

---

## 1. Estimate Identification

| Field | Value |
|-------|-------|
| Snapshot ID | EST_PKG01_DRAFT_2026-01-28_2330 |
| Estimate Label | PKG01_DRAFT |
| Pricing Date | January 2026 |
| Currency | CAD (Canadian Dollars) |
| Estimate Class | Class 5 (Order of Magnitude) |
| Expected Accuracy | -30% to +50% |
| Base Estimate | $1,303,000 |
| Contingency | $326,000 (25%) |
| Total Estimate | $1,629,000 |

---

## 2. Scope Definition

### 2.1 Inclusions

This estimate covers PKG-01 Demolition & Removals as defined in the project decomposition:

**Deliverables (4):**
- DEL-01.01 Demolition Design Drawing Set (Drawing)
- DEL-01.02 Demolition Technical Specification (Specification)
- DEL-01.03 Demolition Procedures (Procedure)
- DEL-01.04 Demolition Installation & Test Records (Record)

**Physical Scope:**
- Track 6 rail infrastructure removal and disposal
- Dolphin 2 marine structure removal and disposal
- Perimeter fencing removal and disposal
- Salt tent building dismantling and disposal
- Associated decommissioning activities

**Cost Categories Included:**
- Engineering & Design (E) — drawing production, specification writing, QA/QC documentation
- Project Management (PM) — procedure development, EPCM allocation
- Procurement (P) — vendor coordination for materials
- Materials (MAT) — temporary works, protection measures, disposal containers
- Construction Directs (CD) — demolition labor, equipment, waste disposal
- Construction Indirects (CI) — field supervision, safety oversight, QA/QC

### 2.2 Exclusions

- Owner's costs and project oversight
- Land acquisition or lease costs
- Financing costs
- Permits obtained by Employer (per decomposition Section 1.2)
- Nitrogen skid supply (Employer-responsible per DEC-07)
- Hazardous materials abatement beyond placeholder allowance
- Escalation (pricing date = January 2026, escalation_mode = NONE)
- Taxes (excluded per project convention)

---

## 3. Pricing Basis

### 3.1 Currency and Pricing Date

| Parameter | Value | Basis |
|-----------|-------|-------|
| Currency | CAD | Project location: Surrey, BC, Canada (D-011) |
| Pricing Date | 2026-01 | Current date; no historical pricing sources (D-012) |
| Escalation | None | escalation_mode = NONE per config (D-009/D-012) |

### 3.2 Pricing Sources Hierarchy

Per D-013, no project-specific pricing sources were discovered:

| Priority | Source Type | Availability | Usage |
|----------|-------------|--------------|-------|
| 1 | Vendor Quotes | None found | Not used |
| 2 | Rate Tables | None found | Not used |
| 3 | Historical Data | None found | Not used |
| 4 | Fallback Model | Available | 100% of pricing |

**Pricing Basis:** 100% Allowance/Parametric (Fallback Typical Model)

### 3.3 Pricing Method Summary

| Method | Line Items | Amount | % of Base |
|--------|------------|--------|-----------|
| ALLOWANCE | 11 | $1,061,000 | 81.5% |
| PARAMETRIC | 3 | $241,460 | 18.5% |
| QUOTE | 0 | $0 | 0% |
| RATE_TABLE | 0 | $0 | 0% |
| **Total** | **14** | **$1,303,000** | **100%** |

---

## 4. Quantity Basis

### 4.1 Quantities Extracted from Deliverable Documents

No explicit quantities were extracted from deliverable documents. All deliverable documents indicate quantities as TBD pending site surveys and as-built drawings.

### 4.2 Assumed Quantities (for allowance sizing)

| Scope Item | Assumed Quantity | Basis | Confidence |
|------------|------------------|-------|------------|
| Track 6 | ~500 LF track | Typical terminal siding length | LOW |
| Dolphin 2 | ~6-10 piles + deck | Typical mooring dolphin | LOW |
| Fencing | ~2,000 LF | Typical perimeter length | LOW |
| Salt tent | ~5,000 SF footprint | Typical storage tent | LOW |

**Critical Note:** These quantities are assumptions for allowance sizing only. Actual quantities must be determined from as-built drawings and site surveys before budget commitment.

---

## 5. Contracting Assumptions

| Assumption | Value |
|------------|-------|
| Contract Type | Design & Build (D&B Contractor scope) |
| Demolition Contractor | Subcontracted to demolition specialist |
| Marine Contractor | Subcontracted to marine demolition specialist |
| Hazmat Contractor | Subcontracted to licensed abatement contractor if required |
| Labor Rates | Canadian union rates assumed for BC location |
| Equipment | Contractor-furnished; included in unit rates |

---

## 6. Location and Productivity

### 6.1 Site Location

| Parameter | Value |
|-----------|-------|
| Project Site | Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC |
| Region | Greater Vancouver, British Columbia, Canada |
| Climate Zone | Pacific Northwest (marine, temperate) |

### 6.2 Productivity Factors

| Factor | Assumption | Impact |
|--------|------------|--------|
| Active Terminal | Work within operating terminal | Reduced productivity assumed |
| Marine Work | Over-water operations (Dolphin 2) | Weather-dependent productivity |
| Weather | Pacific Northwest (wet winters) | Seasonal productivity impact |
| Access | Terminal access restrictions | Limited work windows |

**Productivity Adjustment:** Embedded in allowance sizing (no explicit factor applied).

---

## 7. Indirects Model

### 7.1 Method Selection

Per D-017, indirects are calculated using the factor-based model from the fallback typical model due to absence of schedule data.

### 7.2 Indirects Factors Applied

| CBS | Factor | Base | Calculated |
|-----|--------|------|------------|
| CI (Construction Indirects) | 18% of CD | $950,000 | $171,000 |
| PM (Project Management) | 6% of (CD+CI+MAT) | $1,161,000 | $69,660 |
| P (Procurement Services) | 2% of MAT | $40,000 | $800 |

### 7.3 Indirects Coverage

Construction Indirects (CI) include:
- Field supervision
- Safety officer allocation
- QA/QC coordination
- Site management overhead

---

## 8. Contingency

### 8.1 Contingency Method

Per D-018, contingency is calculated using PCT_BY_BUCKET method with allowance-heavy adjustment.

### 8.2 Contingency Rates

| CBS | Baseline Rate | Allowance Share | Adjustment | Final Rate |
|-----|---------------|-----------------|------------|------------|
| E | 10% | 100% | +10% | 20% |
| PM | 10% | 100% | +10% | 20% |
| P | 10% | 100% | +10% | 20% |
| MAT | 15% | 100% | +10% | 25% |
| CD | 20% | 100% | +10% | 30% |
| CI | 20% | N/A (factor) | N/A | 0%* |

*CI contingency embedded in CD calculation.

### 8.3 Contingency Summary

| Metric | Value |
|--------|-------|
| Base Estimate | $1,303,000 |
| Total Contingency | $326,000 |
| Contingency Rate | 25.0% |
| Total with Contingency | $1,629,000 |

### 8.4 Contingency Rationale

Elevated contingency rates (baseline + 10% allowance adjustment) are applied because:
1. 100% of estimate is allowance-based (no quotes or rate tables)
2. Hazardous materials status is unknown
3. Structure quantities are assumed (not surveyed)
4. Marine demolition highly variable

---

## 9. Rounding Policy

| Parameter | Value |
|-----------|-------|
| Rounding Unit | $1,000 CAD |
| Application | Summary totals only |
| Detail Precision | Full calculated values retained |

---

## 10. Completeness and Known Gaps

### 10.1 Completeness Metrics

| Metric | Value |
|--------|-------|
| Deliverable Coverage | 100% (4/4) |
| Scope Item Coverage | 100% (4/4 structures) |
| Quote-Based Lines | 0% |
| Quantity Extraction | 0% |
| Overall Completeness | 50% |

### 10.2 Known Gaps

| Gap | Impact | Resolution |
|-----|--------|------------|
| No vendor quotes | HIGH — accuracy unknown | Obtain demolition contractor quotes |
| No structure quantities | HIGH — sizing assumptions | Survey structures, obtain as-builts |
| Hazmat status unknown | HIGH — potential cost increase | Complete hazmat survey |
| No schedule data | MED — indirects factor-based | Develop demolition schedule |
| No disposal quotes | MED — disposal cost variable | Obtain disposal facility quotes |

---

## 11. References

### 11.1 Source Documents

| Document | Use |
|----------|-----|
| Decomposition (PKG-01) | Scope definition |
| DEL-01.01 through DEL-01.04 | Deliverable requirements and attributes |
| _CONFIG.md | Estimate configuration parameters |
| EST_PKG00_DRAFT estimate | Estimating conventions and format |

### 11.2 Related Estimate Documents

| Document | Content |
|----------|---------|
| Decision_Log.md | 9 decisions (D-010 through D-018) |
| Assumptions_Log.md | 11 assumptions (A-101 through A-111) |
| Source_Index.md | Source discovery results |
| Detail.csv | 14 line items with full traceability |
| Summary.md | Cost summary by CBS and deliverable |
| Risk_Register.md | 9 risks identified |
| QA_Report.md | QA checks and completeness scoring |
| WBS_CBS_Matrix.csv | WBS to CBS mapping |

---

## 12. Approval and Version Control

| Field | Value |
|-------|-------|
| Prepared By | ESTIMATING Agent |
| Preparation Date | 2026-01-28 |
| Estimate Status | DRAFT |
| Review Status | Pending human review |

**Version History:**
- v1.0 (2026-01-28): Initial draft estimate created

---

## 13. Recommendations for Next Estimate Cycle

1. **Obtain marine contractor quote** for Dolphin 2 removal (highest-value item at $450k)
2. **Complete hazardous materials survey** for all structures
3. **Obtain as-built drawings** for Track 6 and Dolphin 2 to determine actual quantities
4. **Obtain demolition contractor quotes** for Track 6 and salt tent
5. **Establish engineering rate table** for consistent deliverable cost estimation
6. **Obtain disposal facility quotes** with current tipping fees

**Target:** Achieve Class 3 estimate (±20% accuracy) with vendor quotes and quantities.

---

**End of Basis of Estimate**
