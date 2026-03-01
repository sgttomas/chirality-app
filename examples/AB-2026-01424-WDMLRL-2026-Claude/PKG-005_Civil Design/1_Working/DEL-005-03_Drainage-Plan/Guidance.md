# Guidance — DEL-005-03: Drainage Plan

## Purpose

The Drainage Plan exists to satisfy the civil design obligation under SOW-0015, SOW-0020, and SOW-0021 — specifically the drainage features and components component of the final civil design package. Its function is to communicate stormwater management intent to the construction team (PKG-018 — Sitework and Civil Construction) and to demonstrate to the County and permit authorities that the project site will drain positively, future storm events are accounted for, and neighbouring property drainage conditions will not be adversely changed.

This deliverable is part of the broader civil design family within PKG-005. It is one of seven deliverables within that package; its drainage content is distinct from the Site Grading Plan (DEL-005-02), though the two are closely interdependent. The Drainage Plan focuses on the hydraulic elements — conveyance routes, structures, sizing, and details — while the Grading Plan establishes the surface geometry from which drainage flow paths are derived.

The Drainage Plan supports:
- **OBJ-001**: A code-compliant, fully functional facility that passes all applicable inspections. (Source: Decomposition §5.)
- **OBJ-003**: Complete, P.Eng.-stamped IFC design documentation across all disciplines before construction begins. (Source: Decomposition §5.)

---

## Principles

### Positive Drainage is a Hard Requirement
The RFP explicitly states that the grading design shall account for positive site drainage (R-01, §3.4). In Alberta's climate, positive drainage is critical to prevent standing water from freezing, undermining gravel surfaces, and damaging structures. The drainage plan must demonstrate that all site areas — including the building apron, gravel driving surfaces, and operational areas — drain to controlled collection or dispersal points.

### Neighbour Non-Alteration is a Regulatory and Contractual Constraint
The requirement that drainage conditions of neighbouring properties not be altered (R-01, §3.4; SOW-0021) is both a regulatory norm (typically enforced through municipal drainage policies and the Alberta Environment regulatory framework) and an explicit contractual obligation. The design must demonstrate the pre- and post-development drainage boundary conditions. This is not merely a best-practice suggestion; it is a pass/fail criterion for the design.

### Priority Ranking When Hard Requirements Conflict
Both positive drainage (REQ-001) and neighbour non-alteration (REQ-003) are hard requirements. However, achieving positive drainage in some site configurations could require directing additional flow toward a site boundary, which may conflict with the neighbour non-alteration constraint. **TBD (A-005):** The Civil Engineer of record and Owner must establish an explicit priority ranking when positive drainage (REQ-001), neighbour non-alteration (REQ-003), and cost/constructability constraints conflict. Until this ranking is established, the design should treat neighbour non-alteration as an absolute constraint and achieve positive drainage within that boundary — but this approach may require on-site detention or storage to resolve, which has cost and space implications. (Source: R-01, §3.4 establishes both requirements without priority guidance; Decomposition SOW-0020, SOW-0021.)

### The Site is a Landfill-Adjacent, Heavy-Equipment Operational Facility
The project site context (West Dried Meat Lake Regional Landfill, SW 14–44–21–W4, Ferintosh area, Camrose County) informs drainage design in important ways:
- The site is rural and on County-owned land; no municipal storm sewer infrastructure may be available (ASSUMPTION — stormwater must be managed on-site or dispersed to natural features; confirm during design).
- Heavy equipment (motor scraper class) will operate on site; this creates high wheel loads and concentrated pavement stress points that may affect drainage grades and surface stability.
- The wash bay generates process water (equipment wash effluent) that flows to the wash bay exterior mud sump cleanable by excavator (R-01, §3.4; SOW-0027b). This drainage stream must be separated from clean stormwater in the drainage plan.

> **TBD (B-004):** Are there specific Alberta Environment and Protected Areas requirements for stormwater management at or near landfill sites that would impose additional constraints beyond standard municipal drainage? The landfill-adjacent context may trigger environmental requirements (e.g., stormwater quality treatment, monitoring, or separation requirements) that materially change the design approach. This question should be resolved with Alberta Environment and Protected Areas and/or the Civil Engineer before finalizing the drainage design. (Source: landfill proximity noted in _CONTEXT.md and Decomposition; environmental considerations flagged as ASSUMPTION in Considerations below.)

