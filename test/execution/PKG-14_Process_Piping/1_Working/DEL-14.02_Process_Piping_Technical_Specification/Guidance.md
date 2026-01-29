# Guidance: DEL-14.02 Process Piping Technical Specification

## Purpose

This guidance document supports the development of **Process Piping Technical Specification** for **PKG-14 Process Piping**.

**Deliverable intent** (source: Decomposition DEL-14.02; scope: Specification.md Scope; attributes: Datasheet.md Specification Type): Defines performance, materials, and workmanship requirements for process piping per ER requirements.

**Deliverable classification:**
- **Type:** Specification (Technical Specification for materials, performance, workmanship) (attributes: Datasheet.md Identification)
- **Discipline:** Mechanical (Process Piping)
- **Responsible:** D&B Contractor

**Project context** (source: Decomposition Section 1.1; scope: Specification.md Product context; applicability: Datasheet.md Conditions):
- **Facility:** Canola Oil Transload Facility — Phase 1 (Design & Build)
- **Product:** CSD (Crude Super Degummed) canola oil (food-grade product) (requirements: Specification.md FR-1, PR-2; attributes: Datasheet.md Product Handled)
- **Throughput:** 1,000,000 MT per annum (requirements: Specification.md FR-4; attributes: Datasheet.md Throughput)
- **Operation:** Transfer from rail tank cars to storage to marine export
- **Location:** Fraser Surrey Terminal, Surrey, BC (coastal/marine environment) (requirements: Specification.md FR-5, FR-7, FR-10; conditions: Datasheet.md Environmental classification)

## Principles

**Engineering rationale (Mechanical — Process Piping specification):**

**1. Material selection philosophy:**
- **Food-grade compatibility:** CSD canola oil is a food product; all piping materials must be non-toxic, non-contaminating, and suitable for food contact (source: product context; requirements: Specification.md FR-1, PR-2, PR-4; considerations: Datasheet.md Special considerations - Food-grade service; procedure: Procedure.md Step 1, Step 2a)
- **Product compatibility:** Canola oil is generally non-corrosive; carbon steel is typical for liquid service; stainless steel may be required for nitrogen distribution or clean-in-place systems (requirements: Specification.md FR-1, PR-2; materials: Datasheet.md Typical materials; trade-offs discussed below in item 1; procedure: Procedure.md Step 2a)
- **Coastal environment:** Fraser Surrey location (coastal/marine) requires external corrosion protection (coatings, corrosion allowance) for exposed piping and supports (requirements: Specification.md FR-5, FR-7, PR-3; conditions: Datasheet.md Environmental classification; considerations: Datasheet.md Special considerations - Corrosion protection; procedure: Procedure.md Step 2a, Step 2b)
- **Design life:** Material selection and corrosion allowances should support 25-year design life — **ASSUMPTION** (location TBD: ER Volume 2 Part 1; requirements: Specification.md PR-3; conditions: Datasheet.md Design life; trade-offs: item 1 below; procedure: Procedure.md Step 2a)
- **Lifecycle cost:** Material choices should consider not just initial cost but also maintenance, reliability, and replacement costs (source: OBJ-9 Lifecycle Cost Optimization; requirements: Specification.md PR-3; considerations: item 5 below; trade-offs: item 1 below; procedure: Procedure.md Step 1)

**2. ASME B31.3 Process Piping Code:**
- Governs all aspects of process piping: design, materials, fabrication, assembly, erection, examination, inspection, testing (code: Datasheet.md Applicable Standard; requirements: Specification.md QR-1, PR-1, PR-5, PR-9, PR-10; standards: Specification.md Standards - Process piping design; procedure: Procedure.md Prerequisites, Step 1, Step 2a; examples: item 5 below)
- Chapter II defines acceptable materials (pipe, fittings, flanges, bolting, gaskets) with allowable stresses and temperature limits (requirements: Specification.md QR-1; standards: Specification.md Standards - Piping materials; procedure: Procedure.md Step 1, Step 2a; examples: item 1 below, item 5 below)
- Material selection must comply with code requirements for design pressure and temperature (requirements: Specification.md FR-2, FR-3, PR-1; conditions: Datasheet.md Operating temperature range, Operating pressure; procedure: Procedure.md Step 1, Step 2a)
- **TBD** — Service classification (normal fluid service vs. high-pressure fluid service vs. toxic/flammable fluid service) affects code requirements (location TBD: ER Volume 2 Part 2; requirements: Specification.md QR-2; procedure: Procedure.md Step 1)

