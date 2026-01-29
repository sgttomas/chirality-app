# Procedure: DEL-15.02 Pump Technical Specification

## Purpose

This procedure defines the process for **producing** the **Pump Technical Specification** within **PKG-15 Pumps & Rotating Equipment** for the Canola Oil Transload Facility.

**Deliverable purpose:** Defines performance, materials, and workmanship requirements for pumps per ER requirements.

**Source:** `_CONTEXT.md` (description), decomposition DEL-15.02 entry

**Deliverable type:** Specification (Equipment Technical Specification for procurement)
**Responsible party:** D&B Contractor (Mechanical discipline)

This procedure covers:
1. **Specification development:** How to define pump performance, materials, and quality requirements
2. **Review and verification:** How to ensure specification is complete, accurate, and coordinated
3. **Procurement support:** How to support vendor bidding, evaluation, and selection
4. **Configuration management:** How to maintain specification through project lifecycle

**Source:** Standard EPC procurement specification development process

## Prerequisites

### Dependencies

**Dependency tracking mode:** NOT_TRACKED — Dependencies are coordinated externally by humans (see `execution/_Coordination/_COORDINATION.md`)

**Source:** `_DEPENDENCIES.md`

### Upstream Information Required

Before commencing specification development, the following information must be available or in progress:

| Information | Source | Status |
|------------|--------|--------|
| **Process design basis** | Process engineering (PKG-10, 11, 12) | **TBD** — Pump services, flow rates, system configuration |
| **Fluid properties** | ER Part 2 or process data | **TBD** — CSD canola oil properties (SG, viscosity, temperature, vapor pressure) |
| **Preliminary pump sizing** | DEL-15.03 (in progress) or process engineering | **TBD** — Required flow, head, NPSH available |
| **Environmental requirements** | ER Part 1 and 2 | **TBD** — Seismic, corrosion protection, spill prevention, hazardous area classification |
| **Quality requirements** | ER Part 1 | **TBD** — Testing, inspection, documentation requirements |
| **Employer standards** | ER Part 1 and 2 | **TBD** — Preferred standards editions, vendor qualifications |

**Source:** Typical pump specification information flow

**Note:** Specification development can begin with preliminary information (process flow diagrams, estimated flows/pressures) and be updated as detailed design progresses (DEL-15.03 calculations finalized).

### Reference Materials

The following reference materials shall be available:

**From package `0_References/` or project document management system:**
- Employer's Requirements Volume 2 Part 1 (General Requirements) — **location TBD**
- Employer's Requirements Volume 2 Part 2 (Civil & Process Mechanical Works) — **location TBD**
- API 610 (latest edition) — Centrifugal Pumps for Petroleum, Petrochemical and Natural Gas Industries
- API 682 (latest edition) — Shaft Sealing Systems for Centrifugal and Rotary Pumps
- Project procurement procedures and templates — **TBD**

**Source:** Standards listed in Specification.md and Datasheet.md; ER locations from `0_References/_REFERENCE_INDEX.md`

### Personnel Requirements

| Role | Qualifications | Responsibilities |
|------|---------------|------------------|
| **Lead Mechanical Engineer** | P.Eng. (BC or equivalent), 10+ years process/mechanical design | Overall specification responsibility, technical direction, approval |
| **Mechanical Engineer** | Engineering degree, 5+ years pump/rotating equipment experience | Specification development, calculations coordination, vendor interface |
| **Procurement Engineer** | Engineering degree or equivalent, procurement experience | Commercial terms, vendor prequalification, bid evaluation support |
| **Checker (Independent)** | P.Eng. or senior engineer, not involved in original specification | Independent technical review, code compliance verification |

**Source:** **ASSUMPTION** — Typical qualifications for specification development team; specific requirements TBD per project Quality Management Plan

### Tools and Software

- **Word processing software:** For specification document development (Word, PDF)
- **Spreadsheet software:** For vendor proposal evaluation matrix
- **Calculation software:** For pump sizing verification (coordinate with DEL-15.03)
- **Document management system:** **TBD** — For version control and distribution

**Source:** **ASSUMPTION** — Typical engineering software tools

## Steps

### Phase 1: Specification Development

#### Step 1.1: Define Pump Services and Duties

**Action:**
- Review process design basis and identify all pump services required for facility
- For each pump service, define:
  - **Service description** (e.g., "Railcar Unloading Pump")
  - **Fluid** (CSD canola oil with properties)
  - **Flow rate** (normal, minimum, maximum)
  - **Pressure** (suction, discharge)
  - **Temperature** (normal, design minimum/maximum)
  - **Quantity** (number of pumps required, duty/standby configuration)

