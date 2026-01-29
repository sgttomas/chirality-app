# Guidance: DEL-14.05 Process Piping Installation & Test Records

## Purpose

QA/QC records demonstrating ASME B31.3 compliance for process piping installation and testing in PKG-14 (scope: Specification.md Scope; attributes: Datasheet.md Record Type).

**Project context:** CSD canola oil transload facility, 1,000,000 MT/annum, Fraser Surrey Terminal BC (cross-reference DEL-14.01, DEL-14.02).

## Principles

**1. Material Traceability:**
- All pressure-containing materials (pipe, fittings, flanges, bolting) require Material Test Reports (MTRs) (construction: Datasheet.md Construction item 1; requirements: Specification.md FR-1, PR-1; quality standard: Datasheet.md Quality Standard; quality: Specification.md QR-1; considerations: below - Material Certificates; procedure: Procedure.md Step 1; verification: Specification.md Verification - Material certificates; documentation: Specification.md Documentation - Record types; examples: below item 1; cross-reference DEL-14.02, DEL-14.04)
- MTRs verify material grade, heat number, mechanical properties, chemical composition (construction: Datasheet.md Construction item 1; requirements: Specification.md PR-1; considerations: below - Material Certificates; procedure: Procedure.md Step 1; examples: below item 1)
- Traceability from procurement through installation critical for code compliance and future maintenance (construction: Datasheet.md Construction item 1 - Traceability; requirements: Specification.md FR-1; interface: Specification.md IR-1; quality: Specification.md QR-2; considerations: below - Material Certificates; procedure: Procedure.md Step 1)
- MTRs filed by heat number for easy retrieval (considerations: below - Material Certificates; procedure: Procedure.md Step 1; documentation: Specification.md Documentation - Storage)

**2. Weld Quality:**
- **Visual inspection:** All welds (100%) per ASME B31.3 Section 341 acceptance criteria (construction: Datasheet.md Construction item 2 - Visual inspection; requirements: Specification.md FR-2, PR-2; quality standard: Datasheet.md Quality Standard; standards: Specification.md Standards - ASME B31.3; considerations: below - Weld Inspection; procedure: Procedure.md Step 2; verification: Specification.md Verification - Weld inspection; examples: below item 2)
- **NDE (Non-Destructive Examination):** Extent depends on service class per ASME B31.3 Section 344 (construction: Datasheet.md Construction item 2 - NDE records; requirements: Specification.md FR-2, PR-2; quality standard: Datasheet.md Quality Standard; standards: Specification.md Standards - ASME B31.3; trade-offs: below item 2; procedure: Procedure.md Step 2; verification: Specification.md Verification - Weld inspection; examples: below item 2)
  - Normal fluid service: Spot NDE (e.g., 10-20% of welds) typical (trade-offs: below item 2; procedure: Procedure.md Step 2)
  - High-pressure or critical service: Higher NDE percentage or 100% (trade-offs: below item 2; procedure: Procedure.md Step 2; cross-reference DEL-14.03)
- **Acceptance criteria:** ASME B31.3 defines allowable defect sizes (cracks, porosity, undercut, etc.) (requirements: Specification.md PR-2; quality standard: Datasheet.md Quality Standard; standards: Specification.md Standards - ASME B31.3; considerations: below - Weld Inspection; procedure: Procedure.md Step 2; examples: below item 2)
- **Welder qualifications:** Welders must be qualified per ASME Section IX; Welding Procedure Specifications (WPS) must be qualified by Procedure Qualification Records (PQR) (construction: Datasheet.md Construction item 2 - Welder qualifications; requirements: Specification.md FR-2; standards: Specification.md Standards - ASME B31.3; considerations: below - Weld Inspection; procedure: Procedure.md Step 2; verification: Specification.md Verification - Weld inspection; documentation: Specification.md Documentation - Record types; cross-reference DEL-14.02)

