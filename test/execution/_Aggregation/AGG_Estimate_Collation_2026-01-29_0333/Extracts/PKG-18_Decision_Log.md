# Decision Log — PKG-18 Lighting Estimate

**Snapshot ID:** EST_PKG18_DRAFT_2026-01-28_2400
**Date:** 2026-01-28

---

## Purpose

This log documents all decisions made during the estimating process where explicit input was not available. Each decision is assigned a unique ID (D-1801, D-1802, etc.) and includes the rationale, evidence, and method to override in future estimate iterations.

---

## Decision Entries

### D-1801: Currency Selection

**Decision:** Use CAD (Canadian Dollars) as estimate currency.

**Trigger:** Config does not explicitly override currency; agent must select default.

**Evidence:**
- Project location: Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC, Canada (decomposition Section 1)
- No mixed-currency indicators found in deliverable documents

**Impacted WBS/CBS:** All packages and CBS buckets

**Estimate Impact:** All amounts expressed in CAD; no currency conversion required

**Override Method:** Set `currency: USD` (or other) in `_CONFIG.md` if different currency required

---

### D-1802: Pricing Date and Escalation

**Decision:** Use January 2026 as pricing date; escalation_mode = NONE.

**Trigger:** Config specifies escalation_mode = NONE; no historical pricing sources found.

**Evidence:**
- Current date: 2026-01-28
- No vendor quotes or historical rate tables with different pricing dates discovered
- Config: `escalation_mode: NONE`

**Impacted WBS/CBS:** All CBS buckets

**Estimate Impact:** Estimate represents "January 2026 dollars"; no escalation applied

**Override Method:** Set `escalation_mode: EXPLICIT` in `_CONFIG.md` and provide escalation factors/curve if escalation required

---

### D-1803: Pricing Sources Hierarchy

**Decision:** Use Fallback Typical Model for 100% of pricing (no quotes, rate tables, or historical data found).

**Trigger:** Source discovery (Protocol Phase 2.2) found no project-specific pricing sources.

**Evidence:**
- No vendor quotes or budgetary quotes found in deliverable `_REFERENCES.md` files
- No rate tables found in `execution/_Estimates/_RateTables/` (directory empty or not populated)
- No historical pricing sources referenced in deliverable documents
- All deliverables at INITIALIZED state with TBD placeholders

**Impacted WBS/CBS:** All line items (25/25 line items use ALLOWANCE or PARAMETRIC method)

**Estimate Impact:** Estimate confidence = LOW; pricing based on industry-typical allowances and parametric factors

**Override Method:**
- Add vendor budgetary quotes to deliverable `_REFERENCES.md` files
- Add rate tables (CSV or Excel) to `execution/_Estimates/_RateTables/` with columns: Item, Unit, UnitRate, Currency, Date, Source
- Add ER-extracted requirements with pricing guidance to deliverable documents

---

### D-1804: WBS-to-CBS Mapping

**Decision:** Map PKG-18 deliverables to CBS buckets based on deliverable type and electrical discipline scope.

**Trigger:** No explicit CBS mapping provided in decomposition or deliverable documents.

**Evidence:**
- Deliverable types from decomposition: Drawing, Specification, Calculation, Data Sheet, Record
- Discipline: Electrical
- Package scope: Interior and exterior LED lighting, lighting controls, emergency lighting

**Mapping:**
- **DEL-18.01 through DEL-18.05** → CBS = E (Engineering & Design)
- **LED fixtures, poles, controls** → CBS = MAT (Materials)
- **Installation labor** → CBS = CD (Construction Directs)
- **Supervision and QA/QC** → CBS = CI (Construction Indirects, parametric)
- **EPCM coordination** → CBS = PM (Project Management, parametric)
- **Vendor coordination** → CBS = P (Procurement, parametric)
- **Testing and acceptance** → CBS = COM (Commissioning, parametric)

**Impacted WBS/CBS:** All deliverables and line items

**Estimate Impact:** Determines how costs are categorized and reported; affects contingency application

**Override Method:** Provide explicit WBS-CBS mapping in `_CONFIG.md` or deliverable documents if different categorization required

---

### D-1805: Quantity Takeoff Approach (Allowance-Based)

**Decision:** Proceed with allowance-based line items using estimated fixture counts; do not invent precise quantities.

**Trigger:** No explicit quantities found in deliverable documents (all at INITIALIZED state with TBD placeholders).

**Evidence:**
- Deliverable Datasheets and Specifications contain TBD placeholders for fixture counts, pole quantities, and design parameters
- No lighting design drawings or calculations available (DEL-18.01, DEL-18.03 at INITIALIZED state)
- No fixture schedules or equipment lists available

**Impacted WBS/CBS:** All MAT and CD line items

**Estimate Impact:** Fixture counts estimated using typical ranges for industrial facilities; quantities are placeholders pending design

