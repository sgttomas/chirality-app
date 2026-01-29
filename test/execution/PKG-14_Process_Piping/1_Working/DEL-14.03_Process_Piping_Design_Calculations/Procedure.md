# Procedure: DEL-14.03 Process Piping Design Calculations

## Purpose

Procedure for producing pipe sizing, stress analysis, and flexibility analysis calculations for PKG-14 Process Piping per ASME B31.3 (scope: Specification.md Scope; attributes: Datasheet.md Calculation Type; rationale: Guidance.md Purpose).

## Prerequisites

**Dependencies:** NOT_TRACKED (coordinated externally; see `_DEPENDENCIES.md`)

**Inputs** (interface: Specification.md Interface Requirements; rationale: Guidance.md Considerations sections):
- Piping geometry (DEL-14.01 drawings) (interface: Specification.md IR-1; construction: Datasheet.md Construction items 2, 3 - Inputs; rationale: Guidance.md Principles item 2; examples: Guidance.md Examples - Typical stress analysis; cross-reference DEL-14.01)
- Material properties (DEL-14.02 specification) (interface: Specification.md IR-2; construction: Datasheet.md Construction items 2, 3 - Inputs; conditions: Datasheet.md Design Conditions; rationale: Guidance.md Principles item 2; cross-reference DEL-14.02)
- Design conditions (DEL-14.04 data sheets) (interface: Specification.md IR-3; requirements: Specification.md FR-1, PR-4; conditions: Datasheet.md Design Conditions; rationale: Guidance.md Principles item 1; considerations: Guidance.md Considerations - Pipe Sizing; cross-reference DEL-14.04)
- Process flow rates, temperatures, pressures **TBD** (interface: Specification.md IR-3; requirements: Specification.md PR-4, PR-5; conditions: Datasheet.md Design Conditions; rationale: Guidance.md Principles item 1; examples: Guidance.md Examples - Typical pipe sizing)
- Seismic/wind criteria **TBD** (NBC 2020 assumed) (requirements: Specification.md PR-7; conditions: Datasheet.md Seismic criteria; rationale: Guidance.md Principles item 4; standards: Specification.md Standards - NBC 2020; considerations: Guidance.md Considerations - Stress Analysis; cross-reference DEL-14.01, DEL-14.02)

**Tools** (attributes: Datasheet.md Software/Tools; requirements: Specification.md PR-2, QR-2; considerations: Guidance.md Considerations - Stress Analysis):
- CAESAR II, AutoPIPE, or equivalent (stress/flexibility) (construction: Datasheet.md Construction items 2, 3 - Software; requirements: Specification.md PR-2; standards: Specification.md Standards - Software; rationale: Guidance.md Principles item 2; examples: Guidance.md Examples - Typical stress analysis)
- Excel, MathCAD, or equivalent (hydraulic sizing) (construction: Datasheet.md Construction item 1; requirements: Specification.md PR-1, PR-3; standards: Specification.md Standards - Darcy-Weisbach; examples: Guidance.md Examples - Typical pipe sizing)
- ASME B31.3 code text (code: Datasheet.md Design Code; requirements: Specification.md FR-5, FR-8, PR-5, PR-6; standards: Specification.md Standards - ASME B31.3; rationale: Guidance.md Principles items 2, 3, 4; cross-reference DEL-14.01, DEL-14.02)

**Personnel** (quality: Specification.md QR-1):
- Piping engineer (P.Eng. or equivalent) (quality: Specification.md QR-1; rationale: Guidance.md Principles items 1, 2, 3)
- Independent checker (qualified piping engineer) (quality: Specification.md QR-1; verification: Specification.md Verification - Calculation check; verification table: Step 4)

## Steps

### Step 1: Pipe Sizing Calculations

**Objective:** Determine pipe diameters for all process piping lines (construction: Datasheet.md Construction item 1; requirements: Specification.md FR-1, FR-2, FR-3; rationale: Guidance.md Principles item 1; examples: Guidance.md Examples - Typical pipe sizing).

