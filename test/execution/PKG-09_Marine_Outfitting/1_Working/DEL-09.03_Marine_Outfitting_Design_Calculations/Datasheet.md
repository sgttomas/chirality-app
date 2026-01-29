# Datasheet: DEL-09.03 Marine Outfitting Design Calculations

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-09.03 |
| Name | Marine Outfitting Design Calculations |
| Package | PKG-09 Marine Outfitting |
| Discipline | Marine |
| Type | Calculation |
| Responsible | D&B Contractor |
| Status | INITIALIZED |

## Scope (Decomposition)

**Package scope (PKG-09):** Fenders, bollards, ladders, life-saving equipment, existing Berth 10 upgrades and repairs. (**Source:** Decomposition, PKG-09)

**Deliverable intent (DEL-09.03):** Provides the engineering basis and sizing/verification calculations for marine outfitting. (**Source:** Decomposition, DEL-09.03 row)

**Anticipated artifacts (from decomposition):**
- Fender reaction calculations
- Bollard load calculations

## Deliverable Attributes (Calculation Package)

| Attribute | Value |
|-----------|-------|
| Calculation package/numbering | **TBD** — per project document control procedure |
| Software used | **TBD** — **ASSUMPTION:** Hand calculations, Excel spreadsheet, or specialized marine engineering software (e.g., SACS, ANSYS) depending on complexity |
| Calculation method(s) | **TBD** — **ASSUMPTION:** Code-based methods per PIANC, BS 6349, or equivalent |
| Design code(s)/standard(s) | **TBD** — to be extracted from Employer's Requirements; **ASSUMPTION:** PIANC guidelines for fenders, BS 6349 for bollards |
| Load cases / combinations | **TBD** — normal mooring, storm mooring, emergency breakaway (bollards); design berthing energy at various deflections (fenders) |
| Revision | **TBD** — per project revision scheme |
| Classification | **TBD** — **ASSUMPTION:** Design calculations (for construction and as-built record) |

## Calculation Checklist (Minimum)

Each calculation corresponds to requirements in `Specification.md § 2` and has corresponding rationale in `Guidance.md` and procedural steps in `Procedure.md`.

| Calculation | Specification § | Guidance § | Procedure Step | Content | Status |
|-------------|-----------------|------------|----------------|---------|--------|
| Fender reaction calculations | SPEC § 2.1 | Guidance § Principles (Fender Calculations) | Proc Step 5 | Reaction forces at design deflection; verify structure capacity per PKG-08 allowable; substantiate DEL-09.02 § 2.1 requirements | **TBD** — pending DEL-08.06, DEL-08.07 inputs |
| Bollard load calculations | SPEC § 2.2 | Guidance § Principles (Bollard Calculations) | Proc Step 5 | Design loads from mooring analysis; required SWL with factors; verify selected bollard/foundation capacity; substantiate DEL-09.02 § 2.2 requirements | **TBD** — pending DEL-08.09 inputs |

## Related Deliverables (PKG-09 and PKG-08)

This calculation deliverable bridges upstream design inputs (PKG-08 analyses) and downstream equipment selection/substantiation (PKG-09 data sheets and specifications).

| Deliverable | Relationship | Interface Point |
|-------------|--------------|-----------------|
| DEL-08.06 Berthing Energy Calculation Report | **Input** — berthing energy basis for fender selection | Primary input for fender reaction calculation; provides design berthing energy (kJ), vessel characteristics, approach velocity |
| DEL-08.07 Fender System Deflection Characteristics Data Package | **Input** — fender performance data | Primary input for fender reaction calculation; provides deflection/reaction curves for selected fender system |
| DEL-08.08 Fender Supplier Design Verification Letter/Report | **Input** — fender suitability confirmation | Supplementary input for fender calculation validation |
| DEL-08.09 Mooring Analysis Report | **Input** — mooring line loads for bollard capacity | Primary input for bollard load calculation; provides mooring line loads (kN) under normal, storm, emergency conditions |
| DEL-08.03 Marine Structures Design Calculations | **Coordination** — structural capacity verification | Interface loads (fender reactions, bollard loads) must be within PKG-08 structural capacity |
| DEL-09.02 Marine Outfitting Technical Specification | **Substantiation** — calculations verify specification requirements | Calculations demonstrate compliance with performance requirements in DEL-09.02 § 2.1, 2.2 |
| DEL-09.04 Marine Outfitting Data Sheet Package | **Output** — calculation results populate data sheets | Fender reaction values and bollard capacity values from calculations substantiate DEL-09.04 data sheets |
| DEL-09.01 Marine Outfitting Design Drawing Set | **Coordination** — geometry and arrangement | Bollard arrangement, line angles, fender locations from drawings inform calculation assumptions |

