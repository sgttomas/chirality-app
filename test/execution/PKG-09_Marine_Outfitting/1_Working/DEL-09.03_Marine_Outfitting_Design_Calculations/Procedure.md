# Procedure: DEL-09.03 Marine Outfitting Design Calculations

## Purpose

This procedure defines the process for producing and verifying **Marine Outfitting Design Calculations** within **PKG-09 Marine Outfitting**.

**Decomposition definition (authoritative):** Provides the engineering basis and sizing/verification calculations for marine outfitting. (**Source:** Decomposition, DEL-09.03 row)

**Deliverable type:** Calculation
**Responsible party:** D&B Contractor

**Scope:** This procedure covers the calculation development process from scope confirmation through issue preparation, including input collection, calculation execution, independent checking, and verification activities.

## Prerequisites

### Dependencies

Dependencies are coordinated externally (NOT_TRACKED). See `_DEPENDENCIES.md` and `execution/_Coordination/_COORDINATION.md`.

**Required upstream inputs (confirm availability and maturity prior to commencement):**

| Input | Source | Specification § | Guidance § | Required For | Status |
|-------|--------|-----------------|------------|--------------|--------|
| Berthing energy results | DEL-08.06 | SPEC § 1.3, 2.1 | Guidance § Principles (Fender Calculations) | Fender reaction calculation — design energy (kJ), vessel characteristics, approach velocity | **TBD** |
| Fender deflection/reaction curves | DEL-08.07 / Vendor | SPEC § 1.3, 2.1 | Guidance § Principles (Fender Calculations) | Fender reaction calculation — R vs δ curve for selected fender | **TBD** |
| Fender supplier verification | DEL-08.08 | SPEC § 1.3, 2.1 | Guidance § Principles (Fender Calculations) | Fender performance validation | **TBD** |
| Mooring line loads | DEL-08.09 | SPEC § 1.3, 2.2 | Guidance § Principles (Bollard Calculations) | Bollard load calculation — line loads (kN) for normal/storm/emergency cases | **TBD** |
| Design vessel characteristics | Employer's Requirements | SPEC § 1.2 | — | Both calculations — vessel type, LOA, beam, displacement, mooring configuration | **TBD** |
| Environmental conditions | Employer's Requirements | SPEC § 1.2 | — | Load cases — wind, current, wave, tidal range, temperature range | **TBD** |
| Marine structure geometry and support conditions | PKG-08 outputs (DEL-08.01, DEL-08.03) | SPEC § 3 | Guidance § Considerations (Interface loads) | Interface load verification — fender/bollard mounting locations, structural capacities, allowable loads | **TBD** |
| Applicable codes/standards | Employer's Requirements / Authority | SPEC § 1.2, Standards | Guidance § Principles | Methods and factors — PIANC, BS 6349, or equivalent | **TBD** |

### Reference Materials

- See `_REFERENCES.md` for applicable reference documents.
- See `0_References/` in package directory (`test/execution/PKG-09_Marine_Outfitting/0_References/`) for reference materials.
- Employer's Requirements (Vol 2 Part 1–3) — **TBD** (criteria applicable to marine outfitting calculations).
- Applicable codes: PIANC guidelines, BS 6349, local port authority requirements — **TBD**.

### Personnel Requirements

| Role | Requirement |
|------|-------------|
| Originator (Calculation Engineer) | Qualified Marine discipline engineer with experience in marine terminal design, fender/bollard design, marine engineering calculations — **TBD** (qualifications per project quality plan) |
| Checker | Independent qualified engineer (independent of originator; qualified in Marine discipline or relevant calculation experience) — **TBD** (checker qualifications per project quality plan) |
| Approver | **TBD** — per project authority matrix (typically Marine discipline lead or Package Manager) |

**ASSUMPTION:** Personnel competency and authority per project quality procedures and authority matrix.

### Tools and Resources

| Tool/Resource | Purpose | Status |
|---------------|---------|--------|
| Calculation tools | Hand calculations, Excel spreadsheet, or specialized software (e.g., SACS, ANSYS) | **TBD** — method to be selected based on calculation complexity |
| Vendor data access | Fender deflection curves, bollard catalogs | **TBD** — vendor data to be obtained during equipment selection |
| Code/standard access | PIANC guidelines, BS 6349, other applicable codes | **TBD** — library access or online subscriptions |

## Steps

### Step 1: Confirm Scope

**Objective:** Establish the calculation scope and confirm anticipated artifacts.

**Actions:**
1. Review DEL-09.03 anticipated artifacts from the decomposition:
   - Fender reaction calculations
   - Bollard load calculations
