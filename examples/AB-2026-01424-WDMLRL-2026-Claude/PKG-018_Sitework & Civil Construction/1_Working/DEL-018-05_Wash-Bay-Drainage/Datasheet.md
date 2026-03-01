# DEL-018-05 | Wash Bay Drainage & Mud Sump — Datasheet

---

## Identification

| Field | Value |
|-------|-------|
| **Deliverable ID** | DEL-018-05 |
| **Title** | Wash Bay Drainage & Mud Sump |
| **Package** | PKG-018 — Sitework & Civil Construction |
| **Deliverable Type** | Construction |
| **SOW Reference** | SOW-0027b |
| **Responsible Party** | General Contractor |
| **Project** | 2026 Design Build — West Dried Meat Lake Regional Landfill Maintenance Shop Addition |
| **Owner** | Camrose County |
| **Site Location** | SW 14–44–21–W4, near Ferintosh, Alberta |
| **Contract Form** | CCDC 14–2013 Design-Build Stipulated Price |
| **Completion Deadline** | December 31, 2026 |
| **Objectives** | OBJ-001 (Operational), OBJ-004 (Environmental/Mechanical Readiness) |
| **Related Deliverables** | DEL-018-02 (Site Grading — upstream), DEL-018-06 (Utility Tie-Ins — coordination), DEL-011-05 (Wash Bay Enclosure — interface) |

Source: _CONTEXT.md; Decomposition SS7 PKG-018 table; RFP SS1.1, SS3.1.

---

## Attributes

### System Components

| Component | Description | Source |
|-----------|-------------|--------|
| **Wash Bay Floor Drain** | Floor drain(s) inside the 24'-wide wash bay, collecting wash water and directing it to the exterior mud sump | App B (Plumbing) — floor drain shown in wash bay; SOW-0027b |
| **Exterior Mud Sump** | Exterior below-grade sump pit located on the east side of the building adjacent to the wash bay; receives wash bay drainage; designed for cleanout by excavator | RFP SS3.4; App B (Shop) — "Wash Bay Mud Sump" label; Decomposition Vocabulary Map |
| **Drainage Connection** | Subsurface pipe connecting wash bay floor drain(s) to the exterior mud sump | SOW-0027b: "floor drains, connection to mud sump" |
| **Pressure Washer Reel / Water Tap** | Water tap and pressure washer reel inside wash bay (upstream of drainage system) | App B (Plumbing) |
| **Grading for Drainage Flow** | Site grading in the vicinity of the mud sump must support positive drainage and not alter neighbouring property conditions | RFP SS3.4 (SOW-0020, SOW-0021); _CONTEXT.md |

### Physical Parameters

| Parameter | Value | Source |
|-----------|-------|--------|
| Wash Bay Width | 24 ft | App B (Shop) — plan dimensions |
| Mud Sump Location | Exterior, east side of building, adjacent to wash bay | App B (Shop) and App B (Plumbing) — label and position |
| Mud Sump Cleanout Method | Excavator cleanout (open-top or accessible design) | RFP SS3.4: "for clean out with excavator"; Decomposition Vocabulary Map |
| Mud Sump Dimensions | TBD — not specified in RFP; to be determined in civil design (DEL-005-02, DEL-005-03). **Note:** This value is required before construction can proceed; it is a prerequisite for sump excavation and material procurement. [Enrichment: A-003] | location TBD |
| Mud Sump Capacity | TBD — not specified in RFP; to be sized by civil/plumbing engineer based on sediment loading rate and target cleanout interval (see Cleanout Frequency below). [Enrichment: A-003] | location TBD |
| Sump Pit Construction Material | TBD — not specified; ASSUMPTION: concrete or precast structure consistent with landfill site conditions | ASSUMPTION |
| Floor Drain Count (Wash Bay) | TBD — App B (Plumbing) shows one floor drain in the wash bay; Specification REQ-002 and Procedure Step 5.1 use "floor drain(s)" in the plural form. Confirm whether the system includes one drain or multiple drains, as this affects pipe sizing and connection design. ASSUMPTION: one drain per App B (Plumbing); final count per plumbing IFC drawings (DEL-006-03). [Enrichment: E-003] | App B (Plumbing); location TBD pending IFC |
| Pipe Material / Diameter | TBD — to be specified in IFC drawings (DEL-005, DEL-006). [Enrichment: A-003] | location TBD |
| Invert Elevations | TBD — to be established by civil design (DEL-005-02, DEL-005-03). [Enrichment: A-003] | location TBD |
| Drainage Pipe Minimum Slope (Gradient) | TBD — required to ensure positive flow from floor drain to sump per Specification REQ-003; to be specified in civil IFC drawings (DEL-005). ASSUMPTION: minimum slope consistent with plumbing code requirements for the pipe diameter selected. [Enrichment: B-002] | ASSUMPTION; location TBD pending IFC |
| Site Frost Depth | TBD — required for sump and pipe design (burial depth and frost heave protection); to be confirmed from geotechnical report (SOW-0001). ASSUMPTION: significant frost depth given Camrose County, Alberta location. [Enrichment: B-001] | Geotechnical report (SOW-0001) — location TBD |
| Excavator Access Clearance Envelope | TBD — minimum width and height clearance around the mud sump to allow excavator bucket access for cleanout; to be defined in civil IFC drawings (DEL-005). Referenced in Specification REQ-004, Guidance Considerations, and Procedure Step 3.4. [Enrichment: X-003] | location TBD pending IFC |
| As-Built Survey Scope | TBD — specific survey points (sump invert, rim elevation, pipe inverts at entry/exit, pipe alignment, surface grades), survey accuracy standard, and datum reference to be defined by civil engineer. The as-built survey (DEL-008-04) is listed as an anticipated artifact in Specification and a record in Procedure but the required measurement scope is not yet specified. [Enrichment: E-004] | location TBD; PROPOSAL: Civil engineer defines survey scope |

