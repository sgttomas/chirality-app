# Procedure: DEL-14.02 Process Piping Technical Specification

## Purpose

This procedure defines the process for **producing** the **Process Piping Technical Specification** within **PKG-14 Process Piping**.

**Deliverable description** (source: Decomposition DEL-14.02; scope: Specification.md Scope; rationale: Guidance.md Purpose): Defines performance, materials, and workmanship requirements for process piping per ER requirements.

**Specification outputs** (source: Decomposition DEL-14.02; attributes: Datasheet.md Specification Sections; scope: Specification.md Scope):
- Piping Material Specification (requirements: Specification.md FR-1 through FR-5; construction: Datasheet.md Construction item 1; rationale: Guidance.md Principles item 1, item 2; examples: Guidance.md Examples item 1)
- Pipe Support Specification (requirements: Specification.md FR-6, FR-7, FR-8; construction: Datasheet.md Construction item 2; rationale: Guidance.md Principles item 3; examples: Guidance.md Examples item 2)
- Insulation Specification (requirements: Specification.md FR-9, FR-10; construction: Datasheet.md Construction item 3; rationale: Guidance.md Principles item 4; examples: Guidance.md Examples item 3)

## Prerequisites

**Dependencies:**

Per `_DEPENDENCIES.md`: **NOT_TRACKED** — Dependencies are coordinated externally by humans.

**Upstream inputs required** (rationale: Guidance.md Considerations item 2):
- Process design basis (temperatures, pressures, flow rates) (requirements: Specification.md FR-2, FR-3; conditions: Datasheet.md Operating temperature range, Operating pressure; **TBD** source)
- Piping system requirements from ER Volume 2 Part 2 (location: test/Volume_2_Part_2_Employers_Requirements.pdf; requirements: Specification.md QR-2; rationale: Guidance.md Considerations item 3)
- Preliminary piping layouts or P&IDs (cross-reference DEL-14.01) (requirements: Specification.md IR-1; rationale: Guidance.md Considerations item 2; examples: Guidance.md Examples item 4; **TBD** timing)
- Equipment material specifications (pumps, tanks, valves) (requirements: Specification.md IR-4, IR-5, IR-6; rationale: Guidance.md Considerations item 2; cross-reference PKG-13, PKG-15, PKG-16)
- Seismic and structural design criteria (requirements: Specification.md FR-8; conditions: Datasheet.md Seismic requirements; rationale: Guidance.md Principles item 3; **TBD** — location TBD: ER Volume 2 Part 1)
- Hazardous area classification study (conditions: Datasheet.md Hazardous area classification; rationale: Guidance.md Considerations item 3; **TBD** — location TBD: ER Volume 2 Part 2)

**Reference materials:**
- ASME B31.3 — Process Piping (code text and commentary) (code: Datasheet.md Applicable Standard; requirements: Specification.md QR-1; rationale: Guidance.md Principles item 2; standards: Specification.md Standards - Process piping design; examples: Guidance.md Examples item 5)
- ASME B16.5, B16.9, B16.11, B16.20, B16.21 — Flanges, fittings, gaskets (standards: Specification.md Standards - Process piping design; rationale: Guidance.md Considerations item 1; examples: Guidance.md Examples item 1, item 5)
- ASTM material standards (A106, A53, A312, A193, A194, etc.) (standards: Specification.md Standards - Piping materials; rationale: Guidance.md Considerations item 1; examples: Guidance.md Examples item 1, item 5)
- MSS SP-58, MSS SP-69 — Pipe hangers and supports (if applicable) (standards: Specification.md Standards - Pipe supports; rationale: Guidance.md Principles item 3; examples: Guidance.md Examples item 2, item 5)
- Employer's Requirements Volume 2 Part 1 and Part 2 (requirements: Specification.md QR-2, Standards - Project-specific requirements; rationale: Guidance.md Considerations item 3)
- **TBD** — Insulation standards (ASTM C547, C552, or equivalent) (standards: Specification.md Standards - Insulation; rationale: Guidance.md Principles item 4)

**Personnel requirements:**
- **Lead Engineer:** Mechanical engineer with process piping specification experience (requirements: Specification.md QR-3; rationale: Guidance.md Principles item 2; **TBD** qualifications)
- **Materials Engineer:** Specialist in materials selection and corrosion (if available) (rationale: Guidance.md Principles item 1; **TBD**)
- **Checker:** Independent reviewer qualified in process piping (requirements: Specification.md QR-3; verification: Specification.md Verification - Specification review; **TBD**)
- **Approver:** Discipline Lead or Project Engineer (requirements: Specification.md QR-3; **TBD**)

