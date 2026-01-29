# Datasheet: DEL-22.06 Building MEP Shop Design Drawing Set

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-22.06 |
| Name | Building MEP Shop Design Drawing Set |
| Package | PKG-22 Building Interior & MEP |
| Discipline | Buildings |
| Type | Drawing |
| Responsible | D&B Contractor (Suppliers/Subcontractors) |
| Status | INITIALIZED |

## Attributes

| Attribute | Value |
|-----------|-------|
| Drawing Number Prefix | **TBD** — Per project shop drawing numbering system (typically prefixed with "SD-" or vendor drawing number) |
| Sheet Size | **TBD** — Varies by vendor/fabricator (typical: ANSI D, ISO A1) |
| Scale | **TBD** — Varies by shop drawing type (typical: 1:20, 1:50, or as noted) |
| File Format | **TBD** — **ASSUMPTION**: PDF for submittal; native CAD per vendor standards |
| Submittal Classification | Shop Drawings (per DEL-22.02 submittal requirements) |
| Review Status | Submitted / Reviewed / Approved / Approved as Noted / Rejected (tracked during construction) |

**Source:** Decomposition REVISED_v2.md, DEL-22.06 entry; _CONTEXT.md

## Conditions

**Operating / Environmental Context:**

This deliverable defines and substantiates building MEP shop drawings (fabrication drawings) in accordance with Employer's Requirements.

**Source:** Decomposition REVISED_v2.md, DEL-22.06 description

### Purpose and Use

| Purpose | Description |
|---------|-------------|
| Fabrication Guidance | Provides detailed dimensions and specifications for shop fabrication of MEP components |
| Coordination Verification | Demonstrates fabricated components will fit within building and coordinate with structure and other systems |
| Quality Control | Allows engineer review of vendor interpretation of design before fabrication |
| Installation Reference | Provides field installation guidance with detailed connections and assembly instructions |

**Source:** ASSUMPTION: standard shop drawing purposes in EPC projects

### Shop Drawing Context

**Shop drawings differ from design drawings (DEL-22.01):**

- **Design Drawings** (DEL-22.01): Show design intent, performance requirements, general arrangement (prepared by design engineer)
- **Shop Drawings** (DEL-22.06): Show fabrication details, exact dimensions, connections, materials (prepared by vendors/fabricators based on design drawings)

**Shop Drawing Submittal Process:**

1. Contractor issues DEL-22.01 design drawings and DEL-22.02 specifications to vendors
2. Vendors prepare shop drawings showing how they will fabricate and install work
3. Contractor submits shop drawings to engineer for review
4. Engineer reviews shop drawings and returns with comments: Approved, Approved as Noted, Revise and Resubmit, or Rejected
5. Vendor revises shop drawings (if required) and resubmits
6. After approval, vendor fabricates per approved shop drawings

**Source:** Standard shop drawing submittal process per DEL-22.02 Specification Section 1 (General Requirements - Submittals)

## Construction

**Materials / Configuration:**

### Anticipated Shop Drawing Artifacts

Per Decomposition REVISED_v2.md, DEL-22.06 anticipated artifacts:

1. **Prefab ductwork shop drawings** — Fabricated ductwork sections with dimensions, fittings, and connections

**Source:** Decomposition REVISED_v2.md, DEL-22.06 anticipated artifacts

### Additional Anticipated Shop Drawings (Inferred from MEP Scope)

**ASSUMPTION**: Additional shop drawings likely required to fully support DEL-22.01 design and DEL-22.02 specifications:

**HVAC Shop Drawings:**
- Prefabricated ductwork sections (as noted in anticipated artifacts)
- Packaged HVAC equipment (dimensional drawings, rigging weights, utility connections)
- Ductwork accessories (dampers, louvers, diffusers, grilles)

**Plumbing Shop Drawings:**
- Prefabricated plumbing assemblies (if modular approach used)
- Plumbing fixtures (dimensional drawings, rough-in requirements)
- Specialty plumbing equipment (water heaters, pumps, backflow preventers)

