# Risk Register

## Overview

This register identifies risks to the estimate accuracy and suggests mitigation actions. Contingency is applied per the PCT_BY_BUCKET method (see BOE.md).

---

## R-001: Unloading Arm Pricing Uncertainty

**Risk Driver:** Price (equipment cost variance)

**Cause → Consequence:**
- Cause: No vendor quotes for 32 specialized railcar unloading arms; pricing based on industry typical range
- Consequence: Actual vendor pricing may vary ±30% from $50k/unit assumption ($45k-65k/unit range); total arms cost variance ±$480k

**Affected Buckets:**
- CBS: MAT (unloading arms L-006)
- WBS: PKG-10

**Suggested Mitigation:**
1. Obtain budgetary quotes from minimum 3 suppliers (TechnipFMC, OPW, Emco Wheaton, Ultraflow)
2. Specify arm requirements clearly in DEL-10.02 (materials, reach envelope, swivels, controls) to enable comparable quotes
3. Consider value engineering: aluminum arms (lower cost) vs stainless steel arms (higher cost, better corrosion resistance)
4. Include vendor technical review in procurement process to verify arm suitability for gravity flow and food-grade service

**Contingency Handling:** 25% contingency applied to MAT bucket ($639k total) provides ~$400k buffer on arms alone; partially covers upside variance.

---

## R-002: Header Piping Length Variance

**Risk Driver:** Quantity (piping length variance from layout)

**Cause → Consequence:**
- Cause: Header piping length (400 lm) estimated before DEL-10.01 layout drawings completed; actual routing may differ
- Consequence: Piping length variance ±20% (320-480 lm) affects material cost ±$56k and labor cost ±$36k (total ±$92k)

**Affected Buckets:**
- CBS: MAT (header piping L-008), CD (piping installation L-016)
- WBS: PKG-10

**Suggested Mitigation:**
1. Progress DEL-10.01 header layout drawings to define actual routing and measure piping length
2. Coordinate header routing with PKG-07 rail track layout (station spacing drives header length)
3. Optimize header routing to minimize length while maintaining gravity flow slopes (minimum 1:100 per DEL-10.01)
4. Consider header routing alternatives in DEL-10.01 development (direct path vs looped/manifold configuration)

**Contingency Handling:** 25% contingency on MAT and 30% on CD provides buffer for piping length variance.

---

## R-003: Containment Configuration Uncertainty

**Risk Driver:** Scope (containment pan configuration affects cost)

**Cause → Consequence:**
- Cause: Containment configuration not yet defined (individual pans vs grouped zones vs common containment)
- Consequence: Configuration change could affect cost ±30%: individual pans (32 units @ $8k = $256k assumed) vs grouped containment zones (lower material cost ~$180k but different installation) vs common containment trench (lowest material ~$120k but highest installation complexity)

**Affected Buckets:**
- CBS: MAT (containment pans L-009, sump pumps L-010), CD (pan installation L-017, pump installation L-018)
- WBS: PKG-10

**Suggested Mitigation:**
1. Progress DEL-10.03 containment volume calculations to determine regulatory requirements
2. Develop containment configuration options in DEL-10.01 with cost/benefit analysis
3. Coordinate with Employer and regulatory authorities on acceptable containment approach
4. Consider trade-offs: individual pans (easier cleanup, localized spills, higher cost) vs grouped/common containment (lower cost, more complex drainage, larger single-spill impact)

**Contingency Handling:** 25% contingency on MAT and 30% on CD provides buffer for configuration variance; contingency may not fully cover shift to grouped/common containment if significant cost reduction (would reduce estimate).

---

## R-004: Simultaneous Operations and Throughput Risk

**Risk Driver:** Scope / Productivity (throughput capacity verification affects equipment sizing)

**Cause → Consequence:**
- Cause: Simultaneous unloading operations and throughput capacity not yet verified by DEL-10.03 calculations
- Consequence: If throughput analysis shows more simultaneous stations required or higher flow rates needed, header sizing may increase (larger pipe diameter) or additional equipment may be required (larger arms, boosted flow); cost impact +$100k-300k if significant upsizing required

**Affected Buckets:**
- CBS: MAT (header piping L-008, unloading arms L-006, valves L-013), CD (header installation L-016), E (calculations DEL-10.03)
- WBS: PKG-10 (DEL-10.03, DEL-10.01, DEL-10.02)

**Suggested Mitigation:**
1. **Priority:** Progress DEL-10.03 throughput calculations to verify 1,000,000 MT/annum achievable with 32 stations
2. Obtain operating schedule assumptions from Employer (operating hours/year, peak demand periods)
3. Obtain product data for canola oil (viscosity-temperature relationship affects flow rates significantly)
4. Consider design margin in header sizing (10-25% overcapacity for operational flexibility per OBJ-4)
5. Verify railcar unloading rate assumptions with arm vendor data

**Contingency Handling:** 25% contingency on MAT and 30% on CD provides partial buffer; significant upsizing (e.g., 10-inch to 12-inch header upgrade) may exceed contingency.

