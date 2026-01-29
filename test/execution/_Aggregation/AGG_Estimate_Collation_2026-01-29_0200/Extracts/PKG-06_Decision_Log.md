# Decision Log

## Snapshot ID
EST_PKG06_DRAFT_2026-01-28_2333

## Purpose
This log records all decisions made by the estimating agent during the straight-through pipeline run for PKG-06 Structural Steelwork.

---

## D-001: Currency Selection

**Decision:** CAD (Canadian dollars)

**Trigger:** No explicit currency override in config; must select single currency for snapshot.

**Evidence:**
- Project location: Fraser Surrey Terminal, Surrey, BC, Canada (decomposition Section 1)
- File: `test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`

**Impacted WBS/CBS:** All packages and CBS buckets

**Estimate Impact:** All line items priced in CAD; no currency conversion required.

**Override Path:** Specify `currency: USD` (or other) in `execution/_Estimates/_CONFIG.md` if CAD is incorrect.

---

## D-002: Pricing Date

**Decision:** 2026-01 (January 2026 dollars)

**Trigger:** No explicit pricing date in config or source documents.

**Evidence:** Current date (2026-01-28); no historical pricing basis found.

**Impacted WBS/CBS:** All

**Estimate Impact:** Pricing basis is current month; no escalation applied (escalation_mode = NONE).

**Override Path:** Specify `pricing_date: YYYY-MM` in config if different basis is required.

---

## D-003: Estimate Label

**Decision:** PKG06_DRAFT

**Trigger:** No estimate label specified in config.

**Evidence:** Default label convention per AGENT_ESTIMATING.md (Function 1.3).

**Impacted WBS/CBS:** Metadata only (snapshot identification)

**Estimate Impact:** Snapshot labeled as draft; not for procurement or commitment.

**Override Path:** Specify `estimate_label` in config (e.g., `30PCT`, `IFC`, `BUDGET`).

---

## D-004: CBS Inclusions/Exclusions

**Decision:** Include E, PM, P, MAT, CD, CI, COM, CONT; exclude Owner's costs, land, financing, permits obtained by Employer, escalation, taxes.

**Trigger:** No config override; default inclusion/exclusion per AGENT_ESTIMATING.md (Function 1.3).

**Evidence:**
- Decomposition Section 1.2: Contractor scope only; Employer-responsible items excluded except interfaces.
- AGENT_ESTIMATING.md: default `include_scopes` and `exclude_scopes`.

**Impacted WBS/CBS:** All CBS buckets

**Estimate Impact:** Estimate covers full EPC-style D&B scope; excludes owner/financing items.

**Override Path:** Modify config `include_scopes` / `exclude_scopes` if different scope is required.

---

## D-005: WBS → CBS Mapping for PKG-06

**Decision:** Map PKG-06 deliverables to CBS as follows:
- DEL-06.01 (Drawing Set) → E (Engineering & Design)
- DEL-06.02 (Technical Specification) → E
- DEL-06.03 (Design Calculations) → E
- DEL-06.04 (Data Sheet Package) → E
- DEL-06.05 (Installation & Test Records) → E (QA/documentation effort)

Construction/installation scope (not tied to specific deliverables) → CD, MAT, CI

**Trigger:** Deliverable types indicate engineering/design work; construction is implicit in package scope.

**Evidence:**
- Decomposition PKG-06 deliverables (lines 248-252): types are Drawing, Specification, Calculation, Data Sheet, Record
- Package scope (line 242): steel platforms, stairs, gangways, access structures, handrails, pipe supports

**Impacted WBS/CBS:** All PKG-06 deliverables and construction line items

**Estimate Impact:** Engineering effort separated from materials/construction; allows CBS-based contingency.

**Override Path:** N/A (standard WBS→CBS mapping per deliverable type).

---

## D-006: Productivity and Location Factors

**Decision:** Productivity factor = 1.0 (BC lower mainland baseline); no location adjustment applied.

**Trigger:** No project-specific productivity or location data available.

**Evidence:**
- Location: Fraser Surrey Terminal, Surrey, BC (decomposition)
- Assumption: BC lower mainland is baseline productivity region (no remote/offshore adjustment)

**Impacted WBS/CBS:** CD, CI (construction labor productivity)

**Estimate Impact:** Labor hours and indirects computed using standard BC productivity; no uplift or reduction.

**Override Path:** If site-specific productivity data becomes available (remote access, congestion, working hours constraints), adjust labor hour estimates or apply factor in config.

---

## D-007: Geotechnical/Foundation Interface Assumption

**Decision:** Assume structural steel platforms/pipe racks will be supported on concrete foundations provided under PKG-05 (Concrete Structures). Coordination of foundation loads is external (dependency tracking mode = NOT_TRACKED).

**Trigger:** No explicit foundation design information in PKG-06 deliverables.

**Evidence:**
- PKG-06 scope (decomposition): platforms, stairs, gangways, handrails, pipe supports
- PKG-05 scope (decomposition): concrete structures (likely includes foundations)
- `_DEPENDENCIES.md`: NOT_TRACKED

**Impacted WBS/CBS:** PKG-06 MAT, CD (structural steel erection assumes foundations are ready)

**Estimate Impact:** Structural steel estimate does not include foundation costs (those are in PKG-05).

**Override Path:** Confirm foundation responsibility via cross-package coordination (outside estimating agent scope).