**3. Pipe support design philosophy:**
- Supports must accommodate all loads: dead weight, operating loads, thermal expansion, seismic, wind (source: ASME B31.3; requirements: Specification.md FR-6, FR-8; construction: Datasheet.md Construction item 2 - Design criteria; procedure: Procedure.md Step 2b; examples: item 2 below)
- Support spacing per ASME B31.3 Table 321.7.4 (typical: every 6-9 m for carbon steel pipe depending on size) (requirements: Specification.md FR-6; construction: Datasheet.md Construction item 2 - Design criteria; procedure: Procedure.md Step 2b; examples: item 2 below)
- Thermal expansion managed through expansion loops, expansion joints, or spring hangers (requirements: Specification.md FR-6; construction: Datasheet.md Construction item 2 - Support types; trade-offs: item 3 below; procedure: Procedure.md Step 2b)
- Seismic design per NBC 2020 (BC location) — **ASSUMPTION**; confirm design basis (requirements: Specification.md FR-8; conditions: Datasheet.md Seismic requirements; procedure: Procedure.md Step 2b; referenced in DEL-14.01)
- Support materials must be compatible with coastal environment (corrosion-resistant or protected) (requirements: Specification.md FR-7; conditions: Datasheet.md Environmental classification; construction: Datasheet.md Construction item 2 - Support materials; procedure: Procedure.md Step 2b)

**4. Insulation philosophy:**
- Personnel protection: Surfaces exceeding **TBD** °C require insulation to prevent burns (**ASSUMPTION**: 60°C threshold typical) (requirements: Specification.md FR-9, PR-7; construction: Datasheet.md Construction item 3; trade-offs: item 4 below; procedure: Procedure.md Step 2c)
- Energy conservation: **TBD** — extent of thermal insulation for heated lines (location TBD: ER Volume 2 Part 2; requirements: Specification.md FR-9; considerations: Datasheet.md Construction item 3 - ASSUMPTION; trade-offs: item 4 below; procedure: Procedure.md Step 2c)
- Weather protection: All outdoor insulation requires weatherproof jacketing (aluminum, stainless steel, or PVC) (requirements: Specification.md FR-10; conditions: Datasheet.md Environmental classification; construction: Datasheet.md Construction item 3 - Jacketing materials; procedure: Procedure.md Step 2c; examples: item 3 below)
- Coastal environment: Jacketing must be corrosion-resistant and sealed against moisture infiltration (requirements: Specification.md FR-10; conditions: Datasheet.md Environmental classification; procedure: Procedure.md Step 2c)

**5. Quality and traceability:**
- All pressure-containing materials require Material Test Reports (MTRs) with heat numbers and certifications (requirements: Specification.md PR-8, QR-5; construction: Datasheet.md Construction item 1 - Material testing; procedure: Procedure.md Step 2a, Step 7; verification: Specification.md Verification - Material verification; examples: item 1 below)
- Material traceability from receipt through installation critical for code compliance and future maintenance (requirements: Specification.md QR-6; procedure: Procedure.md Step 2a, Step 7; verification: Specification.md Verification - Material verification)
- Welding procedures and welder qualifications per ASME Section IX (requirements: Specification.md PR-5, QR-7; standards: Specification.md Standards - Welding and fabrication; procedure: Procedure.md Step 2a; verification: Specification.md Verification - Fabrication verification)
- Hydrostatic testing per ASME B31.3 (typically 1.5 times design pressure for 10 minutes minimum) (requirements: Specification.md PR-10; standards: Specification.md Standards - Testing and inspection; procedure: Procedure.md Step 2a; verification: Specification.md Verification - Installation verification; cross-reference DEL-14.05)

