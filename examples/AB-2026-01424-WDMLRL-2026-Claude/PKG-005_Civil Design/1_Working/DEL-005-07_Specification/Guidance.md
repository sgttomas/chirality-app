# Guidance — DEL-005-07: Civil Specification

---

## Purpose

DEL-005-07 exists to provide the normative written specification that governs all civil materials, workmanship, and quality standards for the West Dried Meat Lake Regional Landfill Maintenance Shop Addition. It is the companion document to the PKG-005 drawing set and forms the contractual quality baseline for civil sitework construction under the CCDC 14–2013 Design-Build contract.

The specification is produced by the Civil Engineer as part of final design deliverables (OBJ-003: P.Eng.-stamped IFC documentation) and must be in place before civil construction (PKG-018) commences. It directly enables:
- County and regulatory inspection of civil works.
- Contractor quality control and materials procurement.
- Dispute resolution regarding workmanship during construction and the 2-year guarantee period.

Source: RFP §3.3.2, §3.4; Decomposition §5 (OBJ-001, OBJ-003), §7 (DEL-005-07).

---

## Principles

### 1. Drainage-First Grading Design
The overriding civil design principle for this project is positive drainage. The site is an active landfill with heavy equipment operations. Standing water on driving surfaces creates safety hazards, surface degradation, and potential regulatory issues. All grading decisions should prioritize drainage over aesthetics or convenience of construction.
Source: RFP §3.4 (SOW-0020, SOW-0021).

### 2. Equipment-Calibrated Surface Design
The driving surface specification must be calibrated to motor scraper-class equipment — the heaviest equipment operating at this landfill site. The gravel surface thickness, gradation, and subgrade preparation requirements should be derived from equipment load data and geotechnical subgrade conditions, not from generic light-traffic or passenger vehicle standards.
Source: RFP §3.3.2, §3.4.

### 3. Geotechnical-Informed Design
The civil specification cannot be fully completed until the geotechnical report (DEL-008-01) is available. The specification should be structured so that geotechnically-dependent values (subgrade CBR, frost protection depth, compaction standards) are clearly flagged as TBD until they can be replaced with geotechnically-confirmed values. Issuing a specification without this grounding would create risk of subgrade failure under heavy equipment loads.
Source: RFP §4.8.2; Decomposition §4 (SOW-0304).

**Schedule Risk — Geotechnical Report Dependency:** If the geotechnical report (DEL-008-01) delivery is delayed relative to the civil design timeline, the civil specification cannot be finalized. The Project Manager should establish a contingency approach for this dependency, including: (a) identification of the latest acceptable date for receiving DEL-008-01 given the December 31, 2026 project completion deadline; (b) interim measures if the report is delayed (e.g., issuing specification with [GEO TBD] placeholders and a revision plan); and (c) communication protocol to escalate the delay early. This is a critical-path dependency for DEL-005-07.
Source: Procedure.md Step 2; see item B-004 in _SEMANTIC_LENSING.md.

### 4. Scope Boundary Clarity
The specification must be explicit about what is County-supplied versus Proponent-supplied. Aggregate/gravel is County-supplied (SOW-0203). The specification should include material quality and gradation requirements that the County's aggregate must meet — giving the County a clear target for what they must supply — while making clear that supply is not the Proponent's cost.
Source: RFP §3.3.1; Decomposition §4.

### 5. CSI Format for Constructability
ASSUMPTION: Using CSI MasterFormat Division 31 (Earthwork) and Division 32 (Exterior Improvements) as the specification structure will aid coordination with other discipline specifications (architectural Division 03 for concrete pads, etc.) and facilitate subcontractor tendering. This is standard Alberta practice for construction specifications on institutional projects.

---

## Considerations

### Site Context — Active Landfill
The construction site is at the West Dried Meat Lake Regional Landfill (SW 14–44–21–W4, Ferintosh, Alberta). This is an operational facility. Civil works must be sequenced to minimize interference with landfill operations. The specification should address dust control, erosion and sediment control during construction, and site cleanliness requirements appropriate for a working landfill environment.
Source: Appendix C — Site Maps; RFP §2.15 (Prime Contractor OH&S obligations).

