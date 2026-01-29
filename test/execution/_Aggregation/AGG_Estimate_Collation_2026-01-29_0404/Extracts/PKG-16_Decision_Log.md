# Decision Log — PKG-16 Valves & Specialty Equipment

**Snapshot ID:** EST_PKG16_DRAFT_2026-01-28_2347
**Package:** PKG-16 Valves & Specialty Equipment
**Date:** 2026-01-28

---

## Purpose

This log records all decisions made during the estimating process where ambiguities, missing inputs, or defaults required agent selection of a runnable path forward.

Each decision is traceable to its trigger, evidence (or lack thereof), impacted scope, and override path for the next iteration.

---

## Decision Entries

### D-1601: Workspace Paths (Auto-Discovery)

**Decision:** Use default project paths as defined in AGENT_ESTIMATING.md

**Trigger:** No explicit paths provided by human; using defaults

**Evidence:**
- Execution root: `/Users/ryan/ai-env/projects/chirality-app/test/execution/` (exists, verified)
- Decomposition: `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` (exists, verified)
- Estimates output: `/Users/ryan/ai-env/projects/chirality-app/test/execution/_Estimates/` (exists, verified)

**Impacted WBS/CBS:** All

**Estimate Impact:** None (paths valid)

**Override:** N/A (paths are correct)

---

### D-1602: Currency Selection

**Decision:** Use **CAD** (Canadian dollars) as estimate currency

**Trigger:** Config file specifies CAD; project location in Surrey, BC, Canada

**Evidence:**
- `_CONFIG.md` line 9: `currency | CAD | Canadian dollars (project location: Surrey, BC)`
- Project location: Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC
- All prior package estimates (PKG-00 through PKG-14) used CAD

**Impacted WBS/CBS:** All

**Estimate Impact:** All amounts in CAD; no currency conversion required

**Override:** Update `_CONFIG.md` if different currency desired

---

### D-1603: Pricing Date

**Decision:** Use **January 2026** (2026-01) as pricing date

**Trigger:** Config file specifies 2026-01; current date is 2026-01-28

**Evidence:**
- `_CONFIG.md` line 10: `pricing_date | 2026-01 | January 2026 (current date)`
- Current date: 2026-01-28

**Impacted WBS/CBS:** All

**Estimate Impact:** Prices represent January 2026 dollars; no escalation applied (per D-1609)

**Override:** Update `_CONFIG.md` if different pricing date desired

---

### D-1604: Estimate Label

**Decision:** Use **PKG16_DRAFT** as estimate label

**Trigger:** Following established pattern from prior packages

**Evidence:**
- Prior estimates: PKG00_DRAFT, PKG01_DRAFT, PKG03_DRAFT, PKG04_DRAFT, etc.
- This is conceptual/budgeting estimate (no design quantities or vendor quotes)

**Impacted WBS/CBS:** N/A (label only)

**Estimate Impact:** Snapshot ID = EST_PKG16_DRAFT_2026-01-28_2347

**Override:** Provide alternate label in conversation or `_CONFIG.md`

---

### D-1605: Rounding Policy

**Decision:** Round summary totals to nearest **$1,000 CAD**

**Trigger:** Config file specifies rounding = 1000

**Evidence:**
- `_CONFIG.md` line 12: `rounding | 1000 | Round to nearest $1,000`
- Consistent with all prior package estimates

**Impacted WBS/CBS:** Summary only (Detail.csv retains calculated precision)

**Estimate Impact:** Summary totals rounded to nearest $1k; Detail.csv unrounded

**Override:** Update `_CONFIG.md` if different rounding desired

---

### D-1606: Scope Inclusions/Exclusions

**Decision:** Include Engineering, PM, Procurement, Materials, Construction Directs/Indirects, Commissioning; exclude Owner's costs, land, financing, permits

**Trigger:** Config file specifies include/exclude scopes

**Evidence:**
- `_CONFIG.md` lines 16-30: Include scopes E, PM, P, MAT, CD, CI, COM; exclude Owner's costs, land, financing, permits
- Consistent with EPC/Design-Build scope boundary
- Decomposition Section 1.2 (Scope Focus) — Contractor responsible for design, procurement, construction, commissioning

**Impacted WBS/CBS:** All CBS buckets

**Estimate Impact:** Full EPC scope coverage; Owner-supplied items excluded

**Override:** Update `_CONFIG.md` include/exclude lists if scope boundary changes

---

### D-1607: Contingency Method

