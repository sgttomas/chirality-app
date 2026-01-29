# Guidance: DEL-09.03 Marine Outfitting Design Calculations

## Purpose

This guidance document supports the development of **Marine Outfitting Design Calculations** for **PKG-09 Marine Outfitting**.

**Decomposition definition (authoritative):** Provides the engineering basis and sizing/verification calculations for marine outfitting. (**Source:** Decomposition, DEL-09.03 row)

This deliverable is classified as a **Calculation** under the **Marine** discipline, to be produced by **D&B Contractor**.

**Downstream use:** Calculations provide the engineering basis for equipment selection and performance verification. They bridge upstream design inputs (PKG-08 analyses) and downstream equipment substantiation (DEL-09.04 data sheets, DEL-09.02 specification compliance demonstration).

## Principles

### Calculation Intent

**Purpose:**
- Provide a clear, checkable engineering basis for selecting and verifying marine outfitting equipment (fenders and bollards) within PKG-09.
- Calculations bridge the gap between:
  - **Upstream inputs:** PKG-08 berthing/mooring analyses (DEL-08.06, DEL-08.09) providing design loads/energies
  - **Downstream outputs:** Equipment selection (DEL-09.04 data sheets) and specification compliance (DEL-09.02 performance requirements)
- Demonstrate compliance with applicable codes and standards (PIANC, BS 6349, or equivalent).
- Document interface loads to PKG-08 Marine Structures for structural capacity coordination.

