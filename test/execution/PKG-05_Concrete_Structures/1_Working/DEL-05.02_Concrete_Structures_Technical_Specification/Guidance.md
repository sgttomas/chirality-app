# Guidance: DEL-05.02 Concrete Structures Technical Specification

## Purpose

- Guide drafting of the **Concrete Structures Technical Specification** so it captures performance/material/workmanship requirements required by the Employer's Requirements. (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:233.)
- Ensure the specification supports PKG-05's role in storage capacity (OBJ-3: 45,000 MT) and environmental protection (OBJ-7) by emphasizing durability and containment-related requirements. (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:782; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:786; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:41-42.)
- Provide specification language that supports quality construction, clear acceptance criteria, and effective QA/QC verification for DEL-05.04 records. (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:235.)

## Principles

**P-01: Requirement Clarity (Measurable and Verifiable)**
Use "shall" statements with measurable acceptance criteria and explicit verification hooks (test/inspection/record) so QA/QC can generate DEL-05.04 records without ambiguity:
- Each requirement should have a clear acceptance criterion (e.g., "minimum 28-day compressive strength of X MPa")
- Each requirement should specify verification method (e.g., "verify by cylinder testing per CSA A23.1")
- Each hold point should be explicit (e.g., "hold concrete placement until rebar inspection approved")
- Avoid ambiguous language ("adequate," "sufficient," "as required") — use specific values or reference standards
(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:235; Specification.md: FR-06; Specification.md: FR-09; Specification.md: QR-02.)

**P-02: Durability-First Framing**
Structure requirements around exposure/durability classes and workmanship controls as defined in Employer's Requirements:
- Organize concrete specification by exposure class (not just by element type)
- Lead with durability requirements (w/c ratio, cover, air entrainment) before mix design details
- Emphasize curing and protection requirements for long-term durability
- Address BC coastal environment exposure (freeze-thaw, marine exposure if applicable, seasonal conditions)
- Align with OBJ-9 Lifecycle Cost Optimization through durable materials and construction quality
**TBD:** Specific exposure class definitions from Employer's Requirements Volume 2 Part 2 concrete section.
(Source: test/Volume_2_Part_2_Employers_Requirements.pdf, location TBD; Datasheet.md: Conditions; Specification.md: FR-03; Specification.md: PR-01.)

**P-03: Containment Sensitivity (OBJ-7 Environmental Protection)**
Pay special attention to joints, penetrations, liners, and waterstops where concrete interfaces with containment or ground liner system:
- Emphasize quality control for containment structures (enhanced inspection, testing, acceptance)
- Specify joint construction details (construction joints, control joints, expansion joints)
- Specify waterstop installation and testing requirements
- Specify penetration sealing requirements
- Specify liner interface requirements (surface preparation, termination details)
- Provide clear acceptance criteria for containment integrity
(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:226; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:786; Specification.md: FR-05; Specification.md: PR-03.)

**P-04: Evidence-Based Standards (No Invented Requirements)**
Where referenced codes/standards are not accessible from Employer's Requirements, label them **TBD** and cite the Employer's Requirements as source-of-truth:
- Reference specific code sections in requirements (e.g., "per CSA A23.1 Cl. X.X") only when confirmed from ERs
- Do not invent code requirements based on assumption or general knowledge
- Flag unconfirmed standards as **TBD** and note they require extraction from ERs
- When codes are confirmed, ensure references are current and applicable to BC location
(Source: test/Volume_2_Part_2_Employers_Requirements.pdf, location TBD; Datasheet.md: Attributes; Specification.md: Standards.)

**P-05: Consistency Across Deliverables**
Maintain terminology consistency so DEL-05.01 (drawings) and DEL-05.04 (QA records) reference the same definitions:
- Material designations (concrete mix names like "Mix 30MPa-XF" for consistency across drawings, specs, and records)
- Exposure class terminology (use same terms in specification, drawing notes, and test records)
- Finish designations (e.g., "F1 smooth finish," "F2 rough finish" — define once, use everywhere)
- Inspection/testing terminology (consistent hold point names, test names, acceptance criteria)
- Coordinate specification language with DEL-05.01 drawing general notes during IDC
(Source: Specification.md: QR-03; Procedure.md: Steps; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:232; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:235.)