**Decision:** Use **PCT_BY_BUCKET** with allowance-heavy adjustments

**Trigger:** Config file specifies contingency_method = PCT_BY_BUCKET

**Evidence:**
- `_CONFIG.md` line 35: `contingency_method | PCT_BY_BUCKET | Apply contingency % by CBS bucket`
- AGENT_ESTIMATING fallback model (lines 676-689): baseline contingency + allowance-heavy adjustment

**Impacted WBS/CBS:** All CBS buckets (contingency line)

**Estimate Impact:** Contingency rates 15-30% by CBS bucket depending on allowance share

**Override:** Update `_CONFIG.md` to `RISK_BASED` if three-point estimate desired; provide risk model inputs

---

### D-1608: Indirects Model

**Decision:** Use **factor-based** indirects (CI, P, PM, COM)

**Trigger:** No construction schedule or duration data available

**Evidence:**
- No schedule available in workspace
- AGENT_ESTIMATING protocol (lines 307-320): "factor-based model (default) using the fallback typical model" when schedule unavailable
- Factors: CI=18%, P=2%, PM=6%, COM=3% (AGENT_ESTIMATING lines 666-673)

**Impacted WBS/CBS:** CI, P, PM, COM

**Estimate Impact:**
- CI = 0.18 × CD
- P = 0.02 × MAT
- PM = 0.06 × (CD + CI + MAT)
- COM = 0.03 × (CD + CI + MAT)

**Override:** Provide construction schedule and duration data to enable time-based indirects model

---

### D-1609: Escalation Mode

**Decision:** Use **NONE** (no escalation)

**Trigger:** Config file specifies escalation_mode = NONE

**Evidence:**
- `_CONFIG.md` line 36: `escalation_mode | NONE | No escalation (current pricing)`
- No schedule available for cashflow curve
- January 2026 pricing basis (current)

**Impacted WBS/CBS:** N/A (no escalation line)

**Estimate Impact:** Estimate in current January 2026 dollars; escalation exposure noted in Risk Register

**Override:** Update `_CONFIG.md` to `EXPLICIT` and provide schedule/cashflow data if escalation calculation desired

---

### D-1610: WBS to CBS Mapping

**Decision:** Map PKG-16 deliverables to CBS buckets per deliverable type

**Trigger:** Deliverables span multiple CBS categories (engineering, materials, construction)

**Evidence:**
- DEL-16.01 (drawings) → Engineering (E)
- DEL-16.02 (specifications) → Engineering (E)
- DEL-16.03 (calculations) → Engineering (E)
- DEL-16.04 (datasheets) → Engineering (E)
- DEL-16.05 (test records) → Construction Indirects (CI) and Commissioning (COM)
- Valve equipment → Materials (MAT)
- Valve installation → Construction Directs (CD)

**Impacted WBS/CBS:** All deliverables

**Estimate Impact:** Engineering costs allocated to E; materials to MAT; installation to CD; testing/commissioning to CI/COM

**Override:** N/A (mapping follows deliverable type convention)

---

### D-1611: Valve Quantity Estimation Basis

**Decision:** Estimate valve quantities using **parametric approach** based on facility type and system complexity

**Trigger:** No P&IDs available; no valve lists; no equipment datasheets with valve counts

**Evidence:**
- Deliverable status: All INITIALIZED (no design quantities)
- Facility parameters from decomposition:
  - 32 railcar unloading stations (PKG-10)
  - 3 storage tanks × 15,000 MT each (PKG-13)
  - Marine loading system (PKG-11)
  - Product transfer and metering (PKG-12)
- Typical transload facility valve density (industry experience)

**Impacted WBS/CBS:** MAT, CD (valve quantities drive material and installation costs)

**Estimate Impact:** Valve count estimate:
- Control valves: ~25-35 units (flow, pressure, level control at railcar stations, tanks, loading system)
- Isolation valves: ~120-180 units (manual and automated; line isolation, equipment isolation)
- Relief valves: ~15-25 units (tank relief, pump relief, line thermal relief)
- Strainers: ~15-20 units (pump suction protection, meter protection)
- Total: ~175-260 valves

**Assumption:** A-1601 (valve count parametric)

**Override:** Provide P&IDs with valve counts and service assignments to replace parametric estimate with actual valve list

---

### D-1612: Valve Size Distribution

**Decision:** Estimate valve size distribution using **typical size mix** for transload facility

**Trigger:** No line list available; no pipe sizes defined; no valve datasheets with sizes

