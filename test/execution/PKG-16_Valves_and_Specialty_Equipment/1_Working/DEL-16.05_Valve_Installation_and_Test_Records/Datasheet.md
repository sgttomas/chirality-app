# Datasheet: DEL-16.05 Valve Installation and Test Records

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-16.05 |
| Name | Valve Installation and Test Records |
| Package | PKG-16 Valves & Specialty Equipment |
| Discipline | Mechanical / QA/QC |
| Type | Record |
| Responsible | D&B Contractor (QA/QC) |
| Status | INITIALIZED |

**Source:** `_CONTEXT.md`

## Attributes

| Attribute | Value |
|-----------|-------|
| Record Types | Material certificates, FAT records, pressure test records, set pressure test records |
| Record Number Prefix | **TBD** — Per project record numbering system |
| Record Category | Quality Assurance / Quality Control (QA/QC) records; As-Built documentation |
| Retention Period | **TBD** — **ASSUMPTION**: Facility life + 25 years (permanent record for code compliance and warranty) |
| Format | **TBD** — **ASSUMPTION**: PDF for issued records; native files for working records |
| Revision | **TBD** — Initial issue typically Rev 0 or "Final"; records generally not revised (new test = new record) |
| Classification | **TBD** — **ASSUMPTION**: For Construction / As-Built Documentation |
| Applicable Systems | All valve systems (railcar unloading, marine loading, product transfer, storage tanks) |

**Source:** `_CONTEXT.md` (anticipated artifacts); typical QA/QC record attributes

## Conditions

**Operating / Environmental Context:**

This deliverable provides evidence of completion, inspection, and testing for valves at the canola oil transload facility (1,000,000 MT/annum throughput) at Fraser Surrey Terminal, Surrey, BC.

**Source:** Decomposition document Section 1.1 (Project Overview)

**Records Purpose:**

Installation and test records demonstrate compliance with design specifications (DEL-16.02), datasheets (DEL-16.04), and applicable codes (ASME, API, CSA B51) (see also Specification.md — Functional Requirements for record content):

**Primary Uses:**
1. **Code Compliance:** Demonstrate compliance with ASME Section VIII, ASME B31.3, CSA B51, and API standards
2. **Quality Assurance:** Verify valves manufactured, tested, and installed per specifications
3. **Warranty Support:** Provide evidence for manufacturer warranty claims
4. **Regulatory Compliance:** Support Technical Safety BC registration (for relief valves on registered pressure vessels)
5. **Operational Reference:** Provide baseline performance data for future maintenance and testing
6. **Liability Protection:** Demonstrate due diligence in valve installation and testing

**Record Types (per `_CONTEXT.md`):**

### 1. Material Certificates

**Purpose:** Provide traceability and certification of valve materials per ASME, API, and ASTM requirements.

**Typical Material Certificates (MTRs = Material Test Reports):**
- **Valve Body:** ASTM material certification (e.g., ASTM A351 CF8M for 316SS castings)
  - Chemical composition (actual analysis vs. specification limits)
  - Mechanical properties (tensile strength, yield strength, elongation, hardness)
  - Heat number and heat treatment records
  - Mill test report (MTR) or certificate of compliance (CoC)
- **Valve Trim:** Material certificates for seat, plug/disc, stem, packing
  - Same content as body certificates (chemical composition, mechanical properties, heat number)
- **Actuator Components:** Material certificates for actuator housing, springs, bolting
- **Bolting and Fasteners:** Material certificates per ASTM A193/A194 (stainless steel bolting)
  - Heat number, mechanical properties, corrosion resistance
- **Gaskets and Seals:** Material certificates and compatibility statements (PTFE, RTFE, graphite, elastomers)
  - Material composition, temperature/pressure ratings, compatibility with canola oil

**Regulatory Requirements:**
- ASME Section VIII requires material traceability for pressure vessels and relief valves ("UV" stamp)
- CSA B51 requires material certificates for pressure equipment registered in BC
- **TBD:** Specific CSA B51 material certificate requirements per Technical Safety BC guidance

**Source:** ASME Section VIII, API 600/608/609/526, CSA B51 material certificate requirements

### 2. Factory Acceptance Test (FAT) Records

**Purpose:** Demonstrate valve performance and quality prior to shipment from manufacturer.

**Typical FAT Records:**