## Considerations

**Factors to consider during specification development:**

**1. Specification structure and content:**

**Piping Material Specification:**
- Material selection matrix (material by service, temperature, pressure) (requirements: Specification.md FR-1, FR-2, FR-3; procedure: Procedure.md Step 2a; examples: item 1 below)
- Pipe materials, sizes, schedules, and pressure ratings (ASTM A106 Gr. B typical for carbon steel) (requirements: Specification.md FR-1, FR-2, FR-3, FR-4; materials: Datasheet.md Typical materials - Pipe; standards: Specification.md Standards - Piping materials; procedure: Procedure.md Step 2a; examples: item 1 below)
- Fitting types and materials (ASME B16.9 butt-weld fittings standard) (construction: Datasheet.md Construction item 1 - Fitting materials; standards: Specification.md Standards - Process piping design; procedure: Procedure.md Step 2a; examples: item 1 below)
- Flange types, materials, and ratings (ASME B16.5 Class 150 or 300 typical) (construction: Datasheet.md Construction item 1 - Flange materials; materials: Datasheet.md Typical materials - Flanges; standards: Specification.md Standards - Process piping design; trade-offs: item 2 below; procedure: Procedure.md Step 2a; examples: item 1 below)
- Gasket materials (spiral-wound or compressed fiber for food service) (requirements: Specification.md PR-4; materials: Datasheet.md Typical materials - Gaskets; standards: Specification.md Standards - Process piping design; procedure: Procedure.md Step 2a; examples: item 1 below)
- Bolting materials (ASTM A193 Gr. B7 bolts typical) (construction: Datasheet.md Construction item 1 - Bolting materials; materials: Datasheet.md Typical materials - Bolting; standards: Specification.md Standards - Piping materials; procedure: Procedure.md Step 2a; examples: item 1 below)
- Special items (expansion joints, strainers, sight glasses) (construction: Datasheet.md Construction item 1 - Special items; procedure: Procedure.md Step 2a; examples: item 1 below)
- Material testing requirements (MTRs, PMI, hydrostatic testing) (requirements: Specification.md PR-8, PR-9, PR-10; construction: Datasheet.md Construction item 1 - Material testing; procedure: Procedure.md Step 2a; examples: item 1 below)

**Pipe Support Specification:**
- Support types (rigid hangers, spring hangers, saddles, shoes, anchors, guides, restraints) (requirements: Specification.md FR-6; construction: Datasheet.md Construction item 2 - Support types; procedure: Procedure.md Step 2b; examples: item 2 below)
- Support materials (carbon steel or stainless steel; coatings for corrosion protection) (requirements: Specification.md FR-7; construction: Datasheet.md Construction item 2 - Support materials; procedure: Procedure.md Step 2b; examples: item 2 below)
- Design criteria (allowable stresses, load combinations, seismic factors) (requirements: Specification.md FR-6, FR-8; construction: Datasheet.md Construction item 2 - Design criteria; procedure: Procedure.md Step 2b; examples: item 2 below)
- Support spacing and layout guidance (reference ASME B31.3 Table 321.7.4) (rationale: item 3 above; procedure: Procedure.md Step 2b; examples: item 2 below)
- Installation tolerances and adjustment provisions (requirements: Specification.md PR-6; construction: Datasheet.md Construction item 2 - Installation requirements; procedure: Procedure.md Step 2b; examples: item 2 below)
- Structural attachment details and hardware (requirements: Specification.md IR-2; construction: Datasheet.md Construction item 2 - Attachment details; procedure: Procedure.md Step 2b; examples: item 2 below)