**3. Hydrostatic Testing:**
- Pressure test to verify piping integrity before commissioning (construction: Datasheet.md Construction item 3; requirements: Specification.md FR-3, PR-3; quality standard: Datasheet.md Quality Standard; interface: Specification.md IR-2; rationale: above item 4 below; considerations: below - Hydrostatic Testing; procedure: Procedure.md Step 3; verification: Specification.md Verification - Hydrostatic test; examples: below item 3)
- **Test pressure:** 1.5 × design pressure (ASME B31.3 default); may be higher or lower per code rules or project requirements (construction: Datasheet.md Construction item 3 - Test pressure; requirements: Specification.md PR-3; quality standard: Datasheet.md Quality Standard; standards: Specification.md Standards - ASME B31.3; considerations: below - Hydrostatic Testing; procedure: Procedure.md Step 3; examples: below item 3; cross-reference DEL-14.03, DEL-14.04)
- **Duration:** 10 minutes minimum at test pressure (construction: Datasheet.md Construction item 3 - duration; requirements: Specification.md PR-3; quality standard: Datasheet.md Quality Standard; considerations: below - Hydrostatic Testing; procedure: Procedure.md Step 3; examples: below item 3)
- **Acceptance:** No leaks, no visible distortion (requirements: Specification.md PR-3; considerations: below - Hydrostatic Testing; procedure: Procedure.md Step 3; verification: Specification.md Verification - Acceptance; examples: below item 3)
- **Timing:** Performed after installation complete, before insulation applied (so leaks can be observed) (considerations: below - Hydrostatic Testing; trade-offs: below item 3; procedure: Procedure.md Step 3; cross-reference DEL-14.02)

**4. Record Organization:**
- Records typically organized by piping system or deliverable line list (DEL-14.04) (construction: Datasheet.md Construction items; interface: Specification.md IR-1; rationale: above; considerations: below - Material Certificates; procedure: Procedure.md Step 4; cross-reference DEL-14.04)
- Ensures completeness (all lines documented, no gaps) (requirements: Specification.md FR-1, FR-2, FR-3; quality: Specification.md QR-1; rationale: above; procedure: Procedure.md Step 4; verification: Specification.md Verification - Acceptance)
- Facilitates turnover to operations and maintenance (requirements: Specification.md FR-4; interface: Specification.md IR-2; rationale: above; procedure: Procedure.md Step 5; cross-reference PKG-33, PKG-34)

## Considerations

**Material Certificates:**
- Collected during procurement phase (requirements: Specification.md FR-1; rationale: above item 1; procedure: Procedure.md Prerequisites, Step 1; cross-reference DEL-14.02, DEL-14.04)
- Supplier provides MTRs with material shipment (construction: Datasheet.md Construction item 1; rationale: above item 1; procedure: Procedure.md Step 1)
- QA/QC reviews MTRs for specification compliance before accepting material (performance: Specification.md PR-1; interface: Specification.md IR-1; quality: Specification.md QR-1; rationale: above item 1; procedure: Procedure.md Step 1; verification: Specification.md Verification - Material certificates; cross-reference DEL-14.02, DEL-14.04)

**Weld Inspection:**
- Performed during fabrication/installation by qualified inspectors (construction: Datasheet.md Construction item 2; requirements: Specification.md FR-2; quality: Specification.md QR-1; rationale: above item 2; procedure: Procedure.md Step 2; examples: below item 2)
- Weld maps created showing each weld location and number (construction: Datasheet.md Construction item 2 - Weld maps; requirements: Specification.md FR-2; rationale: above item 2; procedure: Procedure.md Step 2; documentation: Specification.md Documentation - Record types; examples: below item 2; cross-reference DEL-14.01)
- Failed welds repaired and re-inspected (performance: Specification.md PR-2; quality standard: Datasheet.md Quality Standard; rationale: above item 2; procedure: Procedure.md Step 2; examples: below item 2)

