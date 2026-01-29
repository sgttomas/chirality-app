# Procedure: DEL-14.04 Process Piping Data Sheet Package

## Purpose

Procedure for creating line list and piping material data sheets for PKG-14 Process Piping (scope: Specification.md Scope; attributes: Datasheet.md Data Sheet Type; rationale: Guidance.md Purpose).

## Prerequisites

**Dependencies:** NOT_TRACKED (see `_DEPENDENCIES.md`)

**Inputs** (interface: Specification.md Interface Requirements; rationale: Guidance.md Principles item 3):
- P&IDs (DEL-14.01) — line numbers and services (interface: Specification.md IR-1; requirements: Specification.md FR-1, FR-3; construction: Datasheet.md Construction item 1 - Provides traceability; rationale: Guidance.md Principles items 1, 3; considerations: Guidance.md Considerations - Line List Development; verification: Specification.md Verification; examples: Guidance.md Examples items 1, 2; cross-reference DEL-14.01)
- Piping specification (DEL-14.02) — materials (interface: Specification.md IR-2; requirements: Specification.md FR-5, FR-6; construction: Datasheet.md Construction item 2 - Cross-reference; rationale: Guidance.md Principles items 2, 3; quality: Specification.md QR-2; considerations: Guidance.md Considerations - Coordination; verification: Specification.md Verification; examples: Guidance.md Examples item 3; cross-reference DEL-14.02)
- Design calculations (DEL-14.03) — sizes, design P/T (interface: Specification.md IR-3; performance: Specification.md PR-1; requirements: Specification.md FR-2; conditions: Datasheet.md Design pressure/temperature; rationale: Guidance.md Principles item 3; considerations: Guidance.md Considerations - Line List Development; verification: Specification.md Verification; cross-reference DEL-14.03)

**Tools:** Excel or database software for line list (attributes: Datasheet.md Line List Format; requirements: Specification.md QR-4; documentation: Specification.md Documentation - Format)

## Steps

### Step 1: Extract Line Numbers from P&IDs

**Objective:** Identify all piping lines from P&IDs (requirements: Specification.md FR-1; interface: Specification.md IR-1; rationale: Guidance.md Principles item 1; examples: Guidance.md Examples items 1, 2).

**Actions:**
1. Review all P&IDs (DEL-14.01) (interface: Specification.md IR-1; construction: Datasheet.md Construction item 1 - Provides traceability; rationale: Guidance.md Principles item 3; considerations: Guidance.md Considerations - Line List Development; cross-reference DEL-14.01)
2. Extract each unique line number (construction: Datasheet.md Construction item 1 - Typical columns; requirements: Specification.md FR-2; rationale: Guidance.md Principles item 1; examples: Guidance.md Examples item 1)
3. Record service description (e.g., "Canola Oil from Railcar Header to Tank T-101") (product: Datasheet.md Product/Service; construction: Datasheet.md Construction item 1 - Typical columns; requirements: Specification.md FR-2; procedure noted above; examples: Guidance.md Examples items 1, 2)
4. Record from/to equipment or locations (construction: Datasheet.md Construction item 1 - Typical columns; requirements: Specification.md FR-2; interface: Specification.md IR-4; procedure noted above; documentation: Specification.md Documentation - Line list columns; examples: Guidance.md Examples item 1)

**Outputs:**
- Draft line number list extracted from P&IDs (requirements: Specification.md FR-1; construction: Datasheet.md Construction item 1; verification: Specification.md Verification - Cross-check line list)

---

### Step 2: Populate Line List

**Objective:** Complete line list with all design data (requirements: Specification.md FR-2; construction: Datasheet.md Construction item 1; rationale: Guidance.md Principles item 1; considerations: Guidance.md Considerations - Line List Development; examples: Guidance.md Examples items 1, 2).

**Actions:**
1. For each line, populate:
   - Line Number (from P&IDs) (from Step 1; requirements: Specification.md FR-2; examples: Guidance.md Examples item 1)
   - Service Description (from Step 1; requirements: Specification.md FR-2; examples: Guidance.md Examples item 1)
   - From Equipment / To Equipment (from Step 1; requirements: Specification.md FR-2; interface: Specification.md IR-4; documentation: Specification.md Documentation - Line list columns; examples: Guidance.md Examples item 1)
   - Pipe Size (from DEL-14.03 calculations or P&IDs) (interface: Specification.md IR-3; requirements: Specification.md FR-2; construction: Datasheet.md Construction item 1 - Typical columns; rationale: Guidance.md Principles item 3; documentation: Specification.md Documentation - Line list columns; examples: Guidance.md Examples item 1; cross-reference DEL-14.03)
   - Material Class (assign based on service and pressure rating) (requirements: Specification.md FR-2, FR-4; rationale: Guidance.md Principles item 2; considerations: Guidance.md Considerations - Line List Development; from Step 3; documentation: Specification.md Documentation - Line list columns; examples: Guidance.md Examples item 1)
   - Design Pressure (from DEL-14.03 or process data) (conditions: Datasheet.md Design pressure/temperature; performance: Specification.md PR-1; interface: Specification.md IR-3; requirements: Specification.md FR-2; documentation: Specification.md Documentation - Line list columns; examples: Guidance.md Examples item 1; cross-reference DEL-14.03)
   - Design Temperature (from DEL-14.03 or process data) (conditions: Datasheet.md Design pressure/temperature; performance: Specification.md PR-1; interface: Specification.md IR-3; requirements: Specification.md FR-2; documentation: Specification.md Documentation - Line list columns; examples: Guidance.md Examples item 1; cross-reference DEL-14.03)
   - Insulation Required (Y/N based on temperature or personnel protection) (requirements: Specification.md FR-2; considerations: Guidance.md Considerations - Line List Development; documentation: Specification.md Documentation - Line list columns; examples: Guidance.md Examples item 1; cross-reference DEL-14.02)
   - Spec Reference (DEL-14.02) (requirements: Specification.md FR-3, FR-6; interface: Specification.md IR-2; rationale: Guidance.md Principles item 3; documentation: Specification.md Documentation - Line list columns; examples: Guidance.md Examples item 1; cross-reference DEL-14.02)
