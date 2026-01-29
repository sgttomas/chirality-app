# Decision Log

## Snapshot Identification

| Field | Value |
|-------|-------|
| Snapshot ID | EST_PKG23_DRAFT_2026-01-28_2400 |
| Package | PKG-23 Fire Protection |
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

**Decision:** Use `PKG23_DRAFT` as estimate label.

**Trigger:** Estimate label required for snapshot identification and tracking.

**Evidence:**
- Following established pattern from previous packages (PKG00_DRAFT through PKG20_DRAFT per _LATEST.md)
- Package-specific labels per snapshot convention

**Impacted WBS/CBS:** N/A (metadata only)

**Estimate Impact:** None (label is for identification only)

**Override Path:** Provide different label via config or user instruction for next run

---

### D-004: Scope Inclusions

**Decision:** Include Engineering (E), PM, Procurement (P), Materials (MAT), Construction Directs (CD), Construction Indirects (CI), Commissioning (COM).

**Trigger:** CBS scope definition required for estimate coverage.

**Evidence:**
- Config file specifies include scopes list
- PKG-23 scope includes design deliverables (engineering), fire protection equipment (procurement, materials), installation (construction), testing (commissioning) per decomposition

**Impacted WBS/CBS:** All CBS buckets except excluded scopes

**Estimate Impact:** Estimate includes full EPC coverage for contractor scope

**Override Path:** Modify `_CONFIG.md` include_scopes/exclude_scopes if different coverage is required

---

### D-005: Scope Exclusions

**Decision:** Exclude Owner's costs, land acquisition, financing costs, permits obtained by Employer, building sprinkler systems (PKG-22 scope).

**Trigger:** Exclusions required for estimate boundary definition.

**Evidence:**
- Config file specifies exclude scopes
- Decomposition Section 1.2 Scope Focus confirms "Contractor's scope of work only"
- Building fire suppression systems allocated to PKG-22 Building Interior & MEP per decomposition

**Impacted WBS/CBS:** N/A (exclusions)

**Estimate Impact:** Building sprinkler systems not costed in PKG-23; allocated to PKG-22

**Override Path:** Review decomposition if scope boundary changes

---

### D-006: Rounding Policy

**Decision:** Round to nearest $1,000 CAD.

**Trigger:** Rounding policy required per config.

**Evidence:**
- Config file specifies `rounding: 1000`

**Impacted WBS/CBS:** All summary totals

**Estimate Impact:** Summary totals rounded; Detail.csv retains calculated precision

**Override Path:** Modify `_CONFIG.md` rounding if different precision required

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
- DEL-23.03 fire water demand calculations not complete
- Fallback typical model permits allowance-based pricing when sources are not available (AGENT_ESTIMATING.md STRUCTURE section "Placeholder allowance policy")

**Impacted WBS/CBS:** All CBS buckets (Engineering, Materials, Construction Directs, Construction Indirects, PM, Procurement, Commissioning)

**Estimate Impact:** All line items are lump-sum allowances (Qty=1, Unit=LS, UnitRate=Amount); estimate confidence is LOW

**Override Path:** Provide design quantities from DEL-23.01 drawings and DEL-23.03 calculations; obtain vendor quotes for fire protection equipment

---

### D-009: Indirects Model Selection

**Decision:** Use factor-based indirects model (fallback typical model).

**Trigger:** No schedule/duration data available; indirects model required for CI, PM, P, COM pricing.

**Evidence:**
- No schedule or duration data discovered in deliverables
- Fallback typical model (AGENT_ESTIMATING.md STRUCTURE section "Default factors") defines factor-based indirects:
  - Construction Indirects (CI) = 0.18 × Construction Directs (CD)
  - Procurement Services (P) = 0.02 × (MAT)
  - EPCM/PM = 0.06 × (CD + CI + MAT)
  - Commissioning (COM) = 0.03 × (CD + CI + MAT)

**Impacted WBS/CBS:** CI, PM, P, COM buckets

**Estimate Impact:** Indirects are factor-derived based on directs/materials base costs

**Override Path:** Provide project schedule with durations and resource loading to enable time-based indirects pricing

---

### D-010: WBS → CBS Mapping for PKG-23 Deliverables

**Decision:** Map PKG-23 deliverables to CBS buckets as follows:
- DEL-23.01, 23.02, 23.03, 23.04 → Engineering (E)
- DEL-23.05 → Construction Indirects (CI) for QA/QC records capture
- Fire protection equipment (hydrants, FACP, detectors, foam equipment) → Materials (MAT)
- Installation work (fire water loop, hydrants, fire alarm, foam systems) → Construction Directs (CD)

**Trigger:** WBS → CBS mapping required for cost categorization.

**Evidence:**
- DEL-23.01 through DEL-23.04 are design deliverables (Drawing, Specification, Calculation, Data Sheet) → Engineering discipline
- DEL-23.05 is QA/QC records → Construction Indirects
- PKG-23 scope includes fire protection equipment → Materials bucket
- PKG-23 scope includes installation → Construction Directs
- Testing and commissioning (hydrostatic, flow, fire alarm, foam testing) → included in Commissioning bucket via indirects factor

**Impacted WBS/CBS:** All PKG-23 deliverables mapped to E, MAT, CD, CI buckets

**Estimate Impact:** Cost distribution across CBS buckets reflects engineering-heavy (design) + materials/construction (installation) mix

**Override Path:** Review mapping if deliverable types or CBS bucket definitions change

---

### D-011: Fire Pump Exclusion

**Decision:** Exclude fire pump from PKG-23 estimate; assume municipal fire water supply provides adequate pressure.

**Trigger:** Fire pump requirement not confirmed; need to determine if dedicated fire pump is required.

**Evidence:**
- No fire water demand calculation available (DEL-23.03 INITIALIZED)
- No hydraulic analysis available to confirm supply pressure adequacy
- Municipal fire water supply often adequate for industrial facilities in urban areas
- Fire pump may be required if supply pressure is insufficient or if insurance/AHJ requires dedicated pump

**Impacted WBS/CBS:** MAT, CD, CI, COM (fire pump would add $150k-300k to estimate)

**Estimate Impact:** Fire pump cost excluded; estimate may be understated if fire pump required

**Override Path:** Complete DEL-23.03 hydraulic calculations; confirm municipal supply pressure; add fire pump scope if required

---

### D-012: Foam System Inclusion

**Decision:** Include tank foam suppression system for all 3 × 15,000 MT tanks and marine loading foam system in PKG-23 scope.

**Trigger:** Foam system requirement for combustible liquid storage facilities per NFPA 30.

**Evidence:**
- Product is CSD canola oil, Class IIIA combustible liquid per NFPA 30 (flash point >93°C)
- NFPA 30 requires foam suppression for combustible liquid storage tanks above certain thresholds
- DEL-23.01 anticipated artifacts include foam system layout
- DEL-23.02 anticipated artifacts include foam system specification

**Impacted WBS/CBS:** MAT ($425k foam equipment), CD ($150k foam installation)

**Estimate Impact:** Foam system is significant cost driver (~$575k or 27% of base estimate)

**Override Path:** Confirm foam system requirements per NFPA 30 and insurance/AHJ; adjust foam system scope if alternative fire protection approach approved

---
