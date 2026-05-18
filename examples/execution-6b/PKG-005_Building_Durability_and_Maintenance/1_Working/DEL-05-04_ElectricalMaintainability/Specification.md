# Electrical Maintainability — Specification

## Scope

### What This Deliverable Covers

DEL-05-04 is the electrical systems maintainability narrative for the Town of Penhold Public Services Building (RFP 2024_004). It describes the design approach, systems selection, and construction methods that will ensure the electrical, lighting, IT/telecom, security, fire alarm, and emergency power systems of the PSB are easy to inspect, service, repair, and upgrade throughout the design life of the facility.

This deliverable addresses RFP §7.1.4 — "Building Durability / Ease of Repair and Maintenance" (p. 17) — from the electrical engineering discipline perspective, per the decomposition definition in PKG-005. It forms part of the PKG-005 suite alongside architectural, structural, and mechanical maintainability narratives (DEL-05-01 through DEL-05-03).

**Design lives in scope:**
- Main building (Fire Hall + Public Works): 50 years (RFP §2.2, pp. 7–8)
- Cold Storage ancillary building: 20 years (Decomposition v2.3, PKG-005 goal)

### Inclusions

- Electrical panel and distribution system maintainability
- Lighting system maintainability (LED fixture types, zone standardization, access, lifecycle)
- Building controls and management system serviceability
- IT/telecommunications infrastructure maintainability (structured cabling, labeling, spare capacity)
- Security and access control system lifecycle (base scope + Optional Items 3 and 4 context)
- Fire alarm system maintenance approach
- Emergency/backup power system maintainability (generator integration, transfer switch serviceability)
- Solar-ready electrical provisions (conduit rough-in and panel space reservation for future PV)

### Exclusions

- Mechanical system electrical interfaces (belongs to DEL-05-03)
- Structural provisions for conduit support (belongs to DEL-05-02)
- Energy efficiency narrative for electrical systems (belongs to DEL-04-03)
- Electrical/IT concept design narrative (belongs to DEL-02-05)
- Detailed construction drawings and specifications (post-award IFC documents)
- Pricing and cost estimates (belongs to PKG-001)
- Pickled Sand Storage Building (removed per Addendum 03 §1.2)

---

## Requirements

### Electrical Panel & Distribution

| ID | Requirement | Source | Verification |
|----|-------------|--------|-------------|
| R-EML-01 | Electrical systems, including receptacles and grounding, shall be designed to meet current needs and allow for future flexibility. The Design-Builder shall advise on optimal options considering program, budget, and operational needs. | RFP OSR §10.4 (p. 42) | Design review at 60% and 100% Detailed Design |
| R-EML-02 | Electrical receptacles shall be installed inside and outside the buildings. Coordination with mechanical systems (including overhead door openers) is required to ensure compatibility. | RFP OSR §10.4 (p. 42) | Design review; coordination drawing review at 100% IFC; commissioning check |
| R-EML-03 | The main panel and sub-panels shall be located to allow direct, unobstructed access for routine maintenance, circuit additions, and future load upgrades without requiring vehicle or equipment relocation. The electrical room (Functional Program row 13.0) with key fob access is the designated location for main electrical systems. | RFP OSR §10.4 (future flexibility); RFP App B row 13.0 (p. 46) | Site inspection at commissioning; O&M manual panel location diagram |
| R-EML-04 | All circuits, panels, and disconnects shall be labeled at the panel and at the point of use. Labels shall be durable (engraved, laminated, or equivalent) and legible for the full design life. | **ASSUMPTION: standard CEC practice; specific CEC clause TBD** | Pre-commissioning labeling inspection; O&M manual circuit schedule |
| R-EML-05 | Distribution panels shall include spare breaker capacity to accommodate future loads without panel replacement, supporting the 50-year design life. **ASSUMPTION: minimum 20% spare breaker positions at commissioning is industry-standard practice for municipal facilities; specific percentage TBD at detailed design. This figure requires confirmation by the Electrical Engineer with normative grounding (e.g., utility or municipal design standard) or explicit Owner acceptance as a design-stage decision. See Guidance EX-002 note and Conflict Table CON-001.** | ASSUMPTION (good practice); RFP OSR §10.4 (p. 42) — future flexibility | Panel schedule review at 100% Detailed Design; confirmed spare capacity percentage documented |

