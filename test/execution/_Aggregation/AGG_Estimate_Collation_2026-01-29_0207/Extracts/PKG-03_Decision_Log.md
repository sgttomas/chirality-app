# Decision Log

## Snapshot Identification

| Field | Value |
|-------|-------|
| Snapshot ID | EST_PKG03_DRAFT_2026-01-28_2330 |
| Package | PKG-03 Underground Utilities & Drainage |
| Date | 2026-01-28 |

## Decision Entries

### D-001: Currency Selection

**Decision:** Use CAD (Canadian dollars) for this estimate.

**Trigger:** Currency not explicitly stated in deliverables; required for estimate execution.

**Evidence:**
- Project location is Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC, Canada (Source: decomposition Section 1)
- Config file `/Users/ryan/ai-env/projects/chirality-app/test/execution/_Estimates/_CONFIG.md` specifies `currency: CAD`

**Impacted WBS/CBS:** All packages and CBS buckets (currency applies to entire estimate)

**Estimate Impact:** All costs expressed in CAD; no currency conversion required

**Override Path:** Modify `_CONFIG.md` if different currency is required

---

### D-002: Pricing Date

**Decision:** Use 2026-01 (January 2026) as pricing date.

**Trigger:** Pricing date required for estimate basis and future escalation reference.

**Evidence:**
- Config file specifies `pricing_date: 2026-01`
- Current date is 2026-01-28 (January 2026)

**Impacted WBS/CBS:** All CBS buckets (pricing date applies to all costs)

**Estimate Impact:** Estimate is in "January 2026 dollars"; no escalation applied (escalation_mode = NONE per config)

**Override Path:** Modify `_CONFIG.md` pricing_date if different pricing basis is required

---

### D-003: Estimate Label

**Decision:** Use `PKG03_DRAFT` as estimate label.

**Trigger:** Estimate label required for snapshot identification and tracking.

**Evidence:**
- Following established pattern from previous packages (PKG00_DRAFT, PKG01_DRAFT, PKG02_DRAFT per _LATEST.md)
- Config file lists `estimate_label: PKG00_DRAFT` (package-specific labels per snapshot)

**Impacted WBS/CBS:** N/A (metadata only)

**Estimate Impact:** None (label is for identification only)

**Override Path:** Provide different label via config or user instruction for next run

---

### D-004: Scope Inclusions

**Decision:** Include Engineering (E), PM, Procurement (P), Materials (MAT), Construction Directs (CD), Construction Indirects (CI), Commissioning (COM).

**Trigger:** CBS scope definition required for estimate coverage.

**Evidence:**
- Config file specifies include scopes list
- PKG-03 scope includes design deliverables (engineering), equipment/materials (procurement, materials), installation (construction), testing (commissioning) per decomposition

**Impacted WBS/CBS:** All CBS buckets except excluded scopes

**Estimate Impact:** Estimate includes full EPC coverage for contractor scope

**Override Path:** Modify `_CONFIG.md` include_scopes/exclude_scopes if different coverage is required

---

### D-005: Scope Exclusions

**Decision:** Exclude Owner's costs, land acquisition, financing costs, permits obtained by Employer.

**Trigger:** Exclusions required for estimate boundary definition.

**Evidence:**
- Config file specifies exclude scopes
- Decomposition Section 1.2 Scope Focus confirms "Contractor's scope of work only. Employer-responsible items (permits obtained by Employer, nitrogen skid supply) are excluded except for interface connections."

**Impacted WBS/CBS:** N/A (exclusions)

**Estimate Impact:** Permits obtained by Employer are not costed; Contractor scope only

**Override Path:** Review decomposition Section 1.2 if scope boundary changes

---

### D-006: Contingency Method

**Decision:** Use `PCT_BY_BUCKET` (percentage by CBS bucket) with allowance-based adjustments.

**Trigger:** Contingency method required for risk reserve calculation.

**Evidence:**
- Config file specifies `contingency_method: PCT_BY_BUCKET`
- Fallback typical model (AGENT_ESTIMATING.md STRUCTURE section) defines baseline contingency percentages by CBS bucket and allowance-heavy adjustments

**Impacted WBS/CBS:** Contingency (CONT) applied to all CBS buckets

**Estimate Impact:** Contingency rates elevated due to 100% allowance-based estimate (see Risk_Register.md for bucket-specific rates)

**Override Path:** Modify `_CONFIG.md` contingency_method to RISK_BASED if risk-based contingency is preferred; provide risk data for risk quantification

---

### D-007: Escalation Mode

**Decision:** Use `NONE` (no escalation).

**Trigger:** Escalation mode required for estimate basis definition.

**Evidence:**
- Config file specifies `escalation_mode: NONE`
- Pricing date is current (2026-01); no escalation required for current pricing

**Impacted WBS/CBS:** N/A (no escalation bucket)

**Estimate Impact:** Estimate total does not include escalation; costs are in current January 2026 dollars

**Override Path:** Modify `_CONFIG.md` escalation_mode to EXPLICIT if escalation is required; provide schedule/cashflow curve and escalation factors

---

### D-008: Pricing Method for All Line Items

**Decision:** Use ALLOWANCE method for all line items due to absence of vendor quotes, rate tables, and explicit quantities.

**Trigger:** No pricing sources or explicit quantities available; pricing method required for estimate execution.

**Evidence:**
- Source Index shows 0 vendor quotes, 0 rate tables
- All deliverables in INITIALIZED status with quantities TBD
- Fallback typical model permits allowance-based pricing when sources are not available (AGENT_ESTIMATING.md STRUCTURE section "Placeholder allowance policy")

**Impacted WBS/CBS:** All CBS buckets (Engineering, Materials, Construction Directs, Construction Indirects, PM, Procurement, Commissioning)

