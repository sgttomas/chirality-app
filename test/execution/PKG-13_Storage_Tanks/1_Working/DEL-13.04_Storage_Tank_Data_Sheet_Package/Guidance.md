# Guidance: DEL-13.04 Storage Tank Data Sheet Package

## Purpose

This guidance document supports the development of **Storage Tank Data Sheet Package** for **PKG-13 Storage Tanks**.

### Deliverable Context

**Description:** Defines and substantiates storage tank in accordance with ER requirements.

**Source:** _CONTEXT.md, Decomposition document DEL-13.04

This deliverable is classified as a **Data Sheet** under the **Mechanical** discipline, to be produced by **D&B Contractor**.

### Role in Project Delivery

Data sheets serve as the primary technical summary documents for equipment procurement, fabrication, installation, and operations. They consolidate design information from multiple sources (drawings, calculations, specifications) into concise, single-page summaries that equipment vendors, fabricators, installers, and operators use as the authoritative source of equipment parameters.

For PKG-13 Storage Tanks, this deliverable provides:
- Tank data sheets (3) summarizing each 15,000 MT storage tank
- Agitator data sheets (3) summarizing mixing equipment for each tank
- Overflow protection data sheet(s) summarizing overfill protection systems

**Source:** Typical data sheet function in engineering projects; _CONTEXT.md (Anticipated Artifacts)

### Downstream Use

- **Fabrication:** Tank fabricator uses tank data sheets as basis for detailed fabrication drawings
- **Procurement:** Agitator vendor uses agitator data sheets to verify compliance with specification
- **Installation:** Installation contractor uses data sheets to verify received equipment and plan installation
- **Commissioning:** Commissioning team uses data sheets to verify equipment performance
- **Operations:** Operations team uses data sheets as quick reference for equipment parameters
- **Maintenance:** Maintenance team uses data sheets to plan maintenance activities and order spare parts

**Source:** Typical data sheet downstream use

---

## Principles

### Design Principles

**DP-01: Equipment Documentation Philosophy**

Data sheets are not design documents — they are technical summaries extracted from design documents. The design exists in drawings, calculations, and specifications; the data sheet consolidates that design information into a standardized, easy-to-reference format.

**Key principle:** Data sheets shall be derived from design documents, not created independently. Every value on a data sheet shall have a traceable source in a design drawing, calculation, specification, or vendor document.

**Source:** Typical engineering documentation hierarchy

**DP-02: Vendor Data Integration**

Agitator data sheets require integration of vendor-supplied information. The design specification (DEL-13.02) defines performance requirements; the vendor selection process identifies a compliant vendor; the vendor provides detailed technical data that is incorporated into the agitator data sheet.

**Key principle:** Vendor data shall be validated against specification requirements before integration. Discrepancies shall be identified, evaluated, and resolved through engineering review and/or vendor clarification.

**Source:** Typical vendor data coordination workflow

**DP-03: Cross-Discipline Coordination**

Tank and agitator data sheets interface with multiple disciplines:
- **Piping (PKG-14):** Nozzle sizes, ratings, service descriptions, line numbers
- **Instrumentation (PKG-20):** Instrumentation connections, tag numbers, measurement ranges
- **Electrical (PKG-17):** Agitator motor data, electrical supply parameters
- **Control Systems (PKG-19):** Agitator control interface, overflow protection alarm/interlock logic

**Key principle:** Data sheets shall be verified with all interfacing disciplines before issuance. Interdisciplinary checks are mandatory.

**Source:** Typical interdisciplinary coordination requirements

**DP-04: Standardization and Consistency**

Within a project, data sheets shall use consistent format, terminology, and units. Tank data sheets for all three tanks shall follow the same template. Agitator data sheets for all three agitators shall follow the same template.

**Key principle:** Standardization improves usability, reduces errors, and streamlines review. Use project-approved templates without deviation unless justified by technical necessity.

**Source:** Typical project documentation standards

**DP-05: Traceability and Version Control**

Data sheets evolve through the project lifecycle as design matures and vendor data becomes available. Each revision shall be tracked, and the current revision shall be clearly identifiable.

**Key principle:** Maintain revision history on each data sheet. Superseded revisions shall be archived but not destroyed, to preserve design evolution history.

**Source:** Typical document control principles

---

## Considerations

### Factors to Consider During Development

**C-01: Data Sheet Timing**

Data sheets are typically produced in multiple stages:
- **Preliminary (Design Stage):** Based on design calculations and specifications, before vendor selection
- **Interim (Procurement Stage):** Updated with vendor selection and preliminary vendor data
- **Final (As-Built Stage):** Updated with final vendor data and as-built information

**TBD** — Project staging and data sheet issuance milestones

**Source:** Typical data sheet development timeline