**Control Valves (per IEC 60534-4):**
- **Flow Test:** Actual Cv measurement at multiple valve openings (verify Cv vs. manufacturer catalog)
- **Seat Leakage Test:** Leakage rate measurement per ANSI/FCI 70-2 (verify Class IV, V, or VI shutoff)
- **Stroke Test:** Valve stroking time measurement (open to close, close to open)
- **Actuator Performance Test:** Actuator output torque/thrust verification; fail-safe action test (for spring-return actuators)
- **Positioner Calibration:** Smart positioner calibration and loop test (4–20 mA signal verification, HART communication test)
- **Hydrostatic Pressure Test:** Body/bonnet pressure test per IEC 60534-4 (typically 1.5× rated pressure)
- **Witness Hold Points:** **TBD** — Owner or third-party witness required for critical valves

**Isolation Valves (per API 598 or ISO 5208):**
- **Hydrostatic Shell Test:** Pressure test of valve body with actuator removed (1.5× rated pressure for Class 150; per API 598 Table 1)
- **Seat Leakage Test:** Seat tightness test per API 598 or ISO 5208 (leak rate verification for specified leakage class)
- **Backseat Test:** Stem backseat leakage test (for valves with backseating feature)
- **Actuator Function Test:** Actuator torque verification and cycle test (if automated valve)
- **Fire-Safe Test:** API 607 fire test certification (if fire-safe valve specified) — typically performed on prototype, not every valve

**Relief Valves (per API 527):**
- **Set Pressure Test:** Cold differential test pressure (CDTP) verification (see Construction section below for CDTP details)
- **Seat Tightness Test:** API 527 seat tightness test (if tight shutoff required — not standard for all relief valves)
- **Capacity Certification:** ASME stamped capacity certification (capacity flow test performed on prototype or by calculation per ASME Section VIII)
- **ASME Stamping:** "UV" stamp (for pressure vessels) or "V" stamp (for piping) applied after successful testing
- **National Board Registration:** National Board Number assigned and stamped on valve nameplate (if required)

**FAT Witness Requirements:**
- **Critical Valves:** Owner or Owner's representative may witness FAT (ESD valves, large control valves, all relief valves)
- **Hold Points:** Manufacturer notifies Owner/Contractor prior to FAT; testing cannot proceed without witness approval
- **TBD:** Witness requirements per project quality plan and Employer's Requirements

**Source:** IEC 60534-4, API 598, API 527, ASME Section VIII FAT requirements

### 3. Pressure Test Records

**Purpose:** Verify valve installation and piping integrity after field installation.

**Typical Pressure Test Records (per ASME B31.3 and CSA B51):**

**Hydrostatic Pressure Test (Most Common):**
- **Test Medium:** Water (with corrosion inhibitor if required; drained after test)
- **Test Pressure:** 1.5× design pressure (ASME B31.3 paragraph 345.4)
  - Example: Class 150 piping (design pressure 285 psig @ 100°F) → test pressure = 1.5× 285 = 428 psig
