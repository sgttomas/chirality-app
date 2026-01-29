# Risk Register — PKG-16 Valves & Specialty Equipment

**Snapshot ID:** EST_PKG16_DRAFT_2026-01-28_2347
**Package:** PKG-16 Valves & Specialty Equipment
**Date:** 2026-01-28

---

## Purpose

This register identifies risks affecting the estimate accuracy and cost certainty for PKG-16, along with suggested mitigations and contingency handling.

---

## Risk Entries

### R-1601: Valve Quantity Uncertainty (Scope Risk)

**Risk Driver:** Scope / Quantity

**Cause:** No P&IDs available; valve count estimated parametrically at 220 units

**Consequence:** Actual valve count may differ significantly from estimate
- Underestimate: If actual count 260+ valves (+18%), cost increase ~$360k-$500k
- Overestimate: If actual count 180 valves (-18%), cost decrease ~$320k-$420k

**Affected Buckets:**
- MAT (valve equipment cost scales linearly with count)
- CD (installation labor scales with count)
- P, PM, COM (indirects scale with MAT and CD)

**Suggested Mitigation:**
1. Complete P&IDs for PKG-10 (railcar unloading), PKG-11 (marine loading), PKG-12 (product transfer), PKG-13 (storage tanks)
2. Develop preliminary valve list with tag numbers and service assignments
3. Coordinate with process and piping teams to validate valve interface requirements
4. Re-estimate when valve count confirmed (expected accuracy improvement: -10% / +15%)

**Contingency Handling:**
- Base estimate uses parametric count (220 valves)
- Contingency (25-30% on MAT and CD) provides buffer for ±20% count variability
- If count exceeds +20%: additional contingency drawdown or change order required

**Probability:** HIGH (no P&IDs; count highly uncertain)

**Impact:** HIGH ($320k-$500k potential variance)

---

### R-1602: Valve Size and Specification Risk (Scope/Price Risk)

**Risk Driver:** Scope / Quantity / Price

**Cause:** No piping line list; valve sizes estimated using distribution assumption (60% small, 30% medium, 10% large)

**Consequence:** Actual valve size mix may differ from estimate
- Larger valves (shift to 40% medium, 20% large): Cost increase ~$250k-$400k
- Smaller valves (shift to 75% small, 20% medium): Cost decrease ~$150k-$250k

**Affected Buckets:**
- MAT (valve cost scales significantly with size; large valves 5-10× small valves)
- CD (large valve installation requires more labor and crane time)

**Suggested Mitigation:**
1. Complete piping line list (PKG-14) with line sizes and pressure classes
2. Complete DEL-16.04 valve datasheets with actual valve sizes
3. Obtain vendor budgetary quotes for actual valve list (by size and type)
4. Re-estimate when sizes confirmed

**Contingency Handling:**
- Base estimate uses typical size distribution for transload facilities
- Contingency (25% MAT, 30% CD) provides buffer for moderate size mix changes
- If large valve count increases significantly: additional contingency or change order

**Probability:** MEDIUM (size distribution typical for transload; actual mix TBD)

**Impact:** MEDIUM ($150k-$400k potential variance)

---

### R-1603: Stainless Steel Material Premium Risk (Price Risk)

**Risk Driver:** Price / Specification

**Cause:** Valve material assumed 316SS stainless steel for food-grade service; specification not finalized

**Consequence:** Material selection changes affect cost
- If carbon steel acceptable (with coatings): Cost decrease ~$530k (-32% MAT cost)
- If upgraded alloys required (duplex, super-duplex for corrosion): Cost increase ~$250k-$400k (+15-25% MAT cost)

**Affected Buckets:**
- MAT (material premium 2-3× for SS vs CS; 3-5× for duplex vs SS)
- CD (minimal impact; installation labor similar)

**Suggested Mitigation:**
1. Extract material requirements from ER Volume 2 Part 2 (Mechanical specifications)
2. Complete DEL-16.02 valve specification with actual material selections
3. Confirm food-grade cleanliness requirements and coastal corrosion environment
4. Obtain vendor quotes for specified materials
5. Consider lifecycle cost (SS reduces maintenance vs. CS with coatings)