**Insulation Specification:**
- Insulation types by service (mineral wool, cellular glass, foam) (requirements: Specification.md FR-9; construction: Datasheet.md Construction item 3 - Insulation materials; procedure: Procedure.md Step 2c; examples: item 3 below)
- Insulation thickness by temperature range (requirements: Specification.md FR-9, PR-7; construction: Datasheet.md Construction item 3 - Insulation thicknesses; procedure: Procedure.md Step 2c; examples: item 3 below)
- Jacketing materials (aluminum for most services; stainless steel for high-temperature or corrosive environments) (requirements: Specification.md FR-10; construction: Datasheet.md Construction item 3 - Jacketing materials; procedure: Procedure.md Step 2c; examples: item 3 below)
- Vapor barriers and weather sealing (requirements: Specification.md FR-10; construction: Datasheet.md Construction item 3 - Vapor barriers; procedure: Procedure.md Step 2c; examples: item 3 below)
- Application methods and workmanship standards (requirements: Specification.md PR-7; construction: Datasheet.md Construction item 3 - Application methods; procedure: Procedure.md Step 2c; examples: item 3 below)
- Inspection and testing requirements (requirements: Specification.md PR-7; standards: Specification.md Standards - Insulation; verification: Specification.md Verification - Installation verification; procedure: Procedure.md Step 2c; examples: item 3 below)

**2. Interface considerations:**
- Piping materials coordinate with equipment materials (pumps, valves, tanks) to avoid galvanic corrosion and ensure pressure/temperature compatibility (requirements: Specification.md IR-4, IR-5, IR-6; procedure: Procedure.md Prerequisites, Step 1, Step 3) — cross-reference PKG-13, PKG-15, PKG-16
- Pipe support loads coordinate with structural design (requirements: Specification.md IR-2; rationale: item 3 above; procedure: Procedure.md Step 2b, Step 3) — cross-reference PKG-05, PKG-06
- Insulation requirements coordinate with piping layout for access and clearances (requirements: Specification.md IR-3; procedure: Procedure.md Step 3) — cross-reference DEL-14.01

**3. Regulatory and code compliance:**
- ASME B31.3 is the governing code for process piping (code: Datasheet.md Applicable Standard; requirements: Specification.md QR-1; rationale: item 2 above; standards: Specification.md Standards - Process piping design)
- Food-grade service may require additional certifications or material restrictions (confirm with regulatory authority) (requirements: Specification.md FR-1; rationale: item 1 above; considerations: Datasheet.md Special considerations - Food-grade service)
- **TBD** — Transport Canada or other regulatory requirements for rail-connected piping (location TBD: ER Volume 2 Part 1)
- **TBD** — Environmental regulations affecting material selection or coating requirements (requirements: Specification.md FR-5; conditions: Datasheet.md Environmental classification)

**4. Procurement and construction:**
- Specification drives procurement: material callouts must be clear, complete, and aligned with available supplier products (requirements: Specification.md QR-4; procedure: Procedure.md Step 7; documentation: Specification.md Documentation - Integration with procurement)
- Long-lead items (specialty materials, large flanges, expansion joints) should be identified early (construction: Datasheet.md Construction item 1 - Special items; procedure: Procedure.md Step 7)
- Prefabrication opportunities: specification should support shop fabrication where practical (better quality control, faster installation) (standards: Specification.md Standards - Welding and fabrication; trade-offs: item 5 below)
- Field welding vs. shop welding: specification should allow flexibility while ensuring quality (requirements: Specification.md PR-5; standards: Specification.md Standards - Welding and fabrication; trade-offs: item 5 below)

**5. Operational and maintenance considerations:**
- Material selection affects maintenance: corrosion-resistant materials reduce long-term maintenance (source: OBJ-9; requirements: Specification.md PR-3; rationale: item 1 above; trade-offs: item 1 below)
- Insulation design affects access: removable insulation sections required at flanges, valves, instruments for maintenance (requirements: Specification.md IR-3; construction: Datasheet.md Construction item 3 - Application methods; procedure: Procedure.md Step 2c)
- Spare parts strategy: standardized materials simplify spare parts inventory (trade-offs: item 2 below)

## Trade-offs

**Competing concerns to evaluate:**

