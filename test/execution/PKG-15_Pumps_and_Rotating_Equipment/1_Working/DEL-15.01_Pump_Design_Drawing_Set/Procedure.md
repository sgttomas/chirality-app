# Procedure: DEL-15.01 Pump Design Drawing Set

## Purpose

This procedure defines the process for **producing** the **Pump Design Drawing Set** within **PKG-15 Pumps & Rotating Equipment** for the Canola Oil Transload Facility.

**Deliverable purpose:** Defines the design arrangement and details for pumps per ER requirements.

**Source:** `_CONTEXT.md` (description), decomposition DEL-15.01 entry

**Deliverable type:** Drawing
**Responsible party:** D&B Contractor (Mechanical discipline)

This procedure covers:
1. **Production process:** How to develop, draft, and verify pump design drawings
2. **Coordination process:** How to ensure interdisciplinary alignment
3. **Approval process:** How to review, check, and approve drawings for issue

**Source:** Standard engineering drawing production process; API 610 Section 6 (installation requirements inform drawing content)

## Prerequisites

### Dependencies

**Dependency tracking mode:** NOT_TRACKED — Dependencies are coordinated externally by humans (see `execution/_Coordination/_COORDINATION.md`)

**Source:** `_DEPENDENCIES.md`

### Upstream Information Required

Before commencing drawing development, the following information must be available or in progress:

| Information | Source | Status |
|------------|--------|--------|
| **Process design basis** | Process engineering (PKG-10, 11, 12) | **TBD** — Flow rates, pressures, temperatures, fluid properties |
| **Pump sizing calculations** | DEL-15.03 (Pump Design Calculations) | **TBD** — Required flow, head, NPSH, power |
| **Pump specifications** | DEL-15.02 (Pump Technical Specification) | **TBD** — Performance requirements, materials, standards |
| **Vendor pump outline drawings** | Pump vendor (via procurement) | **TBD** — Dimensions, nozzle locations, weights, motor data |
| **Site layout and constraints** | Civil discipline (PKG-01–04) | **TBD** — Available plot space, existing utilities, site datum |
| **Foundation design criteria** | Structural discipline (PKG-05) | **TBD** — Allowable soil bearing, seismic criteria, foundation type |
| **Piping design requirements** | Piping discipline (PKG-14) | **TBD** — Piping routes, support requirements, thermal expansion |
| **Electrical requirements** | Electrical discipline (PKG-19, 20) | **TBD** — Motor sizes, power supply, conduit routing |
| **Hazardous area classification** | Process safety / I&C | **TBD** — Area classification (if applicable) for motor selection |

**Source:** Typical pump design information flow; dependencies inferred from cross-discipline coordination requirements

**Coordination note:** Since dependency tracking is NOT_TRACKED, formal coordination is managed by humans via project coordination meetings, IDC reviews, and schedule management. Refer to project coordination plan.

### Reference Materials

The following reference materials shall be available:

**From package `0_References/` or project document management system:**
- Employer's Requirements Volume 2 Part 1 (General Requirements) — **location TBD**
- Employer's Requirements Volume 2 Part 2 (Civil & Process Mechanical Works) — **location TBD**
- Project CAD standards document — **TBD**
- Project drawing standards and title block templates — **TBD**
- Site survey and existing facility as-built drawings — **TBD**

**Applicable codes and standards:**
- API 610 — Centrifugal Pumps for Petroleum, Petrochemical and Natural Gas Industries
- ASME B31.3 — Process Piping (for piping interface requirements)
- ASME B16.5 — Pipe Flanges and Flanged Fittings
- ACI 318 / CSA A23.3 — Structural Concrete (for foundation design coordination)
- NBC 2015 — National Building Code of Canada (seismic and structural loads)
- WorkSafeBC — Occupational Health and Safety Regulation (access and clearances)

**Source:** Standards listed in Specification.md and Datasheet.md; ER locations from `0_References/_REFERENCE_INDEX.md`

### Personnel Requirements