2. Review `Datasheet.md` Calculation Checklist for minimum calculation content requirements.
3. Confirm calculation scope boundaries:
   - Fender calculations: reaction forces at design deflection; verification against structural capacity
   - Bollard calculations: required SWL with factors; verification against selected bollard rating; foundation capacity (if applicable)
4. Identify any additional calculations required beyond decomposition-listed artifacts (e.g., ladder structural calculations if required; existing Berth 10 bollard capacity verification).
5. Document scope clarifications (if any).

**Inputs:** Decomposition, `Datasheet.md`, `Specification.md`.
**Outputs:** Confirmed calculation scope; scope clarification notes (if any).
**Verification:** Calculation scope addresses all `Datasheet.md` Calculation Checklist items and decomposition anticipated artifacts.

### Step 2: Collect Inputs

**Objective:** Obtain all required inputs for calculations and document source traceability.

**Actions:**
1. Request required inputs per Prerequisites table above from source deliverable owners (DEL-08.06, DEL-08.07, DEL-08.08, DEL-08.09, PKG-08).
2. Obtain Employer's Requirements clauses applicable to marine outfitting calculations (design vessel, environmental conditions, safety factors, acceptance criteria).
3. Obtain applicable codes and standards (PIANC, BS 6349, or as specified by ER).
4. Obtain vendor data for selected fender and bollard systems (deflection curves, performance data, catalog sheets).
5. Document input sources with full traceability:
   - For deliverables: cite deliverable ID, document number, revision, date, section/page
   - For vendor data: cite document number/catalog reference, revision/date, supplier name
   - For codes/standards: cite designation and edition (e.g., "BS 6349-4:2014")
   - For ER: cite ER volume, section, clause number
6. Prepare input register tracking all inputs:
   - Input description
   - Source (deliverable ID, document number, revision, date, or ER clause)
   - Status (received, TBD)
   - Value/data extracted
7. Log missing inputs as **TBD** with action owners and target dates.

**Inputs:** Prerequisites list, `Specification.md § 1.3`.
**Outputs:** Input register with source traceability; extracted input data; missing inputs log with action owners.
**Verification:** Input register is complete and tracks all required inputs; all received inputs have full source citation; missing inputs have action owners assigned and reviewed with Project Manager or Package Lead.

### Step 3: Define Design Basis

**Objective:** Document design basis and assumptions for calculations.

**Actions:**
1. Document design basis per `Specification.md § 1.2`:
   - **Design vessel characteristics:** Extract from ER or DEL-08.06/DEL-08.09 (vessel type, LOA, beam, displacement, approach velocity, mooring configuration).
   - **Environmental conditions:** Extract from ER or DEL-08.06/DEL-08.09 (wind, current, wave, tidal range, temperature range).
   - **Safety factors and load factors:** Extract from applicable codes or ER (fender energy absorption factors, bollard design factors, load combinations).
   - **Acceptance criteria:** Define what constitutes acceptable results (e.g., "Fender reaction ≤ structural allowable," "Bollard SWL ≥ required SWL").
2. Label assumptions explicitly:
   - For each assumption not directly supported by source documents, label **ASSUMPTION** and state basis for engineering judgment.
   - Flag assumptions requiring approval (significant engineering judgments, deviations from codes, extrapolations beyond vendor data).
3. Prepare Design Basis section of calculation document with all items documented and sourced/labeled.

**Inputs:** Input register (Step 2), ER clauses, codes/standards, `Specification.md § 1.2`, `Guidance.md § Principles (Evidence Rules)`.
**Outputs:** Design Basis section of calculation; assumptions list with labels and approval flags.
**Verification:** All design basis items documented; all assumptions labeled; approval flags identified; sources cited or TBD noted.

### Step 4: Define Load Cases

**Objective:** Define load cases and combinations for calculations.

**Actions:**
1. Define load cases per Employer's Requirements and applicable codes:
   - **Fender calculations:**
     - Design berthing energy at various deflections (if multiple scenarios considered)
     - Temperature effects on fender stiffness (if applicable per codes/ER)
   - **Bollard calculations:**
     - Normal mooring (routine cargo transfer operations)
     - Storm mooring (design environmental conditions without vessel departure)
     - Emergency breakaway (maximum line load before line failure or bollard failure)
2. Define load combinations and factors (per applicable codes):
   - Combination of wind, current, wave loads (if applicable)
   - Load factors (ultimate limit state, serviceability limit state) per codes
