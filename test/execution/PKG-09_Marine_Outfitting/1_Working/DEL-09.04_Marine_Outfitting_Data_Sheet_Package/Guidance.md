# Guidance: DEL-09.04 Marine Outfitting Data Sheet Package

## Purpose

This guidance document supports the development of **Marine Outfitting Data Sheet Package** for **PKG-09 Marine Outfitting**.

**Decomposition definition (authoritative):** Defines and substantiates marine outfitting in accordance with Employer's Requirements. (**Source:** Decomposition, DEL-09.04 row)

This deliverable is classified as a **Data Sheet** under the **Marine** discipline, to be produced by **D&B Contractor**.

**Downstream use:** Data sheets substantiate that selected equipment meets DEL-09.02 specification and Employer's Requirements. They serve design verification, procurement, installation, and QA/QC purposes.

## Principles

### Data Sheet Intent

**Purpose:**
- Data sheets are **evidence artifacts** that substantiate selected equipment meets requirements.
- Data sheets serve multiple critical purposes:
  - **Design verification:** Confirm equipment matches DEL-09.03 calculation requirements (energy/reaction for fenders, SWL for bollards).
  - **Procurement:** Provide basis for RFQs, purchase orders, vendor selection.
  - **Installation:** Define mounting, tolerances, and interface requirements for construction.
  - **QA/QC:** Provide baseline for installation inspection and DEL-09.05 records verification.
  - **Operations/Maintenance:** Provide equipment specifications for facility operations and maintenance planning.

**Key Principles:**
- **Traceability matters:** Vendor document IDs, revisions, and dates should be explicit; certificate attachments should be complete.
- **Consistency is critical:** Data sheet values must match DEL-09.03 calculations; tags must match DEL-09.01 drawings.
- **Completeness over speed:** Mark fields **TBD** if vendor data not available; update when submittals received; do not guess or infer missing data.

**Cross-reference:** Content requirements are defined in `Specification.md § 2`.

### Evidence Rules

**Source Fidelity:**
- Do not infer missing vendor data — mark **TBD** and request the specific vendor submittal.
- Cite vendor document ID, revision, and date for all data sourced from vendor literature.
- Any project-specific modifications or selections should be noted on the data sheet (e.g., non-standard coatings, custom configurations).

**Traceability:**
- Each data field sourced from vendor data shall reference: vendor document number or catalog reference, revision/edition, date.
- Example: "Source: XYZ Fender Co., Catalog ABC-2024, Rev. 3, dated 2024-06-15, Model CF-800."

### Fender Data Sheets (supports SPEC § 2.1)

**Key content:**

**Performance characteristics:**
- **Energy absorption rating:** Energy capacity (kJ) at rated deflection (typically 50-60% of fender dimension).
- **Reaction force at design deflection:** Reaction force (kN) at deflection corresponding to design berthing energy from DEL-09.03.
- **Must be consistent with DEL-09.03 fender reaction calculations:** Cross-check energy and reaction values (verified per `Procedure.md § Step 5`).
- **Reference the specific deflection curve used:** If vendor provides multiple curves (different temperatures, velocities), identify which curve was used for design.

**Deflection/reaction curves:**
- **Attach manufacturer's curves:** Full curves showing energy vs. deflection (E vs δ) and reaction vs. deflection (R vs δ).
- **Note conditions:** Temperature and velocity conditions for curves (e.g., "23°C, 0.1 m/s strain rate").
- **Identify design curve:** If multiple curves provided, clearly identify which curve was used for DEL-09.03 calculations.

**Hardware details:**
- **Chains, pads, frontal frames, fixing systems:** These are integral to fender performance and installation; include specifications, materials, dimensions.
- **Installation hardware:** Anchor bolts, backing plates, shims, gaskets as applicable.

**Corrosion protection:**
- **Coating or protection system:** Specify coating type, dry film thickness (DFT), application method for steel components.
- **Rubber durability:** UV resistance, ozone resistance (per ASTM D1149 or equivalent), service life expectation in marine environment.

