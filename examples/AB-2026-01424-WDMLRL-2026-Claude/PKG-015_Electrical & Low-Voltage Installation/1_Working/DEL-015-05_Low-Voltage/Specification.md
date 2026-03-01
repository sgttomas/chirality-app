# Specification — DEL-015-05 Low-Voltage Systems

---

## Scope

### Included

This deliverable covers the installation of low-voltage signal and communication wiring for the New North Shop addition at the West Dried Meat Lake Regional Landfill, specifically:

1. **Security camera wiring** (SOW-0064): Supply and install all rough-in wiring, conduit, and termination infrastructure required to support security cameras at locations defined in the IFC Low-Voltage System Plans (DEL-004-07).
2. **2-way radio antenna wiring** (SOW-0065): Supply and install antenna wire/cabling and associated rough-in conduit or sleeves required to support 2-way radio communication at locations defined in the IFC Low-Voltage System Plans (DEL-004-07).

> **Scope boundary clarification (CONF-015-05-01):** The phrase "wiring for security cameras" is interpreted as passive rough-in infrastructure (conduit, cable, junction boxes, terminations to patch panel or junction point). Whether active components such as PoE injectors, network switches, or patch panels are included is TBD -- confirm with Owner/Electrical Engineer per CONF-015-05-01. [Lensing: A-001]

**Source:** Decomposition §3G (SOW-0064, SOW-0065); App B-Elec (Electrical Notes); _CONTEXT.md

### Excluded

The following are not part of this deliverable:

- Supply or installation of security camera heads, housings, recording equipment (NVR/DVR), or network switches — ASSUMPTION: excluded based on "wiring for security cameras" language in SOW-0064/App B-Elec; confirm with Owner/Electrical Engineer.
- Supply or installation of 2-way radio base stations, antennas, or radio equipment — ASSUMPTION: excluded based on "antenna wire" language in SOW-0065/App B-Elec; confirm.
- Low-voltage control wiring for HVAC, overhead doors, or equipment — covered by other DEL-015-xx deliverables or PKG-013.
- Data networking (structured cabling / IT network) — not referenced in RFP or decomposition; status TBD.
- High-voltage power wiring (covered by DEL-015-01 through DEL-015-04).

> **Commissioning scope note:** The verification/commissioning scope for this deliverable is contingent on the resolved scope boundary (CONF-015-05-01/02). If scope is wiring-only, commissioning means cable continuity verification and handoff to Owner/integrator. If scope includes active components, commissioning includes functional testing. Owner to confirm commissioning definition once scope boundary is resolved. [Lensing: X-003]

---

## Requirements

### REQ-015-05-01 — Security Camera Wiring Installation
**Statement:** The Electrical Contractor shall install wiring for security cameras as shown on the IFC Electrical/Low-Voltage drawings.
**Basis:** SOW-0064 (Decomposition §3G); App B-Elec (Electrical Notes: "Wiring for Security Cameras").
**Mandatory:** Yes.

### REQ-015-05-02 — Antenna Wire for 2-Way Radios
**Statement:** The Electrical Contractor shall install antenna wire for 2-way radios as shown on the IFC Electrical/Low-Voltage drawings.
**Basis:** SOW-0065 (Decomposition §3G); App B-Elec (Electrical Notes: "Antenna Wire for 2 Way Radios").
**Mandatory:** Yes.

### REQ-015-05-03 — Compliance with IFC Drawings
**Statement:** All low-voltage wiring installation shall conform to the Issued for Construction (IFC) Low-Voltage System Plans (DEL-004-07) and Electrical Specification (DEL-004-09) once issued. Where conflict exists between this specification and the IFC drawings, the IFC drawings govern.
**Basis:** RFP §3.3.2; RFP §3.4 (design-build framework).
**Note:** IFC drawings are not yet issued; this requirement is a forward reference. — ASSUMPTION: DEL-004-07 will provide routing, quantities, and cable specifications.

