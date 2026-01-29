# Datasheet: DEL-28.03 Design Coordination Installation & Test Records

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-28.03 |
| Name | Design Coordination Installation & Test Records |
| Package | PKG-28 Design Verification |
| Discipline | Design |
| Type | Record |
| Responsible | D&B Contractor (QA/QC) |
| Status | INITIALIZED |

## Attributes

| Attribute | Value |
|-----------|-------|
| Record Category | Design Coordination Records |
| Record Types | Coordination meeting minutes, clash detection reports, RFI logs, interface agreements, coordination registers |
| Coordination Frequency | **TBD** — **ASSUMPTION**: Regular coordination meetings (weekly or bi-weekly during active design phases) |
| BIM/3D Modeling Requirement | **ASSUMPTION**: 3D coordination model required for clash detection — **TBD**: BIM execution plan requirements |
| Coordination Phases | Aligned with design submission stages: 30%, 60%, 90%, IFC |
| Retention Period | **TBD** — **ASSUMPTION**: Project lifetime plus 7-10 years per contract and professional liability requirements |
| Classification | Project Controlled — Quality Records |

**Source:** _CONTEXT.md (DEL-28.03 description, anticipated artifacts); Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md (PKG-28 scope: inter-discipline coordination)

## Conditions

**Design Coordination Context:**

Design coordination records provide evidence that inter-discipline design coordination was performed systematically throughout the design process, supporting design quality, constructability, and **OBJ-6: Regulatory Compliance** — "The Works comply with all permits, codes, and authority requirements." Effective design coordination reduces design errors, conflicts, and construction issues.

**Source:** Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md (Section 2, OBJ-6; Section 6, Objective-to-Deliverable Mapping: DEL-28.01–DEL-28.03 associated with OBJ-6); **ASSUMPTION**: Design coordination supports quality and compliance

**Coordination Scope:**

Design coordination addresses interfaces between discipline packages across the full project scope, including but not limited to:
- **Civil-Structural interfaces**: Foundation elevations, embedments, underground utilities vs. foundations, site grading vs. structure elevations
- **Structural-Mechanical interfaces**: Equipment foundations, pipe support attachments, tank support structures, equipment access platforms
- **Structural-Electrical interfaces**: Cable tray support attachments, electrical equipment foundations, conduit penetrations through structures
- **Mechanical-Electrical interfaces**: Motor control interfaces, heat tracing power, instrumentation power, hazardous area classification alignment
- **Process-Civil interfaces**: Underground piping vs. site utilities, drainage connections, containment system integration
- **Marine-Structural interfaces**: Wharf structure vs. marine loading arms, fender attachment details, mooring hardware
- **All disciplines-Architectural interfaces** (if buildings included): Building penetrations, equipment rooms, access requirements

**Source:** Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md (Section 4, Package Summary: multi-discipline project); **ASSUMPTION**: Typical inter-discipline interfaces for industrial facility

**Coordination Methods:**

- **Coordination meetings**: Regular meetings between discipline design leads to review design progress, identify and resolve interface issues, make coordination decisions
- **3D model coordination (BIM)**: Use of 3D design models to detect and resolve spatial conflicts (clashes) between disciplines — **TBD**: BIM execution plan, model requirements, clash detection protocol
- **RFI process**: Formal Request for Information (RFI) process for design questions, clarifications, and issue resolution
- **Interface registers**: Documented interface agreements between disciplines (elevations, locations, connection details, responsibility assignments)
- **Design review meetings**: Multi-discipline design reviews at key milestones (30%, 60%, 90%, IFC) to verify coordination

**Source:** _CONTEXT.md (anticipated artifacts: coordination records, clash detection reports, RFI logs); **ASSUMPTION**: Standard D&B multi-discipline coordination methods

**Coordination Timing:**

