# Specification — DEL-005-03: Drainage Plan

## Scope

### What This Deliverable Covers

DEL-005-03 is the Drainage Plan drawing set for the West Dried Meat Lake Regional Landfill Maintenance Shop Addition project. It is one component of the PKG-005 Civil Design package. This deliverable covers the design and drawing documentation for all stormwater management systems, surface drainage, drainage structures, and drainage details required for the project site at SW 14–44–21–W4, near Ferintosh, Alberta.

Specifically, this deliverable covers scope items:
- **SOW-0015**: Complete final civil design including site grading plan with drainage features and components (Source: R-01, §3.3.2; Decomposition §3C)
- **SOW-0020**: Grading design shall account for positive site drainage and future storm events (Source: R-01, §3.4; Decomposition §3C)
- **SOW-0021**: Grading design shall not alter drainage conditions of neighbouring properties (Source: R-01, §3.4; Decomposition §3C)

This deliverable supports **OBJ-001** (code-compliant, fully functional facility) and **OBJ-003** (complete P.Eng.-stamped IFC documentation). (Source: Decomposition §7, PKG-005.)

### What This Deliverable Excludes

| Excluded Item | Reason / Where Handled |
|---|---|
| Site Grading Plan (overall grading contours) | Separate deliverable: DEL-005-02_Site-Grading-Plan |
| Driving Surface and Pad Layout | Separate deliverable: DEL-005-04_Driving-Surface-Layout |
| Civil Sections and Details (generic) | Separate deliverable: DEL-005-05_Civil-Sections |
| Civil Calculation Package | Separate deliverable: DEL-005-06_Calculation-Package |
| Civil Specification (written specification) | Separate deliverable: DEL-005-07_Specification |
| Wash bay structural enclosure | PKG-011 (SOW-0027a) |
| Wash bay drainage and wash bay exterior mud sump physical construction | PKG-018 (SOW-0027b) — this deliverable provides the design; construction is in PKG-018 |
| Plumbing floor drains inside building | PKG-006 / PKG-014 |
| Landscape planting and restoration | PKG-007 |
| Bulk cut and fill | County responsibility (OUT of scope) |
| Brushing and clearing | County responsibility (OUT of scope) |
| Aggregate supply | County/Landfill responsibility (OUT of scope) |

---

## Requirements

Requirements are derived from accessible sources. Requirements labeled **ASSUMPTION** are inferred from source context and standard civil engineering practice.

### REQ-001 — Positive Site Drainage
**Requirement:** The drainage design shall provide for positive drainage across the project site, ensuring that stormwater is directed away from building structures and paved/gravel surfaces, and that standing water is not created in operational areas.
**Source:** R-01, §3.4 ("Grading Design shall account for positive site drainage and future storm events"); Decomposition SOW-0020.
**Verification:** Engineering review of drainage plan; confirmation that all graded surfaces drain to designated collection or dispersal points.

### REQ-002 — Future Storm Event Capacity
**Requirement:** The drainage design shall account for future storm events. Design storm return period and rainfall intensity parameters are TBD pending civil engineer's determination of applicable Alberta regulatory or municipal requirements.
**Source:** R-01, §3.4 ("account for positive site drainage and future storm events"); Decomposition SOW-0020.
**Verification:** Drainage calculations (DEL-005-06) confirming adequacy for the selected design storm.

> **TBD (A-001):** What design storm return period and rainfall intensity apply to this site under Alberta standards and Camrose County requirements? This is the single most consequential open normative parameter. Enforceable threshold values (return period, rainfall intensity, acceptable peak discharge rate at site boundary) must be determined and recorded before verification can establish pass/fail. (Source: R-01, §3.4 — storm events referenced but not quantified; resolution proposed via Civil Engineer of record, Camrose County, and Alberta Environment.)

### REQ-003 — No Alteration of Neighbouring Property Drainage
**Requirement:** The drainage design shall not alter the drainage conditions of neighbouring properties. Stormwater shall be managed within the project site boundary or directed to appropriate outlets without increasing runoff volumes or changing flow paths to adjacent properties.
**Source:** R-01, §3.4 ("Grading design shall not alter the drainage conditions of neighboring properties"); Decomposition SOW-0021.
**Verification:** Engineering review confirming pre- and post-development drainage patterns at site boundary; review by Civil Engineer of record. Verification shall include quantified pre-development vs. post-development runoff comparison with benchmark values or an acceptable change threshold (TBD — method and thresholds to be determined by Civil Engineer of record; documented in DEL-005-06). (Enrichment: F-001 — conformance benchmark currently undefined; without quantified values, verification is subjective.)