| Role | Qualifications | Responsibilities |
|------|---------------|------------------|
| **Lead Mechanical Engineer** | P.Eng. (BC or equivalent), 10+ years experience in process/mechanical design | Overall deliverable responsibility, technical direction, approval |
| **Mechanical Designer** | Engineering degree or diploma, 5+ years pump/mechanical design experience | Drawing development, calculations, coordination |
| **CAD Technician/Designer** | CAD certification, 3+ years experience in process/mechanical CAD | Drafting, CAD standards compliance, drawing production |
| **Checker (Independent)** | P.Eng. or senior engineer, not involved in original design | Independent technical review, code compliance verification |
| **Interdisciplinary Coordinators** | Representatives from Process, Civil, Structural, Piping, Electrical, I&C disciplines | IDC review, interface coordination, conflict resolution |

**Source:** **ASSUMPTION** — Typical qualifications for mechanical design team; specific requirements TBD per project Quality Management Plan and professional registration requirements (BC)

**Note:** Professional engineering seal (P.Eng.) required for drawings submitted to authorities having jurisdiction (AHJ) per BC Engineers and Geoscientists Act.

### Tools and Software

- **CAD software:** **TBD** — Per project standards (typical: AutoCAD, MicroStation, or equivalent)
- **3D modeling software (if applicable):** **TBD** — For coordination and clash detection (e.g., Navisworks, Revit, PDMS)
- **Calculation software:** **TBD** — For pump sizing, NPSH, foundation loads (e.g., Excel, MathCAD, specialized pump software)
- **Document management system:** **TBD** — For version control and distribution

**Source:** **ASSUMPTION** — Typical engineering software tools; specific project tools TBD per project execution plan

## Steps

### Phase 1: Design Development

#### Step 1.1: Review Design Basis

**Action:**
- Review process design basis (flow rates, pressures, temperatures, fluid properties)
- Review pump sizing calculations (DEL-15.03) for required pump performance
- Review pump specifications (DEL-15.02) for equipment requirements
- Review site layout and plot plan for pump location constraints

**Verification:**
- Design basis is complete and approved for use
- Pump sizing calculations are checked and approved
- Pump specifications are issued for procurement (or at least in advanced draft)

**Records:**
- Design basis review memo (if required by project procedures)

**Source:** Standard design development process; API 610 design requirements inform this phase

---

#### Step 1.2: Obtain Vendor Pump Data

**Action:**
- Issue equipment requisition to procurement (coordinate with DEL-15.02, DEL-15.04)
- Receive vendor pump outline drawings (general arrangement, nozzle schedule, weights)
- Receive vendor foundation loading diagram (static and dynamic loads)
- Receive vendor motor data (dimensions, terminal box location, weights)

**Verification:**
- Vendor data is reviewed for compliance with specification requirements
- Vendor data is dimensionally consistent and complete
- Vendor data is approved for design (AFD) or approved for construction (AFC) per project procedures

**Records:**
- Vendor drawing transmittal and review log
- Vendor data approval documentation

**Source:** Typical procurement and vendor data workflow; API 610 requires vendor to provide installation drawings per Section 6

**Timing:** This step may occur in parallel with preliminary arrangement studies (using typical pump dimensions), with final drawings updated once vendor data is confirmed.

---

#### Step 1.3: Develop Preliminary Pump Arrangement

**Action:**
- Determine pump locations on site plot plan (coordinate with civil layout, piping routing, access requirements)
- Establish equipment spacing and clearances per API 610 Section 6.1.1 (maintenance access)
- Identify foundation locations and preliminary sizes
- Develop preliminary piping interface arrangement (suction/discharge routing)
- Identify access routes and platforms (coordinate with structural discipline)

**Considerations:**
- NPSH available vs. required (lower pump elevation improves NPSH for suction-limited services)
- Piping routing economy (minimize piping runs to reduce friction losses and capital cost)
- Maintenance access (coupling end clearance, seal access, instrument access)
- Constructability (crane access, laydown area, installation sequence)
- Safety (egress routes, spill containment, hazardous area boundaries)

**Verification:**
- Preliminary arrangement is reviewed by lead engineer
- Preliminary arrangement is coordinated with affected disciplines (IDC kickoff meeting)

**Records:**
- Preliminary arrangement sketches or marked-up plot plan
- IDC coordination meeting minutes

**Source:** API 610 Section 6.1.1 (clearances), Section 6.2 (piping); standard engineering design development process