## Inputs / Dependencies (NOT_TRACKED)

Dependencies are coordinated externally (see `execution/_Coordination/_COORDINATION.md`). Required inputs:

| Input | Source | Specification § | Guidance § | Required For | Status |
|-------|--------|-----------------|------------|--------------|--------|
| Berthing energy results | DEL-08.06 | SPEC § 2.1 | Guidance § Principles (Fender Calculations) | Fender selection/verification — design energy (kJ), vessel characteristics, approach velocity, environmental conditions | **TBD** |
| Fender deflection/reaction curves | DEL-08.07, Vendor | SPEC § 2.1 | Guidance § Principles (Fender Calculations) | Fender reaction calculation — reaction force vs deflection curve for selected fender system | **TBD** |
| Fender supplier verification | DEL-08.08 | SPEC § 2.1 | Guidance § Principles (Fender Calculations) | Fender suitability confirmation — validates fender performance data and applicability | **TBD** |
| Mooring line loads | DEL-08.09 | SPEC § 2.2 | Guidance § Principles (Bollard Calculations) | Bollard capacity calculation — mooring line loads (kN) under normal, storm, emergency conditions | **TBD** |
| Design vessel characteristics | Employer's Requirements | SPEC § 1.2 | — | Both calculations — vessel type, LOA, beam, displacement, mooring configuration | **TBD** |
| Environmental conditions | Employer's Requirements | SPEC § 1.2 | — | Load cases — wind, current, wave, tidal range, temperature range | **TBD** |
| Marine structure geometry and support conditions | PKG-08 outputs (DEL-08.01, DEL-08.03) | SPEC § 3 | Guidance § Considerations (Interface loads) | Interface loads — fender/bollard mounting locations, structural capacities, allowable reaction forces | **TBD** |
| Safety factors and acceptance criteria | Employer's Requirements / Codes | SPEC § 1.2, Standards | Guidance § Principles (Evidence Rules) | Capacity verification — load factors, safety factors per codes (e.g., BS 6349, PIANC) | **TBD** |

## Outputs (Minimum)

| Output | Content | Specification § | Datasheet Checklist | Status |
|--------|---------|-----------------|---------------------|--------|
| Fender reaction calculation package | Inputs (berthing energy, fender data), assumptions, methodology, reaction at design deflection(s), comparison to allowable structural capacity, conclusions | SPEC § 1, 2.1 | Fender reaction calculations row | **TBD** |
| Bollard load calculation package | Inputs (mooring loads, load cases), assumptions, methodology, required SWL with factors, comparison to selected bollard rating, foundation capacity verification (if applicable), conclusions | SPEC § 1, 2.2 | Bollard load calculations row | **TBD** |

**Output consistency:** Calculation results shall be consistent with values stated in DEL-09.04 data sheets (fender reaction force, bollard SWL) and DEL-09.02 specification requirements.

## Acceptance (Definition of Done)

- Calculations cover all decomposition-listed artifacts for DEL-09.03 (fender reaction calculations, bollard load calculations).
- All calculation sections per `Specification.md § 1` (Purpose, Design Basis, Inputs, Methods, Load Cases, Results, Check Record) are complete.
- All assumptions are stated and traceable to sources or flagged **ASSUMPTION** with basis for engineering judgment.
- All inputs are referenced with document number, revision, and date (per `Specification.md § 4` traceability requirements).
- Calculation results are consistent with DEL-09.04 data sheet values (fender reactions, bollard capacities).
- Calculation results demonstrate compliance with DEL-09.02 specification performance requirements (§ 2.1, 2.2).
- Interface loads to PKG-08 Marine Structures are documented for coordination.
- Independent check completed and documented per `Procedure.md § Step 6` with checker sign-off.
- Cross-document consistency verified with `Specification.md`, `Guidance.md`, and `Procedure.md`.

## References

- `Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` (PKG-09 scope; DEL-09.03 definition)
- `_REFERENCES.md` (this deliverable) — lists applicable reference documents
- `Specification.md` (DEL-09.03) — requirements governing this datasheet
- `Guidance.md` (DEL-09.03) — rationale and calculation considerations
- `Procedure.md` (DEL-09.03) — production/verification process