**C-02: Level of Detail**

Data sheets shall provide sufficient detail for their intended use, but shall not duplicate design drawings or specifications. Strike a balance between completeness and conciseness.

**Example:** Nozzle summary on tank data sheet lists nozzle sizes, ratings, and services, but does not duplicate the detailed nozzle schedule drawing showing orientations, elevations, and weld details.

**Source:** Typical data sheet content conventions

**C-03: Tank-Specific vs. Generic Data**

Three tanks are nominally identical (3 × 15,000 MT), but may have variations:
- **Identical:** Capacity, dimensions, materials, design pressure/temperature
- **Potentially different:** Nozzle orientations (to suit piping layout), instrumentation (to suit control logic), Phase 2 connections (if expansion is staged)

**Key consideration:** Determine which data is truly identical and which data requires tank-specific verification.

**TBD** — Tank-to-tank variations require design review

**Source:** ASSUMPTION based on typical tank farm design

**C-04: Agitator Vendor Data Availability**

Agitator data sheets cannot be finalized until vendor is selected and vendor data is received. Plan for interim data sheet issuance with design basis values, followed by final data sheet issuance with vendor data.

**Key consideration:** Identify which agitator data fields are design basis (specified by D&B Contractor) vs. vendor-specific (provided by agitator manufacturer).

**Source:** Typical vendor equipment procurement workflow

**C-05: Overflow Protection System Configuration**

Overflow protection may be:
- **Single system:** One overflow protection system serving all three tanks with shared alarm logic
- **Individual systems:** One overflow protection system per tank with independent alarm logic

**TBD** — System configuration requires process design and control logic review

This decision affects whether one data sheet or three data sheets are required.

**Source:** Typical overflow protection design options

**C-06: Units and Nomenclature Standards**

Confirm project unit system early:
- **SI units:** Meters, kilograms, Celsius, Pascals
- **Imperial units:** Feet, pounds, Fahrenheit, PSI
- **Mixed units:** Common in Canadian projects (e.g., dimensions in meters, pressures in PSI)

Confirm nomenclature standards:
- Tag numbering (TK-101 vs. T-101 vs. 13-TK-0101)
- Service descriptions (CSD canola oil vs. Crude Super Degummed Canola Oil)

**TBD** — Project unit system and nomenclature standards require project engineering manual

**Source:** ASSUMPTION based on typical project standards development

**C-07: Interface with Installation and Test Records**

Data sheets are referenced by installation and test records (DEL-13.05). Installation contractor verifies received equipment against data sheets; test records document as-built deviations.

**Key consideration:** Data sheet format and content shall facilitate field use (clear, concise, printable).

**Source:** DEL-13.05 relationship

**C-08: Interface with Fabrication Quality Documentation**

Data sheets are referenced by fabrication quality documentation (DEL-13.06). Fabricator verifies material certifications and fabrication records against data sheet material specifications.

**Key consideration:** Material specifications on data sheets shall match material certifications required by specification (DEL-13.02).

**Source:** DEL-13.06 relationship

---

## Trade-offs

### Competing Concerns to Evaluate

**T-01: Template Standardization vs. Customization**

**Trade-off:**
- **Standardized template:** Easier to produce, review, and use; ensures consistency across all data sheets
- **Customized template:** Allows optimization for specific equipment type; may capture unique data more effectively

**Recommendation:** Use standardized project templates unless technical justification exists for customization. For this deliverable, use same template for all three tank data sheets and same template for all three agitator data sheets, but allow different templates for tanks vs. agitators.

**Source:** Typical project template philosophy

**T-02: Preliminary vs. Final Issuance**

**Trade-off:**
- **Early preliminary issuance:** Provides information to downstream users sooner, but may contain TBDs or preliminary values that change later
- **Delayed final issuance:** Ensures data is complete and verified, but delays availability to downstream users

**Recommendation:** Issue preliminary data sheets when design basis is established (post-calculations, pre-vendor selection). Issue interim data sheets when vendor is selected (preliminary vendor data). Issue final data sheets when vendor data is complete and verified.

**Source:** Typical data sheet issuance strategy

**T-03: Level of Detail: Summary vs. Comprehensive**

**Trade-off:**
- **Summary format:** Concise, single-page, easy to use; may omit some technical details
- **Comprehensive format:** Captures all technical data; may be multi-page and harder to use as quick reference

**Recommendation:** Data sheets should be concise summaries (single page preferred). Detailed data remains in source documents (drawings, calculations, specifications). Exception: Agitator data sheets may be multi-page if vendor data is extensive.

**Source:** Typical data sheet format conventions

**T-04: Manual vs. Automated Data Sheet Generation**