**Data sources:**
- Process flow diagrams (PFDs) and piping & instrumentation diagrams (P&IDs)
- DEL-15.03 (pump sizing calculations) — coordinate closely
- ER Part 2 (process requirements)

**Verification:**
- Pump duties are consistent with process design and facility throughput requirements (OBJ-2: 1,000,000 MT/annum)

**Records:**
- Pump duty summary table (may be part of DEL-15.03 or specification)

**Source:** Standard pump specification development process; coordinate with DEL-15.03 (calculations)

---

#### Step 1.2: Develop Specification Structure and Content

**Action:**
- Select specification template or develop structure per project standards
- For each pump service, develop specification sections:

**1. General**
- Scope of supply (pump, motor, baseplate, coupling, seal, auxiliary equipment)
- Applicable codes and standards (API 610, API 682, ASME, CSA, etc.)
- Definitions and terminology

**2. Equipment Description**
- Service description
- Fluid properties
- Operating conditions (flow, head, temperature, NPSH)
- Environmental conditions (ambient temperature, seismic, corrosion)

**3. Design Requirements**
- Pump type (per API 610 nomenclature)
- Materials of construction (per API 610 Annex G)
- Mechanical seal (per API 682 type and plan)
- Coupling (per API 610 Section 5.4)
- Baseplate (fabricated steel, grouted)
- Driver (motor specifications: power, voltage, enclosure, efficiency)

**4. Performance Requirements**
- Hydraulic performance curve requirements (flow-head-efficiency-power-NPSH)
- Performance tolerances (ISO 9906 Grade 2)
- Minimum continuous stable flow
- NPSH margin requirement

**5. Testing Requirements**
- Shop tests per API 610 Section 7 (hydrostatic, performance, vibration)
- Witness/hold points
- Test report requirements

**6. Quality Assurance**
- Vendor quality plan requirements
- Material certifications and traceability
- Inspection and test points (ITPs)

**7. Documentation Requirements**
- Vendor drawings (outline, cross-section, foundation loads)
- Performance curves
- Data sheets
- O&M manuals
- Material certifications
- Test reports

**8. Delivery and Installation Support**
- Shipping and packaging requirements
- Storage requirements (if applicable)
- Installation supervision (if required)
- Commissioning support (if required)

**Verification:**
- Specification structure is complete and follows project/industry standards
- Content is consistent with API 610 and API 682 requirements

**Records:**
- Draft specification document(s)

**Source:** API 610 Section 1 (scope and requirements structure); industry-standard specification templates

---

#### Step 1.3: Define Pump Performance Requirements

**Action:**
- For each pump service, specify performance requirements based on DEL-15.03 calculations:

| Parameter | How to Specify |
|-----------|----------------|
| **Rated Flow** | From system design (m³/hr or L/s) |
| **Rated Head** | From system head curve at rated flow (m or kPa) |
| **NPSH Available** | From NPSH calculation (worst-case suction conditions) |
| **Operating Speed** | Vendor to propose (typical: motor synchronous speed 1,200, 1,800, 3,600 RPM) |
| **Fluid Properties** | Specific gravity, viscosity, temperature, vapor pressure at operating conditions |
| **Performance Tolerance** | ISO 9906 Grade 2 (Flow ±7%, Head ±5%, Efficiency not guaranteed below stated value) |
| **Preferred Operating Region** | 70–120% of rated flow (per API 610) |
| **Minimum Flow** | Vendor to define (minimum continuous stable flow without damage) |
| **NPSH Margin** | NPSHA shall exceed vendor NPSHR by minimum 0.5m (or more for critical services) |

**Verification:**
- Performance requirements match DEL-15.03 calculations
- Performance requirements support project objectives (OBJ-2 throughput capacity)

**Records:**
- Performance requirements section of specification
- Coordination record with DEL-15.03

**Source:** API 610 Section 3 (hydraulic performance); ISO 9906 (performance testing); DEL-15.03 (calculations)

---

#### Step 1.4: Define Materials and Construction Requirements

**Action:**
- Specify materials for pump components per API 610 Annex G material designations:

| Component | Material Specification | Rationale |
|-----------|------------------------|-----------|
| **Casing** | Cast iron (S-6) or carbon steel (S-1) | Non-corrosive service; cost-effective |
| **Impeller** | Matched to casing material | Wear resistance; food-grade compatible (**TBD**) |
| **Shaft** | Carbon steel or 316 SS | 316 SS preferred for coastal corrosion resistance |
| **Wear Rings** | Bronze or stainless steel | Replaceable component; dissimilar metal to casing |
| **Mechanical Seal** | API 682 Type 2 (externally mounted cartridge), SiC or WC faces | Long life, low maintenance |
| **Baseplate** | Structural steel ASTM A36 or CSA G40.21 350W | Standard fabricated baseplate |

