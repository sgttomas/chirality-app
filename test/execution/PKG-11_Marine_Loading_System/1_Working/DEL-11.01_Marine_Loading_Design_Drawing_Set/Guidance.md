# Guidance: DEL-11.01 Marine Loading Design Drawing Set

## Purpose

This guidance document supports the development of **Marine Loading Design Drawing Set** for **PKG-11 Marine Loading System**.

**Deliverable purpose:** Defines the design arrangement and details for the marine loading system, enabling procurement, construction, and commissioning of loading facilities that support safe, reliable, and flexible vessel loading operations at Fraser Surrey Terminal.
**Source:** Decomposition DEL-11.01 description and Section 1 project context.

**Classification:** Drawing deliverable under the Process discipline, produced by the D&B Contractor.
**Source:** Datasheet.md §Identification.

**Objectives context (per decomposition Section 6):**
- **OBJ-1 Safe & Reliable Operation** — drawings communicate safety-critical interfaces (ERC, leak detection, ESD)
- **OBJ-2 Throughput Capacity** — loading arm envelope and pipe sizing support 1,000,000 MT/annum throughput
- **OBJ-4 Operational Flexibility** — operating envelope accommodates diverse vessel sizes
- **OBJ-7 Environmental Protection** — spill containment, double-walled pipe, and leak detection provisions are clearly shown

**Source:** Datasheet.md §Objectives Mapping, Specification.md §Scope.

## Principles

**Engineering rationale (Process discipline — marine loading):**

1. **Safety-first design communication:** The drawing set must clearly convey all safety-critical features—emergency release coupling (ERC) for vessel drift protection, leak detection for spill prevention, and ESD interface points for automated shutdown. These features directly support OBJ-1 Safe & Reliable Operation.
   **Source:** Decomposition PKG-11 scope (ERC, leak detection, ESD); good practice **ASSUMPTION**.

2. **Operability and access:** Loading arm reach envelope and clearance zones must accommodate the full range of design vessel sizes while providing adequate access for operations and maintenance personnel. This supports OBJ-4 Operational Flexibility.
   **Source:** Decomposition OBJ-4; good practice **ASSUMPTION**.

3. **Environmental protection:** Double-walled pipe construction with annulus leak detection provides primary and secondary containment; drawings must clearly show how this protection is achieved and monitored. This supports OBJ-7 Environmental Protection.
   **Source:** Decomposition PKG-11 scope (double-walled pipe, leak detection).

4. **Interface clarity:** Marine loading interfaces with multiple disciplines (marine structures, piping, instrumentation, electrical, civil, building works); clear interface identification reduces coordination errors and supports safe, reliable operation.
   **Source:** Datasheet.md §Interfaces table; good practice **ASSUMPTION**.

**ASSUMPTION:** Design development follows good engineering practice and applicable codes/standards as confirmed by the Employer's Requirements.

**Applicable standards context:**
- OCIMF (Oil Companies International Marine Forum) guidelines for marine loading arms — **TBD** applicability
- API 2610 (Terminal piping design) — **TBD** applicability
- ASME B31.3 (Process piping) — **TBD** applicability
- Project-specific CAD/drafting standards — **TBD**

**Source:** Specification.md §Standards; industry practice **ASSUMPTION**.

## Cross-Document Alignment Notes

| Alignment Check | Datasheet | Specification | Procedure |
|-----------------|-----------|---------------|-----------|
| Anticipated artifacts | §Construction (table with 4 drawing types) | §Scope (4 artifacts listed) / §Documentation | §Steps (Steps 3-6) / §Records |
| Interface list | §Interfaces (8 interfaces) | §Interface Requirements (INT-01 through INT-05) | §Steps Step 1, Step 8 (IDC table with 6 disciplines) |
| Acceptance criteria | §Deliverable Acceptance (6 criteria) | §Verification (6 acceptance criteria) | §Verification (6-item checklist) |
| Standards reference | §References | §Standards (7 standards) | §Prerequisites |
| Package components | §Conditions (6 scope items) | §Scope (6 scope items) | §Steps (Steps 3-6 cover 4 drawing types) |

**Alignment verification (Pass 2/3):**
- Anticipated artifacts: Consistent count of 4 drawing types across all documents
- Interface list: Datasheet shows 8 interfaces; Specification groups into 5 interface requirements (INT-01 through INT-05); Procedure Step 8 IDC table shows 6 disciplines — **consistent coverage**
- Acceptance criteria: All 6 criteria align across Datasheet, Specification, and Procedure
- Standards: 7 standards in Specification.md match references in other documents
- Package components: All 6 PKG-11 scope items consistently referenced

Where ER clause references are not available, items remain explicitly **TBD** (do not infer requirements).

## Considerations

**Factors to consider during drawing development:**

### Safety Considerations
- Emergency release coupling (ERC) position and actuation clearances — supports OBJ-1
- Leak detection sensor visibility and accessibility for maintenance — supports OBJ-1, OBJ-7
- ESD interface points clearly identified for I&C coordination — supports OBJ-1
- Hazardous area classification zones shown where they affect equipment selection/location — **TBD** (coordinate with PKG-27 per Datasheet.md §Conditions)
  **Source:** Specification.md §Requirements REQ-06, REQ-08; Datasheet.md §Conditions.