**Note on TBD parameters:** Six physical parameters from the Pass 1 draft remain TBD (Mud Sump Dimensions, Capacity, Construction Material, Floor Drain Count, Pipe Material/Diameter, Invert Elevations). Four additional parameters have been identified through semantic lensing (Drainage Pipe Minimum Slope, Site Frost Depth, Excavator Access Clearance Envelope, As-Built Survey Scope). These TBDs collectively prevent construction execution and must be resolved through IFC design (DEL-005, DEL-006) and the geotechnical report (SOW-0001). [Enrichment: A-003, B-001, B-002, X-003, E-004]

---

## Conditions

### Operating Context

| Condition | Description | Source |
|-----------|-------------|--------|
| **Wash Water** | Wash bay used for washing large equipment (motor scraper class and similar landfill equipment) | RFP SS3.4: "Single enclosed bay dedicated for washing large equipment such as a motor scraper" |
| **Wash Water Character** | ASSUMPTION: wash water contains sediment, mud, and equipment wash residue; sump allows settlement before management. (Note: Decomposition source uses the term "effluent"; see Guidance Terminology Conventions for canonical vocabulary.) | Decomposition Vocabulary: "Exterior sump for wash bay effluent, cleanable by excavator" |
| **Environmental Setting** | Active landfill site; discharge management is an environmental compliance requirement | OBJ-004; _DEPENDENCIES.md |
| **Cleanout Frequency** | TBD — not specified in RFP. This datum is essential for validating sump sizing and establishing a maintenance plan. The civil/plumbing engineer should define an assumed sediment accumulation rate based on the anticipated equipment wash frequency and sediment loading, and the Owner should confirm acceptable cleanout intervals. ASSUMPTION: periodic excavator cleanout as sump fills with sediment. [Enrichment: E-001] | ASSUMPTION; RFP SS3.4; PROPOSAL: Owner defines operational expectations; engineer validates against sump capacity |
| **Climate** | Alberta semi-arid, freeze-thaw; below-grade sump subject to frost heave and freeze conditions | ASSUMPTION based on site location (SW 14-44-21-W4, Camrose County, AB) |
| **Regulatory** | Environmental discharge permit (ENV-PERMIT-001) may be required; regulatory authority TBD | _DEPENDENCIES.md |

### Constraints

- Drainage design must not alter drainage conditions of neighbouring properties. (Source: RFP SS3.4 / SOW-0021)
- Site grading plan must account for positive site drainage and future storm events. (Source: RFP SS3.4 / SOW-0020)
- Work must be complete by December 31, 2026. (Source: RFP SS3.1)
- IFC drawings must be signed/stamped by a P.Eng. licensed in Alberta. (Source: RFP SS3.3.2 / SOW-0018)
- DEL-018-05 is sequentially dependent on DEL-018-02 (Site Grading) to establish drainage grades. (Source: _DEPENDENCIES.md)

---

## Construction

### Scope of Work (from SOW-0027b)

Construct wash bay drainage infrastructure including:
1. Floor drain(s) within the wash bay (24' wide, interior to building DEL-011-05)
2. Drainage pipe connecting floor drain(s) to exterior mud sump
3. Exterior mud sump for excavator cleanout

Note: SOW-0027b was split from the original SOW-0027 (Decision D-006 in Decomposition) and absorbs the former SOW-0047. The wash bay structural enclosure is a separate deliverable (DEL-011-05 / SOW-0027a).

### Work Excluded from DEL-018-05

- Wash bay structural enclosure and steel plate floor (DEL-011-05 / SOW-0027a — PKG-011)
- Interior floor drains in repair bays (DEL-014-04 / SOW-0045 — PKG-014)
- Plumbing design drawings (DEL-006 series — PKG-006)
- Civil design and IFC drainage plan drawings (DEL-005 series — PKG-005)
- Utility tie-ins (DEL-018-06 / SOW-0080 — PKG-018)

### County-Supplied Scope (OUT — not Contractor responsibility)

- Supply of aggregate/gravel (RFP SS3.3.1 / SOW-0203)
- Bulk cut and fill (RFP SS3.3.1 / SOW-0201)
- Development permit, building permit, and Safety Code permit fees (RFP SS3.3.1 / SOW-0202)

---

## References

| Ref | Document | Relevance |
|-----|----------|-----------|
| R-01 | AB-2026-01424-WDMLRL RFP.pdf | Primary requirements: SS3.4 mud sump requirement; SS3.3.2 drainage and grading obligations |
| R-07 | AB-2026-01424-Appendix C - Site Maps.pdf | Site location and expansion area; confirms landfill context |
| App B (Shop) | AB-2026-01424-Appendix B (Shop).pdf | Conceptual floor plan showing "Wash Bay Mud Sump" label, exterior east side |
| App B (Plumbing) | AB-2026-01424-Appendix B (Plumbing).pdf | Floor drain location in wash bay; pressure washer reel; water tap |
| Decomposition | WDMLRL_Decomposition_Claude.md | SOW-0027b definition; PKG-018 scope; OBJ-001 and OBJ-004; Decision D-006; Vocabulary Map |
| _CONTEXT.md | DEL-018-05_Wash-Bay-Drainage/_CONTEXT.md | Deliverable identity, scope summary, objectives |
| _DEPENDENCIES.md | DEL-018-05_Wash-Bay-Drainage/_DEPENDENCIES.md | Upstream/downstream dependency declarations |
| SOW-0001 | Geotechnical Report (per RFP SS3.3.2) | Frost depth, soil conditions — required for sump and pipe design |