**Evidence:**
- Facility type: Canola oil transload with railcar unloading, storage, marine loading
- Typical transload piping: 2" to 12" product lines; 1" to 4" utility/control lines
- Larger isolation valves at tank inlets/outlets (8" to 12")
- Smaller control valves at railcar stations (2" to 4")

**Impacted WBS/CBS:** MAT (valve cost varies significantly with size)

**Estimate Impact:** Size distribution assumption:
- Small (DN50-DN100 / 2"-4"): 60% of valves
- Medium (DN150-DN200 / 6"-8"): 30% of valves
- Large (DN250-DN300 / 10"-12"): 10% of valves

**Assumption:** A-1602 (valve size distribution)

**Override:** Provide piping line list with line sizes to replace size distribution assumption with actual valve sizes

---

### D-1613: Valve Material Selection

**Decision:** Use **stainless steel (316SS)** as baseline for product-contact valves

**Trigger:** Food-grade canola oil service requires cleanable, corrosion-resistant materials

**Evidence:**
- DEL-16.04 Datasheet.md lines 303-314: "Stainless steel (316SS or 304SS) for food-grade cleanliness and corrosion resistance"
- DEL-16.02 Datasheet.md lines 167-176: "Stainless steel (316SS or 304SS) preferred for product-contact materials"
- Coastal marine environment (Fraser Surrey Terminal) requires corrosion-resistant materials
- Food-grade product (canola oil) requires cleanable surfaces

**Impacted WBS/CBS:** MAT (stainless steel valves cost ~2-3× carbon steel)

**Estimate Impact:** Higher material costs vs. carbon steel; lower lifecycle maintenance costs

**Assumption:** A-1603 (material selection)

**Override:** Provide DEL-16.02 specification with actual material selections if different from 316SS baseline

---

### D-1614: Actuator Type Distribution

**Decision:** Estimate actuator distribution as **60% manual, 30% pneumatic, 10% electric**

**Trigger:** No P&IDs with actuation requirements; no control philosophy available

**Evidence:**
- Isolation valves: Typically manual unless ESD or seasonal operation required
- Control valves: Typically pneumatic actuation for modulating control
- Large isolation valves (MOVs): Electric actuation for large sizes (DN200+)
- Typical transload facility actuation mix (industry experience)

**Impacted WBS/CBS:** MAT (actuators add significant cost), CD (automated valves require hookup)

**Estimate Impact:** Actuated valve costs ~3-5× manual valves (actuator + accessories + hookup)

**Assumption:** A-1604 (actuator type distribution)

**Override:** Provide P&IDs with valve actuation requirements or control philosophy document

---

### D-1615: Control Valve Complexity

**Decision:** Estimate control valve complexity as **50% standard globe, 30% ball/butterfly, 20% severe service**

**Trigger:** No valve datasheets with trim types; no sizing calculations available

**Evidence:**
- Standard globe valves: Typical for general flow/pressure control (railcar stations, tank level control)
- Ball/butterfly control valves: Large sizes, on/off with modulation capability
- Severe service: Potential high pressure drop applications (pressure reducing stations)

**Impacted WBS/CBS:** MAT (severe service valves cost ~2-3× standard)

**Estimate Impact:** Weighted average control valve cost reflects complexity mix

**Assumption:** A-1605 (control valve complexity)

**Override:** Provide DEL-16.03 sizing calculations or DEL-16.04 datasheets with valve body styles and trim types

---

### D-1616: Pricing Sources (Fallback Model)

**Decision:** Use **fallback typical model** for all valve pricing (no vendor quotes or rate tables available)

**Trigger:** Source discovery (Source_Index.md) found no vendor quotes or rate tables

**Evidence:**
- Searched `/Users/ryan/ai-env/projects/chirality-app/test/execution/PKG-16_Valves_and_Specialty_Equipment/0_References/` — no vendor quotes
- Searched `/Users/ryan/ai-env/projects/chirality-app/test/execution/_Estimates/_RateTables/` — no rate tables
- All deliverables INITIALIZED status (no design quantities)

**Impacted WBS/CBS:** MAT, CD (all valve material and installation costs)

**Estimate Impact:** 100% allowance-based pricing with LOW confidence; typical market rates for BC/Canada

**Override:** Provide vendor budgetary quotes or populate `_RateTables/` with project-specific valve rates

---

### D-1617: Valve Count Parametric Model

**Decision:** Estimate valve count using **facility-type parametric** approach

**Trigger:** No P&IDs; no valve lists; no equipment datasheets with valve interface counts

