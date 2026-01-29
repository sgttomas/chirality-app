# Guidance: DEL-13.05 Storage Tank Installation & Test Records

## Purpose

This guidance document supports the development of **Storage Tank Installation & Test Records** for **PKG-13 Storage Tanks**.

### Deliverable Context

**Description:** Provides evidence of completion, inspection, and testing for storage tank.

**Source:** _CONTEXT.md, Decomposition document DEL-13.05

This deliverable is classified as a **Record** under the **Mechanical** discipline, to be produced by **D&B Contractor (QA/QC)**.

### Role in Project Delivery

Installation and test records are the objective quality evidence that demonstrates:
1. Materials conform to specifications
2. Workmanship meets code requirements (API 650, CSA W59)
3. Tanks are structurally sound and leak-free
4. Tanks are ready for commissioning and operation

These records are not design documents or procedures — they are **evidence** collected during fabrication, installation, and testing that demonstrates compliance. They form the as-built quality dossier for each tank.

**Source:** Typical quality assurance documentation purpose; API 650 quality requirements

### Downstream Use

- **Client Acceptance:** Client reviews records to verify quality before accepting facility
- **Regulatory Compliance:** Authorities may require quality records for permit compliance or inspections
- **Insurance:** Insurers may require quality records for coverage
- **Operations:** Operations team references records for understanding tank as-built configuration
- **Maintenance:** Maintenance team uses weld maps and material certificates for future repairs
- **Incident Investigation:** Records provide baseline data if structural issues arise

**Source:** Typical quality record downstream use

---

## Principles

### Design Principles

**DP-01: Quality Evidence Philosophy**

Installation and test records are **objective evidence** of compliance. They are factual documentation of what was built and tested, not interpretations or summaries.

**Key principle:** Records shall be contemporaneous (created at the time of the activity), authentic (signed by qualified personnel), and traceable (cross-referenced to design documents and specifications).

Every record answers a quality question:
- **Material certificates:** "Did we use the right materials?"
- **Weld maps:** "Where are the welds and who made them?"
- **NDE reports:** "Do the welds meet acceptance criteria?"
- **Hydrostatic test records:** "Is the tank structurally sound and leak-free?"

**Source:** Typical QA record philosophy

**DP-02: Traceability**

Traceability is essential for quality assurance and future maintenance. If a material defect is discovered after commissioning, traceability allows identification of all affected components.

