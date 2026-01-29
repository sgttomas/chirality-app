# Risk Register — PKG-17 Electrical Power Distribution

**Snapshot ID:** EST_PKG17_DRAFT_2026-01-28_0005
**Date:** 2026-01-28

---

This register identifies risks that could affect the estimate accuracy and provides suggested mitigation actions.

---

## R-1701: Actual Motor Loads Significantly Exceed Assumptions

**Risk Driver:** Scope / Quantity

**Cause → Consequence:**
- **Cause:** No load calculations exist; motor loads from PKG-10 (railcar unloading), PKG-11 (marine loading), PKG-13 (storage tanks), PKG-15 (pumps) are TBD
- **Consequence:** Transformer, switchgear, MCC, and cable sizing may be significantly undersized, requiring larger equipment and increased cable sizes

**Affected Buckets:** MAT (transformers, switchgear, MCCs, cables), CD (installation labor scales with equipment size)

**Probability:** Medium | **Impact:** Medium-High

**Potential Cost Impact:** +$150,000 to +$400,000 CAD

**Suggested Mitigation:**
1. Prioritize load calculations (DEL-17.03) early in design
2. Coordinate with equipment packages (PKG-10, PKG-11, PKG-13, PKG-15) to obtain motor schedules and load requirements
3. Include diversity factors and future load growth allowances in transformer sizing
4. Request vendor budgetary quotes for range of equipment sizes

**Contingency Handling:** Partially covered by 25% MAT contingency; may require additional scope change if loads exceed 50% of assumptions

---

## R-1702: Hazardous Area Classification Required

**Risk Driver:** Scope / Requirements

**Cause → Consequence:**
- **Cause:** ER requirements not yet extracted; hazardous area classification (Class I Div 2) may be required for railcar unloading area or tank farm areas due to flammable vapor hazards
- **Consequence:** Electrical equipment in hazardous areas must be rated (explosion-proof or purged enclosures), increasing equipment costs and installation complexity; cable and conduit sealing required

**Affected Buckets:** MAT (rated equipment premium), CD (installation complexity), E (additional calculations and area classification drawings)

**Probability:** Medium | **Impact:** Medium

**Potential Cost Impact:** +$100,000 to +$250,000 CAD

**Suggested Mitigation:**
1. Extract ER requirements for hazardous area classification requirements
2. Conduct area classification study early in design (may be part of DEL-27.01 Design Basis or DEL-17.03)
3. Coordinate with process safety team for vapor release scenarios
4. Obtain vendor quotes for both standard and rated equipment options

**Contingency Handling:** Covered by 25% contingency on MAT and 30% contingency on CD

---

## R-1703: Utility Service Voltage/Configuration Different Than Assumed

**Risk Driver:** Interface / Requirements

**Cause → Consequence:**
- **Cause:** Utility service parameters not confirmed; assumption is 12.5kV MV service (typical for BC Hydro), but actual service voltage may differ
- **Consequence:** If utility service is different voltage (e.g., 25kV instead of 12.5kV), transformers and MV switchgear must be re-specified; if service capacity is limited, additional service upgrades or on-site generation may be required

**Affected Buckets:** MAT (transformer and switchgear voltage rating), potentially significant if on-site generation required

**Probability:** Low-Medium | **Impact:** Medium

**Potential Cost Impact:** +$75,000 to +$200,000 CAD (equipment re-specification); potentially +$500k+ if on-site generation required

**Suggested Mitigation:**
1. Confirm utility service parameters with BC Hydro early in design (voltage, capacity, connection point, service charges)
2. Request utility service availability study if not already provided
3. Obtain transformer and switchgear budgetary quotes for multiple voltage options
4. Coordinate with Employer re: any utility service upgrade cost responsibilities

**Contingency Handling:** Equipment re-specification covered by contingency; on-site generation would be scope change

---

## R-1704: Cable Routing Lengths Significantly Exceed Estimates

**Risk Driver:** Quantity / Design

**Cause → Consequence:**
- **Cause:** No equipment layout drawings exist; cable lengths are estimated based on assumed facility layout and equipment distribution
- **Consequence:** If actual routing distances are longer (due to congestion, separation requirements, site constraints), cable material and installation costs increase; may require additional cable tray/conduit

**Affected Buckets:** MAT (cables, cable tray, conduit), CD (cable pulling and termination labor)

**Probability:** Medium | **Impact:** Low-Medium

**Potential Cost Impact:** +$100,000 to +$300,000 CAD

**Suggested Mitigation:**
1. Develop preliminary electrical layout (DEL-17.01) showing equipment locations and cable routing corridors
2. Coordinate with civil, structural, and process layouts to confirm equipment locations
3. Include cable routing margin (15-20% length allowance) in cable schedules
4. Optimize equipment locations to minimize cable runs during design

**Contingency Handling:** Covered by 25% contingency on MAT and 30% contingency on CD

---

## R-1705: Poor Soil Resistivity Requiring Enhanced Grounding System

**Risk Driver:** Site Conditions / Geotechnical

**Cause → Consequence:**
- **Cause:** No soil resistivity survey conducted; grounding design assumes typical soil resistivity for Fraser River area
- **Consequence:** If soil resistivity is high (rocky soil, poor conductivity), grounding system may require additional electrodes, deeper electrodes, ground enhancement material (bentonite, conductive concrete), or alternative grounding methods

