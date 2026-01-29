# Guidance: DEL-15.04 Pump Data Sheet Package

## Purpose

This guidance document supports the management and review of the **Pump Data Sheet Package** for **PKG-15 Pumps & Rotating Equipment** within the Canola Oil Transload Facility project.

**Deliverable purpose:** Defines and substantiates pumps in accordance with ER requirements.

**Source:** `_CONTEXT.md` (description), decomposition DEL-15.04 entry

### Role in Project Delivery

The Pump Data Sheet Package serves as:

1. **Specification compliance verification** — Confirms vendor equipment meets DEL-15.02 requirements
2. **Design input** — Provides data for DEL-15.01 (arrangement), PKG-05 (foundations), commissioning
3. **Procurement record** — Documents as-purchased equipment for project records
4. **O&M baseline** — Provides equipment data for operations and maintenance

**Source:** Standard role of vendor data in EPC projects

### Contribution to Project Objectives

This deliverable supports:

- **OBJ-1 (Safe & Reliable Operation):** Verified pump performance ensures reliable facility operation
- **OBJ-9 (Lifecycle Cost Optimization):** Pump efficiency verification supports energy cost optimization

**Source:** Decomposition Section 2 (Objectives)

## Principles

### Principle 1: Vendor Data Review is Not Vendor Design Review

**Important distinction:**

| Contractor Review (Required) | Vendor Design Review (Not Required) |
|------------------------------|-------------------------------------|
| Verify data matches specification (DEL-15.02) | Verify vendor internal design calculations |
| Verify NPSH margin is adequate (per DEL-15.03) | Verify vendor stress analysis |
| Verify operating point is acceptable | Verify vendor FEA models |
| Verify materials comply with codes | Review vendor manufacturing procedures |
| Verify dimensions suitable for installation | Approve vendor QA/QC plans in detail |

**Rationale:** Vendor is responsible for pump internal design per API 610. Contractor verifies compliance with specification and suitability for application, not vendor design adequacy.

**Source:** Standard EPC vendor data review scope; API 610 assigns pump design responsibility to manufacturer

### Principle 2: Critical Review Items for Pump Data

**High-priority review items:**

1. **NPSH margin verification** — Most critical for reliability
   - Calculate: NPSH margin = NPSHA (DEL-15.03) - Vendor NPSHR
   - Requirement: Margin ≥ 0.5m (API 610 minimum)
   - **Failure mode:** Insufficient NPSH margin → cavitation → pump damage

2. **Operating point verification** — Critical for efficiency and reliability
   - Plot vendor pump curve against calculated system curve (DEL-15.03)
   - Operating point should be within 70–120% of BEP (best efficiency point)
   - **Failure mode:** Operating far from BEP → low efficiency, high energy cost, reduced pump life

3. **Performance tolerance check** — Verify guarantees are achievable
   - Vendor performance must meet specification within ISO 9906 Grade 2 tolerances (Flow ±7%, Head ±5%)
   - **Failure mode:** Vendor over-promises → field performance test fails

4. **Materials compliance** — Verify suitability for service
   - Wetted materials compatible with CSD canola oil (non-corrosive, food-grade if required)
   - Material designations match API 610 Annex G
   - **Failure mode:** Wrong materials → corrosion, contamination

**Source:** API 610 performance requirements; common vendor data review issues

### Principle 3: Dimensional Data for Installation Design

Vendor outline drawings must provide:

- **Pump and motor envelope dimensions** for clearance verification
- **Nozzle locations** (coordinates relative to pump centerline/baseplate)
- **Baseplate dimensions** for foundation design
- **Anchor bolt pattern** (spacing, bolt circle diameter)
- **Weights** (dry, operating, lifting) for rigging and foundation loads

**Common dimensional data issues:**

| Issue | Impact | Prevention |
|-------|--------|------------|
| **Nozzle locations inconsistent with data sheet** | Piping design errors | Cross-check dimensions between data sheet and outline drawing |
| **Weights not provided for all components** | Foundation loads incomplete | Request complete weight breakdown (pump, motor, baseplate, fluid, auxiliary equipment) |
| **Lifting lug locations not shown** | Rigging plan cannot be developed | Request lifting lug locations and capacities |

**Source:** DEL-15.01 uses vendor data for arrangement; common dimensional data issues

## Considerations

### Vendor Data Review Timing

**Early review (Rev 0):**
- Conducted soon after vendor contract award
- Focus on critical items (NPSH, operating point, major dimensions)
- Identify major issues early to allow vendor correction without schedule impact

