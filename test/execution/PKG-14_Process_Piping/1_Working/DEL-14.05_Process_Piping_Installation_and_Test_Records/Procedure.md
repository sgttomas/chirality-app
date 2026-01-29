# Procedure: DEL-14.05 Process Piping Installation & Test Records

## Purpose

Procedure for collecting, verifying, and archiving QA/QC records for PKG-14 process piping per ASME B31.3 (scope: Specification.md Scope; attributes: Datasheet.md Record Type; rationale: Guidance.md Purpose).

## Prerequisites

**Dependencies:** NOT_TRACKED (see `_DEPENDENCIES.md`)

**Inputs** (interface: Specification.md Interface Requirements; rationale: Guidance.md Principles item 4; procedure noted below):
- Material certificates from suppliers (construction: Datasheet.md Construction item 1; requirements: Specification.md FR-1; interface: Specification.md IR-1; rationale: Guidance.md Principles item 1; considerations: Guidance.md Considerations - Material Certificates; Step 1 below)
- Weld inspection records from QC inspectors (construction: Datasheet.md Construction item 2; requirements: Specification.md FR-2; rationale: Guidance.md Principles item 2; considerations: Guidance.md Considerations - Weld Inspection; Step 2 below)
- Hydrostatic test results from field testing (construction: Datasheet.md Construction item 3; requirements: Specification.md FR-3; rationale: Guidance.md Principles item 3; considerations: Guidance.md Considerations - Hydrostatic Testing; Step 3 below)

**Reference:** ASME B31.3 Chapter VI, Project Quality Management Plan **TBD** (quality standard: Datasheet.md Quality Standard; requirements: Specification.md Standards section; rationale: Guidance.md Principles items 2, 3; cross-reference DEL-14.02)

## Steps

### Step 1: Material Certificates (MTRs)

**Objective:** Collect and verify material certificates for all pressure-containing components (construction: Datasheet.md Construction item 1; requirements: Specification.md FR-1, PR-1; rationale: Guidance.md Principles item 1; examples: Guidance.md Examples item 1).

**Actions:**
1. Collect MTRs from suppliers for all pressure-containing materials (construction: Datasheet.md Construction item 1; requirements: Specification.md FR-1; rationale: Guidance.md Principles item 1; considerations: Guidance.md Considerations - Material Certificates; examples: Guidance.md Examples item 1; cross-reference DEL-14.02, DEL-14.04)
2. Verify MTRs match purchase order and DEL-14.04 (material data sheets) (interface: Specification.md IR-1; performance: Specification.md PR-1; rationale: Guidance.md Principles item 1; quality: Specification.md QR-1; considerations: Guidance.md Considerations - Material Certificates; verification: Specification.md Verification - Material certificates; examples: Guidance.md Examples item 1; cross-reference DEL-14.04)
3. File MTRs by heat number and material type (construction: Datasheet.md Construction item 1 - Traceability; rationale: Guidance.md Principles item 1; considerations: Guidance.md Considerations - Material Certificates; quality: Specification.md QR-2; documentation: Specification.md Documentation - Storage)
4. QA/QC review and approval (quality: Specification.md QR-1; rationale: Guidance.md Principles item 1; verification: Specification.md Verification - Material certificates; verification table)

**Outputs:**
- Material certificate file organized by heat number (construction: Datasheet.md Construction item 1; requirements: Specification.md FR-1; documentation: Specification.md Documentation - Record types; records: Records section)

---

### Step 2: Weld Inspection Records

**Objective:** Document weld quality verification per ASME B31.3 (construction: Datasheet.md Construction item 2; requirements: Specification.md FR-2, PR-2; quality standard: Datasheet.md Quality Standard; rationale: Guidance.md Principles item 2; examples: Guidance.md Examples item 2).