## Steps

### Step 1: Requirements Gathering and Review

**Objective:** Compile all applicable requirements, codes, and standards (requirements: Specification.md QR-1, QR-2; rationale: Guidance.md Principles item 1, item 2; verification: Specification.md Verification - Specification review).

**Actions:**
1. Review Employer's Requirements Volume 2 Part 2 for process piping material and workmanship requirements (location: test/Volume_2_Part_2_Employers_Requirements.pdf; requirements: Specification.md QR-2; rationale: Guidance.md Considerations item 3; examples: Guidance.md Examples item 4) — extract relevant clauses
2. Review ASME B31.3 for material requirements (Chapter II) and allowable materials table (code: Datasheet.md Applicable Standard; requirements: Specification.md QR-1; rationale: Guidance.md Principles item 2; standards: Specification.md Standards - Process piping design; examples: Guidance.md Examples item 5)
3. Review project objectives (OBJ-1 Safety, OBJ-2 Throughput, OBJ-9 Lifecycle Cost) for material selection drivers (scope: Specification.md Product context; rationale: Guidance.md Principles item 1; considerations: Guidance.md Considerations item 5)
4. Identify service conditions:
   - Product: CSD canola oil (food-grade, non-corrosive) (product: Datasheet.md Product Handled; scope: Specification.md Product context; requirements: Specification.md FR-1; rationale: Guidance.md Principles item 1)
   - Temperature range: **TBD** (from process design basis) (conditions: Datasheet.md Operating temperature range; requirements: Specification.md FR-2; prerequisites above)
   - Pressure range: **TBD** (from process design basis or DEL-14.03) (conditions: Datasheet.md Operating pressure; requirements: Specification.md FR-3; cross-reference DEL-14.03)
   - Environmental: Coastal/marine (Fraser Surrey, BC) (conditions: Datasheet.md Environmental classification; requirements: Specification.md FR-5, FR-7, FR-10; rationale: Guidance.md Principles item 1)
5. Review preliminary piping layouts (DEL-14.01) to understand piping systems and routing (requirements: Specification.md IR-1; examples: Guidance.md Examples item 4; cross-reference DEL-14.01)
6. Collect equipment interface requirements (material compatibility with pumps, tanks, valves) (requirements: Specification.md IR-4, IR-5, IR-6; rationale: Guidance.md Considerations item 2; prerequisites above)

**Verification:** Requirements compilation reviewed and approved by discipline lead (verification: Specification.md Verification - Specification review; verification table row: Step 1).

---

### Step 2: Material Selection and Specification Development

**Objective:** Select appropriate materials and develop piping material specification (requirements: Specification.md FR-1 through FR-10; rationale: Guidance.md Principles items 1-4; considerations: Guidance.md Considerations item 1).

**Actions:**

**2a. Develop Piping Material Specification:**
1. Define scope and applicability (PKG-14 process piping systems) (scope: Specification.md Scope; applicability: Datasheet.md Conditions; rationale: Guidance.md Purpose; examples: Guidance.md Examples item 1)
2. List referenced codes and standards (ASME, ASTM, etc.) (code: Datasheet.md Applicable Standard; standards: Specification.md Standards section; rationale: Guidance.md Principles item 2; examples: Guidance.md Examples item 1)
3. Create material selection matrix:
   - Material by service class (liquid canola oil, nitrogen, CIP, etc.) (requirements: Specification.md FR-1, IR-7; rationale: Guidance.md Principles item 1; considerations: Guidance.md Considerations item 1; examples: Guidance.md Examples item 1)
   - Material by temperature range and pressure range (requirements: Specification.md FR-2, FR-3; rationale: Guidance.md Principles item 2; examples: Guidance.md Examples item 1)
   - **ASSUMPTION**: Carbon steel (ASTM A106 Gr. B) for canola oil liquid service; stainless steel (ASTM A312 Gr. 304/316) for nitrogen and CIP (materials: Datasheet.md Typical materials - Pipe; requirements: Specification.md FR-1; rationale: Guidance.md Principles item 1; trade-offs: Guidance.md Trade-offs item 1)
4. Specify pipe materials:
   - Material grade (ASTM A106 Gr. B, A53 Gr. B, A312 Gr. 304, etc.) (materials: Datasheet.md Typical materials - Pipe; standards: Specification.md Standards - Piping materials; examples: Guidance.md Examples item 1)
   - Size range (DN 25 to DN 400 typical — confirm per DEL-14.03 sizing calculations) (requirements: Specification.md FR-4; cross-reference DEL-14.03; cross-reference DEL-14.01)
   - Schedule or wall thickness (per ASME B31.3 pressure design) (requirements: Specification.md PR-1; rationale: Guidance.md Principles item 2; cross-reference DEL-14.03)
   - End preparation (plain end, beveled for welding) (examples: Guidance.md Examples item 1)