### Lighting Systems

| ID | Requirement | Source | Verification |
|----|-------------|--------|-------------|
| R-EML-06 | Lighting shall follow IES recommendations and be energy-efficient LED technology throughout all buildings. | RFP OSR §10.5 (p. 42) | Lighting calculation submittal per IES; design review |
| R-EML-07 | Emergency exit lights above personal doors shall include internal batteries as per code requirements. | RFP OSR §10.5 (p. 42) | Commissioning battery function test; test records |
| R-EML-08 | Switches at personal doors in ancillary buildings shall have weatherproof covers. | RFP OSR §10.5 (p. 42) | Pre-occupancy inspection |
| R-EML-09 | Fixture mounting heights in apparatus bays and workshop bays shall be adjusted to avoid interference with machinery and clearance above 16 ft overhead door height (minimum). | RFP OSR §10.5 (p. 42); Addendum 03 §1.10 (16 ft minimum door height) | Design review; field verification at commissioning |
| R-EML-10 | LED fixture and driver types shall be standardized by zone category across the facility to minimize the number of distinct spare parts required for ongoing maintenance. Zone categories: apparatus bay (industrial high-bay, IP65 minimum for wet/damp location), office/shared space, storage, outdoor. A quantitative standardization target shall be established at detailed design (e.g., maximum number of distinct fixture/driver types per zone category, or maximum total distinct types facility-wide). **ASSUMPTION: derived from RFP OSR §10.5 and RFP §7.1.4 intent (ease of maintenance). Quantitative acceptance threshold TBD at detailed design by Electrical Engineer. See Conflict Table CON-002 regarding IP rating terminology normalization.** | ASSUMPTION (based on RFP OSR §10.5, p. 42; RFP §7.1.4, p. 17) | Fixture schedule review at 100% Detailed Design; standardization confirmation against quantitative target |
| R-EML-11 | Cold Storage building shall be provided with motion-activated LED lighting (interior and exterior) and 120V outlets interior. Fixtures shall be cold-rated for the unheated, freeze-thaw environment. | RFP App B (row 32.0, p. 46) | Pre-commissioning inspection; cold-start function test |

### IT / Telecom Infrastructure

| ID | Requirement | Source | Verification |
|----|-------------|--------|-------------|
| R-EML-12 | IT/Data compatibility shall be provided throughout the main structure. Structured cabling shall be a minimum of Category 6A (CAT6A) throughout. **ASSUMPTION: CAT6A is recommended practice for 50-year lifecycle (supports multiple active equipment generations); to be confirmed by Electrical Engineer at detailed design. See Guidance P-002.** | RFP OSR §10.6 (p. 42); Guidance P-002 (CAT6A recommendation) | Design review; commissioning connectivity test; cabling category verification |
| R-EML-13 | The meeting room (ICP) shall accommodate a minimum of 15 concurrent access points for internet for Emergency Management use. | RFP OSR §10.6 (p. 42) | Commissioning test; access point count verification in ICP room |
| R-EML-14 | A display system (wall-mounted, capable of connecting to a laptop for dispatching data display) shall be provided in the fire apparatus bay closest to the office area. The system shall be a wall-mounted screen (mounted TV or equivalent) with hardware to connect to a laptop for receiving and displaying dispatch data. | RFP OSR §10.6 (p. 42) | Pre-occupancy inspection and functional test |
| R-EML-15 | A PA (public address) system shall be installed throughout the main structure. PA is not required in ancillary buildings. | RFP OSR §10.6 (p. 43) | Pre-occupancy functional coverage test throughout main structure |
| R-EML-16 | All IT/telecom cable runs shall be labeled at both ends and documented in the as-built drawings to support troubleshooting, reconfiguration, and future expansion without disruption. **ASSUMPTION: derived from RFP §7.1.4 ease-of-maintenance requirement and OSR §10.6 compatibility requirements.** | ASSUMPTION (RFP §7.1.4, p. 17; RFP OSR §10.6, p. 42) | As-built drawing review at closeout; cable schedule completeness |
| R-EML-17 | Spare conduit capacity shall be provisioned alongside primary IT/telecom runs to accommodate future expansion without trenching or major rework. **ASSUMPTION: typical practice for municipal facilities with evolving IT needs; specific spare quantity TBD at detailed design.** | ASSUMPTION (good practice; RFP OSR §10.4, p. 42 — future flexibility) | Conduit pathway drawing review at 100% Detailed Design |