**Actions:**
1. Visual inspection of all welds (100%) by qualified inspector (construction: Datasheet.md Construction item 2 - Visual inspection; requirements: Specification.md FR-2, PR-2; quality standard: Datasheet.md Quality Standard; standards: Specification.md Standards - ASME B31.3; rationale: Guidance.md Principles item 2; considerations: Guidance.md Considerations - Weld Inspection; verification: Specification.md Verification - Weld inspection; examples: Guidance.md Examples item 2)
2. NDE per ASME B31.3 requirements (radiography, ultrasonic, etc.) (construction: Datasheet.md Construction item 2 - NDE records; requirements: Specification.md FR-2, PR-2; quality standard: Datasheet.md Quality Standard; standards: Specification.md Standards - ASME B31.3; rationale: Guidance.md Principles item 2; considerations: Guidance.md Considerations - Weld Inspection; trade-offs: Guidance.md Trade-offs item 2; verification: Specification.md Verification - Weld inspection; documentation: Specification.md Documentation - Record types; examples: Guidance.md Examples item 2)
3. Record weld number, location, welder ID, inspection results (construction: Datasheet.md Construction item 2; requirements: Specification.md FR-2; rationale: Guidance.md Principles item 2; considerations: Guidance.md Considerations - Weld Inspection; examples: Guidance.md Examples item 2; cross-reference DEL-14.01)
4. File weld maps and inspection reports (construction: Datasheet.md Construction item 2 - Weld maps; requirements: Specification.md FR-2; rationale: Guidance.md Principles item 2; considerations: Guidance.md Considerations - Weld Inspection; quality: Specification.md QR-2; documentation: Specification.md Documentation - Record types; examples: Guidance.md Examples item 2)
5. Repair/re-inspection if welds fail acceptance criteria (performance: Specification.md PR-2; rationale: Guidance.md Principles item 2; considerations: Guidance.md Considerations - Weld Inspection; verification: Specification.md Verification - Weld inspection; examples: Guidance.md Considerations - Failed welds)

**Outputs:**
- Weld inspection file with all weld records (construction: Datasheet.md Construction item 2; requirements: Specification.md FR-2; documentation: Specification.md Documentation - Record types; records: Records section)

---

### Step 3: Hydrostatic Testing

**Objective:** Verify piping pressure integrity per ASME B31.3 (construction: Datasheet.md Construction item 3; requirements: Specification.md FR-3, PR-3; quality standard: Datasheet.md Quality Standard; rationale: Guidance.md Principles item 3; examples: Guidance.md Examples item 3).

**Actions:**
1. Isolate piping system for testing (install blind flanges or valves) (construction: Datasheet.md Construction item 3 - System boundaries; requirements: Specification.md FR-3; considerations: Guidance.md Considerations - Hydrostatic Testing; examples: Guidance.md Examples item 3; cross-reference DEL-14.01)
2. Fill system with water (or other suitable test fluid) (requirements: Specification.md PR-3; considerations: Guidance.md Considerations - Hydrostatic Testing; trade-offs: Guidance.md Trade-offs item 3; examples: Guidance.md Examples item 3 - Test Fluid)
3. Pressurize to 1.5 × design pressure (construction: Datasheet.md Construction item 3 - Test pressure; requirements: Specification.md PR-3; quality standard: Datasheet.md Quality Standard; rationale: Guidance.md Principles item 3; standards: Specification.md Standards - ASME B31.3; considerations: Guidance.md Considerations - Hydrostatic Testing; examples: Guidance.md Examples item 3; cross-reference DEL-14.03, DEL-14.04)
4. Hold pressure for 10 minutes minimum (construction: Datasheet.md Construction item 3 - duration; requirements: Specification.md PR-3; quality standard: Datasheet.md Quality Standard; rationale: Guidance.md Principles item 3; considerations: Guidance.md Considerations - Hydrostatic Testing; examples: Guidance.md Examples item 3)
5. Inspect for leaks or deformation (requirements: Specification.md PR-3; rationale: Guidance.md Principles item 3; considerations: Guidance.md Considerations - Hydrostatic Testing; verification: Specification.md Verification - Acceptance; examples: Guidance.md Examples item 3 - Test Result)
6. Document test pressure, duration, results (construction: Datasheet.md Construction item 3 - Test certificate; requirements: Specification.md FR-3; considerations: Guidance.md Considerations - Hydrostatic Testing; documentation: Specification.md Documentation - Record types; examples: Guidance.md Examples item 3)
7. QA/QC witness and sign test certificate (quality: Specification.md QR-1; rationale: Guidance.md Principles item 3; verification: Specification.md Verification - Hydrostatic test; examples: Guidance.md Examples item 3 - QA/QC Witness)

