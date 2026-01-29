# Specification: DEL-09.03 Marine Outfitting Design Calculations

## Scope

This specification defines the requirements for producing **Marine Outfitting Design Calculations** within **PKG-09 Marine Outfitting**.

**Decomposition definition (authoritative):** Provides the engineering basis and sizing/verification calculations for marine outfitting. (**Source:** Decomposition, DEL-09.03 row)

**Package scope (PKG-09):** Fenders, bollards, ladders, life-saving equipment, existing Berth 10 upgrades and repairs. (**Source:** Decomposition, PKG-09)

**Anticipated deliverable artifacts:**
- Fender reaction calculations
- Bollard load calculations

**Purpose:** Calculations provide the engineering basis for selecting and verifying marine outfitting equipment, bridging upstream design inputs (PKG-08 analyses) and downstream equipment selection/substantiation (DEL-09.04 data sheets, DEL-09.02 specification).

## Requirements

### 1) Calculation Package Structure Requirements

Each calculation package shall include the following sections (per `Datasheet.md` Calculation Checklist and `Guidance.md § Examples`). Cross-reference to verification steps in `Procedure.md`.

#### 1.1 Purpose and Scope

**Requirements:**
- Statement of calculation objective (what is being calculated and why).
- Reference to DEL-09.03 decomposition intent and deliverable context.
- Items included and excluded in calculation scope.
- Identification of intended use (design verification, equipment selection basis, substantiation of DEL-09.02 requirements).

**Rationale:** See `Guidance.md § Principles (Calculation Intent)`.
**Verification:** See `Procedure.md § Step 1` (confirm scope).

#### 1.2 Design Basis and Assumptions

