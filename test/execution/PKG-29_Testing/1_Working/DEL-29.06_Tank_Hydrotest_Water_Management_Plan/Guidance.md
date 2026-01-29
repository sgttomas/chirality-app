# Guidance: DEL-29.06 Tank Hydrotest Water Management Plan

## Purpose

Guidance for **Tank Hydrotest Water Management Plan** for **PKG-29 Testing**.

**Deliverable Purpose:** Defines planned approach and controls for tank hydrotest water management to meet ER requirements. **Source:** Decomposition line 651

**Type:** Plan | **Discipline:** T&C | **Responsible:** D&B Contractor (QA/QC)

## Principles

### Environmental Stewardship in Testing

**"Do No Harm":** Hydrostatic testing should not create environmental damage. Large-volume water use and discharge require careful planning.

**Key Concerns:**
1. **Water Taking:** Large volumes may stress local supply (municipal or natural source)
2. **Contamination:** Hydrotest water picks up rust, mill scale, coating chemicals
3. **Discharge Impact:** Untreated discharge could harm aquatic life (Fraser River) or overwhelm municipal treatment
4. **Regulatory Compliance:** Unauthorized discharge is environmental violation with penalties

**Source:** General environmental management principles **ASSUMPTION**

### Hierarchy of Disposal Options

**Preferred → Least Preferred:**
1. **Discharge with treatment** (to river or sewer) — Most cost-effective if water quality acceptable
2. **Haul to municipal WWTP** — More expensive but ensures proper treatment
3. **Haul to remote disposal** — Most expensive, last resort

**Source:** Waste management hierarchy **ASSUMPTION**

## Considerations

**1. Timing and Permits**
- Permit applications take months; start early
- River discharge may have seasonal restrictions (salmon spawning: Oct-Mar typical **ASSUMPTION**)
- Municipal sewer discharge may require pre-approval and capacity reservation

**2. Water Source Selection**
- **Municipal water:** Clean, reliable, but expensive for large volumes and may stress supply
- **River intake:** Cheaper, but requires intake permit and pumps/filtration
- **Trucked water:** Flexible but very expensive for large volumes (not practical for 45,000 m³)

**3. Treatment System Sizing**
- Must handle peak drain rate (not just average)
- Allow for treatment inefficiency (may need multiple passes)
- Consider weather (freezing temperatures affect treatment)

**4. Coating Considerations**
- New tank coatings may leach solvents or cure byproducts
- Epoxy coatings: Check for amine leachate (raises pH)
- Zinc-rich coatings: Check for heavy metals
- Coordinate with coating supplier on leachate potential

**5. Cost Drivers**
- Haul-away: ~$5-10/m³ (45,000 m³ = $225k-450k) **ASSUMPTION**
- Treatment system rental: ~$50k-100k **ASSUMPTION**
- Discharge permit fees: Varies
- Laboratory testing: ~$500-1000 per sample set **ASSUMPTION**

## Trade-offs

**Discharge vs. Haul-Away:**
- Discharge: Lower cost, faster, but requires permits and treatment
- Haul-Away: Higher cost (potentially $250k+), no permit needed, guaranteed disposal
- **Recommendation:** Pursue discharge permits early; keep haul-away as backup

**Single vs. Sequential Tank Testing:**
- Sequential: Can reuse water between tanks (with treatment), reduces total volume
- Simultaneous: Faster schedule but no water reuse, higher volume
- **Recommendation:** Sequential with water reuse if schedule allows

## Examples

**Hydrotest Water Management Plan Outline:**

```
TANK HYDROTEST WATER MANAGEMENT PLAN

1. Executive Summary
   - 3 tanks, ~45,000 m³ total water
   - Fill from municipal supply
   - Treat and discharge to municipal sewer (permit applied)
   - Haul-away backup if discharge permit delayed

2. Water Sourcing
   - Source: Metro Vancouver municipal water
   - Supply rate: 200 m³/hr (coordinated with utility)
   - Fill duration: 75 hr per tank (3 days)

3. Fill/Hold/Drain Schedule
   - Tank 1: Fill Aug 1-4, Hold Aug 5, Drain Aug 6-9
   - Tank 2: Fill Aug 10-13, Hold Aug 14, Drain Aug 15-18
   - Tank 3: Fill Aug 20-23, Hold Aug 24, Drain Aug 25-28

4. Treatment System
   - Temporary settling tanks (2 × 100 m³)
   - Bag filters (10 micron)
   - pH adjustment system
   - Discharge rate: 150 m³/hr to sewer

5. Sampling/Testing
   - Parameters: pH, TSS, Oil & Grease, COD, Metals (Zn, Cr)
   - Frequency: Pre-discharge from each tank, Post-treatment daily
   - Lab: ABC Environmental Labs (accredited)
   - Acceptance: Per sewer discharge permit limits

6. Discharge
   - Discharge point: Municipal sewer connection at XYZ location
   - Permit: Applied May 1, approval expected June 30
   - Discharge limits: pH 6-9, TSS <100 mg/L, O&G <15 mg/L

7. Contingency (Haul-Away)
   - If permit not approved or water quality fails
   - Hauler: DEF Liquid Waste Services (licensed)
   - Disposal: Metro Vancouver Annacis WWTP
   - Cost estimate: $300k

8. Environmental Monitoring
   - Daily inspection of treatment system
   - Record all sampling and test results (DEL-29.07)
   - Track all disposal (DEL-29.08)
   - Report any spills or non-compliance immediately
```

**Source:** Typical hydrotest water management plan structure **ASSUMPTION**

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|-------------|----------|----------|----------|-------------------|-------------------|--------------|
| — | — | — | — | — | — | **TBD** |

---

## Cross-Document Linkage

| Document | Key Sections | Relationship |
|----------|--------------|--------------|
| Datasheet.md | §Attributes, §Construction | Provides factual context for plan components and disposal options |
| Specification.md | §Requirements (FR, PR, IR, QR), §Standards, §Verification | Defines normative requirements that this Guidance supports |
| Procedure.md | §Steps 1-8 | Implements this Guidance through specific plan development steps |

**Guidance-to-Specification Traceability:**
- §Principles (Environmental Stewardship) → Supports Specification QR-2, OBJ-7
- §Principles (Hierarchy of Disposal) → Supports Specification FR-4
- §Considerations Item 1 (Timing/Permits) → Supports Specification PR-2, IR-1
- §Considerations Item 2 (Water Source) → Supports Specification FR-1
- §Considerations Items 3-4 (Treatment, Coatings) → Supports Specification FR-2
- §Trade-offs → Informs engineering decisions for Specification requirements

**Guidance-to-Procedure Traceability:**
- §Considerations Item 1 (Timing) → Procedure Step 7 (Permits)
- §Considerations Item 2 (Water Source) → Procedure Step 2
- §Considerations Items 3-4 → Procedure Steps 3-4 (Treatment)
- §Trade-offs (Sequential vs. Simultaneous) → Procedure Step 1
- §Examples (Plan Outline) → Procedure Step 8 (Compile)
