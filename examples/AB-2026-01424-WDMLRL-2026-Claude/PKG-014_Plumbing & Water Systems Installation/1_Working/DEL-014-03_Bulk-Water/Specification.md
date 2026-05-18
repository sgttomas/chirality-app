# Specification — DEL-014-03 Bulk Water Fill System

**Document Type:** Specification (normative)
**Deliverable ID:** DEL-014-03
**Package:** PKG-014 — Plumbing & Water Systems Installation
**Revision:** R1 — 2026-02-26
**Status:** SEMANTIC_READY
**Enrichment Pass:** P3 (Semantic Lensing applied)

---

## Scope

### What This Deliverable Covers

DEL-014-03 covers the supply, installation, and commissioning of the Bulk Water Fill System at the West Dried Meat Lake Regional Landfill Maintenance Shop Addition. This includes:

- The high-volume pump used for external filling of the cistern or water transport vehicles
- The fill line(s) from pump to exterior fill point
- The exterior fill connection point (coupling, hardware, protection enclosure as required)
- All associated piping, valves, fittings, and supports within the bulk fill system boundary
- Electrical coordination for pump power supply (power circuit itself is under DEL-015-04)
- Pressure and flow testing of the completed system
- Integration with the 50,000L cistern (DEL-014-01)

### What This Deliverable Excludes

- Design of the bulk fill system (under PKG-006 — Plumbing Design, DEL-006-04 and associated drawings)
- The 50,000L cistern and internal distribution pump (under DEL-014-01)
- Electrical power circuits to pump motor (under DEL-015-04 — Equipment Power Circuits)
- Site bulk cut and fill earthworks (County-provided; SOW-0201, OUT of Proponent scope)
- Plumbing fixtures (under DEL-014-06)
- Floor and sump drains (under DEL-014-04)

---

## Requirements

### REQ-014-03-01 — System Function
The bulk water fill system shall provide high-volume external filling capability, enabling bulk water delivery to the cistern at the exterior of the building.

**Source:** RFP S3.4 — "Bulk water fill. With high volume pump for external filling."
**Classification:** Mandatory
**Note:** The RFP language "for external filling" is directional toward cistern replenishment. Whether the system must also support water *extraction* (pumping from cistern to vehicles) is unresolved. See Conflict Table C-003 in Guidance.md. **TBD -- Owner/PM to confirm scope of "external filling."** *(Semantic Lensing E-004)*

---

### REQ-014-03-02 — Pump Performance
The pump shall be rated as "high volume" for external filling purposes. Specific flow rate in LPM shall be confirmed in the plumbing design (PKG-006 IFC documents).

**Source:** RFP S3.4 (location: S3.4, pump performance TBD in IFC design)
**Note:** The 100 LPM / 2.5" connection specified in RFP S3.4 is associated with the internal cistern distribution pump (SOW-0042/DEL-014-01), not the bulk fill pump. The bulk fill pump flow rate is not explicitly stated in available sources. Design to confirm. **(TBD — design confirmation required)**

---

### REQ-014-03-03 — Exterior Fill Point Location
The bulk water fill *connection point* shall be located on the exterior of the building as indicated on the conceptual plumbing drawing (App B — Plumbing), on the north face of the building.

**Source:** R-06 (Appendix B — Plumbing conceptual drawing)
**Note:** This requirement specifies the *fill connection point* location. The pump location (indoor utility room vs. near exterior wall) is a separate design decision to be resolved in IFC drawings (PKG-006). See Guidance.md T-1 for pump location trade-off discussion and Conflict Table C-004. Exact fill point location to be confirmed in IFC plumbing drawings. *(Semantic Lensing E-003)*

---

### REQ-014-03-04 — Cistern Integration
The bulk fill system shall connect to and be compatible with the 50,000L cistern installed under DEL-014-01. The fill line shall terminate at or interface with the cistern filling connection.

**Source:** _CONTEXT.md ("Integration with cistern system"); RFP S3.4; _DEPENDENCIES.md
**Classification:** Mandatory

---