5. Specify fitting materials:
   - Butt-weld fittings per ASME B16.9 (elbows, tees, reducers, caps) (construction: Datasheet.md Construction item 1 - Fitting materials; materials: Datasheet.md Typical materials - Fittings; standards: Specification.md Standards - Process piping design; considerations: Guidance.md Considerations item 1; examples: Guidance.md Examples item 1)
   - Socket-weld fittings per ASME B16.11 (small bore DN 50 and under) (materials: Datasheet.md Typical materials - Fittings; standards: Specification.md Standards - Process piping design; examples: Guidance.md Examples item 1)
   - Material grades matching pipe materials (requirements: Specification.md FR-1; rationale: Guidance.md Principles item 1)
6. Specify flange materials:
   - Flange types (weld neck, slip-on, blind per ASME B16.5) (construction: Datasheet.md Construction item 1 - Flange materials; standards: Specification.md Standards - Process piping design; considerations: Guidance.md Considerations item 1; examples: Guidance.md Examples item 1)
   - Flange ratings (Class 150 or 300 per design pressure — confirm per DEL-14.03) (materials: Datasheet.md Typical materials - Flanges; requirements: Specification.md FR-3; trade-offs: Guidance.md Trade-offs item 2; cross-reference DEL-14.03)
   - Flange facings (raised face standard; ring-type joint if high-pressure) (examples: Guidance.md Examples item 1)
   - Material grades (ASTM A105 for carbon steel, A182 Gr. F304/F316 for stainless steel) (materials: Datasheet.md Typical materials - Flanges; standards: Specification.md Standards - Piping materials; examples: Guidance.md Examples item 1)
7. Specify gasket materials:
   - Spiral-wound gaskets with filler (ASME B16.20) for critical services (materials: Datasheet.md Typical materials - Gaskets; requirements: Specification.md PR-4; standards: Specification.md Standards - Process piping design; considerations: Guidance.md Considerations item 1; examples: Guidance.md Examples item 1)
   - Compressed non-asbestos fiber gaskets (ASME B16.21) for general services (materials: Datasheet.md Typical materials - Gaskets; requirements: Specification.md PR-4; examples: Guidance.md Examples item 1)
   - Food-grade compatible materials (no contamination of product) (requirements: Specification.md PR-4; rationale: Guidance.md Principles item 1; considerations: Datasheet.md Special considerations - Food-grade service)
8. Specify bolting materials:
   - ASTM A193 Gr. B7 bolts with A194 Gr. 2H nuts (standard for carbon steel flanges) (materials: Datasheet.md Typical materials - Bolting; standards: Specification.md Standards - Piping materials; considerations: Guidance.md Considerations item 1; examples: Guidance.md Examples item 1)
   - ASTM A193 Gr. B8 (stainless steel) for stainless steel flanges or corrosive environments (materials: Datasheet.md Typical materials - Bolting; requirements: Specification.md FR-5; examples: Guidance.md Examples item 1)
   - Bolt lengths and sizes per ASME B16.5 (standards: Specification.md Standards - Process piping design; examples: Guidance.md Examples item 1)
9. Specify special items:
   - Expansion joints (material, type, ratings) (construction: Datasheet.md Construction item 1 - Special items; requirements: Specification.md FR-6; considerations: Guidance.md Considerations item 4; examples: Guidance.md Examples item 1; **TBD** if required)
   - Strainers (Y-type, basket type) — material and mesh size per service (construction: Datasheet.md Construction item 1 - Special items; examples: Guidance.md Examples item 1)
   - Sight glasses (material, pressure rating) (construction: Datasheet.md Construction item 1 - Special items; examples: Guidance.md Examples item 1; **TBD** if required)
10. Define material testing and inspection requirements:
    - Material Test Reports (MTRs) required for all pressure-containing components (requirements: Specification.md PR-8, QR-5; construction: Datasheet.md Construction item 1 - Material testing; rationale: Guidance.md Principles item 5; considerations: Guidance.md Considerations item 1; verification: Specification.md Verification - Material verification; examples: Guidance.md Examples item 1)
    - Positive Material Identification (PMI) for critical welds (construction: Datasheet.md Construction item 1 - Material testing; rationale: Guidance.md Principles item 5; examples: Guidance.md Examples item 1)
    - Dimensional inspection per applicable ASME/ASTM standards (verification: Specification.md Verification - Material verification)
