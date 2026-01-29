# Decision Log — PKG-15 Pumps & Rotating Equipment Estimate

**Snapshot ID:** EST_PKG15_DRAFT_2026-01-28_2345
**Package:** PKG-15 Pumps & Rotating Equipment
**Estimate Date:** 2026-01-28
**Currency:** CAD
**Pricing Date:** 2026-01

---

## Decision Entries

### D-001: Workspace Paths and Inputs Discovery
**Decision:** Used default workspace paths from Project Instance Paths.
**Trigger:** Standard initialization; no explicit paths provided by human.
**Evidence:**
- Execution root: `/Users/ryan/ai-env/projects/chirality-app/test/execution/`
- Decomposition: `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`
- Estimates output: `/Users/ryan/ai-env/projects/chirality-app/test/execution/_Estimates/`

**Impact:** Standard paths; no estimate impact.
**How to override:** Provide explicit paths in conversation.

---

### D-002: Currency Selection
**Decision:** Use CAD (Canadian Dollars) as estimate currency.
**Trigger:** Project location in Surrey, BC, Canada; existing _CONFIG.md specifies CAD.
**Evidence:**
- _CONFIG.md line 9: `currency | CAD | Canadian dollars (project location: Surrey, BC)`
- Project location: Fraser Surrey Terminal, Surrey, BC

**Impact:** All costs in CAD; no currency conversion required.
**How to override:** Update _CONFIG.md currency parameter.

---

### D-003: Pricing Date
**Decision:** Use 2026-01 (January 2026) as pricing date.
**Trigger:** Current date is 2026-01-28; _CONFIG.md specifies 2026-01.
**Evidence:**
- _CONFIG.md line 10: `pricing_date | 2026-01 | January 2026 (current date)`
- Current pricing environment

**Impact:** Costs reflect January 2026 pricing (no escalation applied).
**How to override:** Update _CONFIG.md pricing_date parameter.

---

### D-004: Estimate Label
**Decision:** Use estimate label "PKG15_DRAFT"
**Trigger:** Package-specific estimate following established phased approach.
**Evidence:** _CONFIG.md pattern of package-by-package estimates; PKG-00 through PKG-13 completed.

**Impact:** Snapshot labeled as draft estimate for PKG-15.
**How to override:** Update estimate_label in conversation or config.

---

### D-005: Pump Quantities - Parametric Allowance Approach
**Decision:** Use parametric allowances for pump quantities since deliverables show "TBD" for all pump counts.
**Trigger:** Deliverable documents (DEL-15.02, DEL-15.04) list all pump quantities as "TBD" pending DEL-15.03 calculations.
**Evidence:**
- DEL-15.04 Datasheet line 36: "Quantity | **TBD** — One data sheet per pump unit"
- DEL-15.02 Specification lines 27-32: All pump service quantities shown as "**TBD**"
- Exploration agent confirmed: "most pump quantities and capacities marked as TBD"

**Estimated quantities (for budgeting):**
- Railcar unloading transfer pumps: 4 units (2 duty + 2 standby, supporting 32 railcar stations and 1M MT/annum throughput)
- Marine loading pumps: 2 units (1 duty + 1 standby)
- Tank transfer pumps: 2 units (for 3 x 15,000 MT tanks)
- Sump pumps: 6 units (railcar area, marine loading area, tank farm containment)
- **Total: 14 pump units**

**Impacted WBS/CBS:** All PKG-15 deliverables; Materials (MAT), Construction Directs (CD)
**Estimate Impact:** HIGH - pump quantities directly affect equipment cost and installation hours.
**How to override:** Provide finalized pump quantities from DEL-15.03 calculations or ER Part 2.

**Related Assumptions:** A-001, A-002, A-003, A-004

---

### D-006: Pump Sizing and Power Ratings
**Decision:** Use typical sizing ranges for process facility pumps in canola oil service.
**Trigger:** Specific pump capacities and motor power ratings listed as "TBD" in deliverables.
**Evidence:**
- DEL-15.02 lines 76-88: All performance data (flow, head, power) shown as "TBD"
- Facility throughput requirement: 1,000,000 MT/annum
- 32 railcar stations, 3 storage tanks, marine loading capacity