**Construction Sequencing Constraints:** TBD — the Civil Engineer needs operational context from the County regarding specific constraints imposed by active landfill operations on civil construction, including but not limited to: access restrictions, permitted operating hours for construction, haul route conflicts with landfill equipment, and any seasonal restrictions. These constraints will directly affect the construction sequencing plan and should be obtained before finalizing the specification.
Source: Guidance.md — Site Context; see item D-002 in _SEMANTIC_LENSING.md.

### Frost and Subgrade Conditions
Alberta's Central region experiences significant ground frost. Subgrade preparation requirements — frost protection depth for granular base, subgrade stabilization if weak soils are encountered — will be critical specification elements. These values must come from the geotechnical investigation. Specifying insufficient frost protection on a heavy-equipment driving surface at this site is a high-consequence design error.
Source: RFP §4.8.2; location and climate context from RFP §1.0, Appendix C.

### Mud Sump Interface
The exterior mud sump (for wash bay drainage) sits at the boundary between civil, plumbing (PKG-006), and structural (PKG-002) disciplines. The civil specification will need to clearly define which elements are civil scope versus plumbing scope versus structural scope. This interface should be resolved during design coordination, and the specification should cross-reference the relevant plumbing and structural sections.
Source: RFP §3.4 (SOW-0027b); Decomposition §4 (D-006).

**Proposed Scope Division (TBD — requires coordination confirmation):**

| Physical Element | Proposed Discipline Scope | Cross-Reference |
|---|---|---|
| Sump excavation and backfill | Civil (PKG-005 / DEL-005-07) | REQ-CIVIL-009 |
| Surface drainage grading to sump location | Civil (PKG-005 / DEL-005-07) | REQ-CIVIL-001 |
| Sump vessel (precast concrete or cast-in-place) | Structural (PKG-002) — TBD | DEL-002-12 Structural Specification |
| Drainage pipe connection from wash bay to sump | Plumbing (PKG-006) | DEL-006-08 Plumbing Specification |
| Cleanout access design (excavator clearance) | Civil/Structural interface — TBD | REQ-CIVIL-009; RFP §3.4 |
| Sump sizing and effluent management | Plumbing (PKG-006) — TBD | DEL-006-07 Plumbing Calculation Package |

This table is a **PROPOSAL** pending confirmation during interdisciplinary coordination (Procedure Step 1). The Civil Engineer, Plumbing Engineer, and Structural Engineer must agree on the scope boundary before specifications are finalized.
Source: See item X-003 in _SEMANTIC_LENSING.md.

### Topsoil Stripping — Owner Pre-Work Uncertainty
The RFP (§3.3.2) notes that topsoil stripping is the Proponent's responsibility "if not already performed by Owner." At the time of specification writing, it may not be confirmed what pre-work the County will have completed. The specification should include a topsoil stripping section, with a note that quantity may be reduced based on pre-construction condition survey.
Source: RFP §3.3.2; Decomposition D-010.

### Concrete Pad Specifications

**Terminology Note:** The RFP and Appendix B use "cement pads" colloquially, but the technically correct term is "concrete pads" (cement is a component of concrete, not the finished material). The civil specification should use "concrete pads" throughout. Datasheet.md and Specification.md have been updated to reflect this; all documents should use "concrete pads" for consistency. See item X-002 in _SEMANTIC_LENSING.md.

Appendix B (conceptual drawings) shows concrete pad locations. The civil specification should include concrete mix design requirements, reinforcement (if any), thickness, and surface finish appropriate for heavy equipment use. Detailed dimensions and reinforcement design will come from the structural engineer (PKG-002 interface).
Source: Appendix B (Shop); SOW-0078.

### Coordination with County-Performed Bulk Works
The County is performing brushing, clearing, and bulk cut and fill (SOW-0200, SOW-0201). The civil specification and drawings must establish the finished subgrade condition that the County's bulk cut and fill must achieve, so that Proponent civil works can begin from a defined base. This handoff criterion should be documented.
Source: RFP §3.3.1.