**Estimate Impact:** All line items are lump-sum allowances (Qty=1, Unit=LS, UnitRate=Amount); estimate confidence is LOW

**Override Path:** Provide design quantities from DEL-03.01 drawings and vendor quotes for materials/equipment to enable volume-based and quote-based pricing

---

### D-009: Indirects Model Selection

**Decision:** Use factor-based indirects model (fallback typical model).

**Trigger:** No schedule/duration data available; indirects model required for CI, PM, P, COM pricing.

**Evidence:**
- No schedule or duration data discovered in deliverables
- Fallback typical model (AGENT_ESTIMATING.md STRUCTURE section "Default factors") defines factor-based indirects:
  - Construction Indirects (CI) = 0.18 × Construction Directs (CD)
  - Procurement Services (P) = 0.02 × (MAT + FRT)
  - EPCM/PM = 0.06 × (CD + CI + MAT)
  - Commissioning (COM) = 0.03 × (CD + CI + MAT)

**Impacted WBS/CBS:** CI, PM, P, COM buckets

**Estimate Impact:** Indirects are factor-derived based on directs/materials base costs

**Override Path:** Provide project schedule with durations and resource loading to enable time-based indirects pricing

---

### D-010: WBS → CBS Mapping for PKG-03 Deliverables

**Decision:** Map PKG-03 deliverables to CBS buckets as follows:
- DEL-03.01, 03.02, 03.03, 03.04, 03.06 → Engineering (E)
- DEL-03.05 → Construction Indirects (CI) for QA/QC records capture
- Storm drainage materials → Materials (MAT) + Construction Directs (CD)
- OWS equipment → Materials (MAT) + Construction Directs (CD)
- Duct banks → Materials (MAT) + Construction Directs (CD)
- Trenchless crossings → Construction Directs (CD)

**Trigger:** WBS → CBS mapping required for cost categorization.

**Evidence:**
- DEL-03.01 through DEL-03.04 are design deliverables (Drawing, Specification, Calculation, Data Sheet) → Engineering discipline
- DEL-03.05 is QA/QC records → Construction Indirects
- DEL-03.06 is specialist surveyor report → Engineering
- PKG-03 scope includes materials (pipes, OWS, duct bank materials) → Materials bucket
- PKG-03 scope includes installation (excavation, pipe laying, OWS installation, duct bank construction, trenchless boring) → Construction Directs
- Testing and commissioning (pressure testing, CCTV, OWS performance verification) → included in Commissioning bucket via indirects factor

**Impacted WBS/CBS:** All PKG-03 deliverables mapped to E, MAT, CD, CI buckets

**Estimate Impact:** Cost distribution across CBS buckets reflects engineering-heavy (design) + materials/construction (installation) mix

**Override Path:** Review mapping if deliverable types or CBS bucket definitions change

---

### D-011: Allowance Sizing Approach for PKG-03

**Decision:** Size allowances using engineering judgment based on typical underground utilities scope for canola oil transload facility with key parameters:
- 1,000,000 MT/a throughput (decomposition Project Overview)
- 45,000 MT storage in 3 tanks (decomposition Project Overview)
- 32 railcar unloading stations (decomposition Project Overview)
- Storm drainage for tank farm, railcar unloading area, marine loading platform access
- OWS for spill containment and environmental protection
- Duct banks for electrical/communications infrastructure
- Trenchless crossings for rail tracks and existing utilities

**Trigger:** Allowance amounts required for Detail.csv line items; no vendor quotes or quantities available.

**Evidence:**
- Decomposition Section 1.1 Project Overview provides key parameters
- PKG-03 scope description: "Storm drainage, containment water collection, oil-water separator, underground utility routing, trenchless crossing, outfalls"
- Typical underground utilities scope for industrial facility includes:
  - Storm drainage network (several hundred to 1000+ LM of pipe depending on site area)
  - OWS unit (typically 1-2 units for industrial facility of this scale)
  - Duct banks (several hundred LM of conduit for electrical/comms)
  - Trenchless crossings (5-10 crossings for rail/road/existing utility conflicts)

**Impacted WBS/CBS:** MAT, CD buckets (materials and construction allowances)

**Estimate Impact:** Allowance amounts sized to order-of-magnitude for budgeting purposes; confidence LOW pending design quantities

**Override Path:** Provide design quantities from DEL-03.01 drawings and calculations from DEL-03.03 to replace allowances with volume-based estimates

---

### D-012: Engineering Allowance Sizing for PKG-03

**Decision:** Size engineering allowance based on typical engineering effort for underground utilities package with 6 deliverables (4 design deliverables + 2 record deliverables).

**Trigger:** Engineering cost required for E bucket; no labor hours or rates available.

**Evidence:**
- PKG-03 has 6 deliverables: 1 drawing set, 1 specification, 1 calculation package, 1 data sheet package, 1 installation records, 1 CCTV survey report
- Typical engineering effort for underground utilities includes:
  - Civil engineers (senior, intermediate) for design, calculations, specifications
  - CAD technicians for drawing production
  - QA/QC reviewers for interdisciplinary and independent checks
  - Specialist surveyors for CCTV survey
- Comparable package PKG-02 (9 deliverables, earthworks scope) had Engineering = $268,500 CAD (per _LATEST.md)
- PKG-03 has fewer deliverables (6 vs 9) but includes specialist CCTV survey and OWS environmental engineering

**Impacted WBS/CBS:** E bucket (Engineering)

**Estimate Impact:** Engineering allowance sized based on deliverable count and scope complexity

**Override Path:** Provide engineering labor hours breakdown by discipline and deliverable to enable hour-based engineering estimate

---