**Key Principles:**
- **Traceability is paramount:** Every key input should be sourced with document number, revision, date, or labeled TBD/ASSUMPTION.
- **Transparency:** Calculations should be clear enough that an independent checker can verify methodology, inputs, and arithmetic.
- **Reproducibility:** Provide sufficient detail (formulas, inputs, intermediate steps) that calculations can be reproduced if needed.
- **Code compliance:** Follow applicable design codes (PIANC for fenders, BS 6349 for bollards, or as specified by Employer's Requirements).

**Cross-reference:** Calculation structure requirements are defined in `Specification.md § 1`.

### Evidence Rules

**Source Fidelity:**
- Do not invent load cases, safety factors, vessel assumptions, or acceptance criteria — mark **TBD** until sourced from Employer's Requirements and the marine design basis (DEL-08.06, DEL-08.09, codes).
- Cite document number, revision, and date for all external inputs (deliverables, vendor data, codes/standards).
- Label assumptions explicitly as **ASSUMPTION** and flag for approval where engineering judgment is applied without direct source support.

**Traceability:**
- Each input shall reference source: ER clause, deliverable (ID + doc number + revision + section/page), vendor document, code/standard (designation + edition + clause).
- Use input register (per `Procedure.md § Step 2`) to track all inputs with status (received, TBD) and version control.

### Fender Calculations (supports SPEC § 2.1)

**Purpose:** Verify that the selected fender system absorbs the design berthing energy and that the resulting reaction force is within the marine structure's capacity.

**Calculation Methodology:**

**Inputs:**
1. **Berthing energy (E in kJ):** From DEL-08.06 Berthing Energy Calculation Report
   - Design berthing energy is the primary input
   - Berthing energy depends on: vessel characteristics (displacement, block coefficient), approach velocity, berthing angle, added mass coefficient, environmental conditions
   - Extract energy value with citation: document number, revision, section/page
2. **Fender deflection/reaction curve:** From DEL-08.07 Fender System Deflection Characteristics Data Package or vendor data
   - Curve shows relationship between deflection (δ in mm or %) and reaction force (R in kN)
   - Energy absorption: E = ∫ R dδ (area under curve)
   - Extract curve with citation: document number, revision, supplier name
3. **Marine structure allowable load:** From PKG-08 DEL-08.03 Marine Structures Design Calculations
   - Structural capacity to support fender reaction force
   - Extract allowable with citation and coordinate with PKG-08

**Calculation Steps:**
1. Input berthing energy E (kJ) from DEL-08.06
2. Input fender deflection/reaction curve from DEL-08.07 or vendor
3. Determine deflection δ corresponding to energy E:
   - From curve: Find δ where E = ∫ R dδ (area under curve up to δ equals E)
   - May require interpolation or iteration
4. Read reaction R (kN) at deflection δ from curve
5. Apply temperature factor (if applicable):
   - Fender rubber stiffness varies with temperature
   - Check fender manufacturer guidance for temperature correction factors
   - Typical: higher temperature → softer rubber → lower reaction; lower temperature → stiffer rubber → higher reaction
   - **TBD:** Site temperature range and applicability of temperature factors
6. Compare calculated reaction R to marine structure allowable load (from PKG-08)
   - Margin = (Allowable - R) / Allowable × 100%
7. **Conclusion:**
   - R ≤ Allowable → Fender selection is acceptable (structure can support fender loads)
   - R > Allowable → Review fender selection (select fender with lower reaction) or review structural capacity (PKG-08 may need to increase capacity)

**Key Considerations:**
- **Temperature effects:** Site temperature range affects fender rubber stiffness; apply temperature factors per manufacturer guidance if required by codes/ER.
- **Manufacturer's rated performance vs. site-specific factors:** Fender performance data from DEL-08.07 should be for the specific fender model/size selected; verify applicability to site conditions.
- **Multiple fender contact scenarios:** Design vessel list may include multiple vessel sizes; verify fender performance for governing case (typically largest vessel or highest energy case).
- **Fender system vs. individual fender:** If multiple fenders may contact simultaneously, consider load sharing and cumulative reaction (coordinate with DEL-08.06 berthing energy analysis assumptions).

**Output:**
- Fender reaction summary for DEL-09.04 data sheets:
  - Fender type and size (e.g., "Cone fender 800H × 1600L")
  - Energy capacity (kJ at rated deflection)
  - Reaction force at design deflection (kN)
  - Comparison to structural allowable (margin %)

**ASSUMPTION:** Fender calculation methodology follows PIANC guidelines or equivalent unless ER specifies alternative method.

### Bollard Calculations (supports SPEC § 2.2)

**Purpose:** Verify that the selected bollard and its foundation can resist the design mooring line loads.

**Calculation Methodology:**

**Inputs:**
1. **Mooring line loads:** From DEL-08.09 Mooring Analysis Report
   - Mooring line loads (kN per line) for each load case:
     - Normal mooring (routine cargo transfer operations)
     - Storm mooring (design environmental conditions without vessel departure)
     - Emergency breakaway (maximum line load before line failure or bollard failure)
   - Extract loads with citation: document number, revision, section/page, load case
2. **Bollard arrangement and line angles:** From DEL-09.01 Marine Outfitting Design Drawing Set (if available)
   - Bollard locations, line angles (horizontal angle, vertical angle)
   - Affects load components and foundation reactions
3. **Design factors:** From applicable codes or Employer's Requirements
   - BS 6349 recommends: Bollard SWL ≥ MBL (minimum breaking load) of largest mooring line
   - Typical design factors: 1.5–2.0 for SWL relative to maximum line load
   - **TBD:** Design factors to be confirmed from codes/ER

**Calculation Steps:**
1. Input mooring line loads from DEL-08.09 for each load case (normal, storm, emergency)
2. Input bollard arrangement and line angles from DEL-09.01 (if available; otherwise assume typical angles)
3. Determine maximum line load (governing case):
   - Typically storm mooring or emergency breakaway produces maximum load
   - Extract maximum line load value (kN)
4. Apply design factor per code:
   - Required SWL = maximum line load × design factor
   - Example: Maximum line load = 500 kN, design factor = 2.0 → Required SWL = 1000 kN (or ~100 tonnes)
5. Compare required SWL to selected bollard rating:
   - Selected bollard SWL (from vendor catalog or DEL-09.04 datasheet)
   - Margin = (Selected SWL - Required SWL) / Required SWL × 100%
6. Verify foundation/anchorage capacity (if bollard mounted on marine structure):
   - Foundation loads: horizontal load, vertical load (from line angles), overturning moment
   - Coordinate with PKG-08 for structural capacity verification (DEL-08.03)
   - Typical foundation types: through-bolt, cast-in anchor, post-installed anchor, grout-filled base plate
   - **TBD:** Foundation type and capacity verification (coordinate with PKG-08)
7. **Conclusion:**
   - Selected SWL ≥ Required SWL → Bollard selection is acceptable
   - Selected SWL < Required SWL → Review bollard selection (select higher capacity bollard)
   - Foundation capacity adequate → Foundation is acceptable
   - Foundation capacity inadequate → Coordinate with PKG-08 for foundation upgrade

**Key Considerations:**
- **Design factors per applicable codes:** BS 6349 recommends SWL ≥ MBL of largest line; some codes/port authorities may have different factors; confirm from ER/codes.
- **Horizontal and vertical load components:** Line angles affect load distribution; vertical loads may be significant if line angle is steep; consider in foundation design.
- **Foundation type:** Through-bolt foundations transfer loads directly to structure; cast-in anchors require coordination with structural concrete pours; post-installed anchors have specific installation and capacity verification requirements.
- **Proof load testing:** Some codes/port authorities require proof load testing of bollards after installation (typically 1.5 × SWL); if required, note in calculation and specify in DEL-09.02 specification.

**Output:**
- Bollard capacity summary for DEL-09.04 data sheets:
  - Bollard type (e.g., "Double horn bollard" or "Tee-head bollard")
  - Safe working load (SWL) rating (kN or tonnes)
  - Required capacity (kN or tonnes)
  - Margin (%)
  - Foundation type (if applicable)

**ASSUMPTION:** Bollard calculation methodology follows BS 6349 or equivalent unless ER specifies alternative method.

## Considerations

### Factors to Consider During Development

| Factor | Consideration | Reference |
|--------|---------------|-----------|
| **Input timing** | Berthing energy analysis (DEL-08.06) and mooring analysis (DEL-08.09) must be completed and matured before finalizing calculations; early draft calculations with preliminary inputs may be possible but require updating when final inputs available | `Datasheet.md § Inputs` |
| **Vendor data** | Fender deflection curves are vendor-specific; fender performance data (DEL-08.07) should be for the specific fender model/size selected; confirm vendor and model before finalizing calculations | — |
| **Interface loads** | Fender reaction forces and bollard loads transfer to marine structure (PKG-08); interface loads must be documented for PKG-08 coordination; PKG-08 structural calculations (DEL-08.03) must confirm structural capacity | `Specification.md § 3` |
| **Existing Berth 10 upgrades** | Upgrades may involve verification of existing bollard foundations or new anchorages for replacement bollards; may require site investigation, capacity assessment of existing elements, retrofit design | — |
| **Temperature range** | Site temperature range affects fender rubber stiffness; check if temperature factors required by codes/ER; consult fender manufacturer guidance | `Guidance.md § Principles (Fender Calculations)` |
| **Multiple vessel sizes** | Design vessel list may include range of vessel sizes; identify governing case (typically largest vessel or highest energy) for fender calculations; verify bollard capacity accommodates largest mooring line loads | — |

### Relationship to Other Deliverables

| Deliverable | Relationship | Flow |
|-------------|--------------|------|
| DEL-08.06 Berthing Energy Calculation Report | **Primary input** for fender sizing | DEL-08.06 provides berthing energy (kJ) → DEL-09.03 calculates fender reaction (kN) |
| DEL-08.07 Fender System Deflection Characteristics Data Package | **Primary input** for fender performance | DEL-08.07 provides fender deflection/reaction curve → DEL-09.03 determines reaction at design energy |
| DEL-08.08 Fender Supplier Design Verification Letter/Report | **Supplementary input** for fender validation | DEL-08.08 confirms fender suitability → DEL-09.03 uses verified fender data |
| DEL-08.09 Mooring Analysis Report | **Primary input** for bollard sizing | DEL-08.09 provides mooring line loads (kN) → DEL-09.03 calculates required bollard SWL |
| DEL-08.03 Marine Structures Design Calculations | **Interface coordination** for structural capacity | DEL-09.03 calculates interface loads (fender reactions, bollard loads) → DEL-08.03 verifies structural capacity |
| DEL-09.01 Marine Outfitting Design Drawing Set | **Input** for geometry and arrangement | DEL-09.01 provides bollard arrangement, line angles → DEL-09.03 uses in bollard load calculation |
| DEL-09.02 Marine Outfitting Technical Specification | **Substantiation** target | DEL-09.03 calculations demonstrate compliance with DEL-09.02 performance requirements (§ 2.1, 2.2) |
| DEL-09.04 Marine Outfitting Data Sheet Package | **Output** destination | DEL-09.03 calculation results (fender reactions, bollard capacities) populate DEL-09.04 data sheets |

## Trade-offs

### Competing Concerns to Evaluate

| Trade-off | Factors | Resolution Approach |
|-----------|---------|---------------------|
| **Conservative vs. optimistic assumptions** | Conservative assumptions (higher factors, worst-case conditions) increase equipment size/cost but provide higher safety margin; optimistic assumptions (lower factors, average conditions) reduce equipment size/cost but risk non-compliance or inadequate capacity | **Recommendation:** Use code-recommended factors and design conditions; document assumptions clearly; obtain approval for assumptions that deviate from codes/ER; balance safety with economy |
| **Calculation method complexity** | Hand calculations are transparent, easy to check, but limited in complexity and may require simplifying assumptions; software calculations can handle more complex scenarios (multiple load cases, non-linear behavior) but may be "black box" and harder to verify | **Recommendation:** Choose method appropriate for calculation complexity; hand calculations or spreadsheet for straightforward cases; software for complex cases; ensure independent checker can verify methodology regardless of method; provide benchmark comparison if using software |
| **Temperature factor application** | Applying temperature factors to fender stiffness increases design margin (accounts for worst-case temperature) but may oversize fenders; not applying factors reduces conservatism but may underestimate reaction in cold conditions | **Recommendation:** Follow fender manufacturer guidance and ER requirements; if ER is silent, apply temperature factors per manufacturer recommendations for site temperature range; document rationale |
| **Multiple vessel sizes** | Calculating for all vessels in design list increases effort and calculation volume but ensures all cases are covered; calculating for governing case only (typically largest vessel) reduces effort but requires engineering judgment to identify governing case | **Recommendation:** Identify governing case based on berthing energy analysis (DEL-08.06 should identify design vessel); verify governing case assumptions with sensitivity check if multiple vessels have similar energies; document vessel list and governing case selection rationale |

## Examples

### Reference Checklists

- Use `Datasheet.md` (Calculation Checklist) as the minimum checklist for this deliverable.
- Use the decomposition's anticipated artifacts as the baseline:
  - Fender reaction calculations
  - Bollard load calculations
- Ensure all calculation sections per `Specification.md § 1` are complete.

### Input Sources

| Input | Source Document | Purpose | Status |
|-------|-----------------|---------|--------|
| Berthing energy | DEL-08.06 Berthing Energy Calculation Report | Primary input for fender sizing; design energy (kJ) | **TBD** |
| Fender performance | DEL-08.07 Fender System Deflection Characteristics Data Package | Primary input for fender reaction; deflection/reaction curve | **TBD** |
| Fender verification | DEL-08.08 Fender Supplier Design Verification Letter/Report | Validation of fender performance data | **TBD** |
| Mooring line loads | DEL-08.09 Mooring Analysis Report | Primary input for bollard sizing; line loads (kN) for normal/storm/emergency cases | **TBD** |
| Design vessel data | Employer's Requirements | Vessel characteristics (LOA, beam, displacement, mooring configuration) | **TBD** — ER clause extraction required |
| Safety factors | Applicable codes (BS 6349, PIANC, etc.) and Employer's Requirements | Design factors for fender/bollard sizing | **TBD** — codes to be confirmed |
| Structural capacity | DEL-08.03 Marine Structures Design Calculations | Allowable loads for interface coordination (fender reactions, bollard loads) | **TBD** — PKG-08 coordination required |

### Typical Calculation Structure

A typical marine outfitting calculation package may follow this structure (adapt as needed for project-specific requirements):

**1. Cover / Title Sheet**
- Document number, revision, date
- Project name, package, deliverable ID
- Originator name, checker name, approver name (with signatures and dates)

**2. Purpose and Scope** (per Specification § 1.1)
- Calculation objective
- Items included and excluded
- Reference to decomposition intent

**3. Design Basis and Assumptions** (per Specification § 1.2)
- Design vessel characteristics
- Environmental conditions
- Safety factors and load factors
- Assumptions (labeled ASSUMPTION where not directly sourced)

**4. Inputs and References** (per Specification § 1.3)
- ER clauses, vendor data, supporting deliverables, drawings, codes/standards
- Input register with source traceability (document number, revision, date)

**5. Methods and Tools** (per Specification § 1.4)
- Calculation method (hand, spreadsheet, software)
- Formulas and code references
- Software verification (if applicable)

**6. Load Cases and Combinations** (per Specification § 1.5)
- Load cases defined
- Load combinations and factors

**7. Calculation Body**
- **7.1 Fender Reaction Calculation**
  - Inputs, methodology, calculations, results
- **7.2 Bollard Load Calculation**
  - Inputs, methodology, calculations, results

**8. Results and Conclusions** (per Specification § 1.6)
- Results summary with units
- Governing load case identification
- Comparison to acceptance criteria / allowable values
- Conclusions and recommendations

**9. Appendices** (as needed)
- Appendix A: Vendor data (fender deflection curves, bollard catalogs)
- Appendix B: Input sheets (extracts from DEL-08.06, DEL-08.07, DEL-08.09)
- Appendix C: Software output (if applicable)

**10. Check Record** (per Specification § 1.7)
- Independent check verification
- Checker identification and sign-off

### Cross-Document Consistency

**Ensure consistency with other DEL-09.03 documents:**
- **Datasheet:** Calculation Checklist items match Specification requirements and Procedure steps.
- **Specification:** All requirements have corresponding rationale in this Guidance document and verification steps in Procedure.
- **Procedure:** All steps reference applicable Specification requirements and Guidance considerations.

**Ensure consistency with related PKG-09 deliverables:**
- **DEL-09.02:** Calculation results substantiate specification performance requirements (§ 2.1, 2.2)
- **DEL-09.04:** Calculation results match data sheet values (fender reactions, bollard SWL)
- **DEL-09.01:** Bollard arrangement and line angles from drawings inform bollard load calculation
