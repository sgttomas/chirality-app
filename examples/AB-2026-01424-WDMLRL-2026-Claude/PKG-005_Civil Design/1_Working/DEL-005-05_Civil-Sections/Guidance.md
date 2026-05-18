# Guidance — DEL-005-05: Civil Sections & Details

---

## Purpose

DEL-005-05 (Civil Sections & Details) exists to translate the site grading and drainage design into construction-ready cross-sections and detail drawings. While the Site Grading Plan (DEL-005-02), Drainage Plan (DEL-005-03), and Driving Surface & Pad Layout Plan (DEL-005-04) establish intent in plan view, this deliverable communicates the vertical geometry, material layering, drainage connectivity, and interface conditions that contractors need to actually build the civil infrastructure.

In the context of this project, civil sections and details serve two audiences:
1. **The construction contractor (PKG-018)** — who needs section drawings to price, set out, and build gravel surfaces, pads, drainage features, and utility crossings.
2. **The permit and inspection authority** — who requires IFC drawings stamped by a P.Eng. licensed in Alberta, demonstrating that the design meets Alberta Safety Code requirements.

**Source for project context:** RFP §3.3.2; Decomposition — PKG-005, DEL-005-05.

---

## Principles

### 1. Sections must communicate construction intent, not just design intent
Detail drawings exist to prevent field interpretation errors. Cross-sections should show sufficient information for a contractor to install the work without further engineering input for routine conditions: material types, layer thicknesses, slopes, compaction references, and connection elevations (or references to survey data).

**ASSUMPTION:** This is a professional practice principle for civil drawing sets; not stated explicitly in the RFP but consistent with the IFC stamp requirement (RFP §3.3.2).

### 2. Gravel section design must reflect the actual equipment load
The RFP explicitly requires the driving surface to accommodate the weight and turning radius of a motor scraper (RFP §3.3.2). Motor scrapers are among the heaviest construction equipment used on landfill operations. ASSUMPTION: the gravel section thickness and subbase design must be derived from the geotechnical report (equivalent single axle load or California Bearing Ratio method, or equivalent Alberta method) rather than from a lighter commercial vehicle assumption. Using an under-designed section risks premature surface failure under landfill operational loads.

### 3. Drainage design governs grading sections
The drainage requirement (positive site drainage; no off-site drainage alteration — RFP §3.4) directly constrains the cross-fall slopes and edge conditions shown in grading sections. Sections should be coordinated with the Drainage Plan (DEL-005-03) and the Civil Calculation Package (DEL-005-06) to ensure the finished grades depicted are consistent with the stormwater management design, not just the plan view grading intent.

### 4. Mud sump detail has a plumbing interface
The exterior mud sump (RFP §3.4; App B — conceptual drawing) is a civil construction element (excavation, liner/structure, connection piping) that interfaces with the wash bay floor drain system (PKG-006 — plumbing). The civil section detail must coordinate invert elevations and connection locations with the PKG-006 plumbing drawings to avoid field conflicts at the building/slab interface.

### 5. Details must distinguish County-supplied from Proponent-supplied materials
The RFP specifies that aggregate supply is by County (RFP §3.3.1). Detail drawings and notes should clearly identify where aggregate/gravel is County-supplied, so the contractor does not include supply cost and the design does not inadvertently specify a proprietary or non-County-supplied gradation. ASSUMPTION: the Civil Specification (DEL-005-07) will govern material specifications; the sections should cross-reference the specification rather than duplicate material requirements.

---

## Terminology Notes

### Design Vehicle Terminology (B-003)
The following terminology inconsistency exists across documents and should be normalized:
- **Specification** REQ-005-05-002 uses "large construction equipment, including a motor scraper"
- **Guidance** Principle 2 treats "motor scraper" as the specific design vehicle
- **Datasheet** Attributes uses "large construction equipment, including motor scraper"