**Estimated sizing:**
- Railcar unloading pumps: 200 m³/hr @ 50m head, 30 kW motors (estimate based on throughput requirements)
- Marine loading pumps: 400 m³/hr @ 40m head, 50 kW motors
- Tank transfer pumps: 150 m³/hr @ 30m head, 15 kW motors
- Sump pumps: 25 m³/hr @ 15m head, 3 kW motors

**Impacted WBS/CBS:** DEL-15.01 through DEL-15.05; Materials (MAT), Electrical (E)
**Estimate Impact:** MEDIUM - affects equipment cost and electrical load.
**How to override:** Provide finalized pump sizing from DEL-15.03 or vendor data.

**Related Assumptions:** A-002, A-005

---

### D-007: API 610 Pump Specification
**Decision:** Assume API 610 centrifugal pumps for all process services; standard industrial pumps for sump service.
**Trigger:** DEL-15.02 specifies API 610 as primary standard; typical for process industry.
**Evidence:**
- DEL-15.02 line 187: "**API 610** (latest edition) — Centrifugal Pumps for Petroleum, Petrochemical and Natural Gas Industries"
- Line 134: "Horizontal or vertical centrifugal pump per API 610"

**Impact:** API 610 compliance increases equipment cost vs. commercial pumps (typically 1.5-2.0× cost multiplier).
**Impacted WBS/CBS:** Materials (MAT)
**Estimate Impact:** MEDIUM - affects unit costs
**How to override:** Confirm API 610 requirement or allow commercial pumps per ER Part 2.

**Related Assumptions:** A-002

---

### D-008: Materials of Construction
**Decision:** Carbon steel/cast iron casings with stainless steel wetted parts for food-grade canola oil service.
**Trigger:** DEL-15.02 identifies canola oil as food-grade product; materials must be food-compatible.
**Evidence:**
- DEL-15.02 line 128: "Canola oil is a food-grade product. Materials in contact with product should be compatible with food-grade service"
- Line 118: Material options include cast iron, ductile iron, carbon steel, stainless steel

**Assumed materials:**
- Casings: Cast iron or carbon steel
- Impellers/wetted parts: 316 stainless steel
- Seal faces: Silicon carbide
- Baseplates: Structural steel

**Impacted WBS/CBS:** Materials (MAT)
**Estimate Impact:** LOW - typical materials for vegetable oil service.
**How to override:** Provide specific material requirements from ER Part 2 or vendor recommendations.

**Related Assumptions:** A-002

---

### D-009: Engineering Effort Distribution
**Decision:** Allocate engineering hours across 5 deliverables using complexity weighting.
**Trigger:** No explicit engineering hours provided in deliverables.
**Evidence:** Standard EPC practice; similar packages (PKG-00, PKG-11) used parametric approach.

**Distribution:**
- DEL-15.01 Design Drawings: 40% (arrangement, foundation interface most complex)
- DEL-15.02 Specification: 25% (procurement specification development)
- DEL-15.03 Calculations: 20% (sizing, NPSH, system curves)
- DEL-15.04 Data Sheets: 10% (vendor data review and approval)
- DEL-15.05 Test Records: 5% (commissioning support and documentation)

**Impacted WBS/CBS:** Engineering (E)
**Estimate Impact:** LOW - distribution methodology, not absolute value.
**How to override:** Provide detailed engineering hour estimates by deliverable.

---

### D-010: Indirects and Management Factors
**Decision:** Apply fallback typical model factors for indirects and project management.
**Trigger:** No project-specific indirects or PM rates found in rate tables or source documents.
**Evidence:** No rate tables in `/Users/ryan/ai-env/projects/chirality-app/test/execution/_Estimates/_RateTables/`

**Factors applied (from AGENT_ESTIMATING.md fallback model):**
- Construction Indirects (CI): 18% of Construction Directs (CD)
- Procurement Services (P): 2% of (MAT + FRT)
- EPCM/PM: 6% of (CD + CI + MAT)
- Commissioning (COM): 3% of (CD + CI + MAT)

**Impacted WBS/CBS:** CI, P, PM, COM buckets
**Estimate Impact:** MEDIUM - affects total project cost by ~25-30%.
**How to override:** Provide project-specific rates in _RateTables/ or update _CONFIG.md.

**Related Assumptions:** A-006, A-007, A-008

---