### Security & Access Control

| ID | Requirement | Source | Verification |
|----|-------------|--------|-------------|
| R-EML-18 | Key Fob access control shall be provided for controlled zones as identified in the Functional Program, including the electrical room (row 13.0) and IT room (row 17.0), at minimum. | RFP App B (rows 13.0, 17.0, p. 46) | Pre-occupancy access control test by zone |
| R-EML-19 | Access control system shall be designed for multiple zones within the main structure to allow shared space use and control of interdepartmental access. Ancillary buildings shall not be included in access control. | RFP OSR §12.3 (p. 44) | Design review; commissioning zone-by-zone test |
| R-EML-20 | Security and camera system (Optional Item 4) shall include cameras in parts of the interior of the main building and on the exterior. Installation and monitoring costs shall be priced separately per the pricing template. | RFP OSR §12.4 (p. 44) | Per Optional Item scope acceptance and commissioning |
| R-EML-21 | No supplier preference is specified by the Town for security/camera systems. The system shall be selected with interoperability and upgrade pathway considered to avoid vendor lock-in. | Addendum 03 §1.19 | Design basis statement in O&M manual; upgrade pathway documentation |

### Emergency Power

| ID | Requirement | Source | Verification |
|----|-------------|--------|-------------|
| R-EML-22 | A backup diesel generator shall be provided (outdoor location). At minimum, it shall support: kitchen, meeting room (ICP), and 2 bathrooms. Bay doors shall have either a generator-powered or a manual secondary opening mechanism (Design-Builder's choice). | Addendum 03 §1.15 | Commissioning load test under full essential load; O&M manual |
| R-EML-23 | The generator and transfer switch shall be accessible for routine testing, inspection, and servicing without confined-space entry. The transfer switch shall be located indoors (heated) where practical. **ASSUMPTION: derived from RFP §7.1.4 ease-of-maintenance; specific access clearance TBD at detailed design.** | ASSUMPTION (RFP §7.1.4, p. 17); Addendum 03 §1.15 | Pre-occupancy inspection; commissioning load test documentation |
| R-EML-30 | Generator fuel tank capacity shall be sized to a runtime target at rated essential load. **ASSUMPTION: 72-hour runtime target referenced in Guidance EX-003; this figure requires Owner confirmation and generator sizing analysis at detailed design. If the 72-hour target is not a design requirement, Guidance EX-003 shall be updated to clarify its illustrative nature.** | Guidance EX-003 (ASSUMPTION); Addendum 03 §1.15 (generator required) | Generator sizing calculation review at detailed design; fuel tank capacity verification at commissioning |

### Bay Infrastructure Electrical Provisions

| ID | Requirement | Source | Verification |
|----|-------------|--------|-------------|
| R-EML-27 | Bay sump pumps (required per Addendum 03 §1.8) shall be provided with dedicated electrical circuits, corrosion-resistant connections rated for the wet/salt/particulate bay environment, and accessible disconnect provisions for pump maintenance without main panel shutdown. **ASSUMPTION: specific circuit sizing and protection TBD at detailed design by Electrical Engineer based on sump pump selection.** | Addendum 03 §1.8 (bay sumps required); Datasheet Addendum 03 Requirements table; Guidance C-001 | Design review; commissioning functional test of sump pump circuits; accessible disconnect verification |
| R-EML-28 | Water fill stations (Addendum 03 §1.16: one in fire apparatus bay, one in PW bay) shall have electrical provisions if powered (e.g., heated, metered). If fill stations are non-powered, this requirement is satisfied by documenting the non-powered decision. **TBD: Electrical Engineer + Mechanical Engineer to confirm whether fill stations require electrical provisions at detailed design.** | Addendum 03 §1.16; Datasheet Addendum 03 Requirements table (S1.16 row) | Design review confirming powered/non-powered decision; if powered, commissioning functional test |

### Future Capacity Provisions

| ID | Requirement | Source | Verification |
|----|-------------|--------|-------------|
| R-EML-29 | Electrical infrastructure shall accommodate future EV charging station installation without major panel replacement or service upgrade. Provisions shall include: panel space allocation, conduit pathway designation to potential EV charging locations, and load calculation allowance. **TBD: Owner to confirm interest in EV charging provisions; scope and extent TBD at detailed design.** | Guidance EX-002 (EV charging referenced as future capacity justification); RFP OSR §10.4 (p. 42) — future flexibility | Design review confirming panel space and conduit pathway allocation for future EV; documented in as-built drawings |

### Solar Readiness

| ID | Requirement | Source | Verification |
|----|-------------|--------|-------------|
| R-EML-24 | The roof shall be solar-capable with required orientation (flat, south, west, or southwest). Electrical rough-in provisions (conduit stubs from roof to electrical room, panel space reservation, inverter location designation) shall be provided for future photovoltaic addition without requiring major electrical system rework. | Addendum 03 §1.17; RFP OSR §10.4 (p. 42) — future flexibility | Design review; as-built drawings showing rough-in locations and panel space reservation |

### Documentation

| ID | Requirement | Source | Verification |
|----|-------------|--------|-------------|
| R-EML-25 | As-built drawings shall include all electrical, lighting, IT/telecom, and control systems in CAD (DWG and PDF) format reflecting actual installed conditions. | RFP §7.5 (p. 24) | Closeout document review; Owner sign-off |
| R-EML-26 | O&M manuals shall include: electrical panel schedules (with spare capacity records), lighting fixture schedules (with part numbers and zone map), IT cable schedules (labeled runs), access control zone maps, fire alarm documentation (riser diagram, component schedule), generator operation instructions (monthly test procedure, fuel system), and all manufacturer warranties. Provided as two hard-copy 3-ring binders plus a complete digital copy. | RFP §7.5 (p. 24); RFP §7.3.6 (p. 22) | Closeout document review; Owner sign-off before occupancy |

---

## Standards

| Standard | Application | Status |
|----------|-------------|--------|
| Canadian Electrical Code Part I (CEC) | All electrical installation | **ASSUMPTION: applicable per local AHJ; specific clause references TBD. Electrical Engineer + AHJ confirmation required at detailed design to establish specific Part I clause applicability.** |
| IES (Illuminating Engineering Society) | Lighting levels and fixture selection | Explicitly required by RFP OSR §10.5 (p. 42) |
| NBCC and Alberta Building Code | Emergency lighting, exit signs, safety, accessibility | Referenced in RFP §7.2 (p. 19); §1 (Definitions, p. 6) |
| Alberta Building Code — Accessibility / Barrier-Free Design | Electrical system accessibility provisions: panel heights, switch heights, receptacle heights in accessible spaces | **ASSUMPTION: applicable for public building; specific clause references TBD. Electrical Engineer + Architect to confirm at detailed design. See also CSA B651.** |
| CSA B651 (Accessible Design for the Built Environment) | Accessibility requirements for electrical installations in barrier-free areas | **ASSUMPTION: applicable as referenced standard under Alberta Building Code; specific clauses TBD at detailed design** |
| CAN/ULC-S527 (or equivalent) | Fire alarm control equipment | **ASSUMPTION: applicable; specific clause references TBD. Electrical Engineer to confirm applicable edition and clauses at detailed design.** |
| TIA-568 (or equivalent Canadian standard) | Structured cabling | **ASSUMPTION: applicable for IT/telecom infrastructure; specific edition and clauses TBD. Electrical Engineer to confirm at detailed design.** |
| CCDC 14-2013 (+ Appendix J Supplementary Conditions) | Contract framework; quality standards | RFP §1 (p. 6); App J (p. 61) |
| CSA C282 / NFPA 110 (or Canadian equivalent) | Emergency generator installation | **ASSUMPTION: applicable; Canadian equivalent (CSA C282) to be confirmed by Electrical Engineer at detailed design. Specific clauses TBD.** |

---

## Verification

| Requirement ID(s) | Verification Method | Timing | Responsible Party |
|-------------------|---------------------|--------|-------------------|
| R-EML-01, R-EML-03 | Design review — panel location drawings and electrical room access | 60% + 100% DD | Electrical Engineer |
| R-EML-02 | Coordination drawing review; field check at commissioning | 100% IFC; commissioning | Electrical Engineer + Mechanical Engineer |
| R-EML-04, R-EML-05 | Panel schedule review; pre-commissioning labeling inspection | 100% DD; pre-occupancy | Electrical Engineer |
| R-EML-06 | Lighting calculation submittal per IES | 60% DD | Electrical Engineer |
| R-EML-07, R-EML-08, R-EML-09, R-EML-11 | Pre-occupancy inspection; cold-start test (Cold Storage) | Pre-occupancy | Electrical Engineer + General Contractor |
| R-EML-10 | Fixture schedule review (zone standardization confirmation) | 100% DD | Electrical Engineer |
| R-EML-12, R-EML-13 | Network access point count; commissioning connectivity test in ICP room | Commissioning | IT/Telecom Subcontractor + Electrical Engineer |
| R-EML-14, R-EML-15 | Pre-occupancy functional test; PA coverage test | Pre-occupancy | Electrical Engineer |
| R-EML-16 | As-built drawing review; cable schedule completeness check | Closeout | Electrical Engineer |
| R-EML-17 | Conduit pathway drawing review showing spare stubs | 100% DD | Electrical Engineer |
| R-EML-18, R-EML-19 | Access control zone-by-zone functional test | Commissioning | Security Subcontractor |
| R-EML-20 | Per Optional Item scope acceptance and commissioning test | If accepted | Security Subcontractor |
| R-EML-21 | Design basis statement in O&M manual; upgrade pathway documented | Closeout | Electrical Engineer |
| R-EML-22, R-EML-23 | Generator load test under full simulated essential load; transfer switch accessibility inspection | Commissioning | Electrical Engineer + Generator Subcontractor |
| R-EML-24 | As-built drawings showing conduit rough-in locations and panel space reservation | Closeout | Electrical Engineer |
| R-EML-25, R-EML-26 | Closeout document review; Owner sign-off; O&M manual verified to include maintenance sequencing guide (per Guidance C-002) showing which circuits/systems can be worked simultaneously vs. sequentially | Closeout | Proposal Manager + Electrical Engineer |
| R-EML-27 | Bay sump pump circuit functional test; accessible disconnect verification; corrosion-resistant connection inspection | Commissioning | Electrical Engineer |
| R-EML-28 | Powered/non-powered decision documented; if powered, commissioning functional test | 60% DD (decision); Commissioning (if powered) | Electrical Engineer + Mechanical Engineer |
| R-EML-29 | Panel space and conduit pathway allocation for future EV documented in as-built drawings | Closeout | Electrical Engineer |
| R-EML-30 | Generator sizing calculation review; fuel tank capacity verification against confirmed runtime target | 100% DD; Commissioning | Electrical Engineer + Generator Subcontractor |

---

## Documentation

### Anticipated Artifacts

| Artifact | Description | Timing |
|----------|-------------|--------|
| Electrical maintainability narrative | Primary deliverable: prose narrative per RFP §7.1.4 (p. 17) addressing all seven system areas | Proposal submission |

### Supporting Artifacts (Post-Award / Construction)

| Artifact | Description | Timing |
|----------|-------------|--------|
| Fixture schedule | Standardized fixture/driver type list with zone mapping, part numbers, and cold-rating (Cold Storage) | 100% Detailed Design |
| Panel schedule | Circuit count, spare capacity record, labeling convention, load calculations | 100% IFC |
| IT/Telecom cable schedule | All runs labeled at both ends; conduit layout; spare stub locations | Closeout (as-built) |
| O&M manual — electrical chapters | Panel, fixture, IT, access control, fire alarm, generator; manufacturer warranties | Closeout |
| As-built drawings — electrical and IT | CAD DWG + PDF; reflects actual installed conditions | Closeout |
