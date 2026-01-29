# Specification: DEL-09.04 Marine Outfitting Data Sheet Package

## Scope

This specification defines the requirements for producing **Marine Outfitting Data Sheet Package** within **PKG-09 Marine Outfitting**.

**Decomposition definition (authoritative):** Defines and substantiates marine outfitting in accordance with Employer's Requirements. (**Source:** Decomposition, DEL-09.04 row)

**Package scope (PKG-09):** Fenders, bollards, ladders, life-saving equipment, existing Berth 10 upgrades and repairs. (**Source:** Decomposition, PKG-09)

**Anticipated deliverable artifacts:**
- Fender data sheets
- Bollard data sheets

**Purpose:** Data sheets are evidence artifacts that substantiate selected equipment meets DEL-09.02 specification and Employer's Requirements. They serve design verification, procurement, installation, and QA/QC purposes.

## Requirements

### 1) Data Sheet Package Structure Requirements

The data sheet package shall include the following (per `Datasheet.md` Content Checklist and `Guidance.md § Examples`). Cross-reference to verification steps in `Procedure.md`.

#### 1.1 Cover/Index

**Requirements:**
- Title page identifying the package (project name, package ID, deliverable ID, revision, date).
- Index listing all included data sheets with:
  - Equipment tag
  - Equipment type (fender type, bollard type)
  - Data sheet reference/page number
  - Revision and date
- **TBD:** Format per project document control procedures.

**Rationale:** See `Guidance.md § Principles (Data Sheet Intent)`.
**Verification:** See `Procedure.md § Step 7` (issue preparation).

#### 1.2 Equipment Identification

**Requirements:**
- Each data sheet shall include:
  - **Equipment tag:** Per project equipment tagging convention (**TBD** — format to be established; e.g., "FEN-01" for fenders, "BOL-01" for bollards).
  - **Drawing reference(s):** Per DEL-09.01 drawing numbers showing equipment location.
  - **Location identifier:** Descriptive location (e.g., "Berth face Sta. 0+25.0, El. +3.5m").
- **Tag consistency:** Tags shall be consistent across DEL-09.01 drawings, DEL-09.04 data sheets, and DEL-09.05 installation records.
- **Traceability:** Tag shall uniquely identify each equipment item for tracking through design, procurement, installation, and operations.

**Rationale:** See `Guidance.md § Considerations (Tag consistency)`.
**Verification:** See `Procedure.md § Step 5` (verify consistency).

#### 1.3 Attachments

**Requirements:**
- Supporting documents shall be attached or referenced:
  - **Manufacturer product literature:** Vendor catalog sheets, product brochures (cite vendor document number, revision, date).
  - **Performance curves:** Fender deflection/reaction curves (attach full curve; identify specific curve used for design per DEL-09.03).
  - **Certificates and test reports:** FAT certificates, material certificates (MTRs), proof load test certificates (if applicable), compliance statements.
  - **Installation instructions:** Vendor installation procedures or guidelines (if provided).
- **Attachment management:** Ensure all attachments are legible, correctly labeled, and cross-referenced in data sheet body.
- **Version control:** All vendor documents shall be cited with document number, revision, and date.

**Rationale:** See `Guidance.md § Principles (Evidence Rules)` and `Guidance.md § Considerations (Attachment management)`.
**Verification:** See `Procedure.md § Step 5` (verify vendor document references).

### 2) Content Coverage Requirements

The data sheet package shall contain data sheets for each equipment category (per `Datasheet.md` Content Checklist). Requirements shall demonstrate compliance with DEL-09.02 specification.

#### 2.1 Fender Data Sheets

**Required fields (per `Datasheet.md § Fender Data Sheets`):**