**Certificates:**
- **Factory acceptance test (FAT) certificates:** Demonstrating fender performance verification (compression test, deflection measurement).
- **Material certificates:** Rubber compound specifications, steel backing material certificates.
- **Compliance statements:** Vendor attestation of compliance with specification requirements.

**ASSUMPTION:** Fender data sheet format follows project standard or vendor format with project header.

### Bollard Data Sheets (supports SPEC § 2.2)

**Key content:**

**Capacity:**
- **Safe Working Load (SWL):** Rated capacity (kN or tonnes bollard pull); must meet or exceed required capacity from DEL-09.03 bollard load calculations.
- **Design factors:** Note factors applied per codes (e.g., "SWL = 2.0 × maximum line load per BS 6349").
- **Ultimate capacity:** If available from vendor, note ultimate capacity (typically SWL × factor, e.g., 2.5).

**Material specification:**
- **Steel grade:** Cast steel (e.g., ASTM A27 Grade 65-35) or fabricated steel (e.g., ASTM A572 Grade 50); specify grade, heat treatment (if applicable).
- **Casting specifications:** If cast bollard, specify casting standard, inspection requirements (visual, NDT).
- **Hardware materials:** Base plate, anchor bolts, nuts, washers — specify materials and grades.

**Fixing/anchorage:**
- **Foundation type:** Through-bolt, cast-in anchor, post-installed anchor, grout-filled base plate.
- **Anchor details:** Bolt size, grade, embedment depth, spacing; coordinate with PKG-08 if bollard mounted on marine structure.
- **Base plate:** Dimensions, thickness, material, hole pattern.

**Proof load testing:**
- **If required by DEL-09.02 or codes:** Document test requirements (test load typically 1.5 × SWL, hold time, acceptance criteria).
- **Test certificates:** If proof load testing performed, attach test certificates with load curves, results, acceptance sign-off.

**Corrosion protection:**
- **Hot-dip galvanizing or coating system:** Specify standard (ASTM A123, ISO 1461), minimum coating thickness, surface preparation.
- **Touch-up provisions:** Note requirements for field touch-up after installation (if applicable).

**ASSUMPTION:** Bollard data sheet format follows project standard or vendor format with project header.

## Considerations

### Factors to Consider During Development

| Factor | Consideration | Reference |
|--------|---------------|-----------|
| **Tag consistency** | Equipment tags must match across DEL-09.01 drawings, DEL-09.04 data sheets, DEL-09.05 installation records; establish tagging convention early | `Specification.md § 3` |
| **Calculation alignment** | Data sheet performance values (fender energy/reaction, bollard SWL) must match DEL-09.03 calculation results; cross-check required | `Specification.md § 4`; `Procedure.md § Step 5` |
| **Specification compliance** | Data sheet fields should demonstrate compliance with DEL-09.02 performance, materials, installation, quality requirements | `Specification.md § 2` |
| **Vendor submittal timing** | Data sheets depend on vendor selection and submittal availability; may require preliminary data sheets with TBD fields; update when vendor data received | `Guidance.md § Trade-offs` |
| **Attachment management** | Ensure attached curves and certificates are legible, correctly labeled, cross-referenced in data sheet body; version control vendor documents | `Specification.md § 1.3`; `Guidance.md § Trade-offs` |

### Relationship to Other Deliverables

| Deliverable | Relationship | Flow |
|-------------|--------------|------|
| DEL-09.01 Marine Outfitting Design Drawing Set | Provides drawing references and equipment tag locations | DEL-09.01 establishes tags → DEL-09.04 uses tags in data sheets |
| DEL-09.02 Marine Outfitting Technical Specification | Defines field requirements and acceptance criteria | DEL-09.02 specifies requirements → DEL-09.04 demonstrates compliance |
| DEL-09.03 Marine Outfitting Design Calculations | Provides calculation values that data sheets must substantiate | DEL-09.03 calculates performance → DEL-09.04 substantiates with vendor data |
| DEL-09.05 Marine Outfitting Installation & Test Records | Installation records verify as-installed equipment matches data sheets | DEL-09.04 defines baseline → DEL-09.05 verifies as-installed matches |

## Trade-offs

### Competing Concerns to Evaluate