**1. Material cost vs. longevity:**
- **Trade-off:** Carbon steel (lower cost, requires corrosion allowance and coatings) vs. stainless steel (higher cost, better corrosion resistance, lower maintenance) (requirements: Specification.md FR-5, PR-3; materials: Datasheet.md Typical materials - Pipe; procedure: Procedure.md Step 2a)
- **Guidance:** For CSD canola oil liquid service (non-corrosive product), carbon steel is typical; stainless steel justified for nitrogen distribution, clean-in-place systems, or where food-contact requirements are stringent (requirements: Specification.md FR-1, IR-7; rationale: item 1 above; materials: Datasheet.md Typical materials - Pipe; procedure: Procedure.md Step 2a)
- **Consideration:** Coastal environment may favor stainless steel for critical exposed piping to reduce maintenance (source: OBJ-9 Lifecycle Cost Optimization; requirements: Specification.md FR-5; conditions: Datasheet.md Environmental classification; rationale: item 1 above)

**2. Standardization vs. optimization:**
- **Trade-off:** Standardize on a few material grades and sizes (simpler procurement, lower inventory) vs. optimize each line for minimum cost (more complexity) (considerations: item 5 above)
- **Guidance:** Standardization generally preferred for lifecycle benefits; optimize only where significant cost/performance benefit justifies complexity (rationale: item 1 above; considerations: item 5 above)
- **Example:** Standardize on ASME B16.5 Class 150 flanges for most services; use Class 300 only where pressure requires it (materials: Datasheet.md Typical materials - Flanges; requirements: Specification.md FR-3; considerations: item 1 above; procedure: Procedure.md Step 2a; referenced in DEL-14.03)

**3. Pipe support design — flexibility vs. rigidity:**
- **Trade-off:** Spring hangers allow thermal expansion but are more expensive; rigid hangers are simpler and cheaper but create higher thermal stresses (requirements: Specification.md FR-6; construction: Datasheet.md Construction item 2 - Support types; rationale: item 3 above; procedure: Procedure.md Step 2b)
- **Guidance:** Use spring hangers where thermal expansion analysis (DEL-14.03) shows high stresses; rigid hangers acceptable for most lines with adequate flexibility (expansion loops) (requirements: Specification.md FR-6; rationale: item 3 above; procedure: Procedure.md Step 2b; cross-reference DEL-14.03)
- **Consideration:** Seismic loads may require additional restraints beyond standard support spacing (requirements: Specification.md FR-8; conditions: Datasheet.md Seismic requirements; rationale: item 3 above; procedure: Procedure.md Step 2b)

**4. Insulation extent:**
- **Trade-off:** Insulate all piping (maximum personnel protection and energy conservation) vs. insulate only where required (lower cost, easier maintenance access) (requirements: Specification.md FR-9; construction: Datasheet.md Construction item 3; rationale: item 4 above; procedure: Procedure.md Step 2c)
- **Guidance:** Insulate where personnel protection required (hot surfaces) and where energy conservation justified by heat loss calculations; avoid over-insulating (adds cost and maintenance difficulty) (requirements: Specification.md FR-9, PR-7; rationale: item 4 above; procedure: Procedure.md Step 2c)
- **TBD** — Project insulation philosophy (location TBD: ER Volume 2 Part 2; requirements: Specification.md FR-9; considerations: Datasheet.md Construction item 3 - ASSUMPTION; procedure: Procedure.md Step 2c)

**5. Specification detail level:**
- **Trade-off:** Detailed prescriptive specification (tells contractor exactly what to do) vs. performance-based specification (defines outcomes, allows contractor flexibility) (scope: Specification.md Scope; procedure: Procedure.md Step 2)
- **Guidance:** For D&B (Design & Build) contract, performance-based approach with minimum mandatory requirements allows contractor optimization while ensuring code and ER compliance (requirements: Specification.md QR-1, QR-2; standards: Specification.md Standards section)
- **Balance:** Prescribe critical items (material grades, pressure ratings, testing requirements); allow flexibility on non-critical details (support types, installation methods) (procedure: Procedure.md Step 2)

## Examples

**Reference examples and precedents:**

