# Specification: DEL-16.04 Valve Data Sheet Package

## Scope

This specification defines the requirements for producing **Valve Data Sheet Package** within **PKG-16 Valves & Specialty Equipment**.

**Purpose:** Defines and substantiates individual valve selections per ER requirements for the Canola Oil Transload Facility at Fraser Surrey Terminal.

**Source:** `_CONTEXT.md`

**Anticipated deliverable artifacts:**
- Control valve data sheets (flow, pressure, level control valves)
- Isolation valve data sheets (manual and automated gate, ball, butterfly valves)
- Relief valve data sheets (pressure relief and thermal relief valves)

**Source:** `_CONTEXT.md`

**Valve Categories (per PKG-16 scope):**
- Control valves (modulating flow, pressure, or level control)
- Isolation valves (on/off isolation service, manual or automated)
- Relief valves (overpressure protection per ASME Section VIII and CSA B51)
- Specialty items (check valves, strainers, etc. — may have separate datasheets)

**Source:** Decomposition document Section 5, PKG-16 scope (location TBD)

**Inclusions:**
- Individual valve datasheets with tag numbers, service descriptions, process conditions
- Valve sizing data (from DEL-16.03 calculations)
- Valve specifications (body, trim, actuator, accessories)
- Material specifications (body, trim, gaskets, bolting)
- Performance requirements (leakage class, rangeability, set pressure)
- Vendor data incorporation (post-procurement update with actual valve data)

**Exclusions:**
- Valve sizing calculations (see DEL-16.03 Valve Design Calculations) — datasheets reference calculation results
- Valve procurement specifications (see DEL-16.02 Valve Technical Specification) — datasheets support procurement per specification
- Valve arrangement drawings (see DEL-16.01 Valve Design Drawing Set) — drawings show valves identified in datasheets
- Valve installation and test records (see DEL-16.05) — records reference datasheets for acceptance criteria

**Source:** Scope definition inferred from deliverable type and package structure

## Requirements

### Functional Requirements

**Datasheet Package Content:**

The valve datasheet package shall include individual datasheets for all valves within PKG-16 scope (see also Procedure.md — Steps for datasheet development workflow):

**1. Control Valve Data Sheets:**

Each control valve shall have an individual datasheet containing the following information (see also Datasheet.md — Construction section for detailed content):

**Minimum Required Content:**

**A. Identification:**
- Valve tag number (per P&ID tagging convention)
- Service description (clear, concise description of valve function)
- P&ID reference (document number, revision, sheet number)
- Line number (from piping line list)
- System (e.g., Railcar Unloading, Marine Loading, Product Transfer)

**B. Process Conditions:**
- Fluid name and properties (density, viscosity, vapor pressure)
- Operating conditions: Normal and design flow rates, inlet/outlet pressures, temperature
- Differential pressure across valve
- Allowable pressure drop range (for control authority)
- Special conditions (e.g., high viscosity, variable temperature, winterization requirements)

**C. Valve Sizing and Selection (from DEL-16.03):**
- Required Cv or Kv (at design conditions)
- Selected valve size (DN or NPS)
- Valve body style (globe, ball, butterfly) with justification
- Trim type and characteristic (equal percentage, linear, quick-opening)
- Flow direction (flow-to-open or flow-to-close)
- Rangeability (turndown ratio)
- Cavitation assessment (acceptable, marginal, requires anti-cavitation trim)
- Noise level prediction (dBA at 1 meter)
- Sizing margin (selected Cv vs. required Cv)

**D. Valve Body Specifications:**
- Body material (per DEL-16.02 specification and service requirements)
- End connections (flanged, threaded, welded) and flange rating
- Pressure-temperature rating (per ASME B16.34)
- Body style (through-body, angle, three-way)
- Bonnet type (bolted, threaded, pressure-seal)

**E. Trim Specifications:**
- Trim material (stainless steel, hardened alloy, etc.)
- Seat material (metal, soft-seated PTFE/RTFE)
- Plug/disc material
- Stem material
- Packing material and type (graphite, PTFE, live-loaded)
- Leakage class (ANSI/FCI 70-2 Class I through VI)