**TBD:** The civil engineer should clarify whether "motor scraper" is the governing design vehicle (i.e., the specific equipment whose axle load governs section thickness design) or one example of a broader design vehicle class ("large construction equipment"). If the motor scraper is the governing design vehicle, all documents should use "motor scraper" as the primary term. If "large construction equipment" is the governing class, the motor scraper should be identified as the critical member of that class for design purposes. **Proposed authority:** Civil engineer. *[Source: Specification.md, REQ-005-05-002; Guidance.md, Principle 2; Datasheet.md, Attributes — lensing item B-003]*

### TBD Notation Convention (E-002)
Documents currently use inconsistent TBD notation formats: "TBD", "TBD --", "(TBD)", "type TBD", "-- TBD", and "values are TBD." For consistent tracking and automated resolution verification, adopt a single TBD notation convention across all four documents:
- **Proposed format:** `TBD` followed by a parenthetical context identifier where helpful, e.g., `TBD (pending geotech report)`, `TBD (pending PKG-006 coordination)`.
- Avoid variant forms such as dashes before/after TBD or embedding TBD within descriptive phrases without a clear placeholder boundary.

**Note:** This normalization should be applied during the next revision pass. *[Source: all four documents — lensing item E-002]*

---

## Considerations

### Geotechnical report dependency
The geotechnical investigation (PKG-008) is an upstream dependency for this deliverable. Key inputs needed from the geotech report include:
- Subgrade bearing capacity (to confirm section thickness adequacy for motor scraper loads)
- Frost depth (to determine subbase depth requirements in central Alberta)
- Soil classification and plasticity (to determine subgrade preparation requirements)
- Groundwater depth (relevant to sump invert selection)

Until the geotech report is available, section layer thicknesses for subbase and subgrade preparation should be held as TBD placeholders in draft drawings. Issuing sections with assumed layer depths without geotech confirmation is not recommended for a motor-scraper-loaded surface.

**Source:** RFP §3.3.2 (geotech report required); ASSUMPTION: standard Alberta civil engineering practice for heavy-load pavement design.

### Survey data dependency
Finished grade elevations shown in sections (particularly at transitions and drainage outfalls) depend on the preliminary survey data from PKG-008. Without survey-confirmed existing grade elevations, sections cannot show accurate cut/fill depths or drainage slopes. ASSUMPTION: survey data will be available before detailed section design is finalized.

### Alberta freeze-thaw context
Central Alberta experiences significant freeze-thaw cycling. ASSUMPTION: Subbase/subgrade design should account for frost heave potential in fine-grained soils, consistent with Alberta Infrastructure or equivalent standards. This is particularly relevant for the cement pad interface and any rigid-to-flexible surface transitions. Specific requirements TBD pending geotech report.

### Retaining wall applicability
The _CONTEXT.md lists retaining wall sections as an anticipated artifact. Whether retaining walls are required depends on the site grading design (DEL-005-02). If the expansion area can be graded without retained cuts, retaining wall details may not be needed. ASSUMPTION: the civil engineer will confirm during detailed design whether retaining walls are required. If not required, this artifact can be omitted with a note in the drawing set.

### Utility crossing coordination
Utility routing (gas, electrical, communications) under driving surfaces requires coordination with PKG-004 (electrical) and utility providers (gas, communications). Civil crossing details should not be finalized until utility routing is confirmed. ASSUMPTION: utility crossings beneath gravel surfaces are anticipated given the RFP requirement to coordinate utility tie-ins (RFP §3.3.2).

### Constructability Review Rationale (F-004)
Procedure Step 11 mentions circulating detail sheets to PKG-018 (construction contractor) "if contractor is engaged at time of design." The rationale for whether and when constructability review provides value should be considered:

- Under the CCDC 14-2013 Design-Build contract form, the contractor and designer are on the same team. Constructability review during design is generally beneficial because the contractor can identify field execution issues (access constraints, equipment clearances, construction sequencing) before drawings are finalized.
- However, if the contractor is not yet engaged at the time of civil section design, constructability review may be deferred to the first IFC revision.
- **TBD:** Confirm with the project manager / contract administrator whether constructability review by PKG-018 is expected as a formal quality assurance step, or whether it is optional. If formal, define the review scope and timing in Procedure Step 11. **Proposed authority:** Project manager / contract administrator. *[Source: Guidance.md; Procedure.md, Step 11 — lensing item F-004]*