**1. Typical piping material specification content:**
- Scope and applicability (what piping systems covered) (scope: Specification.md Scope; applicability: Datasheet.md Conditions; considerations: item 1 above)
- Referenced codes and standards (ASME B31.3, ASME B16.5, ASTM standards) (code: Datasheet.md Applicable Standard; standards: Specification.md Standards section; procedure: Procedure.md Prerequisites, Step 2a)
- Material selection table (material by service class, temperature range, pressure range) (requirements: Specification.md FR-1, FR-2, FR-3; considerations: item 1 above; procedure: Procedure.md Step 2a)
- Pipe specifications (material grade, size range, schedule or wall thickness, end preparation) (requirements: Specification.md FR-1, FR-4; construction: Datasheet.md Construction item 1; materials: Datasheet.md Typical materials - Pipe; procedure: Procedure.md Step 2a)
- Fitting specifications (material, types, size range, dimensions per ASME B16.9) (construction: Datasheet.md Construction item 1 - Fitting materials; materials: Datasheet.md Typical materials - Fittings; standards: Specification.md Standards - Process piping design; considerations: item 1 above; procedure: Procedure.md Step 2a)
- Flange specifications (material, type — slip-on, weld neck, blind — ratings, facings, dimensions per ASME B16.5) (construction: Datasheet.md Construction item 1 - Flange materials; materials: Datasheet.md Typical materials - Flanges; standards: Specification.md Standards - Process piping design; considerations: item 1 above; procedure: Procedure.md Step 2a)
- Gasket specifications (material — spiral-wound, compressed fiber — dimensions per ASME B16.20/B16.21) (requirements: Specification.md PR-4; materials: Datasheet.md Typical materials - Gaskets; standards: Specification.md Standards - Process piping design; considerations: item 1 above; procedure: Procedure.md Step 2a)
- Bolting specifications (material grade, size, length, nut material per ASTM A193/A194) (materials: Datasheet.md Typical materials - Bolting; standards: Specification.md Standards - Piping materials; considerations: item 1 above; procedure: Procedure.md Step 2a)
- Special items (expansion joints, strainers, sight glasses, sample connections) (construction: Datasheet.md Construction item 1 - Special items; considerations: item 1 above; procedure: Procedure.md Step 2a)
- Material testing and inspection (MTR requirements, dimensional inspection, PMI — positive material identification) (requirements: Specification.md PR-8, PR-9; construction: Datasheet.md Construction item 1 - Material testing; rationale: item 5 above; considerations: item 1 above; procedure: Procedure.md Step 2a; verification: Specification.md Verification - Material verification)
- Marking and identification (material stamps, heat numbers, traceability) (requirements: Specification.md QR-6; rationale: item 5 above; considerations: item 1 above; procedure: Procedure.md Step 2a; verification: Specification.md Verification - Material verification)

**2. Typical pipe support specification content:**
- Support types and applications (when to use each type) (requirements: Specification.md FR-6; construction: Datasheet.md Construction item 2 - Support types; rationale: item 3 above; considerations: item 1 above; procedure: Procedure.md Step 2b)
- Materials and finishes (carbon steel with coating, stainless steel, hardware materials) (requirements: Specification.md FR-7; construction: Datasheet.md Construction item 2 - Support materials; considerations: item 1 above; procedure: Procedure.md Step 2b)
- Design criteria (allowable stresses, load factors, seismic design factors per NBC 2020) (requirements: Specification.md FR-8; construction: Datasheet.md Construction item 2 - Design criteria; rationale: item 3 above; considerations: item 1 above; procedure: Procedure.md Step 2b)
- Support spacing guidance (reference ASME B31.3 or project-specific tables) (requirements: Specification.md FR-6; rationale: item 3 above; considerations: item 1 above; procedure: Procedure.md Step 2b)
- Thermal expansion provisions (spring hanger selection, expansion loop design) (requirements: Specification.md FR-6; rationale: item 3 above; trade-offs: item 3 above; procedure: Procedure.md Step 2b; cross-reference DEL-14.03)
- Installation requirements (tolerances, alignment, adjustment procedures) (requirements: Specification.md PR-6; construction: Datasheet.md Construction item 2 - Installation requirements; considerations: item 1 above; procedure: Procedure.md Step 2b; verification: Specification.md Verification - Installation verification)
- Typical details (standard support configurations, structural attachment details) (construction: Datasheet.md Construction item 2 - Attachment details; considerations: item 1 above; procedure: Procedure.md Step 2b; documentation: Specification.md Documentation - Typical details)

