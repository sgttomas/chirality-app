# Assumptions Log — PKG-16 Valves & Specialty Equipment

**Snapshot ID:** EST_PKG16_DRAFT_2026-01-28_2347
**Package:** PKG-16 Valves & Specialty Equipment
**Date:** 2026-01-28

---

## Purpose

This log records all assumptions and allowances where scope, quantities, or pricing required estimation due to missing design information or vendor data.

Each assumption is traceable to impacted WBS/CBS, cost impact, confidence level, and resolution path.

---

## Assumption Entries

### A-1601: Valve Count Parametric Estimate

**Statement:** Total valve count estimated at **220 valves** (30 control, 150 isolation, 20 relief, 20 strainers)

**Why Needed:** No P&IDs available; no valve lists; no equipment datasheets with valve interface counts

**Basis:**
- 32 railcar unloading stations @ 4-6 valves/station → 128-192 valves
- 3 storage tanks @ 10-15 valves/tank → 30-45 valves
- Marine loading system → 15-25 valves
- Product transfer system → 10-15 valves
- Total range: 183-277 valves
- Conservative midpoint: 220 valves

**Impacted WBS/CBS:** All deliverables, MAT, CD

**Cost Impact:** $1,320,000 CAD (materials) + $470,000 CAD (installation) = $1,790,000 CAD base cost

**Range:** -20% / +30% (176-286 valves) → $1,430k-$2,320k

**Confidence:** LOW

**Resolution Path:** Complete P&IDs (PKG-10, PKG-11, PKG-12, PKG-13) with valve tagging and counts; provide actual valve list

**Reference:** Decision D-1611, D-1617

---

### A-1602: Valve Size Distribution

**Statement:** Valve size distribution: 60% small (DN50-100), 30% medium (DN150-200), 10% large (DN250-300)

**Why Needed:** No piping line list; no valve datasheets with sizes

**Basis:**
- Typical transload facility piping: 2"-12" product lines, 1"-4" utility/control lines
- Small valves (DN50-100 / 2"-4"): Control valves, small isolation, instruments → ~132 units (60%)
- Medium valves (DN150-200 / 6"-8"): Tank isolation, main product lines → ~66 units (30%)
- Large valves (DN250-300 / 10"-12"): Tank inlets/outlets, main headers → ~22 units (10%)

**Impacted WBS/CBS:** MAT (valve cost scales with size)

**Cost Impact:** Weighted average valve cost reflects size distribution

**Range:** Small-heavy (70%-20%-10%) reduces cost ~10%; large-heavy (50%-30%-20%) increases cost ~15%

**Confidence:** LOW

**Resolution Path:** Provide piping line list with line sizes or DEL-16.04 datasheets with actual valve sizes

**Reference:** Decision D-1612

---

### A-1603: Valve Material Selection (Stainless Steel)

**Statement:** Product-contact valves specified as **316SS** (stainless steel)

**Why Needed:** DEL-16.02 specification not finalized; material selection TBD

**Basis:**
- Food-grade canola oil service requires cleanable, corrosion-resistant materials
- DEL-16.04 Datasheet.md: "Stainless steel (316SS or 304SS) for food-grade cleanliness"
- Coastal marine environment (Fraser Surrey Terminal) requires corrosion resistance
- Industry practice: 316SS typical for edible oil service

**Impacted WBS/CBS:** MAT (SS valves cost ~2-3× carbon steel)

**Cost Impact:** Material allowances priced at SS rates (~2.5× carbon steel baseline)

**Range:** If carbon steel acceptable (with coating): reduce MAT cost ~40% ($528k savings); if upgraded alloys required: increase MAT cost ~15% ($198k increase)

**Confidence:** MEDIUM (supported by deliverable datasheets; formal specification TBD)

**Resolution Path:** Complete DEL-16.02 specification with actual material selections; confirm food-grade requirements in ER Volume 2 Part 2

**Reference:** Decision D-1613

---

### A-1604: Actuator Type Distribution

**Statement:** Actuator distribution: 60% manual, 30% pneumatic, 10% electric (by valve count)

**Why Needed:** No P&IDs with actuation requirements; no control philosophy

**Basis:**
- Manual valves: ~132 units (isolation valves for maintenance, infrequent operation)
- Pneumatic actuated: ~66 units (control valves, ESD valves, seasonal isolation)
- Electric actuated: ~22 units (large MOVs for tank isolation, main line isolation)
- Typical transload facility: Majority manual isolation; automated for control and safety

**Impacted WBS/CBS:** MAT (actuators), CD (automated valves require pneumatic/electrical hookup)

**Cost Impact:** Actuated valves (88 units) add ~$660k actuator cost + $110k installation vs. manual baseline

**Range:** If more automation (40% pneumatic, 20% electric): increase cost ~$250k; if less automation (20% pneumatic, 5% electric): reduce cost ~$350k

**Confidence:** LOW

**Resolution Path:** Provide P&IDs with valve actuation symbols or control philosophy document with automation strategy

**Reference:** Decision D-1614

---

### A-1605: Control Valve Complexity Mix

**Statement:** Control valve complexity: 50% standard globe, 30% ball/butterfly, 20% severe service

**Why Needed:** No sizing calculations; no trim selections; no service conditions defined

**Basis:**
- Standard globe valves: General flow/pressure control (15 units) @ ~$8k-12k
- Ball/butterfly control valves: Large size modulating applications (9 units) @ ~$10k-18k
- Severe service: High pressure drop, cavitation, noise control (6 units) @ ~$15k-30k
- Typical process facility control valve mix

**Impacted WBS/CBS:** MAT (severe service valves cost ~2-3× standard)

**Cost Impact:** Weighted average control valve cost ~$12k (vs. $10k if all standard)

**Range:** If all standard: reduce control valve cost ~$60k; if more severe service (40%): increase cost ~$90k

**Confidence:** LOW

**Resolution Path:** Complete DEL-16.03 sizing calculations or DEL-16.04 datasheets with valve body styles and trim types

**Reference:** Decision D-1615