### REQ-014-03-05 — Code Compliance
The installation shall comply with all applicable Alberta Safety Codes and plumbing regulations in force at the time of construction, including the Alberta Plumbing Code (National Plumbing Code as adopted in Alberta; specific edition/year to be confirmed -- see Standards table).

**Source:** RFP S3.3.2 ("The proposed building must adhere to all Alberta Safety Codes")
**Classification:** Mandatory

---

### REQ-014-03-06 — Backflow Prevention
A backflow prevention device appropriate to the hazard level shall be installed as required by the applicable plumbing code.

**Source:** ASSUMPTION — standard requirement under Alberta Plumbing Code for systems connected to potable/service water cisterns. Specific device type TBD in plumbing design (PKG-006). **Confirm with plumbing engineer: identify specific Alberta Plumbing Code clause and applicable CSA B64 series standard that mandates backflow prevention for this application.** If confirmed, reclassify this requirement from ASSUMPTION to Mandatory with code citation. *(Semantic Lensing A-001)*
**Classification:** ASSUMPTION — confirm with plumbing engineer

---

### REQ-014-03-07 — Freeze Protection
The system shall incorporate provisions to prevent freeze damage to the pump, fill line, and exterior connection point, appropriate for Alberta Central region winter conditions.

**Source:** ASSUMPTION — site location near Ferintosh, Alberta subject to sustained sub-zero temperatures. Specific measures (heat trace, drain-back, insulation enclosure) TBD in plumbing design (PKG-006). **Plumbing engineer / design team to confirm whether this can be elevated to Mandatory with code citation (Alberta Plumbing Code or Alberta Building Code provisions for freeze protection of plumbing systems).** *(Semantic Lensing A-002)*
**Classification:** ASSUMPTION — confirm with plumbing engineer

---

### REQ-014-03-08 — Electrical Coordination
The pump motor shall be connected to an electrical circuit provided under DEL-015-04 (Equipment Power Circuits). The Plumbing Contractor shall coordinate motor electrical specifications with the Electrical Contractor in advance of rough-in.

**Source:** ASSUMPTION — standard coordination requirement between plumbing and electrical subcontractors. Power circuit scope boundary confirmed by decomposition (PKG-015 vs PKG-014). **Plumbing engineer / design team to confirm whether this can be elevated to Mandatory with confirmed authority.** *(Semantic Lensing A-002)*
**Classification:** ASSUMPTION

---

### REQ-014-03-09 — IFC Drawing Compliance
Installation shall be executed in strict conformance with the Issued for Construction (IFC) plumbing drawings stamped by a P.Eng. licensed in Alberta, to be produced under PKG-006.

**Source:** RFP S3.3.2 — "All Issued For Construction Drawings must be signed/stamped by a professional engineer licensed to practice in the province of Alberta."
**Classification:** Mandatory

---

### REQ-014-03-10 — Guarantee Period
All materials and workmanship shall be guaranteed for the construction period plus a two-year warranty period following the Construction Completion Certificate (CCC), per contract terms.

**Source:** RFP S2.10
**Classification:** Mandatory

---

### REQ-014-03-11 — OH&S Compliance During Installation
All installation work under DEL-014-03 shall comply with Alberta Occupational Health and Safety (OH&S) legislation and the Prime Contractor's site-specific OH&S program (DEL-019-01). The Plumbing Contractor shall adhere to all applicable OH&S requirements during the installation period.

**Source:** RFP S2.15 (Prime Contractor obligations); SOW-0083 (Prime Contractor OH&S Program under DEL-019-01). **Note:** Alberta OH&S was listed in the Standards table but had no corresponding requirement; this requirement formalizes that flow-down. *(Semantic Lensing D-001)*
**Classification:** Mandatory

---

### REQ-014-03-12 — OBJ-004 Traceability
The bulk water fill system installation and commissioning shall satisfy DEL-014-03's contribution to OBJ-004 ("Install and commission all mechanical, plumbing, and water storage systems to operational readiness"). The system shall be demonstrated as operationally ready as part of the building systems commissioning (DEL-020-01) and this demonstration shall be documented as evidence of OBJ-004 partial fulfillment.