**Contingency Handling:**
- Base estimate uses 316SS (conservative for food-grade + coastal environment)
- If CS acceptable: savings reallocated or contingency reduction
- If upgraded alloys required: contingency drawdown or scope clarification

**Probability:** LOW (SS appropriate for canola oil + coastal environment; unlikely to downgrade)

**Impact:** HIGH ($250k-$530k potential variance)

---

### R-1604: Control Valve Complexity and Trim Selection Risk (Scope/Price Risk)

**Risk Driver:** Scope / Price

**Cause:** Control valve complexity (standard, ball/butterfly, severe service) estimated at 50%-30%-20% mix; actual trim requirements TBD pending sizing calculations

**Consequence:** Control valve costs vary significantly with complexity
- More severe service valves (cavitation, noise control): Cost increase ~$90k-$150k
- All standard valves (no severe service): Cost decrease ~$60k-$100k

**Affected Buckets:**
- MAT (severe service valves 2-3× standard due to special trim, materials, testing)

**Suggested Mitigation:**
1. Complete DEL-16.03 control valve sizing calculations (Cv, pressure drop, cavitation assessment)
2. Identify severe service applications (high pressure drop, flashing, cavitation risk)
3. Complete DEL-16.04 control valve datasheets with trim types
4. Obtain vendor quotes for actual valve specifications (standard vs severe service pricing)

**Contingency Handling:**
- Base estimate uses weighted average complexity mix
- Contingency (25% MAT) provides buffer for complexity changes
- Severe service valves typically identified during detailed design (60-90% stage)

**Probability:** MEDIUM (some severe service likely; extent TBD)

**Impact:** MEDIUM ($60k-$150k potential variance)

---

### R-1605: Actuator and Automation Requirements Risk (Scope/Price Risk)

**Risk Driver:** Scope / Price

**Cause:** Actuator distribution (60% manual, 30% pneumatic, 10% electric) estimated without control philosophy or P&IDs

**Consequence:** Automation level changes affect cost significantly
- More automation (40% pneumatic, 20% electric): Cost increase ~$250k-$350k
- Less automation (20% pneumatic, 5% electric): Cost decrease ~$300k-$400k

**Affected Buckets:**
- MAT (actuators add $3k-$40k per valve; positioners add $2k-$5k)
- CD (actuated valves require pneumatic/electrical hookup; +2-4 hours labor per valve)

**Suggested Mitigation:**
1. Develop control philosophy document (automation strategy, ESD requirements)
2. Complete P&IDs with valve actuation symbols (hand, pneumatic, electric)
3. Coordinate with PKG-19 (control systems) for ESD valve requirements
4. Coordinate with PKG-17 (electrical) and PKG-20 (instrumentation) for actuation power/control
5. Re-estimate when actuation requirements defined

**Contingency Handling:**
- Base estimate uses typical transload automation level (moderate automation)
- Contingency (25-30%) provides buffer for moderate automation changes
- If full automation required (safety, operational efficiency): significant cost increase likely exceeds contingency

**Probability:** MEDIUM (automation level TBD; typical transload uses moderate automation)

**Impact:** HIGH ($250k-$400k potential variance)

---

### R-1606: Vendor Pricing Variability (Price Risk)

**Risk Driver:** Price

**Cause:** No vendor quotes; all pricing based on typical market rates (allowances)

**Consequence:** Actual vendor pricing may differ from allowance estimates
- Competitive bidding, favorable market: Cost decrease ~10-20% ($168k-$336k)
- Single-source, unfavorable market, specialty valves: Cost increase ~15-30% ($252k-$504k)
- Vendor quote vs. allowance variability typical: -15% / +25%

**Affected Buckets:**
- MAT (valve and actuator pricing)
- P (procurement services scale with MAT)

**Suggested Mitigation:**
1. Obtain budgetary quotes from multiple valve vendors (Fisher, Emerson, Valmet for control; Velan, Tyco for isolation; Crosby, Farris for relief)
2. Conduct vendor market survey (3-5 vendors per category)
3. Include pricing validity period in quotes (inflation protection)
4. Consider preferred vendor programs or standing agreements (DP World Fraser Surrey Terminal may have existing vendor relationships)
5. Re-estimate when quotes obtained (expected accuracy improvement: -10% / +15%)