**Hydrostatic Testing:**
- Requires system isolation (blind flanges or closed valves) (construction: Datasheet.md Construction item 3 - System boundaries; requirements: Specification.md FR-3; rationale: above item 3; procedure: Procedure.md Step 3; examples: below item 3; cross-reference DEL-14.01)
- Water typically used as test fluid (unless incompatible with product or freezing risk) (requirements: Specification.md PR-3; rationale: above item 3; considerations: above; trade-offs: below item 3; procedure: Procedure.md Step 3; examples: below item 3)
- Test pressure monitored continuously during test duration (requirements: Specification.md PR-3; rationale: above item 3; procedure: Procedure.md Step 3; examples: below item 3)
- After test, water drained and system dried (especially for food-grade service like canola oil) (requirements: Specification.md FR-3; rationale: above item 3; considerations: above; procedure: Procedure.md Step 3; cross-reference DEL-14.02)

**Regulatory Compliance:**
- Records may be required for facility operating permits (requirements: Specification.md FR-4, QR-3; rationale: above item 4; quality: Specification.md QR-2; procedure: Procedure.md Step 5)
- Regulatory authorities (Transport Canada, local jurisdiction) may audit records (requirements: Specification.md QR-3; quality: Specification.md QR-2; procedure: Procedure.md Step 5)
- Permanent retention recommended (attributes: Datasheet.md Retention Period; quality: Specification.md QR-2; rationale: above item 4; documentation: Specification.md Documentation - Retention)

## Trade-offs

**1. Record Detail Level:**
- Minimal records (MTRs, test certs only): Fast, meets minimum code requirements (requirements: Specification.md FR-1, FR-3; quality standard: Datasheet.md Quality Standard)
- Comprehensive records (detailed inspection logs, photos, intermediate tests): Thorough, but higher effort and storage needs (requirements: Specification.md FR-1, FR-2, FR-3; quality: Specification.md QR-1)
- **Guidance:** Minimum ASME B31.3 requirements plus project-specific additions; avoid unnecessary detail (quality: Specification.md QR-1; rationale: above items 1-4; procedure: Procedure.md Steps 1-3)

**2. NDE Extent:**
- Minimum code (spot NDE): Lower cost, faster (construction: Datasheet.md Construction item 2 - NDE; performance: Specification.md PR-2; rationale: above item 2; procedure: Procedure.md Step 2)
- 100% NDE: Maximum confidence, higher cost and schedule impact (performance: Specification.md PR-2; rationale: above item 2; procedure: Procedure.md Step 2)
- **Guidance:** Risk-based approach; critical lines warrant higher NDE percentage (requirements: Specification.md FR-2; performance: Specification.md PR-2; rationale: above item 2; procedure: Procedure.md Step 2; cross-reference DEL-14.03)

**3. Hydrostatic Test Sequencing:**
- Test early (during construction): Identifies issues early, but may require re-testing after later work (requirements: Specification.md FR-3; rationale: above item 3; considerations: above - Hydrostatic Testing; procedure: Procedure.md Step 3)
- Test late (near completion): Single test, but delays issue discovery (requirements: Specification.md FR-3; considerations: above - Hydrostatic Testing; procedure: Procedure.md Step 3)
- **Guidance:** Test in phases aligned with construction progress; balance early issue detection vs. re-test risk (requirements: Specification.md FR-3, FR-4; rationale: above item 3; procedure: Procedure.md Step 3; cross-reference PKG-33, PKG-34)

## Examples

**1. Material certificate (MTR) example:**
- Heat Number: A12345 (construction: Datasheet.md Construction item 1; requirements: Specification.md FR-1; rationale: above item 1; procedure: Procedure.md Step 1)
- Material: ASTM A106 Gr. B Seamless Pipe (construction: Datasheet.md Construction item 1; interface: Specification.md IR-1; procedure: Procedure.md Step 1; cross-reference DEL-14.02, DEL-14.04)
- Size: 8" NPS Schedule 40 (interface: Specification.md IR-1; procedure: Procedure.md Step 1; cross-reference DEL-14.04)
- Mechanical Properties: Tensile strength, yield strength, elongation (requirements: Specification.md PR-1; procedure: Procedure.md Step 1)
- Chemical Composition: C, Mn, P, S, Si (requirements: Specification.md PR-1; procedure: Procedure.md Step 1)
- Supplier Certification: Signed and stamped (quality: Specification.md QR-1; procedure: Procedure.md Step 1; verification: Specification.md Verification - Material certificates)