---

#### Step 1.4: Perform Foundation Load Analysis

**Action:**
- Extract pump and motor weights from vendor data
- Calculate static and dynamic loads (operating, seismic, wind if elevated)
- Determine anchor bolt forces and foundation reactions
- Coordinate with structural engineer for foundation design (PKG-05)

**Deliverables to structural:**
- Equipment loads (vertical, horizontal, moments)
- Anchor bolt configuration (number, spacing, size)
- Foundation interface requirements (grout pad, baseplates, sleeves)

**Verification:**
- Load analysis is checked by independent engineer
- Foundation loads are transmitted to structural discipline and acknowledged

**Records:**
- Foundation load calculation (may be part of DEL-15.03 or separate calc)
- Structural coordination memo or transmittal

**Source:** API 610 Section 6.1 (foundation design); ACI 351.3R (Foundations for Dynamic Equipment)

---

### Phase 2: Drawing Production

#### Step 2.1: Develop Pump Arrangement Drawings

**Action:**
- Produce pump arrangement drawings in CAD per project standards
- Include plan views, elevations, and sections as required for clarity
- Show pump centerlines, equipment outlines, and key dimensions
- Show clearance envelopes for maintenance and access
- Show interfaces to piping, structural, electrical, and I&C systems
- Include general notes, material specifications, and references to related drawings

**Drawing content checklist:**
- [ ] Equipment identification and tag numbers
- [ ] Pump and motor outlines (from vendor data)
- [ ] Baseplate or foundation outline
- [ ] Suction and discharge nozzle locations, sizes, and orientations
- [ ] Anchor bolt pattern and locations
- [ ] Clearance dimensions (coupling end, seal access, instrument access)
- [ ] Access platforms, ladders, and walkways (coordinate with structural)
- [ ] Electrical conduit entry locations (coordinate with electrical)
- [ ] Instrument connection locations (coordinate with I&C)
- [ ] General notes (materials, installation requirements, references)
- [ ] Title block, revision block, and approval signatures

**CAD standards:**
- Layer naming per project standards — **TBD**
- Line types and weights per project standards — **TBD**
- Text styles and sizes per project standards — **TBD**
- Symbol library per project standards — **TBD**

**Verification:**
- Self-check by originator (completeness, accuracy, CAD standards compliance)

**Records:**
- CAD files (native format) and PDF plots
- Self-check sign-off (per project procedures)

**Source:** Project CAD standards (TBD); typical mechanical drawing content per API 610 and industry practice

---

#### Step 2.2: Develop Foundation Detail Drawings

**Action:**
- Produce foundation detail drawings showing:
  - Foundation plan and elevation views
  - Anchor bolt layout, size, and embedment depth
  - Grout pad dimensions and thickness
  - Concrete strength and reinforcement general notes (detailed design by structural)
  - Interface dimensions to coordinate with structural drawings (PKG-05)
  - Baseplates and sole plates (if applicable)
  - Piping sleeves or blockouts through foundation

**Coordination:**
- Review structural concrete drawings for consistency
- Confirm anchor bolt embedment meets ACI 318 Appendix D or CSA A23.3 requirements
- Confirm foundation dimensions and elevations match site civil drawings

**Verification:**
- Self-check by originator
- Coordination check with structural discipline

**Records:**
- CAD files and PDF plots
- Structural coordination sign-off (per IDC procedures)

**Source:** API 610 Section 6.1.4 (foundations and grouting); ACI 318 / CSA A23.3 (foundation design)

---

#### Step 2.3: Develop Piping Interface Drawings

**Action:**
- Produce piping interface drawings showing:
  - Pump nozzle schedule (tag, service, size, rating, orientation, elevation)
  - Flange details (type, rating, material, facing, gasket)
  - Piping support requirements near pump (first support location)
  - Allowable nozzle loads (from vendor data or API 610 limits)
  - Interface to piping drawings (DEL-14.01)
  - Valve and instrument locations near pump
  - Drain and vent connections

**Coordination:**
- Review piping isometric drawings for consistency
- Confirm nozzle locations match piping routing
- Confirm allowable nozzle loads are not exceeded (piping flexibility analysis)