**Actions:**
1. Collect flow rates and product properties (density, viscosity) for each line (interface: Specification.md IR-3; requirements: Specification.md PR-4; conditions: Datasheet.md Flow rates, Product properties; rationale: Guidance.md Principles item 1; considerations: Guidance.md Considerations - Pipe Sizing; examples: Guidance.md Examples - Typical pipe sizing input)
2. Apply Darcy-Weisbach method to calculate pressure drop vs. pipe diameter (construction: Datasheet.md Construction item 1 - Methodology; requirements: Specification.md PR-1; standards: Specification.md Standards - Darcy-Weisbach; rationale: Guidance.md Principles item 1; examples: Guidance.md Examples - Typical pipe sizing method)
3. Select pipe sizes balancing velocity limits (1.5-3.0 m/s typical) and pressure drop budget (requirements: Specification.md FR-2, FR-3; rationale: Guidance.md Principles item 1; considerations: Guidance.md Considerations - Pipe Sizing; trade-offs: Guidance.md Trade-offs item 1; verification: Specification.md Verification - Acceptance criteria)
4. Document: Line ID, flow rate, product, diameter, velocity, pressure drop (construction: Datasheet.md Construction item 1 - Outputs; requirements: Specification.md FR-1, FR-2; documentation: Specification.md Documentation)
5. Check: Independent verification of calculations (quality: Specification.md QR-1; verification: Specification.md Verification - Calculation check; verification table)

**Outputs:**
- Pipe sizing calculation package (construction: Datasheet.md Construction item 1; requirements: Specification.md FR-1; documentation: Specification.md Documentation; records: Records section)
- Recommended pipe sizes for all lines (construction: Datasheet.md Construction item 1 - Outputs; requirements: Specification.md FR-1; cross-reference DEL-14.01, DEL-14.02, DEL-14.04)

---

### Step 2: Stress Analysis

**Objective:** Verify piping and supports comply with ASME B31.3 stress limits (construction: Datasheet.md Construction item 2; requirements: Specification.md FR-5, FR-6, FR-7; rationale: Guidance.md Principles items 2, 4; examples: Guidance.md Examples - Typical stress analysis).

**Actions:**
1. Build piping model (CAESAR II/AutoPIPE): geometry from drawings, materials from specification (attributes: Datasheet.md Software/Tools; construction: Datasheet.md Construction item 2 - Software; requirements: Specification.md PR-2; standards: Specification.md Standards - Software; interface: Specification.md IR-1, IR-2; quality: Specification.md QR-2; rationale: Guidance.md Principles item 2; examples: Guidance.md Examples - Typical stress analysis)
2. Apply loads: pressure, weight, temperature, seismic (NBC 2020), wind (construction: Datasheet.md Construction item 2 - Inputs; requirements: Specification.md PR-5, PR-6, PR-7; conditions: Datasheet.md Design Conditions; rationale: Guidance.md Principles items 2, 4; examples: Guidance.md Examples - Load applications)
3. Define supports: locations from drawings, types (rigid, spring, anchor) (interface: Specification.md IR-1; requirements: Specification.md FR-6; rationale: Guidance.md Principles item 4; considerations: Guidance.md Considerations - Stress Analysis; cross-reference DEL-14.01, DEL-14.02)
4. Run load cases: sustained (P+W), occasional (P+W+E), thermal expansion (construction: Datasheet.md Construction item 2; requirements: Specification.md PR-6; rationale: Guidance.md Principles items 2, 4; examples: Guidance.md Principles item 4 - Load Combinations)
5. Check results: stress ratios ≤ 1.0, support loads, nozzle loads (construction: Datasheet.md Construction item 2 - Outputs; requirements: Specification.md FR-5, FR-6, FR-7; quality: Specification.md QR-3; verification: Specification.md Verification - Acceptance criteria; examples: Guidance.md Examples - Check results)
6. Iterate: Adjust supports, add expansion loops, or add spring hangers if stresses excessive (requirements: Specification.md FR-5; rationale: Guidance.md Principles item 3; considerations: Guidance.md Considerations - Stress Analysis; trade-offs: Guidance.md Trade-offs item 3)
7. Document: Stress analysis report with model, loads, results, conclusions (construction: Datasheet.md Construction item 2 - Outputs; quality: Specification.md QR-4; documentation: Specification.md Documentation; records: Records section)