- Specify mechanical seal system per API 682:
  - **Seal type:** Single or dual seal (decision per Guidance.md trade-off)
  - **Seal support system plan:** Plan 11 (recirculation), Plan 32 (external flush), or Plan 53A/53B/54 (dual seal with barrier fluid)

- Specify driver (motor) requirements:
  - **Motor type:** Electric motor (induction), fixed-speed or VFD-driven (decision per Guidance.md trade-off)
  - **Motor efficiency:** NEMA Premium Efficiency or IEC IE3 minimum (supports OBJ-9)
  - **Motor enclosure:** TEFC, ODP, or explosion-proof (per hazardous area classification) — **TBD**
  - **Motor voltage:** Per electrical system design (coordinate with Electrical discipline) — **TBD**

**Verification:**
- Materials are appropriate for CSD canola oil service and environmental conditions
- Materials comply with API 610, API 682, and applicable codes
- Food-grade compatibility confirmed if required — **TBD**

**Records:**
- Materials and construction section of specification

**Source:** API 610 Annex G (materials); API 682 (seals); Guidance.md (material selection principles)

---

#### Step 1.5: Define Testing and Quality Requirements

**Action:**
- Specify shop testing requirements per API 610 Section 7:

| Test | Requirement | Acceptance Criteria | Witness |
|------|-------------|---------------------|---------|
| **Hydrostatic test** | 1.5× design pressure (minimum) | No leaks, no visible distortion | **TBD** |
| **Performance test** | Rated flow + 2 additional points (70%, 120%) | ISO 9906 Grade 2 tolerances | **TBD** |
| **Vibration test** | During performance test | API 610 Figure 15 or ISO 10816 limits | **TBD** |
| **NPSH test** | If critical NPSH service | NPSHR verified per API 610 Section 7.4 | **TBD** |
| **Seal test** | During performance test | No visible liquid leakage per API 682 | **TBD** |

- Specify quality assurance requirements:
  - Vendor quality plan submittal and approval
  - Material certifications (MTRs) for pressure-retaining components
  - Inspection and test plan (ITP) with hold/witness points
  - NDT requirements (if welded construction)

- Specify documentation requirements:
  - **For design:** Outline drawings, cross-sectional drawings, performance curves, foundation loads
  - **For construction:** Fabrication drawings, weld procedures, NDT reports
  - **For commissioning:** Test reports, O&M manuals, spare parts lists
  - **For operations:** Data sheets, maintenance procedures, troubleshooting guides

**Verification:**
- Testing requirements comply with API 610 Section 7
- Quality requirements comply with project Quality Management Plan
- Witness/hold points are appropriate for project risk level

**Records:**
- Testing and quality requirements section of specification

**Source:** API 610 Section 7 (shop tests), Section 8 (quality assurance); project Quality Management Plan (TBD)

---

### Phase 2: Review and Verification

#### Step 2.1: Self-Check

**Action:**
- Specification author performs self-check:
  - Completeness: All required sections included per procedure Step 1.2
  - Accuracy: Performance requirements match DEL-15.03; materials appropriate for service
  - Consistency: Cross-references to other deliverables are correct (DEL-15.01, DEL-15.03, DEL-15.04, DEL-15.05)
  - Compliance: API 610, API 682, and applicable codes referenced correctly
  - Clarity: Specification is clear, unambiguous, and biddable by vendors

**Verification:**
- Self-check sign-off on specification or in project tracking system

**Records:**
- Self-check documentation

**Source:** Standard engineering quality procedure

---

#### Step 2.2: Interdisciplinary Check (IDC)

**Action:**
- Distribute specification to affected disciplines for review:
  - **Process:** Verify pump duties and system requirements are correct
  - **Mechanical (peer review):** Verify technical content and code compliance
  - **Piping:** Verify nozzle sizes, flange ratings, and piping interface requirements
  - **Electrical:** Verify motor specifications (voltage, power, enclosure)
  - **I&C:** Verify control and instrumentation requirements
  - **Procurement:** Verify specification is biddable and includes commercial terms

- Resolve IDC comments and update specification as required

**Verification:**
- All IDC comments are addressed (resolved or incorporated)
- IDC sign-offs obtained per project procedures