### Coordinate with the Grading Plan and Other Civil Deliverables
The drainage plan does not stand alone. It depends on:
- **DEL-005-02 (Site Grading Plan)**: Surface grades determine flow paths and collection points. Drainage plan sheet notes must be consistent with grading plan elevations and contours.
- **DEL-005-05 (Civil Sections and Details)**: Standard civil sections (swales, ditches, culverts) may be cross-referenced.
- **DEL-005-06 (Civil Calculation Package)**: All drainage sizing shall be supported by calculations. The drainage plan should identify which elements are governed by calculations in DEL-005-06.
- **PKG-018 (Sitework and Civil Construction)**: Construction personnel will build to this drawing set; drawing clarity and completeness directly affect constructed quality.

### Geotechnical Data Will Inform Drainage Design
The geotechnical investigation (DEL-008-01, PKG-008) will characterize subgrade conditions. Soil permeability, frost depth, and subsurface drainage conditions are likely to influence the drainage design approach — particularly decisions about detention storage, infiltration feasibility, and pipe invert depths. The drainage plan may need to be revisited or confirmed after the geotech report is available. (ASSUMPTION: standard civil engineering practice; geotech report not yet available at time of this drafting.)

---

## Considerations

### Storm Return Period Selection
The RFP requires accounting for "future storm events" (R-01, §3.4) but does not specify a design storm return period or rainfall intensity. The Civil Engineer of record must determine the appropriate design storm for this facility type and site context under applicable Alberta standards. Relevant considerations include:
- Municipal or County drainage design requirements (if any) — TBD.
- Alberta Environment and Protected Areas stormwater management guidelines — TBD.
- Proximity to the landfill and any associated environmental protection requirements — TBD.
- Risk profile of the facility (a maintenance shop — moderate consequence of flooding; however, heavy equipment operational requirements may increase sensitivity to surface drainage conditions).
- **Climate change factors (E-002):** For a drainage system with a multi-decade service life, the Civil Engineer should consider whether to apply a climate change uplift factor to historical rainfall data per current Alberta guidance. REQ-002 references "future storm events," which may implicitly require accounting for changing precipitation patterns. TBD — determine whether current Alberta Environment guidance recommends or requires a climate change intensity-duration-frequency (IDF) adjustment for new infrastructure. (Source: Specification REQ-002; R-01, §3.4.)

Until the design storm is selected and confirmed, drainage structure sizing is TBD.

### Separation of Process Water from Stormwater
The wash bay exterior mud sump (SOW-0027b) receives equipment wash effluent. This is a process drainage stream that should be physically separated from the site's clean stormwater collection system. The drainage plan must clearly delineate this boundary. The civil drainage plan addresses site stormwater; the wash bay exterior mud sump detail (DEL-005-03 interface item) should show the sump location and its relationship to the external graded surface without commingling with the clean drainage network. (ASSUMPTION: separation is standard practice for landfill operations and required for environmental compliance; specific regulatory requirement — location TBD.)

### Gravel Driving Surface Drainage
The final driving surface is gravel, designed for motor scraper class equipment (R-01, §3.3.2). Gravel surfaces are permeable but also susceptible to erosion if drainage is not well managed. Edge treatment, ditch or swale placement, and crown grades for gravel running surfaces are standard civil design elements and should be included in the drainage plan.

### County-Provided Aggregate and Its Implications
Aggregate supply is a County/Landfill responsibility (Decomposition SOW-0203). The drainage design should not assume specific aggregate specifications unless confirmed — drainage performance of gravel surfaces is sensitive to grading and fines content. This is noted as a coordination item.

> **Rationale note (X-002):** The uncertainty around County-supplied aggregate specification directly affects drainage design assumptions in two ways: (a) **gravel permeability** — fines content governs how much rainfall infiltrates through the driving surface vs. becoming surface runoff, affecting runoff volume calculations; and (b) **erosion resistance** — aggregate gradation affects susceptibility to washout at concentrated flow points (swale entries, catch basin approaches). Until the aggregate specification is known, the Civil Engineer should either design to a worst-case permeability assumption (high fines content = low permeability = maximum surface runoff) or establish a hold point pending aggregate specification confirmation. (Source: Decomposition SOW-0203; Datasheet > Attributes > Aggregate Supply.)