**Affected Buckets:** MAT (additional grounding materials), CD (additional installation labor), E (additional grounding calculations and testing)

**Probability:** Low-Medium | **Impact:** Low-Medium

**Potential Cost Impact:** +$50,000 to +$150,000 CAD

**Suggested Mitigation:**
1. Conduct soil resistivity survey early in design (4-point Wenner method)
2. Design grounding system per IEEE 80 with touch/step potential analysis
3. Include grounding enhancement material allowance if resistivity is unfavorable
4. Consider deep-driven electrodes or chemical ground rods if required

**Contingency Handling:** Covered by 25% contingency on MAT and 30% contingency on CD

---

## R-1706: Equipment Delivery Lead Times and Premium Pricing

**Risk Driver:** Schedule / Market Conditions

**Cause → Consequence:**
- **Cause:** Electrical equipment (especially transformers and switchgear) may have long lead times (6-12 months for custom configurations)
- **Consequence:** If project schedule requires expedited delivery, premium pricing and/or air freight may be required; schedule delays if equipment is on critical path

**Affected Buckets:** MAT (premium pricing), FRT (expedited freight), potentially schedule-driven indirects increase

**Probability:** Medium | **Impact:** Medium

**Potential Cost Impact:** +$100,000 to +$300,000 CAD

**Suggested Mitigation:**
1. Issue RFQs for major electrical equipment early (transformers, switchgear, MCCs)
2. Confirm vendor lead times and expedite charges during procurement
3. Consider standard equipment configurations where possible to reduce lead times
4. Include schedule float for electrical equipment procurement on critical path

**Contingency Handling:** Covered by 25% contingency on MAT and FRT

---

## R-1707: ER Requirements Not Extracted (Additional Requirements)

**Risk Driver:** Scope / Requirements

**Cause → Consequence:**
- **Cause:** Employer's Requirements (Vol 2 Parts 1-3) not yet extracted for electrical requirements
- **Consequence:** ER may specify additional requirements such as: additional redundancy (N+1), backup power systems, enhanced monitoring, special grounding/bonding requirements, marine-environment ratings, specific equipment manufacturers/standards

**Affected Buckets:** MAT (additional equipment or upgraded ratings), E (additional engineering), CD (additional installation complexity)

**Probability:** Medium | **Impact:** Medium

**Potential Cost Impact:** +$50,000 to +$200,000 CAD

**Suggested Mitigation:**
1. Extract ER requirements for electrical systems early in design phase
2. Review ER for redundancy requirements, backup power, and special electrical standards
3. Clarify with Employer any critical electrical performance requirements
4. Include ER requirements in electrical specifications (DEL-17.02)

**Contingency Handling:** Covered by 25% overall contingency; significant ER-driven scope additions may require scope change

---

## R-1708: Integration Complexity with Control Systems and Instrumentation

**Risk Driver:** Interface / Coordination

**Cause → Consequence:**
- **Cause:** Electrical power distribution interfaces with control systems (PKG-19) and field instrumentation (PKG-20); coordination requirements TBD
- **Consequence:** Integration requirements may include: additional power distribution to I/O cabinets, UPS distribution to remote field panels, control power transformers, grounding/shielding coordination for instrumentation, loop isolation

**Affected Buckets:** MAT (additional distribution equipment), CD (additional terminations and testing), E (additional coordination effort)

**Probability:** Medium | **Impact:** Low-Medium

**Potential Cost Impact:** +$75,000 to +$200,000 CAD

**Suggested Mitigation:**
1. Coordinate electrical design with control systems design (PKG-19) and instrumentation design (PKG-20)
2. Define control power distribution architecture early
3. Establish grounding and shielding philosophy for instrumentation circuits
4. Include instrument power requirements in load calculations

**Contingency Handling:** Covered by 25% overall contingency

---

## Risk Summary Table

| Risk ID | Risk Driver | Probability | Impact | Cost Range (CAD) | Contingency Coverage |
|---------|-------------|-------------|--------|------------------|----------------------|
| R-1701 | Scope/Quantity (motor loads) | Medium | Med-High | +$150k to +$400k | Partial |
| R-1702 | Scope/Requirements (hazardous area) | Medium | Medium | +$100k to +$250k | Yes |
| R-1703 | Interface (utility service) | Low-Med | Medium | +$75k to +$200k | Yes (equipment); No (generation) |
| R-1704 | Quantity/Design (cable lengths) | Medium | Low-Med | +$100k to +$300k | Yes |
| R-1705 | Site Conditions (soil resistivity) | Low-Med | Low-Med | +$50k to +$150k | Yes |
| R-1706 | Schedule/Market (lead times) | Medium | Medium | +$100k to +$300k | Yes |
| R-1707 | Scope/Requirements (ER extraction) | Medium | Medium | +$50k to +$200k | Yes |
| R-1708 | Interface (control systems) | Medium | Low-Med | +$75k to +$200k | Yes |

**Total Risk Exposure:** +$700,000 to +$2,000,000 CAD (cumulative, not probabilistic)

**Contingency Provision:** $962,000 CAD (25% of base)

**Coverage Assessment:** Contingency is adequate for individual risks; cumulative risk exposure exceeds contingency, indicating importance of design development and vendor quotes to reduce uncertainty

---

**Total Risks:** 8 (R-1701 through R-1708)

---

**END OF RISK REGISTER**