11. Define marking and traceability requirements (heat numbers, material stamps) (requirements: Specification.md QR-6; rationale: Guidance.md Principles item 5; considerations: Guidance.md Considerations item 1; verification: Specification.md Verification - Material verification; examples: Guidance.md Examples item 1)

**2b. Develop Pipe Support Specification:**
1. Define support types and applications:
   - Rigid hangers (rod hangers, clevis hangers) (construction: Datasheet.md Construction item 2 - Support types; requirements: Specification.md FR-6; considerations: Guidance.md Considerations item 1; examples: Guidance.md Examples item 2)
   - Spring hangers (variable spring, constant support) (construction: Datasheet.md Construction item 2 - Support types; requirements: Specification.md FR-6; rationale: Guidance.md Principles item 3; trade-offs: Guidance.md Trade-offs item 3; examples: Guidance.md Examples item 2)
   - Saddles and shoes (construction: Datasheet.md Construction item 2 - Support types; examples: Guidance.md Examples item 2)
   - Anchors, guides, restraints (for thermal expansion and seismic) (construction: Datasheet.md Construction item 2 - Support types; requirements: Specification.md FR-6, FR-8; rationale: Guidance.md Principles item 3; examples: Guidance.md Examples item 2)
2. Specify support materials:
   - Carbon steel (ASTM A36 or equivalent) with corrosion-protective coating (construction: Datasheet.md Construction item 2 - Support materials; requirements: Specification.md FR-7; rationale: Guidance.md Principles item 1, item 3; considerations: Guidance.md Considerations item 1; examples: Guidance.md Examples item 2)
   - Stainless steel (ASTM A240 Gr. 304) for corrosive environments (construction: Datasheet.md Construction item 2 - Support materials; requirements: Specification.md FR-7; trade-offs: Guidance.md Trade-offs item 1; examples: Guidance.md Examples item 2)
   - Hardware materials (rods, clevises, U-bolts) (construction: Datasheet.md Construction item 2 - Support materials; examples: Guidance.md Examples item 2)
3. Define design criteria:
   - Allowable stresses per AISC 360 or equivalent (construction: Datasheet.md Construction item 2 - Design criteria; standards: Specification.md Standards - Pipe supports; examples: Guidance.md Examples item 2)
   - Load combinations (dead load + operating load + thermal + seismic + wind) (requirements: Specification.md FR-6, FR-8; construction: Datasheet.md Construction item 2 - Design criteria; rationale: Guidance.md Principles item 3; examples: Guidance.md Examples item 2)
   - Seismic design factors per NBC 2020 (requirements: Specification.md FR-8; conditions: Datasheet.md Seismic requirements; rationale: Guidance.md Principles item 3; examples: Guidance.md Examples item 2) — **TBD** site-specific seismic criteria
4. Provide support spacing guidance:
   - Reference ASME B31.3 Table 321.7.4 for maximum spacing by pipe size (requirements: Specification.md FR-6; rationale: Guidance.md Principles item 3; considerations: Guidance.md Considerations item 1; examples: Guidance.md Examples item 2)
   - Adjust for specific conditions (high-temperature, heavy valves, changes in direction) (requirements: Specification.md FR-6; examples: Guidance.md Examples item 2)
5. Define thermal expansion provisions:
   - Spring hanger selection criteria (where required per DEL-14.03 stress analysis) (requirements: Specification.md FR-6; trade-offs: Guidance.md Trade-offs item 3; examples: Guidance.md Examples item 2; cross-reference DEL-14.03)
   - Expansion loop design guidance (requirements: Specification.md FR-6; rationale: Guidance.md Principles item 3; examples: Guidance.md Examples item 2)
6. Specify installation requirements:
   - Installation tolerances (elevation, alignment) (requirements: Specification.md PR-6; construction: Datasheet.md Construction item 2 - Installation requirements; considerations: Guidance.md Considerations item 1; verification: Specification.md Verification - Installation verification; examples: Guidance.md Examples item 2)
   - Adjustment provisions (for thermal growth, settlement) (construction: Datasheet.md Construction item 2 - Installation requirements; examples: Guidance.md Examples item 2)
   - Structural attachment details (embed plates, beam clamps, drilled anchors) (requirements: Specification.md IR-2; construction: Datasheet.md Construction item 2 - Attachment details; considerations: Guidance.md Considerations item 1, item 2; examples: Guidance.md Examples item 2)
7. Provide typical details (standard support configurations, sketches) (construction: Datasheet.md Construction item 2; considerations: Guidance.md Considerations item 1; documentation: Specification.md Documentation - Typical details; examples: Guidance.md Examples item 2)