---

### A-1606: Valve Unit Costs (Typical BC Market Rates)

**Statement:** Valve unit costs based on typical BC/Canada market pricing (January 2026)

**Why Needed:** No vendor quotes; no rate tables

**Basis (typical unit costs, stainless steel):**

**Isolation Valves (Manual):**
- Small (DN50-100, gate/ball): $1,500/unit
- Medium (DN150-200, gate/ball): $5,000/unit
- Large (DN250-300, gate/ball): $15,000/unit

**Isolation Valves (Automated):**
- Small pneumatic (DN50-100): $5,000/unit (valve + actuator + accessories)
- Medium pneumatic (DN150-200): $12,000/unit
- Large electric (DN250-300, MOV): $35,000/unit (valve + motor operator)

**Control Valves (with pneumatic actuator + positioner):**
- Small (DN50-100, standard globe): $10,000/unit
- Medium (DN150-200, ball/butterfly): $18,000/unit
- Severe service (anti-cavitation, noise trim): $25,000/unit

**Relief Valves (API 526, stainless steel):**
- Small (DN25-50, orifice D-F): $4,000/unit
- Medium (DN80-100, orifice G-J): $8,000/unit
- Large (DN150+, orifice K+): $15,000/unit

**Strainers (Y-type or basket, stainless steel):**
- Small (DN50-100): $2,500/unit
- Medium (DN150-200): $6,000/unit

**Check Valves (swing or wafer, stainless steel):**
- Small (DN50-100): $1,200/unit
- Medium (DN150-200): $4,000/unit
- Large (DN250-300): $12,000/unit

**Impacted WBS/CBS:** MAT

**Cost Impact:** Total valve material cost ~$1,320k (weighted average ~$6k per valve)

**Range:** -15% / +25% vendor quote variability → $1,120k-$1,650k

**Confidence:** LOW (no vendor quotes; market rate assumptions)

**Resolution Path:** Obtain budgetary quotes from valve vendors for actual project valve list

**Reference:** Decision D-1618

---

### A-1607: Valve Installation Productivity

**Statement:** Valve installation labor hours: 4-24 hours per valve (size and complexity dependent)

**Why Needed:** No construction management estimate; no project productivity data

**Basis:**
- Small manual valve (DN50-100): 4 hours (rigging, bolting, gaskets, alignment)
- Medium manual valve (DN150-200): 8 hours
- Large manual valve (DN250-300): 16 hours
- Actuated valve additional: +2-4 hours (actuator mounting, pneumatic/electrical hookup, calibration)
- Testing support: +1-2 hours per valve (hydrostatic test, functional test)
- Average: ~6 hours per valve (weighted by size and actuation distribution)

**Impacted WBS/CBS:** CD (installation labor)

**Cost Impact:** Installation labor ~1,320 hours @ $95/hr = $125k

**Range:** -20% / +30% productivity variability → $100k-$163k

**Confidence:** MEDIUM (typical productivity; site-specific constraints TBD)

**Resolution Path:** Provide construction manager's productivity estimate or historical data for valve installation at marine terminals

**Reference:** Decision D-1619

---

### A-1608: Valve Type Ratio (Count Distribution)

**Statement:** Valve count by type: 30 control (13%), 150 isolation (68%), 20 relief (9%), 20 strainers/specialty (9%)

**Why Needed:** No P&IDs; no valve service assignments

**Basis:**
- Control valves: Flow/pressure/level control at railcar stations (16), tanks (6), loading arms (4), transfer (4) → 30 units
- Isolation valves: Equipment isolation, line isolation, maintenance blocks (typical ~65-75% of valve count) → 150 units
- Relief valves: Tank relief (3), pump relief (8), thermal relief (9) → 20 units
- Strainers: Pump suction (8), meter protection (8), spares (4) → 20 units
- Total: 220 valves

**Impacted WBS/CBS:** MAT, CD

**Cost Impact:** Control valves (higher unit cost) = ~24% of MAT cost despite 13% of count

**Range:** If more control (20% of count): increase cost ~$150k; if fewer control (10% of count): reduce cost ~$80k

**Confidence:** LOW

**Resolution Path:** Provide P&IDs with valve counts by type and service

**Reference:** Decision D-1622

---

### A-1609: Relief Valve Count

**Statement:** Relief valve count estimated at **20 units** (3 tank, 8 pump, 9 thermal)

**Why Needed:** No DEL-16.03 relief calculations; no equipment datasheets with relief requirements

**Basis:**
- Storage tanks: 3 tanks → 3 tank relief valves (one per tank per ASME Section VIII)
- Pumps: 8 pumps estimated (4 unloading, 2 transfer, 2 loading) → 8 pump relief valves
- Thermal relief: 9 blocked line segments (tank outlets, pump discharge, loading arms) → 9 thermal relief valves
- Total: 20 relief valves

**Impacted WBS/CBS:** MAT (relief valves)

**Cost Impact:** Relief valves ~$135k (20 units @ $6,750 average)

**Range:** 15-25 relief valves → $101k-$169k

**Confidence:** LOW

**Resolution Path:** Complete DEL-16.03 relief calculations or provide PKG-13 storage tank datasheets with relief valve requirements

**Reference:** Decision D-1623

---

### A-1610: Strainer Count

**Statement:** Strainer count estimated at **20 units** (8 pump suction, 8 meter, 4 spare)

**Why Needed:** No equipment list; no P&IDs with strainer locations

**Basis:**
- Pump suction strainers: 8 pumps → 8 strainers (one per pump)
- Meter protection strainers: 8 meters (custody transfer, batching) → 8 strainers
- Spare/standby strainers: 4 units
- Total: 20 strainers

**Impacted WBS/CBS:** MAT (strainers)

**Cost Impact:** Strainers ~$65k (20 units @ $3,250 average)

**Range:** 14-26 strainers → $46k-$85k

**Confidence:** LOW

**Resolution Path:** Provide P&IDs or equipment list with strainer requirements

**Reference:** Decision D-1624

---