**Verification:**
- Self-check by originator
- Coordination check with piping discipline

**Records:**
- CAD files and PDF plots
- Piping coordination sign-off (per IDC procedures)

**Source:** API 610 Section 4.2.9 (nozzle loads), Section 6.2 (piping installation); ASME B31.3 (piping flexibility)

---

### Phase 3: Review and Verification

#### Step 3.1: Self-Check

**Action:**
- Originator performs self-check using project checklist (if available) or general review criteria:
  - Completeness: All required views, details, and notes included
  - Accuracy: Dimensions match vendor data and calculations
  - Consistency: Cross-references to other drawings are correct
  - Compliance: CAD standards, drawing standards, code requirements met
  - Clarity: Drawing is understandable and unambiguous

**Verification:**
- Self-check sign-off on drawing or in project tracking system

**Records:**
- Self-check sign-off documentation

**Source:** Standard engineering quality procedure

---

#### Step 3.2: Interdisciplinary Check (IDC)

**Action:**
- Distribute drawings to affected disciplines for review:
  - **Process:** Verify pump locations and services match process requirements
  - **Civil:** Verify foundation locations and site elevations are correct
  - **Structural:** Verify foundation loads and anchor bolt requirements are coordinated
  - **Piping:** Verify nozzle locations, sizes, and orientations match piping design
  - **Electrical:** Verify motor data and conduit entry locations are correct
  - **I&C:** Verify instrument connection locations are accessible and correct

- Hold IDC review meeting (or distribute comments via project system)
- Resolve IDC comments and update drawings as required
- Obtain IDC sign-off from each affected discipline

**Verification:**
- All IDC comments are addressed (resolved or incorporated)
- IDC sign-offs obtained per project procedures

**Records:**
- IDC comment log and resolution tracking
- IDC sign-off documentation

**Source:** Standard engineering IDC procedure; ensures cross-discipline coordination per Specification.md (IF-1 through IF-4)

---

#### Step 3.3: Independent Check

**Action:**
- Qualified checker (independent of original design) performs technical review:
  - Verify design complies with API 610, ASME B31.3, NBC 2015, and applicable codes
  - Verify dimensions and calculations are correct (check sample dimensions against vendor data)
  - Verify clearances meet API 610 Section 6.1.1 requirements
  - Verify foundation design is adequate for loads (coordinate with structural checker)
  - Verify constructability and maintainability provisions are adequate

- Checker issues check comments or questions
- Originator resolves check comments and updates drawings
- Checker verifies comment resolution and signs off

**Verification:**
- All check comments are addressed
- Checker sign-off obtained

**Records:**
- Check comment log and resolution tracking
- Checker sign-off on drawing or in project tracking system

**Source:** Standard engineering independent check procedure; ensures technical rigor and code compliance per Specification.md (QR-1)

---

#### Step 3.4: Approval and Issue

**Action:**
- Lead mechanical engineer (or discipline manager) reviews drawings for:
  - Overall technical adequacy
  - Compliance with project requirements and Employer's Requirements
  - Readiness for issue (all comments resolved, all sign-offs obtained)

- Approve drawings for issue (sign and seal if required by jurisdiction)
- Assign revision and issue status per project procedures:
  - **IFR (Issued for Review):** For client/Employer review and comment
  - **IFC (Issued for Construction):** For construction use (no further changes expected)
  - **AFC (Approved for Construction):** After client approval (if required)

- Transmit drawings to project document control for distribution

**Verification:**
- All required sign-offs obtained (originator, checker, IDC disciplines, approver)
- Drawing metadata (number, revision, issue date, status) is correct
- Transmittal includes all required drawings and support documentation

**Records:**
- Approved drawings (PDF and native CAD)
- Transmittal documentation
- Document control registration

**Source:** Standard engineering approval and issue procedure per Specification.md (QR-2); professional seal requirements per BC Engineers and Geoscientists Act

---

### Phase 4: Configuration Management

#### Step 4.1: Maintain Revision Control

**Action:**
- Track all changes to drawings during project lifecycle
- Issue revised drawings with revision clouds and delta symbols per project standards
- Update revision block with revision number, date, description, and approval signatures
- Maintain superseded revisions per document retention requirements