### REQ-004 — IFC Drawing Quality and P.Eng. Stamp
**Requirement:** All Issued for Construction (IFC) drawings within this deliverable shall be signed and stamped by a Professional Engineer (P.Eng.) licensed to practice in the Province of Alberta.
**Source:** R-01, §3.3.2 ("All Issued For Construction Drawings must be signed/stamped by a professional engineer licensed to practice in the province of Alberta"); Decomposition SOW-0018.
**Verification:** Confirmation of P.Eng. stamp and seal on all IFC drawing sheets prior to release for construction.

### REQ-005 — Preliminary Design Approval Prior to IFC
**Requirement:** A preliminary civil design (DEL-005-01) must be delivered and approved by the County project team before the final Drainage Plan IFC drawings are issued.
**Source:** R-01, §3.3.2 ("Deliver Preliminary Design for the County project team to approve"); Decomposition SOW-0010e.
**Verification:** County approval acknowledgement on file before IFC drawings are released.

### REQ-006 — Code and Regulatory Compliance
**Requirement:** The drainage design shall adhere to all applicable Alberta building codes, regulations, and Alberta Safety Codes.
**Source:** R-01, §3.3.2, §3.4.
**Verification:** Code compliance review by the Civil Engineer of record referencing specific applicable code clauses (TBD — specific code clause references to be identified by Civil Engineer once governing codes are confirmed; see Standards table below); permit authority review during permit process. Compliance determination must be traceable to named provisions. (Enrichment: A-003 — generic "code review" verification lacks traceability without specific clause citations.)

### REQ-007 — Wash Bay Exterior Mud Sump Interface
**Requirement:** The drainage plan shall identify and detail the wash bay exterior mud sump connection for the wash bay drainage system, coordinating with the wash bay drainage infrastructure scope (SOW-0027b / PKG-018). The wash bay exterior mud sump shall be clearly delineated from the clean stormwater collection system on the drainage plan.
**Source:** R-01, §3.4 ("Mud sump from wash bay on exterior of building for clean out with excavator"); Decomposition SOW-0027b.
**Verification:** Coordination check between DEL-005-03 and PKG-018 construction drawings.

> **Terminology note (X-001):** The canonical term for this element is **wash bay exterior mud sump**. This replaces prior variant terms ("exterior mud sump," "wash bay drainage system," "mud sump") used inconsistently across documents. All documents in this deliverable set use this canonical term.

### REQ-008 — Driving Surface Drainage Consideration (ASSUMPTION)
**Requirement (ASSUMPTION):** The drainage design shall account for runoff from the gravel driving surface, which is designed to accommodate the weight and turning radius of heavy construction equipment including motor scraper class vehicles. (Source: R-01, §3.3.2 — driving surface requirement; drainage coordination is ASSUMPTION inferred from standard civil design practice.)
**Verification:** Engineering review confirming driving surface runoff is captured and directed appropriately. Verification shall include: (a) flow path tracing from gravel driving surfaces to collection/dispersal points, and (b) catch area delineation confirming all driving surface runoff is accounted for. (Enrichment: X-003 — generic "engineering review" verification does not produce a definitive finding for a requirement that is itself an ASSUMPTION; either confirm the requirement and specify the verification test, or convert to a design consideration in Guidance.)

---

## Standards

The following standards are understood to govern this deliverable. Where the specific text of a standard was not accessible in the available sources, this is noted.

> **Action required (A-002):** All five standards entries below are tagged ASSUMPTION with "location TBD." The Civil Engineer of record must confirm applicability and identify specific edition/clause references for each standard before mandatory practice can be verified against the correct criteria.