**F. Actuator and Accessories (from DEL-16.03):**
- Actuator type (pneumatic spring-return, double-acting, electric)
- Actuator action (air-to-open or air-to-close)
- Fail-safe mode (FC, FO, FL) with justification
- Required torque/thrust
- Selected actuator size and output
- Safety factor achieved
- Air supply pressure (for pneumatic)
- Stroking time
- Positioner type (analog, smart digital, communication protocol)
- Accessories (limit switches, solenoid valves, air sets, manual override)

**G. Codes and Standards:**
- Design code (IEC 60534 / ISA-75)
- Flange standard (ASME B16.5 or B16.47)
- Materials standards (ASTM)
- Testing standard (IEC 60534-4)

**H. Vendor Data (post-procurement — see Procedure.md Step 4):**
- Manufacturer and model number
- Serial number
- Certified Cv data
- Factory acceptance test results
- Material certificates (MTRs)
- O&M manual reference

**Source:** ISA Form S20.50 control valve datasheet format; typical EPC datasheet content

**2. Isolation Valve Data Sheets:**

Each isolation valve (manual or automated) shall have an individual datasheet containing the following information:

**Minimum Required Content:**

**A. Identification:**
- Valve tag number (XV-#### for manual, MOV-#### or AOV-#### for automated)
- Service description
- P&ID reference
- Line number
- Operation type (manual, pneumatic, electric)

**B. Process Conditions:**
- Fluid name and properties
- Design flow rate (for pressure drop calculation)
- Design pressure and temperature
- Special conditions (e.g., fire-safe required, cryogenic service, high temperature)

**C. Valve Specifications:**
- Valve type (gate, ball, butterfly, plug)
- Valve size (DN or NPS)
- Pressure class (ASME Class 150, 300, 600, etc.)
- Body material
- Trim material
- Seat material (soft-seated or metal-seated)
- End connections and flange facing
- Stem type (rising, non-rising, outside screw & yoke)
- Packing type
- Leakage class (API 598 or ISO 5208)
- Fire-safe certification (API 607 if required)

**D. Actuation (for automated valves, from DEL-16.03):**
- Actuator type and action
- Fail-safe mode (if applicable)
- Required torque
- Selected actuator size
- Safety factor
- Stroking time
- Air supply or electric power requirements
- Accessories (limit switches, solenoid valves)

**E. Manual Operation (for manual valves):**
- Handwheel or gearbox
- Operating torque
- Number of turns to open/close
- Open/closed position indication

**F. Codes and Standards:**
- Design code (API 600, 608, 609, 6D)
- Testing standard (API 598, ISO 5208)
- Fire-safe standard (API 607 if applicable)

**G. Vendor Data (post-procurement):**
- Manufacturer and model
- Serial number
- Test certificates
- Material certificates

**Source:** Typical isolation valve datasheet content for process facilities

**3. Relief Valve Data Sheets:**

Each relief valve shall have an individual datasheet containing the following information (see also Datasheet.md — Construction section for API 526 requirements):

**Minimum Required Content:**

**A. Identification:**
- Relief valve tag number (PSV-#### or PRV-####)
- Protected equipment tag number
- P&ID reference
- Service description

**B. Protected Equipment Data:**
- Equipment type (pressure vessel, piping, heat exchanger, storage tank)
- MAWP (Maximum Allowable Working Pressure)
- Design pressure and temperature
- Volume (for thermal expansion)
- Wetted surface area (for fire case)

**C. Relief Scenario and Sizing (from DEL-16.03):**
- Governing relief scenario (thermal expansion, fire case, blocked discharge, etc.)
- Required relief capacity (kg/h or lb/h)
- Relieving pressure (set pressure + overpressure)
- Fluid state at relief (liquid, vapor, two-phase)
- Set pressure and tolerance (per API 526)
- Overpressure allowance (10% or 21%)
- Accumulated pressure during relief

**D. Orifice Sizing (from DEL-16.03):**
- Required orifice area (mm² or in²)
- Selected API 526 orifice designation (D, E, F, G, H, J, K, L, M, N, P, Q, R, T)
- Actual orifice area (from API 526 table)
- ASME stamped relief capacity

**E. Valve Specifications:**
- Relief valve type (conventional, balanced-bellows, pilot-operated)
- Valve size (inlet × outlet, e.g., NPS 3 × 4)
- Body material
- Spring material
- Trim material
- Seat material
- Inlet/outlet connection type
- Pressure-temperature rating
- ASME stamp ("UV" for vessels, "V" for piping)

**F. Discharge Arrangement:**
- Discharge location (atmosphere, header, containment)
- Discharge piping size
- Back pressure (% of set pressure)
- Inlet piping loss (% of set pressure)

**G. Testing and Certification:**
- Set pressure test (cold differential test pressure)
- Test medium (air, nitrogen, water)
- Capacity certification (ASME stamped)
- Seat tightness test (API 527 if required)

**H. Codes and Standards:**
- Design code (ASME Section VIII, ASME B31.3, CSA B51)
- Sizing standard (API 520/521)
- Manufacturing standard (API 526)
- Testing standard (API 527)

**I. Vendor Data (post-procurement):**
- Manufacturer and model
- Serial number
- ASME National Board Number
- Set pressure test certificate
- Capacity certification
- Material certificates

**J. Regulatory Compliance:**
- CSA B51 registration requirement (TBD)
- National Board registration (if required)

**Source:** API 526 and ASME Section VIII relief valve datasheet requirements

**Datasheet Format:**

**Format Options:**
- **Option A:** Standardized form templates (one template per valve type: control, isolation, relief)
- **Option B:** Tabular format (database or spreadsheet with columns for each datasheet parameter)
- **Option C:** Vendor-specific format (using valve manufacturer's standard datasheet format)

**Recommendation:** Use Option A (standardized form templates) for consistency and ease of review; ISA Form S20.50 for control valves; custom templates for isolation and relief valves

**TBD:** Datasheet format selection based on project document management preferences

**Source:** Typical datasheet format options for EPC projects

### Performance Requirements

**Datasheet Completeness:**

1. **All Required Fields Populated:** Every datasheet field shall be populated with data or marked "N/A" if not applicable; no blank fields permitted
2. **Data Accuracy:** All data shall be verified against source documents (calculations, P&IDs, specifications)
3. **Units Consistency:** All datasheets shall use consistent units (SI or Imperial per project standard); units clearly indicated for all numerical values
4. **Revision Control:** Datasheets shall be revision-controlled; revisions tracked with reason for change and date

**Datasheet Consistency:**

1. **Internal Consistency:** Data within each datasheet shall be internally consistent (e.g., valve size matches line size; pressure rating adequate for design pressure)
2. **Cross-Deliverable Consistency:** Datasheets shall be consistent with:
   - DEL-16.03 calculations (Cv, set pressure, actuator size match calculation results)
   - DEL-16.02 specification (materials, leakage class, testing requirements comply with specification)
   - P&IDs (tag numbers, service descriptions, fail-safe modes match P&IDs)
   - Piping line list (line numbers, line sizes, pressure classes match)
   - Equipment datasheets (protected equipment MAWP for relief valves)

3. **P&ID Traceability:** Every valve on P&ID shall have corresponding datasheet; every datasheet shall reference P&ID location

**Datasheet Verification (see Specification — Verification section):**

1. **Designer Self-Check:** Originator verifies datasheet completeness and accuracy
2. **Calculation Cross-Check:** Verify sizing data matches DEL-16.03 calculation results (Cv, set pressure, actuator size)
3. **Specification Compliance Check:** Verify datasheet specifications comply with DEL-16.02 procurement specification
4. **P&ID Cross-Check:** Verify tag numbers, line numbers, fail-safe modes match P&IDs
5. **Interdisciplinary Check:** Process, piping, instrumentation, and control systems review datasheets for interface correctness

**Source:** Datasheet quality requirements typical for EPC projects

### Interface Requirements

**Multi-Discipline Coordination:**

The valve datasheet package shall be coordinated with the following disciplines/deliverables (see also Procedure.md — Step 3 for coordination process):

1. **Process (PKG-10, PKG-11, PKG-12, PKG-13):**
   - P&IDs provide valve tag numbers, service descriptions, line numbers
   - Process datasheets provide fluid properties (density, viscosity, vapor pressure)
   - Valve datasheets provide feedback to process (pressure drops, relief capacities)

2. **Mechanical Piping (PKG-14):**
   - Piping line list provides line numbers, line sizes, pressure classes
   - Valve datasheets specify valve end connections and flange ratings (must match piping)
   - Relief valve discharge piping design coordinated with relief valve datasheets (back pressure limits)

3. **Instrumentation (PKG-20):**
   - Control valve datasheets specify positioner type and communication protocol
   - Instrumentation datasheets for flow meters, pressure transmitters coordinated with valve datasheets
   - I/O list coordinated with valve instrumentation (limit switches, position transmitters)

4. **Control Systems (PKG-19):**
   - Control valve fail-safe modes coordinated with control logic
   - ESD valve logic coordinated with valve datasheets (closure time, fail-safe action)
   - Communication protocol for smart positioners coordinated with DCS/PLC

5. **Electrical (PKG-17):**
   - Electric actuator motor specifications coordinated with electrical datasheets (voltage, enclosure rating)
   - Motor control center (MCC) coordinated with motor-operated valve (MOV) datasheets

6. **Safety (DEL-27.02 HAZOP):**
   - Relief valve scenarios coordinated with HAZOP recommendations
   - Control valve and ESD valve fail-safe modes coordinated with HAZOP safety requirements
   - Safety-critical valve identification coordinated with HAZOP risk assessment

**Source:** Interface requirements inferred from multi-discipline nature of valve datasheets; formal dependencies NOT_TRACKED per `_DEPENDENCIES.md`

**Vendor Coordination (Post-Procurement):**

- After valve procurement, vendor-supplied data incorporated into datasheets (see Procedure.md — Step 4)
- Vendor submittal review verifies compliance with datasheet requirements
- Discrepancies resolved through vendor clarification or design revision
- Final "As-Built" datasheets reflect actual installed valves

**Source:** Typical EPC vendor coordination process

### Quality Requirements

**Datasheet Quality:**

1. **Accuracy:** All data verified against authoritative sources (calculations, P&IDs, specifications, vendor submittals)
2. **Traceability:** All data traceable to source documents (calculation number, P&ID revision, specification section, vendor submittal number)
3. **Clarity:** Datasheets shall be clear and unambiguous; use industry-standard terminology
4. **Completeness:** All required fields populated; TBD items flagged for resolution
5. **Consistency:** Datasheets consistent internally and with related deliverables

**Review and Approval:**

1. **Design Review:** Datasheets reviewed by discipline lead prior to issue
2. **Interdisciplinary Check:** Multi-discipline review for interface correctness (see Procedure.md — Step 3)
3. **Employer Review:** Datasheets submitted to Employer per project submittal schedule (30%, 60%, 90% design) — **TBD**
4. **Approval:** Datasheets approved by discipline lead (P.Eng.) per project authority matrix — **TBD**

**Sign-Off Requirements:**
- Originator sign-off (designer who prepared datasheets)
- Checker sign-off (independent reviewer) — **TBD** if independent check required for datasheets
- Approver sign-off (discipline lead P.Eng.)
- **TBD:** Sign-off protocol per project quality procedures

**Version Control:**

- Initial issue: Rev 0 or A (for procurement)
- Post-procurement vendor data incorporation: Rev 1 or B
- As-Built (final with actual installed valve data): Rev 2 or C (or "As-Built" designation)
- **TBD:** Revision convention per project document control procedures

**Source:** Datasheet quality requirements typical for EPC projects

## Standards

**Applicable codes and standards:**

**Datasheet Format Standards:**
- ISA Form S20.50 — Specification Forms for Process Measurement and Control Instruments (control valve datasheets)
- No equivalent standard forms for isolation and relief valve datasheets; industry practice varies

**Valve Design Standards (referenced in datasheets):**
- **Control Valves:**
  - IEC 60534 / ISA-75 series — Industrial-Process Control Valves
  - ANSI/FCI 70-2 — Control Valve Seat Leakage
- **Isolation Valves:**
  - API 600 — Steel Gate Valves (Flanged and Butt-welding Ends)
  - API 608 — Metal Ball Valves (Flanged, Threaded, and Welding Ends)
  - API 609 — Butterfly Valves (Double-Flanged, Lug- and Wafer-Type)
  - API 6D — Pipeline Valves (Gate, Plug, Ball, and Check Valves)
  - API 598 — Valve Inspection and Testing
  - API 607 — Fire Test for Quarter-Turn Valves
  - ISO 5208 — Industrial Valves – Pressure Testing of Valves
- **Relief Valves:**
  - API 526 — Flanged Steel Pressure-Relief Valves
  - API 527 — Seat Tightness of Pressure Relief Valves
  - ASME BPVC Section VIII — Pressure Vessels (relief valve requirements)
  - CSA B51 — Boiler, Pressure Vessel and Pressure Piping Code

**Materials and Construction:**
- ASME B16.34 — Valves – Flanged, Threaded, and Welding End
- ASME B16.5 — Pipe Flanges and Flanged Fittings (NPS 1/2 through NPS 24)
- ASME B16.47 — Large Diameter Steel Flanges (NPS 26 through NPS 60)
- ASTM standards for materials (A105, A182, A351, A193, A194, etc.)

**Canadian Codes:**
- CSA B51 — Boiler, Pressure Vessel and Pressure Piping Code (mandatory in BC)

**Project-Specific:**
- Employer's Requirements (Volume 2 Parts 1–3) — **TBD** — datasheet format and content requirements
- Project Engineering Standards — **TBD** — datasheet templates, numbering system, review/approval procedures

**Source:** Standards inferred from valve datasheet scope; applicability to be confirmed during datasheet development

## Verification

**Verification methods for Data Sheet deliverables:**

### 1. Designer Self-Check

Originator performs self-check of datasheets prior to submittal for review (see Procedure.md — Step 2 for self-check process):
- Completeness check (all required fields populated; no blanks)
- Accuracy check (data verified against source documents)
- Units check (consistent units; units indicated for all values)
- Internal consistency check (valve size matches line size, pressure rating adequate, etc.)
- Nomenclature check (tag numbers, service descriptions consistent with P&IDs)

### 2. Calculation Cross-Check

Verify sizing data matches DEL-16.03 valve design calculations:
- **Control Valves:** Verify required Cv, selected valve size, trim type, actuator size match calculation results
- **Relief Valves:** Verify set pressure, orifice designation, relief capacity match calculation results
- **Actuators:** Verify required torque/thrust, actuator size, safety factor match calculation results

**Acceptance Criterion:** Datasheet sizing data shall match calculations within rounding tolerance (±2%)

### 3. Specification Compliance Check

Verify datasheet specifications comply with DEL-16.02 valve technical specification:
- Materials comply with specification (body, trim, gaskets, bolting)
- Leakage class complies with specification
- Testing requirements comply with specification
- Code compliance verified (correct design codes cited)

### 4. P&ID Cross-Check

Verify datasheets match P&IDs:
- Tag numbers match P&ID tag numbers (including prefixes: FV, PCV, PSV, XV, MOV, etc.)
- Service descriptions consistent with P&ID service
- Line numbers match P&ID line numbers
- Fail-safe modes (FC, FO, FL) match P&ID notation
- All valves on P&ID have datasheets; all datasheets reference P&ID location

**Acceptance Criterion:** 100% match between datasheets and P&IDs; discrepancies resolved by updating P&ID or datasheet

### 5. Process Simulation Confirmation

For critical control valves, verify valve sizing is consistent with process simulation:
- Flow rates match process simulation cases (normal, design, minimum)
- Pressures match simulation results
- Valve pressure drop within simulation assumptions
- **TBD:** Process simulation verification requirements per project

### 6. Vendor Data Cross-Check (Post-Procurement)

After valve procurement, verify vendor-supplied data matches datasheet requirements (see Procedure.md — Step 4):
- Vendor-certified Cv matches or exceeds required Cv (control valves)
- Vendor ASME stamped capacity matches or exceeds required relief capacity (relief valves)
- Vendor actuator output meets or exceeds required torque/thrust with safety factor
- Vendor materials comply with datasheet specifications
- Vendor testing complies with datasheet requirements

**Acceptance Criterion:** Vendor data complies with datasheet requirements; discrepancies <10% acceptable with engineering justification; discrepancies >10% require design revision or vendor resubmittal

### 7. Interdisciplinary Check (IDC)

Multi-discipline review of datasheets (see Procedure.md — Step 3 for IDC process):
- **Process:** Verify flow rates, pressures, fluid properties correct
- **Piping:** Verify line sizes, pressure classes, end connections correct
- **Instrumentation:** Verify control valve instrumentation (positioner, limit switches) correct
- **Electrical:** Verify electric actuator specifications (voltage, enclosure) correct
- **Control Systems:** Verify fail-safe modes, communication protocols correct

**IDC Comments:**
- Category A (must resolve): Technical errors, safety issues, non-compliance with codes/standards
- Category B (incorporate if feasible): Recommendations, optimizations, clarifications
- Category C (noted): Informational comments, suggestions for future consideration

**Acceptance Criterion:** All Category A comments resolved; Category B/C comments responded to

**Source:** Verification methods typical for datasheet deliverables; specific criteria TBD per project quality procedures

## Documentation

**Required documentation outputs:**

### Primary Deliverables (per _CONTEXT.md)
- **Control Valve Data Sheets:** Individual datasheets for each control valve (one datasheet per valve or grouped by system)
- **Isolation Valve Data Sheets:** Individual datasheets for each isolation valve (manual and automated)
- **Relief Valve Data Sheets:** Individual datasheets for each relief valve

**Format:** **TBD** — **ASSUMPTION:** Standardized form templates (ISA S20.50 for control valves; custom templates for isolation and relief valves)

**Quantity:** **TBD** — Multiple datasheets per category; total quantity TBD pending P&ID development

### Supporting Documentation
- **Valve Register/Index:** List of all valves with tag numbers, types, sizes, and datasheet numbers
- **Datasheet Summary:** Consolidated summary of key valve data (sizes, types, quantities by system)
- **Valve Count by Type:** Summary table (e.g., "15 control valves, 42 isolation valves, 8 relief valves")
- **IDC Comment/Response Log:** Record of interdisciplinary comments and resolutions
- **Vendor Submittal Register:** List of vendor submittals with datasheet references (post-procurement)

**Documentation Requirements:**

**Document Control:**
- All datasheets shall comply with project document control procedures
- Datasheet numbering per project numbering system — **TBD**
  - **ASSUMPTION:** Format "DS-PKG16-CV-###" (control valves), "DS-PKG16-XV-###" (isolation), "DS-PKG16-PSV-###" (relief)
  - Alternate: Datasheet numbers match valve tag numbers (e.g., datasheet for FV-1234 is "FV-1234 Data Sheet")
- Revision control: Initial issue Rev 0 or A; vendor data incorporation Rev 1 or B; As-Built Rev 2 or C — **TBD**
- Distribution list: **TBD** — Engineering disciplines, procurement, vendors, construction, commissioning

**Format:**
- **TBD** — **ASSUMPTION:** PDF for issued datasheets; native files (Excel, Word) for working datasheets
- Page size: **TBD** — Letter (8.5" × 11") or A4
- Header/footer: Project title, datasheet number, valve tag, revision, page number

**Submittal Requirements:**
- 30% Design submittal — **TBD** — Preliminary datasheets for representative valves
- 60% Design submittal — **TBD** — Datasheets for all valves (preliminary vendor selection)
- 90% Design submittal — **TBD** — Near-final datasheets (ready for procurement)
- IFP (Issued for Procurement) — **TBD** — Final datasheets for vendor bidding
- IFC (Issued for Construction) / As-Built — **TBD** — Final datasheets with vendor data incorporated

**Source:** Submittal milestones inferred from decomposition Section 5, PKG-27, DEL-27.04 (Design Submission Packages); specific requirements TBD

**Records Retention:**
- Retention period: **TBD** — **ASSUMPTION**: Facility life + 10 years typical for equipment datasheets (operational record)
- Archival format: **TBD** — **ASSUMPTION:** PDF/A for long-term preservation
- As-Built datasheets transferred to Owner for O&M use

**Source:** Records retention typical for EPC projects; specific requirements TBD per project procedures