## Considerations

**C-01: Scope Boundary (Contractor Scope Only)**
Contractor scope only; do not impose requirements on Employer-responsible items except at interfaces:
- Specification covers concrete works within PKG-05 scope (foundations, containment walls, equipment pads, thrust blocks, ground liner interfaces)
- Do not specify requirements for Employer-supplied items unless required for interface coordination
- Clearly identify interface requirements with other disciplines (embedded items, coordination points)
(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:49; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:226; Specification.md: Scope.)

**C-02: Interface Coordination (Dependencies Coordinated Externally)**
Embedded items, anchors, sleeves, and blockouts must align with equipment/vendor requirements and other disciplines:
- Coordinate embedded item requirements with:
  - PKG-10, PKG-11, PKG-13, PKG-15 (equipment anchor bolts, mounting provisions)
  - PKG-14 (pipe sleeves, thrust block interfaces)
  - PKG-17 (electrical conduit sleeves, embedments)
  - PKG-20 (instrument penetrations, mounting provisions)
  - PKG-03 (drainage penetrations, clash avoidance)
- Specify embedment installation requirements (tolerances, placement, protection)
- Specify hold points for embedded item verification before concrete placement
- Dependencies coordinated externally per NOT_TRACKED mode (see `_DEPENDENCIES.md`)
(Source: `_DEPENDENCIES.md`; test/execution/_Coordination/_COORDINATION.md; Specification.md: FR-12; Specification.md: IR-02.)

**C-03: Constructability (Feasible Site Requirements)**
Specify tolerances and workmanship requirements that are feasible on site:
- **Reinforcement congestion:** Avoid specifying bar sizes/spacing that create unconstructable congestion; coordinate with DEL-05.01 detailing
- **Vibration access:** Ensure consolidation requirements are achievable with standard equipment; note where special consolidation is required
- **Curing constraints:** BC seasonal conditions affect curing requirements (winter cold, summer heat); specify appropriate protection
- **Formwork practicality:** Tolerances should be achievable with standard formwork; note where special formwork is required
- **ASSUMPTION:** Standard constructability considerations for concrete construction; specific project constraints TBD from Employer's Requirements and Contractor's construction methodology
(Source: Specification.md: FR-04; Specification.md: FR-08; Specification.md: PR-03.)

**C-04: Inspection and Testing Documentation**
Define what must be recorded and retained (pour records, cylinder tests, rebar inspections) and when hold points occur:
- Specify inspection requirements for reinforcement placement (hold point before concrete placement)
- Specify inspection requirements for formwork (hold point before concrete placement)
- Specify inspection requirements for embedded items (hold point before concrete placement)
- Specify testing requirements for concrete (slump, air content, temperature, cylinders) and sampling frequencies
- Specify documentation requirements that enable generation of DEL-05.04 records (pour records, cylinder test results, rebar inspection records)
- Provide templates or formats for inspection/testing records if possible
- **TBD:** Specific acceptance thresholds and hold point criteria from Employer's Requirements
(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:235; Specification.md: FR-06; Specification.md: FR-09; Specification.md: QR-02.)

**C-05: BC Coastal Environment Requirements**
Concrete structures must be designed and specified for BC coastal environment:
- **Freeze-thaw exposure:** BC coastal climate has freeze-thaw cycles; specify air entrainment and durability requirements
- **Marine exposure:** Proximity to Fraser River and ocean may require enhanced durability for chloride exposure (**TBD** from project location and ERs)
- **De-icing salts:** Vehicle traffic areas may have de-icing salt exposure (**TBD** applicability)
- **Sulfates:** Soil sulfate content may require sulfate-resistant cement (**TBD** from geotechnical investigation)
- **Seasonal construction:** Cold weather and hot weather concreting procedures for BC climate
- **TBD:** Specific exposure class assignments from Employer's Requirements Volume 2 Part 2 concrete section
(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:10; Datasheet.md: Conditions; Specification.md: FR-03; Specification.md: FR-04; Specification.md: PR-01.)

