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
| Objective Mapping | OBJ-6: Regulatory Compliance |

**Source:** _CONTEXT.md (DEL-28.03); Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md (Section 6, Objective-to-Deliverable Mapping)

## Attributes

| Attribute | Value | Specification § | Guidance § | Procedure Step |
|-----------|-------|-----------------|------------|----------------|
| Record Category | Design Coordination Records | — | P-1 | Step 6, Step 7 |
| Record Types | Coordination minutes, clash reports, RFI logs, interface registers, issue logs | FR-1, FR-3, FR-5, FR-6, FR-7 | C-3, C-4, C-5, C-6 | Steps 2-6 |
| Coordination Frequency | **TBD** — Weekly/bi-weekly during active design | FR-2 | C-3 | Step 2.1 |
| BIM/3D Coordination | **TBD** — If BIM used, per BEP | FR-3, IR-5 | P-4, C-4, T-3 | Step 3 |
| Coordination Phases | 30%, 60%, 90%, IFC | IR-2 | P-2 | Step 5 |
| Retention Period | **TBD** — 7-10 years post-project | QR-4 | — | Step 7.3 |
| Classification | Project Controlled — Quality Records | QR-3 | C-9 | Step 6, Step 7 |

**Source:** _CONTEXT.md (DEL-28.03 description, anticipated artifacts); Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md (PKG-28 scope)

## Conditions

**Design Coordination Context:**

Design coordination records provide evidence that inter-discipline design coordination was performed systematically throughout the design process, supporting design quality, constructability, and **OBJ-6: Regulatory Compliance**.

**Source:** Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md (Section 2, OBJ-6; Section 6, Objective-to-Deliverable Mapping)

**Coordination Scope:**

| Interface Type | Disciplines | Specification § | Example Coordination Points |
|----------------|-------------|-----------------|----------------------------|
| Civil-Structural | PKG-01, PKG-06, PKG-07 | IR-1 | Foundation elevations, embedments, site utilities |
| Structural-Mechanical | PKG-06, PKG-10, PKG-12 | IR-1 | Equipment foundations, pipe supports, access platforms |
| Structural-Electrical | PKG-06, PKG-17 | IR-1 | Cable tray supports, equipment foundations, conduit penetrations |
| Mechanical-Electrical | PKG-10, PKG-17 | IR-1 | Motor controls, heat tracing, instrumentation power |
| Process-Civil | PKG-10, PKG-01 | IR-1 | Underground piping, drainage, containment |
| Marine-Structural | PKG-08, PKG-09 | IR-1 | Wharf vs. loading arms, fender attachments, mooring hardware |

**Source:** Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md (Section 4, Package Summary)

**Coordination Methods** — See Guidance.md Considerations:

| Method | Purpose | Specification § | Procedure Step |
|--------|---------|-----------------|----------------|
| Coordination Meetings | Regular inter-discipline issue resolution | FR-1, FR-2 | Step 2 |
| 3D/BIM Clash Detection | Spatial conflict identification | FR-3, FR-4 | Step 3 |
| RFI Process | Design questions and clarifications | FR-5 | Step 4.2 |
| Interface Registers | Critical interface documentation | FR-6 | Step 4.3 |
| Issue Tracking | Coordination issue management | FR-7 | Step 4.4 |

## Construction

**Materials / Configuration:**

Anticipated artifacts:
- Inter-discipline coordination records
- Clash detection reports
- RFI logs

**Source:** _CONTEXT.md (anticipated artifacts)

**Detailed Record Types:**

**1. Coordination Meeting Minutes** — See Specification.md FR-1, D-1; Procedure.md Step 2.3:

| Element | Content |
|---------|---------|
| Meeting ID | Sequential numbering (e.g., COORD-MTG-001) |
| Date/Time/Location | Meeting details |
| Attendees | Names, disciplines, companies |
| Agenda Items | Discussion topics |
| Interface Issues | Issues identified and discussed |
| Decisions Made | Coordination decisions |
| Action Items | Responsible party, due date |
| Next Meeting | Scheduled date |

**2. Clash Detection Reports** (if BIM used) — See Specification.md FR-3, FR-4, D-2; Procedure.md Step 3.4:

| Element | Content |
|---------|---------|
| Report Date | Clash run date |
| Model Revisions | Models analyzed |
| Software | Clash detection software |
| Clash Summary | Total, Critical, Major, Minor counts |
| Clashes by Discipline | Breakdown by discipline pair |
| Critical Clashes | Details and assignments |
| Status | Prior clash closure status |

**3. RFI Logs** — See Specification.md FR-5, D-3; Procedure.md Step 4.2:

| Column | Content |
|--------|---------|
| RFI Number | Sequential (RFI-001, etc.) |
| Originator | Discipline raising question |
| Addressee | Responding party |
| Description | RFI question/issue |
| Date Submitted | Submit date |
| Response | Resolution text |
| Date Responded | Response date |
| Status | Open/Responded/Closed |

**4. Interface Registers** — See Specification.md FR-6, D-4; Procedure.md Step 4.3:

| Column | Content |
|--------|---------|
| Interface ID | Unique identifier |
| Discipline Pair | Disciplines involved |
| Interface Description | What is coordinated |
| Responsible Disciplines | Responsibilities by discipline |
| Interface Criteria | Elevations, locations, connections |
| Status | TBD/Agreed/Verified |

**5. Coordination Issue Logs** — See Specification.md FR-7, D-5; Procedure.md Step 4.4:

| Column | Content |
|--------|---------|
| Issue Number | Sequential |
| Description | Issue details |
| Disciplines Affected | Impacted disciplines |
| Priority | Critical/High/Medium/Low |
| Responsible Party | Assigned for resolution |
| Target Date | Resolution deadline |
| Resolution | How resolved |
| Status | Open/In Progress/Resolved |

## Cross-Deliverable Coordination

| Related Deliverable | Relationship | Specification § |
|--------------------|--------------|-----------------|
| DEL-27.04 Design Submission Packages | Coordinated designs submitted at each stage | IR-2 |
| DEL-28.01 Independent Design Verification | IDV may identify coordination issues | IR-3 |
| DEL-28.02 VFPA IP Review Responses | VFPA may identify coordination requirements | IR-4 |
| PKG-01 through PKG-36 | Coordination across all discipline packages | IR-1 |

**Source:** Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md (PKG-27, PKG-28); Specification.md (Interface Requirements)

## References

| Reference | Status | Notes |
|-----------|--------|-------|
| _REFERENCES.md | See file | Applicable reference documents |
| 0_References/ | See folder | Package reference materials |
| BIM Execution Plan | **TBD** | BIM requirements if BIM used |
| Project Quality Management Plan | **TBD** | QMP reference |
| Employer's Requirements | **TBD** | Specific ER sections for coordination |
| ISO 9001 | Applicable | Quality Management — quality records |
| ISO 19650 | **TBD** | BIM standards if BIM used |
| _DEPENDENCIES.md | NOT_TRACKED | Dependencies coordinated externally |

**Cross-Document Traceability:**
- Specification.md — Requirements FR-1 through FR-7, PR-1 through PR-3, IR-1 through IR-6, QR-1 through QR-4
- Guidance.md — Principles P-1 through P-6, Considerations C-1 through C-9, Trade-offs T-1 through T-6
- Procedure.md — Steps 1-8, Verification V-1 through V-5

**Source:** Specification.md; Guidance.md; Procedure.md