**Contingency Handling:**
- Contingency (25% MAT) sized for no-quote uncertainty
- Vendor quotes typically reduce contingency to 10-15% MAT
- If quotes exceed allowances by >20%: contingency drawdown or scope review

**Probability:** MEDIUM (vendor pricing variability typical; material markets relatively stable Q1 2026)

**Impact:** MEDIUM-HIGH ($170k-$500k potential variance)

---

### R-1607: Site Access and Operational Interface Risk (Productivity Risk)

**Risk Driver:** Productivity / Schedule

**Cause:** Fraser Surrey Terminal is an active marine terminal; valve installation in operational areas may require coordination, off-shift work, or access restrictions

**Consequence:** Productivity impacts
- Operational coordination delays: Schedule slip 10-20% (8-12 weeks → 9-14 weeks)
- Off-shift work premium: Labor cost increase 10-25% ($17k-$41k)
- Access restrictions (crane, rigging): Equipment cost increase or workarounds required

**Affected Buckets:**
- CD (installation labor and equipment)
- CI (extended site supervision)

**Suggested Mitigation:**
1. Coordinate with DP World Fraser Surrey Terminal operations team (operational windows, access constraints)
2. Develop detailed construction execution plan (shift work, crane access, traffic management)
3. Include terminal coordination meetings in schedule
4. Pre-order long-lead valves to avoid critical path delays
5. Consider phased installation (by system or area) to minimize operational impact

**Contingency Handling:**
- Base estimate uses standard productivity (no off-shift premium)
- Contingency (30% CD, 30% CI) includes buffer for operational interface
- If major off-shift work required: contingency drawdown or schedule adjustment

**Probability:** MEDIUM-HIGH (active terminal; coordination required)

**Impact:** MEDIUM ($17k-$60k; primarily schedule risk)

---

### R-1608: Relief Valve Set Pressure and Protected Equipment Coordination Risk (Interface Risk)

**Risk Driver:** Interface / Scope

**Cause:** Relief valve sizing requires protected equipment MAWP data (tanks, vessels, piping); PKG-13 tank datasheets and other equipment specs not available

**Consequence:** Relief valve counts and sizes may change
- Underestimate relief count (missing protection scenarios): Add 5-10 relief valves → $34k-$80k
- Overestimate (consolidated protection, larger orifices): Reduce 3-5 relief valves → savings $20k-$40k
- Orifice size changes: -20% / +40% cost variance per valve

**Affected Buckets:**
- MAT (relief valves)
- CD (relief valve installation)
- E (DEL-16.03 relief calculations)

**Suggested Mitigation:**
1. Coordinate with PKG-13 (storage tanks) for tank MAWP and relief requirements
2. Complete DEL-16.03 relief valve sizing calculations per API 520/521
3. Obtain PKG-10/PKG-11/PKG-12 equipment datasheets with pressure relief requirements
4. Conduct HAZOP (DEL-27.02) to identify all overpressure scenarios requiring relief
5. Re-estimate relief valve scope when protected equipment defined

**Contingency Handling:**
- Base estimate: 20 relief valves (3 tank, 8 pump, 9 thermal per A-1609)
- Contingency (25% MAT) provides buffer for ±25% relief valve count/size changes
- If major relief scope increase (HAZOP findings): contingency drawdown or scope change

**Probability:** MEDIUM (relief valve count may vary; tank relief certain; pump/thermal relief TBD)

**Impact:** MEDIUM ($20k-$80k potential variance)

---

### R-1609: Control Valve Positioner and Communication Protocol Risk (Price/Interface Risk)

**Risk Driver:** Price / Interface

**Cause:** Control valve positioner protocol assumed HART (lower cost); actual protocol TBD pending PKG-19 (control systems) and PKG-20 (instrumentation) specifications

**Consequence:** Communication protocol changes affect cost
- Foundation Fieldbus (vs. HART): Cost increase ~$500-$1,000 per positioner → $15k-$30k total (30 valves)
- Profibus, Modbus, or proprietary protocol: Cost variability -$200 to +$1,500 per positioner
- If analog (4-20 mA only, no digital): Cost decrease ~$1,500-$2,500 per positioner → $45k-$75k savings