**2. Weld inspection record example:**
- Weld Number: W-2014-035 (construction: Datasheet.md Construction item 2; requirements: Specification.md FR-2; procedure: Procedure.md Step 2)
- Line Number: 8"-CO-201 (interface: Specification.md IR-1; procedure: Procedure.md Step 2; cross-reference DEL-14.01, DEL-14.04)
- Welder ID: WLD-007 (qualified per ASME Section IX) (construction: Datasheet.md Construction item 2 - Welder qualifications; requirements: Specification.md FR-2; rationale: above item 2; procedure: Procedure.md Step 2)
- WPS: WPS-CS-GTAW-01 (Welding Procedure Specification) (construction: Datasheet.md Construction item 2; rationale: above item 2; procedure: Procedure.md Step 2; cross-reference DEL-14.02)
- Visual Inspection: PASS (per ASME B31.3 Section 341) (construction: Datasheet.md Construction item 2 - Visual inspection; performance: Specification.md PR-2; quality standard: Datasheet.md Quality Standard; standards: Specification.md Standards - ASME B31.3; procedure: Procedure.md Step 2; verification: Specification.md Verification - Weld inspection)
- NDE Method: Radiography (RT) (construction: Datasheet.md Construction item 2 - NDE; performance: Specification.md PR-2; procedure: Procedure.md Step 2; documentation: Specification.md Documentation - Record types)
- NDE Result: PASS (per ASME B31.3 acceptance criteria) (performance: Specification.md PR-2; rationale: above item 2; procedure: Procedure.md Step 2; verification: Specification.md Verification - Weld inspection)
- Inspector Sign-off: [Name, Date] (quality: Specification.md QR-1; procedure: Procedure.md Step 2; verification: Specification.md Verification - Weld inspection)

**3. Hydrostatic test certificate example:**
- Test ID: HT-PKG14-001 (construction: Datasheet.md Construction item 3; requirements: Specification.md FR-3; procedure: Procedure.md Step 3)
- System: Railcar Unloading Header (Railcar Stations 1-10 to Tank T-101) (construction: Datasheet.md Construction item 3 - System boundaries; procedure: Procedure.md Step 3; cross-reference DEL-14.01, DEL-14.04)
- Design Pressure: 1,035 kPa (150 psi) (performance: Specification.md PR-3; procedure: Procedure.md Step 3; cross-reference DEL-14.03, DEL-14.04)
- Test Pressure: 1,550 kPa (225 psi = 1.5 × design pressure) (construction: Datasheet.md Construction item 3 - Test pressure; requirements: Specification.md PR-3; quality standard: Datasheet.md Quality Standard; rationale: above item 3; procedure: Procedure.md Step 3; examples: above item 3)
- Test Fluid: Water (considerations: above - Hydrostatic Testing; trade-offs: below item 3; procedure: Procedure.md Step 3)
- Test Duration: 15 minutes (minimum 10 min per ASME B31.3) (construction: Datasheet.md Construction item 3 - duration; requirements: Specification.md PR-3; quality standard: Datasheet.md Quality Standard; rationale: above item 3; procedure: Procedure.md Step 3)
- Test Result: PASS — No leaks, no visible distortion (requirements: Specification.md PR-3; rationale: above item 3; procedure: Procedure.md Step 3; verification: Specification.md Verification - Acceptance)
- QA/QC Witness: [Name, Date, Signature] (quality: Specification.md QR-1; procedure: Procedure.md Step 3; verification: Specification.md Verification - Hydrostatic test)
