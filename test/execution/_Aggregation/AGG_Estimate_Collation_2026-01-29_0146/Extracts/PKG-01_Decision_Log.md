# Decision Log — PKG-01 Demolition & Removals Estimate

**Snapshot ID:** EST_PKG01_DRAFT_2026-01-28_2330
**Package Scope:** PKG-01 Demolition & Removals
**Date:** 2026-01-28

---

## D-010: Estimate Scope — PKG-01 Only

**Decision:** Create estimate for PKG-01 Demolition & Removals only.

**Trigger:** Project instructions (INIT.md) specify phased work by package.

**Evidence:** `/Users/ryan/ai-env/projects/chirality-app/INIT.md`, lines 3-6; continuation of package-by-package estimating approach established in D-001 (PKG-00 estimate).

**Impacted WBS/CBS:** PKG-01 (4 deliverables: DEL-01.01 through DEL-01.04).

**Estimate Impact:** This estimate covers only PKG-01 demolition scope. Indirects and PM allocated proportionally.

**Override Path:** To create full project estimate, modify scope in `_CONFIG.md` to include all packages.

---

## D-011: Currency Selection — CAD (Inherited)

**Decision:** Use Canadian dollars (CAD) as the estimate currency.

**Trigger:** Inherited from PKG-00 estimate basis (D-002) and `_CONFIG.md`.

**Evidence:** Project location is Fraser Surrey Terminal, Surrey, BC. `_CONFIG.md` specifies `currency = CAD`.

**Impacted WBS/CBS:** All line items.

**Estimate Impact:** All costs expressed in CAD.

**Override Path:** Set `currency` parameter in `_CONFIG.md`.

---

## D-012: Pricing Date — January 2026 (Inherited)

**Decision:** Use January 2026 as the pricing date.

**Trigger:** Inherited from PKG-00 estimate basis (D-003) and `_CONFIG.md`.

**Evidence:** `_CONFIG.md` specifies `pricing_date = 2026-01`.

**Impacted WBS/CBS:** All line items.

**Estimate Impact:** Costs represent January 2026 pricing.

**Override Path:** Set `pricing_date` parameter in `_CONFIG.md`.

---

## D-013: Source Priority — No Project-Specific Pricing Sources Found

**Decision:** Use fallback typical model for pricing due to absence of project-specific quotes, budgets, or rate tables.

**Trigger:** Source discovery found no vendor quotes, budgetary proposals, or project rate tables in PKG-01 deliverable folders or `_Estimates/_RateTables/` directory.

**Evidence:**
- All PKG-01 deliverable `_REFERENCES.md` files reference only the decomposition document
- `_Estimates/_RateTables/` directory is empty
- No demolition contractor quotes or marine removal quotes discovered

**Impacted WBS/CBS:** All CBS buckets.

**Estimate Impact:** HIGH — All line items will use fallback allowances with LOW confidence. Demolition costs are highly site-specific and require contractor quotes for accuracy.

**Override Path:**
1. Obtain demolition contractor budgetary quotes (Track 6, Dolphin 2)
2. Obtain marine contractor quote for Dolphin 2 marine work
3. Add rate tables or quotes to `_Estimates/_RateTables/` or deliverable folders
4. Re-run estimate pipeline

---

## D-014: Demolition Scope Breakdown — Structure-Based Estimation

**Decision:** Estimate demolition costs by major structure: Track 6 (rail), Dolphin 2 (marine), fencing, salt tent.

**Trigger:** Decomposition PKG-01 scope explicitly identifies these four demolition items with distinct work types requiring different methods and equipment.

**Evidence:** Decomposition PKG-01 scope: "Removal and disposal of existing infrastructure including Track 6, Dolphin 2, fencing, salt tent dismantling, and associated decommissioning."

**Impacted WBS/CBS:** CD (Construction Directs), MAT (Materials for disposal/protection).

**Estimate Impact:** Four separate allowance line items for construction directs, sized based on typical demolition work complexity:
- Track 6: Rail infrastructure (moderate complexity, specialized equipment)
- Dolphin 2: Marine structure (high complexity, marine equipment required)
- Fencing: Simple removal (low complexity)
- Salt tent: Building structure (moderate complexity)