**Outputs:**
- Hydrostatic test certificates for all piping systems (construction: Datasheet.md Construction item 3; requirements: Specification.md FR-3; documentation: Specification.md Documentation - Record types; records: Records section)

---

### Step 4: Compilation and Review

**Objective:** Compile complete record package and verify completeness (requirements: Specification.md FR-4; quality: Specification.md QR-1; rationale: Guidance.md Principles item 4; procedure noted above).

**Actions:**
1. Compile all records for each piping system (construction: Datasheet.md Construction items 1-3; requirements: Specification.md FR-1, FR-2, FR-3; rationale: Guidance.md Principles item 4; quality: Specification.md QR-2; documentation: Specification.md Documentation - Record types)
2. Cross-check against DEL-14.04 (line list) — all lines documented (interface: Specification.md IR-1; rationale: Guidance.md Principles item 4; quality: Specification.md QR-1; verification: Specification.md Verification - Acceptance; verification table; cross-reference DEL-14.04)
3. QA/QC review for completeness and compliance (quality: Specification.md QR-1; rationale: Guidance.md Principles items 1, 2, 3; trade-offs: Guidance.md Trade-offs item 1; verification: Specification.md Verification - Acceptance)
4. Prepare final acceptance package (requirements: Specification.md FR-4; quality: Specification.md QR-1; documentation: Specification.md Documentation - Record types; verification table)

**Outputs:**
- Complete QA/QC record package for PKG-14 process piping (requirements: Specification.md FR-4; documentation: Specification.md Documentation section; records: Records section)

---

### Step 5: Archiving

**Objective:** Archive records permanently per contract and regulatory requirements (attributes: Datasheet.md Retention Period; quality: Specification.md QR-2, QR-3; considerations: Guidance.md Considerations - Regulatory Compliance; documentation: Specification.md Documentation - Storage, Retention).

**Actions:**
1. File records in project archive (attributes: Datasheet.md Retention Period; quality: Specification.md QR-2; considerations: Guidance.md Considerations - Regulatory Compliance; documentation: Specification.md Documentation - Storage; records: Records section)
2. Deliver copy to Employer per contract requirements **TBD** (requirements: Specification.md FR-4; interface: Specification.md IR-2; quality: Specification.md QR-3; considerations: Guidance.md Considerations - Regulatory Compliance; documentation: Specification.md Documentation - Retention; records: Records section)
3. Retain permanently (facility life + regulatory period) (attributes: Datasheet.md Retention Period; quality: Specification.md QR-2; considerations: Guidance.md Considerations - Regulatory Compliance; documentation: Specification.md Documentation - Retention; records: Records section)

**Outputs:**
- Archived QA/QC records available for facility operations, maintenance, and regulatory compliance (requirements: Specification.md FR-4; interface: Specification.md IR-2; rationale: Guidance.md Principles item 4; quality: Specification.md QR-2; cross-reference PKG-33, PKG-34)

---

## Verification

**Verification activities summary:**

