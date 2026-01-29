# Guidance: DEL-04.01 Pavement Design Drawing Set

## Purpose

This guidance clarifies how to review and coordinate the Pavement Design Drawing Set (DEL-04.01) to ensure:
- Every plan, section, and interface annotation aligns with the specification (DEL-04.02), calculations (DEL-04.03), and test records (DEL-04.04)
- OBJ-8 future-expansion provisions are visible and dimensioned for Phase 2 continuity
- Cross-document consistency is maintained across Datasheet, Specification, Guidance, and Procedure
- **ASSUMPTION** and **TBD** items are properly logged and tracked for resolution

## Principles

### P1: Traceability as Foundation
Every element shown on drawings must be traceable to either:
- A specification clause in DEL-04.02 (for materials, tolerances, workmanship)
- A calculation output in DEL-04.03 (for layer thicknesses, load capacities, design parameters)
- An Employer's Requirement reference (for performance criteria, standards, acceptance)
- An explicit **ASSUMPTION** or **TBD** notation (when source data is pending)

**Rationale**: Traceability prevents unvalidated design elements from entering construction and enables efficient change management when upstream inputs are revised.

### P2: Interface Coordination is Non-Negotiable
Pavement design interfaces with multiple disciplines:
- **PKG-03** (Underground Utilities): Surface drainage slopes must tie into catch basin invert elevations
- **PKG-05** (Concrete Structures): Pavement grades at building perimeters must match finished floor elevations
- **PKG-07** (Rail Works): Pavement elevations at rail crossings must accommodate track top-of-rail and maintain clearances
- **PKG-08** (Marine Structures): Pavement termination at wharf edge must coordinate with berth elevations and loading arm swing radii

**Rationale**: Interface mismatches discovered during construction cause costly rework. Early coordination via drawing review cycles prevents conflicts.

### P3: Future Expandability Must Be Explicit (OBJ-8)
Phase 2 expansion provisions require:
- Reserved pavement corridors shown with dimensional envelopes (width, elevation range)
- Tie-in points marked with coordinates and assumed grades (flagged as **ASSUMPTION** until Phase 2 design)
- Structural pavement sections designed for ultimate Phase 2 loads (even if initial Phase 1 use is lighter)
- Utility stub-outs and drainage capacity allowances shown on interface drawings

**Rationale**: OBJ-8 Future Expandability is a project objective. Retrofitting pavement for Phase 2 is more costly than designing for ultimate capacity initially. Explicit callouts prevent oversight.

### P4: Assumptions and TBDs Drive Review Efficiency
Every **ASSUMPTION** and **TBD** on drawings must have:
- Clear description (what is assumed or unknown)
- Impact scope (which deliverables or packages are affected)
- Resolution path (who confirms, what input is needed, by when)
- Tracking ID (cross-referenced in Procedure assumption log)

**Rationale**: Untracked assumptions become hidden risks. Flagging them explicitly enables prioritization and ensures resolution before issuance.

## Considerations

### Design Iteration Management
- **When to iterate**: DEL-04.03 calculation revisions (e.g., refined geotechnical data, revised loading assumptions) trigger drawing updates to maintain consistency. Procedure Step 4 governs coordination.
- **Version control**: Each drawing revision updates the revision history table and triggers Guidance re-review per Specification R3.3.
- **Communication**: Notify DEL-04.02 and DEL-04.04 teams when drawing revisions affect material call-outs or test acceptance criteria.

### Scale and Detail Selection
- **Plan sheet scale**: Balance readability (large enough to show dimensions clearly) with coverage (minimize sheet count). Typical scales: 1:500 to 1:1000 for site plans, 1:100 to 1:250 for detail plans.
- **Section scale**: Exaggerated vertical scale (e.g., H=1:100, V=1:10) may be used to clarify thin layers, but must be clearly noted to avoid misinterpretation.
- **Detail enlargements**: Provide enlarged details (1:20, 1:10, 1:5) for complex joints, transitions, or interface conditions that cannot be shown clearly at plan scale.

### Material Call-Out Precision
- **Generic vs. specific**: Use generic terms ("Asphalt Concrete Wearing Course") on drawings with reference to DEL-04.02 specification clause for detailed mix design. Avoid specifying proprietary products on drawings unless sole-sourced per Employer's Requirements.
- **Tolerance notation**: State tolerances explicitly (e.g., "±10 mm thickness", "±0.5% grade") rather than relying on "standard practice" assumptions. Reference DEL-04.02 for acceptance criteria.