### A-1611: Specialty Equipment Scope (Check Valves)

**Statement:** Specialty equipment includes **20 check valves**; other specialty items excluded

**Why Needed:** "Specialty items" in PKG-16 scope is ambiguous

**Basis:**
- Check valves: Backflow prevention at pump discharge (8), gravity feed prevention (8), system isolation (4) → 20 units
- Other specialty (pressure regulators, special service valves): Assumed minimal or included in other packages

**Impacted WBS/CBS:** MAT (check valves)

**Cost Impact:** Check valves ~$50k (20 units @ $2,500 average)

**Range:** 15-30 check valves → $38k-$75k; if other specialty items required: +$50k-$150k

**Confidence:** LOW

**Resolution Path:** Clarify "specialty items" scope or provide P&IDs showing specialty equipment

**Reference:** Decision D-1625

---

### A-1612: Installation Labor Rate (All-In Blended)

**Statement:** Installation labor rate **$95/hr all-in** (blended pipefitter, instrument tech, electrician)

**Why Needed:** No project labor rate tables

**Basis:**
- BC Lower Mainland union rates (2026): $70-85/hr base wage
- All-in multiplier (benefits, burden, small tools): 1.4-1.5×
- Blended crafts (pipefitter 60%, instrument tech 25%, electrician 15%): $90-100/hr
- Midpoint: $95/hr

**Impacted WBS/CBS:** CD (installation labor)

**Cost Impact:** Installation labor ~$125k (1,320 hours @ $95/hr)

**Range:** $85-105/hr → $112k-$139k

**Confidence:** MEDIUM (typical BC rates; project-specific rates TBD)

**Resolution Path:** Provide project labor rate table or construction manager's all-in labor rate estimate

**Reference:** Decision D-1626

---

### A-1613: Engineering Hours Estimate

**Statement:** Engineering effort estimated at **3,400 hours** across 5 deliverables

**Why Needed:** No engineering budget; no manhour estimate from project team

**Basis:**
- DEL-16.01 drawings: 1,000 hours (arrangement drawings for ~220 valves, actuator details)
- DEL-16.02 specifications: 500 hours (3 specs: control, isolation, relief)
- DEL-16.03 calculations: 750 hours (30 control valve sizing, 20 relief valve sizing, actuator sizing)
- DEL-16.04 datasheets: 1,150 hours (220 datasheets @ 5 hours each avg)
- Total: 3,400 hours

**Impacted WBS/CBS:** E (engineering cost)

**Cost Impact:** Engineering ~$527k (3,400 hours @ $155/hr)

**Range:** 2,700-4,100 hours → $419k-$636k

**Confidence:** MEDIUM (typical effort for valve package; actual hours vary with design complexity)

**Resolution Path:** Provide engineering manager's manhour budget or historical data for similar valve packages

**Reference:** Decision D-1627

---

### A-1614: Engineering Hourly Rate (Blended)

**Statement:** Mechanical engineering rate **$155/hr blended** (P.Eng., EIT, CAD tech mix)

**Why Needed:** No engineering rate table

**Basis:**
- BC mechanical engineer (P.Eng.): $160-200/hr
- Engineer-in-Training (EIT): $120-140/hr
- CAD technician: $90-110/hr
- Blended mix (30% P.Eng., 50% EIT, 20% CAD): $150-160/hr
- Midpoint: $155/hr

**Impacted WBS/CBS:** E

**Cost Impact:** Engineering priced at $155/hr

**Range:** $140-170/hr → $476k-$578k

**Confidence:** MEDIUM (typical BC engineering rates; project billing rates TBD)

**Resolution Path:** Provide engineering rate table or project billing rates

**Reference:** Decision D-1628

---

### A-1615: Testing Scope in Commissioning Factor

**Statement:** Valve testing (DEL-16.05) included in **COM factor** (no separate testing line)

**Why Needed:** DEL-16.05 testing scope not quantified (test counts, duration TBD)

**Basis:**
- Relief valve set pressure testing: Vendor FAT (included in valve supply cost)
- Control valve stroking/calibration: Field commissioning (included in COM factor)
- Hydrostatic testing: Field installation verification (included in COM factor)
- COM factor = 3% × (CD+CI+MAT) covers typical commissioning/testing scope

**Impacted WBS/CBS:** COM (testing cost allocation)

**Cost Impact:** Testing included in COM = $58k; no separate testing line

**Range:** If extensive testing required (special FATs, third-party witness): add $30k-$80k dedicated testing line

**Confidence:** MEDIUM (typical testing scope for valves)

**Resolution Path:** Provide detailed test plan if testing scope exceeds typical commissioning coverage

**Reference:** Decision D-1629

---

### A-1616: Control Valve Count (Railcar Unloading)

**Statement:** Railcar unloading stations (32 stations) require **16 control valves** (one per two stations)

**Why Needed:** No P&IDs; no unloading system control philosophy

**Basis:**
- 32 railcar stations (PKG-10 scope from decomposition)
- Typical unloading: Gravity feed with flow control or pump-assisted
- Control valve strategy: One flow control valve per two stations (paired stations) → 16 control valves
- Alternate: One control valve per station → 32 control valves (increases cost)

**Impacted WBS/CBS:** MAT (control valves)

**Cost Impact:** 16 control valves @ ~$10k avg = $160k

**Range:** 8-32 control valves (depending on unloading control strategy) → $80k-$320k

**Confidence:** LOW

**Resolution Path:** Provide PKG-10 railcar unloading system P&IDs or control philosophy

**Reference:** Related to A-1608 (valve type ratio)

---

### A-1617: Storage Tank Valve Count

**Statement:** Storage tanks (3 tanks) require **~36 valves total** (12 per tank)

**Why Needed:** No tank P&IDs; no PKG-13 tank datasheets with valve interface requirements