**Verification:**
- Revision history is complete and traceable

**Records:**
- All drawing revisions archived per project procedures

**Source:** Standard document control procedure per Specification.md (QR-2)

---

#### Step 4.2: Incorporate Field Changes (During Construction)

**Action:**
- Receive field change requests or red-line markups from construction
- Evaluate changes for technical impact (may require re-calculation or re-coordination)
- Issue revised drawings if changes affect design or installation
- Document changes per project change management procedures

**Verification:**
- Field changes are technically evaluated and approved
- Revised drawings issued if required

**Records:**
- Field change documentation (RFIs, change orders, red-line markups)
- Revised drawings (if applicable)

**Source:** Standard construction change management procedure

---

#### Step 4.3: Prepare As-Built Drawings (Post-Construction)

**Action:**
- Incorporate all field changes and red-line markups into final as-built drawings
- Verify as-built dimensions during site inspection (if required)
- Issue as-built drawings with final revision (typically "As-Built" or "Rev X")
- Archive as-built drawings per project requirements

**Verification:**
- As-built drawings accurately represent installed condition
- All construction markups are incorporated

**Records:**
- As-built drawings (final revision)
- As-built certification (if required by ER Part 1)

**Source:** Standard as-built documentation procedure per Specification.md (QR-3); ER Part 1 as-built requirements (TBD)

---

## Verification

### Verification Activities Summary

| Phase | Verification Activity | Responsible Party | Acceptance Criteria |
|-------|----------------------|-------------------|---------------------|
| **Design Development** | Design basis review | Lead Engineer | Design basis complete and approved |
| **Design Development** | Vendor data review | Mechanical Engineer + Procurement | Vendor data complies with specification and is approved for design |
| **Drawing Production** | Self-check | Originator (Designer/Engineer) | Completeness, accuracy, CAD standards compliance |
| **Review** | IDC review | All affected disciplines | No unresolved conflicts; IDC sign-offs obtained |
| **Review** | Independent check | Qualified Checker | Code compliance verified; technical adequacy confirmed; check sign-off obtained |
| **Approval** | Final approval | Lead Mechanical Engineer (P.Eng.) | All comments resolved; drawing ready for issue; approval signature/seal obtained |
| **Construction** | Installation verification | Construction QC + DEL-15.05 | Installed condition matches approved drawings (within tolerances) |

**Source:** Standard engineering verification process per Specification.md (Verification section)

### Sign-Off Requirements

All drawings shall obtain the following sign-offs before issue:

1. **Originator sign-off** — Self-check complete
2. **IDC sign-offs** — All affected disciplines reviewed and commented (or confirmed no comment)
3. **Checker sign-off** — Independent check complete and comments resolved
4. **Approver sign-off** — Lead Mechanical Engineer approval (with professional seal if required)

**Source:** **ASSUMPTION** — Standard sign-off protocol; specific requirements TBD per project Quality Management Plan

### Verification Records

Verification records shall include:

- Self-check documentation
- IDC comment logs and sign-offs
- Independent check comment logs and sign-offs
- Approval signatures and professional seals (if applicable)
- Document transmittals and distribution records

**Records retention:** Per project document retention requirements — **TBD** — **ASSUMPTION**: Minimum 25 years for engineering drawings

**Source:** Project document control procedures (TBD)

---

## Records

### Documentation Outputs

The following documents shall be produced as outputs of this procedure:

1. **Pump Arrangement Drawings** (per DEL-15.01 scope)
   - Overall pump layout plan views
   - Pump elevation views
   - Section views as required
   - Clearance and access details

2. **Pump Foundation Details** (per DEL-15.01 scope)
   - Foundation plan and elevation views
   - Anchor bolt layout and details
   - Grout pad details
   - Baseplate details (if applicable)

3. **Piping Interface Drawings** (per DEL-15.01 scope)
   - Pump nozzle schedule
   - Flange and gasket details
   - Piping support requirements

**Source:** `_CONTEXT.md` anticipated artifacts; Specification.md (Documentation section)

### Supporting Documentation

Supporting documents that accompany the drawings:

