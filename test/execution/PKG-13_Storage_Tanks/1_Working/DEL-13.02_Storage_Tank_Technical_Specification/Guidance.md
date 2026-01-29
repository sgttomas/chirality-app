# Guidance: DEL-13.02 Storage Tank Technical Specification

## Purpose

This guidance supports development of **Storage Tank Technical Specification** for **PKG-13 Storage Tanks**.

**Deliverable Role:** Defines performance, materials, and workmanship requirements for 3 × 15,000 MT CSD canola oil storage tanks, agitators, and appurtenances per ER and API 650.

**Project Objectives Supported:** OBJ-1 (Safe & Reliable Operation), OBJ-3 (Storage Capacity — 45,000 MT), OBJ-8 (Future Expandability — Phase 2)

**Source:** _CONTEXT.md; Decomposition document

---

## Principles

**DP-01: Specification Clarity and Enforceability**
- Requirements stated using imperative mood ("shall" for mandatory, "should" for recommended)
- Avoid ambiguity — each requirement must be verifiable
- Reference standards by edition and date
- **Source:** Specification best practice

**DP-02: API 650 as Foundation**
- API 650 is the primary standard — specification builds upon it, not replaces it
- Where project requirements exceed API 650, clearly identify and justify
- Do not repeat API 650 content — reference it
- **Source:** API 650 usage best practice; Decomposition PKG-13 Scope

**DP-03: Material Selection for Service and Lifecycle**
- Materials must be compatible with CSD canola oil (corrosion, contamination)
- Consider operating temperature range, seismic loads, environmental exposure
- Balance initial cost with lifecycle performance (OBJ-9 Lifecycle Cost Optimization)
- **Source:** OBJ-1, OBJ-9; API 650 material selection principles

**DP-04: Quality Through Fabricator Qualification**
- Qualified fabricator (CSA W47.1 or equivalent) is essential for quality
- Welding procedures and welder qualifications per CSA W59 and API 650
- Inspection and testing per API 650 Section 8
- **Source:** Canadian regulatory environment; API 650 quality requirements

**DP-05: Procurement-Friendly Specification**
- Provide sufficient detail for vendor bidding and proposal evaluation
- Avoid over-specification that limits vendor flexibility unnecessarily
- Clearly identify critical requirements vs. informational content
- **Source:** ASSUMPTION based on design-build procurement best practice

---

## Considerations

### API 650 Tank Specification Considerations

**Material Selection:**
- Shell material: API 650 Table 4-1 provides material options; carbon steel typical for canola oil — **ASSUMPTION**
- Brittle fracture: API 650 Appendix D applies if minimum design metal temperature (MDMT) below specified limits
- Corrosion allowance: **TBD** (depends on internal coating use and service life expectations)

**Roof Type Selection:**
- Cone roof: Economical, suitable for non-volatile products (canola oil has low volatility) — **ASSUMPTION preferred**
- Dome roof: Structurally efficient for large diameters
- Floating roof: Uncommon for canola oil (low volatility); high cost
- **Source:** API 650 roof types; Guidance for DEL-13.01 (trade-off TD-02)

**Seismic Design:**
- API 650 Appendix E required for BC location (seismic zone) — **ASSUMPTION**
- Anchored vs. unanchored determined by overturning analysis (DEL-13.03)
- Base shear, sloshing, and foundation interaction per Appendix E
- **Source:** API 650 Appendix E; NBC 2020 seismic requirements

**Fabrication and Welding:**
- Shop vs. field fabrication: depends on tank size, site access, cost — **TBD**
- Welding processes: SMAW, FCAW, SAW common; specification should allow approved alternatives
- Joint design and weld details per API 650 Figures 5-1 through 5-10
- **Source:** API 650 fabrication and welding requirements

**Inspection and Testing:**
- Visual inspection of all welds per API 650 Section 8
- NDE: Vacuum box testing for bottom-to-shell and bottom lap welds; MT or PT for nozzle welds
- Hydrostatic test: Fill to design capacity for 24 hours (typical); verify no leakage or visible distortion
- **Source:** API 650 Sections 7 and 8

### Agitator Specification Considerations

**Agitator Type:**
- Side-entering: Common for large storage tanks; easier access for maintenance
- Top-entering: Requires roof penetration and support structure
- Bottom-mounted: Less common; complex installation
- **TBD** — Selection depends on process requirements and tank configuration