- **Test Duration:** Hold pressure for minimum duration per ASME B31.3 (typically 10 minutes for piping ≤2" diameter; 30 minutes for larger)
- **Acceptance Criteria:** No visible leakage; no pressure drop during hold period
- **Valve Position During Test:**
  - **Isolation Valves:** Tested in closed position (to verify seat integrity)
  - **Control Valves:** Tested in closed position (seat test) AND open position (body test)
  - **Relief Valves:** Isolated during system pressure test (relief valve set pressure typically < system test pressure); relief valve tested separately per set pressure test
- **Test Witnessing:** **TBD** — Inspector or Owner witness may be required for code compliance

**Pneumatic Pressure Test (Alternative):**
- **Use When:** Hydrostatic test not feasible (cannot drain water, risk of freezing, etc.)
- **Test Medium:** Air or nitrogen (inert gas preferred for safety)
- **Test Pressure:** 1.1× design pressure (lower than hydrostatic due to stored energy risk)
- **Safety Precautions:** Barricade test area; personnel exclusion during pressurization
- **Acceptance Criteria:** No audible leakage; soap bubble test on joints and valve connections

**CSA B51 Requirements:**
- Pressure testing required for piping systems >103 kPa (15 psig) design pressure
- Test records must be retained for inspection by Technical Safety BC
- **TBD:** CSA B51 pressure test requirements specific to Fraser Surrey facility

**Source:** ASME B31.3 Chapter IX (Pressure Testing), CSA B51 Section 6 (Testing), API 598

### 4. Set Pressure Test Records (Relief Valves)

**Purpose:** Verify relief valve set pressure and provide ASME/CSA B51 compliance documentation.

**Set Pressure Testing (per API 526 and API 527):**

**Cold Differential Test Pressure (CDTP):**
- **Definition:** Pressure at which relief valve is set on test bench at ambient temperature
- **CDTP Adjustment:** Accounts for spring constant change with temperature
  - CDTP = Set Pressure × (K_test / K_operating)
  - Where K = spring rate at temperature (manufacturer provides CDTP based on valve service temperature)
- **Example:** Relief valve with 100 psig set pressure at 200°F operating temperature might have CDTP = 105 psig at 70°F test temperature (manufacturer-specific)

**Test Procedure (API 527):**
- **Test Medium:** Air, nitrogen, or water (depends on valve service and manufacturer recommendation)
- **Test Setup:** Relief valve installed on test bench; pressure slowly increased until valve opens (pops)
- **As-Found Test:** Record pressure at which valve first pops (as-found set pressure) — verifies valve not damaged during shipping/installation
- **Adjustment (if required):** If as-found set pressure not within tolerance, adjust spring compression and retest
- **As-Left Test:** Record final set pressure after adjustment (as-left set pressure) — this is the certified set pressure
- **Set Pressure Tolerance (per API 526):**
  - Pressures ≤ 70 psig: ±3 psi
  - Pressures > 70 psig: ±2% of set pressure
  - **Acceptance:** As-left set pressure must be within tolerance

**Test Witnessing:**
- **Critical Relief Valves:** Set pressure testing typically witnessed by Owner or Inspector
- **Regulatory Requirement:** CSA B51 may require authorized inspector witness for relief valves on registered pressure vessels — **TBD**

**Test Frequency:**
- **Initial Installation:** All relief valves tested before installation
- **Periodic Retesting:** Relief valves typically retested every 3–5 years per API 576 (in-service inspection)
- **After Maintenance:** Relief valves retested after any maintenance involving disassembly or seat replacement

**Test Records:**
- Valve tag number and service
- Set pressure (design) and CDTP
- As-found set pressure (before adjustment)
- As-left set pressure (after adjustment)
- Test medium (air, nitrogen, water)
- Test date and tester name/certification
- Witness signature (if witnessed)
- ASME National Board Number (stamped on valve)
- Next test due date

**Source:** API 526, API 527, API 576, ASME Section VIII, CSA B51

**Operating / Environmental Conditions:**

**Project Context:**
- **Location:** Fraser Surrey Terminal, Surrey, BC — coastal marine environment (corrosion considerations for test equipment and witness access)
- **Product:** CSD canola oil (food-grade) — test medium must not contaminate product; flushing required after hydrostatic testing
- **Operating Temperature Range:** **TBD** — Typical -10°C to +50°C ambient; heated product lines 40–60°C
- **Design Life:** **TBD** — **ASSUMPTION**: 25 years; records retained for facility life + 25 years
- **Hazardous Area Classification:** **TBD** — Test equipment must be rated for hazardous area if testing in classified areas

**Source:** Decomposition document Section 1.1 (Project Overview); environmental context for testing

**For record requirements and verification, see Specification.md. For record development procedure, see Procedure.md. For testing principles and examples, see Guidance.md.**

## Construction

**Record Package Structure:**

Per `_CONTEXT.md`, this deliverable includes records for material certification, factory acceptance testing, field pressure testing, and relief valve set pressure testing. Records organized by valve and test type:

### Material Certificate Package

**Organization:**
- Material certificates filed by valve tag number
- Separate sub-packages for: valve body certificates, trim certificates, actuator certificates, bolting certificates, gasket certificates
- **Format:** PDF scan of manufacturer-issued MTRs; original hard copies retained per project records retention policy

**Required Content per Certificate:**
- Material specification (ASTM, ASME, API)
- Heat number and lot number (traceability to manufacturing batch)
- Chemical composition (actual analysis with min/max spec limits)
- Mechanical properties (tensile strength, yield strength, elongation, hardness)
- Heat treatment record (if applicable: annealing, quenching, tempering)
- Manufacturer name and certification statement
- Certifying authority (manufacturer quality manager, third-party inspector if required)
- Date of issue

**Special Requirements for Food-Grade Service (Canola Oil):**
- Material certificates should confirm food-grade compliance (FDA CFR 21, NSF/ANSI 61, or equivalent)
- Stainless steel certificates for 316SS (ASTM A351 CF8M castings, ASTM A182 F316/F316L forgings)
- Gasket and seal material compatibility with edible oils
- **TBD:** Specific food-grade certification requirements per Employer's Requirements or regulatory authority

**Source:** ASME Section VIII material traceability requirements; API 600/608/609/526 material certificate requirements

### Factory Acceptance Test (FAT) Records Package

**FAT Record Contents:**

**Control Valve FAT Record:**
- Valve identification (tag number, manufacturer, model, serial number)
- Test date and location (manufacturer facility)
- Test witness (if applicable: Owner representative, third-party inspector)
- Test procedures reference (IEC 60534-4, manufacturer test procedure)
- Test results:
  - Flow test: Actual Cv at 25%, 50%, 75%, 100% travel (compare to catalog Cv)
  - Seat leakage test: Leakage rate (mL/min or bubbles/min); leakage class verification (Class IV, V, VI)
  - Stroke test: Open/close time (seconds); verify within specification
  - Actuator test: Output torque/thrust (Nm or kN); fail-safe action (FC or FO) verification
  - Positioner calibration: Input signal (4–20 mA) vs. valve position (% open); linearity within ±1%
  - Hydrostatic test: Test pressure, hold duration, result (pass/no leakage)
- Acceptance/rejection: Pass/fail for each test; overall acceptance
- Test engineer signature
- Witness signature (if witnessed)

**Relief Valve FAT Record (Set Pressure Test):**
- Valve identification (tag number, manufacturer, model, serial number, ASME National Board Number)
- Set pressure (design) and CDTP
- Test date and location
- Test procedure reference (API 527)
- Test medium (air, nitrogen, water)
- Test results:
  - As-found set pressure (psig or barg)
  - Adjustment made (if required): spring compression adjustment
  - As-left set pressure (psig or barg)
  - Set pressure tolerance verification: Within ±3 psi or ±2% (per API 526)
  - Seat tightness test (if performed): Leakage rate (bubbles/min); pass/fail per API 527
- ASME capacity certification: Stamped capacity (kg/h or lb/h) at set pressure + overpressure
- ASME stamp verification: "UV" or "V" stamp present and legible
- Test engineer signature and certification number (if applicable)
- Witness signature (if required by CSA B51 or Employer)

**Source:** IEC 60534-4, API 527, manufacturer standard test procedures

### Field Pressure Test Records Package

**Pressure Test Record Contents:**

**Piping System Hydrostatic Test Record (Including Valves):**
- System identification (piping system number, line numbers included in test)
- Valve identification (list of valves in test section; valve position during test: open or closed)
- Test date and location
- Test procedure reference (ASME B31.3, CSA B51, project test procedure)
- Test parameters:
  - Test medium: Water (with additives: corrosion inhibitor, biocide)
  - Design pressure: psig or barg (per piping class)
  - Test pressure: 1.5× design pressure (per ASME B31.3)
  - Test duration: Hold time in minutes (per ASME B31.3 based on pipe size)
  - Ambient temperature during test (°C or °F)
- Test results:
  - Initial pressure reading (psig or barg)
  - Final pressure reading after hold period
  - Pressure drop during hold (acceptable: <5% or <5 psi)
  - Visual inspection result: No visible leakage, no weeping at joints/valves
  - Acceptance: Pass/fail
- Valve-specific observations:
  - Isolation valves: Seat tightness verified (no leakage past closed valve)
  - Control valves: Body integrity verified (no external leakage)
  - Relief valves: Isolated during test or removed (set pressure < test pressure)
- Test engineer signature
- Inspector/witness signature (if required)

**Post-Test Actions:**
- Test medium drained and flushed (for food-grade service)
- System dried (nitrogen blow-down if required)
- Valves lubricated and actuated after test (verify no damage from test pressure)

**Source:** ASME B31.3 Article 345, CSA B51 Section 6, typical field test record format

### Set Pressure Test Records Package (Relief Valves — Field Verification)

**Field Set Pressure Test Record:**

In addition to factory set pressure test (FAT), relief valves may be retested in field after installation to verify:
- No damage during shipping/installation
- Set pressure within tolerance after field installation
- Compliance with CSA B51 requirements (if required by Technical Safety BC)

**Field Test Record Contents:**
- Valve identification (tag number, manufacturer, model, serial number, ASME National Board Number)
- Protected equipment (vessel or piping tag number, MAWP)
- Test date and location (field test facility or in-situ test rig)
- Test procedure reference (API 527, project test procedure)
- Test parameters:
  - Set pressure (design) and CDTP
  - Test medium (air or nitrogen; water typically not used for field test)
  - Ambient temperature during test (affects CDTP)
- Test results:
  - As-found set pressure (verify within tolerance vs. FAT as-left set pressure)
  - Adjustment (if required) — **Note:** Field adjustment not recommended; if out of tolerance, return valve to shop
  - As-left set pressure (if adjusted)
  - Acceptance: Pass (within tolerance) or Fail (return to shop for rework/replacement)
- Test engineer signature and certification (pressure relief valve tester certification if required)
- Inspector/witness signature (if required by CSA B51 or Employer)

**CSA B51 Compliance:**
- Relief valves protecting registered pressure vessels in BC require periodic testing per CSA B51
- Test records submitted to Technical Safety BC for compliance verification
- **TBD:** CSA B51 test frequency and reporting requirements for Fraser Surrey facility

**Source:** API 527, CSA B51 Section 4.11, typical field set pressure test record format

**Interface Deliverables (see also Specification.md — Interface Requirements):**
- DEL-16.02 (Valve Technical Specification) — Specification defines testing requirements; records demonstrate compliance
- DEL-16.04 (Valve Data Sheet Package) — Datasheets specify test acceptance criteria; records verify actual performance vs. datasheet requirements
- DEL-16.03 (Valve Design Calculations) — Calculations establish design basis (Cv, set pressure); test records verify actual performance vs. design
- DEL-16.01 (Valve Design Drawing Set) — Drawings show valve locations; test records reference valve tags per drawings
- Pressure vessel records (PKG-13 Storage Tanks) — Relief valve test records cross-referenced to protected vessel records

**Source:** Interface requirements inferred from package structure; formal dependencies NOT_TRACKED per `_DEPENDENCIES.md`

## References

**Reference Documents:**
- See `_REFERENCES.md` for applicable reference documents
- See `0_References/` in package directory for reference materials

**Applicable Standards:**

**Material Certification:**
- ASTM material standards (A105, A182, A351, A193, A194, etc.) — Define material requirements and test methods
- ASME BPVC Section II — Materials specifications
- ASME BPVC Section VIII — Material traceability requirements for pressure vessels and relief valves

**Factory Acceptance Testing:**
- IEC 60534-4 / ISA-75.02 — Control Valve Capacity Test Procedures
- ANSI/FCI 70-2 — Control Valve Seat Leakage
- API 598 — Valve Inspection and Testing (isolation valves)
- ISO 5208 — Industrial Valves – Pressure Testing of Valves
- API 527 — Seat Tightness of Pressure Relief Valves (relief valve set pressure testing)
- API 607 — Fire Test for Quarter-Turn Valves (if fire-safe valves specified)

**Field Pressure Testing:**
- ASME B31.3 — Process Piping, Chapter IX (Pressure Testing)
- CSA B51 — Boiler, Pressure Vessel and Pressure Piping Code, Section 6 (Testing)

**Set Pressure Testing:**
- API 526 — Flanged Steel Pressure-Relief Valves (set pressure tolerances)
- API 527 — Seat Tightness of Pressure Relief Valves (set pressure test procedures)
- API 576 — Inspection of Pressure-Relieving Devices (periodic retesting requirements)
- ASME BPVC Section VIII — Pressure Vessels (relief valve capacity certification)

**Canadian Codes:**
- CSA B51 — Boiler, Pressure Vessel and Pressure Piping Code (mandatory in BC; testing and inspection requirements)

**Project-Specific:**
- Employer's Requirements — **TBD** — **ASSUMPTION**: Volume 2 Parts 1–3 contain testing, inspection, and record retention requirements
- Project Quality Management Plan — **TBD** — QA/QC procedures, record formats, witness/hold point requirements

**Source:** Standards inferred from testing and record requirements; applicability confirmed during procedure development

**Cross-references:**
- See `_DEPENDENCIES.md` (NOT_TRACKED — dependencies coordinated externally)
- Decomposition document: `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`, Section 5, PKG-16, DEL-16.05