**Outputs:**
- Stress analysis reports for critical lines (construction: Datasheet.md Construction item 2; requirements: Specification.md FR-5; documentation: Specification.md Documentation; records: Records section)
- Support loads for structural design (construction: Datasheet.md Construction item 2 - Outputs; requirements: Specification.md FR-6; interface: Specification.md IR-6; verification: Specification.md Verification - Acceptance criteria; cross-reference PKG-05, PKG-06, DEL-14.01)
- Equipment nozzle loads (construction: Datasheet.md Construction item 2 - Outputs; requirements: Specification.md FR-7; interface: Specification.md IR-5; verification: Specification.md Verification - Acceptance criteria)

---

### Step 3: Flexibility Analysis

**Objective:** Analyze thermal expansion and verify thermal stresses/loads acceptable (construction: Datasheet.md Construction item 3; requirements: Specification.md FR-8, FR-9, FR-10; rationale: Guidance.md Principles item 3; examples: Guidance.md Examples - Typical flexibility analysis).

**Actions:**
1. Identify lines with significant temperature variation (ΔT > 50°C typical threshold) (construction: Datasheet.md Construction item 3 - TBD; conditions: Datasheet.md Operating temperature; requirements: Specification.md FR-8; considerations: Guidance.md Considerations - Flexibility Analysis; trade-offs: Guidance.md Trade-offs item 2)
2. Model thermal expansion in stress software (attributes: Datasheet.md Software/Tools; construction: Datasheet.md Construction item 3 - Software; requirements: Specification.md PR-2; standards: Specification.md Standards - Software, ASME B31.3; interface: Specification.md IR-1, IR-2; rationale: Guidance.md Principles item 3; examples: Guidance.md Examples - Typical flexibility analysis)
3. Calculate thermal displacements and stresses (construction: Datasheet.md Construction item 3 - Outputs; requirements: Specification.md FR-8; rationale: Guidance.md Principles item 3; examples: Guidance.md Examples - Calculate thermal growth)
4. Verify equipment nozzle loads within allowables (vendor data) (construction: Datasheet.md Construction item 3 - Outputs; requirements: Specification.md FR-9; interface: Specification.md IR-5; rationale: Guidance.md Principles item 3; considerations: Guidance.md Considerations - Flexibility Analysis; verification: Specification.md Verification - Acceptance criteria)
5. Provide mitigation if needed (expansion loops, expansion joints, spring hangers) (construction: Datasheet.md Construction item 3 - Outputs; requirements: Specification.md FR-10; rationale: Guidance.md Principles item 3; considerations: Guidance.md Considerations - Flexibility Analysis; trade-offs: Guidance.md Trade-offs item 3; examples: Guidance.md Examples - Model with expansion loop; cross-reference DEL-14.01, DEL-14.02)
6. Document: Flexibility analysis report with thermal growth, stresses, nozzle loads (construction: Datasheet.md Construction item 3 - Outputs; quality: Specification.md QR-4; documentation: Specification.md Documentation; records: Records section)

**Outputs:**
- Flexibility analysis reports for lines with significant thermal expansion (construction: Datasheet.md Construction item 3; requirements: Specification.md FR-8; documentation: Specification.md Documentation; records: Records section)
- Thermal expansion mitigation requirements (construction: Datasheet.md Construction item 3 - Outputs; requirements: Specification.md FR-10; cross-reference DEL-14.01, DEL-14.02)
- Equipment nozzle loads from thermal expansion (construction: Datasheet.md Construction item 3 - Outputs; requirements: Specification.md FR-9; interface: Specification.md IR-5; verification: Specification.md Verification - Acceptance criteria)

---

### Step 4: Independent Check

**Objective:** Independent verification of all calculations (quality: Specification.md QR-1, QR-2, QR-3; verification: Specification.md Verification - Calculation check).

**Actions:**
1. Assign checker (qualified engineer, not calculation originator) (personnel: Prerequisites section; quality: Specification.md QR-1; verification: Specification.md Verification - Calculation check)
2. Checker verifies: inputs, methodology, software model, results reasonableness, code compliance (quality: Specification.md QR-2, QR-3; verification: Specification.md Verification - Calculation check sections)
3. Checker signs off or issues comments (quality: Specification.md QR-1; documentation: Specification.md Documentation - Check sign-off)
4. Resolve comments and update calculations (quality: Specification.md QR-3)

