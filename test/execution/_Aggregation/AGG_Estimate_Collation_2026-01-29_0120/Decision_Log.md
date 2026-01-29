# Decision Log — PKG-00 Site Establishment Estimate

**Snapshot ID:** EST_PKG00_DRAFT_2026-01-28_2315
**Package Scope:** PKG-00 Site Establishment
**Date:** 2026-01-28

---

## D-001: Estimate Scope — Package-Level Estimating

**Decision:** Create separate estimates by package rather than single project-wide estimate.

**Trigger:** Project instructions (INIT.md) specify phased work by package: "Progress one deliverable at a time until all deliverables in that package are complete. Only complete one package at a time."

**Evidence:** `/Users/ryan/ai-env/projects/chirality-app/INIT.md`, lines 3-11.

**Impacted WBS/CBS:** All packages (PKG-00 through PKG-35). This estimate covers PKG-00 only.

**Estimate Impact:** This estimate is a subset of the full project. Indirects, project management, and other cross-package costs are allocated proportionally to PKG-00.

**Override Path:** To create full project estimate, modify scope in `_CONFIG.md` to include all packages.

---

## D-002: Currency Selection — CAD

**Decision:** Use Canadian dollars (CAD) as the estimate currency.

**Trigger:** Default currency selection per AGENT_ESTIMATING protocol (Phase 1.3).

**Evidence:** Project location is Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC (decomposition Section 1, line 10). Canadian location indicates CAD currency.

**Impacted WBS/CBS:** All line items.

**Estimate Impact:** All costs expressed in CAD. No currency conversion required for Canadian vendors/rates.

**Override Path:** Set `currency` parameter in `_CONFIG.md` if different currency required.

---

## D-003: Pricing Date — January 2026

**Decision:** Use January 2026 as the pricing date ("dollars of" month).

**Trigger:** No explicit pricing date found in deliverable documents. Default to current date per AGENT_ESTIMATING protocol.

**Evidence:** Current date is 2026-01-28. No historical pricing dates referenced in deliverable `_REFERENCES.md` files.

**Impacted WBS/CBS:** All line items.

**Estimate Impact:** Costs represent January 2026 pricing. No escalation applied (escalation_mode = NONE per config).

**Override Path:** Set `pricing_date` parameter in `_CONFIG.md` if different pricing basis required.

---

## D-004: Workspace Paths — Default Paths Used

**Decision:** Use default workspace paths specified in AGENT_ESTIMATING instructions.

**Trigger:** Initialization Phase 1.1 — auto-discovery of project paths.

**Evidence:**
- Project workspace: `/Users/ryan/ai-env/projects/chirality-app/test/`
- Execution root: `/Users/ryan/ai-env/projects/chirality-app/test/execution/`
- Decomposition: `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`
- Estimates output: `/Users/ryan/ai-env/projects/chirality-app/test/execution/_Estimates/`

All paths verified as accessible.

**Impacted WBS/CBS:** N/A (infrastructure decision).

**Estimate Impact:** None (path selection does not affect cost values).

**Override Path:** Paths can be overridden via conversation if project structure changes.

---

## D-005: Source Priority — No Project-Specific Pricing Sources Found

**Decision:** Use fallback typical model for pricing due to absence of project-specific quotes, budgets, or rate tables.

**Trigger:** Source discovery (Phase 2.2) found no vendor quotes, budgetary proposals, or project rate tables in deliverable `_REFERENCES.md` files or `_Estimates/_RateTables/` directory.

**Evidence:**
- All deliverable `_REFERENCES.md` files state "no references identified yet" or list only the decomposition document
- `_Estimates/_RateTables/` directory is empty (created during initialization)
- No pricing documents discovered in PKG-00 deliverable folders

**Impacted WBS/CBS:** All CBS buckets.

**Estimate Impact:** HIGH — All line items will use fallback allowances or parametric models with LOW confidence ratings. Estimate totals will have wide uncertainty ranges.