---

## D-008: Pricing Basis Selection (All Allowances)

**Decision:** All PKG-06 line items priced via allowances using fallback typical model.

**Trigger:** No vendor quotes or rate tables available; explicit quantities (tonnage, counts) not yet defined in deliverables (TBD status).

**Evidence:**
- Source_Index.md: no quotes, no rate tables, no design drawings with quantities
- Deliverables status: INITIALIZED (quantities TBD pending design)

**Impacted WBS/CBS:** All CBS buckets (E, MAT, CD, CI, PM, P, COM)

**Estimate Impact:** All line items have Method=ALLOWANCE or Method=PARAMETRIC; Confidence=LOW. Contingency percentages elevated per allowance-heavy adjustment (AGENT_ESTIMATING.md, STRUCTURE: Fallback Typical Model).

**Override Path:** Provide structural steel design drawings (with tonnages, counts, sizes), vendor quotes, or project rate tables to replace allowances with quantity-based pricing in next run.

---

## D-009: Indirects/Services Factors (Fallback Model)

**Decision:** Apply factor-based indirects per fallback typical model:
- CI (Construction Indirects) = 0.18 × CD
- P (Procurement Services) = 0.02 × MAT
- PM (EPCM/Project Management) = 0.06 × (CD + CI + MAT)
- COM (Commissioning) = 0.03 × (CD + CI + MAT)

**Trigger:** No time-based schedule or project-specific indirects model available.

**Evidence:** AGENT_ESTIMATING.md, STRUCTURE: Fallback Typical Model (default factors).

**Impacted WBS/CBS:** CI, P, PM, COM

**Estimate Impact:** Indirects/services are parametric (factor-derived); not based on project schedule or org chart.

**Override Path:** Provide project schedule with durations, staffing plan, or project-specific indirects rates in config/rate tables.

---

## D-010: Contingency Method and Percentages

**Decision:** Use PCT_BY_BUCKET method with allowance-heavy adjustment:
- E: 10% base + 10% allowance adjustment = 20%
- MAT: 15% base + 10% allowance adjustment = 25%
- CD: 20% base + 10% allowance adjustment = 30%
- CI: 20% base + 10% allowance adjustment = 30%
- PM: 10% base + 5% (factor-derived adjustment) = 15%
- P: 10% base + 5% (factor-derived adjustment) = 15%
- COM: 25% base + 5% (factor-derived adjustment) = 30%

**Trigger:** contingency_method = PCT_BY_BUCKET (default); all base estimate lines are allowance/parametric (100% allowance share for E, MAT, CD).

**Evidence:**
- AGENT_ESTIMATING.md, STRUCTURE: Fallback Typical Model (contingency defaults and allowance-heavy adjustment formula)
- Source_Index.md: 100% allowance-based estimate

**Impacted WBS/CBS:** All CBS buckets

**Estimate Impact:** Contingency percentages elevated due to low estimate maturity and absence of vendor pricing.

**Override Path:** Provide vendor quotes or detailed design to reduce allowance share and lower contingency %.

---

## D-011: Escalation Mode

**Decision:** escalation_mode = NONE (no escalation applied).

**Trigger:** Default config; pricing date is current (2026-01).

**Evidence:** AGENT_ESTIMATING.md, Function 1.3 (default escalation_mode).

**Impacted WBS/CBS:** All

**Estimate Impact:** Estimate totals are in January 2026 dollars; no adjustment for future expenditure timing.

**Override Path:** Set `escalation_mode: EXPLICIT` in config and provide cashflow curve or escalation factors if escalation is required.

---

## D-012: Structural Steel Tonnage Allowance (Placeholder)

**Decision:** Estimate structural steel fabricated tonnage as 150 tonnes (allowance).

**Trigger:** No design drawings or calculations with explicit tonnage available.

**Evidence:**
- Package scope: platforms, stairs, gangways, pipe racks, handrails, pipe supports (decomposition line 242)
- Assumption: medium-scale industrial facility structural steel package
- Comparable EPC projects: 100-200 tonnes typical for railcar unloading facility access structures

**Impacted WBS/CBS:** MAT (structural steel material), CD (fabrication/erection labor)

**Estimate Impact:** Allowance sizing for MAT and CD line items; actual tonnage may vary significantly when design is complete.

**Override Path:** Provide structural steel design drawings with member sizes/lengths or explicit tonnage estimate from DEL-06.03 calculations.

---

## D-013: Handrail and Grating Allowances

**Decision:** Estimate handrail as 400 linear meters and grating as 800 m² (allowances).

**Trigger:** No design drawings or data sheets with explicit quantities available.

**Evidence:**
- DEL-06.04 scope: gangway data sheets, grating data sheets (decomposition line 251)
- Package scope: access platforms, stairs, gangways (decomposition line 242)
- Assumption: industrial railcar unloading facility with 32 unloading stations requires extensive walkways and grating

**Impacted WBS/CBS:** MAT (handrail/grating supply), CD (installation labor)

**Estimate Impact:** Allowance sizing; actual quantities TBD when design drawings (DEL-06.01) are issued.

**Override Path:** Provide platform/gangway layout drawings showing linear footage of handrails and grating areas.

---

**Decision Log compiled:** 2026-01-28 23:33
**Total Decisions:** 13 (D-001 through D-013)