**Basis (per tank, typical):**
- Tank inlet isolation: 1 valve (large, DN200-300)
- Tank outlet isolation: 1 valve (large, DN200-300)
- Tank level control: 2 valves (inlet flow control, outlet level control)
- Tank relief valve: 1 valve (overpressure protection per ASME)
- Tank drain: 1 valve (manual, small)
- Tank sample: 1 valve (manual, small)
- Tank gauge/instrumentation: 2 valves (isolation for level gauges, temperature)
- Tank nitrogen blanketing: 2 valves (supply, relief) — if nitrogen blanketing used
- Tank heating/circulation: 1 valve (if heating system used)
- Total per tank: ~12 valves
- 3 tanks: ~36 valves

**Impacted WBS/CBS:** MAT, CD

**Cost Impact:** Tank valves ~$260k materials + $40k installation

**Range:** 9-15 valves per tank → $243k-$405k total (materials + installation)

**Confidence:** LOW

**Resolution Path:** Provide PKG-13 storage tank P&IDs or tank datasheets with valve interface schedule

**Reference:** Related to A-1601 (valve count)

---

### A-1618: Marine Loading Arm Valve Count

**Statement:** Marine loading system (PKG-11) requires **~25 valves** (loading arm isolation, flow control, relief)

**Why Needed:** No PKG-11 marine loading P&IDs; loading arm configuration TBD

**Basis:**
- Loading arm: 1-2 arms (typical for ship loading)
- Valves per arm: Flow control (1), inlet isolation (2), emergency isolation (ESD, 1), relief (1), drain (1), sample (1), nitrogen purge (1) → ~8 valves per arm
- Shore piping: Main isolation (2), flow meter isolation (4), pump isolation (4), header valves (3) → ~13 valves
- Total: ~25 valves (conservative for 1-2 loading arms)

**Impacted WBS/CBS:** MAT, CD

**Cost Impact:** Marine loading valves ~$180k materials + $30k installation

**Range:** 15-40 valves (depending on loading arm count and complexity) → $105k-$350k

**Confidence:** LOW

**Resolution Path:** Provide PKG-11 marine loading system P&IDs or loading arm vendor datasheet with valve requirements

**Reference:** Related to A-1601 (valve count)

---

### A-1619: Product Transfer System Valve Count

**Statement:** Product transfer and metering (PKG-12) requires **~30 valves**

**Why Needed:** No PKG-12 transfer system P&IDs; piping layout TBD

**Basis:**
- Transfer pumps: 2-3 pumps @ 6 valves each (suction, discharge, bypass, drain, sample, relief) → 12-18 valves
- Transfer piping: Manifold isolation, header isolation → 8-12 valves
- Meters: Custody transfer meters with isolation, bypass, proving → 6-10 valves
- Total: ~26-40 valves
- Estimate: 30 valves (midpoint)

**Impacted WBS/CBS:** MAT, CD

**Cost Impact:** Transfer valves ~$195k materials + $35k installation

**Range:** 20-40 valves → $130k-$310k

**Confidence:** LOW

**Resolution Path:** Provide PKG-12 product transfer P&IDs or transfer pump/meter datasheets

**Reference:** Related to A-1601 (valve count)

---

### A-1620: Valve Installation Cost (Rigging, Bolting, Testing)

**Statement:** Valve installation includes rigging, bolting, gasket installation, alignment, hydrostatic testing support

**Why Needed:** No installation specification; no construction WBS with valve installation breakdown

**Basis:**
- Rigging and positioning: 1-4 hours (size-dependent)
- Bolting and gasket installation: 1-2 hours
- Alignment verification: 0.5-1 hour
- Hydrostatic test support: 1-2 hours (pressurize, hold, inspect)
- Total: 4-9 hours per valve (average 6 hours weighted by size)

**Impacted WBS/CBS:** CD

**Cost Impact:** Installation labor ~$125k (1,320 hours total)

**Range:** -20% / +30% → $100k-$163k

**Confidence:** MEDIUM

**Resolution Path:** Provide construction execution plan or installation procedure with crew makeup and productivity

**Reference:** Related to A-1607

---

### A-1621: Actuator Hookup Labor

**Statement:** Actuator hookup (pneumatic/electrical) adds **2-4 hours per actuated valve**

**Why Needed:** No construction estimate for instrumentation/electrical hookup

**Basis:**
- Pneumatic hookup: Tubing installation, air set mounting, leak check, stroking test → 2-3 hours
- Electrical hookup: Conduit/cable pull, terminations, motor test, stroking test → 3-4 hours
- Positioner/accessories: Calibration, loop check → +1-2 hours
- 88 actuated valves (30 pneumatic control + 36 pneumatic isolation + 22 electric isolation)
- Average: 3 hours per actuated valve
- Total: 264 hours

**Impacted WBS/CBS:** CD (hookup labor)

**Cost Impact:** Actuator hookup ~$25k (264 hours @ $95/hr)

**Range:** 2-5 hours per valve → $17k-$42k

**Confidence:** MEDIUM

**Resolution Path:** Provide construction manager's estimate for actuator installation and hookup

**Reference:** Included in overall installation labor (A-1607, A-1620)

---

### A-1622: Control Valve Accessories (Positioners, Limit Switches)

**Statement:** Control valves (30 units) include **smart positioners** ($3,500 each avg); isolation valves include **limit switches** where actuated ($800 each avg)

**Why Needed:** No instrumentation specification; no accessory list

**Basis:**
- Control valves: Smart positioner with HART or FF protocol (typical for modern DCS integration)
- Positioner cost: $2,500-$4,500 (size and protocol dependent) → avg $3,500
- Automated isolation valves (66 units): Limit switches for position indication
- Limit switch cost: $600-$1,000 (enclosure-dependent) → avg $800
- Total accessories: 30 positioners + 66 limit switches = $158k

**Impacted WBS/CBS:** MAT (valve accessories)

**Cost Impact:** Accessories ~$158k (included in control valve and automated isolation valve line items)

**Range:** -20% / +30% → $126k-$205k

**Confidence:** MEDIUM (typical accessories for process control)

**Resolution Path:** Provide instrumentation specification (PKG-20) or control philosophy with positioner/accessory requirements

**Reference:** Included in valve unit costs (A-1606)