**Override Path:** Provide structure-specific quantities (linear feet of track, pile count for dolphin, linear feet of fencing, tent dimensions) to enable quantity-based pricing.

---

## D-015: Dolphin 2 Marine Demolition — Marine Equipment Requirement

**Decision:** Dolphin 2 demolition requires marine equipment (barge, crane) and is estimated as a marine construction operation with higher unit costs.

**Trigger:** Structure type (marine dolphin) and location require over-water demolition operations.

**Evidence:** DEL-01.03 Datasheet.md specifies Dolphin 2 removal procedure requires "marine equipment mobilization (barge, crane)" and "marine traffic coordination, tide/weather assessment, marine safety zone establishment."

**Impacted WBS/CBS:** CD (Dolphin 2 line item).

**Estimate Impact:** Dolphin 2 allowance sized higher than land-based demolition to account for marine equipment mob/demob, marine crew, weather sensitivity, and marine safety requirements. Confidence is LOW due to lack of marine contractor quote.

**Override Path:** Obtain marine demolition contractor budgetary quote with scope specific to Dolphin 2 structure (pile count, deck area, access conditions).

---

## D-016: Hazardous Materials — Status Unknown

**Decision:** Exclude hazardous materials abatement costs from base estimate; add placeholder allowance for potential contamination.

**Trigger:** Deliverable documents indicate hazardous materials presence is TBD pending survey.

**Evidence:** DEL-01.02 Datasheet.md states "Hazardous materials: TBD (presence and extent of hazardous materials in existing structures to be demolished)." DEL-01.02 Specification R21 addresses special disposal requirements for hazardous materials "if present."

**Impacted WBS/CBS:** CD (potential hazmat abatement), MAT (disposal costs).

**Estimate Impact:** A contingency placeholder is included for potential hazardous materials discovery. If hazmat survey identifies asbestos, lead, or contaminated materials, costs could increase significantly.

**Override Path:** Complete hazardous materials survey prior to estimate finalization. If hazmat present, add abatement costs and licensed hazmat contractor costs.

---

## D-017: Indirects Model — Factor-Based (Inherited)

**Decision:** Apply indirects using factor-based model.

**Trigger:** Inherited from PKG-00 estimate basis (D-006). No schedule data available for time-based calculation.

**Evidence:** No construction schedule with PKG-01 duration. Deliverable Procedure.md documents do not specify demolition duration.

**Impacted WBS/CBS:** CI, PM, P.

**Estimate Impact:** Indirects calculated as factors of CD and MAT per fallback model.

**Override Path:** Provide PKG-01 demolition schedule duration to enable time-based indirects.

---

## D-018: Contingency Method — PCT_BY_BUCKET (Inherited)

**Decision:** Apply contingency using percentage-by-CBS-bucket method with allowance-heavy adjustment.

**Trigger:** Inherited from PKG-00 estimate basis (D-008) and `_CONFIG.md`.

**Evidence:** `_CONFIG.md` specifies `contingency_method = PCT_BY_BUCKET`. 100% of PKG-01 estimate is ALLOWANCE-based, triggering maximum allowance adjustment.

**Impacted WBS/CBS:** All CBS buckets.

**Estimate Impact:** Higher contingency applied due to 100% allowance-based estimate (baseline + 10% allowance adjustment).

**Override Path:** Obtain vendor quotes to reduce allowance share and corresponding contingency.

---

## Decision Summary Table

| Decision ID | Topic | Selection | Confidence | Impact Level |
|-------------|-------|-----------|------------|--------------|
| D-010 | Scope | PKG-01 only | HIGH | HIGH |
| D-011 | Currency | CAD (inherited) | HIGH | MED |
| D-012 | Pricing Date | 2026-01 (inherited) | MED | MED |
| D-013 | Sources | Fallback model | LOW | HIGH |
| D-014 | Structure Breakdown | 4 structures | MED | MED |
| D-015 | Dolphin 2 | Marine equipment | MED | HIGH |
| D-016 | Hazmat | Unknown (excluded) | LOW | HIGH |
| D-017 | Indirects | Factor-based | MED | MED |
| D-018 | Contingency | PCT_BY_BUCKET | MED | MED |

---

**Total Decisions Recorded:** 9