**Fire Suppression Shop Drawings:**
- Sprinkler system layout (as-coordinated with structure showing exact head locations)
- Sprinkler pipe fabrication drawings (spool sheets for prefabricated sections)
- Fire protection equipment (fire pump, alarm valve, control valves)

**Electrical Building Services Shop Drawings** (coordinate with PKG-17):
- Lighting fixture shop drawings (dimensional, photometric data)
- Electrical panel shop drawings (layout, bus sizing, breaker schedule)

**Source:** Inferred from DEL-22.01 scope; standard MEP shop drawing types

### Typical Shop Drawing Content

**Shop drawings typically include:**

1. **Cover Sheet / Title Block**
   - Project identification
   - Vendor/fabricator name and contact
   - Drawing number and revision
   - Submittal date and resubmittal history

2. **Layout and Arrangement**
   - Overall dimensions and configuration
   - Connection to building structure and other systems
   - Clearances and access requirements

3. **Fabrication Details**
   - Material specifications and gauges
   - Weld details and connection methods
   - Fastener types and sizes
   - Shop assembly vs. field assembly

4. **Installation Details**
   - Support and hanger locations and types
   - Field connections and joints
   - Alignment and levelness requirements
   - Sequence of installation (if critical)

5. **Equipment Data**
   - Performance data (cross-reference to DEL-22.04 data sheets)
   - Utility connection requirements (electrical, piping, controls)
   - Rigging weights and lifting points

**Source:** ASSUMPTION: standard shop drawing content; industry practice

### Shop Drawing Review Focus

**Engineer reviews shop drawings for:**

- **Compliance**: Verify shop drawings comply with design intent, specifications, and codes
- **Coordination**: Verify shop-fabricated items coordinate with building structure, other trades, and available space
- **Completeness**: Verify shop drawings provide sufficient detail for fabrication and installation
- **Materials**: Verify materials and finishes match specifications
- **Performance**: Verify equipment performance matches design requirements (cross-check with DEL-22.04 data sheets)

**Engineer does NOT review for:**
- **Means and Methods**: Construction methods and fabrication techniques (contractor responsibility)
- **Safety**: Construction safety (contractor responsibility)
- **Cost**: Shop drawing review does not constitute approval of cost changes

**Source:** Standard shop drawing review scope and limitations

## References

### Project References

- Decomposition: `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`
- Context: `_CONTEXT.md`
- Dependencies: `_DEPENDENCIES.md` (NOT_TRACKED — dependencies coordinated externally)
- Additional references: See `_REFERENCES.md` and `execution/PKG-22_Building_Interior_and_MEP/0_References/`

### Applicable Standards

Shop drawings shall comply with applicable design codes and standards per DEL-22.02:

- **NBC 2020** — National Building Code of Canada 2020
- **ASHRAE 90.1** — Energy Standard for Buildings
- **NFPA 13** — Installation of Sprinkler Systems (fire protection shop drawings)
- **SMACNA** — Duct construction standards (ductwork shop drawings)
- **CSA standards** — Material and equipment standards

**Source:** DEL-22.02 Specification Standards section; applicable fabrication standards

### Cross-References

**Related Deliverables (within PKG-22):**

- **DEL-22.01** — Building MEP Design Drawing Set (shop drawings based on design drawings)
- **DEL-22.02** — Building MEP Technical Specification (shop drawings must comply with specifications, particularly submittal requirements section)
- **DEL-22.03** — Building MEP Design Calculations (shop drawings must support calculated performance)
- **DEL-22.04** — Building MEP Data Sheet Package (shop drawings must match equipment data sheets)
- **DEL-22.05** — Building MEP Installation and Test Records (installation per approved shop drawings verified during testing)

**Related Deliverables (other packages):**

- **PKG-21** — Building Structures & Envelope (shop drawings must coordinate with building structure and space constraints)
- **PKG-17** — Electrical Power Distribution (electrical shop drawings coordinate with MEP equipment power requirements)
- **PKG-19** — Control Systems (control interfaces shown on shop drawings must coordinate with BAS)

**Source:** PKG-22 deliverable relationships; shop drawing coordination requirements