**Source:** Decomposition S5 (OBJ-004); _CONTEXT.md (Objectives: OBJ-004); Datasheet References. **Note:** OBJ-004 was referenced in supporting documents but had no explicit verification criterion traceable to this deliverable. *(Semantic Lensing D-003)*
**Classification:** Mandatory

---

## Standards

| Standard / Code | Description | Applicability | Status |
|---|---|---|---|
| Alberta Plumbing Code (National Plumbing Code as adopted in Alberta) | Governing plumbing installation code | Mandatory — all plumbing work | Applicable — **specific edition/year TBD; PM / plumbing engineer to confirm applicable edition in force at time of construction** *(Semantic Lensing A-003)* |
| Alberta Safety Codes Act | Overarching safety code framework for Alberta | Mandatory | RFP S3.3.2 |
| CCDC 14-2013 | Design-Build Stipulated Price Contract | Contract form | RFP S2.7 |
| Alberta OH&S | Occupational Health & Safety — Prime Contractor obligations | Mandatory during construction | RFP S2.15; SOW-0083; now addressed in REQ-014-03-11 *(Semantic Lensing D-001)* |
| CSA B64 series | Backflow prevention devices | ASSUMPTION — **confirm applicability with plumbing engineer; if confirmed as applicable, change status to "Applicable" with specific standard number** *(Semantic Lensing C-001)* | location TBD |

---

## Verification

| Requirement | Verification Method | Responsibility | Timing | Acceptance Criteria |
|---|---|---|---|---|
| REQ-014-03-01 (System Function) | Operational test — demonstrate external fill capability at completion | Plumbing Contractor | Commissioning | Water is delivered from exterior fill point to cistern; system operates without fault |
| REQ-014-03-02 (Pump Performance) | Pump performance test — measure flow rate against design spec | Plumbing Contractor | Commissioning | Achieved flow rate (LPM) meets or exceeds the design specification value established in PKG-006 IFC documents. **TBD — quantitative acceptance criterion (LPM) to be added when IFC design confirms pump flow rate specification.** *(Semantic Lensing A-005)* |
| REQ-014-03-03 (Exterior Location) | Visual inspection against IFC drawings | Plumbing Contractor / Owner Rep | Rough-in inspection + final inspection | Fill connection point installed at location shown on IFC drawings (north face of building per conceptual drawing) |
| REQ-014-03-04 (Cistern Integration) | Visual inspection of connections; fill test demonstrating water delivery to cistern | Plumbing Contractor | Commissioning | Physical connection complete; cistern level increases during pump operation from exterior fill point |
| REQ-014-03-05 (Code Compliance) | Safety Code inspection and sign-off | Safety Codes Officer | During/after construction | Safety Codes Officer issues passing inspection report with no outstanding deficiencies |
| REQ-014-03-06 (Backflow Prevention) | Inspection of installed device against design specification | Safety Codes Officer / Plumbing Contractor | Inspection | Device installed per plumbing engineer specification and applicable code; device test passes per manufacturer and code requirements |
| REQ-014-03-07 (Freeze Protection) | Design review (confirm measures in IFC); site inspection of installed provisions | Plumbing Engineer / Contractor | Design review + installation | Freeze protection measures match IFC specification; heat trace continuity confirmed (if applicable); drain-back operates correctly (if applicable) |
| REQ-014-03-08 (Electrical Coordination) | Coordination documentation review; motor nameplate vs. circuit specification comparison | Plumbing + Electrical Contractors | Pre-rough-in | **Signed coordination form or meeting minutes on file confirming motor specifications (voltage, phase, amperage) match the electrical circuit provided under DEL-015-04. Motor nameplate data matches circuit breaker rating.** *(Semantic Lensing F-002)* |
| REQ-014-03-09 (IFC Drawing Compliance) | As-built mark-up review; red-line as-built drawings | Plumbing Contractor | Closeout | **As-built drawings reflect all deviations from IFC; red-line mark-ups signed and dated by site foreman; all field changes documented with RFI/change order reference where applicable.** *(Semantic Lensing X-003)* |
| REQ-014-03-10 (Guarantee Period) | Contract compliance; defect log during 2-year warranty period | Owner / Plumbing Contractor | Post-CCC | No unresolved warranty defects at end of guarantee period |
| REQ-014-03-11 (OH&S Compliance) | OH&S program compliance monitoring; incident reporting | PM / Safety Coordinator | During construction | Zero OH&S violations attributable to DEL-014-03 installation work; compliance with Prime Contractor OH&S program (DEL-019-01) |
| REQ-014-03-12 (OBJ-004 Traceability) | Operational readiness demonstration as part of DEL-020-01 building systems commissioning | Commissioning Agent / PM | Commissioning | Bulk water fill system demonstrated as operationally ready; commissioning record documents OBJ-004 partial fulfillment for this deliverable *(Semantic Lensing D-003)* |
| Pressure Test | Pressure test of fill line per Alberta Plumbing Code | Plumbing Contractor | After completion, before commissioning | **TBD — specific test pressure (kPa/psi), hold duration, and pass/fail criteria to be confirmed from applicable Alberta Plumbing Code clause or plumbing engineer specification. Zero leakage at required test pressure for required duration.** *(Semantic Lensing F-001)* |