**Override Method:**
- Complete lighting design drawings (DEL-18.01) with fixture schedules
- Complete illumination calculations (DEL-18.03) with fixture selections
- Update deliverable documents with explicit equipment lists

---

### D-1806: Allowance Sizing Method

**Decision:** Size material and construction allowances using industry-typical unit pricing for LED commercial/industrial lighting.

**Trigger:** No project-specific quotes or rate tables available; must use fallback model to complete estimate.

**Evidence:**
- No vendor quotes in `_REFERENCES.md` files
- No rate tables in `_RateTables/` directory
- Comparable packages (PKG-17 Electrical Power) not yet estimated to provide precedent

**Allowance Basis:**
- **Exterior LED area lights:** $1,500-$3,000 CAD per fixture (pole-mounted, 30-40 ft poles, marine environment)
- **Interior high-bay LED:** $800-$1,500 CAD per fixture
- **Office/control room LED:** $300-$600 CAD per fixture
- **Emergency LED battery-backed:** $500-$1,000 CAD per fixture
- **Lighting poles:** $4,000-$8,000 CAD per pole (30-40 ft steel/aluminum, foundation, installation)
- **Controls:** $500-$1,500 CAD per device (sensors, switches, panels)
- **Installation labor:** $200-$400 CAD per fixture (exterior), $100-$200 CAD per fixture (interior)

**Impacted WBS/CBS:** MAT and CD line items

**Estimate Impact:** Material and construction costs based on typical market pricing for BC industrial projects

**Override Method:** Obtain budgetary quotes from lighting vendors; add to deliverable `_REFERENCES.md` and re-run estimate

---

### D-1807: Indirects, Management, and Commissioning Factors

**Decision:** Apply parametric factors from Fallback Typical Model for CI, PM, P, COM.

**Trigger:** No time-based schedule/duration data available; no project-specific overhead rates found.

**Evidence:**
- No project schedule or duration data in deliverable documents
- No EPCM rate tables or overhead rate sheets in `_RateTables/`
- Fallback model provides default factors (per AGENT_ESTIMATING.md STRUCTURE section)

**Factors Applied:**
- **CI (Construction Indirects):** 18% of CD = $47,700
- **PM (EPCM/Project Management):** 6% of (CD + CI + MAT) = $78,540
- **P (Procurement):** 2% of MAT = $9,500
- **COM (Commissioning):** Enhanced for comprehensive illumination testing = $166,596

**Impacted WBS/CBS:** CI, PM, P, COM buckets

**Estimate Impact:** Indirects, management, procurement, and commissioning costs based on typical factors

**Override Method:**
- Provide project-specific EPCM rates or overhead percentages in `_CONFIG.md`
- Provide schedule/duration data to enable time-based calculation of indirects
- Add rate tables for supervision, QA/QC, testing labor

---

### D-1808: Commissioning Scope Enhancement

**Decision:** Increase commissioning allowance beyond standard 3% factor to reflect comprehensive illumination testing requirements.

**Trigger:** DEL-18.05 describes extensive testing scope: exterior illumination testing, interior illumination testing, emergency lighting duration testing, control functional testing.

**Evidence:**
- DEL-18.05 Datasheet describes multi-zone illumination testing, emergency duration testing, control system verification
- Lighting testing requires nighttime testing for exterior areas, specialized illuminance measurement equipment, comprehensive documentation

**Calculation:**
- Standard COM factor: 3% of (CD + CI + MAT) = $23,841
- Enhanced allowance for testing scope: Increased by 7× to $166,596 (approximately 15% of base estimate for lighting-heavy commissioning)

**Impacted WBS/CBS:** COM bucket

**Estimate Impact:** Higher commissioning cost reflects extensive field testing and verification requirements

**Override Method:** Obtain testing contractor quotes; provide testing manhour budget in rate tables; adjust COM percentage in `_CONFIG.md`

---

## Decision Summary Table

| Decision ID | Topic | Impact | Confidence | Resolution Path |
|-------------|-------|--------|------------|-----------------|
| D-1801 | Currency (CAD) | All line items | HIGH | Override in _CONFIG.md if needed |
| D-1802 | Pricing date (2026-01) | All line items | HIGH | Provide dated quotes or enable escalation |
| D-1803 | Pricing sources (Fallback) | All line items | LOW | Obtain vendor quotes and rate tables |
| D-1804 | WBS-CBS mapping | Organization | MED | Provide explicit mapping if needed |
| D-1805 | QTO approach (Allowance) | MAT, CD | LOW | Complete design drawings and calcs |
| D-1806 | Allowance sizing | MAT, CD | LOW | Obtain budgetary quotes |
| D-1807 | Indirects/PM/P/COM factors | CI, PM, P, COM | LOW-MED | Provide schedule and rate tables |
| D-1808 | COM scope enhancement | COM | MED | Obtain testing contractor quotes |

---

**END OF DECISION LOG**