| Trade-off | Factors | Resolution Approach |
|-----------|---------|---------------------|
| **Vendor data completeness vs. schedule** | Complete vendor data may not be available until vendor selection finalized; waiting delays procurement/construction; issuing incomplete data sheets risks rework | **Recommendation:** Issue preliminary data sheets with TBD fields where vendor data not available; clearly mark TBDs with action owners; update data sheets when vendor submittals received; track TBD resolution in action log |
| **Standardization vs. optimization** | Standard products simplify data sheets (one data sheet per type) but may not be optimal for all locations; custom products optimize performance but complicate data sheets | **Recommendation:** Prefer standard products where they meet requirements; document selection basis; use equipment type groups where possible (e.g., "Fender Type A - Qty 8") |
| **Level of detail** | Too much detail increases effort and data sheet length; too little detail reduces value for procurement/installation/QA | **Recommendation:** Include all fields required by DEL-09.02 specification; attach full vendor literature rather than transcribing all details; focus data sheet body on key identification, performance, installation fields |
| **Multiple vendors** | Different vendors may have different data formats and information availability; forcing consistency may delay submittals | **Recommendation:** Use consistent project data sheet format (header, identification, key fields); attach vendor literature as-is for detailed specs; accept vendor format variations in attachments |

## Examples

### Reference Checklists

- Use `Datasheet.md` (Content Checklist) as the minimum checklist for this deliverable.
- Use the decomposition's anticipated artifacts as the baseline:
  - Fender data sheets (one per fender type or individual fender)
  - Bollard data sheets (one per bollard type or individual bollard)

### Typical Data Sheet Structure

**Fender Data Sheet Example:**

1. **Header:** Project name, package, deliverable ID, equipment tag, drawing ref, revision, date
2. **Equipment Identification:** Tag, location, drawing reference
3. **Manufacturer Information:** Vendor name, model, catalog reference, contact
4. **Physical Characteristics:** Dimensions (L × D × H), weight, rubber grade, steel backing
5. **Performance Characteristics:** Energy rating (kJ), reaction force at design deflection (kN), rated deflection (%)
6. **Hardware:** Chains, anchor pads, frontal frame, fixing bolts
7. **Corrosion Protection:** Coating system (type, DFT), service life, UV/ozone resistance
8. **Installation Requirements:** Mounting method, tolerances, orientation
9. **Attachments:** Deflection curves (E vs δ, R vs δ), FAT certificates, material certificates
10. **Notes and Deviations:** Project-specific modifications, TBDs, action items

**Bollard Data Sheet Example:**

1. **Header:** Project name, package, deliverable ID, equipment tag, drawing ref, revision, date
2. **Equipment Identification:** Tag, location, drawing reference
3. **Manufacturer Information:** Vendor name, model (Tee-head, horn, etc.), catalog reference, contact
4. **Physical Characteristics:** Dimensions, weight, steel grade (cast or fabricated)
5. **Capacity:** SWL (kN or tonnes), design factors, ultimate capacity
6. **Corrosion Protection:** Hot-dip galvanizing or coating (standard, thickness)
7. **Fixing/Anchorage:** Foundation type, anchor bolt specs, base plate details
8. **Installation Requirements:** Mounting procedure, tolerances, grouting requirements
9. **Testing:** Proof load test requirements (if applicable), test certificates
10. **Attachments:** Material certificates (MTRs), welding certificates, compliance statements
11. **Notes and Deviations:** Project-specific modifications, TBDs, action items

### Cross-Document Consistency

**Ensure consistency with other DEL-09.04 documents:**
- **Datasheet:** Content Checklist items match Specification requirements and Procedure steps.
- **Specification:** All requirements have corresponding rationale in this Guidance document and verification steps in Procedure.
- **Procedure:** All steps reference applicable Specification requirements and Guidance considerations.

**Ensure consistency with related PKG-09 deliverables:**
- **DEL-09.01:** Equipment tags match drawings; drawing references correct
- **DEL-09.02:** Data sheet fields demonstrate specification compliance
- **DEL-09.03:** Performance values (fender energy/reaction, bollard SWL) match calculations
- **DEL-09.05:** Data sheets provide baseline for installation records verification