**Affected Buckets:**
- MAT (control valve positioners)

**Suggested Mitigation:**
1. Coordinate with PKG-19 (control systems) for DCS/PLC communication architecture
2. Complete instrumentation specification (PKG-20) with field device protocol requirements
3. Obtain vendor quotes for positioners with actual protocol specified
4. Consider lifecycle cost (smart positioners enable remote diagnostics and predictive maintenance)

**Contingency Handling:**
- Base estimate uses HART (most common; mid-range cost)
- Contingency (25% MAT) covers protocol variability
- If Foundation Fieldbus required: contingency drawdown ~$15k-$30k

**Probability:** LOW-MEDIUM (HART very common; Foundation Fieldbus higher performance but higher cost)

**Impact:** LOW-MEDIUM ($15k-$75k potential variance)

---

### R-1610: Hazardous Area Classification Impact (Price Risk)

**Risk Driver:** Price / Specification

**Cause:** Hazardous area classification assumed Class I, Division 2 / Zone 2; actual classification TBD pending area classification study

**Consequence:** Area classification affects actuator and accessory specifications
- Non-hazardous (unclassified): Cost decrease ~$30k-$60k (no explosion-proof enclosures)
- Class I, Division 1 / Zone 1: Cost increase ~$60k-$120k (higher certification level)
- Pneumatic actuators: Minimal impact (intrinsically safe)
- Electric actuators (22 units): Significant impact ($1.5k-$5k premium per actuator for Div 1/Zone 1)

**Affected Buckets:**
- MAT (electric actuators and accessories)

**Suggested Mitigation:**
1. Obtain hazardous area classification study for facility
2. Coordinate with PKG-17 (electrical) for area classification drawings
3. Complete DEL-16.02 specification with actual actuator enclosure requirements
4. Obtain vendor quotes for actuators with actual area classification specified

**Contingency Handling:**
- Base estimate assumes Div 2 / Zone 2 (moderate premium included)
- Contingency (25% MAT) covers classification variability
- If Div 1 / Zone 1: contingency drawdown ~$60k-$120k

**Probability:** MEDIUM (some process areas likely classified; extent TBD)

**Impact:** MEDIUM ($30k-$120k potential variance)

---

### R-1611: Installation Productivity Risk (Productivity Risk)

**Risk Driver:** Productivity

**Cause:** Installation productivity assumed standard (6 hours avg per valve); site-specific constraints TBD

**Consequence:** Productivity impacts
- Favorable (experienced crew, good access, pre-fabrication): Reduce labor 15-20% → savings $25k-$33k
- Unfavorable (access constraints, coordination delays, rework): Increase labor 20-40% → cost increase $33k-$66k

**Affected Buckets:**
- CD (installation labor)
- CI (extended field supervision if productivity lower)

**Suggested Mitigation:**
1. Obtain construction manager's productivity estimate for valve installation at marine terminals
2. Review historical data from similar projects (transload facilities, active terminal environments)
3. Include valve pre-assembly where possible (actuator mounting, accessory installation in shop vs. field)
4. Plan installation sequence to minimize rework and coordination delays
5. Conduct mock-up installation for complex valves (large MOVs, control valve assemblies)

**Contingency Handling:**
- Base estimate uses typical productivity (A-1607: 4-12 hrs per valve by size)
- Contingency (30% CD) sized for productivity variability
- If major productivity issues: contingency drawdown or schedule extension

**Probability:** MEDIUM (site-specific constraints TBD; active terminal may impact productivity)

**Impact:** MEDIUM ($25k-$66k potential variance)

---

### R-1612: Vendor Lead Time and Availability Risk (Schedule/Price Risk)

**Risk Driver:** Schedule / Price

**Cause:** Valve lead times vary by type and supplier; long-lead items may drive schedule or require expediting

**Consequence:** Lead time impacts
- Standard valves: 8-16 weeks typical (minimal impact)
- Control valves with smart positioners: 12-20 weeks (moderate impact)
- Large MOVs, specialty valves, API 526 relief valves: 16-24 weeks (long-lead)
- If late order or supply chain delays: Expediting cost ~5-15% of valve cost → $84k-$252k