---

### A-1623: Valve Freight and Logistics

**Statement:** Valve freight estimated at **8% of valve FOB cost**

**Why Needed:** No freight quotes; no logistics plan

**Basis:**
- Valve shipment: Lower Mainland BC delivery from vendors (typically Ontario, Quebec, or USA)
- Freight for industrial equipment: 5-10% of FOB typical
- Conservative: 8% of valve material cost
- Valve MAT cost: $1,320k → freight ~$106k

**Impacted WBS/CBS:** FRT (if separated) or MAT (if freight included in MAT)

**Cost Impact:** Freight ~$106k (included in MAT allowances or separate FRT line)

**Range:** 5-12% → $66k-$158k

**Confidence:** MEDIUM

**Resolution Path:** Obtain freight quotes or use project logistics plan with freight factors

**Reference:** Not separated in this estimate (freight included in MAT allowances); see Note in BOE

---

### A-1624: Relief Valve Set Pressure Testing (Vendor FAT)

**Statement:** Relief valve set pressure testing performed at **vendor FAT** (included in valve supply cost)

**Why Needed:** DEL-16.05 test scope not detailed; FAT vs field testing TBD

**Basis:**
- API 526 relief valves: Typically factory-tested and ASME-stamped before shipment
- Set pressure test certificate provided with each valve
- Field testing: Verification only (not full set pressure test)
- Vendor FAT cost: Included in valve supply price (no separate line)

**Impacted WBS/CBS:** MAT (relief valves), COM (field verification)

**Cost Impact:** FAT included in relief valve unit cost (no separate testing line)

**Range:** If field set pressure testing required: add $15k-$30k (test equipment rental, labor, recertification)

**Confidence:** HIGH (standard industry practice for API 526 relief valves)

**Resolution Path:** Confirm test plan in DEL-16.05 or commissioning procedures

**Reference:** Supports D-1629 (testing in COM factor)

---

### A-1625: Valve Body Material Cost Premium (Stainless Steel)

**Statement:** Stainless steel valve cost premium: **~2.5× carbon steel baseline**

**Why Needed:** No vendor quotes for SS vs CS valves; material premium estimation required

**Basis:**
- Carbon steel isolation valve (DN100, manual): ~$600 typical
- Stainless steel 316 isolation valve (DN100, manual): ~$1,500 typical
- Material premium factor: 2.3-2.7× (average 2.5×)
- Applied to all product-contact valves per A-1603

**Impacted WBS/CBS:** MAT

**Cost Impact:** SS material premium adds ~$530k vs. carbon steel baseline

**Range:** 2.0-3.0× premium → $425k-$635k premium

**Confidence:** MEDIUM (typical SS premium; vendor-specific pricing varies)

**Resolution Path:** Obtain vendor quotes for SS valves or confirm material selection in DEL-16.02 specification

**Reference:** Related to A-1603 (material selection)

---

### A-1626: Actuator Cost Distribution

**Statement:** Actuator costs: Pneumatic $3k-$15k (size-dependent), Electric $8k-$40k (size-dependent)

**Why Needed:** No actuator quotes; no vendor selection

**Basis:**
- Small pneumatic actuator (DN50-100, spring-return): $3,000-$5,000
- Medium pneumatic actuator (DN150-200, double-acting): $8,000-$15,000
- Large electric actuator (DN250-300, motor operator): $20,000-$40,000
- Accessories (air set, solenoid, limit switches): $1,500-$3,000
- Weighted average per A-1604 distribution

**Impacted WBS/CBS:** MAT (actuators included in automated valve lines)

**Cost Impact:** Actuators ~$660k (88 actuated valves)

**Range:** -20% / +30% → $528k-$858k

**Confidence:** LOW (no vendor quotes)

**Resolution Path:** Obtain actuator budgetary quotes or actuator vendor catalog pricing

**Reference:** Included in automated valve unit costs (A-1606)

---

### A-1627: Valve Bolting and Gasket Allowance

**Statement:** Valve bolting and gaskets estimated at **5% of valve cost**

**Why Needed:** No flange bolt count; no gasket specifications

**Basis:**
- Typical valve installation: ASME B16.5 flange bolting + spiral-wound gaskets
- Bolting and gasket cost: 3-7% of valve cost (size-dependent)
- Average: 5% of valve material cost
- Valve MAT cost: $1,320k → bolting/gaskets ~$66k

**Impacted WBS/CBS:** MAT (bolting/gaskets included in installation allowances)

**Cost Impact:** Bolting/gaskets ~$66k (included in valve material allowances)

**Range:** 3-8% → $40k-$106k

**Confidence:** MEDIUM

**Resolution Path:** Develop flange bolt/gasket schedule from piping design or extract from vendor valve submittals

**Reference:** Included in valve material line items

---

### A-1628: Valve Installation Equipment (Crane, Rigging)

**Statement:** Valve installation equipment (crane, rigging, lifting gear) included in **CD installation allowance**

**Why Needed:** No construction equipment estimate; no rigging plan

**Basis:**
- Small/medium valves: Manual handling or small crane (cost embedded in labor productivity)
- Large valves (DN250-300): Mobile crane required (~2-4 hours crane time per valve @ $150/hr)
- Rigging gear: Slings, shackles, spreader bars (consumable allowance ~2% of CD)
- Total: ~88 crane hours for 22 large valves + rigging consumables

**Impacted WBS/CBS:** CD (installation equipment)

**Cost Impact:** Equipment ~$13k crane + $9k rigging = $22k (included in CD installation allowances)

**Range:** -30% / +50% → $15k-$33k

**Confidence:** MEDIUM

**Resolution Path:** Provide construction equipment plan or crane/rigging estimate from construction manager

**Reference:** Included in CD installation allowances

---

### A-1629: Valve Calibration and Loop Check (Control Valves)

**Statement:** Control valve calibration and loop check (30 valves) estimated at **4 hours per valve**

**Why Needed:** No commissioning plan; no loop list; no testing procedures