**2c. Develop Insulation Specification:**
1. Define insulation requirements and extent:
   - Personnel protection (surfaces over **TBD** °C — **ASSUMPTION**: 60°C) (requirements: Specification.md FR-9; rationale: Guidance.md Principles item 4; trade-offs: Guidance.md Trade-offs item 4)
   - Energy conservation — **TBD** philosophy (location TBD: ER Volume 2 Part 2; requirements: Specification.md FR-9; construction: Datasheet.md Construction item 3 - ASSUMPTION; rationale: Guidance.md Principles item 4; trade-offs: Guidance.md Trade-offs item 4)
   - Freeze protection (if applicable for outdoor piping in winter) (conditions: Datasheet.md Environmental classification; examples: Guidance.md Examples item 3)
2. Specify insulation types by service:
   - Mineral wool (fiberglass or rock wool) for most services (ambient to 450°C) (construction: Datasheet.md Construction item 3 - Insulation materials; requirements: Specification.md FR-9; considerations: Guidance.md Considerations item 1; examples: Guidance.md Examples item 3)
   - Cellular glass for cryogenic services (if applicable) (construction: Datasheet.md Construction item 3 - Insulation materials; standards: Specification.md Standards - Insulation; examples: Guidance.md Examples item 3)
   - Foam insulation for low-temperature services (chilled lines) (construction: Datasheet.md Construction item 3 - Insulation materials; examples: Guidance.md Examples item 3)
3. Provide insulation thickness table:
   - Thickness by pipe size and operating temperature (construction: Datasheet.md Construction item 3 - Insulation thicknesses; requirements: Specification.md FR-9, PR-7; considerations: Guidance.md Considerations item 1; examples: Guidance.md Examples item 3)
   - Reference ASTM standards or manufacturer data for thermal performance (standards: Specification.md Standards - Insulation; examples: Guidance.md Examples item 3)
4. Specify jacketing materials:
   - Aluminum (0.4mm or 0.5mm) for outdoor piping (weather protection) (construction: Datasheet.md Construction item 3 - Jacketing materials; requirements: Specification.md FR-10; rationale: Guidance.md Principles item 4; considerations: Guidance.md Considerations item 1; examples: Guidance.md Examples item 3)
   - Stainless steel (0.4mm) for high-temperature or corrosive environments (construction: Datasheet.md Construction item 3 - Jacketing materials; requirements: Specification.md FR-10; conditions: Datasheet.md Environmental classification; examples: Guidance.md Examples item 3)
   - PVC for indoor low-temperature applications (construction: Datasheet.md Construction item 3 - Jacketing materials; examples: Guidance.md Examples item 3)
5. Define vapor barriers and weather sealing:
   - Vapor barrier requirements for cold services (prevent moisture infiltration) (construction: Datasheet.md Construction item 3 - Vapor barriers; requirements: Specification.md FR-10; considerations: Guidance.md Considerations item 1; examples: Guidance.md Examples item 3)
   - Sealants and joint tape for weather protection (construction: Datasheet.md Construction item 3 - Vapor barriers; requirements: Specification.md FR-10; rationale: Guidance.md Principles item 4; examples: Guidance.md Examples item 3)
   - Coating or mastic for corrosion protection under insulation (CUI) (requirements: Specification.md FR-10; conditions: Datasheet.md Environmental classification; examples: Guidance.md Examples item 3)
6. Specify application procedures:
   - Surface preparation (cleaning, priming) (construction: Datasheet.md Construction item 3 - Application methods; requirements: Specification.md PR-7; considerations: Guidance.md Considerations item 1; examples: Guidance.md Examples item 3)
   - Insulation installation (wrapping, securing, sealing joints) (construction: Datasheet.md Construction item 3 - Application methods; requirements: Specification.md PR-7; examples: Guidance.md Examples item 3)
   - Jacketing installation (overlaps, fastening, sealing) (construction: Datasheet.md Construction item 3 - Application methods; requirements: Specification.md PR-7; examples: Guidance.md Examples item 3)
   - Removable insulation sections at flanges, valves, instruments (requirements: Specification.md IR-3; considerations: Guidance.md Considerations item 5; examples: Guidance.md Examples item 3)
7. Define inspection and testing requirements:
   - Visual inspection of installation quality (requirements: Specification.md PR-7; verification: Specification.md Verification - Installation verification; examples: Guidance.md Examples item 3)
   - Thickness verification (requirements: Specification.md PR-7; examples: Guidance.md Examples item 3)
   - Leak testing of jacketing seams (if applicable) (examples: Guidance.md Examples item 3)