**Records:**
- IDC comment log and resolution tracking

**Source:** Standard engineering IDC procedure

---

#### Step 2.3: Independent Check

**Action:**
- Qualified checker (independent of original specification development) performs technical review:
  - Verify compliance with API 610, API 682, and applicable codes
  - Verify performance requirements are adequate for system duty
  - Verify materials are appropriate for service and environmental conditions
  - Verify testing and quality requirements are complete and appropriate
  - Verify specification is consistent with ER requirements

- Checker issues check comments or questions
- Author resolves check comments and updates specification
- Checker verifies comment resolution and signs off

**Verification:**
- All check comments are addressed
- Checker sign-off obtained

**Records:**
- Check comment log and resolution tracking
- Checker sign-off on specification

**Source:** Standard engineering independent check procedure per Specification.md (QR-1)

---

#### Step 2.4: Approval and Issue

**Action:**
- Lead mechanical engineer (or discipline manager) reviews specification for:
  - Overall technical adequacy
  - Compliance with project requirements and Employer's Requirements
  - Readiness for procurement issue

- Approve specification for issue (sign and seal if required by jurisdiction)
- Assign revision and issue status per project procedures:
  - **IFP (Issued for Procurement):** For equipment requisition and vendor bidding
  - **IFR (Issued for Review):** For client/Employer review and comment (if required before procurement)

- Transmit specification to procurement and project document control

**Verification:**
- All required sign-offs obtained (author, checker, IDC disciplines, approver)
- Specification metadata (number, revision, issue date, status) is correct

**Records:**
- Approved specification (PDF)
- Transmittal documentation
- Document control registration

**Source:** Standard engineering approval and issue procedure; professional seal requirements per BC Engineers and Geoscientists Act

---

### Phase 3: Procurement Support

#### Step 3.1: Support Vendor Bidding and Clarifications

**Action:**
- Respond to vendor requests for information (RFIs) and clarifications during bid period
- Issue specification addenda if clarifications require specification changes
- Participate in pre-bid meetings if held

**Verification:**
- All vendor RFIs are answered
- Addenda are issued per project document control procedures

**Records:**
- Vendor RFI log and responses
- Specification addenda (if issued)

**Source:** Standard procurement support activities

---

#### Step 3.2: Evaluate Vendor Proposals

**Action:**
- Develop vendor proposal evaluation matrix per Specification.md (Verification section):
  - Technical compliance (flow, head, NPSH, efficiency, materials, codes)
  - Quality (vendor quality plan, past performance, certifications)
  - Delivery schedule (meets project schedule)
  - Price (capital cost, lifecycle cost if VFD evaluated)
  - Energy efficiency (pump and motor efficiency)
  - Standardization (commonality with other pumps)

- Review vendor technical proposals:
  - Verify hydraulic performance meets specification requirements (within ISO 9906 tolerances)
  - Verify NPSHR is less than NPSHA with adequate margin
  - Verify materials comply with specification
  - Verify testing and quality plan comply with specification
  - Identify exceptions and deviations from specification

- Prepare technical evaluation report with recommendations

**Verification:**
- Evaluation is objective and based on specification requirements
- All vendor proposals are evaluated consistently using same criteria

**Records:**
- Vendor proposal evaluation matrix
- Technical evaluation report

**Source:** Standard vendor proposal evaluation process per Specification.md

---

#### Step 3.3: Support Vendor Selection and Contract Award

**Action:**
- Participate in vendor selection meeting with procurement and project management
- Recommend technically acceptable vendor(s)
- Support contract negotiations if technical clarifications required
- Review purchase order technical attachments for consistency with specification

**Verification:**
- Selected vendor is technically compliant
- Purchase order references specification correctly

**Records:**
- Vendor selection documentation
- Purchase order (procurement responsibility)

**Source:** Standard procurement process

---

### Phase 4: Configuration Management

#### Step 4.1: Maintain Specification Through Design Development

**Action:**
- Update specification if design changes occur (e.g., flow/head changes from DEL-15.03 updates)
- Issue specification revisions per project document control procedures
- Coordinate revisions with vendor if contract already awarded (change order process)

**Verification:**
- Specification remains current and consistent with design basis

**Records:**
- Specification revisions

**Source:** Standard configuration management process

---

#### Step 4.2: Support Vendor Data Review

**Action:**
- Review vendor submittal data for compliance with specification:
  - Outline drawings (verify dimensions, nozzle locations, weights)
  - Performance curves (verify flow, head, efficiency, NPSH within specification limits)
  - Material certifications (verify materials match specification)
  - Quality documentation (verify quality plan, test procedures)