### D-011: Contingency Method
**Decision:** Use PCT_BY_BUCKET method with allowance-heavy adjustments.
**Trigger:** _CONFIG.md specifies PCT_BY_BUCKET; estimate has high allowance content due to TBD quantities.
**Evidence:**
- _CONFIG.md line 35: `contingency_method | PCT_BY_BUCKET`
- High TBD content increases uncertainty

**Baseline contingency by CBS:**
- Engineering (E): 10%
- Project Management (PM): 10%
- Procurement (P): 10%
- Materials (MAT): 15% + allowance adjustment
- Construction Directs (CD): 20% + allowance adjustment
- Construction Indirects (CI): 20%
- Commissioning (COM): 25%

**Allowance adjustments:**
- If bucket allowance share ≥ 50%: +5%
- If bucket allowance share ≥ 80%: additional +5% (total +10%)

**Impacted WBS/CBS:** All CBS buckets
**Estimate Impact:** HIGH - contingency 20-30% of base cost expected given TBD quantities.
**How to override:** Switch to RISK_BASED method in _CONFIG.md or provide better quantity data.

---

### D-012: Rounding Policy
**Decision:** Round to nearest $1,000 CAD.
**Trigger:** _CONFIG.md specifies rounding = 1000.
**Evidence:** _CONFIG.md line 12: `rounding | 1000 | Round to nearest $1,000`

**Impact:** All summary values rounded to $1,000.
**How to override:** Update _CONFIG.md rounding parameter.

---

### D-013: Escalation Mode
**Decision:** No escalation applied (current dollars).
**Trigger:** _CONFIG.md specifies escalation_mode = NONE.
**Evidence:** _CONFIG.md line 36: `escalation_mode | NONE | No escalation (current pricing)`

**Impact:** Estimate is in January 2026 dollars; no time-phased escalation.
**How to override:** Set escalation_mode = EXPLICIT in _CONFIG.md.

---

### D-014: Installation Labor Productivity
**Decision:** Use standard industrial rates for BC coastal location with skilled trades.
**Trigger:** No project-specific productivity data provided.
**Evidence:** Project location (Fraser Surrey Terminal, Surrey, BC); industrial terminal setting.

**Assumed productivity:**
- Pump setting and alignment: 24 manhours per pump unit (medium-size process pumps)
- Piping connections: included in PKG-14 (Process Piping)
- Electrical connections: included in PKG-17/19 (Electrical)
- Testing and commissioning: 16 manhours per pump unit

**Labor rate:** $95/hr loaded (BC prevailing industrial rate including benefits, burden)

**Impacted WBS/CBS:** Construction Directs (CD)
**Estimate Impact:** MEDIUM
**How to override:** Provide project-specific labor rates and productivity factors.

**Related Assumptions:** A-003

---

### D-015: Commissioning Scope
**Decision:** Commissioning includes FAT witness, installation supervision, performance testing, and documentation.
**Trigger:** DEL-15.05 scope; standard for critical rotating equipment.
**Evidence:** DEL-15.05 anticipated artifacts include FAT records, performance test records, vibration analysis.

**Assumed commissioning effort:**
- FAT witness (vendor shop): 8 hours per major pump (included in travel allowance)
- Installation supervision: included in Construction Indirects
- Performance testing: 16 manhours per pump
- Vibration analysis: 4 manhours per pump
- Documentation: 8 manhours per pump

**Impacted WBS/CBS:** Commissioning (COM)
**Estimate Impact:** LOW - commissioning 3-5% of total.
**How to override:** Provide detailed commissioning plan from DEL-15.05.

**Related Assumptions:** A-009

---

## Summary

**Total Decisions:** 15
**High Impact:** 2 (D-005 pump quantities, D-011 contingency)
**Medium Impact:** 5
**Low Impact:** 8

**Key Uncertainties:**
1. Pump quantities (TBD in all deliverables → parametric allowance used)
2. Pump sizing and power ratings (TBD → typical values assumed)
3. No vendor quotes available (all equipment priced parametrically)
4. Installation labor productivity assumptions

**Next Run Improvements:**
- Finalize pump quantities from DEL-15.03 calculations
- Obtain vendor budgetary quotes for API 610 pumps
- Confirm engineering hours by deliverable
- Validate labor rates and productivity for BC location