- Design calculations (DEL-15.03) — Referenced on drawings
- Equipment specifications (DEL-15.02) — Referenced on drawings
- Vendor data sheets (DEL-15.04) — Attached or referenced
- Material take-off (MTO) — For procurement support
- Installation procedures — For construction guidance (may be part of DEL-15.05)

**Source:** Standard engineering documentation hierarchy

### Record Management

**Filing locations (per project lifecycle):**

- **During development:** `1_Working/DEL-15.01_Pump_Design_Drawing_Set/` — Active working files
- **During review:** `2_Checking/To/` — Drawings issued for review (copy)
- **After approval:** `3_Issued/` — Issued drawings (copy)
- **Working location remains:** `1_Working/` — Authoritative working location per project conventions

**Document control:**
- All drawings registered in project document management system
- Unique drawing numbers assigned per project numbering system — **TBD**
- Revision control per project procedures — **TBD**
- Distribution per project distribution matrix — **TBD**

**Archive and retention:**
- Final as-built drawings archived per project close-out procedures
- Retention period per ER Part 1 requirements — **TBD** — **ASSUMPTION**: Minimum 25 years (typical for engineering records in Canada)

**Source:** Project document control procedures (TBD); retention per Canadian engineering records standards

---

## References

### Primary References

- **Decomposition:** `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` (DEL-15.01 entry, objectives)
- **Context:** `_CONTEXT.md` (deliverable identity and anticipated artifacts)
- **Dependencies:** `_DEPENDENCIES.md` (NOT_TRACKED — coordination managed externally)
- **Reference Index:** `PKG-15/0_References/_REFERENCE_INDEX.md`

### Cross-References (DEL-15 Package)

- **DEL-15.02** — Pump Technical Specification (performance requirements input to design)
- **DEL-15.03** — Pump Design Calculations (sizing, NPSH, loads input to drawings)
- **DEL-15.04** — Pump Data Sheet Package (vendor data input to drawings)
- **DEL-15.05** — Pump Installation & Test Records (installation verification uses these drawings)

### Cross-References (Other Packages)

- **PKG-05** — Concrete Structures (foundation design coordination)
- **PKG-06** — Structural Steelwork (support platforms and access coordination)
- **PKG-10, 11, 12** — Process packages (pump services and flow requirements)
- **PKG-14** — Process Piping (piping interface coordination)
- **PKG-19, 20** — Electrical packages (motor and power supply coordination)
- **PKG-29, 30** — I&C packages (instrumentation interface coordination)

**Source:** Dependencies inferred from deliverable scope; formal coordination per project procedures (NOT_TRACKED in `_DEPENDENCIES.md`)

### Applicable Standards and Codes

- **API 610** — Centrifugal Pumps for Petroleum, Petrochemical and Natural Gas Industries (Section 6: Installation)
- **API 682** — Pumps—Shaft Sealing Systems for Centrifugal and Rotary Pumps
- **ASME B31.3** — Process Piping (piping interface requirements)
- **ASME B16.5** — Pipe Flanges and Flanged Fittings
- **ACI 318** / **CSA A23.3** — Structural Concrete (foundation design)
- **ACI 351.3R** — Foundations for Dynamic Equipment (pump foundation design guidance)
- **NBC 2015** — National Building Code of Canada (seismic and structural loads)
- **WorkSafeBC** — Occupational Health and Safety Regulation (access and clearances)
- **BC Engineers and Geoscientists Act** — Professional seal requirements

**Source:** Standards listed in Specification.md and Datasheet.md

---

**Document Status:** ENRICHED (Pass 1)
**Enrichment Date:** 2026-01-28
**Agent:** 4_DOCUMENTS enrichment cycle

**Next Steps:**
1. Execute this procedure to produce DEL-15.01 drawings
2. Coordinate with upstream deliverables (DEL-15.02, DEL-15.03) as they become available
3. Coordinate with downstream deliverables (DEL-15.04, DEL-15.05) during equipment procurement and installation phases
4. Update procedure as lessons learned emerge during project execution

**Cross-References:**
- Datasheet.md — Equipment attributes and conditions inform drawing content
- Specification.md — Requirements govern drawing production and verification
- Guidance.md — Design principles and trade-offs inform design decisions