| Standard | Applicability | Accessibility / Notes |
|---|---|---|
| Alberta Building Code (current edition) | Governing building code for provincial compliance | ASSUMPTION: likely applicable; specific edition and drainage-specific clauses — location TBD. Civil Engineer to confirm applicable edition and identify relevant drainage provisions. |
| Alberta Safety Codes Act and associated codes | Applicable Safety Codes as required by the County | R-01, §3.3.2; specific drainage Safety Code provisions — location TBD. Civil Engineer to identify applicable Safety Code provisions for site drainage. |
| Camrose County Development and Building Permit requirements | Local municipal permitting requirements may include site drainage conditions | ASSUMPTION: likely applicable; specific requirements — location TBD pending permit application. Civil Engineer to confirm municipal drainage conditions during permit process. |
| Alberta Environment and Protected Areas stormwater guidance | Provincial stormwater management guidance — may set design storm criteria. If confirmed applicable, this standard must be treated as a governing requirement for compliance coverage. (Enrichment: C-002 — compliance coverage is incomplete without this as a confirmed governing standard if it applies.) | ASSUMPTION: likely applicable for a landfill-adjacent municipal facility; specific requirements — location TBD. Civil Engineer to confirm applicability and identify specific guidance document and applicable provisions. |
| Canadian Standards / municipal engineering design guidelines | Any applicable municipal drainage design standards for Camrose County | ASSUMPTION: may apply; specific standards — location TBD. Civil Engineer to confirm whether Camrose County has adopted municipal drainage design standards. |

---

## Verification

> **Action required (D-001):** Most verification methods below use generic "engineering review" language without stating what constitutes pass vs. fail. The Civil Engineer of record should define explicit acceptance criteria for each requirement to enable definitive conformance verdicts. Suggested format: "Drainage plan demonstrates [criterion] at [threshold]."

| Requirement | Verification Method | Acceptance Criteria (TBD) | Responsible Party |
|---|---|---|---|
| REQ-001 (Positive drainage) | Engineering review of drainage plan; grading model or spot elevation check | TBD — define minimum grade, confirm no ponding areas in operational zones | Civil Engineer of record |
| REQ-002 (Storm event capacity) | Drainage calculations in DEL-005-06; calculation review | TBD — confirm design storm return period and rainfall intensity thresholds (see A-001, C-001) | Civil Engineer of record |
| REQ-003 (No neighbour alteration) | Pre/post drainage comparison with quantified runoff benchmarks; Civil Engineer review | TBD — define acceptable runoff volume/rate change threshold at site boundary (see F-001) | Civil Engineer of record |
| REQ-004 (P.Eng. stamp) | Stamp present on all IFC sheets | P.Eng. stamp, signature, and registration number on each sheet | Civil Engineer / Project Manager |
| REQ-005 (Preliminary approval) | County approval documented before IFC release | County written approval on file | Project Manager |
| REQ-006 (Code compliance) | Civil Engineer code review referencing specific code clauses (TBD); permit authority review | TBD — list applicable code clauses and confirm compliance for each (see A-003) | Civil Engineer of record / Permit Authority |
| REQ-007 (Wash bay exterior mud sump interface) | Coordination review with PKG-018 scope | Wash bay exterior mud sump located, detailed, and delineated from clean stormwater system | Civil Engineer / Project Manager |
| REQ-008 (Driving surface) | Engineering review with flow path tracing and catch area delineation (see X-003) | TBD — confirm all driving surface runoff captured and directed to collection/dispersal points | Civil Engineer of record |

---

## Documentation

The following artifacts are anticipated as outputs of this deliverable:

| Artifact | Status |
|---|---|
| Drainage plan drawings (multiple sheets) | Required |
| Storm sewer layout and profiles | Required (if applicable; applicability confirmed during design) |
| Inlet and catch basin locations and details | Required |
| Outlet structures and energy dissipation details | Required where applicable |
| Drainage calculations and sizing | Required (DEL-005-06; cross-referenced) |
| Stormwater detention/retention features | TBD — applicability to be determined by Civil Engineer |
| Drainage legend and notes | Required |
| Low-impact development (LID) details | TBD — applicability subject to regulatory or Owner direction |
| Wash bay exterior mud sump drainage connection detail | Required (interface with PKG-018) |

**Note:** All drawings shall be produced and formatted in accordance with standard engineering drawing practice applicable in Alberta. Drawing format and scale requirements are TBD pending Civil Engineer's determination and any Owner-specified CAD or drawing standards. (Enrichment: F-003 — for a deliverable whose primary output is a drawing set, the applicable drawing/CAD standard affects quality evaluation. The Civil Engineer and Owner should confirm drawing format and CAD standard requirements before drawing production begins.)