**Verification:**
- All inputs verified against source documents (interface: Specification.md IR-1, IR-2, IR-3; verification: Specification.md Verification - Calculation check)
- Methodology compliant with ASME B31.3 and industry standards (requirements: Specification.md PR-1; standards: Specification.md Standards section; verification: Specification.md Verification - Calculation check)
- Software models correct (geometry, loads, boundary conditions) (quality: Specification.md QR-2; verification: Specification.md Verification - Calculation check)
- Results meet acceptance criteria (quality: Specification.md QR-3; verification: Specification.md Verification - Acceptance criteria)

---

### Step 5: Approval and Issuance

**Objective:** Finalize and issue calculation package (attributes: Datasheet.md Revision Control; quality: Specification.md QR-4; documentation: Specification.md Documentation).

**Actions:**
1. Compile calculation package (all calcs, check sign-offs) (documentation: Specification.md Documentation - Calculation package; records: Records section)
2. Discipline lead approval (quality: Specification.md QR-4; documentation: Specification.md Documentation - Check sign-off)
3. Issue to `3_Issued/` with revision control (attributes: Datasheet.md Revision Control; documentation: Specification.md Documentation - Storage; records: Records section - Storage)

**Outputs:**
- Complete calculation package ready for use in design and construction (documentation: Specification.md Documentation; records: Records section)

---

## Verification

**Verification activities summary:**

| Step | Verification Method | Acceptance Criteria |
|------|---------------------|---------------------|
| 1. Pipe Sizing | Independent check | Velocities 1.5-3.0 m/s; pressure drops within budget (requirements: Specification.md FR-2, FR-3; quality: Specification.md QR-1; verification: Specification.md Verification - Acceptance criteria) |
| 2. Stress Analysis | Independent check, software verification | Stress ratios ≤ 1.0; support loads OK; nozzle loads within allowables (requirements: Specification.md FR-5, FR-6, FR-7; quality: Specification.md QR-2, QR-3; verification: Specification.md Verification - Acceptance criteria) |
| 3. Flexibility Analysis | Independent check, vendor data comparison | Thermal stresses ≤ ASME B31.3; nozzle loads within vendor allowables (requirements: Specification.md FR-8, FR-9; quality: Specification.md QR-3; verification: Specification.md Verification - Acceptance criteria) |
| 4. Independent Check | Qualified engineer review | All calculations verified; checker sign-off (quality: Specification.md QR-1; verification: Specification.md Verification - Calculation check) |
| 5. Approval | Discipline lead review | Package complete and approved (quality: Specification.md QR-4) |

**Overall acceptance criteria** (quality: Specification.md QR-3; verification: Specification.md Verification - Acceptance criteria):
- All stress ratios ≤ 1.0 (ASME B31.3 compliance) (code: Datasheet.md Design Code; requirements: Specification.md FR-5, FR-8; rationale: Guidance.md Principles item 2)
- Equipment nozzle loads within vendor allowables (requirements: Specification.md FR-7, FR-9; interface: Specification.md IR-5; rationale: Guidance.md Principles item 3)
- Support loads within structural capacity (requirements: Specification.md FR-6; interface: Specification.md IR-6; cross-reference PKG-05, PKG-06)
- Velocities within acceptable range (requirements: Specification.md FR-3; rationale: Guidance.md Principles item 1)

---

## Records

**Outputs** (construction: Datasheet.md Construction section; documentation: Specification.md Documentation):
- Pipe sizing calculations (summary table and detailed calcs) (construction: Datasheet.md Construction item 1; requirements: Specification.md FR-1; Step 1 above)
- Stress analysis reports (software models and output) (construction: Datasheet.md Construction item 2; requirements: Specification.md FR-5; Step 2 above)
- Flexibility analysis reports (thermal expansion results) (construction: Datasheet.md Construction item 3; requirements: Specification.md FR-8; Step 3 above)

**Storage:** `2_Checking/` (review) → `3_Issued/` (approved) (attributes: Datasheet.md Revision Control; documentation: Specification.md Documentation - Storage; Step 5 above)

**Format:** PDF for issued calculations; native software files for models (attributes: Datasheet.md Software/Tools; quality: Specification.md QR-4; documentation: Specification.md Documentation)

**Retention:** **TBD** — permanent as part of project record **ASSUMPTION** (quality: Specification.md QR-4; cross-reference DEL-14.01, DEL-14.02)