### REQ-015-05-04 — Alberta Safety Code Compliance
**Statement:** All low-voltage installation shall comply with the applicable Alberta Safety Codes and the Alberta Electrical Code (CEC Part I as adopted by Alberta) in force at the time of construction.
**Basis:** RFP §3.3.2 ("The proposed building must adhere to all Alberta Safety Codes"); RFP §3.4.
**Note:** Specific code edition TBD -- Electrical Engineer to confirm applicable code edition (e.g., "CEC 2024 as adopted by Alberta via STANDATA LEG-ELC-25-R1" or equivalent current adoption). Pinning the edition avoids ambiguity if editions change during project lifecycle. STANDATA requirements -- location TBD in DEL-004-09 (Electrical Specification). [Lensing: A-003]

### REQ-015-05-05 — P.Eng.-Stamped IFC Documentation
**Statement:** All IFC drawings for the low-voltage systems shall be signed and stamped by a professional engineer licensed to practice in the Province of Alberta before construction work commences.
**Basis:** RFP §3.3.2 ("All Issued For Construction Drawings must be signed/stamped by a professional engineer licensed to practice in the province of Alberta").
**Responsible party:** Electrical Engineer (PKG-004 / DEL-004-07 design team); this requirement constrains when DEL-015-05 installation may begin.

### REQ-015-05-06 — Inspection Coordination
**Statement:** The Electrical Contractor shall submit all required inspection requests for low-voltage work. The County project representative must be present for all inspections and shall be provided with a copy of all complete inspection reports.
**Basis:** RFP §3.3.2 ("Submit all inspection requests... County project representative must be present for all inspections").

### REQ-015-05-07 — Completion Deadline
**Statement:** All low-voltage installation work shall be complete, inspected, and commissioned on or before December 31, 2026.
**Basis:** RFP §3.1 ("All Work... must be completed on or before December 31, 2026").

### REQ-015-05-08 — Guarantee Period
**Statement:** All materials and workmanship shall be warranted for a period of two (2) years following the date of the Construction Completion Certificate (CCC). Defects shall be rectified within 10 days of written Owner instruction.
**Basis:** RFP §2.10.2; §2.10.6.