3. Identify governing load case (expected case that produces maximum demand):
   - For fenders: typically design berthing energy case
   - For bollards: typically storm mooring or emergency breakaway case
4. Document load cases and combinations in Load Cases section of calculation document.

**Inputs:** Design basis (Step 3), ER clauses, codes/standards (PIANC, BS 6349), DEL-08.06, DEL-08.09, `Specification.md § 1.5`, `Guidance.md § Principles (Bollard Calculations)`.
**Outputs:** Load Cases section of calculation; governing load case identification.
**Verification:** Load cases defined per codes/ER; load combinations and factors stated; governing case identified with rationale.

### Step 5: Execute Calculations

**Objective:** Perform fender and bollard calculations using appropriate methods and tools.

**Actions:**

**5a. Fender Reaction Calculation (per `Specification.md § 2.1` and `Guidance.md § Principles (Fender Calculations)`):**
1. Input berthing energy E (kJ) from DEL-08.06.
2. Input fender deflection/reaction curve from DEL-08.07 or vendor data (R vs δ).
3. Determine deflection δ corresponding to energy E:
   - From curve: Find δ where E = ∫ R dδ (area under curve up to δ equals E)
   - May require graphical integration, numerical integration, or vendor-provided energy tables
4. Read reaction R (kN) at deflection δ from curve.
5. Apply temperature factor (if applicable):
   - Check fender manufacturer guidance for temperature correction
   - Apply factor to reaction: R_adjusted = R × temperature factor
6. Compare calculated reaction R (or R_adjusted) to marine structure allowable load (from DEL-08.03).
7. Calculate margin: Margin (%) = (Allowable - R) / Allowable × 100%.
8. Document calculation steps, intermediate values, and results.

**5b. Bollard Load Calculation (per `Specification.md § 2.2` and `Guidance.md § Principles (Bollard Calculations)`):**
1. Input mooring line loads from DEL-08.09 for each load case (normal, storm, emergency).
2. Input bollard arrangement and line angles from DEL-09.01 (if available; otherwise assume typical).
3. Determine maximum line load (governing case among normal, storm, emergency).
4. Apply design factor per code (e.g., Required SWL = maximum line load × design factor).
5. Compare required SWL to selected bollard rating (from vendor catalog or DEL-09.04 datasheet).
6. Calculate margin: Margin (%) = (Selected SWL - Required SWL) / Required SWL × 100%.
7. Verify foundation/anchorage capacity (if bollard mounted on marine structure):
   - Calculate foundation loads (horizontal, vertical, overturning moment)
   - Compare to PKG-08 structural capacity (from DEL-08.03)
8. Document calculation steps, intermediate values, and results.

**5c. Calculation Methods and Tools:**
- Record methodology: hand calculation, spreadsheet (cite filename), or software (cite name/version).
- State formulas and code references (cite code designation, edition, clause, equation).
- If software is used:
  - Document software name, version, license status
  - Verify output reasonableness (order-of-magnitude check, comparison to hand calculation or benchmark)
  - Attach software input/output files as appendix
- Show sample calculations or derivations where needed for clarity.

**Inputs:** Design basis (Step 3), load cases (Step 4), input register (Step 2), `Specification.md § 1.4, 2.1, 2.2`, `Guidance.md § Principles`.
**Outputs:** Calculation body with methodology, inputs, calculations, intermediate values, results; appendices with vendor data, software output (if applicable).
**Verification:** Calculations follow stated methodology; inputs correctly applied; formulas/code references cited; arithmetic correct (verified in Step 6 independent check); results reasonable (order-of-magnitude check).

### Step 6: Independent Check

**Objective:** Verify calculation methodology, inputs, arithmetic, and code compliance by independent checker.

**Actions:**
1. Assign independent checker (qualified engineer independent of originator per project quality procedures).
2. Provide checker with calculation document and supporting materials:
   - Draft calculation (Step 5 output)
   - Input register (Step 2)
   - Input source documents (DEL-08.06, DEL-08.07, DEL-08.08, DEL-08.09, DEL-08.03, ER clauses, codes/standards)
   - Vendor data
   - Related deliverables (DEL-09.01, DEL-09.02, DEL-09.04 for cross-reference)