### As-Built Survey Verification Rationale (E-003)
The Procedure Records table lists "Survey data (PKG-008) — Filed as upstream input reference" but does not address as-built survey verification of the constructed civil sections. For inspection evidence completeness:

- **TBD:** Clarify whether as-built survey verification of civil sections (comparing constructed grades/depths to design sections) is within the scope of this deliverable's inspection evidence, or whether as-built verification is handled separately (e.g., by PKG-008 surveyor or County inspection process).
- If within scope, specify the stage at which as-built survey is required (e.g., pre-cover subgrade check, post-compaction base course, final grade).
- If outside scope, add a note in the Records table identifying where as-built verification responsibility resides. **Proposed authority:** Civil engineer / County project representative. *[Source: Procedure.md, Records table; Guidance.md — lensing item E-003]*

### Relationship to Civil Specification (DEL-005-07)
Material specifications (gradation, compaction density, quality assurance) should reside in DEL-005-07 (Civil Specification), not be repeated in full on each detail sheet. Detail drawings should cross-reference the specification by section number. This separation is consistent with standard IFC drawing practice and avoids inconsistency if specification values change.

---

## Trade-offs

| Trade-off | Option A | Option B | Proposed Approach |
|---|---|---|---|
| Gravel section thickness — pre/post geotech | Issue with assumed thickness for tender purposes; revise after geotech | Hold details until geotech report is received | ASSUMPTION: issue with TBD placeholders for subbase depth; use geotech report to confirm before IFC stamp. Do not stamp without geotech confirmation for motor-scraper-loaded surfaces. |
| Level of detail for standard vs. site-specific sections | Use Alberta Infrastructure or APWA standard details by reference for routine items | Produce project-specific details for all items | ASSUMPTION: use standard details by reference where applicable (reduces drafting effort and leverages pre-approved details); produce project-specific details only where standard details do not apply (mud sump, pad interfaces, site-specific drainage structures). **Decision criteria (A-006):** A standard detail is acceptable when (a) the project site conditions fall within the standard detail's stated applicability range, (b) the design loading is not heavier than the standard detail's design basis, and (c) no project-specific constraint (e.g., motor-scraper loading, County-supplied aggregate, or unusual subgrade conditions) requires a modification. When any of these conditions is not met, a project-specific detail is required. **TBD:** The civil engineer shall confirm the applicability of each proposed standard detail against the geotech report findings and site-specific constraints. *[Source: Guidance.md, Trade-offs row 2 — lensing item A-006]* |
| Mud sump — civil vs. plumbing boundary | Civil section shows full sump structure including interior drain connection | Civil section shows sump shell only; plumbing shows interior drain | ASSUMPTION: civil shows exterior sump construction including connection stub to building; plumbing shows interior drain piping to stub. Boundary should be explicitly noted on both drawing sets to avoid gaps. |
| Retaining wall inclusion | Include retaining wall details as placeholder, to be developed if needed | Omit from set; add if design confirms requirement | ASSUMPTION: omit from first-issue; add note that retaining wall details will be issued as an addendum if the grading design (DEL-005-02) confirms their necessity. |

---

## Examples

**Typical civil section drawing set structure (ASSUMPTION — for reference; final structure TBD by civil engineer):**

