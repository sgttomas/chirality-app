# Decision Log

This log captures all decisions made by the estimating agent during the straight-through pipeline run where defaults were selected, ambiguities were resolved, or interpretations were required.

---

## D-001: Scope Interpretation — Design Basis Documents

**Decision:** Design Basis Documents (DEL-27.01) are interpreted as project-wide multi-discipline design basis memoranda (not discipline-specific design calculations). Discipline-specific design is assumed to be covered under the respective discipline packages (PKG-01 through PKG-26).

**Trigger:** Decomposition does not explicitly distinguish between "project-wide design basis" and "discipline-specific design calculations."

**Evidence:** Decomposition line 614 lists "Design basis memorandum, design criteria" as anticipated artifacts for DEL-27.01. This language suggests high-level criteria documents rather than detailed calculations.

**Impacted WBS/CBS:** PKG-27 / DEL-27.01 / Engineering (E)

**Estimate Impact:** Moderate. This interpretation results in 5 design basis documents (one per discipline) estimated at 200-400 hours each, totaling $215,000 CAD. Alternative interpretation (detailed calculations in PKG-27) would significantly increase the estimate.

**How to Override:** If discipline-specific design calculations should be included in PKG-27, provide explicit scope definition in deliverable folder `_REFERENCES.md` or `Specification.md` and re-run estimate.

---

## D-002: Disciplines Requiring Design Basis Documents

**Decision:** Design basis documents are required for 5 core disciplines: Civil/Structural, Mechanical (Process), Electrical, I&C, and Marine.

**Trigger:** Decomposition does not list specific disciplines for design basis documents.

**Evidence:** Project scope includes civil/structural works (PKG-01 through PKG-08), mechanical/process systems (PKG-10 through PKG-16), electrical systems (PKG-17 through PKG-18), instrumentation & controls (PKG-19 through PKG-20), and marine structures/loading (PKG-08, PKG-09, PKG-11). Building-specific design basis is assumed to be covered under PKG-21/PKG-22.

**Impacted WBS/CBS:** PKG-27 / DEL-27.01 / Engineering (E)

**Estimate Impact:** Moderate. 5 disciplines × $35,000-$55,000 each = $215,000 total. Fewer disciplines would reduce cost; additional disciplines (e.g., separate Buildings, Fire Protection) would increase cost.

**How to Override:** Provide explicit discipline list in deliverable folder or config and re-run estimate.

---

## D-003: HAZOP Study Duration and Participation

**Decision:** HAZOP study is estimated as 5 days of facilitated sessions with senior engineering participation from 5 disciplines.

**Trigger:** Decomposition does not specify HAZOP study duration or participant count.

**Evidence:** Industry typical for bulk liquid transload facility with 3 storage tanks, railcar unloading, marine loading, and product transfer systems. Typical HAZOP for 10-15 process nodes requires 5 days of facilitated sessions.

**Impacted WBS/CBS:** PKG-27 / DEL-27.02 / Engineering (E)

**Estimate Impact:** Moderate. HAZOP total = $66,200 CAD. Shorter duration (3 days) would reduce to ~$45,000; longer duration (7 days) would increase to ~$85,000.

**How to Override:** Provide HAZOP scope definition (number of process nodes, required participants, session duration) in deliverable folder or rate table with HAZOP facilitator quote and re-run estimate.

---

## D-004: Phase 2 Expansion Documentation Scope

**Decision:** Phase 2 expansion documentation includes concept design (general arrangement drawing) and feasibility engineering (capacity analysis, staging assessment, order-of-magnitude cost estimate).

**Trigger:** Decomposition lists "Phase 2 general arrangement drawing, Phase 2 engineering memo" but does not specify level of detail (concept vs. detailed feasibility).

**Evidence:** Decomposition line 616 lists "Phase 2 Expansion Documentation" under PKG-27 (Engineering Design), suggesting forward-looking planning rather than detailed Phase 2 design. Detailed Phase 2 design would be a separate future project phase.

**Impacted WBS/CBS:** PKG-27 / DEL-27.03 / Engineering (E)