**Trade-off:**
- **Manual (Excel/Word template):** Simple, flexible, no specialized tools required; higher risk of transcription errors
- **Automated (database-driven):** Reduces transcription errors, ensures consistency with source data; requires database setup and maintenance

**Recommendation:** For this project scale (3 tanks, 3 agitators), manual data sheet generation using Excel templates is likely sufficient. Consider automated generation for larger projects or if project document management system supports it.

**TBD** — Data sheet generation method requires project document management system capabilities

**Source:** Typical project data management approach

---

## Examples

### Reference Examples and Precedents

**Example 1: Tank Data Sheet Typical Content**

Typical tank data sheet includes:
- **Identification:** Tag number, service, design standard
- **Capacity:** Volume and mass capacity
- **Dimensions:** Diameter, height, shell courses
- **Materials:** Shell, bottom, roof material specifications
- **Design Conditions:** Pressure, temperature, seismic, wind, snow
- **Nozzle Summary:** Table of all nozzles with size, rating, service
- **Internals:** Agitator, water draw-off, overflow protection
- **Coatings:** Internal and external coating systems
- **Foundation:** Foundation type and loading

**Source:** Typical API 650 tank data sheet practice

**Example 2: Agitator Data Sheet Typical Content**

Typical agitator data sheet includes:
- **Identification:** Tag number, service, tank tag
- **Manufacturer Data:** Manufacturer, model, serial number
- **Impeller Data:** Type, diameter, speed
- **Motor Data:** Power, voltage, speed, enclosure
- **Shaft Data:** Length, diameter, material
- **Mounting:** Mounting type, nozzle size, orientation
- **Performance:** Mixing intensity, turnover time
- **Utilities:** Electrical supply, control interface

**Source:** Typical industrial agitator data sheet practice

**Example 3: Interdisciplinary Check Scenario**

**Scenario:** Tank data sheet shows inlet nozzle as 12" 150# ANSI. Piping P&ID shows inlet line as 10" 150#.

**Resolution:** Interdisciplinary check identifies discrepancy. Engineering review determines piping line size is correct (10" per hydraulic calculations). Tank data sheet is corrected to 10" 150# ANSI inlet nozzle. Design drawing (DEL-13.01) nozzle schedule is also corrected. Discrepancy documented in design change log.

**Lesson:** Interdisciplinary checks catch errors before construction. Early identification avoids field rework.

**Source:** Typical interdisciplinary coordination scenario

**Example 4: Vendor Data Integration Scenario**

**Scenario:** Specification (DEL-13.02) requires agitator motor to be 600V, 3-phase, 60Hz, TEFC enclosure, 10 HP minimum. Vendor proposes 15 HP motor to meet mixing performance. Vendor data sheet provides detailed motor data (manufacturer, model, weight, dimensions, efficiency).

**Resolution:** Engineering review confirms 15 HP motor is acceptable (meets performance with margin). Agitator data sheet is populated with vendor-provided motor data (15 HP, manufacturer, model). Specification requirement is met (exceeds 10 HP minimum).

**Lesson:** Vendor data integration requires engineering judgment to verify compliance with specification. Vendor data is not blindly copied — it is reviewed and validated.

**Source:** Typical vendor data coordination scenario

---

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|-------------|----------|----------|----------|-------------------|-------------------|--------------|
| CT-13.04-01 | Tank tag numbering convention (TK-xxx vs. T-xxx) | Consideration C-06 | Project engineering manual (TBD) | Datasheet.md Data Sheet Scope; all data sheets | Project numbering standard | **TBD** |
| CT-13.04-02 | Agitator vendor data availability timing vs. data sheet issuance schedule | Consideration C-04 | Project schedule (TBD) | Datasheet.md Timing; Specification.md FR-04 | Project schedule + procurement plan | **TBD** |
| CT-13.04-03 | Tank-to-tank variations (nozzle orientations, Phase 2 connections) | Consideration C-03 | DEL-13.01 design decisions (TBD) | All tank data sheets | Design freeze / DEL-13.01 drawings | **TBD** |
| CT-13.04-04 | Overflow protection system configuration (single vs. individual) | Consideration C-05 | Process design / PKG-19 control logic (TBD) | Overflow data sheet(s) | Process engineering + P&IDs | **TBD** |

**Note:** These conflicts represent data sheet coordination decisions requiring design inputs and project standards. Resolution during WORKING_ITEMS will enable data sheet finalization.

---

**Document Status:** Pass 3 Complete — Enrichment complete. Design principles, considerations, trade-offs, and examples developed. Conflict Table added for data sheet coordination decisions requiring human ruling. Cross-document references verified. All TBDs marked. ASSUMPTIONs labeled. Ready for WORKING_ITEMS refinement.

**Last Updated:** 2026-01-28