**Affected Buckets:**
- MAT (expediting fees)
- P (increased procurement management)
- Schedule (critical path if valves delay installation)

**Suggested Mitigation:**
1. Identify long-lead valves early (large MOVs, control valves, relief valves)
2. Issue Request for Quotation (RFQ) early to confirm lead times
3. Place purchase orders for long-lead items before detailed design complete (based on preliminary datasheets)
4. Maintain communication with vendors for delivery schedule updates
5. Include expediting allowance in procurement budget if schedule is aggressive

**Contingency Handling:**
- Base estimate assumes normal lead times (no expediting)
- P factor (2% MAT) includes standard procurement coordination
- If expediting required: contingency drawdown or separate expediting allowance
- Schedule risk managed separately (not in cost estimate)

**Probability:** MEDIUM (some long-lead valves likely; supply chain stable Q1 2026)

**Impact:** MEDIUM ($0-$252k if expediting required; primarily schedule risk)

---

### R-1613: Actuator Sizing and Safety Factor Risk (Scope Risk)

**Risk Driver:** Scope / Quantity

**Cause:** Actuator sizing requires torque calculations (DEL-16.03); no calculations available; actuator sizes estimated

**Consequence:** Undersized or oversized actuators
- Undersized: Actuators cannot operate valves; replace/upgrade required → $50k-$150k
- Oversized: Cost premium for unnecessarily large actuators → $30k-$80k
- Typical safety factor: 1.5-2.0× required torque; higher factors increase cost

**Affected Buckets:**
- MAT (actuator cost scales with size/torque output)
- CD (actuator replacement labor if undersized)

**Suggested Mitigation:**
1. Complete DEL-16.03 actuator sizing calculations (breakaway torque, running torque, packing friction)
2. Apply appropriate safety factors (1.5× minimum; 2.0× for critical service)
3. Verify valve manufacturer torque data vs. calculated torque
4. Conduct actuator sizing review (independent check)
5. Specify actuator testing during FAT (confirm torque output meets requirements)

**Contingency Handling:**
- Base estimate uses typical actuator sizes for valve sizes (per A-1626)
- Contingency (25% MAT) covers actuator sizing variability
- If undersized actuators discovered late: contingency drawdown or rework cost

**Probability:** LOW (actuator oversizing common practice; undersizing rare with proper safety factors)

**Impact:** MEDIUM ($30k-$150k potential variance; rework risk if undersized)

---

### R-1614: Relief Valve Scenario Identification Risk (Scope Risk)

**Risk Driver:** Scope

**Cause:** Relief valve count (20 units) estimated before HAZOP (DEL-27.02) and detailed process design; actual overpressure scenarios TBD

**Consequence:** HAZOP may identify additional relief requirements
- Additional relief scenarios (blocked discharge, runaway reactions, utility failures): Add 3-8 relief valves → $20k-$64k
- Consolidated relief (multiple scenarios protected by single larger relief): Reduce 2-4 relief valves → savings $13k-$32k

**Affected Buckets:**
- MAT (relief valves)
- E (DEL-16.03 additional relief calculations)
- CD (relief valve installation)

**Suggested Mitigation:**
1. Conduct preliminary HAZOP (DEL-27.02) or hazard identification workshop
2. Complete DEL-16.03 relief valve sizing for all credible overpressure scenarios per API 521
3. Coordinate with process team (PKG-10, PKG-11, PKG-12, PKG-13) for relief scenarios
4. Review relief valve requirements in ER Volume 2 Part 2
5. Re-estimate when HAZOP complete and relief valve list finalized

**Contingency Handling:**
- Base estimate: 20 relief valves (typical for facility type per A-1609)
- Contingency (25% MAT, 20% E) provides buffer for relief scope changes
- HAZOP typically identifies 0-5 additional relief valves (covered by contingency)

**Probability:** MEDIUM (HAZOP may identify additional scenarios; typical range ±25% relief count)

**Impact:** LOW-MEDIUM ($13k-$64k potential variance)

---

### R-1615: Strainer and Specialty Equipment Scope Ambiguity (Scope Risk)