**Estimate Impact:** Moderate. Phase 2 documentation total = $113,000 CAD. Concept-only (no feasibility engineering) would reduce to ~$65,000; detailed feasibility (including detailed cost estimate, schedule, risk assessment) would increase to ~$180,000.

**How to Override:** Clarify Phase 2 documentation scope with Employer/Client and provide updated scope definition in deliverable folder or config, then re-run estimate.

---

## D-005: Design Submission Package Effort Assumptions

**Decision:** Design submission packages are estimated with increasing effort at each milestone:
- 30% Design: 500 hours ($95,000)
- 60% Design: 600 hours ($110,000)
- 90% Design: 700 hours ($125,000)
- IFC (Issued for Construction): 850 hours ($145,000)

**Trigger:** Decomposition does not specify engineering effort for design submission package compilation and coordination.

**Evidence:** Typical design-build project with 200-300 total IFC drawings across all disciplines. Early submissions have fewer drawings but require proportionally more coordination effort per drawing due to inter-discipline interface resolution.

**Impacted WBS/CBS:** PKG-27 / DEL-27.04 / Engineering (E)

**Estimate Impact:** High. Design submission packages total = $475,000 CAD (42% of total base estimate). This is the largest single deliverable in PKG-27.

**How to Override:** Provide project schedule with design milestone dates, estimated drawing counts per milestone, and coordination requirements in deliverable folder or config, then re-run estimate.

---

## D-006: Cathodic Protection Design Scope

**Decision:** Cathodic protection design includes marine structures (piles, berthing, loading platform) and buried/submerged infrastructure (underground piping, tank bottom protection if applicable).

**Trigger:** Decomposition lists "CP design basis, anode layout calculations, current demand calculations, design drawings" but does not specify which structures require cathodic protection.

**Evidence:** Project includes marine structures (PKG-08, PKG-09, PKG-11) and underground utilities (PKG-03) in a coastal marine environment, which typically requires cathodic protection for steel structures and buried piping.

**Impacted WBS/CBS:** PKG-27 / DEL-27.05 / Engineering (E)

**Estimate Impact:** Moderate. Cathodic protection design total = $75,000 CAD. Limited scope (marine piles only) would reduce to ~$40,000; expanded scope (including all buried piping, tank farm, rail infrastructure) would increase to ~$120,000.

**How to Override:** Provide geotechnical study results, corrosivity testing data, and final design of structures requiring CP, then re-run estimate with updated scope.

---

## D-007: No Vendor Quotes Available

**Decision:** No vendor quotes were found in the workspace. All line items are priced using parametric/allowance methods.

**Trigger:** Source discovery phase (Function 2) found no vendor quotes, budgetary proposals, or quotations in the workspace.

**Evidence:** Search conducted in:
- Deliverable `_REFERENCES.md` files (PKG-27 deliverables not yet scaffolded)
- Project workspace for files matching "quote", "proposal", "budget"
- No matching files found.

**Impacted WBS/CBS:** All PKG-27 deliverables (all CBS categories affected)

**Estimate Impact:** High. Entire estimate is based on parametric/allowance pricing, resulting in LOW confidence and WARNINGS status. Vendor quotes for specialist sub-consultants (HAZOP facilitator, CP specialist) would improve confidence.

**How to Override:** Obtain budgetary quotes from specialist sub-consultants and engineering service providers, save to workspace with clear filenames (e.g., "HAZOP_Facilitator_Quote_2026.pdf"), and re-run estimate.

---

## D-008: No Project-Specific Rate Tables Available

**Decision:** No project-specific engineering rate tables were found in `_RateTables/` directory. Industry typical rates for Greater Vancouver engineering market were used as parametric basis.

**Trigger:** Source discovery phase (Function 2) found no rate tables in `execution/_Estimates/_RateTables/` directory.

**Evidence:** Directory exists but is empty.

**Impacted WBS/CBS:** All PKG-27 deliverables (Engineering (E) CBS category primarily affected)

**Estimate Impact:** High. All engineering rates are parametric assumptions ($145-$185/hr blended rates), resulting in LOW confidence. Project-specific rate tables with negotiated engineering service rates would improve confidence.