### Long-Term Maintenance of Drainage Infrastructure (C-003)
The Considerations above address design-stage decisions but do not discuss post-construction maintenance or lifecycle value of drainage elements. The following maintenance factors should inform design decisions:
- **Cleaning frequency and access:** The wash bay exterior mud sump explicitly requires excavator access for cleaning (R-01, §3.4). Other drainage elements (catch basins, swales, detention features) also require periodic maintenance. The drainage plan should consider equipment access paths for maintenance vehicles.
- **Lifecycle cost implications:** Lined swales and concrete structures have higher initial cost but lower maintenance compared to earthen channels. Trade-off selection (see Trade-offs table below) should account for the Owner's maintenance capacity and budget.
- **Sediment and debris management:** A landfill-adjacent, heavy-equipment facility will generate sediment (gravel fines, tracked material). Drainage structures should be designed with sediment traps or cleanout access appropriate for the expected sediment loading.

TBD — the Civil Engineer and Owner should discuss maintenance expectations and incorporate them into drainage element selection and layout. (Source: R-01, §3.4 — wash bay exterior mud sump maintenance; Decomposition SOW-0027b; standard civil engineering practice.)

---

## Trade-offs

| Trade-off | Options | Considerations |
|---|---|---|
| On-site detention vs. graded dispersal | Retention/detention pond vs. sheet-flow dispersal to site perimeter | Detention pond provides better stormwater management and less neighbour impact; requires more land and maintenance. Sheet-flow dispersal is simpler but may not satisfy storm event requirements depending on site size and soil permeability. Selection TBD by Civil Engineer. |
| Concrete swales vs. earthen swales | Lined (concrete or rip-rap) vs. unlined drainage channels | Lined channels provide higher capacity and erosion resistance (important given heavy equipment); earthen channels are lower cost. Site conditions will govern. |
| Underground storm pipe vs. surface drainage | Piped storm sewer vs. surface drainage ditches/swales | Urban-style piped storm sewer is unlikely given rural site and lack of municipal sewer (ASSUMPTION); surface drainage is most probable primary approach. Confirm during design. |
| LID integration | Low-impact development measures (bioswales, infiltration) | LID applicability depends on soil permeability (geotech data needed) and regulatory environment. May be beneficial for neighbour non-alteration requirement. |

---

## Examples

No project-specific drainage design examples were available in the accessible source documents. The following are general references to inform design approach:

- The RFP references the need for a site grading plan "with drainage features and components" (R-01, §3.3.2) — indicating the County expects a drawing-level treatment of drainage, not just narrative description.
- The wash bay exterior mud sump requirement (R-01, §3.4) is a specific drainage feature element that should appear on the drainage plan as a located and detailed element.
- The Appendix C site maps (R-07) provide the aerial view of the site expansion area; Civil Engineer should use this to understand existing site topography and drainage patterns before developing the drainage design. (Note: R-07 content was not fully accessible in text form; Civil Engineer should review the source PDF directly.)

---

## Conflict Table (for human ruling)

No unresolvable conflicts were identified during the Pass 1 + Pass 2 drafting of this deliverable's four documents. The following items are flagged as requiring design-stage resolution but are not source-level conflicts:

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|---|---|---|---|---|---|---|
| C-001 | Design storm return period not specified — the RFP requires accounting for "future storm events" but provides no specific return period or rainfall criteria | R-01, §3.4 (storm events referenced but not quantified) | Alberta standard practice (design storm to be selected by engineer) | Specification REQ-002; Guidance — Storm Return Period | Civil Engineer of record to select and document in DEL-005-06 Calculation Package | TBD |
| C-002 | Process water (wash bay exterior mud sump) vs. stormwater separation — drainage plan boundary between civil stormwater and wash bay process drainage not defined in RFP | R-01, §3.4 (wash bay exterior mud sump referenced) | SOW-0027b (wash bay drainage in PKG-018) | Specification REQ-007; Guidance — Separation of Process Water | Civil Engineer to define boundary on drainage plan; confirm with Owner | TBD |
| C-003 | Stormwater disposal method (on-site retention vs. dispersal to natural drainage) — not specified in RFP; rural site with no confirmed municipal storm sewer connection | R-01, §3.3.2, §3.4 | R-07 (site aerial — not fully extracted) | Specification REQ-001, REQ-002, REQ-003; Guidance — Trade-offs | Civil Engineer of record; confirm with Camrose County and Alberta Environment | TBD |