**Verification:**
- Material selections reviewed for code compliance, product compatibility, and environmental suitability (requirements: Specification.md QR-1, QR-2, FR-1, FR-5; rationale: Guidance.md Principles item 1, item 2; verification: Specification.md Verification - Specification review; verification table row: Step 2)
- Specifications reviewed for completeness and consistency with design basis (verification: Specification.md Verification - Specification review; verification table row: Step 2)

---

### Step 3: Technical Review (Interdisciplinary Check)

**Objective:** Coordinate specifications with other disciplines and resolve conflicts (requirements: Specification.md IR-1, IR-2, IR-3; rationale: Guidance.md Considerations item 2; verification: Specification.md Verification - Specification review).

**Actions:**
1. Distribute specifications to:
   - Process engineer — verify product compatibility and service conditions (requirements: Specification.md FR-1, PR-2; rationale: Guidance.md Principles item 1)
   - Structural engineer — verify pipe support loads and seismic criteria (requirements: Specification.md IR-2, FR-8; rationale: Guidance.md Principles item 3; cross-reference PKG-05, PKG-06)
   - Equipment engineers — verify material compatibility with pumps, tanks, valves (requirements: Specification.md IR-4, IR-5, IR-6; rationale: Guidance.md Considerations item 2; cross-reference PKG-13, PKG-15, PKG-16)
   - Instrumentation — verify insulation access for instruments (requirements: Specification.md IR-3; considerations: Guidance.md Considerations item 5)
2. Conduct review meeting or collect written comments (requirements: Specification.md QR-3; verification: Specification.md Verification - Specification review; verification table row: Step 3)
3. Address comments:
   - Material conflicts (e.g., galvanic corrosion between dissimilar materials) (rationale: Guidance.md Considerations item 2)
   - Support load or attachment issues (requirements: Specification.md IR-2; rationale: Guidance.md Principles item 3)
   - Insulation access or clearance issues (requirements: Specification.md IR-3)
4. Update specifications based on review comments

**Verification:** Interdisciplinary check sign-off from all affected disciplines (verification: Specification.md Verification - Specification review; verification table row: Step 3).

---

### Step 4: Independent Check

**Objective:** Peer review by qualified independent checker (requirements: Specification.md QR-3; verification: Specification.md Verification - Specification review).

**Actions:**
1. Assign independent checker (mechanical engineer, not involved in original drafting) (personnel requirements: Prerequisites section; requirements: Specification.md QR-3)
2. Checker reviews specifications for:
   - Code compliance (ASME B31.3, ASME B16.x, ASTM standards) (requirements: Specification.md QR-1; code: Datasheet.md Applicable Standard; rationale: Guidance.md Principles item 2; standards: Specification.md Standards section)
   - Completeness (all required content present) (scope: Specification.md Scope; construction: Datasheet.md Construction section)
   - Material compatibility (pipe/fitting/flange/gasket materials consistent) (requirements: Specification.md FR-1, PR-2; rationale: Guidance.md Principles item 1; considerations: Guidance.md Considerations item 1)
   - Constructability (can materials be procured and installed as specified) (considerations: Guidance.md Considerations item 4, item 5; trade-offs: Guidance.md Trade-offs item 5)
   - ER compliance (requirements: Specification.md QR-2; rationale: Guidance.md Considerations item 3)
3. Checker issues comments (red markup or comment log)
4. Originator addresses comments and updates specifications
5. Checker verifies comment resolution and signs off (requirements: Specification.md QR-3)

**Verification:** Checker sign-off confirming review complete and comments resolved (verification: Specification.md Verification - Specification review; verification table row: Step 4).

---

### Step 5: Employer Review (if required)

**Objective:** Submit specifications to Employer for review and approval (requirements: Specification.md QR-3; rationale: Guidance.md Considerations item 3; verification: Specification.md Verification - Specification review).

**Actions:**
1. Prepare submittal package:
   - Piping Material Specification (scope: Specification.md Scope; construction: Datasheet.md Construction item 1)
   - Pipe Support Specification (scope: Specification.md Scope; construction: Datasheet.md Construction item 2)
   - Insulation Specification (scope: Specification.md Scope; construction: Datasheet.md Construction item 3)
   - Transmittal letter with submittal code (e.g., "IFA" — Issued for Approval) (documentation: Specification.md Documentation - Submittal requirements)
2. Submit to Employer per project submittal procedures (documentation: Specification.md Documentation - Submittal requirements; **TBD** submittal schedule and process — location TBD: ER Volume 2 Part 1)
3. Await Employer comments
4. Address Employer comments:
   - Revise specifications per Employer requirements (requirements: Specification.md QR-2, QR-3)
   - Respond to comments with explanations or justifications as needed