2. Verify completeness: All lines from P&IDs captured in line list (requirements: Specification.md FR-1; quality: Specification.md QR-1; interface: Specification.md IR-1; rationale: Guidance.md Principles item 1; verification: Specification.md Verification - Cross-check; verification table)

**Outputs:**
- Complete line list with all design data (construction: Datasheet.md Construction item 1; requirements: Specification.md FR-1, FR-2; documentation: Specification.md Documentation - Line list columns; records: Records section)

---

### Step 3: Define Material Classes

**Objective:** Establish material classes for piping systems (requirements: Specification.md FR-4; attributes: Datasheet.md Material Classes; construction: Datasheet.md Material Class Examples; rationale: Guidance.md Principles item 2; considerations: Guidance.md Considerations - Material Data Sheets; trade-offs: Guidance.md Trade-offs item 1).

**Actions:**
1. Group lines by service and pressure rating (requirements: Specification.md FR-4; rationale: Guidance.md Principles item 2; considerations: Guidance.md Considerations - Material Data Sheets; trade-offs: Guidance.md Trade-offs item 1)
2. Define material classes (e.g., CS-150, CS-300, SS-150) (attributes: Datasheet.md Material Classes; construction: Datasheet.md Material Class Examples; requirements: Specification.md FR-4; rationale: Guidance.md Principles item 2; considerations: Guidance.md Considerations - Material Data Sheets; examples: Guidance.md Examples item 3)
3. Typical classes:
   - CS-150: Carbon steel, Class 150, canola oil liquid service (construction: Datasheet.md Material Class Examples; performance: Specification.md PR-2; rationale: Guidance.md Principles item 2; considerations: Guidance.md Considerations - Material Data Sheets; examples: Guidance.md Examples item 3; cross-reference DEL-14.02)
   - CS-300: Carbon steel, Class 300, high-pressure services (construction: Datasheet.md Material Class Examples; requirements: Specification.md FR-4; trade-offs: Guidance.md Trade-offs item 1; examples: Guidance.md Examples item 3; cross-reference DEL-14.02, DEL-14.03)
   - SS-150: Stainless steel, Class 150, nitrogen or CIP service (construction: Datasheet.md Material Class Examples; requirements: Specification.md FR-4; rationale: Guidance.md Principles item 2; examples: Guidance.md Examples item 3; cross-reference DEL-14.02)

**Outputs:**
- Material class definitions (attributes: Datasheet.md Material Classes; requirements: Specification.md FR-4; used in Step 2, Step 4)

---

### Step 4: Create Material Data Sheets

**Objective:** Document material specifications for each material class (requirements: Specification.md FR-5, FR-6; construction: Datasheet.md Construction item 2; rationale: Guidance.md Principles item 2; considerations: Guidance.md Considerations - Material Data Sheets; examples: Guidance.md Examples item 3).

**Actions:**
1. For each material class, create data sheet specifying:
   - Pipe material and schedule (reference DEL-14.02) (construction: Datasheet.md Construction item 2 - Each class specifies; requirements: Specification.md FR-5; interface: Specification.md IR-2; rationale: Guidance.md Principles item 2; documentation: Specification.md Documentation - Material data sheets; examples: Guidance.md Examples item 3; cross-reference DEL-14.02)
   - Fitting material and type (requirements: Specification.md FR-5; interface: Specification.md IR-2; examples: Guidance.md Examples item 3; cross-reference DEL-14.02)
   - Flange material, type, and rating (construction: Datasheet.md Material Class Examples; requirements: Specification.md FR-5; interface: Specification.md IR-2; trade-offs: Guidance.md Trade-offs item 1; examples: Guidance.md Examples item 3; cross-reference DEL-14.02)
   - Gasket material and type (requirements: Specification.md FR-5; performance: Specification.md PR-2; interface: Specification.md IR-2; examples: Guidance.md Examples item 3; cross-reference DEL-14.02)
   - Bolting material (requirements: Specification.md FR-5; interface: Specification.md IR-2; examples: Guidance.md Examples item 3; cross-reference DEL-14.02)