**3. Typical insulation specification content:**
- Insulation types by service (mineral wool for most services, cellular glass for cryogenic, foam for low-temperature) (requirements: Specification.md FR-9; construction: Datasheet.md Construction item 3 - Insulation materials; considerations: item 1 above; procedure: Procedure.md Step 2c)
- Insulation thickness table (thickness by pipe size and temperature range) (requirements: Specification.md FR-9; construction: Datasheet.md Construction item 3 - Insulation thicknesses; considerations: item 1 above; procedure: Procedure.md Step 2c)
- Jacketing types (aluminum for outdoor, stainless steel for high-temp or corrosive, PVC for indoor low-temp) (requirements: Specification.md FR-10; construction: Datasheet.md Construction item 3 - Jacketing materials; rationale: item 4 above; considerations: item 1 above; procedure: Procedure.md Step 2c)
- Vapor barriers and sealants (where required, materials, application methods) (requirements: Specification.md FR-10; construction: Datasheet.md Construction item 3 - Vapor barriers; considerations: item 1 above; procedure: Procedure.md Step 2c)
- Application procedures (surface preparation, insulation installation, jacketing installation, sealing) (requirements: Specification.md PR-7; construction: Datasheet.md Construction item 3 - Application methods; considerations: item 1 above; procedure: Procedure.md Step 2c)
- Quality requirements (inspection, testing, acceptance criteria) (requirements: Specification.md PR-7; standards: Specification.md Standards - Insulation; verification: Specification.md Verification - Installation verification; considerations: item 1 above; procedure: Procedure.md Step 2c)

**4. Related deliverables to review:**
- DEL-14.01 (Process Piping Design Drawing Set) — drawings reference materials specified in this deliverable (requirements: Specification.md IR-1; procedure: Procedure.md Prerequisites)
- DEL-14.03 (Process Piping Design Calculations) — calculations determine pressure ratings and wall thicknesses specified here (requirements: Specification.md FR-3, FR-6; procedure: Procedure.md Step 1, Step 2a, Step 2b)
- DEL-14.04 (Process Piping Data Sheet Package) — line list assigns material classes from this specification to each line (requirements: Specification.md IR-1; procedure: Procedure.md Step 2a)
- DEL-14.05 (Installation & Test Records) — testing and inspection verify compliance with this specification (requirements: Specification.md QR-8, PR-8, PR-9, PR-10; verification: Specification.md Verification sections)

**5. Code and standard references:**
- ASME B31.3 Chapter II — Materials (required reading for specification writers) (code: Datasheet.md Applicable Standard; requirements: Specification.md QR-1; rationale: item 2 above; standards: Specification.md Standards - Process piping design; procedure: Procedure.md Prerequisites, Step 1)
- ASME B16.5 — Pipe Flanges and Flanged Fittings (flange dimensions and ratings) (standards: Specification.md Standards - Process piping design; considerations: item 1 above; procedure: Procedure.md Prerequisites, Step 2a)
- ASME B16.9 — Butt-Welding Fittings (fitting dimensions) (standards: Specification.md Standards - Process piping design; considerations: item 1 above; procedure: Procedure.md Prerequisites, Step 2a)
- ASTM material standards (A106, A53, A312, A193, A194, etc.) — material properties and requirements (standards: Specification.md Standards - Piping materials; considerations: item 1 above; procedure: Procedure.md Prerequisites, Step 2a)
- MSS SP-58 — Pipe Hangers and Supports (support design and materials) (standards: Specification.md Standards - Pipe supports; rationale: item 3 above; considerations: item 1 above; procedure: Procedure.md Prerequisites, Step 2b)
