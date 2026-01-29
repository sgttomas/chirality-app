# Datasheet: DEL-31.01 Record Design Drawing Set

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-31.01 |
| Name | Record Design Drawing Set |
| Package | PKG-31 Documentation & Deliverables |
| Discipline | Project Delivery |
| Type | Drawing Set |
| Responsible | D&B Contractor |
| Status | INITIALIZED |

## Attributes

| Attribute | Value |
|-----------|-------|
| Drawing Set Type | Record Design Drawings |
| Scope | All disciplines (Civil, Structural, Mechanical, Process, Electrical, I&C, Marine, Buildings, Fire Protection) |
| Drawing Standard | VFPA (Vancouver Fraser Port Authority) standards |
| Format | **TBD** — **ASSUMPTION**: CAD format per VFPA requirements (likely AutoCAD .dwg or similar) |
| Coordinate System | **TBD** — **ASSUMPTION**: BC Albers or project-specific coordinate system per VFPA requirements |
| Drawing Numbering | **TBD** — Per project drawing numbering system |
| Revision Control | Per project document control procedures |
| Classification | **ASSUMPTION**: For Official Use (project documentation) |

**Source:** _CONTEXT.md; Decomposition DEL-31.01 (line 686)

## Conditions

**Purpose and Context:**

Record Design Drawings represent the final approved design as it was intended to be constructed. These drawings:
- Document the design intent and specifications for all facility systems and components
- Serve as the baseline for construction activities
- Provide reference for future modifications and lifecycle management
- Support OBJ-1 (Safe & Reliable Operation) and OBJ-9 (Lifecycle Cost Optimization)

**Source:** Decomposition Section 2 (Project Objectives), lines 59 and 67

**Applicable Conditions:**

- Project: Canola Oil Transload Facility — Phase 1 (Design & Build)
- Location: Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC
- Facility Capacity: 1,000,000 MT/annum throughput; 45,000 MT storage
- Regulatory Authority: VFPA (Vancouver Fraser Port Authority)
- Design Standards: Per Employer's Requirements and applicable codes
- Environmental Classification: Marine/industrial environment, Fraser River location

**Source:** README.md (Project snapshot); Decomposition Section 1 (Project Overview)

**Design Life:**
- **TBD** — To be specified per Employer's Requirements and facility asset management strategy

## Construction

**Drawing Set Composition:**

The Record Design Drawing Set shall include drawings from all project disciplines:

1. **Site & Civil Drawings:**
   - Site plans, grading, drainage, pavement, rail works
   - **ASSUMPTION**: Package scope DEL-04.01 through DEL-07.01 drawing outputs

2. **Marine Structures Drawings:**
   - Wharf, berth, and marine infrastructure
   - **ASSUMPTION**: Package scope DEL-08.01 and DEL-09.01 drawing outputs

3. **Structural Drawings:**
   - Concrete structures, structural steel, building structures
   - **ASSUMPTION**: Package scope DEL-05.01 and DEL-06.01 drawing outputs

4. **Storage Tank Drawings:**
   - Tank design, foundations, appurtenances
   - **ASSUMPTION**: Package scope DEL-13.01 drawing outputs

5. **Process & Mechanical Drawings:**
   - Piping, equipment layouts, P&IDs, mechanical systems
   - **ASSUMPTION**: Package scope DEL-10.01, DEL-11.01, DEL-12.01, DEL-14.01, DEL-15.01, DEL-16.01 drawing outputs

6. **Electrical & I&C Drawings:**
   - Power distribution, lighting, control systems, instrumentation
   - **ASSUMPTION**: Package scope DEL-17.01, DEL-18.01, DEL-19.01 drawing outputs

7. **Fire Protection & Safety Drawings:**
   - Fire detection, suppression, safety systems
   - **ASSUMPTION**: Package scope DEL-23.01, DEL-24.01 drawing outputs

8. **Building Drawings:**
   - Modular buildings, MEP systems
   - **ASSUMPTION**: Package scope DEL-25.01, DEL-26.01 drawing outputs

**Drawing Standards and Conventions:**

- All drawings shall conform to VFPA drawing standards and requirements
- **TBD** — Specific VFPA drawing standard reference document
- Drawing title blocks, stamps, and signatures per project procedures
- Layer naming, line weights, and symbology per VFPA/project standards
- **TBD** — Scale requirements and sheet sizes

**Deliverable Format:**

- Electronic format: **TBD** — **ASSUMPTION**: CAD native files plus PDF
- Hard copy requirements: **TBD** — Per Employer's Requirements
- Transmittal format: Per project document control procedures

## References

- `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` — Decomposition, Section 5 (PKG-31), line 686
- `_CONTEXT.md` — Deliverable identity and description
- `_REFERENCES.md` — Applicable reference documents (to be populated)
- Employer's Requirements Volume 2 Part 1 — **TBD** — Specific section references for record drawing requirements
- VFPA Drawing Standards — **TBD** — **location TBD**
- Project Drawing Register — **TBD** — **location TBD**
- Cross-references: See `_DEPENDENCIES.md` (NOT_TRACKED — dependencies coordinated externally)

**Supporting Project Objectives:**
- OBJ-1: Safe & Reliable Operation (Decomposition line 780)
- OBJ-9: Lifecycle Cost Optimization (Decomposition line 788)