**Override Path:** To improve estimate accuracy:
1. Add vendor quotes to deliverable `_REFERENCES.md` files or place quote files in deliverable folders
2. Add rate tables (CSV, XLSX, or MD format) to `_Estimates/_RateTables/` directory
3. Re-run estimate pipeline

---

## D-006: Indirects Model — Factor-Based (No Schedule Data)

**Decision:** Apply indirects using factor-based model rather than time-based model.

**Trigger:** No construction schedule or duration data discovered in deliverable documents.

**Evidence:** Deliverable `Procedure.md` and `Guidance.md` files reference project duration as "multi-year EPC project" and provide example equipment mobilization/demobilization spanning 52 weeks, but no detailed project schedule or critical path was found.

**Impacted WBS/CBS:** Construction Indirects (CI), Project Management (PM), Commissioning (COM).

**Estimate Impact:** Indirects calculated as factors of Construction Directs (CD) and Materials (MAT) using fallback typical model defaults.

**Override Path:** Provide detailed construction schedule to enable time-based indirects calculation (staffing levels × duration).

---

## D-007: Rounding Policy — Nearest $1,000

**Decision:** Round estimate totals to nearest $1,000 CAD.

**Trigger:** Default rounding policy per AGENT_ESTIMATING protocol and `_CONFIG.md` setting.

**Evidence:** `_CONFIG.md`, rounding = 1000.

**Impacted WBS/CBS:** Summary totals only (detail line items retain calculated precision).

**Estimate Impact:** Minimal — rounding affects presentation only, not line item accuracy.

**Override Path:** Modify `rounding` parameter in `_CONFIG.md` (e.g., 10000 for $10k rounding, 100 for $100 rounding).

---

## D-008: Contingency Method — Percentage by Bucket (PCT_BY_BUCKET)

**Decision:** Apply contingency using percentage-by-CBS-bucket method with allowance-heavy adjustment.

**Trigger:** Default contingency method per AGENT_ESTIMATING protocol and `_CONFIG.md` setting.

**Evidence:** `_CONFIG.md`, contingency_method = PCT_BY_BUCKET. Risk-based three-point estimation not feasible without vendor quotes and project-specific risk data.

**Impacted WBS/CBS:** All CBS buckets — contingency calculated separately for E, PM, P, MAT, CD, CI, COM.

**Estimate Impact:** Contingency will be higher for buckets with high allowance share (due to low confidence in fallback pricing).

**Override Path:**
1. Set `contingency_method = RISK_BASED` in `_CONFIG.md` to enable three-point estimation
2. Provide vendor quotes and project-specific risk data to support risk-based model

---

## D-009: Escalation — Not Applied

**Decision:** Do not apply escalation to this estimate.

**Trigger:** Default escalation mode per AGENT_ESTIMATING protocol and `_CONFIG.md` setting (escalation_mode = NONE).

**Evidence:** No cashflow curve or expenditure schedule discovered. Pricing date (2026-01) represents current pricing; no forward escalation required for draft estimate.

**Impacted WBS/CBS:** All line items (escalation = 0%).

**Estimate Impact:** Estimate represents January 2026 dollars without adjustment for future price changes.

**Override Path:**
1. Set `escalation_mode = EXPLICIT` in `_CONFIG.md`
2. Provide construction schedule with cashflow curve to enable escalation calculation

---

## Decision Summary Table

| Decision ID | Topic | Selection | Confidence | Impact Level |
|-------------|-------|-----------|------------|--------------|
| D-001 | Scope | PKG-00 only | HIGH | HIGH |
| D-002 | Currency | CAD | HIGH | MED |
| D-003 | Pricing Date | 2026-01 | MED | MED |
| D-004 | Paths | Defaults | HIGH | NONE |
| D-005 | Sources | Fallback model | LOW | HIGH |
| D-006 | Indirects | Factor-based | MED | MED |
| D-007 | Rounding | $1,000 | HIGH | LOW |
| D-008 | Contingency | PCT_BY_BUCKET | MED | MED |
| D-009 | Escalation | NONE | HIGH | LOW |

---

**Total Decisions Recorded:** 9
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