- Coordination begins at project start and continues throughout design development
- Intensive coordination occurs before each design submission milestone (30%, 60%, 90%, IFC)
- Coordination continues during construction as design refinements and field conditions require
- **Source:** **ASSUMPTION**: Continuous coordination aligned with design schedule; design submission stages from DEL-27.04 and DEL-28.01

## Construction

**Materials / Configuration:**

Anticipated artifacts:
- Inter-discipline coordination records
- Clash detection reports
- RFI logs

**Source:** _CONTEXT.md (anticipated artifacts)

**Detailed Record Types:**

**1. Inter-Discipline Coordination Meeting Minutes**
- Meeting frequency, date, attendees
- Agenda items and discussion topics
- Interface issues identified and discussed
- Decisions made and action items assigned
- Responsible party and due date for action items
- **ASSUMPTION**: Standard meeting minutes format

**2. Clash Detection Reports**
- Clash detection run date and model revisions analyzed
- Software used (e.g., Navisworks, Revit, other BIM clash detection tools) — **TBD**: BIM software specification
- Clash report showing all detected clashes by discipline pair (e.g., Civil-Structural, Mechanical-Electrical)
- Clash severity classification (Critical, Major, Minor) — **TBD**: Classification criteria
- Clash resolution status (Open, In Progress, Resolved)
- Clash resolution description (how clash was resolved, which discipline made changes)
- **ASSUMPTION**: BIM-based clash detection per standard BIM coordination workflow

**3. RFI (Request for Information) Logs**
- RFI number (sequential numbering system)
- Originator (discipline raising question)
- Addressee (discipline or party expected to respond)
- RFI question/issue description
- Date submitted
- Response/resolution
- Date responded
- Status (Open, Responded, Closed)
- Related drawing/document references
- **ASSUMPTION**: Standard RFI tracking system

**4. Interface Registers/Agreements** — **ASSUMPTION**: Documented interface coordination
- Discipline pair (e.g., Civil-Structural, Mechanical-Electrical)
- Interface description (what is being coordinated)
- Responsible discipline for each interface element
- Interface criteria (elevations, locations, sizes, connection details)
- Agreement date
- Status (TBD, Agreed, Verified)

**5. Coordination Registers/Issue Logs** — **ASSUMPTION**: Issue tracking during coordination
- Issue number
- Issue description
- Discipline(s) affected
- Priority (Critical, High, Medium, Low)
- Responsible party for resolution
- Target resolution date
- Resolution description
- Status (Open, In Progress, Resolved)

**Deliverable Coordination** — **ASSUMPTION**: Design coordination interfaces with multiple deliverables:
- IDV Reports (DEL-28.01) — IDV may identify coordination issues requiring resolution
- VFPA IP Review Responses (DEL-28.02) — VFPA may identify coordination requirements
- Design Submission Packages (DEL-27.04) — Coordinated designs submitted at each stage
- All discipline design packages (PKG-01 through PKG-36) — Coordination ensures consistency across all discipline deliverables

**Source:** Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md (PKG-27, PKG-28 deliverables; Section 4, Package Summary: all discipline packages)

## References

- See `_REFERENCES.md` for applicable reference documents
- See `0_References/` in package directory for reference materials
- BIM Execution Plan (BEP) — **TBD**: Project BIM requirements and coordination protocols
- Project Quality Management Plan — **TBD**: QMP reference for coordination procedures
- Employer's Requirements — **TBD**: Specific ER sections governing design coordination requirements
- Applicable standards: ISO 9001 (Quality Management), ISO 19650 (BIM) — **ASSUMPTION**: BIM standards if BIM is used
- Cross-references: See `_DEPENDENCIES.md` (NOT_TRACKED — dependencies coordinated externally)
- Related deliverables:
  - DEL-27.04 (Design Submission Packages) — Coordination supports design submissions
  - DEL-28.01 (Independent Design Verification Reports) — IDV coordination
  - DEL-28.02 (VFPA IP Review Responses) — VFPA coordination
  - All discipline packages (PKG-01 through PKG-36) — Coordination across all disciplines