**Risk Driver:** Scope

**Cause:** "Specialty items" in PKG-16 scope not defined; strainer count estimated; check valves included as specialty

**Consequence:** Specialty equipment scope changes
- Additional specialty (pressure regulators, special service valves, filters): Add $50k-$150k
- Fewer specialty (check valves in piping package PKG-14): Reduce $30k-$62k

**Affected Buckets:**
- MAT (specialty equipment)
- CD (installation if additional equipment)

**Suggested Mitigation:**
1. Clarify "specialty items" scope in PKG-16 vs. other packages (PKG-14 piping, PKG-20 instrumentation)
2. Complete P&IDs with specialty equipment identified and tagged
3. Review ER requirements for specialty equipment (pressure regulators, nitrogen blanketing valves, etc.)
4. Coordinate with process team for specialty equipment requirements
5. Re-estimate when specialty scope clarified

**Contingency Handling:**
- Base estimate: 20 check valves included; other specialty excluded (per D-1625)
- Contingency (25% MAT) provides buffer for specialty scope additions
- If major specialty scope (e.g., 20+ pressure regulators): may exceed contingency

**Probability:** MEDIUM (specialty scope ambiguous; check valves likely correct; other specialty TBD)

**Impact:** MEDIUM ($30k-$150k potential variance)

---

### R-1616: Material Escalation Risk (Price Risk)

**Cause:** Estimate in January 2026 dollars; no escalation applied; material costs subject to inflation over project duration

**Consequence:** Escalation impacts (if project duration 2-3 years)
- Stainless steel: Historical escalation 3-6% per year
- Actuators and instrumentation: Historical escalation 2-4% per year
- Weighted average: ~3-5% per year
- 2-year exposure: ~$100k-$168k escalation on $1,678k MAT
- 3-year exposure: ~$151k-$252k escalation

**Affected Buckets:**
- MAT (materials escalation)
- CD (labor escalation separate; typically 2-3% per year)

**Suggested Mitigation:**
1. Obtain construction schedule with procurement and installation milestones
2. Develop escalation forecast by CBS bucket with expenditure curve (cashflow)
3. Consider fixed-price quotes with extended validity (6-12 months)
4. Place purchase orders for long-lead valves early to lock pricing
5. Include escalation allowance if schedule >18 months

**Contingency Handling:**
- Base estimate: No escalation (January 2026 pricing per D-1609)
- Escalation risk noted; not included in contingency
- If escalation included: add 3-6% of MAT and CD per year of exposure

**Probability:** MEDIUM-HIGH (project duration likely 2-3 years; escalation likely)

**Impact:** MEDIUM ($100k-$252k over 2-3 years; manageable with early procurement)

---

### R-1617: Engineering Scope Creep Risk (Scope Risk)

**Risk Driver:** Scope

**Cause:** Engineering hours estimated at 3,400 hours; actual effort may increase due to design complexity, revisions, vendor coordination

**Consequence:** Engineering overrun
- Design complexity (severe service valves, special applications): Add 10-20% hours → $53k-$105k
- Multiple design revisions (P&ID changes, ER clarifications): Add 15-30% hours → $79k-$158k
- Favorable (simple design, vendor standard selections): Reduce 10-15% hours → savings $53k-$79k

**Affected Buckets:**
- E (engineering hours)
- PM (engineering management scales with E)

**Suggested Mitigation:**
1. Freeze P&IDs and process design before starting detailed valve design (minimize rework)
2. Use vendor standard valve selections where possible (minimize custom engineering)
3. Conduct early vendor engagement (technical workshops to confirm selections)
4. Implement design change control process (limit scope creep)
5. Track engineering hours by deliverable and flag variances early

**Contingency Handling:**
- Base estimate: 3,400 hours (per A-1613; typical for valve package)
- Contingency (20% E) provides buffer for scope and revision uncertainty
- If major scope increase: contingency drawdown or fee adjustment

**Probability:** MEDIUM (design scope creep common; extent depends on design freeze discipline)

**Impact:** MEDIUM ($53k-$158k potential variance)

---

### R-1618: Testing and Commissioning Scope Risk (Scope Risk)