### CAD Layer and File Management (**TBD** – pending project CAD standards)
- **Layer naming**: Use consistent layer naming per project CAD manual (e.g., "PAVE-ASPH", "PAVE-CONC", "PAVE-MARK" for different pavement elements).
- **File naming**: Follow project drawing numbering system (e.g., "DEL-04.01-C-001-PLAN.dwg"). Confirm format from drawing management plan.
- **External references (XREFs)**: Coordinate base map XREFs with PKG-03, PKG-05, PKG-07, PKG-08 to avoid duplicate geometry and maintain interface consistency.

## Review Checklist

### Pre-Review Preparation
- [ ] Confirm Datasheet Assumptions & TBDs are current (review Datasheet "Assumptions & TBDs" section)
- [ ] Obtain latest DEL-04.03 calculation outputs for section thickness verification
- [ ] Obtain latest DEL-04.02 specification draft for material call-out cross-checking
- [ ] Review Procedure assumption log to identify open items affecting drawings

### Step 1: Plan Completeness (Specification R1.1)
- [ ] **Coverage**: All pavement zones listed in Datasheet "Drawing Scope" are shown on plan sheets (asphalt, concrete, curbs, sidewalks, parking, line marking)
- [ ] **Extents**: Pavement boundaries are dimensioned with tie-in points to adjacent packages (PKG-03, PKG-05, PKG-07, PKG-08)
- [ ] **Phase 2 provisions**: OBJ-8 expansion corridors are shown with dimensional envelopes and labeled as future tie-in zones
- [ ] **Coordinate references**: Plan shows coordinate grid, benchmark elevations, and references to site survey control points
- [ ] **Scale verification**: Scale bar is present, scale notation is correct, and plan is legible at stated scale
- [ ] **Missing elements**: Any zones not shown are noted as **TBD** with explanation in Procedure assumption log

### Step 2: Section Verification (Specification R1.2)
- [ ] **Thickness validation**: Layer thicknesses shown on section drawings match DEL-04.03 calculation outputs (verify by cross-checking calculation sheet references)
- [ ] **Material call-outs**: Each layer (wearing course, binder, base, subbase) references the corresponding DEL-04.02 specification clause
- [ ] **Subgrade requirements**: Subgrade preparation (compaction, CBR, proof rolling) is annotated and consistent with DEL-04.02 and DEL-04.03 design assumptions
- [ ] **Joint details**: Construction joints, expansion joints, control joints are detailed with spacing, sealant, and dowel/tie bar requirements (if applicable)
- [ ] **Drainage provisions**: Cross-slopes and longitudinal slopes are noted; tie-ins to PKG-03 catch basins are shown with inverts
- [ ] **Tolerances**: Thickness, grade, and smoothness tolerances are stated and consistent with DEL-04.02 acceptance criteria
- [ ] **Unresolved items**: Any sections pending DEL-04.03 final calculations are flagged as **TBD** on drawing notes

### Step 3: Line Marking & Notes (Specification R1.3)
- [ ] **Legend completeness**: Line marking legend includes all striping types (centerline, edge line, parking stalls, pedestrian crossings, directional arrows)
- [ ] **Material specifications**: Legend references DEL-04.02 for paint vs. thermoplastic material selection, color, and reflectivity
- [ ] **Dimensions**: Parking stall dimensions, traffic lane widths, and striping widths are stated
- [ ] **Application notes**: Environmental constraints (temperature, humidity) and surface preparation requirements reference DEL-04.02
- [ ] **Consistency check**: Line marking shown on plans matches legend descriptions; no unmarked or mislabeled features

### Step 4: Interface & OBJ-8 Callouts (Specification R1.4)
- [ ] **PKG-03 interfaces**: Surface drainage slopes tie into catch basin locations and invert elevations (coordinate with DEL-03.01 drawings)
- [ ] **PKG-05 interfaces**: Pavement grades at building perimeters match structure finished floor elevations (coordinate with DEL-05.01 drawings)
- [ ] **PKG-07 interfaces**: Pavement elevations at rail crossings accommodate track top-of-rail and clearance envelopes (coordinate with DEL-07.01 drawings)
- [ ] **PKG-08 interfaces**: Pavement termination at marine structure boundaries coordinates with berth elevations (coordinate with DEL-08.01 drawings)
- [ ] **Phase 2 callouts**: Reserved corridors for OBJ-8 expansion are dimensioned and annotated with assumed tie-in elevations (flagged as **ASSUMPTION** until Phase 2 input received)
- [ ] **Assumption logging**: All interface assumptions are logged in Procedure assumption log with coordination status and resolution path

