# Datasheet: DEL-26.04 Coating Installation & Test Records

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-26.04 |
| Name | Coating Installation & Test Records |
| Package | PKG-26 Protective Coatings & Painting |
| Discipline | Coatings |
| Type | Record |
| Responsible | D&B Contractor (QA/QC) |
| Status | INITIALIZED |

**Source:** `_CONTEXT.md`

## Attributes

| Attribute | Value | Source |
|-----------|-------|--------|
| Record Category | Installation and Quality Records (Coating Application) | Decomposition DEL-26.04 description |
| Record Types | Surface preparation, coating application, DFT measurement, adhesion test, holiday detection | DEL-26.01 (QR-1, QR-2); DEL-26.02 (Documentation requirements) |
| Record Format | Standard forms/templates completed during coating work | **ASSUMPTION** |
| Retention Period | **TBD** — Per project record retention requirements | Project quality plan |

## Conditions

**Purpose and Context:**

This deliverable provides record templates and compiles completed records that demonstrate compliance with coating requirements specified in DEL-26.01 and procedures defined in DEL-26.02. Records provide traceability and evidence of coating quality for acceptance and project closeout.

**Records Generated During:**
- Surface preparation (per DEL-26.02 surface preparation procedures)
- Coating application (per DEL-26.02 coating application procedures)
- Inspection and testing (per DEL-26.01 QR-1 inspection requirements)

**Source:** DEL-26.01 (QR-2 Documentation); DEL-26.02 (Documentation and Records)

## Construction

**Materials / Configuration:**

This deliverable consists of record templates (forms) and completed records organized by coating application.

### Record Templates and Content

**1. Surface Preparation Records**
- **Purpose:** Document surface preparation activities and acceptance before coating application
- **Content:**
  - Date and time of surface preparation
  - Area/location prepared (tank ID, grid location, etc.)
  - Surface preparation method (SSPC standard achieved: SP-1, SP-3, SP-5, SP-6, SP-10, SP-11)
  - Environmental conditions (temperature, humidity, wind, precipitation)
  - Abrasive type and size (if blast cleaning)
  - Surface cleanliness verification (visual inspection per SSPC-VIS 1)
  - Surface profile measurement (per ASTM D4417)
  - Inspector name and signature
  - Acceptance for coating application (yes/no)
- **Source:** DEL-26.01 (QR-1 Surface Preparation Inspection); DEL-26.02 (Surface Preparation Procedures — Documentation)

**2. Coating Application Records**
- **Purpose:** Document coating application activities and environmental conditions
- **Content:**
  - Date and time of application
  - Area/location coated
  - Coating system applied (primer, intermediate, topcoat)
  - Coating material batch/lot numbers
  - Environmental conditions during application (temperature, humidity, dew point, surface temperature, wind)
  - Wet film thickness (WFT) measurements during application
  - Cure times (start/finish of cure period between coats)
  - Recoat window verification (within manufacturer limits)
  - Applicator name
  - Inspector name and signature
- **Source:** DEL-26.01 (QR-2 Documentation — Application Records); DEL-26.02 (Coating Application Procedures — Documentation)

**3. DFT (Dry Film Thickness) Measurement Records**
- **Purpose:** Document DFT measurements and acceptance per DEL-26.01 requirements
- **Content:**
  - Date and time of measurement
  - Area/location measured (grid pattern or 100% coverage per application)
  - Coating system (primer, intermediate, topcoat, total DFT)
  - DFT readings (location, measurement value in mils or microns)
  - Acceptance criteria (minimum DFT per DEL-26.01)
  - Acceptance (yes/no — all readings meet minimum; average meets target)
  - Non-conformances (areas not meeting DFT requirements)
  - Corrective actions (additional coating applied, re-measured)
  - Inspector name and signature
- **Source:** DEL-26.01 (PR-4 DFT, QR-1 DFT Measurement); SSPC-PA 2