3. Checker performs independent check per `Specification.md § Verification` check criteria:
   - **Methodology is appropriate:** Calculation methods follow applicable codes (PIANC, BS 6349); formulas/equations correctly applied; approach is sound.
   - **Inputs are correctly applied:** All inputs match source documents (verify against input register); inputs are appropriate for calculation (no misapplication of data).
   - **Arithmetic is correct:** Numerical calculations verified (spot-check critical calculations; verify formulas in spreadsheet if applicable).
   - **Results are reasonable:** Results pass reasonableness check (order-of-magnitude, comparison to similar projects, engineering judgment).
   - **Code compliance is demonstrated:** Safety factors, load cases, methods comply with applicable codes (PIANC, BS 6349, or as specified by ER).
   - **Traceability is adequate:** All inputs cite sources; assumptions labeled; TBDs noted.
4. Checker documents findings in check record:
   - Comments, questions, corrections identified
   - Categorize comments (e.g., "Critical," "Moderate," "Minor," "Clarification")
5. Originator reviews checker comments and responds:
   - **Accept:** Incorporate correction into calculation; document acceptance.
   - **Clarify:** Provide clarification or additional justification; revise calculation if needed to improve clarity.
   - **Reject:** Provide justification for rejection (if checker comment is not applicable); discuss with checker to resolve.
6. Originator revises calculation to address checker comments (corrections, clarifications, improvements).
7. Checker reviews revised calculation and confirms resolution of comments.
8. Checker provides sign-off:
   - Confirmation that calculation is methodologically sound, inputs are correct, arithmetic is verified, results are reasonable, code compliance demonstrated
   - Checker signature and date on check record
   - **TBD:** Checker acceptance criteria and sign-off requirements per project quality procedures.

**Inputs:** Draft calculation (Step 5), all supporting materials and references.
**Outputs:** Check record with checker findings; comment resolution log; revised calculation incorporating checker comments; checker sign-off.
**Verification:** Checker sign-off obtained; all checker comments resolved and documented; calculation meets all technical accuracy, code compliance, and traceability requirements.

### Step 7: Summarize Results

**Objective:** Prepare results summary and ensure consistency with related deliverables.

**Actions:**
1. Prepare Results and Conclusions section per `Specification.md § 1.6`:
   - **Results summary:**
     - Key calculated values with units (fender reaction force in kN, bollard required SWL in kN or tonnes)
     - Intermediate results (as needed for traceability)
     - Governing load case identification (which case produced maximum demand)
   - **Comparison to acceptance criteria:**
     - Fender: R ≤ Allowable structural load (state margin %)
     - Bollard: Selected SWL ≥ Required SWL (state margin %)
   - **Conclusions:**
     - State whether calculated values meet acceptance criteria
     - Identify any exceedances or concerns
     - Provide recommendations (equipment selection, design modifications, coordination with PKG-08)
2. Cross-check results with DEL-09.04 data sheets:
   - Verify that fender reaction force in calculation matches DEL-09.04 fender datasheet
   - Verify that bollard SWL in calculation matches DEL-09.04 bollard datasheet
   - If discrepancies exist, resolve (update calculation or update datasheet to match)
3. Verify consistency with DEL-09.02 specification requirements:
   - Calculation results substantiate DEL-09.02 § 2.1 fender performance requirements
   - Calculation results substantiate DEL-09.02 § 2.2 bollard performance requirements
4. Document interface loads for PKG-08 coordination:
   - Fender reaction forces (magnitude, location, direction)
   - Bollard loads (magnitude, location, direction, foundation reactions if applicable)
   - Include in Results summary or create Interface Loads summary section
5. Finalize Results and Conclusions section with all items complete.

**Inputs:** Calculation results (Step 5), checker-verified calculation (Step 6), DEL-09.04 datasheets, DEL-09.02 specification, `Specification.md § 1.6, 4`.
**Outputs:** Results and Conclusions section; interface loads summary; cross-check verification with DEL-09.04 and DEL-09.02.
**Verification:** Results summary is complete with all key values, governing cases, comparisons, conclusions; results consistent with DEL-09.04 data sheets; results substantiate DEL-09.02 requirements; interface loads documented for PKG-08 coordination.

### Step 8: Issue Preparation

**Objective:** Prepare calculation package for issue (review/approval or construction).

**Actions:**
1. Apply final document control:
   - Assign document number per project numbering system (if not already assigned).
   - Apply revision designation per project revision scheme (e.g., Rev 0 for first issue, Rev A/B/C for subsequent revisions).
   - Update cover sheet / title sheet with document number, revision, date, project information, originator/checker/approver names.
2. Compile final calculation package:
   - Cover / Title Sheet
   - Purpose and Scope (§ 1.1)
   - Design Basis and Assumptions (§ 1.2)
   - Inputs and References (§ 1.3)
   - Methods and Tools (§ 1.4)
   - Load Cases and Combinations (§ 1.5)
   - Calculation Body (Fender reaction calculation, Bollard load calculation)
   - Results and Conclusions (§ 1.6)
   - Check Record (§ 1.7)
   - Appendices (vendor data, input sheets, software output, etc.)