**Requirements:**
- **Design vessel characteristics** shall be stated (from Employer's Requirements or DEL-08.06/DEL-08.09):
  - Vessel type, length overall (LOA), beam, displacement
  - Design approach velocity (for fender calculations)
  - Mooring arrangement (number of lines, line types, pretension) (for bollard calculations)
  - **TBD:** Specific vessel data to be extracted from ER
- **Environmental conditions** shall be stated (from Employer's Requirements or DEL-08.06/DEL-08.09):
  - Wind speed (sustained, gust)
  - Current velocity
  - Wave height (significant wave height, design wave)
  - Tidal range (high water, low water, mean tide levels)
  - Temperature range (ambient air, water) — affects fender rubber stiffness
  - **TBD:** Specific environmental data to be confirmed
- **Safety factors and load factors** shall be stated (from applicable codes or Employer's Requirements):
  - Fender energy absorption factors (if applicable)
  - Bollard design factors (e.g., BS 6349 recommends SWL ≥ MBL of largest mooring line)
  - Load combinations and factors
  - **TBD:** Specific factors to be confirmed from codes/ER
- **Assumptions not supported by source documents shall be labeled **ASSUMPTION**** and flagged for approval with basis for engineering judgment stated.
- **Design life and service life requirements** shall be stated (if applicable to calculation). (**TBD** — from ER)

**Rationale:** See `Guidance.md § Principles (Evidence Rules)`.
**Verification:** See `Procedure.md § Step 3` (define design basis); `Procedure.md § Step 6` (independent check verifies assumptions are appropriate).

#### 1.3 Inputs and References

**Requirements:**
- **All inputs shall be documented with source traceability:**
  - Employer's Requirements clauses (cite ER volume, section, clause number)
  - Vendor data (cite document number, revision, date, supplier name)
  - Supporting deliverables (cite deliverable ID, document number, revision, date, section/page)
    - DEL-08.06 Berthing Energy Calculation Report (for fender calculations)
    - DEL-08.07 Fender System Deflection Characteristics Data Package (for fender calculations)
    - DEL-08.08 Fender Supplier Design Verification Letter/Report (for fender calculations)
    - DEL-08.09 Mooring Analysis Report (for bollard calculations)
    - DEL-08.01 Marine Structures Design Drawing Set (for geometry, arrangement)
    - DEL-08.03 Marine Structures Design Calculations (for structural capacity, allowable loads)
  - Drawings and geometry (cite drawing numbers, revisions)
  - Codes and standards (cite designation and edition, e.g., "BS 6349-4:2014," "PIANC WG33:2002")
- **Input register** (per `Procedure.md § Step 2`) shall track all inputs with status (received, TBD) and version control.

**Rationale:** See `Guidance.md § Principles (Evidence Rules)`.
**Verification:** See `Procedure.md § Step 2` (collect inputs); `Procedure.md § Step 6` (independent check verifies inputs are correct and appropriately applied).

#### 1.4 Methods and Tools

**Requirements:**
- **Calculation method** shall be stated:
  - Hand calculation (formulas, equations, step-by-step logic)
  - Spreadsheet calculation (Excel or equivalent — include spreadsheet filename, version, date)
  - Software calculation (specify software name, version, license status)
- **Software verification** (if software used):
  - Verify output reasonableness (order-of-magnitude check, comparison to hand calculation or industry benchmark)
  - Document software validation (if required by project quality plan)
  - **TBD:** Software validation requirements per project procedures
- **Formulas and code references** shall be cited:
  - Reference specific code clauses or equations (e.g., "per BS 6349-4:2014 § 5.3.2, Equation 5.1")
  - State formula variables with units
  - Show sample calculations or derivations where needed for clarity

**Rationale:** See `Guidance.md § Principles (Calculation Intent)` and `Guidance.md § Considerations`.
**Verification:** See `Procedure.md § Step 5` (execute calculations); `Procedure.md § Step 6` (independent check verifies methodology is appropriate and arithmetic is correct).

#### 1.5 Load Cases and Combinations

**Requirements:**
- **Load cases** shall be defined per Employer's Requirements and applicable codes:
  - **Fender calculations:** Design berthing energy at various deflections (if multiple cases considered); temperature effects on fender stiffness (if applicable).
  - **Bollard calculations:** Typical load cases include:
    - Normal mooring (routine cargo transfer operations)
    - Storm mooring (design environmental conditions without vessel departure)
    - Emergency breakaway (maximum line load before line failure or bollard failure)
  - **TBD:** Specific load cases to be confirmed from ER and codes
- **Load combinations and factors** shall be stated (per applicable codes):
  - Combination of wind, current, wave loads (if applicable)
  - Load factors (ultimate limit state, serviceability limit state)
  - **TBD:** Load combinations and factors per codes/ER

**Rationale:** See `Guidance.md § Principles (Bollard Calculations)`.
**Verification:** See `Procedure.md § Step 4` (define load cases); `Procedure.md § Step 6` (independent check verifies load cases are appropriate and code-compliant).

#### 1.6 Results and Conclusions

**Requirements:**
- **Results summary** shall include:
  - Key calculated values with units (fender reaction force in kN, bollard required SWL in kN or tonnes, etc.)
  - Governing load case identification (which case produces maximum demand)
  - Intermediate calculation results (as needed for verification and traceability)
- **Comparison to acceptance criteria / allowable values:**
  - **Fender calculations:** Compare calculated reaction force to marine structure allowable load (from PKG-08)
  - **Bollard calculations:** Compare required SWL to selected bollard rating
  - State margin (e.g., "Calculated reaction 500 kN < Allowable 600 kN, margin = 20%")
- **Conclusions and recommendations:**
  - State whether calculated values meet acceptance criteria
  - Identify any exceedances or concerns
  - Provide recommendations for equipment selection or design modifications (if needed)
- **Consistency with data sheets:** Results shall match values stated in DEL-09.04 data sheets.

**Rationale:** See `Guidance.md § Principles (Calculation Intent)`.
**Verification:** See `Procedure.md § Step 7` (summarize results); `Procedure.md § Step 6` (independent check verifies results are reasonable and correctly interpreted).

#### 1.7 Check Record

**Requirements:**
- **Independent check verification** per `Procedure.md § Step 6`:
  - Checker identifies (name, title, qualifications)
  - Check scope stated (methodology, inputs, arithmetic, code compliance)
  - Check findings documented (comments, questions, corrections)
  - Originator response to check findings (revisions made, clarifications provided)
  - Checker sign-off (confirmation that calculation is acceptable and ready for use)
- **TBD:** Check record format and sign-off requirements per project quality procedures.

**Rationale:** See `Guidance.md § Principles (Calculation Intent)`.
**Verification:** See `Procedure.md § Step 6` (independent check).

### 2) Content Coverage Requirements

The calculation deliverable shall contain explicit calculations for each anticipated artifact (per `Datasheet.md` Calculation Checklist):

#### 2.1 Fender Reaction Calculations

**Requirements:**

| Requirement | Content | Specification § | Guidance § | Status |
|-------------|---------|-----------------|------------|--------|
| **Input basis** | Berthing energy (E in kJ) from DEL-08.06; cite document number, revision, section/page | § 1.3 | Guidance § Principles (Fender Calculations) | **TBD** — pending DEL-08.06 |
| **Fender performance data** | Deflection/reaction curves from DEL-08.07 or vendor data; cite source with document number, revision | § 1.3 | Guidance § Principles (Fender Calculations) | **TBD** — pending DEL-08.07 and vendor selection |
| **Calculation scope** | Determine reaction force (R in kN) at deflection corresponding to energy E; consider temperature effects if applicable | § 1.4, 1.5 | Guidance § Principles (Fender Calculations) | **TBD** |
| **Verification** | Compare calculated reaction R to marine structure allowable load (from PKG-08 DEL-08.03); state margin | § 1.6 | Guidance § Considerations (Interface loads) | **TBD** — pending PKG-08 coordination |
| **Output** | Fender reaction summary (type, size, energy capacity, reaction force at design deflection) for DEL-09.04 data sheets | § 1.6 | — | **TBD** |

**Calculation methodology (typical):**
1. Input: Berthing energy E (kJ) from DEL-08.06
2. Input: Fender deflection/reaction curve from DEL-08.07 or vendor (R vs δ, where R = reaction in kN, δ = deflection in mm or %)
3. Determine deflection δ corresponding to energy E (from curve or equation: E = ∫ R dδ)
4. Read reaction R at deflection δ from curve
5. Apply temperature factor (if applicable per fender manufacturer guidance)
6. Compare R to marine structure allowable load (from DEL-08.03)
7. Conclude: R ≤ Allowable → OK; R > Allowable → review fender selection or structural capacity

**Rationale:** See `Guidance.md § Principles (Fender Calculations)`.
**Verification:** See `Procedure.md § Step 5` (execute calculations); `Procedure.md § Step 6` (independent check).

#### 2.2 Bollard Load Calculations

**Requirements:**

| Requirement | Content | Specification § | Guidance § | Status |
|-------------|---------|-----------------|------------|--------|
| **Input basis** | Mooring line loads from DEL-08.09 (load per line in kN for normal, storm, emergency cases); cite document number, revision, section/page | § 1.3 | Guidance § Principles (Bollard Calculations) | **TBD** — pending DEL-08.09 |
| **Load cases** | Normal mooring, storm mooring, emergency breakaway; define load combinations and factors per codes | § 1.5 | Guidance § Principles (Bollard Calculations) | **TBD** — load cases from DEL-08.09 and codes |
| **Calculation scope** | Determine required bollard SWL (kN or tonnes) including design factors; verify foundation capacity (if bollard mounted on marine structure) | § 1.4, 1.5 | Guidance § Principles (Bollard Calculations) | **TBD** |
| **Verification** | Compare required SWL to selected bollard rating; state margin; verify foundation/anchorage capacity (coordinate with PKG-08) | § 1.6 | Guidance § Considerations (Interface loads) | **TBD** — pending bollard selection and PKG-08 coordination |
| **Output** | Bollard capacity summary (type, SWL rating, required capacity, margin) for DEL-09.04 data sheets | § 1.6 | — | **TBD** |

**Calculation methodology (typical):**
1. Input: Mooring line loads (kN per line) from DEL-08.09 for each load case (normal, storm, emergency)
2. Input: Bollard arrangement and line angles from DEL-09.01 (if available)
3. Determine maximum line load (governing case)
4. Apply design factor per code (e.g., BS 6349 recommends SWL ≥ MBL of largest line; typical factor 1.5–2.0)
5. Calculate required SWL = maximum line load × design factor
6. Compare required SWL to selected bollard rating
7. Verify foundation/anchorage capacity (if applicable — coordinate with PKG-08 for structural capacity)
8. Conclude: Selected SWL ≥ Required SWL → OK; Selected SWL < Required SWL → review bollard selection

**Rationale:** See `Guidance.md § Principles (Bollard Calculations)`.
**Verification:** See `Procedure.md § Step 5` (execute calculations); `Procedure.md § Step 6` (independent check).

### 3) Interface / Coordination Requirements

**Interface coordination with PKG-08 Marine Structures:**
- **Fender calculations:** Fender reaction forces shall be documented and coordinated with PKG-08 structural capacity (DEL-08.03 calculations shall confirm structure can support fender loads).
- **Bollard calculations:** Bollard loads shall be documented and coordinated with PKG-08 structural capacity (DEL-08.03 calculations shall confirm structure/foundation can support bollard loads).
- **Interface loads documentation:** Clearly state interface loads (magnitude, location, direction) for PKG-08 coordination.
- **Coordination mode:** Dependencies are managed externally (NOT_TRACKED). See `_DEPENDENCIES.md` and `execution/_Coordination/_COORDINATION.md`.

**Verification:** See `Procedure.md § Step 6` (independent check verifies interface loads are documented); coordinate via interdisciplinary check if required.

### 4) Quality / Traceability Requirements

**Traceability:**
- **Inputs from vendor data and other deliverables shall be version-controlled and referenced** (document number, revision, date) per § 1.3 requirements.
- **All assumptions shall be labeled **ASSUMPTION**** and tracked per § 1.2 requirements; assumptions requiring approval shall be flagged.
- **Calculation results shall be consistent with values in DEL-09.04 data sheets** (fender reaction force, bollard SWL) — cross-check per `Procedure.md § Step 7`.
- **Calculation results shall substantiate DEL-09.02 specification requirements** (§ 2.1 fender performance, § 2.2 bollard performance).

**Verification:** See `Procedure.md § Step 6` (independent check verifies traceability); `Procedure.md § Step 7` (cross-check with data sheets).

## Standards

**Applicable standards and codes (to be confirmed from Employer's Requirements and regulatory approvals):**

- Employer's Requirements (Vol 2 Part 1–3) — applicable clauses **TBD** (see `_REFERENCES.md`).
- **ASSUMPTION:** Calculation/design codes for marine outfitting, which may include:
  - **PIANC (World Association for Waterborne Transport Infrastructure):** Guidelines for marine fender systems (e.g., PIANC WG33 "Guidelines for the Design of Fenders Systems: 2002" or later)
  - **BS 6349 (British Standard for Maritime Works):** Port design codes for bollards and mooring equipment (e.g., BS 6349-4:2014 "Code of practice for design of fendering and mooring systems")
  - **Local port authority requirements:** Specific calculation methods or safety factors (if applicable)
- **Safety factors per applicable codes** (to be confirmed and stated in § 1.2 Design Basis).

## Verification

**Verification methods for Calculation deliverables (per `Procedure.md`):**

| Method | Applicability | Criteria | Procedure § |
|--------|---------------|----------|-------------|
| Independent check | All calculations | Methodology appropriate; inputs correctly applied; arithmetic correct; results reasonable; code compliance demonstrated | Proc § Step 6 |
| Software output verification | If software used | Output reasonableness verified; benchmark comparison performed (if applicable) | Proc § Step 5 |
| Design code compliance | All | Factors, methods, load cases per applicable codes (PIANC, BS 6349, etc.) | Proc § Steps 3, 4, 5 |
| Sensitivity checks | As applicable | Key input sensitivity evaluated (e.g., temperature effect on fender stiffness, line angle effect on bollard load) | Proc § Step 5 (optional) |
| Cross-check with data sheets | All | Results consistent with DEL-09.04 data sheet values (fender reactions, bollard SWL) | Proc § Step 7 |

**Acceptance criteria (per `Datasheet.md § Acceptance`):**
- Calculations cover all decomposition-listed artifacts (fender reaction + bollard load).
- All calculation sections per § 1 (Purpose, Design Basis, Inputs, Methods, Load Cases, Results, Check Record) are complete.
- Key assumptions and inputs are stated and traceable to sources or labeled ASSUMPTION with basis.
- Calculation results are consistent with DEL-09.04 data sheet values.
- Calculation results substantiate DEL-09.02 specification performance requirements (§ 2.1, 2.2).
- Interface loads to PKG-08 Marine Structures are documented.
- Independent check record is included with checker sign-off.

## Documentation

**Required documentation outputs (per decomposition and `Datasheet.md`):**
- Fender reaction calculations
- Bollard load calculations
- (May be combined into a single calculation package or separate calculation packages, depending on project document control preferences)

**Documentation requirements:**
- All documents shall comply with project document control procedures.
- Revision control per project numbering system — **TBD**.
- Format: **TBD** — **ASSUMPTION:** PDF for issue/record; native format (Excel, software files) for working files and reproducibility.
- Records management per `Procedure.md § Records`.