**4. Adhesion Test Records**
- **Purpose:** Document adhesion testing per ASTM D3359
- **Content:**
  - Date and time of test
  - Area/location tested
  - Test method (cross-hatch tape test per ASTM D3359)
  - Test results (rating 0B through 5B)
  - Acceptance criteria (typically 4B or 5B per DEL-26.01)
  - Acceptance (yes/no)
  - Non-conformances (failed adhesion tests)
  - Corrective actions (remove coating, re-prepare surface, re-apply, re-test)
  - Inspector name and signature
- **Source:** DEL-26.01 (PR-3 Adhesion, QR-1 Adhesion Testing); ASTM D3359

**5. Holiday Detection Records (Immersion Service)**
- **Purpose:** Document holiday (pinhole) detection for coatings in immersion service (tank internals, marine immersion zones)
- **Content:**
  - Date and time of inspection
  - Area/location inspected
  - Holiday detection method (low-voltage wet sponge or high-voltage holiday detector)
  - Holidays detected (location, description)
  - Repair actions (surface prep, re-coating of detected holidays)
  - Re-inspection results (holidays repaired and re-tested)
  - Inspector name and signature
- **Source:** DEL-26.01 (QR-1 Holiday Detection); DEL-26.02 (Coating Application Procedures — Holiday Detection)

**6. Final Acceptance Records**
- **Purpose:** Document final coating acceptance after all work complete
- **Content:**
  - Date of final acceptance
  - Area/location accepted (tank ID, structure ID, etc.)
  - Summary of coating work (coating system applied, total DFT achieved)
  - Summary of inspection and testing (surface prep acceptance, DFT acceptance, adhesion tests passed, holidays repaired)
  - Final acceptance (yes/no — all requirements met per DEL-26.01)
  - Inspector name and signature
  - QA/QC manager approval signature
- **Source:** DEL-26.01 (QR-1 Inspection and Testing); DEL-26.02 (Coating Application Procedures — Final Acceptance)

## References

**Source documents:**
- **Decomposition:** Section 5 PKG-26, DEL-26.04
- **Context:** `_CONTEXT.md`
- **Cross-documents:** `Specification.md`, `Guidance.md`, `Procedure.md` (this deliverable)

**Primary upstream references:**
- **DEL-26.01** (Coating Technical Specification) — Defines requirements and acceptance criteria documented in these records
- **DEL-26.02** (Coating Procedures) — Procedures generate these records during execution
- **DEL-26.03** (Coating Data Sheet Package) — Manufacturer data sheets provide acceptance criteria (DFT, adhesion)

**Applicable standards:**
- **SSPC-PA 2:** Measurement of Dry Coating Thickness (DFT measurement method)
- **SSPC-VIS 1:** Visual Standard for Abrasive Blast Cleaned Steel (surface prep acceptance)
- **ASTM D3359:** Adhesion testing (cross-hatch tape test)
- **ASTM D4417:** Surface profile measurement

**Cross-references (internal to PKG-26):**
- **DEL-26.01** (Specification) — QR-1 (Inspection), QR-2 (Documentation)
- **DEL-26.02** (Procedures) — Documentation sections in surface prep and coating application procedures
- **DEL-26.03** (Data Sheet Package) — Manufacturer data for acceptance criteria

**Cross-references (interdisciplinary):**
- **PKG-30** (Commissioning) — Tank internal coating records submitted for commissioning acceptance
- **PKG-13** (Storage Tanks) — Tank coating records filed with tank documentation

**Dependency tracking:** NOT_TRACKED

**Project objectives:**
- **OBJ-1:** Safe & Reliable Operation — Records demonstrate coating quality for reliable corrosion protection
- **OBJ-3:** Storage Capacity — Tank internal coating records demonstrate food-grade compliance
- **OBJ-9:** Lifecycle Cost Optimization — Quality records support warranty and lifecycle maintenance

**Source:** Decomposition Section 6