**Example traceability chain:**
1. Material certificate (Heat #12345) shows shell plate delivered
2. Weld map shows Heat #12345 used in shell course 3, weld joints W-301 through W-305
3. NDE reports show weld joints W-301 through W-305 examined and accepted
4. If Heat #12345 is later found defective, shell course 3 can be identified for inspection or replacement

**Key principle:** Every material heat shall be traceable to specific tank components. Every weld joint shall be traceable to NDE results.

**Source:** API 650 quality assurance requirements; typical material traceability practice

**DP-03: API 650 Compliance Documentation**

API 650 is the governing design and construction standard for these storage tanks. The installation and test records demonstrate compliance with API 650 requirements:

| API 650 Requirement | Record Evidence |
|---------------------|-----------------|
| Section 2.2: Materials meet specifications | Material certificates (MTRs) |
| Section 8: Welds meet acceptance criteria | NDE reports |
| Section 7.4: Tank passes hydrostatic test | Hydrostatic test records |
| Section 8: Weld procedure and welder qualification | WPS/PQR/WPQ (DEL-13.06) referenced on weld map |

**Key principle:** Records shall explicitly demonstrate API 650 compliance. Do not assume compliance — document it with objective evidence.

**Source:** API 650 quality documentation requirements

**DP-04: As-Built Documentation**

Design documents show the intended design. Installation and test records show the as-built reality. Deviations occur during construction (field modifications, repair welds, material substitutions).

**Key principle:** Records shall reflect as-built conditions, not design intent. Weld maps shall be updated with repair welds. NDE reports shall document all examination cycles including repairs. Material certificates shall reflect materials actually used, not materials originally specified (if substitutions occurred with approved design changes).

**Source:** Typical as-built documentation philosophy

**DP-05: Hold and Witness Points**

Certain quality activities require client witness or hold points per the Inspection and Test Plan (ITP — DEL-29.02). Hold points cannot proceed without client sign-off. Witness points allow client observation.

**Key principle:** Records for hold/witness activities shall include client inspector signature confirming observation or acceptance. Do not proceed past hold points without client release.

**Source:** Typical ITP and quality hold point practice

---

## Considerations

### Factors to Consider During Development

**C-01: Record Collection Timing**

Quality records are generated at different phases:
- **Material certificates:** During procurement (before fabrication begins)
- **Weld maps:** During fabrication (updated progressively as welding proceeds)
- **NDE reports:** During fabrication (after each weld or weld sequence is completed)
- **Hydrostatic test records:** After erection (before commissioning)

**Key consideration:** Establish record collection workflow early. QA personnel shall be present during fabrication and testing to collect records in real time. Retroactive record collection is difficult and may result in missing data.

**Source:** Typical QA workflow planning

**C-02: Material Certificate Verification**

Material certificates are provided by suppliers. Not all suppliers provide complete or correct certificates.

**Key consideration:** Review MTRs upon receipt. Verify:
- Material grade matches specification
- Heat number is legible and unique
- Chemical composition is within specification limits
- Mechanical properties (yield, tensile, elongation) are within specification limits
- Mill or supplier stamp/signature is present

Reject incomplete or incorrect certificates before materials are used. Once materials are fabricated into the tank, correcting certificate deficiencies is difficult.

**Source:** Typical material receiving inspection practice

**C-03: Weld Map Development**

Weld maps can be developed two ways:
1. **Pre-fabrication:** Create preliminary weld map from design drawings showing planned weld joint locations; update with welder IDs and dates during fabrication
2. **Post-fabrication:** Create weld map after fabrication by documenting actual weld joint locations

**Recommendation:** Pre-fabrication approach is preferred. It provides fabricator with clear weld joint identification system before welding begins, reducing confusion and improving traceability.

**TBD** — Weld map development timing and responsibility (D&B Contractor or tank fabricator)

**Source:** Typical weld map development practice

**C-04: NDE Extent and Sampling**

API 650 allows spot examination (sampling) of vertical and horizontal shell welds (see API 650 Table 8-1). Spot examination reduces NDE cost and schedule but provides less assurance than full examination.

**Key consideration:** Determine NDE extent (spot vs. full) early in project. Factors:
- **Cost:** Full examination is more expensive
- **Schedule:** Full examination takes longer
- **Risk:** Spot examination may miss defects; full examination provides higher assurance
- **Client preference:** Client may require full examination regardless of API 650 allowances

**TBD** — NDE extent per project specification (DEL-13.02) and ER

**Source:** API 650 Section 8.1; typical NDE planning

**C-05: NDE Repair Cycles**

When NDE identifies defects exceeding acceptance criteria, welds must be repaired and re-examined. Multiple repair cycles may occur.

**Key consideration:** Document all repair cycles. Retain all NDE reports (initial examination showing defect, post-repair examination showing acceptance). Do not discard "failed" NDE reports — they are part of the quality record showing the repair process.

**Source:** Typical NDE and repair documentation practice

**C-06: Hydrostatic Test Witness**

Hydrostatic testing is typically a hold point requiring client witness. Client inspector observes test setup, filling, hold period, and draining.

**Key consideration:** Coordinate hydrotest timing with client to ensure witness is available. Do not perform hydrotest without client release if it is a hold point per ITP (DEL-29.02).

Settlement measurements are critical. Use survey equipment to measure foundation settlement before, during, and after testing. Excessive settlement may indicate foundation problems requiring engineering evaluation.

**TBD** — Client witness requirements per ER and ITP (DEL-29.02)

**Source:** API 650 Section 7.4; typical hydrotest witness practice

**C-07: Record Package Compilation**

After all quality activities are complete, compile records into tank dossiers (one per tank). Organizing records during the project is easier than organizing after the fact.

**Key consideration:** Establish dossier structure and index early. As records are generated, file them in the appropriate dossier section. Prepare draft index progressively. Final dossier compilation becomes a review and quality check, not a major assembly effort.

**Source:** Typical as-built documentation compilation practice

**C-08: Electronic vs. Hard Copy Records**

Modern projects typically use electronic records (PDF dossiers, document management systems). However, some clients or regulatory authorities require hard copy records (bound books, binders).

**TBD** — Electronic and hard copy requirements per ER and project document management procedures

**Key consideration:** Verify archival format requirements early. If hard copy is required, plan for printing, binding, and indexing. If electronic, verify file format requirements (PDF/A for archival, searchable text, etc.).

**Source:** Typical document archival planning

---

## Trade-offs

### Competing Concerns to Evaluate

**T-01: NDE Extent: Spot vs. Full Examination**

**Trade-off:**
- **Spot examination (API 650 minimum):** Lower cost, faster schedule; meets code minimum; some risk that defects are missed between examined joints
- **Full examination (100% radiography):** Higher cost, longer schedule; maximum assurance; all weld defects are identified

**Recommendation:** Consider risk and client preference. For critical tanks (large capacity, seismic zone, environmental sensitivity), full examination may be justified. For lower-risk applications, spot examination per API 650 is acceptable.

**TBD** — NDE extent decision requires project risk assessment and client input

**Source:** API 650 Section 8.1; typical NDE extent selection

**T-02: Record Format: Electronic vs. Hard Copy**

**Trade-off:**
- **Electronic (PDF dossiers):** Easy to distribute, search, and archive; requires document management system; some clients/authorities may not accept electronic-only
- **Hard copy (bound books):** Tangible, durable, universally accepted; difficult to search and reproduce; storage space required

**Recommendation:** Hybrid approach — maintain electronic master with hard copy archive. Electronic for working use, hard copy for long-term archival and regulatory compliance.

**TBD** — Format requirements per ER

**Source:** Typical document archival practice

**T-03: Weld Map Detail: Summary vs. Comprehensive**

**Trade-off:**
- **Summary weld map:** Shows major welds only (shell seams, bottom-to-shell, roof-to-shell); simpler, easier to read
- **Comprehensive weld map:** Shows every weld including nozzles, attachments, structural welds; complete traceability but complex

**Recommendation:** Comprehensive weld map for quality records. All welds shown provide full traceability. Summary weld map can be extracted for operational use if needed.

**Source:** Typical weld map practice

**T-04: Record Review: Sampling vs. 100% Review**

**Trade-off:**
- **Sampling review:** QA reviews sample of MTRs, NDE reports; faster but may miss errors
- **100% review:** QA reviews every record; slower but ensures completeness and accuracy

**Recommendation:** 100% review for quality records. Records are permanent documentation — errors discovered later are costly to correct. Investment in thorough review during compilation is justified.

**Source:** Typical QA review practice

---

## Examples

### Reference Examples and Precedents

**Example 1: Material Certificate (MTR) Typical Content**

Typical MTR includes:
- **Mill identification:** Mill name, address, certification stamp
- **Material specification:** ASTM A36, ASTM A283 Grade C, etc.
- **Heat number:** Unique identifier for material lot (e.g., Heat #12345)
- **Product form:** Plate, 12mm thick, 2000mm × 6000mm
- **Chemical composition:** C, Mn, P, S, Si percentages (per heat analysis)
- **Mechanical properties (per heat):** Yield strength, tensile strength, elongation
- **Test results:** Test specimen location, test values, acceptance statement
- **Certification:** Mill certifier signature and date

**Source:** Typical mill test report format per ASTM standards

**Example 2: Weld Map Typical Layout**

Typical weld map shows:
- Tank elevation view (unrolled shell)
- Shell course boundaries (horizontal lines)
- Vertical seam locations (vertical lines)
- Weld joint identification numbers (W-101, W-102, W-103, etc.)
- Material heat numbers annotated on shell plates
- Table listing weld joints with WPS number, welder ID, weld date, NDE report number

**Source:** Typical API 650 tank weld map practice

**Example 3: NDE Report Typical Content**

Typical radiographic testing (RT) report includes:
- **Procedure:** RT procedure reference number
- **Weld joint:** Weld joint ID from weld map (e.g., W-101)
- **Technique:** X-ray or gamma-ray source, film type, exposure parameters
- **Acceptance criteria:** API 650 Section 8.2.2.2 or project specification reference
- **Film identification:** Film number and location markers
- **Interpretation:** Defects identified (porosity, slag, lack of fusion, cracks) with size and location
- **Disposition:** Accept or reject
- **Examiner:** Name, certification (ASNT Level II RT), signature, date

**Source:** Typical RT report format

**Example 4: Hydrostatic Test Record Typical Content**

Typical hydrotest record includes:
- **Tank identification:** Tank tag (TK-101)
- **Test parameters:** Test pressure (e.g., 7.5 m head = 73.5 kPa), test duration (24 hours)
- **Water source:** Municipal water supply (cross-reference to DEL-29.06)
- **Settlement measurements:**
  - Baseline (empty tank): Elevation at 8 foundation points
  - At test pressure (full tank): Elevation at same 8 points
  - After draining: Final elevation at same 8 points
  - Maximum differential settlement: 15mm (within API 650 limit of 300mm)
- **Visual inspection:** No leaks observed at any welds or nozzles; no visible distortion of shell or roof
- **Acceptance:** Tank passes API 650 Section 7.4 requirements
- **Signatures:** D&B Contractor QA inspector, Client witness inspector, date

**Source:** Typical API 650 hydrotest record format

**Example 5: Traceability Scenario**

**Scenario:** Shell plate material Heat #67890 is found to have incorrect chemical composition after fabrication (supplier certification error discovered during random audit).

**Traceability investigation:**
1. Review material certificates to identify all shipments with Heat #67890 (find 5 plates)
2. Review weld maps to identify where Heat #67890 plates were used (Tank TK-102, shell course 2, east quadrant)
3. Review NDE reports for affected welds (W-201 through W-205) to verify weld quality
4. Engineering evaluation: Chemical composition deviation assessed for impact on tank integrity
5. Decision: No impact on tank integrity (deviation within acceptable tolerance); document engineering evaluation in project file

**Lesson:** Traceability enables rapid identification of affected components when material issues are discovered. Without traceability, entire tank or all tanks may require investigation.

**Source:** Typical material traceability scenario

---

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|-------------|----------|----------|----------|-------------------|-------------------|--------------|
| CT-13.05-01 | NDE extent (spot vs. full examination) for shell welds | Trade-off T-01 | DEL-13.02 specification / ER (TBD) | Datasheet.md NDE Reports; Specification.md PR-02 | Project specification + ER | **TBD** |
| CT-13.05-02 | Record format (electronic vs. hard copy archival) | Trade-off T-02 | ER document management requirements (TBD) | Datasheet.md Documentation Context; Specification.md DR-03 | ER + project document procedures | **TBD** |
| CT-13.05-03 | Client witness hold points for hydrostatic testing | Consideration C-06 | ITP (DEL-29.02) / ER (TBD) | Specification.md PR-05; Procedure.md Step 6 | ITP + ER | **TBD** |
| CT-13.05-04 | Weld map development responsibility (D&B Contractor vs. fabricator) | Consideration C-03 | Contract scope split (TBD) | Datasheet.md Weld Maps; Procedure.md Step 3 | Contract documents | **TBD** |

**Note:** These conflicts represent quality documentation decisions requiring project specification and ER inputs. Resolution during WORKING_ITEMS will enable record collection planning.

---

**Document Status:** Pass 3 Complete — Enrichment complete. Design principles, considerations, trade-offs, and examples developed. Conflict Table added for quality documentation decisions requiring human ruling. Cross-document references verified. All TBDs marked. ASSUMPTIONs labeled. Ready for WORKING_ITEMS refinement.

**Last Updated:** 2026-01-28