**Risk Driver:** Scope

**Cause:** Commissioning scope (DEL-16.05) estimated using COM factor (3% of CD+CI+MAT); actual testing requirements TBD

**Consequence:** Testing scope changes
- Extensive testing (vendor FAT witness, third-party inspection, special performance tests): Add $30k-$80k
- Minimal testing (vendor self-certification, no field tests): Reduce $15k-$30k
- Relief valve field set pressure testing (if required vs. vendor FAT only): Add $15k-$30k

**Affected Buckets:**
- COM (commissioning and testing labor)

**Suggested Mitigation:**
1. Complete DEL-16.05 test procedures with test scope, acceptance criteria, duration
2. Clarify FAT witness requirements in quality plan (critical valves only vs. all valves)
3. Coordinate with commissioning team for test schedule and resource requirements
4. Review ER requirements for valve testing and acceptance
5. Re-estimate commissioning when test plan finalized

**Contingency Handling:**
- Base estimate: COM factor 3% (typical for valve testing per A-1615)
- Contingency (35% COM due to 100% parametric) provides buffer for testing scope variability
- If extensive testing: contingency drawdown or separate testing allowance

**Probability:** MEDIUM (testing scope TBD; factor-based estimate typical)

**Impact:** MEDIUM ($15k-$80k potential variance)

---

### R-1619: Currency Exchange Risk (if applicable)

**Risk Driver:** Price

**Cause:** Estimate in CAD; some vendors may quote in USD (US valve manufacturers)

**Consequence:** Currency exchange rate fluctuations
- CAD/USD exchange rate (current ~1.40 CAD per USD assumed)
- If CAD weakens (1.45-1.50): Cost increase ~3-7% on USD-quoted valves
- If CAD strengthens (1.30-1.35): Cost decrease ~4-8% on USD-quoted valves
- Assume 50% of valves sourced from US vendors: exposure ~$420k USD → ±$17k-$59k CAD variance

**Affected Buckets:**
- MAT (valve and actuator procurement)

**Suggested Mitigation:**
1. Request vendor quotes in CAD where possible
2. Include currency exchange assumptions in procurement contracts
3. Consider currency hedging for large USD purchases (if project risk management includes hedging)
4. Monitor CAD/USD exchange rate during procurement period
5. Update estimate when vendor quotes obtained with confirmed currency

**Contingency Handling:**
- Base estimate: All costs in CAD (per D-1602)
- Currency risk not explicitly included in contingency
- Contingency (25% MAT) provides partial buffer for currency fluctuations

**Probability:** LOW-MEDIUM (currency fluctuations typical; CAD/USD relatively stable)

**Impact:** LOW ($17k-$59k potential variance)

---

### R-1620: Winter Construction Productivity Impact (Productivity Risk)

**Risk Driver:** Productivity / Schedule

**Cause:** Fraser Surrey BC winter climate (-10°C to +5°C); valve installation may occur in winter months

**Consequence:** Winter productivity impacts
- Cold weather: Reduced labor productivity 10-20% (bolt-up, gasket handling, testing)
- Freeze protection: Winterization measures during installation (heaters, enclosures)
- Weather delays: Schedule slip increases indirects (CI extended duration)

**Affected Buckets:**
- CD (labor productivity)
- CI (extended duration)

**Suggested Mitigation:**
1. Schedule valve installation for shoulder seasons (spring/fall) if possible
2. Include winter construction plan (heated enclosures, weather protection)
3. Use cold-weather gasket materials if winter installation required
4. Plan hydrostatic testing for non-freezing periods (or use glycol/methanol test fluids)
5. Include weather contingency in construction schedule

**Contingency Handling:**
- Base estimate uses standard productivity (no winter adjustment)
- Contingency (30% CD, 30% CI) provides buffer for weather-related productivity loss
- Winter construction allowance (if dedicated): $10k-$25k separate line (not included in base)

**Probability:** MEDIUM (installation timing TBD; winter work possible)

**Impact:** LOW-MEDIUM ($10k-$40k potential impact)

---

## Risk Summary Statistics