**How to Override:** Create engineering rate table in `execution/_Estimates/_RateTables/Engineering_Rates_2026.csv` with columns: Discipline, Level (Senior/Intermediate/Junior), HourlyRate_CAD, and re-run estimate.

---

## D-009: Project Management Factor Adjustment

**Decision:** Project Management (PM) factor set to 11.5% of Engineering (E) base, higher than fallback model default (6%).

**Trigger:** PKG-27 scope includes multi-discipline coordination across 5 core disciplines, HAZOP facilitation, and four major design submission milestones requiring significant PM oversight.

**Evidence:** Fallback model default PM factor is 6% for typical projects. Design-only packages with high coordination complexity typically range 8-12%. PKG-27 has exceptionally high coordination requirements due to multi-discipline design basis development and four major submission milestones.

**Impacted WBS/CBS:** PKG-27 / N/A / Project Management (PM)

**Estimate Impact:** Moderate. PM total = $130,000 CAD (11.5% of E base $944,200). Fallback model default (6%) would result in PM = $57,000, reducing total estimate by $73,000.

**How to Override:** If PM factor should be different, update `_CONFIG.md` with `pm_factor: 0.06` (or other value) and re-run estimate.

---

## D-010: WBS-to-CBS Mapping for PKG-27

**Decision:** All PKG-27 deliverables mapped to Engineering (E) CBS category because this package is exclusively design engineering work. Support activities (PM, CD, CI, COM) are assigned to their respective CBS categories per standard project structure.

**Trigger:** Decomposition does not specify CBS mapping for deliverables.

**Evidence:** PKG-27 scope is "All engineering design, investigations, studies, HAZOP, Phase 2 feasibility documentation" per decomposition line 608. All deliverables are engineering design or engineering analysis activities.

**Impacted WBS/CBS:** All PKG-27 deliverables / Engineering (E) primarily

**Estimate Impact:** None (this is a classification decision, not a cost decision).

**How to Override:** Not applicable (standard CBS mapping per project structure).

---

## D-011: Contingency Method and Application

**Decision:** PCT_BY_BUCKET contingency method selected per config default. Baseline contingency percentages applied with allowance-heavy adjustments (+2% for buckets with >50% allowance share).

**Trigger:** Config file specifies `contingency_method: PCT_BY_BUCKET`.

**Evidence:** Config file `/Users/ryan/ai-env/projects/chirality-app/test/execution/_Estimates/_CONFIG.md` line 35.

**Impacted WBS/CBS:** All CBS categories

**Estimate Impact:** Moderate. Total contingency = $141,000 (12.5% weighted average). Engineering (E) and PM buckets received +2% adjustment due to allowance-heavy pricing (>50% allowance share). Alternative RISK_BASED method would produce three-point estimate range.

**How to Override:** To use RISK_BASED contingency method, update `_CONFIG.md` with `contingency_method: RISK_BASED` and re-run estimate.

---

## Summary

| Decision ID | Topic | Estimate Impact |
|-------------|-------|----------------|
| D-001 | Scope interpretation — Design Basis Documents | Moderate |
| D-002 | Disciplines requiring design basis documents | Moderate |
| D-003 | HAZOP study duration and participation | Moderate |
| D-004 | Phase 2 expansion documentation scope | Moderate |
| D-005 | Design submission package effort assumptions | High |
| D-006 | Cathodic protection design scope | Moderate |
| D-007 | No vendor quotes available | High |
| D-008 | No project-specific rate tables available | High |
| D-009 | Project Management factor adjustment | Moderate |
| D-010 | WBS-to-CBS mapping for PKG-27 | None |
| D-011 | Contingency method and application | Moderate |

**Total Decisions:** 11

**Decisions with HIGH impact:** 3 (D-005, D-007, D-008)

**Decisions requiring user input for next run:** D-003 (HAZOP scope), D-004 (Phase 2 scope), D-005 (design submission effort), D-006 (CP scope), D-007 (obtain quotes), D-008 (create rate tables)

---

**Decision Log Prepared By:** ESTIMATING Agent (Straight-Through Pipeline)
**Date:** 2026-01-29 00:40