**Evidence:**
- 32 railcar unloading stations: ~4-6 valves per station (unloading valve, isolation, drain, sample) → 128-192 valves
- 3 storage tanks: ~10-15 valves per tank (inlet, outlet, relief, drain, gauge, sample) → 30-45 valves
- Marine loading system: ~15-25 valves (loading arm isolation, flow control, relief)
- Product transfer: ~10-15 valves (transfer pumps, meters, manifolds)
- Total range: ~183-277 valves
- Midpoint: ~230 valves

**Impacted WBS/CBS:** MAT (valve count drives material cost), CD (installation cost)

**Estimate Impact:** Parametric valve count = 220 valves (conservative midpoint)
- Control: 30 units (flow, pressure, level control)
- Isolation: 150 units (manual and automated block valves)
- Relief: 20 units (tank, pump, line protection)
- Strainers: 20 units (pump suction, meter protection)

**Assumption:** A-1601 (valve count parametric)

**Override:** Provide P&IDs with actual valve count and service assignments

---

### D-1618: Valve Unit Cost Assumptions

**Decision:** Use **typical BC market rates** for valve pricing (no vendor quotes)

**Trigger:** No vendor quotes or rate tables available

**Evidence:**
- Industry experience: BC/Lower Mainland valve pricing
- Stainless steel valve premium (~2-3× vs. carbon steel)
- Actuator costs: Pneumatic ~$3k-$15k, Electric ~$8k-$40k (size-dependent)
- Control valve positioners: ~$2k-$5k per unit

**Impacted WBS/CBS:** MAT

**Estimate Impact:** Valve allowances sized using typical unit costs:
- Small isolation valve (DN50-100, SS, manual): $800-$2,500 each
- Medium isolation valve (DN150-200, SS, manual): $3,000-$8,000 each
- Large isolation valve (DN250-300, SS, manual): $10,000-$25,000 each
- Control valve (DN50-100, SS, pneumatic, positioner): $8,000-$15,000 each
- Relief valve (API 526, SS): $3,000-$12,000 each (size-dependent)
- Strainer (SS, Y-type or basket): $1,500-$5,000 each

**Assumption:** A-1606 (valve unit costs)

**Override:** Provide vendor budgetary quotes or historical pricing data for BC/Canada market

---

### D-1619: Installation Labor Productivity

**Decision:** Use **typical valve installation productivity** (4-12 hours per valve depending on size and complexity)

**Trigger:** No project-specific installation rates or crew productivity data

**Evidence:**
- Small valves (DN50-100): ~4-6 hours (rigging, bolting, alignment, testing)
- Medium valves (DN150-200): ~8-12 hours
- Large valves (DN250-300): ~16-24 hours
- Actuated valves: +2-4 hours for actuator mounting and hookup
- BC labor rate (all-in with benefits, indirects): ~$85-$110/hr

**Impacted WBS/CBS:** CD

**Estimate Impact:** Installation labor allowances reflect size and actuation complexity

**Assumption:** A-1607 (installation productivity)

**Override:** Provide project labor rate tables and construction management estimate of crew productivity

---

### D-1620: Indirects Factors (CI, P, PM, COM)

**Decision:** Apply factor-based indirects per AGENT_ESTIMATING fallback model

**Trigger:** No construction schedule available; factor-based appropriate for conceptual estimate

**Evidence:**
- AGENT_ESTIMATING lines 666-673: CI=18%, P=2%, PM=6%, COM=3%
- All prior package estimates used same factors
- No schedule or duration data available

**Impacted WBS/CBS:** CI, P, PM, COM

**Estimate Impact:**
- CI = 0.18 × CD (construction supervision, QA/QC, HSE, site overhead)
- P = 0.02 × MAT (procurement, expediting, inspection)
- PM = 0.06 × (CD + CI + MAT) (project management, engineering management, cost/schedule control)
- COM = 0.03 × (CD + CI + MAT) (commissioning, testing per DEL-16.05, handover)

**Override:** Provide construction schedule and duration estimate to enable time-based indirects calculation

---

### D-1621: Contingency Baseline Rates

**Decision:** Apply baseline contingency rates per AGENT_ESTIMATING model with allowance-heavy adjustments

**Trigger:** All pricing is allowance/parametric-based; no vendor quotes

**Evidence:**
- AGENT_ESTIMATING lines 678-689: baseline + allowance-heavy adjustment
- Baseline: E=10%, MAT=15%, CD=20%, CI=20%, P=10%, PM=10%, COM=25%
- Allowance share ≥50%: +5%; ≥80%: +10%
- PKG-16 allowance share: 100% (all allowance/parametric)

