# Guidance: DEL-13.03 Storage Tank Design Calculations

## Purpose

This guidance supports development of **Storage Tank Design Calculations** for **PKG-13 Storage Tanks**.

**Deliverable Role:** Provides engineering basis and verification for 3 × 15,000 MT CSD canola oil storage tank design per API 650.

**Project Objectives Supported:** OBJ-1 (Safe & Reliable Operation), OBJ-3 (Storage Capacity), OBJ-8 (Future Expandability)

**Source:** _CONTEXT.md; Decomposition document

---

## Principles

**CP-01: API 650 is Prescriptive**
- API 650 provides detailed formulas and procedures — follow them precisely
- Document where calculations deviate from or supplement API 650 requirements
- **Source:** API 650 design methodology

**CP-02: Conservative Design for Safety**
- Use conservative assumptions where data is uncertain
- Safety factors inherent in API 650 formulas — do not reduce without justification
- **Source:** OBJ-1 (Safe & Reliable Operation); API 650 philosophy

**CP-03: Optimization Within Constraints**
- Optimize tank geometry for cost (minimize shell weight, foundation size)
- Constraints: site footprint, height limits, crane capacity, transportation — **TBD**
- Document optimization rationale and trade-offs
- **Source:** Engineering economics; typical tank design practice

**CP-04: Seismic Design is Critical for BC Location**
- API 650 Appendix E seismic design is mandatory — **ASSUMPTION** (BC seismic zone)
- Seismic loads often govern anchorage and base plate design
- Sloshing (convective) loads must be included per Appendix E
- **Source:** API 650 Appendix E; NBC 2020 seismic requirements

---

## Considerations

**API 650 Shell Thickness Calculation:**
- Hydrostatic pressure governs: $t_d = 4.9 D (H - 0.3) G / S_d$ (API 650 Eq. 5-2)
- Minimum thickness per Table 5-1a (varies by diameter)
- Commercial plate thickness must be used (round up to standard sizes)
- Corrosion allowance: **TBD** (depends on coating use and service life)

**Seismic Analysis per API 650 Appendix E:**
- Site seismic parameters: **TBD** (PGA, spectral acceleration from NBC 2020 or site study)
- Impulsive component: Short-period tank response to ground acceleration
- Convective (sloshing) component: Liquid motion with longer period
- Anchorage decision: Compare overturning moment to tank dead weight resistance
  - If self-weight sufficient → Unanchored (base plate yielding check required)
  - If insufficient → Anchored (anchor bolts and anchor chairs required)

**Foundation Loading and Settlement:**
- Settlement limits per API 650 Appendix B: Uniform settlement typically not critical; differential settlement limited
- Maximum differential settlement: Varies by diameter (typically L/200 to L/300 over diameter)
- Coordinate with DEL-02.04 (geotechnical) and DEL-05.03 (foundation design)

**Tank Geometry Optimization:**
- Typical D/H ratio: 1:1 to 2:1 for large atmospheric tanks
- Larger diameter → Shorter height → Less shell thickness (less hydrostatic pressure)
- Larger diameter → Larger foundation footprint
- **TBD** — Site constraints on footprint and height

---

## Trade-offs

**TD-01: Tank Diameter vs. Height**
- Large D, low H: Less shell thickness, larger foundation, more site area
- Small D, tall H: Thicker shell, smaller foundation, less site area, higher seismic loads
- **Decision:** Optimize based on site constraints, shell cost, foundation cost

**TD-02: Anchored vs. Unanchored**
- Unanchored: Lower cost, simpler construction; requires seismic overturning check
- Anchored: Higher cost, anchor bolts/chairs; resists overturning in severe seismic
- **Decision:** Per API 650 Appendix E analysis (not optional if overturning exceeds resistance)

**TD-03: Calculation Method (Hand vs. Software)**
- Hand calculations: Transparent, easy to check; time-consuming for complex geometry
- Software: Faster, handles complexity; requires validation and spot-checking
- **Balance:** Use software for bulk calculations; hand-check critical elements

---

## Examples

**Typical Calculation Sequence:**
1. Establish capacity requirement (15,000 MT) and product SG
2. Trial tank geometry (D, H)
3. Calculate shell thicknesses per API 650 Eq. 5-2
4. Check minimum thickness per Table 5-1a
5. Design bottom per Sections 5.4/5.5
6. Design roof per Section 5.10
7. Check wind stability per Section 5.9
8. Perform seismic analysis per Appendix E
9. Calculate foundation loads
10. Verify settlement per Appendix B
11. Iterate geometry if needed for optimization

**Cross-Document References:**
**See Datasheet.md:** Calculation scope, types, inputs/outputs, load cases
**See Specification.md:** Requirements for calculation content (CR series), performance (PR series), verification (VR series)
**See Procedure.md:** Workflow for performing, checking, and approving calculations

---

**Document Status:** Pass 3 (Final) — Enrichment complete. API 650 principles, seismic methodology, optimization trade-offs provided. Cross-document consistency verified. Ready for WORKING_ITEMS refinement.

**Last Updated:** 2026-01-28