**Basis:**
- Control valve commissioning: Stroking test, positioner calibration, control loop check, functional test
- Typical effort: 3-5 hours per control valve (instrument tech + process engineer)
- 30 control valves @ 4 hours = 120 hours
- Rate: $110/hr (instrument tech higher rate than pipefitter)

**Impacted WBS/CBS:** COM (commissioning labor)

**Cost Impact:** Control valve commissioning ~$13k (included in COM factor $58k)

**Range:** 3-6 hours per valve → $10k-$20k

**Confidence:** MEDIUM

**Resolution Path:** Provide commissioning plan or DEL-16.05 test procedures with test duration estimates

**Reference:** Included in COM factor (supports A-1615)

---

### A-1630: Relief Valve Field Verification Testing

**Statement:** Relief valve field verification (20 valves) estimated at **2 hours per valve**

**Why Needed:** No test plan; field verification scope TBD

**Basis:**
- Factory set pressure test: Performed at vendor (included in valve cost)
- Field verification: Visual inspection, nameplate verification, installation orientation check
- No field set pressure testing (valves arrive pre-tested and sealed)
- Typical effort: 1.5-2.5 hours per relief valve
- 20 relief valves @ 2 hours = 40 hours

**Impacted WBS/CBS:** COM

**Cost Impact:** Relief valve verification ~$4k (included in COM factor $58k)

**Range:** 1-3 hours per valve → $2k-$6k

**Confidence:** MEDIUM

**Resolution Path:** Provide commissioning plan or DEL-16.05 relief valve test procedures

**Reference:** Included in COM factor (supports A-1615, A-1624)

---

### A-1631: Isolation Valve Installation Testing (Hydrostatic)

**Statement:** Isolation valve hydrostatic testing performed as **part of piping hydrostatic test** (no separate valve test)

**Why Needed:** DEL-16.05 test scope TBD; valve testing vs piping testing boundary

**Basis:**
- Industry practice: Isolation valves tested during piping system hydrostatic test (ASME B31.3)
- No separate valve shell test (valves shop-tested per API 598 before shipment)
- Field test: Seat leakage check during system hydrostatic (included in piping test scope)
- Valve test cost: Included in PKG-14 piping test cost (no separate line)

**Impacted WBS/CBS:** COM (piping test coordination)

**Cost Impact:** No separate isolation valve testing cost (included in PKG-14 piping commissioning)

**Range:** If separate valve testing required: add $8k-$15k

**Confidence:** HIGH (standard practice)

**Resolution Path:** Confirm with DEL-16.05 test procedures or PKG-14 piping commissioning procedures

**Reference:** Supports D-1629 (testing in COM factor)

---

### A-1632: Valve Installation Duration (Overall)

**Statement:** Valve installation duration estimated at **8-12 weeks** (field installation phase)

**Why Needed:** No construction schedule; duration estimate required for indirects (if time-based)

**Basis:**
- 220 valves total
- Installation crew: 2-4 pipefitters + 1-2 instrument techs
- Productivity: ~3-5 valves per day (crew-day) → 44-73 days
- Calendar duration with site coordination, material delivery delays: 8-12 weeks
- Note: Duration not used (factor-based indirects per D-1608)

**Impacted WBS/CBS:** N/A (informational; not used for indirects)

**Cost Impact:** None (factor-based indirects used instead of duration-based)

**Range:** 6-16 weeks (crew size and productivity variability)

**Confidence:** MEDIUM

**Resolution Path:** Provide construction schedule with valve installation activity duration

**Reference:** Supports D-1608 (factor-based indirects rationale)

---

### A-1633: Special Tools and Equipment (Valve Repair, Testing)

**Statement:** Special tools (torque wrenches, hydrostatic test pump, valve repair tools) estimated at **$8,000 allowance**

**Why Needed:** No tool list; no equipment rental estimate

**Basis:**
- Torque wrenches (flange bolting): $2,000 rental/purchase
- Hydrostatic test pump (portable): $3,000 rental
- Valve repair tools (seat lapping, actuator repair): $2,000
- Miscellaneous small tools: $1,000
- Total: ~$8,000

**Impacted WBS/CBS:** CD (special tools)

**Cost Impact:** Special tools ~$8k (included in installation allowances or CI)

**Range:** $5k-$12k

**Confidence:** MEDIUM

**Resolution Path:** Provide construction tool list or equipment rental plan

**Reference:** Included in CD installation allowances or CI overhead

---

### A-1634: Valve Spare Parts Allowance (Not Included)

**Statement:** Valve spare parts **excluded** from PKG-16 estimate (likely separate package or Owner-supplied)

**Why Needed:** Spare parts scope ambiguity (Contractor vs Owner responsibility)

**Basis:**
- PKG-16 scope: "Control valves, isolation valves, relief valves, strainers, specialty items"
- No explicit spare parts deliverable (DEL-16.01 through DEL-16.05)
- Typical EPC scope: Contractor provides installed equipment; Owner purchases spare parts separately
- Spare parts may be in PKG-31 (Operations & Maintenance) or separate procurement

**Impacted WBS/CBS:** MAT (if spare parts included, would add ~5-10% of valve cost)

**Cost Impact:** None (spare parts excluded)

**Range:** If spare parts included: add $66k-$132k (5-10% of valve MAT cost)

**Confidence:** MEDIUM (scope interpretation)

**Resolution Path:** Clarify spare parts responsibility in Employer's Requirements or contract scope of work

**Reference:** Exclusion noted in BOE Section 2.2

---

### A-1635: Valve Coating and Painting (External)

**Statement:** External valve coating/painting **excluded** from PKG-16 (covered in PKG-26 Protective Coatings & Painting)

**Why Needed:** Coating scope boundary between packages

**Basis:**
- Stainless steel valves: Typically unpainted (corrosion-resistant material)
- If carbon steel valves used (utilities): External coating per PKG-26 scope
- Valve internal coatings (if required): Vendor-applied (included in valve supply cost)

**Impacted WBS/CBS:** MAT (if coating included in PKG-16)