**Impacted WBS/CBS:** CONT (contingency)

**Estimate Impact:** Elevated contingency rates:
- E: 20% (baseline 10% + 10% allowance adjustment)
- MAT: 25% (baseline 15% + 10% allowance adjustment)
- CD: 30% (baseline 20% + 10% allowance adjustment)
- CI: 30% (baseline 20% + 10% allowance adjustment)
- P: 15% (baseline 10% + 5% allowance adjustment)
- PM: 15% (baseline 10% + 5% allowance adjustment)
- COM: 35% (baseline 25% + 10% allowance adjustment)

**Override:** Obtain vendor quotes and design quantities to reduce allowance share and lower contingency

---

### D-1622: Control Valve vs Isolation Valve Ratio

**Decision:** Estimate **13% control valves, 68% isolation valves, 9% relief valves, 9% strainers** (by count)

**Trigger:** No P&IDs; no valve service assignments; must estimate mix

**Evidence:**
- Typical transload facility: More isolation valves than control valves (many manual block valves for maintenance isolation)
- Control valves: Flow/pressure/level control at critical points (railcar stations, loading arms, tank inlets)
- Relief valves: Safety-critical overpressure protection (one per tank, pump, blocked line segment)
- Strainers: One per pump suction, one per meter (protection devices)
- Industry ratios for process facilities: ~10-15% control, ~65-75% isolation, ~5-10% relief, ~5-10% specialty

**Impacted WBS/CBS:** MAT (control valves cost ~3-5× isolation valves due to actuators/instrumentation)

**Estimate Impact:** Weighted average valve cost reflects mix (higher isolation valve count reduces average cost)

**Assumption:** A-1608 (valve type ratio)

**Override:** Provide P&IDs with valve counts by type to replace parametric ratio

---

### D-1623: Relief Valve Sizing Basis (Placeholder)

**Decision:** Estimate relief valve count based on **protected equipment count** (tanks, pumps, blocked segments)

**Trigger:** No DEL-16.03 relief calculations; no equipment datasheets with MAWP

**Evidence:**
- Storage tanks: 3 tanks → 3 tank relief valves (one per tank)
- Pumps: ~6-8 pumps (unloading, transfer, loading) → 6-8 pump relief valves
- Thermal relief (blocked line segments): ~6-10 thermal relief valves
- Total: ~15-21 relief valves
- Estimate: 20 relief valves (midpoint)

**Impacted WBS/CBS:** MAT (relief valve count)

**Estimate Impact:** Relief valve count = 20 units

**Assumption:** A-1609 (relief valve count)

**Override:** Provide DEL-16.03 relief calculations or PKG-13 tank datasheets with relief requirements

---

### D-1624: Strainer Count Estimation

**Decision:** Estimate **20 strainers** (one per pump suction, one per meter, spares)

**Trigger:** No piping layout; no equipment list with strainer requirements

**Evidence:**
- Pump count estimate: ~6-8 pumps → 6-8 pump suction strainers
- Meter count estimate: ~6-10 meters (custody transfer, batching) → 6-10 meter strainers
- Spare/standby: ~2-4 additional strainers
- Total: ~14-22 strainers
- Estimate: 20 strainers (midpoint)

**Impacted WBS/CBS:** MAT (strainer count)

**Estimate Impact:** Strainer count = 20 units

**Assumption:** A-1610 (strainer count)

**Override:** Provide P&IDs or equipment datasheets with actual strainer requirements

---

### D-1625: Specialty Equipment Scope

**Decision:** Include **check valves** as specialty equipment; exclude other specialty items for this estimate

**Trigger:** "Specialty items" in PKG-16 scope is ambiguous; no deliverables explicitly list specialty equipment

**Evidence:**
- PKG-16 scope: "Control valves, isolation valves, relief valves, strainers, specialty items"
- Common specialty items: Check valves (backflow prevention), pressure regulators, special service valves
- Check valves: Typical ~15-25 units in transload facility (pump discharge, gravity feed prevention)

**Impacted WBS/CBS:** MAT

**Estimate Impact:** Add 20 check valves to material estimate

**Assumption:** A-1611 (specialty equipment scope = check valves)

**Override:** Provide scope clarification for "specialty items" or P&IDs showing specialty equipment

---

### D-1626: Installation Labor Rate