## Trade-offs

**T-01: Higher Durability Controls vs Cost/Schedule**
Stricter mix/curing/testing requirements improve long-term performance but may add time and cost:
- **Issue:** Higher durability requirements (lower w/c ratio, longer curing, more testing) increase material costs and construction duration
- **Benefit:** Improved long-term durability, reduced lifecycle maintenance costs (supports OBJ-9 Lifecycle Cost Optimization)
- **Consideration:** Balance initial cost vs lifecycle cost based on Employer's Requirements priorities
- **TBD:** Specific durability requirements and cost/schedule impact until ER requirements are confirmed
(Source: Specification.md: FR-03; Specification.md: PR-01.)

**T-02: Standard Details vs Bespoke Requirements**
Standardizing concrete mixes/details aids constructability but must still satisfy exposure and interface constraints:
- **Standardization benefits:** Reduced complexity, fewer mix changes, construction efficiency, quality control simplicity
- **Bespoke requirements:** Site-specific exposure classes, equipment interface requirements, containment requirements may require custom mixes or details
- **Approach:** Use standard mixes where conditions are similar (e.g., standard foundation mix, standard wall mix) and custom mixes where required (e.g., containment wall with special durability requirements)
- **TBD:** Opportunities for standardization until design basis and exposure requirements are confirmed

**T-03: Tolerance Tightness vs Constructability**
Tighter tolerances improve equipment fit and interface quality but may be difficult to achieve on site:
- **Issue:** Equipment pad tolerances, anchor bolt placement tolerances, and finished surface tolerances affect equipment installation quality
- **Tighter tolerances:** Better equipment fit, reduced shimming, improved alignment (supports equipment interfaces)
- **Constructability:** Very tight tolerances may require special formwork, skilled labor, increased inspection, potential for non-conformances
- **Balance:** Specify tolerances appropriate to the interface requirement (tighter for equipment pads, more relaxed for buried foundations)
- **Coordinate:** Align specified tolerances with equipment vendor requirements and DEL-05.01 drawing tolerances
(Source: Specification.md: FR-11; Specification.md: PR-02.)

**T-04: Inspection Frequency vs Schedule/Cost**
More frequent inspection and testing improves quality assurance but increases cost and may slow construction:
- **Issue:** Testing frequencies (cylinder sampling, air content testing) and inspection hold points affect cost and schedule
- **More frequent:** Better quality assurance, earlier detection of non-conformances, better data for acceptance decisions
- **Less frequent:** Lower cost, faster construction, reduced QA/QC resource requirements
- **Balance:** Specify frequencies aligned with Employer's Requirements and project quality priorities
- **Risk-based:** Consider more frequent inspection/testing for critical elements (containment structures, tank foundations)
- **TBD:** Specific testing frequencies and hold point requirements from Employer's Requirements
(Source: Specification.md: FR-06; Specification.md: FR-09; Specification.md: QR-02.)

## Examples

**E-01: Specification Organization (Example Structure)**
Minimum expected section set:
1. **Concrete Specification:**
   - Section 1: General (scope, references, definitions, submittals)
   - Section 2: Materials (cement, aggregates, water, admixtures, certifications)
   - Section 3: Mix Design (strength requirements, durability requirements, exposure classes, mix proportioning)
   - Section 4: Delivery and Placement (delivery requirements, placement procedures, consolidation, joints)
   - Section 5: Finishing and Curing (finishing requirements, curing methods, protection)
   - Section 6: Quality Control (testing frequencies, acceptance criteria, sampling procedures)
   - Section 7: Defects and Repairs (defect identification, repair procedures, rejection criteria)