**Final review (Rev A or later):**
- Conducted after vendor incorporates comments
- Verify all comments addressed
- Approve for construction (AFC) if acceptable

**Source:** Standard vendor data review timing

### Common Vendor Data Deficiencies

| Deficiency | Frequency | Resolution |
|------------|-----------|------------|
| **Performance curves missing or incomplete** | Common | Request complete curves (head, efficiency, power, NPSH vs. flow) |
| **NPSH curve not provided** | Common | Request NPSHR vs. flow curve |
| **Foundation loads not provided** | Occasional | Request static and dynamic loads for foundation design |
| **Motor data sheet missing or incomplete** | Occasional | Request complete motor data (especially for electrical coordination) |
| **Outline drawings dimensions unclear** | Occasional | Request clarification or revised drawing with clear dimensioning |
| **Materials not specified to API 610 Annex G** | Occasional | Request materials be specified using API 610 material codes |

**Source:** Common vendor data submittal issues in pump projects

### Cross-Discipline Coordination

**Mechanical → Piping (DEL-14):**
- Provide vendor nozzle sizes and orientations
- Verify nozzle loads from piping flexibility analysis do not exceed vendor allowable loads

**Mechanical → Structural (PKG-05):**
- Provide vendor foundation loads for foundation design
- Verify anchor bolt pattern matches foundation design

**Mechanical → Electrical (PKG-19/20):**
- Provide motor data sheets for power supply and starter sizing
- Coordinate motor terminal box orientation for conduit routing

**Source:** Typical cross-discipline coordination using vendor data

## Trade-offs

### Trade-off: Speed of Review vs. Thoroughness

| Approach | Advantages | Disadvantages |
|----------|-----------|---------------|
| **Fast review** (2–5 days) | Minimizes schedule impact; vendor can proceed | May miss issues; rework if problems found later |
| **Thorough review** (1–2 weeks) | Higher confidence in data quality | Potential schedule delay; vendor waiting for approval |

**Guidance:** Prioritize critical items (NPSH, operating point, major dimensions) for fast review. Less critical items (detailed accessories, minor dimensional details) can be reviewed later or during fabrication hold points.

**Source:** EPC project schedule management; risk-based review approach

### Trade-off: Accepting Vendor Deviations vs. Requiring Full Compliance

**Scenario:** Vendor proposes deviation from specification (e.g., different material, alternate seal type, slightly different performance).

| Option | When to Use |
|--------|-------------|
| **Accept deviation** | Deviation is technically acceptable and does not impact project objectives; rejecting would cause schedule/cost impact |
| **Reject deviation** | Deviation compromises safety, reliability, or key project requirements; accepting would require extensive downstream design changes |

**Guidance:** Evaluate deviations based on technical merit and project impact, not specification compliance alone. Document accepted deviations and obtain Employer approval if required by contract.

**Source:** EPC change management; engineering judgment

## Examples

### Example: NPSH Margin Verification

**Given:**
- Calculated NPSHA (from DEL-15.03): 9.8m
- Vendor NPSHR (from data sheet): 8.5m
- Required margin: 0.5m (API 610 minimum)

**Check:**
- NPSH margin = 9.8m - 8.5m = **1.3m**
- Requirement: Margin ≥ 0.5m
- **Result: ACCEPTABLE** (margin exceeds minimum)

**Source:** NPSH verification methodology

### Example: Operating Point Verification

**Given:**
- System curve (from DEL-15.03): H = 7.5 + 0.0035 × Q² (H in m, Q in m³/hr)
- Vendor pump curve (from performance data): Intersects system curve at Q = 150 m³/hr, H = 86m
- Vendor BEP (from performance curve): 160 m³/hr at 78% efficiency

**Check:**
- Operating point: 150 m³/hr
- BEP: 160 m³/hr
- Operating point as % of BEP: 150 / 160 = **93.75%**
- Requirement: 70–120% of BEP
- **Result: ACCEPTABLE** (within preferred operating region)

**Source:** Operating point verification methodology

---

**Document Status:** ENRICHED (Pass 1)
**Enrichment Date:** 2026-01-28
**Agent:** 4_DOCUMENTS enrichment cycle

**Cross-References:**
- Datasheet.md — Vendor data content and structure
- Specification.md — Vendor data requirements and acceptance criteria
- Procedure.md — Vendor data submittal and review process
- DEL-15.02 — Pump Technical Specification (vendor data verified against spec)
- DEL-15.03 — Pump Design Calculations (NPSH and operating point verification)
- DEL-15.01 — Pump Design Drawing Set (uses vendor outline drawings)
- DEL-15.05 — Pump Installation & Test Records (vendor data baseline for commissioning)