**Decision:** Use **$95/hr all-in** (blended rate for pipefitter, instrument tech, electrician)

**Trigger:** No project labor rate tables available

**Evidence:**
- BC Lower Mainland union labor rates (2026): $70-85/hr base wage
- All-in rate with benefits, payroll burden, small tools: 1.4-1.5× base = $98-$128/hr
- Blended rate (pipefitter + instrument tech + electrician): $90-$100/hr typical
- Midpoint: $95/hr

**Impacted WBS/CBS:** CD (installation labor cost)

**Estimate Impact:** Installation labor priced at $95/hr blended rate

**Assumption:** A-1612 (labor rate)

**Override:** Provide project labor rate tables or construction manager's all-in labor rate estimate

---

### D-1627: Engineering Hours Estimation

**Decision:** Estimate engineering hours using **deliverable complexity** and **typical effort per valve**

**Trigger:** No engineering budget; no manhour estimate from project team

**Evidence:**
- DEL-16.01 drawings: ~800-1,200 hours (arrangement drawings for ~220 valves, actuator details)
- DEL-16.02 specifications: ~400-600 hours (3 specs: control, isolation, relief)
- DEL-16.03 calculations: ~600-900 hours (30 control valve sizing, 20 relief valve sizing, actuator sizing)
- DEL-16.04 datasheets: ~900-1,400 hours (220 datasheets @ 4-6 hours each)
- Total: ~2,700-4,100 hours
- Estimate: 3,400 hours (midpoint)

**Impacted WBS/CBS:** E (engineering cost)

**Estimate Impact:** Engineering effort = 3,400 hours @ $155/hr blended = $527k

**Assumption:** A-1613 (engineering hours)

**Override:** Provide engineering manager's manhour estimate or historical data for similar valve packages

---

### D-1628: Engineering Hourly Rate

**Decision:** Use **$155/hr blended** rate for mechanical engineering

**Trigger:** No engineering rate table available

**Evidence:**
- BC mechanical engineer rate (P.Eng. + EIT mix): $120-180/hr
- CAD technician rate: $80-120/hr
- Blended rate for mechanical discipline: $140-170/hr typical
- Midpoint: $155/hr

**Impacted WBS/CBS:** E

**Estimate Impact:** Engineering priced at $155/hr blended rate

**Assumption:** A-1614 (engineering rate)

**Override:** Provide engineering rate table or project billing rates

---

### D-1629: QA/QC Testing Scope (DEL-16.05)

**Decision:** Include testing scope in **COM (Commissioning)** factor-based bucket

**Trigger:** DEL-16.05 testing scope not quantified (test counts, duration TBD)

**Evidence:**
- DEL-16.05 anticipated artifacts: Material certificates, FAT records, set pressure test records
- Testing included in COM factor (3% of CD+CI+MAT)
- Relief valve set pressure testing: Typically vendor FAT (included in valve supply cost)
- Control valve stroking tests: Field commissioning activity (included in COM)

**Impacted WBS/CBS:** COM (testing cost included in commissioning factor)

**Estimate Impact:** No separate testing line; testing included in COM = 3% × (CD+CI+MAT)

**Assumption:** A-1615 (testing scope in COM factor)

**Override:** Provide detailed test plan if testing scope exceeds typical commissioning factor coverage

---

### D-1630: RUN_STATUS Classification

**Decision:** Set RUN_STATUS = **WARNINGS**

**Trigger:** Estimate complete but with material assumptions and 100% allowance-based pricing

**Evidence:**
- No critical failures (all required files generated; all line items have Qty/Unit/UnitRate)
- Material assumptions: Valve counts, sizes, materials all parametric/allowance-based
- Confidence: LOW (100% allowance/parametric pricing)
- Suitable for conceptual budgeting; not suitable for procurement or GMP

**Impacted WBS/CBS:** N/A (status classification)

**Estimate Impact:** Estimate published with WARNINGS status; flagged for re-estimate when design quantities available

**Override:** Obtain design quantities and vendor quotes to upgrade status to OK

---

## Decision Summary Statistics

| Metric | Count |
|--------|-------|
| Total decisions | 30 |
| Path/workspace decisions | 1 |
| Config/basis decisions | 9 |
| Quantity estimation decisions | 7 |
| Pricing decisions | 6 |
| Scope/mapping decisions | 5 |
| Status decisions | 2 |

---

**Decision Log Prepared By:** Estimating Agent
**Date:** 2026-01-28
**Status:** Complete (30 decisions recorded)