---

## R-005: Interface Coordination Risk

**Risk Driver:** Interface (coordination with PKG-07, PKG-14, PKG-17, PKG-20)

**Cause → Consequence:**
- Cause: Multiple package interfaces not yet coordinated (PKG-07 rail track alignment, PKG-14 downstream piping, PKG-17 electrical, PKG-20 instrumentation)
- Consequence: Interface mismatches could require rework (relocate arms, resize connections, add interface equipment); cost impact typically $20k-80k for interface modifications

**Affected Buckets:**
- CBS: All buckets (interface changes ripple through design, materials, installation)
- WBS: PKG-10 (all deliverables)

**Suggested Mitigation:**
1. Establish interface control documents (ICDs) between PKG-10 and adjacent packages
2. Conduct interdisciplinary coordination (IDC) reviews per DEL-10.01 Procedure.md Step 4
3. Identify critical interfaces early: (a) PKG-07 track alignment for arm positioning; (b) PKG-14 header discharge connection; (c) PKG-17 sump pump power; (d) PKG-20 flow indicators and level switches
4. Freeze interface points before finalizing equipment procurement

**Contingency Handling:** Contingency provides buffer for minor interface adjustments; major redesign would require scope change.

---

## R-006: Regulatory Containment Requirements Risk

**Risk Driver:** Scope (regulatory requirements may mandate larger containment or different configuration)

**Cause → Consequence:**
- Cause: Containment volume requirements (Environment Canada, BC regulations) not yet confirmed; regulatory compliance verification pending
- Consequence: If regulatory requirements exceed assumptions, containment scope may increase (larger pans, additional freeboard, rainfall allowance); cost impact +$50k-150k if significant containment upsizing required

**Affected Buckets:**
- CBS: MAT (containment pans L-009), CD (pan installation L-017), E (calculations DEL-10.03)
- WBS: PKG-10 (DEL-10.01, DEL-10.03)

**Suggested Mitigation:**
1. Obtain applicable environmental regulations (Environment Canada Code of Practice, BC Spill Reporting Regulation)
2. Progress DEL-10.03 containment volume calculations with regulatory compliance verification
3. Coordinate containment design approach with Employer environmental team and regulatory authorities early
4. Consider conservative containment sizing (exceed minimum regulatory requirements) to reduce compliance risk

**Contingency Handling:** 25% contingency on MAT and 30% on CD provides buffer for moderate containment upsizing.

---

## R-007: Food-Grade Material Requirements Risk

**Risk Driver:** Scope (food-grade material requirements may affect equipment selection and cost)

**Cause → Consequence:**
- Cause: Food-grade compatibility requirements (canola oil is food-grade edible oil) may mandate specific materials (stainless steel vs carbon steel, food-grade seals, surface finish requirements)
- Consequence: If strict food-grade requirements apply, equipment costs may increase: stainless steel arms vs aluminum (+20-30%), stainless header vs carbon steel (+40-60%); total cost impact potential +$300k-600k if full stainless steel upgrade required

**Affected Buckets:**
- CBS: MAT (arms L-006, header L-008, containment L-009, valves L-013)
- WBS: PKG-10 (DEL-10.02, DEL-10.04)

**Suggested Mitigation:**
1. Clarify food-grade requirements in Employer's Requirements (strict vs general food-safety compliance)
2. Verify material selection criteria in DEL-10.02 (food-grade compatible materials vs food-grade certified materials)
3. Obtain vendor data on material options and food-grade certifications
4. Consider scope: crude super degummed (CSD) canola oil may have less stringent requirements than refined edible oil

**Contingency Handling:** 25% contingency on MAT ($639k) provides partial buffer; full stainless steel upgrade may exceed contingency if required.

---

## R-008: Installation Productivity Risk

**Risk Driver:** Productivity (actual installation hours may vary from assumptions)

**Cause → Consequence:**
- Cause: Installation labor hours estimated without detailed method statements or site-specific productivity data
- Consequence: Productivity variance ±20% affects labor costs: 32 arms at 70-80 hrs/unit (±15 hrs variance = ±$52k total); header installation at 4-5 hrs/lm (±1 hr variance = ±$44k total); cumulative labor variance ±$140k

**Affected Buckets:**
- CBS: CD (all installation labor lines L-015 through L-023), CI (derived from CD)
- WBS: PKG-10

**Suggested Mitigation:**
1. Develop detailed installation method statements with crew composition and hours per activity
2. Benchmark productivity against historical projects or industry data for similar railcar unloading systems
3. Conduct constructability review to identify installation challenges (access, sequencing, coordination with rail operations)
4. Consider site-specific factors: (a) work within active rail corridor; (b) rail traffic interruptions; (c) confined space or elevated work

**Contingency Handling:** 30% contingency on CD ($215k) and 30% on CI ($39k) provides buffer for productivity variance.

---

## R-009: Commissioning Scope Risk

**Risk Driver:** Scope (commissioning and testing scope may expand beyond assumptions)