**Cost Impact:** None (external coating in PKG-26; internal coating in valve supply)

**Range:** If external coating in PKG-16: add $10k-$25k

**Confidence:** MEDIUM

**Resolution Path:** Confirm coating scope split between PKG-16 and PKG-26

**Reference:** Exclusion noted in BOE

---

### A-1636: Valve Nameplate and Identification

**Statement:** Valve nameplates and tags **included** in valve supply cost (no separate allowance)

**Why Needed:** Nameplate/tagging scope allocation

**Basis:**
- Manufacturer nameplates: Included in valve supply (standard practice)
- Field identification tags: Typically low cost (~$5-10 per tag)
- 220 valves @ $8 avg = $1,760 (minimal impact; included in valve supply allowances)

**Impacted WBS/CBS:** MAT (valve nameplates)

**Cost Impact:** Nameplates ~$2k (included in valve allowances)

**Confidence:** HIGH

**Resolution Path:** N/A (standard practice)

**Reference:** Included in valve material allowances

---

### A-1637: Valve Storage and Preservation (Pre-Installation)

**Statement:** Valve storage and preservation **included in CI (Construction Indirects)** factor

**Why Needed:** No laydown plan; valve delivery vs installation schedule TBD

**Basis:**
- Valve delivery-to-installation lag: Typically 2-6 months (early delivery for long-lead items)
- Storage requirements: Covered, secured laydown area; preservation checks
- Storage cost: Included in CI overhead (temporary facilities and site management)
- No separate storage line

**Impacted WBS/CBS:** CI (material storage overhead)

**Cost Impact:** Storage overhead included in CI = 18% × CD

**Range:** If dedicated valve storage required: add $5k-$15k

**Confidence:** MEDIUM

**Resolution Path:** Provide logistics plan or material management plan with storage requirements

**Reference:** Included in CI factor (D-1608)

---

### A-1638: Environmental Conditions (Coastal Marine Atmosphere)

**Statement:** Valve materials and coatings suitable for **C4/C5-M corrosion category** (coastal marine environment)

**Why Needed:** No environmental classification study; corrosion category TBD

**Basis:**
- Location: Fraser Surrey Terminal (active marine terminal, Fraser River)
- ISO 12944 corrosion categories: C4 (high industrial/coastal), C5-M (very high marine)
- Material impact: Stainless steel preferred (per A-1603); external components require corrosion-resistant materials

**Impacted WBS/CBS:** MAT (material selection premium)

**Cost Impact:** SS material selection addresses corrosion (no additional coating required for SS)

**Confidence:** MEDIUM

**Resolution Path:** Obtain environmental classification study or coating specification (PKG-26)

**Reference:** Supports A-1603 (SS material selection)

---

### A-1639: Hazardous Area Classification Impact on Actuators

**Statement:** Actuators and accessories rated for **Class I, Division 2 / Zone 2** (Group D) hazardous area (estimated)

**Why Needed:** No hazardous area classification study; electrical area classification TBD

**Basis:**
- Canola oil: Flammable liquid (flash point ~325°C; low fire risk but still classified)
- Typical classification: Class I, Division 2 or Zone 2 (not normally present; present under abnormal conditions)
- Actuator impact: Explosion-proof or purged enclosures for electric actuators; increased cost ~10-20%
- Pneumatic actuators: Typically intrinsically safe (minimal cost impact)

**Impacted WBS/CBS:** MAT (electric actuators)

**Cost Impact:** Hazardous area rating adds ~$30k-$60k to electric actuator cost (22 units @ $1.5k-3k premium each)

**Range:** If non-hazardous (unclassified): reduce cost ~$45k; if Class I, Division 1 / Zone 1: increase cost ~$80k

**Confidence:** LOW

**Resolution Path:** Obtain hazardous area classification study or electrical area classification drawings

**Reference:** Included in electric actuator unit costs (A-1606, A-1626)

---

### A-1640: Valve Installation Access and Rigging Constraints

**Statement:** Valve installation assumes **standard site access** (no major rigging constraints)

**Why Needed:** No site layout; no construction execution plan with access constraints

**Basis:**
- Location: Fraser Surrey Terminal (active marine terminal; operational constraints)
- Valve locations: Process areas, tank farm, railcar area, marine loading platform
- Access: Assume standard crane access; no confined space or height restrictions for valve installation
- Productivity impact: Terminal operations may require off-shift work or access coordination (risk R-1607)

**Impacted WBS/CBS:** CD (installation productivity and equipment)

**Cost Impact:** Standard productivity assumed (per A-1607); operational constraints risk in contingency

**Range:** If major access constraints (confined space, working at height, limited crane access): increase CD cost 10-25%

**Confidence:** MEDIUM

**Resolution Path:** Provide site layout, construction execution plan, or operational interface constraints

**Reference:** Risk R-1607 (terminal operations interface)

---

### A-1641: Valve Vendor Quality Requirements (API/ASME Compliance)

**Statement:** All valves comply with **API/ASME/CSA standards** (premium quality; not economy-grade)

**Why Needed:** No vendor qualification requirements; quality level TBD

**Basis:**
- Relief valves: ASME Section VIII required (pressure vessel code compliance)
- Isolation valves: API 600/608/609 typical for process facilities
- Control valves: IEC 60534 / ISA-75 series typical
- CSA B51: Mandatory in BC for pressure equipment
- Premium quality vs. economy-grade: ~15-30% cost premium

**Impacted WBS/CBS:** MAT (valve quality level)

**Cost Impact:** API/ASME quality level assumed in unit costs (per A-1606)

**Range:** If economy-grade acceptable: reduce cost ~20% ($264k savings); if higher quality (DNV, NACE): increase cost ~15% ($198k)

**Confidence:** MEDIUM (API/ASME typical for EPC projects; ER requirements TBD)

**Resolution Path:** Confirm quality requirements in ER Volume 2 Part 2 or DEL-16.02 specification

**Reference:** Related to A-1606 (unit costs based on API/ASME quality)

---

### A-1642: Control System Integration (Positioner Protocol)