- Approve vendor data for construction (AFC) or return with comments

**Verification:**
- Vendor data complies with approved specification
- Vendor data is suitable for downstream design use (DEL-15.01 arrangement drawings)

**Records:**
- Vendor data review and approval documentation (tracked in DEL-15.04 Data Sheet Package)

**Source:** Standard vendor data review process; coordinate with DEL-15.04

---

## Verification

### Verification Activities Summary

| Phase | Verification Activity | Responsible Party | Acceptance Criteria |
|-------|----------------------|-------------------|---------------------|
| **Development** | Performance requirements check | Mechanical Engineer + DEL-15.03 author | Requirements match calculations |
| **Development** | Materials selection check | Lead Mechanical Engineer | Materials appropriate for service and compliant with codes |
| **Review** | Self-check | Specification Author | Completeness, accuracy, compliance |
| **Review** | IDC review | All affected disciplines | No unresolved conflicts; IDC sign-offs obtained |
| **Review** | Independent check | Qualified Checker | Code compliance, technical adequacy confirmed |
| **Approval** | Final approval | Lead Mechanical Engineer (P.Eng.) | Specification ready for procurement |
| **Procurement** | Vendor proposal evaluation | Mechanical Engineer + Procurement | Vendor meets technical requirements |
| **Post-award** | Vendor data review | Mechanical Engineer | Vendor data complies with specification |

**Source:** Standard specification development and procurement verification process

### Sign-Off Requirements

All specifications shall obtain the following sign-offs before issue for procurement:

1. **Author sign-off** — Self-check complete
2. **IDC sign-offs** — All affected disciplines reviewed
3. **Checker sign-off** — Independent check complete
4. **Approver sign-off** — Lead Mechanical Engineer approval (with professional seal if required)
5. **Procurement sign-off** — Specification ready for bidding

**Source:** **ASSUMPTION** — Standard sign-off protocol; specific requirements TBD per project Quality Management Plan

## Records

### Documentation Outputs

The following specification documents shall be produced:

1. **Railcar Unloading Pump Specification** (per DEL-15.02 scope)
2. **Marine Loading Pump Specification** (per DEL-15.02 scope)
3. **Sump Pump Specification** (per DEL-15.02 scope)
4. **Transfer Pump Specification** (if applicable) — **TBD**

**Source:** `_CONTEXT.md` (anticipated artifacts); Specification.md (Documentation section)

### Supporting Documentation

Supporting documents that accompany or result from the specifications:

- **DEL-15.03** — Pump Design Calculations (sizing, NPSH) — Input to specification
- **Equipment requisition** — Procurement document referencing specification
- **Vendor proposals** — Vendor technical and commercial proposals
- **Vendor proposal evaluation** — Technical evaluation report and recommendation
- **Purchase order** — Contract document referencing specification
- **DEL-15.04** — Pump Data Sheet Package — Vendor data reviewed against specification

**Source:** Standard EPC procurement documentation flow

### Record Management

**Filing locations (per project lifecycle):**

- **During development:** `1_Working/DEL-15.02_Pump_Technical_Specification/` — Active working files
- **During review:** `2_Checking/To/` — Specifications issued for review (copy)
- **After approval:** `3_Issued/` — Issued specifications (copy)
- **Working location remains:** `1_Working/` — Authoritative working location per project conventions

**Document control:**
- All specifications registered in project document management system
- Unique specification numbers assigned per project numbering system — **TBD**
- Revision control per project procedures — **TBD**

**Archive and retention:**
- Final specifications with all addenda archived per project close-out procedures
- Retention period per ER Part 1 requirements — **TBD** — **ASSUMPTION**: Minimum 25 years

**Source:** Project document control procedures (TBD); retention per Canadian engineering records standards

---

**Document Status:** ENRICHED (Pass 1)
**Enrichment Date:** 2026-01-28
**Agent:** 4_DOCUMENTS enrichment cycle

**Cross-References:**
- Datasheet.md — Equipment attributes, fluid properties, materials inform specification content
- Specification.md — Requirements govern specification development and verification
- Guidance.md — Design principles and trade-offs inform specification decisions
- DEL-15.01 — Pump Design Drawing Set (informed by specification and vendor data)
- DEL-15.03 — Pump Design Calculations (input: sizing, NPSH requirements)
- DEL-15.04 — Pump Data Sheet Package (output: vendor data reviewed against specification)
- DEL-15.05 — Pump Installation & Test Records (field testing per specification requirements)