5. Resubmit if required

**Verification:** Employer approval received (or "No Comment" or "Noted" per submittal code) (verification: Specification.md Verification - Specification review, Acceptance criteria; verification table row: Step 5).

---

### Step 6: Approval and Issuance

**Objective:** Finalize and issue specifications for use in procurement and construction (requirements: Specification.md QR-3; documentation: Specification.md Documentation section).

**Actions:**
1. Incorporate all review comments and Employer approvals (from Steps 3-5)
2. Discipline lead reviews final specifications for overall consistency and completeness (requirements: Specification.md QR-3; verification: Specification.md Verification - Specification review; verification table row: Step 6)
3. Approver signs specifications (or electronic approval per project procedures) (personnel requirements: Prerequisites section; attributes: Datasheet.md Revision)
4. Issue specifications per project document control procedures:
   - Issuance code: **TBD** (e.g., "IFC" — Issued for Construction) (attributes: Datasheet.md Classification, Revision; documentation: Specification.md Documentation section)
   - Revision control per project numbering system (attributes: Datasheet.md Document Number, Revision; requirements: Specification.md QR-3; documentation: Specification.md Documentation - Revision control)
5. Place issued copies in `3_Issued/` folder (documentation: Specification.md Documentation - Storage location; records: Records section - Storage locations)
6. Distribute to procurement, fabrication, and construction teams (considerations: Guidance.md Considerations item 4; documentation: Specification.md Documentation - Integration with procurement; records: Records section - Distribution)
7. Update document register and transmittal log (requirements: Specification.md QR-3; documentation: Specification.md Documentation - Revision control)

**Verification:** Approver sign-off confirming specifications ready for use (verification: Specification.md Verification - Acceptance criteria; verification table row: Step 6).

---

### Step 7: Procurement Support (Ongoing)

**Objective:** Support procurement activities using the specifications (requirements: Specification.md QR-4, QR-5, QR-6; rationale: Guidance.md Principles item 5; considerations: Guidance.md Considerations item 4; documentation: Specification.md Documentation - Integration with procurement).

**Actions:**
1. Provide specifications to procurement team for material RFQs (Request for Quotations) and purchase orders (considerations: Guidance.md Considerations item 4; documentation: Specification.md Documentation - Integration with procurement; records: Records section - Distribution)
2. Review material submittals from vendors:
   - Material certifications (MTRs, test reports) (requirements: Specification.md PR-8, QR-5; rationale: Guidance.md Principles item 5; verification: Specification.md Verification - Material verification)
   - Product data sheets
   - Deviations or substitutions from specification (requirements: Specification.md QR-4; trade-offs: Guidance.md Trade-offs item 2)
3. Approve or reject material submittals (verification: Specification.md Verification - Material verification; verification table row: Step 7)
4. Track long-lead items and expedite as needed (construction: Datasheet.md Construction item 1 - Special items; considerations: Guidance.md Considerations item 4)
5. Update specifications if approved substitutions or changes occur (with revision control) (attributes: Datasheet.md Revision; requirements: Specification.md QR-3; documentation: Specification.md Documentation - As-built documentation)

**Verification:** Material procured complies with approved specifications (requirements: Specification.md QR-4, QR-5; verification: Specification.md Verification - Material verification, Acceptance criteria; verification table row: Step 7).

---

## Verification

**Verification activities summary:**

| Step | Verification Method | Acceptance Criteria |
|------|---------------------|---------------------|
| 1. Requirements Gathering | Discipline lead review | All requirements compiled and confirmed (requirements: Specification.md QR-1, QR-2) |
| 2. Specification Development | Code compliance check | Materials comply with ASME B31.3 and ER; specifications complete (requirements: Specification.md QR-1, QR-2, FR-1 through FR-10; verification: Specification.md Verification - Specification review) |
| 3. Technical Review (IDC) | Interdisciplinary review | All disciplines sign off; no unresolved conflicts (requirements: Specification.md IR-1, IR-2, IR-3; verification: Specification.md Verification - Specification review) |
| 4. Independent Check | Peer review by qualified checker | Checker sign-off; all comments resolved (requirements: Specification.md QR-3; verification: Specification.md Verification - Specification review) |
| 5. Employer Review (if required) | Employer submittal review | Employer approval or acceptance (requirements: Specification.md QR-3; verification: Specification.md Verification - Specification review, Acceptance criteria) |
| 6. Approval and Issuance | Discipline lead approval | Specifications approved for issue (requirements: Specification.md QR-3; verification: Specification.md Verification - Acceptance criteria) |
| 7. Procurement Support | Material submittal review | Materials comply with specifications (requirements: Specification.md QR-4, QR-5, QR-6; verification: Specification.md Verification - Material verification, Acceptance criteria) |