### REQ-015-05-09 — Coordination with Upstream Dependencies
**Statement:** The Electrical Contractor shall coordinate low-voltage rough-in with the Equipment Power Circuit installation (DEL-015-04) and with the structural/envelope work to ensure sleeve and conduit penetrations are incorporated prior to concrete pours or wall closures.
**Basis:** _DEPENDENCIES.md (upstream: DEL-015-04); RFP §3.3.2 (coordinate communication lines).
**ASSUMPTION:** Sleeve/penetration coordination is required given concrete structure (35' ceiling building per RFP §3.4). Exact coordination protocol TBD in construction schedule.
**Note (separation distance):** Minimum separation distance between low-voltage and power wiring per Alberta Electrical Code (CEC Section 16) must be maintained. Electrical Engineer to specify separation distance requirement applicable to shared conduit pathways with DEL-015-04. [Lensing: F-001]

---

## Standards

| Standard | Applicability | Accessibility |
|---|---|---|
| Alberta Electrical Code (CEC Part I, adopted by Alberta) | Governing electrical installation standard for Alberta | ASSUMPTION: likely applicable; specific edition location TBD in DEL-004-09 |
| Alberta Safety Codes Act | Overarching code compliance framework | RFP §3.3.2; §3.4 |
| CCDC 14–2013 | Contract form governing all obligations | RFP §2.7 |
| DEL-004-07 Low-Voltage System Plans | Project-specific IFC drawings (when issued) | Not yet issued |
| DEL-004-09 Electrical Specification | Project-specific material and workmanship standards (when issued) | Not yet issued |

> Note: No additional low-voltage-specific standards (e.g., TIA-568, BICSI, CSA T530) were referenced in the RFP or conceptual drawings. Whether such standards apply will be determined by the Electrical Engineer in DEL-004-07/DEL-004-09. Rationale for current omission: the RFP and conceptual drawings reference only general Alberta Electrical Code compliance; no structured cabling or telecommunications standards are cited because the scope is limited to security camera wiring and radio antenna wiring (not data networking). If DEL-004-09 introduces structured cabling standards, this section shall be updated accordingly. [Lensing: C-002] — ASSUMPTION: Standard industry practice for security camera and antenna rough-in in Alberta industrial facilities will apply where not otherwise specified.

> **Workmanship standards:** TBD -- no workmanship acceptance criteria currently exist (e.g., conduit support spacing, bend radius limits, pull tension limits). Record workmanship standards once DEL-004-09 is issued, as DEL-004-09 will define material and workmanship standards for this scope. [Lensing: X-002]

---

## Verification

| Requirement ID | Verification Method | Verified By | Timing |
|---|---|---|---|
| REQ-015-05-01 | Visual inspection; comparison against IFC drawing (DEL-004-07) as-installed. Quantitative acceptance criteria TBD -- Electrical Engineer to define measurable thresholds in DEL-004-09 (e.g., cable continuity test pass/fail, insulation resistance threshold, conduit fill percentage limit). [Lensing: A-005] | Electrical Contractor; County representative | Prior to wall/ceiling closure; at final inspection |
| REQ-015-05-02 | Visual inspection; comparison against IFC drawing (DEL-004-07) as-installed. Quantitative acceptance criteria TBD -- Electrical Engineer to define measurable thresholds in DEL-004-09 (e.g., antenna cable continuity, insulation resistance). [Lensing: A-005] | Electrical Contractor; County representative | Prior to wall/ceiling closure; at final inspection |
| REQ-015-05-03 | Drawing review; field verification against IFC drawings | Electrical Engineer; Electrical Contractor | During construction and at final inspection |
| REQ-015-05-04 | Safety Code inspection (Alberta permit authority) | Safety Codes Officer; Electrical Contractor | Per permit inspection schedule |
| REQ-015-05-05 | Document review — confirm P.Eng. stamp on IFC drawings prior to construction start | Design-Builder; Electrical Contractor | Before installation commences |
| REQ-015-05-06 | Inspection request records; County sign-off on inspection reports | County project representative | Per inspection schedule |
| REQ-015-05-07 | Project schedule milestone; Construction Completion Certificate | Design-Builder; County | By December 31, 2026 |
| REQ-015-05-08 | Warranty documentation submitted at CCC; defect tracking during guarantee period | County; Electrical Contractor | Post-CCC |
| REQ-015-05-09 | Pre-construction coordination meeting records (formal record with required attendees and sign-off -- see Procedure Records table [Lensing: F-002]); shop drawing review | Design-Builder; Electrical Contractor | Pre-construction / prior to slab pours |

---

## Documentation

### Anticipated Artifacts

| Artifact | Description | When Required |
|---|---|---|
| IFC Low-Voltage System Plans (DEL-004-07) | P.Eng.-stamped installation drawings defining routes, terminations, and quantities | Before installation commences |
| Electrical Specification (DEL-004-09) | Material and workmanship standards for low-voltage work | Before installation commences |
| Safety Code Permit | Electrical permit issued by Alberta Safety Codes authority | Before installation commences |
| Inspection Reports | Copies of all inspection reports, co-signed by County representative | At each inspection milestone |
| As-Built Drawings | Record drawings showing actual installed routing of security camera wiring and antenna cabling. As-built scope to include: routing deviations from IFC, cable test results summary, labeling schedule as-installed, and conduit fill documentation (TBD -- Design-Builder to confirm required as-built content). [Lensing: E-001] | At project closeout / CCC |
| Warranty Documentation | Contractor warranty letter covering 2-year guarantee period for all materials and workmanship per REQ-015-05-08. Warranty shall cover all materials and workmanship without exclusion unless specific exclusions are pre-approved by the Owner in writing; any permitted exclusion categories TBD. [Lensing: E-002] | At CCC submission |
| Lien Holdback Release Documents | WCB clearance letter and statutory declaration per RFP §2.13.2. Required for contractual closeout. [Lensing: X-004] | At CCC submission |
| Construction Completion Certificate (CCC) | Owner-issued certificate confirming acceptance | At project completion |