**Statement:** Control valve positioners use **HART protocol** (digital communication with DCS)

**Why Needed:** No control system architecture; no instrumentation specification (PKG-20)

**Basis:**
- Modern DCS: Typically HART or Foundation Fieldbus
- HART: Most common, lower cost than FF (~$500-1,000 difference per positioner)
- Foundation Fieldbus: Higher functionality, higher cost
- Assumption: HART baseline (conservative cost)

**Impacted WBS/CBS:** MAT (positioner cost)

**Cost Impact:** HART positioners assumed in control valve costs (A-1622)

**Range:** If Foundation Fieldbus required: add $15k-$30k (30 positioners @ $500-1k premium)

**Confidence:** MEDIUM

**Resolution Path:** Provide control system architecture (PKG-19) or instrumentation specification (PKG-20) with field device protocol

**Reference:** Related to A-1622 (positioner costs)

---

### A-1643: Valve Documentation and Manuals

**Statement:** Valve O&M manuals and documentation **included in valve supply cost** (no separate allowance)

**Why Needed:** Documentation deliverable scope (vendor-supplied vs Contractor-produced)

**Basis:**
- Vendor documentation: O&M manuals, parts lists, drawings included with valve supply (standard practice)
- Contractor documentation: DEL-16.01 through DEL-16.05 (covered in Engineering budget)
- No separate documentation line

**Impacted WBS/CBS:** MAT (vendor documentation included in valve cost)

**Cost Impact:** Vendor manuals included in valve supply; Contractor documentation in E (engineering)

**Confidence:** HIGH

**Resolution Path:** N/A (standard practice)

**Reference:** Supports E and MAT line items

---

### A-1644: Winterization Requirements (Low-Temperature Operation)

**Statement:** Valve winterization (heat trace, insulation) **excluded** from PKG-16 (covered in PKG-27 Winterization or PKG-28 Heat Tracing)

**Why Needed:** Winterization scope boundary; BC winter climate considerations

**Basis:**
- Fraser Surrey winter: -10°C to +5°C typical (occasional -15°C)
- Canola oil: High viscosity at low temperature; product lines likely heat-traced
- Valve winterization: Heat trace, insulation for outdoor valves (scope likely PKG-27 or PKG-28)
- PKG-16 scope: Valve supply and installation only

**Impacted WBS/CBS:** MAT (if winterization included in PKG-16)

**Cost Impact:** None (winterization in PKG-27/28)

**Range:** If winterization in PKG-16: add $30k-$60k (heat trace, insulation for outdoor valves)

**Confidence:** MEDIUM

**Resolution Path:** Clarify winterization scope boundary between PKG-16, PKG-27, PKG-28

**Reference:** Exclusion noted in BOE

---

### A-1645: Valve Acceptance Testing (FAT/SAT)

**Statement:** Valve factory acceptance testing (FAT) **included in valve supply cost**; site acceptance testing (SAT) **included in COM factor**

**Why Needed:** FAT/SAT scope and cost allocation TBD

**Basis:**
- FAT: Vendor shop test per API 598, API 527, IEC 60534-4 (included in valve cost)
- SAT: Field functional testing and acceptance (included in commissioning labor)
- Witness costs: If Contractor witness required at vendor FAT → add travel/labor (TBD)

**Impacted WBS/CBS:** MAT (FAT in valve cost), COM (SAT in commissioning)

**Cost Impact:** FAT included in valve cost; SAT included in COM factor

**Range:** If witness FAT required for critical valves: add $15k-$35k (travel, labor for 5-10 FAT trips)

**Confidence:** MEDIUM

**Resolution Path:** Confirm FAT witness requirements in quality plan or valve procurement specification

**Reference:** Supports A-1624 (relief valve FAT), A-1615 (testing in COM)

---

### A-1646: Valve Warranty and Defects Liability

**Statement:** Valve warranty (typically 12-24 months) and defects liability **excluded** from PKG-16 estimate (covered in PKG-35 Defects Liability or separate)

**Why Needed:** Warranty scope allocation; defects period cost TBD

**Basis:**
- Standard valve warranty: 12-24 months from commissioning
- Defects liability period: Typically 12-24 months after substantial completion
- Warranty/defects costs: Typically separate from initial procurement/installation (PKG-35 scope)

**Impacted WBS/CBS:** N/A (warranty excluded)

**Cost Impact:** None (warranty in PKG-35)

**Range:** If warranty included in PKG-16: add $20k-$50k (valve defect rectification allowance)

**Confidence:** MEDIUM

**Resolution Path:** Confirm defects liability scope in contract or PKG-35 deliverables

**Reference:** Exclusion noted in BOE

---

## Assumption Summary Statistics

| Metric | Count |
|--------|-------|
| Total assumptions | 46 |
| Quantity/count assumptions | 12 |
| Pricing/cost assumptions | 15 |
| Scope/boundary assumptions | 8 |
| Quality/specification assumptions | 6 |
| Schedule/duration assumptions | 2 |
| Exclusion clarifications | 3 |

## Assumptions by Cost Impact (Descending)

| Assumption | Description | Cost Impact | Confidence |
|------------|-------------|-------------|------------|
| A-1601 | Valve count (220 valves) | $1,790k | LOW |
| A-1606 | Valve unit costs (typical BC rates) | $1,320k | LOW |
| A-1613 | Engineering hours (3,400 hours) | $527k | MEDIUM |
| A-1603 | Stainless steel material selection | +$530k premium | MEDIUM |
| A-1608 | Valve type ratio (13% control, 68% isolation) | Mix impact ~$300k | LOW |
| A-1626 | Actuator costs | $660k | LOW |
| A-1607 | Installation productivity (6 hrs/valve avg) | $125k | MEDIUM |
| A-1622 | Control valve accessories (positioners) | $158k | MEDIUM |
| A-1605 | Control valve complexity mix | ~$60k premium | LOW |

---

**Assumptions Log Prepared By:** Estimating Agent
**Date:** 2026-01-28
**Status:** Complete (46 assumptions recorded)