**Mixing Duty:**
- Purpose: Maintain product uniformity, prevent settling, blend different batches
- Power and speed: Determined by tank volume, product viscosity, mixing intensity required
- **TBD** — Requires process engineering input or vendor recommendation

**Materials:**
- Wetted parts compatible with canola oil (typically carbon steel or stainless steel)
- Seals and gaskets suitable for product and temperature
- **TBD** — Material selection coordination with vendor

### Tank Appurtenance Considerations

**Overflow Protection:**
- Prevent overfilling beyond safe capacity
- Typical: Overflow nozzle at maximum fill level with piping to containment
- Coordinate with PKG-14 (piping) and PKG-19 (control systems for high-level alarms)
- **Source:** Decomposition PKG-13 Scope; typical safety feature

**Water Draw-off:**
- Remove water accumulation from tank bottom (condensation, product moisture)
- Typical: Low-point nozzle with external valve
- May integrate with tank sump or drain system
- **Source:** Decomposition PKG-13 Scope

**Phase 2 Connections:**
- Connections installed in Phase 1, capped/blanked for Phase 2
- Locations and sizes per Phase 2 scope — **TBD** (ER extraction)
- Protection: Blind flanges, corrosion protection
- **Source:** Decomposition PKG-13 Scope; OBJ-8 (Future Expandability)

---

## Trade-offs

**TD-01: Specification Detail Level**
- **High Detail:** Reduces vendor interpretation variability; may limit vendor flexibility and increase cost
- **Performance-Based:** Allows vendor engineering; requires robust performance criteria and acceptance testing
- **Balance:** Specify critical requirements (materials, standards, testing); allow vendor flexibility on methods

**TD-02: Material Grade Selection**
- **Higher Grade Steel:** Better toughness, weldability; higher cost
- **Standard Grade:** Economical; may require PWHT or preheat for thick sections
- **Decision:** Based on shell thickness (from DEL-13.03), welding, and fabrication plan

**TD-03: Internal Coating**
- **With Coating:** Product purity, corrosion protection, longer service life; higher initial cost, coating maintenance
- **Without Coating (Bare Steel):** Lower cost; potential corrosion, product contamination risk
- **Decision:** **TBD** — Based on ER, product specifications, lifecycle cost analysis (OBJ-9)

**TD-04: Fabricator Pre-Qualification**
- **Pre-Qualify Fabricators:** Ensures only qualified bidders; reduces procurement risk; may limit competition
- **Qualify After Award:** Broader bidder pool; risk of non-compliant fabricator; specification must clearly define qualification requirements
- **Decision:** **TBD** — Based on project procurement strategy

---

## Examples

**API 650 Tank Specification Structure (Typical):**
1. Scope — Defines coverage
2. References — API 650 edition, NBC 2020, CSA standards
3. Design Basis — 15,000 MT capacity, CSD canola oil, Surrey BC location, seismic per NBC 2020
4. Materials — Shell plates per API 650 Table 4-1, CSA G40.21 for structural steel
5. Fabrication — Per API 650 Section 5
6. Welding — WPS/PQR per CSA W59 and API 650
7. Inspection — Per API 650 Section 8
8. Testing — Hydrostatic per API 650 Section 7
9. Coating — Internal/external systems per PKG-26 spec
10. Documentation — MTRs, WPS/PQR/WPQ, NDE reports, hydrostatic test report

**Agitator Specification Structure (Typical):**
1. Scope
2. Performance Requirements — Mixing duty, power, speed
3. Design and Construction — Type, materials, motor/drive
4. Installation — Mounting, alignment, piping/electrical interfaces
5. Testing — FAT, site performance test
6. Documentation — Vendor drawings, test reports, O&M manual

**Tank Appurtenance Specification Structure (Typical):**
- Organized by appurtenance type (nozzles, manholes, vents, overflow, etc.)
- Each section: size, quantity, material, standard, installation requirements

---

## Cross-Document References

**See Datasheet.md:** Standards, materials, fabrication/installation approach, testing requirements
**See Specification.md:** Content requirements (CR series), performance requirements (PR series), interface requirements (IR series)
**See Procedure.md:** Workflow for developing and reviewing the specification documents

---

**Document Status:** Pass 3 (Final) — Enrichment complete. Principles, API 650/agitator/appurtenance considerations, trade-offs, and examples provided. Cross-document consistency verified. Ready for WORKING_ITEMS refinement.

**Last Updated:** 2026-01-28
