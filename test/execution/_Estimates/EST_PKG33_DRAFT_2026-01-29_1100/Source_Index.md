# Source Index — PKG-33 HSE Management

**Snapshot ID:** EST_PKG33_DRAFT_2026-01-29_1100
**Date:** 2026-01-29
**Package:** PKG-33 HSE Management

---

## Source Discovery Summary

This document catalogs the pricing and quantity sources discovered during the source indexing phase (Phase 2.2 of AGENT_ESTIMATING protocol).

---

## 1. Explicit Pricing Sources (Highest Priority)

**Search Strategy:**
- Searched for vendor quotes, budgetary proposals, budget sheets
- Checked deliverable `_REFERENCES.md` files (deliverable folders not yet scaffolded)
- Searched project workspace for pricing documents matching: `quote`, `proposal`, `budget`

**Result:** None found

**Impact:** No vendor-provided pricing available; must rely on rate tables or fallback model.

---

## 2. Rate Tables / Cost Libraries

**Search Strategy:**
- Checked `execution/_Estimates/_RateTables/` for existing rate tables
- Searched for files matching: `rate`, `unit cost`, `cost`, `pricing`

**Result:** No project-specific rate tables found

**Impact:** No project rate tables available; must rely on allowances and fallback model.

---

## 3. Quantity Sources

**Search Strategy:**
- Read decomposition document Section 5, PKG-33 (lines 719-737)
- Checked for deliverable folders under `execution/PKG-33_HSE_Management/`
- Searched for Datasheet.md, Specification.md files

**Results:**

| Source | Available | Content |
|--------|-----------|---------|
| Decomposition (PKG-33) | YES | Package description, 8 deliverables with types and anticipated artifacts |
| Deliverable folders | NO | Not yet scaffolded |
| Datasheet.md files | NO | Not yet created |
| Specification.md files | NO | Not yet created |
| Employer's Requirements Vols 1-3 | NO | Referenced but not yet indexed for HSE requirements |

**Quantities Successfully Extracted:**
- 8 deliverables identified (DEL-33.01 through DEL-33.08)
- Deliverable types: 2 plans, 2 assessments/procedures, 3 installation & test records, 1 method statement
- Anticipated artifacts described

**Quantities NOT Extracted:**
- Specific HSE plan page counts or documentation hours
- Number of risk assessments or method statements required
- Environmental monitoring frequency and duration
- Waste management volumes or disposal frequency
- Emergency response plan complexity and drill requirements

**Impact:** Cannot create detailed effort-based or materials-based estimates; must use lump-sum allowances.

**Source:** Decomposition `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` lines 719-737.

---

## 4. Embedded Fallback Model (Applied)

**Trigger:** No vendor quotes or project rate tables discovered.

**Model Components Used:**
- Indirects factors (CI, PM, P)
- Allowance placeholders for HSE plans, assessments, and records
- Contingency baseline (PCT_BY_BUCKET method)

**Transparency:** All fallback model uses are:
- Labeled `Method=ALLOWANCE` or `Method=PARAMETRIC`
- Marked `Confidence=LOW` or `MED`
- Traced to Decision Log entries (D-005, D-006, D-008)

**Source:** AGENT_ESTIMATING STRUCTURE section (Fallback Typical Model).

---

## 5. Source Priority Applied

Per AGENT_ESTIMATING protocol Section 3.3:

| Priority | Method | PKG-33 Coverage |
|----------|--------|-----------------|
| 1 | Vendor Quotes | 0% (none available) |
| 2 | Rate Tables | 0% (none available) |
| 3 | Allowances / Parametric | 100% (fallback applied) |

**Decision:** D-005 (Use fallback model due to absence of project-specific sources)

---

## 6. Source Quality Assessment

| Source Type | Quality | Availability | Usability |
|-------------|---------|--------------|-----------|
| Vendor quotes | N/A | Not available | N/A |
| Project rate tables | N/A | Not available | N/A |
| Decomposition | HIGH | Available | Good — provides deliverable structure and types |
| Deliverable documents | N/A | Not yet created | N/A |
| Fallback model | LOW-MED | Embedded | Adequate for conceptual estimate |

---

## 7. Recommendations for Next Estimate

To improve estimate maturity from Class 5 to Class 4 or Class 3, provide:

1. **HSE services quotes:**
   - HSE plan preparation services (OHS Plan, Emergency Response Plan)
   - Risk assessment and method statement development services
   - Environmental compliance monitoring services

2. **Project rate tables** in `_Estimates/_RateTables/`:
   - HSE professional labor rates (HSE manager, coordinator, specialist)
   - Environmental consultant rates (monitoring, compliance, reporting)
   - Waste management disposal rates (by waste type)
   - Emergency response equipment/training costs

3. **Deliverable detail:**
   - Scaffold deliverable folders (PREPARATION agent)
   - Initialize drafts (4_DOCUMENTS agent)
   - Define specific HSE documentation requirements in Specification.md

4. **Reference documents:**
   - Employer's Requirements HSE sections (if applicable in Volumes 1-3)
   - VFPA environmental compliance requirements
   - Local authority HSE/environmental permit requirements

---

**Source Index Prepared By:** Estimating Agent (Phase 2.2)
**Date:** 2026-01-29
**Status:** Complete (no project-specific sources found; fallback model applied)