3. Prepare issue package:
   - **Format:** PDF for issue/record; native format (Excel, software files) for working files and reproducibility (per `Specification.md § Documentation`).
   - **Transmittal:** Prepare transmittal cover sheet listing document number, title, revision, purpose of issue (e.g., "For Review," "For Approval," "For Construction").
4. Prepare issue records:
   - Input register (Step 2)
   - Assumptions list with approval status
   - Check record with checker sign-off (Step 6)
   - Cross-check verification with DEL-09.04 and DEL-09.02 (Step 7)
5. Update `_STATUS.md` when ready for CHECKING or ISSUED state:
   - **CHECKING:** Calculation issued for review/approval (placed in `2_Checking/To/`)
   - **ISSUED:** Calculation approved and issued for construction (placed in `3_Issued/`)
   - Update status with date, revision, and brief description of issue.
6. Archive previous revisions (if applicable) per project records management procedures.

**Inputs:** Final calculation (Steps 5, 6, 7), all supporting records, project document control procedures.
**Outputs:** Issue-ready calculation package; transmittal; supporting records (input register, assumptions, check record, cross-check); updated `_STATUS.md`.
**Verification:** Calculation package is complete and complies with project document control requirements; all check/sign-off records are complete and attached; `_STATUS.md` updated correctly with appropriate state and revision information.
**TBD:** Project document control procedures and issue protocols.

## Verification

**Summary of verification activities performed throughout this procedure:**

| Activity | Step | Criteria | Sign-off |
|----------|------|----------|----------|
| Scope confirmation | Step 1 | Calculation scope addresses all `Datasheet.md` Calculation Checklist items and decomposition artifacts | Originator |
| Input collection and traceability | Step 2 | All required inputs obtained or TBD with action owners; all inputs have full source citation (deliverable ID, doc number, revision, date, section/page) | Originator / Package Lead |
| Design basis documentation | Step 3 | All design basis items documented; assumptions labeled; sources cited or TBD noted | Originator |
| Load cases defined | Step 4 | Load cases defined per codes/ER; load combinations and factors stated; governing case identified | Originator |
| Calculations executed | Step 5 | Methodology appropriate; inputs correctly applied; formulas/code references cited; arithmetic correct (verified in Step 6); results reasonable | Originator |
| Independent check | Step 6 | Methodology, inputs, arithmetic, code compliance, results verified by independent checker | Checker |
| Results summarized and cross-checked | Step 7 | Results summary complete; consistent with DEL-09.04 data sheets; substantiates DEL-09.02 requirements; interface loads documented | Originator |
| Issue readiness | Step 8 | Calculation package complete; complies with document control requirements | Approver |

**Sign-off requirements (per project quality procedures):**

| Role | Signature | Purpose |
|------|-----------|---------|
| Originator | Required | Confirms calculation is complete and meets requirements |
| Checker | Required | Confirms independent check completed; calculation is methodologically sound, inputs correct, arithmetic verified, results reasonable, code compliant |
| Approver | Required | Authorizes issue for intended purpose (review/approval/construction) |

**ASSUMPTION:** Sign-off protocol and authority matrix per project quality procedures.

## Records

**Documentation outputs (per `Specification.md § Documentation` and `Datasheet.md`):**
- Fender reaction calculations
- Bollard load calculations
- (May be combined into a single calculation package or separate calculation packages, depending on project document control preferences)

**Record management:**

| Record | Location | Retention | Purpose |
|--------|----------|-----------|---------|
| Draft calculations (in progress) | `1_Working/` | Per project procedures | Working files during development |
| Review package | `2_Checking/To/` | Per project procedures | Issue for review/approval |
| Issued calculations | `3_Issued/` | Per project procedures | Final issue for construction; project record |
| Input register | Deliverable folder or project QA system | Per project procedures | Source traceability; tracking of inputs |
| Assumptions list | Deliverable folder or project QA system | Per project procedures | Tracking of assumptions and approval status |
| Check record with checker sign-off | Deliverable folder or project QA system | Per project procedures | Evidence of independent check |
| Cross-check verification (with DEL-09.04, DEL-09.02) | Deliverable folder or project QA system | Per project procedures | Evidence of consistency verification |

**ASSUMPTION:** Electronic records managed in project document management system with appropriate access controls, backup/retention protocols, and audit trail.

**Cross-reference:** See `Datasheet.md § References` for related documents.