**Overall acceptance criteria:**
- Specifications comply with ASME B31.3 material requirements (Chapter II) (code: Datasheet.md Applicable Standard; requirements: Specification.md QR-1; rationale: Guidance.md Principles item 2; verification: Specification.md Verification - Acceptance criteria)
- Materials suitable for CSD canola oil service (food-grade, product-compatible) (requirements: Specification.md FR-1, PR-2; rationale: Guidance.md Principles item 1; verification: Specification.md Verification - Acceptance criteria)
- Materials suitable for coastal/marine environment (corrosion-resistant or protected) (requirements: Specification.md FR-5, FR-7; conditions: Datasheet.md Environmental classification; verification: Specification.md Verification - Acceptance criteria)
- All interdisciplinary coordination issues resolved (requirements: Specification.md IR-1, IR-2, IR-3; verification: Specification.md Verification - Specification review, Acceptance criteria)
- Employer approval received (if required) (requirements: Specification.md QR-3; verification: Specification.md Verification - Acceptance criteria)
- Specifications approved for procurement and construction use (verification: Specification.md Verification - Acceptance criteria)

---

## Records

**Documentation outputs:**

**Specification documents** (source: Decomposition DEL-14.02; attributes: Datasheet.md Specification Sections; scope: Specification.md Scope; documentation: Specification.md Documentation section):
- Piping Material Specification (pipe, fittings, flanges, gaskets, bolting, special items, testing requirements) (construction: Datasheet.md Construction item 1; requirements: Specification.md FR-1 through FR-5; examples: Guidance.md Examples item 1)
- Pipe Support Specification (support types, materials, design criteria, installation requirements) (construction: Datasheet.md Construction item 2; requirements: Specification.md FR-6, FR-7, FR-8; examples: Guidance.md Examples item 2)
- Insulation Specification (insulation materials, thicknesses, jacketing, application procedures) (construction: Datasheet.md Construction item 3; requirements: Specification.md FR-9, FR-10; examples: Guidance.md Examples item 3)

**Supporting records:**
- Material selection basis memo (rationale for material choices, service conditions, compatibility) (rationale: Guidance.md Principles item 1; documentation: Specification.md Documentation - Supporting documentation; examples: Guidance.md Examples item 4)
- Interdisciplinary check (IDC) records (comments, responses, sign-offs) (verification: Specification.md Verification - Specification review; verification table: Step 3)
- Independent check records (check comments, resolutions, sign-off) (verification: Specification.md Verification - Specification review; verification table: Step 4)
- Employer submittal and approval records (transmittals, Employer comments, responses) (verification: Specification.md Verification - Specification review; verification table: Step 5)
- Specification revision history (tracking all changes and approvals) (attributes: Datasheet.md Revision; requirements: Specification.md QR-3; documentation: Specification.md Documentation - Revision control)

**Record management:**

**Storage locations:**
- Working files: `1_Working/DEL-14.02_Process_Piping_Technical_Specification/` (documentation: Specification.md Documentation - Storage location)
- Review copies: `2_Checking/To/` (issued for review) (documentation: Specification.md Documentation - Storage location)
- Issued copies: `3_Issued/` (approved specifications with revision control) (attributes: Datasheet.md Revision; documentation: Specification.md Documentation - Storage location; Step 6 above)

**Electronic format:**
- **TBD** — **ASSUMPTION**: PDF for issued specifications; Word/native format for working copies (documentation: Specification.md Documentation - Electronic format)
- **TBD** — Document management system (DMS) for controlled issuance and revision tracking (attributes: Datasheet.md Revision; requirements: Specification.md QR-3)

**Retention:**
- **TBD** — Specification retention period per contract or regulatory requirements (location TBD: ER Volume 2 Part 1; documentation: Specification.md Documentation - Submittal requirements)
- **ASSUMPTION**: Permanent retention as part of project record

**Distribution:**
- Procurement team (for material RFQs and purchase orders) (considerations: Guidance.md Considerations item 4; documentation: Specification.md Documentation - Integration with procurement; Step 7 above)
- Fabrication contractors (for piping fabrication and installation) (considerations: Guidance.md Considerations item 4)
- Construction management (for quality control and inspection) (verification: Specification.md Verification - Fabrication verification, Installation verification; cross-reference DEL-14.05)
- Employer (as required per contract) (requirements: Specification.md QR-3; Step 5 above)