### Step 5: Document Control Review (Specification R1.5)
- [ ] **Title block**: Project name, deliverable ID (DEL-04.01), sheet number, revision number, date are correct
- [ ] **Drawing list**: Index sheet lists all drawing sheets with current revision status
- [ ] **Revision history**: Revision history table is complete with revision number, date, description, and approval signatures
- [ ] **Reference table**: Applicable specifications (DEL-04.02), calculations (DEL-04.03), and Employer's Requirements sections are listed
- [ ] **Legend & notes**: General notes sheet includes material symbols, abbreviations, standard details, and safety warnings (if applicable)
- [ ] **Procedure verification**: Drawing set conforms to Procedure Step 5 QA checklist

### Step 6: Traceability Audit (Specification R2.1, R2.2, R2.3)
- [ ] **Specification references**: Every material call-out and tolerance on drawings references a DEL-04.02 clause (use Procedure traceability matrix to verify)
- [ ] **Calculation references**: Layer thicknesses and design parameters reference DEL-04.03 calculation sheets (use Procedure traceability matrix to verify)
- [ ] **Test record references**: Drawing notes identify elements requiring field verification per DEL-04.04 (e.g., "Compaction testing per DEL-04.04")
- [ ] **Cross-document consistency**: Terminology, entity names, and values are consistent across Datasheet, Specification, Guidance, Procedure

## Trade-offs

### Depth of Detail vs. Construction Flexibility
**Trade-off**: Highly detailed drawings reduce contractor uncertainty but may constrain means-and-methods flexibility. Less detailed drawings allow contractor optimization but increase risk of non-conformance to design intent.

**Guidance**:
- Specify performance requirements (e.g., "achieve 95% compaction per DEL-04.02") rather than prescriptive methods where Employer's Requirements allow flexibility
- Detail critical interfaces (structure transitions, utility crossings) to prevent conflicts
- Use notes like "Contractor to submit construction sequence plan for approval" when flexibility is appropriate
- Reference DEL-04.02 for workmanship standards rather than repeating specification text on drawings

### Sheet Count vs. Clarity
**Trade-off**: Minimizing sheet count reduces document management burden but may result in crowded, hard-to-read drawings. More sheets improve clarity but increase coordination effort.

**Guidance**:
- Prioritize readability: If a plan sheet is too crowded to dimension clearly, split into multiple sheets at logical boundaries
- Use match lines for large sites to maintain continuity across sheets
- Group related details on single detail sheets to reduce sheet proliferation
- Balance per project norms (typical EPC projects: 10-20 sheets for pavement package of this scope – **ASSUMPTION**)

### Standardization vs. Site-Specific Optimization
**Trade-off**: Using standard pavement sections (e.g., OPSS/MMCD typical sections) accelerates design but may not optimize for site-specific soil conditions or loading. Custom-designed sections match site conditions but require more analysis (DEL-04.03 effort).

**Guidance**:
- Start with standard sections as baseline (reference TAC Pavement Design Manual or MMCD typical sections)
- Validate with DEL-04.03 calculations using site-specific geotechnical data
- Adjust layer thicknesses as needed based on DEL-04.03 outputs
- Document deviations from standards in drawing notes and Procedure assumption log

## Coordination Guidance

### Internal PKG-04 Coordination
- **DEL-04.02 coordination**: Notify specification author when drawings introduce new materials or revise tolerances (requires specification update per Specification R2.1)
- **DEL-04.03 coordination**: Share layout assumptions and loading scenarios with calculation lead; schedule coordination meeting after DEL-04.03 draft completed to review section thickness outputs (Procedure Step 4)
- **DEL-04.04 coordination**: Provide final issued drawing set to QA/QC team as basis for test planning; identify critical test locations on drawings (e.g., heavy load zones, transition areas)

### Cross-Package Coordination
- **PKG-03 coordination**: Share surface drainage slopes and catch basin tie-in elevations; request invert elevations and rim elevations from DEL-03.01 drawings
- **PKG-05 coordination**: Request finished floor elevations and structure pad elevations from DEL-05.01 drawings; confirm pavement grades at building perimeters
- **PKG-07 coordination**: Request track top-of-rail elevations and clearance envelopes from DEL-07.01 drawings; coordinate rail crossing details and embedment zones
- **PKG-08 coordination**: Request berth elevations and wharf edge details from DEL-08.01 drawings; confirm pavement termination limits and loading arm swing radii clearances