2. **Reinforcement Specification:**
   - Section 1: General (scope, references, definitions, submittals)
   - Section 2: Materials (reinforcing steel grades, certifications, epoxy coating if required)
   - Section 3: Fabrication (bending, cutting, threading, identification)
   - Section 4: Placement (tolerances, support, cover, spacing, lap splices, couplers)
   - Section 5: Inspection (placement inspection, cover verification, hold points)
   - Section 6: Protection (storage, protection from damage/corrosion)

3. **Formwork Specification:**
   - Section 1: General (scope, references, definitions, submittals)
   - Section 2: Materials (formwork materials, release agents, coatings)
   - Section 3: Design and Construction (formwork design, tolerances, bracing)
   - Section 4: Surface Finishes (finish requirements by element type, acceptance criteria)
   - Section 5: Embedded Items (sleeves, blockouts, anchor bolts, plates, inserts)
   - Section 6: Formwork Removal (stripping times, procedures, protection, re-shoring)
   - Section 7: Inspection (form inspection before placement, hold points)

(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:233; Datasheet.md: Construction.)

**E-02: Requirement Language Examples**

**Good requirement (measurable, verifiable):**
- "Concrete for tank foundations shall have a minimum 28-day compressive strength of 35 MPa, verified by cylinder testing per CSA A23.1-C5. Sample one set of cylinders per 50 m³ of concrete placed or per day, whichever is more frequent."

**Poor requirement (ambiguous, unverifiable):**
- "Concrete shall be adequate for foundations." (What strength? How verified?)

**Good containment requirement (clear intent, measurable):**
- "Waterstops at containment wall joints shall be PVC type W2 per CAN/CSA-A123.5, installed with continuous joint sealing and tested by visual inspection before concrete placement. No gaps, tears, or discontinuities permitted."

**Good hold point requirement (explicit, actionable):**
- "HOLD POINT: Do not place concrete until reinforcement placement inspection is complete and approved. Inspection shall verify cover, spacing, lap splices, and support per Section 4.4."

(Source: Specification.md: FR-06; Specification.md: FR-09; Specification.md: PR-03; Guidance.md: P-01.)

**E-03: Verification Hook Examples (Enable DEL-05.04 Records)**

**For pour records:**
- "Record for each concrete placement: date, time, location, element description, volume placed, weather conditions, slump test results, air content test results, concrete temperature, cylinder sample numbers, inspector name, and acceptance/rejection decision."

**For cylinder test results:**
- "Test cylinders at 7 days and 28 days. Record: sample number, placement date, test date, age at test, compressive strength (MPa), acceptance decision (accept/reject per Section 6.3 criteria)."

**For rebar inspection records:**
- "Rebar placement inspection shall verify and record: element description, bar size and grade, cover measurements (minimum 5 locations per element), spacing measurements, lap splice lengths, support type and spacing, cleanliness, and acceptance/rejection decision with deficiency notes if applicable."

(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:235; Specification.md: FR-06; Specification.md: FR-09.)

## Local Conflict Table

No conflicts identified from accessible sources. Employer's Requirements clause extraction pending for final verification. (Source: test/Volume_2_Part_2_Employers_Requirements.pdf, location TBD.)

## Cross-Document Notes

- **Specification:** This guidance informs how `Specification.md` requirements (FR-01 through QR-03) are structured and what is emphasized (durability, containment, verification). Each Principle should support corresponding Specification requirements. Specification language should follow these Principles for clarity and consistency. (Source: Specification.md: Requirements.)
- **Procedure:** `Procedure.md` operationalizes drafting, review, and issue sequencing so the specification is checked and controlled before use. Considerations noted here (interfaces, constructability, documentation) should be addressed in Procedure steps. (Source: Procedure.md: Steps; Procedure.md: Verification.)
- **Datasheet:** Datasheet Construction section lists the specification artifacts (concrete, reinforcement, formwork) that these Principles and Considerations guide. Ensure specification content aligns with Datasheet construction breakdown and conditions. (Source: Datasheet.md: Construction; Datasheet.md: Conditions.)