---

## Documentation

### Required Artifacts

| Artifact | Description | Responsible | Timing |
|---|---|---|---|
| IFC Plumbing Drawings | Pump and fill line details (produced under DEL-006-04) | Plumbing Engineer (PKG-006) | Pre-construction |
| Pump Submittals | Manufacturer data sheets, pump curves, performance data | Plumbing Contractor | Pre-installation |
| Safety Code Inspection Report | Plumbing inspection sign-off | Safety Codes Officer | During/after installation |
| Commissioning Record | Pump performance test results; system operational verification; OBJ-004 partial fulfillment evidence | Plumbing Contractor / Commissioning Agent | Commissioning phase |
| As-Built Drawings | Red-lined or updated drawings reflecting installed condition; signed and dated by site foreman | Plumbing Contractor | Closeout |
| Warranty Documentation | Pump and equipment manufacturer warranties | Plumbing Contractor | Closeout |
| Operations & Maintenance Manual (O&M) | Pump operation, maintenance schedule, winterization procedure | Plumbing Contractor | Closeout |
| Electrical Coordination Record | Signed coordination form or meeting minutes confirming motor-to-circuit compatibility | Plumbing Contractor + Electrical Contractor | Pre-rough-in |

---

## Semantic Lensing Enrichment Log (Pass 3)

| ItemID | Action Taken |
|---|---|
| A-001 | REQ-014-03-06 note expanded to request specific code clause and CSA B64 confirmation |
| A-002 | REQ-014-03-07 and REQ-014-03-08 notes expanded to request elevation to Mandatory if code-confirmed |
| A-003 | Standards table Alberta Plumbing Code entry updated to request specific edition/year confirmation |
| A-005 | Verification table REQ-014-03-02 row updated with TBD quantitative acceptance criterion note |
| C-001 | Standards table CSA B64 entry updated with request to confirm and elevate from ASSUMPTION |
| C-002 | Plumbing code terminology harmonized to "Alberta Plumbing Code (National Plumbing Code as adopted in Alberta)" throughout |
| D-001 | New REQ-014-03-11 added for OH&S compliance flow-down; Standards table cross-referenced |
| D-003 | New REQ-014-03-12 added for OBJ-004 traceability; Verification and Documentation rows added |
| E-003 | REQ-014-03-03 note clarified to distinguish fill point location from pump location; cross-referenced Guidance T-1 and Conflict Table |
| E-004 | REQ-014-03-01 note updated to flag bidirectional ambiguity; cross-referenced Conflict Table C-003 |
| F-001 | Pressure test row added to Verification table with TBD for specific test parameters |
| F-002 | REQ-014-03-08 verification row updated with explicit acceptance format (signed coordination form) |
| X-003 | REQ-014-03-09 verification acceptance criteria expanded with specific as-built standard |