### Warranty and Guarantee Period Obligations
Under the CCDC 14-2013 contract, the 2-year guarantee period (construction period + 2 years post-CCC) applies to all civil works. TBD: the specification should define what constitutes acceptable performance during the guarantee period for civil elements, including but not limited to:
- Driving surface rutting tolerance (maximum allowable rut depth under normal traffic before repair is required).
- Drainage performance maintenance (positive drainage to be maintained; no new ponding areas).
- Concrete pad surface condition (no unacceptable cracking, spalling, or settlement).
- Grading integrity (no erosion-induced changes to finished grades that affect drainage).

Without defined performance criteria, dispute resolution during the guarantee period will lack an objective basis. The Civil Engineer should establish measurable acceptance thresholds in the specification.
Source: Guidance.md Purpose (2-year guarantee period); CCDC 14-2013 (RFP §2.7); SOW-0120, SOW-0121. See item A-005 in _SEMANTIC_LENSING.md.

### Climate Adaptation Considerations
TBD: confirm whether climate change adaptation factors should be applied to design storm calculations for this site. Given the active landfill context and potentially long operational design life, current design storm standards may not adequately account for increasing storm intensity trends in Central Alberta. The Civil Engineer should consider whether a climate adjustment factor is warranted for the drainage design return period (REQ-CIVIL-003) and document the rationale for the chosen approach in the Civil Calculation Package (DEL-005-06).
Source: Specification.md REQ-CIVIL-003; see item E-002 in _SEMANTIC_LENSING.md.

---

## Trade-offs

| Trade-off | Option A | Option B | Recommended Approach |
|---|---|---|---|
| Gravel surface thickness | Design for average landfill equipment loads (lighter, cheaper) | Design for maximum expected load (motor scraper) | Option B — RFP explicitly requires motor scraper capacity (RFP §3.3.2); under-designing creates liability during guarantee period |
| Drainage design storm frequency | 1:10 year storm (common for site works) | 1:25 or higher (more conservative) | TBD — Civil Engineer to determine based on applicable Alberta standards and site context; RFP only states "future storm events" without specifying return period |
| Specification format | Narrative/prescriptive only | CSI MasterFormat structured | ASSUMPTION: CSI format preferred for coordination with other disciplines and subcontractor clarity; human to confirm |
| Mud sump scope division | Civil specifies entire sump | Civil specifies only excavation/backfill; plumbing specifies sump vessel | Recommended: Civil specifies earthworks/backfill; Plumbing specifies sump vessel and connection — consistent with CSI division of work |

---

## Examples

No specific precedent examples from accessible sources. The following is contextual guidance only:

- For a motor scraper-class gravel driving surface in Alberta, typical granular base depths range from 300 mm to 600 mm over prepared subgrade, depending on subgrade bearing capacity. ASSUMPTION: actual design depth must come from geotechnical report. Do not adopt these illustrative values without geotechnical support.
- CSI Section 31 20 00 (Earth Moving) and 32 11 23 (Aggregate Base Courses) are commonly used for gravel driving surfaces on institutional and industrial sites in Alberta. ASSUMPTION: subject to Civil Engineer's preference and project-specific requirements.

---

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|---|---|---|---|---|---|---|
| CF-CIVIL-01 | Topsoil stripping scope is conditional on Owner pre-works: the RFP says the Proponent strips topsoil "if not already performed by Owner," but the decomposition (D-010) treats this as assumed required. If the County performs stripping before construction, the specification quantity and cost are moot. | RFP §3.3.2 — "if not already performed by Owner" | Decomposition D-010 — "assumed required" | Specification.md REQ-CIVIL-006; Procedure.md Step 3 | Include the stripping specification section, note the conditional; confirm with County at project award whether pre-stripping is complete. | TBD |
| CF-CIVIL-02 | County supplies aggregate (OUT of scope), but the civil specification must set quality/gradation standards the aggregate must meet. Who is responsible for testing County-supplied aggregate to confirm specification compliance? | Decomposition §4 (SOW-0203) — supply is County responsibility | RFP §3.3.2 / CCDC 14–2013 — Proponent responsible for quality control | Specification.md REQ-CIVIL-004; Procedure.md Records | Civil Engineer to recommend; likely Proponent tests incoming aggregate or County certifies conformance. | TBD |