| Requirement | Content | Guidance § | Procedure § | Status |
|-------------|---------|------------|-------------|--------|
| **Identification** | Tag per project convention, drawing ref (DEL-09.01), location | Guidance § Principles | Proc § Step 4 | **TBD** |
| **Manufacturer/model** | Vendor name, model/type designation, catalog reference | Guidance § Principles | Proc § Step 3, 4 | **TBD** — vendor selection |
| **Physical data** | Dimensions (L × D × H), weight, rubber grade, steel backing material | Guidance § Principles | Proc § Step 4 | **TBD** — vendor data |
| **Performance data** | Energy absorption (kJ at rated deflection), reaction force at design deflection (kN), rated deflection (%) | Guidance § Principles | Proc § Step 4, 5 | **TBD** — substantiated by DEL-09.03 |
| **Deflection curves** | Manufacturer curves (E vs δ, R vs δ) with temperature/velocity conditions; identify curve used for design | Guidance § Principles | Proc § Step 3, 4 | **TBD** — vendor data |
| **Hardware** | Chains, anchor pads, frontal frame, fixing bolts | Guidance § Principles | Proc § Step 4 | **TBD** — vendor data |
| **Corrosion protection** | Coating system (type, DFT), service life, UV/ozone resistance | Guidance § Principles | Proc § Step 4 | **TBD** — per DEL-09.02 § 1.4 |
| **Installation** | Mounting method, tolerances, orientation | Guidance § Principles | Proc § Step 4 | **TBD** — per DEL-09.02 § 1.5 |
| **Certificates** | FAT certificates, material certs, compliance statements | Guidance § Principles | Proc § Step 3, 4 | **TBD** — vendor submittals |

**Verification:** Fender performance values (energy, reaction) shall match DEL-09.03 calculation results (verified per `Procedure.md § Step 5`).

**Rationale:** See `Guidance.md § Principles (Fender Data Sheets)`.

#### 2.2 Bollard Data Sheets

**Required fields (per `Datasheet.md § Bollard Data Sheets`):**

| Requirement | Content | Guidance § | Procedure § | Status |
|-------------|---------|------------|-------------|--------|
| **Identification** | Tag per project convention, drawing ref (DEL-09.01), location | Guidance § Principles | Proc § Step 4 | **TBD** |
| **Manufacturer/model** | Vendor name, model/type (Tee-head, horn, etc.), catalog reference | Guidance § Principles | Proc § Step 3, 4 | **TBD** — vendor selection |
| **Physical data** | Dimensions, weight, steel grade (cast/fabricated) | Guidance § Principles | Proc § Step 4 | **TBD** — vendor data |
| **Capacity** | SWL (kN or tonnes), design factors, ultimate capacity | Guidance § Principles | Proc § Step 4, 5 | **TBD** — substantiated by DEL-09.03; verify SWL ≥ required |
| **Corrosion protection** | Coating or hot-dip galvanizing (standard, thickness) | Guidance § Principles | Proc § Step 4 | **TBD** — per DEL-09.02 § 1.4 |
| **Fixing/anchorage** | Foundation type (through-bolt, cast-in, post-installed), anchor specs, base plate | Guidance § Principles | Proc § Step 4 | **TBD** — coordinate PKG-08 if on structure |
| **Proof load** | Test requirements (if applicable), test load (1.5 × SWL typical), certificates | Guidance § Principles | Proc § Step 3, 4 | **TBD** — per DEL-09.02 § 2.2 and codes |
| **Installation** | Mounting procedure, tolerances, grouting (if applicable) | Guidance § Principles | Proc § Step 4 | **TBD** — per DEL-09.02 § 1.5 |
| **Certificates** | Material certs (MTRs), welding certs (if fabricated), compliance statements | Guidance § Principles | Proc § Step 3, 4 | **TBD** — vendor submittals |

**Verification:** Bollard capacity (SWL) shall meet or exceed required capacity from DEL-09.03 calculation (verified per `Procedure.md § Step 5`).

**Rationale:** See `Guidance.md § Principles (Bollard Data Sheets)`.

### 3) Interface / Coordination Requirements