**Cause → Consequence:**
- Cause: Commissioning scope estimated without detailed testing procedures or Employer acceptance criteria
- Consequence: Expanded testing scope (e.g., extended performance testing, multiple test runs for throughput verification, additional witness testing) could increase commissioning costs +20-40% (+$25k-50k)

**Affected Buckets:**
- CBS: COM (all commissioning lines L-027 through L-030)
- WBS: PKG-10 (DEL-10.05)

**Suggested Mitigation:**
1. Obtain Employer's Requirements commissioning and acceptance testing criteria
2. Develop detailed commissioning procedures (DEL-10.05) with test scope and estimated hours
3. Clarify witness testing requirements (Employer presence, third-party inspection)
4. Plan commissioning sequencing: individual arm testing → zone testing → full system integration testing

**Contingency Handling:** 30% contingency on COM ($37k on $122k base) provides buffer for commissioning scope expansion.

---

## R-010: PKG-07 Rail Track Interface Risk

**Risk Driver:** Interface (rail track alignment and station positioning affects unloading arm layout)

**Cause → Consequence:**
- Cause: PKG-07 track layout not yet available; station spacing and alignment assumed
- Consequence: If actual track layout differs from assumptions (curved track vs straight, tighter/wider spacing, elevation changes), unloading arm positioning and header routing may require redesign; rework cost potential $50k-150k

**Affected Buckets:**
- CBS: E (redesign effort), MAT (potential equipment changes), CD (installation adjustments)
- WBS: PKG-10 (all deliverables)

**Suggested Mitigation:**
1. **Priority:** Coordinate with PKG-07 early to establish track alignment and station positions
2. Freeze rail track layout before finalizing unloading arm procurement
3. Include flexibility in arm specification (adjustable mounting, swivel reach envelope) to accommodate minor track variations
4. Conduct site survey to verify track alignment and identify constraints

**Contingency Handling:** Contingency provides buffer for minor interface adjustments; major redesign would require scope change or additional budget.

---

## Contingency Summary

**Method:** PCT_BY_BUCKET with allowance-heavy adjustments

**Total Contingency:** $996,000 CAD (25.4% of $3,913,000 base)

**Contingency by CBS:**

| CBS | Base Amount | Contingency % | Contingency $ | Rationale |
|-----|-------------|---------------|---------------|-----------|
| E | $135,000 | 20% | $27,000 | 100% allowance; no engineering rates |
| MAT | $2,555,000 | 25% | $639,000 | 100% allowance; specialized equipment |
| CD | $717,000 | 30% | $215,000 | 100% allowance; specialized installation |
| CI | $129,000 | 30% | $39,000 | Factor-derived from CD |
| PM | $204,000 | 15% | $31,000 | Factor-derived |
| P | $51,000 | 15% | $8,000 | Factor-derived |
| COM | $122,000 | 30% | $37,000 | Allowance-based; testing scope uncertainty |

**Coverage Assessment:**

The contingency is sized to address:
- ✓ Pricing variance from allowances to actual vendor quotes (±20-30% typical)
- ✓ Minor quantity adjustments from design refinement (±10-20%)
- ✓ Productivity variance (±15-25%)
- ✓ Minor interface adjustments and coordination rework
- ⚠ Partial coverage for major scope changes (e.g., containment configuration change, full stainless steel upgrade)
- ✗ Does not cover major redesign or significant scope additions

**Recommendation:** Contingency is appropriate for this estimate maturity level (INITIALIZED deliverables, 100% allowance pricing). As estimate matures with vendor quotes and design details, contingency can be reduced (target 15-20% at detailed design stage).

---

## Risk Summary

Total risks logged: 10 (R-001 through R-010)

**Risks by impact potential:**

| Impact Level | Count | Risk IDs |
|--------------|-------|----------|
| HIGH (>$200k potential) | 3 | R-001 (arm pricing ±$480k), R-004 (throughput/sizing +$100k-300k), R-007 (stainless upgrade +$300k-600k) |
| MEDIUM ($50k-200k) | 4 | R-002 (piping length ±$92k), R-003 (containment config ±30%), R-006 (containment regulatory +$50k-150k), R-010 (rail interface $50k-150k) |
| LOW (<$50k) | 3 | R-005 (interface coordination $20k-80k), R-008 (productivity ±$140k but covered by contingency), R-009 (commissioning +$25k-50k) |

**Risk mitigation priorities:**
1. **Obtain vendor quotes** for unloading arms (R-001) — highest cost item with greatest uncertainty
2. **Coordinate PKG-07 interface** early (R-010) — prevents redesign and rework
3. **Progress DEL-10.03 calculations** (R-004) — verify throughput capacity and sizing basis
4. **Clarify food-grade requirements** (R-007) — material selection affects multiple cost elements
5. **Define containment configuration** (R-003, R-006) — regulatory compliance and cost optimization

**Overall risk assessment:** MEDIUM-HIGH risk level due to 100% allowance-based estimate and specialized equipment with limited pricing data. Risk will reduce significantly when vendor quotes obtained and design details progress from INITIALIZED to IN_PROGRESS state.