### Operational Considerations
- Loading arm slew/luff envelope for design vessel range — supports OBJ-4
- Operator shelter location for visibility and access to loading controls — supports OBJ-1, OBJ-4
- Access/egress routes for normal operations and emergency evacuation — supports OBJ-1
- Clearance for fender compression at maximum vessel approach — coordinate with DEL-08.xx Marine Structures
  **Source:** Specification.md §Requirements REQ-06, REQ-09; Datasheet.md §Interfaces.

### Constructability Considerations
- Installation sequence and lifting/handling access
- Foundation interface coordination with marine structures (PKG-08)
- Pipe routing constructability (double-walled pipe fabrication and installation)
- Shelter prefabrication and installation access
  **Source:** Procedure.md §Steps Step 4 (pipe arrangement), Step 6 (shelter); good practice **ASSUMPTION**.

### Environmental Considerations
- Secondary containment provisions (drip trays, sumps, bunding) — supports OBJ-7
- Drainage routing to oil-water separator / containment system — supports OBJ-7
- Annulus leak detection tap point locations for effective coverage — supports OBJ-7
  **Source:** Specification.md §Requirements REQ-07, REQ-08; Decomposition OBJ-7.

### Throughput Considerations
- Loading arm pipe sizing and flow capacity — supports OBJ-2 (1,000,000 MT/annum)
- Double-walled export pipe sizing — supports OBJ-2
- Coordinate with DEL-11.03 design calculations for throughput verification
  **Source:** Decomposition OBJ-2; Datasheet.md §Objectives Mapping.

## Trade-offs

**Competing concerns to evaluate:**

| Trade-off | Option A | Option B | Guidance |
|-----------|----------|----------|----------|
| Detail level vs. schedule | Detailed IFC drawings | Schematic-level for early procurement | Match detail level to project stage and ER requirements (**TBD**) |
| OEM standard vs. site-specific | Accept OEM standard envelope | Require site-specific modifications | Prefer OEM standard where it meets ER (DEL-11.06); minimize custom engineering |
| Operating envelope vs. structure cost | Larger envelope for flexibility | Constrained envelope for smaller platform | Balance against marine structure cost (PKG-08 coordination); supports OBJ-4 |
| Shelter location vs. visibility | Close to loading arm for quick response | Set back for safety | Meet ER requirements for operator protection and visibility (**TBD**); supports OBJ-1 |
| Drawing granularity | Separate drawings per system | Combined multi-system drawings | Balance clarity vs. drawing count; consider maintenance usability |

**ASSUMPTION:** Trade-off evaluation requires engineering judgment based on ER requirements, project stage, and coordination with adjacent packages.

## Examples

**Reference examples and precedents:**

Anticipated drawing deliverables (from decomposition):

| Drawing | Key Content | Source Reference | Related Requirement |
|---------|-------------|------------------|---------------------|
| Loading arm GA | Plan/elevation, slew/luff envelope, ERC location, connection details | DEL-11.06 OEM data, DEL-11.03 envelope calcs | Specification.md REQ-06 |
| Double-walled pipe arrangement | Pipe routing, annulus tap points, expansion loops, support locations | DEL-11.02 pipe spec, DEL-14 interfaces | Specification.md REQ-07 |
| Leak detection layout | Sensor locations (annulus, drip trays, sump), signal routing diagram | DEL-11.02 leak detection spec, DEL-19 I&C | Specification.md REQ-08 |
| Operator shelter | Location plan, floor plan, sections, services interfaces | DEL-11.02 shelter spec, PKG-22 building works | Specification.md REQ-09 |

**Source:** Datasheet.md §Construction table, Specification.md §Requirements, Procedure.md §Steps 3-6.

**Drawing content checklist (cross-reference to Procedure.md):**
- Loading arm GA (Procedure.md §Step 3): Plan/elevation views, slew/luff envelope, ERC location, connection flanges, operating/maintenance clearances
- Double-walled pipe arrangement (Procedure.md §Step 4): Pipe routing, annulus tap locations, expansion provisions, support locations, tie-in flanges
- Leak detection layout (Procedure.md §Step 5): Annulus sensor locations, drip tray locations, sump locations, signal routing, setpoints reference
- Operator shelter (Procedure.md §Step 6): Shelter location, floor plan, access/egress routes, HVAC/lighting/power interfaces, control panel location

**Employer's Requirements expectations:** **TBD** until clause references are provided.

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|-------------|----------|----------|----------|-------------------|-------------------|--------------|
| — | No conflicts identified at this stage | — | — | — | — | — |

*Note: Conflicts will be logged here when specific ER clauses are extracted and any discrepancies with decomposition scope or technical standards are identified.*

---

**Pass 2/3 Enrichment Notes:**
- Enhanced cross-document alignment table with specific section references and verification notes
- Added "Related Requirement" column to Examples table to link drawings to Specification requirements
- Added "Throughput Considerations" section to address OBJ-2 (previously missing)
- Added "Drawing granularity" trade-off
- Enhanced traceability with explicit "Source:" citations throughout
- Expanded drawing content checklist with specific cross-references to Procedure.md steps
- All TBDs and ASSUMPTIONs preserved from Pass 1
- Verified alignment: 4 drawing types, 8/5/6 interfaces (consistent coverage), 6 acceptance criteria, 7 standards, 6 scope items