- **C-001 General Notes and Legend** — Drawing symbols, abbreviations, specification cross-references, general construction notes
- **C-101 Typical Gravel Driving Surface Section** — Full-depth gravel section from subgrade to wearing surface; notes on compaction, material, and motor scraper load basis
- **C-102 Gravel Pad Section** — Contractor-supplied cement and County-supplied gravel pad area interfaces per App B
- **C-103 Grading and Fill Section** — Typical and specific cut/fill transitions; bench geometry if required; topsoil stripping note
- **C-201 Site Drainage Details** — Swale section, culvert installation detail, catchbasin detail (types TBD)
- **C-301 Wash Bay Mud Sump Detail** — Plan and section of exterior mud sump; dimensions, connection invert, material
- **C-302 Sump Drain Detail (Repair Bays)** — Cross-section at floor drain; coordination note reference to PKG-006
- **C-401 Utility Crossing Details** — Cover depths, sleeving, backfill for electrical, gas, and communications crossings
- **C-501 Driveway Apron and Transition Details** — Entry/exit transitions from public road (if applicable) or internal transitions
- **C-601 Edge Condition and Pad Interface Details** — Gravel-to-cement pad transitions; edge restraints

**Source:** ASSUMPTION — this structure is illustrative and consistent with standard Alberta civil IFC drawing practice for projects of this scale. The civil engineer shall determine the final drawing structure.

---

## Conflict Table (for human ruling)

The following potential conflicts are noted for awareness and human ruling. Two additional conflicts (CONF-005-05-03, CONF-005-05-04) were added during Pass 3 semantic lensing enrichment:

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|---|---|---|---|---|---|---|
| CONF-005-05-01 | Aggregate supply is County-provided (RFP §3.3.1), but gravel section design must specify gradation requirements — if County aggregate does not meet the specified gradation for motor-scraper loading, a conflict exists between supply responsibility and design specification. | RFP §3.3.1 (County supplies aggregate) | RFP §3.3.2 (driving surface must accommodate motor scraper) | REQ-005-05-003; Datasheet — Driving Surface Material; Specification — Standards | Civil engineer to confirm County aggregate gradation meets heavy-load section requirements during preliminary design; if not, escalate to Owner for resolution | TBD |
| CONF-005-05-02 | Bulk cut/fill is County scope (RFP §3.3.1), but grading sections will depict finished grades achieved through grading — if County bulk cut/fill leaves the site at a configuration incompatible with the civil engineer's design, a scope gap exists. | RFP §3.3.1 (bulk cut/fill by County) | RFP §3.3.2 (final grading and landscape by Proponent per IFC drawings) | REQ-005-05-004; Specification — Scope | Proponent civil engineer to confirm existing grade (post-County cut/fill) against design intent before finalizing sections; document acceptance of existing grade condition | TBD |
| CONF-005-05-03 (D-001) | Aggregate supply is County-provided (RFP §3.3.1) while Specification REQ-005-05-003 requires the section detail to specify gravel material type, gradation, depth, and compaction requirements. If County-supplied aggregate does not meet the design gradation for motor-scraper loading, the compliance enforcement baseline is unresolved. This conflict reinforces CONF-005-05-01 from the normative-applying perspective: the compliance baseline for gravel specification cannot be enforced if the supply source is outside the Proponent's control. | Datasheet — Conditions — Aggregate Supply (County-supplied, OUT of scope) | Specification — REQ-005-05-003 (gradation specification requirement) | REQ-005-05-003; Datasheet — Conditions; Specification — Standards | Civil engineer to confirm County aggregate gradation meets heavy-load section requirements during preliminary design; if not, escalate to Owner for resolution. *[lensing item D-001]* | TBD |
| CONF-005-05-04 (D-002) | Civil-plumbing boundary at the mud sump is described differently across documents. Guidance Trade-off row 3 proposes "civil shows exterior sump construction including connection stub to building; plumbing shows interior drain piping to stub," but Specification REQ-005-05-006 requires the civil detail to show "connection to the wash bay drain" without specifying where the scope boundary lies. Procedure Step 5.2 says "confirm with PKG-006" but the boundary definition is not formalized. A formal boundary definition is needed to confirm practical delivery scope. | Specification — REQ-005-05-006 (connection to wash bay drain — boundary undefined) | Guidance — Trade-offs row 3 (connection stub boundary proposal) | REQ-005-05-006; Procedure Step 5.2; Guidance Trade-offs row 3 | Civil engineer / PKG-006 plumbing engineer to formally define the civil-plumbing scope boundary at the mud sump and document it on both drawing sets. *[lensing item D-002]* | TBD |