| Metric | Count |
|--------|-------|
| Total risks | 20 |
| Scope risks | 8 |
| Price risks | 6 |
| Productivity risks | 3 |
| Interface risks | 2 |
| Schedule risks | 1 |

## Risks by Impact (Descending)

| Risk ID | Description | Probability | Impact | Potential Variance |
|---------|-------------|-------------|--------|-------------------|
| R-1601 | Valve quantity uncertainty | HIGH | HIGH | -$320k / +$500k |
| R-1602 | Valve size mix variance | MEDIUM | MEDIUM | -$150k / +$400k |
| R-1603 | Stainless steel material premium | LOW | HIGH | -$530k / +$400k |
| R-1605 | Actuator/automation requirements | MEDIUM | HIGH | -$400k / +$350k |
| R-1606 | Vendor pricing variability | MEDIUM | MED-HIGH | -$168k / +$504k |
| R-1616 | Material escalation (2-3 years) | MED-HIGH | MEDIUM | +$100k-$252k |
| R-1617 | Engineering scope creep | MEDIUM | MEDIUM | -$79k / +$158k |
| R-1608 | Relief valve scope coordination | MEDIUM | MEDIUM | -$40k / +$80k |
| R-1618 | Testing/commissioning scope | MEDIUM | MEDIUM | -$30k / +$80k |
| R-1607 | Site access/operational interface | MED-HIGH | MEDIUM | +$17k-$60k |
| R-1610 | Hazardous area classification | MEDIUM | MEDIUM | -$60k / +$120k |
| R-1611 | Installation productivity | MEDIUM | MEDIUM | -$33k / +$66k |
| R-1615 | Specialty equipment scope | MEDIUM | MEDIUM | -$62k / +$150k |
| R-1604 | Control valve complexity | MEDIUM | MEDIUM | -$100k / +$150k |
| R-1612 | Vendor lead times/expediting | MEDIUM | MEDIUM | +$0-$252k |
| R-1609 | Positioner protocol | LOW-MED | LOW-MED | -$75k / +$30k |
| R-1619 | Currency exchange | LOW-MED | LOW | ±$17k-$59k |
| R-1620 | Winter construction | MEDIUM | LOW-MED | +$10k-$40k |

## Contingency Sizing Rationale

**Method:** PCT_BY_BUCKET with allowance-heavy adjustments (per D-1621)

**Allowance Share:** 100% (all line items ALLOWANCE or PARAMETRIC)

**Baseline Contingency Rates:**
- E: 10% baseline + 10% allowance adjustment = 20%
- MAT: 15% baseline + 10% allowance adjustment = 25%
- CD: 20% baseline + 10% allowance adjustment = 30%
- CI: 20% baseline + 10% allowance adjustment = 30%
- P: 10% baseline + 5% allowance adjustment = 15%
- PM: 10% baseline + 5% allowance adjustment = 15%
- COM: 25% baseline + 10% allowance adjustment = 35%

**Rationale for Elevated Contingency:**
1. No vendor quotes (pricing uncertainty)
2. Valve quantities parametric (scope uncertainty)
3. Valve sizes estimated (cost driver uncertainty)
4. Actuation requirements TBD (significant cost variability)
5. Material specifications TBD (SS premium vs. alternatives)
6. Active terminal site (productivity and access risk)
7. Multi-discipline interfaces (coordination risk)

**Contingency Adequacy:**
- Base estimate: $2,602,000 CAD
- Contingency: $625,000 CAD (24% overall)
- Total: $3,227,000 CAD

**Coverage Assessment:**
- Contingency covers combined impact of:
  - Valve count ±20% ($320k-$500k) → covered
  - Vendor pricing variability -15%/+25% ($252k-$420k) → partially covered
  - Actuation level changes ($250k-$350k) → partially covered
  - Material premium changes ($250k-$530k) → partially covered if downside; not if multiple upside risks combine

**Conclusion:** Contingency adequate for typical variance (single or dual moderate risks); insufficient if multiple high-impact risks materialize concurrently (e.g., valve count +20% AND vendor pricing +20% AND more automation); expect contingency drawdown 40-70% during detailed design/procurement

---

**Risk Register Prepared By:** Estimating Agent
**Date:** 2026-01-28
**Status:** Complete (20 risks identified)
