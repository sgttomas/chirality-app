# Datasheet: DEL-31.02 As-Built Design Drawing Set

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-31.02 |
| Name | As-Built Design Drawing Set |
| Package | PKG-31 Documentation & Deliverables |
| Discipline | Project Delivery |
| Type | Drawing Set |
| Responsible | D&B Contractor |
| Status | INITIALIZED |

## Attributes

| Attribute | Value |
|-----------|-------|
| Drawing Set Type | As-Built Drawings |
| Scope | All disciplines (Civil, Structural, Mechanical, Process, Electrical, I&C, Marine, Buildings, Fire Protection) |
| Drawing Standard | VFPA (Vancouver Fraser Port Authority) standards |
| Baseline | Record Design Drawing Set (DEL-31.01) with construction markups and deviations incorporated |
| Format | **TBD** — **ASSUMPTION**: CAD format per VFPA requirements (likely AutoCAD .dwg or similar) |
| Coordinate System | **TBD** — **ASSUMPTION**: Same as Record Drawings (BC Albers or project-specific coordinate system per VFPA requirements) |
| Drawing Numbering | **ASSUMPTION**: Same drawing numbers as Record Drawings with "As-Built" designation or per project numbering convention |
| Revision Control | Per project document control procedures |
| Classification | **ASSUMPTION**: For Official Use (project documentation and operations reference) |

**Source:** _CONTEXT.md; Decomposition DEL-31.02 (line 687)

## Conditions

**Purpose and Context:**

As-Built Drawings represent the facility as actually constructed, reflecting:
- The approved design from Record Drawings (DEL-31.01)
- Field changes, deviations, and modifications made during construction
- Actual installed conditions, dimensions, and configurations
- Final equipment locations, routing, and connections

As-Built drawings serve as:
- The definitive record of the constructed facility for operations and maintenance (DEL-31.03, DEL-31.04)
- Baseline for future modifications, expansions (OBJ-8), and retrofits
- Reference for facility asset management and lifecycle cost optimization (OBJ-9)
- Regulatory compliance documentation and handover to Employer

**Source:** Decomposition Section 2 (Project Objectives), lines 59, 66-67; **ASSUMPTION** per industry practice for as-built documentation

**Applicable Conditions:**

- Project: Canola Oil Transload Facility — Phase 1 (Design & Build)
- Location: Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC
- Facility Capacity: 1,000,000 MT/annum throughput; 45,000 MT storage
- Regulatory Authority: VFPA (Vancouver Fraser Port Authority)
- Construction Verification: As-built drawings verified against actual field conditions
- Environmental Classification: Marine/industrial environment, Fraser River location

**Source:** README.md (Project snapshot); Decomposition Section 1 (Project Overview)

**Relationship to Record Drawings:**
- As-Built drawings are produced from Record Design Drawings (DEL-31.01) as the baseline
- Construction markups, field measurement data, and change documentation are incorporated
- As-Built drawings supersede Record Drawings as the authoritative reference for the constructed facility
- **Source:** **ASSUMPTION** per as-built documentation practice; cross-reference DEL-31.01

**Design Life:**
- **TBD** — To be specified per Employer's Requirements and facility asset management strategy
- As-Built drawings shall remain current throughout facility design life and be updated for major modifications

## Construction

**As-Built Drawing Set Composition:**

The As-Built Drawing Set shall include drawings from all project disciplines, showing final constructed conditions:

1. **Site & Civil As-Builts:**
   - Final grading, drainage, pavement, rail works as-constructed
   - **ASSUMPTION**: Based on Package scope DEL-04.01 through DEL-07.01 record drawings updated with construction markups

2. **Marine Structures As-Builts:**
   - Wharf, berth, and marine infrastructure as-constructed
   - **ASSUMPTION**: Based on Package scope DEL-08.01 and DEL-09.01 record drawings updated with construction markups

3. **Structural As-Builts:**
   - Concrete structures, structural steel, building structures as-constructed
   - **ASSUMPTION**: Based on Package scope DEL-05.01 and DEL-06.01 record drawings updated with construction markups

4. **Storage Tank As-Builts:**
   - Tank design, foundations, appurtenances as-constructed
   - **ASSUMPTION**: Based on Package scope DEL-13.01 record drawings updated with construction markups

5. **Process & Mechanical As-Builts:**
   - Piping, equipment layouts, P&IDs, mechanical systems as-constructed
   - **ASSUMPTION**: Based on Package scope DEL-10.01, DEL-11.01, DEL-12.01, DEL-14.01, DEL-15.01, DEL-16.01 record drawings updated with construction markups

6. **Electrical & I&C As-Builts:**
   - Power distribution, lighting, control systems, instrumentation as-constructed
   - **ASSUMPTION**: Based on Package scope DEL-17.01, DEL-18.01, DEL-19.01 record drawings updated with construction markups

7. **Fire Protection & Safety As-Builts:**
   - Fire detection, suppression, safety systems as-constructed
   - **ASSUMPTION**: Based on Package scope DEL-23.01, DEL-24.01 record drawings updated with construction markups

8. **Building As-Builts:**
   - Modular buildings, MEP systems as-constructed
   - **ASSUMPTION**: Based on Package scope DEL-25.01, DEL-26.01 record drawings updated with construction markups

**As-Built Documentation Methods:**

- **Field Markups:** Construction team marks up Record Drawings with redlines showing actual installed conditions, deviations, field changes
- **Field Measurements:** Survey and measurement data collected to verify actual dimensions, locations, elevations
- **Change Documentation:** Approved design changes, RFIs, field orders, construction change notices incorporated
- **Photographic Documentation:** **ASSUMPTION**: Field photographs may supplement as-built drawings for critical or complex installations
- **CAD Updates:** Marked-up drawings transferred to CAD for final as-built drawing production
- **Source:** **ASSUMPTION** per typical as-built documentation workflow

**Drawing Standards and Conventions:**

- All drawings shall conform to VFPA drawing standards and requirements
- **TBD** — Specific VFPA drawing standard reference document
- Drawing title blocks updated to indicate "As-Built" status
- As-built changes clearly indicated (e.g., revision clouds, change notes, or per project standards)
- **TBD** — As-built markup and notation conventions per project procedures

**Deliverable Format:**

- Electronic format: **TBD** — **ASSUMPTION**: CAD native files plus PDF
- Hard copy requirements: **TBD** — Per Employer's Requirements
- Transmittal format: Per project document control procedures

## References

- `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` — Decomposition, Section 5 (PKG-31), line 687
- `_CONTEXT.md` — Deliverable identity and description
- `_REFERENCES.md` — Applicable reference documents (to be populated)
- DEL-31.01 Record Design Drawing Set — Baseline for as-built drawings
- Employer's Requirements Volume 2 Part 1 — **TBD** — Specific section references for as-built drawing requirements
- VFPA Drawing Standards — **TBD** — **location TBD**
- Project Drawing Register — **TBD** — **location TBD**
- Construction change documentation (RFIs, field orders, change notices) — **TBD** — **location TBD**
- Commissioning Records (PKG-30) — **TBD** — May provide verification of final installed conditions
- Cross-references: See `_DEPENDENCIES.md` (NOT_TRACKED — dependencies coordinated externally)

**Supporting Project Objectives:**
- OBJ-1: Safe & Reliable Operation (Decomposition line 780) — Accurate as-built documentation supports safe operations
- OBJ-8: Future Expandability (Decomposition line 786) — As-built drawings provide baseline for Phase 2 planning
- OBJ-9: Lifecycle Cost Optimization (Decomposition line 788) — As-built drawings enable effective asset management and maintenance planning