| Step | Verification Method | Acceptance Criteria |
|------|---------------------|---------------------|
| 1. Material Certificates | QA/QC review of MTRs | All materials have MTRs matching specifications (requirements: Specification.md FR-1, PR-1; verification: Specification.md Verification - Material certificates) |
| 2. Weld Inspection | Visual + NDE per ASME B31.3 | All welds inspected and accepted; inspector sign-off (requirements: Specification.md FR-2, PR-2; verification: Specification.md Verification - Weld inspection) |
| 3. Hydrostatic Testing | Witnessed pressure test | Test pressure 1.5×design, duration ≥10 min, no leaks; QA/QC sign-off (requirements: Specification.md FR-3, PR-3; verification: Specification.md Verification - Hydrostatic test, Acceptance) |
| 4. Compilation and Review | Completeness check vs. line list | All systems documented; QA/QC approval (requirements: Specification.md FR-4; verification: Specification.md Verification - Acceptance) |
| 5. Archiving | Permanent filing | Records archived and delivered to Employer (quality: Specification.md QR-2, QR-3; verification: Specification.md Verification - Acceptance) |

**Overall acceptance criteria** (verification: Specification.md Verification - Acceptance; verification table):
- All materials have MTRs (100% coverage) (requirements: Specification.md FR-1; quality: Specification.md QR-1; rationale: Guidance.md Principles item 1)
- All welds inspected and accepted per ASME B31.3 (requirements: Specification.md FR-2, PR-2; quality standard: Datasheet.md Quality Standard; rationale: Guidance.md Principles item 2)
- All piping systems hydrostatically tested and passed (requirements: Specification.md FR-3, PR-3; quality standard: Datasheet.md Quality Standard; rationale: Guidance.md Principles item 3)
- Complete record package approved for commissioning (requirements: Specification.md FR-4; quality: Specification.md QR-1; interface: Specification.md IR-2; cross-reference PKG-33, PKG-34)

---

## Records

**Outputs** (construction: Datasheet.md Construction section; scope: Specification.md Scope; documentation: Specification.md Documentation section):
- Material Test Reports (MTRs) for all pressure-containing materials (construction: Datasheet.md Construction item 1; requirements: Specification.md FR-1; documentation: Specification.md Documentation - Record types; Step 1 above; examples: Guidance.md Examples item 1)
- Weld inspection records (visual and NDE) (construction: Datasheet.md Construction item 2; requirements: Specification.md FR-2; documentation: Specification.md Documentation - Record types; Step 2 above; examples: Guidance.md Examples item 2)
- Hydrostatic test certificates (construction: Datasheet.md Construction item 3; requirements: Specification.md FR-3; documentation: Specification.md Documentation - Record types; Step 3 above; examples: Guidance.md Examples item 3)
- Final acceptance certificate (requirements: Specification.md FR-4; quality: Specification.md QR-1; documentation: Specification.md Documentation - Record types; Step 4 above)

**Storage:** `3_Issued/` → Project archive (attributes: Datasheet.md Retention Period; quality: Specification.md QR-2; documentation: Specification.md Documentation - Storage; Step 5 above)

**Format:**
- PDF for issued records (quality: Specification.md QR-4; documentation: Specification.md Documentation section)
- Organized by piping system or line list (DEL-14.04) (interface: Specification.md IR-1; rationale: Guidance.md Principles item 4; quality: Specification.md QR-2; Step 4 above; cross-reference DEL-14.04)

**Retention:** Permanent (facility life + regulatory period) (attributes: Datasheet.md Retention Period; quality: Specification.md QR-2; considerations: Guidance.md Considerations - Regulatory Compliance; documentation: Specification.md Documentation - Retention; Step 5 above)

**Distribution:**
- Project archive (permanent retention) (Step 5 above)
- Employer (per contract requirements) (requirements: Specification.md FR-4; interface: Specification.md IR-2; quality: Specification.md QR-3; Step 5 above)
- Commissioning team (for system turnover) (interface: Specification.md IR-2; rationale: Guidance.md Principles item 4; Step 5 above; cross-reference PKG-33, PKG-34)