### Owner/Engineer Coordination
- **Employer's Requirements clarification**: If ER pavement requirements are ambiguous or incomplete, prepare Request for Information (RFI) with specific questions and proposed interpretations (log as **TBD** in Procedure assumption log until resolved)
- **Geotechnical data**: Request site-specific geotechnical investigation report (soil bearing capacity, CBR, groundwater levels) for DEL-04.03 input and drawing annotation (flagged as **TBD** in Datasheet until provided)
- **Phase 2 expansion input**: Request Phase 2 layout and tie-in elevation assumptions from Owner for OBJ-8 coordination (flagged as **ASSUMPTION** until confirmed)

## Examples

### Example 1: Pavement Section Annotation (Good Practice)
```
SECTION A-A: HEAVY DUTY ASPHALT PAVEMENT
- 50 mm Asphalt Concrete Wearing Course (DEL-04.02 Clause 3.2.1)
- 100 mm Asphalt Concrete Binder Course (DEL-04.02 Clause 3.2.2)
- 150 mm Granular Base Course (DEL-04.02 Clause 3.3.1)
- 300 mm Granular Subbase Course (DEL-04.02 Clause 3.3.2)
- Subgrade: Compact to 95% Standard Proctor (DEL-04.02 Clause 3.1.1)
- Layer thicknesses validated by DEL-04.03 Calculation Sheet C-001
- Thickness tolerance: ±10 mm (DEL-04.02 Clause 4.2.1)
- Field verification per DEL-04.04 (compaction testing, core sampling)
```

**Why this works**: Every material references DEL-04.02, thicknesses reference DEL-04.03, test requirements reference DEL-04.04. Tolerances are explicit. Traceability is complete.

### Example 2: Phase 2 Expansion Callout (OBJ-8)
```
FUTURE PHASE 2 EXPANSION CORRIDOR
- Reserved pavement envelope: 12 m width × 200 m length (see Plan Sheet C-003)
- Assumed tie-in elevation: 5.50 m (geodetic) – ASSUMPTION pending Phase 2 design
- Design pavement section for ultimate Phase 2 loading (per DEL-04.03 Case 2)
- Coordinate with Phase 2 team before finalizing tie-in details
- Refer to Procedure Assumption Log ID: A-04.01-015
```

**Why this works**: Dimensional envelope is clear, assumption is flagged, responsibility for resolution is stated, traceability to assumption log is provided.

### Example 3: Interface Note to PKG-03 (Drainage Coordination)
```
INTERFACE NOTE: PKG-03 DRAINAGE TIE-IN
- Surface drainage slope: 2.0% toward catch basin CB-101 (see DEL-03.01 Sheet D-005)
- Catch basin rim elevation: 5.75 m (geodetic) – coordinate with DEL-03.01
- Pavement surface elevation at tie-in: 5.80 m (geodetic)
- Verify CB-101 invert elevation accommodates slope from adjacent zones
- Assumption Log ID: A-04.01-022 (pending DEL-03.01 final issue)
```

**Why this works**: Interface elevation is stated, coordination requirement is explicit, reference to adjacent package deliverable (DEL-03.01) is provided, assumption tracking is in place.

## References

### Source Documents
- **Decomposition**: `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`, Section PKG-04, DEL-04.01, OBJ-8
- **Datasheet (DEL-04.01)**: Attributes, Conditions, Construction, Assumptions & TBDs, Cross-document Coordination
- **Specification (DEL-04.01)**: Requirements R1.1–R1.5, R2.1–R2.3, R3.1–R3.3, Verification Methods, Standards
- **Procedure (DEL-04.01)**: Workflow Steps, Controls, traceability matrix, assumption log
- **DEL-04.02**: Pavement Technical Specification (material and workmanship references)
- **DEL-04.03**: Pavement Design Calculations (section thickness validation)
- **DEL-04.04**: Pavement Installation & Test Records (field verification basis)

### Industry References (**ASSUMPTION** – pending ER confirmation)
- **TAC Pavement Design and Rehabilitation Manual**: Design methodology guidance
- **OPSS or MMCD**: Standard pavement section details and construction practices
- **CSA A23.1/A23.2**: Concrete materials and testing standards (if applicable)