**Tag consistency is critical:**
- Equipment tags shall align across:
  - **DEL-09.01 drawings:** Tags shown on drawings
  - **DEL-09.04 data sheets:** Tags used in data sheet identification
  - **DEL-09.05 installation records:** Tags used in installation and test records
  - **Asset tagging conventions:** Tags used in facility asset management system (**TBD** — asset tagging system to be confirmed)
- **Coordination mode:** Dependencies are managed externally (NOT_TRACKED). See `_DEPENDENCIES.md` and `execution/_Coordination/_COORDINATION.md`.

**Verification:** See `Procedure.md § Step 5` (verify tag alignment).

### 4) Quality / Traceability Requirements

**Vendor data traceability:**
- Each data sheet shall state the vendor source document with full traceability:
  - Vendor document number or catalog reference
  - Revision or edition
  - Date or publication date
  - Vendor name and contact information
- **Example citation:** "Source: XYZ Fender Co., Catalog ABC-2024, Rev. 3, dated 2024-06-15, Model CF-800."

**Project-specific deviations:**
- Any project-specific modifications, selections, or deviations from standard vendor data shall be noted clearly on data sheet (e.g., "Non-standard coating per project specification").

**Missing information:**
- Missing information shall be marked **TBD** and tracked for vendor submittal follow-up.
- Maintain action log with action owner and target date for TBD resolution.

**Calculation consistency:**
- Data sheet values shall be consistent with DEL-09.03 calculation results:
  - Fender energy/reaction values match DEL-09.03 fender calculation
  - Bollard SWL meets or exceeds DEL-09.03 required capacity
  - Cross-check performed per `Procedure.md § Step 5`

**Verification:** See `Procedure.md § Step 5` (verify consistency with calculations).

## Standards

- Employer's Requirements (Vol 2 Part 1–3) — applicable clauses **TBD** (see `_REFERENCES.md`); submittal requirements and data sheet content.
- **ASSUMPTION:** Data sheet/submittal standards per Employer's Requirements and project document control procedures.

## Verification

**Verification methods for Data Sheet deliverables (per `Procedure.md`):**

| Method | Applicability | Criteria | Procedure § |
|--------|---------------|----------|-------------|
| Vendor data cross-check | All data sheets | Correct vendor doc ID, revision, date cited; vendor data correctly transcribed | Proc § Step 5 |
| Completeness check | All data sheets | All required fields per `Datasheet.md` Content Checklist addressed (completed or TBD with action) | Proc § Step 5 |
| Calculation consistency check | All data sheets | Fender energy/reaction values and bollard SWL match DEL-09.03 calculation results | Proc § Step 5 |
| Tag alignment check | All data sheets | Equipment tags match DEL-09.01 drawings; no discrepancies | Proc § Step 5 |
| Units/nomenclature check | All data sheets | Consistent units (SI: kN, kJ, mm, tonnes); consistent terminology across data sheets | Proc § Step 5 |
| Peer review | All data sheets | Technical accuracy, completeness, specification compliance | Proc § Step 6 |

**Acceptance criteria (per `Datasheet.md § Acceptance`):**
- Data sheet package covers all decomposition-listed artifacts (fender + bollard data sheets).
- All Content Checklist items in `Datasheet.md` are addressed (completed or TBD with action).
- Data sheet values are consistent with DEL-09.03 calculation results.
- Equipment tags align with DEL-09.01 drawings.
- Data sheets demonstrate compliance with DEL-09.02 specification requirements.
- Vendor source documents properly referenced with full traceability.

## Documentation

**Required documentation outputs (per decomposition and `Datasheet.md`):**
- Fender data sheets (one per fender or fender group)
- Bollard data sheets (one per bollard or bollard type)

**Documentation requirements:**
- All documents shall comply with project document control procedures.
- Revision control per project numbering system — **TBD**.
- Format: **TBD** — **ASSUMPTION:** Project data sheet template or vendor format with project header; PDF for issue/record.
- Records management per `Procedure.md § Records`.