2. Cross-reference DEL-14.02 for detailed specifications (requirements: Specification.md FR-6; interface: Specification.md IR-2; construction: Datasheet.md Construction item 2 - Cross-reference; quality: Specification.md QR-2; rationale: Guidance.md Principles item 3; considerations: Guidance.md Considerations - Coordination; documentation: Specification.md Documentation - Material data sheets; verification: Specification.md Verification; examples: Guidance.md Examples item 3)

**Outputs:**
- Material data sheets for all material classes (construction: Datasheet.md Construction item 2; requirements: Specification.md FR-4, FR-5; documentation: Specification.md Documentation - Material data sheets; records: Records section)

---

### Step 5: Independent Check

**Objective:** Verify line list and data sheets (quality: Specification.md QR-3; verification: Specification.md Verification).

**Actions:**
1. Cross-check line list vs. P&IDs (all lines captured) (requirements: Specification.md FR-1; quality: Specification.md QR-1; interface: Specification.md IR-1; verification: Specification.md Verification - Cross-check; verification table; cross-reference DEL-14.01)
2. Verify design P/T vs. DEL-14.03 calculations (performance: Specification.md PR-1; interface: Specification.md IR-3; verification: Specification.md Verification - Verify design P/T; verification table; cross-reference DEL-14.03)
3. Verify material classes vs. DEL-14.02 specification (requirements: Specification.md FR-6; quality: Specification.md QR-2; interface: Specification.md IR-2; verification: Specification.md Verification - Verify material classes; verification table; cross-reference DEL-14.02)
4. Checker sign-off (quality: Specification.md QR-3; verification: Specification.md Verification - Independent check sign-off; verification table)

**Verification:**
- All verifications complete per Specification.md Verification section (verification table)

---

### Step 6: Approval and Issuance

**Objective:** Issue line list and data sheets (attributes: Datasheet.md Revision Control; quality: Specification.md QR-4; documentation: Specification.md Documentation section).

**Actions:**
1. Discipline lead approval (quality: Specification.md QR-3; verification: Specification.md Verification - Acceptance)
2. Issue to `3_Issued/` with revision control (attributes: Datasheet.md Revision Control; documentation: Specification.md Documentation - Storage; records: Records section)
3. Distribute to design, procurement, fabrication, and construction teams (rationale: Guidance.md Principles item 1; considerations: Guidance.md Considerations - Coordination; documentation: Specification.md Documentation; records: Records section)

**Outputs:**
- Issued line list and material data sheets ready for use (verification: Specification.md Verification - Acceptance; records: Records section)

---

## Verification

**Verification activities summary:**

| Step | Verification Method | Acceptance Criteria |
|------|---------------------|---------------------|
| 1. Extract Line Numbers | Cross-check vs. P&IDs | All lines from P&IDs captured (requirements: Specification.md FR-1; quality: Specification.md QR-1) |
| 2. Populate Line List | Data verification | All columns complete and accurate (requirements: Specification.md FR-2; verification: Specification.md Verification) |
| 3. Define Material Classes | Review vs. DEL-14.02 | Classes align with specification (requirements: Specification.md FR-4; quality: Specification.md QR-2) |
| 4. Create Material Data Sheets | Cross-reference verification | Data sheets consistent with DEL-14.02 (requirements: Specification.md FR-5, FR-6; quality: Specification.md QR-2; verification: Specification.md Verification) |
| 5. Independent Check | Qualified engineer review | Checker sign-off (quality: Specification.md QR-3; verification: Specification.md Verification) |
| 6. Approval | Discipline lead approval | Package approved for issue (verification: Specification.md Verification - Acceptance) |

**Overall acceptance criteria** (verification: Specification.md Verification - Acceptance; verification table):
- Line list complete (all lines from P&IDs) (requirements: Specification.md FR-1; quality: Specification.md QR-1)
- Material data sheets accurate and consistent with DEL-14.02 (requirements: Specification.md FR-6; quality: Specification.md QR-2)
- Checked and approved (quality: Specification.md QR-3)

---

## Records

**Outputs** (scope: Specification.md Scope; construction: Datasheet.md Construction section; documentation: Specification.md Documentation section):
- Line list (Excel or database) (construction: Datasheet.md Construction item 1; requirements: Specification.md FR-1, FR-2; attributes: Datasheet.md Line List Format; Step 2 above)
- Piping material data sheets (PDF) (construction: Datasheet.md Construction item 2; requirements: Specification.md FR-4, FR-5; Step 4 above)

**Storage:** `2_Checking/` → `3_Issued/` (attributes: Datasheet.md Revision Control; documentation: Specification.md Documentation - Storage; Step 6 above)

**Format:** Excel or database for line list; PDF for data sheets (attributes: Datasheet.md Line List Format; documentation: Specification.md Documentation - Format)

**Distribution:**
- Design team (piping, structural, instrumentation) (considerations: Guidance.md Considerations - Coordination)
- Procurement team (material ordering) (rationale: Guidance.md Principles item 2)
- Fabrication and construction (installation reference) (rationale: Guidance.md Principles item 1)
